# Otter recordings with no transcript yet — retry list

Deliberately NOT marked in the ledger, so each daily sweep re-checks them.
Otter is known to produce transcripts late and to re-cut recordings, so an
empty fetch is not proof the content is lost.

| id | title | start | duration | first seen empty | checks | last checked |
|---|---|---|---|---|---|---|
| e7tRKdn4qMEKmNqC-zzIjqTDd3Y | HKM AI Dev | 2026-11-06 00:58 | 7m01s  | 2026-11-06 | 4 | 2026-11-09 |
| Zhb1D9ur05RVv-CtNqw00B_7arI | HKM AI Dev | 2026-11-09 00:58 | 11m56s | 2026-11-09 | 1 | 2026-11-09 |

Rule: if a recording is still empty after 5 checks, mark it SKIPPED in the
ledger with note "no transcript produced by Otter after 5 checks" and drop it
from this file. Never report these as a clean zero (rule 5) — they were
recorded, they are simply unreadable.

## Retired to the ledger as SKIPPED on 2026-11-09

The 3, 4 and 5 Nov recordings reached 5 checks (2026-11-05 … 2026-11-09) with
the duration unchanged every single time, so they were never slow re-cuts in
progress. Marked SKIPPED. Their content is not recoverable through the Otter
API — only someone opening those recordings in the Otter UI can tell whether
the audio exists at all.

## The HKM AI Dev pattern — six recordings, zero text

| date | duration | transcript |
|---|---|---|
| 3 Nov | 14m04s | none |
| 4 Nov | 12m04s | none |
| 5 Nov | 10m02s | none |
| 6 Nov | 7m01s  | none |
| 7 Nov | — | **no recording at all** |
| 8 Nov | — | **no recording at all** |
| 9 Nov | 11m56s | none |

The last readable HKM AI Dev was 29 Oct. Every recording since has produced a
duration and no text. The 7–8 Nov gap and the 9 Nov resumption at a longer
duration rule out the explanation that the standup simply stopped being held:
the meeting is still running and still being captured, and the transcription
is what is failing. No other meeting on this account fails this way.

That is eleven days of the CRM/AI standup with no readable record — the period
covering the 2 Nov CRM release and the data-governance dispute.
