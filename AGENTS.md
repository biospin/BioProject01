# Paper Researcher Agent Router (Dual Lens)

이 프로젝트는 scientific paper를 분석하고 구조화된 노트를 `analysis/<primary-topic>/<paper-id>/` 아래에 저장한다. 분석 결과는 **객관적 분석(core)** 과 **두 가지 해석 시선(academic / industry)** 으로 분리한다. `AGENTS.md`는 라우터 역할만 담당한다. 자세한 작성 규칙은 `skills/` 아래의 local skill에 있다.

## 출력물의 사용자

- **Academic lens**: 연구자가 후속 논문을 설계하거나, 본인 논문·제안서·학회 발표에서 인용하기 위해 본다. 저자 한계, 분석자 판단, 다음 논문 아이디어, citation 후보가 중심.
- **Industry lens**: 시니어 바이오인포매티션이 회사 파이프라인·신약개발·진단·BD 관점에서 본다. 규제(QA/RA), BD value, 자체 제품화 가능성, 활용 시나리오, 등급 평가가 중심.

두 lens는 한 paper에 동시에 적용되는 것이 기본이다. 사용자가 한 쪽만 명시하면 skip 가능.

## 언어
- 기본 출력 언어는 한국어로 작성한다.
- 분야에서 자연스러운 표준 scientific term은 English로 유지한다. 예: `RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `transcription`, `translation`, `single-cell`, `multi-omics`, `baseline`, `dataset`, `benchmark`, `BD`, `QA`, `RA`, `IND`, `IRB`.

## Hallucination 방지의 핵심 원칙

분석은 반드시 `analysis/<primary-topic>/<paper-id>/sources/` 아래의 원문 PDF와 supplementary data만을 근거로 한다. 본문에 없는 수치, 외부 지식, 추측은 사실처럼 쓰지 않는다. 외부 맥락이 필요하면 `외부 맥락:` 또는 `해석:`으로 명시 분리한다.

**원칙의 자세한 정의·예시·금지사항은 `skills/source-grounding/SKILL.md`에 한 곳에 모아둔다.** 다른 skill은 source grounding 원칙을 *따른다*고 짧게 참조만 하고 규칙을 반복하지 않는다.

## 출력 경로

모든 `analysis/...` 경로는 **프로젝트 루트** (예: `/Users/kkkim/projects/autobiox/BioProject01/`) 기준 상대 경로다. *논문 원문 binary*(PDF, xlsx, docx 등)는 `.gitignore`로 commit 차단되어 있고, 분석 노트(`*.md`, `paper-info.yaml`, `.url`, `.bib`)는 git tracked.

```
analysis/
├── <primary-topic>/
│   └── <paper-id>/                # 예: wang-2024-multivelo/
│       ├── paper-info.yaml        # 메타데이터·citation·카테고리·다운로드 링크 (single source of truth)
│       ├── core.md                # 객관적 분석 (개요·문제·방법·결과·Figure·Table)
│       ├── lens-academic.md       # 학계 시선 해석
│       ├── lens-industry.md       # 산업 시선 해석
│       ├── methodology-brief.md   # 재현·검토용 압축본
│       ├── figures/               # core-figure가 추출한 panel 이미지 (해당 시)
│       ├── slides/                # full-slides 결과 (해당 시)
│       └── sources/               # 원문 PDF + supplementary + paper.bib
│           ├── paper.pdf
│           ├── paper.bib
│           └── supp_*.{pdf,xlsx,csv,...}
└── _index/                        # 자동 생성 인덱스 (build_index.py)
    ├── papers.csv                 # 엑셀 등에서 정렬·필터용 통합 표
    ├── <topic>.md                 # topic별 markdown 목록 (다중 topic 지원)
    └── README.md                  # 인덱스 사용 가이드
