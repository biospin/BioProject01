# OpenClaw Week2 Agent Setup

## 목적

Week2에서는 1주차의 paper-level Single Agent stack을 유지하면서, OpenClaw에서 role별 agent를 분리해 `Paper Scrapper -> Insight -> Validation -> Handoff` 흐름을 운영한다.

Repo 안의 `skills/*/SKILL.md`가 agent의 작업 contract이고, OpenClaw는 이 contract를 실행하는 조율 layer로 사용한다.

## Workspace

기본 작업 위치:

```text
analysis/<primary-topic>/_evidence/week2/
```

예:

```text
analysis/epigenomic-lag/_evidence/week2/
├── scope.md
├── papers.jsonl
├── comparison_table.md
├── evidence_bundle.md
├── insight.md
├── validation_report.md
└── handoff.md
```

## Agent Roles

### 1. Orchestrator

- Uses: `AGENTS.md`의 `Evidence-to-Insight Workflow (Week2)`
- Input:
  - topic
  - seed paper
  - keyword
  - inclusion / exclusion criteria
- Output:
  - `scope.md`
  - 최종 `handoff.md`
- Responsibility:
  - 각 agent가 같은 topic folder와 같은 file contract를 사용하게 한다.
  - paper-level 분석 결과와 topic-level evidence 결과를 섞지 않게 관리한다.

### 2. Paper Scrapper Agent

- Uses: `skills/paper-scrapper/SKILL.md`
- Input:
  - `scope.md`
  - existing `analysis/<primary-topic>/<paper-id>/` folders
  - DOI / URL / abstract metadata if provided
- Output:
  - `papers.jsonl`
  - `comparison_table.md`
  - `evidence_bundle.md`
- Done when:
  - all records follow the Paper Record Contract
  - each claim/result has evidence source or explicit `미제공:` / `검토필요:`
  - important missing PDFs or missing full analyses are listed

### 3. Insight Agent

- Uses: `skills/insight-agent/SKILL.md`
- Input:
  - `evidence_bundle.md`
  - `papers.jsonl`
- Output:
  - `insight.md`
- Done when:
  - field flow, differentiation, repeated limitations, unresolved gaps, follow-up directions are written
  - final section contains `Claims for Validation`
  - every insight is traceable to paper records

### 4. Validation Agent

- Uses: `skills/validation-agent/SKILL.md`
- Input:
  - `evidence_bundle.md`
  - `papers.jsonl`
  - `insight.md`
- Output:
  - `validation_report.md`
- Done when:
  - each claim has a verdict
  - overreach and missing assumptions are explicitly listed
  - required revisions to `insight.md` are actionable

### 5. Integrator

- Uses:
  - `insight.md`
  - `validation_report.md`
  - project handoff context in `CLAUDE.md`
- Output:
  - `handoff.md`
- Responsibility:
  - Jira / Confluence ready action item으로 정리한다.
  - 검증된 insight와 보류할 insight를 분리한다.
  - 다음 paper-level full analysis가 필요한 후보를 명시한다.

## Suggested OpenClaw Run Order

1. Orchestrator creates `scope.md`.
2. Paper Scrapper Agent creates `papers.jsonl`, `comparison_table.md`, `evidence_bundle.md`.
3. Insight Agent creates `insight.md`.
4. Validation Agent creates `validation_report.md`.
5. If validation verdict is `revise`, Insight Agent updates `insight.md`.
6. Integrator creates `handoff.md`.

## Cross Validation

팀원이 각자 만든 Validation Agent를 사용할 경우:

- 같은 `evidence_bundle.md`와 `insight.md`를 입력으로 사용한다.
- 각자 `validation_report.<name>.md`로 출력한다.
- Orchestrator 또는 Integrator가 일치/불일치 항목을 `validation_report.md`의 `Cross Validation Notes`에 통합한다.

## Guardrails

- OpenClaw agent가 외부 검색을 하더라도 `papers.jsonl`에 들어가는 claim은 출처를 남긴다.
- abstract-only paper는 `status: abstract-only`로 둔다.
- paper-level 분석이 필요한 중요한 후보는 Week2 산출물에 억지로 깊게 쓰지 말고 `Missing Evidence` 또는 `Handoff`에 action item으로 남긴다.
- 1주차 산출물인 `analysis/<topic>/<paper-id>/` 구조는 유지한다.
