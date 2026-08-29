---
name: tracker-setup
description: Use when the user wants to set up the task system, set up a tracker, or initialise task tracking in a project — triggers like "set up the task system here", "set up a tracker for this project", "initialise task tracking". Scaffolds a git-tracked tracker/ directory of task and decision documents plus a CLAUDE.md standing-rules block. Manages project task *documents* on disk, not Claude Code's in-session task tools (TaskCreate/TaskList) — those are scoped to one conversation and never persist; this skill is for the durable, git-tracked record instead.
---

# tracker-setup

One-time scaffold. Run this once per project, at the project root. If the project already has a
tracker, this skill refuses to touch it and hands off instead — see Step 0.

This document is self-contained for execution: it tells you what to run and in what order. It
points at `references/` for content to copy, but does not restate what those files say.

## Step 0 — check whether a tracker already exists

Before touching git or anything else, look at the project root:

- **If `tracker/` exists:** stop. Do not scaffold, do not overwrite anything. Tell the user this
  project already has a tracker and invoke the `tracker-audit` skill instead — that skill, not this
  one, handles an existing tracker.
- **Else if `tasks/` exists (and `tracker/` does not):** stop. Tell the user this project uses the
  superseded `tasks/` layout, that these skills do not support it, and that migrating to `tracker/`
  is done by hand, not by this skill. Do not scaffold anything.
- **Otherwise:** proceed to Step 1.

## Step 1 — git before anything else

Run, at the project root:

```
git rev-parse --is-inside-work-tree
```

**If this fails (no repo yet):**

1. Take `<project-name>` as the basename of the project's absolute root directory.
2. Check whether the project's absolute path contains `Dropbox`, `iCloud`, `OneDrive`, or
   `Google Drive` as a substring.
   - **If it does not:** run `git init -b main`. None of the multi-machine questions below apply —
     skip straight to point 3.
   - **If it does:** the project lives inside a cloud-sync folder. A `.git` directory syncs like any
     other folder, but git's object store is not designed for that: a sync client can write a
     partial object mid-commit, two devices can converge on conflicting copies of the same ref, or a
     sync event can simply delete `.git` outright — and none of this looks like an error to the sync
     client, only to git, later. **Do not pick a layout for the user. Ask: "Will you work on this
     project from more than one computer?"** Then present these four options — compactly, the goal
     is a clear choice, not a wall of text — and apply whichever one the user picks:

     - **A — one machine, git database outside the sync folder** (`--separate-git-dir`).
       *Recommended when it applies.* Works at any repo size. **Blunt warning:** the `.git` pointer
       file holds an **absolute path**, which binds the repo to this machine — on a second computer
       git will fail outright, or, worse, find a *different* repo living at that path, while the
       sync client keeps syncing the working tree regardless, so edits made elsewhere show up as
       uncommitted changes with no history behind them.
     - **B — several machines, git database *inside* the sync folder.** The simplest multi-machine
       option, and the only one where gitignored material (data, workspaces, model outputs) travels
       between machines too — usually the whole reason the project is in a sync folder. **Degrades
       as the repo grows:** sync churn on `.git` risks silent corruption, and the risk is *higher*
       multi-machine, since two machines can touch `.git` mid-sync. Rule: let the sync client finish
       before switching machines, never work from two at once. Suitable for small projects only.
     - **C — several machines, separate-git-dir on each, shared remote.** Holds up at any size but
       demands clean setup on every machine and disciplined pull-before/push-after every session.
       **Strongly discouraged** — easy to get subtly wrong. Gitignored material does NOT travel this
       way.
     - **D — no git at all.** Sync history is the only history. Always available, and the honest
       choice for someone not comfortable with git. Costs: no traceability, no revert, and
       `tracker-close` loses its commit duty.

     Apply the choice:
     - **A:** `mkdir -p "$HOME/git-repos" && git init -b main --separate-git-dir="$HOME/git-repos/<project-name>.git"`.
       Tell the user plainly what this does: working files stay in the project folder and keep
       syncing normally; `.git` there becomes a small pointer *file* reading `gitdir:
       $HOME/git-repos/<project-name>.git`; the real object database lives outside the sync folder
       entirely.
     - **B:** plain `git init -b main`, inside the sync folder as normal.
     - **C:** run A's command on *this* machine; tell the user every other machine needs its own
       `git init -b main --separate-git-dir=...` pointed outside its own sync folder, plus a shared
       remote (point 5 below can set that up now).
     - **D:** run no git command at all. Tell the user plainly that `tracker/` will not be under
       version control and sync history is the only history from here on; `.gitignore` is still
       worth writing (point 3) for editor/tooling hygiene even without git.

     **Record the letter chosen** — Step 4 writes it, plus a one-line reminder, into `CLAUDE.md`'s
     `## Project settings` section:
     - A: "One machine; git database lives outside the sync folder via an absolute-path pointer —
       this repo will not work from a second machine without redoing setup there."
     - B: "Several machines; git database lives inside the sync folder — let sync finish before
       switching machines, never work from two at once. Check sync status before starting work each
       session; this catches divergence, it does not make multi-machine editing safe."
     - C: "Several machines; separate git database on each, shared remote — pull before and push
       after every session; gitignored files do not travel this way. Check the remote before
       starting work each session; this catches divergence, it does not make multi-machine editing
       safe."
     - D: "No git — sync history is the only history; `tracker-close` skips the commit step."
