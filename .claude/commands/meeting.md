# /meeting — process the meetings that just finished

**Usage:** `/meeting` (every transcript since last run) · `/meeting 2` (last N) ·
`/meeting <otter-id> ...` (specific).

Fetch the transcript(s) from Otter. **Run the four lenses as PARALLEL agents** — never
sequentially in the main context, and never let one lens's conclusion colour
another's reading; the value is four independent readings compared afterwards:
  1. DECISIONS — anything settled (record conflicts as both).
  2. OWED TO US — commitments others made, with who and when.
  3. OWED BY THE PRINCIPAL — his own commitments; the class that gets lost as
     background narrative. These become tracked items in the SAME turn, and anything
     with a time attached becomes a CALENDAR EVENT immediately (rule 2).
  4. IDEAS — long-horizon intent → /idea-intake, never a dated task.
Where a per-attendee view is wanted, one agent per PERSON.

Then consolidate: archive the verbatim transcript (Drive, link recorded in the tracker),
propose all updates for approval (rule 2 — never auto-applied), file approved items,
draft the summary post. Speaker labels are NOT identity — resolve every name against
the Contacts register before it enters a draft (rule 12). Numbers are extracted and
marked claimed-by-them until a system confirms (rule 9).

## ASSIGNMENT STEP — every action item gets an owner before it gets filed
Owner resolution, in strict order:
1. **Explicit name in the transcript wins** — resolved through the Contacts register
   (speaker labels are not identity; an unresolvable name is a red flag to raise,
   never a guess).
2. Otherwise **department-of-topic → that department's HOD**, flagged
   `by department inference` on the proposed row. Departments and HODs come ONLY
   from a docs/ORG-STRUCTURE.md whose header says **CONFIRMED** — a DRAFT org file
   means no inference: the row goes out owner-blank for the Principal to fill.
Due dates ONLY if the meeting stated one — never invented. Every task's Source field
carries the transcript link.

**Granularity:** a body of work assigned to a department is ONE parent task to its
HOD — decomposition is the HOD's call unless the meeting named people to pieces.
(Calibration: "25 campaigns for Sri Krishna Janmashtami with a deadline" = ONE parent
task to the Digital Marketing HOD with the deadline, not 25 tasks.)

## APPROVAL GATE — first two weeks (relaxed only by the Principal, never by the desk)
Nothing is created in ClickUp from a transcript until the FULL proposed batch — one
row per task: title · owner (+ inference flag) · due · priority · source — is
approved row-by-row. Corrections apply to the batch, then it files in the same turn.
Gate start date and any relaxation are recorded in docs/OPERATIONS.md §5.
