# MultiVelo Paper Analysis

## 1. Paper Info

- **Title:** Multi-omic single-cell velocity models epigenome–transcriptome interactions and improves cell fate prediction
- **Authors:** Chen Li, Maria C. Virgilio, Kathleen L. Collins, Joshua D. Welch
- **Year:** 2023 (published online October 13, 2022)
- **Journal:** Nature Biotechnology, Volume 41, pages 387–398
- **DOI:** 10.1038/s41587-022-01476-y
- **Paper type:** Method

## 2. Executive Overview (3-5 sentences)

MultiVelo extends the RNA velocity framework to incorporate chromatin accessibility data from single-cell multi-omic (ATAC+RNA) datasets, modeling the temporal relationship among chromatin state (c), unspliced RNA (u), and spliced mRNA (s) via coupled ODEs. The paper identifies two distinct gene regulation classes — Model 1 (chromatin closes before transcription ceases) and Model 2 (transcription ceases before chromatin closes) — and defines four cell states (primed, coupled-on, decoupled, coupled-off) that capture the degree of epigenome-transcriptome synchrony. Applied to mouse brain, mouse skin, human HSPC, and human fetal brain datasets, MultiVelo improves cell fate prediction accuracy over RNA-only velocity (scVelo) by eliminating biologically implausible backflows. The method quantifies priming and decoupling intervals as fractions of the induction-repression cycle but does not extract gene-specific activation lag or shutdown lag as continuous, standalone kinetic variables.

## 3. Research Question & Motivation (1-2 paragraphs)

The primary research question is: can incorporating chromatin accessibility dynamics into RNA velocity improve the modeling of gene expression kinetics and cell fate prediction in single-cell multi-omic data? The secondary question is whether distinct temporal patterns of chromatin-transcription coupling exist across genes and cell states.

The motivation is that existing RNA velocity methods (scVelo) model only spliced/unspliced RNA, ignoring epigenomic regulation that precedes transcription. Since chromatin remodeling at promoters and enhancers is a prerequisite for transcriptional activation, failing to incorporate it leads to inaccurate velocity estimates, especially in stem cells undergoing rapid epigenomic changes. Prior approaches could not leverage the paired chromatin+RNA information now available from 10x Multiome and SHARE-seq assays.

**Project connection:** MultiVelo directly addresses the temporal ordering of chromatin opening and transcription — the foundation of our project's **activation lag** and **shutdown lag** concepts. The paper's Model 1/Model 2 classification and priming/decoupling intervals are precursors to lag quantification, but they frame timing as discrete switch-time differences rather than continuous per-gene lag variables. This distinction is critical: MultiVelo provides the conceptual and computational substrate for lag estimation, but the actual continuous activation lag / shutdown lag extraction requires additional post-processing or extension (as attempted by MoFlow and MultiVeloVAE).

## 4. Methods (1-2 paragraphs)

MultiVelo models gene expression dynamics through three coupled ODEs: chromatin accessibility c(t) governed by opening/closing rate alpha_c with a binary switch k_c in {0,1}; unspliced RNA u(t) with transcription rate proportional to c(t); and spliced RNA s(t) with splicing rate beta and degradation rate gamma. Three switch times are estimated per gene: t_i (transcription induction start), t_c (chromatin closing start), and t_r (transcription repression start). The relative ordering of t_c and t_r determines Model 1 (t_c < t_r) vs. Model 2 (t_r < t_c). Parameters are fitted via an iterative EM algorithm — the E-step assigns each cell a latent time by projecting to the nearest point on the ODE trajectory (500–1,000 anchor points over [0, 20] arbitrary time units), and the M-step optimizes rate parameters via Nelder-Mead simplex minimization of MSE. Block coordinate descent sequentially updates c-exclusive, u-related, then s-related parameters, typically converging in 5–10 iterations.

Chromatin data is preprocessed by aggregating ATAC peaks at promoters (within 10 kb of TSS) and correlated distal enhancers (>=0.5 correlation within 10 kb), followed by TF-IDF normalization and [0,1] scaling. Smoothing via weighted nearest neighbors (WNN, 50 neighbors) addresses ATAC sparsity. Gene-level Model 1/2 assignment uses the ratio of top chromatin values relative to the steady-state line before parameter fitting. Dynamic time warping (DTW) is applied post-hoc to quantify time lags between modalities (e.g., c vs. s, TF expression vs. binding site accessibility), but this is an analysis step, not part of the core model.

## 5. Dataset & Experimental Setup

MultiVelo was applied to four single-cell multi-omic datasets:

