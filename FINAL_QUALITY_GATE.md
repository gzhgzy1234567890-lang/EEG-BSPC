# FINAL_QUALITY_GATE.md

Phase A audit against the 100-point rubric of the research goal. Scores below are for **execution quality of
Phase A**, not for the whole project and not for publication readiness.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A versions and traceability | 15 | 13 | AUDIT_BASELINE.md, AUTO/commit history, FILE inventory | two claim rows in CLAIM_EVIDENCE_MATRIX.csv still carry hand-entered numbers without their own generated CSV |
| B information access and protocol | 20 | 12 | EVENT_AND_WINDOW_AUDIT.md, test_two_sided_ext.py output, PROTOCOL_CAUSAL_V16 Rev D | 2a cue latency asserted from documentation, not measured; 2a/2b windows differ and are not reconciled |
| C mathematics and theory | 15 | 0 | - | Phase C not started |
| D statistics | 15 | 7 | STATISTICAL_ANALYSIS_PLAN.md, results/statistics_recomputed_2b.json, recompute_2b.py | Holm not executed (family has one live test); sleep hierarchy not yet recomputed |
| E mechanism and confounding | 10 | 4 | CURRENT_BLOCKERS.md, CLAIM_EVIDENCE_MATRIX.csv | D phase not started |
| F literature and novelty | 10 | 0 | - | NOVELTY_MATRIX.md not written |
| G reproducibility | 10 | 7 | commits 8660894, scripts, JSON, this gate | no third-party replication; SEED blocked |
| H manuscript consistency | 5 | 2 | manuscript cites the current commit; FREEZE CHECK PASS | manuscript still describes the 2a window incorrectly (flagged, not yet fixed) |
| **total** | **100** | **45** | | |

## Hard gates

| gate | status | evidence |
|---|---|---|
| unrepaired data leakage | PASS (none found; past-only assertions pass) | test_two_sided_ext.py |
| wrong proof | N/A (no proofs yet) | - |
| core numbers not recomputable | PASS for 2b (independent recompute matches); NOT CHECKED for sleep-EDF | statistics_recomputed_2b.json |
| code contradicts paper | **FAIL**: the manuscript's 2a window sentence contradicts the code | EVENT_AND_WINDOW_AUDIT.md |
| post-hoc selection called confirmation | PASS (2a labelled exploratory) | CLAIM_EVIDENCE_MATRIX.csv |
| target labels in a "label-free" method | PASS | protocol, S31/S33 texts |
| unfinished experiment reported as done | PASS | CURRENT_BLOCKERS.md |
| SEED claimed end-to-end causal | PASS (marked BLOCKED) | CURRENT_BLOCKERS.md B1 |
| incorrect multiplicity | PASS (family frozen before tests) | STATISTICAL_ANALYSIS_PLAN.md |
| non-significant reported as significant | PASS (2a filter effect p=0.13 stated) | protocol Rev C/D |
| filter difference attributed solely to future access | PASS (stated as a limitation) | AUDIT_BCI2B_EA.md, protocol |
| hash match called scientific correctness | PASS (never claimed) | this file |
| AI rerun called third-party | PASS | REPRODUCIBILITY.md |
| tests reported without running | PASS (all runs logged) | GOAL_ROUND_LOG.md |
| unverified "first" claims | PASS (none used) | - |

## Verdict

**Phase A: FAIL.** One hard gate is open (the manuscript's window sentence contradicts the code), and the score
is 45/100. The open gate is a text defect, not a data defect: the archived results were produced by the code, and
the fix is to correct the sentence and to state the 2a/2b window difference. That fix is the first action of the
next round.

## What is not claimed here

- This is not a publication-readiness statement.
- The 45/100 is an execution score for Phase A only.
