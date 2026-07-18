#!/usr/bin/env python3
"""p6_curvature_tertile_validation.py — advisor 게이트 판별 테스트.

문제(advisor 2026-07-18): "곡률이 측정검증을 예측한다"의 make-or-break로 돌린
stiffness_predicts_validation.md는 *파라미터 간* 랭킹(α≫γ)만 검정했다(외부 ground truth가
α·γ 둘뿐 → n=2, 점 2개는 항상 단조). 진짜 주장은 *파라미터 내, 유전자 간*(n=수백):
  "per-gene 곡률(강성)이 높을수록 그 유전자의 fit rate가 실측과 더 잘 맞는다."

설계(method 일관): 강성 kap_*는 MultiVelo 목적함수로 쟀으므로(p3_profile_likelihood),
검증도 MultiVelo의 fit rate로 한다.
  α leg: MultiVelo fit_alpha vs K562 TT-seq 합성율(Part B), 유전자를 kap_alpha 3분위로 나눠
         각 분위 내 Spearman(fit_alpha, synth) 상승 여부.
  γ leg: MultiVelo fit_gamma vs MOLM13 실측 분해율 k_deg(Part A, 가장 깨끗한 reference),
         kap_gamma 3분위로 나눠 고강성 분위가 회복(+)하고 저강성이 안 되는지.
판정: ρ_high − ρ_low 의 bootstrap 95% CI가 0을 (양으로) 배제하면 "곡률→검증" 지지.
비고: 헤드라인의 γ 역방향(−0.224)은 scVelo(rna_only) γ였다 — 그 γ의 per-gene 곡률은 우리가
안 쟀으므로(kap은 MultiVelo) tertile 불가. 참고로 rna_only γ×MOLM13 overall만 병기한다.

실행: conda run --no-capture-output -n scv-preprocess python -u scripts/p6_curvature_tertile_validation.py
산출: results/curvature_tertile_validation.csv + stdout 요약
"""
import numpy as np, pandas as pd
from scipy import stats
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"; DATA = ROOT / "data"
RNG = np.random.default_rng(20260718); B = 10000

HK = set(l.strip() for l in (DATA / "housekeeping.txt").read_text().splitlines() if l.strip())


def load_col(path, col):
    df = pd.read_csv(path)
    s = df.set_index("gene")[col].dropna()
    s = s[s > 0]
    return s[~s.index.duplicated()]


def load_measure(path, col):
    df = pd.read_csv(path)
    s = df.set_index("gene")[col].dropna()
    s = s[s > 0]
    return s.groupby(level=0).median()


def boot_rho(x, y, b=B):
    n = len(x); rho0 = stats.spearmanr(x, y).statistic
    rhos = np.empty(b); idx = np.arange(n)
    for i in range(b):
        s = RNG.choice(idx, n, replace=True)
        rhos[i] = stats.spearmanr(x[s], y[s]).statistic
    lo, hi = np.nanpercentile(rhos, [2.5, 97.5])
    return float(rho0), float(lo), float(hi)


def tertile_test(name, fit, meas, kap, sign, rows):
    """fit,meas,kap: gene-indexed Series. sign=+1 (검증=양), MOLM13 k_deg는 +.
    유전자를 kap 3분위로 나눠 각 분위 내 Spearman(fit,meas)."""
    genes = fit.index.intersection(meas.index).intersection(kap.index)
    genes = genes.difference(HK)
    f = fit.loc[genes].astype(float); m = meas.loc[genes].astype(float); k = kap.loc[genes].astype(float)
    k = k.replace([np.inf, -np.inf], np.nan).dropna()
    genes = k.index; f = f.loc[genes]; m = m.loc[genes]
    N = len(genes)
    print(f"\n===== {name} =====  n(공통, non-HK, 유한 kap) = {N}")

    ro, lo, hi = boot_rho(f.values, m.values)
    print(f"  overall Spearman(fit,meas) = {ro:+.3f}  CI[{lo:+.3f},{hi:+.3f}]  (검증방향 부호=+)")
    rows.append(dict(leg=name, bin="overall", n=N, rho=round(ro,3), ci_lo=round(lo,3), ci_hi=round(hi,3)))

    # 3분위 (n 작으면 2분위로 폴백)
    nbin = 3 if N >= 90 else 2
    labels = (["low","mid","high"] if nbin==3 else ["low","high"])
    try:
        qb = pd.qcut(k, nbin, labels=labels, duplicates="drop")
    except ValueError:
        qb = pd.qcut(k.rank(method="first"), nbin, labels=labels)
    perbin = {}
    for lab in labels:
        gsub = qb.index[qb == lab]
        if len(gsub) < 10:
            print(f"  [{lab}] n={len(gsub)} <10 스킵"); continue
        fr = f.loc[gsub].values; mr = m.loc[gsub].values
        r, l, h = boot_rho(fr, mr)
        kmed = float(k.loc[gsub].median())
        perbin[lab] = (gsub, r, l, h)
        print(f"  [{lab:4}] n={len(gsub):3}  kap_med={kmed:+6.2f}  Spearman(fit,meas)={r:+.3f}  CI[{l:+.3f},{h:+.3f}]")
        rows.append(dict(leg=name, bin=lab, n=len(gsub), kap_med=round(kmed,2),
                         rho=round(r,3), ci_lo=round(l,3), ci_hi=round(h,3)))

    # 판정: ρ_high − ρ_low bootstrap CI (분위 내 재표집)
    if "low" in perbin and "high" in perbin:
        glo, rlo, *_ = perbin["low"]; ghi, rhi, *_ = perbin["high"]
        flo, mlo = f.loc[glo].values, m.loc[glo].values
        fhi, mhi = f.loc[ghi].values, m.loc[ghi].values
        nlo, nhi = len(glo), len(ghi); diffs = np.empty(B)
        ilo, ihi = np.arange(nlo), np.arange(nhi)
        for i in range(B):
            slo = RNG.choice(ilo, nlo, replace=True); shi = RNG.choice(ihi, nhi, replace=True)
            diffs[i] = stats.spearmanr(fhi[shi], mhi[shi]).statistic - stats.spearmanr(flo[slo], mlo[slo]).statistic
        dlo, dhi = np.nanpercentile(diffs, [2.5, 97.5]); dpt = rhi - rlo
        frac = float((diffs > 0).mean())
        verdict = "지지(CI 0배제)" if dlo > 0 else ("경향" if frac > 0.9 else "미지지")
        print(f"  >>> ρ_high−ρ_low = {dpt:+.3f}  CI[{dlo:+.3f},{dhi:+.3f}]  P(diff>0)={frac:.3f}  → {verdict}")
        rows.append(dict(leg=name, bin="high_minus_low", n=nlo+nhi, rho=round(dpt,3),
                         ci_lo=round(float(dlo),3), ci_hi=round(float(dhi),3), frac_gt0=round(frac,3), verdict=verdict))
        return verdict
    return "분위부족"


