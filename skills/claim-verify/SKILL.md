---
name: claim-verify
description: Verify whether a specific insight, interpretation, or takeaway from a full.md analysis is well-supported by evidence. Rates evidence strength, flags overreach, and cross-checks against other analyzed papers.
---

# Claim Verify

## 언제 실행하나
사용자가 특정 insight나 해석이 논문 근거로 뒷받침되는지 확인하고 싶을 때 실행한다.
`takeaway`나 `apply-map`에서 나온 주장을 검증할 때 특히 유용하다.

## 입력
- 검증할 insight 또는 주장 (사용자가 제공하거나 `full.md`에서 추출)
- 해당 논문의 `full.md`
- cross-paper insight를 검증할 때는 `analysis/<topic>/_evidence/week2/insight.md`의 Insight 목록과 `evidence_bundle.md`

## 검증 기준 (6개)

각 insight마다 아래 6개 항목을 순서대로 확인한다. Evidence와 Scope를 먼저 통과시킨 뒤 Novelty와 Actionability를 평가한다. 근거가 약한 새로운 해석은 Novelty가 높아도 `Needs Evidence`로 남긴다.

| Criterion | 질문 |
|---|---|
| Evidence | 논문 문장, Figure, Table, 실험 결과에 근거하는가 |
| Logic | 주장과 근거 사이 논리 흐름이 자연스러운가 |
| Scope | 논문 범위를 넘어 과장하지 않았는가 |
| Novelty | 단순 요약이 아니라 분석적 insight인가 |
| Actionability | 후속 분석, 실험, 의사결정으로 이어지는가 |
| Risk | 반례, 한계, 불확실성을 함께 기록했는가 |

## Status (5단계)

| Status | 조건 |
|---|---|
| **Valid** | 6개 기준을 모두 통과. 수치와 조건이 명확하고 범위를 넘지 않음 |
| **Needs Evidence** | 방향은 타당하나 근거가 부족. 저자도 hypothesis 수준으로 제시한 경우 포함 |
| **Overstated** | 근거는 있으나 논문 범위를 넘어 해석. computational prediction을 검증된 사실처럼 다루는 경우 |
| **Unclear** | 주장 자체가 모호하거나 검증 가능한 형태가 아님 |
| **Rejected** | `full.md` 근거와 모순되거나 다른 분석 논문이 반증 |

## 근거 강도 기준

| 등급 | 조건 |
|---|---|
| **강함** | 정량적 수치 + 복수 데이터셋에서 일관 + ablation 또는 perturbation 확인 |
| **보통** | 정량적 수치가 있지만 단일 데이터셋이거나 ablation 없음 |
| **약함** | 시각적 근거 (heatmap, UMAP 등)에 의존하거나 수치 없는 정성 설명만 있음 |
| **없음** | `full.md`에서 해당 주장의 직접 근거를 찾을 수 없음 |

## 과해석 체크리스트
- Causal claim인데 association evidence만 있는가
- 단일 데이터셋 결과를 일반화했는가
- Figure의 시각적 패턴을 수치 없이 강하게 해석했는가
- 저자 주장과 분석자 해석이 섞여 있는가
- 다른 분석된 논문과 모순되는가

## 실행 절차
1. 검증할 주장을 정확히 파악한다.
2. 해당 논문의 `full.md`를 읽고 Results, Figure, Methods 섹션에서 근거를 찾는다.
3. 근거 강도를 분류한다.
4. 6개 기준을 순서대로 적용하고 과해석 체크리스트를 함께 확인한다.
5. `analysis/` 아래 다른 논문 `full.md`에서 같은 주제를 다루는 내용이 있으면 교차 검증한다.
6. Status를 배정하고 Reason과 Evidence를 함께 기록한다.

## 출력 형식

```markdown
### Claim Verify

**검증 대상:** [주장 또는 insight]
**출처:** [논문 제목 > 섹션]

**근거 강도:** [강함 / 보통 / 약함 / 없음]
- 근거 내용: [full.md에서 찾은 수치, Figure, 비교]
- 근거가 부족한 이유: (있으면)

**과해석 여부:**
- Causal vs association:
- 일반화 범위:
- 시각적 근거 의존:
- 다른 논문과의 모순:

**Cross-paper 검증:** (다른 분석된 논문이 있을 때)
- 지지하는 논문:
- 모순되는 논문:

**6기준 판정:**
| Evidence | Logic | Scope | Novelty | Actionability | Risk |
|---|---|---|---|---|---|
| ✅/⚠️/❌ | | | | | |

**Status:** [Valid / Needs Evidence / Overstated / Unclear / Rejected]
**Reason:** (그렇게 판단한 짧은 이유)
**Evidence:** (근거 위치 — Figure, Table, 수치)
**Risk / Next Check:** (반례, 한계, 다음 확인 사항)
```

### 여러 insight를 한 번에 검증할 때

`insight.md`의 Insight 목록처럼 복수 항목을 검증하는 경우 아래 7열 표를 사용한다. 이 형식은 3주차 산출물(`validation/<topic>/insight_validation_week3.md`)과 동일하므로 그대로 이어붙일 수 있다.

```markdown
| ID | Paper | Insight | Status | Reason | Evidence | Risk / Next Check |
```

## 주의
- `Valid`는 수치와 조건이 명확히 있을 때만 사용한다.
- 저자가 한계로 인정한 내용은 과해석이 아니다.
- 검증은 `full.md`와 `evidence_bundle.md` 기준으로 한다. PDF 원문이나 외부 지식을 우선 근거로 삼지 않는다.
- `Rejected`는 근거와 모순될 때만 쓴다. 근거를 찾지 못한 것뿐이면 `Needs Evidence`다.
- causal mechanism이 필요한 주장은 perturbation 근거가 없으면 `Valid`로 올리지 않는다.
- 결과가 서로 다를 때는 같은 dataset·같은 metric·같은 source data의 직접 비교를 우선하고, UMAP stream 같은 qualitative evidence는 보조 근거로 둔다.
