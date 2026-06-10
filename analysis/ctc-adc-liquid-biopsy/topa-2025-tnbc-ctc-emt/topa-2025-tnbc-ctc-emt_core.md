# topa-2025-tnbc-ctc-emt — Core Analysis

---

## Executive Summary

- **무엇**: 전이성 유방암 환자 33명을 대상으로 TROP2 또는 HER2 타깃 ADC 치료 중 CTC를 연속 채혈하여, epitope 발현이 ADC 획득 내성의 주요 원인인지 최초로 전향적으로 추적한 연구.
- **모델 / 방법**: CTC-iChip (음성 면역자기 농축, epitope-agnostic) + PhenoImager 40× multispectral imaging → 단일 CTC별 TROP2·HER2 발현 정량화. 치료 전(D0) · 치료 3주 후(~D21) · 진행 시점의 3-timepoint 직렬 설계.
- **핵심 결과**:
  - ① TROP2-ADC: Day 21 CTC ≥80% 감소 시 median TTP 391 vs. 97일 (HR 4.15, p=0.0046)
  - ② HER2-ADC: Day 21 CTC ≥80% 감소 시 median TTP 322 vs. 66일 (HR 9.12, p=0.0002)
  - ③ 진행 시 CTC TROP2 발현 유지 또는 증가 (9명 중 8명 = 89%); HER2도 7명 중 5명(71%) 변화 없음
  - ④ Epitope switching (동일 TOP1 inhibitor payload) 2차 ADC: median TTP 90일 vs. 1차 229일 (p=0.0006)
- **우리 적용**: ADC pipeline에서 TROP2/HER2 발현 기반 patient selection 전략 재고 근거. CTC 조기 감소를 on-treatment response biomarker로 채용하는 시나리오 검토 가능 (pipeline-applicable / BD-opportunity).
- **심층**: 학술·산업 한계는 `topa-2025-tnbc-ctc-emt_lens-academic.md` / `topa-2025-tnbc-ctc-emt_lens-industry.md` / `topa-2025-tnbc-ctc-emt_methodology-brief.md` 참고.

---

## Identity

- **Title**: Epitope Expression Persists in Circulating Tumor Cells as Breast Cancers Acquire Resistance to Antibody Drug Conjugates
- **Authors**: Avanish Mishra#, Rachel Abelman#, Quinn Cunneely#, Victor Putaturo, Akansha A. Deshpande, Remy Bell, Elizabeth M. Seider, Katherine H. Xu, Mythreayi Shan, Justin Kelly, Shih-Bo Huang, Kaustav A. Gopinathan, Kruthika Kikkeri, Jon F. Edd, John Walsh, Charles S. Dai, Leif Ellisen, David T. Ting, Linda Nieman, Mehmet Toner, Aditya Bardia, Daniel A. Haber\*, Shyalamala Maheswaran\* (#: equal contribution; *: co-corresponding)
- **Affiliations**: Center for Engineering in Medicine and Surgery (MGH/Harvard Medical School); Krantz Family Center for Cancer Research (MGH Cancer Center/Harvard Medical School); Division of Hematology Oncology (MGH/Harvard Medical School); Howard Hughes Medical Institute; Shriners Children's Hospital Boston
- **Year**: 2025 (posted April 3, 2025)
- **Venue**: bioRxiv preprint (not peer-reviewed at time of analysis)
- **DOI**: 10.1101/2025.04.02.646822
- **Citation key**: mishra2025epitope
- **COI**: M.T., D.A.H., S.M., D.T.T.는 CTC-iChip 기술을 상용화하는 TellBio의 공동창업자. Massachusetts General Hospital has patent protection on the inertial separation array and inertial focusing microfluidic technologies.
- **Funding**: NIH (K25HL169816, RO1CA129933, U01CA214297, R21CA260989, R01CA255602), Howard Hughes Medical Institute, Breast Cancer Research Foundation, National Foundation for Cancer Research.

---

## Background

### 배경 스토리

- **문제의 출발점**: ADC (antibody-drug conjugate, 항체-약물 접합체)는 종양 세포 표면 항원을 표적 삼아 세포독성 payload를 선택적으로 전달하는 기전으로, TROP2와 HER2를 타깃하는 ADC 3종 — sacituzumab govitecan (SG), datopotamab deruxtecan (Dato-DXd), trastuzumab deruxtecan (T-DXd) — 이 전이성 유방암에 FDA 승인을 받았다. 그러나 초기 반응 후 내성 획득이 빠르며, 1차 ADC 치료 후 2차 ADC에서 치료 지속 기간이 유의미하게 단축된다는 후향적 관찰 데이터가 축적되고 있다 (refs. 11–13).

- **선행 접근 A — 조직 생검 기반 epitope scoring**: TROP2 발현 정도가 SG 반응을 예측할 것이라는 가정 하에 tumor biopsy IHC가 biomarker 전략으로 시도되었다. 그러나 ASCENT 등 phase 3 시험의 biomarker 분석에서 TROP2 발현 수준은 임상 반응과 유의한 상관을 보이지 않았다 (refs. 19–21). HER2에서도 T-DXd가 HER2-low (median PFS 9.9 vs. 5.1개월, HR 0.5, p<0.001) 및 HER2-ultralow 환자군에서 유효성을 보이면서 (refs. 6, 23, 24) epitope 의존적 selectivity 가정이 흔들렸다.

