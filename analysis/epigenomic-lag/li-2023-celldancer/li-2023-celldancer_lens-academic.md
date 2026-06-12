# Lens — Academic — Li 2023 cellDancer

> 본 lens는 `li-2023-celldancer_core.md`의 *객관적 분석*을 기반으로 *학계 시선 해석*을 작성한다. 산업·규제·임상 risk와 BD value는 `li-2023-celldancer_lens-industry.md` 참조.

## Limitations

### 저자가 명시한 한계

§Discussion (p9, last 3 paragraphs)에서 저자가 명시한 한계 4개:

1. **Absolute time scale 회복 불가** (§Discussion p9, 직접 인용): "due to the limitation that scRNA-seq captures only spliced and unspliced mRNA abundances, it is unfeasible to infer the absolute magnitude of the RNA velocity and the underlying $(\alpha, \beta, \gamma)$ values using only scRNA-seq data. Additional time information introduced by experimental techniques, such as metabolic labeling or different timepoint datasets, could be incorporated to obtain such absolute kinetic rates." → 모든 cellDancer 결과가 *relative / pseudotime 단위*. wall-clock 단위 lag 정량은 불가.
2. **Multi-omic 확장 미구현** (§Discussion p9): chromatin accessibility를 input matrix에 추가하면 transcription rate 추정을 *강화 가능*하다고 명시했지만 본 paper는 *RNA-only*. → 사실상 이 future direction을 *MultiVelo `@li2023multivelo`*와 *MoFlow `@hong2026moflow`*가 실현.
3. **DNN architecture 의존성** (§Discussion p9): fully-connected DNN이 복잡한 dependency에서는 LSTM (ref. 47) 또는 CNN (ref. 48)으로 *교체 가능*하다고 인정 — *현재 architecture가 모든 regime에 최적이 아님*.
4. **ODE 종속성** (§Discussion p9): cellDancer는 *first-order rate equation*에만 적용 가능. 일반적 $dT(t)/dt = f(T(t), R(t))$ form에 적용 가능하지만 *명시적 분리 가능* 조건 필요. → second-order moment (stochastic dynamics) 직접 처리 안 됨.

### 분석자가 판단한 한계

- **부족한 점 ①** — *velocity directional accuracy의 정량 metric 부재*.
  - 왜 중요한가: 본 paper의 *real-data 결과 (erythroid, hippocampus, pancreas, human neurogenesis)*가 모두 *UMAP/t-SNE flow의 시각적 평가*만으로 정확성을 주장. CBDir (cross-boundary direction correctness, Qiao 2021), Velocity coherence, In-cluster coherence 같은 *third-party metric*이 없음. *simulation에서만 정량 error rate (Supp Table 1)*.
  - 어떤 증거가 부족한가: external benchmark suite (예: scvelo benchmark, UniTVelo benchmark dataset)에서 측정한 *third-party 정량 score*.
  - 외부 확인: `@hong2026moflow` 본문은 동일 cellDancer를 *CBDir로 재평가* — HSPC dataset에서 cellDancer $-0.056$ vs MultiVelo $0.063$, MoFlow $0.191$; SHARE-seq cellDancer $0.026$ vs MoFlow $0.144$ (Supp Table 1 of MoFlow). 즉 *chromatin-aware dataset에서 cellDancer가 약함*. 본 paper에서는 이 영역을 *측정하지 않음* — 강한 영역 (multi-lineage RNA-only)만 평가.

- **부족한 점 ②** — *ablation 부재*.
  - 왜 중요한가: cellDancer의 핵심 design choice 4개 — (1) cosine similarity vs L2/MSE loss, (2) max over neighbor vs mean over neighbor, (3) DNN 깊이 (2 hidden layer), (4) neighbor 개수 — 어느 하나가 *결과에 결정적인지* 본문 ablation 없음. 따라서 *cellDancer 성능이 어디서 오는지* 분리 불가.
  - 어떤 증거가 부족한가: ablation table (component on/off × dataset × metric).
  - 분석자 추론: §Discussion에서 저자는 "automatically inferred from a neural network by optimizing a simple loss function based on local cosine similarity"라고 핵심을 *cosine + local neighbor*로 자기 인식 — *하지만 이 두 가지가 정말 critical인지 ablation 부재로 확인 불가*. MoFlow는 동일한 cosine loss를 *Mahalanobis 거리 기반 neighbor*로 변형하고 *chromatin opening/closing 양쪽 가설 lower-loss 선택*을 추가했는데, 이 변형이 *cellDancer 자체 분석 부재* 위에서 진행됨.

