# INDEX

*File type: **overwrite-only** — rewritten in place. Correct claims where they stand; never stack a correction above one.*

What exists and what state it's in. What to do next is `PRIORITIES.md`.

Status: `done` · `in-progress` · `ready` · `blocked` · `proposed` · `abandoned` (kept, never
deleted). `R:Human` / `R:Claude`: `ok` once that party reviewed the row; review never gates `done`.
IDs number by phase (`T1xx`, `T2xx`), never reused. Task names ≤50 characters; detail belongs in
the detail file. ≤10 path-forward bullets of ≤30 words, each naming a task. Closed phases move to
`ARCHIVE.md`. Rules: the `tracker-*` skills.

## The path forward

- Data pipeline is nearly done: `T103` is the last step before Phase 2. See
  `detail/T103_feature_extraction.md`.
- The batch cap in `T103` applies to model B only; model A runs unbatched. See that file's Notes.
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
