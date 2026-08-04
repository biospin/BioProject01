# velo-tf GPU 활성화 fix (BIOP01-22)

> 적용·검증 지용기, 2026-07-27, 공유 GPU 서버(`/opt/envs/velo-tf`). env는 git 미추적이라 이 문서가
> 재현·검토·롤백의 정본이다. **env 소유는 류재면/kkkim** — 검토 후 정본 편입 판단 바람.

## 증상

`velo-tf`(CRAK-Velo / cellDancer arm)의 TensorFlow가 GPU를 못 봤다: `tf.config.list_physical_devices("GPU")` → **0개**.
(같은 서버에서 velo-torch PyTorch는 cuda=True·3 GPU 정상.)

## 원인 (읽기 전용 진단으로 확정)

- TF 2.13.1은 **CPU 빌드가 아니라 CUDA 빌드**다: `is_cuda_build=True`, `cuda_version=11.8`, `cudnn_version=8`.
- 그런데 로그가 `Could not find cuda drivers` → **CUDA 11.8 런타임을 못 찾음**.
- 시스템에는 **CUDA 12.4만** 설치돼 있고(`/usr/local/cuda-12.4`), 11.8이 없다. driver 535.309.01.
- env 안에 nvidia-cu11 pip 라이브러리도 **없었다**(`site-packages/nvidia/` 부재).
- 즉 TF 2.13이 요구하는 cu11 런타임(libcudart.so.11.0, libcudnn.so.8 등)이 어디에도 없어 GPU 초기화 실패.
  (velo-torch는 torch 자체가 cu121 라이브러리를 번들해서 무관하게 동작.)

## fix (additive · 되돌림 가능)

### 1) cu11 런타임 라이브러리 설치 (`--no-deps` — 기존 패키지 무변경)

```bash
/opt/envs/velo-tf/bin/pip install --no-deps \
  nvidia-cudnn-cu11==8.6.0.163 nvidia-cuda-runtime-cu11==11.8.89 \
  nvidia-cublas-cu11 nvidia-cufft-cu11 nvidia-curand-cu11 \
  nvidia-cusolver-cu11 nvidia-cusparse-cu11 nvidia-cuda-cupti-cu11 nvidia-nccl-cu11 \
  nvidia-cuda-nvcc-cu11 nvidia-cuda-nvrtc-cu11
```

`--no-deps`라 tensorflow/keras/unitvelo/scvelo/scanpy/anndata는 **버전 그대로**(설치 후 실측 확인). 11개 nvidia-cu11 패키지만 새로 들어간다.

### 2) activation 훅 — `conda run -n velo-tf`가 자동으로 CUDA 경로를 잡게

`/opt/envs/velo-tf/etc/conda/activate.d/zz_cuda_ld.sh`:

```bash
# velo-tf GPU 활성화 (BIOP01-22). 되돌리려면 이 파일 삭제.
NVDIR=/opt/envs/velo-tf/lib/python3.9/site-packages/nvidia
export LD_LIBRARY_PATH="$(ls -d $NVDIR/*/lib 2>/dev/null | paste -sd:):$LD_LIBRARY_PATH"
export PATH="$NVDIR/cuda_nvcc/bin:$PATH"   # ptxas (XLA)
```

파이프라인은 `scripts/p2_crakvelo.sh`에서 `conda run --no-capture-output -n velo-tf python …`로 호출하고,
`conda run`은 `activate.d`를 소싱하므로 이 훅이 자동 발동한다.

## 검증 (실측)

| 항목 | 결과 |
|---|---|
| 핵심 .so 존재 | libcudart.so.11.0 · libcudnn.so.8 · libcublas.so.11 · libcufft.so.10 ✅ |
| 훅 소스 후 GPU 인식 | **n_gpu: 3** (RTX A6000) ✅ |
| 실제 GPU 연산 | matmul ✅ · conv2d(cudnn 경로) ✅ |
| ptxas 경고 | nvcc 설치 후 **해소** ✅ |
| 기존 패키지 | tensorflow 2.13.1 · keras 2.13.1 · unitvelo 0.2.5.2 · scvelo 0.3.4 무변경 ✅ |

## 주의 / 남은 것

- 이 fix는 **`conda run`(또는 `conda activate`) 경로에서만** 발동한다. 스크립트가 `/opt/envs/velo-tf/bin/python`을
  **직접** 부르면 훅이 안 걸려 GPU를 못 본다(직접 호출 실측 n_gpu=0). 파이프라인은 `conda run`을 쓰므로 문제없으나,
  직접 호출 경로를 쓸 계획이면 그 스크립트에 위 `LD_LIBRARY_PATH` export를 명시하거나 `conda run`으로 통일할 것.
- **GPU 가시성**을 복구했을 뿐, CRAK-Velo/cellDancer 파이프라인 자체의 GPU 동작·수치는 env 소유자(류재면/kkkim)가
  별도 검증해야 한다(이 arm은 원래 "가장 취약·미검증"으로 표기됨).
- 롤백: `activate.d/zz_cuda_ld.sh` 삭제 + (원하면) 위 11개 nvidia-cu11 패키지 제거 → 원상.
- env가 재생성되면 이 fix도 사라진다. **재현성 정본이 되려면** 위 두 단계를 `setup_envs.sh` 또는
  `velo-tf.lock.yml` 갱신에 편입해야 한다(소유자 판단).
