# HANDOFF

## Objective

BioProject01의 기존 논문 분석 하네스를 CLI/대화형 실행만이 아니라 웹에서 클릭 기반으로 다룰 수 있게 만들었다.

목표는 기존 `AGENTS.md`, `skills/`, `analysis/` 구조를 대체하지 않고, 웹 대시보드를 "조작판"으로 추가하는 것이다. 웹은 새 분석 요청을 기록하고, 기존 분석 목록을 보여주고, deterministic helper script를 클릭으로 실행한다.

## Current Status

- Local dashboard implemented under `web/`.
- Team/LAN sharing implemented with token authentication.
- Dashboard records web-created requests under `artifacts/web-runs/`.
- Dashboard can now start a saved request directly with `codex exec --cd <repo> -`.
- Codex job status and logs are stored beside the run prompt.
- `AGENTS.md` now includes a short `Web Dashboard Workflow` routing section.
- Local server was started and verified at `http://127.0.0.1:8765`.
- API smoke test confirmed 9 existing paper-analysis folders are listed.
- Token mode smoke test confirmed:
  - no token -> `401`
  - correct token -> paper list returned

## Relevant Repository Structure

```text
AGENTS.md
skills/
analysis/
web/
  app.py
  index.html
  README.md
  DEPLOY.md
  scripts/share_dashboard.sh
  static/app.css
  static/app.js
artifacts/
  README.md
  web-runs/
```

Existing paper-analysis source of truth remains:

```text
AGENTS.md
skills/*/SKILL.md
analysis/<topic>/<paper-id>/
```

The dashboard starts LLM-driven analysis through Codex only after the user clicks `Run in Codex`. It also runs deterministic scripts:

- `codex exec --cd <repo> -`
- `skills/source-grounding/scripts/build_index.py`
- `skills/core-to-html/scripts/build_html.py <paper-dir>`

## Files Modified And Why

- `AGENTS.md`
  - Added `Web Dashboard Workflow` near the end.
  - Purpose: route "웹으로 논문 분석", "클릭으로 논문 해석", "팀원에게 배포" requests to the dashboard.

## Files Added And Why

- `web/app.py`
  - Python standard-library local web server.
  - Lists papers, creates run prompts, starts Codex jobs, serves files, rebuilds index, renders HTML reports.
  - Supports optional token auth via `--token` or `BIOP01_DASHBOARD_TOKEN`.

- `web/index.html`
  - Browser UI for new analysis request, run prompt viewing, existing paper search, index rebuild, HTML render.

- `web/static/app.css`
  - Dashboard styling.

- `web/static/app.js`
  - Frontend API calls, filtering, run prompt creation, Codex job start/status, prompt copy/download, token storage in browser localStorage.

- `web/README.md`
  - Short local usage guide.

- `web/DEPLOY.md`
  - Team deployment guide with local mode, LAN mode, token instructions, and safety boundary.

- `web/scripts/share_dashboard.sh`
  - Convenience script for LAN sharing.
  - Generates a token if `BIOP01_DASHBOARD_TOKEN` is unset.
  - Prints local/LAN URL candidates.

- `artifacts/README.md`
  - Explains non-paper operational artifacts.

- `artifacts/web-runs/.gitkeep`
  - Keeps the run directory in git even before real run records exist.

## Commands Run And Results

### Project inspection

```bash
rg --files -g 'AGENTS.md' -g 'package.json' -g 'pyproject.toml' -g 'README*' -g '*.py'
find . -maxdepth 3 -type d
rg -n "paper|논문|study|interpret|해석|pdf|doi|article|reading|summar|요약|autobiox" . -S
```

Result: BioProject01 has an existing paper-analysis harness:

- router: `AGENTS.md`
- skills: `skills/source-grounding`, `skills/core-*`, `skills/lens-*`, `skills/methodology-brief`, `skills/core-to-html`
- outputs: `analysis/<topic>/<paper-id>/`

### Web dashboard validation

```bash
python3 -m py_compile web/app.py
bash -n web/scripts/share_dashboard.sh
```

Result: both passed.

```bash
python3 web/app.py --port 8765
curl -s http://127.0.0.1:8765/api/papers | python3 -c 'import json,sys; print(len(json.load(sys.stdin).get("papers", [])))'
```

Result: server started and returned `9`.

### Request creation smoke test

```bash
curl -s -X POST http://127.0.0.1:8765/api/run/new \
  -H 'Content-Type: application/json' \
  -d '{"source":"DOI: 10.0000/test","topic":"epigenomic-lag","mode":"abstract-only","lens":"none","notes":"smoke test"}'
```

Result: created a temporary run under `artifacts/web-runs/20260608-204935/`. This dummy run was removed afterward.

### Token mode smoke test

```bash
python3 web/app.py --host 127.0.0.1 --port 8766 --token test-token
curl -s -o /tmp/biop01_no_token.json -w '%{http_code}' http://127.0.0.1:8766/api/papers
curl -s -H 'X-Dashboard-Token: test-token' http://127.0.0.1:8766/api/papers
```

Result:

- without token: `401`
- with token: returned 9 papers

Test server on port `8766` was stopped. Server on `8765` remained running at the end of implementation.

## How To Reproduce From Scratch

