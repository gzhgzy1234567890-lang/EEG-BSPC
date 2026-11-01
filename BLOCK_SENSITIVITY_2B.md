# BLOCK_SENSITIVITY_2B.md

Sensitivity of the pre-specified BCI-2b endpoint to the block length. The protocol fixed 15 trials per block; this
analysis recomputes the same endpoint at 10 and 20 trials, with everything else (causal filter, source-only
alignment, csp, completed-block mean, first block unscored) unchanged.

| block | representation | n | mean delta | 95 per cent interval | Wilcoxon p | subjects positive |
|---|---|---|---|---|---|---|
| 10 | csp | 9 | +0.0336 | [+0.0099, +0.0586] | 0.055 | 7/9 |
| **15 (pre-specified)** | **csp** | **9** | **+0.0341** | **[+0.0099, +0.0583]** | **0.039** | **8/9** |
| 20 | csp | 9 | +0.0340 | [+0.0096, +0.0595] | 0.055 | 7/9 |
| 10 | euc | 9 | +0.0384 | [+0.0196, +0.0573] | 0.0039 | 9/9 |
| 15 | euc | 9 | +0.0317 | [+0.0167, +0.0472] | 0.0039 | 9/9 |
| 20 | euc | 9 | +0.0323 | [+0.0146, +0.0519] | 0.0078 | 8/9 |

## What is stable and what is not

- **The effect size is stable**: 0.0336, 0.0341 and 0.0340 across the three block lengths, a spread of 0.0005.
- **The bootstrap interval is stable and excludes zero** in all three: lower bounds 0.0096 to 0.0099.
- **The rank test is borderline**: p = 0.039 at the pre-specified block length and 0.055 at the other two. With nine
  subjects the Wilcoxon test has few attainable values, and the assignment of ranks shifts with one or two subjects.

## Honest reading

The pre-specified analysis stands exactly as registered: block 15, +0.0341, p = 0.039 uncorrected. The sensitivity
analysis shows that the **magnitude** does not depend on the block length but that the **p-value sits on the 0.05
boundary** and would not be called significant at the two alternative lengths. The paper therefore reports the
endpoint as a stable effect size with a borderline test, not as a robust significant result.

This analysis was run after the referee report and is labelled exploratory; the pre-specified endpoint remains the
block-15 result.
