#!/usr/bin/env python3
"""GSE205117 (mouse gastrulation E7.5–8.75, 10x Multiome) → processed h5ad (build+finalize).

5번째 cross-dataset 재현(사전등록 manuscript/PREREGISTRATION_gse205117.md). HSPC/human_brain/E18/BMMC/
macrophage와 **동일 스키마**(rna_spliced_unspliced.h5ad + atac_gene.h5ad)로 마감한다.

입력:
  - GEX: 우리 STARsolo Velocyto 4런(rep1) — /home/kkkim/data/gse205117_fullB/gex_solo/<SRR>/<SRR>_Solo.out/
         {Velocyto/raw/{spliced,unspliced}.mtx + features.tsv + barcodes.tsv, Gene/filtered/barcodes.tsv(=세포)}.
         mtx orientation = genes×cells (transpose). var symbol = features col1.
  - ATAC: GEO 제공 fragments.tsv.gz 4런 — data 밖 /home/kkkim/data/gse205117_fullB/atac_frag/.
          바코드는 GEX space(strip '-1' → GEX 16bp, 실측 교집합 97.3% — probe_barcode_join). revcomp/ARC 불필요.
  - peak/frag→gene: **우리 자체 집계**(gencode vM25 gene body ±10kb, build_human_brain 패턴). provider gene-activity 미사용.

산출: data/processed_gse205117/{rna_spliced_unspliced.h5ad, atac_gene.h5ad}

스테이지(무거운 ATAC 집계는 detached):
  conda run -n scv-preprocess python build_gse205117.py rna       # 빠름 → rna raw(all filtered cells)
  conda run -n scv-preprocess python build_gse205117.py atac      # 무거움(fragments 스트리밍) → atac_gene raw
  conda run -n scv-preprocess python build_gse205117.py finalize  # QC/normalize/graph/lineage → 최종 스키마
"""
from __future__ import annotations
import gzip
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.io as sio
import scanpy as sc
import anndata as ad

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                   # pipeline/hspc-velocity-benchmark
GEX_BASE = Path("/home/kkkim/data/gse205117_fullB/gex_solo")
FRAG_BASE = Path("/home/kkkim/data/gse205117_fullB/atac_frag")
GTF = ROOT / "data" / "ref" / "mm10" / "gencode.vM25.annotation.gtf"
OUT = ROOT / "data" / "processed_gse205117"
OUT.mkdir(parents=True, exist_ok=True)
RAW_RNA = OUT / "_raw_rna.h5ad"          # stage rna 산출(pre-finalize)
RAW_ATAC = OUT / "_raw_atac_gene.h5ad"   # stage atac 산출(pre-finalize)

# 4 rep1 시점: GEX SRR ↔ ATAC fragments 파일
SAMPLES = {
    "E7.5":  dict(srr="SRR19450575", frag="GSM6205427_E7.5_rep1_ATAC_fragments.tsv.gz"),
    "E8.0":  dict(srr="SRR19450564", frag="GSM6205430_E8.0_rep1_ATAC_fragments.tsv.gz"),
    "E8.5":  dict(srr="SRR19450560", frag="GSM6205434_E8.5_rep1_ATAC_fragments.tsv.gz"),
    "E8.75": dict(srr="SRR19450574", frag="GSM6205436_E8.75_rep1_ATAC_fragments.tsv.gz"),
}

# HSPC와 동일 하이퍼파라미터(공정 비교)
N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, SEED = 2000, 30, 30, 1.0, 0
PEAK_DIST = 10000                        # gene body ±10kb (multivelo aggregate_peaks_10x 기본과 정합)
QC = dict(min_genes=500, max_genes=9000, max_pct_mito=15.0)

# mouse gastrulation lineage marker (mouse symbol case; concordance엔 비-load-bearing)
LINEAGE_MARKERS = {
    "Epiblast":        ["Pou5f1", "Nanog", "Utf1", "Slc7a3", "Dppa5a"],
    "PrimitiveStreak": ["T", "Mixl1", "Fgf8", "Wnt3", "Nkx1-2"],
    "Mesoderm":        ["Mesp1", "Tbx6", "Hand1", "Gata4", "Snai1", "Lefty2"],
    "Endoderm":        ["Foxa2", "Sox17", "Cer1", "Foxa1", "Trh"],
    "Ectoderm":        ["Sox2", "Pax6", "Sox1", "Nes", "Six3"],
    "Blood":           ["Gata1", "Klf1", "Hba-a1", "Runx1", "Hbb-bh1", "Gypa"],
    "Cardiac":         ["Nkx2-5", "Myl7", "Tnnt2", "Hand2"],
}
RARE_LINEAGES = {"Cardiac", "Blood"}


