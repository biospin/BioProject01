#!/usr/bin/env bash
# 셔플 draw 변동(shuffle-seed 반복) refit 무인 드라이버 (detached).
# idempotent — 이미 있는 (b,seed) csv 는 skip. 기존 paired_shuffle / runtorun 산출물은 건드리지 않는다.
# 사용: setsid nohup bash scripts/run_shuffle_seed_refit.sh </dev/null >/dev/null 2>&1 &
set -u
ROOT=/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark
LOG="$ROOT/results/logs/shuffle_seed_refit.log"
HB="$ROOT/results/logs/SHUFFLE_SEED_HEARTBEAT"
DONE="$ROOT/results/logs/SHUFFLE_SEED_DONE"
PY=/opt/envs/velo-mv/bin/python
NJ="${MV_BOOT_NJOBS:-8}"      # 3 stream 병렬 → 3×8=24 thread (32 core)
mkdir -p "$ROOT/results/logs"
rm -f "$DONE"
cd "$ROOT/scripts" || exit 1

( while :; do echo "hb $(date -Is)" > "$HB"; sleep 60; done ) &
HBPID=$!
trap 'kill $HBPID 2>/dev/null' EXIT

{
  echo "=== shuffle-seed refit start $(date -Is) pid=$$ ppid=$PPID njobs_per_stream=$NJ ==="
  T0=$(date +%s)
  PIDS=""
  for b in 0 1 2; do
    (
      export TMPDIR="/tmp/mvs$b"
      mkdir -p "$TMPDIR"
      "$PY" -u p2_multivelo_shuffle_seed_refit.py --boots "$b" --njobs "$NJ" \
        > "$ROOT/results/logs/shuffle_seed_refit_b$b.log" 2>&1
      echo "stream b=$b rc=$? $(date -Is)"
    ) &
    PIDS="$PIDS $!"
  done
  # heartbeat 서브셸은 무한루프이므로 인자 없는 wait 를 쓰면 안 된다(영원히 안 끝남).
  wait $PIDS
  T1=$(date +%s)
  echo "=== end $(date -Is) elapsed_sec=$((T1-T0)) ==="
  echo "elapsed_sec=$((T1-T0)) $(date -Is)" > "$DONE"
} >> "$LOG" 2>&1
