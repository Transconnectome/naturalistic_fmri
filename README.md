# Naturalistic fMRI Literature & Wisdom Synthesis (2021–2026)

> An AI-assisted research corpus pipeline: **100 top-tier papers** on naturalistic fMRI, **uploaded to NotebookLM**, distilled into **20 expert-level queries** across 7 systematic categories to surface **SOTA / outstanding questions / AI applications**.

[![License: MIT (code)](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Papers](https://img.shields.io/badge/papers-100-blue)](top100_paths.json)
[![NotebookLM](https://img.shields.io/badge/NotebookLM-integrated-orange)](https://notebooklm.google.com)
[![Coverage](https://img.shields.io/badge/years-2021--2026-brightgreen)](papers_all.json)

---

## 🚀 TL;DR — 5분 안에 이해하기

**무엇을**: 탑티어 저널(Nature Commun, eLife, PNAS, J Neurosci, Neuron, Cerebral Cortex, Imaging Neurosci, HBM 등)의 naturalistic fMRI 논문 **100편**을 체계적으로 수집해 Google NotebookLM에 업로드하고, 분야 **최고 전문가 관점의 20개 핵심 질문**을 쿼리해서 얻은 **지혜의 샘**(wisdom synthesis) 문서를 만드는 재현 가능한 파이프라인.

**왜**:
- 분야가 파편화되어 있음 — 300편+ 스캔 대신 100편 정수만 큐레이트
- 개별 논문보다 **구조적 종합**이 필요 — NotebookLM의 cross-source synthesis 활용
- **SOTA ↔ outstanding questions ↔ AI 기회**를 체계적으로 매핑하여 연구 방향 설정

**결과**:
- ✅ 100/100 PDF 다운로드 및 NotebookLM 업로드 성공
- ✅ 20개 전문가 쿼리 실행 완료 (각 쿼리당 3-part: SOTA / Outstanding / AI)
- ✅ 각 쿼리당 평균 20 sources used, 30+ citations
- 📝 `wisdom_synthesis.md`로 종합 정리 중

---

## ⚡ Quick Start

### 1️⃣ 클론 & 설치

```bash
git clone https://github.com/Transconnectome/naturalistic_fmri.git
cd naturalistic_fmri
pip install -r requirements.txt
```

### 2️⃣ PDF 수집 (선택사항 — 메타데이터는 이미 포함됨)

```bash
make download          # Europe PMC 경유 100여 편 PDF 자동 다운로드
# 또는 수동으로:
python3 search_papers.py          # PubMed 8개 쿼리 → 335편 필터링
python3 select_and_download.py    # PMC PDF 병렬 다운로드 (4 workers)
python3 retry_failed.py           # HTTP 500 backoff 재시도
python3 select_100.py             # 관련성 스코어 기반 top 100 선별
```

### 3️⃣ NotebookLM 연동

```bash
# 사전 요구사항: nlm CLI 설치 및 로그인 (docs/03-notebooklm-guide.md 참조)
pip install notebooklm-mcp-cli
nlm login

# 빈 notebook 생성 후 ID를 upload_to_nlm.sh에 설정, 그 다음:
bash upload_to_nlm.sh     # 100편 PDF 병렬 업로드 (4 workers)
```

### 4️⃣ 20개 전문가 쿼리 실행

```bash
# MCP 기반: Claude Code에서 mcp__notebooklm__notebook_query 호출
# 또는 CLI:
nlm chat <NOTEBOOK_ID> < docs/04-queries.md
```

### 5️⃣ 지혜의 샘 정리

답변은 `answers/Q01-Q20_*.md`로 자동 저장됨. 종합 시:
```bash
python3 synthesize.py > wisdom_synthesis.md   # (스크립트 개발 중)
```

---

## 📦 What's in This Repo

```
naturalistic_fmri/
├── README.md                     ← 이 파일
├── CLAUDE.md                     ← AI 에이전트 온보딩 가이드
├── LICENSE                       ← MIT (code only)
├── CITATION.cff                  ← 인용 방법
├── Makefile                      ← make download / make upload / make query
├── requirements.txt              ← Python 의존성
│
├── 📄 docs/                      ← 상세 문서
│   ├── 01-quickstart.md          ← 5분 온보딩
│   ├── 02-pipeline.md            ← 파이프라인 기술 해설
│   ├── 03-notebooklm-guide.md    ← NotebookLM 연동 상세 (필독!)
│   ├── 04-queries.md             ← 20개 전문가 쿼리 전문 + 설계 근거
│   ├── 05-reproducibility.md     ← 처음부터 재현하기
│   └── 06-extending.md           ← 논문/쿼리 추가하기
│
├── 🔧 Python 파이프라인
│   ├── search_papers.py          ← PubMed E-utilities 검색
│   ├── select_and_download.py    ← PMC PDF 병렬 다운로드
│   ├── retry_failed.py           ← HTTP 500 backoff 재시도
│   ├── select_100.py             ← 관련성 기반 선별
│   ├── save_answer.py            ← NotebookLM 응답 파서
│   └── upload_to_nlm.sh          ← NotebookLM 병렬 업로드
│
├── 🗃️ Metadata (JSON)
│   ├── papers_all.json           ← 335편 top-journal 필터링
│   ├── papers_top120.json        ← top 120 후보
│   ├── papers_selected.json      ← 다운로드 대상 120
│   ├── top100_paths.json         ← 선별된 top 100 경로
│   ├── download_manifest.json    ← 다운로드 결과
│   └── retry_manifest.json       ← 재시도 결과
│
├── 📝 answers/                   ← 20개 쿼리 응답 (markdown + citations)
│   ├── Q01_statistical_inference.md
│   ├── Q02_stimulus_standardization.md
│   ├── ...
│   └── Q20_beyond_movies.md
│
├── 📊 logs/                      ← 실행 로그
│   ├── upload.log
│   └── upload_fail.log
│
└── pdfs/                         ← 131 PDFs (gitignored — copyright)
```

---

## 🧠 NotebookLM 연동

이 프로젝트의 **핵심 특징**: Google NotebookLM을 research synthesis 엔진으로 활용.

### NotebookLM이란?

[Google NotebookLM](https://notebooklm.google.com)은 업로드한 문서(PDF, URL, Google Drive)를 기반으로 **source-grounded AI 대화**를 제공하는 도구. 특징:
- **Citation 기반 답변**: 모든 주장이 원 논문 구절과 연결됨
- **Cross-source synthesis**: 여러 논문에 걸친 종합 가능
- **Plus 플랜**: 300-600개 소스까지 지원 (무료는 50개)

### 연동 방법

이 repo는 **3가지 NotebookLM 접근 방식**을 지원합니다:

| 방식 | 도구 | 용도 |
|------|------|------|
| **CLI** | `nlm` (notebooklm-mcp-cli) | 초기 업로드, bulk 작업 |
| **MCP** | `mcp__notebooklm__*` | Claude Code 내에서 쿼리 실행 |
| **Web UI** | notebooklm.google.com | 수동 탐색, 쿼리 검증 |

### 이 연구의 NotebookLM 노트북

- **제목**: "Naturalistic fMRI Literature 2021-2026 (100 papers)"
- **ID**: `d9265824-3383-4fd4-8d17-03512a338ee5`
- **소스**: 100 PDF + 1 메모 = 101 sources
- **공개 여부**: 현재 private (재현 시 자신의 노트북을 생성하세요 — `make create-notebook`)

자세한 가이드: [`docs/03-notebooklm-guide.md`](docs/03-notebooklm-guide.md)

---

## 🔬 Pipeline Highlights

### 핵심 기법 #1: Europe PMC PDF Bypass

NCBI PMC는 최근 **Proof-of-Work (PoW) 챌린지**를 PDF 다운로드에 도입. 기존 `https://pmc.ncbi.nlm.nih.gov/.../pdf/` URL은 JS 렌더링 필요한 HTML만 반환.

**솔루션**: Europe PMC의 render endpoint 사용:
```python
url = f"https://europepmc.org/articles/PMC{pmc_id}?pdf=render"
# → 302 redirect → application/pdf 직접 반환, 쿠키/JS 불필요
```

이 방법으로 **131편 PDF를 평균 2.7초/편에 다운로드** 성공. (NCBI 직접 시도 시 0% 성공)

### 핵심 기법 #2: PubMed E-utilities Multi-Query Expansion

단일 쿼리로는 분야를 커버 못함. **8개의 상호 보완적 쿼리**로 780 unique PMIDs 수집:

```
Q1: naturalistic + fMRI
Q2: movie/film + fMRI
Q3: narrative/storytelling + fMRI
Q4: inter-subject correlation + fMRI
Q5: naturalistic stimuli/paradigm + fMRI
Q6: audiobook/podcast/spoken language + fMRI
Q7: naturalistic viewing/movie watching + fMRI
Q8: story listening/comprehension + fMRI
```

→ 300+ top-journal 필터링 → 131 PMC-available 다운로드 → 100 relevance-selected.

### 핵심 기법 #3: 20 Queries × 3-Part Structure

각 쿼리는 NotebookLM 최적화된 **SOTA / Outstanding / AI** 3-part 구조:

```
Q10 - LLM-Brain Alignment: Depth vs. Shallowness
(a) What does the corpus reveal about scope and strength?
(b) Shallow vs. deep alignment — current debate?
(c) What stringent tests — scaling laws, cross-family, lesions?
```

→ 쿼리 하나당 평균 **20 sources used, 30+ citations**, 5-12 KB 답변.

---

## 📊 Results Snapshot

### Corpus Coverage (100 papers, 2021–2026)

| Year | Papers |
|------|--------|
| 2026 | 6      |
| 2025 | 40     |
| 2024 | 27     |
| 2023 | 14     |
| 2022 | 7      |
| 2021 | 6      |

### Top Represented Journals

- Imaging Neuroscience (MIT Press/OHBM) — 24
- Human Brain Mapping — 15
- Cerebral Cortex — 11
- Nature Communications — 9
- Journal of Neuroscience — 9
- eLife — 9
- Communications Biology — 7
- PNAS — 7
- Neuron — 2
- Current Biology — 1
- PLoS Biology — 1

### Dominant Research Themes (from Explore-agent analysis)

1. **Affective/Social** (~170 papers in 335-filtered) — interpersonal sync, ASD/ADHD biomarkers
2. **Inter-subject correlation/hyperalignment** (71) — 2× growth in 2025
3. **Clinical applications** (71) — autism, depression, ADHD
4. **Fingerprinting** (30) — trait × state × stimulus decomposition
5. **Event segmentation & dynamics** (20) — HMM-based, 2025 surge
6. **Developmental** (16) — infants (Ellis 2025), lifespan trajectories
7. **Cross-species** (14) — marmoset/macaque comparative, 2024-2025 growth
8. **LLM alignment** (10) — exponential growth; GPT-2, Caucheteux 2023
9. **Memory & reinstatement** (15) — hippocampal-DMN dialogue
10. **Multimodal** (15) — early cross-modal + late convergence

### Identified Gaps (motivating outstanding questions)

- **0 papers**: Computational theory grounding, VR/immersive, ethical/privacy
- **<2 papers**: Longitudinal, motion-specific artifact methods
- **<5 papers**: Real-world ambulatory, pharmacological interactions

---

## 🎯 Who Is This For?

- **Naturalistic fMRI researchers**: 2021-2026 문헌 조망, 연구 공백 발견
- **Neuro-AI researchers**: brain-LLM alignment, brain foundation models 진입점
- **Graduate students**: 분야 온보딩 (3-4주 → 3-4일로 단축)
- **Systems-level neuroscientists**: SOTA 방법론 일괄 검토
- **Clinical translation**: biomarker 파이프라인 설계 참조
- **Review paper writers**: 구조화된 citation base

---

## 🛠️ Reproducibility

이 프로젝트는 **100% 재현 가능**하게 설계되었습니다:

1. **논문 메타데이터**: `papers_all.json`에 335편 전체 PubMed 레코드 (PMID, DOI, PMC ID, title, abstract)
2. **다운로드 재현**: 스크립트 한 번 실행으로 동일 100편 확보 가능
3. **쿼리 재현**: `docs/04-queries.md`에 20개 쿼리 전문 수록
4. **답변 로그**: `answers/Q01-Q20_*.md`에 citation 포함 전체 응답
5. **파이프라인 로그**: `upload.log`, `download_manifest.json`, `retry_manifest.json`

상세: [`docs/05-reproducibility.md`](docs/05-reproducibility.md)

---

## 🤝 Contributing

### 논문 추가하기

새 쿼리/저널을 `search_papers.py`의 `QUERIES` 또는 `TOP_JOURNALS`에 추가 → 재실행 → diff 확인 → PR.

### 새 쿼리 추가하기

`docs/04-queries.md`의 7-카테고리 구조에 맞춰 3-part 쿼리 초안 → 테스트 실행 → PR.

### 응답 개선하기

`answers/` 하위 파일에 대한 cross-check, 외부 참고문헌 추가 환영.

자세한 기여 가이드: [`docs/06-extending.md`](docs/06-extending.md)

---

## 📖 Citation

이 repo나 파이프라인을 학술적으로 활용하실 경우:

```bibtex
@software{naturalistic_fmri_2026,
  author = {Cha, Jiook and {SNU Connectome Lab}},
  title = {Naturalistic fMRI Literature \& Wisdom Synthesis (2021-2026): An AI-Assisted Research Corpus with NotebookLM Integration},
  year = 2026,
  month = 4,
  url = {https://github.com/Transconnectome/naturalistic_fmri},
  organization = {Seoul National University, Department of Psychology}
}
```

상세: [`CITATION.cff`](CITATION.cff)

---

## 📜 License

- **Code (scripts, Makefile, docs)**: MIT License — see [`LICENSE`](LICENSE)
- **Paper metadata (JSON)**: PubMed/PMC 공공 도메인 정보 기반 (자유 사용)
- **PDFs**: **Gitignored** — 개별 논문은 각 발행기관 저작권. 사용자는 자신의 기관 라이선스로 다운로드해야 함
- **쿼리 응답 (answers/*.md)**: Creative Commons BY-SA 4.0 — NotebookLM 생성물, 원 논문 인용 유지 의무

---

## 🙏 Acknowledgments

- **Google NotebookLM** — source-grounded synthesis 엔진
- **Europe PMC** — reliable OA PDF delivery via `pdf=render` endpoint
- **NCBI PubMed E-utilities** — 35M+ 논문 메타데이터 무료 제공
- **notebooklm-mcp-cli** by @tbcooney — NotebookLM programmatic access
- **Claude Code (Anthropic)** — 파이프라인 구축, 쿼리 설계, 문서화 orchestration

---

## 🔗 Links

- **Repository**: https://github.com/Transconnectome/naturalistic_fmri
- **SNU Connectome Lab**: https://www.connectomelab.com
- **NotebookLM**: https://notebooklm.google.com
- **Europe PMC**: https://europepmc.org

---

## ❓ FAQ

**Q: PDF 없이도 쿼리 답변을 볼 수 있나요?**
A: 네. `answers/*.md`에 모든 응답이 citation과 함께 저장되어 있습니다. PDF는 로컬 재현 시에만 필요.

**Q: NotebookLM Plus가 필수인가요?**
A: 100+ 논문 업로드 시 필요 (무료는 50개 한도). Plus는 300개, 특정 계정은 600개까지. 50편으로 스케일 다운하면 무료로도 가능.

**Q: 한국어 쿼리가 작동하나요?**
A: NotebookLM은 다국어 지원. 하지만 코퍼스가 영어이므로 **영어 쿼리가 더 정확**합니다. 한국어 번역은 `docs/04-queries.md`에서 참조 가능.

**Q: 왜 NCBI PMC 직접 다운로드가 실패하나요?**
A: PMC는 최근 PoW(Proof-of-Work) anti-bot을 도입. 해결책: Europe PMC render endpoint — `docs/02-pipeline.md` 참조.

**Q: 파이프라인을 다른 분야에 쓸 수 있나요?**
A: 네. `search_papers.py`의 `QUERIES`와 `TOP_JOURNALS`만 수정하면 됩니다. 예시: `docs/06-extending.md`.

---

🧠 Built with **ultrathink** by SNU Connectome Lab | 2026
