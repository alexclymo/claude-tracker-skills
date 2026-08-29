# Worked example — the tracker system on a fake project

A self-contained, **non-working** illustration of the `tracker/` task-and-decision system, applied
to a fictional empirical-economics paper. Nothing here runs: `code/main.py` raises
`NotImplementedError` and `tex/main.tex` is a skeleton that isn't meant to compile into a real
document. The point of the folder is the `tracker/` directory and the `CLAUDE.md` standing-rules
block beside it.

## What the fake project is

*Commuting Time and Job Satisfaction* — a panel study asking whether longer commutes predict lower
job satisfaction, using the invented National Household Panel Survey (NHPS). It is deliberately
caught mid-stream: the data pipeline is nearly finished, estimation hasn't started, and the paper is
still a skeleton. That's what makes the tracker interesting to look at.

## How to read it

Read in the same order a real session would (`CLAUDE.md` spells this out):

1. `tracker/INDEX.md` — the map: two live phases plus one archived, every task and its status.
2. `tracker/PRIORITIES.md` — what the next session would pick up, and why.
3. `tracker/DECISIONS.md` — the two decisions on record; open a `detail/D0*.md` for the reasoning.

Three things are worth noticing, because they are the format's whole reason to exist:

- **`D01` was revised in place.** The ledger shows only the *current* backward-fill ruling. The
  retired forward-fill ruling lives in `detail/D01_imputation_rule.md`'s `## History`, and `T101`'s
  progress log still records the forward-fill run that actually happened. Current truth on top,
  history preserved — never a stack of contradicting claims.
- **`D02` is scope-tagged `[spec: fixed-effects]`.** It binds only the fixed-effects robustness
  specification, not the pooled baseline — see the `★ SCOPE` banner in its detail file. A fact that
  isn't universal is tagged so nobody over-applies it.
- **`T103` carries filled stopping criteria** because it's the in-progress task someone might work
  on unsupervised; the not-yet-started tasks leave that section empty, as the format intends.

## Layout

```
example/
  README.md          this file
  CLAUDE.md          standing-rules block + this project's settings (loaded every session)
  tex/main.tex       skeleton paper — placeholder, does not compile to real results
  code/main.py       skeleton pipeline — placeholder, raises NotImplementedError
  tracker/
    INDEX.md         the map (status of everything)
    PRIORITIES.md    what to do next
    DECISIONS.md     the decisions ledger
    JOURNAL.md       rolled-off session history
    ARCHIVE.md       closed-phase tables
    detail/          one file per task (T###) and per decision (D##)
```

Everything here is fictional and safe to read, copy, or adapt.
