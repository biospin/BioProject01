# 03. 레이어 B — 멀티 AI 협업 인계 (여러 AI가 팀으로 이어달리기)

팀원마다 다른 AI(Claude, Codex, Gemini)를 쓰고 결과물은 JIRA·Confluence·Git으로 공유한다. 문제는 한 작업이 끝나도 다음 담당자의 AI에 신호가 자동으로 가지 않는다는 점이다. 사람이 확인할 때까지 대기가 생기고 인계가 지연된다.

이 레이어는 그 인계를 자동화한다. 설계 문서는 두 편이다.

- `guide/ai-handoff-architecture-guide.md`: **무엇을** 인계하나. JIRA 상태 전환 신호에서 다음 AI 실행까지의 4계층 구조.
- `guide/openclaw-claude-guide.md`: **어떻게 싸고 안정적으로** 돌리나. OpenClaw와 메시지 큐로 그 구조를 실현하고 비용을 통제하는 방법.

## 1. 설계 원칙

| 원칙 | 내용 |
| --- | --- |
| 단일 신호원 | 인계 신호는 JIRA 상태 전환만 쓴다. Git 머지 등은 JIRA 상태로 수렴시킨다 |
| 사람 승인 우선 | 초기엔 Slack 원클릭 승인 후 실행. 신뢰가 쌓이면 단계적으로 자동화 |
| 최소 권한 | AI별 서비스 계정 분리, 프로젝트 단위 권한, main 직접 push 금지 |
| 폭주 방지 | 티켓당 자동 인계 횟수 상한(기본 5회), 실패 시 즉시 사람 에스컬레이션 |

## 2. 4계층 아키텍처

```
① 이벤트 소스 (기존 스택)
   JIRA 상태 전환(Ready for AI) / Git PR 머지 → JIRA 상태 자동 전환
        │  Webhook (JIRA Automation → HTTP POST)
        ▼
② 이벤트 허브 (신규)
   Webhook 수신 → Next Agent 필드로 분기 → (선택) Slack 승인 → 워커 호출
   실패 시 ai-failed 라벨 + Slack 알림
        │  Execute / SSH / HTTP
        ▼
③ AI 워커 (신규)
   run_agent.sh <agent> <issue_key>
     ├ claude -p ...   (Claude Code headless)
     ├ codex exec ...  (Codex CLI 비대화)
     └ gemini -p ...   (Gemini CLI 비대화)
        │  MCP (공통 mcp.json)
        ▼
④ MCP 공통
   Atlassian 원격 MCP → JIRA 이슈·코멘트·상태, Confluence
   GitHub MCP → 저장소, PR, 이슈

작업 완료 → AI가 MCP로 JIRA 상태 전환 → 다시 ①의 신호 발생 → 체인 반복
```

### 인계 루프 (티켓 생애주기)

1. AI나 사람이 작업을 완료한다. 커밋·PR·문서와 함께 **Handoff 코멘트**를 남긴다.
2. JIRA 상태를 `Ready for AI`로 전환하고 `Next Agent` 필드를 지정한다.
3. JIRA Automation이 이벤트 허브로 웹훅을 보낸다.
4. 허브가 `Next Agent` 값으로 분기하고, 초기엔 Slack 승인을 거친다.
5. 해당 AI 워커가 실행되어 MCP로 티켓·코드 맥락을 읽고 작업한다.
6. 완료하면 1번으로 돌아간다. 체인이 이어진다.

## 3. Handoff 코멘트 — 인계 맥락의 정형화

모든 AI의 규칙 파일(CLAUDE.md / AGENTS.md / GEMINI.md)에 같은 템플릿을 강제한다.

```markdown
## Handoff
- 완료한 것: (요약 3줄 이내)
- 산출물: (커밋 해시 / PR 링크 / Confluence 페이지 링크)
- 다음 작업: (다음 AI가 해야 할 일, 구체적으로)
- 제약/주의: (건드리면 안 되는 것, 실패했던 접근)
- Next Agent: claude | codex | gemini | human
```

기준은 하나다. **다음 워커가 이 코멘트 하나만 읽어도 착수할 수 있어야 한다.** 이것이 레이어 A의 산출물 계약과 같은 발상이다. A는 파일로, B는 JIRA 코멘트로 맥락을 넘긴다.

## 4. 공통 MCP — 모든 AI가 같은 방식으로 읽고 쓴다

`mcp.json` 하나를 설정 전용 저장소(`agent-config`)로 버전 관리하고, 세 AI에 같은 서버 정의를 물린다. 연결 대상은 Atlassian 원격 MCP(JIRA·Confluence)와 GitHub MCP다. 세 도구 모두 MCP 표준을 따르므로 서버 정의는 그대로 재사용하고 파일 형식만 각 도구에 맞게 바꾼다. 토큰은 파일에 직접 쓰지 않고 환경변수·시크릿 매니저로 주입한다.

## 5. OpenClaw로 실현하기 — 허브와 워커를 대체

