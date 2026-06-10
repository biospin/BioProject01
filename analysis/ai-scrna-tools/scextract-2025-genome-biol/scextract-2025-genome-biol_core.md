# scExtract — core analysis

> Wu Y. and Tang F., 2025. *scExtract: leveraging large language models for fully automated single-cell RNA-seq data annotation and prior-informed multi-dataset integration.* Genome Biology 26:174. DOI: 10.1186/s13059-025-03639-x
>
> **근거 자료**: 전체 PDF (`sources/scextract-2025-genome-biol.pdf`, 28 pages). 외부 지식 사용 시 `외부 맥락:` 표기.

---

## Executive Summary

- **무엇**: 공개된 scRNA-seq 논문 PDF에서 전처리 파라미터와 세포 유형 정보를 LLM으로 자동 추출·annotation하고, 그 annotation을 prior로 삼아 다수 데이터셋을 통합하는 end-to-end 프레임워크(scExtract). 기존 reference transfer 방식의 novel cell type 발견 불가 문제와 배치 보정 시 생물학적 다양성 손실 문제를 동시에 해결한다.
- **모델 / 방법**: LLM agent(GPT-4o-mini / Deepseek-v2.5 / Claude-3.5-Sonnet 중 선택)가 논문 PDF에서 파라미터를 추출 → scanpy 기반 필터링·클러스터링·annotation 5단계 파이프라인 실행 → annotation에서 생성한 cell-type similarity matrix $M_{IJ}$를 scanorama-prior($d'_{ij} = d_{ij}/M_{IJ}$)와 cellhint-prior($S'_{ij} = \beta[(1-\alpha_i)S_{ij} + \alpha_i M_{IJ}] + (1-\beta)S_{ij}$)에 주입하여 배치 보정 및 annotation harmonization 수행.
- **핵심 결과**:
  - ① cellxgene 18개 benchmark dataset — text-to-embedding annotation 정확도에서 SingleR·scType·CellTypist·GPTCelltype 전 방법 대비 우위 (Fig. 2D; Wilcoxon p < 10⁻¹³)
  - ② 췌장 multi-platform benchmark — scanorama-prior가 원본 scanorama 대비 batch correction + biological conservation 양 지표 우월 (Fig. 3B)
  - ③ 대규모 3개 데이터셋 (Immune ALL 33k cells, Blood 336k cells, HCLA 585k cells) — scExtract two-step pipeline이 기존 방법 대비 integration 성능 우위 (Fig. 4A–C)
  - ④ 피부 14개 데이터셋 통합 (440,000 cells) — 전자동으로 건선 특이적 CXCL14⁺ 증식 keratinocyte subpopulation 발굴
  - ⑤ 처리 비용·시간 — 데이터셋 1건당 20분 이내, API 비용 $1 미만 (Fig. S3E)
- **우리 적용**: scRNA-seq pipeline에서 공개 데이터셋 재활용 또는 multi-dataset atlas 구축 시 LLM-driven annotation + prior-aware integration을 직접 차용 가능. use_case: `pipeline-applicable` / `methodology-reference`.
- **심층**: 한계·재현 ROI는 `scextract-2025-genome-biol_lens-academic.md` / `scextract-2025-genome-biol_lens-industry.md` / `scextract-2025-genome-biol_methodology-brief.md` 참고.

---

## Identity

| 항목 | 내용 |
|---|---|
| Title | scExtract: leveraging large language models for fully automated single-cell RNA-seq data annotation and prior-informed multi-dataset integration |
| Authors | Yuxuan Wu¹, Fuchou Tang¹·² |
| Affiliations | ¹Biomedical Pioneering Innovation Center, School of Life Sciences, Peking University, Beijing 100871; ²Beijing Advanced Innovation Center for Genomics (ICG), Ministry of Education Key Laboratory of Cell Proliferation and Differentiation |
| Year | 2025 |
| Venue | Genome Biology 26:174 |
| DOI | 10.1186/s13059-025-03639-x |
| Document type | Software paper (Open Access, CC BY 4.0) |
| Citation key | `wu2025scextract` |
| GitHub | https://github.com/yxwucq/scExtract (BSD 2-Clause) |
| Zenodo (code) | https://doi.org/10.5281/zenodo.15555221 |
| Zenodo (benchmark data) | https://doi.org/10.5281/zenodo.13827072 |
| Received / Accepted / Published | 2024-12-31 / 2025-06-02 / 2025-06-19 |
| Funding | Beijing Natural Science Foundation (7242109), New Cornerstone Science Foundation |
| Competing interests | None declared |

---

## Background

### 배경 스토리

- **문제의 출발점**: 공개 scRNA-seq 데이터는 매년 수천 건씩 증가하지만(Fig. 1A; 2024년 기준 연간 6,000건 이상 신규 논문), 대부분의 공개 데이터셋에는 세포 수준 annotation이 없거나 불완전하다. cellxgene은 2024년 8월 기준 1,458개 데이터셋을 보유하지만, 이는 매년 쏟아지는 신규 데이터의 극히 일부다. 데이터 공유 프로토콜은 raw sequencing data 제출만 의무화하고 처리된 발현 행렬은 요구하지 않으므로, 많은 소규모 데이터셋은 단일-세포 수준 annotation 없이 공개된다.

- **선행 접근 A — reference label transfer** (SingleR, scType, CellTypist): 고품질 reference dataset의 레이블을 새 데이터셋으로 전달한다. 구현이 간단하고 대규모 적용이 가능하나, (1) reference에 없는 novel cell type을 발견하지 못하고, (2) 희귀 cell type 비율이 낮아 reference에서 드물게 등장하면 annotation 정확도가 급감한다. 또한 cross-tissue reference 데이터가 없으면 적용 범위가 제한된다.

