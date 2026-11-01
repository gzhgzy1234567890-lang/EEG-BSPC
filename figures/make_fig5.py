# -*- coding: utf-8 -*-
"""Figure 5: the three new mechanism results in one panel."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, 'results')
online = json.load(open(os.path.join(R, 'online_decomposition_anchored.json')))
fac = json.load(open(os.path.join(R, 'factorial_2x2_rich.json')))
lam = json.load(open(os.path.join(R, 'factorial_lambda_dense.json')))
sw = json.load(open(os.path.join(R, 'sleep_memory_sweep.json')))


def subj(rows, key):
    d = {}
    for r in rows:
        d.setdefault(r['subj'], {}).setdefault(r.get('night', 0), []).append(r[key])
    return np.array([np.mean([np.mean(v) for v in n.values()]) for n in d.values()])


def boot(v, n=5000, seed=20261101):
    rng = np.random.default_rng(seed)
    b = [rng.choice(v, len(v), replace=True).mean() for _ in range(n)]
    return np.percentile(b, 2.5), np.percentile(b, 97.5)


fig, ax = plt.subplots(1, 3, figsize=(13.2, 3.6))
base = subj(online, 'none')
conds = [('full', 'full'), ('mix', 'composition'), ('within', 'within-class'), ('unmatched', 'unmatched')]
vals, errs, labels = [], [], []
for key, lab in conds:
    d = subj(online, key) - base
    lo, hi = boot(d)
    vals.append(d.mean()); errs.append([d.mean() - lo, hi - d.mean()]); labels.append(lab)
ax[0].bar(range(len(vals)), vals, yerr=np.array(errs).T, capsize=3, color=['#3b6ea5', '#a5452f', '#2f7a4a', '#888888'])
ax[0].axhline(0, color='k', lw=0.8)
ax[0].set_xticks(range(len(labels))); ax[0].set_xticklabels(labels, fontsize=8)
ax[0].set_ylabel('change in balanced accuracy')
ax[0].set_title('(a) online decomposition, sleep-EDF', fontsize=9)

for prior, style, lab in ((0, '-o', 'no composition change'), (1, '-s', 'composition change')):
    for drift, col in ((0.0, '#999999'), (0.5, '#3b6ea5'), (1.0, '#a5452f')):
        xs, ys = [], []
        for l in sorted({r['lam'] for r in lam}):
            d = {}
            for r in lam:
                if r['prior'] == prior and abs(r['drift'] - drift) < 1e-9 and abs(r['lam'] - l) < 1e-9:
                    d.setdefault(r['subj'], []).append(r['delta'])
            if not d:
                continue
            v = np.array([np.mean(x) for _, x in sorted(d.items())])
            xs.append(l); ys.append(v.mean())
        if xs:
            ax[1].plot(xs, ys, style, color=col, ms=3, lw=1,
                       label='%s, drift %.1f' % ('comp' if prior else 'no comp', drift))
ax[1].axhline(0, color='k', lw=0.8)
ax[1].set_xlabel('correction strength')
ax[1].set_title('(b) strength sweep, controlled factorial', fontsize=9)
ax[1].legend(fontsize=5.5, loc='upper left')

mems = [1, 2, 3]
means, los, his = [], [], []
for mm in mems:
    d = {}
    for r in sw:
        d.setdefault(r['subj'], {}).setdefault(r['night'], []).append(r['mem%d' % mm] - r['none'])
    v = np.array([np.mean([np.mean(x) for x in n.values()]) for n in d.values()])
    lo, hi = boot(v)
    means.append(v.mean()); los.append(lo); his.append(hi)
ax[2].errorbar(mems, means, yerr=[np.array(means) - np.array(los), np.array(his) - np.array(means)],
               fmt='o-', capsize=3, color='#a5452f')
ax[2].axhline(0, color='k', lw=0.8)
ax[2].set_xticks(mems); ax[2].set_xticklabels(['1 block\n(7.5 min)', '2 blocks\n(15 min)', '3 blocks\n(22.5 min)'], fontsize=7)
ax[2].set_ylabel('change in balanced accuracy')
ax[2].set_title('(c) memory sweep, real sleep-EDF', fontsize=9)
plt.tight_layout()
for ext, dpi in (('pdf', None), ('png', 300)):
    out = os.path.join(HERE, 'Fig5_mechanisms.%s' % ext)
    plt.savefig(out, dpi=dpi if dpi else None, bbox_inches='tight')
print('figure written')
print('panel a:', ['%.4f' % v for v in vals])
print('panel c:', ['%.4f' % v for v in means])
