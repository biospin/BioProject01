# Multi-omic single-cell velocity models epigenome–transcriptome interactions and improves cell fate prediction

Citation: `@li2023multivelo` — Li C, Virgilio MC, Collins KL, Welch JD. *Nat Biotechnol* 41(3):387–398 (2023). DOI: 10.1038/s41587-022-01476-y. PMCID: PMC10246490.

> 본 분석은 `sources/li-2023-multivelo.pdf` (48 page NIHMS author manuscript) + `sources/li-2023-multivelo-supp-1-info.pdf` (11 page supplementary) 만을 근거로 한다. 외부 지식은 `외부 맥락:` 등 prefix로 분리한다.

---

## Executive Summary

_(분석 마무리 단계에서 추가됨)_

RNA velocity는 unspliced/spliced RNA만으로 cell trajectory를 추정해 chromatin이 transcription을 어떻게 시간차로 조절하는지 직접 모델링할 수 없었다. MultiVelo는 chromatin opening/closing을 transcription rate를 조절하는 시간 변수로 두는 3-ODE 모델 + EM 기반 latent time 추정으로 이를 확장하고, 각 gene을 *primed / coupled-on / decoupled / coupled-off* 4 state로 분류한다. 네 dataset (E18 mouse brain, mouse hair follicle, fetal human cortex, human HSPC 10x Multiome 신규 데이터)에서 backflow 제거 등 cell fate 예측 정확도가 RNA-only baseline (scVelo)을 능가했고, gene을 chromatin closing이 transcription repression 전(M1, 41.4%)인지 후(M2, 26.7%, cell-cycle GO enriched)인지로 양분하며, TF expression이 motif accessibility를 평균적으로 선행하고 psychiatric-disease SNP accessibility와 linked gene expression 간의 시간차도 정량화한다 (자세한 한계·재현 ROI는 `li-2023-multivelo_lens-academic.md`, `li-2023-multivelo_lens-industry.md` 참고).

---

## Identity

- **Title**: Multi-omic single-cell velocity models epigenome–transcriptome interactions and improves cell fate prediction
- **Authors**: Chen Li, Maria C. Virgilio, Kathleen L. Collins, Joshua D. Welch (corresponding, welchjd@umich.edu)
- **Affiliation**: University of Michigan (Computational Medicine & Bioinformatics, CMB Program, Microbiology, Internal Medicine, Computer Science)
- **Venue / Year**: *Nature Biotechnology* 41(3): 387–398 (2023). Online 2022-10-13.
- **Funding**: NIH R01AI149669, R01HG010883, F31AI155047, T32GM070449, T32GM007315, DK106829 (HSPC sample)
- **COI**: 저자 명시 — "no competing interests"
- **Code**: https://github.com/welch-lab/MultiVelo (PyPI, Bioconda) — author manuscript에 license 명시는 없음. `검토필요: GitHub 페이지에서 license 확인 필요 (보통 MIT).`

---

## Background

### 배경 스토리

- **문제의 출발점**: scRNA-seq snapshot은 동일 cell을 시간 따라 관찰할 수 없으므로 *세포 분화 순서·속도*를 직접 측정하지 못한다. 계산적으로 trajectory를 재구성해야 한다. (§Introduction)
- **선행 접근 A — Pseudotime/trajectory inference (Cao 2019, Slingshot, TSCAN, Palantir, SLICER)**: cell 간 similarity로 *pseudotime* 축에 cell을 배열.
- **A의 한계**: similarity 기반이라 *전이 방향·속도*를 예측 불가. (§Introduction)
- **선행 접근 B — RNA velocity (La Manno 2018; Bergen 2020 scVelo)**: unspliced(u)/spliced(s) RNA의 ODE를 fit해 transition 방향·속도와 latent time을 함께 추정. dynamical 모델은 induction/repression phase를 explicit하게 잡는다.
- **B의 한계**: ① **transcription rate가 induction phase 동안 일정하다고 가정** → chromatin이 transcription rate를 시간에 따라 조절하는 효과를 잡지 못함. ② RNA-only이므로 chromatin priming처럼 transcription 이전에 일어나는 epigenomic 변화를 보지 못함. (§Introduction 마지막 문단)
- **선행 접근 C — protein velocity (Gorin 2020)**: RNA + protein. 단 steady-state 가정 → cell별 latent time 추정 못함. (§Introduction)
- **선행 접근 D — single-cell epigenome velocity (Ma 2020 SHARE-seq chromatin potential; Tedesco 2021 chromatin velocity)**: epigenome 정보만 사용, gene expression 미포함.
- **이 논문으로 이어지는 gap**: multi-omic single-cell (SNARE-seq, SHARE-seq, 10x Multiome) 기술 등장으로 *같은 cell에서 chromatin + RNA 동시 측정*이 가능해졌으니, ① chromatin accessibility를 transcription rate를 조절하는 *시간 변수*로 ODE 안에 넣고, ② chromatin–transcription 사이 *time lag*를 정량화하는 모델이 필요하다. (§Introduction 마지막 + §S1)

### 기본 개념

- **유전자 발현 흐름**: chromatin opening → TF binding → transcription (u → s) → mRNA degradation/export. 본 논문은 이 단계들이 *동시에* 일어나지 않고 chromatin opening이 transcription을 *시간차로* 선행하거나 chromatin closing이 transcription repression과 *어긋날* 수 있다는 점을 정량화. (§Introduction, §Results "MultiVelo: a differential equation model…")
- **RNA velocity 기본 (scVelo dynamical 모델)**: `du/dt = α^(k) − βu`, `ds/dt = βu − γs`. k는 induction(1)/repression(0) state. steady-state에서 `γ = u/s`. cell의 latent time τ는 ODE inversion으로 EM 추정 (Methods Eq. 1–9).
- **Multi-omic 데이터**: SNARE-seq (Chen 2019), SHARE-seq (Ma 2020), 10x Multiome — 단일 세포에서 RNA + ATAC 동시 측정.
- **Priming**: chromatin은 열렸으나 transcription은 아직 시작 안 함 (c > 0, u ≈ s ≈ 0). 분화 시작 단계 신호. (§Results 본문)
- **Decoupling**: chromatin closing과 transcription repression이 *다른 시점*에 시작. c와 u/s가 *반대 방향*으로 움직이는 구간. (§Results 본문)
- **외부 맥락**: chromatin "opening"은 일반적으로 distal enhancer/promoter의 nucleosome 재배치를 의미하며 ATAC-seq peak signal로 정량화 (본문 인용 Klemm 2019 ref.16). 본 논문은 이 효과를 단일 scalar c(t) ∈ [0,1]로 단순화.

### 이 논문이 필요성

