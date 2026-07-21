# Lens — Academic — Cui 2024 DeepVelo

> `@cui2024deepvelo` — `Genome Biology` 25:27 (2024). DOI: 10.1186/s13059-023-03148-9. 분석 근거: `cui-2024-deepvelo_core.md`, sources/cui-2024-deepvelo.pdf, sources/cui-2024-deepvelo-supp-1-figures.pdf (Supp Notes S1–S5, Figs S1–S29), sources/cui-2024-deepvelo-supp-5-direction-consistency.xlsx, sources/cui-2024-deepvelo-supp-9-hp-sweep.xlsx, sources/cui-2024-deepvelo-supp-10-direction-consistency-v2.xlsx.

## Limitations

### 저자가 명시한 한계

- **Rare cell type에서의 continuity 한계** (§Discussion p17): continuity assumption은 *충분한 cell density*가 필요. rare cell type은 $t+1$ neighbor가 sparse → DeepVelo가 *robust 하다고 hyperparameter 결과로 부분 방어*하지만 *rare type 자체가 적은 경우*는 해결책 없음.
- **Confidence quantification 부재** (§Discussion p17): "there is a lack of probabilistic tools to test the kinetics estimated by either previous methods or DeepVelo." DeepVelo의 *continuity score*와 *correlation score*는 *post hoc heuristic*일 뿐 *well-calibrated posterior*가 아님. uncertainty estimation을 future work로 위임.
- **Gene-gene interaction 모델링 제한** (§Discussion p17): DeepVelo의 GCN은 *cell graph*만 사용. *gene 간 regulatory interaction*은 추가 정보 없음. *transformer-based architecture*로 gene-gene interaction을 explicit하게 모델링하는 것을 *future work*로 제안.
- **Multi-omics 확장 미구현** (§Discussion p17): DeepVelo는 RNA-only. *chromatin (Chromatin Velocity ref. 5, MultiVelo ref. 4) / protein (protaccel ref. 6) / metabolic labeling (Dynamo ref. 8)* 확장이 *future work*로 남음 — *현재 형태로는 epigenome-transcriptome lag 분석 불가*.

### 분석자가 판단한 한계

- **Cell-specific rate가 *진짜 biochemical rate*인지 미검증**:
  - 부족한 점: DeepVelo는 *cell-specific* $(\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g})$를 학습하지만, 학습된 rate가 *실제 transcription/splicing/degradation rate*와 일치하는지 *biochemical assay (metabolic labeling, smFISH, intron-exon ratio quantification)*로 검증 없음.
  - 왜 중요한가: 만일 학습된 rate가 *consistency loss를 minimize하는 fit parameter*일 뿐이라면, *cell heterogeneity를 표현하는 latent feature*로는 유용하지만 *biological rate*로는 인용 불가. 본문은 rate UMAP이 cell-type cluster와 일치한다 (Fig. 3a)는 *post hoc consistency*만 보임.
  - 어떤 증거가 부족한가: *smFISH* 또는 *intron labeling* 같은 *orthogonal kinetic rate measurement*와 cross-validation.
- **GCN vs FFNet ablation의 *trade-off* 해소 부족** (`cui-2024-deepvelo_core.md` §Robustness, Supp Table S9):
  - 부족한 점: GCN은 direction score 우위, FFNet은 cell-type-wise consistency 우위. 두 metric이 *trade-off*인데 *왜 direction이 더 중요*한지 *quantitative 논의* 부재.
  - 왜 중요한가: 사용자가 *과제에 따라* 다른 architecture를 선호할 수 있는데, 본문은 *single best choice (GCN)*만 결론. *FFNet이 적합한 시나리오*를 명시하면 *method 적용 가이드*로 더 의미.
  - 어떤 증거가 부족한가: dataset-specific decision rule. e.g., "small cell count + single lineage = FFNet, multi-lineage + large cell count = GCN".
- **Simulation의 *unfair advantage* 의심**:
  - 부족한 점: time-dependent simulation (Fig. 3d-h)은 *scVelo 자체 simulator*로 생성. *DeepVelo의 continuity loss design이 simulation generator의 inverse*가 될 위험. cellDancer (`@li2023celldancer`)도 같은 simulation을 사용했지만 *별도 simulator design space*에서 testing은 없음.
  - 왜 중요한가: 시뮬레이션 우위가 *generator-specific*인지 *general*인지 불명확.
  - 어떤 증거가 부족한가: *independent ground-truth simulator* (예: spatial scRNA-seq with continuous time labeling, lineage tracing) 또는 *biological gold standard* (perturbation + bulk validation).
