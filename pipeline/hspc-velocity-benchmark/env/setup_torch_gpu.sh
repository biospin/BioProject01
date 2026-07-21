#!/usr/bin/env bash
# DL arm(MultiVeloVAE/MoFlow) 원샷 셋업 — GPU 머신에서 그대로 실행.
# 2026-06-15 이 Mac(CPU)에서 검증한 env 보정 6건 + MoFlow 패치 2건을 자동 적용.
# GPU torch는 §GPU 주석 참고(드라이버에 맞춰 1줄만 바꿈).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"          # .../env
ROOT="$(dirname "$HERE")"                       # .../hspc-velocity-benchmark
VENDOR="$ROOT/vendor"
# 주의: upstream 커밋 핀 (2026-07-15 HEAD 기준). GPU 머신 vendor/에서 실제 검증 커밋으로 교체 확인 권장.
MOFLOW_COMMIT="2197359756d7fdd13ccdb5c2e3e62087807b0787"
MVVAE_COMMIT="0557b5d3030c0282fe929f8e97baf737562bb568"

echo "[1/5] torch env 생성 (miniforge mamba)"
mamba env create -f "$HERE/velo-torch.yml" || echo "  (이미 있으면 무시)"
PY="$(conda info --base)/envs/velo-torch/bin/python"
[ -x "$PY" ] || PY="$HOME/miniforge3/envs/velo-torch/bin/python"

echo "[2/5] env 보정: setuptools<80(pkg_resources) + fastdtw"
"$PY" -m pip install -q 'setuptools<80' fastdtw

echo "[3/5] MultiVeloVAE 설치 (welch-lab, BSD-3)"
"$PY" -m pip install -q "git+https://github.com/welch-lab/MultiVeloVAE.git@${MVVAE_COMMIT}"

echo "[4/5] MoFlow clone + 패치 2건"
if [ ! -d "$VENDOR/MoFlow" ]; then
  git clone https://github.com/AriHong/MoFlow.git "$VENDOR/MoFlow"
  git -C "$VENDOR/MoFlow" checkout "$MOFLOW_COMMIT"
fi
ED="$VENDOR/MoFlow/src/MoFlow/eval_dtw.py"
INIT="$VENDOR/MoFlow/src/MoFlow/__init__.py"
# 패치①: plot_dtw 시그니처 뒤 잉여 '):' 줄 제거. (검증은 최종 [5/5] import가 수행 — 미적용 시 set -e로 중단)
"$PY" - "$ED" <<'PYEOF'
import sys
p=sys.argv[1]; s=open(p).read()
open(p,'w').write(s.replace("         figsave=None):\n    ):\n","         figsave=None):\n"))
print("  eval_dtw.py 패치 적용")
PYEOF
# 패치②: 없는 simulation import 주석 처리
sed -i.bak 's|^from \.simulation import simulate|# from .simulation import simulate  # repo 누락(patch)|' "$INIT" && rm -f "$INIT.bak"
# 패치③: velocity()의 adata_result 오타(미정의 NameError) → adata
grep -q "adata_result\.layers" "$VENDOR/MoFlow/src/MoFlow/moflow.py" || echo "  경고: 패치③ 대상 없음 — 핀 커밋 확인(이미 수정됐거나 drift)"
sed -i.bak 's|adata_result\.layers|adata.layers|g' "$VENDOR/MoFlow/src/MoFlow/moflow.py" && rm -f "$VENDOR/MoFlow/src/MoFlow/moflow.py.bak"

echo "[5/5] 검증 (import + GPU 가용)"
PYTHONPATH="$VENDOR/MoFlow/src" "$PY" - <<'PYEOF'
import torch, multivelovae
from MoFlow.moflow import MOFlow
print(f"  torch {torch.__version__} | cuda={torch.cuda.is_available()} | multivelovae OK | MoFlow OK")
PYEOF

cat <<'EOF'

✅ 셋업 완료. 다음:
  - GPU torch: 위 torch가 cuda=False면 →
      $PY -m pip install --force-reinstall torch --index-url https://download.pytorch.org/whl/cu121
    (드라이버 CUDA 버전에 맞춰 cu121/cu118 등)
  - substrate 복사: data/processed/{rna_spliced_unspliced,atac_peaks}.h5ad
  - 실행: p2_multivelovae.py / p2_moflow.py (runner) — MoFlow는 MOFlow(...).velocity(adata, n_jobs=N)
  - 런타임은 이 머신에서 소형 smoke로 먼저 측정 후 full.
EOF
