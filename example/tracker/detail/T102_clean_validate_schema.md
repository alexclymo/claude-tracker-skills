# T102 — Clean and validate schema

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

*One detail file per task. If this log starts covering more than one task ID, the task has become
an umbrella — split it into one file per child rather than letting this one grow to cover all of
them. Size: `tracker-close` warns at ~3,000 words and flags for splitting at ~5,000.*

## Current state
*Refreshed: 2026-06-15*

Status: `done`, reviewed by both parties. Cleaned the long panel from `T101` and validated it
against a documented schema: types coerced, out-of-range values caught, wave coverage checked. A
schema manifest is written alongside the cleaned panel and feeds `T103`.

## Goal

Produce a validated, analysis-ready panel — correct types, no out-of-range values, a documented
schema — from `T101`'s ingested data.

## Sub-steps

- Coerce column types to the schema.
- Range-check key fields (job satisfaction in `[0, 10]`, commute time `≥ 0`).
- Drop or quarantine malformed rows rather than silently repairing them.
- Emit a schema manifest describing the validated panel.

## Acceptance criteria

- Schema validation passes with zero errors.
- A schema manifest is written and records the field types and ranges enforced.

## Stopping criteria

## Notes

Feeds `T103`, which selects modelled variables from this validated panel.

## Progress log

### 2026-06-15 — Cleaning and schema validation complete; reviewed by both parties

Coerced types, applied range checks, quarantined a small number of malformed rows, and wrote the
schema manifest. Both parties reviewed and signed off.