- **A의 한계**: 조직 생검은 (1) 단일 병소에서만 채취되어 전이 병소 전체의 공간적 이질성을 반영하지 못하고, (2) 치료 중 동적 변화를 추적할 수 없다. 특히 유방암에서 흔한 뼈 전이는 석회화 제거 과정으로 인해 IHC 정량이 부정확해진다.

- **선행 접근 B — CTC 기반 액체 생검**: CTC는 혈액으로 유리되어 전체 종양 부담을 대변하며, 단일 세포 분해능으로 이질성을 파악할 수 있다. 그러나 EpCAM 기반 CellSearch 등 기존 플랫폼은 epithelial marker를 co-express하지 않는 CTC에 대한 선택 편향을 유발하고 (EMT를 겪은 mesenchymal CTC 누락), 크기 기반 분리는 직경이 백혈구와 겹치는 약 65%의 CTC를 검출하지 못한다 (ref. 28).

- **이 논문으로 이어지는 gap**: ADC 치료 중 TROP2·HER2 epitope 발현이 내성 획득 시점에 실제로 변하는지, 그리고 CTC가 이 변화를 serial monitoring으로 포착할 수 있는지를 전향적으로 검증한 데이터가 전무하다.

### 기본 개념

- **ADC 기전**: 항체 → 종양 표면 epitope 결합 → 내재화(internalization) → payload 방출 → 세포사. SG/Dato-DXd/T-DXd 모두 topoisomerase I (TOP1) 억제제 계열 payload (camptothecin 관련 화합물)를 공유한다. "Bystander effect"는 ADC를 흡수한 세포 주변의 항원 음성 세포도 방출된 payload로 사멸하는 현상 — SG의 linker가 spontaneous hydrolysis에 susceptible하여 이 효과가 크다고 알려져 있다 (ref. 2).
- **CTC-iChip**: 음성 선택(negative selection) 기반 미세유체 CTC 농축 장치. 관성 분리 어레이로 RBC·혈소판 제거 → 자기 표지 WBC (CD45/CD16/CD66b-biotinylated Ab + Dynabeads T1) 분리 → 비표지 CTC 수집. EpCAM 비의존적이므로 epithelial/mesenchymal 모든 CTC를 포함한다.
- **Multispectral imaging**: 여러 형광 채널 동시 획득 + spectral unmixing으로 교차 형광 보정. DAPI / AF488 (EpCAM/panCK/CK19) / AF555 (TROP2) / AF594 (HER2) / AF647 (CD45/CD16/CD66b) 동시 측정. 40× 분해능(0.25 μm/pixel)으로 단일 세포 수준 정량.
- **H-score**: $\text{H-score} = 1 \times P_{Low} + 2 \times P_{Medium} + 3 \times P_{High}$. 발현 분포의 방향성 변화를 한 수치로 포착. 0(전체 null)~3(전체 high) 범위.

### 이 논문의 필요성

- **핵심 이유**: FDA 승인 TROP2/HER2 ADC가 epitope 발현과 무관하게 유효성을 보이는 역설적 임상 관찰이 축적되면서, "내성 획득 시 epitope가 하향조절되는가"를 전향적으로 검증할 데이터가 요구됨.
- **기존 방법으로 부족했던 지점**: 조직 생검은 공간·시간적 이질성을 반영 못 하고, 기존 CTC platform은 epithelial marker 의존 편향으로 ADC 연구에 적합하지 않음.
- **이 논문이 해결하려는 방향**: EpCAM-agnostic CTC-iChip + multispectral imaging으로 치료 전·중·진행 시점의 TROP2·HER2 발현을 단일 CTC 수준에서 직렬 추적하여 내성 기전에서의 역할을 규명.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 전이성 유방암 환자의 ADC 치료 과정에서 (1) 기저 CTC TROP2/HER2 발현이 반응을 예측하는지, (2) 진행 시점에 epitope 발현이 변화하는지, (3) 동일 payload 계열 순차 ADC가 교차 내성을 나타내는지를 정량적으로 검증.
- **입력**: 전혈 20 mL (Streck tubes 고정), 복수 시간점 (D0, ~D21, 진행 시).
- **출력**: CTC 수(/20 mL), 각 CTC의 TROP2 및/또는 HER2 발현 class (Null/Low/Medium/High), H-score, 임상 outcome (TTP).
- **추정 대상**: CTC 발현 분포 변화 (ΔH-score), CTC 수 변화율, 기저 발현과 반응 간 상관.
- **중요한 hidden assumption**: CTC가 전체 전이 부담을 대표한다는 가정; EpCAM-agnostic 포획이 모든 관련 CTC 하위군을 포함한다는 가정.

### 플랫폼 및 측정 절차

