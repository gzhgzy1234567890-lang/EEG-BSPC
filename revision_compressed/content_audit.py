# -*- coding: utf-8 -*-
"""Extend the content audit with the new checks and run everything."""
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
stext = ' '.join(p.text for p in s.paragraphs)
checks = []
checks.append(('no "Tables 4 and 5" misreference', 'Tables 4 and 5' not in text))
checks.append(('no duplicate "never adds them"', text.count('never adds them') <= 1))
checks.append(('certificate uses uncorrected scores', 'both scores on the left are uncorrected' in text))
checks.append(('null-space wording', 'not in the null space of F W' in text))
checks.append(('abstract names three components', 'composition, within-class and unmatched-class' in text))
checks.append(('no absolute claims about the optimum',
               not any(x in text for x in ('exactly when a composition', 'only when composition'))))
checks.append(('2.3 qualifies the two-term split', 'whenever the source and the target support the same classes' in text))
checks.append(('4.4 does not infer memory from the strength grid',
               'varies the correction strength, not the memory' in text))
checks.append(('Discussion separates transductive from past-only',
               'uses only completed blocks' in text and 'centres the target on the whole target session' in text))
checks.append(('S37 holds the four proofs', 'S37. Proofs of Propositions 1-4' in stext))
checks.append(('S37 P1 states the shifted correction correctly',
               'the extra +c is again removed by the shifted intercepts' in stext))
checks.append(('within-session reference not called an upper bound', 'upper bound' not in text))
checks.append(('dataset count clarified', 'A sixth, SEED-IV, is used only' in text))
checks.append(('main equations numbered 1-4', all(('(%d)' % i) in text for i in (1, 2, 3, 4))))
checks.append(('no dangling (7)-(9) in the manuscript', not any(('(%d)' % i) in text for i in (7, 8, 9))))
checks.append(('supplement has no dangling Equation (n)', not any(('Equation (%d)' % i) in stext for i in (2, 3, 4, 5))))
checks.append(('supplement tables renumbered', 'Table S9.' in stext and 'Table S10.' in stext))
s_arr = np.array([0.0, 1.0]); d = np.array([0.0, 2.0])
kstar = int(np.argmax(s_arr))
correct = [s_arr[kstar] - s_arr[j] - (d[kstar] - d[j]) for j in range(2) if j != kstar]
flips = int(np.argmax(s_arr - d)) != kstar
checks.append(('counter-example: corrected formula flags the flip', correct[0] <= 0 and flips))
for name, ok in checks:
    print(('PASS ' if ok else 'FAIL ') + name)
print('CONTENT AUDIT', 'PASS' if all(c[1] for c in checks) else 'FAIL')
