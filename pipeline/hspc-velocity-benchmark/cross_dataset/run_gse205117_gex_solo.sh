#!/usr/bin/env bash
# GSE205117 full B 후속 자동화(무인): 다운(DL_DONE) 대기 → GEX 4런 STARsolo Velocyto(full) → 세포필터+nnz QC → GEX_SOLO_DONE.
# ⚠️ ATAC 처리·세포통합·P1~P3는 설계·검증 필요 → 여기서 멈추고 리포트(미검증 heavy 무인실행 방지).
# 실행: setsid bash run_gse205117_gex_solo.sh </dev/null >gex_solo.log 2>&1 &
set -u
W="/home/kkkim/data/gse205117_fullB"
IDX="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark/data/ref/mm10_star"
SEQ=/opt/envs/seqtools/bin
PY=/home/kkkim/miniconda3/envs/scv-preprocess/bin/python   # scipy 정상 python
FQ="$W/fastq"; OUT="$W/gex_solo"; mkdir -p "$OUT" "$W/tmp"
DONE="$W/GEX_SOLO_DONE"; FAIL="$W/GEX_SOLO_FAIL"; PROG="$W/GEX_SOLO_PROGRESS"; rm -f "$DONE" "$FAIL"
# GEX rep1 4런 (E7.5/E8.0/E8.5/E8.75)
declare -A GEX=( [E7.5]=SRR19450575 [E8.0]=SRR19450564 [E8.5]=SRR19450560 [E8.75]=SRR19450574 )
log(){ echo "[$(date '+%F %T')] $*"; }
die(){ log "FAIL: $*"; echo "$*" > "$FAIL"; exit 1; }
log "=== GEX solo 후속 자동화 시작 (PID $$) — DL_DONE 대기 ==="

# ── 0) 다운·변환 완료 대기 ──
echo "wait DL_DONE ($(date '+%F %T'))" > "$PROG"
i=0; until [ -f "$W/DL_DONE" ]; do sleep 120; i=$((i+1)); [ $((i%30)) -eq 0 ] && log "…DL_DONE 대기 중 ($((i*2))분)"; done
log "DL_DONE 감지 → GEX 처리 시작"

# ── 1) 각 GEX 런: STARsolo CB_UMI_Simple + Velocyto (full depth) ──
REPORT="$OUT/QC_REPORT.txt"; : > "$REPORT"
for tp in E7.5 E8.0 E8.5 E8.75; do
  srr=${GEX[$tp]}; R1="$FQ/${srr}_1.fastq"; R2="$FQ/${srr}_2.fastq"; od="$OUT/$srr"
  echo "STARsolo $tp($srr) ($(date '+%F %T'))" > "$PROG"
  [ -s "$R1" ] && [ -s "$R2" ] || { log "[$tp] fastq 없음($R1/$R2) → skip"; echo "$tp $srr: fastq 없음" >> "$REPORT"; continue; }
  if [ -f "$od/${srr}_Solo.out/Gene/Summary.csv" ]; then log "[$tp] 이미 완료 → skip"; else
    log "[$tp] $srr STARsolo Velocyto (R1 barcode 28bp / R2 cDNA)"
    mkdir -p "$od"
    "$SEQ/STAR" --runMode alignReads --genomeDir "$IDX" \
      --readFilesIn "$R2" "$R1" \
      --soloType CB_UMI_Simple --soloCBstart 1 --soloCBlen 16 --soloUMIstart 17 --soloUMIlen 12 \
      --soloCBwhitelist None --soloFeatures Gene Velocyto \
      --soloCellFilter CellRanger2.2 3000 0.99 10 \
      --runThreadN 12 --outSAMtype None \
      --outFileNamePrefix "$od/${srr}_" >>"$W/star_gex.log" 2>&1 || { log "[$tp] STARsolo 실패"; echo "$tp $srr: STARsolo FAIL" >> "$REPORT"; continue; }
  fi
  # nnz QC (filtered 세포 기준)
  "$PY" - "$od/${srr}_Solo.out" "$tp" "$srr" >> "$REPORT" 2>>"$W/nnz_gex.log" <<'PY'
import sys,os,scipy.io as sio,numpy as np
base,tp,srr=sys.argv[1],sys.argv[2],sys.argv[3]
raw=os.path.join(base,"Velocyto","raw"); filt=os.path.join(base,"Gene","filtered")
try:
    fb=set(open(os.path.join(filt,"barcodes.tsv")).read().split())
    rb=open(os.path.join(raw,"barcodes.tsv")).read().split()
    idx=[i for i,b in enumerate(rb) if b in fb]
    S=sio.mmread(os.path.join(raw,"spliced.mtx")).tocsc()[:,idx]
    U=sio.mmread(os.path.join(raw,"unspliced.mtx")).tocsc()[:,idx]
    nnz=lambda M:100.0*(M!=0).sum()/(M.shape[0]*M.shape[1])
    print(f"{tp} {srr}: cells={len(idx)} spliced_nnz={nnz(S):.1f}% unspliced_nnz={nnz(U):.1f}% u/s={U.sum()/max(S.sum(),1):.3f}")
except Exception as e:
    print(f"{tp} {srr}: nnz 계산실패 {e}")
PY
  log "[$tp] 완료"
done

{ echo "=== GEX solo DONE ==="; date; echo "--- QC(filtered 세포 기준) ---"; cat "$REPORT";
  echo; echo "다음 단계(설계 필요, 무인 미실행): ATAC 처리(cellranger-arc/chromap) + GEX 세포 매칭 → MultiVelo 등 → P1~P3 concordance."; } > "$DONE"
log "=== GEX solo 완료 — QC: $REPORT / 다음=ATAC 설계 ==="
