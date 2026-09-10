#!/usr/bin/env python3
"""Ledger of which Otter transcripts the desk has already processed.

WHY A FILE AND NOT MEMORY: the Otter sweep Routine fires into a long-running
session whose context is compacted, and whose container is reclaimed after
inactivity. Anything held only in conversation is lost on the first restart and
the desk re-analyses transcripts it already handled — or worse, silently skips
new ones. The ledger is append-only JSONL in logs/, the same convention as
logs/edits.jsonl. It records PROCESSING state, never task state (ClickUp owns
that), so it is not a second registry of live state.

States:
  PROPOSED  analysed; action items shown to the Principal, awaiting approval
  FILED     approved and created in ClickUp (carries the task ids)
  SKIPPED   analysed; nothing actionable (record WHY in note)

Usage:
  python3 scripts/otter_ledger.py check <id> [<id> ...]   # prints ids NOT yet seen
  python3 scripts/otter_ledger.py mark <id> --state PROPOSED --title "..." [--note "..."]
  python3 scripts/otter_ledger.py list [--state FILED]
  python3 scripts/otter_ledger.py pending                 # PROPOSED but never FILED
"""
import os, sys, json, argparse, datetime

LEDGER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      'logs', 'otter-seen.jsonl')
STATES = ('PROPOSED', 'FILED', 'SKIPPED')

def _rows():
    if not os.path.exists(LEDGER):
        return []
    out = []
    for line in open(LEDGER, encoding='utf-8'):
        line = line.strip()
        if line:
            try: out.append(json.loads(line))
            except json.JSONDecodeError: pass      # never let one bad line hide the rest
    return out

def latest():
    """id -> most recent row for that id (a transcript can move PROPOSED -> FILED)."""
    by = {}
    for r in _rows():
        by[r['id']] = r
    return by

def unseen(ids):
    known = latest()
    return [i for i in ids if i not in known]

def mark(tid, state, title='', note='', tasks=None):
    if state not in STATES:
        raise SystemExit(f'state must be one of {STATES}, got {state!r}')
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    row = {'id': tid, 'state': state, 'title': title, 'note': note,
           'tasks': tasks or [],
           'at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')
    return row

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check');  c.add_argument('ids', nargs='+')
    m = sub.add_parser('mark');   m.add_argument('id')
    m.add_argument('--state', required=True); m.add_argument('--title', default='')
    m.add_argument('--note', default=''); m.add_argument('--tasks', default='')
    l = sub.add_parser('list');   l.add_argument('--state', default=None)
    sub.add_parser('pending')
    a = ap.parse_args()

    if a.cmd == 'check':
        new = unseen(a.ids)
        print('\n'.join(new) if new else '')
        print(f'# {len(new)} new of {len(a.ids)} checked '
              f'({len(latest())} in ledger)', file=sys.stderr)
    elif a.cmd == 'mark':
        r = mark(a.id, a.state, a.title, a.note,
                 [t for t in a.tasks.split(',') if t])
        print(json.dumps(r, ensure_ascii=False))
    elif a.cmd == 'list':
        rows = sorted(latest().values(), key=lambda r: r['at'])
        rows = [r for r in rows if not a.state or r['state'] == a.state]
        for r in rows:
            print(f"{r['at'][:16]}  {r['state']:<9} {r['id']:<32} {r['title'][:44]}")
        print(f'# {len(rows)} transcript(s)')
    elif a.cmd == 'pending':
        rows = [r for r in latest().values() if r['state'] == 'PROPOSED']
        for r in sorted(rows, key=lambda r: r['at']):
            print(f"{r['at'][:16]}  {r['id']:<32} {r['title'][:50]}")
        print(f'# {len(rows)} analysed but NOT yet approved/filed')

if __name__ == '__main__':
    main()
