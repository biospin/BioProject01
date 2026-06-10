# proszek-2025-adc-ctc-resistance — Academic Lens

> 근거: `sources/proszek-2025-adc-ctc-resistance.pdf` (전문 PDF 기반 분석).

---

## Limitations

### 저자가 명시한 한계

- **Unmatched comparison**: Pre- vs post-T-DXd 샘플이 같은 환자에서 paired로 채취된 것이 아님. 두 집단 간 기저 특성 차이가 mutation 농축 결과를 confound할 수 있음. 저자 명시: "We did not have matched patient samples to examine mutational pressures at the individual patient level and therefore cannot establish causality between T-DXd treatment and the emergence of the identified mutations."
- **ESR1 mutation confounding**: ESR1 mutation 농축이 T-DXd 자체의 선택압이 아닌 내분비 치료 노출 누적의 결과일 수 있음. 저자가 직접 논의에서 언급.
- **ABCC1 발현 조절의 다중 기전**: NFE2L2/KEAP1 mutation이 관찰됐으나, ABCC1 발현 증가와의 연관이 해당 개별 환자에서 통계적으로 유의하지 않았음(power 부족). Post-transcriptional regulation(miRNA 등)도 기여 가능.
- **In vitro mechanistic evidence의 한계**: HER2+ 세포주 2개에만 ABCC1 억제 효과 검증. HER2-low/null 상황이나 다른 세포주에서는 결과가 다를 수 있음(SUM190 세포주에서 일부 불일치).
- **Real-world OS의 한계**: 보험청구 데이터 기반 OS는 표준 임상시험 endpoint가 아님. 치료 중단 이유, PD 여부, OS 이외 endpoint(PFS, ORR) 미제공.

### 분석자가 판단한 한계

- **ABCC1 억제 specificity**: MK-571은 ABCC1 외 ABCC2 등 다른 ABC transporters도 억제하는 pan-ABCC inhibitor. 관찰된 세포독성 증강이 순수하게 ABCC1 억제에 의한 것인지 확인하기 위해서는 ABCC1-selective siRNA 또는 CRISPR knockout 실험이 필요.
  - 왜 중요한가: ABCC1 특이적 기전이 검증돼야 ABCC1 억제가 치료 전략으로 개발될 근거가 생김.
  - 어떤 증거가 부족한가: ABCC1 KO 세포주 또는 shRNA knockdown 실험 부재.

- **SMAD4 mutation 농축 설명 부재**: SMAD4(q<0.0005, 가장 강한 신호)가 post-T-DXd에서 농축되는 이유에 대해 Discussion에서 전혀 언급 없음.
  - 왜 중요한가: SMAD4는 TGF-β/BMP pathway 핵심 tumor suppressor. T-DXd 내성 맥락에서의 역할이 완전히 미설명.
  - 어떤 증거가 부족한가: SMAD4 mutation과 OS 간 연관성 분석, 기전적 설명.

- **HER2 IHC vs RNA 발현 discordance**: HER2-low/null 환자의 20% 이상이 ERBB2 최고발현 quartile(Q4)에 속하는 상황이 발생 가능. RNA 기반 ERBB2와 IHC 기반 HER2 분류 간 불일치에 대한 해석이 부족.
  - 왜 중요한가: 현재 임상에서 T-DXd 처방은 IHC 기반 HER2 분류에 의존하므로, RNA 기반 ERBB2 발현이 독립적 예측력을 가진다면 현 선별 기준의 보완 또는 대안이 될 수 있음.

