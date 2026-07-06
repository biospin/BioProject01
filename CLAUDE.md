# CLAUDE.md — kkkim-pipeline (HSPC 연구: 논문 근거 + 파이프라인)

> 이 브랜치(`kkkim-pipeline`)는 HSPC 연구의 **단일 작업 브랜치**다. 두 폴더로 분리한다:
> - **`paper_analysis/`** — paper 분석 *산출물* 14편 (어떤 method·confound를 쓸지의 근거). 분석 *하네스* 자체는 여기 없다 — 외부 재사용 repo `kakyungkim/paper-analysis-harness`에 있다.
> - **`pipeline/`** — 그 근거로 실제 데이터를 돌리는 코드.
>
> paper-agent 브랜치는 archive(보존만)했고, 새 paper 분석은 외부 하네스로 돌려 산출물만 `paper_analysis/`에 반입한다.

## 무엇을 하는가
목표: gene별 **chromatin→transcription lag**(activation/shutdown) 정량 → baseline epigenomic feature로 epigenetic drug response timing 예측. 1차 데이터셋 = **Human HSPC 10x Multiome (GSE209878)**.

## paper_analysis/ (근거 레이어)
- 14편 dual-lens 분석(`core`+`lens-academic`+`lens-industry`+`methodology-brief`) + `_index/`. 파이프라인 method 선택(DESIGN.md)의 근거.
- 분석 하네스(`AGENTS.md`/skills/web)는 외부 `kakyungkim/paper-analysis-harness`. 새 분석은 거기서 돌리고 산출 폴더만 `paper_analysis/<topic>/<paper-id>/`로 복사.

## 하네스 (OpenClaw 기반, Claude Code 호환)
- **이 분석 하네스(`AGENTS.md` + `skills/`)는 박상준(@poqopo) `Harness_Baseline`에서 반입**해 우리 파이프라인에 맞춘 것. 원저작자 박상준 (원 repo LICENSE 미지정 — 공유·수정은 동의 전제).
- 포맷: `AGENTS.md`(project frame) + `skills/ROUTES.md`(dataset→task 라우팅) + `skills/<dataset>/<task>/SKILL.md` + `agents/openai.yaml`. **이건 OpenClaw/Codex 네이티브 포맷**이라 OpenClaw로 바로 실행 가능하고, Claude Code에서도 동작한다.
- **OpenClaw 연습 중**: 앞으로 분석을 OpenClaw 기반으로 돌리는 것을 기본 감안한다. skill/agent 포맷(`openai.yaml`)을 유지한다.
- dataset 4종 × task 4단계(`download→preprocessing→model→visualization`). 우리는 **`human-hspc-10x-multiome`** 가 active.

## 실행 구현 — `pipeline/hspc-velocity-benchmark/`
SKILL(지침)을 실제로 돌리는 코드:
- `scripts/download_data.sh` — GSE209878 다운로드 (MV-1=day0, MV-2=day7). `download_manifest.tsv`(sha256), `P0_provenance.md`.
- `scripts/p1_build.py` — 통일 전처리(공통 branch). `P1_README.md`, `scripts/check_data.py`.
- `DESIGN.md` — velocity method head-to-head 벤치마크 = model 단계 method-selection. `REVIEW-methodologist-2026-06-13.md`.
- `env/` — 프레임워크별 격리 conda env(`scv-preprocess`/`velo-mv`/`velo-torch`/`velo-tf`/`celldancer`) + 유틸 `seqtools`(STAR·sra-tools·velocyto) + `setup_envs.sh`, `README.md`. (2026-07-11 명명: velocity env는 `velo-*` 접두. velocity 5종 전부 팀공유 `/opt/envs`, 개인 `~/miniconda3/envs`엔 scv-preprocess만(협업서버) — `conda run -n <env>`로 해소. /opt 공유 마운트 여부는 팀원 확인 필요.)
- `dataset/` — GSE209878 dataset card.
- `BASELINE-ALIGNMENT.md` — Harness_Baseline 정합 기록.

