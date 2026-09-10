# Design

This document explains how the tracker system is put together and why it is shaped the way it is —
what each file is for, how each is allowed to be written, and the rules that keep the whole thing
consistent. See [`README.md`](README.md) for what it does and how to install it; this is for whether
the design holds up.

## The core idea

A project's notes are asked to do two incompatible jobs at once: be the current state of the world,
and be a log of everything that has happened. A single markdown file can be read either way, but not
easily written both ways. Appending preserves history and is cheap under time pressure; overwriting
preserves accuracy and costs more attention per edit. Left undirected, a file drifts toward whichever
is cheaper, which is almost always appending. The state-as-of-now reading and the log reading start to
disagree, and nothing about the format makes disagreeing an error, so nobody catches it.

The system's answer is to stop asking any one file to do both. Each file is given a single job and a
single legal way of being written, and the rest of the design follows from that.

## The files

The whole system is a `tracker/` folder of markdown. Nothing here is a database or a tool — it is text
a human can read and an agent can load.

### `INDEX.md` — what exists and what state it's in

The map of the project. One table per phase, one row per task, plus a short "path forward" section at
the top. Deliberately *not* a list of what to do next; that is `PRIORITIES.md`'s job.

```markdown
## Phase 1: Data pipeline

| ID | Task | Status | Depends | R:Human | R:Claude | Category |
|-----|------|--------|---------|---------|----------|----------|
| T101 | Ingest raw survey data | done | — | ok | ok | code |
| T102 | Clean and validate schema | done | T101 | ok | ok | code |
| T103 | Build feature extraction | in-progress | T102 | — | ok | code |
```

Statuses run `done` · `in-progress` · `ready` · `blocked` · `proposed` · `abandoned`. Task IDs are
numbered by phase (`T1xx` for Phase 1) and never reused, including for abandoned work — a stable ID
means a commit message citing `T103` stays findable forever. The `Task` column stays a name, not a
sentence — the one thing that reliably destroys a table like this is one cell growing into a
paragraph — but that is a writing rule, not a check; the checks are on whole files.

### `PRIORITIES.md` — what to do next

The pointer, read straight after `INDEX.md`. Three sections and no more: notes for the next session,
the next priorities, and a window of recent sessions.

```markdown
## Next priorities

- Close out `T103`'s sparse-channel handling, then start `T104`'s unit tests.
- Once `T104` is done, start `T201` using the batching recipe noted in `detail/T103_*.md`.

## Recent sessions

- **2026-07-14** — Capped model-B batches at 256; found the sparse-channel gap in `T103`.
- **2026-07-10** — Scaffolded the feature extractor against `T102`'s validated schema.
```

Every bullet is capped at 30 words and has to point at a task ID or a detail file — a bullet naming
nothing is already drifting away from the thing it was describing. `Recent sessions` is a fixed
window of five: when a sixth lands, the oldest moves to `JOURNAL.md` in the same edit. It is a window
that gets rewritten, not a list that grows.

### `tracker/detail/T###_*.md` — one file per task

Where the actual work lives: goal, sub-steps, acceptance criteria, stopping criteria, notes, and a
dated progress log. The file opens with a `## Current state` block that is rewritten every time the log
below it grows.

```markdown
## Current state
*Refreshed: 2026-07-15*

Status: `in-progress`. Current approach: extract features batch-wise per the recipe in this file's
`## Notes`, using the schema validated in `T102`. Open: the extractor does not yet handle the
sparse-channel case surfaced in the 2026-07-14 session below.

## Progress log

### 2026-07-14 — Capped model-B batches at 256; surfaced sparse-channel gap

Applied the 256-row cap for model B. Found that channels with >40% missing values behave
unpredictably in the current recipe.
```

This pairing is the most important one in the system. The progress log is genuinely append-only and
allowed to grow — it is a record of what was believed and done at the time, and stays true as that.
But a long log with a summary at the top that nobody has refreshed is worse than no summary, because
the summary is the part a reader sees first. So the head and the body are written in one operation:
you may not grow the log without refreshing the state above it.

Decisions live here too. A choice made while working a task — which imputation rule, which sample
restriction — is a dated note in that task's `## Notes`, scope-tagged if it only holds for one model
or regime. v2 kept a separate decisions ledger with per-decision files and a ratification column; it
was retired in v3 because few decisions in a live project are final, agents filed facts there as
rulings, and the ledger cost more to keep honest than it returned. A rule that genuinely binds the
whole project is a line in `CLAUDE.md`, written with the human's say-so.