- **PA tumor discovery의 *counterfactual* 부재**:
  - 부족한 점: PA의 immunogenicity heterogeneity 발견 (Fig. 7)이 *DeepVelo로만 가능*했다는 *counterfactual* 검증 없음. scVelo로 같은 PA cell을 분석했을 때 *branching이 안 나오는지* 직접 비교 없음.
  - 왜 중요한가: *biological discovery의 method-attribution*이 핵심 contribution인데, *direct ablation* (PA × scVelo) 없이는 *DeepVelo's necessity*가 *implied*에 그친다.
  - 어떤 증거가 부족한가: PA × scVelo 분석 + branching 실패 시각화 또는 정량 (e.g., Louvain modularity 차이).
- **Sample diversity 편향**:
  - 부족한 점: 모든 발달 dataset이 *mouse*. PA cohort는 *human 3명 모두 male, age 7–15*. *human adult tissue / female / racial diversity / disease state generalization* 직접 검증 없음.
  - 왜 중요한가: cell-specific kinetics method를 *human disease application*으로 확장하려면 *generalization 증거*가 필요. mouse-specific kinetic pattern이 human에서 그대로 성립한다는 보장 없음.
  - 어떤 증거가 부족한가: 동일 organ의 human adult dataset 추가 benchmark (e.g., human bone marrow, human hippocampus organoid, human liver).
- **Multi-batch / batch confound 처리 미명확**:
  - 부족한 점: dentate gyrus는 P12+P35 *multi-batch*임에도 *batch correction layer 없음*. velocity가 *batch effect와 confounded*되지 않는지 명시적 검증 없음.
  - 왜 중요한가: large-scale atlas (multi-lab, multi-donor) 적용 시 *batch effect가 cell-specific rate에 leak*할 위험. 본문은 "multi-time-point에 적용 가능"만 주장.
  - 어떤 증거가 부족한가: batch confound 진단 (e.g., velocity vs batch covariate Pearson correlation, kBET).
- **Full-batch training scalability**:
  - 부족한 점: batch size = $N$ cells (full-batch). 본문 benchmark의 최대 cell 수 = 30k (organogenesis downsample). *real-world atlas (10M cells, e.g., HCA)에 적용 가능한지* 미검증.
  - 왜 중요한가: minibatch training 시 GCN의 *neighbor batch sampling 전략*에 따라 결과가 달라질 수 있음.
  - 어떤 증거가 부족한가: 100k–1M cell 규모 benchmark + minibatch 전략 비교.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장 — "DeepVelo가 cell-type을 학습한다"**:
  - 현재 논문에서 제시한 근거: Fig. 3a (cell-specific kinetic rate UMAP이 cell-type cluster와 일치). Supp Fig. S5 (epoch별 cluster 진화).
  - 더 필요해 보이는 근거: cluster *형성 mechanism*. 단순히 *neighbor information leakage*인지 *kinetic dynamics에 대한 biological insight*인지 분리 안 됨. cell-type label을 *입력에 주지 않았어도*, GCN의 *neighborhood smoothing*이 cell-type-별 cluster를 *직접적으로 강제*할 수 있음. 진정한 *kinetic-driven cluster*임을 보이려면 *kinetic rate UMAP*과 *expression UMAP*의 *clustering metric 비교* 필요.
- **연결이 약한 주장 — "continuity assumption is more general"**:
  - 현재 논문에서 제시한 근거: Note S2의 superset 증명 (steady-state + dynamical scVelo → continuity).
  - 더 필요해 보이는 근거: *증명이 학습 가능성을 보장하지 않음*. continuity가 *theoretical superset*이라도 *finite sample에서 적절히 학습*된다는 *empirical evidence*는 별도. 학습 결과가 *steady-state region에서도 정확한가*에 대한 ablation (예: gene을 *steady-state로 강제한 simulation*에서의 정확도) 필요.
- **연결이 약한 주장 — PA immunogenicity의 임상 implication**:
  - 현재 논문에서 제시한 근거: 3 sample에서 immune pathway enrichment + MAPK 활성 immunogenic-only.
  - 더 필요해 보이는 근거: *outcome*과의 연결. 본문은 "implications for prognosis and treatment"를 *주장*만 — *outcome 없는 cohort*라 *실제 prognostic value*는 시각 불가. *paired clinical follow-up*이 있는 cohort가 필요.

