# Lens — Academic — Hong 2026 MoFlow

> Citation: `@hong2026moflow`. 본 노트는 `hong-2026-moflow_core.md` 작성 후 *학계 시선*만 따로 정리. 산업·규제·BD 관점은 `hong-2026-moflow_lens-industry.md`. 본 paper는 `@li2023multivelo`(MultiVelo) post-extension 두 흐름 중 하나이고, 직접 sibling은 `@li2025multivelovae`(MultiVeloVAE) — cross-reference 빈번.

---

## Limitations

### 저자가 명시한 한계

- **Long-range enhancer-promoter interaction 직접 modeling 부재** (Discussion p12): "It does not explicitly model long-range enhancer-promoter interactions, nor does it account for transcriptional memory or motif-level regulation." → 단일 gene-level $c$ aggregation (promoter + linked enhancer) 의존, enhancer별 distinct kinetics 미반영.
- **Gene-wise inference의 pathway-level coordination 미포착** (Discussion p12): "Additionally, inference remains gene-wise, potentially limiting the detection of coordinated pathway-level programs." → gene network / co-regulation 정보 미사용.
- **Embedding 의존성 caveat** (HSPC §Results p11): "Similar to other velocity-based methods, the vector visualization depends on embedding velocity vectors into a fixed low-dimensional space (e.g., UMAP). This reliance can introduce distortions originating from the embedding rather than the underlying dynamics, and thus, the inferred velocity fields should be interpreted with caution."
- **HSPC reconstruction의 *not always fully consistent*** (HSPC §Results p11): "MoFlow recovered both continuity and divergence of trajectories, although its reconstructions were not always fully consistent across all branches." → HSPC bifurcation 일부 분기 부정확 저자 자체 인정.
- **Min-max normalization의 chromatin variance obscuring** (Fig. 7 caveat, p10): "both c and s were min-max normalized to the [0, 1] range for modeling compatibility, which may obscure low-level chromatin accessibility variance."
- **10x Multiome nuclear RNA capture 한계** (Fig. 7 caveat, p10): "as the 10x multiome platform captures nuclear RNA rather than total RNA, apparent degradation may reflect nuclear export." → cluster 0–3의 *rapid RNA turnover* 해석에 *nuclear export ≠ degradation* 모호함.
- **In vitro RNA half-life 외부 reference 사용** (Fig. 7 caveat, p11): "nuclear localization and kinetic measurements derived from in vitro cell lines may not fully reflect the in vivo dynamics of developing brain tissue." → Ietswaart 2024 NIH3T3 데이터로 *in vivo developing brain* 해석.

### 분석자가 판단한 한계

- **부족한 점 1 — 단일 metric (CBDir)에만 정량 의존**:
  - **왜 중요한가**: Supp Table 1의 CBDir이 *유일한 정량 benchmark*. `@li2025multivelovae`의 GCBDir (k-step + random-walk null subtraction), true time correlation, Mann–Whitney U, MSE/MAE 같은 *다축 metric*이 적용되지 않음. CBDir은 *cluster boundary 1-hop neighbor*만 평가 → *long-range trajectory accuracy*는 측정 안 됨.
  - **어떤 증거가 부족한가**: ① k-step CBDir (k=2..10) curve, ② cell type 간 ground-truth time이 있는 dataset (예: MEF 0–28 day reprogramming, Biddy 2018)에서 latent time vs true time correlation, ③ posterior sampled trajectory의 *uncertainty / variance*, ④ random-walk null model subtraction (GCBDir).

- **부족한 점 2 — Ablation 완전 부재**:
  - **왜 중요한가**: MoFlow의 *core design choice* — warm-up length (default 20 epoch), 2-stage 학습, Mahalanobis vs Euclidean neighbor, hard vs soft $k$ selection, neighbor count (default 40), DNN architecture (3-layer 64-48-32), learning rate (0.001), weight decay (0.04), max epoch (200) — *모두 default*에 sensitivity 분석 부재. *각 design choice의 marginal contribution*을 모른 채로는 MoFlow의 *어떤 component가 성능 향상의 원인*인지 attribution 불가.
  - **어떤 증거가 부족한가**: ① warm-up = 0 vs 20 vs 50, ② single-stage vs 2-stage, ③ Mahalanobis vs Euclidean neighbor, ④ neighbor count 20 vs 40 vs 80, ⑤ hard min vs soft mean (Eq. 24 vs 25) 비교, ⑥ DNN depth 2 vs 3 vs 4 layer.

