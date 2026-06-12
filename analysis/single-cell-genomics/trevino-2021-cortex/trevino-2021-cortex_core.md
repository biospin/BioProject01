# Trevino 2021 — Developing Human Cortex Multi-ome — Core Analysis

## Executive Summary

- **무엇**: developing human cerebral cortex에서 gene expression과 chromatin accessibility를 single-cell 해상도로 연결해 corticogenesis의 regulatory element activity와 ASD noncoding mutation impact를 해석한 Cell paper.
- **모델 / 방법**: scRNA-seq, scATAC-seq, joint multi-omic assay를 결합하고, linked regulatory element와 gene expression의 상관 및 base-pair-resolution neural network scoring으로 cell-type-specific regulatory disruption을 평가.
- **핵심 결과**:
  - ① **Corticogenesis atlas** — abstract 기준, gene expression과 chromatin accessibility의 single-cell atlas를 만들고 continuous differentiation trajectory에서 regulatory wave를 관찰.
  - ② **TF-regulatory coupling** — lineage-determining TF는 linked regulatory element activity와 gene expression 간 강한 상관을 보이며, early differentiating cells에서 active chromatin state가 먼저 나타난다고 보고.
  - ③ **ASD noncoding mutation analysis** — ASD individuals의 noncoding mutations가 특정 cell type에서 enrichment되고 frequently disrupted TF binding sites가 식별됨.
- **우리 적용**: `methodology-reference`와 `academic-citation` 가치가 높다. `GSE162170`은 후속 multiome velocity papers에서 fetal human cortex benchmark로 재사용되는 reference dataset.
- **심층**: `sources/publisher_fulltext_excerpt.txt`로 publisher summary와 data/code availability는 고정했지만, 원문 PDF가 `sources/`에 아직 없으므로 Figure/Table의 panel-level 수치와 STAR Methods 세부는 manual PDF drop 후 재검토 필요. lens와 methodology brief 참고.

## Identity

- **Title**: Chromatin and gene-regulatory dynamics of the developing human cerebral cortex at single-cell resolution
- **Authors**: Trevino, Alexandro E. et al.
- **Year / Venue**: 2021, Cell 184(19):5053-5069.e23
- **DOI / PMID**: `10.1016/j.cell.2021.07.039`, PMID `34390642`
- **Citation key**: `@trevino2021cortex`
- **Source boundary**: `sources/abstract.txt`, `sources/publisher_fulltext_excerpt.txt`, `sources/data_GSE162170.url`, `sources/code_Brain_ASD.url`, `sources/code_brain_comp.url`, publisher URL stubs. `미제공:` local PDF `sources/trevino-2021-cortex.pdf`는 현재 없음.

## Background

### 배경 스토리

- **문제의 출발점**: Cortical development의 genetic perturbation은 ASD를 포함한 neurodevelopmental disease와 연결된다. 그러나 어떤 genomic regulatory region이 어떤 developmental cell state에서 중요하게 작동하는지는 bulk assay만으로 분해하기 어렵다 (`sources/abstract.txt`).
- **선행 접근 A**: scRNA-seq는 cell type과 differentiation state별 gene expression program을 분리한다. 한계는 regulatory element activity와 TF binding 가능성을 직접 보지 못한다는 점.
- **선행 접근 B**: scATAC-seq는 chromatin accessibility를 통해 candidate cis-regulatory elements를 잡는다. 한계는 같은 cell에서 transcript output과 regulatory state를 직접 묶지 못하면 enhancer-gene link가 간접 추론에 머문다는 점.
- **이 논문으로 이어지는 gap**: 저자는 scRNA-seq, scATAC-seq, joint multi-omic measurements를 함께 사용해 developing human cortex에서 cell type별 regulatory element activity map을 만들고, 그 map을 ASD noncoding mutation interpretation에 연결하려 한다.

### 기본 개념

