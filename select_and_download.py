#!/usr/bin/env python3
"""
Select top 100 naturalistic fMRI papers and download PDFs.
Filters out lower-tier journals, prioritizes PMC-available for reliable download.
"""
import json
import re
import requests
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = Path("/home/juke/naturalistic_fmri_pdfs")
PDF_DIR = OUT_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# Journals to EXCLUDE (not truly top-tier for this field)
EXCLUDE = [
    "brain sciences",  # MDPI
]

def is_excluded(journal):
    if not journal:
        return True
    j = journal.lower()
    return any(e in j for e in EXCLUDE)

def sanitize_filename(name, maxlen=150):
    """Make filename safe and reasonably short."""
    if not name:
        return "untitled"
    # Remove HTML-ish characters
    name = re.sub(r'<[^>]+>', '', name)
    # Replace unsafe chars
    name = re.sub(r'[^\w\-. ]', '_', name)
    name = re.sub(r'\s+', '_', name)
    return name[:maxlen].strip('_.')

def make_filename(paper, idx):
    year = paper.get("year") or "NA"
    first_author = "Unknown"
    if paper.get("authors"):
        first_author = paper["authors"][0].split()[-1]  # last name
    title = paper.get("title") or "untitled"
    title_short = sanitize_filename(title, maxlen=80)
    return f"{idx:03d}_{year}_{sanitize_filename(first_author, 30)}_{title_short}.pdf"

def fetch_pmc_pdf_url(pmc_id):
    """Get actual PDF URL via Europe PMC (avoids PMC PoW challenge)."""
    pmc = pmc_id.replace("PMC", "")
    # Europe PMC render URL bypasses NCBI PMC PoW and returns PDF directly
    url = f"https://europepmc.org/articles/PMC{pmc}?pdf=render"
    return url

def download_pdf(paper, idx):
    """Download a single PDF."""
    filename = make_filename(paper, idx)
    fpath = PDF_DIR / filename
    if fpath.exists() and fpath.stat().st_size > 10000:
        return (idx, paper.get("pmid"), "SKIP_EXISTS", str(fpath))

    pmc_id = paper.get("pmc_id")
    if not pmc_id:
        return (idx, paper.get("pmid"), "NO_PMC", None)

    pdf_url = fetch_pmc_pdf_url(pmc_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept": "application/pdf,*/*",
    }
    try:
        r = requests.get(pdf_url, headers=headers, timeout=60, allow_redirects=True)
        if r.status_code == 200 and (r.headers.get("Content-Type", "").startswith("application/pdf") or r.content[:4] == b"%PDF"):
            with open(fpath, "wb") as f:
                f.write(r.content)
            return (idx, paper.get("pmid"), "OK", str(fpath))
        else:
            return (idx, paper.get("pmid"), f"HTTP_{r.status_code}_CT_{r.headers.get('Content-Type', 'NA')[:30]}", None)
    except Exception as e:
        return (idx, paper.get("pmid"), f"ERROR_{type(e).__name__}", None)

def main():
    # Load all filtered papers
    all_papers = json.loads((OUT_DIR / "papers_all.json").read_text())
    print(f"Loaded {len(all_papers)} papers from papers_all.json")

    # Filter out excluded journals
    filtered = [p for p in all_papers if not is_excluded(p.get("journal"))]
    print(f"After excluding low-tier journals: {len(filtered)}")

    # Prioritize PMC-available, then year desc, then relevance (keep current order within group)
    filtered.sort(key=lambda r: (not r.get("has_pmc", False), -int(r.get("year") or 0)))

    # Keep top 120 PMC-available (allow slack for failures)
    pmc_papers = [p for p in filtered if p.get("has_pmc")][:120]
    print(f"Top {len(pmc_papers)} PMC-available papers selected for download")

    # Save selected list
    sel_file = OUT_DIR / "papers_selected.json"
    with open(sel_file, "w") as f:
        json.dump(pmc_papers, f, indent=2, ensure_ascii=False)

    # Download in parallel with limited concurrency
    print("\nDownloading PDFs (concurrent, max 6)...")
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(download_pdf, p, i+1): (i, p) for i, p in enumerate(pmc_papers)}
        for fut in as_completed(futures):
            idx, p = futures[fut]
            res = fut.result()
            results.append(res)
            status = res[2]
            print(f"  [{res[0]:03d}] PMID={res[1]} → {status}")

    # Summary
    ok = sum(1 for r in results if r[2] in ("OK", "SKIP_EXISTS"))
    fails = [r for r in results if r[2] not in ("OK", "SKIP_EXISTS")]
    print(f"\n=== Download Summary ===")
    print(f"Successful: {ok}")
    print(f"Failed: {len(fails)}")
    if fails:
        print("\nFirst 10 failures:")
        for r in fails[:10]:
            print(f"  [{r[0]:03d}] PMID={r[1]} → {r[2]}")

    # Save download manifest
    manifest = OUT_DIR / "download_manifest.json"
    with open(manifest, "w") as f:
        json.dump(results, f, indent=2)

    # Count actual PDF files
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    print(f"\nActual PDFs in {PDF_DIR}: {len(pdf_files)}")

if __name__ == "__main__":
    main()
