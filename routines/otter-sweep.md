# Routine — Otter transcript sweep (hourly, self-bound)

**Routine id:** `trig_01VVjwRPosDAmd7Y9TG4NBBE` · **cron:** `19 * * * *` (hourly,
anchored to the creation minute so it does not pile onto :00 with every other Routine).

**Cadence — 30 minutes was REQUESTED but is NOT AVAILABLE.** The platform enforces a
1-hour minimum and rejects anything shorter: *"cron expression '*/30 * * * *' may fire
runs as little as 30 minutes apart; the minimum interval is 1 hour"*. Hourly is the
closest permitted. Do not "fix" this by adding a second offset Routine — two Routines
for one cadence breaks the one-per-cadence invariant and double-analyses transcripts.

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
