---
name: tracker-audit
description: Use when the user wants to audit the task tracker, clean up the task docs, or says the docs feel stale, out of date, or contradictory — triggers like "audit the task tracker", "clean up the task docs", "the docs feel stale", "reconcile the tracker", "health check the tracker", "do the tracker docs still match reality". Sweeps the whole repo — tracker/, CLAUDE.md, architecture and navigation docs, and code comments — for stale and contradictory claims, reports them ranked by how likely each is to cause a wrong agent decision, and fixes them only on explicit approval. Manages project task *documents* on disk, not Claude Code's in-session task tools (TaskCreate/TaskList) — those are scoped to one conversation and never persist; this skill audits the durable, git-tracked record instead.
---

# tracker-audit

The periodic deep sweep. `tracker-close` checks its own edits at the end of each session; this skill
checks **everything else** — the accumulated corpus, including every file no recent session
happened to touch. Those untouched files are where rot lives, because nothing else in this
collection ever re-reads them.

**Why this skill exists, concretely.** On a real research project, a detail file's head sat frozen
for two dozen sessions while its log grew beneath it. By the time anyone looked, the head named a
deleted function, prescribed an abandoned method, and still claimed a framing a later decision had
retired — and nothing in the file signalled any of it. Agents kept loading it as current. Audit's
job is to find claims like that **before** they cost someone a decision.

This document is self-contained for execution: it tells you what to run, in what order, and what
each subagent should hunt for.

## The one rule that outranks the rest: report first, always

**The detect phase never edits anything.** Not a typo, not a date stamp, not an obviously-wrong
status. Every subagent this skill launches is read-only, and this skill itself writes nothing until
the user has seen the report and said yes. A skill that quietly rewrites a corpus it has just
finished misreading is worse than no skill at all — audit's findings are judgments about meaning,
and judgments need a human check before they become edits.

Corollary: **never declare a pivot.** See Step 6.

## Step 0 — guard: read the canonical invariants and mechanical checks

Read `~/.claude/skills/tracker-setup/references/invariants.md` and
`~/.claude/skills/tracker-setup/references/mechanical_checks.md`.

**If either file is not there, stop.** Do not fall back on the summary in a project's CLAUDE.md block
or on your memory of what the invariants or checks say — a checklist reconstructed from memory is
exactly the kind of drifted second copy I1 exists to prevent. Say plainly:

> `tracker-audit` needs the canonical references at
> `~/.claude/skills/tracker-setup/references/invariants.md` and
> `~/.claude/skills/tracker-setup/references/mechanical_checks.md`, and at least one of those files
> is missing. The four `tracker-*` skills (`tracker-setup`, `tracker-close`, `tracker-audit`,
> `tracker-supersede`) share these files and must be installed together — copy the whole `skills/`
> directory, not this skill alone.

I1–I9 as read from that file are the detection checklist for Step 2. **Read the list as "find
violations of each."** If setup ever starts enforcing a new invariant, this skill starts checking it
automatically, because it reads the list rather than restating it.

## Step 1 — scope the run before launching anything

Establish four things and say them back to the user in one short paragraph before Step 2 starts:

1. **The tracker directory.** Normally `tracker/` at the project root. If the project has no
   `tracker/`, stop and say so — this skill audits a tracker, it does not create one, and it does
   not support the superseded `tasks/` layout. The single exception: if the user has explicitly
   named a different directory for this run, use it, and say in the report which directory you
   used. Do not infer that exception from the mere presence of another directory.
2. **The corpus boundary.** `tracker/` plus `CLAUDE.md` plus architecture/navigation docs (`README`,
   `docs/`, `AGENTS.md`, anything that tells a reader how the project works) plus code comments.
   Nothing outside the repo.
3. **The depth dial** (see Step 2). Default is normal. Say which depth you are running.
4. **Whether this is report-only.** If the user asked for a read-only or diagnostic run, say
   explicitly that nothing will be modified, and treat Steps 4 and 5 as out of scope for the run
   rather than as steps awaiting approval.

## Step 2 — detect: four corners, parallel read-only subagents

Launch the four corners **as parallel subagents**, in a single batch. They do not depend on each
other, and running them serially on a large corpus is the difference between a sweep someone
actually runs and one they avoid.

**Every subagent is read-only.** Say so in each prompt, in those words. Give each one the invariants
file path so it cites `I#` from the canonical text rather than from your paraphrase.

### The shape of a finding — required, no exceptions

Each corner returns findings in exactly this four-part shape. A finding missing any part is not a
finding; send it back or drop it.

