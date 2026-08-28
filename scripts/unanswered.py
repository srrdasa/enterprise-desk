#!/usr/bin/env python3
"""EXHAUSTIVE unanswered-message detector across every Slack channel + thread.

WHY THIS EXISTS (ported learning). A point-in-time sweep plus a human reading its
output through `tail` let real messages die silently on the originating desk — three
stakeholder requests sat unanswered for days while the daily digest reported "clean".

The fix is not a bigger sweep — it is a detector whose definition of DONE is
"we replied". An item stays unanswered until a message from the Principal or the desk
lands after it, so it RESURFACES on every review until it is closed. No separate
state file to drift: the live channel IS the state.

Definition of unanswered:
  * TOP-LEVEL: a human (not the desk, not the Principal) message with NO later
    top-level message from us in that channel, AND no thread reply from us.
  * THREAD: a thread whose LAST reply is from a human (not us).
Answered-by-others is shown flagged (not ours to chase, but confirm).

Identity from env: DESK_BOT_ID (the bot's Uxxxx), PRINCIPAL_SLACK_ID (the Principal's
Uxxxx), DESK_NAME. DESK_TZ_OFFSET_MIN (minutes from UTC, e.g. 330 for IST) for display.

Usage:  python3 scripts/unanswered.py [days]     # default 3
Never truncate this output with head/tail — read all of it. That truncation is the
exact bug this script exists to kill."""
import os, sys, time, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slack import sl

OURS = {os.environ.get('DESK_BOT_ID', ''), os.environ.get('PRINCIPAL_SLACK_ID', '')} - {''}
TZ = datetime.timezone(datetime.timedelta(minutes=int(os.environ.get('DESK_TZ_OFFSET_MIN', '0'))))

def _dt(ts):
    return datetime.datetime.fromtimestamp(float(ts), TZ).strftime('%d-%b %H:%M')

def _is_ours(m):
    return (m.get('user') in OURS) or (m.get('username') == os.environ.get('DESK_NAME', 'The Desk'))

def roster():
    r = sl('users.list', limit=400)
    return {u['id']: (u.get('real_name') or u.get('name')) for u in r.get('members', [])}

def find(days=3):
    cutoff = time.time() - days * 86400
    r = sl('conversations.list', types='public_channel,private_channel',
           limit=200, exclude_archived='true')
    chans = [c for c in r.get('channels', []) if c.get('is_member')]
    names = roster()
    out = []
    for c in sorted(chans, key=lambda x: x['name']):
        cid, nm = c['id'], c['name']
        h = sl('conversations.history', channel=cid, limit=60)
        msgs = [m for m in h.get('messages', [])
                if float(m['ts']) > cutoff and m.get('subtype') not in
                ('channel_join', 'channel_leave', 'channel_topic', 'channel_purpose')]
        msgs.sort(key=lambda m: float(m['ts']))
        last_our_top = max([float(m['ts']) for m in msgs if _is_ours(m)], default=0.0)
        for m in msgs:
            if m.get('reply_count', 0) > 0:
                tr = sl('conversations.replies', channel=cid, ts=m['ts'], limit=60)
                replies = tr.get('messages', [])[1:]
                if replies and not _is_ours(replies[-1]) and float(replies[-1]['ts']) > cutoff:
                    who = names.get(replies[-1].get('user', ''), '?')
                    out.append((nm, 'THREAD', who, replies[-1], m))
            elif not _is_ours(m) and float(m['ts']) > last_our_top:
                later_human = any(float(x['ts']) > float(m['ts']) and not _is_ours(x)
                                  and x.get('user') != m.get('user') for x in msgs)
                who = names.get(m.get('user', ''), m.get('username') or '?')
                out.append((nm, 'ANSWERED-BY-OTHERS?' if later_human else 'TOP', who, m, None))
    return out

def main():
    days = float(sys.argv[1]) if len(sys.argv) > 1 else 3
    if not OURS:
        print('WARNING: DESK_BOT_ID / PRINCIPAL_SLACK_ID not set — every message will '
              'look unanswered. Set them (see docs/SECRETS-SETUP.md).')
    items = find(days)
    print(f'UNANSWERED (last {days:g}d): {len(items)} items — read ALL of them, never tail this.')
    for nm, kind, who, m, parent in items:
        tag = f' [reply on: "{(parent.get("text") or "")[:60]}…"]' if parent else ''
        print(f'\n #{nm} [{kind}] {who} at {_dt(m["ts"])}{tag}')
        print(f'   {(m.get("text") or "")[:400]}')
    if not items:
        print('clean — every recent human message has a reply from us after it.')

if __name__ == '__main__':
    main()
