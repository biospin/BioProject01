#!/usr/bin/env bash
# MoFlow run-to-run null 재적합 무인 드라이버 (detached). idempotent — 이미 있는 run은 skip.
# 사용: setsid nohup bash scripts/run_moflow_runtorun_refit.sh </dev/null >/dev/null 2>&1 &
set -u
ROOT=/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark
LOG="$ROOT/results/logs/moflow_runtorun_refit.log"
HB="$ROOT/results/logs/MOFLOW_RUNTORUN_HEARTBEAT"
DONE="$ROOT/results/logs/MOFLOW_RUNTORUN_DONE"
mkdir -p "$ROOT/results/logs"
rm -f "$DONE"
cd "$ROOT/scripts" || exit 1
export CUDA_VISIBLE_DEVICES=1
export PYTHONPATH="$ROOT/vendor/MoFlow/src"

( while :; do echo "hb $(date -Is)" > "$HB"; sleep 60; done ) &
HBPID=$!
trap 'kill $HBPID 2>/dev/null' EXIT

{
  echo "=== moflow runtorun start $(date -Is) pid=$$ ppid=$PPID ==="
  conda run --no-capture-output -n velo-torch python -u p2_moflow_runtorun_refit.py --runs 2 --gpu
  rc=$?
  echo "=== end $(date -Is) rc=$rc ==="
  echo "rc=$rc $(date -Is)" > "$DONE"
} >> "$LOG" 2>&1
