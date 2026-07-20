# 멀티 AI 협업 인계 자동화 구성안 및 설치 가이드

> JIRA / Confluence / Git 스택을 그대로 유지하면서, 웹훅 이벤트 허브 + MCP 공통화로
> AI(Claude, Codex, Gemini) 간 작업 인계를 자동화하는 구성안입니다.

- 작성일: 2026-07-14
- 버전: v1.0 (초안)
- 대상 독자: 프로젝트 관리자, 인프라 담당자, 각 AI 사용 팀원

---

## 1. 배경과 목표

### 1.1 현재 문제

- 팀원별로 서로 다른 AI(Claude, Codex, Gemini)를 사용하며 결과물은 JIRA / Confluence / Git으로 공유
- 한 작업이 완료되어도 **다음 담당자의 AI에 자동으로 신호가 전달되지 않아** 사람이 확인할 때까지 대기 → 인계 지연 발생

### 1.2 목표

1. 작업 완료 신호를 **JIRA 상태 전환 하나로 일원화**한다.
2. 상태 전환이 발생하면 **이벤트 허브가 다음 담당 AI를 자동(또는 원클릭 승인 후) 실행**한다.
3. 모든 AI가 **동일한 MCP 설정**으로 JIRA / Confluence / Git을 읽고 쓰게 하여 인계 방식을 표준화한다.
4. 인계 시 **정형화된 컨텍스트 패키지**(Handoff 코멘트)를 강제하여, 다음 AI가 코멘트 하나만 읽고 착수할 수 있게 한다.

### 1.3 설계 원칙

| 원칙 | 내용 |
|---|---|
| 단일 신호원 | 인계 신호는 JIRA 상태 전환만 사용. Git 머지 등은 JIRA 상태로 수렴시킴 |
| 사람 승인 우선 | 초기에는 Slack 원클릭 승인 후 실행. 신뢰 확보 후 단계적 완전 자동화 |
| 최소 권한 | AI별 서비스 계정 분리, 프로젝트 단위 권한, main 브랜치 직접 push 금지 |
| 폭주 방지 | 티켓당 자동 인계 횟수 상한(기본 5회), 실패 시 즉시 사람 에스컬레이션 |

---

## 2. 전체 아키텍처

```
┌──────────────────────────────────────────────────────────────────┐
│  ① 이벤트 소스 계층 (기존 스택)                                     │
│                                                                    │
│   JIRA ── 상태 전환(Ready for AI) ──┐                              │
│   Git  ── PR 머지 → JIRA 상태 자동 전환(스마트 커밋/연동) ──┘        │
└───────────────────────────┬──────────────────────────────────────┘
                            │ Webhook (JIRA Automation → HTTP POST)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  ② 이벤트 허브 계층 (신규: n8n, Docker 1대)                         │
│                                                                    │
│   Webhook 수신 → Next Agent 필드로 분기(Switch)                    │
│   → (선택) Slack 승인 버튼 → 워커 호출                              │
│   → 실패 시 ai-failed 라벨 + Slack 알림                            │
└───────────────────────────┬──────────────────────────────────────┘
                            │ Execute Command / SSH / HTTP
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  ③ AI 워커 계층 (신규: 공용 리눅스 서버)                             │
│                                                                    │
│   run_agent.sh <agent> <issue_key>                                 │
│    ├─ claude -p ...      (Claude Code headless)                    │
│    ├─ codex exec ...     (Codex CLI 비대화 모드)                    │
│    └─ gemini -p ...      (Gemini CLI 비대화 모드)                   │
└───────────────────────────┬──────────────────────────────────────┘
                            │ MCP (공통 mcp.json)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│  ④ MCP 공통 계층                                                   │
│                                                                    │
│   Atlassian 원격 MCP 서버  → JIRA 이슈/코멘트/상태, Confluence      │
│   GitHub MCP 서버          → 저장소, PR, 이슈                       │
└──────────────────────────────────────────────────────────────────┘

작업 완료 → AI가 MCP로 JIRA 상태 전환 → 다시 ①의 신호 발생 → 체인 반복
```

