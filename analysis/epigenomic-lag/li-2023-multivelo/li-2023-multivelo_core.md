# MultiVelo — 객관적 분석 (core.md)

> Citation: `@li2023multivelo` (Li, Virgilio, Collins, Welch — Nature Biotechnology 2023, vol 41(3) pp 387–398, DOI 10.1038/s41587-022-01476-y)
> Document type: paper (peer-reviewed)
> 출처 자료: `sources/li-2023-multivelo.pdf` (본문), `sources/li-2023-multivelo-supp-1-info.pdf` (supplementary), `sources/abstract.txt` (PubMed)
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다.

## Executive Summary

*분석 마무리 단계에서 작성 — 현재는 placeholder.*

`검토필요:` core.md / lens-academic.md / lens-industry.md / methodology-brief.md가 완성된 후 LLM이 3~5문장으로 압축한다.

---

## 1. 문제 정의 및 연구 목적

### 배경 스토리

- **문제의 출발점**: cell 운명(fate)은 chromatin opening → TF binding → RNA induction → splicing → translation의 *순차적 gene expression 조절*에 의해 결정된다. 그러나 single-cell sequencing은 cell을 파괴하므로 *같은 cell이 시간에 따라 변하는 과정*을 직접 관찰할 수 없다. snapshot에서 temporal dynamics를 추론하는 방법이 필요하다 (Introduction, p2).
- **선행 접근 A — Trajectory inference (pseudotime)**: cell-cell similarity로 pseudotime axis 구성 (refs 1–5).
  - **A의 한계**: similarity 기반 pseudotime은 transition의 *방향*이나 *상대 속도*를 직접 예측하지 못한다.
- **선행 접근 B — RNA velocity**: spliced/unspliced ratio로 미래 cell state 예측. scVelo (Bergen et al., ref 7)이 dynamical model 확장으로 transient state까지 다룸.
  - **B의 한계**: RNA-only model은 *chromatin remodeling이 transcription rate를 바꾸는 과정*을 직접 포함하지 못한다. 특히 promoter/enhancer가 먼저 열렸지만 RNA는 아직 증가하지 않은 *priming* 구간, chromatin closing과 transcriptional repression이 어긋나는 *decoupling* 구간을 설명하기 어렵다.
- **선행 접근 C — Single-cell epigenome velocity**: chromatin 데이터 단독으로 future direction 추정 시도 (refs 9, 10). 단 gene expression을 함께 모델링하지 않았다.
- **이 논문으로 이어지는 gap**: 10x Multiome, SHARE-seq, SNARE-seq처럼 *같은 cell에서 RNA와 chromatin accessibility를 동시*에 측정할 수 있게 되었으나, multi-omic 정보를 *mechanistic velocity model 안에서 함께* 해석하는 방법이 없었다 (p2).

### 기본 개념

- **RNA velocity**: unspliced pre-mRNA `u(t)`와 spliced mature mRNA `s(t)`의 상대량으로 미래 transcriptional state를 예측. `du/dt = α − βu`, `ds/dt = βu − γs` 형식의 ODE.
- **Chromatin accessibility `c(t)`**: promoter·enhancer 주변 chromatin이 transcription machinery에 접근 가능한 정도. 논문은 c를 [0, 1] 범위로 정규화하고 *transcription rate가 c에 비례*한다고 가정.
- **Priming**: chromatin이 먼저 열렸으나 transcription이 시작되지 않은 시간 구간. `Δt_priming = t_i − t_o` (transcriptional induction switch time − chromatin opening switch time).
- **Decoupling**: chromatin closing과 transcriptional repression이 동시에 일어나지 않아 c와 RNA가 *서로 다른 방향*으로 움직이는 구간. `Δt_decoupling = t_r − t_c`.
- **Model 1 / Model 2 / Model 0** (Methods, p14):
  - **Model 1 (delayed transcriptional repression)**: chromatin closing이 transcriptional repression보다 먼저 시작.
  - **Model 2 (delayed chromatin repression)**: transcriptional repression이 먼저 시작, chromatin closing이 뒤따름.
  - **Model 0**: chromatin closing 후 *늦게* 다시 transcription 시작 — biologically implausible로 default disabled.
- **4 cell-gene states**: primed (red) → coupled on (orange) → decoupled (green) → coupled off (blue).

### 이 논문이 필요성

- **핵심 이유**: multi-omic snapshot에는 epigenome ↔ transcriptome의 *시간차*가 들어 있지만, 기존 RNA-only velocity는 이를 *독립적인 regulatory signal*로 활용하지 못했다.
- **기존 방법으로 부족했던 지점**: RNA-only phase portrait에서는 RNA가 거의 없는 cell들이 원점 부근에 몰려 *cell ordering*이 불명확해진다. chromatin accessibility는 RNA보다 먼저 변할 수 있어 *early differentiation state*를 더 잘 분리할 수 있다 (Results, p4–5).
- **이 논문이 해결하려는 방향**: chromatin accessibility `c`, unspliced RNA `u`, spliced RNA `s`를 *하나의 ODE system*으로 묶어 cell latent time, gene-specific switch time, rate parameter, state assignment를 *동시에 추정*한다.

---

## 2. 방법론 분석

> Adaptive depth: 본 자료는 *computational method 중심 paper*이므로 **full depth**로 작성.

