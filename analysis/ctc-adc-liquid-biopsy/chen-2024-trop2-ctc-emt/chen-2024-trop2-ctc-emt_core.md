# chen-2024-trop2-ctc-emt — Core Analysis

## Executive Summary

- **무엇**: TNBC (triple-negative breast cancer) CTC 검출에서 EMT 중 EpCAM 소실로 기존 CellSearch 계열 assay가 mesenchymal-type CTC를 놓치는 문제를 해결하기 위해, TROP2가 TNBC 조직·세포주·임상 CTC 세 단계 모두에서 고발현되고 EMT를 기능적으로 촉진하는 새로운 CTC marker임을 제안한 translational biology paper.
- **모델 / 방법**: bioinformatics (TCGA/GTEx/CPTAC) + in vitro 기능 실험 (과발현/shRNA knockdown, wound healing, transwell, western blot) + 임상 혈액 샘플 (CanPatrol CTC assay, RNA-ISH, spiking assay, n=39). 통계: Student's t-test, one-way ANOVA, Spearman 상관분석.
- **핵심 결과**:
  - ① TCGA+GTEx — *TACSTD2* transcription이 정상 유방조직 대비 TNBC에서 유의하게 높음 (p < 0.001); Kaplan-Meier HR = 5.333, p = 0.042
  - ② IHC (TNBC 60례) — pT·pN 스테이지와 TROP2 IHC score 양의 상관 (p < 0.001)
  - ③ Cell line 기능 실험 — TROP2 과발현 시 vimentin, cyclinD1, c-myc, sox2 상승; knockdown 시 감소; migration/invasion 동방향 변화 (p < 0.05~0.001)
  - ④ Spiking assay — CK 단독 recovery 19.3~29.6%; CK+TROP2 이중 양성 16.9~30.2% (MDA-MB468/453/231)
  - ⑤ CanPatrol 임상 39례 — TNBC CTC에서 TROP2 signal이 Luminal/HER2+ 대비 유의하게 높음; TROP2 vs. vimentin $R^2 = 0.2522$, p < 0.0001
- **우리 적용**: TROP2를 EpCAM/CK 기반 liquid biopsy panel에 추가 marker로 검토할 근거 논문. `academic-citation` + `commercialization-candidate` 용도.
- **심층**: 한계·재현 ROI는 `chen-2024-trop2-ctc-emt_lens-academic.md` / `chen-2024-trop2-ctc-emt_lens-industry.md` / `chen-2024-trop2-ctc-emt_methodology-brief.md` 참고.

---

## Identity

- **Title**: TROP2 is highly expressed in triple-negative breast cancer CTCs and is a potential marker for epithelial mesenchymal CTCs
- **Authors**: Qingyu Liao†, Ruiming Zhang†, Zuli Ou†, Yan Ye, Qian Zeng, Yange Wang, Anqi Wang, Tingmei Chen, Chengsen Chai, Bianqin Guo (†공동 1저자)
- **교신저자**: Chengsen Chai (chengsenchai@cqmu.edu.cn), Bianqin Guo (guobianqin121@cqu.edu.cn)
- **Year**: 2024
- **Venue**: Molecular Therapy: Oncology, Vol. 32, March 2024
- **DOI**: 10.1016/j.omton.2024.200762
- **Citation key**: `@liao2024trop2ctc`
- **소속**: Key Laboratory of Clinical Laboratory Diagnostics (Ministry of Education), Chongqing Medical University; Chongqing University Cancer Hospital; CAS Key Laboratory for Biomedical Effects of Nanomaterials and Nanosafety / National Center for Nanoscience and Technology, Beijing
- **Open access**: CC BY-NC-ND 4.0
- **Funding**: Chongqing Municipal Education Commission (HZ2021006), Natural Science Foundation of Chongqing (CSTB2023NSCQ-MSX0845, CSTC2021JCYJ-MSXMX1221), Chongqing Talents Program (CQYC20210309587)

---

## Background

#### 배경 스토리

