#!/usr/bin/env python3
"""STEP2 (EXPLORATORY) — A1~A4 모델: baseline 크로마틴이 α/lag을 설명하는가.

설계 §4. 엄밀성 게이트(§5): 염색체 grouped hold-out CV(누출차단) · permutation null · 강상관 regularize
(ElasticNet) · 상관≠인과(예측만) · 결정론적(seed 고정).

A1  alpha_consensus ~ chromatin+covariates   : α 설명 (재현 타깃)
A2  lag_consensus   ~ chromatin+covariates   : lag 설명 (비재현 타깃, 대조 — 예상 R²≪A1)
A3  lag_reprod      ~ chromatin+covariates   : 어디서 lag이 재현되나 (노이즈 vs 조건부신호)
A4  nested ΔR²(chromatin | baseline_expr+gene_length) for α & lag  : confound 통제 incremental

모델: ElasticNet(표준화, alpha=ElasticNetCV 1회 선택 후 freeze) + HistGradientBoosting.
CV: GroupKFold(5), group=chrom (한 염색체가 train/test 동시 등장 금지).
유의성: A1~A3 = y 전역 permutation N=1000(EN); A4 = chromatin block row-permute N=1000(base-y 보존).

실행: conda run -n scv-preprocess python scripts/step2_models.py
출력: results/step2/{model_results.csv, feature_importance.csv, deltaR2_A4.csv}
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "results/step2"
SEED = 20260713
NPERM = 1000
NPERM_GBM = 200
CHROMATIN = ["me3_prom", "ac_prom", "me3_breadth", "ac_enh", "me1_enh", "n_links", "cpg_prom"]
BASE = ["baseline_expr", "gene_length_log10"]
FULL = CHROMATIN + BASE


def oof_predict_en(X, y, groups, alpha, l1=0.5):
    """GroupKFold OOF 예측 (ElasticNet, fold별 StandardScaler)."""
    oof = np.full(len(y), np.nan)
    gkf = GroupKFold(n_splits=5)
    for tr, te in gkf.split(X, y, groups):
        sc = StandardScaler().fit(X[tr])
        m = ElasticNet(alpha=alpha, l1_ratio=l1, max_iter=10000, random_state=SEED)
        m.fit(sc.transform(X[tr]), y[tr])
        oof[te] = m.predict(sc.transform(X[te]))
    return oof


def oof_predict_gbm(X, y, groups):
    oof = np.full(len(y), np.nan)
    gkf = GroupKFold(n_splits=5)
    for tr, te in gkf.split(X, y, groups):
        m = HistGradientBoostingRegressor(max_depth=3, max_iter=200,
                                          learning_rate=0.05, l2_regularization=1.0,
                                          random_state=SEED)
        m.fit(X[tr], y[tr])
        oof[te] = m.predict(X[te])
    return oof


def pick_alpha(X, y):
    sc = StandardScaler().fit(X)
    cv = ElasticNetCV(l1_ratio=0.5, cv=5, max_iter=10000, random_state=SEED)
    cv.fit(sc.transform(X), y)
    return float(cv.alpha_)


def run_model(df, target, feats, label):
    d = df[[target, "chrom"] + feats].dropna()
    X = d[feats].values.astype(float)
    y = d[target].values.astype(float)
    g = d["chrom"].values
    alpha = pick_alpha(X, y)
    # observed
    oof_en = oof_predict_en(X, y, g, alpha)
    r2_en = r2_score(y, oof_en); rho_en, _ = spearmanr(y, oof_en)
    oof_gb = oof_predict_gbm(X, y, g)
    r2_gb = r2_score(y, oof_gb); rho_gb, _ = spearmanr(y, oof_gb)
    # permutation null (EN, y shuffle)
    rng = np.random.default_rng(SEED)
    null = np.empty(NPERM)
    for i in range(NPERM):
        yp = rng.permutation(y)
        null[i] = r2_score(yp, oof_predict_en(X, yp, g, alpha))
    p_en = (1 + int((null >= r2_en).sum())) / (NPERM + 1)
    # GBM perm (smaller)
    nullg = np.empty(NPERM_GBM)
    for i in range(NPERM_GBM):
        yp = rng.permutation(y)
        nullg[i] = r2_score(yp, oof_predict_gbm(X, yp, g))
    p_gb = (1 + int((nullg >= r2_gb).sum())) / (NPERM_GBM + 1)
    return dict(analysis=label, target=target, n=len(y), n_feat=len(feats),
                en_alpha=alpha, R2_EN=r2_en, spearman_EN=rho_en, p_EN=p_en,
                R2_GBM=r2_gb, spearman_GBM=rho_gb, p_GBM=p_gb,
                null_R2_EN_mean=float(null.mean()), null_R2_EN_p95=float(np.quantile(null, .95)))


def nested_delta(df, target, label):
    """A4: chromatin의 base 위 incremental ΔR². chromatin block row-permute null(base-y 보존)."""
    d = df[[target, "chrom"] + FULL].dropna()
    Xb = d[BASE].values.astype(float)
    Xc = d[CHROMATIN].values.astype(float)
    y = d[target].values.astype(float)
    g = d["chrom"].values
    a_b = pick_alpha(Xb, y)
    a_f = pick_alpha(d[FULL].values.astype(float), y)
    r2_base = r2_score(y, oof_predict_en(Xb, y, g, a_b))
    r2_full = r2_score(y, oof_predict_en(np.hstack([Xc, Xb]), y, g, a_f))
    dR2 = r2_full - r2_base
    # null: chromatin block 행 셔플(base-y 관계 보존) → incremental만 파괴
    rng = np.random.default_rng(SEED + 1)
    null = np.empty(NPERM)
    for i in range(NPERM):
        perm = rng.permutation(len(y))
        Xf = np.hstack([Xc[perm], Xb])
        null[i] = r2_score(y, oof_predict_en(Xf, y, g, a_f)) - r2_base
    p = (1 + int((null >= dR2).sum())) / (NPERM + 1)
    return dict(analysis=label, target=target, n=len(y),
                R2_base=r2_base, R2_full=r2_full, deltaR2=dR2, p_deltaR2=p,
                null_dR2_mean=float(null.mean()), null_dR2_p95=float(np.quantile(null, .95)))


def importances(df, target, feats):
    d = df[[target] + feats].dropna()
    X = d[feats].values.astype(float); y = d[target].values.astype(float)
    sc = StandardScaler().fit(X)
    alpha = pick_alpha(X, y)
    m = ElasticNet(alpha=alpha, l1_ratio=0.5, max_iter=10000, random_state=SEED)
    m.fit(sc.transform(X), y)
    return pd.Series(m.coef_, index=feats)


def main():
    feat = pd.read_csv(OUT / "features_hspc.csv", index_col=0)
    tgt = pd.read_csv(OUT / "targets_alpha_lag.csv", index_col=0)
    df = feat.join(tgt[["alpha_consensus", "lag_consensus", "lag_reprod"]], how="inner")
    print(f"[mod] feature∩target join {df.shape}; chrom {df['chrom'].nunique()}개", flush=True)
    print(f"[mod] usable per target: α {df['alpha_consensus'].notna().sum()}, "
          f"lag {df['lag_consensus'].notna().sum()}, lag_reprod {df['lag_reprod'].notna().sum()}", flush=True)

    results = []
    results.append(run_model(df, "alpha_consensus", FULL, "A1_alpha_full"))
    print(f"[mod] A1 done R2_EN={results[-1]['R2_EN']:.3f} p={results[-1]['p_EN']:.3g}", flush=True)
    results.append(run_model(df, "lag_consensus", FULL, "A2_lag_full"))
    print(f"[mod] A2 done R2_EN={results[-1]['R2_EN']:.3f} p={results[-1]['p_EN']:.3g}", flush=True)
    results.append(run_model(df, "lag_reprod", FULL, "A3_lagreprod_full"))
    print(f"[mod] A3 done R2_EN={results[-1]['R2_EN']:.3f} p={results[-1]['p_EN']:.3g}", flush=True)
    res = pd.DataFrame(results)
    res.to_csv(OUT / "model_results.csv", index=False)

    # A4 nested ΔR²
    a4 = [nested_delta(df, "alpha_consensus", "A4_alpha"),
          nested_delta(df, "lag_consensus", "A4_lag")]
    pd.DataFrame(a4).to_csv(OUT / "deltaR2_A4.csv", index=False)
    print(f"[mod] A4 α ΔR²={a4[0]['deltaR2']:.3f} p={a4[0]['p_deltaR2']:.3g} | "
          f"lag ΔR²={a4[1]['deltaR2']:.3f} p={a4[1]['p_deltaR2']:.3g}", flush=True)

    # feature importance (EN coef, standardized) — A1 & A2
    imp = pd.DataFrame({
        "coef_alpha_A1": importances(df, "alpha_consensus", FULL),
        "coef_lag_A2": importances(df, "lag_consensus", FULL),
    })
    imp.to_csv(OUT / "feature_importance.csv")
    print("[mod] ✓ model_results.csv, deltaR2_A4.csv, feature_importance.csv", flush=True)
    print(res.to_string(index=False), flush=True)
    print(imp.to_string(), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
