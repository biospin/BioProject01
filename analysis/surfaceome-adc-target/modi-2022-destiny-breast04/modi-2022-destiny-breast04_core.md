# modi-2022-destiny-breast04 — Core Analysis

## Executive Summary

- **무엇**: HER2 발현 수준이 낮은(IHC 1+ 또는 IHC 2+/ISH-음성) 전이성 유방암 환자에서 trastuzumab deruxtecan(T-DXd)이 의사 선택 화학요법 대비 유의한 PFS·OS 개선을 보인 Phase 3 DESTINY-Breast04 시험. HER2-low를 독립 치료 가능 집단으로 최초 확립하고 ADC 승인 근거를 제공.
- **모델 / 방법**: 무작위 배정(2:1), 공개 라벨, Phase 3 시험. T-DXd 5.4 mg/kg Q3W vs. 의사 선택(capecitabine/eribulin/gemcitabine/paclitaxel/nab-paclitaxel). 1차 endpoint: HR+ 코호트 PFS(blinded independent central review). 계층화 log-rank + stratified Cox regression.
- **핵심 결과**:
  - ① HR+ 코호트(n=331+163) — T-DXd mPFS 10.1개월 vs. PC 5.4개월, HR 0.51 (95% CI 0.40–0.64), P<0.001
  - ② 전체 환자(n=373+184) — T-DXd mPFS 9.9개월 vs. PC 5.1개월, HR 0.50 (95% CI 0.40–0.63), P<0.001
  - ③ HR+ 코호트 OS — T-DXd 23.9개월 vs. PC 17.5개월, HR 0.64 (95% CI 0.48–0.86), P=0.003
  - ④ 전체 환자 OS — T-DXd 23.4개월 vs. PC 16.8개월, HR 0.64 (95% CI 0.49–0.84), P=0.001
  - ⑤ ORR: T-DXd 52.6% vs. PC 16.3% (HR+ 코호트); ILD/pneumonitis 12.1% (grade 5: 0.8%)
- **우리 적용**: HER2-low 정의(IHC 1+/2+ ISH-음성)가 CTC 기반 HER2 동적 프로파일링 연구의 타깃 집단 경계선과 직접 연결됨. regulatory-precedent + BD-opportunity use case.
- **심층**: 한계·재현 ROI는 `modi-2022-destiny-breast04_lens-academic.md` / `modi-2022-destiny-breast04_lens-industry.md` / `modi-2022-destiny-breast04_methodology-brief.md` 참고.

---

## Identity

- **Title**: Trastuzumab Deruxtecan in Previously Treated HER2-Low Advanced Breast Cancer
- **Authors**: Modi S, Jacot W, Yamashita T, Sohn J, Vidal M, Tokunaga E, Tsurutani J, Ueno NT, Prat A, Chae YS, Lee KS, Niikura N, Park YH, Xu B, Wang X, Gil-Gil M, Li W, Pierga J-Y, Im S-A, Moore HCF, Rugo HS, Yerushalmi R, Zagouri F, Gombos A, Kim S-B, Liu Q, Luo T, Saura C, Schmid P, Sun T, Gambhire D, Yung L, Wang Y, Singh J, Vitazka P, Meinhardt G, Harbeck N, Cameron DA — DESTINY-Breast04 Trial Investigators
- **Year**: 2022 (published June 5, 2022; updated June 15, 2022)
- **Venue**: New England Journal of Medicine 387:9–20
- **DOI**: 10.1056/NEJMoa2203690
- **Citation key**: `@modi2022destinybreast04`
- **Funding**: Daiichi Sankyo and AstraZeneca
- **ClinicalTrials.gov**: NCT03734029

---

## Background

### 배경 스토리

