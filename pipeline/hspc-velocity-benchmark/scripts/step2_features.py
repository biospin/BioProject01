#!/usr/bin/env python3
"""STEP2 (EXPLORATORY) — GSE70677 HSPC baseline chromatin feature 어셈블.

설계 정본: STEP2-CHROMATIN-EXPLAINS-KINETICS-DESIGN.md §3.
GSE70677 Human CD34+ HSPC histone ChIP-seq (SICER island BED, hg19) → gene별 baseline
promoter/enhancer 활성 feature. 타깃(GSE209878 α/lag)과 gene-SYMBOL 축에서 조인(liftOver 회피).

가용 마크(feasibility gate 2026-07-13 실측):
  - H3K4me3  GSM1816326  promoter 활성      (BED4: chrom,start,end,island_score)
  - H3K4me1  GSM1816327  enhancer           (BED4)
  - H3K27ac  GSM1816328  active prom/enh    (BED4)
  - CpG island (UCSC hg19 cpgIslandExt)     promoter CpG class
BLOCKED (설계 §2b 중 미가용):
  - HSPC input BED (GSM1816325 = supp NONE) → island은 이미 SICER FDR0.01로 input 대비 유의 → 별도 input 정규화 불가(한계)
  - CAGE (GSM1816314 = supp NONE, raw SRA만) → CAGE_init/CAGE_shape feature BLOCKED
  - GSE70677 RNA = Affymetrix HG-U133 CEL (microarray), cms-r에 affy/hgu133plus2.db 부재 → baseline_expr 독립 소스 BLOCKED
    → baseline_expr는 GSE209878 day0 HSC/MPP 발현으로 대체(same-cell confound; 정직 라벨).

feature (gene-level):
  me3_prom, ac_prom          : promoter TSS±2kb island_score 합 (log1p)
  me3_breadth                : promoter 겹침 island bp (breadth; me3 broad-domain 신호)
  ac_enh, me1_enh            : distal enhancer (2kb<|d|≤50kb) island_score 합 (log1p)
  n_links                    : distal enhancer island 개수(union me1∪ac) = peak-to-gene linkage
  cpg_prom                   : promoter TSS±2kb CpG island 겹침 여부(0/1)
  baseline_expr              : GSE209878 day0 HSC/MPP 평균 log1p 발현 (confound 공변량)
  gene_length_log10          : log10 gene body 길이 (confound 공변량)
  chrom                      : 염색체 (grouped-CV hold-out 그룹)

실행: conda run -n scv-preprocess python scripts/step2_features.py
출력: results/step2/features_hspc.csv  (parquet 엔진 부재 → CSV; 내용 동일)
"""
import sys, gzip, re
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
OUT = RES / "step2"
DATA = HERE / "data/gse70677"
GTF = HERE / "data/gencode.v19.genes.gtf.gz"    # hg19 (BED와 동일 assembly)
RNA = HERE / "data/processed/rna_spliced_unspliced.h5ad"
BEDS = {"me3": DATA / "H3K4me3.bed.gz", "me1": DATA / "H3K4me1.bed.gz", "ac": DATA / "H3K27ac.bed.gz"}
CPG = DATA / "cpgIslandExt_hg19.txt.gz"
METHOD_CSVS = ["multivelo_genes.csv", "moflow_genes.csv", "multivelovae_genes.csv",
               "crakvelo_genes.csv", "rna_only_dynamical_genes.csv"]
PROM_WIN = 2000
ENH_WIN = 50000


def gene_universe():
    genes = set()
    for c in METHOD_CSVS:
        p = RES / c
        if p.exists():
            genes |= set(pd.read_csv(p, index_col=0).index.astype(str))
    return genes


