# BioProject01 Paper Dashboard

Local click-based dashboard for the existing paper analysis harness.

## Run

```bash
python3 web/app.py --port 8765
```

Open `http://127.0.0.1:8765`.

## Share With Teammates On The Same Network

Use a token when binding to the local network:

```bash
BIOP01_DASHBOARD_TOKEN='change-this-token' python3 web/app.py --host 0.0.0.0 --port 8765
```

Then share:

```text
http://<your-lan-ip>:8765
```

Teammates enter the same token in the `Team token` field in the top toolbar.

For convenience, you can also run:

```bash
./web/scripts/share_dashboard.sh
```

## What It Does

- Records a new paper-analysis request under `artifacts/web-runs/<run-id>/`.
- Generates a ready-to-use `prompt.md` for the existing `AGENTS.md` Full Paper Workflow.
- Runs that `prompt.md` autonomously through either engine:
  - `Claude로 분석` → `claude -p --dangerously-skip-permissions` (stdin = prompt.md), logs to `claude.log` / `claude-job.json`.
  - `Codex로 분석` → `codex exec --cd <repo> -`, logs to `codex.log` / `codex-job.json`.
- Stores execution status and logs per engine in the same run directory; the two engines are independent and can be run on the same request.
- Uploads local PDFs into `artifacts/uploads/` and uses the uploaded path as the analysis source.
- Lists existing `analysis/<topic>/<paper-id>/` folders.
- Rebuilds `analysis/_index/` with `skills/source-grounding/scripts/build_index.py`.
- Renders an existing paper folder to HTML with `skills/core-to-html/scripts/build_html.py`, then opens it in a browser tab.
- Opens `View Core` as a browser-readable page instead of dumping the markdown into a small dashboard box.

## Guided Tutorial

처음 방문하면 우측 하단에 단계별 튜토리얼 카드가 자동으로 열린다(6단계: 둘러보기 → 자료 입력 → 옵션·요청 만들기 → 분석 실행 → 결과 확인 → 팀 공유/인덱스). 각 단계는 해당 화면 영역을 강조 표시하며 스크롤한다.

- 다시 보기: 상단 toolbar의 `❓ 튜토리얼` 버튼.
- 조작: `다음`/`이전` 버튼 또는 키보드 `→`/`←`, 닫기는 `건너뛰기`·`✕`·`Esc`.
- 방문 기록은 브라우저 `localStorage`(`biop01_tutorial_seen`)에 저장돼 다음부터는 자동으로 열리지 않는다.

상단에 고정된 `처음이면 이 순서대로 진행하세요` 가이드 카드(1·2·3 단계)는 그대로 유지되며, 각 단계 버튼은 해당 입력/실행/결과 영역으로 스크롤한다.

## Visual Asset

The dashboard header uses an image generated from the BioProject01 project documents:

```text
web/static/images/bioproject01-dashboard-hero.png
```

Prompt summary: scientific dashboard banner for BioProject01, combining single-cell genomics, chromatin accessibility, RNA velocity, paper-analysis cards, and dual academic/industry analysis streams. No readable text or logos.

## Click Flow

1. For a local PDF, choose the PDF and click `Upload PDF`; the uploaded path is copied into Source.
2. For DOI or URL, fill Source directly.
3. Fill topic, mode, and lens.
4. Click `Create Run Prompt`.
5. Confirm the prompt in the bottom `실행 요청 텍스트` panel.
6. Click `Claude로 분석` (or `Codex로 분석`).
7. In the same bottom panel, check the status card, generated-file badges, and engine log. Use `상태 새로고침` if the job is not auto-refreshing.
8. After analysis files appear in `analysis/<topic>/<paper-id>/`, click `Build Index`.
9. Click `Render HTML` on the paper row to rebuild and open the HTML report.
10. Click `View Core` on the paper row to open the core markdown analysis in a browser tab.

## Boundary

The dashboard does not replace the LLM-driven analysis steps. It is a control surface
for the existing harness and deterministic helper scripts. The source of truth remains:

- `AGENTS.md`
- `skills/*/SKILL.md`
- `analysis/<topic>/<paper-id>/`
