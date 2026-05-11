---
name: full-overview
description: Analyze the Overview section of a full scientific paper review. Use when Codex needs to explain whether Figure 1 belongs to the paper overview, identify the core concepts used by the paper, describe how the paper reframes those concepts as a method, summarize what this reveals, and state the expected effects or benchmark-level implications.
---

# Full Overview

## 목표
논문의 Overview를 “이 논문이 어떤 핵심 개념을 어떤 method 관점으로 재구성했고, 그 결과 무엇을 알 수 있게 되었으며, 어떤 기대 효과가 있는가”의 흐름으로 정리한다. 일반적으로 Figure 1은 논문의 전체 방법 개요를 담는 경우가 많으므로, Overview 작성 전에 Figure 1이 overview에 해당하는지 먼저 확인한다.

## 언어 규칙
- 기본 출력은 한국어로 작성한다.
- `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `baseline`, `dataset`, `benchmark`, `Figure 1`처럼 분야에서 그대로 쓰는 용어는 영어를 유지할 수 있다.
- 영어 용어를 유지할 때는 처음 한 번 한국어 설명을 덧붙인다.
- 불필요하게 문장 전체를 영어로 쓰지 않는다.

## 작업 절차
1. Figure 1의 제목, caption, 본문 언급을 먼저 확인한다.
2. Figure 1이 논문의 전체 개념 또는 방법 구조를 설명하는지 판단한다.
3. Overview 첫 줄에 Figure 1 포함 여부를 명시한다.
   - 포함되면: `Figure 1 포함 여부: 포함됨 - 이유: ...`
   - 포함되지 않으면: `Figure 1 포함 여부: 포함되지 않음 - 이유: ...`
4. 논문이 사용하는 핵심 개념을 뽑는다.
5. 그 개념을 어떤 method 관점에서 바라보는지 설명한다.
6. 그 method를 적용해서 무엇을 알 수 있게 되었는지 정리한다.
7. 기대 효과를 정리한다. benchmark, baseline, dataset, downstream task 성능이 언급되면 보존한다.

## 출력 형식
사용자가 다른 형식을 요청하지 않으면 아래 구조를 따른다.

```markdown
### Overview
- Figure 1 포함 여부:

#### 핵심 개념
- 개념:
- 이 개념이 필요한 이유:

#### Method 관점
- 논문이 이 개념을 바라본 방식:
- 입력:
- 처리 과정:
- 출력:

#### 이 관점으로 알 수 있는 것
- 알 수 있게 된 점 1:
- 알 수 있게 된 점 2:

#### 기대 효과
- 성능 또는 분석상 기대 효과:
- benchmark / baseline 관련 근거:
- 적용 가능한 상황:
```

## 작성 규칙
- Overview는 Background보다 한 단계 더 방법 중심이어야 한다. “왜 필요한가”보다 “무엇을 어떻게 사용했는가”를 중심에 둔다.
- Figure 1이 overview에 해당하면 Figure 1 설명을 Overview 안에 통합하고, Figure 분석 섹션에서는 중복을 줄인다.
- `A라는 개념을 B라는 method 관점에서 바라보았고, 그 결과 C를 알 수 있었다`의 문장 흐름을 우선한다.
- 방법 설명은 너무 세부적인 수식 전개보다 핵심 입력, 변환, 출력이 보이게 쓴다.
- 기대 효과는 논문에 근거가 있는 범위에서 쓴다. 논문이 benchmark나 baseline 결과를 제시하면 수치나 비교 대상을 보존한다.
- 성능 근거가 아직 Overview 단계에서 명확하지 않으면 `성능 근거는 Results에서 확인 필요`라고 표시한다.

## 예시 문장
```markdown
- 이 논문은 `chromatin accessibility`라는 개념을 RNA velocity의 동역학 method 관점에서 다시 바라본다. 즉 chromatin이 열리고 닫히는 상태를 RNA 생성 과정의 외부 배경이 아니라, unspliced RNA와 spliced RNA 변화를 함께 설명하는 시간 변수로 넣는다. 그 결과 chromatin이 먼저 열렸지만 RNA가 아직 증가하지 않은 priming 상태와, chromatin closing과 transcription repression이 어긋나는 decoupling 상태를 구분할 수 있다.
```
