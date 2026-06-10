<!-- liu-2023-ctc-scrna-protocol_core.md — PDF 전문 기반 재분석 (2026-06-10) -->

## Executive Summary

- **무엇**: PDAC(췌장 선암) 간전이 환자에서 CTC(circulating tumor cells)를 EpCAM/CA19-9 코팅 microfluidic chip으로 분리하고, 10x Genomics Chromium scRNA-seq로 프로파일링하며, CellPhoneDB로 immune checkpoint ligand-receptor pair를 동정하는 wet-lab + 전산 end-to-end 프로토콜.
- **모델 / 방법**: HPV 혈액 → RBC lysis → microfluidic chip CTC 포획 → FACS solid tumor 단일세포 분리 → 10x Chromium 3' scRNA-seq → Seurat v4 QC/clustering/annotation → CopyKAT CNV CTC 확인 → CellPhoneDB v2 interaction weight score로 immune checkpoint pair 동정.
- **핵심 결과**:
  - ① PDAC 간전이 환자 6명 HPV 혈액에서 Hoechst⁺ EpCAM⁺ CD45⁻ CTC 검출, microfluidic chip elution 후 scRNA-seq 투입 (Figure 1).
  - ② 혈액 유래 세포 t-SNE에서 CTC cluster (PTPRC⁻ CD9⁺ KRT8⁺ PPBP⁺ PF4⁺ + CNV aneuploidy)가 면역세포와 분리 동정 (Figure 3).
  - ③ CTC–면역세포 간 CD94-NKG2A:HLA-E, LGALS9:CD47, SIPRA:CD47, TIGIT:NECTIN2/3 등 CTC 특이적 immune checkpoint pair 동정 (Figure 5).
- **우리 적용**: `pipeline-applicable` + `methodology-reference` — CTC 분리 SOP와 scRNA-seq QC/annotation pipeline을 우리 CTC ADC 파이프라인의 wet-lab 표준 및 bioinformatics baseline으로 직접 참조 가능.
- **심층**: 한계·재현 ROI는 `liu-2023-ctc-scrna-protocol_lens-academic.md` / `liu-2023-ctc-scrna-protocol_lens-industry.md` / `liu-2023-ctc-scrna-protocol_methodology-brief.md` 참고.

---

## Identity

| 항목 | 내용 |
|---|---|
| Title | Protocol for identifying immune checkpoint on circulating tumor cells of human pancreatic ductal adenocarcinoma by single-cell RNA sequencing |
| Authors | Xiaowei Liu, Jinen Song, Xinyu Liu, Hao Zhang, Xueyan Wang, Yuanxi Li, Zhankun Yang, Jing Jing, Xuelei Ma*, Hubing Shi* |
| Year | 2023 |
| Venue | STAR Protocols 4, 102539 |
| DOI | 10.1016/j.xpro.2023.102539 |
| PMC | PMC10491853; PMID 37659082 |
| Citation key | `@liu2023ctcscrnaprotocol` |
| License | CC BY-NC-ND 4.0 (Open Access) |
| 소속 | Institute for Breast Health Medicine / Dept. of Biotherapy, West China Hospital, Sichuan University; Dept. of Pancreatic Surgery, West China Hospital; College of Chemical Engineering, Shijiazhuang University |
| Correspondence | drmaxuelei@gmail.com (X.M.), shihb@scu.edu.cn (H.S.) |

---

## Background

### 배경 스토리

