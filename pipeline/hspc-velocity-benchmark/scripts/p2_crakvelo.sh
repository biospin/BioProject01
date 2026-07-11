#!/bin/bash
# p2_crakvelo.sh — CRAK-Velo (TF/UniTVelo 확장) fit 실행.
#
# 선행: scripts/p2_crakvelo_prep.py (substrate) + scripts/p2_crakvelo_cistopic.py (obsm['cisTopic']).
# 입력: crakvelo_rna_prepro.h5ad + crakvelo_atac_postpro.h5ad  (config의 절대경로)
# 산출: data/velocity/crakvelo_fit/{adata_rna_fit.h5ad, adata_atac_fit.h5ad, B.txt}
#
# env: tf (TF 2.15.1 GPU, unitvelo 0.2.5, pybedtools). GPU: cuda:1 (CUDA_VISIBLE_DEVICES=1 → gpu_id=0).
# main.py 는 sibling 패키지(velocity/model/utils)를 top-level import → cwd=crak-velo/ 필수.
set -euo pipefail
ROOT=/home/kkkim/project/BioProject01/pipeline/hspc-velocity-benchmark
CFG=$ROOT/scripts/p2_crakvelo_config.json
WIN=100000

mkdir -p "$ROOT/data/velocity/crakvelo_fit"
source ~/miniconda3/etc/profile.d/conda.sh
export CUDA_VISIBLE_DEVICES=1
export PYTHONUNBUFFERED=1

cd "$ROOT/vendor/CRAK-Velo/crak-velo"
exec conda run --no-capture-output -n velo-tf python -u main.py --config "$CFG" --w "$WIN"
