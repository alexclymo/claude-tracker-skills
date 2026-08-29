# Commuting Time and Job Satisfaction — example project

> **This is a fictional, non-working example** bundled with the `claude-tracker-skills` repo to show
> the `tracker/` system in use. No data, code, or paper here is real or runnable. Start reading at
> `tracker/INDEX.md`.

An empirical panel study of whether longer commutes predict lower job satisfaction, using the
(invented) National Household Panel Survey (NHPS).

<!-- BEGIN tracker (generated from tracker-setup/references/invariants.md — regenerate with tracker-audit) -->
## Task System

*Tracker format: `tracker-format: 2`. If a skill you are running targets a newer format than this,
the tracker predates it — see the migration rule below.*

This project tracks tasks and decisions in `tracker/`, not in this file and not in Claude Code's
in-session task tools. At the start of every session, read, in order:

1. `tracker/INDEX.md` — what exists and its current status.
2. `tracker/PRIORITIES.md` — what to do next.
3. `tracker/DECISIONS.md` — the decisions ledger (one line per decision). Open a decision's
   `tracker/detail/D##_*.md` only when its ruling is relevant to the task at hand.

`tracker/` is the single source of truth for project state. Claude Code's built-in `TaskCreate` /
`TaskList` and other in-session task tools are scoped to this conversation only — they do not
substitute for `tracker/`, and nothing written there persists to the next session.

### Standing rules

- **Three write modes (I2), and every file is written only in its declared mode** — see line 3 of
  each file. `overwrite-only` files are rewritten in place; `append-only` files are appended to,
  never rewritten; `headed-append` files pair a small current head with an appended body, and the
  head must be refreshed in the same operation that grows the body.
- **Edit in place.** A correction replaces the claim where it stands; it never stacks a newer claim
  above an older, uncorrected one.
- **Anchor by symbol, section, or function name — never `file:line`.** Line numbers drift on the
  next edit and silently point at whatever now sits there; a name doesn't (I7).
- **Scope-tag new facts that could apply to more than one context** — a second model, dataset, or
  approach — with an explicit tag like `[model-B]` or `[regime: cold]` (I4).
- **Demote before you add.** If a state file is at or near its cap, move something out — to a
  detail file, `JOURNAL.md`, or `ARCHIVE.md` — before adding new content (I5).
- **Do not restructure the tracker mid-task on a format mismatch.** If the tracker's
  `tracker-format` is older than the skill you are running expects — a block with no `tracker-format`
  line at all is v1 — read it as-is and finish the task. Add a one-line migration suggestion to the
  session handoff (PRIORITIES → *Notes for next session*); let the human run the migration
  deliberately (`tracker-audit` offers it). Never convert structure while doing unrelated work.
- **`★` is reserved for supersession and scope banners only** — never for findings.
- **Refresh the date stamp** whenever you rewrite `PRIORITIES.md` or a `headed-append` head.
- **Before working unsupervised on a task, write its stopping criteria into that task's detail
  file first** — success condition, bailout condition, wall-clock cap. Autonomy without a written
  stopping point is not licensed.
- **Commit `tracker/` separately from code.** Never mix a task-doc update into a code commit.

### Session end

Run the `tracker-close` skill before ending a session. It confirms or demotes every `in-progress`
task, writes session state, checks its own edits against the invariants, recommends
`tracker-audit` or `tracker-supersede` when warranted, and commits `tracker/` (per this project's
git layout below — one layout skips commits entirely).
<!-- END tracker -->

## Project settings

Chosen once at setup, not generated from the invariants above — this project's own preferences, not
universal rules. This section sits after `<!-- END tracker -->`, so regenerating the block above
never touches it.

- **Code changes on close:** ask — `tracker-close` asks each time whether to commit code changes.
  (`tracker/` and code are always committed separately.)
- **Working relationship:** You are helping with an empirical economics paper on commuting and job
  satisfaction. Work as a collaborator, not an assistant: say when you are unsure, flag reasoning you
  think is wrong rather than going along with it, and ask before acting on an ambiguous instruction.
  The user's judgment on econometric specification and data provenance is better than yours — defer
  there and check rather than assume. Escalate anything that changes the paper's direction.

---

# Project notes

Everything below is ordinary `CLAUDE.md` material and has nothing to do with the tracker system —
it's the standing "how we work here" context every session should have. The tracker block above
governs task and decision *state*; these sections are the project's own conventions. In a real
project this is where your notes live; the content here is plausible but fake.

## Tech stack

- **Language:** Python 3.11, managed with `uv` — `uv sync` to install, `uv run` to execute.
- **Analysis:** `pandas` for wrangling, `statsmodels` for the pooled OLS baseline, `linearmodels`
  for the fixed-effects specification.
- **Paper:** LaTeX, built with `latexmk`. Regression tables are written out by the analysis code as
  `.tex` fragments and `\input` into `tex/main.tex` — never typed by hand.
- **Data:** the NHPS extract is not in the repo (it's gitignored); it lives under `data/`, obtained
  per `T002`.

## Running things

- **Install:** `uv sync`
- **Run the pipeline:** `uv run python code/main.py` — a placeholder here; the real stages are
  `load → validate → build → estimate` (see the module docstring).
- **Build the paper:** `cd tex && latexmk -pdf main.tex`
- **Never commit** anything under `data/` or any built PDF — both are gitignored, and raw data must
  not leave the machine.

## Code style

- Format with `ruff format` and lint with `ruff check` before committing; CI runs both.
- Type-hint public functions. Keep pipeline stages pure where practical: data in, data out, no hidden
  global state.
- One stage per function, named for its tracker task where there's a mapping (see `code/main.py`).
- No hard-coded paths or magic numbers in the middle of a function — read them from a config.

## Writing style

- US spelling, Oxford comma.
- In prose, refer to specifications by name ("the pooled baseline", "the fixed-effects spec"), not by
  table number — numbers move when tables are regenerated.
- If a reported number changes, re-run the estimation task (`T201`); do not edit the generated
  `.tex`.
- Keep the *reasoning* behind a modelling choice in the tracker (`DECISIONS.md`), not buried in a
  paper footnote — the footnote can cite it once it's settled.
