# 04. 20 Research Queries — 전문 + 설계 근거

이 문서는 NotebookLM 코퍼스(100편 naturalistic fMRI 논문)에 실행한 **20개 전문가급 쿼리**의 전문과 설계 배경을 제공합니다.

---

## Design Philosophy

### 7 Categories (Systematic Coverage)

| Category | # Queries | Rationale |
|----------|-----------|-----------|
| **A. Methodological Foundations** | 3 | 통계적 추론, 자극 표준화, 동작/아티팩트 — 모든 결론의 신뢰성 토대 |
| **B. Neural Representation & Dynamics** | 3 | 시간 계층, 공유 vs 개별 부호, 다중 모달 — naturalistic 고유 기여 |
| **C. Memory, Events, Prediction** | 3 | 사건 분할, 기억 공고화, 예측 — 연속 경험 → 이산 표상 |
| **D. AI-Neuro Alignment** | 4 | LLM 정합, 기초 모델, 생성적 디코딩, 신경 영감 AI — 가장 빠른 성장 프런티어 |
| **E. Individual Differences & Clinical** | 3 | 임상 우위 기전, 종단 추적, 지문 해석 — 사회적 임팩트 영역 |
| **F. Developmental & Cross-Species** | 2 | 발달 궤적, 종간 정합 — naturalistic 특히 강력한 두 영역 |
| **G. Frontiers & Meta-Science** | 2 | 문화적 편향, 영화 너머 — 분야의 외연과 건전성 |

### 3-Part Query Structure

모든 쿼리는 동일한 구조:
- **(a) SOTA**: 코퍼스가 보여주는 현재 합의
- **(b) Outstanding**: 미해결 쟁점
- **(c) AI angle**: Neuro-AI가 제공하는 지렛대

---

## Category A. Methodological Foundations

### Q1 — Statistical Inference for Naturalistic Data

> How do the corpus papers infer neural representations from non-stationary, trial-free naturalistic data?
>
> (a) Dominant frameworks (ISC variants, encoding models, HMM, MVPA, information-theoretic measures) and their underlying assumptions
> (b) Statistical power limitations, generalizability challenges, multiple-comparison issues under dependent samples
> (c) AI-driven advances — counterfactual stimulus generation via foundation models, information bottleneck theory, causal representation learning
>
> Synthesize across multiple papers with specific citations.

**Why**: Naturalistic fMRI는 repeated trial이 없음 → 전통 통계 부적합. ISC/HMM 등 새로운 프레임워크 필요성과 한계.

**Answer file**: [`../answers/Q01_statistical_inference.md`](../answers/Q01_statistical_inference.md)

---

### Q2 — Stimulus Standardization and Generalizability

> The field leans heavily on a limited canon of stimuli (Sherlock, Forrest Gump, Pixar shorts like Partly Cloudy, Black Mirror episodes).
>
> (a) What evidence exists in the corpus for cross-stimulus generalization vs. stimulus-specific findings?
> (b) Standardization efforts and shared datasets — Narratives, StudyForrest, Natural Scenes Dataset, HCP 7T movies, CamCAN?
> (c) Can foundation-model embeddings (CLIP, Whisper, LLMs) enable stimulus-invariant inference — treating any naturalistic content as a sample from a "stimulus basis space"?
>
> Synthesize with citations.

**Why**: Sherlock-effect (특정 영화가 과도하게 인용됨) 극복 필요. Foundation model embeddings로 stimulus-invariant inference 가능성 탐구.

---

### Q3 — Motion, Physiology, and Artifact Handling

> Naturalistic paradigms inherently maximize head motion (laughter, startle, eye tracking) and physiological variation.
>
> (a) How do corpus papers handle head motion during movie watching, physiological noise correction, engagement-motion coupling?
> (b) Motion/physiology as pure confound vs. informative signal about engagement/arousal — current debate
> (c) Deep-learning solutions — motion-aware denoising networks, self-supervised artifact removal, real-time prospective correction
>
> Synthesize with citations.

**Why**: Naturalistic이 rest 대비 motion 낮지만 여전히 artifact. Motion을 engagement signal로 재해석 가능성.

