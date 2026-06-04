# BIOP01-21 Week 2 Presentation

## Slide 1. Title

**BIOP01-21 [2주차 과제] Insight Agent 만들기**  
Topic: `chromatin-transcription lag literature`

- 발표자: 용기
- 분석 논문: `MultiVelo`, `MultiVeloVAE`, `MoFlow`
- 목표: 여러 논문에서 cross-paper insight를 추출해, gene-specific lag 연구의 현재 위치와 남은 gap을 정리

### Speaker Note
이번 2주차 과제에서는 논문 하나를 요약하는 게 아니라, 여러 논문을 비교해서 cross-paper insight를 뽑는 Agent를 만드는 데 초점을 맞췄습니다. 주제는 chromatin-transcription lag modeling으로 잡았고, MultiVelo, MultiVeloVAE, MoFlow 세 편을 시작 논문 세트로 사용했습니다.

---

## Slide 2. Why This Topic

- 프로젝트 핵심 질문:
  - `activation lag`: chromatin opening 이후 transcription onset까지 걸리는 시간
  - `shutdown lag`: transcription shutdown 이후 chromatin closing까지 걸리는 시간
- 이 주제는 프로젝트 Step 1과 직접 연결됨
- 세 논문 모두 chromatin-RNA timing을 다루지만, 해석 방식이 다름

### Speaker Note
이 주제를 선택한 이유는 프로젝트의 핵심 개념인 activation lag과 shutdown lag에 가장 직접적으로 연결되기 때문입니다. 세 논문은 모두 timing을 다루지만, MultiVelo는 ordering, MultiVeloVAE는 continuous dynamics, MoFlow는 signed lag 쪽으로 초점이 다릅니다.

---

## Slide 3. Input Paper Set

1. `MultiVelo`
   - priming interval / decoupling interval
   - Model 1 / Model 2
2. `MultiVeloVAE`
   - continuous cell-specific coupling / decoupling
   - posterior-based differential dynamics
3. `MoFlow`
   - positive / negative chromatin-to-RNA lag
   - relay velocity without fixed global latent-time axis

### Speaker Note
처음부터 논문 수를 넓히기보다, timing 개념이 분명한 세 편으로 시작했습니다. 세 논문은 같은 문제를 다루지만, timing을 정의하는 방식이 다르기 때문에 비교 대상으로 적합했습니다.

---

## Slide 4. Agent Structure

### Pipeline
1. `scope.md`
   - 주제, 키워드, 포함/제외 기준 정의
2. `paper-analysis`
   - 논문별 구조화 분석
3. `papers.jsonl`
   - 비교 가능한 record 저장
4. `comparison_table.md`
   - method / assay / result / limitation 비교
5. `evidence_bundle.md`
   - Insight Agent 입력용 근거 묶음
6. `insight.md`
   - 최종 cross-paper insight 생성

### Speaker Note
Agent 구조는 1차적으로 논문별 분석을 만들고, 2차적으로 그것을 비교 가능한 입력 구조로 변환한 뒤, 마지막에 cross-paper insight를 생성하는 방식입니다. 즉 요약 Agent와 Insight Agent를 분리했습니다.

---

## Slide 5. Output Files

- `analysis/chromatin-transcription-lag/_evidence/week2/scope.md`
- `analysis/chromatin-transcription-lag/_evidence/week2/papers.jsonl`
- `analysis/chromatin-transcription-lag/_evidence/week2/comparison_table.md`
- `analysis/chromatin-transcription-lag/_evidence/week2/evidence_bundle.md`
- `analysis/chromatin-transcription-lag/_evidence/week2/insight.md`
- `Skills/insight-agent.md`

### Speaker Note
2주차 산출물은 단일 문서가 아니라, Insight Agent가 재사용할 수 있는 입력 구조까지 포함합니다. 특히 `papers.jsonl`, `comparison_table.md`, `evidence_bundle.md`를 따로 둔 것이 핵심입니다.

---

## Slide 6. Role And Perspective

### Agent Role
- 단순 요약자가 아니라 `cross-paper analyst`
- 논문 간 관계, 반복 패턴, unresolved gap을 찾는 역할

### Required Perspectives
- `Field Flow`
- `Differentiation Map`
- `Repeated Limitations`
- `Unresolved Gaps`

### Speaker Note
이번 Agent의 역할은 논문을 잘 요약하는 것이 아니라, 여러 논문을 같이 봤을 때만 보이는 관계와 패턴을 찾는 것입니다. 그래서 최종 산출물도 네 개 섹션으로 제한했습니다.

---

## Slide 7. Summary Vs Insight

### Summary
- 각 논문이 무엇을 했는지 설명
- 논문별 독립 정보 중심

### Insight
- 논문들 사이의 관계를 설명
- 무엇이 field를 확장했는지 정리
- 공통 limitation과 unresolved gap 도출

### Example
- Summary: `MultiVelo는 priming/decoupling interval을 정의했다`
- Insight: `MultiVelo -> MultiVeloVAE -> MoFlow`로 갈수록 ordering -> continuous dynamics -> signed lag로 timing 개념이 확장됐다

### Speaker Note
이 부분이 가장 중요합니다. summary는 논문별 설명이고, insight는 논문 간 관계에서 새롭게 보이는 구조입니다. 그래서 최종 `insight.md`는 논문별 섹션 대신 field-level synthesis를 만들도록 설계했습니다.

---

## Slide 8. Main Insight 1 - Field Flow

