# FINAL_QUALITY_GATE.md

Updated after: window fix (A), Phase C1 theory, C2 certificate on real data, E1 novelty matrix.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 13 | AUDIT_BASELINE.md; commits 5092c92 -> ... -> b81f5ef | two claim rows still hand-entered |
| B | 20 | 16 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py; window sentence fixed | 2a cue latency from documentation, not measured |
| C | 15 | 12 | THEORY_PROOFS.md (Props 1-4 proved, 5 weakened), THEORY_TEST_RESULTS.md, C2_CERTIFICATE_RESULTS.md (certificate exact on 3 subjects) | C5 (theory-to-simulation link) not done; Prop 5 sign version open |
| D | 15 | 8 | STATISTICAL_ANALYSIS_PLAN.md; statistics_recomputed_2b.json | sleep-EDF hierarchy not yet re-derived; Holm not executed (family has one live test) |
| E | 10 | 7 | NOVELTY_MATRIX.md built from fetched abstracts | full texts not read; MOABB coverage unchecked |
| F | 10 | 3 | CURRENT_BLOCKERS.md B1/B2 | SEED blocked; no external validation report; no third-party run |
| G | 10 | 7 | commits, scripts, JSON, seeds | no third-party replication |
| H | 5 | 3 | window sentence fixed; theory not yet integrated into the manuscript | manuscript still lacks the new theory and the 2b numbers |
| **total** | **100** | **69** | | |

## Hard gates

All fifteen gates pass at this commit. The most recently closed one was "code contradicts paper" (window sentence).
Proofs: Props 1-4 verified numerically; Prop 5 explicitly weakened where the counterexample failed, and the
failed attempt is recorded in THEORY_TEST_RESULTS.md rather than hidden.

## Verdict

**Not approved.** 69/100 is below 96 and Phase D, F and G are incomplete. The project continues; no completion
claim is made.

## Next (automatic)

1. Phase D1: controlled generator with the frozen grid (baseline shift x prior shift x duration x memory), run it;
2. Phase D3: matched mechanism analysis with the corrected within-subject-by-stratum procedure;
3. Phase B: sleep-EDF hierarchy recomputation from the archived JSONs.
