# scassist-2025-bioinformatics_core.md

## Executive Summary

- **무엇**: scRNA-seq (single-cell RNA sequencing) 분석 전 과정에 걸쳐 LLM (Large Language Model)이 파라미터 추천·해석 보조를 수행하는 R 패키지 SCassist. 기존 task-specific 모델(Geneformer, scGPT 등)과 달리 표준 Seurat 워크플로우 전체에 통합된 "workflow assistant" 패러다임을 처음으로 제시.
- **모델 / 방법**: Seurat 객체에서 계산한 데이터 metrics + 사전 정의된 prompt template을 결합한 augmented prompt를 Google Gemini / OpenAI GPT / Ollama(Llama3)에 전달하고, 파싱된 응답을 화면 출력 또는 Seurat 메타데이터로 반환. 일부 함수는 2-round LLM chaining 사용.
- **핵심 결과**:
  - ① LCMV dataset (4,136 ground-truth tokens) — groundedness score 98.7%
  - ② BCRUV dataset (4,110 ground-truth tokens) — groundedness score 99.9%
  - ③ 두 dataset 모두 BERT 기반 semantic similarity 74~76%
  - ④ 8명 전문가 human evaluation, Wilcoxon Signed-Rank p = 0.0001122로 높은 점수 방향 유의. 전문가 수준·dataset 간 차이 없음
  - ⑤ Google Gemini API 1,978회 호출에 총 비용 $2.07 (약 2개월)
- **우리 적용**: scRNA-seq QC/정규화/클러스터링 파라미터 결정을 LLM 보조로 자동화하는 선행 사례 — `methodology-reference` 및 `academic-citation` 관점. 우리 HSPC 10x Multiome 파이프라인의 QC 단계 보조 도구로 참고 가능하나 Python 기반 파이프라인과는 언어 불일치(R 전용).
- **심층**: 한계·재현 ROI는 `scassist-2025-bioinformatics_lens-academic.md` / `scassist-2025-bioinformatics_lens-industry.md` / `scassist-2025-bioinformatics_methodology-brief.md` 참고.

---

## Identity

- **Title**: SCassist: an AI based workflow assistant for single-cell analysis
- **Authors**: Vijayaraj Nagarajan, Guangpu Shi, Samyuktha Arunkumar, Chunhong Liu, Jaanam Gopalakrishnan, Pulak R. Nath, Junseok Jang, Rachel R. Caspi
- **Affiliation**: Laboratory of Immunology, National Eye Institute (NEI), NIH, Bethesda, MD (일부 저자는 alumni)
- **Year**: 2025
- **Venue**: *Bioinformatics*, 41(8), btaf402 (Oxford University Press, Applications Note)
- **DOI**: 10.1093/bioinformatics/btaf402
- **Published**: 2025-07-12 (Advance Access). Received 2024-12-27, Revised 2025-06-06, Accepted 2025-07-11
- **Citation key**: `nagarajan2025scassist`
- **GitHub**: https://github.com/NIH-NEI/SCassist
- **Zenodo snapshot**: https://doi.org/10.5281/zenodo.15298665
- **Funding**: NIH Intramural Research Program, NEI (EY000184, R01 EY032482)
- **COI**: Vijayaraj Nagarajan, Rachel R. Caspi — SCassist에 대한 provisional patent 보유. 미국 정부 직원 저작물로 공개 영역(public domain in the US).

---

## Background

#### 배경 스토리

