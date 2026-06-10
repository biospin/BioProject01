# Methodology Brief — negishi-2022-gastric-ctc-scrna

## 한 줄 결론 (모든 독자)

- Citation: `@negishi2022gastricctcscrna`  |  Importance: `중` (위암 CTC scRNA-seq 최초 보고, 탐색적 수준이나 위암 CTC 생물학 이해의 출발점)
- 한 문장 결론: MCA/GCM 기반 EpCAM-independent 위암 단일 CTC 전사체 분석 — EMT·혈소판 부착·epithelial 3개 서브그룹 식별; 소규모 탐색 연구로 임상 적용은 후속 대규모 검증 필요.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: open — RNA-seq raw data DDBJ accession DRA011720 공개. 분석 source data는 Supplementary Data 1–9 (MOESM3 xlsx).
- **코드 공개**: 없음 (명시적 code repository 미제공). Methods에 Trimmomatic, HISAT2, HTseq, Seurat, DAVID 파이프라인 기술. 특정 Seurat resolution parameter는 미공개 → 정확한 클러스터링 재현 불확실.
- **자원 요구**: GPU 불필요. RNA-seq 분석은 일반 bioinformatics 서버(~16 core, 64 GB RAM)로 충분. 5 M reads/cell, 47 CTC 규모.
- **핵심 의존성**: Trimmomatic-0.36, HISAT2 2.1.0 (hg19), HTseq, R stats v3.6.2, Seurat (버전 미명시), DAVID v6.8, heatmap.2 (R), Quartz-seq WTA 프로토콜.
- 자세히 → [negishi-2022-gastric-ctc-scrna_core.md](negishi-2022-gastric-ctc-scrna_core.md) §Methods, [sources/negishi-2022-gastric-ctc-scrna.pdf](sources/negishi-2022-gastric-ctc-scrna.pdf) §Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 부분 불일치. 우리 주력 dataset(HSPC 10x Multiome)과 직접 호환 없음. 단 scRNA-seq 분석 pipeline(Seurat, UMAP)은 공통. 위암 CTC 데이터가 필요할 경우 DRA011720 raw data 재분석 가능.
- **자원 가능성**: 분석 재현은 기존 bioinformatics 환경으로 가능. 단 MCA/GCM CTC 분리 장비 없음 — wet lab 재현 시 CRO 또는 Yoshino lab 협력 필요.
- **비용·시간 추정**: 분석(재현) — 1–2주. CTC 분리·sequencing 실험 — 6개월 이상, 환자 IRB 포함.
- **ROI 한 줄**: 탐색적 위암 CTC 생물학 레퍼런스로 academic-citation ROI 있음; 제품화 ROI는 현 단계 낮음 (TRL 2–3).
- 자세히 → [negishi-2022-gastric-ctc-scrna_lens-industry.md](negishi-2022-gastric-ctc-scrna_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: ITGA2가 47개 CTC 중 22개(45%)에서 발현 — 위암 ADC target 후보로서 현재 진행 중인 ADC pipeline에서 coverage되는 target인지 확인 필요.
- 질문: MCA 장치 제조사 Optonics Precision (일본)의 국내 유통 또는 공동연구 가능성 — BD 담당자 문의 필요.
- **다음 액션**: DRA011720 raw data를 우리 bioinformatics 환경에서 재분석해 Seurat 파라미터 및 서브그룹 재현성 확인 — 2주 내 시도 가능.

---

마지막 갱신: 2026-06-10
