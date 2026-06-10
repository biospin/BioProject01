# kang-2024-kaist-tumor-normal — Core Analysis

## Executive Summary

- **무엇**: 30 암종 1,070 종양 + 493 정상 샘플에서 4.9M 세포 pan-cancer tumor-normal single-cell atlas를 구축하고, NMF 기반 cell state 분해를 통해 hallmark gene signature, 염증성 fibroblast 아형, TLS 구성 cell state를 체계적으로 특성화한 자원 논문
- **모델 / 방법**: AND-gating 알고리즘으로 cell type별 hallmark signature 추출 → NMF ($K=5$~$9$, 총 35 modules/individual) 기반 cell state 정의 → Ro/e(ratio of observed/expected) 통계로 조직 편향 정량화 → 137개 spatial transcriptomics dataset deconvolution으로 TLS signature 공간 검증
- **핵심 결과**:
  - ① Pan-cancer 4.9M 세포 (104 datasets, 999 donors) — 종양-정상 비교 가능한 단일 unified atlas 구축
  - ② AKR1C1⁺ vs WNT5A⁺ 염증성 fibroblast 두 아형: 기관 분포·세포 상호작용·공간 패턴에서 뚜렷이 구분
  - ③ 인터페론 풍부 community state (TLS 성분 포함) — tumor/adjacent normal/healthy normal 간 rewiring 확인
  - ④ TLS signature가 면역치료 반응을 유의하게 예측 (OR ≈ 1.3, $p = 1.4 \times 10^{-3}$, $n = 1261$ 환자 meta-analysis)
  - ⑤ RCC 공간 전사체에서 TLS-enriched vs non-enriched cell type 구분 — Treg, LAMP3⁺ DC, CCL19⁺ fibroblast가 TLS 내 풍부
- **우리 적용**: ADC target validation 시 정상조직 발현 baseline으로 직접 참조 가능 (pipeline-applicable). Zenodo 공개 data + web portal (cellatlas.kaist.ac.kr/ecosystem/)로 즉시 접근
- **심층**: 한계·재현 ROI → `kang-2024-kaist-tumor-normal_lens-academic.md` / `kang-2024-kaist-tumor-normal_lens-industry.md` / `kang-2024-kaist-tumor-normal_methodology-brief.md`

---

## Identity

- **Title**: Systematic dissection of tumor-normal single-cell ecosystems across a thousand tumors of 30 cancer types
- **Authors**: Kang, J.†, Lee, J.H.†, Cha, H., An, J., Kwon, J., Lee, S., Kim, S., Baykan, M.Y., Kim, S.Y., An, D., Kwon, A.Y., An, H.J., Lee, S.H., Choi, J.K., Park, J.E. (†co-first)
- **Year**: 2024
- **Venue**: Nature Communications 15, 4067
- **DOI**: 10.1038/s41467-024-48310-4
- **Published**: 2024-05-14 (Erratum: 2025-03-21)
- **Affiliations**: KAIST Graduate School of Medical Science and Engineering; KAIST Department of Bio and Brain Engineering; Samsung Medical Center (SMC); CHA Bundang Medical Center; National Cancer Center (NCC)
- **Citation key**: `@kang2024tumornormal`
- **PMID**: 38744958
- **Data/Code**: Zenodo DOI:10.5281/zenodo.10651059; web portal https://cellatlas.kaist.ac.kr/ecosystem/; LC cohort scRNA-seq EGA EGAD00000000469; LC cohort bulk RNA-seq GEO GSE218989

---

## Background

#### 배경 스토리

- **문제의 출발점**: 종양은 malignant cell과 tissue-infiltrating stromal·immune cell로 구성된 매우 이질적인 조직이며, single-cell RNA-seq (scRNA-seq)이 TME 내 세포 이질성의 고해상도 분석을 가능하게 했다. 그러나 기존 pan-cancer atlas 대부분은 종양 샘플만 분석하거나 T cell, myeloid cell 등 특정 세포 계통에 집중했다. 종양과 짝을 이루는 정상 조직과의 비교가 제한적이어서 "종양 특이 현상인가, 정상에도 있는 것인가"를 구분하기 어려웠다.
- **선행 접근 A**: Barkley et al., 2022 (Nat Genet)가 암종 간 공통 cancer cell state를 정의했다. A의 한계: 주로 종양 조직 중심이고, 정상 대조 조직을 체계적으로 포함하지 않았으며 30 암종 규모의 통합 tumor-normal 비교는 없었다.
- **선행 접근 B**: Cheng et al., 2021과 Zheng et al., 2021 등은 pan-cancer myeloid cell 또는 T cell atlas를 구축했다. B의 한계: 단일 세포 계통에만 집중하여 여러 세포 유형의 상호작용·co-occurrence 패턴을 통합 분석하기 어려웠다.
- **이 논문으로 이어지는 gap**: ① tumor, adjacent normal, healthy normal 3가지 조직 유형을 동시에 포함하는 대규모 atlas 부재; ② TME 내 상호작용 생태계(ecosystem) 전체를 조망하는 multi-cell-type co-occurrence 분석 부재; ③ TLS(tertiary lymphoid structure)를 구성하는 cell state들과 그 공간적 배치를 cross-cancer 수준으로 검증한 연구 부재.

#### 기본 개념

