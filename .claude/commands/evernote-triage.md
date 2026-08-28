# /evernote-triage — classify the Evernote archive without building a graveyard

**Usage:** `/evernote-triage` (next batch) · `/evernote-triage <notebook>` (one notebook)

**Premise:** ~6,000 notes. EXPECT most to be REFERENCE or OBSOLETE — a mass dump of
6,000 "tasks" is exactly the write-only-graveyard failure this desk exists to prevent.
The deliverable is an organized archive plus a SHORT list of genuinely live actions.

**Prerequisites (hard):**
1. Notes converted: `python3 scripts/enex_to_md.py evernote/raw/*.enex` (the
   Principal's manual step feeds evernote/raw/: Evernote → each notebook → Export →
   .enex → into a session or Drive).
2. docs/ORG-STRUCTURE.md header says **CONFIRMED** — classification is against real
   departments and people, never guessed ones.

**BINDING CALIBRATION GATE: the first batch is exactly 100 notes.** The Principal
reviews that batch's classifications and corrects the taxonomy BEFORE any bulk run.
Bulk proceeds only after his sign-off, recorded in docs/OPERATIONS.md §5.
After calibration, batches of 150–200.

## Per note — classify into ALL of:
- **department** (from ORG-STRUCTURE.md) · **project** (recurring topics become the
  project list — propose, don't invent silently) · **person** (Contacts-resolved)
- **class:** ACTION (live, someone must still do something) · REFERENCE (worth
  keeping, nothing to do) · OBSOLETE (superseded/expired — MARKED, never deleted)

## Routing
- **ACTION** → a PROPOSED task row (title · owner per the /meeting assignment rules ·
  due only if the note states one · Source = the note's INDEX path). Rows go through
  the SAME approval gate as meeting batches — nothing files without the Principal's
  row-by-row pass. Stale "actions" from years back default to OBSOLETE with one line
  of reasoning unless clearly still live.
- **REFERENCE** → proposed slot in the Notion knowledge structure (under the
  registers parent, one page per department/project). Registers layer PENDING →
  record the proposed structure in the triage log and carry a TODO.
- **OBSOLETE** → marked in the triage log with a one-line reason. Never deleted.

## The triage log (committed; content stays out of git)
Append one line per note to `evernote/TRIAGE.md`:
`| INDEX path | class | department | project | person | one-line reason |`
Every batch ends loud: `EVERNOTE triage: N processed (A action · R reference ·
O obsolete), N proposed tasks awaiting approval, N remaining` — zeros printed, never
skipped (rule 5).
