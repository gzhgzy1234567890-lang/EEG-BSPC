# -*- coding: utf-8 -*-
"""Cosmetic fixes for fig2: legend and titles inside the axes."""
import io
import os
import sys
import subprocess

HERE = r"G:\Work_work\math\EEG\paper_v8"
p = os.path.join(HERE, "pv8_fig2b.py")
s = io.open(p, encoding="utf-8").read()
s = s.replace('ax[0].legend(frameon=False, loc="lower left")',
              'ax[0].legend(frameon=False, loc="upper right")')
s = s.replace('ax[0].set_title("(a) unit medians and the held-out point", loc="left")',
              'ax[0].set_title("(a) unit medians, held-out star", loc="left")')
s = s.replace('ax[1].set_title("(b) every cell; stars are held out", loc="left")',
              'ax[1].set_title("(b) every cell", loc="left")')
io.open(p, "w", encoding="utf-8").write(s)
r = subprocess.run(["python", "pv8_fig2b.py"], cwd=HERE, capture_output=True, text=True)
print((r.stdout or "").strip()[-60:])
