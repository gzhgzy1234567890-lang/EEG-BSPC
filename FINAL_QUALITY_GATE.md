# FINAL_QUALITY_GATE.md

Updated after the window-sentence fix (closing the Phase A hard gate) and Phase C1 (theory foundations).

## Phase A — PASS on the hard gates, score updated

| item | max | score | evidence |
|---|---:|---:|---|
| A versions and traceability | 15 | 13 | AUDIT_BASELINE.md; commits 5092c92 -> b095b44 -> 8660894 -> 8be54e9 -> 6abf2bb |
| B information access and protocol | 20 | 16 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py (K=2,3,4; future-perturbation invariance <1e-12); window sentence corrected to state 2a = cue+0..4 s and 2b = cue+0.5..3.5 s |
| C mathematics and theory | 15 | 9 | THEORY_PROOFS.md (Props 1-4 proved, 5 weakened after the counterexample failed), THEORY_TEST_RESULTS.md (formula vs Monte Carlo <1e-3; certificate 400/400) |
| D statistics | 15 | 8 | STATISTICAL_ANALYSIS_PLAN.md; statistics_recomputed_2b.json (independent recompute matches) |
| E mechanism and confounding | 10 | 4 | CURRENT_BLOCKERS.md; D phase not started |
| F literature and novelty | 10 | 0 | NOVELTY_MATRIX.md not written |
| G reproducibility | 10 | 7 | commits, scripts, JSON; no third-party replication; SEED blocked |
| H manuscript consistency | 5 | 3 | window sentence fixed; new theory not yet in the manuscript |
| **total** | **100** | **60** | |

## Hard gates

| gate | status | evidence |
|---|---|---|
| unrepaired data leakage | PASS | past-only assertions |
| wrong proof | PASS so far | Props 1-4 checked numerically; Prop 5 explicitly weakened and marked open where not proved |
| core numbers not recomputable | PASS for 2b; sleep-EDF not yet re-derived | statistics_recomputed_2b.json |
| **code contradicts paper** | **PASS** (was FAIL) | preprocessing sentence now states trial-relative windows and the 2a/2b difference |
| post-hoc selection called confirmation | PASS | CLAIM_EVIDENCE_MATRIX.csv |
| target labels in a "label-free" method | PASS | protocol |
| unfinished experiment reported as done | PASS | CURRENT_BLOCKERS.md |
| SEED claimed end-to-end causal | PASS (BLOCKED) | CURRENT_BLOCKERS.md |
| incorrect multiplicity | PASS | STATISTICAL_ANALYSIS_PLAN.md |
| non-significant reported as significant | PASS | protocol Rev C/D |
| filter difference attributed solely to future access | PASS | AUDIT_BCI2B_EA.md |
| hash match called correctness | PASS | - |
| AI rerun called third-party | PASS | REPRODUCIBILITY.md |
| tests reported without running | PASS | GOAL_ROUND_LOG.md |
| unverified "first" claims | PASS | NOVELTY_MATRIX still empty, nothing claimed |

## Verdict

**Phase A hard gates: PASS. Phase A score 60/100 (below the 96 threshold, so Phase A is not marked approved as a
whole).** Phase C is partially complete (C1, C3, C4 attempted; C2 and the theory-to-simulation link still open).

## Not claimed

- publication readiness;
- that the theory is novel (the novelty matrix has not been written);
- third-party reproduction.