- **ABCC1 발현의 pre-analytic variability**: FFPE 조직 RNA 기반 TPM은 조직 채취·고정·보관 조건에 민감. ABCC1 RNA와 단백질 상관이 moderate(r=0.4 언급)라는 점은 WTS 기반 biomarker로서의 noise를 반영. 임상 적용을 위해서는 IHC assay 또는 더 robust한 assay 개발 필요.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: 저자는 "ABCC1이 T-DXd 내성의 핵심 efflux pump"라고 주장하지만, NFE2L2/KEAP1 mutation과 ABCC1 발현 변화 간의 연결이 이 코호트에서 통계적으로 입증되지 않았음(저자 직접 인정: "this analysis was not well powered").
  - 현재 논문에서 제시한 근거: NFE2L2 gain-of-function mutation과 KEAP1 loss-of-function mutation이 post-T-DXd에서 농축됨(별개의 두 분석).
  - 더 필요해 보이는 근거: NFE2L2/KEAP1 mutation 보유 환자에서 ABCC1 발현이 실제로 더 높은지 correlation 분석; 이들 환자의 OS가 NFE2L2/KEAP1 wild-type과 다른지 분석.

- **SUM190 세포주 불일치**: SUM190-TDXdR에서 ABCC1 단백질 발현이 parent와 비슷한데도 MK-571 + T-DXd 병용이 T-DXd 단독 대비 유의한 추가 감소를 보임(p<0.0001). 이는 ABCC1 independent 기전의 병용 상승 효과일 수 있어, 논문의 주요 주장(ABCC1-mediated efflux)과 긴장 관계.

### 정리되지 않은 질문

- SMAD4 mutation이 T-DXd 내성에서 어떤 역할을 하는가? TGF-β signaling과 ADC 내성 간의 link?
- ABCC1 발현이 높은 환자에서 T-DXd 이후 2차 치료(항암제 변경 등)의 패턴이 다른가?
- ABCC1 억제를 위한 임상 가능한 전략이 있는가(기존 승인 약물 중 ABCC1 억제 효과 있는 것)?
- HER2 IHC와 ERBB2 RNA 발현의 discordance가 있는 환자군에서 T-DXd 효능은 어느 기준이 더 예측적인가?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: Real-world 2,799명 코호트에서 ABCC1이 HER2와 독립적인 T-DXd 내성 biomarker임을 처음으로 large-scale로 제시. ABCC1-mediated efflux 억제라는 therapeutic hypothesis를 in vitro에서 부분 검증.

- **다음 논문으로 이어질 아이디어**:
  1. **ABCC1 KO + T-DXd 내성 세포 모델**: CRISPR-Cas9으로 ABCC1을 knockout한 T-DXd 내성 세포주를 구성하고 T-DXd 감수성 회복 여부 검증 → ABCC1 특이적 기여도 정량화.
  2. **ABCC1 re-sensitization in HER2-low/null models**: HER2-low 및 HER2-null 세포주에서 ABCC1 억제 + T-DXd 효과 검증 (현 논문은 HER2+ 세포주만).
  3. **NFE2L2/KEAP1 mutation → ABCC1 upregulation → OS 연결 pathway 검증**: 환자 코호트에서 NFE2L2/KEAP1 mutation 보유 vs wild-type에서 ABCC1 발현 차이 + OS 비교 — 지금 논문에서 시도했으나 power 부족으로 미결.
  4. **SMAD4 mutation과 T-DXd 내성의 연결 기전**: TGF-β pathway와 ADC 내성 관계 규명.
  5. **Liquid biopsy 기반 ABCC1 cfRNA 또는 CTC ABCC1 발현 모니터링**: 치료 중 ABCC1 발현 변화를 비침습적으로 추적하는 방법론 개발.

- **설명을 더 매끄럽게 만들 방법**: (1) Matched pre/post-T-DXd 조직 pair 기반 prospective study 설계. (2) ABCC1과 NFE2L2/KEAP1 mutation의 동일 환자 내 연관성 분석 (현 논문은 두 분석이 다른 N을 씀). (3) ABCC1 단백질 발현(IHC)과 RNA 발현(WTS) 간 clinical-grade concordance 연구.