- **NMF (non-negative matrix factorization)**: 유전자 발현 행렬을 양수 행렬 두 개의 곱으로 분해해 각 세포가 어떤 발현 프로그램(module)의 혼합인지 추출하는 비지도 방법. 이 논문에서는 세포 유형별·샘플별로 $K=5$~$9$ NMF를 돌려 개인당 35 module을 생성, 이를 clustering해 pan-cancer cell state를 정의한다.
- **AND-gating 알고리즘**: 복수 장기·암종에서 공통적으로 upregulated된 gene을 cell type별로 추출하는 방법. 특정 암종에만 존재하는 편향된 signature를 제거하고 보편적 hallmark gene을 추출하기 위해 사용. 두 조건: (i) 해당 cell type에서 다른 cell type 대비 upregulated ($\log_2$ fold-change > 0), (ii) 종양 조직에서 정상 조직 대비 highly expressed ($\log_2$ fold-change > 0.5, adjusted $p < 0.05$).
- **Ro/e (ratio of observed to expected)**: $\log_2(\text{observed}/\text{expected})$ 형태. 특정 cell state가 특정 조직 유형(normal/adjacent normal/tumor)에서 통계적으로 풍부한지/희귀한지를 카이제곱 분석 기반으로 정량화. Ro/e > 0이면 해당 조직에 풍부, < 0이면 희귀.
- **TLS (tertiary lymphoid structure)**: 종양 조직 내에서 형성되는 lymphoid-like 구조로, LAMP3⁺ DC, Treg, Tfh, CCL19⁺ fibroblast 등을 포함. 면역치료 반응의 favorable predictor로 알려져 있으나, 단일 세포 수준에서 non-TLS 조직과의 구분이 명확하지 않았다.
- **ssGSEA (single-sample gene set enrichment analysis)**: 개별 샘플에서 gene set의 활성도를 점수화. 이 논문에서 cell state score를 bulk RNA-seq cohort에 적용해 TCGA 생존 분석과 면역치료 반응 예측에 사용.

#### 이 논문의 필요성

- **핵심 이유**: 정상 조직 baseline을 포함한 대규모 tumor-normal paired atlas가 없어 TME 특이성 판단이 제한적이었다.
- **기존 방법으로 부족했던 지점**: 기존 atlas는 특정 세포 계통 또는 종양 조직만을 다루었고, 공간적 배치와 bulk transcriptomics와의 연계가 체계적이지 않았다.
- **이 논문이 해결하려는 방향**: 30 암종 1,563 샘플 통합 → NMF 기반 세포 상태 정의 → spatial transcriptomics deconvolution → immunotherapy cohort 검증으로 이어지는 포괄적 tumor-normal ecosystem 지도 제공.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: 다양한 기관·암종의 scRNA-seq 데이터를 통합해 종양-정상 조직 간 공통 및 조직 특이 cell state를 정의하고, 이들의 공간적 배치와 임상적 의미를 파악한다.
- **입력**: 104 개 공개 scRNA-seq dataset (10x Chromium 기반, 종양 1,070개 + 정상 493개 샘플) + 137개 spatial transcriptomics dataset + 1,261명 면역치료 bulk RNA-seq cohort + 8,887 TCGA bulk RNA-seq
- **출력**: cell state 정의 (NMF module), hallmark gene signature, Ro/e 기반 조직 편향, co-occurrence network, TLS signature, 면역치료 반응 예측 odds ratio
- **추정 대상**: 각 세포의 cell state 소속(NMF weighted average), 조직 유형별 cell state 풍부도(Ro/e), 면역치료 반응과 cell state 연관성(logistic regression odds ratio)
- **중요한 hidden assumption**: NMF로 정의된 cell state는 생물학적으로 의미 있는 발현 프로그램에 해당하며, 배치 보정(BBKNN) 이후 dataset 간 통합이 충분하다고 가정

#### 확률 / 통계학적 구조

- **Model family**: Unsupervised decomposition (NMF) + 비모수 통계 (Wilcoxon rank sum test) + 로지스틱 회귀 meta-analysis (random effects model)
- **Likelihood / objective**: NMF objective: $\min_{W,H \geq 0} \|X - WH\|_F^2$. AND-gating: two-sided $t$-test, $\log_2$ fold-change threshold.
- **Prior / regularization**: NMF의 non-negativity constraint. 품질 낮은 module (NMF weight < 10~20 또는 > 150~170, cell type별 의존적) 및 ribosomal/mitochondrial-enriched cluster 제거.
- **Latent variable / hidden state**: NMF module (cell state) — 각 세포가 어떤 발현 프로그램을 활성화하는지 나타내는 latent representation
- **Inference / optimization**: sklearn.decomposition.NMF (scikit-learn v1.0.2, $K=5,6,7,8,9$로 35 module 생성) → Leiden clustering으로 module 군집화 → UMAP 시각화
- **Noise, sparsity, uncertainty 처리**: Scrublet으로 doublet 제거; ambient RNA(soup effect) 자동 탐지 알고리즘 적용 (2 장기에서 다수를 차지하는 module을 doublet/soup으로 판정); 희귀 cell type 보존을 위한 Geometric sketching ($n$ 서브샘플링)

#### 핵심 method insight

- **기존 방법의 한계**: PCA/UMAP 기반 clustering은 dataset 수가 많아질수록 batch effect에 취약하고, 특정 세포 계통만 분석하거나 cell state 정의가 study별로 달라 pan-cancer 비교가 어려웠다.
- **이 논문이 바꾼 가정**: 세포 유형별·개인별 NMF를 독립적으로 수행한 후 cross-sample로 통합하면, 각 개인 내 발현 이질성과 pan-cancer 공통 프로그램을 동시에 포착할 수 있다. AND-gating 알고리즘은 특정 암종에 편향된 gene이 아닌, 복수 기관에서 공통적으로 나타나는 hallmark gene만 남긴다.
- **새로 추가한 변수 또는 구조**: (1) tumor/adjacent normal/healthy normal 3-way tissue 분류 및 Ro/e 정량화; (2) ligand-receptor interaction 분석(CellPhoneDB v3)으로 AKR1C1⁺/WNT5A⁺ fibroblast의 세포 상호작용 차이 특성화; (3) cell2location을 이용한 spatial transcriptomics deconvolution으로 TLS cell state 공간 검증
- **이 변화가 중요한 이유**: 단순 clustering이 아닌 NMF 기반 발현 프로그램 분해로, 한 세포가 여러 cell state를 공유(blending)하는 현실을 반영하며, 개인 내 희귀 cell state도 K-parameter scan을 통해 포착 가능

