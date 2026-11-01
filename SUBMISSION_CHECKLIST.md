# Submission checklist — BSPC (current state)

## Files to upload

| System field | File | Status |
|---|---|---|
| Manuscript | BSPC_Candidate_V8.docx / .pdf | 20 pages, **11593 words (Word count, references included)**, 9 tables, 4 figures; abstract, keywords, CRediT, competing interests, data availability, AI-use declaration |
| Supplementary material | Supplementary_Material.docx / .pdf | 27 pages, **S1-S33** |
| Highlights | BSPC_Highlights_V8.docx / .pdf | five items, each under 85 characters |
| Graphical abstract | Figures/Graphical_Abstract_BSPC.png / .pdf | 3279 x 1239 px |
| Cover letter | Cover_Letter_BSPC.docx / .pdf | title, case, declarations |

No reviewer-response letter is included: this is a first submission.

## Archive used in the same run

The full audit archive (BSPC_Submission_Package_final.zip, 38 entries) keeps the protocols, the deviations and
the superseded records, each labelled as such. Only the files above are for the journal.

## Checks that pass

- numbers: `python sleep_edf/check_numbers.py` -> CHECK PASS;
- documents: FREEZE_RECORD.md lists ten files with sizes and SHA-256; FREEZE CHECK PASS;
- commit: every current document cites `9c39cee`;
- archives: submission 12 entries, audit 38 entries, 0 hash mismatches.

## Decisions for the authors

1. **Article type and length.** 11593 words (Word count, references included) against the ~5,000 that third-party summaries mention; the official
   Guide could not be retrieved from this environment. If a limit is enforced, cut Section 4.2.1 and the
   estimator table rather than results.
2. **Graphical abstract format.** TIFF or EPS if the system demands it; the figure regenerates from
   `figures/ga_corrected.py`.
3. **Relation to the earlier alignment manuscript.** The paragraph is written in neutral terms; its submission
   status is an author fact and must be confirmed before upload.
4. **Suggested reviewers.** Three to five names outside the authors' institutions, not prepared here.
5. **ORCID and funding.** Acknowledgements state that no specific grant was received.