- **부족한 점 ③** — *gene 간 공동 regulation 모델 안 됨*.
  - 왜 중요한가: gene별 독립 DNN이므로 *TF cascade*, *gene-gene co-regulation*이 모델 내부에서 표현 안 됨. *dynamo*에 downstream 의존 (Figure 2g Gata2 perturbation, Figure 4g Arx-Pax4 Jacobian).
  - 어떤 증거가 부족한가: cellDancer 자체로 *regulatory network inference* 평가 — 본 paper는 모든 regulatory 결과를 dynamo에 위임.
  - 외부 맥락: 후속 method 중 *Bayesian framework* (VeloVI, PyroVelocity)는 *gene 간 shared latent variable*로 partial 해결. MultiVeloVAE (`@li2025multivelovae`)는 *shared latent time + cell-gene chromatin opening rate*로 해결.

- **부족한 점 ④** — *cell cycle confound 통제 부재*.
  - 왜 중요한가: pancreas dataset에서 ductal cell의 *cycling subpopulation*만 식별 (Fig. 4e). *전체 dataset의 cell cycle covariate (S/G2M score)*는 *통제하지 않음*. cell cycle gene이 *velocity 결과를 왜곡*할 가능성. project CLAUDE.md의 *"Confound 통제 필수"* 원칙 위배.
  - 어떤 증거가 부족한가: cell cycle phase별 sub-analysis 또는 *cell cycle score를 covariate로 regression out*한 결과.

- **부족한 점 ⑤** — *single-sample 분석만, batch effect 처리 부재*.
  - 왜 중요한가: 모든 dataset이 *single sample / single batch*. *cross-sample harmonization* (예: scVI, Harmony) 없이 동일 framework가 multi-sample data에 적용 가능한지 *증명 없음*.
  - 어떤 증거가 부족한가: 2+ batch dataset에서 cellDancer 결과 + batch effect quantification.
  - 외부 맥락: `@li2025multivelovae`가 이 한계를 *conditional VAE (cVAE)*로 해결 — 후속 method의 추가 contribution이 됨.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장 ①**: §Discussion p9에서 "cellDancer DNN is scalable" 주장 — 근거는 *gene별 독립 DNN의 multi-processing 가능성* (Extended Data Fig. 10).
  - 현재 논문에서 제시한 근거: 18,140 cells × 2,159 genes에서 1 → 30 jobs로 286 → 36 min (8× 가속). 15 jobs 이후 *saturation* (40 min, 53 genes per minute).
  - 더 필요해 보이는 근거: *cell number scaling* (예: 100k, 500k, 1M cells)에서 runtime 추세. *gene number scaling* (현재 최대 2,159 → 20k whole transcriptome). *GPU 가속* 효과 (현재 CPU 24-core Intel Xeon W만 보고).
  - 분석자 판단: 본 paper의 "scalable" 주장은 *gene-level 병렬화*에 한정 — *single-gene runtime 자체*는 cell 수에 *quadratic 가능* (DNN input layer 크기 $2n$, output $3n$). full atlas (1M cells × 20k genes) 적용 시 *재추정 필요*.

- **연결이 약한 주장 ②**: §Discussion p9에서 "kinetic rate가 cell identity indicator" 주장 — Figure 4 pancreas만 근거.
  - 현재 논문에서 제시한 근거: $(\alpha, \beta, \gamma)$ UMAP에서 alpha/beta/delta/epsilon 분리 (Fig. 4d) + cycling subpopulation 분리 (Fig. 4e).
  - 더 필요해 보이는 근거: *quantitative cell type classification accuracy* (예: knn classifier on kinetic rate vs gene expression의 ARI, NMI, silhouette). *다른 tissue/dataset*에서 같은 패턴 — pancreas 하나만 보여줌. cell cycle Extended Data Fig. 6도 sub-evidence지만 *cell line (RPE1)*이라 in vivo cell type identity와는 다른 맥락.

