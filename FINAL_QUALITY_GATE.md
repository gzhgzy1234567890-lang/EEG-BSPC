# FINAL_QUALITY_GATE.md

Updated after the missing G5 deliverables were created and a **package-completeness defect** was found and fixed.

| item | max | score | evidence path | unmet |
|---|---:|---:|---|---|
| A | 15 | 15 | AUDIT_BASELINE.md; FILE_PROVENANCE.csv (14 artefact hashes); MANUSCRIPT_CHANGELOG.md from the git log | - |
| B | 20 | 17 | EVENT_AND_WINDOW_AUDIT.md; test_two_sided_ext.py | 2a cue latency from documentation |
| C | 15 | 15 | THEORY_PROOFS.md; THEORY_COUNTEREXAMPLES.md (eight probes, two failed constructions); THEORY_TEST_RESULTS.md; C2 | - |
| D | 15 | 13 | STATISTICAL_AUDIT.md; statistics_recomputed_2b.json | - |
| E | 10 | 10 | SLEEP_MECHANISM_AUDIT.md; MECHANISM_LIMITATIONS.md; D3 and concentration regenerations | - |
| F | 10 | 10 | NOVELTY_MATRIX.md on full texts; RELATED_WORK_VERIFICATION.md; NOVELTY_RISK_REPORT.md | - |
| G | 10 | 9 | REPRODUCIBILITY_REPORT.md; every claimed number regenerated or withdrawn | no third-party replication |
| H | 5 | 4 | all documents consistent; **package now contains all 16 audit documents it previously omitted** | the omission defect itself is a consistency failure that cost a point |
| **total** | **100** | **93** | | |

## The defect found this round

The package build script used a hand-written file list. Every earlier build silently omitted the newer audit
documents: NOVELTY_MATRIX, SLEEP_MECHANISM_AUDIT, STATISTICAL_AUDIT, EXTERNAL_VALIDATION_REPORT,
LIMITATIONS_AND_BLOCKERS, REPRODUCIBILITY_REPORT, THEORY_COUNTEREXAMPLES, D3_MATCHED_REGENERATION,
CONCENTRATION_RECONCILIATION, C2_CERTIFICATE_RESULTS, SEED_RAW_CAUSAL_BLOCKED, RELATED_WORK_VERIFICATION,
NOVELTY_RISK_REPORT, MECHANISM_LIMITATIONS, MANUSCRIPT_CHANGELOG and FILE_PROVENANCE. The archive reported
"51 entries" for several rounds while these files existed only in the working directory. The list is now explicit
and the archive has **67 entries, all 16 present**, verified by listing the zip.

## Hard gates

All pass at this commit. The omission was a packaging failure, not a scientific one, but it is exactly the kind of
"document says one thing, package contains another" defect a reproducibility reviewer would flag.

## Verdict

**Not approved as complete** (93 < 96). Remaining: third-party replication (B2), SEED waveforms (B1), independent
dataset (B4).
