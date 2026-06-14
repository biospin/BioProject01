# CLAUDE.md — kkkim-pipeline (실제 데이터 파이프라인 레이어)

> 이 브랜치(`kkkim-pipeline`)는 **실제 데이터 파이프라인을 돌려 분석**하는 레이어다. paper 분석 레이어(`kkkim-paper-agent`)와 **분리**한다. paper 분석의 *결론*(어떤 method·confound를 쓸지)은 이 파이프라인의 *개념적 입력*이며, paper 분석 산출물·하네스는 여기 두지 않는다.

## 무엇을 하는가
목표: gene별 **chromatin→transcription lag**(activation/shutdown) 정량 → baseline epigenomic feature로 epigenetic drug response timing 예측. 1차 데이터셋 = **Human HSPC 10x Multiome (GSE209878)**.

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
- `kkkim-pipeline` = **독립 파이프라인 브랜치.** paper-agent에서 **merge 받지 않는다** (paper 산출물을 끌어오지 않음).
- paper 분석/하네스 = `kkkim-paper-agent`. 거기 것을 여기서 수정하지 않는다.
- `epigenomics`, `braveji-*`, `main` 등 다른 협업자 영역은 안 건드린다.

## 언어 / commit 규칙
- 출력 기본 한국어. 분야 표준 영어 용어 유지(RNA/DNA/ATAC/chromatin/pseudotime/baseline 등).
- Author: `kakyungkim <kakyung.kim@gmail.com>`. Claude attribution(footer/co-author) **금지**. Remote SSH `git@github.com:biospin/BioProject01.git`.
- 원문 binary·대용량(.h5ad/.h5mu/.loom/PDF/data)은 `.gitignore`. tracked = `*.md`, `*.yaml`, `*.tsv`(요약), 코드.

## 방법론 주의 (분석 시 반복)
1. **Pseudotime ≠ wall-clock**: lag은 pseudotime 단위로 보고. (GSE209878 day0/day7은 batch 통합돼 wall-clock anchor로 직접 못 씀.)
2. **Confound**: cell cycle·burst·ambient/doublet 통제. lineage별(within-lineage) 계산, rare lineage(MK/platelet) uncertainty 별도.
3. **Multicollinearity**: promoter/enhancer ATAC 등 강상관 → regularized.
4. **Multiple testing**: gene 단위 → permutation FDR.
5. method 차이 ≠ preprocessing 차이: 공통 전처리 후 method 분기(C2), 공통 graph ablation.
