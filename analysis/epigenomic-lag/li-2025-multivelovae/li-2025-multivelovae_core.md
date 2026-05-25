# Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE

Citation: `@li2025multivelovae` — Li C*, Gu Y*, Virgilio MC, Lee KH, Collins KL, Welch JD. *Nat Commun* 16(1):11505 (2025). DOI: 10.1038/s41467-025-66287-6. PMCID: PMC12748740. (*equal contribution)

> 본 분석은 `sources/li-2025-multivelovae.pdf` (24 page Nature Communications open access PDF) + `sources/abstract.txt` (PubMed) 만을 근거로 한다. Supplementary Note·Supplementary Figures (1~22) 본문은 다운로드되지 않아 일부 항목은 `미제공:`으로 표시한다. 외부 지식은 `외부 맥락:` 등 prefix로 분리한다.

---

## Executive Summary

MultiVeloVAE는 선행 자가 method `@li2023multivelo` (MultiVelo)의 *discrete 4 state + binary chromatin opening rate*를 *continuous, cell-specific* coupling factor κ와 decoupling factor δ로 일반화하고, 여기에 *multi-sample conditional VAE + 모든 gene에 공통된 shared latent time + 부분적으로 겹치는 modality (multi-omic + scRNA-only)*  지원 + *Bayesian differential dynamics test*를 추가한 multi-omic RNA velocity framework다 (Methods §"Problem setup"–"Differential dynamics testing", Results §"MultiVeloVAE infers cell times..."–§"MultiVeloVAE identifies genes with differential dynamics..."). 핵심 모델은 chromatin accessibility c, unspliced u, spliced s를 입력받아 cell time t와 cell state z, 그리고 cell-gene별 chromatin opening rate k_c와 transcription rate ρ를 posterior로 추정하는 conditional autoencoding variational Bayes로, 학습은 ELBO 최대화로 수행한다 (Eq. 4–8). 핵심 결과는 ① RNA-only mode에서 scVelo / UniTVelo / DeepVelo / VeloVI / PyroVelocity / cellDancer 6개 baseline 대비 10개 scRNA-seq dataset에서 latent time correlation·GCBDir·Mann–Whitney U 모두에서 우위 (Fig. 2f), ② 신규 생성한 7-day human embryoid body (EB) 10x Multiome dataset에서 NANOG+ root cell + 3 germ layer trajectory 정확 회복 (Fig. 3a), ③ 두 HSPC 10x Multiome batch를 conditional VAE로 정렬해 scVI·Scanorama 대비 biological conservation metric에서 우위 (Fig. 4d-e), ④ 신규 macrophage differentiation dataset에서 Bayes factor + Gaussian process 기반 differential dynamics test로 macrophage vs DC 분기 driver gene을 통계적으로 식별 (Fig. 6), ⑤ scRNA-only sample에 chromatin in silico imputation 후 SPI1 / GATA1 knockout in silico perturbation까지 가능 (Fig. 7). 우리 HSPC multiome pipeline에서 MultiVelo를 *직접 대체 또는 보완*할 강력한 candidate이며, GPU 가속이 추가되어 MultiVelo 대비 runtime 단축 효과까지 있다 (Fig. 3h). 자세한 한계·재현 ROI는 `li-2025-multivelovae_lens-academic.md`, `li-2025-multivelovae_lens-industry.md` 참고.

---

## Identity

- **Title**: Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE
- **Authors**: Chen Li*, Yichen Gu*, Maria C. Virgilio, Kun H. Lee, Kathleen L. Collins, Joshua D. Welch (corresponding, welchjd@umich.edu). (*equal contribution; C.L. and Y.G.).
- **Affiliation**: University of Michigan (Computational Medicine & Bioinformatics; Electrical and Computer Engineering; CMB Program; Microbiology & Immunology; Internal Medicine; Computer Science & Engineering).
- **Venue / Year**: *Nature Communications* 16(1):11505 (2025). Received 2025-02-18, Accepted 2025-10-31, online 2025-11-20.
- **Funding**: NIH R01AI149669 (K.L.C., J.D.W.), R01HG010883, UM1MH130966 (J.D.W.), F31AI177258 (C.L.), F31AI15504 (M.C.V.). University of Michigan Flow Cytometry / Advanced Genomics Core 지원 (Acknowledgements).
- **COI**: 저자 명시 — "no competing interests" (Competing interests).
- **License**: CC BY-NC-ND 4.0 (Open Access). Code는 BSD-3-Clause (GitHub welch-lab/MultiVeloVAE, PyPI, Zenodo archive DOI 10.5281/zenodo.17268254).
- **Data availability**: 신규 GEO **GSE284047** (10x Multiome HSPC + macrophage + EB processed). Raw FASTQ는 dbGaP **phs002915.v2.p1** restricted access. Post-processed AnnData는 figshare DOI 10.6084/m9.figshare.30280333.
- **Predecessor**: `@li2023multivelo` (MultiVelo, Nat Biotechnol 2023) — discrete 4 state ODE model. MultiVeloVAE는 이를 continuous + multi-sample + differential testing으로 확장. VeloVAE (Gu, Blaauw, Welch — ICML 2022, ref. 57)도 직접 predecessor.

---

## Background

### 배경 스토리

- **문제의 출발점**: single-cell sequencing은 cell을 *파괴*하기 때문에 longitudinal 관찰 불가. computational method가 cell snapshot을 *trajectory*로 재구성해야 한다 (§Introduction p1).
- **선행 접근 A — Pseudotime inference** (Trapnell 2014, diffusion pseudotime, SLICER; refs 1–3): scRNA snapshot으로 cell을 ordering하지만 *starting cell state*를 사전 지정해야 함.
- **A의 한계**: similarity 기반 ordering → *전이 방향·속도* 직접 추정 불가, root cell 지정 필요.
- **선행 접근 B — RNA velocity 1세대** (La Manno 2018 ref. 4; scVelo dynamical model — Bergen 2020 ref. 5): unspliced u / spliced s의 mechanistic ODE를 fit. scVelo는 *latent time*도 동시 추정 → root cell 사전 지정 불필요.
- **B의 한계 (저자 명시, §Introduction p2)**: ① *gene별로 latent time이 따로* 추정되어 gene 간 일관성 부족, ② gene expression이 *discrete on/off state*로 모델링됨, ③ *single cell type* 가정으로 lineage bifurcation 무시.
- **선행 접근 C — RNA velocity 2세대** (UniTVelo ref. 10, DeepVelo ref. 11, cellDancer ref. 12, VeloVI ref. 13, PyroVelocity ref. 14): UniTVelo는 *shared time scale + flexible parametric*; DeepVelo·cellDancer는 *cell-specific rate*; VeloVI·PyroVelocity는 Bayesian.
- **C의 한계 (저자 명시, §Introduction p2)**: UniTVelo는 multi cell type modeling 안 됨 + biochemical interpretability 약함; DeepVelo·cellDancer는 *post hoc* cell time inference (model 학습 후 별도 ordering)이라 inferred time과 velocity 사이 inconsistency 발생.
- **선행 접근 D — Multi-omic single-cell velocity** (MultiVelo `@li2023multivelo` ref. 9): chromatin accessibility c를 ODE에 추가, *priming / coupled-on / decoupled / coupled-off* 4 state로 cell-gene 분류. M1 / M2 두 model class.
- **D의 한계 (저자 명시, §Results "MultiVeloVAE improves velocity inference..." p4-5)**: ① 모든 cell에 *single set of ODE parameters* — cell-specific differential dynamics 불가, ② cell이 *discrete 4 state*에 강제 할당 — continuous gradient 무시, ③ multiple cell type emerging 동시 발생 *단일 lineage 가정* — multi-lineage bifurcation 모델링 안 됨.
- **선행 접근 E — Multi-sample / multi-omic integration** (Seurat ref. 15, LIGER ref. 16, scVI ref. 17, Harmony ref. 37, Scanorama ref. 38): batch effect 보정·dataset 통합은 가능하나 *RNA velocity inference 자체*에는 미지원. velocity inference 후 통합 또는 통합 후 velocity inference로 *post hoc chaining*해야 하는데 이는 error 누적 + hypothesis test 불가.
- **이 논문으로 이어지는 gap**: chromatin–RNA coupling을 ① *cell-specific continuous*로 모델링하고, ② *multi-sample / partially-overlapping modality* (multi-omic + RNA-only)에서 jointly 추정하며, ③ *cell type / lineage / time 간 차이*를 *statistically* test할 수 있는 unified framework 필요.

### 기본 개념

- **유전자 발현 흐름** (Methods Eq. 4): `dc/dt = k_c α_c − α_c c` (chromatin), `du/dt = ρ α c − β u` (transcription), `ds/dt = β u − γ s` (splicing). 본 논문은 k_c와 ρ를 각각 *cell-specific [0,1] continuous variable*로 일반화. MultiVelo는 k_c, ρ를 binary indicator로 가정한 것에 비해 *flexible*.
- **RNA velocity (scVelo dynamical)**: `du/dt = α^(k) − βu`, `ds/dt = βu − γs`. transcription rate가 induction(k=1) / repression(k=0) phase 내내 상수.
- **VeloVAE** (Gu 2022, ref. 57): cell-specific *real-valued* relative transcription rate ρ ∈ [0,1]를 명시 추정. MultiVeloVAE의 직접 predecessor 중 하나.
- **VAE / Conditional VAE**: autoencoder 구조의 latent z, t를 posterior로 estimate. cVAE는 sample label b를 conditioning variable로 추가해 latent space에서 batch effect 분리 (ref. 17 scVI 동일 전략).
- **Coupling factor κ, Decoupling factor δ** (Methods Eq. 21): δ := k_c − ρ (range [−1,1]), κ := k_c + ρ − 1 (range [−1,1]). δ=1은 chromatin이 transcription보다 빠르게 열림 (priming or Model 2 decoupling), δ=−1은 Model 1 decoupling, κ=1은 coupled induction, κ=−1은 coupled repression. *thresholding하면 MultiVelo의 discrete state와 대응*하나 *cell마다 다른 값*을 허용.
- **GCBDir (Generalized cross-boundary direction correctness)**: UniTVelo의 CBDir (ref. 10)을 k-step neighbor + time ordering + random-walk null subtraction으로 확장한 metric (Methods Eq. 17–20). 높을수록 cell type transition direction이 정확.
- **Bayesian differential test** (Methods Eq. 22–25): posterior에서 두 조건의 sample을 반복 추출 → log difference (LD) 또는 log fold change (LFC) 계산 → Bayes factor + Gaussian process regression + LRT. FDP control (default α_FDR=0.05).
- **외부 맥락**: VAE 기반 RNA velocity는 본 분야에서 2023~24년 사이에 폭발적으로 등장 (VeloVI, PyroVelocity, DeepVelo). MultiVeloVAE는 그 흐름에 *multi-omic chromatin 축*을 추가한 변형.

