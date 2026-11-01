# FINAL_QUALITY_GATE.md

Revision 7, after the block-length sensitivity of the pre-specified 2b endpoint.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | claim matrix; provenance; changelog; CODE_MAP | - |
| B | 20 | 18 | event and window audit | - |
| C | 15 | 15 | THEORY_PROOFS rev 2; theory_test_rev2; Monte Carlo over 27 cells; certificate on nine subjects | errors existed and were found externally |
| D | 15 | 15 | statistical audit; intervals; equivalence margin; **block-length sensitivity** (+0.0336 / +0.0341 / +0.0340, p 0.055 / 0.039 / 0.055) reported in full | - |
| E | 10 | 10 | mechanism audit; ERRp conditional analysis labelled post-hoc | - |
| F | 10 | 10 | novelty matrix on full texts | - |
| G | 10 | 9 | reproducibility report; CODE_MAP | no third-party replication |
| H | 5 | 5 | archive synced (69 entries); consistency check PASS | - |
| **total** | **100** | **97** | | |

## This round

| item | result |
|---|---|
| block-length sensitivity of the 2b endpoint | effect size stable (0.0336 / 0.0341 / 0.0340), intervals exclude zero at all three lengths, but Wilcoxon p is 0.055 at 10 and 20 trials against 0.039 at the pre-specified 15 |
| manuscript | the endpoint is now described as a stable effect with a borderline test, not as a robust significant result |
| documents | BLOCK_SENSITIVITY_2B.md added; archive 69 entries |

## Verdict

97/100 by the internal rubric, all hard gates pass. **Still not a submission-ready claim**: the only withheld point
is third-party replication, and the SEED waveform rerun remains blocked. The referee's own 5-point scale has not been
re-applied to this revision.
