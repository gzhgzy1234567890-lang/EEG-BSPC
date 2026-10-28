# Causal mean correction in cross-session EEG decoding

Code, figures and the plain-text output of every number in

> **Causal mean correction in cross-session EEG decoding: when it helps, and how
> much to correct**
> Zihao Gong, Jiran Li, Ke Huo, Yubin Han, Guangyu Shi, Yongqiang Xie

## What each table needs

| table | script | output |
|---|---|---|
| levels of `none`/`zero`/`mean`, per subject | `src/pv8_final.py` | `results/final_2.txt` |
| datasets and cells | `src/pv8_common.py` (loaders) | — |
| estimators at a fixed prefix | `src/pv8_causal.py` | `results/causal.txt` |
| block-wise estimator and its weight | `src/pv8_invgate.py` | `results/invgate.txt` |
| block-length sweep and family LODO | `src/pv8_rel_sweep.py` | `results/rel_sweep.txt` |
| held-out SEED-IV | `src/pv8_causal_seed4.py`, `src/pv8_dirgate_ci.py` | `results/causal_seed4.txt` |
| direction / drift / PCA gates (negative results) | `src/pv8_dirgate.py`, `src/pv8_driftgate.py`, `src/pv8_pcagate.py` | `results/*gate*.txt` |
| per-cell displacement model | `src/pv8_exp14.py`, `src/pv8_law2.py` | `results/exp14.txt`, `law2.txt` |
| bound, invariances, split-sample AUC | `src/pv8_exp17.py` | `results/exp17.txt` |
| calibration | `src/pv8_cal.py` | `results/cal.txt` |
| property tests | `tests_properties.py` | `results/tests.txt` |

## Data

Six public datasets, not included: BCI Competition IV 2a/2b, SEED, SEED-IV,
NER2015 and grasp-and-lift. Set `BSPC_DATA` to the directory holding them and
`BSPC_OUT` for the cache and the results; the cache schema is in the manuscript,
Section 3.

## Reproducing

```
python src/pv8_final.py 1,2
python src/pv8_causal.py
python src/pv8_invgate.py
python src/pv8_rel_sweep.py
python tests_properties.py
```

Figures: `src/pv8_figs.py`, `src/pv8_fig2b.py`, `src/pv8_fig4.py`,
`src/pv8_fig5.py`. Python 3.7, numpy 1.21, scipy 1.7, scikit-learn 1.0,
matplotlib 3.5. MIT licence.
