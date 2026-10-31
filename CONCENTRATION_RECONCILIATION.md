# CONCENTRATION_RECONCILIATION.md

## The claim under test

Supplement S33: "Structure matching, done within subject and within stratum ... the matched difference is
+0.050 ([+0.002, +0.096]), positive in 19 of 28 subjects, two-sided sign test p = 0.087."

## What was regenerated

A full rerun of the sleep-EDF pipeline (`sleep_edf/d3_concentration.py`) recording, for every scored block, its
class concentration (share of the majority class), the block and history class counts, the history length, and the
balanced-accuracy change caused by the correction. 8,503 blocks, 32 subjects, 45 recordings.

Five arm definitions were then evaluated offline (`analyze_concentration.py`), each with at least two blocks per
arm inside each subject-by-stratum cell:

| arms | subjects | cells | matched difference | positive | sign p | Wilcoxon p |
|---|---|---|---|---|---|---|
| median concentration inside stratum | 32 | 150 | **-0.0228** | 10/32 | 0.050 | 0.085 |
| above vs below the uniform share 1/k | 3 | 3 | +0.0250 | 2/3 | 1.000 | 0.500 |
| concentration >= 0.6 vs below | 29 | 96 | -0.0064 | 14/29 | 1.000 | 0.705 |
| concentration >= 0.7 vs below | 32 | 151 | +0.0050 | 17/32 | 0.860 | 0.940 |
| top vs bottom tercile inside stratum | 32 | 530 | -0.0035 | 15/32 | 0.860 | 0.501 |

## Verdict

**+0.050 is not reproduced.** None of the five specifications returns a positive effect of that size; the median
split returns -0.023 with only 10 of 32 subjects positive, and the others are indistinguishable from zero.

## Why the original may have differed

- the concentration measure is not pinned down in the supplement (share of the majority class is the natural
  reading, but entropy or an effective-class count would differ);
- "history length" could mean epochs rather than blocks;
- the original ran on a pipeline state that is not archived with a per-block record, so the exact cells cannot be
  reconstructed.

## What happens to the claim

The exploratory +0.050 is **withdrawn**. The supplement now reports the regeneration: no reproducible association
between class concentration and the size of the correction effect at the block level, under five definitions.
Given that sleep-EDF's main effect is -0.10 with 32/32 subjects negative and does not depend on concentration, this
removal costs the paper nothing and removes an unverifiable number.
