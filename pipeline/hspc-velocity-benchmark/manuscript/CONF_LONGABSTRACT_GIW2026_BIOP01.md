<!--
════════════════════════════════════════════════════════════════════════
한국어 메모 (제출 전 제거) — 출처·framing·미확정
════════════════════════════════════════════════════════════════════════
학회: BIOINFO 2026 / GIW XXXV / ISCB-Asia (2026-11-17~20, 연세대). 트랙: talk and poster (BIOP01-86 확정 → 이 2p long abstract 필요).
정합 기준: 이 문서는 199단어 블라인드 초록(CONF_ABSTRACT_GIW2026_BIOP01.md, 커밋 b478f00)과 정합해야 한다.
정본(수정 금지, 읽기만): draft_v2.md, results/FINDINGS.md, CLAIMS.yaml.

수치 출처(전부 실측 — 지어낸 값 없음):
- α cross-method ρ=0.88(=+0.882): FINDINGS §1, draft L105/L127.
- lag magnitude strongest pair MV×MVVAE +0.163 [95%CI +0.078,+0.244], most pairs |ρ|≤0.08; signed 3-way {−0.04,−0.01,+0.08}: FINDINGS §1, draft L67.
- sign-agreement 54.6%(n=560, binomial p=0.03); chromatin-leads MoFlow 44.8%/MVVAE 49.3%/CRAK 41.1%: FINDINGS §1, draft L67.
- ATAC-shuffle(=per-gene lag 층): 분포 통계 동일 MW p=0.20, KS p=0.51, per-gene lag ρ=0.72, chromatin likelihood 0.239→0.237; marker lag MW p=0.58: FINDINGS §2, draft L127/L171.
- γ: cross-method ρ≈−0.109; multiome(MV/MVVAE) 외부회수 null; RNA-only scVelo γ 역방향 −0.224: FINDINGS §1·§8, draft L105/L107.
- α↔synthesis +0.24~+0.29(+0.262); abundance↔synthesis +0.410; α↔abundance +0.809; cross-method α +0.882: draft L171, FINDINGS §10.
- cross-dataset α: macrophage +0.643 > BMMC +0.55 > human_brain +0.475 > gastrulation +0.415 > E18 +0.32; lag +0.03~+0.19: FINDINGS §7.
- 사전등록 gastrulation 6/6 PASS: FINDINGS §7-E, prereg_gse205117_scorecard.md.
- profile-likelihood freed-nuisance 2.49×, α stiffer 77%(3.53×/94.57%=상한): FINDINGS §8, draft L171. ConsensusVelo[41] 정면 인용 의무.
- baseline→α: real day0 ATAC ρ=+0.309(6/6 lineage 양수), lag ρ≈+0.05(chance), abundance가 α 운반 ρ=+0.72, ATAC 추가효과 Δρ=−0.02: FINDINGS §6·L177.

FRAMING(BIOP01-86 지침):
- 차별점 = "velocity 출력 신뢰도를 어떻게 재는가 = 4축 방법론"(negative result 아님). Methods를 앞세움.
- 결과는 정직: α만 per-gene method-robust(집단수준 robust 2종=50/50 balance + canonical marker direction은 별도로 명시). lag·γ 비robust. α의 synthesis 추적은 abundance confound로 α-specific 아님(+0.410 vs +0.262 반드시 본문 명시).
- 결론 = reliability map + routing rule. overclaim 금지.

⚠️ 층 구분(필수, critic 지시): "ATAC-shuffle 인과대조"는 **per-gene lag 층** 결과다(lag이 chromatin-shuffle 불변 → model-structural). draft L113~123의 **cell×gene velocity-matrix 층**은 별개 target이고, 거기선 "chromatin inert" 주장을 철회하고 작지만 유계한 chromatin 기여를 인정했다. 이 long abstract는 4축의 causal control을 per-gene lag 층으로만 서술하고, matrix 층 수치를 끌어오지 않는다.

