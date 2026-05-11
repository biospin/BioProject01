# Multi-omic single-cell velocity models epigenome-transcriptome interactions and improves cell fate prediction

- 저자: Chen Li, Maria C. Virgilio, Kathleen L. Collins, Joshua D. Welch
- 연도: 2023
- Venue: Nature Biotechnology
- DOI: https://doi.org/10.1038/s41587-022-01476-y
- 분야: single-cell multi-omics, RNA velocity, epigenome-transcriptome dynamics
- 입력 PDF: `papers/MultiVelo.pdf`

### Background

#### 배경 스토리
- 문제의 출발점: cell fate는 DNA에서 RNA, protein으로 이어지는 gene expression regulation에 의해 결정되지만, single-cell sequencing은 cell을 파괴하므로 같은 cell이 시간에 따라 변하는 과정을 직접 관찰할 수 없다.
- 선행 접근 A: trajectory inference는 cell 간 similarity를 이용해 pseudotime을 만들고 developmental progress를 추정했다.
- A의 한계: similarity 기반 pseudotime은 transition direction이나 relative rate를 직접 예측하지 못한다.
- 선행 접근 B: RNA velocity는 spliced RNA와 unspliced RNA를 이용해 transcriptional change의 방향과 속도를 추정했다. scVelo 같은 dynamical model은 transient state까지 다룰 수 있게 했다.
- B의 한계: RNA-only model은 chromatin remodeling이 transcription rate를 바꾸는 과정을 직접 넣지 않는다. 특히 promoter/enhancer가 먼저 열렸지만 RNA는 아직 증가하지 않은 상태, 또는 chromatin closing과 transcriptional repression이 어긋나는 상태를 설명하기 어렵다.
- 이 논문으로 이어지는 gap: 10x Multiome, SHARE-seq, SNARE-seq처럼 같은 cell에서 RNA와 chromatin accessibility를 동시에 측정할 수 있게 되었지만, 이 multi-omic 정보를 mechanistic velocity model 안에서 함께 해석하는 방법이 부족했다.

#### 기본 개념
- RNA velocity: unspliced pre-mRNA와 spliced mature mRNA의 상대량을 이용해 cell의 미래 transcriptional state를 예측하는 방법이다. 이 논문은 여기에 chromatin accessibility를 추가한다.
- chromatin accessibility: promoter나 enhancer 주변 chromatin이 열려 transcription machinery가 DNA에 접근하기 쉬운 정도다. 논문에서는 `c(t)`로 모델링하며 transcription rate가 `c(t)`에 비례한다고 둔다.
- priming: chromatin이 먼저 열렸지만 RNA production은 아직 시작되지 않은 시간 구간이다. MultiVelo는 이 구간을 `ti - to`로 정량화한다.
- decoupling: chromatin closing과 transcriptional repression이 동시에 일어나지 않아 accessibility와 RNA가 서로 다른 방향으로 움직이는 구간이다. MultiVelo는 이 구간을 `tr - tc`로 정량화한다.
- model 1 / model 2: model 1은 chromatin closing이 transcriptional repression보다 먼저 시작되는 경우이고, model 2는 transcriptional repression이 먼저 시작되고 chromatin closing이 뒤따르는 경우다.

#### 이 논문이 필요성
- 핵심 이유: multi-omic snapshot 데이터에는 epigenome과 transcriptome 사이의 시간차가 들어 있지만, 기존 RNA-only velocity는 이를 독립적인 regulatory signal로 활용하지 못했다.
- 기존 방법으로 부족했던 지점: RNA-only phase portrait에서는 RNA가 거의 없는 cell들이 원점 부근에 몰려 cell ordering이 불명확해질 수 있다. chromatin accessibility는 RNA보다 먼저 변할 수 있어 early differentiation state를 더 잘 분리할 수 있다.
- 이 논문이 해결하려는 방향: chromatin accessibility, unspliced RNA, spliced RNA를 하나의 ODE system으로 묶어 cell latent time, gene-specific switch time, rate parameter, state assignment를 동시에 추정한다.

### Overview
- Figure 1 포함 여부: 포함됨 - Figure 1은 MultiVelo의 ODE 구조, model 1/model 2의 event ordering, priming/decoupling, 네 가지 cell-gene state를 모두 설명하는 전체 방법 개요다.

