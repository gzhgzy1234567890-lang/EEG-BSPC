# Reproduction guide

Every number in the manuscript is produced by the scripts in `src/` from the cached
EEG features, and the corresponding outputs are in `results/`.

## Order

1. `python src/pv8_final_compare.py`      -> `results/final_compare.txt`
   (Table 5 of the manuscript: the estimator comparison. Run this with the current
   code: the single-block fallback of Eq. (9) carries exactly one factor of K. The
   earlier version without that factor gives 0.6703 instead of 0.6774 on
   grasp-and-lift.)
2. `python src/pv8_lambda_control.py`     -> `results/lambda_control.txt`   (Table 15)
3. `python src/pv8_master.py`             -> `results/master_stats.md`, `results/master_cells.csv`
   (Tables 16 and 17: the correction-strength response and the trend analysis)
4. `python src/pv8_phase30.py`            -> `results/phase30.txt`         (Table 14)
5. `python src/pv8_kalman_audit.py`       -> `results/kalman_audit.txt`    (Section 4.12.1)
6. `python src/audit_repro.py`            -> `results/repro_audit.md`      (12 PASS, 1 NOT VERIFIED)
7. `python src/pv8_figs.py`, `python src/pv8_fig2b.py`, `python src/pv8_fig4.py`,
   `python src/pv8_figs_core.py`, `python src/pv8_fig_regimes.py`  -> `figs/`

## What is verified and what is not

Verified: every table of the manuscript against the outputs above
(`src/check_docx_numbers.py`: 106 numbers, 0 mismatches), and the implementation
invariants in `audit_repro.py` (lambda = 0 equals no correction, lambda = 1 equals the
full historical correction, no dependence on later trials, common evaluation window,
translation equivariance, zero-displacement handling).

Not verified: regeneration of the feature cache from the original public EEG
recordings. The audit starts from the cached features.