- **핵심 이유**: 기존 RNA velocity는 transcription rate를 induction phase 내내 상수로 가정해, *cell이 priming인지 coupled인지 decoupled인지* 구분할 수 없다.
- **기존 방법으로 부족했던 지점**: ① chromatin → transcription의 *시간차*를 RNA만 보면 못 본다. ② early stem-like cell에서 chromatin이 먼저 열리는 priming을 직접 잡을 메커니즘이 없다. ③ TF expression vs binding-site accessibility, disease SNP accessibility vs target gene expression 같은 *cross-modality lag*도 정량 불가.
- **이 논문이 해결하려는 방향**: chromatin accessibility c(t)를 ODE 안에 *transcription rate proportional* 항으로 추가하고, chromatin opening/closing과 transcription induction/repression 각각의 *switch time*을 latent variable로 추정 → 각 gene을 4 state (primed/coupled-on/decoupled/coupled-off) × 2 model (M1: chromatin closing이 먼저 / M2: transcription repression이 먼저)로 분류 가능.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 단일 cell의 (c, u, s) 관측 3-tuple으로부터 ① 각 gene의 ODE rate parameter 5개 (α_co, α_cc, α, β, γ) + switch time 3개 (t_c, t_i, t_r), ② 각 cell의 *latent time* t와 *state* k (4종) 동시 추정. EM으로 joint inference.
- **입력**: cell × gene chromatin accessibility c, unspliced count u, spliced count s. 모두 normalize·smooth된 값.
- **출력**: ① gene별 rate parameter + switch time + best-fit model (M1 vs M2) + likelihood. ② cell별 gene-wise latent time + state assignment + 3D velocity vector (dc/dt, du/dt, ds/dt).
- **추정 대상**: ODE 8개 core parameter θ = {α_co, α_cc, α, β, γ, t_c, t_i, t_r} (Methods §"Differential equation model…" 마지막 문단).
- **중요한 hidden assumption**: ① observation은 deterministic ODE prediction + Gaussian noise (`x_i ~ N(f(t_i, θ), σ²I)`). ② chromatin은 transcription보다 *먼저* 열린다 (model 0 배제, §"Differential equation model…" 후반). ③ chromatin opening/closing kinetics는 mirror image, 단일 α_c로 표현 가능 (notation 단순화; package는 separate rate 사용).

### 확률 / 통계학적 구조

- **Model family**: continuous-time deterministic ODE + Gaussian observation noise. → Maximum likelihood / least-squares (MSE). 별도로 stochastic 변형 (Markov chromatin state, moment equations) 제공.
- **Core ODE (Methods Eq. 11–13)**:
  - `dc/dt = k_c · α_c − α_c · c` (k_c=1 opening / 0 closing)
  - `du/dt = α^(k) · c(t) − β u`
  - `ds/dt = β u − γ s`
  - **핵심 변화**: scVelo는 `du/dt = α^(k) − βu` (α 상수). MultiVelo는 `α^(k) · c(t)`로 *transcription rate를 c(t)의 함수*로 둠. chromatin이 닫혀 있으면 transcription 0, 열리면 비례 증가.
- **Likelihood (Eq. 18–19)**: `−log L(θ) = (3/2) log(2π σ²) + (1/(2nσ²)) Σ ||x_i − f(t_i, θ)||²`. → MLE = MSE 최소화. σ² MLE는 residual 표본분산.
- **Prior / regularization**: 명시적 prior 없음. 대신 ① k_c, k ∈ {0,1} 이산 state로 latent 구조 제약, ② switch time을 *interval* (Δt)로 parameterize해 양수 제약만으로 valid model 보장, ③ 일부 dataset에서 likelihood threshold (0.07 mouse skin, 0.02 HSPC)로 gene 필터링.
- **Latent variable / hidden state**: ① cell latent time t ∈ [0, 20 hr] (scVelo 기본 range), ② state k_c × k ∈ {primed, coupled-on, decoupled, coupled-off}, ③ gene별 model M1 vs M2.
- **Inference / optimization**: EM. E-step — 현재 θ로 ODE 해를 500–1,000 anchor point에서 평가, 각 cell을 가장 가까운 anchor에 KD-tree로 할당해 t 추정. M-step — Nelder–Mead simplex로 MSE 최소화, parameter를 c/u/s subset block coordinate descent (5–10 iter). Numba로 가속.
- **Noise, sparsity, uncertainty 처리**:
  - **Sparsity**: ATAC count는 매우 sparse → peak-to-gene 집계 후 TF-IDF normalization, WNN (Seurat V4) k=50 smoothing (§Methods preprocessing).
  - **Cell-to-cell noise**: 인접 RNA neighbor로 t, velocity vector smoothing (post-processing).
  - **Model determination**: ODE fit 전에 phase portrait의 *top chromatin value*가 steady-state line 위/아래에 있는지로 M1/M2 사전 결정 → 계산량 절감 + ambiguous assignment 방지. 사용자가 둘 다 fit해 likelihood 비교도 가능 (Extended Data Fig. 4h).
  - **Decoupling significance**: LRT (Eq. 23–24) — `λ_LR = -2n(ℓ(θ_0) − ℓ(θ̂))`, χ²₁ 분포. decoupling interval이 chromatin fit 개선 정도로 판단. `multivelo.LRT_decoupling`.

### 핵심 method insight

- **기존 방법의 한계**: scVelo는 *induction phase 내내 transcription rate α 상수*라 가정. 이는 chromatin이 점진적으로 열리며 transcription rate가 0 → 최대로 *증가*하는 priming 동작을 표현 못함. RNA-only 모델은 chromatin이 닫히기 시작했지만 transcription이 아직 진행 중인 decoupling 구간도 보지 못함 (§Discussion, §S1).
- **이 논문의 바꾼 가정**: transcription rate를 `α · c(t)`로 두어 *chromatin accessibility의 함수*로 변환. c(t)는 단조 증가/감소가 아니라 opening/closing phase에 따라 비대칭. → 동일 induction 구간에서도 *c가 작은 초기*는 transcription rate가 낮고, c가 saturate되면 high rate. 이게 phase portrait의 *curvature*를 자연스럽게 설명 (Extended Data Fig. 1b의 Cdh13 fit 비교).
- **새로 추가한 변수**: ① c(t) — chromatin accessibility ODE, ② k_c — chromatin state, ③ t_c — chromatin closing switch time, ④ α_co, α_cc — opening/closing rate constants, ⑤ M1/M2 — gene-level model class, ⑥ primed/decoupled/coupled-on/coupled-off — cell-gene state assignment.
- **이 변화가 중요한 이유**: ① priming 구간을 직접 추정해 early stem-like cell의 *분화 의도*를 잡을 수 있고, ② chromatin closing vs transcription repression의 순서로 *gene을 cell-cycle 등 functional class로 분리* 가능 (M2는 cell-cycle GO enriched, Fig. 2 + §S5), ③ chromatin이 추가 정보를 제공하므로 backflow 등 *RNA-only velocity의 알려진 artifact*가 줄어듦 (Fig. 2a vs 2b, Fig. 5a, Fig. 6a-b).

### 이전 방법과의 차이

- **Baseline**:
  - **scVelo dynamical** (Bergen 2020) — RNA-only EM, constant α^(k).
  - **scVelo steady-state / stochastic** (La Manno 2018) — ratio-based parameter, moment equation.
  - **VeloAE** (Qiao 2021, ref. 47) — autoencoder, scVelo velocity regularization.
  - **MultiVelo without chromatin** — c=1 constant로 축소하면 RNA-only 변형 (Methods §"Other details").
- **공통점**: induction/repression phase의 ODE 해 형태 (Eq. 7–8 vs Eq. 14–16), EM 기반 latent time, Nelder–Mead optimization, post-processing (smoothing, velocity stream)은 scVelo 도구 (`tl.velocity_graph`, `pl.velocity_embedding_stream`) 그대로 활용 (§Methods "Post-fitting analyses").
- **차이점**:
  - ODE에 c(t) 추가, transcription rate가 시간 가변.
  - 8 parameter (vs scVelo 4–5)로 차원 증가 → identifiability 우려 있지만 model predetermination + interval parameterization으로 완화.
  - Model 선택 (M1 vs M2), 4 state assignment, decoupling LRT는 scVelo에 없음.
  - chromatin preprocessing pipeline (TF-IDF + WNN smoothing, peak-to-gene aggregation, distal enhancer 0.5 correlation threshold) 명시 (Supplementary Fig. 6에서 9개 변형 비교).