- **문제의 출발점**: HER2 양성(IHC 3+ 또는 IHC 2+/ISH 양성) 유방암은 trastuzumab 계열 등 HER2 표적 치료로 성과를 거뒀으나, HER2 음성(HER2-negative)으로 분류된 전이성 유방암 환자의 약 60%는 IHC 1+ 또는 IHC 2+/ISH-음성("HER2-low")으로, 기존 HER2 이진 분류(양성 vs. 음성)에서 치료 가능 대상에 포함되지 않았다.

- **선행 접근 A — CDK4/6 억제제 + 내분비 치료**: HR+ HER2-음성 전이성 유방암에서 CDK4/6 억제제(palbociclib, ribociclib)와 내분비 치료 병합은 약 2년간 효과적이지만, 이후 내성이 빈번히 발생한다. CDK4/6 억제제 및 화학요법 이후 real-world PFS는 4개월 수준(Mo et al., Clin Breast Cancer 2022 — 본문 인용).

- **선행 접근 B — 기존 HER2 표적 치료(trastuzumab, T-DM1)의 HER2-low 시도**: NSABP B-47과 T-DM1 Phase 2 연구에서 HER2-low 환자에 대해 기존 HER2 표적 치료는 임상 이득이 없음이 확인됐다(본문 ref. 3, 4). 즉 HER2 과발현이 없으면 항체 자체의 결합 효율 및 ADCC 메커니즘이 충분하지 않다.

- **Gap**: HER2-low는 기존 HER2 이진 분류에서 "음성"으로 처리되어 화학요법만 받아왔으나, IHC로 검출 가능한 수준의 HER2 단백질이 ADC의 전달 매개체로 충분할 수 있다는 가설이 제기됐다. Phase 1/2 연구(Modi 2020, Diéras 2022)에서 T-DXd가 ORR 37–37.5%, mPFS 6.3–11.1개월의 가능성을 보였으나, Phase 3 무작위 비교 근거가 없었다.

- **이 논문으로 이어지는 gap**: HER2-low 집단을 독립 치료 가능 인구로 정의하고, T-DXd의 생존 이득을 Phase 3 수준에서 검증하는 DESTINY-Breast04가 설계됐다.

### 기본 개념

- **HER2-low 정의**: IHC 1+ 또는 IHC 2+ + ISH-음성(in situ hybridization 비증폭). HER2 양성(IHC 3+ 또는 IHC 2+/ISH 양성)도 음성(IHC 0)도 아닌 중간 발현 집단. 전이성 유방암 HER2-negative의 약 60%가 여기에 해당.
- **Trastuzumab deruxtecan (T-DXd, DS-8201)**: 인간화 항-HER2 단클론 항체(trastuzumab)에 topoisomerase I 억제제(DXd, exatecan 유도체)를 tetrapeptide 기반 절단 가능 링커로 연결한 ADC. drug-to-antibody ratio 8:1. 막 투과성 payload가 HER2 이질적 발현 인접 세포에도 bystander killing 효과를 발휘.
- **Bystander effect**: T-DXd의 payload(DXd)가 막 투과성이어서 HER2 발현이 낮거나 없는 인접 종양 세포에도 세포독성 효과 전달. HER2-low처럼 이질적 발현 종양에서 특히 중요한 메커니즘.
- **ADC 설계 비교**: 기존 T-DM1(emtansine, DAR 약 3.5, 막 비투과성 payload)과 달리 T-DXd는 높은 DAR(8:1)과 절단 가능 링커·막 투과성 payload로 낮은 HER2 발현에서도 충분한 세포 내 농도를 달성.
- **Stratified log-rank test / Cox regression**: PFS 1차 분석에 사용된 통계 방법. HR+ 코호트를 1차 검정군으로 설정하고, 전체 환자 및 OS를 sequential testing으로 분석.

### 이 논문의 필요성

