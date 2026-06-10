# montero-2022-adc-case-studies — Core Analysis

## Executive Summary

- **무엇**: 췌장 ductal adenocarcinoma (PDAC) 혈행 전이 과정에서 CTCs (circulating tumor cells)가 NK cell 면역 감시를 어떻게 회피하는지 single-cell 수준에서 규명하고, 핵심 immune checkpoint 분자쌍 HLA-E:CD94-NKG2A를 타깃으로 한 전이 억제 전략을 제시한 논문.
- **모델 / 방법**: 6명 PDAC 간전이 환자에서 원발암·간전이·간문맥(HPV) 혈액을 동시 수집 → 10x Genomics scRNA-seq (74,206 cells) + 마이크로유체 칩 CTC 단일세포 분리 → CellPhoneDB 세포간 상호작용 분석 → in vitro LDH assay + in vivo bioluminescence 전이 모델 기능 검증.
- **핵심 결과**:
  - ① 523개 CTC single-cell 프로파일링; CTC는 혈소판 관련 유전자(PPBP, PF4, RGS18)를 특이적으로 과발현하며 독립 cluster 형성.
  - ② CellPhoneDB 분석에서 HLA-E:CD94-NKG2A가 혈행 환경 특이적 CTC-NK cell 최대 inhibitory checkpoint pair로 식별됨 (solid tumor에서는 약함).
  - ③ In vitro: HLA-E 과발현 → NK cell killing 억제; monalizumab (anti-NKG2A) 처치 또는 shHLA-E 발현 → NK 세포독성 회복 (LDH assay, ** p < 0.01, t-test, n = 3 반복).
  - ④ In vivo 폐전이 모델: anti-NKG2A day −1 처치 → lung metastasis 63배 감소; H2-T23(HLA-E homolog) knockdown → 115배 감소 (p < 0.001, t-test, n = 5/group, Kaplan-Meier p = 3e−4).
  - ⑤ 기전: 혈소판 내재화(internalization)로 획득한 platelet-derived RGS18이 AKT-GSK3β-CREB1 signaling axis를 통해 HLA-E 발현 상향 조절.
- **우리 적용**: HLA-E는 CTC surface protein으로 ADC 타깃 후보 논의 시 academic-citation 근거; NK cell 기반 liquid biopsy + immunotherapy 병용 전략 설계 참고. `academic-citation` / `BD-opportunity` use case.
- **심층**: 한계·재현 ROI는 `montero-2022-adc-case-studies_lens-academic.md` / `montero-2022-adc-case-studies_lens-industry.md` / `montero-2022-adc-case-studies_methodology-brief.md` 참고.

---

## Identity

- **Title**: Immune checkpoint HLA-E:CD94-NKG2A mediates evasion of circulating tumor cells from NK cell surveillance
- **Authors**: Xiaowei Liu, Jinen Song, Hao Zhang, Xinyu Liu, Fengli Zuo, Yunuo Zhao, Yujie Zhao, Xiaomeng Yin, Xinyu Guo, Xi Wu, Hu Zhang, Jie Xu, Jianping Hu, Jing Jing, Xuelei Ma, Hubing Shi
- **Corresponding authors**: Xuelei Ma (drmaxuelei@gmail.com), Hubing Shi (shihb@scu.edu.cn)
- **First author**: Xiaowei Liu — 논문 표기 "Liu et al., 2023"
- **Year**: 2023 (published online 2023-01-26, print 2023-02-13) — paper-info.yaml의 year: 2022는 오기재
- **Venue**: Cancer Cell, Volume 41, pp. 272–287.e9
- **DOI**: 10.1016/j.ccell.2023.01.001
- **PMID**: 36706761
- **Citation key**: liu2023hlae
- **Affiliation 주저자**: West China Hospital, Sichuan University, Chengdu, China
- **Funding**: National Key R&D Program of China (2022YFC2504703, 2022YFC2504700), NSFC (82172634, 22105137, 81902685), Key Program of Science and Technology Bureau of Sichuan, China Postdoctoral Science Foundation, West China Hospital (ZYYC20013)
- **COI**: 저자 모두 competing interests 없음 선언

---

## Background

### 배경 스토리

