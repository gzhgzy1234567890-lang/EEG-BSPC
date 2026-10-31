# CURRENT_BLOCKERS.md

Final state. Two blockers remain; both are external to this environment and neither can be resolved by further
work here.

## B1. SEED raw waveforms absent

- **Verified**: `E:\data\SEED-all\seed` contains only `ExtractedFeatures_1s`, `ExtractedFeatures_4s` and the
  stimulus table. No `Preprocessed_EEG` directory, no `.cnt` file anywhere on the volume.
- **Blocks**: the raw-to-feature causal rerun, five-band DE re-extraction, and a filter-only comparison against the
  archived +0.214.
- **Allowed**: past-only mean estimation on the released DE features, labelled as such.
- **Resolution**: obtain `Preprocessed_EEG` (15 subjects) or the SEED-Multimodal `.cnt` set (12 subjects).
- **Record**: SEED_RAW_CAUSAL_BLOCKED.md.

## B2. No third-party replication

- Every execution in this repository was performed by the authors or by this assistant. No external group has run
  the package.
- **Blocks**: the claim of independent reproduction; the gate "AI internal recomputation called third-party" stays
  clean only because no such claim is made.
- **Resolution**: an external group runs `REPRODUCIBILITY_REPORT.md` and reports hashes.

## Resolved during the project

| id | item | resolution |
|---|---|---|
| B3 | BCI-2a cue latency taken from an internal comment | verified against the official data-set description (Brunner et al. 2008) and cited [26] |
| B4 | no dataset outside the development corpora | two independent corpora added: P300 speller (single session) and BCI challenge (five sessions per subject) |
| B5 | 2b alignment effect exactly zero | traced to an absolute eigenvalue floor, fixed with a relative floor, rerun |
| B6 | manuscript window sentence contradicted the code | sentence corrected and the 2a/2b difference stated |
| B7 | 16 audit documents were never packaged | build list fixed; archive verified to contain all 67 entries |

## Not blockers, recorded for completeness

- Holm correction is vacuous with one live test and is described as such.
- The concentration contrast was withdrawn after failing regeneration; it is not a blocker, it is a removed claim.
