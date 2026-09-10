# INDEX

*File type: **overwrite-only** — rewritten in place. Correct claims where they stand; never stack a correction above one.*

What exists and what state it's in. What to do next is `PRIORITIES.md`.

Status: `done` · `in-progress` · `ready` · `blocked` · `proposed` · `abandoned` (kept, never
deleted). `R:Human` / `R:Claude`: `ok` once that party reviewed the row; review never gates `done`.
IDs number by phase (`T1xx`, `T2xx`), never reused. Task names ≤50 characters; detail belongs in
the detail file. ≤10 path-forward bullets of ≤30 words, each naming a task. Closed phases move to
`ARCHIVE.md`. Rules: the `tracker-*` skills.

## The path forward

- Phase 1 assembles the regression dataset (`T103`) using the backward-fill imputation rule folded
  into `T101`'s Notes; it's the last step before analysis begins.
- The ≥3-wave sample restriction folded into `T103`'s Notes (scope `[spec: fixed-effects]`) binds
  the planned FE robustness check, not the pooled baseline (`T201`).
- Baseline estimation (`T201`) is blocked on `T103`; the paper draft (`T202`) follows it.

## Phase 0: Project setup

Closed 2026-05-30 — full task table in `ARCHIVE.md`.

## Phase 1: Data pipeline

| ID | Task | Status | Depends | R:Human | R:Claude | Category |
|-----|------|--------|---------|---------|----------|----------|
| T101 | Ingest survey panel data | done | — | ok | ok | code |
| T102 | Clean and validate schema | done | T101 | ok | ok | code |
| T103 | Build regression dataset | in-progress | T102 | — | ok | code |

## Phase 2: Analysis and writeup

| ID | Task | Status | Depends | R:Human | R:Claude | Category |
|-----|------|--------|---------|---------|----------|----------|
| T201 | Estimate baseline regression | blocked | T103 | — | — | analysis |
| T202 | Draft paper | proposed | T201 | — | — | writing |
