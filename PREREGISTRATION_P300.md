# PREREGISTRATION_P300.md

Written and committed **before** the analysis was run. Frozen protocol for an independent-dataset test of the
composition prediction.

## Why this dataset, and what it can and cannot test

The P300 speller dataset in `E:\data\Event-Related Potentials (P300, EEG) - BCI dataset` was not used anywhere in
the development of this paper. It is a different task (ERP detection rather than motor imagery or sleep staging),
a different montage (16 channels), a different sampling rate (128 Hz) and a different class balance.

It **cannot** test cross-session transfer, because it contains a single session per subject. It **can** test the
prediction that a composition-dominated displacement hurts: the classes are imbalanced roughly 6:1 (non-target
versus target), so under Proposition 1 the displacement is about (2 pi_B - 1) a = 0.72 a, a composition term with
no cross-session drift to justify it.

## Frozen design

| item | value |
|---|---|
| data | `data_allsubjects`, a list of 16 MNE EpochsArray objects, 16 channels, 0-586 ms at 128 Hz |
| subject order | as stored, 16 subjects |
| split | within each subject, epochs in stored order: first 50 per cent = source A, last 50 per cent = target B |
| features | log-variance per channel in four equal sub-windows of the epoch (16 x 4 = 64 features) |
| classifier | LDA, solver lsqr, shrinkage auto, fitted on A only |
| correction | past-only, block 15, full displacement d = P(mean scores of scored blocks so far) - P(mean scores of A) |
| scored trials | all of B after the first block of 15 |
| endpoint | delta balanced accuracy = BA(corrected) - BA(uncorrected) on the scored trials |
| statistic | per-subject delta; two-sided sign test and Wilcoxon across 16 subjects; no multiplicity correction (single endpoint) |
| evidence class | independent dataset, pre-registered, **mechanism test** (not a cross-session claim) |

## Prediction stated in advance

Because the target prior is far from balanced and there is no session drift to remove, **the correction should
reduce balanced accuracy**: delta < 0 in a majority of the 16 subjects, with the subject-level sign test rejecting
zero.

If the correction instead helps, Proposition 1's composition account does not transfer to this dataset and the
paper must say so.

## What will be reported

All 16 subject values, the mean, the sign test, the Wilcoxon p, and the class priors actually observed in A and B.
No subject will be dropped; if a subject has a single-class block the block is skipped and the count is reported.
