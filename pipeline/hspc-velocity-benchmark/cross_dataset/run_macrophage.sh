#!/usr/bin/env bash
# cross-dataset #4 macrophage (figshare 30280333) fit 생산 드라이버 — kkkim GPU heavy-run 몫.
# 지용기 님 계약(BIOP01-29 댓글): results/{rna_only_dynamical,multivelo,multivelovae}_genes_macrophage.csv 3종.
# downstream(p3_concordance·bootstrap·Δρ)은 지용기 님 CPU 몫이라 이 드라이버는 stage 4~7(build→floor→MV→VAE)만.
# 모든 stage idempotent(산출물 있으면 skip). 실행(반드시 detach):
#   setsid bash run_macrophage.sh </dev/null >macro_driver.log 2>&1 &
set -u

ROOT="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
SCRIPTS="$ROOT/scripts"
CROSS="$ROOT/cross_dataset"
RESULTS="$ROOT/results"
DATA="$ROOT/data"
CONDA="/home/kkkim/miniconda3/bin/conda"

DS="macrophage"
CONFIG="../cross_dataset/config_${DS}.py"        # p1_config가 SCRIPTS/에서 상대해석
SUFFIX="_${DS}"

PROC="$DATA/processed_${DS}"
OUT_RNA="$PROC/rna_spliced_unspliced.h5ad"
OUT_ATAC="$PROC/atac_gene.h5ad"
# 입력(figshare, 이미 staged): build_macrophage.py가 data/macrophage/8489-MV-1-9060-MV-3_*_postpro_concat.h5ad 읽음
RNA_IN="$DATA/${DS}/8489-MV-1-9060-MV-3_adata_postpro_concat.h5ad"
ATAC_IN="$DATA/${DS}/8489-MV-1-9060-MV-3_adata_atac_postpro_concat.h5ad"

FLOOR_CSV="$RESULTS/rna_only_dynamical_genes${SUFFIX}.csv"
MV_CSV="$RESULTS/multivelo_genes${SUFFIX}.csv"
VAE_CSV="$RESULTS/multivelovae_genes${SUFFIX}.csv"

DONE="$CROSS/MACRO_FIT_DONE"
FAILED="$CROSS/MACRO_FAILED"
PROGRESS="$CROSS/MACRO_PROGRESS"

# multiprocessing.Manager AF_UNIX 소켓 경로 107자 한계 → TMPDIR 짧게(bmmc 교훈).
export TMPDIR="/home/kkkim/.tmp_macro"; mkdir -p "$TMPDIR"
export HDF5_USE_FILE_LOCKING=FALSE

log() { echo "[$(date '+%F %T')] $*"; }
hb()  { { echo "=== MACROPHAGE FIT PROGRESS ==="; echo "updated: $(date '+%F %T')";
          echo "driver : PID $$ (PPID $PPID)"; echo "stage  : $1";
          echo "build  : $( [ -f "$OUT_RNA" ] && [ -f "$OUT_ATAC" ] && echo ok || echo - )";
          echo "floor  : $( [ -f "$FLOOR_CSV" ] && echo "$(wc -l <"$FLOOR_CSV") 행" || echo - )";
          echo "MV     : $( [ -f "$MV_CSV" ] && echo "$(wc -l <"$MV_CSV") 행" || echo - )";
          echo "VAE    : $( [ -f "$VAE_CSV" ] && echo "$(wc -l <"$VAE_CSV") 행" || echo - )"; } > "$PROGRESS"; }
die() { log "FAILED at $1"; { echo "FAILED at $1"; echo "$2"; date; } > "$FAILED"; exit 1; }

rm -f "$DONE" "$FAILED"
log "=== macrophage fit driver 시작 (PID $$, PPID $PPID) ==="

# 입력 staged 확인
[ -f "$RNA_IN" ] && [ -f "$ATAC_IN" ] || die "0-input" "figshare h5ad 입력 없음: $RNA_IN / $ATAC_IN"

