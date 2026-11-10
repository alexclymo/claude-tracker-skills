# Using the tracker with other agents

The skills were written for Claude Code, but nothing in them depends on it in any deep way. They are
plain Markdown instructions, and the tracker they build is plain Markdown under git. Any agent that
can read a skill and edit files can run them.

I primarily just use Claude Code. The setup below has been built only for my own case: Codex as a
backup for when Claude is down, sharing the same projects. See [What has been
tested](#what-has-been-tested) before relying on it, as it has not been fully tested.

## What actually ties it to Claude Code

One thing matters. The system works because the tracker's standing rules — the block
`tracker-setup` writes into `CLAUDE.md` — are in the agent's context at the start of every session,
without anyone asking. Claude Code loads `CLAUDE.md` automatically. Most other agents load
`AGENTS.md` instead, and if yours never sees the block, the tracker just sits on disk unread.
Everything below is about making sure it gets read.

The rest is minor. The skills need to be installed where your agent looks for them. `tracker-audit`
asks its walkthrough questions with a Claude Code tool (`AskUserQuestion`) and may hand big reads to
subagents; another agent can just ask in chat and read inline. The `R:Claude` column in the task
tables is only a name, which could be replaced with `R:Agent` or similar if desired.

## One agent, not Claude Code

Clone the repo, open your agent in the cloned folder, and paste this:

> These are three skills written for Claude Code, in `skills/`. Install them for you, at the user
> level, keeping the three folders side by side — `tracker-close` and `tracker-audit` read files
> from `../tracker-setup/references/`. In the installed copies only: change every reference to the
> instructions file `CLAUDE.md` to the file you load at session start (for most agents,
> `AGENTS.md`), but do not rename the template file `claude_md_block.md`. Where a skill names a
> Claude Code tool (`AskUserQuestion`, subagents, `TaskCreate`/`TaskList`), use your nearest
> equivalent or ask me in chat. Then show me what you changed.

Then, in a session at your project's root, say **"set up a tracker for this project"** as usual.

For Codex, the user-level skills folder is `~/.agents/skills/` (not `~/.codex/skills/`), and the
files load without changes to their frontmatter.

## Several agents on the same projects

This is the setup I use. The principle is one copy of everything, with each agent pointed at it.

**Keep `CLAUDE.md` as the canonical file.** The skills write their block there, so keeping it
canonical means editing nothing. Point the other agent at it, either per project, with a one-line
`AGENTS.md` next to `CLAUDE.md`:

```
All agent guidance for this project lives in CLAUDE.md in this directory: read that file instead.
```

or, for Codex, once globally in `~/.codex/config.toml`:

```toml
project_doc_fallback_filenames = ["CLAUDE.md"]
```

The fallback is used only in folders that have no `AGENTS.md`, so if a project has one, the pointer
line is what does the work. Point one way only — never have the two files refer to each other.
(Claude Code now also reads `AGENTS.md`, and its own docs suggest the reverse arrangement:
`AGENTS.md` canonical, with `CLAUDE.md` starting `@AGENTS.md`. That works too, but the skills would
then need the edit from the section above.)

**Install the skills once and link them.** Install for Claude Code as in the
[README](README.md#install), then link the three folders into the other agent's skills directory —
for Codex:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.claude/skills/tracker-setup ~/.agents/skills/
ln -s ~/.claude/skills/tracker-close ~/.agents/skills/
ln -s ~/.claude/skills/tracker-audit ~/.agents/skills/
```

Link all three, never one alone, for the same `references/` reason as above. An upgrade is then a
single reinstall on the Claude Code side.

**Tell the other agent about Claude Code tools, once.** A few lines in its global instructions file
(`~/.codex/AGENTS.md` for Codex) save repeating this per project: treat `CLAUDE.md` files as
instructions, read the project's one if it isn't already in context, and where a `CLAUDE.md` or a
skill names a Claude Code tool, use the nearest equivalent or ask in chat.

Two smaller things. Codex caps the instruction files it loads at 32 KiB in total by default, so a
long `CLAUDE.md` gets cut off; the tracker block itself is small. And Claude Code's hooks, memory
and permission rules do not carry over to the other agent.

## What has been tested

As of November 2026, with Codex CLI as a backup alongside Claude Code, in the setup just above:
Codex finds the three skills through the symlinks, loads `CLAUDE.md`, and answers "what are our open
tasks?" correctly from `INDEX.md`, `PRIORITIES.md` and the detail files.

Not yet tested: running `tracker-setup`, `tracker-close` or `tracker-audit` end to end under
Codex; the audit's walkthrough without `AskUserQuestion`; and the single-agent install prompt.
Paths and config keys for other agents change quickly — check them against your agent's own docs.

A local model run *through* Claude Code (for example via Ollama) needs none of this, since it is
still Claude Code — though smaller models follow long skills less reliably.
