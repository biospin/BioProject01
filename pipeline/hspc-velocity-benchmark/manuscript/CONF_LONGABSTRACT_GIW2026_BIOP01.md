<!--
════════════════════════════════════════════════════════════════════════
한국어 메모 (제출 전 제거) — v2, 2026-10-23
════════════════════════════════════════════════════════════════════════
학회: BIOINFO 2026 / GIW XXXV / ISCB-Asia (2026-11-17~20, 연세대). #241 구두발표 채택(BIOP01-87).
v2 = ML4H Submission 294 반박문(10/13)에서 인정·약속한 정정을 반영한 판. 추적 카드 BIOP01-90.
v1(8/15 제출본, 94aa054)과의 차이:
- MultiVelo lag 주 정의를 priming interval(t_sw1)로 바꿨다. 기존 t_sw2−t_sw1은 coupled-on 길이이며 민감도 분석으로 둔다.
  방법별 추정량은 Methods에 명시했다.
- 곡률 비율은 log 좌표의 상대 정밀도 비교로 낮췄다. 범위 비율 좌표에서는 0.10으로 뒤집히고, 경계 고정 199/205가 induction-only다.
- lag 결론을 "판별 불가"에서 "방법 간 재현 안 됨"으로 바꿨다(MultiVelo 재적합 +0.624).
- ATAC 셔플은 "세포 수준 짝 파괴"로 좁혔다. "chromatin이 기여하지 않는다"는 삭제했다.
- α: 발현량 보정 후 +0.715로 재현은 되지만, kinetic 정보라는 근거는 없다. 합성 참조 두 곳 중 한 곳과만 연관된다.
- 외부 데이터셋 주 수치를 같은 유전자 짝 Δρ로 바꿨다(macrophage +0.843, gastrulation +0.979). 사전등록은 gastrulation뿐이다.
- 신뢰도 지도를 재현성·정확성·routing 3열로 바꿨다. routing은 "발현량을 먼저, α는 직교 성분만"이다.
수치 출처:
- 새 수치는 results/post_review_robustness.gen.md(R1~R5, scripts/p17_post_review_robustness.py)와 results/bootstrap_refit.md에서 왔다.
- 외부 짝 Δρ는 ML4H 원고 Appendix C에서 왔다. 나머지는 v1 출처를 그대로 따른다(draft_v2, FINDINGS).
아직 coupled-on 정의 값인 것: ATAC 셔플 per-gene ρ=0.72, 재적합 lag +0.624. 본문에 정의를 표기했다.
priming 기준 재계산에는 HPC 셔플·refit 결과가 필요하다.
그림: figures/fig01_concordance_v2.py, figures/fig07_reliability_map_v2.py. 두 스크립트 모두 표시 수치를 위 출처와 대조하고, 불일치하면 멈춘다.
빌드: manuscript/conf_giw2026/README.md
════════════════════════════════════════════════════════════════════════
-->

# A reliability map for per-gene multiome RNA velocity parameters in single-cell kinetics

*(GIW/ISCB-Asia 2026 — oral track long abstract. Authors and affiliations withheld for blind review.)*

## Background and motivation

Multiome RNA-velocity methods emit several per-gene quantities, each offered as a biological
readout: a transcription rate α, a degradation rate γ, and a chromatin-to-transcription lag offered
as a clock for regulatory timing. A derived quantity is usable as a feature only if it is
reliable, and reliability is testable: it should reproduce when a different algorithm is run on the
*same* cells, hold up in independent data, and agree with an external measurement of the same rate
where one exists — axes rarely applied to individual velocity outputs. Recent general benchmarks
score velocity at the embedding and transition-vector level and report method-dependent direction
[25,26,27], but neither sort the per-gene outputs by reliability nor anchor them to an external
measurement. We ask not "which method wins" but how to measure the reliability of a velocity
output, and build a map telling an analyst which outputs to trust and which need orthogonal
validation.

## Methods: a four-axis reliability protocol

We ran up to five velocity arms — an RNA-only scVelo floor [1,9] plus four chromatin-informed
methods (MultiVelo [3], MultiVeloVAE [4], MoFlow [5], CRAK-Velo [6]) — on human hematopoietic stem
and progenitor cells (10x Multiome, GSE209878; day0+day7 integrated, 21,878 cells), branching from a
common preprocessing. The methods do not estimate the same lag: MultiVelo's priming interval
(t_sw1; coupled-on duration t_sw2 − t_sw1 as sensitivity), MultiVeloVAE's rate proxy 1/α_c − 1/α,
and dynamic-time-warping offsets for MoFlow and CRAK-Velo. Each
per-gene output was tested on four axes. **(1) Cross-method reproducibility:** rank agreement on one
method pair and one shared gene set, under every lag definition, with a gene-label permutation-FDR
test (N=10⁴). **(2) Within-lineage ATAC shuffle:** within each lineage we permuted ATAC profiles
across cells, which destroys cell-level chromatin–RNA pairing while preserving lineage-level
chromatin distributions, and re-fit. **(3) Cross-dataset replication** in five external multiomes
spanning tissue distance (human fetal cortex, E18 mouse brain, same-tissue human BMMC, HSPC-derived
macrophages, mouse gastrulation), the last against six predictions sealed before fitting.
**(4) External anchoring:** fitted α against measured synthesis rates (K562 TT-seq; a second source
as replication) and fitted γ against measured mRNA half-life (SLAM-seq), with transcript abundance
as a competing baseline. CIs are paired gene bootstraps conditional on the fits, checked against a
co-expression-module bootstrap.

