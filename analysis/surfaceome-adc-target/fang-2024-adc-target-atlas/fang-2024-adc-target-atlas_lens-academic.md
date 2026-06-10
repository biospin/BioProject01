# Lens — Academic — fang-2024-adc-target-atlas

## Limitations

#### 저자가 명시한 한계

- **RNA-단백질 불일치 가능성**: 저자는 ERBB2의 경우 일부 암종에서 mRNA-protein Pearson r이 낮음을 직접 언급(Fig. 6b, Discussion). 전사체 기반 발현 추정이 단백질 표면 밀도를 과소/과대 추정할 수 있음을 인정.
- **발현 이질성(heterogeneity)**: 환자 간·환자 내 발현 이질성이 ADC 효과에 영향을 미친다고 언급. 기능 유전체 mRNA 프로파일링으로 부분 보정했으나 완전한 해결책은 아님 (Results §Assembling).
- **내재화(internalization) 이슈**: Discussion에서 ADC 타겟 후보 중 내재화가 매우 빠른 것(예: HER2 double epitope ADC MEDI4276의 high internalization requirement → 과도한 심장 독성)이 오히려 문제가 될 수 있음을 언급. 내재화 속도를 정확히 예측하는 방법이 완전하지 않음.
- **데이터 가용성**: 데이터·코드 모두 "corresponding author on reasonable request"로만 제공 — 완전한 공개 접근 없음.

#### 분석자가 판단한 한계

- **부족한 점 1**: 선별된 75개 타겟 + 165개 target-indication 조합에 대한 *독립적 wet-lab 검증*이 없다. IHC 또는 flow cytometry로 실제 단백질 표면 발현을 확인한 실험이 본문에 없다.
  - 왜 중요한가: ADC 타겟의 결정적 기준은 항체 접근 가능한 표면 단백질 밀도인데, RNA 발현이 이를 완전히 대리하지 못한다. 특히 KCNE4, SLC39A6 같은 transporter/channel은 RNA-protein 상관이 낮을 수 있다.
  - 어떤 증거가 부족한가: 적어도 신규 35개 후보 중 TOP 5~10의 IHC 또는 FACS validation 데이터.

- **부족한 점 2**: 12개 drubability 기준의 가중치가 명시되지 않았다. radar chart 시각화로 제시되어 있으나, 각 축의 상대적 중요도나 통합 점수 산식이 없다.
  - 왜 중요한가: 가중치 없는 종합 점수는 해석자 주관에 의존한다. 예를 들어 internalization이 0.3 가중치인지 0.1인지에 따라 NECTIN4_BLCA와 EGFR_LUAD의 최종 순위가 달라진다.
  - 어떤 증거가 부족한가: 12개 기준의 가중치 산식 또는 expert panel validation.

- **부족한 점 3**: CTC(순환 종양 세포) 맥락 검증이 없다. 이 atlas는 고형암 조직 기반이므로, 혈중을 순환하는 CTC에서의 표면 발현이 조직 발현과 일치하는지 독립적으로 확인되지 않았다.
  - 왜 중요한가: CTC 기반 liquid biopsy 플랫폼(예: CytoGen)에서 ADC 타겟을 발굴할 때 이 atlas를 참조 기준으로 쓰려면, 조직-CTC 발현 일치도 데이터가 필요하다.
  - 어떤 증거가 부족한가: 적어도 일부 타겟에 대한 TCGA(조직) vs. CTC 발현 비교 데이터.

- **부족한 점 4**: 760개 임상시험 데이터는 2022-12-31 기준이며, 이후 승인·종료된 ADC(예: Dato-DXd, patritumab deruxtecan 등)가 포함되지 않았다. 임상 landscape 해석 시 시점 제한 명시가 필요하다.

#### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장 1**: "ADC accumulation이 가장 많은 타겟으로 CD276이 선별됐다"고 언급하나(Results §Differential gene expression), CD276의 정상 조직 발현이 낮지 않음에도 왜 최종 165개 조합에 남아있는지 명확히 설명하지 않는다. 이후 논문에서 CD276-ADC(예: ifinatamab deruxtecan)가 임상 진입한 맥락과 연결이 필요.
  - 현재 논문에서 제시한 근거: CD276은 many target-indication 조합에서 가장 높은 ADC accumulation을 나타낸다고 언급. 단 정상 조직 발현 이슈를 fully 해결하지 않고 별도 논의로 미룸.
  - 더 필요해 보이는 근거: CD276의 ADC-specific 독성 임상 데이터와 알고리즘 점수의 상관 분석.

- **연결이 약한 주장 2**: 기능 유전체 mRNA 프로파일링으로 "단백질 과발현율"을 예측했다고 주장하나, 이 예측이 실제 IHC-based protein overexpression rate와 일치하는지 검증한 데이터가 본문에 없다.
  - 현재 근거: ref.24(Perna et al. 2017, Cancer Cell)의 방법론을 차용. 검증은 reference 논문에 있다고 가정.
  - 더 필요한 근거: 본 atlas의 예측 과발현율 vs. 실제 IHC 결과의 concordance analysis (최소 2~3 타겟).

#### 정리되지 않은 질문

- 질문 1: 75개 최종 타겟 중 35개 "신규(previously unreported)" 후보의 명단이 본문에 명시되지 않음. Supplementary Table 4에서만 확인 가능. 이 35개가 어떤 기준으로 "ADC R&D에서 보고되지 않은" 것으로 분류됐는지 기준이 불분명.
- 질문 2: 병리 stage별 발현 변화 분석(Fig. 4c)에서 stage IV 데이터가 있는 암종이 제한적. 전이성 환자에서의 타겟 발현이 초기 stage와 다를 경우 ADC 적응 범위가 달라진다.
- 질문 3: RTK/RAS/MAP-Kinase pathway의 receptor tyrosine kinase 중 ERBB2, ERBB3, EGFR, FGFR3, MET가 선별 목록에 있음(Supplementary Figure 7). 이들 oncogene의 이중 용도(ADC 타겟 + targeted therapy 타겟)에서 발생하는 내성 기전이 ADC 효과에 어떤 영향을 주는지는 이 논문의 범위 밖.

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 개별 타겟 중심의 ADC 개발 역사에서 벗어나, 범-암종 체계적 surfaceome atlas를 통해 75개 후보 + 165개 target-indication 조합을 제시한 것. 특히 35개 신규 후보는 기존 R&D에서 간과된 타겟 풀을 확장하는 가치가 있다.
- **다음 논문으로 이어질 아이디어**:
  - VCAM1, HAVCR1, CA9, UPK1B 등 과발현율이 높은 신규 후보 대상 ADC linker-payload 최적화 연구.
  - 75개 타겟의 IHC + FACS 기반 단백질 표면 발현 밀도 systematic validation.
  - 이 atlas에서 선별된 타겟 중 암 줄기세포(CSC) 특이 발현 타겟(LGR5, EGFR, ERBB2, CSF1R, MET, IGF1R, TPBG)에 대한 ADC + 화학요법 병용 전략.
  - CTC에서의 surfaceome 발현 atlas 구축 (조직 atlas 대응).
- **설명을 매끄럽게 만들 방법**: CD276의 알고리즘 점수와 정상 조직 발현 사이의 tradeoff를 명시적으로 설명하고, 최종 선별에서 어떤 가중치로 살아남았는지 공개.
- **우선순위가 높은 후속 실험 / 분석**:
  - Supplementary Table 4의 165개 조합 중 STAD(위암) + BRCA(유방암) subset의 과발현율 데이터 추출 → CytoGen CTC 발현 데이터와 비교.
  - ERBB2_BRCA, TROP2_BRCA, HER3(ERBB3)_BRCA 세 타겟의 radar chart 12개 기준 점수를 비교하여 병용 ADC 전략 근거 구성.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction: "an optimal ADC should encompass three essential components: 1) a mAb with high specificity for an antigen, whether homogeneous or heterogeneous, that is overexpressed in tumors; 2) a linker that maintains stability in the bloodstream but can readily cleave at target sites; 3) a warhead with high sensitivity for specific indications."
  - 사용 시나리오: ADC 개발 overview 섹션에서 ADC 구성 요소를 소개할 때.
  - BibTeX key: `@fang2023adctargetatlas`

