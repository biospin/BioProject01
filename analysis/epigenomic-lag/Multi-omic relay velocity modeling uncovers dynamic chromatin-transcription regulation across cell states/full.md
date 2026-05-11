# Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states

- 저자: Ari Hong, Sangseon Lee, Kwangsoo Kim
- 연도: 2026
- Venue: Nature Communications
- DOI: https://doi.org/10.1038/s41467-025-67259-6
- 분야: single-cell multi-omics, RNA velocity, chromatin accessibility, relay velocity, deep learning
- 입력 PDF: `papers/MoFlow.pdf`

### Background

#### 배경 스토리
- 문제의 출발점: cell fate transition은 gene expression program과 epigenetic modification이 함께 바뀌는 동적 과정이지만, single-cell RNA-seq는 각 cell의 static snapshot만 제공하므로 실제 시간 방향과 regulatory timing을 직접 관찰하기 어렵다.
- 선행 접근 A: RNA velocity는 unspliced RNA와 spliced RNA의 비율을 이용해 cell의 미래 transcriptional state를 예측했다. scVelo 같은 ODE 기반 dynamical model은 gene-specific kinetic rate와 latent time을 추정해 transient state까지 다룰 수 있게 했다.
- A의 한계: ODE 기반 model은 gene마다 하나의 transcriptional path를 가정하는 경향이 있고, heterogeneous 또는 branching system에서는 fixed kinetic assumption이 맞지 않을 수 있다. 또한 RNA abundance만 사용하므로 chromatin accessibility 같은 upstream regulatory context를 직접 반영하지 못한다.
- 선행 접근 B: VeloAE, VeloVAE, VeloVI 같은 neural model은 latent space를 학습해 복잡한 structure를 잡으려 했고, cellDancer는 local relay velocity model을 통해 latent time 없이 local neighbor transition에 맞춰 velocity를 추정했다.
- B의 한계: neural model은 global temporal ordering이나 synchronous transcription/splicing assumption에 의존하는 경우가 많고, cellDancer는 transcriptome-only라 epigenomic regulation을 넣지 못한다.
- 선행 접근 C: MultiVelo는 chromatin accessibility를 ODE model에 넣어 epigenome-transcriptome interaction을 모델링했다.
- C의 한계: MultiVelo는 fixed gene classification과 shared kinetic regime에 의존한다. 따라서 branching trajectory, asynchronous transcriptional kinetics, cell-specific chromatin-transcription regulation을 유연하게 잡기 어렵다.
- 이 논문으로 이어지는 gap: multi-omic data에서 chromatin accessibility와 RNA를 함께 측정할 수 있지만, latent time이나 fixed gene label 없이 single-cell resolution에서 kinetic parameter를 추정하고 local regulatory dynamics를 잡는 velocity model이 필요했다.

#### 기본 개념
- RNA velocity: unspliced pre-mRNA와 spliced mature mRNA의 상대량으로 cell의 미래 RNA state를 예측하는 방법이다. 이 논문에서는 `u`와 `s` velocity뿐 아니라 chromatin accessibility `c` velocity까지 함께 본다.
- chromatin accessibility: promoter/enhancer 주변 chromatin이 열려 transcription machinery가 접근 가능한 정도다. MoFlow에서는 chromatin opening/closing을 `dc/dt = alpha_c * (k - c)`로 모델링한다.
- relay velocity: 실제 time-series가 없을 때 expression space의 local neighbor를 짧은 시간 뒤의 가능한 future state로 보고, predicted velocity vector가 neighbor displacement와 잘 맞도록 학습하는 방식이다.
- local adaptive kinetics: 하나의 global latent time이나 gene class에 맞추는 대신, 각 cell의 `(c, u, s)` 상태에서 cell-specific kinetic parameter를 추정하는 관점이다.
- asynchronous regulation: chromatin accessibility 변화와 RNA production/repression이 동시에 일어나지 않는 현상이다. 이 논문은 negative `c-s` lag처럼 RNA change가 chromatin change보다 먼저 보이는 경우도 중요하게 해석한다.

#### 이 논문이 필요성
- 핵심 이유: 기존 RNA velocity는 RNA-only 또는 fixed kinetic assumption에 묶여 있어, branching tissue development에서 local regulatory dynamics와 chromatin-dependent/independent transcription을 분리하기 어렵다.
- 기존 방법으로 부족했던 지점: MultiVelo는 chromatin을 통합하지만 gene-specific latent time과 fixed model class를 사용하고, cellDancer는 local relay를 사용하지만 chromatin을 쓰지 않는다.
- 이 논문이 해결하려는 방향: MoFlow는 deep neural network로 cell-specific `alpha_c`, `alpha`, `beta`, `gamma`를 추정하고, local neighbor relay loss로 velocity를 학습하며, chromatin opening/closing scenario 중 낮은 angular error를 선택해 flexible chromatin-aware velocity를 만든다.

