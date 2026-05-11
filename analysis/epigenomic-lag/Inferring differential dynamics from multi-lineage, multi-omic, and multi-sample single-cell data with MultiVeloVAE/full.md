# Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE

- 저자: Chen Li, Yichen Gu, Maria C. Virgilio, Kun H. Lee, Kathleen L. Collins, Joshua D. Welch
- 연도: 2025
- Venue: Nature Communications
- DOI: https://doi.org/10.1038/s41467-025-66287-6
- 분야: single-cell multi-omics, RNA velocity, variational inference, multi-sample integration, differential dynamics
- 입력 PDF: `papers/MultiVeloVAE.pdf`

### Background

#### 배경 스토리
- 문제의 출발점: cell differentiation은 gene expression과 chromatin accessibility가 시간에 따라 함께 변하는 과정이지만, single-cell sequencing은 cell을 파괴하므로 동일 cell을 longitudinal하게 추적할 수 없다. 따라서 snapshot cell들을 dynamic trajectory로 조립하는 computational method가 필요하다.
- 선행 접근 A: pseudotime inference는 cell들을 differentiation stage 순서로 배열해 trajectory를 추정했다.
- A의 한계: pseudotime은 시작점 지정이 필요하고, gene expression change의 방향과 rate를 mechanistic하게 직접 추정하지 않는다.
- 선행 접근 B: RNA velocity는 unspliced RNA와 spliced RNA를 이용해 transcription/splicing/degradation ODE를 맞추고 cell의 future state를 예측했다. scVelo는 steady-state assumption을 완화하고 latent time을 함께 추정했다.
- B의 한계: 초기 RNA velocity model은 각 gene을 separate time scale에서 모델링하고, gene expression을 discrete on/off state로 단순화하며, single lineage 또는 single cell type 가정을 강하게 가진다.
- 선행 접근 C: UniTVelo, DeepVelo, cellDancer, VeloVI, PyroVelocity는 shared time scale, cell-specific rate, Bayesian count modeling 등 일부 문제를 해결했다.
- C의 한계: UniTVelo는 multi-cell-type modeling과 biochemical interpretability가 제한적이고, DeepVelo/cellDancer는 post hoc cell time inference 때문에 inferred time과 velocity가 불일치할 수 있다. 또한 기존 방법들은 multi-sample velocity inference, partial modality integration, differential velocity testing을 체계적으로 지원하지 못했다.
- 선행 접근 D: MultiVelo는 chromatin accessibility를 RNA velocity ODE에 통합해 priming과 decoupling을 설명했다.
- D의 한계: MultiVelo는 population 전체에 하나의 parameter set을 가정하고, primed/coupled/decoupled state를 discrete하게 배정한다. multi-lineage differentiation에서 cell-type-specific rate 변화와 continuous state transition을 잡기 어렵다.
- 이 논문으로 이어지는 gap: biological discovery에는 여러 sample, 여러 lineage, partially overlapping modality, condition 간 dynamic difference를 함께 다룰 수 있는 velocity model이 필요했다.

#### 기본 개념
- RNA velocity: unspliced nascent RNA와 spliced mature RNA를 이용해 RNA abundance의 변화 방향과 속도를 추정하는 방법이다.
- multi-omic velocity: RNA뿐 아니라 chromatin accessibility `c`를 함께 모델링해, chromatin opening이 transcription을 선행하거나 transcription repression과 chromatin closing이 어긋나는 현상을 해석한다.
- variational autoencoder (VAE): encoder가 latent variable의 posterior distribution을 추정하고 decoder가 observed data를 재구성하는 probabilistic neural model이다. MultiVeloVAE는 이 구조로 cell time `t`, cell state `z`, kinetic parameters를 posterior inference한다.
- shared latent time: 모든 gene을 하나의 common time scale `t` 위에서 모델링하는 개념이다. gene별 time이 충돌하는 문제를 줄이고, 실제 capture time prior가 있으면 hours/days 같은 real temporal unit과 연결할 수 있다.
- coupling / decoupling factor: MultiVeloVAE는 chromatin opening rate `kc`와 transcription rate `rho`를 비교해 decoupling factor `delta = kc - rho`, coupling factor `kappa`를 정의한다. 이는 MultiVelo의 discrete state를 continuous, cell-specific score로 일반화한다.

#### 이 논문이 필요성
- 핵심 이유: 기존 velocity model은 multi-lineage, multi-sample, multi-omic data를 동시에 처리하고 condition/cell type/time별 differential dynamics를 통계적으로 검정하는 기능이 부족했다.
- 기존 방법으로 부족했던 지점: single-sample integration tool은 batch correction에는 유용하지만 velocity ODE와 modality 간 관계를 보존하지 못할 수 있고, velocity tool은 대체로 statistical hypothesis testing을 제공하지 않는다.
- 이 논문이 해결하려는 방향: MultiVeloVAE는 VAE와 chromatin-RNA ODE를 결합해 multi-sample, multi-omic, RNA-only, partially overlapping modality를 함께 다루고, Bayesian differential testing으로 velocity parameter와 modality dynamics 차이를 검정한다.

### Overview
- Figure 1 포함 여부: 포함됨 - Figure 1은 MultiVeloVAE의 multi-omic ODE assumption, encoder/decoder architecture, 기존 method 대비 기능 차이, multi-sample integration 원리를 모두 보여주는 전체 방법 개요다.

