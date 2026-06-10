# bardia-2021-ascent-tnbc_core.md

## Executive Summary

- **무엇**: 재발·불응성 전이성 삼중음성유방암(mTNBC)에서 TROP2 타깃 ADC인 sacituzumab govitecan(SG)이 의사 선택 단일제 화학요법(TPC) 대비 PFS와 OS를 통계적으로 유의하게 연장한다는 것을 확인한 pivotal Phase 3 무작위 대조 시험 (ASCENT).
- **모델 / 방법**: 전향적 1:1 무작위 배정 공개라벨 Phase 3 RCT. Primary endpoint = 뇌전이 없는 환자에서 독립적 중앙 판정(BICR)에 의한 PFS. Kaplan-Meier + stratified log-rank + stratified Cox proportional-hazards 모델. 계층 인자: 이전 화학요법 수(2–3 vs. >3), 지역(북미 vs. 유럽), 기저 뇌전이 유무.
- **핵심 결과**:
  - ① 뇌전이 없는 환자 (n=468, primary population) — PFS 5.6 mo (SG) vs. 1.7 mo (TPC), HR 0.41 (95% CI 0.32–0.52), P<0.001
  - ② OS 12.1 mo vs. 6.7 mo, HR 0.48 (95% CI 0.38–0.59), P<0.001
  - ③ 객관적 반응률(ORR) 35% vs. 5% (Table 2)
  - ④ 전체 무작위 집단(n=529, 뇌전이 포함) — PFS 4.8 mo vs. 1.7 mo, HR 0.43, P<0.001
  - ⑤ 모든 사전 지정 하위군에서 SG 이익 방향 일관 (Figure 2)
- **우리 적용**: ADC 타깃으로서 TROP2의 임상 검증 근거. SEV_BRCA 또는 NCCHE_Gastric 파이프라인의 TROP2 ADC 비교 기준선(regulatory-precedent + BD-pitch-reference)으로 직접 활용.
- **심층**: 한계·재현 ROI는 `bardia-2021-ascent-tnbc_lens-academic.md` / `bardia-2021-ascent-tnbc_lens-industry.md` / `bardia-2021-ascent-tnbc_methodology-brief.md` 참고.

---

## Identity

- **Title**: Sacituzumab Govitecan in Metastatic Triple-Negative Breast Cancer
- **Authors**: A. Bardia, S.A. Hurvitz, S.M. Tolaney, D. Loirat, K. Punie, M. Oliveira, A. Brufsky, S.D. Sardesai, K. Kalinsky, A.B. Zelnak, R. Weaver, T. Traina, F. Dalenc, P. Aftimos, F. Lynce, S. Diab, J. Cortés, V. Diéras, C. Ferrario, P. Schmid, L.A. Carey, L. Gianni, M.J. Piccart, S. Loibl, D.M. Goldenberg, Q. Hong, M.S. Olivo, L.M. Itri, H.S. Rugo (ASCENT Clinical Trial Investigators)
- **Year**: 2021
- **Venue**: New England Journal of Medicine 384:1529–1541
- **DOI**: 10.1056/NEJMoa2028485
- **Citation key**: bardia2021ascent
- **ClinicalTrials.gov**: NCT02574455; EudraCT 2017-003019-21
- **Funding**: Immunomedics (subsidiary of Gilead Sciences)

---

## Background

### 배경 스토리

#### 배경 스토리