- **선행 접근 B — LLM-based annotation** (GPTCelltype, ref 7): marker gene list를 LLM에 입력해 cell cluster에 레이블을 붙인다. reference 의존성을 없애고 novel cell type 발견이 가능하지만, 논문에서 사용한 전처리 파라미터·클러스터링 세분성을 반영하지 않아 저자의 생물학적 판단과 불일치가 생기고, 배치 보정 단계와 연결되지 않는다. LLM에 논문 맥락을 제공하지 않으면 hallucination과 generic annotation 경향이 있다.

- **선행 접근 C — 통합 배치 보정** (scanorama [ref 8], cellhint [ref 9]): 여러 데이터셋을 임베딩 공간에서 정렬한다. 하지만 기존 방법은 annotation 정보를 배치 보정 과정에 반영하지 않아, 서로 다른 cell type의 군집을 과도하게 병합(over-integration)하거나 rare cell type을 소수 집단에서 소거하는 경향이 있다.

- **이 논문으로 이어지는 gap**: 논문 본문에 있는 전처리 파라미터와 marker gene 정보를 자동 추출해서 annotation을 먼저 완성한 뒤, 그 annotation을 배치 보정에 prior로 주입하는 통합 파이프라인이 없었다. 또한 LLM annotation의 variability를 실용적 수준에서 quantify하고 관리하는 framework가 부재했다.

### 기본 개념

- **LLM agent**: 여기서는 구조화된 출력(JSON/YAML)을 생성하고 외부 도구(scanpy API)를 호출하도록 prompt가 설계된 LLM. 단순 텍스트 생성이 아니라 파라미터 추출 → 코드 실행 → 결과 반영 루프를 수행한다. 이 논문에서는 GPT-4o-mini, Deepseek-v2.5, Claude-3.5-Sonnet 3종을 지원한다.

- **Mutual Nearest Neighbor (MNN) 기반 배치 보정**: 서로 다른 batch에서 임베딩 거리가 가장 가까운 세포쌍을 anchor로 삼아 임베딩을 정렬한다. scanorama가 이 방식을 사용한다. 핵심 약점은 세포 유형 정보 없이 거리만으로 MNN을 계산하므로, 다른 세포 유형의 세포가 neighbor로 잘못 선택될 수 있다는 점이다.

- **Text-to-embedding similarity**: cell type 이름 문자열을 임베딩 벡터로 변환한 뒤 cosine similarity로 annotation 정확도를 측정하는 방법. OpenAI text-embedding-3-large 모델(Azure API)을 사용. 동의어·약어를 부분적으로 처리할 수 있으나 일반 목적 모델에서는 생물학적 specificity가 낮다는 한계가 있다. 이 논문은 이 metric을 핵심 평가 기준으로 사용.

- **Cell Ontology**: 세포 유형 간 계층적 관계를 표준화한 온톨로지. annotation 정확도를 ontology 수준으로 평가하면 단순 문자열 매칭보다 계층적 유사도를 반영할 수 있다. 이 논문은 Jaccard coefficient를 Cell Ontology 전체 노드에 계산하는 방식 사용.

### 이 논문의 필요성

- **핵심 이유**: 공개 scRNA-seq 데이터의 annotation 부재 문제를 해결하기 위해 논문 자체를 정보 소스로 활용하는 전략이 필요하다.
- **기존 방법으로 부족했던 지점**: reference transfer는 novel cell type에, GPTCelltype은 논문 맥락 통합과 배치 보정 연계에 한계가 있었다.
- **이 논문이 해결하려는 방향**: 논문 PDF → LLM agent 파라미터 추출 → annotation → annotation-prior 배치 보정의 완전 자동화 파이프라인 구축.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 논문 PDF + raw count matrix(h5ad 형식) → 세포 유형 annotation이 완료된 processed AnnData + 다수 데이터셋의 annotation-aware integrated embedding
- **입력**: (1) 논문 PDF, (2) raw count matrix (h5ad, cell barcode × gene), (3) batch key (`obs` field에 filename 등으로 지정)
- **출력**: (1) 처리 파라미터 config 파일 + reasoning log, (2) annotation 포함 processed h5ad, (3) multi-dataset integrated embedding
- **추정 대상**: 클러스터별 cell type 레이블, confidence level (LLM self-reported), sample tissue origin, disease state, developmental stage
- **중요한 hidden assumption**: 논문 PDF에 실제 전처리 파라미터와 marker gene 정보가 기술되어 있어야 LLM 추출이 의미 있다. 파라미터가 명시되지 않은 경우 LLM은 default값으로 fallback하고 log에 기록한다.

### 확률 / 통계학적 구조

**LLM annotation 단계** — stochastic. LLM 출력이 run마다 달라질 수 있으므로 저자는 confidence level을 cell cluster마다 출력하여 불확실성을 정량화한다. Confidence level이 낮은 클러스터에서 두 번째 annotation round(re-annotation)를 수행하는 self-reflective 루프.

**Scanorama-prior 수식 (MNN 거리 가중)**:
$$d'_{ij} = d_{ij} / M_{IJ}$$
$d_{ij}$: cell $i$와 cell $j$ 사이의 raw embedding distance. $M_{IJ}$: cell type $I$와 cell type $J$ 사이의 text-to-embedding cosine similarity. annotation이 유사할수록 $M_{IJ}$가 크고 $d'_{ij}$가 작아져, 같은 cell type끼리 MNN 후보로 선택될 확률이 높아진다. 일반적으로 text-to-embedding cosine distance는 0.3 이상이므로 extreme outlier를 도입하지 않는다.

