# Supplementary package — Additional files (Genome Biology / BMC convention)

> Target journal is Genome Biology (BMC), which uses **"Additional file N"**, not standalone "Supplementary Table S1".
> Body citation form: `(Additional file 1: Table S1)`. The manuscript carries an **Additional files** section listing each entry.
> **Only artefacts that exist are registered here.** Items still to be produced are marked `TO BE RENDERED` and must not be cited as if they exist.
> Manifest maintained with the drafts (`draft_v2.md` / `draft_v2_ko.md`). BIOP01-56.

---

### Additional file 1: Table S1
**Title.** Inventory of primary and external datasets.
**Description.** Accession, species, tissue or system, number of cells analysed, platform/assay, role in the study, and dataset-specific caveats for the primary HSPC dataset, the five external multiome replications, and the two measured-rate reference panels.
**Format.** .csv (to be supplied as .xlsx at submission)
**Source.** `results/supp_dataset_inventory.csv`
**Cited in.** Methods (datasets); Table 1 footnote.

### Additional file 2: Table S2
**Title.** Inventory of velocity arms and their lag definitions.
**Description.** For each arm (RNA-only scVelo floor, MultiVelo, MultiVeloVAE, MoFlow, CRAK-Velo): model family, chromatin channel, the exact per-gene lag definition, its sign convention (and whether the sign is informative), and the arm's role. Documents why MultiVelo's lag sign is structurally positive and therefore excluded from all sign-based tests.
**Format.** .csv (to be supplied as .xlsx at submission)
**Source.** `results/supp_velocity_arms_inventory.csv` (contains one `<FILL>`: scVelo primary citation)
**Cited in.** Methods (velocity arms); Results (sign convention caveat).

### Additional file 3: Table S3
**Title.** Per-gene chromatin-leading versus RNA-first direction by method, with cross-method consensus.
**Description.** For every gene, the directional lag value from each sign-variable arm (MoFlow, CRAK-Velo, MultiVeloVAE rate-proxy), the resulting direction call, the number of methods available, and the consensus label (unanimous chromatin-leading, unanimous RNA-first, or split). MultiVelo's structurally positive lag is tabulated for completeness but excluded from the consensus. This is the per-gene evidence behind the finding that per-gene direction does not reproduce across methods.
**Format.** .csv
**Source.** `results/per_gene_direction_by_method.csv` (n=1,175 genes; 640 with ≥2 sign-variable methods) · summary in `results/per_gene_direction_summary.md`
**Cited in.** Results (direction reproducibility); Discussion.

### Additional file 4: Table S4
**Title.** Genes whose direction is unanimous across methods, with their quantitative characteristics.
**Description.** The 83 genes called chromatin-leading by every available sign-variable method, together with their chromatin–RNA coupling, mean expression, fitted transcription rate and marker annotation. Accompanying analysis shows these are the highest-expression, highest-α lineage-effector loci, and states explicitly that a signal-to-noise explanation cannot be separated from a biological one.
**Format.** .csv
**Source.** `results/unanimous_chromatin_genes.csv` · interpretation in `results/unanimous_loci_characterization.md`
**Cited in.** Results (where direction is usable); Table 2 conditional row.

### Additional file 5: Table S5
**Title.** Per-gene profile-likelihood stiffness for all four fitted rates.
**Description.** Per-cell-normalised objective-function curvature for α, α_c, β and γ for every gene with a valid fit, the basis for the identifiability ranking and for the stiffness-tertile analysis.
**Format.** .csv
**Source.** `results/stiffness_all_params.csv` (n=538 fitted, 506 with finite curvature)
**Cited in.** Results (identifiability mechanism).

### Additional file 6: Table S6
**Title.** Cross-method concordance on shared genes.
**Description.** Per-gene values used for the cross-method reproducibility comparisons across arms, from which the headline α and lag concordance statistics are computed.
**Format.** .csv
**Source.** `results/concordance_shared.csv`
**Cited in.** Results (reproducibility); Table 1.

### Additional file 7: Table S7
**Title.** External rate validation across strata.
**Description.** All method × cell-line × stratum results for fitted α versus measured TT-seq synthesis rate and for fitted γ versus measured mRNA half-life, including bootstrap confidence intervals, sample sizes and the housekeeping / non-housekeeping split.
**Format.** .csv (two files)
**Source.** `results/external_rate_validation_alpha.csv`, `results/external_rate_validation_gamma.csv` (second α source: `results/external_rate_validation_schwalb.csv`)
**Cited in.** Results (external corroboration).

