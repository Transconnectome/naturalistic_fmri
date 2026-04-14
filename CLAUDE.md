# CLAUDE.md — AI Agent Onboarding Guide

> Project-specific instructions for **Claude Code** and other AI agents working with this repository.

This document is automatically loaded by Claude Code when running in this repo. It provides context, conventions, and common operations so agents can be productive immediately.

---

## 🎯 Project Identity

**Name**: Naturalistic fMRI Literature & Wisdom Synthesis (2021-2026)
**Purpose**: Curate 100 top-tier naturalistic fMRI papers, upload to NotebookLM, query with 20 expert-level questions, synthesize into a wisdom document.
**Status**: Production pipeline. 100/100 PDFs uploaded, 20/20 queries executed, synthesis in progress.

**Core philosophy**:
- Evidence over assumption — every claim in answers must cite corpus papers
- Reproducibility first — all scripts run end-to-end with zero manual config
- AI as force multiplier — NotebookLM, Claude, and foundation models compound each other

---

## 🗺️ Repository Map (What Lives Where)

```
Python pipeline (order of execution):
  search_papers.py         → PubMed E-utilities multi-query
  select_and_download.py   → Europe PMC PDF fetch (parallel)
  retry_failed.py          → HTTP 500 retry with backoff
  select_100.py            → Relevance-score selection
  save_answer.py           → NotebookLM JSON → markdown parser
  upload_to_nlm.sh         → Bulk NotebookLM upload

Metadata (JSON, all stable):
  papers_all.json          ← 335 filtered papers (full metadata)
  papers_top120.json       ← top 120 candidates
  papers_selected.json     ← download targets (120)
  top100_paths.json        ← selected 100 PDF paths
  download_manifest.json   ← what downloaded
  retry_manifest.json      ← retry outcomes

Query answers (markdown, 20 files):
  answers/Q01_statistical_inference.md
  answers/Q02_stimulus_standardization.md
  ...
  answers/Q20_beyond_movies.md
  (each contains: full answer + references with source_ids + cited_text)

Documentation (docs/):
  01-quickstart.md         ← 5-min onboarding
  02-pipeline.md           ← technical deep-dive on pipeline
  03-notebooklm-guide.md   ← NotebookLM setup + MCP + CLI usage
  04-queries.md            ← 20 queries verbatim + rationale
  05-reproducibility.md    ← reproduce from scratch
  06-extending.md          ← add papers / new queries

Ignored (gitignore):
  pdfs/                    ← 131 PDFs (~350 MB, copyright)
  *.log                    ← runtime logs
  __pycache__/, .venv/     ← Python artifacts
```

---

## 🚦 Common Operations (Copy-Paste Ready)

### ✅ Run the full pipeline from scratch

```bash
# Requires: pip, nlm CLI, NotebookLM Plus account
pip install -r requirements.txt
make full-pipeline         # search → download → retry → select → upload
```

### ✅ Add new papers (e.g., extend to 2027)

```bash
# Edit search_papers.py QUERIES (update year range)
python3 search_papers.py           # Regenerate papers_all.json
python3 select_and_download.py     # Download new papers
python3 select_100.py              # Re-select top 100
# Manually diff top100_paths.json old vs. new, upload deltas
```

### ✅ Run a single query against the NotebookLM notebook

**Via MCP (preferred in Claude Code)**:
```python
# Use mcp__notebooklm__notebook_query
notebook_id = "d9265824-3383-4fd4-8d17-03512a338ee5"  # default notebook
query = "Q21 — [your new question]: ..."
# Result saved to tool-results/, parse with save_answer.py
```

**Via CLI**:
```bash
nlm chat <notebook_id> "Q21 — [your question]"
```

### ✅ Parse a NotebookLM answer JSON

```bash
python3 save_answer.py \
  --file /path/to/tool-result.txt \
  --qid 21 \
  --title "my_query_topic"
# → answers/Q21_my_query_topic.md
```

### ✅ Rebuild the wisdom synthesis

```bash
# Manual synthesis (recommended — needs expert judgment)
# Open all answers/*.md, distill into structured wisdom_synthesis.md
# Structure: 7 categories × (SOTA / Outstanding / AI / Citations)
```

---

## 🛠️ Tooling Conventions

### Python Style

