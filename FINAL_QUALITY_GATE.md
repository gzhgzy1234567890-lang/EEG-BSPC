# FINAL_QUALITY_GATE.md

Updated after the concentration contrast was tested and withdrawn.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | AUDIT_BASELINE.md; commits to 0251498 | two claim rows hand-entered |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 14 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2 | Prop 5 sign version open |
| D | 15 | 13 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; D3_MATCHED_REGENERATION.md; CONCENTRATION_RECONCILIATION.md | - |
| F | 10 | 8 | NOVELTY_MATRIX.md; RELATED_WORK_VERIFICATION.md; NOVELTY_RISK_REPORT.md | full texts unread |
| G | 10 | 9 | REPRODUCIBILITY_REPORT.md; every claimed number now either regenerated or withdrawn | no third-party replication |
| H | 5 | 5 | supplement states the withdrawal; FREEZE CHECK PASS | - |
| **total** | **100** | **90** | | |

## Hard gates

All pass. The "unrecomputable core result" gate is cleaner than last round: a secondary claim that could not be
recomputed has been **withdrawn** rather than left standing, and the paper now contains no number that this
environment cannot regenerate.

## Verdict

**Not approved as complete** (90 < 96). The remaining points are the three external items (SEED waveforms, external
dataset, third-party replication) plus full-text literature verification.

## Note on what the withdrawal costs

The removed number was exploratory, positive and non-significant (p = 0.087). Removing it does not weaken the main
result: the sleep effect is -0.10 with 32/32 subjects negative and is now shown to be insensitive to class
composition matching (six specifications) and to training priors (0.003 change).
