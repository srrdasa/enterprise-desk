# /idea-intake — process a batch of ideas (links/text/transcript extracts) end-to-end

Takes raw idea material — WhatsApp pastes (through `scripts/wa_parse.py` first), Slack
idea-channel posts, transcript list-4 extracts, pasted links — and runs the pipeline:
resolve → group → analyse → score → dedupe → file → post. Say the source person if it
isn't obvious — it goes in the record.

## 1. RESOLVE EVERY LINK FIRST — never analyse from the URL
A YouTube/IG URL tells you nothing; guessing from the slug is how ideas get misfiled.
- YouTube video/Short/playlist — the page HTML is JS-rendered; use the oEmbed API:
  `curl -sS "https://www.youtube.com/oembed?url=<URL-ENCODED-LINK>&format=json"`
  (returns title + channel).
- Ordinary page — WebFetch with a prompt asking what the site is and offers.
- Login-walled (Instagram etc.) — record what IS visible, mark unfetchable, ask the
  Principal for the detail rather than inventing it.
- If a link cannot be resolved, say so in the record. Never fill the gap with a guess.

## 2. GROUP RELATED ITEMS
Several links usually make ONE idea. A bare label next to a link ("Hindi") is a label,
not an idea. One Ideas-DB page per group, not per link.

## 3. ANALYSE EACH GROUP — the five required fields
- **Category** — what kind of thing this is.
- **Where it applies** — the specific workflow/cost line in OUR operation; tie to real
  figures where they exist. If nowhere, say so plainly.
- **Do we already run this / is there better** — check honestly; name cheaper or more
  established options; flag marketing claims as unverified.
- **Disposition** — IMMEDIATE / FUTURE / ALREADY-COVERED.
- **ICE** — Impact, Confidence, Ease, each 1–10 with one line of reasoning; if the
  total ≥ 21, score RICE too and record it. (ICE flatters cheap-and-small items — the
  RICE note is where that gets said.)
Be a reviewer, not a summariser: name what a source actually says; short-form video is
a signal to check against primary sources, never a direct input to a decision; flag
rights/licensing exposure before any adoption.

## 4. DEDUPE, THEN FILE — ClickUp Ideas list
Run `ideas.dedupe_candidates(text)` for the keyword shortlist, READ the candidate
pages, judge semantically. Same idea → `ideas.add_mention(page_id, source)` — Mentions
increments and a comment records when/where; NEVER a second page. Genuinely new →
create the entry (`clickup.create_task` on the Ideas list): Name, State=Open, ICE,
Mentions=1, Category (tags), Disposition, Source (person + channel + date),
description = links with resolved titles + the five fields.

## 5. POST — the ideas channel
One post per idea group carrying the disposition and honest caveats — not a link
summary. Threading per rule 13. Tag the source person by Slack ID.

## 6. CLOSE THE LOOP — count line is MANDATORY
- Anything actionable now ALSO gets a task in the Tasks DB — the idea page records the
  idea, not the task that executes it.
- Sweep the channel for missed posts: any idea post with no matching page is processed
  retroactively. No idea goes unprocessed.
- ALWAYS end with: `IDEA intake: N captured, N mentions attached, N new` — a run that
  finds nothing prints `0 captured — verify sources`. Silence is the bug (rule 5).
