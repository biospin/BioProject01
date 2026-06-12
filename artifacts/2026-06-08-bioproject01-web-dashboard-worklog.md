# 2026-06-08 BioProject01 Web Dashboard Worklog

## Purpose

BioProject01의 논문 분석 하네스는 원래 CLI와 Codex prompt 중심으로 동작했다. 오늘 작업의 목적은 팀원이 브라우저에서 클릭 기반으로 논문 분석 요청을 만들고, Codex 실행 상태와 산출물을 확인하고, 분석 결과를 바로 열어볼 수 있게 만드는 것이었다.

## Final State

- Local dashboard: `web/app.py`
- Browser UI: `web/index.html`, `web/static/app.js`, `web/static/app.css`
- Dashboard docs: `web/README.md`, `web/DEPLOY.md`
- LAN sharing script: `web/scripts/share_dashboard.sh`
- Dashboard banner image: `web/static/images/bioproject01-dashboard-hero.png`
- Run records: `artifacts/web-runs/<run-id>/`
- Harness routing: `AGENTS.md` `Web Dashboard Workflow`
- Artifact map: `artifacts/README.md`

## Work Completed

### 1. Codex Startup Warning Cleanup

Initial Codex startup showed repeated plugin skill YAML errors and an unauthorized Atlassian MCP startup failure.

Actions:

- Fixed invalid YAML frontmatter in affected `agent-workbench` skill `SKILL.md` files.
- Disabled or commented the unauthorized Atlassian MCP entry in the Codex config so startup does not stall on failed handshake.

Result:

- Codex startup became quieter and the BioProject01 work could proceed without unrelated plugin/MCP warnings blocking attention.

### 2. Click-Based Dashboard Scaffold

Created a stdlib Python web server under `web/app.py`.

Core routes:

- `/` serves the dashboard.
- `/static/...` serves CSS, JS, and image assets.
- `/api/papers` lists `analysis/<topic>/<paper-id>/paper-info.yaml`.
- `/api/runs` lists dashboard-created run requests.
- `/api/run/new` creates `artifacts/web-runs/<run-id>/request.json` and `prompt.md`.
- `/api/run/build-index` runs `skills/source-grounding/scripts/build_index.py`.
- `/api/run/render-html` runs `skills/core-to-html/scripts/build_html.py <paper-dir>`.
- `/api/run/start-codex` starts `codex exec --cd <repo> -` with the saved `prompt.md`.
- `/api/run/codex-status` returns job status, log tail, and detected output files.
- `/view/html?paper_path=<paper-dir>` opens rendered core HTML.
- `/view/core?path=<core-md>` opens a browser-readable rendered view of `*_core.md`.

### 3. Run Prompt Workflow

The dashboard now creates a paper-analysis request from browser form fields:

- Source: DOI, URL, or PDF path.
- Topic.
- Mode: full, abstract-only, core-only, question.
- Lens: both, academic, industry, none.
- Notes.

Each request is stored in:

```text
artifacts/web-runs/<run-id>/
  request.json
  prompt.md
```

The prompt follows the project `AGENTS.md` Quick Start and Full Paper Workflow.

### 4. Run In Codex

Added `Run in Codex` button.

Behavior:

1. Reads the active run's `prompt.md`.
2. Starts:

   ```bash
   codex exec --cd /Users/kkkim/projects/autobiox/BioProject01 -
   ```

3. Writes:

   ```text
   artifacts/web-runs/<run-id>/codex-job.json
   artifacts/web-runs/<run-id>/codex.log
   ```

4. Tracks status as `running`, `succeeded`, `failed`, `finished-unknown`, `not-started`, or `invalid-status`.

Special case:

- If the dashboard server restarts while Codex is running, the old process handle is lost. The dashboard checks whether the PID is still alive. If not, it marks the job as `finished-unknown` and asks the user to inspect `codex.log` and generated outputs.

### 5. Status UX Improvement

The first version made it hard to tell whether `Run in Codex` had actually run.

Changed UI:

- The bottom `실행 요청 텍스트` panel now shows:
  - status card,
  - generated-file badges,
  - Codex log tail.
- The old black `작업 로그` was renamed to `시스템 로그` and restyled as a secondary light log.

Generated-file detection checks for:

- `paper-info.yaml`
- `core.md`
- `academic lens`
- `industry lens`
- `methodology brief`
- `core.html`

### 6. Trevino Test Run

Test request:

