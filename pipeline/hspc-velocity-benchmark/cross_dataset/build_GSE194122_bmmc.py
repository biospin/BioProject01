#!/usr/bin/env python3
"""GSE194122 human BMMC 10x Multiome (donor09) → processed h5ad (build + finalize 합침).

cross-dataset 재현 4번(same-tissue human hematopoiesis, HSPC 최근접 replication). velocyto로 복구한
RNA loom + processed h5ad의 ATAC peak matrix를 받아 HSPC/human_brain/E18과 **동일 스키마**로 마감한다.

입력:
  - RNA : data/GSE194122_bmmc_velocyto/*.loom (donor09 GEX BAM velocyto run 산출; spliced/unspliced)
  - ATAC: data/GSE194122/GSE194122_multiome_BMMC_processed.h5ad (donor09=batch 's4d9', counts layer,
          feature_types=='ATAC' peaks 'chr1-9776-10668', + obs['cell_type'])
  - GTF : data/ref/gencode.v44.basic.annotation.gtf.gz (human — human_brain과 동일 재사용)

산출 (config_GSE194122_bmmc.OUT = data/processed_GSE194122_bmmc):
  - rna_spliced_unspliced.h5ad : cells×genes, X=spliced+unspliced, layers{counts,spliced,unspliced},
                                 obs{cell_type,lineage,leiden}, human gene SYMBOL 축, HVG/PCA/neighbors 완료
  - atac_gene.h5ad             : cells×genes, gene-level accessibility (gencode-proximity 집계)

⚠️ ATAC 집계: HSPC는 mv.aggregate_peaks_10x(peak_annotation+linkage)였으나 GSE194122는 ARC ancillary
   미제공 → human_brain과 동일 gencode gene-body ±PEAK_DIST proximity 집계(구현 차이 문서화).
   lineage: 제공된 obs['cell_type'] 직접 사용(조혈 marker 강제 안 함; concordance는 전역 fit rank).

실행 (scv-preprocess env):
  conda run --no-capture-output -n scv-preprocess python -u cross_dataset/build_GSE194122_bmmc.py
"""
from __future__ import annotations
import gzip
import re
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scanpy as sc
import anndata as ad

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                   # pipeline/hspc-velocity-benchmark
LOOM_DIR = ROOT / "data" / "GSE194122_bmmc_velocyto"
H5AD = ROOT / "data" / "GSE194122" / "GSE194122_multiome_BMMC_processed.h5ad"
GTF = ROOT / "data" / "ref" / "gencode.v44.basic.annotation.gtf.gz"
OUT = ROOT / "data" / "processed_GSE194122_bmmc"
OUT.mkdir(parents=True, exist_ok=True)

BATCH = "s4d9"                                        # donor09 = site4/donor9 (SRR17693266)
# HSPC와 동일 하이퍼파라미터 (공정 비교)
N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, SEED = 2000, 30, 30, 1.0, 0
PEAK_DIST = 10000                                    # gene body ±bp (mv.aggregate_peaks_10x 기본과 정합)
QC = dict(min_genes=500, max_genes=8000, max_pct_mito=20.0)
RARE = {"pDC", "cDC2", "Plasma cell", "MK/E prog", "Normoblast", "ID2-hi myeloid prog", "ILC"}


def core_barcodes(names):
    """velocyto/anndata barcode를 16bp core로 정규화.
    'PREFIX:AAAC...x' | 'AAAC...-1' | 'AAAC...-12-s4d9' → 'AAAC...'."""
    out = []
    for b in map(str, names):
        b = b.split(":")[-1]
        if b.endswith("x"):
            b = b[:-1]
        b = b.split("-")[0]
        out.append(b)
    return out


def load_gencode_genes(path: Path) -> pd.DataFrame:
    """gencode gtf → gene별 (symbol, chrom, start, end). basic annotation의 gene feature만."""
    rows = []
    pat_name = re.compile(r'gene_name "([^"]+)"')
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] != "gene":
                continue
            m = pat_name.search(f[8])
            if not m:
                continue
            rows.append((m.group(1), f[0], int(f[3]), int(f[4])))
    df = pd.DataFrame(rows, columns=["symbol", "chrom", "start", "end"])
    df = df.groupby(["symbol", "chrom"], as_index=False).agg(start=("start", "min"), end=("end", "max"))
    return df


