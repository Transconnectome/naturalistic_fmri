#!/usr/bin/env python3
"""Select top 100 naturalistic fMRI PDFs from downloaded set based on title relevance."""
import json
import re
from pathlib import Path

PDF_DIR = Path("/home/juke/naturalistic_fmri_pdfs/pdfs")

STRONG = ["naturalistic", "movie watching", "movie-watching", "narrative", "inter-subject", "intersubject", "isc ", "story listening", "story comprehension", "free viewing", "naturalistic stimul"]
MODERATE = ["movie", " film", "story", "narrative", "listening", "audio", "natural viewing", "event segment", "real-world"]
NEGATIVE = ["task-based", "task based", "preclinical", "rodent", "mouse model", "rtms for psychiatric"]

def score_title(filename):
    # Extract title portion from filename
    lower = filename.lower()
    score = 0
    for w in STRONG:
        if w in lower:
            score += 3
    for w in MODERATE:
        if w in lower:
            score += 1
    for w in NEGATIVE:
        if w in lower:
            score -= 4
    # Prefer newer years for equal score
    m = re.search(r'_(\d{4})_', filename)
    year = int(m.group(1)) if m else 2020
    return (score, year)

def main():
    pdfs = list(PDF_DIR.glob("*.pdf"))
    print(f"Total PDFs: {len(pdfs)}")

    scored = [(score_title(p.name), p) for p in pdfs]
    scored.sort(key=lambda x: (-x[0][0], -x[0][1]))

    # Select top 100
    top100 = [p for (_, p) in scored[:100]]
    print(f"Selected top 100 by relevance score")

    # Print distribution
    years = [int(re.search(r'_(\d{4})_', p.name).group(1)) for p in top100 if re.search(r'_(\d{4})_', p.name)]
    from collections import Counter
    yc = Counter(years)
    for y in sorted(yc, reverse=True):
        print(f"  {y}: {yc[y]}")

    # Save list
    with open("/home/juke/naturalistic_fmri_pdfs/top100_paths.json", "w") as f:
        json.dump([str(p) for p in top100], f, indent=2)

    # Show excluded ones
    excluded = [p for (_, p) in scored[100:]]
    print(f"\nExcluded ({len(excluded)} papers):")
    for p in excluded[:10]:
        s, y = score_title(p.name)
        print(f"  score={s} year={y}: {p.name[:90]}")

    print(f"\nFirst 10 selected:")
    for p in top100[:10]:
        s, y = score_title(p.name)
        print(f"  score={s} year={y}: {p.name[:90]}")

if __name__ == "__main__":
    main()