### `JOURNAL.md` and `ARCHIVE.md` — the overflow

Rolled-off session history and closed phases, respectively. Both are append-only, never loaded in
normal work, and never deleted. They exist so that `PRIORITIES.md` and `INDEX.md` can stay short
without anything being lost: material moves *out*, rather than being trimmed away.

## Three write modes

Every file above declares its write mode on its own third line, and every skill that touches it may
only write it that way:

- **overwrite-only** (`INDEX.md`, `PRIORITIES.md`) — rewritten in place. A correction replaces the
  claim where it stands; nothing is ever stacked above an older version. These files answer "what's
  true right now," so they can never accumulate a stale layer underneath a current one.
- **append-only** (`JOURNAL.md`, and a detail file's `## Progress log`) — entries added at end of
  file, never rewritten. These are narrative, not current-state claims, so nothing about them needs
  reconciling.
- **headed-append** (every `detail/T###_*.md` file) — a small current-state head paired with an
  appended body, both written in the same operation.

The point of typing files this way is not persuasion. It is that the rot becomes structurally
unreachable rather than merely against the rules. A correction stacked above a stale claim requires an
overwrite-only file to have been written append-style — so if every skill that opens `INDEX.md` only
ever rewrites it, that failure has no file left to happen in. The mode doesn't ban long files; it bans
one whose top no longer describes its bottom.

## The one job

The tracker has one job: what an agent reads at session start must be currently true, and short
enough to be read. Everything below serves that. v2 stated most of this ground as nine numbered
invariants; v3 rewords the rules, adds a few, and drops the numbers, which only ever served
cross-references between the skills. The canonical wording lives with the skills, in
[`claude_md_block.md`](skills/tracker-setup/references/claude_md_block.md), and is written into each
project's `CLAUDE.md` from there, so a fix reaches an existing tracker instead of stopping at the
copy it was scaffolded with. Each rule carries the failure that produced it.

**Correct in place.** A wrong claim is rewritten where it stands — never annotated below it, never
contradicted above it — and line 3 of every file names the one way that file may be written. On one
real project a detail file's head sat untouched for two dozen sessions, and when a later decision
retired the framing it described, nothing marked the reversal where the retired claim lived.

**Head before body.** A detail file's `## Current state` is rewritten every time its progress log
grows, in the same edit. Appending feels like updating, so nobody re-read that head; by the time
anyone looked it named a deleted function and prescribed an abandoned method. A long log under a
stale summary is worse than no summary, because the summary is what a reader sees first.

**One home per fact.** Status lives in `INDEX.md`, what-next in `PRIORITIES.md`, narrative in the
progress log; you point at a fact rather than restate it. The same project's `INDEX.md` had grown
paragraphs above its tables, each citing the very file its fact belonged in instead of living there.
Two homes, and nobody's job is to notice which one has gone stale.

**Short by construction.** `INDEX.md` rows are names, not sentences; `PRIORITIES.md` bullets are ≤30
words and name a task ID or a detail file; near a cap, move something out before adding. That
project ran the natural experiment for us: same rules, same authors, and the file-level word cap on
`PRIORITIES.md` held completely while the per-row limit on `INDEX.md` task names failed on most rows.

**Anchor by name.** Symbols, sections, function names; never `file:line`. That frozen head named a
function long after it had been deleted — a name at least stays greppable, so the staleness is
detectable; a line number would have pointed silently at whatever moved into its place.

**Say where it applies.** A fact true only of one model, dataset, or regime carries a tag saying so,
like `[model-B]`. The project ran several models side by side, and its largest task file — named for
one of them — had quietly swallowed work belonging to the others, each of which already had its own
row. A file whose edges are unmarked reads as universal, and inherits what isn't its own.

**Dead things say so.** A retired approach or task is marked dead at its home, with `★ SUPERSEDED by
<x> (date)` or status `abandoned` — never deleted, never left reading as current, and `★` is
licensed for nothing else. That same head was eventually wrong on every axis at once with nothing
signalling it, because the retirement had been recorded a level away, in the decisions ledger, and
nothing carried it outward. A retirement is an event with a sweep attached, not a quiet edit.

**Decisions live where they were made.** A choice made inside a task is a note in that task's detail
file; a rule binding the whole project is a line in `CLAUDE.md`, written with the human's say-so;
retiring something project-wide is the human's call, never an agent's inference.

**Stopping criteria before autonomy.** Success condition, bailout condition and a wall-clock cap go
into the detail file before a task is worked unsupervised — the cheapest moment to find out you
cannot state them.

**Do not restructure.** No sections added to state files, no formats converted mid-task: a tracker
whose format stamp is older than the skill running against it is read and finished as-is, with a
one-line note left in `PRIORITIES.md` for the human.

**Commit `tracker/` separately from code.** The two move at different speeds and get reverted for
different reasons; one commit holding both costs you the ability to undo either alone.

Short-by-construction is worth a note on why its caps are aggregates. A cap that asks for restraint
item by item tends not to hold, because each overrun looks small and locally justified at the moment
it is written; a cap checked as a single number at write time does hold. So the mechanical checks
([`checks.md`](skills/tracker-setup/references/checks.md)) are word counts over whole files, and the
per-item limits that survive — a task name that stays a name — are writing rules, never measured.

## How it gets used

Day to day you don't manage these files by hand. The standing rules in the generated `CLAUDE.md`
block, loaded every session, tell the agent when to read and write each one:

- **At session start**, the agent reads `INDEX.md` and `PRIORITIES.md` — what exists and what's next
  — then opens the `detail/T###_*.md` file for whatever task you're picking up.
- **During the session** you talk to the agent normally, no special commands. It keeps the current
  task's detail file up to date as the work moves.
- **At session end**, `tracker-close` writes the session's state back: it sets the status of every
  task the session worked, refreshes their heads, rolls the oldest `Recent sessions` note into
  `JOURNAL.md`, commits `tracker/` separately from any code, and says what to pick up next time.
- **Once per project**, `tracker-setup` scaffolds the folder and writes the `CLAUDE.md` block.
- **Now and then**, when the docs start to drift, *you* run `tracker-audit`: it reads what agents
  load, reports at most ten findings, and walks you through fixes five at a time. A retirement — one
  approach dead, another current — is something it asks about and sweeps on your yes; it never
  declares one.

None of the three skills run themselves; an agent has to invoke them. That is deliberate for
`tracker-close` above all — a skill that can block a session's end is one people learn to route
around, so it never refuses to close.

The agent makes and revises decisions on its own, noting each one where it was made — in the detail
file of the task it came up in, as the work moves. The one judgment that stays yours is declaring
something retired: guessing at that doesn't produce one bad line, it broadcasts a wrong marker
everywhere the sweep reaches, which is why the audit asks you and never infers.

## Notable design decisions

A few choices that shape the whole system, over and above the file-by-file rules above.

**Plain markdown, not a tool.** No database, no schema, no CLI — just text files a human reads
directly and an agent loads. At this scale a bespoke tool would cost more to build and maintain than
it saves, and markdown is already the medium both the human and the agent are fluent in. The
discipline lives in the write rules every skill follows, not in a storage layer that enforces them
mechanically.

**The agent drives; you talk in plain English.** There are no commands to memorize and no expectation
that you edit the files by hand. The standing rules make reading and updating the tracker part of
ordinary work, and even the three skills trigger on natural phrasing rather than a fixed syntax. It
should feel like working with a collaborator who keeps good notes, not like operating a bug tracker.

**Nothing is ever deleted.** Retired things get a banner, abandoned tasks keep their row and their
ID, closed phases move to `ARCHIVE.md`, and a project migrating from v2 keeps its old decisions
verbatim in `ARCHIVE.md`. Deleting is how a project loses the answer to "didn't we try that
already?" — the goal is that dead things stay readable while being unmistakably marked dead.

**Automation handles mechanism; the human handles meaning.** The skills do the mechanical work —
sweeping every file that names a thing, rolling old sessions into the journal, checking the word
caps — but stop short of judgments. `tracker-audit` reports what looks stale and changes nothing
until you say yes: whether a claim is *actually* stale, or whether two docs genuinely contradict, is a
reading rather than a measurement, and a skill that silently rewrites a corpus it just misread is
worse than no skill at all. The same line is why an agent can sweep a retirement but never declare one.

**Format is versioned, migrations are opt-in.** The generated `CLAUDE.md` block carries a
`tracker-format` stamp; each skill targets a version. A tracker older than the running skill is read
as-is — the skills stay backward-compatible — and a migration is *suggested* at session handoff, run
deliberately by the human through `tracker-audit`, never forced mid-task. A format change is an
event the human opts into, not a tax the tooling imposes. v3 also made the format cheaper to change:
the rules agents follow live in the skills and are read at runtime, and the few lines a project
carries — the `CLAUDE.md` block and the two state-file headers — are regenerated by `tracker-audit`.

## What v3 changed, and why

v2's close was slow and noisy: thirteen checks every session, then a snapshot report of every file's
size and every check's number — long enough that it went unread, which is the same as not having run
it. v3's close verifies only what it wrote itself, says nothing when that passes, and answers in a
handful of lines.

Audit fired too often and returned too much. Close recommended it almost every session, because "a
file is over a size threshold" was grounds for a recommendation and a 5,000-word detail file is
still 5,000 words the morning after an audit. The audit then swept the whole corpus with no cap on
findings, so a stale head in a closed task's file — which nobody will open again — arrived alongside
a stale head in tomorrow's. A list too long to act on gets half acted on, and close starts
recommending it again. v3 scopes audit to what agents actually load, caps the report at ten findings
ranked by what an agent would get wrong tomorrow, and walks through them five at a time.

The decisions ledger is gone, for the reason given in the detail-file section above: a dedicated
slot for rulings turned out to be a magnet, and the machinery around it cost more to keep honest
than it returned.

And the skills were rewritten for a stronger model. They had been written to persuade a fast,
careless reader: repetition, worked reasoning, every check spelled out and argued for. A
higher-effort model reads that differently — it executes an enumerated checklist literally and
exhaustively, and it fills whatever space it is given. So v3 states goals, boundaries and budgets
instead, and spends what is left on the rules that say *do not*.

## Git, and the cloud-sync caveat

The tracker leans on git, and `tracker-setup` will initialize a repo if the project doesn't already
have one. This is worth doing: because every session's work gets committed — `tracker/` separately
from code — you and the agent can both work more freely. A bad edit is one revert away, and the diff
of what changed is always there to inspect. The agent drives the mechanics, so it asks little git
fluency of you. Strongly recommended, though the system will run without it.

One setup needs care: a project that **already lives in a cloud-synced folder** (Dropbox, iCloud,
OneDrive) **and** that you want to work on from **more than one computer**. Git's object store is many
small files rewritten on every commit, and a sync client that writes one mid-commit can corrupt the
repo — silently, as far as the sync client is concerned; only git notices, and only later. The two
pressures pull apart: the clean fix is to move the real git directory *outside* the synced folder, but
that is exactly what stops the history travelling between machines the way the synced files do.

There is no perfectly clean answer, so `tracker-setup` doesn't pick one. It detects a cloud-synced
path, asks whether you work from one machine or several, and lays out four options with their
trade-offs: the git database *outside* the sync folder (one machine — recommended where it applies);
*inside* it (simplest for several machines, but it degrades as the repo grows); a separate database
plus a shared remote on every machine (holds up at size, but easy to get subtly wrong); or no git at
all (sync history is then the only history). Whichever you pick, the choice and a one-line reminder of
its pitfall are written into `CLAUDE.md`, so later sessions know the ground they stand on.

The approach I use sidesteps the multi-computer half of the problem entirely: Claude Code only ever
works on a project from a single, always-on machine in my office, and I reach that machine from my
laptop or phone over `/remote-control` or SSH. The tracker git is set up using the first option: the git
database is only stored on my always-on machine, in a folder outside of Dropbox, and synced to a
remote copy on GitHub for safety. When away from the office, I work on or view my files from my other
devices using Dropbox — while talking to Claude over remote — and these files get instantly synced
back to my always-on machine via Dropbox, where Claude Code then deals with the git history
automatically as part of its tracker process.