## Results

**Among the per-gene outputs, α reproduces across methods; the lag does not, under any definition.**
α reproduced at Spearman ρ=+0.882 [+0.856, +0.904] (MultiVelo vs MultiVeloVAE, 538 genes), and the
RNA-only floor recovered it too (+0.82 to +0.89). On
the same genes the lag reached +0.364 [+0.285, +0.440] with MultiVelo's priming interval and +0.163
[+0.078, +0.247] with the coupled-on duration; computing both methods' lags from one identical formula
did not raise agreement (signed +0.124, magnitude −0.009). Against MoFlow the lag did not reproduce
(priming +0.038 [−0.046, +0.122]). Every α-minus-lag contrast excluded zero (smallest Δρ +0.518
[+0.441, +0.596]), also under the module bootstrap (Figure 1). Direction stayed near balance (sign agreement 54.6%, n=560;
chromatin-leads fractions 41–49%), so a genome-wide "chromatin primes transcription" ordering is not
supported. Within one method the lag is moderately stable (MultiVelo refit on 12 overlapping 70%
subsamples: coupled-on lag +0.624, α +0.949), so the failure is reproducibility across methods and
definitions, not necessarily within-method noise. γ was fragile (ρ≈−0.11) and did not recover a
measured half-life (RNA-only scVelo ran reversed, −0.224).

**The lag survives destruction of cell-level chromatin pairing (axis 2).** Shuffling ATAC across
cells within lineage left the MultiVelo lag distribution statistically unchanged (Mann–Whitney
p=0.20, KS p=0.51), preserved its per-gene ranking (ρ=0.72, coupled-on definition) and left the
chromatin likelihood unchanged (0.239→0.237). The fitted lag therefore depends little on which cell's chromatin is paired
with which cell's RNA. Because the shuffle preserves lineage-level chromatin, this does not show that
chromatin contributes nothing overall; the cell×gene velocity matrix, a separate target, shows a
small bounded chromatin contribution.

**The α-over-lag ordering replicates, including under preregistration (axis 3).** On the same genes
and method pair, α exceeded the lag in HSPC-derived macrophages (Δρ +0.843 [+0.773, +0.912]) and
mouse gastrulation (+0.979 [+0.916, +1.041]). Cross-dataset α decayed with tissue distance yet stayed
reproducible (+0.643 to +0.32) while the lag stayed low (+0.03 to +0.19; method pairs differ by
dataset). Mouse gastrulation, the only preregistered system,
passed six-of-six predictions sealed before fitting; HSPC and the other systems were not preregistered.

**α is reproducible beyond abundance, but its kinetic accuracy is not established (axis 4).**
Fitted α tracked the measured TT-seq synthesis rate (non-housekeeping ρ +0.24 to +0.29), but the
second synthesis source was null, and transcript abundance tracked the first at least as strongly
(+0.410 versus +0.262). After removing mean expression from both methods' α, cross-method agreement
remained high (partial Spearman +0.715 [+0.659, +0.765], from +0.882) while the lag stayed low
(+0.182). α therefore carries a method-independent component beyond expression level, but that
component has not been shown to be kinetic; it may come from the unspliced and spliced counts both
methods read.

**Profile likelihood gives relative precision, not a coordinate-free identifiability claim.** In log
coordinates on MultiVelo's objective, α is located more tightly relative to its own magnitude than
the lag (median curvature ratio 3.53, α tighter in 95% of 258 interior-lag genes; 2.49 with nuisance
parameters freed, on the 148 genes with positive curvature on both axes). The comparison depends on
coordinates: expressing the lag as a fraction of the pseudotime horizon reverses the ratio (0.10),
and neither choice is canonical. Most boundary-pinned lags (199 of 205) come from induction-only
fits, reflecting trajectory coverage more than non-identifiability. We therefore claim cross-method
non-reproducibility, not strict non-identifiability; ConsensusVelo's weakly identified switch times
[41] are consistent with this reading but do not prove it.

## Conclusion

