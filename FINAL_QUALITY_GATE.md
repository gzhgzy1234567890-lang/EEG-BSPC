# FINAL_QUALITY_GATE.md

Updated after the BCI-2a cue timing was verified against the official data-set description and cited.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | FILE_PROVENANCE.csv; MANUSCRIPT_CHANGELOG.md; pre-registrations committed before runs | - |
| B | 20 | **18** | EVENT_AND_WINDOW_AUDIT.md now cites Brunner et al. 2008 (t = 0 fixation, cue at t = 2 s, imagery to t = 6 s); the 2a window is the cue-to-fixation-off interval; test_two_sided_ext.py | 2a timing verified from the published description rather than from raw 2a annotations, which are not in the local corpus |
| C | 15 | 15 | THEORY_PROOFS.md; THEORY_COUNTEREXAMPLES.md; THEORY_TEST_RESULTS.md | - |
| D | 15 | 13 | STATISTICAL_AUDIT.md; both independent pre-registrations | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; MECHANISM_LIMITATIONS.md; three regenerations | - |
| F | 10 | 10 | NOVELTY_MATRIX.md on full texts; two independent corpora | - |
| G | 10 | 9 | REPRODUCIBILITY_REPORT.md | no third-party replication |
| H | 5 | 4 | documents consistent; word count now synced from Word rather than estimated | earlier count slips | 
| **total** | **100** | **94** | | |

## The last documentation-dependent item is closed

The 2a cue timing was the only claim resting on an internal code comment. The official BCI Competition IV data set
2a description states the fixation cross at t = 0, the cue at t = 2 s and imagery until t = 6 s, so an epoch from
2 to 6 s after the trial marker is exactly 0 to 4 s after the cue. The manuscript now cites that description [26].

## Hard gates

All pass.

## Verdict

**Not approved as complete** (94 < 96). Two points remain and both are external: a third-party replication (G) and
the SEED raw waveforms (part of F, already documented as BLOCKED).
