# Methodology Brief — li-2023-celldancer

## 한 줄 결론 (모든 독자)

- Citation: `@li2023celldancer` | Importance: **중** — MoFlow의 *direct methodological predecessor*로 계보 설명·RNA-only baseline 비교에 필수, chromatin 부재로 우리 핵심 task에는 간접 가치.
- 한 문장 결론: *Latent time 없는 local cosine loss + gene별 DNN*으로 cell-specific $(\alpha, \beta, \gamma)$를 추정하는 RNA-only relay velocity method. MoFlow가 이 architecture를 chromatin-aware로 확장 → 우리 프로젝트에서는 *RNA-only baseline + 방법론 계보 인용*.

## 재현 가능성 체크 (재현 담당자)

- 데이터 접근: `open` — 사용 dataset 6종 모두 public (GSE132188 pancreas, GSE95753 hippocampus, E-MTAB-6967 erythroid, SRP129388 human embryo, GSE128365 RPE1 FUCCI, 그리고 simulation은 SciPy로 자체 생성). scVelo / dynamo CLI로 즉시 access.
- 코드 공개: https://github.com/GuangyuWangLab2021/cellDancer (PyTorch Lightning). `검토필요: license 명시 부재 — GitHub 직접 확인 필요. 상업 사용 가능 여부 미확정.` 미제공: maintenance 상태 (active / archived) 본문 부재.
- 자원 요구: CPU 24-core Intel Xeon W에서 18,140 cells × 2,159 genes / 15 jobs / 40 min (Extended Data Fig. 10). GPU 필수 아님. 100k+ cells 또는 20k+ genes 확장 시 *재추정 필요*. 미제공: RAM 요구량 본문 부재 — `해석: dataset 크기 기준 32–64GB 추정.`
- 핵심 의존성: `pytorch-lightning` (ref. 49), `scipy >= 1.0` (ref. 50, RK ODE solver), `scvelo` (pre-processing), `scanpy` (data handling), `dynamo` (downstream vector field / perturbation, ref. 22). 특정 version 명시 부재.
- 자세히 → [li-2023-celldancer_core.md](li-2023-celldancer_core.md) §Methods, [sources/li-2023-celldancer.pdf](sources/li-2023-celldancer.pdf) §Methods p11–13

## 우리 적용 가능성 (의사결정자)

- Dataset 호환: 우리 4 dataset (10x mouse brain, SHARE-seq mouse skin, human brain multiome, HSPC 10x multiome) 모두 *chromatin + RNA* — cellDancer는 *RNA-only 사용*. 본질적 fit *약함* — 단 RNA-only baseline 비교용으로는 OK.
- 자원 가능성: 우리 환경 (CPU multi-core 가용)에서 직접 적용 가능. 18k cells 40분 — *2일 안에 4 dataset 전부 RNA-only baseline 결과 얻기 가능*.
- 비용·시간 추정: HSPC dataset에 cellDancer 단독 적용 + 4-way 비교 table (cellDancer / scVelo / MultiVelo / MoFlow / MultiVeloVAE) 작성 — ~ 2주 wall time, 1 person-week.
- ROI 한 줄: *MoFlow 결과의 ablation 의미* 부여 — *chromatin modality의 실제 contribution*을 RNA-only cellDancer baseline 대비 정량으로 보여주는 *과학적 가치*. 자체 BD 가치는 약함.
- 자세히 → [li-2023-celldancer_lens-industry.md](li-2023-celldancer_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)

- 핵심 follow-up 질문 1–2개:
  - `질문: cellDancer GitHub license 확인 — 상업 사용 가능 여부 + 우리 fork 가능 여부 결정.`
  - `질문: 우리 HSPC dataset에 cellDancer 적용 시 cell cycle confound 처리 (pre-filter vs post-hoc regression)?`
- 다음 액션: HSPC subset에 cellDancer 적용 시도 + MoFlow와 head-to-head CBDir 비교 — 다음 분기 (~2주). 결과는 `analysis/epigenomic-lag/_evidence/week2/comparison_table.md`에 추가.
- 자세히 → [li-2023-celldancer_lens-academic.md](li-2023-celldancer_lens-academic.md) (cellDancer→MoFlow 진화 sub-section), [li-2023-celldancer_lens-industry.md](li-2023-celldancer_lens-industry.md) §4

---
마지막 갱신: 2026-05-26
