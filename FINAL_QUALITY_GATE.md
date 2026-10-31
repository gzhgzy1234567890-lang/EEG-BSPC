# FINAL_QUALITY_GATE.md

Updated after abstract/highlights rewrite, manuscript tracked in the repository, the two adversarial reviews, and
the SPDIM/BBSE citation fix.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | AUDIT_BASELINE.md; manuscript tracked in repo; commits up to dc37187 | two claim rows hand-entered |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 14 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2_CERTIFICATE_RESULTS.md; manuscript 2.3 | Prop 5 sign version open |
| D | 15 | 12 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json | Holm vacuous with one test; now stated |
| E | 10 | 9 | SLEEP_MECHANISM_AUDIT.md | D4 not re-derived from raw cells |
| F | 10 | 7 | NOVELTY_MATRIX.md; SPDIM and BBSE now cited with the claim narrowed | full texts unread |
| G | 10 | 7 | commits, scripts, JSON, seeds | no third-party replication |
| H | 5 | 4 | abstract, highlights, sections 2.3/4.8 updated | Reviewer 1 M1 (2a emphasis) not yet addressed |
| **total** | **100** | **84** | | |

## Hard gates

All pass at this commit.

## Verdict

**Not approved** (84 < 96). Reviewer 2's blocking item (T2, SPDIM citation) is now fixed; Reviewer 1's M1 and M2
remain open and are the next round's work, together with the final consistency pass.

## Next (automatic)

1. M1: mark the 2a number inline as exploratory, or move 2a to the supplement;
2. M2: add the "implementation difference, not only future access" caveat to every abstract-level mention;
3. final consistency check (abstract numbers vs tables) and gate re-score.
