# nami-2021-her2-emt-silencing — Core Analysis

## Executive Summary

- **무엇**: EMT(상피-간엽 전환) 과정에서 ERBB2 유전자 chromatin이 epigenetic 리모델링에 의해 silencing되고, 이것이 trastuzumab·lapatinib 내성의 핵심 기전임을 공개 genomics 데이터 + BT474 세포 실험으로 제시한 기전 연구.
- **모델 / 방법**: 공개 데이터(METABRIC n=1904 종양, GEO ChIP-seq/ATAC-seq/expression arrays) + BT474 세포주에서 직접 EMT 유도 → ERBB2 발현·chromatin 상태·trastuzumab binding을 상관·비교 분석. 통계: two-tailed Student's t-test + ANOVA, $p < 0.050$ 유의 기준.
- **핵심 결과**:
  - ① METABRIC 1904 유방암 종양 — ERBB2 발현과 상피 마커(12종) 정(+) 상관, 간엽 마커(12종) 부(-) 상관 (모두 $p < 0.0001$).
  - ② HER2-high vs. HER2-low cell lines(n=5 vs. n=3) — active histone marks(H3K4me2, H3K4me3, H3K9ac, H3K27ac, H4K8ac) ERBB2 chromatin에서 HER2-high에 풍부; inactive marks(H3K9me, H3K27me3)는 양군 모두 낮아 "activator 부재"가 silencing 기전.
  - ③ Promoter-enhancer loop: HCC-1954(HER2-high) 240개, MCF7(HER2-low) 11개.
  - ④ BT474 EMT 유도(15일) — 간엽 표현형 전환 + trastuzumab binding 감소(immunofluorescence; 정량 수치 미제공).
  - ⑤ A549 TGF-β1 72 h 처리 — ERBB2 mRNA 유의 감소($p < 0.05$~$p < 0.0001$).
- **우리 적용**: HER2 ADC 개발·CTC liquid biopsy 맥락에서, EMT 상태 tumor/CTC의 ERBB2 epigenetic silencing이 HER2 ADC 내성·표적 소실 기전으로 작용함을 지지하는 background reference. `academic-citation` + `BD-opportunity`.
- **심층**: 한계·재현 ROI는 `nami-2021-her2-emt-silencing_lens-academic.md` / `nami-2021-her2-emt-silencing_lens-industry.md` / `nami-2021-her2-emt-silencing_methodology-brief.md` 참고.

---

## Identity

- **Title**: Epigenetic Silencing of HER2 Expression during Epithelial-Mesenchymal Transition Leads to Trastuzumab Resistance in Breast Cancer
- **Authors**: Babak Nami, Avrin Ghanaeian, Corbin Black, Zhixiang Wang
- **Year**: 2021
- **Venue**: *Life* (Basel), 11(9), 868
- **DOI**: 10.3390/life11090868
- **Citation key**: nami2021her2emt
- **Affiliations**: Signal Transduction Research Group, Department of Medical Genetics, Faculty of Medicine and Dentistry, University of Alberta, Edmonton, Canada (Nami, Wang); Department of Anatomy and Cell Biology, Faculty of Medicine and Health Sciences, McGill University, Montréal, Canada (Ghanaeian, Black)
- **Received / Accepted / Published**: 25 July 2021 / 14 August 2021 / 24 August 2021
- **Funding**: CIHR to Z.W.; WCHRI Graduate Studentship (B.N.). "No specific funding was received for this study."
- **COI**: "The authors declare no conflict of interest."
- **License**: CC BY 4.0 (open access, MDPI)

---

## Background

### 배경 스토리

- **문제의 출발점**: HER2(ERBB2 gene 인코딩, 185 kDa receptor tyrosine kinase)는 유방암의 약 20–30%에서 과발현되어 PI3K/Akt, PLC-γ, MAPK 경로 과활성화를 통해 종양 성장·생존·침윤을 유도한다. Trastuzumab(Herceptin®), pertuzumab(Perjeta®), lapatinib 등 HER2-targeting 치료제가 FDA 승인을 받았으나, HER2-양성 유방암 환자의 약 60–70%는 de novo 내성 또는 치료 중 내성을 발생시킨다(refs [11,12,15]).

