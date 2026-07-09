# Related Work — chromatin-informed velocity, benchmarks, and the chromatin→transcription lag

> Literature scout deliverable for the HSPC velocity-lag benchmark manuscript.
> Grounds the study's claims (see `results/FINDINGS.md`) in prior work, states the scoop verdict, and
> positions the contribution honestly. All bibliographic detail verified against CrossRef/PubMed
> (accessed 2026-07-05); items I could not fully verify are flagged inline.
>
> Study in one line: we benchmark five velocity arms (scVelo dynamical RNA-only floor, MultiVelo,
> MultiVeloVAE, MoFlow, CRAK-Velo) on the **gene-level chromatin→transcription lag** in human HSPC 10x
> Multiome (GSE209878), cross-replicated on human fetal cortex (GSE162170). Core result is a
> **negative/robustness benchmark**: the per-gene lag is *not* method-robust (pairwise Spearman
> ρ ≈ −0.04 to +0.12; cross-method sign-agreement set = 0/598 genes at FDR<0.10), whereas
> transcription rate α is robust (ρ=0.88), the population direction balance (~50/50) is robust, and
> canonical priming-marker direction is robust. A negative control shows MultiVelo's lag is driven by
> model structure (switch-time ordering), not chromatin.

---

## 0. SCOOP CHECK — verdict first

**Verdict: NOVEL, but partially anticipated — the specific systematic negative result is ours; the raw
observation that two methods can disagree on a gene's lag is not new.**

What we searched for and what we found:

1. **A published paper stating that chromatin-informed / multiome velocity methods disagree on the
   gene-level chromatin→transcription lag, as its thesis?** — **Not found.** No paper treats
   cross-method concordance of the lag as the object of study.

2. **General RNA-velocity benchmarks (2026) — do they cover this?** Two large 2026 benchmarks exist and
   are *adjacent but not overlapping*:
   - *Benchmarking RNA velocity methods across 17 independent studies* (Cell Reports Methods 2026;
     bioRxiv 2025.08.02.668272) evaluates **15 RNA-only methods** on **accuracy / stability /
     usability of velocity direction** — it does not include the multiome-lag methods and does not
     score a chromatin→transcription lag at all.
   - *Benchmarking algorithms for RNA velocity inference* (bioRxiv 2026.01.03.697314; 29 algorithms,
     176 datasets, extended to multi-omics) **does include** MultiVelo and scKINETICS, but scores them
     on **developmental-flow / directionality validity** (e.g. it reports MultiVelo showing more
     frequent local disagreements with expected transition direction than scKINETICS). It benchmarks
     *velocity vectors*, **not per-gene lag concordance**, and applies neither a permutation-FDR
     agreement test nor a causal negative control.
   → Neither benchmark measures what we measure. We should cite both and state plainly that they
     score velocity *direction*, whereas we score the *lag* quantity and its cross-method reproducibility.

3. **The method papers themselves — incidental per-gene lag comparisons against MultiVelo?** This is the
   real prior-art edge, because MoFlow, MultiVeloVAE and CRAK-Velo each published claiming to improve on
   MultiVelo. The one direct hit:
   - **MoFlow** (Hong et al., Nat Commun 2025) reports an incidental cross-method observation: *"a
     consistent subset of genes exhibiting negative c–s [chromatin–spliced] lags via both global time
     from MultiVelo and MoFlow,"* while noting MultiVelo imposes overly linear trajectory dependencies.
     This is framed as **competitive validation on a favorable subset** (our method also recovers the
     biologically sensible negative-lag genes), **not** as a systematic robustness audit. It reports
     partial *agreement*, not a quantified ~0 concordance, and no negative control.

**What precisely remains ours after this check:**
- (a) **Systematic quantification of cross-method lag concordance across 4–5 arms** with a permutation
  null (N=10⁴) → per-gene agreement-set = **0/598 genes at FDR<0.10** (empty). No prior work quantifies
  the disagreement this way; the closest (MoFlow) reports a *concordant subset* on a single pairwise cut.
- (b) The **causal negative control** — shuffling ATAC within lineage leaves MultiVelo's lag
  distribution statistically unchanged (MW p=0.20, KS p=0.51, per-gene ρ=0.72 preserved) → the lag is
  **model-structural (switch-time ordering), not chromatin-driven**. No competing paper tests this.
