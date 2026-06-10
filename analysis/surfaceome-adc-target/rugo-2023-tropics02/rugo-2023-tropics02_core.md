<!-- rugo-2023-tropics02_core.md -->
<!-- Executive Summary는 모든 섹션 완성 후 맨 앞에 추가 예정 -->

## Executive Summary

- **무엇**: HR+/HER2- 전이성 유방암(mBC)에서 sacituzumab govitecan(SG)이 단일 항암화학요법(TPC) 대비 전체 생존(OS)을 통계적으로 유의하게 연장한다는 Phase 3 최종 OS 분석. TROP-2 ADC가 이 subtype에서 OS benefit을 입증한 최초 Phase 3 보고.
- **모델 / 방법**: 1:1 무작위 배정(층화: 내장 전이 유무, 전이 세팅 내분비 요법 6개월 이상 여부, 전이 화학요법 라인 수). Primary endpoint는 BICR에 의한 PFS; OS는 사전 규정된 계층적 검정에서 PFS 유의 후 공식 검정 전환. Kaplan-Meier + stratified log-rank + Cox regression. Alpha 관리: Lan-DeMets Pocock spending function (two-sided 0·0223 at FA).
- **핵심 결과**:
  - ① OS — SG 14·4개월 vs TPC 11·2개월, HR 0·79 (95% CI 0·65–0·96), p=0·020
  - ② ORR — SG 21% vs TPC 14%, OR 1·63 (95% CI 1·03–2·56), p=0·035
  - ③ TROP-2 subgroup — H-score <100: HR 0·75 (95% CI 0·54–1·04); H-score ≥100: HR 0·83 (95% CI 0·62–1·11); OS benefit 전 subgroup 일관
  - ④ QoL TTD — 전신 건강/QoL 4·3 vs 3·0개월 (HR 0·75, p=0·0059); 피로 2·2 vs 1·4개월 (HR 0·73, p=0·0021)
  - ⑤ Safety — Grade ≥3 AE: SG 74% vs TPC 60%; 치료 관련 사망 1건(SG, 패혈성 쇼크)
- **우리 적용**: SEV_BRCA CTC에서 TROP-2 발현 정량화 및 ADC pitch의 임상 근거 직결. `regulatory-precedent` + `BD-opportunity` + `academic-citation` 세 가지 use_case 모두 해당.
- **심층**: 한계·재현 ROI는 `rugo-2023-tropics02_lens-academic.md` / `rugo-2023-tropics02_lens-industry.md` / `rugo-2023-tropics02_methodology-brief.md` 참고.

---

## Identity

| 항목 | 내용 |
|---|---|
| Title | Overall survival with sacituzumab govitecan in hormone receptor-positive and human epidermal growth factor receptor 2-negative metastatic breast cancer (TROPiCS-02): a randomised, open-label, multicentre, phase 3 trial |
| Authors | Rugo HS, Bardia A, Marmé F, Cortés J, Schmid P, Loirat D, Trédan O, Ciruelos E, Dalenc F, et al. (35 저자) |
| Year | 2023 |
| Venue | The Lancet, Vol. 402, pp. 1423–1433 |
| Published online | 2023-08-23 |
| DOI | 10.1016/S0140-6736(23)01245-X |
| PMID | 37633306 |
| Citation key | `@rugo2023tropics02` |
| Funding | Gilead Sciences |
| ClinicalTrials.gov | NCT03901339 |
| Document type | Phase 3 RCT (planned final OS analysis) |

---

## Background

### 배경 스토리

