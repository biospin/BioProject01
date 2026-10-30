# Speaker notes

Explanation
Good morning. I am Ka-Kyung Kim. This is joint work with Jaemyun Lyu, Geongyu Lee, Sejin Park and Yong Gi Ji, carried out in Pseudo Lab, an open research community in Seoul. The talk is about a simple question: which numbers that RNA velocity methods give us per gene can we actually trust?

Transition
Let me start with why that question matters.

Objective
Introduce the talk and the speaker.

Visual cue
Title and author line.

Source and caveats
Talk based on the BIOINFO/GIW ISCB-Asia 2026 long abstract, submission 241.

Type: main
Estimated seconds: 25

---

Explanation
Multiome velocity methods read spliced and unspliced RNA together with chromatin accessibility from the same cell, and fit a kinetic model for every gene. Out of that fit come several per-gene quantities: a transcription rate alpha, a degradation rate gamma, a chromatin opening rate alpha c, and a chromatin-to-transcription lag that is often read as a clock for regulatory timing. Each of these is offered as a biological readout. Our own starting point was practical: we wanted to use the lag as a feature, to ask whether genes that are primed early respond earlier to an epigenetic drug. Before doing that, we had to know whether the lag is reliable. Recent benchmarks score velocity at the level of the embedding and the transition vectors. They do not sort the per-gene outputs by reliability, and they do not anchor them to an external measurement.

Transition
So what does reliable mean, and how can it be tested?

Objective
Motivate the reliability question.

Visual cue
Point to the four outputs, then to the question line.

Source and caveats
Background of the long abstract; recent benchmarks: Luo 2026, Huang 2026, Wu 2026.

Type: main
Estimated seconds: 65

---

Explanation
We call a per-gene output reliable if it passes four tests. First, cross-method reproducibility: two reasonable methods run on the same cells should rank the genes the same way. We test this with rank correlation and a gene-label permutation test. Second, a within-lineage ATAC shuffle: we permute chromatin profiles across cells inside each lineage, which destroys the pairing between a cell's chromatin and its own RNA, and refit. Third, replication in five external multiome datasets, from same-tissue bone marrow to mouse gastrulation; the last one was tested against predictions sealed before fitting. Fourth, external anchoring: we compare the fitted alpha with measured synthesis rates and the fitted gamma with measured mRNA half-lives, always against transcript abundance as a competing baseline. The primary data are human hematopoietic stem and progenitor cells, about twenty-two thousand cells, run through five velocity arms after one common preprocessing.

Transition
One detail turned out to matter a lot: what each method calls the lag.

Objective
Explain the protocol before any result.

Visual cue
Walk left to right across the four columns, then point at the data strip.

Source and caveats
Methods of the long abstract. GSE209878, day 0 and day 7 integrated, 21,878 cells.

Type: main
Estimated seconds: 70

---

Explanation
The word lag hides different quantities. In MultiVelo, the gap between chromatin opening and the start of transcription is the priming interval, t switch one. The duration from t switch one to t switch two is something else: the time the gene spends with chromatin open and transcription on. We report the priming interval as the main definition and the coupled-on duration as a sensitivity analysis. MultiVeloVAE does not fit switch times; the closest quantity is a rate proxy, one over alpha c minus one over alpha. MoFlow and CRAK-Velo give offsets through dynamic time warping. Because no two of these are the same object, we compared every definition we could compute, and we also applied one identical formula to both MultiVelo and MultiVeloVAE.

Transition
Here is what happens when we compare them on the same genes.

Objective
Make the comparison fair before showing it.

Visual cue
Read down the method column; stress the MultiVelo row.

Source and caveats
Li 2023 (MultiVelo), Li 2025 (MultiVeloVAE), Hong 2025 (MoFlow), El Kazwini 2026 (CRAK-Velo).

Type: main
Estimated seconds: 60

---

Explanation
On the left, alpha from MultiVelo against alpha from MultiVeloVAE on 538 shared genes. The Spearman correlation is 0.882, and the RNA-only scVelo floor agrees with both at 0.82 to 0.89. On the right, every row is one output, with its 95 percent interval. Alpha c, the chromatin opening rate, reaches only 0.29. For the lag, the best case is MultiVelo's priming interval against the MultiVeloVAE rate proxy, at 0.364. The coupled-on duration gives 0.163. Using one identical formula in both methods does not help: 0.124 signed, essentially zero in magnitude. Against MoFlow, the priming interval gives 0.038, with an interval that includes zero. The column on the far right is the difference from alpha on the same bootstrap draw. Every contrast excludes zero; the smallest is 0.518.

Transition
A natural objection is that genes are not independent, or that this is a formula artifact.

Objective
Deliver the main result with its uncertainty.

Visual cue
Left panel first, then the alpha row at the top of the right panel, then the lag rows.

Source and caveats
Long abstract Figure 1; harmonized sensitivity analyses on 538 genes, B=10,000.

Type: main
Estimated seconds: 85

---

