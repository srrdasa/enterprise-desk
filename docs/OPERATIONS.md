# Operations Manual — FILL THIS IN before first use

## 1. Identity (the desk cannot run on placeholders)
- Principal: <name> · Slack ID <Uxxxx> · mailboxes: <gmail addr>, <outlook addr>
- Desk posts as: <DESK_NAME> (<icon>) · bot ID <Uxxxx>
- Timezone: <tz> (DESK_TZ_OFFSET_MIN=<n>)

## 2. Infrastructure map
- Notion workspace: <link> · Tasks DB: <link> · Ideas DB: <link> · Registers: <links>
- Slack workspace(s): <name(s)> · digest channel: <#channel Cxxxx> ·
  ideas channel: <#channel Cxxxx> · leadership routing (if any): <#channel>
- Drive filing root: <folder link> · restricted folder: <link>
- Otter account: <email>

## 3. Channel routing
Who gets addressed where (seniority routing, if it applies): <fill in>

## 4. Bootstrap for a fresh session
1. Clone this repo; env vars arrive from the cloud environment.
2. `bash scripts/setup_desk.sh` — every check PASS before real work.
3. Connectors are account-bound: verify Gmail/Outlook/Otter/Slack/Drive/Calendar are
   authorized on this account and enabled in-chat for connector legs.
4. Do NOT create or modify Routines unless the Principal asks — one-per-cadence.
5. SYNC CONTRACT — (a) first action of every session: `git pull --ff-only` when on
   main, or `git fetch && git rebase origin/main` on a session branch; (b) last action
   of every session that changed files: `bash scripts/sync_main.sh` — no PRs, no
   lingering session branches, main is the only branch that exists; (c) the maintainer
   pushes fixes to main from his own sessions — they reach this desk at the next pull,
   so long-running sessions should re-pull before acting on rules. 'Immediate' means
   next-pull, not hot-reload: a session that already loaded CLAUDE.md keeps its loaded
   copy until it pulls and re-reads.

## 5. Learnings
(Append operational learnings here as they are earned — with dates. Rules graduate to
CLAUDE.md only under its cap discipline, at three instances sharing a root cause.)
