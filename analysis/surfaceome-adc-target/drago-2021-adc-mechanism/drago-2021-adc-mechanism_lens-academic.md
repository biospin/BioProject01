# Lens — Academic: drago-2021-adc-mechanism

## Limitations

### 저자가 명시한 한계

- **내성 기전의 임상 미확인**: Figure 3와 §Resistance 섹션에서 제시한 3대 내성 카테고리(항원 downregulation, intracellular trafficking 변화, ABC efflux)는 "supported largely by in vitro evidence but have not yet been confirmed in patients with cancer"라고 저자가 직접 명시.
- **ADC-TME 상호작용의 불완전한 이해**: bystander effect, extracellular payload release, Fc-mediated immune activation의 임상 기여 비중이 대부분 ADC에서 poorly characterized라고 인정(Fig. 2 caption).
- **예측 바이오마커 부재**: 환자 선택을 개선할 예측 바이오마커의 필요성을 강조하지만, IHC 기반 정량의 한계(semi-quantitative, cut-off 불명확)를 인정하며 해결책을 제시하지 않음.
- **병용 임상 근거 미성숙**: Fig. 4에서 제시한 병용 전략 4가지는 대부분 preclinical 또는 early phase 수준. KATE2 trial(T-DM1 + atezolizumab)에서 병용 효과 미확인.
- **ADC 약동학 모델의 복잡성**: PK/PD 모델링 시도들이 유망하지만 더 많은 검증이 필요하다고 인정(§How ADCs work in vivo).

### 분석자가 판단한 한계

**① ADC 간 직접 비교의 부재**
- 부족한 점: 9종 ADC의 임상 결과를 나란히 제시하지만, cross-trial 비교의 한계(환자 선택, 선행치료 종류·수, 측정 방법 차이)를 해당 섹션에서 충분히 다루지 않는다. 독자가 ORR 수치를 직접 비교하도록 유도하는 구조.
- 왜 중요한가: 동일 타겟에서 다른 payload를 쓴 ADC(T-DM1 vs T-DXd)의 우열을 논할 때 선행치료 이질성이 교란 변수로 작동하므로, ADC design 차이가 만드는 실제 효능 차이를 과대평가할 수 있다.
- 어떤 증거가 부족한가: 같은 환자군에서 head-to-head trial 데이터 또는 최소한 matched cohort 분석.

**② Fc 기능의 실제 ADC 활성 기여도**
- 부족한 점: §How ADCs work in vivo에서 Fc-mediated ADCC/ADCP가 ADC 활성에 기여할 수 있다고 논의하지만, payload delivery와 Fc 기능 각각의 상대적 기여를 분리한 실험 데이터가 없다.
- 왜 중요한가: Fc-silenced ADC variant와 wild-type Fc ADC를 같은 환자 조건에서 비교한 데이터 없이 Fc 기능을 "important contributor"로 서술하면 설계 원칙 오도 가능.
- 어떤 증거가 부족한가: Fc engineering 비교 임상 또는 전임상 paired experiment.

**③ DAR과 hydrophobicity가 치료 지수에 미치는 영향의 단순화**
- 부족한 점: 고DAR → 간 clearance 증가 → 치료 지수 악화라는 논리를 제시하지만, payload hydrophobicity를 보정하면 고DAR도 안전하다는 증거(sacituzumab govitecan, DAR 8)가 병행해 등장한다. 두 결론이 충분히 통합되지 않고 나란히 서술된다.
- 해석: DAR의 임상적 최적값은 payload class·linker type·antibody 특성의 함수이며, 단순한 수치 권고로는 설계 원칙을 전달하기 어렵다.

**④ 내성 기전의 교차 검증 미흡**
- 부족한 점: ABC transporter efflux, lysosomal dysfunction, antigen loss를 별개의 카테고리로 제시하지만, 실제 내성 암세포에서 이 메커니즘들이 어느 비중으로 동시 발생하는지 분석한 멀티플렉스 데이터 없음.
- 왜 중요한가: 내성 극복 전략(ABC transporter 억제, lysosome acidification 복원 등)을 선택할 때 dominant mechanism을 알아야 하는데, 현 데이터로는 환자별 dominant mechanism 예측 불가.

### 설명이 매끄럽지 않은 지점

