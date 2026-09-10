# T101 — Ingest survey panel data

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

## Current state
*Refreshed: 2026-09-10*

Status: `done`, reviewed by both parties. Loaded the raw NHPS extract (waves 2010–2022) into a tidy
long-format panel, one row per respondent-wave. Missing income is imputed in this step; the current
rule (formerly ruling `D01`, now folded into Notes below) is backward-fill with a validity flag —
the earlier forward-fill run is preserved in the log below, not overwritten.

## Goal

Turn the raw NHPS extract into a single tidy long-format panel ready for cleaning and schema
validation (`T102`).

## Sub-steps

- Locate and parse the raw NHPS extract.
- Reshape to long format (one row per respondent-wave).
- Impute missing income per the rule in Notes, attaching a validity flag to every imputed cell.
- Write the long panel and reconcile row counts against the codebook.

## Acceptance criteria

- Row counts reconcile with the NHPS codebook.
- Every imputed income cell carries a validity flag distinguishing it from an observed value.

## Stopping criteria

## Notes

The imputation pass lives in this step. When the rule was revised on 2026-07-19, this step's pass
changed with it — the head above reflects the current rule; the log records what actually ran, and
when.

**D01 folded in from the retired decisions ledger** (2026-09-10): backward-fill missing income,
carrying an explicit validity flag on every imputed cell, applied in this ingest step before the
panel is cleaned; the flag propagates into `T103`'s estimation dataset so each specification can
distinguish imputed income from observed income. Set by claude 2026-07-19, not yet human-ratified —
confirm before relying on it in the writeup. Alternatives considered: forward-fill (the original
rule, set human 2026-06-01, replaced because it silently carried stale income across gaps that
`T103` then treated as real variation) and mean-fill (discarded the panel's temporal structure).
Full text preserved in `ARCHIVE.md` under `### Decisions (format v2, retired 2026-09-10)`.

## Progress log

### 2026-06-10 — Initial ingest with forward-fill imputation

Loaded waves 2010–2022 and reshaped to long format. Imputed missing income by forward-fill — the
`D01` ruling in force at the time. Row counts reconciled against the codebook.

### 2026-07-19 — Re-ran imputation as backward-fill + validity flag per revised D01

`D01` was revised (forward-fill → backward-fill + flag). Re-ran only the imputation pass; the rest
of the ingest was unchanged. Re-reviewed and signed off.
