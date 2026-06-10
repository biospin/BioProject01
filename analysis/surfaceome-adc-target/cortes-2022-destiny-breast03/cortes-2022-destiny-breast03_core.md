# cortes-2022-destiny-breast03_core.md

---

## Executive Summary

- **무엇**: HER2 양성 전이성 유방암(HER2+ MBC)의 2차 치료 표준인 T-DM1을 T-DXd로 대체할 수 있는지를 검증한 첫 번째 head-to-head Phase 3 RCT (DESTINY-Breast03). T-DXd의 우월성을 입증해 치료 패러다임을 전환시킨 pivotal trial.
- **모델 / 방법**: Phase 3, 다기관, 공개표지, 무작위배정 대조시험 — T-DXd 5.4 mg/kg q3w vs. T-DM1 3.6 mg/kg q3w, 1:1 무작위배정, N=524. 1차 평가변수 = blinded independent central review (BICR) 기반 progression-free survival (PFS).
- **핵심 결과**:
  - ① PFS (BICR) — T-DXd 중앙값 미도달(NR; 95% CI 18.5–NE) vs. T-DM1 6.8개월(95% CI 5.6–8.2); HR=0.28 (95% CI 0.22–0.37), P<0.001
  - ② 12개월 PFS율 — T-DXd 75.8% vs. T-DM1 34.1%
  - ③ ORR (BICR) — T-DXd 79.7% vs. T-DM1 34.2%; complete response 16.1% vs. 8.7%
  - ④ OS (interim, 1차 분석) — HR=0.55 (95% CI 0.36–0.86), P=0.007; prespecified threshold(P<0.000265) 미도달
  - ⑤ ILD/폐렴 (adjudicated, drug-related) — T-DXd 10.5% vs. T-DM1 1.9%; grade 3 이상은 없음(0건 grade 4–5)
- **우리 적용**: T-DXd의 HER2 ADC 설계(DAR≈8, topoisomerase I inhibitor payload, bystander effect)가 surfaceome-adc-target 분석의 핵심 기준 사례; ADC 타겟 선정·payload 설계·ILD 위험 관리 모두 직접 참조 가능. use_case: `BD-opportunity` + `regulatory-precedent`.
- **심층**: 한계·재현 ROI는 `cortes-2022-destiny-breast03_lens-academic.md` / `cortes-2022-destiny-breast03_lens-industry.md` / `cortes-2022-destiny-breast03_methodology-brief.md` 참고.

---

## Identity

- **Title**: Trastuzumab Deruxtecan versus Trastuzumab Emtansine for Breast Cancer
- **Authors**: J. Cortés, S.-B. Kim, W.-P. Chung, S.-A. Im, Y.H. Park, R. Hegg, M.H. Kim, L.-M. Tseng, V. Petry, C.-F. Chung, H. Iwata, E. Hamilton, G. Curigliano, B. Xu, C.-S. Huang, J.H. Kim, J.W.Y. Chiu, J.L. Pedrini, C. Lee, Y. Liu, J. Cathcart, E. Bako, S. Verma, S.A. Hurvitz, for the DESTINY-Breast03 Trial Investigators
- **Year**: 2022
- **Venue**: New England Journal of Medicine
- **Volume / Pages**: 386:1143–1154
- **DOI**: 10.1056/NEJMoa2115022
- **Citation key**: `cortes2022destinybreast03`
- **Document type**: paper (Phase 3 RCT)
- **ClinicalTrials.gov**: NCT03529110
- **Funding**: Daiichi Sankyo and AstraZeneca

---

## Background

### 배경 스토리

- **문제의 출발점**: 유방암은 전 세계 여성에서 가장 많이 진단되고 사망률이 가장 높은 암이다. 유방암 환자의 약 20%는 HER2 (human epidermal growth factor receptor 2)를 과발현하는 종양을 갖는다 (본문 §Introduction). HER2 표적 치료제들이 임상 결과를 개선해왔지만 진행성·전이성 질환에서는 치료가 불가능하고 대부분의 환자가 진행을 경험한다.

- **선행 접근 A — 1차 치료 표준 (pertuzumab + trastuzumab + taxane)**: 새로 진단된 HER2+ MBC의 1차 표준치료는 pertuzumab과 trastuzumab(항-HER2 항체)에 taxane을 병합하는 요법으로 확립되어 있다 (본문 ref 4–7). 이 요법은 중앙 OS를 크게 연장시켰지만, 1차 치료 후 진행한 환자에서의 후속 치료 선택지가 제한된다.

