#!/usr/bin/env python3
"""P3 — per-lineage refit lag 일치도 ("진짜 within-lineage H1"). DESIGN §4; CLAUDE.md #2.

p2_multivelo_perlineage.py 가 lineage별 따로 fit한 switch time을 받아,
lag(=fit_t_sw2−fit_t_sw1)이 **gene-intrinsic robust 속성인지** 평가한다.

H1 재평가 축 (전역 3-way H1은 cross-method였음; 여기선 within-method cross-lineage):
  A. lineage별 lag magnitude 분포 (진짜 per-lineage fit — lineage_lag.md의 dominant-귀속 대체).
  B. cross-lineage 일치도: ≥2 lineage에서 fit된 gene의 lag magnitude rank Spearman (lineage 쌍별).
     → 같은 gene의 chromatin→transcription lag이 어느 분화경로로 fit하든 비슷한가?
  C. per-lineage refit vs 전역 fit lag (multivelo_genes.csv) Spearman.
  D. α_c(fit_alpha_c) cross-lineage 일치도 — H1에서 α는 robust quantity였음(전역 ρ 0.88). 대조군.

MultiVelo lag sign은 구조적(sw2>sw1 항상 양수)이라 방향성 분석 제외, magnitude rank만.

실행: conda run -n scv-preprocess python pipeline/.../scripts/p3_lineage_refit.py
출력: results/lineage_refit.md, results/lineage_refit_pairs.csv
"""
from __future__ import annotations
import sys
from itertools import combinations
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import p1_config as p1
import p2_config as cfg

REFIT_DIR = cfg.RESULTS / "lineage_refit"
MIN_OVERLAP = 15   # 쌍별 Spearman 최소 공통 gene


def load_lineage_lags():
    """slug_genes.csv → {lineage: DataFrame(lag, alpha_c)} (lag>0만 의미, magnitude 사용)."""
    out = {}
    for csv in sorted(REFIT_DIR.glob("*_genes.csv")):
        slug = csv.name.replace("_genes.csv", "")
        d = pd.read_csv(csv, index_col=0)
        if "fit_t_sw1" not in d or "fit_t_sw2" not in d:
            continue
        lag = (d["fit_t_sw2"] - d["fit_t_sw1"])
        df = pd.DataFrame({"lag": lag, "alpha_c": d.get("fit_alpha_c")})
        df = df[df["lag"].notna()]
        out[slug] = df
    return out


def pairwise_spearman(lags, col):
    rows = []
    for a, b in combinations(sorted(lags), 2):
        da, db = lags[a][col].dropna(), lags[b][col].dropna()
        shared = da.index.intersection(db.index)
        if len(shared) < MIN_OVERLAP:
            rows.append(dict(lin_a=a, lin_b=b, n=len(shared), rho=np.nan, p=np.nan))
            continue
        rho, p = spearmanr(da.loc[shared], db.loc[shared])
        rows.append(dict(lin_a=a, lin_b=b, n=len(shared), rho=rho, p=p))
    return pd.DataFrame(rows)


