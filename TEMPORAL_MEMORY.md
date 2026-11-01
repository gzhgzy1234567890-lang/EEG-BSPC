# TEMPORAL_MEMORY.md

Task C: where the sign of the effect changes as a function of memory length, on the two real corpora and in a
controlled experiment.

## Part 1. SEED: memory sweep at subject level (15 subjects, archived per-cell values)

The estimator averages the last w DE segments; the segments are the **1 s** distributed differential-entropy
features stated in the data table, so w segments = w seconds.

| memory | effect on balanced accuracy | 95 per cent interval | subjects positive |
|---|---|---|---|
| w = 5 s | -0.1129 | [-0.1453, -0.0804] | 1/15 |
| w = 10 s | -0.1075 | [-0.1402, -0.0750] | 1/15 |
| w = 25 s | -0.0797 | [-0.1150, -0.0462] | 2/15 |
| w = 50 s | -0.0408 | [-0.0747, -0.0068] | 6/15 |
| w = 100 s | +0.0196 | [-0.0149, +0.0552] | 8/15 |
| w = 200 s | +0.1066 | [+0.0697, +0.1453] | 14/15 |
| w = 400 s | +0.2025 | [+0.1624, +0.2435] | 15/15 |
| exponential, alpha 0.20 | -0.1041 | [-0.1371, -0.0716] | 2/15 |
| exponential, alpha 0.05 | -0.0389 | [-0.0755, -0.0028] | 6/15 |
| exponential, alpha 0.02 | +0.0570 | [+0.0218, +0.0942] | 13/15 |
| exponential, alpha 0.01 | +0.1422 | [+0.1024, +0.1839] | 15/15 |

**The sign changes between 50 and 100 s.** A SEED film is 3,394/15 about 226 s, so the crossing sits just under one
film: the correction helps only once its memory spans a whole film.

## Part 2. sleep-EDF: the real time scales

| quantity | value (20 nights, 2,200 stage runs) |
|---|---|
| stage run length, median | 1.5 min |
| stage run length, mean | 12.4 min |
| stage run length, 90th percentile | 14.5 min |
| class proportions (W, N1, N2, N3, R) | 0.68, 0.03, 0.17, 0.05, 0.07 |
| majority-class share per night, median | 0.68 |

The main experiment blocks 15 epochs of 30 s, so its memory is 7.5 min at the second block and at most 22.5 min
over a 60-epoch series: **one to three blocks, in a corpus whose majority class occupies 68 per cent of the night.**

## Part 3. Controlled experiment: memory x class duration x drift

Same generator as Task B (real class-conditional means and pooled covariance from 12 subjects), 12 subjects,
4 seeds, source balanced and i.i.d., target 1,200 epochs, drift implemented as a ramp of the stated magnitude.
`mem` is the number of past blocks (15 epochs each) averaged; effect is corrected minus uncorrected balanced accuracy.

**No drift (the pure composition and noise floor):**

| class run | mem 1 | mem 4 | mem 16 |
|---|---|---|---|
| 1 epoch | -0.0234 | -0.0095 | -0.0033 |
| 5 epochs | -0.0719 | -0.0195 | -0.0072 |
| 25 epochs | **-0.2749** | -0.1103 | -0.0276 |

**With a ramp drift:**

| class run | drift | mem 1 | mem 16 |
|---|---|---|---|
| 1 | 0.5 | -0.0187 | +0.0008 |
| 1 | 1.0 | -0.0027 | **+0.0216** |
| 25 | 0.5 | -0.2604 | -0.0246 |
| 25 | 1.0 | -0.2414 | -0.0333 |

## What the three parts say together

1. **Memory length is a first-order determinant, through the variance of the estimate.** With no drift at all the
   effect is -0.023 at one block, -0.010 at four and -0.003 at sixteen: the correction pays for its own estimation
   noise, and the price falls as the memory grows.
2. **Class duration sets how large that price is.** At one block of memory a 25-epoch class run turns a -0.023
   floor into **-0.275**, an order of magnitude larger, because a short memory lags the composition. The same long
   runs at sixteen blocks cost only -0.028.
3. **A drift only produces a net gain where the composition change is small.** At run 1 and sixteen blocks of
   memory a one-sd ramp gives **+0.0216** (12/12 subjects positive); at run 25 the same drift cannot overcome the
   lag and the effect stays at -0.033.
4. **This is the pattern the two corpora show.** SEED crosses to positive only when the memory spans a film, and
   sleep-EDF, whose memory is one to three blocks in a corpus dominated by one stage, sits in the regime the
   controlled experiment says is harmful.

## What this does not establish

- The controlled experiment uses Gaussian class conditionals with a pooled covariance; it isolates the factors at
  the cost of a simplified generator.
- The mapping from memory in segments to seconds depends on the segment duration, 1 s for SEED and 30 s for
  sleep-EDF; the corpora are compared in time rather than in sample counts, but neither conversion is exact for a
  non-uniform estimator such as the exponential average.
- Task C does not show that memory is the only difference between the corpora: class counts, balance, feature set
  and split all differ as well.
