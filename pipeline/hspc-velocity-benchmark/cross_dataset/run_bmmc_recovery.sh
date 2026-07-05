#!/usr/bin/env bash
# GSE194122 human BMMC (donor09) cross-dataset 재현 무인 드라이버 — 로그아웃돼도 끝까지.
# 모든 stage idempotent(산출물 있으면 skip) → 재실행이 velocyto 등 값비싼 stage를 재수행 안 함.
# stage: [0]BAM download [1]ref genes.gtf [2]rmsk gtf(optional) [3]velocyto run
#        [4]build [5]floor [6]MultiVelo [7]VAE [8]P3 concordance
# git 커밋 안 함(사용자 복귀 후 수동). 실행(반드시 detach):
#   setsid bash run_bmmc_recovery.sh </dev/null >bmmc_driver.log 2>&1 &
set -u

ROOT="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
SCRIPTS="$ROOT/scripts"
CROSS="$ROOT/cross_dataset"
RESULTS="$ROOT/results"
DATA="$ROOT/data"
CONDA="/home/kkkim/miniconda3/bin/conda"

DS="GSE194122_bmmc"
CONFIG="../cross_dataset/config_${DS}.py"        # p1_config가 SCRIPTS/에서 상대해석
SUFFIX="_${DS}"

# ── 경로 ──
GSE_DIR="$DATA/GSE194122"
BAM="$GSE_DIR/site4_donor09_multiome_gex.possorted_genome_bam.bam"
BAM_EXPECT_SIZE=28660822562
# 공개 S3(no-sign) → HTTPS 직접 주소지정 가능(헤더 스트리밍으로 검증). curl -C - 로 resume.
BAM_URL="https://sra-pub-src-2.s3.amazonaws.com/SRR17693266/site4_donor09_multiome_gex.possorted_genome_bam.bam.1"
BCFILE="$GSE_DIR/s4d9_barcodes_CB_dash1.txt"

REF_TGZ="$DATA/ref/refdata-cellranger-arc-GRCh38-2020-A-2.0.0.tar.gz"
REF_GTF="$DATA/ref/refdata-cellranger-arc-GRCh38-2020-A/genes/genes.gtf"
RMSK_GTF="$DATA/ref/GRCh38_rmsk.gtf"
RMSK_TXT="$DATA/ref/hg38_rmsk.txt.gz"

VELO_OUT="$DATA/GSE194122_bmmc_velocyto"
SAMPLEID="GSE194122_s4d9"

PROC="$DATA/processed_${DS}"
OUT_RNA="$PROC/rna_spliced_unspliced.h5ad"
OUT_ATAC="$PROC/atac_gene.h5ad"

FLOOR_CSV="$RESULTS/rna_only_dynamical_genes${SUFFIX}.csv"
MV_CSV="$RESULTS/multivelo_genes${SUFFIX}.csv"
VAE_CSV="$RESULTS/multivelovae_genes${SUFFIX}.csv"
CONC_MD="$RESULTS/concordance_${DS}.md"

# ── sentinel / 로그 ──
DONE="$CROSS/BMMC_DONE"
FAILED="$CROSS/BMMC_FAILED"
PROGRESS="$CROSS/BMMC_PROGRESS"

# samtools sort 임시 파일을 대용량 디스크로 (system /tmp 소진 방지 — advisor 경고)
export TMPDIR="$DATA/tmp_bmmc"; mkdir -p "$TMPDIR"
export HDF5_USE_FILE_LOCKING=FALSE

log() { echo "[$(date '+%F %T')] $*"; }
hb()  { { echo "=== BMMC RECOVERY PROGRESS ==="; echo "updated: $(date '+%F %T')";
          echo "driver : PID $$ (PPID $PPID)"; echo "stage  : $1";
          echo "BAM    : $( [ -f "$BAM" ] && echo "$(stat -c%s "$BAM")/$BAM_EXPECT_SIZE B" || echo missing )";
          echo "loom   : $( ls "$VELO_OUT"/*.loom 2>/dev/null | head -1 || echo none )";
          echo "floor  : $( [ -f "$FLOOR_CSV" ] && echo "$(wc -l <"$FLOOR_CSV") 행" || echo - )";
          echo "MV     : $( [ -f "$MV_CSV" ] && echo "$(wc -l <"$MV_CSV") 행" || echo - )";
          echo "VAE    : $( [ -f "$VAE_CSV" ] && echo "$(wc -l <"$VAE_CSV") 행" || echo - )";
          echo "conc   : $( [ -f "$CONC_MD" ] && echo exists || echo - )"; } > "$PROGRESS"; }
die() { log "FAILED at $1"; { echo "FAILED at $1"; echo "$2"; date; } > "$FAILED"; exit 1; }

rm -f "$DONE" "$FAILED"
log "=== BMMC recovery driver 시작 (PID $$, PPID $PPID, SID $(ps -o sid= -p $$|tr -d ' ')) ==="

# ── [0] BAM download (idempotent: 정확한 크기면 skip) ──
hb "0 BAM download"
if [ -f "$BAM" ] && [ "$(stat -c%s "$BAM")" = "$BAM_EXPECT_SIZE" ]; then
  log "[0] BAM 이미 완전(size ok) → skip"
else
  log "[0] BAM download 시작(curl -C - resume) → $BAM"
  curl -fsSL -C - -o "$BAM" "$BAM_URL" || die "0-BAM-download" "curl BAM 다운로드 실패"
  [ "$(stat -c%s "$BAM")" = "$BAM_EXPECT_SIZE" ] || die "0-BAM-size" "다운로드 크기 불일치 $(stat -c%s "$BAM")!=$BAM_EXPECT_SIZE"
fi

