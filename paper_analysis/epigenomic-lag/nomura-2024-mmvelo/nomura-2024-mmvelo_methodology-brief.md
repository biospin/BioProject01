# Methodology Brief — mmVelo (Nomura 2024, bioRxiv preprint)

> 재현·검토용 압축본. 본 paper는 *peer-review 전 preprint*이므로 본 brief에서 인용한 수치·식·default 값은 PDF v1 (2024-12-17) 기준이며 publication 시 재확인.

## 한 줄 요약

mmVelo는 RNA velocity (splicing kinetics anchor)로 cell-state transition $d_n$을 추정하고, 그 transition을 *peak-specific ATAC decoder*에 통과시킨 차분 $\Delta \text{ATAC}_{np} = C_p^a \odot (f_p^a(z_n + \rho d_n) - f_p^a(z_n))$으로 *single-peak chromatin velocity*를 정의하는 *mixture-of-experts VAE*.

## Input / Output

- **Input**: per-cell $(a_n, u_n, s_n)$ — peak-level scATAC count + unspliced + spliced mRNA count. 10x Multiome / SHARE-seq.
- **Output**: 
  - Cell-state latent $z_n$ (multimodal).
  - Cell-state transition $d_n$.
  - $\Delta \text{ATAC}_{np}$ (peak-level chromatin velocity).
  - $\Delta \text{spliced}_{ng}$, $\Delta \text{unspliced}_{ng}$.
  - Motif velocity $dy_n/dt = (dy_n/dz_n)^T d_n$ (chromVAR extension).
  - TF-peak regulatory edges (GRNBoost2 + permutation FDR).
  - Cross-modal velocity (singleome → missing modality velocity).

## Core idea (수식 골격)

1. **Multimodal cell state** (PDF p.12 §5.2):
   $$q(z_n | a_n, s_n, u_n) = \tfrac{1}{2}\left( q(z_n | a_n) + q(z_n | s_n, u_n) \right)$$
   ZINB likelihood for ATAC, NB likelihood for spliced·unspliced.

2. **Splicing kinetics anchor** (PDF p.14 §5.4): observed target
   $$\frac{ds_n}{dt}\bigg|_{\text{obs}} = \frac{\tanh(\beta \odot C^u \odot f^u(z_n) - \gamma \odot C^s \odot f^s(z_n))}{\|\cdot\|_2}$$
   ($\beta, \gamma$ learnable, steady-state init + deviation regularizer).

3. **vMF likelihood for predicted velocity** (PDF p.13 §5.4):
   $$\frac{ds_n}{dt}\bigg| z_n, d_n \sim \mathrm{vMF}\left(\frac{\tanh(C^s \odot (f^s(z_n + \rho d_n) - f^s(z_n)))}{\|\cdot\|_2}, \kappa\right), \quad \rho = 0.01, \kappa = 1$$

4. **Peak-level chromatin velocity** (PDF p.14 §5.5):
   $$\Delta \text{ATAC}_{np} = C_p^a \odot (f_p^a(z_n + \rho d_n) - f_p^a(z_n))$$
   — *peak-specific decoder branch* + 공통 transition $d_n$. **per-peak kinetic rate parameter는 없다.**

## 3-stage training (PDF p.11 §5.1, p.13–14)

| Stage | 목적 | 학습 대상 | 학습률 / epoch |
|---|---|---|---|
| 1 | MoE-VAE cell state inference | 전체 encoder/decoder + dispersion | AdamW lr=0.0001, 500 epoch, early stop 30 epoch |
| 2 | Smoothed-profile decoder fine-tuning (k=50 NN) | decoder만 | AdamW lr=0.01 |
| 3 | Cell-state dynamics ($d_n$ encoder + $\beta, \gamma$) | $d_n$ encoder + splicing rate, 나머지 frozen | AdamW lr=0.0001 |

Train/val split 90/10. Minibatch 128. 

## Dependencies (PDF + code repo 추정)

- PyTorch.
- scvi-tools (VAE backbone scaffold, Lopez 2018 인용).
- Velocyto (`run10x`, `run` command) — unspliced/spliced quantification.
- Signac — peak filtering (`LinkPeaks`, ±50kb TSS for DORC, ±500kb for feature selection at correlation > 0.01).
- Seurat `SCTransform` — preprocessing normalization (input feature 선정용).
- Scanpy — clustering, annotation, standard pipeline.
- pycisTarget (SCENIC+ stack) — motif enrichment.
- GRNBoost2 (Arboreto) — TF-peak regression.
- chromVAR / `motifmatchr` — motif activity, motif velocity 기반.
- JASPAR2022 — motif matrix.
- GREAT — peak-gene functional enrichment (Fig 5h).

