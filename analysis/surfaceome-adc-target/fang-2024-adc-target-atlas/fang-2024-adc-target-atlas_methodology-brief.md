# Methodology Brief — fang-2024-adc-target-atlas

## 한 줄 결론 (모든 독자)

- Citation: `@fang2023adctargetatlas` | Importance: `상` (pan-cancer ADC target atlas 최초 체계화 — NCCHE Gastric / SEV BRCA CTC 타겟 외부 검증 기준)
- 한 문장 결론: 19개 고형암종 × 다중 omics 통합 알고리즘으로 75개 ADC 타겟 후보 + 165개 target-indication 조합을 제시한 atlas — Supplementary Table 4/6가 핵심 활용 자료.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 반공개. TCGA/GTEx/HPA 등 공개 데이터베이스 기반. Supplementary Tables (MOESM2.xlsx)는 논문과 함께 제공. 원시 분석 데이터는 "corresponding author on reasonable request" — 즉시 공개 접근 없음.
- **코드 공개**: 없음. 알고리즘 자세한 코드 비공개 ("custom computer codes available from corresponding author upon reasonable request"). 단 방법론은 Methods에 충분히 기술되어 있어 재구현 가능.
- **자원 요구**: 추정: RNA-seq 분석(DESeq2) + PCA 기반 기능 유전체 프로파일링 — 표준 bioinformatics 서버 (16core/64GB RAM) 충분. GPU 불필요. 전체 파이프라인 재현 시 ~1~2주 공수.
- **핵심 의존성**: R (DESeq2, ggstatsplot, OmicCircos, GSVA/ssGSEA), Python (데이터 처리). 외부 DB: RNAseqDB, TCGA, GTEx, HPA, HPM, COMPARTMENTS, BloodSpot, OncokB.
- 자세히 → [fang-2024-adc-target-atlas_core.md](fang-2024-adc-target-atlas_core.md) §Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: Supplementary Table 4 (165개 target-indication) + Table 6 (과발현율)을 CytoGen CTC 발현 목록과 교차 비교 — 직접 가능. 기술 플랫폼 차이(CTC vs. TCGA 조직) 있으나 타겟 목록 수준 비교는 즉시 가능.
- **자원 가능성**: MOESM2.xlsx 다운로드 + Python/R 교차 비교 스크립트 — 1인 1~2일. 재현 분석(전체 파이프라인) 필요시 ~2주.
- **비용·시간 추정**: 교차 분석(타겟 목록 비교) → ~1 person-day. BD 슬라이드 추가 → ~2hr. 전체 atlas 재현 → ~2주.
- **ROI 한 줄**: NCCHE Gastric / SEV BRCA CTC 타겟 선택의 외부 검증 근거를 즉시 확보 — BD 발표 신뢰도 향상 대비 1~2일 투자.
- 자세히 → [fang-2024-adc-target-atlas_lens-industry.md](fang-2024-adc-target-atlas_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: MOESM2.xlsx Supplementary Table 4에서 STAD 관련 target-indication 추출 후 NCCHE Gastric CTC 발현 타겟과 교차 — 몇 개나 일치하는가? (즉시 실행 가능)
- 질문: Fig. 5 갈색 점(신규 타겟)과 검정 점(기존 ADC 타겟)의 구분 기준이 Supplementary Table 4의 어느 열에 있는가? 35개 신규 후보 명단 확인 필요.
- 다음 액션: MOESM2.xlsx 열람 → Supplementary Table 4에서 STAD/BRCA 행 추출 → CytoGen CTC 타겟 목록과 교차 분석 스크립트 작성 (이번 주 내)

---

마지막 갱신: 2026-06-10
