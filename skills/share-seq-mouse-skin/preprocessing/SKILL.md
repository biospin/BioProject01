---
name: share-seq-mouse-skin-preprocessing
description: Preprocess the SHARE-seq mouse skin dataset GSE140203 for gene-specific epigenomic lag analysis. Use when Codex needs to inspect, normalize, annotate, integrate, or prepare paired chromatin and RNA inputs from mouse skin differentiation.
---

# SHARE-seq Mouse Skin Preprocessing

## Dataset
- Name: SHARE-seq mouse skin
- Accession: GSE140203
- Biology: mouse skin differentiation
- Data type: paired chromatin + RNA
- Main use: baseline dataset for chromatin/RNA timing during differentiation.

## 목표
SHARE-seq mouse skin 데이터를 lag modeling에 필요한 paired chromatin/RNA representation으로 정리한다. mouse skin differentiation trajectory, lineage/cell state annotation, gene-level accessibility feature를 함께 검증한다.

## 우선 확인 항목
- GSE140203 원본 또는 processed file 위치.
- genome build와 gene annotation source.
- RNA matrix, chromatin accessibility matrix, peak annotation.
- paired modality barcode mapping.
- skin lineage, differentiation stage, pseudotime annotation.
- SHARE-seq 특이적인 sparsity와 batch structure.

## 작업 절차
1. `data/share-seq-mouse-skin/` 또는 사용자가 지정한 입력 경로를 확인한다.
2. accession, download source, processed/raw 여부를 기록한다.
3. RNA와 chromatin modality의 cell matching을 확인한다.
4. QC와 filtering 기준을 modality별로 분리한다.
5. peak-to-gene linkage와 promoter/enhancer feature를 만든다.
6. pseudotime 또는 differentiation axis를 확인하고 방향성을 기록한다.
7. 산출물은 `work/share-seq-mouse-skin/` 또는 `results/share-seq-mouse-skin/` 아래에 저장한다.

## 출력 형식
```markdown
## Preprocessing Plan
- Dataset:
- Input files:
- Metadata checked:
- QC criteria:
- Genome build / annotation:
- Time axis:
- Outputs:
- Open issues:
```

## 주의할 점
- SHARE-seq processed object의 annotation이 어떤 genome build에 맞는지 확인한다.
- differentiation pseudotime 방향이 biological maturation과 일치하는지 점검한다.

