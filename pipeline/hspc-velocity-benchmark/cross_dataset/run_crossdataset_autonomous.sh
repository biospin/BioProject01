#!/usr/bin/env bash
# Cross-dataset(human_brain) 무인 오케스트레이터 — 로그아웃돼도 끝까지 수행.
#   1) MultiVelo 풀런 완료 대기(polling). 죽었고 산출물 없으면 재실행(최대 N회).
#   2) 완료 시 P3 cross-dataset concordance 실행 → concordance_human_brain.md
#   3) DONE/FAILED sentinel 드롭. git 커밋은 안 함(사용자 복귀 후 수동).
# 실행(반드시 detach): setsid bash run_crossdataset_autonomous.sh </dev/null >driver.log 2>&1 &
set -u

ROOT="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
SCRIPTS="$ROOT/scripts"
CROSS="$ROOT/cross_dataset"
RESULTS="$ROOT/results"
CONFIG="../cross_dataset/config_human_brain.py"
SUFFIX="_human_brain"

MV_CSV="$RESULTS/multivelo_genes${SUFFIX}.csv"
MV_LOG="$CROSS/p2_multivelo${SUFFIX}.log"
CONC_MD="$RESULTS/concordance${SUFFIX}.md"
CONC_LOG="$CROSS/p3_concordance${SUFFIX}.log"
DONE="$CROSS/AUTOPIPE_DONE"
FAILED="$CROSS/AUTOPIPE_FAILED"
PROGRESS="$CROSS/AUTOPIPE_PROGRESS"

MAX_RELAUNCH=3
POLL_SEC=120
# 무한대기 방지 상한(초): ~2h 예상 → 5h 넘으면 실패 처리
MAX_WAIT_SEC=$((5 * 3600))

CONDA="/home/kkkim/miniconda3/bin/conda"

log() { echo "[$(date '+%F %T')] $*"; }

rm -f "$DONE" "$FAILED"
log "=== autonomous driver 시작 (PID $$, PPID $PPID, SID $(ps -o sid= -p $$ | tr -d ' ')) ==="

launch_mv() {
  log "MultiVelo 풀런 launch"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" \
      HDF5_USE_FILE_LOCKING=FALSE "$CONDA" run --no-capture-output -n mv \
      python -u p2_multivelo.py > "$MV_LOG" 2>&1 ) &
  MV_PID=$!
  log "MultiVelo PID=$MV_PID"
}

mv_done() {
  # 완료 판정: 산출 csv 존재 + 로그에 성공마커 + csv 데이터행 존재
  [ -f "$MV_CSV" ] || return 1
  grep -q "gene fit" "$MV_LOG" 2>/dev/null || return 1
  [ "$(wc -l < "$MV_CSV")" -ge 2 ] || return 1
  return 0
}

mv_alive() {
  # human_brain 풀런만 매칭: p2_multivelo.py 있고 --genes(smoke) 없는 프로세스
  pgrep -af "p2_multivelo.py" 2>/dev/null | grep -qv -- "--genes"
}

heartbeat() {
  # 중간중간 저장(사용자 요청): poll마다 진행상황 스냅샷 → 재로그인 시 한눈에 상태 확인.
  local stage="$1"
  local chunks; chunks=$(grep -cE "genes will be fitted" "$MV_LOG" 2>/dev/null || echo 0)
  local lastgene; lastgene=$(grep -E "predicted model|final params" "$MV_LOG" 2>/dev/null | tail -1 | cut -c1-60)
  {
    echo "=== AUTOPIPE PROGRESS (heartbeat) ==="
    echo "updated : $(date '+%F %T')"
    echo "driver  : PID $$ (PPID $PPID)"
    echo "stage   : $stage"
    echo "relaunch: $relaunch/$MAX_RELAUNCH,  waited: ${waited}s / ${MAX_WAIT_SEC}s"
    echo "mv chunk: ${chunks}/~17 (MV_CHUNK=50, 총 802 gene)"
    echo "mv last : $lastgene"
    echo "mv csv  : $( [ -f "$MV_CSV" ] && echo "존재 ($(wc -l < "$MV_CSV") 행)" || echo "미생성" )"
  } > "$PROGRESS"
}

# ---- 1) MultiVelo 풀런 완료 대기 ----
relaunch=0
waited=0
while true; do
  if mv_done; then
    log "MultiVelo 완료 감지: $MV_CSV ($(wc -l < "$MV_CSV") 행)"
    heartbeat "MultiVelo 완료 — P3 진입"
    break
  fi
  heartbeat "MultiVelo 풀런 진행 중"
  if mv_alive; then
    :  # 진행 중 — 대기
  else
    if [ "$relaunch" -ge "$MAX_RELAUNCH" ]; then
      log "MultiVelo 프로세스 없음 + 산출물 없음 + 재실행 $MAX_RELAUNCH회 소진 → 실패"
      { echo "FAILED at MultiVelo stage after $MAX_RELAUNCH relaunches"; date; } > "$FAILED"
      exit 1
    fi
    relaunch=$((relaunch + 1))
    log "MultiVelo 프로세스 죽었고 산출물 없음 → 재실행 ($relaunch/$MAX_RELAUNCH)"
    launch_mv
    sleep 15
  fi
  sleep "$POLL_SEC"
  waited=$((waited + POLL_SEC))
  if [ "$waited" -ge "$MAX_WAIT_SEC" ]; then
    log "MAX_WAIT_SEC($MAX_WAIT_SEC) 초과 → 실패"
    { echo "FAILED: MultiVelo exceeded MAX_WAIT_SEC"; date; } > "$FAILED"
    exit 1
  fi
done

# ---- 2) P3 cross-dataset concordance ----
log "P3 cross-dataset concordance 실행"
( cd "$SCRIPTS" && HDF5_USE_FILE_LOCKING=FALSE "$CONDA" run --no-capture-output -n scv-preprocess \
    python -u p3_crossdataset_concordance.py --dataset human_brain ) > "$CONC_LOG" 2>&1
rc=$?
if [ "$rc" -ne 0 ] || [ ! -f "$CONC_MD" ]; then
  log "P3 concordance 실패 (rc=$rc, md 존재=$( [ -f "$CONC_MD" ] && echo yes || echo no ))"
  { echo "FAILED at P3 concordance stage (rc=$rc)"; date; } > "$FAILED"
  exit 1
fi

# ---- 3) DONE sentinel ----
log "완료. concordance → $CONC_MD"
{
  echo "=== AUTOPIPE DONE ==="
  date
  echo ""
  echo "산출물:"
  echo "  MultiVelo full: $MV_CSV ($(wc -l < "$MV_CSV") 행)"
  echo "  concordance   : $CONC_MD"
  echo ""
  echo "--- concordance 판정 발췌 ---"
  grep -A3 "## 판정" "$CONC_MD" 2>/dev/null
  echo ""
  echo "--- headline ---"
  grep "headline lag" "$CONC_MD" 2>/dev/null
} > "$DONE"
log "=== driver 정상 종료 ==="
exit 0
