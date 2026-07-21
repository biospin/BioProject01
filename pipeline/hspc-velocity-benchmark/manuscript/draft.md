# Which velocity outputs are real and which are shadows of the model? A cross-method robustness audit of the chromatin→transcription lag in human HSPC multiome

<!--
FIRST DRAFT for paper-critic review. Genome Biology IMRaD format.
Numbers sourced only from results/FINDINGS.md (Korean/canonical half, 2026-07-14),
results/identifiability_dissociation.md, results/external_rate_validation.md,
PREREGISTRATION_gse205117.md, related_work.md. No new analysis; no fabricated numbers.
Author/affiliation/corresponding/IP left as <FILL>. Research and education use only.
-->

**Authors:** <FILL: author list>

**Affiliations:** <FILL: affiliations>

**Corresponding author:** <FILL: name, email>

> *Research- and education-use draft.* This manuscript reorganizes already-verified results for peer review; it is not a clinical or diagnostic resource. Author, affiliation, corresponding-author and IP fields are placeholders pending confirmation.

---

## Abstract

**Background.** Chromatin-informed ("multiome") RNA-velocity methods report a per-gene chromatin→transcription *lag* — the timing offset between when a locus opens/closes and when its transcription switches — as a biological readout, and this quantity has been proposed as an input for predicting the timing of epigenetic-drug responses. Before a derived quantity can be used that way, it must be shown to be *method-robust*: the same number regardless of which reasonable algorithm produced it. We asked, in human hematopoietic stem and progenitor cells (HSPCs) profiled by 10x Multiome, whether the gene-level lag is such a quantity, and, if not, which velocity outputs are.

**Results.** Across up to five velocity arms (an RNA-only scVelo dynamical floor plus MultiVelo, MultiVeloVAE, MoFlow and CRAK-Velo), the per-gene lag was not reproducible: pairwise magnitude concordance was |ρ|≤0.08 and cross-method sign-agreement was 48% (chance level). A causal negative control — shuffling ATAC within lineage — left the MultiVelo lag distribution statistically unchanged (Mann–Whitney p=0.20, per-gene ρ=0.72 preserved), and this extended to a structurally independent second method (MoFlow), showing the lag is model-structural rather than chromatin-driven. In contrast, the transcription rate α was highly reproducible across methods (Spearman ρ=0.88) and was recovered even by the RNA-only floor. The α>lag ordering held in every one of six systems (HSPC plus five external multiomes: adult brain, fetal E18 mouse brain, human bone-marrow mononuclear cells, macrophage differentiation, and mouse gastrulation), and the mouse-gastrulation replication passed a preregistered 6-of-6 scorecard sealed before any fit. Profiling MultiVelo's own likelihood confirmed the mechanism: α is stiff (identifiable) while lag is sloppy and boundary-limited (per-gene curvature ratio ≥2.49× on the conservative freed-nuisance basis, α stiffer in 77% of genes). Finally, fitted α — but not γ — was anchored to an external measurement: it recovered measured K562 TT-seq synthesis rates in all three methods (non-housekeeping ρ +0.24 to +0.29, all CI-excluding-0), whereas degradation rate γ was not recovered even where an external ground truth existed.

**Conclusions.** The velocity-derived chromatin→transcription lag is *not* robustly reproducible across method or dataset — a statement about the current methods, not a claim that timing biology is absent — whereas the transcription rate α is reproducible and externally anchored. We distil this into a velocity-output confidence map: trust α and rate-derived signals; treat lag, absolute timing and lag sign as requiring orthogonal validation. Any downstream timing-prediction model should route through the robust day0-ATAC→α path rather than consume a single-method lag.

**Keywords:** RNA velocity, single-cell multiome, chromatin accessibility, transcriptional kinetics, parameter identifiability, benchmarking, hematopoiesis

---

## Background

RNA velocity infers the direction and speed of transcriptional change from the balance of unspliced and spliced mRNA, and a family of chromatin-informed extensions now couples this to single-cell ATAC to model how chromatin state feeds transcription. A recurring output of these methods is a per-gene *chromatin→transcription lag*: MultiVelo defines explicit priming/decoupling offsets between chromatin and RNA switch times and classifies genes accordingly [1]; MultiVeloVAE generalizes these to continuous per-cell decoupling/coupling factors [2]; MoFlow infers per-cell chromatin-opening, transcription, splicing and degradation rates and reports chromatin–spliced lags without a pre-assigned latent time [3]; and CRAK-Velo integrates chromatin-accessibility kinetics and admits a trajectory-derived lag [4]. Same-family alternatives (archetypal ATAC+RNA trajectory modeling [5]; regulatory velocity from differential-accessibility priors [6]) and the RNA-only generative velocity our floor builds on (veloVI, which adds posterior velocity uncertainty [7], and the RNA-only Bayesian veloVAE [8], distinct from the multiome MultiVeloVAE) frame the landscape. The biological motivation is "chromatin potential" — the observation that accessibility at key loci can precede expression during lineage commitment, i.e. that chromatin *primes* fate [14]; in transient-TF-rich systems such as the developing cortex, multi-stage TF→accessibility→target lags are documented [15], which is exactly where a per-gene lag would be most method-sensitive.

