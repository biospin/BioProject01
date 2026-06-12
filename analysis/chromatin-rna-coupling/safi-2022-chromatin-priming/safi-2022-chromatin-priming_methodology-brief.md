# Methodology Brief — safi-2022-chromatin-priming

## 한 줄 결론 (모든 독자)
- Citation: `@safi2022chromatinpriming`  |  Importance: `중` (우리 activation lag 가설의 방향성을 같은 HSPC system에서 지지하는 academic citation; gene-level lag 정량의 직접 근거는 아님)
- 한 문장 결론: mouse LSK HSPC scATAC-seq에서 stem-like + multi-lineage chromatin program을 동시에 가진 transition 집단(`LSKFlt3int CD9high`)을 정의해 chromatin priming이 lineage commitment·frank gene expression에 *선행*함을 보인 연구. 우리 논문의 선행성 주장 supporting citation으로 사용.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` — scATAC GEO **GSE173075**, scRNA-seq **GSE173076**, sc-qPCR OSF `osf.io/y3faj`, 추가 scRNA(Rodriguez-Fraticelli 2018) GSE90742. `검토필요:` STAR Methods Resource Availability는 GSE148746이라 적어 *accession 불일치* — 재현 전 GEO 확정 필수.
- 코드 공개: processed data + figure 재현 code가 OSF에 deposit. 분석은 공개 도구 조합(Seurat, Slingshot v1.2, FIMO v4.12.0, ruptures, NABO, SnapATAC v1.0.0, SCExV). 독립 repo·license는 `미제공:`.
- 자원 요구: GPU 명시 없음. `추정:` 표준 CPU server로 충분(method paper 아님, single-cell 분석 stack).
- 핵심 의존성: cellranger-atac v1.1.0, Seurat v3.0.1, Slingshot v1.2, FIMO(MEME 4.12.0), Python `ruptures`, SnapATAC v1.0.0, mm10.
- 자세히 → [safi-2022-chromatin-priming_core.md](safi-2022-chromatin-priming_core.md) §Methods, [sources/safi-2022-chromatin-priming.pdf](sources/safi-2022-chromatin-priming.pdf) §STAR Methods

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: *개념적 호환*(HSPC lineage priming). modality·species 불일치 — 본 연구는 mouse scATAC *단독*, 우리는 human 10x Multiome(GSE209878, paired ATAC+RNA).
- 자원 가능성: 분석 재현은 우리 환경으로 가능(GPU 불필요). 단 가져올 직접 feature/model 없음.
- 비용·시간 추정: citation·개념 차용은 즉시. change-point transition-zone 절차를 우리 paired multiome에 변형 적용하려면 ~1개월(motif→gene-level promoter accessibility로 변경 + cell-cycle 통제 추가).
- ROI 한 줄: pipeline 직접 ROI는 낮음. academic-citation·methodology-reference ROI는 분명 — 우리 lag 작업이 메우는 gap(non-paired→paired)을 정당화하는 선행 연구.
- 자세히 → [safi-2022-chromatin-priming_lens-industry.md](safi-2022-chromatin-priming_lens-industry.md) §3

## 본인 재회고 (본인)
- `질문:` change-point density(Figure 3C/3H) 절차를 우리 paired multiome에서 *gene-level promoter ATAC change point* vs *transcription onset change point*로 옮겨 두 pseudotime 차이를 lag proxy로 정의할 수 있나?
- `질문:` CD9high transition state·SPI1/GATA1 crossover가 human HSPC paired multiome에서 재현되나(cross-species 일반화)?
- 다음 액션: 우리 GSE209878 분석에서 chromatin-leads-transcription 선행성을 보일 때 본 paper를 same-system supporting citation으로 인용. erratum·GEO accession 확정은 인용 직전에.
- 자세히 → [safi-2022-chromatin-priming_lens-academic.md](safi-2022-chromatin-priming_lens-academic.md), [safi-2022-chromatin-priming_lens-industry.md](safi-2022-chromatin-priming_lens-industry.md) §4

---
마지막 갱신: 2026-06-12
