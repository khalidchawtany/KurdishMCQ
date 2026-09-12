#!/usr/bin/env python3
"""Duplicate removal used during KurdishMCQ dataset construction.

Two records are considered duplicates only if the whitespace-trimmed
(question, choices, answer) signature matches exactly; the first
occurrence is kept. Matching is exact (no fuzzy or orthographic
normalization), as described in the Data in Brief article.

Works with either record layout:
  - construction layout: {"question": ..., "choices": [...], "answer": ...}
  - published layout:    {"question": ..., "option A".."option D", "answer": ...}

Usage:
    python3 dedup.py input.json output.json
"""
import json, sys


def create_signature(item):
    question = item.get('question', '').strip()
    if 'choices' in item:
        choices = tuple(str(c).strip() for c in item.get('choices', []))
    else:
        choices = tuple(str(item.get(f'option {c}', '')).strip() for c in 'ABCD')
    answer = str(item.get('answer', '')).strip()
    return (question, choices, answer)


def filter_entries(entries):
    seen_signatures = set()
    filtered_entries = []
    for entry in entries:
        current_sig = create_signature(entry)
        if current_sig not in seen_signatures:
            filtered_entries.append(entry)
            # Mark this signature as seen so it's not added again
            seen_signatures.add(current_sig)
    return filtered_entries


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    entries = json.load(open(sys.argv[1], encoding='utf-8'))
    filtered = filter_entries(entries)
    json.dump(filtered, open(sys.argv[2], 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f"input: {len(entries)} records")
    print(f"kept:  {len(filtered)} records ({len(entries) - len(filtered)} duplicates removed)")


if __name__ == '__main__':
    main()
