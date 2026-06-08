---
name: paper-scrapper
description: Collect and normalize a topic-scoped set of papers into comparable records for Week2 evidence-to-insight workflow. Produces papers.jsonl, comparison_table.md, and evidence_bundle.md.
---

# Paper Scrapper

## 목표

주제 범위(`scope.md`, keyword, seed paper)를 받아 관련 paper 후보를 모으고, 중복을 제거한 뒤 Insight Agent와 Validation Agent가 같은 evidence를 읽을 수 있도록 비교 가능한 record로 정규화한다.

이 skill은 개별 paper deep analysis를 대체하지 않는다. 이미 분석된 paper는 `analysis/<primary-topic>/<paper-id>/`의 `paper-info.yaml`, `<paper-id>_core.md`, lens 파일, methodology brief를 우선 근거로 사용한다. 아직 분석되지 않은 paper는 DOI metadata, abstract, source URL 수준으로만 record를 만들고 `status`에 한계를 표시한다.

## Source grounding

- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 여러 paper를 비교할 때도 각 claim은 특정 paper record와 evidence source에 연결한다.
- full analysis가 없는 paper에 대해 결과 수치나 limitation을 추측하지 않는다.

## 입력

기본 입력 위치:

```text
analysis/<primary-topic>/_evidence/week2/scope.md
```

`scope.md`에는 다음을 포함한다.

```markdown
# Scope

## Topic
- primary topic:
- research question:

## Seed papers
- citation key / DOI / URL:

## Keywords
- ...

## Inclusion criteria
- ...

## Exclusion criteria
- ...

## Priority
- must-have:
- nice-to-have:
```

## 출력

기본 출력 위치:

```text
analysis/<primary-topic>/_evidence/week2/
├── papers.jsonl
├── comparison_table.md
└── evidence_bundle.md
```

## Paper Record Contract

`papers.jsonl`은 한 줄에 paper 하나를 담는다. 모든 record는 아래 field를 유지한다.

```json
{
  "record_id": "li-2023-multivelo",
  "title": "MultiVelo: ...",
  "authors": ["Li, ..."],
  "year": 2023,
  "venue": "Nature Biotechnology",
  "doi": "...",
  "url": "...",
  "local_analysis": "analysis/epigenomic-lag/li-2023-multivelo",
  "document_type": "paper",
  "topic_relevance": "왜 이 topic에 들어오는지",
  "research_question": "논문이 푸는 문제",
  "assay_or_data": ["10x Multiome", "SHARE-seq"],
  "method": "핵심 method / model / algorithm",
  "main_claims": ["claim 1", "claim 2"],
  "key_results": ["결과와 수치. 근거 위치 포함"],
  "limitations": ["저자 한계 또는 분석자 한계. prefix 사용"],
  "follow_up": ["후속 실험/분석 후보"],
  "evidence_sources": ["core.md §Results", "Figure 2", "paper-info.yaml"],
  "status": "full-analysis | abstract-only | metadata-only | needs-pdf"
}
```

작성 규칙:

- `record_id`는 기존 paper-id가 있으면 그대로 쓴다.
- `local_analysis`는 기존 분석 폴더가 있을 때만 채운다. 없으면 `null`.
- `key_results`는 수치와 출처가 함께 있을 때만 넣는다.
- `limitations`는 저자 명시 한계와 분석자 판단 한계를 구분한다.
- `status`는 다음 중 하나:
  - `full-analysis`: core/lens/methodology brief가 존재.
  - `abstract-only`: abstract 또는 metadata만 확보.
  - `metadata-only`: title/DOI/venue 정도만 확보.
  - `needs-pdf`: topic상 중요하지만 source PDF가 필요.

## comparison_table.md 형식

```markdown
# Comparison Table

| record_id | year | method | assay/data | main claim | key result | limitation | relevance | status |
|---|---:|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

표는 빠른 비교용이다. 긴 설명은 `evidence_bundle.md`에 둔다.

## evidence_bundle.md 형식

```markdown
# Evidence Bundle

## Scope Summary
- Topic:
- Research question:
- Inclusion / exclusion:

## Paper Records

### <record_id> — <short title>
- Identity:
- Topic relevance:
- Research question:
- Method / assay / dataset:
- Main claims:
- Key results:
- Limitations:
- Follow-up possibility:
- Evidence sources:
- Status:

## Cross-Paper Signals
- 반복되는 문제:
- 방법론 차이:
- dataset / assay 차이:
- 공통 한계:
- 후속 연구 후보:

## Missing Evidence
- PDF 필요:
- full analysis 필요:
- 확인할 metadata:
```

## 작업 절차

1. `scope.md`를 읽고 topic, seed paper, keyword, 포함/제외 기준을 확정한다.
2. `analysis/<primary-topic>/` 아래 기존 paper 분석 폴더를 우선 스캔한다.
3. 각 기존 paper의 `paper-info.yaml`과 core/lens/methodology 파일에서 record field를 채운다.
4. scope에 포함되지만 아직 분석 폴더가 없는 paper는 DOI/URL/abstract metadata 수준으로 record를 만든다.
5. 중복을 제거한다.
   - DOI가 같으면 같은 paper.
   - preprint와 published version은 version 차이를 남기고 대표 record 하나로 묶는다.
   - title이 거의 같고 저자/연도가 같으면 중복 후보로 표시한다.
6. `papers.jsonl`, `comparison_table.md`, `evidence_bundle.md`를 생성한다.
7. full analysis가 필요한 중요한 후보는 `Missing Evidence`에 명확히 남긴다.

## 품질 기준

- Insight Agent가 원문을 다시 열지 않아도 논문 간 비교를 시작할 수 있어야 한다.
- Validation Agent가 claim별 근거 위치를 추적할 수 있어야 한다.
- `papers.jsonl`과 `evidence_bundle.md`의 내용이 서로 모순되면 안 된다.
- 후보 paper를 많이 모으는 것보다 같은 schema로 비교 가능하게 만드는 것이 우선이다.

## 금지

- link list만 만들고 끝내지 않는다.
- abstract-only paper의 결과를 full paper처럼 쓰지 않는다.
- topic relevance가 약한 paper를 숫자 채우기용으로 넣지 않는다.
- evidence source 없는 claim을 `main_claims`나 `key_results`에 넣지 않는다.