**[1] HER2 발현 수준과 T-DXd 반응 관계**
- 연결이 약한 주장: T-DXd가 HER2 역치 이하 발현 유방암에서도 activity를 보인다(early signs)는 관찰에서 저자는 "bystander effect 덕분일 수 있다"고 해석. 그러나 T-DXd의 high DAR(8)과 membrane-permeable DXd의 bystander potential이 각각 어느 정도인지는 미분리.
- 현재 논문 근거: Trastuzumab duocarmazine의 HER2 역치 이하 활성 언급 및 T-DXd DAR 8 + cleavable linker 특성.
- 더 필요해 보이는 근거: HER2 IHC 0~1+ 환자에서 T-DXd 활성의 전향적 확인 (→ 실제로 이후 DESTINY-Breast06 trial에서 확인됨. 외부 맥락으로 병기 필요).

**[2] Sacituzumab govitecan의 irinotecan-compared activity**
- 연결이 약한 주장: T-DXd가 irinotecan에 내성인 위암에서 ORR 41.7%를 보인다는 관찰을 "payload를 ADC로 전달하면 약물내성 극복 가능"의 근거로 쓴다.
- 현재 논문 근거: Single phase II trial (irinotecan 선행치료 후 T-DXd).
- 더 필요해 보이는 근거: 같은 환자에서 irinotecan monotherapy ORR과 T-DXd ORR의 direct comparison, 또는 irinotecan 치료 전·후 TOPO1 발현/활성 변화.

**[3] Bystander effect의 이중성**
- 연결이 약한 주장: Bystander effect가 "중요한 기여 인자"라고 하지만, 같은 단락에서 정상 조직 비표적 세포의 독성 위험도 언급한다. 둘 중 어떤 상황에서 bystander가 net benefit인지 규칙을 제시하지 않는다.
- 더 필요해 보이는 근거: 동물 모델에서 antigen-heterogeneous tumor vs. 정상 조직에서 bystander killing quantification.

### 정리되지 않은 질문

- **질문**: 같은 HER2 타겟 항체(trastuzumab)를 쓰면서 linker-payload가 다른 T-DM1 vs T-DXd에서 내성 프로파일이 어떻게 다른가? PIK3CA 돌연변이가 T-DM1 내성과 uncorrelated라면 T-DXd는 어떠한가?
- **질문**: TME hypoxia가 bystander effect와 linker cleavage에 미치는 영향이 ADC마다 다른가? TME 조건을 사전에 측정해 ADC 선택을 최적화할 수 있는가?
- **질문**: ADC-면역요법 병용에서 ADCC/ADCP를 통한 면역 활성화가 PD-L1/PD-1 차단과 실제로 시너지를 내는지, 아니면 면역 고갈(exhaustion) 위험이 있는지?
- **질문**: 비항체 backbone(peptide fragment, diabody, PEN-221 peptide conjugate)이 ADC와 경쟁할 조건은 무엇인가? tumor penetration 이점이 systemic PK 불이익을 상쇄하는 조건?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: ADC 설계의 3요소 프레임워크(항체·링커·payload)와 in vivo 기전을 체계적으로 통합한 현장 표준 리뷰. 2021년 이후 ADC 관련 논문에서 가장 많이 인용되는 review 중 하나. 타겟 선정, 링커 선택, 독성 예측, 내성 기전 분류의 사실상 교과서 역할.
- **다음 논문으로 이어질 아이디어**:
  - ADC 타겟 단백질의 surfaceome proteomics와 internalization kinetics를 통합한 "ADC targetability score" 개발. 각 단백질의 발현 수준, 세포막 밀도, 내재화율, turnover를 정량화해 타겟 우선순위 자동화.
  - Longitudinal biopsy에서 ADC 내성 발생 시점의 multi-omic profiling — 항원 발현, ABC transporter, lysosomal pH를 동시 측정하는 멀티플렉스 어세이 개발.
  - HER2 IHC 0~1+ 환자에서 T-DXd 활성의 molecular correlate 규명 — bystander DXd에 노출되는 HER2 음성 세포의 TOPO1 발현·DNA repair 상태가 핵심 변수일 것.
- **설명을 더 매끄럽게 만들 방법**:
  - DAR-efficacy-toxicity의 3방향 관계를 payload hydrophobicity 및 linker type과 함께 통합 도식화(현재는 따로 논의).
  - 내성 3카테고리를 환자별 dominant mechanism으로 구분하는 biomarker 전략을 별도 섹션으로 추가.