- **문제의 출발점**: scRNA-seq 표준 분석 워크플로우(quality filtering → normalization → dimension reduction → clustering → annotation)는 각 단계마다 연구자가 적절한 파라미터를 직접 결정해야 한다. variable gene 해석·PC 해석·enrichment analysis 등에는 생물학 배경 지식이 별도로 필요하며, 전문성과 시간 비용이 높다.
- **선행 접근 A — task-specific single-cell AI 모델(Geneformer, scGPT, scBERT, TOSICA, CellLM, GeneCompass, CellPLM, scTPC, tGPT, scFoundation)**: foundation model 또는 fine-tuned model로 세포 유형 annotation, imputation, integration, clustering, trajectory 분석, perturbation/drug response prediction 등 개별 과제에서 높은 성능을 달성.
- **A의 한계**: 각 모델이 특정 task에 집중하며, scRNA-seq 파이프라인 *전체*에 걸친 step-by-step workflow 안내가 없다. QC 파라미터나 normalization 방법 선택 같은 파이프라인 초입 단계를 다루지 않는다.
- **선행 접근 B — LLM 기반 애플리케이션(GPTCelltype, ChatCell)**: GPT-4 추론 능력을 이용한 자동 세포 유형 annotation(GPTCelltype), natural language interface를 통한 scRNA-seq 상호작용(ChatCell).
- **B의 한계**: annotation 등 특정 downstream task에만 집중. 파이프라인 전체를 포괄하는 workflow assistance 부재. 일반 목적 LLM을 유연하게 선택·교체하는 접근도 없었다.
- **이 논문으로 이어지는 gap**: 사용자가 Seurat 기반 표준 워크플로우를 step-by-step으로 진행하면서 각 단계의 파라미터 추천·결과 해석을 동시에 받을 수 있는 *통합형 workflow assistant*가 부재. SCassist는 이 gap을 일반 목적 LLM + retrieval·tool-based augmentation 기법으로 접근.

#### 기본 개념

- **Seurat**: R 기반 single-cell analysis 표준 라이브러리. QC, normalization, variable feature selection, PCA, UMAP, FindNeighbors(KNN), FindClusters, FindAllMarkers 등을 포함하는 complete workflow 제공.
- **Augmented prompt**: 사전 정의된 prompt template에 Seurat 계산 결과(metrics, gene list, statistics)를 결합해 LLM에 전달. 외부 모델 학습 없이 context에 데이터를 직접 주입하는 RAG(retrieval-augmented generation)에 근접한 방식.
- **ClusterProfiler**: R 기반 KEGG pathway / Gene Ontology (GO) enrichment analysis 패키지. SCassist `analyze_enrichment` 함수가 내부적으로 호출.
- **Groundedness score** $G$: $G = |GT \cap LLM| / |LLM|$. ground truth(GT) 토큰과 LLM 응답 토큰의 교집합 비율. hallucination 억제의 간접 지표.
- **Semantic similarity**: BERT uncased model로 embedding 후 cosine similarity 계산. LLM 응답과 입력 enrichment 문서 간 의미론적 유사도.

#### 이 논문의 필요성

- **핵심 이유**: scRNA-seq 파이프라인의 각 파라미터(filtering cutoff, normalization method, k.param, resolution 등)는 데이터 특성에 따라 달라지나 기존 도구들이 이 결정을 자동화하지 않았다. 전문성이 낮은 연구자의 진입 장벽을 낮추는 것이 목표.
- **기존 방법으로 부족했던 지점**: task-specific AI 모델들이 annotation 등 개별 과제에 특화되어 있고, R/Seurat 환경 내에서 파이프라인 전체를 커버하는 통합 assistant가 없었다.
- **이 논문이 해결하려는 방향**: 일반 목적 LLM의 추론 능력 + 데이터 기반 augmented prompt 설계 + 기존 Seurat workflow와의 seamless 통합으로 전 단계 workflow assistance 구현.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: Seurat 객체(scRNA-seq count matrix + metadata)를 입력으로 받아 각 분석 단계(QC, normalization, dim reduction, clustering, annotation, enrichment)에 최적화된 파라미터 추천과 생물학적 해석을 LLM을 통해 제공.
- **입력**: Seurat 객체(raw count matrix, metadata), 이전 Seurat 분석 결과(PCA 결과, FindAllMarkers 결과, ClusterProfiler 결과 등), 사용자가 제공하는 실험 설계 설명.
- **출력**: 파라미터 추천 값 + 추천 근거 텍스트, 세포 유형 annotation + reasoning, enrichment 해석 + interactive network visualization, 필요 시 Seurat 메타데이터 업데이트.
- **추정 대상**: 각 단계별 최적 파라미터(filtering cutoff, normalization method, PC 수, k.param, resolution 범위), 각 cluster의 세포 유형, 주요 biological pathway.
- **중요한 hidden assumption**: LLM의 파라미터 추천이 training data에서 학습된 일반화된 패턴(generalized patterns)에 기반하며, 특정 데이터셋의 실제 생물학적 이질성을 반드시 반영하지는 않는다고 저자가 명시.

#### 확률 / 통계학적 구조