#### 이전 방법과의 차이

- **Baseline**: Barkley et al. 2022 (Nat Genet) — cancer cell state; Cheng et al. 2021 — myeloid atlas; Zheng et al. 2021 — pan-cancer T cell
- **공통점**: scRNA-seq 통합, cell type annotation, UMAP 시각화, marker gene 기반 annotation
- **차이점**: ① 정상 조직(adjacent normal + healthy normal)을 종양과 동시에 포함; ② 세포 유형별 개인별 NMF를 통해 발현 프로그램을 모듈화; ③ AND-gating으로 보편적 hallmark gene 추출; ④ 137개 spatial transcriptome dataset deconvolution으로 공간 검증; ⑤ 1,261명 면역치료 cohort 통합으로 임상 예측력 검증
- **차이가 크게 나타나는 조건**: 여러 암종에 걸쳐 공통 cell state를 정의해야 할 때, 또는 정상 조직 대비 종양 특이 세포 상태를 구분해야 할 때

#### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: 104 scRNA-seq datasets (30 cancer types), 137 spatial transcriptome datasets (11 cancer types), 1,261 면역치료 cohort (4 cancer types)
- **Metric**: Ro/e (조직 편향), Pearson correlation (cell state score 일치도), odds ratio + 95% CI (면역치료 반응 예측), Wilcoxon rank sum test p-value (TLS 점수 비교)
- **개선된 결과**: TLS signature가 RCC spatial transcriptomics에서 TLS vs non-TLS 구분 ($p = 1.5 \times 10^{-5}$, $n=17$ samples), 면역치료 반응 예측 OR ≈ 1.3 ($p = 1.4 \times 10^{-3}$)
- **Ablation 근거**: 미제공 (ablation study 형태의 실험 설계는 없고, Ro/e threshold 기반 Ro/e filtering 방법으로 희귀 cell state를 장기 특이 분석에서 제외)
- **정성적 효과**: AKR1C1⁺ fibroblast — cancer cell/CTSK⁺ macrophage와 proximity; WNT5A⁺ fibroblast — exhausted CD8⁺ T cell/Treg과 proximity, 면역억제 TME 형성에 차별적 역할

#### Method 관점의 한계

- **약한 assumption**: NMF의 $K$ 선택이 자동화되지 않고 $K=5$~$9$ 범위 고정. 세포 유형·조직별 $K$가 실제로 다를 수 있음.
- **구현 또는 학습상의 부담**: 4.9M 세포 통합을 위해 Geometric sketching으로 서브샘플링 → 희귀 cell state가 일부 누락될 가능성.
- **일반화가 불확실한 조건**: 10x Chromium 이외 기술(Smart-seq2 등) 제외 조건; 유체 샘플(ascites, CSF, PBMC), 세포주, 마우스 실험은 제외. FFPE 샘플 비율 및 sample 보존 품질 편차가 통합에 영향.

---

## Results

#### Dataset별 결과

##### Dataset 1 — Pan-cancer tumor-normal single-cell meta-atlas 구축
- **Dataset**: 104 개 공개 scRNA-seq 데이터셋 (PubMed, Google Scholar, GEO, Single Cell Portal, COVID-19 Cell Atlas, Curated Cancer Cell Atlas에서 수집)
- **목적**: 종양-정상 생태계의 포괄적 단일 세포 지도 구축
- **사용한 데이터 규모**: 4,901,584 세포; 1,070 종양 + 493 정상 샘플; 999명; 30 암종; breast cancer(BRCA)가 가장 많고 그 뒤 lung cancer(LC), head and neck(HNSC), hepatocellular carcinoma(HCC) 순
- **Baseline / 비교 대상**: 기존 pan-cancer atlas (Barkley 2022, Cheng 2021 등)와의 cell state 유사도(Pearson correlation)로 검증
- **Metric / 평가 기준**: cell state 정의 후 Pearson correlation을 이용한 기존 signature 일치도; Ro/e 기반 조직 편향 정량화
- **주요 수치**: 4.9M 세포, 104 datasets, 30 cancer types; 세포당 $K=5$~$9$ NMF → 35 modules/individual; Geometric sketch로 각 dataset별 서브샘플
- **정성 결과**: AND-gating 알고리즘으로 세포 유형별(CD8⁺ T, NK, Treg, Macrophage, DC, Fibroblast, Endothelial, Cancer cell) hallmark gene signature 추출 성공. UMAP에서 cell type별·기관별 분포 확인 (Fig. 1C, D)
- **논문 주장과의 연결**: 기존 atlas 대비 종양+정상 포함 대규모 통합이 가능해 tumor-specific vs normal-shared 세포 상태 구분의 기반 마련

##### Dataset 2 — Hallmark gene signature 특성화 (8 cancer types, 9 cell types)
- **Dataset**: BRCA, CRC, HCC, HNSC, LC, OV, PAAD, RCC 8개 암종 (정상 조직이 짝으로 있는 암종)
- **목적**: cell type별 종양 특이 hallmark gene 동정
- **사용한 데이터 규모**: 8 암종 × 주요 cell type별 AND-gating 분석
- **Baseline / 비교 대상**: 정상 조직에서의 발현 수준
- **Metric / 평가 기준**: $\log_2$ fold-change > 0 (종양 vs 정상), adjusted $p < 0.05$; GO enrichment (Enrichr, MsigDB Hallmark 2020, GO BP 2023, GO MF 2023)
- **주요 수치**: CD8⁺ T 세포 — 종양에서 CD27, TIGIT, CTLA4, LAG3, PDCD1 상향; 정상에서 IL7R, PTGER2, PTGER4 상향. Macrophage — 종양에서 CCL7, ADAMDEC1, SLAMF9 상향. DC — 종양에서 CCL19, LAMP3 상향. Cancer cell — PRKCA, GSK3B, CAMKK2, PLOD1, EGLN3, P4HA1 (glycolysis, mTORC1, cell cycle 관련) 상향. Fibroblast(tumor) — FAP, COL1A1, COL10A1, MMP11 상향
- **정성 결과**: CD8⁺ T tumor-infiltrating cells에서 면역관문 exhaustion 마커 풍부, DC에서 CCL19/LAMP3의 inflammatory·migratory 기능 관련. PAAD에서 CD8⁺ T cell이 PDCD1, LAG3를 발현하지 않아 PAAD에서 checkpoint inhibitor 반응이 낮은 이유를 부분 설명 (Fig. 2A)
- **논문 주장과의 연결**: 기관·세포 유형에 걸쳐 공통 hallmark gene을 AND-gating이 효과적으로 추출함을 보임

