# Methodology Brief — drago-2021-adc-mechanism

## 한 줄 결론 (모든 독자)

- Citation: `@drago2021adcmechanism`  |  Importance: `상` — ADC 타겟 선정·링커-payload 설계·내성 기전·차세대 전략이 단일 리뷰로 통합된 현장 표준 문헌.
- 한 문장 결론: FDA 승인 9종 ADC의 3요소(항체·링커·payload) 분석과 in vivo 기전·내성 분류를 정리한 리뷰. surfaceome 타겟 우선순위 평가와 BD 발표 레퍼런스로 직접 활용.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 재현 적용 불가 — 자료 유형: review paper. 원자료 없음. 인용된 임상시험 데이터는 각 원논문(ClinicalTrials.gov 등록번호 포함) 참조.
- **코드 공개**: 해당 없음.
- **자원 요구**: 해당 없음.
- **핵심 의존성**: 해당 없음.
- 자세히 → [drago-2021-adc-mechanism_core.md](drago-2021-adc-mechanism_core.md) §Methods (Method taxonomy 기술)

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 직접 분석 dataset 없음. surfaceome-adc-target 분석에서 타겟 선정 기준 적용 가능: 발현 수준, 내재화율, oncogenic relevance, 정상 조직 발현 차이.
- **자원 가능성**: 바이오인포매틱스 팀에서 surfaceome scoring 알고리즘으로 즉시 구현 가능. wet lab 불필요(concept 단계).
- **비용·시간 추정**: surfaceome ADC targetability scoring prototype — 분석 인력 1인 2주.
- **ROI 한 줄**: SEV_BRCA / NCCHE_Gastric ADC 전략 수립과 BD 발표에서 즉시 인용 가능. 리뷰 논문 특성상 추가 실험 투자 없이 high-citation baseline reference로 활용.
- 자세히 → [drago-2021-adc-mechanism_lens-industry.md](drago-2021-adc-mechanism_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: surfaceome dataset의 TROP2, nectin 4, HER2 발현 분포가 이 리뷰의 ADC targetability 기준(발현 수준·종양 특이성·내재화율)과 어떻게 매핑되는가? 첫 번째 scoring 검증 타겟으로 이 세 단백질을 우선 실험적으로 확인.
- 질문: belantamab mafodotin 철수(2022) 이후 BCMA 표적 ADC 전략이 어떻게 변화했는가? 우리 BCMA 타겟 전략에 영향.
- **다음 액션**: surfaceome_adc_targetability_scoring 분석 시작 — 이 리뷰의 §Antibody and target selection 기준을 점수 항목으로 코드화. 이번 분기.
- 자세히 → [drago-2021-adc-mechanism_lens-academic.md](drago-2021-adc-mechanism_lens-academic.md), [drago-2021-adc-mechanism_lens-industry.md](drago-2021-adc-mechanism_lens-industry.md) §4

---

마지막 갱신: 2026-06-10
