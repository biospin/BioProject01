# Methodology Brief — cui-2024-deepvelo

## 한 줄 결론 (모든 독자)

- Citation: `@cui2024deepvelo`  |  Importance: **중** — RNA-only이지만 *cell-specific kinetics*의 foundational reference. MoFlow / MultiVeloVAE 후속 method의 직접 background.
- 한 문장 결론: GCN + continuity loss로 *cell- and gene-specific* $(\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g})$를 학습하는 self-supervised RNA velocity framework — *multi-lineage/time-dependent direction 정확도*에서 scVelo 대비 우위, 그러나 chromatin 없음 → epigenomic-lag 직접 적용 불가.

## 재현 가능성 체크 (재현 담당자)

- **데이터 접근**: 발달 dataset은 `open` (GEO: GSE95753, GSE104323, GSE132188, GSE118068, GSE119945; Figshare 10.6084/m9.figshare.24716592.v1; scVelo-curated). PA는 `restricted` (EGA EGAS00001003170, controlled access).
- **코드 공개**: `https://github.com/bowang-lab/DeepVelo` + Zenodo DOI 10.5281/zenodo.10251639. MIT license. `검토필요:` 최근 commit / issue activity로 maintenance 상태.
- **자원 요구**: GPU 권장 (없으면 scVelo dynamical 대비 $4\times$, 있으면 $10$–$20\times$ speedup; hindbrain 13,501 cells 36초). Full-batch training (batch = $N$ cells) → ~30k cells까지 검증; 100k+는 *GPU memory 부담* (본 paper 미검증).
- **핵심 의존성**: Python + PyTorch + DGL (Deep Graph Library) + scVelo (preprocessing) + scanpy + numpy. `추정:` PyTorch >= 1.10, DGL >= 0.7.
- 자세히 → [cui-2024-deepvelo_core.md](cui-2024-deepvelo_core.md) §Methods, [sources/cui-2024-deepvelo.pdf](sources/cui-2024-deepvelo.pdf) §Methods p18–27.

## 우리 적용 가능성 (의사결정자)

- **Dataset 호환**: 우리 HSPC 10x Multiome (GSE209878)과 *modality mismatch* — DeepVelo는 RNA-only, 우리는 multi-ome. *chromatin information 활용 불가*. RNA-only baseline benchmark로는 사용 가능.
- **자원 가능성**: GPU 보유 + dataset 30k cell 이하면 학습 가능. Python 환경 standard.
- **비용·시간 추정**: *직접 적용 시*: ~2-3일 (preprocessing 통합 + 학습 + 결과 분석). *baseline benchmark 통합 시*: ~1일.
- **ROI 한 줄**: 직접 method 도입 ROI **낮음** (chromatin 없음, 후속 method가 보완). 그러나 *cell-specific kinetics motivation citation + benchmark 비교용으로 ROI **중**.*
- 자세히 → [cui-2024-deepvelo_lens-industry.md](cui-2024-deepvelo_lens-industry.md) §3 (BD value & 상용화).

## 본인 재회고 (본인)

- 핵심 follow-up 질문:
  - 질문: Bo Wang lab의 *multi-omic DeepVelo* 또는 *transformer-based velocity* 후속 paper / preprint가 있는가? (저자 future work에 명시)
  - 질문: DeepVelo의 *PA immunogenicity heterogeneity 발견* ($n=3$ patient)이 larger PA cohort 또는 higher-grade glioma에서 *재현*되었는가?
- 다음 액션: Week2 evidence bundle (`analysis/epigenomic-lag/_evidence/week2/`)에 DeepVelo의 *cell-specific kinetics 통계* (multifaceted gene $0.58$, direction score 비교)와 *MoFlow / MultiVeloVAE의 NEW vs borrowed contribution*을 인용 — 다음 sprint 안 (~1주일).
- 자세히 → [cui-2024-deepvelo_lens-academic.md](cui-2024-deepvelo_lens-academic.md) (Citation 후보 + DeepVelo's place in the deep-learning RNA velocity lineage), [cui-2024-deepvelo_lens-industry.md](cui-2024-deepvelo_lens-industry.md) §4.

---
마지막 갱신: 2026-05-26