- **A의 한계**: 1차 치료 후 진행한 환자에게는 표준 2차 치료가 필요하다. EMILIA 시험에서 T-DM1(trastuzumab emtansine)이 lapatinib + capecitabine 대비 PFS와 OS를 개선해 2차 치료 표준으로 자리 잡았다 (본문 ref 7, 8 — EMILIA에서 T-DM1 중앙 PFS 9.6개월, 중앙 OS 30.9개월). 그러나 이 수치는 현재 환자 집단(대부분 pertuzumab 선치료를 받은)에서는 더 낮게 관찰된다 — DESTINY-Breast03에서 T-DM1 arm의 중앙 PFS가 6.8개월로 나타나는 것이 그 방증이다.

- **선행 접근 B — T-DXd (trastuzumab deruxtecan)의 Phase 2 데이터**: T-DXd(DS-8201)는 인간화 항-HER2 단클론항체에 topoisomerase I 억제제 payload를 고약물-항체비(DAR≈8)의 cleavable linker로 연결한 antibody–drug conjugate (ADC)이다 (본문 ref 9, 10). DESTINY-Breast01 Phase 2 단일군 연구에서 2회 이상 항-HER2 치료를 받은 HER2+ MBC 환자에서 ORR 60.9% (95% CI 53.4–68.0), 중앙 PFS 16.4개월을 달성해 가속 승인을 받았다 (본문 §Introduction).

- **B의 한계 / 이 논문으로 이어지는 gap**: DESTINY-Breast01은 단일군 Phase 2이었고, 당시 표준 2차 치료인 T-DM1과의 직접 비교(head-to-head) 데이터가 없었다. 규제 승인 확대와 치료 표준 전환을 위해서는 T-DM1 대비 우월성을 Phase 3 RCT로 증명해야 했다. 이 gap이 DESTINY-Breast03의 설계 근거다.

### 기본 개념

- **HER2+ 유방암**: HER2 단백질을 과발현하거나 HER2 유전자가 증폭된 유방암 아형. 면역조직화학(IHC) 3+ 또는 HER2 ISH 양성(IHC 2+)으로 정의. 본 시험에서는 중앙 실험실 IHC 판독으로 확인.

- **ADC (Antibody–Drug Conjugate) 구조**: ① 항체(HER2 결합) → ② linker(tumor 내 lysosomal enzyme에 의해 절단되는 tetrapeptide-based cleavable linker) → ③ payload(DXd, topoisomerase I 억제제, DNA 손상 유도). T-DXd는 DAR≈8로 고부하이며 payload가 막 투과성을 가져 이웃 HER2 낮은 세포까지 죽이는 bystander effect를 발생시킨다 (본문 ref 9–11).

- **T-DM1(trastuzumab emtansine)**: 항-HER2 항체에 미소관 저해제(DM1)를 non-cleavable linker로 연결한 ADC. DAR≈3.5. EMILIA 시험에서 2차 치료 표준으로 확립.

- **Progression-free survival (PFS)**: 무작위배정일부터 종양 진행(RECIST v1.1 기준) 또는 어떤 이유로든 사망까지의 시간. 본 시험의 1차 평가변수. BICR과 investigator review 두 가지로 평가.

- **Interstitial lung disease (ILD) / 폐렴**: T-DXd의 class-specific 독성. 독립 판정위원회가 모든 잠재적 ILD/폐렴 사례를 평가. NCI CTCAE v5.0로 분류. 관리 지침이 임상시험 프로그램에 포함되어 있고, grade 2 이상 발생 시 T-DXd 투여 중단이 의무화됨.

### 이 논문의 필요성

- **핵심 이유**: T-DM1 기반 2차 치료 표준 하에서 HER2+ MBC 환자의 예후는 여전히 불량하며, 특히 1차 치료에 pertuzumab을 포함한 현재 환자에서 T-DM1의 실제 PFS는 EMILIA 때보다 낮다.
- **기존 방법으로 부족했던 지점**: DESTINY-Breast01의 단일군 설계와 3차 이상 치료 환자 집단은 2차 치료 표준 교체를 뒷받침하기에 부족했다.
- **이 논문이 해결하려는 방향**: T-DXd 5.4 mg/kg q3w가 T-DM1 3.6 mg/kg q3w 대비 PFS에서 우월한지 Phase 3 RCT로 직접 검증. 동시에 OS, ORR, 안전성(특히 ILD)을 평가해 규제·임상 의사결정의 근거를 확보.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: Phase 3, 다기관(15개국 169센터), 공개표지, 무작위배정 대조시험. T-DXd 5.4 mg/kg IV q3w vs. T-DM1 3.6 mg/kg IV q3w의 efficacy 및 safety 비교.
- **입력**: HER2+ (IHC 3+ 또는 IHC 2+/ISH+), 절제불가능 또는 전이성 유방암, trastuzumab + taxane 선치료 이력이 있는 환자 (진행성 질환에서 진행 혹은 neoadjuvant/adjuvant 치료 중 6–12개월 내 재발). Brain metastasis 동반 가능(clinically stable, 이전 치료 완료).
- **출력**: PFS (BICR, 1차), OS (key secondary), ORR (complete + partial response), PFS by investigator, safety.
- **추정 대상**: 두 치료군 간 PFS HR의 우월성.
- **중요한 hidden assumption**: 무작위배정으로 알려진 및 알려지지 않은 교란변수 균형. Stratification 변수(호르몬수용체 상태, 이전 pertuzumab 치료, 내장전이 여부)로 잔여 불균형 최소화.