Explanation
Genes in the same co-expression module are not independent draws, so we also resampled whole modules instead of single genes. With ten to one hundred modules, the alpha-minus-lag difference stays at 0.72 and its lower bound never falls below 0.58. Second, direction. If chromatin systematically opened before transcription, methods should at least agree on the sign of the lag. They agree for 54.6 percent of 560 genes, and the fraction of genes where chromatin leads sits between 41 and 49 percent depending on the method. So a genome-wide statement that chromatin primes transcription is not supported by these outputs. Third, within-method noise. Refitting MultiVelo on twelve overlapping 70 percent subsamples gives a moderately stable coupled-on duration, 0.624, against 0.949 for alpha. So the failure is reproducibility across methods and definitions, not necessarily within-method noise, at least for the coupled-on duration; the priming interval was not refit-tested.

Transition
What happens when we break the pairing between each cell's chromatin and its RNA?

Objective
Show the contrast is not an artifact.

Visual cue
One row at a time, top to bottom.

Source and caveats
Co-expression module bootstrap (coupled-on duration); long abstract Results.

Type: main
Estimated seconds: 65

---

Explanation
Here we permuted ATAC profiles across cells within each lineage and refitted MultiVelo. The distribution of the priming interval does not change: Mann-Whitney p 0.65, Kolmogorov-Smirnov p 0.46. On the right, each dot is a gene, observed against shuffled. The per-gene ranking is preserved, with a Spearman correlation of 0.753; the coupled-on duration behaves the same way at 0.72. The chromatin likelihood itself barely moves, 0.239 to 0.237. So the fitted lag depends little on which cell's chromatin is paired with which cell's RNA. I want to be careful about what this does not show. The shuffle keeps the chromatin distribution of each lineage, so it does not show that chromatin contributes nothing. At the level of the cell-by-gene velocity matrix, which is a separate target, we do see a small, bounded chromatin contribution.

Transition
Is any of this specific to hematopoiesis?

Objective
Show the cell-level pairing control and what it does not prove.

Visual cue
Left panel: overlap of the two histograms. Right panel: points along the diagonal.

Source and caveats
Priming-interval recomputation (single shuffle realization, 538 genes); ATAC shuffle in the findings ledger.

Type: main
Estimated seconds: 70

---

Explanation
We repeated the analysis in five external multiomes, ordered roughly by distance from bone marrow. Within each dataset, alpha agrees across methods at 0.81 to 0.93, and the lag magnitude stays between minus 0.09 and plus 0.07. On the same gene pairs, alpha minus lag is 0.843 in macrophages and 0.979 in gastrulation, with intervals well above zero. When we match genes across datasets, from HSPC to each external system, alpha still reproduces, decaying from 0.64 in HSPC-derived macrophages to 0.32 in E18 mouse brain, while the lag stays at 0.03 to 0.19. Mouse gastrulation is special: it is where lineage priming is strongest, and it is the one system we tested by preregistration. We sealed six predictions before any fit, including thresholds such as alpha agreement of at least 0.50, and all six passed. The other systems were not preregistered. Each external replication is a single sample, and the cross-dataset alpha intervals overlap, so the ordering by tissue distance is qualitative.

Transition
Reproducible is not the same as accurate. So we turned to measured rates.

Objective
Show the ordering holds outside HSPC.

Visual cue
Within-dataset columns first, then cross-dataset columns, then the gastrulation row and the callout.

Source and caveats
Manuscript Table 1; preregistration sealed 2026-07-12 (mouse gastrulation, GSE205117).

Type: main
Estimated seconds: 75

---

Explanation
Alpha is one of only two outputs with a laboratory counterpart. Fitted alpha tracks the synthesis rate measured by TT-seq in K562 cells in all three methods, between 0.24 and 0.29, with intervals that exclude zero. But a second, independent synthesis source was null. And steady-state transcript abundance, which every method sees, tracks the measured synthesis at 0.41, at least as strongly as alpha. So this is consistency evidence, not proof that alpha is the better synthesis estimator. What does survive is the reproducibility of alpha beyond abundance: after removing mean expression from both methods' alpha, their agreement is still 0.715, while the lag stays at 0.18. Alpha therefore carries a method-independent component beyond expression level. Whether that component is kinetic has not been shown; it may come from the unspliced and spliced counts that both methods read.

Transition
The degradation rate is the other output with a measured counterpart.

Objective
Say what the external match does and does not establish.

Visual cue
Compare the three alpha bars with the abundance bar, then read the right column.

Source and caveats
K562 TT-seq synthesis rates, non-housekeeping genes (GSE229305); Schwalb 2016 TT-seq. The +0.715 and +0.182 come from the abundance-controlled sensitivity analysis; the lag there is the coupled-on duration.

Type: main
Estimated seconds: 70

---

Explanation
For gamma we have measured mRNA half-lives in three cell lines. Across three methods and three lines, only one of nine cells recovers gamma, weakly. The textbook scVelo gamma, from the RNA-only floor, runs in the wrong direction in the cleanest reference, MOLM13, at minus 0.224: genes with larger fitted degradation have longer measured half-lives. Gamma is also fragile across methods, around minus 0.11.

Transition
Let me put all of this together.

Objective
Close the accuracy axis for γ.

