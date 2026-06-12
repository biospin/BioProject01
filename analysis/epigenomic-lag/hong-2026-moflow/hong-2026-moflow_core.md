# Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states

Citation: `@hong2026moflow` — Hong A, Lee S, Kim K. *Nat Commun* 17(1):566 (2025–2026). DOI: 10.1038/s41467-025-67259-6. PMCID: PMC12808240. PMID: 41457082.

> 본 분석은 `sources/hong-2026-moflow.pdf` (17 page Nature Communications open access PDF, Received 2025-06-20, Accepted 2025-11-25) + `sources/abstract.txt` (PubMed) + Supplementary 6종 (Supp-1 Tables PDF, Supp-2 description PDF, Supp-3/4/5 source-data xlsx, Supp-6 Reporting Summary)을 근거로 한다. 외부 지식은 `외부 맥락:` / `해석:` / `추정:` / `미제공:` / `검토필요:` / `질문:` prefix로 분리한다. Cross-reference 대상: `@li2023multivelo` (MultiVelo, Nat Biotechnol 2023), `@li2025multivelovae` (MultiVeloVAE, Nat Commun 2025).

---

## Executive Summary

- **무엇**: MoFlow는 chromatin accessibility $c$, unspliced $u$, spliced $s$를 입력으로 받아 *latent time을 추정하지 않고* cell-specific kinetic parameter $(\alpha_c, \alpha, \beta, \gamma)$를 두 개의 DNN으로 학습하는 *relay-velocity 기반 multi-omic RNA velocity framework*. `@li2023multivelo`(MultiVelo)의 ODE 가정과 `@li2025multivelovae`(MultiVeloVAE)의 VAE+latent-time 접근과 달리, cellDancer의 *local neighbor displacement cosine loss*에 chromatin opening/closing 양쪽 가설을 *동시 평가 후 lower-loss 선택*하는 구조를 추가.
- **모델 / 방법**: $dc/dt = \alpha_c (k - c)$, $du/dt = \alpha c - \beta u$, $ds/dt = \beta u - \gamma s$ (Eq. 1–3)를 cell-wise discrete time-step으로 풀고, 각 cell $j$의 chromatin-aware 예측 velocity vector $v_j^{\mathrm{cus}}(k=0)$과 $v_j^{\mathrm{cus}}(k=1)$ 중 *Mahalanobis 거리 기반 neighbor*에 대한 cosine loss가 더 낮은 쪽 (Eq. 25)을 학습 signal로 사용. 2-stage 학습 (RNA $\to$ joint).
- **핵심 결과**:
  - ① **Human brain cortex 10x Multiome** (Trevino 2021, GSE162170; 4,693 cells × 842 genes): CBDir 0.362 vs MultiVelo 0.211, cellDancer −0.015, scVelo 0.211 (Supp Table 1, Fig. 2d).
  - ② **Mouse skin SHARE-seq** (Ma 2020, GSE140203): CBDir 0.144 vs MultiVelo 0.115, cellDancer 0.026, scVelo 0.005; LCHA gene (chromatin 안정 + transcription 가변) group이 cell cycle score와 가장 강한 상관 (Fig. 5).
  - ③ **10x embryonic mouse brain (E18)**: CBDir 0.535 vs MultiVelo 0.155, cellDancer 0.132, scVelo 0.273 — *모든 dataset 중 격차 최대* (Fig. 6d, Supp Table 1).
  - ④ **Human HSPC 10x Multiome** (Li 2023, GSE209878): CBDir 0.191 vs MultiVelo 0.063, cellDancer −0.056, scVelo −0.103 (Supp Table 1, Supp Fig. 5c).
  - ⑤ **시간 lag 메커니즘 해석**: 12 gene cluster에서 chromatin–spliced RNA $(c\!-\!s)$ lag의 *negative sign* 빈도가 두 mechanism으로 분리 — (i) cluster 0–3은 nuclear half-life 짧음 + 빠른 export → "rapid RNA turnover", (ii) cluster 10은 nuclear-compartment-sequestered RNA (polycomb / speckle, Khyzha 2025 ref. 44)의 conditional export (Fig. 7).
- **우리 적용**: HSPC 10x Multiome pipeline에서 *MultiVelo 대체 candidate* — `@li2025multivelovae`(MultiVeloVAE)와 두 갈래 후속 비교 대상. MoFlow는 *latent time 추정 자체를 회피*하고 local neighbor displacement만 사용한다는 점이 우리 데이터의 *gene-specific lag* 분석에는 강점, 반면 multi-sample 통합 / Bayesian differential test가 없는 점이 약점.
- **심층**: 한계·재현 ROI는 `hong-2026-moflow_lens-academic.md` / `hong-2026-moflow_lens-industry.md` / `hong-2026-moflow_methodology-brief.md` 참고.

---

## Identity

- **Title**: Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states
- **Authors**: Ari Hong (Seoul National University, Interdisciplinary Program in Bioinformatics), Sangseon Lee (Inha University, Department of Artificial Intelligence — corresponding, ss.lee@inha.ac.kr), Kwangsoo Kim (Seoul National University Hospital, Transdisciplinary Medicine & Center for Data Science, Healthcare AI Research Institute & College of Medicine — corresponding, kwangsookim@snu.ac.kr).
- **Venue / Year**: *Nature Communications* 17(1):566 (2025–2026). Received 2025-06-20, Accepted 2025-11-25, Published online 2025-12-29.
- **Funding** (Acknowledgements, p16):
  - Basic Science Research Program through NRF, MOE (RS-2024-00410829) — A.H.
  - IITP grant (MSIT) (No. RS-2022-00155915, AI Convergence Innovation Human Resources Development, Inha University) — S.L.
  - Bio&Medical Technology Development Program of NRF (MSIT) (No. RS-2022-NR067309) — S.L.
  - Korea National Institute of Health (KNIH) research project (No. 2024-ER-0801-01) — K.K.
- **COI**: 저자 명시 — "no competing interests" (Competing interests, p16).
- **License**: CC BY-NC-NC-ND 4.0 (Open Access, "by-nc-nd/4.0"). 다른 사람의 *adapted material 재배포 권한 없음* — 본 분석 노트는 derivative work이므로 외부 공유 시 주의 필요.
- **Code**: https://github.com/AriHong/MoFlow (PyTorch Lightning 기반). Zenodo archive DOI 10.5281/zenodo.17666878 (Hong 2025, ref. 47). `검토필요: GitHub 페이지에서 license type (예: MIT, BSD, GPL) 확인 필요. paper Code availability에는 license 명시 없음.`
- **Data availability** (p15):
  - Human brain multi-ome: GEO GSE162170 + https://github.com/GreenleafLab/brainchromatin (Trevino 2021, ref. 13).
  - 10x embryonic mouse brain: 10x Genomics dataset https://www.10xgenomics.com/resources/datasets/fresh-embryonic-e-18-mouse-brain-5-k-1-standard-1-0-0.
  - SHARE-seq mouse skin: GEO GSE140203 (Ma 2020, ref. 28).
  - 10x Human HSPC: GEO GSE209878 (`@li2023multivelo`의 신규 dataset, ref. 12).
  - External: Allen Brain Atlas (https://portal.brain-map.org/atlases-and-data/rnaseq, ref. 27).
  - External: RNA half-life data (Ietswaart 2024 ref. 43, NIH3T3 mouse cell), polycomb/speckle RNA gene set (Khyzha 2025 ref. 44).
- **Predecessor / 직접 비교 method**:
  - `@li2023multivelo` (MultiVelo, ref. 12) — ODE-based, discrete 4 state, shared kinetic regime.
  - cellDancer (Li 2024, ref. 11) — relay velocity 원조, RNA-only.
  - scVelo dynamical (Bergen 2020, ref. 7) — RNA-only ODE.
- **본 paper의 직접적 sibling**: `@li2025multivelovae` (MultiVeloVAE, 2025-11-20 publication) — MoFlow와 같은 *post-MultiVelo* timeframe (2개월 차이). 두 method 모두 MultiVelo의 후속이지만 본문에서 *서로 인용·비교 없음* (MoFlow 본문에 MultiVeloVAE 인용 부재 — 동시 publication cycle이라 검토 시점 차이로 추정).

---

## Background

### 배경 스토리

- **문제의 출발점** (§Introduction p1–2): scRNA-seq snapshot은 cell을 *파괴*하므로 동일 cell의 시계열을 직접 측정 불가. computational reconstruction이 필수. 현재 RNA velocity는 그 standard approach 중 하나로, unspliced/spliced ratio를 통해 future transcriptional state를 예측 (La Manno 2018, ref. 6).
- **선행 접근 A — ODE 기반 RNA velocity** (La Manno 2018 ref. 6, scVelo dynamical Bergen 2020 ref. 7): gene-specific kinetic rate + latent time을 동시 추정. 단 *single transcriptional path per gene* 가정으로 heterogeneous system에서 부정확.
- **선행 접근 B — Neural network 기반** (VeloAE ref. 8, VeloVAE ref. 9, VeloVI ref. 10): latent space 학습으로 complex structure 포착, *global temporal ordering + synchronous transcription/splicing* 가정. RNA-only.
- **A, B의 공통 한계** (§Introduction p1–2): ① RNA abundance만 사용 → chromatin accessibility 같은 regulatory context 미반영. ② global latent time 가정 → local regulatory dynamics 손실.
- **선행 접근 C — cellDancer** (Li 2024, ref. 11): *local relay velocity model + latent time 없음*. 그러나 transcriptomic data only — chromatin 정보 없음.
- **선행 접근 D — MultiVelo** (`@li2023multivelo`, ref. 12): ODE 기반에 chromatin accessibility 추가. 단 *fixed gene classification* (induction-only / repression-only / M1 complete / M2 complete)과 *shared kinetic regime* (모든 cell 동일 ODE parameter) 가정.
- **이 논문으로 이어지는 gap** (§Introduction p2, 본문에서 정리): "three key challenges remain unresolved: (i) modeling dynamics with branching trajectories without fixed gene labels, (ii) capturing asynchronous transcriptional kinetics, and (iii) integrating epigenomic context without relying on rigid structural assumptions." → MoFlow가 풀고자 하는 세 가지 task.

### 기본 개념

- **유전자 발현 흐름** (§Methods Eq. 1–3): $dc/dt = \alpha_c (k - c)$ (chromatin), $du/dt = \alpha c - \beta u$ (transcription), $ds/dt = \beta u - \gamma s$ (splicing). MultiVelo의 ODE를 그대로 따르되 *gene-specific 두 rate constant $(\alpha_{co}, \alpha_{cc})$를 cell-specific 단일 rate $\alpha_c$로 통합*. $k \in \{0, 1\}$은 chromatin opening/closing state.
- **Relay velocity 모델** (cellDancer, Li 2024 ref. 11): cell $j$의 neighbor $j'$이 cell $j$의 *future state proxy*라는 가정으로, predicted velocity $v_j$와 transcriptomic displacement $x_{j'} - x_j$ 사이 cosine distance를 최소화 (Eq. 15). global latent time 없이 *순간적 local direction*만 학습.
- **Cosine similarity loss**: $L_j = \min_{j' \in \mathcal{N}_j} (1 - \cos(v_j, x_{j'} - x_j))$ (Eq. 15). neighbor 중 *direction-best-fit* 하나만 선택.
- **CBDir (cross-boundary direction correctness)** (Qiao 2021, ref. 8; UniTVelo Gao 2022, ref. 40): 두 cell type 경계에서 velocity vector가 *source $\to$ target* 방향과 얼마나 정렬되는지 측정. 본 paper의 주 성능 지표 (Eq. 27–28, Supp Table 1).
- **DTW (dynamic time warping)** (Berndt 1994 ref. 25, fastdtw Salvador 2004 ref. 26): 두 시계열의 *optimal warping path*를 찾는 nonlinear alignment. chromatin–spliced RNA $(c\!-\!s)$ lag, unspliced–spliced $(u\!-\!s)$ lag 정량에 사용.
- **DAC score (distribution of average across cell types)** (§Methods "Distribution of averages..."): gene별 parameter $x$ (예: $\alpha$, $c$)의 *cell type 간 mean의 variance*. $\mathrm{DAC}(x)_g = \frac{1}{K}\sum_{k=1}^{K} (\mu_{x,g,k} - \bar{\mu}_{x,g})^2$. 높을수록 cell type 간 strong heterogeneity.
- **m1, m2 score**: chromatin closing과 transcription repression 사이의 *discordance* 정량. m1 = chromatin이 닫혔는데 unspliced RNA 증가 (예: model 1 = chromatin-first repression), m2 = chromatin이 열렸는데 unspliced RNA 감소 (예: model 2 = RNA-first repression). MultiVelo의 *discrete M1/M2 model*을 *continuous score*로 일반화.
- **RNA-on / RNA-off score**: 각 cell이 *unspliced + spliced 양쪽 모두 positive velocity*면 "on" (Eq. 29), 양쪽 모두 negative면 "off" (Eq. 30). MultiVelo의 "on/off/complete" discrete state를 *continuous fraction*으로 일반화.
- **외부 맥락**: relay velocity 원조 cellDancer는 ICML 2022 NeurIPS 류 conference보다는 *Nat Biotechnol* (2024)에서 발표 — 본 paper와 같은 author commonity (Li S.) 추정 가능하나 본 paper는 *공동 저자 아님* (Hong/Lee/Kim 3명). `검토필요: cellDancer 저자 (Shengyu Li 등)와 본 paper의 Sangseon Lee가 다른 인물임 — 한국 이름 표기 동일성 주의.`

