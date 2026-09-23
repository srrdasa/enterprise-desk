# ORG STRUCTURE — HKGT DMT

**STATUS: CONFIRMED — 2026-09-23.**
Source: `Org_Structre_RR_Sep_2026.xlsx`, the Principal's HR org sheet (OPERATOR,
supplied 2026-09-17; applied and confirmed 2026-09-23). It supersedes the ClickUp-inferred structure confirmed
2026-08-28: the sheet is authority for name, designation, department and reporting
line. ClickUp IDs, emails and Slack IDs are carried over from that earlier file for
the 24 people who matched, and are the ONLY way the desk can assign or @-mention.

**Headcount: 50 on the sheet** (up from 26 tracked in August). 24 carry a desk
identity; **26 have no ClickUp account known to the desk** and cannot be assigned
work in the tracker until one is matched.

## Routing — read this before inferring an owner

`.claude/commands/meeting.md` step 2 routes department-of-topic work to a department
head. The August rule (one HOD for all departments, `All Depts` as a wildcard) is
**withdrawn** — this sheet carries real per-department heads and a per-person Manager.
Do NOT match on the bare token `HOD`: only one person's designation contains it, and
routing every department to them would be wrong.

| Department | Head for routing | Basis |
|---|---|---|
| Yatra | Byreddy Saivardhan Reddy | designation 'Yatra Manager'; appears as manager 'Sai Vardhan' for 15 of the 17 |
| Marketing | Hem Chand Tunga | designation 'Head - Digital Marketing'; manages 4 of the 8 |
| Online Presence | Maddela Satish | designation 'Graphics - HOD'; Praveen is a sub-lead under him for 6 |
| Fund Raising | **UNRESOLVED — route to MKCD** | three managers split it — MKCD (3), Nama Prabhu Dasa (3), Shravan (2) — and no Head/HOD designation |
| HR | **UNRESOLVED — route to MKCD** | Rajendra Prasad Kandepu is 'HR Manager' but the sheet has both HR staff reporting to MKCD, not to him |
| Kirtan | **UNRESOLVED — route to MKCD** | both report to MKCD directly |
| AI | **UNRESOLVED — route to MKCD** | reports to MKCD directly |
| Culture Connect | **UNRESOLVED — route to MKCD** | single volunteer, reports to MKCD directly |
| ERP | **UNRESOLVED — route to MKCD** | reports to 'HG Lakshmikanth Prabhu', who has no row and no desk identity |
| Office Assistant | **UNRESOLVED — route to MKCD** | reports to MKCD directly |

**Fallback:** every row's Next Level Reporting is `MKCD` (Mukunda Dasa, the
Principal). An UNRESOLVED department, or any topic that does not map cleanly to one,
goes to him — not to a guessed head.

## The table

Manager and Reporting Authority are copied verbatim from the sheet. `MKCD` is the
Principal. Next Level Reporting is `MKCD` for all 50 rows, so it is not repeated as a
column. A blank ClickUp ID means the desk has no account for that person.

### Yatra — 17

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 33 | Sudhir | Sudhir | Volunteer | MKCD | MKCD | — | — |
| 34 | Pradyut Kumar Das | Prema Rupa Dasa | Senior Yatra Coordinator | Sai Vardhan | STDD | 100908346 | — |
| 35 | Vikash Kumar | — | Senior Tele Sales Executive | Sai Vardhan | STDD | — | — |
| 36 | D Narsing Rao | — | Tele Sales Executive | Sai Vardhan | STDD | — | — |
| 37 | Anthati Sai Kumar | — | Tele Sales Executive | Sai Vardhan | STDD | — | — |
| 38 | Lingala Sai Sharath | — | Tele Sales Executive | Sai Vardhan | STDD | — | — |
| 39 | Ramesh J | Radha Giridhari Dasa | Fund Raising Executive | Sai Vardhan | STDD | — | — |
| 40 | Rajashekhar Reddy | — | Fund Raising Executive | Sai Vardhan | STDD | — | — |
| 41 | S Sudhakar | Sudhakar | Fund Raiser | Sai Vardhan | STDD | — | — |
| 42 | G Sai Kiran | — | Tele Sales Executive | Sai Vardhan | STDD | — | — |
| 43 | Deepak Kumar | — | Senior Yatra Admin Executive | Sai Vardhan | STDD | 100908342 | U0BTHE6D1RP |
| 44 | Nagella Banusundar | Arjun Bandhu Dasa | Senior Yatra Coordinator | Sai Vardhan & MKCD | STDD | 100909875 | — |
| 45 | V Naveen Kumar | — | Accounts Executive | Sai Vardhan & MKCD | STDD | 100908344 | — |
| 46 | Sashikanta Sahoo | Sahoo | Fund Raising Executive | Sai Vardhan & MKCD | STDD | 100918048 | — |
| 47 | Racharla Naveen Kumar | — | Admin Executive | Sai Vardhan & MKCD | STDD | 106800112 | — |
| 48 | Angadala Naga Hanumaya Kumar | — | Junior Accounts Executive | Sai Vardhan & MKCD | STDD | — | — |
| 49 | Byreddy Saivardhan Reddy | — | Yatra Manager | STDD & MKCD | STDD | — | — |

