#!/usr/bin/env python3
"""Regenerate boards/otter-backlog.md from logs/otter-seen.jsonl.

The board is a GENERATED VIEW (CLAUDE.md single-registry rule): the ledger is the
source of truth, this file is the readable roll-up. Prints the authoritative
counts so a commit message never has to guess them — two commit messages have
already carried an off-by-one because the count was written before the regen ran.

Usage: python3 scripts/otter_board.py        # rewrite + print counts
       python3 scripts/otter_board.py --line # print the one-line summary only
"""
import json, re, sys, datetime

LEDGER = 'logs/otter-seen.jsonl'
BOARD  = 'boards/otter-backlog.md'
MARK   = {'FILED': '**FILED**', 'SKIPPED': 'SKIPPED', 'PROPOSED': '**PROPOSED**'}
ROW    = re.compile(r'\| (\d+) \| (\S+) \| (.+?) \| (.+?) \| (.+?) \| `(.+?)` \|')

def states():
    out = {}
    for line in open(LEDGER):
        if line.strip():
            e = json.loads(line)
            out[e['id']] = e['state']
    return out

def regenerate(write=True):
    st, txt = states(), open(BOARD).read()
    rows = ROW.findall(txt)
    for _, _, _, cur, title, tid in rows:
        want = MARK.get(st.get(tid, 'PENDING'), 'PENDING')
        if want != cur:
            txt = txt.replace(f'| {cur} | {title} | `{tid}` |',
                              f'| {want} | {title} | `{tid}` |')
    total = len(rows)
    pend  = sum(1 for r in rows if st.get(r[5], 'PENDING') == 'PENDING')
    done  = total - pend
    txt = re.sub(r'\*\*\d+ processed · \d+ PENDING\*\*',
                 f'**{done} processed · {pend} PENDING**', txt)
    txt = re.sub(r'Generated \d{4}-\d\d-\d\d \d\d:\d\d UTC',
                 'Generated ' + datetime.datetime.now(datetime.timezone.utc)
                 .strftime('%Y-%m-%d %H:%M UTC'), txt)
    if write:
        open(BOARD, 'w').write(txt)
    return done, pend, total

if __name__ == '__main__':
    done, pend, total = regenerate()
    line = f'{done} processed, {pend} pending (of {total} enumerated)'
    print(line if '--line' in sys.argv else
          f'boards/otter-backlog.md regenerated: {line}')
