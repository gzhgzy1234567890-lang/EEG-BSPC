# EEG-BSPC — code, result files and manuscript sources

This repository holds the analysis code and result files for one current submission and for the earlier
alignment study whose feature caches and benchmark definitions the current paper reuses. The alignment paper's
pipeline is kept so that the reuse can be checked.

**Current submission (BSPC):**

> When does causal mean correction help or harm EEG decoding? Evidence from cross-recording benchmarks and a
> trial-order audit

**Earlier paper (alignment), whose caches are reused:**

> Align, don't zero: consistent feature centring for cross-session EEG decoding

The current manuscript states the reuse in its Data availability and overlap paragraph; whether the alignment
paper has been submitted, is under review, or has appeared is a question for the authors and is not asserted
here.

---

## Where each claim of the current paper comes from

| claim | code | output |
|---|---|---|
| SEED, full-strength correction | `grasp_and_lift_order/seed_gate_online.py`, `seed_models.py` | `grasp_and_lift_order/results/*.json` |
| SEED, film-disjoint over five rotations | `grasp_and_lift_order/seed_film_disjoint_rotations.py` | `grasp_and_lift_order/results/seed_film_disjoint*.json` |
| SEED, estimator comparison (S30) | `grasp_and_lift_order/seed_estimators.py` | `grasp_and_lift_order/results/seed_estimators.json` |
| SEED, memory sweep and its subject-level statistics (S31) | `grasp_and_lift_order/seed_memory_scale.py`, `seed_memory_scale_stats.py` | `grasp_and_lift_order/results/seed_memory_scale.json` |
| sleep-EDF, completed-block correction | `sleep_edf/sleep_edf_frozen.py` | `sleep_edf/results/sleep_edf_frozen_cells.json` |
| sleep-EDF, five-estimator matrix | `sleep_edf/sleep_estimator_matrix.py` | `sleep_edf/results/*.json` |
| sleep-EDF, global decomposition (S27) | `sleep_edf/sleep_decomposition.py` | `sleep_edf/results/sleep_decomposition*.json` |
| sleep-EDF, block-wise decomposition over the class union (S31) | `sleep_edf/sleep_blockwise.py` | `sleep_edf/results/sleep_blockwise.json` |
| sleep-EDF, per-block composition and all-block error change (S31) | `sleep_edf/sleep_blocks_all.py`, `sleep_block_composition.py`, `composition_stats.py` | `sleep_edf/results/sleep_blocks_all.json`, `sleep_block_composition.json` |
| sleep-EDF, telemetry protocol | `sleep_edf/sleep_telemetry.py` | `sleep_edf/results/sleep_telemetry*.json` |
| sleep-EDF, online label-free gate | `sleep_edf/sleep_gate_online.py` | `sleep_edf/results/*.json` |
| grasp-and-lift, acquisition-order audit | `grasp_and_lift_order/gal_order_test.py`, `build_gal_time.py` | `grasp_and_lift_order/results/gal_order*.json` |
| grasp-and-lift, matched scored trials | `grasp_and_lift_order/matched_samples.py` | `grasp_and_lift_order/results/matched*.json` |
| non-linear decoders | `sleep_edf/sleep_models.py` | `sleep_edf/results/sleep_models*.json` |

## Numbers check

```
python sleep_edf/check_numbers.py    # every number in the manuscript and supplement, from the archived results
python sleep_edf/check_s31.py        # the S31 block-wise and memory-sweep values
```

Both print `CHECK PASS` when the archived results reproduce the reported values. This is a check on the
archived result files, not a re-run of the EEG processing.

## Data (public; not included)

| dataset | where | layout expected |
|---|---|---|
| SEED | BCMI, <https://bcmi.sjtu.edu.cn/home/seed/> | `$BSPC_CACHE_SEED/*.npz` (per-session features) |
| sleep-EDF cassette | PhysioNet, `sleep-cassette` | `E:\data\sleep-edf\sleep-cassette\*PSG.edf` + `*EC-Hypnogram.edf` |
| grasp-and-lift | Kaggle, `grasp-and-lift-eeg-detection` | `E:\data\grasp-and-lift-eeg-detection\train\*.csv` |
| BCI Competition IV 2a / 2b | <https://www.bbci.de/competition/iv/> | `$BSPC_DATA/BCICIV-2a-mat`, `BCICIV-2b` |
| Lee2019-MI (OpenBMI) | GigaDB 100542 | `D:\data\mne_data\...` |

## Environment

Python 3.7, numpy 1.21.6, scipy 1.7.3, scikit-learn 0.23.2, mne 0.23.4, matplotlib 3.5.3.

## Reproducing the figures

```
python figures/ga_corrected.py     # graphical abstract
```
