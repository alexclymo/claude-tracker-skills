# DECISIONS

*File type: **overwrite-only** — the ledger below is rewritten in place. Correct rows where they
stand; never stack a correction above one. Each decision's rationale lives in its own
`detail/D##_*.md` file, not here.*

The ledger: one row per decision, the current ruling in one line. This file is read every session;
open a decision's `detail/D##_*.md` only when its ruling is relevant.

## Conventions

- **One row per decision, one `detail/D##_*.md` file per decision** — the row count must equal the
  number of `detail/D*.md` files (mechanical check 3). `D` IDs are numbered like tasks and never
  reused.
- **The row shows the *current* ruling.** Decisions are revised in place in their detail file (new
  ruling on top, retired ruling demoted to that file's `## History`), so a row never points forward
  to a superseding entry — there is no `★ superseded → D##` chain to follow. The row always reads as
  current truth.
- **`Set by`** — `claude <YYYY-MM-DD>` or `human <YYYY-MM-DD>`: who authored the current ruling and
  when. Rewritten whenever the ruling is revised.
- **`Ratified`** — `human <YYYY-MM-DD>` once the human has confirmed the current ruling; `—`
  otherwise. A human-set ruling is self-ratified (same date). A row with `Ratified = —` is a
  Claude-set ruling the human has not yet endorsed — `tracker-close` surfaces these at session end.
- **Scope tags (I4).** Once a second model, dataset, or approach exists, a ruling that isn't
  universal carries a `[tag]` in the Scope cell and a matching `★ SCOPE` note in its detail file.
- **Archive when long.** When the ledger passes ~40 rows or ~1,500 words, *suggest* moving rows for
  closed/retired phases to `ARCHIVE.md` (their detail files stay). A suggestion, not a hard stop.

<!-- BEGIN ledger -->
| ID | Ruling (one line) | Scope | Set by | Ratified |
|-----|-------------------|-------|--------|----------|
| D01 | Backward-fill imputation with an explicit validity flag | — | claude 2026-07-19 | — |
| D02 | Cap feature-extraction batch size at 256 | [model-B only] | human 2026-06-20 | human 2026-06-20 |
| D03 | Pipeline recipe: ingest, validate, impute, extract | — | claude 2026-07-05 | human 2026-07-06 |
<!-- END ledger -->
