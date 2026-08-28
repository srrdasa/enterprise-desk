#!/usr/bin/env python3
"""Slack sweep that does not lose threaded replies.

TWO BUGS ARE FIXED HERE, both of which silently returned nothing rather than erroring.

WHY THIS EXISTS. The obvious sweep — conversations.history(oldest=window), then fetch
replies for the parents it returns — has a blind spot that cost us a real message on
19 Aug 2026. A stakeholder posted a critical document as a REPLY on a thread whose parent was from the previous day. The parent fell outside the history
window, so history never returned it, so its replies were never fetched, so the reply
was structurally invisible to the sweep. Nobody saw it for a day.

That is not an edge case. Almost every reply we receive lands on a thread the desk
itself started, and those parents age out of the window within a day or two. The naive
sweep therefore misses the majority of stakeholder replies by design.

THE FIX. conversations.history returns `latest_reply` on every thread parent. So: scan a
WIDE parent window (default 60 days), and fetch replies for any parent whose latest_reply
falls inside the actual sweep window — regardless of how old the parent is. Top-level
messages are still filtered on the sweep window as before.

SECOND BUG, and it is the one slack.py already warns about in its own docstring: an
`oldest` value with 7 fractional digits makes Slack return ok=true with ZERO messages.
`time.time() - days*86400` produces exactly that often enough to be maddening — the first
version of this file used str() and swept an empty workspace without a single error. Always
ts6(), never str().

Usage:  python3 scripts/slack_sweep.py [hours_back] [parent_days]
"""
import sys
import time

sys.path.insert(0, 'scripts')
from slack import sl, ts6

SKIP_SUBTYPES = {'channel_join', 'channel_leave', 'channel_topic',
                 'channel_purpose', 'channel_name', 'bot_add', 'bot_remove'}


def member_channels():
    out, cur = [], None
    while True:
        r = sl('conversations.list', types='public_channel,private_channel',
               limit=200, exclude_archived='true', **({'cursor': cur} if cur else {}))
        out += [c for c in r['channels'] if c.get('is_member')]
        cur = r.get('response_metadata', {}).get('next_cursor')
        if not cur:
            return out


def roster():
    users, cur = {}, None
    while True:
        r = sl('users.list', limit=200, **({'cursor': cur} if cur else {}))
        for u in r['members']:
            p = u.get('profile', {})
            users[u['id']] = p.get('display_name') or u.get('real_name') or u['name']
        cur = r.get('response_metadata', {}).get('next_cursor')
        if not cur:
            return users


def sweep(since_ts, parent_since_ts):
    """Return {channel_name: [messages]} for everything new since `since_ts`,
    INCLUDING replies on threads whose parent is older than the window."""
    found = {}
    for c in member_channels():
        new, seen = [], set()
        cur = None
        while True:
            r = sl('conversations.history', channel=c['id'],
                   oldest=ts6(parent_since_ts), limit=200,
                   **({'cursor': cur} if cur else {}))
            msgs = r.get('messages', [])
            for m in msgs:
                if m.get('subtype') in SKIP_SUBTYPES:
                    continue
                # a top-level message inside the sweep window
                if float(m['ts']) >= since_ts and m['ts'] not in seen:
                    seen.add(m['ts'])
                    new.append(m)
                # THE FIX: any thread whose newest reply landed inside the window,
                # however old the parent is.
                latest = m.get('latest_reply')
                if m.get('reply_count') and latest and float(latest) >= since_ts:
                    rr = sl('conversations.replies', channel=c['id'],
                            ts=m['ts'], limit=200)
                    for x in rr.get('messages', [])[1:]:
                        if float(x['ts']) >= since_ts and x['ts'] not in seen:
                            seen.add(x['ts'])
                            x['_parent_ts'] = m['ts']
                            x['_parent_preview'] = (m.get('text') or '')[:90]
                            new.append(x)
            cur = r.get('response_metadata', {}).get('next_cursor')
            if not cur or not msgs:
                break
        if new:
            found[c['name']] = sorted(new, key=lambda x: float(x['ts']))
    return found


def dm_checklist(users):
    """The bot token CANNOT see the Principal's DMs. Binding rule 7 requires every review
    cycle to sweep them, and for three weeks it silently did not: the channel sweep reported clean while a DM carried a sign-off nobody had read.
    A script cannot close this gap - reading the Principal's DMs needs the USER-SCOPED Slack
    connector, which is an MCP call, not an HTTP call with a bot token. So the script
    does the one thing it can: it makes the gap impossible to walk past."""
    print("\n" + "=" * 68)
    print("DM SWEEP IS NOT DONE. The bot token cannot see the Principal's DMs.")
    print("Binding rule: read EVERY id below with the user-scoped Slack connector")
    print("  mcp__Slack__slack_read_channel(channel_id=<USER ID>)  # a user id reads that DM")
    print("A sweep reported without this block worked through is INCOMPLETE - say so")
    print("rather than reporting it clean.")
    print("=" * 68)
    for uid, name in sorted(users.items(), key=lambda kv: kv[1]):
        print("  %-14s %s" % (uid, name))
    print("=" * 68)


def main():
    hours = float(sys.argv[1]) if len(sys.argv) > 1 else 24
    pdays = float(sys.argv[2]) if len(sys.argv) > 2 else 60
    now = time.time()
    since, psince = now - hours * 3600, now - pdays * 86400
    users = roster()
    found = sweep(since, psince)
    print("SWEEP: last %gh (threads scanned back %g days)" % (hours, pdays))
    for name, msgs in found.items():
        print("\n===== #%s  (%d)" % (name, len(msgs)))
        for m in msgs:
            who = users.get(m.get('user', ''), m.get('username') or '?')
            when = time.strftime('%d-%b %H:%M', time.localtime(float(m['ts'])))
            tag = ''
            if '_parent_ts' in m:
                tag = ' [REPLY on older thread: "%s..."]' % m['_parent_preview'][:60]
            files = [f.get('name') for f in (m.get('files') or [])]
            print("  [%s] %s%s" % (when, who, tag))
            if files:
                print("      FILES: %s" % files)
            print("      %s" % (m.get('text') or '').replace('\n', ' | ')[:600])
    dm_checklist(users)


if __name__ == '__main__':
    main()