### 이 논문이 필요성

- **핵심 이유**: MultiVelo가 chromatin–RNA lag 정량을 *최초로* 제공했지만 (a) cell-specific rate 미지원, (b) 단일 lineage 가정, (c) sample 간 통합 미지원, (d) hypothesis test 미지원 — 이 네 한계 모두를 *동시에* 해결할 framework가 부재.
- **기존 방법으로 부족했던 지점**: (1) developmental atlas, case-control study, multi-subject GWAS 같은 *multi-sample 비교*가 single-cell multi-omic에서 표준화 안 됨, (2) scRNA-only sample이 압도적으로 많은데 multi-omic chromatin 정보를 *imputation*해 함께 분석할 수 없음, (3) cell type 간·time 간 differential dynamics를 statistical principled하게 test 못함, (4) MultiVelo의 4 state는 cell type 간 gradient를 *binary 강제*하므로 multi-lineage bifurcation에서 fitting이 매끄럽지 못함 (Fig. 3a EB dataset의 MultiVelo backflow가 예시).
- **이 논문이 해결하려는 방향**: ① k_c, ρ를 cell-specific continuous로 두는 VAE 기반 inference, ② cVAE로 batch covariate를 directly conditioning (post hoc 통합 chaining 회피), ③ partially-overlapping modality (multi-omic + scRNA) 동시 학습, ④ Bayes factor + Gaussian process LRT로 differential dynamics statistical test, ⑤ GPU 가속으로 MultiVelo의 EM 기반 CPU runtime 한계 극복.

---

## Methods

### 이 method가 푸는 문제

- **Formal task** (§Methods "Problem setup"): cell × gene tuple (c, u, s)에서 ① cell time t, cell state z를 posterior로 추정, ② gene-specific ODE parameter θ = {α_c, α, β, γ}와 cell-specific rate {k_c, ρ}를 동시 학습, ③ 다중 sample b ∈ {1,…,B} 조건에서 sample-specific θ_b 분리, ④ 두 cell 집단 간 임의 변수의 Bayesian differential test.
- **입력**: c ∈ R^{N×G} (chromatin accessibility, optional — RNA-only mode는 c=1로 고정), u ∈ R^{N×G} (unspliced), s ∈ R^{N×G} (spliced), b ∈ {1,…,B}^N (one-hot encoded sample/batch label, optional), optional 시간 prior p₀(t) ~ N(t_true, σ₀²) (cell-wise capture time이 있으면).
- **출력**: ① cell time posterior q(t|x, b), cell state posterior q(z|x, b) (모두 Gaussian); ② gene-specific θ = [α_c, α, β, γ]; ③ cell-specific k_c, ρ; ④ batch-corrected (c, u, s) reconstruction; ⑤ 임의 variable의 differential test 결과 (Bayes factor, LRT p-value, FDR).
- **추정 대상**: variational posterior q_φ(z, t | x, b), generative parameter θ_b per batch, optional q_φ(θ) (parameter uncertainty extension, §Methods "Estimating ODE parameter uncertainty" Eq. 16).
- **중요한 hidden assumption**: (1) c, u, s 모두 *Gaussian observation noise* (MultiVelo와 동일), (2) latent prior p(z, t) = p(z)p(t)는 isotropic multivariate Gaussian, (3) chromatin은 *transcription보다 먼저* 열린다는 MultiVelo의 가정 유지 (Model 0 배제 — §Methods "Modeling chromatin accessibility and gene expression kinetics"), (4) gene별 ODE parameter는 sample 간 *유사*하다는 prior로 cross-sample regularization (Eq. 8 second term `λ Σ (θ_b − θ_r)²`), (5) k_c는 시간 무한대에서 chromatin steady-state expectation (`lim_{t→∞} c(t) = k_c`, Eq. 6).

### 확률 / 통계학적 구조

- **Model family**: amortized variational inference + ODE generative. Encoder = MLP, Decoder = MLP + ODE analytical solution (Eq. 5 closed form). Generative ODE는 MultiVelo (`@li2023multivelo`)와 동일한 3-equation system (Eq. 4), 단 k_c, ρ가 *continuous cell-specific*.
- **ELBO** (Eq. 7, multi-omic): `ELBO = Σᵢ E_{q(z,t|xᵢ,b)}[log p(cᵢ|z,t,b) + log p(uᵢ|z,t,b) + log p(sᵢ|z,t,b)] − KL(q(z|x,b)||p(z|b)) − KL(q(t|x,b)||p(t|b))`. Multi-sample loss (Eq. 8): `Loss = −ELBO + λ Σ_b (θ_b − θ_r)²` (θ_r은 reference batch parameter).
- **Mixed RNA-only mode reconstruction** (Eq. 10): multi-omic cell에는 (c, u, s) 모두, RNA-only cell에는 (u, s)만 likelihood에 포함. pseudo-c=1로 placeholder.
- **BasisVAE for gene mixture** (Eq. 12–14): gene 단위로 7개 cluster (induction-only / repression-only / complete의 조합) basis function. 각 gene은 categorical w로 *어느 basis로 generated*되었는지 표현. variational mixture of ODE — `Σ_k I{w=k} · F_k(t; θ)`. cluster 초기화는 ellipse fit 후 quantile-based vector + Dirichlet(5,5) Kolmogorov–Smirnov test.
- **Prior / regularization**:
  - latent prior p(z, t) = isotropic Gaussian, optional p₀(t) = N(t_true, σ₀²).
  - cross-batch θ regularization (`λ Σ (θ_b − θ_r)²`).
  - lower bound clipping for per-gene standard deviation (low-quality gene의 over-fitting 완화, §"Neural network and ODE parameter initialization").
  - Softplus inverse를 통한 positive ODE parameter 제약.
  - cosine annealing scheduler로 학습률 동적 조정.
- **Latent variable / hidden state**:
  - z ∈ R^d (cell state latent embedding, Gaussian posterior).
  - t ∈ R (cell time, Gaussian posterior).
  - k_c ∈ [0, 1] (cell-gene chromatin opening rate, decoder output).
  - ρ ∈ [0, 1] (cell-gene transcription rate, decoder output).
  - w ∈ {1,…,K} (gene-level basis assignment, K=2 RNA-only or K=4 multi-omic).
- **Inference / optimization**:
  - Encoder는 (c, u, s, b)을 입력받아 q(z, t|x, b)를 출력. Decoder는 (z, t, b)에서 (k_c, ρ)을 추정한 뒤 ODE Eq. 5의 해를 통해 (c, u, s)를 reconstruct.
  - 학습은 mini-batch SGD + EM 2-stage. Stage 1: global (c₀, u₀, s₀) initial condition. Stage 2: ancestor cell averaging으로 cell별 initial condition 갱신 (E-step) + ODE parameter fine-tune (M-step).
  - GPU 가속 (Methods "Development and testing environment"): RTX 3060 12 GB, 64 GB RAM, Arch Linux.
  - 학습 중단 조건: (c₀, u₀, s₀) initial value 변화가 modality variance 대비 stagnate. Best holdout validation model 저장.
- **Noise, sparsity, uncertainty 처리**:
  - **Sparsity**: ATAC 자체 sparsity는 *peak-to-gene* 집계 (promoter + correlated nearby enhancer) — MultiVelo와 동일. RNA는 STARsolo (ref. 70) + Scanpy normalize + scVelo k-NN smoothing.
  - **Cell-state uncertainty** (Eq. 15): `z_var := Σ log(σ_z/||z||) + Σ |z_std|/2 · (1 + log(2π))`. Cell type별 uncertainty를 시각화 (Fig. 2c, 3e).
  - **ODE parameter uncertainty** (Eq. 16): optional extension. variational posterior q_φ(θ)에 factorized log-normal prior.
  - **Batch effect**: cVAE conditioning + 별도 gene set g_b per batch (highly-variable gene 차이 처리) + Eq. 8의 cross-batch L2 regularization.
  - **Multiple testing** (Eq. 25): differential dynamics test에서 posterior expected FDP control, default α_FDR = 0.05.

### 핵심 method insight

- **기존 방법의 한계**: MultiVelo는 (1) cell이 *discrete 4 state*에 강제 할당, (2) 모든 cell에 *single ODE parameter set* — cell type 간 동일한 chromatin opening kinetics 가정, (3) latent time이 *gene별로* 추정되어 gene 간 inconsistency, (4) batch effect / sample variation을 model 내부에 포함 못함, (5) hypothesis test 불가, (6) lineage bifurcation은 explicit 표현 불가.
- **이 논문의 바꾼 가정**:
  - k_c, ρ를 *cell-gene별 [0,1] real-valued*로 일반화 → MultiVelo의 binary k_c ∈ {0,1}, indicator ρ를 *완전 일반화*.
  - 모든 gene에 *공통 latent time t*를 강제 (Methods "Problem setup", Fig. 1a "the latent time t is shared across all genes").
  - cVAE conditioning으로 batch label b를 latent space + decoder ODE parameter에 *동시에* 분리.
  - posterior sampling 기반 Bayesian differential test로 *cell type / time / sample 간* 임의 variable 비교 가능.
- **새로 추가한 변수 / 구조**:
  - z (low-dimensional cell state latent embedding, MultiVelo에는 없음).
  - cell-specific k_c, ρ (continuous).
  - batch-conditional ODE parameter θ_b.
  - BasisVAE mixture (gene별 7 cluster).
  - decoupling factor δ, coupling factor κ (Eq. 21) — MultiVelo의 4 state를 *연속 cell-specific*으로 일반화.
  - GCBDir metric (Eq. 19–20).
  - in silico perturbation (c=u=s=0 후 model decode) — pre-trained 모델로 SPI1/GATA1 KO simulation 가능.
- **이 변화가 중요한 이유**:
  - cell-specific (k_c, ρ) 덕분에 *같은 gene이 lineage에 따라 다른 coupling/decoupling 패턴*을 보이는 multi-lineage system을 modeling 가능 (Fig. 5a,b의 HDC, AZU1, LYZ가 lineage별로 다른 δ 부호).
  - shared latent time 덕분에 gene 간 정렬 일관성 확보 — MultiVelo의 gene별 latent time conflict가 EB dataset에서 backflow를 만드는 문제 (Fig. 3a, b) 해결.
  - conditional VAE 덕분에 chaining (먼저 통합 → MultiVelo) 없이 *직접* multi-sample velocity 추정 가능, hypothesis test 가능.
  - differential dynamics test 덕분에 *driver gene*을 statistical principled로 식별 (Fig. 6b의 macrophage vs DC volcano plot).
  - in silico perturbation으로 *wet-lab CRISPR 없이도* TF KO 예측 (Fig. 7e-h).

