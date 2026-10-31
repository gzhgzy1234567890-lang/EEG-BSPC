# SEED_RAW_CAUSAL_BLOCKED.md

## Checked

| item | finding |
|---|---|
| `E:\\data\\SEED-all\\seed` | contains `ExtractedFeatures_1s`, `ExtractedFeatures_4s`, the stimulation table and channel metadata |
| `Preprocessed_EEG` directory | **absent** |
| `.cnt` files anywhere on E: | **none** |
| consequence | no raw or continuous waveform is available locally |

## What this blocks

The strict raw-to-feature causal pipeline for SEED cannot be executed here. Specifically it blocks:

- causal filtering of continuous EEG with per-film state reset;
- five-band DE re-extraction (1-4, 4-8, 8-14, 14-30, 30-50 Hz);
- a filter-only comparison against the archived +0.214.

## What is still allowed

Past-only mean estimation **on the released DE features**. That is a statement about the estimator, not about the
feature pipeline, and the manuscript must label it that way. It also must not attribute a difference from +0.214
to filtering unless the features and scored trials are held fixed.

## Resolution path

1. obtain `Preprocessed_EEG` (15 subjects) or the SEED-Multimodal `.cnt` set (12 subjects);
2. confirm sample rate and the preprocessing already applied;
3. freeze the five-band protocol and the film-boundary rule;
4. re-extract, re-run, and compare on identical scored trials.

Until then this item is BLOCKED, not failed and not done.
