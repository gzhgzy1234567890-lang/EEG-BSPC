# FINAL_QUALITY_GATE.md

Revision 3, after the referee's P0 and P1 items.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | claim matrix; provenance; response document | the gate certified wrong proofs before external review |
| B | 20 | 18 | event and window audit with the official 2a description | - |
| C | 15 | 13 | THEORY_PROOFS rev 2 (coefficient, residual, threshold, constrained weight, finite-sample sign flip); theory_test_rev2.py passes | three errors had to be corrected; correct now, wrong when shipped |
| D | 15 | 14 | statistical audit; both independent tests now carry bootstrap intervals and an equivalence margin | - |
| E | 10 | 10 | mechanism audit and limitations; wording limited to locating the component | - |
| F | 10 | 10 | novelty matrix on full texts | - |
| G | 10 | 9 | reproducibility report | no third-party replication |
| H | 5 | 4 | MANIFEST, freeze and gate regenerated; abstract 219 words; consistency check PASS | the archive had been stale before this round |
| **total** | **100** | **92** | | |

## What changed in this round

| item | change |
|---|---|
| MC5 | the five-test family is now described as pre-specified but **not** as five independent confirmations; SEED's uncontrolled preprocessing, the development use of 2a/2b and the two failing datasets are stated in the same paragraph |
| MC6 | "inert" removed everywhere; P300 now reports -0.0005 [-0.0024, +0.0012] and ERRp -0.0044 [-0.0166, +0.0075] against a 0.02 equivalence margin, with the explicit statement that the intervals lie inside the margin but the decoders are too weak to support equivalence |
| MC7 | mechanism wording limited to locating the class-mix component under an oracle diagnostic |
| minor 1 | pair counting corrected to "three per subject, 27 in total" |
| minor 3 | references 23 and 25 carry venue and year |
| minor 4 | abstract compressed from 262 to 219 words and relieved of secondary numbers |
| minor 5 | the practical paragraph no longer implies that partial strength is a validated safe setting |

## Hard gates

All pass at this revision. The wrong-proof failure of the previous revision is recorded in the history rather than
overwritten.

## Not claimed

- that a third-party replication exists;
- that the paper would now be accepted: the referee's second-round conditions include full-text verification of the
  remaining claims and a further check of the evidence tiers, which this round addresses but does not discharge.