- (c) The **α-robust / lag-fragile dissociation**: the same pipeline yields a highly reproducible
  transcription rate (cross-method ρ=0.88) and a non-reproducible lag, and the same day0-ATAC baseline
  features predict α (held-out ρ=+0.31) but not lag (≈chance). This "what survives vs. what doesn't"
  framing is the contribution, and is absent from the method papers, which report lag as a headline
  biological readout without a reproducibility audit.

A "we beat MultiVelo" plot is a competitive claim; a *robustness critique with a null model and a causal
control* is a different kind of claim. That framing distinction is defensible and should be stated
explicitly in the paper. **Scoop risk: low-to-moderate — cite MoFlow's incidental comparison up front
and differentiate; do not claim to be the first to notice any cross-method lag discrepancy.**

---

## 1. Landscape

### (i) Chromatin-informed / multiome velocity methods — and the lag/timing quantity each defines

| Method | Ref | Lag/timing quantity it defines |
| --- | --- | --- |
| **MultiVelo** | Li et al. 2023, Nat Biotechnol [1] | ODE with chromatin switch time; explicit lags Δt_priming = t_i and Δt_decoupling = t_r − t_c between chromatin and RNA switch times; classifies genes into M1 (chromatin closes *before* transcriptional repression) vs M2 (*after*). **This is the lag our benchmark centers on.** |
| **MultiVeloVAE** | Li et al. 2025, Nat Commun [2] | VAE extension; continuous, cell-specific **decoupling factor δ** (chromatin-opening rate − transcription rate) and **coupling factor κ**; generalizes the discrete priming/decoupling of MultiVelo to per-cell values. |
| **MoFlow** | Hong et al. 2025, Nat Commun [3] | "Relay velocity" deep net; infers per-cell chromatin opening/closing, transcription, splicing, degradation rates without pre-assigned latent time; reports chromatin–spliced (c–s) lags and distinguishes chromatin-dependent vs -independent repression. |
| **CRAK-Velo** | El Kazwini et al. 2026, Genome Biol [4] | Semi-mechanistic model integrating chromatin-accessibility kinetics into velocity; our arm derives a DTW-based lag from its trajectories (see `crakvelo_sign_check.md`; a sign-convention bug and a smooth-kinetics shape artifact were found and are reported as a caution against using its lag cross-method). |
| **ArchVelo** | Nat Commun 2026 (s41467-026-74000-4) [5] — *verify author list* | Archetypal decomposition of paired scATAC+scRNA trajectories with gene-level latent-time alignment; benchmarked on mouse brain and human hematopoiesis. Not in our arms; relevant as a same-family alternative. |
| **scKINETICS** | Su et al. 2023, Bioinformatics 39(Suppl 1):i394 [6] | Regulatory-velocity using differential-accessibility peaks as priors; does not require paired RNA+ATAC. Included in the 697314 benchmark alongside MultiVelo. |

RNA-only dynamical/generative velocity that our floor and arms build on: scVelo dynamical model
(Bergen et al. 2020), **veloVI** (Gayoso et al. 2024, Nat Methods [7]) which adds posterior velocity
**uncertainty** quantification, and the RNA-only Bayesian **veloVAE** (Gu et al. 2026, PLOS Comput Biol
[8]) — distinct from the multiome MultiVeloVAE above; worth disambiguating in the text since names collide.

### (ii) Velocity benchmark / critique literature

