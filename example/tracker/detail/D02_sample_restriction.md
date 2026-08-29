# D02 — Estimation sample restriction

*File type: **headed-append** — the `## Current ruling` head is rewritten whenever the ruling
changes; `## History` is appended, never edited. Same discipline as a task detail file.*

*One file per decision. This file answers "what is the current ruling and how did it get here"; the
ledger in `DECISIONS.md` carries only its one-line summary and provenance.*

## Current ruling
*Set by: human 2026-06-28 · Ratified: human 2026-06-28*

★ SCOPE `[spec: fixed-effects]` — this ruling binds the fixed-effects specification only. The pooled
baseline (`T201`) uses the full sample and ignores it.

Restrict the fixed-effects estimation sample to respondents observed in at least three waves.

**Mechanism.** Applied in `T103` when building the FE-spec extract; the pooled extract is left
unrestricted. See `T103`'s sub-steps.

**Rationale.** The FE specification identifies from within-respondent variation, which needs several
observations per person. A ≥3-wave floor keeps the within estimator stable without trimming the
sample so hard that the estimates lose precision.

**Alternatives considered.** ≥2 waves (too few for a stable within estimator); a fully balanced
panel (discards too many respondents and risks selection on attrition).

## History
