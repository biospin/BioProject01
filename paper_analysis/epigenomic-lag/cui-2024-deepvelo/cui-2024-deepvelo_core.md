# DeepVelo: deep learning extends RNA velocity to multi-lineage systems with cell-specific kinetics

Citation: `@cui2024deepvelo` — Cui H, Maan H, Vladoiu MC, Zhang J, Taylor MD, Wang B. *Genome Biology* 25:27 (2024). DOI: 10.1186/s13059-023-03148-9. Open Access (CC BY 4.0).

## Executive Summary

- **무엇**: DeepVelo는 기존 RNA velocity (velocyto, scVelo)의 *steady-state 가정*과 *cell-agnostic constant kinetic rate 가정*을 동시에 풀고, GCN(graph convolutional network)으로 *cell- and gene-specific* transcription rate $\alpha_{i,g}$, splicing rate $\beta_{i,g}$, degradation rate $\gamma_{i,g}$를 추정해 multi-lineage / time-dependent dynamics에서도 일관된 velocity를 제공한다. RNA-only method이며 epigenome modality는 다루지 않는다 (§Background p2, §"DeepVelo model" p3).
- **모델 / 방법**: 입력 $(s_i, u_i)$ — spliced/unspliced count + 30-NN graph $G$ → GCN encoder가 layer-wise propagation $H^{(l+1)} = \sigma(\tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H^{(l)} W^{(l)})$ (Eq. 3)로 cell embedding 학습 → fully connected decoder가 $(\alpha, \beta, \gamma) \in \mathbb{R}^{N \times D}$ 출력 → velocity $\tilde{v}_i = \beta_i u_i - \gamma_i s_i$ (Eq. 4). Loss는 *continuity assumption* 기반 $L_c = L^{+} + L^{-} + L_{\mathrm{Pearson}}$ (Eq. 14) — 미래 cell state $G_{i,t+1}$를 *neighbor expression 평균*으로 surrogate해 self-supervised training. Adam, lr $0.001$, 2 hidden GCN layers (size 64), 100 epochs, Pearson term scaling $18.0$ (§"Implementation details" p24).
- **핵심 결과**:
  - ① **Dentate gyrus neurogenesis** (n=2,930 cells, GSE95753) — overall consistency: DeepVelo $0.9482$ vs scVelo dynamical $0.8009$ vs scVelo stochastic $0.8633$; celltype-wise consistency: $0.844$ vs $0.6077$ vs $0.7455$; Mann-Whitney U two-sided $p < 1.0 \times 10^{-300}$ (Fig. 2b-c, Supp Table on Direction/Consistency).
  - ② **Hindbrain GABAergic / gliogenic bifurcation** (Vladoiu 2019, GSE118068) — direction score $0.38337$ vs $0.32636$ (dynamical) vs $0.39282$ (stochastic); GABAergic marker ranking Mann-Whitney $p = 1.376 \times 10^{-7}$, $n = 245$; gliogenic NS ($p > 0.05$, $n = 131$); top driver pathway enrichment (Tfap2a/b, Lhx5, Neurod6, Hes1, Sox9), 97 GABAergic + 151 gliogenic enriched pathways for DeepVelo; Fisher exact $p = 1.407 \times 10^{-9}$ ($n_{\mathrm{scVelo}}=103$, $n_{\mathrm{DeepVelo}}=97$) for neurogenic functional enrichment (Fig. 4, Fig. 5, §p10–12).
  - ③ **Mouse mesenchymal/chondrocyte organogenesis** (MOCA, GSE119945, downsampled to 30k cells) — direction $0.28153$ vs $-0.03545$ (dynamical) vs $0.0717$ (stochastic); overall consistency $0.8986$ vs $0.7719$; multi-furcating lineage 정확 회복 (Fig. 6).
  - ④ **Mouse gastrulation** (Pijuan-Sala 2019) — direction $0.769$ vs $-0.475$ (dynamical) vs $0.018$ (stochastic) — *가장 큰 margin*; overall consistency $0.979$ vs $0.843$ vs $0.747$ (Supp Table S4, sheet "Direction Score").
  - ⑤ **Pilocytic astrocytoma (PA, n=3 patients, EGAS00001003170)** — tumor cell branches로 immunogenic vs depleted subpopulation 발견 (MHC class II, antigen presentation enriched in immunogenic; neurogenesis pathways in depleted) (Fig. 7, Supp Tables S5–S7).
  - ⑥ **Runtime**: CPU-only DeepVelo는 scVelo dynamical 대비 $4\times$ speedup; GPU 사용 시 $10$–$20\times$. Hindbrain 13,501 cells 36 seconds (§"computationally robust" p16, Supp Fig. S8).
- **우리 적용**: HSPC multiome 파이프라인의 *direct method 후보*는 아니다 — DeepVelo는 chromatin을 다루지 않는 RNA-only baseline. 우리에게는 (1) **methodology-reference**: MoFlow / MultiVeloVAE가 자신의 cell-specific kinetics rationale을 설명할 때 인용하는 *direct predecessor* — `cell-agnostic kinetic rate 가정의 문제`를 설명하는 *원문 출처*. (2) **academic-citation**: 우리 논문 introduction에서 RNA velocity 2세대 (cell-specific rate) 도입부 인용 후보. epigenetic lag 직결은 약함.
- **심층**: 한계·재현 ROI는 [`cui-2024-deepvelo_lens-academic.md`](cui-2024-deepvelo_lens-academic.md) / [`cui-2024-deepvelo_lens-industry.md`](cui-2024-deepvelo_lens-industry.md) / [`cui-2024-deepvelo_methodology-brief.md`](cui-2024-deepvelo_methodology-brief.md) 참고.

## Identity

- **Title**: DeepVelo: deep learning extends RNA velocity to multi-lineage systems with cell-specific kinetics
- **Authors**: Haotian Cui¹²³†, Hassaan Maan¹³⁴†, Maria C. Vladoiu⁵, Jiao Zhang⁶⁷, Michael D. Taylor⁶⁷⁸⁹, Bo Wang¹²³⁴¹⁰* (†co-first; *corresponding)
- **Affiliations** (선택): University of Toronto / Vector Institute / University Health Network / SickKids / Texas Children's Cancer Center / Baylor College of Medicine
- **Year / Venue**: 2024 (published 2024-01-19; received 2023-09-26; accepted 2023-12-18), *Genome Biology* 25:27
- **DOI**: 10.1186/s13059-023-03148-9
- **License**: Creative Commons Attribution 4.0 International (open access)
- **Citation key**: `cui2024deepvelo`
- **Funding**: NSERC (RGPIN-2020-06189, DGECR-2020-00294), CIFAR AI Chairs, Peter Munk Cardiac Centre AI Fund (B.W.), Canada Research Chairs.
- **COI**: Bo Wang serves on Strategic Advisory Board of Vevo Therapeutics Inc.; 다른 저자 COI 없음.
- **Code / Data**: https://github.com/bowang-lab/DeepVelo (MIT license), Zenodo DOI 10.5281/zenodo.10251639. 처리된 데이터는 Figshare 10.6084/m9.figshare.24716592.v1; raw은 GEO (GSE95753, GSE104323, GSE132188, GSE118068, GSE119945) + EGA (EGAS00001003170, controlled access).

## Background

### 배경 스토리

- **문제의 출발점**: RNA velocity (La Manno 2018, *Nature*, ref. 1)는 spliced/unspliced read 비율로 *mRNA 시간 derivative*를 추정해 single-cell trajectory의 *방향성*을 제공한다. La Manno 원 method (velocyto)는 *steady-state assumption*에 기반 — 각 gene별로 induction의 정점과 quiescent steady state가 동시에 sequencing data에 보존된다고 가정. 이후 scVelo (Bergen 2020, ref. 2)는 dynamical model로 4개 transcriptional state (induction / repression / steady-on / steady-off)를 도입해 steady-state 일부를 완화했다.
- **선행 접근 A — velocyto** (steady-state 가정): per-gene linear regression으로 steady-state ratio 추정 → velocity는 *해당 ratio에서의 deviation*. 충분한 quiescent steady state cell이 sequencing에 잡혀야 동작.
  - **A의 한계** (§p2): 두 핵심 가정 — (1) gene별로 충분한 cell이 steady state에 있다는 가정, (2) splicing/degradation rate가 *모든 cell에서 동일* (cell-agnostic). 두 가정 모두 multi-lineage system에서 깨진다.
