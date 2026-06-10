# proszek-2025-adc-ctc-resistance — Core Analysis

## Executive Summary

- **무엇**: T-DXd(trastuzumab deruxtecan, HER2 타겟 ADC)에 대한 실세계 내성 기전 규명. Caris Life Sciences의 보험청구 데이터와 다기관 종양 multi-omic profiling(WTS + NGS + IHC/CISH)을 통합한 2,799명 코호트에서 T-DXd-specific OS 예측 유전자와 치료 유도 mutation을 동정했다.
- **모델 / 방법**: Multivariate Cox proportional hazards regression — 96개 전사체 feature(11개 curated pathway)를 pre-T-DXd 조직 RNA TPM 연속 변수로 입력, T-DXd-specific OS를 outcome으로 분석. 추가로 pre/post-T-DXd 비교 집단(unmatched)에서 somatic mutation 농축 분석(Chi-square + BH correction, $q < 0.05$).
- **핵심 결과**:
  - ① *ERBB2*(HER2) 고발현 → T-DXd-specific OS 연장 (ERBB2 Q4 중앙값 27.3개월 vs Q1 13.2개월, p<0.0001)
  - ② *ABCC1*(MRP1, drug efflux pump) 고발현 → OS 단축 (Q4 14.2개월 vs Q1 22.0개월, p<0.0001); HER2 독립적 예측인자
  - ③ Post-T-DXd 샘플에서 *ERBB2*, *SMAD4*, *NFE2L2*, *TOP1* mutation 농축 (BH 보정 후 유의)
  - ④ HCC1954-TDXdR 세포주에서 MK-571(ABCC1 억제제) + T-DXd 병용 시 단독 대비 세포 생존율 유의미하게 추가 감소 (p<0.0001)
- **우리 적용**: ADC 내성 biomarker 패널(ABCC1 발현 + ERBB2 발현 + NFE2L2/KEAP1 mutation)로 치료 전 선제 위험 분류 모델 설계에 참조 — `academic-citation` + `BD-opportunity` 관련성 높음.
- **심층**: 한계·재현 ROI는 `proszek-2025-adc-ctc-resistance_lens-academic.md` / `proszek-2025-adc-ctc-resistance_lens-industry.md` / `proszek-2025-adc-ctc-resistance_methodology-brief.md` 참고.

---

## Identity

- **Title**: Mechanisms of resistance to trastuzumab deruxtecan in breast cancer elucidated by multi-omic molecular profiling
- **Authors**: George W. Sledge Jr., Joanne Xiu, Reshma L. Mahtani, Ana C. Sandoval Leon, Funda Meric-Bernstam, Jennifer R. Ribeiro, Ninad N. Kulkarni, Dileep R. Rampa, Jangsoon Lee, Naoto T. Ueno, Matthew J. Oberley, Milan Radovich, David B. Spetzler
- **Year**: 2025 (Received 1 Aug 2025; Accepted 16 Nov 2025; Published online 20 Dec 2025)
- **Venue**: npj Breast Cancer 12:1
- **DOI**: 10.1038/s41523-025-00868-y
- **Citation key**: `@sledge2025tdxdresistance`
- **Institutions**: Caris Life Sciences, Phoenix, AZ (주저자 소속); Miami Cancer Institute; MD Anderson Cancer Center; University of Hawai'i Cancer Center
- **Funding**: Caris Life Sciences; University of Hawai'i Cancer Center Support Grant (P30CA071789, Shared Resources: Preclinical Core)
- **Competing interests**: G.W.S., J.X., J.R.R., N.K., M.J.O., M.R., D.S.는 Caris Life Sciences 직원. 다수 저자 AstraZeneca, Daiichi Sankyo 등 복수 제약사와 consulting/advisory/research funding 관계.

---

## Background

#### 배경 스토리

- **문제의 출발점**: T-DXd는 HER2-positive 및 HER2-low 전이성 유방암에서 FDA 승인을 받고 임상적 성공을 거뒀지만, 사실상 모든 환자에서 내성이 발생한다. 전임상 연구들은 ADC 세포독성 경로의 여러 단계에서 다양한 내성 기전이 존재할 수 있음을 시사했으나, 대규모 real-world 코호트 데이터는 부재했다.

- **선행 접근 A — 전임상 세포주 모델**: T-DM1 내성에서 lysosomal proteolytic activity 저하, caveolae-mediated endocytosis, ERBB2/ERBB3 activating alteration 등이 보고됐다. T-DXd에 대해서도 유사한 기전이 제안됐으나 실제 환자 코호트에서의 검증이 없었다.

- **A의 한계**: 단일 세포주·마우스 모델 결과를 실세계 환자에 직접 외삽하기 어려움. 어떤 기전이 임상적으로 OS와 연관되는지, 치료 과정에서 어떤 mutation이 선택되는지에 대한 large-scale 데이터 없음.

- **선행 접근 B — 소규모 임상 연구**: 일부 연구들이 HER2 소실, ERBB2 kinase domain mutation, TOP1 mutation이 T-DXd 내성과 관련될 수 있음을 시사했다. 단 대부분 소규모·단일 기관.

- **B에도 남은 한계**: 다양한 경로의 feature를 동시에 multivariate 분석한 대규모 real-world 코호트 연구 부재. 특히 ABCC1(ABC transporter, drug efflux pump)이 T-DXd 내성에 기여하는지에 대한 임상 증거가 없었다.