- **문제의 출발점**: Immune checkpoint blockade (ICB) 요법이 여러 암종에서 효과적이지만, 그 대부분은 고형 종양 내 T cell 기반 면역 감시 복원에 집중되어 있다. 혈행을 통해 이동 중인 CTC가 면역 감시를 어떻게 피하는지는 거의 알려지지 않았다.
- **선행 접근 A — PD-1:PD-L1 / CTLA-4 기반 ICB**: T cell 중심 checkpoint는 흑색종·NSCLC 등에서 durable response를 보였다. 그러나 PDAC는 anti-PD-1 단독 임상 (NCT02459301 등)에서 지속적으로 실패했으며, 본 논문의 scRNA-seq 데이터에서도 CD274 (PD-L1) 발현이 CTCs 및 혈행 biopsy에서 낮고 PD-1:PD-L1 상호작용이 CTC-immune cell 쌍에서 관찰되지 않음.
- **A의 한계**: 혈행을 통해 이동 중인 CTC와 NK cell 사이의 interaction을 T cell 중심 ICB는 다루지 않는다.
- **선행 접근 B — NK cell 관찰 연구**: CTC 수와 cytotoxic immunocyte(NK cell, T cell, monocyte) 수 사이의 임상적 음의 상관이 관찰된 바 있으나, 어떤 immune cell이 핵심이고 어떤 inhibitory molecular pair가 이를 suppressive하게 만드는지 single-cell 수준에서 직접 규명한 연구는 없었다.
- **B의 한계**: Solid tumor microenvironment 분석 데이터를 혈행 CTC 환경에 적용할 수 없으며, CTC 특이적 immune checkpoint pair를 직접 식별한 연구 부재.
- **이 논문으로 이어지는 gap**: CTC가 혈행에서 (1) 어떤 면역 세포의 감시를 받는지, (2) 어떤 checkpoint pair로 회피하는지, (3) 그 분자적 upstream이 무엇인지 — 세 가지를 동시에 규명하는 연구가 없었다.

### 기본 개념

- **CTC (Circulating Tumor Cells, 순환 종양 세포)**: 원발 병소에서 방출되어 혈관 내를 순환하는 종양 세포. PDAC의 간전이는 주로 간문맥(hepatic portal vein, HPV)을 통한 CTC 전파로 이루어짐.
- **HLA-E**: MHC class Ib 분자. signal peptide sequence를 표면에 제시하여 NK cell의 inhibitory receptor CD94-NKG2A의 ligand로 작용. HLA-E:CD94-NKG2A 결합 시 NK cell 내 SHP-1 (tyrosine phosphatase)이 활성화되어 세포독성 억제.
- **NKG2A (KLRC1) vs NKG2C (KLRC2)**: CD94와 heterodimer를 형성하는 C-type lectin receptor. NKG2A는 inhibitory (ITAM motif 없음, SHP-1 연결), NKG2C는 activating. NKG2A가 존재하면 NKG2C의 activating 기능이 silenced.
- **RGS18 (Regulator of G-protein Signaling 18)**: 원래 megakaryocyte/platelet에서 고발현. G-protein signaling을 통해 GPCR downstream을 조절. CTC가 혈소판을 내재화하여 platelet-derived RGS18을 획득하면 AKT-GSK3β-CREB1 axis를 통해 HLA-E 발현 상향 조절됨.

### 이 논문의 필요성

- **핵심 이유**: PDAC는 5년 생존율 약 8%로 예후 극히 불량; 간전이가 주요 사망 원인. 혈행 CTC 제거 전략이 전이 예방의 새로운 접근이 될 수 있음.
- **기존 방법으로 부족했던 지점**: 혈행이라는 독특한 면역 환경(혈소판 존재, NK cell 비율 특이성)에서 CTC 면역 회피를 분석한 single-cell 연구 부재.
- **이 논문이 해결하려는 방향**: scRNA-seq + microfluidic CTC 분리 + in vivo 마우스 모델로 HLA-E:CD94-NKG2A를 혈행 CTC 특이적 immune checkpoint로 규명하고, 이 checkpoint 봉쇄의 전이 억제 효과 입증.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: PDAC 환자 단일세포 전사체 데이터로 CTC-NK cell 상호작용의 핵심 inhibitory checkpoint pair를 도출하고, 기능 실험으로 인과 관계 검증.
- **입력**: HPV 혈액 + 원발/전이 종양 생검에서 분리한 단일 세포 (74,206 cells, 18 samples).
- **출력**: CTC 분류 및 transcriptional signature, 세포간 상호작용 network, HLA-E 조절 pathway, in vivo 전이 억제 효능.
- **추정 대상**: 혈행 환경 특이적 ligand-receptor pair (CellPhoneDB empirical shuffling 기반).
- **중요한 hidden assumption**: EpCAM+/CD45− 세포 = CTC로 정의. scRNA-seq에서 PTPRC−/PPBP+ marker로 재확인. CopyKAT (v1.0.5) integrative Bayesian approach로 malignant cell CNV 확인.

### 확률 / 통계학적 구조