- **선행 접근 B — scVelo dynamical** (Bergen 2020, ref. 2): steady-state 가정을 4-state dynamical model로 일반화. cyclic trajectory 가정 (induction → steady-on → repression → steady-off) + per-gene constant kinetic rate.
  - **B의 한계** (§p2): cyclic trajectory 가정이 실제 multi-lineage scRNA-seq에 거의 맞지 않음 (multifactorial kinetics; Bergen 2021 ref. 3 review). 그리고 *cell-agnostic kinetic rate*라는 두 번째 가정은 그대로 — *같은 gene이 lineage에 따라 다른 dynamics*를 보일 수 있는 multi-lineage에서 잘못된 velocity direction을 만든다.
- **선행 접근 C — multi-modal velocity 확장**: MultiVelo (Li 2023, ref. 4 — `@li2023multivelo`), Chromatin Velocity (ref. 5), protaccel (ref. 6), VeloAE (ref. 7), Dynamo (ref. 8 — metabolic labeling).
  - **C의 한계** (§p2): core velocity computation은 여전히 원 idea를 따름 → cell-agnostic kinetic rate 가정 그대로. *modality는 확장*했지만 *cell heterogeneity를 직접 풀지 않음*.
- **선행 접근 D — cellDancer** (Li 2023, ref. 16, Nat Biotechnol; `@li2023celldancer`): cell-specific kinetic rate 시도 (DeepVelo와 *동시기 preprint*). DNN으로 $(u,s) \to (\alpha, \beta, \gamma)$ mapping + cosine similarity loss.
  - **D의 한계 (저자가 본문에서 직접 비교)** (§p5): direction score에서 cellDancer가 *4개 method 중 최악* (특히 multi-lineage hindbrain·chondrocyte); consistency는 높지만 *direction*이 약해 over-smoothed estimation으로 진단됨 (Supp Fig. S1, Supp Note S3). DeepVelo는 *direction 우위*로 차별화.
- **이 논문으로 이어지는 gap**: complex multi-lineage system에서 *cell-specific kinetics*가 필요한 것은 합의되어 가나, (1) cell-specific 가정을 *제대로 학습할 architecture*가 없고 (cellDancer는 direction 약함), (2) *predefined cyclic kinetic pattern에 묶이지 않는 loss*가 없다. DeepVelo는 GCN + *continuity assumption* 기반 self-supervised loss로 이 두 gap을 동시에 푼다.

### 기본 개념

- **RNA velocity**: spliced mRNA의 시간 derivative $v = ds/dt$. unspliced $u$와 spliced $s$의 *상대 비율 변화*로 *유전자별 induction/repression direction*을 추정.
- **Transcriptional kinetic rates** $(\alpha, \beta, \gamma)$:
  - $\alpha$: transcription rate (DNA → unspliced pre-mRNA)
  - $\beta$: splicing rate (unspliced → spliced)
  - $\gamma$: degradation rate (spliced → degraded)
  - 기본 ODE (Eq. 1): $du/dt = \alpha - \beta u$, $ds/dt = \beta u - \gamma s$.
- **Cell-agnostic vs cell-specific rate**: 종전 method는 *모든 cell에서 동일한* $(\alpha_g, \beta_g, \gamma_g)$ — gene-only specific. DeepVelo는 $(\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g})$ — *cell $i$ × gene $g$* 모두에 specific.
- **Graph convolutional network (GCN)**: 각 cell node가 *spliced+unspliced expression vector* $v_i = [s_i, u_i]$를 feature로 가지고, 30-NN graph 위에서 layer-wise message passing $H^{(l+1)} = \sigma(\tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H^{(l)} W^{(l)})$로 *neighborhood-aware* embedding 학습. *single cell만의 noisy count*에서 smoothened representation 추출.
- **Continuity assumption**: sequencing data가 *consecutive differentiation stage의 연속 스펙트럼*을 capture 한다는 가정. cell $i$의 *미래 stage* $G_{i,t+1}$은 *현재 sequencing population 안에 있는 neighbor cell의 expected expression*과 같다는 가정 — destructive sequencing이라 직접 $t+1$ 관측은 불가하므로 *neighbor surrogate* 필요 (Eq. 7).
- **Direction score / Consistency score**: DeepVelo가 도입·차용한 평가 지표.
  - *Overall consistency*: cell의 velocity가 *30-NN 이웃 velocity*와 평균 cosine similarity.
  - *Cell-type-wise consistency*: 같은 cell type 안 모든 cell의 velocity와 cosine similarity — *over-smoothing bias 보정*.
  - *Direction score*: 사전 annotated cell-type pair $(A, B)$의 boundary cell에서, velocity가 $A \to B$ 방향과 얼마나 align되는지 (VeloAE의 CBDir 변형, Eq. 18–20).

### 이 논문이 필요성

- **핵심 이유**: scRNA-seq dataset의 *58%* gene이 multi-faceted kinetics를 보임 (Supp Fig. S3) — *cell-agnostic kinetic rate* 가정은 평균적으로도 부적합.
- **기존 방법으로 부족했던 지점**: velocyto·scVelo는 cell-agnostic rate로 *multi-lineage에서 velocity 방향이 역전*. cellDancer는 cell-specific 시도했지만 *direction이 떨어지고 over-smoothed*. 어느 method도 *time-dependent kinetics (degradation rate가 시간에 따라 변하는 simulation)에서 correct direction*을 회복하지 못함.
- **이 논문이 해결하려는 방향**: (1) GCN으로 *cell-specific kinetic rate*를 *neighborhood-aware*하게 학습 — single cell noise 완화. (2) *continuity assumption* 기반 self-supervised loss — predefined cyclic pattern에 의존하지 않음. (3) consistency 외 *direction score*를 evaluation에 추가 — over-smoothing detection.

## Methods

### 이 method가 푸는 문제

- **Formal task**: scRNA-seq의 spliced/unspliced count로부터 *cell-specific*, *gene-specific* RNA velocity 추정.
- **입력**: spliced count $s_i \in \mathbb{R}^{D}$ + unspliced count $u_i \in \mathbb{R}^{D}$ for each cell $i \in \Omega$ (population). $D$ = highly variable gene 수 (default $2000$ or $3000$).
- **출력**: per-cell-per-gene kinetic rates $\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g} \in \mathbb{R}^{N \times D}$, velocity vector $\tilde{v}_i \in \mathbb{R}^{D}$ (Eq. 4: $\tilde{v}_i = \beta_i u_i - \gamma_i s_i$).
- **추정 대상**: 위 kinetic rates의 *cell-specific* 함수 (neural network parameter $\theta$).
- **중요한 hidden assumption**: *continuity assumption* (Eq. 7) — 충분히 dense하게 sampled cell population이라면 cell $i$의 미래 $t+1$ state $G_{i,t+1}$의 expected expression은 *현재 sequencing population 안의 적절한 neighbor 집합* $N_{i,t+1}$의 expected expression과 같다. 즉 $G_{i,t+1} = \mathbb{E}_{P(i \to j)}[G_{j,\tau(j)}]$ for $j \in N_{i,t+1}$. self-supervised이고 cell-type annotation 불필요.

### 확률 / 통계학적 구조

- **Model family**: deterministic discriminative deep neural network (변분 prior 없음, 확률적 sampling 없음). cellDancer 계열의 *discriminative* 구조에 *graph convolution + continuity loss*를 추가.
- **Likelihood / objective**: 명시적 likelihood 없음. *continuity equation* (Eq. 10):
  $$\frac{1}{|\Omega|} \sum_{i \in \Omega} \Big[ s_i + v_i - \sum_{j \in N_{i,t+1}} s_j P(i \to j) \Big] \approx 0$$
  의 squared difference를 minimize. 실제 학습 loss (Eq. 14):
  $$L^{+} = \frac{1}{|\Omega|} \sum_i \Big\| s_i + \tilde{v}_i - \sum_{j \in \tilde{N}_i} s_j P_{c+}(i \to j) \Big\|^2$$
  $$L^{-} = \frac{1}{|\Omega|} \sum_i \Big\| s_i - \tilde{v}_i - \sum_{j \in \tilde{N}_i} s_j P_{c-}(i \leftarrow j) \Big\|^2$$
  $$L_{\mathrm{Pearson}} = -[\eta_u \mathrm{corr}(\tilde{v}_i, u_i) + \eta_s \mathrm{corr}(\tilde{v}_i, -s_i)]$$
  $$L_c = L^{+} + L^{-} + L_{\mathrm{Pearson}}$$
  - $L^{+}$: forward continuity ($t \to t+1$).
  - $L^{-}$: backward continuity ($t \to t-1$) — *방향 모호성* 해결 위해 추가 (forward만 쓰면 $\tilde{v}_i$와 $-\tilde{v}_i$가 *symmetric*).
  - $L_{\mathrm{Pearson}}$: $v$가 $u$와 positive correlation, $s$와 negative correlation을 가져야 한다는 *direction-fixing heuristic* (Eq. 1 derivation; Note S4). $\eta_s = 18.0$ default — 다른 두 항에 비해 크게 weight.