### 2.1 이 method가 푸는 문제 (formal task)

- **입력**: 같은 cell에서 측정된 chromatin accessibility `c`, unspliced pre-mRNA count `u`, spliced mRNA count `s`. 10x Multiome / SHARE-seq / SNARE-seq.
- **출력**: gene별 velocity vector (`dc/dt`, `du/dt`, `ds/dt`), 각 cell의 latent time `t`와 state `k`, gene별 rate parameter (`α_c`, `α`, `β`, `γ`), switch times (`t_o`, `t_c`, `t_i`, `t_r`), 그리고 *gene별 model 1/2 또는 induction-only/repression-only/partial* 분류.
- **추정 대상**: ODE parameters θ = (`α_c`, `α^(k)`, `β`, `γ`, switch times) + 각 cell의 latent time.
- **Hidden assumption**:
  1. transcription rate ∝ chromatin accessibility (즉 c가 transcription rate의 *시간 가변 multiplier* 역할).
  2. chromatin opening/closing이 [0, 1] 범위로 *asymptotic*으로 접근 (full open → 1, full closed → 0).
  3. observed cell들은 *deterministic ODE solution* 주위에 *i.i.d. Gaussian noise*로 분포 (model likelihood).
  4. 모든 gene이 *공통의 cell-wise latent time*을 공유 (latent time normalization).

### 2.2 확률 / 통계학적 구조

#### Model family

*Probabilistic latent variable model* — deterministic 3-ODE system + Gaussian observation noise + EM-based joint inference of cell time and ODE parameters.

#### ODE system (Eqs 10–13, p13)

```
dc/dt = k_c · α_c − α_c · c(t)       (chromatin: opening k_c=1, closing k_c=0)
du/dt = α^(k) · c(t) − β · u(t)      (unspliced RNA, transcription scaled by chromatin)
ds/dt = β · u(t) − γ · s(t)          (spliced RNA, splicing→degradation)
```

- `α_c`: chromatin rate (opening rate `α_co` / closing rate `α_cc` 별도로 fit, paper에서는 notational simplicity 위해 단일 표기).
- `α^(k)`: transcription rate (induction k=1 vs repression k=0).
- `β`: splicing rate, `γ`: RNA degradation rate.
- Analytical solution (Eqs 14–16, p13): closed-form for `c(t)`, `u(t)`, `s(t)` given switch times and initial values.

#### Likelihood (Eq 18–19, p15)

`x_i = (c_i, u_i, s_i) ~ N(f(t_i, θ), σ²I)` — observations are i.i.d. Gaussian around ODE prediction with isotropic covariance.

Negative log likelihood:
```
−log L(θ) = (3/2) log(2π σ²) + (1 / 2nσ²) Σ ||x_i − f(t_i, θ)||²
```

Maximum likelihood estimation ↔ MSE minimization.

#### Inference / optimization: Expectation-Maximization

- **E-step**: 현재 ODE parameter 기준으로 각 cell의 expected latent time을 추정. 3D ODE solution을 직접 invert하기 어려우므로 *anchor point approach* — 500–1,000개 uniformly distributed anchors 만들어 *KD-tree*로 nearest anchor 찾기 (scipy KDTree, ref 49). time 범위는 0~20 hr (scVelo default 일치).
- **M-step**: 현재 cell time 추정 기준으로 ODE parameter를 *MSE 최소화*. Nelder-Mead simplex (scipy.optimize.minimize, ref 48). Block coordinate descent — c-only params → u-related → s-related 순차 업데이트.
- 수렴: 5~10 iterations이 대부분 충분 (Methods, p18).
- Switch time이 *순서대로* 발생하도록 (induction 먼저 → repression 나중) *switch interval*을 actual parameter로 사용. 모든 parameter가 positive면 valid model.

#### Initialization (p16–17)

- RNA params (α, β, γ, RNA switch time): scVelo steady-state model 따라 — top-quantile u 평균을 α 초기값, β=1, γ는 top-quantile (u, s)의 linear regression.
- Chromatin rate `α_c`: `−log(1 − c_high / t_cc)` 초기값. c_high = above-mean cell의 평균.
- RNA switch-on time, chromatin switch-off time: 2-hour grid search로 best MSE 조합.
- u rescale factor `a`: bimodality assumption + steady-state 식에서 유도 (Eqs 20–22, p17). `a = 1 / (s_2 − s_1)` (s가 [0,1] 정규화 후 u의 중간점 좌우의 s 값 차이).

#### Sparsity·noise·confounding 처리

- **Sparsity**: ATAC-seq 데이터의 *sparsity* 보완 — peak-to-gene aggregation (promoter + correlated distal enhancers, correlation ≥ 0.5, 10kb window) + TF-IDF normalization + WNN smoothing (Seurat V4, ref 60).
- **Noise**: nearest-neighbor smoothing (scVelo `pp.moments`, 30 PCs, 50 neighbors).
- **Cell cycle confound** (HSPC dataset에서만): G2M / S phase score를 `scanpy.pp.regress_out`으로 RNA expression에서 제거. unspliced·spliced는 변경 안 함 (Methods p24, Extended Data Fig 2b).
- **Batch effect** (HSPC day0+day7, human brain dc2r2): Seurat `FindIntegrationAnchors` + `IntegrateData`로 통합. 또는 batch가 심한 sample은 제거 (human brain의 3번째 sample).

