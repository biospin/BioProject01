# Methodology Brief — hu-2021-cancer-surfaceome-atlas

## 한 줄 결론 (모든 독자)

- Citation: `@hu2021cancersurfaceomeatlas` | Importance: `상` — 전체 surfaceome의 2.5%만 current ADC/CAR-T drug target; 신규 1,433개 치료 타깃 후보 + caGESP 409개가 우리 ADC 파이프라인 1차 필터로 즉시 활용 가능.
- 한 문장 결론: 9개 자원 통합으로 GESP 3,567개를 정의하고, 33개 암종에서 caGESP 409개를 식별한 pan-cancer surfaceome atlas — ADC 타깃 우선순위 결정 및 AND/iCAR-T 쌍 탐색에 직접 활용 가능한 공개 자원.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: open — TCGA (cancergenome.nih.gov), GTEx (xenahubs), CPTAC (proteomics.cancer.gov), DepMap (depmap.org), scRNA-seq (GEO: GSE125449, GSE131907, GSE131928, GSE139829 외). 모두 공개.
- **코드 공개**: https://github.com/fcgportal/TCSA (공개). TCSA 포털 http://fcgportal.org/TCSA 통해 분석 결과 직접 조회 가능.
- **자원 요구**: GPU 불필요. 재현 시 TCGA/GTEx 규모 데이터 처리 필요 (RAM 32~64GB, 멀티코어 CPU 추정). 포털 직접 조회는 웹 브라우저만으로 가능.
- **핵심 의존성**: GISTIC v2.0.23, HAPSEG v1.1.1, ABSOLUTE v1.0.6; TiSGeD v1.0(SPM), TissueEnrich v1.0, pSI v1.1, GSEA v1.17.0(SSEA), limma(MWW); scMatch v1.0, LTMG v1.0, CellPhoneDB v2.1.4.
- 자세히 → [hu-2021-cancer-surfaceome-atlas_core.md](hu-2021-cancer-surfaceome-atlas_core.md) §Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 우리 현재 데이터셋(HSPC, BRCA, gastric)은 TCSA 직접 입력이 아님. 단, TCSA의 caGESP 목록(Supp. Table 9)을 우리 관심 암종(SEV_BRCA, NCCHE_Gastric → STAD, PAAD) 필터링 후 overlap 분석 즉시 가능.
- **자원 가능성**: Supp. Table 9 xlsx 다운로드 + R/Python 교차 분석 — 1인 기준 1~2 person-day. 추가 재현(5-알고리즘 재구성)은 1~2주.
- **비용·시간 추정**: 포털 조회 즉시 + 우선순위 목록 구축 1 person-day. 내부 internalization assay 추가 시 별도 wet lab 일정 필요.
- **ROI 한 줄**: caGESP 409개 + Supp. Tables 9,10을 ADC 타깃 우선순위 결정에 직접 연결할 수 있어 내부 타깃 발굴 시간 단축; 공개 atlas 인용으로 사내/외부 보고서 신뢰도 향상.
- 자세히 → [hu-2021-cancer-surfaceome-atlas_lens-industry.md](hu-2021-cancer-surfaceome-atlas_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: TCSA 포털에서 STAD, BRCA에 해당하는 tier 1 caGESP를 바로 추출할 수 있는가? 현재 우리 파이프라인 타깃 리스트와 overlap 얼마나 되는가?
- 질문: caGESP 중 ADC internalization 데이터가 이미 문헌 보고된 것 (CEACAM5, EPCAM, MUC1 제외 나머지) 몇 개인가 — 다음 wet lab 우선순위 결정에 필요.
- 다음 액션: TCSA 포털 조회 + Supp. Table 9 다운로드 → STAD/BRCA caGESP tier 1 목록 추출 → 내부 ADC 타깃 리스트와 교차 → 신규 후보 확인 (이번 주 내).
- 자세히 → [hu-2021-cancer-surfaceome-atlas_lens-academic.md](hu-2021-cancer-surfaceome-atlas_lens-academic.md), [hu-2021-cancer-surfaceome-atlas_lens-industry.md](hu-2021-cancer-surfaceome-atlas_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
