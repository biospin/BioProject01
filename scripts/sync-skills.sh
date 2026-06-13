#!/usr/bin/env bash
#
# sync-skills.sh — root skills/ (single source of truth) → .claude/skills/ (Claude mirror)
#
# 설계 (2026-06-13 결정):
#   - root `skills/`        = 유일 source. Codex(코덱스), AGENTS.md 라우터, web/app.py 스크립트가 읽음.
#                            Claude Max 중단 시 Codex가 메인 엔진으로 승격될 수 있으므로 1급 경로로 유지.
#   - `.claude/skills/`     = Claude Code auto-discovery용 파생 mirror. **직접 수정 금지** — 항상 이 스크립트로 갱신.
#
# 왜 복사인가: claude.ai/code 웹(GitHub 체크아웃)이 symlink를 따라가는지 미검증이라, 안전하게 실제 파일 복사로 둔다.
#             웹에서 symlink 동작이 확인되면 `.claude/skills -> ../skills` 심볼릭으로 전환해 중복 자체를 없앨 수 있다.
#
# 사용법:
#   scripts/sync-skills.sh           # root skills/ 를 .claude/skills/ 로 동기화 (mirror)
#   scripts/sync-skills.sh --check   # 동기화 여부만 검사 (변경 없음). 어긋나면 exit 1. (pre-commit 훅용)
#
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SRC="$REPO_ROOT/skills/"
DST="$REPO_ROOT/.claude/skills/"

# 빌드 노이즈만 제외하고 나머지는 그대로 미러링한다 (scripts/, agents/openai.yaml 포함 = 충실한 사본).
EXCLUDES=(--exclude='__pycache__/' --exclude='*.pyc' --exclude='.DS_Store')

# -r 재귀, -l 심볼릭, -p 권한, -c 체크섬(내용) 기준 비교.
# 의도적으로 -t(타임스탬프 보존)를 빼서, 내용이 같고 mtime만 다른 경우를 "어긋남"으로 잡지 않는다.
RFLAGS=(-rlpc --delete --itemize-changes)

if [[ ! -d "$SRC" ]]; then
  echo "✗ source 없음: $SRC" >&2
  exit 2
fi
mkdir -p "$DST"

if [[ "${1:-}" == "--check" ]]; then
  # dry-run: 변경이 필요하면(itemized 출력이 비어있지 않으면) 어긋난 것.
  OUT="$(rsync "${RFLAGS[@]}" "${EXCLUDES[@]}" --dry-run "$SRC" "$DST")"
  if [[ -n "$OUT" ]]; then
    echo "✗ .claude/skills 가 root skills/ 와 어긋나 있습니다. 'scripts/sync-skills.sh' 실행 필요:" >&2
    echo "$OUT" >&2
    exit 1
  fi
  echo "✓ in sync (.claude/skills == skills)"
  exit 0
fi

rsync "${RFLAGS[@]}" "${EXCLUDES[@]}" "$SRC" "$DST"
echo "✓ synced: skills/ → .claude/skills/"
