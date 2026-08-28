#!/usr/bin/env python3
"""Auto-fetch the org structure DRAFT from live ClickUp + Slack data — minimum
Principal input by design: he corrects a numbered table, he never fills a form.

Pulls: workspace members (name/email/role), spaces/folders/lists (the de-facto
departments), user groups, and recent tasks per list (~200) for real assignment
patterns. Cross-matches ClickUp members to the Slack roster BY EMAIL (needs the
bot scope `users:read.email`; if emails come back empty the script says so and
falls back to name-matching at LOWER confidence — flagged per row).

Output: docs/ORG-STRUCTURE.md, status DRAFT, as a numbered table:
  # · Name · ClickUp ID · email · Slack ID · department (inferred) · role
  (inferred) · confidence · evidence
UNPLACED people stay in an UNPLACED section — never guessed into a department.

CONFIRMATION PROTOCOL (the gate the assignment engine depends on):
  The Principal replies with row-number corrections ONLY ("3: HOD Graphics ·
  7: guest, skip"); a blank reply = all rows confirmed. The desk then edits the
  rows and flips the file header to CONFIRMED with the date. The assignment
  engine (meeting step) reads ONLY rows in a file whose header says CONFIRMED.

Usage: python3 scripts/org_fetch.py [--write]   (default prints; --write saves)
"""
import os, sys, collections, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clickup as C
from slack import sl

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'docs', 'ORG-STRUCTURE.md')
TASK_SAMPLE_PAGES = 2      # 100/page -> ~200 recent tasks per list

def teams():
    st, r = C.api('GET', '/team')
    if st != 200:
        raise SystemExit(f'ClickUp /team: HTTP {st} {r}')
    return r.get('teams', [])

def structure(team_id):
    """spaces -> folders -> lists (+ folderless lists). Returns [(space, folder
    or None, list)] — each list is a candidate department signal."""
    out = []
    st, r = C.api('GET', f'/team/{team_id}/space?archived=false')
    for sp in r.get('spaces', []) if st == 200 else []:
        st2, rf = C.api('GET', f"/space/{sp['id']}/folder?archived=false")
        for fo in rf.get('folders', []) if st2 == 200 else []:
            for li in fo.get('lists', []):
                out.append((sp['name'], fo['name'], li))
        st3, rl = C.api('GET', f"/space/{sp['id']}/list?archived=false")
        for li in rl.get('lists', []) if st3 == 200 else []:
            out.append((sp['name'], None, li))
    return out

def groups(team_id):
    st, r = C.api('GET', f'/group?team_id={team_id}')
    return r.get('groups', []) if st == 200 else []

def assignment_patterns(list_ids):
    """user_id -> Counter(list_name) over recent tasks: who actually works where."""
    pat = collections.defaultdict(collections.Counter)
    for lid, lname in list_ids:
        for page in range(TASK_SAMPLE_PAGES):
            st, r = C.api('GET', f'/list/{lid}/task?' + urllib.parse.urlencode(
                {'page': page, 'include_closed': 'true', 'order_by': 'updated',
                 'reverse': 'true'}))
            tasks = r.get('tasks', []) if st == 200 else []
            for t in tasks:
                for a in t.get('assignees', []):
                    pat[a.get('id')][lname] += 1
            if not tasks or r.get('last_page') is True:
                break
    return pat

def slack_roster():
    """[{'id','name','real','email'}] for human, non-deleted members.
    Returns (roster, emails_present: bool)."""
    out, cursor, emails = [], '', False
    while True:
        r = sl('users.list', limit=200, **({'cursor': cursor} if cursor else {}))
        if not r.get('ok'):
            print(f"WARN  Slack users.list failed: {r.get('error')} — Slack IDs will be blank", file=sys.stderr)
            return [], False
        for m in r.get('members', []):
            if m.get('deleted') or m.get('is_bot') or m.get('id') == 'USLACKBOT':
                continue
            email = (m.get('profile') or {}).get('email', '')
            emails = emails or bool(email)
            out.append({'id': m['id'], 'name': m.get('name', ''),
                        'real': (m.get('profile') or {}).get('real_name', ''),
                        'email': email})
        cursor = (r.get('response_metadata') or {}).get('next_cursor', '')
        if not cursor:
            return out, emails

