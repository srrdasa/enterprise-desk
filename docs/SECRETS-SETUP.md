# Secrets & environment setup

Plaintext token files are forbidden. Every entry point gets credentials as ENV VARS:
cloud environment settings, Routine payloads, or GitHub Actions secrets.

## Required
| Var | What / where to get it |
|---|---|
| NOTION_API_KEY | notion.so/my-integrations → your integration → secret |
| NOTION_TASKS_DB | Tasks database ID (32-hex from its URL) |
| NOTION_IDEAS_DB | Ideas database ID |
| SLACK_BOT_TOKEN | api.slack.com/apps → your app → OAuth → Bot User OAuth Token (xoxb-) |

Slack app bot scopes: `channels:read, groups:read, channels:history, groups:history,
users:read, chat:write, chat:write.customize` — then install to the workspace and
invite the bot to every channel it should sweep.

## Recommended
| Var | Purpose |
|---|---|
| DESK_NAME / DESK_ICON | the bot's posting identity (e.g. "PK's Desk" / :file_cabinet:) |
| DESK_BOT_ID | the bot's Uxxxx (auth.test → user_id) — unanswered.py needs it |
| PRINCIPAL_SLACK_ID | the Principal's Uxxxx — so his replies count as "answered" |
| DESK_TZ_OFFSET_MIN | display timezone, minutes from UTC (IST = 330) |
| SLACK_BOT_TOKEN_2 | optional second workspace |

## Where to put them
1. **Cloud environment** (claude.ai/code → Cloud environments → your env →
   Environment variables) — for interactive + routine sessions. Paste
   `scripts/environment_setup.sh` into the same dialog's Setup script box.
2. **GitHub Actions secrets** — only if using `.github/workflows/fire-desk-routine.yml`.

Connectors (Gmail, Outlook, Otter, Slack, Drive, Calendar) are authorized per Claude
account and ticked per Routine — they carry their own auth; no env vars needed.

The SessionStart hook (`scripts/session_start.sh`) checks presence on every session
and warns loudly — presence only, never values.