### 정리되지 않은 질문

- **질문 1**: cell-specific kinetic rate $(\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g})$가 *cell cycle phase*와 어떻게 confound되는가? cell cycle은 *transcription rate 자체를 modulate*하는 강력한 covariate. 본문은 cell cycle covariate 통제 없음.
- **질문 2**: "novel driver gene" Neurod6의 *experimental validation*은 어디서? 본문은 *literature association* (Tutukova 2021)만. *perturb-seq* 또는 *CRISPRi knockdown* 후 GABAergic 분화 변화 검증.
- **질문 3**: Pearson term scaling $\eta_s = 18.0$이라는 *unusually large weight*는 어떻게 결정? hyperparameter sweep ($U(1, 100)$)에서 *18.0이 최적*이라는 근거가 본문에 직접 없음. *sensitivity*는 sweep에서 *robust*로 결론.
- **질문 4**: DeepVelo의 *runtime 비교*가 GPU 시간만 — *학습 epoch 별 plateau 시점*은 명시 없음. 100 epoch이 *충분 vs over-training* 판단 기준이 무엇인가?
- **질문 5**: cellDancer (`@li2023celldancer`)와 *경쟁 method*임에도, 본문 비교는 *direction score 1개*만 (Supp Fig. S1). consistency / pathway enrichment / driver gene 정량 비교가 *왜 없는가*? — `해석:` 같은 시기 published라 fair benchmark의 *snapshot 차이* 우려 (DeepVelo가 cellDancer preprint를 비교 baseline으로 보아 *non-final code*에 대한 결과일 가능성).

## Final Takeaways

- **이 논문의 가장 큰 의미**:
  - *Cell-specific kinetic rate*를 *GCN + continuity loss*로 학습하는 *최초의 self-supervised framework*. cellDancer와 *동시기 경쟁 paper*지만 *direction score 우위*로 차별화.
  - *Continuity assumption*의 *theoretical superset 증명* (Note S2) — *epistemic*하게 *기존 method 가정의 unified abstraction*을 제안.
  - PA tumor의 *intra-tumor immunogenicity heterogeneity* 발견 — *DeepVelo의 biological utility를 narrative로 demonstrate* (causal attribution은 약함).
- **다음 논문으로 이어질 아이디어**:
  - **Multi-omic DeepVelo** — chromatin + RNA + protein → cell-specific rate. 저자 future work에 명시. *우리 epigenomic-lag 문제와 정확히 align* — 직접 후속 분석 가치.
  - **Probabilistic DeepVelo** — VAE 기반 cell-specific kinetic rate. MultiVeloVAE (`@li2025multivelovae`)가 이 방향에서 일부 구현. *posterior sampling*으로 confidence quantification.
  - **Transformer DeepVelo** — gene-gene interaction을 transformer self-attention으로 모델링 (저자 future work). *interpretable driver gene 후보 도출* 가능.
  - **cell cycle-controlled DeepVelo** — cell cycle phase를 covariate로 분리한 cell-specific rate. cell cycle gene을 *control set*으로 두고 *kinetics의 cell cycle invariance 검증*.
  - **Spatial DeepVelo** — spatial transcriptomics + RNA velocity. continuity assumption이 *spatial neighborhood*로 자연스럽게 확장 가능.
- **설명을 더 매끄럽게 만들 방법**:
  - PA discovery에 대해 *DeepVelo vs scVelo direct counterfactual* 추가 (PA × scVelo branching 시각).
  - cell-specific rate의 *biochemical validation* (smFISH, intron-exon ratio) — 가장 임팩트 큰 추가 실험.
  - GCN vs FFNet trade-off의 *task-dependent decision rule* 제시.
  - cell cycle confound 분석 — 본문 핵심 weakness.
- **우선순위가 높은 후속 실험 / 분석**:
  - (1) DeepVelo + chromatin modality (multi-ome) → *MoFlow / MultiVeloVAE와 head-to-head*.
  - (2) PA cohort 확대 ($n > 20$ patient) + outcome 데이터와 immunogenicity correlation.
  - (3) cell cycle controlled benchmark — cell cycle gene을 분리한 cell-specific rate가 *여전히 cell-type-specific cluster*를 형성하는지.

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Background p2 (steady-state + cell-agnostic 가정 한계 비판):
  > "The original RNA velocity approach utilized the assumption that the observed transcriptional phases in scRNA-seq last long enough to reach both an apex of induction and a quiescent steady-state equilibrium. … These assumptions are often violated in complex biological systems."
  - 사용 시나리오: 본인 논문 / 제안서 introduction에서 *RNA velocity 한계 → multi-omic / cell-specific 필요*로 transition할 때.
  - BibTeX key: `@cui2024deepvelo`
