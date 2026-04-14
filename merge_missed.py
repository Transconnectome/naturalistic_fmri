#!/usr/bin/env python3
"""Merge + deduplicate missed papers from PubMed extended + web/preprint searches."""
import json
import re
from pathlib import Path
from collections import Counter, defaultdict

OUT_DIR = Path("/home/juke/naturalistic_fmri_pdfs")

def normalize_title(t):
    """Lowercase, remove non-alphanum, trim."""
    if not t:
        return ""
    t = re.sub(r'<[^>]+>', '', t)          # strip HTML
    t = re.sub(r'[^a-z0-9\s]', '', t.lower())
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def normalize_doi(d):
    if not d:
        return ""
    return d.lower().strip().replace('https://doi.org/', '').replace('http://doi.org/', '').rstrip('/')

def main():
    pm = json.load(open(OUT_DIR / "papers_missed_pubmed.json"))
    web = json.load(open(OUT_DIR / "papers_missed_web.json"))
    existing = set(open(OUT_DIR / "existing_pmids.txt").read().strip().split('\n'))
    print(f"PubMed missed: {len(pm)}")
    print(f"Web missed: {len(web)}")
    print(f"Existing PMIDs: {len(existing)}")

    # Normalize both to unified schema
    unified = []

    for p in pm:
        unified.append({
            "pmid": p.get("pmid"),
            "doi": normalize_doi(p.get("doi", "")),
            "title": p.get("title", ""),
            "title_normalized": normalize_title(p.get("title", "")),
            "authors": p.get("authors", []),
            "journal": p.get("journal", ""),
            "year": p.get("year"),
            "venue": p.get("journal", ""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{p.get('pmid')}/" if p.get("pmid") else "",
            "pmc_id": p.get("pmc_id"),
            "has_pmc": p.get("has_pmc", False),
            "abstract": p.get("abstract", "")[:500] if p.get("abstract") else "",
            "source": "pubmed_extended",
            "matched_query": p.get("matched_query", ""),
            "priority": None,
            "source_hop": None,
        })

    for p in web:
        authors = p.get("authors", "")
        if isinstance(authors, str):
            authors = [a.strip() for a in re.split(r'[,;]', authors) if a.strip()][:5]
        unified.append({
            "pmid": p.get("pmid"),
            "doi": normalize_doi(p.get("doi", "")),
            "title": p.get("title", ""),
            "title_normalized": normalize_title(p.get("title", "")),
            "authors": authors if isinstance(authors, list) else [str(authors)],
            "journal": p.get("venue", ""),
            "year": str(p.get("year", "")),
            "venue": p.get("venue", ""),
            "url": p.get("url", ""),
            "pmc_id": None,
            "has_pmc": False,
            "abstract": p.get("abstract_snippet", "")[:500],
            "source": "web_preprint",
            "matched_query": p.get("relevance_reason", ""),
            "priority": p.get("priority"),
            "source_hop": p.get("source_hop"),
        })

    print(f"Total before dedup: {len(unified)}")

    # Dedup by (title_normalized, doi, pmid)
    seen_keys = set()
    deduped = []
    dup_count = 0
    for p in unified:
        keys = []
        if p["pmid"]:
            keys.append(("pmid", p["pmid"]))
        if p["doi"]:
            keys.append(("doi", p["doi"]))
        if p["title_normalized"]:
            keys.append(("title", p["title_normalized"][:100]))  # first 100 chars

        # Check if any key already seen
        already = any(k in seen_keys for k in keys)
        if already:
            dup_count += 1
            continue

        # Add all keys for this paper
        for k in keys:
            seen_keys.add(k)
        deduped.append(p)

    print(f"After dedup (intra-missed): {len(deduped)} ({dup_count} duplicates removed)")

    # Cross-check against existing corpus (by PMID)
    before_existing_filter = len(deduped)
    deduped = [p for p in deduped if not p.get("pmid") or p["pmid"] not in existing]
    print(f"After excluding existing PMIDs: {len(deduped)} ({before_existing_filter - len(deduped)} in existing corpus)")

    # Sort: PubMed papers first (more structured metadata), then by year desc
    deduped.sort(key=lambda p: (
        0 if p["source"] == "pubmed_extended" else 1,
        -int(p["year"]) if p["year"] and str(p["year"]).isdigit() else 0,
    ))

    # Save
    out_file = OUT_DIR / "papers_missed.json"
    with open(out_file, "w") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)
    print(f"\nSaved merged output: {out_file} ({len(deduped)} papers)")

    # Statistics
    print("\n=== Statistics ===")
    years = Counter(str(p.get("year", "")) for p in deduped)
    print("\nYears:")
    for y in sorted(years, reverse=True)[:10]:
        print(f"  {y}: {years[y]}")

    sources = Counter(p["source"] for p in deduped)
    print("\nSources:")
    for s, c in sources.items():
        print(f"  {s}: {c}")

    venues = Counter(p["venue"] or p["journal"] for p in deduped)
    print("\nTop 20 venues:")
    for v, c in venues.most_common(20):
        print(f"  {c:4d}  {v[:60]}")

    has_pmc = sum(1 for p in deduped if p["has_pmc"])
    print(f"\nPMC available (downloadable): {has_pmc}")

    priorities = Counter(p.get("priority") for p in deduped if p.get("priority"))
    print(f"\nWeb-identified priorities: {dict(priorities)}")

if __name__ == "__main__":
    main()
