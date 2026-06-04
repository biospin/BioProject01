# Insight

Generated from: `papers.jsonl`, `comparison_table.md`, `evidence_bundle.md`
Skill: `Skills/insight-agent.md`

---

## Field Flow

The field moved through three distinct phases, each expanding what "timing" means in chromatin-RNA dynamics.

**Phase 1 — Ordering (which modality changes first?).**
MultiVelo established that chromatin accessibility and transcription do not change simultaneously. Its priming interval and decoupling interval were the first operationalized timing concepts in joint chromatin-RNA velocity: priming interval = time from chromatin opening to transcription onset; decoupling interval = time from transcription repression to chromatin closing. Both were defined in latent-time units and summarized at the gene level by Model 1 (chromatin leads) or Model 2 (transcription leads). The framework answered the ordering question but not the magnitude question.

**Phase 2 — Continuous cell-specific dynamics (how much does timing vary?).**
MultiVeloVAE replaced MultiVelo's discrete per-gene regime labels with continuous, cell-specific coupling ($k_c$) and decoupling ($\delta/\kappa$) factors inferred through a variational posterior. This moved the field from "is gene G in Model 1 or Model 2?" toward "how strongly decoupled is gene G in cell C at pseudotime T?" The decoupling factor is the closest existing variable to a cell-resolved lag estimate, but it is derived from model parameters rather than directly measured from timing data.

**Phase 3 — Direct lag scoring (what is the signed lag magnitude?).**
MoFlow removed the latent-time dependency entirely. Its relay velocity model computes a signed chromatin-to-spliced RNA lag per gene per cell without requiring a global trajectory ordering. Positive lag = chromatin leads transcription; negative lag = transcription precedes chromatin closing. This is the most direct published analog to the activation lag and shutdown lag concepts in this project.

Cross-paper statement: MultiVelo defined the ordering, MultiVeloVAE made it continuous, MoFlow made it signed and latent-time-free — three successive expansions of the same core question.

Evidence anchor: MultiVelo §Methods (priming interval, decoupling interval definitions); MoFlow §Results (positive/negative lag interpretation; relay velocity formulation without fixed latent time).

Project implication: Step 1 of this project (define and quantify gene-specific lag) has direct conceptual predecessors in all three papers, but none delivers an explicit, uncertainty-quantified activation lag or shutdown lag variable ready for downstream use without adaptation.

---

## Differentiation Map

| Paper | What it does uniquely well | Where it falls short for this project |
|---|---|---|
| MultiVelo | Interpretable ODE frame; established priming/decoupling as field vocabulary; four large multiome datasets | Discrete M1/M2 labels suppress continuous lag structure; latent time only; no CI on timing estimates |
| MultiVeloVAE | Posterior-based uncertainty; multi-sample differential dynamics; continuous cell-specific decoupling factor | Indirect path to lag: factor must be post-processed; heavier preprocessing; still pseudotime-anchored |
| MoFlow | Signed lag per gene per cell; relay velocity bypasses latent-time assumptions; closest direct analog | Gene-wise only; no multi-sample design; missing long-range regulatory context; no perturbation test |

**Dataset overlap with conflicting emphasis.**
MultiVelo and MoFlow both analyze SHARE-seq mouse skin and E18 mouse brain. MultiVelo uses these datasets to validate improved trajectory consistency over RNA-only velocity. MoFlow uses the same datasets to show that relay velocity outperforms fixed latent-time approaches on directional consistency metrics (CBDir). Authors' claim in MultiVelo: latent time is the appropriate axis for chromatin-RNA joint dynamics. Authors' claim in MoFlow: fixed latent time is a source of systematic error that relay velocity avoids. Inference: the two papers draw methodologically opposite conclusions from shared data, indicating that the appropriate temporal axis for lag estimation is still an open question.

**Step 1/2/3 differentiation.**
- For Step 1 (quantify lag): MoFlow is the strongest starting point; MultiVelo provides the conceptual vocabulary.
- For Step 2 (predict lag from baseline features): None of the three directly attempts this; MultiVeloVAE's continuous posterior is suggestive of feature-driven lag prediction but does not model epigenomic baseline as input.
- For Step 3 (validate against drug/perturbation response timing): All three are weak. MultiVeloVAE provides in-silico perturbation but no wall-clock validation; MultiVelo and MoFlow do not address it.

Evidence anchor: comparison_table.md Step 1/2/3 relevance columns; MoFlow §Introduction (relay velocity rationale); MultiVeloVAE §Methods (decoupling factor definition).

Project implication: no single paper delivers a complete Step 1 solution; a hybrid approach — MoFlow lag scores as primary, MultiVeloVAE uncertainty as secondary — is the most defensible starting point for this project.

---

## Repeated Limitations

Four limitations appear independently in all three papers. Their recurrence indicates structural constraints of the current field, not individual paper shortcomings.

