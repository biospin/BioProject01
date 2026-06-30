#!/usr/bin/env bash
# cross-dataset replication 원커맨드 실행기
# 사용법: ./run_all.sh <dataset_name> [--gpu]
# 예시:   ./run_all.sh skin
#          ./run_all.sh mouse_brain --gpu
#
# 전제: data/<dataset_name>/ 아래에 CellRanger ARC 결과 OR
#       cross_dataset/<dataset_name>/rna_spliced_unspliced.h5ad 이미 있음

set -euo pipefail
DATASET="${1:-}"
GPU_FLAG=""
[[ "${2:-}" == "--gpu" ]] && GPU_FLAG="--gpu"

if [[ -z "$DATASET" ]]; then
  echo "사용법: $0 <dataset_name> [--gpu]"
  echo "예시:   $0 skin"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")/../scripts" && pwd)"
LOG_DIR="/tmp"
export HDF5_USE_FILE_LOCKING=FALSE

echo "[$(date '+%H:%M:%S')] === Cross-dataset replication: $DATASET ==="

# P1 (raw 데이터 있을 때만 — h5ad 이미 있으면 스킵)
PROC_DIR="$(cd "$(dirname "$0")/.." && pwd)/data/processed_${DATASET}"
if [[ ! -f "${PROC_DIR}/rna_spliced_unspliced.h5ad" ]]; then
  echo "[$(date '+%H:%M:%S')] P1 전처리 시작..."
  conda run --no-capture-output -n scv-preprocess \
    python -u "${SCRIPT_DIR}/p1_build.py" --dataset "$DATASET" \
    > "${LOG_DIR}/p1_${DATASET}.log" 2>&1
  echo "[$(date '+%H:%M:%S')] ✓ P1 완료"
else
  echo "[$(date '+%H:%M:%S')] ✓ P1 산출물 존재 → 스킵"
fi

# P2 MultiVelo (CPU, ~2h)
echo "[$(date '+%H:%M:%S')] P2 MultiVelo 시작..."
OMP_NUM_THREADS=1 conda run --no-capture-output -n mv \
  python -u "${SCRIPT_DIR}/p2_multivelo.py" --dataset "$DATASET" \
  > "${LOG_DIR}/p2_mv_${DATASET}.log" 2>&1
echo "[$(date '+%H:%M:%S')] ✓ P2 MultiVelo 완료"

# P2 RNA-only floor
echo "[$(date '+%H:%M:%S')] P2 RNA-only 시작..."
conda run --no-capture-output -n mv \
  python -u "${SCRIPT_DIR}/p2_rna_only.py" --dataset "$DATASET" \
  > "${LOG_DIR}/p2_rna_${DATASET}.log" 2>&1
echo "[$(date '+%H:%M:%S')] ✓ P2 RNA-only 완료"

# P2 DL arm (torch env, GPU 있으면 훨씬 빠름)
if conda env list | grep -q "^torch"; then
  echo "[$(date '+%H:%M:%S')] P2 MultiVeloVAE 시작 (${GPU_FLAG:-cpu})..."
  conda run --no-capture-output -n torch \
    python -u "${SCRIPT_DIR}/p2_multivelovae.py" --dataset "$DATASET" $GPU_FLAG \
    > "${LOG_DIR}/p2_vae_${DATASET}.log" 2>&1
  echo "[$(date '+%H:%M:%S')] ✓ P2 MultiVeloVAE 완료"

  echo "[$(date '+%H:%M:%S')] P2 MoFlow 시작..."
  PYTHONPATH="$(cd "$(dirname "$0")/../ext/MoFlow/src" && pwd)" \
  conda run --no-capture-output -n torch \
    python -u "${SCRIPT_DIR}/p2_moflow.py" --dataset "$DATASET" $GPU_FLAG \
    > "${LOG_DIR}/p2_moflow_${DATASET}.log" 2>&1
  echo "[$(date '+%H:%M:%S')] ✓ P2 MoFlow 완료"
else
  echo "[$(date '+%H:%M:%S')] ⚠ torch env 없음 → DL arm 스킵 (MultiVelo+RNA-only만)"
fi

# P3 concordance (HSPC 결과와 비교)
echo "[$(date '+%H:%M:%S')] P3 concordance (vs HSPC)..."
conda run --no-capture-output -n mv \
  python -u "${SCRIPT_DIR}/p3_concordance.py" --dataset "$DATASET" --compare-to hspc \
  > "${LOG_DIR}/p3_${DATASET}.log" 2>&1
echo "[$(date '+%H:%M:%S')] ✓ P3 완료"

echo ""
echo "=== 완료: $DATASET ==="
RESULTS="$(cd "$(dirname "$0")/../results" && pwd)"
echo "결과: ${RESULTS}/concordance_${DATASET}.md"
echo "로그: ${LOG_DIR}/p1_${DATASET}.log ... p3_${DATASET}.log"
