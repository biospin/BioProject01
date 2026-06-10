# shitara-2020-destiny-gastric01 — Core Analysis

---

## Executive Summary

- **무엇**: HER2 양성 위암 2차 이상 치료 실패 환자에서 T-DXd(trastuzumab deruxtecan, DS-8201)를 의사 선택 화학요법(이리노테칸/파클리탁셀)과 비교한 open-label Phase 2 RCT(DESTINY-Gastric01). 이전 trastuzumab 포함 요법 실패 후 T-DXd가 ORR 및 OS를 통계적으로 유의미하게 개선함을 처음으로 증명.
- **모델 / 방법**: 2:1 무작위 배정(T-DXd 6.4 mg/kg q3w vs. 의사 선택), primary endpoint = ORR (독립 중앙 검토, RECIST v1.1), key secondary = OS; 고정 순차 검정(fixed-sequence testing) + Lan–DeMets O'Brien–Fleming boundary로 familywise type I error 0.05 통제.
- **핵심 결과**:
  - ① ORR (T-DXd vs. 화학요법): 51% (95% CI 42–61) vs. 14% (6–26), P<0.001
  - ② Confirmed ORR: 43% vs. 12%; confirmed complete response 10명(8%) vs. 0명
  - ③ OS: 중앙값 12.5개월 vs. 8.4개월, HR 0.59 (95% CI 0.39–0.88), P=0.01
  - ④ PFS: 중앙값 5.6개월 vs. 3.5개월, HR 0.47 (95% CI 0.31–0.71)
  - ⑤ ILD/pneumonitis(T-DXd): 12명(10%), grade 3/4 3건, 1명 drug-related 사망(폐렴)
- **우리 적용**: ADC target 선정 및 BD pitch 근거 자료로 직접 활용 가능(regulatory-precedent + BD-opportunity). HER2 IHC/ISH 동반진단 설계·ADC payload 선택 framework의 clinical benchmark.
- **심층**: 한계·재현 ROI는 `shitara-2020-destiny-gastric01_lens-academic.md` / `shitara-2020-destiny-gastric01_lens-industry.md` / `shitara-2020-destiny-gastric01_methodology-brief.md` 참고.

---

## Identity

- **Title**: Trastuzumab Deruxtecan in Previously Treated HER2-Positive Gastric Cancer
- **Authors**: Kohei Shitara, Yung-Jue Bang, Satoru Iwasa, Naotoshi Sugimoto, Min-Hee Ryu, Daisuke Sakai, Hyun-Cheol Chung, Hisato Kawakami, Hiroshi Yabusaki, Jeeyun Lee, Kaku Saito, Yoshinori Kawaguchi, Takahiro Kamio, Akihito Kojima, Masahiro Sugihara, Kensei Yamaguchi et al.
- **Year**: 2020
- **Venue**: New England Journal of Medicine, 382:2419–2430
- **DOI**: 10.1056/NEJMoa2004413
- **Citation key**: shitara2020destinygastric
- **Document type**: paper (peer-reviewed RCT)
- **ClinicalTrials.gov**: NCT03329690 (DESTINY-Gastric01)
- **Sponsor**: Daiichi Sankyo; AstraZeneca co-authored post-collaboration agreement (March 2019)

---

## Background

### 배경 스토리

#### 배경 스토리

- **문제의 출발점**: HER2 양성 위·위식도접합부(GEJ) 선암은 동아시아를 중심으로 전체 위암의 약 15–20%를 차지한다. 1차 치료로 trastuzumab + 화학요법이 표준(ToGA 시험, OS 13.8 개월 vs. 11.1 개월)이지만, 이후 2차·3차 치료에서는 HER2 표적 치료가 유의한 OS 개선을 보이지 못했다.

- **선행 접근 A — 표준 2차 치료 (ramucirumab + paclitaxel)**: HER2 무관하게 2차 치료에서 OS 9.6개월(vs. 단독 paclitaxel 7.4개월), PFS 4.4개월(vs. 2.9개월), ORR 28%(vs. 16%)를 달성했으나 HER2 특이 치료 효과 없음.