- **연결이 약한 주장 ③**: top 500 low-loss gene의 GO enrichment를 *biological meaningfulness* 증거로 사용 (Fig. 3d).
  - 현재 논문에서 제시한 근거: hippocampus top 500 gene이 neurogenesis, neuron differentiation 등 enriched.
  - 더 필요해 보이는 근거: *control comparison* — 같은 dataset에서 *임의 random 500 gene* 또는 *high-loss gene 500개*의 GO enrichment가 *non-significant* 인지 확인. 현재 결과는 *cellDancer가 hippocampus의 dominant biology를 catch*하는 것일 뿐 *cellDancer-specific signal*인지 불확실.
  - 분석자 판단: hippocampus dataset의 *어떤 gene이든 neurogenesis-related로 enriched*될 가능성 (top 2,159 highly variable gene 모두 neuron 관련) — *cellDancer 우위 증거*로서 약함.

### 정리되지 않은 질문

- **질문 1**: cellDancer의 cosine loss가 *max over neighbor* 인데, neighbor 후보 중 *cosine-best-fit 하나의 outlier*가 있으면 loss가 *그 outlier만 따라가지 않는가*? outlier sensitivity 분석 부재. 만약 neighbor graph에 *technical doublet* 또는 *contamination cell*이 섞여 있으면 cellDancer가 *artifact direction*을 따라갈 위험.
- **질문 2**: gene-shared pseudotime estimation (Eq. 10–13, §Methods Pseudotime estimation p12)이 *graph-based time adjustment algorithm* (p12 step 1–5)에 의존. *cycle이 존재하면 algorithm이 실패* (p12: "If a cycle exists, the time adjustment algorithm fails. ... we suggest reducing the n_path parameter")라고 명시. 이 cycle failure가 *얼마나 자주 발생*하는지, *어떤 dataset에서 typical*한지 본문 없음. cyclic process (cell cycle) 자체가 *cellDancer pseudotime의 본질적 한계*.
- **질문 3**: simulation에서 *transcriptional boost*는 *uniform distribution*에서 $\alpha$ pre-boost $U(1.6, 2.4)$ → post-boost $U(4, 6)$로 *불연속 jump*. real-data MURK gene이 *gradual transition*인지 *step-function jump*인지 — simulation 가정이 *real biology와 맞는가*? Barile 2021 (ref. 18)이 명확한 step인지 *원문 확인 필요*.
- **질문 4**: §Discussion p9의 "metabolic labeling으로 absolute time scale 회복" 후속 작업 — 본 paper 시점 (2023) 이후 actual 후속 paper가 나왔는가? cellDancer GitHub에 update 있는가? `검토필요:` *GitHub repo 직접 확인 필요*.
- **질문 5**: human embryonic neurogenesis (Extended Data Fig. 7) dataset이 *1,054 cells*로 *가장 작음*. cellDancer가 *< 500 cells/lineage* 환경에서 동작하는가? Extended Data Fig. 8c는 1,000 cells까지만 sparse simulation — *그 미만은 미제공*.

## cellDancer → MoFlow 진화 (sub-section)

본 paper는 `@hong2026moflow` (MoFlow)의 *direct methodological predecessor*. 본 sub-section은 (1) cellDancer가 한 것, (2) MoFlow가 *cellDancer로부터 해결한* 한계, (3) cellDancer가 *MoFlow보다 여전히 잘하는* 영역을 분리 정리한다. 본 sub-section은 `hong-2026-moflow_core.md`의 Background·Methods 분석을 cross-reference.

### cellDancer가 한 것 (core contribution)

- **Relay velocity paradigm** (§Methods p11, Eq. 6–9): velocity inference를 *generative likelihood maximization*에서 *local neighbor cosine similarity max*로 전환. *latent time을 명시적으로 추정하지 않음*.
- **Gene-별 독립 DNN**: $\Phi_{\theta_i}: (u, s) \to (\alpha, \beta, \gamma)$. parameter explosion 없이 cell-specific kinetic rate.
- **Discretized ODE 외삽** (Eq. 4–5): analytic solution 불필요 → 다른 ODE 확장 가능. *cellDancer의 architectural flexibility*가 이후 multi-omic 확장의 *enabler*.
- **Cell-specific $(\alpha, \beta, \gamma)$의 secondary use** (Fig. 4 pancreas, Extended Data Fig. 6 cell cycle): kinetic rate 자체가 *cell identity marker*.

