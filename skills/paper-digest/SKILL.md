---
name: paper-digest
description: Create a structured paragraph-by-paragraph digest of a paper that follows the paper's own section and paragraph order. Use when the user wants a condensed but faithful summary (0.5–1 page) that preserves the paper's narrative flow, distinct from the analysis-framework reorganization of full.md. Each paragraph in the paper becomes one sentence in the digest.
---

# Paper Digest

## 목표
논문의 실제 섹션·단락 구조를 그대로 따라가면서, 각 단락을 한 문장으로 압축한다. `full.md`가 분석 프레임워크(Background/Overview/Methods/Results/Discussion)로 재구성하는 것과 달리, 이 skill은 저자가 논문을 쓴 순서와 흐름을 유지한다. 결과물은 반 페이지에서 한 페이지 분량(약 400–800어 내외)이 되어야 한다.

## 언어 규칙
AGENTS.md의 언어 규칙을 따른다.

## full.md와의 차이

| | full.md | paper-digest |
|---|---|---|
| 구조 | 분석 프레임워크로 재구성 | 논문 원본 섹션 순서 유지 |
| 깊이 | 분석·판단·한계 포함 | 요약·압축만 |
| 분량 | 긴 문서 (섹션별 상세) | 반 페이지–한 페이지 |
| 용도 | 깊은 이해, 후속 연구 설계 | 빠른 내용 파악, 공유·발표 준비 |

## 사용 시점
- 사용자가 `full.md` 외에 논문 흐름을 따르는 간결한 버전을 원할 때.
- 논문 내용을 다른 사람에게 빠르게 전달해야 할 때.
- 논문 전체를 읽지 않고 각 단락에서 무슨 말을 하는지 파악하고 싶을 때.

## 작업 절차
0. 이미 작성된 `full.md`가 있으면 먼저 읽어 논문 구조를 파악한다.
1. 논문의 실제 섹션 순서를 그대로 따른다 (Introduction → Results subsections → Discussion → Limitations).
2. 각 단락(paragraph)을 읽고 핵심 주장 또는 발견을 한 문장으로 압축한다.
   - 단락이 매우 짧거나 기술적 세부사항만 담고 있으면 앞뒤 단락과 합칠 수 있다.
   - 수치, 데이터셋 이름, 핵심 용어는 보존한다.
3. 각 섹션 제목은 논문 원문 제목을 그대로 쓴다.
4. 전체 분량이 반 페이지–한 페이지가 되도록 조정한다.
   - 너무 길면 덜 중요한 기술적 세부 단락을 합치거나 생략한다.
   - 너무 짧으면 핵심 수치나 비교 결과를 문장에 추가한다.

## 출력 형식
```markdown
# [논문 제목] — Digest

**저자**: ...  **저널**: ...  **연도**: ...

## Introduction
[단락 요약 문장들]

## Results

### [Results subsection 제목]
[단락 요약 문장들]

### [다음 subsection]
...

## Discussion
[단락 요약 문장들]

## Limitations
[한계 요약 문장들]
```

## 작성 규칙
- 한 단락 → 한 문장 원칙. 단, 짧은 전환 단락은 묶어도 된다.
- 저자의 주장을 그대로 전달한다. 분석자의 판단이나 비판은 넣지 않는다.
- 수치(AUC, n수, sensitivity 등)는 최소 1개 이상 문장에 포함한다.
- 논문에 없는 내용을 추가하지 않는다.
- 출력 파일은 `analysis/<topic>/<paper-title>/digest.md`에 저장한다.