#### 핵심 개념
- 개념: gene expression dynamics는 chromatin accessibility `c`, unspliced RNA `u`, spliced RNA `s`가 시간에 따라 함께 변하는 과정이라는 관점이다.
- 이 개념이 필요한 이유: chromatin opening과 closing은 RNA induction/repression보다 앞서거나 뒤처질 수 있다. 이 시간차를 모델링해야 epigenome-transcriptome interaction을 cell fate prediction에 반영할 수 있다.

#### Method 관점
- 논문이 이 개념을 바라본 방식: MultiVelo는 chromatin opening/closing, transcription induction/repression, splicing, degradation 또는 nuclear export를 rate parameter와 switch time으로 표현하는 ODE model로 재구성한다.
- 입력: 같은 cell에서 측정된 chromatin accessibility, unspliced pre-mRNA count, spliced mRNA count.
- 처리 과정: 각 gene의 `(c, u, s)` 3D phase portrait에 ODE curve를 맞추고, 각 cell을 curve의 가장 가까운 지점에 projection해 latent time `t`와 state `k`를 부여한다. parameter와 cell time은 heuristic initialization 뒤 expectation-maximization으로 반복 추정한다.
- 출력: velocity vector, latent time, gene별 model 1/model 2 또는 partial kinetics, primed/coupled-on/decoupled/coupled-off state, priming 및 decoupling interval length.

#### 이 관점으로 알 수 있는 것
- 알 수 있게 된 점 1: RNA-only model에서는 구분하기 어려운 early chromatin change를 이용해 cell transition direction을 더 자연스럽게 추정할 수 있다.
- 알 수 있게 된 점 2: chromatin과 RNA가 항상 동시에 움직이는 것이 아니라, priming과 decoupling이라는 반복적인 time lag pattern이 존재한다.
- 알 수 있게 된 점 3: TF expression과 motif accessibility, disease-associated SNP accessibility와 linked gene expression 사이의 시간차도 latent time 위에서 분석할 수 있다.

#### 기대 효과
- 성능 또는 분석상 기대 효과: RNA-only velocity보다 cell fate prediction과 local direction consistency가 개선되고, epigenomic regulation의 시점을 gene별로 해석할 수 있다.
- benchmark / baseline 관련 근거: mouse skin SHARE-seq에서 MultiVelo latent time은 Palantir pseudotime과 Spearman 0.51로 상관되어 scVelo의 0.44보다 높았다. mouse brain, HSPC, fetal human brain에서도 scVelo가 backflow 또는 hierarchy mismatch를 보인 반면 MultiVelo는 알려진 differentiation trajectory와 더 일치한다고 보고했다.
- 적용 가능한 상황: 같은 cell에서 RNA와 ATAC을 함께 측정한 10x Multiome, SHARE-seq 등 single-cell multi-omic dataset, 특히 early stem/progenitor cell처럼 epigenomic change가 빠르게 일어나는 상황.

### Figure / Table Analysis

#### Figure 1
- 이 Figure가 필요한 이유: MultiVelo가 단순히 RNA velocity에 ATAC feature를 추가한 모델이 아니라, chromatin accessibility와 RNA production의 event ordering을 explicit하게 모델링한다는 점을 정의하기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: gene expression 과정에는 chromatin opening, transcription induction, chromatin closing, transcription repression의 시간차가 있으며, 이 시간차로 priming, decoupling, model 1/model 2를 구분할 수 있다.

##### 패널별 설명
- a: `c`, `u`, `s`를 연결하는 세 ODE와 chromatin opening/closing, transcription, splicing, degradation 또는 nuclear export 과정을 제시한다.
- b: chromatin closing과 transcriptional repression의 순서가 다른 model 1과 model 2를 비교한다.
- c: chromatin이 먼저 열리고 RNA가 아직 없는 priming 구간을 보여준다.
- d: chromatin closing과 transcription repression이 어긋나 accessibility와 RNA가 반대 방향으로 움직이는 decoupling 구간을 보여준다.
- e: primed, coupled-on, decoupled, coupled-off 네 상태의 phase portrait를 제시한다.
- f, g: model 1 gene과 model 2 gene의 simulated `(c, u, s)` 값이 서로 다른 trajectory를 만든다는 점을 보여준다.