**Scanorama-prior 수식 (군집 중심 displacement bias)**:
$$\text{Bias}'_{ij} = \text{Bias}_{ij} + M_{IJ} \times (v_i - v_I - v_j + v_J)$$
$v_i$: cell $i$ 임베딩, $v_I$: cell type $I$ 평균 임베딩, $v_j$: target cell $j$ 임베딩, $v_J$: target cell type $J$ 평균 임베딩. annotation 일치도($M_{IJ}$)가 높을수록 군집 단위로 target 위치로 이동하여 biological structure가 보존된다.

**Cellhint-prior 수식 (adaptive prior weighting)**:
$$S'_{ij} = \beta[(1-\alpha_i)S_{ij} + \alpha_i M_{IJ}] + (1-\beta)S_{ij}$$
$S_{ij}$: cell $i$와 cell type $J$ 사이의 raw similarity. $\alpha_i$: cell $i$의 clarity score의 inverse — 불확실할수록 prior 비중 증가. $\beta$: prior 효과 강도 hyperparameter (default 0.1). clarity score는 cell $i$의 발현 프로파일을 전체 cell type에 대한 softmax 유사도 entropy로 측정. 발현이 애매한 세포(low clarity)일수록 prior annotation에 더 의존하도록 adaptive하게 설계.

**Model family**: deterministic graph-based batch correction에 annotation similarity를 weight로 주입하는 hybrid 방식. 생성 모델이 아니라 similarity-weighted neighbor construction.

**Noise / sparsity 처리**: LLM annotation의 noise 내성을 실험적으로 검증 — (1) similar naming (alias), (2) unbiased incorrect naming, (3) biased incorrect naming의 3가지 시나리오. scanorama-prior는 시나리오 1·2에서 robust, 시나리오 3(biased mislabeling)에서 성능 저하. cellhint-prior는 3개 시나리오 모두에서 cell type harmonization tree 구조를 유지 (Fig. S12A–C, S12F).

### 핵심 method insight

- **기존 방법의 한계**: scanorama는 세포 간 raw distance만으로 MNN을 구성하므로 annotation 정보가 없다. 다른 cell type이더라도 임베딩 거리가 가까우면 MNN에 선택되어 over-integration이 발생.
- **이 논문이 바꾼 가정**: annotation similarity $M_{IJ}$를 distance modifier로 사용하면 같은 cell type끼리의 MNN 선택 확률을 높이면서 다른 cell type 사이의 bridge를 약화할 수 있다.
- **새로 추가한 구조**: (1) LLM annotation → similarity matrix → 배치 보정 연결 파이프라인. (2) cellhint-prior의 clarity score 기반 adaptive weighting.
- **이 변화가 중요한 이유**: rare cell type이 majority cell type에 흡수되지 않고 독립적 cluster를 유지하면서도 cross-dataset annotation이 harmonized된다.

### 이전 방법과의 차이

- **Baseline**: scanorama (원본), cellhint (원본), SingleR, scType, CellTypist, GPTCelltype
- **공통점**: scanorama-prior는 scanorama의 MNN 프레임워크를 그대로 사용. cellhint-prior는 cellhint의 cluster-level integration 프레임워크를 유지.
- **차이점**: annotation-derived similarity matrix $M_{IJ}$를 MNN distance 또는 cellhint similarity에 prior로 주입. LLM annotation 단계를 배치 보정 전 upstream으로 통합.
- **차이가 크게 나타나는 조건**: dataset 수가 많고(>4) cell 수가 중간 규모(50k~250k)일 때 scanorama-prior가 가장 유리. Cell 수가 매우 많거나(>200k) dataset 수가 적을(≤4) 때는 cellhint-prior 단독이 우월. 저자가 명시적으로 실용 권고를 제시.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: cellxgene 18개 dataset, 췌장 multi-platform (5개), Immune ALL 33k cells (5 datasets), Blood 336k cells (4 datasets), HCLA 585k cells (14 datasets)
- **Metric**: text-to-embedding cosine similarity (cell/group level), Cell Ontology Jaccard, Adjusted Rand Index, KMeans ARI, Silhouette label score, iLISI, kBET
- **개선된 결과**: scExtract는 18개 dataset 전체에서 text-to-embedding 기반 group-level 정확도가 현행 방법보다 높음 (Wilcoxon p < 10⁻¹³). Fig. 2H/I에서 scExtract vs. GPTCelltype p < 5×10⁻⁵.
- **Ablation 근거**: Fig. 2F — 배경 지식 없는 scExtract(no context)는 context가 있는 scExtract보다 정확도 낮음 (p = 0.009, 0.003, 0.02 for 3 LLM models). 배경 지식 통합이 성능의 핵심 요소.
- **정성적 효과**: 비용·시간 효율 — 데이터셋 1건당 20분 이내, $1 미만 (Fig. S3E). GPU 불필요 (API만으로 동작).

### Processing pipeline 세부 5단계

**(1) Filtering**: 기본값 min_genes = 300 (10X Chromium 기준). 논문에 명시된 경우 mitochondrial/ribosomal gene 비율, genes per cell 상한 추가 적용. 명시되지 않은 파라미터는 default 유지.

**(2) Preprocessing**: 고변이 유전자(HVG) 수, kNN graph 크기, harmonypy 기반 sample-level batch correction 여부를 논문에서 추출. 나머지는 scanpy default.

