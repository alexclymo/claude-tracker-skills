# D01 — Income imputation rule

*File type: **headed-append** — the `## Current ruling` head is rewritten whenever the ruling
changes; `## History` is appended, never edited. Same discipline as a task detail file.*

*One file per decision. This file answers "what is the current ruling and how did it get here"; the
ledger in `DECISIONS.md` carries only its one-line summary and provenance.*

## Current ruling
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

## History

*Appended at EOF when the ruling changes: `### YYYY-MM-DD — <what changed>`, stating the retired
ruling and why. Never edited once written — this is the frozen record of how the decision evolved.*

### 2026-07-19 — replaced forward-fill with backward-fill + validity flag

Was: forward-fill, no validity flag (set human 2026-06-01). Changed because forward-fill silently
carried stale income across gaps, which `T103` treated as real variation. The forward-fill runs are
dated in `T101`/`T103`'s progress logs and in `JOURNAL.md`, which remain the record of what actually
executed at the time.