- **문제의 출발점**: CTC는 원발 종양에서 혈행으로 이탈해 전이를 개시하는 세포로, 저자는 "종양 전이의 씨앗"으로 표현한다 (Summary). PDAC는 발견 시 이미 전이가 진행된 경우가 많아 예후가 극히 불량하며, CTC를 통한 liquid biopsy가 기존 조직 생검의 대안 경로로 주목받는다.
- **Immune checkpoint 접근의 필요성**: CTC가 혈중 면역세포의 감시를 회피하는 기전이 충분히 밝혀지지 않았으며, CTC 표면의 면역관문 분자가 전이 개시에 어떻게 기여하는지 단일세포 수준에서 분석한 연구는 드물었다 (ref. 1 = Liu et al. 2023 Cell 41:272–287).
- **CTC 분리 방법의 기술적 한계**: 전통적 Ficoll 밀도원심분리나 단일 EpCAM 항체 분리는 PDAC CTC에서 EMT(epithelial-mesenchymal transition) 진행 세포의 capture efficiency 감소 문제가 있다. EpCAM + CA19-9 이중 항체 코팅 microfluidic chip이 이 한계를 일부 보완할 수 있다.
- **HPV 혈액 접근**: PDAC 간전이 환자에서 hepatic portal vein(HPV) 혈액은 말초혈 대비 CTC 농도가 높아, 간 전이 연구에 적합한 소스임을 이 프로토콜의 전제로 삼는다.
- **단일세포 분석의 필요성**: Bulk transcriptomics로는 CTC를 혈액 내 다른 세포에서 분리 분석하기 어렵다. scRNA-seq + CNV 분석 조합이 CTC 동정 + immune checkpoint profile 분석을 동시에 가능케 한다.
- **이 프로토콜로 이어지는 gap**: Liu et al. 2023 Cell 논문 (ref. 1)의 연구 데이터를 재현 가능한 step-by-step 절차로 문서화하고, 다른 연구자가 PDAC 및 유사 암종에 적용할 수 있게 표준화해야 했다.

### 기본 개념

- **CTC (circulating tumor cells)**: 원발 종양 또는 전이 병소에서 혈행으로 이탈한 종양세포. Liquid biopsy의 핵심 표적. PDAC에서는 간문맥(HPV) 혈액에서 농도가 높다.
- **EpCAM (CD326)**: 상피세포 부착분자. CTC capture의 가장 보편적 항원. EMT 진행 시 발현 감소 — 이 프로토콜은 CA19-9 항체를 병용해 보완한다.
- **MerryHealth microfluidic chip**: EpCAM + CA19-9 항체 코팅 미세유체 칩. 포획 → elution으로 생존 CTC 회수. 칩을 항상 wet 상태로 유지해야 하며(CRITICAL), 전 과정 4°C 유지.
- **CopyKAT (Copy Karyotype Analysis Tools)**: scRNA-seq count matrix에서 염색체 복제수 변이(CNV)를 추론. 면역세포를 normal control로 삼아 종양세포(aneuploidy)를 구분. marker gene annotation을 보완하는 이중 검증 도구.
- **CellPhoneDB v2.0**: 리간드-수용체 쌍의 통계적 유의성(permutation test)으로 세포 유형 간 상호작용을 정량화. 이 프로토콜은 기본 interaction count 대신 expression-weighted **interaction weight score** (유의한 L-R pair의 발현량 합산)를 사용.
- **Immune checkpoint**: T/NK 세포의 면역 활성화를 억제하는 신호 분자 쌍. PD-1:PD-L1, CTLA-4:CD80 외에도, CTC에서 CD94-NKG2A:HLA-E, LGALS9:CD47, TIGIT:NECTIN2/3 등이 확인됨.

### 이 프로토콜의 필요성

- **핵심 이유**: PDAC CTC scRNA-seq는 wet-lab 난이도(CTC 희귀성, 세포 생존율 유지, 소량 세포 library 작성)와 전산 난이도(CTC 동정, CNV 분석, 면역관문 동정)가 모두 높아 표준 SOP가 부재했다.
- **기존 방법으로 부족했던 지점**: 단일 EpCAM 항체 + Ficoll 분리는 PDAC CTC 수율 부족. 표준 Seurat pipeline은 CTC-specific CNV 검증 및 면역관문 분석 단계 미포함.
- **이 프로토콜이 해결하려는 방향**: HPV 혈액 채취 → microfluidic chip CTC 분리 → 10x scRNA-seq → Seurat + CopyKAT CTC 동정 → CellPhoneDB interaction weight score 기반 면역관문 분석을 하나의 재현 가능한 end-to-end 절차로 묶는다.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: PDAC 간전이 환자의 HPV 혈액에서 CTC를 분리하고, 원발/전이 병소 단일세포 현탁액과 함께 scRNA-seq로 프로파일링한 뒤, CTC와 면역세포 간 immune checkpoint ligand-receptor pair를 동정한다.
- **입력**: (1) HPV 혈액 (EDTA 튜브, ≥10 mL, 채취 후 1–2 h 내 처리), (2) 원발췌장종양 및 간전이 병소 신선 조직 (절제 후 15 min 내 tissue storage solution 투입, 1 h 내 실험실 도착).
- **출력**: (1) CTC 단일세포 현탁액 (면역형광 CTC 확인 포함), (2) Cell Ranger count matrix, (3) Seurat 객체 (cell type annotation), (4) CopyKAT CNV heatmap, (5) CellPhoneDB interaction weight score table + dotplot.
- **추정 대상**: CTC cluster 소속 세포 (marker + CNV 이중 기준), immune checkpoint 기능 ligand-receptor pair.
- **핵심 hidden assumption**: EpCAM/CA19-9 양성 세포가 PDAC CTC를 충분히 대표한다는 가정. EMT 완료 CTC는 chip에서 누락될 수 있다.

