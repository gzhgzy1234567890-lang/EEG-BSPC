# -*- coding: utf-8 -*-
"""Content audit with the fifth-review checks."""
import docx, os, sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
def resolve(name):
    for base in (HERE, os.path.join(HERE, '..'), os.path.dirname(HERE)):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return os.path.abspath(p)
    return None
M = resolve('Revised_Manuscript.docx'); S = resolve('Revised_Supplementary.docx')
if M is None or S is None:
    print('CANNOT LOCATE the manuscript or the supplement - run from the unzipped package')
    sys.exit(2)
m = docx.Document(M); s = docx.Document(S)
text = ' '.join(p.text for p in m.paragraphs)
text += ' ' + ' '.join(c.text for t in m.tables for r in t.rows for c in r.cells)
stext = ' '.join(p.text for p in s.paragraphs)
stext += ' ' + ' '.join(c.text for t in s.tables for r in t.rows for c in r.cells)
abstract = m.paragraphs[8].text
checks = []
checks.append(('no "Tables 4 and 5" misreference', 'Tables 4 and 5' not in text))
checks.append(('no duplicate "never adds them"', text.count('never adds them') <= 1))
checks.append(('certificate uses uncorrected scores', 'both scores on the left are uncorrected' in text))
checks.append(('null-space wording', 'not in the null space of F W' in text))
checks.append(('abstract names three components', 'composition, within-class and unmatched-class' in abstract))
checks.append(('no absolute claims about the optimum',
               not any(x in text for x in ('exactly when a composition', 'only when composition'))))
checks.append(('2.3 qualifies the two-term split', 'whenever the source and the target support the same classes' in text))
checks.append(('4.4 does not infer memory from the strength grid',
               'varies the correction strength, not the memory' in text))
checks.append(('Discussion separates transductive from past-only',
               'uses only completed blocks' in text and 'centres the target on the whole target session' in text))
checks.append(('S37 holds the four proofs', 'S37. Proofs of Propositions 1-4' in stext))
checks.append(('S37 setting matches Table 1', 'mean (fit on X_A, apply to X_B - mu_B + mu_A)' in stext))
checks.append(('within-session reference not called an upper bound', 'upper bound' not in text))
checks.append(('dataset count clarified', 'A sixth, SEED-IV, is used only' in text))
checks.append(('main equations numbered 1-4', all(('(%d)' % i) in text for i in (1, 2, 3, 4))))
checks.append(('no dangling (7)-(9) anywhere', not any(('(%d)' % i) in text or ('(%d)' % i) in stext for i in (7, 8, 9))))
checks.append(('supplement has no dangling Equation (n)', not any(('Equation (%d)' % i) in stext for i in (2, 3, 4, 5))))
checks.append(('supplement tables renumbered', 'Table S9.' in stext and 'Table S10.' in stext))
checks.append(('Table 4 header cites Eq. 4 not Eq. 9', 'variance-ratio (Eq. 4)' in text))
checks.append(('Methods AI paragraph exists', 'Implementation and AI assistance.' in text))
checks.append(('declaration points at Section 3', 'paragraph of Section 3' in text))
checks.append(('Table 8 memory row no longer claims a sufficient condition',
               'depends on the decision geometry' in text and 'stable over the memory window and the window spans' not in text))
checks.append(('Discussion does not claim one shared curve',
               'different points of the same curve' not in text))
checks.append(('abstract separates the two BCI-2a protocols',
               'target-informed alignment on BCI-2a' in abstract and '0.034 on BCI-2b' in abstract))
checks.append(('S9 caption points at Table S10', 'which is Table S10' in stext))
checks.append(('S37 says at most K', 'whose dimension is at most K' in stext))
checks.append(('reference 25 has the published title',
               'Test-time adaptation for EEG foundation models: a systematic study under real-world distribution '
               'shifts' in text))
s_arr = np.array([0.0, 1.0]); d = np.array([0.0, 2.0])
kstar = int(np.argmax(s_arr))
correct = [s_arr[kstar] - s_arr[j] - (d[kstar] - d[j]) for j in range(2) if j != kstar]
flips = int(np.argmax(s_arr - d)) != kstar
checks.append(('counter-example: corrected formula flags the flip', correct[0] <= 0 and flips))
for name, ok in checks:
    print(('PASS ' if ok else 'FAIL ') + name)
print('CONTENT AUDIT', 'PASS' if all(c[1] for c in checks) else 'FAIL')
