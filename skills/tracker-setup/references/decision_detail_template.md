# D01 — Imputation recipe

*File type: **headed-append** — the `## Current ruling` head is rewritten whenever the ruling
changes; `## History` is appended, never edited. Same discipline as a task detail file.*

*One file per decision. This file answers "what is the current ruling and how did it get here"; the
ledger in `DECISIONS.md` carries only its one-line summary and provenance.*

## Current ruling
*Set by: claude 2026-07-19 · Ratified: —*

Backward-fill missing sensor readings, carrying an explicit validity flag on every imputed cell,
applied uniformly across channels before feature extraction.

**Mechanism.** Implemented in the ingest step (`T101`) as a single pass per channel; the validity
flag propagates into the feature matrix so `T103` can distinguish imputed from observed values.

**Scope.** All channels, all datasets. No scope tag — one dataset regime so far.

**Alternatives considered.** Forward-fill (the original ruling, see History) masked sensor dropouts
as real readings; mean-fill discarded temporal structure. Backward-fill + flag keeps the gap
visible downstream.

## History

*Appended at EOF when the ruling changes: `### YYYY-MM-DD — <what changed>`, stating the retired
ruling and why. Never edited once written — this is the frozen record of how the decision evolved.*

### 2026-07-19 — replaced forward-fill with backward-fill + validity flag

Was: forward-fill, no validity flag (set human 2026-06-02). Changed because forward-fill silently
carried the last good reading across dropouts, which `T103` then treated as real signal. Reproduced
runs that used forward-fill are dated in `T101`/`T103` progress logs and `JOURNAL.md`, which remain
the record of what was actually executed at the time.
