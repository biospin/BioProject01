#!/usr/bin/env bash
# run-to-run null refit 무인 드라이버 (detached). idempotent — 이미 있는 (b,nj)는 skip.
# 사용: setsid nohup bash scripts/run_runtorun_refit.sh </dev/null >/dev/null 2>&1 &
set -u
ROOT=/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark
LOG="$ROOT/results/logs/runtorun_refit.log"
HB="$ROOT/results/logs/RUNTORUN_HEARTBEAT"
DONE="$ROOT/results/logs/RUNTORUN_DONE"
PY=/opt/envs/velo-mv/bin/python
export TMPDIR=/tmp/mvrr
mkdir -p "$TMPDIR" "$ROOT/results/logs"
rm -f "$DONE"
cd "$ROOT/scripts" || exit 1

( while :; do echo "hb $(date -Is)" > "$HB"; sleep 60; done ) &
HBPID=$!
trap 'kill $HBPID 2>/dev/null' EXIT

{
  echo "=== runtorun refit start $(date -Is) pid=$$ ppid=$PPID ==="
  # 1) nj=16 (legacy refit_b 와 worker 수까지 동일) → 적합 결정론 직접 측정
  "$PY" -u p2_multivelo_runtorun_refit.py --boots 0,2 --njobs 16
  rc16=$?
  echo "--- nj16 rc=$rc16 $(date -Is) ---"
  # 2) nj=12 (짝맞춘 shuffle arm B 와 동일 조건) → 짝 Δ 와 같은 nj 대비를 갖는 null
  "$PY" -u p2_multivelo_runtorun_refit.py --boots 0,2 --njobs 12
  rc12=$?
  echo "=== end $(date -Is) rc16=$rc16 rc12=$rc12 ==="
  echo "rc16=$rc16 rc12=$rc12 $(date -Is)" > "$DONE"
} >> "$LOG" 2>&1
