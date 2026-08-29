---
name: tracker-close
description: Use when ending a session, closing out, wrapping up and updating the task docs, or at session end — triggers like "end the session", "close out", "wrap up and update the task docs", "let's close for today", "session end". Confirms or demotes in-progress work, writes the session's state into tracker/, compliance-checks its own edits against the invariants and the mechanical size/consistency checks, recommends tracker-audit or tracker-supersede when warranted, and commits tracker/ separately from code. Manages project task *documents* on disk, not Claude Code's in-session task tools (TaskCreate/TaskList) — those are scoped to one conversation and never persist; this skill closes out the durable, git-tracked record instead.
---

# tracker-close

Runs at the end of every session that touched a `tracker/`-managed project. It is the highest-value
skill in the collection precisely because it runs every time: every session either preserves the
invariants in `tracker/INDEX.md`'s conventions header and `tracker-setup/references/invariants.md`
(read from the installed path, `~/.claude/skills/tracker-setup/references/invariants.md`, if you
need the full rationale behind a check below) or it is where drift starts.

This document is self-contained for execution: it tells you what to check and in what order, and
reproduces the mechanical commands literally so you never have to go find them elsewhere — except
the six aggregate checks in Duty 3, which live in one shared file with `tracker-audit` so the two
can't drift apart on them again (that drift is how they diverged in the first release).

## Close never refuses to close

**This is the rule everything else in this document serves.** A skill that can block the end of a
session is hostile, and a hostile skill gets bypassed — at which point it protects nothing, because
nobody runs it. `tracker-close` never stops short of committing. When it finds a problem:

- If the problem is in something **this session touched**, fix it before committing — that is Duty
  3.
- If the problem is in something **this session did not touch** — pre-existing bloat, a
  contradiction it didn't create, a stale date stamp from three sessions ago — it does not fix it
  and it does not block on it. It **reports** the problem and **recommends** `tracker-audit` or
  `tracker-supersede` by name, with a specific reason. That is Duty 4. It does not run either skill
  itself; recommending is as far as this skill's authority goes.

Either way, Duty 5 always runs — even on a project set up with no git at all, where it has nothing to
commit to. There is no exit path from this document that ends without either a commit or an explicit,
plain statement of why not.

## Duty 1 — Confirm or demote every `in-progress` row (I6)

Open `tracker/INDEX.md` and list every row currently marked `in-progress` across all phase tables.

**Any number of these rows may legitimately be `in-progress` at once.** Parallel work across
several tasks is normal, and a task may correctly stay in flight across many sessions — this duty
is never a headcount and never a target to bring to zero. What I6 forbids is a specific thing: an
`in-progress` row that nobody looked at this session. So for **each** `in-progress` row, one of two
things must happen, and it must happen for every row, not just the ones this session worked on:

1. **Confirm it live.** This session's context (the conversation, `git diff`/`git log` since the
   last close, and the task's detail-file `## Current state`) shows the task is still being worked
   and the detail file's current-state claim still holds. Leave the INDEX status as `in-progress`.
   The confirmation is evidenced by Duty 2's write — either a fresh Progress-log entry that
   describes work **on that task's own goal**, not merely any entry that happens to land in that
   task's file (an unrelated edit logged into the same detail file is not evidence the task itself
   moved), or, if the task wasn't advanced this session but is still genuinely active — paused for
   this session only, not abandoned — an explicit one-line note in `PRIORITIES.md`'s `Notes for next
   session` that says so and gives the reason. Either form is a real, written act of re-confirming,
   not silence read as consent. An `in-progress` row with neither is not confirmed — demote it.
2. **Demote it.** If the task wasn't worked this session and nothing in the detail file or
   conversation affirms it's still active, change its INDEX status to whichever is true:
   - `ready` — unblocked, simply paused.
   - `blocked` — a dependency now stands in the way that didn't before.
   - `abandoned` — no longer being pursued (kept for history, never deleted).
   Update the task's detail-file `## Current state` status line to match in the same pass (Duty 2
   folds this in — don't write INDEX now and the detail head later).

Also check the reverse direction while you're in INDEX: a task `blocked` on a dependency that is
itself `abandoned` or superseded is a dead dependency (I6) — fix the `Depends` value or the status,
whichever is true, rather than leaving a block on something that will never unblock it.

Do this duty **before** Duty 2's broader write pass, since demotions here change what Duty 2 needs
to write.

## Duty 2 — Write state

With Duty 1's statuses decided, write everything this session changed. All of the following are one
pass, not independent edits made at different times:

