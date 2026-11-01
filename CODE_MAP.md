# CODE_MAP.md

Which script produces which number, at which commit. Written in response to the referee's request for an explicit
mapping between the audit code and the submitted version.

Repository: https://github.com/gzhgzy1234567890-lang/EEG-BSPC, commit **a735d6a** at the time of this map (the map
itself is committed with the revision that contains it; the authoritative pointer is the commit that adds this
file).

| result | script | output | seed |
|---|---|---|---|
| 2b 2x2 table, all representations | `origin_equivariance/src/causal_2b.py` | `origin_equivariance/results/causal_2b.json` | 20261101 |
| 2b independent recomputation | `origin_equivariance/src/recompute_2b.py` | `results/statistics_recomputed_2b.json` | 20261101 |
| 2a 2x2 table | `origin_equivariance/src/causal_2a.py` | `results/causal_2a.json` | 20261101 |
| past-only assertions (K = 2, 3, 4) | `origin_equivariance/src/test_two_sided_ext.py` | stdout, "ALL ASSERTIONS PASSED" | - |
| theory regression tests, revision 2 | `origin_equivariance/src/theory_test_rev2.py` | stdout, "THEORY TEST PASS" | - |
| referee claim checks (MC1-MC4) | `origin_equivariance/src/verify_referee_claims.py` | stdout | - |
| certificate, nine subjects | `origin_equivariance/src/c2_certificate_all.py` | `results/c2_certificate_all.json` | - |
| D1 controlled grid | `origin_equivariance/src/sim_d1.py` | `results/d1_grid.json` | 20261101 |
| D5 prior control | `sleep_edf/d5_priors.py` | `sleep_edf/results/d5_priors.json` | 20261101 |
| D3 matched, six specifications | `sleep_edf/d3_blocks.py` + `sleep_edf/analyze_d3.py` | `results/d3_matched.json`, `d3_blocks.json` | - |
| concentration regeneration | `sleep_edf/d3_concentration.py` + `analyze_concentration.py` | `results/d3_concentration.json` | - |
| sleep hierarchy recomputation | `sleep_edf/b3_hierarchy.py` | `results/b3_hierarchy.json` | 20261101 |
| BBSE support split | `sleep_edf/d4_recheck.py` (in `paper_v8/`) | `results/sleep_bbse2.json` | - |
| P300 pre-registered and exploratory | `p300_external.py`, `p300_external_explore.py` | `p300_results/*.json` | 20261101 |
| ERRp cross-session | `errp_external.py` | `errp_results/errp_external.json` | - |
| bootstrap intervals for the two external corpora | `p300_ci.py` | stdout | 20261101 |
| cross-document consistency | `consistency_check.py` | stdout, "CONSISTENCY PASS" | - |
| package build and hashes | `tools_build_package.py` | `BSPC_Submission_Package_final.zip` | - |

## What is not in the archive

The audit ZIP contains documents, not executables. The code lives in the repository above; the raw EEG is not
redistributable and is not included. A reader can therefore check every number against the archived JSON and re-run
the scripts against the public corpora, but cannot regenerate the raw EEG from the ZIP alone. This limitation is
stated in the manifest as well.

## Reproducing one number, end to end

```
git clone https://github.com/gzhgzy1234567890-lang/EEG-BSPC
cd EEG-BSPC
python origin_equivariance/src/recompute_2b.py     # prints csp +0.0341 [+0.0104, +0.0585], p = 0.0391
```

That script reads only the archived JSON, so it needs no EEG data at all.
