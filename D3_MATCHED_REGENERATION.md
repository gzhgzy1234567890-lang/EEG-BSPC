# D3_MATCHED_REGENERATION.md

## What was regenerated

An independent run of the sleep-EDF pipeline (`sleep_edf/d3_blocks.py`), recording, for every scored block of
every cell, the balanced-accuracy change produced by the past-only correction and the stratum key: the class set of
the block, the class set of the history, the history class balance, and the block index. 8,503 block records over
4,983 cells and 32 subjects.

Six matching specifications were then evaluated offline (`analyze_d3.py`):

| specification | subjects | strata | mean delta | positive | Wilcoxon p |
|---|---|---|---|---|---|
| A exact class sets + prior to 0.01 | 32 | 854 | **-0.1036** | 0/32 | <1e-6 |
| B class sets + prior bin 0.1 | 32 | 820 | -0.1036 | 0/32 | <1e-6 |
| C class sets only | 32 | 734 | -0.1034 | 0/32 | <1e-6 |
| D class sets + prior + block index | 32 | 930 | -0.1050 | 0/32 | <1e-6 |
| E exact, at least 3 blocks per stratum | 32 | 791 | -0.1019 | 0/32 | <1e-6 |
| F balanced strata only | 32 | 735 | -0.1035 | 0/32 | <1e-6 |

**Conclusion: matching on class composition does not change the sign or the size of the sleep effect. Under every
specification the matched difference is about -0.10 with no positive subject.**

## What this does not regenerate

The supplement's structure-matched **concentration** contrast (+0.050, 19/28 subjects, sign test p = 0.087) is a
different quantity: it compares blocks of high and low class concentration inside a stratum, not corrected versus
uncorrected blocks. The archived cells do not store per-block class concentration, so that number could not be
regenerated in this round. It remains **un-verified** and must not be treated as reproduced.

## Consequence for the paper

- The matched correction-vs-none robustness check can be added to the main text as a new sentence; it strengthens
  the negative result.
- The concentration contrast stays exploratory and un-regenerated; the supplement already labels it exploratory,
  but a reader should also be told it has not been recomputed from the archive. That sentence is added in this
  round.
