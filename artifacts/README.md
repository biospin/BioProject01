# Artifacts

This directory stores operational outputs that are not paper-level analysis notes.

## `web-runs/`

Each click-created paper analysis request is stored in:

```text
artifacts/web-runs/<run-id>/
  request.json
  prompt.md
  codex-job.json
  codex.log
```

`prompt.md` is the handoff from the web dashboard to the existing BioProject01 paper-analysis harness.

## `uploads/`

Local PDFs uploaded through the web dashboard are stored in:

```text
artifacts/uploads/<timestamp>-<filename>.pdf
```

The dashboard copies this repo-relative path into the Source field so the normal paper-analysis workflow can run from the uploaded PDF.

## Work Logs

- `2026-06-08-bioproject01-web-dashboard-worklog.md` — reproducible record of the Codex startup fixes, dashboard implementation, deployment path, status UI improvements, and browser preview changes. Includes the **2026-06-09 Claude Code harness port** update (skills/agents ported to `.claude/`, `.gitignore` policy change, and the Trevino re-run comparison).
- `2026-06-08-bioproject01-web-dashboard-presentation.md` — presentation-ready Markdown deck (Marp slides) for explaining the dashboard harness to teammates. Includes the 2026-06-09 Claude port appendix slides.
- `blog-harness-codex-to-claude.md` — prose blog post explaining the harness structure and the step-by-step additions (Codex→Claude port, re-run, web dashboard + tutorial, dual-engine execution, fixes). Narrative counterpart to the Marp deck; updated as new work lands.
