# Candidate datasets for cross-dataset lag replication — filtered table

> Literature-scout deliverable. Companion to `STATUS.md` (execution state) and
> `../ONBOARDING-cross-dataset-perspective.md` (why each dataset stresses the result differently).
> Purpose: a strictly filtered shortlist for replicating the HSPC lag-robustness result.
> Verified against source papers / GEO on 2026-07-05; unverified items flagged.

## The filter (a dataset qualifies only if ALL hold)
1. **Paired RNA+ATAC in the same cells** — 10x Multiome or SHARE-seq (NOT unpaired scRNA + separate scATAC).
2. **Spliced/unspliced recoverable** — either processed velocity layers are distributed, OR
   BAM/fragments are available to run velocyto/CellRanger-ARC ourselves.
3. **A real differentiation trajectory** — a continuum of states, not a static tissue snapshot.

Most public multiome data fails #2 or #3. Best yield = datasets the multiome-velocity papers themselves
benchmarked on (already velocity-ready and directly comparable to their published lags).

## Strategy note
Our five arms trace to the **MultiVelo family**; MultiVelo's own four datasets and MultiVeloVAE's ten are
the natural pool. Human datasets are preferred: they share the gene-ID axis with our HSPC primary
(GSE209878), so cross-dataset lag-rank comparison needs no ortholog/case mapping (STATUS.md trap #1 —
mouse `Gata1`≠`GATA1` collapses the intersection to ~0).

---

## Filtered candidate table

| # | Accession | Organism / tissue | Assay | Spliced/unspliced recoverable? | Trajectory? | Verdict |
|---|-----------|-------------------|-------|-------------------------------|-------------|---------|
| P | **GSE209878** | Human HSPC (CD34+) | 10x Multiome | ✅ (our P1 pipeline) | ✅ hematopoiesis, 7 lineages | **PRIMARY (done)** |
| 1 | **GSE162170** | Human fetal cerebral cortex | 10x Multiome | ✅ processed spliced/unspliced provided | ✅ neurogenesis (RG→IPC→ExN, IN, OPC) | **GO (in progress)** |
| 2 | **GSE194122** | Human bone marrow (BMMC) | 10x Multiome | ⚠️ raw only → recover from BAM/fragments | ✅ hematopoiesis | **GO (next)** |
| 3 | 10x "Fresh Embryonic E18 Mouse Brain (5k)" | Mouse E18 brain | 10x Multiome | ✅ spliced/unspliced on MultiVelo GitHub | ✅ neurogenesis (cycling-rich) | **GO (low-effort)** |
| 4 | **GSE140203** | Mouse skin (hair follicle) | SHARE-seq | ⚠️ raw only, non-10x → heavier reprocessing | ✅ TAC→hair shaft (strong priming) | **DEFER** |
| 5 | MultiVeloVAE new sets (embryoid body, macrophage diff.) | Human | 10x Multiome | ✅ likely velocity-ready (authors ran velocity) | ✅ differentiation | **DEFER (accession unverified)** |
| 6 | Unpaired scRNA + scATAC atlases (generic) | various | separate assays | ❌ not same-cell | — | **SKIP** |

---

## Per-candidate verdict + reasoning

### 1. GSE162170 — Human fetal cortex (Trevino et al. 2021, Cell) — **GO (in progress)**
- **Why it passes:** processed spliced/unspliced counts distributed directly (no BAM reprocessing);
  human, so gene axis overlaps HSPC (no ortholog mapping); genuine neurogenic trajectory.
- **Value:** transient-TF-rich system → lag expected *more* method-sensitive; a fair external test of the
  α-robust / lag-fragile split. This is a MultiVelo original dataset (developing human cortex) so results
  are directly comparable to published lags.
- **State:** built (8,414 cells after QC, 6 cortical lineages), RNA-only floor done, MultiVelo full run +
  P3 concordance running under the autonomous driver (see STATUS.md). ⚠️ Uses foreign provider
  spliced/unspliced — fine for a *cross-dataset* concordance test (adds noise only → conservative w.r.t.
  the "lag fragile" conclusion), but note it in Methods.

### 2. GSE194122 — Human bone marrow BMMC (NeurIPS 2021 multimodal) — **GO (recommended next)**
- **Why it passes:** 10x Multiome, same-cell RNA+ATAC; **human hematopoiesis — the same lineage axis as
  our HSPC primary**, which is the single most informative external test (same biology, independent
  donors/sites). Used by MultiVeloVAE, so velocity-ready reference results exist.
- **Cost/risk:** GEO deposits raw sequencing → spliced/unspliced must be recovered from BAM/fragments
  (velocyto/CellRanger-ARC). Moderate effort but the exact P1 path we already built for HSPC. 12 donors ×
  4 sites → strong batch structure; subset to a clean donor/site or model batch, mirroring HSPC handling.
- **Why not #1:** biological redundancy with HSPC is a feature (tightest replication) but the cortex is
  already in flight and tests a *different* tissue; run GSE194122 immediately after to nail the
  same-tissue reproducibility claim.

