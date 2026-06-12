# Ma 2020 — SHARE-seq / Chromatin Potential — Core Analysis

## Executive Summary

- **무엇**: SHARE-seq로 같은 single cell에서 RNA expression과 chromatin accessibility를 동시에 측정하고, hair follicle differentiation에서 chromatin accessibility가 RNA induction보다 먼저 변한다는 `chromatin potential` 개념을 제시한 Cell 2020 resource paper.
- **모델 / 방법**: fixed/permeabilized cell에서 Tn5 tagging과 poly(T)-UMI RT를 수행한 뒤 3-round split-pool barcoding으로 ATAC fragment와 cDNA를 같은 cell barcode에 묶고, DORC score와 RNA state의 kNN matching으로 현재 chromatin state가 가리키는 미래 RNA state를 추정.
- **핵심 결과**:
  - ① 전체 SHARE-seq profiling — 84,426 cells across 4 cell lines and 3 tissues; mouse skin 분석은 34,774 high-quality paired profiles.
  - ② species-mixing QC — 903 human + 1,341 mouse cells, doublet 1개, collision rate 0.04%로 reported.
  - ③ adult mouse skin cis-regulation — 63,110 peak-gene associations를 도출하고 DORC가 lineage-determining genes/super-enhancer와 연결됨.
  - ④ computational pairing benchmark — separate ATAC/RNA computational pairing은 같은 cluster assignment 기준 skin 74.9%, brain 36.7%로 tissue별 편차가 큼.
  - ⑤ chromatin potential — TAC에서 IRS/hair shaft 방향으로 흐름을 보이며, RNA velocity보다 early TAC fate dynamics를 더 잘 분리한다고 저자 주장.
- **우리 적용**: `chromatin-rna-coupling` topic의 foundational reference. GSE140203은 MultiVelo/MultiVeloVAE 계열에서 재사용되는 mouse skin paired ATAC/RNA benchmark이므로 `methodology-reference`, `pipeline-applicable`, `academic-citation` 가치가 높음.
- **심층**: 한계·재현 ROI는 `ma-2020-shareseq_lens-academic.md` / `ma-2020-shareseq_lens-industry.md` / `ma-2020-shareseq_methodology-brief.md` 참고.

## Identity

- **Title**: Chromatin Potential Identified by Shared Single-Cell Profiling of RNA and Chromatin
- **Authors**: Sai Ma, Bing Zhang, Lindsay M. LaFave, Andrew S. Earl, Zachary Chiang, Yan Hu, Jiarui Ding, Alison Brack, Vinay K. Kartha, Tristan Tay, Travis Law, Caleb Lareau, Ya-Chieh Hsu, Aviv Regev, Jason D. Buenrostro
- **Year / Venue**: 2020, Cell 183(4):1103-1116.e20
- **DOI**: 10.1016/j.cell.2020.09.056
- **Citation key**: `@ma2020shareseq`
- **Primary source used**: `sources/pmc_fulltext.url`, `sources/publisher_fulltext.url`, `sources/abstract.txt`. `sources/ma-2020-shareseq.pdf`는 local shell DNS/network 제한으로 미다운로드.

## Background

### 배경 스토리

- 문제의 출발점: cell differentiation은 gene expression 변화만으로 끝나지 않고 chromatin accessibility, TF binding, enhancer activation 같은 regulatory layer를 거친다. 저자는 asynchronous differentiation 때문에 cross-sectional sample에서 regulatory event의 시간 순서를 직접 보기 어렵다는 점을 출발점으로 둔다.
- 선행 접근 A: scRNA-seq는 cell state와 differentiation trajectory를 높은 throughput으로 복원할 수 있지만, 같은 cell에서 regulatory chromatin state를 보지 못한다.
- A의 한계: RNA가 이미 변한 뒤의 상태를 읽기 쉽다. enhancer가 먼저 열리고 promoter activation이나 nascent RNA가 뒤따르는지, 같은 cell 기준으로 직접 연결하기 어렵다.
- 선행 접근 B: scATAC-seq와 bulk/low-throughput chromatin profiling은 regulatory element와 motif activity를 잡아낼 수 있다.
- B의 한계: scATAC와 scRNA를 별도 cell에서 측정하면 computational pairing이 필요하다. 이 논문에서 같은 SHARE-seq data를 일부러 modality별로 분리해 pairing을 시험했을 때, 같은 cluster assignment 기준 정확도는 skin 74.9%, mouse brain 36.7%로 tissue와 depth에 민감했다.
- 이 논문으로 이어지는 gap: 같은 cell에서 RNA와 chromatin을 동시에 측정하고, 그 paired variation으로 peak-gene association, DORC, chromatin potential을 계산해야 chromatin priming의 temporal order를 직접 평가할 수 있다는 논리다.

