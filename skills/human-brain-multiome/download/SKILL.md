---
name: human-brain-multiome-download
description: Download or register the human brain multi-ome dataset GSE162170 for gene-specific epigenomic lag analysis. Use when Codex needs to find official data sources, fetch raw or processed files, verify files, or create a download manifest before preprocessing.
---

# Human Brain Multiome Download

## Dataset
- Name: Human brain multi-ome
- Accession: GSE162170
- Biology: fetal / developing human brain
- Data type: human multiome
- Main use: human developmental dataset for gene-specific epigenomic lag analysis.

## 목표
GSE162170 human brain multiome 데이터를 GEO/SRA, 원 논문 supplement, 또는 공식 data portal에서 확인하고, donor/stage/region metadata와 함께 재현 가능한 다운로드 manifest를 만든다.

## 우선 확인 항목
- GEO Series GSE162170, linked SRA runs, supplementary files, 원 논문/portal URL.
- controlled-access 여부, 사용 조건, citation, download date.
- human genome build와 gene annotation source.
- donor, developmental stage, brain region, batch/sample metadata.
- RNA matrix, ATAC fragments/peak matrix, peak annotation, cell metadata.
- raw data 재처리가 필요한지, processed object로 분석 가능한지.

## 작업 절차
1. 공식 출처를 확인하고 accession, URL, access date, access restriction을 기록한다.
2. raw FASTQ/SRA, processed matrix/object, metadata 파일을 분리해 받을 파일 목록을 만든다.
3. `data/human-brain-multiome/raw/`, `data/human-brain-multiome/processed/`, `metadata/human-brain-multiome/` 경로를 사용한다.
4. donor/stage/region/run mapping을 우선 저장하고, sample sheet를 preprocessing에서 바로 읽을 수 있게 둔다.
5. provider checksum 또는 local sha256 checksum을 manifest에 남긴다.
6. 다운로드 후 파일 크기, 압축 무결성, matrix/object shape, obs/var metadata 일부를 확인한다.
7. `metadata/human-brain-multiome/download_manifest.tsv` 또는 `.md`에 source, URL, accession/run, file path, size, checksum, date, genome build, annotation source를 기록한다.

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
- donor, developmental stage, brain region metadata가 lag modeling confounder가 될 수 있으므로 다운로드 단계부터 분리해서 기록한다.
- controlled-access 파일이면 인증 절차와 접근 불가 파일을 명확히 남긴다.
