---
name: human-hspc-10x-multiome-preprocessing
description: Preprocess the human HSPC 10x Multiome dataset GSE209878 for gene-specific epigenomic lag analysis. Use when Codex needs to inspect, normalize, annotate, integrate, or prepare hematopoietic stem/progenitor multiome inputs.
---

# Human HSPC 10x Multiome Preprocessing

## Dataset
- Name: Human HSPC 10x Multiome
- Accession: GSE209878
- Biology: hematopoietic stem/progenitor state
- Data type: human 10x multiome
- Main use: baseline human hematopoietic dataset for gene-specific lag analysis.

## 목표
GSE209878 human HSPC 10x Multiome 데이터를 hematopoietic lineage와 progenitor differentiation timing 분석에 맞게 전처리한다.

## 우선 확인 항목
- GSE209878 원본 또는 processed file 위치.
- human genome build와 gene annotation source.
- RNA matrix, ATAC fragments/peak matrix, peak annotation.
- cell type, HSPC subpopulation, lineage commitment, pseudotime annotation.
- donor/sample/batch metadata.
- hematopoietic lineage별 충분한 cell count.

## 작업 절차
1. `data/human-hspc-10x-multiome/` 또는 사용자가 지정한 입력 경로를 확인한다.
2. accession, processed/raw 여부, metadata source를 기록한다.
3. RNA/ATAC modality pairing과 QC를 확인한다.
4. HSPC subpopulation과 lineage annotation을 정리한다.
5. promoter/enhancer accessibility와 peak-to-gene linkage feature를 만든다.
6. lineage commitment pseudotime 또는 ordering을 확인한다.
7. 산출물은 `work/human-hspc-10x-multiome/` 또는 `results/human-hspc-10x-multiome/` 아래에 저장한다.

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
- lineage commitment 방향과 pseudotime root를 명확히 기록한다.
- rare population은 filtering으로 사라지지 않도록 기준을 따로 검토한다.


## ▶ 우리 실행 구현 (kkkim-pipeline)
- `pipeline/hspc-velocity-benchmark/scripts/p1_build.py` — 통일 전처리(공통 branch): GEX/ATAC 분리, spliced/unspliced 병합, timepoint 라벨, method-agnostic Leiden
- `pipeline/hspc-velocity-benchmark/scripts/check_data.py` — 산출물 검증
- `pipeline/hspc-velocity-benchmark/P1_README.md`, `env/scv-preprocess.yml`
