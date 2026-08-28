#!/usr/bin/env python3
"""Idea-pipeline helpers over the Notion Ideas database.

DESIGN (ported from the originating desk, where these detectors caught a 14-day
silent intake stop and 27 never-triaged ideas):
- Notion is the ONLY source of truth for idea state. Nothing here caches to disk;
  boards/idea-board.md is a GENERATED view, never hand-edited.
- Dedupe is two-stage: `dedupe_candidates()` is the CHEAP keyword shortlist; the
  semantic judgement is made by the desk READING the candidate pages. A token
  overlap must never decide that two ideas are the same.
- A duplicate becomes a MENTION (Mentions += 1, plus a comment saying when/where),
  never a second page. Mention count is a conviction signal.

Usage:
  python3 scripts/ideas.py smoke   # counts, newest, gap
  python3 scripts/ideas.py board   # regenerate boards/idea-board.md
"""
import os, re, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion as N

BOARD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     'boards', 'idea-board.md')
STATES = ('Open', 'Promoted', 'Merged', 'Killed')

STOP = set('''a an and are as at be but by for from has have how i if in is it its of on or
our so that the their there these this to was we what when which who will with you your
should would could can may might do does did not no yes'''.split())

def _now(): return datetime.datetime.now(datetime.timezone.utc)
def _parse(ts):
    try: return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception: return None
def age_days(ts):
    d = _parse(ts)
    return (_now() - d).days if d else 0

def fetch_all():
    return N.q(N.IDEAS(), sorts=[{'timestamp': 'created_time', 'direction': 'descending'}])

def is_open(page):
    return (N.r_select(page, 'State') or 'Open') == 'Open'

def keywords(text, limit=40):
    toks = re.findall(r'[a-z0-9]{3,}', (text or '').lower())
    out, seen = [], set()
    for t in toks:
        if t in STOP or t in seen: continue
        seen.add(t); out.append(t)
        if len(out) >= limit: break
    return out

def dedupe_candidates(text, pages=None, top=8):
    """Cheap stage-one filter: rank existing ideas by keyword overlap.
    Returns [(score, page)] for the desk's semantic stage two."""
    pages = pages if pages is not None else fetch_all()
    kw = set(keywords(text))
    scored = []
    for p in pages:
        hay = set(keywords(N.r_title(p) + ' ' + N.r_rich(p, 'Source') + ' '
                           + ' '.join(N.r_multi(p, 'Category'))))
        ov = len(kw & hay)
        if ov: scored.append((ov, p))
    scored.sort(key=lambda x: -x[0])
    return scored[:top]

def add_mention(page_id, source):
    """A recurring idea gains a mention, never a second page."""
    st, page = N.api('GET', f'/pages/{page_id}')
    m = (N.r_number(page, 'Mentions') or 1) + 1
    N.update(page_id, {'Mentions': N.p_number(m)})
    N.comment(page_id, f'Mention: {_now().date().isoformat()}, {source}')
    return m

def intake_gap_days(pages=None):
    pages = pages if pages is not None else fetch_all()
    if not pages: return 999
    return min(age_days(N.created(p)) for p in pages)

def newest(pages=None):
    pages = pages if pages is not None else fetch_all()
    return pages[0] if pages else None

def never_triaged(pages=None):
    pages = pages if pages is not None else fetch_all()
    return [p for p in pages if is_open(p) and N.r_number(p, 'ICE') is None]

def review_overdue(days=90, pages=None):
    """Open ideas whose last review (or creation, if never reviewed) is > N days ago,
    plus anything whose recorded re-review date has passed."""
    pages = pages if pages is not None else fetch_all()
    out = []
    today = _now().date().isoformat()
    for p in pages:
        if not is_open(p): continue
        rv = N.r_date(p, 'Reviewed')
        if rv:
            if age_days(rv + 'T00:00:00Z') > days or rv < today and age_days(rv + 'T00:00:00Z') > days:
                out.append(p)
        elif age_days(N.created(p)) > days:
            out.append(p)
    return out

