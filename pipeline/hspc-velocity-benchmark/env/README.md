# Env 구축 — HSPC velocity benchmark

> 4개 env로 분리한다. **이유(P0 핵심 발견)**: PyTorch(MultiVeloVAE/MoFlow) ↔ TensorFlow
> (CRAK-Velo/cellDancer)가 한 env에서 CUDA/버전 충돌. 격리가 유일하게 안정적.

## env 4종

| env | method | 프레임워크 | GPU |
|---|---|---|---|
| `scv-preprocess` | 공통 전처리(P1) | — | 불요 |
| `mv` | MultiVelo, scVelo | numba | 불요 |
| `torch` | MultiVeloVAE, MoFlow | PyTorch | 선택 |
| `tf` | CRAK-Velo, cellDancer | TensorFlow | 선택 |

## 사전 준비
- miniconda 또는 mambaforge. **mamba 권장**(conda solve가 느림): `CONDA=mamba`.

## 생성
```bash
bash pipeline/hspc-velocity-benchmark/env/setup_envs.sh          # 4개 모두
CONDA=mamba bash .../env/setup_envs.sh mv                        # 하나만, mamba로
```

## 설치 순서(권장)
1. `mv` — 가장 가볍고 baseline. 먼저 성공시켜 MultiVelo 1-fit으로 데이터 파이프 검증.
2. `scv-preprocess` — P1 전처리.
3. `torch` — MultiVeloVAE/MoFlow (H1 핵심 쌍).
4. `tf` — CRAK-Velo/cellDancer (가장 까다로움, 마지막).

## GPU (1대 가용 — §7b)
- 기본 yml은 **CPU wheel**. 11k cells는 CPU로 충분(MultiVelo는 GPU 미지원).
- GPU 쓸 때만:
  - torch: `pip install torch --index-url https://download.pytorch.org/whl/cu121` (CUDA 버전 맞게)
  - tf: `pip install "tensorflow[and-cuda]"`
- 1 GPU를 `torch`·`tf` env가 순차 점유. bootstrap 반복이 CPU로 비현실적일 때만 GPU.

## 검증 + lock (재현성)
```bash
conda run -n mv     python -c "import multivelo, scvelo; print('mv ok')"
conda run -n torch  python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
conda run -n tf     python -c "import tensorflow as tf; print('tf', tf.__version__)"
# 성공한 env는 정확 버전 동결:
conda env export -n <env> > pipeline/hspc-velocity-benchmark/env/<env>.lock.yml
```
→ `.lock.yml`은 *commit* (재현용). 원본 `<env>.yml`은 느슨한 spec, lock은 정확 핀.

## Known gotchas (`검토필요:` — 머신에서 iteration 필요)
- **numpy<2 고정**: scvelo/scanpy 일부가 numpy 2.x 미대응. 충돌 시 numpy 1.26으로.
- **github 패키지 import 이름**: MultiVeloVAE/MoFlow/CRAK-Velo의 실제 import 이름은 repo 확인 후 검증 명령 수정. 설치 실패 시 repo README의 설치법 우선.
- **CRAK-Velo cisTopic 의존**: 무거움. CRAK-Velo가 cisTopic을 요구하면 `tf.yml` 주석의 cisTopic 줄 해제(또는 pycisTopic conda). TF/UniTVelo 버전이 가장 잘 깨지는 지점 — UniTVelo repo의 권장 TF 버전에 맞춤.
- **scVelo dynamical model**: `scv.tl.recover_dynamics`가 numba 컴파일로 첫 실행 느림(정상).

## 다음 (P0 종료)
env 구축 후 → MultiVelo 1-fit(원논문 124분/12-thread CPU 대조)으로 시간·메모리 측정 → `P0_provenance.md §3` 체크리스트 갱신 → P1 통일 전처리 진입.
