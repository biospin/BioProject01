# TODO

## High priority

- [ ] Open `http://127.0.0.1:8765` and visually verify the dashboard layout.
- [ ] Create one real paper-analysis request from the web UI.
- [ ] Click `Run in Codex` for the generated request.
- [ ] Use `Refresh Status` and inspect `artifacts/web-runs/<run-id>/codex.log`.
- [ ] After real analysis files are generated, click `Build Index` and confirm `analysis/_index/papers.csv` updates.
- [ ] Click `Render HTML` for the new paper and confirm `<paper-id>_core.html` is generated.

## Medium priority

- [ ] Run `./web/scripts/share_dashboard.sh` during a team session and confirm another teammate can access the LAN URL with the token.
- [ ] Decide whether `artifacts/web-runs/*` should be committed, ignored, or periodically archived.
- [ ] Add a short screenshot or walkthrough to `web/README.md` after the first real team use.
- [ ] Consider adding a "copy prompt" button if browser UX feels clunky.

## Low priority

- [ ] Consider adding a real job queue if LLM analysis execution is later integrated into the web flow.
- [ ] Consider adding filters by `importance`, `use_case`, and `analysis_status_short`.
- [ ] Consider adding links from paper rows directly to generated HTML reports when present.

## Blocked / Needs confirmation

- [ ] Needs confirmation: team deployment preference, local-per-user vs one LAN host.
- [ ] Needs confirmation: whether web requests should remain private local artifacts or become shared study-session records.
- [ ] Needs confirmation: whether Codex/Claude LLM execution should remain manual or become part of a controlled backend workflow.

## Done (2026-06-09 — Claude port + dual-engine)

- [x] Ported Codex harness to Claude Code: `.claude/skills/` (16), `.claude/agents/` (7), `CLAUDE.md` router, `.gitignore` share-exception.
- [x] Verified the port by re-running one paper (Trevino 2021) in Claude → matches Codex output.
- [x] Added interactive 6-step tutorial to the web dashboard (auto-open first visit + replay button).
- [x] Made the dashboard engine-aware: `Claude로 분석` + `Codex로 분석`, `start-claude`/`claude-status` endpoints.
- [x] paper-row Analyze button now uses Claude (avoids Codex usage-limit failures).
- [x] Uploaded PDF is now copied into `analysis/<topic>/<paper-id>/sources/` (prompt instruction) so analysis is PDF-grounded.
- [x] Wrote prose blog `artifacts/blog-harness-codex-to-claude.md` (kept in sync with slides).

## Follow-ups (Claude port)

- [ ] Test the dashboard `Claude로 분석` end-to-end in the browser (sandbox blocked auto-launch here).
- [ ] Decide whether the paper-row button should offer an engine choice instead of defaulting to Claude.
- [ ] Consider making the uploaded-PDF → `sources/` copy deterministic (dashboard-side) rather than prompt-driven.

## Done

- [x] Added local web dashboard under `web/`.
- [x] Added dashboard API for paper listing, run prompt creation, index rebuild, HTML render, and repo-scoped file viewing.
- [x] Added dashboard API for starting and checking Codex jobs.
- [x] Added bottom prompt panel with copy/download/run/status controls.
- [x] Added team token support for LAN sharing.
- [x] Added `web/scripts/share_dashboard.sh`.
- [x] Added `web/README.md` and `web/DEPLOY.md`.
- [x] Added `artifacts/README.md` and `artifacts/web-runs/.gitkeep`.
- [x] Added `Web Dashboard Workflow` section to `AGENTS.md`.
- [x] Verified Python syntax for `web/app.py`.
- [x] Verified shell syntax for `web/scripts/share_dashboard.sh`.
- [x] Verified local API returns 9 existing papers.
- [x] Verified token mode rejects missing token and accepts correct token.
