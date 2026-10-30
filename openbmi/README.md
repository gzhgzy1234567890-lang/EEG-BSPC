# OpenBMI / Lee2019-MI external validation

Python 3.7 with scipy, numpy, scikit-learn 1.0.

- lee2019_direct.py - loads the two MAT sessions directly (EEG_MI_train.x, .t, .y_dec, .fs),
  epochs 0-4 s after cue, builds 62-channel x 4-band log-variance features, fits source-only LDA and
  evaluates the completed-block estimator over the frozen lambda grid.
- lee2019_parallel.py - eight download threads from the GigaDB S3 mirror, four evaluation
  processes, resumable through openbmi_all.json.
- lee2019_secondary.py - four estimators (completed block, cumulative, window 50, exponential 0.05)
  by five strengths.

Protocol: OPENBMI_FROZEN_PROTOCOL.md (sha256_16 2a935aecb2c461f3). One amendment is recorded:
the epoch window moved from the protocol's 2-6 s to the reference implementation's 0-4 s before any
external prediction existed.

Results: openbmi_all.json holds the per-subject BA at lambda = 0 and 1 and the paired difference;
lee2019_secondary.json holds the full estimator-by-strength surface. Main result: n = 54,
mean paired difference +0.0319, 95 per cent CI [+0.0159, +0.0479], p = 0.0002, 18 subjects negative.