- **차이가 크게 나타나는 조건**:
  - chromatin이 *transcription보다 먼저* 변하는 early progenitor (V-SVZ → IPC → 상부 layer neuron; HSC → MEP/GMP).
  - phase portrait가 RNA만으로는 *origin 근처*에 cell이 몰려 trajectory 방향을 잡기 어려운 dataset (Eomes/Tle4, Fig. 2d).
  - cell-cycle gene 같은 *transient activation* 패턴 (M2 enrichment).

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: 4개 dataset — E18 mouse brain (10x Multiome), 성체 mouse hair follicle (SHARE-seq, Ma 2020), fetal human cortex (Trevino 2021, 10x Multiome), 신규 human HSPC (10x Multiome day0 + day7, GSE209878).
- **Metric**: ① velocity stream의 *biological 일관성* (정성), ② Spearman correlation between MultiVelo latent time vs Palantir pseudotime, ③ likelihood ratio test p-value (decoupling significance), ④ Wilcoxon rank-sum (M1 vs M2 cell-cycle, expression timing), ⑤ DTW lag.
- **개선된 결과**:
  - Mouse skin: MultiVelo Spearman 0.51 vs scVelo 0.44 (vs Palantir baseline; §Results "MultiVelo quantifies epigenomic priming in SHARE-seq…").
  - Mouse brain: M2 enriched cell-cycle GO terms p < 0.002 FDR; M2 highest spliced expression earlier P = 9×10⁻⁷ (Wilcoxon).
  - HSPC: H3K4me3 (active promoter mark) higher in M2 genes p = 0.016; H3K4me1 (primed enhancer) higher in M1 p = 0.097.
  - Decoupling LRT (Supplementary Fig. 5d): Meis2 p = 9.5×10⁻¹⁷⁴, Robo2 p = 3.2×10⁻²⁷⁹, Satb2 p = 9.7×10⁻¹⁶⁹ — decoupling interval이 통계적으로 유의미하게 chromatin fit 개선.
  - Simulation: 985/1000 genes (98.5%) likelihood-based correct model assignment; 95.8% based on top-quantile counts (§Methods "Generation of simulated data" + §S3).
- **Ablation 근거**:
  - Without chromatin (MultiVelo RNA-only) — backflow 증가, root cell prediction 부정확 (Supplementary Fig. 5a, §S4).
  - Without decoupling — gene fitting 불일치 증가, ExN lineage 부정확 (Supplementary Fig. 5b-c).
  - M1-only or M2-only 강제 — discordance gene fitting 악화, neural lineage 영역에서 latent time variance 증가 (Supplementary Fig. 5e-f).
  - Comparison of chromatin aggregation strategies — WNN smoothing이 9개 변형 중 RNA-ATAC 정보 balance가 가장 좋음 (Supplementary Fig. 6).
- **정성적 효과**:
  - Mouse brain: scVelo는 upper layer neuron에 backflow 발생 (Fig. 2b). MultiVelo는 RG → IPC → ExN → 상하부 layer trajectory를 정확히 잡음.
  - HSPC: scVelo는 HSC differentiation 방향 부정확. MultiVelo는 HSC → MPP → LMPP/MEP/GMP의 hematopoietic hierarchy 회복 (Fig. 5a).
  - Mouse skin: scVelo는 hair-shaft direction 못 잡음, MultiVelo는 TAC → IRS/hair-shaft 방향 회복 (Fig. 4a-b).
  - Wnt3 priming: 'chromatin potential' 현상 (Ma 2020)을 시간 정량 가능. DTW에서 c-s lag 최대 0.6 / 1.0 total range (Fig. 4f).

### Method 관점의 한계

- **약한 assumption**:
  - Gaussian noise, diagonal covariance — RNA count의 *negative binomial / dropout*은 별도 모델링 안 함 (smoothing으로 대체).
  - Chromatin은 transcription 전에 열린다고 *전제* (model 0 배제). 실제 transcription이 먼저 열리는 case (예: 일부 nucleosome eviction during transcription)는 표현 못함 (§S2).
  - Single c per gene — promoter + 모든 linked enhancer peak를 *합산*해 한 scalar로. enhancer별 distinct kinetics는 못 본다.
- **구현 / 학습상의 부담**:
  - Parameter 수 증가 (8개 vs scVelo 4–5)로 *local optima* 위험. grid search 초기화 (switch time 2시간 간격) + interval parameterization으로 완화. 그래도 *partial trajectory* gene은 fit 어려움 (latent time scaling 후 보정).
  - Runtime: HSPC dataset 124 min (12-thread CPU). dataset scale up 시 *cell 수에 선형* (anchor distance), gene 수에 *병렬* (parallel optimization). GPU 가속 미구현.
- **일반화가 불확실한 조건**:
  - "Transcriptional boost" (Bergen 2021): 일부 gene이 inflection point 후 transcription rate가 급격히 증가. MultiVelo는 chromatin-driven 점진 증가만 modeling — 다른 mechanism (예: pioneer TF burst)은 못 잡음 (§S5).
  - 동시에 multiple distinct cell type emerging하는 system은 ODE assumption 한계 (저자가 §S5에서 명시).
  - Cell cycle confound: HSPC에서 cell cycle score를 regress-out했으나 (Extended Data Fig. 2b), `해석: 일반적으로 cell cycle effect가 chromatin opening/closing rate 추정에 어떤 영향 주는지 systematic ablation은 본문 미제공. 검토필요.`

---

## Results

### Dataset별 결과

#### Dataset 1 — 10x Multiome E18 mouse brain

- **Dataset**: 10x Genomics website 공개 데이터, 약 5,000 cells. Filtering 후 3,365 cells × 936 highly variable genes.
- **목적**: MultiVelo의 *기본 동작* 검증. 알려진 cortex 발달 trajectory (RG → IPC → ExN → upper/deeper layer)를 회복하는가?
- **사용한 데이터 규모**: 3,365 cells, 936 genes, 426 high-likelihood gene이 ODE model fit (likelihood threshold scVelo 기본 0.05).
- **Baseline**: scVelo dynamical (RNA-only). VeloAE도 Supplementary Fig. 4에서 비교.
- **Metric**: velocity stream의 trajectory 일관성 (정성), Wilcoxon rank-sum (M1 vs M2 cell-cycle), 4 state proportion, primed/decoupled interval length.
- **주요 수치**:
  - 게놈 분포 (variable genes 865개): induction-only 29.5%, repression-only 2.4%, M1 41.4%, M2 26.7% (Fig. 2h).
  - M1 vs M2 expression / accessibility 총량: Wilcoxon P = 0.38, 0.32 (no significant difference).
  - M2 highest spliced expression timing earlier than M1: P = 9×10⁻⁷, Wilcoxon one-sided.
  - M2 cell-cycle GO terms: 'positive regulation of cell cycle', 'mitotic cell cycle', 'regulation of cell cycle phase transition' (p value `미제공: 본문은 FDR-significant라고만 명시, exact p 없음. Mouse brain은 FDR임계값 미명시; HSPC는 < 0.002`).
  - State interval length (median across genes): primed 21%, decoupled 19% of total time. coupled-on, coupled-off 합해 약 60% (Fig. 3e, §Results 본문).
  - Chromatin closing rate / opening rate ratio: median ≈ 1 (Fig. 3f).