- **이 논문으로 이어지는 gap**: 보험청구 데이터와 Caris Life Sciences의 다기관 종양 profiling을 결합하면 2,799명 규모의 T-DXd 치료 코호트를 구성할 수 있다. 이를 통해 (1) 96개 전사체 feature를 multivariate Cox regression으로 동시 스크리닝해 T-DXd-specific OS 예측인자 동정, (2) pre/post-T-DXd 조직의 mutation landscape 비교로 치료 유도 선택압 확인이 가능하다.

#### 기본 개념

- **T-DXd (trastuzumab deruxtecan)**: HER2(ERBB2)를 타겟하는 ADC. Antibody 부분이 HER2에 결합 → endocytosis → lysosomal cleavage로 payload(deruxtecan, topoisomerase I 억제제 DXd) 방출 → DNA double-strand break → 세포사. Membrane-permeable payload의 bystander effect로 HER2-low 환자에서도 효과적.

- **ABCC1 (MRP1, Multidrug Resistance Protein 1)**: ATP-binding cassette subfamily C member 1. 세포 내 약물을 능동 수송으로 외부로 배출하는 efflux pump. 고발현 시 세포 내 DXd 농도 감소 → ADC 효능 저하. 암 세포에서 다양한 화학요법 내성과 연관.

- **NFE2L2–KEAP1 축**: NFE2L2(NRF2)는 ABCC1을 포함한 해독·항산화 관련 유전자들의 전사 활성화인자. KEAP1은 NFE2L2의 negative regulator로, 정상 조건에서 NFE2L2를 단백질 분해로 억제한다. NFE2L2 gain-of-function mutation 또는 KEAP1 loss-of-function mutation → NFE2L2 과활성 → ABCC1 전사 증가 → drug efflux 증가.

- **Real-world OS 계산 방식**: 이 연구에서 T-DXd-specific OS는 "T-DXd 첫 투약일(First of T-DXd)부터 마지막 환자 접촉일(Last Contact)"로 보험청구 데이터 기반으로 계산. 표준 임상시험의 PFS·PD 기반 endpoint와 다름.

#### 이 논문의 필요성

- **핵심 이유**: T-DXd 내성 기전에 대한 대규모 real-world 데이터 공백. 전임상에서 제안된 기전들이 실제 환자 OS와 연관되는지 미확인.
- **기존 방법으로 부족했던 지점**: 단일 기관·소규모·matched pair 없이는 치료 전후 mutation 변화와 생존 예측인자를 동시에 포괄하기 어려움.
- **이 논문이 해결하려는 방향**: (1) 11개 경로에 걸친 96개 feature 동시 스크리닝으로 T-DXd-specific biomarker 발굴. (2) 2,799명 규모에서 multivariate 분석으로 독립 예측인자 확립. (3) Pre/post-T-DXd 비교로 치료 선택압으로 농축되는 mutation 동정. (4) In vitro에서 ABCC1 억제의 T-DXd 감수성 회복 효과 검증.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: (1) T-DXd로 치료된 유방암 환자 코호트에서 치료 전 종양 분자 프로파일(전사체·돌연변이·IHC)과 T-DXd-specific OS 간 multivariate 연관성 분석. (2) Pre- vs. post-T-DXd 조직 간 somatic mutation 빈도 차이 비교.
- **입력**: 조직 RNA 발현(TPM, WTS), DNA mutation 데이터(NGS), IHC/CISH HER2 상태, 보험청구 기반 OS.
- **출력**: T-DXd-specific OS와 유의미하게 연관된 유전자/RNA signature 및 HR; post-T-DXd 샘플에서 농축되는 mutation 목록.
- **추정 대상**: 각 유전자 발현의 hazard ratio (HR); post-T-DXd mutation 농축 odds (Chi-square).
- **중요한 hidden assumption**: Pre-T-DXd 샘플(n=2,420)과 post-T-DXd 샘플(n=379)은 matched pair가 아님(저자 명시). 두 집단 간 기저 특성 차이로 인한 confounding 가능성 존재.

#### 확률 / 통계학적 구조

- **Model family**: Cox proportional hazards model (multivariate). RNA TPM 값을 연속 변수로 처리.
- **Likelihood / objective**: Partial likelihood maximization. T-DXd-specific OS를 outcome, RNA TPM을 연속 입력 변수로 사용. Kaplan-Meier 분석은 log-rank test.
- **Prior / regularization**: 없음. 96개 feature를 개별 Cox regression으로 분석 후 Benjamini-Hochberg (BH) FDR 보정 ($q < 0.05$).
- **Latent variable / hidden state**: 없음 (기전적 latent variable 모델링은 없음).
- **Inference / optimization**: 표준 Cox partial likelihood. Molecular comparisons는 Chi-square test + BH 보정 ($q < 0.05$).
- **Noise, sparsity, uncertainty 처리**: 95% CI 보고. ABCC1 threshold 최적화에 5 percentile 단위 25가지 cutoff 테스트 (Supplementary Table S4). Mutation prevalence 5% VAF + 5개 이상 alignment를 positive call 기준으로 사용.

#### 핵심 method insight

- **기존 방법의 한계**: 기존 T-DXd 내성 연구는 단일 기전(HER2 소실)에 집중하거나 소규모 matched pair였음. 어떤 경로가 임상 OS와 독립적으로 연관되는지 포괄적 스크리닝 없음.
- **이 논문이 바꾼 가정**: 보험청구 DB + 다기관 종양 profiling 통합으로 unmatched이더라도 충분한 규모(N=2,799)에서 혼란변수 통제 가능.
- **새로 추가한 구조**: 96개 전사체 feature를 11개 ADC-관련 pathway로 사전 큐레이션해 동시 분석. 기존 단일 biomarker 접근 대비 경로-수준 체계적 스크리닝.
- **이 변화가 중요한 이유**: 기존 T-DXd 내성 연구에서 증거가 부족했던 efflux pump(ABCC1)를 독립 예측인자로 동정. HER2 IHC 단독으로는 포착 불가능한 예후 층화 가능성 시사.