From the repository root:

```bash
cd /Users/kkkim/projects/autobiox/BioProject01
mkdir -p web/static web/scripts artifacts/web-runs
```

Create the following files from this repository's current versions:

```text
web/app.py
web/index.html
web/static/app.css
web/static/app.js
web/README.md
web/DEPLOY.md
web/scripts/share_dashboard.sh
artifacts/README.md
artifacts/web-runs/.gitkeep
```

Make the share script executable:

```bash
chmod +x web/scripts/share_dashboard.sh
```

Add the `Web Dashboard Workflow` section to `AGENTS.md`:

```markdown
## Web Dashboard Workflow

사용자가 "웹으로 논문 분석", "클릭으로 논문 해석", "팀원에게 논문 분석 하네스 배포"처럼 요청하면 `web/` 대시보드를 안내한다.

- 로컬 실행: `python3 web/app.py --port 8765`
- 팀 LAN 공유: `./web/scripts/share_dashboard.sh`
- 확인 문서: `web/README.md`, `web/DEPLOY.md`
- 실행 요청 기록: `artifacts/web-runs/<run-id>/request.json`, `artifacts/web-runs/<run-id>/prompt.md`

웹 대시보드는 기존 분석 규칙을 대체하지 않는다. 새 분석 요청을 클릭으로 기록하고, 기존 `AGENTS.md` Full Paper Workflow에 넣을 `prompt.md`를 만든다. 결정적 스크립트 실행은 `analysis/_index/` rebuild와 `<paper-id>_core.html` render에 한정한다. LLM이 필요한 core/lens/methodology 분석은 기존 `skills/` 규칙과 `analysis/<topic>/<paper-id>/` 산출물 계약을 그대로 따른다.
```

Validate:

```bash
python3 -m py_compile web/app.py
bash -n web/scripts/share_dashboard.sh
python3 web/app.py --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

## Team Distribution

For each teammate running locally:

```bash
git pull
cd /Users/kkkim/projects/autobiox/BioProject01
python3 web/app.py --port 8765
```

For one person hosting on LAN:

```bash
cd /Users/kkkim/projects/autobiox/BioProject01
./web/scripts/share_dashboard.sh
```

The script prints:

- local URL
- LAN URL candidates
- generated token

Teammates open the LAN URL and enter the token in the `Team token` field.

Do not expose this server to the public internet. It can read repository files and run helper scripts.

## Key Decisions And Rationale

- Used Python standard library instead of Flask/FastAPI.
  - Reason: no extra dependency needed for a small local dashboard.

- Runs LLM-driven analysis as an explicit user action.
  - Reason: the dashboard should not auto-start a long Codex job just because a prompt was created. `Run in Codex` is the boundary.

- Web-created analysis requests are saved as `prompt.md`.
  - Reason: this preserves a clean handoff from UI clicks to the existing `AGENTS.md` Full Paper Workflow.

- Added token auth for team sharing.
  - Reason: LAN sharing exposes file-read and script-run API endpoints. Token auth reduces accidental access risk.

## Known Risks

- The dashboard is not hardened for public internet exposure.
- The file viewer is intentionally repository-scoped, but still exposes repo file content to token holders.
- `Render HTML` requires dependencies from `skills/source-grounding/scripts/requirements.txt`.
- `Render HTML` may fail if source PDF or required Python packages are missing.
- `Run in Codex` depends on local Codex auth and may fail if the analysis requires unavailable network access or tool approval.

## Unresolved Questions

- Needs confirmation: whether teammates should run their own local copy or one host should serve the dashboard during study sessions.
- Needs confirmation: whether future versions should add a persistent job queue that survives dashboard restarts.
- Needs confirmation: whether web-created run records should be git-tracked or ignored after team usage grows.

## Exact Next Steps

1. Open `http://127.0.0.1:8765` and visually test the dashboard.
2. Create a real paper request through the UI.
3. Click `Run in Codex`.
4. Use `Refresh Status` to watch `codex-job.json` and `codex.log`.
5. After analysis outputs are created, click `Build Index`.
6. Select the new paper and click `Render HTML`.
7. Run `./web/scripts/share_dashboard.sh` for a team study session.
8. Decide whether to add `.gitignore` rules for `artifacts/web-runs/*` after real team usage.

## Suggested First Command For Next Session

```bash
cd /Users/kkkim/projects/autobiox/BioProject01
python3 web/app.py --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

## Earlier Environment Cleanup In This Session

Before the BioProject01 dashboard work, Codex startup warnings were cleaned up outside this repository:

- Fixed invalid YAML frontmatter in 8 `agent-workbench` `SKILL.md` files by changing long `description:` values to YAML block scalar form.
- Applied to both plugin cache and original plugin path:
  - `/Users/kkkim/.codex/plugins/cache/kkkim/agent-workbench/0.1.0+codex.20260606001918/skills/...`
  - `/Users/kkkim/plugins/agent-workbench/skills/...`
- Commented out unauthorized Atlassian MCP startup config in `/Users/kkkim/.codex/config.toml`.
- Verified:
  - all 8 skill frontmatters parsed successfully
  - `codex mcp list` showed no configured MCP servers

Those environment changes are not part of the BioProject01 repository.