- **Prior / regularization**: explicit prior 없음. dropout $0.2$ (hidden layer 간) + GCN의 *implicit regularization* (neighborhood smoothing).
- **Latent variable / hidden state**: GCN hidden state $H^{(l)} \in \mathbb{R}^{N \times d_l}$ ($d_l = 64$ for 2 layers default). 명시적 latent variable distribution 없음 — *embedding* 수준의 deterministic representation.
- **Inference / optimization**: full-batch (batch size = $N$ cells) Adam (Kingma 2014, ref. 40), lr $0.001$, AMSGrad, weight decay $0$, lr decay $\gamma=0.97$ per epoch, 100 epochs.
- **Noise, sparsity, uncertainty 처리**:
  - Noise/sparsity: GCN neighborhood averaging (30-NN graph) + preprocessing 시 30-NN smoothing (scVelo `scv.pp.moments`).
  - Uncertainty: posterior 없음. 대신 *continuity score* $CS\text{-}\mathrm{cell}_i = 1 - \frac{1}{M}\sum_g \tanh(\epsilon^{(\mathrm{con})}_{i,g})$ (Eq. 16)와 *CS-gene* (Eq. 17)을 *confidence proxy*로 제공. 또 *correlation score* (학습 후 actual Pearson $\mathrm{corr}(\tilde{v}, u)$, $\mathrm{corr}(\tilde{v}, -s)$).
  - Missingness: 명시 처리 없음. scVelo 표준 preprocessing 사용 (filter_and_normalize default).
- **Direction probability** (Eq. 12): cell $i$의 forward target 후보 cell $j$ 선택은 *cosine similarity* heuristic
  $$P_{c+}(i \to j) = \begin{cases} 1/Z & \text{if } S_{\cos}(s_j - s_i, \tilde{v}_i) > 0 \text{ and } j \in N_i, \\ 0 & \text{otherwise} \end{cases}$$
  $Z$는 condition 만족하는 neighbor 수. $K_c = 30$ neighbor를 cell $i$의 PCA-30 space에서 Euclidean distance로 미리 선정.

### 핵심 method insight

- **기존 방법의 한계**:
  - velocyto/scVelo는 *single cell만의 noisy $(u, s)$*에서 *gene-specific constant rate*를 fit → cell heterogeneity 손실 + multi-lineage에서 방향 역전.
  - cellDancer는 cell-specific 시도하지만 *neighbor information을 cosine similarity loss로 약하게*만 사용 → over-smoothing + direction 떨어짐.
- **이 논문의 바꾼 가정**: (1) cell의 *neighborhood*를 *GCN message passing*으로 explicit하게 input feature에 통합 → single-cell noise를 *embedding 수준*에서 완화. (2) *continuity assumption* — *predefined cyclic pattern*과 *steady-state* 가정 둘 다 *대체*. 두 assumption의 *상위* 가정으로 작용 (Note S2에서 *기존 가정 → continuity 가정*이 implication된다고 증명).
- **새로 추가한 변수 또는 구조**: cell-specific kinetic rate $(\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g})$를 GCN output으로 *학습 가능 parameter*화. 또 *continuity score*를 *confidence measure*로 제공 (post hoc).
- **이 변화가 중요한 이유**:
  - *Theoretical*: continuity가 *steady-state·dynamical scVelo 가정의 superset*이라는 증명 (Note S2.1–2.5) — *기존 method가 동작하는 모든 시나리오에서 DeepVelo도 동작 + 더 일반화된 시나리오 추가*.
  - *Empirical*: multi-lineage에서 cell-specific rate가 *Tmsb10 같은 multifaceted gene을 phase portrait 한 panel에 두 trajectory로 분리* (Fig. 3a-c) — gene-level cyclic 가정에서는 표현 불가.
  - *Asymptotic*: cell sample이 충분치 않을 때 continuity의 *asymptotic error*가 기존 가정의 error보다 *smaller*임을 증명 (Corollary 1, 2, Note S2).

### 이전 방법과의 차이

- **Baseline**: velocyto (La Manno 2018, ref. 1) / scVelo dynamical (Bergen 2020, ref. 2) / scVelo stochastic / cellDancer (Li 2023, ref. 16). MultiVelo·Chromatin Velocity·protaccel·VeloAE·Dynamo는 *modality 확장*으로 직접 비교 대상 아님 (cell-agnostic rate라 동일한 한계 보유한다고 본문이 주장, §p2).
- **공통점**: ODE form (Eq. 1)은 동일; preprocessing (scVelo `filter_and_normalize`, 30-NN smoothing)도 동일; velocity projection (Gaussian kernel transition probability를 UMAP/tSNE에 투영)도 scVelo 차용.
- **차이점**:
  - **Rate parameterization**: velocyto/scVelo의 $(\alpha_g, \beta_g, \gamma_g)$ ← DeepVelo의 $(\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g})$.
  - **Architecture**: velocyto = linear regression; scVelo = EM over latent state; cellDancer = per-gene DNN; DeepVelo = *cross-gene GCN* (모든 gene이 *동일 neural network*를 통과 — *gene 간 information sharing*).
  - **Loss**: velocyto = regression residual; scVelo = likelihood EM; cellDancer = cosine similarity over neighbor; DeepVelo = *forward + backward continuity + Pearson direction term*.
  - **Self-supervision**: cell-type annotation 불필요 (cellDancer와 공통, scVelo와 부분 공통).
- **차이가 크게 나타나는 조건**: multi-lineage / multi-furcating differentiation, time-dependent kinetics, multifaceted gene (cell-type 간 dynamics 다른 gene). 단일 lineage·cyclic dataset에서는 차이 작음 (예: pancreas endocrinogenesis는 direction score $0.31$ vs $0.28$ — gap $0.03$만; vs gastrulation은 $0.77$ vs $-0.47$ — gap $1.24$).

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: 6 development + 1 simulation + 3 PA tumor.
  - Dentate gyrus neurogenesis (n=2,930, GSE95753), Pancreatic endocrinogenesis (GSE132188), Hindbrain (GSE118068), Large-scale hippocampus (La Manno 2018), Mesenchymal organogenesis (GSE119945, downsampled 30k), Mouse gastrulation (Pijuan-Sala 2019).
- **Metric**: direction score, overall consistency, cell-type-wise consistency, driver gene marker overlap, pathway enrichment ratio.
- **개선된 결과** (Supp Table on Direction/Consistency, sheet "Direction Score"/"Overall Consistency"/"Celltype-wise Consistency"; 검토 시 sources/cui-2024-deepvelo-supp-5-direction-consistency.xlsx):
  | Dataset | Direction (DV / scV-dyn / scV-stoch) | Overall (DV / scV-dyn / scV-stoch) | Celltype-wise (DV / scV-dyn / scV-stoch) |
  | --- | --- | --- | --- |
  | Dentate gyrus | $0.370$ / $-0.008$ / $0.191$ | $0.948$ / $0.801$ / $0.863$ | $0.844$ / $0.608$ / $0.746$ |
  | Pancreatic endo. | $0.312$ / $0.276$ / $0.307$ | $0.904$ / $0.816$ / $0.876$ | $0.650$ / $0.510$ / $0.696$ |
  | Hindbrain | $0.383$ / $0.326$ / $0.393$ | $0.936$ / $0.871$ / $0.914$ | $0.609$ / $0.543$ / $0.593$ |
  | Large-scale DG | $0.601$ / $0.147$ / $0.347$ | $0.934$ / $0.857$ / $0.874$ | $0.713$ / $0.589$ / $0.645$ |
  | Mesenchymal organ. | $0.282$ / $-0.035$ / $0.072$ | $0.899$ / $0.772$ / $0.767$ | $0.633$ / $0.470$ / $0.492$ |
  | Mouse gastrulation | $0.769$ / $-0.475$ / $0.018$ | $0.979$ / $0.843$ / $0.747$ | $0.918$ / $0.590$ / $0.543$ |
  | Simulation | N/A | $0.997$ / $0.970$ / $0.969$ | N/A |
  - DeepVelo는 *모든 dataset에서 direction과 overall consistency 1위*. celltype-wise consistency는 pancreatic endocrinogenesis에서 scVelo stochastic ($0.696$)이 DeepVelo ($0.650$)보다 미세하게 높음 — *유일한 예외*.