### 기본 개념

- `SHARE-seq`: simultaneous high-throughput ATAC and RNA expression with sequencing. Tn5로 open chromatin을 표시하고, poly(T)-UMI primer로 mRNA를 reverse transcription한 뒤, split-pool hybridization barcoding으로 ATAC fragment와 cDNA를 같은 cell barcode에 연결한다.
- `DORC`: domains of regulatory chromatin. 특정 gene 주변에서 유의하게 연결된 peak가 많이 모인 regulatory chromatin domain이다. 논문은 adult mouse skin에서 DORC를 lineage-determining genes와 super-enhancer annotation에 연결한다.
- `chromatin potential`: 현재 cell의 chromatin state가 어떤 future RNA state와 가장 잘 맞는지를 kNN 방식으로 찾고, 현재 위치에서 그 future RNA-state neighbor 방향으로 vector를 그리는 metric이다.
- `residual`: DORC accessibility와 matched RNA expression의 차이로, chromatin이 RNA보다 먼저 활성화되는 구간을 정량화하는 데 사용된다.

### 이 논문의 필요성

- 핵심 이유: chromatin과 RNA가 "비슷한 cell type map"을 만들더라도, lineage commitment 직전에는 두 modality가 어긋날 수 있다. 이 어긋남이 바로 chromatin priming 신호다.
- 기존 방법으로 부족했던 지점: separate-modality integration은 paired truth가 없어서 asynchrony를 error로 처리하거나 놓칠 수 있다.
- 이 논문이 해결하려는 방향: paired single-cell multi-omics assay를 크게 확장하고, paired covariance를 이용해 enhancer-gene linkage와 fate-priming vector를 계산한다.

## Methods

### SHARE-seq experimental protocol

- Formal task: 같은 single cell에서 chromatin accessibility fragment와 gene expression UMI를 동시에 회수해 cell-level paired matrix를 만든다.
- 입력: fixed/permeabilized cells or nuclei, Tn5 transposase, poly(T) RT primer with UMI/biotin, 96-well split-pool barcoded oligos.
- 출력: cell-by-peak ATAC count matrix와 cell-by-gene RNA count matrix, 공통 barcode로 연결된 paired profiles.
- 핵심 절차: (1) Tn5 transposition, (2) poly(T)-UMI RT, (3) 96-well plate hybridization, (4) 3회 반복 barcoding으로 약 $96^3 \approx 10^6$ barcode space 생성, (5) reverse crosslinking, (6) streptavidin bead로 cDNA를 chromatin library에서 분리, (7) shared barcode로 paired profiles 식별.
- 기술적 장점: 모든 반응을 bulk-like scale에서 처리하므로 library prep cost가 낮다. 저자는 100,000 cells 기준 SHARE-seq library prep cost를 약 $433로 제시하고, sci-CAR는 같은 규모에서 $30,000 초과로 비교했다.
- 검토필요: 본 분석에서는 supplementary protocol PDF를 로컬로 확인하지 못했다. 세부 oligo sequence, buffer, exact incubation time은 supplemental table/method PDF 재확인 필요.

### cis peak-gene association and DORC

- Formal task: paired cell variation을 이용해 chromatin peak와 nearby gene expression의 cis association을 추정한다.
- 입력: cell-by-peak accessibility, cell-by-gene expression, gene TSS 기준 genomic window.
- 출력: significant peak-gene associations, gene별 DORC peak set, cell별 DORC score.
- 통계 구조: peak accessibility와 gene expression의 co-variation을 평가하되 chromatin measurement technical bias를 보정한다. 본문은 GM12878에서 13,277 significant peak-gene associations를 보고했고, adult mouse skin에서는 63,110 peak-gene associations를 제시했다.
- DORC 정의: gene을 significantly associated peak 수로 rank하고, skin data에서는 TSS ±50 kb 기준 peak 10개 이상, GM12878에서는 peak 5개 이상을 cutoff로 사용했다. 이후 association window를 TSS ±500 kb로 확장해 DORC score를 계산했다.
- DORC score: 각 cell에서 해당 gene에 유의하게 연결된 peak count를 fragment depth normalization 후 합산한 값이다.
- Method 관점의 한계: peak-gene association은 correlation 기반이다. chromatin accessibility가 target gene expression을 유도한다는 causal evidence가 되려면 perturbation이나 lineage tracing이 추가로 필요하다.