### 이 논문이 필요성

- **핵심 이유**: MultiVelo가 chromatin–RNA dynamics를 처음 integrate했지만 (a) gene-specific *discrete* class assignment 필요, (b) 모든 cell이 *동일* kinetic regime 공유, (c) gene별 *latent time*이 trajectory를 *이상적 c→u→s 순서*로 over-correct할 가능성 — 이 셋을 해소할 *cell-specific + latent-time-free + chromatin-aware* framework가 부재.
- **기존 방법으로 부족했던 지점**:
  - scVelo / cellDancer는 chromatin 무시 → priming 못 봄.
  - MultiVelo는 chromatin 포함하지만 *모든 cell에 동일 ODE* → cell type 간 *transcription rate variability* (LCHA gene 같은 group) 못 봄.
  - MultiVelo의 *gene-specific latent time*은 chromatin–RNA lag이 *positive lag (c→s 표준 순서)* 방향으로 over-correct되어 *진짜 negative lag* (RNA가 chromatin보다 먼저 변화) 신호를 *artifact로 사라지게* 만든다는 점 (Fig. 3g vs 3f의 PDGFRA, MAP3K1 예시).
  - cellDancer는 cell-specific local kinetics를 잡지만 chromatin context 부재 → LCHA 같은 *chromatin-independent transcriptional flexibility* gene 구분 불가.
- **이 논문이 해결하려는 방향** (§"MoFlow: deep learning framework..." p2–3):
  - chromatin opening/closing assumption 두 가설을 *모두 시도하고 lower-loss 선택* → fixed gene classification 회피.
  - cell-wise kinetic parameter $(\alpha_c, \alpha, \beta, \gamma)$ 학습 → cell type 간 heterogeneity 포착.
  - relay velocity (latent time 없음) + 2-stage 학습 (RNA → joint) → chromatin sparsity 대응.
  - DTW-based $(c\!-\!s)$, $(u\!-\!s)$ lag를 *global pseudotime* (MoFlow) vs *gene-specific latent time* (MultiVelo) 양쪽에 대해 비교 → MultiVelo의 over-correction 입증.

---

## Methods

### 이 method가 푸는 문제

- **Formal task** (§Methods "Extension of relay velocity model to multi-omics" p13): cell × gene tuple $(c, u, s)$에서 cell-specific kinetic parameter $\theta_j = \{\alpha_c, \alpha, \beta, \gamma\}_j$를 *gene 단위로* 학습. 동시에 cell-wise chromatin state $k_j \in \{0, 1\}$을 *추정*. *Latent time은 추정하지 않음* — relay-based local neighbor displacement만 사용.
- **입력**: cell × gene matrix
  - $c \in \mathbb{R}^{N \times G}$: chromatin accessibility (peak-to-gene aggregation + TF-IDF normalization + WNN smoothing, Seurat v4 ref. 45, $k=50$ neighbor).
  - $u \in \mathbb{R}^{N \times G}$: unspliced RNA count (velocyto + scanpy + scVelo preprocessing).
  - $s \in \mathbb{R}^{N \times G}$: spliced RNA count.
  - 모두 $[0, 1]$ min-max normalize.
- **출력**:
  - cell-wise kinetic parameter $(\alpha_c, \alpha, \beta, \gamma)_j$ via $\Phi_{\theta_c}$, $\Phi_{\theta_{us}}$.
  - cell-wise chromatin state $k_j \in \{0, 1\}$ (warm-up 후 best-fit selection).
  - cell-wise 3D velocity vector $v_j^{cus} = (dc/dt, du/dt, ds/dt)_j$.
  - global pseudotime (post hoc, scVelo `tl.velocity_pseudotime`).
  - downstream: RNA-on / RNA-off / m1 / m2 score, DAC score, DTW lag.
- **추정 대상**: 두 DNN의 weight $\theta_c$ (chromatin head), $\theta_{us}$ (RNA head). 각 gene별 독립 학습 — *gene-wise inference* (gene 간 정보 공유 없음).
- **중요한 hidden assumption**:
  - (1) chromatin → transcription 인과 (model 0 배제 — chromatin이 transcription의 *rate parameter*로 작동).
  - (2) neighbor in joint $(c, u, s)$ space (Mahalanobis distance, default 40 neighbor)가 *future state proxy*.
  - (3) chromatin은 RNA보다 *slowly evolving + noisier* → 2-stage 학습 정당화.
  - (4) cell-wise kinetic은 *gene 간 독립*. gene network 정보 미사용.
  - (5) ODE를 *discrete Euler-step*으로 풀음 (Eq. 13, 14, 17의 $\Delta t$ 형식).
  - (6) opening/closing 양쪽 시나리오 중 *lower-loss 자동 선택* — chromatin state $k$가 *posterior 추론 없이 hard label*로 결정.

### 확률 / 통계학적 구조

- **Model family**: deep neural network + ODE-discretized prediction + cosine similarity loss. *확률 모델이 아님* — 명시적 likelihood나 prior 없음. cellDancer 계승의 *deterministic discriminative* 구조.
- **Generative ODE** (Eq. 1–3):

$$\frac{dc}{dt} = \alpha_c (k - c), \quad \frac{du}{dt} = \alpha c - \beta u, \quad \frac{ds}{dt} = \beta u - \gamma s$$

- **Discrete update** (Eq. 13, 14, 17):

$$\frac{u(t + \Delta t) - u(t)}{\Delta t} = \alpha(t) - \beta(t) u(t), \quad \frac{s(t + \Delta t) - s(t)}{\Delta t} = \beta(t) u(t) - \gamma(t) s(t)$$

$$\frac{c(t + \Delta t) - c(t)}{\Delta t} = \alpha_c(c(t), u(t), s(t)) \cdot (k(t) - c(t))$$

- **두 DNN architecture** (§Methods "Extension of relay velocity model..." 후반, p13):
  - $\Phi_{\theta_c}: (c, u, s) \to (\alpha_c, k)$ (chromatin head, output 1 또는 2 node).
  - $\Phi_{\theta_{us}}: (c, u, s) \to (\alpha, \beta, \gamma)$ (RNA head, output 3 node).
  - 공통 구조: input layer ($3N$ node) → FC hidden $(64, 48, 32)$ + ReLU → output layer ($N$ or $3N$ node) + Sigmoid (parameter $[0, 1]$ 제약).
  - learning rate $0.001$, weight decay $0.04$ (L2 regularization).
- **Loss formulation** (Eq. 20–25):
  - First, find optimal future cell among RNA-only neighbor $\mathcal{N}_j^{cus}$:

  $$j^* = \arg\min_{j' \in \mathcal{N}_j^{cus}} L_{j'}^{us}, \quad L_{j'}^{us} = 1 - \cos(v_j^{us}, x_{j'}^{us} - x_j^{us})$$

  - Evaluate chromatin scenarios (open $k=1$, close $k=0$):

  $$L_j^{cus, k=1} = 1 - \cos\!\left(v_j^{cus}(k=1),\, x_{j^*}^{cus} - x_j^{cus}\right), \quad L_j^{cus, k=0} = 1 - \cos\!\left(v_j^{cus}(k=0),\, x_{j^*}^{cus} - x_j^{cus}\right)$$

  - Warm-up (default 20 epochs): $L_j^{\mathrm{total}} = \frac{1}{2}(L_j^{cus, k=1} + L_j^{cus, k=0})$.
  - After warm-up: $L_j^{\mathrm{total}} = \min(L_j^{cus, k=1}, L_j^{cus, k=0})$ (Eq. 25).
  - Total gene loss: $L_i = \frac{1}{N}\sum_j L_{ij}^{\mathrm{total}}$.