### 이전 방법과의 차이

- **Baseline (Fig. 2 RNA-only benchmark에 사용된 6개)**: scVelo (ref. 5), UniTVelo (ref. 10), DeepVelo (ref. 11), VeloVI (ref. 13), PyroVelocity (ref. 14), cellDancer (ref. 12).
- **Baseline (multi-omic)**: MultiVelo (`@li2023multivelo`, ref. 9) — 본 논문의 직접 predecessor + 자체 비교 (Fig. 3a, b, g, h, Supplementary Fig. 7).
- **Baseline (integration)**: Scanorama (ref. 38), scVI (ref. 17) (Fig. 4d-e benchmark).
- **Baseline (cross-modality imputation)**: scButterfly (ref. 49), scCross (ref. 50), MultiVI (ref. 51) (Supplementary Fig. 19).
- **Baseline (perturbation)**: Dynamo (ref. 52), CellOracle (ref. 53) (Fig. 7g-h).
- **공통점**:
  - 3-ODE system (c, u, s) Eq. 4는 MultiVelo와 동일.
  - peak-to-gene 집계 (promoter + linked enhancer) 전처리는 MultiVelo와 동일.
  - cell-specific ρ ∈ [0,1] real-valued는 VeloVAE (ref. 57)에서 가져옴.
  - cVAE conditioning 전략은 scVI (ref. 17)에서 차용.
  - CBDir metric base는 UniTVelo (ref. 10).
- **차이점**:
  - k_c ∈ [0,1] continuous + cell-specific (MultiVelo는 binary).
  - shared latent time t across all genes (scVelo·MultiVelo·VeloVAE는 gene별 time).
  - multi-sample cVAE + batch-specific θ_b.
  - mixed RNA-only / multi-omic 동시 학습 (Eq. 10).
  - Bayesian differential test (LD, LFC, Bayes factor, GP, LRT, FDP).
  - GCBDir metric (k-step + time ordering + random-walk subtraction).
  - in silico perturbation 지원.
  - GPU 가속 학습 (MultiVelo는 CPU EM).
- **차이가 크게 나타나는 조건**:
  - multi-lineage bifurcation system (EB 3 germ layer, HSPC 5+ lineage) — MultiVelo의 single cell type 가정이 backflow 유발 (Fig. 3a).
  - 두 sample을 함께 분석해야 하는 case-control / multi-donor study (Fig. 4 HSPC×2).
  - scRNA-seq sample이 다수이고 multi-omic은 reference 1~2개인 setting (Fig. 7).
  - cell type 간 driver gene을 statistical 식별해야 하는 case (Fig. 6 macrophage vs DC).
  - cell type별 transcriptional boost가 있는 erythroid maturation 같은 MURK gene (Fig. 2e, refs 6, 30).

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: 10개 RNA-only scRNA-seq dataset (Fig. 2, refs 20–29), 5개 multi-omic dataset (MultiVelo 비교 — Fig. 3g, Supplementary Fig. 8d), 2개 HSPC 10x Multiome (Fig. 4 batch effect benchmark), 1개 신규 EB 10x Multiome (Fig. 3a), 1개 신규 HSPC + macrophage 10x Multiome (Fig. 6), 1개 scRNA-only bone marrow BMMC + 2개 multi-omic HSPC (Fig. 7).
- **Metric**:
  - True time correlation (Fig. 2f) — actual capture time이 있는 dataset에서.
  - GCBDir (k-step CBDir + random-walk null subtraction, Eq. 19–20) (Fig. 2f, 3g).
  - Mann–Whitney U statistic of direction correctness (Fig. 2f).
  - MSE, MAE on held-out test set (Fig. 2f, Supplementary Fig. 4).
  - scIB integration metrics (iLISI, kBET, batch effect / biological conservation) (Fig. 4d-e).
  - Pearson correlation of predicted vs true chromatin (Supplementary Fig. 19a).
  - Runtime (Fig. 3h).
  - Bayes factor + LRT p-value (Fig. 6).
- **개선된 결과** (정량):
  - **RNA-only benchmark on 10 datasets** (Fig. 2f): MultiVeloVAE가 latent time correlation + GCBDir + Mann–Whitney U 모두에서 box-plot median 기준 가장 높음. `미제공: 본문은 "MultiVeloVAE achieves better performance across these metrics"라고만 명시, 각 dataset별 정확 metric 값은 Source Data file이나 Supplementary Fig. 4 참조`.
  - **MultiVelo vs MultiVeloVAE on 5 multi-omic datasets** (Fig. 3g): MultiVeloVAE의 mean k-step CBDir이 *최대 5-step neighbor*에서 MultiVelo보다 높음.
  - **Runtime** (Fig. 3h, n=5): MultiVeloVAE가 MultiVelo보다 *significantly faster* (GPU-accelerated gradient descent). `미제공: 정확 minute 값은 본문 미명시, Source Data 참조`.
  - **scIB benchmarks** (Fig. 4d-e): Scanorama와 batch effect 제거 성능 *comparable*, scVI보다 biological conservation 우위.
  - **Cross-modality prediction** (Supplementary Fig. 19): MultiVeloVAE가 scButterfly와 *on par*, scCross·MultiVI보다 Pearson correlation + MSE 우위. GCBDir 기준 ground-truth ATAC baseline보다도 *높음* — `해석: 본 결과는 MultiVeloVAE의 ATAC prediction이 velocity-guided downstream task에서 ground truth보다 nominal하게 더 잘 작동한다는 다소 의외의 결과. 사용된 cell이 다르거나 noise denoising 효과일 가능성.`
  - **Differential dynamics test** (Fig. 6b): macrophage (n=850) vs DC (n=221) 비교, p < 0.05 + FDR < 0.05로 differential velocity gene 식별. *PROS1, LGMN, LGALS3*가 chromatin opening rate에서 가장 큰 early-time 차이, RNA velocity에서는 mid-time 차이, spliced count에서는 late-time 차이.
- **Ablation 근거**:
  - **RNA-only mode** (chromatin term 제거, c=1 강제): MultiVeloVAE 코드 자체에 *built-in* 옵션 (§Methods "RNA-only and heterogeneous mode"). Fig. 2 전체가 사실상 RNA-only mode ablation — 그래도 baseline 우위.
  - **Without multi-sample inference**: MultiVelo on 2 HSPC samples로 별도 inference 시 *backflow + 잘못된 hierarchy* (Supplementary Fig. 9a).
  - **Pre-integration → MultiVelo (chaining)**: Scanorama integration 후 MultiVelo 적용 시 modality 관계 disruption → velocity inference 실패 (Supplementary Fig. 9b-c).
  - **Time prior on/off** (Supplementary Fig. 5): MEF dataset (6 time points)에서 capture-time prior를 추가하면 latent time이 *real time scale 0–28 days*와 align.
- **정성적 효과**:
  - **EB 3 germ layer** (Fig. 3a): MultiVeloVAE는 NANOG+ pluripotent root cell 정확 식별 + mesendoderm/ectoderm trajectory 회복. MultiVelo는 *unexpected backflows* 발생.
  - **HSPC**: MultiVeloVAE는 MultiVelo의 latent time을 *correct* (Fig. 3c vs d, Supplementary Fig. 7e).
  - **Mouse brain (subsampled)** (Fig. 2b): cell type별 uncertainty가 *cell cycle score와 inverse correlation*. neurons는 maturation 중 uncertainty 유지, fibroblast·oligodendrocyte는 빠르게 fate commit.
  - **MURK genes** (Smim1, Hba-x; Fig. 2e): scVelo의 *convex phase portrait* 문제를 BasisVAE의 multi-basis로 해결, transcription boost를 spliced phase portrait에 정확 reconstruct.
  - **Mouse skin** (Supplementary Fig. 7h-j): Wnt3의 priming pattern을 *IRS lineage와 진짜 priming lineage*로 정확 분리. MultiVelo는 IRS 전부에 잘못 priming 부여.
  - **GATA2→GATA1 switching** (Fig. 5b, Supplementary Fig. 11c): erythroid maturation에서 GATA1-linked gene은 coupling factor 증가, GATA2-linked gene HDC는 erythrocyte에서 negative decoupling → epigenomic repression 시그널.
  - **SPI1/GATA1 in silico KO** (Fig. 7e-h): SPI1 KO는 GMP/DC lineage 차단, GATA1 KO는 MEP/Erythrocyte/Megakaryocyte 차단. Dynamo (ref. 52) + CellOracle (ref. 53)과 *consistent*.

### Method 관점의 한계

- **약한 assumption**:
  - Gaussian observation noise on (c, u, s) — RNA count의 *negative binomial / dropout*은 별도 modeling 안 됨 (MultiVelo와 동일 한계).
  - chromatin은 transcription 전에 열린다는 *Model 0 배제* 가정 유지 (Methods "Modeling chromatin accessibility..." 후반).
  - Single c per gene — promoter + 모든 linked enhancer peak 합산. enhancer별 distinct kinetics는 directly modeling 안 됨 (Discussion에서 "MultiVeloVAE does not directly model the effects of individual cis-regulatory elements" 명시, peak-level correlation은 downstream로만).
  - Stationary BasisVAE assumption — gene이 *training 중* 단일 basis로 categorize되므로 cell-type 간 gene이 *다른 basis*를 쓰는 경우 표현 어려움.
- **구현 / 학습상의 부담**:
  - Neural network parameter (encoder + decoder MLP) + ODE parameter + θ_b per batch + (optional) q_φ(θ) → parameter 수 증가. 단 GPU 가속으로 wall-clock은 MultiVelo보다 빠름.
  - Two-stage EM 학습 (initial condition fitting → ODE fine-tune), holdout validation 추적.
  - cross-batch L2 regularization weight λ는 hyperparameter — sensitivity 분석 `미제공:`.
  - `미제공: 본문 Methods에 정확한 layer width, depth, batch size 등 hyperparameter table 없음 (Supplementary Fig. 21에 architecture diagram만 추정). Reproducibility를 위해선 GitHub 코드의 default config 확인 필요.`
  - Mature cell type (e.g., PBMCs)에서 velocity inference 자체가 어렵다는 한계 (Discussion 명시).
