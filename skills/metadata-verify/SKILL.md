---
name: metadata-verify
description: paper-info.yaml의 DOI·제목·저자·연도·저널을 Crossref API + PubMed Eutils로 검증. 불일치 리포트 생성 및 선택적 자동 수정.
---

# Metadata Verify Skill

## 목적

`paper-info.yaml` 생성 후, 특히 PDF 없이 만든 경우, DOI·제목·저자·연도·저널이 실제 출판물과 일치하는지 Crossref + PubMed로 확인한다. Hallucination으로 인한 잘못된 메타데이터가 분석 파이프라인에 전파되는 것을 방지한다.

## 실행 방법

```bash
# 단일 paper 검증
python3 skills/metadata-verify/scripts/verify_metadata.py analysis/<topic>/<paper-id>/

# 전체 analysis/ 일괄 검증
python3 skills/metadata-verify/scripts/verify_metadata.py --all

# 특정 토픽만
python3 skills/metadata-verify/scripts/verify_metadata.py --all --topic ctc-adc-liquid-biopsy

# 불일치 자동 수정 (doi, title, year, venue)
python3 skills/metadata-verify/scripts/verify_metadata.py analysis/<topic>/<paper-id>/ --patch
```

## 검증 항목

| 필드 | 검증 방법 | 심각도 |
|---|---|---|
| `doi` | Crossref API 404 여부 | 🔴 critical |
| `title` | Crossref 제목과 similarity 비교 | 🔴 critical (<0.50) / 🟡 warning (<0.85) |
| `year` | Crossref 발행 연도와 숫자 비교 | 🟡 warning |
| `venue` | Crossref 저널명과 similarity 비교 | 🟡 warning |

## 출력

- 콘솔: 이슈 리포트 + 수정 제안값
- `--patch` 시: `paper-info.yaml` 자동 수정 (doi, doi_or_url, title, year, venue)
- `--all` 시: 전체 요약 (pass/warning/critical 편수)

## DOI 없는 경우 처리

- `doi_or_url`이 URL(http로 시작)이면 DOI 부분만 추출해 검증
- DOI 자체가 없으면 `title` + `year`로 Crossref title search → 후보 DOI 제안
- 제안 similarity ≥ 0.85 이면 `--patch` 시 자동 등록

## 언제 사용하나

1. **PDF 없이 paper-info.yaml 수동 생성 직후** — 등록하기 전 즉시 실행
2. **분석 pipeline 진입 전 pre-flight** — hallucination 잡고 시작
3. **전체 일괄 검증** — `--all`로 주기적 integrity check

## AGENTS.md 연동

신규 paper 등록 시 (fetch_sources.py → paper-info.yaml 작성) 다음 단계로 이 skill을 실행해 메타데이터 정확성을 보장한다:

```
paper 등록 → metadata-verify → (통과) → 분석 pipeline
                             → (critical) → 수정 후 재검증
```