- §Introduction: "since most antigens are tumor-associated rather than tumor-specific, on-target off-tumor toxicity becomes inevitable."
  - 사용 시나리오: ADC 독성 리스크 섹션에서 on-target off-tumor 독성의 일반적 문제를 서술할 때.
  - BibTeX key: `@fang2023adctargetatlas`

- §Results (Assembling): "starting from 20,242 HUGO gene symbols across 19 solid cancer types, our algorithm identified 75 candidate antigens with features potentially suitable for ADC targeting and their 165 target-indication combinations."
  - 사용 시나리오: ADC 타겟 발굴 방법론을 인용하거나 신규 후보 규모를 제시할 때.
  - BibTeX key: `@fang2023adctargetatlas`

- §Discussion: "the extensive landscape of ADC targets compiled herein serves as a valuable resource for cancer researchers, clinical oncologists, and the wider scientific and pharmaceutical community invested in the rapidly evolving field of ADC oncology therapeutics for solid cancers."
  - 사용 시나리오: 논문의 clinical relevance를 강조하는 결론 섹션에서.
  - BibTeX key: `@fang2023adctargetatlas`

### 인용 가능 수치

- 75개 unique ADC 타겟 + 165개 target-indication 조합, 35개 신규 후보 (§Results, Supplementary Table 4)
  - 사용 시나리오: pan-cancer ADC target landscape 규모 제시 시. 예: "Fang et al. (2023)는 19개 고형암종에서 75개 ADC 타겟 후보를 체계적으로 도출했으며…"
  - BibTeX key: `@fang2023adctargetatlas`

- 159개 ADC 확인, 72개 고형암 개입 평가 중 (36개 unique 타겟), BRCA n_ADC = 28 (§Results, Supplementary Table 2)
  - 사용 시나리오: ADC 임상 landscape 현황 인용 시.
  - BibTeX key: `@fang2023adctargetatlas`

- DS-8201(trastuzumab deruxtecan): HER2+ mBC에서 ORR 60.9%, DCR 97.3% (§Introduction, ref.5 재인용)
  - 사용 시나리오: HER2-ADC 임상 효과의 representative data로 인용 시.
  - 주의: 이 수치는 ref.5 (Modi et al. 2020, NEJM)의 재인용. 직접 인용은 원 저자 논문으로.

### 인용 가능 Figure/Table

- Figure 1a — 19개 암종 × 36개 타겟의 log₂FC heatmap + 32개 정상 조직 단백질 발현 수준
  - 무엇을 보여주는지: 현재 임상 ADC 타겟의 종양 선택성과 정상 조직 안전성 프로파일 전체 조망.
  - 사용 시나리오: ADC 타겟 선택의 복잡성 및 on-target off-tumor 독성 리스크를 시각화할 때.
  - BibTeX key: `@fang2023adctargetatlas`

- Figure 5 — 예측 단백질 과발현율 dot plot (75개 타겟 × 22개 tumor subtype)
  - 무엇을 보여주는지: 신규 ADC 타겟 후보들의 암종별 예측 과발현율 landscape.
  - 사용 시나리오: 신규 ADC 타겟 발굴 pipeline의 output을 보여줄 때 또는 BRCA subtype별 과발현율 비교 시.
  - BibTeX key: `@fang2023adctargetatlas`

- Figure 6c,d — ERBB2_BRCA 외 대표 타겟의 12개 기준 radar chart
  - 무엇을 보여주는지: ADC 타겟 드러거빌리티의 다차원 평가 방법론 시각화.
  - 사용 시나리오: ADC 타겟 평가 framework 소개 slide에서.
  - BibTeX key: `@fang2023adctargetatlas`
