# Routine prompt — Daily Ops Loop (set your schedule, e.g. 9:00 local)
Paste the block below as the Routine's prompt (claude.ai/code -> Routines -> New routine),
with this repo + the desk cloud environment attached and connectors ticked.

---
Run the daily ops loop (credentials/context in this session):
0. TOOLING (critical in a fresh session — read before aborting anything):
   - ClickUp (tasks + ideas): scripts/clickup.py with CLICKUP_* env vars. No ClickUp
     MCP connector is ever required — do not block on one.
   - Notion (registers only): scripts/notion.py with NOTION_API_KEY +
     NOTION_REGISTERS_PAGE. Pair absent = registers layer PENDING: carry register
     entries as TODOs, say so, continue. A Notion MCP connector is NEVER required.
   - Slack channels (read + post): scripts/slack.py with SLACK_BOT_TOKEN. The Slack
     connector is only needed for the Principal's personal DMs.
   - Gmail / Outlook / Otter / Drive / Calendar steps DO need their connectors enabled
     in this chat. If a connector shows enabledInChat=false: SKIP only those steps,
     mark each skipped step "CONNECTOR OFF" in the digest, and RUN EVERYTHING ELSE.
     Never abort the whole loop while the env-var paths work.
   - Verify env vars exist first; if THEY are missing, that alone is a full stop.
1. TASKS — ClickUp Tasks list: due today, overdue, Highest unassigned; group by owner.
1a. TRACKER HYGIENE (light) — run `python3 scripts/tracker_audit.py`. Anything CHECK 1
   flags (closure language but still open) gets a decision THIS cycle — close it or say
   why not. Do not let a flagged item sit silently across multiple daily runs.
2. SLACK INBOX — run `python3 scripts/slack_sweep.py 24 60` (never hand-roll the sweep:
   it fixes the two silent-miss bugs — threaded replies on old parents, and the 7-digit
   timestamp that returns ok=true with zero messages). Then run
   `python3 scripts/unanswered.py 3` and read ALL of it — never head/tail this output.
   Surface every human message needing a reply; DRAFT suggested replies in the digest
   for approval — NEVER auto-reply (rule 1). Work the DM checklist the sweep prints,
   via the user-scoped Slack connector; if the connector is off, say the DM leg did not
   run — never let the channel result stand in for it.
2b. OTTER TRANSCRIPTS — scan Otter (otter_get_user_info to anchor the date, then
   otter_search created_after=yesterday). For each meeting with a real transcript, run
   /meeting: FOUR lists per rule 2 (decisions / owed to us / the Principal's own
   commitments / ideas), archive + file + propose updates for approval. Timed
   commitments become calendar events in the SAME turn. Skip 0-second captures, note
   them. Connector off -> mark and continue.
2c. IDEA CAPTURE (standing — loud zero) — process idea-class items from today's
   channels, transcripts and mail through /idea-intake (grouped, ICE-scored,
   deduped-as-mentions). Report counts even when zero.
3. GMAIL — new mail (1d): anything needing reply (draft for approval), commitments,
   contradictions vs the tracker, attachments to file (rule 3).
3b. OUTLOOK — same sweep on the Microsoft mailbox. The two mailboxes are one inbox to
   this desk: one combined reply-queue in the digest, source-tagged.
4. INCOMING ORIGINALS — any original doc/file received via chat, Slack or email since
   last run: save to Drive (sensitive -> restricted), record contents + link in the tracker,
   surface every upload link.
5. TRACK EVERY TO-DO — file EVERY to-do surfaced anywhere in this loop in the Tasks DB
   with Owner/Priority/Due; dedupe first; if done in-run, file then resolve. Nothing
   surfaced ends the loop untracked.
6. DIGEST — post to the Principal's channel: top-5 actions, overdue by name, replies
   awaiting approval (with originals side by side), files filed, new tasks, and the
   ideas line: `Ideas: N new / N mentions` — when today's total is 0 AND the intake gap
   exceeds 7 days, render `⚠ IDEA intake: 0 today, N days since last item — verify
   sources`. Minimal output when nothing changed.
7. PERSON-WISE PENDING LISTS — one message per person, built with
   `python3 scripts/pending.py <owner>` (rule 7 verbatim: unverified items never as
   current asks; grouped by who they must connect with; render_line format; close what
   is reported done in the same cycle).
STYLE: short plain messages; no credentials anywhere; drafts are drafts until approved.