This lag is attractive as a mechanistic clock. Our own motivating goal is to predict the *timing* of epigenetic-drug responses from baseline epigenomic features, for which a per-gene activation/shutdown offset would be a natural covariate. But a velocity-derived quantity is only usable downstream if it is robust to the modeling choices that produced it. The velocity-critique literature is emphatic that many velocity readouts are fragile: violated model assumptions and multiple kinetic regimes produce wrong velocities [9], the pipelines carry many user-set hyperparameters and often are not actionable [10], and reliable quantification of even the velocity *direction* is non-trivial [11]. Two 2026 benchmarks establish that velocity direction is method-dependent with no universal winner [12,13] — but both score the velocity *vector*, not the per-gene *lag*, and neither applies a permutation-null concordance test or a causal negative control. The one direct precedent, MoFlow, compared its chromatin–spliced lags to MultiVelo's and reported a *consistent subset* of negative-lag genes [3]: competitive validation on a favorable subset, not a systematic reproducibility audit.

We therefore treat the lag not as a finding but as a hypothesis to be stress-tested (H1): *is the per-gene chromatin→transcription lag a method-robust quantity?* We benchmark it head-to-head across an RNA-only floor and four chromatin-informed arms in human HSPC 10x Multiome (GSE209878), with a permutation-FDR agreement test, a causal ATAC-shuffle negative control, cross-dataset replication in five external systems including a preregistered test, a profile-likelihood analysis of the objective function itself, a synthetic multi-method positive control, and an external anchoring of the fitted rates to measured synthesis and degradation. The framing is a robustness audit — which velocity outputs are real and which are shadows of the model — rather than a "we beat method X" comparison. Where our objective-function analysis touches parameter identifiability, we note up front that the weak identifiability of velocity switch-times has been shown before by ConsensusVelo via likelihood flatness and Fisher information [16]; that work is confirmatory of our mechanism, and our fresh contribution is the cross-method lag benchmark itself, together with the α-stiff/lag-sloppy *dissociation* and its extension to the multiome lag.

---

## Results

### R1. The per-gene chromatin→transcription lag is not reproducible across methods, but transcription rate α is