- **Cell type annotation**: Seurat (v4.0.1). LogNormalize → PCA 50 components → Louvain clustering (resolution 1.0) → t-SNE (PC parameter 50). scBet (v1.0)으로 주석. CopyKAT으로 CNV 기반 malignancy.
- **Differential expression**: FindMarkers (Wilcoxon rank-sum test). min.pct = 0.25, logfc.threshold = 0.25. Adjusted p-value 사용 (p.adj < 0.05 기준).
- **Cell-cell communication**: CellPhoneDB (v2.0). Empirical shuffling으로 p-value 산출. 유의 기준: p < 0.05 & mean expression (Molecule 1, Molecule 2) > 0.5.
- **Gene set enrichment**: SingleCellSignatureExplorer (v3.6) + limma (v3.42.0). HALLMARK/C2.CP.KEGG/C2.CP.REACTOME/C5.BP (MSigDB v7.1).
- **In vivo 통계**: two-sample t-test (LDH assay, bioluminescence intensity, nodule count), log-rank test (Kaplan-Meier). Statistical thresholds: *p < 0.05; **p < 0.01; ***p < 0.001; ****p < 0.0001.

### 핵심 method insight

- **기존 방법의 한계**: CTC 분석의 대부분은 bulk RNA-seq 또는 단순 marker 기반이었으며, 혈행 내 CTC와 면역 세포의 상호작용을 single-cell 수준에서 profiling하는 것이 불가능했다.
- **이 논문이 바꾼 가정**: HPV 혈액을 고형 종양과 동등한 조직으로 취급하여 혈행 환경 내 CTC + 면역 세포를 동시 scRNA-seq. 이를 통해 혈행 특이적 immune checkpoint를 고형 병소와 직접 비교.
- **새로 추가한 구조**: Microfluidic chip 기반 CTC 포획 (EpCAM/CA19-9 antibody coating, PDMS two-layer structure) — flow cytometry FACS 대비 세포 생존율 보호 성능 우수 (Figure S2F).
- **이 변화가 중요한 이유**: 고형 병소에서는 PD-L1:PD-1이 주요 checkpoint로 부각되지만, 혈행에서는 PD-L1 발현이 낮고 HLA-E:NKG2A가 지배적임을 단일 연구에서 처음으로 직접 비교 제시.

### 이전 방법과의 차이

- **Baseline**: 기존 CTC 연구 — bulk RNA-seq (PDAC: GSE144561; BRCA: GSE67939, GSE86978; COAD: GSE74369; HCC: GSE117623; SKCM: GSE38495; mouse PDAC: GSE51372).
- **공통점**: EpCAM 기반 CTC identification, DEG analysis, gene set enrichment.
- **차이점**: HPV 혈액에서 직접 single-cell profiling. 18 samples (primary + HPV + metastasis) 동시 통합. CellPhoneDB로 CTC-immune cell 상호작용 network 구성. In vitro LDH assay + in vivo bioluminescence 이중 검증.
- **차이가 크게 나타나는 조건**: 혈행 환경 특이적 checkpoint (HLA-E:NKG2A) — solid tumor에서 HLA-E 발현이 CTCs보다 낮음.

### 효과가 Results에서 나타난 방식

- In vivo lung metastasis: NKG2A 봉쇄 day −1 → 63배 감소, H2-T23 knockdown → 115배 감소 (Figure 3E, 3G–K, *** p < 0.001).
- In vivo liver metastasis: RGS18 과발현 → 간전이 증가 (p = 0.00079, Kaplan-Meier, Figure 5F); NKG2A 봉쇄로 역전.
- In vitro: HLA-E 과발현 시 NK cell killing 감소; monalizumab 처치 시 회복 (Figure 3A).

### Method 관점의 한계

- CTC 수가 작아 (총 523 cells, 6 patients) 환자별 통계 분석 통계력 제한.
- CellPhoneDB는 RNA 발현 proxy; 단백질 수준 결합 친화도(KD) 데이터 없음.
- In vivo 모델: Balb/c nude (T cell 없음) 또는 C57BL/6 (immunocompetent, KPC syngeneic). 인간 면역 시스템 완전 재현 불가.
- RGS18 mRNA vs 단백질 직접 전달 경로 구분 — qPCR 결과는 human RGS18 mRNA 증가를 시사하나, 완전한 내재화 기전 규명은 향후 과제로 남음.

---

## Results

### Dataset별 결과

#### Dataset 1 — PDAC 환자 scRNA-seq (6 patients, 18 samples)

