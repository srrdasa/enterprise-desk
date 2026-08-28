# Enterprise Desk — a portable Claude Code operations process

An executive desk that runs on Claude Code: daily communications sweeps (Slack, Gmail,
Outlook, Otter meetings), a Notion task tracker with hygiene checks that don't let
items rot, an idea pipeline with scoring and a monthly review cadence, drafted-never-
auto-sent replies, and a voice log that measures itself honestly.

Generalized from a production desk. Every binding rule in CLAUDE.md exists because its
absence cost that desk a real message, a stale list, or a silently dead pipeline.

## Quick start (~1 hour)
1. **Repo** — push this to a PRIVATE GitHub repo of your own.
2. **Notion** — create the integration + two databases per `docs/NOTION-SCHEMA.md`.
   Share both with the integration (page-level permissions — the #1 setup failure).
3. **Slack** — create a bot app per `docs/SECRETS-SETUP.md`, install, invite it to
   the channels it should sweep.
4. **Identity** — fill in `docs/OPERATIONS.md` §1–3.
5. **Cloud environment** — claude.ai/code → Cloud environments → new env on this
   repo: add the env vars (SECRETS-SETUP) and paste `scripts/environment_setup.sh`
   as the Setup script.
6. **Connectors** — authorize Gmail, Outlook, Otter, Slack, Google Drive, Google
   Calendar on the Claude account that will run the desk.
7. **Verify** — open a session on the repo, run `bash scripts/setup_desk.sh`, get
   all PASS.
8. **Routines** — create ONE daily + ONE weekly Routine (claude.ai/code → Routines)
   pointing at this repo + environment, connectors ticked, prompts from
   `routines/*.md`. Test-fire before accepting. One-per-cadence is a hard invariant.
9. **First session** — paste the SESSION PROMPT from the bottom of CLAUDE.md.

## Daily life
You read the digest; you approve or edit drafts; you answer the desk's questions.
The desk sweeps, files, tracks, chases, and reports — with counts, every time, so a
silent failure is impossible by design. Monthly you sit `/idea-review` for 30 minutes:
promote / park / merge / kill. The cadence is the deliverable, not the database.

## Layout
CLAUDE.md — binding rules (capped file; read it) · routines/ — the two loop prompts ·
.claude/commands/ — /desk /pending /idea-intake /idea-review /meeting ·
scripts/ — Notion/Slack helpers, audits, sweeps, board renderer ·
docs/ — schema, secrets, ops manual, voice · boards/ — generated idea board ·
logs/ — the edits log (the desk's only objective quality score).
