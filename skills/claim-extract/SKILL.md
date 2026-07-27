---
name: claim-extract
description: Extract core claims, research gap, and prior work positioning through selective reading of Abstract and Introduction. Pull only the sentences that define what the paper claims and why—do not read comprehensively.
---

# Claim Extract

## 언제 실행하나
`fig1-decode` 이후 실행한다. Abstract와 Introduction을 처음부터 끝까지 읽지 않는다. 목표는 발췌독으로 핵심 주장만 뽑는 것이다.

## 입력
논문 PDF (Abstract, Introduction).

## 발췌 대상 문장
다음 유형의 문장만 찾아 추출한다.

**뽑을 것:**
- 논문이 풀려는 문제를 정의하는 문장
- 기존 방법의 한계를 직접 서술하는 문장
- "우리는 X를 제안한다 / 개발한다 / 보인다" 형태의 기여 선언 문장
- 데이터 규모나 실험 조건을 언급하는 문장
- Abstract에 있는 핵심 수치 결과

**뽑지 않을 것:**
- 이미 알려진 사실 나열 (배경 설명)
- "Section 2에서는..." 형태의 논문 구성 안내
- "우리의 방법은 혁신적으로..." 형태의 수사

## 실행 절차
1. Abstract 전체를 읽고 발췌 대상 문장을 표시한다.
2. Introduction 마지막 단락 (기여 요약)을 읽는다.
3. Introduction 중간에서 "기존 방법의 한계" 단락 하나를 찾아 읽는다.
4. 발췌 문장들을 출력 형식으로 구조화한다.
5. Abstract에 없는 항목은 "Abstract에 명시 없음"으로 표시한다. 추측하지 않는다.

## 출력 형식

```markdown
### Claim Extract

**연구 문제:**

**기존 방법의 한계:**

**이 논문의 주장 (저자 원문 기반):**

**핵심 수치 결과 (있으면):**

**데이터 / 실험 규모 (있으면):**

**Introduction에서 추가로 파악한 내용:**
```

## 주의
- 저자가 실제로 쓴 문장에 근거한다. 해석이나 요약으로 바꾸지 않는다.
- 과장된 주장은 그대로 인용하되, 신빙성 판단은 `quality-gate`에서 한다.
- 발췌가 아니라 요약을 쓰면 저자의 주장이 희석된다.
