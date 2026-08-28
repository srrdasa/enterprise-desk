#!/bin/bash
# One-command setup & test battery. Run this first in any new session.
# Checks env vars, ClickUp auth + both lists, Slack auth, the OPTIONAL Notion
# registers layer (WARN if absent, FAIL if present-but-rejected), helper imports,
# routine files, git remote. Reports each check PASS/FAIL and never prints a secret.
cd "$(dirname "$0")/.." || exit 1
pass() { echo "PASS  $1"; }
fail() { echo "FAIL  $1"; FAILED=1; }

for v in CLICKUP_API_TOKEN CLICKUP_TASKS_LIST CLICKUP_IDEAS_LIST SLACK_BOT_TOKEN; do
  [ -n "${!v}" ] && pass "env $v present" || fail "env $v MISSING (docs/SECRETS-SETUP.md)"
done
for v in DESK_NAME DESK_BOT_ID PRINCIPAL_SLACK_ID DESK_TZ_OFFSET_MIN; do
  [ -n "${!v}" ] && pass "env $v present" || echo "WARN  env $v not set (identity defaults will be used)"
done
if [ -n "$NOTION_API_KEY" ] && [ -n "$NOTION_REGISTERS_PAGE" ]; then
  pass "env Notion registers pair present"
elif [ -n "$NOTION_API_KEY" ] || [ -n "$NOTION_REGISTERS_PAGE" ]; then
  fail "Notion registers HALF-configured (one of NOTION_API_KEY/NOTION_REGISTERS_PAGE missing)"
else
  echo "PEND  Notion registers not configured — register entries carried as TODOs (docs/NOTION-REGISTERS.md)"
fi
if [ "$PRINCIPAL_SLACK_ID" = "$DESK_BOT_ID" ] && [ -n "$DESK_BOT_ID" ]; then
  fail "PRINCIPAL_SLACK_ID equals DESK_BOT_ID — it must be the Principal's HUMAN member ID (breaks unanswered.py silently)"
fi

python3 - << 'PY'
import os, sys; sys.path.insert(0, 'scripts')
try:
    import clickup as C
    st, me = C.api('GET', '/user')
    print(('PASS' if st == 200 else 'FAIL') + f'  ClickUp auth (HTTP {st})')
    for name, env in (('Tasks', 'CLICKUP_TASKS_LIST'), ('Ideas', 'CLICKUP_IDEAS_LIST')):
        lid = os.environ.get(env, 'MISSING')
        st, r = C.api('GET', f'/list/{lid}')
        print(('PASS' if st == 200 else 'FAIL') + f'  ClickUp {name} list reachable (HTTP {st})')
        if st == 200:
            try:
                C.fields(lid)
                print(f'PASS  ClickUp {name} custom fields readable ({len(C.fields(lid))} fields)')
            except RuntimeError as e:
                print('FAIL ', e)
    import ideas, tracker_audit, pending, slack, edit_log, wa_parse, notion
    print('PASS  all helper scripts import')
    from slack import sl
    r = sl('auth.test')
    print(('PASS' if r.get('ok') else 'FAIL') + f"  Slack auth ({r.get('user', '?')})")
    if r.get('ok') and os.environ.get('PRINCIPAL_SLACK_ID') == r.get('user_id'):
        print('FAIL  PRINCIPAL_SLACK_ID is the BOT\'s own ID (auth.test user_id) — set the Principal\'s human member ID')
    if notion.registers_available():
        st, me = notion.api('GET', '/users/me')
        print(('PASS' if st == 200 else 'FAIL') + f'  Notion registers auth (HTTP {st})')
        st, r = notion.api('GET', f"/pages/{os.environ['NOTION_REGISTERS_PAGE']}")
        print(('PASS' if st == 200 else 'FAIL') + f'  Notion registers page reachable (HTTP {st})' +
              ('' if st == 200 else ' — is the page SHARED with the integration? Notion permissions are page-level.'))
    else:
        print('PEND  Notion registers layer not configured — skipped (see docs/NOTION-REGISTERS.md)')
except SystemExit as e:
    print('FAIL ', e)
except Exception as e:
    print('FAIL ', type(e).__name__, str(e)[:200])
PY

for f in routines/daily-ops-loop.md routines/weekly-verification.md CLAUDE.md docs/CLICKUP-SCHEMA.md; do
  [ -f "$f" ] && pass "$f present" || fail "$f MISSING"
done
git remote -v | grep -q origin && pass "git remote configured" || fail "no git remote"
[ -z "$FAILED" ] && echo "ALL CHECKS COMPLETE" || echo "FIX FAILURES BEFORE RUNNING THE DESK"
