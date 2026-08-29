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
means a commit message citing `T103` stays findable forever. The `Task` column is capped at 50
characters, because the one thing that reliably destroys a table like this is one cell growing into a
paragraph.

### `PRIORITIES.md` — what to do next

The pointer, read straight after `INDEX.md`. Three sections and no more: notes for the next session,
the next priorities, and a window of recent sessions.

```markdown
## Next priorities

- Close out `T103`'s sparse-channel handling, then start `T104`'s unit tests.
- Once `T104` is done, start `T201` per `D03`'s pipeline recipe.

## Recent sessions

- **2026-07-14** — Applied `D02`'s batch cap; found the sparse-channel gap in `T103`.
- **2026-07-10** — Scaffolded the feature extractor against `T102`'s validated schema.
```

Every bullet is capped at 30 words and has to point at a decision, a detail file, or a task ID — a
bullet naming nothing is already drifting away from the thing it was describing. `Recent sessions` is
a fixed window of five: when a sixth lands, the oldest moves to `JOURNAL.md` in the same edit. It is a
window that gets rewritten, not a list that grows.

### `DECISIONS.md` — what we decided and why

A ledger of current rulings, one row per decision, each row's full reasoning living in its own
`detail/D##_*.md` file rather than in this one.

```markdown
| ID | Ruling (one line) | Scope | Set by | Ratified |
|-----|-------------------|-------|--------|----------|
| D01 | Backward-fill imputation with an explicit validity flag | — | claude 2026-07-19 | — |
| D02 | Cap feature-extraction batch size at 256 | [model-B only] | human 2026-06-20 | human 2026-06-20 |
```

The **ledger** exists because reading every full rationale costs roughly the whole decision record,
which for a mature project is thousands of words; a session reads the short ledger instead and opens
a `detail/D##_*.md` file only when its ruling is actually relevant. Unlike `INDEX.md`, the ledger is
overwrite-only in a stronger sense than "correct a wrong cell": a row never records history at all —
`Set by` and `Ratified` are provenance for the *current* ruling, not a trail of who has held the pen.
The trail lives one level down.

Concretely, `Set by` records who authored the current ruling and when (`claude <date>` or `human
<date>`), and `Ratified` records whether the human has since confirmed it (`human <date>`, or `—` if
not). Agents make and revise rulings freely — that's not the reserved judgment here — but a
`claude`-set ruling sits with `Ratified: —` until a human endorses it, and `tracker-close` surfaces
any ruling that has stayed unratified across a session boundary.

DECISIONS is *current policy* — what the project follows now, and who is answerable for that.
It is deliberately not a reproducibility record of what was actually run under an earlier ruling;
that record lives in the dated, append-only logs — `JOURNAL.md` and each task's progress log —
which keep the true history of what happened even after the policy that governed it has changed.

### `tracker/detail/D##_*.md` — one file per decision

Where a ruling's full reasoning lives — the part the ledger deliberately leaves out. The file opens
with a `## Current ruling` head over an append-only `## History`.

```markdown
## Current ruling
*Set by: claude 2026-07-19 · Ratified: —*

Backward-fill missing sensor readings, carrying an explicit validity flag on every imputed cell,
applied uniformly across channels before feature extraction.

## History

### 2026-07-19 — replaced forward-fill with backward-fill + validity flag

Was: forward-fill, no validity flag (set human 2026-06-02). Changed because forward-fill silently
carried the last good reading across dropouts, which downstream feature extraction then treated as
real signal.
```

Supersession is **edit-in-place**, the stronger form of I3. Reversing a ruling does not add a
banner pointing elsewhere; it rewrites the detail file's `## Current ruling` head with the new
ruling and demotes the retired one, verbatim, into that same file's append-only `## History`. A
reader opens the file, reads the head, and is already looking at what's true — there is no `★
superseded → D##` chain to follow, and no way to land on a dead ruling and mistake it for live
without deliberately reading past the head into the history below it.

### `tracker/detail/T###_*.md` — one file per task

