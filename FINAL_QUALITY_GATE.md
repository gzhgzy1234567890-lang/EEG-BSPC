# FINAL_QUALITY_GATE.md

Updated after B3 (hierarchical recomputation) and D5 (LDA prior control).

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 13 | AUDIT_BASELINE.md; commits 5092c92 -> 5db810e | two claim rows hand-entered |
| B | 20 | 16 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 13 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2_CERTIFICATE_RESULTS.md | Prop 5 sign version open |
| D | 15 | 12 | STATISTICAL_AUDIT.md (subject -0.1023, 32/32, p=8e-7, CI [-0.1145, -0.0900]); statistics_recomputed_2b.json; holm not executed (family has one live test) | Holm bookkeeping still nominal |
| E | 10 | 9 | SLEEP_MECHANISM_AUDIT.md: D1 50/50, D5 priors +0.003 [-0.000, +0.006], D2-D4 graded | D4 BBSE recheck from raw cells not rerun this round |
| F | 10 | 4 | NOVELTY_MATRIX.md from 4 fetched abstracts | full texts unread; external validation report missing |
| G | 10 | 7 | commits, scripts, JSON, seeds | no third-party replication |
| H | 5 | 3 | commits cited; theory and D results not yet in the manuscript | integration pending |
| **total** | **100** | **77** | | |

## Hard gates

All pass at this commit.

## Verdict

**Not approved** (77 < 96). Remaining: manuscript integration (G), external validation report (F), two adversarial
reviews, and the SEED blocker.

## Next (automatic)

1. G: integrate the theory (Props 1-4), the 2a/2b results with evidence classes, and the D1/D5 controls into the
   manuscript;
2. F: write EXTERNAL_VALIDATION_REPORT.md and SEED_RAW_CAUSAL_BLOCKED.md;
3. G4: two adversarial reviews with page-level objections.
