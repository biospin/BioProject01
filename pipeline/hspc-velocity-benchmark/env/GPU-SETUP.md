# DL arm(MultiVeloVAE / MoFlow) — GPU 머신 셋업·실행 가이드

> 2026-06-15 이 Mac(CPU)에서 **설치·import·API까지 검증** 완료. 실제 full run은 GPU 머신에서.
> CPU full run은 비현실적임을 실측 확인(아래 §런타임).

## 1. torch env 빌드 (miniforge)
```bash
mamba env create -f env/torch.yml          # torch+lightning+scvelo+scanpy (CPU). GPU는 §4.
# env에 setuptools/pkg_resources 누락 → 보정 (MoFlow가 옛 pkg_resources API 사용)
python -m pip install 'setuptools<80' fastdtw     # setuptools 80+는 pkg_resources 제거
python -m pip install 'git+https://github.com/welch-lab/MultiVeloVAE.git'   # → multivelovae 0.1.0
```

## 2. MoFlow — pip 불가, clone + 패치 2건
MoFlow는 패키지가 아님(setup.py 없음) → clone 후 PYTHONPATH로 사용. **repo에 버그 2건 → 패치 필요**:
```bash
git clone https://github.com/AriHong/MoFlow.git vendor/MoFlow
# 패치 ①: src/MoFlow/src/MoFlow/eval_dtw.py 의 plot_dtw 시그니처에 잉여 '):' 줄(≈94행) 제거
# 패치 ②: src/MoFlow/src/MoFlow/__init__.py 의 `from .simulation import simulate` 주석 처리
#         (simulation.py가 repo에 누락; 학습엔 불필요)
export PYTHONPATH=$PWD/vendor/MoFlow/src
```
- import 확인: `from MoFlow.moflow import MOFlow`

## 3. 실행 API (검증함)
- **MoFlow**: `m = MOFlow(adata_rna, adata_atac, max_epoches=200, min_epoches=20, embed='X_umap', device=<gpu>)` 후 **`m.velocity(adata_rna, n_jobs=N)`** 가 per-gene 학습 트리거.
  - 입력: `adata_rna.layers['Ms','Mu']`(scv.pp.moments), `adata_atac.layers['Mc']`(chromatin smoothing), `adata.obsm['X_umap']`.
  - **gene별로 PyTorch-Lightning Trainer를 따로 돌림** (per-gene 오버헤드 큼).
- **MultiVeloVAE**: `import multivelovae` (0.1.0, BSD-3). API는 welch-lab repo `/notebook` 데모 기준.
- 공통 입력 substrate = P1 산출(`data/processed/rna_spliced_unspliced.h5ad` + `atac_peaks.h5ad`). GPU 머신으로 복사.

## 4. GPU 활성화
- `torch.cuda.is_available()` 확인. torch CUDA wheel: `pip install torch --index-url https://download.pytorch.org/whl/cu121`(드라이버에 맞춰).
- MoFlow는 `device=<not None>` → accelerator="gpu". MultiVeloVAE는 데모 config의 device 인자.
- macOS는 loky 병렬 시 `OMP_NUM_THREADS=1` 필요(SIGSEGV 회피). Linux GPU 머신에선 무관.

## 5. 런타임 (이 Mac CPU 실측 → GPU 머신 결정 근거)
| method | CPU(이 Mac) | 근거 |
|---|---|---|
| **MoFlow** | **수일(비현실적)** | 실측: 8 genes × 2 epochs > 11분 미완료(n_jobs=6). per-gene Trainer 오버헤드 지배 → 700 gene × 실효 20–50 epoch = 일 단위 |
| **MultiVeloVAE** | **~1–2일(추정)** | VAE; 원논문 GPU "수 시간", CPU 10–30× |
| (참고) MultiVelo | 7.4h ✅ 완료 | numba ODE, CPU |
- **결론: DL arm은 GPU 필수.** GPU면 둘 다 수 시간 내 예상.
