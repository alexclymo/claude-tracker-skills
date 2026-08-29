# ARCHIVE

*File type: **append-only** — entries appended at end of file. Never rewritten.*

Never loaded at session start. Exists so that closing a phase in `INDEX.md` never means destroying
the record — the phase's full task table moves here, verbatim, leaving only a one-line pointer
behind in `INDEX.md`.

Entries: `### Phase N — <name> (closed YYYY-MM-DD)`, each holding the closed phase's complete task
table exactly as it last read in `INDEX.md`.

### Phase 0 — Environment setup (closed 2026-05-30)

| ID | Task | Status | Depends | R:Human | R:Claude | Category |
|-----|------|--------|---------|---------|----------|----------|
| T001 | Provision compute environment | done | — | ok | ok | code |
| T002 | Install pinned dependencies | done | T001 | ok | ok | code |