- **A의 한계**: ramucirumab은 VEGFR-2 차단제로 HER2 표적이 아니며, 3차 이후 치료 옵션이 매우 제한적이다.

- **선행 접근 B — 3차 이후 HER2 표적 시도**: lapatinib + 화학요법(TyTAN, LOGiC), pertuzumab + trastuzumab + 화학요법(JACOB), trastuzumab emtansine(T-DM1, GATSBY), 지속적 trastuzumab + paclitaxel 등이 시험되었으나 위암에서 OS 연장 실패. T-DM1의 경우 ORR 20.6%(vs. 19.6%), OS 7.9개월(vs. 8.6개월)로 열세.

- **B의 한계**: HER2 표적 치료 실패의 기전으로 (1) trastuzumab 내성(PI3K 변이, 다른 성장인자 수용체 신호 증가), (2) 치료 후 HER2 발현 감소, (3) 위암에서 흔한 heterogeneous HER2 발현이 지목된다. 기존 ADC인 T-DM1은 payload(emtansine)가 항체 분해 후에도 linker에 결합된 형태로 남아 막투과성이 낮고 bystander killing이 제한적이다.

- **이 논문으로 이어지는 gap**: (1) bystander killing이 가능한 membrane-permeable payload를 가진 ADC, (2) drug-to-antibody ratio(DAR) ~8로 높은 payload 밀도, (3) lysosomal cathepsin에 의해 절단되는 cleavable linker를 조합하면 heterogeneous HER2 발현에서도 효과를 낼 수 있다는 가설이 DS-8201(trastuzumab deruxtecan) 개발로 이어진다.

#### 기본 개념

- **Antibody-drug conjugate (ADC)**: 항체, linker, cytotoxic payload 세 요소로 구성. 항체가 종양 표면 항원(HER2)에 결합 → 내재화(internalization) → lysosome에서 linker 절단 → payload 방출 → DNA 손상 또는 세포 사멸.
- **Trastuzumab deruxtecan (T-DXd, DS-8201)**: humanized anti-HER2 monoclonal antibody에 cleavable tetrapeptide linker로 topoisomerase I inhibitor(DXd, exatecan derivative)를 결합. DAR ≈ 8 (T-DM1 DAR ≈ 3.5). Linker는 혈중에서 안정적이지만 lysosomal cathepsin(암세포 과발현)에 의해 절단된다.
- **Bystander killing effect**: T-DXd에서 방출된 DXd payload는 막투과성이 높아 인접 HER2 음성 세포에도 확산되어 사멸을 유도. 이론적으로 HER2 heterogeneous 종양에서 유리.
- **HER2 heterogeneity in gastric cancer**: HER2 IHC 3+/ISH+ 비율이 위암에서 유방암보다 낮고, 병소 내(intratumoral) 불균일성이 더 크다. 이것이 기존 HER2 표적제의 제한 요인.
- **RECIST v1.1**: 고형종양 반응 평가 기준. Complete response(CR), Partial response(PR, ≥30% 감소), Stable disease(SD), Progressive disease(PD, ≥20% 증가). ORR = CR + PR.

#### 이 논문의 필요성

