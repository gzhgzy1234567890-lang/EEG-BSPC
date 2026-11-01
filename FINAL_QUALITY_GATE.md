# FINAL_QUALITY_GATE.md

Revision 4, after the referee's P2 item (certificate scope) was addressed.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 14 | claim matrix; provenance; response document | previous gate certified wrong proofs before external review |
| B | 20 | 18 | event and window audit | - |
| C | 15 | 14 | THEORY_PROOFS rev 2; theory_test_rev2.py; certificate now on all nine subjects (793 trials, agreement 1.000) | three errors had to be corrected |
| D | 15 | 14 | statistical audit; external tests with intervals and an equivalence margin | - |
| E | 10 | 10 | mechanism audit; wording limited to locating the component | - |
| F | 10 | 10 | novelty matrix on full texts | - |
| G | 10 | 9 | reproducibility report | no third-party replication |
| H | 5 | 4 | MANIFEST/freeze/gate synced; abstract 219 words; consistency check PASS | archive had been stale earlier |
| **total** | **100** | **93** | | |

## P2 progress this round

| item | state |
|---|---|
| widen the certificate demonstration | **done**: all nine BCI-2b subjects, 793 scored trials, agreement 1.000 in every subject, flip rates 0.027-0.361 |
| SEED waveform-level causal rerun | blocked, documented |
| independent end-to-end replication | blocked, documented |

## Remaining before a second-round submission

Nothing that this environment can do for the two blocked items. Everything else the referee listed as P0 and P1 is
closed, with one deliberate exception recorded honestly: the theory was wrong when shipped, and the gate that
passed it has been regraded rather than restored.