#### 이전 방법과의 차이

- **Baseline**: HER2 IHC/CISH 단독 환자 선별, 또는 단일 biomarker 분석. 소규모 matched-pair 전후 비교.
- **공통점**: Kaplan-Meier + log-rank, Cox regression 사용.
- **차이점**: (1) Real-world 보험청구 데이터로 대규모 코호트 구성 (N=2,799). (2) 96개 feature를 사전 정의된 11개 pathway로 동시 스크리닝. (3) Pre/post-T-DXd mutation 비교를 별도 NGS 분석(N=2,799)으로 수행.
- **차이가 크게 나타나는 조건**: HER2-low, HER2-null 환자군에서 ABCC1의 독립적 예측력 — IHC 기반 HER2 분류로는 포착할 수 없는 차이를 전사체 발현이 보완.

#### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: Caris Life Sciences real-world cohort (WTS n=1,829, NGS n=2,432, 총 N=2,799).
- **Metric**: T-DXd-specific OS 중앙값(개월), Hazard Ratio, 95% CI, FDR-adjusted q-value.
- **개선된 결과**: ABCC1이 독립 예측인자로 확인(q<0.05, ERBB2 독립적). ERBB2 발현과 IHC HER2 status가 OS와 일관되게 연관.
- **Ablation 근거**: ABCC1과 상관도 높은 ABCE1(ρ=0.601), ABCB7(ρ=0.615), ABCF2(ρ=0.639)를 interaction term으로 추가해도 ABCC1이 독립 예측인자 유지 (Supp. Table S3).
- **정성적 효과**: In vitro에서 MK-571(ABCC1 억제제) + T-DXd 병용이 HCC1954-TDXdR 세포에서 단독 대비 상승 효과 확인.

#### Method 관점의 한계

- **약한 assumption**: Unmatched pre/post-T-DXd 비교 — 두 집단 간 기저 특성 차이가 mutation 농축 결과를 confound할 수 있음. 저자 명시.
- **구현 또는 학습상의 부담**: 보험청구 데이터 접근이 Caris 고유. OS 계산이 standard trial endpoint가 아닌 claims 기반으로, dead/censored 판정에 100일 보험청구 부재 기준 사용.
- **일반화가 불확실한 조건**: HER2-low, HER2-null 환자에서의 ABCC1 억제 효과는 HER2+ 세포주 두 개에서만 in vitro 검증됨. 다른 암종 외삽 불확실. MK-571은 임상 개발 단계 화합물이 아님.

---

## Results

#### Dataset별 결과

##### Dataset 1 — Caris Real-World Cohort: 전사체 발현과 T-DXd-specific OS (multivariate Cox)

- **Dataset**: Real-world breast cancer cohort, 미국 다기관, FFPE 조직 WTS + 보험청구 OS.
- **목적**: Pre-T-DXd 조직의 96개 전사체 feature와 T-DXd-specific OS 간 multivariate 연관성 확인.
- **사용한 데이터 규모**: N=1,714 (pre-T-DXd WTS 보유 + T-DXd-specific OS 데이터 가용, 전체 WTS n=1,829 중).
- **Baseline / 비교 대상**: 96개 전사체 feature(11개 pathway)를 Cox regression에 연속 변수로 투입.
- **Metric**: T-DXd-specific OS (중앙값, 개월), HR (per TPM unit change of RNA<1), 95% CI, FDR-adjusted q-value (BH method).
- **주요 수치**:
  - *ERBB2* (HER2): q<0.05 (bubble chart에서 가장 큰 원, 좌측). ERBB2 Q4 중앙 OS 24.9개월 (95% CI 22.9–32.3), Q1 13.2개월 (95% CI 11.2–14.3), p<0.0001 (Fig. 2c).
  - *ABCC1* (MRP1): q<0.05. ABCC1 Q1 중앙 OS 22.0개월 (95% CI 17.9–27.3), Q2 17.7개월, Q3 16.3개월, Q4 14.2개월 (95% CI 11.8–15.6), p<0.0001 (Fig. 2b).
  - *MKI67* (Ki-67): q<0.05, 그러나 T-DXd 비치료 환자에서도 동일 방향 OS 연관 확인 → T-DXd-specific이 아닌 general prognostic marker (Supp. Fig. S2).
  - *FCGR3A*: q<0.05 in Cox, 그러나 KM curve에서 quartile 간 OS 차이 유의하지 않음 (p=0.94, Supp. Fig. S1b).
  - *ABCA6*, *RAB6A*: 마찬가지로 유의하지 않음 (각 p=0.25, p=0.10, Supp. Fig. S1c,d).
  - ABCC1 독립 예측인자 확인: ABCE1(ρ=0.601), ABCB7(ρ=0.615), ABCF2(ρ=0.639)를 interaction term으로 포함해도 ABCC1 독립성 유지. ABCC1 Cox -log10(p) = 2.14 (Supp. Table S3).