- **Model family**: 결정론적 rule-based가 아닌, LLM의 추론 능력에 기반한 soft recommendation 시스템. 명시적 Bayesian inference나 probabilistic model 없음.
- **Likelihood / objective**: 명시적 objective function 없음. LLM이 augmented prompt에 대해 그럴듯한 응답을 생성하는 autoregressive generation에 의존.
- **Prior / regularization**: 없음. prompt template 설계가 LLM 출력의 형식·내용을 구조화하는 역할.
- **Latent variable / hidden state**: 없음.
- **Inference / optimization**: API call(Google/OpenAI) 또는 local Ollama 추론. 일부 함수는 2-round LLM chaining(1차 응답 → 2차 쿼리 입력, 예: `analyze_enrichment` → `summary_network`).
- **Noise, sparsity, uncertainty 처리**: 명시적 처리 없음. Seurat의 QC/filtering이 upstream에서 처리 후 결과를 입력으로 받음.

#### 핵심 method insight

- **기존 방법의 한계**: 사용자가 매번 수동으로 파라미터를 탐색하거나 고정된 휴리스틱을 데이터 무관하게 적용. Biological interpretation은 전적으로 연구자의 사전 지식에 의존.
- **이 논문이 바꾼 가정**: 데이터로부터 계산한 metrics를 augmented prompt에 포함하면, 일반 목적 LLM의 추론 능력을 데이터 기반 파라미터 추천에 활용할 수 있다는 가정.
- **새로 추가한 변수 또는 구조**: (1) Seurat 계산 metrics를 prompt에 포함하는 augmented prompt 파이프라인, (2) 함수별 독립 prompt template(모듈화, GitHub 공개), (3) 2-round LLM chaining(`analyze_enrichment` 결과 → `summary_network`).
- **이 변화가 중요한 이유**: 사용자가 복잡한 prompt를 직접 작성할 필요 없이 함수 호출만으로 데이터 기반 추천을 받을 수 있다. General-purpose LLM의 광범위한 생물학 지식을 각 단계에 주입.

#### 이전 방법과의 차이

- **Baseline**: GPTCelltype(GPT-4 기반 annotation), ChatCell(natural language interface), 기존 Seurat 수동 분석 워크플로우.
- **공통점**: Seurat FindAllMarkers 결과를 annotation에 활용. GPTCelltype과 동일 입력(FindAllMarkers)으로 annotation 비교 수행.
- **차이점**: GPTCelltype은 annotation task만. SCassist는 QC부터 enrichment까지 전 단계 포괄. 모든 함수에서 추천에 대한 transparent reasoning(추천 근거 텍스트)을 항상 제공.
- **차이가 크게 나타나는 조건**: 파이프라인 초기 단계(QC, normalization, PC selection)에서 차이가 가장 두드러짐 — 기존 LLM 도구들이 이 단계를 다루지 않음.

#### 구현 세부 — 함수 목록

저자가 명시한 10개 핵심 함수:

| 함수 | 역할 |
|---|---|
| `SCassist_analyze_quality()` | nCount_RNA, nFeature_RNA 및 사용자 지정 QC metrics로 filtering cutoff 추천 |
| `SCassist_recommend_normalization()` | dataset 특성(cell 수, gene expression distribution, library size variation) 기반 normalization 방법 추천 |
| `SCassist_analyze_variable_features()` | Seurat이 식별한 top variable features의 GO pathway·생물학적 맥락 해석 |
| `SCassist_recommend_pcs()` | 각 PC의 variance explained 분석 → downstream 분석에 쓸 PC 수 추천 |
| `SCassist_analyze_pcs()` | top PC의 driving biological process 해석 |
| `SCassist_recommend_k()` | cell 수·PC 수·clustering 목표 기반 k.param 범위 추천 |
| `SCassist_recommend_res()` | mean expression variability, median neighbor distance, highly variable gene 수 기반 resolution 범위 추천 |
| `SCassist_analyze_and_annotate()` | cluster별 top markers 기반 세포 유형 예측 + reasoning. Seurat 메타데이터에 annotation 추가 옵션 |
| `SCassist_analyze_enrichment()` | ClusterProfiler KEGG/GO enrichment 실행 → pathway·regulator·key gene 인사이트 생성 |
| `SCassist_summary_network()` | `analyze_enrichment` 출력에서 network 데이터 추출 → interactive network 시각화 |

