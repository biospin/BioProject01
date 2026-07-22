# OpenClaw에서 Claude 실행하기 — 비용 최소화 & 메시지 큐 연동 가이드

> OpenClaw 앞단에 Claude를 붙여 작업을 돌릴 때의 인증/과금 방식과, Kafka·ActiveMQ 같은 실시간 메시지 큐를 연동하는 아키텍처를 정리한 문서입니다.

> **연계 문서:** `ai-handoff-architecture-guide.md`(멀티 AI 협업 인계 자동화). 그 문서가 정의한
> **이벤트 허브(②)+AI 워커(③) 계층을 OpenClaw로 실현**하는 방법을 이 문서 **§3**에 통합했다.
> 요약하면: 인계 가이드는 *무엇을*(JIRA 상태전환 신호 → Handoff 코멘트 → 다음 AI), 이 문서는
> *어떻게 싸고 안정적으로*(OpenClaw + 메시지 큐 + 비용 레버)를 담당한다. **§3을 먼저 읽고**
> 세부 실행은 §1(비용)·§2(큐)로 내려가면 된다.

---

## 1. OpenClaw → Claude 실행 방식 (비용 우선)

OpenClaw로 Claude에 작업을 돌리는 핵심 경로는 **두 가지 인증 방식**이고, 여기에 토큰 비용을 줄이는 옵션들이 붙습니다.

### 1-1. (가장 저렴할 수 있음) 기존 Claude 구독을 Claude CLI로 재사용

이미 Claude Code 로그인(Pro/Max 구독)이 있다면, 별도 API 키 없이 그 로그인을 그대로 끌어다 쓰는 방식입니다. OpenClaw가 같은 호스트의 기존 Claude CLI 로그인을 감지해 재사용합니다.

```bash
openclaw onboard   # Claude CLI 선택
```

구독료가 정액이라 가벼운 개인용·간헐적 사용이라면 토큰당 과금보다 싸게 먹히는 경우가 많습니다.

> ⚠️ **2026년 6월 15일부터 과금 방식이 바뀝니다.**
> OpenClaw는 내부적으로 `claude -p`(비대화형 print 모드)로 동작하는데, Anthropic은 이 경로를 Agent SDK/프로그래매틱 사용으로 취급합니다. 6월 15일부터 구독 기반 `claude -p` 사용량은 일반 Claude 플랜 한도가 아니라 **매월 주어지는 별도 Agent SDK 크레딧**에서 먼저 차감되고, 그게 소진되면 표준 API 요율로 과금됩니다. 즉 "구독으로 무한정 자동화"는 더 이상 기대하기 어렵습니다.

### 1-2. (예측 가능한 비용) Anthropic API 키 + 비용 절감 옵션

```bash
openclaw onboard --anthropic-api-key "$ANTHROPIC_API_KEY"
```

토큰당 종량제라 항상 켜둔 게이트웨이 호스트나 공유 자동화에 가장 명확하고 예측 가능한 경로로 권장됩니다. 비용을 더 줄이는 옵션:

- **프롬프트 캐싱** — API 키 인증에서 지원. 기본값 5분(`"short"`), 확장 1시간(`"long"`). 같은 컨텍스트를 반복 사용하는 에이전트는 `cacheRetention: "long"`으로 입력 토큰 비용을 크게 절감. 재사용이 거의 없는 버스트성 트래픽은 `"none"`.
- **모델 선택** — 기본을 Opus로 두면 비싸짐. 단순 작업은 Sonnet/Haiku급으로 내리고, 정말 필요한 에이전트만 Opus를 쓰도록 에이전트별로 모델 분리.
- **thinking 레벨 조절** — Claude 4.6은 OpenClaw에서 기본 `adaptive` thinking. 단순 작업은 레벨을 낮춰 출력 토큰 절감.

### 1-3. 비용 우선 추천 순서

| 상황 | 권장 방식 |
| --- | --- |
| 이미 Pro/Max 구독 보유 + 개인용·소규모 자동화 | 6월 15일 전까지 **Claude CLI 재사용**이 최저가. 이후 Agent SDK 크레딧 소진 양상 보고 재판단 |
| 항상 켜두는 서버 / 공유 프로덕션 | **API 키 + 프롬프트 캐싱(`long`) + 작업별 모델 다운그레이드** 조합 |

> 참고: OpenClaw는 Claude 외에 구독형 대안으로 OpenAI Codex, Qwen Cloud, MiniMax, Z.AI/GLM도 안내합니다. "Claude로 실행"이 전제라면 위 두 경로가 핵심입니다.

