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
English throughout, but the package also includes four skills that help maintain the quality of the
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
whenever that task is being worked on. A few master files hold the list of active tasks, the current
priorities, and the decisions made along the way. These are read at the start of each session, via a
small set of standing instructions placed in `CLAUDE.md`.

A nice side effect is that the system organises your work and thoughts — which can get hard when
you're working with AI agents that move quickly, sometimes across several projects at once. The
to-do list tracks your tasks, and an open task stays open until you mark it completed.

To pass information on to the next session, you simply tell the agent to update the documents before
closing. That can be an ordinary sentence in chat, or the dedicated `tracker-close` skill.

Notes like these rot in predictable ways. A correction gets appended below the stale claim it
corrects, so the wrong version is still what a reader sees first. A decision that was only ever true
of one model gets read as universal once the project moves past it. Keeping that rot in check is most
of what the four skills do.

Finally, the system makes the agent automatically log all its work using git, so that you can always
confidently let the agent work knowing you can roll back mistakes. This is handled by the agent, so
no in-depth knowledge of how to use git is required. It is optional but highly recommended.

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
into line.

## Install

Copy the skills to your user-level skills directory if you want them available across all your
projects. Or into a single project's `.claude/skills/` instead, if you would rather keep them scoped
to one project.

If you installed them at the user level and work from more than one computer, install them on each —
that directory is per-machine and doesn't sync. And if the project you're tracking already lives in a
cloud-synced folder (Dropbox, iCloud, …) that you open from several machines, read [the git caveat in
`DESIGN.md`](DESIGN.md#git-and-the-cloud-sync-caveat) before running `tracker-setup` — the git layout
there needs a deliberate choice.

**Copy all four skill directories, not just the one you think you need.** `tracker-audit` and
`tracker-supersede` read their canonical rules from `tracker-setup/references/` at runtime rather than
carrying their own copy, and refuse to run with a clear error if that path is missing.

Then just say, in a Claude Code session at your project's root: **"set up a tracker for this
project."** No slash command needed — each skill triggers on a handful of natural phrasings; see its
own description for the exact ones.

## The four skills

**`tracker-setup`** — run once per project. Checks for a git repo and initializes one if needed (asking
how to lay things out if the project lives in a cloud-sync folder, since that changes the safe
choice), scaffolds `tracker/` from templates, writes a `CLAUDE.md` standing-rules block, and populates
an initial task list from the project's code base, git history, and TODOs.

**`tracker-close`** — run at the end of every session that touched a tracked project. Confirms or
demotes every in-progress task, writes the session's state into `tracker/`, checks its own edits for
compliance before committing, and flags anything outside what it touched by name-dropping
`tracker-audit` or `tracker-supersede`.

**`tracker-audit`** — the periodic deep sweep, run when the docs feel stale or on whatever cadence you
like. Searches the whole repo for claims that no longer match reality, reports them ranked by how
likely each is to cause a wrong decision, and fixes them only once you say yes.

**`tracker-supersede`** — run when you tell it something is retired and something else has taken its
place. Requires both names stated explicitly, then sweeps every place the retired thing is named —
statuses, the decision log, detail files, `CLAUDE.md`, code comments — marking it dead, not deleting
it.

## What it creates

```
tracker/
├── INDEX.md           what exists and its status
├── PRIORITIES.md      what to do next, capped and reconciled every session
├── DECISIONS.md       a ledger of current rulings; full rationale in detail/D##_*.md
├── JOURNAL.md         rolled-off session history — never loaded, never deleted
├── ARCHIVE.md         closed phases moved out of INDEX — same idea
└── detail/
    ├── T###_*.md      one file per task: current state + dated progress log
    └── D##_*.md       one file per decision: current ruling + history
```

Every file above declares, on its own third line, how it may be written — rewritten in place,
appended to only, or a current-state head paired with an appended body — and every skill here writes
it only that way. That's the core of the design; `DESIGN.md` explains why.

To see what that looks like filled in, [`example/`](example/) is a worked example: a fictional
empirical-economics paper caught mid-stream, with a complete `tracker/` beside it. Nothing in it
runs — the folder exists so you can read a real tracker before scaffolding your own.

## Not Claude Code's built-in task tools

This is unrelated to Claude Code's in-session task tools — `TaskCreate`/`TaskList` and
`~/.claude/tasks/`. Those are scoped to a single conversation and nothing written there survives past
it. `tracker/` is a durable, git-tracked record meant to outlive any one session — which is why these
skills are named `tracker-*` rather than `task-*`, specifically to avoid that collision.

## Design

[`DESIGN.md`](DESIGN.md) walks through the structure of each file, the three write modes, and the nine
invariants that hold the system together.

## Status

The basic tracker system is something I've been using and refining for a few months across a handful
of my own projects. It seems to work well and is nice to work with. Claude naturally uses the system
to store important information, and you can pick up tasks without having to explain every time what
you're working on.

The four skills are much newer and haven't been road-tested much yet. They were made because the
original system was suffering from bloated and stale task documents: context was getting overloaded
(tens of thousands of tokens loaded just from the task docs, degrading agent performance), and stale,
conflicting information was being quietly loaded into context, causing agents to make mistakes or
repeat ones I thought I'd corrected. I have tightened the rules on how large the task files can grow,
and introduced these skills to periodically force myself and the agent to go through and tidy up the
documents.

[`CHANGELOG.md`](CHANGELOG.md) records what has changed and when. The version numbers there are
tracker *format* versions rather than a release count, so the first public release is v2.
