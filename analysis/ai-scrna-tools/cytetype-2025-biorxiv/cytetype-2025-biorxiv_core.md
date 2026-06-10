# cytetype-2025-biorxiv_core.md
<!-- PDF 기반 전체 분석. abstract-only 버전 덮어씀. Source: sources/cytetype-2025-biorxiv.pdf (2025-11-07) -->

## Executive Summary

- **무엇**: single-cell transcriptomics에서 cell type annotation을 단순 label 배정에서 증거 기반 생물학적 발견으로 전환하는 multi-agent AI 프레임워크 CyteType을 제안. 핵심 기여는 5개 특화 agent의 협업, pseudo-bulked expression database 기반 hypothesis testing, confidence score와 heterogeneity flag를 통한 불확실성 정량화, 그리고 semantic benchmark metric CyteOnto.
- **모델 / 방법**: 입력(scRNA-seq cluster + study context) → Contextualizer (pathway/tissue context) → Annotator (경쟁 가설 생성 + 동적 증거 수집) → Reviewer (CellGuide cross-check, confidence score) → Literature & Clinical Relevance (PubMed/Disease Ontology/Drug Ontology) → Summarizer. 평가 metric: CyteOnto Gaussian Hill Kernel similarity ($\sigma=0.25$, $c=1.0$, $A=1.0$).
- **핵심 결과**:
  - ① 동일 LLM(GPT-5) 조건, GPTCellType 대비 +388.52% similarity ($z=8.04$, $p<.001$, Tukey-adjusted, 4 datasets/205 clusters)
  - ② CellTypist 대비 +267.9% ($z=8.15$, $p<.001$); SingleR 대비 +100.67% ($z=8.36$, $p<.001$)
  - ③ 16 LLMs 평가: closed-weight > open-weight ($b=-0.035$, $p<.001$), chain-of-thought 추가 이점 없음 ($p=0.22$)
  - ④ High-confidence annotation이 더 높은 similarity: $F=23.88$, $p<.001$; 반복 실행 majority agreement >80%
  - ⑤ 977 clusters × 20 datasets: 41% functional enhancement, 29% subtype refinement, 30% major reannotation; Pearson $r=-0.79$ (heterogeneity vs. confidence, $p<.001$)
- **우리 적용**: scRNA-seq cell type annotation 자동화에 `pipeline-applicable`. Python (AnnData) / R (Seurat) SDK 공개. 우리 HSPC 10x Multiome dataset에 바로 적용 가능. confidence score로 expert review 우선순위 결정에 활용.
- **심층**: 한계·재현 ROI는 `cytetype-2025-biorxiv_lens-academic.md` / `cytetype-2025-biorxiv_lens-industry.md` / `cytetype-2025-biorxiv_methodology-brief.md` 참고.

---

## Identity

- **Title**: Multi-agent AI enables evidence-based cell annotation in single-cell transcriptomics
- **Authors**: Gautam Ahuja\*, Alex Antill\*, Yi Su, Giovanni Marco Dall'Olio, Sukhitha Basnayake, Göran Karlsson, Parashar Dhapola† (\*equal contribution, †corresponding: parashar@nygen.io)
- **Affiliations**: Nygen Analytics AB (Medicon Village, Lund, Sweden); Stem Cell and Leukemia Lab, Lund University, Sweden; GMD Bioinformatics, UK
- **Year**: 2025
- **Venue**: bioRxiv preprint, posted November 7, 2025
- **DOI**: 10.1101/2025.11.06.686964
- **Document type**: preprint (CC-BY-NC 4.0; not peer-reviewed)
- **Citation key**: `ahuja2025cytetype`
- **Software**:
  - Python (AnnData): https://github.com/NygenAnalytics/CyteType
  - R (Seurat): https://github.com/NygenAnalytics/CyteTypeR
  - CyteOnto: https://github.com/NygenAnalytics/CyteOnto
  - Benchmark: https://github.com/dalloliogm/cytetype_benchmark/tree/main/notebooks/manual
  - Manuscript: https://github.com/NygenAnalytics/CyteType_manuscript
  - Example HTML report (HTAN MSK): https://nygen-labs-prod--cytetype-api.modal.run/report/5b4eb3e1-fde7-4609-8be0-2bea015c241d?v=250722