### Overview
- Figure 1 포함 여부: 포함됨 - Figure 1은 MoFlow의 ODE 개념, DNN architecture, local relay neighbor selection, chromatin opening/closing 비교 loss, downstream velocity/pseudotime/gene-level analysis를 모두 보여주는 전체 방법 개요다.

#### 핵심 개념
- 개념: cell fate velocity는 RNA abundance만의 문제가 아니라 chromatin accessibility `c`, unspliced RNA `u`, spliced RNA `s`가 local cell-state context 안에서 함께 움직이는 문제라는 관점이다.
- 이 개념이 필요한 이유: transcription rate는 chromatin state에 영향을 받지만, 실제 cell에서는 chromatin remodeling과 RNA induction/repression이 비동기적으로 일어나고 lineage branch마다 kinetic program이 달라질 수 있다.

#### Method 관점
- 논문이 이 개념을 바라본 방식: MoFlow는 chromatin opening/closing, transcription, splicing, degradation 또는 nuclear export를 cell-specific kinetic parameter로 표현하는 deep relay velocity model이다.
- 입력: 각 cell과 gene의 chromatin accessibility `c_i`, unspliced RNA `u_i`, spliced RNA `s_i`.
- 처리 과정: DNN이 `(c, u, s)`에서 `alpha_c`, `alpha`, `beta`, `gamma`를 예측한다. RNA velocity vector로 future neighbor 후보를 고르고, predicted velocity와 neighbor displacement의 cosine distance를 줄인다. chromatin state는 opening(`k=1`)과 closing(`k=0`)을 모두 평가한 뒤 더 낮은 loss를 선택한다.
- 출력: chromatin/unspliced/spliced velocity, velocity pseudotime, gene-level kinetic parameter, RNA-on/RNA-off score, m1/m2 score, DTW 기반 `c-s` 및 `u-s` time lag.

#### 이 관점으로 알 수 있는 것
- 알 수 있게 된 점 1: global latent time 없이도 local neighbor transition을 이용해 branching trajectory에서 biologically plausible direction을 추정할 수 있다.
- 알 수 있게 된 점 2: MultiVelo의 model 1/model 2 같은 discrete repression class를 MoFlow의 continuous m1/m2 score와 RNA-on/off score로 재해석할 수 있다.
- 알 수 있게 된 점 3: transcription rate `alpha`와 chromatin accessibility `c`를 분리해, chromatin-independent transcriptional boost나 RNA export/half-life와 관련된 negative `c-s` lag를 분석할 수 있다.

#### 기대 효과
- 성능 또는 분석상 기대 효과: scVelo, cellDancer, MultiVelo보다 developmental trajectory direction과 cross-boundary transition coherence를 개선하고, cell-type-specific regulatory program을 더 세밀하게 해석할 수 있다.
- benchmark / baseline 관련 근거: developing human brain cortex에서 CBDir은 MoFlow 0.362, MultiVelo 0.211, scVelo 0.211, cellDancer -0.015였다. E18 mouse brain과 human HSPC에서도 MoFlow가 가장 높은 CBDir을 보였다고 보고했다.
- 적용 가능한 상황: RNA와 ATAC을 함께 측정한 10x Multiome 또는 SHARE-seq dataset, 특히 brain, skin, blood처럼 branch가 많고 asynchronous regulation이 예상되는 developmental system.

### Figure / Table Analysis

#### Figure 1
- 이 Figure가 필요한 이유: MoFlow가 RNA-only relay velocity를 chromatin-aware relay velocity로 확장하는 방식을 정의하기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MoFlow는 fixed latent time이나 fixed gene class 없이 single-cell resolution에서 chromatin/RNA kinetic parameter를 추정할 수 있다.

##### 패널별 설명
- a: chromatin opening/closing, transcription, splicing, degradation 또는 nuclear export를 연결하는 conceptual ODE model을 보여준다.
- b: DNN이 cell별 `(c_i, u_i, s_i)`를 입력받아 `alpha_ci`, `alpha_i`, `beta_i`, `gamma_i`를 예측하고, RNA velocity 기반 future neighbor와 opening/closing loss를 비교하는 architecture를 보여준다.
- c: MoFlow output이 AnnData/scVelo workflow와 연결되어 velocity embedding, velocity pseudotime, gene-level dynamics, repression mode inference에 사용될 수 있음을 보여준다.

##### 본문에서 강조한 비교
- 비교 대상: traditional RNA velocity와 MoFlow, global latent time alignment와 local relay alignment.
- 관찰된 차이: MoFlow는 chromatin opening/closing assumption을 모두 평가하고 낮은 angular error scenario를 선택한다.
- 이 차이가 의미하는 것: chromatin state를 미리 label로 고정하지 않고, local context에 맞는 chromatin-aware velocity를 학습할 수 있다.

##### 해석 시 주의점
- 주의점: Figure 1은 model design과 workflow의 설명이다. 실제 trajectory accuracy와 biological interpretation은 이후 dataset 결과로 검증된다.