# ─────────────────────────── STAGE rna ───────────────────────────
def load_gex_timepoint(tp: str) -> ad.AnnData:
    """STARsolo Velocyto/**filtered**(spliced/unspliced, genes×cells) → cells×genes AnnData.

    ⚠️ STARsolo whitelist=None 함정(2026-07-14 실측): Velocyto의 **barcodes.tsv 문자열이 mislabel**됨
       (Velocyto/raw·filtered 바코드가 Gene 바코드와 다른 space; string match하면 real cell에 count≈1 garbage).
       그러나 **Velocyto/filtered matrix column 순서 = Gene/filtered cell 순서**(positional).
       실측: posSpearman(Gene counts, Velocyto spliced) = 0.996–0.997, features 동일(4시점 전부).
       → spliced/unspliced는 Velocyto/**filtered**에서 읽되, cell 바코드는 **Gene/filtered/barcodes.tsv를
         positional**로 부여한다(Velocyto barcodes.tsv 무시). Gene/filtered 바코드 = ATAC 매칭된 real cell."""
    srr = SAMPLES[tp]["srr"]
    base = GEX_BASE / srr / f"{srr}_Solo.out"
    vfilt = base / "Velocyto" / "filtered"
    gfilt = base / "Gene" / "filtered"
    # features: Velocyto/filtered와 Gene/filtered 동일(실측 검증). col1 = symbol.
    symbols = pd.read_csv(vfilt / "features.tsv", sep="\t", header=None)[1].astype(str).to_numpy()
    g_symbols = pd.read_csv(gfilt / "features.tsv", sep="\t", header=None)[1].astype(str).to_numpy()
    assert np.array_equal(symbols, g_symbols), f"{tp}: Velocyto/filtered features != Gene/filtered"
    # cell 바코드 = Gene/filtered (real cell, ATAC 매칭). Velocyto matrix col과 positional 정합.
    filt_bc = pd.read_csv(gfilt / "barcodes.tsv", header=None)[0].astype(str).to_numpy()
    n_cells = len(filt_bc)
    print(f"  [{tp}/{srr}] features={len(symbols)} filtered_cells={n_cells} (Velocyto/filtered positional)",
          flush=True)

    def read_layer(name):
        M = sio.mmread(str(vfilt / f"{name}.mtx")).tocsr()   # genes×cells (filtered)
        assert M.shape[0] == len(symbols) and M.shape[1] == n_cells, \
            f"{tp} {name} dims {M.shape} != ({len(symbols)},{n_cells}) — Velocyto/filtered positional 불일치"
        return M.T.tocsr()                                   # cells×genes (positional, Gene/filtered 순서)

    spl = read_layer("spliced")
    uns = read_layer("unspliced")
    # positional sanity: Gene/filtered total count vs Velocyto spliced total의 cell별 상관(≥0.9 기대)
    from scipy.stats import spearmanr
    G = sio.mmread(str(gfilt / "matrix.mtx")).tocsc()
    r, _ = spearmanr(np.asarray(G.sum(0)).ravel(), np.asarray(spl.sum(1)).ravel())
    assert r >= 0.9, f"{tp}: positional Spearman(Gene,Velocyto spliced)={r:.3f} < 0.9 — 정합 실패, 중단"
    print(f"    [{tp}] positional Spearman(Gene,Velocyto spliced)={r:.3f} ✓", flush=True)
    obs_names = np.array([f"{tp}_{b}" for b in filt_bc])     # 시점 prefix(바코드 충돌 방지)
    a = ad.AnnData(X=(spl + uns).tocsr(),
                   obs=pd.DataFrame({"timepoint": tp, "gex_barcode": filt_bc}, index=obs_names),
                   var=pd.DataFrame(index=symbols))
    a.layers["spliced"] = spl
    a.layers["unspliced"] = uns
    a.var_names_make_unique()
    return a


