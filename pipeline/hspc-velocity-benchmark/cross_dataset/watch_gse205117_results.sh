#!/usr/bin/env bash
# GSE205117 결과 자동요약 watcher (무인): 각 단계 완료 sentinel 감지 → RESULTS_SUMMARY.md에 결과+해석 append.
# 세션 끊겨도 결과가 durable하게 기록됨(BIOP02 auto-summary 패턴).
# 실행: setsid bash watch_gse205117_results.sh </dev/null >watch.log 2>&1 &
set -u
W="/home/kkkim/data/gse205117_fullB"
SUM="$W/RESULTS_SUMMARY.md"
touch "$SUM"
log(){ echo "[$(date '+%F %T')] $*"; }
appended_dl=0; appended_gex=0
[ -f "$SUM" ] && grep -q "^## " "$SUM" 2>/dev/null || cat > "$SUM" <<'HDR'
# GSE205117 full B — 결과 자동요약 (watcher 생성, 최신이 아래)

> 5번째 cross-dataset. 각 단계 완료 시 자동 append. 사전등록 대조표 = `manuscript/PREREGISTRATION_gse205117.md`.
HDR
log "=== watcher 시작 (PID $$) ==="

while :; do
  # 다운·변환 완료
  if [ "$appended_dl" = 0 ] && [ -f "$W/DL_DONE" ]; then
    { echo; echo "## $(date '+%F %T') — 다운로드·변환 완료";
      echo "- .sra 8/8, fastq 변환 완료. GEX(rep1): E7.5/E8.0/E8.5/E8.75, ATAC(rep1) 동일.";
      echo "- fastq: \`$W/fastq/\`. 다음: GEX STARsolo Velocyto(자동) → ATAC 처리(수동 설계).";
    } >> "$SUM"; appended_dl=1; log "DL_DONE 요약 append"
  fi
  # GEX Velocyto+QC 완료
  if [ "$appended_gex" = 0 ] && [ -f "$W/GEX_SOLO_DONE" ]; then
    { echo; echo "## $(date '+%F %T') — GEX STARsolo Velocyto + QC 완료";
      echo "### QC (filtered 세포 기준, 4 GEX 런)";
      echo '```'; cat "$W/gex_solo/QC_REPORT.txt" 2>/dev/null; echo '```';
      echo "### 해석";
      echo "- unspliced/spliced 비율이 건강(~0.2–0.4)하고 세포수·nnz가 정상이면 → GSE205117 GEX가 velocity-ready 확정(preflight GO의 full-depth 확증).";
      echo "- ⚠️ 이건 **GEX(RNA) 측만**. 사전등록의 cross-method lag/α 재현 검정은 **chromatin-aware method(MultiVelo/MoFlow/MVVAE)** 필요 → **ATAC 처리 후**에만 가능.";
      echo "### 다음 (수동, 다음 세션)";
      echo "1. ATAC 처리: cellranger-arc(GEX+ATAC 조인트, 표준) 또는 chromap+barcode 매칭. mm10-arc ref 필요.";
      echo "2. GEX+ATAC 통합 AnnData(공유 세포) → RNA-only floor(scVelo) + chromatin-aware 다method fit.";
      echo "3. within/cross-method concordance(α·lag) 산출 → **\`PREREGISTRATION_gse205117.md\` 6개 예측에 통과/실패 기록**(사후구제 금지).";
    } >> "$SUM"; appended_gex=1; log "GEX_SOLO_DONE 요약 append"
  fi
  # 둘 다 기록되면 종료
  [ "$appended_dl" = 1 ] && [ "$appended_gex" = 1 ] && { log "=== 전 단계 요약 완료 — watcher 종료 ==="; break; }
  sleep 300
done