### 확률 / 통계학적 구조

본 자료는 protocol/procedure 중심이므로 probabilistic model은 없다. 전산 단계의 statistical assumption:

- **QC threshold**: nFeature_RNA > 200 & < 7,500; percent.mito < 25%. doublet = nFeature_RNA > 7,500.
- **Normalization**: `LogNormalize` (scale factor $10^4$).
- **Variable features**: `mean.var.plot` (mean cutoff 0.0125–3, dispersion cutoff 0.5–Inf).
- **Regression**: `nCount_RNA`, `percent.mt` covariates (ScaleData).
- **Clustering**: PCA 40 PC (Elbow plot 기반) → `FindNeighbors` → `FindClusters` (resolution = 1.0). Blood subset은 동일 파라미터 재적용.
- **CopyKAT**: `KS.cut = 0.1`, `win.size = 25`, euclidean distance, `n.cores = 20` (서버 환경에 따라 조정). 환자별 개별 실행.
- **CellPhoneDB interaction weight score**: $W_{A \to B} = \sum_{\text{sig. L-R pairs, } p < 0.05} \text{mean}(\text{ligand}_A, \text{receptor}_B)$. 기본 count 대신 발현량 가중치를 사용.
- **면역관문 필터**: CellPhoneDB 결과 중 immune checkpoint gene list 포함 pair에서 추가 필터: $p < 0.05$ AND $\text{mean(Molecule1, Molecule2)} > 0.5$.

### 핵심 method insight

- **기존 방법의 한계**: bulk RNA-seq는 CTC–면역세포 상호작용 분리 분석 불가. 단일 EpCAM capture는 EMT-CTC 누락. CellPhoneDB 기본 interaction count는 발현량 미반영.
- **이 프로토콜이 바꾼 가정**: EpCAM + CA19-9 이중 항체 chip으로 PDAC-specific 포획 효율 향상. HPV 혈액 직접 채취로 간문맥 CTC 농도 활용. CellPhoneDB에 expression-weighted score 적용.
- **새로 추가한 구조**: CopyKAT CNV + marker gene (PTPRC$^-$ CD9$^+$ PPBP$^+$ PF4$^+$) 이중 검증으로 CTC 동정 신뢰도 향상. 혈소판 marker(PPBP, PF4)를 CTC marker로 포함한 것은 CTC–platelet cluster 오염 가능성도 내포 (Troubleshooting Problem 6 참조).
- **이 변화가 중요한 이유**: EMT를 겪은 EpCAM$^-$ CTC도 CNV aneuploidy를 보유하므로, marker 분류만으로 놓치는 세포를 CNV로 보완 가능.

### 이전 방법과의 차이

- **Baseline**: 기존 PDAC CTC 연구들의 말초혈 Ficoll 분리 + bulk 면역형광 또는 단일 EpCAM 마이크로비드.
- **공통점**: EpCAM 항체 기반 포획, 10x Genomics 플랫폼 사용.
- **차이점**: ① HPV 혈액 사용 (말초혈 대비 CTC 농도 높음), ② CA19-9 항체 병용 microfluidic chip, ③ CNV + marker gene 이중 CTC 동정, ④ interaction weight score 계산.
- **차이가 크게 나타나는 조건**: EpCAM 발현 감소 EMT-CTC 비율이 높은 환자 (CA19-9 병용 효과 증대).

### 효과가 Results에서 나타난 방식

- **Dataset**: PDAC 간전이 환자 6명; HPV 혈액 6 sample; raw: NGDC GSA-human HRA003672; processed: NGDC OMIX002487.
- **Metric**: (1) CTC 포획 검증 — Hoechst⁺ EpCAM⁺ CD45⁻ 면역형광, (2) 세포 생존율 >80% 권장 (Trypan blue), (3) scRNA-seq 투입 전 ≥100 CTCs 확보 권장.
- **개선된 결과**: HPV 혈액에서 Hoechst⁺ EpCAM⁺ CD45⁻ CTC 시각 확인 (Figure 1G). Solid tumor에서 300,000–500,000 FACS-sorted cells 확보 가능. t-SNE에서 CTC cluster 구분 및 CNV 확인 (Figure 3).
- **정성적 효과**: CTC와 Primary/Metastasis tumor cell 간 immune checkpoint pair가 tissue-of-origin별로 differential함을 시연 (Figure 5).