**Answer file**: [`../answers/Q03_motion_and_artifact_handling.md`](../answers/Q03_motion_and_artifact_handling.md)

---

## Category B. Neural Representation & Dynamics

### Q4 — Temporal Receptive Windows & Cortical Hierarchy

> Hasson's temporal receptive window hierarchy posits progressively longer integration timescales from sensory to associative cortex.
>
> (a) Corpus evidence for hierarchy universality across stimulus types (narrative/music/silent film); refinements from scale-free dynamics (2025)
> (b) Hemodynamic confound vs. true neural timescale hierarchy; dissociation methods
> (c) Can state-space AI models (Mamba, transformers with learned timescale priors) recapitulate hierarchy from brain-agnostic training?
>
> Synthesize with citations.

**Why**: Temporal hierarchy는 naturalistic fMRI의 signature finding. BOLD 아티팩트 vs 실제 뇌 속성 구분 중요.

---

### Q5 — Shared vs. Idiosyncratic Neural Codes

> The tension between inter-subject correlation (ISC, capturing shared variance) and fingerprinting (capturing idiosyncratic variance) is central in naturalistic fMRI.
>
> (a) Which brain regions and computations are shared vs. idiosyncratic; how this varies by stimulus type, cognitive demand, individual
> (b) Neurobiological interpretation — hierarchical level (sensory vs. associative), feedforward vs. recurrent, universal vs. culturally-learned
> (c) How can hyperalignment-based AI embeddings and individual-level foundation models simultaneously capture shared + personal structure?
>
> Synthesize with citations.

**Why**: 집단 vs 개인의 productive tension. Hyperalignment가 두 측면 동시 포착 가능한지 검증.

**Answer file**: [`../answers/Q05_shared_vs_idiosyncratic_codes.md`](../answers/Q05_shared_vs_idiosyncratic_codes.md)

---

### Q6 — Multimodal Integration in Naturalistic Viewing

> Natural stimuli are inherently multimodal (visual + auditory + linguistic + embodied).
>
> (a) Neural binding mechanisms — convergence zones (STS), temporal synchronization, shared embedding spaces
> (b) Unresolved questions — temporal precedence of modalities, bottom-up vs. top-down binding, role of prediction
> (c) How do multimodal AI models (CLIP, Flamingo, Gemini, video-language foundation models) predict cross-modal naturalistic activity?
>
> Synthesize with citations.

**Why**: 2-branch DNN이 early cross-modal 실패 → 뇌는 V1에 acoustic info 표상. 생물학적 타당 아키텍처 필요.

---

## Category C. Memory, Events, and Prediction

### Q7 — Event Segmentation Mechanisms

> HMM-inferred event boundaries are central in the corpus but their relation to subjective/behavioral boundaries is imperfect.
>
> (a) Corpus findings on how event boundaries are computed (surprise, context change, goal shift); convergence across methods
> (b) Discrepancies with behavioral boundaries — model misspecification vs. genuine neural-behavioral divergence vs. individual variability
> (c) Can generative AI (Sora, Veo for video; LLMs for narratives) produce parametrically-controlled naturalistic stimuli for causal tests?
>
> Synthesize with citations.

**Why**: HMM event boundaries는 이론적 artifact일 가능성. Generative AI로 causal manipulation 가능.

---

### Q8 — Naturalistic Memory Encoding & Reinstatement

> The corpus shows strong hippocampal-cortical dialogue during naturalistic encoding (Kwon 2025, Chen-Cohen 2022).
>
> (a) Established mechanisms — event-boundary-triggered consolidation, continuous replay, schema integration, hippocampal-DMN coupling
> (b) Generalization across movies vs. narratives vs. real-life; mental reinstatement role
> (c) AI-based memory models (episodic memory in transformers, Hopfield associative memory, RAG architectures) informed by naturalistic fMRI
>
> Synthesize with citations.

**Why**: 연속 경험의 이산 기억 변환 메커니즘 (event boundary → consolidation) 이 AI 메모리 아키텍처에 영감.