**(3) Clustering**: Leiden 또는 Louvain + estimated cluster 수를 논문에서 추출 또는 LLM이 cell population 수 기반 추론. 더 정교한 모델일수록 cluster 수 추정이 정확해지는 경향.

**(4) Annotation**: Wilcoxon rank-sum test로 top 10 HVG per cluster 선정 → LLM이 cell type, confidence level, sample tissue origin, disease state, developmental stage를 출력. 이전 question-answering cache context를 초기화하고 annotation 전용 tool model로 전환하여 비용 절감. Annotation은 inherent variability가 있으므로 log 검토 권고.

**(5) Re-annotation (optional)**: LLM이 low-confidence cluster에 대해 tissue/cell type context 기반으로 characteristic marker gene을 선정 → 해당 genes의 cluster별 발현량 query → 재annotation. 발현 데이터는 LLM이 직접 처리하지 못하므로 tool model이 natural language로 요약한 뒤 LLM에 입력.

### Integration pipeline (2단계)

**Step 1 — Cellhint-prior**: 인접 데이터셋을 reference로 삼아 cell type harmonization tree 구성 → annotation nomenclature 불일치 수정. text-to-embedding 접근의 유연성으로 harmonized cell type에서 similarity matrix 도출.

**Step 2 — Scanorama-prior**: harmonized annotation에서 유도한 $M_{IJ}$ matrix로 MNN 가중 거리 조정 + cluster center displacement bias 적용 → embedding-level batch correction.

**실용 권고** (저자 제시): 평균 cell 수/dataset > 50,000 이거나 dataset 수 < 4이면 cellhint-prior 단계에서 중단. Standard cell type 명칭은 description 추가 없이도 충분한 prior 정보를 제공 (Fig. S16A–B).

### Method 관점의 한계

- **약한 assumption**: annotation similarity를 거리 modifier로 쓰는 것은 annotation이 대체로 정확하다는 전제에 의존. biased incorrect annotation 시나리오에서 scanorama-prior 성능 저하.
- **구현 / 학습상의 부담**: LLM API 비용이 데이터셋 수·복잡도에 비례. 여러 데이터셋이 포함된 복잡한 manuscript, unpublished manuscript, custom algorithm 시나리오에서 reproducibility 저하 (Fig. S4C).
- **일반화가 불확실한 조건**: 논문에 파라미터가 기재되지 않은 경우 default값 사용. 혈액 sample은 고형 조직보다 annotation consistency 낮음 (Fig. S5A). domain-specific embedding 모델 없이는 annotation 정확도가 모델 특성에 의존.

---

## Results

### Dataset별 결과

#### Dataset 1 — cellxgene benchmark (annotation accuracy)

- **Dataset**: 18개 manually annotated datasets from cellxgene (21개에서 distinct cell type이 없는 3개 제외). 다양한 human tissue (liver, kidney, intestine 등). 셀 규모 ~10⁴/dataset.
- **목적**: LLM-based annotation vs. reference transfer 방식 annotation accuracy 비교.
- **사용한 데이터 규모**: 18개 dataset. 개별 dataset n 미제공 (cellxgene 기준 typically < 50k cells/set).
- **Baseline / 비교 대상**: SingleR (HumanPrimaryCellAtlas), scType, CellTypist v1.6.3, GPTCelltype. LLM provider 3종: Deepseek-v2.5, GPT-4o-mini, Claude-3.5-Sonnet.
- **Metric / 평가 기준**: (1) text-to-embedding cosine similarity (cell-level 및 group-level), (2) Cell Ontology Jaccard similarity, (3) Adjusted Rand Index (ARI).
- **주요 수치**:
  - Text-to-embedding group-level accuracy: scExtract > scExtract(no context) > GPTCelltype (Fig. 2H, p < 5×10⁻⁵ by Wilcoxon signed-rank test).
  - Cell Ontology similarity: scExtract > scExtract(no context) ≈ GPTCelltype (Fig. 2I, p = 0.018).
  - ARI group-based mean: scExtract(Claude 3.5) — lowest ARI 중 하나 (Claude 3.5가 세분화된 annotation을 선호하므로 clustering structure와의 ARI가 낮아짐). 절댓값 수치 본문 미기재.
  - LLM provider 간 성능: Claude 3.5 > Deepseek v2.5 > GPT-4o-mini (정확도 순).
  - 배경 지식 추가 효과: p = 0.009, 0.003, 0.02 (Deepseek, Claude, GPT-4o-mini 각각, Fig. 2F Wilcoxon).
  - Annotation accuracy vs. confidence level: 양의 상관 (Fig. 2G).
- **정성 결과**: group-level annotation method(scExtract, scType)가 single-cell-level method(SingleR, CellTypist)보다 annotated cell type 수에서 실제 논문 보고값과 더 높은 Pearson 상관 (Fig. 2B). SingleR/CellTypist는 single-cell noise로 cell type 수를 과대 추정.
- **논문 주장과의 연결**: article-derived prior knowledge가 annotation 정확도를 유의하게 향상. confidence level이 실제 accuracy를 반영 → LLM 불확실성 정량화 가능.
- 해석: text-to-embedding metric은 OpenAI general embedding 모델을 사용하므로 언어적 유사도와 생물학적 유사도가 혼재할 수 있음. 동일 18개 dataset이므로 독립 cohort 재현성 검증은 별도 필요.

---

#### Dataset 2 — 췌장 multi-platform benchmark (integration)