### 2.1 인계 루프 (티켓 생애주기)

1. AI(또는 사람)가 작업 완료: 커밋/PR/문서 + **Handoff 코멘트** 작성
2. JIRA 상태를 `Ready for AI`로 전환, `Next Agent` 필드 지정
3. JIRA Automation이 이벤트 허브(n8n)로 웹훅 발송
4. 허브가 `Next Agent` 값으로 분기, (선택) Slack 승인
5. 해당 AI 워커 실행 → MCP로 티켓/코드 컨텍스트 로드 → 작업 수행
6. 완료 시 1번으로 복귀 (체인 지속)

---

## 3. 구성요소 상세

### 3.1 JIRA

| 항목 | 설정 |
|---|---|
| 커스텀 필드 `Next Agent` | Single Select: `claude` / `codex` / `gemini` / `human` |
| 커스텀 필드 `AI Hop Count` | Number, 자동 인계 횟수 카운터 (폭주 방지용, 선택) |
| 워크플로 상태 `Ready for AI` | 사람 검토용 `Done`과 분리된 자동 인계 신호 상태 |
| Automation 규칙 | `Ready for AI` 전환 시 허브로 웹훅 POST |

### 3.2 이벤트 허브 (n8n)

- self-hosted n8n, Docker Compose로 1 컨테이너 운영
- 워크플로: `Webhook → IF(Hop Count 검사) → Switch(Next Agent) → [Slack 승인] → Execute/SSH → 에러 처리`

### 3.3 AI 워커

- 공용 리눅스 서버 1대 (Ubuntu 22.04+ 권장, Node.js 20+)
- 세 AI CLI 설치 + 대상 Git 저장소 클론 + 래퍼 스크립트 `run_agent.sh`
- AI별 서비스 계정: `ai-claude@…`, `ai-codex@…`, `ai-gemini@…` (JIRA/Git 이력 추적용)

### 3.4 MCP 공통 설정

- `mcp.json` 하나를 Git 저장소(`agent-config` 리포)로 버전 관리
- 연결 대상: Atlassian 원격 MCP 서버, GitHub MCP 서버

### 3.5 인계 컨텍스트 패키지 (Handoff 코멘트)

모든 AI의 규칙 파일(CLAUDE.md / AGENTS.md / GEMINI.md)에 동일 템플릿을 강제:

```markdown
## Handoff
- 완료한 것: (요약 3줄 이내)
- 산출물: (커밋 해시 / PR 링크 / Confluence 페이지 링크)
- 다음 작업: (다음 AI가 해야 할 일, 구체적으로)
- 제약/주의: (건드리면 안 되는 것, 실패했던 접근)
- Next Agent: codex
```

> 기준: **다음 워커가 이 코멘트 하나만 읽어도 착수할 수 있어야 한다.**

---

## 4. 설치 가이드

> 아래 순서대로 진행하면 됩니다. 예상 소요: 총 3~5일 (파일럿 기준).
> 서드파티 CLI(Codex, Gemini)의 옵션명은 버전에 따라 다를 수 있으니 각 공식 문서의 최신 내용을 함께 확인하세요.

### 4.0 사전 준비

- [ ] 공용 리눅스 서버 1대 (2 vCPU / 4GB RAM 이상, Docker 설치 가능)
- [ ] JIRA/Confluence 관리자 권한 (커스텀 필드, Automation 생성)
- [ ] AI별 서비스 계정 3개 (JIRA + GitHub), 최소 권한 부여
- [ ] API 자격 증명:
  - Anthropic: Claude 구독 또는 API 키 (`claude setup-token`으로 CI용 장기 토큰 발급 가능)
  - OpenAI: Codex 사용 가능한 계정/API 키
  - Google: Gemini CLI 인증 (Google 계정 또는 API 키)
  - GitHub: MCP용 Personal Access Token (repo 범위, AI 계정별 발급)
- [ ] Slack Incoming Webhook 또는 Slack App (승인 버튼용, 선택)