**Answer file**: [`../answers/Q08_memory_encoding_and_reinstatement.md`](../answers/Q08_memory_encoding_and_reinstatement.md)

---

### Q9 — Predictive Processing & Naturalistic Expectation Violation

> Predictive coding is the dominant theoretical framework but naturalistic validation remains patchy.
>
> (a) Naturalistic evidence — expectation violations, surprise encoding, top-down modulation, hierarchical prediction errors, Caucheteux/King 2023-style multi-timescale predictions
> (b) Bayesian surprise vs. simpler novelty/salience — free energy vs. mutual information vs. KL divergence operationalization
> (c) LLMs with controllable surprisal (varying entropy of predicted words) to disambiguate predictive-coding mechanisms
>
> Synthesize with citations.

**Why**: Predictive coding theory는 광범위 주장. Naturalistic으로 실증적 구분 가능성 (Caucheteux 2023 layer-specific 증거).

---

## Category D. AI-Neuro Alignment

### Q10 — LLM-Brain Alignment: Depth vs. Shallowness

> LLM embeddings strongly predict cortical activity during language processing (Schrimpf 2021, Caucheteux 2023, Jain 2024).
>
> (a) Scope and strength — which brain areas, which linguistic levels (phonemic/syntactic/semantic/discourse), which model families (transformer/RNN/cognitive)
> (b) Shallow (shared statistics) vs. deep (shared computation) alignment debate
> (c) Stringent tests — scaling laws, cross-family comparisons (transformer vs. SSM/Mamba vs. cognitive), lesion experiments, counterfactual prompts
>
> Synthesize with citations.

**Why**: 분야의 가장 큰 논쟁. LLM-brain alignment가 우연한 통계 아닌 실제 계산 공유인지 stringent test 필요.

---

### Q11 — Foundation Models for Naturalistic Brain Activity

> Toward a "Brain Foundation Model" trained on naturalistic fMRI that generalizes across subjects/stimuli/tasks.
>
> (a) Corpus progress — large datasets (HCP 7T, UK Biobank, NSD, NNDb), spatiotemporal transformers, hyperalignment pretraining
> (b) Architecture/data requirements — transformer vs. GNN vs. state-space, pretraining objectives, scaling laws
> (c) Closest current work and gap to a true Brain FM; roadmap
>
> Synthesize with citations.

**Why**: Brain foundation models은 분야 미래. 데이터/아키텍처 요구사항 체계적 매핑.

**Answer file**: [`../answers/Q11_brain_foundation_models.md`](../answers/Q11_brain_foundation_models.md)

---

### Q12 — Generative Decoding from Naturalistic Brain Activity

> Brain-to-text (Tang/Huth 2023), brain-to-image (MindEye, Takagi 2023), brain-to-video (Chen 2024) have matured.
>
> (a) Current state and limits of generative decoding from naturalistic stimuli; fidelity benchmarks
> (b) Fundamental limits — modality-independent semantic meaning, personal/autobiographical interpretations, unconscious content, privacy implications
> (c) What decoding success/failure teaches about cortical representational format; generative AI + brain data joint tool
>
> Synthesize with citations.

**Why**: Decoding은 brain reading 현실화. 한계/윤리 이슈 병행 검토 필수.

**Answer file**: [`../answers/Q12_generative_decoding.md`](../answers/Q12_generative_decoding.md)

---

### Q13 — Neurally-Inspired AI Architectures

> Naturalistic neuroscience reveals brain computations (temporal hierarchies, event segmentation, predictive dynamics, hippocampal replay, attention prioritization).
>
> (a) Corpus findings applicable to AI — biological timescale ratios, event-segmented processing, hippocampal replay-inspired memory, attention-modulated feedback
> (b) Robust transferable principles vs. species/tissue-specific
> (c) What would a "naturalistic-inspired foundation model" look like — comparison with brain-agnostic large models on efficiency, alignment, interpretability
>
> Synthesize with citations.

**Why**: Neuro → AI 양방향. Event segmentation, timescale hierarchy 등을 LLM 아키텍처에 주입 가능성.