def stage_rna():
    print("[stage rna] STARsolo Velocyto 4런 병합", flush=True)
    parts = [load_gex_timepoint(tp) for tp in SAMPLES]
    # 4런은 동일 STAR index → 동일 gene 축. concat outer(안전).
    rna = ad.concat(parts, axis=0, join="outer", merge="same")
    rna.obs["dataset"] = "gse205117"
    rna.write_h5ad(RAW_RNA)
    for lyr in ("spliced", "unspliced"):
        M = rna.layers[lyr]
        nnz = M.nnz / np.prod(M.shape)
        print(f"  {lyr} nnz={nnz:.4f}", flush=True)
    print(f"[stage rna] → {RAW_RNA.name} {rna.shape} "
          f"(cells/tp: {rna.obs['timepoint'].value_counts().to_dict()})", flush=True)


# ─────────────────────────── STAGE atac ───────────────────────────
def load_gencode_genes(path: Path) -> pd.DataFrame:
    rows = []
    pat = re.compile(r'gene_name "([^"]+)"')
    with open(path, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9 or f[2] != "gene":
                continue
            m = pat.search(f[8])
            if not m:
                continue
            rows.append((m.group(1), f[0], int(f[3]), int(f[4])))
    df = pd.DataFrame(rows, columns=["symbol", "chrom", "start", "end"])
    # 같은 symbol 여러 좌표 → 최소 start~최대 end(가장 관대한 gene body)
    df = df.groupby(["symbol", "chrom"], as_index=False).agg(start=("start", "min"), end=("end", "max"))
    df = df.drop_duplicates("symbol", keep="first").reset_index(drop=True)   # symbol 유일화
    return df


def _build_chrom_index(gsel: pd.DataFrame):
    """chrom → (lo_sorted, hi_sorted, gidx_sorted): lo=start-PEAK_DIST 정렬."""
    lo = np.maximum(gsel["start"].to_numpy() - PEAK_DIST, 0)
    hi = gsel["end"].to_numpy() + PEAK_DIST
    chrom = gsel["chrom"].astype(str).to_numpy()
    idx = {}
    for c in np.unique(chrom):
        sel = np.where(chrom == c)[0]
        order = sel[np.argsort(lo[sel])]
        idx[c] = (lo[order], hi[order], order.astype(np.int32))
    return idx


def aggregate_fragments_to_genes(frag_path: Path, kept_bc: np.ndarray, gsel: pd.DataFrame,
                                 chrom_idx: dict, tp: str, K_NEIGHBORS: int = 8) -> sp.csr_matrix:
    """fragments.tsv.gz 스트리밍 → cell×gene 카운트(gene body ±PEAK_DIST 겹침, multi-assign 근사).

    kept_bc = 이 시점 GEX filtered 16bp 바코드(순서 = 최종 cell 축). fragment 바코드는 strip '-1'."""
    n_cells, n_genes = len(kept_bc), gsel.shape[0]
    bc2idx = pd.Series(np.arange(n_cells, dtype=np.int32), index=pd.Index(kept_bc))
    dense = np.zeros((n_cells, n_genes), dtype=np.float32)
    total, kept_frag, assigned = 0, 0, 0
    reader = pd.read_csv(frag_path, sep="\t", header=None, comment="#",
                         names=["chrom", "start", "end", "bc", "cnt"],
                         usecols=["chrom", "start", "end", "bc"],
                         dtype={"chrom": str, "start": np.int64, "end": np.int64, "bc": str},
                         chunksize=8_000_000)
    for ci, chunk in enumerate(reader):
        total += len(chunk)
        bc = chunk["bc"].str.slice(0, -2)                     # strip '-1'
        cell = bc2idx.reindex(bc.to_numpy()).to_numpy()       # NaN = not a kept cell
        m = ~np.isnan(cell)
        if not m.any():
            continue
        cell = cell[m].astype(np.int32)
        mid = ((chunk["start"].to_numpy()[m] + chunk["end"].to_numpy()[m]) // 2)
        ch = chunk["chrom"].to_numpy()[m]
        kept_frag += len(cell)
        for c in np.unique(ch):
            if c not in chrom_idx:
                continue
            sub = ch == c
            X = mid[sub]; C = cell[sub]
            lo_s, hi_s, gid_s = chrom_idx[c]
            pos = np.searchsorted(lo_s, X, side="right")      # genes with lo<=X are [:pos]
            for k in range(K_NEIGHBORS):
                cand = pos - 1 - k
                valid = cand >= 0
                if not valid.any():
                    break
                cc = np.where(valid)[0]
                cand_v = cand[cc]
                contained = hi_s[cand_v] >= X[cc]              # lo<=X 이미 보장, hi>=X 체크
                if contained.any():
                    rows = C[cc][contained]
                    cols = gid_s[cand_v[contained]]
                    np.add.at(dense, (rows, cols), 1.0)
                    assigned += int(contained.sum())
        if (ci + 1) % 5 == 0:
            print(f"    [{tp}] {total/1e6:.0f}M frags read, {kept_frag/1e6:.1f}M in-cell, "
                  f"{assigned/1e6:.1f}M gene-assigns", flush=True)
    print(f"  [{tp}] DONE frags={total/1e6:.0f}M in-cell={kept_frag/1e6:.1f}M "
          f"assigns={assigned/1e6:.1f}M", flush=True)
    return sp.csr_matrix(dense)


def stage_atac():
    print("[stage atac] gencode vM25 gene-window 집계", flush=True)
    rna = sc.read_h5ad(RAW_RNA)
    rna_symbols = set(rna.var_names)
    genes_df = load_gencode_genes(GTF)
    gsel = genes_df[genes_df["symbol"].isin(rna_symbols)].reset_index(drop=True)
    print(f"  gencode genes: {genes_df.shape[0]}, ∩RNA symbols: {gsel.shape[0]}", flush=True)
    chrom_idx = _build_chrom_index(gsel)
    gene_symbols = gsel["symbol"].to_numpy()

    parts = []
    for tp, s in SAMPLES.items():
        frag_path = FRAG_BASE / s["frag"]
        assert frag_path.exists(), f"{tp} fragments 없음: {frag_path}"
        # 이 시점 GEX filtered 바코드(cell 축) — RNA obs에서 추출(순서 보존)
        sub = rna.obs[rna.obs["timepoint"] == tp]
        kept_bc = sub["gex_barcode"].astype(str).to_numpy()
        obs_names = sub.index.to_numpy()                      # 이미 "{tp}_{bc}"
        print(f"  [{tp}] fragments={frag_path.name} cells={len(kept_bc)}", flush=True)
        M = aggregate_fragments_to_genes(frag_path, kept_bc, gsel, chrom_idx, tp)
        a = ad.AnnData(X=M, obs=pd.DataFrame({"timepoint": tp}, index=obs_names),
                       var=pd.DataFrame(index=gene_symbols))
        parts.append(a)
    atac = ad.concat(parts, axis=0, join="outer", merge="same")
    atac.obs["dataset"] = "gse205117"
    atac.write_h5ad(RAW_ATAC)
    nnz = atac.X.nnz / np.prod(atac.X.shape)
    print(f"[stage atac] → {RAW_ATAC.name} {atac.shape} nnz={nnz:.4f}", flush=True)


# ─────────────────────────── STAGE finalize ───────────────────────────
def annotate_lineage(rna):
    used = {}
    for lin, genes in LINEAGE_MARKERS.items():
        present = [g for g in genes if g in rna.var_names]
        if present:
            sc.tl.score_genes(rna, present, score_name=f"sig_{lin}", ctrl_size=50, random_state=SEED)
            used[lin] = present
    if not used:
        print("  ⚠ marker 없음 → lineage=leiden"); rna.obs["lineage"] = rna.obs["leiden"]; return rna
    cols = [f"sig_{lin}" for lin in used]
    means = rna.obs.groupby("leiden", observed=True)[cols].mean()
    cl2lin = means.idxmax(axis=1).str.replace("sig_", "", regex=False)
    rna.obs["lineage"] = rna.obs["leiden"].map(cl2lin).astype("category")
    rna.obs["lineage_rare"] = rna.obs["lineage"].isin(RARE_LINEAGES)
    print("  lineage 분포:\n    " + rna.obs["lineage"].value_counts().to_string().replace("\n", "\n    "))
    return rna


def stage_finalize():
    print("[stage finalize] QC → normalize → HVG → graph → lineage", flush=True)
    rna = sc.read_h5ad(RAW_RNA)
    atac = sc.read_h5ad(RAW_ATAC)
    print(f"  raw RNA {rna.shape} | raw ATAC {atac.shape}", flush=True)

    # ── QC (mouse mito = mt-) ──
    rna.var["mito"] = rna.var_names.str.lower().str.startswith("mt-")
    sc.pp.calculate_qc_metrics(rna, inplace=True, percent_top=None)
    if rna.var["mito"].any():
        rna.obs["pct_mito"] = (np.asarray(rna[:, rna.var["mito"]].X.sum(1)).ravel()
                               / np.asarray(rna.X.sum(1)).ravel().clip(min=1) * 100)
    else:
        rna.obs["pct_mito"] = 0.0
    n0 = rna.n_obs
    sc.pp.filter_cells(rna, min_genes=QC["min_genes"])
    rna = rna[(rna.obs["n_genes_by_counts"] <= QC["max_genes"])
              & (rna.obs["pct_mito"] <= QC["max_pct_mito"])].copy()
    print(f"[QC] {n0} → {rna.n_obs} cells (mito≤{QC['max_pct_mito']}, genes {QC['min_genes']}~{QC['max_genes']})",
          flush=True)

    # ── RNA∩ATAC cell 정합 ──
    common = [c for c in rna.obs_names if c in set(atac.obs_names)]
    print(f"[align] RNA∩ATAC cells: {len(common)} (RNA {rna.n_obs}, ATAC {atac.n_obs})", flush=True)
    assert len(common) >= 500, f"교집합 {len(common)} < 500"
    rna = rna[common].copy(); atac = atac[common].copy()

    # ── normalize + HVG + graph (HSPC 순서 복제) ──
    rna.layers["counts"] = rna.X.copy()
    sc.pp.normalize_total(rna, target_sum=1e4)
    sc.pp.log1p(rna)
    sc.pp.highly_variable_genes(rna, n_top_genes=N_HVG)
    sc.pp.pca(rna, n_comps=N_PCS, random_state=SEED)
    sc.pp.neighbors(rna, n_neighbors=N_NEIGHBORS, random_state=SEED)
    sc.tl.leiden(rna, resolution=LEIDEN_RES, random_state=SEED, key_added="leiden")
    print(f"[graph] leiden={rna.obs['leiden'].nunique()} HVG={int(rna.var['highly_variable'].sum())}",
          flush=True)
    rna = annotate_lineage(rna)

    # ── ATAC gene-level 정규화 ──
    atac.obs["lineage"] = pd.Categorical(
        pd.Index(atac.obs_names).map(pd.Series(rna.obs["lineage"].astype(str).values, index=rna.obs_names)))
    atac.obs["leiden"] = pd.Categorical(
        pd.Index(atac.obs_names).map(pd.Series(rna.obs["leiden"].astype(str).values, index=rna.obs_names)))
    atac.layers["counts"] = atac.X.copy()
    sc.pp.normalize_total(atac, target_sum=1e4)
    sc.pp.log1p(atac)

    def _portable(a):
        a.uns.pop("log1p", None)
        for k in list(a.uns):
            if a.uns[k] is None:
                del a.uns[k]
    _portable(rna); _portable(atac)

    rna.write_h5ad(OUT / "rna_spliced_unspliced.h5ad")
    atac.write_h5ad(OUT / "atac_gene.h5ad")
    shared_g = sorted(set(rna.var_names) & set(atac.var_names))
    print(f"[RNA]  → rna_spliced_unspliced.h5ad {rna.shape}", flush=True)
    print(f"[ATAC] → atac_gene.h5ad {atac.shape}", flush=True)
    print(f"[VERIFY] obs identical: "
          f"{np.array_equal(rna.obs_names.to_numpy(), atac.obs_names.to_numpy())}", flush=True)
    print(f"[VERIFY] RNA∩ATAC genes: {len(shared_g)}", flush=True)
    for lyr in ("spliced", "unspliced"):
        M = rna.layers[lyr]; nnz = M.nnz / np.prod(M.shape)
        print(f"[VERIFY] {lyr} nnz={nnz:.4f} (>0 필수)", flush=True)
    print("DONE", flush=True)


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else ""
    if stage == "rna":
        stage_rna()
    elif stage == "atac":
        stage_atac()
    elif stage == "finalize":
        stage_finalize()
    else:
        print("usage: build_gse205117.py {rna|atac|finalize}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
