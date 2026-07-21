#!/usr/bin/env bash
# GSE205117 fits 드라이버(run_gse205117_fits.sh) watchdog — 조용한 사망 재발 대비 자동 재기동.
# fits stage(floor→MV→VAE→prereg)는 전부 idempotent+sentinel(완료분 skip)이라 특별 정리 불필요.
# 실행: cd cross_dataset && setsid bash watchdog_gse205117_fits.sh </dev/null >>fits_watchdog.log 2>&1 &
set -u
R="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
CD="$R/cross_dataset"
DONE="$CD/GSE205117_FIT_DONE"; FAIL="$CD/GSE205117_FIT_FAILED"
LOCK="$CD/.fits_watchdog.lock"
POLL=300; MAX_RESTART=6; restarts=0; last_restart=0
log(){ echo "[$(date '+%F %T')] $*"; }

exec 9>"$LOCK"; if ! flock -n 9; then log "이미 fits watchdog 실행 중(락) → 종료"; exit 0; fi
log "=== fits watchdog 시작 (PID $$, PPID $PPID) — $POLL초 폴링 ==="

while true; do
  if [ -f "$DONE" ]; then log "GSE205117_FIT_DONE 감지 → 임무 완료, 종료"; exit 0; fi
  if [ -f "$FAIL" ]; then log "GSE205117_FIT_FAILED 감지 → 사람 개입 필요, 재기동 안 함, 종료"; exit 0; fi
  if pgrep -f "run_gse205117_fits.sh" >/dev/null 2>&1; then sleep "$POLL"; continue; fi

  log "⚠️ fits 드라이버 미검출 + DONE/FAIL 없음 → 사망 판정, 복구"
  if [ "$restarts" -ge "$MAX_RESTART" ]; then
    log "재기동 $MAX_RESTART회 초과 → crash-loop 의심, 중단(사람 개입). FAIL 마커 생성."
    { echo "fits watchdog: 재기동 $MAX_RESTART회 초과로 중단"; date; } > "$FAIL"; exit 1
  fi
  now=$(date +%s)
  if [ "$last_restart" -ne 0 ] && [ $((now - last_restart)) -lt 600 ]; then
    log "직전 재기동 <10분 → crash-loop 의심, 60초 더 대기"; sleep 60
  fi
  cd "$R" || exit 1
  setsid bash "$CD/run_gse205117_fits.sh" </dev/null >>"$CD/fits_driver.log" 2>&1 &
  restarts=$((restarts+1)); last_restart=$(date +%s); sleep 8
  newpid=$(pgrep -f "run_gse205117_fits.sh" | head -1)
  if [ -n "$newpid" ]; then
    log "✅ 재기동 #$restarts 성공 — 드라이버 PID $newpid (PPID $(ps -o ppid= -p "$newpid"|tr -d ' ')). 완료 stage는 skip."
  else
    log "❌ 재기동 #$restarts 후에도 미검출 — 다음 폴에서 재시도"
  fi
  sleep "$POLL"
done
