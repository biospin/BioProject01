# 05. 컴포넌트 매핑 — 설계 요소가 저장소 어디에 있나

AI Scientist 설계의 각 요소가 실제로 어느 파일에 구현·문서화돼 있는지 정리한 지도다. 이 폴더(`ai_scientist/`)는 설계를 **설명**하고, 아래 파일들이 그 설계를 **구현**한다.

## 레이어 A — 단일 랩 자동화

| 설계 요소 | 저장소 위치 |
| --- | --- |
| 랩 구조 지도(멤버 명부·관계도·JD) | `docs/HARNESS.md` |
| 라우팅표 + 산출물 계약 요약 | `CLAUDE.md` (*Agent routing & artifact contract* 절) |
| 멤버 정의 8종 | `.claude/agents/{hspc-velocity-analyst,literature-scout,novelty-strategist,research-methodologist,manuscript-writer,presenter,paper-critic,paper-orchestrator,design}.md` |
| 오케스트레이터(실행 입구) | `.claude/skills/paper-production-orchestrator/SKILL.md` |
| 단일 컨텍스트(thesis·claim 등급표·loop 규율) | `pipeline/hspc-velocity-benchmark/manuscript/PAPER_DIRECTION.md` |
| 분석 실행 엔진(P0–P5) | `pipeline/hspc-velocity-benchmark/scripts/` (`download_data.sh`, `p1_build.py`, `p2_*.py`, `p3_*.py`, `p10*` 등) |
| method 선택 근거 | `pipeline/hspc-velocity-benchmark/DESIGN.md`, `paper_analysis/`(dual-lens 14편) |
| 실험 env 격리 | `pipeline/hspc-velocity-benchmark/env/` |
| 분석 산출물 계약 | `pipeline/hspc-velocity-benchmark/results/FINDINGS.md` + `results/*.csv` + `results/*.md` |
| 집필·그림 산출물 | `pipeline/hspc-velocity-benchmark/manuscript/draft_v2{,_ko}.md`, `figures/figNN_*.py` |
| 검수·리뷰 산출물 | `manuscript/REVIEW-<venue>-<date>.md` |
| 검증 게이트 스크립트 | `scripts/p3_concordance.py`, `p3_crossdataset_concordance.py`, `p3_scrambled_null.py` |
| 글쓰기 규율(한국어 윤문) | `.claude/rules/writing-style.md` |
| 상태 핸드오프 | `HANDOFF.md`, `TODO.md`, `SESSION-LOG.md` |

## 레이어 B — 멀티 AI 협업 인계

| 설계 요소 | 저장소 위치 |
| --- | --- |
| 인계 아키텍처(4계층·인계 루프·설치 가이드) | `guide/ai-handoff-architecture-guide.md` |
| OpenClaw 실현(허브+워커 대체·메시지 큐·비용 레버) | `guide/openclaw-claude-guide.md` |
| 분석 하네스 project frame(OpenClaw/Codex 네이티브 포맷) | `AGENTS.md` (dataset 라우팅을 `skills/ROUTES.md`에 위임) |
| dataset→task 스킬 트리(`skills/ROUTES.md`, `skills/<dataset>/<task>/{SKILL.md,agents/openai.yaml}`) | 이 브랜치 체크아웃에는 없다. `AGENTS.md`·`README.md`가 규정하는 포맷이며, 실제 스킬 트리는 OpenClaw로 돌릴 때 채운다 |
| MCP 공통 설정 | `.mcp.json` (설계 목표는 `agent-config` 저장소로 버전 관리) |
| 팀·역할·AI 계정 매핑 | `Project-Info.md` (데이터셋 담당자 ↔ github·atlassian·slack·openclaw bot) |
| JIRA·Confluence 좌표 | `Project-Info.md` (JIRA space `BIOP01`, Confluence space `VC`) |

## 두 레이어의 접점

| 공유 요소 | 레이어 A에서 | 레이어 B에서 |
| --- | --- | --- |
| 인계 계약 | 결과 파일(`results/FINDINGS.md`) | JIRA Handoff 코멘트 |
| 사람 게이트 | 공개·main 병합 승인 | 초기 Slack 승인 |
| 폭주·비용 방지 | 검증 게이트, claim 등급 | Hop Count 상한, 큐·DLQ, 모델 티어링 |
| 실행 도구 | Claude Code(agent·Skill) | OpenClaw 세션 또는 `run_agent.sh` |
| 라우터 포맷 | `CLAUDE.md` 라우팅표 | `Next Agent` 필드 → 브리지 분기 |

## 읽는 순서 제안

1. 전체 그림만 빠르게: 이 폴더 [README.md](README.md)와 [01_overview.md](01_overview.md).
2. 단일 랩이 어떻게 도나: [02_single_lab_harness.md](02_single_lab_harness.md) → `docs/HARNESS.md` → `.claude/skills/paper-production-orchestrator/SKILL.md`.
3. 여러 AI가 어떻게 이어달리나: [03_multi_ai_collaboration.md](03_multi_ai_collaboration.md) → `guide/ai-handoff-architecture-guide.md` → `guide/openclaw-claude-guide.md`.
4. 왜 이렇게 설계했나: [04_design_principles.md](04_design_principles.md).