### Method 관점의 한계

- EpCAM/CA19-9 chip이 단일 상업 제품(Hangzhou MerryHealth)에 종속 — 재현성 제약.
- Capture efficiency 정량 수치 (cells/mL, capture rate%) 미제공.
- CTC ≥100개 미달 시 처리 방법 불명확.
- CellPhoneDB v2.0 사용; v3/v4 호환성 미언급.
- Seurat resolution = 1.0 고정 — 데이터 크기 변화 시 적합성 재검토 필요.
- PPBP, PF4를 CTC marker에 포함 — 혈소판 오염 세포를 CTC로 오분류할 위험 (Problem 6).

---

## Results

### Dataset 1 — PDAC 간전이 환자 코호트

- 환자 수: PDAC 간전이 환자 6명 (West China Hospital, Sichuan University).
- 채취 샘플: HPV 혈액 (각 ≥10 mL, EDTA 튜브), 원발췌장종양 및 간전이 병소 (laparoscopic surgery).
- IRB: West China Hospital Ethics Committee on Biomedical Research 승인.
- Data deposit: Raw — NGDC GSA-human HRA003672; Processed — NGDC OMIX002487 (combined gene expression matrix 다운로드 가능).
- Code: https://github.com/Jinen22/scRNA-PDAC-CC; Zenodo: https://doi.org/10.5281/zenodo.8151927.

### CTC 분리 결과 (Steps 1–19, ~2 h)

- HPV 혈액 → RBC lysis buffer (1:3 v/v, 10 min, 4°C) → 0.1% BSA-HBSS 희석 → 500 g 5 min 원심 → cell resuspension buffer 재현탁 (1–3 × 10⁷ cells/mL) → microfluidic chip 투입 (5 mL/h) → wash (30 mL/h, 3회) → elution buffer (50 mL/h) → 500 g 5 min → 0.01% BSA-HBSS 재현탁.
- 세포 생존율 평가: 0.4% Trypan blue, hemocytometer (>80% 권장).
- CTC 확인: 10% 분취 → TRITC-CD45 + FITC-EpCAM + Hoechst 33342 면역형광 → Hoechst⁺ EpCAM⁺ CD45⁻ = CTC (Figure 1G).
- CRITICAL: ≥100 CTCs 확보 후 10x Genomics 투입 권장.

### Solid tumor 단일세포 분리 결과 (Steps 20–44, ~1–2.5 h)

- 신선 조직 (<1 mm³) → 효소 분해 (0.4 mg/mL collagenase I + IV + 0.25% trypsin, 37°C 10–15 min) → 70 µm 여과 → 500 g 5 min → RBC lysis → FACS 준비.
- FACS (BD FACSAria SORP, 100 µm nozzle): PI⁻ (생존 전체) 또는 PI⁻ CD45⁻ (생존 비면역세포) gate (Figure 2).
- 700–1,200 cells/µL로 재현탁 (FACS count 기반 조정).
- Expected yield: 300,000–500,000 cells/sample.

### scRNA-seq 및 CTC 동정 (Steps 45–63, ~3–4 days)

- 10x Genomics Chromium Next GEM Single Cell 3' GEM, Library & Gel Bead Kit v3; capture target 5,000–8,000 cells; overloading 금지 (doublet rate 0.8%/1,000 cells 증가).
- Sequencing: NovaSeq 6000 (Illumina), 80,000–100,000 reads/cell.
- Cell Ranger v3.0.0, GRCh38 alignment.
- Seurat: 샘플별 로딩 후 merge; QC (nFeature_RNA 200–7,500, percent.mito <25%); LogNormalize; FindVariableFeatures; ScaleData; RunPCA (40 PC); FindNeighbors/Clusters (res=1.0); RunTSNE.
- Blood subset (seu.b): group_tissue == "Blood" subset → 위 pipeline 재실행 (res=1.0, dims 1:40).
- CTC 동정: PTPRC⁻ CD9⁺ KRT8⁺ PPBP⁺ PF4⁺ cluster = 잠재 CTC (Figure 3B). CopyKAT CNV aneuploidy로 확인 (Figure 3C). 두 기준 일치 세포 = CTC (Figure 3D).