- **Neighbor 정의** (§"Extension of relay velocity model..." p13): Mahalanobis distance in joint $(c, u, s)$ space, default $n_{\mathrm{neighbors}} = 40$. Mahalanobis로 *modality 간 variance scale 차이 보정* — 단순 Euclidean보다 robust.
- **Optimizer**: Adam, weight decay 0.04, early stopping (loss 10 epoch마다 점검, max 200 epoch). PyTorch Lightning 구현.
- **Latent variable / hidden state**:
  - cell-gene별 $\alpha_c, \alpha, \beta, \gamma \in [0, 1]$ — Sigmoid output, *deterministic*.
  - cell-gene별 $k \in \{0, 1\}$ — warm-up 후 hard-selected.
  - latent time *없음* (이게 MoFlow의 핵심 차별).
- **Inference / optimization**:
  - 2-stage 학습 (§"Extension..." p13): Stage 1 — RNA-based kinetic만 (chromatin 학습 제외) with neighborhood alignment. Stage 2 — chromatin parameter joint 학습, alignment는 freeze.
  - GPU 가속 — 구체 환경 본문 미명시. `미제공: 본문에 GPU model, VRAM, runtime 정보 부재. Reporting Summary에 hardware 미명시.`
- **Noise, sparsity, uncertainty 처리**:
  - **Sparsity**: ATAC 자체는 WNN smoothing (k=50, Seurat v4) + peak-to-gene aggregation + TF-IDF normalization으로 미리 처리. RNA는 scanpy + scVelo standard preprocessing.
  - **Cell-to-cell noise**: 명시적 처리 없음. neighbor displacement 자체가 *implicit smoothing*.
  - **Parameter uncertainty**: 직접 추정 없음 (cellDancer/MultiVeloVAE는 가능). *deterministic point estimate*.
  - **Multiple testing**: 2-sided t-test (Fig. 2f, 2g, 2h, 2i, 2j, 4f) + Mann–Whitney U test (Fig. 5c) + Fisher's exact test (Fig. 7g) + one-sided KS test (Fig. 7e). *명시적 multiple comparison correction은 본문 부재* (Bonferroni / BH adjustment 언급 없음). `검토필요: Fig. 7e의 multiple KS test (16 cluster × 4 half-life type)는 multiple testing adjustment 필요.`
  - **Chromatin state uncertainty**: hard min selection (Eq. 25)이라 *soft posterior 없음*. 동일 cell이 *border-line case*일 때 stability 문제 가능.

### 핵심 method insight

- **기존 방법의 한계**:
  - **MultiVelo** (`@li2023multivelo`): (1) gene별 *discrete 4 state* (priming / coupled-on / decoupled / coupled-off) + *2 model* (M1/M2) 강제 할당, (2) 모든 cell에 *동일* ODE parameter, (3) gene-specific *latent time*이 trajectory를 *이상적 c→s 순서*로 over-correct.
  - **scVelo / cellDancer**: chromatin 무시 → priming 못 봄. cellDancer는 cell-specific kinetic 가능하지만 RNA only.
  - **shared limitations**: branching trajectory에서 *backflow* artifact, *asynchronous regulation* 미포착.
- **이 논문의 바꾼 가정**:
  - **Latent time 자체 제거**: cellDancer 계승. global pseudotime이 *필요하면 post hoc* (scVelo `tl.velocity_pseudotime`).
  - **chromatin state $k$의 dynamic per-cell selection**: warm-up 후 lower-loss scenario 채택 → fixed gene classification (MultiVelo의 M1/M2) 회피.
  - **두 DNN으로 chromatin / RNA head 분리** + **2-stage 학습**: chromatin이 slower + noisier라는 점을 학습 schedule에 반영.
  - **Mahalanobis neighbor in $(c, u, s)$ joint space**: cellDancer의 expression-only neighbor와 다르게 *chromatin과 RNA 양쪽 정보로 future state proxy 정의*.
- **새로 추가한 변수 / 구조**:
  - cell-wise chromatin rate $\alpha_c(c, u, s)$ — MultiVelo는 gene-wise 2 rate $(\alpha_{co}, \alpha_{cc})$.
  - cell-wise chromatin state $k_j$ — MultiVelo는 gene별 single transition switch time $t_c$로 처리.
  - **m1 / m2 continuous score** (Eq. 32, 33): MultiVelo discrete M1/M2를 *cell fraction*으로 일반화.
  - **RNA-on / RNA-off continuous score** (Eq. 29, 30): MultiVelo discrete "on/off/complete"를 *cell fraction*으로 일반화.
  - **DAC score** (DAC$\alpha$, DAC$c$): cell type 간 parameter variance 정량 → LCHA, HCHA, LCLA, HCLA grouping (Fig. 5a).
  - **decoupling-sOff, decoupling-sOn, both-on, both-off** (Fig. 3c): cell-wise unspliced/spliced velocity sign에 따른 4 transcriptional state.