##### 본문에서 강조한 비교
- 비교 대상: chromatin closing이 transcriptional repression보다 먼저 시작되는 model 1과, transcriptional repression이 먼저 시작되는 model 2.
- 관찰된 차이: model 1 gene은 transcriptional induction phase에서 chromatin accessibility가 최대가 되고, model 2 gene은 transcriptional repression phase에서 accessibility가 최대가 된다.
- 이 차이가 의미하는 것: RNA phase portrait만으로는 구분하기 어려운 regulatory timing을 chromatin accessibility가 구분해 준다.

##### 해석 시 주의점
- 주의점: Figure 1은 model assumption과 simulated behavior를 설명하는 개요이므로, 실제 biological frequency와 generality는 이후 dataset 결과로 확인해야 한다.

#### Figure 2
- 이 Figure가 필요한 이유: embryonic mouse brain 10x Multiome dataset에서 MultiVelo가 알려진 cortical development trajectory를 복원하고, model 1/model 2 gene class를 실제 데이터에서 구분할 수 있음을 보여주기 위해 배치되었다.
- 이 Figure가 뒷받침하는 주장: chromatin accessibility를 통합하면 RNA-only scVelo보다 cell fate direction이 더 생물학적으로 타당해지고, gene regulation에는 두 distinct mechanism이 존재한다.

##### 패널별 설명
- a: MultiVelo velocity stream과 latent time이 RG에서 neuron, astrocyte, oligodendrocyte 방향으로 이어지는 known trajectory를 복원한다.
- b: scVelo RNA-only velocity는 upper layer neuron 내부에서 biologically implausible backflow를 예측한다.
- c: cell cycle score가 RG 근처 cycling population에서 높아 MultiVelo latent time의 early root가 생물학적 기대와 맞음을 보조한다.
- d: Eomes, Tle4 같은 marker gene에서 RNA phase portrait만으로는 cell ordering이 어렵지만, chromatin value가 먼저 상승해 differentiating cell을 더 잘 분리한다.
- e: Satb2(model 1)와 Gria2(model 2)의 RNA phase portrait를 chromatin 값으로 색칠해 model별 maximum accessibility timing 차이를 보여준다.
- f: `c-u`, `c-s` pairwise phase portrait에서도 model 1과 model 2 차이가 드러난다.
- g: model 2 gene이 model 1 gene보다 latent time상 더 이른 시점에 highest spliced expression을 보이는 heatmap을 제시한다.
- h: fit gene `n = 865`에서 model 1 41.4%, model 2 26.7%, induction-only 29.5%, repression-only 2.4%의 비율을 제시한다.
- i: MultiVelo가 `(c, u, s)` 3D velocity vector를 예측할 수 있음을 시각화한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVelo와 scVelo, model 1 gene과 model 2 gene.
- 관찰된 차이: scVelo는 upper layer neuron에서 backflow를 보였고, MultiVelo는 known cortical development와 맞는 velocity를 보였다. model 2 gene은 cell-cycle 관련 GO term에 enriched되며 model 1보다 최고 spliced expression이 더 이른 latent time에 나타났다.
- 이 차이가 의미하는 것: chromatin accessibility는 RNA-only model이 놓치는 early regulatory change를 제공하며, model 2는 transient activation과 관련될 가능성이 있다.

##### 해석 시 주의점
- 주의점: model 2가 transient activation에 쓰인다는 설명은 저자의 hypothesis이며, causal perturbation으로 직접 증명된 것은 아니다.

#### Figure 3
- 이 Figure가 필요한 이유: MultiVelo가 gene별 kinetics만 분류하는 것이 아니라 cell-gene state를 primed, coupled-on, decoupled, coupled-off로 배정하고 interval length를 정량화할 수 있음을 보여주기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: embryonic mouse brain에서 epigenome과 transcriptome은 일부 구간에서 coupled되지만, priming과 decoupling이라는 반복적인 discordance state도 관찰된다.