- **문제의 출발점**: CTC (circulating tumor cell, 순환 종양 세포)는 원발 종양에서 혈액으로 탈락한 세포로 전이의 씨앗이자 real-time liquid biopsy 대상이다. CTCs는 이미 여러 임상 시험에서 BC 환자의 예후와 치료 반응 예측에 독립적 가치를 보였다.
- **선행 접근 A — EpCAM 기반 enrichment**: CellSearch (FDA cleared)가 EpCAM 항체 기반으로 CTC를 농축하는 표준 방법으로, 임상 예후 데이터도 풍부하다.
- **A의 한계**: EMT (epithelial-mesenchymal transition) 진행 중 EpCAM이 downregulation되어 mesenchymal-type CTC는 CellSearch로 포착되지 않는다. TNBC는 유방암 서브타입 중 EMT 활성이 가장 높고, 예후가 가장 불량하며, early recurrence와 visceral metastasis 비율이 높다. 따라서 TNBC에서 mesenchymal CTC 미검출 문제가 가장 심각하다.
- **선행 접근 B — 대안 EMT-CTC marker 탐색 (vimentin, N-cadherin, Twist 등)**: 여러 연구가 mesenchymal marker를 CTC assay에 추가하려 시도했으나, TNBC에서 specificity와 임상 검증이 부족한 상태다.
- **B의 한계**: 기존 mesenchymal marker는 stromal 세포 오염, tumor specificity 부족, 임상 샘플 규모 검증 미흡 문제가 잔존한다.
- **이 논문으로 이어지는 gap**: TNBC 특이적으로 고발현되면서 EMT를 *촉진*하고, 기존 CTC assay에 추가 가능하며, 이미 FDA 승인 치료 표적인 단일 단백질 marker가 없다. TROP2는 EpCAM과 같은 *TACSTD* 유전자 패밀리로, TNBC 치료 ADC sacituzumab govitecan (Trodelvy)의 표적이다. 저자들은 TROP2가 TNBC CTC에서 고발현되고 EMT-CTC를 포착하는 데 활용될 수 있다는 가설을 세웠다.

#### 기본 개념

- **TROP2 (TACSTD2)**: trophoblast cell-surface antigen 2. calcium-transducing transmembrane glycoprotein. 정상 조직에서는 발현이 낮고 다수 악성 종양에서 과발현된다. EpCAM (*TACSTD1*)과 같은 유전자 패밀리. TNBC 치료 ADC sacituzumab govitecan (Trodelvy)의 표적이기도 하다.
- **EMT (epithelial-mesenchymal transition)**: 상피세포가 간엽세포 특성을 획득하는 과정. EpCAM, CK (cytokeratin) 등 epithelial marker가 감소하고 vimentin, N-cadherin 등 mesenchymal marker가 증가한다. 암 전이 및 화학요법 저항성과 연관된다.
- **CTC 이질성**: 같은 환자 혈액에도 epithelial CTC (E-CTC), hybrid epithelial-mesenchymal CTC (H-CTC), TROP2 양성 CTC (T-CTC) 등 여러 표현형이 공존한다.
- **CanPatrol CTC assay**: RNA-ISH (RNA in situ hybridization) 기반 플랫폼 (Surexam, Guangzhou). 10 mL 혈액 음성 농축 후 CK8/18/19 (epithelial), vimentin/Twist (mesenchymal), TROP2 mRNA를 다중 검출하여 E-CTC/H-CTC/T-CTC로 분류한다.
- **Spiking assay**: 건강 공여자 혈액에 알려진 수의 종양세포주를 첨가해 CTC 회수율(recovery)을 측정하는 검증 방법.

#### 이 논문의 필요성