##### Dataset 3 — AKR1C1⁺ vs WNT5A⁺ 염증성 fibroblast 아형 특성화
- **Dataset**: BRCA, OV, UCEC, CRC, HNSC 5개 암종 mesenchymal cell 분석
- **목적**: 두 염증성 fibroblast 아형의 기능적 차이와 공간적 분포 차이 규명
- **사용한 데이터 규모**: Mesenchymal NMF module에서 추출된 cell state; BRCA, OV, CRC, HNSC 공간 전사체 분석 (smFISH $n=3$ CRC/HNSC 조직 샘플, magnification 20X)
- **Baseline / 비교 대상**: 다른 fibroblast subtype (CCL19⁺, BMP4⁺, PI16⁺, desmoplastic, myofibroblast 등)
- **Metric / 평가 기준**: Ro/e (조직 편향), CellPhoneDB ligand-receptor 상호작용 강도, Pearson correlation (spatial co-localization)
- **주요 수치 (Fig. 3E, 4F, G)**: AKR1C1⁺ fibroblast — tumor에서 Ro/e 상향; BRCA·OV에서 cancer cell, neutrophil, CTSK⁺ macrophage, DC1, PRR-induced mo-DC와 co-localization. WNT5A⁺ fibroblast — CRC·HNSC에서 desmoplastic fibroblast, exhausted CD8⁺ T cell, Treg, DC1, PRR-induced mo-DC와 co-localization. CRC와 HNSC에서 WNT5A를 정상 조직에서 발현 없음; CRC/HNSC에서 AKR1C1을 발현하지 않는 정상 조직도 있음 (반대 패턴).
- **정성 결과**: AKR1C1⁺ fibroblast는 IL6/CTSK⁺ macrophage 축을 통해 pro-tumorigenic; WNT5A⁺ fibroblast는 면역억제(Treg/exhausted T cell)와 proximity하여 immunosuppressive TME 형성. smFISH로 CRC/HNSC의 desmoplastic stroma에서 WNT5A⁺ fibroblast를 공간적으로 확인 (Fig. 4E, F, G)
- **논문 주장과의 연결**: 두 fibroblast 아형이 동일한 CXCL1/3/8을 공유하지만 기관 분포·상호작용 파트너·공간 패턴에서 기능적으로 구분됨을 직접 증명

##### Dataset 4 — 면역치료 예측 cell state 동정 (1,261명 bulk RNA-seq meta-analysis)
- **Dataset**: 4개 암종 8개 면역치료 cohort — LC 본원 cohort ($n=497$, SMC), melanoma (Van Allen $n=75$, Gide $n=73$, Riaz $n=46$, Hugo $n=25$), bladder (Mariathasan $n=347$), RCC (McDermott $n=165$, Miao $n=33$)
- **목적**: 면역치료 반응을 예측하는 cell state와 비예측 cell state 구분
- **사용한 데이터 규모**: $n=1,261$; 4 cancer types; 8 cohorts; unified processing pipeline (Trimmomatic, STAR, HTSeq, TPM 정규화)
- **Baseline / 비교 대상**: 기존 면역치료 반응 signature (PD-L1 pathway, antigen-presenting machinery, interferon signatures — 타 연구 gene sets)
- **Metric / 평가 기준**: ssGSEA로 cell state score 산출 → logistic regression per cohort → metagen으로 random effects meta-analysis → OR (95% CI), $p$-value
- **주요 수치**: Exhausted CD8⁺ T cell state 및 CXCL9⁺ macrophage, mesenchymal-derived interferon, LAMP3⁺ DC, CCL19⁺ fibroblast 등 인터페론 풍부 community state들이 OR > 1 (favorable). Desmoplastic fibroblast, osteoblast, CTSK⁺ macrophage는 OR < 1 (adverse). TLS signature: OR ≈ 1.3 ($p = 1.4 \times 10^{-3}$, Fig. 6C). 면역치료 예측 cell state들의 TCGA 생존 분석에서 유의미한 예후 연관성은 대부분 없음 (Supp. Fig. S17, S18) — 이는 면역치료가 특정 cohort에서 반응을 나타내지만 전체 예후에는 영향이 작음을 시사
- **정성 결과**: 인터페론 풍부 community state 내 구성 cell type들이 면역치료 반응을 예측. PRR-induced activation state와 TLS 비구성 일부 cell type(exhausted CD8⁺ T, ISG15⁺ macrophage, pDC)은 공간적으로 TLS와 무관하나 면역치료에 favorable
- **논문 주장과의 연결**: TLS 및 interferon-enriched community가 면역치료 반응과 연계되나, 단순 TLS 정의만으로는 반응 예측의 복잡성을 충분히 반영하지 못함을 강조