- **Dataset**: 6명 치료 naive PDAC 간전이 환자. Primary pancreatic tumor + HPV blood + liver metastasis tumor 동시 수집. 10x Genomics Chromium 3' Gene Expression Kit V3. Illumina HiSeq 4000 (target depth: 100,000 reads/cell).
- **사용한 데이터 규모**: QC 후 74,206 single cells, 26,808 features (18 samples). Primary 27,296 cells, HPV blood 9,988 cells, metastasis 36,922 cells.
- **세포 분류 결과**: 8개 major cell type — 29,930 epithelial (EPCAM+, KRT8+), 1,675 fibroblasts (FAP+, COL1A1+), 875 endothelial (VWF+, PECAM1+), 523 CTCs (PTPRC−, PPBP+), 19,072 myeloid (CD14+, LYZ+, FPR1+, AIF1+), 1,448 B cells (CD79A+, CD19+), 2,485 NK cells (KLRF1+, KLRD1+), 18,198 T cells (CD3D+, CD3G+). Immunocyte re-clustering으로 16 subtypes 식별 (NK, NK-T, CD8 Ex, CD8 EFF, Memory T, Naive T, Treg, B cell, Neutrophil, Monocyte, M1 Macro, M2 Macro, cDC, pDC, Mast cell — Figure S6).
- **CTC 특이 signature**: Top 100 upregulated DEGs 중 32개가 131개 platelet marker gene과 overlap (Venn plot, Figure S4I). Platelet markers (PPBP, PF4, GP9, ITGA2B), GPCR family (RGS18, NRGN, CCL5, GNG11), EMT drivers (TGFB1, SRGN, SPARC, SH3BGRL3) 과발현; epithelial markers (CDH1, KRT8, KRT18, KRT19) 하향 (Figure 1D, S4J).
- **논문 주장과의 연결**: CTC의 platelet signature는 platelet internalization 기반 RGS18 획득 가설로 이어지며, immune-related signature 상향은 NK cell과의 상호작용을 지시.

#### Dataset 2 — CTC-immune cell 상호작용 분석 (CellPhoneDB)

- **Dataset**: 위 scRNA-seq dataset에 CellPhoneDB (v2.0) 적용. Primary, HPV blood, metastasis 구획 각각.
- **주요 수치**: HLA-E:CD94-NKG2A 분자쌍이 HPV blood의 CTC-NK cell interaction에서 가장 강하게 식별됨 (Figure 2G). HLA-E 발현이 CTCs에서 primary/metastatic tumor cells보다 유의하게 높음 (Figure 2H, 2J, Wilcoxon test, p < 0.0001). 7개 공개 CTC dataset 모두에서 CTC > tumor cells HLA-E 발현 확인 (PDAC, HCC, BRCA, COAD, SKCM, mouse PDAC CTC). NKG2A (KLRC1) 발현이 HPV blood NK cell에서 우세; NKG2A+/NKG2C− NK가 majority (Figure 2K, p < 0.0001).
- **PD-L1 부재**: CD274:PDCD1 (PD-L1:PD-1) interaction이 CTC-immune cell 쌍에서 관찰되지 않음. PD-L1 발현이 CXCL9/10/11 (T cell homing chemokine) 발현과 함께 CTC에서 낮음 (Figure S7D, E) — anti-PD-1 단독 임상 실패의 생물학적 설명.
- **논문 주장과의 연결**: 혈행 환경에서 NK cell이 CTC 감시의 주역이며, HLA-E:CD94-NKG2A가 이를 억제하는 주요 checkpoint.

#### Dataset 3 — In vitro 기능 검증 (LDH assay)

- **Dataset**: SU86.86 PDAC cell line ± HLA-E 과발현/knockdown + patient-derived NK cells. LDH-GloTM Cytotoxicity Detection Kit (Promega, J2381). E:T ratio 10:1, 5:1. ± monalizumab (anti-NKG2A, 100 μg/mL).
- **주요 수치**: HLA-E 과발현 시 10:1 E:T ratio에서 NK cell killing % 약 40–60% → 약 20–30%로 감소 (mean ± SD, * p < 0.05, ** p < 0.01, t-test, n = 3 반복). shHLA-E → killing 증가. Monalizumab 처치 → HLA-E 과발현의 inhibitory 효과 부분 역전 (** p < 0.01, Figure 3A).
- **Western blot**: HLA-E 과발현 조건에서 SHP-1 phosphorylation 증가, GZMB (granzyme B) 하향 (Figure 3B) — HLA-E:NKG2A signaling 경로 확인.
- **논문 주장과의 연결**: HLA-E:CD94-NKG2A 상호작용이 SHP-1을 통해 NK cell 세포독성을 기능적으로 억제함.

#### Dataset 4 — In vivo 폐전이 모델 (anti-NKG2A timing 실험)

