# Mechanical checks

The six aggregate checks and their thresholds, in one place so `tracker-close` (Duty 3, scoped to
files this session grew) and `tracker-audit` (corner (b), run over the whole corpus) can't drift
apart on them — which is exactly how they diverged in the collection's first release.

Run all six exactly as written, from the project root. The commands spell `tracker/` literally;
substitute a different directory if one applies to this run and say so in the report. If a check's
assumption doesn't hold for the project in front of you — a different column layout, no ledger
markers, no `detail/` subdirectory — say so, adapt the command, and report the number you *can* get.
A check skipped in silence reads in a report exactly like a check that passed.

```bash
# 1. Always-loaded file sizes
#   PRIORITIES: flat word cap (its content is bounded by construction).
wc -w tracker/PRIORITIES.md
#   INDEX: cap the PROSE only (non-table lines) — table rows grow legitimately with the task list.
echo "INDEX prose words: $(awk '!/^\|/' tracker/INDEX.md | wc -w)"   # skimmability guard, cap ~800
echo "INDEX total  words: $(wc -w < tracker/INDEX.md)"               # >5000 -> SUGGEST archiving closed phases

# 2. Longest Task-column cell, and total Task-column characters
awk -F'|' '/^\| *T[0-9]+ *\|/ {gsub(/^ +| +$/,"",$3); print length($3)"\t"$2}' tracker/INDEX.md \
  | sort -rn | head -5
awk -F'|' '/^\| *T[0-9]+ *\|/ {gsub(/^ +| +$/,"",$3); n+=length($3)} END {print "Task column total chars:", n}' tracker/INDEX.md

# 3. Ledger rows vs decision detail files (must be equal — one D## row per detail/D##_*.md)
echo "ledger rows: $(awk '/BEGIN ledger/,/END ledger/' tracker/DECISIONS.md | grep -c '^| D[0-9]')"
echo "D detail files: $(ls tracker/detail/D*.md 2>/dev/null | wc -l | tr -d ' ')"

# 4. Detail file sizes — task (T##_) and decision (D##_) files share tracker/detail/ (warn >3000, flag split >5000)
wc -w tracker/detail/*.md | sort -rn | head -10

# 5. Each detail file's append-at-EOF section must be its last section.
#    The two templates end differently by design: task files with "## Progress log", decision files
#    with "## History". Same invariant (I2) — anything below either one silently stops being the record.
for f in tracker/detail/*.md; do
  case "$(basename "$f")" in
    T*) want="## Progress log" ;;
    D*) want="## History" ;;
    *) echo "UNRECOGNISED: $f — neither a T##_ task nor a D##_ decision detail file"; continue ;;
  esac
  last=$(grep '^## ' "$f" | tail -1 | sed 's/[[:space:]]*$//')
  [ "$last" = "$want" ] || echo "LEAK: $f — last section is ${last:-<no ## sections>}, expected $want"
done

# 6. Heads refreshed where bodies grew — two contexts, one invariant (I2).
#    The head's date line differs by file kind: task files carry "*Refreshed: ...*", decision files
#    "*Set by: ... · Ratified: ...*". Match both, anchored at line start, or D-files go unchecked and
#    any file that merely QUOTES the word "Refreshed:" in its prose reports as a spurious extra head.
#    Both variants read git, so both must first establish that git can SEE tracker/. An empty result
#    means "nothing changed" only then; on a gitignored tracker or a layout-D (no git) project it
#    means "I cannot look" — and reporting that as a pass would hide exactly what check 6 exists to
#    catch. Probe, then branch. Never infer a clean result from an empty one.

# 6a. tracker-close: uncommitted working tree, mid-session, before Duty 5's commit.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then blind="not a git repository (layout D)"
elif git check-ignore -q tracker/detail; then blind="tracker/ is gitignored"
else blind=""; fi

if [ -z "$blind" ]; then
  # -z, not plain --porcelain: git C-quotes any path containing a space in the plain form
  # ('?? "tracker/detail/T2 notes.md"'), which then fails a -f test and is skipped in silence.
  # NUL-delimited output is never quoted. Each record is 2 status chars + space + path; a rename
  # emits a second, prefix-less record for the old path, which the case below drops (it no longer
  # exists, so there is no head to check).
  tmp=$(mktemp)
  git status --porcelain -z -- tracker/detail/ > "$tmp"
  if [ -s "$tmp" ]; then
    while IFS= read -r -d '' rec; do
      case "$rec" in ??\ *) f=${rec#???} ;; *) continue ;; esac
      [ -f "$f" ] && grep -HE '^\*(Refreshed|Set by):' "$f"   # every date must be today
    done < "$tmp"
  else
    echo "check 6a: working tree clean — no detail files changed this session"
  fi
  rm -f "$tmp"
else
  echo "CHECK 6a DEGRADED — git evidence unavailable ($blind); the working tree cannot be diffed."
  echo "Cross-check the dates below against the detail files THIS session grew (Duty 2 knows them):"
  grep -HE '^\*(Refreshed|Set by):' tracker/detail/*.md
fi

# 6b. tracker-audit: committed history, whole corpus.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then blind="not a git repository (layout D)"
elif git check-ignore -q tracker/detail; then blind="tracker/ is gitignored"
else blind=""; fi

grep -HE '^\*(Refreshed|Set by):' tracker/detail/*.md
if [ -z "$blind" ]; then
  git log -1 --format=%cd --date=short -- tracker/detail/   # compare against the dates above
else
  echo "CHECK 6b DEGRADED — git evidence unavailable ($blind); there is no committed history to"
  echo "compare against. Read the dates above against PRIORITIES' Recent sessions / JOURNAL instead."
fi
```

**Thresholds:** `INDEX.md` prose (non-table lines) ≤ 800 words; total > 5,000 words *suggests*
archiving closed phases to `ARCHIVE.md` (not a hard fail) · `PRIORITIES.md` ≤ 2,000 words · longest
Task cell ≤ 50 chars · detail file warn at 3,000 words, flag split at 5,000 · ledger rows == D-detail
file count.

Check 6 has two variants because close and audit read different evidence at different times. Close
runs *before* any commit, so `git log` (6b) can't see this session's edits — a forgotten refresh
would look identical to a compliant one — and must instead read the working tree (6a). `--porcelain`
covers staged, unstaged, and brand-new untracked detail files in one pass; a diff against HEAD alone
would miss the untracked case, since a new file has nothing to diff against. Audit runs after the
fact over committed history, where 6b is correct and is **not valid mid-session before a commit**.

Both variants degrade rather than skip when git can't see `tracker/`. This is not a formality: a
project may keep its tracker gitignored (local + sync only), and layout D has no git at all — both
are supported setups, and in both, every git query returns empty. The old check read that emptiness
as "nothing changed" and passed. A degraded check 6 still prints every head date — `Refreshed:` on a
task file, `Set by:` on a decision file; what it loses is only the ability to narrow them to the
files that changed. Close closes that gap from its
own memory — it knows which detail files Duty 2 grew — and audit compares against the tracker's own
session record. **A DEGRADED line is a result, not an error: report it in the run's output rather
than treating check 6 as passed.**
