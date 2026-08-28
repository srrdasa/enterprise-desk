# Notion setup — the two databases (one-time, ~15 minutes)

The scripts address properties BY NAME. Create them exactly as written (case-sensitive)
or edit the names in `scripts/notion.py` readers — one or the other, consistently.

## 0. The integration
1. notion.so/my-integrations → New integration (internal) → copy the secret → that is
   `NOTION_API_KEY`.
2. **Share BOTH databases with the integration** (••• menu on the database page →
   Connections → your integration). **Notion permissions are page-level: an unshared
   database silently returns empty results or 404.** This is the #1 setup failure.
3. A database's ID is the 32-char hex in its URL (before any `?v=`). Those are
   `NOTION_TASKS_DB` and `NOTION_IDEAS_DB`.

## 1. Tasks database — properties
| Property | Type | Options |
|---|---|---|
| Name | Title | — |
| Status | Select | Open · In Progress · Blocked · Done · Deferred |
| Owner | Select | one option per person the desk tracks (short names fine) |
| Priority | Select | Highest · High · Medium · Low |
| Due | Date | — |
| Area | Multi-select | your workstreams |
| Due moves | Number | starts 0 — incremented ONLY by `move_due()` (rule 6) |
| Waiting on | Text | — |
| Source | Text | where this came from (permalink / MAIL:subject / OPERATOR) |

"Deferred" (still relevant, later) and "Done" (no longer relevant at all) are
different outcomes; don't default to the former.

## 2. Ideas database — properties
| Property | Type | Options |
|---|---|---|
| Name | Title | — |
| State | Select | Open · Promoted · Merged · Killed |
| ICE | Number | 3–30 (sum of three 1–10 scores; reasoning lives in the page body) |
| RICE | Number | only when ICE ≥ 21 |
| Mentions | Number | starts 1 — incremented ONLY by `add_mention()` |
| Category | Multi-select | your idea topics (drives the board clustering) |
| Disposition | Select | IMMEDIATE · FUTURE · ALREADY-COVERED |
| Reviewed | Date | set by /idea-review |
| Skips | Number | review skips — nothing may be skipped twice |
| Promoted to | Text | task URL once promoted |
| Source | Text | person + channel + date |

## 3. Register pages (plain Notion pages, shared with the integration)
- **Credential-Sharing Register** — what system, by whom, to whom, when, channel.
  NEVER the value (rule 11).
- **Contacts** — full name · short names/aliases · Slack display name · Slack ID
  (rule 12).
- **Reviews** — /idea-review session summaries.
- **Weekly Verification** — the weekly output pages.

## 4. Verify
`bash scripts/setup_desk.sh` — both DB checks must PASS before anything else runs.