- **정성 결과**:
  - scVelo는 upper layer neuron에 "biologically implausible backflows" 발생 (Fig. 2b). MultiVelo는 RG/cycling population에서 시작하는 latent time을 정확히 회복 (Fig. 2a, c).
  - Satb2 (M1)는 induction phase에 chromatin max — Gria2 (M2)는 repression phase에 chromatin max (Fig. 2e).
  - Eomes, Tle4 같은 marker gene은 RNA만으로는 phase portrait origin에 cells가 몰려 구분 어려운데 chromatin이 *먼저* 올라가 *2D phase portrait가 못 보여주는 differentiation 방향*을 제공 (Fig. 2d, §Results 본문).
  - Robo2, Gria2, Grin2b를 chromatin/RNA UMAP로 비교하면 *decoupled state에서 가장 큰 discrepancy* 발생 (Fig. 3b, circled region).
- **논문 주장과의 연결**: chromatin을 추가하면 RNA-only baseline의 backflow가 해소되고, gene을 *M1 vs M2*로 양분해 chromatin 변화의 시간순서를 정량할 수 있다는 핵심 주장 1차 확인.

#### Dataset 2 — SHARE-seq mouse hair follicle (Ma 2020, GSE140203)

- **Dataset**: SHARE-seq, TAC + IRS + cuticle + cortex + medulla. 저자로부터 UMAP/cell type annotation 직접 수령.
- **목적**: 'chromatin potential' (Ma 2020에서 명명한 priming 현상)을 *시간 단위로* 정량.
- **사용한 데이터 규모**: 6,436 cells, 962 genes. Spearman 비교용은 likelihood > 0.07 필터로 140 velocity gene.
- **Baseline**: scVelo (RNA-only). Palantir pseudotime이 ground-truth proxy.
- **Metric**: MultiVelo latent time vs Palantir pseudotime Spearman, DTW c-s / u-s lag.
- **주요 수치**:
  - Spearman: MultiVelo 0.51 vs scVelo 0.44 (vs Palantir).
  - 4 state proportion: induction-only 32.4%, repression-only 0.0%, M1 66.6%, M2 1.0% (Fig. 4c). `해석: 성체 hair follicle은 mouse brain보다 induction-only + M1이 극단적으로 우세 — 일방향 분화 시스템 특성과 일치.`
  - Wnt3 DTW c-s lag max 0.6 / total time 1.0 (Fig. 4f). u-s lag는 c-s보다 항상 짧음.
- **정성 결과**:
  - scVelo는 hair-shaft 방향 못 잡음. MultiVelo는 TAC → IRS / hair-shaft cuticle / cortex / medulla 분기 정확.
  - Wnt3, Dsc1: induction-only + priming. Cux1, Dlx3, CobII1: induction + repression + 짧은 decoupling.
- **논문 주장과의 연결**: priming 현상을 직접 *시간 단위로* 정량 가능. dataset 종 (mouse adult skin) 변화에도 robust.

#### Dataset 3 — Human HSPC 10x Multiome (신규, GSE209878)

- **Dataset**: 신규 생산. Fred Hutch CD34+ HSPC, Stemspan II 배양, day 0 + day 7. 10x Multiome ATAC + Gene Expression.
- **목적**: 혈액 분화 hierarchy 회복 + cell cycle confounding 상황에서도 작동하는지 검증 + ChIP-seq histone mark로 M1/M2 *외부 검증*.
- **사용한 데이터 규모**: 11,605 cells × 1,000 genes (joint filtered). 11개 Leiden cluster. day 0 + day 7 Seurat 통합. variable genes 936개 fit.
- **Baseline**: scVelo (RNA-only). 외부 bulk ChIP-seq (GEO GSE70677) for FACS-purified HSC.
- **Metric**: 정성 stream, 4 state proportion, Wilcoxon (histone mark M1 vs M2), priming gene 시각화.
- **주요 수치**:
  - 4 state proportion: induction-only 39.3%, repression-only 0.5%, M1 40.4%, M2 19.8% (Fig. 5b). `미제공: 본문에 fit gene n 수 명시 없음 — Fig. 5b caption에 n=936으로 나옴.`
  - Histone mark Wilcoxon one-sided rank-sum (M1 vs M2):
    - H3K4me3 (active promoter): p = 0.016, M2 higher.
    - H3K4me1 (primed enhancer): p = 0.097, M1 somewhat higher.
    - H3K27ac (active enhancer): p = 0.48, no difference.
  - GO enrichment M2: 'regulation of mitotic cell cycle', 'regulation of mitotic metaphase/anaphase transition', 'regulation of mitotic sister chromatid separation' (all FDR < 0.002).
- **정성 결과**:
  - scVelo는 HSC differentiation hierarchy 부정확. MultiVelo는 HSC → MPP → LMPP/MEP/GMP/MK/Eryth/DC/Granulocyte/Platelet 5+ lineage 정확 회복 (Fig. 5a).
  - Priming gene 예: AZU1 (GMP), HBD (erythrocyte), HDC (granulocyte), LYZ (DC), PF4 (megakaryocyte) — 모두 induction-only + 초기 chromatin priming.
  - Velocity vector: chromatin은 시작 시점에 highest, RNA velocity는 HSC/MPP/MEP/GMP에서 *증가*했다가 differentiated cell에서 0으로 수렴 (Fig. 5f).
- **논문 주장과의 연결**: ① RNA-only는 hematopoietic hierarchy 못 잡는다는 알려진 어려움 (ref. 41 Bergen 2021)을 MultiVelo가 해소, ② M1/M2 분류가 ChIP-seq histone mark와 *생물학적으로 일관*되게 일치 (M2 = active promoter, M1 = primed enhancer). 단 H3K27ac은 차이 없음으로 분류 신호의 *전체 강도는 약함*.

#### Dataset 4 — Fetal human cerebral cortex 10x Multiome (Trevino 2021)

- **Dataset**: 저자로부터 multi-omic RNA + ATAC peak 직접 수령. 3개 sample 중 batch effect로 1개 제외, 2개 sample 사용 (dc2r2_r1, dc2r2_r2).
- **목적**: 발달 cortex의 TF–binding site lag, disease SNP–gene lag 정량.
- **사용한 데이터 규모**: 4,693 cells × 919 genes. ATAC consensus peaks ~500 bp. TF motif: chromVAR + JASPAR2020 → 30 variable motif.
- **Baseline**: scVelo (RNA-only).
- **Metric**: 정성 stream, 4 state proportion, DTW lag (TF expression vs motif accessibility), SNP–gene lag.
- **주요 수치**:
  - 4 state proportion (n=747): induction-only 50.5%, repression-only 3.1%, M1 38.3%, M2 8.2% (Fig. 6d).
  - TF expression vs motif accessibility DTW lag: *median across TFs positive at most latent times* (Fig. 6f) → TF expression이 motif accessibility를 *선행*. Median 정확 수치 `미제공: 본문은 "median … was positive"라고만 명시, 정확 magnitude 미보고`.
  - SNP analysis: 6,968 mental/behavioral disorder SNPs (EFO_0000677, Ensembl GWAS Catalog) → consensus peak overlap + top-gene 연결 757 SNPs → 3 group (early/late/before/after).
