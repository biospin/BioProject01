# Methodology Brief — cortes-2022-destiny-breast03

## 한 줄 결론 (모든 독자)
- Citation: `@cortes2022destinybreast03`  |  Importance: `상` (HER2+ MBC 2차 치료 표준 전환을 Phase 3 RCT로 확정한 pivotal 데이터 + ADC 설계 benchmark)
- 한 문장 결론: T-DXd가 T-DM1 대비 PFS HR=0.28로 우월함을 입증해 2차 치료 표준을 교체했으며, DAR≈8 + topoisomerase I inhibitor + cleavable linker ADC 설계의 임상 검증 기준점.

---

## 재현 가능성 체크 (재현 담당자)
- **데이터 접근**: 임상시험 데이터 — 공개 접근 불가. NCT03529110 (ClinicalTrials.gov). 요약 통계는 논문 본문 및 Supplementary에 모두 수록됨. 개인수준 데이터(IPD)는 별도 데이터 공유 신청 필요 (Data Availability Statement 존재 — Supplementary Appendix p.7).
- **코드 공개**: 없음 (임상시험; 통계 분석 코드 미공개). Statistical analysis plan은 protocol에 포함.
- **자원 요구**: 재현 시도 불가 (임상 RCT). 논문 수치 재계산 시 R `survival` 패키지 또는 SAS LIFETEST로 log-rank/Cox 결과 확인 가능.
- **핵심 의존성**: RECIST v1.1 (progression 정의), NCI CTCAE v5.0 (AE 분류), MedDRA v23.0 (AE coding).
- 자세히 → [cortes-2022-destiny-breast03_core.md](cortes-2022-destiny-breast03_core.md) §Methods, [sources/nejmoa2115022_appendix.pdf](sources/nejmoa2115022_appendix.pdf) §Supplementary Methods

---

## 우리 적용 가능성 (의사결정자)
- **Dataset 호환**: 직접 적용 불가 (임상 RCT). 단, surfaceome-adc-target 분석에서 ADC 타겟 평가 기준으로 활용 — T-DXd의 DAR, payload, linker 설계 파라미터가 신규 ADC 설계 benchmark.
- **자원 가능성**: 문헌 분석 수준에서 즉시 활용 가능. 임상 재현은 Phase 3 인프라(169개 기관, 5.4 mg/kg IV q3w 투여, ILD 모니터링 체계) 필요.
- **비용·시간 추정**: 문헌 참조 — 즉시. 유사 ADC 임상 설계를 위한 protocol 작성 참조 — 1–2주. 신규 ADC IND에서 safety management 섹션 작성 참조 — 수일.
- **ROI 한 줄**: ADC 플랫폼 설계 방향성과 ILD 안전관리 프로토콜 참조로 향후 ADC 임상 개발의 기준 문서로 활용. BD·규제 대응 pitch에서 인용 가치 최상.
- 자세히 → [cortes-2022-destiny-breast03_lens-industry.md](cortes-2022-destiny-breast03_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)
- **질문**: 최종 OS 분석(T-DM1 crossover 보정 포함)이 발표되었는가? ESMO/ASCO 2023–2024 업데이트 확인 필요.
- **질문**: DESTINY-Breast03 기준 Asia 환자 ILD 발생률이 비아시아 대비 유의하게 다른가? 아시아 특이적 ILD 위험 분석 논문 별도 탐색 필요.
- **다음 액션**: surfaceome-adc-target 분석 내 다른 ADC 논문(예: DESTINY-Breast04, TROPION-Breast01)과 비교 evidence bundle 구성 — 다음 sprint.
- 자세히 → [cortes-2022-destiny-breast03_lens-academic.md](cortes-2022-destiny-breast03_lens-academic.md), [cortes-2022-destiny-breast03_lens-industry.md](cortes-2022-destiny-breast03_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
