#!/usr/bin/env python3
"""Regenerate the KurdishMCQ distribution figures (Data in Brief article, Figs. 1-2)
directly from the published dataset.

Usage:
    python3 make_figures.py KurdishMCQ.json
Outputs: options_distribution.svg, grade_distribution.svg
"""
import json, sys
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def bar(fname, labels, counts, xlabel, figsize, pad, ylim_pad):
    plt.figure(figsize=figsize)
    bars = plt.bar(labels, counts, color=["#4ba3d9"] * len(labels))
    for b in bars:
        h = b.get_height()
        plt.text(b.get_x() + b.get_width() / 2, h + pad, f"{h}",
                 ha="center", va="bottom", fontsize=10)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.ylim(0, max(counts) + ylim_pad)
    plt.tight_layout()
    plt.savefig(fname, dpi=150, bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close()
    print("wrote", fname)

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1], encoding="utf-8"))

    ans = Counter(r["answer"] for r in data)
    bar("options_distribution.svg", ["A", "B", "C", "D"],
        [ans[c] for c in "ABCD"], "Options", (6, 4), 20, 300)

    gr = Counter(r["grade"] for r in data)
    labels = ["9", "10", "11", "12", "Other"]
    bar("grade_distribution.svg", labels,
        [gr[l.lower()] if l == "Other" else gr[l] for l in labels],
        "Grade level", (7, 4), 100, 600)

if __name__ == "__main__":
    main()