3. If the project root has no `.gitignore`, write one. Be ruthless about large binaries and
   generated output — this is a text-and-code tracker system, nothing it produces should ever need
   a binary in git. Cover at minimum: common data/model artifact extensions (`*.csv`, `*.parquet`,
   `*.h5`, `*.hdf5`, `*.pkl`, `*.npy`, `*.npz`, `*.pt`, `*.pth`, `*.ckpt`, `*.onnx`), archives
   (`*.zip`, `*.tar`, `*.tar.gz`, `*.7z`), media (`*.mp4`, `*.mov`, `*.mp3`, `*.wav`), and the usual
   environment/cache clutter (`__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `node_modules/`, `.DS_Store`,
   `*.log`, `.vscode/`, `.idea/`). If a `.gitignore` already exists, leave it as the user wrote it.
4. Do **not** stage or commit anything yet. Nothing is committed until Step 5, and even then only
   `tracker/` and the `CLAUDE.md` block — never the project's existing code. That stays uncommitted
   (or committed later by the user, separately) unless the user asks otherwise.
5. Mention, once, that you can set up a private remote for this repo if the user wants one now —
   offer it, do not require it, and do not block on an answer.

**If the check succeeds (a repo already exists):** do nothing to git itself. Note whether
`.gitignore` exists; if the project has none, apply the same ruthless default from point 3 above.
Proceed to Step 2 either way.

## Step 2 — scan the project to find its initial task list

Do this before writing anything into `tracker/` (Step 3 needs these findings):

- **Git history** (`git log --oneline` if any commits exist) — what's already done.
- **Open branches** (`git branch -a`, if any exist beyond the current one) — each unmerged branch is
  a candidate in-flight or proposed task; check its name and its unique commits
  (`git log main..<branch> --oneline`) to see what it's working toward.
- **`TODO` / `XXX` / `FIXME` markers** (e.g. `grep -rn 'TODO\|XXX\|FIXME'` over source files,
  excluding anything the new `.gitignore` excludes) and any obviously incomplete or stubbed-out
  files — what's in flight.
- **The dependency chain** between what you find — what unblocks what — to decide `Depends` and
  which ready task comes next.
- Anything that looks aspirational but not yet started (a stub module, a named-but-empty
  directory, a comment describing a future step) goes in as `proposed`, not `ready` or `in-progress`.

Turn each finding into one future `INDEX.md` row (`ID | Task | Status | Depends | R:Human | R:Claude
| Category`, task name ≤50 chars) plus one future detail file. Use `T1xx` numbering for this first
phase unless the scan clearly reveals distinct phases already (see `index_template.md`'s
phase-numbering convention).

If the project is a **research project**, phase names like "Data pipeline" / "Model estimation" /
"Results and writeup" are a reasonable example split — offer it as an example, not a default, and
prefer whatever the scan actually shows. If it's a **software project**, phase names like
"Scaffolding" / "Core feature" / "Hardening and release" are the equivalent example. Say
explicitly, when presenting either, that it is an example the user should confirm or correct, not a
decision already made on their behalf.

## Step 3 — scaffold `tracker/`

Create `tracker/` and `tracker/detail/` at the project root. `tracker/detail/` is shared: task
detail files (`T###_<slug>.md`) and decision detail files (`D##_<slug>.md`) both live there, side
by side, distinguished only by the ID prefix.

Using the six file templates in `references/` — `index_template.md`, `priorities_template.md`,
`decisions_template.md`, `journal_template.md`, `archive_template.md`, `detail_template.md` — write
`tracker/INDEX.md`, `tracker/PRIORITIES.md`, `tracker/DECISIONS.md`, `tracker/JOURNAL.md`,
`tracker/ARCHIVE.md`, and one `tracker/detail/T###_<slug>.md` per task found in Step 2.

**Adapt, do not copy.** Every template carries one worked example (a fictional data-pipeline
project, tasks `T101`–`T203`, decisions `D01`–`D03`) so its cross-references resolve to each other
inside the template file. That example exists to show the *shape* — file-type line, conventions
header, column layout, section rules, word caps — not to be pasted into a real project. Carry the
structural parts (the file-type line, the Conventions/Rules header, the section-kind rules, the
word-cap and bullet-length rules) into each real file verbatim; replace every example row, entry,
and narrative sentence with this project's own content from Step 2, or leave it genuinely empty
where there is nothing yet:

- `INDEX.md` — real conventions header (unchanged from the template) plus "The path forward" and
  phase tables built from Step 2's findings. A brand-new project has one phase table, not two.
- `PRIORITIES.md` — use the template's own **"Day-one initial state"** block in place of its worked
  three-section example — the template says exactly when to do this. Two of its three sections
  ("Recent sessions" empty, and the "Notes for next session" bullet) transfer as written. But its
  "Next priorities" bullet ("start the first ready task") is written for the case where INDEX is
  still empty when PRIORITIES is scaffolded — by this point in this skill's own order, Step 2
  already found real tasks and Step 3 already wrote them into INDEX, so name the actual first task
  by ID instead of the generic phrase (e.g. "Confirm the initial task list in INDEX.md looks right,
  then pick up `T101`" — pick whichever real task is unblocked, regardless of whether the scan
  classified it `ready` or `in-progress`; INDEX's own status is the source of truth, so don't repeat
  "ready" here if the row says otherwise). Set `Last updated:` to today's date.
- `DECISIONS.md` — keep the Conventions header and the `<!-- BEGIN ledger -->`/`<!-- END ledger -->`
  markers; the ledger and the body start **empty** (no `D##` rows, no entries) — a new project has
  made no decisions yet. Do not invent one to fill the space.
- `JOURNAL.md` and `ARCHIVE.md` — keep the header and the explanatory sentence; drop the example
  entry. Both start with zero entries.
- `tracker/detail/T###_<slug>.md` — one per initial task, built from `detail_template.md`'s
  structure (Current state head, Goal, Sub-steps, Acceptance criteria, Stopping criteria, Notes,
  Progress log). Leave `## Stopping criteria` and `## Progress log` empty at scaffold time — per the
  template, stopping criteria are written when autonomy is granted for that task, not guessed at
  creation, and there is no session narrative yet to log. A brand-new project has made no decisions
  yet (see the `DECISIONS.md` bullet above), so no `tracker/detail/D##_<slug>.md` file is created
  at scaffold time either — when the first decision is ratified, build one from
  `decision_detail_template.md`, e.g. `tracker/detail/D01_<slug>.md`, in this same `tracker/detail/`
  folder, alongside the `T###_<slug>.md` files above.

## Step 4 — ask the remaining preferences, then generate the CLAUDE.md block

Two more one-time choices belong in `## Project settings`, alongside the git layout recorded in
Step 1. Ask both before writing the block.

**Code-commit preference.** Ask how `tracker-close` should treat code changes at session end — the
`tracker/`-separate-from-code rule itself is never optional (Step 5 below, and `tracker-close` Duty
5); this only decides whether code also gets committed:
- **auto** — close commits code changes too, as a **second, separate** commit from the `tracker/`
  commit. **This is the default if the user expresses no preference.**
- **ask** — close asks each time whether to commit code changes.
- **never** — close leaves code alone, as today.

**Working relationship (optional).** Offer, don't push, a short block covering: the project's domain
and what you're helping with; where the user's judgment beats yours and you should defer; where you
should challenge or flag rather than comply; what to escalate rather than decide alone. **This is
deliberately not a persona — never claim expert-level or superior knowledge; asserting expertise
mainly raises confidence, and confidently-wrong is the failure this whole system exists to fight.**
Offer this fillable default, capped at 80 words, for the user to edit or skip entirely:

> You are helping with an academic research project in \<domain>. Work as a collaborator, not an
> assistant: say when you are unsure, flag reasoning you think is wrong rather than going along with
> it, and ask before acting on an ambiguous instruction. The user's domain judgment in \<areas> is
> better than yours — defer there and check rather than assume. Escalate anything that changes the
> project's direction.

Skipping this section entirely is fine.

**Generate the block, in two parts, in order.** Read `references/claude_md_block.md`. First, copy
its `<!-- BEGIN tracker` line through its `<!-- END tracker -->` line, inclusive, unedited — it is
generated from `references/invariants.md` and regenerated the same way later by `tracker-audit`.
Second, write its `## Project settings` section, filled in with this project's actual answers in
place of the reference file's placeholders, **after** `<!-- END tracker -->`, never inside it — kept
out of the generated region precisely so a later regeneration can never overwrite a choice this
project's user made once and that nothing can re-derive:

- **Git layout bullet:** the letter chosen in Step 1 plus its recorded one-line reminder — omit this
  bullet entirely if the project was never in a sync folder (there was no question to answer).
- **Code-commit bullet:** `auto`, `ask`, or `never`, as just chosen.
- **Working-relationship bullet:** the filled-in or edited text, or omit the bullet entirely if
  skipped.

**Matching rule (see `claude_md_block.md`'s own header note): a CLAUDE.md has the block if some line
starts with `<!-- BEGIN tracker` — a prefix match. Never grep for the byte-exact string
`<!-- BEGIN tracker -->`; the shipped BEGIN line carries a parenthetical after it and that exact
string never appears in an installed block.**

- **If `CLAUDE.md` does not exist at the project root:** create it containing exactly the block, then
  `## Project settings` right after `<!-- END tracker -->`.
- **If `CLAUDE.md` exists and no line starts with `<!-- BEGIN tracker`:** append the block, then
  `## Project settings`, to the end of the file, separated from existing content by a blank line.
- **If a line already starts with `<!-- BEGIN tracker`:** this should not happen at setup time (Step
  0 would have already handed off), but if it does, stop and hand off to `tracker-audit` rather than
  writing a second block.

**Locate `## Project settings` by heading name, never by "whatever comes after END."** A project's
`CLAUDE.md` may carry its own sections after where this block lands — the user's own notes, other
tooling's config — and setup must never assume everything past `<!-- END tracker -->` belongs to it.
If a line reading exactly `## Project settings` already exists, write into that section in place. Otherwise
insert the new `## Project settings` section immediately after `<!-- END tracker -->`, ahead of
anything else already there, leaving all of it untouched.

## Step 5 — initial commit of `tracker/` alone

**If git layout D was chosen in Step 1 (no git for this project), skip this step entirely** — there
is no git to stage or commit to. Tell the user plainly that `tracker/` and `CLAUDE.md` exist on disk
but are not under version control, and that sync history is the only history from here on. Nothing
in this step applies; the project is otherwise fully set up.

Otherwise, stage only what this skill created — nothing from the project's pre-existing code:

```
git add tracker/ CLAUDE.md
```

Before committing, sanity-check what's staged: `git diff --cached --stat` (file count) and a rough
size check (`git diff --cached --stat` also shows this, or `du -sh tracker/`). Everything staged
here is hand-written markdown produced in Steps 2–4, so the count should match what you created
(five `tracker/*.md` files, one or more `tracker/detail/*.md` files, one `CLAUDE.md`) and the total
size should be a few tens of KB at most. If the count or size is a surprise — something unrelated
got staged — stop and investigate before committing; do not commit through an unexplained surprise.

Then commit:

```
git commit -m "Set up tracker/: scaffold task and decision system"
```

This is the **only** commit this skill makes. It never commits the project's existing code — that
stays exactly as git left it (untracked, or already committed, depending on Step 1), for the user
to commit separately whenever they choose.

## What this leaves behind

After this skill finishes, the project has:

- A `tracker/` directory that is now the single source of truth for project state, and a
  `CLAUDE.md` block that puts the standing rules — the I2 write modes, edit-in-place, scope tags,
  demote-before-add, `★` reserved for supersession/scope, the date-stamp refresh, stopping criteria
  before unsupervised work, committing `tracker/` separately from code — always in context, every
  session, without anyone having to invoke anything.
- A `## Project settings` section right after that block, holding this project's own one-time
  choices — git layout, code-commit preference, and, if the user wanted it, a short
  working-relationship note — placed outside the generated region so regeneration can never touch it.
- Everything else about `tracker/` is **invoked, not standing**: `tracker-setup` (this skill, once),
  `tracker-close` (every session), `tracker-audit` (periodic), `tracker-supersede` (at a pivot). None
  of them run themselves; an agent has to call them.
- One judgment this skill and its siblings never make on their own: **declaring a pivot** — that
  some approach, model, or plan is now dead and something else is now current. `tracker-audit` can
  surface a candidate and ask; only the human decides yes.
