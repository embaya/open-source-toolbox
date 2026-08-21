# GitHub metadata overlay

`github.jsonl` is generated metadata keyed by the curated `repository` field. It is intentionally separate from `catalog/*.jsonl` so automated refreshes cannot overwrite human/AI curation.

## Fields

Typical fields include GitHub language, license, topics, Stars, forks, issues, archive/disabled state, push/update timestamps, latest release, maintenance status and two heuristic navigation scores.

## Maintenance status

- `ACTIVE` — pushed within 90 days
- `SLOW` — pushed within 365 days
- `STALE` — pushed within 730 days
- `DORMANT` — no push for more than 730 days
- `ARCHIVED` / `DISABLED` — GitHub repository state
- `MISSING` — GitHub returned 404
- `INACCESSIBLE` — metadata refresh could not read the repository
- `UNKNOWN` — insufficient timestamps

## Scores

`activity_score` and `maturity_score` are deterministic **heuristics for navigation and comparison only**. They are not security reviews, quality certifications or production-readiness scores. They never alter curated priority A/B/C automatically.
