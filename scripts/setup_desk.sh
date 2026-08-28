#!/bin/bash
# One-command setup & test battery. Run this first in any new session.
# Checks env vars, Notion auth + both databases, Slack auth, helper imports,
# routine files, git remote. Reports each check PASS/FAIL and never prints a secret.
cd "$(dirname "$0")/.." || exit 1
pass() { echo "PASS  $1"; }
fail() { echo "FAIL  $1"; FAILED=1; }

for v in NOTION_API_KEY NOTION_TASKS_DB NOTION_IDEAS_DB SLACK_BOT_TOKEN; do
  [ -n "${!v}" ] && pass "env $v present" || fail "env $v MISSING (docs/SECRETS-SETUP.md)"
done
for v in DESK_NAME DESK_BOT_ID PRINCIPAL_SLACK_ID; do
  [ -n "${!v}" ] && pass "env $v present" || echo "WARN  env $v not set (identity defaults will be used)"
done

python3 - << 'PY'
import sys; sys.path.insert(0, 'scripts')
try:
    import notion as N
    st, me = N.api('GET', '/users/me')
    print(('PASS' if st == 200 else 'FAIL') + f'  Notion auth (HTTP {st})')
    for name, db in (('Tasks', 'NOTION_TASKS_DB'), ('Ideas', 'NOTION_IDEAS_DB')):
        import os
        st, r = N.api('GET', f'/databases/{os.environ.get(db, "MISSING")}')
        ok = st == 200
        print(('PASS' if ok else 'FAIL') + f'  Notion {name} DB reachable (HTTP {st})' +
              ('' if ok else ' — is the DB SHARED with the integration? Notion permissions are page-level.'))
    import ideas, tracker_audit, pending, slack, edit_log, wa_parse
    print('PASS  all helper scripts import')
    from slack import sl
    r = sl('auth.test')
    print(('PASS' if r.get('ok') else 'FAIL') + f"  Slack auth ({r.get('user', '?')})")
except SystemExit as e:
    print('FAIL ', e)
except Exception as e:
    print('FAIL ', type(e).__name__, str(e)[:200])
PY

for f in routines/daily-ops-loop.md routines/weekly-verification.md CLAUDE.md; do
  [ -f "$f" ] && pass "$f present" || fail "$f MISSING"
done
git remote -v | grep -q origin && pass "git remote configured" || fail "no git remote"
[ -z "$FAILED" ] && echo "ALL CHECKS COMPLETE" || echo "FIX FAILURES BEFORE RUNNING THE DESK"
