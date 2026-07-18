#!/usr/bin/env python3
"""p5_stiffness_all_params.py — profile-likelihood 강성(κ)을 α·α_c·β·γ 전 rate로 확장.

목적(make-or-break A): 내부 식별성(목적함수 곡률) 랭킹이 외부 측정-검증 랭킹과 일치하는가?
  - 외부검증(external_rate_validation.md): α는 실측 TT-seq 합성율 회복(+0.24~+0.29), γ는 역방향(−0.224).
  - 가설: stiff(식별 가능) 파라미터가 측정으로 검증되고, sloppy 파라미터는 안 되거나 거꾸로 → "곡률이 신뢰를 예측".
p3_profile_likelihood의 LL/curvature/load/prep 재사용(같은 MultiVelo 목적함수·latent-time 재최적화).
실행: conda run --no-capture-output -n velo-mv python -u scripts/p5_stiffness_all_params.py [--smoke N]
산출: results/stiffness_all_params.csv (gene별 per-cell κ 4종)
"""
import os, sys, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_profile_likelihood as pl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", type=int, default=0)
    args = ap.parse_args()
    import pandas as pd, time
    a, C, U, S, conn = pl.load()
    V = a.var
    names = list(a.var_names)
    order = range(len(names))
    if args.smoke:
        rng = np.random.default_rng(pl.SEED)
        order = sorted(rng.choice(len(names), args.smoke, replace=False))

    t0 = time.time(); recs = []
    for k, gi in enumerate(order):
        r = V.iloc[gi]
        if not (r.fit_alpha > 1e-6 and r.fit_beta > 1e-6 and r.fit_gamma > 1e-6 and r.fit_alpha_c > 1e-6):
            continue
        g = pl.prep(C, U, S, gi)
        if g is None or g["nkeep"] < 30:
            continue
        ac, al, be, ga = r.fit_alpha_c, r.fit_alpha, r.fit_beta, r.fit_gamma
        tsw = np.array([r.fit_t_sw1, r.fit_t_sw2, r.fit_t_sw3])
        rc, ru, scc = r.fit_rescale_c, r.fit_rescale_u, r.fit_scale_cc
        model, direc = int(r.fit_model), str(r.fit_direction)
        nk = g["nkeep"]
        # 각 rate 파라미터를 log-공간 섭동, 나머지 고정 → per-cell 곡률
        ka, _  = pl.curvature(lambda X: pl.LL(g, conn, ac, X,  be, ga, tsw, rc, ru, scc, model, direc), al)
        kac, _ = pl.curvature(lambda X: pl.LL(g, conn, X,  al, be, ga, tsw, rc, ru, scc, model, direc), ac)
        kb, _  = pl.curvature(lambda X: pl.LL(g, conn, ac, al, X,  ga, tsw, rc, ru, scc, model, direc), be)
        kg, _  = pl.curvature(lambda X: pl.LL(g, conn, ac, al, be, X,  tsw, rc, ru, scc, model, direc), ga)
        recs.append(dict(gene=names[gi], nkeep=nk,
                         kap_alpha=ka/nk, kap_alpha_c=kac/nk, kap_beta=kb/nk, kap_gamma=kg/nk))
        if (k + 1) % 50 == 0:
            print(f"  ...{k+1} genes ({time.time()-t0:.0f}s)", flush=True)

    df = pd.DataFrame(recs)
    out = os.path.join(pl.RES, "stiffness_all_params.csv" if not args.smoke else "stiffness_all_params.smoke.csv")
    df.to_csv(out, index=False)
    print(f"\nwrote {out}  n={len(df)}  ({time.time()-t0:.0f}s)\n")

    print("=== 파라미터별 강성(median per-cell κ; 높을수록 stiff=식별 가능) ===")
    meds = {}
    for p in ["kap_alpha", "kap_alpha_c", "kap_beta", "kap_gamma"]:
        v = df[p].replace([np.inf, -np.inf], np.nan).dropna()
        meds[p] = v.median()
        print(f"  {p:12} median={v.median():+.4f}  (n={len(v)}, frac>0={(v>0).mean():.1%})")
    print("\n=== 식별성 랭킹(stiff→sloppy) ===")
    for p, m in sorted(meds.items(), key=lambda x: -x[1]):
        print(f"  {p:12} {m:+.4f}")
    print("\n외부 측정-검증(external_rate_validation.md):")
    print("  α = 실측 합성율 회복 (+0.24~+0.29, CI 0 배제)  |  γ = 역방향 (−0.224, CI 0 배제)")
    print("→ α가 최고 stiff & γ가 최저(또는 음/무)면: **내부 식별성 랭킹 = 외부 측정검증 랭킹** (곡률이 신뢰를 예측).")


if __name__ == "__main__":
    main()