### Chromatin potential

- Formal task: 현재 cell의 chromatin state가 가장 잘 예측하는 future RNA state를 찾아 cell fate direction을 vector로 표현한다.
- 입력: DORC-regulated gene set의 chromatin/DORC score와 RNA expression, chromatin low-dimensional embedding.
- 출력: 각 cell의 chromatin potential arrow, arrow length, inferred root/transition direction.
- 알고리즘: 각 cell $x$의 chromatin neighborhood에 대해 RNA expression이 현재 chromatin state와 가장 correlation 높은 cell $y$를 kNN으로 찾는다. 논문은 $k = 10$ RNA-chromatin neighbors를 사용했다. chromatin potential arrow는 chromatin low-dimensional space에서 cell $x$와 matched RNA-neighbor cells의 방향/거리로 표현된다.
- 핵심 insight: RNA velocity는 spliced/unspliced RNA 차이를 이용해 비교적 가까운 transcriptional future를 예측한다. chromatin potential은 enhancer/DORC accessibility가 RNA induction보다 먼저 변한다는 가정에 기대어 더 이른 lineage bias를 잡으려 한다.
- 중요한 hidden assumption: 현재 dataset 안에 "미래 RNA state"에 해당하는 cell들이 관측되어 있어야 한다. 즉, trajectory 전체가 충분히 sampled되어야 하며, missing intermediate state가 많으면 nearest-neighbor future가 왜곡될 수 있다.
- 검토필요: arrow length와 prediction timescale의 절대 시간 단위는 본문에서 정의되지 않는다. pseudotime/embedding 거리 기반의 상대량으로 해석해야 한다.

## Results

### Dataset별 결과

#### Dataset 1 — human/mouse cell-line mixture QC

- Dataset: GM12878 human cells와 NIH/3T3 mouse cells mixture.
- 목적: barcode collision, species specificity, paired assay purity 검증.
- 사용한 데이터 규모: 2,000 expected cells 기준, filter 통과 cell은 903 human + 1,341 mouse.
- 주요 수치: doublet 1개, collision rate 0.04%; expected collision rate 0.052%. filter 통과 cell 평균 2,545 RNA UMIs, estimated RNA UMI library size 9,660; 평균 8,252 unique ATAC fragments, estimated ATAC library size 19,723, fragments in peaks 65.5%.
- 논문 주장과의 연결: split-pool barcode space가 충분히 커서 modality pairing이 낮은 collision으로 가능하다는 QC 근거.
- 통계/재현성: replicate 및 추가 cell line에서 similar performance라고 보고. p-value/CI는 이 QC 수치에는 미제공.

#### Dataset 2 — mouse lung, brain, skin tissue profiling

- Dataset: mouse lung, brain, skin; Introduction에서는 4 cell lines와 3 tissue types 합산 84,426 cells로 보고.
- 목적: SHARE-seq가 primary tissue와 nuclei/cell input에서 동작하는지 확인.
- 주요 결과: mouse skin, brain, lung에서 ATAC/RNA modality가 major cell type을 회수. nuclei input에서는 intronic RNA 비율 증가가 관찰됨.
- 비용 결과: 100,000 cells library prep cost 약 $433로 제시. sci-CAR는 같은 규모에서 $30,000 초과로 비교.
- 논문 주장과의 연결: assay의 scale과 cost advantage를 뒷받침한다.
- 주의점: cost는 저자 hands-on condition 기준이다. reagent price, sequencing cost, labor, failure rate는 별도 일반화가 어렵다.

#### Dataset 3 — adult mouse skin paired atlas