- §Background p2 (cell-specific kinetics 필요성):
  > "The kinetic rates are intrinsically cell-specific since there is a high degree of variability in transcriptional dynamics between cells [14]. Furthermore, these intrinsic cell-specific transcriptional dynamics are likely to be similar among similar cell-types [15], necessitating cell-type-specific parameters."
  - 사용 시나리오: cell-specific kinetics를 motivation으로 잡을 때.
  - BibTeX key: `@cui2024deepvelo`
- §Discussion p17 (confidence quantification 미해결 한계):
  > "There is a lack of probabilistic tools to test the kinetics estimated by either previous methods or DeepVelo. We anticipate future work in the estimation of RNA velocity will address this gap."
  - 사용 시나리오: 본인 제안서에서 *probabilistic / Bayesian velocity의 motivation*으로 인용.
  - BibTeX key: `@cui2024deepvelo`
- §Discussion p17 (multi-omics 확장 future work — 우리 영역과 정확히 align):
  > "Recent work shows promising research directions by extending the velocity of cellular dynamics from RNA to proteins [6], epigenomics [5], and multi-omics velocities [4]. DeepVelo could be naturally updated and well fitted into these settings by enriching input and output space with additional -omics information."
  - 사용 시나리오: epigenomic-lag 또는 multi-omic velocity 연구의 *prior work + open gap*으로 인용.
  - BibTeX key: `@cui2024deepvelo`
- §"DeepVelo's cell-specific kinetic rates enable..." p6 (multifaceted kinetics 빈도):
  > "[V]arying kinetic rates in the differentiation of intestinal stem cells. These varying kinetics are often misinterpreted in existing velocity methods" (referring to Battich et al. ref. 19, Bergen ref. 20).
  - 사용 시나리오: multifaceted kinetics가 *artifact가 아니라 biological reality*임을 주장할 때.
  - BibTeX key: `@cui2024deepvelo`

### 인용 가능 수치

- *Mouse gastrulation direction score*: DeepVelo $0.769$ vs scVelo dynamical $-0.475$ — *부호 반전*. (Supp Table sheet "Direction Score").
  - 사용 시나리오: cell-agnostic rate가 가장 극단적으로 실패하는 setting의 정량 evidence.
  - BibTeX key: `@cui2024deepvelo`
- *multi-faceted gene 비율*: 평균 *$0.58$* (Supp Fig. S3) — cell-specific kinetics 필요성의 *경험적 통계*.
  - 사용 시나리오: cell-specific method의 필요성 motivation. "scRNA-seq dataset의 58% gene이 multi-faceted kinetics를 보임 (`@cui2024deepvelo` Supp Fig S3)."
  - BibTeX key: `@cui2024deepvelo`
- *Dentate gyrus consistency*: DeepVelo $0.948$ vs scVelo dynamical $0.801$, Mann-Whitney U $p < 10^{-300}$, $n = 2{,}930$.
  - 사용 시나리오: 본인 benchmark에서 DeepVelo baseline 인용 시.
  - BibTeX key: `@cui2024deepvelo`
- *PA immunogenic vs depleted pathway 수*: Sample 1 immunogenic 155 vs depleted 6; Sample 2 immunogenic 129 vs depleted 38; Sample 3 immunogenic 263 vs depleted 43 — *intra-tumor heterogeneity 강도*.
  - 사용 시나리오: scRNA-seq tumor heterogeneity 사례 인용.
  - BibTeX key: `@cui2024deepvelo`
- *Runtime*: GPU 사용 시 hindbrain 13,501 cells 36초 — RNA velocity의 *scalability evidence*.
  - 사용 시나리오: scRNA-seq pipeline의 *throughput*을 논할 때.
  - BibTeX key: `@cui2024deepvelo`

### 인용 가능 Figure/Table

- **Figure 1**: DeepVelo pipeline schematic (GCN encoder + FC decoder + extrapolation training).
  - 사용 시나리오: 본인 review에서 *deep learning velocity의 architecture 진화*를 보일 때, velocyto → scVelo → DeepVelo → MultiVeloVAE / MoFlow의 *architecture timeline*으로 인용.
  - BibTeX key: `@cui2024deepvelo`