- **Dataset**: 5개 pancreas scRNA-seq datasets (inDrop × 3, Smart-seq2, Fluidigm C1). 플랫폼 간 batch effect가 큰 표준 benchmark. n 미제공 (typical benchmark ~10k cells).
- **목적**: scanorama-prior vs. scanorama 원본 integration 성능 비교; cellhint-prior vs. cellhint 비교.
- **Baseline / 비교 대상**: PCA, scanorama, scanorama-prior, cellhint, cellhint-prior.
- **Metric**: scib_metrics 기반 — batch correction (iLISI, kBET) + biological conservation (KMeans ARI, Silhouette, NMI). knn = 30, UMAP default params.
- **주요 수치**: Fig. 3B 표에서 scanorama-prior total score > scanorama total score. 절댓값 수치 본문 미기재 (Fig. 3B에 시각적으로만 제시). cellhint-prior가 inDrop-Smart-seq2-Fluidigm C1 간 alignment 개선 (Fig. 3D, E).
- **정성 결과**: scanorama-prior는 Leiden clustering resolution = 0.7 사용 시 cell type 분리 구조가 batch 기반 분리보다 명확 (Fig. 3A). cellhint-prior는 inDrop series에 기존 cellhint가 어려움을 겪던 Smart-seq2/Fluidigm C1 통합을 개선.
- **논문 주장과의 연결**: annotation prior가 배치 보정 과정에서 biological diversity를 보존한다는 주장을 정량적으로 지지.

---

#### Dataset 3 — 대규모 multi-dataset integration (3개 atlas 규모)

- **Dataset**:
  - A: Immune ALL — 33,506 cells, 5 datasets, 16 cell types
  - B: Blood — 335,916 cells, 4 datasets, 24 cell types
  - C: HCLA (Human Lung Cell Atlas 부분집합) — 584,944 cells, 14 datasets, 50 cell types
- **목적**: scExtract two-step pipeline의 확장성 및 규모별 method 선택 guideline 도출.
- **Baseline / 비교 대상**: PCA, cellhint, cellhint-prior, scanorama, scanorama-prior.
- **Metric**: KMeans ARI, Silhouette label score, iLISI, kBET (Fig. 4).
- **주요 수치**:
  - Immune ALL (5 datasets): scanorama-prior > scanorama (bio conservation 측면). 절댓값 수치 본문 미기재.
  - Blood (4 datasets): cellhint-prior ≈ cellhint >> scanorama-prior, scanorama (Fig. 4B). 저자 설명: high cell count + few datasets → graph-based approach 유리.
  - HCLA (14 datasets): scanorama-prior 선두, prior-enhanced 방법과 원본 간 gap 확대 (Fig. 4C).
- **정성 결과**: GPU(V100) 사용 시 scanorama-prior가 ~1M cells까지 확장 가능 (Fig. S15B). cellhint-based 방법은 대규모 concatenated dataset에서 원본 논문 대비 긴 실행시간 — 저자 설명: 원본은 downsampling benchmark, 이 논문은 concatenation으로 다른 조건.
- **논문 주장과의 연결**: dataset 수가 많을수록 embedding-based scanorama-prior의 prior 효과가 커진다는 실용적 guideline.

---

#### Dataset 4 — 피부 skin atlas (440,000 cells, 14 datasets)

- **Dataset**: 20개 후보에서 선별된 14개 human skin scRNA-seq datasets (psoriasis, atopic dermatitis, acne, granuloma annulare, healthy 포함). 60,000 cells 초과 dataset은 downsampling. Claude 3.5 사용.
- **목적**: scExtract 전자동 파이프라인으로 대규모 disease atlas 구축 및 novel biological finding 실증.
- **사용한 데이터 규모**: 440,108 cells (Fig. 5A caption 기준).
- **Baseline**: 없음 (application study).
- **주요 수치**:
  - CXCL14⁺ psoriatic proliferating keratinocyte 비율: 건선 35→58% (본문 기술), 반면 healthy cells 27→13% (Fig. 6I pseudo-bulk expression 기반).
  - ILC marker KLRB1 발현: neonatal skin에서 타 disease state 대비 고발현 (Fig. 5G).
  - T cell disease-specific pattern: AD에서 IL13/IL22 발현 증가, psoriasis에서 IL17 family, granuloma annulare(GA)에서 IFNG (Fig. 5H).
  - Psoriasis keratinocyte(cluster 0): COL17A1 고발현, IGFBP3 고발현 (basal layer marker, 기존 IHC 연구 [ref 56]와 일치).
- **정성 결과**: scExtract two-step scanorama-prior가 원본 scanorama 대비 proliferating keratinocyte subpopulation(cluster 0 vs. cluster 3)을 multi-batch에서 정확하게 분리. 원본 scanorama는 두 subpopulation을 batch 기반으로 분리 (Fig. 6D vs. 6E).
- **논문 주장과의 연결**: 전자동 atlas 구축이 수동 처리 없이 novel subpopulation을 발굴하는 생물학적 발견 능력 실증.

---

#### Dataset 5 — output stability 및 prompt sensitivity

