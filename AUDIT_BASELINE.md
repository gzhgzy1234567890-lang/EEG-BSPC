# AUDIT_BASELINE.md

## Baseline

- repository: https://github.com/gzhgzy1234567890-lang/EEG-BSPC
- baseline commit audited: **5092c92** (Revision C: BCI-2b csp result, 2a statistics downgraded)
- manuscript at baseline: BSPC_Candidate_V8.docx, 18 pages, 9,345 words
- supplement at baseline: Supplementary_Material.docx, 27 pages, S1-S33
- audit archive: BSPC_Submission_Package_final.zip, 39 entries, FREEZE CHECK PASS at that commit

## What is in the baseline

| category | files |
|---|---|
| protocols | PROTOCOL_CAUSAL_V16.md (Revision C), PROTOCOL_SLEEP_TELEMETRY.md |
| causal experiments | origin_equivariance/src/causal_2a.py, causal_2b.py, analyze_causal.py, analyze_causal_2b.py, test_two_sided.py |
| sleep analyses | sleep_edf/sleep_edf_frozen.py, sleep_blockwise.py, sleep_blocks_all.py, sleep_bbse.py, matched_strata.py, composition_stats.py, check_numbers.py, check_s31.py |
| results | origin_equivariance/results/causal_2a.json, causal_2b.json, v1_baseline/causal_2a_v1.log; sleep_edf/results/*.json |
| manuscript chain | BSPC_Candidate_V8.docx/.pdf, Supplementary_Material.docx/.pdf, FREEZE_RECORD.md, SUBMISSION_CHECKLIST.md, REPRODUCIBILITY.md |

## Error history preserved (not overwritten)

| commit | state | why it matters |
|---|---|---|
| ddc4192 | causal_2a with a zero-centred estimator | wrong two-sided correction; kept as v1 baseline |
| 3732384 | estimator fixed, 2a rerun | first correct two-sided numbers |
| b012fda | 2x2 factorial on 2a | separated filter and EA effects |
| 5092c92 | 2b csp result, 2a statistics downgraded | baseline for this audit |
| this round | relative whitening floor; 2b rerun; EA audit | fixes the EA defect found in A2 |

## Claim-evidence chain

See CLAIM_EVIDENCE_MATRIX.csv: one row per manuscript claim, with protocol, dataset, code, output, test and
evidence class.

## Standing rule for this audit

No number is quoted in any audit document unless it can be produced by a named script from a named input file at
a named commit. Where that chain is broken, the item is marked BLOCKED in CURRENT_BLOCKERS.md.