- **일반화가 불확실한 조건**:
  - Discussion: "inference outcome depends on the quality of unspliced and spliced RNA measurements." → 시퀀싱 quality 낮은 sample에 취약.
  - Discussion: 모든 multi-sample 통합에 *velocity inference가 sample마다 reliable*해야 함 → 한 sample이 noisy면 통합 결과도 손상.
  - Discussion: de novo 학습 — atlas-level pre-training 부재. 새 dataset마다 model 처음부터 학습.
  - `검토필요: Bergen 2021 (@li2023multivelo의 §S5 한계)에서 지적된 "simultaneous emergence of multiple cell types" challenge가 MultiVeloVAE의 cell-specific (k_c, ρ) + multi-lineage BasisVAE로 해결되는지 본문 명시 없음. Fig. 3a EB 결과는 시각적으로 multi-lineage를 잘 잡지만 quantitative 비교는 부재.`
  - cell cycle confound: HSPC 등에서 `regress out cell cycle effects from total RNA expressions` (§"Automated data preprocessing")로 명시 처리, 단 cell cycle phase별 ablation `미제공:`. MultiVelo 한계 그대로 계승.

---

## Results

### Dataset별 결과

#### Dataset 1 — RNA-only benchmark on 10 scRNA-seq datasets

- **Dataset**: 10개 scRNA-seq dataset (refs 20–29). 대표: Bone marrow mononuclear cells (BMMC) (Fig. 2a), subsampled developing mouse brain (Fig. 2b, ref. 24 La Manno 2021), mouse gastrulation (Pijuan-Sala 2019 ref. 21), human bone marrow hematopoietic (ref. 30 Barile 2021), MEF reprogramming with 6 time points (Biddy 2018 ref. 31), Pancreas (Bastidas-Ponce 2019 ref. 20), 외 4개. 일부는 UniTVelo (ref. 10)에서 제공된 preprocessed data 사용.
- **목적**: MultiVeloVAE의 RNA-only mode가 기존 RNA velocity baseline 6종 (scVelo, UniTVelo, DeepVelo, VeloVI, PyroVelocity, cellDancer) 대비 정량 우위인지 검증.
- **사용한 데이터 규모**: dataset당 cell·gene 수 본문 `미제공:` (Fig. 2 caption + Supplementary Fig. 1 참조). MEF dataset만 명시 — 6 time points (0~28 days).
- **Baseline**: scVelo (steady-state + dynamical), UniTVelo, DeepVelo, VeloVI, PyroVelocity, cellDancer. scVelo·UniTVelo는 out-of-sample prediction 없어서 MSE/MAE 평가 제외. cellDancer는 reconstruction 대신 cosine similarity 최적화이므로 MSE/MAE 제외.
- **Metric**: ① latent time vs known time point label correlation, ② GCBDir (generalized cross-boundary direction correctness, k-step + time ordering + random-walk subtraction), ③ Mann–Whitney U statistic for cluster transition direction, ④ data fit MSE/MAE on held-out test set (subset of methods only).
- **주요 수치**:
  - Fig. 2f: MultiVeloVAE box-plot median이 세 metric 모두에서 최상위. `미제공: 정확 median + IQR 수치는 Source Data file 또는 Supplementary Fig. 4`.
  - "MultiVeloVAE achieves better performance across these metrics, fitting the data accurately, aligning well with true time point labels, and generalizing well to test held-out test sets." (본문 p4).
- **정성 결과**:
  - BMMC (Fig. 2a): MultiVeloVAE는 HSC cluster origin + naive T cell island 정확 식별. *다른 method는 varying levels of backflow + inaccurate temporal predictions* (Supplementary Fig. 2 참조).
  - Mouse brain subsampled (Fig. 2b): root cell이 neural tube + neural crest로 식별, neuron / glioblast / fibroblast 방향 smooth. cell state uncertainty가 least differentiated cell에서 최고. capture time vs latent time 일치.
  - MEF reprogramming (Supplementary Fig. 5): 6 time points에서 latent time이 0–28 day와 align (time prior 사용 시 더 정확).
  - Pancreas (Supplementary Fig. 6): scVelo·UniTVelo·VeloVI는 *conflicting gene dynamics* — DeepVelo, cellDancer, MultiVeloVAE는 fate transitions를 shared temporal axis로 잡음.
  - MURK gene (Smim1, Hba-x; Fig. 2e): BasisVAE의 multi-basis가 transcription boost를 spliced phase portrait에 reconstruct.
- **논문 주장과의 연결**: RNA-only mode조차 *현존 baseline을 outperform* — chromatin 없이도 VAE + shared time + BasisVAE 구조가 standalone gain을 제공.

#### Dataset 2 — Multi-omic comparison with MultiVelo on 5 datasets

- **Dataset**: ① 신규 EB (7-day, 10x Multiome, 4,240 cells × 3,138 genes, GSE284047), ② Mouse brain 10x Multiome (`@li2023multivelo` AnnData 재사용), ③ Human brain 10x Multiome (Trevino 2021 ref. 35), ④ HSPC 10x Multiome (`@li2023multivelo`의 single time-point), ⑤ Mouse skin SHARE-seq (Ma 2020 ref. 36).
- **목적**: MultiVeloVAE가 MultiVelo (`@li2023multivelo`)를 multi-omic setting에서 directly outperform하는지 검증 + 신규 EB dataset에서 multi-lineage 능력 시연.
- **사용한 데이터 규모**: EB만 명시 (4,240 cells × 3,138 genes). 나머지는 `@li2023multivelo`와 동일 AnnData (§Methods "Automated data preprocessing").
- **Baseline**: MultiVelo (직접 자체 비교).
- **Metric**: 정성 (velocity stream, latent time, marker gene dynamics), 정량 k-step CBDir + Mann–Whitney U (Fig. 3g, Supplementary Fig. 8d), runtime (Fig. 3h, n=5).
- **주요 수치**:
  - Fig. 3g: MultiVeloVAE의 mean GCBDir이 *5-step neighbor까지* MultiVelo보다 높음 (both gene space + embedded space).
  - Fig. 3h: MultiVeloVAE runtime이 MultiVelo보다 *significantly faster* (n=5, GPU 가속). `미제공: 정확 minute 값`.
  - EB dataset: 4,240 cells × 3,138 genes (§"Automated data preprocessing"). NANOG+ root cell 식별, 3 germ layer (endoderm/ectoderm/mesendoderm) 정확 trajectory.
  - HSPC: MultiVelo의 latent time이 MultiVeloVAE에 의해 *corrected* (Fig. 3c, d, Supplementary Fig. 7e).
- **정성 결과**:
  - EB (Fig. 3a, b): MultiVeloVAE는 NANOG+ pluripotent root cell + 정확 mesendoderm/ectoderm trajectory. MultiVelo는 *unexpected backflows*. PAX6, ENC1, SAT1 (lineage marker) dynamics가 MultiVeloVAE에서는 lineage별로 명확 분기, MultiVelo는 intermingled.
  - Mouse brain (Supplementary Fig. 7a-d): cell state UMAP이 PCA UMAP보다 lineage separation 우위. OPC가 astrocyte·neuron lineage에서 분리. Satb1, Gria2, Grin2b가 더 잘 분리. chromatin velocity prediction이 noisier ATAC에서도 정확.
  - Mouse skin Wnt3 (Fig. 3f, Supplementary Fig. 7h-k): MultiVeloVAE는 priming-modality difference (k_c − ρ)를 cell-별로 quantify하여 IRS lineage의 진짜 priming vs noise 분리. MultiVelo는 IRS 전부에 잘못 priming. MultiVeloVAE latent time이 diffusion pseudotime과 *highest correlation*.
  - Human brain (Supplementary Fig. 7f-g): MultiVeloVAE는 cycling population을 global stem cell type로 식별, mGPC/OPC를 root로 잘못 잡은 MultiVelo의 backflow 해소.
- **논문 주장과의 연결**: continuous (k_c, ρ) + shared latent time + multi-lineage BasisVAE가 *모든 multi-omic dataset에서 MultiVelo 대비 quantitative + qualitative 개선* 제공.

#### Dataset 3 — Multi-sample integration on 2 HSPC 10x Multiome (Fig. 4)

- **Dataset**: 두 신규 HSPC 10x Multiome sample, 같은 culture protocol (7-day STIF medium)이나 *다른 donor + 다른 library prep + 다른 sequencing 시점* (substantial batch effects). 통합 17,667 cells × 892 genes.
- **목적**: cVAE multi-sample inference가 ① batch effect 제거, ② biological variation 보존, ③ MultiVelo의 single-sample 처리 한계 극복.
- **사용한 데이터 규모**: 17,667 cells × 892 genes (jointly preprocessed). cell type composition은 유사.
- **Baseline**: ① MultiVelo single-sample inference (Supplementary Fig. 9a), ② Scanorama pre-correction → MultiVelo chaining (Supplementary Fig. 9b-c), ③ scIB benchmark에서 Scanorama (ref. 38), scVI (ref. 17).
- **Metric**: scIB integration metrics (batch removal: iLISI, kBET; biological conservation metrics), 정성 UMAP, rate parameter distribution overlap (Fig. 4c).
- **주요 수치**:
  - cell 수: 17,667 (jointly QC-passed). gene 수: 892 (jointly highly variable).
  - Fig. 4d-e: MultiVeloVAE이 batch removal에서 Scanorama와 *comparable* + iLISI / kBET (embedded space)에서 *outperforms*. scVI보다 batch removal은 낮지만 biological conservation은 *consistently higher*.
- **정성 결과**:
  - 정렬 전 UMAP (Fig. 4a top): 두 batch가 *strongly separated*.
  - 정렬 후 UMAP (Fig. 4a bottom): cell types가 *cohesively merged*, CD133+ HSC가 root, dendritic / granulocyte / erythrocyte / megakaryocyte lineage predecessor 정확.
  - Fig. 4c: rate parameter (α_c, α, β, γ) distribution이 *largely overlapping* — cell type composition이 비슷하니까 expected.
  - Supplementary Fig. 10: 추가 phase portrait가 high-likelihood gene에서 합리적.
  - Supplementary Fig. 9: MultiVelo single-sample은 library size + unspliced/spliced ratio difference에 *easily biased*. Scanorama pre-correction은 *modality relationship disruption*으로 후속 velocity inference 실패.
- **논문 주장과의 연결**: chaining 방식 (pre-correction → velocity)이 정보 손실, MultiVeloVAE의 *directly integrated* cVAE가 둘 다 잡음.

#### Dataset 4 — Continuous coupling / decoupling factor on HSPC (Fig. 5)