def aggregate_peaks_to_genes(atac, genes_df, target_genes):
    """peak-level ATAC(cells×peaks, var seqnames/start/end) → gene-level(cells×genes).
    gene body ±PEAK_DIST 창에 겹치는 peak 합산 (finalize_human_brain.py와 동일 구현)."""
    peaks = atac.var
    P = atac.X.tocsc()
    gsel = genes_df[genes_df["symbol"].isin(set(target_genes))].reset_index(drop=True)
    print(f"  gencode genes ∩ RNA: {gsel.shape[0]}", flush=True)
    cols_gene, cols_peak = [], []
    peak_start = peaks["start"].to_numpy()
    peak_end = peaks["end"].to_numpy()
    peak_chrom = peaks["seqnames"].astype(str).to_numpy()
    by_chrom = {}
    for c in np.unique(peak_chrom):
        idx = np.where(peak_chrom == c)[0]
        order = idx[np.argsort(peak_start[idx])]
        by_chrom[c] = (order, peak_start[order], peak_end[order])
    for gi, row in enumerate(gsel.itertuples(index=False)):
        ch = row.chrom
        if ch not in by_chrom:
            continue
        order, ps, pe = by_chrom[ch]
        lo, hi = row.start - PEAK_DIST, row.end + PEAK_DIST
        j = np.searchsorted(ps, hi, side="right")
        cand = order[:j]
        ce = pe[:j]
        keep = cand[ce >= lo]
        if keep.size:
            cols_gene.append(np.full(keep.size, gi, dtype=np.int32))
            cols_peak.append(keep.astype(np.int32))
    if not cols_gene:
        raise RuntimeError("peak→gene 겹침 0 — 좌표계(chr prefix) 불일치 의심")
    g_idx = np.concatenate(cols_gene)
    p_idx = np.concatenate(cols_peak)
    M = sp.csr_matrix((np.ones(g_idx.size, np.float32), (g_idx, p_idx)),
                      shape=(gsel.shape[0], atac.n_vars))
    gene_counts = (P @ M.T).tocsr()
    print(f"  peak→gene pairs: {g_idx.size}, genes with ≥1 peak: "
          f"{(np.asarray((M.sum(1))).ravel()>0).sum()}", flush=True)
    out = ad.AnnData(X=gene_counts, obs=atac.obs.copy(),
                     var=pd.DataFrame(index=gsel["symbol"].to_numpy()))
    out.var_names_make_unique()
    return out


def find_loom() -> Path:
    looms = sorted(LOOM_DIR.glob("*.loom"))
    if not looms:
        raise FileNotFoundError(f"velocyto loom 없음: {LOOM_DIR}/*.loom")
    return looms[0]


