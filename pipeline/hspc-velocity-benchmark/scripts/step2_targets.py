#!/usr/bin/env python3
"""STEP2 (EXPLORATORY) — 타깃(α consensus / lag consensus / lag_reprod) 어셈블.

설계 §2a. Part1(GSE209878) method별 fit에서 두 kinetic 타깃을 gene-level consensus로 만든다.
per-method 정의는 p3_concordance.py의 canonical 정의를 그대로 승계:
  α         : multivelo fit_alpha, multivelovae vae_alpha, floor(rna_only) fit_alpha
  lag 크기  : multivelo |t_sw2−t_sw1|, moflow |cs_lag_median|, crakvelo |cs_lag_median|,
              multivelovae |1/vae_alpha_c − 1/vae_alpha|

⚠️ clean-gate 규율(FINDINGS §1): MultiVelo lag은 구조적 양수 → **크기(magnitude) rank만** 사용, sign 미사용.
consensus는 스케일 상이 → **percentile-rank 평균**(median 아님, advisor 지적).

타깃:
  alpha_consensus   : α percentile-rank 평균 (≥2 method)   ← 재현 신호(ρ0.88)
  lag_consensus     : lag 크기 percentile-rank 평균 (≥2 method) ← 비재현 신호(ρ0.04)
  lag_reprod        : lag 크기 percentile-rank의 method간 SD의 음수 (≥3 method) ← A3 타깃
                      (높을수록 method간 lag 크기 순위가 일관 = 재현적)
  + per-method 원값 컬럼 유지

실행: conda run -n scv-preprocess python scripts/step2_targets.py
출력: results/step2/targets_alpha_lag.csv
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
OUT = RES / "step2"


def load(name):
    p = RES / name
    return pd.read_csv(p, index_col=0) if p.exists() else None


def pct_rank(s):
    return s.rank(pct=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mv = load("multivelo_genes.csv")
    vae = load("multivelovae_genes.csv")
    fl = load("rna_only_dynamical_genes.csv")
    mo = load("moflow_genes.csv")
    ck = load("crakvelo_genes.csv")

    # --- α per method (raw) ---
    alpha = {}
    if mv is not None:
        m = mv[mv["fit_likelihood"].notna()] if "fit_likelihood" in mv else mv
        alpha["alpha_mv"] = m["fit_alpha"].astype(float)
    if vae is not None and "vae_alpha" in vae:
        alpha["alpha_vae"] = vae["vae_alpha"].astype(float)
    if fl is not None and "fit_alpha" in fl:
        f = fl[fl["fit_likelihood"].notna()] if "fit_likelihood" in fl else fl
        alpha["alpha_floor"] = f["fit_alpha"].astype(float)
    A = pd.DataFrame(alpha)

    # --- lag magnitude per method (raw) ---
    lag = {}
    if mv is not None:
        m = mv[mv["fit_likelihood"].notna()] if "fit_likelihood" in mv else mv
        lag["lag_mv"] = (m["fit_t_sw2"] - m["fit_t_sw1"]).abs().astype(float)
    if mo is not None and "cs_lag_median" in mo:
        lag["lag_moflow"] = mo["cs_lag_median"].abs().astype(float)
    if ck is not None and "cs_lag_median" in ck:
        lag["lag_crak"] = ck["cs_lag_median"].abs().astype(float)
    if vae is not None and {"vae_alpha_c", "vae_alpha"} <= set(vae.columns):
        lag["lag_vae"] = (1.0 / vae["vae_alpha_c"].clip(1e-6)
                          - 1.0 / vae["vae_alpha"].clip(1e-6)).abs().astype(float)
    Lg = pd.DataFrame(lag)

    # --- consensus via percentile-rank average ---
    Ar = A.apply(pct_rank)
    Lr = Lg.apply(pct_rank)
    out = pd.DataFrame(index=sorted(set(A.index) | set(Lg.index)))
    out = out.join(A).join(Lg)
    out["n_alpha_methods"] = Ar.notna().sum(1).reindex(out.index)
    out["n_lag_methods"] = Lr.notna().sum(1).reindex(out.index)
    out["alpha_consensus"] = Ar.mean(1).where(Ar.notna().sum(1) >= 2).reindex(out.index)
    out["lag_consensus"] = Lr.mean(1).where(Lr.notna().sum(1) >= 2).reindex(out.index)
    # lag_reprod = -SD of per-method percentile-ranks (≥3 methods) → 높을수록 재현적
    reprod = (-Lr.std(1, ddof=0)).where(Lr.notna().sum(1) >= 3)
    out["lag_reprod"] = reprod.reindex(out.index)

    out.to_csv(OUT / "targets_alpha_lag.csv")
    print(f"[tgt] ✓ targets {out.shape} → step2/targets_alpha_lag.csv", flush=True)
    print(f"[tgt] α methods: {list(A.columns)} | lag methods: {list(Lg.columns)}", flush=True)
    print(f"[tgt] alpha_consensus n={out['alpha_consensus'].notna().sum()} "
          f"(≥2 method), lag_consensus n={out['lag_consensus'].notna().sum()} (≥2), "
          f"lag_reprod n={out['lag_reprod'].notna().sum()} (≥3)", flush=True)
    # sanity: 승계 재현 신호 확인 — α method간 pairwise Spearman
    from scipy.stats import spearmanr
    cols = list(A.columns)
    print("[tgt] α cross-method Spearman (재현 신호 sanity, FINDINGS ρ~0.88):", flush=True)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            sh = A[[cols[i], cols[j]]].dropna()
            if len(sh) >= 10:
                r, _ = spearmanr(sh[cols[i]], sh[cols[j]])
                print(f"    {cols[i]}×{cols[j]}: ρ={r:+.3f} (n={len(sh)})", flush=True)
    lcols = list(Lg.columns)
    print("[tgt] lag 크기 cross-method Spearman (비재현 sanity):", flush=True)
    for i in range(len(lcols)):
        for j in range(i + 1, len(lcols)):
            sh = Lg[[lcols[i], lcols[j]]].dropna()
            if len(sh) >= 10:
                r, _ = spearmanr(sh[lcols[i]], sh[lcols[j]])
                print(f"    {lcols[i]}×{lcols[j]}: ρ={r:+.3f} (n={len(sh)})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