- **선행 접근 A (HER2 shedding 기전)**: 기존 제안 기전 중 하나는 ECD shedding — EJM 부위 절단 시 p95HER2가 막에 남고 세포외 도메인이 분리되어 trastuzumab 결합이 불가해진다. IJM 절단 시는 반대 결과. 이 기전은 일부 환자에서 확인되나 60–70% 내성 발생률을 충분히 설명하지 못한다(refs [11,12,16,17]).

- **A의 한계**: HER2 shedding은 단백질 수준 기전이어서 ERBB2 mRNA 자체의 downregulation을 설명하지 못한다. 또한 lapatinib(세포내 TK 도메인 억제제) 내성과의 연결도 불명확하다.

- **선행 접근 B (EMT-내성 연결 가설)**: Nami & Wang(Cancers 2017, ref [12])이 EMT와 HER2 내성 사이의 negative feedback loop 가설을 제시. 상피형 세포는 HER2 high, 간엽형 세포는 HER2-low/-negative이며 trastuzumab 내성이다. CD44+/CD24− 간엽형 BCSCs(유방암 줄기세포)가 HER2-low이고 trastuzumab 고내성을 보인다는 임상·세포 데이터도 다수 축적되었다(refs [28–45]).

- **B의 한계**: EMT와 ERBB2 발현 감소의 *분자 기전*이 규명되지 않았다. 특히 ERBB2 유전자가 어떻게 silenced 되는지가 불명확했다. Promoter CpG island methylation이 후보로 거론되었으나, 세포주 간 methylation 차이가 없다는 결과가 있었다.

- **이 논문으로 이어지는 gap**: Promoter methylation이 아닌 *chromatin architecture 재조직*—특히 active histone mark의 소실과 ERBB2 chromatin accessibility 감소—이 ERBB2 silencing을 유도한다는 가설이 직접 검증된 연구가 없었다. 이 논문은 공개 genomics 데이터 재분석 + 세포 실험으로 그 공백을 채우려 한다.

### 기본 개념

- **EMT (epithelial-mesenchymal transition)**: 상피형 세포가 간엽형 표현형으로 전환. E-cadherin 감소, Vimentin/N-cadherin 증가, 이동성 획득 특징. TF 네트워크(SNAI2, ZEB1, TWIST2 등)로 조절.
- **Chromatin accessibility**: ATAC-seq, DNase I hypersensitivity로 측정. Open chromatin = TF 접근 가능, 발현 허용. Closed chromatin = 접근 차단, 발현 억제.
- **Active vs. inactive histone marks**: H3K4me2/me3(활성 promoter), H3K9ac, H3K27ac, H4K8ac(활성 enhancer), H2BK120ub, H3K39me3, H3K79me2(활성 gene body) — 발현 허용. H3K9me, H3K27me3(폐쇄/비활성) — 발현 억제.
- **Promoter-enhancer chromatin loop**: IM-PET(Integrated Methods for Predicting Enhancer Targets) / ChIA-PET으로 검출. ERBB2 promoter가 먼 거리 enhancer와 loop를 형성할 때 전사 활성화에 기여.
- **TF binding at cis-regulatory regions**: ChIPbase v2.0(ChIP-seq indexed in 3,740 human biological samples)으로 ERBB2 ±10 kb 영역의 TF 결합 패턴 조사.

### 이 논문의 필요성