## Compute requirements

- GPU 1대 (PyTorch + ZINB decoder + 500 epoch).
- Memory: 미보고. 우리 HSPC (수만 cell, 수만 peak) 기준 *128GB RAM + GPU 16GB* 정도 추정 (검토필요 — code 실행으로 검증).
- Training time: 미보고. SHARE-seq mouse skin (예: ~수만 cell) 기준 *수 시간 ~ 1일* 추정.

## Reproducibility ROI

| 항목 | 평가 | 비고 |
|---|---|---|
| Code 존재 | yes | https://github.com/nomuhyooon/mmVelo (PyTorch) |
| DOI-cited code (Zenodo) | **no** | publication 시점이라고 PDF p.23 §10.3 명시 |
| License 명시 | **미확인** | LICENSE 파일 직접 확인 필요 |
| Tutorial / example notebook | **미확인** | repo 직접 확인 필요 |
| Datasets public | **yes** | 10x E18, GSE140203, GSE162170 모두 GEO public |
| Hyperparameter table | yes (Methods §5.6) | 단 sensitivity 실험 없음 |
| Random seed 기록 | 미보고 | 검토필요 |
| Conda/Docker env | **미확인** | repo 직접 확인 필요 |

**ROI 등급**: **중상** — Code repository 존재 + 모든 dataset public이므로 *완전 재현*은 *데이터 다운로드 + GPU 학습* 단계만 거치면 됨. 단 *peer-review 후 변경*과 *Zenodo deposit 부재*는 리스크.

## 우리 데이터에 적용 시 체크리스트 (HSPC 10x Multiome, GSE209878)

- [ ] GitHub repo clone, README 읽기, LICENSE 확인.
- [ ] Conda env 또는 Docker 준비 (PyTorch + scvi-tools + Signac/Seurat R-Python 혼합 환경).
- [ ] HSPC dataset preprocessing: Velocyto `run10x`로 unspliced/spliced, Signac `LinkPeaks` (±50kb + ±500kb correlation filtering for DORC + features).
- [ ] cell type annotation (standard Scanpy + marker gene). interneuron-equivalent (HSPC에서는 *non-differentiating cell*) 제외.
- [ ] mmVelo 학습 (3 stage, default hyperparameter).
- [ ] *동일 dataset*에 MultiVelo, MultiVeloVAE, MoFlow도 적용 (비교 benchmark).
- [ ] Peak-level chromatin velocity 위에 *switch-time detection* 알고리즘 적용 → promoter–enhancer lag 정량.
- [ ] Cell cycle / burst kinetics confound 통제 (CLAUDE.md §2 "burst kinetics + cell cycle" 가이드).
- [ ] 결과를 `analysis/epigenomic-lag/_evidence/week3/`에 head-to-head row로 저장.

## 주요 risks (재현 관점)

- **Peer-review 전 변경 가능성**: publication 시 default hyperparameter, loss term, ELBO 변경 가능.
- **Hyperparameter sensitivity 미보고**: $\rho, \kappa, k, lr$이 우리 dataset에서 동일 default로 잘 동작한다는 보장 없음 → grid search 시간 별도 예산.
- **smoothed profile imputation effect**: k=50 NN 평균이 *batch / cell cycle confound* 흡수 위험. 결과 해석 시 confound 통제 필수.
- **causal language**: TF-peak regulation 출력은 *putative* → 우리 분석 노트에도 *predicted* hedge 일관 사용.

## 핵심 차용 후보 (우리 자체 method 개발에서)

- **MoE-VAE backbone**: 우리 multimodal cell-state inference의 기본 framework으로 차용.
- **Splicing-kinetics anchor + decoder difference projection**: 우리 *peak-level lag estimator*의 첫 baseline.
- **chromVAR motif velocity 식**: 우리 TF-level lag analysis에 차용 가능.
- **GRNBoost2 + permutation FDR 0.001**: TF-peak edge inference 차용 가능.

## One-line takeaway

mmVelo는 *peer-review 전*이지만 *peak-level chromatin velocity*를 정의하는 *유일한 직접 후보*이고, 우리 HSPC pipeline에서 *MultiVelo와 head-to-head 적용 + switch-time detection 추가*가 가장 ROI 큰 차용 시나리오다.
