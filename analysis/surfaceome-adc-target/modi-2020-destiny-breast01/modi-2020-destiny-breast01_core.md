# modi-2020-destiny-breast01_core.md

## Executive Summary

- **무엇**: T-DM1(trastuzumab emtansine) 이후 치료 옵션이 사실상 없었던 heavily pre-treated HER2+ 전이성 유방암 환자에서, 차세대 ADC인 trastuzumab deruxtecan (T-DXd, DS-8201)의 단독 요법 효능·안전성을 확인한 Phase 2 등록 임상 (DESTINY-Breast01).
- **모델 / 방법**: 2파트 오픈 라벨 단일군 Phase 2 다기관 연구. Part 1에서 권장 용량 결정 (5.4 mg/kg vs. 6.4 mg/kg PK/exposure-response 분석), Part 2에서 5.4 mg/kg 고정 용량의 efficacy·safety 평가. Primary endpoint: 독립 중앙 검토(ICR) 기반 ORR.
- **핵심 결과**:
  - ① 전체 코호트 (n=184, ITT) — ORR 60.9% (95% CI 53.4–68.0), median DOR 14.8개월, median PFS 16.4개월
  - ② T-DM1 진행 후 코호트 (n=180) — ORR 61.1% (95% CI 53.6–68.3), T-DM1 대비 효능 유지 확인
  - ③ 뇌전이 아집단 (n=24) — median PFS 18.1개월 (95% CI 6.7–18.1)
  - ④ 안전성 — grade ≥3 AE 57.1%; ILD 13.6% (grade 5: 2.2%), 핵심 독성 신호
- **우리 적용**: HER2 표면 발현 기반 ADC 타겟 검증의 regulatory-precedent + BD-opportunity 레퍼런스. SEV_BRCA, NCCHE_Gastric HER2 양성 환자군 적용 근거 제공.
- **심층**: 학술적 한계(단일군·단기 추적)는 `modi-2020-destiny-breast01_lens-academic.md` / 산업·규제 시사는 `modi-2020-destiny-breast01_lens-industry.md` / 재현·적용 체크는 `modi-2020-destiny-breast01_methodology-brief.md` 참고.

---

## Identity

- **Title**: Trastuzumab Deruxtecan in Previously Treated HER2-Positive Breast Cancer
- **Authors**: Modi S, Saura C, Yamashita T, Park YH, Kim S-B, Tamura K, Andre F, Iwata H, Ito Y, Tsurutani J, Sohn J, Denduluri N, Perrin C, Aogi K, Tokunaga E, Im S-A, Lee KS, Hurvitz SA, Cortes J, Lee C, Chen S, Zhang L, Shahidi J, Yver A, Krop I — 교신저자: Modi S (MSK), Krop I (DFCI)
- **Year**: 2020 (online December 11, 2019)
- **Venue**: New England Journal of Medicine, 382:610-621
- **DOI**: 10.1056/NEJMoa1914510
- **Citation key**: `@modi2020destinybreast01`
- **Funding**: Daiichi Sankyo, AstraZeneca (공동 sponsor)
- **Trial ID**: DESTINY-Breast01 (ClinicalTrials.gov — NCT03248492 해당 trial)

---

## Background

### 배경 스토리

#### 배경 스토리

- **문제의 출발점**: HER2 양성(overexpression 또는 amplification) 전이성 유방암은 전체 전이성 유방암의 약 15–20%를 차지한다 (본문 §Introduction). 1차 표준치료인 trastuzumab + pertuzumab + taxane 조합(CLEOPATRA trial)은 median PFS 18.7개월, median OS 56.5개월을 달성했으나, 이후 진행하면 선택지가 빠르게 좁아진다.

- **선행 접근 A — T-DM1 (trastuzumab emtansine, 2차 표준치료)**: 마이크로튜불 억제제 emtansine을 trastuzumab에 접합한 ADC로, trastuzumab + taxane 이후 2차 표준치료. EMILIA trial에서 ORR 43.6% (95% CI 38.6–48.6), median PFS 9.6개월 달성.