**CTC-iChip 처리**: 의료 등급 cyclic olefin copolymer (COC) 재질, Stratec Biomedical 제조. 혈액 1:1 buffer 희석 후 압력 구동 flow. 관성 분리 어레이 16개로 RBC·혈소판·비결합 beads 제거 → 2단계 자기 분리로 CD45/CD16/CD66b-biotinylated Ab + 1 μm Dynabeads MyOne Streptavidin T1 표지 WBC 제거. 72시간 Streck 고정 후 처리 가능 (기존 즉시 처리 대비 workflow 확장). 최적화 조건: Ab·bead 농도 4배 감소 → CTC 회수율 96.9±5.1% 유지, Log₁₀ WBC 감소 2.88±0.56, Log₁₀ RBC 감소 4.19±0.47.

**Staining**: EpCAM (Cell Signaling 5198S) / pan-CK CK8/18 (Cell Signaling 4523S) / CK19 (Thermo Fisher MA5-18158) → AF488; TROP2 (Novus NBP2-89492R, -89493R) → Dyite-550 또는 AF555 (abcam ab214488, ab150078); HER2 (abcam ab11710, ab150160) → AF594; CD45/CD16/CD66b → AF647; DAPI (ThermoFisher 62248). Blocking: 3% BSA + 2% Normal Goat Serum, 1 hr. FFPE 조직은 Leica Bond RX 자동 염색기, HIER Bond ER2 (Tris-EDTA pH 9.0) 40분.

**Imaging 및 분석**: Akoya PhenoImager 40× (0.25 μm/pixel), 8-bit (0–255), DAPI/AF488/AF555/AF594/AF647 채널. Spectral unmixing: Akoya InForm. Segmentation: HALO image analysis. 독립 연구원 2인 이상 수동 검증. CTC = DAPI+, EpCAM/panCK/CK19+, CD45/66b/16-, intact nucleated cell.

**발현 class 경계**: Cell line calibrators로 quartile 결정. TROP2: BRx-142 (high), AU565 (medium), MDA-MB-231 (low), Mel-167 (null). HER2: AU565 (high), BRx-142 (medium), MDA-MB-231 (low), Mel-167 (null). 환자별 분석마다 동일 cell line 조건으로 표준화. $\text{H-score} = 1 \times P_{Low} + 2 \times P_{Medium} + 3 \times P_{High}$.

### 코호트 설계

- **ADC 코호트**: MGH IRB DF-HCC protocol 13-416 승인, 전원 informed consent. 전이성 유방암 TROP2-ADC (n=17) 또는 HER2-ADC (n=13) 치료 시작 환자, 총 33명 / 36 치료 course. 전원 여성.
- **반응 분류**: 치료 지속 >6개월 = strong response; ≤6개월 = poor response.
- **시간점**: baseline D0, ~Day 21 (첫 2주기 후), 진행 또는 치료 중단 시점.
- **Concordance 서브세트**: 7명에서 matched CTC + 전이 조직 생검 (4명은 ADC 치료 전, 채취 간격 ≤3개월).

### 통계

- Kaplan-Meier + Log-rank test (TTP 비교)
- Fisher's exact test (matched pre/post H-score 변화 유의성)
- Pearson r (TROP2–HER2 coexpression 상관)
- Welch's T-test (1차 vs. 2차 ADC TTP 비교)
- 다중 비교 보정: 본문에 명시 없음 (미제공)

### Method 관점의 한계

- **CTC 수 부족**: 일부 환자 CTC ≤8개 → 발현 이질성 대표성 낮음. Concordance 불일치 4건 모두 CTC 수 부족 원인.
- **소규모 matched cohort**: 진행 시 matched sample n=9 (TROP2), n=7 (HER2) — 통계 power 제한.
- **Cell-line calibration 고정**: 발현 class 경계가 4종 세포주 기반으로 고정되어 환자 간 절대 형광 강도 차이를 완전 표준화하기 어려움.
- **FFPE vs. cytospin 비교**: 조직(FFPE)과 CTC(cytospin)의 전처리 차이로 정량 비교에 체계적 오차 개입 가능.
- **단일 기관**: MGH 단독 전향적 관찰 코호트; 독립 검증 코호트 없음.

---

## Results

### Dataset별 결과

#### Dataset 1 — Concordance cohort (CTC vs. matched tumor biopsy, n=7 patients)

- **Dataset**: 전이성 유방암 7명, 각각 matched 조직 생검 + 혈액 CTC (간격 ≤3개월). 4명은 ADC 치료 전.
- **목적**: CTC multispectral imaging이 조직 생검의 TROP2·HER2 발현을 대리할 수 있는지 concordance 검증.
- **데이터 규모**: 단일세포 수 — MGH002: biopsy 24,356 / CTC 8; 039: 14,720/166; 040: 11,704/3; 041: 5,637/4; 022: 5,061/18; 042: 2,163/49; 043: 5,617/8.
- **주요 수치**:
  - TROP2 concordance: 7쌍 중 4쌍 concordant positive (57%); 14쌍(7명×2 epitope) 전체 기준 10쌍(71%) concordant.
  - HER2 concordance: 7쌍 중 6쌍(86%) concordant.
  - 불일치 4건: MGH040(TROP2+HER2), 041(TROP2), 042(TROP2) — 모두 CTC 수 3–4개로 부족.
