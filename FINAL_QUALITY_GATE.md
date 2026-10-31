# FINAL_QUALITY_GATE.md

Final gate of this iteration, after the claim matrix was rebuilt and an automated cross-document consistency check
was run.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | CLAIM_EVIDENCE_MATRIX.csv rebuilt (16 rows, one WITHDRAWN); FILE_PROVENANCE.csv; MANUSCRIPT_CHANGELOG.md | - |
| B | 20 | 18 | EVENT_AND_WINDOW_AUDIT.md with the official 2a description cited [26] | 2a timing verified from the published description rather than from local raw annotations |
| C | 15 | 15 | THEORY_PROOFS.md; THEORY_COUNTEREXAMPLES.md; THEORY_TEST_RESULTS.md | - |
| D | 15 | 13 | STATISTICAL_AUDIT.md; two pre-registered independent tests | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; MECHANISM_LIMITATIONS.md; three regenerations | - |
| F | 10 | 10 | NOVELTY_MATRIX.md on full texts; two independent corpora | - |
| G | 10 | 9 | REPRODUCIBILITY_REPORT.md; every claim regenerable or withdrawn | **no third-party replication** |
| H | 5 | 5 | `consistency_check.py`: all 10 abstract numbers appear in the body, all 16 claim locations resolve, all 10 freeze hashes match | - |
| **total** | **100** | **95** | | |

## Hard gates

All fifteen pass.

## Verdict

**Not complete.** 95/100 with one point withheld for the absence of third-party replication; the SEED waveform gap
is documented and does not enter the score because no claim depends on it.

The remaining gap cannot be closed from inside this environment: it requires an external group to execute the
package. The project is therefore **BLOCKED** on that item, not complete.

## Automated evidence for the consistency score

```
abstract numbers: 0.001 0.003 0.008 0.011 0.034 0.071 0.091 0.102 0.108 0.214
numbers in abstract but not in body: []
claims whose manuscript location is not a known section: []
freeze rows 10 mismatches []
CONSISTENCY PASS
```
