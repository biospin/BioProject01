# Lens — Academic
# pantel-2019-ctc-review

---

## Limitations

### 저자가 명시한 한계

- **기술 한계**: CTC 및 ctDNA 농도가 비전이성 MRD 단계에서 매우 낮아 현재 ultra-sensitive assay도 충분하지 않을 수 있다. 혈액량(5–10 ml)이 제한 요인으로, 대규모 코호트에서 robust한 결과를 얻기 어렵다(본문 §Considerations for future studies).
- **EMT CTC 누락**: EpCAM 기반 플랫폼(CellSearch 포함)은 EMT를 거친 CTC를 포획하지 못한다. MRD 단계의 CTC는 EMT 빈도가 더 높을 수 있어 시스템 편향 가능성(본문 §Considerations for future studies, §Detection of CTCs).
- **ctDNA clonal haematopoiesis 혼동**: 고감도 assay(특히 CAPP-Seq)는 노화·양성 종양과 연관된 clonal haematopoiesis(CHIP)로 인한 낮은 수준 변이를 false positive로 검출할 수 있다(본문 §Conclusions).
- **코호트 규모 불균형**: ctDNA 연구 코호트(n=20–55)와 CTC 연구 코호트(n=213–3,173)의 불균형. ctDNA 결론의 신뢰 구간이 매우 넓다(Garcia-Murillas HR 25.1, 95% CI 4.08–130.50)(Table 1).
- **pre-analytical 변이**: 혈액 채취부터 처리까지의 pre-analytical 조건(온도·시간·원심분리 프로토콜)이 CTC·ctDNA 측정에 영향. 다기관 임상 연구에서 표준화 부족(본문 §Conclusions).
- **전향적 개입 근거 부재**: 대부분의 임상 연구가 retrospective 또는 prospective observational로, CTC·ctDNA 기반 개입이 실제 환자 outcome을 개선한다는 RCT 증거가 2019년 시점에는 없었다.

### 분석자가 판단한 한계

- **전립선암 데이터의 일관성 부재**: Supplementary Table 1의 9개 조기 전립선암 연구 모두 CTC 예후 의미를 보이지 못했다. 본문 §Clinical MRD studies on CTCs에서 "data more heterogeneous"로 서술하지만, 결국 전립선암에서 CTC가 MRD 대리표지자로 사용될 수 없다는 결론을 명시하지 않는다. 이 점은 저자들이 완화해서 서술한 부분이다.
  - 왜 중요한가: 전립선암은 CTC 기술 개발의 주요 임상 적용처로 논의되지만, 현재 데이터로는 CTC 기반 MRD 추적이 지지되지 않는다.
  - 더 필요한 근거: PSA kinetics나 PSMA PET 대비 CTC의 독립적 예측력을 보여주는 prospective 연구.

- **CTC와 ctDNA의 직접 비교 부재**: 이 리뷰는 두 기술을 "상호 보완적"이라고 기술하지만, 같은 환자·같은 시점에서 두 방법을 동시에 사용한 head-to-head 비교 데이터를 정량화하지 않는다. 어떤 암종·어떤 임상 상황에서 어느 방법이 우선인지 결론을 내리지 못한다.
  - 더 필요한 근거: 동일 코호트 내 CTC와 ctDNA의 concordance·discordance 비율 및 예후 예측력 직접 비교.

- **치료 표적 정보의 임상 검증 수준 불균일성**: Figure 3은 EGFR(FDA 승인 검사 존재), AR-V7(임상 연구 단계), BRAF(소규모 연구)를 같은 도식에 나열한다. 각 바이오마커의 LOE(Level of Evidence)를 구분하지 않아 독자가 오판할 수 있다.

- **혈중 반감기 1.0–2.4시간의 해석 문제**: 전립선 수술 3개월 후 CTC가 여전히 검출된다는 데이터를 근거로 저자는 "clinically occult lesion에서 유래한다"고 해석하지만, 이는 직접 실험적 검증이 아닌 추론이다.

### 설명이 매끄럽지 않은 지점

- **연관 vs. 인과**: 이 리뷰 전체에서 CTC/ctDNA 양성과 불량 예후의 "연관"이 "CTC가 MRD를 유발한다"는 방향으로 서술되는 경향이 있다. 그러나 CTC 수가 높다는 것이 종양 부하의 반영일 뿐 MRD 자체의 원인이 아닐 수 있다. Causal claim과 biomarker claim을 더 명확히 분리해야 했다.

- **Cancer dormancy section(Box 1)**: dormancy의 분자적 기전이 "under investigation"으로 처리되어 있어, 왜 MRD 감시가 기술적으로 가능한지에 대한 메커니즘적 연결이 약하다. MRD → dormancy → reactivation 경로에 대한 생물학적 근거가 보강된다면 리뷰의 논리가 더 탄탄해진다.

- **PDX 모델의 한계 서술**: CTC로부터의 PDX 성공률이 "generally very low"이고 "generally >1,000 CTCs from patients with breast cancer"가 필요하다고 언급하지만, 이 한계를 극복하기 위한 구체적 전략이 제시되지 않는다.

### 정리되지 않은 질문

