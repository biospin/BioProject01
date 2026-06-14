---
name: human-brain-multiome-model
description: Model gene-specific activation lag and shutdown lag in the human brain multi-ome GSE162170 dataset.
---

# Human Brain Multiome Model

## 목표
GSE162170 human developing brain multiome에서 cell type 또는 lineage별 chromatin/RNA timing 차이를 고려해 gene-specific lag structure를 추정한다.

## 입력
- 전처리된 human RNA/ATAC multiome object.
- donor, brain region, developmental stage, cell type metadata.
- pseudotime 또는 developmental ordering.
- gene-level regulatory features와 timing estimates.

## 작업 절차
1. preprocessing output의 donor/stage/region confounding을 확인한다.
2. lineage 또는 cell type별 time axis를 정의한다.
3. gene별 activation lag과 shutdown lag을 계산한다.
4. donor 또는 batch effect를 고려한 model specification을 정한다.
5. baseline epigenomic features로 continuous lag 또는 short/long class를 예측한다.
6. held-out donor, held-out lineage, held-out brain region evaluation을 우선 고려한다.

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
- human developmental data에서는 donor/stage/region 효과를 lag로 오해하지 않도록 한다.
- cross-species 비교를 한다면 mouse dataset과 annotation mapping 기준을 별도로 기록한다.

