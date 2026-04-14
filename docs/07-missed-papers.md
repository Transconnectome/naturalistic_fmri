# 07. Missed Papers Discovery (2021-2026 Deep Research)

> 원본 335편 코퍼스에 **포함되지 않은** 추가 naturalistic fMRI 논문 **604편**을 발견한 딥 리서치 결과.

---

## 핵심 결과 요약

| 지표 | 값 |
|------|-----|
| **원본 코퍼스** | 335 논문 (8 PubMed 쿼리) |
| **추가 발견** | **604 논문** (82 PubMed + 웹/preprint 100) |
| **결합 총합** | **939 논문** (원본의 2.8배) |
| **중복 제거 후** | 604 (36개 에이전트 간 중복 제거) |
| **원본 PMID와 겹침** | 0 (완벽한 보완 관계) |
| **PMC 다운로드 가능** | 374 (62%) |
| **High-priority (must-add)** | 55 |
| **Medium-priority** | 29 |

---

## 탐색 방법

### Agent A — PubMed 확장 검색 (54 → 540)

기존 8개 쿼리 → **82개로 확장**. 주요 gap 영역:

1. **방법론**: ISFC, SRM, hyperalignment, encoding models, 7T naturalistic
2. **주제**: VR/immersive, video games, music listening, hyperscanning
3. **모달리티**: EEG-fMRI concurrent, MEG-fMRI
4. **이론**: predictive coding + naturalistic, free energy, active inference
5. **인구**: 영유아 naturalistic, 노화, 임상 서브타입
6. **테마**: Theory of mind + movie, empathy + naturalistic
7. **종간**: 마모셋/마카크 naturalistic 특화
8. **저널 확장**: Neuropsychologia, Frontiers in Neuroscience, Scientific Data, Scientific Reports, SCAN, Mol Psychiatry 등

**결과**: 2,684 raw hits → 540 strictly filtered papers

### Agent B — 웹/Preprint 탐색 (100)

PubMed이 놓친 영역:
- **bioRxiv/medRxiv** preprints (26)
- **arXiv** ML 논문 (20)
- **Conference proceedings** (NeurIPS, CCN, ICLR, Algonauts 2025) (10)
- **Recent high-tier** (Nat Commun, Neuron, eLife Dec 2024 - Apr 2026) (27)
- **Scientific Data** 데이터셋 논문 (7)

---

## 연도 분포

| Year | Original 335 | Missed 604 | Total 939 |
|------|--------------|------------|-----------|
| 2026 | 21 | 62 | 83 |
| 2025 | 75 | 163 | 238 |
| 2024 | 65 | 99 | 164 |
| 2023 | 59 | 84 | 143 |
| 2022 | 59 | 105 | 164 |
| 2021 | 56 | 91 | 147 |

**관찰**: 2025년이 가장 활발 (238편/년). 2022-2024년 상대적으로 일정. Missed papers가 특히 2025-2026년에 많음 (최신성 + PubMed 인덱싱 지연 반영).

---

## 발견된 주요 저널 (누락 분석)

### 대폭 확장된 저널 (원본 + 누락)

| 저널 | Original | Missed | Total |
|------|----------|--------|-------|
| NeuroImage | 59 | 43 | 102 |
| Cerebral Cortex | 33 | 15 | 48 |
| Human Brain Mapping | 27 | 12 | 39 |
| Imaging Neuroscience | 26 | 9 | 35 |
| Nature Communications | 13 | 13 | 26 |
| J Neuroscience | 18 | 16 | 34 |
| eLife | 22 | ~5 | 27 |

### 원본에 없었지만 누락에서 대폭 발견

| 저널 | Missed | 의미 |
|------|--------|------|
| **Scientific Data** | 23 | **데이터셋 논문** — 원본 코퍼스 완전히 놓침 |
| **Frontiers in Neuroscience** | 23 | Open access, mid-tier 활발 |
| **Scientific Reports** | 22 | 다양한 분야, 정량 연구 |
| **bioRxiv** | 21 | Preprint, 2024-2026 최신 |
| **Neuropsychologia** | 19 | 전통 신경심리학, 종종 놓침 |
| **SCAN** (Social Cognitive and Affective Neuroscience) | 18 | 사회 naturalistic 강세 |
| **Frontiers in Psychiatry** | 17 | 정신의학 적용 |
| **Frontiers in Human Neuroscience** | 14 | 영상/행동 결합 |
| **arXiv** | 14 | ML + brain papers |
| **PLoS ONE** | 13 | Broad OA |
| **Developmental Cognitive Neuroscience** | 8 | 발달 특화 |