### Fund Raising — 8

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 4 | Adicherla Naresh | Nama Prabhu Dasa | Fund Raising Executive | MKCD | MKCD | 100909874 | — |
| 5 | B Sharvana Kumar | — | Senior Fund Raising Executive | MKCD | MKCD | 100908345 | — |
| 6 | Yankiral Shiv Raj | — | Driver | MKCD | MKCD | — | — |
| 7 | P Srilakshmi Sailaja | — | Telesales Manager | Nama Prabhu Dasa | MKCD | — | — |
| 8 | Shiva Vara Prasad | — | Assistant - Outreach | Nama Prabhu Dasa | MKCD | — | — |
| 9 | Venkatesh - Auto Driver | — | Auto Driver | Nama Prabhu Dasa | MKCD | — | — |
| 10 | Nelluru Charan Kumar | — | Assistant - Outreach | Shravan | MKCD | 101083310 | — |
| 11 | Anji - Auto Driver | — | Auto Driver | Shravan | MKCD | — | — |

### Marketing — 8

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 16 | Himanshu Bisoyi | — | Full-Stack Developer | Hem Chand | STDD | 100908348 | U0BSXM1A1L7 |
| 17 | Kouloju Sumanth | — | SEO Specialist | Hem Chand | STDD | 100908337 | — |
| 18 | Gugulothu Venkatesh | — | PPC | Hem Chand | STDD | 218543610 | — |
| 19 | Venigalla Sayikiran | — | CRM Executive | Hem Chand | STDD | 100908340 | — |
| 20 | Manikanta Y | Maha Bhuja Dasa | **[[unverified: sheet cell holds a name, not a designation]]** | MKCD | MKCD | 260630579 | U0BTGRHEYEQ |
| 21 | Hem Chand Tunga | — | Head - Digital Marketing | STDD | STDD | 100828205 | — |
| 22 | Srinivas Mahankali — Consultant | — | Consultant | STDD | STDD | — | — |
| 23 | Aniket - DYGN Media Consultant | — | Consultant | STDD | STDD | — | — |

### Online Presence — 8

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 25 | Pinnoju Shashank | — | Video Editor | Praveen | STDD | — | — |
| 26 | Chenna Reddy Gujjula | — | Photographer | Praveen | STDD | — | — |
| 27 | Nagavishnu | — | Video Editor | Praveen | STDD | 101043738 | — |
| 28 | Kanukuntla Venugopal | — | Content Creator | Praveen | STDD | 100937968 | — |
| 29 | Merugu Akhil | — | Digital Marketing SEO | Praveen | STDD | 101043740 | — |
| 30 | Sai Bharath Vamshi | — | Senior Video Editor | Praveen | STDD | 95095479 | U0BTFS3PP4J |
| 31 | Vanamamulai Praveen | — | Senior Graphic Designer | Satish & STDD | STDD | 95095480 | U0BU7CS2JN4 |
| 32 | Maddela Satish | — | Graphics - HOD | STDD | STDD | 101054675 | — |

### HR — 2

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 12 | Rajendra Prasad Kandepu | — | HR Manager | MKCD | MKCD | — | — |
| 13 | Parishetty Gnaneshwar | — | HR Executive | MKCD | MKCD | 100909505 | — |

### Kirtan — 2

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 14 | Amit Mondal | Amrita Nimai Dasa | Kirtaniya | MKCD | MKCD | — | — |
| 15 | Madhu Mangal Das | — | Kirtaniya | MKCD | MKCD | — | — |

### AI — 1

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 1 | Bala Ganesh | Bala Mukunda Dasa | AI | MKCD | MKCD | — | — |

### Culture Connect — 1

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 2 | Suguna Radha Devi Dasi | Suguna Radha Devi Dasi | Volunteer | MKCD | MKCD | 266585199 | — |

