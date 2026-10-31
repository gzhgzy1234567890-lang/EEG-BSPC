# Reproducing the results in this paper

Every script reads its paths from the environment, with the author's layout as the default:

```
BSPC_DATA        raw datasets (default E:\data)
BSPC_CACHE_ROOT  the directory holding cache_* (default G:\Work_work\math\EEG\local_analysis)
BSPC_CODE        the repository root (default: the directory of the script)
```

## Sleep-EDF

| result in the paper | script | output |
|---|---|---|
| main -0.102 over 4,983 cells | `sleep_edf/sleep_edf_frozen.py` | results/sleep_edf_frozen_cells.json |
| strict causal filtering | `sleep_edf/sleep_edf_causal.py` | results/sleep_edf_causal_cells.json |
| five estimators x five strengths | `sleep_edf/sleep_estimator_matrix.py` | results/sleep_edf_estimator_matrix.json |
| decomposition (Section 4.7, S27) | `sleep_edf/sleep_decomposition.py` | results/sleep_decomposition.json |
| identical class sets (693 cells) | `sleep_edf/decomposition_identical_sets.py` | prints the subset |
| telemetry protocol (S26) | `sleep_edf/sleep_telemetry.py` | results/sleep_telemetry_cells.json |
| nonlinear decoders (S28) | `sleep_edf/sleep_models.py` | results/sleep_models.json |
| block-wise online gate (S29) | `sleep_edf/sleep_gate_online.py` | results/sleep_gate_online.json |

## Grasp-and-lift and SEED

| result | script |
|---|---|
| acquisition-order rebuild | `grasp_and_lift_order/build_gal_time.py` |
| three orderings (Table 8) | `grasp_and_lift_order/gal_order_test.py` |
| matched scored trials | `grasp_and_lift_order/matched_samples.py` |
| SEED film-disjoint, three rotations | `grasp_and_lift_order/seed_film_disjoint_rotations.py` |
| SEED film-level recall | `grasp_and_lift_order/seed_film_level.py` |
| SEED online gate | `grasp_and_lift_order/seed_gate_online.py` |

## What is not one command

The scripts assume the feature caches exist. `build_gal_time.py` is the only one that starts from raw CSVs;
for sleep-EDF the features are rebuilt from the EDF files inside each script. A single end-to-end entry point
that fetches the data, builds every cache and regenerates every table does not exist yet, and the paper says so.
