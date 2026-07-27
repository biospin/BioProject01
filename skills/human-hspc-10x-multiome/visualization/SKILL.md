---
name: human-hspc-10x-multiome-visualization
description: Visualize preprocessing, lag estimates, model outputs, and hematopoietic lineage interpretation for the human HSPC 10x Multiome GSE209878 dataset.
---

# Human HSPC 10x Multiome Visualization

## 목표
Human HSPC 10x Multiome 분석 결과를 HSPC subpopulation, lineage commitment trajectory, gene-specific lag, model performance 관점에서 시각화한다.

## 우선 Figure
- UMAP with HSPC subpopulation and lineage labels.
- QC summary by sample/batch.
- lineage commitment pseudotime plot.
- activation lag/shutdown lag distribution by lineage.
- representative hematopoietic regulator genes dynamics.
- predicted vs observed lag and feature importance.
- uncertainty or missingness summary.

## 작업 절차
1. lineage별 trajectory와 pseudotime root를 Figure caption에 명시한다.
2. rare population은 별도 panel 또는 annotation으로 보존한다.
3. representative gene plot은 accessibility와 RNA dynamics를 함께 보여준다.
4. model performance는 split 기준과 lineage composition을 함께 표시한다.

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


## ▶ 우리 실행 구현 (kkkim-pipeline)
- (예정) P5 결과 시각화 — lag 분포(lineage별), method concordance, UMAP/trajectory. design/presentation은 이 단계로 통합.
