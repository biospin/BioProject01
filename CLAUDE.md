# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 이 repo는 무엇인가

두 개의 layer가 공존한다:

1. **Paper analysis workspace (현재 활성)** — scientific paper / preprint / industry report / regulatory 문서 등을 dual-lens 구조(`core` + `lens-academic` + `lens-industry` + `methodology-brief`)로 분석해서 `analysis/<topic>/<paper-id>/` 아래에 누적한다. 이 layer의 운영 규칙은 **[AGENTS.md](AGENTS.md)** 가 router로 모두 정의한다. CLAUDE.md는 그것을 중복하지 않는다.
2. **연구 프로젝트 컨텍스트 (계획)** — Epigenetic Therapy 기반 Response Time 예측. 코드 파이프라인은 아직 없고, 관련 paper들을 layer 1에서 수집/해석하는 단계.

## Paper analysis 작업 시 — AGENTS.md 먼저 읽기

`AGENTS.md`가 단일 진입점이다. 거기에 정의된 것:
- Quick Start (DOI / PDF / URL 한 줄로 분석 시작)
- Dual-lens 출력 구조: `core` (객관적) + `lens-academic` (학계 시선) + `lens-industry` (산업 시선) + `methodology-brief` (재현용 압축본)
- `paper-info.yaml` = single source of truth
- `paper-id` naming: `<lastname>-<year>-<short-keyword>` (예: `li-2023-multivelo`)
- `core.md` section 고정 순서 (Executive Summary → Identity → Background → Methods → Results → Figures → Tables → Supplementary Information → 분석 메모)
- Skill routing 테이블 — 작업별로 어떤 `skills/<name>/SKILL.md`를 호출하는지
- Slide 워크플로우는 명시 요청 시에만 (`design.md`를 visual reference로 사용)

## 실제 호출 가능한 스크립트

전부 `python3` 실행. 의존성은 `skills/source-grounding/scripts/requirements.txt`.

```bash
# Paper source 자동 fetch (PDF / .bib / .url)
python3 skills/source-grounding/scripts/fetch_sources.py <args>

# analysis/_index/{papers.csv, <topic>.md} 자동 빌드
python3 skills/source-grounding/scripts/build_index.py

# core.md → figure-embedded HTML report
python3 skills/core-to-html/scripts/build_html.py <paper-dir>

# PDF figure를 panel별 PNG로 자동/수동 crop
python3 skills/core-figure/scripts/extract_panels.py <pdf> --page N --figure "Figure 2" \
  --figure-bbox x0,y0,x1,y1 --out analysis/<topic>/<paper-id>/figures

# (외부 공유용) paper 분석 폴더 압축/공유
python3 skills/source-grounding/scripts/share_paper.py <paper-dir>
```

`paper-info.yaml`이 갱신될 때마다 `build_index.py`를 다시 돌려 `_index/`를 일치시킨다.

## 언어 규칙

- 출력 기본은 한국어.
- 분야 표준 영어 용어는 그대로 유지: `RNA`, `DNA`, `TF`, `chromatin`, `transcription`, `single-cell`, `multi-omics`, `baseline`, `dataset`, `benchmark`, `BD`, `QA`, `RA`, `IND`, `IRB`, `Figure`, `panel` 등.
- 영어 용어 첫 사용 시 한국어 보충은 1회만.

## Hallucination 방지

분석은 `analysis/<topic>/<paper-id>/sources/`의 원문 PDF + supplementary만 근거로 한다. 외부 지식이 필요하면 `외부 맥락:` 또는 `해석:`으로 명시 분리. 세부 규칙은 `skills/source-grounding/SKILL.md` 한 곳에만 모여 있다 — 다른 skill은 이를 참조만 한다.

## Branch 컨벤션

팀 컨벤션은 **`<사람>-<workstream>`**. 본인 영역 안에서 workstream별로 branch를 따로 둔다.

| Branch | 용도 |
|---|---|
| `kkkim-paper-agent` | **본인 paper analysis 작업 — 현재 활성 branch.** 새 paper 분석 추가는 여기서. |
| `kkkim-<workstream>` | 다른 workstream 시작 시 새로 분기 (예: `kkkim-pipeline` = 코드, `kkkim-data` = dataset 전처리). 시작 시점에 만들면 됨. |
| `epigenomics`, `braveji-paper-agent`, `main` | **건드리지 않는다.** 다른 협업자 영역. |

