# FINAL_QUALITY_GATE.md

Revision 5, after the consolidated evidence table, the positioning paragraph and the code map.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | CLAIM_EVIDENCE_MATRIX; FILE_PROVENANCE; MANUSCRIPT_CHANGELOG; CODE_MAP maps every result to its script | - |
| B | 20 | 18 | event and window audit | - |
| C | 15 | 14 | THEORY_PROOFS rev 2; theory_test_rev2; certificate on nine subjects | three errors corrected rather than prevented |
| D | 15 | 14 | statistical audit; intervals and equivalence margin for the external corpora | - |
| E | 10 | 10 | mechanism audit; locating wording | - |
| F | 10 | 10 | novelty matrix on full texts | - |
| G | 10 | 9 | REPRODUCIBILITY_REPORT; CODE_MAP | no third-party replication |
| H | 5 | 5 | Table 9 consolidates every headline result with its class; MANIFEST, freeze and gate synced; consistency check PASS | - |
| **total** | **100** | **95** | | |

## This round

| item | change |
|---|---|
| MC5 | Table 9 added: every headline result with estimate, interval, evidence class and what it does not establish |
| MC8 | positioning paragraph: the model is explanatory, not a theory of domain adaptation; the certificate is an identity |
| MC9 | CODE_MAP.md: script -> output -> seed for every number, plus what the archive does not contain |

## Hard gates

All pass.

## Verdict

**Not complete.** 95/100, one point withheld for the absence of any third-party execution, and the SEED
raw-waveform rerun remains blocked. Neither can be produced in this environment.

## What changed in the score history, honestly

| revision | score | reason |
|---|---|---|
| pre-referee | 95 | gate claimed theory verified |
| after MC1-MC4 | 89 | the theory was wrong when shipped; regraded |
| after MC5-MC7 | 92 | evidence tiers, equivalence framing, abstract |
| after P2 certificate | 93 | nine subjects instead of three |
| after table, positioning, code map | 95 | archive and traceability complete |

The score returned to 95 only after the errors were found by someone else. That is recorded here so the number is
not mistaken for a validation.