- **핵심 이유**: Trastuzumab/lapatinib 내성의 epigenetic chromatin 기전을 규명하면, 내성 예측 바이오마커와 epigenetic 억제제 병용 치료 설계의 생물학적 근거가 생긴다.
- **기존 방법으로 부족했던 지점**: 내성 기전 연구가 단백질 수준(HER2 shedding, downstream signaling)에 집중되어 ERBB2 chromatin 구조와 EMT-관련 TF 재조직의 연결을 체계적으로 다루지 않았다.
- **이 논문이 해결하려는 방향**: 공개 genomics 데이터(METABRIC, GEO ChIP-seq/ATAC-seq) + in vitro EMT 유도 실험으로 EMT → ERBB2 chromatin 폐쇄 → HER2 발현 감소 → trastuzumab 내성의 기전적 사슬을 제시.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: EMT 상태와 ERBB2 chromatin 활성 사이의 상관관계를 공개 데이터 재분석 + 세포 실험으로 검증하고, EMT가 trastuzumab 내성을 유도하는 기전으로서 ERBB2 epigenetic silencing을 제시.
- **입력**: (1) METABRIC n=1,904 유방암 RNA-seq Z-score(cBioPortal); (2) GEO expression arrays — 세포주 panel(GSE50811), lapatinib-sensitive/resistant BT474(GSE16179), TGF-β1 처리 A549(GSE17708); (3) CpG methylation array(GSE44838); (4) GEO/Cistrome ChIP-seq — 7가지 히스톤 mark × 6–7 cell lines(Table S2); (5) ATAC-seq, DNase-seq (MCF7 vs. MDA-MB-231); (6) 4Dgenome IM-PET promoter-enhancer interaction; (7) BT474 in vitro EMT 유도 실험.
- **출력**: ERBB2 발현-EMT 마커 상관계수, histone mark ChIP-seq enrichment 비교, chromatin accessibility, trastuzumab binding immunofluorescence.
- **중요한 hidden assumption**: 서로 다른 연구실·조건에서 생산된 공개 ChIP-seq 데이터를 배치 효과 보정 없이 비교 가능하다고 가정. Cell line n=5–8로 통계 검정력 제한.

### 확률 / 통계학적 구조

- **Model family**: 관찰 연구 + correlation analysis + group comparison. Computational method/tool 개발 없음.
- **통계 검정**: Two-tailed Student's t-test, ANOVA. GraphPad Prism v.6.
- **표현 방식**: Mean ± SD.
- **유의 기준**: $p < 0.050$.
- **Multiple testing correction**: 미제공. 12 epithelial + 12 mesenchymal marker × ERBB2 상관 등 다중 비교에 대한 FDR 보정 명시 없음.
- **ChIP-seq 시각화**: WashU Epigenome Browser. 정량 비교 통계 없이 browser track 시각적 비교 위주.
- **Expression data 전처리**: GEO array → Affymetrix TAC 3.0 소프트웨어.

### 핵심 method insight

- **기존 방법의 한계**: CpG island methylation 분석이 ERBB2 silencing을 설명하지 못했다. HER2-high(BT474, HCC-1954, MDA-MB-453, SKBR3)와 HER2-low(BT20, MCF7, MDA-MB-231, MDA-MB-468, SUM-159PT, T47D) 세포주 사이에 promoter methylation 유의한 차이 없음(Figure 1D, GSE44838).
- **이 논문이 바꾼 가정**: ERBB2 silencing은 DNA methylation이 아니라 histone modification 패턴(active mark 소실)과 chromatin accessibility 감소에 의해 조절된다.
- **분석 전략의 핵심**: (1) ChIPbase v2.0으로 epithelial vs. mesenchymal TF가 ERBB2 cis-regulatory region에 차별 결합함을 보임; (2) 복수 active/inactive histone mark ChIP-seq을 HER2-high vs. HER2-low에 걸쳐 비교; (3) 4Dgenome IM-PET로 promoter-enhancer loop 수 정량; (4) in vitro EMT → trastuzumab binding 감소로 기능적 귀결 확인.
- **이 변화가 중요한 이유**: Active mark 결핍이 원인이라면 HDAC inhibitor 또는 chromatin remodeling inhibitor와 HER2 치료제 병용이 내성 극복 전략이 될 수 있다.

### 이전 방법과의 차이

- **Baseline / 선행 연구**: HER2 단백질 발현 변화만 관찰하거나 단일 cell line에서 EMT-HER2 연결 확인.
- **공통점**: Cell line 기반 expression 비교, GEO 공개 데이터 활용.
- **차이점**: 복수 histone mark × 복수 cell line ChIP-seq 동시 비교; ERBB2 promoter-enhancer loop 수 정량화; in vitro EMT 유도 후 약물 binding 확인.
- **차이가 크게 나타나는 조건**: HER2-high epithelial(BT474, HCC-1954, SKBR3, AU565, MDA-MB-361) vs. HER2-low mesenchymal(MCF7, MDA-MB-231, MDA-MB-468) 비교.

### 효과가 Results에서 나타난 방식