def match_slack(member, roster, emails_present):
    """(slack_id, confidence, evidence). Email match = high; name = lower."""
    em = (member.get('email') or '').lower()
    if em and emails_present:
        for s in roster:
            if s['email'].lower() == em:
                return s['id'], 'high', f'email match ({em})'
    name = (member.get('username') or '').lower()
    for s in roster:
        if name and (name == s['real'].lower() or name == s['name'].lower()):
            return s['id'], 'low', 'name match only' + (
                '' if emails_present else ' — Slack emails unavailable (add users:read.email scope)')
    return '', 'none', 'no Slack match found'

def build():
    tms = teams()
    team = tms[0]
    if len(tms) > 1:
        print(f"WARN  {len(tms)} ClickUp workspaces visible; using '{team['name']}'", file=sys.stderr)
    members = [m.get('user', {}) for m in team.get('members', [])]
    struct = structure(team['id'])
    grps = groups(team['id'])
    pat = assignment_patterns([(li['id'], (fo or sp) + ' / ' + li['name'])
                               for sp, fo, li in struct])
    roster, emails_present = slack_roster()

    grp_of = {}
    for g in grps:
        for uid in g.get('members', []):
            grp_of.setdefault(uid if isinstance(uid, (int, str)) else uid.get('id'),
                              []).append(g.get('name'))

    rows, unplaced = [], []
    for m in sorted(members, key=lambda u: (u.get('username') or '').lower()):
        uid = m.get('id')
        sid, conf_s, ev_s = match_slack(m, roster, emails_present)
        top = pat.get(uid, collections.Counter()).most_common(2)
        dept, conf_d, ev_d = '', 'none', 'no recent task assignments'
        if grp_of.get(uid):
            dept, conf_d, ev_d = grp_of[uid][0], 'high', f"user group '{grp_of[uid][0]}'"
        elif top:
            dept, conf_d = top[0][0], ('medium' if top[0][1] >= 3 else 'low')
            ev_d = f'{top[0][1]} recent tasks in "{top[0][0]}"'
        role = {'1': 'owner', '2': 'admin', '3': 'member', '4': 'guest'}.get(
            str(m.get('role', '')), str(m.get('role', '')))
        conf = min(conf_s, conf_d, key=['high', 'medium', 'low', 'none'].index) \
               if dept and sid else 'low'
        row = (m.get('username') or '(no name)', str(uid), m.get('email') or '',
               sid, dept, role, conf, f'{ev_d}; {ev_s}')
        (rows if dept else unplaced).append(row)

    lines = ['# ORG STRUCTURE — HKGT DMT',
             '',
             '**STATUS: DRAFT — not yet confirmed by the Principal.**',
             'The assignment engine reads ONLY a CONFIRMED version of this file.',
             'Reply with row-number corrections only ("3: HOD Graphics · 7: guest,',
             'skip"); a blank reply confirms every row as printed.',
             '',
             '| # | Name | ClickUp ID | Email | Slack ID | Department (inferred) | Role | Confidence | Evidence |',
             '|---|---|---|---|---|---|---|---|---|']
    n = 0
    for r in rows:
        n += 1
        lines.append(f'| {n} | ' + ' | '.join(str(x) for x in r) + ' |')
    lines += ['', '## UNPLACED (no department signal — stays unplaced until the Principal places them)', '']
    for r in unplaced:
        n += 1
        lines.append(f'- {n}. {r[0]} (ClickUp {r[1]}, Slack {r[3] or "—"}, {r[5]}) — {r[7]}')
    lines += ['', f'_Sources: ClickUp workspace "{team["name"]}" (members, groups, '
              f'{len(struct)} lists, task sample); Slack roster '
              f'({"emails" if emails_present else "NO emails — users:read.email missing"})._']
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    text = build()
    if '--write' in sys.argv:
        open(OUT, 'w', encoding='utf-8').write(text)
        print(f'wrote {OUT} (STATUS: DRAFT — needs the Principal\'s row confirmation)')
    else:
        print(text)
