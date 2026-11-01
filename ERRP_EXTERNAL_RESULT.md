# ERRP_EXTERNAL_RESULT.md

Outcome of the pre-registered **cross-session** external test. Protocol committed as `969b0d5` before the run.

## Design as pre-registered

16 subjects, five sessions each, four consecutive forward pairs (1->2, 2->3, 3->4, 4->5), epochs 0-600 ms after
each feedback marker, per-channel log-variance in four sub-windows (224 features), LDA fitted on the source
session, past-only correction with block 15 on the target session, delta balanced accuracy averaged over the four
pairs per subject.

## Result

| quantity | value |
|---|---|
| subjects | 16 |
| mean delta balanced accuracy | **-0.0044** |
| subjects positive | 6 of 16 |
| two-sided sign test | p = 0.45 |
| Wilcoxon | p = 0.53 |
| balanced accuracy without correction | 0.45-0.58 per subject |

Per-subject values: S02 -0.0074, S06 +0.0436, S07 -0.0317, S11 -0.0004, S12 -0.0014, S13 -0.0199, S14 -0.0175,
S16 +0.0033, S17 -0.0196, S18 +0.0191, S20 -0.0008, S21 -0.0236, S22 -0.0622, S23 +0.0010, S24 +0.0217,
S26 +0.0260. All 16 reported; none dropped.

## Post-hoc conditional analysis (added after the referee's MC6)

The referee noted that a near-chance decoder limits what a null result can mean. Conditioning on decoding quality
shows the effect is not flat:

| subset | n | mean delta | 95 per cent interval | positive |
|---|---|---|---|---|
| all subjects | 16 | -0.0044 | [-0.0166, +0.0074] | 6/16 |
| balanced accuracy >= 0.52 | 6 | **-0.0239** | **[-0.0415, -0.0093]** | 1/6 |
| balanced accuracy >= 0.55 | 3 | -0.0297 | [-0.0622, -0.0074] | 0/3 |

Spearman correlation between per-subject balanced accuracy and the correction effect: **rho = -0.71, p < 0.01**.

Reading, and its limits:

- the correction is *more harmful where decoding is better*, which is the opposite of what a pure power explanation
  would predict, and it points in the same direction as the sleep-EDF loss;
- the subsets were chosen **after** seeing the data, n is 6 and 3, and the correlation is across subjects in one
  corpus; this is **EXPLORATORY and post-hoc**, not a replication of the sleep result;
- the honest summary is therefore: overall near zero, negative where decoding is usable, with the caveat that the
  conditional analysis was not pre-registered.

## Interpretation

1. **No significant cross-session effect** on this dataset, in either direction. The mean is -0.004 with six
   subjects positive.
2. The decoders are weak (balanced accuracy 0.45-0.58, i.e. around chance for many subjects), so the test has low
   power: a correction can only change decisions that are near the boundary, and at chance-level decoding the
   boundary carries little information. The null is therefore **uninformative about the sign** and informative
   only in the weak sense that no large effect appears.
3. This is the second independent dataset in the paper and the first with the cross-session structure the paper is
   about. It does not replicate the sleep-EDF harm, does not replicate the BCI gain, and does not contradict
   either: at this decoding strength the correction is close to inert.

## Evidence grading

**EXPLORATORY-INDEPENDENT**: independent data, pre-specified protocol, no pre-specified sign (registered as
two-sided). It cannot support a confirmatory claim in either direction.

## What goes into the paper

One Discussion sentence: a second independent corpus with five sessions per subject shows no cross-session effect
of the correction (-0.004, 6 of 16 positive) at near-chance decoding, which bounds how large a cross-session effect
can be when the decoder is weak but does not test the sign.