#### 핵심 개념
- 개념: cell differentiation dynamics를 `c`, `u`, `s`가 하나의 shared latent time과 latent cell state 위에서 움직이는 probabilistic ODE process로 본다.
- 이 개념이 필요한 이유: multi-lineage differentiation에서는 같은 gene도 lineage마다 chromatin opening rate와 transcription rate가 달라질 수 있고, multi-sample study에서는 biological variation과 technical variation을 분리하면서 velocity를 추정해야 한다.

#### Method 관점
- 논문이 이 개념을 바라본 방식: MultiVeloVAE는 encoder가 observed `(c, u, s)`와 optional batch covariate `b`에서 cell time `t`와 cell state `z` posterior를 추정하고, decoder가 `z`, `t`, `b`에서 cell/gene-specific chromatin state `kc`와 transcription rate `rho`를 예측한 뒤 ODE analytical solution으로 `(c, u, s)`를 재구성한다.
- 입력: multiome cell의 chromatin accessibility `c`, unspliced RNA `u`, spliced RNA `s`; RNA-only cell의 `u`, `s`; sample/batch categorical covariate.
- 처리 과정: auto-encoding variational Bayes로 ELBO를 최대화한다. batch label로 encoder/decoder를 condition해 latent `z`와 `t`에서 sample effect를 제거하고, reference batch로 decode해 counterfactual corrected `(c, u, s)`를 생성할 수 있다.
- 출력: latent time, latent cell state, cell-state uncertainty, chromatin/transcription rate parameter, velocity, coupling/decoupling factor, differential dynamics test 결과, missing modality generation, in silico perturbation prediction.

#### 이 관점으로 알 수 있는 것
- 알 수 있게 된 점 1: RNA-only data에서도 MultiVeloVAE는 기존 velocity method 대비 true time correlation, transition direction, held-out fit quality를 개선할 수 있다.
- 알 수 있게 된 점 2: multi-omic data에서는 MultiVelo의 discrete priming/decoupling state를 continuous, cell-type-specific factor로 확장해 lineage-specific regulation을 볼 수 있다.
- 알 수 있게 된 점 3: 여러 sample과 partially overlapping modality를 같은 model 안에서 처리해, batch correction과 velocity inference를 분리하지 않고 통합할 수 있다.
- 알 수 있게 된 점 4: posterior sampling과 Bayes factor를 이용해 cell type, lineage, time point 사이의 differential velocity와 parameter dynamics를 통계적으로 검정할 수 있다.

#### 기대 효과
- 성능 또는 분석상 기대 효과: 기존 RNA velocity, MultiVelo, single-cell integration tool보다 trajectory direction, biological conservation, multi-sample integration, differential dynamics interpretation을 개선한다.
- benchmark / baseline 관련 근거: RNA-only benchmark는 10개 real scRNA-seq dataset에서 scVelo, UniTVelo, DeepVelo, VeloVI, PyroVelocity, cellDancer와 비교했다. Multi-omic benchmark에서는 5개 dataset에서 MultiVelo 대비 k-step CBDir과 Mann-Whitney U statistics가 개선되었다고 보고했다.
- 적용 가능한 상황: developmental atlas, case-control study, multi-donor study, scRNA와 multiome이 섞인 partially overlapping modality dataset, lineage별 regulatory dynamics 비교.

### Figure / Table Analysis

#### Figure 1
- 이 Figure가 필요한 이유: MultiVeloVAE가 MultiVelo와 VeloVAE를 어떻게 결합하고, multi-sample/multi-omic/partial modality setting을 어떻게 처리하는지 한 번에 정의하기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MultiVeloVAE는 shared latent time, continuous cell-specific rate, multi-sample conditioning, differential testing이 가능한 probabilistic velocity framework다.

##### 패널별 설명
- a: multi-omic dynamics assumption과 neural network architecture를 보여준다. Encoder는 `(c, u, s)`와 optional batch covariate에서 cell state와 cell time을 추정하고, decoder는 `kc`와 `rho`를 예측한 뒤 ODE solution으로 data를 재구성한다.
- b: 기존 velocity method와 MultiVeloVAE의 기능 차이를 표로 요약한다. MultiVeloVAE는 multi-lineage, multi-sample, multi-omic, differential testing을 함께 지원한다는 점이 핵심이다.
- c: 여러 dataset을 통합할 때 sample-specific technical effect를 제거하고 corresponding cell state를 찾으며 joint dynamics를 inference하는 방식을 보여준다.

##### 본문에서 강조한 비교
- 비교 대상: 기존 RNA velocity method, single-cell integration method, MultiVeloVAE.
- 관찰된 차이: 기존 integration method는 velocity ODE와 modality relationship을 직접 보존하지 않고, 기존 velocity method는 multi-sample differential testing을 지원하지 않는다.
- 이 차이가 의미하는 것: MultiVeloVAE는 batch correction과 velocity inference를 하나의 probabilistic model 안에서 같이 수행한다.

##### 해석 시 주의점
- 주의점: Figure 1은 capability를 설명하는 개요이며, 실제 performance는 Figure 2-7과 Supplementary benchmark에서 확인해야 한다.