- **핵심 이유**: TNBC는 EpCAM 기반 CTC 검출의 가장 취약한 서브타입인 동시에 실시간 모니터링 필요성이 가장 크다.
- **기존 방법으로 부족했던 지점**: EpCAM 의존 assay는 mesenchymal CTC를 구조적으로 놓친다. TNBC 특이적 대안 marker의 임상 검증이 부족하다.
- **이 논문이 해결하려는 방향**: TROP2가 TNBC 조직/세포주/CTC에서 고발현되고 EMT를 기능적으로 촉진하며, 기존 CK 기반 marker와 결합하면 TNBC CTC 검출률을 높일 수 있는지를 세포주 + 임상 혈액 샘플로 검증한다.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: TROP2의 TNBC CTC marker 유효성 평가 — (1) TNBC 조직/세포주에서의 발현 특성, (2) TROP2의 EMT 촉진 기능 확인, (3) 혈액 CTC에서의 검출 가능성 검증.
- **입력**: TCGA/GTEx RNA-seq 공개 데이터, CPTAC 단백체 데이터, TNBC 임상 조직 (n=60), BC 세포주 7종 (MCF-10A, MCF-7, SK-BR3, MDA-MB231/453/468, BT549), 임상 혈액 샘플 (n=39).
- **출력**: TROP2 발현 수준 (transcript/protein), EMT marker 연동 여부, spiking recovery 수치, 임상 CTC TROP2 signal.
- **중요한 hidden assumption**: CanPatrol RNA-ISH의 TROP2 mRNA signal이 단백질 발현과 일치한다고 전제. 임상 cohort는 Chongqing University Cancer Hospital 단일 기관.

#### 확률 / 통계학적 구조

- **통계 검정**: Student's t-test (2그룹 비교), one-way ANOVA (다그룹 비교). 소프트웨어: GraphPad Prism 9. 유의 기준 p < 0.05.
- **상관 분석**: Spearman's rank correlation. R 버전 4.0.3 (`ssgsea` parameter).
  - Figure 3A — TACSTD2 vs. EMT markers: p = 0.013, Spearman r = 0.20
  - Figure 3A — TACSTD2 vs. TGF-β: p = 1.61×10⁻⁴, r = 0.29
  - Figure 5D — TROP2 vs. vimentin (임상 CTC): $R^2 = 0.2522$, p < 0.0001
  - Figure S3 — TROP2 vs. vimentin (세포주 RNA-ISH): MDA-MB231 $R^2 = 0.06052$, p = 0.0146; MDA-MB453 $R^2 = 0.009$, p = 0.2305 (비유의); MDA-MB468 $R^2 = 0.1234$, p < 0.0001
- **Kaplan-Meier**: TCGA TNBC. *TACSTD2* 고발현 vs. 저발현군 OS 비교. HR = 5.333, p = 0.042.
- **결과 표현**: mean ± SD. 독립 반복 실험 최소 3회.
- **Multiple testing correction**: 미제공. 다중 비교 보정 명시 없음.
- **CI / effect size**: 본문 미제공.

#### 핵심 method insight

- **기존 방법의 한계**: EpCAM 기반 CTC enrichment는 EMT-high 세포를 구조적으로 놓친다. 대안 mesenchymal marker는 tumor specificity 부족.
- **이 논문이 바꾼 가정**: TROP2가 단순히 EMT 중에 살아남는 passive marker가 아니라 EMT를 *능동적으로 촉진*한다. 동시에 EpCAM 패밀리 단백질로서 EpCAM-음성 EMT CTC에서도 발현이 유지될 수 있다.
- **새로 추가한 구조**: 기존 CK + vimentin 이중 marker 체계에 TROP2를 세 번째 축으로 추가. T-CTC (TROP2 양성 CTC) 서브타입을 새로 정의.
- **이 변화가 중요한 이유**: TROP2는 이미 FDA 승인 ADC (sacituzumab govitecan)의 표적이므로, therapeutic target과 liquid biopsy biomarker가 동일 분자인 companion Dx 가능성을 열어준다.

#### 이전 방법과의 차이

- **Baseline**: EpCAM/CK 기반 CellSearch; CanPatrol의 CK+vimentin 이중 marker 분류.
- **공통점**: 음성 농축 전략, 형광 면역 표지 후 자동화 현미경 스캔.
- **차이점**: TROP2 RNA-ISH probe를 추가하여 T-CTC (TROP2 양성 CTC) 서브타입 정의. 특히 EMT-CTC에서 TROP2 발현 증가를 exploiting함.
- **차이가 크게 나타나는 조건**: TNBC 환자, hybrid EMT CTC 비율이 높은 경우.

#### 효과가 Results에서 나타난 방식