### 2.3 핵심 method insight

- **기존 방법의 한계**: scVelo dynamical model은 *transcription rate α가 induction phase 동안 시간 invariant*라고 가정. chromatin의 영향을 *별도 layer*가 아닌 *constant*로 흡수.
- **이 논문의 바꾼 가정**: transcription rate = `α^(k) · c(t)` — chromatin accessibility가 *시간 가변 multiplier*. 따라서 같은 transcription "induction" 상태 안에서도 chromatin이 변하면 effective transcription rate가 변한다.
- **새로 추가한 변수**: 
  1. `c(t)` 자체가 ODE에 명시적으로 들어옴 (이전엔 외부 covariate).
  2. `k_c` (chromatin opening/closing state) 분리.
  3. switch times `t_o`, `t_c`, `t_i`, `t_r`로 *event ordering* 명시.
- **중요성**: chromatin과 RNA의 *시간차*(priming, decoupling)를 *quantitative interval*로 추정 가능. 이전엔 정성적 관찰에 그쳤다.

### 2.4 이전 방법과의 차이

- **Baseline**: scVelo dynamical model (Bergen et al., ref 7).
- **공통점**: 
  - dynamical ODE framework, EM-based parameter estimation, latent time inference.
  - α / β / γ rate parameters.
- **차이점**:
  - ODE가 *2개 → 3개* (c 추가).
  - transcription rate `α → α · c(t)` (chromatin multiplier).
  - state 수 *2개 (induction/repression) → 4개* (primed / coupled-on / decoupled / coupled-off).
  - *Model 1 vs Model 2 분류* — chromatin closing이 transcriptional repression보다 *먼저인지 나중인지*.
  - Stochastic version: chromatin "breathing" (open/closed 빠른 switching) Markov model 추가 (refs 51–52).
- **차이가 크게 나타나는 조건**:
  - *early stem/progenitor cell*처럼 epigenomic change가 빠른 상황 → 가장 큰 개선.
  - RNA가 거의 없는 *early induction cell*들이 phase portrait 원점 근처에 몰려있는 경우 → chromatin이 ordering 보조.
  - *partial trajectory genes* (induction-only or repression-only)도 본문에서 비중 큼.

### 2.5 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: embryonic mouse brain E18 (10x Multiome), SHARE-seq mouse hair follicle, human HSPC (10x Multiome day0+day7), fetal human cerebral cortex (10x Multiome).
- **Metric**: cell fate prediction accuracy (velocity stream consistency), Spearman correlation with Palantir pseudotime, decoupling LRT p-value, GO enrichment, runtime.
- **개선된 결과**:
  - SHARE-seq 피부: Spearman with Palantir — **MultiVelo 0.51 vs scVelo 0.44** (p7).
  - scVelo가 *biologically implausible backflow*를 생성한 dataset (mouse brain upper layer neurons, fetal brain IPCs/upper layer)에서 MultiVelo가 정상 방향 추정.
  - Mouse brain: 426 genes high-likelihood fit.
  - HSPC: 11,605 cells, 1,000 genes.
  - Human brain: 4,693 cells, 919 genes.
- **Ablation 근거**:
  - 동일 ODE에서 chromatin을 *constant 1*로 두면 RNA-only model로 환원 가능 → 같은 framework 안에서 chromatin 효과만 toggling.
  - Likelihood ratio test (LRT) for decoupling: chromatin fit likelihood 기준 χ² test (1 df). null = decoupling interval 없음. 본문은 *significant decoupling genes*에 한해 LRT 결과 해석.
- **정성적 효과**: 
  - Mouse brain의 *Eomes*, *Tle4* (IPC, deep-layer neuron markers) — chromatin이 RNA보다 먼저 변해 *gradual progression* 시각화 가능.
  - SHARE-seq *Wnt3* — DTW로 측정한 *c-s delay 최대 0.6* (total time range 1).
  - HSPC *AZU1* (GMP), *HBD* (erythroid), *LYZ* (DC progenitor), *PF4* (megakaryocyte) — terminal marker 모두 chromatin priming pattern.

### 2.6 Method 관점의 한계

- **약한 assumption**: 
  - transcription rate가 c에 *정확히 비례* — 실제로는 TF binding, polymerase recruitment 등 다른 layer의 영향이 흡수됨.
  - Gaussian i.i.d. residual — 실제 single-cell data는 *count-based*, *over-dispersed* (negative binomial 더 자연스러움). 단 normalized·smoothed 값 사용으로 완화.
  - 4 state ordering이 *deterministic* — 한 gene이 ordering을 *바꿀 수* 없음 (e.g., 같은 gene이 일부 cell type에선 Model 1, 다른 cell type에선 Model 2).
- **구현·학습상 부담**:
  - Runtime: mouse brain 40 min, skin 69 min, HSPC 124 min, human brain 40 min (parallel, Intel i7-9750H 12 thread, Methods p22).
  - Memory: 857 MiB ~ 2,921 MiB peak.
  - ATAC preprocessing pipeline 의존성: Seurat·Signac·scanpy·scVelo·Velocyto·LIGER (mouse skin DORC) — 환경 셋업 부담.
  - chromatin peak aggregation rules (10kb window, correlation 0.5)이 *hyperparameter* — gene별 enhancer mapping 품질에 영향.