### Cell type annotation 및 PDAC atlas (Steps 64–66, >1 day)

- Solid tumor 유래 세포 coarse typing: 8 sub-type (Table 1 marker 기반) — Epithelial, Fibroblast, Endothelial, CTC, B cell, Myeloid, NK, T cell (Figure 4A).
- CopyKAT: primary/metastasis 세포 각 환자별 개별 실행 → Normal/Malignant 구분 (Figure 4C/D).
- 면역세포 sub-typing: 14 sub-type (Table 2 marker 기반) — NK/NKT, CD8 Ex, CD8 EFF, Treg, Memory T, Naive T, B cell, Neutrophil, Monocyte, M1, M2, cDC, pDC, Mast cell (Figure 4E–G).

### 면역관문 동정 결과 (Steps 67–71, ~7 h)

- CellPhoneDB v2.0: Primary, Blood, Metastasis 세 조직 개별 실행 (Python CLI, statistical analysis, 100 iterations).
- Interaction weight score 계산 후 immune checkpoint gene list 필터 (p < 0.05 & mean > 0.5).
- CTC–면역세포 간 주요 immune checkpoint pair (Figure 5):
  - CD94-NKG2A: HLA-E (NK/NKT, CD8 EFF — CTC)
  - CD94-NKG2C: HLA-E
  - LGALS9: CD47, MRC2 (Treg, M2, cDC — CTC)
  - SIPRA: CD47
  - TIGIT: NECTIN2, NECTIN3 (T cell, NK — CTC)
  - HAVCR2: 여러 쌍
- CTC의 immune checkpoint profile이 Primary tumor 및 Metastasis와 조직별로 다른 패턴을 보임 (Figure 5A–C circle plot 비교).

### 전체 결과 요약

HPV 혈액 기반 EpCAM/CA19-9 chip CTC 포획 → 10x scRNA-seq → CopyKAT + marker 이중 CTC 동정 → CellPhoneDB interaction weight score 기반 immune checkpoint 분석의 통합 pipeline이 PDAC CTC의 면역관문 profile을 단일세포 해상도에서 동정 가능함을 시연했다. CTC가 Primary tumor 및 Metastasis와 구별되는 immune checkpoint 분자 조합을 발현할 수 있다는 것이 이 프로토콜의 핵심 biological output이다.

---

## Figures

### Figure 1. The experimental scheme for capturing CTC by microfluidic chip

#### 패널별 설명

- **A/B**: HPV 혈액 EDTA 튜브 채취 전(A)·후 RBC lysis(B) 상태.
- **C**: RBC lysis 후 cell pellet.
- **D**: MerryHealth CTC microfluidic chip 외관.
- **E**: Syringe pump + chip 셋업 (4°C cold table). Collection tube, polyethylene connect tube 위치 표시.
- **F**: Chip 채널 내 포획 세포 현미경 이미지 (scale bar 100/50 µm). 포획 전 wash 확인용.
- **G**: 포획 CTC 다중 면역형광: Hoechst 33342 (blue, 핵), EpCAM (green), CD45 (red). Hoechst⁺ EpCAM⁺ CD45⁻ = CTC (cyan). Scale bar 100 µm.

#### 본문에서 강조한 비교

- Panel G: CTC를 면역세포(CD45⁺)와 구별. EpCAM⁺ CD45⁻ 포획 세포의 CTC 정체성 확인.

#### 해석 시 주의점

- 정량적 capture efficiency(cells/mL, %) 수치 미제공. 시각 확인에 그침.
- 환자별 CTC 수 이질성이 크다고 언급되나 범위 미제공.

---

### Figure 2. FACS sorting strategy for single-cell isolation from solid tumors

#### 패널별 설명

- **A**: PI⁻ 전략 — P1(FSC/SSC, 72.1%), P2(singlet, 87.2%), P3(PI⁻ live, 93.6%).
- **B**: PI⁻ CD45⁻ 전략 — P1(69.3%), P2(86.3%), P3(PI⁻ CD45⁻, 76.2%).

#### 본문에서 강조한 비교

- A는 전체 생존세포, B는 비면역 생존세포만 분리. 분석 목적(면역세포 포함/제외)에 따라 선택.

#### 해석 시 주의점

