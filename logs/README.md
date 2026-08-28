# logs/edits.jsonl — the desk's only objective quality score

Every draft that goes out gets a line: draft, final, edit_ratio — logged via
scripts/edit_log.py, honestly. An unedited send counts (ratio 0.0). No self-scoring
anywhere: a model rating its own output produces a number that looks rigorous and
measures nothing. The diff is objective, free, and already here.

Weekly, the verification routine prints summary() into the report. When a correction
pattern hits three instances sharing a root cause, it graduates to a durable rule in
docs/VOICE-AND-PREFERENCES.md — one incident is noise (CLAUDE.md rule 10).

This directory starts empty on purpose. If you later build a golden eval set for
CLAUDE.md cap-cuts (recommended once the file nears its cap), put it in evals/.