---

### 4.1 단계 1 — JIRA 설정 (약 반나절)

#### 4.1.1 커스텀 필드 생성

1. JIRA 관리 → 이슈 → 사용자 정의 필드 → **필드 만들기**
2. `Next Agent`: Select List (single choice), 옵션 `claude`, `codex`, `gemini`, `human`
3. (선택) `AI Hop Count`: Number Field, 기본값 0
4. 두 필드를 대상 프로젝트의 화면(Screen)에 추가
5. 필드 ID 확인: `https://<your-domain>.atlassian.net/rest/api/3/field` 에서 `customfield_XXXXX` 값 메모

#### 4.1.2 워크플로 상태 추가

1. 프로젝트 워크플로 편집 → 상태 `Ready for AI` 추가
2. 전환(Transition): `In Progress → Ready for AI`, `In Review → Ready for AI` 등 필요한 경로 연결

#### 4.1.3 Automation 규칙 생성

프로젝트 설정 → Automation → **규칙 만들기**:

- **트리거**: Issue transitioned → To status: `Ready for AI`
- **조건**: `Next Agent` is not empty AND `Next Agent` != `human`
- **액션**: Send web request
  - URL: `https://<n8n-host>/webhook/ai-handoff`
  - Method: `POST`, Content-Type: `application/json`
  - Body (custom data):

```json
{
  "issueKey": "{{issue.key}}",
  "summary": "{{issue.summary}}",
  "nextAgent": "{{issue.customfield_XXXXX}}",
  "hopCount": "{{issue.customfield_YYYYY}}",
  "issueUrl": "{{issue.url}}"
}
```

- (권장) Headers에 공유 시크릿 추가: `X-Handoff-Token: <랜덤 문자열>` — n8n에서 검증

#### 4.1.4 Git → JIRA 신호 일원화

- GitHub for Jira 앱 설치(Atlassian Marketplace) 후 저장소 연결
- PR 머지 시 자동 전환: Automation 규칙 추가 — 트리거 "Pull request merged" → 액션 "Transition issue to `Ready for AI`"
- 또는 스마트 커밋 사용: 커밋 메시지에 `PROJ-123 #ready-for-ai` (전환 이름은 워크플로에 맞게)

---

### 4.2 단계 2 — 이벤트 허브(n8n) 설치 (약 1일)

#### 4.2.1 Docker Compose로 n8n 기동

서버에서:

```bash
mkdir -p /opt/n8n && cd /opt/n8n
cat > docker-compose.yml << 'EOF'
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=n8n.your-domain.com
      - WEBHOOK_URL=https://n8n.your-domain.com/
      - GENERIC_TIMEZONE=Asia/Seoul
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=<강력한 비밀번호>
    volumes:
      - n8n_data:/home/node/.n8n
      # 워커 스크립트를 컨테이너에서 실행할 경우 마운트
      - /opt/agents:/opt/agents:ro
volumes:
  n8n_data:
EOF
docker compose up -d
```

- 외부에서 JIRA 웹훅을 받아야 하므로 HTTPS 리버스 프록시(nginx/Caddy) + 도메인 구성 권장
- 사내망만 쓸 경우 JIRA Cloud는 외부 → 서버 접근이 필요하므로 방화벽에서 Atlassian IP만 허용

#### 4.2.2 n8n 워크플로 구성

n8n UI(`https://n8n.your-domain.com`)에서 새 워크플로 생성, 노드를 순서대로 연결:

1. **Webhook 노드**
   - HTTP Method: POST, Path: `ai-handoff`
   - (권장) 헤더 `X-Handoff-Token` 검증용 IF 노드를 바로 뒤에 배치
2. **IF 노드 — 폭주 방지**
   - 조건: `{{$json.hopCount}} < 5` → true만 통과
   - false 경로: Slack 알림 "자동 인계 상한 도달, 사람 확인 필요"
3. **Switch 노드**
   - 기준: `{{$json.nextAgent}}` → 케이스 `claude` / `codex` / `gemini`
