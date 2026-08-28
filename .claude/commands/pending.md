# /pending — person-wise pending list (ClickUp → chat-ready)

**Usage:** `/pending <owner> [--all]`

Run `python3 scripts/pending.py <owner>` FIRST — it applies the near-term filter
(overdue / due 7d / Highest), the unverified flag, and render_line(). Never hand-write
the query or the line format (rules 6–7).

Then, for each UNVERIFIED item: re-verify against the live source (the thread, the
mail, the related task, or the person) and update the task — or keep it in the
explicit "unverified — please confirm" section. Post one message per person, grouped
by who they must connect with, full detail so nobody has to open ClickUp to act.
`--all` drops the near-term filter; default is near-term only — a far-future item is
not a current ask.