- **부족한 점 3 — 신규 dataset 부재**:
  - **왜 중요한가**: 4개 dataset 모두 *이전 publication에서 재사용*. `@li2025multivelovae`는 EB (4,240 cells × 3,138 genes), HSPC$\times 2$ (17,667 cells × 892 genes), HSPC+macrophage (9,908 cells × 929 genes) 신규 produce. MoFlow는 *method 자체*만 contribution — *MoFlow가 신규 biology를 발견했음을 보여줄 신규 dataset experiment 부재*. 검증된 method라기보다 *이전 data의 reanalysis*에 가까움.
  - **어떤 증거가 부족한가**: ① 신규 dataset에서 MoFlow 발견한 *novel biology* (e.g., cluster 10 polycomb/speckle sequestration)의 *wet-lab validation* (e.g., FISH로 nuclear localization 확인, conditional export experiment), ② multi-donor / multi-batch dataset에서 MoFlow inference robustness, ③ disease vs healthy 같은 *applied scenario*에서 MoFlow가 *baseline 대비 신규 발견*.

- **부족한 점 4 — Cell-cycle confound 처리 명시 부재**:
  - **왜 중요한가**: HSPC, mouse skin, mouse brain 모두 *cycling-heavy* dataset. cell-cycle gene이 *trajectory inference에 dominant signal*로 작용 가능. `@li2023multivelo`는 cell-cycle effect를 RNA expression에서 regress out (Extended Data Fig. 2b)했고, `@li2025multivelovae`도 동일 한계 계승. MoFlow는 본문 / Methods에서 *cell-cycle 처리 언급 부재* — reference dataset (Li 2023의 preprocessed)를 그대로 사용해서 *간접 상속*.
  - **어떤 증거가 부족한가**: ① cell-cycle phase (G1/S/G2M)별 separate fit, ② cell-cycle gene 제외 후 fit 결과 비교, ③ MoFlow가 *cell cycle 영향을 받지 않는 transcription rate*를 정량할 수 있는지 확인.

- **부족한 점 5 — Multi-sample / multi-batch 통합 미지원**:
  - **왜 중요한가**: `@li2025multivelovae`의 cVAE multi-sample inference (Fig. 4) 같은 기능 부재. 두 donor / 두 batch를 함께 분석하려면 *별도 학습 후 post hoc 비교*만 가능. *batch effect 제거 + biological variation 보존*이 MoFlow framework 안에서 불가능.
  - **어떤 증거가 부족한가**: ① 두 HSPC sample (예: Li 2023 dataset의 day 0 + day 7) 통합 시 MoFlow의 robustness, ② cross-batch consistency metric, ③ batch effect로 인한 false discovery 비율.

- **부족한 점 6 — Hypothesis test / differential dynamics 부재**:
  - **왜 중요한가**: `@li2025multivelovae`의 Bayesian differential test (Bayes factor + Gaussian process + LRT) 같은 *cell type 간 driver gene을 statistical principled로 식별*하는 framework 부재. MoFlow는 모든 비교가 *2-sided t-test, Mann–Whitney U, Fisher's exact* — *post hoc descriptive statistics*만.
  - **어떤 증거가 부족한가**: ① cell type 간 differential velocity gene의 *FDR control*, ② multiple comparison correction (Fig. 7e의 128 KS test 같은 *수십~수백 test* 보정), ③ posterior uncertainty 기반 confidence interval.

- **부족한 점 7 — Negative chromatin–RNA lag 메커니즘 해석의 confounding**:
  - **왜 중요한가**: Fig. 7의 cluster 0–3 "rapid RNA turnover" vs cluster 10 "nuclear sequestration + conditional export" 가설이 모두 *external reference* (Ietswaart 2024 NIH3T3, Khyzha 2025 polycomb/speckle)에 의존. *MoFlow inference 결과와 외부 reference의 상관관계*만 보임 — *causal*은 입증 못함. MALAT1, XIST는 *half-life estimation에서 excluded*인데 cluster 10 결론에 포함 — *circular reasoning* 가능성.
  - **어떤 증거가 부족한가**: ① MoFlow 결과 cluster 10 gene을 *MALAT1/XIST 제외 후* polycomb/speckle Fisher's exact 재실행, ② developing brain 자체에서 RNA half-life 측정 (e.g., metabolic labeling SLAM-seq), ③ MoFlow가 *cluster 10 새 gene*을 발견했는지 (외부 reference에 *없는* gene) 정량.