- **일반화가 불확실한 조건**:
  - WNN smoothing은 *paired multi-omic*에 최적화 — *unpaired* (별도 scRNA + snATAC) 데이터에서는 Seurat anchor로 imputed ATAC을 만들어야 하며, 결과 품질은 *paired보다 낮음* (Supplementary Fig 1).
  - Bulk ChIP-seq처럼 *cell-type 해상도가 다른* dataset에는 직접 적용 안 됨.
  - 본문은 *fast differentiation*에 강조 — slow turnover (성숙 organ, post-mitotic) 환경에선 priming/decoupling interval이 짧아 검출 약할 수 있음 (`해석:` 본문에 명시 안 됨).

---

## 3. 주요 결과

### Dataset 1 — Embryonic mouse brain (E18 10x Multiome)

- **Dataset**: ~3,365 cells (filtering 후), 936 highly variable genes. Cell types: radial glia (RG), IPC, neurons (upper/deep layer), astrocytes, oligodendrocytes. Interneurons·Cajal-Retzius·microglia 제외 (non-differentiating).
- **사용한 데이터 규모**: n = 3,365 cells, 936 genes input → 426 genes fit with high likelihood.
- **Baseline / 비교 대상**: scVelo (RNA-only).
- **Metric**: velocity vector consistency, cell fate accuracy (visual), Wilcoxon rank-sum for gene properties, GO enrichment.
- **주요 수치**:
  - Model 1 vs Model 2 genes의 expression/accessibility level 차이: Wilcoxon P = 0.38, P = 0.32 (not significantly different).
  - M2 genes가 latent time에서 *더 일찍* 최대 spliced expression 도달: **P = 9 × 10⁻⁷** (Wilcoxon rank-sum one-sided).
  - Gene type 분포: 29.5% induction-only, 2.4% repression-only, 41.4% model 1 (complete), 26.7% model 2 (complete).
  - Median primed interval = 21% of total time, median decoupled interval = 19%.
  - Chromatin opening rate (α_co) ≈ chromatin closing rate (α_cc): median ratio ≈ 1.
- **정성 결과**:
  - scVelo는 upper layer neuron에서 *biologically implausible backflow* 생성, MultiVelo는 RG → IPC → 상위층/심층 progression 정상.
  - Eomes, Tle4: RNA-only로는 phase portrait 원점에 몰려 ordering 불가, chromatin이 *gradual changes* 보여줌.
  - Model 1 gene example: Satb2 (induction phase에서 최대 c). Model 2 example: Gria2 (repression phase에서 최대 c).
- **GO enrichment**: M2 genes가 *cell cycle 관련 term* ('positive regulation of cell cycle', 'mitotic cell cycle', 'regulation of cell cycle phase transition')에 유의하게 enriched. `해석:` M2가 *rapid transient activation* 유전자에 적합, M1은 *stably expressed* 유전자.
- **논문 주장과의 연결**: chromatin 통합이 RNA-only model의 *backflow·ordering 문제*를 해결. M1/M2 분류는 *생물학적으로 의미 있는 차이*를 반영.

### Dataset 2 — SHARE-seq mouse hair follicle

- **Dataset**: GSE140203. TAC (transit-amplifying cell) → IRS (inner root sheath), medulla, hair shaft cuticle/cortex.
- **사용한 데이터 규모**: 6,436 cells, 962 genes. Spearman comparison: likelihood > 0.07 (140 high-quality velocity genes).
- **Baseline / 비교 대상**: scVelo, Palantir (ref 4) pseudotime.
- **Metric**: Spearman correlation with Palantir.
- **주요 수치**:
  - **MultiVelo Spearman = 0.51 (vs Palantir)**, **scVelo Spearman = 0.44**. → MultiVelo 우위.
  - Wnt3 (paracrine signal, hair growth)의 c-s DTW delay 최대 = **0.6** (total time range 1).
- **정성 결과**:
  - scVelo는 *방향을 잡지 못함* (hair shaft differentiation을 RNA만으론 capture 못 함).
  - MultiVelo는 *TAC을 root*로 정확히 식별, IRS·hair shaft 분기 capture.
  - SHARE-seq 원논문(ref 9)에서 정의한 *"chromatin potential"* (chromatin이 RNA보다 먼저 변하는 gene) 현상을 MultiVelo의 priming interval로 *정량화* 가능.
  - Mouse brain 대비 *induction-only gene이 더 많고 model 2가 더 적음*.
- **논문 주장과의 연결**: 다른 dataset (skin)에서도 일관된 chromatin-RNA lag 정량화 가능 → *generalizability 일부 입증*.

### Dataset 3 — Human HSPCs (10x Multiome, in-house)

