# FINAL_QUALITY_GATE.md

Updated after C2 (certificate on real data), E1 (novelty matrix from fetched abstracts) and D1 (controlled
generator, 50/50 sign agreement).

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 13 | AUDIT_BASELINE.md; commits 5092c92 -> 2da0320 | two claim rows hand-entered |
| B | 20 | 16 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py; window sentence fixed | 2a cue latency from documentation |
| C | 15 | 13 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2_CERTIFICATE_RESULTS.md | Prop 5 sign version open |
| D | 15 | 9 | STATISTICAL_ANALYSIS_PLAN.md; statistics_recomputed_2b.json; D1 grid | sleep-EDF hierarchy not re-derived; Holm not executed |
| E | 10 | 8 | NOVELTY_MATRIX.md (4 abstracts fetched); SLEEP_MECHANISM_AUDIT.md (D1, D2-D4 recaps, D5 open) | full texts unread; D5 not run |
| F | 10 | 3 | CURRENT_BLOCKERS.md | SEED blocked; no external validation report |
| G | 10 | 7 | commits, scripts, JSON, seeds | no third-party replication |
| H | 5 | 3 | manuscripts cite the current commit; theory and D results not yet in the manuscript | integration pending |
| **total** | **100** | **72** | | |

## Hard gates

All pass at this commit. Evidence: for each gate, the path is named in the previous version of this file; the
newest checks are the 50/50 D1 sign agreement (theory-to-simulation) and the exact C2 certificate on three real
subjects.

## Verdict

**Not approved** (72 < 96). Remaining: D5, sleep-EDF hierarchy recomputation, manuscript integration of B/C/D,
external validation report, two adversarial reviews.

## Next (automatic)

1. D5: LDA priors (empirical vs uniform) and threshold controls on sleep-EDF;
2. B3: hierarchy recomputation from archived JSONs;
3. G: integrate theory and the 2b/2a results into the manuscript.