##### Dataset 5 — 공간 전사체 분석 (137 datasets, 11 cancer types)
- **Dataset**: BLCA, BRCA, CRC, HCC, HNSC, LC, OV, PAAD, RCC, SSCC, UCEC 11개 암종 spatial transcriptomics ($n=137$)
- **목적**: TLS signature의 공간적 분포 확인, TLS-enriched vs non-enriched cell type 동정
- **사용한 데이터 규모**: 137 spatial transcriptome datasets; cell2location deconvolution; RCC TLS-labeled data로 TLS signature 검증 ($n=17$ RCC samples, Wilcoxon rank sum test)
- **Baseline / 비교 대상**: TLS 양성 vs TLS 음성 spot; cell2location으로 단일 세포 atlas를 reference로 사용
- **Metric / 평가 기준**: TLS signature score (ssGSEA sc.tl.score), Pearson correlation (cell type spatial co-localization), OR (TLS signature 예측력), Wilcoxon rank sum test $p$-value
- **주요 수치**: TLS signature score — TLS vs non-TLS spot 비교: $p = 1.5 \times 10^{-5}$, $n=17$ RCC samples (Fig. 6B). TLS signature 면역치료 반응 예측: OR ≈ 1.3, $p = 1.4 \times 10^{-3}$ (Fig. 6C). TLS-enriched cell types (BH adjusted $p < 0.05$): Treg, plasma cell, CD8⁺ T, XCL1⁺ NK, FCN1⁺ mono-MΦ, CD4⁺ T, LAMP3⁺ DC, PI16⁺ fibroblast, Th, CCL19⁺ fibroblast (Fig. 6D). TLS-depleted: CTSK⁺ macrophage, desmoplastic fibroblast, mesothelium-derived fibroblast, cancer cell (Fig. 6D).
- **정성 결과**: 11개 암종에서 TLS signature와 TLS-enriched cell type들의 공간 co-localization 패턴이 일관적으로 확인 (Fig. 6E). Desmoplastic fibroblast/SPPI⁺ macrophage는 WNT5A⁺ fibroblast와 상호 배타적으로 존재하는 패턴 관찰 (Supp. Fig. S20B).
- **논문 주장과의 연결**: TLS signature가 공간적으로 실제 TLS를 반영하고 면역치료 반응을 예측함을 다중 데이터 수준에서 검증

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 인터페론 신호 풍부 community state (LAMP3⁺ DC, CCL19⁺ fibroblast, CXCL9⁺ macrophage, exhausted CD8⁺ T 등)가 tumor/adjacent normal/healthy normal 간 rewiring을 보이며 면역치료에 consistently favorable. Pro-tumorigenic community (desmoplastic fibroblast, CTSK⁺ macrophage, pEMT cancer cell, SPPI⁺ macrophage)는 consistently adverse.
- **가장 중요한 수치**: TLS signature 면역치료 반응 OR ≈ 1.3 ($p = 1.4 \times 10^{-3}$, $n=1,261$); TLS vs non-TLS spot score 차이 $p = 1.5 \times 10^{-5}$ (RCC)
- **baseline 대비 차이**: 기존 PD-L1, antigen-presenting machinery, interferon signature들도 함께 검증하여, 이 논문의 cell state-based score가 기존 signature와 comparable 또는 complementary임을 확인 (Fig. 5E)
- **결과 해석 시 주의점**: TCGA 생존 분석에서 대부분 cell state가 유의미한 예후 연관성이 없어 면역치료 특이적 반응 예측 지표임에 한정. 대부분 cell state의 임상 예측력은 단일 암종이 아닌 pooled cohort에서 나타남.

---

## Figures

#### Figure 1 — Pan-cancer tumor-normal single-cell landscape overview

- **이 Figure가 필요한 이유**: 논문의 핵심 주장인 "대규모 tumor-normal 통합 atlas 구축"을 시각적으로 제시하기 위해. 데이터 규모, 처리 파이프라인, 최종 UMAP 결과를 한눈에 보여준다.
- **이 Figure가 뒷받침하는 주장**: 104 datasets, 4.9M 세포, 30 암종을 통합한 tumor-normal atlas가 실제로 구축되었음을 입증.

##### 패널별 설명
- **A**: 30 암종별 tumor/normal 샘플 수를 원형 차트로 표시. BRCA, LC, HNSC, HCC 순으로 다수. Tumor(적색)와 Normal(녹색/청색) 막대 비율 시각화.
- **B**: scRNA-seq 처리 파이프라인 흐름도. Log-normalization → NMF ($K=5$~$9$) → max-normalization → Leiden clustering → UMAP → AND-gating signature → cell projection 순서.
- **C**: 최종 UMAP — 주요 세포 유형(B cell, CD4⁺ T, CD8⁺ T, Mast, Monocyte-derived macrophage, DC, Endothelial, Epithelial, Fibroblast, Macrophage, NK, Pericyte, Plasma cell, Plasmacytoid DC, Treg)으로 채색.
- **D**: 동일 UMAP를 기관 원산지(22 장기)로 채색하여 조직 편향 시각화.
- **E**: NMF module clustering 과정 — mitochondrial/ribosomal cluster 제거 → soup-contaminated cluster 제거 → final NMF UMAP. 하단에 Coincidence / Cell state heterogeneity / Survival analysis / Cell projection / Spatial transcriptomics 5가지 downstream analysis 아이콘.

##### 본문에서 강조한 비교
- 비교 대상: tumor sample vs. normal sample UMAP 분포
- 관찰된 차이: UMAP에서 cell type별 분리는 명확하나, 동일 cell type 내에서 기관 및 tumor/normal 기원에 따른 heterogeneity 존재
- 이 차이가 의미하는 것: 세포 유형 수준 annotation 이후 세포 상태 수준 분해(NMF)가 필요함을 시각적으로 정당화

##### 해석 시 주의점
- UMAP은 전체 4.9M 세포가 아닌 Geometric sketch로 선택된 서브셋을 표시. 희귀 cell type은 과소 표현될 수 있음.

---

#### Figure 2 — Tumor ecosystem hallmark gene signature landscape