| Dataset | Species / Tissue | Modality | Cells (post-QC) | Genes | Accession |
|---|---|---|---|---|---|
| Embryonic mouse brain | Mouse E18 cortex | 10x Multiome (ATAC+RNA) | 3,365 | 936 | 10x Genomics website |
| Mouse hair follicle | Mouse dorsal skin | SHARE-seq (paired ATAC+RNA) | 6,436 | 962 | GSE140203 |
| Human HSPC | Human CD34+ cells (Day 0 + Day 7) | 10x Multiome | 11,605 | 1,000 | Fred Hutch (generated) |
| Human fetal cortex | Human developing brain | 10x Multiome | 4,693 | 919 | Authors' prior publication |

All datasets provide paired chromatin accessibility and RNA from the same cells. Bulk ChIP-seq from GSE70677 was used as supplementary annotation for HSPCs. The human brain dataset had one batch removed due to severe batch effects.

- Dataset sizes are adequate for demonstrating the method across diverse biological systems.
- No formal train/test split; the method is unsupervised (EM fitting per gene).
- Data leakage is not a major concern for this type of generative model, but the lack of held-out validation is a limitation.

## 6. Key Results

### Result 1: Model 1 vs. Model 2 gene classification

- **Authors' claim:** Genes fall into two mechanistically distinct classes based on the temporal ordering of chromatin closing and transcriptional repression.
- **Evidence:** In mouse brain, 41.4% of variable genes are Model 1, 26.7% Model 2, 29.5% induction-only, 2.4% repression-only. GO enrichment shows Model 2 enriched for cell cycle terms (positive regulation of cell cycle, mitotic cell cycle; FDR <0.002). Model 1 genes achieve highest spliced expression earlier in latent time than Model 2 (p=9e-7, Wilcoxon rank-sum).
- **My assessment:** The classification is well-supported by consistent patterns across all four datasets and simulation validation (1,000 simulated genes with accurate recovery of model labels).
- **Strength of support:** **Strong**
- **Caveat:** The binary M1/M2 classification obscures what is likely a continuum of timing relationships. Genes near the M1/M2 boundary may be misclassified.

### Result 2: Improved velocity and cell fate prediction

- **Authors' claim:** MultiVelo produces more accurate velocity streamplots and latent time estimates than RNA-only scVelo.
- **Evidence:** Visual elimination of biologically implausible backflows in mouse brain and human brain; Spearman correlation with Palantir pseudotime: 0.51 (MultiVelo) vs. 0.44 (scVelo) in mouse skin. Correct prediction of hair follicle TAC to IRS/shaft differentiation where scVelo fails.
- **My assessment:** The improvement is consistent but modest in quantitative terms. Evaluation relies heavily on visual comparison and a single correlation metric against one external pseudotime method.
- **Strength of support:** **Moderate**
- **Caveat:** No systematic benchmark against multiple trajectory inference methods. The 0.07 improvement in Spearman correlation (0.51 vs. 0.44) is suggestive but not large.

### Result 3: Priming and decoupling interval quantification

- **Authors' claim:** The model quantifies the length of priming intervals (chromatin open, transcription not yet started) and decoupling intervals (chromatin and transcription moving in opposite directions).
- **Evidence:** Median priming interval = 21% of induction-repression cycle; median decoupling interval = 19% (mouse brain). Coupled on/off states comprise the larger proportion. Pattern consistent across tissues.
- **My assessment:** These intervals are derived from switch time differences (priming = t_i, decoupling = t_r - t_c), which are continuous per-gene values. However, they are expressed in arbitrary latent time units, not real time, and their uncertainty is not quantified (no confidence intervals or bootstrap estimates).
- **Strength of support:** **Moderate**
- **Caveat:** Without uncertainty quantification, it is unclear which per-gene interval estimates are reliable vs. noise-driven, especially for low-expression genes.

### Result 4: TF expression–binding site accessibility time lag (DTW)

- **Authors' claim:** TF expression generally precedes binding site accessibility, with a positive median time lag across expressed TFs (human brain).
- **Evidence:** DTW alignment of TF expression and chromVAR motif accessibility time series. Example: Wnt3 in mouse skin shows c-to-s delay up to 0.6 normalized time units. EGR1 and PBX3 show consistent lead of TF expression over motif accessibility.
- **My assessment:** DTW is applied post-hoc, not as part of the core model. The lag values are informative but are in normalized pseudotime units. The analysis is descriptive rather than predictive.
- **Strength of support:** **Moderate**
- **Caveat:** DTW lag is a derived quantity, not a primary model output. Its biological meaning depends on the fidelity of the underlying latent time, which is not independently validated.

## 7. Biological / Practical Interpretation (1-2 paragraphs)

MultiVelo provides a mechanistic interpretation of chromatin-transcription coupling: Model 1 genes (chromatin closes before transcription ceases) may represent genes where chromatin state is a leading indicator of future transcriptional shutdown, while Model 2 genes (transcription ceases before chromatin closes) maintain an accessible chromatin state even after silencing — potentially reflecting epigenetic memory. The identification of primed and decoupled states in specific cell populations (e.g., primed radial glia, decoupled transit-amplifying cells) connects to known biology of stem cell fate commitment, where epigenomic priming precedes transcriptional activation.

