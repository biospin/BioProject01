#!/usr/bin/env python3
"""p9_supp_inventories.py — Supplementary inventory tables for the Genome Biology submission (BIOP01-56).

Writes two literal inventory tables that the manuscript cites but that no analysis
script emitted:
  - results/supp_velocity_arms_inventory.csv  (Additional file 1: Table S1)
  - results/supp_dataset_inventory.csv        (Additional file 2: Table S2)

Provenance of every value:
  - velocity arms          : manuscript/draft_v2.md Methods "Velocity methods and the RNA-only floor";
                             lag column definitions from scripts/p8_per_gene_direction_table.py.
  - primary/external cells : n_obs of data/processed*/rna_spliced_unspliced.h5ad
                             (21878 / 3572 / 2850 / 8414 / 10779 / 4423), cross-checked
                             against results/runtime.csv n_cells.
  - accessions / platforms : manuscript/draft_v2.md Methods "Datasets" and Declarations.
  - measured-rate refs     : data/PROVENANCE_halflife.md.
Unknown values are written as <FILL>; nothing is inferred or invented.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "results")

ARMS_HEADER = [
    "arm", "method", "reference", "model_family", "chromatin_channel",
    "lag_definition", "lag_sign_convention", "role_in_study",
]
ARMS = [
    ["RNA-only floor", "scVelo (dynamical model)", "<FILL: scVelo primary citation, not yet in the manuscript reference list>",
     "ODE, splicing kinetics only", "none (RNA spliced/unspliced only)",
     "not defined (no chromatin channel)", "not applicable",
     "Lower bound: what is recoverable without chromatin; α and γ only"],
    ["chromatin-informed", "MultiVelo", "Li 2023 [1]",
     "chromatin switch-time ODE", "ATAC aggregated to gene level",
     "lag = t_sw2 - t_sw1 (switch-time difference)",
     "structurally positive (switch times are monotonically ordered), hence uninformative for sign",
     "Primary chromatin-informed arm; profile-likelihood and ATAC-shuffle control run on this arm"],
    ["chromatin-informed", "MultiVeloVAE", "Li 2025 [2]",
     "variational autoencoder, continuous per-cell decoupling and coupling",
     "ATAC aggregated to gene level",
     "rate-proxy lag = 1/alpha_c - 1/alpha (column vae_proxy_lag)",
     "sign-variable (direction informative)",
     "Second chromatin-informed arm; the within-dataset lag axis in Table 1 is MultiVelo versus MultiVeloVAE"],
    ["chromatin-informed", "MoFlow", "Hong 2025 [3]",
     "relay velocity", "ATAC aggregated to gene level",
     "chromatin-to-spliced DTW lag (cs_lag_median, fastdtw)",
     "sign-variable (direction informative)",
     "Third chromatin-informed arm; carries the sealed per-gene lag prediction in the gastrulation preregistration"],
    ["chromatin-informed (sensitivity only)", "CRAK-Velo", "El Kazwini 2026 [4]",
     "semi-mechanistic", "cisTopic-derived chromatin representation",
     "DTW-derived lag (cs_lag_median)",
     "sign-variable; an opposite-sign convention bug relative to MoFlow fastdtw was found and corrected",
     "Sensitivity arm only, because the DTW construct produces a shape artifact on smooth dynamics"],
]

DATA_HEADER = [
    "dataset", "accession", "species", "tissue_or_system", "cells_analyzed",
    "platform_assay", "role", "notes",
]
DATASETS = [
    ["Human HSPC (day0 + day7, integrated)", "GSE209878", "human",
     "haematopoietic stem and progenitor cells", "21878", "10x Multiome (RNA + ATAC)",
     "primary dataset",
     "Day0 and day7 batch-integrated; the lag is therefore in pseudotime units, not wall-clock"],
    ["Macrophage differentiation (Day14, HSPC-direct)", "GSE284047 (figshare 30280333)",
     "human", "macrophage differentiation from HSPC", "3572", "10x Multiome (RNA + ATAC)",
     "external replication (cross-method and cross-dataset)",
     "Nearest lineage to the primary dataset; single sample"],
    ["Human bone-marrow mononuclear cells (BMMC)", "GSE194122", "human",
     "bone marrow", "2850", "10x Multiome (RNA + ATAC)",
     "external replication (cross-method and cross-dataset)",
     "donor09 / site4; spliced and unspliced recovered from the GEX BAM with velocyto; single donor"],
    ["Human fetal cortex (Trevino 2021)", "GSE162170", "human",
     "developing cerebral cortex", "8414", "10x Multiome (RNA + ATAC)",
     "external replication (cross-dataset axis only)",
     "No MultiVeloVAE fit, so within-dataset cross-method alpha and lag are not computable (Table 1, N/A)"],
    ["Mouse gastrulation (E7.5 / E8.0 / E8.5 / E8.75, rep1)", "GSE205117", "mouse",
     "gastrulating embryo (priming-maximal developmental atlas)", "10779",
     "10x Multiome (RNA + ATAC)",
     "external replication, preregistered confirmatory test",
     "GEX via STARsolo Velocyto raw; ATAC aggregated from GEO fragments over gene bodies +/-10 kb (gencode vM25); scored 6 PASS / 0 FAIL against thresholds sealed by commit hash before fitting"],
    ["Fresh Embryonic E18 Mouse Brain 5k (10x demo)",
     "none (10x Genomics demo dataset, no GEO accession)", "mouse", "embryonic E18 brain",
     "4423", "10x Multiome (RNA + ATAC), CellRanger-ARC 1.0.0",
     "external replication (cross-method and cross-dataset)",
     "MultiVelo tutorial data; the cross-species arm"],
    ["K562 TT-seq synthesis rates (Todorovski 2024)",
     "GSE229305 (subseries of GSE229314)", "human", "K562 (CML cell line), bulk",
     "not applicable (bulk; 11776 genes)", "TT-seq",
     "measured synthesis-rate reference (external corroboration of alpha)",
     "Untreated condition; primary external synthesis-rate anchor"],
    ["K562 TT-seq synthesis rates (Schwalb 2016)", "GSE75792", "human",
     "K562 (CML cell line), bulk", "not applicable (bulk; 2746 genes after gene-level mapping)",
     "TT-seq",
     "second, independent measured synthesis-rate reference",
     "Per-transcriptional-unit rates remapped to genes via GENCODE v19; did not corroborate the primary source (the two measured K562 sources agree only at rho about 0.15)"],
    ["K562 and THP-1 mRNA half-life (Todorovski 2024)", "GSE229314 (Supplementary Table S10)",
     "human", "K562 and THP-1 (AML) cell lines, bulk",
     "not applicable (bulk; 6580 and 7001 genes)", "SLAM-seq",
     "measured degradation reference (external test of gamma)",
     "Untreated sheets; right-censored at a 24 h ceiling (8.1% of K562 genes), noted in the degradation analysis"],
    ["MOLM-13 mRNA half-life (RNADecayCafe reprocessing of Muhar 2018)",
     "Zenodo record 15785218 (original study: Muhar 2018 SLAM-seq)", "human",
     "MOLM-13 (AML) cell line, bulk", "not applicable (bulk; 10624 genes)", "SLAM-seq",
     "cross-study measured degradation reference",
     "Independent laboratory and independent reprocessing pipeline; the cross-study transfer reference"],
]


def write(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


if __name__ == "__main__":
    write(os.path.join(RES, "supp_velocity_arms_inventory.csv"), ARMS_HEADER, ARMS)
    write(os.path.join(RES, "supp_dataset_inventory.csv"), DATA_HEADER, DATASETS)