### ERP — 1

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 3 | Saikumar Dumpetti | — | ERP Developer | HG Lakshmikanth Prabhu | STDD | — | — |

### Office Assistant — 1

| # | Name (as per Aadhaar) | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 24 | Purushottam Sharma | — | Office Associate | MKCD | MKCD | — | — |

### No department on the sheet

| # | Name | Spiritual name | Designation | Manager | Reporting Auth. | ClickUp ID | Slack ID |
|---|---|---|---|---|---|---|---|
| 50 | P Ravi Kumar | — | Senior Video Editor | — | — | 101084085 | U0BTH59V9M2 |

Row 50 is the only row with no department and no manager, and it belongs to one of
the six people the desk can still @-mention. Placing him is a one-line fix worth
making in the source sheet.

## Desk accounts NOT on the HR sheet

Real ClickUp accounts the desk still sees. They are not employees on this sheet, so
they carry no department; never route department work to them.

| Name | ClickUp ID | Email | Slack ID | Note |
|---|---|---|---|---|
| Mukunda Dasa (the Principal) | 100877577 | mkcd@hkmhyderabad.org | U0BN7BW55C0 | appears on the sheet as `MKCD`, the reporting authority for all 50 |
| Mukunda Prabhu Exe Asst | 100910556 | dmt@hkmhyderabad.org | — | shared account (`dmt@`), not an individual |
| (no name on the account) | 106864846 | — | — | zero tasks, no Slack match; likely an integration |

## Unresolved identities — raise before they enter any draft (rule 12)

These appear as managers or reporting authorities but have no row on the sheet and no
entry in the Contacts register, so the desk cannot tag them or assign to them:

- **`STDD`** — Reporting Authority for **32 of the 50**, more than anyone except the
  Principal. The single most load-bearing unknown in this file.
  `[[unverified: initialism not resolved to a person]]`
- **`HG Lakshmikanth Prabhu`** — manager of the ERP developer (row 3).
  `[[unverified: no desk identity]]`
- **`Shravan`** — manager of rows 10 and 11. Almost certainly row 5, B Sharvana Kumar,
  but the spelling differs. `[[unverified: inferred from spelling, not confirmed]]`

## Slack tagging coverage — 6 of 50

Only these people can be @-mentioned. The desk tags by Slack user ID (rule 12 — a
short name does not resolve); **the other 44 must be named in plain text**, with the
tag noted as unavailable. Never invent a handle.

| Name | Slack ID | Department |
|---|---|---|
| Himanshu Bisoyi | U0BSXM1A1L7 | Marketing |
| Manikanta Y | U0BTGRHEYEQ | Marketing |
| Sai Bharath Vamshi | U0BTFS3PP4J | Online Presence |
| Vanamamulai Praveen | U0BU7CS2JN4 | Online Presence |
| Deepak Kumar | U0BTHE6D1RP | Yatra |
| P Ravi Kumar | U0BTH59V9M2 | — |

Coverage fell from 7-of-27 to 6-of-50: the roster nearly doubled while the number of
matched Slack accounts did not move, and the Principal's own ID now sits outside the
employee table. Getting the 44 into Slack under their `@hkmhyderabad.org` addresses is
the single highest-leverage fix for outbound drafting.

## Source-sheet corrections applied

Spelling normalised here; **the source sheet still carries the original** and is worth
fixing there so the next import is clean:

- `HR Manger` → HR Manager
- `Photo Grapher` → Photographer
- `Senior Yatra Cordinator` → Senior Yatra Coordinator
- `Srinivas Mahankali-Conslutant` → Srinivas Mahankali — Consultant
- Row 20 (Manikanta Y): the Designation cell repeats his spiritual name
  "Maha Bhuja Dasa" instead of a designation — his actual designation is unknown.

## Identity matches ratified by the Principal, 2026-09-23

Four August rows could not be matched to this sheet by name. The Principal confirmed
all four, which is what preserves their ClickUp and Slack IDs:

- `Vishnu` = **Nagavishnu** (row 27) · `Ravi Pusthela` = **P Ravi Kumar** (row 50)
- `Naveen R` = **Racharla Naveen Kumar** (row 47) · `Saci Ku Gauranga Dasa` =
  **Venigalla Sayikiran** (row 19)

_Sources: `Org_Structre_RR_Sep_2026.xlsx` (OPERATOR, supplied 2026-09-17) for every name,
designation, department and reporting line. ClickUp IDs, emails and Slack IDs:
ClickUp workspace "Hare Krishna Movement" + Slack roster, fetched 2026-08-28 by
`scripts/org_fetch.py`, carried forward through the joins above._