| Work | Ref | Relevance to us |
| --- | --- | --- |
| **RNA velocity — current challenges and future perspectives** | Bergen et al. 2021, Mol Syst Biol [9] | The canonical "pitfalls" review: violated model assumptions, multiple kinetic regimes, and phase-portrait failures produce wrong velocities. Grounds our premise that a velocity-derived quantity must be robustness-checked. |
| **RNA velocity unraveled** | Gorin, Fang, Chari, Pachter 2022, PLOS Comput Biol [10] | Deep critique: velocity is often not actionable due to many user-set hyperparameters and mismatch between transcription biophysics and the models. Our negative result is a concrete instance in the multiome-lag setting. |
| **Towards reliable quantification of cell state velocities** | Marot-Lassauzaie et al. 2022, PLOS Comput Biol [11] | Documents pipeline inconsistencies and proposes κ-velo/eco-velo; motivates treating any velocity readout as fragile until shown otherwise. |
| **Benchmarking RNA velocity methods across 17 independent studies** | Cell Reports Methods 2026 [12] | 15 RNA-only methods, accuracy/stability/usability, "no universal winner." Scores direction, **not lag**; establishes that method choice matters — we extend that to the lag quantity. |
| **Benchmarking algorithms for RNA velocity inference** | bioRxiv 2026.01.03.697314 [13] | 29 algorithms incl. MultiVelo/scKINETICS, extended to multi-omics; scores developmental-flow validity. Closest general benchmark that touches multiome methods — but scores velocity vectors, not per-gene lag concordance, and no null/negative-control. |

### (iii) Chromatin→transcription priming / lag biology (does chromatin lead transcription, and at what timescale?)

- **Chromatin potential** (Ma et al. 2020, Cell [14]; SHARE-seq mouse skin, GSE140203): the foundational
  claim that **chromatin accessibility at DORCs precedes gene expression during lineage commitment**, i.e.
  chromatin *primes* fate. This is the biological hypothesis our benchmark stress-tests at gene level:
  our population-level ~50/50 directional balance says the *global* "chromatin-leads" claim is not
  supported per-gene in HSPC, while canonical priming markers do show chromatin-leading — consistent with
  priming being real for specific loci but not a genome-wide, method-invariant per-gene ordering.
- **Developing human cortex chromatin/gene-regulatory dynamics** (Trevino et al. 2021, Cell [15];
  GSE162170): multi-stage TF→motif-accessibility→target lags and disease-SNP timing in cortical
  neurogenesis. This is our **primary cross-dataset** — a transient-TF-rich system where lag is expected
  to be even more method-sensitive, so it is a fair external test of the α-robust/lag-fragile split.

### (iv) Parameter identifiability & likelihood geometry (closest prior art to §8)

Our §8 profiles the MultiVelo objective along the α axis vs the chromatin→transcription lag axis (lag =
t_sw2 − t_sw1) and finds α **stiff** (well-determined) while the lag direction is **sloppy/near-flat**
(per-gene curvature ratio κ_α/κ_lag ≈ 3.53×; α stiffer in 94.57% of genes) — a *relative (practical)*
non-identifiability. The closest prior art each anticipates a component but none combines the dissociation,
the curvature-ratio framing, and the chromatin-lag extension (scoop check 2026-07-10, `SCOOP-CHECK-2026-07.md`):

| Work | Ref | Overlap → our differentiation |
| --- | --- | --- |
| **Quantifying uncertainty in RNA velocity (ConsensusVelo)** | Zhang et al. 2024 [16] | **Closest — cite head-on.** Establishes *weak (near-non-)identifiability* of the cell latent-time / switching-time direction via likelihood flatness and Fisher information of t_c ("the likelihood remains almost constant for any sufficiently large τ_c"); switch time t0^(2) carries large right-skewed posterior uncertainty. → Anticipates the flat-switch-time half. **We differ:** RNA-only (no chromatin lag), single-parameter Fisher (not a Hessian sloppy/stiff spectrum), and it does **not** dissociate a *stiff α* from the sloppy switch (its λ is also weakly identified); Bayesian posterior framing, not profile-likelihood curvature. |
| **Profile-likelihood identifiability of single-cell bursting kinetics** | Gu et al. 2025, *Bioinformatics* btaf581 [17] | Uses **profile-likelihood** to prove *practical* (not structural) non-identifiability of telegraph-model rates (k_on/k_off/k_syn) from scRNA-seq. → Exact method precedent, but on bursting parameters, not velocity switch-time/lag. (Distinct from [8].) |
| **Are Single Cells Sloppy? (sloppy/stiff Fisher geometry)** | Wang 2025 [18] | Applies the **sloppy-vs-stiff Fisher-information eigenvalue** framework to single cells ("pronounced sloppiness in single cells"). → Same methodology, but on cell-**state** Gaussian coordinates (μ,σ), not velocity kinetic parameters. Direct methodological analog. |
| **BayVel: Bayesian RNA velocity** | 2025, arXiv 2505.03083 [19] | Proves **structural** non-identifiability of scVelo dynamical parameters via a time-shift invariance s(t+a, t0on+a,…) = s(t,…). → Complementary global-time-shift degeneracy (a known scale-degeneracy family); our claim is the *relative curvature* dissociation of lag vs α. |

