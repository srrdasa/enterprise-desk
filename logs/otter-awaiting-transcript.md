# Otter recordings with no transcript yet — retry list

Deliberately NOT marked in the ledger, so each daily sweep re-checks them.
Otter produces transcripts late and re-cuts recordings, so an empty fetch is
not proof the content is lost.

**The list is currently empty.** Every recording in the 3–9 Nov gap has now
reached 5 checks and been retired to the ledger as SKIPPED.

Rule: if a recording is still empty after 5 checks, mark it SKIPPED in the
ledger with note "no transcript produced by Otter after 5 checks" and drop it
from this file. Never report these as a clean zero (rule 5) — they were
recorded, they are simply unreadable.

## The HKM AI Dev gap — opened 3 Nov, closed 10 Nov

| date | duration | transcript |
|---|---|---|
| 29 Oct | — | readable (last good one before the gap) |
| 3 Nov | 14m04s | none — SKIPPED |
| 4 Nov | 12m04s | none — SKIPPED |
| 5 Nov | 10m02s | none — SKIPPED |
| 6 Nov | 7m01s  | none — SKIPPED |
| 7–8 Nov | — | no recording |
| 9 Nov | 11m56s | none — SKIPPED 13 Nov |
| 10 Nov onward | — | readable every day |

Five standups produced a duration and no text and are not recoverable through
the API. Transcription recovered on its own on 10 Nov and has held since.
