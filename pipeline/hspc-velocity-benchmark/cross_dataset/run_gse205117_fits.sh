#!/usr/bin/env bash
# GSE205117 fit 드라이버 — floor + MultiVelo + MultiVeloVAE (+P3 prereg 채점).
# .BUILD_DONE 대기 → 각 stage idempotent(산출물 있으면 skip). 반드시 detach:
#   setsid bash run_gse205117_fits.sh </dev/null >fits_driver.log 2>&1 &
set -u
ROOT="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
SCRIPTS="$ROOT/scripts"; CROSS="$ROOT/cross_dataset"; RESULTS="$ROOT/results"; DATA="$ROOT/data"
CONDA="/home/kkkim/miniconda3/bin/conda"
DS="gse205117"; CONFIG="../cross_dataset/config_${DS}.py"; SUFFIX="_${DS}"
PROC="$DATA/processed_${DS}"; OUT_RNA="$PROC/rna_spliced_unspliced.h5ad"; OUT_ATAC="$PROC/atac_gene.h5ad"
FLOOR_CSV="$RESULTS/rna_only_dynamical_genes${SUFFIX}.csv"
MV_CSV="$RESULTS/multivelo_genes${SUFFIX}.csv"
VAE_CSV="$RESULTS/multivelovae_genes${SUFFIX}.csv"
DONE="$CROSS/GSE205117_FIT_DONE"; FAILED="$CROSS/GSE205117_FIT_FAILED"; PROG="$CROSS/GSE205117_FIT_PROGRESS"
export TMPDIR="/home/kkkim/.tmp_gse"; mkdir -p "$TMPDIR"      # AF_UNIX 107자 한계(bmmc 교훈)
export HDF5_USE_FILE_LOCKING=FALSE
log(){ echo "[$(date '+%F %T')] $*"; }
hb(){ { echo "=== GSE205117 FIT PROGRESS ==="; echo "updated: $(date '+%F %T')"; echo "driver: PID $$ (PPID $PPID)";
        echo "stage : $1"; echo "build : $( [ -f "$OUT_RNA" ]&&[ -f "$OUT_ATAC" ]&&echo ok||echo - )";
        echo "floor : $( [ -f "$FLOOR_CSV" ]&&wc -l <"$FLOOR_CSV"||echo - )";
        echo "MV    : $( [ -f "$MV_CSV" ]&&wc -l <"$MV_CSV"||echo - )";
        echo "VAE   : $( [ -f "$VAE_CSV" ]&&wc -l <"$VAE_CSV"||echo - )"; } > "$PROG"; }
die(){ log "FAILED at $1: $2"; { echo "FAILED at $1"; echo "$2"; date; } > "$FAILED"; exit 1; }
rm -f "$DONE" "$FAILED"
log "=== gse205117 fit driver 시작 (PID $$, PPID $PPID) ==="

# 0) build 완료 대기
i=0; until [ -f "$PROC/.BUILD_DONE" ]; do
  [ -f "$PROC/.BUILD_FAILED" ] && die "0-build" "build 실패(.BUILD_FAILED)"
  sleep 60; i=$((i+1)); [ $((i%10)) -eq 0 ] && log "….BUILD_DONE 대기 ($i분)"; done
{ [ -f "$OUT_RNA" ] && [ -f "$OUT_ATAC" ]; } || die "0-out" "build 산출물 없음"
log "build 완료 감지"

# 1) RNA-only floor (scv-preprocess)
hb "1 floor"
if [ -f "$FLOOR_CSV" ] && [ "$(wc -l <"$FLOOR_CSV")" -ge 2 ]; then log "[1] floor skip"; else
  log "[1] p2_rna_only.py (scv-preprocess)"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" \
      "$CONDA" run --no-capture-output -n scv-preprocess python -u p2_rna_only.py ) || die "1-floor" "floor 실패"
  { [ -f "$FLOOR_CSV" ] && [ "$(wc -l <"$FLOOR_CSV")" -ge 2 ]; } || die "1-floor-out" "floor csv 없음"
fi

# 2) MultiVelo — smoke(--genes 30) 검증 후 full (velo-mv)
hb "2 MV"
if [ -f "$MV_CSV" ] && [ "$(wc -l <"$MV_CSV")" -ge 2 ]; then log "[2] MV skip"; else
  log "[2a] MultiVelo smoke --genes 30 (배선 검증)"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" \
      "$CONDA" run --no-capture-output -n velo-mv python -u p2_multivelo.py --genes 30 ) || die "2a-mv-smoke" "MV smoke 실패"
  { [ -f "$RESULTS/multivelo_genes${SUFFIX}.smoke.csv" ] && [ "$(wc -l <"$RESULTS/multivelo_genes${SUFFIX}.smoke.csv")" -ge 2 ]; } \
      || die "2a-smoke-out" "MV smoke csv 비어있음"
  log "[2b] MultiVelo full"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" \
      "$CONDA" run --no-capture-output -n velo-mv python -u p2_multivelo.py ) || die "2b-mv" "MultiVelo full 실패"
  { [ -f "$MV_CSV" ] && [ "$(wc -l <"$MV_CSV")" -ge 2 ]; } || die "2b-mv-out" "MultiVelo csv 없음"
fi

# 3) MultiVeloVAE (velo-torch; dl_prep → VAE, CUDA:1=BIOP01 전용)
hb "3 VAE"
if [ -f "$VAE_CSV" ] && [ "$(wc -l <"$VAE_CSV")" -ge 2 ]; then log "[3] VAE skip"; else
  log "[3a] p2_dl_prep.py (velo-torch, CUDA:1)"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" CUDA_VISIBLE_DEVICES=1 \
      "$CONDA" run --no-capture-output -n velo-torch python -u p2_dl_prep.py ) || die "3a-dlprep" "dl_prep 실패"
  log "[3b] p2_multivelovae.py --gpu (CUDA:1)"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" CUDA_VISIBLE_DEVICES=1 \
      "$CONDA" run --no-capture-output -n velo-torch python -u p2_multivelovae.py --gpu ) || die "3b-vae" "VAE 실패"
  { [ -f "$VAE_CSV" ] && [ "$(wc -l <"$VAE_CSV")" -ge 2 ]; } || die "3b-vae-out" "VAE csv 없음"
fi

# 4) P3 사전등록 채점 (scv-preprocess)
hb "4 prereg"
log "[4] p3_prereg_gse205117.py"
( cd "$ROOT" && "$CONDA" run --no-capture-output -n scv-preprocess python -u cross_dataset/p3_prereg_gse205117.py ) \
  || log "[4] prereg 채점 rc=$? (fit은 완료; 채점은 수동 재실행 가능)"

hb "FIT+P3 DONE"
{ echo "=== GSE205117 FIT DONE ==="; date; echo "";
  echo "  floor: $FLOOR_CSV ($(wc -l <"$FLOOR_CSV") 행)";
  echo "  MV   : $MV_CSV ($(wc -l <"$MV_CSV") 행)";
  echo "  VAE  : $VAE_CSV ($(wc -l <"$VAE_CSV") 행)";
  echo "  scorecard: $RESULTS/prereg_gse205117_scorecard.md"; } > "$DONE"
log "=== gse205117 fit driver 정상 종료 ==="
exit 0