#### Figure 2
- 이 Figure가 필요한 이유: MultiVeloVAE가 chromatin 없이 RNA-only mode에서도 기존 RNA velocity method보다 잘 작동하는지 검증하기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: shared latent time, multi-basis ODE, variational inference는 scRNA-only dataset에서도 multi-lineage trajectory와 transcriptional boost를 더 잘 처리한다.

##### 패널별 설명
- a: BMMC dataset에서 velocity stream과 latent time을 보여준다. MultiVeloVAE velocity는 HSC cluster와 naive T cell population에서 시작하는 흐름을 만든다.
- b: developing mouse brain dataset에서 neural tube/neural crest root에서 neuron, glioblast, fibroblast 등 differentiated type으로 가는 transition과 latent time을 보여준다. 실제 capture time도 함께 표시된다.
- c: cell-state uncertainty와 latent time 관계를 보여준다. least differentiated cell에서 uncertainty가 높고, cell cycle score와 uncertainty가 대체로 inverse correlation을 보인다.
- d: mouse gastrulation과 human bone marrow hematopoietic cell에서 lineage inference를 보여준다.
- e: transcriptional boost 개념과 Smim1, Hba-x 같은 MURK gene phase portrait를 보여준다.
- f: 10개 scRNA-seq dataset에서 latent time과 true time의 Spearman correlation, GCBDir, Mann-Whitney U statistic을 benchmark한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVeloVAE RNA-only mode vs scVelo, UniTVelo, DeepVelo, VeloVI, PyroVelocity, cellDancer.
- 관찰된 차이: MultiVeloVAE는 true time label alignment, known transition direction, held-out test set fit quality에서 더 나은 성능을 보였다고 보고했다.
- 이 차이가 의미하는 것: MultiVeloVAE의 shared time과 probabilistic fitting은 multi-omic data가 없어도 기존 velocity model의 gene-time inconsistency와 transcriptional boost handling 문제를 줄인다.

##### 해석 시 주의점
- 주의점: Figure 2f의 exact benchmark values는 Source Data에 제공되며 본문에는 전체적 우위만 서술된다. scVelo/UniTVelo는 out-of-sample prediction이 없어 test fit metric에서 제외되었고, cellDancer는 explicit reconstruction이 없어 MSE/MAE에서 제외되었다.

#### Figure 3
- 이 Figure가 필요한 이유: MultiVeloVAE가 MultiVelo의 chromatin-aware velocity를 multi-lineage setting으로 확장한다는 핵심 주장을 직접 검증하기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: shared cell time과 cell-wise `kc`/`rho`를 사용하면 MultiVelo보다 lineage branch, priming, transition direction을 더 안정적으로 추정할 수 있다.

##### 패널별 설명
- a: human embryoid body 10X Multiome에서 MultiVeloVAE와 MultiVelo velocity stream/latent time을 비교한다. MultiVeloVAE는 NANOG+ pluripotent cell을 root로 놓고 mesendoderm, ectoderm 방향을 잡는다.
- b: PAX6, ENC1, SAT1의 generated spliced mRNA를 latent time 함수로 비교한다. MultiVeloVAE는 lineage-specific dynamic divergence를 더 잘 맞춘다.
- c: HSPC UMAP에서 MultiVeloVAE velocity stream과 latent time을 보여준다.
- d: HSPC에서 MultiVelo latent time inference 결과를 비교 대상으로 제시한다.
- e: variational inference가 포착한 cell-state uncertainty를 보여준다. stem-like/multipotent progenitor에서 uncertainty가 높다.
- f: mouse skin Wnt3에서 chromatin accessibility, unspliced, spliced, `kc - rho`를 UMAP에 표시해 continuous priming pattern을 보여준다.
- g: 4개 dataset에서 5-step neighbor까지의 generalized CBDir을 gene space와 embedded space에서 비교한다.
- h: MultiVelo와 runtime을 비교한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVeloVAE vs MultiVelo.
- 관찰된 차이: EB dataset에서 MultiVeloVAE는 NANOG+ root와 mesendoderm/ectoderm branch를 복원하고 MultiVelo는 unexpected backflow를 보였다. Mouse skin Wnt3에서는 MultiVelo가 IRS lineage 전체를 priming으로 잘못 해석하는 반면 MultiVeloVAE는 진짜 priming lineage와 IRS lineage를 분리했다.
- 이 차이가 의미하는 것: MultiVeloVAE의 continuous parameter와 shared time은 multi-lineage에서 discrete state와 single parameter set의 한계를 줄인다.

##### 해석 시 주의점
- 주의점: Figure 3g/h의 exact numeric values는 Source Data에 의존한다. 본문은 MultiVeloVAE가 더 높은 mean transition accuracy와 더 빠른 runtime을 보였다고 서술한다.

#### Figure 4
- 이 Figure가 필요한 이유: MultiVeloVAE가 multi-sample HSPC dataset에서 technical batch effect를 제거하면서 velocity와 biological variation을 보존하는지 보여주기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: batch correction과 velocity inference를 분리하지 않고 conditional VAE 안에서 함께 수행하면, sample covariate를 제거하면서 hematopoietic dynamics를 유지할 수 있다.

