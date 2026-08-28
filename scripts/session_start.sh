#!/bin/bash
# SessionStart hook — runs on EVERY session. Credential presence only; never values.
missing=""
for v in CLICKUP_API_TOKEN CLICKUP_TASKS_LIST CLICKUP_IDEAS_LIST SLACK_BOT_TOKEN; do
  [ -z "${!v}" ] && missing="$missing $v"
done
if [ -n "$missing" ]; then
  echo "DESK WARNING: missing env vars:$missing — see docs/SECRETS-SETUP.md. Env-var-dependent legs will fail; connector legs still work."
else
  echo "Desk credentials present."
fi
if [ -z "$NOTION_API_KEY" ] || [ -z "$NOTION_REGISTERS_PAGE" ]; then
  echo "DESK NOTE: Notion registers pair not set — registers layer PENDING (docs/NOTION-REGISTERS.md); register entries carried as TODOs."
fi
