# Artifacts — 정책 (critic #12)

paper-level 분석 노트가 아닌 운영 산출물. 역할별로 하위 폴더 분리:

| 폴더 | 내용 | git |
|---|---|---|
| `reports/` | 공유용 리포트·발표·blog·진단 (worklog, presentation, figure-crop 진단, blog) | tracked (`*.md`) |
| `reviews/` | 교차 크리틱·리뷰 기록 (예: 박상준 하네스 critic) | tracked (`*.md`) |
| `web-runs/` | 웹 대시보드 런타임 기록 (request/prompt/job/log) | **기본 ignore** — `.gitkeep`만 추적 |

## web-runs 정책
- 런타임 기록은 **default-ignore** (`.gitignore`: `artifacts/web-runs/**`). local path·token이 섞일 수 있어 그대로 commit하지 않는다.
- 공유가 필요한 run만 **scrub**(local path/token 제거) 후 `reports/`로 옮겨 commit한다.
- 절대경로 lint은 `.claude/agents·skills·skills`를 CI(`harness-check.yml`)가 검사. artifacts 공유 전에는 수동 scrub.

## reports/
- `2026-06-08-...-worklog.md` / `-presentation.md` — web dashboard 작업 기록·발표.
- `2026-06-13-figure-crop-perf-diagnosis.md` — figure crop 성능 진단.
- `blog-harness-codex-to-claude.md` — 하네스 blog.
