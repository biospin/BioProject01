---
name: core-methods
description: Analyze the methodology for the objective core.md section. Always invoked, with adaptive depth — full probabilistic/statistical analysis for method-centric papers, method taxonomy for review papers, protocol summary for biology-finding papers, and brief notes for non-paper materials.
---

# Core Methods

## 적용 범위 (Adaptive Depth)

이 skill은 모든 자료에서 *항상* 호출된다. 단 *자료 유형에 따라 깊이를 조정*한다. 억지로 자세한 method 섹션을 만들지 않고, *그 자료의 method 비중*에 맞춘다.

| 자료 유형 | 작성 깊이 | 강조 포인트 |
|---|---|---|
| **Computational methods 중심 paper** (algorithm, benchmark, statistical model) | Full | 확률/통계 구조, objective, baseline 차이, ablation 효과 |
| **실험 biology paper, finding 중심** | Protocol 요약 + statistical assumption | 사용된 통계 검정, sample size, replicate 수, 주요 protocol step |
| **Review paper** | Method taxonomy | 비교된 method 군의 분류와 계열별 강점·한계 |
| **Database / resource paper** | Curation pipeline 요약 | 데이터 수집·정제·QC 절차, version 관리 |
| **Non-paper** (industry-report, whitepaper, blog, news) | 있는 만큼만 | method가 있으면 정리, 없으면 `미제공:`으로 명시. 억지로 채우지 않는다. |

깊이 결정 기준:
- abstract와 본문의 첫 1~2 문단이 *method*인지 *finding*인지를 본다.
- `Methods`, `Model`, `Algorithm`, `Inference`, `Loss function`, `Objective`, `Training`, `Benchmark`, `Ablation` section이 자료의 중심이면 Full.
- 자료가 *결과 중심*이면 Protocol 요약.
- 분류가 애매하면 *Full에 가까운 작성*을 시도하되 `검토필요:`로 표시.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 출력은 `analysis/<primary-topic>/<paper-id>/core.md`의 "방법론" 섹션에 누적된다.

## 목표

Methods를 단순 절차 요약이 아니라 “이 논문이 어떤 probabilistic/statistical insight로 기존 한계를 바꿨는가” 중심으로 분석한다. 특히 다음 네 가지를 반드시 분리한다.

1. 이 method가 풀려는 formal problem.
2. method 내부의 확률/통계/최적화 구조.
3. 이전 method와 다른 핵심 insight.
4. 그 차이가 Results에서 어떤 효과로 나타났는지.

## 언어 규칙

- 기본 출력은 한국어로 작성한다.
- `likelihood`, `prior`, `posterior`, `latent variable`, `variational inference`, `Bayesian`, `Markov`, `ODE`, `loss function`, `regularization`, `optimization`, `gradient`, `negative sampling`, `benchmark`, `ablation`, `baseline`, `metric`처럼 분야에서 자연스러운 용어는 영어로 유지할 수 있다.
- 영어 용어를 처음 사용할 때는 필요한 경우 짧게 한국어 설명을 붙인다.
- 수식이 있으면 그대로 보존하되, 수식의 역할을 한국어로 설명한다.

## 작업 절차

1. Abstract, Introduction 마지막 기여 요약, Methods/Model/Algorithm section, Figure 1 또는 method overview figure, ablation/benchmark Results를 함께 읽는다.
2. 논문이 푸는 computational task를 formal하게 정리한다.
   - 입력:
   - 출력:
   - 추정 대상:
   - latent variable 또는 hidden state:
   - supervised/unsupervised/self-supervised/semisupervised 여부:
3. 확률/통계학적 구조를 분해한다.
   - generative model인지 discriminative model인지.
   - likelihood, prior, posterior, transition model, observation model이 있는지.
   - objective/loss function이 무엇을 벌점화하거나 보상하는지.
   - uncertainty, noise, sparsity, missingness, confounding, time lag, batch effect 등을 어떻게 처리하는지.
4. method insight를 설명한다.
   - 기존 방법이 어떤 assumption 때문에 한계가 있었는지.
   - 이 논문이 그 assumption을 어떻게 바꿨는지.
   - 새 변수가 biological 또는 computationally 어떤 의미를 갖는지.