미확정(<FILL>) / 확인필요:
- 저자·소속·corresponding email: 블라인드 제출이라 미기재. 최종 kkkim 확정.
- Figure 2(reliability map/routing) = draft_v2 Fig. 7 "main; new" — 렌더 완료(figures/fig07_reliability_map.py → fig07_reliability_map.png, 300dpi). 본문 Source 파일명 채움. 축 명칭 충돌 해소(2026-08-10): fig07은 정본 draft_v2 L301대로 4열=cross-method reproducible/chromatin-causal/baseline-predictable/measurement-corroborated로 렌더. Figure 2 legend를 그림·정본에 맞춰 baseline-predictable로 정정함(cross-dataset replicable 폐기). 주의: 이 map 4열은 Methods의 '4축 평가 프로토콜'(cross-method·causal·cross-dataset·external anchor)과 3열째가 다르다 — map은 Table 2를 시각화한 synthesis라 routing에 직결되는 baseline-predictability를 열로 쓰고 cross-dataset은 robustness 증거축으로 본문(axis 3)에만 둔다. draft_v2도 동일 구조(평가 4축 ≠ Fig.7 4열).
- Fig1 = fig01_p2_concordance.png (실재). 참고: 과업이 부른 "4축 개요 도식"은 렌더본 없음(fig04_harness_concept.png는 하네스 개념도이지 4축 도식 아님) → 필요 시 별도 렌더 <FILL>.
- Framing 충돌 메모: critic(초록 주석 L36)은 Fig1+Fig4(abundance bar) 선호, 과업(BIOP01-86)은 Fig1+Fig7 지정. 과업을 따르되 abundance confound 수치(+0.410 vs +0.262)를 Results 본문에 명시해 보완함.
- ⚠️ human cortex(GSE162170) 발생단계: 본 초록은 "human fetal cortex"로 표기(GSE162170=Trevino 발생기 대뇌피질, draft_v2 L123 "Human fetal cortex", 과업 브리핑 "human fetal cortex"와 정합). 단 FINDINGS §7-A는 "성인 human_brain"로 적혀 있어 불일치 — FINDINGS 오기로 판단하나 kkkim 최종 확인 요망.
- ⚠️ γ 외부 앵커(측정 degradation rate/half-life) 출처 미확정: synthesis 앵커=Todorovski 2024 K562 TT-seq(검증됨), 그러나 γ가 대조된 "measured degradation rate/half-life"의 assay 출처는 read한 파일에서 확정 못 함(Schwalb decay는 QC2 null로 배제됨). 본문은 "measured degradation rate"로만 표기(TT-seq 귀속 제거). 출처 확정 후 병기 → <FILL: γ 외부 앵커 출처>.
- 분량: 본문 ~1250단어(가이드 900~1100 초과, 수치 밀도상 추가 압축은 필수내용 손실). 2p 적합 여부는 Fig.2 렌더 후 조판에서 확인 필요.
════════════════════════════════════════════════════════════════════════
-->

# A reliability map for per-gene multiome RNA velocity parameters in single-cell kinetics

*(GIW/ISCB-Asia 2026 — oral track long abstract. Authors and affiliations withheld for blind review.)*

## Background and motivation

Multiome RNA-velocity methods emit several per-gene quantities, each offered as a biological
readout: a transcription rate α, a degradation rate γ, and a chromatin-to-transcription lag meant to
say which genes have chromatin opening ahead of transcription. Downstream analyses increasingly
consume these quantities directly, for example to order genes by regulatory timing. A derived
quantity is usable only if it is reliable, and reliability is testable: the quantity should reproduce
when a different algorithm is run on the *same* cells, should not be an artifact of model structure,
should hold up in independent data, and should agree with an external measurement of the same rate
where one exists. These axes are rarely applied to the individual velocity outputs. Recent general
benchmarks score velocity at the embedding and transition-vector level and report that direction is
method-dependent [25,26,27], but they neither sort the per-gene outputs by reliability nor anchor them
to an external measurement. We therefore ask not "which method wins" but "how does one measure the
reliability of a velocity output", and build a reliability map telling a downstream analyst which
outputs to trust directly and which require orthogonal validation.

## Methods: a four-axis reliability protocol

We ran up to five velocity arms — an RNA-only scVelo floor [1,9] plus four chromatin-informed
methods (MultiVelo [3], MultiVeloVAE [4], MoFlow [5], CRAK-Velo [6]) — on human hematopoietic stem
and progenitor cells (10x Multiome, GSE209878; day0+day7 integrated, 21,878 cells), branching from a
common preprocessing so method differences are not confounded by preprocessing. Each per-gene output
was tested on four axes. **(1) Cross-method reproducibility:** pairwise rank agreement across arms on
a shared gene axis, with a gene-label permutation-FDR agreement test (N=10⁴). **(2) Causal
ATAC-shuffle control:** within each lineage we permuted the ATAC signal to break the chromatin↔RNA
coupling and re-fit, asking whether the per-gene lag depends on chromatin at all. **(3) Cross-dataset
replication:** the ordering was re-tested in five external multiomes spanning tissue distance (human
fetal cortex, fetal E18 mouse brain, same-tissue human BMMC, HSPC-direct macrophage, developmental
mouse gastrulation), the last against six predictions sealed before fitting. **(4) External
anchoring:** fitted α was compared to a measured synthesis rate (K562 TT-seq) and fitted γ to a
measured degradation rate, with transcript abundance as a competing baseline. All headline
correlations carry paired-bootstrap 95% CIs.

## Results

**Among the per-gene outputs, only α reproduces across methods.** The transcription rate α reproduced at Spearman ρ=0.88
(cross-method +0.882) and was recovered even by the RNA-only floor, which has no chromatin channel
(floor vs MultiVelo +0.818; floor vs MultiVeloVAE +0.889). The per-gene lag did not reproduce: under
its original signed definition the three HSPC pairs were −0.04, −0.01 and +0.08, and under a magnitude
convention the strongest pair (MultiVelo vs MultiVeloVAE) reached only +0.163 (95% CI
[+0.078, +0.244]), with most pairs at |ρ|≤0.08 (Figure 1). Direction was at chance: per-gene
sign-agreement between the two sign-variable methods was 54.6% (n=560, binomial p=0.03), and the
chromatin-leads fraction was balanced near 50/50 (MoFlow 44.8%, MultiVeloVAE 49.3%, CRAK-Velo 41.1%),
so a genome-wide "chromatin primes transcription" ordering is not supported. A fourth method did not
rescue concordance (MoFlow vs CRAK-Velo −0.151). γ was fragile too (cross-method ρ≈−0.11): the
multiome methods did not recover a measured half-life, and the RNA-only scVelo γ ran reversed against
it (−0.224).

