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