---

## 2. Kafka / ActiveMQ 등 실시간 메시지 큐 연동

### 2-1. 핵심 전제

**OpenClaw에는 Kafka나 ActiveMQ를 직접 구독(consume)하는 네이티브 백엔드가 없습니다.** 네이티브로 있는 건 채널(Slack·Telegram·WhatsApp·Discord)과, 외부 자동화를 OpenClaw TaskFlow에 묶어주는 **Webhooks 플러그인**입니다.

따라서 메시지 큐는 "OpenClaw 안에 꽂는다"가 아니라 **OpenClaw 앞단에 두는 버퍼/전달 계층**으로 설계합니다. 큐를 구독하는 작은 **브리지 컨슈머**를 두고, 그 컨슈머가 OpenClaw webhook으로 POST 합니다.

### 2-2. 아키텍처

```
Event sources        Broker              Bridge              OpenClaw
(external events) → (Kafka/ActiveMQ) → (throttle + dedup) → (webhook → Claude)
                                              │
                                              │ on failure
                                              ▼
                                       Dead-letter queue
                                       (poison messages)

  ↑──────────── ack only after Claude succeeds ────────────┘
```

- 이벤트 소스가 Kafka/ActiveMQ 브로커로 발행
- 브리지 컨슈머가 레이트리밋·중복제거를 거쳐 OpenClaw webhook으로 전달
- **Claude 처리가 성공한 뒤에만 ack(커밋)**
- 실패 메시지는 데드레터큐(DLQ)로 격리

### 2-3. 왜 큐를 앞에 두나 (안정성 + 비용)

단순 webhook 직결의 함정: 발신자가 이벤트를 쏘는 순간 Gateway가 재시작 중이고 재시도가 짧으면 **이벤트를 잃습니다.** "webhook은 불안정하다"의 진짜 원인은 "엔드포인트에 큐가 없다"는 것입니다.

여기에 LLM 특유의 문제가 겹칩니다 — Claude 호출은 **느리고(수 초), 레이트 리밋이 있고, 토큰당 돈이 나갑니다.** 큐는 고속 이벤트 유입과 느린 Claude 처리를 분리합니다.

- **백프레셔** — 컨슈머의 동시 처리 수(prefetch/in-flight) 제한으로 레이트 리밋·비용 통제
- **중복 제거·병합(coalescing)** — 같은 엔티티 이벤트 50건을 호출 1번으로 합쳐 토큰 비용 절감
- **재시도·DLQ** — poison 메시지의 무한 재시도 과금 차단
- **재처리(replay)** — Kafka라면 오프셋을 되감아 과거 이벤트 재처리

### 2-4. Kafka vs ActiveMQ — 이 용도에서의 선택

**ActiveMQ / Artemis / RabbitMQ (전통 브로커)** 가 LLM 작업 구동에 더 자연스러운 경우가 많습니다.
- 작업 큐 의미론(per-message ack, 재전달 제한, 우선순위, TTL, 내장 DLQ)이 그대로 들어맞음
- "이벤트 1 = Claude 작업 1"을 받아 처리하고 **성공 시에만 ack** → 크래시해도 메시지 보존
- 명령형 워크로드, 중간 규모, 풍부한 메시지 단위 제어에 적합

**Kafka** 는 고처리량·파티션 로그·재처리(오프셋 되감기)·팬아웃이 강점.
- 이벤트가 폭발적으로 많거나, 같은 스트림을 여러 컨슈머 그룹이 나눠 보거나, 재처리가 중요할 때
- 단, 메시지 단위 ack/재전달/우선순위/DLQ가 브로커 내장이 아님 → 멱등성·DLQ·동시성 제어를 **컨슈머에서 직접** 구현

| 상황 | 권장 |
| --- | --- |
| 개인/팀 자동화 + 작업 신뢰성 핵심 | ActiveMQ (또는 RabbitMQ) |
| 대량 이벤트 스트림에서 LLM이 일부만 처리 + 재처리/팬아웃 중요 | Kafka |
| 혼합 | Kafka로 전체 수신·아카이빙 → 처리할 것만 작업 큐(MQ)로 |

### 2-5. 브리지 컨슈머에서 꼭 지킬 4가지

