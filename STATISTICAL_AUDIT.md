# STATISTICAL_AUDIT.md

Independent recomputation from archived cells, script `origin_equivariance/src/b3_hierarchy.py`
(sleep-EDF part: `sleep_edf/b3_hierarchy.py`), reading only `sleep_edf/results/sleep_edf_frozen_cells.json`.

## Hierarchy

| level | count |
|---|---|
| cells (source-target series pairs) | 4,983 |
| recordings (nights) | 45 |
| subjects | 32 |

The cell-level mean is -0.1011 and the subject-level mean is -0.1023. They agree closely, but only the
subject-level value is used for inference; the cell-level number is printed here to show that it is not treated as
independent evidence.

## Inferential statistic

Per-subject value = mean over that subject's nights of the night's mean cell delta.

| quantity | value |
|---|---|
| subjects | 32 |
| mean | -0.1023 |
| sd (between subjects) | 0.0360 |
| negative subjects | 32/32 |
| Wilcoxon signed-rank p | 7.95e-07 |
| bootstrap 95% interval (10,000 resamples, seed 20261101) | [-0.1145, -0.0900] |

Between-night variability within subjects: mean sd 0.0173, about half the between-subject sd, so the aggregation
order matters and is stated.

## What this audit checks and what it does not

- It checks that the reported -0.102 and its interval can be regenerated from the archived cells by a script that
  does not import the original analysis code.
- It does **not** re-run the EEG pipeline; the cells themselves are archived outputs. That limitation is recorded
  in CURRENT_BLOCKERS.md (B2).
- Per-class recall is not in the archived cell file; it is being added by the D5 run and will be reported there.

## Discrepancies

None: the recomputation reproduces the manuscript's -0.102 [-0.114, -0.090] to the third decimal.