### MoFlow가 *cellDancer로부터 해결한* 한계

1. **Chromatin / multi-omic 부재** (cellDancer §Discussion p9 본문 명시 — "chromatin accessibility measured by single-cell assay for transposase-accessible chromatin with sequencing (scATAC-seq) can be likewise included in cellDancer to reinforce the estimation of the transcription rates").
   - MoFlow의 해결책 (`@hong2026moflow` §Methods "Extension of relay velocity model to multi-omics" p13): chromatin accessibility $c$를 추가 input으로 받고, 별도 DNN head $\Phi_{\theta_c}: (c, u, s) \to (\alpha_c, k)$로 chromatin opening rate $\alpha_c$와 *chromatin state* $k \in \{0, 1\}$ 추정. ODE 확장: $dc/dt = \alpha_c (k - c)$, $du/dt = \alpha c - \beta u$, $ds/dt = \beta u - \gamma s$ (MoFlow Eq. 1–3). 이는 *cellDancer §Discussion에서 예고한 multi-omic 확장*의 *직접 실현*.
   - 외부 평가 (MoFlow Supp Table 1): chromatin-aware dataset에서 MoFlow CBDir이 cellDancer 대비 명확히 우위 — HSPC cellDancer $-0.056$ → MoFlow $0.191$; SHARE-seq cellDancer $0.026$ → MoFlow $0.144$; cortex cellDancer $-0.015$ → MoFlow $0.362$.

2. **Chromatin opening/closing 가설 처리 부재** (cellDancer는 chromatin 자체 없음).
   - MoFlow의 추가 contribution (MoFlow §Methods, Eq. 25): chromatin opening ($k=1$) vs closing ($k=0$) 양쪽 시나리오 각각 cosine loss를 계산하고 *lower-loss 자동 선택*. 이는 *MultiVelo의 fixed gene classification (4-state) 회피*인 동시에 *cellDancer의 RNA-only neighbor cosine을 chromatin domain으로 확장*. 즉 cellDancer의 *local cosine loss*를 *chromatin가설 ensemble*로 일반화.

3. **Velocity directional accuracy의 정량 metric 부재** (cellDancer 본문 한계).
   - MoFlow의 해결: *CBDir, Velocity coherence, In-cluster coherence* 등 *third-party benchmark*에 정량 측정. cellDancer를 *quantitative baseline*으로 평가 — 본 paper에서는 *시각적 평가*만 있었음.

4. **gene-specific lag 정량 부재** (cellDancer는 latent time 없으므로 lag 측정도 자체 없음).
   - MoFlow의 추가 contribution: *DTW-based $(c-s)$, $(u-s)$ lag 정량* (`@hong2026moflow` Fig. 7, Methods Eq. 미상 — pseudotime axis 위에서 fastDTW). 이는 *cellDancer가 다루지 않은 새로운 task* — *chromatin-RNA lag mechanism* 분석.

### cellDancer가 *MoFlow보다 여전히 잘하는* 영역

- **RNA-only dataset에 대한 적용성**: chromatin / ATAC 데이터가 없는 *대다수 scRNA-seq dataset*에서 MoFlow는 직접 적용 불가 (chromatin 필수 input). cellDancer는 *순수 scRNA-seq*에 적용 가능 — *광범위 적용성*에서 우위.
- **Multi-rate (transcriptional boost) regime의 정량 우위**: simulation에서 cellDancer boost error rate 13.25% vs scVelo 46.88% (3.5×). MoFlow 본문은 *transcriptional boost simulation* 자체를 *cellDancer와 동일 protocol*로 재평가하지 않음 — *cellDancer의 simulation 우위가 MoFlow에 의해 직접 도전받지 않음*. 분석자 추정: MoFlow의 우위는 *chromatin-aware dataset*에 집중, *pure RNA dynamics inference*에서는 cellDancer가 *여전히 강한 baseline*일 가능성.
- **Computational simplicity**: cellDancer는 *RNA modality 1개*. MoFlow는 *chromatin + RNA 2 modality + 2 DNN head + 2-stage 학습*. 단순한 task에서는 cellDancer가 *implementation overhead 적음*.
- **Cell identity로서의 kinetic rate use case** (Figure 4, Extended Data Fig. 6): MoFlow는 *velocity inference + lag mechanism*에 집중하고 *kinetic rate를 cell identity marker로 사용하는 secondary task*를 직접 다루지 않음. cellDancer의 이 use case는 *후속 method가 계승 안 함* — 독립적 가치.

