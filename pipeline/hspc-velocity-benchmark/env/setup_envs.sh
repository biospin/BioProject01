#!/usr/bin/env bash
#
# setup_envs.sh — 4개 격리 conda env 생성 (프레임워크 충돌 회피).
#   bash pipeline/hspc-velocity-benchmark/env/setup_envs.sh [env이름...]
#   인자 없으면 4개 모두. 예: setup_envs.sh velo-mv   (velo-mv만)
#
# 권장: conda 대신 mamba(빠름). CONDA=mamba bash setup_envs.sh
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CONDA="${CONDA:-conda}"
if [ $# -eq 0 ]; then ENVS=(scv-preprocess velo-mv velo-torch velo-tf); else ENVS=("$@"); fi

command -v "$CONDA" >/dev/null || { echo "✗ $CONDA 없음. miniconda/mambaforge 설치 필요."; exit 1; }

for e in "${ENVS[@]}"; do
  yml="$HERE/$e.yml"
  [ -f "$yml" ] || { echo "✗ $yml 없음, skip"; continue; }
  echo "── $CONDA env create: $e ──"
  "$CONDA" env create -f "$yml" || echo "  ⚠ $e 생성 실패 — README의 known gotchas 참고 후 수동 조정"
done

echo ""
echo "다음:"
echo "  1) 각 env에서 import 확인:  conda run -n velo-mv python -c 'import multivelo, scvelo; print(\"mv ok\")'"
echo "  2) 성공한 env는 lock:        conda env export -n <env> > $HERE/<env>.lock.yml"
echo "  3) MultiVelo 1-fit 시간/메모리 측정 → P0_provenance §3 갱신"
