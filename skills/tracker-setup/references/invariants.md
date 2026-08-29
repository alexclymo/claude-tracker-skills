# Tracker Invariants (I1–I9)

These nine invariants are the spine of the tracker system. They are defined once, here, and every
skill cites them by ID rather than restating them. Setup establishes each invariant when a project
is scaffolded; close preserves it in-session, checking its own edits before committing; audit
detects violations of it across the whole repo; supersede executes I9, the one invariant that is
itself an event rather than a standing rule. One list, read in four directions — that is what stops
the four skills drifting apart from each other over time.

## I1 — One source of truth per fact

State files (`INDEX.md`, `PRIORITIES.md`) hold current truth; `DECISIONS.md` holds rationale; git
history and detail logs hold the narrative. No fact is restated in a second state file.

*Why:* a real project's `INDEX.md` carried paragraphs of undocumented prose above its tables, and
each paragraph cited the very file the fact belonged in instead of living there. Its
`DECISIONS.md` entries separately absorbed evidence tables and what-was-built inventories that
belonged in the task's detail file. Both are the same failure: once a fact has two homes, the two
drift, and nobody's job is to notice which one is stale.

## I2 — Every file declares its type, and is only ever written that way

Every tracker file names its write mode on line 3, and is only ever written that way:

```
*File type: **overwrite-only** — rewritten in place. Correct claims where they stand; never stack a correction above one.*
*File type: **append-only** — entries appended at end of file. Never rewritten.*
*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*
```

A headed-append file pairs a small current-state head with an appended body, written in the same
operation: you may not grow the body without refreshing the head.

*Why:* a real project's largest detail file grew a body that gained entries for two dozen sessions
running, while its head — the spec half — was never touched again after the day it was created.
Appending feels like updating, so nobody re-reads the head; by the time anyone looked, the head
named a since-deleted function, prescribed an abandoned method, and still claimed a framing a later
decision had already retired.

## I3 — Supersession is marked at the source

The current ruling is always the head of its `detail/D##_*.md` file and is what a reader sees first;
when a ruling is reversed, the retired version is demoted into that file's `## History` in the same
edit that installs the new one. A dead ruling therefore has no position from which it can be read as
current — the fix is structural, not a warning banner. The ledger row shows only the current ruling
and never points forward to a superseding entry.

*Why:* that same frozen detail-file head kept describing a framing that a later decision had
retired, and the ID of the decision that retired it did not appear anywhere in the file. Nothing
pointed a reader back to the reversal, because the reversal was never marked where the original
claim lived — only rewriting the head in place, so the current ruling stood where the retired one
used to and the retired one moved down into `## History`, would have stopped the head from reading
as current for so long.

## I4 — Scope every fact that can apply to more than one context

Once a second model, regime, or application exists, every recipe, number, and decision that isn't
universal carries an explicit scope tag: `[KS]`, `[Huggett-diff]`, `[regime: cold]`. Universal-
sounding words with no scope tag are a smell the audit flags.

*Why:* the same real project ran more than one model side by side, yet its largest task file —
named after a single one of them — had quietly swallowed several other tasks that belonged to
their own scopes and already had their own INDEX rows and decisions. A file that reads as
universal because nothing marks its edges is where an unrelated task's facts go to get inherited
by mistake.

## I5 — State files stay skimmable

INDEX rows are the task name only; bullets stay short; PRIORITIES is capped; the recent-sessions
window is fixed-size. **Enforced as aggregates, not as per-item judgment**: a file-level word cap
gets respected because it is checked as one number, while a per-row limit left to write-time
restraint erodes row by row, each overrun looking small and locally justified on its own.

*Why (spec §7.2, the natural experiment):* on the same project, under the same rules, the
file-level PRIORITIES cap held completely while the per-row INDEX task-name limit failed on most
rows — same discipline, same authors, opposite outcome, because one was measured in aggregate and
the other wasn't.

## I6 — Status reflects reality

Any number of tasks may be `in-progress` — parallel work is normal, and a task may legitimately
stay in flight across sessions. What is illegal is `in-progress` that nobody has re-confirmed: at
every close, each in-progress task is explicitly confirmed live or demoted. A task blocked on a
retired or abandoned task is a dead dependency, and INDEX status must not contradict the
PRIORITIES narrative.

*Why:* a real project's "path forward" summary contradicted its own tables more than once, one
task stayed blocked forever on a dependency that had long since been abandoned, and an umbrella
task read `proposed` while every one of its children read `done`. None of this was caught because
nothing re-confirmed status at the point work stopped for the session.

## I7 — Anchors must survive edits

No `file:line` maps in docs; anchor by symbol, section, or function name instead. Cheap, and
always on.

*Why:* that same frozen detail-file head still named a specific function after the function had
been deleted. A symbol anchor can go stale too, but it stays greppable, so the staleness is at
least detectable after the fact. A `file:line` pointer would have silently pointed at whatever
code happened to occupy that line after two dozen sessions of edits, with no signal that it was
wrong at all.

## I8 — Nothing dead may read as current

No doc, comment, or task may still name a retired or superseded thing as live, anywhere in the
repo.

*Why:* a real project's largest detail-file head was, by the time anyone looked, wrong on every
axis at once: its title still claimed a retired framing, its status line hadn't moved, it named a
function that no longer existed, and it prescribed a method that had been abandoned. Nothing in
the file signalled that any of this had changed — it simply read as current.

## I9 — A pivot triggers a sweep

Retiring or replacing a model, approach, or application is an event, not a quiet edit. I8 is
enforced at the moment of the pivot, not months later.

*Why:* the same detail-file head sat untouched for two dozen sessions after the decision that
should have triggered its rewrite. The pivot was recorded in `DECISIONS.md`; nothing carried it
outward to the file that was still describing the world before it. A sweep at the moment of the
pivot is the only thing that closes that gap before it compounds across sessions.

## Notation

`★` is reserved for supersession and scope banners **only** — never for findings. A starred
finding that later turns out wrong is exactly what makes stale text scan as authoritative, which
is the failure this whole file exists to prevent. Two licensed uses, byte-exact:

```
★ SUPERSEDED by <what replaces it> (YYYY-MM-DD): <one line stating what is now true>
★ SCOPE — <scope tag>: <one line stating where this does and does not apply>
```

The first form marks a retired *thing* — a model, approach, dataset, or feature — dead at its home
in the repo so it cannot read as live (I8); `tracker-supersede` writes it when the human retires
something across the project (I9). It is **not** used for decisions: a superseded decision *ruling*
is handled by editing its `detail/D##_*.md` in place — the new ruling becomes the head and the
retired one is demoted to that file's `## History`, with no banner and no ledger status pointer (I3).

Anywhere else `★` appears in a tracker file or an audit finding, that is itself an I8 violation:
something is being marked as attention-worthy-and-true when only supersession of a retired thing
and scope are licensed to claim that.