None of the critiqued velocity/chromatin methods (scVelo, MultiVelo, MultiVeloVAE, MoFlow, CRAK-Velo, HALO)
performs any likelihood-geometry identifiability analysis of the switch-time/lag direction — so §8's
*application* to velocity kinetics and the α-stiff/lag-sloppy *dissociation* are not pre-empted, but the
switch-time-flatness observation itself must be credited to Zhang et al. [16].

---

## 2. Honest positioning against the closest 3–5 works

1. **vs. MultiVelo (Li et al. 2023 [1])** — MultiVelo *introduced* the gene-level chromatin↔transcription
   lag as a biological readout and reported the M1/M2 gene classes. We take that exact readout and ask a
   question the original paper did not: is it reproducible across methods, and is it actually driven by
   chromatin? Our negative control answers "no" for the second part within MultiVelo itself (shuffling
   ATAC does not change the lag), which reframes M1/M2 as partly a property of switch-time ordering.

2. **vs. MoFlow (Hong et al. 2025 [3])** — the closest prior art. MoFlow already compared its c–s lags to
   MultiVelo's and reported a *consistent subset* of negative-lag genes (agreement, favorable subset).
   We must cite this up front. Our contribution is orthogonal: we quantify the *disagreement*
   systematically across 4–5 arms with a permutation null (agreement-set 0/598), rather than validating a
   single method on the genes where it happens to concur.

3. **vs. MultiVeloVAE (Li et al. 2025 [2])** — reformulates the lag as continuous per-cell δ/κ and, like
   the others, presents it as a biological finding. It does not audit whether δ/κ agree with MultiVelo's
   or MoFlow's lag per gene. Our cross-method concordance analysis fills exactly that gap and includes
   this method as an arm.

4. **vs. the 2026 general benchmarks ([12,13])** — these establish that *velocity direction* is
   method-dependent and that no method wins everywhere. We are the multiome-lag-specific complement:
   direction can be broadly recoverable while the *timing offset between modalities* is not, and we show
   which derived quantities (α) survive the method swap and which (lag) do not.

5. **vs. the velocity-critique line (Bergen 2021 [9]; Gorin 2022 [10])** — we operationalize their general
   warnings into a single, decision-relevant negative result for the chromatin-lag use case, with a
   concrete downstream consequence (a drug-response-timing model must not consume a single-method lag; it
   should use the robust α / day0-ATAC→α path instead).

6. **vs. the velocity-identifiability line (Zhang 2024 [16]; Gu 2025 [17]; Wang 2025 [18]; BayVel [19])** —
   Zhang already shows the switch-time is weakly identified from the likelihood; Gu brings profile-likelihood
   to single-cell kinetic rates; Wang brings sloppy/stiff Fisher geometry to single cells. **Our §8 is not
   the first to note velocity-time flatness — we credit Zhang [16] head-on** — and stands as a *confirmatory
   mechanism* for our empirical result. The un-pre-empted contribution is the **dissociation** (lag/switch
   sloppy *while* α is stiff), the **curvature-ratio (κ_α/κ_lag)** framing, and the extension to the
   **chromatin→transcription lag** in multiome. §8 supports, but does not headline, the paper — the fresh
   thesis is the cross-method lag benchmark, not the identifiability geometry.

**One-paragraph gap/novelty statement.** Chromatin-informed velocity methods (MultiVelo, MultiVeloVAE,
MoFlow, CRAK-Velo) each report a gene-level chromatin→transcription lag as a biological readout, and the
priming literature (Ma et al. 2020) motivates it, but no study has asked whether that lag is *the same
quantity* across methods. General RNA-velocity benchmarks (2026) show velocity *direction* is
method-dependent yet do not evaluate the lag; the one incidental cross-method lag comparison (MoFlow vs
MultiVelo) reports agreement on a favorable subset rather than auditing reproducibility. We fill this gap
with a systematic multi-arm concordance benchmark plus a permutation-FDR agreement test and a causal
negative control, showing that the per-gene lag is not method-robust (agreement-set 0/598 at FDR<0.10)
and is model-structural rather than chromatin-driven, while transcription rate α and the day0-ATAC→α path
are robust — a distinction with direct consequences for any downstream timing-prediction model.

