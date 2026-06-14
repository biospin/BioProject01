# Methodology Brief — trevino-2021-cortex

## 한 줄 결론 (모든 독자)
- Citation: `@trevino2021cortex`  |  Importance: `상` — fetal human cortex multiome reference 원 논문, chromatin accessibility·expression·ASD noncoding variant 해석을 한 자료에서 연결.
- 한 문장 결론: PCW16~24 human cortex의 scRNA+scATAC+multiome으로 CRE-gene link·GPC·TF wave를 도출하고 cluster별 BPNet으로 ASD noncoding variant를 prioritize한 자료. 우리 single-cell multiome 분석의 human cortex reference(GSE162170)이자 분석 패턴 차용 대상.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` — GEO `GSE162170`(fetal human cortex singleome + PCW21 multiome). ASD genome은 SSC(An et al. 2018, dbGaP류 → `restricted` 추정).
- 코드 공개: GitHub `GreenleafLab/brain_comp`, `GreenleafLab/Brain_ASD`. `검토필요:` license·maintenance·figure 재현 범위는 repo 직접 확인 필요.
- 자원 요구: **GPU 필수**(cluster별 BPNet 학습, 250,000+ peak × 2,114 bp, 5-fold CV). single-cell 통합·linkage는 고메모리 CPU workflow. `해석:` 본 프로젝트 GPU 1대로 atlas 재처리는 가능하나 BPNet 전체 재학습은 시간 부담.
- 핵심 의존성: 10x Cellranger/ArchR(또는 Signac), CCA 통합(Seurat/Stuart 2019 방식), chromVAR(motif), RNA velocity(scVelo/La Manno), BPNet(Avsec 2020, CNN dilation+residual). `검토필요:` 정확한 version은 STAR Methods.
- 자세히 → [trevino-2021-cortex_core.md](trevino-2021-cortex_core.md) §Methods, [sources/data_GSE162170.url](sources/data_GSE162170.url)

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: 부분 일치 — single-cell multiome·chromatin-RNA coupling benchmark로 직접 유용하나 cortex biology는 우리 HSPC와 다름.
- 자원 가능성: GEO download + 통합/linkage 재현은 우리 환경에서 가능. BPNet 재학습은 GPU·시간 추가 필요.
- 비용·시간 추정: source/metadata audit 0.5~1일, multiome subset 재처리·annotation mapping 1~2주, CRE-gene linking 패턴 차용 PoC 1분기.
- ROI 한 줄: 원 출처를 정확히 잡아두면 후속 MultiVelo/MultiVeloVAE 계열의 fetal cortex 결과 해석에서 provenance 혼선을 줄이고, CCA linking·BPNet scoring 패턴을 우리 lineage에 옮길 수 있다.
- 자세히 → [trevino-2021-cortex_lens-industry.md](trevino-2021-cortex_lens-industry.md) §3

## 본인 재회고 (본인)
- 질문: 후속 velocity 논문이 쓴 Trevino subset은 원 논문의 multiome(PCW21, 8,981 cell)인가 singleome인가? 어떤 QC slice인가?
- 질문: ASD variant scoring의 case/control matching과 permutation FDR이 regulatory-grade로 충분히 투명한가? (effect size 작음: early RG OR=1.909, 단일 SSC cohort)
- 다음 액션: GSE162170 file manifest를 별도 dataset note에 연결하고, multiome subset에 우리 chromatin–transcription lag framework를 적용해 본 논문의 sequential-motif 관찰과 activation lag를 정렬 — 다음 sprint.
- 자세히 → [trevino-2021-cortex_lens-academic.md](trevino-2021-cortex_lens-academic.md), [trevino-2021-cortex_lens-industry.md](trevino-2021-cortex_lens-industry.md) §4

---
마지막 갱신: 2026-06-13