## 작업 기록
- **`SESSION-LOG.md`**: 분석 단계에서 한 일을 세션별로 누적 기록.
- **`HANDOFF.md`**: 현재 상태 + 한 일/할 일. **`TODO.md`**: 할 일 체크리스트.

## Branch 모델 (중요)
- `kkkim-pipeline` = **HSPC 연구 단일 작업 브랜치.** `paper_analysis/`(근거) + `pipeline/`(코드)를 한 브랜치에서 관리.
- `kkkim-paper-agent` = **archive(보존만).** paper 하네스의 마지막 상태 보존용. 새 작업은 여기서 하지 않는다.
- paper 분석 *하네스*는 외부 `kakyungkim/paper-analysis-harness`. 하네스 자체 개선은 거기서 한다.
- `epigenomics`, `braveji-*`, `main` 등 다른 협업자 영역은 안 건드린다.

## 언어 / commit 규칙
- 출력 기본 한국어. 분야 표준 영어 용어 유지(RNA/DNA/ATAC/chromatin/pseudotime/baseline 등).
- Author: `kakyungkim <kakyung.kim@gmail.com>`. Claude attribution(footer/co-author) **금지**. Remote SSH `git@github.com:biospin/BioProject01.git`.
- **커밋 메시지 표기(중요)**: 파이프라인 단계 커밋은 **내부 단계표기 `P0`~`P5`** 를 접두로 쓴다 (예: `P4 permutation FDR 4-way …`, `P5 bootstrap stability …`). `BIOP01-NN`(JIRA 키)은 **그 커밋이 실제로 해당 JIRA 이슈에 대응할 때만** 쓰고, 내부 단계 라벨 용도로는 쓰지 않는다 — 실제 JIRA 키와 충돌하기 때문(BIOP01-24=mouse brain 담당, BIOP01-25~28=BIOP01-23 child task). 과거 `BIOP01-24~28`로 표기된 확증 커밋은 실제로는 내부 P4/P5 작업이었음(추적 시 주의).
- 원문 binary·대용량(.h5ad/.h5mu/.loom/PDF/data)은 `.gitignore`. tracked = `*.md`, `*.yaml`, `*.tsv`(요약), 코드.

## 방법론 주의 (분석 시 반복)
1. **Pseudotime ≠ wall-clock**: lag은 pseudotime 단위로 보고. (GSE209878 day0/day7은 batch 통합돼 wall-clock anchor로 직접 못 씀.)
2. **Confound**: cell cycle·burst·ambient/doublet 통제. lineage별(within-lineage) 계산, rare lineage(MK/platelet) uncertainty 별도.
3. **Multicollinearity**: promoter/enhancer ATAC 등 강상관 → regularized.
4. **Multiple testing**: gene 단위 → permutation FDR.
5. method 차이 ≠ preprocessing 차이: 공통 전처리 후 method 분기(C2), 공통 graph ablation.

---

## Agent routing & artifact contract (논문 생산 하네스)

> 논문 집필·발표 단계용. 재사용 스캐폴드(Designed by Ka-Kyung Kim, CC BY 4.0) 설치본. 전체 랩 지도·멤버 JD = **`docs/HARNESS.md`**. 도메인 분석 슬롯 = **`hspc-velocity-analyst`**(팀이 채운 유일한 슬롯). 이 브랜치(`kkkim-pipeline`)에 project-scope로 설치.

### 자연어 라우팅
요청에 agent 이름이 없어도 아래 표로 배정한다. 프로젝트 agent는 `.claude/agents/`. 그림 작업은 `manuscript-writer`가 `pipeline/hspc-velocity-benchmark/figures/figNN_*.py`를 실행해 소유.

**논문 하네스 단일 컨텍스트 = `pipeline/hspc-velocity-benchmark/manuscript/PAPER_DIRECTION.md`.** 모든 논문 멤버(novelty·literature·methodologist·writer·critic·reviewer)는 작업 전 이 문서를 읽는다 — 현재 thesis·claim 등급표·loop 규율(**claim-defensibility 게이트**: headline claim은 반증기준+make-or-break 검정+advisor 통과 전 PROVISIONAL, 본문 미반영)·사전등록·진행상태가 여기 있다. 매번 재브리핑 불필요.