- **부족한 점 8 — 129 reversal gene의 functional annotation 부재**:
  - **왜 중요한가**: Supp Fig. 2c, d의 "129 gene이 75% 이상 bin에서 lag sign reversal" 결과가 MultiVelo gene-specific latent time *over-correction*의 정량 핵심 evidence. 그러나 *129 gene이 어떤 functional class*인지 본문 부재. OPC marker + cell cycle만 알려진 gene인지, 신규 gene인지 식별 불가.
  - **어떤 증거가 부족한가**: ① 129 reversal gene list 공개 (Supplementary Data로), ② DAVID / GSEA enrichment, ③ 정상 gene과 비교한 expression level / variance 차이.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장 1**: "MultiVelo gene-specific latent time이 over-correct"라는 주장 (Fig. 3g vs 3f, p6):
  - **현재 논문에서 제시한 근거**: PDGFRA, MAP3K1의 c-s lag이 MultiVelo gene-specific time에서는 *positive* (c→s 순서), global time + MoFlow에서는 *negative*. 129 gene이 75% bin에서 reversal.
  - **더 필요해 보이는 근거**: ① *external ground-truth time* (예: time-stamped scRNA + ATAC time course)에서 어느 쪽 lag이 *진짜* 맞는지 검증, ② over-correction이라면 *MultiVelo의 EM이 local optimum에 빠지는 경우*인지 *cost function의 systematic bias*인지 구분, ③ MoFlow와 MultiVelo의 lag sign이 일치하는 gene과 reverse하는 gene의 functional 차이.

- **연결이 약한 주장 2**: "MoFlow가 capture-time-based external Allen Brain Atlas projection으로 OPC 정합 입증" (Fig. 3h, p6):
  - **현재 논문에서 제시한 근거**: MoFlow decoupling-sOff 영역에 OPC 63% embedded vs 다른 영역 20%.
  - **더 필요해 보이는 근거**: ① 다른 cell type (Astrocyte, Excitatory/Inhibitory Neuron)의 embedding 일치도 정량, ② Allen Brain Atlas의 *cell type annotation 자체*가 *해석 다양*하므로 ENCODE 또는 다른 external dataset으로 확인, ③ MoFlow 외 다른 method (MultiVelo, MultiVeloVAE)도 같은 projection 정확도를 보이는지.

- **연결이 약한 주장 3**: "DNA damage response gene이 RG의 transient checkpoint" (Fig. 6g, Supp Fig. 4f-h, p10):
  - **현재 논문에서 제시한 근거**: DAC$\alpha$ GSEA에서 DNA repair, DNA metabolic process 등 양수 NES. RG에서 α가 elevated.
  - **더 필요해 보이는 근거**: ① RG에서 *실제 DNA damage marker* (e.g., γH2AX foci)가 elevated인지 wet-lab 검증, ② 다른 dataset (다른 mouse / human brain)에서 같은 pattern 재현, ③ MultiVelo도 같은 dataset에서 RG의 DNA damage response gene α를 더 정확히 잡을 수 있도록 *별도 cell type-conditioned fit* (현재 MultiVelo는 global single rate).

- **연결이 약한 주장 4**: "cluster 10 = nuclear-sequestered polycomb/speckle RNA의 conditional export" (Fig. 7g, p10–11):
  - **현재 논문에서 제시한 근거**: Fisher's exact (cluster 10 vs others) polycomb p < 0.005, speckle p < 0.05. MALAT1, XIST 포함.
  - **더 필요해 보이는 근거**: ① MALAT1, XIST 제외 후 *coding gene만으로* 같은 enrichment 재현, ② Khyzha 2025 (ref. 44) reference gene set 외 *다른 nuclear compartment gene set* (예: Cajal body)과의 specificity 비교, ③ MoFlow inference 자체와 무관하게 cluster 10에 모이는 gene이 *cell type marker*가 아닌지 (e.g., specific neuronal subtype) 확인.

### 정리되지 않은 질문

- **질문 1**: MoFlow의 *hard $k$ selection* (Eq. 25, warm-up 후)이 cell이 *borderline case* (예: chromatin이 정말 열리는지 닫히는지 ambiguous)일 때 *training stability*에 어떤 영향? soft selection (e.g., warm-up 평균 유지)이 더 안정적이지 않은가?

