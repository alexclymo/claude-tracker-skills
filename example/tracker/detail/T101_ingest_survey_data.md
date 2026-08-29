# T101 — Ingest survey panel data

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

*One detail file per task. If this log starts covering more than one task ID, the task has become
an umbrella — split it into one file per child rather than letting this one grow to cover all of
them. Size: `tracker-close` warns at ~3,000 words and flags for splitting at ~5,000.*

## Current state
*Refreshed: 2026-07-19*

Status: `done`, reviewed by both parties. Loaded the raw NHPS extract (waves 2010–2022) into a tidy
long-format panel, one row per respondent-wave. Missing income is imputed in this step; the current
rule is `D01`'s backward-fill with a validity flag — the earlier forward-fill run is preserved in
the log below, not overwritten.

## Goal

Turn the raw NHPS extract into a single tidy long-format panel ready for cleaning and schema
validation (`T102`).

## Sub-steps

- Locate and parse the raw NHPS extract.
- Reshape to long format (one row per respondent-wave).
- Impute missing income per `D01`, attaching a validity flag to every imputed cell.
- Write the long panel and reconcile row counts against the codebook.

## Acceptance criteria

- Row counts reconcile with the NHPS codebook.
- Every imputed income cell carries a validity flag distinguishing it from an observed value.

## Stopping criteria

## Notes

`D01`'s imputation pass lives in this step. When `D01` was revised on 2026-07-19, this step's pass
changed with it — the head above reflects the current rule; the log records what actually ran, and
when.

## Progress log

### 2026-06-10 — Initial ingest with forward-fill imputation

Loaded waves 2010–2022 and reshaped to long format. Imputed missing income by forward-fill — the
`D01` ruling in force at the time. Row counts reconciled against the codebook.

### 2026-07-19 — Re-ran imputation as backward-fill + validity flag per revised D01

`D01` was revised (forward-fill → backward-fill + flag). Re-ran only the imputation pass; the rest
of the ingest was unchanged. Re-reviewed and signed off.
