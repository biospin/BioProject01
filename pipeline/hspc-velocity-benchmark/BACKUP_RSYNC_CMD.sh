#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# GPU 반납(8월 말) 대비 백업 — 맥미니에서 실행
# 대상 = GPU-only fitted(data/velocity/ 53.9G) + 논문 수치(results/ 20M) = 총 54G
# (ref/·raw·processed는 재수신/재생성 가능 → DATASETS_DOWNLOAD_MANIFEST.md 참조, 백업 제외)
# 맥 여유 84G → 받아도 ~30G 남음. rsync는 증분이라 다시 돌리면 바뀐 것만 받음.
# ─────────────────────────────────────────────────────────────────
set -euo pipefail
SRV=kkkim@121.126.38.195
B=~/project/BioProject01/pipeline/hspc-velocity-benchmark   # 서버 경로
DST=~/biop01_backup

mkdir -p "$DST/data"
# 1) velocity fitted (53.9G) — 매니페스트 경로(data/velocity/...) 보존
rsync -avz --progress "$SRV:$B/data/velocity" "$DST/data/"
# 2) results (논문 수치, 20M)
rsync -avz --progress "$SRV:$B/results" "$DST/"
# 3) 검증용 매니페스트
rsync -avz "$SRV:$B/BACKUP_MANIFEST.tsv" "$DST/"

# ── 무결성 검증 (받은 뒤 맥에서) ──
# cd ~/biop01_backup && awk -F'\t' '$3~/^[a-f0-9]{64}$/{print $3"  "$1}' BACKUP_MANIFEST.tsv | shasum -a 256 -c | grep -v ': OK$' || echo "ALL OK"
echo "백업 완료. 검증: cd $DST && awk -F'\\t' '\$3~/^[a-f0-9]{64}\$/{print \$3\"  \"\$1}' BACKUP_MANIFEST.tsv | shasum -a 256 -c | grep -v ': OK\$' || echo ALL_OK"
