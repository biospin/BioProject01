# kwon-2023-kaist-logic-gate — Core Analysis

## Executive Summary

- **무엇**: CAR 치료의 off-tumor 독성 문제를 해결하기 위해 단일세포 분해능에서 암세포와 정상세포를 구별하는 combinatorial 표면 항원 쌍을 AND/OR/NOT logic gate 기준으로 자동 선발하는 계산 파이프라인(PCASA).
- **모델 / 방법**: Random Forest(RF) → 상위 100개 단일 항원 선발 → CNN으로 9,900쌍 조합 평가 → AND/OR/NOT gate별 Expressing Cell Fraction(ECF) 계산; 입력 = 단일세포 binarized 발현 행렬(tumor + normal), 출력 = CNN weight로 순위화된 gene pair + logic gate.
- **핵심 결과**:
  - ① 1,007,414 세포(412 종양, 12 정상 장기, 17 암종) meta-atlas 구축 — 기존 bulk 기반 대비 ECF와 평균 발현 수준 간 상관계수가 암종별 r = 0.48–0.80으로 중등도, ECF 우위.
  - ② OV에서 AND gate 상위 후보(예: CLDN3 & FOLR1) tumor ECF 74–79%, normal ECF 19% 미만; 기존 임상 단일 항원 7개 중 5개가 tumor ECF 50% 미만이었던 것과 대비.
  - ③ EPCAM-and-CD24 CITE-seq 단백질 수준 검증: tumor ECF(RNA) 90.2%/82.0%, OTE(off-target epitope) CITE-seq 기반 normal ECF 22.4%/35.5%.
  - ④ CLDN3 & CLDN4 IHC 검증: CRC 19/20 케이스 양성(CLDN4 95%, CLDN3 90%), OV 양성; 정상 폐·난소 조직 음성.
  - ⑤ CRC CEACAM5-not-CA4: tumor ECF 90.5%, normal ECF 9.7%.
- **우리 적용**: ADC/CAR 타겟 선정 근거(BD-pitch reference) 및 난소암·CRC 표면항원 combinatorial 우선순위 목록으로 직접 활용 가능 — `BD-opportunity`, `academic-citation`.
- **심층**: 한계·재현 ROI → `kwon-2023-kaist-logic-gate_lens-academic.md` / `kwon-2023-kaist-logic-gate_lens-industry.md` / `kwon-2023-kaist-logic-gate_methodology-brief.md` 참고.

---

## Identity

- **Title**: Single-cell mapping of combinatorial target antigens for CAR switches using logic gates
- **Authors**: Joonha Kwon, Junho Kang, Areum Jo, Kayoung Seo, Dohyeon An, Mert Yakup Baykan, Jun Hyeong Lee, Nayoung Kim, Hye Hyeon Eum, Sohyun Hwang, Ji Min Lee, Woong-Yang Park, Hee Jung An, Hae-Ock Lee, Jong-Eun Park, Jung Kyoon Choi
- **Year**: 2023
- **Venue**: Nature Biotechnology, Vol. 41, pp. 1593–1605 (November 2023)
- **DOI**: 10.1038/s41587-023-01686-y
- **Received**: 2022-05-13 / **Accepted**: 2023-01-20 / **Published online**: 2023-02-16
- **Citation key**: kwon2023logicgate
- **Corresponding authors**: Hee Jung An (hjahn@cha.ac.kr), Hae-Ock Lee, Jong-Eun Park (jp24@kaist.ac.kr), Jung Kyoon Choi (jungkyoon@kaist.ac.kr)
- **Affiliation**: KAIST (Bio and Brain Engineering; GSMS Engineering), The Catholic University of Korea, CHA Bundang Medical Center, Samsung Genome Institute, Penta Medix Co., Ltd.
- **PMID**: 36797491

---

## Background

#### 배경 스토리

- **문제의 출발점**: CAR-T 세포 치료는 종양 항원을 표적으로 삼지만 동일한 항원이 정상 조직에서도 발현될 경우 off-tumor 독성이 발생한다. 고형암은 특히 종양 내 이질성(intratumoral heterogeneity)이 커서 균일한 항원 발현을 기대하기 어렵다.

- **선행 접근 A — 단일 항원 bulk 선발**: 기존 방법은 RNA 발현 프로파일링(bulk RNA-seq)을 사용해 암세포에서 높이 발현되는 단일 항원을 찾았다. EPCAM, MUC16, FOLR1, MSLN 등이 대표적으로 임상시험에 진입했다.
  - A의 한계: Bulk 발현 수준은 개별 세포 수준의 발현 이질성을 감춘다. 집단 평균이 높아 보여도 실제로는 일부 클론에서만 발현될 수 있다. 또한 정상 조직에서의 on-target/off-tumor 발현 여부를 세포 유형 수준에서 평가하지 못한다. 본문에서 저자들은 이를 명시: "average expression levels, even when retrieved from separated tumor and normal cells, can be misleading in identifying and evaluating therapeutic targets."