- **정성 결과**: 모든 조직 샘플에서 null–high 전 class의 세포가 혼재하는 단일 세포 수준 이질성 확인.
- **논문 주장과의 연결**: CTC imaging과 조직 생검 간 대체적 일치 → 혈액 기반 ADC epitope scoring 플랫폼으로서 CTC 유효성 개념 증명.

#### Dataset 2 — TROP2-ADC cohort (n=17 patients)

- **Dataset**: 전이성 유방암, TROP2-targeting ADC 치료 시작 17명. 주로 SG.
- **목적**: 기저 TROP2 CTC 발현이 반응 예측 인자인지; Day 21 CTC 감소가 반응 예측 인자인지.
- **데이터 규모**: 17명; baseline CTC 검출 13명(76.5%; mean 85±117 CTCs/20 mL; median 34/20 mL). 4명 baseline 0 → 전원 strong response.
- **주요 수치**:
  - Day 21 CTC ≥80% 감소 군 (n=11): strong response 9명(82%), median TTP 391일
  - Day 21 CTC <80% 감소 또는 증가 군 (n=4): strong response 0명(0%), median TTP 97일
  - HR 4.15 (95% CI 0.65–26.35), p=0.0046 (Log-rank)
  - 기저 TROP2 ≥5% Medium/High CTC (n=4중 3명=75% strong) vs. <5% (n=9중 2명=22% strong) — 통계적 유의성 미달.
- **정성 결과**: 기저 TROP2 발현 분포는 TTP와 명확한 상관 없음.
- 해석: HR의 CI 하한(0.65)이 1 미만이어서 point estimate 95% 신뢰 구간 안에 null effect 포함. 소규모 코호트 한계.

#### Dataset 3 — HER2-ADC cohort (n=13 patients)

- **Dataset**: HR+/HER2- 전이성 유방암, T-DXd 치료 시작 13명.
- **목적**: HER2-ADC에서 동일 패턴 재현 검증.
- **데이터 규모**: 13명; strong 7명(54%), poor 6명(46%).
- **주요 수치**:
  - Day 21 CTC ≥80% 감소 군 (n=8): strong response 7명(77.8%), median TTP 322일
  - CTC <80% 감소 군 (n=3): strong response 0명(0%), median TTP 66일
  - HR 9.12 (95% CI 0.58–145.4), p=0.0002 (Log-rank)
  - 해석: p값은 강하지만 CI 하한 0.58로 1 미만. n=8 vs. 3으로 KM 추정 불안정.
- **정성 결과**: 기저 HER2 CTC 발현과 TTP 간 상관 없음. 기존 IHC 조직 결과도 반응 상관 없음 (Supplementary Figure 3).

#### Dataset 4 — Progression cohort (matched pre/post ADC, TROP2 n=9, HER2 n=7)

- **Dataset**: ADC 치료 후 질환 진행한 환자의 matched baseline + 진행 시 CTC 쌍 분석.
- **목적**: Epitope 하향조절이 획득 내성의 원인인지 직접 검증.
- **주요 수치**:
  - TROP2: 9명 중 8명(89%) → 진행 시 발현 분포 기저와 comparable (ΔH-score <1). 1명(MGH009, 550일 반응 후 진행) — TROP2 유의미한 증가.
  - HER2: 7명 중 5명(71%) 변화 없음; 1명(14%) 증가; 1명(14%) 감소.
  - 통계: Fisher's exact test. 유의미한 ΔH-score(>1): TROP2 1/9, HER2 2/7.
- **정성 결과**: 진행 시 CTC 형태 및 CTC clustering 패턴이 치료 전과 유사하게 유지됨 (Figure 4C, F).

#### Dataset 5 — Sequential ADC cohort (n=6 patients)