- ERBB2 발현과 epithelial marker 양의 상관, mesenchymal marker 음의 상관 — 모두 $p < 0.0001$ (METABRIC n=1,904).
- HER2-high cell line에서 active promoter(H3K4me2, H3K4me3) + active enhancer(H3K9ac, H3K27ac, H4K8ac) ChIP-seq signal 풍부; HER2-low에서 감소.
- Inactive marks(H3K9me, H3K27me3): 양군 모두 낮아 "activator absence"가 silencing의 핵심 기전.
- HCC-1954(HER2-high) ERBB2 promoter-enhancer loop 240개 vs. MCF7(HER2-low) 11개.
- A549 TGF-β1 72 h: ERBB2 mRNA 유의 감소, $p < 0.05 \sim p < 0.0001$.
- BT474 EMT 유도: Vimentin 증가(간엽 전환 확인) + trastuzumab binding 감소(immunofluorescence).

### Method 관점의 한계

- 세포주 n=5–8 소규모 + 공개 ChIP-seq 배치 효과 미보정.
- ChIP-seq 비교는 정량 통계 없이 browser track 시각적 비교 위주.
- BT474 EMT 실험은 immunofluorescence 이미지만, trastuzumab binding의 정량 데이터(FACS MFI, Western blot HER2 단백질 정량) 미제공.
- Multiple testing correction 미적용.
- 저자 자체 ChIP-seq/ATAC-seq 생성 데이터 없음 — 전체 기전 분석이 공개 데이터 재분석에 의존.

---

## Results

### Dataset별 결과

#### Dataset 1 — METABRIC 유방암 종양 RNA-seq
- **Dataset**: METABRIC study, n = 1,904 breast cancer tumors. RNA-seq Z-score (v2 RSEM). cBioPortal 분석.
- **목적**: ERBB2 발현과 EMT marker 발현 간 상관관계 확인.
- **사용한 데이터 규모**: n = 1,904 종양 샘플, 12 epithelial markers(ALCAM, CD24, CDH1, F11R, FOXA1, KRT7, KRT8, KRT18, KRT19, MUC, NECTIN2, KRT20), 12 mesenchymal markers(CD44, CTNNB1, FOXC1, MYC, NOTCH1, NOTCH2, SNAI2, SOX10, TWIST2, VIM, ZEB1, ZEB2).
- **Metric / 평가 기준**: Pearson $R^2$, $p$-value.
- **주요 수치**:
  - ERBB2 vs. epithelial markers: FOXA1 $R^2 = 0.0784$, KRT8 $R^2 = 0.1237$, KRT18 $R^2 = 0.0730$, CD24 $R^2 = 0.0666$. 모두 $p < 0.0001$.
  - ERBB2 vs. mesenchymal markers: ZEB1 $R^2 = 0.1260$, MYC $R^2 = 0.0718$, FOXC1 $R^2 = 0.0457$, ZEB2 $R^2 = 0.0468$. 모두 $p < 0.0001$.
  - 해석: $R^2$ 범위 0.005–0.12 — 설명 분산이 낮아 ERBB2 발현을 완전히 예측하는 단일 EMT marker는 없음. 방향성(positive vs. negative 상관)은 일관적.
- **논문 주장과의 연결**: Epithelial 상태 종양에서 ERBB2 발현 높고 간엽 상태 종양에서 낮다는 임상 데이터 기반 지지.

#### Dataset 2 — 유방암 세포주 expression + CpG methylation array (GSE44838)
- **Dataset**: GSE44838. 세포주 — HER2-high: BT474, HCC-1954, MDA-MB-453, SKBR3; HER2-low: BT20, MCF7, MDA-MB-231, MDA-MB-468, SUM-159PT, T47D.
- **목적**: ERBB2 발현과 FOXA1(epithelial marker) / FOXC1(mesenchymal marker) 상관, CpG methylation 차이 확인.
- **주요 수치/정성**: ERBB2와 FOXA1 양의 상관, FOXC1 음의 상관(HCC-1954 제외; Figure 1C). CpG island methylation: 세포주 간 유의한 차이 없음(Figure 1D).
- **논문 주장과의 연결**: Promoter methylation이 ERBB2 silencing 원인이 아님을 배제. → chromatin architecture 분석으로 전환 근거.