- `MultiVelo`: ordering 정의
- `MultiVeloVAE`: continuous cell-specific dynamics
- `MoFlow`: signed lag interpretation

### Core message
chromatin-RNA timing 연구는  
`ordering -> continuous decoupling -> direct signed lag`  
방향으로 확장되고 있다.

### Speaker Note
첫 번째 핵심 insight는 field flow입니다. 세 논문을 시간순으로 보면, 단순히 새로운 모델이 나온 게 아니라 timing 개념 자체가 더 직접적이고 정량적인 쪽으로 이동하고 있다는 흐름이 보였습니다.

---

## Slide 9. Main Insight 2 - Differentiation Map

| Paper | Strong point | Weak point |
|---|---|---|
| MultiVelo | 개념적 foundation | latent time, discrete regime |
| MultiVeloVAE | continuous, sample-aware dynamics | lag를 직접 주지는 않음 |
| MoFlow | signed lag 해석이 가장 직접적 | gene-wise scope, perturbation validation 없음 |

### Speaker Note
둘째 insight는 각 논문의 역할 분리입니다. MultiVelo는 foundation, MultiVeloVAE는 refined dynamics, MoFlow는 가장 direct한 lag interpretation으로 볼 수 있었습니다.

추가로 주목할 점은, MultiVelo와 MoFlow가 SHARE-seq mouse skin과 E18 mouse brain이라는 동일한 데이터를 사용했는데 latent time에 대해 정반대 결론을 냈다는 것입니다. MultiVelo는 latent time이 적절한 timing 축이라고 했고, MoFlow는 고정된 global latent time이 오히려 lag 추정을 왜곡한다고 했습니다. 이것은 현재 field에서 temporal axis 자체가 아직 열린 문제임을 보여줍니다.

---

## Slide 10. Main Insight 3 - Repeated Limitations

- wall-clock calibration 부재
- lag-like estimate에 대한 uncertainty filtering 부재
- gene-level chromatin aggregation
- perturbation / drug response validation 부재

### Speaker Note
세 논문을 비교했을 때, limitation도 반복적으로 나타났습니다. 이것은 개별 논문의 약점이라기보다 현재 field 전체의 구조적 한계라고 해석했습니다.

---

## Slide 11. Main Insight 4 - Unresolved Gaps

1. pseudotime -> wall-clock calibration
2. baseline epigenomic features -> lag prediction  ← 이 프로젝트의 핵심 novelty
3. enhancer-level lag resolution
4. multi-sample robustness
5. Step 3 validation framework

### Speaker Note
가장 중요한 unresolved gap은 Step 2와 Step 3 쪽입니다. 특히 baseline feature로 lag를 예측하는 문제는 직접적인 precedent가 거의 없어서, 이 프로젝트의 핵심 novelty가 될 수 있다고 봤습니다.

---

## Slide 12. Project Implication

- Step 1:
  - `MoFlow`가 가장 직접적인 lag target 후보
  - `MultiVelo`는 conceptual vocabulary 제공
  - `MultiVeloVAE`는 cell-specific dynamic context 보완
- Step 2:
  - literature direct precedent가 거의 없음
  - novelty가 가장 큰 구간
- Step 3:
  - 현재 literature만으로는 validation이 부족함

### Speaker Note
프로젝트 관점에서는 Step 1은 기존 논문을 잘 조합하면 시작할 수 있지만, Step 2와 Step 3은 아직 literature gap이 큽니다. 이 점이 오히려 연구 기회라고 판단했습니다.

---

## Slide 13. What I Built

- `paper-analysis`와 `insight-agent`를 분리
- `papers.jsonl` / `comparison_table.md` / `evidence_bundle.md` 구조 설계
- `insight.md`를 네 개 섹션으로 생성
- figure / supplementary / method anchor까지 연결

### Speaker Note
이번 과제에서 단순히 답변만 생성한 것이 아니라, 반복 실행 가능한 입력 구조와 Insight Agent 규칙까지 같이 만들었습니다. 그래서 나중에 논문 수를 더 늘려도 같은 구조를 재사용할 수 있습니다.

---

## Slide 14. Limitations Of My Current Output

- 현재 논문 세트가 3편으로 작음
- `evidence_bundle.md`는 더 촘촘한 figure/table grounding 여지가 있음
- `insight.md`는 발표용으론 충분하지만, 논문화 수준으론 추가 검증 필요

### Speaker Note
현재 결과는 2주차 발표용으로는 충분하지만, 연구 결과물 수준으로 바로 가져가려면 논문 세트 확장과 근거 정밀화가 더 필요합니다.

---

## Slide 15. Next Step

1. 논문 세트 확장
   - related method / benchmark papers 추가
2. Step 1 후보 결정
   - MoFlow 기반 lag target 정의
3. Step 2 설계
   - baseline epigenomic feature -> lag prediction model 구상

### Speaker Note
다음 단계는 literature synthesis를 끝내는 것이 아니라, Step 1의 operational target을 정하고 Step 2 predictive task로 연결하는 것입니다.

---

## Slide 16. Closing

### One-line conclusion
이번 2주차 산출물의 핵심은  
`논문 요약 Agent`가 아니라  
`cross-paper insight를 만드는 Agent`를 만들었다는 점입니다.

### Speaker Note
정리하면, 이번 과제의 핵심 성과는 논문을 잘 읽는 것보다 논문들 사이에서 관계와 gap을 뽑아내는 Agent 구조를 만든 것입니다.
