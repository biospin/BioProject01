# Lens — Academic
## xie-2024-her2-ctc-concordance

---

### Limitations

#### 저자가 명시한 한계
- 소규모 샘플 사이즈(n=43)로 인한 편향 가능성. 저자 스스로 결론부에서 "small sample size may introduce biases" 언급.
- 향후 대규모·엄격 설계 임상 시험 필요성을 명시.
- 표준화된 HER2⁺CTC 검출 방법의 부재 — 방법 차이가 HER2 downgrading에 기여할 수 있다고 인정.

#### 분석자가 판단한 한계

**한계 1 — CTC 미검출 환자 제외에 따른 selection bias**
- 부족한 점: 60명 스크리닝 중 17명(28.3%)이 CTC 0으로 제외됐으나 이 환자들의 조직 HER2 분포, 병기, 치료력 미제공.
- 왜 중요한가: 만약 CTC 미검출군이 특정 HER2 상태 또는 병기에 편중되어 있다면, 불일치율 32.6%는 CTC 검출 가능 환자에 한정된 추정값이다. 전체 유방암 환자에서의 불일치율 외삽이 과대 또는 과소 추정될 수 있음.
- 어떤 증거가 부족한가: CTC 미검출 17명의 임상 특성 표 또는 검출 실패 원인 분석.

**한계 2 — 다중 비교 보정 미시행**
- 부족한 점: Figure 4의 e, f, g 세 가지 Mann-Whitney 검정, 그리고 Spearman 상관 2개(c, d) 등 다수의 가설 검정을 보정 없이 수행.
- 왜 중요한가: p = 0.0106–0.0387 범위의 유의 결과들이 BH correction 후 유의성을 유지할지 불확실. Ki67 상관(p=0.011), ER/PR 연관(p=0.0132)이 false positive일 가능성 배제 불가.
- 어떤 증거가 부족한가: FDR 보정된 q-value 제공, 또는 permutation 기반 검정.

**한계 3 — 조직 생검-혈액 채취 시간차 통제 부재**
- 부족한 점: 조직 HER2 결과는 1년 이내 생검 기준이나, 생검과 혈액 채취 사이의 정확한 시간 간격이 환자별로 미제공. 치료 이력(화학요법, 방사선 등)에 따라 HER2 상태가 변할 수 있음.
- 왜 중요한가: 불일치의 일부는 생물학적 진화가 아니라 시간차·치료 효과일 수 있음. 두 원인을 분리하는 분석 없음.
- 어떤 증거가 부족한가: 생검-혈액 채취 시간 간격별 불일치율 층화 분석.

**한계 4 — kappa 95% CI 미제공**
- 부족한 점: kappa = 0.325, p = 0.030만 보고. n=43의 2×2 표에서 kappa의 표준오차가 상당히 클 수 있음.
- 왜 중요한가: kappa 95% CI가 넓으면 fair-to-moderate 전 구간에 걸쳐 불확실성이 크다는 의미. "significant discordance"의 강도 판단 어려움.
- 어떤 증거가 부족한가: bootstrapped 또는 asymptotic kappa 95% CI.

**한계 5 — IHC 1⁺군에서 cHER2⁺ 비율 역설적 패턴 미설명**
- 부족한 점: IHC 1⁺ 환자 11명 중 54.5% (6명)가 cHER2⁺로, IHC 2⁺FISH⁻(16.7%, 2/12)보다 오히려 높음. 이 패턴은 본문에서 충분히 논의되지 않음.
- 왜 중요한가: IHC 점수 순서(0 < 1+ < 2+ < 3+)와 역전되는 결과는 검출 방법의 비특이적 반응이나 소표본 우연 변이 또는 IHC 1⁺ 카테고리 자체의 이질성을 반영할 수 있음.
- 어떤 증거가 부족한가: IHC 하위그룹별 충분한 표본 + FISH 재확인 + HER2 단백 발현의 정량 IHC (H-score).

#### 설명이 매끄럽지 않은 지점

