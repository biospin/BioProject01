# Lens — Academic
# kang-2024-kaist-tumor-normal

## Limitations

### 저자가 명시한 한계

- **TLS-enriched cell type의 다른 암종 일반화**: RCC 공간 전사체에서 TLS signature를 검증했으나, 같은 signature가 RCC 이외 암종에서 TLS-정의 조직과 동등한 cell type 구성을 가지는지는 확인이 부족하다고 저자가 논의에서 인정 (p.9, Discussion 단락).
- **면역치료 예측 cell state들의 TCGA 예후 비유의성**: 면역치료 favorable cell state들이 TCGA 생존 분석에서 유의미한 예후 효과를 보이지 않음 (Supp. Fig. S17, S18). 저자는 이를 면역치료 특이적 반응 예측 지표이지 일반 예후 지표가 아니라고 해석.
- **단일 면역치료 약제 범주**: CTLA4 및 PD-1/PD-L1 억제제 중심. 다른 modality(항체-약물 결합체, 세포 치료 등)에서의 예측력은 검증되지 않음.
- **Geometric sketching 서브샘플링**: 희귀 cell state가 과소 대표될 가능성. 전체 4.9M 세포가 아닌 subsampled dataset으로 atlas를 구성했으며, 각 dataset의 서브셋 대표성이 암종·기관 간 불균일.

### 분석자가 판단한 한계

- **부족한 점 1 — LC cohort 과중량**: 면역치료 meta-analysis ($n=1,261$)에서 LC cohort가 $n=497$ (39%)로 가장 크다. 코호트 간 이질성($I^2$) 수치가 본문에 제시되지 않아, pooled OR의 신뢰도를 코호트 수준에서 판단할 수 없다.
  - **왜 중요한가**: LC cohort에서 특이하게 강하거나 약한 cell state 연관성이 전체 OR을 왜곡할 수 있다. OR의 범암종 일반화 주장이 약해진다.
  - **어떤 증거가 부족한가**: 코호트별 leave-one-out 민감도 분석 또는 $I^2$ 통계.

- **부족한 점 2 — smFISH 샘플 수 제한**: AKR1C1⁺/WNT5A⁺ fibroblast 공간 검증에 smFISH $n=3$ 조직만 사용. 통계 검정 없이 representative image로 제시.
  - **왜 중요한가**: fibroblast 아형 구분의 핵심 주장(AKR1C1⁺ vs WNT5A⁺ 공간 위치 차이)이 quantitative spatial analysis가 아닌 visual evidence에 의존한다.
  - **어떤 증거가 부족한가**: 더 많은 환자 샘플에서 통계적으로 검증된 co-localization 점수; 또는 multiplex immunofluorescence(mIF)로 protein 수준에서 확인.

- **부족한 점 3 — functional validation 없음**: AKR1C1⁺/WNT5A⁺ fibroblast의 서로 다른 면역조절 역할(한쪽은 immune evasion, 다른 쪽은 immunosuppression)을 in vitro 또는 in vivo 교란 실험 없이 co-occurrence와 ligand-receptor 추정으로만 주장한다.
  - **왜 중요한가**: fibroblast subtype 타깃 치료 전략을 정당화하기 위해서는 기능적 인과 증거가 필요하다.
  - **어떤 증거가 부족한가**: 조건부 knockout, 세포 공배양 실험, 또는 환자 유래 organoid 모델에서 fibroblast subtype 비율 조작 후 T cell 기능 변화 측정.

- **부족한 점 4 — tumor purity 통제**: 각 scRNA-seq 샘플의 tumor purity(종양 세포 비율)가 cell state co-occurrence 분석에 혼란 변수로 작용할 수 있다. 높은 tumor purity 샘플에서는 immune cell state가 과소 대표되고, 낮은 purity에서는 과대 대표된다.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: "인터페론 풍부 community가 면역치료에 favorable하다"는 주장과 "TLS가 인터페론 community의 핵심 구조다"라는 주장을 연결할 때, TLS-exclusive 분석이 아닌 TLS-enriched cell type 분석으로 연결하고 있다. Exhausted CD8⁺ T cell, ISG15⁺ macrophage, pDC가 TLS와 공간적으로 무관하지만 면역치료 favorable로 나오는 것이 이 연결의 일관성을 약화.
- **현재 근거**: co-occurrence network에서 interferon-enriched community로 묶이고, 면역치료 반응 meta-analysis에서 OR > 1 확인. 하지만 TLS 내부에 있어서 favorable인지, TLS 없이도 independent하게 favorable인지 분리 증명이 없음.
- **더 필요해 보이는 근거**: 공간 transcriptomics에서 TLS 양성/음성 영역 내 cell state 조성과 면역치료 반응을 동시에 가진 데이터 (예: 생검 전/후 paired spatial data).

### 정리되지 않은 질문

