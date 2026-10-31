# Frozen protocol: unified source-only, past-only main experiment (v16, revision C)

Frozen 31 October 2026. Revision C records the BCI-2b run, corrects the statistical reading of the 2x2 on
BCI-2a, fixes the CSP rationale, and states what the SEED data would and would not license.

## Estimator

Unchanged: d_b = P(s-bar_{1..b-1} - s-bar_A), blocks of 15, first block unscored, lambda = 1. Unit test
`test_two_sided.py` passes.

## BCI-2a: 2x2 factorial, statistical reading corrected

| | source-only EA | both-session EA |
|---|---|---|
| causal | +0.0705 | +0.0620 |
| non-causal | +0.0805 | +0.0738 |

- alignment +0.0077 [-0.0057, +0.0224], Wilcoxon p = 0.65
- filter -0.0109 [-0.0197, -0.0021], **Wilcoxon p = 0.13**
- interaction +0.0017, p = 0.91

The bootstrap interval for the filter effect excludes zero while the signed-rank test does not, because the two
target different quantities. The protocol fixes Wilcoxon as the confirmatory test, so the correct statement is:
the causal filter is associated with a 0.011 lower gain, the bootstrap interval supports a negative value, but
the signed-rank test does not reach 0.05, and the result is reported as exploratory, not as established.

**What the filter contrast identifies.** `lfilter` and `filtfilt` differ in amplitude response, phase and edge
behaviour, not only in whether future samples are read. The -0.011 is therefore the effect of this specific
filter pair under this protocol, and is not attributed to future-information access alone. Effective magnitude
and phase responses of both filters are reported as supplementary material.

## BCI-2b: pre-specified primary endpoint, result

Three forward pairs (01T->02T, 01T->03T, 02T->03T), 9 subjects, csp fixed in advance as the primary endpoint.
The choice is justified because csp is fitted on the training session only by construction, not because it is
the only source-only representation: euc is source-only as well, and euc_ea and tan have source-only variants
in this protocol. BCI-2b has three EEG channels, so the CSP step yields **two** generalized eigenfilters, not
six as in 2a; the implementation derives the number from the channel count.

| representation | causal + source-only EA | subjects positive | Wilcoxon p |
|---|---|---|---|
| **csp (primary)** | **+0.0341 [+0.0104, +0.0585]** | 8/9 | 0.039 |
| euc | +0.0317 [+0.0167, +0.0472] | 9/9 | 0.0039 |
| euc_ea | +0.0350 [+0.0198, +0.0506] | 8/9 | 0.0078 |
| tan | +0.0483 [+0.0219, +0.0738] | 8/9 | 0.020 |

Filter effects per representation: csp -0.0058 (p = 0.25), euc +0.0071 (p = 0.25), euc_ea +0.0061 (p = 0.30),
tan +0.0079 (p = 0.055). The alignment factor is identically zero for all four, so it has no Wilcoxon p value.

Because the development work had already used BCI-2b, this is a prospective test on a familiar dataset, not an
independent confirmation.

## SEED: what the data would and would not license

Local data contain only the released DE features; no waveform data are present. Beyond that, obtaining
`Preprocessed_EEG` would still not license attributing a difference from the archived +0.214 to the filter,
because that release is already filtered (0-75 Hz), downsampled to 200 Hz and split by film, and any
re-extraction would also change the smoothing, the band edges and the scored samples. A filter-only comparison
would need identical inputs, identical feature rules and identical scored trials, with only the filter changed.
Until then SEED is reported as a past-only mean-estimation experiment on the official cached features, and the
paper does not describe it as an end-to-end causal pipeline.

## Statistics

Subject-level paired values; 95 per cent bootstrap (10,000 resamples, seed 20261101); two-sided Wilcoxon as the
confirmatory test; Holm across the pre-specified primary tests (BCI-2b csp and, if run, the SEED primary).
