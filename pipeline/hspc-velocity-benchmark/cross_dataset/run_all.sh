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

# ── ⛑️ 안전장치 (2026-07-01) ────────────────────────────────────────
# p1/p2/p3 스크립트는 아직 --dataset/--config 배선이 없어 이 스크립트를 그대로
# 돌리면 HSPC 데이터로 돌면서 results/multivelo_genes.csv(HSPC 결과)를 덮어쓴다.
# RUNBOOK.md '데이터 도착 시 체크리스트' ①~③(config 파라미터화 + dataset별
# marker/QC 재정의 + 산출물 suffix) 완료 후, CROSS_DATASET_READY=1 로 해제한다.
CONFIG_FILE="$(cd "$(dirname "$0")" && pwd)/config_${DATASET}.py"
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "❌ config_${DATASET}.py 없음 → config_template.py 복사·편집 후 재실행."
  echo "   (RUNBOOK.md §2 참조. marker/QC는 조직별 재정의 필수 — §'⚠️ 현재 준비 상태')"
  exit 2
fi
if [[ "${CROSS_DATASET_READY:-0}" != "1" ]]; then
  echo "❌ 파이프라인이 아직 cross-dataset 배선 미완 (RUNBOOK '데이터 도착 시 체크리스트' ①~③)."
  echo "   지금 실행하면 HSPC 산출물을 덮어쓸 수 있어 거부한다."
  echo "   ①config 파라미터화 ②dataset별 marker/QC 재정의 ③산출물 dataset-suffix 완료 후:"
  echo "      CROSS_DATASET_READY=1 $0 $DATASET ${2:-}"
  exit 3
fi
# ────────────────────────────────────────────────────────────────────

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
OMP_NUM_THREADS=1 conda run --no-capture-output -n velo-mv \
  python -u "${SCRIPT_DIR}/p2_multivelo.py" --dataset "$DATASET" \
  > "${LOG_DIR}/p2_mv_${DATASET}.log" 2>&1
echo "[$(date '+%H:%M:%S')] ✓ P2 MultiVelo 완료"

# P2 RNA-only floor
echo "[$(date '+%H:%M:%S')] P2 RNA-only 시작..."
conda run --no-capture-output -n velo-mv \
  python -u "${SCRIPT_DIR}/p2_rna_only.py" --dataset "$DATASET" \
  > "${LOG_DIR}/p2_rna_${DATASET}.log" 2>&1
echo "[$(date '+%H:%M:%S')] ✓ P2 RNA-only 완료"

# P2 DL arm (torch env, GPU 있으면 훨씬 빠름)
if conda env list | grep -q "^torch"; then
  echo "[$(date '+%H:%M:%S')] P2 MultiVeloVAE 시작 (${GPU_FLAG:-cpu})..."
  conda run --no-capture-output -n velo-torch \
    python -u "${SCRIPT_DIR}/p2_multivelovae.py" --dataset "$DATASET" $GPU_FLAG \
    > "${LOG_DIR}/p2_vae_${DATASET}.log" 2>&1
  echo "[$(date '+%H:%M:%S')] ✓ P2 MultiVeloVAE 완료"

  echo "[$(date '+%H:%M:%S')] P2 MoFlow 시작..."
  PYTHONPATH="$(cd "$(dirname "$0")/../ext/MoFlow/src" && pwd)" \
  conda run --no-capture-output -n velo-torch \
    python -u "${SCRIPT_DIR}/p2_moflow.py" --dataset "$DATASET" $GPU_FLAG \
    > "${LOG_DIR}/p2_moflow_${DATASET}.log" 2>&1
  echo "[$(date '+%H:%M:%S')] ✓ P2 MoFlow 완료"
else
  echo "[$(date '+%H:%M:%S')] ⚠ torch env 없음 → DL arm 스킵 (MultiVelo+RNA-only만)"
fi

# P3 concordance (HSPC 결과와 비교)
echo "[$(date '+%H:%M:%S')] P3 concordance (vs HSPC)..."
conda run --no-capture-output -n velo-mv \
  python -u "${SCRIPT_DIR}/p3_concordance.py" --dataset "$DATASET" --compare-to hspc \
  > "${LOG_DIR}/p3_${DATASET}.log" 2>&1
echo "[$(date '+%H:%M:%S')] ✓ P3 완료"

echo ""
echo "=== 완료: $DATASET ==="
RESULTS="$(cd "$(dirname "$0")/../results" && pwd)"
echo "결과: ${RESULTS}/concordance_${DATASET}.md"
echo "로그: ${LOG_DIR}/p1_${DATASET}.log ... p3_${DATASET}.log"