1. **ack는 Claude 처리 성공 이후에만** — OpenClaw가 완료를 응답한 뒤 커밋(Kafka 오프셋 커밋 / MQ message ack).
2. **동시 처리 수 제한** — Kafka는 파티션 수, MQ는 prefetch/consumer 수로 in-flight 통제.
3. **멱등성·세션 키** — 처리한 이벤트 id 저장, 또는 PR 번호·인보이스 id마다 세션 하나. 재시도가 중복 알림을 만들지 않도록.
4. **병합(coalescing)** — 같은 엔티티 연속 이벤트는 컨슈머에서 하나로 합쳐 Claude 호출 수 자체를 줄임.

### 2-6. OpenClaw 수신부 (Webhooks 플러그인)

브리지가 POST 하는 대상. 플러그인은 Gateway 프로세스 안에서 동작하므로, Gateway가 다른 머신이면 그 호스트에 설치 후 재시작.

```json5
{
  plugins: { entries: { webhooks: { enabled: true, config: { routes: {
    queue: {
      path: "/plugins/webhooks/queue",
      sessionKey: "agent:main:main",   // 또는 엔티티별 동적 키
      secret: { source: "env", provider: "default", id: "OPENCLAW_WEBHOOK_SECRET" },
      controllerId: "webhooks/queue",
      description: "Kafka/MQ bridge",
    },
  } } } } },
}
```

- 페이로드는 `message` 필드를 포함한 JSON으로 POST. 응답을 특정 채널·수신자로 보내려면 `delivery` 필드 추가.
- **secret(서명 검증) 필수.** 이벤트 소스 측 서명(GitHub/Stripe HMAC 등)도 브리지에서 한 번 더 검증.

> 큐 직접 운영이 부담스러운 소규모라면, 소스와 OpenClaw 사이에 **webhook 릴레이(Hookdeck 등)** 를 두는 더 가벼운 선택지도 있음 — 이벤트 선저장·재시도·dedup·실패 재전송·대시보드 제공.

### 2-7. 비용 관점 요약

큐는 단순 안정성 장치가 아니라 **비용 통제 장치**입니다. Claude 도달 전에 컨슈머에서:

1. 중복·연속 이벤트 **병합**
2. **동시 처리 수**로 호출 폭주 차단
3. **우선순위 큐**로 비싼 Opus 작업과 값싼 Sonnet 작업 분리 라우팅
4. **DLQ**로 실패 메시지 무한 재시도 과금 차단

이를 모델 티어링·프롬프트 캐싱과 맞물리면 실제 토큰 지출이 크게 줄어듭니다.

---

## 3. 멀티 AI 인계 자동화에 OpenClaw 적용 (`ai-handoff-architecture-guide.md` 통합)

인계 가이드는 4계층(① 이벤트 소스=JIRA/Git · ② 이벤트 허브=n8n · ③ AI 워커=run_agent.sh · ④ MCP 공통)으로
AI-to-AI 인계를 설계한다. 그중 **②+③(허브+워커)을 OpenClaw로 대체**하면, 별도 n8n·워커 서버를 세우지 않고도
같은 인계 루프를 돌릴 수 있다. 이 절은 두 문서를 하나의 실행 경로로 잇는다.

### 3-1. 두 아키텍처의 접점 — 무엇이 무엇을 대체하나

| 인계 가이드 계층 | 원 구성 | OpenClaw로 실현 |
| --- | --- | --- |
| ① 이벤트 소스 | JIRA 상태 `Ready for AI` 전환 / PR 머지 | **그대로 유지** (JIRA Automation 웹훅) |
| ② 이벤트 허브 | n8n (Webhook→Switch→승인→실행) | **메시지 큐 브리지(§2)** + OpenClaw Webhooks 플러그인(§2-6). 큐가 허브의 폭주방지·재시도·DLQ를 대신함 |
| ③ AI 워커 | 공용 서버 + `run_agent.sh` + `claude -p` | **OpenClaw 세션**(§1). `claude -p`를 직접 부르는 대신 OpenClaw가 인증·모델선택·thinking레벨을 관장 |
| ④ MCP 공통 | `mcp.json` (atlassian + github) | **동일** — OpenClaw 세션에도 같은 MCP 서버를 물린다 |

→ **핵심 결정:** n8n을 쓸지, OpenClaw 웹훅+큐로 갈지는 팀 규모로 정한다.
- **n8n 경로(인계 가이드 원안):** GUI 워크플로·Slack 승인 버튼이 필요하고 AI CLI를 팀이 직접 관리할 때.
- **OpenClaw 경로(이 문서):** Claude 실행을 OpenClaw에 위임해 **비용 레버(캐싱·모델 티어링·병합)를 한 곳에서** 통제하고, 워커 서버 관리를 줄이고 싶을 때. 인계 가이드 ③의 `run_agent.sh` 프롬프트가 그대로 OpenClaw 세션 지시로 옮겨간다.

