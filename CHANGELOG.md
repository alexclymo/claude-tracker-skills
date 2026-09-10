# Changelog

Notable changes to this repo, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely — an entry per release, with changes
grouped under **Added** / **Changed** / **Fixed** / **Removed**.

**Versions here are tracker format versions, not a release count.** The number in a heading is the
`tracker-format` value that release scaffolds and expects, so the first public release is **v2** —
there is no public v1. Format 1 was the informal version of this system I used on my own projects
before the skills existed; it was never published. A release that changes the format bumps the
number; releases that don't get a dated sub-entry under the current one. The current format is
**v3**.

## v3 — 2026-09-10

Two months of daily use said the system worked but had become expensive to run. v3 cuts the
ceremony: a quiet close, a smaller audit, no decisions ledger, and rules that live in the skills so
fixes reach existing trackers.

### Changed

- **`tracker-close`** now writes state and stops: statuses for tasks worked, progress-log entries
  with refreshed heads, PRIORITIES, a commit. Two checks on the files it touched, silent on pass. At
  most eight lines of output, the last of which is what to pick up next session. It mentions
  `tracker-audit` only when it saw a concrete contradiction it may not fix — never because a file is
  long.
- **`tracker-audit`** is human-run only and reads what agents actually load: INDEX, PRIORITIES, the
  CLAUDE.md block, and the detail files of open tasks. Closed tasks and code comments only on a deep
  run. At most ten findings, ranked by what an agent would get wrong, split into *Wrong* and *Long*,
  then a walkthrough in blocks of five questions. It also offers the v2 → v3 migration and
  regenerates the state-file headers and the CLAUDE.md block when they drift from canonical. A
  declared retirement is swept here, on the human's yes — the job `tracker-supersede` used to do.
- **Thresholds** are more generous: no per-cell or header-prose checks; INDEX suggests archiving
  above 10,000 words (was 5,000); an open task's detail file is flagged only above 15,000 words (was
  3,000 / 5,000); closed tasks are never measured.
- **What a project carries shrank.** The INDEX header is ~90 words (was 450), the PRIORITIES header
  ~35 (was 156), the CLAUDE.md block ~450 (was 534). The rules for maintaining the files live in the
  skills and are read at runtime, so a fix propagates without touching existing trackers.
- **The nine numbered invariants** became one principle — what an agent reads at session start must
  be currently true, and short enough to be read — and eleven one-line rules. The numbering only ever
  served cross-references between skills.
- Skills locate `tracker-setup/references/` relative to their own directory, so a project-local
  install works.

### Removed

- **`DECISIONS.md` and `detail/D##_*.md`.** A decision made while working a task is now a note in
  that task's detail file; a rule for the whole project is a line in `CLAUDE.md`. The migration
  copies a project's existing decisions verbatim into `ARCHIVE.md` and deletes the files.
- **`tracker-supersede`.** Never used in practice; its sweep now lives in `tracker-audit`'s apply
  step.
- `references/invariants.md`, `references/mechanical_checks.md` (replaced by `checks.md`), and the
  two decision templates.

### Migration

Run `tracker-audit` in a v2 project. It shows the plan, archives the decisions, replaces the two
state-file headers and the CLAUDE.md block, stamps `tracker-format: 3`, and commits — only on your
yes. Task detail files are not touched.

## v2 — 2026-07-21

First public release: the four `tracker-*` skills and the `tracker/` system they scaffold.

### Added

- **`tracker-setup`** — run once per project. Checks for a git repo (and asks how to lay it out if the
  project lives in a cloud-sync folder), scaffolds `tracker/` from templates, writes the standing-rules
  block into `CLAUDE.md`, and populates an initial task list from the project's code, git history, and
  TODOs.
- **`tracker-close`** — run at session end. Confirms or demotes in-progress tasks, writes session state
  into `tracker/`, checks its own edits against the invariants and the mechanical size/consistency
  checks, and commits `tracker/` separately from code.
- **`tracker-audit`** — the periodic deep sweep. Searches the whole repo for claims that no longer
  match reality, ranks them by how likely each is to cause a wrong agent decision, and fixes them only
  on explicit approval.
- **`tracker-supersede`** — run on a declared pivot. Requires both halves named — what is retired and
  what replaces it — then sweeps every place the retired thing appears, marking it dead rather than
  deleting it.
- **Tracker format 2** — `INDEX.md`, `PRIORITIES.md`, `DECISIONS.md`, `JOURNAL.md`, `ARCHIVE.md`, and
  one `detail/` file per task and per decision. Every file declares its write mode on its own third
  line — `overwrite-only`, `append-only`, or `headed-append` — and every skill writes it only that way.
- **`example/`** — a worked example: a fake academic project carrying a fully populated tracker, so you
  can see what the system looks like in use before running it on anything of your own.
- **[`DESIGN.md`](DESIGN.md)** — the reasoning: how notes rot, the three write modes, and the nine
  invariants that hold the system together.