- **Dataset**: Fig. 4의 2개 HSPC integrated 결과 + Scenic+ (ref. 42) gene regulatory network inference from one HSPC sample.
- **목적**: continuous δ (decoupling), κ (coupling) factor가 cell type별 priming/decoupling 정량 + TF-gene regulatory pair 해석 가능한지 검증.
- **사용한 데이터 규모**: Scenic+ 결과에서 16 TFs (MultiVeloVAE results와 Scenic+ results 모두에 존재하고 multiple HSPC differentiation stage에서 expressed).
- **Baseline**: 정성 분석 위주. 외부 reference로 ENCODE ChIP-seq + ChromHMM full-stack annotation (ref. 45).
- **Metric**: 정성 (heatmap, network plot), Spearman correlation (TF RNA vs coupling/decoupling factor of target gene) — Fig. 5d.
- **주요 수치**:
  - δ 범위 [−1, 1]. δ ≈ 1은 GMP/DC priming (e.g., HDC, AZU1, LYZ가 lineage별 다른 부호).
  - 16 TFs로 GRN 분석. Platelet / DC lineage에서 *highlighted TF가 linked target gene의 coupling factor*를 증가시킴.
  - Coupling factor κ ≈ 1 (coupled induction)이 *특정 lineage 방향* cell에서 우세, κ ≈ −1 (coupled repression)이 *반대 lineage* cell에서 우세 (Fig. 5a).
  - GATA2→GATA1 switching erythroid differentiation: CMP→MEP→Erythrocyte sequence에서 GATA1-linked gene coupling 증가 (Supplementary Fig. 11c).
  - HDC (Granulocyte marker, GATA2 target): erythrocyte 분화 시 *negative decoupling pattern* → epigenomic repression 시그널.
  - GATA2 target gene 분석: filter 후 log2 fold-change > 0 (positively associated with Erythrocyte lineage only).
- **정성 결과**:
  - SRGN (Granulocyte marker, Supplementary Fig. 13a): linked peak 중 10번째 peak이 mutual information으로 strongly connected. peak가 GMP lineage specific.
  - ChromHMM 분석: positive decoupling 연관 — BivProm1, EnhWk4, HET4, PromF4, PromF5, Quies5, TSS1, TSS2. coupling 연관 — Acet1; BivProm1,2,3; PromF3,4,5; ReprPC1; TSS1,2.
  - `해석: BivProm + TSS + heterochromatin이 decoupling과 연관된다는 결과는 chromatin remodeling의 *early-stage modification*과 일치.`
- **논문 주장과의 연결**: continuous δ, κ이 cell-specific gene regulation 패턴 + TF–enhancer–target gene network을 *single framework 안에서* 정량.

#### Dataset 5 — Macrophage differentiation differential dynamics test (Fig. 6, 신규 dataset)

- **Dataset**: 신규 생성한 macrophage differentiation 10x Multiome. CD34+ HSPC (Fred Hutch Hematology core, mobilized PBMC, U Michigan IRB exempt) 7-day STIF expansion + 7-day MSM (Myeloid Expansion Supplement II + IL-6) macrophage cytokine treatment. 통합 9,908 cells × 929 genes.
- **목적**: Bayesian differential dynamics test로 macrophage vs DC 분기의 driver gene 식별.
- **사용한 데이터 규모**: 9,908 cells × 929 genes (jointly preprocessed). Macrophage cluster 850 cells, DC cluster 221 cells.
- **Baseline**: 직접 비교 method 없음. CellRank (ref. 32)로 terminal state delineation 확인.
- **Metric**: log difference (LD) for bounded variables (k_c, ρ), log fold-change (LFC) for unbounded (c, u, s, velocity), Bayes factor (Eq. 24), Gaussian process LRT (likelihood ratio test, χ² 1 df), posterior expected FDP control (α_FDR=0.05).
- **주요 수치**:
  - Differential velocity gene: p < 0.05 + FDR < 0.05 (Fig. 6b volcano plot).
  - 5,000 posterior-sampled cells from each cluster.
  - PROS1, LGMN, LGALS3: chromatin opening rate에서 *early* latent time 가장 큰 차이, RNA velocity는 *mid* time, spliced count는 *late* time 가장 큼 → priming → activation → stable expression 시간순서.
  - CSF2RB ρ LD가 *time-constant nonzero trend* 예시 (Fig. 6d).
- **정성 결과**:
  - LMPP → GMP → MDP → monocyte → M1/M2 macrophage (Supplementary Fig. 14a) sequence 정확.
  - Prog DC + DC가 DC lineage representing.
  - Erythrocyte / granulocyte / mast / platelet (양 sample 공통)에서 cytokine-treated cell이 *later latent time* — maturation 진행과 일치.
  - Driver TF (Supplementary Fig. 15d): cisTarget DB human TF list로 differential velocity TF 식별. ZNF385D, ARID5B가 Platelet, Mast Cell lineage에서 decoupling pattern.
  - cell-type-specific decoupling (Supplementary Fig. 17a, mouse brain Robo2 / Satb2 / Gria2): Upper Layer + Deeper Layer vs V-SVZ로 비교 시 *Gria2 decoupling 확인*. 이는 `@li2023multivelo` Fig. 3의 cell 평균 분석을 cell type별로 statistical하게 확장한 결과.
- **논문 주장과의 연결**: framework 자체가 *enable*하는 새 분석 — Bayes factor + GP + LRT로 cell type 간 driver gene을 statistical principled로 식별. MultiVelo는 *불가능*했던 분석.

#### Dataset 6 — Partial integration + in silico perturbation (Fig. 7, BMMC + 2 HSPC)

- **Dataset**: 1개 public scRNA-seq bone marrow MMC (Ainciburu 2023, ref. 48, healthy donor) + 신규 2개 10x Multiome HSPC. 통합 27,841 cells × 1,044 genes.
- **목적**: ① partially-overlapping modality (RNA-only + multi-omic) joint inference, ② chromatin imputation 정확도 benchmark, ③ in silico TF KO perturbation.
- **사용한 데이터 규모**: 27,841 cells × 1,044 genes. Sample size for fate analysis: Platelet n=651, Erythrocyte n=3,043, Mast Cell n=476, Granulocyte n=1,211, DC n=294, Prog B n=668.
- **Baseline**:
  - ATAC imputation: scButterfly (ref. 49), scCross (ref. 50), MultiVI (ref. 51).
  - Perturbation: Dynamo (ref. 52), CellOracle (ref. 53).
- **Metric**: Pearson correlation (predicted vs true ATAC), MSE on top-likelihood gene (Supplementary Fig. 19b-c), GCBDir, cell fate probability change (CellRank, Fig. 7g).
- **주요 수치**:
  - 통합 cell count 27,841 (Prog B는 BMMC sample에만 존재).
  - Supplementary Fig. 19a-c: MultiVeloVAE가 scButterfly와 on par + scCross·MultiVI 우위 (Pearson, MSE).
  - Supplementary Fig. 19e: MultiVeloVAE의 GCBDir이 다른 imputation 방법 + *ground-truth ATAC baseline*보다 높음. `해석: 본 결과는 MultiVeloVAE의 ATAC가 ground truth보다 downstream velocity task에서 더 잘 작동한다는 의외 결과 — noise denoising 효과 또는 measurement artifact 가능.`
  - HBB / HDC / LYZ / PF4 (lineage marker)가 BMMC sample에서도 3D c-u-s phase portrait alignment (Fig. 7b, c).
  - BMMC sample의 inferred temporal duration이 HSPC samples보다 *shorter* (Fig. 7d bottom). `해석: in vitro 배양 HSPC가 in vivo BMMC보다 differentiation span이 길다는 결과 — 배양 condition이 differentiation rate를 변형한다는 시그널.`
- **정성 결과**:
  - SPI1 (PU.1) KO (Fig. 7e): GMP-associated lineage (DC 포함) 방향 *reversed*. CellRank fate probability change에서 MEP-associated (Platelet, Erythrocyte) 증가, DC 감소.
  - GATA1 KO (Fig. 7f): MEP downstream (Megakaryocyte, Erythrocyte) disrupted.
  - CellOracle와 *identity shift direction consistent* (Fig. 7h).
- **논문 주장과의 연결**: scRNA + multi-omic joint inference가 *실용 가능* 수준 + pre-trained model로 *wet-lab CRISPR 없이* TF KO 시나리오 예측 → drug target nomination potential.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**:
  - 모든 dataset (RNA-only + multi-omic 합쳐 16+)에서 MultiVeloVAE가 *기존 method 대비 latent time accuracy + velocity direction 개선*.
  - 모든 multi-lineage system에서 MultiVeloVAE는 root cell 정확 식별 + biologically plausible trajectory; MultiVelo는 backflow.
  - chromatin 정보가 *없는* RNA-only sample에서도 multi-omic reference sample과 함께 학습 시 *chromatin imputation 가능*.
  - integration approach (cVAE conditioning)가 *chaining (pre-correction → velocity)보다 항상 우위*.
- **가장 중요한 수치**:
  - 10 scRNA dataset RNA-only benchmark에서 6 baseline 대비 일관된 우위 (Fig. 2f).
  - 5 multi-omic dataset에서 MultiVelo 대비 k-step CBDir 우위 (Fig. 3g).
  - scIB integration benchmark에서 Scanorama / scVI와 다른 trade-off로 우위 (Fig. 4d-e).
  - 17,667 + 9,908 + 27,841 cells의 multi-sample integration 성공 (Fig. 4, 6, 7).
  - SPI1/GATA1 in silico KO가 Dynamo + CellOracle과 *consistent* (Fig. 7).
  - macrophage vs DC differential velocity gene FDR < 0.05 식별 (Fig. 6b).
- **baseline 대비 차이**:
  - 직접 vs MultiVelo: 모든 multi-omic dataset에서 정성·정량 우위, runtime은 GPU 덕분에 *significantly faster*.
  - vs other VAE-based RNA velocity (VeloVI, PyroVelocity): chromatin integration + multi-sample + differential test의 *unique features*.
  - vs Scanorama / scVI: biological conservation 우위, batch removal은 *comparable* 또는 약간 낮음 — trade-off.
