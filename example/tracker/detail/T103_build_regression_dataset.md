# T103 — Build regression dataset

*File type: **headed-append** — the head below is rewritten whenever the body grows. Never append without refreshing it.*

*One detail file per task. If this log starts covering more than one task ID, the task has become
an umbrella — split it into one file per child rather than letting this one grow to cover all of
them. Size: `tracker-close` warns at ~3,000 words and flags for splitting at ~5,000.*

## Current state
*Refreshed: 2026-07-19*

Status: `in-progress`. Assembling the estimation dataset from `T102`'s validated panel: constructing
the outcome (job satisfaction), the key regressor (commute time), and controls, and attaching
`D01`'s imputation validity flags. Two extracts are built — a full-sample extract for the pooled
baseline and a restricted extract for the fixed-effects spec, which applies `D02`'s ≥3-wave sample.
Open: a sparse-income subgroup (respondents missing income in >40% of their waves) is unstable under
the current construction — see the 2026-07-12 log entry.

*This section is rewritten in place every time the log below grows — it is the one place in this
file that must never go stale. If it stops matching the log, the log becomes the only place a
reader can find current truth, which is exactly the failure this format exists to prevent.*

## Goal

Produce the analysis dataset `T201`'s baseline regression consumes: one row per respondent-wave with
the outcome, commute time, controls, and `D01`'s validity flags.

## Sub-steps

- Select modelled variables from `T102`'s validated panel.
- Construct derived controls (age band, log income, hours, industry).
- Attach `D01`'s imputation validity flags.
- Build the FE-spec extract under `D02`'s ≥3-wave restriction; leave the pooled extract unrestricted.
- Write the dataset and a manifest recording the source-panel hash and the code revision.

## Acceptance criteria

- No unexpected nulls in the modelled columns.
- The manifest records the input panel hash and the code revision that built the dataset.
- Both the pooled and FE-spec extracts build end-to-end.

## Stopping criteria

- **Success:** both extracts pass the acceptance criteria and `T201` can consume the dataset without
  modification.
- **Bailout:** if the sparse-income subgroup requires a schema change, stop and report rather than
  patching around it in this step.
- **Wall-clock cap:** 2 hours of unsupervised work before checking in.

## Notes

`D02`'s ≥3-wave restriction is scoped `[spec: fixed-effects]` — apply it only to the FE-spec extract,
never to the pooled baseline.

## Progress log

### 2026-07-12 — Assembled dataset against T102 schema; sparse-income subgroup surfaced

Built the respondent-wave dataset with outcome, commute, and controls, and attached the validity
flags. Found that respondents missing income in >40% of their waves behave unpredictably under the
current construction — recorded as the open item in Current state rather than worked around here.

### 2026-07-19 — Rejoined validity flags after D01 revision

`D01` moved to backward-fill + flag; rejoined the new flags into both extracts. The sparse-income
subgroup is still open.
