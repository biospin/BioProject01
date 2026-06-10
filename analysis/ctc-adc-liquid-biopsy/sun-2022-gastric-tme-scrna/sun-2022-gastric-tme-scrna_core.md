# sun-2022-gastric-tme-scrna — Core Analysis

## Executive Summary

- **무엇**: 위암(GC) 10명 환자에서 종양·주변정상·혈액 매칭 166,533세포의 scRNA-seq atlas를 구축, TASC-TAM-LAMP3+ DC 삼각 상호작용 허브와 Tc17→exhaustion이라는 대안적 T세포 소진 경로를 규명한 TME 지도 논문.
- **모델 / 방법**: 10x Chromium 5' scRNA-seq + TCR/BCR V(D)J profiling → Leiden 클러스터링 → inferCNV·WES 기반 종양세포 동정 → SCENIC TF regulon → CellPhoneDB 리간드-수용체 분석 → RNA velocity·diffusion map 기반 상태전이 추론.
- **핵심 결과**:
  - ① 전체 atlas — 166,533세포, 12 lineage, 종양·주변정상·혈액 각 48.3%/37.2%/14.5%
  - ② TASC (Fib_1 + SMC_1 + Endo_1) 비율 상위 40%군이 TCGA-STAD에서 유의미하게 불량 예후 (Kaplan-Meier, Cox HR > 1, p < 0.01)
  - ③ Tc17 ($\text{IL-17}^+\text{CD8}^+$) 세포가 10환자 중 8명의 종양에서 >1% 확인, tissue-resident memory CD8+ T세포에서 기원하여 소진 상태로 분화하는 alternative exhaustion trajectory 규명
  - ④ Mφ_APOE 대식세포에서 지질·리소솜 관련 유전자 *APOE, TREM2, CD63, LAMP1* 상향, TASC와 상호강화 피드백 루프 형성
  - ⑤ *IL17, IL22, IL26* 수용체(*IL17RA/RC, IL10RB, IL20RA, IL22RA1*)가 종양 조직에서 정상 대비 유의미하게 상향 (TCGA-STAD, Wilcoxon, p < 0.01~0.005)
- **우리 적용**: 위암·고형암 ADC 타겟 선정 시 tissue-side TME reference (TASC, Tc17, Mφ_APOE 세포군 주목); 방법론적으로 CellPhoneDB 기반 L-R 분석 파이프라인 차용 가능 — methodology-reference + academic-citation.
- **심층**: 한계·재현 ROI는 `sun-2022-gastric-tme-scrna_lens-academic.md` / `sun-2022-gastric-tme-scrna_lens-industry.md` / `sun-2022-gastric-tme-scrna_methodology-brief.md` 참고.

---

## Identity

- **Title**: scRNA-seq of gastric tumor shows complex intercellular interaction with an alternative T cell exhaustion trajectory
- **Authors**: Sun K.\*, Xu R.\*, Ma F.\*, Yang N.\*, Li Y.\* et al. (공동 제1저자 5명); 교신저자 Yantao Tian, Xun Lan
- **Year**: 2022
- **Venue**: Nature Communications 13:4943
- **DOI**: 10.1038/s41467-022-32627-z
- **Citation key**: `@sun2022gastrictme`
- **Data**: BIG Data Center GEO Sequence Archive HRA000704; OMIX001073 (processed matrices)
- **Code**: https://github.com/Lan-lab/sc-GC

---

## Background

### 배경 스토리

- **문제의 출발점**: 위암은 전 세계 암 사망 원인 3위(2018년 약 783,000명 사망)이며, 대부분 진행기에 진단된다. PD-1/CTLA-4 면역관문억제제가 흑색종 등에서 paradigm shift를 가져왔지만, GC에서 반응률은 낮다(본문 서론). TME의 세포 구성이 개인마다 크게 다르고 면역·기질·상피 구획이 복잡하게 얽혀 있다는 점이 주요 원인으로 지목됐다.

- **선행 접근 A (bulk RNA-seq 기반 TME 분석)**: Zhang et al. (Gut 2020)과 Wang et al. (Nat Med 2021)이 bulk sequencing으로 위암 transcriptional heterogeneity와 lineage diversity를 정리했다. 그러나 bulk sequencing은 세포 유형 별 해상도를 제공하지 못하며, TME 내 희귀 세포군이나 세포 상태 전이를 포착할 수 없다.

- **선행 접근 B (scRNA-seq 선행 GC atlas)**: Zhang et al. (Cell Rep 2019), Yin et al. (Front Immunol 2021), Kumar et al. (Cancer Disco 2022) 등이 GC 단일세포 지도를 부분적으로 구축했지만, 세포 수가 적거나, 혈액·주변정상 조직 매칭이 없거나, T/B세포 수용체 repertoire 분석 없이 진행되어 상태전이 방향을 추론하기 어려웠다.

- **B의 한계**: 기존 GC scRNA-seq 연구들은 (1) 세포 수가 수천~수만 규모로 atlas 수준에 미달, (2) paratumor + 혈액 matched 샘플 없어 세포 이동 경로 분석 불가, (3) TCR clonotype 기반 세포 계보 추적 미흡.

- **이 논문으로 이어지는 gap**: 위암 TME에서 면역·기질·상피 전 구획을 한 연구 안에서 정량적으로 비교하고, 특히 기질세포(TASC) 및 골수세포(TAM, LAMP3+ DC)가 T세포 기능에 어떻게 작용하는지, 그리고 GC 특이적 Tc17 세포가 어떤 경로로 소진에 이르는지는 규명되지 않았다.