#### Figure 2
- 이 Figure가 필요한 이유: developing human brain cortex에서 MoFlow가 known developmental hierarchy를 더 정확히 복원하고, MultiVelo의 model 1/model 2 regulatory logic을 continuous score로 재현함을 보이기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MoFlow는 biologically implausible backflow를 줄이고, transcriptional repression mechanism을 latent time 없이도 해석할 수 있다.

##### 패널별 설명
- a: MoFlow, scVelo, cellDancer, MultiVelo velocity stream을 같은 UMAP에서 비교한다. MoFlow는 Cyc. Prog.에서 RG, neuronal state로 이어지는 hierarchy를 더 자연스럽게 복원한다.
- b: MoFlow pseudotime이 coherent developmental gradient를 이룬다.
- c: G2/M score가 early Cyc. Prog. cell에서 높아 MoFlow pseudotime의 root assignment를 보조한다.
- d: cross-boundary direction correctness를 비교한다. MoFlow가 가장 높다.
- e: MKI67, SDK2의 gene-wise velocity pattern을 비교한다. MoFlow는 marker gene의 known direction과 맞는 dynamics를 보인다.
- f, g: MoFlow m1/m2 score가 MultiVelo model 1/model 2 gene classification과 유의하게 맞는다.
- h, i: MoFlow RNA-on/RNA-off score가 MultiVelo의 on/off/complete state assignment와 대응한다.
- j: model 2 gene에서 RNA-off score가 높아 transcriptional shutdown과 연결된다.

##### 본문에서 강조한 비교
- 비교 대상: MoFlow vs scVelo/cellDancer/MultiVelo, MoFlow continuous score vs MultiVelo discrete model.
- 관찰된 차이: 842 genes, 4693 cells에서 MoFlow CBDir 0.362로 MultiVelo 0.211, scVelo 0.211, cellDancer -0.015보다 높았다. model 2 gene은 Cyc. Prog.에서 높고 RG로 갈수록 downregulated되는 mitosis-related pattern과 맞았다.
- 이 차이가 의미하는 것: MoFlow는 trajectory direction뿐 아니라 repression timing도 fixed switching time 없이 해석할 수 있다.

##### 해석 시 주의점
- 주의점: m1/m2 score는 MultiVelo class와의 consistency를 보여주지만, model 1/2 mechanism의 causal validation은 아니다.

#### Figure 3
- 이 Figure가 필요한 이유: MoFlow가 OPC lineage에서 transcriptional decoupling과 negative `c-s` lag를 실제 biological region과 연결할 수 있음을 보이기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: global time 위에서는 RNA와 chromatin의 순서가 canonical `c -> u -> s`를 따르지 않는 gene이 존재하고, 이는 모델 artifact가 아니라 OPC 관련 regulation일 수 있다.

##### 패널별 설명
- a: MoFlow pseudotime을 따라 gene을 7개 transcriptional velocity cluster로 나눈다.
- b: cluster별 m2 score와 RNA-off score를 보여준다. cluster 0-1은 mitosis/cell proliferation과 관련되고 RNA-off 또는 m2 score가 높다.
- c: cell별 RNA velocity state를 both-on, both-off, decoupling-sOff, decoupling-uOff로 나누며 mGPC/OPC에서 decoupling-sOff가 두드러진다.
- d: PDGFRA와 MAP3K1 gene-wise velocity stream에서 OPC 부근 decoupling-sOff dynamics를 보여준다.
- e: DTW로 positive/negative time lag를 해석하는 scheme을 제시한다.
- f: MoFlow pseudotime과 MultiVelo global latent time에서는 PDGFRA/MAP3K1의 negative `c-s` lag가 보인다.
- g: MultiVelo gene-specific latent time에서는 같은 negative lag가 사라지고 canonical order로 정렬된다.
- h: Allen Brain Atlas adult scRNA-seq projection에서 OPC-aligned cell이 decoupling-sOff region에 위치한다.

##### 본문에서 강조한 비교
- 비교 대상: MoFlow global pseudotime / MultiVelo global latent time vs MultiVelo gene-specific latent time.
- 관찰된 차이: 400개 초과 gene이 최소 25% time bin에서 lag sign reversal을 보였고, 129개 gene은 75% 초과 bin에서 consistent reversal을 보였다. decoupling-sOff region의 mGPC/OPC cell 중 63%가 OPC로 embedding되었고, complementary region에서는 20%만 OPC였다.
- 이 차이가 의미하는 것: gene-specific latent time fitting은 expected biological order에 맞추기 위해 non-canonical lag를 over-correction할 수 있으며, MoFlow는 global local-transition 기반으로 asynchronous regulation을 남겨둔다.

##### 해석 시 주의점
- 주의점: negative `c-s` lag는 RNA가 chromatin보다 먼저 보인다는 temporal association이다. 직접적 causal mechanism은 추가 실험이 필요하다.

#### Figure 4
- 이 Figure가 필요한 이유: SHARE-seq mouse skin에서 MoFlow가 hair follicle differentiation 방향과 transcriptional boost를 잡는지 검증하기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MoFlow는 chromatin accessibility와 transcription rate를 함께 보면서 lineage-specific transcriptional boost를 cellDancer, scVelo, MultiVelo보다 잘 복원한다.