- **Dataset**: Fred Hutch Hematology Core B 구매 CD34+ cells, single donor, 10x Multiome (day 0 fresh, day 7 expansion). Cell types: HSC, MPP, LMPP, GMP, MEP, granulocyte, erythrocyte, DC, platelet.
- **사용한 데이터 규모**: 11,605 high-quality cells, 1,000 genes (joint filtering 후).
- **Baseline / 비교 대상**: scVelo, prior HSPC marker genes (refs 37–40, 63–67).
- **Metric**: velocity stream visual consistency, GO enrichment, ChIP-seq H3K4me3/H3K4me1/H3K27ac comparison, Wilcoxon rank-sum.
- **주요 수치**:
  - Model 2 genes가 *cell cycle GO term*에 enriched: 'regulation of mitotic cell cycle', 'regulation of mitotic metaphase/anaphase transition', 'regulation of mitotic sister chromatid separation' 모두 **FDR < 0.002**.
  - Lineage marker priming examples: AZU1 (GMP), HBD (erythrocyte), LYZ (DC progenitor), PF4 (megakaryocyte direction).
  - Bulk ChIP-seq (CD34+ HSPC, GSE70677, ref 69): M1 vs M2 gene 간 Wilcoxon rank-sum (one-sided) — *Supp Notes p4 기준 (본문 Extended Data Fig 2c의 정량 수치)*:
    - **H3K4me3** (active promoter mark): **p = 0.016** → Model 2 genes에서 신호 더 큼.
    - **H3K4me1** (primed enhancer mark): **p = 0.097** → Model 1 genes에서 약간 더 (marginal).
    - **H3K27ac** (active enhancer mark): **p = 0.48** → 차이 없음.
    - `해석:` M2 gene이 active promoter mark에서 우세, M1이 primed enhancer에서 우세 — *M1은 chromatin이 RNA보다 먼저 변하는 priming 시나리오와 일치* (enhancer pre-priming).
- **정성 결과**:
  - HSPC 분화 hierarchy를 RNA-only model로는 capture 어렵다 (ref 41).
  - MultiVelo는 *local consistency*와 *biological accuracy* 개선.
  - 두 sample (day 0 + day 7) 통합 시 Seurat anchor로 batch effect 제거, velocity는 day 0 stem → day 7 differentiated 방향 (Extended Data Fig 2d).
- **논문 주장과의 연결**: 본인 (저자) lab에서 *직접 생성한 dataset*. 추가 validation strength.

### Dataset 4 — Fetal human cerebral cortex (10x Multiome, public)

- **Dataset**: 외부 paper의 10x Multiome dataset (ref 43, dc2r2_r1 + dc2r2_r2). 3번째 sample은 batch effect로 제외.
- **사용한 데이터 규모**: 4,693 cells, 919 genes. Cluster rename: RG → RG/Astro, nIPC/GluN1 → nIPC/ExN, GluN3 → ExM, GluN2 → ExUp, GluN4/5 → ExDp.
- **Baseline / 비교 대상**: scVelo, ChIP-seq validated TF-target pairs (refs 72–75).
- **Metric**: velocity consistency, DTW (TF-target, SNP-gene), motif accessibility (chromVAR + JASPAR2020).
- **주요 수치**:
  - Mental/behavioral disorder SNPs (EFO_0000677): **6,968 SNPs** → consensus peak overlap subset = **757 SNPs** → 3 major groups by max accessibility timing relative to linked gene expression.
  - TF-motif DTW: median time lag *positive* (TF expression이 binding site accessibility보다 먼저). Validated 30 motifs from JASPAR2020.
  - HSPC dataset 대비 Model 2 gene 적음 (정량 수치는 본문에 없음 — Fig 6d 참고).
- **정성 결과**:
  - MultiVelo가 RG → IPC → ExUp/ExDp 정상 progression. scVelo는 *backflow*.
  - TF-target gene expression DTW (EGR1, EOMES, FOXP2, PBX3 + literature ChIP-validated targets): TF가 target보다 먼저 발현 (Extended Data Fig 3e).
- **논문 주장과의 연결**: *TF-binding site lag*, *SNP-linked gene lag*까지 확장 가능 → MultiVelo가 단순 single-gene dynamics를 넘어 *regulatory network 시간 구조*를 분석할 수 있음.

### 전체 결과 요약

- **반복적으로 관찰된 patterns**:
  - chromatin이 RNA보다 *먼저* 변하는 *priming* 현상이 4 dataset 모두에서 관찰.
  - Model 1 (delayed transcriptional repression)이 Model 2보다 더 흔함 (mouse brain 41.4% vs 26.7%, HSPC 비슷한 추세).
  - Model 2 gene은 *cell cycle 관련 enriched* (mouse brain + HSPC 일관).
- **가장 중요한 수치**:
  - SHARE-seq Spearman 0.51 vs 0.44 — *유일하게 직접 비교된 정량 metric*.
  - Mouse brain M2 latent time 우위 P = 9 × 10⁻⁷.
  - HSPC GO enrichment FDR < 0.002.
- **Baseline 대비 차이**: 모든 dataset에서 RNA-only scVelo가 *backflow / wrong direction*을 보인 영역을 MultiVelo가 교정. 단 *정량 metric 직접 비교는 mouse skin이 유일*.
- **결과 해석 시 주의점**:
  - `해석:` 1 vs 1 Spearman 비교 (0.51 vs 0.44)만으론 *작은 sample (단일 dataset)*. 다른 dataset에선 *visual consistency* 위주.
  - `검토필요:` ChIP-seq H3K* comparison의 P-value가 본문 텍스트에 없음 — Extended Data Fig 2c 직접 확인 필요.
  - `해석:` Model 1/2 비율 차이가 *cell type 차이* 때문인지 *gene 분포 차이* 때문인지 명확히 분리되지 않음.

---

## 4. Figure 분석