- **질문 2**: 본 paper의 2-stage 학습 (RNA → joint)이 *RNA 학습 stage에서 chromatin head $\Phi_{\theta_c}$의 weight*가 어떻게 처리되는지 본문 명시 부재. *완전 frozen*인가 *random init 유지*인가? 후자라면 stage 2 시작 시 chromatin head가 informative하지 않은 prediction으로 RNA head의 cosine loss를 *drift*시킬 가능성.

- **질문 3**: Mahalanobis distance in $(c, u, s)$ joint space — covariance matrix가 *전체 cell pool*에서 한 번 계산되는지 *local neighborhood*에서 계산되는지 본문 명시 부재. *전자라면* heterogeneous cell type에서 *cell-type-specific neighbor 정의*가 distort 가능.

- **질문 4**: m1, m2 score의 90th percentile threshold (default)가 *Mouse Skin*에서만 *higher threshold 필요* (Supp Fig. 6). *Mouse Skin의 Model 2 gene이 적기 때문*이라 해석하나, threshold가 *dataset-specific*이어야 한다는 점 자체가 *score의 일반성*을 약화. *dataset-independent threshold*는 불가능한가?

- **질문 5**: MoFlow는 *latent time을 추정하지 않는다*고 강조. 그러나 downstream의 pseudotime (scVelo `tl.velocity_pseudotime`)이 *velocity vector에서 inferred*. *MultiVelo의 latent time*과 *MoFlow의 post hoc pseudotime*이 본질적으로 어떻게 다른가? 단지 *학습 과정에서 사용되는가의 차이*인가, *수학적 형식의 차이*인가?

- **질문 6**: MoFlow가 *cell type annotation 없이* 학습. 그러나 DAC score는 *cell type 정의에 의존*. DAC-based grouping (HCHA / LCHA)이 *cell type annotation 품질에 얼마나 민감*한가? Leiden cluster를 *finer / coarser*로 바꾸면 LCHA / HCHA grouping이 어떻게 변하는가?

- **질문 7**: 본 paper의 Fig. 7의 cluster 10 발견 (RNA가 chromatin 전에 증가, polycomb/speckle gene 포함)이 *MoFlow가 detect 가능한 모든 cluster 중 outlier*. *Other clusters (0–9, 11)에는 비슷한 unique pattern이 없는가*? cluster 10 만의 특수성이 *MoFlow가 1개 unique mechanism만 발견*하는 한계인가 *데이터의 실제 limit*인가?

- **질문 8**: `@li2025multivelovae`의 continuous decoupling factor $\delta$, coupling factor $\kappa$가 MoFlow의 m1/m2 + RNA-on/off + 4 RNA velocity state (both-on/both-off/decoupling-sOff/decoupling-sOn)와 어떻게 *대응*되는가? 두 framework의 *continuous score 정의*가 *동일 dataset에서 일치/불일치*하는지 정량 비교 부재.

### MoFlow vs MultiVeloVAE 비교

본 sub-section은 lens-academic이지만 cross-paper 비교가 *분석 핵심*이므로 별도 분리.

- **공통 출발점**: 둘 다 MultiVelo (`@li2023multivelo`)의 *discrete 4 state + shared kinetic regime + gene-specific latent time*의 세 한계를 해소하려는 시도. 둘 다 *cell-specific kinetic*을 통한 *cell-level resolution* 회복을 목표.