- **Dataset**: 1차 ADC 진행 후 epitope switch (동일 TOP1 inhibitor payload, 다른 항체) 2차 ADC — TROP2→HER2 (n=4) 또는 HER2→TROP2 (n=2).
- **목적**: Epitope switching이 교차 내성을 극복하는지 검증.
- **주요 수치**:
  - 6명 전원 poor response (<6개월)
  - Median TTP: 2차 ADC 90일 vs. 1차 ADC naive cohort 229일, p=0.0006 (Welch's T-test)
  - 해석: n=6으로 소규모. Payload cross-resistance를 지지하는 핵심 관찰이나 교란 변수(환자 특성, 치료 이력) 통제 불충분.

#### Dataset 6 — TROP2–HER2 coexpression (n=7 ADC-naive cases)

- **Dataset**: ADC 치료 전 7명의 단일 CTC 및 tumor biopsy cell에서 TROP2·HER2 동시 측정.
- **주요 수치**:
  - Single CTC: Pearson r = 0.49 (P < 0.0001)
  - Single tumor biopsy cell: r = 0.68 (P < 0.0001)
- **정성 결과**: 두 epitope는 중등도 양의 상관. Epitope switching 시 같은 세포군을 재타깃하게 됨을 시사.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 기저 epitope 발현 수준은 TROP2, HER2 ADC 모두에서 반응 예측에 유용하지 않다. 치료 3주 후 CTC 급감(≥80%)은 두 ADC 코호트 모두에서 durable response와 강하게 연관된다. 진행 시 epitope는 대부분 유지되거나 오히려 증가한다.
- **가장 중요한 수치**: TROP2-ADC HR 4.15 (p=0.0046); HER2-ADC HR 9.12 (p=0.0002) — CTC 조기 감소의 예측력; sequential ADC TTP 90 vs. 229일 (p=0.0006) — payload cross-resistance 관찰.
- **결과 해석 시 주의점**: 모든 코호트 소규모(최대 n=17). HR 신뢰구간이 1을 포함 — effect size 추정 정밀도 낮음. 단일 기관 비무작위 관찰 연구. 다중 비교 보정 여부 미명시.

---

## Figures

#### Figure 1
- **이 Figure가 필요한 이유**: CTC-iChip 플랫폼 workflow 전체를 보여주어 기술적 신뢰성을 제공. EpCAM-independent CTC isolation이 epitope-unbiased ADC target scoring을 가능하게 한다는 전제 조건 시각화.
- **이 Figure가 뒷받침하는 주장**: 방법의 타당성.

##### 패널별 설명
- (단일 schematic 패널): 상단 — Fixed Blood → CTC Isolation (CTC-iChip) → Enriched CTCs → Staining → Multispectral Imaging → Epitope Quantitation. 하단 inset — CTC-iChip의 두 단계 설계: (1) RBC/platelet 관성 분리 어레이(16 units); (2) 자기 WBC 분리 채널 (inertial focusing → magnetic sorting). 색상: 녹색=CTC, 분홍=WBC, 적색=RBC/platelet.

##### 본문에서 강조한 비교
- 기존 EpCAM 기반 방법과 달리 CTC-iChip은 epithelial/mesenchymal 무관하게 CTC를 회수 → TROP2·HER2 발현 측정 시 선택 편향 없음.

##### 해석 시 주의점
- 개념 도식. 실제 회수율 데이터는 Supplementary Figure 1에 제시. 독립 기관 검증 없음.

---

#### Figure 2
- **이 Figure가 필요한 이유**: CTC와 조직 생검 간 concordance를 보여야만 이후 CTC-only 코호트 결과가 임상적으로 유효한 의미를 가짐.
- **이 Figure가 뒷받침하는 주장**: CTC multispectral imaging은 matched 조직 생검과 유사한 TROP2·HER2 발현 분포를 보인다 (concordance 71–86%).

##### 패널별 설명
- **A**: 대표 CTC 이미지 4종 (WBC negative control, TROP2+, HER2+, TROP2+/HER2+ double positive). 4채널 (DAPI-파랑, EpCAM/CK-초록, HER2-주황, TROP2-노랑, CD45-빨강). Scale bar 10 μm.
- **B**: 전이 조직 생검 TROP2+/HER2+ 예시 이미지 (동일 항체 cocktail).
- **C**: 7명 matched case의 TROP2 발현 violin plot — CTC(circles) vs. tissue(triangles). 색상=class (null-blue → high-red). Concordance(+)/discordance(-) 표시.
- **D**: HER2 concordance plot (동일 구조).
  - 단일세포 수: MGH002(biopsy 24,356/CTC 8), 039(14,720/166), 040(11,704/3), 041(5,637/4), 022(5,061/18), 042(2,163/49), 043(5,617/8).

##### 본문에서 강조한 비교
- 14쌍 중 10쌍(71%) concordant. 불일치 3건(TROP2)은 모두 CTC 수 부족(MGH040: 3개, 041: 4개, 042: 49개이나 발현 low). HER2 불일치 1건(MGH040, CTC 3개).

##### 해석 시 주의점
- CTC 수 ≤8인 경우(MGH002, 040, 041, 043) concordance 통계적 대표성 낮음. CTC는 전체 전이 병소의 부분 sampling이므로 단일 생검과의 불일치가 기술적 오류인지 진정한 heterogeneity인지 구분 어려움.

---

#### Figure 3
- **이 Figure가 필요한 이유**: CTC 기반 on-treatment biomarker(Day 21 감소)가 임상 반응을 예측한다는 핵심 주장을 TROP2·HER2 두 ADC 코호트에서 병렬로 제시.
- **이 Figure가 뒷받침하는 주장**: 치료 3주 후 CTC 급감이 durable response의 조기 marker다.

##### 패널별 설명
- **A**: TROP2-ADC 17명 환자별 3-column swimmer chart. 좌측 = baseline CTC count + TROP2 expression stacked bar; 중간 = Day 21 % drop heatmap; 우측 = TTP swimmer bar (색=endpoint status: On Tx/Progression/Deceased/No CTCs Observed).
- **B**: TROP2-ADC Kaplan-Meier TTP. Blue = ≥80% drop (n=11), Red = <80% drop (n=4), dashed = no second draw (n=2). Log-rank p=0.0046, HR 4.15 (95% CI 0.65–26.35). 6-month hashed line.
- **C**: HER2-ADC 13명 swimmer chart (동일 구조). "Not Stained for HER2" 항목 추가.
- **D**: HER2-ADC KM plot. Blue ≥80% (n=8), Red <80% (n=3), no second draw (n=1). p=0.0002, HR 9.12 (95% CI 0.58–145.4).

##### 본문에서 강조한 비교
- TROP2-ADC: Day 21 ≥80% 감소 11명 중 9명(82%) strong; <80% 4명 중 0명(0%) strong.
- HER2-ADC: ≥80% 감소 8명 중 7명(77.8%) strong; <80% 3명 중 0명(0%) strong.

##### 해석 시 주의점
- HR CI가 매우 넓음 (TROP2: 0.65–26.35; HER2: 0.58–145.4). 방사선학적 반응 평가 대신 "치료 지속 기간"을 surrogate로 사용. Censoring이 많아 KM 추정 불안정.

---

#### Figure 4
- **이 Figure가 필요한 이유**: 논문의 가장 핵심 주장 — "획득 내성 시 epitope 하향조절 없음" — 을 환자별 longitudinal paired data로 직접 증명.
- **이 Figure가 뒷받침하는 주장**: TROP2 및 HER2 epitope는 ADC 획득 내성 시점에도 감소하지 않으며, 일부는 증가한다.

##### 패널별 설명
- **A**: TROP2-ADC 9명 — baseline vs. progression 시 TROP2 발현 class 비율 stacked bar (null/low/medium/high). 아래 = CTC count/20 mL, timepoint.
- **B**: ΔH-score (X축) vs. $-\log_{10}$(p-value) Fisher's exact test (Y축) 산점도. MGH009만 ΔH-score >1 (우측). 나머지 8명 |ΔH| <1.
- **C**: 대표 이미지 MGH002, MGH003, MGH007 — pre-therapy vs. post-therapy CTCs. 형태 및 발현 시각적 유사성 확인.
- **D**: HER2-ADC 7명 — 동일 구조 stacked bar.
- **E**: HER2 ΔH-score 산점도. 1명 유의한 감소, 1명 증가, 5명 변화 없음.
- **F**: HER2 pre/post representative images — MGH006, MGH022, MGH033.

##### 본문에서 강조한 비교
- TROP2 9명 중 8명 |ΔH-score| ≤1 → Fisher's test 유의성 없음. MGH009만 예외(550일 반응 후 오히려 TROP2 증가).
- HER2 7명 중 5명 변화 없음.

##### 해석 시 주의점
- n이 작아 통계적 power 제한. Fisher's test는 분포 shift 방향을 분리 검증하지 않음. 진행 시 CTC가 혈중으로 선택적 shed되는 세포를 반영하는지 불확실 — 내성 세포 전체를 대표하지 못할 수 있음.

---

#### Figure 5
- **이 Figure가 필요한 이유**: Sequential ADC (epitope switching, same payload)가 교차 내성을 일으킨다는 관찰로 payload-driven resistance hypothesis를 뒷받침.
- **이 Figure가 뒷받침하는 주장**: 동일 payload 유지 + epitope 교체 2차 ADC는 1차 ADC 대비 현저히 짧은 반응을 보인다.

##### 패널별 설명
- **A**: HER2-ADC → TROP2-ADC switch 2명 swimmer plot (MGH014, MGH005).
- **B**: TROP2-ADC → HER2-ADC switch 4명 swimmer plot (MGH021, MGH006, MGH007, MGH008).
- **C**: 2차 ADC (ADC-after-ADC, n=6) vs. 1차 ADC naive (TROP2 n=17, HER2 n=13) TTP 산점도. Median: 2차 90일, 1차 229일. p=0.0006 (Welch's T-test).
- **D**: Single CTC에서 HER2 vs. TROP2 intensity 산점도, r=0.49, P<0.0001.
- **E**: Single tumor biopsy cell HER2 vs. TROP2 intensity, r=0.68, P<0.0001.

##### 본문에서 강조한 비교
- 6명 모두 2차 ADC에서 poor response. 두 그룹(TROP2→HER2, HER2→TROP2) 공통으로 payload class (TOP1 inhibitor)가 동일. 저자는 payload resistance가 primary driver라고 결론.

##### 해석 시 주의점
- n=6 매우 소규모. Randomized cross-over 설계 아님. 두 ADC 모두 TOP1 inhibitor payload → "epitope switching 효과"를 payload 영향에서 독립적으로 평가 불가. Panel D, E의 TROP2–HER2 coexpression (r=0.49/0.68)은 intermediate 상관이므로 two epitopes가 완전 중첩 세포군을 타깃하지 않음 — 이 데이터만으로 epitope switching 실패를 설명하기에는 불충분.

---

## Tables

본문에 정식 Table 없음. Supplementary Table 1 (항체·시약 목록) 및 Supplementary Table 2 (TROP2-ADC 환자 17명 특성)가 언급. 핵심 정량 데이터는 Figure의 swimmer plot, KM curve, scatter plot으로 제시됨.

---

## Supplementary Information

- **Supplementary Figure 1A**: Streck tubes 72시간 고정 후 CTC 안정성 데이터.
- **Supplementary Figure 1B**: WBC-tagging Ab·bead 4배 희석 조건에서 CTC 회수율 96.9±5.1% 유지 + purity 확인.
- **Supplementary Figure 2**: 세포주 calibrator 기반 TROP2·HER2 발현 class 경계 설정 (violin plot에 cutoff 오버레이). BRx-142, AU565, MDA-MB-231, Mel-167 포함.
- **Supplementary Figure 3**: 조직 HER2 IHC standard clinical scoring과 T-DXd 반응 간 상관 부재 재확인.
- **Supplementary Table 1**: ADC 분석 사용 항체·시약 목록.
- **Supplementary Table 2**: TROP2-ADC 코호트 17명 환자 특성 세부 목록.
- **Data availability**: 모든 이미지·데이터는 Open Science Framework (OSF)를 통해 request 기반 공개 예정.

---

## 분석 자체에 대한 메모

- paper-info.yaml의 초기 title ("TNBC CTC single-cell transcriptomics: EMT heterogeneity and ribosomal suppression")은 실제 논문 내용과 완전히 다르다. 이 논문은 transcriptomics를 사용하지 않으며, EMT heterogeneity·ribosomal suppression은 연구 주제가 아니다. 원고 paper-info.yaml 수정 필요.
- Figure 3 HR 신뢰구간이 모두 1을 포함함 (TROP2: 0.65–26.35; HER2: 0.58–145.4). 통계적 유의성(p<0.05)은 달성했으나 effect size 추정 정밀도가 낮아 단독 결론 제한적.
- 다중 비교 보정 적용 여부가 Methods에 명시되지 않음.
- CTC-iChip 공동창업자(TellBio)가 저자에 포함되어 있어 상업적 이해상충이 있음 (전략적 방향 평가 시 고려 필요).
> **폴더명 불일치 주의**: 폴더 ID는 `topa-2025-tnbc-ctc-emt`이나, abstract.txt 및 DOI는 Mishra et al. 2025 bioRxiv 논문임. paper-info.yaml의 "TNBC CTC single-cell transcriptomics: EMT heterogeneity and ribosomal suppression" 기술과 abstract 내용이 부분적으로 다름. 본 분석은 abstract.txt 내용을 1차 근거로 사용.

---

## Executive Summary

- **무엇**: TROP2 또는 HER2 표적 ADC 치료를 받는 전이성 유방암 환자 33명에서 CTC를 전향적으로 모니터링하여 치료 반응 바이오마커와 ADC 내성 시 항원 발현 변화를 정량한 연구.
- **핵심 발견**:
  - 치료 시작 3주 이내 CTC 수 감소 = 내구성 반응 예측 (TROP2: 중앙 TTP 391일 vs 97일, HR 4.15, P=0.0046; HER2: 322일 vs 66일, HR 9.12, P=0.0002).
  - ADC 진행(내성 획득) 시점에서 TROP2 및 HER2 발현 = 치료 전 CTC와 비교해 감소하지 않음 → **표적 항원 소실이 주요 내성 기전이 아님**.
  - 동일 payload 유지하면서 ADC 에피토프 전환(TROP2→HER2 또는 역방향)은 효과 낮음.
- **우리 적용**: CytoGen SEV BRCA 코호트에서 ADC 치료 전후 CTC TROP2/HER2 발현 종적 모니터링 서비스의 직접 근거. "내성은 항원 소실이 아닌 payload 내성" — ABCB1/ABCG2/TOP1 발현 변화 분석의 필요성 지지.
- **심층**: `topa-2025-tnbc-ctc-emt_lens-academic.md` / `topa-2025-tnbc-ctc-emt_lens-industry.md` / `topa-2025-tnbc-ctc-emt_methodology-brief.md` 참고.

---

## Identity

- **Title**: Epitope Expression Persists in Circulating Tumor Cells as Breast Cancers Acquire Resistance to Antibody Drug Conjugates
- **Authors**: Mishra A, Abelman R, Cunneely Q, Putaturo V, Deshpande AA, Bell R, Seider EM, Xu KH, Shan M, Kelly J, Huang SB, Gopinathan KA, Kikkeri K, Edd JF, Walsh J, Dai CS, Ellisen L, Ting DT, Nieman L, Toner M, Bardia A, Haber DA, Maheswaran S.
- **Affiliation**: 외부 맥락: Haber DA, Maheswaran S = MGH/Harvard 유방암 CTC 연구 그룹 (Toner M = 마이크로플루이딕스 전문가, Bardia A = 유방암 종양내과 전문가). 자세한 기관 `미제공:` (abstract에 기재 없음).
- **Venue / Year**: *bioRxiv* Preprint (2025-04-02 온라인). PMCID: PMC11996558.
- **DOI**: 10.1101/2025.04.02.646822
- **PMID**: 40235972
- **License**: bioRxiv 기본 CC-BY — 오픈액세스.
- **Citation key**: `mishra2025ctcadc`
- **폴더 ID**: `topa-2025-tnbc-ctc-emt` (명명 불일치 — paper-info.yaml 수정 권장)

---

## Background

### 배경 스토리

- **ADC 성공과 내성**: TROP2 표적 sacituzumab govitecan (SG, Trodelvy), HER2 표적 trastuzumab deruxtecan (T-DXd, Enhertu)은 전이성 유방암에서 임상 입증. 그러나 모든 환자에서 내성이 발생하며, 내성 기전은 불명확.
- **내성 가설 (사전)**: (1) 표적 항원 발현 감소 / 소실, (2) payload 처리 결함(TOP1 변이, efflux pump 증가), (3) 내재화 효율 감소. 이 논문은 33명 환자의 CTC를 통해 (1)을 직접 검증.
- **CTC가 내성 연구에 적합한 이유**: 치료 과정 중 반복 채혈로 *실시간 종양 변화*를 포착 가능. 조직 생검 대비 침습도 낮고, 전이 세포를 직접 분석.
- **에피토프 스위치 전략**: TROP2 ADC 내성 발생 후 HER2 ADC로 전환(또는 역방향) — payload는 같고 에피토프만 바꾸는 전략이 임상에서 시도됨. 이 논문은 이 전략의 *분자적 근거*를 검증.

### 기본 개념

- **CTC 정량적 이미징**: 단일 CTC의 TROP2/HER2 단백질 발현을 *정량적* 이미징으로 측정 — 형광 강도를 통한 per-cell 발현 수준 정량.
- **에피토프 이질성**: 단일 환자 내 CTC 간에도 TROP2/HER2 발현이 이질적 — 평균값이 아닌 분포로 해석해야 함.
- **TTP (Time to Progression)**: 치료 시작부터 질환 진행까지의 기간 — 내구성 반응의 지표.
- **Bystander effect**: ADC payload가 항원 음성 주변 세포에도 독성을 발휘 — 낮은 항원 발현에서도 효능 나타나는 이유.

### 이 논문이 필요한 이유

- CTC TROP2/HER2 발현이 ADC 치료 반응 예측에 사용 가능한지 전향적 검증 필요.
- ADC 내성 시 항원 발현 변화의 *임상 데이터* 부재 — 실험실 연구(세포주, PDX)와 임상 간 간극.
- 에피토프 전환 치료 전략의 *임상 효능* 데이터 필요.

---

## Methods

Abstract 기술 범위:

- **연구 설계**: 전향적(prospective) CTC 모니터링 연구.
- **환자**: 전이성 유방암 환자 33명 — TROP2 또는 HER2 표적 ADC 치료 중.
- **CTC 분석**: 정량적 이미징(quantitative imaging) — TROP2 및 HER2 단백질 발현을 단일 CTC 수준에서 정량.
- **시점**: 치료 시작 전(베이스라인) + 3주 후 + 진행(progression) 시점 — 3시점 종적 비교.
- **비교 기준**: 매칭 종양 생검(matched tumor biopsy) — CTC와 원발/전이 조직 간 발현 일치도 확인.
- **미제공**: 혈액 채취량, CTC 분리 방법(CellSearch vs 마이크로플루이딕스), 이미징 플랫폼(CyteFinder 등), 통계 방법 상세, 에피토프 전환 환자 수.

---

## Results

Abstract 기술 범위:

1. **베이스라인 TROP2/HER2 이질성**: 미치료 환자 단일 CTC 간 TROP2·HER2 발현 이질적 → 매칭 생검과 유사한 이질성 패턴. 임상 반응과의 상관 *불량*.

2. **3주 CTC 감소 = 내구성 반응 예측**:
   - TROP2 ADC: CTC 감소군 중앙 TTP **391일** vs 비감소군 **97일**, HR 4.15, P=0.0046.
   - HER2 ADC: CTC 감소군 중앙 TTP **322일** vs 비감소군 **66일**, HR 9.12, P=0.0002.

3. **진행 시 항원 발현 유지**: TROP2 및 HER2 발현 = 진행 시점 CTC에서 치료 전 CTC 대비 감소 없음 → 항원 소실이 주된 내성 기전이 아님.

4. **에피토프 전환 전략 실패**: 동일 payload 유지하면서 TROP2→HER2(또는 반대) ADC 전환 = 반응 낮음 → payload 내성이 에피토프 내성보다 우선적 내성 기전임을 시사.

---

## Analysis Notes

- **CytoGen 적용 핵심**: "내성은 payload 쪽에서 온다" → TOP1 발현 감소, efflux pump(ABCB1/ABCG2) 증가 분석이 TROP2/HER2 발현 분석보다 더 중요한 내성 예측 변수.
- **scRNA-seq 적용**: 우리 파이프라인에서 TROP2/HER2 단백질 이질성 → 전사체 이질성으로 대리 측정. 단백질-mRNA 상관관계 가정에 주의.
- **3주 CTC count cut-off**: 치료 3주 후 CTC 수 기준이 scRNA-seq 기반 분석에서는 CTC 클러스터 비율 또는 스코어 변화로 대리 측정.
- **Preprint 주의**: bioRxiv 투고 — 동료심사 전. 임상 수치(TTP, HR, P-value)는 최종 출판 시 변경 가능. BD 미팅에서 인용 시 "preprint" 명시 권장.
- **폴더 ID 오류**: `topa-2025-tnbc-ctc-emt` → `mishra-2025-ctc-adc-epitope` 로 변경 권장. paper-info.yaml 업데이트 필요.
