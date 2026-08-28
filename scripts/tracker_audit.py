#!/usr/bin/env python3
"""Tracker hygiene over the ClickUp Tasks list + idea-pipeline heartbeat.

Ported from a desk where every one of these checks exists because its absence cost a
real message, a stale list, or a silently dead pipeline. The principles carried over:
- CLOSURE DISCIPLINE: if the record says a thing is done, the status moves in the
  same action. Assert on the resulting state, never on the HTTP code.
- STALENESS IS NOT STATUS: an item untouched for 5+ days is `unverified` and never
  goes into a person-wise list as a current ask without re-verification.
- A LIST NOBODY CAN TRUST IS WORSE THAN NO LIST: every rendered line carries
  priority, days overdue, and how many times the due date has already moved.
- SILENCE IS THE BUG: the idea pipeline reports its intake gap every run.

DUE MOVES are tracked by convention (never trusted to platform history): any
due-date change goes through `move_due()` below, which increments the `Due moves`
custom field in the same call. A date changed any other way is a process violation.

Usage: python3 scripts/tracker_audit.py         # all checks
"""
import os, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clickup as N
import ideas as I

STALE_DAYS = 5
DONE_PHRASES = ('done', 'completed', 'closed', 'no longer needed', 'not needed',
                'already sent', 'resolved', 'sorted', 'finished', 'cancel this')

def _today(): return datetime.date.today()
def _days_from_today(iso):
    try: return (datetime.date.fromisoformat(iso[:10]) - _today()).days
    except Exception: return None

def open_tasks():
    return [t for t in N.q(N.TASKS()) if not N.is_done_status(t)]

def move_due(task_id, new_iso):
    """THE ONLY sanctioned way to change a due date: sets Due and increments Due moves."""
    task = N.get_task(task_id)
    moves = (N.r_number(task, 'Due moves') or 0) + 1
    N.set_due(task_id, new_iso)
    return N.set_field(task_id, N.TASKS(), 'Due moves', moves)

# ---------------------------------------------------------------- checks
def check_closure_language_but_open(tasks):
    hits = []
    for t in tasks:
        if I.age_days(N.edited(t)) > 14: continue      # only recently-touched pages
        for c in N.comments(t['id'])[-3:]:
            txt = N.c_text(c).lower()
            if any(p in txt for p in DONE_PHRASES):
                hits.append((t, txt[:90])); break
    if hits:
        print(f'[CHECK 1] CLOSURE LANGUAGE BUT STILL OPEN: {len(hits)}')
        for t, txt in hits:
            print(f'   {N.r_title(t)[:60]} — "{txt}"  -> transition it NOW or say why not')
    else:
        print('[CHECK 1] closure language vs status: clean')

def check_duplicate_titles(tasks):
    from itertools import combinations
    dupes = []
    for a, b in combinations(tasks, 2):
        ka, kb = set(I.keywords(N.r_title(a))), set(I.keywords(N.r_title(b)))
        if ka and kb and len(ka & kb) / max(1, min(len(ka), len(kb))) >= 0.7:
            dupes.append((N.r_title(a)[:50], N.r_title(b)[:50]))
    if dupes:
        print(f'[CHECK 2] POSSIBLE DUPLICATE OPEN TASKS: {len(dupes)}')
        for a, b in dupes[:10]: print(f'   "{a}"  ~  "{b}"')
    else:
        print('[CHECK 2] duplicates: clean')

def check_repeatedly_slipped(tasks, threshold=2):
    hits = [t for t in tasks if (N.r_number(t, 'Due moves') or 0) >= threshold]
    if hits:
        print(f'[CHECK 3] DUE DATE PUSHED {threshold}+ TIMES: {len(hits)} — renegotiate, never silently move again')
        for t in hits: print(f'   {N.r_title(t)[:60]} (moves: {int(N.r_number(t, "Due moves"))})')
    else:
        print('[CHECK 3] repeatedly slipped: clean')

def check_idea_pipeline():
    pages = I.fetch_all()
    gap = I.intake_gap_days(pages)
    if gap > 7:
        nw = I.newest(pages)
        print(f'[CHECK 4a] IDEA INTAKE HAS BEEN SILENT FOR {gap} DAYS (threshold 7)')
        if nw: print(f'           newest is "{N.r_title(nw)[:50]}", created {N.created(nw)[:10]}.')
    else:
        print(f'[CHECK 4a] idea intake gap: {gap}d — ok')
    ro = I.review_overdue(90, pages)
    print(f'[CHECK 4b] Open ideas overdue for review (90d): {len(ro)}')
    for p in ro[:15]: print(f'   {N.r_title(p)[:60]} ({I.age_days(N.created(p))}d)')
    nt = I.never_triaged(pages)
    print(f'[CHECK 4c] Open ideas never triaged (no ICE): {len(nt)}')
    for p in nt[:15]: print(f'   {N.r_title(p)[:60]}')

# ---------------------------------------------------------------- pending lists
def pending_for(owner, max_days_out=7, tasks=None):
    """Near-term list for one owner: overdue, due within N days, or Highest.
    Every item carries unverified / days_overdue / due_moves. NEVER use a bare
    'not Done' query for a person-wise list."""
    tasks = tasks if tasks is not None else open_tasks()
    out = []
    for t in tasks:
        # Owner match: substring against ALL assignee usernames, so a short name
        # ("mukunda") matches the ClickUp username it is part of.
        if owner.lower() not in (N.r_rich(t, 'Owner') or '').lower(): continue
        due = N.r_date(t, 'Due')
        dd = _days_from_today(due) if due else None
        if not (dd is not None and dd <= max_days_out) and N.r_select(t, 'Priority') != 'Highest':
            continue
        out.append({'page': t, 'title': N.r_title(t),
                    'priority': N.r_select(t, 'Priority') or 'Medium',
                    'days_overdue': -dd if (dd is not None and dd < 0) else 0,
                    'due': due, 'due_moves': int(N.r_number(t, 'Due moves') or 0),
                    'unverified': I.age_days(N.edited(t)) >= STALE_DAYS,
                    'url': N.url(t)})
    out.sort(key=lambda x: (-x['days_overdue'], x['priority'] != 'Highest'))
    return out

def render_line(item):
    """Never hand-format a pending line — the recipient must always see priority,
    overdue days, and how many times the date has already moved."""
    bits = [f"[{item['priority']}]", item['title']]
    if item['days_overdue']: bits.append(f"— {item['days_overdue']}d overdue")
    elif item['due']: bits.append(f"— due {item['due']}")
    if item['due_moves']: bits.append(f"(date moved {item['due_moves']}x)")
    if item['unverified']: bits.append("[UNVERIFIED — confirm before treating as a current ask]")
    return ' '.join(bits)

def main():
    tasks = open_tasks()
    print(f'open tasks: {len(tasks)}')
    check_closure_language_but_open(tasks)
    check_duplicate_titles(tasks)
    check_repeatedly_slipped(tasks)
    check_idea_pipeline()

if __name__ == '__main__':
    main()