- **Spiking assay**: CK 단독 recovery (MDA-MB468/453/231): 19.3%, 29.6%, 25.6%. CK+TROP2 이중 양성 recovery: 16.9%, 30.2%, 25.3%. 두 수치가 유사하거나 소폭 높음.
- **CanPatrol 임상 39례**: TNBC에서 TROP2 signal이 Luminal 대비 p < 0.05, HER2+ 대비 p < 0.001 높음.
- **정성 효과**: Epithelial CTC → EMT-TROP2-high CTC로 갈수록 TROP2 발현이 vimentin과 비례하여 증가.

#### Method 관점의 한계

- **약한 assumption**: MDA-MB453에서 TROP2-vimentin 상관 비유의 ($R^2 = 0.009$, p = 0.2305). 세포주 간 일관성 불완전.
- **구현 부담**: CanPatrol assay는 상용 플랫폼 (Surexam). RNA-ISH probe 서열은 Table S2에 공개되어 있으나 assay 재현을 위해 플랫폼 라이선스 필요.
- **일반화 불확실**: 임상 cohort 단일 기관 소규모 (n=39, TNBC n=11). 다중 비교 보정 미적용.

---

## Results

#### Dataset별 결과

##### Dataset 1 — TCGA + GTEx bioinformatics

- **Dataset**: TCGA RNA-seq + GTEx 정상 조직, RNAseqDB 통합 데이터 (Wang 2018, Sci. Data 5:180061). BC subtype: Luminal/HER2+/TNBC vs. adjacent normal.
- **목적**: TROP2 (*TACSTD2*) 발현이 정상 대비 TNBC에서 유의하게 높고 subtype 간 차이가 있음을 확인.
- **사용한 데이터 규모**: Figure 1B (CPTAC 단백체): Normal n=18, Luminal n=64, HER2+ n=64, TNBC n=10.
- **주요 수치**: *TACSTD2* transcription, 정상 대비 세 BC subtype 모두 유의하게 높음 (p < 0.001, Figure 1A). CPTAC 단백 Z-value: TNBC median이 가장 높음 (Figure 1B).
- **논문 주장과의 연결**: TROP2 고발현이 TNBC 특이적이며 CTC marker 가설의 생물학적 근거.

##### Dataset 2 — IHC (임상 TNBC 조직, n=60)

- **Dataset**: Chongqing University Cancer Hospital 유래 TNBC 조직 절편, n=60 (4 μm IHC, H-score).
- **목적**: TROP2 단백 발현과 TNM 스테이징의 상관 확인.
- **주요 수치 (Figure 1D)**:
  - pT stage: T0 vs. T2 p < 0.001; T0 vs. T4 p < 0.01; T1 vs. T4 p < 0.05
  - pN stage: N0 vs. N2 p < 0.001; N0 vs. N3 p < 0.001
  - Kaplan-Meier: HR = 5.333, p = 0.042 (TACSTD2 고발현군 OS 불량)
- **논문 주장과의 연결**: TROP2가 TNM 스테이지 진행과 양의 상관이 있고, 고발현군 OS 불량.

##### Dataset 3 — BC 세포주 기능 실험

- **Dataset**: MCF-10A, MCF-7, SK-BR3, MDA-MB231/453/468, BT549; lentivirus 과발현 (BT549) 및 shRNA knockdown (MDA-MB231).
- **목적**: TROP2의 EMT 촉진 기능 및 migration/invasion 효과 확인.
- **qRT-PCR 주요 수치 (Figure 2C)**:
  - BT549 TROP2 OE → vimentin p < 0.001, cyclinD1 p < 0.01, c-myc p < 0.01, sox2 p < 0.01 상승
  - MDA-MB231 shRNA → vimentin p < 0.05, sox2 p < 0.05~0.01 감소
- **Western blot (Figure 3B)**: TROP2 OE → N-cadherin, vimentin 단백 증가; knockdown → 감소.
- **Wound healing (Figure 3C, D)**:
  - BT549 OE: 48h 상대 면적 유의 증가 (p < 0.05)
  - MDA-MB231 sh: 48h 유의 감소 (p < 0.05~0.001)
- **Transwell (Figure 3E, F)**:
  - BT549 OE: migration p < 0.01, invasion p < 0.001 증가
  - MDA-MB231 sh: migration p < 0.05~0.001, invasion p < 0.05~0.01 감소