- **INDEX statuses and review columns.** Apply Duty 1's confirmations/demotions. Update `R:Human` /
  `R:Claude` to `ok` for any row a party reviewed this session; leave `—` otherwise.
- **Session narrative into the relevant detail file's Progress log, at EOF.** For every task worked
  this session, append one entry under `## Progress log` — never anywhere else in the file — headed
  `### YYYY-MM-DD — <session summary>`. Progress-log entries are the narrative; do not also write
  the narrative into PRIORITIES or INDEX (I1 — one home per fact).
- **Rewrite `PRIORITIES.md`.** Update `Notes for next session` and `Next priorities` to reflect
  where things now stand; both must stay ≤30 words per bullet and link to a `D##`, detail file, or
  task ID. Then update `Recent sessions`: it is a fixed-size window of **at most 5** entries,
  newest first, format `- **YYYY-MM-DD** — <summary, links to what changed>`. Add this session's
  entry at the top. **If this pushes the window past 5, remove the oldest (bottom) entry from
  `Recent sessions` and append it to `JOURNAL.md` as `### YYYY-MM-DD — <one line>` in the same edit
  that adds the new entry** — never add now and prune later. **If `Recent sessions` still holds the
  day-one placeholder line (`(empty — the first session's summary lands here at the next close.)`),
  delete it in this same edit** — it is not a real entry and never counts toward the 5-entry window.
  This is the only way `PRIORITIES.md` is ever written; there is no separate "cleanup" step. Refresh
  the `*Last updated: YYYY-MM-DD*` stamp.
- **Refresh the head of every headed-append file whose body grew.** Two kinds exist:
  - `tracker/detail/T###_*.md` — if you appended to `## Progress log`, rewrite that file's
    `## Current state` block in the same pass and set `*Refreshed: YYYY-MM-DD*` to today. A
    Progress-log entry with a stale `Refreshed:` date is the exact failure mode I2 and I8 exist to
    prevent: appending feels like updating, so the head silently stops being current.
  - `tracker/detail/D##_*.md` — if you set or revised a ruling this session, rewrite its `## Current
    ruling` head, append the retired ruling (if any) to `## History`, refresh its `Set by`, and
    overwrite the matching row's `Ruling`/`Set by` in the `DECISIONS.md` ledger in the same pass.
- **Reconcile `INDEX.md`'s "The path forward" against the tables below it.** It summarizes what the
  phase tables say, so every time the tables change, re-read the bullets against them: does each
  bullet still point at a real, current `D##` / detail file / task ID, and does it still describe
  what the tables now show? ≤10 bullets, ≤30 words each. Fix drift now — this is exactly the same
  kind of head as a detail file's `## Current state`, and drifts the same way if skipped.
- **Surface unratified decisions.** Read the `DECISIONS.md` ledger; for every row with
  `Ratified = —` (a ruling Claude set but the human has not confirmed), list it for the human at
  close: "I made or revised these decisions you haven't ratified — D##, D## — confirm any?" The
  `Set by` date shows how long each has been provisional; a long-provisional ruling is worth
  raising more insistently. On confirmation, set that row's `Ratified` to `human <today>`. Never
  auto-ratify.
- **Surface unreviewed `done` work.** The symmetric case: read `INDEX.md` and list every `done` row
  whose `R:Human` and `R:Claude` are both `—` — "these are finished but nobody has reviewed them:
  T##, T## — review any now?" Review never gates `done` (see the Review-columns convention), so this
  is a standing to-do list, not a blocker: report it and move on unless the human picks something up.
  If a project reviews nothing, say so once — "N `done` rows carry no review" — rather than naming
  them all at every close.

## Duty 3 — Compliance-check its own edits, then run the six mechanical checks

**Scope of this duty is what this session just wrote — Duty 2's edits — not the whole corpus.**
Auditing everything `tracker/` has ever accumulated is `tracker-audit`'s job, not this one's; close
checks its own work.

**First, the invariant checks, against what you just changed:**

- **I1 — one home per fact.** Did session narrative land in a detail file's Progress log, not in
  PRIORITIES or INDEX? Did any evidence table, artifact-path list, or what-was-built inventory you
  wrote land in a detail file rather than a `DECISIONS.md` entry?
- **I2 — write mode respected.** Did every edit to an overwrite-only file (`INDEX.md`,
  `PRIORITIES.md`, and the `DECISIONS.md` ledger) correct claims in place rather than stacking a new
  claim above an old one? Did every headed-append file whose body grew (see Duty 2) get its head
  refreshed in the same pass?