However, the biological conclusions are largely associative, not mechanistic. The paper acknowledges that "we cannot conclusively determine the mechanisms underlying these time lags without additional data." The Model 1/2 distinction is inferred from ODE fitting, not from direct perturbation experiments. Whether the observed priming intervals reflect genuine biological priming vs. artifacts of pseudotime compression or ATAC sparsity remains an open question. The classification of psychiatric disease SNPs into three temporal groups (757 SNPs from 6,968 psychiatric GWAS variants) is interesting but speculative without functional validation.

## 8. Strengths (3-5 bullet points)

- **Principled ODE extension:** Elegantly extends the scVelo dynamical model from 2 variables (u, s) to 3 (c, u, s) with a clear biological rationale for chromatin-dependent transcription rate.
- **Consistent results across diverse datasets:** Model 1/Model 2 distinction and improved velocity accuracy replicate across mouse brain, mouse skin, human HSPC, and human brain — covering both 10x Multiome and SHARE-seq platforms.
- **Simulation validation:** Systematic recovery of model parameters and gene classification from 1,000 simulated genes with varying noise levels builds confidence in the inference procedure.
- **Software availability:** Well-packaged Python tool on PyPI, Bioconda, and GitHub with documented preprocessing pipelines for both data types. Reasonable runtime (40–124 min) and memory (0.86–2.9 GB).
- **Novel biological insight:** The four cell states (primed, coupled-on, decoupled, coupled-off) provide a new interpretive framework for understanding epigenome-transcriptome dynamics during differentiation.

## 9. Limitations (3-5 bullet points)

- **No continuous activation/shutdown lag variable:** The paper defines priming and decoupling intervals via switch time differences, but these are discrete interval lengths in arbitrary latent time — not continuous, per-gene kinetic lag variables with uncertainty estimates. This is the key gap for our project.
- **Pseudotime is not wall-clock time:** All temporal quantities (switch times, intervals, DTW lags) are in arbitrary latent time units. No validation against real-time measurements (e.g., 4sU labeling, time-course experiments) is provided. Latent time is normalized to [0, 20] per gene, making cross-gene temporal comparisons unreliable without additional calibration.
- **Binary chromatin model:** Chromatin is treated as switching between fully open and fully closed states, ignoring intermediate accessibility levels, histone modification gradients, enhancer-promoter looping dynamics, and the complex effects of pioneer factors.
- **No uncertainty quantification on switch times:** Point estimates from EM optimization lack confidence intervals. For genes with sparse ATAC signal or low expression, the reliability of M1/M2 assignment and interval lengths is unknown.
- **Evaluation limited to visual comparison and single correlation metric:** No systematic cross-validation, no comparison against trajectory inference methods beyond Palantir, no held-out gene or cell evaluation. The 0.07 Spearman improvement is modest and not statistically tested.

## 10. Comparison to Prior Work (1-2 paragraphs)

Relative to scVelo (Bergen et al., 2020), MultiVelo's main advance is the incorporation of chromatin accessibility as a third variable in the ODE system, enabling velocity estimation that accounts for epigenomic priming. This is genuinely new — scVelo models only u and s, ignoring the upstream regulatory layer. The improvement is most pronounced in cell states where epigenome and transcriptome are decoupled (stem cells, progenitors), which is precisely where RNA-only velocity fails most.

Compared to subsequent methods: **MultiVeloVAE** (Nat Commun 2025) extends MultiVelo to cell-specific and gene-specific dynamics using a VAE framework, and defines a continuous "decoupling factor" that is closer to our project's continuous lag concept. **MoFlow** (Nat Commun 2025) directly computes gene-specific chromatin-RNA lag via DTW at single-cell resolution without pre-assigned latent time, producing the closest existing analog to our activation lag / shutdown lag. MultiVelo is the conceptual foundation for both methods, but its discrete switch-time parameterization and gene-independent latent time are limitations that both successors address.

**Project connection:** MultiVelo is the foundational method for our project's Step 1 (lag quantification). It provides the ODE framework, the M1/M2 gene classification, and the priming/decoupling interval concept. However, it does not directly output the continuous activation lag and shutdown lag variables our project requires. Specifically:
- **Activation lag** (chromatin open -> transcription start) maps to MultiVelo's priming interval (t_i), but only as a single point estimate per gene in arbitrary time.
- **Shutdown lag** (transcription off -> chromatin close) maps to the decoupling interval (|t_r - t_c|), with the same limitation.
- To operationalize these for Step 2 (baseline feature prediction) and Step 3 (perturbation validation), we would need to: (a) extract per-gene priming/decoupling values from MultiVelo's fitted parameters, (b) add bootstrap CI, (c) control for burst kinetics and cell cycle confounds, and (d) validate against real-time data. MoFlow's DTW approach or MultiVeloVAE's decoupling factor may be more directly suitable for continuous lag extraction.