**핵심 인사이트**: 원본 필터가 "Brain sciences"(MDPI)는 제외했지만, **Scientific Data와 Frontiers 계열을 놓친 것이 큰 gap**. 그러나 Scientific Data의 데이터셋 논문은 naturalistic fMRI 분야에 매우 중요.

---

## Top 10 MUST-ADD Papers (Web Agent 선정)

1. **Algonauts 2025 winner — TRIBE: TRImodal Brain Encoder** (Meta FAIR, arXiv 2507.22229)
   - SOTA naturalistic fMRI 예측. CNeuroMod 80h/피험자 학습. 263개 팀 제압.

2. **Rajimehr et al. — Functional architecture of cerebral cortex during naturalistic movie watching** (Neuron 2024)
   - 랜드마크 176명 × 60분 영화로 24개 기능 영역 매핑

3. **CineBrain — Large-Scale Multi-Modal Brain Dataset during Naturalistic Audiovisual Narrative** (arXiv 2503.06940)
   - 첫 대규모 동시 EEG+fMRI (Big Bang Theory, ~6h/참여자)

4. **Emo-FilM: Multimodal dataset for affective neuroscience** (Scientific Data 2025)
   - 14 영화, 50 감정 annotation, 30 fMRI 참여자, full physiology

5. **Movie-watching evokes ripple-like activity within events** (Nature Communications 2025)
   - iEEG ripples from 10 epilepsy patients — event segmentation 결정적 증거

6. **Between-movie variability severely limits generalizability** (bioRxiv 2024.12.03)
   - 112명 × 8 영화 ISC 변동성 — 중요한 방법론적 경고

7. **Spacetop — unifying naturalistic processes dataset** (Scientific Data 2025)
   - N=101, 6h/참여자, 2h naturalistic + 6 task

8. **Le Petit Prince multi-talker 7T fMRI+EEG** (Scientific Data 2025)
   - First 7T multi-talker naturalistic dataset

9. **BABA — Chinese reality TV naturalistic fMRI+MEG** (Scientific Data 2025)
   - 부모-자녀 dyads, overlapping speech, 비영어 코퍼스

10. **Hasson Lab 2025 trio**:
    - "Unified Acoustic-to-Speech-to-Language Embedding Space" (Nat Hum Behav)
    - "Incremental Accumulation of Linguistic Context" (Nat Commun)
    - "Uncovering a Timescale Hierarchy" (J Neurosci)

---

## Most Productive Labs (2024-2026, 누락된 작업 포함)

| Lab / PI | 기관 | 주요 기여 |
|----------|------|-----------|
| **Uri Hasson** | Princeton | LLM-brain alignment, 대화, 4+ papers |
| **Ken Norman** | Princeton | 음악 reactivation, LLM event segmentation |
| **Janice Chen** | Johns Hopkins | Naturalistic memory, reinstatement |
| **Chris Baldassano** | Columbia | Ripple activity, HMM events |
| **Alex Huth** | UT Austin | Occipital-temporal tuning, LLM QA encoding |
| **Ev Fedorenko** | MIT | Language predictive coding naturalistic |
| **Emily Finn** | Dartmouth | DMN evolving stories |
| **Mariam Aly** | Columbia | Precision fMRI, naturalistic memory |
| **Jack Gallant** | Berkeley | Semantic encoding, task-dependent (2026) |
| **Meta FAIR** | Industry | TRIBE brain encoding SOTA |
| **Courtois NeuroMod** | Montreal | 200h 개인 데이터, THINGS |
| **Liad Mudrik** | Tel Aviv | 생태학적 의식 |
| **Yaara Yeshurun** | Tel Aviv | Narrative + ISC, shared belief |
| **Kanwisher lab** | MIT | Navigational affordances |

---

## 주요 테마별 Missed Papers