We distil these axes into a velocity-output **reliability map** that keeps two kinds of evidence
apart (Figure 2): *reproducibility* — do two reasonable methods, run on the same cells, rank genes the
same way? — and *accuracy* — has the number been compared with a laboratory measurement of the same
rate, and with what result? α is the only per-gene output that is reproducible, including beyond
abundance; its accuracy beyond abundance is not shown. Two further outputs are usable only as
population statements (the near-50/50 directional balance and the direction agreement of canonical
priming markers, which is correlational). The chromatin-opening
rate α_c (ρ=0.29), γ, and the per-gene lag magnitude, sign and timing under every definition tested
are not reproducible. The routing rule follows: enter transcript abundance first, add α only as its
abundance-orthogonal component and keep it only if held-out performance improves, and do not consume
a single-method lag, sign or γ without an orthogonal measurement. Baseline features predict α on
held-out lineages (ρ=+0.31) but not the lag (ρ≈0.05), and day-0 accessibility adds nothing beyond
abundance (Δρ −0.02). Limits: pseudotime is not wall-clock; external replications are single-sample (no donor
variation); the α anchor is one of two sources, measured in K562 rather than HSPC; within-method
stability was assessed for MultiVelo only; and we audited per-gene parameters, not trajectories.

## Figure legends

**Figure 1.** Cross-method agreement of α versus the per-gene lag in HSPC. (A) α, MultiVelo vs
MultiVeloVAE on 538 shared genes (ρ=+0.882). (B) Spearman ρ with 95% CI for α, α_c and every lag
definition: MultiVelo priming interval and coupled-on duration against the MultiVeloVAE rate proxy,
one identical formula in both methods (signed, magnitude), and MultiVelo priming against MoFlow
(537 genes); Δρ = ρ_α − ρ_output on the same bootstrap draw. Source: `figures/fig01_concordance_v2.png`.

**Figure 2.** Velocity-output reliability map. Rows are per-gene outputs; columns are reproducibility
evidence (cross-method, cross-dataset), accuracy evidence (comparison with a measured rate, and
whether it exceeds abundance) and the routing decision (use; use only beside an abundance baseline;
do not use without an independent measurement). Source: `figures/fig07_reliability_map_v2.png`.

## References

[1] La Manno G, Soldatov R, Zeisel A, et al. RNA velocity of single cells. *Nature* 560, 494–498 (2018). doi:10.1038/s41586-018-0414-6.
[3] Li C, Virgilio MC, Collins KL, Welch JD. Multi-omic single-cell velocity models epigenome–transcriptome interactions and improves cell fate prediction. *Nature Biotechnology* 41, 387–398 (2023). doi:10.1038/s41587-022-01476-y.
[4] Li C, Gu Y, Virgilio MC, Lee KH, Collins KL, Welch JD. Inferring differential dynamics from multi-lineage, multi-omic, and multi-sample single-cell data with MultiVeloVAE. *Nature Communications* 16, 11505 (2025). doi:10.1038/s41467-025-66287-6.
[5] Hong A, Lee S, Kim K. Multi-omic relay velocity modeling uncovers dynamic chromatin-transcription regulation across cell states. *Nature Communications* 17, 566 (2025). doi:10.1038/s41467-025-67259-6.
[6] El Kazwini N, Gao M, Kouadri Boudjelthia I, Cai F, Huang Y, Sanguinetti G. CRAK-Velo: chromatin accessibility kinetics integration improves RNA velocity estimation. *Genome Biology* 27(1) (2026). doi:10.1186/s13059-026-04086-y.
[9] Gayoso A, Weiler P, Lotfollahi M, et al. Deep generative modeling of transcriptional dynamics for RNA velocity analysis in single cells. *Nature Methods* 21, 50–59 (2024). doi:10.1038/s41592-023-01994-w.
[25] Luo Y, Ren J, Yang Q, You Z, Zhou Y, Qin Q, Li Q. Benchmarking RNA velocity methods across 17 independent studies. *Cell Reports Methods* 6(4), 101367 (2026). doi:10.1016/j.crmeth.2026.101367.
[26] Huang K, Zhou Y, Wang T, et al. Benchmarking algorithms for RNA velocity inference. bioRxiv 2026.01.03.697314 (2026). [Preprint.]
[27] Wu Y, Kong C, Liao X, Lin Z, Sun X, Liu J. Comprehensive benchmarking of RNA velocity methods across single-cell datasets. *Genome Biology* 27(1), 242 (2026). doi:10.1186/s13059-026-04182-z.
[41] Zhang et al. Quantifying uncertainty in RNA velocity (ConsensusVelo). bioRxiv 2024.05.14.594102 (2024); *Biometrics* (in press). [Full author list/final venue to confirm.]

*Research/education use only; not clinical.*