- **A의 한계**: T-DM1 이후 진행한 환자에게 균일하게 받아들여지는 표준 치료가 정의되어 있지 않다 (본문 §Introduction). 당시 3차 이후 옵션들의 response rate는 약 9–31%, PFS는 약 3–6개월에 불과했다 (본문 refs 7–10). T-DM1 저항 기전으로는 HER2 down-regulation, 이질적 발현(intratumoral/lesion-to-lesion heterogeneity), 수용체 돌연변이, HER2 isoform 발현, lysosomal trafficking 이상, emtansine payload 저항 등이 거론된다 (Discussion §).

- **선행 접근 B — margetuximab + 화학요법(SOPHIA), neratinib + 화학요법(NALA)**: 3차 이후 HER2 표적 요법의 Phase 3 시도. SOPHIA에서 실험군 response rate 22.8%, median PFS 5.8개월; NALA에서 6개월 PFS 약 47%. 의미 있는 생존 연장을 입증하지 못했다.

- **이 논문으로 이어지는 gap**: T-DM1 이후 표준 치료 부재 + 기존 옵션의 낮은 반응률 → 새로운 구조의 ADC 필요. 특히 ① T-DM1에 쓰는 maytansinoid(미세소관 억제)와 다른 payload, ② 더 높은 drug-to-antibody ratio (DAR), ③ 막투과성 높은 bystander killing payload가 저항 극복에 기여할 것이라는 가설.

#### 기본 개념

- **HER2 (human epidermal growth factor receptor 2)**: ErbB2/neu 수용체 타이로신 인산화효소. HER2 양성은 IHC 3+ 또는 IHC 2+/ISH 양성으로 정의. 전이성 유방암에서 과발현·증폭 시 예후 불량 및 HER2 표적 치료 반응성과 연관.

- **ADC (antibody-drug conjugate)**: 단클론항체(표적)—링커—세포독성 payload 세 부분으로 구성. 항체가 표적 세포 수용체에 결합 → 내재화 → 링커 절단(intracellular 또는 plasma) → payload 방출 → 세포사멸. 이 논문의 T-DXd는 cleavable tetrapeptide 링커 + Topo I 억제제 (DXd).

- **Drug-to-antibody ratio (DAR)**: 항체 한 분자당 payload 분자 수. T-DXd: DAR ≈ 8 vs. T-DM1: DAR ≈ 3–4. 높은 DAR = 동일 항체 투여량에서 더 많은 payload 전달.

- **Bystander killing effect**: ADC가 표적 HER2 양성 세포에서 payload를 방출한 뒤, 고막 투과성 payload가 인접 HER2 음성/저발현 세포도 사멸. T-DM1의 emtansine은 낮은 막투과성 → bystander 약함. T-DXd의 DXd는 높은 막투과성 → bystander 강함 (본문 §Introduction; refs 15, 16).

- **RECIST v1.1 (modified)**: 고형암 치료 반응 평가 기준. Complete Response (CR): 모든 표적 병변 소실; Partial Response (PR): 표적 병변 장경 합 ≥30% 감소; Stable Disease (SD): PR/PD 기준 미충족; Progressive Disease (PD): 장경 합 ≥20% 증가 또는 신규 병변.

#### 이 논문의 필요성

- **핵심 이유**: Phase 1 (DS8201-A-J101)에서 HER2+ 유방암 ORR 59.5%, median DOR 20.7개월을 확인했으나 Phase 2 규모 확증이 필요. T-DM1 이후 unmet medical need 해소 여부를 다기관·다국가 코호트에서 검증.
- **기존 방법으로 부족했던 지점**: Phase 1은 dose-escalation 중심으로 확증적 efficacy evidence 부족. T-DM1 이후 동질적 코호트 대상 단일군 Phase 2 데이터가 없었음.
- **이 논문이 해결하려는 방향**: T-DXd 5.4 mg/kg의 최종 권장 용량 결정 + 충분한 sample size (n=184) 하에서 ITT ORR, DOR, PFS를 ICR 기반으로 확증.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: T-DM1 기치료 HER2+ 전이성 유방암 환자에서 T-DXd 5.4 mg/kg의 단독 요법 efficacy 및 safety를 평가하는 2파트 오픈 라벨 단일군 Phase 2 시험.
- **입력**: T-DM1 치료 이력이 있는 HER2+ 전이성 유방암 성인 환자 (centrally confirmed HER2+, ≥1 measurable lesion, ECOG PS 0–1, LVEF ≥50%).
- **출력**: ICR 기반 ORR (primary endpoint), DOR, PFS, OS, safety (secondary/exploratory).
- **추정 대상**: T-DXd 반응률의 점 추정 + 95% CI; 안전성 profile.
- **중요한 hidden assumption**: 단일군 설계 → 통계적 efficacy는 historical benchmark (T-DM1 이후 3차 이후 ORR ~30% 이하) 와의 비교에 의존. 무작위 대조군 없음.

