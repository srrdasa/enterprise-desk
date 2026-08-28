# Routine prompt — Weekly Verification (e.g. Fri 10:00 local)
Paste the block below as the Routine's prompt.

---
Run the weekly verification pass (context/credentials in this session):
0. TOOLING — same as the daily loop step 0: ClickUp + Slack via env-var scripts
   (Notion only for registers, PENDING legal), connector legs skip-not-abort,
   marked in the output.
1. TRACKER HYGIENE — FULL `python3 scripts/tracker_audit.py`. Every finding gets a
   decision this cycle: close it, correct the stale claim (re-verify against the live
   source first — never just re-assert it), merge the duplicate, or renegotiate the
   twice-slipped date with its owner. Nothing carries over silently to next week.
2. IDEA PIPELINE — CHECK 4 output: if reviews are due, tell the Principal in the weekly
   summary to run /idea-review (do not run it unattended — the decisions are his).
   Regenerate the board: `python3 scripts/ideas.py board`, commit and push
   boards/idea-board.md. Read the Movement section: two quiet weeks in a row is the
   early warning that the board is drifting back to a graveyard — say so.
3. PROMISE WALK — every open commitment TO us (rule 2 list 2): kept? Chase-worthy?
   Update with evidence, claimed-by-them until a system confirms.
4. REGISTERS — walk the Credential-Sharing Register and Contacts register for anything
   the week's sweeps surfaced but did not record; reconcile.
5. VOICE — `python3 -c "import sys; sys.path.insert(0,'scripts'); from edit_log import summary; print(summary())"` —
   include the drafts/unedited/median-ratio line in the weekly summary. If a correction
   pattern hit three instances this week, propose the durable rule for
   docs/VOICE-AND-PREFERENCES.md (rule 10).
6. OUTPUT — a "Weekly Verification — [date]" page under the Notion registers parent
   (layer PENDING -> keep the output in the summary and say so) + candid summary to the
   Principal's channel.
STYLE: short plain messages; no credentials anywhere.
