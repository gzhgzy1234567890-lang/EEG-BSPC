# EVENT_AND_WINDOW_AUDIT.md — BCI-IV-2b events, windows and trial counts

Audited against the GDF annotations read with MNE and the pipeline in `origin_equivariance/src/causal_2b.py`.

## Event codes actually present

| code | meaning (BCI-IV-2b documentation) | B0101T | B0102T | B0103T |
|---|---|---|---|---|
| 768 | trial start | 120 | 120 | 160 |
| 769 | cue, left hand | 60 | 60 | 80 |
| 770 | cue, right hand | 60 | 60 | 80 |
| 781 | continuous feedback | 0 | 0 | 160 |
| 1023 | rejected trial | 18 | 22 | 36 |
| 32766 | start of a run | 7 | 6 | 5 |
| 783 | discrete feedback | 0 | 0 | 0 |

## Cue latency

Measured: the nearest cue (769/770) follows a 768 marker by **3.0 s** in every session.

## Rejection rule

Every 1023 coincides with a 768 within 10 ms (18/18, 22/22, 36/36); kept trials are 102, 98 and 124, with
near-balanced classes.

## Windows, and the 2a timing verified against the official description

| dataset | code anchors the epoch at | offset | equivalent after the cue |
|---|---|---|---|
| BCI-2a | 768 (trial start) | +2.0 to +6.0 s | **0.0 to 4.0 s** |
| BCI-2b | 769/770 (cue) | +0.5 to +3.5 s | 0.5 to 3.5 s |

The 2a cue latency is no longer taken from the loader comment. The official BCI Competition IV data set 2a
description (Brunner, Leeb, Mueller-Putz, Schloegl, Pfurtscheller, 2008) states: a fixation cross appears at
t = 0, "after two seconds (t = 2 s), a cue ... appeared and stayed on the screen for 1.25 s", and the subject
imagined until "the fixation cross disappeared from the screen at t = 6 s". So an epoch from t = 2 to t = 6 s is
exactly the cue-to-fixation-off interval, i.e. 0 to 4 s after the cue, and the manuscript's trial-relative wording
is correct.

## Discrepancy found in an earlier manuscript version (fixed)

The preprocessing paragraph used to say "2.0 to 6.0 s after cue onset", which would have been 4.0 to 8.0 s after the
trial marker. The code and the official description agree with 2.0 to 6.0 s after the **trial onset**. The
sentence was corrected; the archived results were always those of the code.

## Protocol difference between the datasets

2a epochs cover 0-4 s after the cue, 2b covers 0.5-3.5 s. This is a difference between the two corpora and is
stated as such in PROTOCOL_CAUSAL_V16.md; it is not corrected retrospectively.

## Filtering across recording boundaries

Each GDF session is filtered as one continuous recording, state carried from first to last sample, never reset at
trial boundaries. No trial is scored within the first 5 s of a session, so the transient cannot reach a scored
trial.

## Scored trials

Corrected and uncorrected conditions share the identical feature matrix and trial vector; the only difference is
the subtracted displacement. The first block (15 trials) is unscored in both.
