# FINAL_QUALITY_GATE.md

Updated after the D3 matched regeneration and the novelty-risk documents.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | AUDIT_BASELINE.md; commits to a4fb0dc | two claim rows hand-entered |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 14 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2 | Prop 5 sign version open |
| D | 15 | 13 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; D3_MATCHED_REGENERATION.md (six specs, -0.104, 0/32) | the supplement's concentration contrast remains un-regenerated and is now labelled as such |
| F | 10 | 8 | NOVELTY_MATRIX.md; RELATED_WORK_VERIFICATION.md; NOVELTY_RISK_REPORT.md; SPDIM/BBSE cited | full texts unread (PDF fetch rejected) |
| G | 10 | 8 | REPRODUCIBILITY_REPORT.md; per-block records archived | no third-party replication |
| H | 5 | 5 | main text and supplement annotated consistently; FREEZE CHECK PASS | - |
| **total** | **100** | **89** | | |

## Hard gates

All pass at a4fb0dc. The D3 regeneration is the reason one of them stays clean: a matched analysis that had only
been run once is now recomputed under six specifications, and the one contrast that could not be recomputed is
labelled in the supplement rather than left implicit.

## Verdict

**Not approved as complete** (89 < 96). Remaining shortfall: external dataset (B4), third-party replication (B2),
SEED waveforms (B1), and full-text reading of three papers.

## Next (automatic)

1. attempt the concentration contrast regeneration with a per-block concentration dump (one more pipeline pass);
2. if it succeeds, either confirm +0.050 or replace it with the regenerated number.