- **Dataset**: KPC-Luc cells (luciferase-tagged mouse PDAC, 5×10^4 cells), tail vein i.v. injection. Balb/c nude mice. Anti-NKG2A antibody (BioXcell, #BE0321) 4 doses (10 mg/kg i.v.), timing: day −1, 0, 1, 3, 또는 5. H2-T23 knockdown KPC-Luc cells 비교. n = 5/group. IVIS Spectrum day 15.
- **주요 수치**: NKG2A 봉쇄 day −1 처치 → fluorescent intensity 63배 감소 (p < 0.001), lung nodule count 유의 감소 (Figure 3E, 3G). H2-T23 knockdown → 115배 감소 (p < 0.001, Figure 3J, K). Kaplan-Meier (n = 5/group): anti-NKG2A 및 shH2-T23 모두 생존 유의 연장, p = 3e−4 (Figure 3O, log-rank test).
- **Timing 의존성**: Day −1, 0 처치에서만 유의미한 전이 억제; day 3, 5 이후에는 효과 없음 — HLA-E:CD94-NKG2A checkpoint가 혈행 CTC 단계에 한정된 작용 window를 가짐.
- **Subcutaneous 대조 실험**: 같은 처치가 피하 종양 성장에는 영향 없음 (Figures S9K–N) → 혈행 특이적 기전 확인.
- **C57BL/6 immunocompetent 검증**: KPC-Luc cells, anti-NKG2A 또는 H2-T23 knockdown → lung metastasis 유의 감소 (Figure 3N, Kaplan-Meier p = 3e−4, n = 5). 해석: T cell이 있는 immunocompetent system에서도 HLA-E:NKG2A 억제 효과 재현됨.

#### Dataset 5 — In vivo 간전이 모델 (RGS18 기전 검증)

- **Dataset**: SU86.86-Luc cells ± hRGS18 overexpression, hemi-splenic injection. Balb/c nude mice. n = 5–6. IVIS imaging day 14. 추가: mRGS18 KPC-Luc + anti-NKG2A (days −1, 0, 1, 2) rescue experiment.
- **주요 수치**: RGS18 과발현 → 간전이 형광 intensity 유의 증가 (p < 0.001, Figure 5C). Kaplan-Meier: Vector vs hRGS18, p = 0.00079, n = 6/group (Figure 5F). NKG2A 봉쇄 → RGS18 유도 전이 억제 (Figure 5G–K, p < 0.001).
- **NK cell 의존성 확인**: B-NDG hIL15 mice (NK cell 없음, human NK 미이식) — hRGS18 과발현 효과 없음 (Figure S11D, E, p > 0.05) → RGS18의 pro-metastasis 기능이 NK cell 의존적임 입증.
- **Human NK + B-NDG rescue**: hIL15 B-NDG mice에 human NK 이식 후 hRGS18 과발현 SU86.86 → 간전이 유의 증가; HLA-E knockdown으로 역전 (Figure S11F, G, p < 0.001).

#### Dataset 6 — RGS18→AKT-GSK3β-CREB1→HLA-E axis (기전 실험)

- **Dataset**: SU86.86, CFPAC-1, CAPAN-1 cell lines. RGS18 과발현/knockdown, CREB1 knockdown, AKT mutants (AKT^Q79K active, AKT^E17K inactive). Western blot, IHC, IF.
- **주요 수치**: RGS18 과발현 → p-AKT(S473)↑, p-GSK3β(S9)↑ (GSK3β 비활성화), p-CREB(Ser133)↑, HLA-E 단백질↑ (Figure 4D). shRGS18 → 반대 방향 (Figure 4D right). shCREB1 → HLA-E 감소 (Figure 4F). AKT^Q79K (active) → HLA-E 증가; AKT^E17K (inactive) → HLA-E 감소 (Figure 4G). 독립 코호트 (n = 13 PDAC): EpCAM+RGS18+ CTC가 모든 환자에서 95–100% 비율 (Figure S10E).
- **혈소판 내재화**: CTC가 PDAC 환자 혈소판(WGA-Alexa594 labeling)을 internalize함을 confocal microscopy + flow cytometry로 확인 (Figure 6B, C). Human platelet 처치 → human RGS18 mRNA 용량 의존적 증가 (KPC cells; mouse Rgs18는 증가 안 함, Figure 6D). HLA-E, RGS18, CD41 단백질 용량 의존적 증가 (Western blot, 0.75–3×10^6 platelets/mL, Figure 6E).

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: HLA-E 과발현이 6명 환자 scRNA-seq, 13명 환자 IHC cohort, 7개 공개 CTC dataset에서 일관되게 확인. NKG2A 봉쇄 또는 HLA-E knockdown이 in vitro/in vivo 모두에서 일관되게 NK 세포독성 회복 및 전이 감소로 이어짐.
- **가장 중요한 수치**: In vivo lung metastasis 63배 (NKG2A 봉쇄) / 115배 (H2-T23 knockdown) 감소. 간전이 모델 생존 p = 0.00079.
- **Baseline 대비 차이**: Solid tumor 대비 혈행 환경에서 HLA-E:NKG2A interaction dominant; solid tumor에서 HLA-E 발현이 CTCs보다 낮음 → 항체 효과 창구(window)는 혈행 CTC 단계에 한정.
- **결과 해석 시 주의점**: Anti-NKG2A 투여 시점이 혈행 CTC 단계를 벗어나면 효과 없음. 6명 PDAC 환자가 단일 기관(West China Hospital), 단일 인종(중국) 코호트 — 일반화 제한.

---

## Figures

### Figure 1 — Transcriptomic characterization of PDAC primary tumors, metastatic lesions, and CTCs at single-cell scale

#### 패널별 설명
- **1A**: 실험 overview — 6 PDAC patients, 18 samples, 10x Genomics scRNA-seq 74,206 cells. FACS sorting + microfluidic chip CTC capture 흐름.
- **1B**: 전체 74,206 cells t-SNE (cell type별 색상). 8 major cell types 시각화.
- **1C**: Tissue origin별 t-SNE (primary 27,296 / blood 9,988 / metastasis 36,922 cells).
- **1D**: Primary tumor vs CTC vs Metastasis tumor top/bottom 30 DEGs heatmap (Z-score). Platelet (purple), GPCR (yellow), EMT (red), epithelial (green), ribosome (navy) 하이라이트.
- **1E**: GSEA signature heatmap by geneset category (Immune, Platelet, Oncogene, EMT, Biosynthetic, Apoptosis, Metabolism, Cell cycle) — CTC vs Primary/Metastasis 비교.

#### 본문에서 강조한 비교
- CTC: platelet 및 immune-related signature 상향, ribosome/biosynthesis 하향 (vs primary/metastasis).
- 32/100 CTC upregulated genes가 platelet marker gene과 overlap.

#### 해석 시 주의점
- CTC 수 523 cells (6 patients); CTC 특이 발현이 platelet internalization artifact인지 실제 고유 발현인지의 완전한 구분은 이 논문에서 다루어지지 않음. Microfluidic chip 이전 RBC lysis + washing 절차를 거쳤으나 혈소판 contamination 완전 제거 여부는 명시 없음.

### Figure 2 — Tumor-immune cellular interaction in HPV blood, primary, and metastatic tumors

#### 패널별 설명
- **2A–B**: 39,729 immunocytes t-SNE (16 subtypes, tissue origin).
- **2C**: 16 subtypes marker gene heatmap.
- **2D–F**: CellPhoneDB 결과 — primary, blood, metastasis 구획 immune checkpoint interaction network (interaction weight scores).
- **2G**: Immune checkpoint pair bubble plot (primary, CTC, metastasis 구획). HLA-E:KLRC1/2가 blood-CTC-NK에서 최상위.
- **2H**: HLA-E 발현 boxplot — CTC > primary = metastasis (p < 0.0001, Wilcoxon).
- **2I**: H2-T23 (mouse HLA-E) 발현 boxplot.
- **2J**: 7개 공개 dataset에서 HLA-E 발현 bar plot (CTC vs tumor cells, *** p < 0.001, **** p < 0.0001).
- **2K**: CD94 (KLRD1) 및 NKG2A (KLRC1) 발현 bar plot in immunocytes from HPV blood (*** p < 0.001).
- **2L**: Multiplex IF — HPV blood에서 CTC (EpCAM, green)와 NK cell (CD94, red)의 물리적 접촉 확인.

#### 본문에서 강조한 비교
- HLA-E:CD94-NKG2A가 forward/backward 모두 CTC-NK 최대 interaction. PD-L1:PD-1은 혈행 CTC-immune cell 상호작용에서 관찰 안 됨.

#### 해석 시 주의점
- CellPhoneDB p-value는 empirical shuffling 기반 추정; 단백질 수준 결합 확인은 IF (2L)에서 공간적 co-localization으로만 제시. 정량적 결합 친화도 없음.

### Figure 3 — Functional validations of immune checkpoint HLA-E:CD94-NKG2A in vitro and in vivo

#### 패널별 설명
- **3A**: LDH assay — NK cell killing % by E:T ratio (10:1, 5:1). Vector/HLA-E/HLA-E+Monalizumab/shHLA-E. Mean ± SD, n = 3, * p < 0.05, ** p < 0.01.
- **3B**: Western blot — GZMB (granzyme B, 상향), p-SHP1 (상향), T-SHP1.
- **3C**: 실험 design schema — anti-NKG2A timing (day −1, 0, 1, 3, 5).
- **3D, E**: IVIS bioluminescence images (day 15) + fluorescent intensity boxplot (n = 5, *** p < 0.001).
- **3F–H**: Lung photographs + nodule count + H&E histology.
- **3I–M**: shH2-T23 실험군 IVIS + nodule count + photographs + H&E.
- **3N, O**: C57BL/6 immunocompetent mice IVIS + Kaplan-Meier (p = 3e−4, n = 5, log-rank).

#### 본문에서 강조한 비교
- Day −1 anti-NKG2A vs day 3 이상: 전자에서만 전이 억제 — 작용 window가 혈행 CTC 단계에 한정됨.
- Subcutaneous 종양 성장에 anti-NKG2A 영향 없음 → 혈행 특이성 입증 (Figure S9).

#### 해석 시 주의점
- Balb/c nude 모델 (T cell 없음); C57BL/6 immunocompetent 모델로 보완했으나, 실제 PDAC 환자의 혼합 면역 환경을 완전히 반영하지 못함.

### Figure 4 — RGS18 promotes the expression of HLA-E on CTCs via the AKT-GSK3β-CREB1 axis

#### 패널별 설명
- **4A**: 3D scatter plot — scRNA-seq 기반 HLA-E 발현과 correlated DEGs. PPBP, PF4, NRGN, RGS18 상위 (upper right quadrant).
- **4B**: Western blot — PPBP/PF4/NRGN/RGS18 과발현 시 HLA-E (SU86.86, CFPAC-1). RGS18 효과 최강.
- **4C**: Multiplex IF — 6 patients biopsies에서 RGS18이 EpCAM+ CTC에서 특이 발현.
- **4D**: Western blot cascade — RGS18 OE → p-AKT↑, p-GSK3β(Ser9)↑, p-CREB↑, HLA-E↑; shRGS18 → 반대.
- **4E**: IF — RGS18 OE → nuclear p-CREB (Ser133) 증가 (SU86.86, CFPAC-1).
- **4F**: Western blot — shCREB1 (3 constructs) → HLA-E 감소 (SU86.86, CFPAC-1).
- **4G**: Western blot — AKT^Q79K (active) → HLA-E 증가; AKT^E17K (inactive) → HLA-E 감소.

#### 해석 시 주의점
- 모든 기전 데이터는 cell line 기반. Primary CTC에서 동일 pathway의 단백질 수준 활성화는 IF (4C: RGS18 발현)와 독립 코호트 scRNA-seq (Figure S10)로 간접 확인에 그침.

### Figure 5 — RGS18 promotes the liver metastasis of PDAC tumor cells

#### 패널별 설명
- **5A**: 간전이 모델 schema (hemi-splenic injection → portal vein → liver metastasis).
- **5B, C**: SU86.86-Luc ± hRGS18 IVIS images + bioluminescence intensity quantification (p < 0.001, n = 5).
- **5D**: Liver photographs (dissected).
- **5E**: H&E + IHC (hEpCAM, hRGS18 staining).
- **5F**: Kaplan-Meier (Vector vs hRGS18, p = 0.00079, n = 6, log-rank).
- **5G–K**: mRGS18 KPC-Luc + anti-NKG2A rescue — IVIS, bioluminescence quantification, liver photographs, H&E (anti-NKG2A → mRGS18 유도 전이 억제).

#### 본문에서 강조한 비교
- RGS18 과발현 + NK 세포독성: 둘이 함께 작용해야 전이 촉진 → NKG2A 봉쇄로 역전 가능.

### Figure 6 — CTCs obtain RGS18 by internalization of platelets

#### 패널별 설명
- **6A**: CTC co-staining (EpCAM/CD41/Hoechst) — 혈소판이 CTC 표면/내부 존재 확인.
- **6B**: Confocal — SU86.86/CFPAC-1에 WGA-Alexa594 prelabeled PDAC patient platelets 처치 후 internalization 확인.
- **6C**: Flow cytometry — platelet internalization 용량 의존적 (0 → 35.4% at 3×10^6 platelets/mL, SU86.86).
- **6D**: qPCR — human RGS18 mRNA 용량 의존적 증가 (KPC + human platelets); mouse Rgs18 불변 → human mRNA 전달 시사.
- **6E**: Western blot — HLA-E, RGS18, CD41 단백질 용량 의존적 증가 (0.75–3×10^6 platelets/mL, SU86.86 + CFPAC-1).

#### 해석 시 주의점
- Platelet internalization이 human RGS18 mRNA transcription을 유도하는 경로 vs 단백질 직접 전달 경로: qPCR 데이터는 전자를 시사하지만 완전한 기전 (어떤 platelet-derived factor가 어떤 경로로 RGS18 transcription을 trigger하는지)은 미규명.

### Figure 7 — Schema of HLA-E:CD94-NKG2A-mediated evasion

#### 패널별 설명
- Summary 모식도: CTC 혈관 intravasate → 혈소판 internalize → RGS18 획득 → AKT 활성화 억제(Ser473↑) → GSK3β 억제(Ser9↑) → CREB1 활성화(Ser133↑) → HLA-E promoter 결합 → HLA-E 표면 발현↑ → CD94-NKG2A 결합 → SHP-1↑ → NK 세포독성(cytokine/granzyme)↓ → 전이 촉진.

---

## Tables

### Table S1 — scRNA-Seq cohort of PDAC patients (n=6)

| 항목 | P1 | P2 | P3 | P4 | P5 | P6 |
|---|---|---|---|---|---|---|
| Tumor stage | cT4N+M IV | cT3N+M IV | cT3N+M IV | cT4N+M1 IV | cT2N+M1 IV | cT3N+M1 IV |
| Liver metastasis | Y | Y | Y | Y | Y | Y |
| Prior treatment | N | N | N | N | N | N |
| Site | neck | head | head | tail | tail | tail |
| Age | 57 | 62 | 66 | 51 | 67 | 54 |
| Sex | M | M | M | F | M | F |
| CA19-9 (U/mL) | 735 | >1000 | 49.1 | 311 | >1000 | 600 |
| Genotype | KRAS, TP53 | KRAS | KRAS, TP53 | KRAS | KRAS, TP53 | KRAS |

모든 환자 stage IV (간전이 확인), 치료 naive.

### Tables S2–S4 (mmc3–5.xlsx)

- **Table S2**: DEG 및 통계 결과 (platelet marker gene overlap analysis).
- **Table S3**: CellPhoneDB 전체 immune checkpoint interaction pair 목록.
- **Table S4**: shRNA hairpin sequences + qPCR primers.

본문 정식 Table은 Table S1만 보충 PDF에 수록됨.

---

## Supplementary Information

### Supplementary Figures (mmc1.pdf / mmc6.pdf, S1–S11)

- **S1**: CT images, H&E, CNV chromosome plots, somatic mutation spectra, KRAS G12V/D hotspot. 전 환자 KRAS mutation (somatic mutation rate 100%).
- **S2**: CTC isolation microfluidic pipeline schema; FACS gating strategy; chip vs FACS efficiency comparison.
- **S3**: scRNA-seq cell type annotation t-SNE (tissue/patient origin); CopyKAT CNV; cell type proportion by tissue origin (barplot).
- **S4**: CTC transcriptional signature — CopyKAT heatmap, t-SNE of 30,453 epithelial+CTC, volcano plot (primary vs metastasis DEGs), correlation matrix, DEG heatmap (top 100 CTC upregulated), Venn plot, boxplots.
- **S5**: GO/KEGG/Reactome enrichment network (ClueGO, CTC upregulated = immune/platelet/oncogene/EMT/apoptosis/metabolism/cell cycle; downregulated = biosynthesis/RNA).
- **S6**: NK cell 16 subtype t-SNE; volcano plots (primary NK / HPV NK / metastasis NK); pathway heatmap; DEG heatmap.
- **S7**: CTC-immunocyte interaction chord diagrams + bubble plots. PD-L1/chemokine receptor 발현 확인 (PD-L1 low in CTCs).
- **S8**: NKG2A/NKG2C density plots + violin plots; co-staining IF; in vivo cell-cell contact enrichment assay; HLA-E overexpression fluorescence + NK ratio quantification.
- **S9**: HLA-E KD/OE western blot; NKG2A/NKG2C flow cytometry (8 PDAC patients, n = 8, *** p < 0.001); KPC lung metastasis models; subcutaneous xenograft (NKG2A 봉쇄 효과 없음).
- **S10**: Violin plots (PPBP, PF4, NRGN, RGS18); RGS18 IF biopsies; RGS18 violin (CTCs vs primary/metastasis, **** p < 0.0001); independent cohort (n = 13) EpCAM+RGS18+ CTC barplot; kinase signaling western blots.
- **S11**: NK depletion vs mRGS18 liver metastasis; B-NDG hIL15 NK-independence test; human NK + B-NDG hIL15 rescue; lung metastasis model schema; KPC platelet internalization.

---

## 분석 자체에 대한 메모

- **paper-id 불일치**: folder 이름 `montero-2022-adc-case-studies` 및 paper-info.yaml의 `authors_short: Montero, A.J. et al.`은 실제 논문(first author: Xiaowei Liu, 2023)과 불일치. Folder rename 없이 분석 파일 내 실제 저자/연도 표기 유지.
- **year 오기재**: paper-info.yaml에 `year: 2022`이지만 실제 출판 2023년. DOI는 정확함.
- **검토필요**: HLA-E를 ADC 타깃으로 고려할 경우 (1) 정상 세포(NK cell, T cell 등)의 HLA-E 발현 수준과 독성 창구, (2) solid tumor 대비 CTC에서만 높은 발현이 ADC delivery 관점에서 어떻게 극복될 수 있는지 추가 검토 필요.
- **질문**: 6명 단일 기관(West China Hospital, 중국) 코호트 — 다른 인종/기관에서의 HLA-E 과발현 CTC 패턴 재현성 검증 필요.