- **우선순위가 높은 후속 실험 / 분석**:
  - 1순위: ABCC1 KO/siRNA knockdown in T-DXd-resistant cell lines → ABCC1 specific contribution to efflux
  - 2순위: SMAD4 mutation functional annotation in T-DXd context
  - 3순위: HER2-low patient-derived organoids 또는 PDX 모델에서 ABCC1 억제 효과 검증

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Results (Abstract): "higher expression of ERBB2 (HER2) and lower expression of ABCC1 (an ATP-binding cassette transporter involved in drug efflux) were significantly associated with longer T-DXd-related overall survival (OS); ABCC1 predicted OS independently of HER2."
  - 사용 시나리오: Introduction에서 T-DXd 내성 기전 중 drug efflux가 임상적으로 유의미함을 인용할 때.
  - BibTeX key: `@sledge2025tdxdresistance`

- §Results (ERBB2 ABCC1): "ABCC1 expression showed no association with HER2 status and remained consistent across all categories (Fig. 3b)"
  - 사용 시나리오: ABCC1이 HER2와 독립적인 별도 biomarker임을 강조하는 근거로.
  - BibTeX key: `@sledge2025tdxdresistance`

- §Discussion: "the combination of reduced HER2 cell surface expression and increased ABCC1-mediated efflux is associated with resistance to T-DXd in metastatic breast cancer"
  - 사용 시나리오: ADC 내성 기전의 pharmacokinetic 모델(uptake vs efflux) 설명 시.
  - BibTeX key: `@sledge2025tdxdresistance`

- §Discussion: "NFE2L2 and KEAP1 mutations represent rational resistance mechanisms for T-DXd through their impact on ABCC1 expression"
  - 사용 시나리오: NFE2L2-KEAP1-ABCC1 axis를 ADC 내성 유전체 맥락에서 인용 시.
  - BibTeX key: `@sledge2025tdxdresistance`

### 인용 가능 수치

- ABCC1 Q4 vs Q1 median OS: 14.2개월 (95% CI 11.8–15.6) vs 22.0개월 (95% CI 17.9–27.3), p<0.0001 (Fig. 2b; N=1,829)
  - 사용 시나리오: ABCC1 고발현 환자의 예후 불량을 수치로 제시할 때.
  - BibTeX key: `@sledge2025tdxdresistance`

- ERBB2 Q4 vs Q1 median OS: 24.9개월 vs 13.2개월, p<0.0001 (Fig. 2c; N=1,714)
  - 사용 시나리오: HER2 발현 수준이 T-DXd 효능의 연속적 예측인자임을 baseline으로 인용.
  - BibTeX key: `@sledge2025tdxdresistance`

- ABCC1 발현 증가: post-T-DXd 중앙값 27 TPM vs pre 22 TPM, p<0.001 (§Results)
  - 사용 시나리오: T-DXd 치료가 ABCC1 발현을 선택적으로 증가시킨다는 근거로.
  - BibTeX key: `@sledge2025tdxdresistance`

### 인용 가능 Figure/Table

- Figure 1 — T-DXd 처리 경로 9단계 모식도 + 내성 기전 개요 + study design
  - 사용 시나리오: 본인 발표에서 ADC 내성 기전 overview 슬라이드에 schema 활용.
  - BibTeX key: `@sledge2025tdxdresistance`

- Figure 4d — ABCC1 × ERBB2 조합 KM curve (최대 OS 분리 27.9 vs 11.2개월)
  - 사용 시나리오: ADC 내성 biomarker combination panel의 임상적 OS 층화 효과를 보여주는 Figure로.
  - BibTeX key: `@sledge2025tdxdresistance`

- Table 1 — T-DXd 치료 코호트 임상 특성 (N=2,799)
  - 사용 시나리오: T-DXd 실세계 코호트의 HER2 status 분포(HER2-null 18%, HER2-low 34% 등) 인용 시.
  - BibTeX key: `@sledge2025tdxdresistance`