### 분석자 종합

- cellDancer는 *MoFlow의 conceptual ancestor*로서 **두 가지 architectural contribution**을 남김:
  1. *latent time 없는 local cosine loss* (MoFlow가 chromatin domain으로 확장).
  2. *discretized ODE + gene별 DNN* (MoFlow가 multi-modality로 확장).
- MoFlow가 *해결한* cellDancer 한계 (chromatin 부재, 정량 metric 부재, lag 측정 부재)는 *모두 epigenomic-lag topic에 직결*. 따라서 우리 프로젝트 (chromatin-RNA lag → epigenetic drug response time)에는 *MoFlow가 primary tool*, cellDancer는 *baseline / 계보 설명용*.
- 단 cellDancer는 *RNA-only dataset 광범위 적용성* + *kinetic rate as identity marker* use case에서 *MoFlow가 못 채우는 niche*를 가짐. *완전 deprecate* 대상이 아닌 *complementary baseline*.

## Final Takeaways

- **이 논문의 가장 큰 의미**: *latent time 없는 local relay velocity*라는 새로운 paradigm을 RNA velocity 분야에 도입. 이후 MoFlow가 이를 *chromatin-aware multi-omic*으로 직접 확장 — 본 paper는 *MoFlow → 우리 프로젝트 (epigenomic-lag → epigenetic drug response time)*로 이어지는 *3-step 계보의 첫 단계*.
- **다음 논문으로 이어질 아이디어**:
  - *Multi-rate kinetic regime simulation benchmark suite*를 cellDancer 정의 4 regime을 넘어 *transcription bursting*, *post-transcriptional decay heterogeneity*, *chromatin-coupled boost* 등으로 확장. third-party benchmark로 *RNA velocity method 전체*를 재평가.
  - cellDancer의 *cosine loss + max over neighbor*에서 *outlier-robust mean* 또는 *top-k average*로 변형한 *robust relay velocity*. SHARE-seq 같은 *technical noise 많은 multiome*에 적합.
  - cellDancer의 *kinetic rate cell identity use*를 *clinical cohort* (예: tumor vs normal multi-sample)에 적용 — *cell type classification feature*로서 *gene expression-based*보다 *kinetic rate-based*가 *batch-invariant*인지 검증.
- **설명을 더 매끄럽게 만들 방법**:
  - real-data 모든 figure에 *CBDir 또는 Velocity coherence 정량 표* 추가.
  - ablation table (loss function, neighbor 개수, DNN 깊이) 추가.
  - cell cycle covariate를 *전체 dataset에 regression out한 후* 결과 재계산 — *cell cycle confound로 인한 inflation*인지 확인.
- **우선순위가 높은 후속 실험 / 분석**:
  - 우리 HSPC 10x Multiome dataset에 cellDancer 단독 적용 → MoFlow / MultiVelo / MultiVeloVAE와 *4-way 비교* (CBDir, IC coherence, lag estimate). cellDancer가 *RNA-only baseline*으로서 어떤 영역 우위인지 정량.
  - cellDancer의 *cosine loss를 weighted mean over neighbor*로 modify한 *cellDancer-robust* 변형 시도 — *outlier sensitivity 한계* 검증.

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- **§Introduction p1–2 (motivation)**: "The existing velocity models assume uniform kinetics of all cells in an scRNA-seq experiment, which may result in poor predictive performance when cell subpopulations have dissimilar RNA velocity kinetics. For example, a number of genes (for example, Hba-x) exhibit a boost in their transcription rates during mouse erythrocyte maturation, which have opposite predictions by scVelo."
  - 사용 시나리오: 본인 introduction에서 *기존 RNA velocity의 universal kinetics 한계*를 짚을 때. *real-data failure case (Hba-x)*로 구체적.
  - BibTeX key: `@li2023celldancer`

