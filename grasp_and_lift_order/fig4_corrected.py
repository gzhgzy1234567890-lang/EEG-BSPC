# -*- coding: utf-8 -*-
"""Rebuild Fig. 4 with the acquisition-order grasp-and-lift curve."""
import csv, json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
LAMS = [0.0, 0.25, 0.50, 0.75, 1.00]
rows = list(csv.DictReader(open('G:/Work_work/math/EEG/paper_v8/results/master_cells.csv')))
cols = ['ba0.00', 'ba0.25', 'ba0.50', 'ba0.75', 'ba1.00']
curves = {}
for ds in ('gal', 'seed', '2b', '2a', 'ner'):
    sub = {}
    for r in rows:
        if r['ds'] != ds:
            continue
        sub.setdefault(r['subj'], []).append([float(r[c]) for c in cols])
    curves[ds] = np.array([np.mean(v, axis=0) for v in sub.values()])
gj = json.load(open('G:/Work_work/math/EEG/paper_v8/results/gal_order_curves.json'))
per = {}
for c in gj['time']['cells']:
    per.setdefault(c[0], []).append(c[3:])
curves['gal'] = np.array([np.mean(v, axis=0) for v in per.values()])
names = {'gal': 'grasp-and-lift (acquisition order)', 'seed': 'SEED', '2b': 'BCI-2b', '2a': 'BCI-2a', 'ner': 'NER2015'}
colors = {'gal': '#1e8449', 'seed': '#c0392b', '2b': '#2471a3', '2a': '#7d3c98', 'ner': '#7f8c8d'}
fig, ax = plt.subplots(1, 2, figsize=(10.0, 3.4))
lam10 = np.array(LAMS) * 100
for ds in ('gal', 'seed', '2b', '2a', 'ner'):
    m = curves[ds].mean(0)
    ax[0].plot(lam10, m, marker='o', ms=3, color=colors[ds], label=names[ds])
    ax[1].plot(lam10, m - m[0], marker='o', ms=3, color=colors[ds], label=names[ds])
ax[0].set_xlabel('correction strength (per cent of full)')
ax[0].set_ylabel('balanced accuracy')
ax[1].set_xlabel('correction strength (per cent of full)')
ax[1].set_ylabel('change in balanced accuracy')
ax[1].axhline(0, color='k', lw=0.6, ls=':')
ax[0].legend(fontsize=7, frameon=False)
ax[1].legend(fontsize=7, frameon=False)
for a, tag in zip(ax, ('(a)', '(b)')):
    a.set_title(tag, loc='left', fontsize=9)
    a.tick_params(labelsize=7)
fig.tight_layout()
out = 'G:/Work_work/math/EEG/paper_v8/figs/fig4_corrected.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=300)
print('saved', out)
for ds in ('gal', 'seed', '2b', '2a', 'ner'):
    m = curves[ds].mean(0)
    print('%-4s' % ds, np.round(m, 4), 'delta %+.4f' % (m[-1] - m[0]))