5. 이전 method / baseline과 비교한다.
   - 무엇을 그대로 가져왔는가?
   - 무엇을 제거/완화/추가했는가?
   - 어떤 data regime에서 차이가 커지는가?
6. Results와 연결한다.
   - benchmark에서 어떤 metric이 개선되었는가?
   - ablation에서 어떤 component가 중요했는가?
   - failure case 또는 trade-off가 있는가?
7. 한계를 적되, Discussion의 일반 limitation과 중복하지 말고 method design 관점으로 제한한다.

## 출력 형식

사용자가 다른 형식을 요청하지 않으면 `full.md` 안에 아래 구조로 추가한다.

```markdown
### Methods

#### 이 method가 푸는 문제
- Formal task:
- 입력:
- 출력:
- 추정 대상:
- 중요한 hidden assumption:

#### 확률 / 통계학적 구조
- Model family:
- Likelihood / objective:
- Prior / regularization:
- Latent variable / hidden state:
- Inference / optimization:
- Noise, sparsity, uncertainty 처리:

#### 핵심 method insight
- 기존 방법의 한계:
- 이 논문의 바꾼 가정:
- 새로 추가한 변수 또는 구조:
- 이 변화가 중요한 이유:

#### 이전 방법과의 차이
- Baseline:
- 공통점:
- 차이점:
- 차이가 크게 나타나는 조건:

#### 효과가 Results에서 나타난 방식
- Benchmark / dataset:
- Metric:
- 개선된 결과:
- Ablation 근거:
- 정성적 효과:

#### Method 관점의 한계
- 약한 assumption:
- 구현 또는 학습상의 부담:
- 일반화가 불확실한 조건:
```

## 작성 규칙

- Methods는 Overview보다 더 수학적/알고리즘적으로 쓴다. Overview가 “무엇을 어떻게 사용하는가”라면, Methods는 “왜 이 objective와 statistical assumption이 이전보다 낫다고 주장하는가”를 설명한다.
- Results와 중복해서 모든 수치를 길게 반복하지 않는다. Methods에서는 component의 효과를 보여주는 수치와 ablation만 선별해 연결한다.
- 수식이 복잡하면 전체 전개를 복사하지 말고, 각 term의 의미를 설명한다.
- method paper의 핵심 figure가 Figure 1이면 Overview와 중복을 피한다. Overview에서는 큰 흐름을 설명하고, Methods에서는 확률/통계 구조와 objective를 자세히 설명한다.
- baseline을 단순 나열하지 않는다. “baseline은 어떤 assumption을 가지고 있고, 이 논문은 그 assumption을 어떻게 바꿨는가”로 비교한다.
- 새로운 notation을 만들지 않는다. 논문 notation을 따르고, 불명확하면 자연어로 설명한다.
- 논문에 없는 수식적 해석을 사실처럼 쓰지 않는다. 필요한 경우 `해석:`이라고 표시한다.

## 좋은 분석의 형태

```markdown
- 기존 RNA velocity model은 unspliced/spliced RNA dynamics만으로 latent time을 추정하기 때문에, chromatin accessibility가 transcription보다 먼저 변하는 priming state를 직접 모델링하지 못한다.
- 이 논문은 chromatin state를 observation noise가 아니라 transcription rate를 조절하는 시간 지연 변수로 둔다. 따라서 likelihood는 RNA count를 맞추는 것뿐 아니라 chromatin opening/closing과 RNA induction/repression 사이의 lag를 설명해야 한다.
- ablation에서 chromatin term을 제거하면 fate prediction 또는 pseudotime alignment가 떨어진다면, 이것은 새 변수의 효과가 단순 feature 추가가 아니라 dynamic assumption의 개선에서 온다는 근거가 된다.
```

## 주의할 점

- Review paper에는 이 section을 억지로 만들지 않는다. review에서 computational methods를 비교한 경우에는 `Results`나 `Figure / Table Analysis`에서 method taxonomy로 정리한다.
- Biology finding 중심 논문에서는 method를 과하게 확대하지 않는다.
- “확률 통계학적 방법”이 명시적으로 없고 deterministic algorithm 중심이면, objective, optimization, model assumption, complexity, benchmark design 중심으로 대체한다.
- 논문이 code나 implementation detail을 제공하면 reproducibility 관점에서 중요한 hyperparameter, training detail, split strategy, runtime을 보존한다.