- **정성 결과**: ABCC1 발현은 HER2 IHC 카테고리와 무관하게 모든 카테고리(HER2-positive, HER2-low, HER2-ultra-low, HER2-null)에서 비슷한 수준 유지 (Fig. 3b 우측). ERBB2 발현은 HER2 IHC 카테고리와 유의미하게 상관(예상; Fig. 3b 좌측).
- **논문 주장과의 연결**: ABCC1-mediated drug efflux가 HER2 expression level과 독립적으로 T-DXd 내성의 핵심 기전임을 지지.

해석: ERBB2와 ABCC1이 각각 반대 방향으로 OS에 영향 — "세포 내 약물 농도 ≈ HER2-mediated uptake / ABCC1-mediated efflux"라는 pharmacokinetic 프레임으로 해석 가능. 단, 이는 연관성 분석이며 직접 인과 증거는 아님.

---

##### Dataset 2 — ABCC1 Quartile 및 HER2/ERBB2 조합 분석

- **Dataset**: 동일 코호트, ABCC1·ERBB2 quartile 및 HER2 status 조합 분석.
- **목적**: ABCC1 threshold 최적화 및 HER2 status와 조합해 환자 층화 개선 여부 확인.
- **사용한 데이터 규모**: ABCC1 분석: N=1,829 (WTS 보유). HER2 status 기반 KM: N=322(HER2-positive), 572(HER2-low), 332(HER2-ultra-low), 332(HER2-null).
- **Metric**: T-DXd-specific OS 중앙값(개월), log-rank p.
- **주요 수치**:
  - ABCC1 Q4(high) vs Q1-3(low, 75th percentile cutoff): 14.2개월 vs 17.8개월, p=0.0021; HR=0.7961, 95% CI [0.6883–0.9207] (Fig. 4a; Supp. Table S4).
  - HER2 status별: HER2-positive 27.3개월, HER2-low 17.5개월, HER2-ultra-low 12.7개월, HER2-null 10.8개월, p<0.0001 (Fig. 4b).
  - ABCC1 Q1-3/HER2-low 최고 19.3개월 vs ABCC1 Q4/HER2-null 최저 8.0개월 (Fig. 4c).
  - ABCC1 Q1-3/ERBB2 Q4 최고 27.9개월 vs ABCC1 Q4/ERBB2 Q1-3 최저 11.2개월 (Fig. 4d).
- **정성 결과**: ABCC1은 HER2 IHC 카테고리 내에서도 추가 예측력 제공. ABCC1 status가 HER2-low와 HER2-null 환자 층화에 특히 기여.
- **논문 주장과의 연결**: ABCC1 상태가 HER2/ERBB2 발현과 독립적이고 보완적으로 T-DXd 치료 결과를 예측함.

---

##### Dataset 3 — Post-T-DXd Mutation Enrichment Analysis (Unmatched NGS 비교)

- **Dataset**: N=2,799 전체 코호트 NGS 데이터. Pre-T-DXd n=2,420; post-T-DXd n=379.
- **목적**: T-DXd 치료 이후 선택적 진화 압력으로 농축되는 somatic mutation 동정.
- **Baseline**: Post-T-DXd treated samples vs. unmatched T-DXd-naïve pre-treatment samples.
- **Metric**: Mutation prevalence, Chi-square p-value, BH-adjusted q-value.
- **주요 수치**:
  - *ESR1*: q<0.005 (가장 강한 신호 중 하나). Pre ~11%, Post ~21% (Fig. 5a **).
  - *ERBB2* (Her2/Neu): q<0.05. Pre ~5%, Post ~10% (Fig. 5a *).
  - *SMAD4*: q<0.0005 (가장 유의). Pre ~2%, Post ~5% (Fig. 5a ***).
  - *NFE2L2*: q<0.05. Gain-of-function mutations 농축 (Fig. 5b lollipop; N-terminal 영역 집중).
  - *KEAP1*: q=0.074 (FDR 역치 미달, 경향성). Loss-of-function mutations (Fig. 5c).
  - *TOP1*: q<0.05.
  - ABCC1 발현: Post-T-DXd 샘플에서 중앙값 27 TPM vs pre 22 TPM (p<0.001), T-DXd 치료가 ABCC1 발현을 선택적으로 증가시킬 가능성.
  - 전체 코호트에서 ERBB2 mutation의 78%가 kinase domain에 위치 (Supp. Fig. S8a 언급).
- **정성 결과**: NFE2L2 gain-of-function과 KEAP1 loss-of-function 동시 관찰 → ABCC1 상향 조절 경로. ESR1 mutation 농축은 호르몬 치료 노출 선택압으로도 해석 가능 (T-DXd 특이적인지 불확실).
- **논문 주장과의 연결**: T-DXd 치료가 (1) ERBB2 mutation(HER2 표적 손실) 및 (2) NFE2L2/KEAP1 pathway(ABCC1-mediated efflux 증가) 방향으로 선택압을 행사함.

검토필요: Unmatched comparison이므로 두 집단의 기저 mutation landscape 차이가 confound할 수 있음. ESR1 mutation 농축이 단순 치료 기간 누적 효과(내분비 치료 exposure)일 가능성을 배제하기 어려움 — 저자도 명시적 한계로 인정.

---

##### Dataset 4 — In Vitro Validation: T-DXd-Resistant Cell Lines

