# Otter recordings with no transcript yet — retry list

Deliberately NOT marked in the ledger, so each daily sweep re-checks them.
Otter produces transcripts late and re-cuts recordings, so an empty fetch is
not proof the content is lost.

| id | title | start | duration | first seen empty | checks | last checked |
|---|---|---|---|---|---|---|
| Zhb1D9ur05RVv-CtNqw00B_7arI | HKM AI Dev | 2026-11-09 00:58 | 11m56s | 2026-11-09 | 4 | 2026-11-12 |

Rule: if a recording is still empty after 5 checks, mark it SKIPPED in the
ledger with note "no transcript produced by Otter after 5 checks" and drop it
from this file. Never report these as a clean zero (rule 5) — they were
recorded, they are simply unreadable. This one reaches 5 checks on the 13 Nov sweep.

## The HKM AI Dev gap — closed on 10 November

| date | duration | transcript |
|---|---|---|
| 29 Oct | — | readable (last good one before the gap) |
| 3 Nov | 14m04s | none — SKIPPED |
| 4 Nov | 12m04s | none — SKIPPED |
| 5 Nov | 10m02s | none — SKIPPED |
| 6 Nov | 7m01s  | none — SKIPPED |
| 7–8 Nov | — | no recording |
| 9 Nov | 11m56s | none — still retrying |
| 10 Nov | 1h58m | readable |
| 11 Nov | 55m34s | readable |

Transcription recovered on 10 Nov on its own and has held for two days.
Five standups (3–6 and 9 Nov) produced a duration and no text; only opening
them in the Otter UI would show whether the audio exists at all.