**1. Pseudotime units, not wall-clock time.**
All three methods output timing estimates anchored to pseudotime or latent time. MultiVelo states this explicitly (§Limitations: timing remains in arbitrary latent time). MultiVeloVAE inherits this through the shared VAE latent axis. MoFlow's relay velocity removes the latent-time axis but the resulting lag scores are still ordinal within a trajectory, not calibrated to hours or days. Inference: any claim that short-lag genes respond faster to a drug in real time requires a calibration step that none of the three papers provides.

**2. No uncertainty interval on lag-like estimates.**
MultiVelo produces point-estimate switch times with no confidence interval. MultiVeloVAE provides a posterior but does not propagate uncertainty through to a per-gene lag summary. MoFlow reports lag signs and magnitudes but without bootstrap or posterior variance. A gene classified as "short lag" could be noise-driven; there is currently no operational way to filter lag estimates by reliability without additional analysis.

**3. Gene-level chromatin aggregation.**
All three aggregate chromatin peaks to the gene level (peak-to-gene linkage or gene-body ATAC). This discards enhancer-specific timing that may differ from promoter-proximal timing. MultiVelo §Limitations and MoFlow §Limitations both name this explicitly. Inference: a gene's aggregate lag may be an average of a fast promoter and a slow distal enhancer, masking the regulatory structure most relevant to drug targeting.

**4. No perturbation or drug response validation.**
None of the three papers connects estimated lag to measured perturbation response timing. MultiVeloVAE's in-silico KO simulations are model-internal tests, not real perturbation experiments. This is a structural absence: the tools to estimate lag exist in draft form, but no paper closes the loop from lag estimate to response-time prediction.

Evidence anchors: MultiVelo §Limitations (latent time, gene-level aggregation); MultiVeloVAE §Limitations (model assumptions, indirect perturbation); MoFlow §Limitations (gene-wise scope, missing regulatory context).

Project implication: all four limitations must be addressed or explicitly scoped out before any output of this project can support a drug response timing claim; the two most tractable are (1) pseudotime calibration via a metabolic labeling dataset and (2) uncertainty filtering via bootstrap resampling of lag estimates.

---

## Unresolved Gaps

**Gap 1 — Pseudotime-to-wall-clock calibration.**
None of the three papers provides a calibration from pseudotime or relay-velocity lag to wall-clock hours or days. This is necessary for Step 3. Without it, "gene A has a shorter lag than gene B" is a rank order statement, not a prediction of response timing. Possible resolution: a time-resolved multiome dataset (e.g., time-stamped multiome with matched bulk RNA-seq at known hours post-perturbation) could provide an empirical conversion factor. No such dataset is used in any of the three papers for this purpose.

**Gap 2 — Baseline epigenomic features → lag prediction (Step 2).**
No paper attempts to predict a gene's lag from static epigenomic features (promoter accessibility, H3K27ac, TF motif score, peak-to-gene linkage). MultiVeloVAE's decoupling factor is inferred from dynamic multiome data, not from baseline. This means Step 2 of this project has no direct precedent in the literature — it is a genuinely novel modeling task. The closest adjacent evidence is the observation in MultiVelo that Model 1 vs Model 2 classification correlates with gene regulatory architecture, but this is not formalized as a predictive model.

**Gap 3 — Enhancer-level lag resolution.**
All three papers operate at gene-level chromatin aggregation. Whether the dominant lag signal comes from the promoter, a proximal enhancer, or a distal regulatory element is unknown. For drug targeting purposes (Step 3), knowing which regulatory element drives the lag matters because different drug classes target different chromatin features (e.g., HDAC inhibitors act on acetylation broadly, while BET inhibitors target enhancer-bound BRD4). This gap cannot be filled without peak-level dynamic modeling.

**Gap 4 — Multi-sample robustness of lag estimates.**
MultiVelo and MoFlow are designed for single-sample inference. MultiVeloVAE adds multi-sample capability, but differential lag across donors or conditions has not been tested in a controlled perturbation context. Whether lag estimates are stable across technical replicates or biological conditions is unknown.

**Gap 5 — Step 3 validation framework.**
No paper proposes, let alone executes, a test of the form: "genes predicted to have short activation lag by method X respond to epigenetic drug Y within T hours, while long-lag genes respond after T+Δ hours." This is the direct test of the project hypothesis. The closest adjacent design in the broader literature (e.g., DeepKINET's metabolic labeling benchmark) targets splicing/degradation rates, not chromatin-RNA lag, and uses labeling data not available for chromatin dynamics.

Evidence anchors: MultiVelo §Limitations (response-time validation absent); MoFlow §Limitations (perturbation-level coordination missing); evidence_bundle.md `What it still does not solve` entries for all three papers.

Project implication: Gaps 1 and 3 are the highest-priority structural blockers for this project; Gap 2 defines the core novelty; Gaps 4 and 5 define the validation design that would make a completed project publishable.
