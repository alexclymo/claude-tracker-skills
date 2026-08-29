# PRIORITIES

*File type: **overwrite-only** — rewritten in place. Correct claims where they stand; never stack a correction above one.*

*Last updated: 2026-07-19*

The pointer: what to do now. Read this after `INDEX.md` and the `DECISIONS.md` ledger.

## Rules

- Every bullet below is ≤30 words and must link to a `D##`, a detail file, or a task ID.
- File cap: ~2,000 words total. Over cap means demote, not add (I5) — move detail to the relevant
  detail file, or a session out of the window below and into `JOURNAL.md`.
- Exactly two kinds of section exist in this file: this Rules block plus the three sections below —
  `Notes for next session`, `Next priorities`, `Recent sessions`. A third kind of section is a bug —
  fix the file, don't add one.
- **`Recent sessions` is a fixed-size window of at most 5 entries that is rewritten, not a list
  that is appended to.** When a sixth session lands, the oldest entry moves to `JOURNAL.md` in the
  same operation that adds the new one. This is the only way this file is ever written — not a
  cleanup step someone remembers to do later.

## Notes for next session

- The sparse-income subgroup surfaced in `T103` (`detail/T103_build_regression_dataset.md`) needs a
  call before `T201` can start — decide whether it forces a schema change.
- `D01` is a Claude-set ruling not yet ratified — confirm the backward-fill switch before relying on
  it in the writeup.

## Next priorities

- Finish `T103`: resolve the sparse-income subgroup, then finalise the estimation dataset.
- Once `T103` closes, start `T201`'s pooled and FE specifications — remember `D02`'s ≥3-wave sample
  applies to the FE spec only.

## Recent sessions

- **2026-07-19** — Revised `D01` to backward-fill + validity flag; rejoined the new flags into
  `T103`'s dataset. See `detail/D01_imputation_rule.md`.
- **2026-07-12** — Assembled the `T103` estimation dataset against `T102`'s schema; the sparse-income
  subgroup surfaced as an open item.
- **2026-06-28** — Ruled `D02` (≥3-wave sample restriction, scoped to the FE spec).
- **2026-06-15** — Completed and reviewed `T101`/`T102`; both parties signed off.
- **2026-06-01** — Ruled `D01` (originally forward-fill); later revised in place.
