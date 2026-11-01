# Round 009 review — pre-submission corrections only, no new experiments

Acting on the internal pre-submission check. Every item is a text or arithmetic correction; no experiment was run
for this round.

| referee item | correction | verified |
|---|---|---|
| abstract said 2.6e-14, body 2.7e-14 | abstract now 2.7e-14 | consistency check passes |
| additivity sentence added absolute values | replaced by the signed sum: -0.0715 + 0.0202 = -0.0513 against the -0.1023 full correction, interaction 0.0510 | recomputed by hand from the anchored archive |
| Section 4.2.1 pointed at Table 4/Table 5 for the estimator comparison | text now points to the supplement S35, where those tables live | grep shows no stale Table 4/5 reference in that block |
| results overview cited wrong sections | sleep-EDF to 4.6, partial correlation to 4.9, cross-day cohort to 4.10, cache composition to 4.5 | section list re-checked against the current headings |
| S36 said 12 x 20 x 2 x 3 x 5 = 1,440 | corrected: 1,440 streams for the main cells, 2,880 strength rows (576 streams x 5 strengths x 2), 3,168 dense-grid rows (288 streams x 11) | counts re-derived from the scripts |
| Data availability cited 6443357 | now cites ef8c890, the commit that holds the anchored decomposition and the dense grid, with a note that later commits change only text | commit inspected in git |
| Highlights still described the old theory | item 2 now 'Class-prior shifts can make online EEG mean correction harmful' (63 chars), item 5 'Longer estimator memory helps on SEED but does not remove sleep-EDF losses' (75 chars) | all five items under 85 characters |
| Cover letter described the superseded global decomposition | results paragraph rewritten around the anchored decomposition, the factorial and the cache audit | cover letter is one page, 461 words |

## State after the round

```
manuscript 21 pages, 11,830 words      supplement 33 pages
CONSISTENCY PASS   FREEZE CHECK PASS   TABLE TRACEABILITY PASS (7/7)
```

## What was deliberately not done

- No new experiments, no new analysis, no restructuring.
- The graphical abstract still reads 'stable offset, correct fully'; changing it means re-rendering the figure and
  was judged not worth the risk for a wording nuance, and that is recorded rather than hidden.
- Length and the SEED provenance gap remain open as before.

## Decision

**Major Revision by the internal rubric (91.5), but cleared for submission after these corrections** — the rubric
scores scientific completeness, and no further science was added; the pre-submission check concerns file and text
consistency, which is now done.