Where the actual work lives: goal, sub-steps, acceptance criteria, stopping criteria, and a dated
progress log. The file opens with a `## Current state` block that is rewritten every time the log
below it grows.

```markdown
## Current state
*Refreshed: 2026-07-15*

Status: `in-progress`. Current approach: extract features batch-wise per `D03`'s pipeline recipe,
using the schema validated in `T102`. Open: the extractor does not yet handle the sparse-channel
case surfaced in the 2026-07-14 session below.

## Progress log

### 2026-07-14 — Added model-B batch cap per D02; surfaced sparse-channel gap

Applied the 256-row cap for model B. Found that channels with >40% missing values behave
unpredictably in the current recipe.
```

This pairing is the most important one in the system. The progress log is genuinely append-only and
allowed to grow — it is a record of what was believed and done at the time, and stays true as that.
But a long log with a summary at the top that nobody has refreshed is worse than no summary, because
the summary is the part a reader sees first. So the head and the body are written in one operation:
you may not grow the log without refreshing the state above it.

### `JOURNAL.md` and `ARCHIVE.md` — the overflow

Rolled-off session history and closed phases, respectively. Both are append-only, never loaded in
normal work, and never deleted. They exist so that `PRIORITIES.md` and `INDEX.md` can stay short
without anything being lost: material moves *out*, rather than being trimmed away.

## Three write modes

Every file above declares its write mode on its own third line, and every skill that touches it may
only write it that way:

