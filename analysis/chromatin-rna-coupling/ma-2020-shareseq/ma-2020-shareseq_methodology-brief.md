# Methodology Brief — ma-2020-shareseq

## 한 줄 결론 (모든 독자)
- Citation: `@ma2020shareseq`  |  Importance: `상` — 본 프로젝트 Dataset 2(GSE140203)의 원 출처이자 chromatin potential 개념의 시초.
- 한 문장 결론: 같은 single cell에서 ATAC+RNA를 동시 측정해 "chromatin accessibility가 RNA induction에 선행한다"를 paired data로 보인 foundational resource. 본 프로젝트 chromatin-transcription lag frame의 출발점이자 후속 도구 공통 benchmark.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` — GEO GSE140203 (mouse skin SHARE-seq, paired ATAC+RNA). 본 프로젝트 Dataset 2.
- 코드 공개: 3종 모두 GitHub open — `masai1116/SHARE-seq-alignmentV2`(V2), `masai1116/SHARE-seq-alignment`(V1, paper 시점), `broadinstitute/epi-SHARE-seq-pipeline`(official re-implementation). 검토필요: license는 각 repo에서 확인.
- 자원 요구: 추정 — assay 분석은 GPU 불요(chromatin potential = kNN $k=10$ + low-dim embedding). RAM은 cell 수에 비례, 본 프로젝트 환경(128GB)으로 충분. 미제공: 본문 runtime estimate 없음.
- 핵심 의존성: ATAC/RNA preprocessing + cis peak-gene association + DORC scoring + kNN matching 파이프라인. 검토필요: 정확한 library/version은 STAR Methods 미확보.
- 자세히 → [ma-2020-shareseq_core.md](ma-2020-shareseq_core.md) §Methods. 원문 PDF·supplementary는 sources에 없음(network 제한, paper-info.yaml `sources.paper.status: blocked`).

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: 부분일치 — GSE140203은 mouse skin이지만 modality 구조(paired ATAC+RNA)가 본인 담당 Human HSPC 10x Multiome(GSE209878)과 동일. 분석 frame은 cross-species로 이식 가능.
- 자원 가능성: 가능 — 공개 데이터 분석이 목적이라 wet-lab split-pool 재현은 불요. 분석 재현은 본 팀 역량 내.
- 비용·시간 추정: 분석 frame(peak-gene → DORC → lag) 시범 적용 ~1개월. confound 통제 추가 시 +α.
- ROI 한 줄: lag 정량화 frame의 직접 차용 대상 + Dataset 2 출처. 단 activation 방향만 grounding되고 shutdown lag·wall-clock 환산·confound 통제는 본 프로젝트가 추가해야 함.
- 자세히 → [ma-2020-shareseq_lens-industry.md](ma-2020-shareseq_lens-industry.md) §3 (BD value & 상용화).

## 본인 재회고 (본인)
- 질문: 본 데이터에서 burst kinetics(mean·variance)·cell cycle phase를 covariate로 통제한 뒤에도 chromatin-leads-RNA가 남는 gene set은 무엇인가? — 본 프로젝트 feature 후보 정의의 직접 입력.
- 질문: pseudotime 위의 "먼저"를 wall-clock으로 옮기는 anchoring은 이 paper에 없다. lag를 시간 단위로 쓰려면 별도 입증 필요.
- 다음 액션: confound-통제 후 priming gene set 재정의를 GSE140203에 시범 적용 — 다음 분기. (가장 낮은 비용·높은 영향, lens-academic 우선순위 1.)
- 자세히 → [ma-2020-shareseq_lens-academic.md](ma-2020-shareseq_lens-academic.md), [ma-2020-shareseq_lens-industry.md](ma-2020-shareseq_lens-industry.md) §4

---
마지막 갱신: 2026-06-09
