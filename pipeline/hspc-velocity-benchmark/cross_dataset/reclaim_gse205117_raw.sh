#!/usr/bin/env bash
# GSE205117 raw 자동정리 — count matrix(velocity 분석의 압축 중간산물)가 검증된 뒤에만 .sra/fastq 삭제.
# BIOP02 "embedding 성공 후 slide 삭제"의 velocity판. raw는 공개 SRA라 재다운 가능한 캐시(sha256 provenance 보존).
#
# ⚠️ 기본은 DRY-RUN(무엇을 지울지·얼마나 확보할지만 출력). 실제 삭제는 --execute 플래그 필요.
# 두 단계:
#  [조기회수] 완료된 GEX 런의 index read(_3/_4, STAR가 안 씀 — _1/_2만 사용). 전체 게이트와 독립, GEX 완료 즉시 회수(런당 ~300G).
#  [전체 raw] .sra + fastq 전량 — 아래 게이트 3중 통과 시에만:
#   (a) 4개 GEX 런 전부 STARsolo Velocyto matrix 산출 + nnz 정상, (b) ATAC 처리 완료, (c) processed spliced/unspliced h5ad 존재.
# ⚠️ 실행은 사람이 눈으로 확인 후(watchdog 자동트리거 안 함, kkkim 정책 2026-07-13). 되돌릴 수 없고 재다운 반나절.
# 사용: bash reclaim_gse205117_raw.sh            # dry-run(안전, 삭제 안 함)
#       bash reclaim_gse205117_raw.sh --execute  # 게이트 통과 시 실제 삭제
set -u
W="/home/kkkim/data/gse205117_fullB"
R="/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark"
EXECUTE=0; [ "${1:-}" = "--execute" ] && EXECUTE=1
declare -A GEX=( [E7.5]=SRR19450575 [E8.0]=SRR19450564 [E8.5]=SRR19450560 [E8.75]=SRR19450574 )
ATAC_SRR="SRR19450572 SRR19450569 SRR19450557 SRR19450555"
log(){ echo "[$(date '+%F %T')] $*"; }
GATE_OK=1; fail(){ log "  ✗ 게이트 실패: $*"; GATE_OK=0; }

log "=== GSE205117 raw 정리 $([ $EXECUTE = 1 ] && echo '(EXECUTE)' || echo '(DRY-RUN)') ==="

# ── 조기회수: GEX index read(_3/_4) — STAR readFilesIn은 _1(barcode)/_2(cDNA)만 사용 → _3/_4는 미사용.
#    ATAC(R1/R2/R3 전부 사용)는 제외. 각 GEX 런의 Gene/Summary.csv 존재 시(=해당 런 STARsolo 완료) 삭제 가능.
#    전체 raw 게이트와 독립 — GEX 완료 즉시 확보(런당 ~300G). ──
log "[조기회수] 완료된 GEX 런의 index read(_3/_4, STAR 미사용) 정리"
idx_freed=0
for tp in E7.5 E8.0 E8.5 E8.75; do
  srr=${GEX[$tp]}; gsum="$W/gex_solo/$srr/${srr}_Solo.out/Gene/Summary.csv"
  if [ ! -f "$gsum" ]; then log "  · $tp($srr) STARsolo 미완 → index read 아직 보류(사용 중일 수 있음)"; continue; fi
  for suf in 3 4; do
    f="$W/fastq/${srr}_${suf}.fastq"
    [ -s "$f" ] || continue
    sz=$(du -h "$f" 2>/dev/null | cut -f1)
    if [ "$EXECUTE" -eq 1 ]; then rm -f "$f" && log "  ✓ 삭제 ${srr}_${suf}.fastq ($sz)"; idx_freed=1
    else log "  [dry-run] 삭제대상 ${srr}_${suf}.fastq ($sz) — GEX 미사용 index read"; fi
  done
done
[ "$EXECUTE" -eq 1 ] && [ "$idx_freed" -eq 1 ] && log "  → GEX index read 회수 완료(_1/_2 cDNA·barcode는 전체 게이트까지 보존)"

