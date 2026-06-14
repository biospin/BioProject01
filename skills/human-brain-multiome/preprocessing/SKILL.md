---
name: human-brain-multiome-preprocessing
description: Preprocess the human brain multi-ome dataset GSE162170 for gene-specific epigenomic lag analysis. Use when Codex needs to inspect, normalize, annotate, integrate, or prepare fetal/developing human brain multiome inputs.
---

# Human Brain Multiome Preprocessing

## Dataset
- Name: Human brain multi-ome
- Accession: GSE162170
- Biology: fetal / developing human brain
- Data type: human multiome
- Main use: baseline human developmental dataset for gene-specific epigenomic lag analysis.

## 목표
GSE162170 human brain multiome 데이터를 lag modeling에 필요한 RNA/ATAC, cell type, developmental trajectory, regulatory feature 형태로 정리한다.

## 우선 확인 항목
- GSE162170 원본 또는 processed file 위치.
- human genome build와 gene annotation source.
- donor, developmental stage, brain region, batch metadata.
- RNA matrix, ATAC fragments/peak matrix, peak annotation.
- cell type, lineage, pseudotime 또는 developmental ordering.
- donor/batch correction 필요성.

## 작업 절차
1. `data/human-brain-multiome/` 또는 사용자가 지정한 입력 경로를 확인한다.
2. accession, portal URL, processed/raw 여부를 기록한다.
3. donor, region, stage, batch metadata를 분리해서 정리한다.
4. RNA/ATAC modality pairing과 QC를 확인한다.
5. promoter/enhancer feature와 peak-to-gene linkage를 human annotation 기준으로 만든다.
6. trajectory 또는 developmental axis 정의를 기록한다.
7. 산출물은 `work/human-brain-multiome/` 또는 `results/human-brain-multiome/` 아래에 저장한다.

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
- donor, region, developmental stage confounding을 모델링 전에 확인한다.
- human gene annotation version을 명확히 남긴다.