- **Dataset**: HCC1954(HER2+), HCC1954-TDXdR, SUM190(HER2+), SUM190-TDXdR.
- **목적**: ABCC1 억제(MK-571)가 T-DXd 내성 세포에서 감수성을 회복하는지 검증.
- **사용한 데이터 규모**: 4개 세포주, MK-571(20 μM 또는 30 μM) + T-DXd(133 nM) 병용, 10일 MTS assay.
- **Metric**: 세포 생존율(% of untreated control), IC50 (μM).
- **주요 수치**:
  - MK-571 IC50: HCC1954 31.7 μM / HCC1954-TDXdR 30.2 μM; SUM190 33.1 μM / SUM190-TDXdR 38.5 μM (Fig. 6a). Parent vs resistant 간 IC50 변화 미미.
  - Western blot: HCC1954-TDXdR에서 ABCC1 단백질 고발현 확인; SUM190-TDXdR에서는 parent와 유사 (Fig. 6b).
  - HCC1954-TDXdR: MK-571(20μM) + T-DXd(133nM) 병용이 T-DXd 단독 및 MK-571 단독 대비 세포 생존율 유의미하게 추가 감소 (p<0.0001, Fig. 6c 좌측).
  - SUM190-TDXdR: 병용 시 T-DXd 단독 대비 유의한 추가 감소(p<0.0001)이나 MK-571 단독과의 차이는 "ns" (Fig. 6c 우측).
- **정성 결과**: ABCC1 단백질이 실제 높은 HCC1954-TDXdR에서만 ABCC1 억제 효과 명확. SUM190-TDXdR에서는 ABCC1이 아닌 다른 내성 기전이 주도적일 수 있음.
- **논문 주장과의 연결**: In vitro 결과가 ABCC1-mediated efflux의 T-DXd 내성 기여를 지지하지만, 세포주마다 다른 반응은 내성 기전의 이질성을 시사.

---

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: HER2(ERBB2) 발현과 T-DXd 효능은 양의 관계; ABCC1 발현과 T-DXd 효능은 음의 관계. 두 인자는 독립적이며 조합 시 OS 차이가 최대 2.5배 이상.
- **가장 중요한 수치**: ABCC1 Q4 vs Q1: 14.2 vs 22.0개월 (p<0.0001). ERBB2 Q4 vs Q1: 24.9 vs 13.2개월 (p<0.0001). ABCC1 Q1-3/ERBB2 Q4 vs ABCC1 Q4/ERBB2 Q1-3: 27.9 vs 11.2개월.
- **baseline 대비 차이**: 단순 HER2 IHC 카테고리보다 ERBB2 RNA 발현 quartile이 더 세밀한 예후 층화 가능. ABCC1은 IHC로 측정되지 않는 추가적인 예측력 제공.
- **결과 해석 시 주의점**: (1) Unmatched comparison — confounding 가능성. (2) Real-world OS는 PFS·PD 기반 trial endpoint와 다름. (3) In vitro 결과는 HER2+ 세포주 2개에만 해당. (4) ESR1 mutation 농축은 T-DXd-specific이 아닐 가능성. (5) 대부분 저자가 Caris Life Sciences 직원 — 이해상충 명시.

---

## Figures

#### Figure 1

- **이 Figure가 필요한 이유**: T-DXd의 세포 내 처리 경로 전체와 논문의 연구 설계를 한눈에 보여주기 위함.
- **이 Figure가 뒷받침하는 주장**: T-DXd 내성이 단일 기전이 아닌 다중 경로(HER2 target level/mutation, ABCC1-mediated efflux, TOP1 mutation 등)에서 발생한다는 개념적 프레임.

##### 패널별 설명
- **상단 schematic**: T-DXd의 9단계 처리 경로 도식 — ① receptor binding, ② endocytosis, ③ intracellular trafficking, ④ lysosomal cleavage, ⑤ topoisomerase 억제, ⑥ drug efflux, ⑦ ADCC, ⑧ TIME(tumor immune microenvironment), ⑨ apoptosis. 각 단계의 X 표시는 내성 발생 가능 지점. 세포 내 NFE2L2–KEAP1–Promoter–ABCC1 전사 축이 drug efflux 단계와 연결됨을 도시.
- **하단 좌측**: Study design 요약. Pre-T-DXd samples: WTS로 전사체 분석(T-DXd-specific OS와 연관성 탐색). Pre/Post-T-DXd unmatched samples: NGS로 post-T-DXd mutation 탐색.
- **하단 우측**: Legend — mutations enriched with T-DXd(번개), toxic payload, HER2 receptor, efflux pump(ABCC1), effector cell, lysosome, T-DXd, T-DXd resistance(X).

##### 본문에서 강조한 비교
- 비교 대상: 전임상에서 제안된 전체 내성 경로 vs 이 연구에서 실증적으로 검증한 것.
- 관찰된 차이: 이 연구는 drug efflux(ABCC1), HER2 target level(ERBB2 expression/mutation), topoisomerase mutation(TOP1)에 실증 결과를 제공.
- 이 차이가 의미하는 것: 연구 설계가 전사체 + 돌연변이 데이터로 접근 가능한 경로로 범위를 좁혔음을 명시.

##### 해석 시 주의점
- 이 Figure는 mechanistic schematic이며 실험 데이터가 아님. 실제 검증은 Results 섹션에서.

---

#### Figure 2

- **이 Figure가 필요한 이유**: 96개 feature 중 T-DXd-specific OS와 유의미하게 연관된 유전자를 시각화하고, ABCC1·ERBB2 발현의 OS 예측력을 quartile KM 분석으로 보여주기 위함.
- **이 Figure가 뒷받침하는 주장**: ERBB2(유익)와 ABCC1(유해) 발현이 T-DXd 특이적 OS의 독립 예측인자라는 핵심 주장.