- **Dataset**: Sample 1 (blood), Sample 11 (solid tissue), Sample 19 (solid tissue). 각 6회 반복.
- **목적**: LLM 출력의 재현성과 prompt 변형 내성 측정.
- **Prompt variants**: Instruction_Reordering, Terminology_Modification, Enhanced_Guidance, Minimalistic_Annotation, Structural_Reformatting (5종).
- **주요 결과**:
  - 파라미터 extraction: 명시된 파라미터에서 높은 일관성. non-critical 파라미터에서 variability 발생, default 처리.
  - Annotation consistency: 고형 조직(Sample 11, 19) > 혈액(Sample 1). Ambiguous marker profiles를 가진 cell subpopulation에서 variability 집중.
  - Strict reproducibility ranking: GPTCelltype > scExtract(no context) > scExtract. 단, 이 순위는 annotation 세분성과 반비례 — context 사용 시 novel subtype 발견 가능하나 variability 증가.
  - Prompt sensitivity: Claude 3.5 Sonnet이 Deepseek v3보다 simplified prompt에서도 일관성 높음 (Fig. S10A–B). Advanced model은 prompt 변형에 더 robust (Fig. S11A–B).
- **논문 주장과의 연결**: scExtract는 well-defined 파라미터와 cell type에서 robust한 재현성. Variability는 모호한 데이터 해석이 필요한 시나리오에서 집중되며, confidence level이 이를 반영.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: article context 통합이 annotation 정확도를 모든 비교에서 향상. Prior-aware integration이 biological diversity preservation과 batch correction을 동시에 개선. Dataset 수가 많을수록 prior 효과 증대.
- **가장 중요한 수치**: Fig. 2H에서 scExtract vs. GPTCelltype Wilcoxon p < 5×10⁻⁵. Fig. 2F에서 배경 지식 추가 효과 p < 0.02. 피부 atlas CXCL14⁺ psoriatic keratinocyte 35→58% subpopulation 비율.
- **Baseline 대비 차이**: reference transfer 방식 대비 annotation 정확도 우위. 원본 scanorama/cellhint 대비 prior-aware version이 biological conservation 지표 상위.
- **결과 해석 시 주의점**: 본문에 절댓값 metric 수치가 Figure에만 제시되고 텍스트에 정리되지 않은 경우 다수. cellxgene curator 레이블을 ground truth로 사용하므로, 해당 레이블 자체의 오류가 accuracy 평가에 영향. Integration 성능의 규모 의존성(scanorama-prior vs. cellhint-prior 분기점)은 경험적 관찰이며 theoretical justification 없음.

---

## Figures

### Figure 1

- **이 Figure가 필요한 이유**: scExtract의 전체 pipeline과 novel 구성요소(scanorama-prior, cellhint-prior)의 직관적 원리를 한 눈에 보여주기 위해.
- **이 Figure가 뒷받침하는 주장**: scExtract가 기존 방식보다 더 완전한 자동화 pipeline을 제공하며, prior annotation 정보가 integration 품질을 개선한다는 개념적 근거.

#### 패널별 설명
- **a**: 연도별 신규 scRNA-seq 논문 수(파란색 bar)와 cellxgene 등재 annotation 데이터셋 수(주황색 bar) 비교. 논문 수는 수천 건이나 annotated dataset은 수백 건 — annotation gap의 규모.
- **b**: scExtract 전체 workflow 개요도. 논문 + raw expression matrix → LLM agent 필터링·전처리·클러스터링·annotation → cellhint-prior harmonization → scanorama-prior embedding integration.
- **c**: scanorama-prior가 prior 없는 scanorama 대비 cell type separation을 개선하는 원리 scatter plot. "Without Prior": cell type A/B 혼합, "With Prior": annotation similarity 기반 분리.
- **d**: scanorama vs. scanorama-prior의 MNN displacement 비교. "With Group Center Bias": scanorama-prior가 군집 중심 단위로 이동 → internal structure distortion 감소.
- **e**: cellhint-prior의 uncertainty-adaptive prior weighting 개념도. High Certainty → expression-based similarity 우선, Low Certainty → prior annotation similarity 비중 증가.

#### 본문에서 강조한 비교
- Panel c, d: scanorama vs. scanorama-prior에서 prior가 cell type-specific MNN 선택을 강화한다는 개념 제시.

#### 해석 시 주의점
- Panel c, d는 conceptual illustration. 실제 데이터에서의 효과는 Fig. 3, 4에서 정량화.

---

### Figure 2

- **이 Figure가 필요한 이유**: scExtract annotation 정확도를 기존 방식 4종과 다면적으로 비교하여 annotation accuracy 주장의 핵심 수치 근거 제공.
- **이 Figure가 뒷받침하는 주장**: article-based prior knowledge를 활용한 LLM annotation이 reference transfer 방식보다 전반적으로 우수하다.

#### 패널별 설명
- **a**: cellxgene 18개 benchmark dataset 선택 흐름 (21개 → 3개 제외 → 18개).
- **b**: 각 방법으로 annotated된 cell type 수 vs. 실제 논문 보고 cell type 수 상관 dot plot. scExtract·scType 높은 Pearson r. SingleR·CellTypist 과대 추정.
- **c**: ARI box plot. Group-based mean ARI > single-cell-based ARI. Claude 3.5 scExtract: 세분 annotation 경향으로 구조적 ARI 낮음.
- **d**: text-to-embedding similarity 비교 (18개 dataset, cell-level + group-level). scExtract가 모든 비교 방법 대비 상위. p-value from Wilcoxon.
- **e**: cell type 빈도 vs. annotation accuracy. 모든 방법에서 rare cell type (<1%) accuracy 감소. scExtract 상대적 우위 유지.
- **f**: 배경 지식 유무에 따른 annotation accuracy 개선 box plot. 3개 LLM 모두 유의한 향상 (p = 0.009, 0.003, 0.02).
- **g**: confidence level vs. accuracy. 양의 상관 → LLM self-reported confidence의 신뢰성.
- **h, i**: Claude 3.5 기준 4개 방법 비교. h = text-to-embedding, i = Cell Ontology similarity. p values 명시.
- **j–n**: 신장 dataset UMAP visualization. j = reference (cellxgene), k = scExtract(Claude 3.5), l = SingleR, m = SingleR similarity, n = scExtract 두 번째 복제.