- Dataset: adult mouse skin SHARE-seq, 34,774 high-quality paired profiles; GEO GSE140203.
- 목적: chromatin/RNA cell state congruence와 불일치, lineage trajectory, chromatin priming 검증.
- 주요 결과: RNA clustering으로 정의한 cell subset이 ATAC UMAP에서도 대체로 분리됨. TAC, IRS, ORS, hair shaft 같은 major cell type이 양쪽 modality에서 회수됐다.
- 예외: granular layer는 RNA에서 더 잘 분리되고, proliferating basal cells는 RNA에서 cell cycle gene expression으로 coherent group을 만들지만 chromatin accessibility에서는 4가지 dimensionality reduction 접근 중 coherent cluster로 나오지 않았다.
- computational pairing benchmark: paired truth를 숨기고 CCA-based ATAC/RNA pairing을 돌리면 same-cluster assignment 기준 skin 74.9%, brain 36.7%. down-sampling에서 low depth/low cell number일수록 error가 커진다고 보고.
- 논문 주장과의 연결: paired measurement는 단순 편의가 아니라 modality asynchrony를 보존하는 데 필요하다는 근거다.

#### Dataset 4 — peak-gene association and DORC

- Dataset: GM12878 23,278 cells, adult mouse skin.
- 목적: chromatin accessibility peak와 target gene expression의 cis association을 paired single-cell covariance로 찾기.
- 주요 수치: GM12878에서 13,277 significant peak-gene associations; p < 0.05, FDR = 0.11. promoter-proximal bias 보정을 언급하며, ATAC peaks의 61.3%가 TSS 2 kb 이내에 있었다고 보고. adult mouse skin에서는 63,110 peak-gene associations.
- DORC 결과: DORC-regulated genes는 lineage-determining genes에 enriched되고 known super-enhancer와 overlap한다고 제시.
- 통계/재현성: peak-gene association에는 FDR가 제시되어 있으나, DORC-super-enhancer overlap의 exact p-value/effect size는 본 분석에서 확인한 공개 crawl text에 수치가 없음.

#### Dataset 5 — hair follicle differentiation and chromatin potential

- Dataset: adult mouse skin hair follicle differentiation trajectories, 특히 TAC에서 IRS/medulla/cuticle-cortex로 이어지는 lineage.
- 목적: DORC accessibility가 target RNA expression보다 먼저 나타나는지 검증하고, chromatin potential로 fate direction을 추론.
- 주요 결과: cuticle/cortex trajectory에서 DORC accessibility가 associated gene expression보다 먼저 상승하는 패턴. Wnt3에서는 DORC accessibility가 TAC 단계에서 먼저 활성화되고, promoter activation, intron signal, exon expression 순서로 이어지는 것으로 제시.
- 주요 수치: DORC-regulated genes/lineages 대부분에서 residual이 positive였고, 본문은 92%라고 보고. RNA velocity 대비 chromatin potential의 prediction reach는 early stage에서 더 길고 late pseudotime에서는 RNA velocity가 더 길었다고 하며, KS test p < 2.2 × 10^{-16}을 제시.
- 논문 주장과의 연결: chromatin accessibility가 lineage choice 이전의 priming state를 반영한다는 중심 claim을 뒷받침한다.
- 주의점: chromatin potential은 lineage tracing이 아니라 paired snapshot의 nearest-neighbor inference다. 저자도 primed chromatin state는 lineage choice가 아니라 lineage bias일 수 있다고 Discussion에서 구분한다.

### 전체 결과 요약

- 반복적으로 관찰된 패턴: RNA와 chromatin은 major cell type 수준에서는 congruent하지만, cell cycle과 differentiation branchpoint에서는 다른 temporal layer를 반영한다.
- 가장 중요한 수치: 34,774 adult mouse skin paired profiles, 63,110 skin peak-gene associations, 92% positive residual pattern, computational pairing accuracy skin 74.9% vs brain 36.7%.
- baseline 대비 차이: SHARE-seq는 separate scATAC/scRNA computational pairing보다 paired truth를 보존하고, RNA velocity보다 early chromatin priming을 잡는다고 저자 주장.
- 결과 해석 시 주의점: 대부분은 observational association이다. causal regulatory chain은 TF perturbation, enhancer perturbation, lineage tracing 없이 확정되지 않는다.

## Figures

### Figure 1 — SHARE-seq assay validation

#### 패널별 설명

- a: SHARE-seq workflow. Tn5 transposition, RT, split-pool barcoding, cDNA/chromatin separation, sequencing으로 이어지는 assay schematic.
- b-c: human/mouse cell-line mixture에서 ATAC fragments와 RNA UMIs가 species별로 분리되는지 보여준다.
- d: human genome mapping fraction을 이용한 species purity/doublet check.
- e: SHARE-seq와 sci-CAR, SNARE-seq, Paired-seq의 ATAC fragment/RNA UMI yield 비교.
- f: GM12878 NFkB1 locus에서 aggregate/single-cell accessibility와 expression profile을 보여준다.