##### 패널별 설명
- **a**: Bubble chart (forest plot 형식). X축 = hazard ratio, bubble 크기 = $-\log_{10}$(FDR-adjusted p-value). 좌측(HR<1, protective): ERBB2가 가장 크고 유의. 우측(HR>1, harmful): ABCC1이 가장 크고 유의. FCGR3A, MKI67, ABCA6, RAB6A도 q<0.05이나 KM에서 quartile 간 유의미한 분리 없음.
- **b**: Kaplan-Meier, ABCC1 quartile. Q1(최저 발현)=22.0개월 (CI 17.9–27.3), Q2=17.7 (CI 15.5–19.8), Q3=16.3 (CI 14.7–18.2), Q4(최고 발현)=14.2개월 (CI 11.8–15.6). p<0.0001 (log-rank).
- **c**: Kaplan-Meier, ERBB2 quartile. Q4=24.9개월 (CI 22.9–32.3), Q3=16.5 (CI 15.0–17.8), Q2=13.7 (CI 12.2–16.6), Q1=13.2개월 (CI 11.2–14.3). p<0.0001.

##### 본문에서 강조한 비교
- ABCC1 Q1 vs Q4: 22.0 vs 14.2개월 (7.8개월 차이). ERBB2 Q4 vs Q1: 24.9 vs 13.2개월 (11.7개월 차이).
- 이 차이가 의미하는 것: 두 biomarker가 반대 방향으로 OS에 영향. Pharmacokinetics 관점에서 "세포 내 drug exposure = target-mediated uptake / efflux" 조합을 반영.

##### 해석 시 주의점
- KM Q2/Q3/Q4 간 차이는 Q1 대비 차이보다 상대적으로 작아, ABCC1 고발현 환자 선별은 top quartile(Q4) cutoff가 실용적. 75th percentile threshold가 Supp. Table S4에서 최적 유의성 확인.

---

#### Figure 3

- **이 Figure가 필요한 이유**: ERBB2와 ABCC1 발현이 HER2 IHC 카테고리와 어떤 관계인지 보여줌으로써, ABCC1이 기존 HER2 검사 체계와 독립적인 biomarker임을 시각화.
- **이 Figure가 뒷받침하는 주장**: ABCC1 발현은 HER2 IHC 상태와 무관해 ABCC1 측정에 별도 assay가 필요.

##### 패널별 설명
- **a**: 막대 그래프. ERBB2 발현 quartile별 HER2 IHC 카테고리 비율 분포. Q4에서 HER2-positive 비율 가장 높고(282/500여 개), Q1에서 HER2-null 비율 가장 높음(168명). 각 quartile 내 케이스 수 표기.
- **b 좌측**: Violin/jitter plot. HER2 IHC category vs ERBB2 TPM. HER2-positive에서 유의미하게 높음(***). 예상된 결과.
- **b 우측**: Violin/jitter plot. HER2 IHC category vs ABCC1 TPM. 모든 카테고리 간 차이 없음("ns"). ABCC1은 HER2 status와 독립적.

##### 본문에서 강조한 비교
- ERBB2 TPM은 HER2 IHC와 양의 상관(기대됨). ABCC1 TPM은 HER2 카테고리와 무관.
- 이 차이가 의미하는 것: ABCC1 측정이 HER2 IHC 결과에 의존하지 않음. ABCC1-high 환자는 모든 HER2 카테고리에 고루 분포.

##### 해석 시 주의점
- 각 IHC 그룹의 케이스 수 불균등(HER2-null vs HER2-positive 간 차이). HER2-ultra-low 그룹 통계 검정력이 상대적으로 낮을 수 있음.

---

#### Figure 4

- **이 Figure가 필요한 이유**: ABCC1과 ERBB2/HER2 status 조합이 단일 biomarker보다 더 세밀한 환자 층화를 가능하게 함을 보여주기 위함.
- **이 Figure가 뒷받침하는 주장**: 두 biomarker의 독립적·보완적 예측력 — T-DXd 치료 전 환자 선별 개선 가능성.

##### 패널별 설명
- **a**: ABCC1 Q4(high) vs Q1-3(low). Q1-3=17.8개월 vs Q4=14.2개월, p=0.0021.
- **b**: HER2 IHC status별 KM. HER2-positive 27.3개월 (CI 24.2–32.6), HER2-low 17.5개월 (CI 16.1–22.6), HER2-ultra-low 12.7개월 (CI 10.5–16.8), HER2-null 10.8개월 (CI 9.4–12.4), p<0.0001.
- **c**: ABCC1 × HER2 status 4-way 조합. 최고: ABCC1 Q1-3/HER2-low 19.3개월 (CI 16.8–19.4). 최저: ABCC1 Q4/HER2-null 8.0개월 (CI 6.8–10.8). p<0.0001.
- **d**: ABCC1 × ERBB2 quartile 4-way 조합. 최고: ABCC1 Q1-3/ERBB2 Q4 27.9개월 (CI 23.4–36.8). 최저: ABCC1 Q4/ERBB2 Q1-3 11.2개월 (CI 10.0–12.7). p<0.0001.

##### 본문에서 강조한 비교
- ABCC1 Q1-3/ERBB2 Q4 vs ABCC1 Q4/ERBB2 Q1-3: 27.9 vs 11.2개월 — 2.5배 이상 차이.
- 이 차이가 의미하는 것: 두 biomarker 조합이 T-DXd 치료 결과 예측 개선에 유용.

