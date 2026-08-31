"""P5c — baseline ATAC→α 의 약한 신호가 선형 모형 탓인지 확인한다.

P5b(atac_alpha_expression_confound.md)에서 ATAC→α 는 raw held-out ρ=+0.309,
발현 통제 partial ρ=+0.112 로 발현 confound에 잠식됐다. "선형 모형이라 놓친 것 아닌가"라는
반론에 답하기 위해 같은 특징·같은 계보 홀드아웃에서 모형 계열만 바꿔 비교한다.

실행: python scripts/p5c_alpha_model_class_check.py   (결과 dir 기준 상대경로)
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler

R = "results"

# 진짜 ATAC peak 특징을 쓴다. lag_model.csv의 base_acc/chrom_rng/acc_mean은
# ATAC peak이 아니라 다른 양이므로 이 분석에 쓰지 않는다(부호가 달라진다).
feat = pd.read_csv(f"{R}/atac_baseline_features.csv").set_index("gene")
lagm = pd.read_csv(f"{R}/lag_model.csv", index_col=0)
abund = pd.read_csv(f"{R}/coupling_per_gene.csv").set_index("gene")["abundance"]

FEATS = list(feat.columns)
d = (feat.join(lagm[["fit_alpha", "lineage"]], how="inner")
         .join(abund, how="left")
         .dropna(subset=FEATS + ["fit_alpha", "lineage"]))
print(f"병합 {d.shape} | 특징 {FEATS}")
print("개별 상관(vs fit_alpha):",
      {c: round(spearmanr(d[c], d.fit_alpha)[0], 3) for c in FEATS})

X, y, groups = d[FEATS].values, d.fit_alpha.values, d.lineage.values
MODELS = {
    "linear(RidgeCV)": lambda: RidgeCV(alphas=np.logspace(-3, 3, 25)),
    "RandomForest": lambda: RandomForestRegressor(
        n_estimators=500, min_samples_leaf=5, random_state=0, n_jobs=-1),
    "GradBoost": lambda: GradientBoostingRegressor(random_state=0),
}

ok = d.abundance.notna().values
rank_ab = np.argsort(np.argsort(d.abundance.values[ok]))


def residual_vs_abundance(v):
    """발현 순위에 대한 선형 잔차. 발현 confound를 뺀 뒤 상관을 본다."""
    rv = np.argsort(np.argsort(v[ok]))
    return rv - np.polyval(np.polyfit(rank_ab, rv, 1), rank_ab)


print(f"\n{'model':18s} {'held-out rho':>13s} {'p':>10s} {'partial(발현통제)':>18s}")
for name, make in MODELS.items():
    pred = np.full(len(y), np.nan)
    for tr, te in LeaveOneGroupOut().split(X, y, groups):   # 계보 하나를 빼고 학습
        sc = StandardScaler().fit(X[tr])
        pred[te] = make().fit(sc.transform(X[tr]), y[tr]).predict(sc.transform(X[te]))
    rho, p = spearmanr(pred, y)
    prho, _ = spearmanr(residual_vs_abundance(pred), residual_vs_abundance(y))
    print(f"{name:18s} {rho:+13.3f} {p:10.2e} {prho:+18.3f}")

print("\nP5b 기록: held-out rho=+0.309, 발현통제 partial=+0.112, n=472")
print("선형이 이 값을 재현하면 설정이 일치한다는 뜻이다.")
