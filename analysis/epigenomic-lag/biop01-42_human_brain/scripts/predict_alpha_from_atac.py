"""BIOP01-42 Phase-1 step3 — baseline epigenomic feature(ATAC) → α 예측.
가설: baseline 크로마틴 접근성이 gene의 전사속도 α를 예측하는가 (HSPC baseline→α ρ=+0.31 패턴이 brain에서도?).
target=log α (heavy-tail). feature=per-gene ATAC gene-activity 통계. gene-level 5-fold CV Spearman.
velo-mv env."""
import numpy as np, pandas as pd, scanpy as sc, os
from scipy import sparse
from scipy.stats import spearmanr
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

DIR = "/workspace/data/cache/biop01/human_brain_GSE162170"

# --- α (target) ---
alpha = pd.read_csv(os.path.join(DIR, "brain_gene_alpha.csv"), index_col=0)
alpha = alpha["fit_alpha"].dropna()
alpha = alpha[alpha > 0]
print(f"α 유전자: {len(alpha)}  (median {alpha.median():.3f}, max {alpha.max():.1f})")
log_alpha = np.log10(alpha)

# --- baseline ATAC feature (per gene) ---
atac = sc.read_h5ad(os.path.join(DIR, "brain_atac.h5ad"))
X = atac.X.tocsc()
genes = atac.var_names
mean_acc = np.asarray(X.mean(axis=0)).ravel()               # 평균 접근성
det_rate = np.asarray((X > 0).mean(axis=0)).ravel()          # 검출률(열린 세포 비율)
sq = X.multiply(X).mean(axis=0)
var_acc = np.asarray(sq).ravel() - mean_acc**2               # 분산
feat = pd.DataFrame({"atac_mean": mean_acc, "atac_detrate": det_rate, "atac_var": var_acc}, index=genes)

# --- 매칭 ---
common = feat.index.intersection(log_alpha.index)
feat = feat.loc[common]; y = log_alpha.loc[common].values
print(f"α ∩ ATAC feature 유전자: {len(common)}")

# --- 단순 상관 (baseline) ---
rho_mean, p_mean = spearmanr(feat["atac_mean"], y)
print(f"\n[단순] Spearman(ATAC 평균접근성, log α) = {rho_mean:+.3f} (p={p_mean:.2e})")
rho_det, _ = spearmanr(feat["atac_detrate"], y)
print(f"[단순] Spearman(ATAC 검출률, log α) = {rho_det:+.3f}")

# --- held-out CV 예측 (gene-level 5-fold) ---
Xf = StandardScaler().fit_transform(feat.values)
def cv_pred(model):
    pred = np.zeros_like(y)
    for tr, te in KFold(5, shuffle=True, random_state=42).split(Xf):
        model.fit(Xf[tr], y[tr]); pred[te] = model.predict(Xf[te])
    return spearmanr(pred, y)[0]
rho_ridge = cv_pred(Ridge(alpha=1.0))
rho_rf = cv_pred(RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=8))
print(f"\n[held-out 5-fold CV] Spearman(예측 log α, 실제) — Ridge {rho_ridge:+.3f} · RF {rho_rf:+.3f}")

res = {
  "n_alpha_genes": int(len(alpha)), "n_matched": int(len(common)),
  "simple_spearman_atac_mean_vs_logalpha": round(float(rho_mean),4), "p_value": float(p_mean),
  "simple_spearman_detrate": round(float(rho_det),4),
  "cv_spearman_ridge": round(float(rho_ridge),4), "cv_spearman_rf": round(float(rho_rf),4),
  "target": "log10(alpha)", "features": ["atac_mean","atac_detrate","atac_var"],
  "note": "held-out gene-level 5-fold CV. baseline 크로마틴(ATAC gene activity)이 전사속도 α를 예측하는지. HSPC baseline→α ρ≈+0.31과 대조.",
}
import json
json.dump(res, open(os.path.join(DIR,"brain_baseline_atac_to_alpha.json"),"w"), indent=2, ensure_ascii=False)
print("\n"+json.dumps(res, indent=2, ensure_ascii=False))
print("DONE_PREDICT")
