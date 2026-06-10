# Methodology Brief — shitara-2020-destiny-gastric01

## 한 줄 결론 (모든 독자)

- Citation: `@shitara2020destinygastric`  |  Importance: `상` — HER2+ 위암 3차 치료에서 ORR 51%·OS HR 0.59를 달성한 랜드마크 RCT. FDA 승인의 pivotal evidence이자 ADC CDx·ILD 솔루션 BD 기회의 근거.
- 한 문장 결론: T-DXd가 trastuzumab 포함 2차 이상 실패 HER2+ 위암 환자에서 ORR과 OS 모두 화학요법 대비 통계적으로 유의미하게 우월했다; ADC target 선정·동반진단·ILD 관리 BD 방향으로 직접 활용 가능.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 임상시험 원시 데이터 비공개 (Daiichi Sankyo 보유). Data sharing statement 있으나 individual patient data는 요청 기반 — regulatory audit 수준 공개 제한. ClinicalTrials.gov NCT03329690에서 프로토콜·결과 요약 확인 가능.
- **코드 공개**: 없음 — 임상시험 통계 분석 코드 비공개. 통계 방법(CMH test, log-rank, Cox regression, Kaplan-Meier, Brookmeyer-Crowley CI)은 표준 패키지(SAS, R `survival` 등)로 재현 가능.
- **자원 요구**: 임상시험 재수행이 아닌 통계 재현은 summary data + standard software로 가능. GPU 불필요.
- **핵심 의존성**: RECIST v1.1, CTCAE v5.0, ICH E9 통계 원칙 준수. CDx: Ventana PATHWAY 4B5 HER2 IHC.
- 자세히 → [shitara-2020-destiny-gastric01_core.md](shitara-2020-destiny-gastric01_core.md) §Methods, [sources/nejmoa2004413_protocol.pdf](sources/nejmoa2004413_protocol.pdf)

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 이 논문 자체는 임상 RCT — 우리의 genomics/single-cell pipeline에 직접 적용 불가. 단, NCCHE_Gastric 코호트(위암 환자)와 연계하면 HER2 발현 profiling, T-DXd 치료 후 샘플 분석 가능.
- **자원 가능성**: 통계 재현(ORR, OS, subgroup)은 공개 수치만으로 가능(R/Python, 1–2일). 실제 환자 데이터 접근에는 IRB + 기관 협력 필요.
- **비용·시간 추정**: 문헌 활용(BD pitch, 발표) = 즉시. CDx 파트너십 파일럿 = 3–6개월. 임상 연계 연구 = 1년+.
- **ROI 한 줄**: regulatory-precedent + BD-opportunity로 즉시 활용 가능한 benchmark 자료. surfaceome ADC target 선정 보고서에서 HER2의 임상 검증 수준을 뒷받침하는 core evidence.
- 자세히 → [shitara-2020-destiny-gastric01_lens-industry.md](shitara-2020-destiny-gastric01_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: T-DXd 내성 기전이 밝혀졌는가? 이 논문 이후 biomarker 분석 결과(HER2 loss, TOP1 mutation, PI3K mutation)가 발표됐는지 DESTINY-Gastric01 exploration cohort 또는 후속 연구 확인.
- 질문: 이 시험에서 ILD 10% → real-world에서는 어떻게 달라졌는가? 일본 post-marketing surveillance(J-RWD, NDB) 데이터 확인.
- 다음 액션: NCCHE_Gastric 코호트에서 HER2 IHC 재검 + T-DXd 사용 가능 환자 풀 파악 → 파일럿 liquid biopsy 연구 feasibility 확인 (이번 분기 내).
- 자세히 → [shitara-2020-destiny-gastric01_lens-academic.md](shitara-2020-destiny-gastric01_lens-academic.md), [shitara-2020-destiny-gastric01_lens-industry.md](shitara-2020-destiny-gastric01_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
