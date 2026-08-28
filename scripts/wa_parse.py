#!/usr/bin/env python3
"""Parse a pasted WhatsApp export/copy into structured desk items.

WHY (standing, 26 Aug 2026). The Principal asked whether the manual pasting of WhatsApp
conversations can be automated. The honest answer is that WhatsApp has NO API for a
personal account — the Business/Cloud API only reads messages sent TO a business
number, and the unofficial libraries (whatsapp-web.js, Baileys) drive WhatsApp Web
through a linked device in breach of WhatsApp's terms, risking a BAN on the number
the organisation uses for clients and partners. That risk is not acceptable for a business-critical number.

So the paste stays, and this removes the work AFTER the paste. The Principal (or the desk operator) pastes; the desk extracts. Reduces a per-conversation chore to one action.

WHAT IT EXTRACTS, in the shape rule 2 requires (three lists, plus a fourth for ideas):
  1. DECISIONS      — anything settled
  2. OWED TO US     — commitments others made, with who and when
  3. OWED BY PRINCIPAL — commitments the Principal made (the class that gets lost)
  4. IDEAS          — long-horizon intent, routed to /idea-intake, never a dated task
Plus: NUMBERS (money, counts, percentages) pulled out for verification, and
TIME-BOXED items ("by 12 pm", "today", "tomorrow") which become chase points.

This script does the mechanical part — speaker/timestamp parsing, number extraction,
commitment-phrase detection. The judgement — what is a decision, whose commitment it
is, what it means — stays with the desk reading the output. A regex must never decide
what someone promised.

Usage:
    python3 scripts/wa_parse.py < pasted.txt
    pbpaste | python3 scripts/wa_parse.py
"""
import re
import sys
from collections import OrderedDict

# [10:23 am, 26/8/2026] Name: text     — the format WhatsApp copy/export produces
LINE = re.compile(
    r'^\[?(?P<time>\d{1,2}:\d{2}\s*(?:am|pm)?)[,\s]+(?P<date>\d{1,2}/\d{1,2}/\d{2,4})\]?\s*'
    r'(?P<who>[^:]{1,60}):\s*(?P<text>.*)$', re.I)

MONEY = re.compile(r'(?:Rs\.?|INR|₹)\s?([\d,]+(?:\.\d+)?)|([\d,]{3,})\s*(?:rupees|lakh|crore)', re.I)
COUNT = re.compile(r'\b([\d,]{3,})\b')
PCT = re.compile(r'\b(\d{1,3}(?:\.\d+)?)\s*%')

COMMIT = re.compile(r'\b(will|shall|going to|by (?:today|tomorrow|EOD|\d{1,2}\s*(?:am|pm))|'
                    r'allow me till|give me till|i.ll|we.ll|let me|working on)\b', re.I)
TIMEBOX = re.compile(r'\b(by\s+\d{1,2}\s*(?:am|pm)|by\s+(?:today|tomorrow|EOD|tonight)|'
                     r'today|tomorrow|tonight|shortly|in an hour)\b', re.I)
IDEA = re.compile(r'\b(we should|someday|idea|in future|later we can|would be good|explore)\b', re.I)
ASK = re.compile(r'\?\s*$|^\s*(please|can you|could you|kindly)\b', re.I)


def parse(raw):
    msgs, cur = [], None
    for line in raw.splitlines():
        m = LINE.match(line.strip())
        if m:
            if cur:
                msgs.append(cur)
            cur = dict(time=m.group('time').strip(), date=m.group('date'),
                       who=m.group('who').strip(), text=m.group('text').strip())
        elif cur and line.strip():
            cur['text'] += ' ' + line.strip()
    if cur:
        msgs.append(cur)
    return msgs


def report(msgs):
    if not msgs:
        print('No WhatsApp-formatted lines found. Expected: [10:23 am, 26/8/2026] Name: text')
        return

    speakers = OrderedDict()
    for m in msgs:
        speakers.setdefault(m['who'], 0)
        speakers[m['who']] += 1

    print(f"WHATSAPP THREAD — {len(msgs)} messages, "
          f"{msgs[0]['date']} {msgs[0]['time']} to {msgs[-1]['date']} {msgs[-1]['time']}")
    print('participants: ' + ', '.join(f'{k} ({v})' for k, v in speakers.items()))

    def block(title, rows, note=''):
        print(f'\n### {title} ({len(rows)})')
        if note:
            print(f'    {note}')
        for who, when, txt in rows:
            print(f'  [{when}] {who}: {txt[:220]}')

    commits, timeboxed, asks, ideas = [], [], [], []
    numbers = []
    for m in msgs:
        t, who, when = m['text'], m['who'], m['time']
        if COMMIT.search(t):
            commits.append((who, when, t))
        if TIMEBOX.search(t):
            timeboxed.append((who, when, t))
        if ASK.search(t):
            asks.append((who, when, t))
        if IDEA.search(t):
            ideas.append((who, when, t))
        for mm in MONEY.finditer(t):
            numbers.append((who, when, mm.group(0), t[:110]))
        for mm in PCT.finditer(t):
            numbers.append((who, when, mm.group(0), t[:110]))

    block('COMMITMENTS — split these into OWED TO US vs OWED BY PRINCIPAL by hand', commits,
          'rule 2: the third list (PRINCIPAL\'s own commitments) is the one that gets lost')
    block('TIME-BOXED — each becomes a chase point with its deadline', timeboxed)
    block('ASKS / QUESTIONS — anything unanswered here is an open loop', asks)
    block('POSSIBLE IDEAS — route via /idea-intake, never a dated task', ideas)

    print(f'\n### NUMBERS TO VERIFY ({len(numbers)})')
    print('    every figure is claimed-by-them until checked against a receipt or a system')
    for who, when, val, ctx in numbers:
        print(f'  [{when}] {who}: {val}   <- {ctx}')

    print('\n### NEXT (desk)')
    print('  1. Sort commitments into the four extraction lists; file each in the Notion Tasks DB with a date.')
    print('  2. Anything with a time attached becomes a calendar event in the SAME turn.')
    print('  3. Verify every number above; mark claimed-by-them until a system confirms it.')
    print('  4. Log any credential-sharing mention in the Credential-Sharing Register (fact, never the value).')
    print('  5. Save the original paste to Drive and record the link (rule 3, incoming originals).')


if __name__ == '__main__':
    report(parse(sys.stdin.read()))