### 확률 / 통계학적 구조

- **Model family**: Single-arm Phase 2; 기술 통계 + Kaplan-Meier (KM) 추정.
- **Likelihood / objective**: Primary endpoint — ORR (CR+PR) by ICR. 이항 비율 추정. Two-sided 95% CI (Clopper-Pearson exact method 추정; 본문에 method 명시 없음, `추정:` exact 방법 사용).
- **Prior / regularization**: 미제공. Bayesian adaptive 요소 명시 없음. PK/exposure-response 모델에서 dose 결정에 노출-반응 및 노출-안전성 modeling 사용 (Part 1).
- **Latent variable / hidden state**: 해당 없음 (임상시험 분석).
- **Inference / optimization**: KM curves (DOR, PFS, OS). Median 추정과 95% CI. 반응 평가는 ICR (independent central review, modified RECIST v1.1) + investigator 평가 병행.
- **Noise, sparsity, uncertainty 처리**: 추적 불충분 환자는 censoring. PFS/OS에서 censor 표시. Data cutoff: 2019년 8월 1일; median follow-up 11.1개월 (range 0.7–19.9).

### 핵심 method insight

- **기존 방법의 한계**: T-DM1의 DAR ≈ 3–4, microtubule inhibitor payload, 낮은 막투과성 → bystander killing 제한, 낮은 payload delivery 효율. HER2 heterogeneity 환경에서 T-DM1 저항 발생.
- **이 논문이 바꾼 가정**: ① HER2 동일 항체 골격에 Topo I 억제제(DXd) + cleavable tetrapeptide linker 조합 → 다른 저항 기전 우회. ② DAR ~8 → 더 많은 payload per antibody. ③ 높은 막투과성 DXd → bystander 효과. ④ linker는 plasma에서 stable, tumor cell 내 cathepsin에 의해 선택적 절단 (refs 12–15).
- **새로 추가한 변수 또는 구조**: Cleavable tetrapeptide-based linker + topoisomerase I inhibitor payload 조합 (T-DM1의 non-cleavable linker + maytansinoid와 대비).
- **이 변화가 중요한 이유**: T-DM1 저항 후에도 ORR 60.9% 달성 — 기전적으로 distinct payload + bystander killing + high DAR이 T-DM1 저항 기전을 극복한 근거. 단, 이 논문 자체가 mechanism study는 아니므로 인과 관계는 `해석:`으로 분리.

### 이전 방법과의 차이

- **Baseline (T-DM1)**: HER2+ MBC 2차 표준치료; ORR 43.6%, median PFS 9.6개월 (EMILIA); DAR ≈ 3–4, maytansinoid payload, non-cleavable thioether linker.
- **공통점**: 동일 trastuzumab 항체 골격; i.v. 투여; HER2 overexpression 타겟.
- **차이점**: Linker type (cleavable tetrapeptide vs. non-cleavable), Payload (Topo I inhibitor DXd vs. maytansinoid DM1), DAR (~8 vs. ~3–4), membrane permeability of payload (high vs. low), dose (5.4 mg/kg vs. 3.6 mg/kg).
- **차이가 크게 나타나는 조건**: T-DM1 이후 진행 환자 (T-DM1 저항 확보된 집단); HER2 heterogeneous tumor; 낮은 HER2 발현 환자 (HER2-low 활동성 시사됨, ref 18).

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: 184명 ITT 코호트 (median 6회 prior therapy; T-DM1, trastuzumab 100% 경험).
- **Metric**: ORR (ICR), DOR, PFS, OS, DCR, CBR.
- **개선된 결과**: ORR 60.9% vs. T-DM1 이후 옵션 9–31% (historical; cross-trial 비교, 본문 Discussion 강조).
- **Ablation 근거**: 미제공 — Phase 2 임상시험으로 component ablation 설계 없음. Dose justification (5.4 mg/kg vs. 6.4 mg/kg)이 사실상 dose ablation 역할.
- **정성적 효과**: Subgroup analysis에서 pertuzumab 기사용, 호르몬수용체 status, 뇌전이 여부 등 주요 예후 인자에 걸쳐 일관된 반응률 (Fig. 2B).