#### 본문에서 강조한 비교
- scExtract(text-to-embedding) vs. GPTCelltype: p < 5×10⁻⁵ (Fig. 2H). 성능 hierarchy: scExtract > scExtract(no context) > GPTCelltype.
- 신장 dataset에서 SingleR이 heterogeneous populations를 동일 세포 유형으로 잘못 분류하는 반면, scExtract는 annotation granularity 유지 (Fig. 2J vs. 2K, 2L).

#### 해석 시 주의점
- Claude 3.5가 ARI 최저(세분화 선호)이나 text-to-embedding 정확도 최고인 역설 — ARI는 clustering granularity에 민감하므로 annotation accuracy와 동시 최적화 어려움.
- 두 번째 복제(Fig. 2N)에서 PT_VCAM1 subtype을 정확하게 식별 — stochastic 재현성 시연이나 일부 subtype은 여전히 미식별.

---

### Figure 3

- **이 Figure가 필요한 이유**: 표준 benchmark(췌장 multi-platform)에서 scanorama-prior와 cellhint-prior의 integration 성능을 정량적으로 검증.
- **이 Figure가 뒷받침하는 주장**: prior-informed integration이 batch correction과 biological conservation 모두 개선.

#### 패널별 설명
- **a**: UMAP 비교 (상: scanorama, 하: scanorama-prior). Column 1: batch, Column 2: cell type, Column 3: Leiden clustering. scanorama-prior가 cell type 단위 더 명확한 분리.
- **b**: 종합 integration metric 표 + bar plot (PCA, scanorama_prior_scanorama, k_scanorama, k_scanorama_prior, k_pure). scanorama-prior 총점 우위.
- **c, d**: cellhint (c) vs. cellhint-prior (d) cell type harmonization tree. cellhint-prior가 inDrop-Smart-seq2-Fluidigm C1 간 alignment 개선.
- **e**: UMAP (cellhint 상단, cellhint-prior 하단). batch separation 감소 + cell type 분리 유지.

#### 해석 시 주의점
- 췌장 benchmark는 소수 platform 조합. 절댓값 metric 수치 본문 미기재.

---

### Figure 4

- **이 Figure가 필요한 이유**: 실제 규모 데이터(33k–585k cells, 4–14 datasets)에서 scExtract two-step integration의 확장성 검증.
- **이 Figure가 뒷받침하는 주장**: dataset 수가 많을수록 scanorama-prior가 선두, cell 수 많고 dataset 적으면 cellhint-prior가 선두.

#### 패널별 설명
- **a**: Immune ALL (33,506 cells). UMAP (5종 방법) + metric bar plots. scanorama_prior > scanorama in bio conservation.
- **b**: Blood (335,916 cells). cellhint_prior, cellhint 우세. scanorama 저성능.
- **c**: HCLA (584,944 cells). scanorama_prior 선두. prior-enhanced 방법과 원본 간 gap 지속 확대.

#### 본문에서 강조한 비교
- HCLA (14 datasets): scanorama-prior leading position, 원본 대비 "increasingly larger advantages" (본문 기술).
- Blood (4 datasets): cellhint-prior ≈ cellhint significantly outperform others (본문 기술).

#### 해석 시 주의점
- 절댓값 metric 수치 본문 미기재. GPU 가속(use_gpu=True, CuPy)으로 scanorama-prior의 시간 복잡도 문제 부분 해소 가능.

---

### Figure 5

- **이 Figure가 필요한 이유**: scExtract가 생성한 피부 440k-cell atlas의 생물학적 타당성과 발견 능력을 실증.
- **이 Figure가 뒷받침하는 주장**: 전자동 pipeline이 이전 연구와 일치하는 결과를 내면서 새로운 생물학 발견을 가능하게 한다.

#### 패널별 설명
- **a–c**: 440k cells 통합 UMAP. a = major cell type (voting annotation), b = dataset source, c = disease state + age.
- **d**: dataset별 정규화 cell type 분포 bar plot.
- **e**: major cell type별 marker gene 발현 dot plot.
- **f**: T cell subpopulation UMAP (8개 subtype).
- **g**: KLRB1 violin plot (ILC marker). neonatal skin에서 고발현.
- **h**: T cell marker gene heatmap (disease state × gene). AD: IL13/IL22, psoriasis: IL17 family, GA: IFNG.

#### 본문에서 강조한 비교
- KLRB1 neonatal 고발현: 기존 연구(ref 39)와 일치 → automated pipeline의 생물학적 타당성.
- Disease-specific T cell pattern: 각 condition별 signature와 일치.

#### 해석 시 주의점
- major_vote 통합 과정에서 minority annotation 소거 가능. Fig. S19C에 automated vs. original annotation 일치도 비교 있으나 정확 수치는 supplementary에만.

---

### Figure 6

- **이 Figure가 필요한 이유**: 건선 특이적 CXCL14⁺ proliferating keratinocyte subpopulation 발굴이라는 구체적 biological discovery 제시.
- **이 Figure가 뒷받침하는 주장**: scExtract two-step integration이 원본 scanorama보다 rare subpopulation을 정확하게 cluster해 novel discovery를 가능하게 한다.

