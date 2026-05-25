# Lens — Academic — Li 2025 MultiVeloVAE

> Citation: `@li2025multivelovae`. 본 노트는 `li-2025-multivelovae_core.md` 작성 후 *학계 시선*만 따로 정리. 산업·규제·BD 관점은 `li-2025-multivelovae_lens-industry.md`로 분리. 본 paper는 `@li2023multivelo`(MultiVelo)의 직접 extension이므로 cross-reference 빈번.

---

## Limitations

### 저자가 명시한 한계

- **Mature cell type에서 velocity inference 신뢰도 저하** (Discussion p13-14): "MultiVeloVAE's inference outcome depends on the quality of unspliced and spliced RNA measurements, which can lead to difficulty in mature cell types with reduced differentiation potential, such as PBMCs." → mature 또는 quiescent cell 분석에는 부적합.
- **De novo training 의존** (Discussion p14): "current velocity inference methods, including deep-learning-based approaches, rely on de novo training. Recent efforts to integrate new data with atlas-level datasets have shown promise for cell-type annotation. Developing pre-trained and validated parameter sets for known cell types could benefit applications that require generic velocity inference on similar, low-quality samples." → 매 dataset마다 model 처음부터 학습 필요, atlas-level pre-training 부재.
- **CITE-seq 등 추가 modality 미지원** (Discussion p14): "In the future, it may be promising to extend the approach to additional types of single-cell data, such as CITE-seq." → 현재 protein modality 미통합.
- **Multi-sample 통합의 quality 의존성** (Discussion p13-14): "For effective integration across datasets, reliable velocity inference is needed for every dataset to ensure consistent results." → 한 sample이 noisy면 통합 전체 신뢰도 하락.
- **개별 cis-regulatory element 직접 modeling 부재** (§Results "MultiVeloVAE infers state-specific decoupling patterns" p9): "individual cis-regulatory elements can play important and diverse roles in regulating transcription kinetics. Although MultiVeloVAE does not directly model the effects of individual cis-regulatory elements, we can perform downstream analyses to investigate the influence of individual peaks." → enhancer별 distinct kinetics는 post hoc correlation으로만 접근.
- **ChromHMM-decoupling association 결과의 잠정성** (§Results p9): "Although more work is needed to investigate these connections, our results suggest that there are interesting histone mark differences among peaks that are related to decoupled vs. coupled states." → BivProm1, EnhWk4, HET4 등 association이 *exploratory*, mechanism 미확정.

### 분석자가 판단한 한계

