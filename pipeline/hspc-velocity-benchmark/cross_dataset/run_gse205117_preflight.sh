#!/usr/bin/env bash
# BIOP01 5번째 cross-dataset 후보 GSE205117(마우스 gastrulation 10x Multiome) nnz GO/NO-GO 스모크.
# skin(SHARE-seq) 실패요인(barcode 부재·비연속) 없음이 확인됨: GEX run = R1 16bp CB + 12bp UMI(연속) + R2 90bp cDNA.
# → fastq-dump subset → STARsolo CB_UMI_Simple + --soloFeatures Velocyto → nnz(top-N 세포, macrophage GO 35.6% 대조).
# 실행: setsid bash run_gse205117_preflight.sh </dev/null >gse205117_preflight.log 2>&1 &
set -u
ROOT="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
IDX="$ROOT/data/ref/mm10_star"
NSPOT="${NSPOT:-20000000}"          # subset spots (env로 조절: 20M/60M 등)
WORK="/home/kkkim/data/gse205117_preflight${WORKSUFFIX:-}"; mkdir -p "$WORK"
SEQ=/opt/envs/seqtools/bin
SRR="SRR19450561"        # GEX(RNA-Seq) run 1개
DONE="$WORK/DONE"; FAIL="$WORK/FAIL"; rm -f "$DONE" "$FAIL"
log(){ echo "[$(date '+%F %T')] $*"; }
die(){ log "FAIL: $*"; echo "$*" > "$FAIL"; exit 1; }
cd "$WORK"
log "=== GSE205117 preflight 시작 (PID $$) — $SRR subset $NSPOT spots ==="

# ── A) GEX fastq subset (R1=barcode 28bp, R2=cDNA 90bp) ──
if [ ! -s "${SRR}_2.fastq" ]; then
  log "[A] fastq-dump subset (network stream, ~10-20min)"
  "$SEQ/fastq-dump" -X "$NSPOT" --split-files "$SRR" -O "$WORK" 2>>"$WORK/fqdump.log" \
    || die "fastq-dump 실패($SRR)"
fi
R1=$(ls "${SRR}_1.fastq" 2>/dev/null); R2=$(ls "${SRR}_2.fastq" 2>/dev/null)
[ -s "$R1" ] && [ -s "$R2" ] || die "R1/R2 fastq 없음"
log "[A] R1(barcode) $(awk 'NR==2{print length($0)}' "$R1")bp / R2(cDNA) $(awk 'NR==2{print length($0)}' "$R2")bp"

# ── B) STARsolo CB_UMI_Simple + Velocyto (whitelist None, 스모크) ──
log "[B] STARsolo align+Velocyto (index 재사용)"
"$SEQ/STAR" --runMode alignReads --genomeDir "$IDX" \
  --readFilesIn "$R2" "$R1" \
  --soloType CB_UMI_Simple --soloCBstart 1 --soloCBlen 16 --soloUMIstart 17 --soloUMIlen 12 \
  --soloCBwhitelist None --soloFeatures Gene Velocyto \
  --runThreadN 12 --outSAMtype None \
  --outFileNamePrefix "$WORK/solo_" >>"$WORK/star.log" 2>&1 || die "STARsolo 실패"

# ── C) nnz(top-N 세포 기준, macrophage 35.6% 대조) ──
log "[C] nnz 계산"
VELO="$WORK/solo_Solo.out/Velocyto/raw"
"$SEQ/python" - "$VELO" <<'PY' || die "nnz 계산 실패"
import sys, scipy.io as sio, numpy as np, os
d=sys.argv[1]
S=sio.mmread(os.path.join(d,"spliced.mtx")).tocsc()   # genes x cells
U=sio.mmread(os.path.join(d,"unspliced.mtx")).tocsc()
tot=np.asarray(S.sum(0)).ravel()
topN=min(5000, (tot>0).sum())
idx=np.argsort(tot)[::-1][:topN]
Ssub=S[:,idx]; Usub=U[:,idx]
def nnz(M): return 100.0*(M!=0).sum()/ (M.shape[0]*M.shape[1])
print(f"[nnz] top{topN} cells | genes={S.shape[0]}")
print(f"[nnz] spliced   nnz={nnz(Ssub):6.2f}%  total={int(Ssub.sum()):,}")
print(f"[nnz] unspliced nnz={nnz(Usub):6.2f}%  total={int(Usub.sum()):,}")
us=nnz(Usub)
print(f"[nnz] SUMMARY spliced={nnz(Ssub):.2f}% unspliced={us:.2f}% (macrophage GO=35.6%)")
print(f"[nnz] 판정: {'GO 후보(충분)' if us>=10 else '약함-확대검토' if us>=2 else 'NO-GO(약함)'}")
PY

{ echo "=== GSE205117 preflight DONE ==="; date; grep "\[nnz\] SUMMARY" "$WORK/gse205117_preflight.log" 2>/dev/null; } > "$DONE"
log "=== DONE — nnz SUMMARY는 로그 하단 참조 ==="