### Figure 1 — Model overview

- **이 Figure가 필요한 이유**: MultiVelo가 단순 *feature 추가 모델*이 아니라 chromatin-RNA *event ordering*을 explicit하게 모델링한다는 점을 정의하기 위함.
- **이 Figure가 뒷받침하는 주장**: gene expression은 chromatin opening / transcription induction / chromatin closing / transcription repression의 시간차로 구성되며, 이 시간차로 priming, decoupling, Model 1/2를 구분할 수 있다.

##### 패널별 설명 (본문 언급 기반, p3–4)
- **a**: 3-ODE system 도식 — chromatin (c), unspliced (u), spliced (s) 변수 + rate parameters (α_co, α_cc, α, β, γ).
- **b**: Model 1 vs Model 2의 event ordering 도식.
- **c**: Priming phase 정의 — c는 양수지만 u, s = 0 구간.
- **d**: Decoupling phase 정의 — c와 RNA가 *반대 방향*.
- **e**: 4 cell-gene states (primed=red, coupled-on=orange, decoupled=green, coupled-off=blue).
- **f**: Model 1 gene의 phase portrait (max accessibility가 induction phase).
- **g**: Model 2 gene의 phase portrait (max accessibility가 repression phase).

##### 본문 강조 비교
- M1 vs M2의 phase portrait 차이가 *RNA-only로는 구분 불가능*. chromatin 정보가 *필수*.

##### 해석 시 주의점
- Figure 1은 *개념 도식* + *실제 fit 예시* 혼합. 도식 부분은 *idealized*이며 실제 데이터는 noise 큼.

### Figure 2 — Embryonic mouse brain results

- **이 Figure가 필요한 이유**: MultiVelo의 첫 dataset 적용 결과. RNA-only model의 backflow 문제를 해결한다는 주장 검증.
- **이 Figure가 뒷받침하는 주장**: chromatin 통합이 cell fate prediction 정확도와 trajectory 일관성을 개선한다.

##### 패널별 설명
- **a**: MultiVelo vs scVelo velocity stream (UMAP). MultiVelo가 RG → 상위층/심층 정상 방향.
- **b**: scVelo의 *biologically implausible backflow* — upper layer neuron 안에서.
- **c**: Cell cycle score map — cycling population이 RG 근처 (latent time 시작).
- **d**: Eomes / Tle4 phase portrait. RNA-only로는 점들이 원점에 몰려 ordering 불가.
- **e**: M1 (Satb2) vs M2 (Gria2) phase portrait 비교 — max chromatin이 induction(M1) vs repression(M2) phase.
- **f**: Pairwise phase portraits (c, u), (c, s) 추가.
- **g**: M1 vs M2의 *spliced expression peak timing* — M2가 earlier (P = 9 × 10⁻⁷).
- **h**: Gene class 분포 (induction-only 29.5%, repression-only 2.4%, M1 41.4%, M2 26.7%).
- **i**: 3D trajectory fit examples.

##### 본문 강조 비교
- scVelo vs MultiVelo의 *방향 차이*가 핵심 (a, b).
- M1 vs M2 *timing 차이* 통계적 입증 (g, p-value).

##### 해석 시 주의점
- `해석:` "Biologically implausible backflow" 판정 기준이 *cortical inside-out development* 외부 지식에 의존 — *작자 해석*임을 명확히.
- `질문:` Figure 2h의 percentage 합계가 100%가 안 됨 (29.5+2.4+41.4+26.7 = 100%). 검산 OK.

### Figure 3 — Embryonic mouse brain priming/decoupling

- **이 Figure가 필요한 이유**: 4 cell-gene states가 *실제 데이터에서 식별 가능*하다는 주장 검증.
- **이 Figure가 뒷받침하는 주장**: MultiVelo는 *gene별 priming, coupling, decoupling phase*를 정확히 capture한다.

##### 패널별 설명
- **a**: 4 state example genes — Grin2b (induction-only, primed+coupled-on), Nfix (model 1, 4 states 모두), Epha5 (model 2, coupled-on + decoupled만).
- **b**: UMAP c vs u 색상 비교 — coupled state에서 색 일치, primed/decoupled에서 *불일치*. 예: Robo2 (M1) decoupled region, Gria2 (M2) decoupled, Grin2b priming.
- **c**: c(t), u(t), s(t) plot along latent time per gene. Robo2 *2 inflection points*, Gria2 *opposite direction*, Grin2b *long priming*.
- **d**: 동일 latent time에서 cell당 *high-likelihood gene state 분포* — cascade transition 확인.
- **e**: 4 state의 *time interval 비율* — coupled phases > primed + decoupled.
- **f**: α_cc / α_co ratio = 1 (chromatin opening ≈ closing rate).

##### 본문 강조 비교
- State 정의가 *visual하게 검증 가능*함을 보임 (b의 UMAP 색 비교).
- *Cascade pattern* (d) — multiple genes가 동시에 priming 또는 decoupling 상태.

##### 해석 시 주의점
- `해석:` UMAP 색 비교(b)는 *qualitative*. 정량 metric은 c, u 간 correlation 등 별도 필요.

### Figure 4 — SHARE-seq mouse hair follicle