- **Cis-regulatory element**: promoter/enhancer처럼 gene expression을 조절하는 noncoding genomic element. 이 논문에서는 chromatin accessibility와 linked gene expression의 관계가 핵심 신호다.
- **Lineage-determining TF**: cell lineage commitment와 differentiation program을 밀어주는 TF. abstract는 linked regulatory elements와 expression levels 사이의 강한 상관, 그리고 early differentiating cells의 active chromatin state 전환을 강조한다.
- **Base-pair-resolution neural network**: noncoding sequence 변화가 TF binding이나 chromatin signal을 얼마나 바꾸는지 위치 단위로 scoring하는 모델 계열. `검토필요:` 모델 이름, architecture, training split, held-out validation은 PDF Methods 확인 필요.

## Methods

### 자료 유형과 분석 깊이

- 이 논문은 computational method paper라기보다 experimental biology + regulatory genomics finding 중심 paper다. 따라서 method는 protocol 요약과 statistical assumption 중심으로 정리한다.
- `검토필요:` STAR Methods와 supplementary가 현재 local source에 없으므로 sample processing, QC threshold, exact model architecture, statistical test는 원문 PDF 확보 후 보강해야 한다.

### 이 method가 푸는 문제

- **Formal task**: developing human cortex의 cell states에 대해 chromatin accessibility, gene expression, regulatory element-gene link, TF activity, ASD noncoding variant impact를 cell-type-specific하게 추정.
- **입력**: scRNA-seq, scATAC-seq, joint multi-omic measurement, ASD individuals의 noncoding mutations (`sources/abstract.txt`).
- **출력**: cell type/state atlas, differentiation trajectory에 따른 regulatory waves, lineage-determining TF 후보, ASD mutation의 cell-type-specific disruption score.
- **중요한 hidden assumption**: linked regulatory element와 gene expression의 상관이 biological regulation을 반영한다는 가정. `해석:` perturbation 없이 이 연결은 causal proof가 아니라 strong association에 가깝다.

### 확률 / 통계학적 구조

- **Model family**: multi-modal single-cell integration + regulatory element-gene association + sequence-level neural network scoring.
- **Likelihood / objective**: `미제공:` abstract에는 수식, objective, loss function이 없다.
- **Prior / regularization**: `미제공:` motif prior, genomic distance prior, peak-gene linkage threshold는 abstract에 없음.
- **Inference / optimization**: `검토필요:` neural network training details, train/test split, negative control, variant scoring calibration은 PDF Methods 확인 필요.
- **Noise, sparsity, uncertainty 처리**: single-cell ATAC sparsity와 donor/cell-state imbalance 처리는 핵심 리스크지만 abstract에 구체적 절차가 없다.

### 핵심 method insight

- 단일 modality가 아니라 transcriptome과 chromatin accessibility를 함께 보면서, regulatory element activation이 gene expression과 cell fate transition보다 앞서거나 동반되는지를 developmental trajectory 위에서 해석한다.
- ASD variant analysis는 noncoding mutation을 단순 위치 annotation으로 끝내지 않고 cell-type-specific regulatory disruption으로 재해석하려는 구조다.
- `해석:` 본 프로젝트 관점의 가치는 algorithm 자체보다 `GSE162170`의 human cortex multiome reference status와 cell annotation, regulatory link benchmark에 있다.

## Results

### Dataset별 결과

#### Dataset 1 — Developing human cerebral cortex single-cell atlas

- **Dataset**: developing human cerebral cortex의 scRNA-seq, scATAC-seq, joint multi-omic measurement (`sources/abstract.txt`).
- **목적**: corticogenesis 동안 cell type/state별 gene expression과 chromatin accessibility를 같은 biological trajectory에서 해석.
- **사용한 데이터 규모**: `미제공:` abstract에는 exact cell 수, donor 수, gestational week 범위가 없다. `검토필요:` GEO `GSE162170` 및 STAR Methods에서 sample table 확인 필요.
- **주요 결과**: gene expression과 chromatin accessibility의 single-cell atlas를 생성했고, nearly continuous differentiation trajectory를 따라 key TF에 의한 gene-regulation wave를 관찰.
- **통계 유의성 / 재현성**: `미제공:` p-value, CI, effect size, multiple testing correction은 abstract에 없음.

#### Dataset 2 — Glial lineage program

- **Dataset**: same human cortex atlas.
- **목적**: neuronal lineage 중심 trajectory 외에 glial lineage의 expression program을 분리.
- **주요 결과**: distinct expression program in the glial lineage를 보고 (`sources/abstract.txt`).
- **해석:** glial lineage program은 cortex development atlas의 coverage를 넓히는 결과지만, 정확한 subtype definition과 marker set은 PDF/Figure 확인 전까지 확정할 수 없다.

