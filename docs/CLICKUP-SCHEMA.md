# ClickUp setup — the tracker's two lists

ClickUp is the desk's tracker (tasks + ideas). Notion holds only the registers &
knowledge layer — see `docs/NOTION-REGISTERS.md`. The scripts address custom fields
BY NAME (case-sensitive); `scripts/clickup.py` fetches field IDs once per session and
fails PLAINLY, naming the missing field, if one is absent.

## 0. Credentials & lists
| Env var | Value |
|---|---|
| CLICKUP_API_TOKEN | ClickUp → Settings → Apps → API Token (personal token) |
| CLICKUP_TASKS_LIST | `901616685481` |
| CLICKUP_IDEAS_LIST | `901616685482` |

Verify any list ID from its URL (`.../li/<id>`) or `python3 scripts/clickup.py smoke`.

## 1. Native features carry the core (never duplicate them as custom fields)
| Desk concept | ClickUp native |
|---|---|
| Status | list statuses: **Open · In Progress · Blocked · Done · Deferred** (Tasks list). Done/Deferred are done-type. "Deferred" (still relevant, later) ≠ "Done". |
| Owner | native **assignees** (real ClickUp users — never a text field) |
| Priority | native priority: Urgent=Highest · High · Normal=Medium · Low |
| Due | native due date — changed ONLY via `move_due()` (rule 6) |
| Category | native **tags** (drives the idea-board clustering) |

## 2. Tasks list (901616685481) — custom fields
| Field | Type | Notes |
|---|---|---|
| Due moves | number | starts 0 — incremented ONLY by `move_due()` (rule 6) |
| Waiting on | short text | — |
| Source | short text | where this came from (permalink / MAIL:subject / OPERATOR / transcript link) |

## 3. Ideas list (901616685482) — custom fields
| Field | Type | Notes |
|---|---|---|
| State | dropdown | Open · Promoted · Merged · Killed |
| ICE | number | 3–30 (sum of three 1–10 scores; reasoning in the task description) |
| RICE | number | only when ICE ≥ 21 |
| Mentions | number | starts 1 — incremented ONLY by `ideas.add_mention()` |
| Skips | number | review skips — nothing may be skipped twice |
| Disposition | dropdown | IMMEDIATE · FUTURE · ALREADY-COVERED |
| Reviewed | date | set by /idea-review |
| Promoted to | short text | task URL once promoted |
| Source | short text | person + channel + date |

Ideas carry NO due date and NO assignee until promotion — promotion is the only
moment an idea acquires either (rule 8).

## 4. API notes the scripts already encode (don't relearn them)
- Personal tokens go in the `Authorization` header WITHOUT a "Bearer" prefix.
- Dates travel as millisecond epochs; `clickup.py` converts, rendering due dates in
  DESK_TZ_OFFSET_MIN and writing them at local noon so the calendar day survives
  timezone conversion.
- Dropdown values are set by option NAME through `set_field()` (which resolves the
  option id); reading returns the option name.
- List queries page at 100; `q()` walks pages and includes closed tasks — callers
  filter with `is_done_status()`.

## 5. Verify
`bash scripts/setup_desk.sh` — ClickUp auth + both lists must PASS before anything
else runs. `python3 scripts/clickup.py fields` prints every custom field with its ID.
