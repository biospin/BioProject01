# Env 구축 — HSPC velocity benchmark

> 5개 env로 분리한다. **이유(P0 핵심 발견)**: PyTorch(MultiVeloVAE/MoFlow) ↔ TensorFlow
> (CRAK-Velo/UniTVelo)가 한 env에서 CUDA/버전 충돌. 격리가 유일하게 안정적.
> **cellDancer는 별도 env**(2026-07-11): TF가 아니라 pytorch-lightning 기반이고 numpy==1.20.3 등
> 옛 버전을 전부 하드핀 → tf/scanpy와 공존 불가. tf.yml에서 분리(→ celldancer.yml).

## env 구성 (2026-07-11 정리·명명)

| env | method | 프레임워크 | GPU |
|---|---|---|---|
| `scv-preprocess` | 공통 전처리(P1) + 협업 JupyterLab 구동 | — | 불요 |
| `velo-mv` | MultiVelo, scVelo | numba | 불요 |
| `velo-torch` | MultiVeloVAE, MoFlow | PyTorch cu121 | ✅ A6000×3 |
| `velo-tf` | CRAK-Velo, UniTVelo | TensorFlow 2.13 | ✅ A6000×3 |
| `celldancer` | cellDancer(참고 method, 격리) | pytorch-lightning(하드핀) | 불요 |
| `seqtools` | STAR·sra-tools·velocyto (cross-dataset raw seq 처리) | — | 불요 |

> **명명·위치(2026-07-11):** velocity 메서드 env는 `velo-*` 접두(구 mv/tf/torch). 유틸(정렬·SRA·loom)은 `seqtools`로 통합(구 star+sratools+velocyto). 팀공유 `/opt/envs`=velo-mv·velo-tf·velo-torch·celldancer·seqtools(velocity 전부), 개인 `~/miniconda3/envs`=scv-preprocess(협업서버 구동용, jupyter로 팀 접근). `conda run -n <env>`는 envs_dirs로 자동 해소. ※ `/opt/envs`가 컨테이너 간 실제 공유 마운트인지는 팀원 `ls /opt/envs`로 확인 필요(미공유 시 `/workspace`로 이전). (BIOP02 `spatialpatho`는 별개, 손대지 않음.)

## 사전 준비
- miniconda 또는 mambaforge. **mamba 권장**(conda solve가 느림): `CONDA=mamba`.

## 생성
```bash
bash pipeline/hspc-velocity-benchmark/env/setup_envs.sh          # 4개 모두
CONDA=mamba bash .../env/setup_envs.sh mv                        # 하나만, mamba로
```

## 설치 순서(권장)
1. `velo-mv` — 가장 가볍고 baseline. 먼저 성공시켜 MultiVelo 1-fit으로 데이터 파이프 검증.
2. `scv-preprocess` — P1 전처리.
3. `velo-torch` — MultiVeloVAE/MoFlow (H1 핵심 쌍).
4. `velo-tf` — CRAK-Velo/UniTVelo. **`tensorflow[and-cuda]` 쓰지 말 것**(extra는 TF≥2.14에만 있어 무한 backtracking) → `tensorflow==2.13.*` 고정, GPU는 아래 cudatoolkit로 별도.
5. `celldancer` — 전용 격리 env(`celldancer.yml`). tf와 절대 합치지 말 것(numpy 하드핀 충돌).

## GPU 사용법 (팀 공용 — 본서버 3×RTX A6000, 48GB each)

### velo-tf env — GPU 설정 완료(2026-07-11). 팀원 누구나 바로 사용:
```bash
conda activate /opt/envs/velo-tf          # 공용 경로 활성화(자기 env 목록에 없어도 -p 경로로 됨)
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"   # A6000 3장 나오면 정상
```
- **`conda activate`만으로 GPU 자동 인식** — `activate.d/zz_cuda_ld.sh` 훅이 `LD_LIBRARY_PATH`를 자동 설정(수동 export 불필요). cudatoolkit 11.8 + cudnn 8.8.0 내장.
- ⚠️ **`tensorflow[and-cuda]` 금지**(unitvelo가 TF<2.14로 묶어 extra 미제공 → 무한 backtracking). TF2.13 고정 후 `mamba install -p /opt/envs/velo-tf -c conda-forge cudatoolkit=11.8 cudnn=8.8.0`으로 붙였음.