### Method 관점의 한계

- **약한 assumption**: 단일군 설계 — historical benchmark 대비 우월성은 "apparent" 비교이며 randomized 비교 아님. 저자도 "cross-trial comparisons must be interpreted with caution" 명시 (Discussion §).
- **구현 또는 학습상의 부담**: 미제공 (임상시험이므로 computational 부담 없음). 단, ILD 관리 protocol 이행 부담 높음 (특수 ILD adjudication committee 운영, Supplementary Appendix §ILD 섹션).
- **일반화가 불확실한 조건**: 단일 cohort, 단일 data cutoff (11.1개월 median follow-up), HER2 2+ ISH-양성 환자는 15.2%로 소수 → HER2 2+ 하위군 결론 제한. 인종 다양성: Asian 38.0%, White 54.9%.

---

## Results

### Dataset별 결과

#### Dataset 1 — DESTINY-Breast01 전체 코호트 (ITT, n=184, 5.4 mg/kg)

- **Dataset**: 전이성 HER2+ 유방암 환자 184명. 2017년 10월–2018년 9월 등록, 72개 기관, 8개국 (북미·아시아·유럽). 모든 환자가 T-DM1 및 trastuzumab 기치료. Median prior therapy 6회 (range 2–27).
- **목적**: T-DXd 5.4 mg/kg의 efficacy 확증 (primary endpoint).
- **사용한 데이터 규모**: n=184 (ITT); median follow-up 11.1개월 (range 0.7–19.9); data cutoff 2019년 8월 1일.
- **Baseline / 비교 대상**: 단일군. Historical comparison: T-DM1 이후 표준 3차 치료 옵션 (ORR 9–31%, PFS 3–6개월, 본문 refs 7–10).
- **Metric / 평가 기준**: ICR 기반 ORR (primary), DOR, PFS, OS, DCR, CBR (secondary).
- **주요 수치**:
  - ORR: **60.9%** (95% CI 53.4–68.0) — CR 6.0%, PR 54.9%
  - DCR: **97.3%** (95% CI 93.8–99.1)
  - CBR (SD ≥6개월 포함): **76.1%** (95% CI 69.3–82.1)
  - Median DOR: **14.8개월** (95% CI 13.8–16.9)
  - Median PFS: **16.4개월** (95% CI 12.7–not reached)
  - Median time to response: **1.6개월** (95% CI 1.4–2.6)
  - 6개월 OS: **93.9%** (95% CI 89.3–96.6)
  - 12개월 OS: **86.2%** (95% CI 79.8–90.7)
  - Median OS: **도달하지 않음** (data cutoff 시점)
  - 치료 지속 환자 (data cutoff 기준): 79/184 (42.9%)
  - Median treatment duration: **10.0개월** (range 0.7–20.5)
  - 6개월 이상 치료 지속: 69.6% (128/184)
- **정성 결과**: 168명 중 종양 크기 감소 환자 대부분 (Fig. 2A waterfall plot). PFS curve는 12개월 이후에도 plateau 경향 (Fig. 3B).
- **논문 주장과의 연결**: T-DM1 이후 heavily pre-treated 환자에서 ORR 60.9% 달성 — Phase 1 결과(59.5%) 재현 + 기존 3차 이후 옵션 대비 현저한 개선.

#### Dataset 2 — T-DM1 진행 후 하위 코호트 (n=180)