##### 패널별 설명
- a: Grin2b는 induction-only gene으로 primed와 coupled-on state만 보이고, Nfix는 complete trajectory로 네 state를 모두 보이며, Epha5는 model 2 gene으로 coupled-on과 decoupled state가 강조된다.
- b: Robo2, Gria2, Grin2b의 UMAP에서 ATAC, unspliced RNA, state assignment를 나란히 비교한다. circled region은 accessibility와 RNA가 어긋나는 priming 또는 decoupling 구간이다.
- c: latent time에 따른 `c(t)`, `u(t)`, `s(t)`를 보여준다. Robo2는 chromatin closing 뒤 RNA가 유지되는 model 1 decoupling을, Gria2는 repression 이후에도 chromatin이 계속 상승하는 model 2 decoupling을, Grin2b는 긴 priming을 보인다.
- d: cell마다 각 state에 속한 high-likelihood gene 수를 세어 neuronal cluster를 따라 state transition cascade가 나타남을 보여준다.
- e: 전체 fit gene에서 네 state interval length를 box plot으로 요약한다.
- f: chromatin closing rate와 opening rate의 비율을 요약한다.

##### 본문에서 강조한 비교
- 비교 대상: coupled state와 primed/decoupled state, gene별 state transition.
- 관찰된 차이: coupled-on/off interval이 primed/decoupled interval보다 길며, median primed interval은 전체 시간의 21%, median decoupled interval은 19%였다. chromatin closing rate/opening rate의 median ratio는 거의 1이었다.
- 이 차이가 의미하는 것: chromatin과 RNA는 전반적으로 correlated하지만, 상당한 비율의 시간에서 modality 간 time lag가 존재한다.

##### 해석 시 주의점
- 주의점: UMAP의 색상 차이는 정성적 확인이며, state assignment는 ODE fit과 latent time 추정의 정확도에 의존한다.

#### Figure 4
- 이 Figure가 필요한 이유: MultiVelo가 10x Multiome뿐 아니라 SHARE-seq mouse skin dataset에서도 chromatin potential과 priming을 재현하고 정량화할 수 있음을 보이기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: chromatin accessibility가 gene expression을 선행하는 현상은 MultiVelo의 priming model로 설명되며, RNA-only velocity보다 differentiation direction을 더 잘 잡는다.

##### 패널별 설명
- a: MultiVelo velocity와 latent time이 TAC에서 IRS와 hair shaft cell로 이어지는 differentiation direction을 보여준다.
- b: scVelo RNA-only velocity는 hair-shaft differentiation direction을 잘 포착하지 못한다.
- c: fit gene `n = 960`에서 induction-only 66.6%, model 1 32.4%, model 2 1.0% 비율을 제시한다. repression-only는 거의 없거나 표시되지 않는다.
- d: Wnt3의 ATAC, unspliced RNA, spliced RNA UMAP을 비교해 accessibility가 RNA보다 먼저 나타나는 time delay를 보여준다.
- e: Wnt3, Dsc1은 induction-only와 priming을, Cux1, Dlx3, Cobll1은 induction/repression과 짧은 decoupling을 보인다.
- f: Wnt3에서 DTW로 `c-s`, `u-s` time series를 align하고 instantaneous time lag를 계산한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVelo latent time과 scVelo, chromatin-spliced RNA lag와 unspliced-spliced RNA lag.
- 관찰된 차이: MultiVelo latent time은 original SHARE-seq 논문의 Palantir pseudotime과 Spearman 0.51로 상관되어 scVelo의 0.44보다 높았다. Wnt3에서 `c-s` delay와 `u-s` delay는 모두 양수였고, `c-s` delay가 더 길었으며 maximum `c-s` delay는 전체 time range 1 중 0.6에 도달했다.
- 이 차이가 의미하는 것: chromatin accessibility가 gene expression을 선행한다는 chromatin potential 현상을 velocity framework에서 정량화할 수 있다.

##### 해석 시 주의점
- 주의점: DTW는 lagged correlation을 정렬하는 방법이므로, chromatin change가 expression change를 직접 유발했다는 causal evidence는 아니다.

#### Figure 5
- 이 Figure가 필요한 이유: 혈액 differentiation처럼 RNA velocity가 어려운 system에서도 chromatin 정보를 넣으면 hierarchy와 lineage direction을 더 잘 설명할 수 있음을 보여주기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: human HSPC에서도 model 1/model 2, priming, terminal marker gene의 chromatin-leading expression pattern이 반복적으로 나타난다.

