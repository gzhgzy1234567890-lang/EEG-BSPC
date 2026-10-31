# EVENT_AND_WINDOW_AUDIT.md — BCI-IV-2b events, windows and trial counts

Audited against the GDF annotations read with MNE 0.23.4 and the pipeline in
`origin_equivariance/src/causal_2b.py` (commit b095b44).

## Event codes actually present

Read from the three sessions of subject 1:

| code | meaning in the BCI-IV-2b documentation | B0101T | B0102T | B0103T |
|---|---|---|---|---|
| 768 | trial start | 120 | 120 | 160 |
| 769 | cue, left hand | 60 | 60 | 80 |
| 770 | cue, right hand | 60 | 60 | 80 |
| 781 | continuous feedback | 0 | 0 | 160 |
| 1023 | rejected trial | 18 | 22 | 36 |
| 32766 | start of a run | 7 | 6 | 5 |
| 783 | discrete feedback | 0 | 0 | 0 |

## Cue latency

Measured: the nearest cue (769/770) follows a 768 marker by **3.0 s** in every session, not 2.0 s. This matters
because the pipeline epochs relative to the cue.

## Rejection rule

Every 1023 marker coincides with a 768 marker within 10 ms (18/18, 22/22, 36/36). Trials whose 768 is marked
1023 are dropped, and the numbers of kept trials are 102, 98 and 124 respectively, with near-perfect left/right
balance (51/51, 48/50, 60/64).

## Windows, as implemented

| dataset | code anchors the epoch at | offset | equivalent after cue |
|---|---|---|---|
| BCI-2a | 768 (trial start) | +2.0 to +6.0 s | **0.0 to 4.0 s** (cue is at +2.0 s) |
| BCI-2b | 769/770 (cue) | +0.5 to +3.5 s | 0.5 to 3.5 s |

## Discrepancy with the manuscript

The manuscript's preprocessing paragraph says "epochs from 2.0 to 6.0 s after cue onset". For 2a the code uses
2.0 to 6.0 s after the **trial start**, which is 0.0 to 4.0 s after the cue. The sentence is wrong by the cue
latency and must be corrected; it is a description error, not a data error, because the archived results were
produced by the code.

The two datasets also use different post-cue windows (0-4 s vs 0.5-3.5 s). This is a protocol difference and is
now stated as such in PROTOCOL_CAUSAL_V16.md; it is not corrected retrospectively, because re-windowing 2a would
create a third protocol whose results do not exist yet.

## Filtering across recording boundaries

Each GDF session is filtered as one continuous recording, with the filter state carried from the first sample to
the last and never reset at trial boundaries. This is the intended causal behaviour and matches the protocol.
No trial is scored within the first 5 s of a session, so the filter transient cannot affect a scored trial.

## Scored trials

Corrected and uncorrected conditions use the identical feature matrix and the identical trial vector; the only
difference is the subtraction of the past-only displacement. First block (15 trials) is unscored in both
conditions. This is asserted in `test_two_sided_ext.py`.

## Open items

- 2a cue latency is taken from the loader's comment and the BCI-IV-2a documentation, not measured from an
  annotation stream (the .mat files carry no events). If a reader requires the measurement, the cue timing would
  have to come from the original .gdf recordings, which are not present locally.
