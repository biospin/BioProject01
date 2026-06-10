## Executive Summary

- **무엇**: 유방암 원발암 조직 HER2 상태와 혈중 CTC HER2 상태 사이의 불일치율을 TBCD(telomerase 기반 CTC 검출법) + 항-HER2 항체로 정량화한 임상 관찰 연구. 주요 기여는 기존 조직 생검의 스냅샷 한계를 CTC 기반 real-time 재프로파일링으로 보완할 수 있다는 근거 제공.
- **모델 / 방법**: 4 ml 말초혈액 → RBC lysis → oHSV1-hTERTp-eGFP 바이러스 감염(MOI=1, 16–24 h) → anti-CD45/anti-HER2 이중 항체 염색 → flow cytometry. CTC = CD45⁻/GFP⁺, HER2+CTC = CD45⁻/GFP⁺/HER2⁺. 일치도 통계: kappa test, chi-square; 상관 분석: Spearman.
- **핵심 결과**:
  - ① 전체 불일치율 32.6% (14/43; kappa = 0.325, p = 0.030) — 조직 vs. CTC HER2 상태는 moderate concordance 미달.
  - ② hHER2⁻ 환자 중 HER2+CTC 검출률 32.1% (9/28) — 조직 음성군의 1/3에서 혈중 HER2 양성 CTC 존재.
  - ③ hHER2⁺ 환자 중 cHER2⁺ 검출률 66.7% (10/15) — 조직 양성이라도 CTC에서 HER2 소실 다수.
  - ④ HER2+CTC 수와 Ki67 index 양의 상관 (R=0.38, p=0.011); 총 CTC 수와 Ki67은 무상관 (R=0.026, p=0.87).
  - ⑤ ER/PR 음성군에서 HER2+CTC 수 유의하게 높음 (p=0.0132).
- **우리 적용**: CTC 기반 HER2 재프로파일링의 임상적 근거 논문 — ADC(T-DXd 등) 적용 확대 논리 및 CTC liquid biopsy 플랫폼 BD pitch 시 `academic-citation` + `BD-opportunity` 레퍼런스.
- **심층**: 한계·재현 ROI는 `xie-2024-her2-ctc-concordance_lens-academic.md` / `xie-2024-her2-ctc-concordance_lens-industry.md` / `xie-2024-her2-ctc-concordance_methodology-brief.md` 참고.

---

## Identity

- **Title**: Concordance of HER2 status between primary tumor and circulating tumor cells in breast cancer
- **Authors**: Peipei Xie, Xiaoli Zhang, Tianyi Liu (공동 1저자), Yuchun Song, Qi Zhang, Duo Wan, Shijia Wang, Shulian Wang, Wen Zhang
- **Year**: 2024 (published online 18 December 2024)
- **Venue**: *Discover Oncology* 15:760
- **DOI**: 10.1007/s12672-024-01663-0
- **PMID**: 39692928 | **PMCID**: PMC11655891
- **Citation key**: xie2024her2ctcconcordance
- **소속**: National Cancer Center / Cancer Hospital, Chinese Academy of Medical Sciences and Peking Union Medical College, Beijing
- **Funding**: Noncommunicable Chronic Diseases-National Science and Technology Major Project (No. 2023ZD0502200)
- **Open access**: CC BY-NC-ND 4.0

---

## Background

### 배경 스토리

- **문제의 출발점**: HER2는 PI3K/Akt, MAPK 경로를 통해 암세포 생존과 증식에 관여하는 trans-membrane tyrosine kinase receptor로, 유방암·위암 등에서 불량 예후 표지자이자 치료 표적이다. 현재 표준 지침(ASCO)은 IHC/FISH로 HER2 양성을 확인한 환자에게만 HER2 표적 치료를 권장한다.

- **선행 접근 A — 조직 IHC/FISH 검사**: 수술·침생검 샘플로 HER2 상태를 단일 시점에 확인하는 표준법. trastuzumab, pertuzumab, T-DM1, trastuzumab deruxtecan(T-DXd) 등 승인 약제의 적응증 기준이 됨.

