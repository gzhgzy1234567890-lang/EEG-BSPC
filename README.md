# EEG-BSPC — code, features and result files

This repository holds the analysis code and the result files for the two manuscripts below. The second
(alignment) paper's pipeline is kept because the first paper reuses its feature caches and comparison
tables; the first is the current submission.

**Current submission (BSPC):**

> When online mean correction harms EEG decoding: a reproducible negative transfer within recording
> series, and where it helps instead

**Earlier paper (alignment):**

> Align, don't zero: consistent feature centring for cross-session EEG decoding

---

## Where each claim of the current paper comes from

| claim | code | output |
|---|---|---|
| transductive table, five development benchmarks | `origin_equivariance/src/pv8_final.py`, `pv8_master.py` | `results/master_stats.md` |
| causal estimator comparison on a common test set | `origin_equivariance/src/pv8_final_compare.py`, `pv8_causal.py` | `results/final_compare.txt` |
| variance-ratio weighting (Eq. 9) and its ablation | `pv8_lambda_control.py`, `pv8_final_compare.py` | `results/final_compare.txt` |
| correction-strength and estimator surface (Tables 9-10) | `pv8_master.py` | `results/master_stats.md` |
| trend diagnostic (Table 11, Fig. 5) | `pv8_trend_test.py` | `results/trend_test.txt` |
| external cross-day cohort (Lee2019-MI) | `openbmi/lee2019_direct.py`, `lee2019_parallel.py`, `lee2019_secondary.py`, `lee2019_sensitivity.py`, `lee2019_variantC.py` | `results/openbmi_all.json`, `lee2019_sensitivity.json`, `lee2019_variantC.json` |
| protocol-consistent sleep-EDF replication | `sleep_edf/sleep_edf_frozen.py` | `sleep_edf/results/sleep_edf_frozen_cells.json` |
| first sleep-EDF implementation, superseded (kept for the deviation record) | `sleep_edf/sleep_edf_test.py`, `sleep_edf_run.py` | `sleep_edf/results/sleep_edf_cells.json` |
| grasp-and-lift composition audit | `sleep_edf/gal_composition_confound.py` | text in `sleep_edf/INDEPENDENT_TEST_DEVIATIONS.md` |

The frozen protocol and its deviation record are in `sleep_edf/INDEPENDENT_TEST_PROTOCOL.md` and
`sleep_edf/INDEPENDENT_TEST_DEVIATIONS.md`. The latter lists every difference between the frozen text
and the executed analysis, together with both result sets.

## Data (public; not included)

| dataset | where | layout expected |
|---|---|---|
| BCI Competition IV 2a | <https://www.bbci.de/competition/iv/#dataset1> | `$BSPC_DATA/BCICIV-2a-mat/A0?T.mat`, `A0?E.mat` |
| BCI Competition IV 2b | <https://www.bbci.de/competition/iv/#dataset2> | `$BSPC_DATA/BCICIV-2b/B0?0?T.gdf`, `B0?0?E.gdf` |
| Lee2019-MI (OpenBMI) | GigaDB, `pub/10.5524/100001_101000/100542` | `D:\data\mne_data\...\session{1,2}\s{N}\sess0{1,2}_subj{N:02d}_EEG_MI.mat` |
| sleep-EDF cassette | PhysioNet, `sleep-cassette` | `E:\data\sleep-edf\sleep-cassette\*PSG.edf` + `*EC-Hypnogram.edf` |

`BSPC_DATA` defaults to `E:\data`. The paths in the Lee2019 and sleep-EDF scripts are absolute and must
be pointed at your copies.

## Environment

Python 3.7, numpy 1.21.6, scipy 1.7.3, scikit-learn 0.23.2, mne 0.23.4, matplotlib 3.5.3.

## Running

```
python src/paper_numbers.py       # alignment paper: every reported number
python src/reproduce.py           # alignment paper: independent re-implementation
python openbmi/lee2019_parallel.py    # external cohort, downloads what is missing
python openbmi/lee2019_secondary.py   # estimator x strength surface
python sleep_edf/sleep_edf_frozen.py  # protocol-consistent replication (~4 min)
```

## A record of defects, kept deliberately

- The alignment pipeline once estimated `tr(Sigma)` as `mean(dd**2) * h / 4`, which is wrong by a factor
  `2D`; the correct form is `sum(dd**2) * h / 2`. A section of the alignment paper was withdrawn because of
  it. See the alignment paper's notes.
- `lee2019_secondary.py` counted a subject as negative against the group mean instead of the subject's own
  baseline; fixed in commit `e05e3af`.
- The first sleep-EDF aggregation keyed subjects on four characters instead of five; fixed, and the
  corrected aggregation reproduces the reported numbers. Both runs are in `sleep_edf/INDEPENDENT_TEST_DEVIATIONS.md`.

## License

MIT. See `LICENSE`.