#### 패널별 설명
- **a**: keratinocyte differentiation trajectory UMAP (disease별). psoriasis에 inflammatory branch, AD는 두 branch 사이 intermediate.
- **b**: KRT10 violin plot. AD에서 비율 높으나 발현 수준 낮음 (분화 진행 but 분화도 낮음).
- **c**: keratinocyte subpopulation UMAP (marker gene overlay). COL17A1, KRT5, KRT1, KRT10 분화 단계별.
- **d**: scExtract scanorama-prior embedding에서 proliferating keratinocyte 2개 subpopulation 분리 성공.
- **e, f**: 원본 scanorama embedding에서 두 subpopulation이 분리되지 않고 batch 기준으로 분리.
- **g**: proliferating keratinocyte subcluster별 disease 구성 비율 (cluster 0,1,6: psoriasis, cluster 4: AD, cluster 2,7: shared).
- **h**: subcluster별 marker gene heatmap.
- **i**: pseudo-bulk expression box plot (MKI67, COL17A1, IGFBP3, CXCL14 across subclusters).

#### 본문에서 강조한 비교
- CXCL14⁺ psoriatic keratinocyte 비율: 35→58% (건선), healthy 27→13% (본문 기술, Fig. 6I 기반).
- COL17A1 고발현: proliferative pressure에 의한 selection pressure 가설.
- IGFBP3 고발현: 기존 IHC 연구(ref 56)와 일치.

#### 해석 시 주의점
- Pseudo-bulk 분석(decoupleR v1.6.0). 인과관계 증명 아님. CXCL14⁺ keratinocyte의 기능적 역할은 추가 실험 필요. cluster 0의 anti-inflammatory CXCL14 고발현 패턴이 역설적으로 anti-inflammatory function인지 altered program인지 미확정.

---

## Tables

본문에 독립적인 정식 Table 없음. Table은 Figure 내 embedded 형식으로만 제공:

- **Fig. 3B (embedded table)**: 췌장 dataset benchmark에서 5개 integration method × 종합 metrics 비교. Row: method, Column: bio conservation, batch correction, total score. 색상 heatmap으로 표시. 수치 본문 미기재, figure에서만 확인 가능.
- **Additional file 2 (Table S1)**: cellxgene benchmark 18개 dataset list + accession (별도 Zenodo 파일).
- **Additional file 3 (Table S2)**: prompt variation 실험에 사용한 5종 prompt variant 전문.
- **Additional file 4 (Table S3)**: 피부 atlas 구축에 사용한 14개 dataset 목록 + accession.

---

## Supplementary Information

- **Additional file 1 (Fig. S1–S19)**: 전체 supplementary figure 모음. 주요 내용:
  - S1A: Cell Ontology 기반 annotation accuracy 비교 (main Fig. 2H/I와 일관된 결과).
  - S1B–D: 신장 dataset 두 번째 annotation round에서 SLC26A7/SLC26A4 기반 intercalated cell subdivision.
  - S2A–B: 배경 지식 오염(confounding content) 비율과 annotation accuracy 관계 — Claude 3.5는 오염에 상대적으로 robust.
  - S3A: Deepseek v2.5 / GPT-4o-mini annotation이 Claude 3.5보다 generic annotation 경향.
  - S3E: 비용/시간 benchmark — 데이터셋당 20분 이내, $1 미만.
  - S4A–C: preprocessing parameter extraction consistency (6회 반복). 복잡한 manuscript에서 variability 증가.
  - S5A–B: annotation consistency (고형 조직 > 혈액).
  - S6A: reproducibility ranking (GPTCelltype > scExtract(no context) > scExtract).
  - S9A–B: methods lacking article context가 novel cell subtypes 식별 실패.
  - S10A–B: prompt variation → Claude 3.5 Sonnet이 simplified prompt에서도 일관.
  - S11A–B: advanced model이 prompt variation에 더 robust.
  - S12A–C, S12F: annotation error scenario (fuzzy / unbiased error / biased error) 하에서 scanorama-prior / cellhint-prior 성능. scanorama-prior는 biased error에서 저하, cellhint-prior는 모든 시나리오 tree structure 유지.
  - S13A–F: label change 실험. scanorama-prior with cellhint-prior harmonization이 robust.
  - S14A–E: embedding level에서 annotation error tolerance 확인.
  - S15A–B: 시간 복잡도 (PC vs. V100 GPU). GPU로 ~1M cells까지 확장.
  - S16A–B: "cell type" vs. "cell type: description" similarity matrix — 차이 없음 (standard 명칭으로 충분).
  - S17A–C: Figs. 4A–C에 해당하는 추가 metric plots.
  - S18: scExtract(no context) 통합 결과. scanorama-prior standard cell types와 original scanorama 사이 성능.
  - S19A–C: 피부 atlas annotation validation.

---

## 분석 자체에 대한 메모

- annotation accuracy 평가에 사용한 text-to-embedding metric이 OpenAI general embedding 모델 기반이라는 점은 biological specificity 측면에서 주의 필요. 저자도 Discussion에서 domain-specific model 개발 필요성 언급.
- ground truth로 사용된 cellxgene curator 레이블 자체에 annotation 오류 가능성 있음.
- Fig. 3B embedded table의 수치가 본문에 없어 정확한 성능 gap 확인이 어려움. 재현 시 scib_metrics 계산 코드 확인 필요.
- 저자 2인(Y.W., F.T.). Y.W.가 code 설계 + bioinformatics 실험 주도. Fuchou Tang은 single-cell genomics 분야 저명 PI (Peking University). 코드·데이터 전부 GitHub + Zenodo 공개 → 재현성 높음.