- **핵심 이유**: 위암 3차 이후 치료에서 유효한 HER2 표적 치료가 존재하지 않았다.
- **기존 방법으로 부족했던 지점**: T-DM1 실패의 주된 원인으로 낮은 막투과성 payload와 낮은 DAR이 지목되며, 이를 극복하기 위한 새 구조의 ADC 필요.
- **이 논문이 해결하려는 방향**: 높은 DAR + bystander killing 가능 DXd payload + cleavable linker를 갖춘 T-DXd가 HER2 양성 위암 3차 이후에서 화학요법 대비 ORR·OS 모두에서 우월한지 Phase 2 RCT로 검증.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: HER2 양성 위·GEJ 선암, 2개 이상 이전 치료(trastuzumab 포함) 실패 환자에서 T-DXd vs. 의사 선택 화학요법의 ORR·OS 비교 (Phase 2 open-label RCT).
- **입력**: HER2 IHC 3+ 또는 IHC 2+/ISH+ 중앙 확인, ECOG PS 0–1, 측정 가능 병변 보유 환자.
- **출력**: ORR(primary), OS(key secondary), confirmed ORR, PFS, response duration, safety.
- **추정 대상**: T-DXd ORR ≥ 30% (귀무가설: ≤ 15%), OS HR < 1.
- **중요한 hidden assumption**: ORR을 primary endpoint로 설정한 Phase 2 디자인. Phase 3 수준의 overall survival power가 아니라 ORR으로 항암 활성 증명 후 OS는 이차 검증.

### 확률 / 통계학적 구조

- **Study design**: Open-label, randomized, Phase 2; 2:1 배정비(T-DXd:PC); 지역(일본/한국), ECOG PS, HER2 상태로 층화.
- **Primary endpoint 통계**: Cochran–Mantel–Haenszel test (지역 층화), Fisher's exact test(민감도 분석). T-DXd ORR ≥ 30% 귀무가설, 양측 α = 0.05.
- **OS 통계**: stratified log-rank test (지역 층화). Lan–DeMets alpha-spending function + O'Brien–Fleming boundary. 최종 분석: ~133명 사망 후. Hazard ratio: Cox proportional-hazards regression (지역 층화 + unstratified 모두 보고).
- **Fixed-sequence testing**: ORR 유의 → OS 같은 α 0.05에서 검정. Familywise type I error 0.05 통제.
- **Kaplan–Meier**: OS, PFS, response duration. 중앙값 95% CI: Brookmeyer–Crowley method.
- **Response duration, PFS**: 이벤트(진행 또는 사망) + 검열(새 항암제 시작 등).

### 핵심 method insight

- **기존 방법의 한계**: T-DM1(GATSBY)은 DAR ~3.5 + 막비투과성 DM1 payload + non-cleavable linker로, HER2 heterogeneous 위암에서 ORR 20%에 그쳤다.
- **이 논문이 바꾼 가정**: DAR ~8 + DXd(막투과성, topoisomerase I inhibitor) + cleavable tetrapeptide linker 조합으로 bystander killing을 통해 HER2 heterogeneous 위암에서도 효과를 낼 수 있다.
- **새로 추가한 변수/구조**: DXd의 막투과성(bystander killing)과 cathepsin-cleavable linker의 조합은 HER2 저발현 세포까지 payload가 도달하는 경로를 제공한다.
- **이 변화가 중요한 이유**: 위암의 heterogeneous HER2 발현 문제를 구조적으로 우회할 수 있다는 mechanistic 근거.

### 이전 방법과의 차이

- **Baseline**: T-DM1 (GATSBY trial), lapatinib + chemotherapy (TyTAN, LOGiC), pertuzumab + trastuzumab + chemotherapy (JACOB).
- **공통점**: anti-HER2 antibody 골격, HER2 IHC/ISH 선별.
- **차이점**:
  - DAR: T-DXd ≈ 8 vs. T-DM1 ≈ 3.5
  - Payload: DXd(topoisomerase I inhibitor, 막투과성) vs. DM1(microtubule inhibitor, 막비투과성)
  - Linker: cleavable tetrapeptide vs. non-cleavable thioether
  - Bystander killing: T-DXd 가능 vs. T-DM1 제한적
- **차이가 크게 나타나는 조건**: HER2 heterogeneous, HER2 IHC 2+/ISH+ 환자군. 그러나 본 시험에서 IHC 2+/ISH+ 환자는 28명(29%)으로 소수여서 서브그룹 해석 주의.

### 효과가 Results에서 나타난 방식

