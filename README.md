# BioProject01 — Epigenetic Therapy 기반 Response Time 예측

연구 주제는 *chromatin accessibility 변화를 매개로 한 약물 반응 시간 (response time) 예측* (제안: 박상준). 현 시점에서 본 repo는 **연구의 paper analysis layer만 구축**된 상태 — 관련 scientific paper를 dual-lens 구조로 분석·누적해 baseline evidence를 마련한다. 실제 chromatin-RNA lag prediction / drug response 분석 코드는 아직 작성 전.

자세한 연구 proposal과 review 의견: [`presentation/[주제] Epigenetic Therapy 기반 Response Time 예측.pdf`](presentation/).

## 현재 동작하는 것 — Paper Analysis Workspace

각 paper는 `analysis/<topic>/<paper-id>/` 아래에 `paper-info.yaml` + 4종 markdown으로 정리된다:

| 파일 | 역할 |
|---|---|
| `<paper-id>_core.md` | 객관적 분석 (9 fixed sections: Executive Summary → Identity → Background → Methods → Results → Figures → Tables → Supplementary → 분석 메모) |
| `<paper-id>_lens-academic.md` | 학계 시선 (저자 한계, 분석자 판단, 후속 연구, citation 후보) |
| `<paper-id>_lens-industry.md` | 산업 시선 (QA/RA 리스크, BD value, 상용화 가능성) |
| `<paper-id>_methodology-brief.md` | 재현·검토용 압축본 |

추가로 (local-only, `.gitignore`):
- `sources/` — 원문 PDF + supplementary
- `figures/` — `core-to-html`이 PDF에서 추출한 panel PNG (smart bbox crop)
- `<paper-id>_core.html` — figure-embedded HTML 보고서 (MathJax 수식 렌더)

## 분석된 paper (2026-05-26 기준)

| paper-id | citation | importance | 핵심 |
|---|---|---|---|
| `li-2023-multivelo` | `@li2023multivelo` (Nat Biotechnol 2023) | 상 | MultiVelo — chromatin–RNA ODE multi-omic velocity의 foundational baseline. M1/M2 모델 정의. |
| `li-2025-multivelovae` | `@li2025multivelovae` (Nat Commun 2025) | 상 | MultiVeloVAE — MultiVelo discrete state를 cVAE + continuous (δ, κ) + Bayesian differential test로 일반화. |
| `hong-2026-moflow` | `@hong2026moflow` (Nat Commun 2025/26) | 상 | MoFlow — cellDancer relay velocity에 chromatin opening/closing dual hypothesis + lower-loss selection 추가. *latent time-free*. |
| `li-2023-celldancer` | `@li2023celldancer` (Nat Biotechnol 2023) | 중 | cellDancer — local relay velocity cosine loss + cell-specific kinetic rate. MoFlow의 직접 predecessor. |
| `cui-2024-deepvelo` | `@cui2024deepvelo` (Genome Biol 2024) | 중 | DeepVelo — GCN + continuity loss + cell/gene-specific kinetic rate. RNA-only foundational baseline. |
| `mizukoshi-2024-deepkinet` | `@mizukoshi2024deepkinet` (Genome Biol 2024) | 중 | DeepKINET — 2-stage VAE + scEU-seq/scNT-seq metabolic labeling validation reference. |
| `nomura-2024-mmvelo` | `@nomura2024mmvelo` (bioRxiv preprint 2024) | 상 | mmVelo — mixture-of-experts VAE + *peak-level* chromatin velocity (decoder-resolution). |

최신 목록·요약·진행 상태: `analysis/_index/papers.csv` (자동 생성). Topic별 view는 `analysis/_index/<topic>.md`.

Cross-paper synthesis (Week2): `analysis/epigenomic-lag/_evidence/week2/{insight,validation_report,comparison_table,handoff}.md`.

## Repo 구조