- **결과 해석 시 주의점**:
  - 정량 metric의 *정확 수치*는 본문 미보고가 많고 Source Data file에 의존. 본문은 "achieves better performance" 위주 서술.
  - GCBDir이 본 논문에서 *제안한* metric이라 self-evaluation bias 가능성. `해석: random-walk null subtraction이 어느 정도 self-bias를 완화하지만, 다른 lab이 같은 dataset에서 GCBDir 외 metric으로 reproduce해야 robust 평가 가능.`
  - 신규 dataset (EB, HSPC, macrophage)가 *모두 single donor / single batch 또는 limited replicate*. inter-donor variance 검증 부족.
  - 두 HSPC sample 통합은 *same protocol 다른 donor*인데 cell type composition이 *유사*. *완전히 다른 cell type 조합* (예: 정상 vs 질환)에서의 generalization은 미검증.
  - cell cycle effect를 *RNA expression*에서만 regress out, unspliced/spliced count는 unchanged (`@li2023multivelo`와 동일 한계 계승).
  - `미제공: MultiVelo에서 보고된 priming/decoupling interval 평균 길이 (21% / 19%) 같은 *aggregate quantitative* 수치는 본 논문에 부재. Continuous (δ, κ)이라 *bin/threshold 선택 의존*.`

---

## Figures

### Figure 1 — Overview of the MultiVeloVAE model

- **이 Figure가 필요한 이유**: MultiVeloVAE의 ① 핵심 architecture (cVAE), ② 기존 method 대비 unique advantage table, ③ multi-sample integration의 schematic을 *수식 전*에 통합 도식화.
- **이 Figure가 뒷받침하는 주장**: VAE encoder-decoder + ODE analytical solution을 결합한 architecture가 multi-omic + multi-sample + chromatin imputation 모두에 적합하다는 framework-level 주장.

#### 패널별 설명

- **a (Top)**: multi-omic dynamics assumption — c → u (transcription) → s (splicing), chromatin이 transcription rate를 조절. *MultiVelo와 동일 ODE 시스템* (Methods Eq. 4 graphical form).
- **a (Bottom)**: MultiVeloVAE neural network architecture. encoder는 (c, u, s, b) 입력 → cell state z + cell time t. c는 *optional*. decoder는 (z, t, b)에서 (k_c, ρ) 추정 + ODE analytical solution으로 (c, u, s) reconstruct.
- **b**: Table — MultiVeloVAE의 unique features vs scVelo / UniTVelo / DeepVelo / VeloVI / PyroVelocity / cellDancer / MultiVelo. 비교 항목 `미제공: Figure에 명시되어 있지만 본 분석 PDF text-only로는 표 내용 미보존. 본문 §"MultiVeloVAE infers cell times..." 단락에 advantages 4개 정리`.
- **c**: multi-sample integration schematic — 두 sample 차이 (library size, sequencing time)를 corresponding cell state로 매핑 + joint dynamics inference.

##### 본문에서 강조한 비교

- **비교 대상**: MultiVeloVAE 4 advantages (continuous (k_c, ρ); shared latent time across genes; multi-sample inference; hypothesis testing)를 기존 method가 못한다는 점 (§"MultiVeloVAE infers cell times...").
- **관찰된 차이**: scVelo / UniTVelo / MultiVelo가 모두 *single sample + binary state + per-gene time + no testing* 중 일부 한계 보유.
- **이 차이가 의미하는 것**: framework-level *모든 한계*를 통합 해결하는 unified design.

##### 해석 시 주의점

- Architecture diagram이 *high-level schematic*. 정확한 layer width/depth/activation은 Supplementary Fig. 21에 추정 — 본 분석에 미접근.
- BasisVAE gene-level clustering 부분은 a에 explicit 표현 안 됨.

### Figure 2 — Benchmarking MultiVeloVAE and previous methods on scRNA datasets

- **이 Figure가 필요한 이유**: MultiVeloVAE의 RNA-only mode가 *현존 6개 RNA velocity baseline을 outperform*하는지 quantitative 검증 — chromatin 없이도 framework 자체가 gain을 준다는 주장 입증.
- **이 Figure가 뒷받침하는 주장**: BMMC, mouse brain, gastrulation, MURK gene fit, 10 dataset aggregate 모두에서 MultiVeloVAE 우위.

#### 패널별 설명

- **a**: BMMC dataset velocity stream UMAP. 위는 cell type 색, 아래는 latent time. HSC origin + naive T cell island 정확.
- **b**: Subsampled mouse brain (ref. 24) UMAP. 좌측 2: cell type + latent time, 우측 2: cell state uncertainty + true captured time. neural tube / neural crest가 root, fibroblast / oligodendrocyte는 빠르게 fate commit, neuron은 maturation 동안 high uncertainty 유지.
- **c**: cell state uncertainty vs latent time density + scatter. 우상단 / 좌하단 / 우하단은 cell type 색, 좌하단 scatter는 cell cycle score. *uncertainty ↔ cell cycle score 역상관*. bar plot inset: 각 cell type별 uncertainty vs latent time regression coefficient.
- **d**: mouse gastrulation (ref. 21) + human bone marrow hematopoietic (ref. 30 Barile 2021) UMAP. 정확 lineage prediction (blood cells에서 multi-basis 효과).
- **e**: transcription boost + MURK gene phase portrait (Smim1, Hba-x). 좌측 convex induction phase 문제 도식화, 우측 spliced phase portrait는 BasisVAE의 induction basis 할당으로 정확 reconstruct.
- **f**: 10 scRNA-seq dataset에서 ① latent time vs true time Spearman correlation, ② GCBDir, ③ Mann–Whitney U statistic box plot. MultiVeloVAE median이 세 metric 모두에서 최상위. dashed line = mean, solid = median, box = IQR, whisker = 1.5×IQR.

##### 본문에서 강조한 비교

- **비교 대상**: MultiVeloVAE RNA-only vs scVelo, UniTVelo, DeepVelo, VeloVI, PyroVelocity, cellDancer.
- **관찰된 차이**: 모든 metric에서 MultiVeloVAE 우위. backflow / inaccurate temporal prediction은 다른 method에서 빈번.
- **이 차이가 의미하는 것**: BasisVAE + shared time + cell-specific ρ의 *RNA-only standalone gain*이 chromatin 없이도 substantial.

##### 해석 시 주의점

- GCBDir이 본 논문 제안 metric → self-evaluation bias 가능. random-walk null subtraction이 완화 장치.
- Box plot이 *dataset 단위 aggregate* — dataset 간 difficulty 차이를 단일 분포에 합침.
- VeloVI / PyroVelocity의 *uncertainty-aware* prediction이 단순 point estimate 비교에서 불리할 가능성. `해석: Bayesian method 본연의 strength (posterior coverage)는 GCBDir에 반영 안 됨.`
- MURK gene을 fit하지 못한 dataset에서도 BasisVAE *misassignment*가 없었는지 보고 부재 — 일부 false-positive induction 가능성 (`@li2023multivelo`의 M2 over-assignment 위험과 유사).

### Figure 3 — Multi-omic velocity inference and comparison with MultiVelo

- **이 Figure가 필요한 이유**: MultiVeloVAE가 직접 predecessor MultiVelo (`@li2023multivelo`)를 multi-omic setting에서 outperform하는지 *직접 비교*. + 신규 EB dataset에서 multi-lineage 능력 시연.
- **이 Figure가 뒷받침하는 주장**: shared time + cell-specific (k_c, ρ) + lineage bifurcation의 *명확한 advantage*가 EB, HSPC, mouse skin 등 모든 multi-omic dataset에서 관찰됨.

#### 패널별 설명

- **a**: 신규 EB dataset velocity stream UMAP. 위는 cell type, 아래는 latent time. 좌측 MultiVeloVAE, 우측 MultiVelo. MultiVeloVAE는 NANOG+ root + mesendoderm/ectoderm trajectory 정확, MultiVelo는 backflow.
- **b**: PAX6, ENC1, SAT1 (lineage marker) generated spliced mRNA를 latent time 함수로 plot. 좌측 MultiVeloVAE는 lineage별로 명확 분기, 우측 MultiVelo는 intermingled.
- **c**: HSPC dataset MultiVeloVAE velocity stream UMAP + latent time.
- **d**: 같은 HSPC dataset에서 MultiVelo latent time — *부정확*, MultiVeloVAE에 의해 corrected됨.
- **e**: cell-state uncertainty UMAP (MultiVeloVAE의 variational posterior로 추정). stem-like / multipotent progenitor에서 *높은 uncertainty*.
- **f**: Wnt3 gene의 modality priming pattern (Mouse skin). 4개 UMAP — original chromatin accessibility / unspliced / spliced / cell-state difference (k_c − ρ). 화살표가 differentiation order 표시. k_c − ρ가 chromatin activation region 정확 capture.
- **g**: 5개 multi-omic dataset에서 GCBDir vs k-step (1~5). MultiVeloVAE가 MultiVelo보다 *지속적으로 위*. 좌측 entire gene space, 우측 embedded space. mean solid line + credible interval ribbon.
- **h**: runtime box plot (n=5). MultiVeloVAE가 MultiVelo보다 *significantly faster*. IQR + median + 1.5×IQR whisker.

##### 본문에서 강조한 비교

- **비교 대상**: MultiVeloVAE vs MultiVelo (모든 panel).
- **관찰된 차이**: backflow 해소, lineage marker 분기, latent time correction, GCBDir 우위, runtime 단축.
- **이 차이가 의미하는 것**: VAE + cell-specific rate + shared time이 MultiVelo의 핵심 한계 (single cell type 가정, gene별 time conflict)를 직접 해결.

##### 해석 시 주의점

- runtime 비교는 *GPU vs CPU* — fair한 자원 비교가 아님. MultiVelo도 GPU porting하면 시간 단축 가능 (단 본 논문 시점 미구현).
- EB dataset만 신규, 나머지는 MultiVelo의 AnnData 재사용 — *MultiVelo paper의 학습 결과*와 직접 head-to-head이지만 hyperparameter / preprocessing은 *다를 수 있음*.
- Wnt3 priming 결과 (f)에서 *cell-state difference*가 priming의 정의 — circular reasoning 위험. `검토필요: ground-truth priming label 부재.`

### Figure 4 — Integration and velocity inference of two HSPCs

- **이 Figure가 필요한 이유**: multi-sample inference 능력의 핵심 시연. 두 batch의 HSPC를 *cVAE 단일 모델*로 통합하면서 velocity inference 동시 수행.
- **이 Figure가 뒷받침하는 주장**: cVAE conditioning이 batch effect를 latent space에서 분리하면서 biological variation을 보존, scIB benchmark에서 Scanorama / scVI와 trade-off 균형.

#### 패널별 설명

