# Methodology Brief — nami-2021-her2-emt-silencing

## 한 줄 결론 (모든 독자)

- **Citation**: `@nami2021her2emt` | **Importance**: `중` — HER2 ADC·CTC liquid biopsy 파이프라인에서 EMT-driven ERBB2 chromatin silencing 기전의 background reference; mechanistic 완성도 낮아 직접 적용보다 인용 용도.
- **한 문장 결론**: EMT 시 ERBB2 promoter/enhancer의 active histone mark가 소실되어(repressor 축적이 아님) HER2 발현이 감소하고 trastuzumab 내성이 생긴다 — 공개 bioinformatics 데이터 재분석 + BT474 세포 실험으로 제시.

---

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: open — METABRIC(cBioPortal), GEO accession GSE44838/GSE16179/GSE17708/GSE50811, Cistrome DB, 4Dgenome(Table S1/S2 전수 목록).
- **코드 공개**: 없음 — 분석에 사용된 소프트웨어는 cBioPortal(web), Affymetrix TAC 3.0, GraphPad Prism v.6, WashU Epigenome Browser. 재현용 script 미제공.
- **자원 요구**: GPU 불필요. ChIP-seq 재분석은 표준 Linux bioinformatics 환경(BWA/Bowtie2, deepTools, samtools). RAM ~32 GB 충분.
- **핵심 의존성**: deepTools 또는 IGV(browser track 시각화), GraphPad Prism v.6(통계), cBioPortal(RNA-seq correlation), Cistrome DB / WashU Epigenome Browser(ChIP-seq).
- 자세히 → [nami-2021-her2-emt-silencing_core.md](nami-2021-her2-emt-silencing_core.md) §Methods, [sources/nami-2021-her2-emt-silencing.pdf](sources/nami-2021-her2-emt-silencing.pdf) §1.1 Materials and Methods

---

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 직접 호환 없음 — 이 논문은 유방암 HER2 epigenomics. 우리 HSPC 10x Multiome과 영역 다름. 단, CTC liquid biopsy + HER2 ADC 파이프라인 맥락에서 EMT marker + HER2 발현 분석이 있으면 직접 관련.
- **자원 가능성**: 공개 데이터 재분석 재현은 즉시 가능(표준 bioinformatics 환경). BT474 wet lab 재현은 세포 배양 + immunofluorescence 환경 필요.
- **비용·시간 추정**: 공개 데이터 재분석 재현 ~1–2주. Wet lab 재현(BT474 EMT + trastuzumab binding FACS) ~1개월.
- **ROI 한 줄**: 직접 알고리즘 차용 가치보다 HER2 ADC 내성 기전 background reference + hypothesis generation 용도. 직접 파이프라인 적용 ROI는 낮음.
- 자세히 → [nami-2021-her2-emt-silencing_lens-industry.md](nami-2021-her2-emt-silencing_lens-industry.md) §3 (BD value & 상용화)

---

## 본인 재회고 (본인)

- 질문: Nami 그룹이 HDAC inhibitor + trastuzumab 병용을 EMT 유도 HER2+ 세포에서 검증한 후속 논문을 발표했는가? (이 논문의 직접 missing experiment)
- 질문: T-DXd(trastuzumab deruxtecan) DESTINY trial에서 EMT + HER2 low 내성 기전이 보고되었는가? Daiichi-Sankyo/AZ 데이터 확인.
- **다음 액션**: HER2 ADC 내성 기전 background section 작성 시 이 논문을 "EMT → ERBB2 chromatin silencing → trastuzumab resistance" 기전 reference로 인용. 이번 달 내 draft에 포함.
- 자세히 → [nami-2021-her2-emt-silencing_lens-academic.md](nami-2021-her2-emt-silencing_lens-academic.md), [nami-2021-her2-emt-silencing_lens-industry.md](nami-2021-her2-emt-silencing_lens-industry.md) §4

---

마지막 갱신: 2026-06-10