# ---------------------------------------------------------------- board rendering
def _nid(p): return 'n' + p['id'].replace('-', '')[:10]
def _short(s, chars=40):
    s = re.sub(r'["\[\]{}<>|]', '', s or '')
    return (s[:chars] + '…') if len(s) > chars else (s or '(untitled)')
def _topic(p):
    cats = N.r_multi(p, 'Category')
    return cats[0] if cats else 'general'

def mermaid_board(pages, max_nodes=40):
    groups = {}
    for p in pages: groups.setdefault(_topic(p), []).append(p)
    lines = ['```mermaid', 'flowchart TD']
    for st, color in (('Open', '#e8f0fe'), ('Promoted', '#e6f4ea'),
                      ('Merged', '#fef7e0'), ('Killed', '#fce8e6')):
        lines.append(f'  classDef {st.lower()} fill:{color},stroke:#555;')
    for topic, ps in sorted(groups.items()):
        lines.append(f'  subgraph {re.sub(r"[^A-Za-z0-9_]", "_", topic)}')
        for p in ps[:max_nodes]:
            state = (N.r_select(p, 'State') or 'Open').lower()
            ice = N.r_number(p, 'ICE')
            tag = f' ICE {int(ice)}' if ice else ''
            lines.append(f'    {_nid(p)}["{_short(N.r_title(p))}{tag}"]:::{state}')
        lines.append('  end')
    lines.append('```')
    return '\n'.join(lines)

def _prev_rows(path=BOARD):
    if not os.path.exists(path): return {}
    rows = {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'\| \[(.+?)\]\((.+?)\) \| .*? \| .*? \| .*? \| (\w+) \|', line)
        if m: rows[m.group(2)] = m.group(3)
    return rows

def render_board(pages=None):
    pages = pages if pages is not None else fetch_all()
    prev = _prev_rows()
    n_open = sum(1 for p in pages if is_open(p))
    unscored = len(never_triaged(pages))
    gap = intake_gap_days(pages)
    head = [f'<!-- GENERATED FROM NOTION by scripts/ideas.py — never hand-edit -->',
            f'# Idea Board — generated {_now().date().isoformat()}', '',
            f'**{len(pages)} items · {n_open} open · {unscored} unscored · intake gap {gap}d**']
    if gap > 7:
        head.append(f'\n> ⚠ **IDEA intake has been silent for {gap} days** — verify sources.')
    body = [mermaid_board(pages), '', '## Ranked (open, by ICE then mentions)', '',
            '| Idea | ICE | Mentions | Age | State |', '|---|---:|---:|---:|---|']
    ranked = sorted((p for p in pages if is_open(p)),
                    key=lambda p: (-(N.r_number(p, 'ICE') or 0), -(N.r_number(p, 'Mentions') or 1)))
    for p in ranked:
        body.append(f'| [{_short(N.r_title(p), 60)}]({N.url(p)}) | '
                    f'{int(N.r_number(p, "ICE") or 0) or "—"} | {int(N.r_number(p, "Mentions") or 1)} | '
                    f'{age_days(N.created(p))}d | {N.r_select(p, "State") or "Open"} |')
    moves = []
    for p in pages:
        old = prev.get(N.url(p))
        new = N.r_select(p, 'State') or 'Open'
        if old and old != new:
            moves.append(f'- {_short(N.r_title(p), 60)}: {old} → {new}')
    body += ['', '## Movement since last regeneration', '']
    body += moves if moves else (['First generation — no previous version to diff against.']
                                 if not prev else ['No state changes. Two quiet weeks in a row means the board is drifting back to a graveyard.'])
    return '\n'.join(head + [''] + body) + '\n'

def write_board(path=BOARD):
    out = render_board()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(out)
    return path

def _smoke():
    pages = fetch_all()
    nw = newest(pages)
    print(f'ideas: {len(pages)} total, {sum(1 for p in pages if is_open(p))} open, '
          f'{len(never_triaged(pages))} unscored, gap {intake_gap_days(pages)}d')
    if nw: print(f'newest: {N.r_title(nw)} ({N.created(nw)[:10]})')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'smoke'
    if cmd == 'board':
        print('wrote', write_board())
    else:
        _smoke()