##### 패널별 설명
- a: MoFlow, scVelo, cellDancer, MultiVelo velocity stream을 비교한다. MoFlow는 TAC-1/TAC-2에서 IRS, medulla, hair shaft-cuticle cortex로 가는 흐름을 포착한다.
- b, c: G2/M score가 TAC-1에서 높아 MoFlow가 actively cycling progenitor를 root-like state로 잡는 것을 보조한다.
- d: MoFlow의 RNA-on, RNA-off, m1, m2 score 분포를 요약한다.
- e: MultiVelo gene class 비율을 보여주며 induction-only 66.6%, model 1 32.4%, model 2 1.0%로 induction-dominant pattern을 보인다.
- f: MoFlow m1/m2 score가 MultiVelo model 1/model 2 class와 유의하게 맞는다.
- g: Hephl1에서 MoFlow가 transcriptional boost trajectory와 transcriptional activity를 더 잘 잡는 사례를 보여준다.

##### 본문에서 강조한 비교
- 비교 대상: MoFlow vs cellDancer/MultiVelo/scVelo, RNA-on/off 및 m1/m2 score vs MultiVelo class.
- 관찰된 차이: MoFlow는 TAC에서 terminal hair follicle lineage로 이어지는 known flow를 재구성했고, Hephl1의 trajectory에서 cellDancer보다 나은 reconstruction을 보였다.
- 이 차이가 의미하는 것: transcriptional boost는 chromatin accessibility만으로 설명되지 않을 수 있으며, MoFlow의 cell-specific `alpha` 추정이 유리하다.

##### 해석 시 주의점
- 주의점: MURK/transcriptional boost gene은 skin에서 체계적으로 연구된 바가 제한적이므로, functional interpretation은 gene-level validation이 필요하다.

#### Figure 5
- 이 Figure가 필요한 이유: transcription rate `alpha`와 chromatin accessibility `c`를 분리하면 chromatin-dependent/independent regulatory strategy를 구분할 수 있음을 보이기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MoFlow는 low chromatin variability but high transcription rate variability gene, 즉 LCHA gene의 cell-cycle-linked transcriptional flexibility를 포착한다.

##### 패널별 설명
- a: chromatin accessibility `c`와 transcription rate `alpha`의 cell-type average variability를 DAC score로 계산해 HCHA, HCLA, LCHA, LCLA 네 그룹으로 나눈다.
- b: LCHA gene은 chromosome segregation, cell division, mitotic spindle organization 등 mitotic regulation에 enriched된다.
- c: LCHA gene expression은 G2/M score와 가장 강한 association을 보이고, LCLA는 가장 약하다.
- d: Padi3, Myo10, Notch1, Trps1, Wnt3의 gene-wise velocity stream을 보여주며 MoFlow가 각 gene의 known direction을 잡는다.
- e: 각 representative gene에서 `c`와 `alpha`의 cell-type-specific distribution을 비교한다.

##### 본문에서 강조한 비교
- 비교 대상: HCHA/HCLA/LCHA/LCLA gene group, MoFlow vs MultiVelo/cellDancer/scVelo gene-wise prediction.
- 관찰된 차이: Padi3와 Myo10은 low chromatin accessibility region에서도 MoFlow가 medulla/IRS 방향을 맞췄고, MultiVelo는 `alpha` variability 제한 때문에 실패했다. Notch1은 MoFlow만 정확히 모델링했고, Wnt3와 Trps1은 MoFlow와 MultiVelo가 모두 잘 잡았다.
- 이 차이가 의미하는 것: accurate RNA velocity는 chromatin-level modulation뿐 아니라 transcription rate 자체의 cell-specific variability를 분리해야 한다.

##### 해석 시 주의점
- 주의점: DAC threshold 0.05 기반 grouping은 downstream interpretation을 쉽게 하지만, threshold sensitivity나 pathway-level coordination은 추가 점검이 필요하다.

#### Figure 6
- 이 Figure가 필요한 이유: E18 mouse brain에서 MoFlow가 brain development trajectory와 radial glia 주변 transcriptional heterogeneity를 얼마나 잘 잡는지 검증하기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: MoFlow는 기존 velocity model의 backflow를 줄이고, early progenitor의 DNA damage response 및 cell-cycle-linked transcriptional program을 더 잘 해석한다.

##### 패널별 설명
- a: MoFlow, scVelo, cellDancer, MultiVelo velocity stream을 E18 mouse brain UMAP에서 비교한다. MoFlow는 Cyc. Prog. -> RG -> IPC -> ExM/SP -> UL/DL 흐름을 포착한다.
- b: MoFlow pseudotime이 neurodevelopment progression을 나타낸다.
- c: G2/M score가 early pseudotime region과 맞아 proliferative root assignment를 보조한다.
- d: CBDir 비교에서 MoFlow가 lineage coherence를 더 높게 보인다.
- e: pseudotime-aligned 12개 gene expression cluster를 보여준다.
- f: cluster별 functional annotation이 cell cycle/DNA repair에서 neural/synaptic function으로 이어지는 progression을 보인다.
- g: cluster 0 gene의 `alpha` DAC 기반 GSEA에서 DNA damage response, DNA repair, mitotic regulation이 early progenitor state와 연결된다.