- **핵심 이유**: HER2-low는 유방암 환자의 절반 이상을 차지함에도 치료 가능 표적으로 인식되지 않았다. T-DXd의 독특한 ADC 구조(고 DAR, 막 투과성 payload, bystander effect)가 낮은 HER2 발현에서도 작동한다는 메커니즘 근거와 Phase 1/2 신호가 있었으나 Phase 3 생존 근거가 없었다.
- **기존 방법으로 부족했던 지점**: 표준 화학요법(eribulin, capecitabine 등)은 mPFS 4–5개월 수준이며, HER2-positive에서 효과적인 기존 항-HER2 치료는 HER2-low에서 작동하지 않았다.
- **이 논문이 해결하려는 방향**: Phase 3 무작위 대조 시험으로 T-DXd의 PFS·OS 이득을 확립하고, IHC 기반 HER2-low 정의를 치료 예측 인자로 검증.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: HER2-low(IHC 1+ 또는 IHC 2+/ISH-음성) 전이성 유방암 환자에서 T-DXd 5.4 mg/kg Q3W vs. 의사 선택 화학요법(capecitabine, eribulin, gemcitabine, paclitaxel, nab-paclitaxel)의 무작위 비교. 1차 endpoint: HR+ 코호트 PFS(blinded independent central review).
- **입력**: 이전 1–2개 라인 화학요법을 받은 HER2-low 전이성 유방암 환자. 중앙 IHC/ISH 검사 확인. HR+ 환자는 최소 1개 라인 내분비 치료 이력 필요.
- **출력**: PFS(1차), OS(핵심 2차), ORR, DOR, 안전성(이상반응 grading).
- **추정 대상**: 두 치료군 간 PFS HR. 계획된 power: HR 0.68 가정 시 90%, HR+ 코호트 318 events 기준.
- **중요한 hidden assumption**: HER2-low가 IHC 검사로 충분히 정의·재현 가능하다는 가정. 실제로 IHC 점수 재현성 문제는 본문에서도 인정됨(Discussion §).

### 확률 / 통계학적 구조

- **Model family**: Survival analysis — Kaplan-Meier 추정, stratified log-rank test(1차), stratified Cox proportional hazards regression(HR 및 95% CI).
- **Likelihood / objective**: 1차 PFS 분석: 두 그룹 간 층화 log-rank 검정, 양측 유의수준 0.05. OS sequential testing: 전체 α 제어를 위해 intermediate stopping boundary 0.0075 설정.
- **Stratification factors**: HER2-low status(IHC 1+ vs. IHC 2+/ISH-음성), 전이성 화학요법 라인 수(1 vs. 2), HR status(양성[CDK4/6 억제제 이전 유무] vs. 음성).
- **Intention-to-treat (ITT) population**: 모든 efficacy 분석. 안전성 분석: 최소 1 용량 투여자.
- **Multiple testing 보정**: Sequential testing 구조(PFS HR+ → PFS 전체 → OS HR+ → OS 전체). Hierarchical family-wise error rate 제어.
- **IHC assay**: VENTANA HER2/neu (4B5) IUO Assay — investigational use only 검사. IHC 2+ 케이스는 INFORM HER2 Dual ISH로 reflex. 2018 ASCO-CAP guideline 기반 알고리즘(Table S1).

### 핵심 method insight

- **기존 방법의 한계**: 기존 HER2 이진 분류 기반 ADC(T-DM1)는 낮은 DAR과 막 비투과성 payload로 인해 HER2 발현이 임계값 이하인 세포에서 충분한 세포독성 달성 불가. 임상 시험도 HER2 양성 기준으로 설계.
- **이 논문이 바꾼 가정**: HER2-low(IHC 1+, 2+/ISH-음성)를 치료 불가 집단이 아닌 ADC 전달 매개체로 충분한 집단으로 재정의. T-DXd의 높은 DAR(8:1) + bystander effect가 낮은 표면 발현에서도 작동.
- **새로 추가한 구조**: IHC 기반 HER2-low 정의의 치료 예측 타당성을 Phase 3 무작위 시험으로 최초 검증. Investigational IHC assay(VENTANA 4B5 IUO)를 companion diagnostic 후보로 사용.
- **이 변화가 중요한 이유**: 전 세계 HER2-음성 유방암 환자의 과반수가 새로운 치료 옵션 대상이 됨. HER2 분류 체계 자체를 HER2-zero / HER2-low / HER2-positive 삼분으로 재편하는 임상적 근거 제공.

