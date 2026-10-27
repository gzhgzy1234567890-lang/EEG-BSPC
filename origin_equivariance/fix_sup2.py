# -*- coding: utf-8 -*-
"""Restore the ^...^ superscript notation (no escapes) and rebuild."""
import io
import os
import subprocess

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()

old = """Zihao Gong$^{a,1}$, Jiran Li$^{b,1}$, Ke Huo$^{a}$, Yubin Han$^{c}$, Guangyu Shi$^{a}$, Yongqiang Xie$^{a,*}$

$^{a}$ School of Mechano-Electronic Engineering, Xidian University, Xi'an 710071, China

$^{b}$ School of Humanities and Social Sciences, Beijing Forestry University, Beijing 100083, China

$^{c}$ School of Life Science and Technology, Xidian University, Xi'an 710071, China

$^{1}$ These authors contributed equally to this work.

$^{*}$ Corresponding author. E-mail address: yqxie@xidian.edu.cn (Y. Xie)."""

new = """Zihao Gong ^a,1^, Jiran Li ^b,1^, Ke Huo ^a^, Yubin Han ^c^, Guangyu Shi ^a^, Yongqiang Xie ^a,*^

^a^ School of Mechano-Electronic Engineering, Xidian University, Xi'an 710071, China

^b^ School of Humanities and Social Sciences, Beijing Forestry University, Beijing 100083, China

^c^ School of Life Science and Technology, Xidian University, Xi'an 710071, China

^1^ These authors contributed equally to this work.

^*^ Corresponding author. E-mail address: yqxie@xidian.edu.cn (Y. Xie)."""

if old not in s:
    print("MISS")
s = s.replace(old, new)
io.open(P, "w", encoding="utf-8").write(s)
for cmd in (["python", "prep_docx2.py"], ["python", "md2docx_v8.py", "--with-figs"]):
    r = subprocess.run(cmd, cwd=os.path.dirname(P), capture_output=True, text=True)
    print(cmd[-1], (r.stdout or "").strip()[-80:])
