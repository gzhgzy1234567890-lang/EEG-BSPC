# Submission checklist — BSPC (current state)

Final state for the first submission to Biomedical Signal Processing and Control.

## Files and the item type to select in Editorial Manager

Upload the five content files individually rather than the zip, so each item type can be set:

| Editorial Manager item type | file to upload | notes |
|---|---|---|
| Manuscript | `BSPC_Candidate_V8.docx` | 20 pages, 9 tables, 4 embedded figures |
| Supplementary Material | `Supplementary_Material.pdf` | 27 pages, S1-S33; the .docx is supplied too if the system asks for an editable version |
| Highlights | `BSPC_Highlights_V8.docx` | 5 items, 60-79 characters each |
| Cover Letter | `Cover_Letter_BSPC.docx` | 1 page, first-submission wording |
| Graphical Abstract | `Graphical_Abstract_BSPC.pdf` | 3279 x 1239 px, PNG also supplied |

Do not mark both the DOCX and the PDF as "Manuscript": that produces a duplicate in the merged PDF.

If the system requires the four main figures as separate files, they are embedded in the manuscript only and must be
exported separately; the graphical abstract is already a separate file.

## Before pressing submit

- [ ] open the merged PDF the system generates and check that Tables 1-9, the four figures and the equations render;
- [ ] approve the PDF; Elsevier treats the submission as complete only after that step;
- [ ] confirm the cited commit `871546b` is reachable (it holds all analysis code and results).

## Consistency evidence

```
FREEZE CHECK PASS   (12 files, sha256 verified)
CONSISTENCY PASS    (abstract numbers present in body; claim locations resolve; freeze rows match)
```

## Word count

The manuscript is 11,593 words including references. No hard limit was verified from the BSPC guide for authors in
this environment, so the length is reported rather than declared compliant.