- **A의 한계 1 — 소량 생검의 false-negative**: 작은 생검 샘플은 종양 내 이질성을 대표하지 못해 HER2 위음성이 발생할 수 있음. 이로 인해 혜택을 받을 수 있는 환자군이 치료에서 제외될 위험.

- **A의 한계 2 — 동적 변화 미반영**: Tarantino et al. (2024)에 따르면 신보조 치료 후 29.5% (319/1080) 유방암 환자에서 조직 HER2 발현이 변한다. HER2 음성 환자가 HER2 양성 환자보다 더 많이 변화 (32.3% vs. 21.3%, p < 0.001). 원발암-재발암 간 불일치율도 38.1% (Shi et al., 247명).

- **선행 접근 B — CTC 기반 HER2 검출**: Wang et al., Pestrin et al., De Gregorio et al. 등이 다양한 enrichment 기술(EpCAM 기반 CellSearch, 필터링 기반 microfluidic 등)로 CTC HER2 상태를 평가했으나, 방법 간 표준화 부재, EpCAM 음성 CTC 포착 어려움, 비용·복잡도 문제가 남아 있음.

- **B의 한계**: CTC는 혈액 내 극소수(수십억 배경 세포 중 수 개)라 민감도·특이도 확보가 어렵다. 특히 상피-중간엽 전이(EMT)를 겪은 EpCAM 음성 CTC는 EpCAM 기반 방법으로 검출 불가.

- **이 논문으로 이어지는 gap**: TBCD(oHSV1-hTERTp-eGFP 기반 telomerase 활성 의존 CTC 검출법)는 EpCAM에 독립적으로 활성 텔로미어 합성효소를 가진 암세포만 선택적으로 표지해 EMT CTC까지 포착 가능하다. 이 기술로 HER2+CTC를 동시 검출하고, 조직 HER2와 CTC HER2 사이의 불일치 규모를 체계적으로 정량화한 연구가 없었다.

### 기본 개념

- **HER2 (Human Epidermal Growth Factor Receptor 2)**: ERBB2 유전자 인코딩 trans-membrane tyrosine kinase. 종양에서 gene amplification 또는 protein overexpression 발생 시 항-HER2 치료 적응증. IHC score 0/1+/2+/3+, FISH amplification 여부로 판정.

- **CTC (Circulating Tumor Cells, 혈중 종양 세포)**: 원발암에서 이탈해 혈류로 진입한 생존 가능 종양 세포. 원발암·전이암의 표현형·유전형 정보를 실시간으로 반영하며, liquid biopsy의 핵심 타깃.

- **TBCD (Telomerase-Based CTC Detection)**: 텔로미어 합성효소 역전사효소(TERT)의 고활성을 이용해 oHSV1-hTERTp-eGFP 바이러스가 TERT⁺ 세포에만 GFP를 발현시킴. 약 90%의 종양 세포가 비정상적 텔로미어 활성을 보이므로 암세포 선택성이 높음. EMT 및 EpCAM 음성 CTC도 포착 가능.

- **Kappa 계수**: 두 분류 검사 간 일치도를 우연 보정 후 측정하는 통계. 0.21–0.40 = fair agreement, 0.41–0.60 = moderate agreement. kappa = 0.325는 fair agreement로 두 측정 간 실질적 불일치를 의미.

- **Ki67 index**: 세포 증식 마커. ≥14%를 high proliferation으로 정의 (Chen et al. 2022 기준).

### 이 논문의 필요성