#### Dataset 3 — Regulatory element linkage and TF dynamics

- **Dataset**: regulatory elements linked to gene expression in differentiating cells.
- **목적**: lineage-determining TF와 regulatory element activity가 differentiation 중 어떻게 연결되는지 평가.
- **주요 결과**: lineage-determining TF는 linked regulatory elements와 expression levels 사이의 strong correlation을 보였고, early differentiating cells에서 active chromatin state로 transition한다고 보고.
- **주의점**: `미제공:` correlation metric, threshold, FDR, genomic distance window, validation assay.

#### Dataset 4 — ASD noncoding mutation scoring

- **Dataset**: ASD individuals의 noncoding mutations (`sources/abstract.txt`).
- **목적**: cell-type-specific regulatory disruption과 TF binding site disruption 후보 식별.
- **주요 결과**: ASD noncoding mutations가 특정 cell type에서 enrichment되고, frequently disrupted TF binding sites가 식별됨.
- **주의점**: `미제공:` ASD cohort size, mutation count, control set definition, enrichment test, multiple-testing correction.

### 전체 결과 요약

- 반복 패턴은 chromatin accessibility와 expression을 같은 developmental trajectory 위에 놓을 때 lineage commitment에 앞선 regulatory state 변화가 보인다는 점.
- 가장 중요한 claim은 ASD noncoding variation을 developing cortex의 cell-type-specific regulatory map으로 해석할 수 있다는 것이다.
- `해석:` strong association과 predictive disruption score가 중심이며, direct perturbation validation 여부는 PDF 확인 전까지 단정하면 안 된다.

## Figures

### Figure 1

#### 패널별 설명

- `검토필요:` 원문 PDF가 없어 panel 구성을 확인하지 못했다.

#### 본문에서 강조한 비교

- abstract 기준으로는 multi-modal cortex atlas와 continuous differentiation trajectory가 초기 핵심 Figure일 가능성이 높다.

#### 해석 시 주의점

- `추정:` Figure 1이 atlas overview라면 cell type embedding, modality coverage, developmental ordering을 보여줄 가능성이 있다. PDF 확인 전에는 panel label과 수치를 인용하지 않는다.

### Figure 2-N

#### 패널별 설명

- `검토필요:` TF regulatory wave, glial lineage, ASD variant enrichment, sequence model disruption 결과가 본문 Figure들에 분산되어 있을 가능성이 높지만, 원문 PDF 부재로 번호와 panel별 수치를 확인하지 못했다.

#### 본문에서 강조한 비교

- abstract에서 확인되는 비교 축은 lineage-determining TF vs linked regulatory elements, early differentiating cells의 chromatin state transition, ASD mutation enrichment by cell type이다.

#### 해석 시 주의점

- Figure 기반 수치, p-value, cell type label은 PDF 확보 후만 인용한다.

## Tables

본문에 정식 Table 존재 여부는 현재 확인 불가. `미제공:` local PDF와 supplementary table이 없으므로 Table 분석은 PDF manual drop 후 보강 필요.

## Supplementary Information

- `sources/`에는 현재 abstract, ScienceDirect excerpt, GEO accession URL, GitHub code URL, publisher/fulltext/PDF URL stub, BibTeX가 있다.
- `미제공:` Cell supplementary PDF/xlsx는 로컬에 없다.
- `검토필요:` Supplementary Methods에서 sample metadata, QC filters, peak calling, peak-gene linkage, ASD cohort, neural network settings를 우선 확인해야 한다.

## 분석 자체에 대한 메모

- 이 파일은 full workflow 산출물 형식으로 작성했지만, 원문 PDF 미확보로 `source-limited full analysis`다. 추후 `sources/trevino-2021-cortex.pdf`가 들어오면 `Methods`, `Results`, `Figures`, `Tables`를 원문 기준으로 재작성해야 한다.
- 로컬 fetch 실패 원인: 외부 DNS 제한. 공개 PDF mirror URL은 `sources/public_pdf_mirror.url`에 남겼다.