#### Dataset 3 — ChIPbase v2.0: ERBB2 chromatin TF binding
- **Dataset**: ChIPbase v2.0, 3,740 human biological samples에서 indexed ChIP-seq.
- **목적**: ERBB2 ±10 kb 내 결합 TF의 EMT 연관성 분류.
- **주요 수치**: 82개 TF가 결합 확인. 8개 = epithelial 유지 TF(CDX2, FOXA1, FOXA2, KLF9, MBD3, MXI1, RUNX3, SP1). 31개 = mesenchymal phenotype master regulator(ATF2, E2F1, E2F6, E2F7, EGR1, ELF2, ETS1, ETV1, FOS, FOXM1, FOXP1, FOXP2, GATA1, GATA2, GATA3, GATA6, HOXC9, JUNB, JUND, KDM5A, MAX, MAZ, MYC, MZF1, NANOG, RELA, SMAD4, STAT4, TEAD6, ZBTB7A) — 총 82개 중 epithelial 8개 < mesenchymal 31개(Figure 1E,F).
- **ATAC-seq/DNase-seq (MCF7 vs. MDA-MB-231)**: MCF7(epithelial-like) > MDA-MB-231(mesenchymal-like) at ERBB2 promoter + enhancer. E2F1(mesenchymal TF) enrichment: MDA-MB-231 > MCF7(Figure 1G).

#### Dataset 4 — 히스톤 mark ChIP-seq (7 cell lines × 10+ marks; GEO/Cistrome Table S2)
- **Dataset**: HER2-high (AU565, BT474, HCC-1954, MDA-MB-361, SKBR3, n=5) vs. HER2-low (MCF7, MDA-MB-231, MDA-MB-468, n=3). Franco et al. 2018(Genome Res.) 데이터 포함.
- **목적**: Active vs. inactive histone mark ChIP-seq enrichment가 HER2 발현 수준과 연관되는지 확인.
- **주요 결과(정성 위주; 정량 수치 browser track 시각 비교)**:
  - Active gene body marks (H2BK120ub, H3K39me3, H3K79me2): HER2-high > HER2-low (Figure 2B).
  - Active promoter marks (H3K4me1, H3K4me3): HER2-high "significantly higher"(Figure 2C).
  - Active enhancer marks (H3K9ac, H3K27ac, H4K8ac): HER2-high "relatively higher"(Figure 2D).
  - Inactive marks (H3K9me, H3K27me3): 양군 모두 낮음. 차이 미미(Figure 2E).
  - **핵심 해석**: Closed ERBB2 chromatin 상태가 repressor mark 축적이 아니라 activator mark 부재로 형성된다.
- **Promoter-enhancer loop(4Dgenome IM-PET/ChIA-PET)**: HCC-1954 — 240개 target enhancer와 loop(134 upstream, 106 downstream). 106개 loop 중 < 50 kb: 88개, > 500 kb: 18개. MCF7 — 11개 upstream enhancer만(10개 < 50 kb, 1개 ≈ 244 kb)(Figure 2F).

#### Dataset 5 — Lapatinib-sensitive vs. resistant BT474 expression array (GSE16179)
- **Dataset**: GSE16179. Lapatinib-sensitive BT474(n=3) vs. lapatinib-resistant BT474(n=3).
- **목적**: Lapatinib 내성이 EMT + ERBB2 downregulation과 연관되는지 확인.
- **주요 수치**: Resistant에서 ERBB2, CDH1, ALCAM, FOXA1, NECTIN2, OCLN 감소($p < 0.05 \sim p < 0.0001$); CDH2, FN1, FOXC1, SNAI2, VIM, MMP2, 3, 9, 10, 28 증가($p$ 같은 범위)(Figure 3A).
- **논문 주장과의 연결**: 자연 발생 lapatinib 내성 세포가 EMT 상태 전환 + ERBB2 감소를 동시에 보임 → EMT-HER2 내성 연결의 임상 세포주 근거.

