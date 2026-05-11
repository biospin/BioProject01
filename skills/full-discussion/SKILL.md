---
name: full-discussion
description: Analyze the Discussion, Limitations, and Final Takeaways of a full scientific paper review. Use when Codex needs to judge what is insufficient, what explanations are not smooth, what important topics were not addressed, and how those limitations can become future research directions or next-paper ideas.
---

# Full Discussion

## 목표
논문의 Limitations와 Final Takeaways를 깊게 정리한다. 단순히 저자가 적은 한계를 옮기는 것이 아니라, 앞서 정리한 Background, Overview, Figure, Results를 바탕으로 어떤 설명이 부족한지, 어떤 연결이 매끄럽지 않은지, 어떤 실험이나 분석이 빠졌는지 판단한다. 이 판단은 다음 논문 아이디어와 후속 연구 방향으로 이어져야 한다.

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `baseline`, `dataset`, `benchmark`, `metric`, `causal evidence`, `perturbation`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 유지할 때는 처음 한 번 한국어 설명을 덧붙인다.
- 불필요하게 문장 전체를 영어로 쓰지 않는다.

## 작업 절차
1. 저자가 Discussion이나 Limitation에서 명시한 한계를 먼저 정리한다.
2. Background, Overview, Figure, Results에서 드러난 약한 연결을 다시 본다.
3. 설명이 매끄럽지 않은 부분을 찾는다.
   - 주장과 evidence 사이에 gap이 있는가?
   - 특정 dataset에서는 맞지만 다른 dataset 일반화가 약한가?
   - 수치 대신 visual plausibility에 의존하는가?
   - causal claim처럼 보이지만 실제로는 association만 보였는가?
4. 논문이 정리하지 않은 부분을 찾는다.
   - missing benchmark
   - missing ablation
   - missing perturbation / validation
   - missing robustness analysis
   - missing failure case
   - missing biological mechanism
5. 각 limitation을 다음 논문 아이디어로 변환한다.
6. Final Takeaways에서는 “그래서 다음에는 무엇을 하면 설명이 더 매끄러워지는가”를 중심으로 쓴다.

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 아래 구조를 따른다.

```markdown
### Limitations

#### 저자가 명시한 한계
- 한계 1:
- 한계 2:

#### 분석자가 판단한 한계
- 부족한 점:
- 왜 중요한가:
- 어떤 증거가 부족한가:

#### 설명이 매끄럽지 않은 지점
- 연결이 약한 주장:
- 현재 논문에서 제시한 근거:
- 더 필요해 보이는 근거:

#### 정리되지 않은 질문
- 질문 1:
- 질문 2:

## Final Takeaways
- 이 논문의 가장 큰 의미:
- 다음 논문으로 이어질 아이디어:
- 설명을 더 매끄럽게 만들 방법:
- 우선순위가 높은 후속 실험 / 분석:
```

## Limitation 판단 규칙
- 저자 명시 한계와 분석자 판단 한계를 구분한다.
- 단순 비판이 아니라 “왜 이 한계가 논문 주장에 영향을 주는지”를 함께 쓴다.
- Figure와 Results에서 수치가 약하거나 visual evidence에 의존한 부분은 표시한다.
- causal evidence가 없는데 regulation을 강하게 해석하는 부분은 주의점으로 남긴다.
- dataset generalization, robustness, ablation, baseline, reproducibility를 반드시 점검한다.

## Final Takeaways 작성 규칙
- Final Takeaways는 요약이 아니라 다음 연구 설계의 출발점이어야 한다.
- 각 takeaway는 가능하면 후속 실험 또는 분석으로 바꿀 수 있게 쓴다.
- “다음 논문 아이디어”는 구체적으로 적는다.
  - 어떤 dataset을 더 써야 하는가?
  - 어떤 baseline이나 ablation을 추가해야 하는가?
  - 어떤 perturbation 또는 validation이 필요한가?
  - 어떤 mechanism을 추가 모델링하면 좋은가?
- 설명을 매끄럽게 만들 방법을 별도로 쓴다.

## 좋은 판단의 형태
```markdown
- 부족한 점: 이 논문은 TF expression이 motif accessibility보다 먼저 나타난다고 해석하지만, 이것은 time lag 기반 association이다.
- 왜 중요한가: regulatory causality를 주장하려면 TF perturbation 후 motif accessibility와 target gene expression이 함께 바뀌는지 확인해야 한다.
- 다음 논문 아이디어: MultiVelo latent time으로 예측한 TF-gene regulatory pair를 perturb-seq 또는 CRISPRi로 검증한다.
```

## 주의할 점
- 논문에 없는 내용을 사실처럼 쓰지 않는다.
- 한계를 과장하지 않는다. “가능한 약점”과 “확인된 약점”을 구분한다.
- Final Takeaways는 읽는 사람이 실제 후속 연구를 설계할 수 있을 만큼 구체적으로 쓴다.
