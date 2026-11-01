# -*- coding: utf-8 -*-
"""Independent checks the automated script cannot do: cross-reference content and certificate arithmetic."""
import docx, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
M = r'G:\Work_work\math\EEG\submit\Revised_Manuscript.docx'
m = docx.Document(M)
text = ' '.join(p.text for p in m.paragraphs)
checks = []
checks.append(('no "Tables 4 and 5" misreference', 'Tables 4 and 5' not in text))
checks.append(('no duplicate "never adds them"', text.count('never adds them') <= 1))
checks.append(('certificate uses uncorrected scores', 'both scores on the left are uncorrected' in text or
               'the two scores on the left of that inequality are both uncorrected' in text))
checks.append(('null-space wording', 'not in the null space of F W' in text))
checks.append(('abstract names three components', 'composition, within-class and unmatched-class' in text))
bad_absolutes = ['exactly when a composition', 'exactly when the composition', 'only when composition']
checks.append(('no absolute claims about the optimum', not any(x in text for x in bad_absolutes)))
# certificate arithmetic on the reviewer's counter-example
import numpy as np
s = np.array([0.0, 1.0]); d = np.array([0.0, 2.0])
kstar = int(np.argmax(s))
mixed = [s[kstar] - (s[j] - d[j]) - (d[kstar] - d[j]) for j in range(2) if j != kstar]
correct = [s[kstar] - s[j] - (d[kstar] - d[j]) for j in range(2) if j != kstar]
corrected = s - d
flips = int(np.argmax(corrected)) != kstar
checks.append(('counter-example: corrected formula is sound', correct[0] <= 0 and flips))
for name, ok in checks:
    print(('PASS ' if ok else 'FAIL ') + name)
print('CONTENT AUDIT', 'PASS' if all(c[1] for c in checks) else 'FAIL')