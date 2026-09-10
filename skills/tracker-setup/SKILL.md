---
name: tracker-setup
description: Use when the user wants to set up the task system, set up a tracker, or initialise task tracking in a project — triggers like "set up the task system here", "set up a tracker for this project", "initialise task tracking". Checks for git (and asks how to lay it out if the project lives in a cloud-sync folder), scaffolds a tracker/ directory of task documents from templates, writes a short standing-rules block into CLAUDE.md, and seeds the task list from the project's code, git history, and TODOs. Manages project task *documents* on disk, not Claude Code's in-session task tools (TaskCreate/TaskList), which never persist.
---

# tracker-setup

One-time scaffold, run once at the project root. It creates `tracker/`, writes the standing-rules
block into `CLAUDE.md`, and seeds the task list from what the project already contains. Templates
and references are in `references/` beside this file. If the project already has a tracker, this
skill refuses and hands off (step 0).

## 0. Existing tracker?

- `tracker/` exists: stop, say so, and suggest the user run `tracker-audit`.
- `tasks/` exists and `tracker/` does not: stop. Say the project uses the old `tasks/` layout,
  which these skills do not support and which is migrated by hand. Scaffold nothing.
- Otherwise continue.

## 1. Git

Run `git rev-parse --is-inside-work-tree` at the project root.

**No repo yet.** Take `<project-name>` as the basename of the project's absolute path. If that path
contains `Dropbox`, `iCloud`, `OneDrive`, or `Google Drive`, read `references/git_layouts.md` and
follow it: it has the user choose a layout (A–D) and tells you what to run and which one-line
reminder to record for step 4. Otherwise run `git init -b main`. In either case, if there is no
`.gitignore`, write one — this is a text-and-code system, nothing it produces needs a binary in
git — covering at least: data and model artifacts (`*.csv`, `*.parquet`, `*.h5`, `*.hdf5`, `*.pkl`,
`*.npy`, `*.npz`, `*.pt`, `*.pth`, `*.ckpt`, `*.onnx`), archives (`*.zip`, `*.tar`, `*.tar.gz`,
`*.7z`), media (`*.mp4`, `*.mov`, `*.mp3`, `*.wav`), and environment clutter (`__pycache__/`,
`*.pyc`, `.venv/`, `venv/`, `node_modules/`, `.DS_Store`, `*.log`, `.vscode/`, `.idea/`). Stage
nothing yet. Mention once that you can set up a private remote if wanted; do not block on an answer.

**Repo exists.** Touch nothing in git. Write the same `.gitignore` if the project has none.

## 2. Scan for tasks

Before writing anything, find what the project is already doing:

- `git log --oneline` (skip if there are no commits yet) — what is done.
- `git branch -a`, and `git log main..<branch> --oneline` for each other branch — in-flight or
  proposed work.
- `grep -rn 'TODO\|XXX\|FIXME'` over source files git tracks or would track, plus stubbed or
  obviously incomplete files — what is in flight.
- The dependency order between these — what unblocks what.

Each finding becomes one INDEX row (`ID | Task | Status | Depends | R:Human | R:Claude | Category`,
name ≤50 characters) and one detail file. Anything aspirational but unstarted is `proposed`, not
`ready`. Number `T1xx` unless the scan clearly shows distinct phases. Phase names like "Data
pipeline / Model estimation / Writeup" (research) or "Scaffolding / Core feature / Release"
(software) are examples to offer, not defaults — say so, and let the user confirm or correct.

## 3. Scaffold

Create `tracker/` and `tracker/detail/`. Write `INDEX.md`, `PRIORITIES.md`, `JOURNAL.md` and
`ARCHIVE.md` from their templates in `references/`, plus one `detail/T###_<slug>.md` per task from
step 2 from `detail_template.md`. Each template shows the shape with a worked example. For the four
state files, carry the header — everything above the first project-content section or entry —
verbatim, and replace every example row, bullet, and entry with this project's content, or leave
the section empty where there is nothing yet.

- `INDEX.md`: header verbatim; `## The path forward` and one phase table per phase from step 2. A
  new project has one phase table.
- `PRIORITIES.md`: header verbatim, with today's date; then the template's **day-one** block, but
  name the first unblocked task by ID in `Next priorities` (whatever status INDEX gives it) instead
  of the generic phrase.
- `JOURNAL.md`, `ARCHIVE.md`: header only, no entries.
- `detail/T###_<slug>.md`: title line `# T### — <task name>`, the file-type line verbatim, then all
  seven sections; `## Current state` opens with today's `*Refreshed:*` date and one line of real
  status; `## Stopping criteria` and `## Progress log` left empty — stopping criteria are written
  when autonomy is granted, and nothing has happened yet.

## 4. CLAUDE.md

Ask two things, then write.

**Code changes on close** — how `tracker-close` treats code at session end: `auto` (commit code as
a second, separate commit; the default if no preference), `ask` (ask each time), or `never`.
`tracker/` is always committed separately from code; this only decides whether code is committed
too.

**Working relationship** (optional) — offer, don't push, a ≤80-word note, never a persona and never
a claim of expertise. Fillable default:

> You are helping with an academic research project in <domain>. Work as a collaborator, not an
> assistant: say when you are unsure, flag reasoning you think is wrong rather than going along with
> it, and ask before acting on an ambiguous instruction. The user's domain judgment in <areas> is
> better than yours — defer there and check rather than assume. Escalate anything that changes the
> project's direction.

Then read `references/claude_md_block.md` and write two things, in order: its block — from the line
starting `<!-- BEGIN tracker` through `<!-- END tracker -->`, verbatim — and, **after** the END
marker, that file's `## Project settings` stub with its placeholders replaced by this project's
answers: the git layout letter and its reminder (omit this bullet if no layout was chosen in step
1), the code-commit preference, and the working-relationship note (omit if skipped).

- No `CLAUDE.md`: create it with exactly those two parts.
- `CLAUDE.md` exists and no line starts with `<!-- BEGIN tracker`: append both parts after a blank
  line.
- A line already starts with `<!-- BEGIN tracker`: stop and suggest `tracker-audit`; never write
  a second block.

Locate `## Project settings` by that heading, never by "whatever follows END" — the file may carry
the user's own sections there. If the heading exists, write into it; otherwise insert it directly
after `<!-- END tracker -->`, leaving everything else untouched.

## 5. Commit

Layout D (no git): skip this step; say once that `tracker/` and `CLAUDE.md` exist on disk but are
not under version control. Otherwise stage only what this skill created:

```bash
git add tracker/ CLAUDE.md          # plus .gitignore, if step 1 wrote it
git diff --cached --stat
```

The stat should show four `tracker/*.md` files, the detail files you wrote, `CLAUDE.md` and possibly
`.gitignore`, a few tens of KB in total. If anything else is staged, stop and investigate. Then:

```bash
git commit -m "Set up tracker/: scaffold task system"
```

This is the only commit this skill makes. The project's own code stays as git left it.

## What this leaves behind

`tracker/` is now the project's source of truth, and the `CLAUDE.md` block puts its rules in
context every session without anyone invoking anything. Everything else is invoked, not standing:
`tracker-close` at the end of each session, `tracker-audit` when the human asks for it. Neither
runs itself.