### 기본 개념

- **TME (tumor microenvironment)**: 종양세포 주변의 면역세포·기질세포·혈관·세포외기질 등 전체 생태계. 종양 진행과 면역요법 반응성을 결정하는 주요 인자.
- **TASC (tumor-associated stromal cells)**: 이 논문이 정의한 집합 개념으로, 종양 조직에 농축된 Fib_1(cancer-associated fibroblast 특성), Endo_1, SMC_1 세 기질 클러스터. Wnt 신호 및 혈관신생 활성이 증가한다.
- **Tc17 세포**: $\text{IL-17}^+\text{CD8}^+$ T세포 군. 고전적 세포독성 CD8+ T세포와는 별개로, *RORC/RORγt*를 발현하며 위암을 포함한 소화기계 암에서 불량 예후와 관련됐다고 보고된 세포군.
- **T세포 소진(exhaustion)**: 종양 내 지속 항원 자극에 의해 T세포가 *PDCD1(PD-1), CTLA4, TIGIT* 등 면역관문 분자를 높이 발현하고 세포독성 기능을 잃는 상태. 본 논문은 cytotoxic-exhaustion 경로 외에 Tc17→exhaustion이라는 새 경로를 제안한다.
- **CellPhoneDB**: 단일세포 데이터에서 ligand-receptor 발현을 이용해 세포 간 상호작용을 통계적으로 예측하는 알고리즘(v2.0). 본 논문에서 세포 유형 쌍 간 L-R 쌍을 도출하는 데 사용.
- **RNA velocity (scVelo)**: 미성숙(unspliced) vs. 성숙(spliced) mRNA 비율로 세포 상태 전이 방향과 속도를 추론하는 방법. 본 논문에서 LAMP3+ DC 발달 방향 확인에 사용.

### 이 논문의 필요성

- **핵심 이유**: 대규모(n > 160,000세포), 삼중 matched(종양·주변정상·혈액) 설계로 GC TME의 전 구획을 동시에 분석한 최대 규모 GC atlas 필요성.
- **기존 방법으로 부족했던 지점**: T세포 상태전이를 clonotype + trajectory 두 축으로 동시에 검증한 연구가 없었고, TASC가 예후 인자임을 scRNA-seq + TCGA-STAD 연계로 검증한 사례 부재.
- **이 논문이 해결하려는 방향**: 4가지 세포 구획(면역/기질/상피/내피) 통합 + TCR/BCR profiling + CellPhoneDB + SCENIC을 조합해 GC TME의 세포간 상호작용 네트워크와 T세포 소진 경로를 규명.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 위암 TME의 전 구획 세포를 single-cell 해상도로 정량·분류하고, 기질세포-면역세포 간 상호작용 네트워크와 CD8+ T세포 상태전이 경로를 규명.
- **입력**: 10명 GC 환자의 종양(10), 주변정상(8), 혈액(4) 샘플에서 분리한 단일세포 라이브러리; 동일 샘플 bulk RNA-seq; WES; TCR/BCR V(D)J sequencing.
- **출력**: 세포유형 분류 atlas, 종양세포 동정, 기질세포 재형성 지도, T세포 소진 trajectory, L-R 상호작용 네트워크, 예후 연관성 결과.
- **추정 대상**: 세포 유형 label, 종양/정상 세포 구분(CNV score 기반), TF regulon 활성, RNA velocity 방향, clonotype 이동 지수.
- **중요한 hidden assumption**: (1) scRNA-seq 클러스터 = 생물학적 세포 상태라고 가정; (2) CellPhoneDB L-R 예측 = 실제 세포 접촉 신호라는 correlative assumption; (3) trajectory 분석의 pseudotime이 실제 시간 경과를 반영한다는 가정.

### 확률 / 통계학적 구조

- **Model family**: 주로 exploratory data analysis + 통계적 가설검정 조합. Deep generative model 없음.
- **Likelihood / objective**: 없음(unsupervised clustering, Leiden algorithm). DEG는 Wilcoxon rank-sum test로 검정; L-R interaction 유의성은 permutation-based empirical p-value (1,000회).
- **Prior / regularization**: SCTransform(Seurat 3.1)으로 배치효과 보정, 변수 유전자 기반 HVG 선택.
- **Latent variable / hidden state**: UMAP embedding (2D 시각화); Diffusion map (DCs 기반 pseudotime). inferCNV의 CNV score가 종양세포의 latent identity proxy.
- **Inference / optimization**: Leiden clustering (γ 파라미터별로 30~100 neighbors); SCENIC (GENIE3+RcisTarget)로 TF regulon activity (AUCell score); MuSiC로 bulk RNA-seq cell type deconvolution.
- **Noise, sparsity, uncertainty 처리**: UMI < 400, 유전자 수 < 200, 미토콘드리아 > 30% 세포 제거; doublet은 conventional marker로 수동 제거(Supplementary Data 2). T세포 분석에서 미토콘드리아 필터 20%로 완화.

### 핵심 method insight