- **이 Figure가 필요한 이유**: AND-gating 알고리즘이 실제로 cell type별 보편적 hallmark gene을 추출했음을 보이고, GO enrichment를 통해 생물학적 의미를 제시하기 위해.
- **이 Figure가 뒷받침하는 주장**: 종양 조직에서 각 세포 유형별로 재현 가능한 hallmark 발현 프로그램이 존재하며, 이것이 기관에 걸쳐 공통적임.

##### 패널별 설명
- **A**: 8개 암종 × 주요 세포 유형의 hallmark gene을 $\log_2$ fold-change heatmap으로 표시. 적색=종양에서 상향, 청색=정상에서 상향. 4개 이상 암종에서 공통으로 나타난 gene만 표시.
- **B**: 세포 유형별 주요 marker gene에 대한 상세 heatmap — 8 암종 × 종양/정상 조건. AKR1C1, WNTSA 등 fibroblast 관련 gene 포함.
- **C**: 세포 유형별 GO 분석 bubble plot. Color = odds ratio, size = $-\log_{10}$(adjusted $p$-value). CD8⁺ T cell — mTORC1, interferon type II 반응 강조; Macrophage — phagocytosis, TNF signaling; Fibroblast — extracellular matrix, cell migration; Endothelial — angiogenesis.

##### 본문에서 강조한 비교
- 비교 대상: PAAD에서 CD8⁺ T cell vs. 다른 암종의 CD8⁺ T cell
- 관찰된 차이: PAAD에서 PDCD1, LAG3 발현이 없음 (Fig. 2A, B)
- 이 차이가 의미하는 것: PAAD에서 면역관문 억제제 반응이 낮은 원인을 단일 세포 수준에서 설명 가능

##### 해석 시 주의점
- AND-gating 결과는 4개 이상 암종에서 공통인 gene만 표시 → 드문 암종 특이 gene은 제외. 인과 관계가 아닌 발현 상관관계.

---

#### Figure 3 — Tumor-normal ecosystem deconvolution into heterogeneous cell states

- **이 Figure가 필요한 이유**: NMF 기반 cell state 정의 결과를 myeloid와 mesenchymal 두 주요 비T 세포 계통에서 구체적으로 보여주고, Ro/e 분석으로 조직 편향을 정량화하기 위해.
- **이 Figure가 뒷받침하는 주장**: 각 세포 유형이 단일 상태가 아니라 다양한 cell state의 혼합이며, 이들의 조직(tumor/normal) 편향이 기능과 연계됨.

##### 패널별 설명
- **A**: Myeloid cell state UMAP — C1QC⁺, CD16⁺ mono-MΦ, CTSK⁺ macrophage, CXCL9⁺ macrophage, LAMP3⁺ DC 등 16 state로 채색.
- **B**: Myeloid cell의 reference component 분석 UMAP — NMF module을 기존 cell type reference에 projection.
- **C**: Mesenchymal cell state UMAP — AKR1C1⁺/WNT5A⁺ inflammatory fibroblast, CCL19⁺ fibroblast, desmoplastic fibroblast, myofibroblast 등.
- **D**: Mesenchymal cell reference component UMAP.
- **E**: 주요 mesenchymal cell state의 Ro/e dot plot (tumor/adjacent normal/normal). WNT5A⁺ inflammatory fibroblast는 tumor에서 풍부(Ro/e > 0). Interferon state들은 tumor에서 풍부. Desmoplastic fibroblast는 tumor에서 풍부, normal에서 depleted.
- **F**: Circos plot — 11개 주요 cell state 간 co-occurrence. Tumor(황색)와 Normal(청색) tissue에서 network 연결 패턴 차이. 호의 두께가 co-occurrence 강도에 비례.

##### 본문에서 강조한 비교
- 비교 대상: Tumor vs. normal tissue에서 Ro/e
- 관찰된 차이: Desmoplastic fibroblast, WNT5A⁺ fibroblast는 tumor-specific; Interferon state는 tumor에서 강화
- 이 차이가 의미하는 것: 특정 cell state는 종양 미세환경에서 선택적으로 유도되거나 유지됨을 정량적으로 지지

##### 해석 시 주의점
- Ro/e는 카이제곱 기반 기대값 대비 관찰값. 샘플 수 불균형(tumor vs. normal 수 차이)이 Ro/e 값에 영향을 줄 수 있음.

---

#### Figure 4 — AKR1C1⁺ and WNT5A⁺ inflammatory fibroblast characterization

- **이 Figure가 필요한 이유**: 두 염증성 fibroblast 아형의 차이를 marker gene, 기관 분포, 세포 상호작용, 공간적 확인까지 다층적으로 증명하기 위해. 이 fibroblast들이 면역억제 또는 pro-tumorigenic TME에서 서로 다른 역할을 한다는 주장의 핵심 증거.
- **이 Figure가 뒷받침하는 주장**: AKR1C1⁺ vs WNT5A⁺ inflammatory fibroblast는 독립적인 아형이며, 세포 상호작용 파트너와 공간적 위치가 다르다.

##### 패널별 설명
- **A**: AKR1C1⁺, WNT5A⁺ fibroblast와 다른 fibroblast subtype(CCL19⁺, PI16⁺)의 marker gene dot plot. AKR1C1: AKR1C1, FOSL1, IL6, CXCL1-3, GREM1, WNT5A: WNT5A, MMP3, GREM1이 상이하게 강조.
- **B**: 각 fibroblast subtype의 암종별 비율 bar plot (tumor 조직 내).
- **C**: 암종별(BRCA, OV, CRC, HNSC 등) normal vs. tumor 조직에서 AKR1C1/WNT5A 발현 패턴. CRC/HNSC에서 opposite pattern 확인.
- **D**: CellPhoneDB 기반 AKR1C1⁺ vs WNT5A⁺ fibroblast의 ligand-receptor 상호작용 heatmap. AKR1C1⁺ — CTSK⁺ macrophage/DC1/PRR-induced mo-DC 중심; WNT5A⁺ — desmoplastic fibroblast/BMP4⁺ fibroblast/endothelial 중심.
- **E**: smFISH — CRC(상단)와 HNSC(하단) FFPE 조직에서 WNT5A, PDGFRA, GREM1 probe 신호. 화살표: 중첩 신호로 WNT5A⁺ fibroblast 위치 확인. Scale bar = 100 μm, magnification 20X.
- **F**: BRCA/OV에서 AKR1C1⁺ fibroblast의 spatial co-localization (cancer cell, desmoplastic fibroblast, neutrophil, DC1, PRR-induced mo-DC, CTSK⁺ macrophage).
- **G**: CRC/HNSC에서 WNT5A⁺ fibroblast의 spatial co-localization (cancer cell, desmoplastic fibroblast, neutrophil, DC1, PRR-induced mo-DC, exhausted CD8⁺ T cell).