Visual cue
Point to the MOLM13 column and the scVelo row.

Source and caveats
External rate validation, non-housekeeping genes; K562 and THP1 half-lives from Todorovski, MOLM13 from RNADecayCafe.

Type: main
Estimated seconds: 35

---

Explanation
This map keeps two kinds of evidence apart. Reproducibility asks whether two reasonable methods, run on the same cells, rank genes the same way. Accuracy asks whether the number has been compared with a laboratory measurement of the same rate, and with what result. Transcript abundance sits on top as the reference baseline. Alpha is the only per-gene output that is reproducible, including beyond abundance; its accuracy beyond abundance is not shown. Two further outputs are usable only as population statements: the near fifty-fifty directional balance, and the agreement of canonical priming markers, which is correlational. The chromatin opening rate, gamma, and the per-gene lag, its sign and its timing, under every definition we tested, are not reproducible. The last column turns this into a decision for each output.

Transition
Here is that decision as a rule.

Objective
Summarize every output on reproducibility and accuracy separately.

Visual cue
Read the column headers, then the abundance row, then the alpha row, then the red block.

Source and caveats
Long abstract Figure 2.

Type: main
Estimated seconds: 70

---

Explanation
If you want to use velocity outputs as features, enter transcript abundance first. Add alpha only as the part that is orthogonal to abundance, and keep it only if held-out performance improves. Do not consume a single-method lag, its sign, or gamma without an orthogonal measurement. The held-out data support this order. On held-out lineages, abundance alone predicts alpha at 0.72; day-0 chromatin accessibility predicts alpha at 0.31, but adding it to abundance changes the correlation by minus 0.016. The same accessibility features do not predict the lag, here the coupled-on duration, at around 0.05.

Transition
To close.

Objective
Make the map usable.

Visual cue
Three steps on the left, numbers on the right.

Source and caveats
Held-out lineage prediction of alpha with abundance control; held-out prediction of the lag.

Type: main
Estimated seconds: 45

---

Explanation
Three points. Reliability of a velocity output is testable, on four axes. Among the per-gene outputs, only alpha passes reproducibility, and its accuracy beyond abundance is still open. The lag does not reproduce under any definition we tested, so treat it as a model output that needs orthogonal validation, not as a regulatory clock. The limits are on the slide: pseudotime is not wall-clock time, the external replications are single samples, the alpha anchor is one of two sources and was measured in K562, and we audited per-gene parameters, not trajectories. Thank you. I am happy to take questions.

Transition
Questions.

Objective
Close with the contribution and its limits.

Visual cue
Three take-home lines, then the limits.

Source and caveats
Conclusion of the long abstract.

Type: main
Estimated seconds: 45

---

Explanation
In log coordinates on MultiVelo's objective, alpha is located more tightly than the lag: median curvature ratio 3.53, alpha tighter in 95 percent of 258 interior-lag genes. Expressing the lag as a fraction of the pseudotime horizon reverses the ratio to 0.10. So we claim cross-method non-reproducibility, not strict non-identifiability. Most boundary-pinned lags, 199 of 205, come from induction-only fits.

Transition
Back to questions.

Objective
Answer: is the lag simply non-identifiable?

Visual cue
Table first.

Source and caveats
Profile-likelihood sensitivity analysis (fixed nuisance parameters, 258 genes). Lag here is the coupled-on duration.

Type: backup
Estimated seconds: 0

---

Explanation
On the 537 genes shared by MultiVelo, MultiVeloVAE and MoFlow, lag magnitude agreement is 0.165, minus 0.013 and minus 0.064 for the three pairs, while alpha agrees at 0.882. The signed VAE against MoFlow comparison reaches 0.107.

Transition
Back to questions.

Objective
Answer: maybe another method pair agrees.

Visual cue
Lag rows against the alpha row.

Source and caveats
Three-method sensitivity analysis, B=10,000. MultiVelo lag here is the coupled-on duration.

Type: backup
Estimated seconds: 0

---

Explanation
Fetal cortex is missing here because it has no MultiVeloVAE fit. Top row: alpha rank against alpha rank in each system. Bottom row: lag magnitude. The lag here is MultiVelo's coupled-on duration against the MultiVeloVAE rate proxy; the priming-interval definition was recomputed in HSPC only.

Transition
Back to questions.

Objective
Answer: show the external scatter.

Visual cue
Top row versus bottom row.

Source and caveats
Supplementary figure, per-dataset concordance.

Type: backup
Estimated seconds: 0

---

Explanation
The six predictions and thresholds were sealed on July 12, 2026, before any velocity fit on this dataset. The pairing used to score prediction five, MultiVelo against MoFlow for the lag, was fixed on July 13, still before any fit. The thresholds, not the HSPC observations, are the pass lines: for example alpha agreement of at least 0.50, while 0.88 in HSPC was only an observation.

Transition
Back to questions.

Objective
Answer: what exactly was preregistered?

Visual cue
Threshold column against the observed column.

Source and caveats
Preregistration sealed 2026-07-12; scorecard for GSE205117.

Type: backup
Estimated seconds: 0