```text
Source: 10.1016/j.cell.2021.07.039
Topic: single-cell-genomics
Mode: full
Lens: both
```

Detected output folder:

```text
analysis/single-cell-genomics/trevino-2021-cortex
```

Detected outputs:

- `paper-info.yaml`
- `trevino-2021-cortex_core.md`
- `trevino-2021-cortex_lens-academic.md`
- `trevino-2021-cortex_lens-industry.md`
- `trevino-2021-cortex_methodology-brief.md`
- `trevino-2021-cortex_core.html`

Known limitation:

- The run was source-limited because the local environment could not download the Cell PDF. The analysis preserved this boundary and marked PDF-dependent details as `검토필요` or `미제공`.

### 7. Render HTML And View Core

The first dashboard version rendered HTML but did not open it directly.

Final behavior:

- `Render HTML` runs the HTML build script and opens `/view/html?paper_path=<paper-dir>` in a new tab.
- `View Core` opens `/view/core?path=<core-md>` in a new tab.
- `View Core` no longer shows raw Markdown in a `<pre>` block. It renders Markdown into readable HTML with headings, lists, bold text, code spans, code blocks, blockquotes, and tables.

### 8. Deployment Path

Local use:

```bash
python3 web/app.py --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

Team LAN sharing:

```bash
BIOP01_DASHBOARD_TOKEN='change-this-token' python3 web/app.py --host 0.0.0.0 --port 8765
```

Convenience script:

```bash
./web/scripts/share_dashboard.sh
```

Teammates enter the token in the `Team token` field.

## Verification Commands

Syntax checks:

```bash
python3 -c "from pathlib import Path; compile(Path('web/app.py').read_text(), 'web/app.py', 'exec')"
node --check web/static/app.js
```

Run server:

```bash
python3 web/app.py --port 8765
```

Check Core view:

```bash
curl -s 'http://127.0.0.1:8765/view/core?path=analysis%2Fsingle-cell-genomics%2Ftrevino-2021-cortex%2Ftrevino-2021-cortex_core.md'
```

Check HTML view:

```bash
curl -s 'http://127.0.0.1:8765/view/html?paper_path=analysis%2Fsingle-cell-genomics%2Ftrevino-2021-cortex'
```

Check run status:

```bash
curl -s 'http://127.0.0.1:8765/api/run/codex-status?run_path=artifacts/web-runs/<run-id>'
```

## Reproduce From Scratch

1. Start from the BioProject01 repo:

   ```bash
   cd /Users/kkkim/projects/autobiox/BioProject01
   ```

2. Ensure the dashboard files exist:

   ```text
   web/app.py
   web/index.html
   web/static/app.js
   web/static/app.css
   web/README.md
   web/DEPLOY.md
   web/scripts/share_dashboard.sh
   artifacts/README.md
   ```

3. Run checks:

   ```bash
   python3 -c "from pathlib import Path; compile(Path('web/app.py').read_text(), 'web/app.py', 'exec')"
   node --check web/static/app.js
   ```

4. Start the dashboard:

   ```bash
   python3 web/app.py --port 8765
   ```

5. In the browser, create a run:

   ```text
   Source: 10.1016/j.cell.2021.07.039
   Topic: single-cell-genomics
   Mode: full
   Lens: both
   ```

6. Click `Create Run Prompt`.
7. Click `Run in Codex`.
8. Watch the status card, generated-file badges, and Codex log in the same bottom panel.
9. After outputs appear, click `Build Index`.
10. In `분석된 자료`, click `Render HTML` to rebuild and open the HTML report.
11. Click `View Core` to open the readable core analysis view.

## Harness Registration Check

Registered:

- `AGENTS.md` now routes web/click/team-deploy requests to `web/`.
- `AGENTS.md` documents `Run in Codex`, status checking, generated-file badges, `Render HTML`, and `View Core`.
- `artifacts/README.md` maps dashboard run outputs and today documentation.
- `web/README.md` documents usage.
- `web/DEPLOY.md` documents team distribution.

Not changed:

- The dashboard does not replace the paper analysis skills.
- Source grounding, core analysis, lens analysis, methodology brief, index rebuild, and HTML rendering still follow the existing `skills/` contracts.
- Human review is still required before treating source-limited analysis as full paper-grounded analysis.

## Files Changed Or Added

Primary dashboard:

- `web/app.py`
- `web/index.html`
- `web/static/app.js`
- `web/static/app.css`
- `web/static/images/bioproject01-dashboard-hero.png`
- `web/README.md`
- `web/DEPLOY.md`
- `web/scripts/share_dashboard.sh`

Harness and artifacts:

- `AGENTS.md`
- `artifacts/README.md`
- `artifacts/web-runs/`
- `artifacts/2026-06-08-bioproject01-web-dashboard-worklog.md`
- `artifacts/2026-06-08-bioproject01-web-dashboard-presentation.md`

---

## 2026-06-09 Update — Claude Code Harness Port

### Purpose

논문 분석 하네스는 원래 Codex CLI 네이티브였다(`AGENTS.md` 라우터 + `skills/*/SKILL.md` + `skills/*/agents/openai.yaml`). 오늘 작업은 **동일 하네스를 Claude Code에서도 네이티브로 실행**할 수 있게 포팅하고, Claude에서 분석 1건을 재실행해 Codex 산출물과 대조한 것이다. 분석 규칙의 single source of truth는 그대로 `AGENTS.md` + `skills/*/SKILL.md`다.

### Work Completed

1. **Skills 등록** — `skills/*/SKILL.md` 16개를 Claude가 자동 discover하도록 `.claude/skills/<name>/`에 배치. 웹(claude.ai/code = GitHub 체크아웃)에서도 동작하도록 심볼릭 링크가 아닌 **실제 복사본**으로 둔다. 원본 `skills/` 변경 시 `.claude/skills/`도 재동기화한다.
2. **Agent 레이어 포팅** — Codex `skills/*/agents/openai.yaml` 7개를 Claude subagent 형식 `.claude/agents/*.md`로 변환: `abstract-analysis`, `core-problem`(Full Background), `core-results`(Full Results), `core-figure`(Full Figure), `lens-academic`(Full Discussion), `full-slides`, `question`. 각 subagent는 해당 `SKILL.md` + `AGENTS.md` 라우터 + source-grounding 규칙을 읽고 작업한다. 나머지 skill(core-methods, core-table, lens-industry, methodology-brief, source-grounding, core-to-html, paper-scrapper, insight-agent, validation-agent)은 Codex에서도 agent-picker 항목이 아니라 skill 호출이므로 Claude에서도 skill로만 사용한다.
3. **CLAUDE.md 라우터 갱신** — "Claude Code 네이티브 실행 (Codex 하네스 포팅)" 섹션을 추가. `AGENTS.md`를 중복하지 않고 위임하며, 포팅 레이어의 위치와 재동기화 규칙만 명시.
4. **`.gitignore` 정책 변경** — `.claude/`는 per-machine 상태라 통째로 ignore돼 있었다. 웹/팀이 포팅 레이어를 받을 수 있도록 `.claude/*`로 바꾸고 `!.claude/skills/`, `!.claude/agents/`만 예외 처리. `settings*.json`과 `worktrees/`는 계속 per-machine으로 ignore.

### Re-run (Claude 재현)

Codex 6/8 run과 동일 paper(Trevino 2021, DOI 10.1016/j.cell.2021.07.039)를 포팅된 `abstract-analysis` skill + source-grounding 규칙으로 Claude에서 재실행.

- 출력: `analysis/single-cell-genomics/trevino-2021-cortex/claude-rerun/trevino-2021-cortex_abstract.md` (Codex 원본을 덮어쓰지 않고 비교용 별도 폴더).
- 근거: 로컬 `sources/abstract.txt` + `publisher_fulltext_excerpt.txt`만 사용. full PDF 미확보 경계는 Codex run과 동일하게 `검토필요:`로 표시.
- 대조 결과: 섹션 구조 동일(Abstract Summary / 추출 규칙 적용 / 후속 작업), source-grounding 표기(`해석:`, `외부 맥락:`, `검토필요:`) 적용, 핵심 사실(GSE162170, `GreenleafLab/Brain_ASD`) 일치.

### How To Use (web/new session)

`.claude/skills/`·`.claude/agents/`는 **세션 시작 시점에 로드**된다. 적용하려면 변경을 commit + push한 뒤, BioProject01 저장소(`kkkim-paper-agent`)로 **새 Claude 세션**을 연다. 그 세션에서 `DOI: ... 분석해줘` 한 줄이면 `AGENTS.md` Full Paper Workflow가 Claude에서 그대로 흐른다.

### Files Changed Or Added (Claude port)

- `.claude/skills/<16 skills>/` (committed 복사본)
- `.claude/agents/abstract-analysis.md`, `core-problem.md`, `core-results.md`, `core-figure.md`, `lens-academic.md`, `full-slides.md`, `question.md`
- `CLAUDE.md` (네이티브 실행 섹션)
- `.gitignore` (`.claude/skills`·`.claude/agents` 예외)
- `analysis/single-cell-genomics/trevino-2021-cortex/claude-rerun/trevino-2021-cortex_abstract.md` (재현 산출물)

### Dashboard UI/UX + Tutorial (Codex 미완료분 이어서)

Codex에서 "화면 UI/UX가 직관적이지 않다 → 튜토리얼/화면 재구성"으로 진행하다 토큰 부족으로 멈춘 작업을 Claude에서 이어 완료했다.

Codex에서 이미 들어와 있던 것(확인됨): 상단 3단계 가이드 카드(`자료 입력 → 분석 시작 → 결과 확인`), step pill로 번호화된 패널 재배치, 실행 상태 패널을 분석 목록 위로 이동, 한국어 버튼 문구(`요청 만들기`, `분석 시작`, `상태 새로고침`), 관련 CSS, 가이드 버튼의 `data-scroll-target` 스크롤 wiring. 단, `web/` 전체가 아직 commit되지 않은 untracked 상태였고 실제 인터랙티브 튜토리얼은 없었다.

Claude에서 추가한 것:

- **인터랙티브 튜토리얼** — 우측 하단 floating 카드로 6단계 가이드(둘러보기 → 자료 입력 → 옵션·요청 → 분석 실행 → 결과 확인 → 팀 공유/인덱스). 각 단계가 대응 화면 영역(`.panel`/`.workflow-guide`/`.topbar`)을 `tutorial-spot` outline으로 강조하고 scrollIntoView.
- 첫 방문 자동 오픈(`localStorage` `biop01_tutorial_seen`), 상단 `❓ 튜토리얼` 버튼으로 재실행, `다음`/`이전`·키보드 `→`/`←`·`Esc`/`건너뛰기`/`✕` 조작.
- `web/index.html`(튜토리얼 버튼 + 오버레이 markup), `web/static/app.css`(튜토리얼 스타일), `web/static/app.js`(`TUTORIAL_STEPS` + 제어 로직), `web/README.md`(Guided Tutorial 섹션) 갱신.

검증: `node --check web/static/app.js` 통과, 로컬 서버 기동 후 `/`가 튜토리얼 markup을 serve하고 `app.js`에 `TUTORIAL_STEPS`, `app.css`에 `tutorial-dialog` 포함 확인, `/api/papers`는 기존 9건 정상 반환(백엔드 무영향).

### Dashboard 실행 엔진에 Claude 추가

대시보드가 Codex만 호출하던 것을 Claude로도 실행하도록 연동했다.

- 백엔드(`web/app.py`): job 시스템을 engine-aware로 일반화. `ENGINES` 설정(codex/claude별 command·log·job 파일), `write/read_job_status(..., engine)`, `start_job(path, engine)`, `get_job(path, engine)`, `watch_job(..., engine)`. JOBS는 `<run_id>:<engine>` 키로 분리해 한 요청에 두 엔진 독립 실행. 라우트 `POST /api/run/start-claude`, `GET /api/run/claude-status` 추가(기존 codex 라우트 유지).
- Claude 실행: `claude -p --dangerously-skip-permissions` (prompt.md를 stdin으로, cwd=repo). codex와 동일하게 자율 실행. 기록은 `claude.log` / `claude-job.json`.
- 프론트(`web/index.html`, `web/static/app.js`): `Claude로 분석`(primary) + `Codex로 분석` 버튼, `state.engine`로 상태 polling·라벨을 엔진별 분기(`runEngine(engine)`, `refreshJob`, `renderJobStatus`). paper-row 자동 실행은 codex 기본 유지.
- 문서: `web/README.md`, `AGENTS.md` Web Dashboard Workflow를 두 엔진 기준으로 갱신.

검증: `python3 -m py_compile`(app.py)·`node --check`(app.js) 통과, `ENGINES` import 확인, `/api/run/claude-status`가 잘못된 run_path를 안전하게 검증, `/`가 두 실행 버튼 serve 확인. 실제 Claude 자율 subprocess 기동은 로컬 sandbox 정책상 이 세션에서 직접 실행하지 않고 대시보드에서 사용자가 테스트한다.

