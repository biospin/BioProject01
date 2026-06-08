---
name: validation-agent
description: Validate Week2 insight claims against the evidence bundle and paper-level analysis files. Produces validation_report.md with claim-level evidence checks, missing assumptions, overreach, and cross-validation notes.
---

# Validation Agent

## 목표

`insight.md`의 claim이 실제 evidence에 의해 지지되는지 검증한다. 결과의 멋짐보다 근거의 안정성을 우선한다. 특히 conclusion이 evidence보다 커진 부분, 빠진 전제, source 확인이 필요한 항목을 분리한다.

이 skill의 출력은 `analysis/<primary-topic>/_evidence/week2/validation_report.md`이다.

## Source grounding

- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 검증은 `evidence_bundle.md`, `papers.jsonl`, 기존 paper-level 분석 파일에 있는 내용만 근거로 한다.
- 원문 PDF 확인이 필요하지만 아직 확인하지 못한 것은 `검토필요:`로 남긴다.

## 입력

```text
analysis/<primary-topic>/_evidence/week2/evidence_bundle.md
analysis/<primary-topic>/_evidence/week2/papers.jsonl
analysis/<primary-topic>/_evidence/week2/insight.md
```

필요하면 기존 paper-level 분석 파일을 보조 근거로 참고한다.

## 출력 형식

```markdown
# Validation Report

## 1. Overall Verdict
- 종합 판정: pass / revise / fail
- 가장 강한 insight:
- 가장 약한 insight:
- 다음 수정 우선순위:

## 2. Claim-level Evidence Check
| claim_id | verdict | evidence found | missing evidence | overreach risk | action |
|---|---|---|---|---|---|

## 3. Missing Assumptions
- claim:
  - 빠진 전제:
  - 왜 중요한가:
  - 확인 방법:

## 4. Overreach / Weak Claims
- claim:
  - 현재 표현:
  - 문제:
  - 더 안전한 표현:

## 5. Source Coverage
| paper | status | evidence quality | validation note |
|---|---|---|---|

## 6. Cross Validation Notes
- 다른 Validation Agent와 일치:
- 다른 Validation Agent와 불일치:
- 토론으로 남길 항목:

## 7. Required Revisions to insight.md
- 수정 1:
- 수정 2:

## 8. Handoff Decision
- Jira / Confluence로 넘겨도 되는 항목:
- 보류할 항목:
- 추가 paper analysis가 필요한 항목:
```

## Verdict 기준

Claim-level `verdict`:

- `supported`: evidence_bundle 또는 paper-level 분석에서 직접 근거가 확인됨.
- `partially-supported`: 방향은 맞지만 일부 paper, 수치, 범위가 부족함.
- `unsupported`: 현재 evidence에서 근거를 찾을 수 없음.
- `overstated`: 근거는 있으나 표현이 evidence보다 큼.
- `needs-source-check`: PDF, supplementary, figure/table 직접 확인이 필요함.

Overall verdict:

- `pass`: 핵심 claim 대부분이 `supported`이고 수정이 경미함.
- `revise`: 핵심 방향은 유효하지만 일부 claim 표현, 근거, scope 수정 필요.
- `fail`: 핵심 insight가 현재 evidence로 지지되지 않음.

## 검증 절차

1. `insight.md`의 `Claims for Validation` 표를 우선 읽는다.
2. 각 claim에 대해 `evidence_bundle.md`와 `papers.jsonl`의 근거 paper를 찾는다.
3. 필요한 경우 해당 paper의 `core.md`, lens 파일, methodology brief를 확인한다.
4. claim이 근거보다 넓게 일반화되었는지 본다.
5. claim별 verdict와 수정 action을 작성한다.
6. `insight.md`에 반영해야 할 수정 목록을 따로 정리한다.

## 검증 질문

- 이 claim은 어느 paper의 어느 결과에 기대는가?
- 같은 claim을 지지하는 paper가 2개 이상인가, 아니면 단일 사례인가?
- 수치, figure, table, method 설명 중 무엇이 근거인가?
- abstract-only paper를 full evidence처럼 사용하지 않았는가?
- association을 causality처럼 표현하지 않았는가?
- dataset-specific 결과를 field-wide conclusion처럼 쓰지 않았는가?
- "우리 적용"이 실제 dataset / assay / code 조건과 맞는가?

## 금지

- Insight Agent의 결론을 그대로 요약하지 않는다.
- 근거 부족을 좋은 문장으로 덮지 않는다.
- 검증하지 못한 항목을 pass 처리하지 않는다.
- 새로운 insight를 추가하지 않는다. 필요하면 `질문:` 또는 `추가 분석 필요`로 남긴다.