### 3-2. 통합 인계 루프 (JIRA 상태 → OpenClaw → JIRA 상태)

```
① JIRA: 상태 → 'Ready for AI', Next Agent 필드 지정
        │  (Automation 웹훅)
        ▼
② 브리지 컨슈머 (§2-5 4원칙: ack-after-success · 동시성제한 · 멱등성 · 병합)
   └ JIRA 웹훅을 큐(ActiveMQ/Kafka)에 적재 → dedup·throttle → OpenClaw webhook POST
        │  (secret 서명 검증, §2-6)
        ▼
③ OpenClaw 세션 = Claude 워커
   └ MCP(atlassian)로 티켓 조회 → 최신 'Handoff' 코멘트 읽기 → '다음 작업' 수행
   └ 작업 브랜치 커밋/PR (main 직접 push 금지)
        ▼
④ 완료: 동일 Handoff 템플릿으로 결과 코멘트 + 상태 전환
   └ 후속 AI 있으면 → 'Ready for AI'(+Next Agent) : ①로 복귀 (체인)
   └ 사람 검토 필요 → 'In Review'(+Next Agent=human) : 체인 정지
        ▲
        └ Claude 처리 성공을 OpenClaw가 응답한 뒤에만 큐 ack (§2-5 ①)
```

- **인계 가이드 §2.1의 6단계 루프를 그대로 보존**하되, 3~5단계(허브 분기·워커 실행)를 큐+OpenClaw가 담당.
- 큐의 **ack-after-success**(§2-5)가 인계 가이드의 "실패 시 상태 유지·자동 재시도 금지"(§5.2)를 자연히 만족 — Claude가 실패하면 ack 안 되고 DLQ로 격리되므로 상태가 넘어가지 않는다.

### 3-3. Handoff 코멘트 템플릿 — OpenClaw 세션 지시에 강제

인계 가이드 §3.5의 템플릿을 **OpenClaw 세션 프롬프트에 그대로 박는다**(§1의 세션이 이 규칙을 지키도록):

```markdown
## Handoff
- 완료한 것: (요약 3줄 이내)
- 산출물: (커밋 해시 / PR 링크 / Confluence 페이지 링크)
- 다음 작업: (다음 AI가 해야 할 일, 구체적으로)
- 제약/주의: (건드리면 안 되는 것, 실패했던 접근)
- Next Agent: claude | codex | gemini | human
```

> 기준(인계 가이드와 동일): **다음 워커가 이 코멘트 하나만 읽어도 착수할 수 있어야 한다.**
> OpenClaw 세션은 `sessionKey`(§2-6)를 **티켓 키 단위**로 잡아, 한 티켓의 인계 맥락이 한 세션에 누적되게 하면
> 프롬프트 캐싱(§1-2 `cacheRetention:"long"`)까지 얹혀 토큰 비용이 크게 준다.

### 3-4. 라우팅 — Next Agent → sessionKey / 채널

- 인계 가이드의 **`Next Agent` 필드**(claude/codex/gemini/human)를 브리지가 읽어 분기한다.
  - `claude` → OpenClaw Claude 세션 webhook
  - `codex`/`gemini` → OpenClaw는 이들도 백엔드로 안내(§1 참고: Codex/Qwen/GLM 등) → 같은 webhook 라우트에 백엔드만 교체
  - `human` → 브리지가 큐에서 소비하지 않고 Slack/JIRA 알림만
- **폭주 방지(Hop Count):** 인계 가이드 §3.1의 `AI Hop Count`를 브리지 멱등성 키와 함께 검사(§2-5 ③). `<5`만 통과, 초과 시 DLQ+알림 — 인계 가이드 §5.2 "5회 초과 차단"과 동일.

### 3-5. 이 통합의 진짜 이득 = 비용 (인계 체인은 호출을 곱셈으로 늘린다)

AI-to-AI 인계는 **한 티켓이 여러 AI를 연쇄 호출**하므로, 단발 실행보다 토큰 지출이 배로 뛴다. 그래서 §1·§2의
비용 레버가 인계 자동화에서 **더 중요**해진다:

