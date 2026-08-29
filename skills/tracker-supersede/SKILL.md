---
name: tracker-supersede
description: Use when the human declares a pivot — triggers like "we've pivoted", "X is dead, Y is the flagship now", "we reversed decision D##", "mark X retired", "X is retired, Y is current", "we're done with the old approach". Requires an explicit statement naming both halves — what is retired and what replaces it — and asks rather than inferring one from a vague prompt. Sweeps every place the retired thing is named across tracker/, CLAUDE.md, and code comments; marks it dead with a banner instead of deleting it; re-scopes claims that were only ever true of it; fixes dependencies left blocked on it; and commits tracker/ separately from any code fix. Manages project task *documents* on disk, not Claude Code's in-session task tools (TaskCreate/TaskList) — those are scoped to one conversation and never persist; this skill sweeps the durable, git-tracked record instead.
---

# tracker-supersede

I9 made repeatable: retiring or replacing a model, approach, or application is an event, not a
quiet edit, and this skill is the mechanical sweep that event triggers.

**Why this skill exists, concretely.** A real research project pivoted four times. Each time, the
old world was never swept: a retired model kept being called "the flagship" in roughly fifteen code
comments, a task sat `blocked` on a dependency that had already been abandoned, and decisions that
were only ever true of the dead approach kept reading as universal. Agents loaded that stale text
and acted on it — not through any fault of their own, because nothing in the file told them it was
dead. This skill is what stops that: one invocation per pivot, sweeping every place the old thing is
named, so I8 ("nothing dead may read as current") holds at the moment of the pivot instead of being
rediscovered months later by `tracker-audit`.

This document is self-contained for execution: it tells you what to search, what to change, and in
what order.

**Scope.** This skill retires a *thing* — a model, approach, dataset, or feature named across the
repo — and requires the human to state both halves (what is retired, what replaces it). Revising a
single decision's *ruling* no longer routes through here: that is an in-place edit of the decision's
`detail/D##_*.md` file (new ruling on top, retired ruling demoted to `## History`), recorded in the
ledger's `Set by`/`Ratified` columns. Use this skill only when the retirement spans many files.

## The one rule that outranks the rest: never infer a pivot

**"X is dead, Y is current" is a judgment about the project's direction, and it is the human's
alone to make** (spec §6). This skill detects nothing and decides nothing about *whether* a pivot
happened — it only executes a pivot someone has already stated. That statement must name **both**
halves explicitly: what is retired, and what replaces it. Anything short of that — a mood ("I think
we've moved on from some of this"), a one-sided claim ("X is basically dead" with no named
replacement), a question, a guess you could make from context — is not a stated pivot. It is a
prompt to ask about, not an instruction to act on.

**Why this is the one behaviour worth checking twice:** a wrong "retired" marker does not stay a
single bad line. It gets broadcast, by design, across every file that mentions the thing — INDEX
rows, PRIORITIES bullets, an affected decision's ruling, detail-file heads, CLAUDE.md, code
comments. An agent that talks itself into declaring a pivot from a vague prompt is worse than no
skill at all, because this skill's whole job is to make that declaration travel everywhere at once.

## Step 0 — guard: read the canonical invariants

Read `~/.claude/skills/tracker-setup/references/invariants.md`. **If it is not there, stop** and say
so plainly — the four `tracker-*` skills share this one file, and a checklist reconstructed from
memory is exactly the kind of drifted second copy I1 exists to prevent:

> `tracker-supersede` needs the canonical invariants at
> `~/.claude/skills/tracker-setup/references/invariants.md` and that file is missing. Copy the
> whole `skills/` directory from the tracker-skills repo, not this skill alone.

This skill executes I9, and leans hardest on I3 (supersession marked at the source), I4 (scope
claims that were only ever true of one thing), I6 (a task blocked on a retired thing is a dead
dependency), and I8 (nothing dead may read as current).

## Step 1 — require the explicit statement

You may arrive here from three places, and all three still owe you the same two named things:

- **The human says it directly** — "X is retired, Y is current," or any of the trigger phrasings in
  this skill's description.
- **`tracker-close` Duty 4** recommended this skill by name because something was retired in
  conversation but the tracker still names it as live outside what that session touched. Duty 4's
  recommendation is not itself the statement — confirm the two names with whoever invokes this
  skill before sweeping.
