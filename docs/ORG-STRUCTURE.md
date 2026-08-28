# ORG STRUCTURE — HKGT DMT

**STATUS: CONFIRMED — 2026-08-28.**
Applied from the Principal's Notion editing surface
(https://app.notion.com/p/3ca81bf463b48175b6b9cf9138a06a84, read back 2026-08-28) —
his **✏️ Department** and **✏️ Designation** values are written into the Department
and Designation columns below and override every inferred value. The assignment
engine reads this file.

**HOD resolution (set by the Principal, 2026-08-28): one HOD for all departments.**
Row 10, Mukunda Dasa, is `All Depts` / `HOD`. `All Depts` is a WILDCARD — it matches
every department name in this table. So department-of-topic inference
(`.claude/commands/meeting.md` ASSIGNMENT STEP 2) resolves to row 10 for Graphics,
Digital Marketing, Fund Raising, Yatra, HR, Culture Connect and Online
Communications alike. No department has its own head; that is deliberate, not a gap.
Do not read a department-level "Manager" or "Senior Manager" designation as an HOD —
`HOD` is the only token the engine matches.

**Editing surface stays Notion:** the Principal edits the page above; the desk reads
it back on his word, re-applies both ✏️ columns here, re-dates this header, and
commits. Corrections may also be given in chat by row number ("3: Graphics, HOD ·
7: skip"). `skip` in Department excludes a person from the desk entirely.

NOTE on the two evidence columns, which describe the ORIGINAL automated fetch and are
NOT a judgement on the confirmed values: **Role** is the ClickUp PERMISSION level
(owner/admin/member/guest) — never a job title, and never overwritten by Designation.
**ID match** is how confidently the person was matched to a Slack account by email —
`high` means a Slack ID was found, `low` means none was. A `low` row's Department and
Designation are still Principal-confirmed fact.

| # | Name | ClickUp ID | Email | Slack ID | Department | Designation | Role | ID match | Evidence (fetch 2026-08-28) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Akhil | 101043740 | sme@hkmhyderabad.org | — | Online Communications | Social Media Executive | member | low | 4 recent tasks in "MOM Tasks by MKCD / May"; no Slack match found |
| 2 | Arjunabandhudas | 100909875 | arbd@hkmhyderabad.org | — | Yatra | Yatra Guide | member | low | 124 recent tasks in "Yatra / office works"; no Slack match found |
| 3 | Bharath Vamshi | 95095479 | asb.vamshi@hkmhyderabad.org | U0BTFS3PP4J | Graphics | Video Editor | member | high | 169 recent tasks in "Graphics Team / Bharth Tasks List"; email match |
| 4 | CHARAN NELLURU | 101083310 | preach-asst@hkmhyderabad.org | — | Fund Raising | FR Assistant | member | low | 11 recent tasks in "Charan Tasks / daily task"; no Slack match found |
| 5 | Deepak kumar | 100908342 | deepak.v@hkmhyderabad.org | U0BTHE6D1RP | Yatra | Admin | member | high | 99 recent tasks in "Deepak Tasks / List"; email match |
| 6 | Gnaneshwar Parishetty | 100909505 | hrexec-dmt@hkmhyderabad.org | — | HR | HR Executive | member | low | 13 recent tasks in "Gnaneshwar Tasks / Daily Tasks"; no Slack match found |
| 7 | Hem Chand Tunga | 100828205 | manager@hkmhyderabad.org | — | Digital Marketing | Marketing Manager | owner | low | 190 recent tasks in "Daily Tasks / Grenaral Tasks"; no Slack match found |
| 8 | Himanshu Bisoyi | 100908348 | webdeveloper@hkmhyderabad.org | U0BSXM1A1L7 | Digital Marketing | Web Developer | admin | high | 5 recent tasks in "14.05.2026 MOM TASKS / List"; email match |
| 9 | MAHA BHUJA DASA | 260630579 | mhbd@hkmhyderabad.org | U0BTGRHEYEQ | Digital Marketing | Senior Manager | admin | high | 72 recent tasks in "MHBD Prabhu Tasks / MHBP Tasks"; email match |
| 10 | Mukunda Dasa (the Principal) | 100877577 | mkcd@hkmhyderabad.org | U0BN7BW55C0 | All Depts | HOD | admin | high | 72 recent tasks in "24.06.2026 MOM TASKS / List"; email match |
| 11 | Mukunda Prabhu Exe Asst | 100910556 | dmt@hkmhyderabad.org | — | All Depts | Executive Assistant | admin | low | shared account; 72 recent tasks in "24.06.2026 MOM TASKS / List"; no Slack match found |
| 12 | Nama Prabhu | 100909874 | namaprabhu@hkmhyderabad.org | — | Fund Raising | FR Preacher | member | low | 34 recent tasks in "24.06.2026 MOM TASKS / List"; no Slack match found |
| 13 | Naveen R | 106800112 | dmt-accounts@hkmhyderabad.org | — | Fund Raising | DCC Coordinator | member | low | 1 recent task in "Sharavan tasks / List"; no Slack match found |
| 14 | Praveen | 95095480 | praveen.v@hkmhyderabad.org | U0BU7CS2JN4 | Graphics | Senior Designer | member | high | 129 recent tasks in "Graphics Team / Praveen Tasks List"; email match |
| 15 | Prema Rupa dasa | 100908346 | yatra1@hkmhyderabad.org | — | Fund Raising | FR Preacher | member | low | 62 recent tasks in "Prabhus Tasks / Prema Rupa Prabhu"; no Slack match found |
| 16 | Ravi Pusthela | 101084085 | ravi.pusthela@hkmhyderabad.org | U0BTH59V9M2 | Graphics | Designer | member | high | 92 recent tasks in "Designer Task Assignment Sheet / Ravi"; email match |
| 17 | Saci Ku Gauranga Dasa | 100908340 | skgd@hkmhyderabad.org | — | Digital Marketing | CRM Executive | member | low | 28 recent tasks in "Prabhus Tasks / Saci Kumar Gauranga Prabhu"; no Slack match found |
| 18 | Sashikanta | 100918048 | preacher1@hkmhyderabad.org | — | Culture Connect | Lead Coordinator | member | low | 56 recent tasks in "24.06.2026 MOM TASKS / List"; no Slack match found |
| 19 | Satish Maddela | 101054675 | satish.maddela@hkmhyderabad.org | — | Online Communications | Manager | member | low | 40 recent tasks in "HKGT Temple Works / Temple Works"; no Slack match found |
| 20 | SHARAVAN KUMAR B | 100908345 | sharavan.b@hkmhyderabad.org | — | Fund Raising | FR Preacher | member | low | 93 recent tasks in "Sharavan tasks / List"; no Slack match found |
| 21 | Shree Lakshmi | 266585199 | sugunaradhadevidasi@gmail.com | — | Culture Connect | Manager | member | low | external gmail address; 15 recent tasks in "Prabhus Tasks / Sashikanta Sahoo"; no Slack match found |
| 22 | Sumanth | 100908337 | seo@hkmhyderabad.org | — | Digital Marketing | SEO | member | low | 38 recent tasks in "HKM SEO / List"; no Slack match found |
| 23 | V NAVEEN KUMAR | 100908344 | accounts.tridas@hkmhyderabad.org | — | Yatra | Accounts Executive | member | low | 1 recent task in "Prabhus Tasks / Sharavan Prabhu Tasks"; no Slack match found |
| 24 | Venkatesh (PPC) | 218543610 | dme1@hkmhyderabad.org | — | Digital Marketing | PPC | member | low | 195 recent tasks in "HKGT Performance Marketing / HKGT Daily Tasks"; no Slack match found |
| 25 | venugopal | 100937968 | conwri@hkmhyderabad.org | — | Online Communications | Content Writer | member | low | 2 recent tasks in "09.04.2026 MOM TASKS / List"; no Slack match found |
| 26 | Vishnu | 101043738 | editor1@hkmhyderabad.org | — | Online Communications | Video Editor | member | low | 37 recent tasks in "Designer Task Assignment Sheet / vishnu"; no Slack match found |

## UNPLACED (no department signal — stays unplaced until the Principal places them)

- 27. (no name) (ClickUp 106864846, Slack —, admin) — no recent task assignments; no
  Slack match found. Left blank by the Principal on the Notion page, so the fetch
  result stands: UNPLACED. Never a routing target.

## Department roll-up (derived from the table above — 26 placed, 1 unplaced)

| Department | Count | Rows |
|---|---|---|
| Digital Marketing | 6 | 7, 8, 9, 17, 22, 24 |
| Fund Raising | 5 | 4, 12, 13, 15, 20 |
| Online Communications | 4 | 1, 19, 25, 26 |
| Graphics | 3 | 3, 14, 16 |
| Yatra | 3 | 2, 5, 23 |
| Culture Connect | 2 | 18, 21 |
| All Depts | 2 | 10, 11 |
| HR | 1 | 6 |

## Slack tagging coverage — 7 of 27

Only rows 3, 5, 8, 9, 10, 14, 16 carry a Slack ID. The desk tags by Slack user ID
(rule 12 — a short name does not resolve), so **the other 20 cannot be @-mentioned in
any outbound draft.** Name them in plain text and say the tag is unavailable; never
invent a handle. This clears itself when they join Slack under their
`@hkmhyderabad.org` address and `scripts/org_fetch.py` runs again.

_Sources: ClickUp workspace "Hare Krishna Movement" (members, groups, 90 lists, task
sample) + Slack roster (emails), fetched 2026-08-28 by `scripts/org_fetch.py` — WARN
at fetch time: 2 ClickUp workspaces visible, used "Hare Krishna Movement". Department
and Designation: OPERATOR (the Principal, via the Notion page, read back 2026-08-28)._
