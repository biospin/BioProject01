<!--
════════════════════════════════════════════════════════════════════════
내부 메모 (제출 전 제거): 출처, 범위, 미확정
════════════════════════════════════════════════════════════════════════
학회: ML4H 2026, Findings track (non-archival). 마감 2026-09-10 23:59 AoE (= 2026-09-11 20:59 KST).
분량 규약: 본문 4페이지, 참고문헌·부록 무제한. 이 파일의 본문(제목~Conclusion)은 조판 여유를 두고
  보수적으로 잡았다. 조판에서 넘치면 산문을 더 줄이지 말고 Table 1의 각주와 Appendix로 더 내린다.
이중맹검: 저자·소속·이메일·CRediT·Acknowledgements·사사·저장소 URL·서버 경로 전부 제거. 자기 인용 없음.
정본(수정 금지, 읽기만): ../draft_v2.md, ../../results/FINDINGS.md, ../PAPER_DIRECTION.md.
선례: ../CONF_LONGABSTRACT_GIW2026_BIOP01.md (2p GIW long abstract), ../conf_giw2026/md2tex.py.

수치 출처(전부 정본 실측, 지어낸 값 없음):
- 본문 수치는 draft_v2.md Results/Discussion/Methods 및 results/*.md에 실재하는 값만 옮겼다.
- P5c(모형 계열 견고성) = results/atac_alpha_model_class_check.md. **탐색적** 상태이므로 Limitations에만 쓰고
  Results로 승격하지 않았다.

claim 등급 준수(PAPER_DIRECTION §2):
- 인과 진술은 HSPC 한정, 행렬 층은 MultiVelo 한정으로 못 박았다.
- 곡률-외부검증 연결은 suggestive supporting으로만 기술(헤드라인 아님).
- 사전등록 통과선 = Spearman ρ≥0.50(봉인). HSPC α=0.88은 관측값이지 통과선이 아니라고 두 곳에 명시.
- named marker 방향 일치는 correlational only(marker-shuffle NULL, p=0.58).

그림: Figure 1만 렌더본 존재(figures/fig01_p2_concordance.png). 신뢰지도 그림(fig07)은 재렌더 필요이며,
  4페이지 제약과 Table 2 중복을 고려해 본문에서 참조하지 않는다. 나머지 fig02~fig06, fig08도 협업 서버
  소멸로 재렌더 대상이지만 이 제출본은 참조하지 않는다.
LaTeX 변환기(conf_giw2026/md2tex.py 재사용) 주의: 본문에 남은 비-ASCII는
  ± × ü Δ α β γ κ ρ τ ⁴ − ≈ ≤ ≥ ≫ ≳ 이다. GIW 변환표에 없는 κ, τ, ≫, ≳, ü를 매크로에 추가해야 한다.
분량: 본문(제목~Figure legend) 3,905단어(표 2개 409단어 포함), Appendix 2,070단어, 참고문헌 33건.
════════════════════════════════════════════════════════════════════════
-->

# A reliability map for per-gene multiome RNA velocity parameters in single-cell kinetics

*(ML4H 2026, Findings track. Anonymized for double-blind review: authors, affiliations, funding and code repository are withheld.)*

## Abstract

Chromatin-informed ("multiome") RNA velocity models emit several per-gene quantities that are increasingly consumed downstream as biomedical features: a transcription rate α, a degradation rate γ, and a chromatin-to-transcription *lag* offered as a mechanistic clock for regulatory timing. A derived quantity is usable as a feature only if it is reliable, and reliability is testable. We audit these outputs on four axes in human hematopoietic stem and progenitor cells (HSPCs; 10x Multiome, GSE209878, 21,878 cells) across five velocity arms that share a common preprocessing branch, so that method differences are not preprocessing artefacts: cross-method reproducibility, an ATAC-shuffle intervention, replication in five external multiomes (one preregistered), and anchoring to metabolically measured synthesis and degradation rates. Among continuous per-gene kinetic parameters only α reproduced across methods (Spearman ρ=0.88, observed); the lag reproduced weakly at best (strongest pair +0.163, most pairs |ρ|≤0.08) with 54.6% sign agreement, and γ neither reproduced (ρ≈−0.1) nor recovered a measured half-life. Profile-likelihood analysis indicates why: α is stiff along the objective while the lag is sloppy and boundary-limited. We distil the axes into a reliability map with an explicit routing rule for downstream models. Research and education use only; not clinical.

**Keywords:** reliability of model-derived features, RNA velocity, single-cell multiome, parameter identifiability, external validation, hematopoiesis

## 1. Introduction

Single-cell models are now routinely used as feature extractors for downstream biomedical prediction, and RNA velocity is a prominent case. Velocity infers the direction and speed of transcriptional change from the balance of unspliced and spliced mRNA [1,2], and a family of chromatin-informed extensions couples this to single-cell ATAC. These models do not emit a single number. Each fits a transcription rate α, a splicing rate β, a degradation rate γ, and, in the multiome variants, a per-gene chromatin-to-transcription lag. MultiVelo defines explicit priming and decoupling offsets between chromatin and RNA switch times [3], MultiVeloVAE generalizes these to continuous per-cell decoupling and coupling factors [4], MoFlow reports chromatin-spliced lags from per-cell rates [5], and CRAK-Velo admits a trajectory-derived lag [6].

The lag is the most attractive of these outputs for health applications, because it promises a per-gene clock: which genes open chromatin ahead of transcription, and therefore how quickly a locus can respond. The motivating task here is predicting the *timing* of an epigenetic-drug response in hematopoietic cells from baseline epigenomic features, for which a per-gene activation or shutdown offset would be a natural covariate.

A derived quantity is usable as a feature only if it is reliable, and reliability has two faces that are usually tested apart. The internal face asks whether the same number appears when a different reasonable algorithm is run on the *same* cells. The velocity-critique literature is emphatic that many readouts fail even this, since violated model assumptions and multiple kinetic regimes produce wrong velocities [21,22] and reliable quantification of even the velocity direction is non-trivial [23]. Three 2026 benchmarks establish that velocity direction is method-dependent with no universal winner [25,26,27], and a fourth comparison reports per-gene driver rankings to be method-dependent [28]. All of them score the velocity *vector* in a low-dimensional embedding or as transition probabilities; none sorts the individual per-gene outputs by reliability, applies a permutation-null concordance test, or perturbs the chromatin input and re-fits. The one task among them named "negative control robustness" [27] scores whether a method emits spuriously non-zero velocity on static cells, which is output plausibility rather than chromatin causality. The external face asks whether a fitted rate recovers an *independently measured* kinetic quantity. Metabolic-labeling assays (TT-seq for synthesis, SLAM-seq half-lives for degradation) [30,31] make this test possible for two of the rates, and it is the stronger bar, because a quantity can reproduce across methods and still be a shared artefact.

The failure mode we address is narrower than outright irreproducibility, and we suspect it is more common: a derived quantity is introduced and demonstrated on illustrative loci, and is then consumed downstream at a per-gene quantitative level at which its reliability was never tested. We therefore treat velocity outputs not as findings but as candidates to be sorted. The contribution of this study is a four-axis reliability protocol and the resulting **reliability map**, which tells an analyst which velocity outputs may enter a downstream model directly, which need an explicit baseline, and which require orthogonal validation first. Where our objective-function analysis touches identifiability we note up front that the weak identifiability of velocity switch-times was shown previously by ConsensusVelo through likelihood flatness and Fisher information [41]; that work is confirmatory of our mechanism, and what is new here is the α-stiff, lag-sloppy *dissociation* and the map built on it.

## 2. Methods

**Data and arms.** The primary dataset is human HSPC 10x Multiome (GSE209878), day0 and day7 integrated, 21,878 cells. Five velocity arms were fit: an RNA-only floor (scVelo dynamical [66], no chromatin channel) and four chromatin-informed methods, MultiVelo [3], MultiVeloVAE [4], MoFlow [5] and CRAK-Velo [6]. All arms branch from a common preprocessing pipeline with a common-graph ablation, so method differences are not preprocessing differences. Pseudotime is not wall-clock: day0 and day7 are batch-integrated, so the lag is expressed in pseudotime units. Five external multiomes were used for replication: human fetal cortex (GSE162170) [19], fetal E18 mouse brain (10x demo, no accession), human BMMC (GSE194122), macrophage differentiation (GSE284047) and mouse gastrulation (GSE205117), each a single donor or sample (Appendix A).

Each per-gene output was then tested on four axes.

**Axis 1, cross-method reproducibility.** Pairwise Spearman rank agreement between arms on a shared gene axis, with paired gene-bootstrap 95% confidence intervals (B=10⁴) and a gene-label permutation-FDR agreement test (N=10⁴, FDR<0.10) [67]; equivalence to zero was assessed by TOST against a pre-declared |ρ|<0.2 bound [48]. The lag is reported under one convention per test, magnitude for the headline metric and signed as a sensitivity value, because signing near-zero, sign-unstable lags lets opposing signs cancel. Genes whose lag is exactly zero have undetermined direction and are excluded from sign statistics. MultiVelo's sign is structurally constrained positive by its switch-time ordering, so it enters magnitude and rank tests but never sign tests (Appendix B).

**Axis 2, ATAC-shuffle intervention.** Within each lineage the ATAC signal was permuted, breaking the chromatin-to-RNA coupling, and the model was re-fit; the resulting lag distribution was compared to the original by Mann-Whitney, Kolmogorov-Smirnov and paired Wilcoxon tests and by per-gene Spearman ρ, for MultiVelo and independently for MoFlow. A marker-level variant asks whether the cross-method direction agreement of canonical priming markers is *caused* by chromatin at those loci, comparing marker and bulk shuffle-induced change on a bias-corrected relative scale.

**Axis 3, cross-dataset replication.** The α-over-lag ordering was re-tested within each external dataset and along the HSPC-to-external gene axis. The fifth external system (mouse gastrulation, a developmental atlas where lineage priming is maximal and a lag would be *most* expected to be method-sensitive) was tested by preregistration [49]: six predictions with pre-declared thresholds were sealed by commit hash before any velocity fit or concordance existed, with no post-hoc rescue permitted. The sealed pass line for within-dataset cross-method α is Spearman ρ≥0.50; the HSPC α=0.88 reported below is an *observed* value and was never the pass line.

**Axis 4, external measurement anchor.** Only two of the fitted quantities have a measured external counterpart at all, so this axis tests exactly those two: fitted α against measured K562 TT-seq synthesis rate (GSE229305 [50]; second source GSE75792 [30]) and fitted γ against measured mRNA half-life by SLAM-seq [31] from the same metabolic-labeling study. Tests are rank-based with paired bootstrap intervals, absolute rates being non-identifiable and the setting cross-context; the headline stratum is non-housekeeping. Transcript abundance was carried throughout as a competing baseline, because measured synthesis equals abundance times the degradation constant.

Confound controls for cell cycle, transcriptional burst and ambient RNA or doublets, the enrichment protocol with a fit-restricted custom background, and the cell-level velocity-matrix audit are given in Appendices A, D and G.

## 3. Results

### 3.1 Only the transcription rate α reproduces across methods

In HSPC the per-gene lag did not concord. Under its original signed definition the three pairwise Spearman correlations were −0.04 (MultiVelo versus MoFlow, p=0.38), −0.01 (MultiVelo versus MultiVeloVAE, p=0.81) and +0.08 (MoFlow versus MultiVeloVAE, p=0.04). Unifying the lag definition raised the strongest pair only to +0.12, and under the magnitude convention that same pair reaches +0.163 (95% CI [+0.078, +0.244], excluding 0), with most pairs at |ρ|≤0.08 (Figure 1). Direction was little better. Among the sign-variable methods the chromatin-leads fraction was balanced near 50/50 (MoFlow 44.8%, MultiVeloVAE 49.3%, CRAK-Velo 41.1%), which does not support a genome-wide "chromatin primes transcription" ordering, and per-gene sign agreement between MoFlow and MultiVeloVAE was 54.6% after excluding zero-lag genes (n=560; binomial p=0.03 against chance), a statistically detectable but practically negligible excess. A fourth method did not rescue concordance: after correcting a CRAK-Velo lag-sign convention bug, MoFlow versus CRAK-Velo was −0.151 and CRAK-Velo versus MultiVeloVAE was −0.04. Of the 640 genes with at least two sign-variable calls only 38.6% were unanimous. Restricting to well-determined genes did not recover a usable rule: agreement rises with α (Spearman +0.25, p=4e-09), yet even the top α decile is only 31.5% unanimous.

In sharp contrast, α reproduced strongly (Spearman ρ=0.88 observed; paired bootstrap +0.882, 95% CI [+0.855, +0.905] on the MultiVelo versus MultiVeloVAE axis) and was recovered even by the RNA-only floor, which has no chromatin channel at all (floor versus MultiVelo +0.818 [+0.773, +0.855]; floor versus MultiVeloVAE +0.889 [+0.862, +0.910]). Ranking all fitted parameters by cross-method reproducibility gives an empirical order α ≫ α_c > β > γ (α +0.882; α_c +0.291 [+0.209, +0.369]; β +0.080 [−0.009, +0.168]; γ −0.109 [−0.192, −0.023]). The lag inherits the fragility of α_c, which sets it, while α does not, and because the lag is a *difference* of two rate timescales its concordance (+0.124 [+0.036, +0.210] for the reconstructed difference) falls below even the weaker component. Table 1 gives the per-parameter summary.


### 3.2 The lag is largely preserved under an ATAC-shuffle intervention

Shuffling ATAC within lineage and re-fitting MultiVelo left no detectable difference in the unpaired lag distribution (Mann-Whitney p=0.20, Kolmogorov-Smirnov p=0.51), preserved much of the per-gene lag ranking (ρ=0.72) and barely moved the chromatin likelihood (0.239 to 0.237). A paired Wilcoxon test nevertheless detected a small shift (p=0.0003, median 5.87 to 5.48), so the lag is not literally invariant and a limited chromatin contribution remains possible. The control extended to a structurally independent second method, the MoFlow lag likewise retaining rank signal after the shuffle (per-gene ρ=0.52, against a cross-method-swap ρ=0.08). Under this intervention the fitted lag is predominantly preserved by model structure, including switch-time ordering, and by gene-intrinsic RNA dynamics, rather than being wholly determined by the chromatin signal, which is also why MultiVelo's apparent 100% chromatin-leads is structural.

The marker corollary is null. Canonical priming markers are the one place where methods do agree on direction (*MPO*, *ELANE*, *AZU1*, *LYZ* and *S100A9* chromatin-leading wherever scored, *MEIS1* RNA-leading, *CSF1R*, *HLF* and *CRHBP* split; Appendix D), so we asked whether chromatin causes that agreement. On a bias-corrected relative-change scale these markers moved no more than bulk genes under the shuffle (marker median 0.137 versus bulk 0.144; Mann-Whitney for marker>bulk p=0.58), and the larger absolute movements of some markers tracked their larger baseline lag rather than chromatin (|Δlag| correlated with lag magnitude, ρ=+0.24). Their direction agreement is therefore descriptive, not causal, and it did not replicate outside HSPC (gastrulation per-gene agreement 50.6%, n=1,061, binomial p=0.71). These causal statements are bounded to HSPC and to this shuffle design.

### 3.3 The ordering replicates across five external systems, one of them preregistered

Within each external dataset, cross-method α reproduced strongly while the within-dataset lag magnitude stayed near zero: E18 mouse brain α median +0.810 versus lag +0.057 [−0.005, +0.118]; human BMMC +0.851 versus −0.088 [−0.209, +0.034]; macrophage +0.865 versus +0.074 [+0.006, +0.143] (equivalent to zero by TOST); mouse gastrulation +0.927 versus −0.026 [−0.089, +0.038]. A structurally independent MoFlow lag pair, added to four of these systems, stayed near zero throughout (all |ρ|≤0.12), so the near-zero within-dataset lag does not depend on the MultiVelo versus MultiVeloVAE pairing. Along the HSPC-to-external gene axis, α outranked its lag counterpart in every system: macrophage +0.643 [+0.554, +0.719] versus +0.148 [+0.027, +0.263]; BMMC +0.550 versus +0.052; human fetal cortex +0.475 (p=4.5e-7) versus +0.185 (p=0.06); gastrulation +0.415 versus +0.028; E18 +0.321 versus +0.105 (Appendix C, Table A1). The cross-dataset α values decrease with tissue distance, but their intervals overlap, so we present that ordering qualitatively and fit no trend.

The gastrulation test was preregistered and passed six of six sealed predictions with no post-hoc rescue (Appendix I). Its sealed pass line for within-dataset cross-method α was ρ≥0.50, which is distinct from the observed HSPC value of 0.88. This is a preregistered confirmatory test of that six-item scorecard, not a claim that all six systems were preregistered.

### 3.4 α agrees with a measured rate, though not α-specifically; γ does not

Fitted α tracked the measured K562 TT-seq synthesis rate in all three methods that were scored: non-housekeeping ρ=+0.236 [+0.095, +0.368] (RNA-only floor, n=193), +0.262 [+0.133, +0.385] (MultiVelo, n=235) and +0.285 [+0.165, +0.398] (MultiVeloVAE, n=251), all intervals excluding zero despite the cross-context setting. We are deliberate about what this establishes. Measured synthesis carries steady-state abundance as a multiplicative factor, and abundance tracks the same measurement at least as strongly as α does (Spearman(abundance, synthesis)=+0.410 versus Spearman(α, synthesis)=+0.262), so the external match is *consistency evidence*, not a claim that α is the most accurate synthesis estimator. Two independent methods agree on α (+0.882) somewhat more than α resembles abundance (+0.809), leaving a small reproducible kinetic component, but shared inputs or model form could also produce that gap. A second measured source (GSE75792) was null for all three methods (ρ −0.05 to −0.01), the decisive cause being that the two measured TT-seq sources agree only at ρ≈0.15 (n=1,905), which caps any corroboration.

γ behaved differently. In the cleanest same-cell comparison all three methods were null against measured K562 degradation (−0.118, +0.053, −0.011) while all three were positive for α, and across a three-cell-line half-life panel only 1 of 9 method-by-line cells recovered γ weakly. The RNA-only scVelo γ came out *reversed* in the uncensored reference (MOLM13, −0.224 [−0.359, −0.085]), genes with larger fitted γ having longer measured half-lives; that reversal is a property of the scVelo γ and is attributed to that method only.

### 3.5 The dissociation is a property of the objective function

Profiling MultiVelo's own likelihood along the α direction and the lag direction (lag = t_sw2 − t_sw1), with latent time re-optimized (n=538 genes), gives far higher per-cell curvature for α than for the lag (median 8.20 versus 2.24). On the conservative freed-nuisance basis, re-optimizing β, γ, α_c, rescale and scale_cc, the dissociation survives at a median stiffness ratio κ_α/κ_lag=2.49×, with α stiffer in 77.03% of genes (n=148); the stricter fixed-nuisance profile gives 3.53× and 94.57%, which we treat as an upper bound. A lag trichotomy underlines the point: of 538 genes, 302 (56%) are interior, 205 (38%) boundary-pinned and 31 (6%) degenerate, so in 44% the data cannot set even an upper bound on the lag. This is *relative (practical)* non-identifiability [51,52,53], not a fully flat valley; it confirms the switch-time flatness reported by ConsensusVelo [41] and adds the α-versus-lag dissociation. Whether internal stiffness *predicts* external validation is only suggestive supporting evidence and no part of the map rests on it: across α stiffness tertiles the direction is monotone as predicted (0.116, 0.153, 0.302) and only the top tertile clears zero (+0.302 [+0.068, +0.511]), but the decisive high-minus-low contrast is not significant (Δρ=+0.186 [−0.149, +0.504], n=70 per tertile) and the γ leg shows no gradient. A synthetic positive control confirms that the failure is regime-specific rather than a method defect (Appendix F).

One layer up, the cell×gene velocity matrix that every method emits before any embedding projection reproduces no better: on the 21,878 cells and 354 genes usable in all five arms, multiome pairs agreed *less* with each other (−0.139) than with the RNA-only floor (+0.080), a paired Δ of −0.206 [−0.207, −0.205] opposite to the preregistered expectation, and the same ordering held in four of four external systems. That layer is a different target from the per-gene lag, its numbers are kept separate, and there destroying the chromatin channel does move the output by a small, bounded amount, a statement restricted to HSPC and to MultiVelo (Appendix G).

### 3.6 The reliability map and its routing rule

Assembling the axes gives a single usage statement (Table 2). Exactly one continuous per-gene kinetic parameter is reproducible on the internal axis and corroborated on the external axis: the transcription rate α. The population directional balance near 50/50 is usable as a population statement. Everything else is unreliable for direct per-gene use: α_c (ρ=0.29), γ (ρ≈−0.1 and not externally recovered), the lag magnitude (most pairs |ρ|≤0.08) and the lag sign and absolute timing (54.6%). The routing rule follows. A downstream model may consume α, but only against an explicit abundance baseline, because α is largely expression and adds no demonstrable synthesis information beyond it; every other rate-derived signal needs output-specific validation; and a single-method lag, sign or γ needs an orthogonal measurement first. For the motivating timing task this yields a concrete design principle: route from baseline features to α, since the same baseline that fails to predict the lag (held-out ρ≈+0.05, chance) predicts α on held-out lineages (ATAC-only ρ=+0.309, positive in all six lineages), with the caveat that transcript abundance carries most of that signal (+0.724) and real day0 ATAC adds no predictive power beyond it (Δρ=−0.016).

## 4. Limitations

Several limits are load-bearing and we state them in full. Pseudotime is not wall-clock, so lags are expressed in pseudotime units. The profile-likelihood result is relative practical non-identifiability, reported on the conservative freed-nuisance basis (2.49×), and the identifiability-to-external-validation link remains suggestive only. All five external replications are single-donor or single-sample, E18 lacks an independent MoFlow lag, and the α corroboration rests primarily on one measured TT-seq source, since the second source was null and the two measured sources agree only at ρ≈0.15. The abundance confound is not resolved: abundance predicts measured synthesis at least as strongly as α does. All data are 10x Multiome, and generalization to other assays is untested. We audited per-gene kinetic parameters and the cell×gene velocity matrix, not the low-dimensional embedding arrows or trajectories that velocity is principally used for, so nothing here establishes that trajectory inference is unreliable. Causal statements from the ATAC-shuffle are bounded to HSPC and, at the matrix layer, to MultiVelo. The named-marker direction agreement is correlational, with a null marker-shuffle test and no replication in gastrulation. Finally, this is a claim about the reliability of the current methods, not about the absence of timing biology: deeper sequencing, finer time resolution or metabolic labeling could yet render the lag identifiable.

One reviewer-anticipated objection deserves its own note, and our check of it is exploratory rather than a result. The baseline-to-α route above was estimated with a linear model, so the weak accessibility signal after controlling for expression might be a model-class artefact. Re-running the same leave-one-lineage-out protocol with flexible learners does not support that reading: linear RidgeCV gives held-out ρ=+0.304 and expression-controlled partial ρ=+0.109 (n=472), RandomForest +0.178 and +0.013, and GradientBoosting +0.206 and +0.056. The nonlinear models do not exceed the linear one, and the gap widens once expression is controlled, which is the expected behaviour of flexible models at n=472 with six features. We report this only as a robustness note, not as a result: it uses a single lineage-holdout protocol, hyperparameters were left at defaults with minimal regularization, and the expression control was not matched line-for-line to the earlier analysis.

## 5. Conclusion

Of the several continuous per-gene quantities that multiome velocity models emit, the transcription rate α is the only one reproducible enough to consider as a downstream feature, and only alongside an abundance baseline: it reproduces across methods (ρ=0.88 observed), is recoverable by an RNA-only floor, and is consistent with an externally measured synthesis rate. The chromatin-to-transcription lag reproduces weakly at best, has near-chance sign agreement, is largely preserved under an ATAC shuffle, and is sloppy in the likelihood; γ is fragile and is not recovered even where an external ground truth exists. The deliverable is the reliability map and its routing rule, and the general lesson transfers beyond velocity: before a model-derived quantity becomes a feature in a health-relevant predictor, it should be sorted by cross-method reproducibility, an intervention on its claimed input, out-of-dataset replication and, where one exists, an external measurement.

*Research and education use only; not clinical.*

## Table 1. Cross-method reproducibility of each fitted per-gene output in HSPC

Paired gene-bootstrap 95% CIs, B=10⁴. Reproducibility is cross-method agreement on the same cells; it is not within-method fit quality, and the two are kept separate by design.

| Fitted output | Cross-method Spearman ρ | 95% CI | Note |
|---|---|---|---|
| Transcription rate α | +0.882 | [+0.855, +0.905] | RNA-only floor also recovers it (+0.818, +0.889) |
| Chromatin-opening rate α_c | +0.291 | [+0.209, +0.369] | sets the lag; method-sensitive |
| Splicing rate β | +0.080 | [−0.009, +0.168] | interval includes zero |
| Degradation rate γ | −0.109 | [−0.192, −0.023] | negative; not externally recovered |
| Lag magnitude (strongest pair) | +0.163 | [+0.078, +0.244] | most pairs at absolute ρ ≤ 0.08 |
| Lag sign agreement | 54.6% | n=560, binomial p=0.03 | 4.6 points above chance |

## Table 2. Velocity-output reliability map and routing rule

"Reliable" is set by the internal (cross-method) axis; the external measurement is corroboration, not a co-equal bar.

| Velocity output | Internal axis | External anchor | Reliability | Routing rule |
|---|---|---|---|---|
| *Steady-state abundance (reference, not a velocity output)* | property of the data | tracks measured synthesis at least as strongly as α (+0.41 versus +0.26) | *reference baseline* | check first; α adds no demonstrable synthesis information beyond it |
| Transcription rate α | high (ρ=0.88; floor recovers it) | corroborated (non-HK ρ +0.24 to +0.29, CIs exclude 0) | reproducible, but largely expression (α to abundance ρ=0.81) | usable with an explicit abundance baseline |
| Population directional balance (~50/50) | high (two methods converge) | n/a | reliable as a population statement | do not read per gene |
| Canonical priming-marker direction | limited descriptive agreement in HSPC; not replicated in gastrulation | no causal support (marker-shuffle p=0.58) | hypothesis-generating only | do not generalize beyond the named loci |
| Chromatin-opening rate α_c | low (ρ=0.29) | n/a | unreliable | stabilize before use |
| Degradation rate γ | low (ρ≈−0.1) | not recovered (K562 3/3 null; scVelo γ reversed, −0.224) | unreliable | do not use as-is |
| Per-gene lag magnitude | low (most pairs at absolute ρ ≤ 0.08) | not predictable from baseline (≈chance) | unreliable | orthogonal validation required |
| Per-gene lag sign / absolute timing | 54.6% agreement; MultiVelo structurally positive | n/a | unreliable (uninformative) | do not use |

## Figure legend

**Figure 1.** Cross-method concordance of the per-gene lag versus the transcription rate α in HSPC. Lag-magnitude pairwise rank agreement (most pairs |ρ|≤0.08, strongest pair +0.163 [+0.078, +0.244]) and per-gene sign agreement (54.6%, n=560, near chance), contrasted with the α reproducibility scatter (ρ=0.88 observed). Source figure: `fig01_p2_concordance.png`.

## References

Reference numbers are inherited from the full-length version of this work so that every value in the main text stays traceable to its source; the numbering is therefore not contiguous.

[1] La Manno G, Soldatov R, Zeisel A, et al. RNA velocity of single cells. *Nature* 560(7719), 494-498 (2018). doi:10.1038/s41586-018-0414-6.
[2] Cao J, Cusanovich DA, Ramani V, et al. Joint profiling of chromatin accessibility and gene expression in thousands of single cells. *Science* 361(6409), 1380-1385 (2018). doi:10.1126/science.aau0730.
[3] Li C, Virgilio MC, Collins KL, Welch JD. Multi-omic single-cell velocity models epigenome-transcriptome interactions and improves cell fate prediction. *Nature Biotechnology* 41, 387-398 (2023). doi:10.1038/s41587-022-01476-y.
[4] Li C, Gu Y, Virgilio MC, Lee KH, Collins KL, Welch JD. Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE. *Nature Communications* 16, 11505 (2025). doi:10.1038/s41467-025-66287-6.
[5] Hong A, Lee S, Kim K. Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states. *Nature Communications* 17, 566 (2025). doi:10.1038/s41467-025-67259-6.
[6] El Kazwini N, Gao M, Kouadri Boudjelthia I, Cai F, Huang Y, Sanguinetti G. CRAK-Velo: chromatin accessibility kinetics integration improves RNA velocity estimation. *Genome Biology* 27(1) (2026). doi:10.1186/s13059-026-04086-y.
[9] Gayoso A, Weiler P, Lotfollahi M, et al. Deep generative modeling of transcriptional dynamics for RNA velocity analysis in single cells. *Nature Methods* 21, 50-59 (2024). doi:10.1038/s41592-023-01994-w.
[18] Ma S, Zhang B, LaFave LM, et al. Chromatin potential identified by shared single-cell profiling of RNA and chromatin. *Cell* 183(4), 1103-1116.e20 (2020). doi:10.1016/j.cell.2020.09.056.
[19] Trevino AE, Müller F, Andersen J, et al. Chromatin and gene-regulatory dynamics of the developing human cerebral cortex at single-cell resolution. *Cell* 184(19), 5053-5069.e23 (2021). doi:10.1016/j.cell.2021.07.039. (GSE162170.)
[21] Bergen V, Soldatov RA, Kharchenko PV, Theis FJ. RNA velocity: current challenges and future perspectives. *Molecular Systems Biology* 17(8), e10282 (2021). doi:10.15252/msb.202110282.
[22] Gorin G, Fang M, Chari T, Pachter L. RNA velocity unraveled. *PLOS Computational Biology* 18(9), e1010492 (2022). doi:10.1371/journal.pcbi.1010492.
[23] Marot-Lassauzaie V, Bouman BJ, Donaghy FD, Demerdash Y, Essers MAG, Haghverdi L. Towards reliable quantification of cell state velocities. *PLOS Computational Biology* 18(9), e1010031 (2022). doi:10.1371/journal.pcbi.1010031.
[25] Luo Y, Ren J, Yang Q, You Z, Zhou Y, Qin Q, Li Q. Benchmarking RNA velocity methods across 17 independent studies. *Cell Reports Methods* 6(4), 101367 (2026). doi:10.1016/j.crmeth.2026.101367.
[26] Huang K, Zhou Y, Wang T, Li X, Zhao X, Liu X, Huang L, Zhou X, Liu J. Benchmarking algorithms for RNA velocity inference. bioRxiv 2026.01.03.697314 (2026). doi:10.64898/2026.01.03.697314. [Preprint, not peer-reviewed.]
[27] Wu Y, Kong C, Liao X, Lin Z, Sun X, Liu J. Comprehensive benchmarking of RNA velocity methods across single-cell datasets. *Genome Biology* 27(1), 242 (2026). doi:10.1186/s13059-026-04182-z.
[28] Ancheta S, Dorman L, Le Treut G, et al. Challenges and progress in RNA velocity: comparative analysis across multiple biological contexts. *PLOS Computational Biology* 22(6), e1014303 (2026). doi:10.1371/journal.pcbi.1014303.
[30] Schwalb B, Michel M, Zacher B, et al. TT-seq maps the human transient transcriptome. *Science* 352(6290), 1225-1228 (2016). doi:10.1126/science.aad9841. (GSE75792.)
[31] Herzog VA, Reichholf B, Neumann T, et al. Thiol-linked alkylation of RNA to assess expression dynamics. *Nature Methods* 14(12), 1198-1204 (2017). doi:10.1038/nmeth.4435.
[41] Zhang et al. Quantifying uncertainty in RNA velocity (ConsensusVelo). bioRxiv 2024.05.14.594102 (2024); *Biometrics* 82(1) ujag018 (in press). doi:10.1101/2024.05.14.594102. [Full author list and final venue to confirm.]
[44] Milacic M, Beavers D, Conley P, et al. The Reactome Pathway Knowledgebase 2024. *Nucleic Acids Research* 52(D1), D672-D678 (2024). doi:10.1093/nar/gkad1025.
[48] Schuirmann DJ. A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability. *Journal of Pharmacokinetics and Biopharmaceutics* 15(6), 657-680 (1987). doi:10.1007/bf01068419.
[49] Nosek BA, Ebersole CR, DeHaven AC, Mellor DT. The preregistration revolution. *Proceedings of the National Academy of Sciences* 115(11), 2600-2606 (2018). doi:10.1073/pnas.1708274114.
[50] Todorovski I, Tsang MJ, Feran B, et al. RNA kinetics influence the response to transcriptional perturbation in leukaemia cell lines. *NAR Cancer* 6(4), zcae039 (2024). doi:10.1093/narcan/zcae039. (GSE229305 synthesis; SLAM-seq half-lives in the parent SuperSeries GSE229314.)
[51] Raue A, Kreutz C, Maiwald T, et al. Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. *Bioinformatics* 25(15), 1923-1929 (2009). doi:10.1093/bioinformatics/btp358.
[52] Kreutz C, Raue A, Kaschek D, Timmer J. Profile likelihood in systems biology. *The FEBS Journal* 280(11), 2564-2571 (2013). doi:10.1111/febs.12276.
[53] Villaverde AF, Barreiro A, Papachristodoulou A. Structural identifiability of dynamic systems biology models. *PLOS Computational Biology* 12(10), e1005153 (2016). doi:10.1371/journal.pcbi.1005153.
[55] Gu et al. Profile-likelihood identifiability analysis of single-cell transcription (telegraph) kinetics. *Bioinformatics* 41(11), btaf581 (2025). doi:10.1093/bioinformatics/btaf581.
[60] Lange M, Bergen V, Klein M, et al. CellRank for directed single-cell fate mapping. *Nature Methods* 19(2), 159-170 (2022). doi:10.1038/s41592-021-01346-6.
[62] Kaminow B, Yunusov D, Dobin A. STARsolo: accurate, fast and versatile mapping/quantification of single-cell and single-nucleus RNA-seq data. bioRxiv (2021). doi:10.1101/2021.05.05.442755. [Preprint, not peer-reviewed.]
[66] Bergen V, Lange M, Peidli S, Wolf FA, Theis FJ. Generalizing RNA velocity to transient cell states through dynamical modeling. *Nature Biotechnology* 38(12), 1408-1414 (2020). doi:10.1038/s41587-020-0591-3.
[67] Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society Series B* 57(1), 289-300 (1995). doi:10.1111/j.2517-6161.1995.tb02031.x.
[68] Xie Z, Bailey A, Kuleshov MV, et al. Gene set knowledge discovery with Enrichr. *Current Protocols* 1(3), e90 (2021). doi:10.1002/cpz1.90.
[71] Wolock SL, Lopez R, Klein AM. Scrublet: computational identification of cell doublets in single-cell transcriptomic data. *Cell Systems* 8(4), 281-291.e9 (2019). doi:10.1016/j.cels.2018.11.005.

## Appendix

### A. Datasets, preprocessing and confound controls

Primary data: human HSPC 10x Multiome (GSE209878), day0 and day7 integrated, 21,878 cells. External systems: human fetal cortex (GSE162170) [19]; fetal E18 mouse brain (10x Genomics "Fresh Embryonic E18 Mouse Brain 5k" demo, CellRanger-ARC 1.0.0, no GEO accession); human BMMC (GSE194122, donor09/site4, spliced and unspliced recovered from the GEX BAM by velocyto [1]); macrophage differentiation (GSE284047, Day14 HSPC-direct); mouse gastrulation (GSE205117, E7.5 to E8.75 rep1, 10,779 cells; GEX via STARsolo Velocyto raw [62], ATAC aggregated from GEO fragments over gene bodies ±10 kb, gencode vM25). ATAC aggregation differs by provenance (HSPC via `mv.aggregate_peaks_10x`; BMMC via gencode-proximity aggregation of the processed peak matrix; gastrulation via fragment aggregation), which adds conservative noise to cross-dataset ranks.

Confound controls. Cell cycle was unbiased at the gene level (cell-cycle genes 1.9% of fit-lag genes; cell-cycle versus rest Mann-Whitney p=0.86; median change 0.037 on exclusion); the cell-level correlation arises because cycling is coupled to lineage (MK 88% versus HSC 3%), which the within-lineage analysis already controls, so no global regress-out was applied. Burst: lag versus α Spearman −0.24, reflected in regularized regression. Ambient RNA and doublets: scrublet [71], doublet median 0.045, pct_mito median 10.4% against a QC maximum of 20%. Analyses were within-lineage, with rare lineages (MK, Baso/Eo/Mast, pDC) carrying separate uncertainty. Multicollinearity of promoter and enhancer ATAC features was handled by regularized regression, and multiple testing across genes by permutation FDR.

### B. Velocity arms and lag conventions

Arms: RNA-only floor (scVelo dynamical [66], no chromatin channel); MultiVelo [3] (chromatin switch-time ODE, lag = t_sw2 − t_sw1); MultiVeloVAE [4] (VAE with continuous per-cell decoupling and coupling); MoFlow [5] (relay velocity, chromatin-spliced DTW lag); CRAK-Velo [6] (semi-mechanistic, DTW-derived lag). A CRAK-Velo lag-sign convention bug, opposite in sign to MoFlow's `fastdtw`, was found and corrected; CRAK-Velo is reported as a sensitivity arm only, given a shape artefact on smooth dynamics. Genes whose directional lag is exactly zero were treated as undetermined and excluded from sign statistics (MoFlow 76 of 636 genes; CRAK-Velo 135 of 868). A convention that instead gives zero its own sign category renders the same MoFlow versus MultiVeloVAE comparison as 48%, which is why the exclusion is stated explicitly. The permutation-FDR per-gene sign-consistency test returned an empty agreement set (0 of 598 genes at FDR<0.10); we report this as a CRAK-dependent sensitivity result rather than a headline, because the empty set requires three sign-variable methods, and a clean sign-variable pair is power-bounded (minimum permutation p ≈ 0.50 regardless of signal).

### C. Cross-dataset details

**Table A1. Replication of the α-over-lag ordering across five external systems.**

Within-dataset α is the median of the three cross-method pairs (floor, MultiVelo, MultiVeloVAE); within-dataset lag is the MultiVelo versus MultiVeloVAE magnitude pair, except human fetal cortex, which has no MultiVeloVAE fit and is supplied by a MultiVelo versus MoFlow pair. Cross-dataset entries are HSPC-to-external magnitude-rank ρ. Cross-dataset α intervals overlap, so the tissue-distance ordering is qualitative. Each replication is one donor or sample.

| System | Tissue relation | Within-dataset α | Within-dataset lag | Cross-dataset α | Cross-dataset lag |
|---|---|---|---|---|---|
| HSPC (GSE209878) | primary | +0.882 | +0.163 [+0.078, +0.244] | n/a | n/a |
| Macrophage (GSE284047) | HSPC-direct | +0.865 | +0.074 [+0.006, +0.143] | +0.643 [+0.554, +0.719] | +0.148 [+0.027, +0.263] |
| Human BMMC (GSE194122) | same tissue | +0.851 | −0.088 [−0.209, +0.034] | +0.550 [+0.368, +0.696] | +0.052 [−0.164, +0.262] |
| Human fetal cortex (GSE162170) | distant | not computable | −0.052 [−0.135, +0.029] | +0.475 [+0.292, +0.626] | +0.185 [−0.005, +0.369] |
| Mouse gastrulation (GSE205117) | priming-maximal | +0.927 | −0.026 [−0.089, +0.038] | +0.415 [+0.244, +0.561] | +0.028 [−0.165, +0.224] |
| E18 mouse brain (10x demo) | cross-species | +0.810 | +0.057 [−0.005, +0.118] | +0.321 [+0.158, +0.472] | +0.105 [−0.069, +0.269] |

Gastrulation passed a preregistered six-item scorecard sealed by commit hash before fitting; its α pass line was ρ≥0.50. The HSPC +0.882 is an observed value, not a pass line.

A structurally independent MoFlow lag pair was added to four external systems: human fetal cortex −0.052 [−0.135, +0.029], macrophage −0.025 [−0.089, +0.041], gastrulation +0.038 [−0.027, +0.099], BMMC −0.116 [−0.228, −0.003] (clearing zero only on the negative side, that is, anti-concordance rather than agreement). On E18 the MoFlow fit succeeded (1,150 genes) but the chromatin-spliced DTW lag was undefined (all-NaN under a collapsed velo-pseudotime), so E18 keeps only the MultiVelo versus MultiVeloVAE pair. Within macrophage, the same-gene MultiVelo versus MultiVeloVAE contrast gives Δρ=+0.843 (ρ_α=+0.917 minus ρ_lag=+0.074; 95% CI [+0.773, +0.912], n=871); this is a within-dataset paired contrast, not the difference of the cross-dataset point estimates. For gastrulation the paired within-dataset α value is +0.953, giving Δρ=+0.979 [+0.916, +1.041]. Human fetal cortex has no within-dataset MultiVeloVAE fit, so its three-pair α median is not computable; its within-dataset lag comes from a MultiVelo versus MoFlow pair (signed −0.028, magnitude −0.052, n=551).

### D. Marker direction, unanimity and enrichment

Tabulating every gene's call from each sign-variable method, the granule markers *MPO*, *ELANE*, *AZU1*, *LYZ* and *S100A9* were chromatin-leading in every method that scored them and the early marker *MEIS1* was RNA-leading, while *CSF1R*, *HLF* and *CRHBP* were split. Of the 640 genes with at least two sign-variable calls, 38.6% were unanimous and 61.4% split. The unanimous chromatin-leading set is enriched for the azurophil-granule programme (Reactome neutrophil degranulation [44], adjusted p=9.4e-04) only against a background restricted to the 640 genes we could score; with a genome-wide background many GO terms appear, which is why the fit-restricted background is used [68]. We do not give this a biological reading: agreement is not correctness, the marker-shuffle control was null, and these are also the genes with the strongest expression signal, so a signal-to-noise explanation cannot be separated. The pattern did not replicate in gastrulation (per-gene agreement 50.6%, n=1,061, binomial p=0.71; unanimous-set sizes matched independent per-method calls, both-chromatin expected 0.347 and observed 0.347), with no counterpart enrichment.

### E. Profile-likelihood details

MultiVelo's likelihood was profiled along the α and lag axes with latent time re-optimized at each scan point (n=538 genes; fit and likelihood reproduction r≈1.0). Two nuisance regimes were run: fixed-nuisance (β, γ, α_c, rescale, scale_cc held), giving the upper-bound ratio 3.53× (IQR [1.92, 7.41]) with α stiffer in 94.57% of genes, and freed-nuisance (those re-optimized), giving the conservative 2.49× with α stiffer in 77.03% of genes (n=148). Freeing β and γ collapses the α curvature to a median 0.19× of its fixed value. The freed ratio is defined only for genes with positive freed lag curvature; the flattest genes, where the ratio is undefined, are excluded, which makes 2.49× conservative. Precedents for this style of analysis on kinetic models are [51,52,53,55], and the closest velocity-specific prior art is ConsensusVelo [41].

### F. Synthetic positive control and power calibration

A chromatin-to-RNA pulse ODE with a known injected onset lag τ was simulated over a switch-sharpness by SNR grid, and two structurally independent methods (MoFlow DTW lag, MultiVelo switch-time lag) were fit on a shared gene axis. In the identifiability corner (W=0.1, SNR=20) the two methods agreed with each other (ρ=+0.454 [+0.20, +0.67]) and with the injected τ (MoFlow +0.506, MultiVelo +0.672). As SNR dropped, concordance collapsed (SNR-marginal means +0.242 at SNR=20, −0.035 at 6, −0.005 at 2). Power calibration shows the real HSPC result is genuinely weak rather than a power artefact: at n=598 and N_perm=10⁴ the test detects |ρ|≳0.15 with power ≥0.8, so most real pairs (|ρ|≤0.08) fall below the detection floor while the single strongest magnitude pair (+0.163) is just detectable, exactly as calibrated. The identifiability corner is narrow (SNR=20 is unrealistically high per gene), which strengthens rather than weakens the reading that real data occupy the non-identifiable regime.

### G. Cell-level velocity-matrix audit (a separate layer)

Definitions, exclusion rules and falsification criteria were sealed before the fitted matrices were read. Cells and genes were matched by name across arms; the 505 genes common to all five arms were reduced to 354 after excluding any gene with a missing or constant velocity in any arm, on the shared 21,878 cells. Only spliced velocity was compared. The preregistered primary metric is the raw per-cell cosine, reported against a cell-shuffled null; because a globally shared direction inflates the raw value (the mean vector accounts for 12.9 to 37.4% of squared row norm depending on the arm), a mean-centred cosine is also reported as a post-hoc diagnostic.

Both preregistered contrasts failed. Multiome pairs agreed less with each other (−0.139) than with the RNA-only floor (+0.080), paired Δ=−0.206 [−0.207, −0.205], and destroying the chromatin channel did not collapse the matrix. Refitting MultiVelo on resampled cells reproduces its own matrix at mean-centred cosine +0.872 (six refits, range +0.826 to +0.887), so the measure detects agreement where agreement exists. An earlier version of the shuffle comparison was not like-for-like (ceiling on 15,315 resampled cells, shuffle on all 21,878); repeating the shuffle on the *same* resampled cell sets puts the shuffled matrix below the intact refit range in three of three pairs (+0.784, +0.813, +0.810), with non-overlapping cell-bootstrap intervals. We therefore withdraw the earlier statement that chromatin is inert in this matrix. What replaces it is bounded: the paired differences are all positive but their magnitude varies two- to three-fold across shuffle draws, sits at a single-digit percentage of the +0.872 ceiling, and stays an order of magnitude below what method choice produces on the same measure (mean-centred cosine −0.530 to +0.131 across method pairs). A same-cell, same-configuration rerun null shows MultiVelo's fit is deterministic here (Δ_rr=0.000000), so the paired difference carries no refit-noise component to subtract; a matched rerun for MoFlow reproduces its matrix at +0.9999, so the near-zero cross-method values involving MoFlow read as genuine disagreement rather than arm instability. This positive statement is restricted to MultiVelo, to HSPC and to this shuffle design. The baseline contrast repeats outside HSPC in four of four external systems (paired per-cell Δ = −0.159, −0.152, −0.289, −0.184; all intervals excluding zero) against a sealed threshold of three of four; the external systems carry no shuffle arm and no refit, so neither the causal control nor the ceiling replicates there. This layer is a different target from the per-gene lag, and its numbers are not carried into the per-gene reliability map. The two layers are consistent rather than contradictory: the same class of shuffle does not perturb the priming-marker lags more than a bulk shuffle, yet it does move the cell×gene matrix a little.

### H. Baseline-feature prediction and model-class robustness

Real day0 ATAC promoter and enhancer accessibility (511 genes over 8,583 day0 HSC/MPP cells) predicted the robust target α on held-out lineages (ATAC-only ρ=+0.309, positive in all six lineages) but not the non-robust lag (ρ=+0.05, chance). The predictable signal is carried by transcript abundance: abundance alone predicts α at ρ=+0.724 on held-out lineages, real ATAC adds no predictive power beyond it (Δρ=−0.016), and the abundance-controlled partial is +0.11. A within-method, cross-lineage refit tells the same story, with lag magnitude concording only weakly across separately fit lineages (median ρ=0.349, range 0.234 to 0.513) against its α_c control (median ρ=0.483).

Model-class robustness (exploratory; reported in Limitations, not as a result). Under the same leave-one-lineage-out protocol on six ATAC features: RidgeCV held-out ρ=+0.304, expression-controlled partial ρ=+0.109 (n=472); RandomForest +0.178 and +0.013; GradientBoosting +0.206 and +0.056. Per-feature correlations with fitted α: enhancer count +0.352, enhancer sum +0.318, enhancer accessibility +0.228, promoter-to-enhancer ratio −0.246, promoter accessibility −0.128, promoter count +0.046. Limits: one lineage-holdout protocol only, default hyperparameters with minimal regularization, and an expression control not matched line-for-line to the earlier analysis.

### I. Preregistration scorecard

For mouse gastrulation (GSE205117), six falsifiable predictions with pre-declared thresholds were sealed by commit hash before any velocity fit or concordance existed: within-dataset cross-method α ρ≥0.50; within-dataset lag ρ≤0.15; α-minus-lag gap ≥0.35; cross-dataset α>+0.2 and greater than the cross-dataset lag; per-gene lag mismatch greater than α mismatch (observed 0.294 versus 0.052 under the sealed original definition, MultiVelo versus MoFlow, n=968); and fragility persisting under maximal priming. All six passed with no post-hoc rescue, and the scorecard reproduced byte-identically on deterministic recomputation. The threshold ρ≥0.50 is the sealed pass line; the observed HSPC α=0.88 is an observed value and was not used as a threshold.

### J. Data and code availability

All primary and external datasets are public under the accessions listed in Appendix A. Analysis code, the sealed preregistration and the deterministic recomputation scripts are withheld during double-blind review and will be released with a permanent identifier on acceptance.
