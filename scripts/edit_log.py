#!/usr/bin/env python3
"""The desk's only objective quality score: the diff between what was drafted and what
the Principal actually sent.

WHY. The learning rule has always captured corrections, and it works - but there has never been a
denominator. Nobody could say whether the desk is getting better or merely accumulating
rules. `logs/edits.jsonl` is that denominator.

HONESTY IS THE WHOLE POINT. If the Principal rewrote a draft, the ratio is high, and recording
that accurately is the reason the file exists. A log that flatters the desk is worse
than no log, because it converts a known gap into a false reassurance.

NO SELF-SCORING. Never write a confidence percentage, a self-assessed grade or a
"how did I do" estimate anywhere. A model rating its own output produces a number that
looks rigorous and measures nothing. The diff is objective, free, and already here.

Usage:
    from scripts.edit_log import log_edit
    log_edit(thread='SLACK:wf003-campaigns#1787...', type='vendor-reply',
             draft=drafted_text, final=sent_text, interviewed=False)

`final` is what actually went out. If it went out unchanged, pass the same string -
that is an edit_ratio of 0.0 and it counts.
"""
import json
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, 'logs', 'edits.jsonl')


def levenshtein(a, b):
    """Iterative two-row Levenshtein. No dependencies - this file must work in the
    cloud runner with nothing installed."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1,          # deletion
                           cur[j - 1] + 1,       # insertion
                           prev[j - 1] + (ca != cb)))  # substitution
        prev = cur
    return prev[-1]


def log_edit(thread, type, draft, final, interviewed=False, stance=None, note=None):
    """Append one honest line. Returns the row written."""
    dist = levenshtein(draft, final)
    ratio = (dist / len(draft)) if draft else 0.0
    row = {
        'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'thread': thread,
        'type': type,
        'stance': stance,
        'draft': draft,
        'final': final,
        'edited': draft != final,
        'edit_chars': dist,
        'edit_ratio': round(ratio, 4),
        'interviewed': bool(interviewed),
    }
    if note:
        row['note'] = note
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + '\n')
    return row


def read_log():
    if not os.path.exists(LOG):
        return []
    out = []
    for line in open(LOG, encoding='utf-8'):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def summary():
    """Counts only. No grade, no self-assessment - see the module docstring."""
    rows = read_log()
    if not rows:
        return 'logs/edits.jsonl is empty - nothing logged yet.'
    n = len(rows)
    unedited = sum(1 for r in rows if not r['edited'])
    ratios = sorted(r['edit_ratio'] for r in rows)
    median = ratios[n // 2] if n % 2 else (ratios[n // 2 - 1] + ratios[n // 2]) / 2
    interviewed = [r for r in rows if r.get('interviewed')]
    iv_unedited = sum(1 for r in interviewed if not r['edited'])
    lines = [
        f'drafts: {n}   unedited: {unedited} ({unedited / n * 100:.0f}%)   '
        f'median edit_ratio: {median:.3f}',
    ]
    if interviewed:
        lines.append(f'interviewed: {len(interviewed)} ({len(interviewed) / n * 100:.0f}%)   '
                     f'of those unedited: {iv_unedited / len(interviewed) * 100:.0f}%')
    else:
        lines.append('interviewed: 0 - the interview gate has not fired yet')
    by_type = {}
    for r in rows:
        t = by_type.setdefault(r['type'], [0, 0])
        t[0] += 1
        t[1] += 0 if r['edited'] else 1
    lines.append('by type:')
    for t, (c, u) in sorted(by_type.items(), key=lambda kv: -kv[1][0]):
        lines.append(f'  {t:22} {c:3} drafts, {u:3} unedited ({u / c * 100:.0f}%)')
    return '\n'.join(lines)


if __name__ == '__main__':
    print(summary())
