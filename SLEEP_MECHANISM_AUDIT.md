# SLEEP_MECHANISM_AUDIT.md — Phase D

## D1. Controlled generator

Script `origin_equivariance/src/sim_d1.py`, seed 20261101, 20 seeds per cell, 600 trials per session,
block = 15, LDA, past-only full correction (lambda = 1).

Factors: constant baseline shift b in {0, 0.25, 0.5, 0.75, 1.0}; target prior pi in {0.2, 0.35, 0.5, 0.65,
0.8}; AR(1) noise rho in {0, 0.9} with amplitude 0.5; a = 1.

Prediction from Proposition 3b: full correction helps iff |b| > |(2 pi - 1) a|.

Result: **the predicted sign matched the simulated sign in 50 of 50 cells.**

| b | pi | rho | delta BA | seeds positive | predicted |
|---|---|---|---|---|---|
| 0.00 | 0.20 | 0.0 | -0.066 | 0/20 | harm |
| 0.00 | 0.50 | 0.0 | -0.001 | 7/20 | tie |
| 0.00 | 0.80 | 0.0 | -0.076 | 0/20 | harm |
| 0.25 | 0.50 | 0.0 | +0.009 | 15/20 | help |
| 0.50 | 0.50 | 0.0 | **+0.047** | 20/20 | help |
| 0.50 | 0.80 | 0.0 | **-0.027** | 1/20 | harm (composition 0.6 > drift 0.5) |
| 1.00 | 0.50 | 0.0 | **+0.146** | 20/20 | help |
| 1.00 | 0.80 | 0.0 | **+0.087** | 20/20 | help (drift 1.0 > composition 0.6) |

The AR factor changes the variances but not the sign: rho = 0.9 cells agree with rho = 0 cells in every row.
Full table: `results/MECHANISM_RESULTS.csv` (50 rows) and `results/d1_grid.json`.

**What this establishes.** Within the symmetric Gaussian model, the sign of the correction effect is predicted by
the ratio of the real drift to the class-composition term, and the prediction is not tuned after seeing the
outcomes.

**What it does not establish.** That sleep-EDF behaves like this model. The real data have multi-class labels,
non-Gaussian features and time structure the model does not represent; D2-D4 are the real-data counterparts and
they are association-level only.

## D2. Decomposition on real data (recap, unchanged)

Full displacement -0.098, joint class-mix -0.091, shared prior -0.120, conditional +0.034 (global diagnostic);
block-wise, causal: full -0.102, mix-only -0.092, conditional +0.020; per-block reconstruction max 1.7e-13.
Non-additivity -0.041 [-0.048, -0.034]. These are ORACLE-DIAGNOSTIC: they use true target labels.

## D3. Matched comparison on real data (recap)

Within subject-by-stratum matching (stratum = classes in block x classes in history x history length), 92 usable
cells over 28 subjects: +0.050 [+0.002, +0.096], 19/28 positive, two-sided sign test p = 0.087.
**Exploratory and not significant.** The earlier +0.068 that pooled across strata is withdrawn.

## D4. BBSE on real data (recap)

Support-valid cells: 1,763 of 4,983. Confusion condition number median 2.0. TV error on the full class space
median 0.207. Removing the estimated prior costs -0.078 [-0.096, -0.060]; removing the true prior on the same
cells costs -0.110 [-0.127, -0.092]. Transductive, not online.

## D5. Classifier priors and thresholds

**Not yet run.** The comparison (empirical LDA priors vs uniform priors vs fixed threshold) is the next
mechanism experiment; it is listed here so that the gap is not hidden.

## D6. Evidence grading of the mechanism claims

| claim | theory | simulation | real association | intervention | confounds controlled | predicts new data |
|---|---|---|---|---|---|---|
| composition-only correction harms when the prior is unbalanced | Props 1-3 | D1 confirms | S31 (+0.084, exploratory) | block-wise mix removal | partial (D3 matching) | not tested |
| correction helps when real drift dominates | Prop 3b | D1 confirms (50/50) | not identified in sleep-EDF | none | none | not tested |
| the loss is carried by the class-mix part | - | - | block-wise -0.092 | oracle labels | class identity, night position not matched | not tested |

No causal explanation is claimed for the sleep-EDF loss; the strongest statement allowed is that the class-mix
displacement carries it under an oracle diagnostic, and that an association with class concentration survives
some structural matching but is not significant.