- **Benchmark**: 187명 treated; T-DXd 125명, PC 62명 (이리노테칸 55명, 파클리탁셀 7명).
- **ORR**: 51% vs. 14%, P<0.001 → primary endpoint 달성.
- **OS**: 12.5 vs. 8.4개월, HR 0.59, P=0.01 → O'Brien–Fleming boundary 0.0202 통과.
- **Ablation 근거**: HER2 IHC 3+ vs. 2+/ISH+ subgroup에서 ORR 58% vs. 29% 차이 — HER2 발현 수준이 효과에 영향. 단 2+/ISH+ N=28로 소수이므로 단정 불가.
- **정성적 효과**: 80% 이상 환자에서 종양 크기 감소(PC 50% 대비), confirmed complete response 10명(8%) — 이는 위암 3차 치료에서 이례적.

### Method 관점의 한계

- **약한 assumption**: Phase 2 open-label 디자인 — performance bias 위험, 독립 중앙 검토가 blinding을 부분 보완하나 완전 이중 맹검은 아님.
- **구현 또는 학습상의 부담**: T-DXd 투약 용량(6.4 mg/kg)이 유방암 표준(5.4 mg/kg)보다 높아 위암 특화 독성 프로파일 필요.
- **일반화가 불확실한 조건**: 일본(79%)·한국(21%)만 참여 → 서양 환자 외삽 불확실. HER2 양성 기준을 최근 archival tissue로만 확인했기 때문에 시간 경과에 따른 HER2 status 변화 반영 불가.

---

## Results

### Dataset별 결과

#### DESTINY-Gastric01 Phase 2 RCT (Primary Analysis)

- **Dataset**: HER2 양성 위·GEJ 선암 환자 (2017년 11월 – 2019년 5월). 일본 48개 기관, 한국 18개 기관.
- **목적**: T-DXd가 trastuzumab 포함 2차 이상 요법 실패 후 3차 치료로서 ORR 및 OS를 화학요법 대비 개선하는지 검증.
- **사용한 데이터 규모**: 무작위 배정 188명, 치료받은 187명 (T-DXd 125명, PC 62명). 중앙 나이 T-DXd 65세(범위 34–82), PC 66세(28–82). ECOG PS 0–1 균형.
- **Baseline/비교 대상**: 의사 선택 화학요법 (irinotecan 150 mg/m² q2w 또는 paclitaxel 80 mg/m² day 1/8/15 q4w).
- **Metric/평가 기준**: ORR(primary, independent central review, RECIST v1.1), OS(key secondary), confirmed ORR, PFS, response duration, safety.

**주요 수치:**