# ── [4] build (scv-preprocess) → processed rna + atac_gene ──
hb "4 build"
if [ -f "$OUT_RNA" ] && [ -f "$OUT_ATAC" ]; then
  log "[4] processed rna+atac_gene 이미 존재 → skip"
else
  log "[4] build_macrophage.py"
  ( cd "$CROSS" && "$CONDA" run --no-capture-output -n scv-preprocess python -u build_macrophage.py ) \
    || die "4-build" "build 실패"
  { [ -f "$OUT_RNA" ] && [ -f "$OUT_ATAC" ]; } || die "4-build-out" "build 산출물 없음"
fi

# ── [5] RNA-only floor (scv-preprocess) ──
hb "5 floor"
if [ -f "$FLOOR_CSV" ] && [ "$(wc -l <"$FLOOR_CSV")" -ge 2 ]; then
  log "[5] floor csv 존재 → skip"
else
  log "[5] p2_rna_only.py"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" \
      "$CONDA" run --no-capture-output -n scv-preprocess python -u p2_rna_only.py ) \
    || die "5-floor" "floor 실패"
  { [ -f "$FLOOR_CSV" ] && [ "$(wc -l <"$FLOOR_CSV")" -ge 2 ]; } || die "5-floor-out" "floor csv 없음"
fi

# ── [6] MultiVelo (mv) ──
hb "6 MultiVelo"
if [ -f "$MV_CSV" ] && [ "$(wc -l <"$MV_CSV")" -ge 2 ]; then
  log "[6] MultiVelo csv 존재 → skip"
else
  log "[6] p2_multivelo.py (mv env)"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" \
      "$CONDA" run --no-capture-output -n mv python -u p2_multivelo.py ) \
    || die "6-mv" "MultiVelo 실패"
  { [ -f "$MV_CSV" ] && [ "$(wc -l <"$MV_CSV")" -ge 2 ]; } || die "6-mv-out" "MultiVelo csv 없음"
fi

# ── [7] MultiVeloVAE (torch; dl_prep → VAE, CUDA:1=BIOP01 전용) ──
hb "7 VAE"
if [ -f "$VAE_CSV" ] && [ "$(wc -l <"$VAE_CSV")" -ge 2 ]; then
  log "[7] VAE csv 존재 → skip"
else
  log "[7] p2_dl_prep.py → p2_multivelovae.py --gpu (torch env, CUDA:1)"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" CUDA_VISIBLE_DEVICES=1 \
      "$CONDA" run --no-capture-output -n torch python -u p2_dl_prep.py ) \
    || die "7-dlprep" "dl_prep 실패"
  ( cd "$SCRIPTS" && CROSS_DATASET_CONFIG="$CONFIG" CROSS_DATASET_SUFFIX="$SUFFIX" CUDA_VISIBLE_DEVICES=1 \
      "$CONDA" run --no-capture-output -n torch python -u p2_multivelovae.py --gpu ) \
    || die "7-vae" "VAE 실패"
  { [ -f "$VAE_CSV" ] && [ "$(wc -l <"$VAE_CSV")" -ge 2 ]; } || die "7-vae-out" "VAE csv 없음"
fi

# ── FIT DONE (downstream/p3는 지용기 님 CPU 몫) ──
hb "FIT DONE"
{ echo "=== MACROPHAGE FIT DONE (3종 fit csv) ==="; date; echo "";
  echo "  floor : $FLOOR_CSV ($(wc -l <"$FLOOR_CSV") 행)";
  echo "  MV    : $MV_CSV ($(wc -l <"$MV_CSV") 행)";
  echo "  VAE   : $VAE_CSV ($(wc -l <"$VAE_CSV") 행)"; echo "";
  echo "→ 지용기 님 downstream: conda run -n scv-preprocess python cross_dataset/p3_concordance_macrophage.py"; } > "$DONE"
log "=== macrophage fit driver 정상 종료 ==="
exit 0