### 확률 / 통계학적 구조

- **Model family**: Survival analysis — Kaplan–Meier estimates + log-rank test (stratified).
- **Likelihood / objective**: Stratified log-rank test, 양측 유의수준 0.05. PFS 우월성 경계값 P<0.000204 (전체 유의수준 0.05에서 interim에 alpha spending 적용).
  - 해석: 논문 본문에는 efficacy superiority boundary를 P<0.000204라고 명시 (p.1145 §Statistical Analysis); interim 분석은 약 245 progression/사망 이벤트 발생 후 수행 (정보 분율 ≈70%).
- **Prior / regularization**: 미제공 (frequentist framework; Bayesian prior 없음).
- **Latent variable / hidden state**: 없음 (traditional RCT survival analysis).
- **Inference / optimization**: Cox proportional hazard model로 HR 및 95% CI 추정. 층화 변수 보정.
- **Noise, sparsity, uncertainty 처리**: Censoring 처리는 표준 right-censoring. BICR로 주관적 bias 최소화. OS는 별도 prespecified boundary P<0.000265 (86 사망 이벤트 기준).

### 핵심 method insight

- **기존 방법의 한계**: DESTINY-Breast01은 단일군 Phase 2였고 선행 치료가 더 많았으며(중앙 6회 이상) 현재 2차 치료 대상 환자와 다른 집단. T-DM1와의 직접 비교 불가.
- **이 논문의 바꾼 가정**: 2차 치료 적절 환자에서 T-DXd를 T-DM1과 같은 조건에서 비교할 수 있다는 것. Pertuzumab 선치료를 받은 환자 비율이 높아 현실의 2차 치료 상황을 더 잘 반영.
- **새로 추가한 변수 또는 구조**: 독립 판정위원회(ILD adjudication committee)를 두어 pulmonary toxicity를 별도 평가 — 이전 single-arm trial에서 ILD가 중요 위험으로 확인된 이후 관리 지침을 trial protocol에 내장.
- **이 변화가 중요한 이유**: Phase 3 RCT 설계와 BICR 기반 PFS, 독립 ILD 판정이 결합되어 결과의 신뢰도가 높고 FDA/EMA의 정식 승인 교체를 지지하는 수준의 근거를 생성.

### 이전 방법과의 차이

- **Baseline**: EMILIA (T-DM1 vs. lapatinib+capecitabine). EMILIA는 pertuzumab 이전 시대 환자 집단.
- **공통점**: 동일한 HER2+ MBC 2차 치료 세팅, 1:1 무작위배정, PFS as primary endpoint.
- **차이점**: 현재 시험은 pertuzumab 선치료 비율 ~62%, brain metastasis 포함, 관리된 ILD protocol 포함, T-DXd DAR≈8 vs. T-DM1 DAR≈3.5.
- **차이가 크게 나타나는 조건**: T-DXd는 HER2 발현 수준이 낮은 이웃 세포에도 bystander killing이 가능하여, 종양 내 HER2 이질성이 있는 경우 더 큰 이점이 예상됨. 다만 이 시험에서 직접 heterogeneity 분석은 없음.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: DESTINY-Breast03 ITT population (T-DXd N=261, T-DM1 N=263).
- **Metric**: PFS (primary), OS (key secondary), ORR, DCR.
- **개선된 결과**: PFS HR=0.28 (72% 위험 감소), ORR 79.7% vs. 34.2%.
- **Ablation 근거**: 미제공 (임상시험이므로 ablation 없음).
- **정성적 효과**: 모든 사전 설정 subgroup (호르몬수용체 상태, pertuzumab 선치료, 내장전이, 뇌전이, 치료 라인 수)에서 T-DXd 우월성이 일관됨.