- **선행 접근 B — dual-target CAR (bispecific)**: 최근 AND, OR, NOT logic gate를 구현하는 CAR switch 연구들이 단일 항원의 한계를 보완하려 시도했다(refs. 10–14). 두 항원을 조합하면 특이도 또는 커버리지를 향상시킬 수 있다.
  - B의 한계: 기존 combinatorial 연구들은 대부분 bulk 발현 수준으로 항원 조합을 설계했다. 이때 population 수준에서는 AND(두 항원이 공동 발현되는 세포)와 OR(어느 하나라도 발현되는 세포)를 구별할 수 없다. 단일세포 수준에서 개별 세포의 발현 논리를 평가해야만 logic gate가 의미 있다.

- **이 논문으로 이어지는 gap**: 단일세포 발현 데이터를 이용해 암세포와 정상세포를 구별하면서 AND/OR/NOT logic gate 각각에 최적화된 표면항원 쌍을 체계적으로 순위화하는 계산 방법이 없었다. 특히 세포 하나하나의 binarized 발현 패턴에서 logic gate별 Expressing Cell Fraction(ECF)을 산출하는 것이 핵심 gap이다.

#### 기본 개념

- **Expressing Cell Fraction (ECF)**: 특정 세포 집단(예: 종양세포 또는 정상세포) 중 해당 유전자를 발현하는 세포의 비율. 논문에서는 binarized 발현(유무)으로 계산. ECF는 항원 커버리지(tumor ECF ↑)와 특이도(normal ECF ↓)를 동시에 평가하는 지표로 사용된다.

- **Logic gate 유형**:
  - AND gate: 두 항원을 *동시에* 발현하는 세포만 표적. 암세포에서는 AND ECF가 높고, 정상세포에서는 낮아야 이상적.
  - OR gate: 두 항원 중 *하나라도* 발현하는 세포 표적. 커버리지는 올라가지만 정상 독성 위험도 높아질 수 있음.
  - NOT gate: 항원 A를 발현하지만 항원 B는 발현하지 않는 세포 표적. 항원 A는 activating switch, B는 inhibitory switch 역할.

- **Surfaceome**: in silico human surfaceome 데이터베이스(wlab.ethz.ch/surfaceome)에서 plasma membrane에 위치하는 2,802개 표면 단백질 유전자 목록. CAR therapy 표적은 항체나 scFv가 접근 가능한 세포 표면에 있어야 하므로 이 범위로 제한.

- **CAR switch 개념**: CAR T 세포가 Boolean logic gate 중 하나로 작동하도록 설계된 construct. AND gate CAR는 두 항원이 동시에 있을 때만 활성화, NOT gate CAR는 B 항원이 있는 정상세포를 피하면서 A 항원 양성 암세포를 표적한다.

#### 이 논문의 필요성

- **핵심 이유**: 고형암 CAR 치료의 off-tumor 독성은 단일세포 수준에서 정상세포 발현 패턴을 평가하지 않고 항원을 선발하기 때문에 발생한다.
- **기존 방법으로 부족했던 지점**: Bulk 발현 기반 대규모 항원 탐색과 단일세포 분해능 간의 괴리, AND/OR 조합을 세포 단위로 평가하는 계산 파이프라인 부재.
- **이 논문이 해결하려는 방향**: 1.4백만 세포 규모 tumor-normal meta-atlas 위에서 RF + CNN 두 단계 머신러닝으로 logic gate별 최적 surfaceome 유전자 쌍을 자동 순위화하고, CITE-seq 및 IHC로 단백질 수준 검증까지 수행.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: 단일세포 발현 atlas에서 암세포 대 정상세포 구별에 최적화된 surface antigen 조합(gene pair)을 AND/OR/NOT logic gate별로 순위화.
- **입력**: 단일세포 RNA-seq batch-corrected 발현 행렬 (batch-corrected CPM, binarized), surfaceome 유전자 2,802개, sample label (tumor cell / normal cell).
- **출력**: 각 cancer type별 logic gate(AND/OR/NOT)별 상위 gene pair 목록 + CNN weight + 조합 ECF (tumor/normal).
- **추정 대상**: 각 gene pair의 "malignancy 구별 기여도" (feature importance in RF; CNN weight in CNN).
- **중요한 hidden assumption**: 유전자 발현을 binarized (0/1)로 처리하므로 연속 발현 수준의 정보가 손실된다. 세포 dropout 효과(false 0)가 결과에 영향을 줄 수 있음을 저자도 Discussion에서 명시.

#### 확률 / 통계학적 구조

- **Model family**: Step 1 — Random Forest (discriminative, supervised classification); Step 2 — CNN (discriminative, supervised classification).

- **Step 1 — RF cell classifier for single-antigen selection**:
  - 입력 행렬: 세포 × 2,802 surfaceome 유전자 (발현 수준, batch-corrected CPM).
  - 레이블: tumor cell (1) / normal cell (0).
  - `randomForest` R package v4.6.14, 100 trees (ntree), 48 variables (mtry) per tree.
  - 훈련 80% / 테스트 20% 분할.
  - Performance: AUC > 0.99 for all cancer types (Supplementary Table 4).
  - 출력: Feature Importance (FI) by "mean decrease in accuracy" — 상위 100개 유전자 선발.