# ── [1] cellranger-arc reference genes.gtf (tar 자체 소유; resume 다운로드) ──
REF_URL="https://cf.10xgenomics.com/supp/cell-arc/refdata-cellranger-arc-GRCh38-2020-A-2.0.0.tar.gz"
hb "1 ref genes.gtf"
if [ -f "$REF_GTF" ]; then
  log "[1] genes.gtf 이미 존재 → skip"
else
  # 타르볼이 없거나 손상(gzip 무결성 실패)이면 resume 다운로드(-C -)로 완성.
  if [ ! -f "$REF_TGZ" ] || ! gzip -t "$REF_TGZ" 2>/dev/null; then
    log "[1] reference 타르볼 (재)다운로드 resume: $REF_URL"
    curl -fsSL -C - -o "$REF_TGZ" "$REF_URL" || die "1-ref-dl" "reference 타르볼 다운로드 실패"
    gzip -t "$REF_TGZ" 2>/dev/null || die "1-ref-integrity" "타르볼 gzip 무결성 실패"
  fi
  log "[1] genes.gtf 추출 (tar -xz)"
  ( cd "$DATA/ref" && tar -xzf "$REF_TGZ" refdata-cellranger-arc-GRCh38-2020-A/genes/genes.gtf ) \
    || die "1-ref-extract" "genes.gtf 추출 실패"
  [ -f "$REF_GTF" ] || die "1-ref-missing" "추출 후 genes.gtf 없음"
fi

# ── [2] rmsk GTF (optional; 실패해도 velocyto는 -m 없이 진행) ──
hb "2 rmsk gtf"
USE_RMSK=1
if [ -f "$RMSK_GTF" ]; then
  log "[2] rmsk gtf 이미 존재 → skip"
else
  log "[2] UCSC hg38 rmsk 다운로드 + GTF 변환"
  if curl -fsSL -o "$RMSK_TXT" "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/rmsk.txt.gz"; then
    # UCSC rmsk.txt: col6=genoName col7=genoStart(0-based) col8=genoEnd col10=strand col11=repName
    zcat "$RMSK_TXT" | awk 'BEGIN{OFS="\t"}
      { print $6,"rmsk","exon",$7+1,$8,".",$10,".","gene_id \""$11"\"; transcript_id \""$11"\";" }' \
      > "$RMSK_GTF" 2>/dev/null
    if [ -s "$RMSK_GTF" ]; then log "[2] rmsk gtf 생성 ($(wc -l <"$RMSK_GTF") lines)"; else USE_RMSK=0; log "[2] rmsk 변환 실패 → -m 없이 진행"; fi
  else
    USE_RMSK=0; log "[2] rmsk 다운로드 실패 → -m 없이 진행(문서화)"
  fi
fi
[ -s "$RMSK_GTF" ] || USE_RMSK=0

# ── [3] velocyto run (loom 있으면 skip; cell-sort는 대용량/장시간) ──
hb "3 velocyto run"
if ls "$VELO_OUT"/*.loom >/dev/null 2>&1; then
  log "[3] loom 이미 존재 → skip: $(ls "$VELO_OUT"/*.loom | head -1)"
else
  mkdir -p "$VELO_OUT"
  RMSK_ARG=(); [ "$USE_RMSK" = 1 ] && RMSK_ARG=(-m "$RMSK_GTF")
  log "[3] velocyto run 시작 (rmsk=$USE_RMSK, TMPDIR=$TMPDIR)"
  "$CONDA" run --no-capture-output -n velocyto velocyto run \
      -b "$BCFILE" -o "$VELO_OUT" -e "$SAMPLEID" \
      "${RMSK_ARG[@]}" -@ 8 --samtools-memory 4000 \
      "$BAM" "$REF_GTF" || die "3-velocyto" "velocyto run 실패"
  ls "$VELO_OUT"/*.loom >/dev/null 2>&1 || die "3-velocyto-loom" "velocyto 후 loom 없음"
fi

# ── [4] build+finalize (scv-preprocess) → processed rna + atac_gene ──
hb "4 build"
if [ -f "$OUT_RNA" ] && [ -f "$OUT_ATAC" ]; then
  log "[4] processed rna+atac_gene 이미 존재 → skip"
else
  log "[4] build_GSE194122_bmmc.py"
  ( cd "$CROSS" && "$CONDA" run --no-capture-output -n scv-preprocess python -u build_GSE194122_bmmc.py ) \
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

# ── [7] MultiVeloVAE (torch; dl_prep → VAE) ──
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

# ── [8] P3 concordance ──
hb "8 P3 concordance"
log "[8] p3_concordance_GSE194122_bmmc.py"
( cd "$CROSS" && "$CONDA" run --no-capture-output -n scv-preprocess python -u p3_concordance_GSE194122_bmmc.py ) \
  || die "8-p3" "P3 concordance 실패"
[ -f "$CONC_MD" ] || die "8-p3-out" "concordance md 없음"

# ── DONE ──
hb "DONE"
{ echo "=== BMMC RECOVERY DONE ==="; date; echo "";
  echo "산출물:";
  echo "  loom  : $(ls "$VELO_OUT"/*.loom | head -1)";
  echo "  rna   : $OUT_RNA";
  echo "  atac  : $OUT_ATAC";
  echo "  floor : $FLOOR_CSV ($(wc -l <"$FLOOR_CSV") 행)";
  echo "  MV    : $MV_CSV ($(wc -l <"$MV_CSV") 행)";
  echo "  VAE   : $VAE_CSV ($(wc -l <"$VAE_CSV") 행)";
  echo "  conc  : $CONC_MD"; echo "";
  echo "--- 판정 발췌 ---"; grep -A2 "^### → " "$CONC_MD" 2>/dev/null; } > "$DONE"
log "=== BMMC recovery driver 정상 종료 ==="
exit 0