#### 본문에서 강조한 비교

- 비교 대상: SHARE-seq internal QC vs 기존 paired multi-omic methods.
- 관찰된 차이: 낮은 collision rate와 paired assay sensitivity를 강조한다.
- 이 차이가 의미하는 것: 이후 DORC와 chromatin potential 분석이 assay artifact만으로 설명되지 않는다는 기본 QC 근거.

#### 해석 시 주의점

- cost/yield 비교는 platform, sequencing depth, filtering 기준에 따라 달라질 수 있다. 원문 Table S1/Supplementary protocol을 확인하면 더 정확해진다.

### Figure 2 — tissue-scale paired profiling

#### 패널별 설명

- a: profiled tissues schematic, mouse skin cellular diversity를 강조.
- b-c: SHARE-seq와 다른 single-cell/nucleus ATAC/RNA approaches의 library size estimates 비교.
- d-e: adult mouse skin cells를 RNA-defined UMAP와 ATAC-defined UMAP에서 각각 표시. RNA cluster label이 ATAC space에서도 major cell type을 대체로 분리함을 보여준다.
- f 이후: RNA cluster와 ATAC cluster congruence, granular layer/cell-cycle basal cells/TAC 같은 예외 패턴을 제시.

#### 본문에서 강조한 비교

- 비교 대상: same-cell RNA state와 chromatin state.
- 관찰된 차이: major cell type은 일치하지만 cell cycle basal cells처럼 RNA에서는 강하고 ATAC에서는 coherent cluster가 약한 상태가 있다.
- 이 차이가 의미하는 것: paired multi-omics는 modality congruence만 확인하는 도구가 아니라, modality mismatch를 biological signal로 읽는 도구다.

#### 해석 시 주의점

- cell type assignment는 marker genes, TF motifs, accessibility peaks를 조합했다. marker ambiguity나 clustering parameter sensitivity는 본 분석에서 정밀 검증하지 못했다.

### Figure 3 — cis regulation and DORCs

#### 패널별 설명

- a: distal regulatory element와 gene expression association을 찾는 analytical framework schematic.
- b: GM12878에서 cell 수/read depth down-sampling 후 peak-gene association 수 변화를 보여준다.
- c: Dlx3 주변 ±500 kb에서 peak accessibility와 Dlx3 RNA expression association p-value를 loop로 표시하고, ChIP-seq/super-enhancer annotation과 비교한다.
- d-e: all genes와 known super-enhancer genes에서 significant peak-gene association 수를 비교한다.
- f-g: lineage-priming genes, ChIP-seq signal enrichment, residual high/low DORC group을 비교한다.
- h-j: chromatin potential workflow와 hair follicle stage projection으로 이어지는 bridge panel 역할.

#### 본문에서 강조한 비교

- 비교 대상: random/proximal peak-gene relationship이 아니라 DORC-dense lineage genes.
- 관찰된 차이: DORC는 super-enhancer/lineage genes와 연결되고, down-sampling은 association power를 줄인다.
- 이 차이가 의미하는 것: paired single-cell scale이 enhancer-gene inference의 핵심 조건이라는 주장.

#### 해석 시 주의점

- peak-gene association은 co-variation 기반이다. enhancer-gene physical contact나 perturbation validation은 별도 증거가 필요하다.

### Figure 4 — lineage priming

#### 패널별 설명

- a: scATAC UMAP coordinates 위에 IRS, medulla, cuticle/cortex fate decisions의 pseudotime을 표시.
- b-d: Wnt3 DORC score와 Wnt3 gene expression residual/relationship. DORC accessibility가 RNA보다 먼저 상승하는 사례.
- e: Wnt3 locus에서 individual peaks, promoter, intron/exon expression이 pseudotime에 따라 순차적으로 활성화되는 패턴.
- f-g: cuticle/cortex lineage에서 DORC accessibility, expression, residual dynamics를 cluster/module 수준으로 정리.
- h-i: lineage-priming DORCs의 TF motif enrichment와 TF expression timing; Lef1/Hoxc13 motif/gene expression이 Wnt3 DORC activation 이전에 나타나는 모델.
- j-l: TF-DORC regulatory network와 stepwise activation schematic.