- **핵심 이유**: 조직 HER2 결과가 실제 종양 전체의 HER2 상태를 과소평가할 가능성이 임상적으로 중요해졌다. 특히 T-DXd 등 ADC가 HER2-low 환자에서도 효과를 보이면서(DESTINY-Breast04), CTC HER2 재프로파일링이 치료 결정에 직접 영향을 줄 수 있는 시점.
- **기존 방법으로 부족했던 지점**: EpCAM 기반 방법은 EMT CTC 포착 실패. 기존 연구들은 방법 이질성이 커 비교 어려움. TBCD로 HER2+CTC를 동시 검출한 규모 있는 전향적 데이터 부재.
- **이 논문이 해결하려는 방향**: TBCD + 항-HER2 항체 조합의 기술적 타당성 검증(spike-in 실험) + 43명 유방암 코호트에서 조직-CTC HER2 불일치율 정량화 + HER2+CTC와 임상 파라미터(Ki67, ER/PR) 연관성 탐색.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 유방암 환자 말초혈액 4 ml에서 TBCD + 항-HER2 항체로 HER2+CTC를 검출하고, 동일 환자의 조직 HER2 결과와 일치도를 정량화.
- **입력**: 4 ml EDTA 말초혈액 (방사선 치료 전 수집), 원발암 조직 IHC/FISH 결과 (1년 이내).
- **출력**: (1) CTC 총 수 (CD45⁻/GFP⁺), (2) HER2+CTC 수 (CD45⁻/GFP⁺/HER2⁺), (3) 조직-CTC HER2 일치도 (kappa).
- **추정 대상**: 조직 HER2와 CTC HER2 간 fair/poor concordance 여부, HER2+CTC와 Ki67 상관.
- **중요한 hidden assumption**: TBCD의 TERT 선택성이 WBC contamination을 충분히 배제한다는 가정. 혈중 정상 세포 중 TERT⁺ WBC 소집단(CD45⁺/GFP⁺)이 관찰되었으나, CD45 음성 gate로 제외된다고 가정.

### 확률 / 통계학적 구조

- **Model family**: 관찰 연구 (단일 기관, 단면 비교). 확률 모델보다는 기술 통계 + 비모수 통계 중심.
- **Likelihood / objective**: 해당 없음 (통계 모델 없음). 검증 지표: kappa 계수 (조직 vs. CTC HER2 일치도), chi-square (범주 비교), Mann-Whitney U / Kruskal-Wallis (비모수 그룹 비교), Spearman $\rho$ (HER2+CTC 수 vs. Ki67 상관).
- **Prior / regularization**: 미제공. Bayesian framework 없음.
- **Latent variable / hidden state**: 없음.
- **Inference / optimization**: R 4.3.2, 양측 검정, p < 0.05 유의.
- **Noise, sparsity, uncertainty 처리**: CTC 수가 0인 환자 17명 제외 (60 → 43명). 다중 비교 보정(BH/Bonferroni) 미시행.

### 핵심 method insight

- **기존 방법의 한계**: CellSearch 등 EpCAM 기반 방법은 EMT를 겪어 EpCAM을 소실한 CTC를 놓침. 기술 플랫폼마다 민감도·특이도 차이가 커 연구 간 비교 어려움.
- **이 논문이 바꾼 가정**: EpCAM 발현이 아닌 TERT 활성(약 90% 종양 세포 양성)을 CTC 선택 기준으로 사용. 이론상 EpCAM 음성 CTC, 특히 EMT 상태 세포도 포착 가능.
- **새로 추가한 변수 또는 구조**: oHSV1-hTERTp-eGFP 바이러스를 살아있는 세포에 감염시켜 TERT 프로모터 활성을 GFP 발현으로 변환. 이어서 항-HER2(APC), 항-CD45(APC-Cy7) 이중 염색 + flow cytometry로 3중 gate(GFP⁺/CD45⁻/HER2⁺).
- **이 변화가 중요한 이유**: TERT 기반 선택은 이론상 EpCAM 의존 방법 대비 포착 범위가 넓고, 생존 가능 활성 종양 세포만 표지한다. Spike-in 실험에서 $r^2 = 0.9986$ (MCF7), $r^2 = 0.9963$ (T47D)의 선형 회수율 확인.

### 이전 방법과의 차이

