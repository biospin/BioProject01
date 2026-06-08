# Atlassian MCP Setup

이 문서는 Claude Code와 OpenClaw에서 Jira / Confluence 작업을 하기 위한 Atlassian MCP 설정 절차다.

목표:
- Jira: `BIOP01`, `BIOP02` issue 조회 / 업데이트
- Confluence: `VC` space 문서 조회 / 정리
- 토큰은 repo 밖에 보관하고, `/tmp`를 쓰지 않는다

## 현재 권장 방식

Atlassian API token은 홈 디렉터리의 비공개 파일에 저장하고, MCP 실행은 wrapper script로 통일한다.

```text
~/.config/atlassian/api-token      # API token, chmod 600
~/.local/bin/atlassian-mcp         # Claude / OpenClaw 공용 wrapper
```

`/tmp`는 OS cleanup, 재부팅, 앱 세션 변화로 삭제될 수 있으므로 장기 설정에 쓰지 않는다.

## 준비물

- Atlassian site URL: `https://biospin-ai.atlassian.net`
- Atlassian login email
- Atlassian API token

API token 발급 위치:

```text
https://id.atlassian.com/manage-profile/security/api-tokens
```

## Token 파일 생성

```bash
mkdir -p ~/.config/atlassian
chmod 700 ~/.config/atlassian

nano ~/.config/atlassian/api-token
chmod 600 ~/.config/atlassian/api-token
```

파일에는 API token 문자열만 한 줄로 넣는다. email이나 URL은 넣지 않는다.

확인:

```bash
ls -l ~/.config/atlassian/api-token
```

권한은 아래처럼 본인만 읽기/쓰기여야 한다.

```text
-rw------- ... ~/.config/atlassian/api-token
```

## Wrapper script 생성

```bash
mkdir -p ~/.local/bin
nano ~/.local/bin/atlassian-mcp
chmod 700 ~/.local/bin/atlassian-mcp
```

`YOUR_EMAIL@example.com`을 본인 Atlassian login email로 바꾼다.

```bash
#!/usr/bin/env bash
set -euo pipefail

export ATLASSIAN_URL="https://biospin-ai.atlassian.net"
export ATLASSIAN_EMAIL="YOUR_EMAIL@example.com"
export ATLASSIAN_API_TOKEN="$(cat "$HOME/.config/atlassian/api-token")"

exec npx -y @atlassian/mcp-atlassian --transport stdio
```

간단 확인:

```bash
test -x ~/.local/bin/atlassian-mcp
```

## Claude Code 등록

```bash
claude mcp add atlassian ~/.local/bin/atlassian-mcp
claude mcp list
```

정상 상태에서는 `atlassian` server가 목록에 보여야 한다. Claude Code 안에서는 `/mcp`로 연결 상태와 인증 오류를 확인할 수 있다.

## OpenClaw 등록

OpenClaw도 같은 wrapper script를 사용한다.

```bash
openclaw mcp set atlassian '{
  "command": "/Users/kkkim/.local/bin/atlassian-mcp",
  "args": []
}'

openclaw mcp list
openclaw mcp show atlassian
```

OpenClaw agent 또는 channel bridge가 MCP server를 다시 읽어야 하는 경우 OpenClaw 세션을 재시작한다.

## 동작 확인

Claude Code에서 확인할 예시:

```text
BIOP01-11 Jira issue를 읽고 title, status, assignee, description을 요약해줘.
```

OpenClaw에서 확인할 예시:

```text
Atlassian MCP를 사용해서 BIOP01 프로젝트에서 나에게 할당된 open issue를 찾아줘.
```

실제 issue 수정, comment 작성, transition 변경은 consequential action이므로 실행 전 내용을 확인하고 진행한다.

## Codex에서의 상태

현재 Codex 앱 directory에는 `Atlassian Rovo`가 보일 수 있지만, `isAccessible: false`이면 Codex 세션에는 Jira tool이 노출되지 않는다. 이 경우 Codex는 Jira를 직접 읽을 수 없고, Claude / OpenClaw MCP 또는 사용자가 붙여준 issue 내용에 의존한다.

Codex 런타임이 로컬 MCP server 로드를 지원하도록 바뀌면, 같은 `~/.local/bin/atlassian-mcp` wrapper를 재사용한다.

## Troubleshooting

### `No MCP servers configured`

Claude:

```bash
claude mcp list
```

OpenClaw:

```bash
openclaw mcp list
```

둘 중 필요한 쪽에 다시 등록한다.

### Token 파일이 없어짐

`/tmp/oc-atlassian.txt` 같은 임시 경로를 썼다면 삭제될 수 있다. 새 token을 발급하거나 기존 token을 다시 `~/.config/atlassian/api-token`에 넣는다.

### 인증 실패

확인 항목:

- `ATLASSIAN_EMAIL`이 Atlassian login email과 같은지
- API token이 revoke되지 않았는지
- `ATLASSIAN_URL`이 `https://biospin-ai.atlassian.net`인지
- token 파일 끝에 불필요한 공백이나 여러 줄이 없는지

### `npx` 다운로드 실패

네트워크 또는 npm registry 접근 문제일 수 있다. 한 번 수동 실행해서 package 설치 / 다운로드가 가능한지 확인한다.

```bash
~/.local/bin/atlassian-mcp
```

MCP server는 stdio로 대기하므로 정상 실행 시 터미널에 오래 머물 수 있다. 종료는 `Ctrl-C`.

## 보안 원칙

- API token은 repo 안에 저장하지 않는다.
- API token을 issue, markdown, prompt, screenshot에 붙이지 않는다.
- token 파일 권한은 `600`, token directory 권한은 `700`을 유지한다.
- token이 노출됐다고 의심되면 Atlassian profile에서 즉시 revoke하고 새로 발급한다.
