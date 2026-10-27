# Routine — Otter transcript sweep (daily, self-bound)

**Routine id:** `trig_01VVjwRPosDAmd7Y9TG4NBBE` · **cron:** `CRON_TZ=Asia/Kolkata 52 20 * * *`
(daily, 8:52 pm IST — a jittered minute so it does not pile onto :00 with every other Routine).

**Cadence — DAILY, by the Principal's instruction (27 Oct).** It ran hourly until
24 Oct. Measured cost of the hourly cadence: 46–78 million tokens per day, ~578 million
over the nine days 10–18 Oct, for about a hundred one-line `0 new transcripts` no-ops —
roughly a third of the month's entire consumption. The daily cadence cut that ~92%
(to ~5M/day) while still catching every real transcript. Do not restore the hourly
schedule, and do not add a second Routine for the same cadence — two Routines for one
cadence breaks the one-per-cadence invariant and double-analyses transcripts.

**Why 8:52 pm IST.** Late enough that the day's meetings have finished AND Otter has
finished processing them (a transcript fetched too early comes back as a short cut and
grows later — see the re-cut warning below), and early enough that the Principal is
still working when the report lands. The sweep window is the last 2 days, so a late
re-cut or a missed day is picked up on the next fire rather than lost.

**Task creation — the gate was LIFTED on 27 Oct.** The Principal's instruction, verbatim
in substance: read the Otter recordings once a day, create the tasks in ClickUp, and
distribute them to the respective employees based on job role — "don't assign the task
to me alone". The sweep now CREATES tasks instead of only proposing them. Four guards
survive the change: owners still resolve by evidence, never by speaker label (rule 12);
an owner that cannot be resolved gets an UNASSIGNED task plus a "needs an owner" line,
never a silent default to the Principal; personnel, salary, termination, credential and
confidential welfare/financial material is still HELD BACK for approval and reported in
chat only; and anything with a time attached also becomes a calendar event (rule 2).

**Target:** fires into ONE persistent session (`session_01ExMoskeTKS1LRMszHywEoY`),
never a fresh session — `persist_session: true`. The Principal asked for continuity so
the desk keeps its context instead of re-introducing itself every fire.

**CONNECTOR CAVEAT — read before trusting this Routine.** It stores NO MCP connectors
(`mcp_connections: []`). The `connectors` parameter is disabled for this organisation,
so it cannot be attached from a session. Because the Routine resumes an existing
session rather than spawning one, it inherits whatever that session holds — but if the
container is reclaimed and reprovisioned, Otter may come back detached and every fire
will correctly report `CONNECTOR OFF — 0 swept`. If that persists, recreate the Routine
from the claude.ai Routines UI with Otter ticked.

**One-per-cadence invariant:** this is the ONLY hourly Routine. A second one would
double-analyse every transcript and double-post the review.

## Each fire

1. `python3 scripts/otter_ledger.py list` — what has already been processed.
2. List recent Otter transcripts via the Otter connector.
3. `python3 scripts/otter_ledger.py check <id> ...` — which are NEW.
4. **If zero new:** print one line — `OTTER sweep: 0 new transcripts (N in ledger)` —
   and STOP. Do not restate old analysis. At ~24 fires a day, a chatty no-op is what
   makes the Principal stop reading the digest.
5. **For each new transcript:** read it IN FULL (they run 80k+ characters — read in
   sequential chunks, never skim, and say so if any part could not be read). Extract
   the four lenses (rule 2): decisions · actions owed TO us · **the Principal's OWN
   commitments** · ideas (→ `/idea-intake`, never dated tasks).
6. Propose action items as a numbered table: owner · due · priority · confidence.
   Owners resolve ONLY against CONFIRMED rows in `docs/ORG-STRUCTURE.md` (rule 12 —
   speaker labels are not identity). Due dates ONLY if stated in the meeting.
   Flag anyone who is not an assignable member of the ClickUp Tasks list.
7. **SHOW FOR APPROVAL. Create nothing.** The meeting-task approval gate is standing:
   the Principal approves or corrects by row number first.
8. `otter_ledger.py mark <id> --state PROPOSED --title "..."` in the SAME turn — so a
   restart between analysis and approval does not lose or duplicate the work.
9. On approval: create the tasks, then `mark <id> --state FILED --tasks <ids>`.
   Nothing actionable in the transcript → `--state SKIPPED --note "<why>"`.

## Known failure modes

- **Connector drop.** Otter detaches from a long-running session. If the Otter tools
  are absent, print `OTTER sweep: CONNECTOR OFF — 0 swept` (rule 5) — never report a
  clean zero you did not earn. It is a fresh session that reattaches connectors.
- **Context compaction.** The ledger is the memory, not the conversation. Always read
  it from disk; never trust recall of what was processed.
- **Transcript quality.** Otter mangles Telugu/Hindi passages badly. Mark low-confidence
  items rather than presenting garbled speech as a clean action item.

- **`created_after` hides same-day recordings.** Observed 2026-09-22: a search with
  `created_after: 2026-09-22` returned nothing, while the identical query with
  `created_after: 2026-09-21` returned that day's 01:58 UTC recording. The filter is
  not inclusive of the day it names. **Always sweep with `created_after` set to
  YESTERDAY**, then discard by ledger check — never by date filter.
- **`otter_search` is a ranked matcher, not an enumerator.** A narrow query returns
  only the single best match, so a one-query zero is not a swept zero (rule 5). Use a
  broad multi-word query (e.g. `meeting discussion team`), which returns the day's
  recordings, and ledger-check every id it returns.

- **A frozen id list is not enumeration — the failure that cost 36 transcripts.**
  Observed 2026-10-20: the sweep had been passing the SAME 11 ids to
  `otter_ledger.py check` every fire, inherited across compactions, and reporting a
  clean `0 new` each time. Meanwhile 36 recordings dated 2026-09-30 → 2026-10-20 sat
  unprocessed. A zero earned against a stale list is exactly the silent-pipeline
  failure rule 5 exists to prevent. **Every fire must re-enumerate from Otter**, and
  the ids passed to `check` must come from THAT fire's search, never from memory or
  from an earlier turn.
- **Paginate.** `otter_search` returns at most `page_size` (max 25) results and a
  `next_cursor`. A single page can stop short of the oldest unprocessed recording.
  Keep paging until the response carries `pagination_completion_reason:
  all_results_returned`, or until the results reach past the newest ledger entry.
- **Large results spill to a file.** A wide search exceeds the tool's token ceiling and
  is written to a `tool-results/*.txt` JSON file instead. Parse it (`python3 -c` over
  `result.content[0].text`) — do not narrow the search just to make it fit, that
  re-creates the frozen-list failure.
- **Ids can begin with `-`.** `check -0hxMs2zBLon...` is parsed as a flag and aborts the
  whole check. Compare against the ledger in Python, or pass `--` first.

- **A recording less than ~2h old may still be growing — and its id may be re-cut.**
  Observed 2026-10-21: `5gpX_ySnmJoKSIMag7N9TLgzsv4` read at 10:20 UTC as a 19m52s
  session starting 01:58, ending mid-sentence. An hour later the same id was a
  **1h13m session starting 03:12**, and the 01:58 session had been split out under a
  new id (`q4me6ByLcso8n8G1AmNCv1zE8Yg`). Otter re-processes and re-cuts live
  recordings after capture. So: a transcript whose `start_time` is within ~2h of the
  sweep is provisional — mark it PROPOSED as usual (step 8 loses nothing), but
  **re-enumerate and compare `duration` on the next fire**, and re-read in full if it
  changed. Never report "ends mid-sentence" as a defect without saying it may simply
  still be recording.