- **Baseline**: CellSearch (EpCAM-기반 immunomagnetic separation + IHC/FISH), filtration-based microfluidic CTC assay.
- **공통점**: flow cytometry 또는 imaging으로 CTC 형태·표지 확인; 항-CD45 음성 gate.
- **차이점**: TBCD는 바이러스 감염 기반 TERT 활성 검출로 살아있는 활성 CTC만 선택 → EpCAM 독립. 하루(16–24 h) 배양 단계 필요.
- **차이가 크게 나타나는 조건**: EMT 상태 CTC 비중이 높은 aggressive tumor (TNBC, high Ki67) 또는 advanced-stage에서 EpCAM 기반 방법과 검출률 차이가 클 것으로 예상. 해석: 직접 비교 실험은 본 논문에 없음.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: Spike-in 실험 (MCF7, T47D; 5, 20, 100, 200 cells/4 ml PB in healthy donor blood), 임상 코호트 n=43.
- **Metric**: $r^2$ (spike-in 선형성), kappa (일치도), Spearman $\rho$ (Ki67 상관), Mann-Whitney U p-value (그룹 비교).
- **개선된 결과**: Spike-in $r^2$ = 0.9986–0.9963; 임상 CTC 검출률 71.7% (43/60). 기존 EpCAM 기반 방법 대비 직접 수치 비교는 제시하지 않음.
- **Ablation 근거**: 없음.
- **정성적 효과**: FlowSight (Amnis ImageStream MK II) 이미징으로 CTC 형태(WBC보다 크고 불규칙), GFP⁺/HER2⁺ 표현형을 시각적으로 확인.

### Method 관점의 한계

- **약한 assumption**: TERT⁺ WBC(CD45⁺/GFP⁺) 소집단이 존재함을 저자 스스로 확인. CD45 gate가 이를 완전 배제한다고 가정하나, CD45 발현이 낮은 WBC subset과 CTC의 혼재 가능성 배제 검증 부족.
- **구현 또는 학습상의 부담**: 16–24 h 바이러스 배양 과정 필요 → 당일 결과 불가. 바이러스 제조·보관 품질 관리 요구.
- **일반화가 불확실한 조건**: 단일 기관(중국 국립암센터), n=43의 소규모. 다중 비교 보정 미시행으로 Ki67, ER/PR 상관 분석 결과의 false positive 가능성 미통제.

---

## Results

### Dataset별 결과

#### Dataset 1 — Spike-in 기술 검증 (in vitro)
- **Dataset**: MCF7 (TERT⁺/HER2⁺), T47D (TERT⁺/HER2⁺) 세포주; 건강 공여자 말초혈액 4 ml에 5, 20, 100, 200 세포 첨가.
- **목적**: TBCD + 항-HER2 항체의 HER2+CTC 검출 선형성 및 회수율 검증.
- **사용한 데이터 규모**: 각 농도 4개 데이터 포인트 × 2 세포주. n 미제공(반복 횟수 명시 없음).
- **Baseline / 비교 대상**: 미제공 (다른 방법과의 비교 없음).
- **Metric / 평가 기준**: 선형 회귀 $r^2$.
- **주요 수치**: MCF7 $r^2 = 0.9986$ (회귀식 $y = 0.9069x - 3.486$), T47D $r^2 = 0.9963$ ($y = 0.9157x - 4.608$).
- **정성 결과**: 24 h 배양 후 MCF7/T47D에서 GFP 발현 확인. TERT⁺ WBC 소집단(CD45⁺/GFP⁺) 존재 확인; CD45⁻ gate로 배제.
- **논문 주장과의 연결**: 검출 방법의 기술적 타당성(선형성, 회수율) 근거.

#### Dataset 2 — 임상 코호트 (주 분석)
- **Dataset**: 중국 국립암센터 2022–2024년 유방암 환자. 초기 60명 스크리닝 → CTC≥1인 43명 최종 분석 (n=17 CTC 미검출로 제외).
- **목적**: 조직 HER2와 CTC HER2 간 일치도 정량화; HER2+CTC와 임상 파라미터 연관성.
- **사용한 데이터 규모**: n=43 (hHER2⁺ 15명, hHER2⁻ 28명). 중앙 나이 48세 (범위 27–69). 병기: II 16.3%, III 81.4%, IV 2.3%. Ki67 ≥14% 86.1%.
- **Baseline / 비교 대상**: 원발암 조직 IHC/FISH 결과 (ASCO 기준).
- **Metric / 평가 기준**: kappa 계수, chi-square p-value; Spearman $\rho$; Mann-Whitney U p-value.

**주요 수치:**