- **Ablation 근거**:
  - **GCN vs FFNet** (Supp Table S9 / sources/cui-2024-deepvelo-supp-10-direction-consistency-v2.xlsx, sheet "Direction Score" sheet "GCN vs FFNet"): GCN 사용이 direction score를 dentate gyrus에서 $+0.115$, hindbrain에서 $+0.015$, large-scale hippocampus에서 $+0.11 \sim +0.35$ (Supp Note S1) — *GCN의 implicit regularization이 핵심*. 다만 small/medium dataset에서는 FFNet이 cell-type wise consistency를 더 높게 (예: dentate gyrus $+0.054$, pancreas $+0.106$) — *consistency 단독 우위*가 GCN의 direction 우위와 trade-off.
  - **Hyperparameter robustness** (Supp Note S1, $n = 5000$ random search; sources/cui-2024-deepvelo-supp-9-hp-sweep.xlsx): learning rate 0.0001–0.1, optimizer (Adam/SGD/RMSprop), GCN k 5–50, t+1 k 5–50, layer size [32,32]–[512,512], Pearson scaling $U(1, 100)$, HVG 500–5000, smoothening neighbor 5–50, PCA 10–50. SGD는 consistency 상승하지만 direction 악화 → Adam 유지. preprocessing neighbor 증가 시 두 지표 동반 상승 → package default 증가 권고. 그 외 hyperparameter에 *robust*.
  - **Driver gene functional enrichment** (Fig. 5e, GABAergic lineage): DeepVelo의 top 100 driver gene이 *neurogenesis pathway에 더 enriched* (Fisher exact $p = 1.407 \times 10^{-9}$, $n_{\mathrm{scV}}=103$, $n_{\mathrm{DV}}=97$).
- **정성적 효과**:
  - *Tmsb10 phase portrait* (Fig. 2d, Fig. 3b-c): granule lineage와 endothelial lineage가 동일 phase portrait region을 점유하지만 *cell-type-specific direction*을 동시에 정확히 예측. scVelo는 두 lineage를 *uniform direction*으로 잘못 분류.
  - *Time-dependent degradation simulation* (Fig. 3d-h): scVelo는 *역방향 trajectory* 시뮬레이션에서 reverse direction을 잡지 못함, DeepVelo는 early→late pseudotime 회복.
  - *PA tumor subpopulation* (Fig. 7): 본문 핵심 *biological discovery* — DeepVelo가 PA의 *intra-tumor immunogenicity heterogeneity*를 *처음으로* 보고 (MHC class II, antigen presentation, cytokine signaling enriched in immunogenic branch; Sample 1 immune $p$-value 매우 작음, sources/cui-2024-deepvelo-supp-7-immunogenic-samples.xlsx).

### Method 관점의 한계

- **약한 assumption**:
  - *Continuity assumption*은 *충분한 cell density*에서 성립 — *rare cell type* (저자 명시, §Discussion p17): t+1 neighbor가 충분하지 않으면 학습 불안정. 저자는 *neighbor 수에 robust*하다는 hyperparameter 결과로 부분 방어하지만, *rare cell type 자체가 아예 빠진 경우*는 미해결.
  - *Pearson direction heuristic* ($\eta_s = 18.0$): cell-agnostic correlation을 *direction tiebreaker*로 사용 — cell-specific direction이 *gene 전반의 평균 correlation*에 의해 약하게 묶일 위험 (Note S4 일부 논의).
- **구현 또는 학습상의 부담**:
  - Full-batch training (batch = $N$ cells) — 대규모 dataset (>100k cells) 시 *GPU 메모리* 부담. 본 paper benchmark는 *최대 30k cells (organogenesis downsampling)* — *full-scale single-cell atlas*에서의 scalability 미검증.
  - GCN 2-layer가 *over-smoothing* (graph DL의 일반 한계) 잠재 — 본문은 직접 언급하지 않으나, FFNet ablation 결과 (cell-type-wise consistency 더 높음)가 *GCN이 더 보수적*임을 시사.
- **일반화가 불확실한 조건**:
  - *Confidence quantification*: 저자도 명시 (§Discussion p17) — *probabilistic uncertainty*가 부재. Continuity score는 *post hoc proxy*일 뿐 well-calibrated posterior 아님.
  - *Chromatin / multi-omics*: RNA-only — *transcription-chromatin lag* 같은 epigenome question 직결 불가. 저자도 future work로 *multi-omics 확장*을 명시 (§Discussion p17).
  - *Batch effect / batch integration*: dentate gyrus multi-batch에서 적용된다고 언급 (§p6) 하지만 *명시적 batch correction layer 없음* — large-scale atlas (multi-lab/donor)에서 *batch confound* 처리 불명확.

## Results

### Dataset 1 — Dentate gyrus neurogenesis (P12 + P35)

- **Dataset**: developing mouse dentate gyrus, 10x Genomics Chromium V1, 2 time points (P12, P35) (GSE95753 — Hochgerner 2017). Subset to neurogenesis-relevant cell types.
- **목적**: cell-specific kinetics가 *multi-faceted gene* (Tmsb10, Ppp3ca)에서 *cell-type-specific direction* 분리할 수 있는지 검증.
- **사용한 데이터 규모**: $n = 2{,}930$ cells (Mann-Whitney test에서 명시).
- **Baseline / 비교 대상**: scVelo dynamical, scVelo stochastic.
- **Metric / 평가 기준**: overall consistency, cell-type-wise consistency, direction score, Mann-Whitney U two-sided test.
- **주요 수치**:
  - Overall consistency mean ± std (sheet "Overall Consistency"): DeepVelo $0.9482 \pm 0.0319$ vs scVelo dynamical $0.8009 \pm 0.1074$ vs scVelo stochastic $0.8633 \pm 0.0658$. Mann-Whitney U $p < 1.0 \times 10^{-300}$, $n = 2{,}930$ both groups (§p5, Fig. 2b).
  - Cell-type-wise consistency: $0.844 \pm 0.0818$ vs $0.6077 \pm 0.1430$ vs $0.7455 \pm 0.0980$ (Fig. 2c).
  - Direction score: $0.370 \pm 0.526$ vs $-0.008 \pm 0.636$ vs $0.191 \pm 0.566$.
- **정성 결과**: granule lineage (neuroblast → granule immature → granule mature) 정확 회복; Tmsb10 phase portrait에서 *granule + endothelial 두 lineage 동시* 정확 (Fig. 3b vs scVelo Fig. 3c).
- **논문 주장과의 연결**: cell-specific kinetic rate가 *multifaceted gene*의 cell-type-별 direction을 분리한다는 *주요 주장의 1차 증거*.
- **통계 유의성 평가**:
  - `해석:` Mann-Whitney U $p < 10^{-300}$은 *극도로 강한 evidence* — 단 *효과 크기* (overall consistency $0.948$ vs $0.801$, $\Delta \approx 0.147$)도 *큰* 실효성. multiple testing correction은 *명시 없음* — 단 두 method 비교라 burden 낮음. `미제공:` confidence interval은 std로만 보고 (CI 형식 없음).
  - `해석:` 재현성은 *single dataset, single technical replicate* — 다른 dataset (hindbrain, organogenesis, gastrulation)에서도 동일 방향의 우위가 나오므로 *cross-dataset replication*은 강함.

### Dataset 2 — Hindbrain development (GABAergic / gliogenic bifurcation)

- **Dataset**: mouse hindbrain, 9 time points (E10 ~ P14), GSE118068 (Vladoiu 2019, ref. 11). Kallisto reference-free alignment → loom; junction between GABAergic and gliogenic lineage subset (neural stem, proliferating VZ, VZ, differentiating GABA, gliogenic progenitor, GABA interneuron).
- **목적**: *bifurcating lineage*에서 cell-type-specific velocity direction이 올바른 trajectory를 회복하는지 + driver gene을 정확히 추출하는지.
- **사용한 데이터 규모**: cell 수 본문 표기 미명시 (`미제공:` 본문에는 n 직접 없음). Direction/Consistency 측정 자체는 *모든 boundary cell* 기준.
- **Baseline / 비교 대상**: scVelo dynamical.
- **Metric / 평가 기준**:
  - Direction score, overall consistency, cell-type-wise consistency.
  - Top 100 driver gene marker overlap (Vladoiu marker), TF overlap (Lambert 2018 ref. 42, ortholog-lifted to mouse), Mann-Whitney U on driver ranking, Fisher exact on pathway functional category.