##### 패널별 설명
- a: MultiVelo와 scVelo velocity stream을 비교한다. MultiVelo는 HSPC differentiation hierarchy와 더 일치하는 방향성을 보인다.
- b: fit gene `n = 936`에서 model 1 40.4%, model 2 19.8%, induction-only 39.3%, repression-only 0.5% 비율을 제시한다.
- c: primed/decoupled interval이 coupled phase보다 짧다는 box plot을 제시한다.
- d: UBE2C, GTSE1, KIF20B 같은 G2/M phase marker가 myeloid, erythroid, platelet lineage에서 model 2 pattern을 보인다.
- e: AZU1, HBD, HDC, LYZ, PF4 등 terminal cell-type marker가 chromatin accessibility 증가 뒤 RNA expression 증가를 보이는 priming 사례를 제시한다.
- f: 같은 gene들의 chromatin, unspliced, spliced velocity를 latent time에 따라 보여준다.
- g: 같은 gene들의 RNA phase portrait를 제시한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVelo와 RNA-only velocity, early progenitor와 differentiated cell.
- 관찰된 차이: 11,605 high-quality cell에서 MultiVelo는 local consistency와 biological accuracy를 개선했다고 보고했다. model 2 gene은 cell-cycle GO term에 enriched되며 FDR < 0.002였다. chromatin velocity는 marker gene에서 초기에 가장 높고, RNA velocity는 lineage commitment 과정에서 증가한 뒤 terminal state에서 equilibrium에 접근한다.
- 이 차이가 의미하는 것: epigenomic priming은 HSPC lineage differentiation에서도 terminal marker expression 이전에 나타날 수 있다.

##### 해석 시 주의점
- 주의점: Figure 5의 성능 평가는 주로 biological plausibility와 local consistency 중심이며, 정량 benchmark는 제한적으로 제시된다.

#### Figure 6
- 이 Figure가 필요한 이유: MultiVelo latent time을 gene 주변 chromatin뿐 아니라 TF motif accessibility와 disease-associated SNP accessibility 분석으로 확장할 수 있음을 보여주기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MultiVelo는 fetal human brain에서 cell fate dynamics를 개선할 뿐 아니라 TF expression, motif accessibility, disease SNP, linked gene expression 사이의 시간 관계를 분석할 수 있다.

##### 패널별 설명
- a: fetal human brain 10x Multiome dataset에서 MultiVelo velocity와 latent time이 known brain development pattern과 일치함을 보여준다.
- b: scVelo RNA-only velocity는 IPC와 upper layer excitatory neuron에서 incongruous backflow를 보인다.
- c: ROBO2(model 1)와 MEF2C(model 2)의 phase portrait를 비교한다.
- d: fit gene `n = 747`에서 induction-only 50.5%, model 1 38.3%, model 2 8.2%, repression-only 3.1% 비율을 제시한다.
- e: EGR1, EOMES, FOXP2, PBX3의 TF gene expression과 motif accessibility time series를 DTW로 align한다.
- f: expressed TF 전체에서 motif time lag quantile을 보여주며 median time lag가 대부분 양수임을 제시한다.
- g: 757개 SNP를 maximum accessibility time과 linked gene maximum expression time의 관계로 분류하고 세 major group을 제시한다.

##### 본문에서 강조한 비교
- 비교 대상: MultiVelo와 scVelo, TF expression time과 motif accessibility time, SNP accessibility time과 linked gene expression time.
- 관찰된 차이: TF expression peak가 downstream motif accessibility peak보다 앞서는 패턴이 대부분의 TF에서 나타났다. GWAS 관련 6,968 SNP 중 model-fit gene에 linked된 accessibility peak와 겹치는 757 SNP를 분석했고, accessibility가 early/late인지 및 linked gene expression보다 앞서는지/뒤따르는지에 따라 세 그룹이 보였다.
- 이 차이가 의미하는 것: MultiVelo latent time은 gene-level velocity를 넘어 regulatory element와 disease variant의 temporal function을 해석하는 축으로 쓰일 수 있다.

##### 해석 시 주의점
- 주의점: 저자도 TF lag의 mechanism은 추가 데이터 없이는 결론낼 수 없다고 명시했다. SNP accessibility가 linked gene expression보다 앞선다고 해서 직접 regulatory causality가 증명되는 것은 아니다.

### Results

#### Dataset별 결과

