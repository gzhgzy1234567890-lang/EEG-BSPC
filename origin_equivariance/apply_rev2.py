# -*- coding: utf-8 -*-
"""Trim the abstract to 250 words and add the missing figure captions."""
import io
import re

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()

NEW_AB = """Removing a session mean is the standard first step in cross-session EEG decoding, and two operations circulate under that description: centring both sessions, or centring one. We settle what the choice is. The two-sided form is the one that is equivariant to a change of the coordinate origin, and we characterize when two corrections are prediction-equivalent: exactly when they differ by a vector in the null space of the classifier's weights. Any other correction makes the result depend on a convention the pipeline does not report, and five elaborations — projected, halved, low-ranked, standardised and label-fitted — do not improve on the mean correction.

We then measure when the convention matters, separating risk from benefit. The one-sided form displaces the decision function by the projection of the target mean onto the fitted weights, so its damage is governed by two measurable quantities: the distance of the feature origin from the data centre, computable from the source session alone, and the displacement in units of the classifier's score spread. On 845 session pairs from five public datasets (BCI-IV-2a, 2b, SEED, NER2015, grasp-and-lift; 11 feature units; three classifier families) an origin sweep leaves the equivariant pipelines unchanged by 0.000 in balanced accuracy over a 250-fold range and drives the one-sided one to exact chance. The source-only statistic orders the damage across units (Spearman -0.76, permutation p = 0.009), and the displacement orders it across classifier settings (-0.78). The benefit of the correction over doing nothing is not ordered by the same statistic, and we report that as a negative result. A label-free certificate identifies collapse exactly (124 of 124 cells) and separates it from chance-level accuracy, which on an imbalanced target is usually something else.
"""

ab_old = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(0)
s = s.replace(ab_old, "## Abstract\n\n" + NEW_AB + "\n**Keywords")

# figure captions
s = s.replace(
    "The gain of `mean` over `none` is +0.0463 on 2a",
    "**Fig. 3.** (a) Balanced accuracy of the three pipelines by dataset; (b) the gain of the two-sided over the uncorrected pipeline, one point per subject, with the box showing the median and quartiles. The two datasets with an origin offset are the two in which the correction recovers most of the gap; the two without one are the two in which it recovers least.\n\nThe gain of `mean` over `none` is +0.0463 on 2a")

s = s.replace(
    "**What the screen does not do.**",
    "**Fig. 2.** (a) The screen at unit level: origin distance of the source session against the penalty of the one-sided pipeline, one point per dataset-by-representation unit, area proportional to the number of cells; (b) the same relation per cell; (c) the origin distance against the induced displacement, which it proxies.\n\n**What the screen does not do.**")

io.open(P, "w", encoding="utf-8").write(s)

ab = re.search(r"## Abstract\s*(.*?)\n\*\*Keywords", s, re.S).group(1)
w = re.findall(r"[A-Za-z][A-Za-z\-']*", ab)
print("abstract words:", len(w))
print("fig captions:", re.findall(r"^\*\*Fig\. (\d)", s, re.M))
