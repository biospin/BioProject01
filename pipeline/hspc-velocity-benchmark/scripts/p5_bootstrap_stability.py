#!/usr/bin/env python3
"""p5_bootstrap_stability.py — per-gene lag bootstrap 안정성 (DESIGN §4D, §4C 1차).

§71-C 1차 기준 = bootstrap lag-sign stability. cell을 복원추출 재표집 → per-gene DTW c-s lag
재계산 → **부호 flip rate**와 **lag CV** 산출. (전체 re-fit은 GPU 다수 회 → 본 단계는 fit된
latent_time 고정 하에 cell 표집 안정성을 측정 = stability 하한.)

입력: crakvelo fit (adata_rna_fit: Ms, latent_time, velocity_genes; adata_atac_fit: cisTopic; B.txt)
방법: gene_chrom = cisTopic @ B / region수, Ms = spliced moments. b회 cell 복원추출 →
      zbin(latent_time 정렬) → dtw_lag → per-gene lag_b. flip_rate = min(>0,<0)/N, CV = std/|mean|.
출력: results/bootstrap_stability.md, results/bootstrap_stability.csv

실행: conda run -n scv-preprocess python scripts/p5_bootstrap_stability.py [N_BOOT]
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import anndata as ad

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
sys.path.insert(0, str(HERE / "scripts"))
from p2_crakvelo_lag import dtw_lag, find_fit_dir

N_BOOT = int(sys.argv[1]) if len(sys.argv) > 1 else 40
N_BIN = 50            # bootstrap은 속도 위해 50 (extraction의 100보다 거침)
SEED = 20260701


def zbin_order(x, order, nbin):
    xs = np.asarray(x, float)[order]
    idx = np.linspace(0, len(xs), nbin + 1).astype(int)
    b = np.array([np.nanmean(xs[idx[k]:idx[k + 1]]) if idx[k + 1] > idx[k] else np.nan
                  for k in range(nbin)])
    b = pd.Series(b).interpolate(limit_direction="both").to_numpy()
    sd = b.std()
    return (b - b.mean()) / sd if sd > 1e-9 else b - b.mean()


def main():
    rng = np.random.default_rng(SEED)
    fit = find_fit_dir()
    print(f"[boot] fit dir: {fit}  N_BOOT={N_BOOT} N_BIN={N_BIN}", flush=True)
    R = ad.read_h5ad(fit / "adata_rna_fit.h5ad")
    A = ad.read_h5ad(fit / "adata_atac_fit.h5ad")
    B = np.loadtxt(fit / "B.txt", delimiter=",")
    if B.ndim == 1:
        B = B.reshape(-1, R.n_vars)
    lt = np.asarray(R.obs["latent_time"], float)
    Ms = R.layers["Ms"] if "Ms" in R.layers else (R.layers.get("spliced", R.X))
    Ms = np.asarray(Ms.todense()) if hasattr(Ms, "todense") else np.asarray(Ms)
    cisT = A.obsm["cisTopic"]
    cisT = np.asarray(cisT.todense()) if hasattr(cisT, "todense") else np.asarray(cisT)
    reg_per_gene = B.sum(axis=0)
    gene_chrom = cisT @ B
    with np.errstate(invalid="ignore", divide="ignore"):
        gene_chrom = gene_chrom / np.where(reg_per_gene > 0, reg_per_gene, np.nan)
    vgenes = (np.asarray(R.var["velocity_genes"], bool)
              if "velocity_genes" in R.var else np.ones(R.n_vars, bool))
    names = list(R.var_names)
    gidx = [gi for gi, g in enumerate(names)
            if vgenes[gi] and reg_per_gene[gi] > 0
            and np.nanstd(gene_chrom[:, gi]) > 1e-9 and np.nanstd(Ms[:, gi]) > 1e-9]
    print(f"[boot] 검정 gene {len(gidx)} / {R.n_obs} cell", flush=True)

    n = R.n_obs
    boot = np.full((len(gidx), N_BOOT), np.nan)
    for b in range(N_BOOT):
        samp = rng.integers(0, n, n)                 # 복원추출
        order = np.argsort(lt[samp])
        for k, gi in enumerate(gidx):
            c = gene_chrom[samp, gi]
            s = Ms[samp, gi]
            cb = zbin_order(c, order, N_BIN)
            sb = zbin_order(s, order, N_BIN)
            boot[k, b] = dtw_lag(cb, sb)[1]
        if (b + 1) % 5 == 0:
            print(f"[boot] {b+1}/{N_BOOT}", flush=True)

    mean = np.nanmean(boot, axis=1)
    std = np.nanstd(boot, axis=1)
    pos = np.nanmean(boot > 0, axis=1)
    neg = np.nanmean(boot < 0, axis=1)
    flip = np.minimum(pos, neg)                       # 부호 flip rate (0=완전안정, 0.5=완전불안정)
    cv = std / np.where(np.abs(mean) > 1e-6, np.abs(mean), np.nan)
    df = pd.DataFrame(dict(gene=[names[gi] for gi in gidx],
                           lag_mean=mean, lag_std=std, sign_flip=flip, cv=cv)).set_index("gene")
    df.to_csv(RES / "bootstrap_stability.csv")

    stable = (df["sign_flip"] < 0.10).mean()
    med_flip = df["sign_flip"].median()
    L = ["# P5 — Bootstrap lag-sign stability (DESIGN §4D, §4C 1차)", "",
         f"- crakvelo fit, {len(gidx)} velocity-gene × {N_BOOT} bootstrap(cell 복원추출), "
         f"N_BIN={N_BIN}, seed={SEED}.",
         "- sign_flip = min(부호>0 비율, 부호<0 비율). 0=완전 안정, 0.5=완전 불안정(동전).",
         "- ⚠️ latent_time 고정(전체 re-fit 아님) → **stability 하한**.", "",
         "## 결과", "",
         f"- **부호 안정 gene(sign_flip<0.10) = {stable:.1%}**, median sign_flip = {med_flip:.3f}.",
         f"- lag CV median = {df['cv'].median():.2f} (|mean| 대비 변동).",
         "", "### 가장 안정 / 불안정 gene (sign_flip)", ""]
    L.append("| | gene | lag_mean | sign_flip | cv |")
    L.append("|---|---|---|---|---|")
    for g, r in df.nsmallest(8, "sign_flip").iterrows():
        L.append(f"| 안정 | {g} | {r['lag_mean']:+.2f} | {r['sign_flip']:.3f} | {r['cv']:.2f} |")
    for g, r in df.nlargest(8, "sign_flip").iterrows():
        L.append(f"| 불안정 | {g} | {r['lag_mean']:+.2f} | {r['sign_flip']:.3f} | {r['cv']:.2f} |")
    L += ["", "## 해석",
          f"- per-gene lag 부호는 cell 표집에 {'민감' if med_flip > 0.15 else '대체로 안정'}"
          f"(median flip {med_flip:.3f}, 안정 {stable:.0%}).",
          "- ⚠️ **이건 안정성의 *가장 약한* 형태**: latent_time·fit 고정 하에 *표집 노이즈*만 본 것. "
          "→ cross-method 불일치(H1)·정확도 실패(simulator)와 **모순 아님**. lag은 '한 fit 안에선 표집에 안정'"
          "하지만 'method/정확도엔 비robust'. 진짜 stability(전체 re-fit 반복)는 이보다 낮음(GPU 반복 fit 시 측정).",
          "- 용도: §71-C agreement-set 1차 기준(표집 안정 gene 우선)·P5 target gene 선별 필터로 사용."]
    (RES / "bootstrap_stability.md").write_text("\n".join(L) + "\n")
    print(f"[boot] ✓ stable {stable:.1%}, med_flip {med_flip:.3f} → bootstrap_stability.md", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
