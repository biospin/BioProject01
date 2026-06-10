# Methodology Brief — kang-2024-kaist-tumor-normal

## 한 줄 결론 (모든 독자)

- Citation: `@kang2024tumornormal`  |  Importance: `상` — 30 암종 tumor-normal 대비 open atlas, ADC target 정상 발현 baseline 참조에 즉시 활용 가능
- 한 문장 결론: KAIST가 4.9M 세포 pan-cancer tumor-normal atlas를 구축해 공개했으며, cellatlas.kaist.ac.kr에서 정상 조직 cell state별 발현을 직접 조회할 수 있다.

## 재현 가능성 체크 (재현 담당자)

- 데이터 접근: `open` — Zenodo DOI:10.5281/zenodo.10651059 (processed scRNA-seq + spatial); GEO GSE218989 (LC bulk); EGA EGAD00000000469 (LC scRNA-seq, controlled access, 4주 처리)
- 코드 공개: Zenodo 동일 repository, license 미명시 (`검토필요:`); scanpy, sklearn, BBKNN, Scrublet, inferCNVpy, CellPhoneDB v3.1.0, cell2location, PyDESeq2 v0.4.3 사용
- 자원 요구: GPU 필수 아님(NMF + scoring); 대규모 메모리 서버 권장 (4.9M 세포 전체 재분석 시). Geometric sketch 서브샘플링으로 일반 서버에서 부분 재현 가능
- 핵심 의존성: `scanpy >= 1.8.2`, `scikit-learn v1.0.2`, `inferCNVpy v0.4.2`, `BBKNN`, `cell2location`, `gseapy v0.10.8`, `scipy.stats v1.10.0`, `statsmodels.stats v0.13.5`
- 자세히 → [kang-2024-kaist-tumor-normal_core.md](kang-2024-kaist-tumor-normal_core.md) §Methods

## 우리 적용 가능성 (의사결정자)

- Dataset 호환: 부분 일치 — 우리 scRNA-seq(10x Chromium)과 같은 platform. Scanpy h5ad 형식 예상, 호환 확인 필요
- 자원 가능성: cellatlas web portal 조회는 즉시 가능 (인터넷 접근). 전체 데이터 local 분석은 HPC 또는 128GB RAM+ 서버 필요
- 비용·시간 추정: web portal 활용 → 1~2일; cell state projection (sc.tl.score_genes) → 1~2주; 전체 재분석 → 1~2개월
- ROI 한 줄: ADC target의 정상 조직 발현 baseline을 세계 최대 규모(30 암종, 4.9M 세포)로 무료 조회 가능 — 즉시 BD pitch 근거로 활용 가능
- 자세히 → [kang-2024-kaist-tumor-normal_lens-industry.md](kang-2024-kaist-tumor-normal_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)

- `질문:` TLS signature gene list (Supp. Data 7 top 50)가 우리 tumor scRNA-seq marker panel과 얼마나 겹치는지 — Zenodo 데이터 수령 즉시 overlap 분석
- `질문:` 정오표 (2025-03-21) 세부 내용 확인 — Fig. 또는 수치에 수정이 있으면 core.md 업데이트 필요
- 다음 액션: cellatlas.kaist.ac.kr/ecosystem/ 에서 우리 ADC target 후보 gene list (AKR1C1, WNT5A 포함) 정상 조직 발현 조회 — 이번 주 내
- 자세히 → [kang-2024-kaist-tumor-normal_lens-academic.md](kang-2024-kaist-tumor-normal_lens-academic.md), [kang-2024-kaist-tumor-normal_lens-industry.md](kang-2024-kaist-tumor-normal_lens-industry.md) §4

---
마지막 갱신: 2026-06-10
