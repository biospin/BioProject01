#!/usr/bin/env bash
# GSE205117 ATAC fragments 다운로드 (processed fragments.tsv.gz, sample별 제공 — raw 정렬 불필요).
# 4 rep1 시점(GEX와 매칭). NCBI DNS 간헐 → curl 재시도 루프 + gzip 무결성 검증 + sha256 provenance.
# 실행(detached): setsid bash dl_gse205117_atac_frag.sh </dev/null >dl_atac_frag.log 2>&1 &
set -u
W="/home/kkkim/data/gse205117_fullB/atac_frag"; mkdir -p "$W"
DONE="$W/ATAC_FRAG_DONE"; PROG="$W/ATAC_FRAG_PROGRESS"; PROV="$W/atac_frag_provenance.tsv"
rm -f "$DONE"
BASE="https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM6205nnn"
# 시점 → GSM_파일명
declare -A F=(
  [E7.5]="GSM6205427/suppl/GSM6205427_E7.5_rep1_ATAC_fragments.tsv.gz"
  [E8.0]="GSM6205430/suppl/GSM6205430_E8.0_rep1_ATAC_fragments.tsv.gz"
  [E8.5]="GSM6205434/suppl/GSM6205434_E8.5_rep1_ATAC_fragments.tsv.gz"
  [E8.75]="GSM6205436/suppl/GSM6205436_E8.75_rep1_ATAC_fragments.tsv.gz"
)
log(){ echo "[$(date '+%F %T')] $*"; }
log "=== ATAC fragments 다운로드 시작 (PID $$, PPID $PPID) ==="
[ -f "$PROV" ] || echo -e "timepoint\tfilename\tbytes\tsha256\tgzip_ok" > "$PROV"
fail=0
for tp in E7.5 E8.0 E8.5 E8.75; do
  rel=${F[$tp]}; fn=$(basename "$rel"); dst="$W/$fn"; url="$BASE/$rel"
  echo "downloading $tp $fn ($(date '+%F %T'))" > "$PROG"
  # 이미 완결(gzip valid + per-file sentinel)이면 skip
  if [ -f "$W/.${fn}.ok" ] && gzip -t "$dst" 2>/dev/null; then log "[$tp] 이미 완결 → skip"; continue; fi
  # curl 전체 GET(-C - resume) + 재시도. DNS('general failure')·연결 끊김은 재시도로 이어받음.
  # (990B 'Object not found!' HTML은 URL 오타였음 — 이제 /suppl/ 정상. 방어적 magic 체크는 유지.)
  ok=0
  for attempt in $(seq 1 40); do
    if [ -f "$dst" ]; then
      magic=$(head -c2 "$dst" | od -An -tx1 | tr -d ' ')
      [ "$magic" != "1f8b" ] && [ "$(stat -c%s "$dst")" -lt 100000 ] && { log "[$tp] 비-gzip 오류partial(magic=$magic) 삭제"; rm -f "$dst"; }
    fi
    log "[$tp] curl attempt $attempt → $fn (현재 bytes=$(stat -c%s "$dst" 2>/dev/null || echo 0))"
    curl -sL --connect-timeout 30 --max-time 3600 -C - -o "$dst" "$url"
    if [ -s "$dst" ] && gzip -t "$dst" 2>/dev/null; then ok=1; break; fi
    log "[$tp] attempt $attempt 미완결(bytes=$(stat -c%s "$dst" 2>/dev/null || echo 0)) → 재시도"
    sleep 15
  done
  if [ "$ok" -ne 1 ]; then log "[$tp] $fn 다운로드 실패(12회) → FAIL"; fail=$((fail+1)); continue; fi
  sz=$(stat -c%s "$dst"); sha=$(sha256sum "$dst" | cut -d' ' -f1)
  touch "$W/.${fn}.ok"
  # provenance append (중복 방지)
  grep -q "$fn" "$PROV" || echo -e "${tp}\t${fn}\t${sz}\t${sha}\tOK" >> "$PROV"
  log "[$tp] 완료 $fn (${sz} bytes, sha256=${sha:0:16}…)"
  # E7.5 landing 신호(바코드 조인 de-risk 트리거)
  [ "$tp" = "E7.5" ] && touch "$W/.E7.5_LANDED"
done
if [ "$fail" -eq 0 ]; then
  { echo "=== ATAC fragments DONE ==="; date; echo; cat "$PROV"; } > "$DONE"
  log "=== ATAC fragments 전부 완료 → $DONE ==="
else
  log "=== $fail/4 실패 — ATAC_FRAG_DONE 미생성 ==="
fi