##### 해석 시 주의점
- Panel c에서 ABCC1 Q4/HER2-null 그룹(n=92)은 소규모로 CI 넓음. 조합 분석 그룹 중 일부의 신뢰구간이 중앙값 수치보다 실제 불확실성이 더 큼.

---

#### Figure 5

- **이 Figure가 필요한 이유**: T-DXd 치료 후 선택적으로 농축되는 somatic mutation을 시각화하고, 내성 기전 관련 NFE2L2/KEAP1 mutation 분포를 제시하기 위함.
- **이 Figure가 뒷받침하는 주장**: T-DXd 치료가 ERBB2, NFE2L2/KEAP1 등 내성 관련 mutation을 선택한다는 주장.

##### 패널별 설명
- **a**: 막대 그래프. X축 = 유전자, Y축 = mutation prevalence. 파란색=pre-T-DXd, 빨간색=post-T-DXd. SMAD4(***), ESR1(**), ERBB2(*), NFE2L2(*), TOP1(*)가 유의하게 농축. 모든 표시 mutation은 unadjusted p<0.05.
- **b**: NFE2L2 lollipop plot. Gain-of-function mutations(파란색), 1-605aa 단백질 도메인 위치. N-terminal 영역(100aa 이전)에 집중.
- **c**: KEAP1 lollipop plot. Loss-of-function mutations(빨간색: frameshift, truncating, missense). BTB, BACK, Kelch 도메인에 분산.

##### 본문에서 강조한 비교
- Pre vs post-T-DXd mutation prevalence 비교. SMAD4가 가장 강한 농축 신호(q<0.0005).
- 이 차이가 의미하는 것: T-DXd가 ERBB2 kinase domain mutation(HER2 표적 손실 → ADC 결합 감소)과 NFE2L2/KEAP1 axis(ABCC1 상향 조절 → drug efflux 증가)를 선택.

##### 해석 시 주의점
- Unmatched comparison. p값은 unadjusted (caption 명시). BH 보정 후 일부 gene의 유의성 역치 변동. 개별 환자 수준에서 causality 확립 불가.

---

#### Figure 6

- **이 Figure가 필요한 이유**: In vitro에서 ABCC1 억제제(MK-571)와 T-DXd 병용의 세포독성 상승 효과를 제시, mechanistic hypothesis를 실험적으로 지지.
- **이 Figure가 뒷받침하는 주장**: ABCC1-mediated efflux가 T-DXd 내성에 기여하며 ABCC1 억제가 감수성을 회복할 수 있다는 therapeutic hypothesis.

##### 패널별 설명
- **a**: IC50 표. 4개 세포주 MK-571 IC50 값. HCC1954 31.7→TDXdR 30.2 μM; SUM190 33.1→TDXdR 38.5 μM. Parent vs resistant 간 IC50 변화 작음.
- **b**: Western blot. ABCC1 단백질. HCC1954-TDXdR에서 명확한 band 증가. SUM190/SUM190-TDXdR는 비슷한 수준. β-actin loading control.
- **c**: 세포 생존율 막대 그래프 (4개 조건: vehicle/T-DXd 단독/MK-571 단독/병용). HCC1954-TDXdR(좌): 병용 시 각 단독 대비 유의미한 추가 감소(p<0.0001). SUM190-TDXdR(우): 병용 시 T-DXd 단독 대비 유의(p<0.0001)이나 MK-571 단독과의 차이 ns.

##### 본문에서 강조한 비교
- HCC1954-TDXdR(ABCC1 고발현) vs SUM190-TDXdR(ABCC1 유사 발현). ABCC1이 실제로 높은 세포주에서만 병용 상승 효과 명확.
- 이 차이가 의미하는 것: ABCC1 단백질 발현 수준이 MK-571 + T-DXd 병용 효과 예측에 중요한 변수.

##### 해석 시 주의점
- MK-571은 ABCC1 외 다른 ABC transporters도 억제하는 tool compound로 ABCC1-specificity 한계. 세포주 결과는 HER2+ 세포주에만 해당; HER2-low/null 상황 외삽 불가. 임상 개발 단계 화합물이 아님.

---

## Tables

#### Table 1 — Clinico-demographic characteristics of T-DXd-treated breast cancer cohort (N=2,799)

- **이 Table이 필요한 이유**: 코호트 구성 및 pre/post-T-DXd 샘플 간 기저 특성 분포의 투명성 제시.
- **이 Table이 뒷받침하는 주장**: 2,799명 코호트의 규모와 HER2 status 다양성을 보여줌으로써 real-world 대표성 주장.

#### 표 구조
- Row: 임상·인구학적 변수(Age, Sex, HER2 status, HR status, Specimen site, Test platform, Total N).
- Column: Pre-T-DXd / Post-T-DXd / Total.
- 셀 값: 중앙값 또는 N(%).

#### 핵심 수치
- 총 N=2,799. Pre-T-DXd n=2,420 (86.5%), Post-T-DXd n=379 (13.5%).
- HER2 status(Total): HER2-null 504(18%), HER2-ultra-low 448(16%), HER2-low 954(34.1%), HER2-positive 446(15.9%), Other/unknown 447(16%).
- Test platform: RNA(WTS) n=1,829 (65.3%), DNA(NGS) n=2,432 (86.9%).
- 중앙 연령 58세. 남성 30명(1.1%).
- Pre-T-DXd 중앙 조직-치료 간격: 15.5개월 (범위 0.1–192개월); Post-T-DXd 10.5개월 (0.1–44.5개월).
- 14%가 T-DXd 이전 TDM1 투여.

