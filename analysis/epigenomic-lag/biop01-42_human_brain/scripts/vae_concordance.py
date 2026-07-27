"""BIOP01-42 옵션 A §7 — MultiVeloVAE α cross-dataset/method 정제 비교.
brain VAE α ↔ HSPC VAE α (same-method, 최약축 핵심) + brain VAE ↔ scVelo/MultiVelo."""
import pandas as pd, numpy as np, json
from scipy.stats import spearmanr
DIR = "/workspace/data/cache/biop01/human_brain_GSE162170"

def load(f, col):
    d = pd.read_csv(f, index_col=0)[col].dropna()
    return d[d > 0]

brain_vae = load(f"{DIR}/brain_multivelovae_genes.csv", "vae_alpha")     # 내 brain VAE α
hspc_vae  = load(f"{DIR}/hspc_targets_alpha_lag.csv", "alpha_vae")       # HSPC VAE α (git)
brain_scv = load(f"{DIR}/brain_gene_alpha.csv", "fit_alpha")             # 내 brain scVelo α
hspc_mv   = load(f"{DIR}/multivelo_genes.csv", "fit_alpha")              # HSPC MultiVelo α
print("brain VAE %d | HSPC VAE %d | brain scVelo %d | HSPC MV %d" % (len(brain_vae), len(hspc_vae), len(brain_scv), len(hspc_mv)))

def xrho(a, b, label):
    g = a.index.intersection(b.index)
    if len(g) < 10:
        print("  %s: shared=%d 부족" % (label, len(g))); return None
    r, p = spearmanr(a.loc[g], b.loc[g])
    print("  %-52s shared=%3d  Spearman=%+.3f (p=%.1e)  %s" % (label, len(g), r, p, "재현O" if abs(r) > 0.3 else "약함"))
    return {"shared": int(len(g)), "spearman": round(float(r), 4), "p": float(p)}

print("\n=== §7 핵심: same-method(VAE) cross-dataset ===")
r_vae = xrho(hspc_vae, brain_vae, "HSPC VAE α ↔ brain VAE α [최약축 정제]")
print("\n=== 보조: method-robustness ===")
r_wb  = xrho(brain_vae, brain_scv, "brain VAE α ↔ brain scVelo α [within-brain method]")
r_mv  = xrho(hspc_mv, brain_vae, "HSPC MultiVelo α ↔ brain VAE α [cross method+dataset]")

out = {"hspc_vae_vs_brain_vae": r_vae, "brain_vae_vs_brain_scvelo": r_wb, "hspc_mv_vs_brain_vae": r_mv,
       "criterion": "|Spearman|>0.3", "note": "MultiVeloVAE 정제. same-method(VAE) cross-dataset이 §7 최약축 직결."}
json.dump(out, open(f"{DIR}/brain_vae_concordance.json", "w"), indent=2, ensure_ascii=False)
print("\nSaved brain_vae_concordance.json")
