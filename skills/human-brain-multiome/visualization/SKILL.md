---
name: human-brain-multiome-visualization
description: Visualize preprocessing, lag estimates, model outputs, and developmental interpretation for the human brain multi-ome GSE162170 dataset.
---

# Human Brain Multiome Visualization

## 목표
Human brain multiome 분석 결과를 donor/stage/region/cell type 구조, developmental trajectory, gene-specific lag, model performance 관점에서 시각화한다.

## 우선 Figure
- UMAP with cell type, donor, developmental stage, brain region.
- QC and batch summary.
- lineage별 pseudotime trajectory.
- chromatin/RNA timing scatter.
- activation lag/shutdown lag distribution by lineage.
- model performance by held-out donor or lineage.
- representative neurodevelopmental genes dynamics.

## 작업 절차
1. donor, region, stage가 Figure에서 어떻게 표시되는지 명시한다.
2. pseudotime 또는 developmental stage axis를 혼동하지 않게 caption을 작성한다.
3. model performance plot은 split 기준을 함께 표시한다.
4. biological interpretation은 developmental lineage별로 분리한다.

## 출력 형식
```markdown
## Visualization Plan
- Dataset:
- Figures:
- Required inputs:
- Aesthetic rules:
- Captions:
- Interpretation notes:
```