### 여러 명이 3장 나눠 쓰는 예절(중요):
```bash
export CUDA_VISIBLE_DEVICES=0        # 자기 GPU 1장만 지정(nvidia-smi로 빈 카드 확인 후)
export TF_FORCE_GPU_ALLOW_GROWTH=true # TF가 카드 메모리 전량 선점하지 않게(안 하면 48GB 통째 독점)
```
- TF는 기본적으로 **보이는 GPU 전부 + 메모리 전량**을 잡음 → 반드시 `CUDA_VISIBLE_DEVICES`로 카드 지정. `nvidia-smi`로 빈 카드 먼저 확인.
### velo-torch env — GPU 이미 설정됨(2026-07-11 확인). 팀원 바로 사용:
```bash
conda activate /opt/envs/velo-torch    # 또는 miniconda 쪽 torch env
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.device_count())"   # True 3
```
- torch 2.2.2+**cu121** + torch_scatter cu121. cu121 wheel이 **CUDA 라이브러리를 자체 번들** → cudatoolkit 설치·activate.d 훅 불필요(tf와 다름, 바로 인식). 드라이버 535(CUDA 12.4 지원)와 호환.
- 멀티유저 예절 동일: `export CUDA_VISIBLE_DEVICES=0` 로 카드 지정(torch는 명시 device 아니면 cuda:0만 씀). `nvidia-smi`로 빈 카드 확인.
- 참고: 11k cells는 CPU로도 충분(MultiVelo는 GPU 미지원). bootstrap 대량 반복 때만 GPU 권장.

## 검증 + lock (재현성)
```bash
conda run -n velo-mv     python -c "import multivelo, scvelo; print('mv ok')"
conda run -n velo-torch  python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
conda run -n velo-tf     python -c "import tensorflow as tf; print('tf', tf.__version__)"
# 성공한 env는 정확 버전 동결:
conda env export -n <env> > pipeline/hspc-velocity-benchmark/env/<env>.lock.yml
```
→ `.lock.yml`은 *commit* (재현용). 원본 `<env>.yml`은 느슨한 spec, lock은 정확 핀.

## Known gotchas (`검토필요:` — 머신에서 iteration 필요)
- **numpy<2 고정**: scvelo/scanpy 일부가 numpy 2.x 미대응. 충돌 시 numpy 1.26으로.
- **github 패키지 import 이름**: MultiVeloVAE/MoFlow/CRAK-Velo의 실제 import 이름은 repo 확인 후 검증 명령 수정. 설치 실패 시 repo README의 설치법 우선.
- **CRAK-Velo cisTopic 의존**: 무거움. CRAK-Velo가 cisTopic을 요구하면 `tf.yml` 주석의 cisTopic 줄 해제(또는 pycisTopic conda). TF/UniTVelo 버전이 가장 잘 깨지는 지점 — UniTVelo repo의 권장 TF 버전에 맞춤.
- **scVelo dynamical model**: `scv.tl.recover_dynamics`가 numba 컴파일로 첫 실행 느림(정상).
- **cellDancer 격리 필수**(2026-07-11): celldancer 1.1.7이 numpy==1.20.3·pandas==1.3.4·scipy==1.7.2·sklearn==1.0.1·skimage==0.19.2·pytorch-lightning==1.5.2를 전부 하드핀. tf(numpy≥1.22)와 한 env면 `ResolutionImpossible`. 반드시 `celldancer.yml` 전용 env(python 3.9 빈 env + pip celldancer). 진짜 충돌은 pip 로그 끝 "depends on numpy" 줄에서 확인(and-cuda 경고는 오진 유발 표면 증상).

## 다음 (P0 종료)
env 구축 후 → MultiVelo 1-fit(원논문 124분/12-thread CPU 대조)으로 시간·메모리 측정 → `P0_provenance.md §3` 체크리스트 갱신 → P1 통일 전처리 진입.
