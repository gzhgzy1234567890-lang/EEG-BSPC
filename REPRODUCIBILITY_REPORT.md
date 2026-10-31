# REPRODUCIBILITY_REPORT.md

Internal reproduction only. No third-party run exists.

## Environment

| item | value |
|---|---|
| OS | Windows, PowerShell |
| Python (analysis) | 3.7.9, numpy 1.21, scipy 1.7.3, scikit-learn 1.0, MNE 0.23.4 |
| Python (document tooling) | 3.12, python-docx |
| code commit | see STATUS.md at the end of each round |
| data roots | E:/data/BCICIV-2a, E:/data/BCICIV-2b, E:/data/sleep-edf, E:/data/SEED-all |

## Commands actually run in this round

| script | purpose | output |
|---|---|---|
| `sleep_edf/d4_recheck.py` | recount the support-valid split from the archived cells | 1,763 valid / 3,220 invalid (64.6%); unseen mass 0.412 vs 0.000 |
| `origin_equivariance/src/recompute_2b.py` | independent 2b table from JSON | csp +0.0341 [+0.0104, +0.0585], p = 0.0391 |
| `sleep_edf/b3_hierarchy.py` | hierarchy recomputation | 32 subjects, -0.1023, CI [-0.1145, -0.0900] |
| `origin_equivariance/src/test_two_sided_ext.py` | assertions K=2,3,4 | ALL ASSERTIONS PASSED |
| `origin_equivariance/src/theory_test.py` | Propositions 2-5 numerics | THEORY TEST PASS |
| `origin_equivariance/src/sim_d1.py` | 50-cell grid | sign matched 50/50 |
| `origin_equivariance/src/c2_certificate.py` | certificate on 3 subjects | agreement 1.000 |

## Seeds

Bootstrap and simulation seeds: 20261101 for every script in this paper. The seed is written in the source of
each script, not passed on the command line, so it cannot drift between runs.

## What a reader can reproduce here

1. every number in Tables 1-8, from the archived JSON/CSV in the repository;
2. every proposition, from the scripts above;
3. the document build, from the DOCX and the build script.

## What a reader cannot reproduce here

1. the raw EEG processing for SEED (no waveforms, see SEED_RAW_CAUSAL_BLOCKED.md);
2. a third-party end-to-end run: the only executions so far are by the authors and by this assistant;
3. the BCI and sleep pipelines on a different machine without the same data roots.

## Claim

Internal reproduction, verified repeatedly. **Not** third-party replication, and the manuscript does not say
otherwise.
