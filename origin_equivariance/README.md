# An audit of mean correction in cross-session EEG decoding

Code, figures and the plain-text output of every number in

> **An audit of mean correction in cross-session EEG decoding: equivariance,
> failure mechanism, and boundaries**
> Zihao Gong, Jiran Li, Ke Huo, Yubin Han, Guangyu Shi, Yongqiang Xie

This archive accompanies the manuscript. It contains the analysis pipeline, the
audit of released preprocessing components, the experiments behind every table
and figure, and the raw text output that the manuscript quotes. The manuscript
itself (`BSPC_Manuscript_v16_with_figs.docx`, `BSPC_draft_v16.md`) and the
highlights file are in the same folder.

## What the paper claims, and where each claim is computed

| Claim in the manuscript | Where it is computed | Output |
|---|---|---|
| The two descriptions of two-sided centring are one pipeline (`dbl` ≡ `mean`) | `src/pv8_final.py` §2 | `results/final_2.txt` |
| Score-difference equivalence: corrections differing by a vector in the null space of P W are prediction-identical | `src/pv8_final.py` §4 | `results/final_4.txt` |
| An origin sweep leaves the equivariant pipelines flat to 0.0e+00 and drives the one-sided one toward 1/K | `src/pv8_exp4.py` | `results/exp4_*.txt` |
| Only the projection of the origin on the weights matters (equal-norm direction control) | `src/pv8_exp11.py` | `results/exp11.txt` |
| The signed displacement model, under the oracle and the model parameterisations | `src/pv8_exp14.py`, `src/pv8_law2.py` | `results/exp14.txt`, `results/law2.txt` |
| The source-only statistic with the centred scale, its invariances and its failures | `src/pv8_zw_centred.py`, `src/pv8_units.py` | `results/zw_centred.txt`, `results/units_centred.txt` |
| Held-out SEED-IV: statistic, AUC, operating point | `src/pv8_seed4.py`, `src/pv8_external.py` | `results/seediv.txt`, `results/external.txt` |
| Bound violation rates, invariance checks, leave-one-dataset-out operating points, split-sample sign AUC | `src/pv8_exp17.py` | `results/exp17.txt` |
| Calibration per subject with paired bootstrap differences | `src/pv8_cal.py` | `results/cal.txt` |
| Streaming under the recorded and the random trial order | `src/pv8_exp8.py` | `results/exp8_*.txt` |
| The code audit of three released preprocessing components | `src/code_audit.py` | `results/code_audit.txt` |
| Figures 1–4 | `src/pv8_figs.py`, `src/pv8_fig2b.py`, `src/pv8_fig4.py` | `figures/` |

## Data

The datasets are public and are **not** included here.

| dataset | source | what the pipeline expects |
|---|---|---|
| BCI Competition IV 2a | <https://www.bbci.de/competition/iv/#dataset1> | `A01T.mat` … `A09E.mat` in `$BSPC_DATA/BCICIV-2a-mat` |
| BCI Competition IV 2b | <https://www.bbci.de/competition/iv/#dataset2> | `B0101T.gdf` … in `$BSPC_DATA/BCICIV-2b` |
| SEED | BCMI Laboratory, SJTU (on request) | differential-entropy `.mat` files |
| SEED-IV (held out) | BCMI Laboratory, SJTU (on request) | `eeg_feature_smooth/{1,2,3}/*.mat` with `de_LDS1..24` |
| NER2015 | Kaggle, *inria-bci-challenge* | error-related potential epochs |
| grasp-and-lift | Kaggle, *grasp-and-lift-eeg-detection* | 32-channel series |

Features are cached as `.npz` files:

```
cache_2a/S01.npz              A_euc, B_euc, A_euc_ea, B_euc_ea, A_tan, B_tan,
                              A_csp, B_csp, ya, yb
cache_2b/B0101T.npz           X (trials, 3, 750), y, date, subj, sess, ch
cache_seed/01_1.npz           X (segments, 310), y, g
cache_seed4_iv/01_1.npz       X (segments, 310), y          (built by src/pv8_seed4.py --build)
cache_ner_feat/S02_01.npz     Ftime (trials, 448), Fpow, Feog, y, ch
cache_gal/subj1_series1.npz   F (trials, 256), y, ch
```

Set the environment before running:

```
$BSPC_DATA   directory containing the dataset folders   (default E:\data)
$BSPC_OUT    directory for the cache and the results    (default the parent of src/)
```

## Reproducing the paper

```
python src/pv8_final.py 1,2,3,4,5,6,7,8,9     # levels, variants, calibration, certificate
python src/pv8_exp4.py 2b,seed,gal            # origin sweep
python src/pv8_exp11.py                       # direction control and in-sample sign
python src/pv8_exp14.py                       # per-cell displacement model (oracle)
python src/pv8_law2.py                        # the model parameterisation
python src/pv8_exp17.py                       # bound rates, invariances, operating points, split-sample AUC
python src/pv8_zw_centred.py                  # the corrected statistic and its failures
python src/pv8_units.py                       # Table 5
python src/pv8_seed4.py --build               # build the SEED-IV cache, then run the held-out test
python src/pv8_external.py                    # the held-out operating point
python src/pv8_cal.py                         # calibration with paired intervals
python src/pv8_exp8.py 2b,seed,gal,2a         # streaming, recorded order
python src/code_audit.py                      # the audit of released components
python src/pv8_figs.py; python src/pv8_fig2b.py; python src/pv8_fig4.py   # figures
```

Every script writes plain text into `results/`; nothing is hidden behind a
plotting call. Python 3.7, numpy 1.21, scipy 1.7, scikit-learn 1.0,
matplotlib 3.5.

## Layout

```
BSPC_Manuscript_v16_with_figs.docx   the manuscript (10 tables, 4 figures)
BSPC_Highlights_v16.docx             the highlights file
BSPC_draft_v16.md                    the manuscript source
src/                                 analysis, one script per table or figure
results/                             plain-text output of every number
figures/                             Figures 1-4 (pdf and png)
```

## License and citation

MIT, see `LICENSE`. If you use this code, please cite the paper above.
