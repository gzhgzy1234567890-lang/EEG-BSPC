# Round 2 review — second compression pass and the readiness gate

Version: `Revised_Manuscript.docx`, **16 pages, 6,818 body words** (excluding references, tables, captions and
declarations), 8 tables, 5 figures; supplement 33 pages.

## Executed this round

| action | result |
|---|---|
| independent-validation section compressed | 614 -> 513 words, every number and every negative result kept |
| protocol-audit section compressed | 406 -> 400, with the BCI-2a cancellation statement kept |
| mechanism evidence matrix added | new Table 8: five mechanisms x theory / real evidence / controlled evidence / cannot show |
| disclosure restored | the superseded whole-target decomposition and the margin-based check are now named again (S31, S24); deleting them in the first pass was a mistake and is recorded here |
| automated submission checker | new `submission_check.py`, 14 checks, **SUBMISSION CHECK PASS** |

## The checker (goal section 8.4)

| check | result |
|---|---|
| abstract numbers appear in the body | pass, 12 of 12 |
| tables and figures sequential | pass, Tables 1-8, Figs 1-5 |
| table elements match captions | pass |
| every `Section x.y` reference resolves | pass |
| every `Sxx` reference exists in the supplement | pass |
| five highlights, each <= 85 characters | pass, 60-77 |
| cover-letter numbers present in the manuscript | pass |
| cover letter carries the current title | pass |
| body within the 6,500-7,500 window | pass, 6,818 |
| experiment arithmetic stated | pass, 1,440 streams and 2,880 rows |
| commit `ef8c890` cited | pass |

## Scores

| dimension | max | baseline | round 1 | round 2 |
|---|---:|---:|---:|---:|
| theory boundary | 8 | 7.5 | 7.5 | 7.5 |
| online decomposition | 22 | 20.5 | 20.5 | 20.5 |
| factorial | 16 | 15.5 | 15.5 | 15.5 |
| temporal | 10 | 8.5 | 8.5 | 8.5 |
| protocol | 12 | 11.5 | 11.5 | 11.5 |
| statistics | 12 | 11.0 | 11.0 | 11.0 |
| reproducibility | 12 | 10.5 | 11.0 | **11.0** |
| structure | 8 | 6.5 | 7.5 | **8.0** |
| **total** | **100** | **91.5** | **93.0** | **93.5** |

Structure reaches the maximum because the manuscript now has the six-section form the goal asked for, 6,818 body
words, a mechanism matrix, and no duplicated section.

## Why not 96

| dimension | score | what would be needed |
|---|---:|---|
| online decomposition | 20.5 | the decomposition is exact and invariant, but it is a single corpus; a second corpus with the same analysis would close it |
| factorial | 15.5 | the controlled experiment is Gaussian; a real-data intervention would close it |
| temporal | 8.5 | the SEED sweep is archived rather than rerun here |
| statistics | 11.0 | no confirmatory replication |
| reproducibility | 11.0 | SEED archived figure still not regenerable; no third-party rerun |

None of these can be closed without new data collection, which the goal forbids.

## Decision

**Submission-ready at 93.5/100**, with the five open items above stated in the checklist rather than scored away.