---

## Background

#### 배경 스토리

- **문제의 출발점**: scRNA-seq dataset이 수백만 cell을 포함하는 규모로 성장하면서 분석 병목은 데이터 처리에서 생물학적 해석, 특히 cluster의 cell type identity 결정으로 이동했다. Disease context에서 cell type annotation은 특히 어렵다 — reference-based classifier는 healthy tissue로 학습되어, 질환 sample에 적용 시 accuracy가 15–30% 하락하고 희귀 cell type을 약 20% 케이스에서 놓친다(저자 ref 7). 수동 annotation은 우수하지만 시간 소요가 크고 annotator 간 25% 편차가 존재한다(ref 8). 기존 방법은 cell type label만 반환하며 justification이나 caveat를 제공하지 않는다(ref 9).

- **선행 접근 A — reference-based classifiers (CellTypist, SingleR)**: 기존 annotated reference dataset과의 상관 또는 logistic regression으로 query cell을 분류. 대규모 atlas에서 빠르고 일관성 있지만, 학습된 cell type 공간 밖의 novel population이나 disease-altered state 발견이 어렵고, label만 반환하여 interpretability가 제한된다.

- **선행 접근 B — LLM 직접 prompting (GPTCellType, Cell2Sentence)**: GPT-4는 expert annotation과 75% 일치(ref 10)를 보이며 LLM 활용 가능성을 입증했다. 그러나 기존 LLM 방식은 ① top marker gene만 처리하고 full expression profile 미활용, ② static pretraining 지식에만 의존해 외부 database 검증 없음, ③ 예측 불확실성 정량화 메커니즘 부재.

- **이 논문으로 이어지는 gap**: reference-based는 이미 알려진 cell type으로 제한, LLM direct prompting은 hallucination과 검증 부재. 두 방식 모두 annotation을 "label 배정"으로 취급하고 증거 체인이 없다. CyteType은 multi-agent hypothesis-driven framework로 이 gap을 메운다: 전체 expression data와 pathway enrichment를 기반으로 경쟁 가설을 생성하고, 외부 database 검증을 수행하며, confidence score로 불확실성을 정량화한다.

#### 기본 개념

- **Cell type annotation**: scRNA-seq에서 클러스터링된 세포 집단에 생물학적 cell type identity를 부여하는 과정. 마커 유전자 발현 패턴을 reference atlas 또는 전문가 지식과 대조한다.
- **Pseudo-bulked expression database**: 각 cluster의 gene 발현 비율(expression percentage)과 top marker gene을 내부 query-ready database로 집계. LLM agent가 function call(도구 호출)로 임의 유전자 조합에 대한 증거를 동적으로 수집한다.
- **Cell Ontology**: 표준화된 세포 유형 분류 체계. CyteOnto는 Cell Ontology term에 LLM-augmented description의 text embedding을 부여하고, Gaussian Hill Kernel로 semantic similarity score를 산출하여 string matching보다 생물학적 의미를 보존한다.
- **Multi-agent system**: 서로 다른 역할의 AI agent가 tool use와 메시지 전달로 협업. 각 agent는 LLM + 외부 database 접근 능력으로 구성.
- **Confidence score & heterogeneity flag**: Reviewer agent가 가상 전문가 패널을 시뮬레이션하여 annotation 확실성을 수치화. 혼합 세포 집단(heterogeneous cluster) 여부도 자동 탐지.

#### 이 논문의 필요성

