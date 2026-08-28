#!/bin/bash
# SessionStart hook — runs on EVERY session. Credential presence only; never values.
missing=""
for v in NOTION_API_KEY NOTION_TASKS_DB NOTION_IDEAS_DB SLACK_BOT_TOKEN; do
  [ -z "${!v}" ] && missing="$missing $v"
done
if [ -n "$missing" ]; then
  echo "DESK WARNING: missing env vars:$missing — see docs/SECRETS-SETUP.md. Env-var-dependent legs will fail; connector legs still work."
else
  echo "Desk credentials present."
fi