### 3. 10x "Fresh Embryonic E18 Mouse Brain (5k)" — **GO (lowest effort)**
- **Why it passes:** the MultiVelo tutorial dataset — spliced/unspliced counts and cell annotations are
  already published on the MultiVelo GitHub, so it is the fastest possible second replication (near-zero
  preprocessing). Cycling-RG-rich → the strongest **cell-cycle confound stress-test** for our
  "cell-cycle is gene-level-unbiased, within-lineage-controlled" claim.
- **Caveat:** mouse → cross-species gene-axis mapping (case/ortholog) required before per-gene lag-rank
  comparison to HSPC (STATUS.md trap #1). Within-dataset cross-method concordance (our core H1) needs no
  mapping, so this dataset still yields the primary result even without ortholog work.
- **Accession:** 10x-hosted demo (no GSE); cite the 10x Genomics dataset page + MultiVelo GitHub for the
  velocity layers.

### 4. GSE140203 — Mouse skin SHARE-seq (Ma et al. 2020, Cell) — **DEFER**
- **Why it (barely) passes the filter:** same-cell RNA+ATAC (SHARE-seq), clear TAC→hair-shaft trajectory,
  and it is the canonical **chromatin-potential / priming best case** — the ideal place to test "is lag
  robust even where priming is strongest?"
- **Why defer:** only `GSE140203_RAW.tar` (no spliced/unspliced); SHARE-seq is **not 10x**, so our
  CellRanger-ARC path does not apply — needs a bespoke velocyto/spliced-recovery route. Mouse → ortholog
  mapping too. High effort; take it only after two human GO datasets confirm the pattern, then it becomes
  the strongest headline ("fragile even in the priming best case").

### 5. MultiVeloVAE-generated sets (human embryoid body, macrophage differentiation) — **DEFER (verify accession)**
- **Why interesting:** newly generated 10x Multiome with differentiation trajectories, run through
  velocity by the authors → likely velocity-ready with reference lags. Human embryoid body adds a
  developmental axis; macrophage differentiation is closer to the drug-timing endpoint.
- **Blocker:** exact GEO accessions not confirmed in this pass (Data-availability section was truncated in
  the fetch). ⚠️ **Do not cite an accession until verified** — pull from the MultiVeloVAE (Nat Commun 16,
  11505, 2025) data-availability statement before use.

### 6. Generic unpaired scRNA + scATAC atlases — **SKIP**
- Fail filter #1 (not same-cell). Chromatin↔transcription lag requires paired measurement per cell; any
  integration-inferred pairing would confound the very quantity we measure. Exclude categorically.

---

## Recommended order
1. Finish **GSE162170** (running).
2. **GSE194122** — same-tissue human hematopoiesis, tightest replication of the HSPC result.
3. **E18 mouse brain (10x)** — cheapest add + cell-cycle stress-test (within-dataset H1 first; ortholog
   mapping only if cross-dataset rank comparison is wanted).
4. Then **GSE140203** (priming best case) and the **MultiVeloVAE** sets if accessions verify.

## Acquisition log 2026-07-05 (Track B — see `P0_provenance_crossdataset.md` for full sha256/URLs)
- **E18 mouse brain 5k (10x Multiome)** — DOWNLOADED to `data/e18_mouse_brain/`. spliced/unspliced **verified
  present** in `10X_multiome_mouse_brain.loom` (4881×32285; spliced 5.30% / unspliced 5.40% nnz, both nonzero).
  All MultiVelo P1 inputs staged (filtered matrix + peak_annotation + feature_linkage.bedpe + cell_annotations + WNN).
  **Verdict: GO now (velocity-ready, lowest effort).** ⚠️ Version correction: this dataset is CellRanger-ARC **1.0.0**
  (`...-1-standard-1-0-0`), not `2-0-0` as row 3 above stated — the Demo notebook and the loom use 1.0.0.
- **GSE194122 human BMMC** — processed h5ad STAGED to `data/GSE194122/` (2.79 GB, complete). h5ad `layers=['counts']`
  only → **no spliced/unspliced**. Recovery diagnosed: not velocity-ready anywhere (MultiVeloVAE points back here;
  its figshare has HSPC/EB/macrophage, not BMMC). Raw = **original 10x GEX possorted BAM, publicly retrievable on SRA**
  (VERIFIED via SDL locate API: `SRR17693266` → `site4_donor09_multiome_gex.possorted_genome_bam.bam`, 28.66 GB,
  public `sra-pub-src-2` S3, no dbGaP) → **velocyto-on-BAM = moderate** (not a FASTQ→CellRanger rerun). **Verdict:
  DEFER the velocyto pass (~29 GB/donor + hours) to a dedicated run; highest replication value once loom recovered.**

## Sources
- GSE162170 / Trevino et al. 2021 Cell: https://doi.org/10.1016/j.cell.2021.07.039
- GSE194122 (NeurIPS 2021 BMMC multiome): https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE194122
- 10x E18 mouse brain demo: https://www.10xgenomics.com/datasets/fresh-embryonic-e-18-mouse-brain-5-k-1-standard-2-0-0 · velocity layers: https://github.com/welch-lab/MultiVelo
- GSE140203 / Ma et al. 2020 Cell (SHARE-seq): https://doi.org/10.1016/j.cell.2020.09.056
- MultiVeloVAE datasets: https://www.nature.com/articles/s41467-025-66287-6 · https://pmc.ncbi.nlm.nih.gov/articles/PMC12748740/
