# =============================================================================
# BioProject01 — single-cell multi-omics RNA velocity 통합 이미지
# 모델: scVelo, MultiVelo, MultiVeloVAE, MoFlow, cellDancer, DeepVelo
#       (+ scanpy/anndata, 선택적 GPU 전처리 rapids-singlecell)
#
# 전략: 단일 env(velo)에 최대한 몰고, DGL 의존으로 충돌나는 DeepVelo만 별도 env 격리.
#       연속성(후속 버전 추적) 불필요 → 1차 빌드 성공 후 버전 LOCK 해서 박제.
#
# 빌드:  docker build -t autobiox-bio01:frozen .
# 실행:  docker run --gpus all -it -v /path/data:/data -v $PWD:/work autobiox-bio01:frozen
#   env 전환 실행:
#     micromamba run -n velo     python run_scvelo_multivelo.py
#     micromamba run -n deepvelo python run_deepvelo.py
#   주피터:
#     docker run --gpus all -p 8888:8888 -v $PWD:/work autobiox-bio01:frozen \
#       micromamba run -n velo jupyter lab --ip 0.0.0.0 --allow-root --no-browser
# =============================================================================

# CUDA 12.1 베이스 (Ampere=A16/A6000 sm_86 호환). 호스트 드라이버가 지원하는 CUDA로 맞출 것.
FROM mambaorg/micromamba:1.5.8-cuda12.1.1-ubuntu22.04

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
        git build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# ─────────────────────────────────────────────────────────────────────────────
# env 1: velo  (메인 — scvelo 계열 + pytorch 기반 모델 대부분)
#   scvelo/MultiVelo는 numpy<2 + numba 조합이 필요해 여기서 핀.
# ─────────────────────────────────────────────────────────────────────────────
RUN micromamba create -y -n velo -c pytorch -c nvidia -c conda-forge -c bioconda \
        python=3.10 \
        "numpy<2" "numba>=0.57,<0.60" pandas scipy \
        scanpy anndata scvelo \
        leidenalg python-igraph louvain \
        jupyterlab ipykernel \
        pytorch torchvision pytorch-cuda=12.1 && \
    micromamba clean -a -y

# pip 설치 (conda에 없는 velocity 패키지). 1차 빌드 후 == 핀으로 고정 권장.
RUN micromamba run -n velo pip install --no-cache-dir \
        multivelo \
        celldancer \
        git+https://github.com/welch-lab/MultiVeloVAE.git

# MoFlow (multi-omic relay velocity, Nature Comms 2025): 논문 Code availability의 repo로 교체.
#   https://www.nature.com/articles/s41467-025-67259-6  → 하단 Code availability 확인 후:
# RUN micromamba run -n velo pip install --no-cache-dir git+https://github.com/<owner>/<MoFlow-repo>.git
RUN echo "TODO: MoFlow repo 확정 후 위 줄 활성화"

# (선택) GPU 가속 전처리 — scanpy 10~20x. 충돌 시 별도 env로 빼기.
# RUN micromamba run -n velo pip install --no-cache-dir rapids-singlecell

# ─────────────────────────────────────────────────────────────────────────────
# env 2: deepvelo  (DGL 의존 → 충돌 격리)
# ─────────────────────────────────────────────────────────────────────────────
RUN micromamba create -y -n deepvelo -c pytorch -c nvidia -c conda-forge \
        python=3.10 "numpy<2" pandas scipy scanpy anndata scvelo \
        ipykernel \
        pytorch pytorch-cuda=12.1 && \
    micromamba clean -a -y

# DGL CUDA 12.1 휠 + DeepVelo (conda가 깐 torch 버전에 맞춰 인덱스 조정 필요할 수 있음)
RUN micromamba run -n deepvelo pip install --no-cache-dir \
        dgl -f https://data.dgl.ai/wheels/torch-2.3/cu121/repo.html && \
    micromamba run -n deepvelo pip install --no-cache-dir deepvelo

WORKDIR /work
CMD ["bash"]

# =============================================================================
# 빌드 성공 후 LOCK(박제) 절차 — 이 프로젝트 동안 버전 고정:
#   docker run --rm autobiox-bio01:frozen micromamba run -n velo     pip freeze > velo.lock
#   docker run --rm autobiox-bio01:frozen micromamba run -n deepvelo pip freeze > deepvelo.lock
#   → 위 pip install 줄을  pip install -r velo.lock  형태로 바꿔 재빌드하면 완전 재현.
# =============================================================================
