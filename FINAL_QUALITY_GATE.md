# FINAL_QUALITY_GATE.md

Revision 6, after a Monte Carlo validation of the corrected coefficient was added.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | claim matrix; provenance; changelog; CODE_MAP | - |
| B | 20 | 18 | event and window audit | - |
| C | 15 | 15 | THEORY_PROOFS rev 2; theory_test_rev2; **Monte Carlo over 27 cells validates the corrected coefficient** (exact within 0.0009, second order within 0.9 per cent at d = 0.1); certificate on nine subjects | the errors existed and were found by the referee, not by this gate |
| D | 15 | 14 | statistical audit; intervals; equivalence margin | - |
| E | 10 | 10 | mechanism audit | - |
| F | 10 | 10 | novelty matrix on full texts | - |
| G | 10 | 9 | reproducibility report; CODE_MAP | no third-party replication |
| H | 5 | 5 | archive synced; consistency check PASS | - |
| **total** | **100** | **96** | | |

## What this means, and what it does not

The score reaches the numeric threshold for the first time, and it does so **after** the theory was corrected and
independently validated rather than before. It does not mean the paper is ready to submit:

- the referee's P2 item on independent end-to-end replication is still open;
- the SEED waveform-level rerun is still blocked;
- the referee's own 5-point scale rated theory rigour 2.5 at the previous version, and this revision has not been
  reviewed again.

## Score history

| revision | score | reason |
|---|---|---|
| pre-referee | 95 | gate claimed theory verified |
| MC1-MC4 | 89 | wrong proofs found externally |
| MC5-MC7 | 92 | evidence tiers, equivalence, abstract |
| P2 certificate | 93 | nine subjects |
| table 9 / positioning / code map | 95 | archive and traceability |
| Monte Carlo validation | 96 | the corrected formula now has a quantitative check |
