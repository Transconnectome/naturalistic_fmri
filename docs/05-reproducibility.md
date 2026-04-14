# 05. Reproducibility — 처음부터 완전 재현

이 프로젝트를 **zero state**에서 완전히 재현하는 상세 가이드.

---

## Reproducibility Levels

| Level | What you reproduce | Time | Requirements |
|-------|-------------------|------|--------------|
| **L0** | Read answers | 0 min | GitHub access |
| **L1** | Metadata exploration | 5 min | Python 3.10+, 50 MB |
| **L2** | PDF download + selection | 30 min | + 500 MB disk, internet |
| **L3** | NotebookLM upload | +15 min | + nlm CLI, NotebookLM Plus |
| **L4** | Query execution | +30 min | + Claude Code or nlm CLI |
| **L5** | Full synthesis | +2-4 hr | + Expert judgment |

---

## L0: Read-Only Reproduction

아무것도 설치하지 않고 결과물 확인:

- GitHub 웹에서 [`answers/`](../answers/) 폴더 탐색
- `papers_all.json` raw 보기: https://github.com/Transconnectome/naturalistic_fmri/blob/main/papers_all.json
- (추후) `wisdom_synthesis.md` 확인

---

## L1: Metadata Exploration

```bash
git clone https://github.com/Transconnectome/naturalistic_fmri.git
cd naturalistic_fmri
pip install -r requirements.txt
```

### 기본 통계

```python
import json
papers = json.load(open('papers_all.json'))
print(f"Total filtered papers: {len(papers)}")
# → 335

from collections import Counter
years = Counter(p['year'] for p in papers if p.get('year'))
print(sorted(years.items(), reverse=True)[:8])
# → [('2025', 67), ('2024', 63), ('2023', 56), ...]

journals = Counter(p['journal'] for p in papers if p.get('journal'))
for j, c in journals.most_common(10):
    print(f"{c:3d}  {j[:60]}")
```

### Top 100 선별 재현

```bash
python3 select_100.py
# → top100_paths.json 재생성
# 원본과 동일한 100개 선별 (deterministic)

diff top100_paths.json <(git show HEAD:top100_paths.json)
# → 차이 없음
```

### 제목 키워드 분석

```python
import json, re
papers = json.load(open('papers_all.json'))
titles = [p['title'].lower() for p in papers]
for kw in ['naturalistic', 'movie', 'narrative', 'isc', 'hmm', 'llm']:
    count = sum(1 for t in titles if kw in t)
    print(f"{kw}: {count}")
```

---

## L2: PDF Download

### 요구사항

- 디스크: 500 MB 여유 (130+ PDFs, ~3 MB 평균)
- 시간: 20-30분 (네트워크 속도 의존)
- 네트워크: Europe PMC (europepmc.org) 접근 가능

### 실행

```bash
# Step 1: 검색 (선택사항 — papers_all.json 이미 있음)
python3 search_papers.py
# → 780 PMID 수집, 335 필터링, papers_all.json 저장

# Step 2: 다운로드
python3 select_and_download.py
# → pdfs/ 폴더에 ~78-120 PDFs

# Step 3: 실패 재시도
python3 retry_failed.py
# → pdfs/ 폴더 추가 ~30-50 PDFs (총 ~131)

# Step 4: 관련성 선별
python3 select_100.py
# → top100_paths.json 생성 (점수 기반 상위 100개)
```

### 예상 결과

```
pdfs/ 폴더: 131 PDF 파일, 약 350 MB
download_manifest.json: 120 시도, ~100 성공
retry_manifest.json: 200 시도, ~131 성공
top100_paths.json: 선별된 100개 경로
```

### 성공률 변동

네트워크/시간에 따라 ±5편 변동 가능. 131편 ±5 = 126-136편 정상 범위.

### Troubleshooting

```bash
# Europe PMC 접근 확인
curl -I "https://europepmc.org/articles/PMC12120555?pdf=render"
# → HTTP/1.1 302 Found

# 특정 PMID 재시도
python3 -c "
from select_and_download import download_pdf
paper = {'pmc_id': 'PMC12120555', 'pmid': '123', 'year': '2025', 'title': 'test', 'authors': []}
print(download_pdf(paper, 1))
"
```

---

## L3: NotebookLM Upload

### 사전 준비

1. **NotebookLM Plus 구독**: 월 $19.99
2. **nlm CLI 설치**:
   ```bash
   pip install notebooklm-mcp-cli
   ```
3. **OAuth 로그인**:
   ```bash
   nlm login
   # → 브라우저 열림, Google 계정 인증
   ```

### 실행

```bash
# Step 1: 새 노트북 생성
NB_ID=$(nlm notebook create "Naturalistic fMRI (reproduced)" | grep -oP 'UUID: \K[a-f0-9-]+')
echo "Notebook ID: $NB_ID"

# Step 2: upload_to_nlm.sh의 NOTEBOOK_ID 수정
sed -i "s/NOTEBOOK_ID=\".*\"/NOTEBOOK_ID=\"$NB_ID\"/" upload_to_nlm.sh

# Step 3: 업로드 (약 5-10분)
bash upload_to_nlm.sh

# Step 4: 검증
nlm notebook get $NB_ID
# → source_count: 101 (100 PDF + 1 default)
```