##### 본문에서 강조한 비교
- 비교 대상: MoFlow vs scVelo/cellDancer/MultiVelo, transcription rate `alpha` DAC vs chromatin accessibility `c` DAC.
- 관찰된 차이: scVelo, MultiVelo, cellDancer는 IPC에서 RG 또는 Cyc. Prog.로 가는 implausible backflow를 보였지만, MoFlow는 expected forward transition을 보였다. cluster 0에서는 `alpha` DAC가 DNA repair/metabolism에 더 구체적으로 enriched되었고 `c` DAC는 약했다.
- 이 차이가 의미하는 것: 일부 early stress-response program은 chromatin remodeling보다 transcriptional burst가 더 중요한 driver일 수 있다.

##### 해석 시 주의점
- 주의점: DNA damage response는 Supplementary figure와 GSEA를 통해 보강되지만, 직접 perturbation이나 protein-level validation은 제시되지 않는다.

#### Figure 7
- 이 Figure가 필요한 이유: negative `c-s` lag가 단순 오류가 아니라 RNA half-life, nuclear export, subnuclear localization과 연결될 수 있음을 보여주기 위해 필요하다.
- 이 Figure가 뒷받침하는 주장: chromatin accessibility와 spliced RNA 사이의 time lag는 RNA kinetics에 의해 shape될 수 있고, RNA가 chromatin opening보다 먼저 보이는 non-canonical pattern도 biological signal일 수 있다.

##### 패널별 설명
- a: 12개 gene cluster별 평균 chromatin accessibility `c`와 spliced RNA `s` profile을 pseudotime 위에 그린다.
- b: DTW로 추정한 `c-s` lag quantile을 보여주며 median time lag가 대부분 negative임을 제시한다.
- c: cluster별 negative `c-s` lag gene 비율을 보여준다. clusters 0-3과 10에서 높다.
- d: Ccnd2, Mki67은 `s`가 chromatin closure보다 먼저 decay하는 예이고, Cdk12, Esf1은 `s` accumulation이 chromatin opening보다 먼저 나타나는 예다.
- e, f: NIH3T3 RNA half-life 자료와 비교해 cluster 0, 3, 10은 short nuclear half-life와 fast export, cluster 1, 2는 prolonged nuclear retention을 보인다.
- g: polycomb/speckle-associated gene enrichment를 보여주며 cluster 10이 nuclear compartment 관련 gene과 유의하게 겹친다.

##### 본문에서 강조한 비교
- 비교 대상: lag-enriched cluster 0-3/10 vs other clusters, RNA half-life signature별 cluster.
- 관찰된 차이: cluster 0-3은 model 2-like shutdown, 즉 RNA decay/export가 chromatin closure보다 빠른 pattern으로 해석된다. cluster 10은 `s`가 `c`보다 먼저 rise하며, transcription/translation/stimulus response와 nuclear compartment RNA overlap이 관찰된다.
- 이 차이가 의미하는 것: negative `c-s` lag는 delayed chromatin inactivation, rapid RNA turnover/export, stimulus-responsive nuclear release 같은 mechanism 후보로 나뉠 수 있다.

##### 해석 시 주의점
- 주의점: half-life 자료는 NIH3T3 cell에서 온 외부 데이터이고, brain development cluster에 직접 측정된 값이 아니다. 10x Multiome은 nuclear RNA를 측정하므로 degradation처럼 보이는 현상은 nuclear export일 수 있다.

### Results

#### Dataset별 결과

##### Developing human brain cortex 10x Multiome
- Dataset: developing human brain cortex 10x Multiome, Trevino et al. dataset.
- 목적: MoFlow가 human cortical development trajectory와 transcriptional repression mechanism을 복원하는지 검증.
- 사용한 데이터 규모: 4693 cells, 842 genes.
- Baseline / 비교 대상: scVelo, cellDancer, MultiVelo, known brain developmental hierarchy, MultiVelo model 1/model 2 classification.
- Metric / 평가 기준: velocity stream biological plausibility, velocity pseudotime, G2/M score alignment, CBDir, m1/m2/RNA-on/RNA-off score consistency.
- 주요 수치: CBDir은 MoFlow 0.362, MultiVelo 0.211, scVelo 0.211, cellDancer -0.015. Figure 2의 m1/m2/RNA-on/RNA-off 비교에서 주요 class 차이는 `p < 0.001`로 표시됨.
- 정성 결과: MoFlow는 Cyc. Prog.에서 RG 및 neuronal lineage로 이어지는 방향을 복원했고, scVelo/cellDancer는 neuronal IPC/GluN1에서 Cyc. Prog. 또는 RG로 돌아가는 backflow를 보였다. MultiVelo는 GluN3 -> GluN2 -> GluN4/5 같은 과도하게 linear한 dependency를 만들었다.
- 논문 주장과의 연결: local relay와 chromatin-aware kinetic parameter 추정이 fixed latent time/gene class보다 branching neurodevelopment trajectory에 잘 맞는다는 핵심 결과다.

