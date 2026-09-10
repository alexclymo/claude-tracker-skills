---
name: tracker-audit
description: Use when the user asks to audit the task tracker, clean up the task docs, or says the docs feel stale, out of date, or contradictory — triggers like "audit the task tracker", "clean up the task docs", "the docs feel stale", "reconcile the tracker", "health check the tracker". Human-run only, never started unasked. Reads the files agents actually load — INDEX, PRIORITIES, the CLAUDE.md block, open tasks' detail files — for claims that are no longer true, reports at most ten findings ranked by what an agent would get wrong, offers a walkthrough in blocks of five questions, and fixes only what the user approves. Also offers the tracker-format migration when a project's block is older than the skill. Manages project task *documents* on disk, not Claude Code's in-session task tools (TaskCreate/TaskList), which never persist.
---

# tracker-audit

The human's periodic sweep of a `tracker/`. Report first: nothing is edited until the human
approves specific items, and this skill never runs unasked. It never declares a retirement — "X is
dead, Y is current" is the human's call; the skill can only ask. Templates and checks are in
`../tracker-setup/references/`, relative to this skill's directory.

## 1. Scope

Stop if there is no `tracker/`. Default scope is what agents load: `INDEX.md`, `PRIORITIES.md`,
the `CLAUDE.md` tracker block, any doc `CLAUDE.md` says to read every session, and the
`detail/T###_*.md` files of tasks whose INDEX status is not `done` or `abandoned`. A **deep** run,
only when asked, adds closed tasks' files and code comments. State the scope in one paragraph first.

## 2. Format

Read the stamp: `grep -o 'tracker-format: [0-9]*' CLAUDE.md`. No stamp means format 1; no block at
all is format 1 too, and the migration's step 4 adds the block. Below 3: the migration (last
section) is the first item of your report, and the rest of the audit reads the files as they are. At
3: compare the headers of INDEX (everything above `## The path forward`) and PRIORITIES (above `##
Notes for next session`) and the CLAUDE.md block (from the line starting `<!-- BEGIN tracker`
through `<!-- END tracker -->`) against the templates and `claude_md_block.md`. JOURNAL and ARCHIVE
are append-only and never regenerated. If any differ, queue a regeneration for step 6 — replace the
region, keep PRIORITIES' `*Last updated:*` date, touch nothing outside it — and say so in one line.
It is not a finding.

## 3. Three looks

Read-only. Work inline; above roughly 30,000 in-scope words, split the reading across read-only
subagents (a cheap model suffices).

- **State files against each other.** For every task PRIORITIES names, does its verb — "start",
  "pick up", "continue", "done" — match the INDEX status? Does each `## The path forward` bullet
  (≤10 of them) still describe what the tables show? Is any row `blocked` on a task that is `done`
  or `abandoned`? Is any `in-progress` task's detail-file `*Refreshed:*` date older than the
  third-newest entry in `Recent sessions`?
- **Heads against their own logs.** For each in-scope detail file, largest first: does
  `## Current state` agree with the last few Progress-log entries — status, approach, what is open,
  every file and symbol it names?
- **Docs against code.** Grep for each function, file, and symbol that an in-scope head, the
  CLAUDE.md block, or an in-scope doc asserts is current — grep only, do not read the codebase; no
  hits is a finding with a clean "true", unless it may simply have been renamed, which makes it a
  question. Any `file:line` anchor. Any approach, model, or task the docs describe as live that the
  code, the git log, or a later log entry shows was retired.

Then the three numbers from `checks.md` — PRIORITIES words (cap 2,000), INDEX words (>10,000
suggests archiving closed phases), the largest open-task detail files (>15,000 words) — mentioned
only when over threshold. Closed tasks are never measured.

## 4. Report

Ten findings at most, ranked by one question: if an agent loaded this file tomorrow and believed
it, what would it get wrong, and how likely is that? Two headings:

- **Wrong** — the doc asserts something false. Each: where (file and section name, never a line
  number); what it says; what is true and how you know, from the most primary source you can reach
  — the code, the commit, the log entry — never another tracker file alone. If you cannot establish
  what is true, you have a question, not a finding.
- **Long** — a count, with at most three files named. Nothing here is false; it costs context.