- **정성 결과**:
  - scVelo는 MEF2C를 "narrow u-s phase portrait"로 잘못 표현 → mostly repressive로 오분류 (§S6). MultiVelo는 induction + repression phase 모두 정확.
  - ROBO2 (M1), MEF2C (M2)가 phase portrait 비교 (Fig. 6c).
  - TF–target gene lag: EGR1, EOMES, FOXP2, PBX3 모두 TF expression이 *먼저* 올라간 후 binding site accessibility (motif) → target gene 순서 (Fig. 6e, Extended Data Fig. 3b).
- **논문 주장과의 연결**: cross-modality (TF expression → motif accessibility → target gene; SNP accessibility ↔ linked gene) lag를 *latent time scale에서* 정량 가능. Disease SNP의 *발달 시점*과 *function*을 추론할 새 framework 제시.

#### Simulation (Extended Data Fig. 5)

- **Dataset**: 1,000 simulated genes (M1 vs M2 random). α_co, α_cc, α, β, γ log-normal sampling. 4 switch interval [1,9] random. cell 수, time interval Poisson sample. noise: diagonal covariance scaled to max(c)²/90 등.
- **목적**: parameter recovery + model determination 정확도.
- **주요 수치**:
  - Likelihood-based model assignment: 985/1000 (98.5%) correct.
  - Top-quantile count based assignment: 95.8% correct.
  - Latent time recovery (Supplementary Fig. 3): MultiVelo > scVelo (chromatin 정보가 latent time 정확도 개선).
- **논문 주장과의 연결**: model 자체의 *parameter identifiability*와 *M1/M2 discrimination*이 noise 아래에서 통계적으로 검증됨.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**:
  - 모든 dataset에서 RNA-only baseline의 *backflow / hierarchy 부정확*을 chromatin 추가로 해결.
  - 모든 dataset에서 M1 (chromatin closing → transcription repression)이 M2보다 우세. M2는 *cell cycle transient activation* 패턴.
  - 모든 dataset에서 induction-only가 두 번째로 많고 repression-only는 거의 없음 → chromatin이 *대부분 열린 후 분화*하고 *닫힌 채로 transcription만 따로* 끝나는 케이스 드묾.
- **가장 중요한 수치**:
  - Spearman 0.51 vs 0.44 (mouse skin) — 가장 직접적인 quantitative win.
  - 98.5% model assignment accuracy (simulation) — method validity 근거.
  - LRT p-values up to 10⁻²⁷⁹ (decoupling significance) — chromatin이 fit에 *통계적으로 유의미*.
  - HSPC H3K4me3 p=0.016 — 외부 ChIP-seq 검증.
- **Baseline 대비 차이**:
  - Spearman 절대 차 +0.07 (mouse skin). `해석: 절대값으로는 모더리트한 개선, 단 RNA-only가 *체계적으로 실패*하는 system에서 chromatin이 필수 정보임을 보여줌 (Bergen 2021의 hematopoiesis 어려움 언급과 정합).`
  - Cell fate prediction의 *방향*이 RNA-only에서는 완전히 틀린 경우가 있어 metric 단순 차이보다 정성적 영향이 큼.
- **결과 해석 시 주의점**:
  - Spearman 0.51은 *Palantir pseudotime*을 ground-truth proxy로 가정. Palantir 자체가 부정확하면 metric 의미 약화. `해석: 진짜 ground-truth (예: real-time labeling, metabolic labeling) 없음.`
  - HSPC histone mark p=0.016은 single dataset, *FDR / multiple testing correction 미명시*. 3개 mark × 2 model = 6개 비교의 burden 고려 시 *조심해서 해석*.
  - Cell cycle GO enrichment는 *조사한 carcategory*에서 의미 있지만, M2 gene이 *반드시* cell cycle gene이라는 인과 주장으로 확장 안 됨.
  - 4개 dataset 모두 *발달/분화 system*. *steady-state tissue* (성인 간, 신장)에서 동일 동작 가정은 검증 안 됨.

---

## Figures

### Figure 1 — Schematic of MultiVelo approach (p37-38)

- **이 Figure가 필요한 이유**: MultiVelo의 핵심 idea (chromatin을 transcription rate 조절 변수로 ODE에 통합 + 4 state + M1/M2 model)를 *수식 전*에 그림으로 설득. 독자가 후속 Results 모두를 이 schematic에 비추어 해석하도록 설계.
- **이 Figure가 뒷받침하는 주장**: ODE 3개 system이 ① priming과 decoupling이라는 두 종류 chromatin-RNA discordance를 자연스럽게 만들어내고, ② 두 가지 다른 gene class (M1, M2)로 분류 가능.

#### 패널별 설명

- **a**: chromatin opening/closing → transcription (β u 생성) → splicing (β u → β u → γs degradation) 흐름과 각 단계의 ODE 식 (Eq. 10–13의 graphical form). 외쪽: chromatin opening rate α_co, 닫힘 rate α_cc, 단순화 형태로 그림.
- **b**: M1과 M2의 phase 진행. *chromatin priming → coupled induction → decoupled repression → stably repressed*. M1: chromatin closing (회색) → transcription repression (orange). M2: 반대.
- **c, d**: priming (c)와 decoupling (d) 상황을 c(t), u(t) plot으로 illustrate.
- **e**: 4 state (primed = 빨강, coupled-on = orange, decoupled = green, coupled-off = blue)를 phase portrait s vs u + c vs u로 시각화. steady-state line이 대각선으로 표시.
- **f, g**: M1 (f)과 M2 (g) gene의 3D (c, u, s) 시뮬레이션 trajectory. transcription starts (red circle), chromatin closes (red diamond), transcription ends (red x), end of trajectory (red diamond/x).

##### 본문에서 강조한 비교

- **비교 대상**: M1 vs M2 (chromatin closing이 transcription repression 전/후).
- **관찰된 차이**: M1 phase portrait는 transcriptional induction phase에서 max chromatin accessibility, M2는 transcriptional repression phase에서 max — 본문 Fig. 2e가 실데이터로 입증.
- **이 차이가 의미하는 것**: 두 *biologically distinct* gene class를 RNA-only로는 구분 불가, chromatin이 *추가적 정보*로 작동.

##### 해석 시 주의점

- Schematic이라 *exact ODE solution이 아닌 도식적 표현*. 실데이터 trajectory는 noise + partial trajectory로 e의 형태가 깔끔하게 나오지 않음 (Fig. 3a에서 실제 모양 확인).
- "Priming/decoupling"이 *factual discovery*가 아닌 *모델 정의*라는 점 — c(t) > 0이고 u(t) = s(t) = 0인 구간을 priming이라고 *명명*했을 뿐 외부 검증 분리 필요.

### Figure 2 — MultiVelo reveals two distinct mechanisms of gene regulation (mouse brain) (p39-40)

- **이 Figure가 필요한 이유**: 핵심 주장 ① "chromatin 추가가 cell fate prediction 정확도 개선" + ② "M1/M2 분류가 gene-level로 의미 있다"를 *동일 dataset (E18 mouse brain)*에서 동시에 입증.
- **이 Figure가 뒷받침하는 주장**: RNA-only baseline (scVelo)이 backflow를 만든다는 것 + M1/M2 gene이 정량적·정성적으로 구분된다는 것.

#### 패널별 설명

