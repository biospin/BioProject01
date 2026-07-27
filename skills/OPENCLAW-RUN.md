# OpenClaw 실행 노트 — HSPC 하네스 (2026-07-01 시연·검증)

> `AGENTS.md`+`skills/`는 OpenClaw/Codex 네이티브 포맷. 이 문서는 실제 OpenClaw로
> 돌리는 방법과 현재 환경의 블로커를 기록한다. (CLAUDE.md: OpenClaw 기반 실행 기본 감안)

## 검증 완료 (구조 — OpenClaw-native 유효)
- `openclaw` CLI 설치 확인: **OpenClaw 2026.5.7** (`~/.nvm/.../bin/openclaw`). `codex`도 설치됨.
- `skills/ROUTES.md` 라우팅: dataset(4종) → task(download/preprocessing/model/visualization) 테이블 정상.
- HSPC 4개 `agents/openai.yaml` 전부 파싱 OK(`interface.display_name`/`default_prompt` 유효):
  Download / Preprocessing / Model / Visualization.
- `skills/human-hspc-10x-multiome/download/SKILL.md` frontmatter(name/description) 정상 → `pipeline/hspc-velocity-benchmark/` 실행 구현과 연결.

## 실행 커맨드 (provider 설정 후 그대로 사용)
```bash
cd ~/project/BioProject01
# openai.yaml의 default_prompt를 그대로 사용
PROMPT=$(python3 -c "import yaml; print(yaml.safe_load(open(
  'skills/human-hspc-10x-multiome/download/agents/openai.yaml'))['interface']['default_prompt'])")

openclaw agent --local --session-id hspc-openclaw-demo -m "$PROMPT"
#   --local   : gateway 대신 임베디드 에이전트(= shell의 provider 키 필요)
#   --session-id : 세션 지정 필수(없으면 "Pass --to/--session-id/--agent" 에러)
#   task 바꾸려면 경로만 교체: download → preprocessing/model/visualization
```

## ⚠️ 현재 블로커 (이 환경) — provider 미설정
- `openclaw agent --local` turn이 **완료되지 못하고 kill됨**(60s 하드 타임아웃, exit 137).
- 원인: shell에 `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` **없음** + `~/.openclaw/`에 provider/auth config **없음**(`plugins/installs.json`만 존재). `openclaw capability`/gateway 호출도 hang.
- 즉 **하네스 결함이 아니라 실행 환경의 provider auth 미설정**. 아래 셋 중 하나 갖추면 실행 가능:
  1. shell에 provider 키 export 후 `--local` (가장 간단), 또는
  2. `openclaw` gateway에 provider 등록 후 `openclaw agent`(--local 없이), 또는
  3. `codex`(동일 openai.yaml 포맷)로 실행.

## 다음
- provider 키 확보 시 위 커맨드로 download → preprocessing 순 실제 turn 시연.
- Codex 경로도 동일 `openai.yaml`이라 병행 검증 가능.
