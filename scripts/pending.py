#!/usr/bin/env python3
"""Person-wise pending list, WhatsApp/Slack-ready.
Usage: python3 scripts/pending.py <owner> [--all]
--all drops the near-term filter (overdue / due 7d / Highest). Default near-term only:
a far-future item is not a current ask."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracker_audit import pending_for, render_line

def main():
    if len(sys.argv) < 2:
        raise SystemExit('usage: pending.py <owner> [--all]')
    owner = sys.argv[1]
    horizon = 100000 if '--all' in sys.argv else 7
    items = pending_for(owner, max_days_out=horizon)
    print(f'PENDING — {owner} ({len(items)} items)')
    unv = [i for i in items if i['unverified']]
    for i in items:
        if not i['unverified']: print(' •', render_line(i))
    if unv:
        print('\nUNVERIFIED — re-verify against the live source before chasing:')
        for i in unv: print(' •', render_line(i))

if __name__ == '__main__':
    main()
