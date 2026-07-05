# Cross-dataset P0 provenance — Track B acquisition (2026-07-05)

> Companion to `candidate_datasets.md` (verdicts) and `STATUS.md` (execution state).
> Records accession, URLs, file list, sha256, license, and the **spliced/unspliced availability verdict**
> for the two Track-B cross-dataset benchmark datasets. Mirrors `data/GSE209878/P0_provenance.md` style.
> Data live under `pipeline/hspc-velocity-benchmark/data/` (gitignored — binaries not committed).

---

## Dataset A — E18 mouse brain 5k (10x Multiome) — **DOWNLOADED, velocity-ready, GO**

MultiVelo tutorial dataset. spliced/unspliced are distributed directly → **cheapest possible second replication**
(near-zero preprocessing) and the strongest cell-cycle confound stress-test (cycling-RG-rich).

- **Accession:** no GSE. 10x Genomics hosted demo "Fresh Embryonic E18 Mouse Brain (5k)", CellRanger-ARC **1.0.0**
  (`e18_mouse_brain_fresh_5k`). Velocity layers + annotations from `welch-lab/MultiVelo` GitHub (Examples/).
  - ⚠️ **candidate_datasets.md doc error:** it cited the `...-2-0-0` version. The MultiVelo Demo notebook
    (authoritative for "what the tutorial uses") and the distributed loom were built against **1-0-0**. Use 1.0.0.
- **Location:** `data/e18_mouse_brain/`
- **License:** 10x Genomics public datasets — Creative Commons Attribution (CC BY). MultiVelo repo files (loom,
  cell_annotations.tsv) — repo is BSD-3-Clause (`welch-lab/MultiVelo`); loom is velocyto-quantified from the 10x public BAM.

### Files (sha256 = first 16 hex)
| file | size | sha256… | source |
|---|---|---|---|
| `10X_multiome_mouse_brain.loom` | 87M | `5620bccd41c275e8` | GitHub welch-lab/MultiVelo `Examples/velocyto/` |
| `cell_annotations.tsv` | 136K | `e568dc50ff33ab0f` | GitHub `Examples/cell_annotations.tsv` |
| `e18_filtered_feature_bc_matrix.tar.gz` | 195M | `dad70202574ad0cd` | 10x `..._filtered_feature_bc_matrix.tar.gz` |
| ↳ extracted `filtered_feature_bc_matrix/{barcodes,features,matrix}.{tsv,mtx}.gz` | | | (GEX + ATAC Peaks combined matrix) |
| `e18_atac_peak_annotation.tsv` | 6.6M | `603564fc7bd6bd61` | 10x `..._atac_peak_annotation.tsv` |
| `e18_analysis.tar.gz` | 290M | `6806c85fbcffc462` | 10x `..._analysis.tar.gz` (secondary analysis) |
| ↳ extracted `analysis/feature_linkage/feature_linkage.bedpe` | 14M | `aadd54a916451c50` | (peak–gene linkage for `mv.aggregate_peaks_10x`) |
| `seurat_wnn.zip` → `seurat_wnn/{nn_idx,nn_dist,nn_cells}.txt` | 1.6M | — | GitHub `Examples/seurat_wnn/` (optional; pyWNN can recompute) |

### URLs
- Loom: `https://raw.githubusercontent.com/welch-lab/MultiVelo/main/Examples/velocyto/10X_multiome_mouse_brain.loom`
- Annotations: `https://raw.githubusercontent.com/welch-lab/MultiVelo/main/Examples/cell_annotations.tsv`
- 10x base: `https://cf.10xgenomics.com/samples/cell-arc/1.0.0/e18_mouse_brain_fresh_5k/e18_mouse_brain_fresh_5k_{filtered_feature_bc_matrix.tar.gz, atac_peak_annotation.tsv, analysis.tar.gz}`
- 10x dataset page: `https://www.10xgenomics.com/resources/datasets/fresh-embryonic-e-18-mouse-brain-5-k-1-standard-1-0-0`

### Spliced/unspliced verdict — **YES, PROVIDED (verified)**
Opened loom with `anndata.read_loom`: **4881 cells × 32285 genes**, `layers = [matrix, ambiguous, spliced, unspliced]`.
- spliced: sum=17,885,009, nnz=8,354,431 (5.30% dense)
- unspliced: sum=23,547,664, nnz=8,510,278 (5.40% dense)
Both nonzero and healthy → velocity-ready. All CellRanger-ARC inputs for `mv.aggregate_peaks_10x` (filtered matrix +
peak_annotation + feature_linkage.bedpe) present → the MultiVelo P1 path applies verbatim.

