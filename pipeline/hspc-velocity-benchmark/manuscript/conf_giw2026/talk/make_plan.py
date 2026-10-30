"""Single source for the GIW 2026 talk plan.

Writes brief.json, evidence-map.json, slide-plan.json and outline.md. build_deck.py reads
slide-plan.json, so titles, timings and notes live only here.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parents[2]            # pipeline/hspc-velocity-benchmark
REL = "../../../"                  # evidence-map.json -> hspc-velocity-benchmark/


def sha(rel):
    return hashlib.sha256((HERE / rel).read_bytes()).hexdigest()[:16]


SOURCES = [
    ("SRC01", "manuscript/CONF_LONGABSTRACT_GIW2026_BIOP01.md", "GIW 2026 long abstract v2 (kkkim-pipeline b319c23)"),
    ("SRC02", "results/post_review_robustness.gen.md", "machine output of scripts/p17_post_review_robustness.py"),
    ("SRC03", "results/priming_recompute.gen.md", "machine output of scripts/p18_priming_recompute.py"),
    ("SRC04", "manuscript/draft_v2.md", "full manuscript draft v2, Table 1 and external-validation section"),
    ("SRC05", "results/external_rate_validation.md", "TT-seq / half-life anchoring"),
    ("SRC06", "results/prereg_gse205117_scorecard.md", "preregistered scorecard, mouse gastrulation"),
    ("SRC07", "results/atac_alpha_expression_confound.md", "held-out lineage prediction of α, abundance control"),
    ("SRC08", "results/lag_model_atac.md", "held-out lineage prediction of the lag"),
    ("SRC09", "results/FINDINGS.md", "findings ledger"),
    ("SRC10", "manuscript/PREREGISTRATION_gse205117.md", "sealed preregistration 2026-07-12"),
]

CLAIMS = [
    ("C01", "Cross-method α agreement MultiVelo vs MultiVeloVAE", "SRC02", "Contract table, rho_alpha", "+0.882 [+0.856, +0.904]", "538 genes", "gene bootstrap 95% CI, B=10,000"),
    ("C02", "Lag agreement, MultiVelo priming interval vs MultiVeloVAE rate proxy", "SRC02", "R5_MVxVAE_priming", "+0.364 [+0.285, +0.440]", "538 genes", "95% CI"),
    ("C03", "Lag agreement, MultiVelo coupled-on duration vs MultiVeloVAE", "SRC02", "R5_MVxVAE_coupled_on", "+0.163 [+0.078, +0.244]", "538 genes", "95% CI"),
    ("C04", "Identical formula in both methods: signed +0.124, magnitude −0.009", "SRC02", "R1_lag_rateproxy_signed / _mag", "+0.124; −0.009", "538 genes", "95% CI"),
    ("C05", "Lag vs MoFlow (priming) does not reproduce", "SRC02", "R5_MVxMoFlow_priming", "+0.038 [−0.046, +0.122]", "537 genes", "95% CI"),
    ("C06", "Smallest α-minus-lag contrast excludes zero", "SRC02", "R5_MVxVAE_priming delta", "+0.518 [+0.441, +0.596]", "538 genes", "paired bootstrap"),
    ("C07", "Module bootstrap keeps Δρ above zero (coupled-on)", "SRC02", "R3 modules K10–K100", "+0.720; lowest lower bound +0.582", "538 genes", "co-expression module resampling"),
    ("C08", "Direction near balance: sign agreement 54.6% (n=560), chromatin-leads 41–49%", "SRC01", "Results paragraph 1", "54.6%; 41–49%", "560 genes", None),
    ("C09", "Within-MultiVelo refit stability of coupled-on duration +0.624, α +0.949; priming not refit-tested", "SRC01", "Results paragraph 1", "+0.624; +0.949", "12 overlapping 70% subsamples", None),
    ("C10", "ATAC shuffle leaves priming interval unchanged", "SRC03", "S table, priming row", "ρ +0.753 [+0.695, +0.806]; MW p 0.651; KS p 0.460", "538 genes", "single shuffle realization"),
    ("C11", "ATAC shuffle, coupled-on ρ 0.72; chromatin likelihood 0.239 to 0.237", "SRC09", "ATAC shuffle entry", "0.72; 0.239→0.237", "538 genes", None),
    ("C12", "Within- and cross-dataset α and lag in five external multiomes", "SRC04", "Table 1", "see table", "per dataset", "95% CI"),
    ("C13", "Preregistered gastrulation scorecard 6/6", "SRC06", "verdict table", "6 PASS / 0 FAIL", "969 genes within; 111 cross", None),
    ("C14", "α vs K562 TT-seq synthesis (non-housekeeping)", "SRC05", "Part B table", "+0.236, +0.262, +0.285", "193 / 235 / 251 genes", "95% CI"),
    ("C15", "Abundance tracks synthesis at least as strongly", "SRC04", "external validation paragraph", "+0.410 vs +0.262", None, "point estimates"),
    ("C16", "Second synthesis source (Schwalb 2016) null", "SRC05", "limitation 2", "ρ −0.05 to −0.01", None, None),
    ("C17", "Partial cross-method α given abundance", "SRC02", "R2_alpha partial", "+0.715 [+0.659, +0.765]", "538 genes", "95% CI"),
    ("C18", "γ vs measured degradation, 3 methods × 3 cell lines", "SRC05", "Part A non-HK table", "scVelo MOLM13 −0.224 [−0.359, −0.085]", "MOLM13 n=188", "95% CI"),
    ("C19", "Cross-method γ fragile", "SRC01", "Results paragraph 1", "ρ≈−0.11", None, None),
    ("C20", "Profile-likelihood curvature ratio depends on coordinates", "SRC02", "R4", "3.53 (log) vs 0.10 (fraction of horizon)", "258 genes", "median, IQR"),
    ("C21", "Held-out lineage prediction of α: abundance +0.724, ATAC +0.309, ATAC increment −0.016", "SRC07", "held-out table", "+0.724; +0.309; −0.016", "6 held-out lineages", None),
    ("C22", "Held-out lineage prediction of the lag by ATAC ≈ chance", "SRC08", "key finding 2", "+0.049", None, None),
]

FIG = REL + "figures/"
ASSETS = [
    ("A01", "SRC01", "Figure 1 of the long abstract", FIG + "fig01_concordance_v2.png", "reproduced"),
    ("A02", "SRC03", "S block, priming row (replot of the same data)", FIG + "figT01_atac_shuffle_priming.png", "redrawn from results/multivelo_genes.csv and scrambled_genes.csv"),
    ("A03", "SRC01", "Figure 2 of the long abstract", FIG + "fig07_reliability_map_v2.png", "reproduced"),
    ("A05", "SRC04", "Additional file 11 panel 1", "assets/figS01_per_dataset_concordance_crop.png",
     "cropped: top 150 px (figure-level caption) removed from figures/figS01_per_dataset_concordance.png; panels intact"),
]

E = "en"

SLIDES = [
    dict(id="S00", title="A reliability map for per-gene multiome RNA velocity parameters in single-cell kinetics",
         purpose="Open the talk.", claims=[], loc=["SRC01: title"], layout="cover", assets=[], sec=20, caveat=None,
         objective="Introduce the talk and the speaker.",
         explanation="Good morning. I am Ka-Kyung Kim. This is joint work with Jaemyun Lyu, Geongyu Lee, Sejin Park and Yong Gi Ji, carried out in Pseudo Lab, an open research community in Seoul. The talk is about a simple question: which numbers that RNA velocity methods give us per gene can we actually trust?",
         cue="Title and author line.",
         transition="Let me start with why that question matters.",
         source="Talk based on the BIOINFO/GIW ISCB-Asia 2026 long abstract, submission 241."),
    dict(id="S01", title="Velocity methods emit per-gene numbers that we read as biology",
         purpose="Pose the question: which per-gene outputs are reliable enough to use as features?",
         claims=[], loc=["SRC01: Background and motivation"], layout="concept: data → model → four outputs → question", assets=[], sec=55, caveat=None,
         objective="Motivate the reliability question.",
         explanation="Multiome velocity methods read spliced and unspliced RNA together with chromatin accessibility from the same cell, and fit a kinetic model for every gene. Out of that fit come several per-gene quantities: a transcription rate alpha, a degradation rate gamma, a chromatin opening rate alpha c, and a chromatin-to-transcription lag that is often read as a clock for regulatory timing. Each of these is offered as a biological readout. Our own starting point was practical: we wanted to use the lag as a feature, to ask whether genes that are primed early respond earlier to an epigenetic drug. Before doing that, we had to know whether the lag is reliable. Recent benchmarks score velocity at the level of the embedding and the transition vectors. They do not sort the per-gene outputs by reliability, and they do not anchor them to an external measurement.",
         cue="Point to the four outputs, then to the question line.",
         transition="So what does reliable mean, and how can it be tested?",
         source="Background of the long abstract; recent benchmarks: Luo 2026, Huang 2026, Wu 2026."),
    dict(id="S02", title="Reliability can be tested on four independent axes",
         purpose="Present the four-axis protocol and the data.",
         claims=[], loc=["SRC01: Methods"], layout="four columns + data strip", assets=[], sec=70, caveat=None,
         objective="Explain the protocol before any result.",
         explanation="We call a per-gene output reliable if it passes four tests. First, cross-method reproducibility: two reasonable methods run on the same cells should rank the genes the same way. We test this with rank correlation and a gene-label permutation test. Second, a within-lineage ATAC shuffle: we permute chromatin profiles across cells inside each lineage, which destroys the pairing between a cell's chromatin and its own RNA, and refit. Third, replication in five external multiome datasets, from same-tissue bone marrow to mouse gastrulation; the last one was tested against predictions sealed before fitting. Fourth, external anchoring: we compare the fitted alpha with measured synthesis rates and the fitted gamma with measured mRNA half-lives, always against transcript abundance as a competing baseline. The primary data are human hematopoietic stem and progenitor cells, about twenty-two thousand cells, run through five velocity arms after one common preprocessing.",
         cue="Walk left to right across the four columns, then point at the data strip.",
         transition="One detail turned out to matter a lot: what each method calls the lag.",
         source="Methods of the long abstract. GSE209878, day 0 and day 7 integrated, 21,878 cells."),
    dict(id="S03", title="The methods do not estimate the same lag",
         purpose="Define every lag that is compared.",
         claims=["C02", "C03"], loc=["SRC01: Methods", "SRC02: R5"], layout="definition table", assets=[], sec=55,
         caveat="MultiVelo's priming interval is the primary definition; the coupled-on duration is a sensitivity analysis.",
         objective="Make the comparison fair before showing it.",
         explanation="The word lag hides different quantities. In MultiVelo, the gap between chromatin opening and the start of transcription is the priming interval, t switch one. The duration from t switch one to t switch two is something else: the time the gene spends with chromatin open and transcription on. We report the priming interval as the main definition and the coupled-on duration as a sensitivity analysis. MultiVeloVAE does not fit switch times; the closest quantity is a rate proxy, one over alpha c minus one over alpha. MoFlow and CRAK-Velo give offsets through dynamic time warping. Because no two of these are the same object, we compared every definition we could compute, and we also applied one identical formula to both MultiVelo and MultiVeloVAE.",
         cue="Read down the method column; stress the MultiVelo row.",
         transition="Here is what happens when we compare them on the same genes.",
         source="Li 2023 (MultiVelo), Li 2025 (MultiVeloVAE), Hong 2025 (MoFlow), El Kazwini 2026 (CRAK-Velo)."),
    dict(id="S04", title="α reproduces across methods; the lag does not, under any definition",
         purpose="Show the central contrast.",
         claims=["C01", "C02", "C03", "C04", "C05", "C06"], loc=["SRC01: Figure 1", "SRC02: R1, R5"], layout="one dominant figure", assets=["A01"], sec=90,
         caveat="All values are rank correlations on 538 shared genes with gene-bootstrap 95% CIs.",
         objective="Deliver the main result with its uncertainty.",
         explanation="On the left, alpha from MultiVelo against alpha from MultiVeloVAE on 538 shared genes. The Spearman correlation is 0.882, and the RNA-only scVelo floor agrees with both at 0.82 to 0.89. On the right, every row is one output, with its 95 percent interval. Alpha c, the chromatin opening rate, reaches only 0.29. For the lag, the best case is MultiVelo's priming interval against the MultiVeloVAE rate proxy, at 0.364. The coupled-on duration gives 0.163. Using one identical formula in both methods does not help: 0.124 signed, essentially zero in magnitude. Against MoFlow, the priming interval gives 0.038, with an interval that includes zero. The column on the far right is the difference from alpha on the same bootstrap draw. Every contrast excludes zero; the smallest is 0.518.",
         cue="Left panel first, then the alpha row at the top of the right panel, then the lag rows.",
         transition="A natural objection is that genes are not independent, or that this is a formula artifact.",
         source="Long abstract Figure 1; harmonized sensitivity analyses on 538 genes, B=10,000."),
    dict(id="S05", title="The gap survives gene dependence, and the direction stays near 50/50",
         purpose="Pre-empt the dependence and direction objections.",
         claims=["C07", "C08", "C09"], loc=["SRC02: R3", "SRC01: Results"], layout="three result rows", assets=[], sec=55,
         caveat="The module bootstrap and the refit test used the coupled-on duration; the priming interval was not refit-tested.",
         objective="Show the contrast is not an artifact.",
         explanation="Genes in the same co-expression module are not independent draws, so we also resampled whole modules instead of single genes. With ten to one hundred modules, the alpha-minus-lag difference stays at 0.72 and its lower bound never falls below 0.58. Second, direction. If chromatin systematically opened before transcription, methods should at least agree on the sign of the lag. They agree for 54.6 percent of 560 genes, and the fraction of genes where chromatin leads sits between 41 and 49 percent depending on the method. So a genome-wide statement that chromatin primes transcription is not supported by these outputs. Third, within-method noise. Refitting MultiVelo on twelve overlapping 70 percent subsamples gives a moderately stable coupled-on duration, 0.624, against 0.949 for alpha. So the failure is reproducibility across methods and definitions, not necessarily within-method noise, at least for the coupled-on duration; the priming interval was not refit-tested.",
         cue="One row at a time, top to bottom.",
         transition="What happens when we break the pairing between each cell's chromatin and its RNA?",
         source="Co-expression module bootstrap (coupled-on duration); long abstract Results."),
    dict(id="S06", title="The fitted lag barely depends on pairing each cell's chromatin with its own RNA",
         purpose="Present the within-lineage ATAC shuffle and its limits.",
         claims=["C10", "C11"], loc=["SRC03: S table", "SRC09: ATAC shuffle"], layout="figure + caveat strip", assets=["A02"], sec=75,
         caveat="The shuffle keeps lineage-level chromatin, so it does not show that chromatin contributes nothing; one shuffle realization.",
         objective="Show the cell-level pairing control and what it does not prove.",
         explanation="Here we permuted ATAC profiles across cells within each lineage and refitted MultiVelo. The distribution of the priming interval does not change: Mann-Whitney p 0.65, Kolmogorov-Smirnov p 0.46. On the right, each dot is a gene, observed against shuffled. The per-gene ranking is preserved, with a Spearman correlation of 0.753; the coupled-on duration behaves the same way at 0.72. The chromatin likelihood itself barely moves, 0.239 to 0.237. So the fitted lag depends little on which cell's chromatin is paired with which cell's RNA. I want to be careful about what this does not show. The shuffle keeps the chromatin distribution of each lineage, so it does not show that chromatin contributes nothing. At the level of the cell-by-gene velocity matrix, which is a separate target, we do see a small, bounded chromatin contribution.",
         cue="Left panel: overlap of the two histograms. Right panel: points along the diagonal.",
         transition="Is any of this specific to hematopoiesis?",
         source="Priming-interval recomputation (single shuffle realization, 538 genes); ATAC shuffle in the findings ledger."),
    dict(id="S07", title="The α-over-lag ordering replicates in five external multiomes",
         purpose="Show replication and the single preregistered system.",
         claims=["C12", "C13"], loc=["SRC04: Table 1", "SRC06: verdict"], layout="native table + preregistration callout", assets=[], sec=80,
         caveat="One sample per system; cross-dataset α CIs overlap; only gastrulation was preregistered.",
         objective="Show the ordering holds outside HSPC.",
         explanation="We repeated the analysis in five external multiomes, ordered roughly by distance from bone marrow. Within each dataset, alpha agrees across methods at 0.81 to 0.93, and the lag magnitude stays between minus 0.09 and plus 0.07. On the same gene pairs, alpha minus lag is 0.843 in macrophages and 0.979 in gastrulation, with intervals well above zero. When we match genes across datasets, from HSPC to each external system, alpha still reproduces, decaying from 0.64 in HSPC-derived macrophages to 0.32 in E18 mouse brain, while the lag stays at 0.03 to 0.19. Mouse gastrulation is special: it is where lineage priming is strongest, and it is the one system we tested by preregistration. We sealed six predictions before any fit, including thresholds such as alpha agreement of at least 0.50, and all six passed. The other systems were not preregistered. Each external replication is a single sample, and the cross-dataset alpha intervals overlap, so the ordering by tissue distance is qualitative.",
         cue="Within-dataset columns first, then cross-dataset columns, then the gastrulation row and the callout.",
         transition="Reproducible is not the same as accurate. So we turned to measured rates.",
         source="Manuscript Table 1; preregistration sealed 2026-07-12 (mouse gastrulation, GSE205117)."),
    dict(id="S08", title="α tracks measured synthesis, but transcript abundance tracks it at least as strongly",
         purpose="Show external anchoring of α with the abundance baseline beside it.",
         claims=["C14", "C15", "C16", "C17"], loc=["SRC05: Part B", "SRC04: external validation", "SRC02: R2"], layout="native bar chart + right column", assets=[], sec=70,
         caveat="Abundance is shown as a point estimate; the second synthesis source was null.",
         objective="Say what the external match does and does not establish.",
         explanation="Alpha is one of only two outputs with a laboratory counterpart. Fitted alpha tracks the synthesis rate measured by TT-seq in K562 cells in all three methods, between 0.24 and 0.29, with intervals that exclude zero. But a second, independent synthesis source was null. And steady-state transcript abundance, which every method sees, tracks the measured synthesis at 0.41, at least as strongly as alpha. So this is consistency evidence, not proof that alpha is the better synthesis estimator. What does survive is the reproducibility of alpha beyond abundance: after removing mean expression from both methods' alpha, their agreement is still 0.715, while the lag stays at 0.18. Alpha therefore carries a method-independent component beyond expression level. Whether that component is kinetic has not been shown; it may come from the unspliced and spliced counts that both methods read.",
         cue="Compare the three alpha bars with the abundance bar, then read the right column.",
         transition="The degradation rate is the other output with a measured counterpart.",
         source="K562 TT-seq synthesis rates, non-housekeeping genes (GSE229305); Schwalb 2016 TT-seq. The +0.715 and +0.182 come from the abundance-controlled sensitivity analysis; the lag there is the coupled-on duration."),
    dict(id="S09", title="γ does not recover measured half-life, even where one exists",
         purpose="Show the γ failure on the external axis.",
         claims=["C18", "C19"], loc=["SRC05: Part A"], layout="native 3 × 3 table", assets=[], sec=40,
         caveat="The reversal belongs to the RNA-only scVelo γ, not to MultiVelo.",
         objective="Close the accuracy axis for γ.",
         explanation="For gamma we have measured mRNA half-lives in three cell lines. Across three methods and three lines, only one of nine cells recovers gamma, weakly. The textbook scVelo gamma, from the RNA-only floor, runs in the wrong direction in the cleanest reference, MOLM13, at minus 0.224: genes with larger fitted degradation have longer measured half-lives. Gamma is also fragile across methods, around minus 0.11.",
         cue="Point to the MOLM13 column and the scVelo row.",
         transition="Let me put all of this together.",
         source="External rate validation, non-housekeeping genes; K562 and THP1 half-lives from Todorovski, MOLM13 from RNADecayCafe."),
    dict(id="S10", title="A reliability map routes each velocity output",
         purpose="Deliver the reliability map.",
         claims=["C01", "C08", "C14", "C17", "C18", "C19"], loc=["SRC01: Figure 2"], layout="one dominant figure", assets=["A03"], sec=85, caveat=None,
         objective="Summarize every output on reproducibility and accuracy separately.",
         explanation="This map keeps two kinds of evidence apart. Reproducibility asks whether two reasonable methods, run on the same cells, rank genes the same way. Accuracy asks whether the number has been compared with a laboratory measurement of the same rate, and with what result. Transcript abundance sits on top as the reference baseline. Alpha is the only per-gene output that is reproducible, including beyond abundance; its accuracy beyond abundance is not shown. Two further outputs are usable only as population statements: the near fifty-fifty directional balance, and the agreement of canonical priming markers, which is correlational. The chromatin opening rate, gamma, and the per-gene lag, its sign and its timing, under every definition we tested, are not reproducible. The last column turns this into a decision for each output.",
         cue="Read the column headers, then the abundance row, then the alpha row, then the red block.",
         transition="Here is that decision as a rule.",
         source="Long abstract Figure 2."),
    dict(id="S11", title="Routing rule: abundance first, α only for what it adds",
         purpose="Give the actionable rule and its held-out support.",
         claims=["C21", "C22"], loc=["SRC07: held-out table", "SRC08"], layout="three steps + evidence column", assets=[], sec=50,
         caveat="Held-out prediction is across six lineages in HSPC.",
         objective="Make the map usable.",
         explanation="If you want to use velocity outputs as features, enter transcript abundance first. Add alpha only as the part that is orthogonal to abundance, and keep it only if held-out performance improves. Do not consume a single-method lag, its sign, or gamma without an orthogonal measurement. The held-out data support this order. On held-out lineages, abundance alone predicts alpha at 0.72; day-0 chromatin accessibility predicts alpha at 0.31, but adding it to abundance changes the correlation by minus 0.016. The same accessibility features do not predict the lag, here the coupled-on duration, at around 0.05.",
         cue="Three steps on the left, numbers on the right.",
         transition="To close.",
         source="Held-out lineage prediction of alpha with abundance control; held-out prediction of the lag."),
    dict(id="S12", title="Take-home",
         purpose="Leave the contribution, its scope, and acknowledgements on screen for Q&A.",
         claims=["C01", "C06"], loc=["SRC01: Conclusion"], layout="take-home + limits + acknowledgements", assets=[], sec=40,
         caveat="Limits shown on slide.",
         objective="Close with the contribution and its limits.",
         explanation="Three points. Reliability of a velocity output is testable, on four axes. Among the per-gene outputs, only alpha passes reproducibility, and its accuracy beyond abundance is still open. The lag does not reproduce under any definition we tested, so treat it as a model output that needs orthogonal validation, not as a regulatory clock. The limits are on the slide: pseudotime is not wall-clock time, the external replications are single samples, the alpha anchor is one of two sources and was measured in K562, and we audited per-gene parameters, not trajectories. Thank you. I am happy to take questions.",
         cue="Three take-home lines, then the limits.",
         transition="Questions.",
         source="Conclusion of the long abstract."),
    # backups
    dict(id="B01", title="Backup: profile likelihood gives relative precision, and it depends on coordinates",
         purpose="Answer identifiability questions.", claims=["C20"], loc=["SRC02: R4"], layout="table + statements", assets=[], sec=0,
         caveat="Neither coordinate system is canonical.", backup=True,
         objective="Answer: is the lag simply non-identifiable?",
         explanation="In log coordinates on MultiVelo's objective, alpha is located more tightly than the lag: median curvature ratio 3.53, alpha tighter in 95 percent of 258 interior-lag genes. Expressing the lag as a fraction of the pseudotime horizon reverses the ratio to 0.10. So we claim cross-method non-reproducibility, not strict non-identifiability. Most boundary-pinned lags, 199 of 205, come from induction-only fits.",
         cue="Table first.", transition="Back to questions.",
         source="Profile-likelihood sensitivity analysis (fixed nuisance parameters, 258 genes). Lag here is the coupled-on duration."),
    dict(id="B02", title="Backup: lag agreement on the three-method gene set",
         purpose="Show every pairwise lag agreement.", claims=["C04", "C05"], loc=["SRC02: R1c"], layout="native table", assets=[], sec=0,
         caveat=None, backup=True,
         objective="Answer: maybe another method pair agrees.",
         explanation="On the 537 genes shared by MultiVelo, MultiVeloVAE and MoFlow, lag magnitude agreement is 0.165, minus 0.013 and minus 0.064 for the three pairs, while alpha agrees at 0.882. The signed VAE against MoFlow comparison reaches 0.107.",
         cue="Lag rows against the alpha row.", transition="Back to questions.",
         source="Three-method sensitivity analysis, B=10,000. MultiVelo lag here is the coupled-on duration."),
    dict(id="B03", title="Backup: within-dataset agreement in HSPC and four external systems",
         purpose="Show the per-dataset scatter.", claims=["C12"], loc=["SRC04: Additional file 11"], layout="one figure", assets=["A05"], sec=0,
         caveat="Lag here is MultiVelo coupled-on duration against the MultiVeloVAE rate proxy, magnitude.", backup=True,
         objective="Answer: show the external scatter.",
         explanation="Fetal cortex is missing here because it has no MultiVeloVAE fit. Top row: alpha rank against alpha rank in each system. Bottom row: lag magnitude. The lag here is MultiVelo's coupled-on duration against the MultiVeloVAE rate proxy; the priming-interval definition was recomputed in HSPC only.",
         cue="Top row versus bottom row.", transition="Back to questions.",
         source="Supplementary figure, per-dataset concordance."),
    dict(id="B04", title="Backup: the six predictions sealed before fitting mouse gastrulation",
         purpose="Show the preregistered scorecard.", claims=["C13"], loc=["SRC06", "SRC10"], layout="native table", assets=[], sec=0,
         caveat="One preregistered system; replication, not discovery.", backup=True,
         objective="Answer: what exactly was preregistered?",
         explanation="The six predictions and thresholds were sealed on July 12, 2026, before any velocity fit on this dataset. The pairing used to score prediction five, MultiVelo against MoFlow for the lag, was fixed on July 13, still before any fit. The thresholds, not the HSPC observations, are the pass lines: for example alpha agreement of at least 0.50, while 0.88 in HSPC was only an observation.",
         cue="Threshold column against the observed column.", transition="Back to questions.",
         source="Preregistration sealed 2026-07-12; scorecard for GSE205117."),
]


# Per-slide seconds re-balanced against the note-length estimate (130–150 words/min) plus pointing time.
SECONDS = {"S00": 25, "S01": 65, "S02": 70, "S03": 60, "S04": 85, "S05": 65, "S06": 70, "S07": 75,
           "S08": 70, "S09": 35, "S10": 70, "S11": 45, "S12": 45}
for _s in SLIDES:
    _s["sec"] = SECONDS.get(_s["id"], _s["sec"])


def crop_assets():
    from PIL import Image
    (HERE / "assets").mkdir(exist_ok=True)
    im = Image.open(BENCH / "figures/figS01_per_dataset_concordance.png")
    im.crop((0, 150, im.width, im.height)).save(HERE / "assets/figS01_per_dataset_concordance_crop.png")


def main():
    crop_assets()
    brief = {
        "presentation_type": "academic-conference-oral",
        "talk_minutes": 15, "qa_included": False, "qa_minutes": None, "timing_buffer_fraction": 0.1,
        "audience": "genome informatics and computational biology researchers (BIOINFO/GIW ISCB-Asia 2026)",
        "slide_language": "en", "notes_language": "en",
        "preferred_color": "#2457C5", "background_mode": "light", "aspect_ratio": "16:9",
        "font_family": "Pretendard (installed; Greek and math glyphs verified)",
        "venue": "BIOINFO/GIW ISCB-Asia 2026, Yonsei University, Seoul, 17–20 November 2026; oral, submission 241",
        "mandatory_template": None,
        "required_disclosures": ["Acknowledgements and funding as in the manuscript draft"],
        "source_files": [s[1] for s in SOURCES],
        "requested_output": "pptx",
        "approval_mode": "waived",
        "assumptions": [
            "Talk length not yet assigned by the organizers on 2026-10-25; planned for 15 minutes of speaking, Q&A separate.",
            "English slides and English speaker notes because the venue is international.",
            "Default primary color #2457C5; no lab template was supplied.",
            "Presenter affiliation shown as Pseudo Lab, Seoul, as requested to the organizers on 2026-09-25.",
        ],
    }
    (HERE / "brief.json").write_text(json.dumps(brief, indent=2, ensure_ascii=False), encoding="utf-8")

    ev = {"sources": [dict(id=i, path_or_identifier=REL + p, version=f"sha256:{sha(REL + p)} ({d})", accessed=True,
                           source_type="user-data") for i, p, d in SOURCES],
          "claims": [dict(id=i, statement=s, source_id=src, locator=loc, source_quote_or_value=v, display_value=v,
                          unit="Spearman ρ" if "ρ" in s or "agreement" in s.lower() else None,
                          denominator_or_evaluation_unit=n, uncertainty_definition=u, qualifiers=[],
                          assistant_calculation=None, verification_status="verified")
                     for i, s, src, loc, v, n, u in CLAIMS],
          "assets": [dict(id=i, source_id=src, locator=loc, path=p, transformation=t, caption_checked=True,
                          scientific_context_preserved=True) for i, src, loc, p, t in ASSETS]}
    (HERE / "evidence-map.json").write_text(json.dumps(ev, indent=2, ensure_ascii=False), encoding="utf-8")

    plan = {"approval": {"status": "waived",
                         "instruction_evidence": "User, 2026-10-25: '나 외출하고 올테니 완벽하게 ppt 만들어줘' (going out; make the deck completely)",
                         "approved_revision": None},
            "revision": "outline-v1", "theme_file": "theme.json",
            "available_speaking_seconds": 900, "target_speaking_seconds": 810, "slides": []}
    for s in SLIDES:
        plan["slides"].append({
            "id": s["id"], "main_or_backup": "backup" if s.get("backup") else "main", "title": s["title"],
            "purpose": s["purpose"], "claim_ids": s["claims"],
            "evidence_locators": s["loc"], "layout": s["layout"], "visual_assets": s["assets"],
            "estimated_seconds": s["sec"], "essential_caveat": s["caveat"],
            "notes": {"language": E, "objective": s["objective"], "explanation": s["explanation"],
                      "visual_cue": s["cue"], "transition": s["transition"], "source_and_caveats": s["source"]}})
    (HERE / "slide-plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")

    main_s = [s for s in SLIDES if not s.get("backup")]
    lines = ["# BIOINFO/GIW ISCB-Asia 2026 oral talk: outline", "",
             f"Planned speaking time {sum(s['sec'] for s in main_s)} s of 900 s (target 810 s). Approval: waived by the user on 2026-10-25.", "",
             "| # | Title | Seconds | Evidence |", "|---|---|---|---|"]
    for s in SLIDES:
        lines.append(f"| {s['id']} | {s['title']} | {s['sec'] or 'backup'} | {', '.join(s['loc'])} |")
    lines += ["", "## Assumptions", ""] + [f"- {a}" for a in brief["assumptions"]]
    lines += ["", "## Design", "", "- Primary #2457C5 on white, Pretendard for all text, 16:9.",
              "- Source figures keep their own colors (green, amber, red, grey semantics of the reliability map)."]
    (HERE / "outline.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"main {len(main_s)} slides, {sum(s['sec'] for s in main_s)} s; backup {len(SLIDES) - len(main_s)}")


if __name__ == "__main__":
    main()
