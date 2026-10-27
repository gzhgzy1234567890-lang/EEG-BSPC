# Origin equivariance in cross-session EEG decoding

Code, figures and raw text output for

> **Origin equivariance in cross-session EEG decoding: what a mean correction
> repairs and how to screen for the risk**
> Zihao Gong, Jiran Li, Ke Huo, Yubin Han, Guangyu Shi, Yongqiang Xie

The repository contains the analysis pipeline, the origin-sweep and streaming
experiments, the screening scripts, the figures, and the plain-text output of
every number reported in the paper.

## What the paper claims, and where each claim is computed

| Claim | Where |
|---|---|
| Only the two-sided mean correction is origin-equivariant | `src/pv8_common.py`, algebra in the manuscript |
| Corrections differing in the null space of the weights are prediction-identical | `src/pv8_final.py` (section 4), `results/final_4.txt` |
| The correction can be applied to the K scores instead of the D features | `src/pv8_exp9.py`, `results/exp9.txt` |
| An origin sweep leaves equivariant pipelines flat and collapses the one-sided one | `src/pv8_exp4.py`, `results/exp4_*.txt` |
| A source-only statistic orders the damage (Spearman -0.755, n = 11) | `src/pv8_screen.py`, `results/screen.txt` |
| The induced displacement orders the damage across classifier families | `src/pv8_exp5.py`, `results/exp5_*.txt`, `src/pv8_exp7.py` |
| The collapse certificate is exact (124/124) | `src/pv8_final.py` (section 7), `results/final_7.txt` |
| Calibration, per subject, with bootstrap intervals | `src/pv8_exp10.py`, `results/exp10.txt` |
| Streaming under the recorded trial order | `src/pv8_exp8.py`, `results/exp8_*.txt` |

## Data

The datasets are public and are **not** included here.

| dataset | source | what the pipeline expects |
|---|---|---|
| BCI Competition IV 2a | <https://www.bbci.de/competition/iv/#dataset1> | `A01T.mat` ... `A09E.mat` in `$BSPC_DATA/BCICIV-2a-mat` |
| BCI Competition IV 2b | <https://www.bbci.de/competition/iv/#dataset2> | `B0101T.gdf` ... in `$BSPC_DATA/BCICIV-2b` |
| SEED | BCMI Laboratory, SJTU (on request) | differential-entropy `.mat` files |
| NER2015 | Kaggle, *inria-bci-challenge* | error-related potential epochs |
| grasp-and-lift | Kaggle, *grasp-and-lift-eeg-detection* | 32-channel series |

Features are cached as `.npz` files with the following schema:

```
cache_2a/S01.npz          A_euc, B_euc, A_euc_ea, B_euc_ea, A_tan, B_tan,
                          A_csp, B_csp, ya, yb
cache_2b/B0101T.npz       X (trials, 3, 750), y, date, subj, sess, ch
cache_seed/01_1.npz       X (segments, 310), y, g
cache_ner_feat/S02_01.npz Ftime (trials, 448), Fpow, Feog, y, ch
cache_gal/subj1_series1.npz F (trials, 256), y, ch
```

`src/bspc_feat.py` builds the 2a and 2b features from the raw files;
`src/make_features_2b.py` is the session-level feature cache builder. The
SEED, NER2015 and grasp-and-lift caches are simple band-power / differential
entropy extracts of the distributed files and are built by the extractors in
the companion archive of the earlier analysis (available from the
corresponding author).

Set the two environment variables before running:

```
$BSPC_DATA   directory containing the dataset folders   (default E:\data)
$BSPC_OUT    directory for the cache and the results    (default .)
```

## Running it

```
python src/pv8_final.py 1,2,3,4,5,6,7,8,9     # every table in the paper
python src/pv8_screen.py                      # the two-statistic screen
python src/pv8_exp4.py 2b,seed,gal            # origin sweep
python src/pv8_exp5.py 2b,gal,ner             # classifier sweep
python src/pv8_exp7.py                        # composition and BCI-2a sweep
python src/pv8_exp8.py 2b,seed,gal,2a         # streaming, recorded order
python src/pv8_exp9.py                        # decision-space form
python src/pv8_exp10.py                       # per-subject calibration
python src/pv8_figs.py                        # figures 1-3
```

Every script writes plain text into `results/`; nothing is hidden behind a
plotting call. Python 3.7, numpy 1.21, scipy 1.7, scikit-learn 1.0,
matplotlib 3.5.

## Repository layout

```
src/        analysis pipeline, one script per experiment
results/    raw text output, one file per script
figures/    Figures 1-3 as submitted (pdf and png)
```

## License

MIT. See `LICENSE`.

## Citation

If you use this code, please cite the paper above.
