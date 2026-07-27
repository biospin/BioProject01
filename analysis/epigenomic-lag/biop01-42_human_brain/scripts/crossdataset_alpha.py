"""BIOP01-42 step4 — cross-dataset α rank concordance. HSPC α(git) ↔ human_brain α.
기존 파이프라인 +0.475 재현확인 + 내 fresh scVelo brain α 독립 재현."""
import pandas as pd, numpy as np, json
from scipy.stats import spearmanr
DIR = "/workspace/data/cache/biop01/human_brain_GSE162170"

def load_alpha(f, col="fit_alpha"):
    d = pd.read_csv(f, index_col=0)
    a = d[col].dropna(); a = a[a > 0]
    return a

hspc = load_alpha(f"{DIR}/multivelo_genes.csv")
brain_old = load_alpha(f"{DIR}/multivelo_genes_human_brain.csv")
brain_new = load_alpha(f"{DIR}/brain_gene_alpha.csv")
print("HSPC a: %d | 기존 brain a: %d | 내 fresh brain a: %d" % (len(hspc), len(brain_old), len(brain_new)))

def xrho(a, b, label):
    g = a.index.intersection(b.index)
    if len(g) < 10:
        print("  %s: shared=%d 부족" % (label, len(g))); return None
    r, p = spearmanr(a.loc[g], b.loc[g])
    verdict = "재현O(>0.3)" if abs(r) > 0.3 else "약함"
    print("  %s\n     shared=%d gene, Spearman(rank a) = %+.3f (p=%.2e)  %s" % (label, len(g), r, p, verdict))
    return {"shared": int(len(g)), "spearman": round(float(r), 4), "p": float(p)}

print("\n=== cross-dataset a rank concordance ===")
r1 = xrho(hspc, brain_old, "HSPC vs 기존 brain(MultiVelo) [기존 +0.475 재현확인]")
r2 = xrho(hspc, brain_new, "HSPC vs 내 fresh brain(scVelo dynamical) [독립 재현]")
r3 = xrho(brain_old, brain_new, "기존 brain vs 내 fresh brain [내 재현 sanity]")

json.dump({"hspc_vs_existing_brain": r1, "hspc_vs_my_fresh_brain": r2, "existing_vs_my_brain": r3,
           "criterion": "|Spearman|>0.3 재현", "note": "a rank cross-dataset. 기존 파이프라인 concordance_human_brain.md +0.475 대조."},
          open(f"{DIR}/brain_crossdataset_alpha_concordance.json", "w"), indent=2, ensure_ascii=False)
print("\nSaved brain_crossdataset_alpha_concordance.json")