##### 패널별 설명
- a: 두 HSPC 10X Multiome sample의 original concatenated gene expression UMAP과 MultiVeloVAE latent cell embedding UMAP을 비교한다. integration 후 cell type이 sample 간 cohesive하게 합쳐지고 velocity stream이 HSC에서 downstream lineage로 향한다.
- b: lineage marker gene의 phase portrait/dynamic plot을 batch correction 전후로 보여준다.
- c: 두 batch의 rate parameter distribution이 대체로 overlap함을 보여준다.
- d: scIB batch effect removal metric으로 Scanorama, scVI와 비교한다.
- e: scIB biological variance conservation metric으로 비교한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVeloVAE vs Scanorama, scVI, 그리고 two-step batch correction + velocity inference.
- 관찰된 차이: MultiVeloVAE는 Scanorama와 비슷한 batch removal 성능을 보이고 embedded space에서 iLISI, kBET 같은 graph integration metric이 더 좋았다. scVI보다 batch removal metric은 낮지만 biological conservation metric은 더 높았다.
- 이 차이가 의미하는 것: MultiVeloVAE는 complete batch mixing만 최대화하기보다, velocity inference에 필요한 biological dynamics를 보존하는 integration을 목표로 한다.

##### 해석 시 주의점
- 주의점: MultiVeloVAE의 integration은 latent space에서 수행되며, high-dimensional `(c, u, s)` 값은 sample difference를 여전히 반영할 수 있다.

#### Figure 5
- 이 Figure가 필요한 이유: MultiVelo의 priming/decoupling state를 continuous, cell-specific coupling/decoupling factor로 확장했을 때 어떤 biological insight가 생기는지 보여주기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: lineage marker와 TF regulatory network에서 coupling/decoupling factor는 cell-type-specific regulatory state와 TF effect를 해석하는 축이 된다.

##### 패널별 설명
- a: HSPC lineage marker gene들의 chromatin, unspliced, spliced dynamics를 coupling factor `kappa`로 색칠한다. 특정 fate로 가는 cell에서 coupled induction/repression이 나타난다.
- b: 같은 gene dynamics를 decoupling factor `delta`로 색칠한다. HDC, AZU1, LYZ 등에서 lineage별 Model 1/Model 2 유사 decoupling phase가 보인다.
- c: Scenic+로 추론한 TF-region-gene GRN에 cell-type-specific region accessibility와 target gene coupling factor를 overlay한다.
- d: TF expression과 target gene coupling/decoupling factor의 Spearman correlation을 보여준다.
- e: housekeeping gene posterior-sampled dynamics와 credible interval을 보여준다.
- f: TF RNA, associated region accessibility, target gene `c/u/s` dynamics를 latent time 위에 정규화해 보여준다.

##### 본문에서 강조한 비교
- 비교 대상: coupling factor vs decoupling factor, TF positive/negative regulatory interaction, lineage-specific target gene dynamics.
- 관찰된 차이: Platelet과 DC에서 activated TF-regulated triplet의 target gene은 coupled induction pattern을 보이고, HSC에서는 positive decoupling으로 initial priming state를 보인다. Erythroid differentiation에서는 GATA1-linked genes의 coupling factor가 증가하고 GATA2-linked genes는 minor change를 보였다.
- 이 차이가 의미하는 것: coupling factor는 gene이 lineage/TF와 전체적으로 연결되는 방향을 보여주고, decoupling factor는 priming 또는 epigenomic repression 같은 fine-grained regulatory timing을 보여준다.

##### 해석 시 주의점
- 주의점: MultiVeloVAE는 gene-linked peak들의 summed accessibility `c`를 모델링하므로 individual cis-regulatory element effect는 downstream correlation/MI 분석으로만 추론한다.

#### Figure 6
- 이 Figure가 필요한 이유: MultiVeloVAE의 Bayesian differential testing이 실제 differentiating macrophage dataset에서 velocity/parameter의 time-varying difference를 찾을 수 있음을 보이기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MultiVeloVAE는 단순 expression difference가 아니라 chromatin opening rate, transcription rate, RNA velocity, spliced count의 divergence timing을 구분해 differential dynamics를 검정할 수 있다.

##### 패널별 설명
- a: human HSPC와 pro-macrophage cytokine 처리 7일 후 sample을 integration 전후 UMAP으로 보여준다. 처리 sample은 macrophage lineage 비율이 높다.
- b: macrophage cluster와 DC cluster에서 posterior-sampled cell을 비교한 differential velocity volcano plot과 significant gene velocity UMAP을 보여준다.
- c: macrophage vs DC에서 PROS1, LGMN, LGALS3 같은 gene의 `kc`, `rho`, `ds/dt`, `s` 차이가 latent time에 따라 어떻게 변하는지 보여준다.
- d: DC vs macrophage 방향의 differential dynamics gene을 같은 방식으로 보여준다.

##### 본문에서 강조한 비교
- 비교 대상: macrophage lineage vs dendritic cell lineage, time-varying differential dynamics vs static expression difference.
- 관찰된 차이: macrophage vs DC 비교에서 RNA velocity가 유의하게 다른 gene을 `p < 0.05`, `FDR < 0.05` 기준으로 찾았다. Figure 6b는 macrophage posterior-sampled cells `n = 850`, DC `n = 221` cluster에서 각각 5000 posterior-sampled cells를 생성해 비교했다.
- 이 차이가 의미하는 것: PROS1 같은 gene은 early latent time에서 `kc`/`rho` 차이가 먼저 크고, middle time에서 velocity 차이가 크며, late time에서 spliced count fold change가 커지는 iterative priming pattern을 보인다.