##### Human OPC lineage analysis
- Dataset: developing human brain cortex dataset의 mGPC/OPC lineage 및 Allen Brain Atlas adult scRNA-seq projection.
- 목적: asynchronous transcriptional regulation과 negative `c-s` lag가 biological OPC context와 연결되는지 확인.
- 사용한 데이터 규모: gene cluster는 7개로 분류. lag sign reversal은 400개 초과 gene에서 25% 이상 bin, 129개 gene에서 75% 초과 bin.
- Baseline / 비교 대상: MoFlow pseudotime, MultiVelo global latent time, MultiVelo gene-specific latent time, Allen Brain Atlas adult scRNA-seq annotation.
- Metric / 평가 기준: DTW `c-s` lag sign, RNA velocity state composition, OPC projection proportion.
- 주요 수치: decoupling-sOff region의 mGPC/OPC cell 중 63%가 OPC로 embedding되었고, complementary region에서는 20%만 OPC였다.
- 정성 결과: PDGFRA와 MAP3K1은 unspliced RNA production이 유지되는 동시에 spliced RNA가 감소하는 decoupling-sOff pattern을 보였다. MultiVelo gene-specific latent time에서는 negative lag가 사라져 canonical order로 보정되는 경향이 있었다.
- 논문 주장과의 연결: MoFlow는 biological order에 맞춘 gene-specific time fitting이 숨길 수 있는 non-canonical regulatory lag를 유지하고 해석할 수 있다.

##### SHARE-seq mouse skin / hair follicle differentiation
- Dataset: SHARE-seq mouse skin hair follicle differentiation.
- 목적: TAC에서 IRS, medulla, hair shaft-cuticle cortex로 이어지는 lineage flow와 transcriptional boost gene을 포착하는지 평가.
- 사용한 데이터 규모: Figure 4에서는 MultiVelo class 비율로 induction-only 66.6%, model 1 32.4%, model 2 1.0%가 제시됨.
- Baseline / 비교 대상: scVelo, cellDancer, MultiVelo, known hair follicle differentiation direction, MultiVelo gene class.
- Metric / 평가 기준: velocity stream consistency, G2/M root-state alignment, RNA-on/off score, m1/m2 score, gene-wise velocity for Hephl1.
- 주요 수치: TAC-1이 가장 높은 G2/M score를 보였고, m1/m2 score class 차이는 `p < 0.001`로 표시됨.
- 정성 결과: MoFlow는 TAC-1/TAC-2에서 terminal lineage로 가는 흐름을 복원했고, Hephl1 transcriptional boost를 cellDancer보다 잘 재구성했다.
- 논문 주장과의 연결: MoFlow는 chromatin accessibility와 transcription rate를 동시에 쓰기 때문에 MURK/transcriptional boost gene을 더 세밀하게 볼 수 있다.

##### Mouse skin DAC gene group analysis
- Dataset: SHARE-seq mouse skin에서 MoFlow가 추정한 cell-type-specific `alpha`와 `c`.
- 목적: transcription rate variability와 chromatin accessibility variability를 분리해 gene regulatory strategy를 해석.
- 사용한 데이터 규모: DAC threshold 0.05로 HCHA, HCLA, LCHA, LCLA 네 그룹을 정의.
- Baseline / 비교 대상: gene group별 GO enrichment, G2/M association, MoFlow vs MultiVelo/cellDancer/scVelo representative gene velocity.
- Metric / 평가 기준: DAVID BP ontology enrichment, Mann-Whitney U test, gene-wise velocity plausibility.
- 주요 수치: Figure 5의 group comparison은 significance marker 중심으로 제시되며 정확한 effect size는 본문에 제공되지 않음.
- 정성 결과: LCHA gene은 chromosome segregation, cell division, mitotic spindle organization에 enriched되고 G2/M score와 강하게 연결되었다. Padi3, Myo10은 low chromatin accessibility에도 transcription rate 변화로 lineage direction을 설명했다.
- 논문 주장과의 연결: chromatin state와 transcription rate를 분리해야 chromatin-independent transcriptional flexibility를 설명할 수 있다.

##### E18 mouse brain 10x Multiome
- Dataset: embryonic day 18 mouse brain 10x Multiome.
- 목적: mouse neurodevelopment에서 trajectory, radial glia heterogeneity, DNA damage response transcriptional program을 평가.
- 사용한 데이터 규모: gene expression cluster는 12개로 분류.
- Baseline / 비교 대상: scVelo, cellDancer, MultiVelo, known mouse brain developmental trajectory, G2/M score, CBDir.
- Metric / 평가 기준: velocity stream plausibility, pseudotime-cell cycle alignment, CBDir, cluster GO enrichment, DAC `alpha` GSEA.
- 주요 수치: CBDir에서 MoFlow가 가장 높다고 보고했으나 본문 발췌에서는 정확한 값이 Figure와 Supplementary Table에 의존한다. cluster 0은 DNA repair, mitosis, DNA damage response 관련 enrichment를 보였다.
- 정성 결과: MoFlow는 Cyc. Prog. -> RG -> IPC -> ExM/SP -> UL/DL 방향을 포착했고, scVelo/MultiVelo/cellDancer는 IPC에서 RG 또는 Cyc. Prog.로 돌아가는 backflow를 보였다.
- 논문 주장과의 연결: MoFlow는 early progenitor에서 chromatin remodeling보다 transcriptional burst가 더 중요한 stress-response program을 잡을 수 있다.

