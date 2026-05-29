---
name: multiome-integration
description: Evaluate multi-ome integration quality in a paper that jointly analyzes scRNA-seq and scATAC-seq (or other paired modalities). Use when Codex needs to assess whether modality alignment is reliable, what integration method was used, how concordance between modalities was measured, and whether integration artifacts could affect downstream conclusions.
---

# Multi-ome Integration Quality

## 목표
Multi-ome 데이터의 modality 통합이 얼마나 신뢰할 수 있는지 평가한다. RNA와 ATAC이 같은 세포에서 측정되더라도 통합 방법, 품질 관리, concordance 확인이 부족하면 downstream 분석 (cell type annotation, trajectory, velocity)의 결론이 artifact일 수 있다. 이 skill은 통합 품질의 약점과 강점을 분리해서 평가한다.

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `scRNA-seq`, `scATAC-seq`, `snRNA-seq`, `snATAC-seq`, `10x Multiome`, `SHARE-seq`, `SNARE-seq`, `paired`, `co-embedding`, `WNN`, `MOFA`, `MOFA+`, `MultiVI`, `ArchR`, `Signac`, `Seurat`, `LSI`, `peak matrix`, `gene activity`, `fragment`, `TSS enrichment`, `FRiP`, `doublet`, `barcode`, `ambient`, `batch effect`, `modality weight`, `concordance`, `co-accessibility`, `gene-peak linkage`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 처음 사용할 때는 필요한 경우 짧게 한국어 설명을 붙인다.

## 사용 시점
다음 중 하나 이상을 만족할 때 이 skill을 사용한다.
- 논문이 scRNA-seq과 scATAC-seq을 paired 또는 joint로 분석하는 경우.
- Multi-ome 통합 결과가 cell type annotation, trajectory, velocity, peak-gene linkage 등 핵심 분석의 입력이 되는 경우.
- 통합 방법 또는 품질 지표가 논문 결론에 직접 영향을 주는 경우.

## 작업 절차
1. Methods에서 data preprocessing과 integration pipeline을 먼저 찾는다.
2. 데이터 유형을 확인한다.
   - 진정한 paired (같은 세포에서 동시 측정): 10x Multiome, SHARE-seq, SNARE-seq 등
   - In silico paired (별도 측정 후 통합): Seurat v4 bridge integration, LIGER, Harmony 등
3. ATAC 데이터 품질 지표를 정리한다.
   - TSS enrichment score
   - FRiP (Fraction of Reads in Peaks)
   - 세포당 fragment 수
   - Doublet 제거 여부 및 방법
4. RNA 데이터 품질 지표를 정리한다.
   - 세포당 UMI 수, gene 수
   - Mitochondrial read 비율 필터
   - Ambient RNA 보정 여부 (SoupX, CellBender 등)
5. 통합 방법을 분류한다.
   - Joint embedding: WNN (Seurat), MultiVI, MOFA+
   - Sequential: ATAC → LSI → joint clustering
   - 각 modality의 weight 또는 기여도가 명시되어 있는가?
6. Modality concordance를 어떻게 확인했는지 평가한다.
   - RNA-based와 ATAC-based cell type annotation이 일치하는가?
   - Gene activity score와 RNA expression이 상관관계를 보이는가?
   - Peak-gene linkage 또는 co-accessibility가 검증되었는가?
7. Batch effect 처리 방법을 확인한다.
   - 샘플 간 또는 실험 배치 간 보정 방법이 있는가?
8. 통합 품질의 한계를 평가한다.
   - Modality 간 cell 수 불균형이 있는가?
   - 특정 cell type에서 ATAC 신호가 너무 sparse하지 않은가?
   - 통합 embedding이 실제 biology를 반영하는지 아니면 batch를 반영하는지 불분명한가?

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 아래 구조를 따른다.

```markdown
### Multi-ome Integration Quality

#### 데이터 유형
- 측정 방법 (paired / in silico):
- 플랫폼:
- 총 세포 수 (RNA / ATAC):
- 샘플 수 및 조건:

#### ATAC 품질 지표
- TSS enrichment:
- FRiP:
- 세포당 fragment 수:
- Doublet 제거 방법:
- Peak calling 방법:

#### RNA 품질 지표
- 세포당 UMI 수:
- 세포당 gene 수:
- MT 비율 필터:
- Ambient RNA 보정:

#### 통합 방법
- 사용한 방법:
- 각 modality 가중치 또는 기여도:
- Batch effect 보정:
- 통합 결과 표현 (UMAP, co-embedding 등):

#### Modality Concordance 확인
- RNA ↔ ATAC cell type 일치 여부:
- Gene activity ↔ RNA 상관관계:
- Peak-gene linkage 검증:
- Concordance 확인에 사용한 방법:

#### 통합 품질 한계
- 논문이 명시한 한계:
- 분석자가 판단한 한계:
- Downstream 분석에 미치는 영향:
```

## 판단 기준

**신뢰도가 높은 통합의 특징:**
- TSS enrichment > 4, FRiP > 0.3 이상 보고
- RNA와 ATAC 기반 annotation이 독립적으로 일치
- Gene activity score와 RNA expression의 positive correlation 확인
- WNN modality weight가 cell type별로 다르게 나타남 (biology를 반영하는 신호)
- Peak-gene linkage가 독립 데이터셋 또는 eQTL과 부합

**주의가 필요한 통합의 특징:**
- ATAC 품질 지표 미보고
- 통합 후 concordance 확인 없음
- In silico paired에서 integration score 미제시
- ATAC sparse cell type이 downstream 분석에 그대로 포함
- Batch가 biology보다 UMAP cluster를 더 잘 설명함

## 주의할 점
- ATAC 데이터는 RNA보다 sparse하므로 cell 수와 coverage가 충분한지 반드시 확인한다.
- `gene activity score`는 peak-to-gene heuristic이며 실제 expression과 다를 수 있다. 이를 RNA의 proxy로 직접 사용한 경우 그 한계를 표시한다.
- 통합 방법이 unsupervised embedding이면 cluster 경계가 soft하고 세포 유형 경계가 통합 방법에 의존할 수 있다.
- Paired multiome이더라도 sequencing depth 불균형 (RNA가 깊고 ATAC이 얕은 경우)은 modality 가중치에 영향을 준다.
- 통합 품질 확인 없이 velocity, trajectory, gene-peak linkage를 주요 결론으로 사용하면 `통합 품질 미검증`으로 표시한다.