- **주요 수치**:
  - Direction score: $0.383 \pm 0.622$ (DeepVelo) vs $0.326 \pm 0.641$ (scVelo dyn) vs $0.393 \pm 0.613$ (scVelo stoch).
  - Overall consistency: $0.936 \pm 0.047$ vs $0.871 \pm 0.148$ vs $0.914 \pm 0.067$.
  - Driver gene marker ranking — GABAergic lineage: Mann-Whitney U two-sided $p = 1.376 \times 10^{-7}$, $n = 245$ both groups. Gliogenic: $p > 0.05$, $n = 131$ both (NS).
  - Pathway enrichment: DeepVelo top 100 → GABAergic 97 enriched + gliogenic 151 enriched pathway (ActivePathways, FDR-corrected; sources/cui-2024-deepvelo-supp-4-pathway-go.xlsx).
  - Neurogenic functional category Fisher exact: $p = 1.407 \times 10^{-9}$ (GABAergic; $n_{\mathrm{scV}}=103$, $n_{\mathrm{DV}}=97$). Gliogenic NS ($p > 0.05$, $n_{\mathrm{scV}}=76$, $n_{\mathrm{DV}}=151$).
  - Known driver gene examples (top 100 from DeepVelo): Tfap2a, Tfap2b, Lhx5 (GABAergic — Zainolabidin 2017, Pillai 2007); Hes1, Sox9 (gliogenic — Wu 2003, Vong 2015). 추가 *novel* driver: Neurod6 (scVelo 미발견, Tutukova 2021 인용).
- **정성 결과**: PAGA trajectory inference 후 *neural stem → VZ → differentiating GABA / gliogenic progenitor* branching 정확 (Fig. 4c). scVelo는 gliogenic progenitor에서 *partial inverse direction* (Fig. 4f, highlighted regions) → trajectory 잘못 추정.
- **논문 주장과의 연결**: cell-specific kinetics가 *driver gene을 functional pathway와 더 잘 일치*시킨다는 주장의 *biological validation*.
- **통계 유의성 평가**:
  - `해석:` GABAergic에서 $p \sim 10^{-7}$ + Fisher $p \sim 10^{-9}$은 *robust evidence*. 단 gliogenic NS 결과는 *효과의 lineage-dependence*를 시사 — DeepVelo의 우위가 *모든 lineage에서 일관*되지 않음.
  - `미제공:` n=245, n=131 등 sample 수의 정확한 unit (cells? markers? all genes?) — *driver gene 분석 sample = 전체 2,000 tested gene 중 marker overlap된 gene 수*로 추정 (§p11 "rankings... across all tested driver genes").
  - `해석:` multiple testing correction은 *FDR (ActivePathways)*로 pathway 단위 적용. method 비교 자체는 *single test*.

### Dataset 3 — Mesenchymal / chondrocyte organogenesis (MOCA)

- **Dataset**: Mouse Organogenesis Cell Atlas (Cao 2019, ref. 12, GSE119945, SRA PRJNA490754) — chondrocyte trajectory subset. Alevin-Fry v0.8.0 reprocessing; spliced/unspliced/ambiguous read 모두 보존.
- **목적**: $n > 2$ multi-furcating lineage (mesenchymal cell이 myocyte / connective tissue progenitor / limb mesenchyme / jaw-tooth progenitor / chondrocyte progenitor / osteoblast / intermediate mesoderm으로 분기)에서의 velocity direction 정확도.
- **사용한 데이터 규모**: 30,000 cells (downsampled from original chondrocyte trajectory, §Methods p18).
- **Baseline**: scVelo dynamical.
- **Metric**: direction score, overall consistency, cell-type-wise consistency, concordance with Cao et al. ground-truth lineage.
- **주요 수치**:
  - Direction score: $0.282 \pm 0.523$ (DV) vs $-0.035 \pm 0.591$ (scVelo dyn) vs $0.072 \pm 0.575$ (scVelo stoch) — *DeepVelo만 positive*, scVelo dynamical은 *역방향*.
  - Overall consistency: $0.899 \pm 0.042$ vs $0.772 \pm 0.086$ vs $0.767 \pm 0.076$.
  - Cell-type-wise consistency: $0.633 \pm 0.077$ vs $0.470 \pm 0.121$ vs $0.492 \pm 0.075$.
- **정성 결과**: scVelo dynamical은 *terminal chondrocyte / osteoblast을 progenitor state로 잘못 예측* — *trajectory 전체 역전*. DeepVelo는 early mesenchymal → multi-furcating differentiation 정확.
- **논문 주장과의 연결**: 가장 *복잡한 lineage*에서도 DeepVelo가 *direction 우위* — *cell-specific rate의 multi-furcating 적용성*.

### Dataset 4 — Mouse gastrulation (Pijuan-Sala 2019)

- **Dataset**: mouse gastrulation single-cell atlas (Pijuan-Sala 2019, ref. 13).
- **목적**: 가장 challenging한 *gene with multiple kinetics* (MURK gene) 시나리오에서 direction 회복.
- **데이터 규모**: 본문 표기 미명시 (`미제공:` Supp Fig. S18).
- **Baseline**: scVelo dynamical, scVelo stochastic.
- **주요 수치** (Supp Table sheet 'Direction Score'):
  - Direction score: $0.769 \pm 0.305$ (DV) vs $-0.475 \pm 0.618$ (scV-dyn) vs $0.018 \pm 0.706$ (scV-stoch) — *DeepVelo의 가장 큰 margin*.
  - Overall consistency: $0.979 \pm 0.020$ vs $0.843 \pm 0.052$ vs $0.747 \pm 0.097$.
  - Cell-type-wise consistency: $0.918 \pm 0.081$ vs $0.590 \pm 0.096$ vs $0.543 \pm 0.126$.
- **논문 주장과의 연결**: MURK gene이 *전체 dataset의 58% 차지* (Supp Fig. S3) — cell-specific kinetics의 *경험적 정당성*.

### Dataset 5 — Large-scale hippocampus (La Manno 2018)

- **Dataset**: 대규모 hippocampus scRNA-seq (La Manno 2018, ref. 1 — velocyto 원 paper의 dataset).
- **목적**: 큰 cell 수에서의 robustness.
- **주요 수치**: Direction $0.601$ vs $0.147$ vs $0.347$; overall consistency $0.934$ vs $0.857$ vs $0.874$; cell-type-wise $0.713$ vs $0.589$ vs $0.645$.

### Dataset 6 — Pilocytic astrocytoma (PA, 3 patients)

- **Dataset**: PA tumor scRNA-seq (Vladoiu 2019, ref. 11, EGAS00001003170 — *controlled access EGA*). CellRanger v7.0.1, hg19 reference.
- **샘플 정보** (sources/cui-2024-deepvelo-supp-6-sheet1.xlsx): Sample 1 (BT2017065, age at Dx 9, M), Sample 2 (BT2017084, 7, M), Sample 3 (BT2017028, 15, M) — *모두 male*.
- **Cell-type 구성** (sources/cui-2024-deepvelo-supp-8-celltype-samples.xlsx):
  - Sample 1: Microglia 4,563 / T-cell 3,943 / Tumor 1,644
  - Sample 2: Microglia 1,138 / T-cell 7,223 / Tumor 3,669
  - Sample 3: Microglia 3,646 / T-cell 1,567 / Tumor 3,054
  - Tumor cell만 추출해 RNA velocity 분석 (§p14).
- **목적**: DeepVelo로 *novel biological discovery* — PA tumor subpopulation 동역학.
- **Baseline**: 본 분석은 DeepVelo 단독 (방법 비교 아님 — *DeepVelo로만 가능한 발견*을 demonstrate).
- **주요 수치 / 결과**:
  - 각 sample의 tumor cell이 *2개 branch*로 분기 (Louvain on DeepVelo velocity graph, Supp Fig. S17).
  - Pathway enrichment (ActivePathways, FDR-corrected):
    - Sample 1 immunogenic: 155 pathway enriched (MAPK cascade $p=2.83\times 10^{-6}$, cell activation $p=5.68\times 10^{-7}$, chemokine activity $p=5.4\times 10^{-4}$).
    - Sample 1 depleted: 6 pathway (CNS development, neurogenesis 위주).
    - Sample 2 immunogenic: 129 (MHC class II protein complex binding $p=2.03\times 10^{-17}$ — *극도 강함*).
    - Sample 3 immunogenic: 263 (MHC class II receptor activity, antigen-related).
  - MAPK pathway가 *immunogenic branch에서만* enrichment — Reitman 2019 (ref. 29) marker score로는 *branch 차이가 드러나지 않았던* 결과 (`해석:` pathway-level analysis가 *marker-level score*보다 더 sensitive하다는 저자 주장).
