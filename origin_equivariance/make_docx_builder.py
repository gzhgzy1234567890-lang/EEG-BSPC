# -*- coding: utf-8 -*-
"""Copy the BSPC docx builder and point it at v8."""
import io

SRC = r"G:\Work_work\math\EEG\local_analysis\md2docx_bspc.py"
DST = r"G:\Work_work\math\EEG\paper_v8\md2docx_v8.py"
s = io.open(SRC, encoding="utf-8").read()
s = s.replace(r'D = r"G:\Work_work\math\EEG\local_analysis"',
              r'D = r"G:\Work_work\math\EEG\paper_v8"')
s = s.replace('SRC = os.path.join(D, "BSPC_draft_v7.md")',
              'SRC = os.path.join(D, "BSPC_draft_v8.md")')
s = s.replace('"BSPC_Manuscript_v7_with_figs.docx"', '"BSPC_Manuscript_v8_with_figs.docx"')
s = s.replace('"BSPC_Manuscript_v7.docx"', '"BSPC_Manuscript_v8.docx"')
s = s.replace('FIGD = os.path.join(D, "figs_bspc")', 'FIGD = os.path.join(D, "figs")')
s = s.replace('sys.path.insert(0, D)',
              'sys.path.insert(0, r"G:\\Work_work\\math\\EEG\\local_analysis")')
io.open(DST, "w", encoding="utf-8").write(s)
print("copied")