| 지표 | 값 |
|---|---|
| 전체 CTC 검출률 | 71.7% (43/60) |
| hHER2⁺에서 cHER2⁺ 검출률 | 66.7% (10/15) |
|  — IHC 3⁺ 환자 | 69.2% (9/13) |
|  — IHC 2⁺, FISH⁺ 환자 | 50.0% (1/2) |
| hHER2⁻에서 cHER2⁺ 검출률 | 32.1% (9/28) |
|  — IHC 2⁺, FISH⁻ | 16.7% (2/12) |
|  — IHC 1⁺ | 54.5% (6/11) |
|  — IHC 0 | 20.0% (1/5) |
| 전체 불일치율 | 32.6% (14/43) |
| Kappa 계수 | 0.325 (p = 0.030) |
| HER2+CTC vs. Ki67 Spearman $\rho$ | 0.38 (p = 0.011) |
| 총 CTC vs. Ki67 Spearman $\rho$ | 0.026 (p = 0.87) |
| cHER2⁺ vs. cHER2⁻ CTC 수 (Mann-Whitney) | p = 0.0387 |
| cHER2⁺ vs. cHER2⁻ Ki67 (Mann-Whitney) | p = 0.0106 |
| ER/PR⁻ vs. ER/PR⁺ HER2+CTC 수 | p = 0.0132 |

**Table 2 (2×2 혼동 행렬):**

|  | cHER2⁻ | cHER2⁺ | 합계 |
|---|---|---|---|
| hHER2⁻ | 19 | 9 | 28 |
| hHER2⁺ | 5 | 10 | 15 |
| 합계 | 24 | 19 | 43 |

- **CI 미제공**: kappa의 95% CI는 본문에 명시되지 않음.
- **다중 비교 보정**: 미시행.
- 해석: kappa 0.325는 fair agreement 구간으로, 조직 HER2와 CTC HER2가 임상 결정을 공유하기에는 불충분한 일치도. p = 0.030은 단측으로는 유의하나 small sample에서의 해석에 주의 필요.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: (1) 조직 HER2⁺라도 CTC에서 HER2 소실 빈번 (hHER2⁺ → cHER2⁻: 5/15). (2) 조직 HER2⁻ 환자의 약 1/3에서 cHER2⁺. (3) HER2+CTC는 Ki67 고발현, ER/PR 음성 표현형과 동반.
- **가장 중요한 수치**: 전체 불일치율 32.6% (kappa=0.325, p=0.030); hHER2⁻에서 cHER2⁺ 32.1%.
- **baseline 대비 차이**: 현재 임상 기준(조직 HER2만으로 표적치료 결정) 대비, CTC HER2 재프로파일링 시 32.6%의 환자에서 치료 결정이 달라질 수 있음을 시사.
- **결과 해석 시 주의점**: n=43 단일 기관 코호트. 다중 비교 보정 미시행. kappa CI 미제공. CTC 0인 17명 제외로 인한 selection bias 가능성.

---

## Figures

#### Figure 1
- **이 Figure가 필요한 이유**: TBCD + 항-HER2 항체 검출 프로토콜의 전체 흐름을 도식화해, 기술 재현성과 이해를 위한 시각적 참조 제공.
- **이 Figure가 뒷받침하는 주장**: 4 ml 말초혈액에서 HER2+CTC를 단계적으로 검출하는 방법이 체계적으로 구현 가능하다.

##### 패널별 설명
- **(단일 패널, 워크플로우 다이어그램)**: 환자 혈액 채취(4 ml EDTA) → RBC lysis → WBC+CTC 혼합물 → oHSV1-hTERTp-eGFP 바이러스 감염(MOI=1, 37°C/5% CO₂, 16–24 h) → 항-CD45/항-HER2 항체 염색 → flow cytometry. 출력: HER2+CTC (CD45⁻/GFP⁺/HER2⁺), HER2⁻CTC (CD45⁻/GFP⁺/HER2⁻), WBC (CD45⁺/GFP⁻) 3종 구분.

##### 본문에서 강조한 비교
- 비교 대상: 없음 (프로토콜 도식).
- 관찰된 차이: N/A.
- 이 차이가 의미하는 것: N/A.

##### 해석 시 주의점
- 프로토콜 도식이므로 실험 결과를 직접 증명하지는 않음. 배양 시간(16–24 h)이 turnaround time 제약 요소임을 명시적으로 드러냄.

