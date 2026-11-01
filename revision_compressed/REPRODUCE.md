# REPRODUCE.md

Short guide to regenerating the numbers in the manuscript. Every path is relative to the repository root.

## Environment

Python 3.7 with numpy, scipy, scikit-learn, mne and matplotlib; Word is needed only to export the DOCX to PDF.

## Data

sleep-EDF is read from the local copy of `sleep-cassette` (the path is the `ROOT` constant in
`sleep_edf/sleep_edf_frozen.py`). SEED uses the cached differential-entropy features in
`local_analysis/cache_seed` and the archived per-cell summaries; the raw DE archive is not redistributed. BCI and
grasp-and-lift use the feature caches described in the supplement.

## Runs, in order

| step | command | output | time |
|---|---|---|---|
| anchor decomposition | `python sleep_edf/online_decomp_anchored.py` | results/online_decomposition_anchored.json | about 25 min |
| factorial | `python factorial_intervention/factorial_rich.py` | results/factorial_2x2_rich.json | about 20 min (cache first) |
| dense strength grid | `python factorial_intervention/factorial_lambda_dense.py` | results/factorial_lambda_dense.json | about 30 min |
| sleep memory sweep | `python temporal_memory/sleep_memory_sweep.py` | results/sleep_memory_sweep.json | about 25 min |
| SEED recomputation | `python seed_multistudy/seed_transductive.py` | results/seed_transductive.json | about 3 min |
| protocol tests | `python research_harness/tests/test_protocol_integrity.py` | 5 tests, prints PASS | under 1 min |
| table traceability | `python table_trace.py` | prints 7 of 7 traced | under 1 min |

## What cannot be regenerated from this release

- the raw recordings to feature-cache step: the caches are provided, the preprocessing is documented but not rerun;
- the SEED archived figure +0.214: the exact aggregation is not recoverable, and the recomputation gives +0.236;
- BCI-2b and the external corpora were run once and their per-subject outputs are archived rather than recomputed.

## Figures

`python figures/make_fig5.py` regenerates Fig. 5 from the archived JSONs; Figs 1-4 are embedded in the submitted
DOCX and were produced by the analysis scripts named in the supplement.
