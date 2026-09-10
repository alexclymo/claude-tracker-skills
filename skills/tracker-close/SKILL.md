---
name: tracker-close
description: Use when ending a session, closing out, wrapping up and updating the task docs, or at session end — triggers like "end the session", "close out", "wrap up and update the task docs", "let's close for today", "session end". Writes the session's state into tracker/ (statuses, progress logs with refreshed heads, PRIORITIES), commits tracker/ separately from code, and ends with what to pick up next session. Quiet by design: at most eight lines of output. Manages project task *documents* on disk, not Claude Code's in-session task tools (TaskCreate/TaskList), which never persist.
---

# tracker-close

Writes the session's state into `tracker/` and commits it. It never refuses to close: it ends in a
commit, or in one plain sentence saying why there is none. Output is at most eight lines — what
changed, one drift sentence if any, the commit, and what to pick up next. Report failures only;
never print numbers, check results, or files that passed.

The rules you are keeping are in the project's `CLAUDE.md` block. The templates and the checks this
skill uses are in `../tracker-setup/references/`, relative to this skill's own directory.

## 1. Statuses

Set the INDEX `Status` of every task worked or discussed this session to what is now true. Name any
other `in-progress` rows in one line without opening their files — "Still in-progress, untouched
today: T5, T9" — so the human can demote one by replying. Rows that have gone quiet for many
sessions are `tracker-audit`'s job, not yours.

## 2. Write

For each task worked this session, in one edit of its `detail/T###_*.md`: append a Progress-log
entry `### YYYY-MM-DD — <summary>` at the end of the file, and rewrite `## Current state` so it says
where the task now stands, with `*Refreshed: <today>*`. Narrative goes in the log only, never into
INDEX or PRIORITIES.

Rewrite `PRIORITIES.md`: `Notes for next session` and `Next priorities` to where things now stand,
≤30 words per bullet, each naming a task ID or detail file; add this session at the top of
`Recent sessions` as `- **YYYY-MM-DD** — <summary>`; if that makes six entries, move the oldest to
`JOURNAL.md` as `### YYYY-MM-DD — <one line>` in the same edit; delete the day-one placeholder if it
is still there; refresh `*Last updated:*`.

Touch INDEX's `## The path forward` only if a status changed, and then only the bullets that
changed. Set `R:Human` / `R:Claude` to `ok` for rows a party reviewed this session.

## 3. Check

Only the files you touched, and only speak if something fails (from
`../tracker-setup/references/checks.md`):

```bash
# per detail file touched (F):
grep -H '^\*Refreshed:' "$F"        # today's date
grep '^## ' "$F" | tail -1          # "## Progress log"
wc -w tracker/PRIORITIES.md         # ≤ 2,000
```

These are your own writes, so fix a failure now: refresh the head, move anything that landed below
the log back above it, demote a PRIORITIES bullet into a detail file. Fix it and say nothing.
Nothing else is checked.

## 4. Drift

If, while doing the above, you saw a concrete contradiction that you are not fixing — a PRIORITIES
bullet saying "start T7" where INDEX has `T7` `done`; a row `blocked` on a task that is `abandoned`;
a `## Current state` that plainly contradicts the log beneath it — say so in one sentence naming the
file, and suggest `tracker-audit`. Report what you noticed in passing; do not go looking. Never on
size, and never as a general "the docs could use a look". If you saw nothing, say nothing.

## 5. Commit

Read `## Project settings` in `CLAUDE.md`. If the git layout is D, say in one sentence that the
tracker's history is the sync folder's and stop here. If `tracker/` is gitignored, say the same and
skip to code below. Otherwise:

```bash
git add tracker/ && git commit -m "<one line: what this session's tracker changes were>"
```

Then code, per the recorded preference: `auto` — commit changes outside `tracker/` as a second,
separate commit; `ask` — ask once; `never` — leave them. Never fold code into the tracker commit.
Push if the layout is B, C, or unset and a remote exists; never for layout A. A plain commit or push
needs no permission; only history rewrites do.

## Output

```
Closed. T112 in-progress → progress logged, head refreshed. T108 in-progress, untouched today.
Wrote detail/T112_tracker_v3.md, PRIORITIES.md, INDEX.md.
Drift: PRIORITIES says "start T109" but INDEX marks it done — worth a tracker-audit.
Committed tracker/ as a1b2c3d. Code left uncommitted per settings.
Next session: pick up T112 — write the implementation plan from the approved spec.
```

The drift line appears only when there is drift. The last line is always the next-session pointer,
taken from what PRIORITIES now says; if nothing is queued, say so.