## 11. Reproducibility Assessment

| Criterion | Status |
|---|---|
| Data availability | Partially public. Mouse brain (10x), SHARE-seq (GSE140203), bulk ChIP (GSE70677) are public. Human HSPC was generated internally (availability unclear). Human brain from authors' prior work. |
| Code availability | Public. GitHub: welch-lab/MultiVelo, PyPI, Bioconda. |
| Parameter details | Reported. EM convergence criteria, likelihood thresholds per dataset, WNN smoothing parameters, anchor point counts specified. |
| Software versions | Partially reported. CellRanger ARC versions specified; Python/Numba versions not explicitly stated. |
| Random seed | Not explicitly reported. |
| Statistical test details | Limited. GO enrichment, Wilcoxon rank-sum (p=9e-7), and Spearman correlations reported, but no formal statistical tests for interval length reliability or M1/M2 boundary sensitivity. |
| Figure-to-method consistency | Good. Figures clearly map to described analyses. |
| Runtime/memory | Reported. 40–124 min, 0.86–2.9 GB across datasets. |

**Rating: Moderate**

The code is public and well-documented, and most preprocessing steps are described. However, the absence of random seeds, incomplete software version specification, and the lack of statistical rigor in key claims (interval reliability, M1/M2 boundary sensitivity) prevent full reproducibility. The HSPC dataset's availability status is ambiguous.

## 12. Final Verdict

- **Take-home message:** MultiVelo is the first principled framework for joint chromatin-RNA velocity modeling. It introduces the M1/M2 gene classification and priming/decoupling concepts that are foundational for understanding chromatin-transcription temporal dynamics. However, it does not directly quantify gene-specific activation lag or shutdown lag as continuous variables, and all temporal quantities are in arbitrary pseudotime units.

- **What I would trust:** The M1/M2 gene classification pattern (replicated across 4 datasets and simulations). The qualitative improvement over RNA-only velocity in stem/progenitor populations. The software implementation and its consistent behavior across platforms.

- **What I would verify independently:** Per-gene priming/decoupling interval estimates (need bootstrap CI). The biological interpretation of Model 2 as "epigenetic memory." The DTW-based TF lag analysis (sensitive to pseudotime accuracy). Whether the improvement over scVelo holds with newer RNA velocity methods (veloVI, scVelo2) as baseline.

- **Who this paper is useful for:** Researchers working with single-cell multi-omic (ATAC+RNA) data who want to incorporate chromatin dynamics into velocity and trajectory analysis. Teams building on chromatin-transcription timing concepts for downstream prediction tasks.

## 13. Project Utility Assessment

**Adaptable with modification**

- **What is useful:** The ODE framework (c->u->s), Model 1/Model 2 gene classification, priming interval and decoupling interval concepts, and the four cell-state taxonomy (primed, coupled-on, decoupled, coupled-off) provide the conceptual and computational foundation for our project's Step 1.
- **How it maps to our 3-step framework:**
  - *Step 1 (lag quantification)*: MultiVelo's switch times (t_i, t_c, t_r) can be post-processed to extract priming interval ~ activation lag and decoupling interval ~ shutdown lag. This is the most direct mapping, but requires adding uncertainty quantification and confound control (burst kinetics, cell cycle).
  - *Step 2 (baseline feature prediction)*: MultiVelo uses aggregated ATAC peaks and TF-IDF normalization as chromatin features, which can serve as baseline features for lag prediction models. However, it does not perform the predictive modeling step itself.
  - *Step 3 (perturbation validation)*: Not addressed. No drug perturbation or time-course validation is included.
- **What needs adaptation:** (1) Extract continuous per-gene lag values from fitted switch time parameters with bootstrap CI. (2) Control for burst kinetics (mean expression + variance) and cell cycle phase as covariates. (3) Convert arbitrary latent time to a scale interpretable for drug response prediction, or validate that latent time ranking preserves real-time ordering. (4) Supplement with MoFlow's DTW-based lag or MultiVeloVAE's decoupling factor for more robust continuous lag estimates.

---

Sources:
- [MultiVelo — Nature Biotechnology](https://www.nature.com/articles/s41587-022-01476-y)
- [MultiVelo — PMC Full Text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10246490/)
- [MultiVelo — PubMed](https://pubmed.ncbi.nlm.nih.gov/36229609/)
- [MultiVelo — GitHub (welch-lab/MultiVelo)](https://github.com/welch-lab/MultiVelo)
- [MoFlow — Nature Communications](https://www.nature.com/articles/s41467-025-67259-6)