- **문제의 출발점**: HR+/HER2- mBC는 유방암의 약 70%를 차지하는 가장 흔한 subtype이다. 국제 가이드라인은 CDK4/6 억제제를 포함한 순차적 내분비 요법을 권장하지만, 내분비 요법 내성이 발생하면 이후 선택지는 단일 항암화학요법으로 제한되며 반응률이 낮고 독성이 누적된다.
- **선행 접근 A (표준 화학요법)**: 에리불린, 비노렐빈, 카페시타빈, 겜시타빈 등 단일 항암제가 후기 라인에서 사용되어 왔다. EMBRACE, Study 301 등 Phase 3 데이터가 있지만, HR+ 세팅에서 OS 개선은 일관되게 입증되지 않았다. 특히 HR+ 환자를 포함한 풀링 분석에서 에리불린이 OS를 유의하게 개선하지 못했다.
- **A의 한계**: 전이 세팅 후기 라인에서 단일 화학요법의 중앙값 PFS는 2–4개월에 그치고, ORR은 10–15% 수준이다. 이 세팅을 타깃으로 한 phase 3 데이터가 거의 없었고, 특히 CDK4/6 억제제 사후 치료 표준이 불분명했다.
- **선행 접근 B (TROP-2 ADC 개발)**: Trop-2(trophoblast cell-surface antigen 2; TACSTD2)는 유방암을 포함한 다수 종양에서 높게 발현되는 transmembrane calcium signal transducer로 불량 예후와 연관된다. Sacituzumab govitecan(SG)은 인간화 항-Trop-2 항체에 topoisomerase I 억제제 SN-38을 hydrolysable linker로 결합한 first-in-class ADC이다. 고약물-항체 비율(7.6:1), 친수성 linker의 빠른 가수분해, bystander effect(Trop-2 미발현 인접 세포에도 SN-38 방출)가 특징이다. ASCENT 시험에서 mTNBC에 OS benefit을 입증했고, IMMU-132-01 단일군 시험(NCT01631552)에서 HR+/HER2- 세팅에서도 활성을 시사했다.
- **B의 한계(TROPiCS-02 이전)**: HR+/HER2- 세팅에서 SG의 무작위 Phase 3 검증이 없었다. 또한 TROP-2 발현이 SG 효능 예측 biomarker로 기능하는지에 대한 근거가 부족했다. TROPiCS-02 primary PFS 분석(Bardia 2022, J Clin Oncol) 시점에서는 OS 미성숙(HR 0·84, p=0·13)이었으므로, 이 논문은 사전 계획된 최종 OS 분석 보고다.
- **이 논문으로 이어지는 gap**: CDK4/6 억제제 이후 내분비 내성 HR+/HER2- mBC 환자에서 SG가 단일 화학요법 대비 OS를 연장하는지, 그리고 TROP-2 발현 수준이 그 효과를 조절하는지 확인할 무작위 Phase 3 최종 분석이 필요했다.

### 기본 개념

