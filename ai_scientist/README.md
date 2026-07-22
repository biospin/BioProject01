# ai_scientist/ — AI Scientist 설계 정리

이 폴더는 이번 프로젝트에서 **AI Scientist**(인공지능이 연구 도구를 넘어 연구 과정 전반을 자동화하고, 여러 연구자가 함께 쓰도록 만든 구조)를 어떻게 설계했는지 한곳에 정리한 문서다. 새 코드를 만드는 것이 아니라, `kkkim-pipeline` 브랜치에 이미 흩어져 구현·기록된 설계를 확인해 하나의 지도로 묶었다.

## 무엇을 다루나

목표는 두 가지였다.

1. **연구 과정 전반의 자동화**: 논문 탐색과 정리, 가설 설정, 실험 수행, 그림·집필, 검수, 발표까지를 사람이 매 단계 손으로 잇지 않고 하나의 흐름으로 돌린다.
2. **여러 연구자와 협업하는 구조**: 팀원마다 다른 AI(Claude, Codex, Gemini)를 쓰더라도, 작업을 서로에게 자동으로 넘기고 이어받는 인계 체계를 표준화한다.

이 두 목표는 각각 하나의 레이어로 설계했고, 서로 맞물린다.

| 레이어 | 무엇인가 | 이 저장소의 구현·근거 |
| --- | --- | --- |
| **A. 단일 랩 자동화** | 한 연구자의 연구 과정 전체를 agent 멤버들이 나눠 맡아 자동으로 돌리는 "AI 연구 랩" | `.claude/agents/` 8종 + `paper-production-orchestrator` Skill + `AGENTS.md`/`skills/` 라우터 + 파이프라인 `scripts/`(P0–P5). 지도 = `docs/HARNESS.md` |
| **B. 멀티 AI 협업 인계** | 여러 연구자·여러 AI가 JIRA 상태 신호로 작업을 자동 인계하는 체계 | `guide/ai-handoff-architecture-guide.md` + `guide/openclaw-claude-guide.md` |

레이어 A는 "AI 한 명이 논문 한 편을 어떻게 끝까지 끌고 가나"를, 레이어 B는 "그런 AI 여럿이 팀으로 어떻게 이어달리나"를 설계한다. A가 랩 안의 분업이라면 B는 랩과 랩, 사람과 사람 사이의 배턴 터치다.

## 문서 구성

- [01_overview.md](01_overview.md) — AI Scientist가 무엇을 자동화하는지와 전체 그림
- [02_single_lab_harness.md](02_single_lab_harness.md) — 레이어 A: 단일 랩 자동화(멤버 명부, 논문 생산 루프, 파이프라인, 게이트)
- [03_multi_ai_collaboration.md](03_multi_ai_collaboration.md) — 레이어 B: 멀티 AI 인계 자동화(JIRA→허브→워커→MCP, OpenClaw+큐)
- [04_design_principles.md](04_design_principles.md) — 두 레이어를 관통하는 설계 원칙
- [05_component_map.md](05_component_map.md) — 설계 요소와 실제 저장소 파일의 매핑

## 한눈에 보는 전체 그림

```
                    사람 = PI (방향 설정 · 승인 · 공개 게이트)
                                  │
      ┌───────────────────────────┴───────────────────────────┐
      │                                                        │
  레이어 A: 단일 랩 자동화                        레이어 B: 멀티 AI 협업 인계
  (한 AI가 논문 한 편을 끝까지)                    (여러 AI가 팀으로 이어달리기)
      │                                                        │
  paper-production-orchestrator (Skill)              JIRA 상태 전환(Ready for AI)
      │  ↓ 멤버 호출                                          │  ↓ Automation 웹훅
  기획 → 분석 → 집필·그림 → 검수 → 발표               이벤트 허브(n8n 또는 OpenClaw+큐)
      │  ↓ 산출물 계약(파일로 인계)                            │  ↓ Next Agent 분기
  results/ · manuscript/ · figures/                  AI 워커(claude/codex/gemini)
      │  ↓ 검증 게이트(숫자 재계산)                            │  ↓ 공통 MCP(JIRA·GitHub)
  사람 승인 → 공개                                    Handoff 코멘트 → 다음 AI (체인)
```

두 레이어의 접점은 **산출물 계약**과 **Handoff 규율**이다. 레이어 A의 멤버가 결과를 파일로 남기는 규율(results/FINDINGS.md 등)과, 레이어 B의 AI가 JIRA에 Handoff 코멘트를 남기는 규율은 같은 발상이다. 다음에 일할 주체가 그 산출물 하나만 읽어도 곧바로 착수할 수 있게 만든다.