#### 본문에서 강조한 비교

- 비교 대상: DORC accessibility onset vs nascent/mature RNA expression onset.
- 관찰된 차이: enhancer accessibility가 promoter/nascent/mature RNA signal보다 앞서는 사례가 반복됨.
- 이 차이가 의미하는 것: chromatin accessibility가 cell fate commitment 이전 lineage priming marker로 작동할 수 있다는 중심 근거.

#### 해석 시 주의점

- pseudotime ordering과 residual은 temporal inference다. 실제 wall-clock time이나 irreversible commitment를 직접 측정한 것은 아니다.

### Figure 5 — chromatin potential

#### 패널별 설명

- a-d: Notch1/Tchh 등 lineage-primed chromatin state를 scRNA UMAP, scATAC region profile, progenitor/differentiated aggregate track에서 보여준다.
- e-g: ChIP-seq histone modification state와 residual high/low DORC genes를 비교해 primed chromatin state의 epigenetic support를 제시.
- h: chromatin potential workflow와 scATAC UMAP arrows. 현재 chromatin state가 연결되는 future RNA state 방향을 vector로 표현한다.
- i: TAC heterogeneity model. TAC-1/TAC-2 root-like positions와 downstream IRS/hair shaft branch 구조를 설명한다.
- j-k: different hair follicle stages projection, Anagen III/VI distribution을 통해 inferred root/branch와 biological stage를 맞춘다.
- l 이후: RNA velocity와 chromatin potential의 방향성/거리 차이를 비교한다.

#### 본문에서 강조한 비교

- 비교 대상: chromatin potential vs RNA velocity.
- 관찰된 차이: chromatin potential은 TAC branchpoint에서 더 긴/분리된 arrows를 보이고, RNA velocity는 late pseudotime에서 더 멀리 예측하는 경향으로 제시된다.
- 이 차이가 의미하는 것: chromatin state는 RNA velocity보다 이른 fate bias를 포착할 수 있다는 주장.

#### 해석 시 주의점

- 저자는 long arrows 일부가 assay noise, low-dimensional embedding error, technical bias 때문일 수 있다고 명시한다. 따라서 arrow 자체를 fate commitment로 읽으면 안 된다.

## Tables

본문에 정식 Table은 확인되지 않았다. Supplementary Table은 protocol/barcode design, cluster annotation, peak-gene association 등 핵심 보조 정보를 포함하는 것으로 원문에서 언급되지만, supplementary binary를 로컬에서 열람하지 못했다.

- 미제공: Table S1의 exact oligo/barcode design과 cost detail.
- 미제공: Table S2의 full RNA cluster annotation.
- 미제공: Table S3의 full GM12878 peak-gene association list.
- 검토필요: supplementary PDFs/XLSX를 확보하면 DORC cutoff, peak-gene list, cell type annotation을 재검증해야 한다.

## Supplementary Information

- `sources/ma-2020-shareseq.pdf`: 미다운로드. local shell DNS/network 제한.
- `sources/pmc_fulltext.url`: PMC fulltext URL. 본 core 분석의 주 근거.
- `sources/public_pdf_mirror.url`: NSF PAR public PDF mirror URL. local shell에서는 DNS 제한으로 접근 실패.
- `sources/data_GSE140203.url`: GEO data accession.
- `sources/code_SHARE-seq.url`, `sources/code_SHARE-seq-v1.url`, `sources/code_SHARE-seq-broad.url`: alignment/pipeline code URLs.
- 미제공: supplementary file local copies. Figure S1-S5와 supplementary tables는 원문 crawl에서 일부 caption/언급만 확인했다.

## 분석 자체에 대한 메모

- PDF binary와 supplementary를 확보하면 우선순위는 (1) Table S1/S2/S3 확인, (2) chromatin potential STAR Methods의 exact formula/normalization 재확인, (3) Figure S5의 RNA velocity 비교 수치 정밀 추출이다.
- 해석: 이 논문은 MultiVelo 이전 단계의 "chromatin leads RNA" 직관을 paired data에서 보여준 foundational resource다. 그러나 dynamic model은 ODE/generative likelihood가 아니라 nearest-neighbor future matching이므로, 후속 velocity model과 같은 수준의 kinetic parameter inference로 읽으면 안 된다.