- **Step 2 — CNN cell classifier for combinatorial target selection**:
  - 입력 행렬: 세포 × 9,900 gene pair combinations (각 pair × 4 feature: exp level gene A, FI gene A, exp level gene B, FI gene B), 즉 9,900 × 4 = 39,600 column.
  - 실제 모델 구조 (Methods §CNN cell classifier):
    - 1st convolution layer: 32 filters (2×1), strides (2×1), ReLU
    - 2nd convolution layer: 32 filters (2×1), strides (1×1), ReLU, 0% dropout
    - Pooling + flatten: max-pooling (1×11) + flatten
    - 1st dense: 450 nodes, ReLU, 25% dropout
    - 2nd dense: 45 nodes, ReLU
    - Output: 2 nodes, sigmoid (binary classification)
  - 총 12,983,013 parameters. Keras 2.6.0 / TensorFlow 2.4.1. Adam optimizer, binary cross-entropy loss, batch size 500, 10 epochs, 5-fold cross-validation.
  - Grad-CAM(Gradient-weighted Class Activation Mapping)으로 각 gene pair의 CNN weight 계산.

- **Likelihood / objective**: Binary cross-entropy. 세포 단위로 malignant vs non-malignant label을 맞추도록 학습.

- **ECF 계산 (expression logic evaluator)**: 각 세포의 두 유전자 발현을 binarized (0/1)로 처리한 뒤, AND = 둘 다 1인 세포 비율, OR = 하나라도 1인 비율, NOT = gene A=1이고 gene B=0인 비율을 각각 tumor와 normal 집단에서 산출.

- **ECF criteria (선발 기준)**: tumor ECF > 70%, normal ECF < 10%를 "좋은 CAR switch 후보"로 정의.

#### 핵심 method insight

- **기존 방법의 한계**: Bulk 발현 수준을 feature로 사용하면 세포 이질성을 무시. ECF와 평균 발현 수준 사이의 상관계수가 r = 0.48–0.80으로 중등도 — 높은 발현 수준이 반드시 높은 ECF를 의미하지 않는다.
- **이 논문이 바꾼 가정**: 발현을 연속값이 아닌 *세포 단위 유무(0/1)* 로 처리 → logic gate 정의가 가능해짐. 동시에 cell classifier를 세포 × 유전자 행렬로 훈련하여 단일세포 분해능에서 malignancy를 예측.
- **새로 추가한 변수 또는 구조**: 
  - ECF (Expressing Cell Fraction) — 기존 "평균 발현 수준"의 single-cell 대응 지표.
  - Logic gate ECF — AND/OR/NOT에 따라 동일 gene pair도 다른 tumor/normal ECF를 가짐.
  - Grad-CAM weight — CNN 결정에 기여한 gene pair의 중요도 해석.
- **이 변화가 중요한 이유**: 동일한 유전자 쌍이라도 logic을 어떻게 적용하느냐에 따라 off-tumor safety 프로파일이 달라짐을 정량화. 예: ERBB2의 FI가 HER2+ 환자에서 가장 높고, HER2+/ER+ 환자에서는 AND gate partner가 OR gate partner보다 더 특이적.

#### 이전 방법과의 차이

- **Baseline**: 기존 임상시험 진행 중이거나 bulk RNA-seq 기반으로 선발된 95개 이전 CAR 타겟(논문 Fig. 4a, gray bars).
- **공통점**: 표면 단백질 유전자 목록(surfaceome) 사용; 암세포 vs 정상세포 구별 목표.
- **차이점**:
  - 단일세포 분해능 → 세포 이질성 및 off-tumor cell type 평가 가능.
  - ECF로 coverage와 specificity 동시 평가 (기존은 평균 발현 수준만).
  - AND/OR/NOT 세 가지 logic을 동시에 최적화.
  - CNN이 두 유전자의 조합 패턴을 단일세포 행렬로 직접 학습.
- **차이가 크게 나타나는 조건**: 고이질성 암종(OV, BRCA 등), 정상 조직에도 낮은 수준으로 발현되는 항원의 off-tumor 평가.

#### 효과가 Results에서 나타난 방식

- **Benchmark**: OV에서 기존 임상 타겟 95개 중 7개만 tumor ECF > 50% (Fig. 4a, gray bars). RF/CNN method의 AND/OR/NOT 조합은 ECF criteria(>70% tumor, <10% normal)를 만족하는 후보를 복수 도출.
- **BRCA subtype validation**: ERBB2 FI가 HER2+ subtype에서 가장 높음 — 알려진 임상 사실과 일치, method 신뢰도 확인 (Fig. 3d).
- **CITE-seq epitope validation**: EPCAM, CD24, FOLR1의 단백질 수준 ECF가 meta-atlas RNA ECF와 높은 일치 (tumor ECF ~90% 이상). 단 정상세포 ECF는 RNA 기반 추정보다 CITE-seq에서 낮아지는 경우도 있음 — RNA contamination 교정 효과.
- **IHC validation (CRC)**: CLDN3 (90%)와 CLDN4 (95%) 단백질 양성률 CRC 케이스에서 확인, 정상 폐·난소 조직 CLDN3/4 음성.

#### Method 관점의 한계

