# FINAL_QUALITY_GATE.md

Updated after the Reviewer 1 fixes (M1, M2, M3) and a numeric consistency check across the documents.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | AUDIT_BASELINE.md; manuscript in repo; commits up to 146d4b8 | two claim rows hand-entered |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 14 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2; manuscript 2.3 | Prop 5 sign version open |
| D | 15 | 13 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json; Holm wording fixed | - |
| E | 10 | 9 | SLEEP_MECHANISM_AUDIT.md | D4 not re-derived from raw cells |
| F | 10 | 7 | NOVELTY_MATRIX.md; SPDIM and BBSE cited | full texts unread |
| G | 10 | 7 | commits, scripts, JSON, seeds | no third-party replication |
| H | 5 | 4 | R1 fixes applied; consistency check run (12 key numbers present; highlights 60-79 chars) | conclusion not re-checked line by line |
| **total** | **100** | **85** | | |

## Hard gates

All pass at this commit.

## Verdict

**Not approved** (85 < 96). The remaining gap is almost entirely F and G: no third-party replication and no
external dataset, both of which are outside this environment. Within the controllable scope the manuscript is now
internally consistent, evidence-graded, and review-hardened.

## Remaining blockers

| id | blocker | consequence |
|---|---|---|
| B1 | SEED waveforms absent | the SEED claim stays at past-only-on-released-features |
| B2 | no third-party end-to-end replication | reproducibility is internal only |
| B4 | no dataset outside the development corpora | external validity limited to "corpora studied" |

## Next (automatic)

1. line-by-line pass of the conclusion against the new evidence classes;
2. reproducibility report update with the actual commands of this round;
3. final gate re-score; if only B1/B2/B4 remain, the project must be reported as BLOCKED for those items, not
   COMPLETE.
