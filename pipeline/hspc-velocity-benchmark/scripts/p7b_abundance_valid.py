#!/usr/bin/env python3
"""p7b_abundance_valid.py — advisor 처방 유효검정 (BIOP01-54).

무효였던 partial(α,synth|abundance) 대신:
 B'-1 head-to-head: Spearman(α,synth) vs Spearman(abundance,synth) — α가 발현량보다 synth를 잘 예측하나?
      (α 포함 변수로 conditioning 회피)
 B'-2 γ 대칭 통제: 동일 분석을 γ에도. 순수 abundance 아티팩트면 α·γ 대칭이어야. α는 synth 회복·γ는 decay 미회복 →
      비대칭이면 "abundance만으로 설명" 반박.
 A'  근접조직 coupling 재현성: HSPC coupling rank vs macrophage/BMMC coupling rank (같은 0.2 바).

실행: ~/miniconda3/envs/scv-preprocess/bin/python -u scripts/p7b_abundance_valid.py
"""
import os, sys, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_profile_likelihood as pl

RES, DATA = pl.RES, os.path.join(pl.ROOT, "data")


def sp(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    return (stats.spearmanr(x[m], y[m]).statistic, stats.spearmanr(x[m], y[m]).pvalue, int(m.sum()))


def partial_sp(x, y, z):
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    rx, ry, rz = stats.rankdata(x[m]), stats.rankdata(y[m]), stats.rankdata(z[m])
    Z = np.c_[np.ones_like(rz), rz]
    res = lambda r: r - Z @ np.linalg.lstsq(Z, r, rcond=None)[0]
    return stats.pearsonr(res(rx), res(ry)).statistic


def coupling(path):
    import scanpy as sc
    a = sc.read_h5ad(path)
    raw = lambda l: (a.layers[l].A if hasattr(a.layers[l], "A") else np.asarray(a.layers[l])).astype(np.float64)
    C, S = raw("ATAC"), raw("Ms")
    out = np.full(C.shape[1], np.nan)
    for g in range(C.shape[1]):
        mm = np.isfinite(C[:, g]) & np.isfinite(S[:, g])
        if mm.sum() >= 20:
            out[g] = stats.spearmanr(C[mm, g], S[mm, g]).statistic
    return pd.Series(out, index=np.array(a.var_names))


HK = set(l.strip() for l in open(os.path.join(DATA, "housekeeping.txt")).read().splitlines() if l.strip())
ab = pd.read_csv(os.path.join(RES, "coupling_per_gene.csv")).set_index("gene")["abundance"]  # HSPC mean Ms
mv = pd.read_csv(os.path.join(RES, "multivelo_genes.csv")).set_index("gene")
alpha = mv["fit_alpha"]; alpha = alpha[alpha > 0]
gamma = mv["fit_gamma"]; gamma = gamma[gamma > 0]
synth = pd.read_csv(os.path.join(DATA, "k562_ttseq_synthrate.csv")).set_index("gene")["synth_rate"]; synth = synth[synth > 0].groupby(level=0).median()
thalf = pd.read_csv(os.path.join(DATA, "halflife_molm13.csv")).set_index("gene")["t_half_h"]; thalf = thalf[thalf > 0].groupby(level=0).median()
kdeg = (np.log(2) / thalf)

print("=== B'-1 head-to-head: α vs abundance, synth 예측력 (non-HK) ===")
c = alpha.index.intersection(synth.index).intersection(ab.index).difference(HK)
al, sy, ba = alpha.loc[c].values, synth.loc[c].values, ab.loc[c].values
ra = sp(al, sy); rb = sp(ba, sy); pa = partial_sp(al, sy, ba)
print(f"  n={len(c)}")
print(f"  Spearman(α, synth)        = {ra[0]:+.3f} (p={ra[1]:.1e})")
print(f"  Spearman(abundance, synth)= {rb[0]:+.3f} (p={rb[1]:.1e})")
print(f"  → α가 abundance보다 {'높음(kinetic 부가가치)' if ra[0]>rb[0] else '낮음/동등'}. (무효 partial={pa:+.3f}, 참고만)")

print("\n=== B'-2 γ 대칭 통제: γ vs abundance, decay(k_deg) 예측력 ===")
cg = gamma.index.intersection(kdeg.index).intersection(ab.index).difference(HK)
ga, kd, bg = gamma.loc[cg].values, kdeg.loc[cg].values, ab.loc[cg].values
rg = sp(ga, kd); rbg = sp(bg, kd); pg = partial_sp(ga, kd, bg)
print(f"  n={len(cg)}")
print(f"  Spearman(γ, k_deg)         = {rg[0]:+.3f} (p={rg[1]:.1e})  [회복=양]")
print(f"  Spearman(abundance, k_deg) = {rbg[0]:+.3f} (p={rbg[1]:.1e})")
print(f"  (무효 partial(γ,kdeg|ab)={pg:+.3f}, 참고만)")
print(f"\n  ★대칭성: α는 synth를 abundance보다 {'잘' if ra[0]>rb[0] else '못'} 예측(Δ={ra[0]-rb[0]:+.3f}) / "
      f"γ는 k_deg를 {'회복' if rg[0]>0.1 else '미회복'}(={rg[0]:+.3f}). "
      f"순수 abundance면 α·γ 대칭이어야 함 → {'비대칭(abundance 단일설명 반박)' if (ra[0]>rb[0] and rg[0]<0.1) else '대칭경향(주의)'}")

print("\n=== A' 근접조직 coupling 재현성 (같은 0.2 바) ===")
hspc_cp = pd.read_csv(os.path.join(RES, "coupling_per_gene.csv")).set_index("gene")["coupling"]
for name, path in [("macrophage", "multivelo_macrophage.h5ad"), ("BMMC", "multivelo_GSE194122_bmmc.h5ad")]:
    try:
        cp = coupling(os.path.join(pl.ROOT, "data", "velocity", path))
        common = hspc_cp.index.intersection(cp.index)
        r = stats.spearmanr(hspc_cp.loc[common].values, cp.loc[common].values, nan_policy='omit').statistic
        verdict = "재현✅(>0.2)" if abs(r) > 0.2 else "미재현(≤0.2)"
        print(f"  HSPC↔{name}: Spearman={r:+.3f} (shared {len(common)}) → {verdict}")
    except Exception as e:
        print(f"  {name} 스킵: {e}")
print("  [참고] HSPC↔human_brain(원거리)=+0.173, 모델 lag cross-dataset=+0.185")
