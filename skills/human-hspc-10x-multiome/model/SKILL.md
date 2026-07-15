---
name: human-hspc-10x-multiome-model
description: Model gene-specific activation lag and shutdown lag in the human HSPC 10x Multiome GSE209878 dataset.
---

# Human HSPC 10x Multiome Model

## 목표
GSE209878 human HSPC 10x Multiome에서 hematopoietic lineage commitment에 따른 gene-specific activation/shutdown lag을 추정하고, baseline chromatin features가 response timing을 설명하는지 모델링한다.

## 입력
- 전처리된 human HSPC RNA/ATAC multiome object.
- HSPC subpopulation, lineage, pseudotime annotation.
- gene-level accessibility, motif, promoter/enhancer, peak-to-gene features.
- chromatin/RNA timing estimates.

## 작업 절차
1. lineage별 pseudotime root와 direction을 확인한다.
2. gene별 chromatin opening/closing과 transcription onset/shutdown timing을 추정한다.
3. activation lag과 shutdown lag을 계산한다.
4. lineage commitment별 lag distribution을 비교한다.
5. baseline epigenomic features로 lag score를 예측한다.
6. held-out lineage 또는 held-out subpopulation 기준으로 generalization을 평가한다.

## 출력 형식
```markdown
## Model Plan
- Dataset:
- Time axis:
- Lag definition:
- Features:
- Model:
- Evaluation:
- Outputs:
- Limitations:
```

## 주의할 점
- HSPC differentiation branch별 timing을 하나의 global pseudotime으로 강제로 합치지 않는다.
- rare lineage의 uncertainty를 별도로 표시한다.


## ▶ 우리 실행 구현 (kkkim-pipeline)
- `pipeline/hspc-velocity-benchmark/DESIGN.md` — velocity method head-to-head 벤치마크 = model 단계의 **"어떤 method로 lag를 추정할지" method-selection** (MultiVelo/MultiVeloVAE/MoFlow/CRAK-Velo + RNA-only floor)
- `pipeline/hspc-velocity-benchmark/REVIEW-methodologist-2026-06-13.md` — 설계 adversarial 검토
- env: `env/velo-mv.yml`(MultiVelo+scVelo), `env/velo-torch.yml`, `env/velo-tf.yml`