#### Dataset 6 — TGF-β1 처리 A549 EMT 시계열 (GSE17708)
- **Dataset**: GSE17708. A549(HER2-high human lung cancer epithelial cell line) + 5 ng/mL TGF-β1, 시점: 0, 0.5, 1, 2, 4, 8, 16, 24, 72 h (각 n=3).
- **목적**: EMT 유도가 ERBB2 발현을 시간 의존적으로 downregulate하는지 확인.
- **주요 수치**: 72 h에서 ERBB2 mRNA "significant decline"($p < 0.05 \sim p < 0.0001$, Figure 3B). 상피 마커(CDH1, EPCAM, MUC1, OCLN) 감소, 간엽 마커(CDH2, FN1, SNAI2, VIM) 증가.
- **주의**: ERBB2 감소가 72 h에서만 나타남 — EMT의 후기 사건. 초기 시점(0.5–8 h) 변화는 유의성 미제공.
- **주의**: A549는 폐암 세포주 — 유방암 일반화 한계 있음.

#### Dataset 7 — BT474 in vitro EMT 유도 (직접 실험)
- **Dataset**: BT474(HER2-positive breast cancer cell line, ATCC). EMT-inducing supplement(StemXVivo CCM017; Wnt-5a, TGF-β1, anti-E-cadherin Ab, anti-sFRP-1 Ab, anti-Dkk-1 Ab), 15일 처리. n=미제공(단일 실험).
- **목적**: EMT 유도 후 HER2 발현 감소 + trastuzumab binding 감소 확인.
- **평가**: Cell morphology(광학현미경) + Vimentin immunofluorescence(EMT 확인) + trastuzumab 10 μg/mL 1 h 처리 후 binding immunofluorescence.
- **주요 결과(정성)**: PBS 대조군 대비 EMT-induced BT474에서 (1) 간엽 형태 전환, (2) Vimentin 발현 증가, (3) trastuzumab binding 감소(Figure 3C). 정량 수치(MFI, flow cytometry) 미제공.
- **논문 주장과의 연결**: EMT가 실제로 trastuzumab binding 저하로 이어짐을 직접 세포 실험으로 보임. 단, 정량 데이터 부재로 증거 수준 제한.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: Epithelial-like 상태 → high ERBB2 / open chromatin / active histone marks / epithelial TF / trastuzumab-sensitive. Mesenchymal-like 상태 → low ERBB2 / closed chromatin / absent active marks / mesenchymal TF / trastuzumab-resistant.
- **가장 중요한 수치**: METABRIC n=1,904에서 epithelial/mesenchymal marker와 ERBB2 상관 $p < 0.0001$; A549 72 h TGF-β1 처리 후 ERBB2 mRNA 유의 감소; HCC-1954 240 vs. MCF7 11 promoter-enhancer loops.
- **결과 해석 시 주의점**: ChIP-seq 비교가 소규모(n=5–8 cell line) + 시각적 비교 중심. BT474 EMT 실험 정량 데이터 부재. Multiple testing correction 미적용. 관찰 연구로 인과 관계 직접 증명 아님.

---

## Figures

#### Figure 1
- **이 Figure가 필요한 이유**: ERBB2 발현이 EMT 상태에 반비례하며, 그 기전이 CpG methylation이 아닌 chromatin architecture임을 여러 데이터를 통해 동시에 제시하기 위해 배치.
- **이 Figure가 뒷받침하는 주장**: Epithelial-like 세포/종양은 ERBB2 high + open chromatin; mesenchymal-like는 ERBB2 low + closed chromatin. Promoter CpG methylation은 차이 없음.

##### 패널별 설명
- **A**: METABRIC n=1,904에서 ERBB2 vs. 12개 epithelial marker 상관 scatter plots(orange). 모두 양의 상관, $p < 0.0001$.
- **B**: METABRIC n=1,904에서 ERBB2 vs. 12개 mesenchymal marker 상관 scatter plots(green). 모두 음의 상관, $p < 0.0001$.
- **C**: 10개 유방암 세포주에서 ERBB2, FOXA1, FOXC1 mRNA. Color gradient bar = HER2 발현 수준. ERBB2와 FOXA1 양의 상관, FOXC1 음의 상관(HCC-1954 제외).
- **D**: 10개 세포주 ERBB2 promoter CpG island methylation. 세포주 간 유의한 차이 없음.
- **E**: ERBB2 ±10 kb 내 TF 결합 word cloud(ChIPbase v2.0). 크기 = 결합 sample 수. CTCF, HNF4A 두드러짐. Orange = epithelial TF, green = mesenchymal TF.
- **F**: 확인된 epithelial TF 수(orange bar, ~10개) vs. mesenchymal TF 수(green bar, ~35개) — mesenchymal TF 압도적 다수.
- **G**: MCF7(epithelial-like) vs. MDA-MB-231(mesenchymal-like)에서 ATAC-seq, DNase-seq, E2F1 ChIP-seq enrichment at ERBB2 promoter/enhancer. MCF7 > MDA-MB-231. 노란색 = enhancer 영역, 분홍색 = promoter 영역.