- **TROP-2 (Trophoblast cell-surface antigen 2)**: TACSTD2 유전자가 코딩하는 transmembrane 단백질. 세포 내 칼슘 신호 transducer. 유방암의 약 80%에서 발현; 발현이 높을수록 불량 예후와 연관. ADC payload 표적으로 적합한 이유: 항체 결합 후 내재화, 높은 발현 빈도, SN-38의 세포 독성.
- **Sacituzumab govitecan (SG, Trodelvy)**: Anti-Trop-2 humanized IgG1κ × SN-38 (irinotecan 활성 대사체). 고 DAR(7.6:1), hydrolysable linker → 종양 미세환경에서 SN-38 방출 → bystander effect. 10 mg/kg IV day 1, 8, q21d 투여.
- **H-score (histochemical score)**: IHC 염색 강도와 양성 세포 비율을 곱한 반정량 점수 (범위 0–300). 이 논문에서는 validated cutoff 없이 연속 변수 또는 <100 / ≥100으로 탐색적 분류.
- **Hierarchical testing**: PFS 통계적 유의 → OS 공식 검정 전환 → ORR → QoL TTD 순 계층 검정 구조. Alpha 소비 함수(LD-Pocock): OS 최종 분석 기준 two-sided α=0·0223.
- **CDK4/6 inhibitor (사이클린-의존성 인산화효소 4/6 억제제)**: 팔보시클립, 리보시클립, 아베마시클립 등. HR+ mBC 1차 내분비 병용 표준. TROPiCS-02는 CDK4/6 억제제 사용 후 환자를 대상으로 한다.
- **TPC (treatment of physician's choice)**: 에리불린, 카페시타빈, 겜시타빈, 비노렐빈 중 임상의 선택.

### 이 논문의 필요성

- **핵심 이유**: CDK4/6 억제제가 표준이 된 현재, CDK4/6 억제제 이후 HR+/HER2- mBC에서 OS를 개선하는 systemic therapy가 없었다.
- **기존 방법으로 부족했던 지점**: 단일 화학요법은 후기 라인에서 OS benefit 미입증; 이전 TROPiCS-02 primary analysis는 OS 미성숙.
- **이 논문이 해결하려는 방향**: 사전 계획된 final OS analysis로 SG의 OS 개선 통계적 공식 검정 완수 + TROP-2 발현 subgroup, CDK4/6 시퀀싱, QoL 포함 2차 endpoint 전체 보고.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: CDK4/6 억제제를 포함한 내분비 치료 + 2–4 라인 화학요법 이력이 있는 HR+/HER2- 국소 재발 불가 또는 전이성 유방암 환자에서, SG (10 mg/kg d1, d8, q21d) vs TPC(에리불린·비노렐빈·카페시타빈·겜시타빈 중 임상의 선택)의 OS 비교 우월성 검정.
- **입력**: 성인(≥18세), ECOG PS 0–1, 측정 가능 병변 ≥1개(RECIST 1.1), HR+ HER2- 확인, 이전 내분비 ≥1회 + taxane + CDK4/6 억제제 + 전이 세팅 화학요법 2–4 라인.
- **출력**: OS (사망까지 기간), PFS, ORR, QoL TTD (global health status/QoL, 피로, 통증).
- **추정 대상**: OS에서 SG의 hazard ratio (death) vs TPC.
- **중요한 hidden assumption**: 층화 무작위 배정으로 비교 가능 baseline. Open-label이므로 placebo effect, 의사 편향, crossover effect가 OS 해석에 영향 가능.

### 확률 / 통계학적 구조

- **Model family**: Kaplan-Meier 생존 추정 + stratified log-rank test (OS, PFS) + Cox proportional hazard regression.
- **Likelihood / objective**: OS에서 사망 사건(event)을 dependent variable로 한 생존 분석. Cox model에서 HR = exp(β); β는 partial likelihood maximization.
- **Prior / regularization**: 없음 (frequentist framework). Alpha spending: Lan-DeMets LD-Pocock function이 OS 중간 분석에서 alpha를 소비. 최종 분석의 two-sided significance level 0·0223 (390 events 기준, 실제 390 events).
- **Latent variable / hidden state**: 없음 (직접 생존 관찰).
- **Inference / optimization**: Stratified log-rank test로 OS 검정. Cox regression은 unstratified로 subgroup 분석에 사용 (주의점: subgroup HR은 unstratified).
- **Noise, sparsity, uncertainty 처리**: Censoring은 마지막 생존 확인일. 95% CI for median OS: Brookmeyer-Crowley method. Multiple testing: ORR은 OS가 유의한 경우에만 검정 (계층 구조). QoL 3 endpoints: Maurer-Bretz graphical approach (1/3 α each).
- **Sample size**: n=543 (SG=272, TPC=271); safety population SG=268, TPC=249. TROP-2 evaluable=462 (85%).

### 핵심 method insight

- **기존 방법의 한계**: 비무작위 단일군 시험(IMMU-132-01) 또는 화학요법 간 직접 비교만 있었고, SG vs 표준 화학요법의 OS 비교는 없었다. Primary PFS 분석(2022)에서 OS는 사전 계획에 따라 descriptive only.
- **이 논문이 바꾼 가정**: Protocol amendment로 PFS 최종 분석과 OS 1차 중간 분석이 동시 수행 가능해졌다(실제 interim 1 events 293 ≥ required 272). 따라서 최종 OS는 LD-Pocock alpha spending을 적용한 formal superiority test로 공식 보고.
- **새로 추가한 변수 또는 구조**: TROP-2 H-score를 연속 변수 및 <100 / ≥100 subgroup으로 탐색적 분석. UGT1A1 genotype(*1/*1, *1/*28, *28/*28)에 따른 안전성 subgroup.
- **이 변화가 중요한 이유**: TROP-2를 치료 선택 biomarker로 기능시키려면 발현 수준별 OS benefit 차이를 확인해야 한다. 이 논문이 최초로 Phase 3에서 이를 탐색적으로 보고.

### 이전 방법과의 차이

- **Baseline (TROPiCS-02 primary PFS 분석, Bardia 2022)**: PFS는 BICR 평가, OS는 descriptive.
- **공통점**: 동일 환자 코호트, 동일 무작위 배정, 동일 층화 변수.
- **차이점**: 이번 보고는 OS가 primary efficacy test; ORR, QoL TTD가 formal hierarchical test 대상으로 전환. Follow-up 연장 (중앙 12·5개월, 이전 10·9개월에서 갱신).
- **차이가 크게 나타나는 조건**: OS benefit이 TROP-2 H-score 무관하게 일관된 점이 PFS 분석 시 시사와 일치.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: ITT population n=543, TROP-2 evaluable subgroup n=462.
- **Metric**: OS (primary); PFS, ORR, QoL TTD (secondary).
- **개선된 결과**: OS HR 0·79 (p=0·020), 중앙값 3·2개월 개선. ORR OR 1·63 (p=0·035). QoL TTD 유의 개선 2개 도메인.
- **Ablation 근거**: TROP-2 subgroup은 H-score <100에서 HR 0·75, ≥100에서 HR 0·83으로 방향 일치. 단 양쪽 모두 95% CI가 1을 포함 → H-score로 환자 선별하지 않아도 benefit이 설명됨.
- **정성적 효과**: 유일한 treatment-related death(SG arm 패혈성 쇼크 1건) 외 새로운 safety signal 없음. pneumonitis 없음.

### Method 관점의 한계

- **약한 assumption**: Open-label 설계로 인한 performance bias. 화학요법 선택(TPC)이 임상의에게 일임되어 있어 군 간 treatment intensity 차이 가능.
- **구현 또는 학습상의 부담**: TROP-2 IHC assay(Roche SP295 clone)가 유방암에서 표준화된 scoring algorithm 없음 — H-score가 continuous variable로 처리, validated cutoff 미존재.
- **일반화가 불확실한 조건**: 내장 전이 없는 환자 n=26으로 매우 소규모 — 이 subgroup의 임상적 해석은 제한적. Black/Asian 환자 비율 낮음(non-White 4%, but 26%는 인종 정보 미수집).

---

## Results

### Dataset별 결과

#### Dataset 1 — TROPiCS-02 ITT Population (OS primary analysis)

- **Dataset**: 전 세계 91개 센터(북미 + 유럽), 2019-05-30 ~ 2021-04-05 무작위 배정, data cutoff 2022-07-01.
- **목적**: SG vs TPC의 OS 우월성 공식 검정.
- **사용한 데이터 규모**: n=543 (SG=272, TPC=271); 390 OS events (SG=191, TPC=199); 중앙 follow-up 12·5개월 (IQR 6·4–18·8, SG arm) / 10·7개월 (IQR 5·6–18·3, TPC arm).
- **Baseline / 비교 대상**: TPC = 에리불린(n=130, 48%), 비노렐빈(n=63, 23%), 겜시타빈(n=56, 21%), 카페시타빈(n=22, 8%). 기준선 균형: 중앙 연령 56세(IQR 49–65), 내장 전이 95%, 이전 CDK4/6 억제제 100%, 이전 화학요법 중앙 3 라인.
- **Metric / 평가 기준**: Stratified log-rank test (two-sided α=0·0223); Kaplan-Meier; Cox HR.
- **주요 수치**:
  - OS 중앙값: SG 14·4개월 (95% CI 13·0–15·7) vs TPC 11·2개월 (95% CI 10·1–12·7)
  - HR for death: 0·79 (95% CI 0·65–0·96), p=0·020
  - 12개월 OS율: SG 61% (95% CI 55–66) vs TPC 47% (95% CI 41–53)
  - 18개월 OS율: SG 39% (95% CI 33–45) vs TPC 32% (95% CI 27–38)
  - 24개월 OS율: SG 25% (95% CI 19–31) vs TPC 21% (95% CI 16–27)
- **논문 주장과의 연결**: OS HR 0·79, p=0·020으로 사전 지정 유의 기준(α=0·0223) 충족. 임상적으로 유의한 3·2개월 중앙값 개선.
- 해석: HR 0·79는 21% 사망 위험 감소. 절대값 3·2개월 차이는 이 세팅의 후기 라인 맥락(표준 치료 OS ~11개월)에서 임상적으로 의미 있다. 단 open-label이므로 후속 치료 차이가 OS에 영향을 줬을 가능성은 배제할 수 없다.

#### Dataset 2 — ORR 및 반응 지속 기간

- **Dataset**: ITT population, BICR 평가.
- **목적**: 종양 반응률 비교 (OS 유의 후 계층 검정).
- **사용한 데이터 규모**: n=543 (SG=272, TPC=271).
- **Metric**: ORR (complete + partial response by RECIST 1.1), OR (odds ratio), clinical benefit rate (CBR = CR + PR + SD ≥6개월).
- **주요 수치**:
  - ORR: SG 21% vs TPC 14%, OR 1·63 (95% CI 1·03–2·56), p=0·035
  - Complete response: SG 2% vs TPC 0%
  - Partial response: SG 20% vs TPC 14%
  - Stable disease: SG 52% vs TPC 39%
  - CBR: SG 34% vs TPC 22%, OR 1·80 (95% CI 1·23–2·63), nominal p=0·0025
  - Median duration of response: SG 8·1개월 (95% CI 6·7–9·1) vs TPC 5·6개월 (95% CI 3·8–7·9)
- 해석: ORR 절대 차이 7%p는 작지만, 이 세팅에서 단일 화학요법 ORR 10–15%를 고려하면 상대 개선이 유의하다. 반응 지속 기간 2·5개월 차이도 임상적으로 의미 있음.

#### Dataset 3 — TROP-2 발현 subgroup (탐색적)

- **Dataset**: TROP-2 IHC evaluable n=462 (SG=238, TPC=224). IHC: Roche SP295 rabbit monoclonal 항체, H-score 0–300.
- **목적**: TROP-2 발현 수준이 SG 효능을 예측하는지 탐색.
- **Baseline**: H-score <100: SG=96, TPC=96; H-score ≥100: SG=142, TPC=128. TROP-2 ≤10 (very low): SG=34, TPC=45 (n=79).
- **Metric**: OS 중앙값, HR (unstratified Cox).
- **주요 수치 (본문 및 Table S5)**:
  - H-score <100: SG 14·6개월 (95% CI 12·7–18·1) vs TPC 11·3개월 (95% CI 10·0–13·3), HR 0·75 (95% CI 0·54–1·04)
  - H-score ≥100: SG 14·4개월 (95% CI 12·7–16·4) vs TPC 11·2개월 (95% CI 9·9–12·9), HR 0·83 (95% CI 0·62–1·11)
  - TROP-2 very low (H-score ≤10): SG 17·6개월 vs TPC 13개월, HR 0·61 (95% CI 0·34–1·08) [n=79, small sample]
- **논문 주장과의 연결**: OS benefit은 TROP-2 H-score 수준 무관하게 일관. 발현 수준에 따른 선별이 필요하지 않다는 근거.
- 해석: 양쪽 subgroup 모두 95% CI가 1을 포함하므로 각 subgroup 단독으로는 통계적 유의 미달. 전체 ITT에서 유의한 OS benefit이 TROP-2 발현 수준에 따라 크게 달라지지 않음은 bystander effect 메커니즘과 일치한다. 단 탐색적 분석이므로 해석 주의.

#### Dataset 4 — CDK4/6 억제제 사용 라인별 subgroup (Table S4)

- **Dataset**: 1L CDK4/6i n=185 (SG=84, TPC=101) vs ≥2L CDK4/6i n=350 (SG=183, TPC=167).
- **주요 수치**:
  - 1L CDK4/6i: OS SG 13·1개월 vs TPC 10·1개월, HR 0·92 (95% CI 0·66–1·28)
  - ≥2L CDK4/6i: OS SG 15·3개월 vs TPC 12·1개월, HR 0·75 (95% CI 0·58–0·97)
- 해석: CDK4/6 억제제를 ≥2L에서 사용한 환자(더 중증 prior therapy)에서 benefit이 수치적으로 더 크다. 1L CDK4/6i subgroup은 CI가 1을 포함하므로 주의. 전체 ITT benefit은 두 subgroup에서 방향이 일치한다.

#### Dataset 5 — QoL (Patient-reported outcomes)

- **Dataset**: EORTC QLQ-C30 evaluable population (SG=234, TPC=207 for global health; SG=234, TPC=205 for fatigue).
- **Metric**: TTD (time to deterioration, ≥10점 악화).
- **주요 수치**:
  - Global health status/QoL TTD: SG 4·3개월 (95% CI 3·1–5·7) vs TPC 3·0개월 (95% CI 2·2–3·9), HR 0·75 (95% CI 0·61–0·92), p=0·0059 (Figure S2)
  - Fatigue TTD: SG 2·2개월 (95% CI 1·6–2·8) vs TPC 1·4개월 (95% CI 1·1–1·9), HR 0·73 (95% CI 0·60–0·89), p=0·0021 (Figure S3)
  - Pain TTD: SG 3·8개월 vs TPC 3·5개월, HR 0·92 (95% CI 0·75–1·13), p=0·42 (유의하지 않음)
- 해석: 통증 TTD를 제외한 2개 QoL 도메인에서 SG가 TPC보다 유의하게 오래 유지. OS benefit이 QoL 악화를 수반하지 않는다는 점이 임상적으로 중요.

#### Dataset 6 — Safety (안전성)

- **Dataset**: Safety population (SG=268, TPC=249).
- **주요 수치**:
  - Any grade treatment-emergent AE: SG 198/268 (74%) Grade ≥3 vs TPC 150/249 (60%) Grade ≥3
  - Leading to treatment discontinuation: SG 17 (6%) vs TPC 11 (4%)
  - Treatment-related death: SG 1 (패혈성 쇼크 by 호중구 감소성 대장염) vs TPC 0
  - Neutropenia (all grade): SG 189 (71%) vs TPC 136 (55%); Grade ≥3: SG 138 (51%) vs TPC 97 (39%)
  - Diarrhoea (all grade): SG 166 (62%) vs TPC 57 (23%); Grade ≥3: SG 27 (10%) vs TPC 3 (1%)
  - Nausea (all grade): SG 157 (59%) vs TPC 87 (35%)
  - Alopecia: SG 128 (48%) vs TPC 46 (18%)
  - Anaemia (all grade): SG 69 (28%) vs TPC 28%
  - Febrile neutropenia Grade ≥3: SG 14 (5%) vs TPC 11 (4%)
  - Neuropathy all-grade: SG 24 (9%) vs TPC 39 (16%)
  - Relative dose intensity: SG 98·9%, eribulin 96·4%, capecitabine 86·4%, gemcitabine 86·4%, vinorelbine 98·0%
- **UGT1A1 genotype** (Table S7/S8): *28/*28 homozygous 25명에서 Grade ≥3 AE 92%, dose reduction 40%으로 wild-type(*1/*1, Grade ≥3 67%)보다 높음. 호중구 감소 Grade ≥3: wild-type 45%, heterozygous 57%, homozygous 64%.
- 해석: Grade ≥3 AE는 SG가 화학요법보다 높지만, 치료 중단으로 이어진 비율 차이는 크지 않다(6% vs 4%). Pneumonitis 없음. UGT1A1 *28/*28 homozygous에서 독성 증가는 표본 크기 소규모(n=25)로 해석 제한.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: OS benefit이 사전 정의된 모든 subgroup(인종, 내장 전이 유무, 내분비 요법 기간, 이전 화학요법 라인 수, 연령, ECOG PS, CDK4/6 억제제 기간, TROP-2 발현 수준)에서 방향 일치.
- **가장 중요한 수치**: OS HR 0·79 (p=0·020), 중앙값 14·4 vs 11·2개월.
- **Baseline 대비 차이**: ORR 21% vs 14% (OR 1·63, p=0·035); QoL TTD 2개 도메인 유의 개선.
- **결과 해석 시 주의점**:
  1. Open-label → 후속 치료 선택 차이가 OS에 미치는 영향 미통제.
  2. TROP-2 subgroup 분석은 탐색적(unstratified Cox, multiple comparisons 미보정).
  3. Visceral metastasis 없는 환자 n=26으로 일반화 불가.
  4. 인종 다양성: non-White 4%, 미수집 26% — 일반화 주의.

---

## Figures

### Figure 1 — Trial Profile (CONSORT flow diagram)

#### 패널별 설명
- 776명 screening → 543명 무작위 배정 (SG=272, TPC=271).
- 제외 151명: 포함 기준 미충족 151명(18 laboratory, 16 exclusion criteria, 48 other reason).
- Safety population: SG=268 (4명 미치료), TPC=249 (22명 미치료).
- 치료 중단: SG=259, TPC=247. 주요 사유: progressive disease (SG 217, TPC 199), adverse events (SG 18, TPC 11).
- 연구 종료 시 치료 중인 환자: SG=9, TPC=2.

#### 본문에서 강조한 비교
- TPC 미치료 22명 중 consent 철회 11명, AE 11명으로 SG보다 높은 미치료율 (8% vs 1.5%).
- SG arm 치료 중단 사유: 병이 진행된 경우가 84%로 압도적으로 많음 — 선택 편향 방향 SG에 불리.

#### 해석 시 주의점
- TPC 미치료 환자(n=22) 중 일부는 무작위 배정 후 상태 악화로 치료 불가 → ITT 분석에 포함되어 TPC arm에 불리하게 작용할 수 있음.

---

### Figure 2 — Overall Survival Kaplan-Meier Curve (ITT population)

#### 패널별 설명
- X축: 시간(개월, 0–36), Y축: Overall survival probability (0–100%).
- SG(파란 실선) vs Chemotherapy(빨간 실선). 세로 해시 마크: censored.
- Table inset: SG n=272, events=191, median OS 14·4개월 (95% CI 13·0–15·7); TPC n=271, events=199, median OS 11·2개월 (95% CI 10·1–12·7). HR 0·79 (95% CI 0·65–0·96), p=0·020.
- At-risk 테이블: 36개월 시점 SG 0명, TPC 0명(follow-up 완료).

#### 본문에서 강조한 비교
- 곡선은 무작위 배정 직후부터 분리 시작, 30개월 이상 유지.
- 12개월 OS율 절대차: 61% vs 47% (14%p); 18개월 39% vs 32% (7%p).

#### 해석 시 주의점
- Crossing 없이 지속적 분리 — PH assumption 비교적 만족.
- 36개월 이후 데이터 없으므로 장기 생존 tail 불명확.

---

### Figure 3 — Forest Plot: Subgroup Analysis of OS

#### 패널별 설명
- X축: HR (death), 범위 0·0625–16 (log scale). Vertical reference line at 1.
- 사전 정의된 subgroup: 인종(White n=362, Non-White n=42), 내장 전이(Yes n=517, No n=26), 내분비 요법 ≥6개월(Yes n=469, No n=74), 이전 화학요법 라인(≤2 n=233, ≥3 n=310), 연령(<65 n=403, ≥65 n=140), ECOG PS(0 n=241, 1 n=302), CDK4/6i 기간(≤12개월 n=327, >12개월 n=208), TROP-2 발현(H-score <100 n=192, H-score ≥100 n=270).
- 전체 HR (Overall, n=543): 0·80 (95% CI 0·66–0·98).

#### 본문에서 강조한 비교
- 모든 subgroup에서 HR <1 (SG 유리 방향).
- 내장 전이 없는 환자(n=26): HR 2·63 (95% CI 0·95–7·29) — 매우 wide CI, 반전 경향 보이지만 tiny n.
- CDK4/6i ≤12개월 subgroup: HR 0·68 (95% CI 0·53–0·88); >12개월: HR 0·98 (0·71–1·37) — duration 별 benefit 차이.

#### 해석 시 주의점
- Subgroup HRs는 unstratified Cox로 계산 — multiplicity 보정 없음. 탐색적 해석만 가능.
- 내장 전이 없는 그룹(n=26)은 표본 크기가 극히 작아 HR 방향 신뢰 불가.
- Overall HR이 Figure 2 (0·79)와 Forest plot의 overall (0·80)로 미세하게 다른 것은 stratified vs unstratified Cox 차이.

---

## Tables

### Table 1 — Patient Demographics and Baseline Characteristics

주요 내용 (Figure 1 상단 삽입, p.1427):
- 중앙 연령: SG 57세 (IQR 49–65), TPC 55세 (48–63). 여성 99%.
- 내장 전이: SG 259 (95%), TPC 258 (95%).
- Previous CDK4/6i ≤12개월: SG 161 (59%), TPC 166 (61%).
- 이전 내분비 요법 ≥6개월 (전이 세팅): SG 235 (86%), TPC 234 (86%).
- 이전 화학요법 라인 중앙값: SG 3 (IQR 2–3), TPC 3 (IQR 2–3). ≥3 라인: SG 159 (58%), TPC 151 (56%).
- TROP-2 evaluable: SG 238 (88%), TPC 224 (83%). H-score <100: SG 96/238 (40%), TPC 96/224 (43%). H-score ≥100: SG 142/238 (60%), TPC 128/224 (57%).
- 해석: 두 군 기준선 균형 양호. CDK4/6i 사용 비율, 이전 화학요법 라인 수, TROP-2 분포 유사.

---

### Table 2 — Summary of Treatment Efficacy

| 항목 | SG (n=272) | TPC (n=271) |
|---|---|---|
| OS 중앙값, 개월 (95% CI) | 14·4 (13·0–15·7) | 11·2 (10·1–12·7) |
| HR (95% CI), p | 0·79 (0·65–0·96), p=0·020 | — |
| 12개월 OS율 | 61% (55–66) | 47% (41–53) |
| 18개월 OS율 | 39% (33–45) | 32% (27–38) |
| 24개월 OS율 | 25% (19–31) | 21% (16–27) |
| ORR, n (%) | 57 (21%) | 38 (14%) |
| OR (95% CI), p | 1·63 (1·03–2·56), p=0·035 | — |
| CBR, n (%) | 92 (34%) | 60 (22%) |
| OR CBR (95% CI), p | 1·80 (1·23–2·63), p=0·0025 | — |
| 반응 지속기간 중앙값, 개월 (95% CI) | 8·1 (6·7–9·1) | 5·6 (3·8–7·9) |

ORR은 통계적 검정 계층상 OS가 유의한 후 검정 — 공식 유의 확인.

---

### Table 3 — Summary of Treatment-Emergent Adverse Events

| 항목 | SG (n=268) | TPC (n=249) |
|---|---|---|
| Grade ≥3 | 198 (74%) | 150 (60%) |
| 치료 중단 | 17 (6%) | 11 (4%) |
| Dose delay | 178 (66%) | 109 (44%) |
| Dose reduction | 90 (34%) | 82 (33%) |
| Serious events | 74 (28%) | 48 (19%) |
| Leading to death | 6 (2%) | 0 |
| Treatment-related death | 1 (<1%) | 0 |

6건의 치료 중 사망 중 1건(패혈성 쇼크)만 치료 관련으로 판정; 나머지 5건(COVID-19 폐렴, 폐색전, 폐렴, 신경계 장애, 부정맥)은 치료 무관.

---

## Supplementary Information

### Supplementary Figure S1 — Hierarchical Testing Procedure
- PFS (BICR, ITT, 2-sided α=0·05) → 유의 시 OS 1차 중간 분석(IA1) → OS 2차 중간 분석(IA2) → OS 최종 분석(FA) → ORR (BICR, ITT, α=0·05) → QoL TTD 3개 도메인 (Maurer-Bretz, 1/3 α each).
- 이 논문은 OS IA2에 해당 (실제 첫 번째 공식 superiority 검정이 IA2로 전환된 경위는 추가 Methods 참조).

### Supplementary Figure S2 — Global Health Status/QoL TTD (Kaplan-Meier)
- SG 4·3개월 (95% CI 3·1–5·7) vs TPC 3·0개월 (95% CI 2·2–3·9), HR 0·75 (95% CI 0·61–0·92), p=0·0059.
- SG n=234, events 210; TPC n=207, events 185.

### Supplementary Figure S3 — Fatigue TTD (Kaplan-Meier)
- SG 2·2개월 (95% CI 1·6–2·8) vs TPC 1·4개월 (95% CI 1·1–1·9), HR 0·73 (95% CI 0·60–0·89), p=0·0021.
- SG n=234, events 218; TPC n=205, events 191.

### Supplementary Table S1 — Study Participant Representativeness
- 북미 229명(42%), 유럽 314명(58%). 여성 538명(99%).
- 인종: White 362 (67%), Black 21 (4%), Asian 16 (3%), 미수집 139 (26%).
- 연구 집단이 HR+/HER2- mBC 전체 인구 대비 약간 더 젊음(중앙 56세 vs 50–64세 범주).

### Supplementary Table S2 — Patient Demographics by CDK4/6i Line
- 1L CDK4/6i (n=185): SG 84, TPC 101 — 이전 화학요법 2 라인이 SG 56%, TPC 50%.
- ≥2L CDK4/6i (n=350): SG 183, TPC 167 — 이전 화학요법 3–4 라인이 SG 66%, TPC 63%.

### Supplementary Table S3 — Patient Demographics by TROP-2 H-score
- H-score <100 (SG n=96, TPC n=96) vs H-score ≥100 (SG n=142, TPC n=128).
- 두 subgroup 기준선 유사; ECOG PS 1이 H-score <100에서 다소 높음(SG 63%, TPC 49%).

### Supplementary Table S4 — PFS and OS by CDK4/6i Line
- 1L CDK4/6i: PFS HR 0·64 (95% CI 0·43–0·94); OS HR 0·92 (0·66–1·28).
- ≥2L CDK4/6i: PFS HR 0·66 (95% CI 0·51–0·87); OS HR 0·75 (0·58–0·97).

### Supplementary Table S5 — PFS and OS by TROP-2 H-score
- H-score <100: PFS SG 5·3개월 vs TPC 4·0개월, HR 0·77 (0·54–1·09); OS HR 0·75 (0·54–1·04).
- H-score ≥100: PFS SG 6·4개월 vs TPC 4·1개월, HR 0·60 (0·44–0·81); OS HR 0·83 (0·62–1·11).

### Supplementary Table S6 — Treatment-Related AEs (any grade ≥10%, Grade ≥3 ≥5%)
- SG 주요 Grade ≥3 AEs: neutropenia 136/268 (51%), diarrhea 25/268 (9%), fatigue 15/268 (6%).
- TPC 주요 Grade ≥3 AEs: neutropenia 95/249 (38%), thrombocytopenia 9/249 (4%), neuropathy 6/249 (2%).
- SG에서 diarrhea all-grade 57% (Grade ≥3 9%)가 TPC 17% (1%)보다 현저히 높음.

### Supplementary Table S7 — AEs by UGT1A1 Status
- Wild-type (*1/*1, n=103): Grade ≥3 67%, dose reduction 25%.
- Heterozygous (*1/*28, n=119): Grade ≥3 75%, dose reduction 41%.
- Homozygous (*28/*28, n=25): Grade ≥3 92%, dose reduction 40%.
- UGT1A1 genotype의 SG 독성 예측 가능성 시사. 단 *28/*28 n=25로 소규모.

### Supplementary Table S8 — AEs of Special Interest by UGT1A1 Status
- Neutropenia Grade ≥3: wild-type 45%, heterozygous 57%, homozygous 64%.
- Diarrhea Grade ≥3: wild-type 6%, heterozygous 13%, homozygous 24%.
- *28/*28 homozygous에서 diarrhea Grade ≥3가 4배 높음.

### Additional Methods (Appendix p.5)
- Alpha spending 전략: LD-Pocock (Pocock approximating Lan-DeMets). OS IA1에서 power 70%까지 제공 가능. ASCENT mTNBC 결과 기반으로 조기 검정 이점 기대.
- Major amendments: 원래 dual primary(ORR + PFS by local investigator) → protocol amendment로 BICR PFS 단일 primary로 전환. Protocol amendment 7에서 PFS 최종 분석 시 non-comparative OS 계획 → 실제 IA1 events(293) ≥ required(272)로 superiority test 전환.

---

## 분석 자체에 대한 메모

- 이 논문은 TROPiCS-02 trial의 primary PFS 분석(Bardia A et al., J Clin Oncol 2022;40:3365-76)의 후속으로 나온 final OS 보고다. gu-2024-tropics02-hrplus는 이 논문의 Correspondence letter(TROP-2 IHC 발현 기준 선별 관련).
- TROP-2 H-score subgroup 분석은 exploratory이고 unstratified Cox. Multiple comparisons 보정 없음. H-score cutoff validation 없음 — 이 점이 biomarker로서 TROP-2의 임상 활용 한계.
- UGT1A1 genotype 분석에서 *28/*28 n=25는 소규모로 결론 도출에 주의 필요.
- 후속 치료(post-progression therapy) 정보가 이 보고에 없어 OS에 대한 교란 요인 통제 불가.
- 이 논문의 승인 근거 역할: 미국 FDA 2023-02, EU EMA 2023-07 — HR+/HER2- (IHC0, IHC1+, IHC2+/ISH-) mBC에서 내분비 치료 + ≥2 systemic therapies 이후 적응증 확대.
