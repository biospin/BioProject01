# Methodology Brief — modi-2020-destiny-breast01

## 한 줄 결론 (모든 독자)

- Citation: `@modi2020destinybreast01`  |  Importance: `상` (DESTINY-Breast01 — HER2+ MBC T-DM1 이후 ADC 표준치료 전환의 등록 근거 Phase 2)
- 한 문장 결론: T-DXd 5.4 mg/kg 단일요법, T-DM1 기치료 HER2+ MBC에서 ORR 60.9% + PFS 16.4개월 확증 — SEV_BRCA / NCCHE_Gastric BD 및 임상 전략 레퍼런스.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 임상시험 데이터 — 재현 불가. ClinicalTrials.gov (NCT03248492) 등록 데이터. 환자 수준 데이터는 `미제공:` (Daiichi Sankyo 데이터 sharing statement 있으나 요청 절차 필요).
- **코드 공개**: 해당 없음 — 임상시험 통계 분석 코드 미공개 (임상 결과 보고 논문).
- **자원 요구**: 해당 없음 (임상시험 재현 불가).
- **핵심 의존성**: 해당 없음.
- 자세히 → [modi-2020-destiny-breast01_core.md](modi-2020-destiny-breast01_core.md) §Methods, [sources/modi-2020-destiny-breast01.pdf](sources/modi-2020-destiny-breast01.pdf) §Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 직접 적용 불가 (임상시험). SEV_BRCA / NCCHE_Gastric T-DXd 처방 환자군의 임상 레퍼런스로 활용.
- **자원 가능성**: BD reference 및 임상 의사결정 문서로 즉시 활용 가능. 계산 자원 불필요.
- **비용·시간 추정**: 문헌 참조 — 즉시 활용 가능.
- **ROI 한 줄**: HER2 ADC 전략 수립 시 regulatory-precedent + BD benchmark 값으로 최고 우선순위 인용 논문.
- 자세히 → [modi-2020-destiny-breast01_lens-industry.md](modi-2020-destiny-breast01_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- `질문:` DESTINY-Breast03 (Phase 3 RCT, T-DXd vs. T-DM1 2차 라인) 결과를 함께 보면 이 논문의 단일군 데이터를 어떻게 재위치시킬 수 있는가? OS benefit 확증 여부.
- `질문:` ILD grade 5 (2.2%) — 우리 기관 T-DXd 투여 환자에서 ILD 모니터링 SOP가 이 논문 Appendix Table S6 권고사항과 일치하는지 확인 필요.
- **다음 액션**: DESTINY-Breast03 결과 논문(외부 맥락 — Modi et al. 2022, NEJM 또는 ASCO) 분석 → `modi-2022-destiny-breast03` 폴더 생성 후 동일 pipeline 적용. 이 논문과 비교 insightagent 실행.

---
마지막 갱신: 2026-06-10