##### 본문에서 강조한 비교
- MCF7 ERBB2 chromatin이 MDA-MB-231보다 더 open/accessible.
- E2F1(mesenchymal TF)이 MDA-MB-231 ERBB2 promoter에서 높은 enrichment — closed chromatin이지만 mesenchymal TF가 점령.

##### 해석 시 주의점
- $R^2$ = 0.005–0.12: 낮은 설명 분산. EMT 상태가 ERBB2 발현 변화의 일부 설명자임을 보이나, 전체를 설명하지 않음.
- Word cloud(Panel E)는 결합 빈도 기반 시각화 — 기능적 중요성과 직접 대응하지 않음.

---

#### Figure 2
- **이 Figure가 필요한 이유**: Active histone mark 풍부도가 ERBB2 발현 수준과 일치하고, inactive mark는 양군 모두 낮다는 것을 복수 mark × 복수 cell line ChIP-seq 데이터로 보이기 위해 배치.
- **이 Figure가 뒷받침하는 주장**: ERBB2 chromatin silencing은 repressor histone 축적이 아니라 activator mark 소실에 의해 형성된다.

##### 패널별 설명
- **A**: ERBB2, MUC1(epithelial), VIM(mesenchymal), GAPDH mRNA bar graphs. HER2-high(HCC-1954, BT474, SKBR3, AU565, MDA-MB-361) vs. HER2-low(MCF7, MDA-MB-231, MDA-MB-468). MUC1은 HER2-high에서 높고 VIM은 HER2-low MCF7/MDA-MB-231에서 높음.
- **B**: H2BK120ub, H3K39me3, H3K79me2(active gene body) ChIP-seq browser tracks. HER2-high > HER2-low.
- **C**: H3K4me1, H3K4me3(active promoter) ChIP-seq tracks. HER2-high에서 significantly higher.
- **D**: H3K9ac, H3K27ac, H4K8ac(active enhancer) tracks. HER2-high에서 higher.
- **E**: H3K9me, H3K27me3(inactive/closed) tracks. 양군 모두 낮음.
- **F**: HCC-1954 (left) vs. MCF7 (right) IM-PET circle interaction map + scatter plot. HCC-1954: 240개 target enhancer regions(134 upstream, 106 downstream). MCF7: 11개 upstream. Scatter plot: chromatin loop size distribution.

##### 본문에서 강조한 비교
- H3K9me, H3K27me3 양군 모두 낮음 — 폐쇄 상태가 "active mark 부재"로 설명.
- HCC-1954 240 loop vs. MCF7 11 loop — chromatin topology와 ERBB2 발현 수준의 직접 연결.

##### 해석 시 주의점
- Browser track 시각적 비교 — 정량 bar graph나 peak intensity 통계 없음.
- 서로 다른 연구실 데이터 통합; 배치 효과 미언급.

---

#### Figure 3
- **이 Figure가 필요한 이유**: EMT가 실제로 HER2 downregulation → 약물 내성으로 이어짐을 두 공개 dataset(lapatinib-resistant BT474, TGF-β1 A549) + 직접 BT474 EMT 실험으로 다각 검증하기 위해 배치.
- **이 Figure가 뒷받침하는 주장**: EMT가 ERBB2 발현을 감소시키고, 이것이 trastuzumab binding 저하로 귀결됨.

##### 패널별 설명
- **A**: GSE16179 — Lapatinib-sensitive(orange) vs. resistant(green) BT474. ERBB2·housekeeping·epithelial marker 낮음; mesenchymal marker·MMP 높음. 통계 * ~ ****.
- **B**: GSE17708 — TGF-β1 처리 A549 시계열(0–72 h). 72 h에서 ERBB2 mRNA 유의 감소. Epithelial ↓, mesenchymal ↑. 통계 * ~ ****.
- **C**: BT474 PBS(상단) vs. EMT-induced(하단). 광학현미경 형태 비교. Immunofluorescence: DAPI(blue), Vimentin(FITC, green), trastuzumab(TRITC, red). EMT 세포: Vimentin 증가, trastuzumab 염색 감소.
- **D**: Summary schematic. EMT 진행에 따른 epithelial phenotype ↓, 간엽 ↑, ERBB2 chromatin activity ↓, HER2 발현 ↓, anti-HER2 drug resistance ↑의 연쇄를 도식화.

