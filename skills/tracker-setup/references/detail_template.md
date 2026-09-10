# T103 — Build feature extraction

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

## Current state
*Refreshed: 2026-07-15*

Status: `in-progress`. Extracting features batch-wise from the schema validated in `T102`; batch
size capped at 256 for model B only (see Notes), model A runs unbatched. Imputation is now
backward-fill with a validity flag, per `T101`'s Notes; this step no longer assumes forward-fill.
Open: the extractor does not yet handle the sparse-channel case surfaced on 2026-07-14.

## Goal

Produce a fixed-width feature matrix from the validated raw dataset, ready for `T201`'s baseline
model.

## Sub-steps

- Load validated schema output from `T102`.
- Compute the feature set.
- Batch and cap where model B applies.
- Write the feature matrix and a manifest of what version produced it.

## Acceptance criteria

- Output matrix has no null feature values.
- Manifest records the input dataset hash and the code revision.
- Runs end-to-end on the full dataset in under 30 minutes.

## Stopping criteria

- **Success:** feature matrix passes all acceptance criteria above and `T201` can consume it
  without modification.
- **Bailout:** if the sparse-channel case requires a schema change, stop and report rather than
  patching around it.
- **Wall-clock cap:** 2 hours of unsupervised work before checking in.

## Notes

- **Batch cap `[model-B]`** (2026-06-20): 256 rows per batch for model B only; model A's extractor,
  added later, runs unbatched. Chosen after model B's extractor ran out of memory at 512.

## Progress log

### 2026-07-10 — Scaffolded extractor against validated schema from T102

Implemented the base extraction pass; the batch cap was not yet needed (model B was the only
consumer at the time).

### 2026-07-14 — Added model-B batch cap; surfaced sparse-channel gap

Applied the 256-row cap for model B. Found that channels with >40% missing values behave
unpredictably in the current recipe; recorded as the open item in Current state above rather than
worked around here.