#### 본문에서 강조한 비교
- Pre vs Post-T-DXd 샘플 HER2 status 분포가 대체로 유사. 18% 환자에서 HER2-null 종양 — T-DXd의 off-label 또는 HER2 검사 이질성 반영 가능.
- Post-T-DXd 샘플에서 RNA WTS 비율 낮음(30% vs 71%) — 이는 병용 분석에서 고려 필요.

#### 해석 시 주의점
- 무작위 배정 아닌 observational cohort. "No matched samples were available" 저자 명시. Pre/post 비교에서 두 집단 간 치료 history 차이(ADC 이전 사용 비율 등)가 bias 원천.

---

## Supplementary Information

#### Supplementary Table S1 — HER2 categorization (IHC/CISH based)
- ASCO/CAP guideline 기반 HER2 IHC intensity + percentage + CISH result → HER2 category (HER2-positive, HER2-low, HER2-ultra-low, HER2-null) 매핑 표. 논문에서 사용된 HER2 분류 기준의 투명한 제시.

#### Supplementary Table S2 — 96 RNA signatures and genes (multivariate analysis)
- 11개 pathway별 96개 feature 전체 목록. TME(9 QuanTISeq signatures), ABC Transporter(32 genes including ABCC1, ABCA1~ABCG2 등), ADCC pathway(9 FCGRs + GZMB), Cytoskeleton organization(PAK4, CAV1, CAV2), Endocytosis, Intracellular trafficking(RAB5B, RAB6A, RAB6B), Lysosome pathway(22개 cathepsin 등), Prognostic Markers(ESR1, PGR, MKI67), Target Dimerization Partners(EGFR, NRG1, ERBB2~ERBB4), Topoisomerase(TOP1, TOP2A, TOP3B, TOP2B), Tubulin(TUBB, TUBB2A, TUBB3, TUBB4B, TUBB6).

#### Supplementary Table S3 — ABCC1 correlated genes Cox analysis
- ABCC1와 Spearman ρ>0.6인 ABCE1(ρ=0.601), ABCB7(ρ=0.615), ABCF2(ρ=0.639) 및 interaction term Cox analysis. ABCC1 단독이 -log10(p)=2.14로 가장 강한 신호. Interaction term 추가해도 ABCC1 독립성 유지.

#### Supplementary Table S4 — ABCC1 threshold optimization
- 5~95 percentile 단위 25가지 cutoff 테스트. 75th percentile이 최적: HR=0.7961, 95% CI [0.6883–0.9207], p=0.0021 (N High=457, N Low=1,372). 이 cutoff를 downstream 분석에 사용.

#### Supplementary Table S5 — Cohort stratified by ABCC1 quartiles
- ABCC1 Q1~Q4별 임상 특성. 대부분 변수 BH-adjusted p>0.1으로 균형. 예외: Brain/CNS specimen(p=0.025), Other Visceral Mets(p=0.025), ADC 이전 사용(ABCC1 Q4에서 34% vs Q1 16%, p=0.015) — ABCC1 고발현 환자가 이전 ADC 치료를 더 많이 받았을 가능성.

#### Supplementary Figures 요약
- **Fig. S1**: MKI67, FCGR3A, ABCA6, RAB6A KM curves. FCGR3A(p=0.94), ABCA6(p=0.25), RAB6A(p=0.10)는 유의하지 않음.
- **Fig. S2**: KI67 발현 — T-DXd 치료군(HR=1.29)과 비치료군(HR=1.32)에서 유사한 prognostic 효과 → T-DXd-specific이 아님.
- **Fig. S3~S10**: ABCC1-ERBB2 scatter 상관, TCGA 검증, ABCC1/ERBB2 combined subgroup KM, mutational landscape, ESR1 mutation 상세 분석, SUM190 trastuzumab 내성 확인, Western blot uncropped 등.

---

## 분석 자체에 대한 메모

1. **Paper-info.yaml title 불일치**: paper-info.yaml의 title("ADC treatment monitoring via CTCs: TROP2/HER2 expression at progression")이 실제 논문 제목("Mechanisms of resistance to trastuzumab deruxtecan in breast cancer elucidated by multi-omic molecular profiling")과 다름. Key finding도 다른 논문(TROP2/CTC)을 참조하고 있음. Yaml 갱신이 필요하며, 실제 논문은 TROP2나 CTC를 사용하지 않음. topic도 `ctc-adc-liquid-biopsy`가 아닌 `adc-resistance` 또는 `surfaceome-adc-target`이 더 적합할 수 있음.

2. **ABCC1 RNA-protein correlation**: Supplementary Fig. S3a-c에서 ABCC1 RNA와 단백질 발현의 상관이 moderate(r=0.4) 수준으로 언급됨. RNA 기반 biomarker로서의 noise를 반영 — 임상 적용 시 RNA IHC assay 개발 필요성이 있음.

3. **MK-571 임상 translational gap**: MK-571은 in vitro tool compound로 임상 개발 단계 화합물이 아님. ABCC1-selective clinical inhibitor가 없으므로 이 논문의 therapeutic hypothesis를 임상으로 translate하기 위해서는 새 화합물 개발 또는 다른 ABCC1 억제 전략이 필요.

4. **SMAD4 mutation 농축**: 이 논문에서 가장 강한 post-T-DXd mutation 농축 신호이나(q<0.0005), Discussion에서 SMAD4에 대한 설명이 없음. SMAD4는 TGF-β pathway의 tumor suppressor로, T-DXd 내성에서의 역할 해석이 필요.
