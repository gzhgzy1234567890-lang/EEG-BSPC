# Submission checklist — BSPC (current state)

Final state for the first submission to Biomedical Signal Processing and Control.

## Files and the item type to select in Editorial Manager

Upload the five content files individually rather than the zip, so each item type can be set:

| Editorial Manager item type | file to upload | notes |
|---|---|---|
| Manuscript | `BSPC_Candidate_V8.docx` | 21 pages, 9 tables, 4 embedded figures |
| Supplementary Material | `Supplementary_Material.pdf` | 27 pages, S1-S33; the .docx is supplied too if an editable version is requested |
| Highlights | `BSPC_Highlights_V8.docx` | 5 items, 60-79 characters each |
| Cover Letter | `Cover_Letter_BSPC.docx` | 1 page, first-submission wording |
| Graphical Abstract | `Graphical_Abstract_BSPC.pdf` | 3279 x 1239 px, PNG also supplied |

Do not mark both the DOCX and the PDF as "Manuscript": that produces a duplicate in the merged PDF.

If the system requires the four main figures as separate files, they are embedded in the manuscript only and must be
exported separately; the graphical abstract is already a separate file.

## Before pressing submit

- [ ] open the merged PDF and check that Tables 1-9, the four figures and the equations render, and that Table 9 is
      not split across pages (it is held together by "keep with next" on every row);
- [ ] approve the PDF; Elsevier treats the submission as complete only after that step;
- [ ] confirm the cited commit `871546b` is reachable (it holds all analysis code and results).

## Length: an open editorial risk, stated rather than resolved

| source | statement | status |
|---|---|---|
| official BSPC guide for authors | "Full paper ... should normally be about 5,000 words" | **could not be verified**: the ScienceDirect page returns HTTP 403 from this environment |
| third-party journal index (scraiber.com) | "Full paper: word limit 5,000 words; abstract 250 words" | retrieved, secondary source |

The manuscript is 11595 words including references (about 10,300 excluding them) and a 219-word abstract. If the
5,000-word figure is a hard limit rather than a guideline, the manuscript is over it. It was **not** cut down here:
halving it would require moving whole result sections into the supplement and re-checking every cross-reference,
which is a restructuring decision for the authors, not a formatting fix. The length is reported to the editors in
the cover letter as it stands.

## Consistency evidence

```
FREEZE CHECK PASS   (12 files, sha256 verified)
CONSISTENCY PASS    (abstract numbers present in body; claim locations resolve; freeze rows match)
```