- **핵심 이유**: 현재 방법들은 label만 반환하고 왜 그 label인지 justification을 제공하지 않는다. 이는 결과 해석 가능성을 제한하고, 잘못된 annotation이 downstream 분석 전체에 영향을 미쳐도 발견하기 어렵게 만든다.
- **기존 방법으로 부족했던 지점**: reference-based는 disease context에서 정확도 하락, LLM direct prompting은 hallucination과 불확실성 정량화 부재.
- **이 논문이 해결하려는 방향**: annotation을 "evidence-grounded biological characterization"으로 재정의. 가설 생성 → 증거 수집 → 외부 검증 → confidence 정량화의 과학적 추론 과정을 자동화.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: scRNA-seq cluster (gene expression matrix + metadata)를 입력으로, Cell Ontology 연결 cell type label + confidence score + 지지 증거(marker 발현 수치, pathway enrichment, literature)를 출력.
- **입력**: AnnData (.h5ad) 또는 Seurat (.RDS) 객체; 사용자 제공 study context (species, tissue, experimental design). 내부적으로 각 cluster의 gene expression percentage와 top marker gene이 pseudo-bulked database로 집계.
- **출력**: Cell type label + Cell Ontology term + confidence score + heterogeneity flag + marker justification + pathway enrichment + literature 연결 + disease association. JSON 구조화 출력 및 interactive HTML report.
- **추정 대상**: 각 cluster의 cell type identity와 annotation 불확실성 (confidence).
- **중요한 hidden assumption**: author-provided annotation을 ground truth proxy로 사용. 이 proxy 자체가 perfect ground truth가 아니라는 점은 저자도 명시.

#### 확률 / 통계학적 구조

- **Model family**: Deterministic multi-agent pipeline + LLM probabilistic generation. 확률 모델 자체보다 외부 database 검증과 structured reasoning에 의존.

- **CyteOnto similarity metric**: Gaussian Hill Kernel over cosine similarity
$$\text{Gaussian Hill}(x) = A \cdot \exp\!\left(-\frac{(x-c)^2}{2\sigma^2}\right)$$
  $c = 1.0$ (center), $\sigma = 0.25$ (width), $A = 1.0$ (amplitude). 높은 유사도 관계를 강조하면서 similarity spectrum 전체에서 감도를 유지. 생물학적 계층 전반에서 단조 감소 달성. Cell type label → 가장 가까운 Cell Ontology term (cosine similarity 기준) → GHKcos로 normalized distance 산출.

- **Statistical analysis — Similarity to author (LME, REML)**:
$$\text{Similarity}_{ijk} = \beta_0 + \beta_1 LLM_{ijk} + u_j + v_k + \varepsilon_{ijk}$$
  LLM 고정효과 $\beta_1$; iteration 랜덤효과 $u_j \sim N(0, \sigma^2_\text{iteration})$; dataset 랜덤효과 $v_k \sim N(0, \sigma^2_\text{dataset})$.

- **Statistical analysis — Majority agreement (GLME, Laplace approximation)**:
$$\text{logit}(\Pr(\text{Mode}_{ijk}=1)) = \beta_0 + \beta_1 LLM_{ijk} + u_j + v_k$$

- **Statistical analysis — Heterogeneity (LME, REML)**:
$$\text{Similarity}_{ij} = \beta_0 + \beta_1 \text{Heterogeneity}_{ij} + u_j + \varepsilon_{ij}$$

- **Statistical analysis — Confidence (LME)**:
$$\text{SimilarityScore}_{ij} = \beta_0 + \beta_1 \text{Confidence}_{ij} + \beta_2 LLM_i + \beta_3(\text{Confidence}_{ij} \times LLM_i) + u_j + \varepsilon_{ij}$$

- **Post-hoc**: Tukey-adjusted pairwise comparison (emmeans R package), $\alpha = 0.05$
- **Correlation**: Pearson (confidence vs. similarity scores), Spearman (confidence vs. heterogeneity — ordinal categories)
- **Reproducibility**: consensus Cell Ontology term = 전 iteration 동일 term; F1 score via k-means ($k=2$) dichotomization of similarity scores

#### 핵심 method insight

