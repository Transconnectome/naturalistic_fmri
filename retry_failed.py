#!/usr/bin/env python3
"""Retry failed downloads with lower concurrency and retries.
Also expand pool to reach 100+ successful downloads."""
import json
import re
import requests
import time
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = Path("/home/juke/naturalistic_fmri_pdfs")
PDF_DIR = OUT_DIR / "pdfs"

EXCLUDE = ["brain sciences"]

def is_excluded(journal):
    if not journal:
        return True
    j = journal.lower()
    return any(e in j for e in EXCLUDE)

def sanitize_filename(name, maxlen=150):
    if not name:
        return "untitled"
    name = re.sub(r'<[^>]+>', '', name)
    name = re.sub(r'[^\w\-. ]', '_', name)
    name = re.sub(r'\s+', '_', name)
    return name[:maxlen].strip('_.')

def make_filename(paper, idx):
    year = paper.get("year") or "NA"
    first_author = "Unknown"
    if paper.get("authors"):
        first_author = paper["authors"][0].split()[-1]
    title = paper.get("title") or "untitled"
    title_short = sanitize_filename(title, maxlen=80)
    return f"{idx:03d}_{year}_{sanitize_filename(first_author, 30)}_{title_short}.pdf"

def download_one(paper, idx, max_retries=3):
    pmc_id = paper.get("pmc_id")
    if not pmc_id:
        return (idx, paper.get("pmid"), "NO_PMC", None)

    filename = make_filename(paper, idx)
    fpath = PDF_DIR / filename
    if fpath.exists() and fpath.stat().st_size > 10000:
        return (idx, paper.get("pmid"), "SKIP_EXISTS", str(fpath))

    pmc = pmc_id.replace("PMC", "")
    url = f"https://europepmc.org/articles/PMC{pmc}?pdf=render"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept": "application/pdf,text/html,*/*;q=0.9",
        "Accept-Language": "en-US,en;q=0.5",
    }

    last_error = None
    for attempt in range(max_retries):
        try:
            time.sleep(0.2 + random.random() * 0.5)
            r = requests.get(url, headers=headers, timeout=90, allow_redirects=True)
            if r.status_code == 200 and (r.headers.get("Content-Type", "").startswith("application/pdf") or r.content[:4] == b"%PDF"):
                with open(fpath, "wb") as f:
                    f.write(r.content)
                return (idx, paper.get("pmid"), "OK", str(fpath))
            last_error = f"HTTP_{r.status_code}"
            if r.status_code in (500, 502, 503, 504, 429):
                time.sleep(2 + attempt * 3)  # backoff
                continue
            else:
                break  # non-retryable
        except Exception as e:
            last_error = f"ERROR_{type(e).__name__}"
            time.sleep(2 + attempt)

    return (idx, paper.get("pmid"), last_error or "FAIL", None)

def main():
    # Load all PMC-available papers from filtered set
    all_papers = json.loads((OUT_DIR / "papers_all.json").read_text())
    filtered = [p for p in all_papers if not is_excluded(p.get("journal")) and p.get("has_pmc")]
    filtered.sort(key=lambda r: -int(r.get("year") or 0))
    print(f"Total PMC-available filtered papers: {len(filtered)}")

    # Check which are already downloaded
    existing_pdfs = {f.name: f for f in PDF_DIR.glob("*.pdf") if f.stat().st_size > 10000}
    print(f"Existing valid PDFs: {len(existing_pdfs)}")

    # Build list of candidates to try (all filtered papers up to 200)
    candidates = filtered[:200]
    print(f"Candidates to attempt: {len(candidates)}")

    # Download with low concurrency + retries
    results = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(download_one, p, i+1): (i, p) for i, p in enumerate(candidates)}
        done = 0
        for fut in as_completed(futures):
            idx, p = futures[fut]
            res = fut.result()
            results.append(res)
            done += 1
            status = res[2]
            if status in ("OK", "SKIP_EXISTS"):
                marker = "✓"
            else:
                marker = "✗"
            print(f"  {marker} [{done:3d}/{len(candidates)}] [{res[0]:03d}] → {status}")

    ok = sum(1 for r in results if r[2] in ("OK", "SKIP_EXISTS"))
    fails = [r for r in results if r[2] not in ("OK", "SKIP_EXISTS")]
    print(f"\n=== Retry Summary ===")
    print(f"Successful: {ok}")
    print(f"Failed: {len(fails)}")

    # Count actual PDFs
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    valid_pdfs = [f for f in pdf_files if f.stat().st_size > 10000]
    print(f"Total valid PDFs in folder: {len(valid_pdfs)}")

    with open(OUT_DIR / "retry_manifest.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
