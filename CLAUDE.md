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
- `env/` — 프레임워크별 격리 conda env 4종(`scv-preprocess`/`mv`/`torch`/`tf`) + `setup_envs.sh`, `README.md`.
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
