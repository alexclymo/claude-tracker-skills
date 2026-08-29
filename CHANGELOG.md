# Changelog

Notable changes to this repo, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely — an entry per release, with changes
grouped under **Added** / **Changed** / **Fixed** / **Removed**.

**Versions here are tracker format versions, not a release count.** The number in a heading is the
`tracker-format` value that release scaffolds and expects, so the first public release is **v2** —
there is no public v1. Format 1 was the informal version of this system I used on my own projects
before the skills existed; it was never published. A release that changes the format bumps the
number; releases that don't get a dated sub-entry under the current one.

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