### 예상 결과

- `upload.log`: 100/100 lines (성공)
- `upload_fail.log`: 0 lines
- NotebookLM web UI (https://notebooklm.google.com)에서 노트북 확인 가능

---

## L4: Query Execution

### MCP (Claude Code) 방식

```python
# 쿼리 로드
queries = load_from_docs("docs/04-queries.md")  # 20 queries

# 병렬 실행
for batch in chunks(queries, 5):
    results = [
        mcp__notebooklm__notebook_query(
            notebook_id=NB_ID,
            query=q,
            timeout=180
        )
        for q in batch
    ]
    for q_id, result in zip(batch_ids, results):
        save_answer(result, qid=q_id, title=q.title_slug())
```

### CLI 방식

```bash
while IFS= read -r query; do
    qid=$(echo "$query" | grep -oP 'Q\d+')
    nlm chat $NB_ID "$query" > raw_responses/${qid}.json
done < queries.txt

# Parse to markdown
for f in raw_responses/*.json; do
    qid=$(basename "$f" .json)
    python3 save_answer.py --file "$f" --qid "${qid:1}" --title auto
done
```

### 예상 결과

- `answers/Q01-Q20_*.md`: 20 markdown files
- 각 파일 5-15 KB
- Citations 평균 30+ per query
- Sources used 평균 20+ per query

### 답변 품질 변동

같은 질문도 시간에 따라 약간 다른 답변. Deterministic 아님.
**하지만**: 주요 결론 (SOTA 합의 영역)은 안정적. 다르면 대체로 wording 차이.

---

## L5: Full Synthesis

현재 `wisdom_synthesis.md` 작성 중. 완료 시 여기에 프로세스 문서화.

### Synthesis Template (제안)

```markdown
# Wisdom Synthesis — Naturalistic fMRI 2021-2026

## Executive Summary (1-page)
[Cross-category 주요 발견]

## Cross-Cutting Themes
[AI 통합, ecological validity, reproducibility]

## A. Methodological Foundations
### SOTA Consensus
### Outstanding Questions
### AI Opportunities
### Key Citations
## B-G: (동일 구조)

## Research Priorities Matrix
[urgency × tractability × impact]

## Citation Index
[topic 기반 grouping]
```

---

## Deterministic vs Non-Deterministic Elements

### Deterministic (항상 동일 결과)

- `search_papers.py`: PubMed 검색 → PMIDs (특정 시점 기준, 메타데이터 업데이트 없으면)
- `select_100.py`: 점수 기반 정렬
- `save_answer.py`: JSON → markdown 변환

### Non-Deterministic (시간에 따라 변동)

- PubMed 결과: 새 논문 인덱싱으로 papers_all.json 변경 가능
- Europe PMC 다운로드: 간헐적 HTTP 500 → 재시도 필요
- NotebookLM 답변: 같은 쿼리도 다른 세부 표현

### Reproducibility 검증

```bash
# Metadata diff
diff <(jq '[.[].pmid] | sort | .[]' papers_all.json) \
     <(git show HEAD:papers_all.json | jq '[.[].pmid] | sort | .[]')
# → 새 논문 포함 시 다름 (정상)

# PDF 개수
ls pdfs/*.pdf 2>/dev/null | wc -l
# → 120-140 범위 (±5 정도 변동 OK)

# Top 100 일치
diff top100_paths.json <(git show HEAD:top100_paths.json)
# → 메타데이터 업데이트 없으면 동일
```

---

## Environment Capture

### 이 프로젝트가 실행된 환경

- **OS**: Linux 6.11.0-1016-nvidia (Ubuntu-like)
- **Python**: 3.12.3
- **requests**: 2.32.5
- **nlm CLI**: 0.4.1 (pip, FastMCP 32 tools)
- **NotebookLM**: Plus plan, 2026-04
- **Claude Code**: Opus 4.6 1M context
- **Network**: Gigabit, South Korea (서울대)

### Container Recommendation

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "search_papers.py"]
```

### Conda Environment

```yaml
# environment.yml
name: naturalistic_fmri
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pip
  - pip:
    - requests>=2.32
    - notebooklm-mcp-cli>=0.4
```

---

## Verification Checklist

완전 재현 후 다음 확인:

- [ ] `papers_all.json` valid JSON, ~335 entries
- [ ] `pdfs/` 120-140 PDFs, 모두 >50 KB
- [ ] `top100_paths.json` exactly 100 paths, 모두 존재 확인
- [ ] NotebookLM notebook `source_count` = 101
- [ ] `upload.log` 100 성공 lines, `upload_fail.log` 빈 파일
- [ ] `answers/Q01-Q20_*.md` 20 files, 각 >3 KB
- [ ] Git clean: `git status` → 추적 안 된 파일 없음 (pdfs/ 제외)

---

## Next Steps

재현 후 extensions:
- 쿼리 추가: [`06-extending.md`](06-extending.md#adding-queries)
- 논문 추가: [`06-extending.md`](06-extending.md#adding-papers)
- 파이프라인 수정: [`02-pipeline.md`](02-pipeline.md)