### Method 관점의 한계

- **약한 assumption**: 공개표지 설계 — investigator-based PFS는 subjective bias 가능성 있음(단, BICR이 1차 평가변수로 설계됨).
- **구현 또는 학습상의 부담**: ILD 관리 프로토콜 적용이 실제 임상에서 훈련되지 않은 기관에서는 재현이 어려울 수 있음.
- **일반화가 불확실한 조건**: Asia 환자 비율이 약 58–61%로 높아 다른 인종/지역 집단 일반화 주의. OS interim 데이터는 추적 기간이 짧아(중앙 15–16개월) 장기 survival benefit는 아직 미확정.

---

## Results

### Dataset별 결과

#### Dataset 1 — DESTINY-Breast03 ITT Population (PFS 1차 분석)

- **Dataset**: Phase 3 RCT, HER2+ unresectable/metastatic breast cancer, 15개국 169센터, trastuzumab + taxane 선치료. N=524 (T-DXd 261, T-DM1 263).
- **목적**: T-DXd 대비 T-DM1의 PFS 우월성 검증.
- **사용한 데이터 규모**: Enrollment 2018.07.20 – 2020.06.23, interim analysis cutoff 2021.05.21, 245 PFS 이벤트 발생 후. 중앙 추적기간 T-DXd 16.2개월, T-DM1 15.3개월.
- **Baseline / 비교 대상**: T-DM1 3.6 mg/kg q3w (당시 2차 치료 표준).
- **Metric / 평가 기준**: PFS (BICR, RECIST v1.1), 층화 log-rank test, HR (Cox).
- **주요 수치**:
  - T-DXd 중앙 PFS: NR (95% CI 18.5–NE)
  - T-DM1 중앙 PFS: 6.8개월 (95% CI 5.6–8.2)
  - HR: 0.28 (95% CI 0.22–0.37), P<0.001
  - 12개월 PFS율: T-DXd 75.8% (95% CI 69.8–80.7) vs. T-DM1 34.1% (95% CI 27.7–40.5)
  - Investigator-assessed 중앙 PFS: T-DXd 25.1개월 (95% CI 22.1–NE) vs. T-DM1 7.2개월 (95% CI 6.8–8.3); HR=0.26 (95% CI 0.20–0.35), P<0.001
- **정성 결과**: 모든 사전 설정 subgroup (HR 상태, pertuzumab 선치료, 내장전이, 뇌전이, 치료 라인 수)에서 T-DXd 이점이 일관됨. 해석: 하위군 HR 범위 0.27–0.38로 전반적 일관성 강함.

#### Dataset 2 — DESTINY-Breast03 ITT Population (OS 1차 interim)

- **Dataset**: 동일 ITT population. OS interim cutoff 2021.05.21, 86 사망 이벤트 (prespecified OS 분석 기준).
- **목적**: OS benefit 조기 신호 파악.
- **사용한 데이터 규모**: T-DXd 33명 사망(12.6%), T-DM1 53명 사망(20.2%).
- **Baseline / 비교 대상**: T-DM1.
- **Metric**: OS, Kaplan–Meier, HR.
- **주요 수치**:
  - 중앙 OS: 두 군 모두 NE (NE–NE)
  - 12개월 OS율: T-DXd 94.1% (95% CI 90.3–96.4) vs. T-DM1 85.9% (95% CI 80.9–89.7)
  - HR: 0.55 (95% CI 0.36–0.86), P=0.007
  - Prespecified OS boundary: P<0.000265 — 미도달 (즉 OS 결론은 이 interim에서 확정 불가)
- **정성 결과**: 생존곡선의 이른 분리와 지속적 벌어짐이 관찰됨. 407명이 추적 중으로 OS 성숙도 낮음.
- **논문 주장과의 연결**: OS 수치는 positive trend이나 아직 prespecified threshold 미충족 — 저자는 "추적 기간이 더 필요하다"고 명시.

#### Dataset 3 — DESTINY-Breast03 ITT Population (ORR 및 항종양 활성)

