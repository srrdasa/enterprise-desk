# Otter recordings with no transcript yet — retry list

Deliberately NOT marked in the ledger, so each daily sweep re-checks them.
Otter produces transcripts late and re-cuts recordings, so an empty fetch is
not proof the content is lost.

| id | title | start | duration | first seen empty | checks | last checked |
|---|---|---|---|---|---|---|
| Zhb1D9ur05RVv-CtNqw00B_7arI | HKM AI Dev | 2026-11-09 00:58 | 11m56s | 2026-11-09 | 2 | 2026-11-10 |

Rule: if a recording is still empty after 5 checks, mark it SKIPPED in the
ledger with note "no transcript produced by Otter after 5 checks" and drop it
from this file. Never report these as a clean zero (rule 5) — they were
recorded, they are simply unreadable.

## The HKM AI Dev gap — closed on 10 November

| date | duration | transcript |
|---|---|---|
| 29 Oct | — | readable (last good one before the gap) |
| 3 Nov | 14m04s | none — SKIPPED 9 Nov |
| 4 Nov | 12m04s | none — SKIPPED 9 Nov |
| 5 Nov | 10m02s | none — SKIPPED 9 Nov |
| 6 Nov | 7m01s  | none — SKIPPED 10 Nov |
| 7 Nov | — | no recording |
| 8 Nov | — | no recording |
| 9 Nov | 11m56s | none — still retrying |
| 10 Nov | 1h58m | **readable, with summary and action items** |

Transcription recovered on 10 Nov on its own. Five standups (3–6 and 9 Nov)
produced a duration and no text and are almost certainly unrecoverable through
the API; only opening them in the Otter UI would show whether the audio exists.

Worth keeping in mind: the 10 Nov recording shows the CRM schema still being
settled, which suggests the lost standups covered the same ground rather than
decisions that were taken and moved past. That is a guess, not evidence.