---

#### Figure 2
- **이 Figure가 필요한 이유**: TBCD 기반 HER2+CTC 검출의 기술적 타당성을 세포주 데이터와 spike-in 실험으로 검증하기 위함. 임상 코호트 분석에 앞서 방법의 신뢰성을 확립하는 핵심 검증 Figure.
- **이 Figure가 뒷받침하는 주장**: 본 방법은 TERT⁺/HER2⁺ 세포를 선택적으로 검출하며, 첨가 세포 수와 검출 수 사이의 선형성이 높다.

##### 패널별 설명
- **a**: CCLE 데이터베이스에서 MCF7, T47D의 TERT 및 HER2 발현 수준 확인 (MCF7, T47D 모두 고발현; MDA-MB231, MDA-MB157은 HER2 저발현).
- **b**: MCF7, T47D에 대한 flow cytometry 항체 염색 결과. MCF7: TERT 96.8%, HER2 100%; T47D: TERT 99.3%, HER2 100% 양성.
- **c**: oHSV1-hTERTp-eGFP 감염 24 h 후 MCF7, T47D 세포에서 GFP 발현 확인 (200× 형광). 대조군 미감염 세포 대비 GFP 발현 명확.
- **d**: Spike-in 선형 회귀. MCF7 $r^2 = 0.9986$ ($y = 0.9069x - 3.486$), T47D $r^2 = 0.9963$ ($y = 0.9157x - 4.608$). Mean±SD 표시.
- **e**: FlowSight (Amnis ImageStream MK II) 이미징. HER2+CTC (CD45⁻/GFP⁺/HER2⁺), CTC (CD45⁻/GFP⁺), TERT+WBC (CD45⁺/GFP⁺), WBC (CD45⁺/GFP⁻) 4종의 밝기·GFP·HER2·CD45 채널 이미지. CTC는 WBC보다 크고 불규칙한 형태.

##### 본문에서 강조한 비교
- 비교 대상: TERT⁺ 세포(MCF7/T47D) vs. TERT⁻ 세포(MDA-MB231 등), WBC vs. CTC.
- 관찰된 차이: TERT⁺ 세포주에서만 GFP 유도 발현; WBC는 CD45⁺/GFP⁻ (TERT⁺ WBC 소집단 존재하나 CD45⁺).
- 이 차이가 의미하는 것: TERT 활성 기반 GFP 표지가 암세포 선택성을 제공. CD45⁻ gate로 WBC(TERT⁺ 포함) 배제 가능.

##### 해석 시 주의점
- Spike-in 실험에서 반복 횟수(replicate n) 미명시. $r^2$ 값은 높지만 신뢰구간 미제공.
- TERT⁺ WBC 소집단 존재는 잠재적 false positive 원인. 본 데이터에서 임상 샘플의 false positive rate 정량화 없음.

---

#### Figure 3
- **이 Figure가 필요한 이유**: 60명 스크리닝 → 43명 최종 분석 과정의 선택 흐름을 투명하게 보여 selection bias 가능성을 독자가 평가하도록 함.
- **이 Figure가 뒷받침하는 주장**: 분석 코호트 구성(hHER2⁺ 15명, hHER2⁻ 28명)의 적절성.

##### 패널별 설명
- **(단일 플로우차트)**: 60명 → CTC 미검출 17명 제외 → 43명 포함. hHER2⁺ n=15, hHER2⁻ n=28 분리.

##### 해석 시 주의점
- CTC 미검출 17명(28.3%)의 임상 특성이 포함군과 다를 경우 selection bias. 이 17명의 조직 HER2 분포 미제공.

---

#### Figure 4
- **이 Figure가 필요한 이유**: 임상 코호트에서 조직-CTC HER2 불일치 패턴 및 HER2+CTC와 임상 파라미터(Ki67, ER/PR) 연관성을 종합적으로 시각화.
- **이 Figure가 뒷받침하는 주장**: (1) CTC HER2와 조직 HER2 불일치 실재; (2) HER2+CTC가 고증식·ER/PR⁻ 표현형과 연관.

