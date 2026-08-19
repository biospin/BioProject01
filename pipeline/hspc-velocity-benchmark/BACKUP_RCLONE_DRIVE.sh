#!/usr/bin/env bash
# 이건규 Drive 접근(rclone remote 'gdrive') 확정 후 서버에서 실행 — 전체 80G(velocity+processed+results).
# 사전: rclone config로 'gdrive' remote 등록(이건규 공유폴더/토큰/서비스계정).
set -euo pipefail
B=/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark
REMOTE=gdrive:biop01_backup

rclone copy "$B/data/velocity" "$REMOTE/data/velocity" -P            # tier1 55G
for p in processed processed_gse205117 processed_human_brain \
         processed_e18_mouse_brain processed_GSE194122_bmmc processed_macrophage; do
  [ -d "$B/data/$p" ] && rclone copy "$B/data/$p" "$REMOTE/data/$p" -P   # tier2 24G
done
rclone copy "$B/results"           "$REMOTE/results" -P
rclone copy "$B/BACKUP_MANIFEST.tsv" "$REMOTE/" -P

# 무결성: rclone check "$B/data/velocity" "$REMOTE/data/velocity"  (또는 매니페스트 sha256 대조)
