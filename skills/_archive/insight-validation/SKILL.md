---
name: insight-validation
description: Validate insights extracted from analyzed scientific papers using evidence, logic, scope, novelty, actionability, and risk criteria.
---

# Insight Validation

## 목표
이미 분석된 paper의 insight가 논문 근거에 의해 충분히 지지되는지 검증한다. 단순 요약과 새로운 해석을 구분하고, 근거 부족·과장·범위 초과를 명시한다.

## 입력
- `analysis/<topic>/<paper-title>/full.md`
- 사용자가 제공한 Insight 목록, 또는 기존 `full.md`에서 추출한 candidate insight

## 검증 기준

각 Insight마다 아래 6개 항목을 확인한다.

| Criterion | 질문 |
|---|---|
| Evidence | 논문 문장, Figure, Table, 실험 결과에 근거하는가 |
| Logic | 주장과 근거 사이 논리 흐름이 자연스러운가 |
| Scope | 논문 범위를 넘어 과장하지 않았는가 |
| Novelty | 단순 요약이 아니라 분석적 insight인가 |
| Actionability | 후속 분석, 실험, 의사결정으로 이어지는가 |
| Risk | 반례, 한계, 불확실성을 함께 기록했는가 |

## Status

- `Valid`: 현재 근거와 범위가 충분하다.
- `Needs Evidence`: 방향은 타당하지만 추가 figure, source data, external validation이 필요하다.
- `Overstated`: 논문 근거보다 주장이 강하다.
- `Unclear`: 근거 또는 용어가 모호해 판단을 보류한다.
- `Rejected`: 논문과 충돌하거나 근거가 없다.

## 출력 형식

```markdown
## Insight Validation

| ID | Paper | Insight | Status | Reason | Evidence | Risk / Next Check |
|---|---|---|---|---|---|---|
```

## 언어 규칙
AGENTS.md의 언어 규칙을 따른다.

## Cross-paper 검증
Insight가 다른 논문에서도 지지되는지 확인하고 싶을 때:
1. `analysis/` 아래 다른 논문의 `full.md`를 검색한다.
2. 같은 주제를 다루는 결과가 있으면 교차 비교한다.
3. 일치하면 Evidence를 강화하고, 모순되면 Risk 항목에 명시한다.
4. 출처는 `논문 제목 > 섹션명` 형식으로 적는다.

## 작성 규칙
- `Evidence`에는 Figure 번호, Table 번호, Results 항목, 수치, 또는 `full.md`의 해당 섹션명을 적는다.
- 논문에 없는 causality를 만들지 않는다. 특히 association, prediction, perturbation, causal mechanism을 구분한다.
- `Needs Evidence`와 `Overstated`는 실패가 아니라 후속 검증 queue로 취급한다.
- 검증은 `full.md` 기준으로 한다. PDF 원문이나 외부 지식을 우선 근거로 삼지 않는다.
