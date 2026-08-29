"""PLACEHOLDER -- illustrative skeleton, NOT working code.

This module sketches the data pipeline for the example project. Nothing
here runs: every function raises NotImplementedError. It exists only to
show what the `code/` folder of a tracked project looks like, and how code
can reference the tracker's tasks and decisions by ID.

Pipeline stages map onto tracker tasks:
    load_panel        -> T101  (ingest survey panel data)
    validate_schema   -> T102  (clean and validate schema)
    build_dataset     -> T103  (build regression dataset)
    estimate_baseline -> T201  (estimate baseline regression; blocked on T103)

Design decisions referenced below:
    D01  backward-fill income imputation with a validity flag
    D02  restrict the fixed-effects sample to respondents in >= 3 waves

See ../tracker/INDEX.md for the full picture.
"""

from __future__ import annotations


def load_panel(path):
    """T101 -- load the raw NHPS extract into a tidy long panel.

    Missing income is imputed by backward-fill, carrying a validity flag
    on every imputed cell, per decision D01. The flag propagates downstream
    so later stages can tell imputed income from observed income.
    """
    raise NotImplementedError("placeholder -- example project, not runnable")


def validate_schema(panel):
    """T102 -- coerce types and range-check the panel.

    Job satisfaction must fall in [0, 10]; commute time must be >= 0.
    Emits a schema manifest; malformed rows are dropped, not patched.
    """
    raise NotImplementedError("placeholder -- example project, not runnable")


def build_dataset(panel, spec="pooled"):
    """T103 -- assemble the estimation dataset (one row per person-wave).

    Builds the outcome, the key regressor (commute time), and controls, and
    attaches D01's validity flags. For spec="fixed_effects", restricts to
    respondents observed in >= 3 waves (decision D02); spec="pooled" uses
    the full sample.
    """
    raise NotImplementedError("placeholder -- example project, not runnable")


def estimate_baseline(dataset):
    """T201 -- pooled OLS plus a fixed-effects robustness check.

    Blocked on T103: needs the finished estimation dataset. Standard errors
    are clustered by individual; results are exported for the paper (T202).
    """
    raise NotImplementedError("placeholder -- example project, not runnable")


def main():
    panel = load_panel("data/nhps_extract.csv")
    panel = validate_schema(panel)
    dataset = build_dataset(panel, spec="pooled")
    estimate_baseline(dataset)


if __name__ == "__main__":
    main()
