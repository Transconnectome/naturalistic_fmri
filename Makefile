.PHONY: help install search download retry select upload full-pipeline clean check verify

NOTEBOOK_ID ?= d9265824-3383-4fd4-8d17-03512a338ee5
PYTHON := python3

help:
	@echo "Naturalistic fMRI Pipeline — Makefile"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install Python dependencies"
	@echo "  make check          Verify environment (Python, nlm CLI, gh)"
	@echo ""
	@echo "Pipeline (run in order):"
	@echo "  make search         PubMed search → papers_all.json (1-3 min)"
	@echo "  make download       Europe PMC PDF fetch → pdfs/ (~15 min)"
	@echo "  make retry          Retry failed downloads with backoff (~10 min)"
	@echo "  make select         Score-based top-100 selection → top100_paths.json"
	@echo "  make upload         Bulk NotebookLM upload (requires NOTEBOOK_ID, 5-10 min)"
	@echo "  make full-pipeline  Run all stages in sequence"
	@echo ""
	@echo "Quality checks:"
	@echo "  make verify         Validate JSON files, PDF counts, answer files"
	@echo "  make clean          Remove /tmp artifacts, *.pyc"
	@echo ""
	@echo "Overrides:"
	@echo "  NOTEBOOK_ID=<uuid>  Use different notebook (default: shared one)"

install:
	pip install -r requirements.txt

check:
	@$(PYTHON) --version
	@$(PYTHON) -c "import requests; print(f'requests {requests.__version__}')"
	@which nlm || (echo "WARN: nlm CLI not installed. Run: pip install notebooklm-mcp-cli")
	@which gh || (echo "WARN: gh CLI not installed")

search:
	$(PYTHON) search_papers.py

download:
	$(PYTHON) select_and_download.py

retry:
	$(PYTHON) retry_failed.py

select:
	$(PYTHON) select_100.py

upload:
	@if [ -z "$(NOTEBOOK_ID)" ]; then echo "ERROR: NOTEBOOK_ID not set"; exit 1; fi
	NOTEBOOK_ID=$(NOTEBOOK_ID) bash upload_to_nlm.sh

full-pipeline: search download retry select upload
	@echo "=== Full pipeline complete ==="
	@echo "Next: run 20 queries (see docs/04-queries.md)"

verify:
	@echo "=== Validating metadata ==="
	@$(PYTHON) -c "import json; d=json.load(open('papers_all.json')); print(f'papers_all: {len(d)} entries')"
	@$(PYTHON) -c "import json; d=json.load(open('top100_paths.json')); print(f'top100_paths: {len(d)} paths')"
	@echo ""
	@echo "=== Counting PDFs ==="
	@ls pdfs/*.pdf 2>/dev/null | wc -l | awk '{print "PDFs: "$$1}'
	@echo ""
	@echo "=== Answer files ==="
	@ls answers/*.md 2>/dev/null | wc -l | awk '{print "Answers: "$$1}'
	@echo ""
	@echo "=== Logs ==="
	@test -f logs/upload.log && awk 'END {print "upload.log: "NR" lines"}' logs/upload.log || echo "upload.log: missing"
	@test -f logs/upload_fail.log && awk 'END {print "upload_fail.log: "NR" lines"}' logs/upload_fail.log || echo "upload_fail.log: missing"

clean:
	rm -rf __pycache__ *.pyc
	rm -f /tmp/test*.pdf /tmp/epmc_test*.pdf /tmp/PMC*.tar.gz /tmp/t.pdf
	@echo "Clean complete"
