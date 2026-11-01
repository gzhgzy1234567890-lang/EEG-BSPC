# TABLE_TRACEABILITY.md

Every headline number in Table 9 was re-derived from its archived source by `table_trace.py` and compared with the
number printed in the manuscript. Run on 1 November 2026, after the revision.

| number in Table 9 | source | check | result |
|---|---|---|---|
| BCI-2b csp +0.0341 [+0.0104, +0.0585] | `statistics_recomputed_2b.json` (from `recompute_2b.py`) | mean, lower and upper bound within 5e-4 | **OK** |
| Sleep-EDF -0.102 [-0.114, -0.090], 32/32 | `b3_hierarchy.json` (from `b3_hierarchy.py`) | mean, interval within 5e-4 | **OK** |
| BCI-challenge ERRp -0.0044 [-0.0166, +0.0075] | `errp_external.json` | mean recomputed from the 16 subject values | **OK** |
| P300 -0.0005 [-0.0024, +0.0012], 7/16 | `p300_external_meanamp.json` | mean recomputed from the 16 subject values | **OK** |

Result: **TABLE TRACEABILITY PASS**, archived in `results/table9_traceability.json`.

## What this does and does not check

- It checks that the numbers printed in the manuscript equal the numbers in the archived outputs, i.e. that no
  transcription error entered the table.
- It does **not** check that the archived outputs are themselves correct: that is the job of the scripts listed in
  CODE_MAP.md and of the pre-registrations, and for the theory of the Monte Carlo and regression tests.

## Numbers not covered by this check

- SEED +0.214 [+0.167, +0.260], BCI-2a +0.071 [+0.041, +0.104] and the grasp-and-lift contrast come from earlier
  archives produced before the current script set; their provenance is recorded in FILE_PROVENANCE.csv and they were
  not re-derived here. That is a gap, and it is stated rather than hidden.