- **기존 방법의 한계**: top marker gene list를 LLM에 직접 전달하는 방식은 full expression context를 활용하지 못하며, database 검증 없이 static pretraining 지식에만 의존. reference-based는 prior cell type space에 bound.
- **이 논문이 바꾼 가정**: annotation은 one-shot classification이 아니라 경쟁 가설을 생성하고 동적으로 증거를 수집하며 반복적으로 재평가하는 scientific reasoning process.
- **새로 추가한 구조**:
  - Pseudo-bulked expression database (내부) — LLM이 임의 gene에 대해 tool call로 실시간 발현 데이터 조회
  - Reviewer agent — 가상 전문가 패널이 CellGuide marker database에서 annotation을 cross-check, confidence score 산출
  - Literature & Clinical Relevance agent — PubMed, Disease Ontology, Drug Ontology 연결
  - CyteOnto — string matching/graph distance 대신 Cell Ontology embedding + GHKcos로 semantic similarity 정량화
- **이 변화가 중요한 이유**: 동일 LLM(GPT-5)으로 CyteType vs. GPTCellType을 직접 비교했을 때 +388.52% — 이는 underlying LLM capability가 아니라 framework architecture의 기여임을 isolate.

#### 이전 방법과의 차이

- **Baseline**: SingleR (R Bioconductor, reference correlation), CellTypist (Python v1.7.1, supervised logistic regression), GPTCellType (LLM direct prompting, R, GPT-5)
- **공통점**: LLM 기반 방법들과 gene expression data 사용
- **차이점 요약**:

| 항목 | 기존 LLM approach | CyteType |
|------|------------------|---------|
| 입력 | Top marker gene list | Full expression percentage (pseudo-bulk DB) |
| 검증 | 없음 | CellGuide marker DB cross-check |
| 불확실성 정량화 | 없음 | Confidence score + heterogeneity flag |
| 출력 | Label | Label + 증거 + 문헌 + 임상 연결 |
| LLM 의존도 | High | Framework architecture이 주도 |

- **차이가 크게 나타나는 조건**: multi-tissue dataset (GTEx v9); 저자 기술 — "performance gains consistent across diverse biological contexts but most pronounced in multi tissue datasets"

#### 효과가 Results에서 나타난 방식

- GPT-5 동일 조건, 4 benchmark datasets (205 clusters): +388.52%, $z=8.04$, $p<.001$
- Open-weight model도 전통적 방법 상회: closed-weight 대비 $b=-0.035$, $SE=0.011$, $p<.001$
- Chain-of-thought 추가 이점 없음: $b=0.014$, $SE=0.011$, $t(3977)$, $p=0.22$
- High-confidence annotations → higher similarity: $F=23.88$, $p<.001$
- Heterogeneous clusters → lower similarity: $F=8.45$, $p<.01$

#### Method 관점의 한계

- **약한 assumption**: author-provided annotation을 ground truth proxy로 사용. Immune Cell Atlas의 경우 CellTypist 자체 label로 만들어져 CellTypist near-perfect (median 1.0, mean 0.8) — positive control로만 유효.
- **구현 및 운영 부담**: cluster당 400,000–600,000 tokens 소비. 처리 시간 평균 5–10분/cluster (LLM provider 속도 의존). 클라우드 API 비용 직결.
- **일반화 불확실성**: 4개 benchmark dataset (205 clusters) 평가. Disease-specific novel cell type에 대한 성능은 large-scale analysis (977 clusters) 결과로만 간접 제시. 독립 lab 외부 replication 없음.
- **Scalable processing**: 기본 병렬 처리 20 clusters, 수백 clusters까지 확장. 대규모 dataset에는 클라우드 인프라 필수.

---

## Results

#### Dataset별 결과

##### Dataset 1 — Primary benchmark (4 datasets, 205 clusters)