```
[I#] <location — file, and section or symbol name, never file:line (I7)>
Stale claim:    "<quote or close paraphrase of what the doc currently asserts>"
Currently true: <what is actually the case, and how you know — the file, row, decision, or
                commit that establishes it>
Risk:           <what an agent would do wrong if it believed the stale claim>
```

"Currently true" is the part that makes a finding actionable and the part most often skipped. **If
you cannot establish what is currently true, you do not have a finding — you have a question.**
Report it in a separate `Questions` list instead, and never rank a question among the findings.

**Establish "currently true" from the most primary source available, never from another tracker
file.** This is the trap this corner walks into most reliably: you find file A contradicting file B,
and you write up B's version as what is currently true. But B is part of the same corpus you were
sent to audit, and in a corpus with two stale claims about one fact, B is very often the *second*
stale claim rather than the truth. Go to the thing the docs describe — the code, the decision entry
that actually made the ruling, the commit, the filesystem — and quote that. If the only evidence you
have is a second doc, say so in the finding ("per `PRIORITIES.md`, unverified against code"), so a
reader knows the correction is only as good as the file it came from.

Findings never use `★`. Per the invariants' Notation section, `★` is reserved for supersession and
scope banners only; a starred finding is itself an I8 violation.

### The depth dial

Three depths, chosen in Step 1 and passed to each corner:

- **Light** — corners (a) and (b) only, mechanical checks plus heads. Minutes. Good after a run of
  quiet sessions.
- **Normal** (default) — all four corners; corner (d) restricted to comments in files git says
  changed recently and to files named in tracker docs.
- **Deep** — all four corners, corner (d) across the whole source tree.

**Corner (d) is the expensive one** and scales with the size of the codebase, not the tracker. On a
large project, run (a)–(c) at full depth and (d) light rather than dropping a corner entirely — a
shallow pass over code comments still catches the loud ones (a comment naming a deleted function, a
`TODO` referencing a task that closed a year ago), and dialling it down is the intended way to keep
this skill cheap enough to run periodically.

### Corner (a) — DECISIONS

**First, and cheaper than anything else in this corner: read the `tracker-format` stamp** in the
project's `CLAUDE.md` block. If it is older than this skill targets (v2), report a single migration
finding, ranked high (a v1 corpus edited under v2 assumptions drifts). A block with **no**
`tracker-format` line at all is v1 — the entire pre-stamp population — so treat a missing stamp as
older than v2 and take the migration path, never as "nothing to compare, skip." The v1→v2 changes are
(1) `DECISIONS.md` splits into a ledger + one `detail/D##_*.md` per decision, (2) the ledger's old
`Status` column becomes `Set by` / `Ratified`, (3) inline `### D##` entries move to their detail
files with the retired-ruling history preserved. Show the concrete plan (which entries → which
files) and apply it only on the human's explicit yes, like every other audit fix — Step 4 covers the
mechanics. `INDEX.md`'s caps need no migration: the v2 prose cap is strictly more permissive than
the flat cap it replaces. If the stamp already reads `2`, read `DECISIONS.md` and its
`detail/D##_*.md` files exactly as v2 describes them below.

Read the tracker's `DECISIONS.md` end to end. Hunt for:

**Cheap first: check for stray banners.** Run `grep -c 'SUPERSEDED' <tracker>/DECISIONS.md` before
reading anything. Under v2 the ledger never carries a forward-pointing banner — supersession is
structural, not a note — so **any** hit here is itself a finding: either leftover v1 structure that
was never migrated (see above), or a reversal someone recorded as a banner instead of editing the
decision's own `detail/D##_*.md` file in place. Chase every hit to that decision's detail file and
check whether its head and `## History` are actually in sync.

- **Retired rulings not demoted at the source (I3).** For every decision, does its own
  `detail/D##_*.md` head (`## Current ruling`) still match what the project actually follows, or does
  it read as current while other evidence — a later session, the code, a different decision — shows
  the project moved on? Supersession is edit-in-place under v2: the fix is to rewrite that file's
  head and move the retired ruling into its own `## History`, never to leave the old ruling standing
  and note the change somewhere else. A `D##` whose head is stale is the single highest-yield check
  in this corner.
- **Ledger/detail mismatch (I2).** This is mechanical check 3 (corner (b)) — ledger rows vs.
  `detail/D##_*.md` file count. Don't re-derive the number here; take it from check 3, and use this
  corner's end-to-end read to say *which* `D##` is missing a row or a file.