##### Time lag / RNA kinetics analysis in mouse brain
- Dataset: E18 mouse brain gene clusters와 외부 NIH3T3 RNA half-life dataset, polycomb/speckle RNA gene set.
- 목적: negative `c-s` lag의 mechanism 후보를 RNA half-life, nuclear export, subnuclear localization 관점에서 해석.
- 사용한 데이터 규모: 12개 cluster 중 clusters 0-3과 10에서 negative `c-s` lag 비율이 높음.
- Baseline / 비교 대상: lag-enriched clusters vs other clusters, NIH3T3 nuclear/cytoplasmic/export/degradation half-life distribution, polycomb/speckle gene overlap.
- Metric / 평가 기준: DTW `c-s` lag, one-sided KS test, Fisher's exact test.
- 주요 수치: Figure 7은 `p < 0.001`, `p < 0.005`, `p < 0.05` marker를 제공하지만, 본문에는 각 cluster별 exact p-value가 제시되지 않음.
- 정성 결과: clusters 0, 3, 10은 short nuclear half-life와 fast export, clusters 1, 2는 long nuclear half-life와 slow export를 보였다. cluster 10은 polycomb/speckle-associated gene과 유의하게 overlap했다.
- 논문 주장과의 연결: chromatin-RNA lag는 chromatin timing만이 아니라 RNA export/degradation/retention kinetics에 의해 만들어질 수 있다.

##### Human HSPC 10x Multiome
- Dataset: human hematopoietic stem and progenitor cell 10x Multiome.
- 목적: blood differentiation에서 MoFlow가 expected hematopoietic hierarchy와 branching lineage를 복원하는지 확인.
- 사용한 데이터 규모: 본문에 cell/gene 수는 명시되지 않음.
- Baseline / 비교 대상: scVelo, cellDancer, MultiVelo, known HSC/MPP -> erythroid/myeloid/lymphoid/megakaryocyte lineage.
- Metric / 평가 기준: velocity stream plausibility, CBDir across annotated lineage boundaries.
- 주요 수치: MoFlow가 tested methods 중 가장 높은 CBDir을 보였다고 보고하나, 본문에는 exact value가 제공되지 않고 Supplementary Table 1에 의존한다.
- 정성 결과: MoFlow는 erythroid, myeloid, lymphoid, megakaryocyte/platelet branch가 HSC/MPP에서 갈라지는 pattern을 대체로 복원했다. scVelo와 cellDancer는 downstream progenitor에서 HSC로 돌아가는 spurious backflow를 보였고, MultiVelo는 overly linear flow로 natural branching을 흐렸다.
- 논문 주장과의 연결: MoFlow의 local relay model은 hematopoiesis처럼 branch가 많은 system에서도 biologically meaningful transition direction을 잡는 데 유리하다.

#### 전체 결과 요약
- 반복적으로 관찰된 패턴: MoFlow는 brain, skin, blood dataset에서 scVelo/cellDancer/MultiVelo보다 backflow를 줄이고 known developmental direction과 더 잘 맞는 velocity stream을 보였다.
- 가장 중요한 수치: human brain cortex CBDir은 MoFlow 0.362, MultiVelo 0.211, scVelo 0.211, cellDancer -0.015. Human brain analysis는 4693 cells와 842 genes 기준. OPC lag reversal은 400개 초과 gene에서 25% 이상 bin, 129개 gene에서 75% 초과 bin. decoupling-sOff region의 OPC projection은 63% vs 20%.
- baseline 대비 차이: scVelo/cellDancer는 RNA-only라 chromatin context를 놓치고, MultiVelo는 chromatin을 쓰지만 fixed gene class/latent time에 의해 overly linear trajectory 또는 over-corrected temporal order를 만들 수 있다. MoFlow는 local relay와 cell-specific kinetic parameter로 이 둘의 약점을 줄이려 한다.
- 결과 해석 시 주의점: 많은 결과가 UMAP velocity embedding과 biological plausibility에 의존한다. CBDir은 known transition annotation이 필요하고, velocity vector를 low-dimensional embedding에 project하는 과정 자체가 distortion을 만들 수 있다.

### Limitations

