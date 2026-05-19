---
name: core-problem
description: Analyze the problem definition and research purpose for the objective <paper-id>_core.md section. Use to explain why this work became necessary, what prior approaches achieved and failed to solve, what gap led to the proposed work, and what basic concepts are needed. Outputs the "문제 정의 및 연구 목적" portion of <paper-id>_core.md.
---

# Core Problem

## 목표
이 자료의 *문제 정의*와 *연구 목적*을 단순 선행연구 나열이 아니라 "왜 이 자료가 나올 수밖에 없었는가"에 대한 배경 스토리로 정리한다. 기존 방법 A, B, C가 각각 무엇을 했고 무엇을 해결하지 못했는지 연결해서, 이 자료가 해결하려는 문제로 자연스럽게 이어지게 만든다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 출력은 `analysis/<primary-topic>/<paper-id>/<paper-id>_core.md`의 "문제 정의 및 연구 목적" 섹션에 누적된다.

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `baseline`, `dataset`, `benchmark`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 유지할 때는 처음 한 번 한국어 설명을 덧붙인다.
- 불필요하게 문장 전체를 영어로 쓰지 않는다.

## 작업 절차
1. Introduction, Related Work, 첫 번째 Results 도입부를 중심으로 읽는다.
2. 논문이 다루는 큰 생물학적 또는 기술적 문제를 한 문장으로 정리한다.
3. 선행 접근들을 역할별로 묶는다.
   - A는 무엇을 가능하게 했는가?
   - A는 무엇을 못했는가?
   - B는 무엇을 보완했는가?
   - B에도 남은 한계는 무엇인가?
4. 위 한계들이 어떻게 이 논문의 연구 질문으로 이어지는지 설명한다.
5. 논문 이해에 필요한 기본 개념을 별도로 정리한다.
6. 배경 설명과 논문 기여를 섞지 않는다. Background에서는 “왜 필요한가”에 집중한다.

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 아래 구조를 따른다.

```markdown
### Background

#### 배경 스토리
- 문제의 출발점:
- 선행 접근 A:
- A의 한계:
- 선행 접근 B:
- B의 한계:
- 이 논문으로 이어지는 gap:

#### 기본 개념
- 개념 1:
- 개념 2:
- 개념 3:

#### 이 논문이 필요성
- 핵심 이유:
- 기존 방법으로 부족했던 지점:
- 이 논문이 해결하려는 방향:
```

## 배경 스토리 작성 규칙
- “기존 연구가 있었다”라고만 쓰지 말고, 기존 연구가 열어준 가능성과 남긴 한계를 함께 적는다.
- 가능하면 `A는 X를 가능하게 했지만 Y는 못했다. B는 Y 일부를 보완했지만 Z는 여전히 남았다. 그래서 이 논문은 Z를 해결하려 한다.`의 흐름으로 쓴다.
- 선행연구 이름이 명시되어 있으면 이름을 보존하고, 명시되지 않으면 방법 계열로 묶는다.
- 저자가 주장한 gap과 분석자가 재구성한 gap을 섞지 않는다. 필요한 경우 `해석:`이라고 표시한다.

## 기본 개념 정리 규칙
- 논문 이해에 꼭 필요한 개념만 고른다.
- 개념 설명은 짧게 쓰되, 논문의 방법과 어떻게 연결되는지 포함한다.
- 생물학적 단계나 계산 과정이 있으면 순서로 정리한다.

예시:

```markdown
- 유전자 발현 흐름: DNA의 조절 영역이 열리는 `chromatin opening` 이후 `TF binding`이 가능해지고, 이어서 `transcription`으로 RNA가 만들어진다. 이후 조절 신호가 사라지면 `TF release`, `chromatin closing`, transcription 감소가 이어질 수 있다. 이 논문은 이 단계들이 항상 동시에 일어나지 않고 시간차가 생긴다는 점을 모델링한다.
```

## 주의할 점
- Background에서 결과 수치나 실험 성능을 길게 설명하지 않는다.
- 논문이 실제로 인용하거나 설명한 선행 흐름에 근거한다.
- 외부 지식을 추가하면 `외부 기본 개념:`으로 표시한다.
