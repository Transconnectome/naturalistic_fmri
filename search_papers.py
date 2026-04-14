#!/usr/bin/env python3
"""
Search PubMed for naturalistic fMRI papers 2021-2026 from top-tier journals.
Collect PMC PDF URLs for open-access papers.
"""
import requests
import time
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUT_DIR = Path("/home/juke/naturalistic_fmri_pdfs")
OUT_DIR.mkdir(exist_ok=True)

# Top-tier journals for naturalistic fMRI
TOP_JOURNALS = [
    "Nature neuroscience",
    "Neuron",
    "Nature communications",
    "NeuroImage",
    "Cerebral cortex",
    "eLife",
    "Proceedings of the National Academy of Sciences",
    "The Journal of neuroscience",
    "Journal of neuroscience",
    "Current biology",
    "Human brain mapping",
    "Cortex",
    "Imaging neuroscience",
    "Trends in cognitive sciences",
    "Nature human behaviour",
    "Science advances",
    "Communications biology",
    "PLoS biology",
    "Brain",
    "Cell reports",
    "Cognitive neurodynamics",
    "Network neuroscience",
]

# Multiple search queries to maximize coverage
QUERIES = [
    '("naturalistic"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "functional MRI"[Title/Abstract] OR "functional magnetic resonance imaging"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
    '("movie"[Title/Abstract] OR "film"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "functional MRI"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
    '("narrative"[Title/Abstract] OR "storytelling"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "functional MRI"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
    '("inter-subject correlation"[Title/Abstract] OR "intersubject correlation"[Title/Abstract]) AND ("fMRI"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
    '("naturalistic stimuli"[Title/Abstract] OR "naturalistic paradigm"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
    '("audiobook"[Title/Abstract] OR "podcast"[Title/Abstract] OR "spoken language"[Title/Abstract]) AND ("fMRI"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
    '("naturalistic viewing"[Title/Abstract] OR "movie watching"[Title/Abstract] OR "movie-watching"[Title/Abstract]) AND ("fMRI"[Title/Abstract] OR "brain"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
    '("story listening"[Title/Abstract] OR "story comprehension"[Title/Abstract]) AND ("fMRI"[Title/Abstract]) AND ("2021"[PDAT] : "2026"[PDAT])',
]

def esearch(query, retmax=200):
    """Search PubMed and return PMIDs."""
    url = f"{BASE}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "sort": "relevance",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("esearchresult", {}).get("idlist", [])

def efetch(pmids):
    """Fetch PubMed records as XML."""
    if not pmids:
        return []
    url = f"{BASE}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.content

def parse_record(art):
    """Extract relevant info from PubmedArticle XML element."""
    info = {
        "pmid": None,
        "title": None,
        "journal": None,
        "year": None,
        "authors": [],
        "doi": None,
        "pmc_id": None,
        "abstract": None,
    }
    # PMID
    pmid_el = art.find(".//PMID")
    if pmid_el is not None:
        info["pmid"] = pmid_el.text
    # Title
    title_el = art.find(".//ArticleTitle")
    if title_el is not None:
        info["title"] = "".join(title_el.itertext()).strip()
    # Journal
    journal_el = art.find(".//Journal/Title")
    if journal_el is not None:
        info["journal"] = journal_el.text
    # Year
    year_el = art.find(".//PubDate/Year")
    if year_el is None:
        year_el = art.find(".//PubDate/MedlineDate")
    if year_el is not None and year_el.text:
        m = re.search(r"\d{4}", year_el.text)
        if m:
            info["year"] = m.group(0)
    # Authors (first 3)
    for au in art.findall(".//Author")[:3]:
        last = au.find("LastName")
        first = au.find("Initials")
        if last is not None:
            name = last.text
            if first is not None and first.text:
                name = f"{first.text} {name}"
            info["authors"].append(name)
    # DOI and PMC ID
    for id_el in art.findall(".//ArticleId"):
        idtype = id_el.get("IdType")
        if idtype == "doi":
            info["doi"] = id_el.text
        elif idtype == "pmc":
            info["pmc_id"] = id_el.text
    # Abstract
    abstract_parts = []
    for a in art.findall(".//AbstractText"):
        label = a.get("Label")
        text = "".join(a.itertext()).strip()
        if label:
            abstract_parts.append(f"{label}: {text}")
        else:
            abstract_parts.append(text)
    if abstract_parts:
        info["abstract"] = " ".join(abstract_parts)
    return info

def journal_matches(journal_name):
    """Check if journal is in top-tier list (case-insensitive partial match)."""
    if not journal_name:
        return False
    j = journal_name.lower()
    for t in TOP_JOURNALS:
        if t.lower() in j or j in t.lower():
            return True
    return False

def build_pdf_url(info):
    """Construct direct PDF URL from PMC ID if available."""
    if info.get("pmc_id"):
        pmc = info["pmc_id"].replace("PMC", "")
        return f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc}/pdf/"
    return None

def main():
    print("Searching PubMed for naturalistic fMRI papers...")
    all_pmids = set()
    for q in QUERIES:
        print(f"Query: {q[:80]}...")
        try:
            pmids = esearch(q, retmax=200)
            print(f"  → {len(pmids)} PMIDs")
            all_pmids.update(pmids)
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(0.4)  # NCBI rate limit
    print(f"\nTotal unique PMIDs: {len(all_pmids)}")

    # Fetch metadata in batches
    pmid_list = list(all_pmids)
    BATCH = 100
    all_records = []
    for i in range(0, len(pmid_list), BATCH):
        batch = pmid_list[i:i+BATCH]
        print(f"Fetching batch {i//BATCH + 1}/{(len(pmid_list)+BATCH-1)//BATCH} ({len(batch)} records)...")
        try:
            xml = efetch(batch)
            root = ET.fromstring(xml)
            for art in root.findall(".//PubmedArticle"):
                info = parse_record(art)
                all_records.append(info)
        except Exception as e:
            print(f"  ERROR: {e}")
        time.sleep(0.4)

    print(f"\nParsed {len(all_records)} records total")

    # Filter by top journals
    filtered = [r for r in all_records if journal_matches(r.get("journal"))]
    print(f"After top-journal filter: {len(filtered)}")

    # Add PDF URLs for PMC-available papers
    for r in filtered:
        r["pdf_url"] = build_pdf_url(r)
        r["has_pmc"] = bool(r.get("pmc_id"))

    # Sort: PMC-available first (easier to download), then by year desc
    filtered.sort(key=lambda r: (not r.get("has_pmc", False), -int(r.get("year") or 0)))

    # Save all filtered papers
    out_file = OUT_DIR / "papers_all.json"
    with open(out_file, "w") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(filtered)} papers to {out_file}")

    # Stats
    pmc_count = sum(1 for r in filtered if r.get("has_pmc"))
    print(f"  PMC-available (direct PDF): {pmc_count}")
    print(f"  Not in PMC: {len(filtered) - pmc_count}")

    # Top 120 candidates (aim for 100 downloads, allow slack for failures)
    top120 = filtered[:120]
    out_top = OUT_DIR / "papers_top120.json"
    with open(out_top, "w") as f:
        json.dump(top120, f, indent=2, ensure_ascii=False)
    print(f"Saved top 120 candidates to {out_top}")

    # Journal breakdown
    from collections import Counter
    jcount = Counter(r.get("journal", "Unknown") for r in top120)
    print("\nJournal breakdown (top 120):")
    for j, c in jcount.most_common():
        print(f"  {c:3d}  {j}")

if __name__ == "__main__":
    main()
