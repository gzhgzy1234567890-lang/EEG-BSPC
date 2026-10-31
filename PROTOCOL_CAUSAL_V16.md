# Frozen protocol: unified source-only, past-only main experiment (v16, revision B)

Frozen 31 October 2026. Revision B completes the 2x2 design on BCI-2a, withdraws the retrospective
pre-specification of euc_ea on that dataset, fixes the CSP description, and rewrites the SEED plan after
checking what data are actually available.

## Estimator

Unchanged from revision A: for a trial in completed block b, the estimate uses blocks 1..b-1 only, and the
two-sided correction removes d_b = P(s̄_{1..b-1} - s̄_A). Unit test `test_two_sided.py` passes (K = 2 and K = 4).

## BCI-2a: 2x2 factorial

Four conditions, all on the same trials and the same classifier:

| | source-only EA | both-session EA |
|---|---|---|
| causal filter | causal_so | causal_arch |
| non-causal filter | noncausal_so | noncausal |

Effects (euc_ea, 9 subjects): alignment +0.008 [-0.006, +0.022]; filter -0.011 [-0.020, -0.002];
interaction +0.002 [-0.010, +0.014]. The near-zero total protocol effect reported in the earlier version is the
sum of these two opposing changes, not evidence that causality does not matter; it is reported as such.

## Pre-specification, corrected

The primary endpoint for BCI-2a is **not** pre-specified: euc_ea was chosen after seeing the first run, so its
+0.071 is an exploratory result. For the datasets not yet run the primary endpoint is fixed now, before any
result is seen:

- BCI-2b: **csp**, the only representation that is source-only by construction in both filter conditions;
- SEED: the released DE representation (the only one available), with the causal processing applied on top of it.

Holm adjustment covers these pre-specified primary tests only. Secondary representations are reported
uncorrected and labelled exploratory.

## CSP description, corrected

What the code computes is **six generalized eigenfilters from a first-class-versus-average contrast**: the
generalized eigenproblem between the first class's average covariance and the across-class average covariance,
with the three smallest and three largest eigenvalues retained. This is not a multi-class one-vs-rest CSP with
three filters per class. The manuscript sentence now says exactly this, and the archived pipeline used the same
code, so this is a description fix rather than a protocol change.

## SEED: data availability first

Checked on this machine before writing the plan:

| item | finding |
|---|---|
| local SEED copy | `E:\\data\\SEED-all\\seed` contains `ExtractedFeatures_1s` and `ExtractedFeatures_4s` and the stimulation tables |
| raw recordings | **not present**: no `Preprocessed_EEG` directory, no `.cnt` files |
| consequence | a raw-to-feature causal rerun for SEED cannot be executed here |

Therefore the SEED plan is stated in two parts, and the paper must say which one it reports:

1. **What can be run here**: causal processing *on top of the released DE features* - the DE values are treated
   as a given, and the mean estimator is past-only. This cannot be described as a strictly causal raw-to-feature
   pipeline, because the released DE features were computed with the official preprocessing (200 Hz resampling,
   0-75 Hz filtering, smoothing variants) that sees the whole segment.
2. **What a strict rerun would require**: the `Preprocessed_EEG` waveforms (or the SEED_Multimodal `.cnt`
   files, which cover 12 of the 15 subjects), five frequency bands (delta 1-4, theta 4-8, alpha 8-14, beta
   14-30, gamma 30-50 Hz), a causal filter per band, and a filter state **reset at every film boundary** with the
   first and last segment of each film discarded. Only then could the result be compared with the archived
   +0.214 as a filter-only difference.

Until part 2 is available, the SEED causal claim in the paper is restricted to part 1 and labelled accordingly.

## Statistics

Subject-level paired values; 95 per cent bootstrap (10,000 resamples, seed 20261101); two-sided Wilcoxon;
Holm across the pre-specified primary tests.