- **기존 방법의 한계**: 기존 GC scRNA-seq는 세포 수 부족 + 혈액 대조군 없음 + TCR 정보 미통합 → T세포 계보 추적 불가.
- **이 논문의 바꾼 가정**: matched 삼중 샘플(종양·주변정상·혈액) + TCR clonotype 공유 분석 + RNA velocity 동시 사용 → 상태전이 방향을 두 독립 방법으로 교차검증.
- **새로 추가한 변수 또는 구조**: Morisita-Horn similarity index로 혈액↔고형조직 간 clonotype 이동 지수를 정량화; TASC를 단일 세포군이 아닌 Fib_1·Endo_1·SMC_1 세 클러스터의 집합 개념으로 정의.
- **이 변화가 중요한 이유**: 두 독립 증거(clonotype + velocity)가 같은 방향을 가리킬 때 trajectory inference의 신뢰도가 높아진다. TASC를 집합으로 보면 MuSiC deconvolution과 예후 분석에서 더 강한 신호를 얻는다.

### 이전 방법과의 차이

- **Baseline**: Zhang 2019(Cell Rep), Yin 2021(Front Immunol), Kumar 2022(Cancer Disco) — 세포 수 소규모, 단일 조직 유형.
- **공통점**: 10x Chromium + Leiden/Louvain 클러스터링 + UMAP.
- **차이점**: (1) 규모 — 166,533세포, 10환자 삼중 매칭. (2) TCR/BCR 통합 + clonotype-sharing matrix. (3) SCENIC TF regulon + CellPhoneDB L-R + MuSiC deconvolution을 동시 적용. (4) TCGA-STAD bulk cohort와 예후 연계 검증.
- **차이가 크게 나타나는 조건**: T세포 상태전이처럼 희귀 세포군 간의 계보 관계를 추론해야 할 때 clonotype+velocity 이중 증거가 결정적.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: TCGA-STAD (n = 375 종양, n = 32 정상), 독립 검증 코호트 7명(MHC class II 분석용), GEO 데이터셋 GTEx (장·식도 정상 조직 발현).
- **Metric**: Kaplan-Meier 생존, Cox HR, Wilcoxon p-value, Spearman correlation, permutation empirical p-value.
- **개선된 결과**: Fib_1·SMC_1 높은 비율 환자군이 TCGA-STAD에서 불량 예후 (HR > 1, p = 0.0019/0.009); Tc17 세포가 10명 중 8명 종양에서 존재; TASC-Mφ_APOE 피드백 루프 in vitro 검증(CAFs CM으로 THP-1 macrophage 유도 후 Mφ_APOE 마커 유전자 증가).
- **Ablation 근거**: Supplementary Note 1–2에서 batch correction(SCTransform)과 T세포 클러스터 robustness를 별도 평가.
- **정성적 효과**: Endo_1의 MHC class II 발현 감소(종양 내 내피세포의 항원제시 기능 약화), LAMP3+ DC가 cDC2에서 기원한다는 RNA velocity 기반 추론.

### Method 관점의 한계

- **약한 assumption**: CellPhoneDB L-R 예측은 세포 접촉 여부를 직접 측정하지 않는다. 공간 정보 없는 bulk co-expression에 기반한 association이다.
- **구현 또는 학습상의 부담**: SCENIC (GENIE3 + RcisTarget)은 계산 비용이 높고, 결과가 reference motif database 품질에 의존한다.
- **일반화가 불확실한 조건**: 단일 기관(Tsinghua-NCC, 중국 Beijing) 10명 코호트; 치료 전 untreated 환자에 한정; 내시경생검이 아닌 수술절제 조직 위주.

---

## Results

### Dataset별 결과

#### Dataset 1 — 위암 TME 전체 atlas (10 GC patients)

- **Dataset**: 10명 위암 환자, 종양 10개·주변정상 8개·혈액 4개 샘플. 10x Chromium 5' scRNA-seq. 중국 National Cancer Center (CICAMS) 및 Tsinghua University 치료 미경험 환자.
- **목적**: GC TME의 전 구획 세포 유형 지도 구축 및 세포 비율 정량화.
- **사용한 데이터 규모**: 166,533세포 (QC 통과), 평균 1,620 유전자/세포, 5,518 UMI/세포. 종양 48.3% / 주변정상 37.2% / 혈액 14.5%.
- **Baseline / 비교 대상**: 혈액 vs. 주변정상 vs. 종양 간 세포 비율 비교 (Ro/e 비율).
- **Metric / 평가 기준**: Ro/e (관찰/기대 세포 비율), 표준화 발현값.
- **주요 수치**: 12 major lineage; Supplementary Data 1에 환자별 임상정보; 내분비세포는 주로 GC07·GC08·GC10 환자에서 기원.
- **정성 결과**: 거의 모든 세포 유형이 모든 환자에서 발견됨. 세포 비율이 환자마다 크게 다름.
- **논문 주장과의 연결**: GC TME가 복잡하고 환자마다 이질적임을 확인, 기존 bulk 연구의 한계를 scRNA-seq으로 보완.

#### Dataset 2 — 상피세포·종양세포 이질성 (epithelial 재클러스터)