##### 해석 시 주의점
- 주의점: posterior-sampled pseudo-cell 기반 differential testing은 model posterior와 Gaussian process fit에 의존한다. 실제 perturbation validation 없이 driver gene으로 단정하면 안 된다.

#### Figure 7
- 이 Figure가 필요한 이유: MultiVeloVAE가 partially overlapping modality를 통합하고, RNA-only sample의 chromatin profile을 생성하며, in silico perturbation까지 수행할 수 있음을 보여주기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: conditional VAE와 multi-omic ODE를 결합하면 scRNA-only sample도 multiome sample과 함께 velocity inference에 넣고 missing ATAC profile 및 perturbation effect를 예측할 수 있다.

##### 패널별 설명
- a: 두 multi-omic HSPC sample과 하나의 scRNA BMMC sample을 통합한 UMAP을 보여준다.
- b: HBB, HDC, LYZ 같은 lineage marker의 original/batch-corrected 3D `c-u-s` phase portrait를 보여준다.
- c: scRNA-only cell에 대해 생성된 chromatin, unspliced, spliced dynamics를 latent time 위에 보여준다.
- d: 생성된 chromatin values와 chromatin velocity arrow를 보여준다.
- e: SPI1(PU.1) in silico KO 후 perturbation force와 latent state/time 변화의 PC1을 보여준다.
- f: GATA1 KO에 대해 같은 분석을 보여준다.
- g: CellRank로 KO 전후 terminal fate probability 변화를 계산한다.
- h: CellOracle perturbation identity shift와 비교한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVeloVAE missing ATAC generation vs scButterfly, scCross, MultiVI; MultiVeloVAE perturbation force vs CellOracle identity shift.
- 관찰된 차이: predicted ATAC은 top-likelihood gene에서 true accessibility와 high Pearson correlation을 보였고, scButterfly와 비슷하며 scCross/MultiVI보다 correlation과 MSE에서 좋았다. MultiVeloVAE-generated ATAC은 lineage separation이 가장 뚜렷했고 GCBDir도 가장 높았다. SPI1 KO는 GMP/DC 관련 lineage flow를 reverse하고, GATA1 KO는 MEP downstream lineage인 megakaryocyte/erythrocyte를 disrupt했다.
- 이 차이가 의미하는 것: MultiVeloVAE는 단순 cross-modality imputation이 아니라 velocity-guided biological variation을 유지하는 generative model로 쓸 수 있다.

##### 해석 시 주의점
- 주의점: in silico KO는 `c, u, s` 값을 0으로 두는 simulation이며, 실제 CRISPR perturbation 실험 결과가 아니다. CellOracle 비교도 batch-corrected counts를 별도로 공급한 조건에서 수행되었다.

### Results

#### Dataset별 결과

##### RNA-only benchmark: 10 real scRNA-seq datasets
- Dataset: BMMC, developing mouse brain, mouse gastrulation, human bone marrow hematopoietic cells, MEF reprogramming, pancreas 등 10개 real scRNA-seq dataset.
- 목적: chromatin 없이도 MultiVeloVAE RNA-only mode가 기존 RNA velocity method보다 trajectory/time/direction을 잘 추정하는지 평가.
- 사용한 데이터 규모: dataset별 cell/gene 수는 본문에 일괄 제공되지 않음. MEF reprogramming은 0-28일 범위의 6 time point를 사용.
- Baseline / 비교 대상: scVelo, UniTVelo, DeepVelo, VeloVI, PyroVelocity, cellDancer.
- Metric / 평가 기준: latent time과 true time의 Spearman correlation, GCBDir, Mann-Whitney U statistic for direction correctness, held-out test MSE/MAE.
- 주요 수치: exact metric values는 Source Data / Supplementary Fig. 4에 제공됨. 본문은 MultiVeloVAE가 data fitting, true time label alignment, test held-out generalization에서 더 좋은 성능을 보였다고 요약한다.
- 정성 결과: BMMC에서는 HSC cluster와 naive T cell population에서 velocity stream이 시작했고, developing mouse brain에서는 neural tube/neural crest root에서 differentiated cell type으로 smooth transition을 보였다.
- 논문 주장과의 연결: MultiVeloVAE의 shared latent time과 multi-basis ODE는 RNA-only dataset에서도 multi-lineage trajectory와 transcriptional boost 문제를 개선한다.

##### Human embryoid body 10X Multiome
- Dataset: 새로 생성한 7-day-old human embryoid body 10X Multiome.
- 목적: early human multi-lineage differentiation에서 MultiVeloVAE가 pluripotent root와 germ-layer branch를 복원하는지 평가.
- 사용한 데이터 규모: QC 후 4240 cells, highly variable gene selection 후 3138 genes.
- Baseline / 비교 대상: MultiVelo, known EB differentiation pattern, NANOG+ pluripotent cell, mesendoderm/ectoderm lineage markers.
- Metric / 평가 기준: velocity stream plausibility, latent time, marker gene generated spliced mRNA dynamics.
- 주요 수치: exact transition accuracy는 Figure 3g/Source Data에 의존. 본문은 MultiVeloVAE가 MultiVelo보다 backflow를 줄이고 branch-specific dynamics를 더 잘 fit한다고 서술한다.
- 정성 결과: MultiVeloVAE는 NANOG+ pluripotent cell을 root로 놓고 mesendoderm 및 ectoderm direction을 예측했다. PAX6, ENC1, SAT1은 각각 early ectoderm, neuroectoderm, mesendoderm 방향의 heightened dynamics를 보였다.
- 논문 주장과의 연결: MultiVeloVAE가 MultiVelo를 multi-lineage setting으로 일반화한다는 핵심 증거다.