- **논문 주장과의 연결**: TROP2 과발현/knockdown이 대칭적으로 EMT marker 및 이동/침윤 능력을 변화시킨다.

##### Dataset 4 — Flow cytometry & IF (세포주 + PBMCs)

- **Dataset**: MDA-MB468, MDA-MB453, MDA-MB231, MCF-10A, 건강 공여자 PBMCs.
- **목적**: TROP2가 TNBC 세포 특이적이고 정상 혈액 세포에서 발현이 낮음을 확인.
- **주요 결과**: Flow cytometry (Figure 4A) — TNBC 세포주에서 TROP2-PE 양성 비율 높음; MCF-10A에서 낮음. Western blot (Figure S2) — MCF-10A, PBMC에서 TROP2 단백 거의 없음.
- **정확한 수치**: Figure 4A bar graph (정확한 %값은 본문 미제공 — 시각 데이터만).
- **논문 주장과의 연결**: TROP2의 TNBC specificity 확인 및 false positive (PBMC) 배제 근거.

##### Dataset 5 — Spiking assay (5 mL 건강인 혈액 + 2,000 세포)

- **Dataset**: MDA-MB468, MDA-MB453, MDA-MB231 각 2,000개를 건강 공여자 5 mL 혈액에 첨가. 음성 농축 후 IF (phycoerythrin anti-TROP2 + fluorescein isothiocyanate anti-CK8/18/19) → 자동화 형광 현미경.
- **목적**: TROP2를 CTC assay에 추가했을 때 회수율 확인.
- **주요 수치 (Figure 4D)**:
  - CK 단독 recovery: MDA-MB468 19.3%, MDA-MB453 29.6%, MDA-MB231 25.6%
  - CK+TROP2 이중 양성 recovery: MDA-MB468 16.9%, MDA-MB453 30.2%, MDA-MB231 25.3%
- **해석**: CK+TROP2 이중 양성 회수율이 CK 단독과 유사하게 유지됨 — TROP2가 CK 양성 세포에서도 동시 발현됨을 확인. TROP2 단독 (CK-음성 TROP2-양성) recovery 수치는 본문 미제공.

##### Dataset 6 — CanPatrol CTC assay (임상 혈액 39례)

- **Dataset**: Chongqing University Cancer Hospital 혈액 39례 — Luminal n=15, HER2+ n=13, TNBC n=11 (Figure S4 기준).
- **목적**: 환자 혈액 CTC에서 TROP2 발현이 TNBC 특이적으로 높고, EMT marker와 상관관계가 있음을 확인.
- **Metric**: RNA-ISH positive signal intensity, CTC count/5 mL.
- **주요 수치**:
  - TNBC CTC TROP2 signal: Luminal 대비 p < 0.05, HER2+ 대비 p < 0.001 높음 (Figure 5C)
  - TROP2 vs. vimentin 상관: $R^2 = 0.2522$, p < 0.0001 (Figure 5D)
  - Epithelial CTC → EMT-TROP2-high CTC: TROP2 발현이 vimentin 증가와 비례하여 상승 (Figure 5D)
- **논문 주장과의 연결**: TROP2가 임상 TNBC CTC에서 EMT 정도와 비례하여 발현되며, mesenchymal-associated CTC 포착 가능성을 임상 데이터로 지지.

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: TROP2는 TNBC 조직·세포주·임상 혈액 CTC 세 단계 모두에서 다른 BC subtype 대비 일관되게 높게 발현됨. TROP2 과발현은 EMT marker 상승과 migration/invasion 증가를 동반함.
- **가장 중요한 수치**: TROP2 vs. vimentin $R^2 = 0.2522$, p < 0.0001 (임상 CTC); Kaplan-Meier HR = 5.333, p = 0.042 (TCGA TNBC).
- **baseline 대비 차이**: CK 단독 spiking recovery와 CK+TROP2 이중 양성 recovery가 유사 수준 — TROP2가 CK 양성 세포에서 동시 발현. CK-음성 TROP2-양성 CTC (진짜 EMT-CTC 추가 포착)의 정량적 수치는 본문 미제공.
- **결과 해석 시 주의점**: 임상 cohort n=39 (TNBC n=11) 소규모 단일 기관. Multiple testing correction 미적용. TROP2 단독 EMT-CTC 회수율의 명시적 수치 부재.

