# Frozen protocol: independent test of online mean correction on sleep-EDF

Frozen before any result of this analysis was produced. Any change after this point is a
deviation and must be recorded in `INDEPENDENT_TEST_DEVIATIONS.md`.

## Why this dataset

The paper's central negative result comes from grasp-and-lift, where successive series of one
recording are used as source and target. No independent dataset in the paper provides that
within-recording structure. Sleep-EDF (cassette subset, `E:\data\sleep-edf`) does: each night is
one continuous recording that can be split into consecutive series, and it plays no part in the
development of the analysis.

## Data and unit of analysis

- 20 subjects, two nights each where both files exist (PSG plus hypnogram).
- Channels: EEG Fpz-Cz and Pz-Oz, sampled as recorded.
- Epochs: 30 s, contiguous, unlabelled epochs dropped.
- Labels: the five sleep stages from the hypnogram (W, N1, N2, N3, REM).
- Series: each night is cut into consecutive series of 60 epochs (30 min); trailing epochs that do
  not fill a series are dropped.
- Cells: every ordered pair of distinct series within the same night (source earlier, target
  later), matching the "same recording, sequential series" structure of grasp-and-lift.

## Signal path (fixed)

1. Band-pass 0.5-30 Hz, fourth-order Butterworth, zero-phase, applied to each series separately.
2. Per 30-s epoch, log-variance in four bands: 0.5-4, 4-8, 8-12, 12-30 Hz, per channel.
3. Features: the resulting 8 values per epoch, no normalisation other than the log.

## Model and correction (fixed)

- Classifier: LDA (lsqr solver, Ledoit-Wolf shrinkage) fitted on the source series only.
- Correction: completed-block mean of the decision-space displacement, blocks of 15 epochs,
  lambda in {0, 1}; the first block of the target is unscored warm-up.
- Primary comparison: BA(lambda = 1) minus BA(lambda = 0) on the post-warm-up target epochs,
  averaged within cell, then within subject.

## Primary statistic

Mean paired difference over subjects; two-sided sign test; subject-level bootstrap of the mean
(10,000 resamples, percentile, seed 20261030). No interim looks.

## Pre-specified interpretation

- If the mean difference is negative and the sign test significant, the within-recording negative
  transfer replicates in an independent dataset.
- If it is positive or null, the paper must state that the negative transfer did not replicate
  outside grasp-and-lift, and its discussion must be rewritten accordingly.
- Either outcome is reported in full, including the subject-level distribution.

## Exclusion rules

- A night is excluded if fewer than four complete series remain after epoching or if fewer than
  two stages are present.
- A subject is excluded only if no night qualifies.
