---
name: celltype-annotation
description: Analyze cell type annotation methodology in a single-cell or multi-ome paper. Use when a paper assigns cell type labels to clusters and Codex needs to explain what annotation strategy was used, what marker genes or reference datasets were relied on, how ambiguous or rare cell types were handled, and how annotation quality was validated.
---

# Cell Type Annotation

## 목표
논문에서 cell type annotation이 어떤 전략으로 이루어졌는지, 그 신뢰도를 어떻게 확보했는지 분석한다. Annotation이 단순 marker gene 조회인지, reference-based transfer인지, semi-supervised 방식인지 구분하고, 각 방식의 한계와 논문이 그 한계를 어떻게 다뤘는지 평가한다.

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `cell type`, `cluster`, `marker gene`, `UMAP`, `leiden`, `louvain`, `label transfer`, `reference`, `annotation`, `doublet`, `ambient RNA`, `confidence score`, `DEG`, `trajectory`, `progenitor`, `lineage`, `FACS`, `IHC`, `snRNA-seq`, `scRNA-seq`, `snATAC-seq`, `scATAC-seq`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 처음 사용할 때는 필요한 경우 짧게 한국어 설명을 붙인다.

## 사용 시점
다음 중 하나 이상을 만족할 때 이 skill을 사용한다.
- 논문이 세포 유형을 분류하고 그 분류 결과가 downstream 분석의 입력이 되는 경우.
- annotation 전략이 논문 결론에 직접 영향을 주는 경우 (예: 특정 cell type에서만 효과가 나타남).
- 논문이 새로운 cell type을 발견했다고 주장하는 경우.
- multi-ome 또는 atlas-scale 데이터에서 annotation 일관성이 중요한 경우.

## 작업 절차
1. Methods와 Supplementary에서 annotation 관련 section을 먼저 찾는다.
2. Annotation 전략을 분류한다.
   - **Marker-based**: known marker gene 기반 수동 또는 자동 annotation
   - **Reference-based (label transfer)**: 공개 reference dataset 또는 atlas 사용 (예: Allen Brain Atlas, PBMC reference, Seurat label transfer, Azimuth, scANVI)
   - **Semi-supervised / self-supervised**: 부분 레이블을 이용한 학습 기반 annotation
   - **Manual curation**: 전문가가 직접 cluster를 검토한 경우
3. 사용한 marker gene 또는 reference를 정리한다.
4. Ambiguous cell, doublet, low-quality cell 처리 방법을 확인한다.
5. Annotation confidence를 어떻게 평가했는지 확인한다.
   - confidence score, prediction score, entropy 기반 filter가 있는가?
   - 여러 방법을 앙상블하거나 cross-check 했는가?
6. Annotation 검증 방법을 확인한다.
   - 독립 데이터셋 또는 외부 atlas와 일치하는가?
   - 실험적 검증 (FACS, IHC, smFISH 등)이 있는가?
   - DEG 기반 cluster 특이성 확인이 있는가?
7. Annotation 한계를 평가한다.
   - 논문이 다루지 못한 cell type이 있는가?
   - Rare cell type, transition state, ambiguous cluster는 어떻게 처리했는가?
   - Reference dataset의 tissue/species mismatch가 있는가?

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 아래 구조를 따른다.

```markdown
### Cell Type Annotation

#### Annotation 전략
- 사용한 방식:
- 참조 데이터셋 / 마커:
- 소프트웨어 / 방법:

#### Annotation 대상
- 데이터셋:
- 총 cell 수:
- 최종 annotation된 cell type 목록:
- Rare / ambiguous cell type 처리:

#### 품질 관리
- Doublet / low-quality cell 필터 방법:
- Confidence score 또는 필터 기준:
- Annotation 불확실성 표시 여부:

#### 검증 방법
- 내부 검증 (DEG, marker 일치 등):
- 외부 검증 (독립 dataset, 실험적 검증):
- Cross-modal 일치 확인 (RNA ↔ ATAC 등):

#### Annotation 한계
- 논문이 명시한 한계:
- 분석자가 판단한 한계:
- 하위 분석에 미치는 영향:
```

## 판단 기준

**신뢰도가 높은 annotation의 특징:**
- 복수의 독립적인 방법으로 일치하는 결과
- Marker gene과 reference-based 결과가 일치
- 실험적 검증 (FACS 또는 in situ) 존재
- confidence score threshold가 명시됨

**주의가 필요한 annotation의 특징:**
- 단일 marker gene 하나에만 의존
- Reference dataset의 tissue 또는 species가 다름
- Ambiguous cluster를 "Unknown"으로 무시
- Rare cell type을 인접 cluster에 병합
- Annotation이 UMAP 시각화에만 근거

## 주의할 점
- Annotation 전략 설명이 Methods에 짧게만 있으면 Supplementary와 Code Availability를 확인한다.
- Label transfer score가 제시되지 않으면 `confidence 미제시`로 표시한다.
- 논문이 새 cell type을 발견했다고 주장하면, 그 주장이 실험적으로 검증되었는지 반드시 확인한다.
- Annotation 결과가 downstream 분석 (trajectory, velocity, DEG)에 얼마나 의존하는지 평가한다.
