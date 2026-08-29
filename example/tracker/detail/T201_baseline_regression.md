# T201 — Estimate baseline regression

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

*One detail file per task. If this log starts covering more than one task ID, the task has become
an umbrella — split it into one file per child rather than letting this one grow to cover all of
them. Size: `tracker-close` warns at ~3,000 words and flags for splitting at ~5,000.*

## Current state
*Refreshed: 2026-07-12*

Status: `blocked` on `T103`. Plan: pooled OLS of job satisfaction on commute time with controls,
standard errors clustered by individual; a fixed-effects specification as a robustness check, run on
`D02`'s ≥3-wave restricted sample. Cannot start until `T103`'s estimation dataset is final — in
particular until the sparse-income subgroup is resolved.

## Goal

Estimate the baseline association between commuting time and job satisfaction, with a fixed-effects
specification as a robustness check, and export the results for the paper (`T202`).

## Sub-steps

- Load `T103`'s finished dataset.
- Estimate the pooled OLS baseline with controls.
- Estimate the FE spec on `D02`'s ≥3-wave sample.
- Tabulate both specs and export a results file `tex/main.tex` can import.

## Acceptance criteria

- A coefficient table covering both specifications.
- Standard errors clustered by individual.
- Results exported in a form `T202`'s paper can consume without hand-editing.

## Stopping criteria

## Notes

The FE spec is where `D02`'s scope tag `[spec: fixed-effects]` applies — the pooled baseline uses the
full sample.

## Progress log