```
.
├── AGENTS.md                       # Paper analysis 시스템의 router (단일 진입점)
├── CLAUDE.md                       # Claude Code 운영 규칙 (branch / commit / 언어 / 스크립트)
├── README.md                       # 본 파일
├── design.md                       # Slide deck 작성 시 visual reference
├── presentation/                   # 연구 proposal PDF, 발표 자료
├── analysis/
│   ├── _index/                     # build_index.py가 생성하는 topic 인덱스
│   ├── <topic>/<paper-id>/         # paper-info.yaml + 4종 md + sources/ + figures/
│   └── <topic>/_evidence/<week>/   # cross-paper insight / validation / handoff
└── skills/                         # paper analysis skill 정의 (SKILL.md 포맷)
    ├── source-grounding/           # 원문 fetch + hallucination 방지 master rule + yaml schema
    ├── core-*/                     # core.md 작성 (problem / methods / results / figure / table)
    ├── lens-academic/              # 학계 시선
    ├── lens-industry/              # 산업 시선
    ├── methodology-brief/          # 재현 압축본
    ├── core-to-html/               # core.md → figure-embedded HTML + MathJax
    ├── abstract-analysis/          # 빠른 스크리닝
    ├── full-slides/                # journal-meeting slide deck 생성
    └── question/                   # 분석된 paper에 대한 질문 응답
```

## 사용법

### 새 paper 분석 추가

자세한 워크플로우는 `AGENTS.md` Quick Start. 가장 단순한 패턴 (Claude Code 또는 Codex CLI에서):

```
DOI: 10.1038/s41587-022-01476-y 분석해줘
```

PDF 또는 URL을 한 줄로 주면 → 폴더 생성 + `paper-info.yaml` seed + source 자동 다운로드 (`fetch_sources.py --discover-supp`로 Nature/Springer supplementary 자동 발견) + 4종 markdown + HTML report 자동 생성.

### 호출 가능한 스크립트

전부 `python3` 실행. 의존성: `pip install -r skills/source-grounding/scripts/requirements.txt`.

```bash
# Paper source 자동 fetch
python3 skills/source-grounding/scripts/fetch_sources.py <paper-info.yaml> --discover-supp --use-pmc --fetch-abstract

# analysis/_index/ 빌드
python3 skills/source-grounding/scripts/build_index.py

# core.md → HTML (smart figure crop + MathJax + 표 추출 캐싱)
python3 skills/core-to-html/scripts/build_html.py <paper-dir>

# PDF figure → panel별 PNG crop
python3 skills/core-figure/scripts/extract_panels.py <pdf> --page N --figure "Figure 2" \
  --figure-bbox x0,y0,x1,y1 --out <paper-dir>/figures
```

## 작성 규칙 (핵심)

- **언어**: 한국어 기본. 분야 표준 영어 용어(`RNA`, `chromatin`, `velocity`, `dataset` 등)는 그대로 유지.
- **수식**: LaTeX `$...$` (inline) / `$$...$$` (display). backtick code span에 수식 넣지 않음 (MathJax 렌더 안 됨).
- **Hallucination 방지**: 모든 사실은 `sources/` 원문 PDF + supplementary에 grounding. 외부 지식은 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 접두사로 분리. 세부 규칙은 `skills/source-grounding/SKILL.md` Part 1.
- **Executive Summary**: 1-paragraph prose 대신 5-bullet bold-labeled (무엇 / 모델 / 핵심 결과 / 우리 적용 / 심층). `AGENTS.md` 표기 규칙 참고.
- **Branch 컨벤션** (`<사람>-<workstream>`): 본인 작업 branch는 `<이름>-paper-agent`. `main`, `epigenomics`, 다른 사람 branch는 건드리지 않음.

## 호환 도구

본 시스템은 **Claude Code**와 **OpenAI Codex CLI** 양쪽에서 동작.
- `AGENTS.md` = Codex CLI native config / Claude Code도 보조로 읽음
- `CLAUDE.md` = Claude Code 전용 (Codex는 무시)
- `skills/<name>/SKILL.md` = 양 도구 공통 skill 포맷
- Python 스크립트는 도구 무관 (사람이 직접 호출해도 동일)

## 팀 & 데이터셋 담당

| Dataset | Primary | Secondary | GitHub ID |
|---|---|---|---|
| 10x embryonic mouse brain | 이건규 | — | Geongyu |
| SHARE-seq mouse skin | 박상준 | — | — |
| Human brain multi-ome | 전연수 | 박세진 | sezinie000 / sjpark |
| Human HSPC 10x Multiome | 김가경 | 류재면 | kakyungkim / JamieLyu |
| 하네스 | 지용기 | — | braveji18 |

## 외부 협업 도구

- **Confluence**: Space `VC`, 경로 `프로젝트 진행-AI전용 > 프로젝트#01`.
- **JIRA**: Space `BIOP01`.
- **Slack**: 멤버별 openclaw bot.
- **Atlassian MCP 설정**: [`openclaw/atlassian-mcp-setup.md`](openclaw/atlassian-mcp-setup.md).
