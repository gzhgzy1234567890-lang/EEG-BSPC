# FINAL_QUALITY_GATE.md

Updated after the independent P300 test (pre-registered, prediction failed, diagnosed and reported).

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | FILE_PROVENANCE.csv; MANUSCRIPT_CHANGELOG.md; PREREGISTRATION_P300 committed before the run | - |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 15 | THEORY_PROOFS.md; THEORY_COUNTEREXAMPLES.md; THEORY_TEST_RESULTS.md | - |
| D | 15 | 13 | STATISTICAL_AUDIT.md; preamble + results for P300 | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; MECHANISM_LIMITATIONS.md; three regenerations | - |
| F | 10 | 10 | NOVELTY_MATRIX.md on full texts; an **independent dataset** now used as a negative control | - |
| G | 10 | 9 | REPRODUCIBILITY_REPORT.md; every claimed number regenerated, withdrawn, or newly produced | no third-party replication |
| H | 5 | 4 | P300 result is in the Discussion; the counts were briefly wrong (10297 vs 10798) and are fixed | the count slip is a real consistency failure, so not a full mark |
| **total** | **100** | **93** | | |

## What the P300 test changed

It **added an independent dataset** (B4 partially addressed) and it **failed its own pre-registered prediction**.
The failure is diagnosed: source and target halves share their class composition, so the displacement is
approximately zero and the correction is inert (-0.0005, 7 of 16 positive). The paper now reports this as a
negative control and says the prediction was wrong.

## Hard gates

All pass. The relevant one here: "unfinished experiment reported as done" — the P300 test is finished and its
negative outcome is reported, not converted into a success.

## Verdict

**Not approved as complete** (93 < 96). Remaining: third-party replication (B2), SEED waveforms (B1), and a
**cross-session** independent dataset (the P300 data are single-session, so they cannot test cross-session transfer).