---

## References

Bibliographic detail verified against CrossRef/PubMed on 2026-07-05 unless flagged.

[1] Li C, Virgilio MC, Collins KL, Welch JD. **Multi-omic single-cell velocity models
epigenome–transcriptome interactions and improves cell fate prediction.** *Nature Biotechnology* 41,
387–398 (2023). doi:10.1038/s41587-022-01476-y. (PMC10246490)

[2] Li C, Gu Y, Virgilio MC, Lee KH, Collins KL, Welch JD. **Inferring differential dynamics from
multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE.** *Nature Communications*
16, article 11505 (2025). doi:10.1038/s41467-025-66287-6.

[3] Hong A, Lee S, Kim K. **Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription
regulation across cell states.** *Nature Communications* 17, article 566 (2025).
doi:10.1038/s41467-025-67259-6. (PMID 41457082; CrossRef and PubMed agree on vol 17 / art 566 despite the
2025 online date — early-access into the 2026 volume.)

[4] El Kazwini N, Gao M, Kouadri Boudjelthia I, Cai F, Huang Y, Sanguinetti G. **CRAK-Velo: chromatin
accessibility kinetics integration improves RNA velocity estimation.** *Genome Biology* 27(1) (2026).
doi:10.1186/s13059-026-04086-y. (PMID 42087173; bioRxiv 2024.09.12.612736.)

[5] **ArchVelo: archetypal velocity modeling for single-cell multi-omic trajectories.** *Nature
Communications* (2026). doi:10.1038/s41467-026-74000-4. ⚠️ *Author list not verified — confirm before
citing in submission.*

[6] Su M, et al. **scKINETICS: inference of regulatory velocity with single-cell transcriptomics data.**
*Bioinformatics* 39(Suppl 1), i394–i403 (2023). (PMC10311321) ⚠️ *First-author initials to confirm.*

[7] Gayoso A, Weiler P, Lotfollahi M, et al. **Deep generative modeling of transcriptional dynamics for
RNA velocity analysis in single cells.** *Nature Methods* 21, 50–59 (2024). doi:10.1038/s41592-023-01994-w.

[8] Gu Y, et al. **Bayesian inference of RNA velocity incorporating timepoints, lineage bifurcations, and
count data (veloVAE).** *PLOS Computational Biology* 22(3), e1014060 (2026).
doi:10.1371/journal.pcbi.1014060. ⚠️ *Full author list to confirm; distinct from MultiVeloVAE [2].*

[9] Bergen V, Soldatov RA, Kharchenko PV, Theis FJ. **RNA velocity — current challenges and future
perspectives.** *Molecular Systems Biology* 17(8), e10282 (2021). doi:10.15252/msb.202110282.

[10] Gorin G, Fang M, Chari T, Pachter L. **RNA velocity unraveled.** *PLOS Computational Biology* 18(9),
e1010492 (2022). doi:10.1371/journal.pcbi.1010492.

[11] Marot-Lassauzaie V, Bouman BJ, Donaghy FD, Demerdash Y, Essers MAG, Haghverdi L. **Towards reliable
quantification of cell state velocities.** *PLOS Computational Biology* 18(9), e1010031 (2022).
doi:10.1371/journal.pcbi.1010031. (PMC9550177) ⚠️ *Author list from record; confirm order.*

[12] **Benchmarking RNA velocity methods across 17 independent studies.** *Cell Reports Methods* (2026),
S2667-2375(26)00067-6. bioRxiv 2025.08.02.668272. ⚠️ *Author list/DOI to confirm at proof stage.*

[13] **Benchmarking algorithms for RNA velocity inference.** bioRxiv 2026.01.03.697314 (2026). ⚠️
*Preprint; author list/venue to confirm.*