- **약한 assumption**: binarized 발현은 dropout 효과에 민감. 낮은 발현 유전자의 0이 생물학적 미발현인지 기술적 dropout인지 구별 불가. 저자는 "final candidates should be pruned by careful inspection of individual cells"라고 명시.
- **구현 또는 학습상의 부담**: CNN 12.9M parameters, 5-fold CV 10 epochs — 9,900쌍 × 세포 수 규모. runtime 미제공.
- **일반화가 불확실한 조건**: BRCA처럼 intertumoral heterogeneity가 큰 암종에서는 sample-wise variation이 커서 일부 환자에 적용 불가. 저자도 "patient subtyping based on single-cell expression logic analysis" 필요성을 언급.

---

## Results

#### Dataset별 결과

##### Dataset 1 — Tumor-normal single-cell meta-atlas 구축

- **Dataset**: 17개 암종 412개 종양의 공개 scRNA-seq + 자체 OV 9 샘플; 12개 정상 장기 정상세포 atlas (Human Cell Atlas 등).
- **목적**: pan-cancer/pan-tissue 단일세포 맥락에서 ECF를 정확하게 계산하기 위한 reference 구축.
- **사용한 데이터 규모**: 종양 세포 1,007,414개 총합 (cancer cell atlas, CCA); 정상 참조 401,717개 세포, 111 cell type (Fig. 1c, 1f). OV dataset은 자체 수집 9 환자.
- **Baseline / 비교 대상**: 정상세포 atlas를 tumor dataset과 통합 정규화 (BBKNN v1.5.1, ridge-regularized linear regression batch correction).
- **Metric**: UMAP clustering — 동일 조직 기원의 세포가 함께 군집되어 통합 성공 확인 (Fig. 1e).
- **주요 수치**: 종양세포 25%, 상피세포 19% (Fig. 1f pie chart). Meta-atlas는 https://cellatlas.kaist.ac.kr/cart에 공개.
- **정성 결과**: 종양 타입별 tSNE에서 cell type annotation이 일관되게 유지됨.

##### Dataset 2 — ECF vs. average expression level 비교

- **Dataset**: Meta-atlas의 6개 주요 암종 (OV, PAAD, LIHC, NSCLC, CRC, BRCA).
- **목적**: 단일세포 ECF가 bulk 평균 발현 수준보다 우월한 지표임을 보임.
- **Metric**: Pearson r (ECF vs. average expression level, per gene, in tumor cells and normal cells).
- **주요 수치**: OV tumor r = 0.67, normal r = 0.79; BRCA tumor r = 0.62, normal r = 0.79; NSCLC tumor r = 0.48, normal r = 0.78. 모든 암종에서 중등도 상관 → ECF와 발현 수준이 일치하지 않는 유전자가 다수 존재 (Fig. 2a).
- **추가 수치**: Differential ECF의 P-value와 FI 상관 > differential expression level P-value와 FI 상관 (OV r = 0.37 vs. 0.30, NSCLC r = 0.36 vs. 0.30) — ECF 기반 선발이 더 타당함을 지지 (Fig. 2d).

##### Dataset 3 — RF cell classifier (단일 항원 선발)

- **Dataset**: 위 6개 암종 meta-atlas subset.
- **목적**: 각 암종별로 종양-정상 구별에 기여하는 상위 100개 surfaceome 유전자 선발.
- **Metric / 평가 기준**: AUC (ROC curve).
- **주요 수치**: AUC > 0.99 for all examined cancer types (Supplementary Table 4).
- **정성 결과**: FI 상위 유전자는 암종별로 상이 (Fig. 2e — LIHC 특이적 C3 cluster 유전자 vs. 범암종 공통 C5 cluster). ERBB2 FI는 HER2+ BRCA subtype에서 최고 (Extended Data Fig. 4) — 알려진 임상 생물학과 일치.
- **통계**: All reported P-values two-sided; P < 0.05 considered statistically significant.

##### Dataset 4 — CNN combinatorial selection + logic gate ECF 평가 (OV 중심)

- **Dataset**: OV subset (자체 수집 9환자 포함).
- **목적**: 최적 AND/OR/NOT logic gate 조합 선발 + ECF criteria 충족 여부 평가.
- **Metric**: CNN weight (Grad-CAM) + combinatorial ECF (tumor/normal).
- **주요 수치 (Fig. 3f, OV)**:
  - AND gate: ECF criteria(>70% tumor, <10% normal) 충족 조합 다수; OR/NOT은 fewer combinations.
  - OV의 AND 상위 후보(Fig. 4b): EPCAM-and-CD24 (tumor 90.2%, normal 22.4%), EPCAM-and-FOLR1 (tumor 82.0%, normal 25.8%), FOLR1-and-CD24 (tumor 80.0%, normal 18.1%).
  - OR gate 상위 (Fig. 4b): FOLR1-or-VTCN1, CESR2-or-FOLR1 — 더 높은 tumor ECF이나 normal ECF도 높아짐.
  - NOT gate: FOLR1-not-CD52 (tumor 100%, normal 3.9%), MUC16-not-CD52 (tumor 79.5%, normal 6.9%) — CD52는 정상세포(림프구) 마커로 inhibitory switch 역할.
