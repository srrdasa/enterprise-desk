# /idea-review — the monthly decision session (~30 min, Principal in the loop)

The cadence is the deliverable, not the database. A parked idea nobody revisits is
indistinguishable from a deleted one, except it costs storage and false comfort.

1. AGENDA — `ideas.review_overdue(90)` plus anything whose parked comment names a
   passed re-review date; rank by ICE then Mentions; pin at top, marked MUST-DECIDE,
   anything with Skips ≥ 1. (First-ever session: use the ICE ranking — the top five
   are decidable now.)
2. WALK them one at a time. The Principal chooses exactly ONE of four outcomes and the
   desk EXECUTES it in the same turn:
   - **promote** — create the delivery task in the Tasks DB (Owner/Priority/Due),
     write "Promoted to: <task url>" on the idea, State=Promoted. Promotion is the
     only moment an idea acquires a due date.
   - **park** — comment the new re-review date; set Reviewed = today.
   - **merge** — `add_mention()` on the surviving idea noting the transfer, comment
     the merge on the duplicate, State=Merged.
   - **kill** — State=Killed, one-line reason in a comment. Archived and searchable,
     never deleted.
   An idea the Principal skips gets Skips += 1 — it cannot be skipped twice.
3. RECORD — set Reviewed = today on every idea touched; append the session summary
   (promoted/parked/merged/killed/skipped, one line per decision) as a comment thread
   on the "Reviews" Notion register page (layer PENDING -> carry as a TODO), and post
   the summary to the ideas channel (threaded).
4. REGENERATE — `python3 scripts/ideas.py board`, commit and push.