- **Dataset**: 상피세포 추출 후 재클러스터링.
- **목적**: 종양세포 vs. 정상 상피세포 동정, 장형이형성(IM) 클러스터 특성 분석.
- **사용한 데이터 규모**: 미제공(본문 "small number of epithelial cells" 일부 환자에서).
- **Baseline / 비교 대상**: Normal 클러스터 vs. Tumor 클러스터 DEG; bulk RNA-seq (동일 환자) vs. scRNA-seq DEG 교집합.
- **Metric**: Spearman correlation (bulk RNA-seq log2FC vs. scRNA-seq log2FC); r = 0.883(GC07), 0.707(GC08_1), 0.789(GC08_2), 0.927(GC10) (Fig. 2e).
- **주요 수치**: GC08·GC09는 goblet/enterocyte score 높음. *CDX2* 관련 유전자 (*GUCY2C, SF, GPA33*) 종양에서 상향.
- **논문 주장과의 연결**: bulk RNA-seq와 scRNA-seq 결과 일치성이 높아 종양 클러스터 동정 신뢰성을 뒷받침.

#### Dataset 3 — 기질세포 재형성 + TASC 예후 (stromal compartment)

- **Dataset**: 기질세포 재클러스터링 → 12 clusters (Endo_1~4, Fib_1~5, SMC_1~2, Myofibroblast); 검증 코호트 9명 추가(MHC class II 유세포분석); TCGA-STAD (n = 1274 종양, n = 1461 주변정상).
- **목적**: 종양 내 기질세포 재형성 특성 파악, TASC 예후 영향 검증.
- **주요 수치**:
  - MHC class II+ 내피세포 비율: 주변정상 > 종양 (p = 2.1e-6, Student's paired t-test, n = 9 검증코호트) (Fig. 3g).
  - WNT2, WNT5A 종양 섬유아세포 상향: p = 3.5e-70, p = 3.9e-56 (Wilcoxon rank-sum, scRNA-seq 데이터) (Fig. 3i).
  - SFRP1 종양 섬유아세포 하향: p = 1.3e-70 (Fig. 3i).
  - Fib_1 높은 비율군 불량 예후 (TCGA-STAD, Kaplan-Meier, HR(high) = 1.8, p(HR) = 0.0019, n_high = 139, n_low = 139) (Fig. 3l).
  - SMC_1 높은 비율군 불량 예후 (HR(high) = 1.8, p(HR) = 0.009) (Fig. 3l).
  - CAFs conditioned medium (CM)이 6개 GC 세포주에서 세포 증식 지원 (CCK-8 assay, n = 6, p < 0.05) (Fig. 3m).
- **논문 주장과의 연결**: TASCs가 Wnt 신호·혈관신생을 통해 종양을 촉진하고 불량 예후와 연관됨을 다중 데이터로 검증.

#### Dataset 4 — 골수세포 이질성 + Mφ_APOE 특성 (myeloid compartment)

- **Dataset**: 골수세포 재클러스터링 → 8 clusters: Mono_CD14, Mono_FCGR3A, Mφ_THBS1, Mφ_APOE, cDC1_XCR1, cDC2_CD1C, pDC_LILRA4, DC_LAMP3.
- **목적**: 종양 vs. 주변정상 대식세포 극성 차이, LAMP3+ DC 기원 규명.
- **주요 수치**:
  - TREM2: Mφ_APOE(T) vs Mφ_APOE(P) — p < 1e-100; APOE: p < 1e-100, 1.1e-14 (Fig. 4e).
  - CD63: p < 1e-100, 6.4e-20; LAMP1: p < 1e-100, 3.0e-12 (Fig. 4e).
  - TFEC/NR1H3 과발현 THP-1 대식세포에서 APOE/APOC1 유의미한 상향 (qPCR, Fig. 4g, p = 0.020~0.052).
- **정성 결과**: RNA velocity 분석에서 LAMP3+ DC가 cDC2에서 유래한다고 추론됨 (Fig. 4i).
- **논문 주장과의 연결**: Mφ_APOE는 지질·리소솜 기능이 강화된 TAM 아형으로, TASC와 상호강화 피드백 루프를 형성해 면역억제 TME를 유지한다.

#### Dataset 5 — T세포 다양성 + Tc17 세포 특성 (T/NK compartment)

- **Dataset**: T·NK세포 재클러스터링 → 10 CD8+ 클러스터, 6 CD4+ Tconv 클러스터, 3 CD4+ Treg 클러스터, 1 cycling cluster. paired TCR sequencing 통합.
- **목적**: GC TME T세포 다양성 전체 규명; Tc17 세포 동정 및 분포; IL17 신호 경로의 종양 촉진 기전 파악.
- **주요 수치**:
  - Tc17 (CD8_C8_IL17A) 클러스터: 10명 중 8명 종양에서 >1% 비율 (Supplementary Fig. 6g).
  - IL17, IL22, IL26 공유 상향 유전자 26개 중 FC > 2, p < 0.01 유전자 다수 (Fig. 5f, Supplementary Data 4).
  - IL17RA: 종양 vs. 정상 TCGA-STAD p = 1.5e-9; IL17RB: p = 3.2e-17; IL10RB: p = 3.1e-5; IL20RA: p = 2.3e-5; IL22RA1: p = 4.8e-3 (Fig. 5h).
  - IHC 검증: anti-CD8, anti-CD4, anti-IL17A 삼중 면역형광으로 CD8+IL17+ 및 CD4+IL17+ 세포 종양 내 존재 확인 (n = 6 환자, GC988401) (Fig. 5d).
- **논문 주장과의 연결**: Tc17 세포가 종양 내 실재하고 IL17/IL22/IL26 수용체가 상향되어 있으므로, Tc17이 분비하는 사이토카인이 종양 세포와 기질세포에 직접 작용해 종양 진행을 촉진할 수 있다.

#### Dataset 6 — Tc17→exhaustion 대안 경로 (TCR clonotype + trajectory)

- **Dataset**: CD8+ T세포 clonotype-sharing matrix; diffusion map + RNA velocity (scVelo) trajectory 분석.
- **목적**: Tc17 세포가 tissue-resident memory에서 기원하고 소진 상태로 분화한다는 대안 경로 규명.
- **주요 수치**:
  - CD8_C8(Tc17)와 CD8_C9(Exhausted) 간 clonotype 공유 확인 (Fig. 6h heatmap).
  - CD8_C5(TOB1, tissue-resident) → CD8_C8(Tc17) → CD8_C9(Exhausted)의 directional stream 확인 (diffusion map, Fig. 6j right).
  - Tc17-exhaustion trajectory에서 cytolytic score 감소, exhaustion score 증가 (Gaussian process regression, 95% CI, Fig. 6m).
  - Tc17-exhaustion trajectory의 exhaustion score가 cytolytic-exhaustion trajectory보다 유의미하게 높음 (Fig. 6m).
  - CD8_C2(Effector, blood origin) → CD8_C4(Effector memory)/CD8_C9(Exhausted)의 cytolytic trajectory도 동시 확인.
- **논문 주장과의 연결**: 고전적 cytotoxic→exhaustion 경로 외에 Tc17→exhaustion이라는 독립 경로가 존재하며, 두 경로의 TF 프로그램이 다르다(EOMES vs. RUNX2).

#### Dataset 7 — 세포 간 상호작용 네트워크 (CellPhoneDB)

- **Dataset**: CellPhoneDB v2.0, permutation 1,000회, p < 0.01 기준, 10명 환자 각자 분석 후 >1 환자에서 유의한 L-R 쌍만 집계.
- **목적**: TME 내 주요 상호작용 허브 세포 규명, TASC-TAM-LAMP3+ DC의 중심성 확인.
- **주요 수치**:
  - 종양 세포는 기질세포와 상호작용이 정상 또는 종양유사 상피세포보다 많음 (Supplementary Fig. 10c).
  - NECTIN2-TIGIT 상호작용: 종양 세포, TASC, DC_LAMP3 등이 고발현 (IHC 검증, n = 6, Fig. 8g).
  - IL34-CSF1R (Mφ_APOE × TASC) 상호작용 유의 (Fig. 8a).
- **논문 주장과의 연결**: TASC, TAM(Mφ_APOE), LAMP3+ DC가 TME 내 상호작용 허브를 형성하며 면역억제 네트워크를 구성한다.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: TASC(Fib_1/Endo_1/SMC_1)와 Mφ_APOE가 종양 조직에 농축되고, T세포 억제에 관여하는 다중 L-R 쌍을 통해 연결된다.
- **가장 중요한 수치**: 166,533세포, Tc17 세포 10명 중 8명 존재, TASC 비율↑ HR = 1.8 (TCGA-STAD), IL17 수용체 유의미한 종양 상향.
- **baseline 대비 차이**: 기존 소규모 GC scRNA-seq 대비 세포 수·조직 유형·multi-omic 통합 모두 확장.
- **결과 해석 시 주의점**: 단일 기관 10명 코호트, 치료 미경험, 수술절제 조직 위주. Tc17 관련 사이토카인(IL22, IL26)의 in vivo 기능 검증 미완.

---

## Figures

### Figure 1 — 위암 TME 전체 atlas 개요

- **이 Figure가 필요한 이유**: 10명 환자의 scRNA-seq + 혈액·주변정상·종양 matched 설계에서 나온 166,533세포를 한 UMAP에 통합하고, 12 lineage가 모든 환자에서 발견됨을 보여주기 위한 출발점 Figure.
- **이 Figure가 뒷받침하는 주장**: GC TME가 복잡하고 이질적이며, 단일세포 해상도 atlas가 필요하다.

##### 패널별 설명
- a: 샘플 수집·해리·scRNA-seq·T/B세포 수용체 profiling·계통분석 전체 워크플로우.
- b: 166,533세포 UMAP, 12 major lineage 색상 구분.
- c: 12 lineage × marker gene 발현 heatmap.
- d: 12 lineage의 marker gene dot plot (발현 비율 + 표준화 발현 수준).
- e: 환자별 세포 유형 구성 비율 bar chart (GC01T~GC10T 종양; GC03T-R1/R2·GC10P-R1/R2 기술 반복).

##### 본문에서 강조한 비교
- 비교 대상: 혈액/주변정상/종양 조직 간 세포 유형 비율.
- 관찰된 차이: 내분비세포는 주로 GC07·GC08·GC10 환자 유래. 환자마다 비율이 크게 다름.
- 이 차이가 의미하는 것: 기존 bulk-seq 연구가 포착하지 못한 intertumoral heterogeneity가 세포 구성 수준에서 존재한다.

##### 해석 시 주의점
- UMAP 표현은 고차원 데이터의 2D 투영이므로 클러스터 간 거리가 생물학적 유사도를 선형적으로 나타내지 않는다.

---

### Figure 2 — 위암 상피세포 단일세포 수준 프로파일링

- **이 Figure가 필요한 이유**: 종양세포를 비종양 상피세포로부터 구분하고, 위암의 주요 병리학적 특징인 장형이형성(IM) 클러스터의 분자적 특성을 확인하기 위해.
- **이 Figure가 뒷받침하는 주장**: 종양 클러스터 동정이 CNV score·WES 돌연변이·발현 패턴의 세 증거로 일관되게 뒷받침된다. CDX2 관련 유전자가 IM의 마스터 조절인자임을 제안한다.

##### 패널별 설명
- a: 상피세포 UMAP, tumor score 색상.
- b: inferCNV score 색상 UMAP.
- c: 돌연변이 수 색상 UMAP.
- d: 정의된 상피세포 유형 (Normal, GMC, PMC, IM_enterocyte, IM_goblet, Tumor_GC07/08/10, Uncertain) UMAP.
- e: 4개 환자 각자 bulk RNA-seq log2FC vs. scRNA-seq log2FC scatter (Spearman r = 0.883/0.707/0.789/0.927).
- f: 상피세포 클러스터 marker gene dot plot.
- g: GC07과 GC10 Pearson correlation heatmap (두 환자 종양 클러스터 유사성).
- h: 상피세포 클러스터의 LYPD2·KRT7·KRT17 violin plot (scRNA-seq).
- i: GTEx 위장관 조직 LYPD2·KRT7·KRT17 violin plot (외부 검증).
- j: 클러스터별 metallothionein 관련 유전자 dot plot.
- k: bulk RNA-seq 및 TCGA-STAD metallothionein score boxplot (tumor vs. normal, p = 4.8e-3).
- l: goblet/enterocyte score violin plot (scRNA-seq).
- m: TCGA-STAD bulk RNA-seq dataset goblet/enterocyte score bar plot.
- n: CDX2 관련 유전자 combined correlation heatmap.

##### 본문에서 강조한 비교
- 비교 대상: Tumor_GC08_1 vs. Tumor_GC08_2 (같은 환자 두 부위).
- 관찰된 차이: GC08_1은 metallothionein 유전자 낮고 WES 돌연변이 농축 낮아 덜 진행된 종양 클러스터로 해석.
- 이 차이가 의미하는 것: intratumoral heterogeneity가 단일 환자 내에서도 종양 부위에 따라 다르다.

##### 해석 시 주의점
- CDX2 upstream TF(HOXA13, HNF4A 등) 기능은 과발현 실험(SGC-7901만 양성, MKN-28 음성)으로 부분 확인에 그침. 인과관계는 추가 검증 필요.

---

### Figure 3 — 기질세포 동적 재형성

- **이 Figure가 필요한 이유**: 종양 기질세포(TASC)의 분자적 특성과 예후 영향을 규명하고, CAF-Mφ 피드백 루프를 in vitro로 검증하기 위해.
- **이 Figure가 뒷받침하는 주장**: TASC(Fib_1/Endo_1/SMC_1)가 종양 진행을 촉진하는 기질세포군으로, Wnt 신호·혈관신생이 상향되고 예후와 역상관한다.

##### 패널별 설명
- a: 기질세포 UMAP (주변정상 orange / 종양 green).
- b: 기질세포 하위 클러스터 UMAP.
- c: 기질세포 marker gene dot plot.
- d: CD31+/HLA-DR+ 내피세포 multicolor IHC (종양 vs. 주변정상, n = 6, scale bar 20 µm).
- e: CD31+/FAP+ 내피세포·섬유아세포 multicolor IHC (n = 6).
- f: Endo_1 vs. 나머지 내피세포 DEG volcano plot.
- g: MHC class II+ 내피세포 비율 꺾은선 (주변정상 > 종양, p = 2.1e-6, validation cohort n = 9).
- h: FAP, BMP1, WNT5A IHC (formalin-fixed paraffin-embedded, n = 6, scale bar 100 µm).
- i: WNT2·WNT5A·SFRP1 boxplot (scRNA-seq, 종양 vs. 주변정상 섬유아세포).
- j: WNT2·WNT5A·SFRP1 TCGA-STAD TPM boxplot.
- k: 혈관신생 score violin plot (세포 유형별).
- l: Fib_1·SMC_1 Kaplan-Meier 생존 곡선 (TCGA-STAD).
- m: GC cell line 6종에서 CAFs CM 세포 증식 CCK-8 assay (p < 0.05).

##### 해석 시 주의점
- Kaplan-Meier 분석은 TASC 비율을 MuSiC deconvolution으로 bulk RNA-seq에서 추정한 값이므로 scRNA-seq 직접 계측값이 아니다. Deconvolution 오차가 HR 추정에 영향을 줄 수 있다.

---

### Figure 4 — 골수세포 이질성: 지질 관련 대식세포 확장

- **이 Figure가 필요한 이유**: Mφ_APOE 아형의 분자적 정체(지질·리소솜 기능)와 TASC와의 상호작용, LAMP3+ DC 발달 기원을 규명하기 위해.
- **이 Figure가 뒷받침하는 주장**: Mφ_APOE가 GC TME의 TAM 대표 아형으로, 지질/리소솜 기능과 면역억제 특성을 갖고 TASC와 피드백 루프를 형성한다.

##### 패널별 설명
- a: 골수세포 UMAP (8 subtype 색상 구분).
- b: 골수세포 marker gene dot plot.
- c: 경로 활성(GSVA score) heatmap (M1/M2 포함, 각 골수 클러스터).
- d: Mφ_APOE vs. Mφ_THBS1 DEG volcano plot.
- e: TREM2/APOE/CD63/LAMP1 boxplot (T vs. P 각 아형, p values).
- f: MITF regulon AUCell score + MITF/NR1H3 발현 + CD63/APOE 발현 UMAP.
- g: NR1H3·TFEC 과발현 THP-1에서 APOC1·APOE qPCR (LPS+IFNγ, Pam3CSK4 자극).
- h: DC 하위 클러스터 UMAP (RNA velocity 화살표).
- i: DC_LAMP3-LAMP3 spliced/unspliced velocity plot.

##### 해석 시 주의점
- LAMP3+ DC 기원(cDC2 유래)은 RNA velocity 기반 추론으로, 실험적 lineage tracing 없이는 인과적 확증이 어렵다.

---

### Figure 5 — T세포 다양성 및 Tc17 세포의 종양 촉진 기전

- **이 Figure가 필요한 이유**: GC TME의 T세포 이질성 전체를 분류하고, 새로 동정한 Tc17 클러스터가 IL17 신호를 통해 종양 진행에 기여한다는 주장을 뒷받침하기 위해.
- **이 Figure가 뒷받침하는 주장**: Tc17 세포가 GC 환자 대다수의 종양에 존재하고, IL17/IL22/IL26 수용체가 종양 조직에 상향되어 있어 치료 타겟이 될 수 있다.

##### 패널별 설명
- a: T세포 전체 UMAP (세포 유형 색상).
- b: 조직 기원 색상 UMAP.
- c: T세포 하위 클러스터 marker gene dot plot.
- d: CD8/CD4/IL17A 삼중 IHC (n = 6, GC988401 환자, scale bar 20 µm).
- e: Tc17 관련 KEGG 경로 enrichment bar (hypergeometric test).
- f: CD8_C9_HAVCR2 vs. CD8_C8_IL17A 상향 유전자 scatter plot.
- g: IL17RA/IL17RB/IL17RC/IL10RB/IL20RA/IL22RA1 dot plot (세포 유형별).
- h: IL17RA/IL17RB/IL17RC/IL10RB/IL20RA/IL22RA1 TCGA-STAD boxplot (종양 vs. 정상).

##### 해석 시 주의점
- Tc17 세포가 실제로 IL22/IL26을 분비해 종양 진행을 촉진한다는 직접적 in vivo 기능 실험(마우스 모델 등)은 본 논문에 없다. bulk TCGA-STAD에서 *IL22, IL26* 발현은 매우 낮아(본문 Discussion) 조직 근접 효과(paracrine effect)에 그칠 가능성이 제기된다.

---

### Figure 6 — TCR 분석 기반 CD8+ T세포 표현형 전이

- **이 Figure가 필요한 이유**: T세포 계보 추적(clonotype 공유)과 RNA velocity 두 독립 방법으로 Tc17→exhaustion alternative trajectory를 입증하기 위해.
- **이 Figure가 뒷받침하는 주장**: Tc17 세포는 tissue-resident CD8+ T세포에서 기원하고 exhausted 상태로 분화할 수 있으며, 이 경로는 cytotoxic-exhaustion 경로와 분자적으로 구별된다.

##### 패널별 설명
- a: clonotype 크기 분포 (clonal vs. non-clonal).
- b: CD8/CD4/Treg T세포 클러스터별 clonal expansion bar.
- c: CD8+ T세포 Morisita-Horn similarity index (blood vs. solid tissue).
- d: CD8+ T세포 하위 클러스터의 세포 이동 관련 경로 GSVA score heatmap.
- e: T세포 클러스터별 clonotype 분포 bar (10명 모두 포함).
- f: CD8+ T세포 같은 클론에서 나온 세포 비율 비교 (실측 vs. permutation, p < 1e-100).
- g: T세포 클러스터 3D VDJ gene usage PCA.
- h: CD8 T세포 inter-cluster clonotype sharing 비율 heatmap.
- i: 선택된 clonotype 세포 UMAP (6개 주요 clonotype 색상).
- j: diffusion map + RNA velocity (cytolytic trajectory left, Tc17 trajectory right).
- k: pseudotime diffusion map (두 trajectory).
- l: cytolytic score·exhaustion score violin plot (CD8 clusters, cytolytic trajectory).
- m: cytolytic/exhaustion score Gaussian process regression 곡선 (pseudotime, 두 trajectory 비교).

##### 해석 시 주의점
- Diffusion map pseudotime은 데이터 내재적 구조에서 추론된 것으로, 실제 시간 경과나 세포 분화 순서를 인과적으로 증명하지 않는다. Clonotype 공유도 연결 가능성을 보여줄 뿐 실제 분화 경로를 직접 증명하지는 않는다.

---

### Figure 7 — T세포 소진 trajectory를 따른 TF 활성 역학

- **이 Figure가 필요한 이유**: 두 소진 경로(cytolytic, Tc17)를 구별하는 TF 조절 프로그램을 SCENIC으로 규명하고, Tc17이 종양 진행에 주는 잠재 영향을 TF 수준에서 설명하기 위해.
- **이 Figure가 뒷받침하는 주장**: 두 exhaustion trajectory가 서로 다른 TF 프로그램을 가지므로 기능적으로 구별되며, Tc17 trajectory에서 *RUNX2*가 잠재적 key regulator다.

##### 패널별 설명
- a: KRT86 imputed expression curve (pseudotime, 두 trajectory, Gaussian process).
- b: UMAP에서 KRT86 발현.
- c: 두 trajectory별 highly variable TF heatmap (cytolytic: EOMES/STAT1 rich; Tc17: NR4A2/RUNX2/RORC/ATF3 rich).
- d: CD8 T세포 하위 클러스터별 TF regulon AUCell score dot plot.
- e: EOMES·RUNX2 AUCell score Gaussian process curve (pseudotime, 두 trajectory).
- f: EOMES·RUNX2 발현 UMAP.

##### 해석 시 주의점
- EOMES, RUNX2를 두 경로의 key regulator로 제안하지만, CRISPR 또는 shRNA 기반 in vitro/in vivo 기능 검증 없이 SCENIC 상관분석에 기반한 주장이다.

---

### Figure 8 — 세포 간 상호작용 네트워크가 종양 진행에 기여

- **이 Figure가 필요한 이유**: CellPhoneDB L-R 분석으로 TME 내 주요 상호작용 허브를 정량화하고, 특히 TASC-Mφ_APOE-LAMP3+ DC의 면역억제 역할을 구체적 L-R 쌍으로 설명하기 위해.
- **이 Figure가 뒷받침하는 주장**: TASC, Mφ_APOE, DC_LAMP3가 TME 내 상호작용 허브를 형성하여 T세포 억제와 면역 회피를 촉진한다.

##### 패널별 설명
- a: 선택된 L-R 쌍 dot plot (세포 유형 쌍 × L-R pair, color = significant patient 비율).
- b: Endo_1·Fib_1·SMC_1 선택 L-R 쌍 발현 heatmap (Notch/PDGF/Chemokine/VEGFA 경로).
- c: 세포 유형 간 추정 비율 Spearman correlation heatmap (TCGA-STAD).
- d: CAFs CM으로 유도된 THP-1 macrophage의 Mφ_APOE·Mφ_THBS1 마커 발현 heatmap (시간별 24~72h).
- e: Mφ_APOE·Mφ_THBS1 score bar (CAFs CM vs. Transwell_CAFs vs. Standard Medium, n = 2~3).
- f: 림프구-기타 세포 L-R 쌍 heatmap.
- g: NECTIN2+/TIGIT+ IHC (n = 6, GC769812 환자, scale bar 20 µm).

##### 해석 시 주의점
- CellPhoneDB 결과는 실제 세포 접촉이나 신호전달을 증명하지 않는다. In vitro CAFs CM 실험(Fig. 8d-e)이 TASC→Mφ_APOE 유도를 부분 검증하지만 실험 수(n = 2~3)가 적다.

---

## Tables

본문에 정식 Table 없음. 모든 정량 데이터는 Figure panel 또는 Supplementary Data(xlsx) 형태로 제공됨.

Supplementary Table 1: 상피세포 유형별 signature gene 목록 (`41467_2022_32627_MOESM4_ESM.xlsx`).
Supplementary Table 2: 실험에 사용된 primer sequences (`41467_2022_32627_MOESM5_ESM.xlsx`).

---

## Supplementary Information

- **Supplementary Methods** (MOESM1_ESM.pdf p2-5): bulk RNA-seq/WES library prep (NEB 키트), CAF conditioned medium 준비, CCK-8 assay 프로토콜, THP-1 자극 실험, RNA 추출 및 qPCR 상세 프로토콜.
- **Supplementary Figures 1-18** (MOESM1_ESM.pdf): Supp Fig 1 (QC, sample 분포), Supp Fig 2 (inferCNV), Supp Fig 3-4 (기질세포), Supp Fig 5 (골수세포), Supp Fig 6-7 (T세포), Supp Fig 8 (TCR), Supp Fig 9 (velocity trajectory), Supp Fig 10-11 (CellPhoneDB), Supp Fig 12 (NK/NKT/γδ T/B세포), Supp Fig 13 (환자 효과 평가), Supp Fig 14 (세포 품질), Supp Fig 15 (T세포 클러스터 robustness), Supp Fig 16 (WES), Supp Fig 17-18 (Western blot uncropped).
- **Supplementary Notes**: Note 1 (배치효과 평가), Note 2 (T세포 클러스터 robustness), Note 3 (GC08 Wnt 신호 이상 case study).
- **Supplementary Data 1-8** (xlsx): 환자 임상정보, doublet 마커, DEG 목록, Tex/Tc17 공통 유전자, VDJ usage matrix, L-R interaction pairs, IHC 항체 목록, 악성/비악성 gene set.

---

## 분석 자체에 대한 메모

- 본 논문 제목에 "early-relapse hepatocellular carcinoma"라는 설명이 사용자 프롬프트에 포함되어 있었으나, 실제 논문은 **위암(gastric cancer) TME** 분석 논문임. 사용자 프롬프트 오기입 가능성 있음 — paper-info.yaml 및 분석 노트에는 원문 기반으로 위암으로 정확히 기재.
- 검토필요: TCGA-STAD 생존 분석에서 cell type proportion 추정에 MuSiC deconvolution을 사용했는데, scRNA-seq reference panel이 동일 데이터셋 기반이므로 circular bias 가능성이 있음.
- 검토필요: Tc17 세포와 Th17 세포 간 공통 유전자 목록(Supplementary Data 4)을 검토하면 기능 중복 해석에 도움이 될 것.
- 질문: Tc17 세포가 IL22/IL26을 실제로 분비하는지 단일세포 수준의 cytokine protein measurement (예: intracellular staining, CyTOF)로 확인된 바 있는가? 추가 문헌 확인 필요.
