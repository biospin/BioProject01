---
name: 10x-embryonic-mouse-brain-download
description: Download or register the 10x embryonic mouse brain multiome dataset for gene-specific epigenomic lag analysis. Use when Codex needs to find official data sources, fetch raw or processed files, verify files, or create a download manifest before preprocessing.
---

# 10x Embryonic Mouse Brain Download

## Dataset
- Name: 10x embryonic mouse brain
- Biology: embryonic mouse brain differentiation
- Data type: 10x Multiome ATAC + Gene Expression
- Main use: baseline multi-omic dataset for chromatin/RNA timing and gene-specific lag structure.

## 목표
10x embryonic mouse brain multiome 데이터를 공식 출처에서 확인하고, raw/processed 파일을 `data/10x-embryonic-mouse-brain/` 아래에 재현 가능하게 받거나 기존 로컬 파일을 manifest로 등록한다.

## 우선 확인 항목
- 공식 10x Genomics dataset page 또는 원 논문/portal URL.
- 사용 조건, 라이선스, citation, download date.
- genome build와 gene annotation version.
- sample/library 이름, chemistry, reference package.
- RNA feature-barcode matrix, ATAC fragments, ATAC peak matrix, peak annotation, cell metadata.
- raw FASTQ가 필요한지, processed matrix/object로 충분한지.

## 작업 절차
1. 공식 출처를 먼저 확인한다. URL, access date, citation을 기록하고, 외부 mirror만 단독 출처로 사용하지 않는다.
2. 받을 파일 목록을 raw와 processed로 나누고, lag analysis에 필요한 최소 파일 세트를 표시한다.
3. `data/10x-embryonic-mouse-brain/raw/`, `data/10x-embryonic-mouse-brain/processed/`, `metadata/10x-embryonic-mouse-brain/` 경로를 사용한다.
4. 대용량 파일은 원본 파일명을 유지하고 덮어쓰지 않는다. 재다운로드가 필요하면 새 하위 폴더나 manifest version을 만든다.
5. 가능한 경우 provider checksum을 확인한다. 없으면 local `sha256sum` 또는 `shasum -a 256` 결과를 manifest에 남긴다.
6. 다운로드 후 파일 크기, 압축 무결성, matrix shape 또는 일부 record를 확인한다.
7. `metadata/10x-embryonic-mouse-brain/download_manifest.tsv` 또는 `.md`에 source, URL, file path, size, checksum, date, genome build, annotation source를 기록한다.

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
- 시간축은 다운로드 단계에서 확정하지 말고, available metadata와 후보 developmental stage/pseudotime 정보만 기록한다.
- 10x reference package와 downstream gene annotation이 다를 수 있으므로 preprocessing에서 다시 확인한다.