4. **(선택) Slack 승인 노드**
   - "Send and Wait for Response" 유형 사용: `PROJ-123 → codex 인계 대기` 메시지 + [승인]/[보류] 버튼
   - 승인 시에만 다음 노드로 진행
5. **Execute Command 노드** (워커가 같은 서버일 때)
   - Command: `/opt/agents/run_agent.sh {{$json.nextAgent}} {{$json.issueKey}}`
   - 워커가 별도 서버면 SSH 노드 또는 HTTP Request 노드로 대체
6. **에러 처리 (Error Trigger 워크플로)**
   - 실패 시: JIRA REST API로 `ai-failed` 라벨 추가 + Slack 알림

워크플로 활성화(Activate) 후, JIRA에서 테스트 티켓을 `Ready for AI`로 전환해 웹훅 수신을 확인합니다.

---

### 4.3 단계 3 — AI CLI 설치 (약 반나절)

공용 서버에서 (Node.js 20+ 필요):

```bash
# Node.js 20 설치 (없을 경우)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs git jq

# 1) Claude Code
npm install -g @anthropic-ai/claude-code
# 인증: 대화형 최초 1회 로그인 또는 CI용 장기 토큰 발급
claude setup-token   # 발급된 토큰을 환경변수/시크릿으로 보관

# 2) Codex CLI (OpenAI)
npm install -g @openai/codex
codex login          # 또는 OPENAI_API_KEY 환경변수 설정

# 3) Gemini CLI (Google)
npm install -g @google/gemini-cli
gemini               # 최초 1회 대화형 인증, 또는 GEMINI_API_KEY 설정
```

설치 확인:

```bash
claude --version && codex --version && gemini --version
```

> 참고 문서
> - Claude Code: https://docs.claude.com/en/docs/claude-code/overview
> - Codex CLI / Gemini CLI는 각 공식 저장소의 최신 설치 문서를 확인하세요.

---

### 4.4 단계 4 — MCP 공통 설정 (약 반나절)

#### 4.4.1 공통 mcp.json 작성

설정 전용 Git 저장소(예: `agent-config`)를 만들고 다음 파일을 관리합니다.

`/opt/agents/mcp.json`:

```json
{
  "mcpServers": {
    "atlassian": {
      "type": "sse",
      "url": "https://mcp.atlassian.com/v1/sse"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
      }
    }
  }
}
```

- Atlassian 원격 MCP 서버는 최초 연결 시 OAuth 브라우저 인증이 필요합니다. 서버 환경에서는 각 AI 계정으로 1회 인증을 완료해 두세요.
- GitHub MCP는 공식 원격 서버(`https://api.githubcopilot.com/mcp/` 등) 또는 로컬 서버 중 팀 정책에 맞는 쪽을 선택합니다.
- 토큰은 파일에 직접 쓰지 말고 환경변수/시크릿 매니저로 주입합니다.

#### 4.4.2 각 AI에 동일 설정 연결

```bash
# Claude Code: 실행 시 --mcp-config 로 주입 (아래 워커 스크립트 참고)
claude -p "..." --mcp-config /opt/agents/mcp.json

# Codex: ~/.codex/config.toml 의 [mcp_servers] 섹션에 동일 서버 등록
# Gemini CLI: ~/.gemini/settings.json 의 "mcpServers" 에 동일 서버 등록
```

세 도구 모두 MCP 표준을 따르므로 서버 정의(URL/command)는 동일하게 재사용하고, 파일 형식만 각 도구에 맞게 변환합니다. 변환된 설정 파일 3종도 `agent-config` 저장소에 함께 커밋해 두세요.

---

### 4.5 단계 5 — 워커 래퍼 스크립트 (약 1일)

#### 4.5.1 디렉토리 구조

```
/opt/agents/
├── mcp.json              # MCP 공통 설정
├── run_agent.sh          # 허브가 호출하는 진입점
├── prompts/
│   └── handoff.md        # 공통 작업 지시 템플릿
├── workspaces/           # AI별 작업 디렉토리 (저장소 클론)
│   ├── claude/
│   ├── codex/
│   └── gemini/
└── logs/
```