**연결 1 — TERT⁺ WBC false positive 위험**
- 연결이 약한 주장: TBCD가 WBC를 효과적으로 배제해 HER2+CTC를 정확히 검출한다.
- 현재 논문에서 제시한 근거: Figure 2e에서 TERT⁺ WBC(CD45⁺/GFP⁺) 소집단 존재 확인, CD45 gate로 배제.
- 더 필요해 보이는 근거: 건강 공여자 혈액으로 수행한 specificity 실험 (CTC 0인 정상인 샘플의 false positive rate 정량화). 임상 샘플에서 TERT⁺ WBC의 빈도와 CD45 발현 분포 상세.

**연결 2 — HER2+CTC 임상 의의 비약**
- 연결이 약한 주장: HER2+CTC가 HER2 표적 치료 가이드에 잠재적 가치를 가진다.
- 현재 논문에서 제시한 근거: 불일치율 통계 + Fehm et al.(lapatinib DETECT III), Wang et al.(Pep@MNPs) 등 외부 연구 인용.
- 더 필요해 보이는 근거: 본 코호트에서 hHER2⁻/cHER2⁺ 환자(n=9)가 HER2 표적 치료 후 반응률 데이터. 현재 논문은 치료 반응을 전혀 추적하지 않음.

#### 정리되지 않은 질문

- 질문 1: CTC가 검출되지 않은 17명과 검출된 43명 사이에 임상 특성(병기, HER2 상태, 치료력) 차이가 있는가?
- 질문 2: 방사선 치료 이전 혈액 채취라고 명시됐으나, 이전 화학요법·내분비 치료력이 HER2+CTC 검출에 어떤 영향을 주는가?
- 질문 3: IHC 1⁺군의 높은 cHER2⁺ 비율이 TBCD 플랫폼의 특이적 한계(특정 HER2 발현 수준에서 항체 염색 위양성)인가, 아니면 실제 생물학적 현상인가?
- 질문 4: 동일 환자에서 종단(longitudinal) 측정 시 HER2+CTC 수치가 치료 반응과 연동하는가?

---

## Final Takeaways

- **이 논문의 가장 큰 의미**: 조직 HER2⁻ 판정을 받은 유방암 환자의 32.1%에서 혈중 HER2+CTC가 검출됐다는 직접 수치 근거 제공. T-DXd 등 ADC의 HER2-low 적응증 확장 흐름 속에서 CTC 기반 재프로파일링의 임상 필요성을 지지하는 데이터.

- **다음 논문으로 이어질 아이디어**:
  1. **종단 코호트 연구**: 동일 유방암 환자를 치료 전-중-후 3시점에 혈액 채취 → HER2+CTC 수치 추이 vs. 방사선/항암 치료 반응 연동 분석. 목표: CTC HER2를 dynamic biomarker로 검증.
  2. **hHER2⁻/cHER2⁺ 환자 임상 시험**: n=9는 너무 작음. 100명 이상 규모로 hHER2⁻/cHER2⁺ 환자에게 T-DXd 또는 lapatinib을 투여 후 ORR/PFS 비교. DETECT III 디자인 참조.
  3. **TBCD specificity 검증 연구**: 정상 공여자(n≥30) + 비암성 질환 환자(n≥30) 혈액에서 TBCD 위양성률 정량화. 현재 논문의 가장 큰 방법론적 공백.
  4. **IHC subgroup 재분류**: ASCO 2023 HER2-low (IHC 1⁺, IHC 2⁺FISH⁻) 정의에 따른 CTC HER2 불일치율 재분석. T-DXd 임상 적용과 직결.
  5. **멀티오믹스 확장**: HER2+CTC에서 single-cell RNA-seq 또는 CTC WES로 HER2 amplification 유무 및 기타 driver mutation 프로파일. 불일치의 생물학적 메커니즘(heterogeneity vs. plasticity) 구분.

