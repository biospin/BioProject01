# A relay velocity model infers cell-dependent RNA velocity

Citation: `@li2023celldancer` — Li S*, Zhang P*, Chen W, Ye L, Brannan KW, Le N-T, Abe J, Cooke JP, Wang G. *Nature Biotechnology* 42:99–108 (2024, online 2023-04-03). DOI: 10.1038/s41587-023-01728-5. (*equal contribution; co-first authors)

> 본 분석은 `sources/li-2023-celldancer.pdf` (28-page Nature Biotechnology open access PDF — main text p1–p9 + Methods p11–p13 + Extended Data Fig. captions p14–p25), `sources/li-2023-celldancer-supp-1-figures-text.pdf` (9 page — Supp Figs 1–3, Supp Note 1 derivation, Supp Table 1), `sources/li-2023-celldancer-supp-2-reporting-summary.pdf` (3 page, image-only Nature Portfolio Reporting Summary — text 추출 불가, `미제공:`), `sources/abstract.txt` (Nature landing) 을 근거로 한다. 본 paper는 MoFlow (`@hong2026moflow`)의 *direct methodological predecessor*로, lens-academic에서 cellDancer → MoFlow 진화 sub-section을 별도 작성한다.

---

## Executive Summary

- **무엇**: cellDancer는 기존 RNA velocity의 *모든 cell에서 동일한 kinetic rate* 가정을 깨고, 각 cell의 *local neighbor displacement*가 future state proxy라는 *relay velocity* idea로 cell-specific transcription/splicing/degradation rate $(\alpha, \beta, \gamma)$를 *gene별 deep neural network*로 추정하는 *RNA-only* method. *latent time을 명시적으로 추정하지 않음*이 scVelo dynamical model과의 핵심 차이.
- **모델 / 방법**: 입력 cell $j$의 spliced $s(t_j)$, unspliced $u(t_j)$ → gene별 DNN $\Phi_{\theta_i}: (u, s) \to (\alpha, \beta, \gamma)$ → discretized ODE $du/dt = \alpha - \beta u$, $ds/dt = \beta u - \gamma s$ (Eq. 1–5)로 next-step state 예측 → loss $\mathcal{L}_j = 1 - \max_{j' \in \mathcal{N}_j} \frac{v_j \cdot v'_j}{\|v_j\| \cdot \|v'_j\|}$ (Eq. 6–9, max-cosine over neighbor displacement). Adam, learning rate 0.001, weight decay 0.004, sigmoid output $\to [0,1]$.
- **핵심 결과**:
  - ① **Simulation (n=1,000 genes × 4 regimes)**: cellDancer error rate 13.25% (transcriptional boost), 2.63% (multi-forward branching), 9.43% (multi-backward branching) vs scVelo 46.88% / 40.57% / 31.13%, velocyto 56.12% / 67.67% / 15.30%, DeepVelo 51.62% / 82.16% / 44.99%, VeloVAE 46.95% / 58.82% / 62.66% (Supp Table 1; P < 0.001 one-sided Wilcoxon, Extended Data Fig. 1c-e).
  - ② **Mouse gastrulation erythroid maturation** (Pijuan-Sala 2019, E-MTAB-6967; 12,329 cells × 89 MURK genes): cellDancer가 erythroid 1→2→3 정방향 회복, scVelo·DeepVelo·VeloVAE는 모두 *반대 방향* (Fig. 2a-c, Extended Data Fig. 2b).
  - ③ **Mouse hippocampal dentate gyrus** (Hochgerner 2018, GSE95753; 18,140 cells × 2,159 genes): 5개 branching lineage (granule, CA1-sub, CA2-3-4, OPC, astrocyte) 정확 회복; branching gene Ntrk2/Gnao1에서 lineage-specific $(\alpha, \beta, \gamma)$ 추정 (Fig. 3a-b, Extended Data Fig. 3).
  - ④ **Mouse pancreatic endocrinogenesis** (Bastidas-Ponce 2019, GSE132188; 3,696 cells × 2,000 genes): $(\alpha, \beta, \gamma)$ UMAP이 alpha/beta/delta/epsilon cell을 분리 — kinetic rate 자체가 *cell identity indicator* (Fig. 4d-e, Supp Fig. 3).
  - ⑤ **Robustness**: dropout 50–70%에서도 Pearson $R^2 > 0.96$ ($\alpha/\beta$), $> 0.84$ ($\alpha/\gamma$) (Extended Data Fig. 8); 1k–10k cells sparse data robust (Extended Data Fig. 8c); 18k cell × 2,159 gene runtime 286 → 36 min (1 → 30 jobs, Extended Data Fig. 10).
- **우리 적용**: MoFlow(`@hong2026moflow`)의 *direct relay velocity predecessor*. RNA-only baseline으로 비교 가치 + cosine loss formulation을 chromatin-aware로 확장한 MoFlow의 *시작점*. `methodology-reference` + `academic-citation` 우선.
- **심층**: 한계·재현 ROI는 `li-2023-celldancer_lens-academic.md` / `li-2023-celldancer_lens-industry.md` / `li-2023-celldancer_methodology-brief.md` 참고.

---

## Identity

- **Title**: A relay velocity model infers cell-dependent RNA velocity
- **Authors**: Shengyu Li*, Pengzhi Zhang*, Weiqing Chen, Lingqun Ye, Kristopher W. Brannan, Nhat-Tu Le, Jun-ichi Abe, John P. Cooke, Guangyu Wang (corresponding, gwang2@houstonmethodist.org). (*equal contribution; S.L., P.Z. co-first authors — p1 affiliation note.)
- **Affiliation**: Houston Methodist Research Institute (Center for Bioinformatics and Computational Biology / Center for Cardiovascular Regeneration / Center for RNA Therapeutics); Weill Cornell Medicine (Cardiothoracic Surgery, Physiology & Biophysics); MD Anderson Cancer Center (Cardiology). (p1 footnote.)
- **Venue / Year**: *Nature Biotechnology* 42:99–108 (2024 January issue, online 2023-04-03). Received 2022-08-01, Accepted 2023-02-28 (p1 header).
- **Funding**: Houston Methodist internal grant to G.W. (p13 Acknowledgements). 미제공: NIH grant 번호 없음.
- **COI**: 저자 명시 — "The authors declare no competing interests." (p13 Competing interests).
- **License**: CC BY 4.0 (Open Access, p10).
- **Data availability** (p13): scVelo CLI로 `scvelo.datasets.pancreas()` (GSE132188), `scvelo.datasets.gastrulation()` (E-MTAB-6967); hippocampus dentate gyrus loom (GSE95753); human embryo glutamatergic neurogenesis loom (SRP129388); scEU-seq RPE1-FUCCI via `dyn.sample_data.scEU_seq_rpe1()` (GSE128365). 모두 *open public*.
- **Code availability** (p13): https://github.com/GuangyuWangLab2021/cellDancer (PyTorch Lightning 구현). 미제공: license 명시 본문 부재 — `검토필요: GitHub repo 직접 확인 필요 (BSD/MIT/GPL 여부).`
- **Citation key**: `li2023celldancer`
- **Successor**: `@hong2026moflow` (MoFlow, Nat Commun 2025-12) — cellDancer의 relay velocity cosine loss를 chromatin-aware multi-omic으로 확장. 본 paper와 MoFlow는 *공동저자 없음* (Hong/Lee/Kim 3명 vs Li/Zhang/Wang 9명).

---

## Background

### 배경 스토리

- **문제의 출발점**: scRNA-seq는 cell을 destructive하게 측정하므로 trajectory inference 알고리즘이 *snapshot에서 directed dynamics를 재구성*해야 한다 (§Introduction p1, refs 9–11).
- **선행 접근 A — Pseudotime / similarity-based ordering** (Palantir refs 9, Wanderlust ref 10, diffusion pseudotime ref 11): cell을 ordering하지만 *root cell 사전 지정* 필요 + *방향성 불명확*.
- **A의 한계** (p1): trajectory의 *direction*과 *root/terminal state*를 결정하기 어렵다.
- **선행 접근 B — RNA velocity 1세대 (velocyto)** (La Manno 2018, ref. 12): unspliced/spliced mRNA의 first-order kinetics ODE로 *순간 미래 상태 외삽*. *Steady-state assumption* + *constant $\alpha$* (각 gene에 단일 transcription rate).
- **선행 접근 C — RNA velocity 2세대 (scVelo dynamical)** (Bergen 2020, ref. 17): full likelihood-based dynamical model로 latent time과 binary $\alpha$ (induction=1, repression=0) 동시 추정.
- **B·C의 공통 한계** (§Introduction p1–2): 모든 cell이 *공통의 $\alpha, \beta, \gamma$*를 공유한다고 가정. multi-stage transition (예: erythroid maturation의 *transcriptional boost* — Hba-x 같은 MURK gene이 분화 중간에 transcription rate가 boost됨)이나 multi-lineage branching (예: hippocampus 5 lineage)에서는 *gene별 kinetic rate가 cell subpopulation마다 다름* → universal kinetics 가정이 깨지면 *velocity 방향이 역전되거나 일부만 맞음*.
- **구체적 failure case** (p1–2, refs 13, 18): scVelo는 erythroid maturation에서 MURK gene (Hba-x 등)의 transcription boost 때문에 방향이 *반대로 예측*됨 (Barile 2021, ref. 18); hippocampus branching gene (Ntrk2 등)에서 5개 lineage 중 일부만 맞음.
- **선행 접근 D — Deep learning velocity 2세대 (DeepVelo, VeloVAE)** (Cui 2022 ref. 19, Gu/Blaauw/Welch 2022 ref. 20 — *둘 다 preprint*): cell-specific kinetic rate 시도 시작.
- **D의 한계 (분석자 판단)**: 본 paper가 D와 비교했을 때, simulation에서 DeepVelo error rate 51.62% (boost) / 82.16% (forward branching) / 44.99% (backward), VeloVAE 46.95% / 58.82% / 62.66%로 *cellDancer 대비 4–30배 큼* (Supp Table 1). 외부 맥락: DeepVelo·VeloVAE 둘 다 본 paper 시점 *preprint*였고 published 버전은 그 이후 출현 — 따라서 본 paper의 비교는 *당시 preprint snapshot*에 한정.
- **이 논문으로 이어지는 gap** (§Introduction p2): cell subpopulation별 *dissimilar kinetics*가 본질적이라면, *gene별로 모든 cell에 단일 ODE parameter*를 fit하는 framework로는 multi-stage·multi-lineage transition을 정확히 다룰 수 없다 → *cell-specific* $(\alpha, \beta, \gamma)$를 *local neighbor information*만으로 학습할 수 있는 framework가 필요.

### 기본 개념

- **RNA velocity 기본 (refs 12, 17)**: 한 gene의 unspliced mRNA $u(t)$와 spliced mRNA $s(t)$ 사이 mass-action 관계 $du/dt = \alpha - \beta u$, $ds/dt = \beta u - \gamma s$. $du/dt$의 부호로 *유도(induction)* 또는 *억제(repression)* 상태를 판정. 모든 gene을 종합한 $(u, s)$ phase portrait의 *위치*가 cell의 *순간적 미래 방향*을 표시.
- **Phase portrait의 hysteresis**: $u$ vs $s$ scatter에서 cell이 *반시계 방향*으로 이동 — induction 상승 phase에서는 $u$ 우선 상승, repression에서는 $u$ 우선 하강. velocyto·scVelo는 이 *전체 portrait*에 *gene별로 단일 $\alpha, \beta, \gamma$*를 fit.
- **MURK gene (multiple rate kinetics)** (Barile 2021, ref. 18, §Introduction p2): erythroid maturation 중 transcription rate가 *단계마다 boost*되는 89개 gene (Hba-x, Smim1, Blvrb, Mllt3, Hbb-y 포함). single $\alpha$ assumption으로는 *분화 중간에 phase portrait가 위로 꺾이는* 패턴이 *반대 방향 차원*으로 해석됨.
- **Branching gene** (refs 12, 18): 여러 lineage에서 *서로 다른 transcription/splicing rate*로 발현되는 gene (Ntrk2, Gnao1, Psd3 등). 한 lineage에서는 induction, 다른 lineage에서는 repression — single ODE로 fit하면 *중간 평균값*이 나옴.
- **Relay velocity** (본 paper의 신 개념, §Introduction p2): 각 cell $j$의 *local neighbor* $\{j'\}$가 *순간적 future state*의 proxy. predicted next state $(u(t_j + \Delta t), s(t_j + \Delta t))$가 neighbor $j'$ 중 *하나*의 관측 displacement $(u_{j'} - u_j, s_{j'} - s_j)$와 *cosine similarity*가 가장 큰 방향이면 그 cell의 $\theta_j$가 정답. *global latent time 추정 없음*.

### 이 논문이 필요성

- **핵심 이유**: heterogeneous cell population에서 *모든 cell에 단일 kinetic rate*는 잘못된 assumption — 특히 MURK gene과 branching gene에서 *velocity 방향이 역전*된다는 *경험적 증거*가 이미 보고됨 (Barile 2021, ref. 18; La Manno 2018, ref. 12). 그래서 *cell-specific* $(\alpha, \beta, \gamma)$ inference framework가 필요.
- **기존 방법으로 부족했던 지점**: scVelo dynamical model은 *gene-shared latent time* 추정에 강하지만 *cell-specific kinetics*는 binary on/off ($\alpha \in \{0, \alpha_g\}$)로만 표현. velocyto는 *steady-state* 가정 자체가 transient에 부적합. DeepVelo·VeloVAE는 *동시기 preprint*로 cell-specific 시도했지만 simulation accuracy가 cellDancer 대비 *4–30배 낮음* (Supp Table 1).
- **이 논문이 해결하려는 방향**: gene별 DNN으로 $(u, s) \to (\alpha, \beta, \gamma)$ mapping을 학습. *cosine similarity max over local neighbor*를 loss로 두면 *global latent time을 추정하지 않고도* cell-specific kinetics를 회복. ODE의 *analytic solution이 필요 없음* → 다른 ODE (protein velocity, multi-omic chromatin velocity) 확장 가능 (§Discussion p9, future work).

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: scRNA-seq의 cell × gene matrix에서 *cell-gene 단위*의 transcription/splicing/degradation rate $(\alpha_j, \beta_j, \gamma_j)_i$ (gene $i$, cell $j$)를 추정. *latent time 추정 명시적으로 회피*.
- **입력** (§Methods "Modeling RNA transcriptional dynamics", p11): gene $i$에 대해 모든 cell $j = 1, \dots, n$의 normalized $(u_j^i, s_j^i)$ vector. *gene별 독립* — 각 gene이 자체 DNN을 학습.
- **출력**: cell-specific $(\alpha_j^i, \beta_j^i, \gamma_j^i)$ + extrapolated next-step $(u_j^i(t + \Delta t), s_j^i(t + \Delta t))$.
- **추정 대상**: DNN parameter $\theta_i$ (gene 단위). cell-specific kinetic rate는 $\theta_i$를 통해 *입력 $(u, s)$의 함수*로 구해짐 (recoverable function, not free parameter).
- **중요한 hidden assumption**:
  - cell $j$의 *local neighbor* $\{j'\}$ 중 *cosine-best-fit* 하나가 cell $j$의 *next time step 진짜 위치*에 가까움 (Eq. 7).
  - sigmoid activation으로 $(\alpha, \beta, \gamma) \in [0, 1]$ 로 *정규화* — *absolute time scale*은 inferable 하지 않음 (§Discussion p9, 본문 명시: "it is unfeasible to infer the absolute magnitude of the RNA velocity ... using only scRNA-seq data").
  - *self-supervised* — ground truth velocity label 없음, 모든 supervision이 neighbor displacement cosine에서.

### 확률 / 통계학적 구조

- **Model family**: model-based deep neural network + first-order ODE 외삽 + *deterministic cosine loss*. *확률 모델 아님* — explicit likelihood / prior / posterior 없음. *discriminative* mapping $\Phi_\theta: (u, s) \to (\alpha, \beta, \gamma)$.
- **DNN architecture** (§Methods p11, Eq. 3): input layer $2n$ nodes (gene의 모든 cell $u, s$) → fully-connected hidden layer 1 (100 nodes, leaky ReLU) → hidden layer 2 (100 nodes, leaky ReLU) → output layer $3n$ nodes (sigmoid, $\alpha, \beta, \gamma \in [0, 1]$).
- **Discretized ODE** (Eq. 4–5):
$$u(t + \Delta t) - u(t) = \Delta t \cdot \left[ \alpha(u(t), s(t)) - \beta(u(t), s(t)) \cdot u(t) \right]$$
$$s(t + \Delta t) - s(t) = \Delta t \cdot \left[ \beta(u(t), s(t)) \cdot u(t) - \gamma(u(t), s(t)) \cdot s(t) \right]$$
- **Loss function** (Eq. 6–9):
$$\mathcal{L} = \sum_{j=1}^{n} \mathcal{L}_j, \quad \mathcal{L}_j = 1 - \max_{\{j'\}} \frac{v_j \cdot v'_j}{\|v_j\| \cdot \|v'_j\|}$$
where $v_j = (u_j(t + \Delta t) - u_j(t), s_j(t + \Delta t) - s_j(t))$ (predicted velocity) and $v'_j = (u_{j'} - u_j, s_{j'} - s_j)$ (observed displacement to neighbor $j'$).
- **Neighbor 정의** (§Methods p11, Eq. 7 직후): `n_neighbors` parameter로 제어. *gene-specific* (gene별 phase space neighbor) 또는 *gene-shared* (embedding space neighbor: spliced-only 또는 spliced+unspliced) 둘 다 가능.
- **Inference / optimization**: Adam optimizer, learning rate $0.001$, weight decay $0.004$ (L2 regularization), sigmoid output regularization, early stopping (loss decrease 없으면 3 checkpoint 후 종료). PyTorch Lightning 구현 (ref. 49).
- **수치 부담** (§Methods p11, Model parameters): time increment $\Delta t = 0.5$, *permutation ratio* (epoch당 sampled cell 비율) dataset 크기에 따라 0.1–0.5 — 작은 dataset (pancreas 3,696 cells) 0.5, 큰 dataset (hippocampus 18,140 cells) 0.1. *gene별 독립 DNN* → multi-processing 병렬화 가능 (§Discussion p9, Extended Data Fig. 10).

### 핵심 method insight

- **기존 방법의 한계**:
  - velocyto: $\alpha$ constant + steady-state assumption — *모든 cell에 동일 rate*. heterogeneous regime에서 inversion.
  - scVelo dynamical: $\alpha \in \{0, \alpha_g\}$ binary + *gene별로 latent time이 따로 추정* → MURK gene boost 또는 branching gene lineage-specific rate 분리 불가.
  - DeepVelo·VeloVAE: cell-specific 시도하지만 simulation에서 error rate $> 40\%$ (Supp Table 1) — *neighbor information을 약하게 사용* 또는 *latent time이 여전히 global*. 미제공: cellDancer 본문은 DeepVelo·VeloVAE의 구체 architecture 차이를 명시하지 않음.
- **이 논문의 바꾼 가정**:
  - velocity inference를 *generative likelihood maximization*에서 *discriminative cosine similarity max over neighbor* 로 전환 — *latent time 추정 회피*.
  - *cell-gene 단위* $(\alpha_j^i, \beta_j^i, \gamma_j^i)$ — DNN의 *입력 $(u, s)$를 통해 함수형으로 표현*, parameter explosion 없음.
- **새로 추가한 변수 또는 구조**: *local neighbor cosine loss* + *gene별 독립 DNN* + *discretized ODE 외삽*. 세 구조가 결합되어 *gene-shared latent time이 필요 없는* end-to-end framework 생성.
- **이 변화가 중요한 이유**:
  - latent time 회피 → multi-lineage branching에서 *lineage 간 time scale 차이*가 자동 처리됨.
  - cell-specific rate → MURK gene boost가 *cell-by-cell로 직접 표현*됨 (cluster 1–8 GO enrichment 가능, Fig. 2e-f).
  - ODE analytic solution 불필요 → 다른 ODE (protein velocity, multi-omic chromatin)로 일반화 가능 (§Discussion p9 — 이 점이 *MoFlow `@hong2026moflow`로 직접 이어짐*).

### 이전 방법과의 차이

| 차이 | velocyto (steady) | scVelo dynamical | cellDancer |
|---|---|---|---|
| $\alpha$ 형태 | constant | binary on/off | cell-specific (DNN output) |
| $\beta, \gamma$ | gene-shared | gene-shared | cell-specific (DNN output) |
| Latent time | 없음 (steady-state) | gene별 latent time inference | *없음* — neighbor displacement만 |
| Loss / objective | linear regression | full likelihood maximization | *cosine similarity max over neighbor* |
| Multi-lineage 처리 | 불가 | gene-shared time으로 부분만 | 자동 (lineage 간 time scale 무관) |
| Multi-rate (MURK) | 불가 | boost 방향 inversion | cell-specific $\alpha$로 직접 표현 |
| ODE 확장성 | 어려움 (analytic solution 필요) | 어려움 | *쉬움* (discretized only) |

- **차이가 크게 나타나는 조건** (Supp Table 1):
  - transcriptional boost: cellDancer 13.25% vs scVelo 46.88% (3.5× 차이).
  - multi-forward branching: cellDancer 2.63% vs scVelo 40.57% (15× 차이).
  - multi-backward branching: cellDancer 9.43% vs scVelo 31.13% (3.3× 차이).
  - 해석: branching에서 가장 큰 차이 — *gene-shared latent time이 lineage를 강제로 한 timeline에 압축*하는 scVelo의 가정이 가장 깨지는 regime.

### 효과가 Results에서 나타난 방식

- **Erythroid maturation** (Fig. 2a, p3): cellDancer는 hematoendothelial progenitor → blood progenitor 1 → blood progenitor 2 → erythroid 1/2/3 *정방향* UMAP flow 회복. scVelo·DeepVelo는 erythroid 3 → blood progenitor 2 *역방향* (Extended Data Fig. 2b). MURK gene만 사용한 별도 분석에서도 cellDancer만 정방향 (Fig. 2c).
- **Hippocampus branching** (Fig. 3a, p5): 5 lineage (granule, CA1-sub, CA2-3-4, OPC, astrocyte) 정확. radial glia가 *자동으로* root state로 식별 (Fig. 3e, ref. 32와 일치). Ntrk2 phase portrait에서 cellDancer만 *두 branch 모두* 맞춤 — astrocyte/OPC upper branch (high $\alpha$, low $\beta$), neuron lower branch (high $\beta$, low $\gamma$) (Fig. 3b, Extended Data Fig. 3).
- **Pancreas kinetic identity** (Fig. 4d, p7): $(\alpha, \beta, \gamma)$ UMAP이 alpha/beta/delta/epsilon cell을 *gene expression UMAP보다 더 명확히* 분리. ductal cell에서 *cycling subpopulation* 분리 (Fig. 4e) — kinetic rate가 *gene expression이 못 잡는 cell cycle 정보*를 표현.
- **Ablation 부재**: 본 paper는 *loss function의 cosine vs L2*, *DNN 깊이 (2 hidden layer)*, *neighbor 개수* 같은 *core component ablation을 명시 제공하지 않음*. `미제공: ablation table 없음`. Extended Data Fig. 9는 *stopping criteria (checkpoint, patience)* 만 sensitivity 분석.
- **Gata2 perturbation** (Fig. 2g, p5): dynamo (ref. 22)와 통합해 *in silico Gata2 suppression* — blood progenitor 1에서 hematopoietic fate diversion 관찰, 실험 (Eich 2018, ref. 23)과 일치. *cellDancer 자체의 perturbation 모델은 아님* — downstream tool 통합.

### Method 관점의 한계

- **약한 assumption** (저자 명시 + 분석자):
  - *neighbor가 future state proxy* — neighbor graph 품질에 sensitive. 본문은 spliced-only vs spliced+unspliced neighbor 비교만 (Extended Data Fig. 7a) — *graph construction algorithm* (KNN, UMAP, PHATE 등) sensitivity는 `미제공:`.
  - sigmoid output $[0, 1]$ → *absolute time scale 회복 불가* (§Discussion p9 본문 명시).
  - *gene별 독립 DNN* → gene 간 *공동 regulation* (TF cascade 등)은 *모델 안에서 표현 안 됨* — downstream dynamo에 의존.
- **구현 또는 학습상의 부담**:
  - gene별 DNN $\to$ 18k cells × 2,159 genes = 1 job 286 분, 15 jobs 40 분 (Extended Data Fig. 10). 작은 dataset (pancreas 3,696 cells)은 빠르지만, full atlas (millions cells × 20k genes) 적용 시 재현 비용 *재검토 필요*.
  - hyperparameter (permutation ratio, neighbor 수)가 dataset마다 *다른 default* (§Methods Model parameters p12) — *automatic tuning 없음*.
- **일반화가 불확실한 조건**:
  - *극단적으로 작은 dataset* (< 500 cells/lineage): 본문은 1,000 cells까지만 sparse simulation (Extended Data Fig. 8c).
  - *very high gene number* (40k+): 본문 demo gene 수 최대 2,159.
  - *cross-batch / multi-sample*: 본문은 *single sample* 단위 분석만 — batch effect 처리 부재. 미제공.
  - *chromatin / multi-omic*: 본문이 *RNA-only* — chromatin accessibility 통합은 §Discussion에서 "could be likewise included" 로만 future direction (p9). 이 future direction을 실제 구현한 것이 *MoFlow `@hong2026moflow`* 와 *MultiVelo `@li2023multivelo`*.

---

## Results

### Dataset별 결과

#### Dataset 1 — Simulation (mono-kinetic + 3 multi-rate regime)

- **Dataset**: 자체 SciPy `integrate.solve_ivp` Runge–Kutta 생성 simulation (§Methods Simulation details, p11–12). 4 regime: mono-kinetic (1,000 genes shared $\beta, \gamma$, two-step $\alpha$); transcriptional boost (2,000 cells × 1,000 genes, $\alpha$ pre-boost $\sim U(1.6, 2.4)$ → post-boost $\sim U(4, 6)$); multi-forward branching (2,000 × 1,000, lineage 1 $\alpha \sim U(0.8, 1.2)$ vs lineage 2 $\alpha \sim U(4, 6)$); multi-backward branching ($\alpha = 0$, $\beta, \gamma \sim U(0.9, 1.1)$, lineage start point 다름).
- **목적**: ground truth 있는 조건에서 baseline 5개 (cellDancer, scVelo, velocyto, DeepVelo, VeloVAE) 정확도 비교.
- **데이터 규모**: 4 regime × 1,000 genes = 4,000 simulated genes; 2,000 cells per regime.
- **Baseline**: scVelo dynamical, velocyto static, DeepVelo (preprint), VeloVAE (preprint).
- **Metric**: *error rate* = "percentage of cells whose predicted RNA velocity is poorly correlated with the ground truth velocity (cosine similarity < 0.7)" (§Methods p12, Extended Data Fig. 1 caption).
- **주요 수치** (Supp Table 1):
  - Transcriptional boost: cellDancer **13.25%** | scVelo 46.88% | velocyto 56.12% | DeepVelo 51.62% | VeloVAE 46.95%.
  - Multi-forward branching: cellDancer **2.63%** | scVelo 40.57% | velocyto 67.67% | DeepVelo 82.16% | VeloVAE 58.82%.
  - Multi-backward branching: cellDancer **9.43%** | scVelo 31.13% | velocyto 15.30% | DeepVelo 44.99% | VeloVAE 62.66%.
  - Mono-kinetic accuracy: cellDancer predicted $\alpha/\beta$, $\gamma/\beta$ Pearson $R^2 = 0.98$ (α/β), $0.93$ (γ/β) vs ground truth (Extended Data Fig. 1a). 미제공: 다른 baseline의 동일 $R^2$ 수치 본문 부재.
- **통계 유의성**: $P < 0.001$ one-sided Wilcoxon test for all three regimes (Extended Data Fig. 1c-e caption, n = 1,000 genes). multiple testing correction *명시 없음* — `검토필요: 3 regime × pairwise 5 method 비교에 BH 보정 적용 여부 본문에 미기재.`
- **정성 결과**: cellDancer는 *two-step $\alpha$ prior 없이*도 active/repressive cluster 자동 분리 (Extended Data Fig. 1b); cell 분포 imbalance (post-boost cell downsampling, lineage 1/2 imbalance) 영향 적음 (Extended Data Fig. 1c-e).
- **재현성**: 4 regime × 1,000 genes 각각 $P < 0.001$ — *regime 간 재현*. 다른 random seed / cohort 비교는 미제공.
- **논문 주장과의 연결**: simulation에서 cellDancer가 baseline 4개를 *3.3–15× outperform* — multi-rate kinetics inference 우월성의 *quantitative anchor*.

#### Dataset 2 — Mouse gastrulation erythroid maturation (Pijuan-Sala 2019)

- **Dataset**: 10x Chromium scRNA-seq, E7.0–E8.5 mouse gastrulation embryo, ArrayExpress **E-MTAB-6967** (ref. 2).
- **목적**: MURK gene (transcription boost) 존재 시 baseline의 *방향 역전*을 실제 dataset에서 보일 수 있는가.
- **데이터 규모** (§Methods scRNA-seq pre-processing p12): **12,329 cells**, cell type = hematoendothelial progenitors / blood progenitors 1/2 / erythroid 1/2/3. 89 MURK genes (Barile 2021 ref. 18 정의). scVelo default + 100 nearest neighbors first moment.
- **Baseline**: scVelo dynamical, DeepVelo, VeloVAE.
- **Metric**: UMAP velocity flow 정성 평가 + MURK-only flow 정성 평가 + GO pathway enrichment (DAVID, BH-corrected, ref. 21).
- **주요 수치**:
  - cellDancer만 정방향 UMAP flow (Fig. 2a, top); scVelo 역방향 (Fig. 2a, bottom); DeepVelo·VeloVAE 부분 역방향 (Extended Data Fig. 2b).
  - 8개 gene cluster GO enrichment (Fig. 2e-f): cluster 7–8이 *erythrocyte development*, *heme biosynthetic process*, *oxygen transport*, *cellular oxidant detoxification* — *erythroid 2/3에서 발현 증가*와 일치.
  - 정확한 p-value scale (Fig. 2f color bar): 0 ~ 1 (각 cluster별 pathway enrichment FDR). 정확한 셀별 q-value는 *원문 Fig. 2f 참조 — 본문 prose에 숫자 미기재*.
- **통계 유의성**: GO enrichment는 DAVID Fisher's exact + BH correction. 미제공: UMAP flow의 *정량적* directional accuracy metric (예: CBDir) — 본 paper는 시각적 평가만.
- **정성 결과**: in silico Gata2 suppression (dynamo, ref. 22)으로 blood progenitor 1에서 hematopoietic fate 분기 확인 — Eich 2018 (ref. 23) 실험과 일치 (Fig. 2g).
- **재현성**: *단일 dataset, 단일 cohort*. cross-lab replication 없음.
- **논문 주장과의 연결**: scVelo의 *known failure case* (MURK gene)를 cellDancer가 *해결한다는 정성 증거*. quantitative metric 부재가 한계.

#### Dataset 3 — Mouse hippocampal dentate gyrus neurogenesis (Hochgerner 2018)

- **Dataset**: 10x Chromium scRNA-seq, postnatal mouse hippocampus, **GSE95753** (ref. 53). loom file: `http://pklab.med.harvard.edu/velocyto/DentateGyrus/DentateGyrus.loom`.
- **목적**: multi-lineage branching (5 lineage)에서 branching gene 처리 능력.
- **데이터 규모**: **18,140 cells × 2,159 genes** (§Methods p12, La Manno 2018 ref. 12 filtering). cell type 10개 (CA, CA1-sub, CA2-3-4, Granule, Neuroblast, nIPC, Radial glia, Glia progenitor, OPC, Astrocyte).
- **Baseline**: scVelo dynamical, velocyto static, DeepVelo, VeloVAE.
- **Metric**: t-SNE velocity flow + phase portrait 정확성 + GO enrichment + pseudotime root state 자동 식별.
- **주요 수치**:
  - 5 lineage 모두 정확 (Fig. 3a). radial glia가 자동으로 root state로 식별 — Malatesta 2003 (ref. 32) 일치.
  - branching gene Ntrk2: cellDancer 두 branch 모두 정확 (Fig. 3b). astrocyte/OPC upper branch (high $\alpha$, low $\beta$, unspliced 우위); neuron lower branch (high $\beta$, low $\gamma$, spliced 우위) (Extended Data Fig. 3).
  - Loss-rank top 500 gene GO enrichment (Fig. 3d, BH-corrected Fisher's exact $P < 0.05$): neurogenesis $1.25 \times 10^{-12}$, generation of neurons $4.96 \times 10^{-12}$, nervous system development $9.14 \times 10^{-12}$, neuron differentiation $8.96 \times 10^{-10}$, brain development $4.00 \times 10^{-3}$, modulation of synaptic transmission $6.22 \times 10^{-3}$.
  - 5 terminal state + most probable path (Fig. 3e, dynamo integration): astrocyte/OPC가 granule/pyramidal neuron보다 *먼저* 생성 — Malatesta 2003 일치.
- **통계 유의성**: GO p-value는 BH-corrected one-sided Fisher's exact $P < 0.05$. *velocity directional accuracy의 정량 p-value*는 미제공.
- **정성 결과**: Dcx는 neuroblast에서 *transient upregulation* — Brown 2003 ref. 33, Couillard-Despres 2005 ref. 34 일치. Psd3는 branching pattern 명확 (Fig. 3f).
- **재현성**: 본 paper 단일 분석. supplementary Fig. 2가 동일 dataset의 *추가 branching gene* (Syt11, Klf7, Gnao1, Dctn3, Gpm6b, Psd3, Ntrk2, Slc1a3, Astn1, Cadm1)을 baseline과 비교 — *모두 cellDancer가 정확*하다는 주장.
- **논문 주장과의 연결**: branching gene 처리가 *cellDancer의 핵심 우위 영역* — simulation의 multi-forward branching error rate 2.63% (Supp Table 1)와 일치하는 real-data 증거.

#### Dataset 4 — Mouse pancreatic endocrinogenesis (Bastidas-Ponce 2019)

- **Dataset**: 10x Chromium scRNA-seq, E15.5 mouse pancreas, **GSE132188** (ref. 36).
- **목적**: cell-specific kinetic rate $(\alpha, \beta, \gamma)$가 *cell identity marker*로 사용 가능한지.
- **데이터 규모**: **3,696 cells × 2,000 genes** (scVelo Bergen 2020 ref. 17 filtering). cell type: ductal / Ngn3-low EP / Ngn3-high EP / pre-endocrine / alpha / beta / delta / epsilon.
- **Baseline**: scVelo dynamical (downstream dynamo for vector field analysis).
- **Metric**: kinetic rate UMAP의 cell type 분리 + Jacobian analysis (Arx vs Pax4).
- **주요 수치**:
  - $(\alpha, \beta, \gamma)$ UMAP이 alpha/beta/delta/epsilon cell을 *gene expression UMAP보다 명확히* 분리 (Fig. 4d, Supp Fig. 3). 정량 separation score는 미제공.
  - ductal cell에서 *cycling subpopulation* 분리 (Fig. 4e) — gene expression UMAP에서는 안 보임.
  - Jacobian analysis (dynamo, ref. 22): Arx가 Pax4를 *downregulate* (alpha cell), Pax4가 Arx를 *downregulate* (beta cell) — Li 2015 ref. 38, Hoffman 2008 ref. 39 일치.
- **통계 유의성**: 정량 separation score / classification accuracy 미제공.
- **정성 결과**: emitting fixed point가 *pancreas progenitor*에 위치, absorbing fixed point가 alpha/beta/epsilon cell에 — *cell fate determination*의 시각적 일치 (Fig. 4f).
- **재현성**: 단일 dataset. cross-cohort 없음.
- **논문 주장과의 연결**: cellDancer의 추가 가치 — *kinetic rate 자체가 cell identity indicator*, gene expression 차원의 *상위 또는 보조 feature*.

#### Dataset 5 — Mouse RPE1-FUCCI cell cycle (scEU-seq, Battich 2020)

- **Dataset**: scEU-seq metabolic labeling, RPE1-FUCCI cell line cell cycle, **GSE128365** (ref. 40).
- **목적**: cellDancer가 추정한 $\alpha, \gamma$가 *실험적으로 측정된 synthesis/degradation rate* (metabolic labeling)와 일치하는가 — *ground truth가 있는 real-data benchmark*.
- **데이터 규모**: **3,058 cells × 2,000 high variable genes** from *pulse experiment* (§Methods p12). unspliced = labeled + unlabeled 합산. 300 nearest neighbors first moment.
- **Baseline**: scEU-seq experimentally derived synthesis/degradation rates (molecules per hour) — Battich 2020 ref. 40 데이터.
- **Metric**: heatmap correlation (Extended Data Fig. 5b), phase portrait alignment (Extended Data Fig. 5c).
- **주요 수치**: 정확한 correlation 수치는 본문 prose에 미기재 — Extended Data Fig. 5 caption에 *qualitative association* 만 명시. "predicted $\alpha$ and $\gamma$ are associated with the experimental measurements of mRNA synthesis and degradation, especially in the highly expressed genes" (p8).
- **통계 유의성**: 미제공 — Pearson r, p-value 본문 부재. `검토필요: Extended Data Fig. 5b heatmap에서 정확한 numerical correlation 추출 필요.`
- **정성 결과**:
  - G1 state low-expression gene에서 cellDancer $\alpha > 0$ vs scEU-seq synthesis rate $\approx 0$ — 저자는 *scEU-seq의 low-expression gene 한계*로 해석 (p8).
  - 7 cluster of $\alpha, \gamma$ dynamic pattern (Extended Data Fig. 6a-b): 3 positive correlation + 4 negative correlation — *turnover strategy diversity*.
  - cluster F (high $\alpha$, high $\gamma$ at mitosis): *signal transduction*, *TGF-β signaling*, *stress-activated protein kinase* — mitosis 중 빠른 cell communication 가설.
  - 17 Leiden subpopulation 중 cluster 3/4 (M phase 일부)가 *cluster 1/2 (G1/S)* 와 reaction rate 유사 (Extended Data Fig. 6d-e) — *gene expression이 못 잡는 cell subpopulation* 식별.
  - 116 differentially expressed gene + 181 differential $\alpha$ rate gene, 그 중 *10% overlap*만 — 163 gene이 *kinetic rate로만 식별* (Extended Data Fig. 6f). 이 163 gene이 *cytokinesis, cell division, mitotic metaphase congression* 에 enriched (Extended Data Fig. 6g).
- **재현성**: scEU-seq 실험 데이터와의 일치가 *외부 ground truth 기반 재현*. 단일 cell line (RPE1).
- **논문 주장과의 연결**: cellDancer 추정 rate가 *임의 fitting 아닌 진짜 kinetic rate*에 가깝다는 증거 — 다른 dataset의 결과 해석 신뢰도 향상.

#### Dataset 6 — Human embryonic glutamatergic neurogenesis

- **Dataset**: human forebrain 10 weeks post-conception scRNA-seq, SRA **SRP129388** (refs 12, 42). loom file: `https://github.com/pachterlab/GFCP_2022/blob/main/notebooks/data/hgForebrainGlut.loom`.
- **목적**: cross-species (human) generalization + neighbor detection 방법 (spliced-only vs spliced+unspliced) sensitivity.
- **데이터 규모**: **1,054 cells × 1,720 genes** (highly variable, scanpy `pp.highly_variable_genes` default). 200 nearest neighbors first moment.
- **Baseline**: cellDancer 자체 변형 (neighbor 정의 차이) — *외부 baseline 비교 없음*.
- **Metric**: UMAP velocity flow + gene-specific phase portrait (ELAVL4 ref. 43, DCX refs 33–34).
- **주요 수치**: 정량 수치 본문 부재 — *정성 일치*만 (Extended Data Fig. 7).
- **통계 유의성**: 미제공.
- **정성 결과**: spliced-only neighbor vs spliced+unspliced neighbor 결과 *consistent* (Extended Data Fig. 7a) — neighbor 정의에 *robust*.
- **재현성**: 단일 sample.
- **논문 주장과의 연결**: cross-species + neighbor sensitivity 점검. 정량 평가 부재.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**:
  - cellDancer는 *cell heterogeneity가 큰 regime* (multi-stage transcriptional boost, multi-lineage branching)에서 baseline 대비 *3.3–15× 낮은 error rate* (Supp Table 1).
  - kinetic rate UMAP이 *cell identity marker* 로 사용 가능 (pancreas Fig. 4d, cell cycle Extended Data Fig. 6).
  - dropout 50–70%, cell 1k–10k sparse data에서 *robust* (Extended Data Fig. 8).
  - real-data ground truth (scEU-seq) 와 *qualitative consistency* — 정량 수치는 미제공.
- **가장 중요한 수치**:
  - Simulation error rate: **cellDancer 2.63% (multi-forward branching) vs DeepVelo 82.16%** — 본 paper의 *flagship number*.
  - Dropout robustness: Pearson $R^2 > 0.96$ ($\alpha/\beta$), $> 0.84$ ($\alpha/\gamma$) at dropout 70% (Extended Data Fig. 8b).
  - Runtime (18,140 cells × 2,159 genes): 286 min (1 job) → 36 min (30 jobs), saturation at 15 jobs / 40 min / 53 genes per minute (Extended Data Fig. 10).
- **Baseline 대비 차이**: simulation에서 *3.3–15× error rate 감소*. real-data에서는 *quantitative metric 부재* — 정성 비교 (UMAP flow direction)만.
- **결과 해석 시 주의점**:
  - real-data benchmark (erythroid, hippocampus, pancreas, human neurogenesis) 모두 *정량 directional accuracy metric (CBDir 등) 없음* — 시각적 평가만. 외부 후속 paper (예: MoFlow `@hong2026moflow`)가 동일 cellDancer를 CBDir로 재평가했을 때 *MultiVelo 대비 낮음* (HSPC: cellDancer $-0.056$ vs MultiVelo $0.063$, MoFlow $0.191$; SHARE-seq: cellDancer $0.026$ vs MoFlow $0.144$). 본 paper의 정성 평가가 *cellDancer 우위 영역만 cherry-pick*했을 가능성 — `검토필요: chromatin-aware dataset (SHARE-seq, multiome)에서는 cellDancer가 chromatin 활용 안 하므로 본질적으로 약한 baseline이라는 점 추가 검토.`
  - simulation regime 4종이 *저자 자신이 정의* — *third-party benchmark suite* (예: scRNA-seq dynamical benchmark) 부재.
  - scEU-seq comparison이 *정량 correlation 수치 없음* — heatmap 시각적 평가만.
  - cell cycle confound: pancreas Fig. 4e는 *ductal cycling cell*만 식별, *전체 dataset의 cell cycle covariate 통제* 없음.
  - multiple testing correction은 *GO enrichment*에만 적용 (BH), *velocity inference benchmark*에는 미적용 — `미제공: simulation regime × method × metric 다중 비교 보정.`

---

## Figures

### Figure 1 — cellDancer workflow

- **이 Figure가 필요한 이유**: 본 paper의 핵심 주장이 "*local relay velocity가 cell-specific kinetics를 회복한다*"라는 *방법론적 contribution*이므로, *workflow 개념*을 한 장에 시각화해야 reader가 이후 모든 Result Figure를 이해 가능.
- **이 Figure가 뒷받침하는 주장**: cell $i$의 $(\alpha, \beta, \gamma)$가 *neighbor cell의 future state*로부터 *cosine similarity 최대화*를 통해 학습된다는 *알고리즘적 골격*.

#### 패널별 설명

- **a**: Transcription dynamics schematic. premature (unspliced) → splicing → mature (spliced) → degradation 의 3-step kinetics. cell $t$의 $(\alpha, \beta, \gamma)_t$는 *neighbor cell*이 *future state proxy*를 제공한다는 가정. *그림은 BioRender로 작성* (Acknowledgements p13).
- **b**: cellDancer DNN architecture. 3 step:
  - Step 1: 모든 cell $i = 1, \dots, n_{\text{cells}}$의 $(u_i, s_i)$ → input layer ($2n$ nodes) → hidden layer 1 (100 nodes) → hidden layer 2 (100 nodes) → output layer ($3n$ nodes, sigmoid) → $(\alpha_i, \beta_i, \gamma_i)$.
  - Step 2: predicted $(\alpha, \beta, \gamma)$로 next-step $(u_i(t + \Delta t), s_i(t + \Delta t))$ 계산.
  - Step 3: loss $\mathcal{L} = \sum (1 - \cos \theta_i)$, 여기서 $\theta_i$는 predicted velocity vs observed neighbor displacement 각도. minimize → DNN weight 업데이트.
- **c**: training progress 시각화. *Sulf2* (mono-kinetic, pancreas), *Gnao1* (multi-lineage branching, hippocampus) 2 gene의 phase portrait이 training epoch 진행하며 *cellDancer가 ground truth pattern으로 수렴*하는 모습.

#### 본문에서 강조한 비교

- **비교 대상**: scVelo/velocyto의 *global ODE fitting* vs cellDancer의 *local neighbor cosine similarity*.
- **관찰된 차이**: cellDancer는 *각 cell의 $\theta_i$를 독립적으로 update* — global latent time 없이.
- **이 차이가 의미하는 것**: cell-specific kinetics가 *parameter-explosion 없이* (DNN parameter $\theta_i$는 *gene별 고정 크기*) 학습 가능.

#### 해석 시 주의점

- **주의점**: Figure 1c는 *2 gene의 cherry-picked example* — training convergence가 *모든 gene에서 항상 같다는 보장은 없음*. transcriptional boost gene은 *100 epoch* 필요한 반면 mono-kinetic은 *25 epoch*에서 수렴 (Extended Data Fig. 1f-i). gene별 학습 시간 *heterogeneity*는 Figure 1c만으로 안 보임.

### Figure 2 — Transcriptional boost in erythroid maturation

- **이 Figure가 필요한 이유**: scVelo의 *known failure case* (MURK gene, Barile 2021 ref. 18 보고)를 cellDancer가 해결한다는 *real-data 핵심 증거*.
- **이 Figure가 뒷받침하는 주장**: cell-specific $\alpha$가 *transcriptional boost*를 *cell-by-cell로 표현* → 방향 정확.

#### 패널별 설명

- **a**: gastrulation erythroid UMAP velocity flow. 상단 cellDancer 정방향 (progenitor → erythroid 3); 하단 scVelo 역방향. cell type 7 class (hematoendothelial progenitor, blood progenitor 1/2, erythroid 1/2/3).
- **b**: MURK gene Hba-x phase portrait + cell-specific $\alpha$. cellDancer는 정방향 velocity + cell-specific $\alpha$가 *progenitor 낮음 → erythroid 중간 boost → 후기 다시 낮음* 표현. scVelo·DeepVelo·VeloVAE는 *역방향 또는 부정확*.
- **c**: MURK gene 89개만 사용한 별도 UMAP flow. cellDancer 정방향 회복.
- **d**: cellDancer pseudotime UMAP. erythroid 3가 terminal로 식별.
- **e**: cellDancer pseudotime 따라 gene을 8 cluster로 분류. cluster 1–3 *progenitor에서 high*, cluster 4–6 *천천히 감소*, cluster 7–8 *erythroid에서 증가*.
- **f**: 각 cluster의 GO pathway enrichment (DAVID, BH-corrected). cluster 1–3 angiogenesis/vasculogenesis/wound healing; cluster 4–6 cell cycle/chromatin organization/RNA splicing/translation; cluster 7–8 erythrocyte development/heme biosynthesis/oxygen transport.
- **g**: dynamo in silico Gata2 suppression. blood progenitor 1에서 hematopoietic fate diversion (erythroid 갈라짐). 행렬 형태의 confidence matrix (0.00–1.00 fraction).

#### 본문에서 강조한 비교

- **비교 대상**: cellDancer vs scVelo (+ DeepVelo, VeloVAE in Extended Data Fig. 2b)의 *UMAP flow direction*.
- **관찰된 차이**: cellDancer 정방향 vs baseline 모두 역방향 또는 일부 역방향.
- **이 차이가 의미하는 것**: MURK gene의 *transcription boost*는 *cell-specific $\alpha$ 없이는* 정확 회복 불가.

#### 해석 시 주의점

- **주의점**:
  - *UMAP flow의 정확성 정량 metric 없음* — 시각적 평가만. CBDir 같은 외부 metric은 *후속 paper* (MoFlow)에서 측정됨.
  - cluster GO enrichment p-value의 *정확한 셀별 수치는 color bar* (0 ~ 1)로만 표시 — 본문 prose 수치 부재.
  - in silico Gata2 perturbation은 *dynamo의 downstream 결과* — cellDancer 자체 perturbation 검증 아님.

### Figure 3 — Hippocampus branching gene

- **이 Figure가 필요한 이유**: multi-lineage branching에서 *gene별로 lineage-specific kinetic rate*를 회복해야 한다는 simulation Result (multi-forward branching error rate 2.63% vs DeepVelo 82.16%)의 *real-data 검증*.
- **이 Figure가 뒷받침하는 주장**: 5 lineage 모두 정확 회복 + branching gene이 *lineage별 다른 $(\alpha, \beta, \gamma)$*.

#### 패널별 설명

- **a**: hippocampus t-SNE velocity flow (cellDancer). 5 lineage (granule, CA1-sub, CA2-3-4, OPC, astrocyte) 명확.
- **b**: Ntrk2 / Gnao1 phase portrait — 5 method 비교 (cellDancer, scVelo dynamic, velocyto, DeepVelo, VeloVAE). cellDancer만 두 branch 정확.
- **c**: 모든 gene의 *minimized loss score* 분포. low-loss gene = mono-kinetic 또는 divergent dynamics; high-loss gene = pattern-less.
- **d**: top 500 low-loss gene의 GO enrichment (Fisher's exact, BH, $P < 0.05$): neurogenesis ($1.25 \times 10^{-12}$), generation of neurons ($4.96 \times 10^{-12}$), nervous system development ($9.14 \times 10^{-12}$), neuron differentiation ($8.96 \times 10^{-10}$), neuron projection development ($1.46 \times 10^{-8}$), synaptic signaling ($1.57 \times 10^{-3}$), chemical synaptic transmission ($1.69 \times 10^{-3}$), brain development ($4.00 \times 10^{-3}$).
- **e**: cellDancer gene-shared pseudotime t-SNE + dynamo most probable path. 5 terminal state.
- **f**: Dcx (mono-kinetic, transient in neuroblast), Psd3 (branching, lineage별 다른 속도) 의 phase portrait + t-SNE expression + pseudotime expression profile.

#### 본문에서 강조한 비교

- **비교 대상**: branching gene Ntrk2 — cellDancer vs scVelo / velocyto / DeepVelo / VeloVAE.
- **관찰된 차이**: cellDancer만 두 branch (astrocyte/OPC vs neuron)의 *서로 반대 방향 velocity* 정확 표현.
- **이 차이가 의미하는 것**: gene-shared latent time을 강제하는 baseline은 *lineage 간 다른 time scale*을 압축해 부정확. cellDancer는 *latent time 회피*로 lineage별 독립.

#### 해석 시 주의점

- **주의점**:
  - "5 lineage 정확 회복" 평가가 *cell type label 기반 시각적 일치* — 정량 lineage classification accuracy 미제공.
  - top 500 gene GO enrichment의 *기준 (low-loss gene = biologically meaningful)*은 *순환 논리* 가능성 — cellDancer가 잘 fit한 gene이 *cellDancer 가정에 맞는 gene*일 가능성 (예: clean dynamics). high-loss gene이 *cellDancer 가정 위배 gene*일 수 있음. 외부 ground truth로 검증되지 않음.

### Figure 4 — Pancreas kinetic rate as cell identity

- **이 Figure가 필요한 이유**: cellDancer의 *secondary contribution* — kinetic rate $(\alpha, \beta, \gamma)$ 자체가 *cell identity marker*로 사용 가능하다는 *novel biological utility*.
- **이 Figure가 뒷받침하는 주장**: gene expression UMAP보다 *kinetic rate UMAP이 cell type 분리에 더 정확하거나 추가 정보 제공*.

#### 패널별 설명

- **a**: schematic — kinetic rate가 cell type 간 *expression보다 더 stable* 하다는 가설.
- **b**: pancreas UMAP velocity flow. 8 cell type (ductal, Ngn3-low EP, Ngn3-high EP, pre-endocrine, alpha, beta, delta, epsilon).
- **c**: Sulf2 phase portrait. cellDancer가 Ngn3-high EP에서 induction (high $\alpha$), pre-endocrine에서 regression (low $\alpha$) 정확 분리.
- **d**: $(\alpha, \beta, \gamma)$ UMAP. alpha/beta/delta/epsilon 분리. Supplementary Fig. 3에 $\alpha$, $\beta$, $\gamma$ 개별 UMAP.
- **e**: 같은 UMAP에서 cell cycle phase (G2M, S) 색상. ductal cell의 *cycling subpopulation* 분리.
- **f**: dynamo vector field. emitting fixed point (red 0) = pancreas progenitor. absorbing fixed point (black 1, 2, 3) = alpha/beta/epsilon.
- **g**: Arx vs Pax4 Jacobian analysis. Arx → Pax4 down (alpha cell); Pax4 → Arx down (beta cell). Li 2015 ref. 38 일치.

#### 본문에서 강조한 비교

- **비교 대상**: gene expression UMAP vs $(\alpha, \beta, \gamma)$ UMAP의 cell type 분리.
- **관찰된 차이**: kinetic rate UMAP이 alpha/beta/delta/epsilon을 *더 명확* 분리 + cycling subpopulation 추가 식별.
- **이 차이가 의미하는 것**: kinetic rate가 *transient transcriptional state*보다 *stable cell identity*를 더 잘 반영 — secondary feature로서 가치.

#### 해석 시 주의점

- **주의점**:
  - 정량 separation score (예: silhouette, ARI) 미제공.
  - cell cycle subpopulation 식별은 *anecdotal* — *주요 confound (cell cycle)을 control했는가*는 별도 검증 부재.
  - Jacobian analysis는 dynamo downstream — cellDancer 자체 regulatory inference 아님.

### Extended Data Figures (10개 — summary)

- **Extended Data Fig. 1**: simulation accuracy. (a) $\alpha/\beta$ $R^2 = 0.98$, $\gamma/\beta$ $R^2 = 0.93$ vs ground truth. (b) two-step $\alpha$ prior 없이도 active/repressive cluster 자동 분리. (c-e) 3 multi-rate regime의 error rate box plot (n = 1,000 genes per regime, 4 sampling ratio: 40/60/80/100%). (f-i) loss score vs epoch — mono-kinetic·branching 25 epoch 수렴, transcriptional boost 100 epoch.
- **Extended Data Fig. 2**: erythroid 추가 분석. (a) cellDancer가 MURK gene phase portrait 정확. (b) scVelo/DeepVelo/VeloVAE의 *역방향 UMAP*. (c) 4 MURK gene (Hba-x, Blvrb, Mllt3, Hbb-y)의 pseudotime profile. (d) long trajectory + pseudotime adjustment schematic.
- **Extended Data Fig. 3**: hippocampus branching gene 추가 (1) phase portrait + (2-4) cell-specific $\alpha, \beta, \gamma$ t-SNE + (5) expression.
- **Extended Data Fig. 4**: hippocampus gene pseudotime expression profile (선택 gene set).
- **Extended Data Fig. 5**: cell cycle (scEU-seq). (a) cell cycle group별 spliced/unspliced. (b) cellDancer $\alpha, \beta, \gamma$ vs scEU-seq synthesis/degradation heatmap — *qualitative association*. (c) phase portrait alignment. (d) FUCCI relative position에서 pseudotime 일치.
- **Extended Data Fig. 6**: cell cycle gene turnover strategy. (a) 7 cluster of $\alpha, \gamma$ dynamic. (b) 각 cluster의 normalized spliced/unspliced. (c) GO enrichment per cluster. (d) 3D UMAP (kinetic vs expression). (e) 17 Leiden cluster의 pseudotime box plot (n = 3,058 cells, 10–90 percentile whisker). (f) Venn diagram — expression DEG 116 + $\alpha$ DEG 181 — *10% overlap*만. (g) 163 $\alpha$-only DEG의 GO — cytokinesis, cell division, mitotic metaphase congression.
- **Extended Data Fig. 7**: human embryonic glutamatergic neurogenesis. (a) spliced-only vs spliced+unspliced neighbor UMAP — *consistent*. (b) gene-shared pseudotime. (c) ELAVL4, DCX phase portrait.
- **Extended Data Fig. 8**: dropout robustness + cell number sparsity. (a) 70% dropout simulation. (b) Pearson $R^2 > 0.96$ ($\alpha/\beta$), $> 0.84$ ($\alpha/\gamma$) at 50/60/70% dropout. (c) 1k–10k cells에서 $\alpha/\beta$, $\alpha/\gamma$ 안정.
- **Extended Data Fig. 9**: stopping criteria sensitivity. checkpoint × patience grid, hippocampus dataset, UMAP velocity flow *robust*.
- **Extended Data Fig. 10**: runtime. (a) total time 286 min (1 job) → 36 min (30 jobs), saturation 15 jobs / 40 min. (b) training speed (genes per minute) 증가. (c) cellDancer vs velocyto/scVelo/DeepVelo/VeloVAE 비교 (18,140 cells × 2,159 genes, 15 jobs) — cellDancer가 *다른 deep learning method와 comparable*. 정확한 분 단위 수치 4 baseline은 본문 미기재 — `검토필요: bar plot 직접 측정 필요.`

---

## Tables

### Supp Table 1 (본문에 정식 Table 없음 — 본문 Table은 부재)

- **이 Table이 필요한 이유**: simulation accuracy의 *유일한 정량 정리* — error rate를 5 method × 3 regime 행렬로 제시. Extended Data Fig. 1c-e box plot의 *summary statistic (mean)*.
- **이 Table이 뒷받침하는 주장**: cellDancer는 모든 multi-rate regime에서 baseline 4개를 outperform.

#### 표 구조

- Row (비교 축 1): regime (transcriptional boost / multi-forward branching / multi-backward branching). 3 row.
- Column (비교 축 2): method (cellDancer / scVelo / velocyto / DeepVelo / VeloVAE). 5 column.
- 셀 값의 의미: *mean error rate %* (cells with cosine similarity < 0.7 vs ground truth, n = 1,000 genes per regime).

#### 핵심 수치

- **Transcriptional boost**: cellDancer **13.25%** | scVelo 46.88% | velocyto 56.12% | DeepVelo 51.62% | VeloVAE 46.95%
  - baseline 대비: cellDancer가 next-best (scVelo 46.88%) 대비 **3.5×** 낮음.
  - 통계적 유의성: $P < 0.001$ one-sided Wilcoxon (Extended Data Fig. 1c, n = 1,000 genes per regime). CI / effect size 미제공.
- **Multi-forward branching**: cellDancer **2.63%** | scVelo 40.57% | velocyto 67.67% | DeepVelo 82.16% | VeloVAE 58.82%
  - baseline 대비: cellDancer가 next-best (scVelo 40.57%) 대비 **15×** 낮음 — *flagship number*.
  - 통계적 유의성: $P < 0.001$ (Extended Data Fig. 1d).
- **Multi-backward branching**: cellDancer **9.43%** | scVelo 31.13% | velocyto 15.30% | DeepVelo 44.99% | VeloVAE 62.66%
  - baseline 대비: velocyto (15.30%)와 cellDancer (9.43%)가 비슷. *cellDancer 우위 격차가 가장 작은 regime*.
  - 통계적 유의성: $P < 0.001$ (Extended Data Fig. 1e).

#### 본문에서 강조한 비교

- **비교 대상**: cellDancer vs 4 baseline method.
- **관찰된 차이**: forward branching에서 *15× 차이* (cellDancer 2.63% vs DeepVelo 82.16%).
- **이 차이가 의미하는 것**: gene-shared latent time을 강제하는 baseline은 *forward branching에서 가장 실패* — *서로 다른 time scale의 두 lineage*가 한 timeline에 압축되기 때문.

#### 해석 시 주의점

- **주의점**:
  - simulation regime 4종 (mono + 3 multi-rate)이 *저자 자신이 정의* — *third-party benchmark suite* 부재.
  - error rate 정의 (cosine similarity < 0.7 cutoff)가 *임의적* — *다른 cutoff*에서 결과 달라질 수 있음.
  - multi-backward branching에서 *velocyto (15.30%)가 cellDancer (9.43%)에 매우 근접* — cellDancer 우위가 *모든 regime에서 일정하지 않음*.
  - mean만 제시 — *variance / individual gene variability*는 box plot (Extended Data Fig. 1c-e)에 시각적으로만.
  - multiple testing correction *명시 없음* (3 regime × pairwise 5 method = 30 비교).

---

## Supplementary Information

### Supplementary Figures (Supp Fig. 1–3)

- **Supp Fig. 1**: pancreas의 3 추가 example gene (Actn4, Top2a, Gng12) training process 시각화. Figure 1c의 추가 example.
- **Supp Fig. 2**: hippocampus branching gene 10개 (Syt11, Klf7, Gnao1, Dctn3, Gpm6b, Psd3, Ntrk2, Slc1a3, Astn1, Cadm1) — cellDancer vs scVelo / velocyto / DeepVelo / VeloVAE 비교. *cellDancer 모두 정확* (저자 주장). 정량 score 미제공 — 시각적 평가.
- **Supp Fig. 3**: pancreas $(\alpha, \beta, \gamma)$ UMAP 개별 embedding ($\alpha$ alone, $\beta$ alone, $\gamma$ alone). Figure 4d의 보충 — *세 rate 모두 cell type 분리에 기여*.

### Supplementary Notes — Note 1: Model-based neural network derivation

- **목적**: DNN이 *RNA velocity inference에 수학적으로 적합*함을 *toy prototype neural network*로 증명.
- **핵심 derivation** (Supp Note 1, p5–7):
  - scVelo dynamical model의 Heaviside step function $\sigma(\beta u - \gamma s) \in \{0, 1\}$로 $\alpha$를 *induction/repression switch*. discretization:
$$du/dt = \sigma(\beta u - \gamma s) \cdot \alpha - \beta u, \quad ds/dt = \beta u - \gamma s$$
  - Heaviside는 미분 불가 → sigmoid $s(x) = 1/(1 + e^{-x})$로 근사 (DNN에서 흔히 사용).
  - prototype DNN: input $(u_i, s_i)$ → hidden layer with weights $\{w\}$ and biases $\{b\}$ → activation $\sigma$. weight가 $\beta$, $-\gamma$ analog, hidden layer output이 $\alpha$ analog.
  - loss $\mathcal{L}_i(u_i, s_i) = 1 - \mathrm{corr}(v_i^{\mathrm{pred}}, v_i^{\mathrm{truth}})$, ground truth $v_i^{\mathrm{truth}}$는 neighbor $i'$ 중 *cosine-best-fit*.
  - simulation: $\alpha = 5.2$, $\beta = 2.0$, $\gamma = 1.0$, initial guess $\alpha_0 = 1.0$, $\beta_0 = 1.0$, $\gamma_0 = 0.5$. Adam learning rate $0.001$. 1,500 epoch 내 수렴 (Note Figure 1C).
- **결론**: DNN architecture가 *RNA velocity ODE의 적절한 surrogate model* 임을 *수학적으로 증명*. *cellDancer는 이 prototype을 확장* — 2 hidden layer, 100 nodes each, sigmoid output regularization $\alpha, \beta, \gamma \in [0, 1]$.
- **해석**: 본 Note 1이 *DNN의 inductive bias가 ODE structure와 compatible*함을 보여줌 — 단순 "DNN이 universal approximator라 잘 fit" 이 아니라 *model-based*임을 강조.

### Supplementary Table 1

- 본 paper의 *유일한 정량 table*. 위 Tables section 참조.

### Reporting Summary (supp-2)

- Nature Portfolio Reporting Summary (3 page, image-only PDF). text extraction 불가 — `미제공: checkbox 형태의 statistical reporting summary 내용은 PDF 직접 확인 필요 (page 1–3 image).` 일반적으로 sample size justification, randomization, blinding, statistical test 등의 reporting 항목. `검토필요: 본 paper가 *machine learning model* 위주라 Reporting Summary의 "Animals" "Human subjects" 같은 wet-lab 항목은 대부분 N/A로 추정.`

---

## 분석 자체에 대한 메모

- **본 paper의 핵심 contribution 두 가지** (분석자 정리):
  1. *Latent time 추정 회피 + local neighbor cosine loss* — RNA velocity inference의 새로운 paradigm. *MoFlow `@hong2026moflow`의 직접 starting point*.
  2. *Cell-specific $(\alpha, \beta, \gamma)$의 cell identity marker로서의 secondary use* — pancreas Fig. 4, cell cycle Extended Data Fig. 6에서 입증.
- **본 paper가 *제기하지 않은* 질문 (분석자 follow-up)**:
  - `질문: cellDancer의 cosine similarity loss가 max over neighbor 인데, neighbor 후보 중 *outlier*가 있으면 loss가 *그 outlier만 따라가지 않는가*? scVelo의 likelihood maximization은 outlier에 더 robust할 가능성. 본문 outlier sensitivity 분석 부재.`
  - `질문: gene별 독립 DNN인데, gene 간 *공동 regulation* (TF cascade)을 모델 안에서 capture하지 않으면 *biological interpretability*가 dynamo downstream에 완전 의존. dynamo 없이 cellDancer만으로 regulatory inference 가능한가?`
  - `질문: chromatin/multi-omic 확장이 §Discussion에서 "could be likewise included"로만 언급. 본 paper 시점 (2023) 기준 MultiVelo (`@li2023multivelo`, 2023 같은 venue 같은 시기)와 비교 안 함 — *왜?* paper-info.yaml에 *peer review* 시점 비교 검토 필요.`
- **본 paper의 *재현 시 주의점***:
  - permutation ratio가 dataset 크기마다 다른 default (§Methods p12) — *automatic tuning 없음*. HSPC 같은 새 dataset 적용 시 hyperparameter search 필요.
  - sigmoid output $[0, 1]$ → absolute time scale 회복 불가. *시간 단위 lag* 분석에는 부적합 — pseudotime 기반만 가능.
  - gene별 독립 DNN으로 인한 runtime — 18k cells × 2,159 genes 15 jobs 40 min. 100k cells × 20k genes로 확장 시 *재추정 비용 필요*.
- **본 paper의 *외부 평가가 발견한 한계* (MoFlow `@hong2026moflow` 본문 참조)**:
  - chromatin-aware dataset (SHARE-seq mouse skin, multiome human cortex, HSPC multiome)에서 cellDancer CBDir가 *MultiVelo / MoFlow 대비 낮음*: HSPC $-0.056$ vs MultiVelo $0.063$, MoFlow $0.191$; SHARE-seq $0.026$ vs MoFlow $0.144$; cortex $-0.015$ vs MoFlow $0.362$ (Supp Table 1 of MoFlow). *RNA-only 본질적 한계*가 *후속 paper의 quantitative benchmark*에서 명확.
- **Week2 validation_report로 surfacing할 항목**:
  - `검토필요: cellDancer가 본 paper에서 *velocity directional accuracy의 정량 metric (CBDir 등)*을 제시하지 않음. 시각적 평가만으로 erythroid/hippocampus/pancreas 결과 검증한 것은 *validation gap*.`
  - `검토필요: simulation regime 4종이 저자 자체 정의 — third-party benchmark 부재.`
  - `미제공: ablation table 없음. cosine loss vs L2, DNN 깊이, neighbor 개수의 영향 부재.`
  - `미제공: cell cycle confound 전체 dataset 통제 부재 — pancreas Fig. 4e의 cycling subpopulation 식별만.`
  - `미제공: cross-batch / multi-sample 처리 부재 — single-sample 분석만.`
