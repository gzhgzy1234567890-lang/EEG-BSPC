# Grasp-and-lift: the cached trial order is class-sorted, and the negative transfer is an artefact of it

**Status: stop-the-press correction.** This file supersedes the grasp-and-lift claims of the V8
manuscript. It was produced on 31 October 2026 in response to a referee report (Major Comment 1) that
asked whether the cached trials are in acquisition order.

## 1. What the cache contains

`local_analysis/cache_gal/*.npz` (96 series, 256 features = 32 channels x 8 windows):

| observation | value |
|---|---|
| samples per series | 56 or 68 |
| class counts | exactly 28/28 or 34/34 |
| order of the labels | **all zeros first, then all ones** |
| HandStart events in the raw recording | 28 or 34 |

The raw series have 28-34 grasp trials, and the cache has exactly two samples per trial, stored with the
class-0 samples first. The label sequence in every one of the 96 files is `0 0 ... 0 1 1 ... 1`; the
switch is at exactly half the file in all 96. That is not an acquisition order: grasp trials occur
throughout a series, and a real sequence alternates between the pre-movement and movement windows of
successive trials.

## 2. Rebuild in true order

`paper_v8/build_gal_time.py` rebuilds the features from the raw CSVs in
`E:\data\grasp-and-lift-eeg-detection\train`:

- HandStart onsets from `*_events.csv` (34 trials for `subj1_series1`);
- class 0 = the 2 s **before** the onset, class 1 = the 2 s **after** it;
- 32 channels, 0.5-30 Hz fourth-order Butterworth zero-phase, log power in 8 consecutive 250-ms windows;
- samples stored in trial order, so the label sequence is `0 1 0 1 ...` — real time.

The rebuilt files have the same shape as the published cache (68 x 256 with 34 positives, or 56 x 256 with
28), so the comparison below changes **only the order of the samples**, not the task or the features.

## 3. The same estimator on three orderings

Estimator: LDA (`lsqr`, Ledoit-Wolf) fitted on the source series; correction by the completed-block mean of
the decision-space displacement, blocks of 15, first block unscored; balanced accuracy on the remaining
trials; 336 cells (12 subjects x 28 series pairs); lambda swept 0 -> 1. Script: `paper_v8/gal_order_test.py`.

| cache | BA at lambda = 0, .25, .5, .75, 1 | delta(1-0) |
|---|---|---|
| published cache (original features, class-sorted) | 0.7727, 0.7584, 0.7318, 0.6997, 0.6652 | **-0.1075** |
| rebuilt features, **class-sorted** (control) | 0.7925, 0.7835, 0.7644, 0.7406, 0.7025 | **-0.0901** |
| rebuilt features, **true time order** | 0.7874, 0.7907, 0.7910, 0.7902, 0.7889 | **+0.0014** |

The published -0.108 is reproduced exactly by the paper's own cache, and the same features reproduce a
comparable loss (-0.090) when they are stored in the published (class-sorted) order. With the samples in
acquisition order the effect is **+0.001**: no negative transfer, and a flat strength curve.

## 4. Why sorting manufactures the effect

In the sorted order the target sequence changes class once at its midpoint. A completed-block mean
(block = 15 samples) therefore carries a large class-prior step in the second half of every cell, and
subtracting it moves the decision scores away from the majority class of each half. In acquisition order
every block of 15 covers about seven trials, so it contains both classes and the running mean is close to
zero; the correction is almost inert (the BA curve is flat to within 0.004).

This is the mechanism the paper attributed to "within-recording non-stationarity". It is a property of the
cache, not of the recording.

## 5. Consequences for the paper

1. **The grasp-and-lift negative transfer is withdrawn.** Section 4.4, Table 9's grasp-and-lift row,
   Fig. 4, the abstract, the overview, the highlights, the cover letter and the conclusion all rest on it.
2. **The trend diagnostics go with it.** Section 4.5 and Table 11, the rho = 0.776 association and the
   partial r = -0.08 are computed on the sorted cells; the "temporal structure" reading must be removed.
3. **Section 4.6's composition analysis still describes the cache correctly** (the block profiles are a
   property of the sorted order), but its interpretation changes: it explains the artefact, not a
   mechanism of mean correction.
4. **The sleep-EDF replication is unaffected**: its series are cut from a continuous recording in real time.
   The class-set stratification added in response to Major Comment 2 supports it:

| target class set | cells | subject mean | subjects negative |
|---|---|---|---|
| identical to source | 693 | **-0.0608** | 29 of 32 (p = 2.6e-6) |
| a subset of the source | 1,070 | -0.1473 | 31 of 32 |
| contains a class absent from the source | 3,220 | -0.0918 | 32 of 32 |

   The negative sign survives in the cleanest subset, which is the one where the classifier is asked only
   about classes it has seen.

## 6. What the paper can still claim

- A negative transfer of past-only mean correction **is observed on sleep-EDF**, in real time order, in
  32 of 32 subjects, and in 29 of 32 when the source and target class sets are identical.
- The same correction is **beneficial on SEED and on the two motor-imagery datasets** as reported, though
  the ordering of those caches has not yet been audited.
- A **methodological result** is now available and is arguably stronger than the original claim: storing
  trials class-sorted manufactures a strong, highly significant negative transfer (-0.09 to -0.11) that
  disappears when the same features are stored in acquisition order (+0.001). That is a concrete warning
  about cache construction in cross-session EEG analyses.

## 7. Reproduction

```
python paper_v8/build_gal_time.py 'subj*'      # rebuild all 96 series in time order (~8 min)
python paper_v8/make_sorted_control.py         # same features, class-sorted
python paper_v8/gal_order_test.py              # the three-way comparison above
python paper_v8/sleep_class_overlap.py         # the class-set stratification
```

Raw data are not shipped; the scripts read the public Kaggle grasp-and-lift CSVs and the sleep-EDF cassette.

## 8. What this means for the submission

The V8 package must not be submitted as it stands. Two coherent revisions are available:

- **A (recommended, no new data):** re-scope the paper around the sleep-EDF replication and the cache-order
  methodological finding. The grasp-and-lift section becomes the demonstration that a common cache
  construction produces a spurious negative transfer. Title, abstract, results, highlights and cover letter
  change; the theory, the estimator comparison and the SEED/BCI positive evidence remain.
- **B:** rebuild every grasp-and-lift analysis on the time-ordered cache (the scripts exist, the pipeline
  matches), report the null result and keep the paper as a single-dataset replication with a strong
  methods warning.

Both require the same first step: remove the sorted-cache numbers from every claim. This file records that
step; the manuscript edit itself has not been applied yet.