### 이전 방법과의 차이

- **Baseline**: 의사 선택 화학요법(eribulin 51.1%, capecitabine 20.1%, nab-paclitaxel 10.3%, gemcitabine 10.3%, paclitaxel 8.2%).
- **공통점**: 전이성 유방암 표준 화학요법 레지멘 사용.
- **차이점**: T-DXd는 HER2-targeted delivery + topoisomerase I 억제. 기존 화학요법은 비특이적 세포독성.
- **차이가 크게 나타나는 조건**: HR-음성 코호트(소규모 n=40+18)에서도 HR 0.46으로 유사한 방향성, CDK4/6 억제제 이전 치료 유무와 무관하게 일관된 이득.

### 효과가 Results에서 나타난 방식

- **Primary endpoint**: HR+ 코호트 PFS — T-DXd mPFS 10.1개월(95% CI 9.5–11.5) vs. PC 5.4개월(95% CI 4.4–7.1), HR 0.51, P<0.001.
- **OS**: HR+ 코호트 OS 23.9 vs. 17.5개월, HR 0.64, P=0.003. 전체 환자 OS 23.4 vs. 16.8개월, HR 0.64, P=0.001.
- **ORR**: T-DXd 52.6% vs. PC 16.3% (HR+ 코호트).
- **Subgroup consistency**: HER2 IHC 1+, 2+/ISH-음성 양 그룹과 CDK4/6 억제제 이전 유무 무관하게 일관된 이득(Fig. S2).

### Method 관점의 한계

- **IHC 재현성**: HER2-low scoring의 관찰자 간 variability가 알려져 있음(Fernandez 2022, JAMA Oncol — 본문 인용). 실제 임상 현장 IHC 결과와 중앙 검사 불일치 가능성.
- **open-label design**: 환자와 의사가 치료 배정 인지 → 평가 bias 가능성. 단 PFS는 blinded independent central review로 1차 평가.
- **HR-음성 코호트 소규모**: n=40+18, P값 미제공(탐색적). HR 0.46이지만 95% CI 0.24–0.89로 폭 넓음.
- **Biomarker 탐색 부재**: T-DXd 반응 예측 biomarker(HER2 IHC score 이외)가 본 시험에서 분석되지 않음. 최소 HER2 발현 역치는 후속 연구(NCT04494425, NCT04132960)에서 진행 중.

---

## Results

### Dataset별 결과

#### Cohort 1 — HR-양성 코호트 (1차 endpoint)

