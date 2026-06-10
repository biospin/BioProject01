# Methodology Brief — pantel-2019-ctc-review

## 한 줄 결론 (모든 독자)

- Citation: `@pantel2019ctcreview`  |  Importance: `상` — MRD 개념과 liquid biopsy를 통합한 분야 표준 리뷰. ADC 표적 근거·임상 모니터링 전략 수립 시 필수 reference.
- 한 문장 결론: CTC·ctDNA 기반 MRD 검출 기술과 암종별 임상 예후 근거를 통합한 리뷰 — ADC 표적(EPCAM·HER2·PSMA 등) 표면 발현 이질성 및 내성 기전 추적의 생물학적 근거를 제공한다.

---

## 재현 가능성 체크 (재현 담당자)

재현 적용 불가 — 자료 유형: Review paper. 독자적 실험 방법이 없음.

- 인용 데이터 접근: 개별 원저(Rack 2014, Garcia-Murillas 2015, Tie 2016 등) — PubMed 오픈 접근 가능.
- CTC 포획 프로토콜: CellSearch 상업용 키트(Menarini Silicon Biosystems). EPISPOT/EPIDROP은 Alix-Panabières 그룹 접촉 또는 상업화 서비스 확인 필요.
- ctDNA 분석: CAPP-Seq(Newman et al., Nat Biotechnol 2016 — iDES). ddPCR: Bio-Rad QX200 플랫폼. BEAMing: Sysmex Inostics 상업 서비스.
- 자원 요구: 미제공 (리뷰 특성상 방법론 자원 명시 없음). 개별 assay별 요구 사항은 원저 참조.
- 자세히 → [pantel-2019-ctc-review_core.md](pantel-2019-ctc-review_core.md) §Methods

---

## 우리 적용 가능성 (의사결정자)

- Dataset 호환: CTC 기반 데이터는 혈액 샘플 기반 — 우리 연구(scRNA-seq 중심)와 직접 pipeline 호환은 없으나, ADC 표적 발굴 및 임상 MRD 모니터링 전략 설계에서 근거로 활용 가능.
- 자원 가능성: CTC 포획(CellSearch 또는 Parsortix)은 외부 CRO 위탁 필요. ctDNA 분석(ddPCR)은 협력 기관에서 시행 가능 여부 확인 필요.
- 비용·시간 추정: 이 논문 자체를 활용하는 것은 즉시(citation 수준). CTC CDx feasibility study 착수까지 1개 분기 이상.
- ROI 한 줄: ADC pitch deck의 표적 선정 근거 및 MRD 임상 모니터링 전략의 선행 근거로 즉시 활용 가능. 독자적 CTC assay 구축은 장기 과제.
- 자세히 → [pantel-2019-ctc-review_lens-industry.md](pantel-2019-ctc-review_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: c-TRAK TN 결과(2022–2023) 및 Guardant Reveal CRC MRD FDA 승인 현황 확인 — 이 리뷰가 예측한 "MRD-triggered 치료 개입 window"가 실제 임상 이익으로 연결됐는지 판단 필요.
- 질문: HER2 discordance(원발 HER2⁻ → CTC HER2⁺ 최대 30%)를 ADC pitch에서 활용할 경우, 이를 뒷받침하는 최신 대규모 코호트 데이터(2020–2024)를 추가 확보해야 한다.
- 다음 액션: ADC pitch deck 작성 시 Rack 2014 CTC HR 수치·Garcia-Murillas 7.9개월 수치를 직접 인용. CTC 표면 항원 프로파일링(EPCAM·HER2·PSMA) 관련 후속 리뷰(2021–2024) 스크리닝 — `pantel-2019-ctc-review_lens-academic.md`의 Citation 후보 섹션 참조.
- 자세히 → [pantel-2019-ctc-review_lens-academic.md](pantel-2019-ctc-review_lens-academic.md), [pantel-2019-ctc-review_lens-industry.md](pantel-2019-ctc-review_lens-industry.md) §4

---

마지막 갱신: 2026-06-10
