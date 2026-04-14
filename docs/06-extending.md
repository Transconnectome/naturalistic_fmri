# 06. Extending — 논문/쿼리 추가 워크플로

이 프로젝트를 **확장**하는 방법: 논문 추가, 새 쿼리 실행, 커스텀 분야 적용.

---

## Adding New Papers

### Case 1: 새 연도 추가 (예: 2027)

1. `search_papers.py`에서 연도 업데이트:

```python
# Before
QUERIES = [
    '(...) AND ("2021"[PDAT] : "2026"[PDAT])',
    ...
]

# After
QUERIES = [
    '(...) AND ("2021"[PDAT] : "2027"[PDAT])',
    ...
]
```

2. 검색 재실행:

```bash
python3 search_papers.py
# → papers_all.json 업데이트 (새 PMID 추가)
```

3. Diff 확인:

```python
import json
old = {p['pmid'] for p in json.load(open('papers_all.json.bak'))}
new = {p['pmid'] for p in json.load(open('papers_all.json'))}
added = new - old
print(f"New papers: {len(added)}")
```

4. 다운로드 + 업로드:

```bash
python3 select_and_download.py    # 새 PMC IDs만 다운로드 (기존은 skip)
python3 retry_failed.py
python3 select_100.py             # 선별 갱신 (top 100 바뀔 수 있음)

# 새 PDF만 NotebookLM에 업로드 (manual diff 후)
bash upload_to_nlm.sh             # 또는 specific files만
```

5. 쿼리 재실행 (선택):

```bash
# 이전 쿼리들 재실행하여 답변 업데이트 확인
# NotebookLM은 새 sources 자동 포함
```

---

### Case 2: 새 키워드/주제 추가 (예: VR fMRI)

1. `search_papers.py`의 `QUERIES`에 추가:

```python
QUERIES.append(
    '("virtual reality" OR "VR") AND ("fMRI" OR "functional MRI") '
    'AND ("2021"[PDAT] : "2026"[PDAT])'
)
```

2. (옵션) `TOP_JOURNALS`에 VR 특화 저널 추가:

```python
TOP_JOURNALS.append("PLoS ONE")   # VR fMRI 자주 게재
```

3. 재실행 + 선별 (`select_100.py`의 키워드 업데이트):

```python
STRONG = [
    "naturalistic", "movie watching", ..., 
    "virtual reality",  # 새 키워드
    "VR",
]
```

---

### Case 3: 특정 저자/그룹 논문 추가

PubMed `[AUTH]` 필드 활용:

```python
QUERIES.append(
    '("Hasson U"[AUTH] OR "Norman KA"[AUTH]) AND ("fMRI") '
    'AND ("2021"[PDAT] : "2026"[PDAT])'
)
```

---

## Adding New Queries

### Step 1: 카테고리 결정

기존 7 카테고리 중 하나에 매칭, 또는 새 카테고리 제안:

- A. Methodological Foundations (방법론)
- B. Neural Representation & Dynamics (표상)
- C. Memory, Events, Prediction (기억/사건/예측)
- D. AI-Neuro Alignment (AI-뇌 정합)
- E. Individual Differences & Clinical (개인차·임상)
- F. Developmental & Cross-Species (발달·종간)
- G. Frontiers & Meta-Science (프런티어·메타)

### Step 2: 3-Part 쿼리 작성

템플릿:

```
Q## — [Title]: [1-sentence context referring to specific corpus theme]

(a) SOTA: What does the corpus reveal about [specific phenomenon]?
    [Optional: paper/method hooks]

(b) Outstanding: What remains unresolved — [dimension A] vs. [dimension B]?
    [Optional: productive tensions]

(c) AI angle: How can [specific AI approach] address [specific limitation]?
    [Optional: concrete AI intervention example]

Synthesize with citations.
```

### Step 3: 검증 실행

