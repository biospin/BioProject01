---
name: share-seq-mouse-skin-download
description: Download or register the SHARE-seq mouse skin dataset GSE140203 for gene-specific epigenomic lag analysis. Use when Codex needs to find official data sources, fetch raw or processed files, verify files, or create a download manifest before preprocessing.
---

# SHARE-seq Mouse Skin Download

## Dataset
- Name: SHARE-seq mouse skin
- Accession: GSE140203
- Biology: mouse skin differentiation
- Data type: paired chromatin + RNA
- Main use: baseline dataset for chromatin/RNA timing during differentiation.

## 목표
GSE140203 SHARE-seq mouse skin 데이터를 GEO/SRA, 논문 supplement, 또는 공식 portal에서 확인하고, lag modeling에 필요한 raw/processed 입력을 재현 가능하게 다운로드하거나 기존 파일을 등록한다.

## 우선 확인 항목
- GEO Series GSE140203, linked SRA runs, supplementary files, 원 논문/portal URL.
- 사용 조건, citation, download date.
- genome build와 gene annotation source.
- RNA matrix, chromatin accessibility matrix, peak annotation, barcode pairing 정보.
- cell type, differentiation stage, pseudotime 또는 lineage metadata 제공 여부.
- raw FASTQ 재처리가 필요한지, processed object로 충분한지.

## 작업 절차
1. GEO와 원 논문/portal을 공식 출처로 확인하고 accession, URL, access date를 기록한다.
2. raw FASTQ/SRA와 processed supplementary file을 분리해서 받을 파일 목록을 만든다.
3. `data/share-seq-mouse-skin/raw/`, `data/share-seq-mouse-skin/processed/`, `metadata/share-seq-mouse-skin/` 경로를 사용한다.
4. SRA 다운로드는 가능하면 run table을 먼저 저장하고, sample/library/run mapping을 manifest에 남긴다.
5. provider checksum이 있으면 검증한다. 없으면 local sha256 checksum을 생성한다.
6. 다운로드 후 압축 무결성, 일부 record, matrix dimensions, barcode 수를 확인한다.
7. `metadata/share-seq-mouse-skin/download_manifest.tsv` 또는 `.md`에 source, URL, accession/run, file path, size, checksum, date, genome build, annotation source를 기록한다.

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
- SHARE-seq는 modality pairing 정보가 핵심이므로 barcode mapping 파일 또는 processed object metadata를 우선 확보한다.
- SRA run 이름만으로 biological sample을 해석하지 말고 GEO sample metadata와 대조한다.