- **Figure 3a (cell-specific kinetic rate UMAP)**: kinetic rate 자체가 cell-type identity를 *latent feature로 표현*한다는 visual claim.
  - 사용 시나리오: cell-specific rate의 biological interpretability를 주장할 때.
  - BibTeX key: `@cui2024deepvelo`
- **Figure 6f (direction score per cell)**: DeepVelo vs scVelo의 *cell-wise direction score density* 시각화 — 본인 method paper에서 *direction score 차이의 cell-level distribution*을 시각화하는 referent로 인용.
  - BibTeX key: `@cui2024deepvelo`
- **Supp Table S8 (5,000-run hyperparameter sweep)**: *robustness benchmark의 좋은 예시*. 본인 method paper에서 hyperparameter robustness 검증 protocol의 reference로.
  - BibTeX key: `@cui2024deepvelo`

## DeepVelo's place in the deep-learning RNA velocity lineage

DeepVelo의 academic 가치를 평가하려면 *deep-learning RNA velocity의 계열 위에서의 위치*가 명확해야 한다. 본 sub-section은 우리가 follow-up 분석 (lens-industry, methodology-brief, validation report)에서 일관되게 인용할 수 있도록 *DeepVelo의 self-positioning과 후속 method가 보완한 내용*을 정리한다.

### 계열의 전개 — velocyto → scVelo → DeepVelo / cellDancer → VeloVAE / MultiVeloVAE / MoFlow

1. **velocyto** (La Manno 2018, ref. 1) — *steady-state regression*. 가정: per-gene linear ratio가 sequencing에 잡힘. 한계: multi-lineage에서 부적합.
2. **scVelo** (Bergen 2020, ref. 2) — *dynamical model + cyclic 4 state*. 가정: per-gene cyclic trajectory. 한계: cell-agnostic rate + cyclic 가정.
3. **DeepVelo** (Cui 2024, 본 paper) — *cross-gene GCN + continuity loss*. 가정: continuity (충분한 cell density). 한계: probabilistic 아님, RNA-only, gene interaction explicit하지 않음.
4. **cellDancer** (Li 2023, ref. 16, `@li2023celldancer`) — *per-gene DNN + cosine similarity loss*. 가정: cell-specific rate, gene-independent training. DeepVelo와 *동시기 경쟁 method*. DeepVelo 비교에서 direction 약함, cellDancer 자체 비교에서 simulation 우위.
5. **VeloVAE** (Gu 2022, ref. 20 — preprint at time of DeepVelo) — *VAE-based velocity*. 가정: posterior over kinetic rate. DeepVelo의 *probabilistic 한계 보완* 방향.
6. **MultiVelo** (Li 2023, ref. 4, `@li2023multivelo`) — *chromatin + RNA ODE coupling*. 가정: chromatin이 transcription rate에 영향. DeepVelo의 *RNA-only 한계 보완* 방향 (multi-omic axis).
7. **MultiVeloVAE** (Li 2025, `@li2025multivelovae`) — *MultiVelo + cell-specific rate + VAE + multi-sample integration*. DeepVelo와 MultiVelo의 *두 한계를 합쳐서 해결*: cell-specific rate + probabilistic + multi-omic + multi-sample.
8. **MoFlow** (Hong 2026, `@hong2026moflow`) — *deep ODE + cell-wise kinetic + chromatin opening/closing dual hypothesis*. DeepVelo의 cell-specific rate를 *chromatin opening/closing dual modeling*과 결합.

### MoFlow와 MultiVeloVAE가 DeepVelo 대비 *NEW*로 더한 것

**MoFlow (`@hong2026moflow`)가 더한 것**:
- **Chromatin opening / closing dual hypothesis**: DeepVelo는 RNA-only. MoFlow는 *chromatin opening 또는 closing 두 가설을 모두 fit하고 lower-loss 선택* — fixed gene classification 회피. `해석:` DeepVelo가 *chromatin term 자체 부재*인 반면 MoFlow는 *chromatin opening의 *binary* classification에서 한 단계 더 나가 *continuous selection*.
- **Cell-wise kinetic parameter $(\alpha_c, \alpha, \beta, \gamma)$ 학습** (출처: `hong-2026-moflow_core.md` §Methods): DeepVelo의 *cell + gene specific rate*에 *chromatin opening rate $\alpha_c$*를 추가. *Chromatin opening rate*는 DeepVelo가 다루지 않는 epigenome dimension.
- **CellDancer 계승 + chromatin axis** (출처: `hong-2026-moflow_core.md` Background): MoFlow는 *cellDancer의 cell-specific kinetic*을 직접 계승 + *MultiVelo의 chromatin coupling*을 합침. DeepVelo는 cellDancer와 *parallel path*였기 때문에 MoFlow의 lineage에서 *직접 reference로 적게 인용*되는 경향. `미제공:` MoFlow가 DeepVelo를 *직접 비교 baseline*으로 사용했는지는 본 분석 시점에서 `hong-2026-moflow_core.md`에 명시 없음.