##### Multi-omic mouse brain, HSPC, embryonic brain, mouse skin datasets
- Dataset: 이전 MultiVelo paper의 10X Multiome mouse brain, HSPC, human embryonic brain, SHARE-seq mouse skin 등.
- 목적: MultiVelo 대비 multi-omic velocity inference 개선과 priming/decoupling continuous modeling 평가.
- 사용한 데이터 규모: dataset별 exact cell/gene 수는 본문에 일괄 제공되지 않음. HSPC-HSPC integration은 17667 cells, 892 genes.
- Baseline / 비교 대상: MultiVelo, known cell type trajectories, diffusion-based pseudotime, marker gene dynamics.
- Metric / 평가 기준: k-step CBDir, Mann-Whitney U statistic, runtime, latent time correlation with diffusion pseudotime, coherence score.
- 주요 수치: Figure 3g는 4개 dataset에서 5-step neighbor까지 GCBDir을 비교하고, Figure 3h는 runtime `n = 5`를 비교한다. exact values는 Source Data에 의존.
- 정성 결과: mouse brain에서는 RG에서 neuron/astrocyte direction을 잡고 OPC를 neuronal/astrocyte lineage와 분리했다. HSPC에서는 MultiVelo latent time을 correction하고 stem-like/multipotent progenitor uncertainty를 높게 추정했다. mouse skin Wnt3에서는 진짜 priming lineage와 IRS lineage를 분리했다.
- 논문 주장과의 연결: continuous cell-specific `kc`/`rho`와 shared time이 multi-lineage chromatin-RNA velocity에 유리함을 보여준다.

##### Two HSPC 10X Multiome multi-sample integration
- Dataset: 서로 다른 donor에서 얻고 library preparation/sequencing이 months apart인 두 human HSPC 10X Multiome sample.
- 목적: MultiVeloVAE가 technical batch effect를 제거하면서 hematopoietic differentiation velocity와 biological variation을 보존하는지 평가.
- 사용한 데이터 규모: HSPC-HSPC integration input은 17667 cells, 892 genes.
- Baseline / 비교 대상: Scanorama, scVI, MultiVelo single-sample-only 또는 two-step correction workflow.
- Metric / 평가 기준: scIB batch effect removal metrics, graph integration metrics(iLISI, kBET), biological variance conservation metrics, marker gene dynamics, rate parameter distribution.
- 주요 수치: exact scIB metric values는 Figure 4d/e Source Data에 의존. 본문은 MultiVeloVAE가 Scanorama와 comparable batch removal, embedded space iLISI/kBET 우위, scVI보다 높은 biological conservation을 보였다고 서술한다.
- 정성 결과: integration 후 disjoint cell type이 latent state UMAP에서 cohesive하게 합쳐지고, HSC가 DC, granulocyte, erythrocyte, megakaryocyte precursor로 잡혔다. CD133 expression이 earliest cell과 맞았다.
- 논문 주장과의 연결: MultiVeloVAE는 batch correction과 velocity inference를 분리하지 않아 modality relationship과 dynamic structure를 보존한다.

##### HSPC coupling/decoupling and TF regulatory network
- Dataset: batch-corrected two HSPC multiome sample, Scenic+ GRN, ENCODE/ChromHMM downstream annotation.
- 목적: continuous coupling/decoupling factor가 lineage-specific gene regulation과 TF effect를 설명하는지 확인.
- 사용한 데이터 규모: Scenic+와 MultiVeloVAE 양쪽에 포함되고 여러 HSPC differentiation stage에서 발현되는 16 TF를 중심으로 분석.
- Baseline / 비교 대상: MultiVelo discrete state, Scenic+ TF-region-gene regulatory network, housekeeping genes, ChromHMM states.
- Metric / 평가 기준: coupling/decoupling factor, TF RNA expression과 target gene factor의 Spearman correlation, peak-rate mutual information, peak-factor correlation.
- 주요 수치: exact correlation coefficient values는 Figure 5 Source Data에 의존.
- 정성 결과: Platelet/DC의 activated TF-regulated triplet은 coupled induction을 보였고, HSC에서는 initial priming 상태가 나타났다. GATA1-linked erythroid genes는 coupling factor가 증가했고, GATA2-linked genes 중 일부는 erythrocyte maturation에서 negative decoupling으로 epigenomic repression을 보였다.
- 논문 주장과의 연결: MultiVeloVAE는 continuous factor를 통해 TF regulatory network와 velocity dynamics를 연결할 수 있다.

