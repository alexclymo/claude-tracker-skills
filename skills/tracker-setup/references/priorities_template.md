# PRIORITIES

*File type: **overwrite-only** — rewritten in place. Correct claims where they stand; never stack a correction above one.*

*Last updated: 2026-07-15*

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

- Sparse-channel gap surfaced in `T103` (`detail/T103_feature_extraction.md`) needs a decision
  before `T201` can start.

## Next priorities

- Close out `T103`'s sparse-channel handling, then start `T104`'s unit tests.
- Once `T104` is done, start `T201` per `D03`'s pipeline recipe.

## Recent sessions

- **2026-07-14** — Applied `D02`'s batch cap; found the sparse-channel gap in `T103`. See
  `detail/T103_feature_extraction.md`.
- **2026-07-10** — Scaffolded the feature extractor against `T102`'s validated schema.
- **2026-06-20** — Ruled on `D02` (batch-size scope) after model B's extractor was added.
- **2026-06-18** — Completed and reviewed `T101`/`T102`.
- **2026-06-02** — Ruled on `D01` (imputation recipe); later revised in place.

---

**Day-one initial state.** When `tracker-setup` scaffolds a brand-new project, paste this in place
of the three sections above — there is no session history yet:

```
## Notes for next session

- Nothing yet — this is the first session. Populate INDEX.md's Phase 1 before writing notes here.

## Next priorities

- Confirm the initial task list in INDEX.md looks right, then start the first ready task.

## Recent sessions

- (empty — the first session's summary lands here at the next close.)
```
