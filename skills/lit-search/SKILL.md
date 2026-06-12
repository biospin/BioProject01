---
name: lit-search
description: 데이터셋(accession)·주제·seed method로부터 분석에 쓸 새 문헌을 웹/PubMed/Crossref/GEO에서 찾아 repo와 중복 제거 후 역할별로 분류한 candidate 목록을 만든다. paper-scrapper(Week2)·source-grounding(단일 full analysis)의 앞단 discovery 단계.
---

# Lit Search (문헌 발견)

## 목표

dataset accession(예: `GSE209878`), 주제(예: `epigenomic-lag`), 또는 seed method 이름(예: MultiVelo)을 받아, **이 프로젝트의 분석 목표에 쓸 수 있는 문헌을 능동적으로 찾아낸다**. 이미 repo에 있는 것과 새로 확보할 것을 구분하고, 각 문헌이 어떤 역할(anchor / method / benchmark / biology)인지 분류해 다음 단계로 넘길 수 있는 candidate 목록을 만든다.

이 skill은 다음 두 skill의 **앞단(discovery front-end)** 이다. 경계가 겹치지 않는다.

| Skill | 입력 | 하는 일 |
|---|---|---|
| **lit-search** (이 skill) | accession / topic / method | repo에 *아직 없는* 문헌을 찾아내고 중복 제거 후 분류 |
| `paper-scrapper` | 이미 알려진 paper 묶음 + `scope.md` | 같은 schema로 정규화해 `papers.jsonl` 등 record 생성 |
| `source-grounding` | 단일 paper(DOI/PDF/URL) | 폴더 생성 + `sources/` 다운로드 + `paper-info.yaml` |

→ lit-search 결과는 `paper-scrapper`(Week2 비교) 또는 `source-grounding`(단일 full analysis)으로 넘긴다.

## Source grounding

- Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 출력에서 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `검토필요:` 표기를 동일하게 사용한다.
- 검색 결과의 제목·저자·연도·DOI는 **확정 전 반드시 1차 출처(GEO 페이지, 출판사 landing, Crossref/PubMed)로 교차 확인**한다. 검색엔진 요약문만 근거로 메타데이터를 확정하지 않는다.
- 결과 수치(metric)·결론은 후속 full analysis 전에는 추측하지 않는다. lit-search 단계의 "why-relevant"는 abstract/title 수준 근거까지만 단정한다.
- repo에 commit하기 전 메타데이터는 `skills/metadata-verify/SKILL.md`로 검증한다.

## 입력

다음 중 하나 이상으로 시작한다.

- **dataset accession** — `GSE209878`, `GSE140203`, EGA/SRA/ArrayExpress ID 등.
- **topic** — `analysis/_index/papers.csv`의 기존 topic 또는 새 주제 키워드.
- **seed method / 도구 이름** — MultiVelo, MoFlow, scKINETICS 등.
- **본인 담당 dataset** — `CLAUDE.md`의 "팀 & 데이터셋 담당" 표에서 담당자가 맡은 dataset.

## 절차

### 1. Identity 해결 (accession → 원 논문)

accession이 입력이면 먼저 출처 publication을 특정한다.

- GEO: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=<GSE...>` 를 fetch → title / organism / platform / 설계(샘플·timepoint) / 연결된 PMID·DOI 추출.
- accession이 *기존 분석된 paper의 데이터셋*일 수 있다 — 반드시 repo와 대조한다(2단계). 예: `GSE209878` = MultiVelo(`li-2023-multivelo`)의 HSPC day0/day7 dataset.

### 2. repo 중복 제거 (가장 먼저, 매번)

새 검색에 들어가기 전에 이미 있는 것을 확인한다.

```bash
# 색인에서 제목·DOI·topic 확인
cat analysis/_index/papers.csv

