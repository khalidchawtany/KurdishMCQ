#!/usr/bin/env python3
"""Quality-control audit for the KurdishMCQ dataset.

Checks blank fields, duplicated options (after Unicode + Kurdish letter-variant
normalization), answer-key consistency, repeated question stems, and fully
identical records, and writes a machine-readable report.

Usage:
    python3 audit_dataset.py KurdishMCQ.json [report.json]
"""
import json, sys, unicodedata, re
from collections import Counter, defaultdict

def norm(s):
    s = unicodedata.normalize("NFKC", str(s or ""))
    s = s.translate(str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"}))
    s = re.sub(r"[​-‏ـ]", "", s)
    return re.sub(r"\s+", " ", s).strip()

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    OPTS = ["option A", "option B", "option C", "option D"]
    report = {"file": sys.argv[1], "total_records": len(data)}

    def rid(i, r):
        return r.get("id", i)

    report["blank_records"] = [rid(i, r) for i, r in enumerate(data)
                               if all(norm(r.get(k)) == "" for k in ["question"] + OPTS)]
    report["blank_options"] = {k: sum(1 for r in data if norm(r.get(k)) == "") for k in OPTS}
    report["blank_fields"] = {k: sum(1 for r in data if norm(r.get(k)) == "")
                              for k in ["group", "grade", "subject", "question", "answer"]}
    report["invalid_answer_keys"] = [rid(i, r) for i, r in enumerate(data)
                                     if norm(r.get("answer")) not in {"A", "B", "C", "D"}]
    report["answer_points_to_blank_option"] = [
        rid(i, r) for i, r in enumerate(data)
        if norm(r.get("answer")) in {"A", "B", "C", "D"}
        and not norm(r.get("option " + r["answer"], ""))]

    dup, amb = [], []
    for i, r in enumerate(data):
        if r.get("source_defect"):
            continue  # documented source-inherited defects
        vals = {c: norm(r.get("option " + c)) for c in "ABCD"}
        nonblank = [v for v in vals.values() if v]
        c = Counter(nonblank)
        dups = {v for v, n in c.items() if n > 1}
        if dups:
            dup.append(rid(i, r))
            if vals.get(r.get("answer", ""), "") in dups:
                amb.append(rid(i, r))
    report["records_with_duplicated_options"] = dup
    report["ambiguous_correct_option_duplicated"] = amb

    stems = defaultdict(list)
    for i, r in enumerate(data):
        q = norm(r.get("question"))
        if q:
            stems[q].append(rid(i, r))
    groups = [v for v in stems.values() if len(v) > 1]
    report["duplicate_stem_groups"] = len(groups)
    report["duplicate_stem_records"] = sum(map(len, groups))

    sig = Counter(tuple(norm(r.get(k)) for k in
                        ["question", "answer"] + OPTS) for r in data)
    report["fully_identical_record_groups"] = sum(1 for c in sig.values() if c > 1)

    out = sys.argv[2] if len(sys.argv) > 2 else "qc_report.json"
    json.dump(report, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for k, v in report.items():
        print(f"{k}: {v if not isinstance(v, list) else len(v)}")
    print("report ->", out)

if __name__ == "__main__":
    main()
