#!/usr/bin/env bash
# 짝맞춘 ATAC-shuffle refit 무인 드라이버 (detached). idempotent — 이미 있는 b는 skip.
# 사용: setsid nohup bash scripts/run_paired_shuffle_refit.sh 0,1,2 </dev/null >/dev/null 2>&1 &
set -u
ROOT=/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark
BOOTS="${1:-0,1,2}"
LOG="$ROOT/results/logs/paired_shuffle_refit.log"
DONE="$ROOT/results/logs/PAIRED_SHUFFLE_DONE"
PY=/opt/envs/velo-mv/bin/python
export TMPDIR=/tmp/mvsh
export MV_BOOT_NJOBS="${MV_BOOT_NJOBS:-12}"
mkdir -p "$TMPDIR" "$ROOT/results/logs"
rm -f "$DONE"
cd "$ROOT/scripts" || exit 1
{
  echo "=== paired shuffle refit start $(date -Is) pid=$$ ppid=$PPID boots=$BOOTS njobs=$MV_BOOT_NJOBS ==="
  "$PY" -u p2_multivelo_paired_shuffle_refit.py --boots "$BOOTS"
  rc=$?
  echo "=== end $(date -Is) rc=$rc ==="
  echo "rc=$rc $(date -Is)" > "$DONE"
} >> "$LOG" 2>&1