- **Dataset**: HypoMap (developing mouse brain, 66 clusters), Immune Cell Atlas (human immune cells, 45 clusters), GTEx v9 (cross-tissue human atlas, 74 clusters), Mouse Pancreatic Cell Atlas (20 clusters)
- **목적**: CyteType vs. reference-based (SingleR, CellTypist) vs. LLM-based (GPTCellType) 비교. Multi-agent architecture의 이점을 underlying LLM과 분리하여 평가.
- **사용한 데이터 규모**: 205 clusters (4 datasets 합계). Cellular diversity 보존하며 down-sampling 적용 (Table SI-3-1).
- **Baseline / 비교 대상**: SingleR, CellTypist (v1.7.1), GPTCellType (GPT-5 사용)
- **Metric**: CyteOnto similarity score (0–1, GHKcos 기반 Cell Ontology semantic similarity)
- **주요 수치**:
  - CyteType vs. GPTCellType (동일 GPT-5): +388.52%, $z=8.04$, $p<.001$ (Tukey-adjusted)
  - CyteType vs. CellTypist: $z=8.15$, $p<.001$; average +267.9%
  - CyteType vs. SingleR: $z=8.36$, $p<.001$; average +100.67%
  - 전체 평균: 기존 방법 대비 +252.36%
  - 예외: Immune Cell Atlas에서 CellTypist near-perfect (median 1.0, mean 0.8) — CellTypist 자체 label 사용, positive control
- **정성 결과**: 이점은 multi-tissue dataset에서 가장 두드러짐.
- **논문 주장과의 연결**: 동일 LLM에서 framework 차이만으로 +388.52% — architecture의 독립적 기여 입증.

##### Dataset 2 — Multi-LLM robustness (16 LLMs)

- **Dataset**: 위 4 benchmark datasets 동일 사용
- **목적**: CyteType architecture robustness를 underlying LLM에 무관하게 평가. LLM 비용·privacy 선택의 실용적 함의 도출.
- **LLM 선정 기준**: context window >32,000 tokens, input cost <$5/M tokens, OpenRouter 접근 가능, tool-use 지원, Graduate-level Google-proof Q&A Benchmark >65 (as of August 29, 2025)
- **테스트 LLMs**: GPT-5, Claude Sonnet 4, Gemini 2.5 Pro (closed-weight); DeepSeek R1, Qwen3 Thinking, Kimi K2, GLM 4.5, Magistral Medium 25.06, Grok 4, GPT-o5S 120B, Gemini 2.5 Flash, Qwen3 235B A22B, Minimax M1, Qwen3 30B A3B Thinking (open-weight 포함)
- **주요 수치**:
  - Closed-weight > open-weight: $b=-0.035$, $SE=0.011$, $p<.001$
  - Chain-of-thought 추가 이점 없음: $b=0.014$, $SE=0.011$, $t(3977)$, $p=0.22$
  - Open-weight (Kimi K2, DeepSeek R1): peak performance의 95% 달성 (Supplementary Information 2)
- **정성 결과**: 모든 tested LLM에서 CyteType이 전통적 방법 상회. CyteType의 structured workflow가 model-native reasoning (chain-of-thought)을 superscede.

##### Dataset 3 — Confidence score & reproducibility 검증

- **Dataset**: Immune Cell Atlas (반복 실행 포함)
- **목적**: confidence score가 annotation 정확도를 예측하는지, heterogeneity flag가 혼합 클러스터를 식별하는지 검증.
- **주요 수치**:
  - High-confidence > low-confidence similarity: $F=23.88$, $p<.001$
  - Heterogeneous cluster → lower similarity: $F=8.45$, $p<.01$
  - Likelihood ratio test (confidence → similarity): $\chi^2=42.06$, $df=16$, $p<.001$
  - Likelihood ratio test (heterogeneity → similarity): $\chi^2=35.44$, $df=16$, $p<.01$
  - 반복 실행: majority agreement >80% (전 LLMs); >70% clusters에서 consensus Cell Ontology term
- **논문 주장과의 연결**: confidence score와 heterogeneity flag가 LLM 선택을 통제한 후에도 독립적으로 similarity를 예측 → "trust layer" 기능 입증.

##### Dataset 4 — Large-scale reannotation (977 clusters, 20 datasets)

- **Dataset**: 20개 datasets, 977 clusters (4 benchmark datasets 포함)
- **목적**: CyteType이 기존 annotation의 단순 검증을 넘어 새로운 biological discovery를 제공하는지 평가. Annotation diversity와 cell state landscape 규명.
- **주요 수치**:
  - 41%: functional enhancement (cell state 정보 추가)
  - 29%: specific subtype refinement
  - 30%: major reannotation
  - 327개 unique Cell Ontology terms (no term >2.5% frequency)
  - 116개 distinct cell states; activation (37%), maturation (16%) most prevalent
  - Predicted heterogeneity vs. confidence: Pearson $r=-0.79$, $p<.001$