- **이 변화가 중요한 이유**:
  - cell-wise kinetic 덕분에 *같은 gene이 cell type별 다른 transcription rate*를 가지는 LCHA / HCHA pattern 식별 가능 (Padi3, Myo10 등 — Fig. 5d, 5e).
  - latent time 회피 덕분에 *gene-wise latent time over-correction*에 영향 받지 않고 *진짜 negative chromatin–RNA lag* 신호 보존 (PDGFRA, MAP3K1 — Fig. 3f, 3g).
  - DTW lag analysis로 *chromatin precede transcription* (positive lag) vs *RNA precede chromatin* (negative lag)을 cluster-level로 정량 → cluster 10의 "RNA-first" 발견 (Fig. 7), 이를 *nuclear export half-life + polycomb/speckle localization*으로 mechanistic 해석.
  - continuous m1/m2 score 덕분에 MultiVelo의 *discrete M1/M2 classification 결과를 본 paper에서 reproduce*하면서 *동시에 cell-level resolution*으로 확장 (Fig. 2f vs MultiVelo's classification).

### 이전 방법과의 차이

- **Baseline (Fig. 2, 4, 6 본문 비교)**: scVelo dynamical (ref. 7), cellDancer (ref. 11), MultiVelo (`@li2023multivelo`, ref. 12).
- **공통점**:
  - 3-ODE system $(c, u, s)$ Eq. 1–3는 MultiVelo와 동일.
  - WNN preprocessing (Seurat v4, ref. 45) MultiVelo와 동일.
  - peak-to-gene aggregation (promoter + linked distal enhancer) MultiVelo와 동일.
  - relay velocity cosine loss는 cellDancer (ref. 11)에서 차용.
  - scVelo suite (`tl.velocity_graph`, `tl.velocity_pseudotime`)로 downstream 분석.
- **차이점**:
  - **latent time 추정 없음** (vs scVelo, MultiVelo가 explicit).
  - **cell-wise kinetic parameter** $(\alpha_c, \alpha, \beta, \gamma)_j$ (vs MultiVelo의 gene-wise single set).
  - **chromatin state $k$의 dynamic best-fit selection** (vs MultiVelo의 gene-wise t_c switch time).
  - **2-stage 학습** (RNA → joint, vs MultiVelo의 EM, cellDancer의 single-stage).
  - **Mahalanobis neighbor in $(c, u, s)$** (vs cellDancer의 expression-only neighbor).
  - **continuous m1/m2, RNA-on/off score** (vs MultiVelo의 discrete state).
  - **DAC, DTW-based downstream analysis** — MoFlow가 propose한 *post hoc gene categorization* (HCHA, HCLA, LCHA, LCLA).
- **차이가 크게 나타나는 조건** (정량적 격차):
  - **10x embryonic mouse brain (E18)**: CBDir 격차 가장 큼 (MoFlow 0.535, MultiVelo 0.155, cellDancer 0.132, scVelo 0.273 — Supp Table 1). RG → IPC backflow가 MultiVelo에서 발생.
  - **Human brain cortex**: scVelo/cellDancer는 IPC/GluN1 → Cyc. Prog. backflow. MultiVelo는 GluN3 → GluN2 → GluN4/5 *linear* mis-imposition.
  - **Human HSPC**: MultiVelo의 *overly linear flow*가 natural bifurcation을 obscure.
  - **PDGFRA, MAP3K1 OPC marker**: gene-wise time fitting (MultiVelo)이 negative lag을 *over-correct*하는 사례 (Fig. 3f, g).

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**:
  - **Dataset 1** — Human brain cortex 10x Multiome (Trevino 2021, ref. 13, GSE162170; 4,693 cells × 842 genes; Fig. 2, 3).
  - **Dataset 2** — SHARE-seq mouse skin (Ma 2020, ref. 28, GSE140203; cell/gene 수 본문 `미제공:`; Fig. 4, 5).
  - **Dataset 3** — 10x embryonic mouse brain E18 (10x dataset page; cell/gene 수 본문 `미제공:`; Fig. 6, 7).
  - **Dataset 4** — 10x Human HSPC (`@li2023multivelo` 신규, ref. 12, GSE209878; cell/gene 수 본문 `미제공:`; Supp Fig. 5).
- **Metric**:
  - CBDir (cross-boundary direction correctness, Qiao 2021 ref. 8) — *primary quantitative metric* (Supp Table 1).
  - 정성 — velocity stream embedding (Fig. 2a, 4a, 6a, Supp Fig. 5b).
  - 정성 — gene velocity (MKI67, SDK2, PDGFRA, MAP3K1, Hephl1, Padi3, Myo10, Notch1, Trps1, Wnt3 — Fig. 2e, 3d, 4g, 5d).
  - 정량 — m1/m2 score across MultiVelo classification (2-sided t-test, p < 0.001 *** marker, Fig. 2f-j, 4f, Supp Fig. 4b).
  - 정량 — DAC score (Fig. 5a, Fig. 6g, Supp Fig. 3a, 3b, 4c-e).
  - 정량 — DTW lag distribution + sign quantile (Fig. 7b, c, Supp Fig. 2c, d).
  - 정량 — RNA half-life KS test (Fig. 7e, f), polycomb/speckle Fisher's exact (Fig. 7g).
  - 정성 — GSEA, GO BP enrichment (DAVID, GSEApy — Fig. 5b, 6f-g, 7f).
- **개선된 결과** (정량, Supp Table 1):
  - Human Brain: MoFlow **0.362**, MultiVelo 0.211, cellDancer −0.015, scVelo 0.211.
  - Mouse Skin: MoFlow **0.144**, MultiVelo 0.115, cellDancer 0.026, scVelo 0.005.
  - Mouse Brain: MoFlow **0.535**, MultiVelo 0.155, cellDancer 0.132, scVelo 0.273.
  - Human HSPC: MoFlow **0.191**, MultiVelo 0.063, cellDancer −0.056, scVelo −0.103.
  - 4개 dataset 평균 CBDir: MoFlow $\approx 0.308$, MultiVelo $\approx 0.136$, cellDancer $\approx 0.022$, scVelo $\approx 0.094$. `해석: 정확한 mean ± std 본문 없음, 본 분석자가 Supp Table 1 4개 값 단순평균.`
- **Ablation 근거**:
  - **MoFlow self-ablation 부재**: warm-up 없이 hard selection만, 또는 2-stage 없이 single-stage 같은 ablation은 *본문 부재*. `검토필요: 핵심 design choice (warm-up, 2-stage, Mahalanobis neighbor) 효과를 정량적으로 확인할 ablation이 본 paper에 없음. Reviewer가 요구하지 않은 듯.`
  - **chromatin head 제거**: 명시적으로 *RNA-only mode*를 본문에서 시연하지 않음 — cellDancer (RNA-only)와의 비교가 implicit ablation 역할.
  - **Threshold sensitivity** (Supp Fig. 6): m1/m2 percentile threshold (default 90th)에 대한 robustness 확인. Mouse Skin은 90% 이상에서만 significant (small Model 2 gene pool 때문) — *dataset 특이성* 시사.
- **정성적 효과**:
  - **Human brain**: scVelo/cellDancer는 IPC/GluN1(red) → Cyc. Prog.(blue) 또는 RG(orange) backflow, MultiVelo는 GluN3 → GluN2 → GluN4/5 linear mis-imposition. MoFlow만 GluN2와 GluN4/5의 *parallel independent paths*를 잡음 (Fig. 2a, e).
  - **Mouse skin Hephl1** (transcriptional boost): MoFlow가 cellDancer 대비 *명확한 hair-follicle-specific high transcription rate $\alpha \cdot c$* 회복 (Fig. 4g).
  - **Mouse skin Notch1, Trps1, Wnt3**: MoFlow가 MultiVelo와 동등하거나 우위 — Notch1은 MoFlow만 정확, Trps1·Wnt3은 두 method 모두 (Fig. 5d).
  - **E18 mouse brain DNA damage response gene** (Supp Fig. 4f, g, h): MoFlow는 Cyc. Prog. → RG 방향 정확 식별, MultiVelo는 *reversed*. MoFlow의 RG progenitor checkpoint function 발견 — radial glia DNA damage response (Qing 2023 ref. 42, Pilaz 2016 ref. 41).
  - **Cluster 10 (E18 mouse brain)**: $s$가 $c$보다 *먼저* 증가하는 unique pattern. Cdk12, Esf1, MALAT1, XIST이 해당. nuclear speckle / polycomb sequestered RNA의 conditional export (Fisher's exact p < 0.005 polycomb, p < 0.05 speckle — Fig. 7g).
  - **OPC lineage (human brain)**: PDGFRA, MAP3K1 negative $c\!-\!s$ lag이 MoFlow global pseudotime과 MultiVelo global latent time 양쪽 모두에서 보임. 그러나 MultiVelo *gene-specific latent time*에서는 *대부분 사라짐*. 이 over-correction이 129 gene에서 75% bin 이상 sign reversal로 정량화 (Supp Fig. 2c, d).
  - **OPC external validation** (Allen Brain Atlas adult brain scRNA, Hodge 2019 ref. 27): MoFlow의 decoupling-sOff 영역에 OPC 63% embedded vs 다른 영역 20% (Fig. 3h).

### Method 관점의 한계

- **약한 assumption**:
  - Cosine loss + Sigmoid output → *parameter scale [0, 1]*에 강제 — biology relevant absolute rate (예: chromatin opening rate in min$^{-1}$)와 직접 연결 안 됨. MultiVelo는 *interpretable rate constants*를 직접 출력.
  - chromatin → transcription 인과 (model 0 배제). nucleosome eviction during transcription 같은 reverse causation 표현 못함.
  - Single $c$ per gene (peak aggregation 후) → enhancer별 distinct kinetics 못 봄 — *MultiVelo, MultiVeloVAE 동일 한계*.
  - hard chromatin state $k \in \{0, 1\}$ selection — soft posterior $p(k=1 \mid x)$ 부재. boundary cell의 stability 문제 가능.
  - gene-wise independent inference → *gene network / co-regulation* 정보 미사용.
  - *deterministic point estimate* — confidence interval / Bayesian uncertainty 부재. MultiVeloVAE는 ELBO 기반 posterior 제공.
- **구현 / 학습상의 부담**:
  - DNN 두 개 × gene 수 만큼 학습 → gene scale-up 시 *computation O(G)*. 단 gene 간 parallel 가능.
  - hyperparameter (learning rate 0.001, weight decay 0.04, 3-layer FC (64, 48, 32), 20 epoch warm-up, max 200 epoch, n_neighbors 40, 90th percentile m1/m2 threshold)가 모두 default. `미제공: hyperparameter sensitivity analysis 본문 부재 — Supp Fig. 6에 threshold만.`
  - 2-stage training schedule이 dataset에 따라 *warm-up 길이*가 적절한지 검증 없음.
  - GPU 요구 사항 본문 미명시. `미제공: hardware (GPU model, VRAM), runtime, scaling 정보 부재. Reporting Summary에도 software/code reference만 있고 hardware 정보 부재.`
- **일반화가 불확실한 조건**:
  - **Multi-sample 통합 미지원**: MultiVeloVAE의 cVAE 같은 batch effect 처리 메커니즘 없음. 다른 donor / 다른 batch는 *별도 학습* 후 *post hoc 비교*만 가능.
  - **Mature / quiescent cell**: relay velocity 자체가 *transitioning cell* 가정 — non-differentiating cell에는 weak signal.
  - **Cell cycle confound**: 명시적 처리 없음. HSPC 같은 *cycling-heavy* dataset에서 cell cycle gene이 trajectory inference에 noise. `검토필요: MoFlow 본문에서 cell cycle regress-out 같은 explicit preprocessing 언급 부재 — MultiVelo와 달리 preprocessing은 reference dataset 그대로 사용.`
  - **Discrete sampling**: scRNA snapshot의 *time interval Δt*는 unknown — relay 가정의 정량적 정당화 어려움.
  - **Hypothesis testing 미지원**: cell type 간 driver gene을 *statistical*로 식별하는 framework 없음 — MultiVeloVAE의 Bayesian differential test 같은 기능 부재.
  - **In silico perturbation 미지원**: TF KO 시뮬레이션 같은 follow-up analysis 부재.

---

## Results

### Dataset별 결과

#### Dataset 1 — Human brain cortex 10x Multiome (Trevino 2021, GSE162170; Fig. 2, 3)

- **Dataset**: Trevino 2021 ref. 13의 preprocessed dataset (Li 2023 ref. 12의 처리 그대로 재사용). 4,693 cells × 842 genes. WNN smoothing 적용된 chromatin signal.
- **목적**: MoFlow의 기본 동작 검증 — known human cortex 발달 trajectory (Cyc. Prog. → RG → mGPC/OPC → nIPC/GluN1 → GluN2-5 → SP) 회복. MultiVelo의 *M1/M2 discrete classification*과의 continuous score 정합성 검증.
- **사용한 데이터 규모**: 4,693 cells, 842 velocity gene (본문 명시).
- **Baseline**: scVelo dynamical, cellDancer, MultiVelo.
- **Metric**: CBDir (Supp Table 1), 정성 velocity stream (Fig. 2a), pseudotime (Fig. 2b), G2/M score (Fig. 2c), gene velocity (Fig. 2e), m1/m2 score (Fig. 2f, g), RNA-on/off score across MultiVelo's "on/off/complete" (Fig. 2h, i, j).
- **주요 수치**:
  - CBDir: MoFlow **0.362**, MultiVelo 0.211, cellDancer −0.015, scVelo 0.211 (Fig. 2d, Supp Table 1).
  - MultiVelo Model 1 gene의 m1 score 평균 > Model 2 gene (Fig. 2f, p < 0.001 ***, 2-sided t-test).
  - MultiVelo Model 2 gene의 m2 score 평균 > Model 1 gene (Fig. 2g, p < 0.001 ***).
  - MultiVelo "off" state gene의 RNA-off score > "on" / "complete" state (Fig. 2h, p < 0.001 ***).
  - Model 2 gene의 RNA-off score > Model 1 gene (Fig. 2j, p < 0.001 ***).
- **정성 결과**:
  - scVelo / cellDancer는 IPC/GluN1(red) → Cyc. Prog.(blue) / RG(orange) backflow.
  - MultiVelo는 GluN3 → GluN2 → GluN4/5 linear mis-imposition — *neurodevelopment 알려진 사실과 불일치* (deep-layer가 먼저 발달, upper-layer가 나중 — Stepien 2021 ref. 15, Zhou 2024 ref. 16).
  - MoFlow는 GluN2 / GluN4/5 parallel independent paths를 정확 회복.
  - MKI67 (proliferation marker, G2/M phase, Uxa 2021 ref. 17): MultiVelo / scVelo가 RG → Cyc. Prog. 방향 *역으로* 예측. MoFlow는 정확 (Cyc. Prog. → RG 감소).
  - SDK2 (synaptic adhesion, Zhang 2023 ref. 18): cellDancer가 *역으로* (decreasing) 예측. MoFlow는 increasing.
  - CREB5 (RG → mGPC/OPC 증가, Kim 2024 ref. 19): cellDancer가 *역으로* (decreasing toward RG). MoFlow는 정확.
- **OPC lineage 분석 (Fig. 3)**:
  - 7 gene cluster 정의 (Fig. 3a). DAVID GO BP annotation (Huang 2007 ref. 20):
    - Cluster 0–1: cell division (p = 1.63e−15), mitotic cell cycle (p = 2.46e−6).
    - Cluster 2–3: positive regulation of cell migration (p = 0.038), actin filament organization (p = 0.008).
    - Cluster 4–6: nervous system development (p = 0.049), presynaptic modulation of chemical synaptic transmission (p = 0.051).
  - mGPC/OPC population: *heterogeneous mixture of states* (both-on, both-off, decoupling-sOff, decoupling-sOn — Fig. 3c).
  - PDGFRA (OPC marker, Marques 2018 ref. 23), MAP3K1 (MAPK/JNK signaling, Lorenzati 2021 ref. 24): vu ≥ 0 + vs < 0 (decoupling-sOff) sustained — *prolonged transcription* 후 transient chromatin burst (Fig. 3d).
  - DTW: PDGFRA, MAP3K1의 *negative c–s lag*이 MoFlow global pseudotime + MultiVelo global latent time 양쪽에 보임 (Fig. 3e, f). 그러나 MultiVelo *gene-specific latent time*에서는 *대부분 사라짐* (Fig. 3g).
  - 400+ gene이 25% 이상 bin에서 sign reversal, 129 gene이 75% 이상 (Supp Fig. 2c, d).
  - External validation (Allen Brain Atlas adult brain scRNA, Hodge 2019 ref. 27): MoFlow decoupling-sOff 영역에 OPC 63% embedded vs 다른 영역 20% (Fig. 3h).
- **논문 주장과의 연결**: ① MoFlow가 MultiVelo / scVelo / cellDancer가 못 보는 *parallel laminar development*를 잡고, ② continuous m1/m2 score가 *MultiVelo discrete classification을 reproduce하면서 cell-level resolution 추가*, ③ gene-specific latent time의 *over-correction*을 정량적으로 입증.

#### Dataset 2 — SHARE-seq mouse skin (Ma 2020, GSE140203; Fig. 4, 5)

- **Dataset**: Ma 2020 ref. 28의 preprocessed dataset (Li 2023 ref. 12 처리 재사용). cell/gene 수 본문 `미제공:`. TAC-1 (red) → TAC-2 (purple) → IRS (orange) / Medulla (green) / Hair Shaft-cuticle.cortex (blue).
- **목적**: MoFlow의 *transcriptional boost gene* (MURK, Multiple-rate kinetic genes, Barile 2021 ref. 30) 분해 능력 검증 + *DAC-based gene categorization* (HCHA, HCLA, LCHA, LCLA) 시연.
- **사용한 데이터 규모**: 본문 `미제공:` — `해석: ref. 28 + ref. 12 따라 약 5,000–6,500 cells 수준 추정. li-2023-multivelo는 6,436 cells × 962 genes로 명시.`
- **Baseline**: scVelo, cellDancer, MultiVelo.
- **Metric**: CBDir (Supp Table 1), 정성 velocity stream (Fig. 4a), G2/M score (Fig. 4b, c), RNA-on/off + m1/m2 score (Fig. 4d, f), Hephl1 velocity (Fig. 4g), DAC$\alpha$ / DAC$c$ scatter (Fig. 5a), GO enrichment for LCHA / HCHA / HCLA (Fig. 5b, Supp Fig. 3a-d).
- **주요 수치**:
  - CBDir: MoFlow **0.144**, MultiVelo 0.115, cellDancer 0.026, scVelo 0.005 (Supp Table 1).
  - MultiVelo의 induction 66.6% / Model 1 32.4% / Model 2 1.0% (Fig. 4e).
  - LCHA gene이 G2/M score correlation에서 가장 강함, LCLA는 가장 약함 (Fig. 5c, Mann–Whitney U test).
  - GO BP for LCHA (Fig. 5b): chromosome segregation (p = 0.0019), cell division (p = 0.0047), negative regulation of cell adhesion (p = 0.014), DNA repair, DNA replication checkpoint signaling, metaphase chromosome alignment, mitotic spindle organization.
- **정성 결과**:
  - TAC-1 root state 정확 식별 (G2/M score 가장 높음, Fig. 4b, c).
  - LCHA gene (chromatin 안정 + transcription 가변): Padi3 (medulla 분화, Vikhe Patil 2021 ref. 33), Myo10 (cell migration, Liakath-Ali 2019 ref. 34) — MoFlow가 정확 예측, MultiVelo 실패 (Supp Fig. 3e).
  - HCHA gene: Trps1 (MoFlow, MultiVelo 모두 정확), Notch1 (Vauclair 2005 ref. 35, MoFlow만 정확).
  - HCLA gene: Wnt3 (Millar 1999 ref. 36, MoFlow, MultiVelo 모두 정확).
  - cellDancer / scVelo: Trps1, Wnt3 방향 실패.
  - Hephl1 (hair follicle, Sharma 2019 ref. 31): MoFlow가 cellDancer 대비 *clear hair-shaft-specific high transcription rate $\alpha \cdot c$* 회복.
- **논문 주장과의 연결**: ① cell-specific kinetic으로 LCHA / HCHA 같은 *chromatin-α decoupling* gene group 식별, ② $\alpha \cdot c$ decomposition으로 *transcriptional boost*가 chromatin과 α 각각에서 얼마나 기여하는지 분리. MultiVelo의 *gene-wise single rate* 한계 극복.

#### Dataset 3 — 10x embryonic mouse brain E18 (Fig. 6, 7)

- **Dataset**: 10x Genomics 공개 dataset. cell/gene 수 본문 `미제공:`. Cyc. Prog. (blue) → RG (purple) → IPC (red) → ExM (green) → Subplate (brown) → UL (pink) / DL (orange).
- **목적**: ① MoFlow의 *DNA damage response gene* radial glia checkpoint 발견, ② *chromatin–RNA time lag*의 12-cluster mechanistic 해석.
- **사용한 데이터 규모**: 본문 `미제공:`. preprocessing은 Li 2023 ref. 12와 동일 strategy (velocyto → scanpy → scVelo → WNN smoothing for ATAC).
- **Baseline**: scVelo, cellDancer, MultiVelo.
- **Metric**: CBDir (Supp Table 1, Fig. 6d), 정성 velocity stream (Fig. 6a), pseudotime (Fig. 6b), G2/M score (Fig. 6c), 12 gene cluster (Fig. 6e), GO BP (Fig. 6f, DAVID), GSEA with DAC$\alpha$ + DAC$c$ (Fig. 6g, GSEApy), DTW c–s lag distribution (Fig. 7b, c), RNA half-life KS test (Fig. 7e, f), polycomb/speckle Fisher's exact (Fig. 7g).
- **주요 수치**:
  - CBDir: MoFlow **0.535**, MultiVelo 0.155, cellDancer 0.132, scVelo 0.273 (Supp Table 1). *4개 dataset 중 격차 최대*.
  - 12 cluster의 GO BP 분포 (Fig. 6f):
    - Cluster 0: cell division (p = 5.20e−42), chromosome segregation (p = 5.45e−31), DNA repair (p = 6.52e−15) — 가장 강한 enrichment.
    - Clusters 0–4: cell cycle, DNA repair, mitosis.
    - Clusters 4–7: neurodevelopment, axon development, cell migration.
    - Clusters 5–9, 11: synaptic functions.
    - Cluster 10: 미분류 (developmental pathway enrichment 미미).
  - GSEA for DAC$\alpha$ (Fig. 6g, cluster 0 gene): DNA Damage Response, DNA Metabolic Process, Negative Regulation of Cellular Process, Replication Fork Processing, DNA Repair, Metaphase Chromosome Alignment, Microtubule Cytoskeleton Organization, Mitotic Metaphase Chromosome Alignment, Mitotic Cytokinesis, Cytoskeleton-Dependent Cytokinesis. NES 양수.
  - DTW c–s lag (Fig. 7b, c): cluster 0–3, 10이 negative lag 비율 가장 높음. cluster 10이 특이 — $s$가 $c$보다 *먼저* 증가 (Fig. 7d Cdk12, Esf1).
  - RNA half-life (Ietswaart 2024 ref. 43, NIH3T3 cell): cluster 0, 3, 10 — *short nuclear half-life + long cytoplasmic + fast export* (one-sided KS test, p < 0.001 ***). cluster 1, 2 — *long nuclear half-life + short cytoplasmic + slow export* (p < 0.001 ***).
  - Polycomb / speckle gene (Khyzha 2025 ref. 44): cluster 10 *significantly enriched* (Fisher's exact, polycomb p < 0.005, speckle p < 0.05, Fig. 7g). MALAT1, XIST이 cluster 10에 포함.
- **정성 결과**:
  - scVelo / MultiVelo / cellDancer: IPC → RG / Cyc. Prog. backflow.
  - MoFlow: Cyc. Prog. → RG → IPC → ExM / Subplate → UL / DL의 정확 forward trajectory.
  - DNA damage response gene (Supp Fig. 4f, g): MoFlow Cyc. Prog. → RG 정확, MultiVelo *역방향*. MoFlow가 *RG progenitor의 transient DNA damage response activation* 발견 — checkpoint function 가설 (Pilaz 2016 ref. 41, Qing 2023 ref. 42).
  - Cluster 10 (e.g., Cdk12, Esf1, MALAT1, XIST): $s$ early accumulation before any rise in $c$ — *constitutively expressed, rapidly upregulated, conditional nuclear export* 가설.
- **논문 주장과의 연결**: ① MoFlow가 chromatin–RNA lag의 *negative sign 메커니즘*을 두 갈래 (rapid RNA turnover vs nuclear-sequestered conditional export)로 분리, ② DNA damage response gene의 cell type-specific α를 cell type-resolved로 식별 — MultiVelo는 *gene별 single α*라 불가능.

#### Dataset 4 — 10x Human HSPC (GSE209878; Supp Fig. 5)

- **Dataset**: `@li2023multivelo` (ref. 12)의 신규 10x Multiome HSPC. WNN preprocessing 재사용. cell/gene 수 본문 `미제공:`.
- **목적**: MoFlow의 hematopoietic 분화 hierarchy 회복 능력 + multi-method 비교.
- **사용한 데이터 규모**: 본문 `미제공:`. `해석: li-2023-multivelo는 11,605 cells × 1,000 genes로 명시.`
- **Baseline**: scVelo, cellDancer, MultiVelo.
- **Metric**: CBDir (Supp Table 1), 정성 velocity stream (Supp Fig. 5a, b).
- **주요 수치**:
  - CBDir: MoFlow **0.191**, MultiVelo 0.063, cellDancer −0.056, scVelo −0.103 (Supp Table 1).
- **정성 결과**:
  - HSC/MPP (orange/red)에서 erythroid (purple), myeloid (GMP/ProgDC; brown/turquoise), lymphoid (LMPP; green), megakaryocyte/platelet (MEP/Platelet; green/light yellow) 분기 정확 회복 (Supp Fig. 5a).
  - scVelo / cellDancer: ProgMK → HSC backflow.
  - MultiVelo: *overly linear flow*가 natural bifurcation을 obscure.
  - MoFlow: continuity + divergence 모두 회복 (단 "not always fully consistent across all branches" — 저자 명시 한계).
- **논문 주장과의 연결**: hematopoietic system에서도 다른 method 대비 정량 우위 — 단 *완전 무결한 결과 아님* 저자 자체 인정.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**:
  - 4개 dataset 모두에서 MoFlow CBDir 최상위.
  - chromatin-aware multi-method (MultiVelo) vs RNA-only (scVelo, cellDancer) vs MoFlow 비교에서, MoFlow가 *chromatin 사용 + cell-specific kinetic + latent time 없음* 조합의 시너지를 보임.
  - backflow artifact는 MoFlow에서 가장 줄어듦 — 4개 dataset 모두 (Fig. 2a, 4a, 6a, Supp Fig. 5b).
  - MultiVelo의 discrete M1/M2 / "on/off/complete" classification은 MoFlow의 continuous m1/m2 / RNA-on/off score와 *정합* (p < 0.001 *** 모든 비교).
  - chromatin–RNA lag의 *negative sign*이 두 dataset (human brain OPC, E18 mouse brain cluster 10)에서 *biologically meaningful*로 입증.
- **가장 중요한 수치**:
  - **Supp Table 1**: 4-dataset CBDir matrix — MoFlow가 모든 dataset에서 best (4/4).
  - E18 mouse brain CBDir 격차 (MoFlow 0.535 vs MultiVelo 0.155)가 가장 두드러짐.
  - 129 gene (75% 이상 bin에서 lag sign reversal) — MultiVelo gene-specific latent time over-correction의 정량.
  - Cluster 10 polycomb Fisher's exact p < 0.005 — conditional nuclear export 가설의 정량 근거.
- **baseline 대비 차이**:
  - vs **scVelo / cellDancer**: chromatin 정보 활용으로 +0.13 ~ +0.38 CBDir.
  - vs **MultiVelo**: cell-specific kinetic + latent-time-free relay 덕분에 +0.03 ~ +0.38 CBDir. *Cell-type-specific transcriptional regulation* (LCHA gene)을 jointly 잡음.
- **결과 해석 시 주의점**:
  - CBDir이 *single metric* — robust 평가에는 다른 metric (true time correlation, MSE, GCBDir from `@li2025multivelovae`) 미적용.
  - 정확 cell·gene 수가 4개 dataset 중 1개 (human brain)만 본문 명시 — 나머지는 `미제공:`.
  - Hyperparameter sensitivity ablation 부재 (warm-up length, neighbor count, learning rate).
  - 모든 결과가 *single random seed*로 추정 — variance 보고 없음.
  - MultiVelo (`@li2023multivelo`)의 *original publication*과 본 paper의 MultiVelo CBDir 수치가 같은 protocol·dataset에서 다를 가능성 — preprocessing parameter 차이 의심.
  - 신규 dataset 부재 — 4개 dataset 모두 *이전 publication에서 재사용*. `해석: MoFlow paper는 method 자체에 집중하고 신규 data 생산은 없음 — `@li2025multivelovae`는 신규 EB/HSPC/macrophage 3개 produce.`

---

## Figures

### Figure 1 — Overview of MoFlow

- **이 Figure가 필요한 이유**: ODE system, DNN architecture, downstream 분석을 *수식 전*에 통합 도식.
- **이 Figure가 뒷받침하는 주장**: chromatin accessibility + RNA를 *cell-specific kinetic* DNN으로 잡고 downstream을 standard scVelo suite로 연결한다는 framework-level 주장.

#### 패널별 설명

- **a — Conceptual model**: chromatin opening/closing이 transcription, splicing, degradation과 함께 시간 의존적 process로 modeled됨을 도식.
- **b — Architecture**: cell $i$의 $(c_i, u_i, s_i)$ 입력. 두 DNN ($\Phi_{\theta_c}$, $\Phi_{\theta_{us}}$)이 cell-specific kinetic $(\alpha_c, \alpha, \beta, \gamma)$를 추정. future neighbor selection (RNA velocity neighbor) + chromatin scenario 양쪽 (open / close) cosine similarity 평가 → lower-loss 채택.
- **c — Downstream**: velocity projection + velocity pseudotime (scVelo `tl.velocity_pseudotime`), gene-wise 분석 (transcriptional repression modes).

#### 본문에서 강조한 비교

- cellDancer (ref. 11)의 relay velocity design을 *MoFlow가 inherit하면서 chromatin 차원 추가*.
- MultiVelo (`@li2023multivelo`, ref. 12)의 ODE를 *cell-specific kinetic으로 일반화*.

#### 해석 시 주의점

- 도식은 *generative model 형태* — 그러나 실제로는 *discriminative cosine loss training* (Eq. 25)이라 도식과 mismatch.
- "downstream" 분석은 *MoFlow가 직접 제공하지 않고 scVelo 호환 출력*으로 사용자가 별도 호출.

### Figure 2 — MoFlow on developing human brain cortex

- **이 Figure가 필요한 이유**: MoFlow의 *primary benchmark* dataset에서 모든 baseline 대비 우위를 시각화 + MultiVelo M1/M2 classification과의 정합성 시연.
- **이 Figure가 뒷받침하는 주장**: ① biologically plausible trajectory 회복, ② backflow 회피, ③ MultiVelo의 discrete state를 *continuous score로 reproduce*.

#### 패널별 설명

- **a** — RNA velocity streamline, 4 method 비교 (MoFlow, scVelo, cellDancer, MultiVelo). MoFlow만 정확한 분기 회복.
- **b** — MoFlow pseudotime — Cyc. Prog. (낮음) → 분화 cell (높음).
- **c** — G2/M score UMAP — Cyc. Prog. 영역에서 가장 높음.
- **d** — CBDir box plot, 4 method 비교. MoFlow 0.362 vs MultiVelo 0.211 vs cellDancer −0.015 vs scVelo 0.211. boundaries = first/third quartile, whiskers 1.5× IQR, mean marker.
- **e** — gene velocity (MKI67, SDK2) 3-method (MoFlow, MultiVelo, cellDancer) 비교. u-s phase portrait.
- **f, g** — m1, m2 score box plot, MultiVelo Model 1 vs Model 2 gene. p < 0.001 ***. 2-sided t-test, 0.5× IQR whisker.
- **h, i** — RNA-on, RNA-off score, MultiVelo "on/off/complete" state 비교.
- **j** — RNA-off score, MultiVelo Model 1 vs Model 2.

#### 본문에서 강조한 비교

- p2–4의 본문 narrative: MoFlow가 *parallel laminar development* (deeper-layer vs upper-layer)를 정확 회복 vs MultiVelo의 linear mis-imposition (Stepien 2021 ref. 15, Zhou 2024 ref. 16 reference로).
- m1/m2 + RNA-on/off score는 MultiVelo의 discrete classification을 *continuous score로 일반화*하면서도 *정합성* 입증.

#### 해석 시 주의점

- CBDir bar plot의 mean marker가 *median이 아닌 mean* — outlier에 민감.
- 정확 sample size n_gene = 842 (본문), per-cluster gene 수는 본문 `미제공:`.
- p < 0.001 *** 외 정확 p-value 본문 부재 — Source Data 미공개 (Supp 3 humanbrain_cluster_GO에 GO만 있고 m1/m2 raw data 부재).

### Figure 3 — Transcriptional decoupling and asynchronous regulation in OPC lineage

- **이 Figure가 필요한 이유**: OPC lineage라는 *specific biological case*에서 MultiVelo의 *gene-specific latent time over-correction*을 정량적으로 입증.
- **이 Figure가 뒷받침하는 주장**: ① MoFlow가 cell-level RNA velocity state (both-on, both-off, decoupling-sOff, decoupling-sOn) heterogeneity를 잡고, ② negative c–s lag이 *real biological signal*이며 *MultiVelo gene-specific time이 artifact로 제거*한다는 주장.

#### 패널별 설명

- **a** — 7 gene cluster heatmap (gene × pseudotime). Cluster 0–1 (cell cycle) → 6 (synaptic).
- **b** — m2 score + RNA-off score box plot, 7 cluster 비교.
- **c** — 4 RNA velocity state UMAP (decoupling-sOff, decoupling-sOn, both-on, both-off). mGPC/OPC 영역에서 decoupling-sOff 우세.
- **d** — PDGFRA, MAP3K1 velocity streamline (MoFlow vs MultiVelo).
- **e** — Canonical case (positive Δt = c → s) vs Non-canonical case (negative Δt = s → c) 도식.
- **f** — DTW alignment along global time, MAP3K1 + PDGFRA, MoFlow pseudotime vs MultiVelo latent time. Norm value (c, u, s) + Time Lag (c-s, u-s) 시각화.
- **g** — DTW alignment along *MultiVelo gene-specific time*. 동일 gene에서 negative lag *사라짐*.
- **h** — Allen Brain Atlas adult brain scRNA projection. OPC-annotated cell이 decoupling-sOff 영역과 PDGFRA / MAP3K1 chromatin burst 영역에 정확 정렬.

#### 본문에서 강조한 비교

- p4–6 narrative: MultiVelo의 *per-gene time fitting이 trajectory를 expected biological order로 over-correct*해 *real asynchronous regulation을 detect 못 함*.
- Allen Brain Atlas projection (Hodge 2019 ref. 27)이 *외부 dataset external validation* 역할.

#### 해석 시 주의점

- DTW 결과는 *binning + smoothing* (default 20 bin, 3-bin window) 의존 — bin 수에 따라 lag sign이 변할 수 있음.
- "129 gene이 75% 이상 bin에서 sign reversal" 정량은 Supp Fig. 2c, d에 시각화이나 *gene list는 Source Data 미공개*. `검토필요: 129 reversal gene의 functional annotation 본문 부재 — 추가 sanity check 어려움.`
- min-max normalization이 *low-level chromatin variance를 obscure*할 가능성 — 저자 자체 명시.

### Figure 4 — Transcriptional boosts and cell-cycle-linked dynamics in hair follicle (SHARE-seq mouse skin)

- **이 Figure가 필요한 이유**: MoFlow의 *transcriptional boost gene* (MURK, ref. 30) 분해 능력 + MultiVelo의 induction/repression class와의 정합성 시연.
- **이 Figure가 뒷받침하는 주장**: cellular kinetic을 *chromatin과 α로 분해*해 cellDancer (ref. 11)가 못 본 chromatin-aware transcription boost를 잡는다.

#### 패널별 설명

- **a** — 4 method velocity streamline.
- **b** — G2/M score UMAP. TAC-1이 가장 높음.
- **c** — G2/M score box plot, 5 cell type. TAC-1 root state.
- **d** — RNA-on/off + m1/m2 score 분포 (MoFlow).
- **e** — MultiVelo gene classification pie chart: induction-only 66.6%, Model 2 1.0%, Model 1 32.4%.
- **f** — m1, m2 score, MultiVelo Model 1 vs Model 2 비교. p < 0.001 ***.
- **g** — Hephl1 velocity (MoFlow, cellDancer, MultiVelo, scVelo). MoFlow + cellDancer은 transcription rate ($\alpha \cdot c$ for MoFlow, $\alpha$ for cellDancer) violin plot. MoFlow는 *hair-shaft cuticle / cortex에서 명확 high boost*.

#### 본문에서 강조한 비교

- Hephl1 (ref. 31): MoFlow가 cellDancer 대비 chromatin-aware 분해로 *cell-type-specific transcription boost*를 명확화.
- p7 본문: "Although MURK genes have not been systematically studied in skin, the widespread presence of induction kinetics suggests the possibility of similar amplification mechanisms."

#### 해석 시 주의점

- MURK / transcriptional boost는 *Bergen 2021 review*에서 명명 — `@li2023multivelo` §S5에서도 한계로 언급. 본 paper는 이를 explicit하게 해결했다 주장하나 *quantitative validation* (예: ground-truth time-series ChIP-seq + RNA-seq)은 부재.
- pie chart의 정확 gene 수 본문 `미제공:`.

### Figure 5 — Decoupling of transcription rate and chromatin accessibility (DAC-based grouping, mouse skin)

- **이 Figure가 필요한 이유**: MoFlow의 *DAC score* 기반 4-gene group (HCHA, HCLA, LCHA, LCLA) framework 시연.
- **이 Figure가 뒷받침하는 주장**: cell-specific α + chromatin 분리 추정 덕분에 *chromatin priming without transcription* (HCLA) vs *transcription flexibility without chromatin change* (LCHA) 같은 *4 quadrant* 분석 가능.

#### 패널별 설명

- **a** — DAC$\alpha$ × DAC$c$ scatter, threshold 0.05로 4 group 분할.
- **b** — LCHA group GO BP enrichment (DAVID): chromosome segregation, cell division, DNA repair, mitotic spindle organization 등.
- **c** — 4 group의 G2/M score correlation comparison. LCHA 가장 강함, LCLA 가장 약함. 2-sided t-test, 0.5× IQR whisker.
- **d** — Padi3, Myo10, Notch1, Trps1, Wnt3 velocity (MoFlow). 모두 정확 방향.
- **e** — 동일 gene의 c, α distribution UMAP, cell-type-specific.

#### 본문에서 강조한 비교

- p7–8: HCHA가 active differentiation (keratinocyte fate, hair follicle development), HCLA가 structural / ion transport, LCHA가 chromosome segregation / spindle organization (cell-cycle linked transcription flexibility), LCLA가 quiescent transcriptional + epigenetic 상태.
- MultiVelo (`@li2023multivelo`)는 *gene-wise single α*라 *cell-type-specific transcription variability* (LCHA가 의미하는 것) 식별 *불가*.

#### 해석 시 주의점

- threshold 0.05는 *ad hoc* — sensitivity analysis 부재.
- DAC score 자체가 *cell type 간 mean variance* — *cell type annotation 품질에 의존*. annotation 부정확하면 LCHA / HCHA grouping도 부정확.
- Supp Fig. 3e의 cellDancer / MultiVelo / scVelo도 함께 비교되었다고 본문에 있으나 panel 자체 본문 미캡션. `검토필요: Supp Fig. 3e 본문 description 확인 필요.`

### Figure 6 — Transcriptional dynamics and regulatory heterogeneity in developing mouse brain (E18)

- **이 Figure가 필요한 이유**: MoFlow의 *backflow 해소 + DNA damage response gene cell-type-specific α* 능력 시연 — 본 paper의 *novel biological discovery*.
- **이 Figure가 뒷받침하는 주장**: ① CBDir 격차 가장 큰 dataset (0.535 vs 0.155), ② radial glia checkpoint function (DNA damage response activation) 발견.

#### 패널별 설명

- **a** — 4 method velocity streamline. MoFlow만 Cyc. Prog. → RG → IPC → UL/DL 정확 forward, 다른 방법 backflow.
- **b** — MoFlow pseudotime.
- **c** — G2/M score UMAP.
- **d** — CBDir box plot, 4 method. MoFlow 0.535 격차 최대.
- **e** — 12 gene cluster heatmap (gene × pseudotime).
- **f** — DAVID GO BP dot plot. cluster 0 = DNA repair, mitosis, cell division (가장 강함). cluster 4–11 progression to synaptic.
- **g** — GSEA with DAC$\alpha$ for cluster 0 gene. DNA damage response 양수 NES, mitotic terms negative NES.

#### 본문에서 강조한 비교

- p7–10: MoFlow의 forward trajectory가 RG → ExM → UL/DL 알려진 발달 hierarchy (Zhu 2023 ref. 37, Gleeson 1999 ref. 38, Poirier 2010 ref. 39)와 일치.
- UniTVelo (ref. 40)의 transition coherence 개선 metric도 본문 언급 (그러나 명시 수치 부재).
- DNA damage response는 RG transient checkpoint (Pilaz 2016 ref. 41, Qing 2023 ref. 42)와 일치.

#### 해석 시 주의점

- 12 cluster choice (K=12)의 sensitivity 부재.
- DAC$c$ enrichment는 *weaker + less specific* — 저자 자체 언급. *transcriptional bursts may drive acute responses to developmental stress*라는 *해석*은 chromatin-vs-α evidence asymmetry가 만들어내는 가설.

### Figure 7 — Time lag between chromatin accessibility and spliced RNA (mouse brain E18)

- **이 Figure가 필요한 이유**: MoFlow의 chromatin–RNA time lag 정량 + *mechanistic explanation* (RNA half-life + nuclear localization)으로 *negative lag의 biological meaning* 입증.
- **이 Figure가 뒷받침하는 주장**: chromatin과 transcription의 *temporal coordination*이 *두 가지 mechanism* (rapid RNA turnover vs nuclear-compartment-sequestered conditional export)으로 다양화된다.

#### 패널별 설명

- **a** — 12 cluster의 mean c, s profile (gene × pseudotime). cluster 10이 *s가 먼저 accumulation*하는 unique pattern.
- **b** — DTW quantile (q0, q25, q50, q75, q100) of c–s lag across pseudotime. median은 negative.
- **c** — gene proportion with negative c–s lag per cluster (heatmap, 12 cluster × 1 dimension).
- **d** — DTW alignment example genes (Ccnd2, Mki67, Cdk12, Esf1). Norm value (c, u, s) + Time Lag (c-s, u-s).
- **e** — one-sided KS test of RNA half-life vs background. 4 row (nuclear, cytoplasmic, nuclear export, nuclear degradation) × 12 cluster. p < 0.001 ***, p < 0.005 **, p < 0.05 *.
- **f** — nuclear half-life + cytoplasm half-life + nuclear export half-life + nuclear degradation half-life box plot, cluster 0, 1, 2, 3, 10 vs other.
- **g** — polycomb / nuclear speckle gene set Fisher's exact test. cluster 10이 *significantly enriched* (polycomb p < 0.005, speckle p < 0.05).

#### 본문에서 강조한 비교

- p10–11: cluster 0, 3, 10 — short nuclear half-life + fast export (rapid RNA turnover). cluster 1, 2 — long nuclear half-life + slow export (delayed chromatin shutdown).
- cluster 10 (Cdk12, Esf1, MALAT1, XIST): polycomb / speckle sequestered RNA의 conditional export — 이는 *nuclear-retained noncoding RNA의 stimulus-responsive release* 메커니즘 (Khyzha 2025 ref. 44).
- 외부 reference: Ietswaart 2024 ref. 43 (NIH3T3 RNA flow), Khyzha 2025 ref. 44 (polycomb/speckle RNA).

#### 해석 시 주의점

- RNA half-life는 *NIH3T3 fibroblast cell line* — *in vivo developing brain*과 직접 비교 불가. 저자 자체 명시: "nuclear localization and kinetic measurements derived from in vitro cell lines may not fully reflect the in vivo dynamics of developing brain tissue."
- 10x Multiome은 *nuclear RNA*를 capture — total RNA가 아니라 *apparent degradation*은 nuclear export 효과일 수 있음. 저자 자체 명시.
- min-max normalization이 *low-level chromatin variance를 obscure*할 가능성. 저자 자체 명시.
- MALAT1, XIST는 *noncoding RNA*로 *half-life estimation에서 excluded*. cluster 10 결론을 "noncoding RNA만의 특수 case일 수 있다"고 약화시키는 caveat 부재.
- 16 cluster × 4 half-life × 2 tail KS test = 128 test → *multiple comparison correction 부재*. `검토필요: 본문 method에 BH correction 언급 없음.`

### Supplementary Figures (요약)

- **Supp Fig. 1** (human brain): 3D phase portrait (c-u-s) for MKI67, BCL11B, CREB5, SDK2, RFX4 — 4 method 비교. 2D c-u, u-s projection도 동일 비교.
- **Supp Fig. 2** (OPC time lag): m1 score / RNA-on score per cluster, 129 gene reversal heatmap, PDGFRA + MAP3K1 chromatin UMAP. 본문 Fig. 3의 quantitative back-up.
- **Supp Fig. 3** (DAC group): GSEA dot plot for DAC$\alpha$ and DAC$c$, HCHA + HCLA GO annotation, cellDancer/MultiVelo/scVelo gene velocity (Padi3, Myo10, Notch1, Trps1, Wnt3). 본문 Fig. 5의 baseline comparison.
- **Supp Fig. 4** (mouse brain): cell type marker dot plot, MultiVelo classification distribution, GSEA, DNA damage response gene velocity (MoFlow vs MultiVelo), DNA damage response gene α distribution.
- **Supp Fig. 5** (HSPC): velocity streamline 4-method, CBDir.
- **Supp Fig. 6** (m1/m2 threshold sensitivity): m1, m2 score percentile threshold 0–95th에서 Model 1 vs Model 2 significance test. Mouse Brain, Human HSPC는 45–70th에서 significant. Mouse Skin은 90th 이상에서만 — Mouse Skin의 작은 Model 2 gene pool 때문.

---

## Tables

본문에 정식 Table 없음. *모든 정량 결과는 Figure의 box plot 또는 Source Data file*에 의존.

Supplementary Table은 1개 — Supp Table 1 (CBDir 4 dataset × 4 method matrix).

### Supplementary Table 1 — CBDir across datasets

| Dataset | MoFlow | MultiVelo | cellDancer | scVelo |
|---|---|---|---|---|
| Human Brain | **0.362** | 0.211 | −0.015 | 0.211 |
| Mouse Skin | **0.144** | 0.115 | 0.026 | 0.005 |
| Mouse Brain | **0.535** | 0.155 | 0.132 | 0.273 |
| Human HSPC | **0.191** | 0.063 | −0.056 | −0.103 |

- 4-dataset 평균 (단순평균): MoFlow $\approx 0.308$, MultiVelo $\approx 0.136$, cellDancer $\approx 0.022$, scVelo $\approx 0.094$. `해석: 본문에 mean ± std 미명시 — 본 분석자의 단순평균.`
- 본문 caption (Supp Table 1): "MoFlow consistently achieves the highest directional accuracy. In particular, MoFlow showed markedly improved performance in the mouse brain dataset (CBDIR = 0.535), where alternative methods exhibited substantially lower directional accuracy."

---

## Supplementary Information

### Supp-1 — Supplementary Table + Supplementary Figure (8 page PDF)

- **Supp Table 1** (위 §Tables 참조): 4-dataset × 4-method CBDir matrix.
- **Supp Fig. 1–6**: 위 §Figures의 Supplementary Figures 항목 참조.

### Supp-2 — Description of Additional Supplementary Files (1 page PDF)

- *Index 역할*. Supp Data 1–3 (xlsx 3개)의 내용 1 줄씩 description.

### Supp-3 — Supplementary Data 1 (xlsx, sheet `humanbrain_cluster_GO`)

- Functional annotation of gene clusters in human brain dataset using DAVID.
- 86 rows × 14 columns.
- Column: Category, Term, Count, %, PValue, Genes, List Total, Pop Hits, Pop Total, Fold Enrichment.
- 핵심 항목 (top 5):
  - GO:0051301 cell division, count 15 (50%), p = 1.63e−15, 15 genes incl UBE2C, KIF14, KIF11, KNL1, SMC4, CDC20, ASPM, CENPE, CCNB2, TPX2, CENPF, CCNB1, KIF18B, PTTG1, NUF2.
  - GO:0007059 chromosome segregation, count 6 (20%), p = 2.46e−6, genes TOP2A, CENPE, CENPF, DIAPH3, NUF2, MKI67.
  - GO:0000278 mitotic cell cycle, count 6 (20%), p = 2.46e−6, genes CENPE, TPX2, CENPF, KIF18B, KIF11, CIT.

### Supp-4 — Supplementary Data 2 (xlsx, 5 sheets — mouse skin)

- GSEA using DAC scores and functional annotation of categorized genes in mouse skin dataset.
- Sheets:
  - `DAC_alpha_gsea` (104 rows × 10 cols, prerank GSEA on DAC$\alpha$): top — Double-Strand Break Repair via Homologous Recombination (NES 1.673, p = 0.0085), Intracellular Signaling Cassette (NES 1.668, p = 0.002), Double-Strand Break Repair (NES 1.615, p = 0.0073). Lead genes for DSB HR: TOPBP1, RBBP8, RAD54B, SMC5, BRCA1, BLM, BRCA2, MCM3, ZMYND8, HELQ.
  - `DAC_c_gsea` (103 rows × 10 cols, GSEA on DAC$c$): top — Intermediate Filament Organization (NES 1.756, p = 0.003), Epithelium Development (NES 1.690, p = 0.0041), Regulation of Cell Migration (NES 1.652, p = 0.001), Axon Guidance (NES 1.629, p = 0.0072). Lead genes for Intermediate Filament: KRT71, KRT28, KRT25, KRT17, KRT35, KRT27, KRT73, KRT75, KRT14 (keratin family).
  - `hcha_GO` (35 rows × 13 cols, DAVID GO BP for HCHA group): top — neuron fate commitment (5 genes, p = 0.0003, NOTCH3, SHH, NOTCH1, GLI3, RUNX1), embryonic limb morphogenesis (p = 0.0056), hair follicle development (5 genes incl SHH, TRPS1, TNFRSF19, LRP4, DSG4, p = 0.0127).
  - `hcla_GO` (9 rows × 13 cols, HCLA group): top — intracellular calcium ion homeostasis (4 genes, p = 0.0121), axon guidance (6 genes, p = 0.0367), epithelial cell differentiation (4 keratin genes, p = 0.0486).
  - `lcha_GO` (29 rows × 13 cols, LCHA group): top — chromosome segregation (6 genes incl CENPE, CENPF, INCENP, CENPC1, SMC5, BRCA1, p = 0.0019), cell division (9 genes, p = 0.0047), negative regulation of cell adhesion (p = 0.0140), cell adhesion (11 genes, p = 0.0153). LCHA gene이 *cell-cycle linked transcriptional regulation* 함의 — 본문 Fig. 5b의 dot plot과 정합.

### Supp-5 — Supplementary Data 3 (xlsx, sheet `mousebrain_cluster_GO`)

- Functional annotation of gene clusters in mouse brain dataset using DAVID.
- 122 rows × 15 columns.
- 핵심 항목 (cluster 0):
  - GO:0051301 cell division, count 61 (25.8%), p = 5.20e−42 — 60+ gene cell-cycle 강력 enriched.
  - GO:0007059 chromosome segregation, count 33 (14.0%), p = 5.45e−31.
  - GO:0006281 DNA repair, count 28 (11.9%), p = 6.52e−15 — DNA damage response 가설의 정량 근거.

### Supp-6 — Reporting Summary (1 page Nature Portfolio template)

- Statistics: 모든 항목 confirmed.
- Software and code: GitHub https://github.com/AriHong/MoFlow + Demo notebooks.
- Data: 모든 dataset public — 10x Multiome E18 mouse brain (10x Genomics), human brain multi-ome (GSE162170), SHARE-seq mouse skin (GSE140203), 10x Human HSPC (GSE209878).
- Human participants: 본 paper는 *secondary data analysis* — primary recruitment 없음. ethics oversight 없음 (publicly available data only).
- Hardware: `미제공:` — Reporting Summary에 hardware (GPU model, RAM) 정보 부재.

---

## 분석 자체에 대한 메모

- **MoFlow가 MultiVeloVAE보다 *2개월 늦게* publish됨** (MultiVeloVAE Nov 20, 2025 vs MoFlow Dec 29, 2025). 같은 *post-MultiVelo* timeframe인데 본문에서 *MultiVeloVAE 인용 부재*. MoFlow 제출 시점 (Received 2025-06-20)에는 MultiVeloVAE preprint도 not yet — `해석: 두 method 모두 동시에 *MultiVelo의 한계를 다른 각도에서* 풀려고 한 작업으로 보임. Discussion에서 reciprocal acknowledgement 없는 것은 자연스러움 (review cycle).`
- **CBDir 단일 metric 의존**: `@li2025multivelovae`는 GCBDir (k-step + random-walk null) + true time correlation + Mann–Whitney U + MSE/MAE까지 4가지 metric. MoFlow는 *CBDir 1개*에 집중. *robust benchmark*로는 제한적.
- **신규 dataset 없음**: 4개 dataset 모두 *이전 publication 재사용*. `해석: MoFlow paper의 contribution은 *method 자체*에 집중 — MultiVeloVAE처럼 신규 EB/HSPC/macrophage dataset 공개는 없음. 우리가 우리 HSPC data에 적용할 때 *MoFlow는 외부 data 의존*이라 추가 검증 자료 만들기 어려움.`
- **Cross-method comparison 누락**: `@li2025multivelovae`의 GCBDir / 4-axis benchmark가 본 paper에 적용된 결과 부재 — *direct head-to-head*는 우리가 직접 수행해야.
- **Ablation 부재**: warm-up length, 2-stage 학습, Mahalanobis vs Euclidean neighbor, hard vs soft k selection 등 *core design choice* ablation 모두 부재. *reviewer 요구 없었던 듯*.
- **Pre-trained model / atlas-level pretraining 부재**: `@li2025multivelovae`도 한계로 명시한 영역. MoFlow도 동일 한계 — 매 dataset *de novo training*. `질문: MoFlow + atlas (예: Human Cell Atlas HSPC) pretraining이 가능한가?`
- **GPU 사양 / runtime 정보 완전 부재**: MultiVeloVAE는 RTX 3060 12 GB + 64 GB RAM 명시 + runtime 직접 측정. MoFlow는 *Reporting Summary에도* 부재. 우리 환경 재현 계획 시 *추가 정보 필요*.
- **분석 시점 cross-reference**: `@li2023multivelo` (li-2023-multivelo_core.md) Methods §"Post-fitting analyses" + `@li2025multivelovae` (li-2025-multivelovae_core.md) Methods §"GCBDir computation"이 본 paper의 *동일 base dataset (Human brain, Mouse skin, HSPC)*에 대해 *다른 metric으로 평가한 결과*가 풍부 — head-to-head benchmark에 활용 가능.
- **검토 우선순위 1**: 본 paper의 Fig. 3f/g (PDGFRA, MAP3K1의 MultiVelo gene-specific time over-correction)가 정말로 *over-correction*인지 아니면 *MultiVelo가 정확한 biological order 회복*인지 — 두 해석 모두 가능. 외부 DTW + bulk time-series chromatin-RNA paired data 필요.
- **검토 우선순위 2**: 본 paper의 Cluster 10 cluster (cdk12, Esf1, MALAT1, XIST)의 polycomb/speckle hypothesis — *MoFlow가 발견*한 것인지 *Khyzha 2025 (ref. 44)의 기존 발견을 MoFlow로 confirm*한 것인지. Discussion에서 *후자*에 가까움.