##### HSPC + pro-macrophage cytokine-treated sample
- Dataset: human HSPC 10X Multiome와 pro-macrophage cytokine 처리 후 7일 더 differentiation한 sample.
- 목적: macrophage vs DC lineage에서 differential velocity와 time-varying differential dynamics를 검정.
- 사용한 데이터 규모: HSPC-macrophage integration input은 9908 cells, 929 genes. Figure 6b는 macrophage cluster `n = 850`, DC cluster `n = 221`에서 각각 5000 posterior-sampled cells를 생성해 비교.
- Baseline / 비교 대상: DC lineage, macrophage lineage, CellRank terminal state analysis.
- Metric / 평가 기준: Bayesian differential velocity test, p-value, FDR, Bayes factor, LD/LFC over latent time, Gaussian process likelihood ratio test.
- 주요 수치: 유의 gene 기준은 RNA velocity `p < 0.05`, `FDR < 0.05`. Figure 6b에서 표시된 group은 `p < 0.05` 및 log difference < -3 또는 > 3이며, shown genes는 모두 FDR < 0.05 확인됨.
- 정성 결과: top-ranked differential kinetic genes는 macrophage 또는 DC marker gene이었다. PROS1, LGMN, LGALS3는 early `kc`/`rho`, middle velocity, late spliced expression 차이가 이어지는 iterative priming pattern을 보였다.
- 논문 주장과의 연결: MultiVeloVAE는 static differential expression이 아니라 dynamic parameter divergence를 시간축 위에서 검정할 수 있다.

##### Partial modality integration: two HSPC multiome + one BMMC scRNA
- Dataset: public healthy donor BMMC scRNA-seq sample + 두 HSPC 10X Multiome sample.
- 목적: RNA-only sample을 multiome sample과 통합하고 missing chromatin accessibility를 생성해 joint velocity inference가 가능한지 평가.
- 사용한 데이터 규모: partial integration은 27841 cells, 1044 genes.
- Baseline / 비교 대상: scButterfly, scCross, MultiVI, ground-truth ATAC baseline, CellOracle perturbation comparison.
- Metric / 평가 기준: predicted vs true accessibility Pearson correlation, MSE, GCBDir, lineage separation, qualitative phase portrait.
- 주요 수치: exact Pearson/MSE/GCBDir values는 Supplementary Fig. 19와 Source Data에 의존. 본문은 MultiVeloVAE가 scButterfly와 비슷하고 scCross/MultiVI보다 correlation/MSE에서 좋으며, GCBDir은 가장 높았다고 서술한다.
- 정성 결과: HBB, HDC, LYZ, PF4에서 generated chromatin profile은 transcription activation을 선행하는 priming pattern을 보였다. scRNA BMMC sample의 inferred temporal duration은 two multiome HSPC dataset보다 짧았다.
- 논문 주장과의 연결: MultiVeloVAE는 cross-modality imputation과 velocity-guided trajectory inference를 동시에 수행할 수 있다.

##### In silico perturbation of SPI1 and GATA1
- Dataset: integrated HSPC/BMMC setting에서 SPI1(PU.1), GATA1 perturbation simulation.
- 목적: pre-trained MultiVeloVAE가 key hematopoietic TF knockout effect를 velocity shift로 예측할 수 있는지 확인.
- 사용한 데이터 규모: CellRank fate probability group size는 Platelet 651, Erythrocyte 3043, Mast Cell 476, Granulocyte 1211, DC 294, Prog B 668.
- Baseline / 비교 대상: known SPI1/GATA1 hematopoietic roles, Dynamo paper result, CellOracle identity shift.
- Metric / 평가 기준: perturbation force, PC1 of perturbed-original latent state/time difference, CellRank fate probability change, CellOracle comparison.
- 주요 수치: exact probability changes는 Figure 7g Source Data에 의존.
- 정성 결과: SPI1 KO는 GMP/DC 관련 differentiation flow를 reverse했고, GATA1 KO는 MEP downstream lineage인 megakaryocyte/erythrocyte를 disrupt했다. CellOracle identity shift는 MultiVeloVAE perturbation force와 잘 맞았다.
- 논문 주장과의 연결: generative velocity model은 missing modality generation뿐 아니라 qualitative perturbation prediction에도 활용될 수 있다.

#### 전체 결과 요약
- 반복적으로 관찰된 패턴: MultiVeloVAE는 shared latent time, cell-specific `kc`/`rho`, conditional VAE를 통해 기존 RNA velocity, MultiVelo, integration-only tool이 각각 놓치는 multi-lineage/multi-sample/partial modality 문제를 통합적으로 처리한다.
- 가장 중요한 수치: EB dataset 4240 cells/3138 genes, HSPC-HSPC integration 17667 cells/892 genes, HSPC-macrophage integration 9908 cells/929 genes, partial HSPC+BMMC integration 27841 cells/1044 genes, differential macrophage/DC posterior sampling은 macrophage `n = 850`, DC `n = 221` cluster에서 각각 5000 cells, perturbation fate group sizes는 Platelet 651, Erythrocyte 3043, Mast Cell 476, Granulocyte 1211, DC 294, Prog B 668.
- baseline 대비 차이: RNA-only에서는 기존 velocity method보다 time/direction/fit metric에서 우수하다고 보고했고, multi-omic에서는 MultiVelo보다 GCBDir과 runtime이 개선되었다. multi-sample integration에서는 Scanorama/scVI와 비교해 biological conservation을 더 잘 유지하는 방향을 보였다.
- 결과 해석 시 주의점: exact benchmark values 다수는 Figure Source Data와 Supplementary에 의존하며 본문에는 주로 방향성/상대 우위가 제시된다. Perturbation과 cis-regulatory element effect는 computational prediction이므로 experimental validation이 필요하다.