- **Dataset**: 전이성 HR-양성, HER2-low 유방암. n=331(T-DXd) vs. 163(PC). 전체 557명 중 88.7%.
- **목적**: 1차 endpoint(PFS) 검증.
- **사용한 데이터 규모**: 331+163=494명. 중앙 추적 기간 18.4개월(95% CI 17.7–18.9).
- **Baseline / 비교 대상**: 의사 선택 화학요법(eribulin 51.1%, capecitabine 20.1%, nab-paclitaxel 10.3%, gemcitabine 10.3%, paclitaxel 8.2%). 두 군의 기저 특성 균형(Table 1): 중앙 연령 56.8 vs. 55.7세, CDK4/6 억제제 이전 투여 70.4% vs. 70.6%, 간 전이 74.6% vs. 71.2%, 전이성 치료 중앙 3라인.
- **Metric**: mPFS(blinded independent central review), OS, ORR, DOR.
- **주요 수치 — PFS**: T-DXd 10.1개월(95% CI 9.5–11.5) vs. PC 5.4개월(95% CI 4.4–7.1), HR 0.51(95% CI 0.40–0.64), P<0.001.
- **주요 수치 — OS**: T-DXd 23.9개월(95% CI 20.8–24.8) vs. PC 17.5개월(95% CI 15.2–22.4), HR 0.64(95% CI 0.48–0.86), P=0.003.
- **주요 수치 — ORR**: T-DXd 52.6%(95% CI 47.0–58.0) vs. PC 16.3%(95% CI 11.0–22.8). CR: 3.6% vs. 0.6%. DOR 중앙 10.7 vs. 6.8개월.
- **Disease control rate**: T-DXd 88.0% vs. PC 66.3%.
- **논문 주장과의 연결**: 1차 endpoint 달성(PFS), sequential testing에서 OS도 interim stopping boundary(P=0.0075) 통과.
- 해석: HR 0.51은 사전 가정(HR 0.68)보다 훨씬 큰 효과 크기. 현재 후기 라인 치료 기준에서 실질적으로 의미 있는 개선.

#### Cohort 2 — 전체 환자 (핵심 2차 endpoint)

- **Dataset**: HER2-low 전이성 유방암 전체. n=373(T-DXd) vs. 184(PC).
- **주요 수치 — PFS**: T-DXd 9.9개월(95% CI 9.0–11.3) vs. PC 5.1개월(95% CI 4.2–6.8), HR 0.50(95% CI 0.40–0.63), P<0.001.
- **주요 수치 — OS**: T-DXd 23.4개월(95% CI 20.0–24.8) vs. PC 16.8개월(95% CI 14.5–20.0), HR 0.64(95% CI 0.49–0.84), P=0.001.
- **ORR**: 52.3%(95% CI 47.1–57.4) vs. 16.3%(95% CI 11.3–22.5).
- **논문 주장과의 연결**: HR+ 코호트와 일관된 이득, HER2-low를 단일 치료 가능 집단으로 확인.

#### Cohort 3 — HR-음성 코호트 (탐색적)

- **Dataset**: HER2-low, HR-음성 전이성 유방암. n=40(T-DXd) vs. 18(PC). 표본 소규모.
- **주요 수치 — PFS**: T-DXd 8.5개월(95% CI 4.3–11.7) vs. PC 2.9개월(95% CI 1.4–5.1), HR 0.46(95% CI 0.24–0.89). P값 미제공(탐색적 코호트).
- **주요 수치 — OS**: T-DXd 18.2개월(95% CI 13.6–NE) vs. PC 8.3개월(95% CI 5.6–20.6), HR 0.48(95% CI 0.24–0.95).
- **ORR**: 50.0%(95% CI 33.8–66.2) vs. 16.7%(95% CI 3.6–41.4).
- 해석: 방향은 일관되나 95% CI가 넓어 단독 근거로 삼기 어려움. 소표본 탐색적 코호트.

#### 안전성 분석