- **a**: MultiVelo velocity stream (left) + latent time (right) on UMAP. ExN, OPC, Astro, V-SVZ, Subventricular cells, Ependymal cells, Upper Layer, Deeper Layer 등 cell type 표시.
- **b**: scVelo velocity stream on 같은 UMAP — *upper layer neuron에 backflow 관찰* (저자가 직접 "biologically implausible backflows"로 명명).
- **c**: Cell cycle score (G2M, S). RG 근처에서 cycling pop. 화살표로 표시 — MultiVelo의 latent time origin과 일치.
- **d**: Eomes, Tle4 phase portrait — RNA만으로는 origin 근처 cluster, c 추가 시 3D 분리 (small inset).
- **e**: Satb2 (M1, red label) vs Gria2 (M2, blue label) 2D u-s phase portrait, c value를 색으로. *Satb2: c가 induction phase에서 max. Gria2: c가 repression phase에서 max*.
- **f**: Satb2/Gria2의 c-u-s 3D phase portrait + cell type color.
- **g**: M1, M2 gene의 *latent time별 spliced expression heatmap*. M2가 *더 일찍* highest expression 도달 (P=9×10⁻⁷ Wilcoxon).
- **h**: 4 type kinetics proportion donut (n=865): induction 29.5%, repression 2.4%, M1 41.4%, M2 26.7%.
- **i**: Bmper, Robo2, Meis2, Grin2b (M1) / Tle4, Igfbpl1, Tnc, Epha5 (M2) 3D phase portrait — *cell type 색*으로.

##### 본문에서 강조한 비교

- **비교 대상**: MultiVelo vs scVelo (a vs b), M1 vs M2 (e, g, h).
- **관찰된 차이**: backflow 해소, M2 timing earlier (P=9×10⁻⁷), proportion M1 ≫ M2.
- **이 차이가 의미하는 것**: chromatin이 *RNA-only가 알아채지 못한 directionality*를 제공, M2가 *transient activation*에 적합한 minor class.

##### 해석 시 주의점

- backflow 평가가 *정성적*. 정량 metric (예: branch consistency score) 미제공.
- M1 ≫ M2 비율이 *어떤 system에서도 항상* 그렇다고 일반화하지 말 것 (mouse skin은 66.6 : 1.0, dataset마다 다름).

### Figure 3 — MultiVelo captures epigenomic priming and decoupling in embryonic mouse brain (p41-42)

- **이 Figure가 필요한 이유**: 4 state assignment가 실제 cell-gene 수준에서 *구분 가능한 시각적 signature*를 가짐을 입증. priming + decoupling이라는 phenomenon이 *artifact가 아닌 reproducible* 함을 보임.
- **이 Figure가 뒷받침하는 주장**: cell-gene pair마다 4 state로 분리되며, *decoupled* state에서 chromatin vs RNA UMAP discrepancy가 시각적으로 확연.

#### 패널별 설명

- **a**: Grin2b (induction-only, primed + coupled-on), Nfix (M1, 4 state 모두), Epha5 (M2, coupled-on + decoupled만)의 3D phase portrait with state color.
- **b**: Robo2 (M1), Gria2 (M2), Grin2b의 UMAP을 c / u / state 3개 column으로. *circled region*: state assignment가 decoupled인 영역 = c, u 색이 *가장 크게 다른 영역*.
- **c**: 같은 세 gene의 c, u, s를 latent time t 함수로 + state 색 + switch time 수직선.
- **d**: 4 state별 cell당 high-likelihood gene 수를 UMAP color로. *coupled-on, coupled-off가 가장 많은 cell이 일반적*, primed/decoupled는 특정 cell에서 enriched (cascade-like transitions).
- **e**: 4 state interval length box plot — primed, coupled-on, decoupled, coupled-off (median 약 21%, 35%, 19%, 25% 추정 from plot; 본문 정확 수치 primed 21%, decoupled 19%).
- **f**: chromatin closing rate / opening rate ratio box plot — median ≈ 1, IQR roughly 0.5–1.5.

##### 본문에서 강조한 비교

- **비교 대상**: 같은 gene의 c UMAP vs u UMAP (b), 4 state interval length (e), opening vs closing rate (f).
- **관찰된 차이**: decoupled region에서 c-u 색 mismatch 가장 큼. closing/opening rate 거의 동등.
- **이 차이가 의미하는 것**: ① decoupled state가 *artifact가 아니라 real biological signal*, ② chromatin opening과 closing의 *내재 속도*가 거의 같음 → asymmetric kinetics는 없음.

##### 해석 시 주의점

- UMAP color mismatch는 *시각적 정성 evidence*. 정량 (예: per-cell c-u correlation drop in decoupled region) 본문 미제공.
- 4 state assignment는 *model 결과물*. 다른 model이면 다른 state 정의가 가능.

### Figure 4 — MultiVelo quantifies epigenomic priming in mouse skin (p43-44)

- **이 Figure가 필요한 이유**: chromatin potential (Ma 2020 SHARE-seq 논문이 처음 명명)을 *시간 단위로* 정량 가능함을 보임. 추가로 chromatin priming이 *adult tissue*에서도 작동함을 검증.
- **이 Figure가 뒷받침하는 주장**: ① MultiVelo가 scVelo가 못 잡는 hair-shaft direction을 회복, ② Wnt3 등 'chromatin potential' gene의 c → u → s lag를 *0~1 단위*로 정량.

#### 패널별 설명

- **a**: MultiVelo velocity stream + latent time. TAC, TAC-2, IRS, Hair Shaft cuticle.cortex, Medulla cell type.
- **b**: scVelo stream — *hair-shaft direction 못 잡음*.
- **c**: kinetics proportion donut (n=960): induction 32.4%, repression 0%, M1 66.6%, M2 1.0%.
- **d**: Wnt3 UMAP colored by c / u / s — *c가 먼저, u 다음, s 마지막*로 신호 출현.
- **e**: Wnt3, Dsc1 (induction + priming), Cux1, Dlx3, CobII1 (induction + repression + 짧은 decoupling)의 c-u-s vs latent time with state.
- **f**: Wnt3 DTW alignment. Top: c vs s alignment (solid line). Middle: u vs s. Bottom: instantaneous time lag (c-s, u-s) — c-s lag가 u-s lag보다 *항상 더 큼*, max ≈ 0.6.

##### 본문에서 강조한 비교

- **비교 대상**: MultiVelo vs scVelo (a vs b), DTW c-s vs u-s lag (f).
- **관찰된 차이**: hair-shaft 방향 회복, c-s lag > u-s lag.
- **이 차이가 의미하는 것**: priming이 hair follicle에서도 발생, *chromatin → unspliced → spliced* 시간순서 정량 가능.

##### 해석 시 주의점

- DTW는 *aligned curve*에서 lag 계산. local alignment가 잘못되면 lag 추정도 틀림. global vs local 선택 (Wnt3=local) 결과에 영향.
- adult skin은 분화 *방향이 단순* (TAC → IRS/shaft). 복잡한 multi-branch system에서 동일 DTW 신호 보장 안 됨.

### Figure 5 — MultiVelo identifies priming in HSPCs (p45-46)

- **이 Figure가 필요한 이유**: hematopoiesis가 RNA velocity로 *알려진 어려운 case* (Bergen 2021, ref. 41). multi-omic으로 해결되는지 + 외부 ChIP-seq으로 M1/M2 검증.
- **이 Figure가 뒷받침하는 주장**: chromatin이 hematopoietic hierarchy 회복 + M1/M2가 외부 histone mark와 일관.

#### 패널별 설명

