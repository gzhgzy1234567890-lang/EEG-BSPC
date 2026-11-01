# -*- coding: utf-8 -*-
"""Submission-only archive: the files an editor needs, nothing else."""
import hashlib, os, sys, zipfile
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SUB = r'G:\Work_work\math\EEG\submit'
OUT = r'G:\Work_work\math\EEG\BSPC_Submission_Package_submit.zip'
FILES = ['BSPC_Candidate_V8.docx', 'BSPC_Candidate_V8.pdf', 'Supplementary_Material.docx', 'Supplementary_Material.pdf',
         'BSPC_Highlights_V8.docx', 'BSPC_Highlights_V8.pdf', 'Cover_Letter_BSPC.docx', 'Cover_Letter_BSPC.pdf',
         'Figures/Graphical_Abstract_BSPC.png', 'Figures/Graphical_Abstract_BSPC.pdf']
README = '''# BSPC submission package (files to upload)


This archive contains only the files an editor or reviewer needs. The audit trail (protocols, superseded records,

test logs) is kept in a separate archive and is not part of the submission.


| file | field in Editorial Manager |

|---|---|

| BSPC_Candidate_V8.docx / .pdf | manuscript |

| Supplementary_Material.docx / .pdf | supplementary material |

| BSPC_Highlights_V8.docx / .pdf | highlights (5 items, each <= 85 characters) |

| Cover_Letter_BSPC.docx / .pdf | cover letter |

| Figures/Graphical_Abstract_BSPC.png / .pdf | graphical abstract (3279 x 1239 px) |



Code and result files: https://github.com/gzhgzy1234567890-lang/EEG-BSPC at commit 7cce41a.

`python sleep_edf/check_numbers.py` in that repository recomputes and asserts every number reported in the

paper from the archived result files (CHECK PASS).

'''
os.makedirs(os.path.join(SUB, '_submit_readme'), exist_ok=True)
readme_path = os.path.join(SUB, '_submit_readme', 'README.md')
open(readme_path, 'w', encoding='utf-8').write(README)
rows = []
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(readme_path, 'README.md')
    for f in FILES:
        p = os.path.join(SUB, f.replace('/', '\\'))
        z.write(p, f)
        b = open(p, 'rb').read()
        rows.append((f, len(b), hashlib.sha256(b).hexdigest()[:16]))
    man = ['# Manifest', '', '| file | bytes | sha256 (first 16) |', '|---|---|---|']
    for f, n, h in rows:
        man.append('| %s | %d | %s |' % (f, n, h))
    z.writestr('MANIFEST.md', '\n'.join(man) + '\n')
digest = hashlib.sha256(open(OUT, 'rb').read()).hexdigest()
print('entries', len(rows) + 2)
print('zip', OUT)
print('sha256', digest)
print('bytes', os.path.getsize(OUT))