- **I4 — new multi-context facts scope-tagged.** Did anything you wrote this session state a
  recipe, number, or ruling that only holds for one model/regime/approach, once more than one
  exists in this project? If so, does it carry a `★ SCOPE — <tag>: ...` banner?
- **I5 — new bullets short and linked.** Every INDEX `Task` cell you touched ≤50 chars, name only.
  Every PRIORITIES bullet you wrote ≤30 words and linking to a `D##`/detail file/task ID. Every
  "path forward" bullet the same.
- **I6 — new INDEX status matches the PRIORITIES narrative.** For every row Duty 1 touched, does
  what PRIORITIES now says about that task agree with its new INDEX status? A task INDEX now calls
  `blocked` that PRIORITIES's `Next priorities` still describes as about to start is a contradiction
  you just created — fix it before committing.
- **I7 — anchors survive edits.** Did anything you wrote this session point at a `file:line`
  location instead of a symbol, section heading, or function name? A line number is wrong the moment
  the next edit shifts it; replace it with an anchor that stays true.

Fix any violation you find here yourself, now, before running the mechanical checks below.

**Then run all six mechanical checks, exactly as written in
`~/.claude/skills/tracker-setup/references/mechanical_checks.md` — the same installed path as
`invariants.md`, and the same file `tracker-audit` reads for these checks — from the project root.
For check 6, run variant 6a (the working-tree form): this duty runs before Duty 5's commit, so
6b's `git log` history read is not valid here.** That file also has the thresholds table; the
numbering below (checks 1–6) matches it exactly.

If 6a prints `CHECK 6a DEGRADED`, git cannot see `tracker/` — it is gitignored, or this is a
layout-D project with no git — and the check has fallen back to listing every detail file's
`Refreshed:` date. **Do not read that as a pass, and do not skip it.** You are the missing evidence:
Duty 2 just told you which detail files you grew this session, so check those files' dates against
today by name, and say in the close summary that check 6a ran degraded and which files you verified
by hand. A degraded 6a is the normal, expected result on those projects — not a fault to fix.

**Why aggregates, not per-item judgment (spec §7.2):** on the same real project, under the same
rules, the file-level PRIORITIES cap held completely while the per-row INDEX task-name limit failed
on 61% of rows — each individual overrun looked small and locally justified at the moment it was
written. A number you can check in one command gets respected; restraint you're trusting yourself to
exercise row-by-row does not. This is why check 1 and check 4 are word counts, not readings.

**What the six checks find splits into two different kinds of finding, with two different rules —
the distinction is not "did this session cause it," it's "is there one correct mechanical fix, or
does fixing it require judgment about what to cut, move, or split":**

- **Checks 3, 5, and 6 are write-mode completions: always finish them now, for any file this
  session's edits grew.** A ledger row with no matching `detail/D##_*.md` file (or a D-file with no
  ledger row), an append-at-EOF section that isn't the file's last section (`## Progress log` in a
  task file, `## History` in a decision file), or a head that wasn't refreshed
  when its body grew each have exactly one correct outcome — add the missing row, move the
  misplaced content back above that final section, rewrite the head to match. There's no half-written
  version of a headed-append file that's fine to leave for later; finish the write, however the gap
  arose. **But this is still scoped to files Duty 2 touched this session** (per this duty's opening
  scope rule) — if any of these checks turn
  up the same problem in a file this session did not grow (a different detail file with a
  long-stale head, say), leave it alone and send it to Duty 4 instead; fixing a file you didn't
  touch is corpus work, not self-compliance.
- **Checks 1, 2 (the column-total reading), and 4 are size caps, not write-mode failures — close
  never fixes these itself, no matter when the bulk arrived, including if it landed this very
  session.** `INDEX.md` is capped on its *prose* (non-table lines) at ~800 words; its *total* word
  count (prose plus table rows) passing ~5,000 words is not a hard fail — it *suggests* archiving
  closed phases to `ARCHIVE.md`. `PRIORITIES.md` stays a flat ≤2,000-word cap. Either overage, a
  detail file over the 3,000/5,000-word thresholds, or Task-column characters accumulated across
  many rows, all require deciding *what to cut, move, or split* — a corpus-level judgment this
  duty's authority doesn't extend to. A 5,000-word padding added in this very session is still not
  this duty's to trim: the size of the needed fix, not its age, is what puts it out of scope. Report
  the number and hand it to Duty 4. The one exception is check 2's **per-row** reading of a single
  cell you personally wrote this session that's over 50 characters — that's an I5 compliance
  violation on your own write, already covered above, and you fix your own cell the same as any
  other compliance issue.

## Duty 4 — Escalation judgment