def main():
    sc.settings.verbosity = 1

    # ── RNA (velocyto loom: spliced/unspliced) ──
    loom = find_loom()
    print(f"[RNA] read loom {loom.name}", flush=True)
    rna = ad.read_loom(str(loom))
    rna.var_names_make_unique()
    rna.obs_names = core_barcodes(rna.obs_names)
    rna = rna[~rna.obs_names.duplicated()].copy()
    for lyr in ("spliced", "unspliced"):
        assert lyr in rna.layers, f"loom에 {lyr} layer 없음"
    rna.X = (rna.layers["spliced"] + rna.layers["unspliced"]).copy()
    print(f"  RNA {rna.shape}, layers={list(rna.layers)}", flush=True)

    # ── ATAC + cell_type (processed h5ad, donor09=s4d9) ──
    print(f"[ATAC] read h5ad (backed) {H5AD.name}, subset batch=={BATCH}", flush=True)
    full = ad.read_h5ad(H5AD, backed='r')
    sub = full[full.obs['batch'] == BATCH]
    obs = sub.obs.copy()
    obs.index = core_barcodes(obs.index)
    atac_mask = (full.var['feature_types'] == 'ATAC').values
    atac_var = full.var[atac_mask]
    # counts layer (raw integer peak counts; X는 binarized라 사용 안 함)
    atac_counts = sub[:, atac_mask].layers['counts']
    atac_counts = atac_counts[:] if not sp.issparse(atac_counts) else atac_counts
    atac_counts = sp.csr_matrix(atac_counts)
    # peak 좌표 파싱 'chr1-9776-10668'
    seqn, start, end = [], [], []
    for p in atac_var.index.astype(str):
        c, s, e = p.rsplit('-', 2)
        seqn.append(c); start.append(int(s)); end.append(int(e))
    atac = ad.AnnData(
        X=atac_counts,
        obs=obs.copy(),
        var=pd.DataFrame({"seqnames": seqn, "start": start, "end": end},
                         index=atac_var.index.astype(str)),
    )
    atac.obs_names = core_barcodes(atac.obs_names)
    atac = atac[~atac.obs_names.duplicated()].copy()
    print(f"  ATAC(peaks) {atac.shape}, seqnames example={atac.var['seqnames'].iloc[0]}", flush=True)

    # ── cell 정합 (loom RNA ∩ h5ad donor09) ──
    common = [c for c in rna.obs_names if c in set(atac.obs_names)]
    print(f"[align] RNA(loom)∩ATAC(h5ad donor09) cells: {len(common)} "
          f"(RNA {rna.n_obs}, ATAC {atac.n_obs})", flush=True)
    assert len(common) >= 500, f"교집합 {len(common)} < 500 — barcode 정규화/donor 확인"
    rna = rna[common].copy()
    atac = atac[common].copy()
    rna.obs["cell_type"] = obs.loc[common, "cell_type"].astype(str).values
    rna.obs["dataset"] = "GSE194122_bmmc"

    # ── QC on RNA ──
    rna.var["mito"] = rna.var_names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(rna, inplace=True, percent_top=None)
    if rna.var["mito"].any():
        rna.obs["pct_mito"] = (np.asarray(rna[:, rna.var["mito"]].X.sum(1)).ravel()
                               / np.asarray(rna.X.sum(1)).ravel() * 100)
    else:
        rna.obs["pct_mito"] = 0.0
    n0 = rna.n_obs
    sc.pp.filter_cells(rna, min_genes=QC["min_genes"])
    rna = rna[(rna.obs["n_genes_by_counts"] <= QC["max_genes"])
              & (rna.obs["pct_mito"] <= QC["max_pct_mito"])].copy()
    print(f"[QC] {n0} → {rna.n_obs} cells (mito≤{QC['max_pct_mito']}, genes {QC['min_genes']}~{QC['max_genes']})",
          flush=True)
    atac = atac[rna.obs_names].copy()

    # ── 정규화 + HVG + graph (HSPC p1_build 순서 복제) ──
    rna.layers["counts"] = rna.X.copy()
    sc.pp.normalize_total(rna, target_sum=1e4)
    sc.pp.log1p(rna)
    sc.pp.highly_variable_genes(rna, n_top_genes=N_HVG)
    sc.pp.pca(rna, n_comps=N_PCS, random_state=SEED)
    sc.pp.neighbors(rna, n_neighbors=N_NEIGHBORS, random_state=SEED)
    sc.tl.leiden(rna, resolution=LEIDEN_RES, random_state=SEED, key_added="leiden")
    print(f"[graph] leiden clusters: {rna.obs['leiden'].nunique()}, "
          f"HVG: {int(rna.var['highly_variable'].sum())}", flush=True)

    # lineage = 제공 cell_type (marker 강제 안 함)
    rna.obs["lineage"] = rna.obs["cell_type"].astype("category")
    rna.obs["lineage_rare"] = rna.obs["lineage"].isin(RARE)
    print("  cell_type 분포:\n    "
          + rna.obs["cell_type"].value_counts().to_string().replace("\n", "\n    "), flush=True)

    # ── ATAC peak→gene (gencode proximity) ──
    genes_df = load_gencode_genes(GTF)
    print(f"[gencode] genes: {genes_df.shape[0]}", flush=True)
    atac_gene = aggregate_peaks_to_genes(atac, genes_df, rna.var_names)
    atac_gene.obs["dataset"] = "GSE194122_bmmc"
    atac_gene.obs["lineage"] = pd.Categorical(
        pd.Index(atac_gene.obs_names).map(pd.Series(rna.obs["lineage"].astype(str).values,
                                                    index=rna.obs_names)))
    atac_gene.obs["leiden"] = pd.Categorical(
        pd.Index(atac_gene.obs_names).map(pd.Series(rna.obs["leiden"].astype(str).values,
                                                    index=rna.obs_names)))
    sc.pp.normalize_total(atac_gene, target_sum=1e4)
    sc.pp.log1p(atac_gene)

    # cross-env 호환: uns None 값 제거
    def _portable(a):
        a.uns.pop("log1p", None)
        for k in list(a.uns):
            if a.uns[k] is None:
                del a.uns[k]
    _portable(rna); _portable(atac_gene)

    rna.write_h5ad(OUT / "rna_spliced_unspliced.h5ad")
    atac_gene.write_h5ad(OUT / "atac_gene.h5ad")
    print(f"[RNA] → rna_spliced_unspliced.h5ad {rna.shape}", flush=True)
    print(f"[ATAC] → atac_gene.h5ad {atac_gene.shape}", flush=True)

    shared_g = sorted(set(rna.var_names) & set(atac_gene.var_names))
    print(f"[VERIFY] RNA↔ATAC obs identical: "
          f"{np.array_equal(rna.obs_names.to_numpy(), atac_gene.obs_names.to_numpy())}", flush=True)
    print(f"[VERIFY] RNA∩ATAC(gene) common genes: {len(shared_g)}", flush=True)
    sp_nnz = rna.layers['spliced'].nnz / np.prod(rna.layers['spliced'].shape)
    un_nnz = rna.layers['unspliced'].nnz / np.prod(rna.layers['unspliced'].shape)
    print(f"[VERIFY] spliced nnz={sp_nnz:.4f}, unspliced nnz={un_nnz:.4f} (both must be >0)", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