##### Embryonic mouse brain 10x Multiome
- Dataset: embryonic mouse brain E18 10x Multiome.
- 목적: MultiVelo가 known mammalian cortex development trajectory를 복원하고, model 1/model 2 gene regulation을 구분할 수 있는지 검증.
- 사용한 데이터 규모: 본문에서 total cell 수는 명시되지 않음. high-likelihood model fit gene은 처음 적용 결과에서 426개로 언급되며, Figure 2h의 kinetics proportion은 fit gene `n = 865` 기준이다.
- Baseline / 비교 대상: RNA-only scVelo, known cortex development trajectory, cell cycle score.
- Metric / 평가 기준: biological plausibility of velocity direction, latent time consistency, model class proportion, Wilcoxon rank-sum test.
- 주요 수치: Figure 2h 기준 model 1 41.4%, model 2 26.7%, induction-only 29.5%, repression-only 2.4%. model 1과 model 2 gene은 total expression/accessibility level에서 유의한 차이가 없었다(Wilcoxon P = 0.38, P = 0.32). model 2 gene은 model 1보다 highest spliced expression이 더 이른 latent time에 나타났다(P = 9 x 10^-7, Wilcoxon rank-sum one-sided test). Figure 3에서는 median primed interval이 전체 time의 21%, median decoupled interval이 19%였다. chromatin closing/opening rate ratio median은 거의 1이었다.
- 정성 결과: MultiVelo는 RG에서 neuron, astrocyte, oligodendrocyte 방향으로 알려진 trajectory를 복원했다. scVelo는 upper layer neuron에서 biologically implausible backflow를 보였다. Eomes, Tle4 같은 marker gene에서 chromatin이 RNA보다 먼저 변화해 RNA-only phase portrait에서 보이지 않는 ordering 정보를 제공했다.
- 논문 주장과의 연결: chromatin accessibility를 통합하면 early regulatory change를 이용해 RNA-only velocity의 ambiguity를 줄이고, epigenome-transcriptome timing에 기반한 gene class를 정의할 수 있음을 보여준다.

##### Mouse dorsal skin SHARE-seq
- Dataset: mouse hair follicle / dorsal skin SHARE-seq dataset.
- 목적: 기존 SHARE-seq 논문에서 제시한 chromatin potential, 특히 Wnt3의 accessibility-leading expression pattern을 MultiVelo로 재현하고 정량화.
- 사용한 데이터 규모: Figure 4c의 fit gene `n = 960`. cell 수는 본문 발췌 범위에서 명시되지 않음.
- Baseline / 비교 대상: scVelo RNA-only model, original SHARE-seq paper의 Palantir pseudotime 및 diffusion map result.
- Metric / 평가 기준: Palantir pseudotime과 latent time의 Spearman correlation, differentiation direction consistency, DTW time lag.
- 주요 수치: MultiVelo latent time과 Palantir pseudotime의 Spearman correlation은 0.51, scVelo는 0.44. kinetics proportion은 induction-only 66.6%, model 1 32.4%, model 2 1.0%. Wnt3의 maximum `c-s` delay는 normalized total time range 1 중 0.6.
- 정성 결과: MultiVelo는 TAC에서 IRS와 hair shaft cell로 가는 direction을 맞췄고, scVelo는 hair-shaft differentiation direction을 잘 잡지 못했다. Wnt3, Dsc1은 induction-only priming을 보였고 Cux1, Dlx3, Cobll1은 짧은 decoupling을 보였다.
- 논문 주장과의 연결: chromatin accessibility가 expression을 선행하는 현상을 MultiVelo가 priming interval과 DTW lag로 정량화할 수 있음을 보여준다.

##### Human HSPC RNA+ATAC
- Dataset: human hematopoietic stem and progenitor cells with single-nucleus RNA-seq and ATAC-seq.
- 목적: RNA velocity가 어려운 hematopoiesis에서 chromatin 통합이 differentiation hierarchy와 lineage marker dynamics를 더 잘 설명하는지 평가.
- 사용한 데이터 규모: filtering 후 11,605 high-quality cell. Figure 5b의 fit gene `n = 936`.
- Baseline / 비교 대상: scVelo RNA-only model, known HSPC differentiation hierarchy와 marker gene annotation.
- Metric / 평가 기준: local consistency, biological accuracy, kinetics proportion, GO enrichment FDR.
- 주요 수치: kinetics proportion은 model 1 40.4%, model 2 19.8%, induction-only 39.3%, repression-only 0.5%. model 2 gene은 cell-cycle 관련 GO term에 enriched되었고 FDR < 0.002.
- 정성 결과: MultiVelo는 HSC, MPP, LMPP, GMP, MEP, erythrocyte, granulocyte, dendritic cell progenitor, platelet 등으로 이어지는 hierarchy와 더 맞는 velocity를 보였다. AZU1, HBD, HDC, LYZ, PF4 같은 terminal marker는 chromatin accessibility 증가 뒤 RNA expression이 증가하는 priming pattern을 보였다.
- 논문 주장과의 연결: epigenomic priming과 model 2 cell-cycle pattern이 brain뿐 아니라 blood differentiation에서도 반복된다는 점을 보여준다.

