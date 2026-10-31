# -*- coding: utf-8 -*-
"""Graphical abstract v2: corrected three outcomes, tighter layout."""
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

fig = plt.figure(figsize=(10.93, 4.13), dpi=300)
fig.patch.set_facecolor('white')

ax = fig.add_axes([0.02, 0.02, 0.30, 0.94])
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-0.34, 0.38)
ax.axis('off')
ax.text(-1.42, 0.365, 'Same correction, three outcomes', fontsize=12.5, ha='left', va='top')
ax.plot([-1.30, 1.30], [0, 0], color='black', lw=1.1)
bars = [(-0.80, 0.2140, '#3d7fb5', 'SEED', '+0.214', '15/15 subjects'),
        (0.00, -0.1023, '#c0504d', 'sleep-EDF', '-0.102', '32/32 subjects'),
        (0.80, 0.0014, '#8c8c8c', 'grasp-and-lift', '+0.001', '6/12 subjects')]
for x, h, c, name, val, sub in bars:
    ax.add_patch(plt.Rectangle((x - 0.17, min(h, 0)), 0.34, abs(h), color=c, lw=0))
    if h >= 0:
        ax.text(x, h + 0.015, val, fontsize=11.5, ha='center', va='bottom')
    else:
        ax.text(x, h - 0.015, val, fontsize=11.5, ha='center', va='top')
    ax.text(x, -0.215, name, fontsize=8.5, ha='center', va='top')
    ax.text(x, -0.262, sub, fontsize=8, ha='center', va='top', color='0.35')
ax.plot([0.80], [0.0014], marker='D', ms=5, color='#8c8c8c')
ax.text(0.80, -0.195, 'sorted cache: -0.108', fontsize=7.5, color='0.45', ha='center', va='top')
ax.annotate('', xy=(0.80, -0.012), xytext=(0.80, -0.085),
            arrowprops=dict(arrowstyle='->', color='0.6', lw=0.8, linestyle=':'))

def box(x, y, w, h, fc, ec):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.006,rounding_size=0.010',
                                      transform=fig.transFigure, facecolor=fc, edgecolor=ec, lw=1.0))
box(0.350, 0.545, 0.295, 0.395, '#f4f5f7', '#c8ccd2')
fig.text(0.4975, 0.925, 'Decision geometry', fontsize=12.5, ha='center', va='top')
fig.text(0.4975, 0.862, 'which shift can change a decision?', fontsize=9.5, ha='center', va='top')
fig.text(0.4975, 0.790, r'$d_{<t} = PW(\hat{\mu}_{<t} - \mu_A)$', fontsize=15, ha='center', va='center')
fig.text(0.4975, 0.665, 'estimate from completed trials only', fontsize=9, ha='center', va='center', style='italic')
box(0.350, 0.065, 0.295, 0.415, '#eaf1f8', '#c8ccd2')
fig.text(0.4975, 0.405, 'only the projection onto the', fontsize=10, ha='center', va='center')
fig.text(0.4975, 0.340, 'centred weights changes scores', fontsize=10, ha='center', va='center')
fig.text(0.4975, 0.160, 'orthogonal shift: no effect', fontsize=9.5, ha='center', va='center', color='0.35')

fig.text(0.845, 0.925, 'Four failure regimes', fontsize=12.5, ha='center', va='top')
regimes = [('stable offset', 'correct fully', '#2e7d32'),
           ('gradual drift', 'long memory lags', '#c77700'),
           ('step change', 'short window', '#c77700'),
           ('class-prior change', 'correction can hurt', '#b03a2e')]
y0 = 0.845
for i, (name, note, col) in enumerate(regimes):
    yy = y0 - i * 0.192
    box(0.702, yy - 0.140, 0.283, 0.140, 'white', col)
    fig.text(0.720, yy - 0.070, name, fontsize=9.5, ha='left', va='center')
    fig.text(0.966, yy - 0.070, note, fontsize=8.5, ha='right', va='center', color=col)

out = r'G:\Work_work\math\EEG\submit\Figures\Graphical_Abstract_BSPC.png'
fig.savefig(out, dpi=300, facecolor='white')
fig.savefig(out.replace('.png', '.pdf'), facecolor='white')
print('pdf written')
print('written')