---

## Figures

#### Figure 1 — TROP2 is highly expressed in TNBC and is related to poor prognosis

- **이 Figure가 필요한 이유**: TROP2를 TNBC CTC marker로 제안하기 전에, TROP2가 TNBC 조직에서 고발현되고 임상 악성도 및 불량 예후와 연결됨을 다단계 증거로 정당화해야 한다.
- **이 Figure가 뒷받침하는 주장**: TROP2는 TNBC에서 특이적으로 높고, TNM 스테이지 및 예후와 양의 상관이 있다.

##### 패널별 설명
- **a**: TCGA+GTEx violin plot. *TACSTD2* (log2 TPM+1), Tumor(red) vs. Normal(blue). BC 세 subtype 모두 정상 대비 p < 0.001.
- **b**: CPTAC 단백체 box plot. Normal/Luminal/HER2+/TNBC (Z-value). TNBC (n=10)가 가장 높은 median.
- **c**: IHC 병리 조직 이미지. Luminal/HER2+/TNBC. TNBC에서 DAB 염색 강도와 범위 가장 크다. Scale bar: 긴 것 625 μm, 짧은 것 100 μm.
- **d**: IHC H-score vs. pT/pN stage scatter. pT: T0 vs. T2 p < 0.001; T0 vs. T4 p < 0.01. pN: N0 vs. N2/N3 p < 0.001.
- **e**: Kaplan-Meier OS. TACSTD2 고발현 vs. 저발현. HR = 5.333, p = 0.042.

##### 본문에서 강조한 비교
- TNBC vs. 다른 BC subtype: CPTAC 단백 Z-value TNBC가 최고 (Figure 1B).
- pT/pN stage 진행에 따른 IHC score 증가: 악성도-발현 양의 상관.

##### 해석 시 주의점
- CPTAC TNBC n=10 소규모. KM p = 0.042는 단일 유전자 기준으로 multiple testing 미보정 시 경계값.

---

#### Figure 2 — TROP2 expression affects the expression of tumor progression markers

- **이 Figure가 필요한 이유**: TROP2가 단순히 TNBC에서 높은 것을 넘어, EMT 및 세포 증식 marker를 기능적으로 조절함을 보여 CTC marker 이상의 생물학적 relevance를 확인.
- **이 Figure가 뒷받침하는 주장**: TROP2 조작(과발현/knockdown)이 vimentin, cyclinD1, c-myc, sox2 발현을 변화시킨다.

##### 패널별 설명
- **a**: qRT-PCR bar. BC 세포주 7종 상대 TROP2 발현. MDA-MB468, MDA-MB231에서 높음; MCF-10A에서 낮음.
- **b**: BT549 lentivirus 과발현 (OEV, OE); MDA-MB231 shRNA (sh-1, sh-2) vs. NC. 각각 TROP2 mRNA 확인. OE에서 ~130~350배 증가; sh에서 ~0.1~0.2배로 감소. (**p < 0.01)
- **c**: TROP2 과발현/knockdown 후 EMT·stemness marker 변화. BT549 OE: vimentin p < 0.001, cyclinD1/c-myc/sox2 p < 0.01. MDA-MB231 sh: vimentin, sox2 등 감소.

##### 본문에서 강조한 비교
- TROP2 OE → vimentin 가장 유의한 상승 (p < 0.001): EMT 연동의 핵심.
- knockdown과 OE가 대칭적 방향: 단순 상관이 아닌 기능적 조절 주장의 근거.

##### 해석 시 주의점
- c-myc, cyclinD1, sox2의 변화가 TROP2 직접 전사 조절인지 EMT 하류 간접 효과인지 인과 구분 미제공.

---

#### Figure 3 — TROP2 promotes invasion by upregulating mesenchymal markers in TNBC cells

- **이 Figure가 필요한 이유**: TROP2-EMT 연관이 발현 수준을 넘어 migration·invasion이라는 기능적 결과로 이어짐을 보여 mechanistic link 확립.
- **이 Figure가 뒷받침하는 주장**: TROP2는 TGF-β EMT 경로와 양의 상관이 있고, 과발현 시 N-cadherin/vimentin 상승과 세포 이동/침윤 증가가 동반된다.