- **overwrite-only** (`INDEX.md`, `PRIORITIES.md`, `DECISIONS.md`'s ledger) — rewritten in place. A
  correction replaces the claim where it stands; nothing is ever stacked above an older version. These
  files answer "what's true right now," so they can never accumulate a stale layer underneath a
  current one.
- **append-only** (`JOURNAL.md`, and a detail file's `## Progress log` or `## History`) — entries added
  at end of file, never rewritten. These are narrative, not current-state claims, so nothing about them
  needs reconciling.
- **headed-append** (every `detail/T###_*.md` and `detail/D##_*.md` file) — a small current-state head
  paired with an appended body, both written in the same operation.

The point of typing files this way is not persuasion. It is that the rot becomes structurally
unreachable rather than merely against the rules. A correction stacked above a stale claim requires an
overwrite-only file to have been written append-style — so if every skill that opens `INDEX.md` only
ever rewrites it, that failure has no file left to happen in. The mode doesn't ban long files; it bans
one whose top no longer describes its bottom.

## The nine invariants

The full definitions, with the concrete failure each answers, live in
[`skills/tracker-setup/references/invariants.md`](skills/tracker-setup/references/invariants.md) — the
canonical source every skill cites by ID rather than restating (I1 forbids exactly that, and a design
doc that violates the invariant it documents has no credibility). In one line each:

- **I1 — one home per fact.** State files hold current truth, `DECISIONS.md` holds rationale, logs
  hold narrative; no fact gets a second home to drift out of sync with the first.
- **I2 — every file declares its write mode and is only ever written that way.** The mechanism above.
- **I3 — supersession is marked at the source.** A reversal is annotated on the *original* entry, not
  only wherever a later sweep happens to land.
- **I4 — scope every fact that can apply to more than one context.** Once a second model or regime
  exists, a ruling that isn't universal needs an explicit tag saying so.
- **I5 — state files stay skimmable, enforced as aggregates.** Word caps and row limits are checked as
  one number, not trusted to per-item restraint.
- **I6 — status reflects reality.** Any number of tasks may be in-progress; what's illegal is
  in-progress that nobody has re-confirmed, or a status that contradicts what another file says about
  the same task.
- **I7 — anchors must survive edits.** No `file:line`; anchor by symbol, section, or function name. A
  line number goes stale silently; a symbol name stays greppable, so at least the staleness is
  detectable.
- **I8 — nothing dead may read as current.** No doc, comment, or task may still name a retired thing as
  live, anywhere in the repo.
- **I9 — a pivot triggers a sweep.** Retiring or replacing something is an event with a mandatory
  cleanup, not a quiet edit that leaves everything else as it was.

I5 is worth a note on why it is phrased as an aggregate. Caps that ask for restraint item by item tend
not to hold, because each individual overrun looks small and locally justified at the moment it is
written. Caps checked as a single number at write time do hold. So the mechanical checks
([`mechanical_checks.md`](skills/tracker-setup/references/mechanical_checks.md)) are word counts and
row counts rather than a request to keep things brief.

## How it gets used

Day to day you don't manage these files by hand. The standing rules in the generated `CLAUDE.md`
block, loaded every session, tell the agent when to read and write each one:

- **At session start**, the agent reads `INDEX.md` and `PRIORITIES.md` — what exists and what's next
  — then opens the `detail/T###_*.md` file for whatever task you're picking up. The `DECISIONS.md`
  ledger is there to be scanned; a `detail/D##_*.md` file is opened only when its ruling actually
  bears on the work.
- **During the session** you talk to the agent normally, no special commands. It keeps the current
  task's detail file up to date as the work moves.
- **At session end**, `tracker-close` writes the session's state back: it confirms or demotes every
  in-progress task, refreshes the state heads, rolls the oldest `Recent sessions` note into
  `JOURNAL.md`, and commits `tracker/` separately from any code.
- **Once per project**, `tracker-setup` scaffolds the folder and writes the `CLAUDE.md` block.
- **Now and then**, when the docs start to drift, `tracker-audit` sweeps for stale or conflicting
  claims, and `tracker-supersede` carries out a declared pivot — retiring one thing in favour of
  another everywhere it is named.

None of the four skills run themselves; an agent has to invoke them. That is deliberate for
`tracker-close` above all — a skill that can block a session's end is one people learn to route
around, so it never refuses to close.

Most decisions the agent makes and revises on its own: a `claude`-set ruling stands as current policy
with its `Ratified` column simply recording that the human hasn't signed off yet. Two things stay the
human's call — *ratifying* those rulings, and *originating* a pivot, the "X is dead, Y is current"
declaration that `tracker-supersede` then sweeps out across the repo. Guessing at a pivot doesn't
produce one bad line; it broadcasts a wrong marker everywhere at once, which is why the skill refuses
to start without both names stated.

## Notable design decisions

A few choices that shape the whole system, over and above the file-by-file rules above.

**Plain markdown, not a tool.** No database, no schema, no CLI — just text files a human reads
directly and an agent loads. At this scale a bespoke tool would cost more to build and maintain than
it saves, and markdown is already the medium both the human and the agent are fluent in. The
discipline lives in the write rules every skill follows, not in a storage layer that enforces them
mechanically.

**The agent drives; you talk in plain English.** There are no commands to memorize and no expectation
that you edit the files by hand. The standing rules make reading and updating the tracker part of
ordinary work, and even the four skills trigger on natural phrasing rather than a fixed syntax. It
should feel like working with a collaborator who keeps good notes, not like operating a bug tracker.

**Nothing is ever deleted.** Retired things get a banner, abandoned tasks keep their row and their
ID, closed phases move to `ARCHIVE.md`, superseded decision rulings keep their exact wording in
`## History`. Deleting is how a project loses the answer to "didn't we try that already?" — the
goal is that dead things stay readable while being unmistakably marked dead.

**Automation handles mechanism; the human handles meaning.** The skills do the mechanical work —
sweeping every file that names a thing, rolling old sessions into the journal, checking the word and
row caps — but stop short of judgments. `tracker-audit` reports what looks stale and changes nothing
until you say yes: whether a claim is *actually* stale, or whether two docs genuinely contradict, is a
reading rather than a measurement, and a skill that silently rewrites a corpus it just misread is
worse than no skill at all. The same line is why an agent can execute a pivot but never originate one.

**Format is versioned, migrations are opt-in.** The generated `CLAUDE.md` block carries a
`tracker-format` stamp; each skill targets a version. A tracker older than the running skill is read
as-is — the skills stay backward-compatible — and a migration is *suggested* at session handoff, run
deliberately by the human through `tracker-audit`, never forced mid-task. A format change is an
event the human opts into, not a tax the tooling imposes.

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