```python
# 먼저 1회 실행, 답변 품질 체크
result = mcp__notebooklm__notebook_query(
    notebook_id="d9265824-3383-4fd4-8d17-03512a338ee5",
    query="Q21 — [Your query]",
    timeout=180
)

# Quality gates:
assert len(result['answer']) > 3000          # 3 KB+
assert len(result['sources_used']) >= 5      # 최소 5 sources
assert "(a)" in result['answer']             # 3-part 구조 유지
```

### Step 4: 파일 저장

```bash
python3 save_answer.py \
  --file /path/to/response.json \
  --qid 21 \
  --title "my_new_topic"
# → answers/Q21_my_new_topic.md
```

### Step 5: 문서 업데이트

1. `docs/04-queries.md`에 쿼리 추가
2. `README.md` "Category" 표의 # Queries 업데이트
3. `wisdom_synthesis.md`에 새 섹션 반영

---

## Customizing for Different Domains

### 다른 분야 적용 (예: predictive coding fMRI → BCI)

1. `search_papers.py` 전면 재작성:

```python
QUERIES = [
    '("brain-computer interface" OR "BCI") AND ("fMRI") AND ("2021"[PDAT]:"2026"[PDAT])',
    '("motor imagery" OR "neurofeedback") AND ("fMRI") AND ("2021"[PDAT]:"2026"[PDAT])',
    ...
]

TOP_JOURNALS = [
    "Neural Engineering",
    "IEEE TBME",
    "Brain-Computer Interfaces",
    ...
]
```

2. `select_100.py` 스코어 조정:

```python
STRONG = ["brain-computer interface", "BCI", "neurofeedback", "motor imagery"]
MODERATE = ["decoding", "EEG", "real-time"]
NEGATIVE = ["passive viewing"]
```

3. `docs/04-queries.md` 쿼리 전면 재설계 (BCI 특화 SOTA/outstanding/AI 구조)

4. NotebookLM 새 노트북 생성 → 재실행

**결과**: 분야별 재현 가능한 corpus + wisdom synthesis 파이프라인.

---

## Scaling Up

### 100 → 300 papers

- NotebookLM Plus plan 한도 (300) 활용
- `select_100.py` → `select_300.py`로 확장
- Upload 시간 ~30분 (4 parallel 기준)
- Query 품질: citation density 하락 가능, 더 넓은 sources_used 활용

### 100 → 50 papers (downsize)

- Free 플랜으로 가능
- `select_100.py` 스코어 threshold 상향
- 더 엄격한 selection: 각 카테고리에 정확히 7-8 papers 할당

---

## Multi-Notebook Architecture

### 언제: 코퍼스 >300 or topical 분리 필요

**Architecture**:

```
Main Notebook: "Naturalistic fMRI Core"
├── 50 most cited papers

Specialty Notebooks:
├── "Naturalistic fMRI: Clinical"     (70 clinical papers)
├── "Naturalistic fMRI: AI-Neuro"     (50 AI-focused papers)
├── "Naturalistic fMRI: Development"  (30 dev/age papers)
└── "Naturalistic fMRI: Methods"      (40 methods papers)
```

### Cross-Notebook Queries

```bash
# nlm CLI cross-query
nlm cross-notebook-query \
  --notebooks "$NB_MAIN $NB_CLINICAL $NB_AINEURO" \
  --query "Q14 — Why clinical naturalistic outperforms rest..."
```

Claude Code MCP 경유:
```python
# 각 notebook 개별 쿼리 후 manual merge
for nb_id in [nb_main, nb_clinical, nb_aineuro]:
    results.append(mcp__notebooklm__notebook_query(
        notebook_id=nb_id, query=q, timeout=180
    ))
synthesis = merge_cross_notebook(results)
```

---

## Automation Scripts

### `run_pipeline.sh` (전체 자동화)