- **이 Figure가 필요한 이유**: 다른 dataset (SHARE-seq, mouse skin)에서도 MultiVelo가 작동하며 Palantir pseudotime과 *정량 비교* 가능.
- **이 Figure가 뒷받침하는 주장**: SHARE-seq paper(ref 9)의 *chromatin potential* 현상을 *quantitative priming interval*로 정량화 가능.

##### 패널별 설명
- **a**: MultiVelo velocity stream — TAC → IRS/hair shaft 방향.
- **b**: scVelo failure — direction 부정확.
- **c**: Gene class 분포 (induction-only 더 많음, M2 더 적음, mouse brain 대비).
- **d**: Wnt3 priming 시각화 — c, u, s UMAP 색이 *명확한 time delay*.
- **e**: SHARE-seq paper의 chromatin potential gene들 (Wnt3, Dsc1, Cux1, Dlx3, Cobll1) priming/decoupling fit.
- **f**: DTW alignment — c vs s, u vs s. c-s delay > u-s delay (chromatin이 더 앞섬). c-s 최대 delay 0.6.

##### 본문 강조 비교
- MultiVelo의 *quantitative time lag* (DTW + priming interval)이 ref 9의 *qualitative chromatin potential*을 *수치화*.

##### 해석 시 주의점
- DTW alignment는 *aggregation bin*에 의존 (20 bins). bin 수 변경 시 결과 변동 가능.

### Figure 5 — Human HSPCs

- **이 Figure가 필요한 이유**: 본인 lab dataset (HSPC)에서 *blood differentiation*에 MultiVelo 적용.
- **이 Figure가 뒷받침하는 주장**: chromatin integration이 *RNA-only model이 어려워하는 blood cell differentiation*에 도움.

##### 패널별 설명
- **a**: MultiVelo vs RNA-only velocity stream on HSPC UMAP. MultiVelo가 *local consistency*↑.
- **b**: Gene class 분포 (mouse brain 패턴과 유사 — M1 다수).
- **c**: Primed/decoupled interval *길이*가 coupled phase보다 짧음.
- **d**: Model 2 marker examples (G2/M phase markers) — chromatin이 expression drop 후에도 계속 accessibility 상승.
- **e**: Lineage-specific marker priming — AZU1 (myeloid), HBD (erythroid), LYZ (DC), PF4 (megakaryocyte).
- **f**: Velocity magnitude plot — stem cell population에서 velocity 높고, differentiated cell에서 낮음 (zero velocity 근처).
- **g**: Local chromatin/RNA trends per lineage.

##### 본문 강조 비교
- *Mouse brain과의 패턴 일관성* (b, c) — *common underlying biology* 시사.
- HSPC의 lineage 별 *priming* (e) — terminal marker가 *발현 전부터 chromatin priming* 됨.

### Figure 6 — Fetal human cerebral cortex

- **이 Figure가 필요한 이유**: 4번째 dataset 적용 + TF/SNP latent time 분석 *확장*.
- **이 Figure가 뒷받침하는 주장**: MultiVelo latent time이 *TF-target lag*, *SNP-gene lag* 분석에도 활용 가능 → regulatory network 시간 구조.

##### 패널별 설명
- **a**: MultiVelo velocity stream — RG → IPC → ExUp/ExDp.
- **b**: scVelo의 backflow (IPC, upper layer neuron).
- **c**: M1/M2 gene examples.
- **d**: Mouse brain 대비 *model 2 gene 적음*.
- **e**: TF-binding site DTW alignment example.
- **f**: TF motif accessibility along latent time. 모든 TF의 median lag *positive* (TF 발현이 motif accessibility보다 먼저).
- **g**: Disease SNP analysis — max accessibility timing이 linked gene expression의 early/late인지에 따라 3 group.

##### 본문 강조 비교
- *TF가 binding site 열림보다 먼저* — counterintuitive (`해석:` 본문은 post-transcriptional regulation, chromatin remodeling complex activity, intercellular signaling을 가설로 제시).
- SNP 그룹화 — disease variant의 *developmental window* 정보 추가.

##### 해석 시 주의점
- `검토필요:` TF가 binding site보다 먼저 발현된다는 결과는 *기존 mechanism (TF가 chromatin opening 유도)*과 *상반*. 본문도 mechanism은 *결론 짓지 않음*. 후속 perturbation 필요.

---

## 5. Table 분석

### Table 1 (본문 표) — 본문에 정식 Table 없음

본문 main figure 외 *Table 1*은 명시되어 있지 않음. 모든 정량 결과는 *Figure에 plot* 또는 *Supplementary Table*에 정리되어 있다 (Methods, p22 에 "Runtime and memory usage statistics in Supplementary Table 1").

### Supplementary Table 1 — Runtime & Memory

<!-- augment-table: supplementary-table-1 -->

- **목적**: Implementation efficiency 입증.
- **표 구조**:
  - Row: 3 metric (Runtime, Peak memory, Memory increment).
  - Column: 4 dataset (mouse brain, mouse skin, human HSPC, human brain).
- **본문 강조 비교**: HSPC가 *가장 무거움* (cell 수 11.6k + 1,000 genes).
- **해석 시 주의점**:
  - 하드웨어: Intel Core i7-9750H (12 threads), 32 GB RAM, Arch Linux.
  - `해석:` 12 thread 기준이므로 server-grade hardware에선 더 빠를 것. 단 memory는 CPU와 무관 — *cell × gene 수 scaling* 주의.

