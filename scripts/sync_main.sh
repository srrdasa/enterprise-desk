#!/bin/bash
# Land this session's work on main. Run at the end of EVERY session that changed files.
set -e
git add -A
git diff --cached --quiet || git commit -m "${1:-desk: session update}"
git fetch origin
git rebase origin/main || { echo "REBASE CONFLICT — resolve, then: git rebase --continue && bash scripts/sync_main.sh"; exit 1; }
git push origin HEAD:main
echo "Landed on main: $(git rev-parse --short HEAD)"
