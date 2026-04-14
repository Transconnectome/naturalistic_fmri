# 03. NotebookLM 연동 가이드

**이 프로젝트의 가장 중요한 부분**: Google NotebookLM을 research synthesis 엔진으로 활용하는 상세 가이드.

---

## NotebookLM이란?

[Google NotebookLM](https://notebooklm.google.com)은 사용자가 업로드한 문서(PDF, URL, Google Drive, 텍스트)를 기반으로 **source-grounded 대화**를 제공하는 AI 도구.

### 전통적 LLM 대비 장점

| 기능 | ChatGPT/Claude | NotebookLM |
|------|----------------|------------|
| Citation | 간헐적, hallucination 위험 | **항상** source chunks 연결 |
| 문맥 | ~200K tokens | 노트북 전체 (실질적 unlimited) |
| 전용성 | 일반 지식 | 업로드한 자료에만 grounded |
| Multi-source synthesis | 가능하지만 검증 어려움 | 자동 cross-reference |
| 공유 | 불가 (세션 내부) | 노트북 링크 공유 가능 |

### 플랜별 한도

| 플랜 | 노트북 | 소스/노트북 | 쿼리/일 |
|------|--------|-------------|---------|
| Free | 100 | 50 | 50 |
| Plus (Google AI Premium) | 100 | 300 | 500 |
| Enterprise | 무제한 | 600+ | 무제한 |

이 프로젝트는 **100 sources × 1 notebook** = Plus 플랜 충분.

---

## 이 프로젝트의 NotebookLM 사용법

### 접근 방식 3가지

#### 방식 1: Web UI (수동 탐색)

1. https://notebooklm.google.com 접속
2. 노트북 생성 → "+ Add source" → PDF 드래그 앤 드롭
3. 좌측 sources 목록 확인, 우측 chat 입력
4. 쿼리 후 citation 클릭 → 원 논문 구절 확인

**장점**: UI로 직관적 탐색, citation 시각화
**단점**: 100개 PDF 수동 업로드는 현실적으로 불가능

#### 방식 2: `nlm` CLI (자동화)

```bash
# 설치
pip install notebooklm-mcp-cli

# 인증 (브라우저 OAuth 한 번)
nlm login

# 노트북 생성
nlm notebook create "Naturalistic fMRI 2021-2026" --description "100 top-tier papers"
# → 반환된 UUID 복사 (예: d9265824-3383-4fd4-8d17-03512a338ee5)

# 단일 소스 추가
nlm source add <notebook_id> --file paper.pdf

# Bulk 업로드 (이 repo의 upload_to_nlm.sh 활용)
bash upload_to_nlm.sh

# 쿼리
nlm chat <notebook_id> "Q10 — LLM-Brain Alignment: ..."

# 노트북 관리
nlm notebook list
nlm notebook get <id>
nlm notebook delete <id>
```

**장점**: 스크립트 가능, headless 환경 OK
**단점**: 세밀한 UI 탐색 불가

#### 방식 3: MCP (Claude Code 통합, **권장**)

Claude Code 안에서 MCP 프로토콜로 직접 호출:

```python
# Tool 로드 (한 번만)
ToolSearch(query="select:mcp__notebooklm__notebook_query,mcp__notebooklm__source_add,mcp__notebooklm__chat_configure", max_results=5)

# 노트북 생성
mcp__notebooklm__notebook_create(title="My Research Notebook")
# → returns {notebook_id: "...", url: "..."}

# 소스 추가 (URL/file/text/drive)
mcp__notebooklm__source_add(
    notebook_id="...",
    source_type="file",
    file_path="/path/to/paper.pdf"
)

# 쿼리
mcp__notebooklm__notebook_query(
    notebook_id="...",
    query="Q10 — ...",
    timeout=180
)
# → returns {answer, sources_used, citations, references}

# 응답 길이 조정
mcp__notebooklm__chat_configure(
    notebook_id="...",
    response_length="longer"   # default | longer | shorter
)
```

**장점**: 대화 흐름 자연스러움, 에이전트 통합
**단점**: Claude Code 내부에서만 사용 가능

---

## 이 프로젝트의 Notebook 현황

- **제목**: "Naturalistic fMRI Literature 2021-2026 (100 papers)"
- **ID**: `d9265824-3383-4fd4-8d17-03512a338ee5`
- **소스 수**: 101 (100 PDF + 1 기본 메모)
- **생성일**: 2026-04-14
- **소유자**: SNU Connectome Lab (snuconnectome)
- **공개 상태**: Private (재현 시 자신의 notebook 생성 권장)

---

## 자신의 NotebookLM 재현

### 단계별 가이드

#### Step 1: NotebookLM Plus 구독 확인

100+ sources는 Plus 필요 (월 $19.99 / ₩26,900). 구독 링크: https://notebooklm.google.com/pricing

#### Step 2: nlm CLI 설치 + 로그인

```bash
pip install notebooklm-mcp-cli
nlm login
# → 브라우저 OAuth 진행

# 또는 device-code (headless)
nlm login --device-code
```

토큰 저장 위치: `~/.nlm/profiles/default/tokens.json` (gitignore 필수)

#### Step 3: 노트북 생성

```bash
nlm notebook create "Naturalistic fMRI (my copy) 2021-2026"
# → UUID 출력됨 (예: abc-123-...)

# 환경변수로 저장 (편의)
export NB_ID="abc-123-..."
```

#### Step 4: PDF 확보

Option A: repo에서 PDF 직접 다운로드 (unicore가 제공 안 함 — 저작권 이유로)
```bash
# 이 repo에는 PDFs 포함 안 됨 (gitignore). 직접 다운로드:
python3 select_and_download.py       # Europe PMC 경유
python3 retry_failed.py              # 실패 재시도
```

Option B: 자신의 관련 PDF 모음 사용
```bash
cp -r /path/to/my/pdfs/ /home/juke/naturalistic_fmri_pdfs/pdfs/
```

#### Step 5: 업로드

`upload_to_nlm.sh` 에서 `NOTEBOOK_ID` 변수를 자신의 `$NB_ID`로 수정 후:
```bash
bash upload_to_nlm.sh
# 또는 동적:
NOTEBOOK_ID="$NB_ID" bash upload_to_nlm.sh
```

업로드 모니터링:
```bash
# 실시간 카운트
watch -n 5 'wc -l upload.log'

# 노트북 소스 수 확인
nlm notebook get $NB_ID
```

#### Step 6: 쿼리 실행

```bash
# 20개 쿼리 모두 실행 (docs/04-queries.md 참조)
while IFS= read -r query; do
    nlm chat $NB_ID "$query" > answers/raw_$(date +%s).txt
done < queries.txt
```

또는 Claude Code MCP 경유 (한 번에 여러 쿼리 병렬):
```python
# 5개씩 병렬 실행
for batch in chunks(queries, 5):
    for q in batch:
        mcp__notebooklm__notebook_query(notebook_id=nb_id, query=q, timeout=180)
```

---

## 쿼리 설계 철학

### 3-Part Structure (이 repo의 표준)

모든 쿼리는 다음 3부분 구조를 따름:

```
Q## — [Title]: [Context-setting sentence about corpus theme]

(a) SOTA: What does the corpus reveal about [specific phenomenon]?
    [Optional: specific papers/methods to probe]

(b) Outstanding: What remains unresolved — [dimension A] vs. [dimension B]?
    [Optional: productive tensions to surface]

(c) AI angle: How can [specific AI approach] address [specific limitation]?
    [Optional: concrete example of AI intervention]

Synthesize across multiple papers with citations.
```

### 왜 이 구조인가?

- **(a)**는 NotebookLM의 강점인 **source-grounded synthesis** 유도. "corpus reveals" 프롬프트가 citation-heavy 답변 생성.
- **(b)**는 multiple papers 간 **productive tensions** 드러냄. 단일 consensus가 아닌 debate 탐구.
- **(c)**는 **forward-looking speculation** 허용하되 corpus 기반으로 제약. 순수 hallucination 방지.

### 쿼리 최적화 팁

1. **카테고리 태깅**: `Q10 — LLM-Brain Alignment` — NotebookLM이 관련 소스 우선 로드
2. **구체적 저자/년도 언급**: "Caucheteux 2023", "Hasson 2008" — 논문 매칭 정확도 상승
3. **Symmetric sub-parts**: (a)/(b)/(c) 모두 비슷한 깊이 요구 — 답변 균형
4. **Citation 명시 요구**: "Synthesize with citations" 마지막에 → reference 섹션 생성

### Corpus-Out-of-Scope 감지

NotebookLM은 corpus에 없는 내용은 **명시적으로 거부**:

```
"While the provided sources offer rich insights into [X], they do not contain 
specific papers you referenced by [Y] (2024). However, the corpus does include..."
```

이 경고문이 나오면:
- 참고문헌을 corpus에서 실제 포함된 것으로 수정
- 또는 외부 지식 필요 항목 제거
- 또는 답변 그대로 수용 (corpus-only에 충실)

---

## 이 repo의 답변 예시 구조

각 `answers/Q##_*.md` 파일:

```markdown
# Q##: Title

[Comprehensive answer organized by (a)/(b)/(c) sub-parts]
[Inline citations: [1], [2], [3], ... — matched to references below]

---

## References

**[1]** (src:43b9cbf0) BOLD signal decomposition...cited text from paper...

**[2]** (src:1331447d) ...

...

**Sources used:** 20 documents
- 43b9cbf0-9356-4700-9922-64658c6fff03
- 1331447d-b1f6-48af-8acf-a148293fc997
- ...
```

**Parse 구조**:
- `answer`: 3-part markdown with inline citations [N]
- `references`: list of {source_id, citation_number, cited_text}
- `sources_used`: list of source UUIDs

---

## Advanced: NotebookLM Outputs Beyond Chat

NotebookLM은 쿼리 외에도 **artifact 생성** 가능:

```bash
# Audio overview (팟캐스트 스타일 요약, 10-20분)
nlm audio create $NB_ID --prompt "Focus on AI-brain alignment (Q10, Q11)"

# Mind map
nlm mindmap create $NB_ID

# Study guide (강의 자료)
nlm studio create $NB_ID --artifact-type study_guide

# FAQ
nlm studio create $NB_ID --artifact-type faq

# Video overview (시각적 요약)
nlm video create $NB_ID

# 인포그래픽
nlm infographic create $NB_ID
```

이 프로젝트에서는 **텍스트 synthesis 중심**이지만, 교육/대중화 목적이면 audio/video 추가 활용 권장.

---

## Troubleshooting

### `nlm login` 실패

**증상**: OAuth 페이지 안 뜸, 또는 "permission denied"

**해결**:
1. `rm -rf ~/.nlm/` (토큰 완전 삭제)
2. `nlm login --browser firefox` (다른 브라우저)
3. `nlm login --device-code` (SSH/헤드리스 환경)
4. Google AI Studio / Workspace 계정 확인 — NotebookLM Plus 할당됐는지

### 업로드 중 "Unauthorized"

**해결**:
```bash
nlm login  # 재인증
# 또는
nlm doctor  # 환경 진단
```

### 쿼리 답변 짧음 (<2 KB)

**원인**: default response_length 짧거나, 쿼리가 구체성 부족

**해결**:
```python
mcp__notebooklm__chat_configure(notebook_id=nb_id, response_length="longer")
```

또는 쿼리에 "Please provide a detailed synthesis of at least 800 words" 추가.

### 쿼리 답변이 "sources do not contain..." 반환

**원인**: 코퍼스에 없는 특정 저자/연도/용어 언급

**해결**: 쿼리에서 외부 references 제거, 일반화:
- ❌ "Caucheteux 2023 showed..."
- ✅ "Recent LLM-brain alignment work has shown..."

### 100편 업로드 후 query throughput 저하

**원인**: NotebookLM indexing 지연 (일반적으로 1-10분)

**해결**: `nlm notebook get <id>`로 "processing" 상태 확인, 완료 후 쿼리.

---

## Security & Privacy

### NotebookLM의 데이터 처리

- 업로드된 PDF는 **Google Cloud**에 저장 (미국)
- 인덱싱/쿼리는 **Google Gemini 모델** 사용
- 학습 데이터로 사용 **안 함** (기본 설정 확인)
- Private notebook은 소유자만 접근 가능
- 공유 링크는 view-only (편집 권한 별도)

### 이 프로젝트의 데이터 노출 수준

- PDFs: **gitignored** — repo에 절대 포함 안 됨
- Metadata (papers_all.json): 공개 정보 (PubMed) 기반
- Answers: NotebookLM 생성, cited text 포함 → 원 논문 저작권 인용 범위
- Notebook ID: 접근 권한 없으면 무의미 (권한은 OAuth 인증 필요)

### 민감 정보 확인

```bash
# 커밋 전 필수
git diff | grep -iE "(password|secret|token|key|api)"
git log --all --oneline | grep -iE "tokens|credentials"
```

---

## 비용

### NotebookLM Plus: $19.99/month (₩26,900)

이 프로젝트 한 번 실행:
- 100 sources × 1 notebook = Plus 한도 내
- 20 queries × 1 day = Plus 한도 내
- 총 **1개월 구독** 으로 충분

### 대안 (무료)

- **50편 한도**: Free 플랜, 이 프로젝트의 절반 규모로 축소
- **MCP + 자체 LLM**: GPT-4, Claude 직접 사용 (하지만 citation 품질 저하)
- **ScholarAI / SciSpace**: 상업 대안, 일부 기능 제한

---

## 관련 리소스

- NotebookLM 공식 Help: https://support.google.com/notebooklm
- `nlm` CLI repo: https://github.com/anthropics/notebooklm-mcp-cli (예시)
- MCP 프로토콜: https://modelcontextprotocol.io
- 이 프로젝트 쿼리 전문: [`04-queries.md`](04-queries.md)
