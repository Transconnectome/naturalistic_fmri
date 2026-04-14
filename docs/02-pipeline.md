# 02. Pipeline — 기술적 심화 해설

파이프라인 전체 아키텍처와 각 단계의 핵심 결정/트릭을 해설합니다.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│  Stage 1: Discovery    │  Stage 2: Retrieval   │  Stage 3: Curation │
│                        │                        │                     │
│  ┌───────────────┐    │  ┌───────────────┐    │  ┌──────────────┐  │
│  │ PubMed       │    │  │ Europe PMC    │    │  │ Relevance    │  │
│  │ E-utilities  │ ─▶ │  │ render URL    │ ─▶ │  │ scoring      │  │
│  │ (8 queries)  │    │  │ (PDF fetch)   │    │  │ (title-based)│  │
│  └───────────────┘    │  └───────────────┘    │  └──────────────┘  │
│        780 PMIDs      │      131 PDFs          │      Top 100       │
│        335 filtered   │                        │                     │
└──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│  Stage 4: NotebookLM   │  Stage 5: Query       │  Stage 6: Synthesis│
│                        │                        │                     │
│  ┌───────────────┐    │  ┌───────────────┐    │  ┌──────────────┐  │
│  │ nlm CLI      │    │  │ 20 queries    │    │  │ Wisdom       │  │
│  │ bulk upload  │ ─▶ │  │ via MCP/CLI   │ ─▶ │  │ synthesis    │  │
│  │ (4 parallel) │    │  │ (3-part)      │    │  │ (7 categories)│  │
│  └───────────────┘    │  └───────────────┘    │  └──────────────┘  │
│   100 sources in      │   answers/*.md         │  wisdom_synthesis  │
│   notebook            │   (citations preserved)│  .md               │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Discovery — PubMed Multi-Query

### Design Decision: Why 8 queries, not 1?

단일 쿼리는 recall이 나쁨. Naturalistic fMRI는 여러 서브필드의 교집합:
- "naturalistic" 키워드 (일반)
- Stimulus type (movie, narrative, audiobook)
- Methodology (ISC, movie-watching)
- Application (story comprehension, event segmentation)

**해결**: 의도적으로 overlapping한 8개 쿼리로 union 수집 → 780 unique PMIDs.

```python
QUERIES = [
    '("naturalistic") AND ("fMRI" OR "functional MRI"...)',
    '("movie" OR "film") AND ("fMRI"...)',
    '("narrative" OR "storytelling") AND ("fMRI"...)',
    '("inter-subject correlation" OR "intersubject correlation") AND ("fMRI")',
    '("naturalistic stimuli" OR "naturalistic paradigm") AND ("fMRI" OR "brain")',
    '("audiobook" OR "podcast" OR "spoken language") AND ("fMRI")',
    '("naturalistic viewing" OR "movie watching") AND ("fMRI" OR "brain")',
    '("story listening" OR "story comprehension") AND ("fMRI")',
]
```

### Top-Journal Filtering

분야 내 권위있는 저널 22개로 필터링. Partial match로 저널명 variants 흡수:
- `"The Journal of neuroscience"` ↔ `"Journal of Neuroscience"`
- `"Cerebral cortex (New York, N.Y. : 1991)"` ↔ `"Cerebral cortex"`

결과: 780 → **335** top-journal papers.

### Rate Limiting

NCBI 정책: 3 requests/second (anonymous). 이를 안전하게 아래로:

```python
time.sleep(0.4)  # 2.5 req/s, below 3 limit
```

300+ records fetch는 batch 100씩: `efetch?id=1,2,3,...,100`

---

## Stage 2: Retrieval — The Europe PMC Trick

### 🚨 Problem: NCBI PMC's Proof-of-Work Challenge

2024-2025년 NCBI는 anti-bot PoW 챌린지를 추가:

```bash
curl https://pmc.ncbi.nlm.nih.gov/articles/PMC12120555/pdf/
# → HTML with JavaScript challenge
# → No PDF without browser automation
```

원인: 상업 스크래퍼 부하 감소. 하지만 legitimate research pipeline도 막힘.

### 🎯 Solution: Europe PMC Render Endpoint

Europe PMC는 EBI/EMBL 운영 PMC 미러. PoW 없이 직접 PDF 제공:

```python
url = f"https://europepmc.org/articles/PMC{pmc_id}?pdf=render"
# → 302 redirect → https://europepmc.org/api/getPdf?pmcid=PMC{id}
# → Content-Type: application/pdf (바이너리 직접 반환)
```

**성공률**: 131/200 시도 (65%). 실패는 주로 최근 논문 (EPMC 인덱싱 지연) 또는 embargoed 상태.

### Parallel Download with Concurrency Control

```python
with ThreadPoolExecutor(max_workers=4) as ex:  # 6→4로 줄임 (Europe PMC rate limit)
    futures = {ex.submit(download_pdf, p, i): ... for i, p in enumerate(papers)}
    for fut in as_completed(futures):
        res = fut.result()
        # HTTP 500 → retry with exponential backoff
        # HTTP 404 → permanent fail (not in EPMC index)
        # application/pdf → save
```

### Retry Strategy

`retry_failed.py`는 낮은 concurrency (3 workers) + jitter:

```python
time.sleep(0.2 + random.random() * 0.5)  # 0.2-0.7s jitter
# Backoff: time.sleep(2 + attempt * 3)
# Max 3 retries per paper
```

결과: 78 → 131 (재시도로 53편 추가 획득).

---

## Stage 3: Curation — Relevance Scoring

### Title-Based Heuristic

Naturalistic fMRI 관련도를 제목 키워드로 스코어:

```python
STRONG = ["naturalistic", "movie watching", "narrative", "inter-subject", ...]  # +3
MODERATE = ["movie", "film", "story", "listening", ...]                         # +1
NEGATIVE = ["task-based", "preclinical", "rodent", ...]                         # -4
```

**Why title not abstract**: 1) 속도 (131 PDFs × abstract = 많은 처리), 2) 제목이 topic의 가장 강한 signal

### Year Tiebreaker

같은 점수면 최신 논문 우선:

```python
scored.sort(key=lambda x: (-score, -year))
```

결과 분포:
| Year | Papers |
|------|--------|
| 2026 | 6 |
| 2025 | 40 |
| 2024 | 27 |
| 2023 | 14 |
| 2022 | 7 |
| 2021 | 6 |

상위 40%가 최신 2년 — naturalistic fMRI의 **가속 성장** 반영.

---

## Stage 4: NotebookLM Upload

### Tool Chain

```
Local PDFs → nlm CLI (source add) → Google Drive buffer → NotebookLM processed source
```

### Bulk Upload Strategy

```bash
# upload_to_nlm.sh의 핵심 루프
for path in "${PATHS[@]}"; do
  nlm source add "$NOTEBOOK_ID" --file "$path" &
  (( (i+1) % 4 == 0 )) && wait     # 4개마다 wait
done
```

성공률: **100/100 (실패 0)**. 소요 시간: 약 8분.

### Rate Limit Observations

- 4 parallel: 안전
- 6 parallel: occasional throttling
- 8+ parallel: 429 errors within minutes

---

## Stage 5: Query Execution

### 3-Part Query Template

```
Q## — [Title]: [Setup referring to corpus theme]
(a) SOTA: What does corpus reveal about...?
(b) Outstanding: What remains unresolved...?
(c) AI angle: How can AI help...?
Synthesize with citations.
```

이 구조가 NotebookLM에 최적화된 이유:
- **(a)** 는 corpus-grounded 답변 유도 (citation 많이 생성됨)
- **(b)** 는 multiple sources의 tensions 드러냄
- **(c)** 는 forward-looking speculation 허용하되 corpus 기반 유지

### MCP vs CLI

| Method | Latency | Throughput | Best For |
|--------|---------|------------|----------|
| `mcp__notebooklm__notebook_query` (Claude Code) | 30-90s | 1 query | 대화형 |
| `nlm chat <id>` (CLI) | 30-90s | 1 query | 스크립트 |
| REST API (프로젝트 미사용) | 변동 | batch | production |

### Output Persistence

Large responses (>30 KB) automatically persisted:

```
tool-results/toolu_<id>.txt   ← full JSON
answers/Q##_topic.md           ← parsed markdown
```

`save_answer.py`가 이 변환 담당:
```python
# JSON → markdown with structure:
# # Q##: Title
# [answer]
# ## References [N citations with source_id + cited_text]
# ## Sources used [N source UUIDs]
```

---

## Stage 6: Synthesis

현재 진행 중 (`wisdom_synthesis.md` 작성 예정).

### Template

```markdown
# Wisdom Synthesis

## Executive Summary (1 page)
## Cross-Cutting Themes
## Category A: Methodological Foundations
  ### SOTA Consensus
  ### Outstanding Questions
  ### AI Opportunities
  ### Key Citations
## ... (B through G)
## Research Priorities Matrix (urgency × tractability × impact)
## Citation Index (grouped by topic)
```

---

## Troubleshooting

### PMC PDF 0 bytes 반환

```bash
file /tmp/test.pdf
# → "XML 1.0 document" (error page)

# 해결: Europe PMC 확인
curl -I "https://europepmc.org/articles/PMC{id}?pdf=render"
# → HTTP/1.1 302 Found → redirects to PDF
```

### NotebookLM `source_count` 미증가

```bash
nlm notebook get <id>
# → sources 목록 확인
# 처리 상태가 "indexed"인지 확인. "processing" 상태면 1-5분 대기.
```

### Query 답변 짧음 (2 KB 미만)

- NotebookLM chat_configure로 `response_length: "longer"` 설정
- 또는 쿼리 더 구체적으로 — 코퍼스에 없는 내용 요청 시 짧아짐

---

## Performance Benchmarks

측정 환경: Linux, Python 3.12, Gigabit network

| Stage | Operation | Time | Throughput |
|-------|-----------|------|------------|
| 1 | PubMed 8 queries + 780 efetch | 2-3 min | ~300 papers/min |
| 2 | PDF download (120, 4 parallel) | 8-12 min | ~10-15 PDFs/min |
| 2 | Retry (200 candidates, 3 parallel) | 10-15 min | ~15 PDFs/min |
| 3 | Top-100 selection | <1 s | N/A |
| 4 | NotebookLM upload (100, 4 parallel) | 5-10 min | ~10-20 uploads/min |
| 5 | Single query | 30-90 s | 1 query/30-90s |
| 5 | 20 queries (serial) | 15-30 min | N/A |

총 소요 (처음부터 끝까지): **약 50-80분** (synthesis 제외).

---

## Design Principles Retrospective

1. **Stdlib + requests only**: 어떤 환경에서도 실행 가능 (Conda/Docker 불필요)
2. **Fail loud, retry smart**: HTTP 500 → backoff / 404 → permanent skip
3. **Idempotent scripts**: 재실행해도 중복 작업 없음 (기존 PDF 존재 시 skip)
4. **Metadata never mutated**: JSON 파일은 regenerate만, 수동 편집 금지
5. **Citation integrity**: `save_answer.py`가 source_id 보존 → 역추적 가능