### Other Supplementary Tables

Supp PDF (11 페이지) 확인 결과 *Supp Table 1만 존재* — 추가 Supp Table 없음.

---

## 6. Supplementary Information

> Supp Table 1은 §5 *Table 분석*에 포함. 여기서는 *Notes*와 *Figures captions*만 toggle로 정리.

::: details Supplementary Notes 요약 (펼치기)

#### S1 — Additional Background and Motivation
- 기존 RNA velocity (steady-state, velocyto package) → dynamical model (scVelo, Bergen et al., ref 7)으로 발전한 history.
- 두 방식 비교:
  - Steady-state: spliced/unspliced *ratio*만으로 induction/repression 판단. 단 transient state 약함.
  - Dynamical: ODE parameter + latent time을 joint inference. transient 포함.
- MultiVelo는 dynamical 위에 chromatin을 *시간 가변 transcription multiplier*로 추가 — mechanistic interpretation.

#### S2 — Simulation Validation
- 1,000 gene simulation: rate parameters / switch times / model 1 vs model 2 무작위 조합.
- Latent time 회복 능력 시험:
  - high-variance (5×) / low-variance (5×) noise 시나리오
  - complete : induction-only : repression-only 비율 다양화 (4:5:1 등)
- 결과: MultiVelo가 key simulation parameter 변화에 robust. complete gene 비율이 높을수록 latent time accuracy↑.

#### S3 — ChIP-seq H3K\* Analysis (HSPC)
- Bulk ChIP-seq (CD34+ HSC, GSE70677, ref 69) M1 vs M2 gene Wilcoxon rank-sum:
  - **H3K4me3** (active promoter): **p = 0.016** → M2 우세
  - **H3K4me1** (primed enhancer): **p = 0.097** → M1 약간 더
  - **H3K27ac** (active enhancer): **p = 0.48** → 차이 없음
- `해석:` M1이 primed enhancer mark에서 우세 — *chromatin이 RNA보다 먼저 변하는 priming 시나리오와 일치* (enhancer pre-priming).
- 자세한 해석은 §3 Dataset 3 부분 참고.

:::

::: details Supplementary Figures captions (펼치기)

#### Figure S1 — Unpaired RNA + ATAC 추정
- Computationally inferred multi-omic profile workflow (Seurat anchor algorithm).
- Unpaired scRNA + snATAC을 paired data로 imputation 후 MultiVelo 적용 결과.
- *한계*: IPC, V-SVZ 영역에서 arrow missing — imputation으로 priming/decoupling 정보 일부 손실.
- Root cell 예측 위치도 약간 shift.

#### Figure S2 — Stochastic ODE Model
- Chromatin "breathing" Markov process — open ↔ closed 빠른 switch.
- Transition probabilities `α_co`, `α_cc`.
- Stochastic velocity estimates (scVelo RNA-only vs MultiVelo multi-omic) phase portrait 비교.

#### Figure S3 — Simulation Latent Time Inference
- 2,000 cells, 500 genes, complete:induction:repression 비율 변화.
- High-variance (5×), Low-variance (5×) 시나리오.
- MultiVelo latent time accuracy가 시뮬레이션 파라미터 변화에 *robust*.

#### Figure S4 — Steady-state Models Comparison
- (a) MultiVelo deterministic SS
- (b) scVelo deterministic SS
- (c) MultiVelo deterministic — unspliced·spliced only (no chromatin)
- (d) MultiVelo stochastic — unspliced·spliced only
- (e) VeloAE with scVelo stochastic
- *결론*: deterministic이 stochastic보다 less stable. chromatin 없으면 MultiVelo deterministic ≈ scVelo deterministic.

#### Figure S5 — Ablation: Chromatin and Decoupling
- (a) MultiVelo *without chromatin* → mouse brain에서 backflow 일부 남음, root 예측 덜 정확.
- (b) *No M1/M2 distinction* (decoupling 없음) → cell time prediction variance 증가.
- *MultiVelo의 두 핵심 contribution (chromatin 통합 + M1/M2 decoupling) 각각의 ablation 입증*.

#### Figure S6 — Smoothing / ATAC Aggregation Methods
- WNN vs RNA-NN vs LSI-NN 비교.
- ATAC peak-to-gene aggregation 전략 비교.
- *결론*: WNN이 RNA·ATAC 정보 균형 → 본문 default.

:::

---

## 분석 자체에 대한 메모

- 본문 + Methods + Supp PDF 페이지 1~11 모두 확인 후 정리. Supp Notes의 ChIP-seq P-values는 §3 Dataset 3에 직접 반영.
- Figure caption은 본문 언급 + Extended Data Fig caption + Supp Fig caption (Notes로 toggle화).
- `검토필요:` Figure 6d의 M2 비율 수치 (본문 텍스트 미명시, Figure에서 시각 확인 필요).
- `질문:` cell cycle confound 처리 (HSPC)가 *RNA만* regress out — unspliced·spliced 그대로. unspliced에 잔여 cell cycle effect 남지 않는지 후속 검토 필요.
- `질문:` MultiVelo의 *Spearman 0.51 vs scVelo 0.44* 차이는 *통계적으로 유의*한가? 본문에 confidence interval 없음. 단일 dataset 비교의 한계.