- **MoFlow vs MultiVeloVAE 핵심 차이**:

  | 측면 | MoFlow (`@hong2026moflow`) | MultiVeloVAE (`@li2025multivelovae`) |
  |---|---|---|
  | Latent time | *추정하지 않음* (cellDancer 상속) | *모든 gene 공유 single $t$* (cVAE posterior) |
  | Model family | Discriminative DNN + cosine loss | Generative cVAE + ELBO + ODE analytical |
  | Cell-specific 변수 | $(\alpha_c, \alpha, \beta, \gamma)$ via DNN, $k \in \{0, 1\}$ hard | $(k_c, \rho) \in [0, 1]$ continuous via decoder |
  | Multi-sample 통합 | *미지원* — 별도 학습 후 post hoc | cVAE conditioning + batch-specific $\theta_b$ + cross-batch L2 |
  | Hypothesis test | *미지원* — post hoc t-test, Mann–Whitney | Bayesian differential test (Bayes factor + GP + LRT) |
  | RNA-only mode | *미지원* — chromatin 항상 필요 (cellDancer가 별도) | *지원* — $c=1$ pseudo-input + mixed mode 학습 |
  | Cross-modality imputation | *미지원* | *지원* — scRNA-only sample에 chromatin 추정 |
  | In silico perturbation | *미지원* | *지원* — $c=u=s=0$ zeroing 후 decode |
  | Uncertainty estimate | *deterministic point* | posterior + optional ODE parameter $q_\phi(\theta)$ |
  | Gene mixture | *없음* — 단일 ODE | BasisVAE 7 cluster |
  | Downstream metric | CBDir (1개) | GCBDir + true time correlation + MSE/MAE + scIB integration |
  | 신규 dataset | 없음 (4개 모두 재사용) | 3개 신규 (EB, HSPC$\times 2$, HSPC+macrophage) |
  | Code license | `검토필요:` (paper 미명시) | BSD-3-Clause |
  | Code repo | github.com/AriHong/MoFlow | github.com/welch-lab/MultiVeloVAE |
  | Citation key | `@hong2026moflow` | `@li2025multivelovae` |

- **동일 dataset (mouse brain, mouse skin, human HSPC) 비교**:
  - 본 두 paper 모두 *MultiVelo와의 비교*에 같은 dataset 사용 (Trevino 2021 human brain, Ma 2020 mouse skin, Li 2023 HSPC, 10x mouse brain). 그러나 *어느 method가 더 우위인지* 직접 head-to-head 비교 **없음** — 두 paper 모두 *MultiVelo와 1:1 비교*만 보고.
  - `해석: 우리가 직접 head-to-head를 해야 함 — 같은 input data로 두 method 돌려 CBDir + GCBDir + runtime + 메모리 비교.`
  - `질문: MoFlow의 CBDir (0.362 human brain, 0.144 mouse skin, 0.535 mouse brain, 0.191 HSPC)이 MultiVeloVAE의 동일 dataset 결과보다 높은가 낮은가? MultiVeloVAE는 CBDir이 아닌 GCBDir만 보고 — 직접 비교 위해 GCBDir 또는 CBDir 한 metric으로 통일 필요.`

- **Method philosophy 비교**:
  - **MoFlow** — *Local relay velocity + chromatin-aware*. *순간 direction*만 신경 쓰고 *time scale은 회피*. cellDancer를 chromatin 차원으로 extend. "trajectory를 어떻게 그릴까"보다 "각 cell의 *just-next-step* direction"에 집중.
  - **MultiVeloVAE** — *Global generative model + multi-sample inference*. *shared time + cell state latent + batch conditioning + differential test* 전체를 *single probabilistic framework* 안에 통합. 본질적으로 *Bayesian inference framework*.
  - `해석: MoFlow는 *engineering-oriented* — 작은 module 여러 개로 robust한 cell-level inference. MultiVeloVAE는 *statistics-oriented* — single coherent posterior 안에서 모든 것을 처리. 우리가 *어느 쪽이 우리 use case에 fit한지*가 선택 기준.`

- **우리 HSPC multiome pipeline에 어떤 method?**:
  - **MoFlow 강점**: ① latent time-free 덕분에 *cell-cycle / lineage가 섞인 system*에서 trajectory artifact 적음, ② DAC + DTW + cluster-based time lag analysis로 *epigenomic lag biology 그 자체*를 mechanistic 해석 (cluster 10 nuclear sequestration 같은), ③ *우리 epigenomic-lag 연구 주제와 직접 정합* — Fig. 7의 c-s lag 분석은 우리 연구 outcome 그 자체.
  - **MoFlow 약점**: multi-sample 통합 안 됨, differential test 안 됨, RNA-only mode 안 됨, 신규 dataset 검증 안 됨.
  - **MultiVeloVAE 강점**: ① multi-sample 통합 (우리가 다 donor 확보 시 즉시 활용), ② Bayesian differential test (cell type 간 driver gene), ③ in silico TF perturbation (drug target nomination), ④ scRNA-only sample integration (public dataset 활용), ⑤ 4-axis benchmark 다양.
  - **MultiVeloVAE 약점**: continuous $(k_c, \rho)$가 *biologically interpretable rate constant*와 직접 mapping 어려움, latent time 가정이 *cell cycle 같은 multi-time-scale system*에서 깨질 가능성.
  - **권장 (분석자 판단)**: **두 method 동시 운영 + cross-validation**.
    - **MoFlow를 primary tool**로 *epigenomic lag 정량* (DTW c-s lag, m1/m2 score, DAC group) → 우리 연구 outcome.
    - **MultiVeloVAE를 secondary tool**로 ① multi-sample 통합 (HSPC$\times$여러 donor), ② Bayesian differential test (HSPC 분기별 driver gene), ③ in silico TF perturbation (drug target).
    - 두 method의 *agree하는 영역*은 *high confidence*, *disagree하는 영역*은 *재검토 대상* — single-method-driven false discovery 방지.