##### 패널별 설명
- **a**: 43명 각 환자(P1–P43)의 4 ml PB CTC 수 막대그래프. hHER2⁻와 hHER2⁺ 구분. HER2⁺CTC(빨간색)와 HER2⁻CTC(파란색) 누적 표시. 개별 환자 이질성 큼 (CTC 수 1–11 범위).
- **b (상)**: hHER2⁺ 환자군에서 cHER2⁺(~67%) vs. cHER2⁻(~33%) 비율; 하단: cHER2⁺ 환자군에서 hHER2⁺ vs. hHER2⁻ 비율 (~53% hHER2⁺, ~47% hHER2⁻).
- **c**: 총 CTC 수 vs. Ki67 산점도 + Spearman 상관 (R=0.026, p=0.87). 상관 없음.
- **d**: HER2⁺CTC 수 vs. Ki67 산점도 + Spearman 상관 (R=0.38, p=0.011). 약한 양의 상관.
- **e**: cHER2⁻ vs. cHER2⁺ 환자에서 총 CTC 수 박스플롯 (p=0.0387*).
- **f**: cHER2⁻ vs. cHER2⁺ 환자에서 Ki67 index 박스플롯 (p=0.0106*).
- **g**: ER/PR⁻ vs. ER/PR⁺ 환자에서 HER2⁺CTC 수 박스플롯 (p=0.0132*).

##### 본문에서 강조한 비교
- 비교 대상: hHER2 양음성 × cHER2 양음성 4개 그룹; cHER2 양음성 vs. Ki67/CTC 수; ER/PR 상태 vs. HER2+CTC 수.
- 관찰된 차이: HER2+CTC는 Ki67 고발현, CTC 수 多, ER/PR⁻와 동반.
- 이 차이가 의미하는 것: HER2+CTC가 단순 기술적 산물이 아니라 생물학적으로 더 aggressive한 종양 표현형과 연결됨을 시사.

##### 해석 시 주의점
- n이 작아 (cHER2⁺ n=19, cHER2⁻ n=24) 그룹 간 비교의 통계적 검정력 제한. 다중 비교 보정(e, f, g 합산) 미시행 → false positive 가능성.

---

## Tables

### Table 1 — 환자 임상 정보

- **이 Table이 필요한 이유**: 코호트 구성을 투명하게 제공해 독자가 선택 편향 또는 일반화 한계를 스스로 평가할 수 있도록.
- **이 Table이 뒷받침하는 주장**: 코호트는 advanced-stage (병기 III 81.4%) 위주의 중국인 유방암 환자.

#### 표 구조
- Row: 각 임상 특성 (연령, 종양 크기, 폐경 상태, TNM 병기, 조직 HER2, 호르몬 수용체, 분자형, Ki67)
- Column: All patients (N=43)

#### 핵심 수치
- 중앙 연령 48세 (27–69); 종양 크기 평균 2.6 cm
- 병기 III 35/43 (81.4%) — heavily advanced cohort
- 조직 HER2 3⁺: 13/43 (30.2%), 2⁺FISH⁻: 12/43 (27.9%), 1⁺: 11/43 (25.6%), 0: 5/43 (11.6%), 2⁺FISH⁺: 2/43 (4.7%)
- 분자형: Luminal B 72.1%, HER2⁺ 16.3%, TNBC 9.3%, Luminal A 2.3%
- Ki67 ≥14%: 37/43 (86.1%)

#### 해석 시 주의점
- 단일 기관 중국 환자. 병기 III 과다 대표 (81.4%). 서양·한국 코호트 외삽 시 주의. ER⁺ 비율 79.1%로 Luminal B 위주 코호트.

---

### Table 2 — 조직 HER2 vs. CTC HER2 혼동 행렬

- **이 Table이 필요한 이유**: 불일치율(32.6%)과 kappa 값(0.325)의 raw data 기반 제시. 논문의 핵심 통계.
- **이 Table이 뒷받침하는 주장**: 조직과 CTC 간 HER2 fair concordance — 임상 결정에 두 결과가 동일하게 쓰일 수 없음.

#### 표 구조
- Row: Histological HER2 (Negative/Positive)
- Column: CTC HER2 status (Negative/Positive)