- **정성 결과**: PA에서 *intra-tumor immunogenicity heterogeneity*가 *최초로 보고됨* (저자 주장 §p15). 모든 3 sample에서 microenvironment immune cell 충분 (T cell, microglia 다수) → 변동의 원인은 *tumor 측 antigenicity 조절*로 해석.
- **논문 주장과의 연결**: DeepVelo가 *기존 method가 놓친 sub-lineage*를 detect → *clinical implication* (PA prognosis, immunotherapy 후보 stratification).
- **통계 유의성 평가**:
  - `해석:` $n=3$ patient — *통계 검증을 위한 sample 수는 작음*. 3 patient 모두에서 같은 *branching 패턴*이 보이는 것은 *3-replicate convergent evidence*로 해석할 수 있으나, *cohort generalization*은 약하다.
  - `검토필요:` Reitman/Aldinger marker score와의 *discrepancy*가 *pathway analysis의 sensitivity 우위*인지 *cell type annotation 차이*인지는 본문에서 직접 분리하지 않음.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 6 dataset 전부에서 DeepVelo가 direction score와 overall consistency 1위. cell-type-wise consistency는 pancreas에서 scVelo stochastic이 더 높은 1건 외 모두 우위.
- **가장 중요한 수치**: Mouse gastrulation의 direction score $0.769$ vs $-0.475$ (scVelo dynamical) — *부호 자체가 다름* (DeepVelo는 올바른 방향, scVelo는 역방향). overall consistency $0.979$ vs $0.843$.
- **Baseline 대비 차이**: direction에서 *$\Delta$ 평균 $\sim 0.3$* (조건별 $0.06$ ~ $1.24$); overall consistency $\Delta$ 평균 $\sim 0.1$; cell-type-wise consistency $\Delta$ 평균 $\sim 0.15$.
- **결과 해석 시 주의점**:
  - `해석:` consistency 단독으로는 *over-smoothing*이 bias될 수 있어 *direction score*가 더 결정적. cellDancer는 consistency 높지만 direction 떨어진다는 본문 비판이 이 관점.
  - `해석:` *모든 dataset이 mouse + 발달*. *human adult* / *질병 (PA 제외)* / *immune system* 등에 generalization 직접 검증 없음 — `미제공:` human adult tissue benchmark.
  - `해석:` PA biological discovery는 *DeepVelo와 scVelo 직접 비교 없음* (DeepVelo 단독 분석) → "DeepVelo 덕분에 발견됐다"는 *반사실 (counterfactual)*은 본문에서 직접 검증되지 않음.

### Robustness 분석 (Supp Note S1)

- **Hyperparameter sweep** (Supp Table S8, $n = 5{,}000$ random search runs, sources/cui-2024-deepvelo-supp-9-hp-sweep.xlsx — 5,001행, 27열): dentate gyrus dataset에서 학습/objective/preprocessing hyperparameter 변화에 따른 consistency + direction score 분포.
  - Adam vs SGD vs RMSprop: SGD는 consistency 상승하지만 direction 악화 → *Adam 유지 결정*.
  - Learning rate 0.0001 ~ 0.1: consistency는 marginal change, direction은 극단값 (0.1, 0.0001)에서만 변동. 0.001 best.
  - Preprocessing neighbor 증가 → consistency + direction 동반 상승 → 차기 패키지 default 증가 권고.
  - 결론: DeepVelo는 *주요 hyperparameter에 robust*.
- **Architecture ablation — GCN vs FFNet** (Supp Table S9, sources/cui-2024-deepvelo-supp-10-direction-consistency-v2.xlsx):
  - GCN이 *direction score에서 우위* (dentate +0.115, hindbrain +0.015, large-scale hippocampus +0.11~+0.35).
  - FFNet이 *cell-type-wise consistency에서 우위* (dentate +0.054, pancreas +0.106, hindbrain +0.057) → *trade-off* 존재. 본문은 *direction이 더 중요*라는 논리로 GCN 채택.

### Runtime

- CPU-only DeepVelo: scVelo dynamical 대비 *$4\times$ speedup*.
- GPU 가속: *$10$–$20\times$* speedup. Hindbrain 13,501 cells 36 초 (§p16, Supp Fig. S8).

## Figures

### Figure 1 — DeepVelo pipeline overview

- 이 Figure가 필요한 이유: method paper의 *architecture introduction*. cell-specific kinetic rate + GCN + extrapolation training의 *3-step 시각화*.
- 이 Figure가 뒷받침하는 주장: cell-specific $(\alpha_i, \beta_i, \gamma_i)$가 *neural network output*으로 학습되고, query cell + neighbor가 *graph input*임을 시각.

#### 패널별 설명

- **a**: cell-specific transcription/splicing/degradation rate concept. unspliced ↔ spliced ODE 도식.
- **b**: full pipeline — preprocessing → training → prediction → downstream.
- **c**: GCN encoder + FC decoder 구조. query cell (dark blue) + k-NN cell (light blue) → latent → $(\alpha, \beta, \gamma)$ → extrapolated $s(t+1)$ → 실측 downstream cell (red) 와의 차이를 minimize.
- **d**: downstream analysis — velocity visualization, pseudotime, confidence score, driver gene.

#### 본문에서 강조한 비교

- 비교 대상: 종전 cell-agnostic kinetic rate vs DeepVelo의 cell-specific rate (figure caption + §p3).
- 관찰된 차이: 종전은 *gene 1개당 1세트 rate*, DeepVelo는 *cell × gene 행렬*.
- 이 차이가 의미하는 것: *expressive power*의 차원이 다름 — multi-lineage가 single global rate로 표현 불가했던 한계 해소.

#### 해석 시 주의점

- `해석:` Figure 1은 schematic — *biological mechanism*이 아니라 *computational pipeline*. *transcription factor binding 메커니즘*과 무관.
- `미제공:` panel 안의 detailed dimension (latent dim, layer 수)은 §"Implementation details" p24에 따로 정리.

### Figure 2 — Dentate gyrus velocity comparison

- 이 Figure가 필요한 이유: DeepVelo vs scVelo의 *첫 정량 비교*. cell-specific kinetics가 *consistency 차이*로 나타남을 시각.
- 이 Figure가 뒷받침하는 주장: cell-specific rate가 *neighborhood-consistent direction*을 제공.

#### 패널별 설명

- **a**: UMAP 위 velocity arrow 비교 — DeepVelo는 neuroblast → granule immature → granule mature flow가 더 일관, scVelo는 mature granule cell에서 *unclear flow*. zoom-in panel 강조.
- **b**: Overall consistency boxplot + histogram (DeepVelo $0.9482$ vs scVelo $0.8009$). Mann-Whitney U $p < 10^{-300}$, $n=2{,}930$.
- **c**: Cell-type-wise consistency boxplot + histogram ($0.844$ vs $0.6077$).
- **d, e**: Tmsb10, Ppp3ca phase portrait — spliced (x축) vs unspliced (y축).
- **f, g**: Tmsb10, Ppp3ca의 velocity와 expression을 UMAP에 시각. high velocity 영역과 high expression 영역의 *alignment*.

#### 본문에서 강조한 비교

- 비교 대상: DeepVelo vs scVelo dynamical (Fig. 2a) + DeepVelo vs scVelo stochastic (panel b-c).
- 관찰된 차이: 모든 metric에서 DeepVelo significant 우위. *효과 크기는 cell-type-wise > overall > direction*의 분산.
- 이 차이가 의미하는 것: cell-specific rate가 *직접적으로 consistency를 향상* + *cell-type-별 boundary*를 잘 표현.

#### 해석 시 주의점

- `해석:` consistency 자체는 *over-smoothing*에서도 높을 수 있어 *direction score* (Fig. S7, S18)와 함께 봐야 의미. 본 Figure는 consistency만 시각.
- `해석:` p-value $< 10^{-300}$은 *극단치* — 보고하기에 적절하나 *effect size*가 더 의미 있음 (overall consistency $\Delta \approx 0.15$).

### Figure 3 — Branching + time-dependent kinetics

- 이 Figure가 필요한 이유: cell-specific kinetics가 *동일 phase portrait region에서 cell-type-별 direction*을 분리할 수 있음을 시각.
- 이 Figure가 뒷받침하는 주장: multifaceted gene과 time-dependent gene 모두에서 DeepVelo 우위.

#### 패널별 설명

- **a**: 2,930 cell의 *cell-specific kinetic rate*를 UMAP으로 시각. cell-type별 cluster, lineage 근접성 — *cell-type annotation 없이 학습했음에도* 발현 — 시각적 sanity check.
- **b**: DeepVelo의 Tmsb10 phase portrait — endothelial / granule lineage *2개 trajectory* 동시 정확.
- **c**: scVelo의 Tmsb10 phase portrait — endothelial이 *반대 방향*으로 분류.
- **d, e, f**: scVelo simulator로 만든 *time-dependent degradation rate* 시뮬 — d) reference constant rate velocity, e) constant rate phase portrait, f) time-dependent rate phase portrait (reversed trajectory).
- **g, h**: time-dependent simulation (500 cells, 30 genes 중 3개 gene에서 $\gamma$가 시간에 따라 증가)에서 DeepVelo vs scVelo의 velocity — DeepVelo가 *correct direction* (early → late pseudotime), scVelo는 *direction 실패*.