- 게이팅 퍼센트는 예시 값 (본문에서 "representative" 언급). 샘플별 조정 필요.

---

### Figure 3. Identifying CTCs from HPV-derived cells by scRNA-seq

#### 패널별 설명

- **A**: 혈액 유래 세포 t-SNE — 22개 cluster (색상 코드).
- **B**: Dot plot — cluster별 marker gene 발현 (PTPRC, CD26, CD9, CD70A, CD70B, SBMY1 = CTC; CD20, CD3E, CD3_E3 = B cell; CD3D, CD3E, CD3G = T cell; KLRB1, KLRF1, NKG7 = NK; CD74, AIF1, LYZ = Myeloid). Z-score normalized; dot size = % expressed.
- **C**: CopyKAT CNV heatmap — CTC (malignant) vs. immune cells (normal). Chromosome scale 상단.
- **D**: t-SNE — cell type label (CTC, B cell, Myeloid, NK, T cell).

#### 본문에서 강조한 비교

- B + C 조합: marker gene (PTPRC⁻ epithelial markers⁺) + CNV aneuploidy가 일치하는 cluster만 CTC로 확정.

#### 해석 시 주의점

- CTC cluster의 세포 수 절대값 미제공. 시각적 cluster 크기로만 상대적 규모 추정.
- PPBP, PF4는 혈소판 marker이기도 하여 platelet-CTC contamination cluster 가능성 존재 (Problem 6).

---

### Figure 4. The single-cell transcriptional atlas of PDAC primary tumors and metastatic lesions

#### 패널별 설명

- **A**: UMAP — 전체 세포 (8 major cell type 색상).
- **B**: UMAP — tissue origin (Primary/Portal-Venous/Metastasis).
- **C**: UMAP — CopyKAT 결과 (Normal/Malignant).
- **D**: UMAP — Primary vs. Metastasis epithelial cells.
- **E**: UMAP — 면역세포 14 sub-type.
- **F**: UMAP — 면역세포 tissue origin.
- **G**: Dot plot — 면역 sub-type별 marker gene 발현 (z-score; dot size = % expressed; Table 2 대응).

#### 본문에서 강조한 비교

- Panel A/B: tissue-of-origin별 cell type 분포. Portal-Venous sample에 CTC cluster 존재.
- Panel C/D: CopyKAT으로 malignant epithelial cells 동정 — primary vs. metastasis 차이 시각화.

#### 해석 시 주의점

- 환자 수(6명)가 적어 tissue-origin별 세포 비율이 개인차의 영향을 크게 받음.
- UMAP 투영은 parameter 의존적이므로 cluster 경계 해석에 주의.

---

### Figure 5. The cell-cell interaction between CTC/tumor cells and immunocytes

#### 패널별 설명

- **A–C**: Circle plot — Primary tumor(A), Blood/CTC(B), Metastasis(C) 조직별 tumor cell–immunocyte interaction weight score 네트워크. 선 두께 = 상호작용 강도.
- **D–F**: Dotplot — Primary(D), Blood/CTC(E), Metastasis(F)에서 유의한 immune checkpoint ligand-receptor pair. Color = mean expression; dot size = $-\log_{10}(p)$.

#### 본문에서 강조한 비교

- Blood 조직 (CTC, Panel B/E)에서 CD94-NKG2A:HLA-E, LGALS9:CD47, SIPRA:CD47 등이 Primary/Metastasis와 차별적 패턴.

#### 해석 시 주의점

- Interaction weight score는 전산적 추론이며 실제 세포-세포 물리적 접촉을 증명하지 않는다.
- CTC 세포 수가 적을 경우 dotplot의 statistical power 제한. in vivo 기능 검증(면역회피 실제 효과)은 이 프로토콜 범위 밖임을 저자가 명시.

---

## Tables

### Table 1. Marker genes of each major cell type (본문 Table 1)

| Cell types | Genes |
|---|---|
| Epithelial | EPCAM, CDH1, MUC1, KRT8 |
| Fibroblast | FAP, COL1A1, DCN |
| Endothelial | VWF, CDH5, ENG, PECAM1 |
| CTC | PTPRC, CD9, TIMP1, PPBP, PF4 |
| B cells | CD79A, CD79B, MS4A1 |
| Myeloid | AIF1, CD14, LYZ, FPR1 |
| NK | KLRF1, KLRD1, FGFBP2, NKG7, GNLY |
| T cells | CD3D, CD3E, CD3G |