- **a**: MultiVelo (left) vs scVelo (right) velocity stream. HSC, MPP, LMPP, MEP, GMP, MK, Eryth, Granulocyte, DC, Platelet 등 11 cluster. MultiVelo는 HSC origin, scVelo는 hierarchy 부정확.
- **b**: kinetics proportion donut (n=936): induction 39.3%, repression 0.5%, M1 40.4%, M2 19.8%.
- **c**: 4 state interval length box plot — primed, coupled-on, decoupled, coupled-off.
- **d**: G2/M cell cycle marker gene UBE2C, GTSE1, KIF20B (M2 패턴) — myeloid, erythroid, platelet lineage별 spliced + ATAC.
- **e**: priming gene 예 AZU1, HBD, HDC, LYZ, PF4의 c-u-s vs latent time. *induction-only + 초기 chromatin priming*.
- **f**: 같은 gene의 c velocity (dc/dt), u velocity (du/dt), s velocity (ds/dt) vs -t (역방향).
- **g**: u-s 2D phase portrait (RNA-only view).

##### 본문에서 강조한 비교

- **비교 대상**: MultiVelo vs scVelo stream (a), M1 vs M2 G2/M markers (d), chromatin vs RNA velocity (f).
- **관찰된 차이**: hematopoietic hierarchy 회복, G2/M marker가 M2 패턴, chromatin velocity는 *시작에서* 최대 RNA velocity는 *중간*에서 최대 (Fig. 5f).
- **이 차이가 의미하는 것**: HSPC에서도 chromatin이 *RNA-only가 못 잡는 hierarchy 정보*를 제공. cell cycle gene이 M2로 분류됨이 GO + ChIP-seq + visual marker 3중 근거.

##### 해석 시 주의점

- HSPC dataset이 *single donor*. Donor variability 미검증.
- Stemspan II 배양 + day 0/day 7 → *in vitro expansion* 영향 가능. in vivo BM HSPC와 동일한 chromatin dynamics 가정은 unverified.

### Figure 6 — MultiVelo infers epigenome and transcriptome dynamics in fetal human brain (p47-48)

- **이 Figure가 필요한 이유**: 핵심 *새로운 응용* — TF expression vs binding site accessibility lag + disease SNP accessibility vs target gene expression lag. 이는 chromatin–RNA lag 정량이라는 method 자체의 *unique value*.
- **이 Figure가 뒷받침하는 주장**: ① fetal cortex에서도 MultiVelo가 정확, ② TF가 *먼저 발현*되고 binding site가 *나중에 열림*, ③ disease-associated SNP은 *발달 시점*에 따라 3 group으로 분류 가능.

#### 패널별 설명

- **a**: MultiVelo stream + latent time. nIPC/ExN, ExUp, SP, ExM, RG/Astro, ExDp, Cyc, mGPC/OPC cell type.
- **b**: scVelo stream — IPC, upper layer neuron에 backflow.
- **c**: ROBO2 (M1, red label), MEF2C (M2, blue label) phase portrait with c color. Arrow가 chromatin closing 위치.
- **d**: kinetics proportion donut (n=747): induction 50.5%, repression 3.1%, M1 38.3%, M2 8.2%.
- **e**: EGR1, EOMES, FOXP2, PBX3의 motif accessibility vs TF gene expression DTW alignment + inset UMAP. *TF expression이 먼저, motif accessibility가 나중*.
- **f**: gene expression vs motif accessibility Δt quantile plot — *median Δt가 latent time 대부분에서 positive* (TF expression이 motif accessibility를 선행).
- **g**: SNP accessibility vs linked gene expression Δt density plot. 3 main group (가운데 ~0 / 위 positive / 아래 negative). example SNP UMAP — rs6822306 vs UNC5C expression 등.

##### 본문에서 강조한 비교

- **비교 대상**: TF gene expression vs motif accessibility lag (e, f), SNP accessibility vs gene expression lag (g).
- **관찰된 차이**: TF lead motif, SNP-gene 관계 3 그룹.
- **이 차이가 의미하는 것**: ① TF가 expression → binding → motif accessibility 변화 → target gene activation의 *시간 순서*를 latent time scale로 직접 추적 가능, ② disease SNP을 *언제 영향*을 주는지 (early vs late, before vs after gene)로 분류 가능.

##### 해석 시 주의점

- TF expression이 motif accessibility를 *선행*한다는 결과는 association이지 *causal proof* 아님. 저자도 명시: "We cannot conclusively determine the mechanisms underlying these time lags without additional data."
- SNP-gene linkage는 *기존 ATAC peak-gene correlation*에 의존 — peak-gene 관계 자체가 부정확하면 SNP 분류도 부정확.
- 6,968 SNP → 757 filtered → 3 group: filtering이 disease-relevant SNP 일부만 유지. cohort/population bias가 GWAS에서 그대로 전이.

### Extended Data Figure 1 — Additional mouse brain (p27)

- **요지**: a) cell type marker gene UMAP. b) Cdh13 RNA-only (scVelo) vs MultiVelo c-aware fit 비교 — *MultiVelo가 chromatin opening으로 인한 transcription rate 상승을 자연스럽게 fit*. c) gene likelihood vs log spliced count scatter — model assignment에 따른 likelihood 차이 없음. d) priming/decoupling interval histogram — *Pbx3 short / Celsr1 long priming, Rspo3 short / Tgfbr1 long decoupling*.

### Extended Data Figure 2 — Additional HSPC (p28-29)

- **요지**: a) HSPC marker gene UMAP. b) Cell cycle (S, G2M) score + unspliced ratio UMAP — cell cycle을 regress-out한 근거. c) FACS-purified HSC bulk ChIP-seq H3K4me3/H3K4me1/H3K27ac box plot (M1 vs M2): H3K4me3 p=0.016, H3K4me1 p=0.097, H3K27ac p=0.48. d) day 0 + day 7 sample 통합 velocity + PROM1 (CD133) HSPC marker UMAP.

### Extended Data Figure 3 — Additional human brain (p29-30)

- **요지**: a) MEF2C RNA-only vs MultiVelo fit — MultiVelo가 induction + repression 모두 정확. b) EOMES, FOXP2 TF DTW. c) 추가 motif DTW (GLI3, PROX1, NFKB1, NR4A1, SP6, ZEB1). d) 30 motif accessibility latent time bin heatmap. e) TF-target gene DTW (EGR1-SYN2, EOMES-BMPER, FOXP2-PRESS12, PBX3-LMO3).

### Extended Data Figure 4 — Chromatin dynamics + simulation illustrations (p30-31)

- **요지**: a) chromatin opening/closing asymptotic ODE schema. b) scVelo의 RNA-only latent time에 따른 chromatin trend — 실데이터에서 c가 *S자 형태*로 변하는 *qualitative 검증*. c) Model 0 simulation — chromatin이 transcription보다 *나중에* 열리는 case가 실데이터에서 거의 없음. d-f) c normalization 효과 (raw vs TF-IDF vs WNN smoothing). g) bimodal expression pattern illustration. h) M1 vs M2 model predetermination logic. i) unspliced rescale factor initialization.

### Extended Data Figure 5 — Simulation study (p32-33)

- **요지**: 1000 simulated gene, M1/M2 random. a) C-U noiseless phase portrait. b) U-S noiseless. c) 3D noiseless. d) noise added. e-h) 두 ground-truth gene (S17 M1, S41 M2)에 대해 M1, M2 모두 fit → likelihood 비교. *985/1000 (98.5%) correct*.

---

## Tables

### Table S1 (supplementary) — Runtime and memory usage