- **a**: UMAP. 위는 통합 전 (gene expression concatenation), 아래는 통합 후 (MultiVeloVAE batch correction). 4개 색 옵션 — cell type, batch label, latent time, CD133 expression. velocity stream이 batch-corrected lineage prediction을 보여줌.
- **b**: 여러 lineage marker gene의 phase portrait + dynamic plot. integration이 *gene expression profile을 merge*하면서 multi-lineage modeling 유지.
- **c**: 두 batch의 rate parameter (α_c, α, β, γ) distribution. *largely overlapping* — cell type composition 유사하기 때문 expected.
- **d**: scIB batch effect removal metrics. MultiVeloVAE이 Scanorama와 comparable, iLISI / kBET (embedded) 우위. scVI는 batch removal 최강.
- **e**: scIB biological conservation metrics. MultiVeloVAE가 scVI보다 consistently higher.

##### 본문에서 강조한 비교

- **비교 대상**: MultiVeloVAE vs Scanorama vs scVI (Fig. 4d-e). 또 보조 — MultiVelo single-sample (Supplementary Fig. 9a), Scanorama → MultiVelo chaining (Supplementary Fig. 9b-c).
- **관찰된 차이**: MultiVeloVAE는 batch removal에서 scVI보다 약하지만 biological conservation 우위. 양쪽 모두 balanced.
- **이 차이가 의미하는 것**: integration ↔ biology preservation trade-off에서 MultiVeloVAE는 *biology 쪽으로* 위치. velocity inference에 적합.

##### 해석 시 주의점

- scIB metric은 *static integration*용 — *velocity-aware* metric은 본 논문이 GCBDir로 따로 보고. 두 metric 모두에서 evaluation이 필요.
- 두 sample이 *cell type composition 유사* — 진짜로 다른 cell type 분포일 때 (e.g., 정상 vs 질환) trade-off가 어떻게 변하는지 미검증.
- Rate parameter overlap (c)이 *similar composition* 덕분이라 명시 — 다른 composition에서는 *cross-batch L2 regularization (Eq. 8의 λ)*이 합리적이지 않을 수 있음.

### Figure 5 — Continuous coupling and decoupling factors in HSPCs

- **이 Figure가 필요한 이유**: MultiVelo의 discrete 4 state를 continuous δ, κ로 일반화한 것이 *실제 biological insight*를 추가 제공하는지 시연. Scenic+ GRN과 ChromHMM annotation을 결합한 external validation.
- **이 Figure가 뒷받침하는 주장**: continuous (δ, κ)가 cell-type-specific priming/decoupling 패턴을 정량 + TF-target 관계와 일치.

#### 패널별 설명

- **a**: lineage marker gene (Hb-related, HSC markers 등)의 c, u, s를 *continuous coupling factor κ로 색*. κ ∈ [−1, 1]. coupled induction (κ≈1)이 specific lineage 방향 cell에서 우세, coupled repression (κ≈−1)이 다른 lineage에서 우세. Inset: UMAP에 marker gene expression.
- **b**: a와 동일 gene을 *continuous decoupling factor δ로 색*. δ ∈ [−1, 1]. δ=1은 priming (k_c=1, ρ=0) ↔ Model 2 decoupling, δ=−1은 Model 1 decoupling.
- **c**: Scenic+ GRN. TF node + region node (TF에 regulated, log2 fold-change로 색) + target gene node (cell-type mean coupling factor로 색). edge는 accessibility-expression correlation + region-to-gene importance. activated TF-region-gene triplet이 강조 (Platelet과 DC 두 cell type).
- **d**: TF RNA expression vs target gene coupling factor (좌) / decoupling factor (우) Spearman correlation. coupling이 positive regulation TF와 *positively* associated, decoupling은 *inversely*.
- **e**: posterior-sampled cell의 mean prediction + credible interval을 cell type별로 시각화. zero line 포함.
- **f**: 한 TF의 RNA + region accessibility + target gene의 c, u, s를 latent time 함수로 plot. specified lineage에서. Modality count는 MultiVeloVAE reconstruct.

##### 본문에서 강조한 비교

- **비교 대상**: coupling vs decoupling factor의 정보 (a vs b), TF positive vs negative regulation (d), GATA2-linked vs GATA1-linked gene (Supplementary Fig. 11c), Platelet vs DC lineage TF effect (c).
- **관찰된 차이**: decoupling factor가 *cell-type-specific multi-omic regulation details*를 보여주고, coupling factor는 *overall* TF-gene association.
- **이 차이가 의미하는 것**: MultiVelo의 4 state로는 잡지 못한 *gradient continuity*가 GRN과 chromatin annotation에 연결 가능.

##### 해석 시 주의점

- Scenic+ GRN 자체가 *predicted* — wet-lab perturbation 검증 없이는 causal direction 미확정.
- ChromHMM annotation은 *external bulk ENCODE* — single-cell resolution 매칭 한계.
- GATA2 → GATA1 switching은 *기존 literature*에서 잘 알려진 phenomenon (refs 43, 44). MultiVeloVAE가 이 알려진 신호를 capture했다는 것이지 *새 발견*은 아님.
- 16 TFs 선정 기준이 *MultiVeloVAE + Scenic+ 양쪽에 있는 것*이라 *cherry-picked bias* 가능.

### Figure 6 — Differential dynamics in macrophage differentiation

- **이 Figure가 필요한 이유**: framework가 *enable*하는 가장 unique 분석 — Bayes factor + Gaussian process LRT 기반 differential dynamics test. 신규 HSPC + macrophage 10x Multiome dataset에서 시연.
- **이 Figure가 뒷받침하는 주장**: cell type 간 driver gene을 statistical principled로 식별 가능, *time-varying* difference도 잡음.

#### 패널별 설명

- **a**: UMAP. 위는 통합 전 (HSPC 파란색, cytokine-treated 주황색), 아래는 통합 후 (cVAE batch correction). 같은 cell type annotation color. Macrophage-associated lineage가 cytokine-treated sample에 enriched.
- **b**: 위 — Macrophage (n=850) vs DC (n=221) cluster의 differential velocity gene volcano plot. 5,000 posterior-sampled cell from each cluster. p < 0.05 + log difference < −3 or > 3을 색으로 표시 (녹색 / 파란색). p-value는 *multiple testing 미보정* (단 FDR < 0.05 verified). 아래 — UMAP에 각 significant gene의 velocity 색.
- **c**: macrophage vs DC differential dynamics. 한 column = 한 gene, 한 row = 한 parameter (k_c, ρ, ds/dt, s). x-axis = latent time, y-axis = LD or LFC. color = Bayes factor. gray ribbon = 95% credible interval (Gaussian process fit). p-value = LRT 1 df (time-varying vs time-constant null). inset scatter = c, u, s vs latent time colored by cell type.
- **d**: c와 동일 layout, DC vs macrophage 비교.

##### 본문에서 강조한 비교

- **비교 대상**: macrophage vs DC, time-varying vs constant pattern, k_c LD vs ρ LD vs velocity LFC vs spliced LFC.
- **관찰된 차이**: PROS1, LGMN, LGALS3에서 early k_c → mid velocity → late spliced 시간 순서. CSF2RB ρ LD는 *time-constant nonzero* (less common pattern).
- **이 차이가 의미하는 것**: gene의 *어느 step* (chromatin opening, transcription rate, velocity, accumulated mRNA)에서 cell type 차이가 시작되는지 *시간 해상도*로 추적 가능 — bulk RNA-seq differential test가 못 잡는 dynamic signal.

##### 해석 시 주의점

- p < 0.05 + FDR < 0.05 verified — 단 Volcano plot의 *displayed p-values are not adjusted*. 사용자가 표 해석 시 두 layer (raw p + FDP) 구분 필요.
- 5,000 posterior-sampled cell — *generated* cell, 실측 cell 아님. posterior misspecification 시 *false confidence*.
- DC cluster n=221 — *상대적으로 작은 cluster*. Bayes factor가 작은 sample에서 *flatten*될 위험.
- LRT의 *null = time-constant LD/LFC*. 따라서 *constant nonzero* 차이는 잡지만 *비선형 small변화*는 power 낮을 수 있음.
- driver gene 식별이 cell-type marker로 *이미 알려진 것* (macrophage / DC marker) 중심 — 진짜 *novel* driver 발견인지 cell type marker enrichment인지 본문 미구분.

### Figure 7 — Integration of two multi-omic HSPCs with one scRNA BMMC + in silico perturbation

- **이 Figure가 필요한 이유**: ① partially-overlapping modality (RNA-only + multi-omic) joint inference의 핵심 시연, ② in silico TF KO perturbation의 실용성 검증.
- **이 Figure가 뒷받침하는 주장**: scRNA-only sample도 multi-omic reference와 joint 학습 시 chromatin imputation 가능 + pre-trained model로 SPI1/GATA1 KO 시나리오 예측 가능.

#### 패널별 설명

- **a**: 3 dataset (HSPC×2 + BMMC) 통합 UMAP. Fig. 4a, 6a와 유사한 batch correction 시연.
- **b**: HBB (erythrocyte), HDC (granulocyte), LYZ (DC) marker의 3D c-u-s phase portrait. original vs batch-corrected. 세 dimension 모두 align — chromatin axis 포함 (BMMC sample은 chromatin 미관측이었으나 imputed).
- **c**: scRNA-seq cell만 추출, generated chromatin / unspliced / spliced를 latent time 함수로 plot. chromatin은 *input에 없는데도* 생성됨. HBB, HDC, LYZ, PF4 모두 priming pattern (chromatin 먼저, transcription 나중).
- **d**: 위 — scRNA-seq cell의 generated chromatin과 inferred chromatin velocity arrow. 아래 — 3개 dataset 모든 cell. BMMC가 multi-omic HSPC보다 *shorter inferred temporal duration*.
- **e**: SPI1 (PU.1) KO. SPI1 expression UMAP + KO 후 perturbation force UMAP + PC1 (cell state difference) UMAP + latent time difference UMAP. *GMP/DC lineage 방향 reversed*.
- **f**: GATA1 KO. e와 동일 layout. *MEP downstream lineage (Megakaryocyte, Erythrocyte) disrupted*.
- **g**: CellRank fate probability change (perturbed vs original). cell type별 sample size 표시 (Platelet=651, Erythrocyte=3043, Mast=476, Granulocyte=1211, DC=294, Prog B=668).
- **h**: CellOracle inferred identity shift after perturbation — MultiVeloVAE perturbation force와 *direction consistent*.

##### 본문에서 강조한 비교