#### 4.5.2 run_agent.sh

```bash
#!/bin/bash
set -euo pipefail

AGENT="$1"          # claude | codex | gemini
ISSUE="$2"          # 예: PROJ-123
BASE=/opt/agents
WORKDIR="$BASE/workspaces/$AGENT/repo"
LOG="$BASE/logs/$(date +%Y%m%d-%H%M%S)-$AGENT-$ISSUE.log"

PROMPT="당신은 팀의 자동화 에이전트다.
1. MCP(atlassian)로 JIRA 티켓 ${ISSUE} 를 조회하고, 최신 'Handoff' 코멘트를 읽어라.
2. 코멘트의 '다음 작업'을 수행하라. 코드 작업은 새 브랜치 ${ISSUE}-${AGENT} 에서 하고,
   완료 후 커밋과 PR 을 생성하라. main 에 직접 push 하지 마라.
3. 완료하면 동일한 Handoff 템플릿으로 결과 코멘트를 남기고,
   후속 작업이 있으면 상태를 'Ready for AI' 로, 사람 검토가 필요하면 'In Review' 로 전환하라.
4. 30분 안에 끝낼 수 없거나 지시가 불명확하면, 작업을 멈추고
   질문 코멘트를 남긴 뒤 상태를 그대로 두어라."

cd "$WORKDIR"
git fetch origin && git checkout main && git pull

case "$AGENT" in
  claude)
    claude -p "$PROMPT" \
      --mcp-config "$BASE/mcp.json" \
      --allowedTools "Bash,Read,Edit,Write,mcp__atlassian,mcp__github" \
      --permission-mode acceptEdits \
      --output-format json > "$LOG" 2>&1
    ;;
  codex)
    codex exec "$PROMPT" > "$LOG" 2>&1
    ;;
  gemini)
    gemini -p "$PROMPT" --yolo > "$LOG" 2>&1
    ;;
  *)
    echo "unknown agent: $AGENT" >&2; exit 1;;
esac

echo "done: $AGENT $ISSUE (log: $LOG)"
```

```bash
chmod +x /opt/agents/run_agent.sh
```

주의사항:

- `--permission-mode acceptEdits`, `--yolo` 등 자동 승인 옵션은 **격리된 작업 디렉토리 + 최소 권한 계정**을 전제로만 사용하세요.
- 타임아웃을 원하면 `timeout 30m` 으로 감싸고, 초과 시 n8n 에러 경로에서 `ai-failed` 처리합니다.
- 로그는 최소 30일 보관을 권장합니다 (감사/디버깅용).

#### 4.5.3 수동 테스트

```bash
# 테스트 티켓 PROJ-1 을 만들고 Handoff 코멘트를 단 뒤:
/opt/agents/run_agent.sh claude PROJ-1
# JIRA 코멘트/상태와 Git 브랜치 생성 여부 확인
```

---

### 4.6 단계 6 — 에이전트 규칙 파일 배포 (약 반나절)

각 작업 저장소 루트에 동일 내용의 규칙 파일을 둡니다.

- Claude Code: `CLAUDE.md`
- Codex: `AGENTS.md`
- Gemini CLI: `GEMINI.md`

공통 내용 예시:

```markdown
# 팀 자동화 에이전트 공통 규칙

## 인계 규칙
- 작업 완료 시 반드시 아래 Handoff 템플릿으로 JIRA 코멘트를 남긴다.
- 후속 AI 작업이 있으면 Next Agent 필드를 지정하고 상태를 'Ready for AI'로 전환한다.
- 사람 검토가 필요하면 상태를 'In Review'로 전환하고 Next Agent 를 'human'으로 둔다.

## Handoff 템플릿
(3.5절 템플릿 동일 삽입)

## 금지 사항
- main 브랜치 직접 push 금지 (항상 브랜치 + PR)
- 티켓 범위 밖 파일 수정 금지
- 비밀키/토큰을 코드나 코멘트에 기록 금지
```

