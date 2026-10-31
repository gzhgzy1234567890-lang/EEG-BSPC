# GOAL_ROUND_LOG.md

## Round 1 (this round)

- git commit before: b095b44
- git commit after: (see the commit produced by this round)
- phase: A (A1 done previously, A3/A4/A5 executed now)
- tasks open at start: A3 event/window audit, A4 extended assertions, A5 2x2 recompute, B-G
- executed this round:

| task | action | evidence |
|---|---|---|
| A3 | read GDF annotations for B0101T/0102T/0103T with MNE; measured event codes, cue latency (3.0 s), rejection coincidence (all 1023 coincide with a 768), kept trials (102, 98, 124) | EVENT_AND_WINDOW_AUDIT.md |
| A3 | compared implemented windows (2a: trial+2..6 s = cue+0..4 s; 2b: cue+0.5..3.5 s) with the manuscript sentence | same file, "Discrepancy" section |
| A4 | wrote and ran test_two_sided_ext.py: K=2,3,4; score vs feature label agreement 1.0000; score-space displacement equals projected feature-space displacement (<1e-10); future-perturbation invariance (<1e-12); block lengths 5/15/20; first block unscored | script output in this log |
| A5 | wrote recompute_2b.py, which reads only the JSON and rebuilds the 2b table; results match the analysis script (csp +0.0341, p=0.0391) | results/statistics_recomputed_2b.json |
| B1 | froze the statistical family in STATISTICAL_ANALYSIS_PLAN.md | file |

- commands run: test_two_sided_ext.py, recompute_2b.py, audit_events.py, audit_events2.py
- test output: "K=2/3/4 score-vs-feature label agreement 1.0000 ... ALL ASSERTIONS PASSED";
  recompute table: csp +0.0341 [+0.0104, +0.0585], p=0.0391
- problems found: (i) the manuscript's 2a window sentence is wrong (2-6 s after trial start, not after cue);
  (ii) 2a and 2b use different post-cue windows, which is a protocol difference not previously stated;
  (iii) the "translation invariance" assertion I first wrote was itself wrong (a constant feature shift changes
  per-class scores) and was replaced by the correct displacement-equivalence assertion.
- fixed: A3 document written, protocol note added, test corrected.
- score after this round: see FINAL_QUALITY_GATE.md
- new blockers: none
- next round: Phase B (statistics recomputation on sleep-EDF hierarchy, Holm bookkeeping), then Phase C theory.
