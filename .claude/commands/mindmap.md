# /mindmap — visual mind map / diagram from desk data

**Usage:** `/mindmap <subject> [--whimsical]`
Examples: `/mindmap org-structure` · `/mindmap project HKGT-Janmashtami` ·
`/mindmap idea-dependencies --whimsical`

## 1. GATHER — pull the real data, never invent structure
- `org-structure` → read docs/ORG-STRUCTURE.md: departments → HODs → managers →
  employees. **CONFIRMED rows only.** If the file header does not say CONFIRMED,
  print `org file is DRAFT — confirm it first (see docs/ORG-STRUCTURE.md)` and STOP;
  a drafted hierarchy rendered as a diagram reads as settled fact (same gate as
  /meeting).
- `project <name>` → ClickUp tasks/subtasks + assignees + dependencies via
  `scripts/clickup.py`: nodes = tasks, edges = dependencies, leaves = owners.
- `idea-dependencies` → the Ideas list: ideas as nodes; relates-to / merge /
  promoted-to links as edges (the idea board's data, in mindmap form).
- `<free subject>` → build from the named transcript/notes, resolving every name
  against the Contacts register and the live roster (rule 12 — speaker labels are
  not identity).

Every node traces to a source. An owner the data does not resolve is rendered
UNPLACED, never guessed.

## 2. RENDER (always) — Mermaid into the repo
Write a `mindmap` block (`flowchart` for dependencies) to
`boards/mindmaps/<subject>-<YYYY-MM-DD>.md`, first line
`<!-- GENERATED — never hand-edit -->`. GitHub-renderable syntax only: no HTML in
node text, quote any label containing punctuation, keep IDs alphanumeric. This layer
is free and always runs — report the path so it is viewable in GitHub immediately.
Commit via `bash scripts/sync_main.sh` (rule 14).

## 3. MIRROR — only with `--whimsical`
Pass the SAME Mermaid markup to Whimsical's create_diagram; return the board URL and
the in-chat preview. The Whimsical connector is installed on this org but ships
**disabled in chat** — enable it in the session's connector settings, or the tools
will not be loaded. If it is off, out of credits, or errors: say so plainly in one
line, skip this step, and note the Mermaid file already stands as the deliverable.
Never fail the command over the mirror.

## 4. REPORT
Path of the committed Mermaid file · Whimsical URL if mirrored · node and edge counts
· every UNPLACED node listed for the Principal to resolve. Loud zero (rule 5): if the
source held nothing, print `0 nodes — verify source` and emit NO file — an empty
diagram is worse than none.