- **`tracker-audit` Step 6** asked a yes/no supersession question and got a yes. Audit's question
  already names both sides ("is the two-stage approach retired in favour of the joint one"), so a
  plain "yes" here **does** carry an explicit statement — the two names came from audit's question,
  not from this skill inferring them.

**Write down, before doing anything else:**

- **Retired:** the exact name(s) used for the thing that is now dead.
- **Current:** the exact name of what replaces it.
- **Aliases:** any other names, abbreviations, or prior names the retired thing has gone by in this
  repo (check `DECISIONS.md` and `INDEX.md` for earlier phrasings before you conclude there are
  none).

**If either name is missing, or the statement is ambiguous about which side is which, ask one short
question naming both slots and stop — change nothing until it is answered:**

> "I think we've moved on from some of this" doesn't tell me what's retired or what replaces it.
> What specifically is being retired, and what is the current approach in its place?

Do not proceed on a partial answer. Do not proceed on silence. This step has no fallback path that
ends in a sweep without both names in hand.

## Step 2 — search: grep the retired name and its aliases, then read every hit

```bash
grep -rn '<retired-name>' tracker/ CLAUDE.md src/ <other-code-dirs>
# repeat once per alias found in Step 1
```

Run it against the whole repository, not just `tracker/` — code comments are an explicit sweep
target and live outside it.

