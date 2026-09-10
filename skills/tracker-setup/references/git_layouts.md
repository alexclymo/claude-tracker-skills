# Git layouts for a project inside a cloud-sync folder

Read by `tracker-setup` only when the project's absolute path contains `Dropbox`, `iCloud`,
`OneDrive`, or `Google Drive`. Present the four options compactly, ask "Will you work on this
project from more than one computer?", and apply the one the user picks. Never choose for them.

## Why this needs a choice

A `.git` directory syncs like any other folder, but git's object store is not designed for that: a
sync client can write a partial object mid-commit, two devices can converge on conflicting copies
of the same ref, or a sync event can simply delete `.git` outright — and none of this looks like an
error to the sync client, only to git, later.

## The four options

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

## Applying the choice

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

## The reminder written into `## Project settings`

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