def main():
    stiff = pd.read_csv(RES / "stiffness_all_params.csv").set_index("gene")
    kap_a = stiff["kap_alpha"]; kap_g = stiff["kap_gamma"]
    rows = []

    # ---- α leg (양성 끝): MultiVelo fit_alpha vs K562 합성율, kap_alpha 3분위 ----
    fit_a = load_col(RES / "multivelo_genes.csv", "fit_alpha")
    synth = load_measure(DATA / "k562_ttseq_synthrate.csv", "synth_rate")
    va = tertile_test("ALPHA (MultiVelo α vs K562 synth | bin=kap_alpha)", fit_a, synth, kap_a, +1, rows)

    # ---- γ leg (흐릿 끝): MultiVelo fit_gamma vs MOLM13 k_deg, kap_gamma 3분위 ----
    fit_g = load_col(RES / "multivelo_genes.csv", "fit_gamma")
    thalf = load_measure(DATA / "halflife_molm13.csv", "t_half_h")
    kdeg = (np.log(2) / thalf).rename("k_deg")   # 검증=양(+): γ 클수록 분해 빠름
    vg = tertile_test("GAMMA (MultiVelo γ vs MOLM13 k_deg | bin=kap_gamma)", fit_g, kdeg, kap_g, +1, rows)

    # ---- 참고: 헤드라인의 scVelo γ×MOLM13 overall(−0.224 재현) — tertile 불가(kap은 MV) ----
    try:
        fit_g_sc = load_col(RES / "rna_only_dynamical_genes.csv", "fit_gamma")
        gsc = fit_g_sc.index.intersection(kdeg.index).difference(HK)
        rsc, lsc, hsc = boot_rho(fit_g_sc.loc[gsc].values.astype(float), kdeg.loc[gsc].values.astype(float))
        print(f"\n[참고] scVelo(rna_only) γ vs MOLM13 k_deg overall = {rsc:+.3f} CI[{lsc:+.3f},{hsc:+.3f}] "
              f"(n={len(gsc)}; 헤드라인 −0.224 재현. 이 γ의 per-gene 곡률은 미측정 → tertile 불가)")
        rows.append(dict(leg="GAMMA_scVelo_ref", bin="overall", n=len(gsc), rho=round(rsc,3),
                         ci_lo=round(lsc,3), ci_hi=round(hsc,3)))
    except Exception as e:
        print(f"[참고] scVelo γ ref 스킵: {e}")

    df = pd.DataFrame(rows)
    out = RES / "curvature_tertile_validation.csv"; df.to_csv(out, index=False)
    print(f"\nwrote {out}")
    print("\n===== 판정 요약 =====")
    print(f"  α leg (곡률→검증): {va}")
    print(f"  γ leg (곡률→검증): {vg}")
    print("  해석: α·γ 모두 high분위가 low분위보다 유의하게 잘 맞으면 '곡률이 신뢰를 예측'을 n=수백에서 입증.")
    print("        아니면 헤드라인을 신뢰 결정지도로 리포지셔닝(advisor 분기).")


if __name__ == "__main__":
    main()