- **Dataset**: 동일 ITT, target lesion 기저치+추적치 모두 있는 환자: T-DXd 245명, T-DM1 228명.
- **목적**: 객관적 반응률 및 종양 축소 정도 평가.
- **Metric**: ORR (CR+PR, BICR), DCR (CR+PR+SD), best percentage change in tumor size.
- **주요 수치**:
  - ORR: T-DXd 79.7% (95% CI 74.3–84.4) vs. T-DM1 34.2% (95% CI 28.5–40.3)
  - CR: T-DXd 16.1% (42/261) vs. T-DM1 8.7% (23/263)
  - PR: 63.6% vs. 25.5% (추정: 79.7%–16.1%=63.6%, 34.2%–8.7%=25.5%)
  - Progressive disease (best response): T-DXd 1.1% vs. T-DM1 17.5%
  - DCR: T-DXd 96.6% vs. T-DM1 76.8%
  - Median time to response: T-DXd 첫 종양 검사 시점(치료 시작 후 가장 빠름) — 본문에 정확한 주 수 미제공; "responses were usually rapid" 언급.
- **논문 주장과의 연결**: 깊은 반응(CR 2배 이상, progressive disease 1% 미만)과 높은 DCR이 종양 제어 측면에서 T-DXd의 질적 우월성을 뒷받침.

#### Dataset 4 — DESTINY-Breast03 Safety Population

- **Dataset**: T-DXd 257명(치료받은 환자), T-DM1 261명.
- **목적**: 약물 관련 이상반응(AE) 빈도·중증도 및 ILD/폐렴 판정 결과 평가.
- **주요 수치 (Table 2)**:
  - Drug-related AE any grade: T-DXd 98.1% vs. T-DM1 86.6%
  - Drug-related AE grade ≥3: T-DXd 45.1% vs. T-DM1 39.8%
  - Drug-related AE로 인한 치료 중단: T-DXd 13.6% vs. T-DM1 7.3%
  - Adjudicated drug-related ILD/폐렴: T-DXd 27명(10.5%) vs. T-DM1 5명(1.9%); grade 4–5: 0건
  - ILD grade 분포 (T-DXd): grade 1 — 7명(2.7%), grade 2 — 18명(7.0%), grade 3 — 2명(0.8%)
  - ILD로 인한 치료 중단: T-DXd 21명(8.2%) vs. T-DM1 3명(1.1%)
  - Serious AE: T-DXd 49/257명(19.1%) vs. T-DM1 47/261명(18.0%)
  - 가장 흔한 drug-related AE (T-DXd): 오심 72.8%, 피로 44.7%, 구토 44.0%, 탈모 36.2%, 호중구감소증 42.8%
- **논문 주장과의 연결**: ILD 발생률이 DESTINY-Breast01 대비 낮아진 것을 저자는 이전 치료 라인이 적고 ILD 관리 프로토콜이 내장됐기 때문으로 설명. 해석: grade 3 이상 ILD가 0.8%로 관리 가능 수준이지만 grade 2 발생 시 의무 중단 기준이 실무에서 훈련 필요성을 높인다.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 모든 efficacy endpoint (PFS, OS 경향, ORR, DCR)에서 T-DXd 우월. 모든 사전 설정 subgroup에서 일관된 PFS HR 0.27–0.38.
- **가장 중요한 수치**: PFS HR=0.28 (95% CI 0.22–0.37), P<0.001; 12개월 PFS 75.8% vs. 34.1%.
- **Baseline 대비 차이**: T-DM1의 현재 trial 중앙 PFS(6.8개월)는 EMILIA(9.6개월)보다 낮음 — pertuzumab 선치료 증가로 인한 것으로 저자가 설명.
- **결과 해석 시 주의점**: OS는 interim으로 아직 미성숙. Asia 환자 비율 ≈60%로 서양 환자 일반화 주의. 공개표지 설계이나 1차 평가변수는 BICR로 bias 최소화됨.

---

## Figures

#### Figure 1 (facing p.1148 — Kaplan–Meier Analysis and Subgroup Analysis of Progression-free Survival)

- **이 Figure가 필요한 이유**: PFS 우월성의 시각적·정량적 근거를 동시에 제공. Panel A는 전체 ITT 집단의 survival curve, Panel B는 subgroup consistency를 forest plot으로 제시해 결과의 범용성을 보인다.
- **이 Figure가 뒷받침하는 주장**: T-DXd가 T-DM1 대비 유의하게 긴 PFS를 보이며, 이 이점은 임상적으로 정의된 모든 하위군에서 일관된다.

