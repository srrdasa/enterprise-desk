# Notion setup — registers & knowledge layer only (one-time, ~5 minutes)

Notion is NOT the tracker — tasks and ideas live in ClickUp (`docs/CLICKUP-SCHEMA.md`).
Notion holds the desk's REGISTERS and, later, the organized reference archive.

## 0. The integration (the Principal's 5-minute setup)
1. notion.so/my-integrations → New integration (internal) → copy the secret → that is
   `NOTION_API_KEY`.
2. Create one parent page named **"MKCD Desk Registers"**.
3. **Share that page with the integration** (••• menu → Connections → the integration).
   **Notion permissions are PAGE-LEVEL: an unshared page silently 404s.** This is the
   #1 setup failure.
4. The page's ID is the 32-char hex at the end of its URL → that is
   `NOTION_REGISTERS_PAGE`.
5. Both values go into the cloud environment's env vars (never chat, never files),
   then open a FRESH session — a resumed session keeps stale env.

## 1. Register pages (created by the desk under the parent, on first PASS)
- **Credential-Sharing Register** — what system, by whom, to whom, when, channel.
  NEVER the value (rule 11).
- **Contacts** — full name · short names/aliases · Slack display name · Slack ID ·
  ClickUp user ID (rule 12).
- **Reviews** — /idea-review session summaries.
- **Weekly Verification** — the weekly output pages.

Until the pair of env vars exists, register entries are carried as explicit TODOs in
the digest — never invented elsewhere (setup_desk.sh reports the layer PENDING, not
FAIL).

## 2. Verify
`bash scripts/setup_desk.sh` — Notion registers must show PASS (or PENDING when the
env pair is deliberately absent). A present key with failing auth is a FAIL.
