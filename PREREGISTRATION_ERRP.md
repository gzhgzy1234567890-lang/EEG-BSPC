# PREREGISTRATION_ERRP.md

Written and committed **before** the analysis is run. Second independent-dataset test, this time with a genuine
cross-session structure.

## Dataset

`E:\data\inria-bci-challenge` (Kaggle BCI Challenge, error-related potentials during a BCI task). 16 subjects,
5 sessions each in `train`, 80 CSV files, 56 EEG channels plus EOG, one `FeedBackEvent` marker column, and
`TrainLabels.csv` giving one binary label per feedback event (5440 events).

This dataset took no part in the development of the paper. Unlike the P300 set, it has **multiple sessions per
subject**, so it can probe cross-session transfer, which is the question the paper is about.

## Frozen design

| item | value |
|---|---|
| sessions used | each subject's sessions 1-5, in file order |
| pairs | consecutive forward pairs: 1->2, 2->3, 3->4, 4->5 (4 pairs per subject) |
| epochs | from each feedback marker, 0 to 600 ms after the marker |
| features | per-channel log-variance in four equal sub-windows (56 channels x 4 = 224) |
| classifier | LDA, solver lsqr, shrinkage auto, fitted on the source session only |
| correction | past-only, block 15, full displacement, applied to the target session |
| scored trials | target-session events after the first block of 15 |
| endpoint | delta balanced accuracy = BA(corrected) - BA(uncorrected), averaged over the four pairs per subject |
| statistic | subject-level mean; two-sided Wilcoxon and sign test across subjects; no multiplicity correction (single endpoint) |

## Prediction

The paper's theory makes the sign depend on what the displacement contains. For these data I cannot know in advance
whether the cross-session displacement is dominated by a real drift or by a change in the class mix, so **no
directional prediction is registered**. The test is two-sided and is labelled
**EXPLORATORY-INDEPENDENT**: independent data, pre-specified protocol, but no pre-specified sign, therefore not a
confirmatory test.

What would be informative either way:

- a large negative effect would replicate the sleep-EDF sign on independent cross-session data;
- a large positive effect would replicate the BCI sign;
- an effect near zero would say that cross-session mean correction is inert when the displacement is small.

## Reporting rules

All 16 subjects reported; no subject dropped; if a subject has fewer than two usable pairs it is reported
separately rather than silently removed. Class priors in source and target are reported per pair.