- **Dataset**: 전체 184명 중 T-DM1에서 진행(progression during or after T-DM1)한 180명.
- **목적**: T-DM1 저항 확보 집단에서의 efficacy 확인.
- **사용한 데이터 규모**: n=180.
- **주요 수치**:
  - ORR: **61.1%** (95% CI 53.6–68.3)
- **논문 주장과의 연결**: T-DM1 저항이 명확한 하위군에서도 전체와 유사한 반응률 → T-DXd가 T-DM1 저항 기전을 우회한다는 간접 근거.

#### Dataset 3 — 뇌전이 하위군 (n=24)

- **Dataset**: 치료받고 무증상인 뇌전이 환자 24명.
- **목적**: 중추신경계 전이 환자 exploratory 분석.
- **주요 수치**:
  - Median PFS: **18.1개월** (95% CI 6.7–18.1)
- **해석**: CI 범위 넓음 (n=24) — 예비적 결과; 결론 확대 자제 요. 뇌 침투 가능성 시사하나 uncontrolled.

#### Dataset 4 — Subgroup 분석 (Fig. 2B)

- **Pertuzumab 기치료 (n=121)**: ORR 64% (78/121)
- **호르몬수용체 양성 (n=97)**: ORR 58% (56/97)
- **호르몬수용체 음성 (n=83)**: ORR 66% (55/83)
- **IHC 3+ (n=154)**: ORR 63% (97/154)
- **IHC 1+/2+, ISH+ (n=28)**: ORR 46% (13/28) — 소수, CI 폭 넓음
- **T-DXd immediately after T-DM1 (n=56)**: ORR 64% (36/56)
- **뇌전이 있음 (n=24)**: ORR 58% (14/24)
- **해석**: 대부분 subgroup에서 ORR 54–76% 범위로 일관. IHC 2+ ISH+ 소군만 46%로 낮지만 sample 소 (n=28, 95% CI 28–66).

#### Dataset 5 — Safety 코호트 (n=184, 5.4 mg/kg)

- **목적**: AE profile 기술.
- **주요 수치**:
  - Any grade AE: 99.5% (183/184)
  - Grade ≥3 AE: 57.1% (89/184 grade 3; 7/184 grade 4)
  - Grade ≥3 AE >5% 해당: decreased neutrophil count 20.7%, anemia 8.7%, nausea 7.6%, decreased WBC 6.5%, decreased lymphocyte 6.5%, fatigue 6.0%
  - Dose interruption: 35.3% (65/184)
  - Dose reduction: 23.4% (43/184)
  - Discontinuation due to AE: 15.2% (28/184)
  - Febrile neutropenia: 1.6% (3/184)
  - ILD (any grade, adjudication): **13.6%** (25/184)
    - Grade 1–2: 10.9% (20/184)
    - Grade 3–4: 0.5% (1/184)
    - Grade 5 (fatal): **2.2%** (4/184) — 본문 Table 2 각주 ‡‡에서 4명 grade 5 포함 명시
  - Decreased LVEF: 1.6% (3/184); clinically significant cardiotoxicity 없음
  - Anti-drug antibody: 6.0% (11/184); 치료 후 새로 발생 3례 모두 치료 중 소실
- **논문 주장과의 연결**: ILD가 핵심 독성 신호. Grade 5 ILD 4명(2.2%)은 규제·임상 관리 관점에서 중요한 안전 이슈.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: T-DM1 이후 heavily pretreated (median 6 lines) 집단에서 ORR ~60%, PFS ~16개월. Subgroup 전반 일관. DCR 97.3%는 거의 모든 환자에서 종양 성장 억제.
- **가장 중요한 수치**: ORR 60.9% (95% CI 53.4–68.0) + ILD 13.6% (fatal 2.2%) — efficacy와 safety를 동시에 특징짓는 두 수치.
- **baseline 대비 차이**: Cross-trial 비교에서 기존 3차 이후 요법(ORR 9–31%) 대비 현저히 높은 반응률. 단 무작위 비교 아님.
- **결과 해석 시 주의점**: 단기 추적 (median 11.1개월), 단일군 설계, OS 미도달 상태, IHC 2+ ISH+ 소집단 과소 대표. Cross-trial ORR 비교는 patient selection 차이 반영.