Report, plainly, the size of every tracker file this session touched, plus the six mechanical
checks' headline numbers even for files not touched (so the report is a snapshot, not just a diff).
Call out anything that grew notably this session even if it's still under threshold.

Then decide whether to recommend `tracker-audit` or `tracker-supersede`. **Recommend a skill by
name with a specific reason — never a vague "the docs could use a look."** Grounds for a
recommendation include, but aren't limited to:

- A file is over one of the mechanical thresholds above — cite the file, the number, and the
  threshold.
- A `Refreshed:` date or ledger/entry mismatch you found predates this session (see Duty 3) — cite
  which file and what's stale.
- A contradiction between INDEX and PRIORITIES, or a dead dependency, that this session did not
  create and Duty 1 couldn't resolve because the ambiguity is pre-existing.
- Something significant was retired or superseded this session in conversation but the tracker
  still names it as live outside what this session touched — that's a `tracker-supersede` case, not
  a `tracker-close` fix, because sweeping every mention across the repo is out of this duty's scope.
- **Format mismatch → handoff, never fix.** If the tracker's `tracker-format` is older than this
  skill targets, do not migrate it. Write one line into PRIORITIES → *Notes for next session*:
  "Tracker is format v<N>; skills target v<M> — run a migration pass (`tracker-audit` offers it) as
  a dedicated task before major decision edits." Then close normally. A block with no
  `tracker-format` line at all is v1 (it predates the stamp) and takes this same migration handoff.

**This skill does not run `tracker-audit` or `tracker-supersede` itself.** Recommending is the
entire extent of Duty 4 — it noticed the corpus needs attention; it did not cause the problem, and
fixing corpus-wide issues is a different skill's job with a different (approval-gated) contract. If
nothing meets the bar above, say so plainly rather than manufacturing a recommendation — a
recommendation with no specific reason is exactly the vague suggestion this duty exists to avoid
making.

## Duty 5 — Commit `tracker/` (and maybe code), per this project's settings

Read the `## Project settings` section of this project's `CLAUDE.md` — it sits right after the
tracker block's `<!-- END tracker -->` line, outside the generated region — first: it records the
git layout (A/B/C/D) chosen at setup and the code-commit preference (auto/ask/never). If
the section, or a line inside it, is missing (a project set up before this section existed), treat
the git layout as unset — push if a remote exists, as below — and the code-commit preference as
`never`, today's default; that is not this duty's problem to fix, just its default to fall back on.

**If git layout is D (no git for this project): skip the rest of this duty entirely.** There is no
git to stage, commit, or push to. Say plainly, once, in the close summary that no history is being
kept for this session and the session's record lives only in the tracker files themselves. This is
not an error and not something to nag about at every close — D was a deliberate, informed choice at
setup. Duty 5 ends here for this project.

**Otherwise, stage and commit `tracker/` alone:**

```bash
git add tracker/
```

Do not stage code changes, `.gitignore` changes, or anything outside `tracker/` in this commit —
`tracker-close` never mixes a task-doc update into a code commit (I1: keeping the state files and
the code changes in separate commits is part of what keeps git history a usable narrative rather
than another place a fact gets restated). **This rule is absolute regardless of the code-commit
preference below** — "auto" means code lands in a *second, separate* commit, never folded into this
one, exactly as `tracker-supersede` already keeps a pivot's tracker and code commits apart.

```bash
git commit -m "<one line: what this session's tracker/ changes were>"
```

**Then handle uncommitted code changes per the recorded preference:**

- **auto (the default when the user expressed no preference at setup):** if `git status` shows
  uncommitted changes outside `tracker/`, stage and commit them as a second, separate commit:
  `git add <changed files outside tracker/>` then `git commit -m "<one line: what this session's
  code changes were>"`.
- **ask:** if such changes exist, ask the user now whether to commit them the same way; commit only
  on yes.
- **never:** leave any code changes uncommitted, exactly as before — not this duty's job.

**Push:**

- **Git layout A:** do not suggest pushing — a layout-A project may have no remote and no second
  machine to push for.
- **Git layout B or C, or unset (a plain, non-sync-folder repo):** push if a remote is configured, as
  before:

```bash
git remote -v
# if a remote is configured:
git push
```

**Only history-rewriting operations — force-push, rebase, amend — need the user's explicit OK
first.** A plain commit and a plain push do not; that's what makes this duty something that always
completes rather than one more thing this skill has to ask permission for.

This duty always runs, regardless of what Duties 1–4 found. A `tracker-close` session that ends
without either a commit or D's explicit no-history statement has not closed.