## Final Takeaways

- **이 논문의 가장 큰 의미**:
  - *Latent time-free* + *chromatin-aware* + *cell-specific kinetic* 조합을 *deterministic discriminative DNN*으로 구현한 첫 paper. relay velocity (cellDancer)에 chromatin을 자연스럽게 결합.
  - CBDir 4-dataset 평균에서 MultiVelo, cellDancer, scVelo를 모두 outperform — *backflow가 가장 적은 framework*.
  - *Negative chromatin–RNA lag의 mechanistic interpretation*을 *RNA half-life + nuclear localization*으로 연결 — 본 paper의 *biological discovery* contribution. Khyzha 2025 polycomb/speckle finding을 *MoFlow가 single-cell 단위로 confirm + extend*.
  - DAC-based 4-quadrant gene grouping (HCHA / HCLA / LCHA / LCLA)으로 *chromatin-α decoupling*을 정량 — Hephl1, Padi3, Myo10 같은 *MURK / transcriptional boost* gene을 cell-type-specific으로 해체.
  - GitHub + Zenodo + PyTorch Lightning open-source 코드 + Demo notebook.

- **다음 논문으로 이어질 아이디어**:
  - **(아이디어 1) MoFlow + MultiVeloVAE의 head-to-head benchmark paper**: 같은 input data (HSPC, mouse brain, human brain, mouse skin)로 두 method 돌려 ① CBDir / GCBDir, ② runtime, ③ memory, ④ cell-type-specific score (MoFlow의 4 RNA state, MultiVeloVAE의 $\delta, \kappa$) confusion matrix, ⑤ ground-truth time이 있는 dataset에서 latent time correlation. *MultiVelo post-extension의 standard benchmark*로 자리잡을 가능성.
  - **(아이디어 2) MoFlow + MultiVeloVAE의 hybrid framework**: MoFlow의 *cell-specific kinetic*과 MultiVeloVAE의 *cVAE multi-sample*을 결합. cell-specific *deterministic* parameter + cVAE *batch conditioning* + Bayesian differential test. *deterministic + variational* hybrid VAE.
  - **(아이디어 3) MoFlow on multi-time-point single-cell ATAC + scRNA**: 시간 별 captured single-cell multiome 시간 stamp가 있다면, MoFlow의 *post hoc pseudotime*과 *real time*을 align. priming → activation의 *real time scale* 검증. epigenomic lag을 *분/시간 단위*로 정량.
  - **(아이디어 4) 우리 HSPC에서 MoFlow 적용 + GATA1, SPI1 KO consequence 비교**: MoFlow는 *in silico perturbation 미지원* — 그러나 MoFlow inference 결과 cell type별 (α, c) profile에서 GATA1, SPI1 target gene의 *chromatin-α 결합 vs decoupling*을 예측. wet-lab CRISPR knockdown으로 검증.
  - **(아이디어 5) MoFlow의 chromatin state $k$를 soft posterior로 일반화**: Eq. 25의 hard min을 *temperature-scaled softmax* 또는 *Gumbel-softmax*로 대체 → differentiable. cell-level chromatin state의 *uncertainty* 정량.
  - **(아이디어 6) Cluster 10 polycomb/speckle 결과의 wet-lab validation**: MoFlow가 발견한 cluster 10 gene의 *nuclear localization*을 spatial transcriptomics (e.g., subcellular MERFISH) 또는 RNA-FISH로 확인. *conditional export* hypothesis 입증.
  - **(아이디어 7) MoFlow + spatial multi-omics**: spatial chromatin (e.g., spatial CUT&Tag) + spatial RNA-seq + MoFlow의 local neighbor relay velocity 결합. *spatial neighbor*를 *time neighbor* 대신 사용 → tissue spatial coordinate에서의 c-s lag 분석.

