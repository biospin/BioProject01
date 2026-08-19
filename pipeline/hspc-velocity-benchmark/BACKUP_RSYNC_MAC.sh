#!/usr/bin/env bash
# 맥미니에서 실행 — BIOP01 tier1(velocity 55G + results)만. 맥 84G에 안전(~29G 잔여).
# 전체 80G(+processed 24G)는 이건규 Drive로(BACKUP_RCLONE_DRIVE.sh).
set -euo pipefail
SRV=kkkim@121.126.38.195
B=~/project/BioProject01/pipeline/hspc-velocity-benchmark   # 서버 경로
DST=~/biop01_backup

mkdir -p "$DST/data"
rsync -avz --progress "$SRV:$B/data/velocity" "$DST/data/"   # 55G
rsync -avz --progress "$SRV:$B/results"       "$DST/"        # 20M
rsync -avz "$SRV:$B/BACKUP_MANIFEST.tsv"      "$DST/"

# 무결성 검증(tier1만): 매니페스트 sha256 대조
echo "검증:"
echo "  cd $DST && awk -F'\\t' '\$1~/^tier1/ && \$4~/^[a-f0-9]{64}\$/{print \$4\"  \"\$2}' BACKUP_MANIFEST.tsv | shasum -a 256 -c | grep -v ': OK\$' || echo ALL_OK"