# accession / 키워드 / DOI 가 repo에 이미 있는지
grep -rn -i '<accession 또는 키워드>' --include='*.md' --include='*.yaml' --include='*.csv' analysis/
```

이미 분석된 문헌은 "repo에 있음"으로 분류하고 새로 찾지 않는다. lit-search의 가치는 *repo에 없는* 문헌을 찾는 데 있다.

### 3. 다각도 검색 (modality별)

한 각도로는 누락이 생긴다. 아래 축을 각각 검색한다(WebSearch + 1차 출처 fetch).

- **Origin / anchor** — dataset/주제를 만든 원 논문. (1단계에서 대개 해결됨.)
- **Method genealogy** — seed method의 직접 후속·대체·경쟁 방법. 특히 *우리 분석 목표(chromatin–transcription lag 정량)* 에 직접 쓰는 도구.
- **Benchmark / 비교 연구** — 후보 method들을 비교한 최신 벤치마크(어떤 method를 쓸지 근거).
- **Biology 검증 문헌** — 프로젝트 핵심 가설(`CLAUDE.md` "연구 프로젝트 핵심 개념": activation/shutdown lag, chromatin priming)을 *같은 생물학적 시스템*에서 뒷받침/반증하는 문헌.

검색 시점이 중요하면 최신 연도를 명시한다(현재 기준 연도 확인). preprint(bioRxiv/medRxiv/arXiv)는 publication 여부를 따로 표시한다.

### 4. 분류

각 후보를 두 축으로 분류한다.

- **repo 상태**: `repo에 있음` / `새로 확보`.
- **역할**: `anchor`(데이터셋 원 논문) / `method`(분석 도구) / `benchmark` / `biology`(가설 검증).

그리고 use_case(`AGENTS.md` Categorization 6종 vocabulary: `pipeline-applicable`, `methodology-reference`, `academic-citation` 등) 후보를 단서로 단다.

### 5. 출력

기본 출력은 markdown candidate 목록이다. 위치는 입력 종류에 따른다.

- dataset 기반: `analysis/_datasets/<dataset-id>/lit-search.md` (+ 확정 시 `secondary-refs.md`에 항목 추가)
- topic 기반(Week2): `analysis/<primary-topic>/_evidence/lit-search/<query-slug>.md` (→ `scope.md` seed로 사용)

출력 형식:

```markdown
# Lit Search — <입력 요약>
- 수행일: <YYYY-MM-DD>
- 입력: <accession / topic / method>
- 분석 목표 정합: <CLAUDE.md 목표와의 연결 한 줄>

## 데이터셋/주제 Identity
- <accession → 원 논문, 설계, repo 내 위치>

## repo에 이미 있어 직접 쓰는 문헌
| paper-id | 역할 | why |
|---|---|---|

## 새로 확보 권장 — Method
| 제목 | 저자·연도·venue | DOI/URL | 역할 | why (출처 근거까지) | repo 상태 |
|---|---|---|---|---|---|

## 새로 확보 권장 — Biology (가설 검증)
| ... |

## 권장 다음 단계
- <source-grounding 단일 분석으로 보낼 것 / paper-scrapper Week2 record로 묶을 것 / _datasets secondary-ref로 추가할 것>
```

## 핸드오프

- **단일 paper를 곧바로 full 분석** → `source-grounding`으로 DOI/URL 넘김 → 이후 `core-*` 흐름.
- **여러 후보를 비교** → `analysis/<topic>/_evidence/week2/scope.md`의 seed로 넣고 `paper-scrapper` 실행.
- **dataset reference 보강** → `analysis/_datasets/<dataset-id>/secondary-refs.md`에 확정 항목 추가, 해당 paper 분석 폴더에 `related:` 양방향 cross-ref.

## 언어 / 톤

`AGENTS.md`의 언어·톤 규칙을 따른다. 한국어 기본, 표준 scientific term은 영어 유지. 검색 결과를 단정적으로 옮기되 확인 안 된 메타데이터는 `추정:` 표시.