---

## Figures

#### Figure 1 — Enrollment and Study Design

- **이 Figure가 필요한 이유**: 연구 design과 patient flow를 한눈에 보여주어 ITT 집단 정의 및 각 part의 코호트 구성을 명확히 한다.
- **이 Figure가 뒷받침하는 주장**: 184명이 5.4 mg/kg을 받았음을 CONSORT-style diagram으로 확인.

##### 패널별 설명
- 단일 flow diagram:
  - 353명 eligibility 평가 → 100명 제외 → 253명 등록 → 184명 5.4 mg/kg, 48명 6.4 mg/kg, 21명 7.4 mg/kg
  - 184명 중: Part 1 PK stage 22명 + Part 1 dose-finding 28명 + Part 2a 130명 + Part 2b 4명
  - 184명 중 79명 (42.9%) 계속 치료 중; 105명 (57.1%) 중단 (PD 53명, AE 28명, consent 철회 8명, 사망 7명, 기타)

##### 본문에서 강조한 비교
- 비교 대상: 전체 enrolled vs. 5.4 mg/kg 코호트
- 관찰된 차이: 5.4 mg/kg 코호트가 primary efficacy 분석 집단
- 이 차이가 의미하는 것: 권장 용량 결정 후 Part 2에서 efficacy 집중 평가 설계

##### 해석 시 주의점
- Part 2b (T-DM1 비진행 중단, n=4)는 매우 소수 → 별도 분석 의미 제한.

---

#### Figure 2 — Efficacy

- **이 Figure가 필요한 이유**: ORR의 크기와 subgroup 일관성을 시각적으로 입증.
- **이 Figure가 뒷받침하는 주장**: 주요 예후·인구통계 subgroup에 걸쳐 T-DXd의 반응이 일관적임.

##### 패널별 설명
- **Panel A (Waterfall plot)**: 168명의 baseline 대비 종양 크기 변화 최대값. 대다수 환자에서 종양 감소. 일부 환자는 매우 큰 감소(≥80%).
- **Panel B (Forest plot)**: 14개 사전 지정 subgroup별 ORR (점 추정 + 95% CI). 전체 ORR 61%, 각 subgroup 54–76% 범위로 CI 겹침.

##### 본문에서 강조한 비교
- 비교 대상: pertuzumab 기치료 여부, 호르몬수용체 status, 뇌전이 유무, HER2 IHC 강도 등
- 관찰된 차이: IHC 2+ ISH+ 집단 (46%)을 제외하면 모든 subgroup에서 ORR 54% 이상
- 이 차이가 의미하는 것: efficacy가 특정 subgroup에 편향되지 않음을 저자가 강조

##### 해석 시 주의점
- Forest plot의 CI는 소 sample subgroup에서 매우 넓음 (예: 뇌전이 24명, CI 37–78). 통계적 interaction test 결과는 미제공 → subgroup 간 실제 차이 여부 판단 불가.
- `해석:` IHC 2+ 집단의 낮은 ORR (46%)은 생물학적으로 흥미롭지만 n=28로 결론 도출에 제한.

---

#### Figure 3 — Kaplan-Meier Analysis

- **이 Figure가 필요한 이유**: DOR와 PFS의 지속 시간을 시각화하여 durability 주장을 뒷받침.
- **이 Figure가 뒷받침하는 주장**: T-DXd의 반응이 단기가 아니라 median 14–16개월 이상 유지됨.

##### 패널별 설명
- **Panel A (Response duration KM)**: 112명 반응자 대상. Median DOR 14.8개월 (95% CI 13.8–16.9). 12개월 시점에서도 대부분 반응 유지 (curve 높은 위치).
- **Panel B (PFS KM)**: 전체 184명. Median PFS 16.4개월 (95% CI 12.7–not reached). PD 48명, 사망 10명 by 20개월; 126명 censor.