- **비교 대상**: SPI1 KO vs GATA1 KO (mutual inhibition pair), MultiVeloVAE vs Dynamo + CellOracle (g, h), multi-omic HSPC vs BMMC temporal duration (d).
- **관찰된 차이**: SPI1/GATA1이 expected opposite lineage 차단. MultiVeloVAE perturbation이 기존 method와 consistent. BMMC가 *shorter* temporal duration.
- **이 차이가 의미하는 것**: framework가 *wet-lab CRISPR 없이* TF perturbation 시나리오 sketch 가능 — drug target nomination potential.

##### 해석 시 주의점

- in silico KO는 *(c, u, s) = 0*로 단순 zeroing — 실제 KO는 *gene-specific compensation mechanism* + *off-target effect*가 있어 동일하지 않음. *consistency with Dynamo/CellOracle*는 *상호 검증*이지 *ground truth 검증* 아님.
- BMMC chromatin imputation은 *multi-omic reference의 cell type 분포*에 의존. reference에 없는 cell type은 imputation 신뢰도 낮음.
- 단일 healthy donor BMMC (ref. 48). donor variability 미검증.
- BMMC vs HSPC temporal duration 차이가 *in vitro vs in vivo*의 differentiation rate 차이라는 해석 — `해석:` confound (sample 처리 시점, batch) 가능성.

---

## Tables

본문에 정식 Table 없음. paper-info.yaml의 sources 블록에는 Supplementary가 별도 포함되지 않았고, 본 분석은 Figure 위주로 구성된다. Source Data files (figshare)에 dataset별 metric 값이 있는 것으로 추정 — `미제공: Supplementary Table은 다운로드되지 않아 본 분석에 포함 안 됨`.

`외부 맥락: Nature Communications는 본문 Table을 *별도로 publish*하기보다 Figure caption과 Source Data로 대체하는 경향이 있음.`

---

## Supplementary Information

### Supplementary Figures (S1–S22, 본문 인용 기반 요약)

본 분석은 Supplementary PDF가 다운로드되지 않아 *본문에서 언급된 supp 항목만* 정리한다. 실제 패널 분석은 `미제공:` — 후속 다운로드 후 확장 필요.

<details>
<summary>S1 — RNA-only benchmark details</summary>

10 scRNA-seq dataset의 cell·gene 수, baseline별 latent time correlation / GCBDir / Mann–Whitney U 정확 수치. (Fig. 2f의 underlying data로 추정.)
</details>

<details>
<summary>S2 — BMMC velocity comparison</summary>

다른 method (scVelo, UniTVelo 등)의 BMMC stream — backflow + inaccurate temporal prediction.
</details>

<details>
<summary>S3 — MURK gene assignment</summary>

a-d: transcription boost가 unspliced acceleration이 0에 가까운 시점에서 detection 가능. e: top likelihood induction-only / repression-only assignment 정확성.
</details>

<details>
<summary>S4 — Benchmark with VeloVI / PyroVelocity / DeepVelo MSE/MAE</summary>

held-out test set fit quality 비교. Fig. 2f의 보조.
</details>

<details>
<summary>S5 — MEF reprogramming time prior</summary>

a-f: time prior on/off 비교. 6 time points (0–28 days)에서 latent time이 time prior 사용 시 더 정확 align. Apoa1 (induced endoderm progenitor marker), Col1a2 (MEF marker)로 successful vs unsuccessful reprogramming 식별.
</details>

<details>
<summary>S6 — Pancreas dataset gene dynamics</summary>

scVelo / UniTVelo / VeloVI는 conflicting gene dynamics, DeepVelo / cellDancer / MultiVeloVAE는 shared temporal axis에서 fate transition 잡음.
</details>

<details>
<summary>S7 — MultiVelo vs MultiVeloVAE on 4 multi-omic datasets</summary>

a, c: mouse brain cell type / latent time. b: Satb1, Gria2, Grin2b lineage separation. d: chromatin velocity prediction quality. e: HSPC latent time. f, g: human brain cycling root + cell-type identification (MultiVelo의 mGPC/OPC misidentification 해소). h-j: mouse skin Wnt3 priming pattern + IRS lineage proper separation. k: latent time vs diffusion pseudotime correlation.
</details>

<details>
<summary>S8 — Inferred rate parameters analysis</summary>

a: cell-specific (k_c, ρ)가 induction/repression stage 정확 반영. Satb2, Gria2 priming/decoupling pattern recapitulate. b: velocities가 modality derivative과 consistent. c: coherence score 낮은 gene은 phase portrait ambiguous. d: 5 dataset에서 k-step CBDir + Mann–Whitney U.
</details>

<details>
<summary>S9 — MultiVelo single-sample failure on HSPC×2</summary>

a: library size + unspliced/spliced ratio difference에 *easily biased*. b-c: Scanorama pre-correction이 modality relationship disruption → 후속 velocity inference 실패.
</details>

<details>
<summary>S10 — Additional batch-corrected phase portraits</summary>

high-likelihood gene에서 phase portrait가 합리적. Fig. 4의 보조.
</details>

<details>
<summary>S11 — Scenic+ analysis details</summary>

a: 16 TFs selected. b: HSC cluster에서 same gene이 mostly positive decoupling (priming) → mature cell에서 coupled induction. c: GATA2→GATA1 switching erythroid sequence.
</details>

<details>
<summary>S12 — Additional TF-region-gene dynamics</summary>

Fig. 5f의 추가 example.
</details>

<details>
<summary>S13 — Peak-level analysis</summary>

a: SRGN gene linked peak 중 10번째 peak이 GMP lineage specific. b: peak accessibility ↔ decoupling factor correlation; ChromHMM state별 enrichment.
</details>

<details>
<summary>S14 — Macrophage differentiation cell type details</summary>

a: LMPP→GMP→MDP→monocyte→M1/M2 macrophage. b: cytokine-treated cell의 maturation latent time. c: 공통 cell type에서 cytokine-treated cell이 later. d: CellRank terminal state. e: rate parameter overlap between two samples.
</details>

<details>
<summary>S15 — Differential erythrocyte vs megakaryocyte + driver TFs</summary>

a-c: 두 lineage 간 differential dynamics gene. d: cisTarget human TF list로 differential velocity TF 식별. ZNF385D / ARID5B가 Platelet / Mast Cell decoupling.
</details>

<details>
<summary>S16 — EB three-lineage differential dynamics</summary>

EB dataset의 mesendoderm / ectoderm 등 lineage 간 driver gene.
</details>

<details>
<summary>S17 — Mouse brain cell-type-specific decoupling test</summary>

a: Robo2, Satb2, Gria2 cell-type-specific decoupling test. Upper Layer / Deeper Layer / V-SVZ 비교.
</details>

<details>
<summary>S18 — 3 dataset integration PCA</summary>

Fig. 7 integration의 latent cell state PC.
</details>

<details>
<summary>S19 — Cross-modality ATAC prediction benchmark</summary>

a: top-likelihood gene Pearson correlation. b-c: MSE, MAE — MultiVeloVAE on par with scButterfly, better than scCross / MultiVI. d: SPINK2 (HSC/LMPP marker) dynamic chromatin plot. e: GCBDir — MultiVeloVAE가 ground-truth ATAC baseline보다도 높음.
</details>

<details>
<summary>S20 — ODE / chromatin process diagrams</summary>

a: stochastic Markov chromatin process. b: k_c interpretation as steady-state expectation.
</details>

<details>
<summary>S21 — Neural network architecture</summary>

a: encoder + decoder MLP architecture. layer width / depth `미제공:` (본문 미명시).
</details>

<details>
<summary>S22 — Automated preprocessing diagnostics</summary>

a: MAD-based outlier removal thresholds. b-e: cell type annotation marker gene lists for each new dataset.
</details>

### Supplementary Notes

본문 인용에서 별도 *named supplementary note*는 식별되지 않음 (MultiVelo `@li2023multivelo`의 S1-S6 같은 분리된 note 구조 없음). 모든 supplementary text는 Methods section + Supplementary Figure caption에 분산되어 있는 것으로 추정.

---

## 분석 자체에 대한 메모

- **누락된 검증 — 본 분석 자체의 한계**:
  - Supplementary PDF (Supplementary Figures + Source Data file)를 다운로드하지 않아 정확 수치 (예: 10 dataset RNA-only benchmark의 dataset별 median GCBDir, Fig. 3h의 정확 runtime minute)는 `미제공:`으로 처리. 후속 fetch 필요.
  - paper-info.yaml의 `sources.supplementary`가 빈 list → publisher landing page에서 supplementary 다운로드 시도 후 본 core 문서 갱신 가능.
- **후속 질문 (분석자 노트)**:
  - `질문: MultiVelo (@li2023multivelo)의 4 state assignment와 MultiVeloVAE의 δ, κ threshold 결과가 *얼마나 일치*하는지 정량 비교 — 본문 명시 부재. 우리 HSPC dataset에서 두 method 모두 돌려 직접 비교 필요.`
  - `질문: Bergen 2021 (@li2023multivelo §S5에서 인용된 review ref. 6)이 지적한 3 RNA velocity challenge — (1) transcriptional boost, (2) simultaneous emergence of cell types, (3) gradually increasing transcription rate — 중 MultiVeloVAE가 *명시적으로 해결한 것*은 (3) 외에 (1) MURK gene multi-basis로 추가. (2)는 multi-lineage BasisVAE로 *암묵적* 해결로 보이는데 직접 검증 부재.`
  - `질문: cell cycle confound 처리는 RNA expression에서 regress out (§"Automated data preprocessing")으로 명시 — unspliced/spliced count + ATAC은 변경 안 함. 이게 cell-specific k_c 추정에 어떤 영향? cell cycle phase ablation 필요.`
  - `질문: GCBDir이 본 논문 제안 metric — 다른 lab의 independent reproduction이 어느 정도 이루어졌는지 모니터링 필요. self-evaluation bias risk.`
- **재검토 항목**:
  - `검토필요: 본 PDF의 Fig. 1b table 내용을 text 추출에서 미보존. 정확한 feature comparison table은 PDF 자체 또는 publisher HTML에서 확인 필요.`
  - `검토필요: Supplementary Fig. 19e의 "MultiVeloVAE GCBDir > ground-truth ATAC baseline" 결과는 의외 — 본 PDF text로는 detailed evaluation setup 확인 불가. ATAC imputation이 ground truth보다 *downstream* task에서 더 잘 작동하는 이유 (noise denoising? 매뉴얼 cell selection?) 추가 조사 필요.`
  - `검토필요: BasisVAE의 7 cluster 초기화 (induction-only / repression-only / complete의 조합) 중 *어느 조합*이 multi-omic 시 자주 선택되는지 본문 미명시. cluster ratio가 dataset별로 어떻게 다른지 알면 우리 dataset에 적용 시 expected gene 분포 예상 가능.`
