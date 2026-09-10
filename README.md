# Claude Code Task Tracker System

**Author:** Alex Clymo

This repo contains a lightweight task tracker system for using Claude Code on academic projects. The
idea is to let Claude Code work more effectively and autonomously, to preserve key information across
sessions, and to keep a simple to-do list that tracks tasks. The system is deliberately simple, built
around markdown files in a `tracker/` folder, and sized for a typical academic project containing both
coding and writing work.

Once set up, you can just talk to your agent as usual and it will read and update the task docs for
you. Starting a session is as simple as saying "Hey! Let's pick up the next task", or "Hey! What
should we work on next?", or "Hi! I'd like to set up a new task". You can talk to your agent in plain
English throughout, but the package also includes three skills that help maintain the quality of the
information stored in the tracker.

I have been using and refining this system across a few of my own projects over the last few months.
It works pretty well and seems about the right size for academic work. Recently, as some projects have
been worked on for longer and longer, the task docs have tended to get too large or full of stale or
conflicting information. That is what the new skills are for, and it is certainly the area where this
system could use the most experimentation and improvement.

Very much a work in progress — I'd be delighted if anyone uses or improves it, and comments are very
welcome.

## The problem and this system's solution

Claude Code sessions are stateless. An open problem is how to carry information across them. This
system is a modest attempt to solve that in the context of a typical academic project.

At heart it is a simple to-do list stored in `tracker/INDEX.md`. Each active task gets its own
markdown file holding the information needed to keep working on it, loaded and updated by the agent
whenever that task is being worked on. Two short master files hold the list of tasks and the current
priorities; decisions made along the way are noted in the task they belong to. These are read at the
start of each session, via a small set of standing instructions placed in `CLAUDE.md`.

A nice side effect is that the system organises your work and thoughts — which can get hard when
you're working with AI agents that move quickly, sometimes across several projects at once. The
to-do list tracks your tasks, and an open task stays open until you mark it completed.

To pass information on to the next session, you simply tell the agent to update the documents before
closing. That can be an ordinary sentence in chat, or the dedicated `tracker-close` skill.

Notes like these rot in predictable ways. A correction gets appended below the stale claim it
corrects, so the wrong version is still what a reader sees first. A summary at the top of a file stops
matching the log beneath it. Keeping that rot in check is most of what the three skills do.

Finally, the system has the agent commit its work with git, so that anything committed can be rolled
back. Commits land at session close, so the safety net is per session, not per edit. The agent drives
git, so day to day you need little git knowledge; recovering from a bad commit is where some fluency
helps. Git is optional but highly recommended.

## Who this is for

People running long, multi-session Claude Code projects — research projects, papers, codebases
worked on over months. The target audience is other academics, but the framework is general. It is
overkill for a weekend project, where the scaffolding costs more than it returns. It is also
too basic for larger or more advanced software projects, which will likely want something more
capable than a folder of markdown files.

## What it is for, and what it isn't

The point of this system is to let Claude Code work more autonomously while you stay firmly in the
steering seat. It is not for one-shotting or vibe-coding academic work. Agents are not good enough at
frontier economics for that, and a tracker that has gone stale will quietly lead one off course
rather than keep it on track. You still read the code, still decide what counts as a result, and
still choose what gets written down.

[`WORKING-WITH-CLAUDE.md`](WORKING-WITH-CLAUDE.md) is the longer version of that argument: notes from
using Claude Code on my own research on what it does well, what you can hand over, what you have to
keep owning yourself, and where this tracker helps or hurts.

## Typical workflow

To get to work, start a session as you normally would: "Hey! Let's work on the next task", or "Hey!
Let's work on T11". The agent reads the tracker, tells you where things stand, and picks up from
there.

Then do the work — normal conversation, no special commands.

At the end, close the session off. Either invoke `tracker-close`, or just say something like "Thanks!
That was a great session, let's close it off here." The agent writes the session's state back into
`tracker/` so the next one can pick it up.

To browse your to-do list, just look at `tracker/INDEX.md` — it is human-readable. It's best not to
edit it yourself; leave that to Claude.

You can read any of the files in the `tracker/` folder to see what information the system has stored.
Then, periodically — whenever the docs start to feel stale — run `tracker-audit` to bring them back
into line. It reports what it found and walks you through the fixes five questions at a time.

## Install

Clone this repo and copy the skills to your user-level skills directory if you want them available
across all your projects:

```bash
git clone https://github.com/alexclymo/claude-tracker-skills.git
cp -r claude-tracker-skills/skills/* ~/.claude/skills/
```

Or copy them into a single project's `.claude/skills/` instead, if you would rather keep them scoped
to one project.

