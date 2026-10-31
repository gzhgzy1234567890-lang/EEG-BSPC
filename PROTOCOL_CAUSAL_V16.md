# Frozen protocol: unified source-only, past-only main experiment (v16)

Frozen before any run, 31 October 2026. Deviations, if they occur, are logged in a deviation table and reported
with both the planned and the executed analysis.

## Data

| dataset | subjects / sessions | pairing |
|---|---|---|
| SEED | 15 subjects, 3 sessions | every ordered session pair within a subject (1->2, 1->3, 2->3) |
| BCI-IV-2a | 9 subjects, 2 sessions (T, E) | T -> E |
| BCI-IV-2b | 9 subjects, 5 sessions | every ordered pair within a subject, as in the archived analysis |

Inclusion: a pair enters only if both sessions contain at least two classes and the target session has at least
four scored blocks.

## Signal processing

- Band-pass 8-30 Hz, fourth-order Butterworth, applied **forward only** (`scipy.signal.lfilter`) to the
  continuous recording, with filter state carried across the whole recording, not restarted per trial or per
  block. The non-causal reference uses `filtfilt` on the same signal, which is the archived pipeline.
- Epoching as in the archived pipeline: BCI-2a cue + 2.0-6.0 s; BCI-2b cue + 2.0-6.0 s; SEED 1 s segments as
  released, filtered causally after concatenating the session.
- No artifact rejection beyond the archived rule; no re-referencing change.

## Features

Four representations, all computed from the causally filtered signal:

| name | definition | target information |
|---|---|---|
| euc | log band power in four sub-bands, 22 channels | none |
| euc_ea | euc after Euclidean alignment with the **source** session covariance only | none |
| tan | tangent space of the source-referenced covariance | source reference only |
| csp | CSP filters fitted on the **training** session, applied to both | fitted on source only |

The archived pipeline used a Euclidean alignment matrix built from the mean of the source *and* target
covariances; that is target-informed and is the second protocol difference besides the filter.

## Estimator and scoring

- Mean estimate for trial t uses only completed blocks 1..b-1, block size 15, first block unscored.
- Lambda fixed at 1.0 (full correction). No per-session tuning.
- The same classifier (LDA, lsqr, Ledoit-Wolf shrinkage), the same scored trials, the same training data for
  corrected and uncorrected conditions.

## Outcomes

For each dataset and representation:

- Delta_causal = BA(causal, lambda=1) - BA(causal, lambda=0);
- Delta_noncausal = the same quantity on the archived non-causal pipeline;
- **Delta_protocol = Delta_causal - Delta_noncausal**, with a subject-level bootstrap interval, reported as a
  protocol-sensitivity statistic and not as a literature-first claim.

## Statistics

Subject-level paired values; 95 per cent bootstrap intervals over subjects (10,000 resamples, seed 20261101);
two-sided Wilcoxon signed-rank per dataset; Holm correction across the three datasets for the primary
Delta_causal test.

## Checks

- SEED keeps the film-disjoint test (five rotations, every film held out once).
- Any subject whose effect is an outlier is reported by name, not trimmed.
- Reconstruction: the corrected and uncorrected conditions share the identical feature matrix by construction;
  asserted in code.