- `질문:` AKR1C1⁺ fibroblast가 OV/UCEC에서 높은 비율을 보이는데, 이 기관 특이성이 ADC 개발 시 off-target toxicity에 어떤 영향을 주는지 별도로 정량화가 필요하다.
- `질문:` TLS signature로 예측된 면역치료 반응이 anti-CTLA4 vs. anti-PD1/L1에서 effect size가 다른지 (약제 특이성). cohort 분류 상 Van Allen/Gide/Hugo가 CTLA4 inhibitor, Riaz가 anti-PD1 — 세부 분석이 본문에 없다.
- `질문:` LAMP3⁺ DC가 TLS의 핵심 조직화 세포로 알려져 있는데 (`외부 맥락:` Sautès-Fridman et al., 2019), 이 논문이 LAMP3⁺ DC의 어떤 세부 substate가 TLS 형성을 주도하는지까지 들어가지는 않는다. 다음 분석 후보.

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 단일 세포 수준에서 tumor와 정상 조직을 30개 암종에 걸쳐 동시에 비교 가능한 최초 수준의 대규모 atlas. ADC target validation, biomarker 개발, TME 이해 모두에서 reference로 직접 활용 가능한 자원 논문.
- **다음 논문으로 이어질 아이디어**:
  1. WNT5A⁺ fibroblast의 면역억제 기전을 조건부 depletion 모델로 검증 — CRISPR/조건부 knockout 마우스에서 WNT5A fibroblast 제거 후 T cell infiltration과 면역치료 반응 변화 측정.
  2. TLS-exclusive cell state 분석 — spatial transcriptomics에서 TLS 영역 내 cell state composition을 분리해, TLS-dependent vs. TLS-independent 면역치료 예측인자를 구분.
  3. AKR1C1⁺ fibroblast의 ADC 독성 관련성 — 정상 fibroblast에서 AKR1C1 발현 수준을 organ별로 정량화하고 ADC 노출 시뮬레이션.
- **설명을 더 매끄럽게 만들 방법**: smFISH $n=3$ → 최소 $n \geq 10$ 조직 샘플에서 multiplex IF를 이용해 AKR1C1/WNT5A fibroblast 존재를 정량화하고 neighboring cell type과의 거리 통계를 추가하면 기관별 co-localization 주장이 훨씬 강해진다.
- **우선순위가 높은 후속 실험 / 분석**:
  - TLS-exclusive 면역치료 반응 분석 (Zenodo dataset 활용 — 이미 공개)
  - LC cohort를 제외한 leave-one-out meta-analysis로 OR robustness 확인 (공개 데이터만으로 재현 가능)
  - cellatlas.kaist.ac.kr/ecosystem/ web portal에서 우리 관심 cell state(AKR1C1⁺, WNT5A⁺ fibroblast, LAMP3⁺ DC)의 정상 조직 발현 패턴 직접 조회

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction (p.2): "TME phenotypes are not simply binarized into anti-tumor or pro-tumor but rather represent interactive cellular organizations or ecosystems."
  - 사용 시나리오: ADC pitch deck 또는 논문 introduction에서 TME ecosystem 관점의 필요성을 강조할 때.
  - BibTeX key: `@kang2024tumornormal`

- §Abstract: "We perform an integrative analysis of 4.9 million single-cell transcriptomes from 1070 tumor and 493 normal samples in combination with pan-cancer 137 spatial transcriptomics, 8887 TCGA, and 1261 checkpoint inhibitor-treated bulk tumors."
  - 사용 시나리오: 단일 세포 + 공간 + bulk 통합 분석의 규모를 인용해 tumor-normal 비교 resource의 필요성과 존재를 논거로 삼을 때.
  - BibTeX key: `@kang2024tumornormal`

- §Discussion (p.10): "Our pan-cancer tumor-normal single-cell meta-atlas presented in the study would provide essential insights into a deeper understanding of tumor-normal ecosystems and lay the groundwork for future studies in precision oncology."
  - 사용 시나리오: precision oncology 연구에서 이 atlas를 reference로 인용할 때의 근거 문장.
  - BibTeX key: `@kang2024tumornormal`

### 인용 가능 수치

- 4.9M 세포, 30 암종, 1,070 tumor + 493 normal 샘플, 104 datasets, 999 donors (§Abstract, Fig. 1A)
  - 사용 시나리오: atlas 규모를 정량화해 prior work 인용 시.
  - BibTeX key: `@kang2024tumornormal`

- TLS signature 면역치료 반응 예측: OR ≈ 1.3, $p = 1.4 \times 10^{-3}$, $n=1,261$ (Fig. 6C)
  - 사용 시나리오: TLS 또는 interferon community 기반 면역치료 반응 예측 연구의 baseline 수치.
  - BibTeX key: `@kang2024tumornormal`

- TLS vs non-TLS signature score: $p = 1.5 \times 10^{-5}$, $n=17$ RCC samples (Fig. 6B)
  - 사용 시나리오: TLS gene signature의 spatial specificity 인용.
  - BibTeX key: `@kang2024tumornormal`

### 인용 가능 Figure/Table

- Fig. 1A (§Results, p.2~3): 30 암종별 tumor/normal 샘플 구성 원형 차트
  - 무엇을 보여주는지: BRCA, LC, HNSC, HCC 중심의 데이터 분포; tumor/normal 비율
  - 사용 시나리오: 본인 논문의 background에서 pan-cancer atlas 규모를 시각적으로 제시할 때.
  - BibTeX key: `@kang2024tumornormal`

- Fig. 6D (§Results, p.10): TLS-enriched vs. TLS-depleted cell type bar chart
  - 무엇을 보여주는지: Treg, LAMP3⁺ DC, CCL19⁺ fibroblast가 TLS 내 풍부; desmoplastic fibroblast, cancer cell이 TLS에서 희귀
  - 사용 시나리오: TLS 구성 cell type 논의 또는 immunotherapy biomarker 리뷰에서 시각 자료로.
  - BibTeX key: `@kang2024tumornormal`
