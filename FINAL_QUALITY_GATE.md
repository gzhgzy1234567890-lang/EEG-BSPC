# FINAL_QUALITY_GATE.md

Final gate for this iteration. Scored against the 100-point rubric with evidence paths.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | AUDIT_BASELINE.md; manuscript tracked; commits 5092c92 -> 338816b | two rows in CLAIM_EVIDENCE_MATRIX.csv still hand-entered |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py; causal 2x2 | BCI-2a cue latency from documentation, not measured |
| C | 15 | 14 | THEORY_PROOFS.md; THEORY_TEST_RESULTS.md; C2; manuscript 2.3 | Prop 5 sign version open by construction |
| D | 15 | 13 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json; Holm wording | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md: D1 50/50, D5 +0.003, D4 1,763/3,220 rechecked (unseen mass 0.412 vs 0.000) | - |
| F | 10 | 7 | NOVELTY_MATRIX.md; SPDIM/BBSE cited; EXTERNAL_VALIDATION_REPORT.md | full texts of SPDIM, PRED and NeuroAdapt-Bench unread; no external dataset |
| G | 10 | 8 | REPRODUCIBILITY_REPORT.md lists the commands, seeds and outputs actually run | no third-party replication |
| H | 5 | 5 | abstract, highlights, sections 2.3/4.8, conclusion all updated; 12 numbers cross-checked; FREEZE CHECK PASS | - |
| **total** | **100** | **88** | | |

## Hard gates

All fifteen pass at 338816b.

## Verdict

**Not approved as complete.** 88/100 is below the 96 threshold, and the shortfall is concentrated in F and G, whose
remaining items require resources this environment does not have:

| id | blocker | points withheld |
|---|---|---|
| B1 | SEED raw waveforms absent (verified: only ExtractedFeatures, no .cnt) | part of F |
| B2 | no third-party replication | part of G |
| B4 | no dataset outside the development corpora | part of F |

Every executable task inside those items has been done and documented: the novelty matrix is built from fetched
abstracts, SPDIM and BBSE are cited and the claim narrowed, the reproducibility report lists the exact commands
and seeds, and the SEED record states precisely what is blocked and how to unblock it.

## Honest statement

The paper is internally consistent, evidence-graded, and its core numbers are independently recomputable from the
archived files. It is not a completed top-venue submission: it lacks an external dataset, a third-party run, and
full-text verification of three related papers. Those are the three things that would most raise acceptance odds,
and none of them can be produced from inside this environment.