def load_tss(want):
    """gencode v19 gene → (chrom, tss, gene_length). canonical=첫 등장."""
    rec = {}
    with gzip.open(GTF, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.split("\t")
            if f[2] != "gene":
                continue
            m = re.search(r'gene_name "([^"]+)"', f[8])
            if not m:
                continue
            name = m.group(1)
            if name not in want or name in rec:
                continue
            chrom, start, end, strand = f[0], int(f[3]), int(f[4]), f[6]
            tss = start if strand == "+" else end
            rec[name] = (chrom, tss, end - start)
    return rec


def load_bed(path):
    """SICER island BED4 → chrom→sorted DataFrame(mid, start, end, score)."""
    df = pd.read_csv(path, sep="\t", header=None,
                     names=["chrom", "start", "end", "score"],
                     dtype={"chrom": str})
    df["mid"] = (df["start"] + df["end"]) // 2
    return {c: g.sort_values("mid").reset_index(drop=True) for c, g in df.groupby("chrom")}


def load_cpg(path):
    df = pd.read_csv(path, sep="\t", header=None, usecols=[1, 2, 3],
                     names=["chrom", "start", "end"], dtype={"chrom": str})
    return {c: g.sort_values("start").reset_index(drop=True) for c, g in df.groupby("chrom")}


def prom_signal(bychrom, chrom, tss):
    """promoter TSS±2kb 겹치는 island score 합 + 겹침 bp(breadth)."""
    sub = bychrom.get(chrom)
    if sub is None:
        return 0.0, 0.0
    lo, hi = tss - PROM_WIN, tss + PROM_WIN
    ov = sub[(sub["end"] > lo) & (sub["start"] < hi)]
    if len(ov) == 0:
        return 0.0, 0.0
    score = float(ov["score"].sum())
    breadth = float((np.minimum(ov["end"], hi) - np.maximum(ov["start"], lo)).clip(lower=0).sum())
    return score, breadth


def enh_signal(bychrom, chrom, tss):
    """distal enhancer (2kb<|mid-tss|≤50kb) island score 합 + 개수."""
    sub = bychrom.get(chrom)
    if sub is None:
        return 0.0, 0
    d = np.abs(sub["mid"].values - tss)
    sel = (d > PROM_WIN) & (d <= ENH_WIN)
    return float(sub["score"].values[sel].sum()), int(sel.sum())


def cpg_promoter(bychrom, chrom, tss):
    sub = bychrom.get(chrom)
    if sub is None:
        return 0
    lo, hi = tss - PROM_WIN, tss + PROM_WIN
    return int(((sub["end"] > lo) & (sub["start"] < hi)).any())


def baseline_expr(want):
    """GSE209878 day0 HSC/MPP 평균 log1p CP10k 발현 (confound 공변량)."""
    import anndata as ad, scipy.sparse as sp
    a = ad.read_h5ad(RNA, backed="r")
    mask = ((a.obs["timepoint"].astype(str) == "day0") &
            (a.obs["lineage"].astype(str) == "HSC/MPP")).values
    n = int(mask.sum())
    sub = a[mask].to_memory()
    X = sub.layers["spliced"] if "spliced" in sub.layers else sub.X
    X = X.tocsr() if sp.issparse(X) else sp.csr_matrix(X)
    depth = np.asarray(X.sum(1)).ravel(); depth[depth == 0] = 1.0
    Xn = X.multiply((1e4 / depth)[:, None]).tocsc()
    genes = list(sub.var_names.astype(str))
    idx = {g: i for i, g in enumerate(genes)}
    out = {}
    for g in want:
        j = idx.get(g)
        if j is None:
            continue
        col = Xn[:, j].toarray().ravel()
        out[g] = float(np.log1p(col).mean())
    return out, n


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    want = gene_universe()
    print(f"[feat] velocity gene universe {len(want)}", flush=True)
    tss = load_tss(want)
    print(f"[feat] gencode v19 TSS 매칭 {len(tss)}/{len(want)}", flush=True)
    beds = {k: load_bed(p) for k, p in BEDS.items()}
    for k in beds:
        print(f"[feat] {k} islands loaded", flush=True)
    cpg = load_cpg(CPG)
    expr, n_base = baseline_expr(want)
    print(f"[feat] baseline_expr (day0 HSC/MPP {n_base} cell) {len(expr)} gene", flush=True)

    rows = []
    for g, (chrom, t, glen) in tss.items():
        me3_p, me3_b = prom_signal(beds["me3"], chrom, t)
        ac_p, _ = prom_signal(beds["ac"], chrom, t)
        ac_e, ac_n = enh_signal(beds["ac"], chrom, t)
        me1_e, me1_n = enh_signal(beds["me1"], chrom, t)
        rows.append(dict(
            gene=g, chrom=chrom,
            me3_prom=np.log1p(me3_p), ac_prom=np.log1p(ac_p),
            me3_breadth=np.log1p(me3_b),
            ac_enh=np.log1p(ac_e), me1_enh=np.log1p(me1_e),
            n_links=int(max(ac_n, me1_n)),
            cpg_prom=cpg_promoter(cpg, chrom, t),
            baseline_expr=expr.get(g, np.nan),
            gene_length_log10=np.log10(max(glen, 1)),
        ))
    feat = pd.DataFrame(rows).set_index("gene").sort_index()
    # baseline_expr 결측(GSE209878 축에 없는 gene)만 drop — chromatin 0은 진짜 부재 신호로 보존
    n0 = len(feat)
    feat = feat[feat["baseline_expr"].notna()]
    print(f"[feat] baseline_expr 결측 drop {n0}→{len(feat)}", flush=True)
    feat.to_csv(OUT / "features_hspc.csv")
    print(f"[feat] ✓ features {feat.shape} → step2/features_hspc.csv", flush=True)
    print(feat.describe().T[["mean", "50%", "max"]].to_string(), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