- **구체적 발견 예시**: diabetic kidney disease atlas에서 저자 label parietal epithelial cells → injured proximal tubule cell (ALDH1A2+, CFH+, VCAM1+); leukocytes → T cell (activated CD45+DOCK2+ pro-inflammatory)
- **논문 주장과의 연결**: High-confidence discrepancy가 disease context에서 집중 발생 — reference 방법이 역사적으로 underperform하는 영역에서 CyteType이 biologically meaningful refinement 발견.

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: framework architecture가 underlying LLM보다 성능에 더 기여. 모든 LLM에서 전통적 방법 상회. Disease context에서 이점 가장 두드러짐.
- **가장 중요한 수치**: GPTCellType 대비 +388.52% ($p<.001$, 동일 LLM 조건) — architecture 기여의 direct evidence.
- **Baseline 대비 차이**: reference-based(SingleR, CellTypist)와 LLM direct prompting 모두 CyteType에 유의하게 열세.
- **결과 해석 시 주의점**: CyteOnto similarity metric 자체가 이 논문에서 함께 제안됨 — 다른 independent metric으로 평가 시 결론이 동일한지 외부 검증 없음. Immune Cell Atlas positive control 해석 별도 주의. 977 clusters 분석은 통계 검정 없이 percentage로만 제시.

---

## Figures

#### Figure 1

- **이 Figure가 필요한 이유**: 논문의 세 핵심 주장 — (A) framework novelty, (B) CyteOnto 평가 방법론, (C) benchmark 결과 — 를 하나의 Figure에서 통합 제시. 독자가 전체 구조를 한눈에 파악할 수 있도록.
- **이 Figure가 뒷받침하는 주장**: multi-agent architecture가 기존 방법보다 우수하며 이 이점은 LLM 선택에 무관하게 일관된다.

##### 패널별 설명

- **A**: CyteType workflow schematic. 입력: heterogeneous sample (tumor microenvironment 예시), scRNA-seq clusters. Study context 구성: enriched pathways, tissue context, external databases, cluster metadata (batch/treatment/disease/normal 비율), pseudo-bulked expression database. → Annotator: 각 cluster에 대해 5개 경쟁 가설 (H1: M2-like TAM, H2: SPP1+ TAM, H3: C1Q+ TAM, H4: Inflammatory TAM, H5: TREM2+ TAM) 생성 → Evidence collection (SPP1/CD163/C1QA/APOE 발현 수준) → Consensus annotation (SPP1+ TAM) → Review (virtual expert panel: High CD4/Low CD4/PDGFR+/Myosin confidence; marker databases 교차 검증; re-annotation with feedback) → Multi-level annotation with confidence and marker justification.
- **B**: CyteOnto benchmarking strategy. CyteType (5 frontier/open-weight LLMs 중 하나로 설정) + SingleR + CellTypist + GPTCellType을 4개 datasets에서 비교. CyteOnto similarity score (text embedding → Cell Ontology term mapping → GHKcos) + Reliability (Majority Agreement, Calibration) + Performance bubble plot.
- **C**: Multi-LLM benchmark 결과. 16 LLMs (closed-weight: GPT-5, Claude Sonnet 4, Gemini 2.5 Pro 등; open-weight: DeepSeek R1, LLaMA 4, Qwen3 등). 각 LLM에 대해 Overall Similarity Score, Hypnotic/Murine Cell Atlas/Human Pancreatic Atlas/Pancreatic Cell Atlas dataset별 score, Majority Agreement, Calibration, Majority Agreement를 bubble plot으로 표시.

##### 본문에서 강조한 비교

- **비교 대상**: CyteType(GPT-5) vs. GPTCellType(GPT-5) — 동일 LLM 조건에서 framework만 다른 직접 비교
- **관찰된 차이**: +388.52%, $p<.001$ (Tukey-adjusted)
- **이 차이가 의미하는 것**: structured hypothesis testing과 evidence collection이 direct LLM prompting 대비 독립적으로 성능을 향상시킴.