- **정성 결과**: 기존 임상 타겟 95개 중 7개만 tumor ECF > 50% (Fig. 4a, gray bars), 반면 RF/CNN 파이프라인은 ECF criteria 충족 후보 다수 발굴.

##### Dataset 5 — CITE-seq epitope validation (OV)

- **Dataset**: OV 3 samples pooled; CRC 3 additional samples (not in meta-atlas).
- **목적**: 선발된 logic switch 후보의 단백질 수준 발현을 단일세포 분해능으로 검증.
- **Metric**: CITE-seq ADT normalized protein expression level; log₂ fold-change (antibody vs. isotype control).
- **주요 수치 (Fig. 5a, OV)**:
  - Meta-atlas RNA ECF: EPCAM 95.2%, CD24 92.9%, FOLR1 84.6%, CD52 56.6%.
  - CITE-seq RNA ECF (OV samples): EPCAM 90.2%, CD24 82.0%, FOLR1 97.2%, CD52 81.0%.
  - CITE-seq protein ECF (OV samples): EPCAM 99.6%, CD24 94.5%, FOLR1 91.5%, CD52 92.2% (tumor); normal EPCAM 43.3%, CD24 16.7%, FOLR1 14.2%, CD52 44.0%.
  - AND gate (EPCAM-and-CD24): tumor protein ECF 90.2%, normal 35.5% (Fig. 5a, right).
  - NOT gate (FOLR1-not-CD52): tumor protein ECF 81.0%, normal 16.3%.
- **주의**: Normal ECF가 meta-atlas RNA 기반보다 CITE-seq 기반에서 일부 상승 — ambient RNA contamination에서 비롯된 RNA-level 과추정이 단백질 검증으로 드러남.

##### Dataset 6 — IHC validation (CRC + OV + NSCLC + BRCA)

- **Dataset**: 20개 케이스 × 4 암종 tissue microarray; 각 암종 5 samples (CRC, OV, NSCLC, BRCA).
- **목적**: CLDN3, CLDN4 단백질 발현을 조직 수준에서 확인.
- **주요 수치 (Fig. 6, Discussion)**:
  - CLDN4: CRC 19/20 (95%) 양성, OV 15/20 (75%), NSCLC 12/20 (60%), BRCA 12/20 (60%).
  - CLDN3: CRC 18/20 (90%), OV 13/20 (65%), NSCLC 9/20 (45%), BRCA 6/20 (30%).
  - 정상 폐·난소 조직(alveolar cell, fallopian tube) CLDN3/4 음성. 정상 유선 소엽 세포 및 결장 상피세포에서 CLDN3/4 낮은 수준 발현 관찰.
- **통계**: 재현성 — 각 암종당 2–3 반복 조직 코어 사용. Statistical significance test 미제공 (IHC는 정성/반정량).

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: AND gate는 tumor specificity ↑, coverage ↓; OR gate는 coverage ↑, normal ECF ↑; NOT gate는 특정 암종(LIHC, 림프구 침윤 많은 조직)에서 정상 보호 효율 ↑. 이 패턴은 OV, PAAD, LIHC, NSCLC, CRC, BRCA 전반에서 일관.
- **가장 중요한 수치**: FOLR1-not-CD52 NOT gate: tumor ECF 100%, normal ECF 3.9% (OV, Fig. 4b).
- **baseline 대비 차이**: 기존 임상 타겟 95개의 OV tumor ECF median은 50% 미만; PCASA 상위 AND/OR/NOT 후보는 tumor ECF 70% 이상 다수.
- **결과 해석 시 주의점**: Tumor ECF > 70%, normal ECF < 10% 기준은 저자가 임의 설정한 기준. BRCA는 sample-wise variation이 커 일부 환자에서 발현이 없을 수 있음 (Extended Data Fig. 8). CITE-seq 실험은 항체 품질에 의존적이며 CLDN3/4는 CITE-seq로 검증 불가 (antibody 미작동).

---

## Figures

#### Figure 1 — Tumor-normal 단일세포 meta-atlas 구축 및 특성화

- **이 Figure가 필요한 이유**: 전체 파이프라인의 출발점인 meta-atlas가 올바르게 통합되었음을 보여야 함. 다양한 batch/플랫폼을 통합한 후에도 조직 기원에 따라 세포가 올바르게 군집되는지 확인.
- **이 Figure가 뒷받침하는 주장**: "단일세포 발현 atlas가 암종과 정상 장기를 함께 커버하면서 cell type annotation의 일관성을 유지한다."

##### 패널별 설명
- **a**: 데이터 통합 파이프라인 개요도. Cancer dataset (QC → CopyKAT tumor 세포 분리 → Merge) + Normal atlas (gene ID 정규화 → QC) → Geometric sketching 서브샘플링 → BBKNN batch correction.
- **b**: CAR switch 발굴 워크플로우. Tumor-normal meta-atlas → RF (상위 100 유전자) → CNN (9,900 조합) → AND/OR/NOT logic gate matching → logical CAR switch 후보.
- **c**: 17개 암종별 세포 수 bar plot. OV n=52, BRCA n=40, CRC n=86 데이터셋이 포함. 총 CCA 1,007,414 cells.
- **d**: 6개 암종 tSNE (OV, PAAD, LIHC, NSCLC, CRC, BRCA). 각 점이 cell type으로 색칠됨. 종양세포와 정상 침윤세포가 분리되어 annotation.
- **e**: 정상세포 atlas를 tumor dataset 위에 overlay한 UMAP. 조직 기원이 같은 세포들이 함께 군집 → 통합 성공.
- **f**: 대표 meta-atlas 세포 구성 pie chart (tumor 25%, 상피세포 19%, fibroblast 9%, endothelial 6%, macrophage 5% 등) + cell type별 세포 수 bar plot.