**Answer file**: [`../answers/Q13_neurally_inspired_ai.md`](../answers/Q13_neurally_inspired_ai.md)

---

## Category E. Individual Differences & Clinical Translation

### Q14 — Why Naturalistic fMRI Outperforms Resting-State for Individual/Clinical Prediction

> The corpus shows naturalistic features consistently outperform resting-state for psychiatric/trait prediction.
>
> (a) Candidate mechanisms — signal amplification (broader activation), ecological specificity (real-world match), better SNR (controlled state), individual-engagement variance amplification
> (b) Which disorders/traits benefit most (autism, ADHD, depression, psychosis, anxiety, personality); effect-size comparisons
> (c) AI-driven adaptive stimulus selection personalizing diagnostic content to maximize individual biomarker signal
>
> Synthesize with citations.

**Why**: Naturalistic의 임상 우위는 반복 관찰 but 기전 불분명. 기전 파악이 stimulus design 가이드.

**Answer file**: [`../answers/Q14_naturalistic_vs_restingstate_clinical.md`](../answers/Q14_naturalistic_vs_restingstate_clinical.md)

---

### Q15 — Longitudinal Stability & Treatment Response Tracking

> Longitudinal naturalistic fMRI is severely underrepresented (<2 corpus papers).
>
> (a) Test-retest stability metrics for ISC, fingerprinting, event segmentation across sessions/weeks/years
> (b) Methodological challenges — habituation, stimulus repetition effects, dose-response confounds, developmental change interference
> (c) AI solutions — adaptive stimulus selection, brain-state-conditioned content generation, synthetic longitudinal benchmarks, digital twins
>
> Synthesize with citations.

**Why**: 종단 연구 부족은 분야 전체 한계. AI가 habituation/repetition 문제 해결할 수 있는지 탐구.

---

### Q16 — Interpretation of Movie-Watching Fingerprints

> Movie-watching brain fingerprints (Finn, Vanderwal, Rosenberg) identify individuals with >90% accuracy.
>
> (a) Composition — stable trait (personality, IQ), state-dependent engagement, stimulus-specific interpretation, noise residual; which networks contribute
> (b) Decomposition studies — multi-stimulus, multi-session designs separating trait/state/stimulus
> (c) AI methods (multi-task learning, disentangled representations, causal inference) for separating factors
>
> Synthesize with citations.

**Why**: Fingerprinting이 강력하지만 해석 불명. Trait/state/stimulus 분해는 disentangled representation의 brain application.

**Answer file**: [`../answers/Q16_movie_watching_fingerprints.md`](../answers/Q16_movie_watching_fingerprints.md)

---

## Category F. Developmental & Cross-Species

### Q17 — Developmental Trajectory of Naturalistic Processing

> When do mature naturalistic processing hierarchies develop?
>
> (a) Corpus findings on infant/child/adolescent naturalistic fMRI (Ellis 2025 infant visual cortex, Cohen 2022 story-evoked responses, Tripathy 2024 adults vs. children)
> (b) Earlier biomarkers for atypical development (ASD, language delay) than traditional tasks?
> (c) AI simulations of neural development (NeuroGPT, lifespan-trained brain FMs) to illuminate what matures when
>
> Synthesize with citations.

**Why**: Naturalistic은 영유아 연구에 특히 강력 (비협조 피험자). 조기 biomarker 가능성 클리니컬 임팩트.

**Answer file**: [`../answers/Q17_developmental_trajectory.md`](../answers/Q17_developmental_trajectory.md)

---

### Q18 — Cross-Species Naturalistic Homologies

> Marmoset/macaque naturalistic fMRI has grown rapidly (14 corpus papers, 5 in 2024-2025).
>
> (a) Cross-species homologies — temporal hierarchies, movie-evoked connectivity, social/face processing, attention networks
> (b) Methodological challenges — stimulus adaptation, cross-species alignment, scanner tech, training
> (c) Multimodal foundation models as shared referential embedding for human + non-human primate naturalistic data
>
> Synthesize with citations.

