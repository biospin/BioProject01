---
name: insight-agent
description: Generate cross-paper insights from evidence_bundle.md and papers.jsonl in four fixed sections — Field Flow, Differentiation Map, Repeated Limitations, Unresolved Gaps. Produces insight.md. Requires paper-scrapper output first.
---

# Insight Agent

## 언제 실행하나
`paper-scrapper`가 `papers.jsonl`과 `evidence_bundle.md`를 만든 뒤 실행한다.
단일 논문에는 실행하지 않는다. cross-paper 관계가 없으면 insight가 아니라 요약이 된다.

## 입력
- `analysis/<topic>/_evidence/week2/papers.jsonl`
- `analysis/<topic>/_evidence/week2/evidence_bundle.md`
- `analysis/<topic>/_evidence/week2/scope.md`

## 출력
`analysis/<topic>/_evidence/week2/insight.md`

## Summary와 Insight의 구분

이 skill의 핵심 판정 기준이다. 아래 표에 맞지 않으면 insight가 아니다.

| | Summary | Insight |
|---|---|---|
| 대상 | 논문 하나가 무엇을 했는지 | 논문들 **사이의 관계** |
| 초점 | 논문별 독립 정보 | field를 확장한 축, 공통 limitation, 남은 gap |
| 예시 | "MultiVelo는 priming interval을 정의했다" | "MultiVelo → MultiVeloVAE → MoFlow로 갈수록 discrete ordering → continuous factor → signed lag로 timing 개념이 확장됐다" |

한 논문만 인용해서 성립하는 문장은 insight 섹션에 넣지 않는다.

## 4개 섹션 (고정)

### 1. Field Flow
선행 흐름과 method/assay/dataset의 변화를 시간순으로 정리한다.
- 각 논문이 직전 논문의 무엇을 넘어섰는지 명시한다.
- field가 움직인 **축**을 한 문장으로 요약한다.
- 저자 겹침이나 같은 연구실 계승 관계가 있으면 표시한다. 독립 그룹의 반론인지 같은 그룹의 후속인지에 따라 무게가 다르다.

### 2. Differentiation Map
논문별 차별점, 강점, 약점을 대조한다.
- 표로 strong point / weak point를 정리한다.
- **같은 dataset을 쓰고 다른 결론을 낸 지점을 반드시 찾는다.** 이것이 가장 강한 cross-paper 근거다. 없으면 없다고 쓴다.

### 3. Repeated Limitations
2편 이상에서 반복되는 공통 한계를 모은다.
- 각 항목마다 몇 편에서 관찰됐는지, 어느 논문이 예외인지 적는다.
- 한 논문이 그 한계를 부분적으로 해결했다면 "공통 한계"로 뭉뚱그리지 않고 예외로 분리한다.
- 개별 논문의 약점이 아니라 field 전체의 구조적 한계인지 구분한다.

### 4. Unresolved Gaps
아직 해결되지 않은 질문과 후속 연구 방향을 정리한다.
- 각 gap마다 literature에 선례가 있는지 없는지 표시한다.
- 선례가 없는 gap은 novelty 후보이므로 별도로 표시한다.

## 출력 형식

```markdown
# Cross-Paper Insight — <topic>

- 대상 논문: N편
- 입력: papers.jsonl, evidence_bundle.md
- 작성일: YYYY-MM-DD

## 1. Field Flow
...
**축:** (한 문장)

## 2. Differentiation Map
| Paper | Strong point | Weak point |
### 같은 dataset, 다른 결론

## 3. Repeated Limitations
| # | 공통 한계 | 관찰된 논문 | 예외 |

## 4. Unresolved Gaps
| # | Gap | 선례 유무 | 비고 |

## Insight 목록 (validation 입력용)
| ID | Insight | 관련 논문 | 근거 ID |
```

마지막 "Insight 목록"은 `claim-verify` 또는 validation 단계가 그대로 받을 수 있는 형식으로 쓴다. 근거 ID는 `evidence_bundle.md`의 `E-xx`를 참조한다.

## 금지
- `evidence_bundle.md`에 없는 근거로 insight를 만들지 않는다.
- 논문 하나의 요약을 insight로 제출하지 않는다.
- "가장 우수한 method는 X다" 같은 순위 결론을 내지 않는다. 조건별 강점을 쓴다.
- 수치를 근거로 쓸 때 어느 dataset의 값인지 빠뜨리지 않는다.

## 언어
AGENTS.md의 언어 규칙을 따른다.
