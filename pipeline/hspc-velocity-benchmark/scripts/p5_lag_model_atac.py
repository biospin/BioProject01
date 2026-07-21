#!/usr/bin/env python3
"""p5_lag_model_atac.py — 진짜 day0 ATAC feature로 baseline→timing 모델 (held-out lineage CV).

p5_lag_model.py(moflow Mc smoothed proxy)의 후속: 한계 ① 해소.
feature set 3종을 leave-one-lineage-out CV로 비교:
  mc-proxy   : {base_acc, chrom_rng, acc_mean}        (기존, moflow Mc smoothed)
  real-atac  : {prom_acc, enh_acc, enh_sum, prom_enh_ratio, n_enh}  (day0 ATAC peak)
  atac+mc    : 둘 합집합
target: lag(method-sensitive) / α(robust 대조).
지표 = held-out lineage Spearman(pred, actual). 모델 = Ridge(표준화).

실행: conda run -n scv-preprocess python scripts/p5_lag_model_atac.py
출력: results/lag_model_atac.md, results/lag_model_atac.csv
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import anndata as ad
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
SEED = 20260701
MIN_LINEAGE_N = 15


def assign_gene_lineage(rna, genes):
    Ms = rna[:, genes].layers["Ms"]
    Ms = np.asarray(Ms.todense()) if hasattr(Ms, "todense") else np.asarray(Ms)
    df = pd.DataFrame(Ms, index=rna.obs_names, columns=genes)
    df["lineage"] = rna.obs["lineage"].values
    return df.groupby("lineage")[genes].mean().idxmax(axis=0)


def chrom_features(moflow, genes):
    g = [x for x in genes if x in moflow.var_names]
    Mc = moflow[:, g].layers["Mc"]
    Mc = np.asarray(Mc.todense()) if hasattr(Mc, "todense") else np.asarray(Mc)
    is_hsc = (moflow.obs["lineage"].astype(str) == "HSC/MPP").to_numpy()
    base = Mc[is_hsc].mean(axis=0) if is_hsc.any() else Mc.mean(axis=0)
    return pd.DataFrame({"base_acc": base, "chrom_rng": Mc.max(0) - Mc.min(0),
                         "acc_mean": Mc.mean(0)}, index=g)


def loo_lineage_cv(X, y, lineages, feat_cols):
    pred = pd.Series(np.nan, index=X.index)
    per = {}
    lins = [l for l in lineages.unique() if (lineages == l).sum() >= MIN_LINEAGE_N]
    for hold in lins:
        tr, te = lineages != hold, lineages == hold
        if tr.sum() < 20:
            continue
        sc = StandardScaler().fit(X.loc[tr, feat_cols])
        m = Ridge(alpha=1.0).fit(sc.transform(X.loc[tr, feat_cols]), y[tr])
        pred[te] = m.predict(sc.transform(X.loc[te, feat_cols]))
        if te.sum() >= 8:
            per[hold] = spearmanr(y[te], pred[te])[0]
    ok = pred.notna() & y.notna()
    overall = spearmanr(y[ok], pred[ok])[0] if ok.sum() > 8 else np.nan
    return pred, per, overall


def main():
    np.random.seed(SEED)
    mv = pd.read_csv(RES / "multivelo_genes.csv", index_col=0)
    mv["lag"] = mv["fit_t_sw2"] - mv["fit_t_sw1"]
    atac = pd.read_csv(RES / "atac_baseline_features.csv", index_col=0)
    rna = ad.read_h5ad(HERE / "data/velocity/dl_input_rna.h5ad")
    moflow = ad.read_h5ad(HERE / "data/velocity/moflow.h5ad")

    genes = [g for g in mv.index if g in rna.var_names]
    lineage = assign_gene_lineage(rna, genes)
    cfeat = chrom_features(moflow, genes)

    df = mv.loc[genes, ["lag", "fit_alpha"]].join(cfeat, how="inner").join(atac, how="left")
    df["lineage"] = lineage.reindex(df.index)

    MC = ["base_acc", "chrom_rng", "acc_mean"]
    ATAC_F = ["prom_acc", "enh_acc", "enh_sum", "prom_enh_ratio", "n_enh"]
    SETS = {"mc-proxy": MC, "real-atac": ATAC_F, "atac+mc": MC + ATAC_F}
    # 공정 비교: 세 set 모두 결측 없는 gene으로 한정
    df = df.dropna(subset=["lag", "fit_alpha", "lineage"] + MC + ATAC_F)
    print(f"[atac-model] 공통 gene {len(df)}\n{df['lineage'].value_counts().to_string()}", flush=True)

    results, preds = {}, {}
    for tgt in ["lag", "fit_alpha"]:
        for sname, cols in SETS.items():
            pred, per, overall = loo_lineage_cv(df[cols + [tgt]], df[tgt], df["lineage"], cols)
            results[(tgt, sname)] = dict(per=per, overall=overall)
            if sname == "real-atac":
                preds[(tgt,)] = pred
            print(f"[atac-model] {tgt:9s} [{sname:9s}] held-out ρ={overall:+.3f}", flush=True)

    for tgt in ["lag", "fit_alpha"]:
        df[f"pred_{tgt}_atac"] = preds[(tgt,)]
    df.to_csv(RES / "lag_model_atac.csv")

    lin_cols = sorted({l for r in results.values() for l in r["per"]})
    L = ["# P5 — 진짜 day0 ATAC feature → kinetic timing 모델 (held-out lineage CV)", "",
         f"- {len(df)} gene(세 feature set 공통), Ridge, leave-one-lineage-out.",
         "- p5_lag_model.py 한계 ①(moflow Mc smoothed) 해소: **day0 HSC/MPP ATAC peak**에서 promoter/enhancer 접근성 직접 사용.",
         "- feature set: **mc-proxy**(moflow Mc) / **real-atac**(prom/enh ATAC) / **atac+mc**(합집합).", "",
         "## held-out lineage 일반화 (Spearman pred vs actual)", "",
         "| target | feature set | overall | " + " | ".join(lin_cols) + " |",
         "|---|---|---|" + "---|" * len(lin_cols)]
    for tgt, tlbl in [("lag", "lag (method-sensitive)"), ("fit_alpha", "α (robust)")]:
        for sname in SETS:
            r = results[(tgt, sname)]
            cells = " | ".join(f"{r['per'].get(l, float('nan')):+.2f}" for l in lin_cols)
            L.append(f"| {tlbl} | {sname} | **{r['overall']:+.3f}** | {cells} |")
    lag_mc = results[("lag", "mc-proxy")]["overall"]
    lag_at = results[("lag", "real-atac")]["overall"]
    a_at = results[("fit_alpha", "real-atac")]["overall"]
    L += ["", "## 해석", "",
          f"- **진짜 ATAC baseline으로 lag held-out ρ={lag_at:+.3f}** (moflow Mc proxy {lag_mc:+.3f}).",
          f"  → {'real ATAC가 proxy보다 일반화 우위' if lag_at>lag_mc+0.05 else ('proxy와 동등' if abs(lag_at-lag_mc)<=0.05 else 'proxy가 더 높음(smoothing이 RNA정보 누설 가능)')}.",
          f"- α(robust) real-atac ρ={a_at:+.3f}.",
          "- **FINDINGS 정합**: lag 값 자체는 cross-method 비robust(H1)지만, day0 baseline ATAC 접근성으로 "
          "lag을 lineage 간 예측하는 신호 크기를 정량 — drug-timing 모델 feature 후보 평가.",
          "- ⚠️ peak-count 기반(fragment 미보유), gene→lineage dominant-expression 근사, Ridge α=1 고정.",
          "- 다음: per-lineage refit target(lineage_refit) + bootstrap 안정 gene으로 target 한정, "
          "promoter/enhancer 개별 ablation."]
    (RES / "lag_model_atac.md").write_text("\n".join(L) + "\n")
    print("[atac-model] ✓ → lag_model_atac.md", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