- **Python 3.12+** (test on 3.10+)
- **stdlib + requests only** for pipeline scripts (no heavy deps)
- **Type hints recommended** but not enforced
- **Functions over classes** unless state is essential (stateless pipelines)
- **Parallelism**: `concurrent.futures.ThreadPoolExecutor(max_workers=3-6)` with `random.uniform` jitter to avoid rate limits

### Shell Style

- **Bash 4+** features OK (`mapfile`, `${!arr[@]}`)
- **Set -u** for safety; avoid `set -e` in parallel contexts (lose failures)
- **Log everything** to separate success / failure files

### Data Files

- **JSON** with `indent=2, ensure_ascii=False` (non-ASCII in titles preserved)
- **Manifests** as list of tuples `[idx, pmid, status, path]`
- **Never mutate metadata files in place** — regenerate from source

---

## 🔑 Authentication & Secrets

### NotebookLM (`nlm` CLI)

```bash
nlm login                    # Browser OAuth, saves tokens to ~/.nlm/
nlm login switch <profile>   # Multi-account switching
```

Token location: `~/.nlm/profiles/<profile>/tokens.json` — **never commit**.

### GitHub

Standard gh CLI: `gh auth login`. This repo's default account: `snuconnectome`.

### No API keys required for core pipeline

PubMed E-utilities and Europe PMC are **unauthenticated** (with 3 req/s rate limit).

---

## 🚫 Do Not

1. **Never commit PDFs** — `.gitignore` covers `pdfs/` and `*.pdf`; check before push
2. **Never commit `tool-results/` raw outputs** — contains system paths
3. **Never modify `papers_all.json` by hand** — always regenerate via `search_papers.py`
4. **Never bypass `save_answer.py`** when storing NotebookLM responses — maintains citation integrity
5. **Never share the specific notebook ID `d9265824-...`** without checking if it's been made public
6. **Never hit NCBI PMC directly** for PDFs — use Europe PMC (PoW bypass)
7. **Never parallel-upload to NotebookLM with >6 workers** — hits rate limits
8. **Never trust inline LLM-generated content without verifying against NotebookLM citations** — hallucination risk in synthesis

---

## ✅ Always Do

1. **Read before edit** — this repo has carefully designed conventions
2. **Test scripts on 5 papers first** before full-scale runs
3. **Commit after each phase** — search → download → select → upload → query → synthesize
4. **Save raw NotebookLM JSON** before parsing — useful for re-runs
5. **Use TaskCreate** for anything 3+ steps
6. **Spawn Explore/Plan agents** for tasks involving >3 searches
7. **Preserve citation source_ids** in all synthesis outputs — enables forward traceability
8. **Keep answers/ files append-only** — treat as immutable log of what NotebookLM said at time T

---

## 🤖 Agent-Specific Guidance

### For Claude Code (this assistant)

- **Current default notebook ID**: `d9265824-3383-4fd4-8d17-03512a338ee5` (Naturalistic fMRI Literature 2021-2026)
- **Deferred tools**: `mcp__notebooklm__*`, `mcp__tavily__*`, `mcp__context7__*` — load via ToolSearch
- **Background uploads**: Use `run_in_background: true` for `upload_to_nlm.sh` (100 uploads take ~5 min)
- **Persisted outputs**: NotebookLM answers >30 KB go to `tool-results/` — path in response

### For Research Agents (deep-research-agent, etc.)

- Check `answers/Q01-Q20_*.md` before running new NotebookLM queries — likely already answered
- When adding external knowledge, clearly mark as "outside corpus" to preserve citation integrity

### For Writing Agents (technical-writer, cha-writer)

- Documentation style: **bilingual Korean/English** where useful, Korean preferred for narrative
- Technical content: **English first**, Korean annotations
- Code identifiers: **never translate** — keep `papers_all.json`, `search_papers.py` in English

---

## 📐 Query Design Principles (for adding new queries)

The 20 existing queries follow a **3-part structure**. When proposing new queries:

```markdown
Q## — [Title]: [One-sentence scope setter referencing corpus theme]
(a) SOTA: What does the corpus reveal about [X]? [Specific paper hooks if possible]
(b) Outstanding: What remains unresolved — [dimension 1] vs. [dimension 2]?
(c) AI angle: How can [specific AI approach] address [specific limitation]?
Synthesize across multiple papers with citations.
```