##### 패널별 설명
- **a**: Spearman 상관 scatter (TCGA). TACSTD2 vs. EMT markers: p = 0.013, r = 0.20. TACSTD2 vs. TGF-β: p = 1.61×10⁻⁴, r = 0.29.
- **b**: Western blot. BT549 OE: N-cadherin, vimentin 단백 증가. MDA-MB231 sh: 감소. GAPDH loading control.
- **c, d**: Wound healing assay (0/24/48h). BT549 OE 48h 상대 면적 유의 증가 (p < 0.05). MDA-MB231 sh 48h 유의 감소 (p < 0.05~0.001).
- **e, f**: Transwell migration/invasion. BT549 OE: migration p < 0.01, invasion p < 0.001 증가. MDA-MB231 sh: migration/invasion 유의 감소.

##### 본문에서 강조한 비교
- OE vs. knockdown의 대칭적 효과: TROP2 기능 주장의 핵심 근거.
- TGF-β 상관은 pathway 연결 시사이지만 직접 TGF-β 차단 실험은 미제공.

##### 해석 시 주의점
- Spearman r = 0.20~0.29는 통계 유의하나 상관 강도가 낮음. 인과 주장에는 경로 개입 실험 필요.
- Transwell invasion assay: 200 μL Matrigel (1:8 희석) 코팅 사용. Migration assay는 Matrigel 없음.

---

#### Figure 4 — Expression of TROP2 in TNBC cells and blood cells

- **이 Figure가 필요한 이유**: TROP2가 TNBC 세포 특이적이고 PBMCs에서 발현이 낮아 CTC marker specificity를 확인하고, 실제 혈액 spiking에서 회수 가능성을 검증.
- **이 Figure가 뒷받침하는 주장**: TROP2는 TNBC cell-specific이고 정상 혈액 세포에서 발현이 낮다.

##### 패널별 설명
- **a**: Flow cytometry histogram. MDA-MB468/453/231, MCF-10A. TROP2-PE 및 EpCAM-FITC. TNBC 세포주에서 TROP2 양성 비율 높음; MCF-10A 낮음.
- **b**: IF. MDA-MB468/453/231, MCF-10A. EpCAM(green), TROP2(orange), merge. TNBC에서 TROP2 신호 강함. MFI bar chart 제공.
- **c**: PBMC IF. DAPI/CK/TROP2/CD45/Bright Field. PBMC (177A, 012A)에서 TROP2 = 0~1 (거의 없음). CD45 양성 확인.
- **d**: Spiking assay IF. MDA-MB468/453/231 각 세포군. CK(green), TROP2(red). Recovery 수치: CK 단독 19.3/29.6/25.6%; CK+TROP2 이중 양성 16.9/30.2/25.3%.

##### 본문에서 강조한 비교
- PBMC TROP2 ≈ 0 vs. TNBC 세포주 TROP2 높음: false positive 배제.
- CK+TROP2 이중 양성 ≈ CK 단독 recovery: TROP2가 CK 양성 세포에서 동시 발현.

##### 해석 시 주의점
- Spiking n=2,000 cells/5 mL는 실제 환자 CTC 농도보다 수십~수백 배 높음. 임상 sensitivity 과대 추정 가능성.
- TROP2 단독 (CK-음성) recovery 수치 미제공 — EMT-CTC 추가 포착률의 핵심 결과 누락.

---

#### Figure 5 — High expression of TROP2 in TNBC CTCs and its potential for detecting mesenchymal-associated CTCs

- **이 Figure가 필요한 이유**: 세포주 데이터를 임상 혈액으로 확장하여, 실제 TNBC 환자 CTC에서 TROP2가 EMT 정도와 상관관계를 보임을 입증.
- **이 Figure가 뒷받침하는 주장**: 임상 TNBC CTC에서 TROP2가 TNBC 특이적으로 높고 EMT 수준과 비례한다.

