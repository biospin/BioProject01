"""BIOP01-42 self-review — baseline ATAC→α (+0.212)의 2대 결함 검증:
① 발현량 confound: ATAC 접근성 ∝ 발현 ∝ α. 발현 통제 후에도 ATAC→α 남나 (partial Spearman).
② shuffle-null: α 순열 1000회로 null band. +0.212가 null 위인가 (프로젝트 5-seed 규율 정신)."""
import scanpy as sc, numpy as np, pandas as pd, os
from scipy import sparse
from scipy.stats import spearmanr, rankdata
DIR = "/workspace/data/cache/biop01/human_brain_GSE162170"

alpha = pd.read_csv(f"{DIR}/brain_gene_alpha.csv", index_col=0)["fit_alpha"].dropna()
alpha = alpha[alpha > 0]
log_a = np.log10(alpha)

# ATAC feature + RNA 발현량 (per gene)
atac = sc.read_h5ad(f"{DIR}/brain_atac.h5ad")
rna  = sc.read_h5ad(f"{DIR}/brain_rna.h5ad")
def genemean(ad):
    X = ad.X.tocsc() if sparse.issparse(ad.X) else ad.X
    return pd.Series(np.asarray(X.mean(0)).ravel(), index=ad.var_names)
atac_mean = genemean(atac)
rna_mean  = genemean(rna)   # 발현량 (spliced 평균)

g = alpha.index.intersection(atac_mean.index).intersection(rna_mean.index)
y = log_a.loc[g].values; xa = atac_mean.loc[g].values; xe = rna_mean.loc[g].values
print(f"공통 유전자: {len(g)}")

r_simple, p_simple = spearmanr(xa, y)
r_ae, _ = spearmanr(xa, xe)   # ATAC↔발현
r_ey, _ = spearmanr(xe, y)    # 발현↔α
print(f"\n[재확인] Spearman(ATAC, logα) = {r_simple:+.3f} (p={p_simple:.1e})")
print(f"[confound] Spearman(ATAC, 발현) = {r_ae:+.3f} | Spearman(발현, logα) = {r_ey:+.3f}")

# ① partial Spearman(ATAC, α | 발현): rank 잔차 상관
def partial_spearman(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    def resid(a, b):
        b1 = np.c_[np.ones_like(b), b]
        beta = np.linalg.lstsq(b1, a, rcond=None)[0]
        return a - b1 @ beta
    ex, ey = resid(rx, rz), resid(ry, rz)
    r, p = spearmanr(ex, ey)
    return r, p
r_par, p_par = partial_spearman(xa, y, xe)
print(f"\n① partial Spearman(ATAC, logα | 발현) = {r_par:+.3f} (p={p_par:.1e})  "
      f"→ {'발현 통제 후에도 유지' if abs(r_par)>0.1 and p_par<0.05 else '발현 confound로 상당부분 설명됨'}")

# ② shuffle-null: α 순열 1000회
rng = np.random.default_rng(0)
null = np.array([spearmanr(xa, rng.permutation(y))[0] for _ in range(1000)])
thr = null.mean() + 2*null.std(ddof=1)
print(f"\n② shuffle-null(1000): mean={null.mean():+.3f} sd={null.std(ddof=1):.3f} thr(+2sd)={thr:+.3f}")
print(f"   real {r_simple:+.3f} vs thr {thr:+.3f} → {'null 위(신호O)' if r_simple>thr else 'null 대비 미확보'}")

import json
json.dump({
  "n_genes": int(len(g)),
  "simple_spearman_atac_alpha": round(float(r_simple),4),
  "atac_vs_expression": round(float(r_ae),4), "expression_vs_alpha": round(float(r_ey),4),
  "partial_spearman_controlling_expression": round(float(r_par),4), "partial_p": float(p_par),
  "shuffle_null_mean": round(float(null.mean()),4), "shuffle_null_thr_2sd": round(float(thr),4),
  "real_above_null": bool(r_simple>thr),
  "verdict": "발현 통제 후 partial + shuffle-null 위면 진짜 chromatin→α 신호",
}, open(f"{DIR}/brain_selfreview_atac_alpha.json","w"), indent=2, ensure_ascii=False)
print("\nSaved brain_selfreview_atac_alpha.json")
