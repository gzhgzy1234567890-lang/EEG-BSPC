# -*- coding: utf-8 -*-
"""Retitle and refresh the abstract so it matches the new evidence."""
import docx, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
M = 'G:/Work_work/math/EEG/submit/BSPC_Candidate_V8.docx'
m = docx.Document(M)
TITLE = ('Mean correction in EEG decoding: decision geometry, temporal memory, and failure modes')
p = m.paragraphs[0]
runs = [r for r in p.runs if r.text]
runs[0].text = TITLE
for r in runs[1:]:
    r.text = ''
ABSTRACT = (
 'Mean correction is a routine first step in cross-session EEG decoding, and whether it helps or hurts is usually '
 'assumed rather than checked. For a fixed affine decoder only the projection of a displacement onto the centred '
 'classifier weights can change a decision, and in a symmetric two-class model the balanced-optimal threshold does '
 'not depend on the target class proportions, so a composition-only correction must hurt while a correction that '
 'removes a real drift can help; the optimal weight is the projection of the drift onto the axis that separates the '
 'two displacements. Empirically, full-strength past-only correction gains 0.214 on SEED and 0.071 on BCI-2a '
 '(exploratory; 0.034 on BCI-2b with an endpoint fixed in advance) and loses 0.102 on sleep-EDF, negative in all 32 '
 'subjects. On the estimator that is actually used, the displacement splits exactly (reconstruction error 2.6e-14) '
 'into a composition term and a within-class term; removing only the composition term costs 0.126 and removing only '
 'the within-class term gains 0.020. A controlled factorial on the real feature statistics separates the two factors: '
 'a composition change alone raises the cost from 0.003 to 0.010, a drift alone gains 0.017 to 0.060, and the sign '
 'follows whichever displacement is larger. Memory sets the scale at which the sign flips, at about one film on SEED '
 'and one to three blocks in sleep-EDF. A two-factor audit finds the filter and alignment choices acting in opposite '
 'directions, and a grasp-and-lift negative case did not survive an audit of its cache order.'
)
a = m.paragraphs[8]
aruns = [r for r in a.runs if r.text]
aruns[0].text = ABSTRACT
for r in aruns[1:]:
    r.text = ''
m.save(M)
print('title and abstract updated; abstract words', len(ABSTRACT.split()))