If you installed them at the user level and work from more than one computer, install them on each —
that directory is per-machine and doesn't sync. And if the project you're tracking already lives in a
cloud-synced folder (Dropbox, iCloud, …) that you open from several machines, read [the git caveat in
`DESIGN.md`](DESIGN.md#git-and-the-cloud-sync-caveat) before running `tracker-setup` — the git layout
there needs a deliberate choice.

**Copy all three skill directories, not just the one you think you need:** `tracker-close` and
`tracker-audit` read their templates and checks from `tracker-setup/references/` at runtime.

**Upgrading from v2:** delete the old skill directories first — `rm -r ~/.claude/skills/tracker-*`
(or the project-local equivalent) — then copy, so that `tracker-supersede` and the retired
reference files go with them.

**What the skills do to git without asking:** `tracker-setup` makes one commit of `tracker/` and
`CLAUDE.md`; `tracker-close` commits `tracker/` at every session end and pushes when the project's
recorded git layout says to. Only history rewrites ever prompt. Decide whether you want that before
installing.

Then just say, in a Claude Code session at your project's root: **"set up a tracker for this
project."** No slash command needed — each skill triggers on a handful of natural phrasings; see its
own description for the exact ones.

## The three skills

**`tracker-setup`** — run once per project. Checks for a git repo and initialises one if needed (asking
how to lay things out if the project lives in a cloud-sync folder, since that changes the safe
choice), scaffolds `tracker/` from templates, writes a `CLAUDE.md` standing-rules block, and populates
an initial task list from the project's code base, git history, and TODOs.

**`tracker-close`** — run at the end of every session that touched a tracked project. Sets the
status of the tasks the session worked, writes the session's state into `tracker/`, checks the head
dates, the log positions, and the PRIORITIES word cap, and commits. It is quiet by design — at most
eight lines of output, the last of which is what to pick up next session.

**`tracker-audit`** — run by hand, when the docs feel stale or on whatever cadence you like. Reads
what agents actually load — `INDEX.md`, `PRIORITIES.md`, the `CLAUDE.md` block, and the detail files
of open tasks — reports at most ten findings ranked by how likely each is to cause a wrong decision,
and walks you through the fixes. It also offers to migrate an older tracker format when it finds one.

## What it creates

```
tracker/
├── INDEX.md           what exists and its status
├── PRIORITIES.md      what to do next, capped and reconciled every session
├── JOURNAL.md         rolled-off session history — never loaded, never deleted
├── ARCHIVE.md         closed phases moved out of INDEX — same idea
└── detail/
    └── T###_*.md      one file per task: current state + dated progress log
```

Every file above declares, on its own third line, how it may be written — rewritten in place,
appended to only, or a current-state head paired with an appended body — and every skill here writes
it only that way. That's the core of the design; `DESIGN.md` explains why. There is no decisions
file: a choice made while working a task is a note in that task's file, and a rule for the whole
project is a line in `CLAUDE.md`.

To see what that looks like filled in, [`example/`](example/) is a worked example: a fictional
empirical-economics paper caught mid-stream, with a complete `tracker/` beside it. Nothing in it
runs — the folder exists so you can read a real tracker before scaffolding your own.

## Not Claude Code's built-in task tools

This is unrelated to Claude Code's in-session task tools, `TaskCreate` / `TaskList`. Those are scoped
to a single conversation and nothing written there survives past it. `tracker/` is a durable,
git-tracked record meant to outlive any one session — which is why these skills are named
`tracker-*` rather than `task-*`, specifically to avoid that collision.

## Design

[`DESIGN.md`](DESIGN.md) walks through the structure of each file, the three write modes, and the one
job the whole thing serves.

## Status

The basic tracker system has been in daily use on my own projects for several months and is nice to
work with: Claude uses it naturally to store what matters, and you can pick up tasks without
re-explaining them every session.

The skills arrived in July 2026 with format v2. They were made because the original system was
suffering from bloated and stale task documents: context was getting overloaded (tens of thousands
of tokens loaded just from the task docs, degrading agent performance), and stale, conflicting
information was being quietly loaded into context, causing agents to make mistakes or repeat ones I
thought I'd corrected. I have tightened the rules on how large the task files can grow, and
introduced these skills to periodically force myself and the agent to go through and tidy up the
documents. Format v3 (September 2026) cut the ceremony back after two months of daily use of those
skills: a quieter close, a smaller audit, and no decisions ledger.

[`CHANGELOG.md`](CHANGELOG.md) records what has changed and when. The version numbers there are
tracker *format* versions rather than a release count, so the first public release was v2 and the
current format is v3.
