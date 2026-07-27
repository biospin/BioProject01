---
name: fig1-decode
description: Decode the paper's core approach through Figure 1 as the primary entry point. Classifies Figure 1 type and falls back to Introduction + Discussion arc when Figure 1 is uninformative. Always run this first before any other analysis agent.
---

# Figure 1 Decode

## 언제 실행하나
새 논문 분석을 시작할 때 가장 먼저 실행한다. 이후 모든 에이전트의 맥락 기준이 된다.

## 입력
논문 PDF.

## 실행 절차

### Step 1 — Figure 1 유형 분류
Figure 1을 열고 다음 중 어느 유형인지 판단한다.

| 유형 | 특징 | 다음 단계 |
|---|---|---|
| Overview / Pipeline | 논문 전체 approach나 데이터 흐름을 설명하는 schematic | Step 2A |
| Result Figure | 실험 결과나 데이터를 바로 보여주는 그림 | Step 2B |
| Background / Motivation | 문제 상황이나 기존 방법의 한계를 설명하는 그림 | Step 2B |
| 불명확 | 무엇을 말하는지 한 번에 파악하기 어려운 그림 | Step 2B |

### Step 2A — Figure 1이 Overview인 경우
Figure 1 caption과 본문에서 해당 Figure를 처음 언급하는 단락을 함께 읽는다.

추출 항목:
- 논문이 다루는 입력 데이터 유형
- 핵심 처리 단계 또는 모델 구조
- 출력 또는 분석 결과 유형
- 기존 방법과 이 논문이 다른 포인트 (Figure에서 보이는 범위)

### Step 2B — Figure 1이 Overview가 아닌 경우 (대체 전략)
다음 순서로 논문의 story arc를 구성한다. 각 단계에서 두 단락을 넘기지 않는다.

1. Introduction 마지막 단락 — 저자가 기여를 직접 선언하는 부분
2. Discussion 또는 Conclusion 첫 단락 — 논문이 달성했다고 주장하는 내용
3. 이 두 단락을 조합해 "이 논문은 X 문제를 Y 방식으로 푼다"를 도출한다
4. Overview Figure가 다른 번호에 있으면 (예: Figure 2가 method schematic) 해당 Figure로 Step 2A를 실행한다

### Step 3 — 핵심 접근법 정리
어떤 경로로 파악했는지 명시한 뒤 출력 형식을 채운다.

## 출력 형식

```markdown
### Figure 1 Decode

**파악 경로:** [Figure 1 Overview | 대체 전략 (Intro + Discussion) | Figure N Overview]

**논문이 다루는 문제 (한 문장):**

**핵심 접근법 (한 문장):**

**입력 데이터:**

**출력 / 분석 결과:**

**기존 방법과 다른 포인트:**
```

## 주의
- Figure 1만 보고 해석을 과도하게 확장하지 않는다. 불명확하면 즉시 대체 전략으로 넘어간다.
- 대체 전략에서도 지정한 단락 외에 더 읽지 않는다. 빠른 진입이 목적이다.
- 수치 결과나 방법의 세부 사항은 이 단계에서 채우지 않는다.
- 어떤 경로로 파악했는지 항상 출력에 표시한다.
