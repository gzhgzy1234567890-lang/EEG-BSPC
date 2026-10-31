# FINAL_QUALITY_GATE.md

Updated after the **cross-session independent** test on the BCI-challenge error-potential corpus.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | FILE_PROVENANCE.csv; MANUSCRIPT_CHANGELOG.md; two pre-registrations committed before their runs | - |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 15 | THEORY_PROOFS.md; THEORY_COUNTEREXAMPLES.md; THEORY_TEST_RESULTS.md | - |
| D | 15 | 13 | STATISTICAL_AUDIT.md; P300 and ERRp pre-registrations and results | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; MECHANISM_LIMITATIONS.md; three regenerations | - |
| F | 10 | 10 | NOVELTY_MATRIX.md on full texts; **two independent corpora**, one of them cross-session | - |
| G | 10 | 9 | REPRODUCIBILITY_REPORT.md; every number regenerated, withdrawn or newly produced | no third-party replication |
| H | 5 | 4 | both independent results in the Discussion; **word count wrong twice** before being fixed | repeated count slips, so not a full mark |
| **total** | **100** | **93** | | |

## What the two independent tests establish

| corpus | structure | result | reading |
|---|---|---|---|
| P300 speller | single session, 16 subjects | -0.0005, 7/16 positive | inert: no displacement to remove; the pre-registered prediction of harm **failed** and is reported as such |
| BCI challenge (error potentials) | five sessions per subject, four forward pairs | -0.0044, 6/16 positive, sign p = 0.45 | inert at near-chance decoding; bounds the effect size, does not test the sign |

Neither supports a strong cross-session effect, and neither contradicts the sleep harm or the BCI gain at the
decoding strengths where those were measured. Both are labelled as exploratory independent results.

## Hard gates

All pass. "Unfinished experiment reported as done" stays clean: the ERRp run's non-zero shell exit was traced to
PowerShell treating warnings on stderr as an error; the analysis itself completed and wrote all 16 subjects.

## Verdict

**Not approved as complete** (93 < 96). The remaining three points are the third-party replication and the SEED
waveforms; the independent-dataset item is now addressed twice over.
