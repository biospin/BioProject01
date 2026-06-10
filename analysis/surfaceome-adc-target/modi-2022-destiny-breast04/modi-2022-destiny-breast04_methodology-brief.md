# Methodology Brief — modi-2022-destiny-breast04

## 한 줄 결론 (모든 독자)
- Citation: `@modi2022destinybreast04`  |  Importance: `상` (DESTINY-Breast04는 HER2-low를 독립 치료 가능 인구로 확립한 pivotal Phase 3, CTC HER2 동적 프로파일링 연구의 임상 근거로 직결)
- **한 문장 결론**: T-DXd vs. 표준 화학요법 Phase 3 무작위 시험으로 HER2-low(IHC 1+/2+ISH-음성) 전이성 유방암에서 mPFS 10.1 vs. 5.4개월, OS 23.9 vs. 17.5개월 이득 확립 — regulatory-precedent + BD-opportunity 최우선 참조.

## 재현 가능성 체크 (재현 담당자)
- **데이터 접근**: restricted. Patient-level 데이터는 Daiichi Sankyo 통제. data-sharing request 가능(NEJM.org data-sharing statement 참조 — `sources/nejmoa2203690_data-sharing.pdf`). 공개 aggregate 수치(Table 2, KM 데이터)는 논문에서 직접 추출 가능.
- **코드 공개**: 없음. 임상시험 통계 분석(SAS/R)은 비공개. Protocol + SAP는 NEJM.org에 공개(`sources/nejmoa2203690_protocol.pdf`).
- **자원 요구**: 재현 불가(임상시험). 통계 방법 재현 시: R `survival` 패키지로 stratified log-rank + Cox 구현 가능. KM 곡선 재현은 digitizing software(WebPlotDigitizer) 활용.
- **핵심 의존성**: VENTANA HER2/neu (4B5) IUO Assay (investigational) — 일반 재현 불가. 상용 IHC assay 대응 연구 별도 필요.
- 자세히 → [modi-2022-destiny-breast04_core.md](modi-2022-destiny-breast04_core.md) §Methods, [sources/nejmoa2203690_protocol.pdf](sources/nejmoa2203690_protocol.pdf)

## 우리 적용 가능성 (의사결정자)
- **Dataset 호환**: 직접 적용 불가(임상시험). 단 CTC HER2 프로파일링 연구(SEV_BRCA, NCCHE_Gastric)에서 HER2-low 환자군 포함 여부와 IHC scoring protocol 정의에 DESTINY-Breast04 기준 직접 참조 가능.
- **자원 가능성**: Wet lab IHC assay — 외부 협력 필요. CTC HER2 IHC 프로토타입 → 내부 feasibility 연구 가능.
- **비용·시간 추정**: CTC HER2 IHC 표준화 pilot → 1개 기관 기준 1–2개월, 외부 CRO 없이 내부 가능.
- **ROI 한 줄**: HER2-low 정의의 임상 타당성이 확립됐으므로 CTC 기반 HER2 동적 추적의 grant·BD pitch에 즉시 활용 가능. 재현 투자 ROI는 낮으나 인용·참조 가치는 최상.
- 자세히 → [modi-2022-destiny-breast04_lens-industry.md](modi-2022-destiny-breast04_lens-industry.md) §3

## 본인 재회고 (본인)
- 질문: HER2-low 정의(IHC 1+/2+/ISH-음성)와 CTC에서 측정한 HER2 발현 수준 간 일치율은? tissue-CTC discordance가 HER2-low 분류를 어떻게 바꾸는가?
- 질문: DESTINY-Breast04 이후 HER2-low patient selection을 AI/digital pathology로 개선하는 동향 연구가 출판됐는가? (2022–2024 literature 추적 필요)
- **다음 액션**: SEV_BRCA 코호트 내 HER2 IHC 데이터에서 HER2-low(1+, 2+/ISH-음성) 비율 추출 — 이번 달 안.
- 자세히 → [modi-2022-destiny-breast04_lens-academic.md](modi-2022-destiny-breast04_lens-academic.md), [modi-2022-destiny-breast04_lens-industry.md](modi-2022-destiny-breast04_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
