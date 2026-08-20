# 05. 컴포넌트 매핑 — 설계 요소가 저장소 어디에 있나

AI Scientist 설계의 각 요소가 실제로 어느 파일에 구현·문서화돼 있는지 정리한 지도다. 이 폴더(`ai_scientist/`)는 설계를 **설명**하고, 아래 파일들이 그 설계를 **구현**한다.

## 레이어 A — 단일 랩 자동화

| 설계 요소 | 저장소 위치 |
| --- | --- |
| 랩 구조 지도(멤버 명부·관계도·JD) | `docs/HARNESS.md` |
| 라우팅표 + 산출물 계약 요약 | `CLAUDE.md` (*Agent routing & artifact contract* 절) |
| 멤버 정의 11 | `.claude/agents/{hspc-velocity-analyst,literature-scout,novelty-strategist,research-methodologist,manuscript-writer,manuscript-condenser,presenter,paper-critic,venue-reviewer,paper-orchestrator,design}.md` |
| Skill (유일한 project-scope, 실행 입구) | `.claude/skills/paper-production-orchestrator/SKILL.md` — 논문 생산 오케스트레이션. 나머지 능력은 agent, 그 외 skill은 Claude Code 전역 skill |
| 단일 컨텍스트(thesis·claim 등급표·loop 규율) | `pipeline/hspc-velocity-benchmark/manuscript/PAPER_DIRECTION.md` |
| 분석 실행 엔진(P0–P5) | `pipeline/hspc-velocity-benchmark/scripts/` (`download_data.sh`, `p1_build.py`, `p2_*.py`, `p3_*.py`, `p10*` 등) |
| method 선택 근거 | `pipeline/hspc-velocity-benchmark/DESIGN.md`, `paper_analysis/`(dual-lens 14편) |
| 실험 env 격리 | `pipeline/hspc-velocity-benchmark/env/` |
| 분석 산출물 계약 | `pipeline/hspc-velocity-benchmark/results/FINDINGS.md` + `results/*.csv` + `results/*.md` |
| 집필·그림 산출물 | `pipeline/hspc-velocity-benchmark/manuscript/draft_v2{,_ko}.md`, `figures/figNN_*.py` |
| 검수·리뷰 산출물 | `manuscript/REVIEW-<venue>-<date>.md` |
| 검증 게이트 스크립트 | `scripts/p3_concordance.py`, `p3_crossdataset_concordance.py`, `p3_scrambled_null.py` |
| 하네스 SSOT 매니페스트 | `harness.yaml` (역할·산출물·게이트 기준표) |
| 하네스 자기검진(harness-doctor) | `scripts/harness_doctor.py` + `.github/workflows/harness-doctor.yml` (팬텀 역할·경로 CI 차단, BIOP01-66) |
| 하네스 3계층 경계 | `docs/HARNESS-LAYERS.md` (core / project profile / run instance, BIOP01-67) |
| 선언적 실행 상태·claim 추적 | `harness_after/RUN_STATE.template.yaml`(BIOP01-68), `harness_after/CLAIMS.template.yaml`(BIOP01-69) |
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

## 외부 참조 — 검증·검수 게이트 강화 근거

검증·검수를 더 조이는 아이디어는 딥리서치·적대적 검토 하네스 두 편에서 참조했다. 통째로 이식할 대상이 아니라, 게이트 한 지점을 깊게 파는 부품으로 가져온다.

| 참조 문서 | 가져온 것 | 반영 위치 |
| --- | --- | --- |
| `docs/hyperresearchdeck.html` | 결정론적 코드 vs LLM 분리, 상태는 파일에(컨텍스트 부패 방어), 고치되 다시 쓰지 마라(도구 권한 락), 인용 무결성·철회·숫자 추적성 lint, 역할별 모델 배분을 검증된 설정 객체로 | [02](02_single_lab_harness.md) §6.1, [04](04_design_principles.md) 원칙 1·3·8, [03](03_multi_ai_collaboration.md) §6 |
| `docs/adversarial_multi_llm_council_harness.md` | 다중 모델 적대적 검토(모델·세션 독립, 자기비판과 타모델 비판 분리, 비판의 재비판, 합의≠진실, 모델 이름≠권위), claim·비판 분류 taxonomy | [02](02_single_lab_harness.md) §6.1, [04](04_design_principles.md) 원칙 3 |

아직 도입하지 않고 더 큰 작업으로 남겨둔 것: 읽은 소스를 영구 축적하고 다음 실행이 재사용하는 Vault, 신디케이션을 합의로 착각하지 않는 독립성 감사(5부=1표). `paper_analysis/`를 인덱스된 재사용 자산으로 키우는 방향과 맞닿아 있다.