- 각 함수는 독립적으로 실행 가능. 사용자는 워크플로우의 어느 단계에서든 시작 가능.
- 고급 사용자는 LLM 모델 선택 및 custom model parameter 설정 가능.
- 설치: `devtools::install_github("NIH-NEI/SCassist")`. R 4.4.1 이상. 의존성: Seurat, rollama, httr, jsonlite, visNetwork, clusterProfiler, BiocManager.

#### LLM 서버 옵션

- **Google(default: gemini-1.5-flash-latest)**: 상용 온라인, 대형 context window로 선택. API key 필요.
- **OpenAI(default: gpt-4o-mini)**: 상용 온라인. API key 필요.
- **Ollama(default: llama3)**: 오픈소스, 로컬 실행. 데이터를 외부 서버로 전송하지 않음. 비용 없음.

#### 평가 방법론

- **Groundedness score**: GeneVenn으로 ground truth 토큰과 LLM 응답 토큰의 overlap 측정. $G = |GT \cap LLM| / |LLM|$.
- **Semantic similarity**: BERT uncased model, tokenize → special token 추가 → BERT input length에 맞게 chunk → input id 변환 → embedding 추출 → chunk embedding 결합 → cosine similarity 계산. Python 환경(transformers, torch, sklearn.metrics.pairwise).
- **Human evaluation**: Likert scale 1~5, 5개 항목(Accuracy, Relevance, Clarity, Trustworthiness, Overall satisfaction). Senior 4명(BioTech industry 2명, NIH Staff Scientist 2명) + junior 4명(PostDoc·Post-Bac, NIH). 두 senior는 평가 대상 workflow의 원저자.
- **통계 검정**: Wilcoxon Signed-Rank test(전반적 점수 편향 확인), Wilcoxon Rank-Sum test(전문가 수준별·dataset별 차이).

#### Method 관점의 한계

- **약한 assumption**: LLM 파라미터 추천이 generalized pattern 기반이므로 특정 dataset의 실제 이질성과 불일치할 수 있음(저자 명시). 추천은 *starting point*이며 기존 방법으로 검증 필요.
- **구현 부담**: API key(Google/OpenAI) 또는 Ollama 설치 필요. R 전용(Python 파이프라인 미지원).
- **일반화 불확실**: LLM 모델 버전 변화로 미래 응답 예측 불가(저자 명시). 저자는 3개월마다 모니터링·패키지 업데이트 공약.

---

## Results

#### Dataset별 결과

##### Dataset 1 — LCMV (인간 Uveitis NK cell)

- **Dataset**: NIH NEI 연구실의 인간 Uveitis 환자 NK cell scRNA-seq 데이터(Nath et al. 2024, *Nat Commun* 15:6443). 구체적 cell 수 본문 미제공.
- **목적**: SCassist 생성 workflow report를 기존 발표 논문 표준 workflow report와 비교 — groundedness, semantic similarity, 전문가 평가.
- **Baseline**: 원저자가 작성한 표준 single-cell 분석 workflow report.
- **Metric**: groundedness score (G), BERT semantic similarity, Likert scale.
- **주요 수치**:
  - Ground truth tokens: 4,136개
  - Groundedness score 평균: 98.7%
  - Semantic similarity (BERT uncased): 76%
  - 카테고리별 세부 수치: Supplementary Table 5에만 제공
- **정성 결과**: 8명 중 7명이 clarity에서 유용하다고 평가. Wilcoxon Signed-Rank p = 0.0001122로 전반적 높은 점수 방향 유의.
- **논문 주장과의 연결**: 데이터 기반 augmented prompt로 높은 groundedness 달성, 기존 전문가 수준 workflow report와 유사한 품질임을 지지.
- 해석: 2개 dataset 모두 저자 소속 기관 내부 데이터. 독립 외부 dataset에서의 재현성 미제공.

##### Dataset 2 — BCRUV (마우스 Th1 세포 운명 결정)

- **Dataset**: NIH NEI 연구실의 마우스 Th1 cell fate specification CTCF binding motif 연구 데이터(Liu et al. 2024, *Immunity* 57:1005-18). 구체적 cell 수 본문 미제공.
- **목적**: Dataset 1과 동일한 평가 프레임워크. 다른 생물학적 맥락에서 일관성 확인.
- **주요 수치**:
  - Ground truth tokens: 4,110개
  - Groundedness score 평균: 99.9%
  - Semantic similarity (BERT uncased): 74%
  - Wilcoxon Rank-Sum: dataset 간 성능 차이 비유의
