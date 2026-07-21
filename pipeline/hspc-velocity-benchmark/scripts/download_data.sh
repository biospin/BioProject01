#!/usr/bin/env bash
#
# download_data.sh — fetch GSE209878 (Human HSPC 10x Multiome) essential files.
#
# 재현: 다른 PC에서도 이 스크립트만 실행하면 동일 데이터가 data/GSE209878/ 에 받아진다.
#   bash pipeline/hspc-velocity-benchmark/scripts/download_data.sh
#
# 받는 것 (~1.9 GB): 두 sample = 두 timepoint (GSM title 확정): MV-1 = day0, MV-2 = day7.
#   - matrix.mtx.gz  : CellRanger ARC 통합 feature matrix (**Gene Expression + ATAC Peaks 둘 다 포함**)
#   - features.tsv.gz / barcodes.tsv.gz : feature·cell 식별자
#   - gex.loom.gz    : velocyto spliced/unspliced (RNA velocity 입력)
#   - peak_annotation.tsv.gz : peak→gene 매핑
#   - feature_linkage.bedpe.gz : peak-gene linkage
#
# 일부러 받지 않는 것:
#   - GSE209878_RAW.tar (9.8 GB 전체 묶음) — 위 파일들로 충분.
#   - *_atac_fragments.tsv.gz (4.3+5.1=9.4 GB) — peak 재호출용. matrix.mtx에 이미 peak count가
#     들어있어 *불필요*. (peak set을 직접 다시 부르고 싶을 때만 받는다 — 맨 아래 OPTIONAL 참고.)
#
# 출처: GEO GSE209878 (PMID 36229609), MultiVelo 원논문 데이터. 라이선스: GEO public.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
OUT="$ROOT/pipeline/hspc-velocity-benchmark/data/GSE209878"
GSE="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE209nnn/GSE209878/suppl"
GSM_MV1_GEX="https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM6403nnn/GSM6403408/suppl"   # 3423-MV-1 GEX loom
GSM_MV1_ATAC="https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM6403nnn/GSM6403409/suppl"  # 3423-MV-1 ATAC
GSM_MV2_GEX="https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM6403nnn/GSM6403410/suppl"   # 3423-MV-2 GEX loom
GSM_MV2_ATAC="https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM6403nnn/GSM6403411/suppl"  # 3423-MV-2 ATAC

# get <url> <dest> : skip if already complete (size match), else resume/download.
# (완료 파일을 -C - 로 resume하면 서버가 416을 반환하므로 크기 비교로 먼저 거른다.)
fsize() { stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null || echo 0; }
get() {
  local url="$1" dest="$2" remote
  mkdir -p "$(dirname "$dest")"
  remote=$(curl -sIL "$url" | awk 'tolower($1)=="content-length:"{l=$2} END{gsub(/\r/,"",l); print l}')
  if [ -f "$dest" ] && [ -n "$remote" ] && [ "$(fsize "$dest")" = "$remote" ]; then
    echo "  = $(basename "$dest") (이미 완료, skip)"; return 0
  fi
  echo "  ↓ $(basename "$dest")  (${remote:-?} bytes)"
  curl -fL --retry 5 --retry-delay 3 -C - -o "$dest" "$url"
}

echo "GSE209878 → $OUT"
# --- MV-1 (3423-MV-1) ---
get "$GSE/GSE209878_3423-MV-1_barcodes.tsv.gz"          "$OUT/MV-1/barcodes.tsv.gz"
get "$GSE/GSE209878_3423-MV-1_features.tsv.gz"          "$OUT/MV-1/features.tsv.gz"
get "$GSE/GSE209878_3423-MV-1_matrix.mtx.gz"            "$OUT/MV-1/matrix.mtx.gz"           # ~582 MB
get "$GSE/GSE209878_3423-MV-1_feature_linkage.bedpe.gz" "$OUT/MV-1/feature_linkage.bedpe.gz"
get "$GSM_MV1_ATAC/GSM6403409_3423-MV-1_atac_peak_annotation.tsv.gz" "$OUT/MV-1/peak_annotation.tsv.gz"
get "$GSM_MV1_GEX/GSM6403408_3423-MV-1_gex_possorted_bam_0E7KE.loom.gz" "$OUT/MV-1/gex.loom.gz"  # ~164 MB
# --- MV-2 (3423-MV-2) ---
get "$GSE/GSE209878_3423-MV-2_barcodes.tsv.gz"          "$OUT/MV-2/barcodes.tsv.gz"
get "$GSE/GSE209878_3423-MV-2_features.tsv.gz"          "$OUT/MV-2/features.tsv.gz"
get "$GSE/GSE209878_3423-MV-2_matrix.mtx.gz"            "$OUT/MV-2/matrix.mtx.gz"           # ~816 MB
get "$GSE/GSE209878_3423-MV-2_feature_linkage.bedpe.gz" "$OUT/MV-2/feature_linkage.bedpe.gz"
get "$GSM_MV2_ATAC/GSM6403411_3423-MV-2_atac_peak_annotation.tsv.gz" "$OUT/MV-2/peak_annotation.tsv.gz"
get "$GSM_MV2_GEX/GSM6403410_3423-MV-2_gex_possorted_bam_ICXFB.loom.gz" "$OUT/MV-2/gex.loom.gz"  # ~274 MB

echo "✓ done. 용량:"; du -sh "$OUT"/MV-1 "$OUT"/MV-2 2>/dev/null || true
echo "다음: python3 pipeline/hspc-velocity-benchmark/scripts/check_data.py <전처리 후 .h5ad/.h5mu>"

# ── OPTIONAL: peak를 직접 다시 부르고 싶을 때만 (9.4 GB, 보통 불필요) ───────────
#   ATAC fragments:
#   get "$GSM_MV1_ATAC/GSM6403409_3423-MV-1_atac_fragments.tsv.gz" "$OUT/MV-1/atac_fragments.tsv.gz"  # 4.3 GB
#   get "$GSM_MV2_ATAC/GSM6403411_3423-MV-2_atac_fragments.tsv.gz" "$OUT/MV-2/atac_fragments.tsv.gz"  # 5.1 GB
