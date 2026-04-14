#!/usr/bin/env python3
"""Re-apply strict relevance filter on papers_missed_pubmed.json without re-fetching."""
import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))
from search_extended import is_relevant, journal_matches

IN_FILE = Path("/home/juke/naturalistic_fmri_pdfs/papers_missed_pubmed.json")
OUT_FILE = Path("/home/juke/naturalistic_fmri_pdfs/papers_missed_pubmed.json")

def main():
    with open(IN_FILE) as f:
        papers = json.load(f)
    print(f"Input: {len(papers)}")

    kept = []
    dropped_relev = 0
    dropped_jrnl = 0
    for p in papers:
        if not is_relevant(p):
            dropped_relev += 1
            continue
        if not journal_matches(p.get("journal")):
            dropped_jrnl += 1
            continue
        kept.append(p)

    print(f"Dropped (not relevant): {dropped_relev}")
    print(f"Dropped (journal):     {dropped_jrnl}")
    print(f"Kept:                  {len(kept)}")

    # Sort: PMC-available first, then by year desc
    kept.sort(key=lambda r: (not r.get("has_pmc", False), -int(r.get("year") or 0)))

    with open(OUT_FILE, "w") as f:
        json.dump(kept, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(kept)} to {OUT_FILE}")

    # Stats
    years = Counter(r.get("year") for r in kept)
    print(f"\nYears: {dict(sorted(years.items()))}")
    jrns = Counter(r.get("journal", "Unknown") for r in kept)
    print(f"\nTop 20 journals:")
    for j, c in jrns.most_common(20):
        print(f"  {c:4d}  {j}")
    tags = Counter(r.get("matched_query") for r in kept)
    print(f"\nTop matched queries:")
    for t, c in tags.most_common(30):
        print(f"  {c:4d}  {t}")

if __name__ == "__main__":
    main()
