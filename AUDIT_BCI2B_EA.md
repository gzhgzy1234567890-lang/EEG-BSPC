# AUDIT_BCI2B_EA.md — the alignment factor on BCI-IV-2b

Baseline audited: commit `5092c92` (results/causal_2b.json written by that run).
Re-run after the fix described below: see the commit registered in CURRENT_BLOCKERS.md.

## Question

Revision C claimed that the alignment factor is zero for all four representations on BCI-2b. The referee
asked whether that is a property of the data, a numerical accident, or a bug.

## What the code does

`causal_2b.py` builds two alignment matrices:

- source-only: `R_s = msqrt_inv(mean_t C_t)`, the source session's average covariance;
- both-session: `R_b = msqrt_inv((mean_t C_t + mean_e C_e) / 2)`.

`euc_ea` is log power after multiplying the trials by R. `euc`, `tan` and `csp` do not use R at all, so for
them the factor is identically zero by construction, not an empirical finding.

## Finding: the whitening floor was larger than every eigenvalue

BCI-2b GDF files are read in volts: the trial standard deviation is 2.2e-6, the average covariance trace is
1.7e-11. `msqrt_inv` clipped eigenvalues at an absolute floor of 1e-8, which is **larger than every eigenvalue**
of a 1e-11-scale covariance. Every eigenvalue was therefore replaced by the floor, and the function returned the
same matrix (1e4 * I) for every input.

Evidence, measured on the baseline commit:

| quantity | subject 1, pair 1->2 |
|---|---|
| relative difference between the two session covariances | 0.185 |
| max abs difference between R_s and R_b | 7.3e-12 |
| max abs difference between the euc_ea features built with R_s and R_b | 2.7e-15 |

The covariances differ by 18 per cent while the whitening matrices agree to 1e-12, which is only possible if the
whitening ignores its input. BCI-2a is unaffected because there the data are in microvolts (trial standard
deviation 11.6, covariance ~1e2, above the floor).

## Fix

The floor is now relative: `floor = 1e-8 * max(eigenvalue)`. With that, on the same cell:

| | before | after |
|---|---|---|
| euc_ea alignment effect (subject level, 9 subjects) | exactly 0.0000 | **-0.0012 [-0.0037, +0.0011]**, Wilcoxon p = 0.40 |
| euc_ea, causal + source EA | +0.0350 | **+0.0358 [+0.0182, +0.0570]**, 9/9, p = 0.0039 |
| csp (primary), causal + source EA | +0.0341 | +0.0341 [+0.0104, +0.0585], 8/9, p = 0.039 |
| tan, causal + source EA | +0.0483 | +0.0486 [+0.0247, +0.0721], 8/9, p = 0.012 |

The pre-specified primary result (csp) is unchanged, because csp does not use the alignment matrix. The euc_ea
numbers move in the third decimal.

## Per-cell table

`results/audit_2b_table.csv` contains, for each of the 27 subject-pair cells, balanced accuracy before and after
correction and their difference, for all four representations and all four conditions (108 columns).

## What this changes in the paper

1. The sentence "the alignment factor is zero for all four representations" was wrong for euc_ea; it is now
   reported as -0.001 (n.s.) and the identically-zero cases are explained by construction.
2. The 2b numbers in the protocol are updated (Revision D).
3. The committed JSON from the baseline run is kept; the new run is a new file.

## What this does not change

The primary endpoint, its direction and its significance. But the incident is a reminder that a numerically
plausible zero can hide an implementation defect, and it is recorded here rather than silently corrected.
