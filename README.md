# BioProject01 — `kkkim-pipeline`

**HSPC 연구 단일 작업 브랜치.** Human HSPC 10x Multiome(GSE209878)로 gene별 chromatin→transcription **lag**를 정량하고, baseline epigenomic feature로 drug response timing을 예측한다. 논문 *근거*와 그것을 돌리는 *코드*를 한 브랜치, 두 폴더로 관리한다.

> 논문 분석 *하네스*(재사용 도구)는 외부 repo **`kakyungkim/paper-analysis-harness`** 에 있다. 새 분석은 거기서 돌리고 산출물만 `paper_analysis/`로 반입한다. 옛 `kkkim-paper-agent` 브랜치는 archive(보존만).

## 구조
- `paper_analysis/` — paper 분석 산출물 14편(dual-lens) + `_index/`. 아래 파이프라인 method 선택의 근거.
- `pipeline/hspc-velocity-benchmark/` — 실제 실행 코드(scripts/env/DESIGN/dataset/manifest).
- `AGENTS.md` + `skills/` — 파이프라인 분석 하네스 (박상준 `Harness_Baseline` 반입, **OpenClaw/Codex 포맷**, Claude Code 호환). dataset 4종 × `download/preprocessing/model/visualization`. active = `human-hspc-10x-multiome`.
- `SESSION-LOG.md` / `HANDOFF.md` / `TODO.md` — 작업 기록·현황·할 일.

## 빠른 시작
```bash
# 1) env (miniforge/mamba)
bash pipeline/hspc-velocity-benchmark/env/setup_envs.sh
# 2) 데이터
bash pipeline/hspc-velocity-benchmark/scripts/download_data.sh
# 3) 전처리(P1)
conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p1_build.py
```
상세: `pipeline/hspc-velocity-benchmark/{P0_provenance,P1_README,DESIGN,env/README}.md`.

## OpenClaw
이 하네스는 OpenClaw로 실행하는 연습 대상이다. `skills/<dataset>/<task>/agents/openai.yaml`이 OpenClaw/Codex agent 정의이고, `AGENTS.md`+`skills/ROUTES.md`가 라우터다. 앞으로 분석을 OpenClaw 기반으로 돌리는 것을 감안해 이 포맷을 유지한다.