- 질문: MRD 감시에 최적화된 CTC assay는 무엇인가? EpCAM 독립 기술(EPISPOT, size-based) vs. CellSearch의 민감도·특이도를 head-to-head로 평가한 대규모 연구가 필요하다.
- 질문: ctDNA의 clonal haematopoiesis 혼동 문제를 어떻게 통제할 것인가? 특히 CAPP-Seq를 고령 암 환자에게 적용할 때 false positive 비율의 정량적 평가가 필요하다.
- 질문: c-TRAK TN(NCT03145961) 등 ctDNA-triggered 치료 임상시험의 결과가 나왔는가? 리뷰가 예측한 "조기 개입 window"가 실제 OS 이익으로 연결되는지는 2019년 이후 데이터로 판단해야 한다.
- 질문: 이 리뷰가 언급하지 않은 CTC cluster(circulating tumour microemboli)의 역할 — CTC cluster는 단일 CTC보다 전이 능력이 높다는 증거가 있으나(본문 §Enrichment에서 짧게 언급), MRD 맥락에서의 임상 의의가 미서술.

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 2014–2018년 사이 집적된 유방암·CRC·폐암 CTC·ctDNA 예후 데이터를 처음으로 MRD라는 개념 아래 통합한 landmark 리뷰. Pantel과 Alix-Panabières는 각자 CTC와 ctDNA 분야의 최선두 연구자로, 이 통합 시각 자체가 이후 MRD 임상시험 설계의 프레임으로 작용했다.

- **다음 논문으로 이어질 아이디어**:
  1. CTC vs. ctDNA head-to-head MRD 예측력 비교 — 동일 유방암·CRC 코호트에서 두 방법을 동시 시행하고, 어느 방법이 먼저 재발을 예측하는지 OS endpoint 무작위 시험.
  2. EMT spectrum을 반영하는 CTC 포획 방법(EpCAM 독립) 대규모 검증 — 특히 MRD 단계에서 EMT 정도가 전이 단계보다 큰지 단일세포 표현형 분석.
  3. ctDNA clonal haematopoiesis 교정 알고리즘 개발 — 고령 MRD 환자에서 false positive를 줄이는 백혈구 DNA matched sequencing 방법론 표준화.
  4. ADC 표적으로서 CTC 표면 항원 프로파일링 — EPCAM·HER2·PSMA 외 MRD CTC에서 우선 발현되는 신규 표면 표적 발굴. ADC payload delivery 관점에서 MRD CTC의 ADC 감수성 평가.

- **설명을 더 매끄럽게 만들 방법**: cancer dormancy 메커니즘(특히 immune surveillance와의 관계)을 CTC/ctDNA 검출 감도의 biological limit과 연결해 서술하면, 기술적 한계와 생물학적 한계를 독자가 명확히 구분할 수 있었을 것.

- **우선순위가 높은 후속 실험 / 분석**:
  - ctDNA-triggered 개입 RCT(c-TRAK TN 결과 검토 → 2022–2023 결과 논문 탐색)
  - CTC 표면 단백질체(surfaceome) 단일세포 수준 분석 — MRD CTC에서 ADC 표적 발현 평가

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction: "a considerable fraction of patients with seemingly successful treatment of early stage cancer have occult micrometastases or minimal residual disease (MRD) that persists after initial therapy as a potential source of subsequent metastatic relapse at distant sites."
  - 사용 시나리오: ADC 또는 liquid biopsy 관련 제안서의 introduction에서 MRD 문제의 임상적 중요성을 정당화할 때. BibTeX key: `@pantel2019ctcreview`

- §Detection of CTCs (EMT): "CTCs are phenotypically very heterogeneous and might not express the chosen marker; therefore, positive selection might introduce a bias that can be avoided by negative selection"
  - 사용 시나리오: CTC 포획 기술 한계를 기술할 때, 특히 EpCAM 독립 포획 방법의 필요성을 justify할 때. BibTeX key: `@pantel2019ctcreview`

- §Therapeutic targets: "the choice of the most appropriate form of liquid biopsy analysis depends on the drug target, although ctDNA and CTCs can provide complementary information"
  - 사용 시나리오: CTC vs ctDNA 상보성 논거, ADC 표적 추적 관련 발표에서. BibTeX key: `@pantel2019ctcreview`

### 인용 가능 수치

- Rack et al. (2014): CTC 양성 DFS HR 2.11(95% CI 1.49–2.99, p<0.0001), OS HR 2.18(95% CI 1.32–3.59, p=0.002) — n=2,090 유방암(Table 1, §Clinical MRD studies on CTCs)
  - 사용 시나리오: CTC의 독립 예후 인자 근거로 본인 제안서·논문의 CTC biomarker 타당성 섹션에서. BibTeX key: `@pantel2019ctcreview`

- Garcia-Murillas et al. (2015): ctDNA 재발 선행 검출 평균 7.9개월(Table 1, §Clinical MRD studies on ctDNA)
  - 사용 시나리오: ctDNA가 영상 대비 재발을 얼마나 일찍 잡는지 수치를 요구할 때. BibTeX key: `@pantel2019ctcreview`

- Tie et al. (2016): 수술 후 CRC-ctDNA HR 18.0(95% CI 7.9–40.0, p<0.001) — stage II 대장암(§Clinical MRD studies on ctDNA)
  - 사용 시나리오: ctDNA의 예후 예측력을 단일 수치로 강조할 때. BibTeX key: `@pantel2019ctcreview`

### 인용 가능 Figure/Table

- Figure 2 (§Methods of ctDNA detection)
  - ctDNA 농도 범위와 assay sensitivity를 병기별로 정리한 schematic. 비전이성 MRD 단계에서 targeted 고감도 assay가 필요함을 한 Figure로 설명.
  - 사용 시나리오: 연구 제안서나 학회 발표에서 "왜 MRD에서 ctDNA 검출이 어려운가"를 시각화할 때. BibTeX key: `@pantel2019ctcreview`

- Table 1 (§Clinical MRD studies)
  - 유방암 CTC·ctDNA 연구 7편의 HR·p-value·CI를 표로 제공. 본인 논문의 related work table 작성 시 구조 참조 가능.
  - 사용 시나리오: liquid biopsy MRD 분야 리뷰 논문·제안서의 관련 연구 요약 테이블. BibTeX key: `@pantel2019ctcreview`