- **우선순위가 높은 후속 실험 / 분석**:
  - Patient-derived organoid(PDO) 또는 patient-derived xenograft(PDX)를 이용한 ADC 내성 발생 시뮬레이션 — 3개 내성 카테고리 동시 모니터링.
  - HER2 표적 ADC 수신자(T-DM1 경험 후 T-DXd 투여) 코호트에서 순차 내성 메커니즘의 단일세포 분석.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Abstract: "The efficacy of a given ADC depends on the intricacies of how the antibody, linker and payload components interact with the tumour and its microenvironment…"
  - 사용 시나리오: ADC 설계의 복잡성을 서론에서 동기화할 때. surfaceome-adc-target 분석의 배경 설명.
  - BibTeX key: `@drago2021adcmechanism`

- §Antibody and target selection: "targets that are functionally oncogenic, as opposed to simply being present on the surface of cancer cells, are less subject to downregulation…"
  - 사용 시나리오: 타겟 우선순위 선정 기준 논의. 기능적 oncogenic driver가 downregulation에 덜 취약하다는 설계 원칙 인용.
  - BibTeX key: `@drago2021adcmechanism`

- §How ADCs work in vivo: "only a fraction of a percent of the administered ADC dose actually reaches tumour cells"
  - 사용 시나리오: ADC 전달 효율의 한계를 근거로 고효능 payload 또는 개선된 전달 전략의 필요성을 도입할 때.
  - BibTeX key: `@drago2021adcmechanism`

- §Resistance: "acquired resistance to ADCs seems to be more complicated and multifactorial, reflecting the general mechanistic complexity of this drug class"
  - 사용 시나리오: 내성 예측 바이오마커 개발의 어려움을 서론에서 설명할 때.
  - BibTeX key: `@drago2021adcmechanism`

- §Conclusions: "Models positing straightforward target-dependent payload delivery might be oversimplified and require revision to account for the mechanistic complexity of ADC action…"
  - 사용 시나리오: 차세대 ADC 기전 연구의 필요성 또는 TME-aware ADC design 제안 논문의 motivation.
  - BibTeX key: `@drago2021adcmechanism`

### 인용 가능 수치

- T-DXd ORR 60.9% (전이성 HER2+ 유방암, ≥2 HER2 기반 요법 후) (§Activity in treatment-refractory cancers)
  - 사용 시나리오: next-gen ADC의 임상 효능 baseline 수치로 인용.
  - BibTeX key: `@drago2021adcmechanism`

- Enfortumab vedotin ORR 44% vs. taxane 단독 ORR 10.5% (요로상피암, 백금+ICI 실패 후) (§Activity)
  - 사용 시나리오: ADC가 standard chemotherapy 대비 superiority를 보이는 대표 수치.
  - BibTeX key: `@drago2021adcmechanism`

- T-DM1 초기 유방암 잔존 병변: 재발/사망 위험 50% 감소 (§Activity)
  - 사용 시나리오: ADC가 adjuvant setting에서도 효능을 보이는 근거.
  - BibTeX key: `@drago2021adcmechanism`

- DAR 8 버전 ADC → 마우스에서 DAR 2 대비 5배 빠른 clearance (§Payloads)
  - 사용 시나리오: 고DAR의 PK 불이익 설명.
  - BibTeX key: `@drago2021adcmechanism`

### 인용 가능 Figure/Table

- **Table 1** — FDA 승인 9종 ADC 통합 표 (타겟·링커·payload·DAR·적응증)
  - 무엇을 보여주는지: 승인 ADC의 설계 파라미터 비교 one-stop reference.
  - 사용 시나리오: ADC 현황 정리 슬라이드, BD 발표 배경 자료.
  - BibTeX key: `@drago2021adcmechanism`

- **Figure 2** — ADC 작용 기전 (6단계 in vivo 경로 도식)
  - 무엇을 보여주는지: 혈관 → 종양 침투 → 항원 결합 → 내재화 → payload 방출 → bystander effect 전 과정.
  - 사용 시나리오: ADC 기전 교육 자료, 발표 배경 슬라이드.
  - BibTeX key: `@drago2021adcmechanism`

- **Figure 3** — ADC 내성 메커니즘 (3카테고리 도식)
  - 무엇을 보여주는지: 항원 loss / intracellular trafficking / payload efflux의 시각화.
  - 사용 시나리오: 내성 극복 전략 논문의 motivation figure.
  - BibTeX key: `@drago2021adcmechanism`
