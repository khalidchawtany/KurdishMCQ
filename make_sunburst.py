#!/usr/bin/env python3
"""Regenerate the KurdishMCQ subject/category sunburst (Data in Brief article, Fig. 3)
directly from the published dataset.

Usage:
    python3 make_sunburst.py KurdishMCQ.json
Output: Fig_FullDS_Subjects_PieChart.svg
"""
import json, sys
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SUBJECT_MAPPING = {
    "Biology": "STEM", "Chemistry": "STEM", "Math": "STEM", "Physics": "STEM",
    "Natural Science": "STEM",
    "History": "Humanities", "Religion Studies": "Humanities",
    "Economics": "Social Science", "Geography": "Social Science",
    "Kurdish Language (Grammar)": "Language", "Kurdish Language (Literature)": "Language",
    "Driving Test": "Other",
}
DISPLAY = {  # line-broken labels as in the article figure
    "Kurdish Language (Grammar)": "Kurdish Language\n(Grammar)",
    "Kurdish Language (Literature)": "Kurdish Language\n(Literature)",
}
CAT_COLORS = {
    "STEM": "#8b2282", "Humanities": "#4ba3d9", "Social Science": "#215891",
    "Language": "#1a6323", "Other": "#d97706",
}
SUB_COLORS = {
    "Biology": "#8b2282", "Physics": "#a55194", "Chemistry": "#ce93d8",
    "Natural Science": "#e1bee7", "Math": "#8b2282",
    "History": "#b3e5fc", "Religion Studies": "#81d4fa",
    "Economics": "#29b6f6", "Geography": "#0288d1",
    "Kurdish Language\n(Grammar)": "#1a6323", "Kurdish Language\n(Literature)": "#388e3c",
    "Driving Test": "#f59e0b",
}

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    counts = Counter(r["subject"] for r in data)

    items = [(DISPLAY.get(s, s), c, SUBJECT_MAPPING[s]) for s, c in counts.items()]
    items.sort(key=lambda x: (x[2], -x[1]))

    inner_labels = [x[0] for x in items]
    inner_counts = [x[1] for x in items]
    inner_colors = [SUB_COLORS[x[0]] for x in items]

    cat_counts, cat_labels, cat_colors = [], [], []
    cur, tot = None, 0
    for _, cnt, cat in items:
        if cat != cur:
            if cur is not None:
                cat_counts.append(tot); cat_labels.append(cur); cat_colors.append(CAT_COLORS[cur])
            cur, tot = cat, cnt
        else:
            tot += cnt
    cat_counts.append(tot); cat_labels.append(cur); cat_colors.append(CAT_COLORS[cur])

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
    wedges_out, _ = ax.pie(cat_counts, radius=1, colors=cat_colors,
                           wedgeprops=dict(width=0.35, edgecolor="white", linewidth=2))
    wedges_in, _ = ax.pie(inner_counts, radius=0.65, colors=inner_colors,
                          wedgeprops=dict(width=0.45, edgecolor="white", linewidth=1.5))

    def add_labels(wedges, labels, radius, fontsize, color, fontweight="normal", split_lines=False):
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
            y, x = np.sin(np.deg2rad(ang)), np.cos(np.deg2rad(ang))
            rotation = ang if ang < 90 or ang > 270 else ang + 180
            display_text = labels[i].replace(" ", "\n") if split_lines else labels[i]
            fs = fontsize - 3 if "\n" in labels[i] else fontsize
            ax.text(x * radius, y * radius, display_text,
                    ha="center", va="center", fontsize=fs, color=color,
                    fontweight=fontweight, rotation=rotation, rotation_mode="anchor",
                    fontfamily="serif", linespacing=0.9)

    add_labels(wedges_out, cat_labels, 0.82, 14, "white", "bold", split_lines=True)
    add_labels(wedges_in, inner_labels, 0.42, 14, "white", split_lines=False)

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.axis("off")
    plt.savefig("Fig_FullDS_Subjects_PieChart.svg", dpi=150,
                bbox_inches="tight", pad_inches=0, transparent=True)
    print("wrote Fig_FullDS_Subjects_PieChart.svg")

if __name__ == "__main__":
    main()