#### 저자가 명시한 한계
- 한계 1: MoFlow는 long-range enhancer-promoter interaction을 명시적으로 모델링하지 않는다.
- 한계 2: transcriptional memory나 motif-level regulation을 account하지 않는다.
- 한계 3: inference가 gene-wise로 수행되어 coordinated pathway-level program detection에는 제한이 있을 수 있다.
- 한계 4: future extension으로 spatial context 또는 protein-level modality를 통합하면 regulatory resolution을 높일 수 있다고 제시했다.
- 한계 5: velocity field는 UMAP 같은 fixed low-dimensional embedding에 투영되므로, embedding distortion 때문에 vector visualization 해석에 주의가 필요하다고 직접 언급했다.

#### 분석자가 판단한 한계
- 부족한 점: benchmark가 일부 dataset에서 CBDir과 stream plot 중심이며, exact numerical metric이 모든 dataset에 동일하게 제공되지는 않는다.
- 왜 중요한가: “outperform” 주장은 강하지만, dataset마다 baseline failure mode와 평가 metric이 다르면 method 간 비교의 객관성이 약해질 수 있다.
- 어떤 증거가 부족한가: 동일 preprocessing, 동일 gene selection, 동일 annotated boundary에서 scVelo/cellDancer/MultiVelo/MoFlow의 full metric table과 uncertainty가 필요하다.

- 부족한 점: MoFlow의 chromatin opening/closing scenario 선택은 lower angular error에 기반하므로, biological chromatin state의 direct observation과 동일하다고 볼 수 없다.
- 왜 중요한가: model이 선택한 `k` state가 실제 chromatin remodeling event를 의미하는지 검증되어야 mechanistic interpretation이 강해진다.
- 어떤 증거가 부족한가: time-resolved chromatin data, perturbation, TF binding 또는 chromatin remodeler activity validation이 필요하다.

- 부족한 점: negative `c-s` lag의 RNA half-life 해석은 외부 NIH3T3 half-life dataset에 의존한다.
- 왜 중요한가: brain development와 fibroblast-like cell line의 RNA kinetics가 다를 수 있고, 10x Multiome은 nuclear RNA 중심이라 degradation과 export를 구분하기 어렵다.
- 어떤 증거가 부족한가: 동일 tissue/cell type에서 nuclear/cytoplasmic RNA fraction, nascent RNA, RNA export rate를 직접 측정한 validation이 필요하다.

#### 설명이 매끄럽지 않은 지점
- 연결이 약한 주장: chromatin-independent transcriptional boost가 MoFlow의 `alpha` variability로 설명된다는 해석.
- 현재 논문에서 제시한 근거: Hephl1, Padi3, Myo10, Notch1 같은 gene-wise trajectory와 DAC group enrichment.
- 더 필요해 보이는 근거: transcription factor activity, enhancer activity, promoter-proximal pausing, protein-level readout과의 연결.

- 연결이 약한 주장: DNA damage response gene의 elevated `alpha`가 RG lineage commitment와 관련된 protective mechanism이라는 해석.
- 현재 논문에서 제시한 근거: cluster 0 DAC `alpha` GSEA와 known neural progenitor DDR literature.
- 더 필요해 보이는 근거: DDR perturbation, DNA damage marker staining, cell-cycle phase control 후 velocity change 분석.

#### 정리되지 않은 질문
- 질문 1: MoFlow의 local neighbor 선택이 rare branch 또는 sparse cell state에서 얼마나 안정적인가?
- 질문 2: gene-wise inference를 pathway-level coupled dynamics로 확장하면 m1/m2, RNA-on/off score의 해석이 어떻게 바뀌는가?
- 질문 3: negative `c-s` lag가 실제 RNA export인지, nuclear RNA capture bias인지, normalization artifact인지 어떻게 분리할 수 있는가?
- 질문 4: enhancer-promoter interaction과 motif activity를 넣으면 chromatin-independent로 보이는 `alpha` variability 중 어느 정도가 설명되는가?

## Final Takeaways
- 이 논문의 가장 큰 의미: MoFlow는 MultiVelo의 chromatin-aware ODE 관점과 cellDancer의 local relay velocity 관점을 결합해, fixed latent time/gene class 없이 cell-specific multi-omic kinetic parameter를 추정하는 framework를 제시했다.
- 다음 논문으로 이어질 아이디어: MoFlow velocity로 예측한 chromatin-independent transcriptional boost gene을 perturb-seq 또는 CRISPRi로 검증하고, `alpha` burst가 TF activity인지 RNA processing/export인지 분해한다.
- 설명을 더 매끄럽게 만들 방법: RNA velocity, chromatin accessibility, nascent RNA, nuclear/cytoplasmic RNA fraction을 같은 cell-state trajectory에 정렬해 `c -> transcription -> nuclear RNA -> cytoplasmic RNA` 순서를 직접 검증한다.
- 우선순위가 높은 후속 실험 / 분석: (1) 동일 dataset에서 unified CBDir/held-out transition benchmark, (2) UMAP embedding distortion을 줄인 high-dimensional velocity evaluation, (3) tissue-specific RNA half-life dataset과의 재분석, (4) enhancer-promoter/motif-level regulatory graph를 포함한 pathway-level MoFlow extension.