- **Category error in detail-file content (I1).** A `detail/D##_*.md` file that has absorbed evidence
  tables, what-was-built inventories, artifact path lists, or result numbers — content whose home is
  the task's own detail file, not the decision's. Mechanical check 4 (corner (b)) already gives the
  size signal shared with task files; a decision file sitting well above its neighbors is the profile
  this failure produces.
- **Unscoped rulings (I4).** Once the project has more than one model, regime, dataset, or
  application, any decision stated in universal language that in fact only holds for one of them.
  Universal-sounding words with no scope tag — in the ledger's Scope cell or the detail file's own
  `★ SCOPE` line — are the smell.
- **Dead things still named live (I8).** Any decision detail file that still describes as current an
  approach later abandoned — check whether its own head was ever rewritten, or whether a different
  decision quietly moved past it without this file being touched.

### Corner (b) — INDEX + PRIORITIES

**Cheap first pass: run all six mechanical checks, exactly as written in `mechanical_checks.md`
(read in Step 0), from the project root.** These are the same six `tracker-close` runs over its own
session's edits; here they run over the whole corpus, and the numbers go in the report whether or
not they breach a threshold. For check 6, run variant 6b (the history form): this runs over
committed history, not a mid-session working tree, which is exactly the context 6b is for. If it
prints `CHECK 6b DEGRADED`, git cannot see `tracker/` (gitignored, or a layout-D project with no
git), so there is no commit date to compare the `Refreshed:` dates against. Read them against
`PRIORITIES`' Recent sessions and `JOURNAL.md` instead, and report the check as degraded with what
you compared — never as passed.

The commands spell `tracker/` literally. If Step 1 established a different directory for this run,
substitute it everywhere before running them, and say in the report which directory the numbers
describe. If a check's assumption does not hold for the project in front of you — a different column
layout, no ledger markers, no `detail/` subdirectory — say so, adapt the command, and report the
number you *can* get. A check you skipped in silence reads in the report exactly like a check that
passed.

**Then the judgment pass over INDEX and PRIORITIES:**

- **INDEX↔PRIORITIES status-word mismatch (I6).** For every task named in `PRIORITIES.md`, compare
  the verb PRIORITIES uses against the status INDEX gives it. PRIORITIES saying "start T##" or "pick
  up T##" for a row INDEX already marks `in-progress`, or "continue T##" for a row marked `proposed`,
  or "next: T##" for a row marked `done` — each is a contradiction between the two state files, and
  it is the specific failure an agent acts on first, because PRIORITIES is what it reads to decide
  what to do. Check this in both directions: a task INDEX calls `in-progress` that PRIORITIES never
  mentions at all is the same rot seen from the other side.
- **"Path forward" versus the tables under it (I6).** INDEX's narrative head is a head like any
  other and drifts like any other. Does every bullet still point at a real, current `D##`/detail
  file/task ID, and still describe what the tables now show?
- **Dead dependencies (I6).** Any row `blocked` on a task that is itself `abandoned`, superseded, or
  `done`. A block that can never clear is a task removed from the project without anyone deciding to.
- **Unconfirmed `in-progress` (I6).** Any number of rows may be `in-progress`; what is illegal is one
  nobody has re-confirmed. Cross-check each against its detail file's `Refreshed:` date and Progress
  log. A row `in-progress` whose detail file has not moved in months is a demotion candidate, not a
  live task.
- **Derived-status contradictions (I6).** An umbrella or parent task whose status is behind all of
  its children (`proposed` while every child is `done`).
- **Undocumented prose in a state file (I1).** Preamble paragraphs above the tables, especially ones
  that cite the very file the fact belongs in. That citation is the tell: the author knew where it
  belonged and wrote it here anyway.
- **Bloat (I5).** Report checks 1, 2 and 4's numbers plainly against thresholds. Size findings are
  real but they are usually **verbose-but-harmless** — sort them accordingly in Step 3.

### Corner (c) — docs versus code

Compare what the tracker and the project's prose docs claim against what the repository actually
contains. This corner is where I8 bites hardest, because doc claims about code go stale silently.

- **Heads of headed-append files (I2).** For every `tracker/detail/*.md`, read its head — `## Current
  state` for a task file, `## Current ruling` for a decision file — **and then read the tail**: the
  last few Progress-log entries for a task file, the last `## History` entry for a decision file. Ask
  whether the head still describes what the tail describes. Rank the biggest files first: a file
  whose body has grown for many sessions is precisely where the head is most likely frozen, and
  appending feels like updating, so nobody re-reads it. Check the head's title, its status line (or,
  for a decision, its `Set by` / `Ratified` line), and every method, file, and symbol it names.
