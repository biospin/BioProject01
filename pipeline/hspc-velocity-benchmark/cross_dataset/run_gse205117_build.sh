#!/usr/bin/env bash
# GSE205117 build 오케스트레이터: ATAC_FRAG_DONE 대기 → stage atac(heavy) → stage finalize.
# detached: setsid bash run_gse205117_build.sh </dev/null >build_orch.log 2>&1 &
set -u
ROOT="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
CD="$ROOT/cross_dataset"; PROC="$ROOT/data/processed_gse205117"
FRAGDONE="/home/kkkim/data/gse205117_fullB/atac_frag/ATAC_FRAG_DONE"
PY="conda run --no-capture-output -n scv-preprocess python -u"
log(){ echo "[$(date '+%F %T')] $*"; }
mkdir -p "$PROC"
log "=== build orchestrator 시작 (PID $$, PPID $PPID) ==="

# 0) 모든 fragments 다운 완료 대기
i=0; until [ -f "$FRAGDONE" ]; do sleep 60; i=$((i+1)); [ $((i%10)) -eq 0 ] && log "…ATAC_FRAG_DONE 대기 ($i분)"; done
log "ATAC_FRAG_DONE 감지"

cd "$ROOT"
# 1) stage atac (heavy, fragments 스트리밍 집계)
if [ -f "$PROC/_raw_atac_gene.h5ad" ] && [ -f "$PROC/.ATAC_STAGE_DONE" ]; then
  log "stage atac 이미 완료 → skip"
else
  log "stage atac 시작"
  $PY cross_dataset/build_gse205117.py atac > "$CD/build_atac_gse205117.log" 2>&1
  rc=$?; if [ $rc -ne 0 ]; then log "stage atac FAIL rc=$rc → 중단"; echo "atac rc=$rc" > "$PROC/.BUILD_FAILED"; exit 1; fi
  touch "$PROC/.ATAC_STAGE_DONE"; log "stage atac 완료"
fi

# 2) stage finalize
log "stage finalize 시작"
$PY cross_dataset/build_gse205117.py finalize > "$CD/build_finalize_gse205117.log" 2>&1
rc=$?; if [ $rc -ne 0 ]; then log "stage finalize FAIL rc=$rc → 중단"; echo "finalize rc=$rc" > "$PROC/.BUILD_FAILED"; exit 1; fi

if grep -q "^DONE" "$CD/build_finalize_gse205117.log"; then
  touch "$PROC/.BUILD_DONE"; log "=== build 완료(finalize DONE) → .BUILD_DONE ==="
else
  log "finalize 로그에 DONE 없음 — 확인 필요"; echo "finalize no-DONE" > "$PROC/.BUILD_FAILED"; exit 1
fi