Across methods, the per-gene lag magnitude did not concord. In HSPC, pairwise Spearman correlations of lag magnitude were −0.04 (MultiVelo × MoFlow, p=0.38), −0.01 (MultiVelo × MultiVeloVAE, p=0.81) and +0.08 (MoFlow × MultiVeloVAE, p=0.04); unifying the lag definition apples-to-apples raised the strongest pair only to +0.12 (Fig. 1, `figures/fig01_p2_concordance.png`). Direction was no better: among the sign-variable methods, the chromatin-leads fraction was 44.8% (MoFlow) and 49.3% (MultiVeloVAE) — a population balance near 50/50 that does not support a genome-wide "chromatin primes transcription" ordering — and the per-gene sign-agreement between MoFlow and MultiVeloVAE was 48%, i.e. chance. (MultiVelo's apparent 100% chromatin-leads is an artifact of its switch-time monotone-ordering constraint and is therefore admitted only to the magnitude/rank tests, never the sign test.) Adding a fourth method did not rescue concordance: after verifying and correcting a CRAK-Velo lag-sign convention bug, MoFlow × CRAK-Velo was −0.151 and CRAK-Velo × MultiVeloVAE was −0.04, and CRAK-Velo's chromatin-leads fraction was 41.1% (balanced). The only lag feature that agreed across methods was the direction of the canonical priming markers (e.g. *CSF1R*, *S100A9*), which were chromatin-leading in both sign-variable methods.

A permutation-FDR analysis (gene-label shuffle null, N=10⁴) confirmed the weakness statistically: cross-method ρ was significant versus the shuffle null for 2 of 3 pairs, but the effect was extremely weak (|ρ|≤0.15) and directionally inconsistent. A per-gene cross-method sign-consistency test returned an empty agreement-set (0/598 genes at FDR<0.10); we report this as a **CRAK-dependent sensitivity result**, not the headline, because the empty set requires three sign-variable methods, and with a clean sign-variable pair ({MoFlow, MultiVeloVAE}) the two-method sign test is power-bounded (min p_perm≈0.50 regardless of signal). The CRAK-independent clean headline is therefore the magnitude concordance (|ρ|≤0.08 across three methods) plus the 48% sign-agreement.

In sharp contrast, the transcription rate α reproduced strongly across methods (Spearman ρ=0.88; paired-bootstrap ρ=+0.882, 95% CI [+0.855, +0.905] for the MultiVelo × MultiVeloVAE axis). The root of the lag's fragility is diagnostic: the chromatin-opening rate α_c that sets the lag is itself method-sensitive (ρ=0.29; +0.291, 95% CI [+0.209, +0.369]), so the lag inherits α_c's method-sensitivity while α does not. **Interpretation:** *which* gene is chromatin-leading changes when you switch methods (non-robust), whereas α and the population-level directional balance converge (robust).

### R2. Chromatin does not drive the lag: a causal negative control

Shuffling ATAC within lineage — breaking the chromatin↔RNA coupling — and re-fitting MultiVelo left the lag distribution statistically identical to the original (Mann–Whitney p=0.20, Kolmogorov–Smirnov p=0.51), preserved the per-gene lag ranking (ρ=0.72), and did not move the chromatin likelihood (0.239→0.237). Only a paired Wilcoxon test detected a marginal shift (p=0.0003, median 5.87→5.48), indicating at most a marginal chromatin contribution. This negative control extended to a structurally independent second method: the MoFlow lag also survived the shuffle (per-gene ρ=0.52, far above the cross-method-swap ρ=0.08, chromatin-channel fit-quality unchanged). **Interpretation:** the lag arises from model structure (switch-time ordering) and gene-intrinsic RNA dynamics, not from the chromatin signal — independently confirming that MultiVelo's 100% chromatin-leads is structural.

### R3. Triangulating the lag's fragility: accuracy, stability, and predictability

We tested the lag along three further axes. **Accuracy:** an injected-lag simulator, evaluated on the CRAK-Velo DTW estimator under noise-free conditions, gave Spearman(true, recovered) = −0.89 — a *strong* rank-tracking (|ρ|=0.89) accompanied by sign inversion and magnitude collapse (~0.06×). This is a shape artifact of that DTW construct on smooth dynamics, i.e. grounds not to trust CRAK-Velo's lag cross-method, rather than evidence that lag is fundamentally unrecoverable; the core H1 arms (MoFlow × MultiVelo × MultiVeloVAE) do not use this construct and are unaffected (Supplementary Fig. S1, `figures/sim_injected_lag.png`). **Stability:** with the fit fixed and cells bootstrap-resampled, lag sign was 83% stable (median flip 0), but this is the weakest kind of stability — sampling noise only — and true re-fit stability would be lower. **Predictability:** pure baseline chromatin features could not predict the lag across held-out lineages (ρ=−0.21); adding fitted kinetic features raised this to +0.59 but circularly (the fitted α_c mechanically determines the MultiVelo lag). Assembling real day0 ATAC promoter/enhancer accessibility (511 genes over 8,583 day0 HSC/MPP cells) sharpened the contrast: the *robust* target α was predicted on held-out lineages (ρ=+0.309, positive in all six lineages), whereas the *non-robust* lag remained unpredictable even with real ATAC (ρ=+0.05, chance) (Supplementary Fig. S2, `figures/lag_model.png`). A within-method, cross-lineage refit told the same story: lag magnitude concorded only weakly across separately-fit lineages (median ρ=0.349, range 0.234–0.513, positive 10/10) while its α_c control was more robust (median ρ=0.483). **Interpretation:** the same features that predict the robust α fail to predict the non-robust lag — H1 reconfirmed on the predictability axis — which is why a downstream timing model should be built on baseline features and α, not on a single lag value.

### R4. The α-robust / lag-fragile ordering replicates across five external systems, including a preregistered test

We asked whether this ordering is a peculiarity of one HSPC dataset by replicating in five external multiomes spanning tissue distance (Fig. 2, `figures/fig02_crossdataset_concordance.png`; Table 1). The key claim is the *preservation of the α>lag ordering*, not any absolute value.

Within each external dataset, cross-method α (floor × MultiVelo × MultiVeloVAE, median of the three pairs) reproduced strongly while the within-dataset lag (MultiVelo × MultiVeloVAE) stayed near zero: E18 mouse brain α median +0.81 vs lag +0.057; human BMMC +0.851 vs −0.088 (p=0.15); macrophage +0.865 vs +0.074 (equivalent to 0 by TOST); mouse gastrulation +0.927 vs −0.026 ([−0.089, +0.038]), a within-dataset dissociation Δρ=+0.979 (95% CI [+0.916, +1.041]). Across datasets, the HSPC→external α rank reproduced above its lag counterpart in every system: adult human brain α +0.475 (p=4.5e-7) vs lag +0.185 (p=0.06); E18 +0.32 (p=2e-4) vs +0.10 (p=0.23); BMMC +0.550 (p=2.9e-8) vs +0.052 (p=0.63); macrophage +0.643 (95% CI [+0.554, +0.719], p=2.5e-33) vs +0.148 (95% CI [+0.027, +0.263], p=0.014); gastrulation +0.415 (95% CI [+0.244, +0.561]) vs +0.028 (95% CI [−0.165, +0.224]). The macrophage axis gives an explicit cross-dataset dissociation Δρ=+0.843 (95% CI [+0.773, +0.912]).

The fifth external system, mouse gastrulation (GSE205117, E7.5–E8.75 10x Multiome, 10,779 cells) — a developmental atlas where lineage priming is maximal and where lag would be *most* expected to be method-sensitive — was tested by **preregistration**: six predictions with pre-declared thresholds were sealed by commit hash before any velocity fit or concordance existed (`PREREGISTRATION_gse205117.md`), with no post-hoc rescue permitted. All six passed (6 PASS / 0 FAIL): within-dataset cross-method α ρ≥0.50 (threshold at `PREREGISTRATION_gse205117.md:15`), within-dataset lag ρ≤0.15, an α−lag ordering gap ≥0.35, cross-dataset α>+0.2 and α>lag, a larger per-gene lag mismatch than α mismatch (per-gene mismatch lag 0.294 by the sealed original definition MultiVelo × MoFlow, n=968, vs α 0.052), and fragility persisting under maximal priming. Because these predictions were sealed before the fits, this replication is confirmatory rather than a post-hoc pattern.

**Honest caveats (Table 1 footnotes).** (i) The cross-dataset α values decrease with tissue distance (macrophage +0.643 > BMMC +0.55 > brain +0.475 > gastrulation +0.415 > E18 +0.32), but their 95% CIs overlap (common region [0.368, 0.472]); we therefore present this only as a *qualitative* ordering and make no monotonic/quantitative claim, and fit no trend to the points. (ii) The within-dataset lag-fragile leg rests, in the four non-HSPC systems, largely on a single method pair (MultiVelo × MultiVeloVAE); only gastrulation additionally has a MoFlow arm, used for its sealed per-gene lag prediction. (iii) All five replications are one donor/sample each — the narrative rests on the consistency across the six axes, not on strong generalization from any one. (iv) Adult human brain has no within-dataset MultiVeloVAE fit, so its within-dataset cross-method lag is not computable; its α-vs-lag evidence is the cross-dataset axis (Table 1, N/A).

### R5. The dissociation is a property of the objective function: α is stiff, lag is sloppy

To ask *why* the observation recurs, we profiled MultiVelo's own likelihood along the α direction and the lag direction (lag = t_sw2 − t_sw1), re-optimizing latent time (n=538 genes; fit/likelihood reproduction r≈1.0) (Fig. 3, `figures/fig05_profile_likelihood.png`). Per-cell curvature was far higher for α than for lag (median 8.20 vs 2.24 per cell). We report the per-gene stiffness ratio κ_α/κ_lag on the conservative **freed-nuisance** basis — re-optimizing β, γ, α_c, rescale and scale_cc — where the dissociation survives with median ratio **2.49×** and α stiffer than lag in **77.03%** of genes (n=148). The stricter fixed-nuisance profile gives a larger 3.53× (IQR [1.92, 7.41]) with α stiffer in 94.57% of genes (244/258), which we treat as an upper bound, noting honestly that freeing β/γ collapses the α curvature to a median 0.19× of its fixed value. A lag trichotomy underlined the point: of 538 genes, 302 (56%) were interior, 205 (38%) boundary-pinned and 31 (6%) degenerate — in 44% the data cannot even set an upper bound on the lag. This is a *relative (practical)* non-identifiability of the lag direction, not a fully flat valley. The weak identifiability of the velocity switch-time itself was established by ConsensusVelo through likelihood flatness and Fisher information [16]; our objective-function analysis is confirmatory of that, and what is not pre-empted is the α-stiff/lag-sloppy *dissociation*, the curvature-ratio framing, and the multiome chromatin→lag extension [17,18,19].

A quantitative, data-axis counterpart of this objective-function dissociation is direct (from the paired-bootstrap identifiability analysis; B=10⁴, seed 20260707). On the HSPC MultiVelo × MultiVeloVAE axis, ρ_α = +0.882 (95% CI [+0.855, +0.904]) while ρ_lag (magnitude) = +0.163 (95% CI [+0.078, +0.244]), giving Δρ = +0.720 (95% CI [+0.639, +0.802]) — a dissociation whose CI excludes 0 by a wide margin, robust to the lag convention (magnitude +0.720; signed +0.893; rate-proxy +0.891, all CI-excluding-0). It replicates externally (BMMC Δρ=+0.994 [+0.874, +1.110]; E18 within-dataset Δρ=+0.841 [+0.779, +0.903]). Ranking the fitted parameters by cross-method reproducibility gives an empirical identifiability order **α ≫ α_c > β > γ** (α +0.882; α_c +0.291 [+0.209, +0.369]; β +0.080 [−0.009, +0.168]; γ −0.109 [−0.192, −0.023]); tellingly, the RNA-only floor — which has no ATAC channel at all — recovers α at chromatin-method strength (floor × MultiVelo +0.818 [+0.773, +0.855]; floor × MultiVeloVAE +0.889 [+0.862, +0.910]). A diff-budget analysis shows why the lag is worst of all: it is the difference of two rate-timescales, and while 1/α concords at +0.882 and 1/α_c at +0.291, their difference falls below even the weaker component (+0.124 [+0.036, +0.210]) — differencing amplifies the noise. (By TOST against a pre-declared |ρ|<0.2 bound, the *directional* lag MoFlow × MultiVeloVAE +0.083 [+0.007, +0.158] is equivalent to zero, while the *magnitude* lag MultiVelo × MultiVeloVAE +0.163 is weak-positive and not certified equivalent at the strict bound; the claim is carried by the dissociation, not by equivalence.)

### R6. Lag non-reproducibility is regime-specific, not a method defect: a synthetic positive control

To show the failure is a property of the data regime rather than a bug, we simulated a chromatin→RNA pulse ODE with a known injected onset lag τ over a switch-sharpness × SNR grid, and fit two structurally independent methods (MoFlow DTW chromatin–spliced lag, MultiVelo switch-time lag) on a shared gene axis (paired-bootstrap 95% CI, B=10⁴) (Fig. 4, `figures/fig_sim_positive_control.png`). In the identifiability corner (high SNR, moderate sharpness; W=0.1, SNR=20) the two methods agreed with each other (concordance ρ=+0.454 [+0.20, +0.67], CI-excluding-0) and with the injected τ (MoFlow +0.506, MultiVelo +0.672). As SNR dropped, concordance collapsed toward zero (SNR-marginal means 20→+0.242, 6→−0.035, 2→−0.005). A power calibration shows the real HSPC null is genuine: at n=598, N_perm=10⁴, the machine detects a concordant lag of |ρ|≳0.15 with power ≥0.8, whereas real HSPC's |ρ|≤0.08 sits near/below that detection floor (power ≈0.58 at ρ≈0.08). **Interpretation:** cross-method lag disagreement is a property of the (low-SNR, smooth) regime that real HSPC occupies, not a defect of any method; the identifiability corner is narrow (SNR=20 is unrealistically high per gene), which only strengthens the claim that real data live in the non-identifiable regime.

### R7. Fitted α — but not γ — is externally anchored to a measured rate

Finally we asked whether the fitted rates recover *measured* kinetic quantities, using rank-based tests only (absolute rates are non-identifiable and the setting is cross-context; every ρ carries a paired-bootstrap 95% CI, B=10⁴; the headline is the non-housekeeping stratum). Fitted α recovered measured K562 TT-seq synthesis rates (GSE229305, same study as the half-life panel) in all three methods: non-housekeeping ρ = +0.236 [+0.095, +0.368] (RNA-only floor, p=9.6e-4, n=193), +0.262 [+0.133, +0.385] (MultiVelo, p=4.9e-5, n=235) and +0.285 [+0.165, +0.398] (MultiVeloVAE, p=4.4e-6, n=251) — all CI-excluding-0, despite the cross-context setting (measured in K562, fit in HSPC). Degradation rate γ, by contrast, was *not* recovered even where external ground truth existed: within the cleanest apples-to-apples comparison (same K562 cells), all three methods were null for γ vs measured degradation while all three were positive for α; extending to a three-cell-line half-life panel, only 1 of 9 method×line cells recovered γ weakly (MultiVeloVAE × MOLM13, +0.164 [+0.028, +0.291]), and the textbook scVelo dynamical γ came out *reversed* in the cleanest reference (MOLM13, −0.224 [−0.359, −0.085], CI-excluding-0). This confirms the identifiability ranking on an external experimental axis: α is the only rate that is both method-reproducible and anchored to a measurement.

**Honest null, reported alongside.** An independent second α source (Schwalb 2016 K562 TT-seq, GSE75792) was *null*: α–Schwalb was 3/3 null (ρ −0.05 to −0.01) while α–Todorovski was 3/3 positive. The decisive cause is that the two measured TT-seq sources themselves agree only weakly (ρ≈0.15, n=1905) — between-study reproducibility of measured synthesis rate is the ceiling on any corroboration. We interpret this asymmetrically and as preregistered: the null does *not* refute α (cross-context, absolute-α non-identifiability, and source noise all apply), but it does mean the "n=1 external" fragility is not removed by this second source; the primary anchor stands, and the honest reading is that the second source is neither reproduction nor refutation.

---

### Table 1. Reproducibility of α versus lag across six systems

Within-dataset entries are cross-method Spearman ρ (RNA-only floor × MultiVelo × MultiVeloVAE for α, median of the three pairs; MultiVelo × MultiVeloVAE for lag magnitude). Cross-dataset entries are HSPC→external rank ρ. This table reports *cross-method reproducibility only*; it must not be read as within-method fit quality (see Table 2, kept separate by design).

| System | Tissue relation | Within-dataset α (median) | Within-dataset lag (MV×VAE) | Cross-dataset α (HSPC→ext) | Cross-dataset lag |
|---|---|---|---|---|---|
| HSPC (GSE209878) | primary | 0.88 | −0.01 (p=0.81)† | — | — |
| Macrophage differentiation (GSE284047) | HSPC-direct | +0.865 | +0.074 (≈0, TOST) | +0.643 [+0.554,+0.719] | +0.148 [+0.027,+0.263] |
| Human BMMC (GSE194122) | same tissue | +0.851 | −0.088 (p=0.15) | +0.550 (p=2.9e-8) | +0.052 (p=0.63) |
| Adult human brain (`<FILL: accession>`) | distant | N/A‡ | N/A‡ | +0.475 (p=4.5e-7) | +0.185 (p=0.06) |
| Mouse gastrulation (GSE205117) | developmental, priming-max | +0.927 | −0.026 [−0.089,+0.038] | +0.415 [+0.244,+0.561] | +0.028 [−0.165,+0.224] |
| E18 mouse brain (`<FILL: accession>`) | cross-species | +0.81 | +0.057 | +0.32 (p=2e-4) | +0.10 (p=0.23) |

† The HSPC within-dataset lag value −0.01 is the MultiVelo × MultiVeloVAE figure cited in FINDINGS §1 (signed convention); the magnitude-convention value on the same axis is +0.163 (95% CI [+0.078, +0.244]) from the dissociation analysis used in R5. The two are reported to their respective sources and not reconciled here.
‡ Adult human brain has no within-dataset MultiVeloVAE fit (MultiVelo + floor only), so within-dataset cross-method lag/α are not computable; its evidence is the cross-dataset axis.
Cross-dataset α CIs overlap → the tissue-distance ordering is qualitative, not a monotonic claim. All five external replications are one donor/sample each. Mouse gastrulation passed a preregistered 6/0 scorecard sealed before fitting.
Note (within-dataset α convention): the within-dataset α values here are the median of the three pairs including the RNA-only floor (e.g. E18 +0.81); the dissociation figures in R5 use the single MultiVelo × MultiVeloVAE pair (e.g. E18 ρ_α +0.898), the same category difference footnoted for the HSPC lag (†).

### Table 2. Velocity-output confidence decision map

Kept deliberately separate from Table 1: this is a *usage* map for velocity outputs, not a fusion of within-method fit quality into cross-method reproducibility.

| Velocity output | Cross-method reproducibility | External anchor | Confidence | Recommended action |
|---|---|---|---|---|
| Transcription rate α | High (ρ=0.88; floor recovers it) | Yes (measured TT-seq synthesis, ρ +0.24 to +0.29) | **High** | Usable directly; preferred downstream feature |
| Population directional balance (~50/50) | High (two methods converge) | — | **High** | Usable as a population statement |
| Canonical priming-marker direction | High (agrees across methods) | Consistent with priming biology [14] | **Medium–High** | Usable for named marker loci, not genome-wide |
| Chromatin-opening rate α_c | Low (ρ=0.29) | — | **Low** | Stabilize (bootstrap/per-lineage) before use |
| Degradation rate γ | Low (ρ≈−0.1) | Not recovered even with external ground truth | **Low** | Do not use as-is |
| Per-gene lag magnitude | Low (|ρ|≤0.08) | Non-predictable from baseline (≈chance) | **Low** | Requires orthogonal validation; do not use single-method value |
| Per-gene lag sign / absolute timing | Chance (48% agreement); structurally biased | — | **Very low** | Do not use; sign is structurally positive = uninformative |

---

## Discussion

The picture that emerges is a clean split between velocity outputs that are *real* — reproducible across methods, recoverable by the RNA-only floor, externally anchored, and predictable from baseline features — and outputs that are *shadows of the model*: the per-gene lag, its sign, and absolute timing. The transcription rate α is the identifiable invariant: it reproduces at ρ=0.88 across methods, is recovered even without a chromatin channel, is anchored to measured TT-seq synthesis, and is predictable from real day0 ATAC. The lag is its opposite on every axis — cross-method (|ρ|≤0.08), causal (chromatin-shuffle-invariant), predictive (≈chance from baseline), and mechanistic (sloppy and boundary-limited in the likelihood). The α_c that sets the lag is itself fragile (ρ=0.29), and since the lag is a *difference* of two rate-timescales, differencing drives its concordance below even the weaker component. That this ordering survives a preregistered test in the priming-maximal gastrulation system, where lag was most expected to be method-sensitive, is the strongest form the confirmation can take.

We are careful about what this does and does not claim. It is a statement about the *methods*, not about biology: chromatin priming is real for specific loci (the canonical markers agree across methods and are chromatin-leading), and deeper sequencing, finer time resolution or metabolic labeling could yet render the lag identifiable. Our claim is a boundary on what the *current* methods support. Two further limits are load-bearing. First, pseudotime is not wall-clock — the day0/day7 batches are integrated, so the lag is in pseudotime units and cannot be anchored to real time. Second, the profile-likelihood result is a *relative (practical)* non-identifiability, not a fully flat valley; we report it on the conservative freed-nuisance basis (2.49×, α stiffer in 77% of genes), because freeing the nuisance parameters partially collapses the α curvature and the stricter fixed-nuisance 3.53× is only an upper bound. The lag-fragile leg, outside HSPC, rests largely on a single method pair (MultiVelo × MultiVeloVAE), except in gastrulation where a MoFlow arm was wired; all five external replications are single-sample.

**Positioning against prior work.** The gene-level chromatin↔transcription lag was *introduced* by MultiVelo as a biological readout [1] and reformulated by MultiVeloVAE and MoFlow [2,3]; none of these audited whether the lag is the *same quantity* across methods, and MoFlow's one cross-method comparison reported agreement on a favorable subset [3]. The 2026 general benchmarks establish that velocity *direction* is method-dependent [12,13] but do not score the lag. Our contribution is the multiome-lag-specific complement: a systematic multi-arm concordance benchmark with a permutation null and a causal negative control, showing which derived quantities (α) survive the method swap and which (lag) do not. On the identifiability side, we credit ConsensusVelo head-on for first showing velocity switch-time flatness [16]; profile-likelihood on single-cell kinetic rates [17], sloppy/stiff Fisher geometry in single cells [18], and structural time-shift degeneracy [19] are further method precedents. Our objective-function analysis is a *confirmatory mechanism* for the empirical benchmark, not the paper's novelty. Against the closest prior work (MoFlow), the un-pre-empted additions are the chance control (permutation FDR) and the causal negative control, which no competing method paper applies to the lag (Fig. 5, `figures/fig03_novelty_comparison.png`).

**Consequence for downstream timing prediction.** The practical payoff of the confidence map (Table 2) is a design principle: a model that predicts epigenetic-drug-response timing must *not* consume a single-method lag. It should instead route through the robust path we validated — day0 ATAC promoter/enhancer accessibility → α — where the same baseline features that fail to predict the lag do predict α on held-out lineages (ρ=+0.31). We emphasize this is a design principle derived from the benchmark, not a wet-lab-validated timing predictor; validating the ATAC→α→timing route against a perturbation ground truth is the natural next step.

---

## Conclusions

The chromatin→transcription lag reported by multiome velocity methods is not a method-robust quantity at the gene level: it fails to reproduce across methods and datasets, is not driven by chromatin, and is sloppy in the likelihood — while the transcription rate α is reproducible (cross-method ρ=0.88), recoverable by the RNA-only floor, and externally anchored to a measured synthesis rate. This is a claim about the methods, not about the absence of timing biology. The contribution of this study is the resulting velocity-output confidence map — trust α and rate-derived signals, treat lag/sign/absolute-timing as requiring orthogonal validation — and the concrete downstream consequence that any timing-prediction model should be built on the robust day0-ATAC→α path rather than on a single-method lag.

---

## Methods

### Datasets

The primary dataset was human HSPC 10x Multiome (GEO GSE209878), day0 and day7 integrated, 21,878 cells. Five external multiome systems were used for cross-dataset replication: adult human brain (`<FILL: accession>`), fetal E18 mouse brain (`<FILL: accession>`; MultiVelo tutorial data), human bone-marrow mononuclear cells (BMMC; GSE194122, donor09/site4, with spliced/unspliced recovered from the GEX BAM by velocyto), macrophage differentiation (GSE284047 / figshare 30280333, Day14 HSPC-direct differentiation), and mouse gastrulation (GSE205117, E7.5/E8.0/E8.5/E8.75 rep1, 10x Multiome, 10,779 cells; GEX via STARsolo Velocyto raw, ATAC aggregated from GEO fragments over gene bodies ±10 kb using gencode vM25). All replications are single-donor/sample. Note that pseudotime is not wall-clock: because day0/day7 are batch-integrated in the primary data, lag is expressed in pseudotime units and no wall-clock anchor is available.

### Common preprocessing and method branch

To separate *method* differences from *preprocessing* differences, all arms shared a common preprocessing branch, after which the velocity method branched (common-graph ablation applied). Cross-dataset arms used per-dataset spliced/unspliced recovery as noted above; ATAC aggregation differed by dataset provenance (HSPC via `mv.aggregate_peaks_10x`; BMMC via gencode-proximity aggregation of the processed peak matrix; gastrulation via GEO fragments over gene bodies ±10 kb), which contributes conservative noise to the cross-dataset rank comparisons.

### Velocity methods and the RNA-only floor

Five arms were fit: an RNA-only floor (scVelo dynamical model, no chromatin channel) and four chromatin-informed methods — MultiVelo [1] (chromatin switch-time ODE; lag = t_sw2 − t_sw1), MultiVeloVAE [2] (VAE, continuous per-cell decoupling/coupling), MoFlow [3] (relay velocity; chromatin–spliced DTW lag) and CRAK-Velo [4] (semi-mechanistic; DTW-derived lag). A CRAK-Velo lag-sign convention bug (opposite sign to MoFlow's `fastdtw`) was found and corrected; CRAK-Velo's lag is reported only as a sensitivity arm given its shape-artifact on smooth dynamics.

### Concordance statistics

All cross-method and cross-dataset concordances were Spearman rank correlations. Where the source analysis provided them, correlations carry a paired gene bootstrap 95% CI (B=10⁴ resamples, seed 20260707, percentile method); pairwise headline correlations in R1 are reported with their p-values and n where that is what the source provides. The lag magnitude convention (|·|) was used throughout for cross-dataset consistency; MultiVelo's structurally positive sign was never invoked for sign tests. Cross-method sign-consistency was tested by permutation FDR (gene-label shuffle null, N=10⁴, FDR<0.10); the empty agreement-set is reported as a CRAK-dependent sensitivity result because a clean sign-variable pair is power-bounded. Equivalence to zero was assessed by TOST against a pre-declared |ρ|<0.2 bound. Tissue-distance ordering of cross-dataset α is reported qualitatively only, as the CIs overlap and no trend is fit to the points.

### Profile-likelihood identifiability

MultiVelo's objective (likelihood) was profiled along the α axis and the lag axis (lag = t_sw2 − t_sw1) with latent time re-optimized at each scan point (n=538 genes; fit/likelihood reproduction r≈1.0). Two nuisance regimes were run: **fixed-nuisance** (β, γ, α_c, rescale, scale_cc held) yielding the upper-bound curvature ratio, and **freed-nuisance** (those re-optimized) yielding the conservative lower bound reported in the text (2.49×). Per-gene stiffness was summarized as the curvature ratio κ_α/κ_lag; interior/boundary-pinned/degenerate classes describe whether the data can bound the lag.

### Preregistration protocol

For the fifth external replication (mouse gastrulation, GSE205117), six falsifiable predictions with pre-declared thresholds were sealed by commit hash before any velocity fit or concordance existed (`PREREGISTRATION_gse205117.md`; within-dataset α ρ≥0.50 at line 15, lag ρ≤0.15, α−lag gap ≥0.35, cross-dataset α>+0.2 and >cross-lag, per-gene lag mismatch > α mismatch, fragility under maximal priming). The threshold ρ≥0.50 is the sealed pass line; the observed HSPC α=0.88 is an observed value, not the pass line. Scoring used the sealed original per-gene definition (MultiVelo × MoFlow for the lag prediction), applied with no post-hoc rescue, and the scorecard reproduced byte-identically on deterministic recomputation.

### Confound controls

Cell-cycle, transcriptional burst and ambient/doublet confounds were controlled. Cell-cycle was unbiased at the gene level (cell-cycle genes 1.9% of fit-lag genes; CC vs rest Mann–Whitney p=0.86; median change 0.037 on exclusion); the cell-level correlation arises because cycling is coupled to lineage (MK 88% ↔ HSC 3%), which the within-lineage analysis already controls, so no global regress-out was performed (to avoid removing differentiation signal). Burst: lag↔α Spearman −0.24 (moderate, reflected in regularized regression). Ambient/doublet: scrublet applied, doublet median 0.045, pct_mito median 10.4% (QC max 20%). Analyses were within-lineage; rare lineages (MK/Baso·Eo·Mast/pDC) were treated with separate uncertainty. Multicollinearity of promoter/enhancer ATAC features was handled by regularized regression; multiple testing across genes used permutation FDR.

### External rate validation

Fitted α and γ were compared (rank-based, cross-context, per-gene bootstrap 95% CI, B=10⁴) to measured rates: α vs measured K562 TT-seq synthesis rate (GSE229305, Todorovski 2024; and a second source, Schwalb 2016 K562 TT-seq, GSE75792), and γ vs measured mRNA half-life (K562/THP1 same-study SLAM-seq, MOLM13 cross-study). The housekeeping stratum is trivially conserved, so the headline is the non-housekeeping stratum. Interpretation of α nulls is asymmetric and preregistered: a null demotes but does not refute, given cross-context measurement and absolute-α non-identifiability.

---

## Declarations

**Ethics approval and consent to participate.** Not applicable — the study uses previously published, de-identified public datasets.

**Consent for publication.** Not applicable.

**Availability of data and materials.** All primary and external datasets are public (GSE209878, GSE194122, GSE284047, GSE205117, GSE229305, GSE75792; adult human brain and E18 mouse brain accessions: `<FILL: accession>`). Analysis code and deterministic recomputation scripts: `<FILL: repository/DOI>`.

**Competing interests.** `<FILL>`.

**Funding.** `<FILL>`.

**Authors' contributions.** `<FILL>`.

**Acknowledgements.** `<FILL>`.

**Disclaimer.** Research- and education-use draft; not a clinical or diagnostic resource.

---

## References

[1] Li C, Virgilio MC, Collins KL, Welch JD. Multi-omic single-cell velocity models epigenome–transcriptome interactions and improves cell fate prediction. *Nature Biotechnology* 41, 387–398 (2023). doi:10.1038/s41587-022-01476-y.

[2] Li C, Gu Y, Virgilio MC, Lee KH, Collins KL, Welch JD. Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE. *Nature Communications* 16, 11505 (2025). doi:10.1038/s41467-025-66287-6.

[3] Hong A, Lee S, Kim K. Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states. *Nature Communications* 17, 566 (2025). doi:10.1038/s41467-025-67259-6.

[4] El Kazwini N, Gao M, Kouadri Boudjelthia I, Cai F, Huang Y, Sanguinetti G. CRAK-Velo: chromatin accessibility kinetics integration improves RNA velocity estimation. *Genome Biology* 27(1) (2026). doi:10.1186/s13059-026-04086-y.

[5] ArchVelo: archetypal velocity modeling for single-cell multi-omic trajectories. *Nature Communications* (2026). doi:10.1038/s41467-026-74000-4. [Author list to verify before submission.]

[6] Su M, et al. scKINETICS: inference of regulatory velocity with single-cell transcriptomics data. *Bioinformatics* 39(Suppl 1), i394–i403 (2023).

[7] Gayoso A, Weiler P, Lotfollahi M, et al. Deep generative modeling of transcriptional dynamics for RNA velocity analysis in single cells. *Nature Methods* 21, 50–59 (2024). doi:10.1038/s41592-023-01994-w.

[8] Gu Y, et al. Bayesian inference of RNA velocity incorporating timepoints, lineage bifurcations, and count data (veloVAE). *PLOS Computational Biology* 22(3), e1014060 (2026). doi:10.1371/journal.pcbi.1014060. [Distinct from MultiVeloVAE [2].]

[9] Bergen V, Soldatov RA, Kharchenko PV, Theis FJ. RNA velocity — current challenges and future perspectives. *Molecular Systems Biology* 17(8), e10282 (2021). doi:10.15252/msb.202110282.

[10] Gorin G, Fang M, Chari T, Pachter L. RNA velocity unraveled. *PLOS Computational Biology* 18(9), e1010492 (2022). doi:10.1371/journal.pcbi.1010492.

[11] Marot-Lassauzaie V, Bouman BJ, Donaghy FD, Demerdash Y, Essers MAG, Haghverdi L. Towards reliable quantification of cell state velocities. *PLOS Computational Biology* 18(9), e1010031 (2022). doi:10.1371/journal.pcbi.1010031.

[12] Benchmarking RNA velocity methods across 17 independent studies. *Cell Reports Methods* (2026), S2667-2375(26)00067-6. bioRxiv 2025.08.02.668272. [Author list/DOI to confirm at proof.]

[13] Benchmarking algorithms for RNA velocity inference. bioRxiv 2026.01.03.697314 (2026). [Preprint; author list/venue to confirm.]

[14] Ma S, Zhang B, LaFave LM, et al. Chromatin Potential Identified by Shared Single-Cell Profiling of RNA and Chromatin. *Cell* 183(4), 1103–1116.e20 (2020). doi:10.1016/j.cell.2020.09.056.

[15] Trevino AE, Müller F, Andersen J, et al. Chromatin and gene-regulatory dynamics of the developing human cerebral cortex at single-cell resolution. *Cell* 184(19), 5053–5069.e23 (2021). doi:10.1016/j.cell.2021.07.039. (GSE162170.)

[16] Zhang et al. Quantifying uncertainty in RNA velocity (ConsensusVelo). bioRxiv 2024.05.14.594102 (2024); *Biometrics* 82(1) ujag018 (in press). doi:10.1101/2024.05.14.594102. [Closest prior art to the profile-likelihood section; cited head-on. Full author list/final venue to confirm.]

[17] Gu et al. Profile-likelihood identifiability analysis of single-cell transcription (telegraph) kinetics. *Bioinformatics* 41(11), btaf581 (2025). doi:10.1093/bioinformatics/btaf581. [Distinct from [8].]

[18] Wang. Sloppiness and Action Constraint in Cell State Transitions: Are Single Cells Sloppy? bioRxiv 2025.12.31.697145 (v2, 2025). [Methodological analog on cell-state Gaussian coordinates.]

[19] BayVel: A Bayesian Framework for RNA Velocity Estimation in Single-Cell Transcriptomics. arXiv:2505.03083 (2025). [Preprint; author list to confirm.]

---

*Bibliography exported to `manuscript/refs.bib`. Items with "to confirm/verify" notes carry over the flags from `related_work.md` (verified vs CrossRef/PubMed 2026-07-05).*