- **논문 주장과의 연결**: 다른 생물학적 맥락에서도 groundedness 유지 확인.

##### Dataset 3 — GPTCelltype 비교 (annotation 정확도 확인)

- **Dataset**: GSM6625298 (SCassist GitHub page 예시 데이터). 구체적 cell 수 미제공.
- **목적**: `SCassist_analyze_and_annotate()` annotation 결과와 GPTCelltype 비교.
- **Metric**: 세포 유형 assignment 일치도. 정량 수치 미제공.
- **결과**: "highly concordant"로 기술. 수치 미제공.
- 해석: 정량 수치 없이 "highly concordant"만 제시. 불일치 케이스 분석 없음.

##### Dataset 4 — API 비용

- **목적**: 실용적 비용 파악.
- **결과**: 2개월 테스트 기간 Google Gemini API 1,978회 호출, 총 비용 $2.07(세금 제외). Ollama 로컬 옵션은 비용 없음.

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: groundedness 두 dataset 모두 98% 이상. 전문가 수준·dataset 간 Likert 점수 차이 없음.
- **가장 중요한 수치**: groundedness 98.7~99.9%, semantic similarity 74~76%, Wilcoxon Signed-Rank p = 0.0001122.
- **Baseline 대비 차이**: clarity에서 7/8 평가자 긍정. 정확도·관련성·신뢰성은 "generally good"(최고 점수는 아님). 세부 Likert 수치는 Supplementary Table 7에만 있어 본문 직접 확인 불가.
- **결과 해석 시 주의점**: 평가 dataset이 저자 내부 데이터 2개뿐. 독립 외부 재현 없음. Ablation study 없음.

---

## Figures

#### Figure 1

- **이 Figure가 필요한 이유**: SCassist의 전체 아키텍처와 각 함수가 Seurat workflow 어느 단계에 대응하는지를 한눈에 보여주기 위함. 논문의 "전 단계 workflow assistance" 주장을 시각적으로 증명하는 overview figure.
- **이 Figure가 뒷받침하는 주장**: SCassist가 QC부터 annotation까지 표준 Seurat workflow 전 단계를 포괄하며, 각 단계에서 데이터 기반 인사이트와 파라미터 추천을 제공한다.

##### 패널별 설명