**Why this structure**:
- (a) grounds the answer in the corpus (SOTA consensus)
- (b) elicits debates (productive tensions)
- (c) surfaces neuro-AI opportunities (the novel contribution)

**Category placement**: Match new queries to one of 7 existing categories (A-G in `docs/04-queries.md`). If it doesn't fit, propose a new category first.

---

## 🔄 Workflow Integration Points

### When user asks "add N more papers"

1. Run `search_papers.py` with updated queries
2. Diff `papers_all.json` to find new PMIDs
3. Download only the diff via `select_and_download.py` with filtered input
4. Upload diff to NotebookLM via `upload_to_nlm.sh`
5. (Optional) Re-run representative queries to check if answers change

### When user asks "run query X against the notebook"

1. Check `answers/` first — is it already there?
2. If no: craft 3-part query, submit via MCP, parse with `save_answer.py`
3. Save to `answers/Q##_title.md`
4. Update `docs/04-queries.md` to register the new query

### When user asks "synthesize findings"

1. Load all `answers/*.md` files
2. Group by category (A-G)
3. For each category, extract: SOTA consensus, outstanding debates, AI opportunities, key citations
4. Write `wisdom_synthesis.md` with structured template
5. Include cross-cutting themes (e.g., foundation models appear in multiple categories)

---

## 📊 Quality Gates

Before committing:

- [ ] `git status` — no PDFs or tool-results/ accidentally staged
- [ ] `git diff` — no hardcoded tokens or absolute paths (/home/juke/...)
- [ ] Answer files valid markdown (render in GitHub preview)
- [ ] Metadata JSON valid (`python3 -c "import json; json.load(open('papers_all.json'))"`)

Before merging to main:

- [ ] All 20 query answers in `answers/`
- [ ] `README.md` reflects current state (version, dates, counts)
- [ ] `docs/` updated if pipeline changed
- [ ] `upload.log` captured if NotebookLM state changed

---

## 🆘 Troubleshooting

### PMC returns HTML instead of PDF

**Cause**: NCBI's new PoW challenge.
**Fix**: Ensure `fetch_pmc_pdf_url()` uses `europepmc.org/articles/PMC{id}?pdf=render`.

### Europe PMC returns HTTP 500

**Cause**: Rate limit or paper not yet indexed.
**Fix**: `retry_failed.py` with exponential backoff (already implemented). If persistent, try BioC API `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC{id}/unicode` as fallback.

### NotebookLM upload fails with "too many requests"

**Cause**: Parallel >6 workers.
**Fix**: Reduce `-P` in `upload_to_nlm.sh` to 2-3; add `sleep 0.5` between batches.

### `nlm` CLI says "not authenticated"

**Fix**: `nlm login` (opens browser). For headless: `nlm login --device-code`.

### Claude Code `mcp__notebooklm__*` tools not loading

**Fix**: Use `ToolSearch` first:
```
ToolSearch(query="select:mcp__notebooklm__notebook_query,mcp__notebooklm__source_add", max_results=5)
```

---

## 🗣️ Communication Conventions

When reporting progress to the user:

- **Korean** for conversational text (매뉴얼, 진행 상황)
- **English** for code, identifiers, file paths
- **Concise**: ≤100 words for routine updates, longer for deliverables
- **Show don't tell**: paste counts (`100/100 success`), not adjectives (`많은`, `성공적`)

---

## 📚 Further Reading

- [`README.md`](README.md) — project overview
- [`docs/01-quickstart.md`](docs/01-quickstart.md) — 5-minute onboarding
- [`docs/02-pipeline.md`](docs/02-pipeline.md) — pipeline technical deep-dive
- [`docs/03-notebooklm-guide.md`](docs/03-notebooklm-guide.md) — NotebookLM setup + usage
- [`docs/04-queries.md`](docs/04-queries.md) — all 20 queries + design rationale
- [`docs/05-reproducibility.md`](docs/05-reproducibility.md) — reproduce from scratch
- [`docs/06-extending.md`](docs/06-extending.md) — add papers / new queries

---

*Last updated: 2026-04-14 by Claude Opus 4.6 orchestrating SNU Connectome Lab's naturalistic fMRI synthesis*
