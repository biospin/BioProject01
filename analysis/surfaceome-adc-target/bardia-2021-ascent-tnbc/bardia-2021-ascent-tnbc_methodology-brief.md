# Methodology Brief — bardia-2021-ascent-tnbc

## 한 줄 결론 (모든 독자)

- Citation: `@bardia2021ascent`  |  Importance: `상` (TROP2 ADC pivotal Phase 3 근거. PFS HR 0.41 + OS HR 0.48. Regulatory gold standard.)
- 한 문장 결론: 재발·불응성 mTNBC에서 sacituzumab govitecan(TROP2-ADC)이 화학요법 대비 PFS/OS/ORR 모두 우월 — ADC 임상 개발·BD 의사결정의 기준 benchmark 논문.

## 재현 가능성 체크 (재현 담당자)

- 데이터 접근: 임상 시험 데이터 — ClinicalTrials.gov NCT02574455. Patient-level data 공개 여부는 NEJM data sharing statement 통해 sponsor(Gilead) 신청 필요. 공개 patient-level dataset 없음.
- 코드 공개: 없음. 통계 분석은 Covance 수행. R/SAS 코드 미공개.
- 자원 요구: 재현 적용 불가 — 임상 RCT 원데이터 필요. 공개 데이터로는 Kaplan-Meier curve digitization 기반 재분석만 가능.
- 핵심 의존성: Kaplan-Meier + stratified log-rank + Cox PH. 통계 방법 재현은 R `survival` 패키지로 가능하나 원데이터 접근이 전제.
- 자세히 → [bardia-2021-ascent-tnbc_core.md](bardia-2021-ascent-tnbc_core.md) §Methods, [sources/bardia-2021-ascent-tnbc.pdf](sources/bardia-2021-ascent-tnbc.pdf) §Statistical Analysis

## 우리 적용 가능성 (의사결정자)

- Dataset 호환: 직접 computational 적용 대상 아님. SEV_BRCA·NCCHE_Gastric 파이프라인에서 TROP2 ADC 임상 근거로 활용.
- 자원 가능성: 재현 불필요. 활용 방식은 (1) BD 미팅 reference, (2) 자체 TROP2 IHC 발현 연구 기획, (3) competitor TROP2 ADC 비교 분석 기준.
- 비용·시간 추정: 논문 읽기 및 내부 공유 — 즉시 가능. TROP2 IHC 자체 발현 연구 — 1분기 내 기획, ~2–3개월 수행.
- ROI 한 줄: TROP2 ADC class의 regulatory-grade 임상 근거 — 향후 TROP2 타깃 ADC 도입·경쟁 분석·CDx 개발 시 필수 reference.
- 자세히 → [bardia-2021-ascent-tnbc_lens-industry.md](bardia-2021-ascent-tnbc_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)

- 질문: ASCENT biomarker sub-study 결과(TROP2 발현 연속 변수와 PFS correlation)가 별도 발표됐는가? PubMed "ASCENT TROP2 biomarker" 검색.
- 질문: Datopotamab deruxtecan (DS-1062) TROPION-Breast01 결과와 head-to-head 비교 시 population mismatch 고려 필요한가?
- 다음 액션: NCCHE_Gastric 또는 SEV_BRCA 보유 FFPE 샘플에서 TROP2 IHC 발현 분포 확인 기획 착수 — 다음 분기.
- 자세히 → [bardia-2021-ascent-tnbc_lens-academic.md](bardia-2021-ascent-tnbc_lens-academic.md), [bardia-2021-ascent-tnbc_lens-industry.md](bardia-2021-ascent-tnbc_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