##### 본문에서 강조한 비교
- AKR1C1⁺: cancer cell/CTSK⁺ macrophage와 co-localization → pro-tumorigenic microenvironment 형성
- WNT5A⁺: exhausted CD8⁺ T cell/Treg과 co-localization → immunosuppressive microenvironment 형성

##### 해석 시 주의점
- smFISH는 $n=3$ 조직 샘플(CRC, HNSC). 통계적 검정 없이 대표 이미지로 제시. Spatial co-localization은 Pearson correlation 기반으로 인과 관계가 아닌 공간적 연관성.

---

#### Figure 5 — Interferon-enriched/pro-tumorigenic community states and immunotherapy prediction

- **이 Figure가 필요한 이유**: co-occurrence network를 tumor/normal/adjacent normal 3가지 조직 유형에서 비교하고, 면역치료 예측력이 있는 cell state를 meta-analysis로 동정하기 위해.
- **이 Figure가 뒷받침하는 주장**: 인터페론 풍부 community가 tumor에서 특이적으로 구성되며, 이를 구성하는 cell state들이 면역치료 반응과 연관된다.

##### 패널별 설명
- **A**: Tumor co-occurrence network — 노드=cell state, 엣지 두께=adjacency. Modularity community별 색상 구분. Interferon-enriched community: LAMP3⁺ DC, CCL19⁺ fibroblast, CXCL9⁺ macrophage 등이 dense subnetwork 형성.
- **B**: Normal co-occurrence network — tumor 대비 interferon community가 산재; LAMP3⁺ DC 주변 immune cell이 healthy normal에서 분산.
- **C**: Adjacent normal co-occurrence network — tumor와 normal의 중간 패턴.
- **D**: 면역치료 cohort 정보 table — cancer type, sample 수, unified processing pipeline.
- **E**: Forest plot — cell state별 OR (95% CI). 적색=favorable (OR > 1), 청색=adverse (OR < 1). 통계적 유의성에 달한 cell state만 표시. Exhausted CD8⁺ T cell, CXCL9⁺ macrophage, LAMP3⁺ DC, CCL19⁺ fibroblast, Tfh 등 favorable; CTSK⁺ macrophage, desmoplastic fibroblast adverse.

##### 본문에서 강조한 비교
- Tumor vs. normal vs. adjacent normal에서 interferon-enriched community의 rewiring
- 면역치료 favorable cell state들이 대부분 interferon-enriched community 소속임을 시각적으로 정량적으로 확인

##### 해석 시 주의점
- Forest plot의 OR은 4개 암종(BLCA, MEL, RCC, LC)의 pooled estimate. 단일 암종에서의 OR는 이보다 effect size와 significance가 작을 수 있음.

---

#### Figure 6 — Spatial transcriptome analysis of tumor ecosystems

- **이 Figure가 필요한 이유**: 단일 세포 atlas에서 정의한 TLS signature와 cell state가 실제 조직 공간에서도 유효한지 확인하고, TLS signature의 면역치료 예측력을 공간적으로 뒷받침하기 위해.
- **이 Figure가 뒷받침하는 주장**: TLS signature가 실제 TLS 조직 spot과 일치하며, 이 signature로 면역치료 반응을 예측할 수 있다.

##### 패널별 설명
- **A**: 11개 암종별 spatial transcriptome dataset 수 bar chart. BRCA, CRC, HNSC, LC, RCC 등 다수.
- **B**: TLS signature score — TLS vs non-TLS spot (RCC, $n=17$). Boxplot; $p = 1.5 \times 10^{-5}$ (Wilcoxon rank sum test). TLS spot에서 score 유의하게 높음.
- **C**: TLS signature 면역치료 반응 예측. OR ≈ 1.3 (95% CI 1.1~1.5 추정), $p = 1.4 \times 10^{-3}$, $n=1,261$. 점=OR, 선=95% CI.
- **D**: TLS-enriched/depleted cell type barplot (BH adjusted $p < 0.05$). TLS-enriched: Treg, Th17, plasma cell, CD8⁺ T, XCL1⁺ NK 등. TLS-depleted: CTSK⁺ macrophage, desmoplastic fibroblast, mesothelium-derived fibroblast, cancer cell.
- **E**: 11개 암종 6개 cell type/signature의 spatial co-localization heatmap. Treg, LAMP3⁺ DC, plasma cell, CCL19⁺ fibroblast, PI16⁺ fibroblast, cancer cell. TLS signature가 높은 spot에서 Treg/LAMP3⁺ DC/plasma cell이 풍부.

##### 본문에서 강조한 비교
- TLS signature score: TLS spot $\gg$ non-TLS spot ($p = 1.5 \times 10^{-5}$)
- 면역치료 반응 예측에서 TLS signature가 유의미함을 기존 TLS 예측 연구(Sautes-Fridman et al., Schumacher et al.)와 비교하여 reinforcement

##### 해석 시 주의점
- B panel은 RCC 17 samples에만 기반. 다른 암종에서의 TLS signature 검증은 co-localization만으로 간접적. C panel은 bulked RNA-seq cohort 기반이므로 spatial heterogeneity는 반영 안 됨.

---

## Tables

