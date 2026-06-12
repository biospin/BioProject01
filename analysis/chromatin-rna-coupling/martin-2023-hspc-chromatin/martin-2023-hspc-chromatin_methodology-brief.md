# Methodology Brief — martin-2023-hspc-chromatin

## 한 줄 결론 (모든 독자)
- Citation: `@martin2023hspcchromatin`  |  Importance: `중` (chromatin priming의 primary 근거이자 방법 참조 가치가 높으나 human·paired RNA·lag 정량은 없음)
- 한 문장 결론: mouse HSPC 13 cell type ATAC-seq로 chromatin priming(접근성이 발현에 선행)을 trajectory 전체에서 정량하고 CRISPRi로 CRE→유전자 인과를 검증한 연구 — 우리 activation lag 가설의 방향성 배경 citation + 분석 설계 참조로 차용.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: `open` — GEO GSE184851(이 연구), GSE162949(선행). UCSC custom track `genome.ucsc.edu/s/ewmartin/atac_bw_mean_allpeaks`.
- 코드 공개: 전용 repo 없음. 모두 public tool — ENCODE ATAC-seq pipeline(v1.1.6/1.4.2), chromVAR, HOMER, GREAT, CRISPOR. (재현 시 파라미터는 본문 Data Processing 절 그대로 사용 가능.)
- 자원 요구: `해석:` bulk ATAC-seq 13 cell type ×2 replicate — 표준 CPU 클러스터로 충분, GPU 불필요. wet lab(FACS, ATAC, CRISPRi mouse 사육)이 실제 병목.
- 핵심 의존성: ENCODE atac-seq-pipeline(mm10), chromVAR(R), HOMER, GREAT, bedtools, GraphPad Prism 9. CRISPRi mouse(dCas9-KRAB@H11) 별도 확보 필요.
- 자세히 → [martin-2023-hspc-chromatin_core.md](martin-2023-hspc-chromatin_core.md) §Methods, [sources/martin-2023-hspc-chromatin.pdf](sources/martin-2023-hspc-chromatin.pdf) §Experimental Procedures(p.534-536)

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: **부분일치** — 우리는 Human HSPC 10x Multiome(GSE209878, single-cell + paired RNA), 본 논문은 mouse bulk ATAC + 외부 expression. modality·종 불일치로 그대로 재현 불가.
- 자원 가능성: 분석 설계(primed peak 유지 정량) 차용은 즉시 가능. mouse 실험 재현은 우리 범위 밖(불필요).
- 비용·시간 추정: CRE 좌표 hg38 liftover + 우리 ATAC overlap 검증은 ~1주 분석. lag 가설 background citation 정리는 즉시.
- ROI 한 줄: lag 가설의 생물학적 정당화 근거 + primed CRE feature prior로 가져올 가치 있음. 직접 재현 ROI는 낮음(modality 불일치).
- 자세히 → [martin-2023-hspc-chromatin_lens-industry.md](martin-2023-hspc-chromatin_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)
- `질문:` mouse HSC-unique/lineage-primed CRE 좌표를 hg38 liftover하면 우리 Human HSPC ATAC peak과 얼마나 겹치나? baseline primed-CRE feature로 쓸 수준인가?
- `질문:` 본 논문 Fig 6C의 "HSC-primed peak <25% 유지" — 우리 multiome에서 "열렸으나 미발현" CRE 비율과 비교 가능한가? lag 측정에서 이 background state를 어떻게 처리할지 정책 필요.
- 다음 액션: lag 가설 문서 background에 priming 정의·수치 인용 추가(즉시). CRE liftover overlap 검증은 다음 multiome sprint(~2주 내)에 묶어 진행.
- 자세히 → [martin-2023-hspc-chromatin_lens-academic.md](martin-2023-hspc-chromatin_lens-academic.md), [martin-2023-hspc-chromatin_lens-industry.md](martin-2023-hspc-chromatin_lens-industry.md) §4

---
마지막 갱신: 2026-06-12