---

## 5. 운영 규칙

### 5.1 승인 게이트 정책

| 단계 | 정책 |
|---|---|
| 도입 초기 (1~4주) | 모든 인계에 Slack 승인 버튼 필수 |
| 안정화 (5주~) | 저위험 작업 유형(코드 리뷰, 테스트 작성, 문서화)만 자동 실행 |
| 성숙 | 티켓 라벨(`auto-ok`)로 자동 실행 여부를 티켓 단위 제어 |

### 5.2 실패/예외 처리

- 워커 비정상 종료 → `ai-failed` 라벨 + Slack 알림 + 상태 유지 (자동 재시도 금지, 사람이 판단)
- AI가 지시 불명확 판단 → 질문 코멘트 후 정지 (프롬프트에 명시됨)
- 자동 인계 5회 초과 → 허브에서 차단, 사람 확인

### 5.3 보안

- AI별 서비스 계정 분리, JIRA는 해당 프로젝트만, GitHub는 PR 권한만
- 웹훅에 공유 시크릿 헤더 검증, n8n은 HTTPS + Basic Auth 이상
- API 키/토큰은 환경변수 또는 시크릿 매니저로만 관리, 저장소 커밋 금지
- 워커 서버는 팀 외 접근 차단, 로그에 토큰이 남지 않는지 주기 점검

---

## 6. 도입 로드맵

| 주차 | 목표 | 산출물 |
|---|---|---|
| 1주차 | JIRA 필드/워크플로/Automation + n8n 설치, **Slack 알림까지만** | 인계 발생 즉시 알림 (자동 실행 없음) |
| 2~3주차 | AI CLI + MCP 공통 설정 + 워커 구축, Slack 승인 후 실행 (반자동) | 첫 AI-to-AI 인계 파일럿 1건 |
| 4주차~ | 저위험 작업 유형부터 승인 생략, 인계 상한/모니터링 정착 | 완전 자동 체인 (제한적) |

## 7. 설치 체크리스트

- [ ] JIRA: `Next Agent`, `AI Hop Count` 필드 + `Ready for AI` 상태 + Automation 규칙
- [ ] Git↔JIRA 연동 (PR 머지 → 상태 전환)
- [ ] n8n Docker 기동 + HTTPS + 웹훅 시크릿
- [ ] n8n 워크플로: Webhook → Hop 검사 → Switch → 승인 → 실행 → 에러 처리
- [ ] 서버에 Claude Code / Codex / Gemini CLI 설치 및 인증
- [ ] `mcp.json` 작성 + 3개 AI에 동일 서버 연결 + `agent-config` 저장소 커밋
- [ ] `run_agent.sh` 배치 + 수동 테스트 통과
- [ ] `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` 규칙 파일 배포
- [ ] 테스트 티켓으로 엔드투엔드 인계 1회 성공
- [ ] 운영 규칙(승인/실패/보안) 팀 공유 및 Confluence 게시

---

## 부록 A. 참고 링크

- Claude Code 문서: https://docs.claude.com/en/docs/claude-code/overview
- Claude Code headless 모드: https://code.claude.com/docs/en/headless
- Atlassian 원격 MCP 서버: Atlassian 공식 문서에서 "Remote MCP Server" 검색
- n8n 셀프호스팅: https://docs.n8n.io
- MCP(Model Context Protocol) 사양: https://modelcontextprotocol.io

## 부록 B. 용어

| 용어 | 설명 |
|---|---|
| MCP | Model Context Protocol. AI가 외부 도구(JIRA, GitHub 등)에 표준 방식으로 접근하는 프로토콜 |
| 이벤트 허브 | 웹훅을 받아 라우팅/승인/실행을 담당하는 자동화 계층 (본 구성에서는 n8n) |
| Handoff 코멘트 | AI 간 인계 시 남기는 정형화된 컨텍스트 패키지 |
| Hop Count | 하나의 티켓에서 자동 인계가 연쇄된 횟수 (폭주 방지 상한 기준) |