본문에 정식 Table은 없음 (Fig. 5D의 cohort 정보가 인라인 table 형태로 제시됨).

### Fig. 5D 인라인 — 면역치료 cohort 정보

- **이 Table이 필요한 이유**: meta-analysis에 사용된 각 cohort의 출처, 암종, 샘플 수, 처리 파이프라인을 명시하여 재현성을 확보하기 위해.
- **이 Table이 뒷받침하는 주장**: meta-analysis가 통일된 pipeline으로 처리된 4개 암종 8개 cohort를 기반으로 함.

#### 표 구조
- Row: cohort (본원 LC, Van Allen melanoma, Gide melanoma, Riaz melanoma, Hugo melanoma, Mariathasan bladder, McDermott RCC, Miao RCC)
- Column: Cancer type, Number of samples, Unified processing pipeline
- Total: $n = 1,261$

#### 핵심 수치
- LC (본원 SMC): $n = 497$ (가장 큰 코호트)
- Bladder (Mariathasan): $n = 347$
- RCC (McDermott): $n = 165$
- Melanoma 4 cohort 합산: $n = 219$

#### 해석 시 주의점
- LC cohort가 $n=497$로 전체의 39%를 차지하여 meta-analysis에서 가중치가 크다. LC 특이 결과가 전체 OR에 과도하게 영향을 줄 수 있음.

---

## Supplementary Information

### Supplementary Data 개요 (MOESM3 기반)

- **Supplementary Data 1**: 104개 scRNA-seq dataset 정보 (accession, cancer type, 샘플 수 등)
- **Supplementary Data 2**: NMF 기반 cell state별 상위 유전자 및 기존 연구 gene signature
- **Supplementary Data 3**: 137개 spatial transcriptome dataset 정보 (11개 암종)
- **Supplementary Data 4**: cell type별 보편적 hallmark gene signature; p-value는 two-sided t-test + BH correction
- **Supplementary Data 5**: 면역치료 scRNA-seq dataset 정보
- **Supplementary Data 6**: 면역치료 반응자/비반응자에서 공통 upregulated gene signature; two-sided t-test + BH correction
- **Supplementary Data 7**: TLS gene signature; two-sided Wald test + BH correction (PyDESeq2)
- **Supplementary Data 8**: LC cohort (SMC $n=497$) 임상 특성

### Supplementary Figures (MOESM1, 44MB) — 주요 내용

- **Supp. Fig. S1A, B**: Geometric sketch 품질 확인; NMF module UMAP — 전체 vs. subsampled
- **Supp. Fig. S1C**: soup-contaminated cluster 자동 탐지 예시
- **Supp. Fig. S2A, B**: AND-gating 알고리즘 적용 세부 — cell type별, 기관별 fold-change 분포
- **Supp. Fig. S3, S4**: NMF 기반 myeloid/T cell/epithelial/neural cell state 상세 annotation; 기존 문헌 signature와 Pearson correlation 검증
- **Supp. Fig. S5A, B**: CD8⁺ T cell Ro/e 조직 분포 — exhausted state와 PRR-induced state의 조직 편향
- **Supp. Fig. S6, S7**: Reference component 구성 방법 및 cell type annotation quality check
- **Supp. Fig. S8**: PRR-induced activation state 기원 분석 (주로 부인암 origin)
- **Supp. Fig. S9**: Epithelial/neural cell state 35 subpopulation UMAP
- **Supp. Fig. S10C, D**: Renal cell carcinoma(RCC) hypoxia/metal response signature; glioblastoma pEMT/oxidative phosphorylation signature
- **Supp. Fig. S11**: 전체 mesenchymal cell state 상세 UMAP 및 marker gene
- **Supp. Fig. S12A–E**: AKR1C1⁺/WNT5A⁺ fibroblast 기관별 상세 scRNA-seq 분포 및 CellPhoneDB 상호작용
- **Supp. Fig. S13, S14**: smFISH CRC/HNSC 추가 이미지
- **Supp. Fig. S15**: WNT5A⁺ fibroblast 면역치료 전/후 HNSC 비교
- **Supp. Fig. S16**: 모든 11개 암종 spatial co-occurrence 네트워크
- **Supp. Fig. S17, S18**: 면역치료 예측 cell state들의 TCGA 생존 예후 분석 — 대부분 유의미하지 않음
- **Supp. Fig. S19A, B**: CD8⁺ T cell immunotherapy responder gene signature (PDCD1, LAG3, CXCL13, CXCR6 등)
- **Supp. Fig. S20A, B**: 면역치료 favorable/adverse component spatial co-localization pattern

---

## 분석 자체에 대한 메모

- **PDF 읽기 범위**: main paper pp.1–17 (전문) + MOESM3 (supplementary description) 완독. MOESM1 (supplementary figures, 44MB), MOESM2 (supplementary notes, 15MB)는 summary만 확인 — 상세 figure는 개별 확인 필요.
- **수치 precision**: smFISH n=3로 제시된 수치는 대표값. Spatial co-localization Pearson correlation 구체적 수치는 Supplementary Fig.에 있으나 본 분석에서 접근 안 됨 (`미제공: 구체적 Pearson r값`).
- `질문:` TLS signature 예측력 OR ≈ 1.3 ($n=1,261$)의 세부 cohort별 heterogeneity($I^2$)가 본문에 제시되지 않음 — 코호트 간 이질성이 크면 pooled OR의 신뢰도 제한.
- `질문:` AKR1C1⁺ 및 WNT5A⁺ fibroblast 각각을 ADC target로 검토할 때 정상 조직 발현 수준이 기관별로 다름 (Fig. 4C) — 이를 ADC selectivity index 계산에 어떻게 반영할지 별도 추출 필요.
- `검토필요:` Fig. 6D의 TLS-enriched cell type 중 PI16⁺ fibroblast가 포함된 것은 본문에서 별도 설명이 없음. Supp. Fig. 확인 필요.