```

### 폴더와 식별자 규칙

- `paper-info.yaml`이 *single source of truth*다. 메타데이터, citation key, BibTeX, 다운로드 링크, 카테고리(domain / use_case / importance), topics 배열이 모두 여기에 있다. 자세한 schema는 `skills/source-grounding/SKILL.md`에 정의.
- **paper-id 형식**: `<lastname>-<year>-<short-keyword>/`
  - 예: `wang-2024-multivelo/`, `gao-2024-multivelovae/`, `wang-2024-chromatin-rna-lag/`
  - keyword는 *저자가 명명한 method/tool 이름* 우선 (MultiVelo, MoFlow 등). 없으면 핵심 어구 1~2단어.
  - 같은 저자/연도/keyword 충돌 시 `-a`, `-b` suffix.
  - paper-id는 BibTeX의 citation.key와 *대응하지만 동일하지 않다*. citation.key는 yaml에 별도 저장 (예: 폴더 `wang-2024-multivelo`, citation.key `wang2024multivelo`).
- **paper-info.yaml 첫 줄에 human-readable header** (주석)를 둔다. 파일 열자마자 어떤 paper인지 즉시 인식.
  ```yaml
  # Wang et al., 2024 — MultiVelo — Nature Methods
  # DOI: 10.1038/s41592-024-xxxxx
  # Topics: epigenomic-lag, single-cell-genomics  |  Importance: 상
  ```

### Topic 다중 분류 규칙 (Option E)

- 폴더는 *primary topic*에만 존재한다 (paper 분석은 한 곳에만 저장).
- 추가 topic은 `paper-info.yaml`의 `topics` 배열에 명시한다 (primary는 첫 번째 항목).
- topic별 view는 `analysis/_index/<topic>.md`에서 본다 — *primary로 속한 것 + secondary로 속한 것 모두 포함*.
- `_index/` 디렉토리는 **자동 생성**된다. 사용자가 직접 편집하지 않는다.

### Topic 결정

- 사용자가 topic을 명시하면 그대로 사용한다.
- 사용자가 topic을 명시하지 않았지만 대화나 기존 묶음에서 명확히 추론 가능하면 그 topic을 사용한다.
- topic을 안전하게 추론할 수 없으면 분석 전에 짧게 물어본다.
- topic folder name은 사용자가 준 주제를 kebab-case로 정규화한다. 예: `epigenomic lag` → `epigenomic-lag`.

### Index 갱신

- paper-info.yaml이 새로 생성되거나 갱신될 때마다 `skills/source-grounding/scripts/build_index.py`로 `_index/`를 다시 빌드한다.
- 자세한 동작은 `skills/source-grounding/SKILL.md` 참고.

## Categorization (paper-info.yaml의 일부)

모든 paper는 다음 카테고리 메타데이터를 갖는다. 분석 과정에서 LLM이 자동으로 채우고 사용자가 검토·수정한다.

- **domain** (분야): abstract / title / venue 정보에서 LLM이 자동 추출. freeform vocabulary로 시작하고 자주 나오는 태그는 추후 누적.
- **use_case** (활용 시나리오): 아래 6개 vocabulary에서 1~3개. 새 vocabulary 추가는 허용하되 본인 확인을 받는다.
  - `academic-citation` — 본인 논문·제안서·학회 발표 reference
  - `methodology-reference` — 방법 차용·변형
  - `pipeline-applicable` — 우리 데이터·프로세스에 바로 적용
  - `BD-opportunity` — 외부 자산 라이선싱·공동연구·경쟁사 관찰
  - `commercialization-candidate` — 자체 제품화 (Dx / assay / SW / therapeutic)
  - `regulatory-precedent` — FDA / EMA / IRB 참고 사례
- **importance**: `level` (상 / 중 / 하) + `perspective` (어떤 관점에서 그 등급인지 한두 문장 사유).

domain은 abstract 분석 단계에서, use_case와 importance는 전체 분석 후 `lens-industry` 단계에서 채우는 것이 자연스럽다. 자세한 작성 규칙은 `skills/lens-industry/SKILL.md` 참고.

## Skill Routing

| Task | Skill |
| --- | --- |
| 원문/supplementary 다운로드, paper-info.yaml 작성, 외부 정보 차단 규칙 | `skills/source-grounding/SKILL.md` |
| Abstract만 빠르게 훑는 경량 분석 | `skills/abstract-analysis/SKILL.md` |
| `core.md` 문제 정의 & 연구 목적 | `skills/core-problem/SKILL.md` |
| `core.md` 방법론 분석 | `skills/core-methods/SKILL.md` |
| `core.md` 주요 결과 (통계 유의성·재현성 강조) | `skills/core-results/SKILL.md` |
| `core.md` Figure 분석 | `skills/core-figure/SKILL.md` |
| `core.md` Table 분석 | `skills/core-table/SKILL.md` |
| `lens-academic.md` 학계 시선 (저자 한계 + 분석자 판단 + 후속 연구 + citation 후보) | `skills/lens-academic/SKILL.md` |
| `lens-industry.md` 산업 시선 (QA/RA 리스크 + BD value + 제품화 + 전문가 코멘트 + 카테고리화) | `skills/lens-industry/SKILL.md` |
| `methodology-brief.md` 재현·검토용 압축본 | `skills/methodology-brief/SKILL.md` |
| 기존 `core.md` 기반 정적 slide deck 생성 | `skills/full-slides/SKILL.md` |
| 분석된 paper에 대한 질문 | `skills/question/SKILL.md` |

## Full Paper Workflow

PDF가 주어졌을 때 다음 순서로 진행한다.

1. **Topic 결정**: 사용자 명시 → 추론 → 모호하면 질문.
2. **Source 준비** (`skills/source-grounding/SKILL.md`):
   - `analysis/<primary-topic>/<paper-id>/sources/`에 PDF와 가능한 모든 supplementary를 모은다.
   - `paper-info.yaml` 스켈레톤 생성 (메타데이터 + citation + 다운로드 링크).
   - `sources/paper.bib` 생성.
   - 외부 지식 사용 금지 규칙을 분석 세션 동안 유지한다.
3. **Metadata 및 domain 추출**: title, authors, year, venue, field, keywords를 `paper-info.yaml`과 `core.md` 첫 부분에 정리. abstract 기반으로 domain 태그도 LLM이 추출하여 `paper-info.yaml`에 기록.
4. **`core.md` 작성** — 객관적 분석. 다음 순서로 skill 호출:
   - 문제 정의: `core-problem`
   - 방법론: `core-methods` (adaptive depth — 자료 유형별 깊이 자동 조정)
   - 주요 결과: `core-results`
   - Figure 분석: `core-figure`
   - Table 분석: `core-table`
5. **`lens-academic.md` 작성** (`lens-academic`): 저자 한계 / 분석자 판단 / 매끄럽지 않은 지점 / 다음 논문 아이디어 / 본인 논문에서 인용할 후보 문장·수치. *학술적* 한계만 다룬다 (산업·규제·임상은 lens-industry로).
6. **`lens-industry.md` 작성** (`lens-industry`): 산업·규제·임상 리스크 / BD value & 상용화 가능성 / 전문가 코멘트(등급·활용 우선순위). 이 단계에서 `paper-info.yaml`의 `use_case`와 `importance`도 채운다.
7. **`methodology-brief.md` 작성** (`methodology-brief`): 재현·검토용 압축본. 우리 데이터에 적용/재현 가능한지 빠르게 판단하기 위한 메모.
8. **Executive Summary (core.md 맨 앞 1단락 추가)** — 위 모든 단계가 끝난 *후* LLM이 core.md 맨 앞에 1단락(3~5문장)을 추가한다. 본인이 분석 노트를 다시 펴봤을 때 1초 안에 paper 그림을 파악하기 위함. 한계는 lens-* 참고하도록 짧게 언급, 본문 분석을 *압축한 진입점*. 형식:
   ```markdown
   ## Executive Summary
   [3~5문장: 무엇을 풀고자 하는 자료인지 + 핵심 방법 한 줄 + 가장 중요한 결과 한 줄 + 어디 쓸 수 있는지 한 줄 + 자세한 한계는 lens-* 참고]
   ```
   이 단락은 별도 skill로 빼지 않고 *분석 마무리 단계*에서 LLM이 직접 작성한다 (core-* 출력을 모아 압축).

각 단계의 출력은 위 출력 경로의 해당 파일에 누적해 저장한다. 한 skill이 다른 skill의 출력을 참조할 수 있다 (예: `lens-industry`는 `core-results`의 수치를 인용).

## Abstract-only Workflow

사용자가 *초록만* 가지고 있거나 *빠른 스크리닝*만 요청하면:

1. `skills/source-grounding/SKILL.md`로 `paper-info.yaml` 스켈레톤만 생성 (PDF가 없어도 abstract 출처와 메타데이터는 기록).
2. `skills/abstract-analysis/SKILL.md`로 `analysis/<primary-topic>/<paper-id>/abstract.md`를 작성.
3. Abstract에 없는 정보는 추측 금지.
4. 나중에 full paper 분석을 진행하면 `abstract.md`는 그대로 보존하고 `core.md`를 별도로 생성한다. 둘은 공존한다.

## Slide Workflow

사용자가 slides, slide deck, presentation 생성을 명시적으로 요청했을 때만 다음 순서를 따른다.

1. `skills/full-slides/SKILL.md`를 사용한다.
2. 먼저 `analysis/<primary-topic>/<paper-id>/core.md`가 존재해야 한다. 없으면 slide를 만들지 말고 full paper 분석이 먼저 필요하다고 말한다.
3. `design.md`를 필수 visual design reference로 사용한다.
4. source PDF에서 관련 Figure image를 캡처해 `slides/assets/figures/`에 저장한다.
5. 각 Figure image는 slide 절반 이하 크기로 유지한다. 큰 multi-panel Figure는 여러 slide로 나눈다.
6. 출력은 `analysis/<primary-topic>/<paper-id>/slides/` 아래 OpenClaw Slides 기반 browser-previewable journal-meeting deck.
7. 사용자가 video export를 명시적으로 요청하지 않는 한 video는 render하지 않는다.
8. 일반 paper analysis 중에는 slides를 자동 생성하지 않는다.

## Question Workflow

사용자가 이미 분석된 paper에 대해 질문하면 다음 순서를 따른다.

1. `skills/question/SKILL.md`를 사용한다.
2. 답변 우선순위:
   - 해당 paper의 `core.md`에 답이 있으면 그 파일만 근거로 답한다.
   - 그래도 부족하면 같은 paper의 `lens-academic.md`, `lens-industry.md`, `methodology-brief.md`, `paper-info.yaml`을 참고한다.
   - 다른 분석된 자료에서 답을 찾으면 `<paper-id>에 따르면...` 형식으로 출처를 명시한다. citation이 필요하면 `paper-info.yaml`의 `citation.key`를 사용 (예: `@wang2024multivelo`).
   - 어떤 분석 파일에도 답이 없으면 그 사실을 말하고 추측하지 않는다.
3. 원문 PDF/외부 지식을 우선 근거로 삼지 않는다. 필요한 경우 먼저 `core.md`를 업데이트한 뒤 다시 답한다.

## Lens 선택 규칙 (요약)

- 기본: `paper-info.yaml` + `core.md` + `lens-academic.md` + `lens-industry.md` + `methodology-brief.md` 모두 작성.
- 사용자가 "academic만" 또는 "industry만"이라고 명시 → 명시된 lens 파일만 작성. 다른 lens는 생성하지 않는다. 단 `paper-info.yaml`의 `use_case`·`importance`는 industry skip 시에도 LLM이 가능한 범위에서 추출하고 *추정 표시* 후 기록한다 (나중에 필요할 때 본인 확인).
- 사용자가 "core만"이라고 명시 → lens 파일은 생성하지 않는다.
- 어떤 경우에도 `paper-info.yaml`, `core.md`, `sources/`는 필수이다.
