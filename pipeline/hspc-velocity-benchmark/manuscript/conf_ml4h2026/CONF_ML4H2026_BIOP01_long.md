<!--
════════════════════════════════════════════════════════════════════════
내부 메모 (제출 전 제거): 출처, 범위, 미확정
════════════════════════════════════════════════════════════════════════
카메라레디(2026-11-01 착수): 마감 11/13 AoE = 11/14(토) 20:59 KST. 반박문(papers/submissions/2026-ml4h/
  reliability-map/rebuttal/final/*.txt)에서 약속한 수정을 반영했다. 수치 출처는 results/post_review_robustness.gen.md
  (R1~R5), results/priming_recompute.gen.md(kkkim-pipeline, 1eb0ae1), 재적합 안정성은 외장하드 백업 refit 표로 재계산(pipeline 77f4232: priming +0.725, coupled-on +0.624).
  익명화 해제: 저자, 소속, 교신, 사사, 연구비, 코드 저장소. 김가경 소속은 GIW와 같이 Pseudo Lab으로 둔다(draft_v2는
  Independent Researcher, 사용자 확인 필요). 이건규 영문명은 본인 제출값 "Geon gyu Lee"(draft_v2 정본).
  미반영(새 그림 필요): 대표 profile 곡선. 외부 시스템의 priming 정의 재계산은 하지 않았고 본문에 그렇게 적었다.
학회: ML4H 2026, Findings track (non-archival). 마감 2026-09-10 23:59 AoE (= 2026-09-11 20:59 KST).
분량 규약: 본문 4페이지, 참고문헌·부록 무제한.
분량 실측(2026-09-10 축약 후): 본문 2,444단어. tectonic 조판 결과 본문이 p4 안에서 끝나고 References가
  p5 최상단(y=91/792, 다른 면 본문 시작 y=93과 같은 높이)에서 시작한다. 총 11쪽.
  축약은 삭제가 아니라 부록 이전이 원칙이었다. 옮긴 것: 구 Table 1(교차재현 요약) -> Appendix B Table A0,
  구 Table 2의 Internal axis/External anchor 2개 열 -> Appendix L(5열 전체판), Introduction의 method별
  lag 정의와 벤치마크 세부 -> Appendix K, Axis4 CI/n -> Appendix J, 나머지 부차 수치 -> Appendix B/C/D/E.
  삭제한 수치는 없다(축약 전후 수치 토큰 대조에서 소실 0건).
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
  4페이지 제약과 Table 1(신뢰지도) 중복을 고려해 본문에서 참조하지 않는다. 나머지 fig02~fig06, fig08도 협업 서버
  소멸로 재렌더 대상이지만 이 제출본은 참조하지 않는다.
LaTeX 변환기(conf_giw2026/md2tex.py 재사용) 주의: 본문에 남은 비-ASCII는
  ± × ü Δ α β γ κ ρ τ ⁴ − ≈ ≤ ≥ ≫ ≳ 이다. GIW 변환표에 없는 κ, τ, ≫, ≳, ü를 매크로에 추가해야 한다.
본문 표는 Table 1(신뢰지도, 3열) 하나뿐이다. md2tex_ml4h.py가 Results 끝에서 두 번째 소절 앞에
  단(column) float으로 끼워 넣는다. 전폭 table*로 두면 자리를 못 찾아 참고문헌 뒤 페이지로 밀린다.
════════════════════════════════════════════════════════════════════════
-->

# A Reliability Map for Per-Gene Multiome RNA Velocity Parameters in Single-Cell Kinetics

**Authors:** Ka-Kyung Kim^1^\*, Jaemyun Lyu^2,3^, Geon gyu Lee^1,4^, Sejin Park^5^, Yong Gi Ji^6^

**Affiliations:** ^1^Pseudo Lab, Seoul, Republic of Korea; ^2^R&D Center, Genolution Inc., Seoul, Republic of Korea; ^3^Laboratory of RNA Cell Biology, Department of Bioconvergence Engineering, Dankook University Graduate School, Yongin, Republic of Korea; ^4^Omixai Co., Ltd., Seoul, Republic of Korea; ^5^Seegene Inc., Seoul, Republic of Korea; ^6^Qaumtum c&s, Seoul, Republic of Korea. \*Corresponding author: kakyung.kim@gmail.com

## Abstract

Chromatin-informed ("multiome") RNA velocity models emit per-gene quantities increasingly consumed downstream as biomedical features: a transcription rate α, a degradation rate γ, and a chromatin-to-transcription *lag* offered as a clock for regulatory timing. A derived quantity is usable as a feature only if it is reliable. We audit these outputs on four axes in human hematopoietic stem and progenitor cells (HSPCs; 10x Multiome, GSE209878, 21,878 cells) across five velocity arms sharing a common preprocessing branch: cross-method reproducibility, a within-lineage ATAC shuffle, replication in five external multiomes (one preregistered), and comparison with metabolically measured rates. Among continuous per-gene kinetic parameters only α reproduced across methods (Spearman ρ=0.88, observed). The lag did not reproduce under any definition tested (at best +0.364, MultiVelo's priming interval against the MultiVeloVAE rate proxy; −0.009 when both methods use one identical formula), sign agreement was 54.6%, and γ neither reproduced (ρ≈−0.1) nor recovered a measured half-life. α stayed reproducible after removing mean expression (partial ρ=+0.715), but abundance tracked measured synthesis at least as well as α, so its kinetic accuracy is not established. The axes distil into a reliability map that keeps reproducibility and accuracy evidence apart, with a routing rule for downstream models. Research and education use only; not clinical.

**Keywords:** reliability of model-derived features, RNA velocity, single-cell multiome, parameter identifiability

## Data and Code Availability

All data analysed here are public and previously published: human HSPC 10x Multiome (GSE209878, primary); human fetal cortex (GSE162170); human BMMC (GSE194122); macrophage differentiation (GSE284047); mouse gastrulation (GSE205117); the 10x Genomics "Fresh Embryonic E18 Mouse Brain 5k" demo, which carries no accession; and the measured-rate references GSE229305 and GSE75792. Accessions, processing and provenance caveats are in Section 3.1.

The analysis scripts, per-gene result tables, sealed preregistration, environment files and deterministic recomputation scripts are public at https://github.com/biospin/BioProject01 (MIT licence; branch kkkim-pipeline, release ml4h2026-camera-ready), archived as <FILL: Zenodo DOI>. Every number in this paper is regenerated from that release.

## Institutional Review Board (IRB)

This work analyses only previously published, publicly available, de-identified datasets and generates no new human-participant data. It is therefore not human subjects research and did not require IRB approval; the original studies obtained their own approvals and consents.

## 1. Introduction

Single-cell models are routinely used as feature extractors for downstream biomedical prediction, RNA velocity prominent among them. Velocity infers the direction and speed of transcriptional change from unspliced and spliced mRNA [1], and chromatin-informed extensions couple this to single-cell ATAC [2]. These models do not emit a single number: each fits a transcription rate α, a splicing rate β, a degradation rate γ and, in the multiome variants, a per-gene chromatin-to-transcription lag [3,4,5,6] (Section 2).

The lag is the most attractive of these outputs for health applications, promising a per-gene clock: which genes open chromatin ahead of transcription, and therefore how quickly a locus can respond. Our motivating task, predicting the *timing* of an epigenetic-drug response in hematopoietic cells, would have consumed it as a covariate. The relevance to health is therefore indirect: we evaluate no patients or clinical decisions, and target an earlier step in health-relevant pipelines, deciding whether a model-derived quantity is reliable enough to enter a downstream predictor as a feature.

Reliability has two faces. The internal face asks whether the same number appears when a different reasonable algorithm is run on the *same* cells, and many velocity readouts fail even this [21,22,23]: 2026 benchmarks establish that velocity direction and per-gene driver rankings are both method-dependent, with no universal winner [25,26,27,28]. To our knowledge all of them score the velocity *vector*, not the individual per-gene outputs, and none perturbs the chromatin input and re-fits (Section 2). The external face asks whether a fitted rate recovers an *independently measured* kinetic quantity, which metabolic-labeling assays [30,31] make possible for two rates, the stronger bar because a quantity can reproduce across methods and still be a shared artefact.

The failure mode we address is narrower than outright irreproducibility and, we suspect, more common: a quantity demonstrated on illustrative loci is then consumed downstream at a per-gene quantitative level at which its reliability was never tested. We therefore treat velocity outputs as candidates to be sorted, and the contribution is a four-axis reliability protocol with the resulting **reliability map**: which outputs may enter a downstream model directly, which need a baseline, and which require orthogonal validation first. ConsensusVelo [41] showed the weak identifiability of velocity switch-times; new here are the per-output α-versus-lag *dissociation* across methods and lag definitions, and the map built on it.

## 2. Related Work

The multiome velocity methods define the lag differently. MultiVelo defines explicit priming and decoupling offsets between chromatin and RNA switch times [3], MultiVeloVAE generalizes these to continuous per-cell decoupling and coupling factors [4], MoFlow obtains a chromatin-spliced lag post hoc, by dynamic time warping of binned chromatin and spliced profiles along pseudotime [5], and CRAK-Velo admits a trajectory-derived lag [6].

The velocity-critique literature reports that violated model assumptions and multiple kinetic regimes produce wrong velocities [21,22] and that reliable quantification of even the velocity direction is non-trivial [23]. Among the 2026 benchmarks, the one task named "negative control robustness" [27] scores whether a method emits spuriously non-zero velocity on static cells, which is output plausibility rather than chromatin causality; to our knowledge no benchmark sorts the individual per-gene outputs by reliability, applies a permutation-null concordance test, or perturbs the chromatin input and re-fits.

## 3. Methods

**Data and arms.** The primary dataset is human HSPC 10x Multiome (GSE209878), day0 and day7 integrated, 21,878 cells. Five velocity arms were fit: an RNA-only floor (scVelo dynamical [66], no chromatin channel) and four chromatin-informed methods, MultiVelo [3], MultiVeloVAE [4], MoFlow [5] and CRAK-Velo [6]. All arms branch from a common preprocessing pipeline with a common-graph ablation, so method differences are not preprocessing differences. The methods do not estimate the same lag (Table A2): we use MultiVelo's priming interval t_sw1 as its primary lag and its coupled-on length t_sw2 − t_sw1 as a sensitivity, MultiVeloVAE's rate proxy 1/α_c − 1/α, and dynamic-time-warping offsets for MoFlow and CRAK-Velo. Pseudotime is not wall-clock, so the lag is expressed in pseudotime units. Five external multiomes replicate the analysis, each a single donor or sample (Section 3.1).

**Four axes.** Each per-gene output was tested for (1) cross-method reproducibility, pairwise Spearman rank agreement between arms on a shared gene axis, with paired gene-bootstrap intervals, a gene-label permutation-FDR test [67] and TOST against a pre-declared |ρ|<0.2 bound [48] (Section 4.1); the intervals resample genes conditional on the fitted models, cells and preprocessing, do not cover cell sampling or refitting, and are checked against a co-expression-module bootstrap; (2) response to a within-lineage ATAC shuffle, permuting ATAC profiles across cells within each lineage, which destroys cell-level chromatin–RNA pairing while preserving lineage-level chromatin distributions, and re-fitting, for MultiVelo and independently for MoFlow, with a marker-level variant (Section 4.3); (3) replication within and across the five external datasets; and (4) agreement with an external measurement, fitted α against measured K562 TT-seq synthesis (GSE229305 [50]; second source GSE75792 [30]) and fitted γ against SLAM-seq mRNA half-life [31], the only two with a measured counterpart, on the non-housekeeping stratum. Transcript abundance was carried throughout as a competing baseline, because at steady state synthesis equals abundance times the degradation rate constant.

**Preregistration.** Mouse gastrulation, where lineage priming is maximal, was tested by preregistration [49]: six predictions with pre-declared thresholds sealed by commit hash before any velocity fit existed. The sealed pass line for within-dataset cross-method α is Spearman ρ≥0.50; the HSPC α=0.88 reported below is an *observed* value and was never the pass line. The primary HSPC analysis and the other four external systems are not preregistered.

Lag conventions, confound controls, the enrichment protocol and the matrix audit are in Sections 3.1, 3.2, 4.3 and 4.8.

### 3.1 Datasets, Preprocessing and Confound Controls

Primary data: human HSPC 10x Multiome (GSE209878), day0 and day7 integrated, 21,878 cells. External systems: human fetal cortex (GSE162170) [19]; fetal E18 mouse brain (10x Genomics "Fresh Embryonic E18 Mouse Brain 5k" demo, CellRanger-ARC 1.0.0, no GEO accession); human BMMC (GSE194122, donor09/site4, spliced and unspliced recovered from the GEX BAM by velocyto [1]); macrophage differentiation (GSE284047, Day14 HSPC-direct); mouse gastrulation (GSE205117, E7.5 to E8.75 rep1, 10,779 cells; GEX via STARsolo Velocyto raw [62], ATAC aggregated from GEO fragments over gene bodies ±10 kb, gencode vM25). ATAC aggregation differs by provenance (HSPC via `mv.aggregate_peaks_10x`; BMMC via gencode-proximity aggregation of the processed peak matrix; gastrulation via fragment aggregation), which adds conservative noise to cross-dataset ranks.

Confound controls. Cell cycle was unbiased at the gene level (cell-cycle genes 1.9% of fit-lag genes; cell-cycle versus rest Mann-Whitney p=0.86; median change 0.037 on exclusion); the cell-level correlation arises because cycling is coupled to lineage (MK 88% versus HSC 3%), which the within-lineage analysis already controls, so no global regress-out was applied. Burst: lag versus α Spearman −0.24, reflected in regularized regression. Ambient RNA and doublets: scrublet [71], doublet median 0.045, pct_mito median 10.4% against a QC maximum of 20%. Analyses were within-lineage, with rare lineages (MK, Baso/Eo/Mast, pDC) carrying separate uncertainty. Multicollinearity of promoter and enhancer ATAC features was handled by regularized regression, and multiple testing across genes by permutation FDR.

### 3.2 Velocity Arms and Lag Conventions

Axis-1 settings: paired gene-bootstrap 95% intervals at B=10⁴ and a gene-label permutation-FDR agreement test at N=10⁴, FDR<0.10.

**Table A2. What each method's lag estimates.**

| Method | Per-gene lag used | Sign |
|---|---|---|
| MultiVelo | priming interval t_sw1 (primary); coupled-on length t_sw2 − t_sw1, chromatin closing minus transcriptional induction for model-1 genes and repression minus induction for model-2 genes (sensitivity) | positive by construction |
| MultiVeloVAE | no native per-gene lag; rate proxy 1/α_c − 1/α | sign-variable |
| MoFlow | dynamic time warping offset between chromatin and spliced-RNA trajectories | sign-variable |
| CRAK-Velo (sensitivity arm) | trajectory-derived offset, also by dynamic time warping | sign-variable |

Arms: RNA-only floor (scVelo dynamical [66], no chromatin channel); MultiVelo [3] (chromatin switch-time ODE, lag = t_sw2 − t_sw1); MultiVeloVAE [4] (VAE with continuous per-cell decoupling and coupling); MoFlow [5] (relay velocity, chromatin-spliced DTW lag); CRAK-Velo [6] (semi-mechanistic, DTW-derived lag). A CRAK-Velo lag-sign convention bug, opposite in sign to MoFlow's `fastdtw`, was found and corrected; CRAK-Velo is reported as a sensitivity arm only, given a shape artefact on smooth dynamics. Genes whose directional lag is exactly zero were treated as undetermined and excluded from sign statistics (MoFlow 76 of 636 genes; CRAK-Velo 135 of 868). A convention that instead gives zero its own sign category renders the same MoFlow versus MultiVeloVAE comparison as 48%, which is why the exclusion is stated explicitly. The permutation-FDR per-gene sign-consistency test returned an empty agreement set (0 of 598 genes at FDR<0.10); we report this as a CRAK-dependent sensitivity result rather than a headline, because the empty set requires three sign-variable methods, and a clean sign-variable pair is power-bounded (minimum permutation p ≈ 0.50 regardless of signal). TOST at the pre-declared |ρ|<0.2 bound does not certify the HSPC magnitude lag as equivalent to zero (interval upper limit +0.244 breaches the bound), and neither is BMMC certified; the MoFlow-versus-MultiVeloVAE directional pair and E18 are certified equivalent. The fragility claim therefore rests on the α-minus-lag dissociation (Δρ=+0.720 [+0.636, +0.802] for the coupled-on length, +0.518 [+0.441, +0.596] for the priming interval), not on an equivalence certificate.

### 3.3 Profile-Likelihood Coordinates

**Coordinates.** Both profiles were taken in log-parameter space: the curvature is −d²LL/d(ln θ)² per cell for θ = α and θ = lag, by a two-sided finite difference with step 0.15 in ln θ. It does not change when either parameter is rescaled, so the ratios are unit-invariant and compare relative precision: a median ratio of 3.53 means α is located about 1.9 times more tightly relative to its own magnitude than the lag is relative to its own. The lag, unlike α, has a natural reference scale, the pseudotime horizon (20 units; the lags of these genes have median 3.50, range 0.20 to 11.22). Expressing the lag linearly as a fraction of that horizon, with α kept in log coordinates, reverses the median ratio on the same 258 genes to 0.10 (IQR [0.03, 0.22]; α stiffer in 1.9%). Because α has no comparable natural scale, neither coordinate choice is canonical, and the curvature ratio does not establish a coordinate-free identifiability difference. The profiled lag is the coupled-on length t_sw2 − t_sw1, not the priming interval. Of the 205 boundary-pinned lags, 199 belong to genes fit in the induction-only direction, whose coupled-on state does not end within the observed trajectory.

### 3.4 Synthetic Positive Control

A chromatin-to-RNA pulse ODE with a known injected onset lag τ was simulated over a switch-sharpness by SNR grid, and two structurally independent methods (MoFlow DTW lag, MultiVelo switch-time lag) were fit on a shared gene axis.

### 3.5 Preregistration Scorecard

For mouse gastrulation (GSE205117), six falsifiable predictions with pre-declared thresholds were sealed by commit hash before any velocity fit or concordance existed: within-dataset cross-method α ρ≥0.50; within-dataset lag ρ≤0.15; α-minus-lag gap ≥0.35; cross-dataset α>+0.2 and greater than the cross-dataset lag; per-gene lag mismatch greater than α mismatch (observed 0.294 versus 0.052 under the sealed original definition, MultiVelo versus MoFlow, n=968); and fragility persisting under maximal priming.

## 4. Results

### 4.1 Only α Reproduces Across Methods

On one method pair (MultiVelo versus MultiVeloVAE) and one gene set (n=538), α reproduced strongly (Spearman ρ=0.88 observed; +0.882 [+0.856, +0.904]) and was recovered even by the RNA-only floor, which has no chromatin channel (Table A0). The per-gene lag did not, under any definition (Figure 1): +0.364 [+0.285, +0.440] with MultiVelo's priming interval, +0.163 [+0.078, +0.247] with its coupled-on length, and no better when both methods compute the lag from one identical formula (signed +0.124, magnitude −0.009). Against MoFlow the priming interval gave +0.038 [−0.046, +0.122]. Every α-minus-lag contrast excluded zero, the smallest being Δρ=+0.518 [+0.441, +0.596], and the coupled-on contrast (Δρ=+0.720) held when genes were resampled as whole co-expression modules (Gene dependence, below). Direction was little better: the chromatin-leads fraction sat near 50/50 across the three sign-variable methods, which does not support a genome-wide "chromatin primes transcription" ordering, and sign agreement between MoFlow and MultiVeloVAE was 54.6% (n=560; binomial p=0.03), a detectable but practically negligible excess.

**Table A0. Cross-method reproducibility of each fitted per-gene output in HSPC.** Paired gene-bootstrap 95% CIs, B=10⁴. Reproducibility is cross-method agreement on the same cells; it is not within-method fit quality, and the two are kept separate by design.

| Fitted output | Cross-method Spearman ρ | 95% CI | Note |
|---|---|---|---|
| Transcription rate α | +0.882 | [+0.856, +0.904] | RNA-only floor also recovers it (+0.818, +0.889) |
| Chromatin-opening rate α_c | +0.291 | [+0.209, +0.369] | sets the lag; method-sensitive |
| Splicing rate β | +0.080 | [−0.009, +0.168] | interval includes zero |
| Degradation rate γ | −0.109 | [−0.192, −0.023] | negative; not externally recovered |
| Lag, MultiVelo priming vs MultiVeloVAE proxy | +0.364 | [+0.285, +0.440] | primary definition; best case of any definition |
| Lag, MultiVelo coupled-on vs MultiVeloVAE proxy | +0.163 | [+0.078, +0.247] | sensitivity definition, as submitted |
| Lag, MultiVelo priming vs MoFlow | +0.038 | [−0.046, +0.122] | n=537 |
| Lag sign agreement | 54.6% | n=560, binomial p=0.03 | 4.6 points above chance |

Within one method the lag is moderately stable (MultiVelo refit on 12 overlapping 70% subsamples: priming interval +0.725, coupled-on length +0.624, α +0.949; Within-method stability, below), so the failure is reproducibility across methods and definitions. For a downstream user the consequence is the same: the value obtained depends on the method and definition chosen.

**Harmonized comparison.** On one method pair (MultiVelo versus MultiVeloVAE) and one gene set (n=538), with Δρ = ρ_α − ρ_output on the same bootstrap draw (B=10⁴): α_c +0.291 [+0.208, +0.369], Δρ +0.591 [+0.510, +0.676]; lag, each method's default definition, magnitude, +0.163 [+0.078, +0.247], Δρ +0.720 [+0.636, +0.802]; lag, MultiVelo priming interval against the MultiVeloVAE proxy, magnitude, +0.364 [+0.285, +0.440], Δρ +0.518 [+0.441, +0.596]; lag, identical formula 1/α_c − 1/α in both methods, signed, +0.124 [+0.038, +0.208], Δρ +0.758 [+0.670, +0.847]; the same, magnitude, −0.009 [−0.095, +0.080], Δρ +0.891 [+0.801, +0.978]. On the 537 genes common to all three methods, α (MultiVelo versus MultiVeloVAE) is +0.882 and the lag pairs are MultiVelo versus MultiVeloVAE +0.165 (magnitude), MultiVelo versus MoFlow −0.013 (magnitude; +0.038 with the priming interval), and MultiVeloVAE versus MoFlow −0.064 (magnitude) and +0.107 (signed). MultiVelo's lag is positive by construction, so it enters magnitude comparisons only. Every α-minus-lag interval excludes zero.

**Gene dependence.** The intervals resample genes conditional on the fitted models, the cells and the preprocessing; they do not cover cell sampling or refitting. As a dependence-aware sensitivity analysis we resampled whole co-expression modules (average-linkage clusters of the gene-gene correlation of smoothed spliced expression) instead of independent genes. For Δρ=+0.720 the interval is [+0.635, +0.800] with independent genes in the same resampling run and [+0.582, +0.794], [+0.600, +0.801], [+0.611, +0.792] and [+0.612, +0.794] with K=10, 20, 50 and 100 modules. The modules are unequal in size (the largest holds 156 to 212 genes), so these intervals are approximate, but the contrast does not depend on treating genes as independent.

**Within-method stability.** MultiVelo was refit from scratch on 12 subsamples of 70% of the 15,315 cells, without replacement to avoid collapsing the neighbour graph. Mean pairwise Spearman correlation of per-gene values across refits was α +0.949, α_c +0.729, the priming interval +0.725 and the coupled-on lag +0.624, with median coefficients of variation 0.23, 0.25, 0.37 and 0.31. Because the subsamples overlap this is an optimistic estimate; the other methods' within-method stability was not assessed, so the cross-method value cannot be attributed entirely to disagreement between methods.

Further HSPC cross-method concordance values follow. Under its original signed lag definition the three pairwise Spearman correlations were −0.04 (MultiVelo versus MoFlow, p=0.38), −0.01 (MultiVelo versus MultiVeloVAE, p=0.81) and +0.08 (MoFlow versus MultiVeloVAE, p=0.04); unifying the lag definition raised the strongest pair only to +0.12, and the magnitude convention gives +0.163 for the coupled-on length (+0.364 for the priming interval). After correcting a CRAK-Velo lag-sign convention bug, MoFlow versus CRAK-Velo was −0.151 and CRAK-Velo versus MultiVeloVAE was −0.04. The chromatin-leads fraction among the sign-variable methods was MoFlow 44.8%, MultiVeloVAE 49.3% and CRAK-Velo 41.1%; the 54.6% MoFlow versus MultiVeloVAE sign agreement is computed after excluding zero-lag genes, and restricting either comparison to well-determined genes recovers no usable rule. Sign unanimity rises with α (Spearman +0.25, p=4e-09), yet even the top α decile is only 31.5% unanimous. The α headline +0.882 [+0.856, +0.904] is the MultiVelo versus MultiVeloVAE axis; the RNA-only floor recovers it at +0.818 [+0.773, +0.855] against MultiVelo and +0.889 [+0.862, +0.910] against MultiVeloVAE. The reconstructed lag difference concords at +0.124 [+0.038, +0.208], below its weaker component α_c. MultiVelo's apparent 100% chromatin-leads fraction is structural, which is why it never enters a sign test.

### 4.2 The Lag Survives Destroying Cell-Level Chromatin Pairing

Permuting ATAC profiles across cells within each lineage and re-fitting MultiVelo left the priming-interval distribution statistically unchanged (Mann–Whitney p=0.65, Kolmogorov–Smirnov p=0.46) and preserved its per-gene ranking (ρ=0.75; 0.72 for the coupled-on length). A paired Wilcoxon test detected a small shift under both definitions (Section 4.3), so the lag is not literally invariant. A structurally independent second method behaved the same way, the MoFlow lag retaining rank signal after the shuffle (ρ=0.52, against a cross-method-swap ρ=0.08). The fitted lag is therefore largely preserved when cell-level chromatin–RNA pairing within lineage is destroyed. Because the shuffle preserves lineage-level chromatin distributions, this does not show that chromatin contributes little overall (Figure 2).

<!-- FIG: figT01_atac_shuffle_priming.png -->

The marker corollary is null: canonical priming markers, the one place where methods agree on direction, moved no more than bulk genes under the shuffle (p=0.58) and did not replicate in gastrulation, so that agreement is descriptive rather than causal (Section 4.3). These causal statements are bounded to HSPC and to this shuffle design.

### 4.3 Marker Direction, Unanimity and Enrichment

Tabulating every gene's call from each sign-variable method, the granule markers *MPO*, *ELANE*, *AZU1*, *LYZ* and *S100A9* were chromatin-leading in every method that scored them and the early marker *MEIS1* was RNA-leading, while *CSF1R*, *HLF* and *CRHBP* were split. Of the 640 genes with at least two sign-variable calls, 38.6% were unanimous and 61.4% split. The unanimous chromatin-leading set is enriched for the azurophil-granule programme (Reactome neutrophil degranulation [44], adjusted p=9.4e-04) only against a background restricted to the 640 genes we could score; with a genome-wide background many GO terms appear, which is why the fit-restricted background is used [68]. The marker-level shuffle variant compares marker and bulk shuffle-induced change on a bias-corrected relative scale; under it the marker median change was 0.137 against a bulk median of 0.144. The ATAC shuffle also barely moved MultiVelo's chromatin likelihood, from 0.239 to 0.237. ATAC shuffle by lag definition (n=538, gene-bootstrap 95% CI, B=10⁴): for the priming interval, per-gene ρ=+0.753 [+0.695, +0.806], Mann-Whitney p=0.65, Kolmogorov-Smirnov p=0.46, paired Wilcoxon p=0.0007, median 4.61 to 5.00; for the coupled-on length, ρ=+0.721 [+0.656, +0.780], Mann-Whitney p=0.20, Kolmogorov-Smirnov p=0.51, paired Wilcoxon p=0.0003, median 5.87 to 5.48. The preserved ranking also reflects switch-time ordering. The shuffle permutes ATAC profiles across cells within each lineage, so it destroys cell-level chromatin–RNA pairing while preserving lineage-level chromatin distributions; it does not test whether chromatin contributes overall. The larger absolute movements of some markers tracked their larger baseline lag rather than chromatin (|Δlag| correlated with lag magnitude, ρ=+0.24). We do not give this a biological reading: agreement is not correctness, the marker-shuffle control was null, and these are also the genes with the strongest expression signal, so a signal-to-noise explanation cannot be separated. The pattern did not replicate in gastrulation (per-gene agreement 50.6%, n=1,061, binomial p=0.71; unanimous-set sizes matched independent per-method calls, both-chromatin expected 0.347 and observed 0.347). The granule programme has no counterpart in mouse gastrulation, so the absence of a matching enrichment there is expected and is not evidence either way.

### 4.4 Replication in Five External Systems

On the same genes and method pair, α exceeded the lag in HSPC-derived macrophages (Δρ=+0.843 [+0.773, +0.912]) and mouse gastrulation (+0.979 [+0.916, +1.041]) (Table A1a); these paired contrasts use the coupled-on length, as the priming interval was not recomputed outside HSPC. In the other external datasets the comparison is not like-for-like, a median over three α pairs against one lag pair, and human fetal cortex has no MultiVeloVAE fit, so its lag comes from a MultiVelo versus MoFlow pair (Table A1, Appendix A). There too α reproduced strongly (median +0.810 to +0.927) while the lag stayed near zero, including a structurally independent MoFlow lag pair (all |ρ|≤0.12; below), and along the HSPC-to-external gene axis α outranked the lag in all five systems. The gastrulation test passed six of six sealed predictions with no post-hoc rescue (Section 3.5); its sealed pass line for cross-method α was ρ≥0.50, distinct from the observed HSPC value of 0.88. That confirmatory claim covers the six-item scorecard only, not all six systems.

<!-- FIG: fig_crossdataset -->

**Table A1a. Like-for-like replication: same genes, same method pair (MultiVelo versus MultiVeloVAE, coupled-on lag magnitude).** Δρ = ρ_α − ρ_lag on the same bootstrap draw. These are the primary external comparisons. The priming interval was not recomputed outside HSPC.

| System | n | ρ_α | ρ_lag | Δρ [95% CI] |
|---|---|---|---|---|
| HSPC (GSE209878) | 538 | +0.882 | +0.163 | +0.720 [+0.636, +0.802] |
| Macrophage (GSE284047) | 871 | +0.917 | +0.074 | +0.843 [+0.773, +0.912] |
| Mouse gastrulation (GSE205117) | 969 | +0.953 | −0.026 | +0.979 [+0.916, +1.041] |

Along the HSPC-to-external axis the human fetal cortex α is significant (p=4.5e-7) while its lag is not (p=0.06). Gastrulation passed a preregistered six-item scorecard sealed by commit hash before fitting; its α pass line was ρ≥0.50. The HSPC +0.882 is an observed value, not a pass line.

The MoFlow lag pairs are structurally independent of the MultiVelo versus MultiVeloVAE pairing. A structurally independent MoFlow lag pair was added to four external systems: human fetal cortex −0.052 [−0.135, +0.029], macrophage −0.025 [−0.089, +0.041], gastrulation +0.038 [−0.027, +0.099], BMMC −0.116 [−0.228, −0.003] (clearing zero only on the negative side, that is, anti-concordance rather than agreement). On E18 the MoFlow fit succeeded (1,150 genes) but the chromatin-spliced DTW lag was undefined (all-NaN under a collapsed velo-pseudotime), so E18 keeps only the MultiVelo versus MultiVeloVAE pair. Within macrophage, the same-gene MultiVelo versus MultiVeloVAE contrast gives Δρ=+0.843 (ρ_α=+0.917 minus ρ_lag=+0.074; 95% CI [+0.773, +0.912], n=871); this is a within-dataset paired contrast, not the difference of the cross-dataset point estimates. For gastrulation the paired within-dataset α value is +0.953, giving Δρ=+0.979 [+0.916, +1.041]. Human fetal cortex has no within-dataset MultiVeloVAE fit, so its three-pair α median is not computable; its within-dataset lag comes from a MultiVelo versus MoFlow pair (signed −0.028, magnitude −0.052, n=551). The MoFlow lag pair is a genuine second within-dataset pair in three of the four systems; in human fetal cortex it is that dataset's first lag pair rather than an additional one.

The six sealed predictions are listed in Section 3.5.

All six passed with no post-hoc rescue, and the scorecard reproduced byte-identically on deterministic recomputation. The threshold ρ≥0.50 is the sealed pass line; the observed HSPC α=0.88 is an observed value and was not used as a threshold.

### 4.5 Measured Rates: α Beyond Abundance, γ Not Recovered

Fitted α tracked the measured K562 TT-seq synthesis rate in all three methods scored, non-housekeeping ρ=+0.236 to +0.285, every interval excluding zero (details below). A second measured source (GSE75792) replicated this for the two multiome methods (MultiVelo +0.270, MultiVeloVAE +0.235, intervals excluding zero) but not for the RNA-only floor (+0.087), and the two sources agree with each other at ρ=+0.415. The fits are HSPC and the measurements K562, so model failure cannot be separated from cell-type differences. At steady state, synthesis equals abundance times the degradation rate constant, so a synthesis measurement largely tracks expression level. HSPC mean expression, our abundance baseline, tracks both K562 measurements at least as strongly as α does (MultiVelo: +0.410 versus +0.262, and +0.309 versus +0.270 for the second source), a value that also reflects expression ranks shared between the two cell types. After removing mean expression from both methods' α, cross-method agreement stayed high (partial Spearman +0.715 [+0.659, +0.765]) while the lag stayed low (+0.182). α therefore carries a reproducible component beyond expression level, but its kinetic content is not established: abundance matches the measurement at least as well, and the component may come from the unspliced and spliced counts both methods read.

γ behaved differently: all three methods were null against measured K562 degradation in the cleanest same-cell comparison while positive for α, and across a three-cell-line half-life panel only 1 of 9 method-by-line cells recovered γ weakly. The RNA-only scVelo γ was *reversed* in the uncensored reference (details below), attributed to that method only.

**Abundance-residualized concordance.** Partial Spearman given HSPC mean expression (n=538): α +0.715 [+0.659, +0.765] (raw +0.882), α_c +0.264 [+0.184, +0.344], coupled-on lag +0.182 [+0.098, +0.265]; α-minus-lag after adjustment +0.533 [+0.441, +0.623]. Each method's α correlates with abundance at +0.795 (MultiVelo) and +0.747 (MultiVeloVAE).

Fitted α against measured K562 TT-seq synthesis, non-housekeeping stratum: ρ=+0.236 [+0.095, +0.368] (RNA-only floor, n=193), +0.262 [+0.133, +0.385] (MultiVelo, n=235) and +0.285 [+0.165, +0.398] (MultiVeloVAE, n=251), all intervals excluding zero. Against the second measured source (GSE75792), non-housekeeping ρ was +0.087 [−0.100, +0.271] (RNA-only floor, n=124), +0.270 [+0.108, +0.428] (MultiVelo, n=157) and +0.235 [+0.080, +0.381] (MultiVeloVAE, n=164). Its transcription units are in GRCh38 coordinates. An earlier version of this analysis joined them to an hg19 gene annotation, which mapped 2,965 of 6,913 units and produced the null result and the ρ≈0.15 inter-source agreement reported there; with GENCODE v24 (GRCh38), 6,907 of 6,913 units map and the two sources agree at ρ=+0.415 (n=6,051 genes). On the same genes, abundance tracks the second source at least as strongly as α does (+0.309; α minus abundance −0.039 [−0.132, +0.050] for MultiVelo and −0.058 [−0.161, +0.043] for MultiVeloVAE), and against the first source α falls below abundance in all three methods (MultiVelo −0.148 [−0.222, −0.077]). Abundance tracks the same TT-seq measurement at least as strongly as α does (+0.410 versus +0.262), and two methods agree on α (+0.882) somewhat more than α resembles abundance (+0.809 on this non-housekeeping stratum; +0.795 on all genes). Against measured K562 degradation the same three methods gave −0.118, +0.053 and −0.011, all null, while all three were positive for α on the same cells. The reversed RNA-only scVelo γ in the uncensored MOLM13 reference is −0.224 [−0.359, −0.085].

### 4.6 Profile Likelihood Gives Relative Precision

In 236 of the 538 genes (44%; 205 boundary-pinned, 31 degenerate) the profile does not bound the lag at all. For the rest, profiling MultiVelo's likelihood with latent time re-optimized compares relative precision only. In log coordinates α is located more tightly than the coupled-on lag (median curvature ratio 3.53 on 258 interior-lag genes; 2.49 with nuisance parameters freed, on 148 genes), but expressing the lag as a fraction of the pseudotime horizon reverses the ratio (0.10), neither choice is canonical, and 199 of the 205 boundary-pinned lags come from induction-only fits, reflecting trajectory coverage (Section 3.3). We therefore claim cross-method non-reproducibility, not strict non-identifiability [51,52,53]; ConsensusVelo's weakly identified switch times [41] are consistent with this reading but do not prove it. A synthetic positive control shows the failure to be regime-specific (Section 4.7), and the cell×gene velocity matrix, a separate layer kept out of the map, reproduces no better across methods (Section 4.8).

<!-- FIG: fig_profile_likelihood -->

MultiVelo's likelihood was profiled along the α and lag axes with latent time re-optimized at each scan point (n=538 genes; fit and likelihood reproduction r≈1.0). Two nuisance regimes were run: fixed-nuisance (β, γ, α_c, rescale, scale_cc held), giving the upper-bound ratio 3.53× (IQR [1.92, 7.41]) with α stiffer in 94.57% of genes (n=258 interior genes with positive curvature on both axes), and freed-nuisance (those re-optimized), giving the conservative 2.49× with α stiffer in 77.03% of genes (n=148). Freeing β and γ collapses the α curvature to a median 0.19× of its fixed value. The freed ratio is defined only for genes with positive freed lag curvature; the flattest genes, where the ratio is undefined, are excluded, which makes 2.49× conservative. Per-cell curvature is far higher for α than for the lag (median 8.20 versus 2.24), and the lag axis is lag = t_sw2 − t_sw1. The γ leg is flat: tertile correlations against measured MOLM13 k_deg are −0.015, −0.101 and +0.077 with a high-minus-low contrast of +0.092 [−0.279, +0.440] (n=67 per tertile), so no stiffness gradient is visible on that axis. Of the 538 genes, 302 (56%) are interior, 205 (38%) boundary-pinned and 31 (6%) degenerate, so in 44% the profile cannot bound the lag; 199 of the 205 boundary-pinned genes are induction-only fits, which reflects trajectory coverage more than non-identifiability. The suggestive stiffness-to-external-validation check gives α stiffness tertile values 0.116, 0.153 and 0.302 at n=70 per tertile, with only the top tertile clearing zero (+0.302 [+0.068, +0.511]) and the decisive high-minus-low contrast not significant (Δρ=+0.186 [−0.149, +0.504]). Precedents for this style of analysis on kinetic models are [51,52,53,55], and the closest velocity-specific prior art is ConsensusVelo [41].

### 4.7 Synthetic Positive Control and Power Calibration

The simulation design is described in Section 3.4.

In the identifiability corner (W=0.1, SNR=20) the two methods agreed with each other (ρ=+0.454 [+0.20, +0.67]) and with the injected τ (MoFlow +0.506, MultiVelo +0.672). As SNR dropped, concordance collapsed (SNR-marginal means +0.242 at SNR=20, −0.035 at 6, −0.005 at 2). Power calibration shows the real HSPC result is genuinely weak rather than a power artefact: at n=598 and N_perm=10⁴ the test detects |ρ|≳0.15 with power ≥0.8, so most real pairs (|ρ|≤0.08) fall below the detection floor while the coupled-on magnitude pair (+0.163) is just detectable, exactly as calibrated. The identifiability corner is narrow (SNR=20 is unrealistically high per gene), which is consistent with real data lying outside the identifiable corner of this grid.

### 4.8 Cell-Level Velocity-Matrix Audit as a Separate Layer

Definitions, exclusion rules and falsification criteria were sealed before the fitted matrices were read. Cells and genes were matched by name across arms; the 505 genes common to all five arms were reduced to 354 after excluding any gene with a missing or constant velocity in any arm, on the shared 21,878 cells. Only spliced velocity was compared. The preregistered primary metric is the raw per-cell cosine, reported against a cell-shuffled null; because a globally shared direction inflates the raw value (the mean vector accounts for 12.9 to 37.4% of squared row norm depending on the arm), a mean-centred cosine is also reported as a post-hoc diagnostic.

Both preregistered contrasts failed. Multiome pairs agreed less with each other (−0.139) than with the RNA-only floor (+0.080), paired Δ=−0.206 [−0.207, −0.205], and destroying the chromatin channel did not collapse the matrix. Refitting MultiVelo on resampled cells reproduces its own matrix at mean-centred cosine +0.872 (six refits, range +0.826 to +0.887), so the measure detects agreement where agreement exists. An earlier version of the shuffle comparison was not like-for-like (ceiling on 15,315 resampled cells, shuffle on all 21,878); repeating the shuffle on the *same* resampled cell sets puts the shuffled matrix below the intact refit range in three of three pairs (+0.784, +0.813, +0.810), with non-overlapping cell-bootstrap intervals. We therefore withdraw the earlier statement that chromatin is inert in this matrix. What replaces it is bounded: the paired differences are all positive but their magnitude varies two- to three-fold across shuffle draws, sits at a single-digit percentage of the +0.872 ceiling, and stays an order of magnitude below what method choice produces on the same measure (mean-centred cosine −0.530 to +0.131 across method pairs). A same-cell, same-configuration rerun null shows MultiVelo's fit is deterministic here (Δ_rr=0.000000), so the paired difference carries no refit-noise component to subtract; a matched rerun for MoFlow reproduces its matrix at +0.9999, so the near-zero cross-method values involving MoFlow read as genuine disagreement rather than arm instability. This positive statement is restricted to MultiVelo, to HSPC and to this shuffle design. The baseline contrast repeats outside HSPC in four of four external systems (paired per-cell Δ = −0.159, −0.152, −0.289, −0.184; all intervals excluding zero) against a sealed threshold of three of four; the external systems carry no shuffle arm and no refit, so neither the causal control nor the ceiling replicates there. This layer is a different target from the per-gene lag, and its numbers are not carried into the per-gene reliability map. The two layers are consistent rather than contradictory: the same class of shuffle does not perturb the priming-marker lags more than a bulk shuffle, yet it does move the cell×gene matrix a little.

### 4.9 Baseline-Feature Prediction

Real day0 ATAC promoter and enhancer accessibility (511 genes over 8,583 day0 HSC/MPP cells) predicted the robust target α on held-out lineages (ATAC-only ρ=+0.309, positive in all six lineages) but not the non-robust lag (ρ=+0.05, chance). The predictable signal is carried by transcript abundance: abundance alone predicts α at ρ=+0.724 on held-out lineages, real day0 ATAC adds no predictive power beyond it (Δρ=−0.016), and the abundance-controlled partial is +0.11. A within-method, cross-lineage refit tells the same story, with lag magnitude concording only weakly across separately fit lineages (median ρ=0.349, range 0.234 to 0.513) against its α_c control (median ρ=0.483).

### 4.10 The Reliability Map

Table 1 assembles the axes. Each row is one number a velocity model outputs per gene, with two evidence columns kept apart (reproducibility across methods, accuracy against a laboratory measurement) and a routing column stating what a downstream model should do with it: use it, use it only next to a simpler baseline, or not use it without an independent measurement. α is the only per-gene output that is reproducible, including beyond abundance; its accuracy beyond abundance is not shown. In operational form the rule is: enter transcript abundance first, add α only as its abundance-orthogonal component and keep it only if held-out performance improves, and do not consume a single-method lag, sign or γ without an orthogonal measurement. For the motivating timing task, baseline features predict α on held-out lineages (ATAC-only ρ=+0.309) but not the lag (ρ≈+0.05, chance), and day-0 ATAC adds nothing beyond abundance (Section 4.9).

<!-- FIG: fig_reliability_map -->

## 5. Discussion

### Limitations

The profile-likelihood result compares relative precision and depends on coordinates, and the stiffness-to-external-validation link is suggestive only. Bootstrap intervals do not cover cell sampling or refitting, and within-method stability was assessed only for MultiVelo. The five external systems test whether the α-over-lag ordering holds across tissues, species and protocols; each is a single donor or sample, so they do not measure donor-to-donor variation within a tissue, and multi-donor HSPC data are the next test. E18 lacks an independent MoFlow lag, and the α association rests on two measured TT-seq sources, both in K562 rather than HSPC, with the RNA-only floor replicating in only one. The abundance confound is unresolved, and all data are 10x Multiome. We audited per-gene parameters and the cell×gene matrix, not the embedding arrows or trajectories velocity is mostly used for, so nothing here establishes that trajectory inference is unreliable. ATAC-shuffle statements are bounded to HSPC, to cell-level pairing within lineage and, at the matrix layer, to MultiVelo, and the named-marker agreement is correlational, with a null marker-shuffle test and no replication in gastrulation. Finally, this concerns the reliability of current methods, not the absence of timing biology: deeper sequencing, finer time resolution or metabolic labeling could yet render the lag identifiable.

The baseline-to-α route was estimated with a linear model, so its weak expression-controlled accessibility signal might be a model-class artefact; an exploratory tree-ensemble re-run does not support that reading (a robustness note, not a result; details below).

Model-class robustness (exploratory; reported in Limitations, not as a result). Under the same leave-one-lineage-out protocol on six ATAC features: RidgeCV held-out ρ=+0.304, expression-controlled partial ρ=+0.109 (n=472); RandomForest +0.178 and +0.013; GradientBoosting +0.206 and +0.056. Per-feature correlations with fitted α: enhancer count +0.352, enhancer sum +0.318, enhancer accessibility +0.228, promoter-to-enhancer ratio −0.246, promoter accessibility −0.128, promoter count +0.046. Limits: one lineage-holdout protocol only, default hyperparameters with minimal regularization, and an expression control not matched line-for-line to the earlier analysis.

## 6. Conclusion

Among the per-gene quantities that multiome velocity models emit, only α is reproducible enough to consider as a downstream feature, and only as an addition to an abundance baseline. Before a model-derived quantity becomes a feature in a health-relevant predictor, sort it by cross-method reproducibility, an intervention on its claimed input, out-of-dataset replication and, where available, an external measurement. *Research and education use only; not clinical.*

## Table 1. Velocity-output reliability map and routing rule.

Reproducibility: do two reasonable methods, run on the same cells, rank genes the same way? Accuracy: has the number been compared with a laboratory measurement of the same rate, and with what result? Full evidence in Appendix B.

| Velocity output | Reproducibility | Accuracy | Routing rule |
|---|---|---|---|
| *Steady-state abundance (reference)* | *property of the data* | tracks measured synthesis at least as well as α (+0.41 vs +0.26) | enter first |
| Transcription rate α | reproducible (ρ=0.88), also beyond abundance (partial ρ=0.72) | associated with both synthesis references (multiome methods); not beyond abundance | add only its abundance-orthogonal part; keep if held-out performance improves |
| Population directional balance (~50/50) | reproducible as a population statement | n/a | do not read per gene |
| Canonical priming-marker direction | descriptive agreement in HSPC; not replicated | no causal support | do not generalize beyond the named loci |
| Chromatin-opening rate α_c | not reproducible (ρ=0.29) | n/a | stabilize before use |
| Degradation rate γ | not reproducible (ρ≈−0.1) | not recovered | do not use as-is |
| Per-gene lag magnitude | not reproducible under any definition (at best +0.36) | no measurement available | orthogonal validation required |
| Per-gene lag sign / absolute timing | not reproducible (54.6% agreement) | no measurement available | do not use |

## Figure legend

**Figure 1.** Cross-method agreement of α versus the per-gene lag in HSPC. (A) α, MultiVelo versus MultiVeloVAE on 538 shared genes (ρ=+0.882). (B) Spearman ρ with 95% CI for α, α_c and every lag definition: MultiVelo priming interval and coupled-on length against the MultiVeloVAE rate proxy, one identical formula in both methods (signed, magnitude), and MultiVelo priming against MoFlow (537 genes); Δρ = ρ_α − ρ_output on the same bootstrap draw. Definitions in Table A2. Source figure: `fig01_concordance_v2.png`.

**Figure: figT01_atac_shuffle_priming.png.** Within-lineage ATAC shuffle and the MultiVelo priming interval in HSPC (n=538 genes). (A) Per-gene priming interval with observed ATAC (median 4.61) and with ATAC permuted across cells within each lineage (median 5.00); Mann–Whitney p=0.65, Kolmogorov–Smirnov p=0.46. (B) Shuffled versus observed priming interval per gene, Spearman ρ=+0.753 [+0.695, +0.806]; dashed line, identity. One shuffle realization is shown.

## Acknowledgements

The authors thank Pseudo Lab, a non-profit AI/ML research community, for providing the collaborative environment that brought the authors together and enabled this research, and Sangjun Park (Yonsei University) for the initial conceptual idea of the project and for reference-literature analysis. This research was supported by the "Open Source AI·SW Developer and Community Support Program" funded by the Ministry of Science and ICT (MSIT), Republic of Korea.

## References

Reference numbers are inherited from the full-length version of this work so that every value in the main text stays traceable to its source; the numbering is therefore not contiguous.

[1] La Manno G, Soldatov R, Zeisel A, et al. RNA velocity of single cells. *Nature* 560(7719), 494-498 (2018). doi:10.1038/s41586-018-0414-6.
[2] Cao J, Cusanovich DA, Ramani V, et al. Joint profiling of chromatin accessibility and gene expression in thousands of single cells. *Science* 361(6409), 1380-1385 (2018). doi:10.1126/science.aau0730.
[3] Li C, Virgilio MC, Collins KL, Welch JD. Multi-omic single-cell velocity models epigenome-transcriptome interactions and improves cell fate prediction. *Nature Biotechnology* 41, 387-398 (2023). doi:10.1038/s41587-022-01476-y.
[4] Li C, Gu Y, Virgilio MC, Lee KH, Collins KL, Welch JD. Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE. *Nature Communications* 16, 11505 (2025). doi:10.1038/s41467-025-66287-6.
[5] Hong A, Lee S, Kim K. Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states. *Nature Communications* 17, 566 (2026). doi:10.1038/s41467-025-67259-6.
[6] El Kazwini N, Gao M, Kouadri Boudjelthia I, Cai F, Huang Y, Sanguinetti G. CRAK-Velo: chromatin accessibility kinetics integration improves RNA velocity estimation. *Genome Biology* 27(1), 209 (2026). doi:10.1186/s13059-026-04086-y.
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
[41] Zhang H, Bochkina N, Wade S. Quantifying uncertainty in RNA velocity. *Biometrics* 82(1), ujag018 (2026). doi:10.1093/biomtc/ujag018.
[44] Milacic M, Beavers D, Conley P, et al. The Reactome Pathway Knowledgebase 2024. *Nucleic Acids Research* 52(D1), D672-D678 (2024). doi:10.1093/nar/gkad1025.
[48] Schuirmann DJ. A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability. *Journal of Pharmacokinetics and Biopharmaceutics* 15(6), 657-680 (1987). doi:10.1007/bf01068419.
[49] Nosek BA, Ebersole CR, DeHaven AC, Mellor DT. The preregistration revolution. *Proceedings of the National Academy of Sciences* 115(11), 2600-2606 (2018). doi:10.1073/pnas.1708274114.
[50] Todorovski I, Tsang MJ, Feran B, et al. RNA kinetics influence the response to transcriptional perturbation in leukaemia cell lines. *NAR Cancer* 6(4), zcae039 (2024). doi:10.1093/narcan/zcae039. (GSE229305 synthesis; SLAM-seq half-lives in the parent SuperSeries GSE229314.)
[51] Raue A, Kreutz C, Maiwald T, et al. Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood. *Bioinformatics* 25(15), 1923-1929 (2009). doi:10.1093/bioinformatics/btp358.
[52] Kreutz C, Raue A, Kaschek D, Timmer J. Profile likelihood in systems biology. *The FEBS Journal* 280(11), 2564-2571 (2013). doi:10.1111/febs.12276.
[53] Villaverde AF, Barreiro A, Papachristodoulou A. Structural identifiability of dynamic systems biology models. *PLOS Computational Biology* 12(10), e1005153 (2016). doi:10.1371/journal.pcbi.1005153.
[55] Gu J, Laszik N, Miles CE, Allard J, Downing TL, Read EL. Scalable inference and identifiability of kinetic parameters for transcriptional bursting from single cell data. *Bioinformatics* 41(11), btaf581 (2025). doi:10.1093/bioinformatics/btaf581.
[62] Kaminow B, Yunusov D, Dobin A. STARsolo: accurate, fast and versatile mapping/quantification of single-cell and single-nucleus RNA-seq data. bioRxiv (2021). doi:10.1101/2021.05.05.442755. [Preprint, not peer-reviewed.]
[66] Bergen V, Lange M, Peidli S, Wolf FA, Theis FJ. Generalizing RNA velocity to transient cell states through dynamical modeling. *Nature Biotechnology* 38(12), 1408-1414 (2020). doi:10.1038/s41587-020-0591-3.
[67] Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society Series B* 57(1), 289-300 (1995). doi:10.1111/j.2517-6161.1995.tb02031.x.
[68] Xie Z, Bailey A, Kuleshov MV, et al. Gene set knowledge discovery with Enrichr. *Current Protocols* 1(3), e90 (2021). doi:10.1002/cpz1.90.
[71] Wolock SL, Lopez R, Klein AM. Scrublet: computational identification of cell doublets in single-cell transcriptomic data. *Cell Systems* 8(4), 281-291.e9 (2019). doi:10.1016/j.cels.2018.11.005.

## Appendix

### A. Cross-Dataset Table for All Five External Systems

**Table A1. All five external systems (not like-for-like).**

Within-dataset α is the median of the three cross-method pairs (floor, MultiVelo, MultiVeloVAE); within-dataset lag is the MultiVelo versus MultiVeloVAE magnitude pair, except human fetal cortex, which has no MultiVeloVAE fit and is supplied by a MultiVelo versus MoFlow pair. Cross-dataset entries are HSPC-to-external magnitude-rank ρ; within-dataset α spans +0.810 to +0.927 and within-dataset lag −0.088 to +0.074, cross-dataset α +0.321 to +0.643 against lag +0.028 to +0.185. Cross-dataset α intervals overlap, so the tissue-distance ordering is qualitative. Each replication is one donor or sample.

| System | Tissue relation | Within-dataset α | Within-dataset lag | Cross-dataset α | Cross-dataset lag |
|---|---|---|---|---|---|
| HSPC (GSE209878) | primary | +0.882 | +0.163 [+0.078, +0.244] | n/a | n/a |
| Macrophage (GSE284047) | HSPC-direct | +0.865 | +0.074 [+0.006, +0.143] | +0.643 [+0.554, +0.719] | +0.148 [+0.027, +0.263] |
| Human BMMC (GSE194122) | same tissue | +0.851 | −0.088 [−0.209, +0.034] | +0.550 [+0.368, +0.696] | +0.052 [−0.164, +0.262] |
| Human fetal cortex (GSE162170) | distant | not computable | −0.052 [−0.135, +0.029] | +0.475 [+0.292, +0.626] | +0.185 [−0.005, +0.369] |
| Mouse gastrulation (GSE205117) | priming-maximal | +0.927 | −0.026 [−0.089, +0.038] | +0.415 [+0.244, +0.561] | +0.028 [−0.165, +0.224] |
| E18 mouse brain (10x demo) | cross-species | +0.810 | +0.057 [−0.005, +0.118] | +0.321 [+0.158, +0.472] | +0.105 [−0.069, +0.269] |

### B. Reliability Map, Full Five-Column Version

Main-text Table 1 is condensed to three columns. The internal-axis and external-anchor evidence behind each verdict is given here.

| Velocity output | Reproducibility evidence | Accuracy evidence | Verdict | Routing rule |
|---|---|---|---|---|
| *Steady-state abundance (reference, not a velocity output)* | property of the data | tracks measured synthesis at least as strongly as α (+0.41 versus +0.26) | *reference baseline* | enter first |
| Transcription rate α | high (ρ=0.88; floor recovers it); partial ρ given abundance +0.715 | associated with both synthesis references (non-HK ρ +0.24 to +0.29; second source +0.24 to +0.27 for the multiome methods, RNA-only null); not shown beyond abundance | reproducible beyond abundance; kinetic content not established | add only its abundance-orthogonal part; keep it only if held-out performance improves |
| Population directional balance (~50/50) | high (two methods converge) | n/a | reliable as a population statement | do not read per gene |
| Canonical priming-marker direction | limited descriptive agreement in HSPC; not replicated in gastrulation | no causal support (marker-shuffle p=0.58) | hypothesis-generating only | do not generalize beyond the named loci |
| Chromatin-opening rate α_c | low (ρ=0.29) | n/a | unreliable | stabilize before use |
| Degradation rate γ | low (ρ≈−0.1) | not recovered (K562 3/3 null; scVelo γ reversed, −0.224) | unreliable | do not use as-is |
| Per-gene lag magnitude | low under every definition (at best +0.364; −0.009 with one identical formula) | no measured counterpart; not predictable from baseline (≈chance) | unreliable | orthogonal validation required |
| Per-gene lag sign / absolute timing | 54.6% agreement; MultiVelo structurally positive | n/a | unreliable (uninformative) | do not use |

### C. Data and Code Availability

All primary and external datasets are public under the accessions listed in Section 3.1. Analysis code, per-gene result tables, the sealed preregistration, environment files and the deterministic recomputation scripts are at https://github.com/biospin/BioProject01 (MIT licence; release ml4h2026-camera-ready), archived as <FILL: Zenodo DOI>.