def main():
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    if not REFIT_DIR.exists() or not list(REFIT_DIR.glob("*_genes.csv")):
        print(f"per-lineage fit CSV 없음 ({REFIT_DIR}) — p2_multivelo_perlineage.py 먼저 실행"); return 1

    lags = load_lineage_lags()
    L = ["# P3 — per-lineage refit lag 일치도 (진짜 within-lineage H1)", "",
         "> p2_multivelo_perlineage.py: 각 terminal lineage를 root(HSC/MPP)∪L 세포로 **따로 fit**.",
         "> lineage_lag.md(전역 fit + dominant-귀속)을 진짜 per-lineage fit으로 대체.",
         "> MultiVelo lag = fit_t_sw2−fit_t_sw1; sign은 구조적(항상 양수)이라 magnitude rank만 평가.", ""]

    # A. lineage별 분포
    L += ["## A. lineage별 lag 분포 (per-lineage refit)", "",
          "| lineage | n_gene | median_lag | mean_lag | IQR_low | IQR_high | median_α_c |",
          "|---|---|---|---|---|---|---|"]
    name_map = {}
    for slug, df in lags.items():
        # slug → 원래 라벨 복원(표시용): 'Baso-Eo-Mast'→'Baso/Eo/Mast'
        disp = slug
        is_rare = any(r.replace("/", "-").replace(" ", "") == slug for r in p1.RARE_LINEAGES)
        name_map[slug] = disp
        lag = df["lag"]
        ac = df["alpha_c"].dropna() if "alpha_c" in df else pd.Series(dtype=float)
        rare = " ⚠️rare" if is_rare else ""
        acm = f"{ac.median():.3f}" if len(ac) else "—"
        L.append(f"| {disp}{rare} | {len(lag)} | {lag.median():.2f} | {lag.mean():.2f} | "
                 f"{lag.quantile(.25):.2f} | {lag.quantile(.75):.2f} | {acm} |")
    L.append("")

    # B. cross-lineage lag magnitude 일치도
    pl = pairwise_spearman(lags, "lag")
    L += ["## B. cross-lineage lag magnitude 일치도 (Spearman rank)", "",
          "> 같은 gene의 lag이 분화경로(lineage)와 무관하게 robust한가? = gene-intrinsic 검정.",
          "", "| lineage A | lineage B | n_shared | Spearman ρ | p |", "|---|---|---|---|---|"]
    for _, r in pl.iterrows():
        rho = f"{r['rho']:.3f}" if pd.notna(r["rho"]) else "n/a"
        pp = f"{r['p']:.2g}" if pd.notna(r["p"]) else "—"
        L.append(f"| {r['lin_a']} | {r['lin_b']} | {int(r['n'])} | {rho} | {pp} |")
    valid = pl["rho"].dropna()
    if len(valid):
        L += ["", f"- **요약**: 쌍별 ρ median={valid.median():.3f}, "
                  f"range [{valid.min():.3f}, {valid.max():.3f}], "
                  f"양수 쌍 {(valid>0).sum()}/{len(valid)}."]
    L.append("")

    # D. α_c cross-lineage 일치도 (대조군)
    if all("alpha_c" in df and df["alpha_c"].notna().any() for df in lags.values()):
        pa = pairwise_spearman({k: v.assign(alpha_c=v["alpha_c"]) for k, v in lags.items()}, "alpha_c")
        va = pa["rho"].dropna()
        L += ["## D. α_c cross-lineage 일치도 (대조군: H1에서 α 계열은 robust)", "",
              "| lineage A | lineage B | n_shared | Spearman ρ | p |", "|---|---|---|---|---|"]
        for _, r in pa.iterrows():
            rho = f"{r['rho']:.3f}" if pd.notna(r["rho"]) else "n/a"
            pp = f"{r['p']:.2g}" if pd.notna(r["p"]) else "—"
            L.append(f"| {r['lin_a']} | {r['lin_b']} | {int(r['n'])} | {rho} | {pp} |")
        if len(va):
            L += ["", f"- **요약**: α_c 쌍별 ρ median={va.median():.3f} "
                      f"(lag {valid.median():.3f}와 비교 — α_c가 더 robust하면 H1 패턴 재현).", ""]

    # C. per-lineage refit vs 전역 fit
    glob_csv = cfg.RESULTS / "multivelo_genes.csv"
    if glob_csv.exists():
        g = pd.read_csv(glob_csv, index_col=0)
        glag = (g["fit_t_sw2"] - g["fit_t_sw1"]).dropna()
        L += ["## C. per-lineage refit vs 전역 fit lag (Spearman)", "",
              "> per-lineage fit이 전역 fit과 얼마나 다른가? (낮으면 전역 fit이 lineage 신호를 뭉갬)",
              "", "| lineage | n_shared | Spearman ρ | p |", "|---|---|---|---|"]
        for slug, df in lags.items():
            shared = df.index.intersection(glag.index)
            if len(shared) < MIN_OVERLAP:
                L.append(f"| {slug} | {len(shared)} | n/a | — |"); continue
            rho, p = spearmanr(df["lag"].loc[shared], glag.loc[shared])
            L.append(f"| {slug} | {len(shared)} | {rho:.3f} | {p:.2g} |")
        L.append("")

    # 결론 자동 판정
    if len(valid):
        verdict = ("lag은 lineage 간에도 일치(robust)" if valid.median() > 0.4
                   else "lag은 lineage 간에도 비robust(gene-intrinsic 아님)" if valid.median() < 0.2
                   else "lag cross-lineage 일치도 약함(경계)")
        L += ["## 결론", "",
              f"- cross-lineage lag magnitude ρ median = **{valid.median():.3f}** → **{verdict}**.",
              "- 전역 3-way H1(cross-method lag 무상관)에 더해, within-method cross-lineage 축에서도 "
              "lag 일치도를 평가 → H1(lag 비robust) 강건성 검정.", ""]

    out_md = cfg.RESULTS / "lineage_refit.md"
    out_md.write_text("\n".join(L), encoding="utf-8")
    pl.to_csv(cfg.RESULTS / "lineage_refit_pairs.csv", index=False)
    print("\n".join(L))
    print(f"\n✓ → {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
