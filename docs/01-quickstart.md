# 01. Quickstart — 5분 안에 시작하기

> 이 프로젝트를 **5분 안에** 실행해보는 최단 경로. 전체 파이프라인은 1-2시간 걸리지만, 이미 만든 결과물을 바로 탐색할 수 있습니다.

---

## 옵션 A: 답변만 읽기 (0분 — 설치 불필요)

**가장 빠른 방법**: GitHub에서 [`answers/`](../answers/) 폴더의 20개 markdown 답변을 바로 읽기.

```
answers/
├── Q01_statistical_inference.md              ← Methodological
├── Q02_stimulus_standardization.md           ← Methodological
├── Q03_motion_and_artifact_handling.md       ← Methodological
├── Q04_*.md                                   ← Neural representation
├── ...
└── Q20_beyond_movies.md                      ← Frontiers
```

각 파일은 3-part 구조 (SOTA / Outstanding / AI applications) + citation 포함.

---

## 옵션 B: 메타데이터 탐색 (2분)

```bash
git clone https://github.com/Transconnectome/naturalistic_fmri.git
cd naturalistic_fmri
pip install -r requirements.txt      # requests만 필요
python3 -c "
import json
papers = json.load(open('papers_all.json'))
print(f'Total: {len(papers)} papers')
print(f'PMC available: {sum(1 for p in papers if p[\"has_pmc\"])}')

from collections import Counter
journals = Counter(p['journal'] for p in papers[:100])
for j, c in journals.most_common(10):
    print(f'{c:3d}  {j[:60]}')
"
```

---

## 옵션 C: PDF 없이 파이프라인 재현 (10분)

```bash
git clone https://github.com/Transconnectome/naturalistic_fmri.git
cd naturalistic_fmri
pip install -r requirements.txt

# 새로 PubMed 검색 (2026년 이후 논문까지 업데이트)
python3 search_papers.py
# → papers_all.json 재생성 (기존 335편 + 신규 추가)

# 기존과 비교
diff <(jq '[.[].pmid] | sort' papers_all.json) \
     <(git show HEAD:papers_all.json | jq '[.[].pmid] | sort')
```

---

## 옵션 D: PDF 다운로드 (20-30분)

```bash
# 필요: 인터넷, 디스크 500 MB 여유
python3 select_and_download.py        # ~20분 (병렬 4 workers)
python3 retry_failed.py               # ~5분 (HTTP 500 재시도)
python3 select_100.py                 # <1초 (관련성 정렬)
# → pdfs/ 폴더에 131개 PDF
```

---

## 옵션 E: 전체 NotebookLM 연동 (1-2시간, Plus 플랜 필요)

```bash
# 1. nlm CLI 설치 및 로그인
pip install notebooklm-mcp-cli
nlm login                     # 브라우저 OAuth

# 2. 새 notebook 생성 후 ID 획득
nlm notebook create "Naturalistic fMRI (my copy)"
# → UUID 반환 (예: abc123...). upload_to_nlm.sh의 NOTEBOOK_ID 변수에 설정

# 3. 업로드
bash upload_to_nlm.sh           # ~5-10분, 4 병렬

# 4. 쿼리 실행 (docs/04-queries.md의 20개 쿼리 사용)
# Claude Code MCP 또는 nlm chat으로
```

자세한 NotebookLM 가이드: [`03-notebooklm-guide.md`](03-notebooklm-guide.md)

---

## 다음 단계

1. **[02-pipeline.md](02-pipeline.md)** — 파이프라인 기술 해설 (NCBI PoW 우회, Europe PMC, 관련성 스코어링)
2. **[03-notebooklm-guide.md](03-notebooklm-guide.md)** — NotebookLM 설정 + MCP + CLI + 쿼리 실행
3. **[04-queries.md](04-queries.md)** — 20개 쿼리 전문 + 7-카테고리 설계 근거
4. **[05-reproducibility.md](05-reproducibility.md)** — 처음부터 완전 재현
5. **[06-extending.md](06-extending.md)** — 논문/쿼리 추가 워크플로

---

## 자주 막히는 곳

| 증상 | 원인 | 해결 |
|------|------|------|
| `ModuleNotFoundError: requests` | Python deps 미설치 | `pip install -r requirements.txt` |
| PMC URL이 HTML 반환 | NCBI PoW 챌린지 | 이미 Europe PMC 사용 중 (코드 확인) |
| `nlm: command not found` | CLI 미설치 | `pip install notebooklm-mcp-cli` |
| `nlm login` OAuth 실패 | 방화벽/프록시 | `nlm login --device-code` 사용 |
| NotebookLM 소스 50개 한도 | Free 플랜 | Plus 업그레이드 또는 50편으로 스케일 다운 |
| `gh: not authenticated` | GitHub CLI 로그인 필요 | `gh auth login` |

문제 해결 상세: [`02-pipeline.md`](02-pipeline.md#troubleshooting)