Then **Questions**, at most five: what you could not establish, and each suspected retirement as a
yes/no naming both halves with the evidence for each. A suspected retirement is never a finding;
questions beyond five wait for the next audit.

```
## Wrong (4)
1. detail/T105_… › Current state — says the extractor is unbatched. True: batched since commit
   3f2a1 (extract.py, `batch_rows`).
…
## Long (2)
- detail/T110_… 16,400 words. INDEX 10,900 words — Phase 0 is all done; archive it?
## Questions
- Is the two-stage estimator retired in favour of the joint one? T201's head prescribes two-stage;
  the last four commits to estimate.py use joint. yes / no
Shall I walk you through these in blocks of five?
```

Then stop. Nothing has been edited.

## 5. Walkthrough

On yes: take the findings and questions in ranked order, five at a time, via `AskUserQuestion`
(at most four questions per call, so a block is two calls). Each question states the item
in a line and offers **fix as proposed**, **skip**, and a free answer — the human's own ruling, or
yes/no for a retirement. Apply the block's approved items (step 6) before offering the next five.
Stop when the human says so or the list is empty.

## 6. Apply

Approved items only, each at its source, in the file's declared write mode. Correct a head or a
bullet where it stands. Set a status to what is true; repoint or clear a `Depends` that can never
clear. A **Long** item has two sanctioned fixes: archive a closed phase — its whole table moves to
`ARCHIVE.md` under `### Phase N — <name> (closed YYYY-MM-DD)`, leaving a one-line pointer in INDEX —
or move PRIORITIES content into the relevant detail file. An over-long detail file is reported, not
restructured. Nothing is deleted.

A **yes** to a retirement question is the one case that sweeps: grep the retired name and its
aliases across `tracker/`, `CLAUDE.md` and, on a deep run, code comments; mark each head or bullet
that asserts it is current with `★ SUPERSEDED by <current thing> (YYYY-MM-DD)`, optionally followed
by `: <one line>`; set rows for tasks that *are* the retired thing to `abandoned`; repoint or
abandon anything `blocked` on them; leave Progress logs and `Recent sessions` alone — they are
history. Refresh every `Refreshed:` date you touch.

Regeneration queued in step 2 is its own yes/no question, asked once after the last block or when
the walkthrough is declined, stating what the replaced region drops; apply it only on yes.

Commit `tracker/` and `CLAUDE.md` together, code comments separately, following the project's
`## Project settings` exactly as `tracker-close` does: layout D, or a gitignored tracker, skips the
commit with one sentence; push where close would (layouts B, C, or unset, with a remote).

## Migration to format 3

Offered whenever the stamp is below 3. Show this plan filled in for the project, then apply it only
on an explicit yes.

1. Copy the decisions record verbatim into `ARCHIVE.md` under
   `### Decisions (format v2, retired YYYY-MM-DD)`: the ledger table, then each `detail/D##_*.md`
   in full under `#### D## — <title>`, minus its own title line and with its headings demoted below
   the `####`. For a format-1 tracker (inline `### D##` entries, no D-files) copy `DECISIONS.md` in
   full. Then delete `DECISIONS.md` and `detail/D*.md`.
2. List every ruling that still appears to be in force and ask, per ruling: fold it into a task's
   `## Notes` as a dated note, put it in `CLAUDE.md` below the block as a project rule, or leave it
   archived.
3. Replace the INDEX and PRIORITIES headers by structure (step 2's regions; if the anchor heading is
   absent, the header is everything above the first `## ` heading) with the template headers, and
   delete the italic template note under `## The path forward` if one is there. Rewrite any INDEX or
   PRIORITIES bullet, and any section of an open task's file other than its Progress log, that cites
   a `D##` to point at the task or the archive instead, refreshing that head's date; repoint or drop
   any link to a file this migration deleted. Progress logs, `Recent sessions` and JOURNAL are
   history: leave their wording.
4. Replace the CLAUDE.md block with `claude_md_block.md`'s, which carries `tracker-format: 3`, or
   add it after the project's own text if there is none; `## Project settings` is untouched. Grep
   the rest of `CLAUDE.md` for `DECISIONS` and `D##`; report hits.
5. Commit `tracker/` and `CLAUDE.md` together, exactly as step 6 does — layout D, or a gitignored
   tracker, skips with one sentence.
