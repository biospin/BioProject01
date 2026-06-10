# Methodology Brief — liu-2023-ctc-scrna-protocol

## 한 줄 결론 (모든 독자)

- Citation: `@liu2023ctcscrnaprotocol`  |  Importance: `중` — PDAC CTC scRNA-seq 표준 프로토콜, CTC ADC 파이프라인 SOP 및 bioinformatics baseline 설계에 직접 참조 가능하나 소규모 코호트 + 단일 상업 chip 종속.
- **한 문장 결론**: HPV 혈액 EpCAM/CA19-9 chip CTC 분리 → 10x scRNA-seq → CopyKAT + Seurat CTC 동정 → CellPhoneDB interaction weight score 면역관문 분석의 end-to-end 재현 가능 프로토콜. CTC ADC 타깃 후보(LGALS9, CD47, TIGIT 등) 발굴에 직결.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: open — NGDC GSA-human HRA003672 (raw), NGDC OMIX002487 (processed combined matrix, 직접 다운로드 가능).
- **코드 공개**: GitHub https://github.com/Jinen22/scRNA-PDAC-CC + Zenodo https://doi.org/10.5281/zenodo.8151927 (CC BY-NC-ND 4.0). 시각화 스크립트 `Figure2.R` + gene list CSV 포함. 유지보수 상태: 확인 필요.
- **자원 요구**: CopyKAT 실행에 n.cores = 20 권장. CellPhoneDB Python CLI. GPU 불필요. RAM: 해석: scRNA-seq 수만 세포 기준 32–64 GB 추정. Runtime: CopyKAT 환자당 수 시간.
- **핵심 의존성**: R ≥ 4.0.3 + Seurat 4.0.1 + CopyKAT 1.0.5 + CellPhoneDB 2.1.2 (Python) + Cell Ranger 3.0.0 + ggplot2 3.3.3 + ComplexHeatmap 2.6.2.
- 자세히 → [liu-2023-ctc-scrna-protocol_core.md](liu-2023-ctc-scrna-protocol_core.md) §Methods, [sources/liu-2023-ctc-scrna-protocol.pdf](sources/liu-2023-ctc-scrna-protocol.pdf) §Step-by-Step

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 10x Genomics 3' scRNA-seq 기반이면 직접 적용 가능. wet-lab은 HPV 혈액(수술 필요) + MerryHealth chip(중국 공급사) — 말초혈 또는 대안 chip 사용 시 수정 필요.
- **자원 가능성**: 전산 파이프라인은 20코어 서버로 가능. wet-lab은 FACS 장비 + microfluidic chip 조달 필요. MerryHealth chip 한국 유통 미확인.
- **비용·시간 추정**: 전산 재현 (OMIX002487 데이터 사용): 1–2주 sprint. 신규 wet-lab 셋업 포함 full pilot: 1–2개월.
- **ROI 한 줄**: CTC ADC 타깃(LGALS9:CD47, CD94-NKG2A:HLA-E 등) 후보군 확보 + scRNA-seq QC pipeline 내재화 → 직접 ROI. 단 HPV 혈액 채취 제약으로 범용 liquid biopsy 적용은 장기 과제.
- 자세히 → [liu-2023-ctc-scrna-protocol_lens-industry.md](liu-2023-ctc-scrna-protocol_lens-industry.md) §3

---

## 본인 재회고 (본인)

- 질문: OMIX002487 processed data로 Figure 3 (CTC t-SNE + CopyKAT) 재현 가능한가? 환자별 CTC 세포 수가 충분한가?
- 질문: PPBP/PF4 혈소판 marker를 CTC marker에서 제외한 뒤 CTC cluster 정의가 어떻게 달라지는가? inferCNV와 CopyKAT 결과 일치 여부 확인 필요.
- **다음 액션**: GitHub Jinen22/scRNA-PDAC-CC clone + OMIX002487 데이터 다운로드 → Seurat + CopyKAT 재현 시도 — 이번 sprint (~2주).
- 자세히 → [liu-2023-ctc-scrna-protocol_lens-academic.md](liu-2023-ctc-scrna-protocol_lens-academic.md), [liu-2023-ctc-scrna-protocol_lens-industry.md](liu-2023-ctc-scrna-protocol_lens-industry.md) §4

---

마지막 갱신: 2026-06-10
