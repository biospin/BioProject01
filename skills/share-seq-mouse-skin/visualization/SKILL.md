---
name: share-seq-mouse-skin-visualization
description: Visualize preprocessing, lag estimates, model outputs, and differentiation interpretation for the SHARE-seq mouse skin dataset.
---

# SHARE-seq Mouse Skin Visualization

## 목표
SHARE-seq mouse skin 분석 결과를 differentiation trajectory, paired chromatin/RNA dynamics, lineage-specific lag, feature predictor 성능 중심으로 시각화한다.

## 우선 Figure
- UMAP 또는 trajectory plot with skin cell state.
- RNA/chromatin QC summary.
- pseudotime별 accessibility/RNA dynamics.
- activation lag/shutdown lag distribution.
- lineage 또는 cell state별 lag comparison.
- predicted vs observed lag.
- representative genes and regulatory peaks plot.

## 작업 절차
1. Figure별 input file과 preprocessing/model version을 기록한다.
2. pseudotime direction과 lineage label을 caption에 명시한다.
3. paired chromatin/RNA plot에서는 smoothing 방법과 window를 기록한다.
4. confidence 낮은 gene은 별도 색상 또는 필터로 처리한다.

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