#### 본문에서 강조한 비교

- 비교 대상: DeepVelo vs scVelo, 같은 region.
- 관찰된 차이: cell-type-별 direction (Tmsb10) + time-dependent kinetics (simulation) 모두 DeepVelo 정확.
- 이 차이가 의미하는 것: *cell-specific rate가 두 어려운 setting*을 동시에 해결 — *separate mechanism이 아니라 같은 framework*가 양쪽을 처리.

#### 해석 시 주의점

- `해석:` panel a (kinetic rate UMAP)는 *DeepVelo가 cell-type을 학습했다*는 주장의 *post hoc* 시각화 — *cell-type label과 일관*은 *intrinsic*이 아니라 *correlated*. ground-truth biology와의 일치는 신뢰성 평가에 유익하지만, *kinetic rate 자체가 실제 biochemical rate*인지 별도 검증 필요 (lens-academic §Limitations).
- `해석:` simulation은 *scVelo 자체 simulator*로 만들었으므로 baseline scVelo 가 *unfair disadvantage*일 가능성 (Bergen 2021 reversed dynamics simulation 차용, ref. 20).

### Figure 4 — Hindbrain velocity + trajectory + driver genes

- 이 Figure가 필요한 이유: bifurcating lineage에서 *trajectory inference 정확도* 시각 + driver gene biological validation.
- 이 Figure가 뒷받침하는 주장: cell-specific rate가 *biological lineage relation*과 *known TF driver*를 동시에 회복.

#### 패널별 설명

- **a**: ground-truth developmental order (6 cell type — NSC → VZ progenitors → differentiating GABA / gliogenic progenitor → GABA interneuron).
- **b**: DeepVelo velocity over tSNE — *outward arrow from NSC*, *inward to GABA interneuron*.
- **c**: PAGA trajectory inference using DeepVelo connectivity — *correct branching*.
- **d**: top 60 driver gene (positive correlation, pseudotime ordered) for GABAergic lineage — heatmap.
- **e**: 선정된 driver gene (Tfap2b, Tfap2a, Lhx5, Neurod6)의 phase portrait + velocity + expression.
- **f**: scVelo dynamical의 velocity + PAGA — *gliogenic progenitor에서 partial inverse*.

#### 본문에서 강조한 비교

- 비교 대상: DeepVelo trajectory (c) vs scVelo trajectory (f); DeepVelo driver gene (d-e) vs scVelo (다음 Figure에서 정량 비교).
- 관찰된 차이: scVelo가 gliogenic에서 *역방향 partial* → trajectory 잘못. driver gene에서 *known TF + novel Neurod6 hit*.
- 이 차이가 의미하는 것: cell-specific rate가 *trajectory + driver 동시 정확도*. *Neurod6* novel hit는 testable hypothesis 제공.

#### 해석 시 주의점

- `해석:` panel f의 *highlighted region*은 저자 manual annotation — *역방향 정도*가 *수치적*으로 quantified되지 않음 (Fig. 6f의 direction score plot이 정량 보강).
- `해석:` Neurod6 hit는 *literature support* (Tutukova 2021)만 — *experimental validation* (perturb-seq, CRISPRi) 부재.

### Figure 5 — Functional enrichment of driver genes

- 이 Figure가 필요한 이유: driver gene의 *biological functional 의미*를 pathway/TF로 정량.
- 이 Figure가 뒷받침하는 주장: DeepVelo의 driver gene이 *기능적으로 더 의미*있음.

#### 패널별 설명

- **a**: top 100 driver gene과 annotated marker overlap (GABAergic / gliogenic, scVelo vs DeepVelo) — DeepVelo가 더 많은 marker overlap.
- **b**: 2,000 tested gene 중 known marker의 *ranking density* — GABAergic에서 DeepVelo가 더 높은 ranking ($p = 1.376 \times 10^{-7}$, $n=245$).
- **c**: TF overlap — GABAergic에서 DeepVelo 더 많은 hit, gliogenic 동률.
- **d**: pathway enrichment 개수 — DeepVelo 97 (GABAergic) + 151 (gliogenic) vs scVelo 103 + 76.
- **e**: functional 분류 (Neurogenesis / Developmental non-neuronal / Non-specific) 비율 — DeepVelo가 *neurogenesis 비율 더 높음* (Fisher $p = 1.407 \times 10^{-9}$).
- **f**: top 20 pathway (FDR p-value 기준).

#### 본문에서 강조한 비교

- 비교 대상: DeepVelo vs scVelo, GABAergic / gliogenic 분리.
- 관찰된 차이: GABAergic에서 *모든 metric* DeepVelo 우위; gliogenic은 marker overlap 우위 + 다른 지표 NS.
- 이 차이가 의미하는 것: *lineage 마다 effect가 다름* — DeepVelo의 우위가 lineage-uniform 아님.

#### 해석 시 주의점

- `해석:` pathway 개수 차이 (151 vs 76 in gliogenic)는 *statistical power*가 아니라 *enrichment threshold*의 결과 — 같은 FDR threshold 적용했으면 *비교 가능*하지만 ranking 우위는 아닐 수 있음.

### Figure 6 — Mesenchymal/chondrocyte multi-furcating

- 이 Figure가 필요한 이유: $n > 2$ furcating lineage에서 direction score 우위 시각 + scVelo의 direction 역전 *시각 + 정량* 동시.
- 이 Figure가 뒷받침하는 주장: multi-furcating 복잡 system에서도 cell-specific rate가 trajectory 정확.

#### 패널별 설명

- **a**: Cao et al. ground-truth differentiation trajectory (solid black: confirmed, grey: assumed, dashed: subset).
- **b**: scVelo dynamical velocity.
- **c**: DeepVelo velocity — 정확.
- **d, e**: overall consistency, cell-type-wise consistency.
- **f**: per-cell direction score (DeepVelo vs scVelo).

#### 본문에서 강조한 비교

- scVelo는 chondrocyte / osteoblast를 *progenitor로 잘못 예측* → trajectory 전체 역전. DeepVelo는 early mesenchymal을 root로 정확.

#### 해석 시 주의점

- `해석:` direction score가 positive ($0.282$)이지만 *std $0.523$*로 큼 — *많은 cell이 여전히 noise level 또는 wrong direction*. 평균만으로 *전체 cell 정확*하다 해석 금지.

### Figure 7 — Pilocytic astrocytoma branching

- 이 Figure가 필요한 이유: DeepVelo의 *biological discovery* — PA의 intra-tumor immunogenicity heterogeneity 첫 보고.
- 이 Figure가 뒷받침하는 주장: DeepVelo가 *기존 marker analysis가 놓친 sub-lineage*를 발견 가능.

#### 패널별 설명

- **a**: 3 PA sample의 tumor cell velocity + Louvain branch.
- **b**: split-branch pseudotime (early vs late tumor cell).
- **c**: Upset plot — 3 sample × 2 branch (immunogenic / depleted)의 pathway overlap.
- **d**: enrichment map (Cytoscape + EnrichmentMap) — pathway node, 색상 = sample × branch enrichment.

#### 본문에서 강조한 비교

- immunogenic branch: MAPK cascade, MHC class II, antigen presentation, adaptive immune response.
- depleted branch: neurogenesis, synaptic organization, biosynthesis.
- *3 sample 모두에서 같은 패턴*.

#### 해석 시 주의점

- `해석:` *DeepVelo 단독 분석* — scVelo와 직접 비교 없음. *DeepVelo로만 가능했다*는 주장은 *implicit*.
- `해석:` 3 sample은 *모두 male, age 7~15* — *cohort 편향*. *sex / age generalization* 불가.
- `검토필요:` `EGAS00001003170`은 *controlled access EGA* — 재현 시 *data access committee* 승인 필요.

## Tables

본문에는 정식 Table 없음 — 모든 수치 비교는 Figure + Supplementary Table.

### Supplementary Table S1 — driver gene marker overlap (hindbrain)

- 출처: sources/cui-2024-deepvelo-supp-3-cell-types.xlsx (Vladoiu GABAergic+gliogenic gene list, 1,030행) + Additional file 2 (S1).
- 내용: top 100 driver gene과 Vladoiu marker overlap. Fig. 5a의 raw counts.
- 핵심: GABAergic에서 DeepVelo > scVelo, gliogenic 비교 결과는 본문에서 NS.
- `해석:` Vladoiu cell-type marker는 *전체 1,030행* (예: Pttg1ip $p$-adj $= 8.85 \times 10^{-58}$, log-FC $0.25$, Gliogenic progenitor annotation) — *broad marker pool*.

