#!/usr/bin/env bash
# GSE205117 GEX solo 드라이버 watchdog — 조용한 사망(2026-07-13 13:10 사례) 재발 시 자동 복구.
# 로직: 5분 폴링 → GEX_SOLO_DONE 있으면 종료 / 드라이버 죽었고 DONE 없으면 stale STARtmp 정리 후 재기동.
# 실행: cd $W && setsid bash <repo>/cross_dataset/watchdog_gse205117_gex.sh </dev/null >>watchdog.log 2>&1 &
# ⚠️ 재기동은 idempotent(Gene/Summary.csv 있는 런은 드라이버가 skip). 중복 방지 위해 인스턴스 1개만.
set -u
W="/home/kkkim/data/gse205117_fullB"
DRIVER="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark/cross_dataset/run_gse205117_gex_solo.sh"
declare -A GEX=( [E7.5]=SRR19450575 [E8.0]=SRR19450564 [E8.5]=SRR19450560 [E8.75]=SRR19450574 )
POLL=300; MAX_RESTART=6; restarts=0; last_restart=0
log(){ echo "[$(date '+%F %T')] $*"; }

# 중복 인스턴스 방지 — flock 원자적 락(pgrep 자기매칭 레이스 회피)
LOCK="$W/.watchdog.lock"
exec 9>"$LOCK"
if ! flock -n 9; then log "이미 watchdog 실행 중(락 점유) → 이 인스턴스 종료"; exit 0; fi
log "=== watchdog 시작 (PID $$, PPID $PPID) — $POLL초 폴링, 최대 재기동 $MAX_RESTART ==="

while true; do
  if [ -f "$W/GEX_SOLO_DONE" ]; then log "GEX_SOLO_DONE 감지 → watchdog 임무 완료, 종료"; exit 0; fi
  if [ -f "$W/GEX_SOLO_FAIL" ]; then log "GEX_SOLO_FAIL 감지 → 사람 개입 필요, 재기동 안 함, 종료"; exit 0; fi

  # 드라이버 생존 확인
  if pgrep -f "run_gse205117_gex_solo.sh" >/dev/null 2>&1; then
    sleep "$POLL"; continue
  fi

  # 드라이버 죽음 & DONE/FAIL 없음 → 복구
  log "⚠️ 드라이버 미검출 + DONE/FAIL 없음 → 사망 판정, 복구 시도"
  if [ "$restarts" -ge "$MAX_RESTART" ]; then
    log "재기동 $MAX_RESTART회 초과 → crash-loop 의심, 중단(사람 개입). FAIL 마커 생성."
    { echo "watchdog: 재기동 $MAX_RESTART회 초과로 중단"; date; } > "$W/GEX_SOLO_FAIL"; exit 1
  fi
  now=$(date +%s)
  if [ $((now - last_restart)) -lt 600 ] && [ "$last_restart" -ne 0 ]; then
    log "직전 재기동 <10분 → 즉시 재사망(crash-loop) 의심, 60초 더 대기"; sleep 60
  fi

  # 진행 중이던(미완) GEX 런의 stale 디렉토리 제거 — STAR는 기존 _STARtmp 있으면 즉시 실패
  for tp in E7.5 E8.0 E8.5 E8.75; do
    srr=${GEX[$tp]}; od="$W/gex_solo/$srr"
    [ -d "$od" ] || continue
    if [ -f "$od/${srr}_Solo.out/Gene/Summary.csv" ]; then
      log "  $tp($srr) 완료됨 → 보존(드라이버가 skip)"
    else
      log "  $tp($srr) 미완 → 디렉토리 제거(stale STARtmp 정리)"; rm -rf "$od"
    fi
  done

  # 드라이버 detached 재기동
  cd "$W" || exit 1
  setsid bash "$DRIVER" </dev/null >>"$W/gex_solo.log" 2>&1 &
  restarts=$((restarts+1)); last_restart=$(date +%s)
  sleep 8
  newpid=$(pgrep -f "run_gse205117_gex_solo.sh" | head -1)
  if [ -n "$newpid" ]; then
    ppid=$(ps -o ppid= -p "$newpid" | tr -d ' ')
    log "✅ 재기동 #$restarts 성공 — 드라이버 PID $newpid (PPID $ppid). PPID=1 이어야 로그아웃 생존."
  else
    log "❌ 재기동 #$restarts 후에도 드라이버 미검출 — 다음 폴에서 재시도"
  fi
  sleep "$POLL"
done