**MultiVeloVAE (`@li2025multivelovae`)가 더한 것** (출처: `li-2025-multivelovae_core.md`):
- **VAE 기반 probabilistic velocity**: DeepVelo의 *deterministic discriminative* 구조와 달리 *cell state $z$ + cell time $t$ posterior 학습*. DeepVelo가 명시한 *probabilistic confidence quantification 부재*를 직접 보완.
- **BasisVAE multi-basis**: cell의 *4-state classification (priming / coupled-on / decoupled / coupled-off)*을 *continuous probabilistic basis로 일반화*. DeepVelo는 4-state 가정 자체가 없으므로 *비교 차원이 다름*. MultiVelo의 4-state 한계를 보완하는 형태.
- **Multi-omic chromatin axis**: MultiVeloVAE는 *chromatin $c$ + spliced $s$ + unspliced $u$ + batch covariate $b$* 입력. DeepVelo는 RNA-only.
- **Multi-sample integration (cVAE)**: 두 sample을 cell state 수준에서 alignment. DeepVelo는 *batch correction layer 없음*.
- **Cell-specific transcription rate $\rho$**: DeepVelo의 *cell-specific* $\alpha_{i,g}$와 *동등한 개념*, 단 *probabilistic decoder*에서 추정. *MultiVelo (Li 2023)의 single set of ODE parameter*는 cell-specific 아님 — *MultiVeloVAE는 DeepVelo의 cell-specific concept을 multi-omic으로 가져옴*.
- **RNA-only mode benchmark** (출처: `li-2025-multivelovae_core.md` Fig. 2f): MultiVeloVAE의 RNA-only mode조차 *DeepVelo를 GCBDir에서 outperform* — MultiVeloVAE $0.637$ vs DeepVelo $0.311$ (10 dataset median). 즉 *VAE + shared time + BasisVAE 구조의 RNA-only standalone gain*이 *DeepVelo의 GCN + continuity*보다 크다고 MultiVeloVAE 본문이 주장.

### DeepVelo로부터 borrowed 한 것

- **Cell-specific kinetic rate concept**: MoFlow / MultiVeloVAE 모두 *cell-specific* $(\alpha, \beta, \gamma)$를 채택 — DeepVelo가 *2024 시점에서 가장 명확하게 motivation을 정리*한 paper. 본 paper §Background는 *cell-specific kinetics의 textbook intro*로 후속 paper들이 인용 가능.
- **Direction score / consistency metric**: DeepVelo의 *cell-type-wise consistency*와 *direction score*는 후속 RNA velocity benchmark의 *de facto standard* 일부. MultiVeloVAE의 GCBDir도 *cross-boundary direction* concept의 후속 확장.
- **Neighborhood-aware learning**: DeepVelo의 GCN message passing 아이디어는 *cell의 noisy 단독 expression*보다 *neighborhood smoothing*이 *kinetic rate 학습에 유리*함을 보임. MoFlow의 *local neighbor 기반 cosine similarity* (cellDancer 계승) 또한 같은 원리.

### 결론 — DeepVelo의 *현재 위치*

DeepVelo는 *RNA velocity의 deep-learning lineage*에서 *cell-specific kinetic rate를 self-supervised로 학습한 첫 framework 중 하나*로 자리잡았다. 그러나 (1) RNA-only, (2) deterministic (probabilistic confidence 부재), (3) chromatin coupling 없음의 세 한계가 후속 method (MoFlow, MultiVeloVAE, VeloVAE 등)의 *공통 motivation*이 되었다. 본인 epigenomic-lag 연구에서 DeepVelo는 *direct method 후보가 아니라 method genealogy의 핵심 reference*로 인용한다 (Citation 후보 섹션 참조).
