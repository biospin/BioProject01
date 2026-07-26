---
name: 10x-embryonic-mouse-brain-preprocessing
description: Preprocess the 10x embryonic mouse brain multiome dataset for gene-specific epigenomic lag analysis. Use when Codex needs to inspect, normalize, annotate, integrate, or prepare ATAC/RNA inputs from embryonic mouse brain differentiation before modeling.
---

# 10x Embryonic Mouse Brain Preprocessing

## Dataset
- Name: 10x embryonic mouse brain
- Biology: embryonic brain differentiation
- Data type: 10x multiome
- Main use: baseline multi-omic dataset for estimating chromatin/RNA timing and gene-specific lag structure.

## 목표
10x embryonic mouse brain multiome 데이터를 lag modeling에 들어갈 수 있는 형태로 정리한다. RNA counts, ATAC peak/accessibility matrix, gene annotation, cell metadata, trajectory 또는 lineage annotation을 함께 점검하고, gene-level activation/shutdown lag 계산에 필요한 입력 테이블을 만든다.

## 우선 확인 항목
- 원본 데이터 위치와 다운로드 source.
- genome build와 gene annotation source.
- RNA matrix, ATAC fragments 또는 peak matrix, peak annotation 존재 여부.
- cell barcode matching, modality pairing, sample/library metadata.
- cell type, developmental stage, lineage, pseudotime annotation.
- raw data와 intermediate output을 분리하는 경로.

## 작업 절차
1. `data/10x-embryonic-mouse-brain/` 또는 사용자가 지정한 입력 경로를 확인한다.
2. 파일 형식은 확장자만 믿지 말고 header, shape, obs/var metadata, 일부 record를 확인한다.
3. RNA와 ATAC barcode overlap을 확인한다.
4. QC 지표를 계산하거나 기존 QC columns를 확인한다.
5. gene annotation, promoter/enhancer definition, peak-to-gene linkage 기준을 기록한다.
6. trajectory 또는 pseudotime 정보가 있으면 time axis 정의를 저장한다.
7. modeling용 산출물을 `work/10x-embryonic-mouse-brain/` 또는 `results/10x-embryonic-mouse-brain/` 아래에 저장한다.

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
- 원본 파일은 덮어쓰지 않는다.
- mouse gene id와 gene symbol mapping을 명확히 남긴다.
- pseudotime과 real developmental stage를 섞어서 해석하지 않는다.

