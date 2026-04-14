#!/usr/bin/env python3
"""Save NotebookLM answer to markdown file with citations."""
import json
import sys
import argparse
from pathlib import Path

def save_answer(data, qid, title):
    out_dir = Path("/home/juke/naturalistic_fmri_pdfs/answers")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"Q{qid:02d}_{title.replace(' ', '_').lower()}.md"

    with open(out_file, "w") as f:
        f.write(f"# Q{qid}: {title}\n\n")
        f.write(data.get("answer", ""))
        f.write("\n\n---\n\n## References\n\n")
        for ref in data.get("references", []):
            num = ref.get("citation_number")
            sid = ref.get("source_id", "")[:8]
            text = ref.get("cited_text", "")[:300]
            f.write(f"**[{num}]** (src:{sid}) {text}...\n\n")

        srcs = data.get("sources_used", [])
        f.write(f"\n**Sources used:** {len(srcs)} documents\n")
        for s in srcs[:10]:
            f.write(f"- {s}\n")

    print(f"Saved: {out_file}")
    return str(out_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="JSON file from tool-results")
    parser.add_argument("--json", help="Inline JSON string")
    parser.add_argument("--qid", type=int, required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    elif args.json:
        data = json.loads(args.json)
    else:
        # Read JSON from stdin
        data = json.load(sys.stdin)

    save_answer(data, args.qid, args.title)

if __name__ == "__main__":
    main()