### Caveats for P1→P2
- **Mouse gene symbols** (var_names e.g. `AC125149.3`). Within-dataset cross-method concordance (core H1) needs no
  mapping. Cross-dataset per-gene lag-rank vs human HSPC requires ortholog/case mapping first (STATUS.md trap #1).
- WNN neighbors provided (`seurat_wnn/`) but tied to the tutorial cell subset; pyWNN can recompute for our QC set.

---

## Dataset B — GSE194122 human BMMC (NeurIPS 2021 multimodal, 10x Multiome) — **STAGED; recovery = velocyto-on-BAM (moderate)**

Same hematopoietic axis as HSPC primary (tightest replication). Human → gene axis overlaps GSE209878 (no ortholog map).

- **Accession:** GEO **GSE194122** → BioProject **PRJNA799242** → SRA study **SRP356158**. Submitter CELLARITY. Homo sapiens.
- **Location:** `data/GSE194122/`
- **License:** GEO public (open access; no dbGaP restriction on this series — reads are public on SRA).

### Downloaded
| file | size | sha256… | source |
|---|---|---|---|
| `GSE194122_multiome_BMMC_processed.h5ad.gz` | 2.79 GB (2,917,117,242 B, complete) | `53b516e7a35518e7` | GEO suppl |

Companion `..._cite_BMMC_processed.h5ad.gz` (CITE-seq) exists but is not multiome → not fetched.

### Processed h5ad structure (verified via h5py)
- `layers = ['counts']` — **NO spliced/unspliced.**
- `var`: `feature_types` (GEX + ATAC Peaks concatenated), `gene_id`.
- `obsm`: `ATAC_gene_activity` (provider gene-activity — do NOT use; would confound method vs preprocessing),
  `GEX_X_pca`, `GEX_X_umap`, `ATAC_lsi_*`, `ATAC_umap`.
- `obs`: `GEX_pseudotime_order`, `ATAC_pseudotime_order` (trajectory present), `GEX_phase` (cell-cycle), `DonorID`,
  `Site`, `Samplename`, `Modality`, per-cell QC. → strong batch structure (multiple donors × 4 sites) → subset a
  clean donor/site or model batch, mirroring HSPC handling.

### Spliced/unspliced verdict — **NO in the processed h5ad; RECOVERABLE via velocyto on the GEX BAM (moderate)**
Recovery-path diagnosis (SRA metadata via eutils efetch, not assumed):
1. **Velocity-ready elsewhere? NO.** MultiVeloVAE (Nat Commun 2025, PMC12748740) analyzed BMMC but points back to
   GSE194122 as "previously published, freely available." Its new deposits (GEO **GSE284047** = HSPC+macrophage+EB;
   figshare **10.6084/m9.figshare.30280333** = post-processed AnnData for `3423-MV`/`8489-MV`/`8964-KL`/`9060-MV`
   samples — i.e. HSPC/EB/macrophage, **not** BMMC) do **not** include a velocity-ready BMMC object.
   - Bonus note (out of Track-B scope): figshare 30280333 contains `3423-MV-2_adata_postpro` — that is the
     **GSE209878 HSPC day7** sample, post-processed by MultiVeloVAE; a possible reference-lag cross-check later.
2. **Raw tier = original 10x possorted BAM on SRA, PUBLICLY retrievable (moderate — VERIFIED, NOT a FASTQ→CellRanger rerun).**
   Confirmed via the SDL locate API (`https://locate.ncbi.nlm.nih.gov/sdl/2/retrieve?acc=SRR17693266`), not just the
   metadata reference — the original BAM is exposed as a public object:
   - RNA/GEX run `SRR17693266` (GSM5828480) → `type:TenX` **`site4_donor09_multiome_gex.possorted_genome_bam.bam`**,
     **28.66 GB** (md5 `a7fed3450edf61dbba4d102087cb282d`), public S3:
     `https://sra-pub-src-2.s3.amazonaws.com/SRR17693266/site4_donor09_multiome_gex.possorted_genome_bam.bam.1`
     (no dbGaP / no auth). The separate `.sra` object (11.4 GB) is the SRA-normalized reads — **not** what velocyto needs.
   - ATAC run e.g. `SRR17693253` (GSM5828493) → `site4_donor09_multiome_atac.possorted_genome_bam.bam` (same scheme).
   - Project runs: **25 RNA-Seq + 13 ATAC-seq** (PRJNA799242).
   - **Recovery = velocyto (`velocyto run` / `run10x`) directly on the GEX possorted BAM** (carries CB/UB tags) with a
     GRCh38 GTF + the filtered-barcode list from the processed h5ad → spliced/unspliced loom. Same difficulty tier as
     the HSPC P1 (which consumed a velocyto loom). **NOT** a CellRanger-ARC rerun from FASTQ (heavy tier avoided because
     the original possorted BAM is public).
   - Retrieval: `prefetch --type all SRRxxxx` (or curl the `sra-pub-src-2` S3 link above); default `.sra` gives
     normalized reads only.
   - Per-sample cost: **~29 GB BAM download + a velocyto pass (hours)**. Stage one clean donor/site first (e.g.
     `site4_donor09`) rather than all 13.

### URLs
- GEO suppl: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE194nnn/GSE194122/suppl/GSE194122_openproblems_neurips2021_multiome_BMMC_processed.h5ad.gz`
- BioProject: `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA799242`  · SRA study SRP356158
- SRA run metadata (eutils): `efetch.fcgi?db=sra&id=<uid>` → RUN_SET/Files carries original BAM filename+semantic_name.

---

## Go/defer for running P1→P2 next
- **E18 mouse brain — GO now (lowest effort).** Velocity-ready, all MultiVelo inputs present, no recovery step. Yields
  the core within-dataset cross-method H1 with zero preprocessing; ortholog mapping only if cross-dataset rank vs HSPC
  is wanted. Cheapest add + cell-cycle stress-test.
- **GSE194122 — DEFER the heavy step, but recovery is only moderate.** Staged (processed h5ad down). Before P1→P2 it
  needs one velocyto pass on the GEX possorted BAM for a chosen donor/site (~11–17 GB + hours) — do that in a dedicated
  pass, not this acquisition pass. Highest scientific value (same-tissue human hematopoiesis, tightest HSPC replication)
  once the loom is recovered.