1. **병합(§2-4·2-7):** 같은 티켓에 연속으로 상태전환/코멘트 이벤트가 쏟아져도 브리지가 하나로 합쳐 Claude 호출 1회로.
2. **모델 티어링(§1-2):** 인계 가이드 §5.1의 "저위험 작업 유형(리뷰·테스트·문서화)"을 **Sonnet/Haiku로**, 핵심 분석만 Opus로. `Next Agent`별로 모델을 다르게 물릴 수 있다.
3. **프롬프트 캐싱(§1-2):** 티켓 단위 sessionKey로 인계 맥락을 재사용 → `cacheRetention:"long"`.
4. **우선순위 큐(§2-7):** 비싼 Opus 인계와 값싼 Sonnet 인계를 다른 큐로 분리 라우팅.
5. **DLQ(§2-5):** poison 티켓이 무한 재인계로 과금되는 것을 차단(= 인계 가이드 §5.2 폭주 방지의 비용판).

### 3-6. 보안·승인 게이트 — 두 문서의 합집합

- **승인 게이트(인계 가이드 §5.1):** 도입 초기엔 Slack 승인 필수. OpenClaw 경로에서는 브리지가 큐→OpenClaw POST **직전에** Slack "Send-and-Wait"를 두거나, OpenClaw webhook을 **수동 트리거 세션**으로 두어 사람이 승인 후 실행.
- **최소 권한(양 문서 공통):** AI별 서비스 계정 분리, JIRA는 해당 프로젝트만, **main 직접 push 금지→브랜치+PR**. (단 이 저장소는 CLAUDE.md가 작업 브랜치 `kkkim-pipeline` 자동 push는 허용하므로, 그 정책이 우선한다.)
- **서명 검증(§2-6 + 인계 가이드 §4.1.3):** JIRA Automation의 `X-Handoff-Token`과 OpenClaw webhook `secret`을 **둘 다** 건다 — 이벤트 소스↔브리지, 브리지↔OpenClaw 두 구간 모두 검증.
- **토큰 비노출:** API 키·PAT는 환경변수/시크릿 매니저로만. `.mcp.json`에 토큰 직접 기입 금지(양 문서 공통).

### 3-7. 도입 순서 (인계 가이드 §6 로드맵의 OpenClaw판)

| 단계 | 인계 가이드 원안 | OpenClaw 통합판 |
| --- | --- | --- |
| 1주차 | JIRA 필드/상태/Automation + n8n, Slack 알림까지 | JIRA 동일 + **OpenClaw 온보딩(§1)** + webhook 플러그인(§2-6), 알림까지 |
| 2~3주차 | AI CLI+MCP+워커, Slack 승인 후 반자동 | **큐 브리지(§2-5)** + OpenClaw 세션 라우팅, Slack 승인 후 반자동. 첫 인계 파일럿 1건 |
| 4주차~ | 저위험부터 승인 생략 | 동일 + **비용 레버(§3-5) 정착**(모델 티어링·캐싱·병합 계측) |

---

## 부록: 빠른 의사결정 체크리스트

- [ ] 이미 Pro/Max 구독이 있나? → (6/15 전) Claude CLI 재사용 검토
- [ ] 24/7 서버/프로덕션인가? → API 키 + 캐싱(`long`) + 모델 티어링
- [ ] 이벤트가 초당 수백 이상 / 재처리 필요? → Kafka, 아니면 ActiveMQ·RabbitMQ
- [ ] 큐 운영 부담이 큰 소규모? → webhook 릴레이로 시작
- [ ] 비용 핵심 레버: 병합 · 동시성 제한 · 모델 다운그레이드 · 프롬프트 캐싱 · DLQ

### AI-to-AI 인계 자동화(§3)를 도입하나?

- [ ] 이벤트 허브를 n8n으로 vs OpenClaw 웹훅+큐로? → GUI/승인버튼 필요=n8n, 비용 통제 일원화=OpenClaw (§3-1)
- [ ] JIRA에 `Ready for AI` 상태 + `Next Agent`·`AI Hop Count` 필드 생성했나? (인계 가이드 §4.1 — **관리자 권한 필요, 아직 없으면 선행**)
- [ ] Handoff 코멘트 템플릿을 OpenClaw 세션 프롬프트에 강제했나? (§3-3)
- [ ] `sessionKey`를 티켓 키 단위로 잡아 캐싱까지 얹었나? (§3-3)
- [ ] `Next Agent`별 모델 티어링 매핑(저위험=Sonnet/Haiku, 핵심=Opus)? (§3-5)
- [ ] 두 구간 서명 검증(JIRA `X-Handoff-Token` + OpenClaw `secret`)? (§3-6)
- [ ] Hop Count `<5` 검사 + DLQ로 무한 재인계 과금 차단? (§3-4·3-5)