`ai-handoff-architecture-guide.md`는 이벤트 허브로 n8n을, 워커로 공용 서버의 `run_agent.sh`를 상정한다. `openclaw-claude-guide.md`는 그 ②+③(허브+워커)을 **OpenClaw와 메시지 큐로 대체**하는 경로를 제시한다. 별도 n8n·워커 서버를 세우지 않고 같은 인계 루프를 돌린다.

| 인계 가이드 계층 | 원 구성 | OpenClaw로 실현 |
| --- | --- | --- |
| ① 이벤트 소스 | JIRA 상태 전환 / PR 머지 | 그대로 유지 |
| ② 이벤트 허브 | n8n | 메시지 큐 브리지 + OpenClaw Webhooks 플러그인 |
| ③ AI 워커 | 공용 서버 + `run_agent.sh` + `claude -p` | OpenClaw 세션(인증·모델선택·thinking 레벨을 OpenClaw가 관장) |
| ④ MCP 공통 | `mcp.json` | 동일. OpenClaw 세션에도 같은 MCP 서버를 물린다 |

허브를 n8n으로 갈지 OpenClaw 웹훅+큐로 갈지는 팀 규모로 정한다. GUI 워크플로와 Slack 승인 버튼이 필요하면 n8n, 비용 통제를 한곳에서 하고 워커 서버 관리를 줄이고 싶으면 OpenClaw다.

메시지 큐를 앞에 두는 이유는 안정성과 비용이다. 웹훅을 허브에 직결하면 허브가 재시작 중일 때 이벤트를 잃는다. 큐는 고속 이벤트 유입과 느린 Claude 처리를 분리한다. 브리지 컨슈머가 지켜야 할 네 가지는 다음과 같다.

1. **ack는 Claude 처리 성공 이후에만.** 실패하면 ack하지 않고 데드레터큐로 격리한다. 이것이 인계 가이드의 "실패 시 상태 유지·자동 재시도 금지"를 자연히 만족한다.
2. **동시 처리 수 제한.** 레이트 리밋과 비용을 통제한다.
3. **멱등성·세션 키.** 재시도가 중복 인계를 만들지 않게 한다.
4. **병합(coalescing).** 같은 티켓의 연속 이벤트를 하나로 합쳐 Claude 호출 수 자체를 줄인다.

## 6. 비용 — 인계 체인은 호출을 곱셈으로 늘린다

AI-to-AI 인계는 한 티켓이 여러 AI를 연쇄 호출하므로 단발 실행보다 토큰 지출이 배로 뛴다. 그래서 비용 레버가 인계 자동화에서 더 중요해진다.

1. **병합**: 같은 티켓에 상태전환·코멘트 이벤트가 쏟아져도 브리지가 하나로 합쳐 호출 1회로.
2. **모델 티어링**: 저위험 작업(리뷰·테스트·문서화)은 Sonnet/Haiku로, 핵심 분석만 Opus로. `Next Agent`별로 모델을 다르게 물린다.
3. **프롬프트 캐싱**: 티켓 단위 sessionKey로 인계 맥락을 재사용해 입력 토큰을 줄인다.
4. **우선순위 큐**: 비싼 Opus 인계와 값싼 Sonnet 인계를 다른 큐로 분리 라우팅한다.
5. **DLQ**: poison 티켓이 무한 재인계로 과금되는 것을 막는다.

## 7. 보안·승인 게이트

- **승인 게이트**: 도입 초기엔 Slack 승인 필수. OpenClaw 경로에서는 브리지가 큐→OpenClaw POST 직전에 Slack "Send-and-Wait"를 두거나, 웹훅을 수동 트리거로 둔다.
- **최소 권한**: AI별 서비스 계정 분리, JIRA는 해당 프로젝트만, main 직접 push 금지(브랜치+PR).
- **서명 검증 2구간**: JIRA Automation의 `X-Handoff-Token`과 OpenClaw webhook `secret`을 둘 다 건다. 이벤트 소스와 브리지 사이, 브리지와 OpenClaw 사이를 모두 검증한다.
- **토큰 비노출**: API 키·PAT는 환경변수·시크릿 매니저로만. `.mcp.json`에 토큰 직접 기입 금지.

## 8. 도입 로드맵

| 주차 | 목표 | 산출물 |
| --- | --- | --- |
| 1주차 | JIRA 필드·워크플로·Automation + 허브 설치, Slack 알림까지만 | 인계 발생 즉시 알림(자동 실행 없음) |
| 2~3주차 | AI CLI·MCP 공통 설정·워커 구축, Slack 승인 후 반자동 | 첫 AI-to-AI 인계 파일럿 1건 |
| 4주차~ | 저위험 작업부터 승인 생략, 인계 상한·모니터링 정착 | 제한적 완전 자동 체인 + 비용 레버 계측 |

설치 절차 전체는 `guide/ai-handoff-architecture-guide.md` §4에, OpenClaw판 세부는 `guide/openclaw-claude-guide.md` §3에 있다.