- **§Introduction p2 (relay velocity definition)**: "Here we propose a 'relay velocity model' that uses the relay of a series of local velocities to provide single-cell resolution inference of velocity kinetics. ... in the relay velocity model the cell-specific velocity of each cell is informed by its neighbor cells and then relays cell-specific velocities."
  - 사용 시나리오: 본인이 *relay velocity 계보*를 소개할 때 원조 정의 인용. MoFlow 인용 시 *원조 method를 명시*하는 표준 인용.
  - BibTeX key: `@li2023celldancer`

- **§Discussion p9 (multi-omic 확장 가능성)**: "chromatin accessibility measured by single-cell assay for transposase-accessible chromatin with sequencing (scATAC-seq) can be likewise included in cellDancer to reinforce the estimation of the transcription rates."
  - 사용 시나리오: *cellDancer 저자가 multi-omic 확장을 예고했으나 본 paper에서는 미실현 → MoFlow / MultiVelo가 실현*이라는 *방법론 계보 narrative*에 핵심.
  - BibTeX key: `@li2023celldancer`

- **§Discussion p9 (latent time 회피의 가치)**: "cellDancer overcomes the barriers for inferring RNA velocity with multiple kinetics, such as branching genes and transcriptional boost genes by local but not global velocity estimation."
  - 사용 시나리오: 본인이 *local vs global velocity estimation* 비교 framework 제시할 때.
  - BibTeX key: `@li2023celldancer`

- **§Methods Pseudotime estimation p12 (cycle failure 인정)**: "If a cycle exists, the time adjustment algorithm fails."
  - 사용 시나리오: 본인이 *pseudotime inference algorithm의 fundamental limitation* — *cyclic biological process (cell cycle, circadian)*에서 모든 pseudotime method의 본질적 한계 — 를 논의할 때.
  - BibTeX key: `@li2023celldancer`

### 인용 가능 수치

- **Multi-forward branching error rate**: cellDancer 2.63% vs DeepVelo 82.16% (Supp Table 1, Extended Data Fig. 1d, n = 1,000 genes, $P < 0.001$).
  - 사용 시나리오: 본인 paper의 *multi-lineage RNA velocity benchmark* baseline 인용. cellDancer의 flagship number.
  - BibTeX key: `@li2023celldancer`

- **Runtime**: 18,140 cells × 2,159 genes 36 min (30 jobs), 53 genes per minute (Extended Data Fig. 10, p8).
  - 사용 시나리오: 본인이 *scalable velocity inference*의 runtime baseline 인용.
  - BibTeX key: `@li2023celldancer`

- **Dropout robustness**: Pearson $R^2 > 0.96$ ($\alpha/\beta$), $> 0.84$ ($\alpha/\gamma$) at 70% dropout (Extended Data Fig. 8b).
  - 사용 시나리오: 본인이 *high-dropout scRNA-seq data에서 method robustness* 평가할 때 reference.
  - BibTeX key: `@li2023celldancer`

### 인용 가능 Figure/Table

- **Figure 1 (workflow schematic)** (§Results p2, BioRender, Acknowledgements p13).
  - 무엇을 보여주는지: *local relay velocity*의 *DNN + cosine loss* workflow를 한 schematic으로 정리.
  - 사용 시나리오: 본인 review 또는 method paper에서 *relay velocity family*를 소개할 때 *원조 schematic* 재인용 (CC BY 4.0 license로 redistribution 가능).
  - BibTeX key: `@li2023celldancer`

- **Supp Table 1 (simulation error rate matrix)**.
  - 무엇을 보여주는지: 3 multi-rate regime × 5 method 의 mean error rate.
  - 사용 시나리오: 본인 paper의 *RNA velocity method 비교 review table*의 base. *cellDancer 우위 영역*과 *baseline 한계*를 한 번에 보여줌.
  - BibTeX key: `@li2023celldancer`

- **Figure 2g (in silico Gata2 perturbation, dynamo integration)**.
  - 무엇을 보여주는지: cellDancer가 *downstream perturbation framework (dynamo)*와 통합되어 *fate diversion* 시뮬레이션 가능.
  - 사용 시나리오: 본인이 *velocity-based in silico perturbation* 분야의 *원조 application*을 인용할 때.
  - BibTeX key: `@li2023celldancer`
