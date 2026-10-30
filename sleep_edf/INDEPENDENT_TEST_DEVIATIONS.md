# Deviations from the frozen sleep-EDF protocol

The frozen file is `INDEPENDENT_TEST_PROTOCOL.md` (sha256_16 `2a935aecb2c461f3`, unchanged). The protocol
requires that any change after freezing be recorded here. This file was created on 31 October 2026, after
an external review pointed out that the first implementation differed from the frozen text in ways this
record had not captured.

Two runs are reported: the **first implementation** (`sleep_edf_test.py` + `sleep_edf_run.py`, the numbers
in the first V8 revision) and the **protocol-consistent re-run** (`sleep_edf_frozen.py`, the numbers now in
the manuscript). Both use the same frozen endpoint, classifier, block length, warm-up rule and sign test.

## D1. Subject and night set

- **Frozen text:** "20 subjects, two nights each where both files exist (PSG plus hypnogram)."
- **Executed, both runs:** every PSG in the cassette that pairs with a hypnogram under the naming
  convention, subject to the inclusion rules. That yields **45 nights from 32 subjects**, 13 of which
  contribute two nights. The public subset available here does not contain 20 subjects with two nights.
- **Consequence:** the unit is still the subject, but the cohort is 32 subjects, not 20. The pre-specified
  sign test and bootstrap are unchanged.

## D2. Stage definition

- **Frozen text:** five stages, W, N1, N2, N3, REM.
- **First implementation:** six labels, W, 1, 2, 3, 4, R, with stage 4 left separate (`STAGES.index`).
- **Protocol-consistent re-run:** stage 3 and stage 4 merged into N3, giving the five frozen classes.
- **Consequence:** the merged run has fewer classes; LDA, balanced accuracy and the correction all change
  slightly. This is why the two runs differ.

## D3. Filter implementation

- **Frozen text:** "Band-pass 0.5-30 Hz, fourth-order Butterworth, zero-phase, applied to each series
  separately."
- **First implementation:** MNE FIR band-pass 0.5-30 Hz on the **whole night**, then a fourth-order
  Butterworth `filtfilt` per band on the whole night; epoching afterwards.
- **Protocol-consistent re-run:** fourth-order Butterworth 0.5-30 Hz, `filtfilt`, applied to the two
  channels of **each 30-minute series separately**, then the four band filters on that series only.
- **Consequence:** the first run allowed filter state to cross series boundaries and used a different
  filter type. The re-run is the frozen path.

## D4. Inclusion rules

- **Frozen text:** a night is excluded if fewer than four complete series remain or fewer than two stages
  are present.
- **First implementation:** nights were dropped only when fewer than two series remained; no night-level
  stage test was applied; pairs additionally required at least two classes in both the source and the
  target series.
- **Protocol-consistent re-run:** the two frozen night-level rules are applied, and the pairwise
  two-class requirement is retained (LDA cannot be fitted to a single-class source and balanced accuracy
  is undefined for a single-class target). The pairwise rule is therefore recorded here as a deviation
  that is unavoidable rather than discretionary.

## D5. Series construction

- **Frozen text:** 30-s epochs, contiguous; series of 60 epochs; trailing epochs dropped.
- **First implementation:** unlabelled epochs were deleted first and the remaining epochs were grouped
  in sixties, so a series could span a gap in the original recording.
- **Protocol-consistent re-run:** the night is cut into contiguous labelled runs first, and series are
  taken inside a run only; a series never crosses an unlabelled epoch.

## D6. Subject aggregation

- **Frozen text:** the primary comparison is averaged within cell, then within subject.
- **First implementation:** all of a subject's cells were pooled, so a night with more cells carried more
  weight.
- **Protocol-consistent re-run:** a subject's value is the **equal-weight mean of that subject's night
  means**; the pooled value is reported beside it.

## D7. Subject identifier (code defect, fixed)

The first aggregation script keyed subjects on the first **four** characters of the file name, which
collapses ten subjects into one and reports seven units instead of 32. The key is the first **five**
characters (`SC4xx`); the sixth is the recording index. Fixed before this note was written; re-aggregating
the stored cells with the correct key reproduces the reported subject-level numbers.

## Both results

| quantity | first implementation | protocol-consistent re-run |
|---|---|---|
| stages | 6 (N3 and N4 separate) | **5 (S3+S4 = N3)** |
| filter | FIR 0.5-30 Hz whole night + per-band on the night | **4th-order Butterworth per series** |
| series | 60 epochs, may span gaps | **contiguous runs only** |
| inclusion | <2 series | **<4 series or <2 stages** |
| subject value | pooled cells | **equal-weight night means** (pooled beside it) |
| nights / subjects / cells | 45 / 32 / 5,537 | **45 / 32 / 4,983** |
| mean difference, subject | -0.1084 | **-0.1023** (pooled -0.1017) |
| bootstrap 95 per cent interval | [-0.121, -0.096] | **[-0.114, -0.090]** |
| subjects negative | 32 of 32 | **32 of 32** |
| sign test | p = 4.7e-10 | **p = 4.7e-10** |
| night-level mean (secondary) | -0.1091, 45 of 45 | **-0.1018 [-0.113, -0.091], 45 of 45, p = 5.7e-14** |

## What the paper now claims

The protocol-consistent run reproduces the negative transfer: every one of 32 subjects and every one of
45 nights is negative, with a mean difference of -0.102 against -0.108 in the first implementation. The
magnitude is about 6 per cent smaller and the interval is narrower.

The paper therefore reports the protocol-consistent numbers and cites this file. It does **not** describe
the replication as a literal execution of the frozen text: D1 (cohort size), D2 (stage merge until the
re-run), D4 (pairwise two-class rule) and D5-D6 (series construction and aggregation, in the first
implementation) are deviations, and the evidence should be read as an independent replication under a
documented protocol rather than as a pre-registered confirmation with zero deviation.

If the re-run had changed the sign or the significance, the paper would have had to downgrade the claim;
it did not, and both runs are archived so that a reader can check the difference.
