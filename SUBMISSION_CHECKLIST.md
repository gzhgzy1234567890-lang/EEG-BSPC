# Submission checklist — BSPC (current state)

Final state for the first submission to Biomedical Signal Processing and Control.

## Files and the item type to select in Editorial Manager

Upload the five content files individually rather than the zip, so each item type can be set:

| Editorial Manager item type | file to upload | notes |
|---|---|---|
| Manuscript | `BSPC_Candidate_V8.docx` | 21 pages, 7 tables, 5 figures embedded |
| Supplementary Material | `Supplementary_Material.pdf` | 33 pages, S1-S36; the .docx is supplied too if an editable version is requested |
| Highlights | `BSPC_Highlights_V8.docx` | 5 items, 60-79 characters each |
| Cover Letter | `Cover_Letter_BSPC.pdf` | 1 page, 480 words |
| Graphical Abstract | `Figures/Graphical_Abstract_BSPC.pdf` | 3279 x 1239 px, PNG also supplied |

Do not mark both the DOCX and the PDF as "Manuscript": that produces a duplicate in the merged PDF.

## If the system asks for the main figures as separate files

`Figures_main/` holds the five figures in document order, extracted from the submitted DOCX:
`Fig1.png` to `Fig5.png`, plus `Fig5_vector.pdf` for the mechanism figure. These are the exact images embedded
in the manuscript, so uploading them cannot introduce a version mismatch.

## Before pressing submit

- [ ] open the merged PDF and check that Tables 1-7, the five figures and the equations render;
- [ ] approve the PDF; Elsevier treats the submission as complete only after that step;
- [ ] confirm the cited commit `ef8c890` is reachable: it is an ancestor of `origin/main` and holds the anchored
      decomposition, the dense strength grid and every result file quoted in the paper. Later commits change only
      the manuscript text.

## Length: an open editorial risk, stated rather than resolved

| source | statement | status |
|---|---|---|
| official BSPC guide for authors | "Full paper ... should normally be about 5,000 words" | **could not be verified**: the ScienceDirect page returns HTTP 403 from this environment |
| third-party journal index (scraiber.com) | "Full paper: word limit 5,000 words; abstract 250 words" | retrieved, secondary source |

The manuscript is 11,918 words including references and a 247-word abstract. If the 5,000-word figure is a hard limit
rather than a guideline, the manuscript is over it. It has not been cut to fit, because the remaining bulk is
evidence rather than padding; the length is reported rather than declared compliant.

## Consistency evidence

```
FREEZE CHECK PASS   (12 files, sha256 verified)
CONSISTENCY PASS    (abstract numbers present in body; claim locations resolve; freeze rows match)
TABLE TRACEABILITY PASS (7 of 7 rows)
PROTOCOL INTEGRITY PASS (5 tests)
```