- **대상**: T-DXd 371명, PC 172명(최소 1 용량 투여).
- **치료 기간 중앙값**: T-DXd 8.2개월(0.2–33.3) vs. PC 3.5개월(0.3–17.6).
- **Grade ≥3 이상반응**: T-DXd 52.6% vs. PC 67.4%. 노출 조정 발생률 T-DXd 1.30/patient-year vs. PC 2.66/patient-year.
- **주요 이상반응(T-DXd)**: 오심 73.0%, 피로 47.7%, 탈모 37.7%. Grade ≥3: 호중구 감소 13.7%, 빈혈 8.1%, 피로 7.5%.
- **ILD/pneumonitis**: T-DXd 12.1%(grade 1: 3.5%, grade 2: 6.5%, grade 3: 1.3%, grade 5: 0.8%). 발생까지 중앙 129일(26–710).
- **Left ventricular dysfunction**: T-DXd에서 4.6%, grade 2 ejection fraction 감소 11.9%(T-DXd) vs. 5.8%(PC).
- **약물 관련 사망**: T-DXd 3.8% vs. PC 2.9%. 약물 관련: T-DXd pneumonitis 2명(0.5%) 등.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: HR+, 전체 환자, HR-음성 코호트 모두에서 방향 일관. IHC 1+와 IHC 2+/ISH-음성 간 PFS 차이 없음(10.3 vs. 10.1개월). CDK4/6 억제제 이전 투여 유무와 무관한 이득.
- **가장 중요한 수치**: HR+ 코호트 PFS HR 0.51(95% CI 0.40–0.64), OS HR 0.64(95% CI 0.48–0.86). 두 모두 interim stopping boundary 통과.
- **baseline 대비 차이**: ORR 52.6% vs. 16.3%는 약 3.2배 차이. 기존 후기 라인 화학요법 ORR 10–20% 수준 대비 현저한 개선.
- **결과 해석 시 주의점**: 개방 라벨 설계, HR-음성 코호트 소규모, IHC 재현성 우려. 또한 DFS가 아닌 mPFS로, 후속 치료 cross-over 여부가 OS 해석에 영향 가능.

---

## Figures

#### Figure 1 — Kaplan-Meier Analysis of PFS and OS

- **이 Figure가 필요한 이유**: 논문의 핵심 primary endpoint(HR+ PFS)와 sequential testing OS 결과를 시각적으로 한 번에 보여주기 위한 4-panel KM 곡선.
- **이 Figure가 뒷받침하는 주장**: T-DXd가 HR+ 코호트 PFS에서 우월하고, OS에서도 통계적으로 유의하게 개선됨.

##### 패널별 설명
- **A — HR+ 코호트 PFS**: T-DXd(n=331) vs. PC(n=163). 곡선 조기 분리, 이후 일관된 분리 유지. mPFS 10.1 vs. 5.4개월, HR 0.51, P<0.001.
- **B — 전체 환자 PFS**: T-DXd(n=373) vs. PC(n=184). mPFS 9.9 vs. 5.1개월, HR 0.50, P<0.001. A와 유사한 곡선 패턴.
- **C — HR+ 코호트 OS**: mOS 23.9 vs. 17.5개월, HR 0.64, P=0.003. 분리는 더 완만하나 분명.
- **D — 전체 환자 OS**: mOS 23.4 vs. 16.8개월, HR 0.64, P=0.001. C와 유사.

##### 본문에서 강조한 비교
- 비교 대상: T-DXd vs. 의사 선택 화학요법.
- 관찰된 차이: PFS에서 HR 0.50–0.51로 진행/사망 위험 약 50% 감소. OS에서 약 36% 사망 위험 감소.
- 이 차이가 의미하는 것: 통계적으로나 임상적으로 meaningful한 이득. OS P값이 interim stopping boundary를 초과함으로써 사전 계획된 sequential testing 모두 통과.

##### 해석 시 주의점
- KM 곡선 추적 후반부 at-risk 수가 감소해 꼬리 부분 신뢰도 낮음. Censoring 비율과 시점은 supplementary 확인 필요.
- 추정: 개방 라벨 설계로 인한 평가 bias는 KM 곡선 형태보다 탐색적 investigator-assessed endpoint에서 더 클 수 있음.

#### Figure S2 — Subgroup Analysis of PFS (HR+ Cohort)

- **이 Figure가 필요한 이유**: 다양한 하위집단(IHC score, CDK4/6 이전 투여, 지역, 연령 등)에서 일관된 이득을 보여 외부 타당성 및 결과의 robustness를 지지.
- **이 Figure가 뒷받침하는 주장**: T-DXd의 PFS 이득은 특정 하위집단에 국한되지 않고 broad population에 적용.
- 해석: Forest plot 형태. 대부분 하위집단에서 HR <1로 T-DXd 방향. 단 일부 소규모 하위집단에서 CI가 1을 포함.

