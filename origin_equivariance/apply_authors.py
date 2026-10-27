# -*- coding: utf-8 -*-
"""Fill in the author block, affiliations, CRediT, funding and repository URL."""
import io

P = r"G:\Work_work\math\EEG\paper_v8\BSPC_draft_v8.md"
s = io.open(P, encoding="utf-8").read()
n0 = len(s)

URL = "https://github.com/gzhgzy1234567890-lang/EEG-BSPC/tree/main/origin_equivariance"

old_head = """Author One^a^, Author Two^b^

^a^ Affiliation, City, Country

^b^ Affiliation, City, Country

*Corresponding author: name@institution.edu*"""

new_head = """Zihao Gong ^a,1^, Jiran Li ^b,1^, Ke Huo ^a^, Yubin Han ^c^, Guangyu Shi ^a^, Yongqiang Xie ^a,\\*

^a^ School of Mechano-Electronic Engineering, Xidian University, Xi'an 710071, China

^b^ School of Humanities and Social Sciences, Beijing Forestry University, Beijing 100083, China

^c^ School of Life Science and Technology, Xidian University, Xi'an 710071, China

^1^ These authors contributed equally to this work.

\\* Corresponding author. E-mail address: yqxie@xidian.edu.cn (Y. Xie).

E-mail addresses: andy.zihao.gong@gmail.com (Z. Gong), dsx54188dsx@163.com (J. Li), huoke@stu.xidian.edu.cn (K. Huo), 2044037857@qq.com (Y. Han), 2793218576@qq.com (G. Shi), yqxie@xidian.edu.cn (Y. Xie)."""

old_credit = """**Author One:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Writing – original draft, Writing – review & editing, Visualization. **Author Two:** Conceptualization, Supervision, Writing – review & editing, Funding acquisition."""

new_credit = """**Zihao Gong:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Writing – original draft, Visualization. **Jiran Li:** Conceptualization, Methodology, Validation, Writing – review & editing. **Ke Huo:** Software, Data curation, Investigation. **Yubin Han:** Formal analysis, Validation, Visualization. **Guangyu Shi:** Data curation, Resources, Validation. **Yongqiang Xie:** Conceptualization, Supervision, Writing – review & editing, Project administration."""

old_ack = """[Funding sources to be inserted. The present version reports no specific grant from funding agencies in the public, commercial, or not-for-profit sectors.]"""

new_ack = """This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."""

old_data = """BCI Competition IV datasets 2a and 2b are available from the competition organisers. SEED is available from the BCMI Laboratory, Shanghai Jiao Tong University, on request for academic use; the present study used the differential-entropy features distributed with that release, unmodified. NER2015 and grasp-and-lift are Kaggle competition datasets and are publicly available. Code, cached features, the origin-sweep and streaming scripts, and the script that regenerates every number and figure are archived at the repository associated with this manuscript, with a commit hash pinned to the reported numbers."""

new_data = """BCI Competition IV datasets 2a and 2b are available from the competition organisers. SEED is available from the BCMI Laboratory, Shanghai Jiao Tong University, on request for academic use; the present study used the differential-entropy features distributed with that release, unmodified. NER2015 and grasp-and-lift are Kaggle competition datasets and are publicly available. The analysis code, the feature-cache schema and the plain-text output of every number reported in this paper are archived at %s (folder `origin_equivariance`), which is the version of record for the code.""" % URL

for a, b in ((old_head, new_head), (old_credit, new_credit),
             (old_ack, new_ack), (old_data, new_data)):
    if a not in s:
        print("MISS:", a[:60].replace("\n", " "))
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("written", n0, "->", len(s))
