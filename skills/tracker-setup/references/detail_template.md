# T103 — Build feature extraction

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

*One detail file per task. If this log starts covering more than one task ID, the task has become
an umbrella — split it into one file per child rather than letting this one grow to cover all of
them. Size: `tracker-close` warns at ~3,000 words and flags for splitting at ~5,000.*

## Current state
*Refreshed: 2026-07-15*

Status: `in-progress`. Current approach: extract features batch-wise per `D03`'s pipeline recipe,
using the schema validated in `T102`; batch size capped at 256 for model B only, per `D02`'s scope
banner — model A runs unbatched. The forward-fill imputation this step used to depend on was
revised in place — `D01` now rules backward-fill with a validity flag (see its `## History`); this
file no longer assumes forward-fill. Open: the extractor does not yet handle the sparse-channel case
surfaced in the 2026-07-14 session below.

*This section is rewritten in place every time the log below grows — it is the one place in this
file that must never go stale. If it stops matching the log, the log becomes the only place a
reader can find current truth, which is exactly the failure this format exists to prevent.*

## Goal

Produce a fixed-width feature matrix from the validated raw dataset, ready for `T201`'s baseline
model.

## Sub-steps

- Load validated schema output from `T102`.
- Compute the feature set per `D03`'s recipe.
- Batch and cap per `D02` where model B applies.
- Write the feature matrix and a manifest of what version produced it.

## Acceptance criteria

- Output matrix has no null feature values.
- Manifest records the input dataset hash and the code revision.
- Runs end-to-end on the full dataset in under 30 minutes.

## Stopping criteria

*Filled in at the moment autonomy is granted for this task, not pre-declared when the task is
created — a stopping condition written before anyone knows what "done" looks like is a guess, not
a guardrail.*

- **Success:** feature matrix passes all acceptance criteria above and `T201` can consume it
  without modification.
- **Bailout:** if the sparse-channel case requires a schema change, stop and report rather than
  patching around it.
- **Wall-clock cap:** 2 hours of unsupervised work before checking in.

## Notes

Model A's extractor was added after this file was created; see `D02`'s scope banner for why the
batch cap doesn't apply to it.

## Progress log

*This must remain the last section of the file. Entries are appended at EOF under
`### YYYY-MM-DD — <session summary>`. If anything is ever added below this section, the log has
stopped being last and will silently stop containing entries — sessions will still happen, but
nothing here will record them.*

### 2026-07-10 — Scaffolded extractor against validated schema from T102

Implemented the base extraction pass; batch cap and scope tag not yet needed (model B was the only
consumer at the time).

### 2026-07-14 — Added model-B batch cap per D02; surfaced sparse-channel gap

Applied the 256-row cap for model B. Found that channels with >40% missing values behave
unpredictably in the current recipe — recorded as the open item in Current state above rather than
worked around here.