### Table 2. Marker genes of each immune cell sub type (본문 Table 2)

| Cell types | Genes |
|---|---|
| NK/NKT | KLRB1, KLRF1, KLRD1, NCAM1, CD3D, CD3E, CD3G |
| CD8 Ex | CD8A, LAG3, TIGIT, CTLA4, PDCD1 |
| CD8 EFF | GZMA, GZMK |
| Treg | FOXP3, IL2RA, IKZF2 |
| Memory T | IL7R, LTB |
| Naive T | CCR7, TCF7, LEF1 |
| B cell | CD79A, CD79B, MS4A1 |
| Neutrophil | FCGR3B, FPR1 |
| Monocyte | CD14, FCN1 |
| M1 | CD68, ITGAX, ITGAM, CD86, IL1B |
| M2 | CD163, MRC1, MSR1 |
| cDC | CD1C, FCER1A, CLEC10A |
| pDC | LILRA4, CCDC50, IL3RA |
| Mast cell | MS4A2, TPSAB1, KIT |

---

## Supplementary Information

- GitHub 코드 저장소: https://github.com/Jinen22/scRNA-PDAC-CC
  - `Figure2.R`: cell-cell interaction 시각화 스크립트
  - `Cellchat_cell_contact_gene_20211213.csv`: cell connect gene list
  - `cellphonedb_gene.csv`: immune checkpoint gene list
- Web portal (code + data): https://doi.org/10.5281/zenodo.8151927
- Raw scRNA-seq data: NGDC GSA-human HRA003672
- Processed combined gene expression matrix: NGDC OMIX002487

### Key Resources Table 주요 항목

| Category | Item | Source | Identifier |
|---|---|---|---|
| Antibody | FITC anti-human CD326 (EpCAM) | BioLegend | Cat# 324204; RRID AB_756078 |
| Antibody | APC/Cy7 anti-human CD45 | BioLegend | Cat# 304014; RRID AB_314402 |
| Assay | Chromium Single Cell 3' GEM Kit v3 | 10x Genomics | Cat# PN-1000075 |
| Assay | SPRIselect Reagent Kit | Beckman Coulter | Cat# B23318 |
| Software | Cell Ranger v3.0.0 | 10x Genomics | http://10xgenomics.com/ |
| Software | Seurat v4.0.1 | Seurat et al. | https://satijalab.org/seurat/ |
| Software | CopyKAT v1.0.5 | Gao et al. | https://github.com/navinlabcode/copykat |
| Software | CellPhoneDB v2.1.2 | Efremova et al. | https://www.cellphonedb.org/ |
| Equipment | BD FACSAria SORP Flow Cytometer | BD Biosciences | N/A |
| Equipment | CTC microfluidic chip | MerryHealth | http://merryhealthbio.com/product/ |

---

## 분석 자체에 대한 메모

1. **이전 분석(abstract 기반)과의 차이**: 이전 분석은 sources/abstract.txt (PMID 37659082)만 근거로 작성됨. 이번 재분석은 PDF 전문(26페이지) 기반. 방법 세부사항, Figure 내용, Troubleshooting, Tables가 모두 새로 포함됨.
2. **Capture efficiency 정량 부재**: Figure 1G에 CTC 시각 확인되나 cells/mL 또는 capture rate(%) 수치 미제공. 프로토콜 재현 시 자체 검증 필요.
3. **PPBP/PF4 CTC marker 문제**: 혈소판(platelet) marker인 PPBP, PF4가 CTC marker에 포함됨. CTC가 혈소판과 cluster를 이룰 수 있어 오분류 위험. 저자는 Problem 6에서 EMT 진행 CTC의 epithelial gene 발현 감소 + platelet 관련성을 언급하며 inferCNV 보완 제안. 재현 시 platelet marker 제거 후 재분석 권장.
4. **CellPhoneDB 버전 호환성**: v2.0 사용; v3/v4로 업그레이드 시 interaction weight score 계산 방식 변경 가능. GitHub 코드 확인 필요.
5. **암종 확장**: Table 1 CTC marker set이 PDAC 특이적. 다른 암종 적용 시 marker 교체 필요 (step 61 CRITICAL note).
6. **HPV 혈액 채취**: 간전이 수술 중 진행되는 침습적 채취. 수술 기회가 없는 환자 또는 간전이 미동반 환자에는 적용 불가.
