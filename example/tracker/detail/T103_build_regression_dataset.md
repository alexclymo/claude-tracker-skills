# T103 — Build regression dataset

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

## Current state
*Refreshed: 2026-09-10*

Status: `in-progress`. Assembling the estimation dataset from `T102`'s validated panel: constructing
the outcome (job satisfaction), the key regressor (commute time), and controls, and attaching
the imputation validity flags from `T101`. Two extracts are built — a full-sample extract for the
pooled baseline and a restricted extract for the fixed-effects spec, which applies the ≥3-wave
restriction in this file's Notes.
Open: a sparse-income subgroup (respondents missing income in >40% of their waves) is unstable under
the current construction — see the 2026-07-12 log entry.

## Goal

Produce the analysis dataset `T201`'s baseline regression consumes: one row per respondent-wave with
the outcome, commute time, controls, and `T101`'s imputation validity flags.

## Sub-steps

- Select modelled variables from `T102`'s validated panel.
- Construct derived controls (age band, log income, hours, industry).
- Attach `T101`'s imputation validity flags.
- Build the FE-spec extract under the ≥3-wave restriction (Notes); leave the pooled extract
  unrestricted.
- Write the dataset and a manifest recording the source-panel hash and the code revision.

## Acceptance criteria

- No unexpected nulls in the modelled columns.
- The manifest records the input panel hash and the code revision that built the dataset.
- Both the pooled and FE-spec extracts build end-to-end.

## Stopping criteria

- **Success:** both extracts pass the acceptance criteria and `T201` can consume the dataset without
  modification.
- **Bailout:** if the sparse-income subgroup requires a schema change, stop and report rather than
  patching around it in this step.
- **Wall-clock cap:** 2 hours of unsupervised work before checking in.

## Notes

**≥3-wave sample restriction** `[spec: fixed-effects]` (set and ratified by the human 2026-06-28;
folded in from the retired decisions ledger 2026-09-10): restrict the fixed-effects estimation sample
to respondents observed in at least three waves. Binds the FE specification only — the pooled
baseline (`T201`) uses the full sample. Applied here when building the FE-spec extract. Alternatives
considered: ≥2 waves (too few for a stable within estimator); a fully balanced panel (discards too
many respondents and risks selection on attrition). Full text in `ARCHIVE.md` under
`### Decisions (format v2, retired 2026-09-10)`.

## Progress log

### 2026-07-12 — Assembled dataset against T102 schema; sparse-income subgroup surfaced

Built the respondent-wave dataset with outcome, commute, and controls, and attached the validity
flags. Found that respondents missing income in >40% of their waves behave unpredictably under the
current construction — recorded as the open item in Current state rather than worked around here.

### 2026-07-19 — Rejoined validity flags after D01 revision

`D01` moved to backward-fill + flag; rejoined the new flags into both extracts. The sparse-income
subgroup is still open.
