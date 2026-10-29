# Reproducibility audit

## Level A -- statistical replication from results/master_cells.csv

| item | verdict | detail |
|---|---|---|
| cell count is the 773 source-only cells of the 845 reported | PASS | 773 cells; 845 counts all representations, 72 of which are target-informed and excluded here |
| subject identity keyed by (dataset, subject) | PASS | 61 distinct (ds, subject) keys, 36 bare names |
| gal endpoint difference D = BA(1)-BA(0) | PASS | -0.1075 [-0.1314, -0.0833] vs paper -0.1075 [-0.1314, ...] |
| seed endpoint difference D = BA(1)-BA(0) | PASS | 0.2142 [0.1672, 0.2602] vs paper 0.2142 [0.1672, ...] |
| grasp-and-lift subject-level rho(dR2, loss) = +0.776 | PASS | 0.7762 over 12 subjects |
| grasp-and-lift R2 0.800 and permutation null 0.255 | PASS | 0.800 / 0.255 |

## Level B -- invariants of the online implementation (real cells)

| item | verdict | detail |
|---|---|---|
| lambda = 0 reproduces the uncorrected scores exactly | PASS | max |difference| = 0.0e+00 |
| lambda = 1 reproduces the full-strength historical correction | PASS | bitwise identical to the definition |
| a prediction does not depend on any later trial | PASS | blocks 1-2 unchanged after corrupting trials 30..n |
| all compared methods share one evaluation window | PASS | scores computed on all 68 trials |
| common feature translation leaves the corrected scores unchanged | PASS | max |difference| = 2.1e-13 after shifting all features by 7.3 |
| a zero displacement is a no-op, not a division by zero | PASS | zero vector handled without NaN |

## Level C -- end to end from the public EEG files

| item | verdict | detail |
|---|---|---|
| features regenerated from the public recordings | NOT VERIFIED | the audit ran from the feature cache; the cache-to-raw path was not re-executed here |

Summary: 12 PASS, 0 FAIL, 1 NOT VERIFIED.
