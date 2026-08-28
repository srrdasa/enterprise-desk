# Operations Manual — MKCD Desk

## 1. Identity
- Principal: **Mukunda Dasa** — runs the **HKGT DMT** (Hare Krishna Golden Temple
  Digital Marketing Team). Slack ID: env `PRINCIPAL_SLACK_ID` — his HUMAN member ID
  (Slack profile → ⋮ → Copy member ID), NEVER the bot's own ID. Verified 2026-08-28
  via Slack users.info: resolves to "Mukunda Dasa" (human, workspace owner) and
  differs from the bot's own user ID. ClickUp ID: `100877577` (workspace member
  fetch 2026-08-28, email match mkcd@hkmhyderabad.org). Mailboxes: `[[unverified:
  Gmail/Outlook addresses pending from the Principal]]`.
- **The organisation's name is exactly "HKGT DMT" or the full name above — no other
  abbreviation, ever.** A four-letter form starting with the same letters that names
  a DIFFERENT organisation appeared in an early draft; the contamination grep
  (README of the build) hard-fails on it, so it is never written anywhere in this
  repo, including here.
- Desk posts as: **MKCD Desk** (env DESK_NAME) · bot user `U0BTF7PP4MP`
  (DESK_BOT_ID) · bot app `B0BTBC3MUB0`. Signs: **"Hare Krishna — MKCD Desk"**.
- Timezone: IST (DESK_TZ_OFFSET_MIN=330).
- The maintainer (external to HKGT DMT) builds and fixes the desk and pushes to
  `main`; he appears in NO drafts, NO org structure, NO outputs. Principal decisions
  and approvals flow through him.

## 2. Infrastructure map
- ClickUp: Tasks list `901616685481` · Ideas list `901616685482`
  (docs/CLICKUP-SCHEMA.md). Both live in workspace **"Hare Krishna Movement"**
  (team `90161377214`) — a second workspace ("Hem Chand Tunga HGT Workspace") is
  visible to the token but is NOT the desk's; org/task fetches scope to the first.
  Required custom fields not yet created on either list — `python3
  scripts/clickup.py missing` prints the exact set (ClickUp UI only; the API
  cannot create fields).
- Whimsical workspace "DMT" (connector): org chart —
  https://whimsical.com/7M4QFiT2MCLRaZG8HT6eBC. **This board is the SOURCE OF TRUTH
  for org structure** as of 2026-08-28 — the Principal edits it directly, and it is
  the only surface that carries reporting lines. docs/ORG-STRUCTURE.md, the Notion
  page and boards/mindmaps/*.md are all generated FROM it on his word. Do NOT
  regenerate the board from the repo (that direction was reversed on 2026-08-28) —
  read it back with the Whimsical connector instead.
- Notion (Principal's own workspace, "Mukunda Charana Dasa's Space", reached via his
  **Notion connector** — a different auth path from the registers integration token):
  Org Structure READ-ONLY mirror —
  https://app.notion.com/p/3ca81bf463b48175b6b9cf9138a06a84 (it was the editing
  surface until 2026-08-28; the Whimsical board replaced it). Regenerated from the
  board; edits made on the page are overwritten. `scripts/notion.py` (integration
  token) CANNOT see it, so no automated leg may depend on it.
- Organisational knowledge base: docs/ORG-KNOWLEDGE.md — what the org does, its
  verticals, digital estate, tooling, doctrine and stated constraints, extracted from
  the 2026-08-27 "Departmental Structure Overview" Otter transcript. Reference only,
  never live state. Derived objectives (DRAFT, unactioned) —
  https://app.notion.com/p/3ca81bf463b481d1a4e8f6a7c4eb6d87
- Notion registers parent ("MKCD Desk Registers"): **PENDING** — env pair not set;
  setup is §0 of docs/NOTION-REGISTERS.md (the Principal's 5 minutes). Record the
  four register page links here the day they exist.
- Slack workspace: hkgtdmt.slack.com · welcome/announcements: **#all-hkgt-dmt**
  `C0BLXK2R279` — CONFIRMED by the Principal 2026-08-28 (no #team-announcements
  exists; this is the workspace-wide default channel). Desk bot joined and posted
  the welcome message there as "MKCD Desk"
  (`https://hkgtdmt.slack.com/archives/C0BLXK2R279/p1787939569077109`).
  · digest channel + ideas channel:
  `[[unverified: to be confirmed by the Principal]]`. Other public channels:
  #social `C0BM9L2ETS9`, #new-channel `C0BMEU22DKK` (bot is a member of both).
- Drive filing root / restricted folder: `[[unverified: pending]]`.
- Otter account: the Principal's (connector-bound, his Claude account).
- NO Atlassian/Confluence anywhere in this desk — any reference, env var, check or
  connector expecting one is leftover contamination to REMOVE, not satisfy.

## 3. Channel routing
ClickUp = tasks & ideas; Slack = discussion; registers = Notion. Person-wise routing:
`[[unverified: to be filled from ORG-STRUCTURE.md once confirmed]]`.

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

## 5. Learnings & standing gates
STANDING GATES (active from 2026-08-28; each is relaxed ONLY by the Principal — the
desk never decides it has earned trust; relaxations are recorded here with a date):
1. **Meeting-task approval gate** — first two weeks of /meeting: the full proposed
   batch is approved row-by-row before anything is created (see /meeting).
2. **Evernote calibration gate** — first triage batch is exactly 100 notes; the
   Principal corrects the taxonomy before any bulk run (see /evernote-triage).

(Append operational learnings here as they are earned — with dates. Rules graduate to
CLAUDE.md only under its cap discipline, at three instances sharing a root cause.)