- **Named symbols that no longer exist (I7, I8).** Grep the codebase for every function, class,
  script, and file name a tracker doc, a `## Current state` head, or a `## Current ruling` head
  asserts is current. A symbol a doc calls live that returns no hits is a finding with an unusually
  clean "currently true": the symbol is gone.
- **`file:line` anchors (I7).** Any doc pointing at a line number. These are wrong-by-construction
  after any edit and silently point at whatever now occupies the line.
- **One task per file (I4, I5).** Detail files that have swallowed other tasks — sections describing
  work that has its own INDEX row or its own `D##`. A file named after one thing but containing
  several reads as universal, and its facts get inherited by the wrong task.
- **CLAUDE.md and other always-loaded docs versus reality (I8).** Does the standing-rules block still
  match the canonical invariants? Does the project's `README`/`AGENTS.md`/architecture doc still
  describe the current layout, the current entry point, the current method?
- **Method and framing claims (I8).** A doc prescribing an approach the decisions record retired.
  Cross-reference against corner (a)'s findings on stale decision heads where you can — but state it
  as a finding only when you can name the decision or commit that retired it.

### Corner (d) — code comments

The expensive corner; scope it per the depth dial. Read comments, docstrings, and module headers as
documents subject to the same invariants:

- **Comments naming retired approaches, models, or decisions as current (I8).** Especially module
  headers and docstrings, which are the code's equivalent of a frozen head.
- **`TODO`/`FIXME`/`XXX` referencing work that is finished, abandoned, or superseded.** Cross-check
  each against the INDEX. A `TODO` for a `done` task is noise an agent will act on.
- **Comments citing task or decision IDs that no longer say what the comment claims** — a `# per
  D07` next to code that D14 changed.
- **Comments describing a function's behaviour that the function no longer has**, where the mismatch
  is plain from reading the two together. Do not attempt a full correctness review; that is not this
  skill's job. Stay with claims that are checkably, textually stale.

## Step 3 — report, ranked, then stop

Report **corner by corner**, and within each corner rank by one criterion only: **how likely this
finding is to cause a wrong agent decision.** Not severity, not size, not how long it has been
wrong. The question is: if an agent loaded this file tomorrow and believed it, what would it get
wrong, and how likely is it to be loaded?

That criterion produces a specific ordering, and it is worth stating why:

- **Top:** a confidently-worded stale claim in a file agents load often — a frozen `## Current state`
  or `## Current ruling` head, a PRIORITIES bullet pointing at the wrong next task, a retired method
  still prescribed as the approach. These are read as current and acted on directly.
- **Middle:** contradictions between two files, where an agent gets one of two answers depending on
  which it read. Dead dependencies, INDEX↔PRIORITIES mismatches, umbrella-status drift.
- **Bottom:** bloat and verbosity. A 32,000-word detail file is a real I5 problem and a real cost,
  but a long file is not a *wrong* file — it wastes context, it does not misdirect.

**Separate the two kinds explicitly**, under headings in the report:

- **Genuinely stale** — the doc asserts something that is not true. These cost decisions.
- **Verbose-but-harmless** — the doc is bloated, redundant, or badly placed, but nothing it says is
  false. These cost context and skimmability.

Never merge the lists to make the report look weightier. A reader who cannot tell at a glance which
findings are *wrong* versus merely *long* will triage badly, and the whole point of ranking is to
make triage cheap.

Close the report with: the mechanical numbers from corner (b) as a table; the `Questions` list
(things you could not establish); the depth you ran and what that means you did **not** look at; and
the supersession candidates from Step 6, phrased as questions.

**Then stop.** Do not proceed to Step 4 without explicit approval, and do not present Step 4 as
though it has already begun. If the run was declared report-only in Step 1, say that the run is
complete and no approval is being sought.

## Step 4 — apply, on explicit approval only

Only after the user approves, and only the findings they approved. If they approve some and not
others, apply exactly those. Work fix-by-fix:

- **Fix at the source (I2, I3).** Correct the claim where it stands in an overwrite-only file; never
  stack a correction above a stale one. For a decision whose current-ruling head is stale, rewrite
  that `detail/D##_*.md` file's head in place and move the retired ruling into its own `## History` —
  supersession is structural under v2, not a banner, and nothing in the ledger row ever points
  forward to a superseding entry.
- **Execute an approved format migration.** Split `DECISIONS.md` into the ledger plus one
  `detail/D##_*.md` per decision, following corner (a)'s plan: convert the old `Status` column to
  `Set by` / `Ratified`, and move each inline `### D##` entry into its own detail file, demoting any
  already-retired ruling into that file's `## History` in the same edit rather than carrying it
  forward as current. On success, rewrite the `CLAUDE.md` block's `tracker-format` stamp to `2`; Step
  5 regenerates the rest of that block if it also needs it.