- **부족한 점 1 — 정량 metric의 본문 노출 부족**:
  - **왜 중요한가**: 핵심 benchmark (Fig. 2f의 10 dataset RNA-only correlation/GCBDir/Mann–Whitney, Fig. 3g의 5 multi-omic dataset CBDir, Fig. 3h의 runtime, Fig. 4d-e의 scIB benchmark)가 모두 *box plot 시각화*만 본문에 수록. 정확 median, IQR, p-value of pairwise comparison 미보고. Source Data file에 의존.
  - **어떤 증거가 부족한가**: ① dataset × method × metric matrix table, ② pairwise Wilcoxon p-value (MultiVeloVAE vs each baseline), ③ effect size (Cohen's d or rank-biserial), ④ runtime의 정확 분 단위 (Fig. 3h n=5 box plot의 median + IQR), ⑤ scIB metric의 정확 score.

- **부족한 점 2 — Bayesian differential test의 false discovery control 검증 부재**:
  - **왜 중요한가**: Fig. 6b의 macrophage (n=850) vs DC (n=221) volcano plot에 "p-values were not adjusted for multiple testing, but all genes shown have been verified to have a False Discovery Rate < 0.05"라 명시 — 그러나 FDR 계산이 *posterior expected false discovery proportion* (Eq. 25)로 *self-evaluated*. *calibration* (예: known null gene set에서의 FDR 실측) 검증 없음.
  - **어떤 증거가 부족한가**: ① permutation null로 FDR calibration, ② simulation에서 known DE / non-DE gene 50:50 mix로 nominal vs realized FDR 비교, ③ 다른 cluster size ratio (예: 850 vs 50, 850 vs 5,000)에서 statistical power curve.

- **부족한 점 3 — In silico perturbation의 ground-truth 검증 부재**:
  - **왜 중요한가**: SPI1/GATA1 KO 결과를 *기존 method (Dynamo, CellOracle)와 consistent*하다고 결론. 그러나 세 method 모두 *같은 known biology* (mutual inhibition)에 의존 → consistency가 *novel prediction* 능력 검증은 아님. 더 *덜 알려진* TF (예: ZNF385D, ARID5B)에 대한 wet-lab Perturb-seq 검증 없음.
  - **어떤 증거가 부족한가**: ① 같은 dataset에서 *novel TF* (literature에서 effect direction 미확정인 것)의 perturbation force 예측 후 wet-lab Perturb-seq로 비교, ② KO simulation의 *quantitative magnitude* 검증 (전체 cell fate probability shift % 단위), ③ partial KO (50% expression) 시 model이 *linear gradient*로 반응하는지.

- **부족한 점 4 — Continuous (δ, κ) 결과를 MultiVelo discrete state와 직접 비교 부재**:
  - **왜 중요한가**: MultiVeloVAE가 MultiVelo의 discrete 4 state를 *continuous로 일반화*했다고 주장하지만, *같은 dataset에서 두 method의 state assignment overlap* (예: discrete decoupled state cell이 continuous δ < 0인 비율) 정량 부재. cell type-specific MultiVeloVAE 결과가 MultiVelo aggregate와 *얼마나 다른지* 정량 부재.
  - **어떤 증거가 부족한가**: ① MultiVelo 4 state vs MultiVeloVAE δ/κ threshold (e.g., |δ|>0.5) confusion matrix, ② gene별 priming/decoupling interval length가 두 method에서 어떻게 다른지, ③ cell-type-specific decoupling이 MultiVelo aggregate를 어떻게 *깨뜨리는지* 정량 (예: 같은 gene이 cell type A에서는 M1, cell type B에서는 M2).

- **부족한 점 5 — Cross-modality ATAC prediction이 ground-truth보다 GCBDir 높은 결과의 정합성 검증**:
  - **왜 중요한가**: Supplementary Fig. 19e에서 MultiVeloVAE 예측 ATAC이 *ground-truth ATAC baseline*보다 GCBDir이 높다는 결과. 이는 *noise denoising 효과* 또는 *evaluation cell selection bias* 가능. 그대로 받아들이면 "ground-truth ATAC을 무시하고 imputation 결과 쓰는 게 낫다"는 잘못된 결론으로 이어질 위험.
  - **어떤 증거가 부족한가**: ① ground-truth ATAC에 동일 smoothing (k-NN) 적용 후 비교, ② cell-별 ATAC 신호 강도와 GCBDir improvement의 상관, ③ ATAC raw vs MultiVeloVAE imputed의 distance to nearest cell type centroid 비교.

- **부족한 점 6 — Inter-donor / cross-cohort replication 부재**:
  - **왜 중요한가**: 신규 dataset (EB, HSPC, macrophage) 모두 *single donor* 또는 *limited replicate*. 두 HSPC sample은 다른 donor지만 *같은 protocol*. 진짜 cross-cohort (다른 institution의 같은 cell type)에서 reproducibility 미검증.
  - **어떤 증거가 부족한가**: ① 같은 cell type의 *external published* dataset에서 같은 gene의 priming/decoupling pattern reproduce 확인, ② δ, κ distribution의 inter-donor coefficient of variation 보고, ③ public consortium (예: Human Cell Atlas, ENCODE) HSPC와 비교.

- **부족한 점 7 — Hyperparameter sensitivity 분석 부재**:
  - **왜 중요한가**: cross-batch regularization weight λ (Eq. 8), BasisVAE cluster 수 K (default 7), encoder/decoder MLP layer (`미제공:`), learning rate schedule (cosine annealing), holdout validation split — 모두 sensitivity 분석 부재. MultiVeloVAE 결과가 *hyperparameter robust*한지 미검증.
  - **어떤 증거가 부족한가**: ① λ ∈ [0, 0.01, 0.1, 1.0] 비교, ② K=4 vs 7 vs 12 결과, ③ MLP depth 1-3 layer 비교, ④ learning rate 10⁻⁴~10⁻² range 비교.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장 1**: ChromHMM enrichment 결과 (§Results "MultiVeloVAE infers state-specific decoupling patterns" p9): "decoupling occurs when peaks in heterochromatin regions are first opened. Bivalent promoter (BivProm1) and weak enhancer (EnhWk4) associations may indicate that decoupling happens when cis-regulatory regions are being established by histone modification changes."
  - **현재 논문에서 제시한 근거**: Spearman correlation between peak accessibility and decoupling factor + ChromHMM state intersection.
  - **더 필요해 보이는 근거**: ① 위와 같은 mechanism (BivProm decoupling = cis-regulatory establishment)을 *temporal sequence*로 보여줄 longitudinal multi-omic data, ② BivProm peak이 *posterior에서 first opening*하는 cell이 *higher δ*를 갖는지 cell-level 검증, ③ 알려진 BivProm gene (예: HOX cluster) examples로 spot check.

- **연결이 약한 주장 2**: TF coupling factor positive correlation + decoupling factor negative correlation 해석 (§Results p9): "the coupling factors of cells subset to non-background lineages of a gene ... are positively associated with the regulatory effects of TFs. In contrast, the decoupling factor is, in general, inversely associated with the TF's RNA level."
  - **현재 논문에서 제시한 근거**: Fig. 5d Spearman correlation scatter.
  - **더 필요해 보이는 근거**: ① cell-cycle / proliferation marker TF가 outlier인지, ② Spearman 분포의 95% CI (단순 mean이 아닌), ③ negative regulation TF만 따로 분리한 sub-analysis (positive와 negative가 섞이면 직관 해석 어려움).

- **연결이 약한 주장 3**: BMMC sample의 shorter inferred temporal duration (§Results p13): "comparing chromatin dynamics across the three samples reveals that the bone marrow scRNA sample has a shorter inferred temporal duration than the two multi-omic HSPC datasets."
  - **현재 논문에서 제시한 근거**: Fig. 7d bottom UMAP의 latent time 색.
  - **더 필요해 보이는 근거**: ① BMMC vs in vitro HSPC의 *실제 differentiation rate* difference에 대한 외부 reference, ② 다른 BMMC scRNA dataset에서도 같은 *shorter duration*이 reproduce되는지, ③ 통합 model의 *latent time scale가 sample 간 commensurable*한지 (Eq. 7의 prior 공유로 가정되지만 검증 없음).

- **연결이 약한 주장 4**: SPI1/GATA1 in silico KO와 wet-lab biology의 alignment (§Results "MultiVeloVAE generates unobserved..." p13): "The KO of SPI1 reversed differentiation flows toward GMP-associated lineages, such as DCs ... These results are similar to those reported in the Dynamo paper."
  - **현재 논문에서 제시한 근거**: perturbation force UMAP + CellRank fate probability + CellOracle direction consistency.
  - **더 필요해 보이는 근거**: ① 같은 dataset의 *positive control* (well-characterized lineage marker KO)로 magnitude calibration, ② SPI1/GATA1 partial KO의 dose-response, ③ Dynamo / CellOracle와의 *quantitative agreement* (correlation of velocity change vectors).

### 정리되지 않은 질문

- **질문 1**: MultiVeloVAE의 `λ Σ (θ_b − θ_r)²` cross-batch regularization (Eq. 8)이 *sample composition이 매우 다른 case* (예: 정상 cell vs 질환 cell mixture)에서도 적절한가? 본문 dataset은 모두 *similar composition between batches* — completely *different cell type distribution* setting (case-control)에서 regularization이 *biology를 강제 동질화*하지 않는지 검증 부재.

- **질문 2**: BasisVAE의 7 cluster initialization (induction-only / repression-only / complete 조합)이 hyperparameter K로 *주어진 fixed* 값. 본문은 K=7을 default로만 명시 — *dataset complexity에 따라 K를 adaptive하게 선택*하는 방법 없는가? non-parametric Bayesian (Dirichlet process)이 더 자연스러울 수 있음.

- **질문 3**: in silico KO를 `c = u = s = 0`으로 zeroing — 이는 *gene expression이 모든 cell에서 영원히 0인 상태*를 simulate. 실제 KO는 *time-dependent decay* (mRNA half-life에 따른 점진적 감소) — 이를 반영한 perturbation simulation이 더 realistic하지 않은가? 본 paper의 simulation이 실험 결과와 quantitative agreement가 약한 것은 이 단순화 때문일 가능성.

- **질문 4**: Continuous (δ, κ)가 *single cell × single gene*마다 unique 값. 그러나 *cell의 stochastic state transition* (e.g., bursty transcription, Markov chromatin)을 직접 modeling하지는 않음. Stochastic ODE 변형 (`@li2023multivelo` Supplementary Fig. 2)이 본 MultiVeloVAE에는 부재 — VAE framework에서 stochastic 변형 자연스럽게 추가 가능한가?

- **질문 5**: MultiVeloVAE에서 `shared latent time t across all genes`을 강제. 그러나 cell이 *진짜로* 모든 gene에 대해 같은 시점에 있다는 가정은 *분화 system 외*에서 깨질 수 있음 (e.g., cell cycle 동안 일부 gene만 oscillating). cell cycle gene과 lineage gene이 *서로 다른 time scale*에 있는 system에 적용 시 결과가 어떻게 변하는가?

- **질문 6**: Differential dynamics test는 *Gaussian process regression with RBF kernel + LRT*. RBF는 *smooth time-varying*만 잡음 — *step function 형태* (예: cell type identity가 sudden switch하는 시점에 gene이 갑자기 on/off)는 정의상 detection 약함. Sudden switch driver gene 식별에는 다른 kernel (e.g., Matern, linear)이 더 적합하지 않은가?

- **질문 7**: 본 paper에서 발견된 "PROS1 chromatin early, velocity mid, spliced late" 시간 순서 (Fig. 6c)가 *MultiVelo의 priming + coupled induction sequence*와 정합하는가? 직접 매핑 부재. continuous (δ, κ)와 MultiVelo discrete state의 *대응 관계*가 본문 명확히 정리되지 않음.

## Final Takeaways

- **이 논문의 가장 큰 의미**:
  - MultiVelo (`@li2023multivelo`)의 *discrete state + single sample* 한계를 *continuous + multi-sample + differential test*로 일반화한 framework-level 진전. RNA velocity 분야에서 *VAE-based + multi-omic + statistical testing*을 단일 model로 통합한 first paper급 contribution.
  - 신규 dataset 3개 (EB 7-day, HSPC×2, HSPC+macrophage, GSE284047) 공개 — community asset.
  - GCBDir metric (k-step + time ordering + random-walk null) 제안 — RNA velocity benchmarking에서 새로운 standard 후보.
  - In silico TF perturbation을 *velocity framework 안에서* 가능하게 함 → Dynamo, CellOracle과 함께 *velocity-based perturbation prediction*의 정착에 기여.
  - cross-modality ATAC imputation 능력 — scRNA-only sample을 multi-omic reference와 join 가능 → 압도적으로 많은 public scRNA dataset 활용 가능.

- **다음 논문으로 이어질 아이디어**:
  - **(아이디어 1) Atlas-level pre-training**: Discussion에서 저자가 직접 언급. Human Cell Atlas + ENCODE 같은 atlas dataset으로 *pre-trained MultiVeloVAE foundation model*을 만들어 새 dataset에 *transfer learning*. low-quality / small dataset에서도 robust velocity inference 가능. → "Foundation model for single-cell multi-omic velocity"
  - **(아이디어 2) Continuous coupling/decoupling을 wet-lab perturbation으로 검증**: MultiVeloVAE 예측 high-δ priming gene (HSPC AZU1, LYZ 등)을 CRISPRi targeted KD 후 chromatin opening / transcription rate 시계열 측정. δ가 *causally regulatory significance*를 가짐을 입증. → "Validating continuous priming/decoupling factors with perturbation"
  - **(아이디어 3) Stochastic VAE extension**: 현 MultiVeloVAE는 deterministic ODE + Gaussian observation. Markov chromatin process나 chemical master equation을 VAE decoder ODE로 결합 → bursty transcription 직접 modeling. → "Stochastic multi-omic velocity with chemical master equation"
  - **(아이디어 4) MultiVeloVAE on disease single-cell**: 정상 vs 질환 (e.g., AML vs healthy HSPC, autoimmune vs healthy macrophage) multi-omic data에 multi-sample inference + differential dynamics test 적용. *질환 특이적 driver dynamics* 발견. 우리 HSPC pipeline + 외부 disease cohort 결합 가능. → "Differential multi-omic velocity in hematologic malignancy"
  - **(아이디어 5) Spatial multi-omic velocity**: Spatial transcriptomics (Slide-seqV2, Stereo-seq) + spatial ATAC (e.g., spatial-CUT&Tag)와 MultiVeloVAE 결합. spatial neighbor와 latent time alignment를 동시 학습. → "Spatial multi-omic velocity"
  - **(아이디어 6) CITE-seq extension**: Discussion에서 저자 직접 언급. protein modality 추가 → 4-modality joint model (c, u, s, protein). protein degradation rate가 새로운 ODE parameter. → "Protein-aware multi-omic velocity"
  - **(아이디어 7) MultiVeloVAE meets long-read sequencing**: long-read scRNA (e.g., scISOseq)와 결합해 isoform-level velocity 추정. 동일 gene 다른 isoform의 priming/decoupling이 다를 가능성. → "Isoform-resolved multi-omic velocity"

- **설명을 더 매끄럽게 만들 방법**:
  - Fig. 2f / Fig. 3g / Fig. 4d-e / Fig. 3h의 정확 metric 값을 *본문 table*에 명시. dataset × method matrix가 더 신뢰감.
  - δ/κ continuous → MultiVelo discrete state mapping 정량 그림 (e.g., 2D histogram of MultiVelo state assignment × MultiVeloVAE (δ, κ) value)을 추가하면 두 method의 *동등 / 차별점*이 명확.
  - Bayesian differential test의 nominal vs realized FDR calibration (simulation 또는 known null gene set)을 supplementary에 추가.
  - in silico KO simulation의 *quantitative agreement* (with Dynamo / CellOracle / wet-lab when available)를 correlation plot으로 제시.
  - mature cell type 한계 (Discussion 명시)를 *negative example* (PBMC fitting failure)로 시각화.

- **우선순위가 높은 후속 실험 / 분석**:
  - **(1) 우리 HSPC dataset에서 MultiVelo vs MultiVeloVAE 직접 비교**: 같은 input AnnData로 두 method 돌려 ① MultiVelo discrete state vs MultiVeloVAE continuous (δ, κ) confusion matrix, ② cell-type-specific decoupling (MultiVelo는 못 본 신호) 식별, ③ runtime / memory 측정. 우리 lens-academic에서 가장 직접 적용 가능한 follow-up.
  - **(2) Differential dynamics test FDR calibration**: known null gene set (housekeeping)에서 macrophage vs DC test의 nominal vs realized FDR 측정. 우리가 future 분석에 사용 시 *trust threshold* 결정에 직결.
  - **(3) Cell cycle confound 별도 ablation**: HSPC dataset에서 cell cycle phase별 (G1/S/G2M) MultiVeloVAE separate fit → k_c, ρ가 phase 따라 어떻게 변하는지 정량. `@li2023multivelo`와 본 paper 모두 미검증 영역.
  - **(4) Cross-modality ATAC prediction의 ground-truth 비교 재검증**: Supplementary Fig. 19의 GCBDir > ground-truth ATAC 결과가 *true generalization*인지 evaluation artifact인지 우리 데이터로 spot check.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- **§Introduction (p2)**: "previous approaches lack key capabilities that are required to make RNA velocity useful for biological discovery: multi-sample inference; the ability to model multi-omic data; incorporating different types of data; and differential testing."
  - 사용 시나리오: 본인 introduction에서 *RNA velocity의 4가지 본질적 한계*를 짚을 때 4-axis 정리로 활용.
  - BibTeX key: `@li2025multivelovae`

- **§Introduction (p2)**: "we introduce MultiVeloVAE, a robust probabilistic model that enables multi-sample velocity inference from single-cell RNA and/or single-cell multi-omic data. Crucially, MultiVeloVAE also enables statistical testing to identify differential velocity, models all genes on a common time scale, and models developmental lineage bifurcation by allowing rate parameters to vary continuously with cell state."
  - 사용 시나리오: MultiVeloVAE의 *one-sentence summary* 인용. review 또는 본인 multi-omic method paper의 prior work 단락.
  - BibTeX key: `@li2025multivelovae`

- **§Results "MultiVeloVAE infers state-specific decoupling patterns" p8**: "the notions of coupled and decoupled states are no longer discrete but continuous and cell-specific. That is, rather than inferring a single value for the amount of coupling or decoupling for a gene across all cells, the chromatin accessibility and transcription of a gene can now be coupled or decoupled to varying degrees across a population of cells."
  - 사용 시나리오: MultiVelo → MultiVeloVAE의 *핵심 generalization*을 인용할 때.
  - BibTeX key: `@li2025multivelovae`

- **§Discussion (p13-14)**: "MultiVeloVAE represents a significant advancement in RNA velocity analysis, with enhanced inference accuracy, multi-sample support, and interpretable kinetic parameters. We anticipate that MultiVeloVAE will be especially valuable for exploring gene dynamics in settings requiring multi-sample comparisons, such as case-control studies, developmental atlases, and studies of genetic variation."
  - 사용 시나리오: case-control / atlas / GWAS 관련 본인 proposal에서 MultiVeloVAE를 candidate tool로 인용.
  - BibTeX key: `@li2025multivelovae`

- **§Discussion (p14)**: "current velocity inference methods, including deep-learning-based approaches, rely on de novo training ... Developing pre-trained and validated parameter sets for known cell types could benefit applications that require generic velocity inference on similar, low-quality samples."
  - 사용 시나리오: *atlas-level pre-training의 부재*를 본인 후속 paper motivation으로 인용. foundation model angle.
  - BibTeX key: `@li2025multivelovae`

- **§Results "Multi-sample multi-omic velocity inference..." p7**: "Performing batch correction using separate approaches prior to velocity inference risks disrupting the intricate relationship between modalities. For instance, we attempted to use Scanorama to extract batch corrected modality counts jointly from the two samples; however, the corrected modalities no longer support successful multi-omic velocity prediction afterwards."
  - 사용 시나리오: pre-correction → velocity *chaining의 위험*을 인용할 때. 본인 multi-sample velocity tool 설계 시 motivation.
  - BibTeX key: `@li2025multivelovae`

### 인용 가능 수치

- **EB dataset: 4,240 cells × 3,138 genes, 7-day human embryoid body 10x Multiome** (§"Automated data preprocessing" p20, GSE284047).
  - 사용 시나리오: 신규 multi-lineage benchmark dataset 인용. 우리 organoid / EB 분석 시 expected scale baseline.
  - BibTeX key: `@li2025multivelovae`

- **HSPC×2 integration: 17,667 cells × 892 genes** (§"Automated data preprocessing" p20).
  - 사용 시나리오: multi-sample HSPC multi-omic integration의 scale 인용.
  - BibTeX key: `@li2025multivelovae`

- **HSPC + macrophage integration: 9,908 cells × 929 genes** (§"Automated data preprocessing" p20).
  - 사용 시나리오: differentiation time-course multi-sample 인용.
  - BibTeX key: `@li2025multivelovae`

- **3-sample partial integration (HSPC×2 + BMMC scRNA): 27,841 cells × 1,044 genes** (§"Automated data preprocessing" p20).
  - 사용 시나리오: partial-modality (multi-omic + RNA-only) joint inference의 scale 인용.
  - BibTeX key: `@li2025multivelovae`

- **Macrophage cluster n=850, DC cluster n=221, 5,000 posterior-sampled cells, p < 0.05 + FDR < 0.05** for differential velocity (Fig. 6b caption).
  - 사용 시나리오: Bayesian differential dynamics test의 *sample size + significance threshold* 인용.
  - BibTeX key: `@li2025multivelovae`

- **CellRank perturbation fate analysis cell counts: Platelet=651, Erythrocyte=3,043, Mast Cell=476, Granulocyte=1,211, DC=294, Prog B=668** (Fig. 7g caption).
  - 사용 시나리오: in silico perturbation의 *cell type별 sample size* 인용.
  - BibTeX key: `@li2025multivelovae`

- **GCBDir metric definition: k-step CBDir averaged over multiple step sizes, minus random-walk null** (Methods Eq. 19-20).
  - 사용 시나리오: 본인 RNA velocity benchmark에서 GCBDir 사용 시 정의 인용.
  - BibTeX key: `@li2025multivelovae`

### 인용 가능 Figure/Table

- **Figure 1 (overview schematic)**:
  - 무엇을 보여주는지 한 줄: cVAE architecture + multi-sample integration + 기존 method 대비 feature table.
  - 사용 시나리오: 본인 review에서 *multi-omic VAE-based RNA velocity*의 schematic으로 인용. *재현 시 license (CC BY-NC-ND 4.0) 확인 필요* — non-commercial only, no derivatives.
  - BibTeX key: `@li2025multivelovae`

- **Figure 2f (10 scRNA-seq dataset benchmark box plot)**:
  - 무엇을 보여주는지 한 줄: RNA-only mode가 6개 baseline (scVelo, UniTVelo, DeepVelo, VeloVI, PyroVelocity, cellDancer) 대비 latent time correlation + GCBDir + Mann–Whitney U에서 일관 우위.
  - 사용 시나리오: 본인 paper에서 *현존 RNA velocity method의 비교 reference* 인용.
  - BibTeX key: `@li2025multivelovae`

- **Figure 3a, b (EB dataset MultiVeloVAE vs MultiVelo)**:
  - 무엇을 보여주는지 한 줄: 신규 EB dataset에서 MultiVeloVAE가 NANOG+ root 정확 + 3 germ layer trajectory, MultiVelo는 backflow.
  - 사용 시나리오: *multi-lineage benchmark*의 시각적 reference. 우리 organoid 분석 시 expected behavior 인용.
  - BibTeX key: `@li2025multivelovae`

- **Figure 4d-e (scIB integration benchmark)**:
  - 무엇을 보여주는지 한 줄: cVAE가 Scanorama / scVI와의 batch removal ↔ biological conservation trade-off에서 *biology preservation* 쪽 우위.
  - 사용 시나리오: 본인 multi-sample integration tool 비교 시 reference baseline.
  - BibTeX key: `@li2025multivelovae`

- **Figure 5a-b (continuous coupling/decoupling factor on HSPC lineage markers)**:
  - 무엇을 보여주는지 한 줄: HDC, AZU1, LYZ가 lineage별로 다른 δ 부호 → cell-type-specific gene regulation 가능.
  - 사용 시나리오: continuous (δ, κ)의 *biological interpretability*를 본인 분석에서 시각 reference.
  - BibTeX key: `@li2025multivelovae`

- **Figure 6c (PROS1 temporal cascade chromatin → velocity → spliced)**:
  - 무엇을 보여주는지 한 줄: chromatin opening early → RNA velocity mid → spliced count late의 *시간 cascade*를 single gene에서 시각화.
  - 사용 시나리오: chromatin-RNA lag을 *gene-level concrete example*로 인용. 본인 epigenomic-lag topic의 *visual exemplar*.
  - BibTeX key: `@li2025multivelovae`

- **Figure 7e-h (SPI1/GATA1 in silico KO + CellRank fate change + CellOracle consistency)**:
  - 무엇을 보여주는지 한 줄: in silico TF perturbation이 기존 method (Dynamo, CellOracle)와 consistent하게 lineage 차단 예측.
  - 사용 시나리오: drug target nomination 또는 perturbation prediction 관련 proposal에서 *velocity framework이 perturbation simulation 가능*의 예시.
  - BibTeX key: `@li2025multivelovae`
