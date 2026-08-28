# Secrets & environment setup

Plaintext token files are forbidden. Every entry point gets credentials as ENV VARS:
cloud environment settings, Routine payloads, or GitHub Actions secrets. Values are
never pasted into chat, echoed, or logged — a session that offers "paste the token as
your next message" is violating this file.

## Required (the tracker + Slack)
| Var | What / where to get it |
|---|---|
| CLICKUP_API_TOKEN | ClickUp → Settings → Apps → API Token (personal token) |
| CLICKUP_TASKS_LIST | Tasks list ID — `901616685481` (docs/CLICKUP-SCHEMA.md) |
| CLICKUP_IDEAS_LIST | Ideas list ID — `901616685482` |
| SLACK_BOT_TOKEN | api.slack.com/apps → your app → OAuth → Bot User OAuth Token (xoxb-) |

Slack app bot scopes: `channels:read, groups:read, channels:history, groups:history,
users:read, users:read.email, chat:write, chat:write.customize` — then install to the
workspace and invite the bot to every channel it should sweep. (`users:read.email` is
what lets ORG-STRUCTURE cross-match ClickUp members to Slack by email.)

## Registers layer (Notion — may legitimately be pending at first)
| Var | What |
|---|---|
| NOTION_API_KEY | notion.so/my-integrations → integration secret |
| NOTION_REGISTERS_PAGE | the shared "MKCD Desk Registers" parent page ID (docs/NOTION-REGISTERS.md) |

Absent pair = the battery reports PEND and register entries are carried as TODOs.
A present key that Notion rejects = FAIL, fix it.

## Identity
| Var | Purpose |
|---|---|
| DESK_NAME / DESK_ICON | the bot's posting identity ("MKCD Desk" / icon emoji) |
| DESK_BOT_ID | the bot's Uxxxx (auth.test → user_id) — unanswered.py needs it |
| PRINCIPAL_SLACK_ID | the Principal's HUMAN Uxxxx (Slack profile → ⋮ → Copy member ID). NEVER the bot's own ID — that silently breaks the unanswered-message detector; the battery cross-checks it against auth.test. |
| DESK_TZ_OFFSET_MIN | display timezone, minutes from UTC (IST = 330) |
| SLACK_BOT_TOKEN_2 | optional second workspace |

## Where to put them
1. **Cloud environment** (claude.ai/code → Cloud environments → your env →
   Environment variables) — for interactive + routine sessions. Paste
   `scripts/environment_setup.sh` into the same dialog's Setup script box.
   **After ANY env-var change: open a FRESH session — a resumed session keeps the
   old values.**
2. **GitHub Actions secrets** — only if using `.github/workflows/fire-desk-routine.yml`.

Connectors (Gmail, Outlook, Otter, Slack, Drive, Calendar) are authorized per Claude
account and ticked per Routine — they carry their own auth; no env vars needed.

The SessionStart hook (`scripts/session_start.sh`) checks presence on every session
and warns loudly — presence only, never values.
