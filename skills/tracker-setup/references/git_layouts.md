# Git layouts for a project inside a cloud-sync folder

Read by `tracker-setup` only when the project's absolute path contains `Dropbox`, `iCloud`,
`OneDrive`, or `Google Drive`. Present the four options compactly, ask "Will you work on this
project from more than one computer?", and apply the one the user picks. Never choose for them.
The hazard: a sync client can corrupt or delete `.git` mid-commit, silently; only git notices.
Under A–C all working files sync, gitignored ones too.

## The four options

- **A — one machine, git database outside the sync folder** (`--separate-git-dir`).
  *Recommended for one machine.* The `.git` pointer file holds an **absolute path**, binding the
  repo to this machine: on a second computer git fails, though edits there still sync back.
- **B — several machines, git database *inside* the sync folder.** The simplest multi-machine
  option. **Degrades as the repo grows:** sync churn risks silently corrupting `.git`. Let sync
  finish before switching machines; never work from two at once. Small projects, or no remote.
- **C — several machines, a git database outside the sync folder on each, shared remote.**
  *Recommended for several machines.* Needs a **private** remote to carry history. Each session
  starts with the reminder's sync check. Its relative pointer needs the sync folder at the same
  place under each home; moving the project breaks it loudly.
- **D — no git at all.** Sync history is the only history: the honest choice for someone not at
  ease with git. Costs: no traceability, no revert, and close loses its commit duty.

## Applying the choice

- **A:** `mkdir -p "$HOME/git-repos" && git init -b main --separate-git-dir="$HOME/git-repos/<project-name>.git"`.
  Tell the user: files keep syncing; `.git` becomes a pointer *file*.
- **B:** plain `git init -b main`, inside the sync folder as normal.
- **C:** A's command, then rewrite `.git` as `gitdir: <path>`, the database's `os.path.relpath`
  from the project folder; check `git status` works. Add the private remote; push the first
  commit. Each other machine, once: `mkdir -p "$HOME/git-repos" && git clone --no-checkout
  --separate-git-dir="$HOME/git-repos/<project-name>.git" <remote> "$(mktemp -d)/x"`, then the
  sync check. Never run `git init` in the synced folder there: it rewrites `.git` for every machine.
  If you can message a session on the other machine (Claude Code: Remote Control), ask the user
  to connect one and name it; setup is easier coordinated.
- **D:** run no git command. Tell the user `tracker/` will not be under version control; still
  write a `.gitignore`.

## The reminder written into `## Project settings`

- A: "One machine; git database outside the sync folder via an absolute-path pointer. Adding a
  machine means moving to C (`tracker-setup`'s `git_layouts.md`)."
- B: "Several machines; git database lives inside the sync folder — let sync finish before
  switching machines, never work from two at once; check sync status at each session start."
- C: "Several machines; a git database on each, relative `.git` pointer, private remote. Before any
  work: `git fetch`; stop if HEAD and `origin/main` have diverged; unless HEAD is only ahead,
  `git reset --mixed origin/main` (even when level); stop unless `git status --porcelain` is
  empty: sync is lagging or the other machine left work uncommitted. On a stop, tell the human;
  never commit, discard, or pull. Close always pushes. Never work from two machines at once."
- D: "No git — sync history is the only history; `tracker-close` skips the commit step."

## Existing repo

Change nothing in git. If `.git` is a file pointing outside the sync folder, ask: one machine is
A; several is C — apply C from the pointer rewrite on. Otherwise warn of the hazard and ask:
several is B; for one, suggest moving the database out by hand (`git init --separate-git-dir`),
then record A if they do, else B.

**A to C, asked for later:** commit and push; apply C from the pointer rewrite on; replace the
`Git layout` line under `## Project settings` with C's reminder.
