# Checks

The only numbers the skills measure. `tracker-close` runs the last two lines for each detail file
it touched this session and the PRIORITIES count; `tracker-audit` runs the first three and reports a
number only when it is over threshold. Substitute the tracker directory if it is not `tracker/`.

```bash
wc -w tracker/PRIORITIES.md                       # cap 2,000 words
wc -w tracker/INDEX.md                            # >10,000 suggests archiving closed phases
wc -w tracker/detail/*.md | sort -rn | head -5     # audit: open-task files >15,000 words go under "Long"
# close, per detail file touched this session: head dated today, Progress log the last section
grep -H '^\*Refreshed:' <file>; grep '^## ' <file> | tail -1
```

Closed tasks (`done`, `abandoned`) are never measured. Task-name length is a writing rule, not a
check.