##### 본문에서 강조한 비교
- Panel C: PBS 대조군(trastuzumab 균일 결합) vs. EMT 유도(trastuzumab 염색 희미) — EMT가 실제로 약물 접근성을 낮춤.
- Panel A: 자연 발생 lapatinib 내성이 EMT 전환 + ERBB2 감소와 동반.

##### 해석 시 주의점
- Panel C 정량 데이터 미제공. 면역형광 이미지만으로 결론 — 재현 및 정량 확인 필요.
- A549는 폐암 세포주 — 유방암 직접 적용 한계.

---

## Tables

본문에 정식 Table 없음.

### Supplementary Table S1

- **목적**: 분석에 사용된 GEO expression/methylation array 데이터 accession ID 목록.
- **구조**: GEO Series / GEO Samples / Data Type / Reference.
- **주요 항목**:
  - GSE110189: CHO-K1/K6 trastuzumab+pertuzumab 처리 (ref [Nami 2019, Cancers]).
  - GSE50811: 유방암 세포주 expression profiling (ref [Dezso 2014, PLoS ONE]).
  - GSE44838: 유방암 세포주 expression + methylation array (ref [Di Cello 2013, PLoS ONE]).
  - GSE16179: Lapatinib-sensitive vs. resistant BT474 (ref [Liu 2009, Cancer Res.]).
  - GSE17708: A549 + TGF-β1 시계열 (ref [Sartor 2010, Bioinformatics]).

### Supplementary Table S2

- **목적**: ChIP-seq 분석에 사용된 Cistrome DB ID + GEO sample ID 전수 목록.
- **구조**: Factor / X-seq 종류 / Cell line / Cistrome DB ID / GEO sample ID / Reference.
- **커버리지**: ATAC-seq(MCF7, MDA-MB-231), DNase-seq(MCF7, MDA-MB-231), FOXA1, E2F1, H2BK120ub, H3K39me3, K3K79me2, H3K4me1, H3K4me3, H3K9ac, H3K27ac, H4K8ac, H3K9me3/me2, H3K27me3 — 세포주 6–7개 × mark별.
- **주요 reference**: Franco et al. 2018 Genome Res.(대부분의 histone mark ChIP-seq 출처, ref [13]).

---

## Supplementary Information

- **Table S1**: GEO expression/methylation array accession. 위 Tables 섹션 요약 참조.
- **Table S2**: ChIP-seq Cistrome DB + GEO accession. 위 Tables 섹션 요약 참조.
- **life-11-00868-s001.zip**: 보완 자료 archive (온라인 https://www.mdpi.com/article/10.3390/life11090868/s1). Supplementary PDF(life-1333507-supplementary.pdf)가 Table S1, S2를 포함.

---

## 분석 자체에 대한 메모

- ChIP-seq 비교가 소규모(HER2-high n=5, HER2-low n=3) + browser track 시각적 비교 중심 — 정량 peak intensity 통계 보완 필요.
- BT474 EMT 직접 실험(Dataset 7)에서 trastuzumab binding 감소의 정량 데이터(FACS, Western blot) 미제공 — 핵심 결론의 증거 수준 제한.
- "Activator histone mark 부재가 ERBB2 silencing 원인"이라는 주장은 흥미롭나, H3K9me/H3K27me3 외 다른 repressor 기전(PRC2 recruitment, DNMT3A de novo methylation at non-CpG island region 등)은 미검토.
- 저자 자체 ChIP-seq/ATAC-seq 생성 데이터 없음 — 전체 chromatin 분석이 공개 데이터 재분석에 의존하며, 비교 cell line 선정의 선택 편향 가능성.
- 재검토 필요: A549 폐암 세포주 결과의 유방암 일반화 타당성, BT474 EMT 실험의 replicate 수 미제공.
