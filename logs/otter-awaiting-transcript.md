# Otter recordings with no transcript yet — retry list

Deliberately NOT marked in the ledger, so each daily sweep re-checks them.
Otter is known to produce transcripts late and to re-cut recordings, so an
empty fetch is not proof the content is lost.

| id | title | start | duration | first seen empty | checks | last checked |
|---|---|---|---|---|---|---|
| 4NU9nZNGFTAP5nY_sul0Of4rsZs | HKM AI Dev | 2026-11-03 00:58 | 14m04s | 2026-11-05 | 4 | 2026-11-08 |
| pUqAYQL01tVqtO6cT2PpGfcupms | HKM AI Dev | 2026-11-04 00:58 | 12m04s | 2026-11-05 | 4 | 2026-11-08 |
| Dwx7wv1XCwd2inR0q8r-p2u-L9A | HKM AI Dev | 2026-11-05 00:59 | 10m02s | 2026-11-05 | 4 | 2026-11-08 |
| e7tRKdn4qMEKmNqC-zzIjqTDd3Y | HKM AI Dev | 2026-11-06 00:58 | 7m01s  | 2026-11-06 | 3 | 2026-11-08 |

Durations are UNCHANGED across all four checks, so these are not slow re-cuts
in progress — the recordings appear to have produced no text at all.

Pattern worth noting: every one is the daily "HKM AI Dev" standup at ~00:58,
and they got shorter each day (14m, 12m, 10m, 7m). No other meeting on this
account has failed this way. The last readable HKM AI Dev was 29 Oct.

**New on 2026-11-08: there is no HKM AI Dev recording at all for 7 Nov.** The
series ran daily from 3 Nov to 6 Nov producing progressively shorter, empty
recordings, and then stopped. That is consistent with the bot being removed
from the calendar invite or the standup no longer being held — not with a
transcription backlog.

Rule: if a recording is still empty after 5 checks, mark it SKIPPED in the
ledger with note "no transcript produced by Otter after 5 checks" and drop it
from this file. Never report these as a clean zero (rule 5) — they were
recorded, they are simply unreadable. The first three reach 5 checks on the
9 Nov sweep.
