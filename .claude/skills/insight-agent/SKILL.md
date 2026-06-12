---
name: insight-agent
description: Read a Week2 evidence_bundle.md and produce cross-paper research insights: field flow, differences, repeated limitations, unresolved gaps, and follow-up research directions.
---

# Insight Agent

## 목표

`evidence_bundle.md`를 읽고 여러 paper 사이의 흐름, 차이, 반복 패턴, unresolved gap을 도출한다. 단순 paper 요약이 아니라 다음 연구 방향이나 실험/분석 설계로 이어질 수 있는 관찰을 만든다.

이 skill의 출력은 `analysis/<primary-topic>/_evidence/week2/insight.md`이다.

## Source grounding

- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 모든 insight는 `evidence_bundle.md`의 paper record 또는 기존 분석 파일 경로에 연결한다.
- 여러 paper를 종합한 해석은 `해석:`으로 표시한다.
- 근거 paper가 1개뿐이면 "반복 패턴"처럼 쓰지 않는다.

## 입력

```text
analysis/<primary-topic>/_evidence/week2/evidence_bundle.md
analysis/<primary-topic>/_evidence/week2/papers.jsonl
```

필요하면 기존 paper-level 분석 파일을 보조 근거로 참고한다.

```text
analysis/<primary-topic>/<paper-id>/<paper-id>_core.md
analysis/<primary-topic>/<paper-id>/<paper-id>_lens-academic.md
analysis/<primary-topic>/<paper-id>/<paper-id>_lens-industry.md
analysis/<primary-topic>/<paper-id>/<paper-id>_methodology-brief.md
```

## 출력 형식

```markdown
# Insight

## 1. Executive Signal
- 가장 중요한 cross-paper insight:
- 왜 지금 중요한가:
- 우리 topic과의 연결:

## 2. Field Flow
- 선행 흐름:
- method / assay / dataset이 어떻게 바뀌는가:
- 어떤 문제가 반복적으로 다음 paper를 유도했는가:

## 3. Differentiation Map
| paper | 무엇이 다른가 | 강점 | 약점 | evidence |
|---|---|---|---|---|

## 4. Repeated Limitations
- 반복 한계 1:
  - 해당 paper:
  - 근거:
  - 왜 중요한가:
- 반복 한계 2:

## 5. Unresolved Gaps
- gap:
  - 현재 evidence:
  - 부족한 evidence:
  - 검증 가능한 질문:

## 6. Follow-up Research Directions
- 방향 1:
  - 가설:
  - 필요한 dataset / assay:
  - 분석 방법:
  - 성공 기준:
  - 관련 paper:

## 7. Practical Actions
- 지금 할 일:
- 다음 분기:
- 장기:

## 8. Claims for Validation
| claim_id | insight claim | evidence papers | evidence strength | validation focus |
|---|---|---|---|---|
```

## Insight 작성 규칙

- `Executive Signal`은 3개 이내로 제한한다.
- `Field Flow`는 시간순 나열이 아니라 "어떤 한계가 다음 방법을 만들었는가" 중심으로 쓴다.
- `Differentiation Map`은 각 paper의 novelty와 trade-off를 한 줄로 비교한다.
- `Repeated Limitations`는 최소 2개 paper에서 반복될 때만 넣는다.
- `Unresolved Gaps`는 후속 실험/분석 질문으로 바꿀 수 있어야 한다.
- `Follow-up Research Directions`는 실행 가능한 단위로 쓴다.
- 마지막 `Claims for Validation`은 Validation Agent가 그대로 점검할 claim list이다.

## Evidence strength 기준

- `strong`: 2개 이상 full-analysis paper에서 직접 근거가 있고 수치/figure/table 근거가 있다.
- `moderate`: full-analysis paper 1개 이상 + 보조 paper에서 일관된 방향성이 있다.
- `weak`: abstract-only 또는 metadata-only 근거가 많거나 claim이 분석자 해석에 크게 의존한다.
- `needs-check`: source PDF, supplementary, 또는 원문 figure 확인이 필요하다.

## 금지

- 여러 논문을 읽었다는 이유만으로 field consensus처럼 단정하지 않는다.
- 산업/BD 해석을 academic insight와 섞지 않는다. 필요하면 Practical Actions에 분리한다.
- Validation Agent가 검증할 수 없는 모호한 claim을 만들지 않는다.
- evidence_bundle에 없는 paper를 근거처럼 끌어오지 않는다.
