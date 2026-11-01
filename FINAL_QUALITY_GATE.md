# FINAL_QUALITY_GATE.md

Revision after the independent referee report. **The previous gate was wrong**: it reported "theory verified, all
hard gates pass" while Proposition 3's second-order coefficient and Proposition 3b's residual sign were incorrect.
That is a hard-gate event ("an explicitly wrong proof"), it was found by external review rather than by this gate,
and it is now repaired.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | claim matrix rebuilt; provenance; changelog | the gate itself certified wrong proofs before external review, which is an A failure |
| B | 20 | 18 | window and event audit with the official 2a description cited | - |
| C | 15 | 12 | THEORY_PROOFS rev 2; THEORY_TEST_RESULTS rev 2; theory_test_rev2.py passes at a != sigma | three errors had to be corrected (coefficient, residual sign, threshold dimension); the proofs are now right but the first version was not |
| D | 15 | 13 | statistical audit; two pre-registered tests | - |
| E | 10 | 10 | mechanism audit; limitations | - |
| F | 10 | 10 | novelty matrix on full texts | - |
| G | 10 | 9 | reproducibility report | no third-party replication |
| H | 5 | 3 | MANIFEST and freeze regenerated; **MANIFEST had been stale (18 pages, 9,345 words) against a 20-page manuscript** | archive inconsistency found by the referee |
| **total** | **100** | **89** | | |

## Hard gates

| gate | status |
|---|---|
| wrong proof | **FAILED in the shipped version** (second-order coefficient, residual sign), repaired in revision 2 |
| unrecomputable core result | pass: the referee's four counterexamples were reproduced locally before any edit |
| code contradicts paper | pass |
| incorrect multiplicity | pass |
| others | pass |

## What this costs

The score drops from 95 to 89 not because new work failed but because the earlier certification was too generous.
A gate that passes a document with a wrong coefficient is not a gate. The correction is verified: the coefficient
is now (a d^2 / (2 s^3)) phi(a/s), the residual is (1 - lambda) b - lambda c, the threshold is defined in feature
space, the weight is clipped to [0, 1], and the finite-sample sign flip is proved. Every one of these is covered by
a test that fails if the error returns.

## Not claimed

- that the paper is now correct in every respect: this round repaired the theory and the archive consistency; the
  evidence grading (MC5), the equivalence framing of the two null external results (MC6) and the mechanism wording
  (MC7) are next;
- that the gate is trustworthy without external review: it demonstrably is not.