#### Figure S3 — HR-음성 코호트 PFS/OS

- **이 Figure가 필요한 이유**: 탐색적 HR-음성 코호트에서도 방향성 일관성을 보여 주는 보조 근거.
- 주의점: 소규모(n=40+18)로 신뢰도 제한.

#### Figure S4 — Antitumor Activity (Waterfall plot 등)

- **이 Figure가 필요한 이유**: ORR 52.6% 및 tumor shrinkage의 깊이를 개별 환자 수준에서 시각화.
- 주의점: Waterfall plot은 최적 반응 기준이며 DOR과 함께 해석해야 함.

#### Figure S5 — HER2-Low Testing Algorithm

- **이 Figure가 필요한 이유**: VENTANA HER2/neu (4B5) IUO Assay를 이용한 HER2-low 판정 흐름을 실제 screening 대상 713명 데이터로 보여줌.
- 해석: Companion diagnostic 개발 맥락에서 assay 적용의 실현 가능성 근거.

---

## Tables

#### Table 1 — 기저 인구통계 및 임상 특성

- **이 Table이 필요한 이유**: 두 치료군(T-DXd vs. PC)의 균형을 확인해 randomization 성공 여부 입증.
- **이 Table이 뒷받침하는 주장**: 무작위 배정이 두 군 간 교란 요인을 균형 잡았음.
- **표 구조**: Row = 특성 항목, Column = HR+ 코호트 T-DXd / PC / 전체 환자 T-DXd / PC.
- **핵심 수치**: 중앙 연령 56.8 vs. 55.7세(HR+), CDK4/6 억제제 이전 투여 70.4% vs. 70.6%, HER2 IHC 1+ 58.3% vs. 58.3%, ECOG 0 56.5% vs. 58.3%, 간 전이 74.6% vs. 71.2%, 전이성 치료 중앙 3라인(1–9).
- **해석 시 주의점**: 중앙 3라인이라는 높은 사전 치료 이력은 대조군 반응률이 낮은 이유 중 하나. 전체의 62.7–67.4%가 3라인 이상 이전.

#### Table 2 — Overall Efficacy

- **이 Table이 필요한 이유**: HR+ 코호트, 전체 환자, HR-음성 코호트의 PFS, OS, ORR 수치를 한 표로 정리해 cross-cohort 비교 가능.
- **이 Table이 뒷받침하는 주장**: 1차 및 핵심 2차 endpoint 모두 통계적으로 유의.
- **표 구조**: Row = 변수(PFS, OS, ORR 등), Column = 코호트별(HR+, 전체, HR-음성) T-DXd/PC 값.
- **핵심 수치**:
  - HR+ PFS HR 0.51(95% CI 0.40–0.64), P<0.001
  - 전체 PFS HR 0.50(95% CI 0.40–0.63), P<0.001
  - HR-음성 PFS HR 0.46(95% CI 0.24–0.89), P 미제공
  - HR+ OS HR 0.64(95% CI 0.48–0.86), P=0.003
  - 전체 OS HR 0.64(95% CI 0.49–0.84), P=0.001
  - HR-음성 OS HR 0.48(95% CI 0.24–0.95), P 미제공
  - HR+ ORR T-DXd 52.6% vs. PC 16.3%; DOR 10.7 vs. 6.8개월
- **본문에서 강조한 비교**: P값이 사전 계획된 interim stopping boundary(0.0075)를 통과 → trial 조기 성공 판정.

#### Table 3 — Drug-Related Adverse Events (≥20% 환자)

