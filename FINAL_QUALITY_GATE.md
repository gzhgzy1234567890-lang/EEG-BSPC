# FINAL_QUALITY_GATE.md

Updated after F (external validation + SEED blocked) and G (theory 2.3 and protocol audit 4.8 integrated).

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 13 | AUDIT_BASELINE.md; commits 5092c92 -> 5ad1040 | two claim rows hand-entered |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py; window sentence fixed | 2a cue latency from documentation |
| C | 15 | 14 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2_CERTIFICATE_RESULTS.md; theory now in manuscript 2.3 | Prop 5 sign version open |
| D | 15 | 12 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json | Holm bookkeeping nominal |
| E | 10 | 9 | SLEEP_MECHANISM_AUDIT.md (D1 50/50, D5 +0.003) | D4 not re-derived from raw cells this round |
| F | 10 | 6 | NOVELTY_MATRIX.md; EXTERNAL_VALIDATION_REPORT.md; SEED_RAW_CAUSAL_BLOCKED.md | full texts unread |
| G | 10 | 7 | commits, scripts, JSON, seeds | no third-party replication |
| H | 5 | 4 | theory 2.3 and 4.8 integrated; commits cited consistently | abstract/highlights not yet updated to the new claims |
| **total** | **100** | **82** | | |

## Hard gates

All pass at this commit.

## Verdict

**Not approved** (82 < 96). Remaining: abstract/highlights update, two adversarial reviews, third-party replication.

## Next (automatic)

1. update abstract, highlights and conclusion to the evidence classes now in the paper;
2. two adversarial reviews (methods/statistics; theory/novelty) with page-level objections;
3. final consistency pass and gate re-score.