#### 핵심 수치
- True concordant (hHER2⁻/cHER2⁻): 19명
- False positive CTC (hHER2⁻/cHER2⁺): 9명 — 임상적으로 ADC 가능 대상
- False negative CTC (hHER2⁺/cHER2⁻): 5명 — CTC에서 HER2 소실
- True concordant (hHER2⁺/cHER2⁺): 10명
- Kappa = 0.325 (p = 0.03); CI 미제공

#### 본문에서 강조한 비교
- 비교 대상: 조직 HER2⁻인데 CTC HER2⁺인 군(9명, 32.1%)
- 관찰된 차이: 이 환자들은 현재 ASCO 기준으로는 HER2 표적 치료 적응증 없으나 CTC 관점에서는 HER2 발현 확인됨
- 이 차이가 의미하는 것: CTC 재프로파일링이 ADC 적응 환자 풀 확장에 기여할 수 있음

#### 해석 시 주의점
- 2×2 행렬 n=43은 kappa 추정 불안정 위험. 95% CI가 0을 포함하지 않는지 확인 필요 (미제공). 해석: kappa 0.325의 SE ≈ 0.10 (추정), 95% CI 대략 0.13–0.52 — fair에서 moderate borderline.

---

## Supplementary Information

### Supplementary Table 1 — 환자별 HER2 상태 및 CTC 수 (n=43)

- 43명 각 환자(P1–P43)의 조직 HER2 IHC 점수, Ki67 index (%), 총 CTC 수, HER2⁺CTC 수, HER2⁻CTC 수를 개인 단위로 제공.
- 주요 확인 사항:
  - P1 (IHC 0, Ki67 50%): HER2⁺CTC 3개 — 조직 HER2⁰이나 CTC 전부 HER2⁺. 불일치의 극단적 사례.
  - P5 (IHC 3⁺, Ki67 20%): CTC 6개 모두 HER2⁻ — hHER2⁺에서 cHER2 완전 소실.
  - P9 (IHC 3⁺, Ki67 30%): CTC 11개 중 HER2⁺ 1, HER2⁻ 10 — hHER2⁺에서 대부분 소실.
  - P22 (IHC 2⁺FISH⁻, Ki67 80%): CTC 2개 모두 HER2⁺, Ki67 최고치 — 극고증식 표현형과 cHER2⁺ 동반.
  - IHC 1⁺ 환자 중 cHER2⁺ 비율(54.5%, 6/11)이 IHC 2⁺FISH⁻(16.7%)보다 높은 역설적 패턴 — 소표본 variation 또는 IHC 1⁺ subcategory 특성 반영 가능.
- 검토필요: IHC 1⁺군에서 cHER2⁺ 비율이 IHC 2⁺FISH⁻보다 높은 이유. 샘플 수가 각 11명, 12명으로 작아 우연 변이 가능성 높음.

---

## 분석 자체에 대한 메모

- **신뢰도 평가**: 주요 통계 수치는 본문, Table 2, Supplementary Table 1과 일치. kappa = 0.325, p = 0.030 확인. 그러나 kappa 95% CI와 다중 비교 보정은 본문에 없어 이를 분석 한계로 명시.
- **누락된 검증**: (1) CTC 미검출 환자(n=17) 임상 특성 미제공 → selection bias 평가 불가. (2) 조직 생검 시점과 혈액 채취 시점 간격(최대 1년)에 따른 HER2 상태 변화 통제 없음. (3) 다중 비교 보정 미시행 (Ki67, ER/PR 연관 분석).
- **재검토 항목**: IHC 1⁺ 환자에서 cHER2⁺ 비율(54.5%)이 IHC 2⁺FISH⁻(16.7%)보다 높은 이상 패턴. Supplementary Table 1에서 확인하면 IHC 1⁺ n=11 중 6명이 HER2⁺CTC — P10(IHC1⁺/Ki67 20%), P20(Ki67 50%), P23(Ki67 20%), P26(Ki67 60%), P32(Ki67 40%), P40(Ki67 10%). 이 중 Ki67 고발현이 많지 않아 단순 증식 효과로 설명 어려움.