- **이 Table이 필요한 이유**: T-DXd의 독특한 안전성 profile(특히 ILD/oсtopenia/ILD)을 화학요법 대조군과 비교.
- **이 Table이 뒷받침하는 주장**: Grade ≥3 이상반응은 T-DXd가 PC보다 낮음(52.6% vs. 67.4%). 단 ILD 위험은 T-DXd 고유.
- **표 구조**: Row = 이상반응 종류, Column = T-DXd(All grades / Grade ≥3) vs. PC(All grades / Grade ≥3).
- **핵심 수치**:
  - 오심: T-DXd 73.0%(Grade ≥3 4.6%) vs. PC 23.8%(0%)
  - 호중구 감소: T-DXd 33.2%(Grade ≥3 13.7%) vs. PC 51.2%(Grade ≥3 40.7%)
  - 빈혈: T-DXd 33.2%(8.1%) vs. PC 22.7%(4.7%)
  - 피로: T-DXd 47.7%(7.5%) vs. PC 42.4%(4.7%)
  - 탈모: T-DXd 37.7%(0%) vs. PC 32.6%(0%)
- **해석 시 주의점**: Grade ≥3 호중구 감소는 PC가 훨씬 높음(40.7% vs. 13.7%). 이는 eribulin/taxane 계열의 알려진 독성. ILD(12.1%)는 별도 adjudication committee 판정이므로 정의 엄격.

#### Table S1 — HER2-Low Scoring Algorithm (Supplementary)

- VENTANA HER2/neu (4B5) IUO Assay의 HER2-low 판정 기준. 0, 1+, 2+, 3+ 구분 알고리즘. Companion diagnostic 개발의 핵심 참조 문서.

#### Table S4 — Overall Safety Summary (Supplementary)

- 전체 이상반응 요약. 노출 조정 발생률(EAIR) Table S5와 함께 safety profile의 상세 근거.

---

## Supplementary Information

- **Supplementary Appendix (nejmoa2203690_appendix.pdf, 30 pages)**:
  - List of Investigators (page 2–7): 전 세계 44개국 이상 참여 기관 목록.
  - Supplementary Methods (page 8–11): 무작위 배정 세부 사항, IHC/ISH assay 상세, 통계 분석 계획(SAP) 보충.
  - Figure S1: Patient Disposition — 713명 스크리닝 → 557명 무작위 배정 흐름.
  - Figure S2: Subgroup Analysis (HR+ PFS Forest plot).
  - Figure S3: HR-음성 코호트 KM curves.
  - Figure S4: Antitumor Activity (waterfall, spider plots).
  - Figure S5: HER2-Low Testing Algorithm flowchart.
  - Table S1: HER2-low scoring algorithm.
  - Table S2: ILD/pneumonitis management guidelines.
  - Table S3: Representativeness of study participants vs. HER2-negative 전체 집단.
  - Table S4: Overall Safety Summary.
  - Table S5: Exposure-Adjusted Incidence Rate (EAIR).
  - Table S6: Staining protocol for VENTANA 4B5 assay.
  - Table S7: Morphology and background staining acceptability criteria.
- **Protocol (nejmoa2203690_protocol.pdf)**: 전체 임상 프로토콜 및 통계 분석 계획(SAP). 본문 방법론 상세 근거.

---

## 분석 자체에 대한 메모

- 이 논문은 oncology clinical trial paper로 computational methods가 없음. core-methods는 임상시험 설계·통계 방법으로 적용.
- HR-음성 코호트의 소규모(n=58)는 논문 저자도 명시적으로 한계로 인정. 이 코호트에서 formal P값 없음.
- ILD 12.1% — T-DXd 계열 전반의 class effect 문제. grade 5(0.8%, 3명)는 약물 관련 사망으로 규제 라벨에 영향.
- Figure 1의 KM 곡선 숫자 추출: PDF 특성상 KM 데이터 숫자가 텍스트 파일에 불규칙하게 섞임. 실제 KM 수치는 Table 2의 요약 통계값을 primary reference로 사용.
- 검토필요: 논문에서 cross-over 여부(진행 후 T-DXd로 전환)가 명시되지 않음. OS 해석 시 후속 치료 영향 별도 확인 필요.