##### 본문에서 강조한 비교
- 비교 대상: DOR curve가 T-DM1 이후 historical comparison과 implicit 비교
- 관찰된 차이: T-DXd DOR 14.8개월 vs. T-DM1 EMILIA median DOR (본문 직접 수치 미제공; PFS 9.6개월 참조)
- `해석:` PFS 16.4개월은 median follow-up 11.1개월 아직 초과 — 충분한 추적 전 median에 도달한 것이므로 신뢰도 높지만 median OS는 미도달로 장기 생존 benefit 판단 유보.

##### 해석 시 주의점
- 추적 기간 중앙값 11.1개월로 PFS curve의 후반부 event 수 적음. OS curve (Fig. S2)는 supplementary에서 제시되나 미도달.
- 뇌전이 하위군 PFS (18.1개월)는 n=24로 CI가 6.7–18.1로 매우 좁지 않음.

---

## Tables

### Table 1 — Patient Demographics and Baseline Characteristics (본문, n=184)

- **이 Table이 필요한 이유**: 184명 ITT 코호트의 기저 특성을 요약하여 환자군의 대표성과 치료 이력의 extensive함을 보여줌.
- **이 Table이 뒷받침하는 주장**: Median 6회 이전 치료(range 2–27), T-DM1·trastuzumab 100% 경험 → 이 연구의 환자가 truly heavily pretreated임.

#### 표 구조
- Row: 환자 특성 항목 (연령, 성별, 인종, 지역, ECOG PS, 호르몬수용체, HER2 발현, 종양 크기, 이전 치료 수, 이전 치료제별 비율, T-DM1 최선 반응)
- Column: n=184 (%)
- 셀 값: n (%), median (range)

#### 핵심 수치
- Median age: 55.0세 (range 28–96); ≥65세: 23.9%
- ECOG PS 0: 55.4%, PS 1: 44.0%
- HER2 IHC 3+: 83.7%; IHC 1+/2+ ISH+: 15.2%
- HR+: 52.7%, HR–: 45.1%
- Median prior regimens: 6 (range 2–27)
- Prior trastuzumab: 100%; Prior T-DM1: 100%; Prior pertuzumab: 65.8%; Other anti-HER2: 54.3%
- Best response to T-DM1: CR/PR/SD 42.9%; PD 35.9%

#### 본문에서 강조한 비교
- 비교 대상: "heavily pretreated" 환자 기술이 주목적
- 관찰된 차이: Median 6회 치료 → 이 집단에서 60.9% ORR는 현저한 수치임

#### 해석 시 주의점
- 전체 253명 특성은 Table S1에 별도 제시. T-DM1 최선 반응 불명 (could not be evaluated) 14명(7.6%) — bias 가능성 제한적.

---

### Table 2 — Adverse Events (본문, n=184)

- **이 Table이 필요한 이유**: T-DXd의 safety profile을 정량화하며 특히 ILD라는 독특한 독성을 보여줌.
- **이 Table이 뒷받침하는 주장**: T-DXd는 GI/hematologic 독성과 더불어 ILD라는 class-specific 독성이 있으며, 이는 관리 가능하지만 grade 5(치명적) 사례도 있음.

#### 표 구조
- Row: AE 종류 (>15% in any grade + 특별 관심 AE)
- Column: Any grade n(%), Grade 3 n(%), Grade 4 n(%)
- 셀 값: n(%)

#### 핵심 수치
- Nausea: 77.7% any grade, 7.6% grade 3
- Fatigue: 49.5% any, 6.0% grade 3
- Alopecia: 48.4% any
- Decreased neutrophil count: 34.8% any, 20.7% grade 3 (highest grade ≥3)
- Anemia: 29.9% any, 8.7% grade 3
- ILD (adjudication-confirmed): **13.6% any grade** (25/184); grade 3: 0.5% (1명); grade 5: 4명 — Table 2 각주 ‡‡ 명시
- Decreased LVEF: 1.6% any; grade 3: 0.5% (1명 → LVEF >55% 유지)

#### 본문에서 강조한 비교
- 비교 대상: trastuzumab/pertuzumab 관련 cardiomyopathy vs. T-DXd
- 관찰된 차이: clinically significant cardiotoxicity 없음 (LVEF 감소 1.6%에 불과)
- 이 차이가 의미하는 것: 심독성은 주요 우려 아님; ILD가 dominant 안전 이슈

