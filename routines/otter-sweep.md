# Routine — Otter transcript sweep (every 30 min, self-bound)

**Cadence:** every 30 minutes · **Target:** fires into ONE persistent session
(`session_01ExMoskeTKS1LRMszHywEoY`), never a fresh session — the Principal asked for
continuity so the desk keeps its context and does not re-introduce itself every fire.

**One-per-cadence invariant:** this is the ONLY 30-minute Routine. A second one would
double-analyse every transcript and double-post the review.

## Each fire

1. `python3 scripts/otter_ledger.py list` — what has already been processed.
2. List recent Otter transcripts via the Otter connector.
3. `python3 scripts/otter_ledger.py check <id> ...` — which are NEW.
4. **If zero new:** print one line — `OTTER sweep: 0 new transcripts (N in ledger)` —
   and STOP. Do not restate old analysis. At 48 fires a day, a chatty no-op is what
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
