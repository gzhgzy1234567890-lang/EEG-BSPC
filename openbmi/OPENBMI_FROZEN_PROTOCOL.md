# OPENBMI (Lee2019-MI) FROZEN PROTOCOL

Status: **frozen before any target-day result was read**. No OpenBMI data have been
downloaded, parsed or scored in this session; the environment has no network access,
so this file fixes the design that will be executed when the data are available.

- Generated: 2026-10-29, Asia/Shanghai.
- Frozen against analysis commit: `b4e4019eb0` (the repository state that produced the
  development results); the execution script must record its own commit and the hash
  of this file in the output.
- Amendments after this point are only allowed as appended, dated entries, and every
  deviation must be reported in the final table.

## 1. Data

- Dataset: Lee2019-MI as distributed for OpenBMI (54 subjects, two sessions on
  different days, left/right hand motor imagery).
- Sessions used: the **labelled offline training phase of each day**. The online test
  phase is not used, because its trials carry no labels usable for supervised scoring.
- Source: day 1 offline phase.
- Target: day 2 offline phase; its labels are used **only** for the final scoring.
- Inclusion: all 54 subjects. A subject is excluded only for a predefined data-quality
  reason (fewer than 30 labelled trials on either day, or a recording that fails to
  load); every exclusion is listed with its reason.

## 2. Signal path (frozen)

1. Band-pass 8-30 Hz, fourth-order Butterworth, zero-phase **within each day
   separately** (no filter state crosses days).
2. Epochs 2.0-6.0 s after cue onset.
3. Features: log-variance in four bands, per channel, computed from the epoch only.
4. No target-day standardisation, no target-day covariance, no target-day feature
   selection. The classifier and its reference statistics come from day 1 alone.
5. Classifier: LDA fitted on day 1 (`solver='lsqr'`, `shrinkage='auto'`), identical to
   the development pipeline.

## 3. Online protocol (frozen)

- Trial order is the acquisition order of the day-2 offline phase.
- Warm-up: the first 15 target trials are **not scored** and no correction is applied.
- From trial 16 onward, the correction at trial t uses only trials that ended before
  the block containing t was completed; blocks are consecutive groups of 15 trials.
- Estimators: completed-block mean (primary), cumulative, sliding window of 50 trials,
  exponential with alpha = 0.05 (secondary).
- Strengths: lambda in {0, 0.25, 0.50, 0.75, 1.00}; lambda = 0 is exactly no correction.
- No parameter is selected on day-2 data. The lambda grid and the estimators are fixed
  by this file.

## 4. Endpoints

- **Primary**: per subject, balanced accuracy on the identical scored trials,
  completed-block mean at lambda = 1 minus lambda = 0.
- Primary statistic: mean paired difference over included subjects, 95 per cent CI
  (bootstrap over subjects, 10,000 resamples), two-sided sign test.
- **Secondary**: the four estimators x five strengths response surface; the number of
  subjects with a negative difference.
- **Exploratory**: class-prior decomposition of the block mean, reverse-day analysis
  (train on day 2, test on day 1), and any other post-hoc analysis. These are labelled
  exploratory and do not enter the primary claim.

## 5. Information boundary

- The correction never uses a trial from the block being scored or later.
- The causal audit is repeated on this data: every feature from trial k onward is
  replaced by noise and the predictions before k must be unchanged (exact equality).
- Filtering, epoching and feature construction are per-day, so no future sample of the
  target day enters any stage.

## 6. What will be reported regardless of outcome

- The number of included subjects and every exclusion.
- Balanced accuracy with and without correction, the paired difference, its CI, and
  the distribution of per-subject differences (improved / degraded / unchanged).
- The full response surface, including cells that contradict the development findings.
- If the cross-day effect is near zero or heterogeneous, that is reported as such; a
  non-significant result is not described as evidence of no effect.
