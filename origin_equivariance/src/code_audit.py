# -*- coding: utf-8 -*-
"""Fetch a handful of public EEG decoding files and report how each one
references the session mean.

Only the lines that matter are printed: any line that fits a scaler/mean to
data, or applies a transform at predict time.
"""
import io
import os
import re
import sys
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "code_audit.txt")
L = []

CANDIDATES = [
    ("MOABB", "NeuroTechX/moabb", "master",
     "examples/plot_cross_session_motor_imagery.py"),
    ("MOABB", "NeuroTechX/moabb", "main",
     "examples/plot_cross_session_motor_imagery.py"),
    ("Braindecode", "braindecode/braindecode", "master",
     "examples/plot_bcic_iv_2a_moabb_trial.py"),
    ("Braindecode", "braindecode/braindecode", "master",
     "braindecode/preprocessing/preprocess.py"),
    ("MNE", "mne-tools/mne-python", "main", "mne/decoding/transformer.py"),
    ("pyRiemann", "pyRiemann/pyRiemann", "master",
     "examples/plot_motor_imagery.py"),
    ("pyRiemann", "pyRiemann/pyRiemann", "master", "pyriemann/utils/mean.py"),
]

PAT = re.compile(r"(StandardScaler|\.fit\(|\.fit_transform\(|\.transform\(|mean\(|"
                 r"class Scaler|class StandardScaler|def transform|def fit)")


def say(s=""):
    L.append(str(s))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def fetch(repo, branch, path):
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (repo, branch, path)
    r = urllib.request.Request(url, headers={"User-Agent": "audit"})
    with urllib.request.urlopen(r, timeout=30) as f:
        return f.read().decode("utf-8", "ignore")


def main():
    say("public code audit: how each file references the session mean")
    say("")
    seen = set()
    for name, repo, branch, path in CANDIDATES:
        key = (repo, path)
        if key in seen:
            continue
        seen.add(key)
        try:
            txt = fetch(repo, branch, path)
        except Exception as e:
            continue
        lines = txt.split("\n")
        hits = [(i + 1, l.strip()) for i, l in enumerate(lines) if PAT.search(l)]
        say("=" * 78)
        say("%s  %s/%s  (%d lines)" % (name, repo, path, len(lines)))
        say("=" * 78)
        for n, l in hits[:12]:
            say("  %4d | %s" % (n, l[:120]))
        say("")
    print("done", OUT)


if __name__ == "__main__":
    main()
