---
name: 10x-embryonic-mouse-brain-visualization
description: Visualize preprocessing, lag estimates, model outputs, and biological interpretation for the 10x embryonic mouse brain multiome dataset.
---

# 10x Embryonic Mouse Brain Visualization

## 목표
10x embryonic mouse brain 분석 결과를 cell state, trajectory, chromatin/RNA timing, gene-specific lag, model performance 관점에서 시각화한다.

## 우선 Figure
- UMAP 또는 trajectory plot with cell type/developmental stage.
- RNA/ATAC QC summary.
- chromatin opening time vs transcription onset time scatter.
- activation lag/shutdown lag distribution.
- lineage별 lag heatmap.
- predicted vs observed lag 및 feature importance.
- representative genes의 accessibility/RNA dynamics plot.

## 작업 절차
1. visualization input이 어떤 preprocessing/model output에서 왔는지 기록한다.
2. axis, unit, pseudotime direction, lineage definition을 Figure caption에 남긴다.
3. gene별 lag plot은 missingness와 confidence를 구분해 표시한다.
4. biological interpretation은 model output이 지지하는 범위 안에서만 작성한다.

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