- **설명을 더 매끄럽게 만들 방법**: 조직-CTC 불일치의 원인을 (a) 종양 내 이질성, (b) 시간적 HER2 변화, (c) 기술적 오류 세 가지로 나눠 각각에 대한 증거를 별도 분석으로 제시하면 주장이 훨씬 설득력 있음. 현재 논문은 이 세 원인을 구분하지 않음.

- **우선순위가 높은 후속 실험 / 분석**:
  1. [높음] TBCD specificity — 건강 공여자 혈액에서 false positive rate 측정.
  2. [높음] 종단 HER2+CTC 추적 — 치료 반응 biomarker 검증.
  3. [중간] kappa 95% CI 재계산 및 다중 비교 보정된 p-value 보고 (기존 데이터 재분석으로 가능).
  4. [중간] 대규모 multicenter cohort (n≥200) 불일치율 재현.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction: "Many studies have shown that HER2-negative breast cancer patients can also benefit from HER2-targeted therapy, especially HER2-targeted ADCs, which means that a large proportion of breast cancer patients who can finally benefit from HER2-targeted treatment strategies are neglected."
  - 사용 시나리오: CTC HER2 재프로파일링의 임상 필요성을 도입부에서 정당화할 때. ADC 연구 제안서 introduction에서 기존 IHC 기반 선택의 한계를 지적할 때.
  - BibTeX key: `@xie2024her2ctcconcordance`

- §Results 3.3: "Discordance in HER2 status between primary tumor and CTC was observed in 32.6% of patients (kappa value = 0.325, p = 0.030)."
  - 사용 시나리오: 조직-혈중 HER2 불일치의 실측 수치로 인용. liquid biopsy의 재프로파일링 필요성 근거로.
  - BibTeX key: `@xie2024her2ctcconcordance`

- §Results 3.3: "The detection rate of HER2+CTC was 32.1% (9/28)" [in histologically HER2-negative patients]
  - 사용 시나리오: HER2⁻ 판정 환자 중 실제로 혈중 HER2⁺ 세포 보유 비율의 직접 수치 근거. ADC 적응 확장 논리.
  - BibTeX key: `@xie2024her2ctcconcordance`

### 인용 가능 수치

- **불일치율 32.6% (kappa=0.325, p=0.030)** (Table 2, §Results 3.3)
  - 사용 시나리오: 조직 vs. CTC HER2 불일치 규모의 baseline 수치. 비교 코호트 언급 시.
  - BibTeX key: `@xie2024her2ctcconcordance`

- **hHER2⁻에서 cHER2⁺ 32.1%** (§Results 3.3)
  - 사용 시나리오: "표준 검사로 놓치는 환자 비율"의 구체적 수치 인용.
  - BibTeX key: `@xie2024her2ctcconcordance`

- **HER2+CTC vs. Ki67 Spearman R=0.38, p=0.011** (Figure 4d)
  - 사용 시나리오: CTC HER2 발현이 단순 기술적 산물이 아닌 생물학적 의미를 가짐을 보여주는 연관성 근거.
  - BibTeX key: `@xie2024her2ctcconcordance` (다중 비교 보정 미시행 한계 함께 언급 권장)

### 인용 가능 Figure/Table

- **Table 2** (§Results 3.3)
  - 조직-CTC HER2 2×2 혼동 행렬 (hHER2⁻/cHER2⁺ 9명, hHER2⁺/cHER2⁻ 5명).
  - 사용 시나리오: 불일치 방향성(양쪽 모두 발생)을 시각적으로 제시해야 할 때.
  - BibTeX key: `@xie2024her2ctcconcordance`

- **Figure 4b**
  - cHER2⁺ 환자에서 hHER2⁺/hHER2⁻ 비율이 거의 50:50임을 보여줌 — CTC HER2⁺가 조직 HER2⁺와 독립적임을 시각화.
  - 사용 시나리오: liquid biopsy의 독립적 정보 가치 강조 시.
  - BibTeX key: `@xie2024her2ctcconcordance`