#### 해석 시 주의점
- ILD grade 5 (치명적) 4명 — 백분율 2.2%. Table 각주 ‡‡에서 이 4명이 "any grade" 25명 안에 포함됨 명시. Supplementary에서 ILD 관리 프로토콜 별도 제공.
- `해석:` ILD 2.2% fatality는 단일군 연구 크기(n=184) 기준으로는 적지만, 적용 규모 확대 시 환자 절대수 증가 → 임상 현장 관리 중요.

---

### Supplementary Tables (appendix)

- **Table S1**: 전체 253명 characteristics — 5.4 mg/kg 코호트와 유사.
- **Table S2**: Part 1 (dose별 efficacy) — 6.4 mg/kg 코호트 등 reference.
- **Table S3**: 전체 safety summary (grade 1–4 분류).
- **Table S4**: 10% 이상 AE (전체 253명).
- **Table S5**: 10% 이상 AE (5.4 mg/kg 184명, 인과관계 불문).
- **Table S6**: ILD 관리 updated guideline — grade별 용량 조정·중단·스테로이드 사용 권고.

---

## Supplementary Information

### 포함 내용 (Supplementary Appendix, 22 pages)

- **연구자 목록**: 8개국 72개 기관, country별 site + principal investigator 전체 목록 (Appendix pages 2–5).
- **Inclusion/Exclusion Criteria**: 상세 기재 (Appendix pages 5–7). ILD 병력 보유자, 뇌전이 중 symptomatic·미치료자 등 제외.
- **Safety Assessment 방법**: TEAE, SAE, 특별 관심 AE, 심전도, 안과 검사 포함 (Appendix page 7).
- **ILD 관리 프로토콜**: 독립 다학제 ILD adjudication committee 운영, grade별 관리 algorithm, corticosteroid 사용 지침 (Appendix pages 7–8 + Table S6). Grade 1 → 완전 소실 시 재투여 (28일 내 소실이면 동일 용량, 28일 초과 시 1단계 감량), Grade 2 이상 → 영구 중단.
- **Supplementary Figure S1**: Study design schema (Part 1 PK stage → dose-finding → Part 2a, 2b).
- **Supplementary Figure S2**: OS KM curve — 6개월 93.9%, 12개월 86.2%; median 미도달.
- **프로토콜 및 공개 자료**: Study protocol NEJM.org에 공개; 저자 별도 data sharing statement 첨부.

---

## 분석 자체에 대한 메모

- 이 논문은 계산 방법론 논문이 아닌 임상시험 결과 보고이므로 `core-methods`의 확률/통계 구조 분석은 임상시험 설계·통계 분석 측면에서 작성.
- Phase 1 (DS8201-A-J101, NCT02564900) 결과와의 정합성: Phase 1 ORR 59.5% vs. Phase 2 ORR 60.9% — 재현성 높음.
- ILD 독성 데이터의 해석: Table 2 각주 ‡‡에서 grade 5 환자 4명이 "any grade" 25명에 포함된다고 명시. 본문 pg. 616에서 "grade 5, 2.2%" 명시. 이 수치는 이후 임상 및 FDA 심사에서 핵심 안전성 이슈가 됨 (외부 맥락으로 별도 분리; `외부 맥락:` 임상 현장에서 T-DXd ILD 모니터링 필수 체계 수립의 직접 근거가 된 study임).
- OS data 미성숙: Median OS 미도달 상태 — 2020년 논문 기준. 이후 연장 추적 결과는 별도 논문 참조 필요.
- `검토필요:` 본문 Table 2의 정확한 ILD grade 분포 — footnote ‡‡와 본문 pg. 616 기술이 일관: 4명 grade 5가 25명 "any" 안에 포함. Grade 3/4 수치는 각각 grade 3: 1명(0.5%), grade 4: 0명 (본문 pg. 616 및 Table 2). Grade 5: 4명(2.2%) — 이는 본문 Table에 별도 열로 제시되지 않고 각주에서 처리됨.
