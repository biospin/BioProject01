#!/usr/bin/env bash
# GSE205117(마우스 gastrulation 10x Multiome) full B 다운로드 — 5번째 cross-dataset.
# aria2c 16연결 병렬로 AWS S3에서 .sra → fasterq-dump 변환. (memory sra-download-slow-aria2c-s3)
# ⚠️ 도구: aria2c·fasterq-dump 모두 /opt/envs/dltools (seqtools엔 sra-tools 없음).
# 실행: setsid bash dl_gse205117_fullB.sh </dev/null >dl_fullB.log 2>&1 &
set -u
WORK="/home/kkkim/data/gse205117_fullB"; SRA="$WORK/sra"; FQ="$WORK/fastq"
mkdir -p "$SRA" "$FQ" "$WORK/tmp"
ARIA=/opt/envs/dltools/bin/aria2c
FQD=/opt/envs/dltools/bin/fasterq-dump
DONE="$WORK/DL_DONE"; PROG="$WORK/DL_PROGRESS"; PARTIAL="$WORK/DL_PARTIAL"; rm -f "$DONE" "$PARTIAL"
GEX="SRR19450575 SRR19450564 SRR19450560 SRR19450574"
ATAC="SRR19450572 SRR19450569 SRR19450557 SRR19450555"
ALL="$GEX $ATAC"
log(){ echo "[$(date '+%F %T')] $*"; }
S3(){ echo "https://sra-pub-run-odp.s3.amazonaws.com/sra/$1/$1"; }
complete(){ [ -s "$SRA/$1.sra" ] && [ ! -f "$SRA/$1.sra.aria2" ]; }   # 완결=파일 존재 + aria2 control 없음
log "=== full B 다운로드 시작 (PID $$) — 8 run(GEX4+ATAC4) ==="

# ── Phase 1: aria2c 다운(파일당 최대 5회 재시도, transient blip 대비) ──
i=0; n=$(echo $ALL|wc -w)
for srr in $ALL; do
  i=$((i+1))
  echo "phase1 다운 $i/$n: $srr ($(date '+%F %T'))" > "$PROG"
  if complete "$srr"; then log "[dl $i/$n] $srr 완결 → skip"; continue; fi
  ok=0
  for try in 1 2 3 4 5; do
    log "[dl $i/$n] $srr aria2c 16연결 (시도 $try)"
    "$ARIA" -x16 -s16 -k1M --max-connection-per-server=16 --continue=true --retry-wait=10 --max-tries=3 \
      --file-allocation=none --console-log-level=warn --summary-interval=60 \
      -d "$SRA" -o "$srr.sra" "$(S3 $srr)" 2>>"$WORK/aria.log"
    if complete "$srr"; then ok=1; log "[dl $i/$n] $srr 완결 ($(du -h "$SRA/$srr.sra"|cut -f1))"; break; fi
    log "[dl $i/$n] $srr 미완결 — 30s 후 재시도"; sleep 30
  done
  [ "$ok" = 1 ] || log "[dl $i/$n] $srr 5회 실패 — 다음으로(재실행 시 이어받음)"
done

# ── 완결성 게이트: 전부 완결돼야 Phase 2 + DL_DONE ──
miss=""; for srr in $ALL; do complete "$srr" || miss="$miss $srr"; done
if [ -n "$miss" ]; then
  { echo "미완결 run:$miss"; echo "재실행: setsid bash cross_dataset/dl_gse205117_fullB.sh …"; date; } > "$PARTIAL"
  log "=== ⚠️ 미완결($miss) — DL_DONE 미생성. 재실행하면 이어받음. ==="; exit 1
fi

# ── Phase 2: fasterq-dump 변환 ──
i=0
for srr in $ALL; do
  i=$((i+1)); echo "phase2 변환 $i/$n: $srr ($(date '+%F %T'))" > "$PROG"
  ls "$FQ/${srr}_2.fastq" >/dev/null 2>&1 && { log "[fq $i/$n] $srr fastq 존재 → skip"; continue; }
  log "[fq $i/$n] $srr fasterq-dump --split-files -e 8"
  "$FQD" "$SRA/$srr.sra" --split-files -e 8 -O "$FQ" -t "$WORK/tmp" >>"$WORK/fqd.log" 2>&1 \
    || { log "[fq $i/$n] $srr 변환 실패"; echo "fq 변환 실패:$srr" >> "$PARTIAL"; }
done
# 변환 완결 확인
fqmiss=""; for srr in $ALL; do ls "$FQ/${srr}_2.fastq" >/dev/null 2>&1 || fqmiss="$fqmiss $srr"; done
[ -z "$fqmiss" ] || { log "=== ⚠️ fastq 미완결($fqmiss) — DL_DONE 미생성 ==="; exit 1; }

{ echo "=== full B 다운로드·변환 DONE ==="; date; echo "GEX:$GEX"; echo "ATAC:$ATAC";
  echo "fastq: $FQ"; ls "$FQ"/*_1.fastq "$FQ"/*_2.fastq 2>/dev/null | sed 's#.*/##'; } > "$DONE"
log "=== DONE — sra:$SRA fastq:$FQ ==="
