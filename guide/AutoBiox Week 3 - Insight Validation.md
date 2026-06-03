# AutoBiox Week 3 — Insight 공유와 Validation 설계

> 2주차 과제 공유 → Validation 기준 정리 → 4주차 Agent 구현 예고
> 키워드: **Insight Agent · Validation · Openclaw**
> 발표: AutoBiox 박상준
>
> *(원본 8-슬라이드 deck `AutoBiox Week 3 - Insight Validation.pdf`를 markdown으로 변환)*

---

## 1. 2주차 과제 공유: Insight Agent

각자 만든 Insight Agent를 다음 4가지 관점으로 공유한다.

- **구조 소개** — 각자 만든 Insight Agent가 어떤 흐름으로 동작하는지 소개한다.
- **입력 자료** — 어떤 논문 또는 논문 묶음을 입력으로 사용했는지 설명한다.
- **역할과 관점** — Agent에게 어떤 역할과 해석 기준을 부여했는지 공유한다.
- **요약 vs Insight** — 단순 요약과 Insight 추출을 어떻게 구분했는지 이야기한다.

---

## 2. Insight Agent 공유 포인트

| 항목 | 공유할 내용 |
|---|---|
| **Input** | 어떤 자료를 넣었는가 |
| **Prompt** | 어떤 기준으로 Insight를 뽑게 했는가 |
| **Output** | 어떤 형식으로 결과가 나왔는가 |
| **Quality** | 의미 있는 관찰이나 연구 방향이 나왔는가 |
| **Limitation** | Agent가 놓치거나 과장한 부분은 없었는가 |

---

## 3. 왜 Validation이 필요한가

```
Insight  ──▶  Validation  ──▶  신뢰 가능한 연구 자산
```

- **Insight**: Agent가 만든 해석은 그럴듯해 보여도 검증이 필요하다.
- **Validation**: 근거, 논리, 범위, 과장을 확인하고 수정 방향을 남긴다.
- **결과**: 신뢰 가능한 연구 자산.

---

## 4. Validation Agent가 볼 기준

| 기준 | 확인 질문 |
|---|---|
| **Evidence** | 논문 문장, Figure, Table, 실험 결과에 근거하는가 |
| **Logic** | 주장과 근거 사이의 논리 흐름이 자연스러운가 |
| **Scope** | 논문에서 말한 범위를 넘어 과장하지 않았는가 |
| **Novelty** | 단순 요약이 아니라 새로운 Insight인가 |
| **Actionability** | 후속 실험, 연구 방향, 의사결정으로 이어질 수 있는가 |
| **Risk** | 반례, 한계, 불확실성이 함께 정리되어 있는가 |

---

## 5. Validation 결과를 어떻게 남길까

- 각 Insight마다 검증 상태를 남긴다.
- 상태값 예시: **Valid, Needs Evidence, Overstated, Unclear, Rejected**
- 왜 그렇게 판단했는지 짧은 이유를 적는다.
- 가능하면 Figure, Table, 논문 문장 등 근거 위치를 함께 남긴다.

### 기록 예시

| 항목 | 내용 |
|---|---|
| **Insight** | 기존 방법보다 특정 조건에서 더 안정적인 결과를 보인다. |
| **Status** | Needs Evidence |
| **Reason** | 모든 조건에서 안정적이라고 말하기에는 실험 범위가 제한적이다. |
| **Evidence** | Figure 3, Table 2 |

---

## 6. 3주차 토론 질문

1. 어떤 Insight가 가장 설득력 있었는가
2. 어떤 Insight는 근거가 부족하거나 과장되어 보였는가
3. Validation Agent가 반드시 확인해야 할 기준은 무엇인가
4. 모두의 Validation Agent 결과가 다르면 어떻게 판단할 것인가
5. 다음 주 실제 Agent 구현을 위해 출력 형식은 어떻게 맞춰야 하는가

---

## 7. 4주차 예고: Openclaw로 실제 Agent 만들기

```
Paper Scrapper  ──▶  Insight Agent  ──▶  Validation Agent  ──▶  Agent Workflow
 논문 수집과 구조화      연구 흐름과 관찰 추출       근거와 논리 검증            실행 흐름 관리
```

- 4주차부터는 **Openclaw**가 필요.
- Openclaw에서 작업 공간을 만들고, Agent별 입력과 출력, 실행 흐름을 관리하는 방법을 공부한다.
