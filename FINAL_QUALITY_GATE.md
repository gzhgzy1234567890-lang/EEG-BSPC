# FINAL_QUALITY_GATE.md

Updated after full texts of SPDIM, PRED and NeuroAdapt-Bench were obtained and read.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | AUDIT_BASELINE.md; commits to 3563551 | two claim rows hand-entered |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 14 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2 | Prop 5 sign version open |
| D | 15 | 13 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; D3 and concentration regenerations | - |
| F | 10 | 10 | NOVELTY_MATRIX.md built on **full texts**; RELATED_WORK_VERIFICATION.md; NOVELTY_RISK_REPORT.md; refs [23]-[25] cited | Bakas 2023 and Widmann 2015 unread directly |
| G | 10 | 9 | REPRODUCIBILITY_REPORT.md; every claimed number regenerated or withdrawn | no third-party replication |
| H | 5 | 5 | abstract, highlights, sections 2.3/4.8, conclusion, supplement all consistent; FREEZE CHECK PASS | - |
| **total** | **100** | **92** | | |

## Hard gates

All fifteen pass at 3563551.

## Verdict

**Not approved as complete** (92 < 96). The remaining four points are the three external dependencies:

| id | blocker | points withheld |
|---|---|---|
| B1 | SEED raw waveforms absent | 1-2 |
| B2 | no third-party replication | 1 |
| B4 | no dataset outside the development corpora | 1-2 |

## What the full-text check changed

It **lowered** one claim (the qualitative label-shift effect is prior art, cited) and **raised** one (SPDIM does
not contain a first-order decision-space analysis, so contribution B survives). The paper now cites the two
closest works and states exactly what is and is not new.
