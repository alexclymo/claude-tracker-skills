# Checks

The only numbers the skills measure. `tracker-audit` runs the first three commands and reports a
number only when it is over threshold; `tracker-close` runs the last two for each detail file it
touched this session, plus the PRIORITIES count. Substitute the tracker directory if it is not
`tracker/`.

```bash
wc -w tracker/PRIORITIES.md                                       # cap 2,000 words
wc -w tracker/INDEX.md                                            # >10,000 suggests archiving closed phases
wc -w tracker/detail/T*.md | grep -v total | sort -rn | head -5   # audit: Long if >15,000
# close, per detail file touched this session:
grep -H '^\*Refreshed:' <file>            # today's date
grep '^## ' <file> | tail -1              # "## Progress log"
```

Closed tasks (`done`, `abandoned`) are never measured: read INDEX first and drop their files from
the third command's output. Task-name length is a writing rule, not a check.
