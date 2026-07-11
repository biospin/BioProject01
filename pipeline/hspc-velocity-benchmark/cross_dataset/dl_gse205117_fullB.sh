#!/usr/bin/env bash
# GSE205117(마우스 gastrulation 10x Multiome) full B 다운로드 — 5번째 cross-dataset.
# aria2c 16연결 병렬로 AWS S3에서 .sra → fasterq-dump 변환. 한국↔미국 국제구간 병목 회피(memory sra-download-slow-aria2c-s3).
# 실행: setsid bash dl_gse205117_fullB.sh </dev/null >dl_fullB.log 2>&1 &
set -u
WORK="/home/kkkim/data/gse205117_fullB"; SRA="$WORK/sra"; FQ="$WORK/fastq"
mkdir -p "$SRA" "$FQ"
ARIA=/opt/envs/dltools/bin/aria2c
FQD=/opt/envs/seqtools/bin/fasterq-dump
DONE="$WORK/DL_DONE"; PROG="$WORK/DL_PROGRESS"; rm -f "$DONE"
# full B: GEX rep1 4개 + ATAC rep1 4개 (E7.5/E8.0/E8.5/E8.75)
GEX="SRR19450575 SRR19450564 SRR19450560 SRR19450574"
ATAC="SRR19450572 SRR19450569 SRR19450557 SRR19450555"
ALL="$GEX $ATAC"
log(){ echo "[$(date '+%F %T')] $*"; }
S3(){ echo "https://sra-pub-run-odp.s3.amazonaws.com/sra/$1/$1"; }
log "=== full B 다운로드 시작 (PID $$) — 8 run(GEX4+ATAC4) ==="

# ── Phase 1: aria2c 16연결 병렬 다운(순차 파일, 파일당 full 병렬; resume) ──
i=0; n=$(echo $ALL|wc -w)
for srr in $ALL; do
  i=$((i+1)); out="$SRA/$srr.sra"
  echo "phase1 다운 $i/$n: $srr ($(date '+%F %T'))" > "$PROG"
  if [ -s "$out" ] && "$FQD" --version >/dev/null 2>&1 && [ ! -f "$out.aria2" ]; then
    log "[dl $i/$n] $srr 이미 완료 → skip"; continue
  fi
  log "[dl $i/$n] $srr aria2c 16연결"
  "$ARIA" -x16 -s16 -k1M --max-connection-per-server=16 --continue=true \
    --file-allocation=none --console-log-level=warn --summary-interval=30 \
    -d "$SRA" -o "$srr.sra" "$(S3 $srr)" 2>>"$WORK/aria.log" \
    || { log "[dl $i/$n] $srr aria2c 실패 — 재시도 1회"; "$ARIA" -x16 -s16 --continue=true -d "$SRA" -o "$srr.sra" "$(S3 $srr)" 2>>"$WORK/aria.log" || log "[dl] $srr 실패(계속)"; }
  log "[dl $i/$n] $srr 완료 ($(du -h "$out" 2>/dev/null|cut -f1))"
done

# ── Phase 2: fasterq-dump 변환(로컬, 멀티스레드) ──
i=0
for srr in $ALL; do
  i=$((i+1)); out="$SRA/$srr.sra"
  echo "phase2 변환 $i/$n: $srr ($(date '+%F %T'))" > "$PROG"
  [ -s "$out" ] || { log "[fq $i/$n] $srr .sra 없음 → skip"; continue; }
  ls "$FQ/${srr}"*.fastq >/dev/null 2>&1 && { log "[fq $i/$n] $srr fastq 존재 → skip"; continue; }
  log "[fq $i/$n] $srr fasterq-dump --split-files -e 8"
  "$FQD" "$out" --split-files -e 8 -O "$FQ" -t "$WORK/tmp" >>"$WORK/fqd.log" 2>&1 \
    || log "[fq $i/$n] $srr 변환 실패(계속)"
done

{ echo "=== full B 다운로드·변환 DONE ==="; date;
  echo "GEX(rep1): $GEX"; echo "ATAC(rep1): $ATAC";
  echo "fastq: $FQ"; ls -la "$FQ" 2>/dev/null | tail -20; } > "$DONE"
log "=== DONE — sra:$SRA fastq:$FQ ==="