[14] Ma S, Zhang B, LaFave LM, Earl AS, Chiang Z, Hu Y, Ding J, Brack A, Kartha VK, Tay T, Law T, Lareau
C, Hsu Y-C, Regev A, Buenrostro JD. **Chromatin Potential Identified by Shared Single-Cell Profiling of
RNA and Chromatin.** *Cell* 183(4), 1103–1116.e20 (2020). doi:10.1016/j.cell.2020.09.056.

[15] Trevino AE, Müller F, Andersen J, et al. **Chromatin and gene-regulatory dynamics of the developing
human cerebral cortex at single-cell resolution.** *Cell* 184(19), 5053–5069.e23 (2021).
doi:10.1016/j.cell.2021.07.039. (GSE162170.)

[16] Zhang et al. **Quantifying uncertainty in RNA velocity (ConsensusVelo).** bioRxiv 2024.05.14.594102
(2024); *Biometrics* (2026, in press). doi:10.1101/2024.05.14.594102. ⚠️ *Full author list/final venue to
confirm — closest prior art to §8; cite head-on.*

[17] Gu et al. **Profile-likelihood identifiability analysis of single-cell transcription (telegraph)
kinetics.** *Bioinformatics* 41(11), btaf581 (2025). doi:10.1093/bioinformatics/btaf581. ⚠️ *Exact
title/author list to confirm; distinct from the veloVAE Gu et al. [8].*

[18] Wang. **Sloppiness and Action Constraint in Cell State Transitions: Are Single Cells Sloppy?**
bioRxiv 2025.12.31.697145 (v2, 2025/2026). ⚠️ *Author list to confirm. Parameter space **confirmed**
(2026-07-10): sloppy/stiff Fisher analysis is on cell-state multivariate-Gaussian (μ,σ) coordinates, NOT
RNA-velocity kinetic parameters — methodological analog only.*

[19] **BayVel: A Bayesian Framework for RNA Velocity Estimation in Single-Cell Transcriptomics.**
arXiv:2505.03083 (2025). ⚠️ *Preprint; author list to confirm.*

---

### Sources (URLs consulted)
- MultiVelo: https://www.nature.com/articles/s41587-022-01476-y · https://pmc.ncbi.nlm.nih.gov/articles/PMC10246490/
- MultiVeloVAE: https://www.nature.com/articles/s41467-025-66287-6 · https://pmc.ncbi.nlm.nih.gov/articles/PMC12748740/
- MoFlow: https://www.nature.com/articles/s41467-025-67259-6 · https://pubmed.ncbi.nlm.nih.gov/41457082/
- CRAK-Velo: https://pubmed.ncbi.nlm.nih.gov/42087173/ · https://doi.org/10.1186/s13059-026-04086-y
- veloVI: https://www.nature.com/articles/s41592-023-01994-w
- veloVAE (RNA-only Bayesian): https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014060
- Bergen review: https://link.springer.com/article/10.15252/msb.202110282
- Gorin "RNA velocity unraveled": https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010492
- Marot-Lassauzaie: https://pmc.ncbi.nlm.nih.gov/articles/PMC9550177/
- Benchmark (17 studies): https://www.cell.com/cell-reports-methods/fulltext/S2667-2375(26)00067-6 · https://www.biorxiv.org/content/10.1101/2025.08.02.668272v1
- Benchmark (algorithms, 29): https://www.biorxiv.org/content/10.64898/2026.01.03.697314v1.full
- Chromatin potential (Ma): https://www.cell.com/cell/fulltext/S0092-8674(20)31253-8
- Zhang ConsensusVelo [16]: https://www.biorxiv.org/content/10.1101/2024.05.14.594102v1.full.pdf
- Gu profile-likelihood [17]: https://academic.oup.com/bioinformatics/article/41/11/btaf581/8300553
- Wang "Are Single Cells Sloppy?" [18]: https://www.biorxiv.org/content/10.64898/2025.12.31.697145v1
- BayVel [19]: https://arxiv.org/html/2505.03083v1
- Trevino cortex: https://doi.org/10.1016/j.cell.2021.07.039
- scKINETICS: https://academic.oup.com/bioinformatics/article/39/Supplement_1/i394/7210448
- ArchVelo: https://www.nature.com/articles/s41467-026-74000-4