##### 본문에서 강조한 비교
- 비교 대상: UMAP에서 같은 tissue origin의 세포 군집 여부.
- 관찰된 차이: 같은 조직 기원의 세포들이 함께 군집 (Fig. 1e).
- 이 차이가 의미하는 것: ridge-regularized regression + BBKNN이 batch effect를 제거하면서도 생물학적 신호를 보존.

##### 해석 시 주의점
- Geometric sketching 기반 서브샘플링은 희귀 cell type 보존에 유리하지만 dominant cell type의 세포 수를 인위적으로 줄임. 이 과정이 ECF 계산에 영향을 줄 수 있음.

---

#### Figure 2 — 단일 항원 선발 결과 특성화

- **이 Figure가 필요한 이유**: ECF가 평균 발현 수준보다 CAR 타겟 평가에 더 적합한 지표임을 정량화하고, RF가 의미 있는 FI를 반환함을 보임.
- **이 Figure가 뒷받침하는 주장**: "ECF는 bulk 발현 수준이 놓치는 세포-수준 이질성을 포착하는 더 생물학적으로 의미 있는 지표다."

##### 패널별 설명
- **a**: 6개 암종에서 ECF vs. average expression level scatter plot (per gene, tumor 파란점, normal 빨간점). 상관계수 r 명시. Bulk에서 높은 발현인데 ECF가 낮은 유전자, 반대 케이스 모두 존재.
- **b**: RF cell classifier 구조 schematic. 세포 × 유전자 행렬 → decision trees → FI by mean decrease in accuracy.
- **c**: OV surfaceome 유전자 FI (상) 와 평균 발현 수준 차이 (하)를 high→low FI 순 bar plot. FI 높은 유전자가 반드시 발현 수준 차이가 큰 것은 아님.
- **d**: 6개 암종에서 FI와 differential ECF P-value 상관 (r) vs. FI와 differential expression P-value 상관 (r) 비교 — 버블 크기는 -log₁₀(P). Differential ECF P-value 상관이 더 높음.
- **e**: surfaceome 유전자 FI (좌) 와 tumor ECF (우) heat map — 5 cluster (C1–C5). C3 cluster는 LIHC 특이, C4는 낮은 ECF with high expression, C5는 높은 FI + ECF.

##### 본문에서 강조한 비교
- ECF(differential) P-value와 FI 상관이 발현 수준(differential) P-value와의 상관보다 높음 → ECF 기반 지표가 FI 예측에 더 적합.

##### 해석 시 주의점
- Pearson correlation을 per gene 레벨에서 계산하므로 세포 수 차이에 의한 통계 불균형 가능성.

---

#### Figure 3 — 조합 항원 선발 결과 특성화

- **이 Figure가 필요한 이유**: CNN이 AND/OR/NOT gate별로 적절한 gene pair를 선발하며, logic gate 종류에 따라 tumor vs. normal ECF 프로파일이 달라짐을 보임.
- **이 Figure가 뒷받침하는 주장**: "CNN combinatorial classifier가 단일세포 발현 논리에서 logic gate별 최적 항원 쌍을 자동 식별한다."

##### 패널별 설명
- **a**: AND/OR/NOT logic의 population 수준 vs. single-cell 수준 구별 불가능성 개념도 (상). NOT gate 설계를 위해 정상세포의 B 항원 발현이 단일세포 수준에서 확인되어야 함 (하).
- **b**: CNN 구조 schematic. 세포 × 9,900 gene pair 행렬 (각 pair당 exp level + FI 4 feature) → convolution layer 1 (gene A feature 추출) → convolution layer 2 (combined feature) → fully connected layers → binary classification + Grad-CAM weight.
- **c**: AND/OR/NOT logic evaluator 개념도. Tumor cell과 normal cell의 binarized 발현에서 gate별 ECF bar 예시.
- **d**: BRCA subtype별 ERBB2 FI + logic gate partner FI heatmap. HER2+ subtype에서 ERBB2 FI 최고 (0.988), AND gate partner TSPAN13 (0.999), OR gate partner CNTNAP2 (0.769) 등. NOT gate partner에서 GABRP, SLC39A14 등.
- **e**: OV의 AND/OR/NOT gate별 CNN weight vs. ECF scatter plot. AND gate tumor r = 0.58 (P = 0.00), normal r = 0.40 (P = 1.00×10⁻²⁶⁶); OR gate tumor r = 0.68, NOT gate tumor r = 0.35. AND gate에서 tumor ECF와 CNN weight 상관이 가장 강함.
- **f**: AND/OR/NOT gate별 tumor/normal ECF barcode plot (OV). X축 CNN weight 순. 빨간 점선(70% tumor) 와 주황 점선(10% normal) 기준. AND gate에서 기준 충족 조합이 가장 많음.