- ORR: T-DXd 51% (95% CI 42–61, n=119 평가 가능) vs. PC 14% (95% CI 6–26, n=56), P<0.001 (Cochran–Mantel–Haenszel)
- Confirmed ORR: T-DXd 43% (95% CI 34–52) vs. PC 12% (95% CI 5–24)
- Confirmed complete response: T-DXd 10명 (8%) vs. PC 0명
- Confirmed partial response: T-DXd 41명 (34%) vs. PC 7명 (12%)
- Disease control rate: T-DXd 86% (95% CI 78–91) vs. PC 62% (95% CI 49–75)
- Median response duration (confirmed): T-DXd 11.3개월 (95% CI 5.6 – NE) vs. PC 3.9개월 (3.0–4.9)
- Median time to response: T-DXd 1.5개월 (1.4–1.7) vs. PC 1.6개월 (1.3–1.7) — 유사
- OS: T-DXd 12.5개월 (95% CI 9.6–14.3) vs. PC 8.4개월 (6.9–10.7), HR 0.59 (95% CI 0.39–0.88), P=0.01 (O'Brien–Fleming boundary 0.0202 통과)
  - 6개월 생존율: T-DXd 80%, PC 66%
  - 12개월 생존율: T-DXd 52%, PC 29%
  - 사망: 101/187명 (T-DXd 62/125 [50%], PC 39/62 [63%])
- PFS: T-DXd 5.6개월 (4.3–6.9) vs. PC 3.5개월 (2.0–4.3), HR 0.47 (95% CI 0.31–0.71)
  - 6개월 PFS: T-DXd 43%, PC 21%
  - 12개월 PFS: T-DXd 30%, PC 0%

해석: OS HR 0.59는 임상적으로 의미 있는 효과 크기다. 단, OS 개선의 일부는 PC군에서 후속 치료를 더 받은 점(74% vs. 48%)에 기인할 수 있어 교란 요인이 존재한다.

**HER2 IHC 서브그룹:**
- IHC 3+: ORR 58% (53/91명) vs. 29% (8/28명, IHC 2+/ISH+)
- 해석: HER2 발현 수준과 T-DXd 반응률의 상관성이 관찰되나 N이 작아 단정 불가. IHC 2+/ISH+ 서브그룹에서도 의사 선택 대비 우월성은 유지.

**후속 치료:** T-DXd군 48% vs. PC군 74%가 후속 항암치료 받음; PD-1/PD-L1 억제제 사용 T-DXd군 31%, PC군 45%.

**Safety — Grade 3 이상 주요 이상반응:**
| 이상반응 | T-DXd (N=125) | PC (N=62) |
|---|---|---|
| 호중구감소증 | 51% (Grade 3: 38%, Grade 4: 13%) | 24% (16%, 8%) |
| 빈혈 | 38% (38%, 0%) | 23% (21%, 2%) |
| 백혈구감소증 | 21% (21%, 0%) | 11% (8%, 3%) |
| 식욕감소 | 17% (17%, 0%) | 13% (13%, 0%) |

- 발열성 호중구감소증: T-DXd 6명(모두 Grade 3) vs. PC 2명
- 치료 중단: T-DXd 15% vs. PC 6%
- 치료 중단(이상반응): T-DXd 62% vs. PC 37%
- 용량 감량: T-DXd 32% vs. PC 34% (유사)
- Drug-related 사망: T-DXd 1명(폐렴), PC 0명

**ILD/Pneumonitis (T-DXd 특이적):**
- 12명(10%): Grade 1 3건, Grade 2 6건, Grade 3 2건, Grade 4 1건, Grade 5 0건
- 발병까지 중앙 시간: 84.5일 (범위 36–638일)
- 중앙 지속 기간: 57.0일; 8명 회복·회복 중, 3명 미회복, 1명 미상
- PC군: ILD 없음
- 좌심실박출률 감소·심부전: 양군 모두 없음

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: T-DXd가 ORR, confirmed ORR, OS, PFS, response duration 모두 PC 대비 개선. 효과는 일본·한국, ECOG PS, HER2 IHC 3+/2+ 등 주요 서브그룹에서 일관되게 관찰.
- **가장 중요한 수치**: ORR 51% vs. 14% (P<0.001), OS HR 0.59 (P=0.01).
- **Baseline 대비 차이**: 3차 치료에서 ORR 51%는 이전 HER2 표적제(T-DM1 20.6%)나 면역관문억제제(nivolumab 11.2%, pembrolizumab 11.6%)를 크게 상회.
- **결과 해석 시 주의점**:
  1. Open-label 디자인 — observer bias 가능성.
  2. 후속 치료 비율 불균형(PC군이 더 많이 받음) — OS 비교 교란 요인.
  3. 일본·한국만의 시험 — 서양 위암 환자군에서 외삽 불확실(이후 서양 코호트 연구로 보완).
  4. HER2 status가 최근 archival tissue 기준 — 치료 중 HER2 변화 미반영.
  5. Phase 2, N=187 — 규모 제한(저자도 명시).

---

## Figures

### Figure 1 — Best Percentage Change from Baseline (Waterfall Plot)

- **이 Figure가 필요한 이유**: ORR(51% vs. 14%)이라는 요약 수치만으로는 반응의 분포와 깊이가 전달되지 않는다. 환자별 종양 크기 변화를 waterfall plot으로 시각화함으로써 대부분의 T-DXd 환자에서 실질적인 종양 감소가 일어났음을 직관적으로 제시.
- **이 Figure가 뒷받침하는 주장**: T-DXd는 일부 환자에서만 반응하는 것이 아니라 대다수 환자(>80%)에서 종양을 줄인다는 주장.

#### 패널별 설명

- **A (T-DXd, N=117)**: 대부분의 바(bar)가 0% 아래, 즉 종양 감소. 다수가 −30% 이하(partial response 기준선) 통과. 완전 소실(−100%)에 근접한 환자도 다수. 20% 이상 증가(PD 기준선) 초과 환자는 소수.
- **B (PC, N=52)**: 바가 넓게 분포, 종양 감소 환자와 증가 환자가 혼재. −30% 이하는 소수. 전반적으로 0% 근방이나 양(+) 방향 분포 우세.

#### 본문에서 강조한 비교

- 비교 대상: T-DXd >80% 환자 종양 크기 감소 vs. PC 약 50% 환자 감소.
- 관찰된 차이: T-DXd에서 종양 감소의 깊이(depth of response)가 명확히 우월.
- 이 차이가 의미하는 것: ORR 수치 차이가 outlier에 의존하지 않고 전체적인 반응 프로필에서 나타남을 보여줌.

#### 해석 시 주의점

- Waterfall plot은 선택적 표시 가능. T-DXd 2명, PC 4명이 기저값 또는 추적 종양 평가 없어 제외됨.
- 개별 바는 독립 중앙 검토(ICR) 기반. 검토 시점의 평가 방법이 반응 분류에 영향 가능.

---

### Figure 2 — Overall Survival (Panel A) and Progression-free Survival (Panel B) (Kaplan-Meier)

- **이 Figure가 필요한 이유**: ORR은 반응 여부만 보여주지만, 임상적 실익은 생존 연장으로 입증되어야 한다. OS와 PFS의 KM 곡선이 두 군의 차이를 시간 경과에 따라 시각화한다.
- **이 Figure가 뒷받침하는 주장**: T-DXd가 화학요법 대비 생존을 유의미하게 연장한다.

#### 패널별 설명

- **Panel A (OS)**: 두 곡선이 초기부터 분리되어 T-DXd군이 지속적으로 우위. 12개월 시점 생존율 52%(T-DXd) vs. 29%(PC)로 두 배 가까이 차이. HR 0.59, P=0.01.
  - T-DXd: 중앙 OS 12.5개월 (9.6–14.3), 62/125 사망
  - PC: 중앙 OS 8.4개월 (6.9–10.7), 39/62 사망
- **Panel B (PFS)**: T-DXd군이 초반부터 분리. 12개월 PFS T-DXd 30% vs. PC 0%. HR 0.47, P value 미제공(본문에 통계 기술 없음, HR만 제시).
  - T-DXd: 중앙 PFS 5.6개월 (4.3–6.9), 73/125 이벤트
  - PC: 중앙 PFS 3.5개월 (2.0–4.3), 36/62 이벤트

#### 본문에서 강조한 비교

- O'Brien–Fleming boundary(0.0202) 통과 — 사전 규정된 interim OS 분석에서 통계적 유의성 확보.
- PC군 74% vs. T-DXd군 48%가 후속 치료(특히 PD-1/PD-L1 억제제)를 받아 OS 격차가 실제 효과보다 과소평가될 가능성.

#### 해석 시 주의점

- PFS HR 0.47에 대한 통계적 유의성 검정(p-value)이 본문 Figure 2B에 명시되지 않음 — 본문에서 수치만 제시(HR, CI). 미제공.
- Censoring 비율: T-DXd 42%, PC 42% — 균형.

---

## Tables

### Table 1 — 환자 기저 특성 (Demographic and Clinical Characteristics)

- **이 Table이 필요한 이유**: 2:1 비율 무작위 배정의 균형 여부를 확인하고, 두 군의 baseline이 비슷하여 결과 비교가 타당함을 보여주기 위해.
- **이 Table이 뒷받침하는 주장**: 무작위화가 주요 예후 인자에서 균형을 달성했다.

#### 표 구조

- Row: 환자 특성 (나이, 성별, 지역, ECOG PS, 조직학, HER2 발현, 원발 부위, 종양 크기, 이전 치료)
- Column: T-DXd (N=125), PC (N=62)
- 셀 값: 중앙값(범위) 또는 n(%)

#### 핵심 수치

- 중앙 나이: T-DXd 65세 (34–82) vs. PC 66세 (28–82)
- 여성: T-DXd 24%, PC 24% — 동일
- 지역: 일본 T-DXd 79%, PC 81%
- ECOG PS 0: T-DXd 50%, PC 48%
- HER2 IHC 3+: T-DXd 77%, PC 76%
- 이전 irinotecan/topoisomerase I inhibitor: T-DXd 6%, PC 8%
- 이전 면역관문억제제: T-DXd 35%, PC 27% — 약간 불균형(T-DXd군이 더 많이 받음)

#### 해석 시 주의점

- 이전 면역관문억제제 사용이 T-DXd군에서 약간 더 높아(35% vs. 27%) 내성 프로파일이 다를 가능성. 통계적 유의성 불명(이 표에서 p-value 미제공).
- 이전 치료 횟수 ≥4: T-DXd 20%, PC 10% — T-DXd군에서 더 많이 pre-treated. 이는 T-DXd군에 불리한 방향으로 baseline이 약간 치우쳤을 가능성.

---

### Table 2 — 유효성 요약 (Summary of Efficacy)

- **이 Table이 필요한 이유**: ORR, confirmed ORR, 반응 분류(CR/PR/SD/PD)를 수치로 정리해 primary endpoint 결과를 명확히 제시.
- **이 Table이 뒷받침하는 주장**: T-DXd의 ORR(51%)이 PC(14%)보다 유의하게 높다.

#### 표 구조

- Row: 반응 분류 및 요약 통계 (ORR, confirmed ORR, best response 세부)
- Column: T-DXd (N=119), PC (N=56) — 평가 가능 환자 기준

#### 핵심 수치

- ORR: T-DXd 51% (42–61) vs. PC 14% (6–26)
- Complete response: T-DXd 9% (n=11) vs. PC 0%
- Partial response: T-DXd 42% (n=50) vs. PC 14% (n=8)
- Stable disease: T-DXd 35% (n=42) vs. PC 48% (n=27)
- Progressive disease: T-DXd 12% (n=14) vs. PC 30% (n=17)
- Confirmed ORR: T-DXd 43% (34–52) vs. PC 12% (5–24)
  - Confirmed CR: T-DXd 8% (n=10) vs. PC 0%
  - Confirmed PR: T-DXd 34% (n=41) vs. PC 12% (n=7)

#### 해석 시 주의점

- Table 2의 분모는 N=119(T-DXd), N=56(PC) — 전체 치료 환자(125, 62)와 다름. 평가 가능 환자 기준. 6명/6명은 독립 중앙 검토에서 측정 가능 병변 미확인.
- 해석: ORR 51%는 통계적으로 강한 증거(P<0.001). 단, confirmed CR 10명은 소규모로 내구성 평가 시 절대 수에 주의.

---

### Table 3 — 주요 이상반응 (Adverse Events ≥ 20%)

- **이 Table이 필요한 이유**: T-DXd의 임상 도입 시 주요 독성 프로파일(특히 골수억제, ILD)을 정량적으로 제시.
- **이 Table이 뒷받침하는 주장**: T-DXd는 유효하지만 고유 독성(골수억제, ILD)이 동반된다.

#### 핵심 수치

(§Safety, Table 3 참조)
- 오심: T-DXd 63%, PC 47% (Grade 3: 5%, 2%)
- 호중구감소증: T-DXd 63% (Grade 3: 38%, Grade 4: 13%) vs. PC 35% (16%, 8%)
- 식욕감소: T-DXd 60% (Grade 3: 17%) vs. PC 45% (13%)
- 빈혈: T-DXd 58% (Grade 3: 38%) vs. PC 31% (21%)
- 혈소판감소증: T-DXd 39% (Grade 3: 10%, Grade 4: 2%) vs. PC 6% (2%, 2%)
- 백혈구감소증: T-DXd 38% (Grade 3: 21%) vs. PC 35% (8%)
- 피로: T-DXd 22% (Grade 3: 7%) vs. PC 24% (3%)

#### 해석 시 주의점

- Grade 3/4 호중구감소증이 T-DXd에서 51%로 높음. 그러나 발열성 호중구감소증은 6명(5%)으로 상대적으로 낮아 관리 가능한 수준.
- 혈소판감소증: T-DXd 39% vs. PC 6% — 큰 차이. PC에서 이리노테칸이 주를 이루는데, 이리노테칸의 혈소판 독성은 T-DXd보다 낮음.
- ILD는 Table 3에 ≥20% 기준 미포함(10%)이나 임상적으로 중요한 T-DXd 특이 독성 — 별도 모니터링 필수.

---

## Supplementary Information

### Supplementary Methods (nejmoa2004413_appendix.pdf)

- **포함 기준(주요)**: HER2 IHC 3+ 또는 IHC 2+/ISH+; 위·GEJ 선암; trastuzumab 포함 2개 이상 이전 치료; ECOG PS 0–1; 측정 가능 병변(RECIST v1.1); 적절한 장기 기능.
- **제외 기준(주요)**: ILD/pneumonitis 병력 또는 영상에서 의심; glucocorticoid 치료력 있는 비감염성 ILD; 무작위화 전 4주 내 방사선치료; 다른 임상시험 참여 중.
- **안전성 평가**: CTCAE v5.0. 독립 ILD 판정 위원회(adjudication committee) 별도 운영.

### Supplementary Figures (nejmoa2004413_appendix.pdf)

- **Figure S1** — Study design 개요.
- **Figure S2** — Patient disposition flowchart: 스크리닝 → 무작위 → 치료 → 주요 중단 사유.
- **Figure S3** — Spider plot (시간에 따른 개별 환자 종양 부담 변화).
- **Figure S4** — Confirmed response의 KM 분석 (duration of response). T-DXd 중앙 11.3개월 vs. PC 3.9개월.
- **Figure S5** — ORR 서브그룹 분석 (forest plot): 지역, ECOG, HER2 상태, 나이, 성별 등.
- **Figure S6** — OS 서브그룹 분석 (forest plot).

### Supplementary Tables (nejmoa2004413_appendix.pdf)

- **Table S1** — Overall safety (모든 치료 관련 이상반응).
- **Table S2** — T-DXd에서 ≥10% 이상반응 상세.

---

## 분석 자체에 대한 메모

- 본 분석은 `sources/shitara-2020-destiny-gastric01.pdf` (본문 12 pages)와 `sources/nejmoa2004413_appendix.pdf` (17 pages)를 근거로 했다. Protocol(`nejmoa2004413_protocol.pdf`)는 보조 참조.
- PFS의 p-value가 본문에 명시되지 않음 — HR과 CI만 제시됨. 검토필요: Fig 2B caption 및 supp text에서 통계 검정 보충 확인 필요.
- ILD 12명의 grading이 adjudication committee 기반으로 조정됨 — 본문 grade 분포와 CTCAE 자가 보고 간 차이 있을 수 있음.
- 후속 치료 불균형(PC군 74% vs. T-DXd군 48%)이 OS 비교의 핵심 교란 요인이나, 이 시험이 intent-to-treat 기반 OS를 primary 추정 대상으로 설계한 것이 아니므로 통계 설계상 이 교란이 완전히 통제되지 않았음.