- **이 Table이 필요한 이유**: 재현·적용 평가 (resource requirement) 가능하도록 4개 dataset 모두에서 runtime, peak memory, memory increment 보고.
- **이 Table이 뒷받침하는 주장**: MultiVelo가 12-thread CPU에서 일반 lab 환경 (32GB RAM)으로 *몇십 분~2시간 내* 실행 가능.

#### 표 구조

- Row: Runtime (min), Peak memory usage (MiB), Memory increment (MiB)
- Column: Mouse brain, Mouse skin, Human HSPC, Human brain
- 셀: 정수 (memory increment만 소수점 1자리).

#### 핵심 수치

- **Runtime**: 40 / 69 / 124 / 40 min (mouse brain / skin / HSPC / human brain).
- **Peak memory**: 857 / 1602 / 2921 / 1100 MiB.
- **Memory increment**: 481.5 / 1136.5 / 2293.2 / 660.6 MiB.
- Hardware: Intel Core i7-9750H (12 threads), 32 GB memory.

#### 본문에서 강조한 비교

- **비교 대상**: dataset 간 자원 요구량.
- **관찰된 차이**: HSPC가 cell 수 11,605개로 가장 크고 runtime + memory도 가장 큼. 나머지 3개는 ~1-1.5 GB로 일반 lab 환경에서 무난.
- **이 차이가 의미하는 것**: cell scale에 *선형*에 가까운 자원 증가. GPU 없이도 dataset당 *분 단위 ~ 2시간*.

#### 해석 시 주의점

- *Intel i7 노트북 급* 하드웨어 기준. server-class GPU 미사용 → 동일 성능을 갖춘 환경에서만 reproducible.
- benchmark이 *4 datasets 모두 medium scale (≤12k cells)*. 100k+ cell scaling은 미검증.
- runtime은 main `recover_dynamics_chrom` function만 측정 — preprocessing (WNN smoothing 등) 별도 시간 미포함.

---

## Supplementary Notes (S1–S6)

<details>
<summary>S1 — Additional Background and Motivation for MultiVelo Method</summary>

기존 scVelo dynamical model 설명. MultiVelo는 *priming, decoupling interval의 길이가 gene별로 다름*을 ODE의 자연스러운 결과로 보임. 두 stable state (coupled-on, coupled-off)이 differentiated cell의 대부분 시간.
</details>

<details>
<summary>S2 — Justification for Model Assumptions</summary>

두 가지 결정: (1) c = 모든 linked peak 합산. (2) transcription은 chromatin이 *열린 후만* 발생. 두 결정 모두 *empirical 관찰*에 근거 (Extended Data Fig. 4a-b). peak 집계 전략은 9개 변형 실험 (Supplementary Fig. 6)에서 결과에 큰 영향 없음. Model 0 (transcription이 chromatin opening 전 시작)은 *생물학적으로 implausible*하다고 판단 (Extended Data Fig. 4c).
</details>

<details>
<summary>S3 — MultiVelo Accurately Fits Simulated Data</summary>

1000 simulated gene으로 M1/M2 discrimination 검증. 98.5% likelihood-based correct, 95.8% top-quantile-count-based correct. Latent time recovery는 MultiVelo가 scVelo보다 정확 (Supplementary Fig. 3).
</details>

<details>
<summary>S4 — Additional Analysis of Mouse Brain Dataset</summary>

MultiVelo는 RNA-only steady-state model (MultiVelo w/o chromatin, scVelo, VeloAE)을 outperform (Supplementary Fig. 4). LRT로 decoupling interval significance 검증 (Supplementary Fig. 5b-d). M1-only / M2-only force fit이 bi-model보다 나쁨 (Supplementary Fig. 5e-f). RNA phase portrait curvature를 RNA-only는 못 잡지만 MultiVelo는 time-varying transcription rate로 잡음 (Extended Data Fig. 1b).
</details>

<details>
<summary>S5 — Additional Details about HSPC Analyses</summary>

Bergen 2021이 지적한 3 challenge (transcriptional boost, simultaneous emergence of cell types, gradually increasing transcription rate) 중 *3번째*만 MultiVelo가 해결. 나머지 두 challenge는 *framework rethink 필요*로 미해결 명시. ChIP-seq histone mark 분석: H3K4me3 (active promoter) M2에서 높음 (p=0.016), H3K4me1 (primed enhancer) M1에서 약간 높음 (p=0.097), H3K27ac no difference.
</details>

<details>
<summary>S6 — Additional Notes on Human Brain</summary>

MEF2C (M2)가 scVelo로는 *mostly repressive*로 잘못 잡힘. MultiVelo는 induction + repression 모두 정확 (Extended Data Fig. 3a). TF-target gene downstream lag 확인 (Extended Data Fig. 3e).
</details>

---

## Supplementary Figures (S1–S6)

<details>
<summary>S1 — Computationally inferred multi-omic profiles</summary>

같은 cell에서 RNA + ATAC을 *실측하지 않은 dataset*에 대해 Seurat anchor로 imputed pairing 후 MultiVelo 실행 가능. IPC, V-SVZ region에서 imputation으로 인한 priming/decoupling 정보 손실 관찰. *MultiVelo가 paired multi-omic이 아닌 separate dataset에도 적용 가능*하지만 결과 quality 저하.
</details>

<details>
<summary>S2 — Stochastic ODE variant</summary>

chromatin을 binary Markov process로 modeling. Steady-state velocity vector를 chromatin accessibility 색으로. M1 gene: steady-state line counter-clockwise rotation. M2: clockwise. Stream plot은 RNA-only stochastic과 비교.
</details>

<details>
<summary>S3 — Simulation latent time recovery</summary>

complete:induction:repression ratio (4:5:1, 4:4:2, 4:3:3, 6:3:1, 1:8:1) + variance level (LV, HV) 변화에 따른 latent time recovery. MultiVelo가 scVelo보다 *모든 setting에서 더 정확*. complete/repression-only gene이 많아질수록 fit 어려워짐.
</details>

<details>
<summary>S4 — Comparison of steady-state models</summary>

MultiVelo deterministic, scVelo deterministic, MultiVelo RNA-only (deterministic + stochastic), VeloAE (scVelo regularization + standalone) 비교. MultiVelo deterministic은 scVelo와 유사. VeloAE standalone은 astrocyte lineage를 잘 못 잡음.
</details>

<details>
<summary>S5 — Chromatin and decoupling importance</summary>

a) RNA-only dynamical MultiVelo — backflow + root prediction 부정확. b) without decoupling — fitting instability 증가. c) gene fitting 비교 (with/without decoupling). d) LRT p-values for decoupling significance:
- Cdh12: 5×10⁻¹¹⁴, Epha5: 7×10⁻¹⁸, Gabra2: 1.5×10⁻³⁴, Gria2: 8×10⁻⁷², Meis2: 9.5×10⁻¹⁷⁴, Plxna2: 0 (under-flow), Plxna4: 0, Robo2: 3.2×10⁻²⁷⁹, Satb2: 9.7×10⁻¹⁶⁹, Unc5d: 3.1×10⁻¹².
e,f) M1-only or M2-only force fit — stream plot 일관성 저하.
</details>

<details>
<summary>S6 — KNN smoothing & ATAC aggregation variants</summary>

9개 variant 비교 (RNA WNN vs RNA KNN smoothing, ATAC TF-IDF + KNN/WNN, peak aggregation strategies). *WNN approach*가 RNA-ATAC balance 가장 좋음. ATAC aggregation은 전략 간 큰 차이 없음 → 저자 선택 (promoter + linked enhancer correlation ≥ 0.5)이 valid.
</details>
