# Changelog

Notable changes to this repo, newest first. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) loosely — an entry per release, with changes
grouped under **Added** / **Changed** / **Fixed** / **Removed**.

**Versions here are tracker format versions, not a release count.** The number in a heading is the
`tracker-format` value that release scaffolds and expects, so the first public release is **v2** —
there is no public v1. Format 1 was the informal version of this system I used on my own projects
before the skills existed; it was never published. A release that changes the format bumps the
number; releases that don't get a dated sub-entry under the current one, numbered `3.1`, `3.2`, ….
Since 3.5 that number is also the `tracker-format` stamp, which the skills compare to catch a stale
install. The current version is **3.5**.

## v3 — 2026-09-10

Two months of daily use said the system worked but had become expensive to run. v3 cuts the
ceremony: a quiet close, a smaller audit, no decisions ledger, and rules that live in the skills so
fixes reach existing trackers.

### 3.5 — 2026-11-16 — version check

- **Added:** the `tracker-format` stamp now carries the release, `3.N`, so the skills can tell a
  stale install from a project that needs updating. `tracker-close` compares its own version with
  the project's after its work and adds one line: reinstall the skills, or run `tracker-audit`. It
  never changes the stamp. `tracker-audit` first reads the latest release's stamp from this repo on
  GitHub; if the installed skills are older than that or than the project, it stops before writing
  and says to update and reinstall. Offline, it says so and carries on. When the project is older,
  audit's existing block regeneration brings it up to date and sets the stamp.
- **Migrating:** nothing by hand. A project's bare `3` reads as 3.0; the next `tracker-audit`
  regenerates the block, which sets `3.5`. Reinstall the skills on every machine once: earlier
  skills have no check, so they cannot warn you.

### 3.4 — 2026-11-13 — unpushed commits no longer stop the same machine

- **Changed:** C's session-start check stopped whenever local commits were unpushed, so a session
  that committed without pushing stopped the next one on the *same* machine. It now stops only
  when HEAD and the remote have diverged. Unpushed commits are kept, and the clean-tree check still
  catches the other machine, where those commits arrive as uncommitted edits.
- **Migrating:** replace a C project's `Git layout` line by hand with the new reminder.

### 3.3 — 2026-11-13 — several machines via a remote

- **Layout C now works, and is recommended for several machines.** Its setup step for a second
  machine failed: the synced `.git` pointer named the first machine's path. C now uses a relative
  pointer, so usernames may differ, and builds each other machine's database by cloning the remote.
  Its `CLAUDE.md` reminder carries a session-start check: fetch, stop on unpushed commits, align
  with the remote, stop unless the synced files match it. Close says plainly when anything is left
  unpushed.
- **Fixed:** `git_layouts.md` said gitignored files do not travel under C. They do; the working
  folder syncs.
- **Migrating:** a project already recorded as layout C keeps its old reminder, since audit never
  regenerates `## Project settings`. Replace that line by hand with C's new reminder from
  `git_layouts.md`.

### 3.2 — 2026-11-13 — existing repos in a sync folder

- **`tracker-setup` now warns about an existing repo in a cloud-sync folder.** Before, the
  git-layout question was asked only when setup created the repo itself, so the commonest case, an
  existing project in Dropbox or iCloud, never saw the warning. Setup still changes nothing in git:
  it asks, records a layout and its reminder, and for a one-machine project with `.git` inside the
  sync folder suggests moving the database out by hand.

### 3.1 — 2026-10-15 — private repos only

- **The system now says plainly that it is for private repos**, or ones shared only with close
  collaborators, and advises a new repo for any public production work. A new README section and a
  `DESIGN.md` section give the reasoning.
- **`tracker-setup` settles repo visibility once**, reading it from GitHub where it can, warns
  plainly, and records `Repo visibility` in `## Project settings`. A public repo is offered three
  paths: make it private, keep `tracker/` out of git, or don't use the tracker.
- **`tracker-close` pushes only a repo recorded as private**, on any layout — fixing layout A, where
  a one-machine project's remote went stale though it is the history's only off-machine copy. On
  GitHub it checks visibility before pushing. `tracker-audit` follows the same rule.
- Projects set up earlier are asked the visibility question once, by whichever of close or audit
  first needs it. No format change: Project settings sit outside the tracker block.

### Added

- `references/checks.md` — the handful of commands the skills measure with, replacing
  `mechanical_checks.md`.
- `references/git_layouts.md` — the cloud-sync git-layout options, moved out of `tracker-setup`
  and read only when a sync folder is detected.

### Changed

- **`tracker-close`** now writes state and stops: statuses for tasks worked, progress-log entries
  with refreshed heads, PRIORITIES, a commit. Three checks on the files it touched, silent on pass.
  At most eight lines of output, the last of which is what to pick up next session. It mentions
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
- **What a project carries shrank.** The INDEX header is 99 words (was 450), the PRIORITIES header
  52 (was 156), the CLAUDE.md block 455 (was 534), all counted with their title and file-type lines.
  The rules for maintaining the files live in the skills and are read at runtime, so a fix
  propagates without touching existing trackers.
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
yes. Progress logs are left as written; an open task's other sections have any `D##` citation
re-pointed.

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