**The lag is model-structural, not chromatin-driven (axis 2).** At the per-gene lag layer, shuffling
ATAC within lineage left the lag distribution statistically unchanged (Mann–Whitney p=0.20, KS p=0.51;
per-gene lag ρ=0.72 preserved; chromatin likelihood 0.239→0.237) and did not perturb the canonical
priming-marker lags more than a bulk shuffle (Mann–Whitney p=0.58). The MultiVelo lag therefore comes
from its switch-time ordering constraint and gene-intrinsic RNA dynamics rather than from chromatin,
which is why "which gene is chromatin-leading" flips with the method. (A separate audit of the
cell×gene velocity matrix, a different target, detected a small, bounded, direction-only chromatin
contribution; we keep that layer distinct and do not carry its numbers into the per-gene map.)

**The ordering replicates, including under preregistration (axis 3).** The α-robust/lag-fragile
ordering held in the four externals carrying a second multiome arm (within-dataset α medians +0.81 to
+0.93 versus lag near zero), and cross-dataset α decayed monotonically with tissue distance yet stayed
reproducible (HSPC-direct macrophage +0.643 > BMMC +0.55 > human cortex +0.475 > gastrulation +0.415 >
E18 +0.32) while the lag was signal-free everywhere (+0.03 to +0.19). In gastrulation, the
priming-maximal system, six sealed predictions passed six-of-six without post-hoc rescue.

**α agrees with a measured rate, but not α-specifically (axis 4).** Fitted α tracked the measured
TT-seq synthesis rate (non-housekeeping ρ +0.24 to +0.29). This is corroboration but not α-specific
accuracy: transcript abundance tracked the same measurement at least as strongly
(Spearman(abundance, synthesis) +0.410 versus Spearman(α, synthesis) +0.262). α is not a mere renaming
of abundance — two independent methods agree on α (+0.882) slightly more than α resembles abundance
(+0.809), leaving a small *reproducible* kinetic signal — but the external match is consistency
evidence, not a claim that α is the most accurate synthesis estimator.

**Why the lag fails.** On MultiVelo's own objective function α is stiff (identifiable) while the lag is
sloppy and boundary-limited (conservative freed-nuisance curvature ratio 2.49×, α stiffer in 77% of
genes). ConsensusVelo already showed the weak identifiability of velocity switch-times [41]; that work
is confirmatory of our mechanism, and our contribution is the α-stiff/lag-sloppy *dissociation* in the
multiome setting.

## Conclusion

We distil these axes into a velocity-output **reliability map** with an explicit routing rule
(Figure 2). Exactly one per-gene output is reliable on the internal axis and corroborated on the
external axis — the transcription rate α. Two further outputs are usable only as population statements
(the ~50/50 directional balance and the cross-method direction agreement of canonical priming markers,
a correlational fact we do not upgrade to causation). Everything else is unreliable: the
chromatin-opening rate α_c (ρ=0.29), γ, and the per-gene lag magnitude, sign and absolute timing. The
routing rule follows: consume α and rate-derived signals directly, and do not consume a single-method
lag, sign or γ without an orthogonal measurement. For downstream timing prediction this yields a
concrete design principle — route from baseline features to α, where the same baseline that fails to
predict the lag (ρ≈0.05) predicts α on held-out lineages (ρ=+0.31), rather than through a single-method
lag. This bounds the reliability of the current methods, not the existence of timing biology: deeper
sequencing or metabolic labeling could yet render the lag identifiable. Load-bearing limits: pseudotime
is not wall-clock; the lag-fragile leg outside HSPC rests largely on a single method pair; the five
external replications are single-sample; the α anchor carries the abundance confound and rests
primarily on one TT-seq source; and we audited per-gene kinetic parameters, not the embedding-level
trajectories velocity is principally used for.

## Figure legends

**Figure 1.** Cross-method concordance of the per-gene lag versus the transcription rate α in HSPC.
Lag-magnitude pairwise rank agreement (most pairs |ρ|≤0.08, strongest +0.163) and sign-agreement
(54.6%, at chance) contrasted with the α reproducibility scatter (ρ=0.88). Source:
`figures/fig01_p2_concordance.png`.

**Figure 2.** Velocity-output reliability map and routing rule. Each velocity output (rows) scored on
the four reliability-map columns (cross-method reproducible / chromatin-causal / baseline-predictable /
measurement-corroborated), the visual form of the paper's Table 2 decision map, with the
trust-versus-validate routing rule. Source:
`figures/fig07_reliability_map.png`.

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
