# ARCHIVE

*File type: **append-only** — entries appended at end of file. Never rewritten.*

Never loaded at session start. Exists so that closing a phase in `INDEX.md` never means destroying
the record — the phase's full task table moves here, verbatim, leaving only a one-line pointer
behind in `INDEX.md`.

Entries: `### Phase N — <name> (closed YYYY-MM-DD)`, each holding the closed phase's complete task
table exactly as it last read in `INDEX.md`.

### Phase 0 — Project setup (closed 2026-05-30)

| ID | Task | Status | Depends | R:Human | R:Claude | Category |
|-----|------|--------|---------|---------|----------|----------|
| T001 | Set up repo and analysis environment | done | — | ok | ok | code |
| T002 | Secure NHPS data access and codebook | done | T001 | ok | ok | data |

### Decisions (format v2, retired 2026-09-10)

The `DECISIONS.md` ledger and its two decision files, copied verbatim when this tracker moved to
format 3. `D01`'s ruling now lives in `detail/T101_ingest_survey_data.md`'s Notes and `D02`'s in
`detail/T103_build_regression_dataset.md`'s Notes.

| ID | Ruling (one line) | Scope | Set by | Ratified |
|-----|-------------------|-------|--------|----------|
| D01 | Backward-fill income imputation with a validity flag | — | claude 2026-07-19 | — |
| D02 | Restrict estimation sample to respondents in ≥3 waves | [spec: fixed-effects] | human 2026-06-28 | human 2026-06-28 |

#### D01 — Income imputation rule

*File type: **headed-append** — the `## Current ruling` head is rewritten whenever the ruling
changes; `## History` is appended, never edited. Same discipline as a task detail file.*

*One file per decision. This file answers "what is the current ruling and how did it get here"; the
ledger in `DECISIONS.md` carries only its one-line summary and provenance.*

##### Current ruling
*Set by: claude 2026-07-19 · Ratified: —*

Backward-fill missing income, carrying an explicit validity flag on every imputed cell, applied in
the ingest step before the panel is cleaned.

**Mechanism.** Implemented in `T101` as a single per-respondent pass; the validity flag propagates
into `T103`'s estimation dataset so each specification can distinguish imputed income from observed
income.

**Scope.** All respondents, the single NHPS panel. No scope tag — one dataset regime so far.

**Alternatives considered.** Forward-fill (the original ruling, see History) carried the last
observed income across gaps, which `T103` then treated as real signal; mean-fill discarded the
panel's temporal structure. Backward-fill + flag keeps the gap visible downstream.

##### History

*Appended at EOF when the ruling changes: `### YYYY-MM-DD — <what changed>`, stating the retired
ruling and why. Never edited once written — this is the frozen record of how the decision evolved.*

###### 2026-07-19 — replaced forward-fill with backward-fill + validity flag

Was: forward-fill, no validity flag (set human 2026-06-01). Changed because forward-fill silently
carried stale income across gaps, which `T103` treated as real variation. The forward-fill runs are
dated in `T101`/`T103`'s progress logs and in `JOURNAL.md`, which remain the record of what actually
executed at the time.

#### D02 — Estimation sample restriction

*File type: **headed-append** — the `## Current ruling` head is rewritten whenever the ruling
changes; `## History` is appended, never edited. Same discipline as a task detail file.*

*One file per decision. This file answers "what is the current ruling and how did it get here"; the
ledger in `DECISIONS.md` carries only its one-line summary and provenance.*

##### Current ruling
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

##### History