##### Fetal human brain 10x Multiome
- Dataset: developing human cortex 10x Multiome.
- 목적: human brain development에서 MultiVelo의 velocity prediction과 regulatory time lag 분석 확장성을 평가.
- 사용한 데이터 규모: Figure 6d의 fit gene `n = 747`. GWAS psychiatric disease 관련 SNP 6,968개 중 model-fit gene에 linked된 accessibility peak와 겹치는 757개 SNP 분석.
- Baseline / 비교 대상: scVelo RNA-only model, known brain development pattern, TF motif accessibility via chromVar, DTW.
- Metric / 평가 기준: velocity direction plausibility, kinetics proportion, TF motif time lag quantile, SNP accessibility-expression timing.
- 주요 수치: kinetics proportion은 induction-only 50.5%, model 1 38.3%, model 2 8.2%, repression-only 3.1%. expressed TF 전체에서 median motif time lag가 대부분 양수였다. SNP 분석은 757개 SNP를 대상으로 수행했다.
- 정성 결과: MultiVelo는 RG 근처 cycling population을 earliest latent time으로 추정했고 known development pattern과 맞는 velocity를 보였다. scVelo는 IPC와 upper layer excitatory neuron에서 incongruous backflow를 보였다. TF expression peak가 motif accessibility peak보다 먼저 나타나는 경향이 확인되었고, SNP는 maximum accessibility time과 linked gene expression time에 따라 세 그룹으로 나뉘었다.
- 논문 주장과의 연결: MultiVelo latent time이 cell fate뿐 아니라 TF regulation과 disease-associated variant function의 temporal interpretation에도 활용될 수 있음을 보여준다.

#### 전체 결과 요약
- 반복적으로 관찰된 패턴: model 1은 모든 주요 dataset에서 model 2보다 대체로 많았고, induction-only gene도 상당한 비율을 차지했다. model 2 gene은 mouse brain과 HSPC에서 cell-cycle 관련 gene과 연결되었다.
- 가장 중요한 수치: mouse skin에서 MultiVelo-Palantir Spearman 0.51 대 scVelo 0.44, HSPC 11,605 cell, fetal human brain SNP 분석 757개, mouse brain primed interval median 21%와 decoupled interval median 19%.
- baseline 대비 차이: scVelo는 mouse brain, mouse skin, fetal human brain에서 backflow 또는 direction mismatch를 보인 반면, MultiVelo는 chromatin 정보를 이용해 known differentiation direction과 더 일치한다고 보고했다.
- 결과 해석 시 주의점: 정량 benchmark가 모든 dataset에서 같은 metric으로 제시되지는 않는다. 여러 핵심 비교는 UMAP stream plot과 biological plausibility에 의존하며, causal regulation은 직접 perturbation으로 검증되지 않았다.

### Limitations

#### 저자가 명시한 한계
- 한계 1: TF expression과 binding site accessibility 사이의 time lag mechanism은 추가 데이터 없이는 conclusively determine할 수 없다고 명시했다.
- 한계 2: 미래 방향으로 TF binding, chromatin looping 같은 gene expression process의 추가 단계를 모델에 포함하는 확장이 필요하다고 제시했다.
- 한계 3: velocity estimate를 trajectoryNet, WaddingtonOT, VeloAE 같은 global dynamics prediction method와 결합할 수 있다고 했지만, 본 논문 자체의 핵심 모델은 global fate probability model은 아니다.

#### 분석자가 판단한 한계
- 부족한 점: benchmark가 dataset마다 같은 정량 metric으로 통일되어 있지 않다.
- 왜 중요한가: “cell fate prediction 개선”이라는 주장이 강한데, 일부 dataset은 stream plot의 biological plausibility 중심으로 평가되어 성능 차이를 객관적으로 비교하기 어렵다.
- 어떤 증거가 부족한가: held-out transition prediction, ground-truth lineage tracing, perturbation-based validation, 동일 metric 기반 multi-dataset benchmark가 더 필요하다.