##### 본문에서 강조한 비교
- AND gate CNN weight-ECF 상관이 OR/NOT보다 강함. LIHC에서는 OR/NOT gate도 많은 조합이 기준 충족.

##### 해석 시 주의점
- LIHC에서 AND gate가 아닌 OR/NOT gate에서 기준 충족 조합이 더 많은 것은 암종별 항원 발현 패턴 차이 반영.

---

#### Figure 4 — OV에서 이전 타겟 대비 combinatorial 항원 후보 평가

- **이 Figure가 필요한 이유**: 실제 임상 타겟과 직접 비교해 파이프라인 우월성을 정량적으로 보임. 또한 각 후보의 cell type 분포를 통해 off-tumor 세부 평가.
- **이 Figure가 뒷받침하는 주장**: "RF/CNN 파이프라인이 기존 임상 타겟보다 우수한 ECF 프로파일을 가진 combinatorial 후보를 발굴한다."

##### 패널별 설명
- **a**: OV에서 이전 95개 타겟의 single/AND/OR/NOT ECF bar plot. Gray bar = 이전 타겟, colored bar = RF/CNN 상위 조합. Dashed line 50%. 이전 타겟 중 7개만 tumor ECF > 50%.
- **b**: AND/OR/NOT gate별 상위 10개 조합의 tumor/normal ECF. FOLR1-not-CD52: tumor 100%, normal 3.9%.
- **c**: AND gate 선발 조합(CLDN3-FOLR1 등) 의 정상 cell type별 ECF bar plot. Alveolar cell, gland에서 CLDN3-FOLR1 조합 발현 — lung toxicity 잠재적 위험.
- **d**: AND gate의 CLDN3/FOLR1 co-expression (Both) 이 tumor-enriched region에 집중 (gray circles, tSNE). NOT gate의 MUC16/CD52 not co-expression이 alveolar cell, ciliated cell, elongated spermatid에 존재.
- **e**: 선발 AND/OR/NOT 조합의 sample-wise expression pattern (heatmap, OV 샘플 × gene pair). 일부 샘플(예: PCBP14)에서 낮은 ECF — sample 이질성 존재.

##### 본문에서 강조한 비교
- 기존 임상 타겟 대비: EPCAM는 기존 AND gate 상위권에 포함(tumor ECF 높음) 이지만 FOLR1이 AND gate에서 ideal counterpart. MSLN, MUC16이 OR gate 상위에 위치 — OR gate에서의 높은 tumor ECF.

##### 해석 시 주의점
- FOLR1-and-SPINT2, FOLR1-and-ITM2B 조합이 alveolar cell에서 공발현 → 폐 독성 위험. Cell type-level 평가 필수.

---

#### Figure 5 — OV에서 CITE-seq 단일세포 에피토프 검증

- **이 Figure가 필요한 이유**: mRNA 발현 기반 ECF가 단백질 수준에서 재현되는지 확인. 단백질이 실제 CAR 타겟 결합의 근거이므로.
- **이 Figure가 뒷받침하는 주장**: "선발된 logic switch 후보가 단일세포 분해능 단백질 수준에서도 tumor-specific 발현 패턴을 보인다."

##### 패널별 설명
- **a**: Meta-atlas RNA ECF (좌) vs. CITE-seq RNA ECF (우) 비교 bar. tumor/normal 각각 single 및 조합 ECF.
- **b**: CITE-seq 기반 세포 clustering + cell type annotation (tSNE).
- **c**: EPCAM, CD24, FOLR1, CD52 mRNA expression level tSNE overlay.
- **d**: EPCAM, CD24, FOLR1, CD52 protein expression level (CITE-seq ADT) tSNE overlay.
- **e**: 8개 cell type별 4개 단백질 발현 ridge plot. CD52는 정상세포(B cell, T cell)에서 주로 발현, EPCAM/CD24/FOLR1은 tumor cell에서 높음.
- **f**: AND/OR/NOT gate별 scatter plot (tumor vs. normal). EPCAM-and-CD24 AND gate box에 tumor 집중. CD24-or-FOLR1 OR gate. CD52-not-FOLR1 NOT gate.

##### 본문에서 강조한 비교
- RNA vs. 단백질 ECF 비교: RNA 과추정(ambient RNA contamination)으로 정상세포 ECF가 실제보다 높게 나타날 수 있음. 단백질 검증에서 FOLR1 normal ECF가 낮아짐.

---

#### Figure 6 — CLDN3/CLDN4 IHC 검증 (CRC, OV, NSCLC, BRCA)

- **이 Figure가 필요한 이유**: CITE-seq 항체가 작동하지 않은 CLDN3/CLDN4를 조직 수준 IHC로 검증. 단백질 발현을 임상 샘플에서 확인.
- **이 Figure가 뒷받침하는 주장**: "CLDN3/CLDN4는 복수 암종의 임상 조직에서 종양세포 막에 발현된다."

