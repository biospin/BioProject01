# Methodology Brief — yu-2016-her2-ctc-dynamic

## 한 줄 결론 (모든 독자)
- Citation: `@jordan2016her2ctc`  |  Importance: `상` (HER2+ CTC 동적 전환 개념이 ADC 타깃 선택·치료 모니터링·병용 전략 설계에 직접 연결되는 foundation paper)
- 한 문장 결론: ER+/HER2− 전이성 유방암 CTC에서 HER2+/HER2− 상태가 자발적으로 상호전환하며, 각 상태의 약물 감수성 차이를 이용한 병용 치료(paclitaxel + Notch inhibitor)가 전임상에서 재발 억제를 달성한다.

## 재현 가능성 체크 (재현 담당자)
- **데이터 접근**: scRNA-seq — open (GEO GSE75367); MS proteomics — open (MassIVE MSV000079419); 환자 CTC 세포주(Brx-42/82/142) — MGH 연구 자원, 직접 접근 불가
- **코드 공개**: 분석 코드 공개 여부 불명확 (논문 미명시). Bioinformatics pipeline (Trimmomatic, tophat2, bowtie1, htseq-count, diptest R-package) 는 표준 공개 도구 조합.
- **자원 요구**: TMT proteomics — Orbitrap Fusion (Thermo Scientific) 질량분석기 필수. scRNA-seq — 표준 Illumina MiSeq 2×151 paired-end. 계산 자원: 표준 HPC, GPU 불필요. 미세유체 CTC-iChip 장비 필수 (연구 플랫폼).
- **핵심 의존성**: tophat2, bowtie1 (alignment); htseq-count (quantification); diptest R-package (bimodality test); GSEA software (Broad Institute, MSigDB v4); SEQUEST-based proteomics platform; STRING database.
- 자세히 → [yu-2016-her2-ctc-dynamic_core.md](yu-2016-her2-ctc-dynamic_core.md) §Methods, [sources/yu-2016-her2-ctc-dynamic.pdf](sources/yu-2016-her2-ctc-dynamic.pdf) §Methods

## 우리 적용 가능성 (의사결정자)
- **Dataset 호환**: 우리 현재 HSPC 10x Multiome 파이프라인과 직접 호환 없음. SEV_BRCA 또는 HER2 표적 ADC 개발 맥락에서만 relevant.
- **자원 가능성**: CTC-iChip 미보유 → 직접 재현 불가. scRNA-seq 분석 파이프라인은 보유 가능. 공개 데이터(GSE75367) 재분석은 즉시 가능.
- **비용·시간 추정**: 공개 scRNA-seq 재분석 1–2주. CTC-iChip 기반 신규 실험은 외부 협력 없이 불가.
- **ROI 한 줄**: 직접 재현 ROI 낮음. Academic citation 및 ADC/HER2 전략 BD 미팅에서 개념 레퍼런스로 활용.
- 자세히 → [yu-2016-her2-ctc-dynamic_lens-industry.md](yu-2016-her2-ctc-dynamic_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)
- 질문: HER2-low ADC(trastuzumab deruxtecan 등)가 HER2 동적 전환 population을 커버하는지, 이 논문이 HER2-low 치료 전략의 근거 자료로 인용될 수 있는지 확인.
- 질문: Notch inhibitor + chemotherapy 병용 임상시험 현황 — ClinicalTrials.gov 조회로 전임상 결과가 임상 번역됐는지 파악.
- **다음 액션**: GSE75367 scRNA-seq 데이터를 현대 Seurat/Scanpy 파이프라인으로 재분석해 HER2 bimodality 및 Notch/RTK 경로 signature를 독립 검증 — 다음 분기 내.

---
마지막 갱신: 2026-06-10