- **Add scope tags (I4)** in the licensed form `★ SCOPE — <tag>: <where this does and does not
  apply>` to facts that are true only for one model, regime, or application.
- **Demote bloat (I5).** Prose that accumulated in a state file moves into the relevant detail file's
  log; an over-long INDEX `Task` cell loses everything but the name, with the detail going to that
  task's detail file. Move, do not delete — the fact keeps exactly one home, and that home is the
  one the invariants name.
- **Correct statuses and dead dependencies (I6).** Set each status to what is true; fix or clear a
  `Depends` that can never clear.
- **Archive closed phases.** A phase whose rows are all `done`/`abandoned` moves out of `INDEX.md`
  into `ARCHIVE.md`, leaving a one-line pointer.
- **Reconcile INDEX↔PRIORITIES** so the narrative and the tables agree, in the same pass.
- **Refresh every head whose body you changed**, and the `*Last updated:*` / `*Refreshed:*` stamps.

Then commit `tracker/` **separately from code**, exactly as `tracker-close` does:

```bash
git add tracker/ CLAUDE.md
git commit -m "<one line: what this audit fixed>"
```

Never mix a code change into this commit. If the apply pass touched code comments (corner (d)), that
is a second, separate commit — a tracker commit and a code commit are different narratives and I1's
one-home-per-fact logic applies to git history too.

## Step 5 — regenerate a stale CLAUDE.md block

Find the project's tracker block: the region from the line **starting with** `<!-- BEGIN tracker`
(prefix match — see `claude_md_block.md`'s header note; never grep for the byte-exact string
`<!-- BEGIN tracker -->`) through `<!-- END tracker -->`. Compare it against
`~/.claude/skills/tracker-setup/references/claude_md_block.md`. If they differ, replace the block's
contents with the canonical version, leaving everything outside the markers untouched. Regeneration
replaces only what sits **between** the two markers; it never reads, writes, or otherwise touches
anything after `<!-- END tracker -->`, which is where `## Project settings` lives.

**This is the step that closes the "improvements never reach old projects" gap.** A project
scaffolded a year ago carries whatever standing rules were canonical then, forever, because nothing
else in this collection ever revisits them — every session loads the old block and never notices.
Regeneration here is how an invariant added to `tracker-setup` today reaches a project set up before
it existed. If the block is missing entirely but the tracker exists, offer to add it.

If the user has hand-edited inside the markers, say so before overwriting and let them decide —
their edit is a fact with a home problem, not necessarily a mistake, and the markers say the region
is generated.

## Step 6 — surface supersession candidates as a fast yes/no

**Audit never declares a pivot.** "X is dead, Y is current" is a judgment about the project's
direction, and it is the human's alone to make — it is the one call no skill in this collection may
originate. Audit can see that two claims conflict; it cannot know which one the project intends to
keep. Guessing wrong here does not produce one bad line, it broadcasts a wrong "retired" marker
across every file that mentions X.

So for every candidate the corners surfaced — a decision that looks reversed, a method two docs
disagree about, an approach the code seems to have left behind — ask **one short question with a
yes/no answer**:

> `DECISIONS.md` D07 prescribes the two-stage estimator; D19 and the last four commits to
> `estimate.py` both use the joint estimator. **Is the two-stage approach retired in favour of the
> joint one — yes or no?**

Rules for these questions:

- State both sides and the evidence for each. Never lead with a conclusion.
- One question per candidate. Batch them as a short list so the user can answer several in a line.
- **On a yes: invoke `tracker-supersede`** with the retired thing and the current thing named. That
  skill owns the sweep; this one does not do it inline.
- **On a no, or on silence: change nothing.** An unanswered question stays a question and goes back
  into the report as one. It never becomes a finding, and it certainly never becomes an edit.
- If a corner reported something as an I8 finding but you cannot name the decision or commit that
  retired it, it belongs here as a question, not there as a finding.

## The boundary with `tracker-close`

`tracker-close` checks **its own edits** at the end of a session and always commits. `tracker-audit`
checks **the whole corpus** and commits nothing without approval. When close finds a problem outside
what its session touched, it reports and recommends this skill by name — it does not fix it. So a
finding this skill reports is frequently one close already declined to fix, by design. Do not treat
that as close having failed; treat it as the handoff working. Equally, do not narrow this skill's
sweep to "what changed recently" — the files nobody touched are the whole reason this skill exists.