##### 패널별 설명
- **a–d**: CRC, OV, NSCLC, BRCA 각 3 반복(i–ix)의 H&E 및 CLDN3/CLDN4 IHC 이미지. Scale bar 300 μm.
  - CRC: CLDN4 membrane staining 강함, CLDN3 약간 낮음.
  - OV: CLDN4 > CLDN3.
  - NSCLC: 혼합 양성/음성.
  - BRCA: CLDN3/4 양성, 정상 유선 소엽에서 낮은 수준.

##### 해석 시 주의점
- IHC는 반정량적. Anti-CLDN3/4 항체 클론이 다르므로 민감도 차이 가능. Staining intensity는 수치화되지 않음.

---

#### Extended Data Figures (요약)

- **Extended Data Fig. 1**: 정상세포 atlas에 tumor 세포를 overlay한 UMAP (cell type annotation; data source 별).
- **Extended Data Fig. 2**: PAAD, LIHC, NSCLC, CRC, BRCA에서의 ECF 차이 (a) 및 발현 수준 차이 (b). OV Fig. 2c의 다른 암종 버전.
- **Extended Data Fig. 3**: 암종별 FI clustering heatmap (expression level) 및 FI 상관계수 matrix. FI 상관: CRC-BRCA r = 0.7, OV-LIHC r = 0.51.
- **Extended Data Fig. 4**: BRCA subtype별 ERBB2/ESR1/PGR ECF boxplot. HER2+ 에서 ERBB2 ECF 0.86±0.19.
- **Extended Data Fig. 5**: PAAD, LIHC, NSCLC, CRC, BRCA에서 CNN weight vs. ECF scatter (AND/OR/NOT × 5 암종). Fig. 3e의 확장.
- **Extended Data Fig. 6**: PAAD, LIHC, NSCLC, CRC, BRCA에서 AND/OR/NOT gate별 ECF barcode plot. Fig. 3f 확장. LIHC는 OR/NOT gate에서 ECF criteria 충족 조합 많음.
- **Extended Data Fig. 7**: OV AND/OR/NOT gate 후보의 TCGA (n=11,768) vs. GTEx normal (n=17,382) sample-wise co-expression. AND 후보는 TCGA에서 높은 co-expression, GTEx에서 낮음.
- **Extended Data Fig. 8**: PAAD, LIHC, NSCLC, CRC, BRCA의 top 10 gene pair 조합별 sample × ECF heatmap. BRCA에서 sample 간 변동성 큼.
- **Extended Data Fig. 9**: OV CITE-seq의 EPCAM/CD24 추가 분석.
- **Extended Data Fig. 10**: CRC CITE-seq validation (CEACAM5, EPCAM, CA4, CPM, VSIG2). CEACAM5-not-CA4 AND gate 검증.

---

## Tables

본문에 정식 Table 없음. 주요 정량 데이터는 Supplementary Tables에 위치.

- **Supplementary Table 1**: 통합된 암종별 sample 수 및 세포 수.
- **Supplementary Table 2**: 12개 정상 장기 111 cell type 목록.
- **Supplementary Table 3**: 분석에 사용된 OV, NSCLC, CRC, BRCA, LIHC, PAAD dataset 목록.
- **Supplementary Table 4**: RF model performance (AUC) by cancer type. AUC > 0.99.
- **Supplementary Table 5**: 각 암종별 FI 상위 100개 유전자.
- **Supplementary Table 6**: CNN model의 Grad-CAM weight (gene pair × cancer type).
- **Supplementary Table 7**: CNN 모델 loss, accuracy, F1, precision, recall, ROC by cancer type.
- **Supplementary Table 8**: OV gene pair의 TCGA/GTEx co-expression correlation.
- **Supplementary Table 9**: AND/NOT gate 정상 cell type별 ECF 분석.

---

## Supplementary Information

- **Supplementary Note**: Methods 상세 — BBKNN 구현, CopyKAT tumor 세포 분리, Geometric sketching 파라미터.
- **Extended Data Figs. 1–10**: 앞서 Figures 섹션에서 요약.
- **Reporting Summary**: IRB 승인 (CHA Bundang Medical Center IRB No. 2019-08-039), 9명 여성 환자 (HGSOC, mean age 56), Stage I–IV. 성/젠더 분석 없음. 5-fold cross-validation; randomization (gene combination 셔플). No sample size calculation.

---

## 분석 자체에 대한 메모

- 검토필요: Fig. 4a에서 AND/OR/NOT gate의 tumor ECF가 "기존 타겟 95개 대비 더 높다"고 강조되지만, 기존 타겟의 ECF cutoff 기준(50%)이 논문의 ECF criteria(70%)와 다름 — 직접 비교 시 기준 불일치에 주의.
- 검토필요: CITE-seq 실험에서 normal ECF가 RNA-atlas 기반보다 낮아지는 경우(ambient RNA correction 효과)와 높아지는 경우(anti-tumor antibody contamination)가 섞여 있음 — 논문에서 "prone to experimental noise"로 명시.
- 질문: PCASA GitHub 코드(https://github.com/kaistomics/PCASA)가 HGSOC 외 암종에 대해 독립적으로 재현 가능한지 확인 필요. OV self-data가 public GEO (GSE192898)에 공개됨.