##### 해석 시 주의점

- Bubble plot (C)에서 정확한 수치 읽기 어려움. 정량 비교는 본문 통계 수치를 우선.
- CyteOnto metric 설계자와 CyteType 개발자가 동일 팀 — evaluation metric과 evaluated method 사이의 methodological independence 한계.

---

## Tables

#### Table 1 — Overview of the CyteType Multi-Agent Architecture (p.10–11)

- **이 Table이 필요한 이유**: 5개 agent 각각의 역할·해결 과제·통합 외부 도구를 구조화하여 framework 아키텍처를 한눈에 제시.
- **이 Table이 뒷받침하는 주장**: CyteType은 단순 LLM wrapper가 아니라 각기 다른 biological challenge를 담당하는 전문화 agent의 협업 시스템이다.

#### 표 구조

- **Row**: Agent 이름
- **Column**: Core Challenge Addressed / Key Functions / Integrated External Tools, Databases, and Ontologies

#### 핵심 내용

| Agent | Core Challenge | Key Functions | Tools |
|-------|---------------|---------------|-------|
| Contextualizer | Raw data의 biological context 부재 | Organism/tissue inference, pathway DB selection, cluster-specific context generation | GTEx, Enrichr (Gene Ontology, Reactome, WikiPathways), blitzGSEA |
| Annotator | Marker gene 모호성 + data sparsity | Multi-hypothesis generation, dynamic evidence collection, ontological linking | Cell Ontology |
| Reviewer | 자동화된 robust validation 부재 | External reference validation, simulated expert panel, heterogeneity detection | CellGuide |
| Literature & Clinical Relevance | 문헌·임상 맥락 연결 부재 | Literature search, disease association analysis, drug target identification | PubMed, Disease Ontology, Drug Ontology |
| Summarizer | 대규모 dataset 해석 어려움 | Annotation similarity analysis, name disambiguation, semantic cluster ordering | N/A |

#### 해석 시 주의점

- Chat agent(human-in-the-loop re-annotation)는 Table에서 별도 항목 없이 본문에서만 기술.
- Table이 agent의 모든 내부 구현을 반영하지 않음 — implementation detail은 Supplementary에서 추가 확인 필요.

---

## Supplementary Information

- **Supplementary Information 1**: CyteOnto semantic similarity framework 방법론 상세. GHKcos metric 검증 3종: (1) 30 Cell Ontology term pairs (defined biological relationships), (2) CD4+ T cell reference series (40 progressively distant cell types), (3) sensory neuron reference series. String-matching, graph-based, direct embedding approach 대비 GHKcos 우월성 입증.
- **Supplementary Information 2**: Open-weight vs. closed-weight LLM 상세 benchmark. Kimi K2, DeepSeek R1이 peak performance의 95% 달성 근거.
- **Supplementary Information 3**: 977 clusters × 20 datasets 대규모 분석 결과 상세 (41%/29%/30% 분포 근거, cell state 분류).
- **Table SI-3-1**: 4 benchmark datasets down-sampling 상세. (본문 참조; Supplementary file 별도 접근 필요)

---

## 분석 자체에 대한 메모

- CyteOnto similarity metric이 이 논문에서 함께 제안·사용됨. 평가 지표 설계자와 평가 대상 개발자가 동일 팀이라는 점은 methodological independence 관점에서 독립 검증 필요 (`검토필요:`).
- 4 benchmark datasets의 ground truth는 author-provided annotation. 품질이 dataset마다 다를 수 있음. 특히 Immune Cell Atlas positive control 해석 주의.
- 977 clusters 대규모 분석은 benchmark 4 datasets와 달리 통계 검정 없이 percentage 제시. Reannotation "improvement" 정의가 저자 기준임에 주의.
- Preprint (2025-11-07) — peer review 미완료. COI: 저자 전원 Nygen Analytics 소속 또는 긴밀한 협력 관계.
- Chat agent(interactive re-annotation) 기능은 main text에서 기술되나 benchmark에 포함되지 않아 성능 독립 평가 미제공.