- **설명을 더 매끄럽게 만들 방법**:
  - Supp Table 1의 CBDir에 *95% bootstrap CI*를 추가 — 단일 값보다 *variance + significance*가 명확.
  - 129 reversal gene list를 *Supplementary Data*로 공개. functional annotation + cell-type expression pattern.
  - cluster 10 결과를 MALAT1, XIST 제외한 후의 *coding-only enrichment*로 강화.
  - MoFlow의 *chromatin head $\Phi_{\theta_c}$ 학습 stability* trace를 supplementary에 추가 — 2-stage 학습의 정당성 입증.
  - 본 paper에 *MultiVeloVAE 비교 절*을 추가 (현재 부재) — peer review revision 가능.

- **우선순위가 높은 후속 실험 / 분석**:
  - **(1) MoFlow + MultiVeloVAE head-to-head**: 우리 HSPC 10x Multiome data + Li 2023 HSPC dataset에서 양 method 돌려 ① CBDir 비교, ② 동일 cell의 MoFlow 4 RNA state vs MultiVeloVAE $(\delta, \kappa)$ confusion matrix, ③ runtime / memory. *다음 sprint (2주)에 즉시 가능*.
  - **(2) MoFlow의 ablation 자체 수행**: warm-up = 0 vs 20, single-stage vs 2-stage, neighbor count 20 vs 40 vs 80. 우리 데이터에서 *어느 design choice가 결정적*인지 직접 측정.
  - **(3) cluster 10 polycomb/speckle 발견의 우리 데이터 재현 확인**: HSPC 10x Multiome에서 MoFlow 학습 후 cluster 10 type gene 발견 여부 확인. 재현되면 *기전 일반성* 증거, 안 되면 *brain-specific* 가설.
  - **(4) MoFlow의 cell-cycle gene effect 정량**: HSPC dataset에서 cell-cycle gene 제외 vs 포함 fit 비교. *cell-cycle confound가 trajectory에 미치는 영향* 정량.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- **§Introduction (p2)**: "Recent extensions seek to overcome some of these limitations. cellDancer introduces a local relay velocity model without latent time, but is limited to transcriptomic data. MultiVelo incorporates chromatin accessibility in an ODE-based model but assumes fixed gene classifications and shared kinetic regimes."
  - 사용 시나리오: 우리 introduction에서 *post-MultiVelo extension 흐름* 설명 시 *MoFlow가 cellDancer + chromatin awareness 결합* 위치 정립.

- **§Introduction (p2)**: "Despite these advances, three key challenges remain unresolved: (i) modeling dynamics with branching trajectories without fixed gene labels, (ii) capturing asynchronous transcriptional kinetics, and (iii) integrating epigenomic context without relying on rigid structural assumptions."
  - 사용 시나리오: epigenomic-lag 분야의 *open problem statement*로. 우리 연구의 motivation에 직접 인용.

- **§Discussion (p11)**: "MoFlow outperforms existing models, such as scVelo, MultiVelo and cellDancer in reconstructing developmental trajectories across diverse tissues, including the brain, skin and hematopoietic cells."
  - 사용 시나리오: post-MultiVelo method 선택 시 *MoFlow를 candidate*로 정당화. CBDir 수치 (Supp Table 1)와 함께 인용.

- **§Discussion (p12)**: "Our findings offer a mechanistic explanation for previously observed time lags between transcription factor motif accessibility and downstream gene activation."
  - 사용 시나리오: *epigenomic lag 자체의 mechanistic basis*가 *RNA nuclear export + degradation kinetics 차이*임을 정립하는 reference.

- **§Methods (p13–14, Eq. 17–25)**: chromatin-aware relay velocity 수식 전체.
  - 사용 시나리오: 우리 method section에서 *MoFlow를 baseline으로 사용*할 때 수식 인용. 또는 *MoFlow를 extend / modify*한 우리 method 정의 시.

### 수치 인용 후보