### A. 방법론 확장 (누락 대폭)
- **VR/Immersive** (75편): VR in-scanner 프로토콜, AR, 360° 영상
- **Encoding models / DNN-LLM** (54편): V-JEPA2, Whisper, Qwen2.5-Omni brain prediction
- **Video games** (54편): 첫 active task naturalistic (영화는 수동)
- **Hyperscanning/Dyadic** (39편): 두 명 동시 스캔
- **Multimodal datasets** (25+편): Scientific Data 2025 release 대량

### B. 신경 표상
- **Event segmentation in infants** (중요, 원본 누락)
- **Ripple activity during movies** (iEEG)
- **Timescale hierarchy** (Hasson 2025 확장)

### C. 임상
- **Depression + naturalistic** (multi-echo, translational psychiatry)
- **Autism + movie** (preregistered replication 누락)
- **fMRI-guided TMS** + naturalistic
- **DOC (disorders of consciousness)** clinical implementation

### D. AI-Neuro
- **Algonauts 2025 multimodal** (5+ dedicated papers)
- **Cross-subject decoding**, Friends data brain-tuning
- **Brain foundation model candidates**

---

## 재현 도구

### Agent A 결과 재현

```bash
python3 search_extended.py
# → 82 queries, ~30 min
# → papers_missed_pubmed.json (540 papers)
```

### Agent B 결과 재현

Web-based 이므로 비확정적. 주요 경로:
- bioRxiv RSS/search: https://www.biorxiv.org
- Google Scholar (via Tavily)
- Nature.com / nature.com/ncomms TOC
- arXiv cs.NE / q-bio.NC
- Author websites (Hasson, Norman, Chen, etc.)

### 병합 재현

```bash
python3 merge_missed.py
# → papers_missed.json (604 papers)
# → 통계 출력
```

---

## 다음 단계

이 604편을 어떻게 활용할 것인가?

### Option 1: Top 100 선별해서 NotebookLM 확장
```bash
# 우선순위: high-priority web papers + PMC-available PubMed papers
# 추가 NotebookLM 노트북 생성 또는 기존에 병합
```

### Option 2: 분류별로 별도 노트북 생성
- Notebook 1: "Naturalistic fMRI Methods" (VR, encoding, DNN)
- Notebook 2: "Naturalistic fMRI Clinical" (depression, autism, DOC)
- Notebook 3: "Naturalistic fMRI Datasets" (Scientific Data papers)

### Option 3: 전체 939편 통합 메가 코퍼스
- NotebookLM Enterprise 한도 (600+) 활용
- 또는 분할해서 cross-notebook query

### Option 4: Research Agenda Writing
- 604편 + 335편 = 939편 기반 포괄적 review paper 작성
- Meta-analysis of convergent findings
- Priority research gap identification

---

## 방법론적 교훈

1. **8 쿼리는 부족**: 82 쿼리로 확장 시 1.6배 발견. Exhaustive coverage는 50+ 쿼리 필요.
2. **PubMed만으로는 부족**: 웹/preprint에서 100편 추가 (특히 최신 6개월 + 데이터셋 + ML)
3. **Scientific Data 간과 금지**: 데이터셋 논문은 분야 infrastructure
4. **Preprint 포함 필수**: 2024-2026 최신 동향 (Hasson lab 등 주요 연구진)
5. **Conference papers (NeurIPS, CCN)**: ML/brain encoding 분야 핵심
6. **Journal whitelist 확대 필요**: Frontiers, SCAN, Developmental CN 등 중위 저널에도 핵심 논문 다수

---

## 파일

- `papers_missed_pubmed.json` — Agent A 출력 (540, 구조화)
- `papers_missed_web.json` — Agent B 출력 (100, 우선순위 포함)
- `papers_missed.json` — 병합 + 중복 제거 (604, unified schema)
- `search_extended.py` — Agent A 재현 스크립트 (82 쿼리)
- `merge_missed.py` — 병합/dedup 스크립트
- `missed_papers_report.md` — Agent A 원본 리포트

---

*Generated via 2-agent parallel deep research. Agent A: general-purpose (PubMed scripting). Agent B: deep-research-agent (web/preprint discovery). Total duration: ~30 min each, parallel execution.*