- 부족한 점: ODE model은 chromatin modifier, pioneer factor, TF, chromatin looping 등 복잡한 regulatory mechanism을 rate constant로 추상화한다.
- 왜 중요한가: 이 단순화는 model interpretability를 높이지만, 특정 gene에서 observed lag가 어떤 molecular mechanism 때문인지 직접 분해하지 못한다.
- 어떤 증거가 부족한가: TF binding, enhancer-promoter contact, chromatin remodeler activity를 동시에 측정하거나 별도 validation하는 자료가 필요하다.

- 부족한 점: disease-associated SNP 분석은 temporal association을 보여주지만 variant function의 causal evidence는 아니다.
- 왜 중요한가: SNP accessibility가 linked gene expression보다 먼저 나타나면 regulatory candidate로 볼 수는 있지만, 실제 eQTL effect나 enhancer function을 증명하지는 않는다.
- 어떤 증거가 부족한가: CRISPR perturbation, allele-specific accessibility/expression, perturb-seq 또는 reporter assay가 필요하다.

#### 설명이 매끄럽지 않은 지점
- 연결이 약한 주장: model 2가 rapid transient activation에 유용할 수 있다는 해석.
- 현재 논문에서 제시한 근거: model 2 gene이 cell-cycle GO term에 enriched되고, highest spliced expression이 model 1보다 더 이른 latent time에 나타난다는 관찰.
- 더 필요해 보이는 근거: cell-cycle perturbation, time-resolved validation, model 2 gene의 protein-level 또는 TF activity dynamics 확인.

- 연결이 약한 주장: chromatin accessibility 통합이 cell fate prediction을 개선한다는 일반 주장.
- 현재 논문에서 제시한 근거: 여러 dataset의 UMAP stream plot, mouse skin Spearman correlation, known trajectory와의 qualitative consistency.
- 더 필요해 보이는 근거: 동일한 metric과 동일한 high-likelihood gene selection 기준으로 MultiVelo, scVelo, chromatin-only, ablation model을 비교하는 benchmark.

#### 정리되지 않은 질문
- 질문 1: priming과 decoupling interval length는 sequencing depth, ATAC sparsity, gene selection threshold에 얼마나 민감한가?
- 질문 2: model 1/model 2 classification은 같은 tissue의 replicate나 다른 platform에서 얼마나 재현되는가?
- 질문 3: TF expression이 motif accessibility보다 앞서는 time lag가 protein translation delay, TF activation delay, chromatin remodeler recruitment 중 무엇을 반영하는가?
- 질문 4: SNP accessibility-expression timing group은 실제 disease mechanism 또는 cell type-specific risk와 얼마나 연결되는가?

## Final Takeaways
- 이 논문의 가장 큰 의미: MultiVelo는 single-cell multi-omics에서 chromatin accessibility를 RNA velocity의 외부 보조 feature가 아니라 transcription dynamics를 설명하는 시간 변수로 통합했다. 그 결과 priming, decoupling, model 1/model 2 같은 epigenome-transcriptome timing concept을 gene별, cell별로 정량화할 수 있게 했다.
- 다음 논문으로 이어질 아이디어: MultiVelo가 예측한 priming gene과 decoupled gene을 perturb-seq 또는 CRISPRi/CRISPRa로 검증해, chromatin opening이 실제 RNA induction을 유도하는지 확인한다.
- 설명을 더 매끄럽게 만들 방법: 같은 dataset에서 full MultiVelo, RNA-only, chromatin-only, no-switch-time, no-model2 같은 ablation을 구성하고, latent time accuracy, transition direction, held-out modality reconstruction을 동일 metric으로 비교한다.
- 우선순위가 높은 후속 실험 / 분석: TF lag 분석에서는 TF protein abundance, motif accessibility, target gene expression을 함께 측정하는 multi-modal dataset이 우선이다. SNP 분석에서는 accessibility가 expression보다 앞서는 candidate SNP를 골라 allele-specific effect와 CRISPR perturbation으로 linked gene expression 변화를 검증하는 것이 중요하다.
