# Reproducibility statement for this submission

## What is public

The analysis code is at https://github.com/gzhgzy1234567890-lang/EEG-BSPC at commit **871546b**. Every result
reported in the paper has a script in that commit, and `REPRODUCE.md` maps the result to the script.

## One command that checks the tables

```
python sleep_edf/check_numbers.py
```

It reads only the archived result files (no raw data), recomputes every number and asserts it against the value
printed in the paper. Output at the time of writing:

```
main          -0.1023 [-0.1149, -0.0899]  32/32 negative  4983 cells
cumulative    -0.1070  32/32 negative
block         -0.1023  32/32 negative
window50      -0.1078  32/32 negative
exponential   -0.0517  32/32 negative
varratio      -0.0820  32/32 negative
decomposition: none 0.4415  full -0.0980  prior -0.1199  cond +0.0340
identical class sets (693 cells): full -0.0512  prior -0.0487  cond +0.0314
gate: always -0.1023  online +0.0001  (10% of blocks corrected)
telemetry     -0.0483 [-0.0588, -0.0369]  21/22 negative  3945 cells
models: lda -0.1047  svm -0.0638  mlp -0.0610
published      -0.1075  12/12 negative
sorted_control -0.0901  12/12 negative
time           +0.0014  6/12 negative
SEED film-disjoint (5 rotations, every film held out once) +0.1894  15/15 positive

CHECK PASS
```

## What it does not check

It verifies the numbers, not the pipeline that produced them. Rebuilding the numbers from the raw EDF and CSV
files is the stage scripts listed in `REPRODUCE.md`; that has been run by the authors but not yet by an
independent party, and the paper says so.

## Limits stated in the paper

- The telemetry protocol was written by the authors before the run; the package cannot independently prove its
  timestamp.
- The telemetry recordings belong to the same corpus as the discovery data, so they are a replication under a
  different acquisition protocol, not an external cohort.
- No single command fetches the data, builds every cache and regenerates every table.
## Later experiments (S30, S31)

The check above covers the results up to the film-disjoint analysis. The three experiments added afterwards
have their own scripts and outputs:

| experiment | script | output |
|---|---|---|
| SEED estimator comparison (S30) | `grasp_and_lift_order/seed_estimators.py` | results/seed_estimators.json |
| SEED memory sweep (S31) | `grasp_and_lift_order/seed_memory_scale.py` | results/seed_memory_scale.json |
| block-wise decomposition (S31) | `sleep_edf/sleep_blockwise.py` | results/sleep_blockwise.json |
| class-run lengths (S31) | `sleep_edf/stage_run_lengths.py` | printed |

Headline values: memory sweep -0.113 (5 segments) to +0.203 (400); exponential -0.105 (alpha 0.2) to +0.130
(alpha 0.01); block-wise full -0.102, joint class-mix only -0.092, conditional only +0.020; per-block
reconstruction error maximum 1.7e-13.