**Why**: Comparative naturalistic fMRI는 침습적 실험(lesion, optogenetics)의 인간 결과 번역 통로. Foundation model이 shared embedding 제공.

---

## Category G. Frontiers & Meta-Science

### Q19 — Cultural Bias and Stimulus Representativeness

> The corpus stimuli are heavily Western, English-language, adult-media-focused.
>
> (a) Corpus acknowledgment of cultural/demographic stimulus bias; cross-cultural replications
> (b) Consequences for neural "universals" vs. culturally-specific findings; global clinical translation
> (c) AI-generated naturalistic stimuli (multilingual LLM narratives, culturally-diverse Sora/Veo video, style-transfer film) — ethical considerations
>
> Synthesize with citations.

**Why**: WEIRD 편향은 분야 건전성 문제. AI-generated stimuli가 해결책이지만 윤리/생태학적 타당성 주의.

---

### Q20 — Beyond Movies: VR, Real-World, Social Interaction

> Naturalistic fMRI remains scanner-constrained (fixed position, 2D display, isolated viewing).
>
> (a) Extensions — VR-in-scanner, hyperscanning (Schippers, Naci, Ramseyer), real-time neurofeedback, ambulatory paradigms
> (b) Technical frontiers — 7T + VR, portable MEG, ultra-low-field MRI, wearable neuroimaging
> (c) AI as enabler — adaptive content, closed-loop stimulation, synthetic controls, cross-modality neural proxies (EEG-fMRI fusion)
>
> Synthesize with citations.

**Why**: Scanner 한계는 naturalistic fMRI의 역설. VR/wearable 기술과 AI 결합으로 real-world 확장.

---

## Query Execution Tips

### Batch Execution (MCP)

5개씩 병렬 (NotebookLM rate limit 고려):

```python
queries_batch = [q1, q2, q3, q4, q5]
for q in queries_batch:
    result = mcp__notebooklm__notebook_query(
        notebook_id="d9265824-3383-4fd4-8d17-03512a338ee5",
        query=q,
        timeout=180
    )
    # save to tool-results/
```

### Response Length Tuning

```python
# 쿼리 전 설정
mcp__notebooklm__chat_configure(
    notebook_id=nb_id,
    response_length="longer"  # 기본값의 1.5-2배 길이
)
```

### Quality Gate

각 쿼리 응답 품질 체크:
- [ ] 답변 길이 >3 KB
- [ ] Citations ≥5
- [ ] 3-part 구조 유지 ((a)(b)(c))
- [ ] 외부 지식 명시적 구분 ("while the sources do not contain...")

---

## Extending the Query Set

새 쿼리 추가 시 → [`06-extending.md`](06-extending.md#adding-queries) 참조.

---

## Korean Translation (쿼리 제목만)

| # | English | Korean |
|---|---------|--------|
| 1 | Statistical Inference | 통계적 추론 |
| 2 | Stimulus Standardization | 자극 표준화 |
| 3 | Motion & Artifact | 동작·아티팩트 |
| 4 | Temporal Hierarchy | 시간 계층 |
| 5 | Shared vs Idiosyncratic | 공유 vs 개별 부호 |
| 6 | Multimodal Integration | 다중 모달 통합 |
| 7 | Event Segmentation | 사건 분할 |
| 8 | Memory Encoding | 기억 공고화 |
| 9 | Predictive Coding | 예측 부호화 |
| 10 | LLM-Brain Alignment | LLM-뇌 정합 |
| 11 | Brain Foundation Models | 뇌 기초 모델 |
| 12 | Generative Decoding | 생성적 디코딩 |
| 13 | Neurally-Inspired AI | 신경 영감 AI |
| 14 | Clinical Superiority | 임상 우위 |
| 15 | Longitudinal Tracking | 종단 추적 |
| 16 | Fingerprint Interpretation | 지문 해석 |
| 17 | Developmental Trajectory | 발달 궤적 |
| 18 | Cross-Species Homologies | 종간 정합 |
| 19 | Cultural Bias | 문화적 편향 |
| 20 | Beyond Movies | 영화 너머 |
