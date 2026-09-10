# T201 — Estimate baseline regression

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

## Current state
*Refreshed: 2026-09-10*

Status: `blocked` on `T103`. Plan: pooled OLS of job satisfaction on commute time with controls,
standard errors clustered by individual; a fixed-effects specification as a robustness check, run on
the ≥3-wave restricted sample (`T103`'s Notes). Cannot start until `T103`'s estimation dataset is final — in
particular until the sparse-income subgroup is resolved.

## Goal

Estimate the baseline association between commuting time and job satisfaction, with a fixed-effects
specification as a robustness check, and export the results for the paper (`T202`).

## Sub-steps

- Load `T103`'s finished dataset.
- Estimate the pooled OLS baseline with controls.
- Estimate the FE spec on the ≥3-wave sample (`T103`'s Notes).
- Tabulate both specs and export a results file `tex/main.tex` can import.

## Acceptance criteria

- A coefficient table covering both specifications.
- Standard errors clustered by individual.
- Results exported in a form `T202`'s paper can consume without hand-editing.

## Stopping criteria

## Notes

The FE spec is where the ≥3-wave restriction's scope tag `[spec: fixed-effects]` applies — the pooled baseline uses the
full sample.

## Progress log