**Read every hit before touching anything. Never blind pattern-replace.** A mention inside a
historical Progress-log entry or a past `Recent sessions` line ("added the Alpha placeholder,
ruled D02") is correct as it stands — it is a narrative record of what happened, not a claim about
what is current, and I2 forbids rewriting append-only history. A mention in a head, a status line,
a ruling, a "path forward" bullet, or a code comment describing the thing as current or in-use is
exactly what needs fixing. The judgment is: **does this hit assert the retired thing is live, right
now?** If yes, it needs a fix from Step 3. If it is describing something that was true in the past
tense, at the time it was written, leave it alone.

## Step 3 — sweep, location by location

Work through every location the design names, using Step 2's hit list to know where to look. Skip a
location only if the search turned up nothing there — say so, don't silently omit it.

- **`DECISIONS.md` — the ruling is edited at its own `detail/D##_*.md` file, not stamped in the
  ledger (I3).** Find the decision(s) whose ruling was only ever true of the retired thing. Edit
  that decision's `detail/D##_*.md` in place: write a new ruling head stating what is now true
  because of this pivot, and demote the old ruling — verbatim — into that file's `## History` in the
  same edit, per I3. Then refresh that row's `Set by` in the ledger to record this pivot, so a
  reader scanning the ledger sees the current ruling directly, with no chain to follow and nothing
  else in the row to touch. If the pivot leaves a decision entirely moot — nothing it ruled on still
  applies — say so in the new ruling head and in `## History` rather than deleting the ledger row; a
  moot ruling is still a fact about what the project once did.

- **`INDEX.md` statuses.** Any row whose task *is* the retired thing (implements it, is scoped
  entirely to it) moves to `abandoned` — the status that means dead, kept for history, never
  deleted. Do not delete the row. A row only partially about the retired thing needs a rewritten
  `Task` cell or a pointer to Step 4's re-scoping rather than a status change.

- **"The path forward" in `INDEX.md`.** Any bullet naming the retired thing as the plan gets
  rewritten to name the current thing, or removed if it no longer applies and nothing replaces it
  point-for-point.

- **`PRIORITIES.md`.** Any bullet in `Notes for next session` or `Next priorities` describing the
  retired thing as the thing to do next is stale by definition — rewrite or drop it. Leave
  `Recent sessions` alone; it is a narrative log covered by Step 2's "past tense" rule.

- **Detail-file heads (`tracker/detail/T###_*.md`) — the whole head, not just `## Current state`.**
  The head of a headed-append file is everything above `## Progress log` — `## Current state`,
  `## Goal`, `## Sub-steps`, `## Acceptance criteria`, `## Stopping criteria`, `## Notes` — and every
  one of those sections can independently read as a live instruction to an agent skimming past
  `## Current state`. Fixing the status line and leaving a `## Sub-steps` list phrased as "implement
  X" is not a complete fix: a reader who jumps straight to sub-steps sees an active checklist, not a
  retired one. For every task whose task itself is retired: set status `abandoned` in
  `## Current state`; and mark every other head section that still reads as a live plan — most
  simply, a one-line qualifier at the top of the section ("*Historical — no longer pursued.*") is
  not enough on its own if the bullets under it still read as imperatives with no such qualifier
  repeated nearby; reread each section after adding the qualifier and ask whether a reader who saw
  only that section, out of context, would think it is still live. For a task that continues under
  the new approach, rewrite the head to say so instead. Refresh `*Refreshed: YYYY-MM-DD*` in the
  same edit (I2). Leave the Progress log below it untouched — that is the narrative Step 2 already
  cleared.

- **`CLAUDE.md`.** Check both the generated block — the region from the line starting with
  `<!-- BEGIN tracker` (prefix match, not the byte-exact string `<!-- BEGIN tracker -->`; see
  `claude_md_block.md`'s header note) through `<!-- END tracker -->` — and anything outside it. If
  the retired thing is only named inside the generated block, this is usually a symptom of a stale
  block, not a project-specific claim — note it but leave regeneration to `tracker-audit` Step 5
  unless the mention is a direct factual claim this skill can fix in place.

- **Code comments.** Rewrite a comment that asserts the retired thing is current — e.g. `# Alpha is
  the production path` becomes a comment naming the current thing and pointing at the decision that
  changed it, e.g. `# Beta is the production path (Alpha retired, see D0X)`. This is a **separate
  concern from the tracker commit** — see Step 6.

## Step 4 — re-scope now-false universal claims (I4)

Some hits from Step 2 are not about the retired thing by name — they are claims that were stated
universally ("the baseline," "always," "the recipe") but were, in fact, only ever true while the
retired thing was current. Once the pivot lands, that universal wording is false. **Do not delete
these claims** — add a scope tag, byte-exact from `invariants.md`'s Notation section, stating where
the claim did and does not apply:

```
★ SCOPE — <scope tag>: <one line stating where this does and does not apply>
```

This is different from an I3 ruling edit: a scope tag says "this was always local, the label was
just missing," not "this was reversed." Use whichever is true of the specific claim — most rulings
about the retired thing itself want the I3 treatment (new ruling head in the decision's own
`detail/D##_*.md`, old ruling demoted to `## History`); most incidental universal-sounding claims
elsewhere want an I4 scope tag.

## Step 5 — fix newly-dead dependencies (I6)

Re-check `INDEX.md`'s `Depends` column against every status Step 3 just changed. **A task `blocked`
on something Step 3 just marked `abandoned` or superseded is now a dead dependency, and I6 makes
that illegal** — a block that can never clear is a task quietly removed from the project without
anyone deciding to. For each one, set the true status: if the blocked task's own purpose no longer
makes sense without the retired thing, mark it `abandoned` too, with a one-line note pointing at the
decision that retired its dependency; if it can proceed against the current thing instead, repoint
`Depends` and change status to `ready` or `blocked` on the real, live dependency. Never leave a
`Depends` value pointing at something now dead.

## Step 6 — present a diff summary, then commit as two separate commits

Before committing, list every file changed and, for each, the one-line reason (which step drove the
change). This is the diff summary the human sees before it lands.

**This is two commits, not one, even though the pivot is a single event.** The project rule that
`tracker/` commits are separate from code commits (I1: git history is a narrative, and a tracker
commit and a code commit are different narratives) applies here exactly as it does to
`tracker-close` and `tracker-audit` — a pivot touching both is not an exception to that rule, it is
two separate facts changing at once.

```bash
git add tracker/ CLAUDE.md
git commit -m "Supersede: <retired thing> retired, <current thing> is current"
```

If Step 3 fixed any code comments, stage and commit those separately:

```bash
git add <changed source files>
git commit -m "Update comments: <retired thing> retired, <current thing> is current"
```

If there is nothing to sweep in code (Step 2 found no hits outside `tracker/`/`CLAUDE.md`), the
second commit simply does not happen — say so rather than committing an empty change.

## The boundary with `tracker-audit` and `tracker-close`

`tracker-audit` may *surface* a supersession candidate as a yes/no question (its Step 6) but never
executes the sweep itself — on a yes, it hands off here. `tracker-close` may *recommend* this skill
by name in its Duty 4 but never invokes it. Both boundaries exist for the same reason Step 1's guard
exists: the sweep this skill performs is broad and mechanical by design, so the decision that
triggers it needs to be unambiguous and human before the sweep starts, not inferred by whichever
skill happened to notice the contradiction first.
