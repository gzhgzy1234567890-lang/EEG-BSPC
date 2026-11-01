# FACTORIAL_2X2.md

Task B: separate the effect of a class-composition change from the effect of a real drift, in a controlled 2x2
factorial built on statistics estimated from real sleep-EDF features.

## Generator

- Class-conditional means and a pooled covariance are estimated **from real sleep-EDF features** (8 log band
  variances, two channels, the same features the main experiment uses) for 12 subjects (one night each, 2,640 to
  3,900 epochs per subject).
- Source: 600 epochs, balanced classes.
- Target: 600 epochs drawn from the same class-conditional Gaussians with a controlled class proportion pi_B.
- Drift: a constant vector added to every target epoch, drawn in a random direction with magnitude
  drift * sqrt(trace(cov)/d) / sqrt(d).
- The decoder, the block length (15), the first-block warm-up and the past-only correction are exactly those of the
  main experiment.
- 20 independent seeds per cell and subject; 1,440 runs in total.
- The class labels of the simulated target are known to the experimenter, so both the displacement components and
  the true drift can be measured rather than inferred.

| cell | class proportions | drift |
|---|---|---|
| A | unchanged (balanced) | none |
| B | changed (+0.25 mass on one class, renormalised) | none |
| C | unchanged | present (0.5 or 1.0 sd) |
| D | changed | present |

## Results (12 subjects, mean over seeds; delta is corrected minus uncorrected balanced accuracy)

| cell | delta | 95 per cent interval | subjects negative | score-space drift |
|---|---|---|---|---|
| A: no change, no drift | **-0.0034** | [-0.0046, -0.0020] | 10/12 | 0.000 |
| B: prior changed only | **-0.0097** | [-0.0112, -0.0082] | 12/12 | 0.000 |
| C1: drift 0.5 | **+0.0172** | [+0.0127, +0.0224] | 0/12 | 0.984 |
| C2: drift 1.0 | **+0.0601** | [+0.0487, +0.0725] | 0/12 | 1.967 |
| D1: both, drift 0.5 | +0.0121 | [+0.0079, +0.0172] | 0/12 | 0.984 |
| D2: both, drift 1.0 | +0.0557 | [+0.0446, +0.0680] | 0/12 | 1.967 |

Main effects: prior change **-0.0064** (p = 0.001), drift **+0.0634** (p = 0.0005), interaction **+0.0020**
(p = 0.027).

## The five questions the design was built to answer

1. **Is a class-composition change alone enough to produce harm?** Yes, but small: -0.0097 against a -0.0034 floor
   that already exists with no change at all. The floor is the finite-sample cost of subtracting a noisy estimate;
   the composition term roughly triples it.
2. **Is a real drift alone enough to produce a gain?** Yes, and monotonically: +0.0172 at 0.5 sd and +0.0601 at
   1.0 sd, positive in all 12 subjects at both magnitudes.
3. **When do the two together turn gain into loss?** When the composition displacement is large relative to the
   drift. Pooling all runs, the sign of the effect is predicted by which displacement is larger in score space:
   where |drift| > |composition| the mean effect is **+0.0398**, where it is not, **-0.0057**. Spearman correlation
   between the true drift magnitude and the effect is **+0.81**, and between the correction magnitude and the effect
   **+0.29**.
4. **Where does the symmetric Gaussian theory hold and where does it fail?** It predicts the ordering correctly
   (drift helps, composition hurts, the ratio decides), and it fails quantitatively in two ways visible here: the
   no-drift, no-change cell is not zero but **-0.0034**, an estimation-noise cost the population theory does not
   contain; and the composition penalty is not additive with the drift benefit (interaction +0.0020, p = 0.027).
5. **Does this explain the sleep-EDF result?** It reproduces its qualitative signature - a correction that hurts when
   the composition change dominates - but it does not identify the origin of the composition change in that corpus.
   The real data have no known ground-truth drift, so the factorial can only show that the observed pattern is
   *sufficient*, not that it is *the* mechanism.

## What this does not establish

- The generator is Gaussian with a pooled covariance; real sleep features are heavier-tailed and their class
  covariances differ. The design isolates the two factors, which requires that simplification.
- The drift magnitudes are chosen, not measured: 0.5 and 1.0 sd are plausible but arbitrary, and the crossover point
  in a real corpus is unknown.
- Twelve subjects from one corpus; the intervals are subject-level bootstrap intervals, not population claims.
