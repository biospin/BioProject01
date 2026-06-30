#!/usr/bin/env python3
"""P3 within-lineage lag 분포 — MultiVelo switch time gene별 lineage 할당 후 집계.

⚠️ MultiVelo switch time은 전역 fit(gene당 1값). 진짜 within-lineage fit은 추후.
   여기서는 gene을 '주요 발현 lineage'로 귀속해 lineage별 lag 분포를 요약한다.
   귀속 기준: P1 lineage 라벨 세포에서 해당 gene spliced expression이 상위 50%를 차지하는 lineage.

실행: conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p3_lineage_lag.py
출력: results/lineage_lag.md, results/lineage_lag.csv
"""
from __future__ import annotations
import sys
import numpy as np
import pandas as pd
import scanpy as sc
import p1_config as p1
import p2_config as cfg


def assign_gene_lineage(rna: "sc.AnnData", genes: list[str]) -> pd.Series:
    """각 gene의 주요 발현 lineage를 할당: lineage별 평균 spliced expr의 argmax."""
    if "lineage" not in rna.obs.columns:
        return pd.Series("unknown", index=genes)
    lins = sorted(rna.obs["lineage"].dropna().unique())
    layer = "spliced" if "spliced" in rna.layers else None
    mat = rna[:, genes].layers[layer] if layer else rna[:, genes].X
    df = pd.DataFrame(
        mat.toarray() if hasattr(mat, "toarray") else np.asarray(mat),
        index=rna.obs_names, columns=genes
    )
    df["lineage"] = rna.obs["lineage"].values
    means = df.groupby("lineage")[genes].mean()
    return means.idxmax(axis=0)   # gene → dominant lineage


def main():
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    L = ["# P3 — Within-lineage lag 분포 (MultiVelo, 전역 fit 기반)", ""]

    mv_csv = cfg.RESULTS / "multivelo_genes.csv"
    if not mv_csv.exists():
        print("multivelo_genes.csv 없음 — 종료"); return 1

    mv = pd.read_csv(mv_csv, index_col=0)
    lag = (mv["fit_t_sw2"] - mv["fit_t_sw1"]).rename("lag")
    lag = lag.dropna()

    rna = sc.read_h5ad(p1.OUT_RNA)
    fit_genes = [g for g in lag.index if g in rna.var_names]
    L.append(f"- fit gene {len(lag)}, RNA에서 찾은 gene {len(fit_genes)}")

    gene_lin = assign_gene_lineage(rna, fit_genes)
    result_rows = []

    L += ["", "## Lineage별 lag 요약 (전역 fit, gene dominant-expression 귀속)", ""]
    L.append("| lineage | n_gene | median_lag | mean_lag | IQR_low | IQR_high | lag>0% |")
    L.append("|---|---|---|---|---|---|---|")

    for lin in sorted(gene_lin.unique()):
        g_lin = gene_lin[gene_lin == lin].index
        lags_lin = lag.loc[[g for g in g_lin if g in lag.index]]
        if len(lags_lin) == 0:
            continue
        med = lags_lin.median()
        mn = lags_lin.mean()
        q25, q75 = lags_lin.quantile(.25), lags_lin.quantile(.75)
        pos_frac = float((lags_lin > 0).mean())
        is_rare = lin in p1.RARE_LINEAGES
        rare_tag = " ⚠️rare" if is_rare else ""
        L.append(f"| {lin}{rare_tag} | {len(lags_lin)} | {med:.2f} | {mn:.2f} | {q25:.2f} | {q75:.2f} | {pos_frac:.1%} |")
        result_rows.append(dict(lineage=lin, n_gene=len(lags_lin), median_lag=med,
                                mean_lag=mn, iqr_low=q25, iqr_high=q75, pos_frac=pos_frac,
                                is_rare=is_rare))

    L += ["",
          "> ⚠️ switch time은 전역 fit — lineage별 귀속은 dominant expression 기준이며 per-lineage fit이 아님.",
          "> rare lineage(MK/Baso·Eo·Mast/pDC)는 uncertainty 별도 보고 필요(DESIGN §4, CLAUDE.md #2).",
          ""]

    # per-lineage switch time 분포도 요약 (scvelo_floor fit_t_ 비교)
    fl_csv = cfg.RESULTS / "rna_only_dynamical_genes.csv"
    if fl_csv.exists():
        fl = pd.read_csv(fl_csv, index_col=0)
        fl_genes = [g for g in fl.index if g in rna.var_names]
        fl_lin = assign_gene_lineage(rna, fl_genes)
        L += ["## scVelo floor fit_t_ lineage별 요약", ""]
        L.append("| lineage | n_gene | median_fit_t |")
        L.append("|---|---|---|")
        for lin in sorted(fl_lin.unique()):
            g_lin = fl_lin[fl_lin == lin].index
            ts = fl.loc[[g for g in g_lin if g in fl.index], "fit_t_"].dropna() if "fit_t_" in fl else pd.Series([], dtype=float)
            if len(ts) == 0:
                continue
            L.append(f"| {lin} | {len(ts)} | {ts.median():.2f} |")
        L.append("")

    out_md = cfg.RESULTS / "lineage_lag.md"
    out_md.write_text("\n".join(L), encoding="utf-8")
    out_csv = cfg.RESULTS / "lineage_lag.csv"
    pd.DataFrame(result_rows).to_csv(out_csv, index=False)
    print("\n".join(L))
    print(f"\n✓ → {out_md} + {out_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
