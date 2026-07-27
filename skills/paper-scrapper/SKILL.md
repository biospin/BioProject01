---
name: paper-scrapper
description: Convert existing per-paper full.md analyses into comparable cross-paper records. Produces scope.md, papers.jsonl, comparison_table.md, and evidence_bundle.md as the structured input for insight-agent. Run only when 2+ papers in the same topic already have full.md.
---

# Paper Scrapper

## 언제 실행하나
같은 topic 아래 `full.md`가 2편 이상 있고, cross-paper insight를 만들려 할 때 실행한다.
`insight-agent`의 선행 단계이며, 단독으로도 비교표만 뽑는 용도로 쓸 수 있다.

## 입력
- `analysis/<topic>/<paper-title>/full.md` (2편 이상)
- 사용자가 지정한 topic 범위와 키워드

## 출력
모두 `analysis/<topic>/_evidence/week2/` 아래에 저장한다.

| 파일 | 내용 |
|---|---|
| `scope.md` | 주제, 키워드, 포함/제외 기준, 선정된 논문 목록 |
| `papers.jsonl` | 논문 1편 = 1 record. 비교 가능한 field로 정규화 |
| `comparison_table.md` | method / assay / result / limitation 4축 비교표 |
| `evidence_bundle.md` | insight-agent 입력용 근거 묶음 |

## 실행 절차

### Step 0 — scope.md 작성
논문을 읽기 전에 범위를 먼저 고정한다.
- 주제 한 문장
- 키워드 목록
- 포함 기준 / 제외 기준
- 선정된 논문과 선정 이유
- 제외한 논문이 있으면 제외 사유

범위를 먼저 쓰지 않으면 이미 분석한 논문에 맞춰 기준이 사후 조정된다.

### Step 1 — papers.jsonl 생성
각 `full.md`를 읽고 아래 schema로 record 1줄씩 쓴다. JSON Lines이므로 record 사이에 빈 줄을 넣지 않는다.

```
id                  짧은 식별자 (kebab-case)
title               논문 제목
authors             저자 배열
year, venue, doi    서지 정보
core_concept        이 논문이 도입한 핵심 개념 한 줄
method_class        method 계열 (예: ODE-based, VAE-based, local relay)
inputs              사용 modality 배열
key_outputs         이 method가 산출하는 것 배열
datasets            [{name, cells, genes, role}] — 수치가 없으면 null
baselines           비교 대상 method 배열
metrics             평가 지표 배열
key_numbers         [{name, value, context}] — full.md에 명시된 값만
limitations_author  저자가 명시한 한계 배열
limitations_analyst 분석자가 판단한 한계 배열
open_questions      정리되지 않은 질문 배열
source              근거가 된 full.md 경로
```

`full.md`에 없는 값은 추측하지 않고 `null` 또는 `"본문 미제시"`로 둔다.

### Step 2 — comparison_table.md 생성
`papers.jsonl`을 method / assay / result / limitation 4축으로 재배열한다.
- 축마다 표 하나를 만들고 행은 논문, 열은 비교 항목으로 둔다.
- result 축에는 반드시 `key_numbers`의 실제 값을 넣는다. "개선됨" 같은 서술만 쓰지 않는다.
- 같은 dataset을 쓴 논문이 있으면 별도로 표시한다. cross-paper 비교의 가장 강한 근거다.

### Step 3 — evidence_bundle.md 생성
insight-agent가 근거를 다시 `full.md`까지 찾아가지 않아도 되도록 묶는다.
각 항목은 다음을 포함한다.
- 근거 ID (`E-01` 형식)
- 논문
- 주장 또는 관찰
- 근거 (Figure 번호, 수치, dataset)
- caveat (해석 시 주의점)

`full.md`의 "해석 시 주의점"과 "분석자가 판단한 한계"를 caveat에 반드시 반영한다.

## 금지
- `full.md`에 없는 수치나 dataset을 만들어내지 않는다.
- 원문 PDF를 다시 읽어 새 수치를 넣지 않는다. 이 skill의 근거는 `full.md`다.
- 논문 간 우열을 이 단계에서 결론짓지 않는다. 해석은 `insight-agent`의 역할이다.
- 한 논문에만 있는 항목을 다른 논문에서도 있는 것처럼 표에 채우지 않는다. 없으면 "해당 없음"으로 둔다.

## 언어
AGENTS.md의 언어 규칙을 따른다. `papers.jsonl`의 key는 영어, value는 한국어로 쓰되 scientific term은 영어로 유지한다.