- **Supp Table 1 CBDir**: MoFlow Human Brain **0.362**, Mouse Skin **0.144**, Mouse Brain **0.535**, Human HSPC **0.191**. 4-dataset 평균 *0.308*. baseline MultiVelo 평균 *0.136*, cellDancer *0.022*, scVelo *0.094*. *2.3× MultiVelo, 14× cellDancer, 3.3× scVelo*. → 우리 introduction에서 *MoFlow의 정량 우위* 강조 시.
- **129 reversal gene** (Supp Fig. 2c, d): *MultiVelo gene-specific latent time over-correction*의 정량 — 우리 method section에서 *latent time-based method의 systematic bias* 논의 시 인용.
- **63% OPC embedded** (Fig. 3h external Allen Brain Atlas projection): MoFlow decoupling-sOff 영역과 OPC identity의 *external validation* 인용.
- **GO BP enrichment** (Supp Data 1–3 xlsx): cell division p = 1.63e−15 (human brain), cell division p = 5.20e−42 (mouse brain), chromosome segregation p = 1.9e−3 (LCHA mouse skin) — 우리 *MoFlow 적용 결과의 reference*로.

### 활용 시나리오

- **시나리오 1 — 우리 epigenomic-lag 연구의 introduction**:
  - "MultiVelo (`@li2023multivelo`)의 ODE 가정의 한계를 극복하려는 두 흐름이 동시 등장 — VAE 기반 generative inference (`@li2025multivelovae`)와 latent time-free deep neural network (`@hong2026moflow`). 본 연구는 두 framework를 우리 HSPC dataset에서 head-to-head 비교한다."

- **시나리오 2 — 우리 method section의 baseline**:
  - "Baseline methods: scVelo (`@bergen2020scvelo`), cellDancer (`@li2024celldancer`), MultiVelo (`@li2023multivelo`), MultiVeloVAE (`@li2025multivelovae`), MoFlow (`@hong2026moflow`)."

- **시나리오 3 — 우리 결과 discussion**:
  - "MoFlow (`@hong2026moflow`)가 *negative chromatin–RNA lag*의 mechanistic explanation을 *RNA half-life 차이*로 제공했지만, 본 연구에서는 *single-cell 단위로 직접 측정한 RNA half-life*를 기반으로 그 가설을 확장한다."

- **시나리오 4 — 학회 발표 (예: Nature Comm Korea, Asia Single Cell Symposium)**:
  - "Post-MultiVelo extension에서 *latent time*을 둘 것인가 말 것인가가 갈림길이다. `@li2025multivelovae`는 shared latent time + cVAE로 *Bayesian framework*를 만들었고, `@hong2026moflow`는 latent time 자체를 회피하고 *local relay velocity*에 집중했다."

### 인용 시 주의

- **CBDir 단일 metric 의존**: paper 본문 또는 우리 인용 시 *유일 metric* 한계 명시 필요. `해석: 우리 인용 시 "CBDir 기준" 명시.`
- **신규 dataset 부재**: MoFlow의 모든 결과가 *이전 publication 재사용*. 새 발견이라 인용 시 *original dataset paper도 함께 인용*해야 attribution 정확.
- **License**: `검토필요:` — GitHub repo의 license 확인 필요. paper 자체는 CC BY-NC-ND 4.0 (commercial 사용 + adaptation 제약).
- **Sangseon Lee (Inha)의 직접 관여 — cellDancer 저자는 다른 인물**: `검토필요: cellDancer 저자 (Shengyu Li 등)와 본 paper의 Sangseon Lee가 다른 인물임 — 한국 이름 표기 동일성 주의. cellDancer를 *predecessor*로만 명시.`

### 분석자의 인용 가치 판단

- **우선순위 1 (높은 가치)**: MoFlow의 *negative c-s lag mechanism* 해석 (Fig. 7) — 우리 *epigenomic lag 연구 주제와 직접 정합*. 인용 시 *이 발견을 build on*하는 우리 contribution 정립.
- **우선순위 2 (높은 가치)**: MoFlow의 *MultiVelo gene-specific latent time over-correction* 정량 (Fig. 3g, 129 reversal gene) — *latent time-based method의 systematic bias*에 대한 우리 비판 정당화.
- **우선순위 3 (중간 가치)**: MoFlow의 *CBDir 우위* — 우리가 *post-MultiVelo extension*을 baseline으로 선택할 때 정당화.
- **우선순위 4 (중간 가치)**: MoFlow의 *DAC-based HCHA / LCHA grouping* — 우리 데이터에 적용해 새 group 발견 시 *MoFlow를 framework*로.
- **우선순위 5 (낮은 가치)**: MoFlow의 *Hephl1, Padi3, Myo10 등 예시 gene* — 우리 데이터와 다른 tissue (mouse skin)라 직접 인용 가치는 낮음.

---