```bash
#!/usr/bin/env bash
set -euo pipefail

# Stage 1: Search
echo "=== Stage 1: PubMed search ==="
python3 search_papers.py

# Stage 2: Download
echo "=== Stage 2: Download ==="
python3 select_and_download.py
python3 retry_failed.py

# Stage 3: Select
echo "=== Stage 3: Select top 100 ==="
python3 select_100.py

# Stage 4: Upload (requires NB_ID env)
if [[ -z "${NB_ID:-}" ]]; then
    echo "ERROR: NB_ID not set. Run: export NB_ID=<notebook_id>"
    exit 1
fi
echo "=== Stage 4: NotebookLM upload ==="
NOTEBOOK_ID="$NB_ID" bash upload_to_nlm.sh

echo "=== Done! Notebook ID: $NB_ID ==="
echo "Next: run queries via Claude Code or nlm CLI"
```

### `run_queries.sh` (20개 쿼리 batch)

```bash
#!/usr/bin/env bash
QUERIES_FILE="docs/04-queries.txt"   # plain text, one query per line

while IFS= read -r query; do
    qid=$(echo "$query" | grep -oP 'Q\d+')
    nlm chat $NB_ID "$query" > raw/${qid}.json
    python3 save_answer.py --file raw/${qid}.json --qid "${qid:1}" --title auto
    sleep 5   # rate limit
done < "$QUERIES_FILE"
```

---

## Versioning & Releases

### Git Tags for Milestones

```bash
git tag -a v1.0 -m "Initial 100-paper corpus + 20 queries"
git push origin v1.0

# Future:
git tag -a v1.1 -m "Extended to 2027, added VR queries"
```

### Release Notes Structure

```markdown
## v1.1 (2027-04)
### Added
- 30 new papers (2027)
- 3 new VR-specific queries (Q21-Q23)

### Changed
- Top-100 selection: 35% turnover vs v1.0
- Q10 (LLM alignment) answer updated with new Gemini 2.0 alignment studies

### Deprecated
- None

### Metadata
- Total papers: 365 → 395 filtered
- NotebookLM sources: 100 → 130
- Queries: 20 → 23
```

---

## Community Contributions

### Issues / Feature Requests

Good issues:
- "Paper X (PMID 12345) missed by search"
- "Query Q15 returns too generic — suggest refinement"
- "Fix Europe PMC timeout handling for slow connections"

### Pull Requests

Welcome:
- New search queries for emerging topics
- Scripts for cross-notebook analysis
- Translation of queries to other languages
- Integration with other research tools (Zotero, Paperpile)

### Code Review Criteria

1. Scripts pass existing tests (if any)
2. Metadata JSON valid after changes
3. `answers/` files follow 3-part structure
4. README/docs updated if user-visible
5. No PDFs committed (gitignore enforced)

---

## FAQ

**Q: 쿼리 답변이 과거와 달라졌어요. 버그인가요?**
A: NotebookLM은 deterministic 아님. 동일 쿼리도 답변 variation 있음. 주요 결론은 안정적이지만 wording/citation 세부는 다를 수 있음.

**Q: 파이프라인을 Jupyter notebook으로 실행 가능?**
A: 가능. 각 Python 스크립트를 cell로 import해서 단계별 실행. 단, 스크립트 자체는 Jupyter dependency 없음 (일부러).

**Q: 다른 신경영상 모달리티 (MEG, EEG, ECoG)로 확장?**
A: 가능. `search_papers.py`에서 "fMRI" → "MEG"/"EEG" 변경. PMC OA 논문 수는 fMRI보다 적지만 여전히 확장 가능.

**Q: GPT / Claude / Gemini로 NotebookLM 대체?**
A: 이론상 가능. 하지만 citation 품질, cross-source synthesis는 NotebookLM이 specialized. Bulk context는 Gemini 1.5+ 경쟁력 있음.

**Q: 이 파이프라인을 기관 내부 private 문헌에 적용?**
A: 가능. Step 1 (PubMed search) 대신 local PDFs로 시작. `upload_to_nlm.sh`는 그대로 작동. NotebookLM Plus 프라이버시 정책 확인 필수.