- **문제의 출발점**: mTNBC(전이성 삼중음성유방암)는 ER, PR, HER2 발현이 모두 결여되어 있어 표적 치료가 없다. 1차 치료 이후 standard-of-care는 단일제 화학요법(eribulin, vinorelbine, capecitabine, gemcitabine)이었으나, 이들의 반응률은 낮고 중앙 PFS는 수개월에 그쳤다.
- **선행 접근 A (단일제 화학요법)**: eribulin 등 여러 단일 cytotoxic agent가 2선 이후 표준 치료로 사용되었다. EMBRACE 연구와 Study 301 pooled analysis(n=428)에서 중앙 PFS 2.8개월, OS 12.9개월(eribulin); 별도 화학요법 arms에서 중앙 PFS 2.6개월, OS 8.2개월 수준이었다.
- **A의 한계**: 객관적 반응률이 낮고(~5% in this trial's TPC arm) 내성이 빠르게 발생한다. 전이 단계에서는 탈진 종양 세포의 가소성으로 인해 새로운 치료 전략이 필요하다.
- **선행 접근 B (면역항암제)**: PD-1/PD-L1 억제제(pembrolizumab 등)가 TNBC에서 임상 활성을 보였지만, KEYNOTE-119는 비표적 선택 집단에서 단일제 pembrolizumab이 화학요법보다 우월하지 않음을 보였다.
- **B의 한계**: PD-L1 발현 선택 없이는 이익이 제한적이고, 이미 면역항암제 노출된 환자에서 재투여 이익 불명확.
- **이 논문으로 이어지는 gap**: TROP2는 >90% 유방암에서 고발현되는 세포막 당단백질로, 이를 타깃으로 하는 ADC라면 화학요법의 낮은 반응률과 면역요법의 선택 한계를 동시에 극복할 수 있다는 가설. Phase 1–2 basket trial IMMU-132-01(n=108 TNBC 코호트)에서 ORR 33%, 중앙 PFS 5.5개월, OS 13.0개월로 accelerated FDA approval 근거를 제공했고, 확증적 Phase 3 시험이 필요했다.

#### 기본 개념

- **TROP2 (Trophoblast cell-surface antigen 2)**: 세포막 관통 칼슘 신호 transducer. 유방암을 포함한 다수 상피성 종양에서 >90% 발현. 정상 조직 대비 종양 과발현으로 ADC 타깃 적합.
- **Sacituzumab govitecan (SG, Trodelvy)**: 항-TROP2 IgG1 kappa 항체 + hydrolyzable linker + SN-38(이리노테칸의 활성 대사체, topoisomerase I inhibitor). Free SN-38은 세포막 투과성이 있어 항체가 내재화되기 전에도 인접 종양세포에 bystander effect 발휘.
- **UGT1A1 다형성**: UGT1A1*6/*28 동형 접합체는 SN-38 glucuronidation 감소 → 혈액독성 위험 증가. 이들 polymorphism 보유자에게는 SG 용량 주의 필요.
- **BICR (Blinded Independent Central Review)**: 영상 평가를 연구자와 독립적으로 맹검 판독. Primary endpoint 신뢰도 확보 수단.
- **ADC 작용 기전**: 항체가 종양 세포 표면 TROP2에 결합 → 항체-약물 복합체 내재화 → 리소솜 내 linker 가수분해 → SN-38 방출 → topoisomerase I 억제 → DNA 손상 → 세포 사멸. 유리 SN-38의 bystander killing 효과도 기여.

#### 이 논문의 필요성

- **핵심 이유**: FDA accelerated approval(2020년 4월)은 Phase 1–2 데이터에 근거했고, 확증적 Phase 3 시험 결과 제출 조건부였다.
- **기존 방법으로 부족했던 지점**: 단일제 화학요법 TPC 대비 PFS/OS 우월성을 충분히 통계적으로 검증하지 못한 상태에서 정규 허가 불가.
- **이 논문이 해결하려는 방향**: 1:1 무작위 대조 Phase 3 설계로 PFS(BICR), OS, ORR에서 우월성을 통계적으로 검증하고 full FDA approval로 전환 근거 마련.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 재발·불응성 mTNBC 환자에서 SG (10 mg/kg IV, days 1 & 8, 21일 주기)가 TPC 단일제 화학요법 대비 PFS를 연장하는지 Phase 3 수준에서 검증.
- **입력**: 무작위 배정된 mTNBC 환자 (≥2회 이전 전신 항암화학요법, 이전 taxane 필수 포함), 기저선 영상.
- **출력**: Primary — 뇌전이 없는 환자에서 BICR PFS. Secondary — OS, investigator-assessed PFS, ORR, response duration, safety.
- **추정 대상**: Kaplan-Meier median PFS/OS, hazard ratio (stratified Cox), ORR (stratified Cochran-Mantel-Haenszel).
- **중요한 hidden assumption**: 기저 뇌전이 환자의 예후적 confounding 효과를 제거하기 위해 primary population을 "뇌전이 없는 환자"로 사전 지정. 뇌전이 포함 full population은 secondary.

### 확률 / 통계학적 구조

- **Model family**: 생존 분석 — Kaplan-Meier 추정 + stratified log-rank test(주 비교) + stratified Cox proportional-hazards(HR 추정). 반응률 비교는 Cochran-Mantel-Haenszel.
- **Likelihood / objective**: 층화(stratified) log-rank test로 type I error 통제. 계층 인자: 이전 화학요법 수(2–3 vs. >3), 지역(북미 vs. 유럽), 뇌전이 유무(yes/no).
- **Prior / regularization**: 사전 power 계산 — HR 0.667 가정, 315 events 기준, 95% power at two-sided α = 0.05. 예상 중앙 PFS: SG 4.5개월 vs. TPC 3개월.
- **Latent variable / hidden state**: 해당 없음 (classical frequentist RCT).
- **Inference / optimization**: 계층 stratified분석으로 randomization 계층과 일관된 효과 추정. 다중성(hierarchical gatekeeping): PFS → OS 순서로 type I error 통제.
- **Noise, sparsity, uncertainty 처리**: 95% CI는 Brookmeyer-Crowley method (log-log transformation). CI는 multiple testing 보정 없이 제시 — 본문에서 명시적으로 "cannot be used to infer treatment effects"라고 경고.

### 핵심 method insight

- **기존 방법의 한계**: Phase 1–2 단일군 trial은 대조군이 없어 TPC 대비 이익 크기를 정확히 추정할 수 없고 FDA full approval 요건 미달.
- **이 논문의 바꾼 가정**: 뇌전이 환자를 primary population에서 사전 배제 — 뇌전이는 독립적 예후 인자로 confounding 효과가 크기 때문.
- **새로 추가한 변수 또는 구조**: BICR(맹검 독립 중앙 판정)을 PFS primary endpoint로 지정 → investigator bias 제거. Hierarchical testing으로 OS 검증.
- **이 변화가 중요한 이유**: Regulatory grade evidence로 FDA full approval 전환 가능; BICR 기반 PFS가 regulatory endpoint로 수용됨.

### 이전 방법과의 차이

- **Baseline (역할로서 이전 시험)**: IMMU-132-01 Phase 1–2 단일군 (n=108 TNBC); KEYNOTE-119 (pembrolizumab vs. 화학요법).
- **공통점**: 동일 환자군(≥2회 이전 치료, taxane 포함), 동일 SG 용량·스케줄.
- **차이점**: Phase 3 무작위 대조군 도입; 계층 stratified분석; BICR primary endpoint; hierarchical OS testing.
- **차이가 크게 나타나는 조건**: 이전 치료 수 >3인 heavily pretreated 군에서도 SG 이익 유지(PFS 5.6 vs. 2.5개월, HR 0.48).

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: mTNBC 환자 88개 기관, 7개국, n=529 (뇌전이 없는 primary population n=468).
- **Metric**: PFS (BICR), OS, ORR.
- **개선된 결과**: PFS HR 0.41(P<0.001), OS HR 0.48(P<0.001), ORR 35% vs. 5%.
- **Ablation 근거**: 사전 지정 하위군 분석(Figure 2) — 65세 이상, 간전이, 이전 PD-1/PD-L1 사용자, 진단 당시 TNBC 아닌 환자 등 모든 subgroup에서 HR < 1.
- **정성적 효과**: 시험은 compelling efficacy evidence로 2020년 3월 Data Safety Monitoring Committee가 조기 중단 권고.

### Method 관점의 한계

- **약한 assumption**: TPC가 physician's choice 4종 중에서 연구자 판단으로 사전 지정되므로 이질적 대조군. 개별 약제 간 비교 불가(underpowered).
- **구현 또는 학습상의 부담**: UGT1A1 다형성 사전 검사 없이 진행 — 독성 위험 환자 사전 선별 없음.
- **일반화가 불확실한 조건**: TROP2 발현 수준별 층화 없음 — "TROP2 낮은 발현" 환자에서의 이익 불확실. 뇌전이 환자 서브그룹은 별도 보고 예정이었으나 본 논문에는 미포함.

---

## Results

### Dataset별 결과

#### Dataset 1 — Primary Population: 뇌전이 없는 mTNBC (n=468)

- **Dataset**: 전 세계 88개 기관, 7개국 (북미 + 유럽), 2017년 11월~2019년 9월 등록. 뇌전이 없는 환자 n=468 (SG n=235, TPC n=233).
- **목적**: Primary efficacy endpoint 검증 — BICR PFS.
- **사용한 데이터 규모**: SG n=235 (이중 233명 여성, 2명 남성), TPC n=233 (233명 전원 여성). 중앙 연령 54세(SG), 53세(TPC). 이전 항암 요법 중앙 3회(1–16). Taxane 100%, anthracycline 82%, carboplatin 66%, PD-1/PD-L1 inhibitor 27~29%.
- **Baseline / 비교 대상**: TPC 구성 — eribulin 54%, vinorelbine 20%, capecitabine 13%, gemcitabine 12%.
- **Metric / 평가 기준**: PFS (BICR, RECIST v1.1), OS, ORR, response duration.
- **주요 수치**:
  - PFS: SG 5.6개월(95% CI 4.3–6.3) vs. TPC 1.7개월(95% CI 1.5–2.6), HR 0.41(95% CI 0.32–0.52), P<0.001 (Table 2, Figure 1A)
  - OS: SG 12.1개월(95% CI 10.7–14.0) vs. TPC 6.7개월(95% CI 5.8–7.7), HR 0.48(95% CI 0.38–0.59), P<0.001 (Table 2, Figure 1B)
  - ORR: SG 35%(82/235) vs. TPC 5%(11/233) (Table 2, Figure 1C)
  - Clinical benefit: SG 45%(105/235) vs. TPC 9%(20/233)
  - 반응 지속 중앙값: SG 6.3개월(95% CI 5.5–9.0) vs. TPC 3.6개월(95% CI 2.8–NE), HR 0.39(95% CI 0.14–1.07) (Figure S6)
  - 첫 반응까지 시간(중앙): 1.5개월(SG) vs. 1.5개월(TPC)
- **정성 결과**: 2020년 3월 data cutoff 시 중앙 추적 17.7개월(range 5.8–28.1). SG arm에서 15/235(6%)가 계속 치료 중, TPC arm에서 0/233이 계속 치료.
- **논문 주장과의 연결**: primary endpoint HR 0.41 달성으로 pre-specified efficacy threshold 충족 → FDA full approval 근거.

#### Dataset 2 — Full Population (뇌전이 포함, n=529)

- **Dataset**: 전체 무작위 배정 집단 (SG n=267, TPC n=262). 뇌전이 기저선 n=61.
- **목적**: 뇌전이 포함 전체 집단에서 효과 일관성 확인 (secondary endpoint).
- **사용한 데이터 규모**: SG n=267, TPC n=262.
- **주요 수치**:
  - PFS: SG 4.8개월(95% CI 4.1–5.8) vs. TPC 1.7개월(95% CI 1.5–2.5), HR 0.43(95% CI 0.35–0.54), P<0.001 (Figure 1D)
  - OS: SG 11.8개월(95% CI 10.5–13.8) vs. TPC 6.9개월(95% CI 5.9–7.7), HR 0.51(95% CI 0.41–0.62) (Figure S7)
  - ORR: SG 31%(83/267) vs. TPC 4%(11/262)
- **논문 주장과의 연결**: primary population과 full population 간 결과 방향 및 크기 일관 → 뇌전이 환자 포함 시에도 이익 유지.

#### Dataset 3 — 안전성 집단 (Safety Population, n=482)

- **Dataset**: SG n=258, TPC n=224 (최소 1회 투여 환자).
- **목적**: 독성 프로파일 비교.
- **주요 수치 (Table 3)**:
  - Any grade adverse event: SG 98% vs. TPC 86%
  - Grade 3 이상: SG 45% vs. TPC 32%
  - Grade 4 이상: SG 19% vs. TPC 15%
  - Neutropenia (any grade): SG 63% vs. TPC 43%; Grade 3: 34% vs. 20%; Grade 4: 17% vs. 13%
  - Diarrhea (any grade): SG 59% vs. TPC 12%; Grade 3: 10% vs. <1%
  - Nausea (any grade): SG 57% vs. TPC 26%
  - Alopecia: SG 46% vs. TPC 16%
  - Febrile neutropenia: SG 6% vs. TPC 2%
  - Grade 3 leukopenia: SG 9% vs. TPC 4%
  - Grade 3 anemia: SG 8% vs. TPC 5%
  - Serious treatment-related adverse events: SG 15%(39명) vs. TPC 8%(19명)
  - 독성으로 인한 치료 중단: SG 5%(12명) vs. TPC 5%(12명) — 발생률 유사
  - 독성으로 인한 사망: SG 3명(respiratory failure 2, postobstructive pneumonia 1 — 모두 치료 비관련 판정) vs. TPC 3명(neutropenic sepsis 1 — 치료 관련 판정)
  - Interstitial lung disease: SG 0건(Grade 1/2), Grade 3 pneumonitis 1건(reversible)
  - 말초신경병증 Grade >2: SG 0건 vs. TPC 3건
- **Dose intensity**: SG 중앙 상대 용량 강도 99.7%; 중앙 투여 기간 4.4개월(최대 22.9개월). G-CSF support: SG 49% vs. TPC 23%.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 모든 사전 지정 하위군(나이, 인종, 이전 치료 수, 지역, PD-1/PD-L1 사용 여부, 간전이, 진단 당시 TNBC 여부)에서 HR < 1 일관 (Figure 2).
- **가장 중요한 수치**: PFS HR 0.41, OS HR 0.48 (뇌전이 없는 primary population, 둘 다 P<0.001).
- **baseline 대비 차이**: ORR 35% vs. 5% — 7배 차이. 과거 Phase 2 IMMU-132-01 TNBC 코호트(ORR 33%)와 일관.
- **결과 해석 시 주의점**: TPC 반응률 5%는 본 시험 설계(chemotherapy-exhausted population)를 반영. Cross-trial comparison 시 population이 다름에 주의(Discussion에서도 언급). 95% CI는 multiple testing 보정 없이 제시되어 single endpoint inference 불가.

---

## Figures

#### Figure 1 (본문 p.1536)

- **이 Figure가 필요한 이유**: primary/secondary efficacy endpoints를 시각적으로 증명하고, 종양 크기 변화(waterfall plot)로 반응 깊이를 직관적으로 보여주기 위함.
- **이 Figure가 뒷받침하는 주장**: SG가 TPC 대비 PFS, OS 모두 유의하게 연장하고 ORR에서 압도적 차이를 보인다.

##### 패널별 설명

- **A (PFS, 뇌전이 없는 환자)**: Kaplan-Meier 생존곡선. SG(n=235) vs. TPC(n=233). 중앙 PFS 5.6 vs. 1.7개월, HR 0.41. 초기 1–3개월 구간에서 두 군 사이 곡선이 급격히 분리.
- **B (OS, 뇌전이 없는 환자)**: SG 중앙 OS 12.1 vs. TPC 6.7개월, HR 0.48. 두 배 가까운 생존 연장.
- **C (Waterfall plot, 뇌전이 없는 환자 중 평가 가능)**: SG n=212, TPC n=160. SG arm에서 다수 환자가 종양 크기 감소(음의 bar), TPC arm은 대부분 증가 또는 변화 미미.
- **D (PFS, 전체 무작위 집단)**: SG n=267 vs. TPC n=262. 중앙 PFS 4.8 vs. 1.7개월, HR 0.43. A와 유사한 분리 패턴, primary population보다 중앙값 약간 낮음.

##### 본문에서 강조한 비교

- 비교 대상: SG vs. TPC.
- 관찰된 차이: Panel A에서 3개월 시점 PFS rate SG ~50% vs. TPC ~10% 수준 (정확한 수치 본문 미제공, Kaplan-Meier curve 시각 추정).
- 이 차이가 의미하는 것: 기존 화학요법의 빠른 progression과 달리 SG는 유의한 비율의 환자에서 6개월 이상 지속 반응 달성.

##### 해석 시 주의점

- Crossover 없음. TPC에서 SG로의 crossover가 없었으므로 OS 효과는 contamination 없이 해석 가능.
- 97%의 patients received treatment as assigned; 3% had no drug given.

#### Figure 2 (본문 p.1537)

- **이 Figure가 필요한 이유**: 다양한 임상 하위군에서 SG 이익의 일관성을 보여 편향 없는 효과임을 주장하기 위함.
- **이 Figure가 뒷받침하는 주장**: SG의 PFS 이익은 나이·인종·이전 치료 수·지역·PD-1/PD-L1 이전 사용·간전이·진단 당시 TNBC 여부에 관계없이 일관됨.

##### 패널별 설명

- Forest plot. 행: subgroup; 열: SG vs. TPC 중앙 PFS, HR(95% CI). 모든 행에서 HR < 1 (Sacituzumab govitecan better 방향).
- 주목할 HR: ≥65세 HR 0.22(95% CI 0.12–0.40, n=90); 간전이 있는 군 HR 0.48(0.34–0.67); 이전 PD-1/PD-L1 사용자 HR 0.37(0.24–0.57).

##### 본문에서 강조한 비교

- ≥65세 서브그룹에서 SG PFS 7.1개월 vs. TPC 2.4개월로 더 큰 절대 이익.
- 이전 PD-L1 사용 여부와 무관하게 SG 이익 유지 — 면역항암제 내성 환자에서도 효과.

##### 해석 시 주의점

- Subgroup 분석은 exploratory. 개별 CI가 넓고 multiple testing 보정 없음. 특히 Asian subgroup(n=18)의 HR 0.40(0.08–2.08)은 CI가 매우 넓어 해석 불가.

---

## Tables

### Table 1 — 기저선 특성 및 이전 치료 (본문 p.1534)

- **이 Table이 필요한 이유**: 무작위 배정이 양 군 간 baseline을 균형 있게 분배했음을 보여주어 교란 편향 없음을 입증.
- **이 Table이 뒷받침하는 주장**: 두 군의 인구통계·병기·이전 치료 특성이 유사하므로 결과 차이가 치료 배정에서 비롯됨.

#### 표 구조

- Row: 특성 항목 (성별, 나이, 인종, ECOG, BRCA 상태, TNBC 진단 여부, 전이 기간, 종양 위치, 이전 치료 수, 이전 약제 등)
- Column: SG (N=235) vs. TPC (N=233)
- 셀 값: n(%) 또는 중앙값(범위)

#### 핵심 수치

- ECOG PS 0: SG 46%, TPC 42%; PS 1: SG 54%, TPC 58% — 균형
- Germline BRCA 양성: SG 7%, TPC 8% — 균형
- 진단 당시 TNBC 아닌 비율: SG 30%, TPC 33% — 약 1/3이 재발 시 TNBC로 전환된 경우
- 이전 항암 요법 중앙 3회(1–16): 양 군 동일
- 간전이: SG 42%, TPC 43%
- 폐전이: SG 46%, TPC 42%
- Taxane 100%, anthracycline ~82%, carboplatin ~66%: 양 군 유사
- 이전 PARP inhibitor: SG 7%, TPC 8%

#### 본문에서 강조한 비교

- 30%의 환자가 진단 당시 TNBC가 아니었음 — 전이 재발 시 phenotypic conversion. 이는 TNBC 정의의 heterogeneity를 시사하며, 재발 생검의 중요성을 강조.
- 이전 PD-1/PD-L1 사용: SG 29%, TPC 26% — immunotherapy-experienced population이 상당수 포함.

#### 해석 시 주의점

- UGT1A1 genotype이 Table에 없음 — 독성 리스크 사전 층화 없음.
- 뇌전이 환자(n=61)는 이 Table에서 제외됨 (뇌전이 없는 468명 기준).

### Table 2 — 치료 효과 요약 (BICR, 본문 p.1535)

- **이 Table이 필요한 이유**: primary/secondary endpoint 모든 수치를 한 표에서 비교 제공. Regulatory submission의 핵심 reference table.
- **이 Table이 뒷받침하는 주장**: SG가 TPC 대비 PFS, OS, ORR 모두에서 우월함.

#### 표 구조

- Row: PFS, HR, OS, HR, ORR, clinical benefit, stable disease, progressive disease 등
- Column: 뇌전이 없는 집단 (SG N=235 / TPC N=233) 및 Full population (SG N=267 / TPC N=262)
- 셀 값: 중앙값(95% CI), n(%)

#### 핵심 수치

- PFS (no brain mets): SG 5.6(4.3–6.3) vs. TPC 1.7(1.5–2.6), HR 0.41(0.32–0.52), P<0.001
- OS (no brain mets): SG 12.1(10.7–14.0) vs. TPC 6.7(5.8–7.7), HR 0.48(0.38–0.59), P<0.001
- ORR (no brain mets): SG 35% vs. TPC 5%
  - Complete response: SG 4%, TPC 1%
  - Partial response: SG 31%, TPC 4%
- Clinical benefit (CR+PR+SD≥6mo): SG 45% vs. TPC 9%
- Progressive disease: SG 23% vs. TPC 38%
- Stable disease ≥6mo: SG 10% vs. TPC 4%
- Response duration (중앙): SG 6.3(5.5–9.0) vs. TPC 3.6(2.8–NE), HR 0.39(0.14–1.07)

#### 본문에서 강조한 비교

- ORR 35% vs. 5% — 절대 차이 30%p. 기존 화학요법 단독 효과 대비 압도적.
- Full population에서 ORR SG 31% vs. TPC 4%로 primary population과 일관.

#### 해석 시 주의점

- Response duration의 HR 95% CI(0.14–1.07)는 1을 포함하며 TPC arm 반응자 수 자체가 매우 적어(n=11) 해석 불확실.

### Table 3 — 안전성 (본문 p.1538)

- **이 Table이 필요한 이유**: 독성 프로파일을 체계적으로 비교하여 허용 가능성(tolerability) 입증.
- **이 Table이 뒷받침하는 주장**: 골수억제(neutropenia)와 설사가 SG에서 더 많지만 치료 중단률은 양 군 유사, 심각한 ILD 거의 없음.

해석 시 주의점: G-CSF support가 SG arm 49% vs. TPC 23%로 차이 — 이 보조 치료 없이는 SG arm의 neutropenia가 더 심각할 수 있다는 점을 고려해야 함.

---

## Supplementary Information

- **Figure S1**: ASCENT 연구 설계 모식도 — 1:1 무작위, 층화 인자 3개, SG 10 mg/kg IV d1&8/21d cycle vs. TPC 4종 선택.
- **Figure S2**: CONSORT diagram — 529명 등록, SG 267명, TPC 262명 배정. TPC arm 32명이 무약물 투여(26명 no trial drug, 6명 withdrew consent) — 이들은 safety 분석 제외, efficacy 분석 포함.
- **Figure S3**: 연구자 평가 PFS (investigator-assessed) — BICR PFS와 일관(SG 5.5개월 vs. TPC 1.7개월, HR 0.35).
- **Figure S4**: OS subgroup 분석 forest plot — PFS subgroup 결과와 방향 일관.
- **Figure S5**: ORR subgroup 분석 forest plot.
- **Figure S6**: 반응 지속 기간 — SG에서 더 긴 반응 지속성.
- **Figure S7**: Full population OS.
- **Figure S8**: SG 용량 조정 알고리즘 (neutropenia/non-neutropenic toxicity용).
- **Table S1**: 모든 grade의 treatment-emergent adverse events (≥10% 발생 또는 worst grade ≥3이 ≥5%) — 본문 Table 3보다 광범위 항목.
- **Supplementary Methods**: 세부 환자 선택 기준, 용량 조정 가이드라인, premedication 규정, UGT1A1 주의사항, 각 TPC agent별 dose modification 기준 상세 기술.
- **Grade 3 Pneumonitis 케이스 기술**: SG arm 1건, 고위험 comorbidity 환자에서 발생, 7주 후 sequelae 없이 회복.
- **Deaths narrative**: SG arm 3건 (모두 치료 비관련 판정), TPC arm 3건(eribulin-related neutropenic sepsis 1건 포함 — 치료 관련).

---

## 분석 자체에 대한 메모

- TROP2 발현 수준 데이터가 본 논문에 없다. 고발현(>90%) 근거는 선행 문헌 인용이며, ASCENT는 TROP2 발현 여부를 entry 기준이나 층화 인자로 사용하지 않았다. 후속 biomarker 분석 필요.
- TPC가 4개 약제 혼합이어서 개별 약제 대비 SG 이익 크기가 불명확하다. Eribulin 대비 효과가 가장 중요할 수 있으나 subgroup 분석이 없다.
- 약 30%의 환자가 진단 당시 TNBC가 아니었다는 점은 tumor heterogeneity를 시사하며, 이들 환자에서 TROP2 발현 수준이 de novo TNBC와 다를 수 있다.
- OS 분석 시 post-progression 치료 데이터가 없어 OS 차이가 순수히 SG 효과인지 이후 치료 이력에도 영향을 받는지 해석 불가.