# ── 게이트 (a) GEX 4런 Velocyto matrix 존재 + nnz 정상 ──
log "[게이트 a] GEX STARsolo Velocyto matrix 검증"
for tp in E7.5 E8.0 E8.5 E8.75; do
  srr=${GEX[$tp]}; vraw="$W/gex_solo/$srr/${srr}_Solo.out/Velocyto/raw"
  gsum="$W/gex_solo/$srr/${srr}_Solo.out/Gene/Summary.csv"
  [ -f "$gsum" ] || { fail "$tp($srr) Gene/Summary.csv 없음(미완)"; continue; }
  for m in spliced.mtx unspliced.mtx barcodes.tsv; do
    [ -s "$vraw/$m" ] || fail "$tp($srr) Velocyto/$m 없음/빈파일"
  done
  [ -s "$vraw/spliced.mtx" ] && log "  ✓ $tp($srr) matrix 존재 ($(du -h "$vraw/spliced.mtx"|cut -f1))"
done

# ── 게이트 (b) ATAC 처리 완료 여부 (다운스트림 설계 후 산출 예정 — 없으면 보류) ──
log "[게이트 b] ATAC 처리 산출 확인"
ATAC_DONE_MARK="$W/ATAC_SOLO_DONE"   # ATAC 파이프라인이 완료 시 남길 마커(미설계 — 현재 없음)
if [ -f "$ATAC_DONE_MARK" ]; then log "  ✓ ATAC 처리 완료 마커 존재";
else fail "ATAC 처리 미완/미설계 — ATAC fastq는 아직 필요(삭제 보류)"; fi

# ── 게이트 (c) processed spliced/unspliced h5ad 존재 ──
log "[게이트 c] processed velocity h5ad 확인"
PROC_H5="$R/data/processed_gse205117/rna_spliced_unspliced.h5ad"   # build 단계 산출(미설계 — 예정 경로)
if [ -s "$PROC_H5" ]; then log "  ✓ processed h5ad 존재 ($(du -h "$PROC_H5"|cut -f1))";
else fail "processed h5ad($PROC_H5) 없음 — build 단계 후 재확인"; fi

# ── 삭제 대상·확보량 산정 ──
echo; log "── 정리 대상 ──"
SRA_SZ=$(du -sh "$W/sra" 2>/dev/null | cut -f1); FQ_SZ=$(du -sh "$W/fastq" 2>/dev/null | cut -f1)
log "  삭제 후보: $W/sra ($SRA_SZ) + $W/fastq ($FQ_SZ)"
log "  보존: gex_solo/*/Solo.out matrix, processed h5ad, results/*.csv, download_manifest(sha256 provenance)"
log "  근거: 공개 SRA → 재다운 가능. 재정렬 필요 시 accession에서 복구."

if [ "$GATE_OK" -ne 1 ]; then
  log "=== ❌ 게이트 미통과 → 삭제 안 함(raw 유지). 위 실패 항목 해소 후 재실행. ==="; exit 1
fi
log "=== ✅ 게이트 통과 ==="
if [ "$EXECUTE" -ne 1 ]; then
  log "=== DRY-RUN 종료 — 실제 삭제하려면 --execute. (kkkim 확인 후) ==="; exit 0
fi

# ── 실제 삭제 (게이트 통과 + --execute) ──
log "── 삭제 실행 ──"
rm -rf "$W/sra" && log "  ✓ sra 삭제"
rm -rf "$W/fastq" && log "  ✓ fastq 삭제"
{ echo "=== GSE205117 raw 정리 완료 ==="; date; echo "삭제: sra($SRA_SZ)+fastq($FQ_SZ). 보존: Solo.out matrix+processed h5ad+results csv."; } > "$W/RAW_RECLAIMED"
log "=== 완료 — 확보. 재현: SRR accession 재다운(download_manifest.tsv sha256). ==="