### Supplementary Table S2 — driver gene ranking comparison (hindbrain)

- Mann-Whitney U statistics for DeepVelo vs scVelo ranking of marker genes. GABAergic $p = 1.376 \times 10^{-7}$.

### Supplementary Table S3 — pathway enrichment (hindbrain GABAergic + gliogenic)

- 출처: sources/cui-2024-deepvelo-supp-4-pathway-go.xlsx (4 sheet).
  - DeepVelo GABAergic: 82 row (GO + REACTOME, FDR-adj).
  - DeepVelo gliogenic: 130 row.
  - scVelo GABAergic: 94 row.
  - scVelo gliogenic: 96 row.
- 핵심: GO category 중심 (cytoskeletal protein binding, microtubule binding 등 — neurogenesis 관련 cell morphogenesis 함). REACTOME 일부.
- `해석:` DeepVelo의 GABAergic top hit (cytoskeletal/microtubule binding)와 scVelo의 GABAergic top hit이 *상당 부분 겹침* (microtubule binding은 둘 다 포함). *완전 비대칭이 아닌, 우선순위 차이*가 결과의 본질.

### Supplementary Table S4 — direction / consistency across 6 datasets

- 출처: sources/cui-2024-deepvelo-supp-5-direction-consistency.xlsx (3 sheet).
- 위 "효과가 Results에서 나타난 방식" table에 본문 인용.

### Supplementary Tables S5–S7 — PA sample metadata + cell types + immunogenic/depleted pathway

- S5 (sources/cui-2024-deepvelo-supp-6-sheet1.xlsx): 3 PA sample clinical info.
- S7 (sources/cui-2024-deepvelo-supp-7-immunogenic-samples.xlsx, 6 sheet — Sample 1/2/3 Immunogenic/Depleted): immune pathway enrichment 정량.
  - Sample 1 Immunogenic 155 pathway; Sample 1 Depleted 6 pathway.
  - Sample 2 Immunogenic 129; Sample 2 Depleted 38.
  - Sample 3 Immunogenic 263; Sample 3 Depleted 43.
  - *모든 sample에서 immunogenic이 depleted보다 enriched pathway 수 훨씬 많음* — *immunogenic이 더 transcriptionally active*.
- S8 (sources/cui-2024-deepvelo-supp-8-celltype-samples.xlsx): sample별 microglia/T-cell/tumor 수 (위 Dataset 6 참조).

### Supplementary Table S8 — hyperparameter sweep results

- 출처: sources/cui-2024-deepvelo-supp-9-hp-sweep.xlsx (5,001 row, 27 column — Weights & Biases sweep export).
- Note S1 + Supp Fig. S19–S27의 raw data.
- 핵심: $n = 5{,}000$ random search → DeepVelo는 *주요 hyperparameter에 robust*.

### Supplementary Table S9 — GCN vs FFNet ablation

- 출처: sources/cui-2024-deepvelo-supp-10-direction-consistency-v2.xlsx (3 sheet — Direction / Overall / Celltype-wise).
- Direction에서 GCN 우위, celltype-wise consistency에서 FFNet 우위.

## Supplementary Information

### Supp Note S1 — Hyperparameter robustness (Supp PDF p1–3)

- $n = 5{,}000$ random search on dentate gyrus.
- Hyperparameter space: learning rate [0.0001, 0.001, 0.01, 0.1], optimizer [Adam, SGD, RMSprop], top G [5, 10, 20, 30, 40, 50], top C [5, 10, 20, 30, 40, 50], NN layer [[32,32], [64,64], [128,128], [256,256], [512,512], [64,64,64]], Pearson scaling $U(1, 100)$, HVG [500, 1000, 2000, 2500, 5000], smoothening neighbor [5, 10, 15, 20, 30, 40, 50], PCA [10, 20, 30, 40, 50].
- 결론: GCN 사용 시 direction score $+0.11$ (large dataset)부터 $+0.35$까지 상승.

### Supp Note S2 — Theoretical analysis of continuity assumption

- **핵심 증명**:
  1. Continuity assumption은 steady-state + scVelo dynamical 가정의 *superset*. (정확히, 이전 가정 만족 → continuity 만족.)
  2. *Asymptotic error bound*: cell $n$이 $(0, T)$ uniform sample이면 nearest spacing의 distribution은 $\mathrm{Beta}(1, n)$. expectation $T/(n+1)$.
  3. velocity estimation의 error는 *gene dynamic function* $f_{\mathrm{dyn}}$의 high-order derivative + nearest spacing에 의해 bound. Corollary 1 + 2: spacing이 $O(1/\sqrt{n})$ 또는 $O(1/n)$의 경우 error 수렴 속도.

### Supp Note S3–S5

- S3: cellDancer comparison detail.
- S4: Pearson correlation heuristic의 properties (direction tiebreaker로 사용 정당성).
- S5: 추가 dataset description.

### Supp Figures S1–S29 (40-page PDF)

- S1: cellDancer direction score 비교 — *4 method 중 최악*.
- S3: multi-faceted gene 비율 — 평균 *0.58*. cell-specific kinetics 필요성의 *경험적 근거*.
- S4: developmental time point (P12+P35 for dentate gyrus, E10~P14 for hindbrain) histogram.
- S5: cell-specific kinetic rate의 *epoch별 PCA 진화* (epoch 10, 20, 30, 60, 90, 120) — endothelial cell이 점진적으로 cluster.
- S6: large-scale hippocampus 비교 (velocity, pseudotime, trajectory).
- S7: 6 dataset의 direction + consistency 종합 box plot.
- S8: runtime CPU vs GPU.
- S11–S16: PA 3-sample의 Reitman / Aldinger marker module score (branching variation과 *correlated하지 않음*을 보임).
- S17: PA Louvain clustering on velocity graph.
- S18: Mouse gastrulation velocity + MURK gene phase portrait + direction score density.
- S19–S27: hyperparameter sweep distribution (각 hyperparameter별).
- S28: continuity error bound 시각화.
- S29: mouse gastrulation MURK gene 추가 분석.

## 분석 자체에 대한 메모

- DeepVelo는 *epigenomic-lag topic의 direct method 후보가 아니다*. chromatin/ATAC를 다루지 않음. 본 분석에서 importance를 *중*으로 둔 이유 — *MoFlow / MultiVeloVAE의 직접 reference*로서 *method genealogy* 이해에 필요.
- `질문:` MoFlow는 본문에서 *cellDancer의 직접 successor*로 자기 위치를 잡았다 (`@li2023celldancer` 참고). 그렇다면 DeepVelo는 어디에 들어가는가? — `해석:` cellDancer와 *동시기 (둘 다 2023 published, 원본은 2022 preprint)*, *별도 lineage*. cellDancer = per-gene DNN + cosine loss / DeepVelo = cross-gene GCN + continuity loss. 두 method는 *competing approach to same problem*.
- `질문:` MultiVeloVAE Fig. 2f의 RNA-only benchmark에서 DeepVelo의 GCBDir median이 $0.311$로 6 baseline 중 *중하위* (`@li2025multivelovae` 참고). 이는 DeepVelo의 *direction score가 GCBDir이라는 다른 metric에서는 더 약함*을 시사 — *metric definition 차이*가 결과 순위를 뒤집을 수 있음. `검토필요:` MultiVeloVAE의 GCBDir vs DeepVelo의 direction score가 어떻게 다른가, 직접 비교 시 어느 쪽이 fair 한가.
- `질문:` DeepVelo의 *PA tumor immunogenicity* discovery는 *임상 implication*이 크지만 *n=3 cohort*. 같은 finding이 *larger PA cohort* (BCH, COG database) 또는 *higher-grade glioma*에서 재현되는지 — *follow-up paper 검색* 필요.
- `검토필요:` Supp Note S2의 *asymptotic error bound 증명*은 *uniform time sampling* 가정에 의존 — 실제 scRNA-seq는 *cell type-별 sampling 편향* (rare type 적음) — 가정 위배 영향은 *Remark 1*에서 부분 논의되지만 정량 평가 미흡.
- `미제공:` Fig. 2의 panel별 zoom-in 영역의 *cell 수*는 본문에 없음 (`전체 2,930 cell` 만 명시).
- `미제공:` Fig. 7 (PA) 분석에서 *분기 detection이 robust*한 정량 검증 (cross-validation, permutation test) 부재 — Louvain 결과만 시각.