- **상단 workflow row**: 표준 Seurat 단계 5개(① QC'd raw.data, ② normalization, ③ dimensionality reduction, ④ clustering/UMAP, ⑤ annotation)를 순서대로 표시. 각 단계의 데이터 상태(meta.data, normalized.data, data/PCA/variable features, KNN/SNN/markers 등)가 명시.
- **하단 SCassist 컴포넌트(분홍 박스)**: 각 Seurat 단계에 대응하는 SCassist 함수 10개가 상단 workflow와 연결선으로 연결. 좌→우 순으로 `analyze_quality`, `recommend_normalization`, `analyze_variable_features`, `recommend_pcs`, `analyze_pcs`, `recommend_k`, `recommend_res`, `analyze_and_annotate`, `analyze_enrichment`, `summary_network`.
- **좌하 Example Component 구조**: `analyze_quality` 예시로, (1) SCassist Function, (2) Computed Metrics(Summary Statistics, Quantile Data, Number of Cells), (3) Augmented Prompt, (4) LLM(Gemini/Llama/GPT), (5) Quality Control Recommendations & Rationale 의 데이터 흐름.
- **우하 결과 예시**: Cluster Profiler enrichment network(CASP8, Toll-like receptor signaling 등 포함된 interactive network map) 샘플.

##### 본문에서 강조한 비교

- 비교 대상: 기존 task-specific 도구(annotation만 다루는 GPTCelltype 등) vs. SCassist(전 단계 포괄).
- 관찰된 차이: SCassist는 QC 파라미터 결정 단계부터 시작해 annotation, enrichment까지 end-to-end 지원.
- 이 차이가 의미하는 것: 파이프라인 초입 단계(QC, normalization)에서의 파라미터 오류가 다운스트림으로 누적되는 문제를 LLM 보조로 줄일 수 있다는 저자의 주장을 뒷받침.

##### 해석 시 주의점

- 이 Figure는 architecture overview이므로 성능 수치 없음. "전 단계 포괄" 주장의 visual 근거로만 사용. 실제 각 함수 성능은 Results §3.2의 groundedness/semantic similarity/human evaluation에서 확인 필요.
- Figure가 단일 panel(multilevel composite)이므로 패널 a/b/c 구분이 없음.

---

## Tables

본문에 정식 Table 없음. 모든 Table(Table 1~8)은 supplementary data(*Bioinformatics* online)로만 제공.

- **Supplementary Table 1**: feature comparison — SCassist vs. 기존 방법들. SCassist의 novel contribution 비교.
- **Supplementary Table 2**: SCassist 전체 함수 목록, task·key benefit·workflow 단계.
- **Supplementary Table 3**: 평가에 사용된 dataset 정보.
- **Supplementary Table 4**: 전문가 평가 Likert scoring sheet 양식.
- **Supplementary Table 5**: LCMV dataset 카테고리별 groundedness score 세부.
- **Supplementary Table 6**: BCRUV dataset 카테고리별 groundedness score, semantic similarity 세부.
- **Supplementary Table 7**: Likert scale 상세 점수(8명 평가자, 5개 항목).
- **Supplementary Table 8**: Wilcoxon Rank-Sum test 결과 — 전문가 수준별·dataset별 차이 없음.

---

## Supplementary Information

- **File 1**: 전체 prompt template(각 함수별). GitHub에도 공개.
- **File 2**: `SCassist_analyze_quality()` 실제 prompt template + 예시 출력.
- **File 3**: SCassist annotation 결과와 GPTCelltype 결과 비교.
- **Supplementary Figure 1**: Likert scale 점수 frequency distribution plot. 8명 평가자, accuracy·relevance·clarity·trustworthiness·overall 5개 항목.
- **Tables 1~8**: 위 Tables 섹션 참고.

---

## 분석 자체에 대한 메모

- 본 논문은 Bioinformatics Applications Note(6페이지 단편). 세부 결과 대부분이 supplementary에만 있어 본문만으로 심층 검증 어려움. Oxford Online supplementary(btaf402_supplementary_data.zip) 접근 필요.
- GPTCelltype 비교에서 "highly concordant"만 기술하고 정량 수치 없음 — 검증 강도 낮음. `질문:` File 3 supplementary에 confusion matrix나 정량 일치율이 있는지 확인 필요.
- 평가 dataset 2개 모두 저자 내부 데이터이며, 두 senior evaluator는 해당 워크플로우의 원저자. 독립 외부 평가 구조 아님.
- Ablation study 없음 — augmented prompt의 각 component(metrics vs. prompt template design vs. LLM 선택)가 groundedness에 어떤 기여를 하는지 분리된 분석 없음.

---

## Executive Summary

- **무엇**: SCassist는 LLM을 Seurat 기반 scRNA-seq 분석 워크플로우에 통합한 R 패키지로, QC 파라미터 추천·정규화·클러스터링 파라미터 제안·세포 유형 주석·인리치먼트 분석까지 단계별 AI 가이던스를 제공한다.
- **핵심 발견**: Gemini/GPT/Llama3 지원. 워크플로우 응답의 Groundedness 98.7% (LCMV 데이터셋), 인간 전문가 평가에서 Wilcoxon p=0.0001로 유의미하게 높은 점수. 2개월 1,978 API 호출 총 비용 $2.07.
- **OncoRader 비교**: SCassist는 파라미터 추천에 특화된 범용 R 패키지로, CTC 분류·ADC 타겟 발굴·다중 에비던스 스코어링과 같은 종양 특이적 분석 축은 전무하다. OncoRader는 CTC × ADC 이중 축 분류, DCIS v2.1 스코어링, tier 분류 체계를 내장한 반면 SCassist는 파라미터 자동화에 그친다.

---

## Identity

- **Title**: SCassist: An AI Based Workflow Assistant for Single-Cell Analysis
- **Authors**: Nagarajan V, Shi G, Arunkumar S, Liu C, Gopalakrishnan J, Nath PR, Jang J, Caspi RR
- **Affiliation**: Laboratory of Immunology (+ Neuro-Immune Regulome Unit), National Eye Institute, NIH, Bethesda, MD 20892, USA
- **Venue / Year**: *Bioinformatics* 41(8):btaf402 (2025-08-02). bioRxiv preprint: 2025.04.22.650107 (2025-04-28)
- **Funding**: 외부 맥락: NIH National Eye Institute (NEI) 내부 연구비 추정. 본문 명시 내용은 PMC 전문 직접 확인 필요.
- **COI**: 외부 맥락: 공식 COI 명시 미확인. NIH 학술 그룹 (비상업).
- **License**: CC BY 4.0 (Oxford University Press open access)
- **Code / Data**: https://github.com/NIH-NEI/SCassist (R 패키지 + 튜토리얼). 데이터: LCMV, BCRUV 공개 데이터셋 사용.
- **Citation key**: `scassist2025bioinformatics`

---

## Background

### 문제의 출발점

scRNA-seq 분석은 QC threshold 설정·정규화 방법 선택·클러스터링 resolution 결정 등 각 단계마다 전문 지식이 필요한 파라미터 결정을 요구한다. 초보 연구자는 이 복잡한 반복적 워크플로우를 안내받기 어렵다.

### 기존 접근의 한계

표준 Seurat 파이프라인은 파라미터를 수동 설정해야 하며, 각 결정의 생물학적 근거를 워크플로우 내에서 설명해주는 도구가 없었다. 세포 유형 주석 도구 (SingleR, CellTypist 등)는 reference DB 의존적이거나 유전자 목록 해석에 전문 지식이 필요하다.

### 이 논문의 해결 방향

사용자 데이터의 실제 통계치 (분위수·분산 설명량 등)와 실험 설명을 결합한 "augmented prompt"를 LLM에 전달하여, 각 단계의 파라미터를 데이터 기반으로 추천하고 근거를 함께 제공한다.

---

## Methods (abstract 범위)

### 핵심 설계

- **Augmented prompt 구성**: (1) 실제 데이터 통계 (요약 통계, 분위수, 설명 분산) + (2) 사전 정의 프롬프트 템플릿 + (3) 실험 설명 → LLM 입력
- **지원 LLM**: Google Gemini (기본: gemini-1.5-flash-latest), OpenAI GPT (기본: gpt-4o-mini), Meta Llama3 (Ollama 로컬 실행)
- **워크플로우 통합 단계**: QC filtering → 정규화 → 차원 축소 → 클러스터링 → 세포 유형 주석 → 인리치먼트 분석
- **세포 유형 주석**: `SCassist_analyze_and_annotate()` 함수. 클러스터 마커 분석 → LLM 세포 유형 예측 + 근거 설명. GPTCelltype와 동일 마커 입력 시 "높은 일치도" 보고.
- **R 패키지 형태**: Seurat 생태계 내에서 동작. 독립 소프트웨어가 아닌 보조 어시스턴트.

### 평가 지표

- **Groundedness**: LLM 출력이 제공된 데이터에 얼마나 기반하는지 (환각 최소화 지표)
- **Semantic Similarity**: 출력의 맥락적 관련성
- **Human Evaluation**: 전문가 8인의 5점 Likert 척도 평가

---

## Results (abstract 범위)

- Groundedness 98.7% (LCMV), 99.9% (BCRUV) — LLM 기반 추천이 실제 데이터에 근거함을 확인
- Semantic Similarity 76% (LCMV), 74% (BCRUV)
- 전문가 8인 Wilcoxon Signed-Rank test p=0.0001 — 무작위 대비 유의미하게 높은 점수
- 2개월 1,978회 API 호출 총 $2.07 비용 — 현실적 운영 비용
- 세포 유형 주석: GPTCelltype와 동일 마커 입력 시 높은 일치도

---

## Analysis Notes

- **재현성**: LCMV, BCRUV 공개 데이터셋. GitHub 튜토리얼 제공.
- **한계**: LLM 환각 (hallucination) 저자 명시. 분기별 모니터링 약속.
- **OncoRader 차별점**: SCassist는 워크플로우 파라미터 어시스턴트이며 세포 분류의 생물학적 특이성 (CTC subtype, ADC tier) 없음.
- **외부 맥락**: 외부 맥락: NIH 비상업 학술 도구로 상업적 경쟁 대상이 아니나, 파라미터 자동화 패러다임의 지형도 파악에 유용.