##### 패널별 설명
- **a**: CanPatrol assay 플로우차트. 10 mL 혈액 → RBC lysis → nanotechnology 기반 음성 농축 → RNA-ISH → 형광 현미경 스캔.
- **b**: RNA-ISH bar. MDA-MB231/453/468 세포주. TROP2, vimentin signal intensity. MDA-MB468에서 TROP2 신호 최고.
- **c**: 임상 39례 CTC. 상단: 전형 케이스 이미지 (Luminal P2997, HER2+ P4187, TNBC P3030). 하단 scatter: TROP2 signal — TNBC > Luminal p < 0.05; TNBC > HER2+ p < 0.001.
- **d**: TROP2 vs. vimentin scatter plot (임상 CTC). $R^2 = 0.2522$, p < 0.0001. 세 CTC 타입: Epithelial CTC (TROP2 낮음/CK 높음/VIM 낮음), EMT-TROP2-low, EMT-TROP2-high (TROP2 높음/CK 낮음/VIM 높음).

##### 본문에서 강조한 비교
- TNBC vs. Luminal/HER2+: TROP2 signal 유의하게 높음.
- E-CTC → EMT-TROP2-high CTC: TROP2 발현이 EMT 정도에 비례하여 증가 (Figure 5D 핵심 관찰).

##### 해석 시 주의점
- TNBC n=11 소규모. Figure 5C scatter에서 outlier 존재.
- $R^2 = 0.2522$: 양의 상관 유의하지만 분산의 25%만 설명. 잔여 75%는 다른 요인.
- CTC count/5 mL에서 TNBC vs. 다른 subtype 간 통계 검정 결과는 본문 미명시.

---

## Tables

본문에 정식 Table 없음. 수치 데이터는 모두 Figure 형태로 제시.

---

## Supplementary Information

#### Table S1 — Primer sequences (qRT-PCR)

β-actin, TROP2, vimentin, c-myc, cyclinD1, sox2 각 forward/reverse primer 서열 (20~22 nt). 재현에 필수.

#### Table S2 — RNA-ISH probe sequences for TROP2

TROP2 mRNA 검출용 probe 4개 (5'→3', 각 ~40 nt). CanPatrol assay 재현에 필수.

#### Figure S1 — Spiking assay flowchart

세포 소화·재현탁·계수 → EasySep Direct Human CTC Enrichment Kit (음성 농축) → ICC (phycoerythrin anti-TROP2 + FITC anti-CK8/18/19) → 자동화 형광 현미경.

#### Figure S2 — TROP2 Western blot in MCF-10A and PBMCs

MCF-10A와 PBMC에서 TROP2 단백 발현 거의 없음. GAPDH 대조. TROP2의 정상 혈액 세포 specificity 보강 근거.

#### Figure S3 — TROP2-vimentin 상관 (RNA-ISH, 세포주)

- MDA-MB231: $R^2 = 0.06052$, p = 0.0146 (유의)
- MDA-MB453: $R^2 = 0.009$, p = 0.2305 (비유의 — 이 세포주에서 상관 없음)
- MDA-MB468: $R^2 = 0.1234$, p < 0.0001 (유의)
- 해석: 세포주 간 일관성 불완전. MDA-MB453 비유의는 Figure 5D의 임상 상관 해석 시 주의 필요.

#### Figure S4 — CTC subtype ratio by BC subtype (n=39)

E-CTC (epithelial), H-CTC (hybrid), T-CTC (TROP2 양성) 비율을 violin plot으로 제시 (Luminal n=15, HER2+ n=13, TNBC n=11). TNBC에서 H-CTC 및 T-CTC 비율이 더 높게 분포.

---

## 분석 자체에 대한 메모

- paper-info.yaml의 `authors_short`가 "Chen, X. et al."로 기재되어 있으나 실제 1저자는 Qingyu Liao 외 공동 1저자. `liao2024trop2ctc`로 citation key 수정 권장.
- TROP2 단독 CTC (CK-음성 TROP2-양성 EMT-CTC) 회수율 정량 수치가 본문에 없음 — 논문의 핵심 주장(EMT-CTC 추가 포착) 대비 가장 결정적인 수치 gap.
- 임상 cohort IRB: Chongqing University Cancer Hospital 윤리위원회 승인 명시. IRB 승인 기재됨.
- 39례 cohort에서 TNBC n=11만으로 TNBC-specific 결론의 통계적 파워가 제한적. 저자도 limitation으로 직접 언급.
