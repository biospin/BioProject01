---
name: abstract-analysis
description: Analyze scientific paper abstracts. Use when Codex needs to summarize, rewrite, extract, or structure a paper Abstract into research purpose, problem or gap, method, main findings, claimed contribution, and caveats.
---

# Abstract Analysis

## 목표
논문 Abstract를 읽고 연구의 전체 지도를 짧고 명확하게 만든다. 논문이 풀려는 문제, 왜 중요한지, 어떤 방법을 제안하는지, 어떤 근거를 제시하는지, 저자가 주장하는 기여가 무엇인지 정리한다.

## Source grounding
- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.
  본 skill의 출력에서도 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
- 출력은 `analysis/<primary-topic>/<paper-id>/abstract.md`. abstract.md는 full paper로 확장되어도 보존되며 `core.md`와 공존한다.

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `baseline`, `dataset`, `benchmark`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 유지할 때는 처음 한 번 한국어 설명을 덧붙인다.
- 불필요하게 문장 전체를 영어로 쓰지 않는다.

## 작업 절차
1. Abstract 전체를 먼저 읽는다.
2. 연구 분야와 task를 파악한다.
3. 연구를 촉발한 문제, 한계, gap을 뽑는다.
4. 제안한 방법이나 접근법을 뽑는다.
5. 데이터셋, 지표, 수치 결과가 있으면 보존한다.
6. 저자가 주장하는 기여와 기대 효과를 뽑는다.
7. Abstract에 없는 정보는 추측하지 말고 빠진 항목으로 표시한다.

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 아래 구조를 따른다.

```markdown
## Abstract Summary
- 한 문장 요약:
- 연구 목적:
- 문제 또는 gap:
- 핵심 방법:
- 주요 결과:
- 저자가 주장하는 기여:
```

## 추출 규칙
- 구체적인 수치, benchmark 이름, dataset 이름, model 이름, task 이름은 유지한다.
- 논문이 실제로 한 일과 논문이 달성했다고 주장하는 일을 구분한다.
- Abstract에 결과가 없으면 `Abstract에 명시되지 않음`이라고 쓴다.
- Abstract가 모호하거나 과장되어 있으면 `모호한 주장:`으로 표시한다.
- Abstract 밖의 배경 지식을 추가해야 할 때는 `Abstract 외부 맥락:`으로 분리한다.

## 문체
- 간결하고 분석적으로 쓴다.
- 칭찬이나 홍보 문구를 피한다.
- 논문에 없는 내용을 채워 넣지 않는다.