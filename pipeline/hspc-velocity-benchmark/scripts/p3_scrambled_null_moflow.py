#!/usr/bin/env python3
"""P3 — MoFlow scrambled-chromatin 음성대조 검정 (Track C / novelty_strategy §4.2).

원본 MoFlow(moflow_genes.csv + moflow.h5ad) vs within-lineage ATAC 셔플 재fit
(moflow_scrambled_genes.csv + moflow_scrambled.h5ad) 을 scrambled_null.md 와 **동일 통계**로 비교:
  (1) fit-quality/chromatin-channel delta  [핵심 discriminator]  — loss, |alpha_c|, |velo_c|
  (2) lag 분포 동일성 — Mann-Whitney, KS + chromatin-leading(cs_lag>0) 비율
  (3) per-gene lag Spearman ρ (signed & |lag|) + Wilcoxon paired  [MoFlow lag 신뢰도 caveat 동반]

출력: results/scrambled_null_moflow.md 는 사람이 작성(이 스크립트는 숫자만 stdout 으로 방출).
실행: conda run --no-capture-output -n velo-torch python scripts/p3_scrambled_null_moflow.py
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scanpy as sc
from scipy import stats
import p2_config as cfg


def _dense(x):
    return x.toarray() if sp.issparse(x) else np.asarray(x)


def per_gene_fitquality(h5ad_path):
    """moflow(.scrambled).h5ad 에서 per-gene chromatin 채널 fit-quality 요약."""
    a = sc.read_h5ad(h5ad_path)
    out = pd.DataFrame(index=a.var_names)
    if "loss" in a.var.columns:
        out["loss"] = a.var["loss"].values
    ac = _dense(a.layers["alpha_c"])
    vc = _dense(a.layers["velo_c"])
    out["alpha_c_mean_abs"] = np.nanmean(np.abs(ac), axis=0)
    out["velo_c_mean_abs"] = np.nanmean(np.abs(vc), axis=0)
    return out


def main():
    R = cfg.RESULTS
    V = cfg.OUT_VELO

    orig = pd.read_csv(R / "moflow_genes.csv", index_col=0)
    scr = pd.read_csv(R / "moflow_scrambled_genes.csv", index_col=0)
    print(f"orig genes {orig.shape}, scrambled genes {scr.shape}")

    # ── (1) fit-quality / chromatin-channel delta  [discriminator] ────────────
    fq_o = per_gene_fitquality(V / "moflow.h5ad")
    fq_s = per_gene_fitquality(V / "moflow_scrambled.h5ad")
    common_fq = fq_o.index.intersection(fq_s.index)
    print(f"\n=== (1) FIT-QUALITY / CHROMATIN-CHANNEL (n={len(common_fq)} common genes) ===")
    for col in ["loss", "alpha_c_mean_abs", "velo_c_mean_abs"]:
        if col not in fq_o.columns or col not in fq_s.columns:
            continue
        o = fq_o.loc[common_fq, col].astype(float)
        s = fq_s.loc[common_fq, col].astype(float)
        mask = o.notna() & s.notna()
        o, s = o[mask], s[mask]
        w = stats.wilcoxon(o, s) if len(o) > 10 else (np.nan, np.nan)
        print(f"  {col:18s} orig median={o.median():.4g}  scr median={s.median():.4g}  "
              f"Δmedian={s.median()-o.median():+.4g}  Wilcoxon p={w[1]:.4g}")

    # ── (2) lag 분포 동일성 ───────────────────────────────────────────────────
    for key in ["cs_lag_median", "cs_lag_mean"]:
        o = orig[key].dropna(); s = scr[key].dropna()
        mw = stats.mannwhitneyu(o, s, alternative="two-sided")
        ks = stats.ks_2samp(o, s)
        print(f"\n=== (2) LAG DISTRIBUTION [{key}] ===")
        print(f"  orig  n={len(o)} median={o.median():.4f} mean={o.mean():.4f} "
              f"IQR=[{o.quantile(.25):.3f},{o.quantile(.75):.3f}] %>0={100*(o>0).mean():.1f}")
        print(f"  scr   n={len(s)} median={s.median():.4f} mean={s.mean():.4f} "
              f"IQR=[{s.quantile(.25):.3f},{s.quantile(.75):.3f}] %>0={100*(s>0).mean():.1f}")
        print(f"  Mann-Whitney U p={mw.pvalue:.4f} | KS D={ks.statistic:.4f} p={ks.pvalue:.4f}")

    # ── (3) per-gene lag: Spearman ρ (signed & |lag|) + Wilcoxon paired ───────
    common = orig.index.intersection(scr.index)
    print(f"\n=== (3) PER-GENE LAG (n={len(common)} common genes) ===")
    for key in ["cs_lag_median", "cs_lag_mean"]:
        o = orig.loc[common, key]; s = scr.loc[common, key]
        mask = o.notna() & s.notna()
        o, s = o[mask].astype(float), s[mask].astype(float)
        rho = stats.spearmanr(o, s)
        rho_abs = stats.spearmanr(o.abs(), s.abs())
        pear = stats.pearsonr(o, s)
        wil = stats.wilcoxon(o, s)
        sign_agree = 100 * (np.sign(o) == np.sign(s)).mean()
        rel = np.abs(s - o) / (np.abs(o) + 1e-9)
        print(f"  [{key}] n={len(o)}")
        print(f"    signed Spearman ρ={rho.correlation:+.4f} (p={rho.pvalue:.4g}) | "
              f"Pearson r={pear[0]:+.4f}")
        print(f"    |lag|  Spearman ρ={rho_abs.correlation:+.4f} (p={rho_abs.pvalue:.4g})")
        print(f"    sign-agreement={sign_agree:.1f}% | Wilcoxon paired p={wil.pvalue:.4g}")
        print(f"    per-gene 상대변화 median={np.nanmedian(rel):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
