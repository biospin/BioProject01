---
name: share-seq-mouse-skin-model
description: Model gene-specific activation lag and shutdown lag in the SHARE-seq mouse skin GSE140203 dataset.
---

# SHARE-seq Mouse Skin Model

## 목표
SHARE-seq mouse skin differentiation에서 gene-specific chromatin/RNA lag structure를 추정하고, skin lineage 또는 differentiation state별 lag 차이를 모델링한다.

## 입력
- 전처리된 paired RNA/chromatin object.
- differentiation pseudotime 또는 lineage annotation.
- gene-level accessibility features, promoter/enhancer features, peak-to-gene linkage.
- timing estimate 또는 MultiVelo/MoFlow-style output.

## 작업 절차
1. preprocessing output의 modality pairing과 pseudotime direction을 확인한다.
2. gene별 chromatin opening/closing과 transcription onset/shutdown timing을 추정한다.
3. activation lag과 shutdown lag을 계산하고 confidence를 남긴다.
4. skin lineage별로 lag distribution을 비교한다.
5. baseline feature로 short/long lag 또는 continuous lag score를 예측한다.
6. held-out lineage 또는 cell state 기준으로 generalization을 평가한다.

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
- SHARE-seq sparsity 때문에 gene filtering과 confidence threshold를 명시한다.
- lineage별 sampling imbalance가 model evaluation에 미치는 영향을 확인한다.