**여러 단계를 엮는 요청 → 단일 agent가 아니라 오케스트레이터 Skill.** "풀 파이프라인 / 프리프린트 업데이트해 제출 준비 / 분석→집필→그림→검수까지 / 그림만 다시 / 리뷰만 다시 / critic 지적 반영"은 **`paper-production-orchestrator`** Skill(`.claude/skills/paper-production-orchestrator/SKILL.md`)로 — 메인 루프가 실행하며 §0에서 PAPER_DIRECTION 로드 후 아래 멤버를 순서대로 호출하고 claim-defensibility 게이트·부분 재실행·검증 게이트를 처리한다. 단일 단계 요청은 아래 agent로 직접 라우팅:

| 요청 (자연어) | 첫 agent |
| --- | --- |
| "분석 돌려줘 / 재실행 / eval·통계 / 오류 분석 / cross-dataset 재현" | `hspc-velocity-analyst` |
| "프리프린트/저널/블로그 초안·섹션 써줘" | `manuscript-writer` |
| "그림 만들어줘 / 그림 번호 정리" | `manuscript-writer` (runs `figures/figNN_*.py`) |
| "선행연구 / related work / 스쿱 확인" | `literature-scout` |
| "차별화 각도 / 뭘 새로 해야 하나" | `novelty-strategist` |
| "가설·실험설계·분석계획 점검·감사" | `research-methodologist` |
| "제출 전 적대적 자체검토 / 그림 QA" | `paper-critic` |
| "정식 venue 리뷰 시뮬레이션" | `reviewer` (전역, 선택) |
| "발표자료/슬라이드/발제" | `presenter` |
| "로고·아이콘·브랜드·그림 미감" | `design` |
| "여러 단계를 어떤 순서로 엮을지 계획만" | `paper-orchestrator` (계획만; 실행은 메인 루프) |

### 산출물 계약
멤버는 중간 결과를 대화에만 남기지 않고 파일로 넘긴다:

| 단계 | Writer | 산출물 | 다음이 읽음 |
| --- | --- | --- | --- |
| 분석·eval | `hspc-velocity-analyst` | `pipeline/hspc-velocity-benchmark/results/FINDINGS.md` + `results/*.csv` + `results/*.md` | 집필·검수 |
| 집필+그림 | manuscript-writer (그림=`figures/figNN_*.py`) | `pipeline/hspc-velocity-benchmark/manuscript/draft.md`, `figures/*.png` | 검수·리뷰·발표 |
| 검증 게이트 | (커밋/공개 전) | `p3_concordance.py` + `p3_crossdataset_concordance.py` + `p3_scrambled_null.py` 재계산 → FINDINGS.md 대조 | 사람 |
| 리뷰 | paper-critic / reviewer | `manuscript/REVIEW-<venue>-<date>.md` | 집필(수정) |
| 발표 | presenter | 슬라이드/발제 | 사람 |
| 상태 핸드오프 | (전원) | `HANDOFF.md`, `TODO.md`, `SESSION-LOG.md` | 다음 세션 |

**사람 승인 게이트:** 공개(프리프린트/blog)는 **저자·소속·IP·corresponding email 확정** 전까지 보류(manuscript-writer의 `<FILL>`). **커밋·push는 작업 완료 시 에이전트가 자동 수행**(2026-07-09 정책 변경 — 기존 '무인 git 금지' 철회, push까지 자동). 단 위 검증 게이트(커밋 전 재계산·FINDINGS 대조)는 유지하고, **프리프린트/blog 외부 공개와 main 병합만 사람 승인**(작업 브랜치 `kkkim-pipeline` push는 자동). 커밋 메시지는 P0~P5 접두 규칙 준수, Claude attribution 금지.

## 글쓰기 규율 (팀 공통, 한국어 산출물)
@.claude/rules/writing-style.md