### Limitations

#### 저자가 명시한 한계
- 한계 1: MultiVeloVAE도 다른 velocity method처럼 unspliced/spliced RNA measurement quality에 의존한다.
- 한계 2: differentiation potential이 낮은 mature cell type, 예를 들어 PBMC에서는 velocity inference가 어려울 수 있다.
- 한계 3: effective multi-sample integration을 위해서는 모든 dataset에서 reliable velocity inference가 필요하다.
- 한계 4: 현재 velocity inference method, deep-learning-based method 포함, 대부분 de novo training에 의존한다.
- 한계 5: future direction으로 known cell type에 대한 pre-trained, validated parameter set이 필요할 수 있다.
- 한계 6: CITE-seq 같은 추가 single-cell modality로 확장하는 것이 유망하다고 제시했다.

#### 분석자가 판단한 한계
- 부족한 점: benchmark exact values가 본문보다 Source Data/Supplementary에 많이 의존한다.
- 왜 중요한가: method superiority를 빠르게 평가하려면 dataset별 metric table과 effect size가 main text에 더 명확히 제시되는 편이 좋다.
- 어떤 증거가 부족한가: main text 안에서 각 dataset의 GCBDir, Spearman, MSE/MAE, runtime median을 표로 요약하면 재현성과 비교 가능성이 높아진다.

- 부족한 점: partial modality generation과 in silico perturbation은 generative model prediction이며, 실제 measured ATAC 또는 experimental KO와 동일하다고 볼 수 없다.
- 왜 중요한가: missing ATAC이 velocity-guided biological variation을 유지한다는 점은 강점이지만, downstream biological conclusion이 imputation artifact에 민감할 수 있다.
- 어떤 증거가 부족한가: held-out donor, held-out lineage, real perturb-seq/CRISPR perturbation, matched multiome validation이 필요하다.

- 부족한 점: conditional batch correction은 known sample covariate에 의존한다.
- 왜 중요한가: sample label이 biological condition과 강하게 confounded된 case-control study에서는 technical variation과 biological variation을 분리하기 어렵다.
- 어떤 증거가 부족한가: simulation 또는 controlled mixture design에서 confounding strength별 recovery 성능을 평가해야 한다.

#### 설명이 매끄럽지 않은 지점
- 연결이 약한 주장: coupling/decoupling factor와 TF regulatory effect의 연결.
- 현재 논문에서 제시한 근거: Scenic+ GRN, TF expression과 target factor Spearman correlation, example dynamics.
- 더 필요해 보이는 근거: TF perturbation 후 target gene `kc`, `rho`, `delta`, `kappa`가 예측대로 변하는지 확인하는 validation.

- 연결이 약한 주장: in silico SPI1/GATA1 KO 결과가 실제 fate disruption을 예측한다는 해석.
- 현재 논문에서 제시한 근거: known hematopoietic TF role, Dynamo와 유사한 result, CellOracle과 qualitative agreement.
- 더 필요해 보이는 근거: 실제 SPI1/GATA1 perturb-seq 또는 CRISPRi multiome에서 fate probability와 velocity shift 비교.

#### 정리되지 않은 질문
- 질문 1: sample covariate와 biological condition이 완전히 confounded된 case-control setting에서 MultiVeloVAE는 어떤 variation을 제거하고 어떤 variation을 보존하는가?
- 질문 2: pre-trained parameter set을 만들 때 tissue-specific RNA kinetics와 chromatin kinetics를 어떻게 일반화할 수 있는가?
- 질문 3: summed gene-linked accessibility `c` 대신 peak-level ODE를 직접 모델링하면 coupling/decoupling factor 해석이 얼마나 달라지는가?
- 질문 4: mature PBMC처럼 velocity signal이 약한 dataset에서 model uncertainty를 어떻게 downstream decision에 반영할 것인가?

## Final Takeaways
- 이 논문의 가장 큰 의미: MultiVeloVAE는 MultiVelo의 chromatin-RNA ODE와 VeloVAE의 probabilistic inference를 결합해, multi-lineage, multi-sample, multi-omic velocity inference와 differential dynamics testing을 하나의 framework로 만든다.
- 다음 논문으로 이어질 아이디어: case-control multiome cohort에서 MultiVeloVAE로 disease-specific differential velocity와 coupling/decoupling factor를 찾고, top TF-target pair를 perturb-seq로 검증한다.
- 설명을 더 매끄럽게 만들 방법: imputed chromatin, inferred `kc/rho`, velocity, final expression change를 시간순 causal chain으로 검증할 수 있는 matched time-course multiome 또는 nascent RNA dataset을 사용한다.
- 우선순위가 높은 후속 실험 / 분석: (1) real perturbation validation of SPI1/GATA1-like predictions, (2) confounded batch-condition simulation benchmark, (3) peak-level kinetic extension, (4) mature/low-velocity cell type에서 uncertainty-aware filtering, (5) CITE-seq/protein modality extension.