**분기 base 결정:**
- paper analysis framework를 그대로 깔고 코드 작성 → `kkkim-paper-agent`에서 분기
- paper analysis와 독립 작업 → `main`에서 분기

**Paper agent skill에 영향을 주는 변경(`AGENTS.md`, `skills/*`, `design.md`)** 은 반드시 `kkkim-paper-agent`에서 한다. 다른 workstream branch에서 skill 자체를 수정하지 않는다.

## Git / commit 규칙

- 원문 binary(PDF, xlsx, docx, pptx 등)는 `.gitignore`로 commit 차단. tracked 대상은 `*.md`, `paper-info.yaml`, `*.url`, `*.bib`, `*.json` (figure-map, manifest 등).
- Author: `kakyungkim <kakyung.kim@gmail.com>` (이 PC의 SSH key가 등록된 GitHub 계정).
- Commit message에 Claude attribution(`Co-Authored-By: Claude`, `🤖 Generated with Claude Code` 등)은 추가하지 않는다.
- Remote는 SSH (`git@github.com:biospin/BioProject01.git`). HTTPS+password는 작동하지 않는다.

## 외부 협업 도구

- **Confluence**: Space `VC`, 경로: 프로젝트 진행-AI전용 > 프로젝트#01
- **JIRA**: Space `BIOP01`
- **Slack**: 멤버별 openclaw bot

## 팀 & 데이터셋 담당

| 담당 데이터셋 | 담당자 | GitHub ID |
|---|---|---|
| 10x embryonic mouse brain | 서정한 | JeonghanSeo |
| SHARE-seq mouse skin | 지용기 | braveji18 |
| Human brain multi-ome | 박세진 / 지용기 | sjpark / braveji18 |
| Human HSPC 10x Multiome | kkkim / jamie (jmryu) | kakyungkim / JamieLyu |
| 하네스 | braveji (ykji) | braveji18 |

## 주요 데이터셋

| Dataset | Accession | Data type |
|---|---|---|
| 10x embryonic mouse brain | 10x Genomics dataset page | 10x multiome |
| SHARE-seq mouse skin | GSE140203 | paired chromatin + RNA |
| Human brain multi-ome | GSE162170 | human multiome |
| Human HSPC 10x Multiome | GSE209878 | human multiome |

## 연구 프로젝트 핵심 개념 (paper 선정·해석에 활용)

목표: gene별 chromatin-transcription lag structure를 정량화 → baseline epigenomic feature로 epigenetic drug response timing을 예측.

- `activation lag`: chromatin이 열린 뒤 transcription이 시작될 때까지의 시간.
- `shutdown lag`: transcription이 꺼진 뒤 chromatin이 닫힐 때까지의 시간.

관련 도구 (분석 대상 paper들이 쓰는 것): MultiVelo, MultiVeloVAE, MoFlow, `scanpy`, `anndata`, `muon`, `snapatac2`, `ArchR`. (이 repo의 stack은 아님 — 이건 paper들이 쓰는 라이브러리.)

## 방법론적 주의사항 (paper 해석 시 반복 등장)

1. **Pseudotime ≠ Wall-clock time**: lag estimate는 pseudotime 단위. 실제 시간 단위 검증은 별도 입증 필요.
2. **Confound 통제**: burst kinetics (mean expression + variance scaling), cell cycle phase를 covariate로 통제하지 않으면 lag estimate가 artifact일 수 있음.
3. **Multicollinearity**: promoter ATAC, enhancer ATAC, H3K27ac, H3K4me3, TF motif score는 강한 상관 → group lasso 등 regularized model 필요.
4. **ChIP-seq mismatch**: bulk ChIP (예: GSE70677)을 baseline feature로 쓸 때 cell type 해상도 손실 주의. multiome ATAC peak을 primary로.
5. **Multiple testing**: gene 단위 가설 (수만 개) → BH correction 또는 permutation 기반 FDR.

## 리소스 요구사항

- RAM 128GB, 저장 1–2TB (dataset당 raw + intermediate 200–500GB), GPU 1대 이상 (MultiVeloVAE 재현용 — 필수).