##### 패널별 설명
- **Panel A (Kaplan–Meier, PFS)**: x축 = 개월, y축 = 무진행 환자 비율(%). T-DXd (파란색, N=261) 곡선이 T-DM1 (회색, N=263) 대비 전반적으로 높게 유지. T-DM1 curve는 6–8개월 구간에서 급격히 하강. 중앙 PFS: T-DXd NR, T-DM1 6.8개월; HR=0.28 (95% CI 0.22–0.37), P<0.001. 12개월 PFS: 75.8% vs. 34.1%.
- **Panel B (Forest plot, subgroup PFS)**: Row = 하위군(호르몬수용체 상태, pertuzumab 선치료, 내장전이, 치료 라인 수, 뇌전이). Column = HR (95% CI). 모든 subgroup에서 HR < 1.0, 신뢰구간이 1.0을 포함하지 않음. HR 범위: 0.27–0.38. 뇌전이 있는 환자 subgroup (N=114): HR=0.38 (95% CI 0.23–0.64), 중앙 PFS T-DXd 15.0개월 vs. T-DM1 3.0개월(추정: 5.7개월로 본문 인용).

##### 본문에서 강조한 비교
- 비교 대상: T-DXd vs. T-DM1 전체 및 사전 설정 subgroup
- 관찰된 차이: 전체 HR=0.28로 약 72% 위험 감소. 어떤 subgroup도 T-DM1 방향으로 HR이 넘어가지 않음.
- 이 차이가 의미하는 것: 결과의 robust consistency — 특정 생물학적 또는 임상적 선택 기준 없이 HER2+ 2차 치료 전반에 걸쳐 T-DXd 이점이 성립함.

##### 해석 시 주의점
- Subgroup analysis는 사전 설정되었으나 개별 subgroup은 상대적으로 작아 과해석 주의.
- 검정: subgroup HR 점 추정치는 비교적 일관적이나 CI가 넓음. 특히 뇌전이 subgroup (N=114)은 탐색적 의미.

---

#### Figure 2 (p.1150 — First Interim Analysis of Overall Survival)

- **이 Figure가 필요한 이유**: PFS benefit가 OS로 이어지는지를 조기에 보여주기 위함. OS는 key secondary endpoint.
- **이 Figure가 뒷받침하는 주장**: OS에서 positive trend가 있음을 시각적으로 보여주되, 아직 prespecified threshold 미충족임을 명시.

##### 패널별 설명
- **단일 panel (OS Kaplan–Meier)**: x축 = 개월(최대 34개월), y축 = 생존 환자 비율(%). 두 곡선이 초기부터 분리되어 T-DXd가 상위에 위치. 12개월 OS: T-DXd 94.1% (95% CI 90.3–96.4) vs. T-DM1 85.9% (95% CI 80.9–89.7). 중앙 OS 두 군 모두 NE. HR=0.55 (95% CI 0.36–0.86), P=0.007.

##### 본문에서 강조한 비교
- 비교 대상: T-DXd vs. T-DM1 전체 ITT
- 관찰된 차이: 12개월 OS율 차이 8.2%p (94.1% vs. 85.9%). 이른 분리와 지속적 벌어짐.
- 이 차이가 의미하는 것: OS benefit의 방향성은 명확하나, 86 사망 이벤트 기준 interim에서 P<0.000265 threshold 미충족으로 공식적 OS 우월성 결론은 보류.

##### 해석 시 주의점
- 추적 기간이 짧아(중앙 15–16개월) OS 데이터 성숙도 낮음. P=0.007이 nominal significance는 있지만 alpha spending 고려 시 아직 경계 미달.
- 407명이 아직 추적 중 — 최종 OS 결과가 별도 논문으로 보고될 예정(본문 내 암시).

---

#### Figure 3 (p.1151 — Antitumor Activity — Waterfall plots)

- **이 Figure가 필요한 이유**: 각 환자 개별의 최대 종양 축소를 시각화해 반응의 깊이와 폭을 보여주는 보조 증거.
- **이 Figure가 뒷받침하는 주장**: T-DXd는 대다수 환자에서 종양 축소를 달성하며 반응 깊이가 T-DM1보다 현저히 깊다.

##### 패널별 설명
- **Panel A (T-DXd, N=245)**: 수직 bar = 각 환자의 baseline 대비 종양 크기 최대 변화율(%). 대부분의 bar가 아래쪽(감소)으로 향함. -30% 이하(partial response 기준 하 점선) 아래에 대부분의 bar가 위치.
- **Panel B (T-DM1, N=228)**: 비교적 더 많은 bar가 0% 이상(증가) 방향이거나 감소 폭이 얕음.

##### 본문에서 강조한 비교
- 비교 대상: T-DXd vs. T-DM1의 개별 반응 분포
- 관찰된 차이: T-DXd에서 progressive disease (best response)가 1.1%뿐, T-DM1에서는 17.5%.
- 이 차이가 의미하는 것: T-DXd는 반응 "깊이"와 "폭" 모두에서 우월 — CR 비율이 거의 두 배, progressive disease 거의 없음.

