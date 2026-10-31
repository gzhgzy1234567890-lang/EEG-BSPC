# Frozen protocol: unified source-only, past-only main experiment (v16, revision A)

Frozen 31 October 2026, revised before the BCI-2b and SEED runs. Revision A fixes the estimator (the first
version centred on a zero score instead of the source mean), states the feature definitions as implemented,
fixes the BCI-2b pairing list, pre-specifies the primary endpoint, and fixes the SEED film-boundary rule.

## Estimator (the correction)

For a trial t in completed block b, the estimate is the mean of the completed blocks 1..b-1 only. The
two-sided correction removes the displacement of that estimate from the source mean:

    d_b = P W (mu_hat_b - mu_A)   computed as   d_b = P (mean score of blocks 1..b-1 - mean score of A)

and the correction applied is x_t - d_b (equivalently, scores s_t - d_b). The first block is unscored.
Unit test: score-space and feature-space implementations must give identical predictions; asserted in
`test_two_sided.py`, which passes for K = 2 and K = 4.

## Data and pairing

| dataset | pairing |
|---|---|
| BCI-IV-2a | T -> E, 9 subjects |
| BCI-IV-2b | the three forward pairs 01T->02T, 01T->03T and 02T->03T, 9 subjects, matching the archived main comparison |
| SEED | the three ordered session pairs per subject (1->2, 1->3, 2->3), 15 subjects |

## Signal processing

Band-pass 8-30 Hz, fourth-order Butterworth. Causal: `lfilter`, forward only, filter state carried along the
continuous recording. Reference: `filtfilt` on the same signal (the archived pipeline). Epochs: BCI cue + 2.0
to 6.0 s. SEED: 1 s segments from the released raw recordings; the filter runs continuously across a session and
**no state reset is made at film boundaries**, but the first and last segment of each film are discarded from
scoring so that no scored segment sits within one filter transient of a film boundary.

## Features (as implemented, not as previously described)

| name | implementation |
|---|---|
| euc | log variance in four consecutive **time windows** of the trial (not four frequency bands; the earlier protocol text was wrong and the manuscript sentence is corrected to match the code) |
| euc_ea | euc after division by an alignment matrix; **source-only** version uses the training-session covariance, the archived version used the mean of both sessions' covariances |
| tan | tangent space of the source-referenced covariance |
| csp | generalised eigenvectors of the first class covariance against the average covariance, three filters per class (six total), fitted on the training session only |

Note: the archived euc_ea and tan are target-informed by construction (they use the target session covariance).
The source-only versions are therefore a protocol change in addition to the filter change, and the two are
reported separately as filter effect and alignment effect.

## Primary endpoint, fixed in advance

The primary confirmatory endpoint is **euc_ea**, the representation used for the paper's headline comparison.
The other three representations are secondary and reported without multiplicity correction. Holm adjustment is
applied across the three datasets for the primary endpoint only.

## Outcomes

- Delta_causal = BA(causal, euc_ea, lambda=1) - BA(causal, euc_ea, lambda=0);
- Delta_noncausal = the archived value for the same dataset and representation;
- Delta_protocol = Delta_causal - Delta_noncausal, with a subject-level bootstrap interval, reported as a
  protocol-sensitivity statistic of this study.

## Statistics

Subject-level paired values; 95 per cent bootstrap over subjects (10,000 resamples, seed 20261101); two-sided
Wilcoxon signed-rank; Holm across datasets for the primary endpoint.
