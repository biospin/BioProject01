---
name: human-hspc-10x-multiome-download
description: Download or register the human HSPC 10x Multiome dataset GSE209878 for gene-specific epigenomic lag analysis. Use when Codex needs to find official data sources, fetch raw or processed files, verify files, or create a download manifest before preprocessing.
---

# Human HSPC 10x Multiome Download

## Dataset
- Name: Human HSPC 10x Multiome
- Accession: GSE209878
- Biology: hematopoietic stem/progenitor state
- Data type: human 10x multiome
- Main use: baseline human hematopoietic dataset for gene-specific lag analysis.

## 목표
GSE209878 human HSPC 10x Multiome 데이터를 GEO/SRA, 원 논문 supplement, 또는 공식 data portal에서 확인하고, HSPC subpopulation과 lineage metadata를 보존한 다운로드 manifest를 만든다.

## 우선 확인 항목
- GEO Series GSE209878, linked SRA runs, supplementary files, 원 논문/portal URL.
- 사용 조건, citation, download date.
- human genome build와 gene annotation source.
- donor/sample/batch metadata, HSPC subpopulation, lineage annotation.
- RNA feature-barcode matrix, ATAC fragments/peak matrix, peak annotation, cell metadata.
- raw FASTQ 재처리가 필요한지, processed matrix/object로 충분한지.

## 작업 절차
1. 공식 출처를 확인하고 accession, URL, access date를 기록한다.
2. raw FASTQ/SRA, 10x output, processed object, metadata 파일을 분리해 받을 파일 목록을 만든다.
3. `data/human-hspc-10x-multiome/raw/`, `data/human-hspc-10x-multiome/processed/`, `metadata/human-hspc-10x-multiome/` 경로를 사용한다.
4. donor/sample/batch/run mapping을 먼저 저장하고, lineage 또는 HSPC subpopulation metadata가 어느 파일에 있는지 표시한다.
5. provider checksum 또는 local sha256 checksum을 manifest에 남긴다.
6. 다운로드 후 파일 크기, 압축 무결성, matrix/object shape, barcode 수, metadata columns 일부를 확인한다.
7. `metadata/human-hspc-10x-multiome/download_manifest.tsv` 또는 `.md`에 source, URL, accession/run, file path, size, checksum, date, genome build, annotation source를 기록한다.

## 출력 형식
```markdown
## Download Plan
- Dataset:
- Official source:
- Access date:
- Files to download:
- Local paths:
- Genome build / annotation:
- Checksums:
- Verification:
- Preprocessing handoff:
- Open issues:
```

## 주의할 점
- HSPC lineage commitment timing을 분석하려면 donor/sample/batch와 lineage labels를 분리해서 보존한다.
- 10x reference와 논문 processed annotation이 다른 경우 둘 다 manifest에 기록한다.

## ▶ 우리 실행 구현 (kkkim-pipeline)
- `pipeline/hspc-velocity-benchmark/scripts/download_data.sh` — GSE209878 재현 다운로드 (MV-1=day0, MV-2=day7)
- `pipeline/hspc-velocity-benchmark/download_manifest.tsv` — sha256 + 출처
- `pipeline/hspc-velocity-benchmark/P0_provenance.md` — provenance/사전체크