### Additional file 8: Table S8
**Title.** Stiffness-tertile test of the identifiability-to-external-validation link.
**Description.** Within-parameter, between-gene test results by stiffness tertile for α and γ, including the high-minus-low contrast and its confidence interval — the underpowered test behind the decision not to claim that curvature predicts external validation.
**Format.** .csv
**Source.** `results/curvature_tertile_validation.csv`
**Cited in.** Results (identifiability, suggestive only).

### Additional file 9: Table S9
**Title.** Data-level chromatin–RNA coupling per gene.
**Description.** Per-gene coupling between smoothed chromatin accessibility and spliced RNA, the same quantity recomputed after shuffling ATAC gene labels, and mean expression — the diagnostic showing that the chromatin signal is present in the data even where the model lag is chromatin-invariant.
**Format.** .csv
**Source.** `results/coupling_per_gene.csv`
**Cited in.** Discussion (coupling diagnostic).

### Additional file 10: Data S1
**Title.** Preregistration document and scorecard for the mouse gastrulation replication.
**Description.** The six falsifiable predictions with pre-declared thresholds, sealed by commit hash before any velocity fit existed, together with the scored outcome (6 PASS / 0 FAIL) and the deterministic recomputation record.
**Format.** .pdf (from Markdown) + .csv scorecard
**Source.** `manuscript/PREREGISTRATION_gse205117.md` · `results/prereg_gse205117_scorecard.md` (+ `.csv`)
**Cited in.** Results (preregistered replication); Methods.

### Additional file 11: Supplementary figures (Figures S1–Sn) — `TO BE RENDERED`
**Title.** Supplementary figures supporting the main display items.
**Description.** Planned panels: per-dataset cross-method concordance scatter plots; profile-likelihood curves for representative stiff and sloppy parameters; the ATAC-shuffle null distribution against the observed lag; the coupling shuffle distribution; the stiffness-tertile ladder for α and γ.
**Format.** .pdf (single bundled file)
**Status.** **Not yet rendered.** Figure scripts exist in the repository; panels must be generated before submission. Do not cite as existing until rendered.

### Additional file 12: Table S10
**Title.** Cell-level velocity-matrix audit across methods, with its causal control and reproducibility ceiling.
**Description.** For every method pair on the 21,878 shared cells and 354 usable genes: per-cell and per-gene cosine similarity, the cell-shuffled null and the excess over it, mean-centred values, and per-(cell,gene) sign agreement with the number of zero (undetermined-direction) entries excluded. Includes the ATAC-shuffle contrast, the MultiVelo bootstrap-refit reproducibility ceiling, and the preregistration document whose falsification criteria were sealed before the fitted matrices were read, together with its scored outcome (both preregistered contrasts failed).
**External replication.** The same measure applied to the four external multiomes that carry a second velocity arm and the RNA-only floor (mouse gastrulation, macrophage, human BMMC, E18 mouse brain): pair table plus the paired baseline contrast per system, verdict REPLICATED 4/4 on both raw and mean-centred cosine against a sealed three-of-four threshold. The external systems have no ATAC-shuffle arm and no refit, so neither the causal control nor the reproducibility ceiling is replicated there.
**Format.** .csv (pair tables, HSPC and external) + .pdf (preregistration, main protocol and external appendix)
**Source.** `results/velocity_matrix_audit_pairs.csv` · `results/velocity_matrix_audit.json` · `results/velocity_matrix_audit.md` · `results/velocity_matrix_audit_external_pairs.csv` · `results/velocity_matrix_audit_external.json` · `results/velocity_matrix_audit_external.md` · `manuscript/PREREGISTRATION_velocity_matrix.md`
**Cited in.** Results (cell×gene velocity matrix); Methods (cell-level velocity-matrix audit); Discussion (scope).

---

## Notes for submission preparation
- At submission, convert `.csv` tables to `.xlsx` (BMC accepts both; one sheet per table for multi-file entries such as Additional file 7).
- Main-text citation style is `(Additional file 3: Table S3)`; add the **Additional files** section after Declarations, listing each entry with its title and one-sentence description.
- Remaining `<FILL>` in this package: scVelo primary citation in Additional file 2.
- Figure numbering in the main text is independent of Figure S numbering; supplementary figures are numbered S1 onward inside Additional file 11.
