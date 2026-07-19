#!/usr/bin/env python3
"""p8_per_gene_direction_table.py — 유전자×method 방향(chromatin-leading vs RNA-first) 일치도 표 (BIOP01-55 후속).

목적: 심사자가 per-gene으로 method 불일치를 직접 확인할 수 있는 Supplementary Table.
- 부호 가변(방향 정보 있음): MoFlow cs_lag_median, CRAK-Velo cs_lag_median, MultiVeloVAE rate-proxy(1/α_c−1/α)
- 부호 무정보: MultiVelo lag(sw2−sw1) — switch-time 단조정렬로 구조적 양수 → 방향 판정 제외(값만 병기)
산출: results/per_gene_direction_by_method.csv + results/per_gene_direction_summary.md
"""
import os, sys, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_profile_likelihood as pl
RES = pl.RES

MYE = ["ELANE", "AZU1", "MPO", "LYZ", "CSF1R", "S100A9"]
HSC = ["HLF", "CRHBP", "MEIS1"]
OTHER_MK = {"IRF8": "pDC", "TCF4": "pDC", "GATA2": "prog", "CPA3": "mast",
            "ITGA2B": "MK", "VWF": "MK", "TFRC": "ery"}


def col(df, *cands):
    for c in cands:
        if c in df.columns: return df[c]
    return None


mo = pd.read_csv(f"{RES}/moflow_genes.csv").set_index("gene")
ck = pd.read_csv(f"{RES}/crakvelo_genes.csv").set_index("gene")
va = pd.read_csv(f"{RES}/multivelovae_genes.csv").set_index("gene")
mv = pd.read_csv(f"{RES}/multivelo_genes.csv").set_index("gene")

d = pd.DataFrame(index=sorted(set(mo.index) | set(ck.index) | set(va.index) | set(mv.index)))
d.index.name = "gene"
d["moflow_cs_lag"] = col(mo, "cs_lag_median", "cs_lag_mean")
d["crak_cs_lag"] = col(ck, "cs_lag_median", "cs_lag_mean")
d["vae_proxy_lag"] = (1 / va["vae_alpha_c"] - 1 / va["vae_alpha"]).replace([np.inf, -np.inf], np.nan)
d["multivelo_lag_sw2_sw1"] = (mv["fit_t_sw2"] - mv["fit_t_sw1"])  # 부호 구조적(무정보)

SIGN_METHODS = ["moflow", "crak", "vae_proxy"]
for m, c in zip(SIGN_METHODS, ["moflow_cs_lag", "crak_cs_lag", "vae_proxy_lag"]):
    d[f"dir_{m}"] = d[c].map(lambda v: np.nan if pd.isna(v) else ("chromatin" if v > 0 else "RNA"))

dirs = d[[f"dir_{m}" for m in SIGN_METHODS]]
d["n_methods"] = dirs.notna().sum(axis=1)
d["n_chromatin"] = (dirs == "chromatin").sum(axis=1)
d["n_RNA"] = (dirs == "RNA").sum(axis=1)


def consensus(r):
    n = r["n_methods"]
    if n < 2: return "insufficient"
    if r["n_chromatin"] == n: return "unanimous_chromatin"
    if r["n_RNA"] == n: return "unanimous_RNA"
    return "split"


d["consensus"] = d.apply(consensus, axis=1)
d["marker"] = ["myeloid" if g in MYE else "HSC" if g in HSC else OTHER_MK.get(g, "") for g in d.index]
d = d.sort_values(["consensus", "gene"])
out = f"{RES}/per_gene_direction_by_method.csv"
d.to_csv(out)

# ---- 요약 ----
sub = d[d.n_methods >= 2]
vc = sub["consensus"].value_counts()
L = ["# 유전자 × method 방향(chromatin-leading vs RNA-first) 일치도 — Supplementary 재료", "",
     "> `scripts/p8_per_gene_direction_table.py`. 부호 가변 3 method(MoFlow·CRAK-Velo·MultiVeloVAE rate-proxy)의 유전자별 방향과 합의 여부.",
     "> MultiVelo lag(sw2−sw1)은 switch-time 단조정렬로 **구조적 양수 = 방향 무정보**라 판정에서 제외(값만 병기).",
     f"> 전체 표: `results/per_gene_direction_by_method.csv` (n={len(d)} genes).", "",
     "## 합의 분포 (부호 가변 method ≥2개 있는 유전자)", "",
     "| 합의 | 유전자 수 | 비율 |", "|---|---|---|"]
for k in ["unanimous_chromatin", "unanimous_RNA", "split"]:
    n = int(vc.get(k, 0)); L.append(f"| {k} | {n} | {n/len(sub):.1%} |")
L += [f"| **계** | {len(sub)} | 100% |", "",
      f"**만장일치(방향 일치) = {int(vc.get('unanimous_chromatin',0)+vc.get('unanimous_RNA',0))}/{len(sub)} "
      f"({(vc.get('unanimous_chromatin',0)+vc.get('unanimous_RNA',0))/len(sub):.1%})**, 나머지는 method 간 방향이 갈린다.", ""]

L += ["## pairwise sign-agreement (chance=50%)", "", "| 쌍 | 일치율 | n |", "|---|---|---|"]
import itertools
for a, b in itertools.combinations(SIGN_METHODS, 2):
    m = d[[f"dir_{a}", f"dir_{b}"]].dropna()
    L.append(f"| {a} × {b} | {(m[f'dir_{a}']==m[f'dir_{b}']).mean():.1%} | {len(m)} |")

L += ["", "## canonical marker (계통 생물학 대조)", "",
      "| gene | 계통 | MoFlow | CRAK | VAE-proxy | 합의 |", "|---|---|---|---|---|---|"]
for g in MYE + HSC + list(OTHER_MK):
    if g in d.index:
        r = d.loc[g]
        f = lambda v: "—" if (isinstance(v, float) and np.isnan(v)) else v
        L.append(f"| {g} | {r['marker']} | {f(r['dir_moflow'])} | {f(r['dir_crak'])} | {f(r['dir_vae_proxy'])} | {r['consensus']} |")

L += ["", "## 읽는 법 (정직)",
      "- **만장일치 비율이 낮고 split이 많다 = per-gene 방향이 method에 따라 갈린다** → '이 유전자는 chromatin-leading'을 신뢰성 있게 말할 수 없다(BIOP01-55 결론).",
      "- 다만 **계통 수준 aggregate**(myeloid priming vs HSC)에서는 세 method 모두 같은 방향 경향을 보인다 — 거친 구조는 재현되나 유전자 단위는 아니다.",
      "- MultiVelo 값은 방향 판정에 쓰지 않는다(구조적 양수)."]
open(f"{RES}/per_gene_direction_summary.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[:40]))
print(f"\nwrote {out} + per_gene_direction_summary.md")