##### 해석 시 주의점
- Waterfall plot은 각 환자가 evaluable해야 하므로 모든 randomized 환자가 포함되지 않음 (T-DXd 245/261, T-DM1 228/263). 추론: 포함 기준이 baseline + postbaseline 측정치 모두 있는 환자로 제한됨. 선택 bias 가능성은 낮으나 excluded 환자 특성 확인 필요.

---

## Tables

### Table 1 (p.1146–1147 — Demographic and Baseline Clinical Characteristics)

- **이 Table이 필요한 이유**: 무작위배정이 두 군의 임상 기저치를 균형 있게 분배했는지 확인.
- **이 Table이 뒷받침하는 주장**: 두 군 사이 기저치 균형 — 결과 차이가 baseline 불균형에서 기인하지 않음.

#### 표 구조
- Row (비교 축 1): 인구통계학적 및 임상 특성 항목
- Column (비교 축 2): T-DXd (N=261) | T-DM1 (N=263)
- 셀 값의 의미: n (%) 또는 median (range)

#### 핵심 수치
- 중앙 연령: T-DXd 54.3세(범위 27.9–83.1) vs. T-DM1 54.2세(범위 20.2–83.0)
- Asia 환자 비율: T-DXd 57.1% (149/261) vs. T-DM1 60.8% (160/263)
- HER2 IHC 3+: T-DXd 89.7% vs. T-DM1 88.2%
- HR 양성: T-DXd 50.2% vs. T-DM1 51.0%
- 내장전이: T-DXd 70.5% vs. T-DM1 70.3%
- 안정 뇌전이: T-DXd 23.8% vs. T-DM1 19.8%
- Pertuzumab 선치료: T-DXd 62.1% vs. T-DM1 60.1%
- Taxane 선치료: T-DXd 99.6% vs. T-DM1 99.6%
- 이전 치료 라인 수(전이 세팅) 중앙값: T-DXd 1 vs. T-DM1 2
  - 해석: 중앙 치료 라인의 1 vs. 2 차이는 T-DM1 군에 더 많은 선치료 환자가 포함됐을 가능성을 시사하지만, 1라인 비율(49.8% vs. 46.8%)은 유사하고 stratification 인자 포함으로 보정됨.

#### 본문에서 강조한 비교
- 본문에서 "두 군의 인구통계학적 및 기저치 질환 특성이 유사하고 전체 HER2+ 유방암 환자 집단을 대체로 대표한다"고 명시 (§Results §Patients).
- 주의점: 이전 치료 라인 수 중앙값의 T-DXd 1 vs. T-DM1 2 차이가 efficacy 결과에 영향을 미치는지 stratification에서 완전히 제어되지 않을 수 있음. 그러나 본문 subgroup 분석(0 or 1 line vs. ≥2 lines)에서 HR이 0.28–0.33으로 유사해 큰 영향 없음.

#### 해석 시 주의점
- Asia 환자가 약 58–61%를 차지해 기타 인종/지역 환자 수가 상대적으로 적음. 인종별 분석은 본문에 없음.

---

### Table 2 (p.1152 — Most Common Drug-Related Adverse Events and Adjudicated Drug-Related ILD or Pneumonitis)

- **이 Table이 필요한 이유**: 두 약물의 안전성 프로파일 직접 비교, 특히 T-DXd의 class-specific toxicity인 ILD의 정량화.
- **이 Table이 뒷받침하는 주장**: T-DXd의 전반적 독성 프로파일은 관리 가능하며, ILD 발생은 DESTINY-Breast01보다 낮고 grade 4–5 없음.

#### 표 구조
- Row: 이상반응 항목
- Column: T-DXd (N=257) | T-DM1 (N=261) × any grade | grade ≥3
- 셀 값의 의미: n (%)

#### 핵심 수치 (Table 2에서 가장 결정적인 셀)

1. **호중구감소증 any grade**: T-DXd 42.8% vs. T-DM1 11.1%; grade ≥3: 19.1% vs. 3.1%
   - 해석: T-DXd에서 혈액독성이 더 높으나 T-DM1에서는 혈소판감소증이 두드러짐.

2. **혈소판감소증 any grade**: T-DXd 24.9% vs. T-DM1 51.7%; grade ≥3: 7.0% vs. 24.9%
   - 해석: T-DM1 특이적 독성(DM1 microtubule inhibitor payload 관련) — T-DXd 대비 현저히 높음.

