# =============================================================================
# BioProject01 / HSPC velocity benchmark — 4-env 통합 이미지 (BIOP01-22)
# 위치: pipeline/hspc-velocity-benchmark/Dockerfile
# 빌드 컨텍스트 = 이 디렉토리(env/*.yml 을 COPY).
#
# env 설계 (프레임워크 충돌로 격리 — env/README.md 근거):
#   scv-preprocess (py3.11)  공통 전처리 P1            GPU 불요
#   mv             (py3.10)  MultiVelo + scVelo        GPU 불요(CPU 7.4h)
#   torch          (py3.10)  MultiVeloVAE + MoFlow     GPU 선택 (PyTorch)
#   tf             (py3.9)   CRAK-Velo + cellDancer    GPU 선택 (TensorFlow, 가장 취약)
#
# 빌드/실행:
#   cd pipeline/hspc-velocity-benchmark
#   docker build -t autobiox-bio01:cpu  .                      # CPU(기본)
#   docker build -t autobiox-bio01:gpu  --build-arg GPU=1 .    # GPU(cu121/tf-cuda)
#   docker run --gpus all -it -v /data:/data -v $PWD:/work autobiox-bio01:gpu
#     conda run -n mv     python -c "import multivelo, scvelo; print('mv ok')"
#     conda run -n torch  python -c "import torch, multivelovae; from MoFlow.moflow import MOFlow; print(torch.cuda.is_available())"
#     conda run -n tf     python -c "import tensorflow as tf; print(tf.__version__)"
# =============================================================================

FROM condaforge/miniforge3:24.9.2-0          # mamba 내장. conda base = /opt/conda

SHELL ["/bin/bash", "-lc"]
WORKDIR /opt/bench

USER root
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# ── env spec 복사 (이 디렉토리의 env/ 그대로) ──
COPY env/scv-preprocess.yml env/mv.yml env/torch.yml env/tf.yml ./env/

# ── 1) scv-preprocess (공통 전처리) ──
RUN mamba env create -f env/scv-preprocess.yml && mamba clean -a -y

# ── 2) mv (MultiVelo + scVelo, baseline) ──
RUN mamba env create -f env/mv.yml && mamba clean -a -y

# ── 3) torch (MultiVeloVAE + MoFlow) + setup_torch_gpu.sh 보정/패치 반영 ──
RUN mamba env create -f env/torch.yml && mamba clean -a -y
RUN set -eux; PY=/opt/conda/envs/torch/bin/python; \
    "$PY" -m pip install --no-cache-dir 'setuptools<80' fastdtw; \
    # MultiVeloVAE pyproject.toml license 포맷 패치 (setuptools>=61 strict validation 우회)
    git clone --depth 1 https://github.com/welch-lab/MultiVeloVAE.git /tmp/MultiVeloVAE; \
    sed -i 's/^license = "BSD-3-Clause"/license = {text = "BSD-3-Clause"}/' /tmp/MultiVeloVAE/pyproject.toml; \
    "$PY" -m pip install --no-cache-dir /tmp/MultiVeloVAE --no-build-isolation; \
    rm -rf /tmp/MultiVeloVAE; \
    git clone --depth 1 https://github.com/AriHong/MoFlow.git /opt/bench/vendor/MoFlow; \
    sed -i 's|^from \.simulation import simulate|# from .simulation import simulate  # repo 누락(patch)|' \
        /opt/bench/vendor/MoFlow/src/MoFlow/__init__.py; \
    sed -i 's|adata_result\.layers|adata.layers|g' /opt/bench/vendor/MoFlow/src/MoFlow/moflow.py
RUN /opt/conda/envs/torch/bin/python - <<'PYEOF'
p="/opt/bench/vendor/MoFlow/src/MoFlow/eval_dtw.py"
s=open(p).read()
open(p,"w").write(s.replace("         figsave=None):\n    ):\n","         figsave=None):\n"))
print("eval_dtw.py 패치 적용")
PYEOF

# ── 4) tf (CRAK-Velo + cellDancer) — 가장 취약(미검증). 실패해도 빌드 계속 ──
RUN mamba env create -f env/tf.yml && mamba clean -a -y || \
    echo "WARN: tf env 생성 실패 — README known gotchas(UniTVelo/TF 버전, cisTopic) 참고해 수동 조정 필요"

# ── GPU wheel (옵션): yml은 CPU 기본 → GPU 빌드 시에만 덮어쓰기 ──
ARG GPU=0
RUN if [ "$GPU" = "1" ]; then set -eux; \
      /opt/conda/envs/torch/bin/pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu121; \
      ( /opt/conda/envs/tf/bin/pip install --no-cache-dir "tensorflow[and-cuda]" || echo "WARN: tf GPU wheel 실패(별도 검증)" ); \
    fi

ENV PYTHONPATH=/opt/bench/vendor/MoFlow/src
WORKDIR /work
CMD ["bash"]

# =============================================================================
# 빌드 성공 후 LOCK(박제) — BIOP01-22 재현성(현재 .lock.yml 미커밋):
#   for e in scv-preprocess mv torch tf; do
#     docker run --rm autobiox-bio01:gpu conda env export -n $e > env/$e.lock.yml
#   done
#   → 4개 env/*.lock.yml 을 이 브랜치(kkkim-pipeline)에 커밋.
#   (GPU에서 cuda=True 검증 후 lock 떠야 GPU wheel 핀까지 고정)
# =============================================================================
