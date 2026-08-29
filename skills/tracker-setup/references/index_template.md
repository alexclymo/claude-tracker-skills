# INDEX

*File type: **overwrite-only** — rewritten in place. Correct claims where they stand; never stack a correction above one.*

The map: what exists and what state it's in. **Not** what to do next — that's `PRIORITIES.md`.

## Conventions

- **Status** — `done` (work finished; review is tracked separately in the `R:*` columns and does not
  gate this) · `in-progress` (active, reconfirmed at every close) · `ready` (unblocked, not started) ·
  `blocked` (waiting on a dependency) · `proposed` (not yet committed to) · `abandoned` (will not be
  done — kept for history, never deleted).
- **Review columns `R:Human` / `R:Claude`** — `ok` once that party has reviewed this row and
  confirmed it is accurate; `—` otherwise. **Review never gates `done`**: a task is `done` when its
  work is finished; whether anyone has reviewed it is a separate fact, tracked here, and reviewing is
  a separate job.
- **ID numbering is by phase** — `T0xx` for Phase 0, `T1xx` for Phase 1, `T2xx` for Phase 2, and so
  on. IDs are never reused, including for abandoned tasks.
- **The `Task` column is the task name only, ≤50 characters.** A longer explanation belongs in the
  detail file's `## Goal`; session narrative belongs in the detail file's Progress log. Evidence and
  artifact paths belong in `DECISIONS.md` or the detail file. The reasoning behind a ruling belongs
  in `DECISIONS.md` too, but as the ruling's rationale, not as evidence. If you're tempted to widen
  this cell, move the content to one of those instead.
- **Traceability to git comes from commit messages that cite the task ID** — e.g.
  `git log --grep="T103"` finds every commit touching that task — not from a column in this table.
- **A closed phase moves to `ARCHIVE.md`,** leaving a one-line pointer where its table used to be
  (e.g. `Phase 0: Environment setup — closed 2026-05-30, see ARCHIVE.md`). Without this, this file
  grows without bound. When `INDEX.md` passes ~5,000 total words, that is the signal to do this — a
  suggestion, not a failure; a legitimately large all-active project may have nothing to archive and
  carries on.
- **An umbrella task does not carry a hand-maintained status.** Derive a parent's status from its
  children (e.g. `done` once every child is `done`); a status set on the parent independently of
  them will drift out of sync with what they actually say.
- **The word cap is on *prose*, not the tables.** Table rows grow with the task list and stay
  skimmable one row at a time; only the non-table prose (this header, Conventions, "The path
  forward", inter-table notes) is capped — at ~800 words. If prose creeps past it, demote detail to
  a decision or detail file; do not trim task rows to hit a number.
- **Exactly three kinds of section exist in this file: this header, "The path forward," and the
  phase tables. A fourth kind of section is a bug — fix the file, don't add one.**

## The path forward

*Reconciled against the tables below at every close (`tracker-close` duty 2). Each bullet ≤30 words
and must point at a `D##`, a detail file, or a task ID — a bullet naming nothing is already
drifting.*

- Data pipeline follows the recipe fixed in `D03`; `T103` is the last step before Phase 2 begins.
- Feature-extraction batch cap (`D02`, `[model-B only]`) doesn't apply to model A — see
  `detail/T103_feature_extraction.md`.
- Phase 2 baseline (`T201`) starts once `T103` closes.

## Phase 1: Data pipeline

| ID | Task | Status | Depends | R:Human | R:Claude | Category |
|-----|------|--------|---------|---------|----------|----------|
| T101 | Ingest raw survey data | done | — | ok | ok | code |
| T102 | Clean and validate schema | done | T101 | ok | ok | code |
| T103 | Build feature extraction | in-progress | T102 | — | ok | code |

## Phase 2: Model training

| ID | Task | Status | Depends | R:Human | R:Claude | Category |
|-----|------|--------|---------|---------|----------|----------|
| T201 | Baseline regression model | proposed | T103 | — | — | analysis |
| T202 | Hyperparameter sweep design | blocked | T201 | — | — | analysis |
| T203 | Draft results memo | proposed | T202 | — | — | writing |