3. **오심 any grade**: T-DXd 72.8% vs. T-DM1 27.6%; grade ≥3: 6.6% vs. 0.4%
   - 해석: 오심은 T-DXd의 가장 흔한 AE. Grade ≥3은 6.6%로 제한적이지만 환자 삶의 질에 영향.

4. **Adjudicated ILD/폐렴 any grade**: T-DXd 10.5% (27/257) vs. T-DM1 1.9% (5/261); grade ≥3: 0.8% (2명) vs. 0%
   - 통계적 유의성: p-value 미제공(본문에 명시 없음). 해석: 10.5% 발생률은 DESTINY-Breast01의 15.4% 대비 낮아졌고, grade 4–5가 없다는 점이 관리 지침 도입의 효과를 시사.

#### 본문에서 강조한 비교
- T-DXd의 두드러진 AE: 오심, 피로, 구토, 탈모, 호중구감소증 — 이들은 고용량 항암제 특성.
- T-DM1의 두드러진 AE: 혈소판감소증 (grade ≥3 24.9%), AST/ALT 상승 (grade ≥3 AST 5.0%, ALT 4.6%).
- ILD 발생 시 median time to onset: T-DXd 168일(범위 33–507일). 발생 환자 대부분 회복.

#### 해석 시 주의점
- ILD grade 3 이상이 매우 낮지만 grade 2 발생 시 의무 투여 중단 → 실제 치료 연속성에 영향. Table S6 (appendix)에 ILD 발생률 상세.
- T-DXd 군에서 drug-related AE로 치료 중단 13.6% (T-DM1 7.3%) — ILD가 주 원인.

---

## Supplementary Information

Supplementary Appendix (nejmoa2115022_appendix.pdf)는 다음으로 구성됨:

- **Supplementary Methods** (p.9–11): 무작위배정 절차, 층화 변수 상세, RECIST v1.1 기반 평가 주기, ILD/폐렴 독립 판정 위원회 구성 및 판정 기준, statistical analysis plan 상세.
- **Figure S1 — Trial Profile** (p.14): Enrollment, randomization, treatment, analysis population flow. T-DXd 261/T-DM1 263 ITT; safety population T-DXd 257/T-DM1 261.
- **Figure S2 — PFS by Investigator Review** (p.15): Investigator-assessed PFS Kaplan–Meier. T-DXd 중앙 PFS 25.1개월 vs. T-DM1 7.2개월; HR=0.26 (95% CI 0.20–0.35), P<0.001.
- **Table S1 — Management Guidelines for Pulmonary Toxicity** (p.16–18): ILD/폐렴 grade별 관리 알고리즘 — grade 1: hold and monitor; grade 2: mandatory discontinue; grade 3–4: permanently discontinue.
- **Table S2 — Representativeness of Study Participants** (p.19–20): ITT 환자와 전체 HER2+ MBC 레지스트리 비교 데이터.
- **Table S3 — Response (IRC)** (p.21): ORR 상세 (CR, PR, SD, PD, NE 구분). T-DXd ORR 79.7% vs. T-DM1 34.2% 확인.
- **Table S4 — Post Anticancer Treatment** (p.22): 시험 치료 종료 후 후속 항암 치료 내역.
- **Table S5 — Overall Safety Summary** (p.23): 전반적 AE 요약.
- **Table S6 — Rates of ILD/Pneumonitis** (p.24): ILD 발생 시기, 회복 여부, 사례별 상세.
- **Table S7 — Analysis of PFS (BICR)** (p.25): stratified log-rank test 및 Cox model 결과 수치.

---

## 분석 자체에 대한 메모

- **추적 기간 짧음**: OS 데이터는 interim이며 미성숙. 최종 OS 분석은 추후 별도 발표가 필요하다 (현재 407명 추적 중).
- **Asia 과대표 가능성**: 전체 환자의 약 58–61%가 Asia 출신으로 서구 환자 집단에서의 일반화는 제한. 인종별 상세 분석은 본문에 없음.
- **공개표지 설계**: 1차 평가변수 BICR로 보완되었으나, 보조적 investigator-reviewed PFS에서는 observer bias 완전 배제 불가.
- **ILD 관리 프로토콜 재현성**: 임상시험 setting에서의 ILD 발생률이 실제 임상 현장보다 낮을 가능성. 관리 지침의 실무 전파가 T-DXd의 안전한 사용에 핵심.
- **검토필요**: Table S6에서 ILD 발생 환자별 회복 여부 및 사망 여부의 상세 데이터가 있으나 본 분석에서 충분히 추출하지 못함. 폐독성 모니터링 프로토콜의 효과 크기 정량화를 위한 추가 분석 필요.
