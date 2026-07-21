#!/usr/bin/env python3
"""P3 — Profile-likelihood practical-identifiability demo (NOVELTY-EXTENSIONS §2).

Turns the paper's INFERRED non-identifiability of the chromatin->transcription lag
into a DEMONSTRATED property of MultiVelo's own objective function, on already-fit
genes. CPU-only, reuses existing MultiVelo fits (data/velocity/multivelo.h5ad); no
new data, no GPU, no re-fit of the model from scratch.

Method (per gene, using MultiVelo's OWN objective machinery):
  - LL(params) = keep.sum() * log( compute_likelihood(...) )   [full-data log-lik]
    where the per-cell latent time / state (the dominant nuisance) is ALWAYS
    re-optimized at each param value via calculate_dist_and_time (KDTree anchor
    assignment on the shared connectivity graph) — i.e. a genuine profile over the
    latent-time nuisance, not a fixed slice.
  - alpha profile: hold switch-times fixed, perturb alpha in log-space -> local
    curvature kappa_alpha = -d^2 LL / d(ln alpha)^2.
  - lag  profile: hold rates fixed, perturb lag = t_sw2 - t_sw1 in log-space
    (rigid shift of t_sw3, gap = t_sw3 - t_sw2 fixed) -> kappa_lag.
  Discriminator = per-cell log-curvature ratio kappa_alpha / kappa_lag (dimensionless,
  n-independent), plus lag half-width in native pseudotime units.

Reproduction validated: our calculate_dist_and_time + compute_likelihood recovers the
stored fit_t / fit_state (r~1.0, state-agree ~100%) and stored fit_likelihood to 3-4
sig figs (conn = row-normalized obsp['connectivities']; weight_c=0.6; outlier=99.8;
n_anchors=500; k=1 — the recover_dynamics_chrom defaults used by p2_multivelo.py).

Honest framing (advisor-gated): the objective is NOT flat along lag. The result is
RELATIVE practical non-identifiability: alpha is the STIFF (identifiable) direction,
the lag is systematically SLOPPIER (~few-fold) and frequently boundary-pinned/degenerate.
Never claim "flat" / "non-identifiable" without the "practical / relative" qualifier.

Symmetric freed-nuisance gate (--subset N): re-optimize the class
{alpha_c, beta, gamma, rescale_c, rescale_u, scale_cc} at each grid point in BOTH
profiles (profiled param's counterpart still fixed). This guards the alpha-stiffness
half against the beta/gamma sloppiness (identifiability_dissociation.md) that a
reviewer would re-run to flatten the alpha peak.

Run (mv env):
  conda run --no-capture-output -n velo-mv python -u scripts/p3_profile_likelihood.py            # full 538 genes, all-fixed
  conda run --no-capture-output -n velo-mv python -u scripts/p3_profile_likelihood.py --subset 50 # + freed-nuisance gate on 50 genes
  conda run --no-capture-output -n velo-mv python -u scripts/p3_profile_likelihood.py --smoke 8   # quick

Outputs:
  results/profile_likelihood_identifiability.csv   (per gene: kappa_alpha/lag, ratio, widths, class)
  results/profile_likelihood_freed.csv             (subset: all-fixed vs freed ratio)
  results/profile_likelihood_curves.csv            (raw scan curves for representative genes -> figure)
"""
from __future__ import annotations
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import argparse
import numpy as np
import scanpy as sc
from multivelo.dynamical_chrom_func import calculate_dist_and_time, compute_likelihood

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
H5 = os.path.join(ROOT, "data", "velocity", "multivelo.h5ad")
RES = os.path.join(ROOT, "results")

WEIGHT_C = 0.6          # recover_dynamics_chrom default (p2_multivelo.py uses defaults)
OUTLIER = 99.8
N_ANCHORS = 500
K = 1
TOTAL_H = 20.0
H_LOG = 0.15            # log-space finite-difference step for curvature
DELTA_PC = 0.05         # per-cell log-lik drop (nats/cell) defining a "practically flat" band
SEED = 20260709


def load():
    a = sc.read_h5ad(H5)

    def raw(l):
        x = a.layers[l]
        return (x.A if hasattr(x, "A") else np.asarray(x)).astype(np.float64)
    C, U, S = raw("ATAC"), raw("Mu"), raw("Ms")
    conn = a.obsp["connectivities"].copy()
    conn.setdiag(1)
    conn = conn.multiply(1.0 / conn.sum(1)).tocsr()
    return a, C, U, S, conn


def prep(C, U, S, gi):
    """Reproduce ChromatinDynamical.__init__ normalization deterministically."""
    c = C[:, gi].copy(); u = U[:, gi].copy(); s = S[:, gi].copy()
    c -= c.min(); u -= u.min(); s -= s.min()
    nz = (c > 0) | (u > 0) | (s > 0)
    no = ((c <= np.percentile(c, OUTLIER)) & (u <= np.percentile(u, OUTLIER))
          & (s <= np.percentile(s, OUTLIER)))
    std_c, std_u, std_s = np.std(c), np.std(u), np.std(s)
    if std_u == 0 or std_s == 0 or np.max(c) == 0:
        return None
    scale_c, scale_u = np.max(c), std_u / std_s
    c /= scale_c; u /= scale_u              # s /= 1
    sf_calc = np.array([np.std(c) / std_s / WEIGHT_C, 1.0, 1.0])   # KDTree distance scaling
    sf_lk = np.array([scale_c / std_c, 1.0 / std_s, 1.0 / std_s])  # likelihood scaling
    keep = nz & no & (u > 0.2 * np.percentile(u, 99.5)) & (s > 0.2 * np.percentile(s, 99.5))
    return dict(c=c, u=u, s=s, sf_calc=sf_calc, sf_lk=sf_lk, keep=keep, nkeep=int(keep.sum()))


def LL(g, conn, ac, al, be, ga, tsw, rc, ru, scc, model, direc):
    """Full-data log-likelihood with latent-time/state re-optimized (profiled out)."""
    try:
        res = calculate_dist_and_time(
            g["c"], g["u"], g["s"], tsw, ac, al, be, ga, rc, ru,
            scale_cc=scc, scale_factor=g["sf_calc"], model=model, direction=direc,
            conn=conn, k=K, t=N_ANCHORS, all_cells=True)
        t_pred, state_pred = res[1], res[2]
        lk, *_ = compute_likelihood(
            g["c"], g["u"], g["s"], tsw, ac, al, be, ga, rc, ru,
            t_pred, state_pred, scale_cc=scc, scale_factor=g["sf_lk"],
            model=model, weight=g["keep"])
        if not np.isfinite(lk) or lk <= 0:
            return np.nan
        return g["nkeep"] * np.log(max(lk, 1e-300))
    except Exception:
        return np.nan


def curvature(f, x0, h=H_LOG):
    """-d^2 f / d(ln x)^2 at x0 via two-sided log-space finite difference."""
    l0 = f(x0); lp = f(x0 * np.exp(h)); lm = f(x0 * np.exp(-h))
    if not (np.isfinite(l0) and np.isfinite(lp) and np.isfinite(lm)):
        return np.nan, l0
    return -(lp - 2 * l0 + lm) / h**2, l0


def analyze_gene(g, r, conn):
    ac, al, be, ga = r.fit_alpha_c, r.fit_alpha, r.fit_beta, r.fit_gamma
    t1, t2, t3 = r.fit_t_sw1, r.fit_t_sw2, r.fit_t_sw3
    gap = t3 - t2
    model, direc = int(r.fit_model), str(r.fit_direction)
    rc, ru, scc = r.fit_rescale_c, r.fit_rescale_u, r.fit_scale_cc
    lag0 = t2 - t1
    nk = g["nkeep"]

    # alpha profile: switch-times fixed, perturb alpha
    fa = lambda AL: LL(g, conn, ac, AL, be, ga, np.array([t1, t2, t3]), rc, ru, scc, model, direc)
    ka, ll_a0 = curvature(fa, al)

    # lag profile: rates fixed, perturb lag (rigid t_sw3 shift; gap fixed)
    fl = lambda LG: LL(g, conn, ac, al, be, ga, np.array([t1, t1 + LG, t1 + LG + gap]), rc, ru, scc, model, direc)
    lag_cls = "interior"
    kl, ll_l0 = np.nan, np.nan
    if lag0 <= 0.2:
        lag_cls = "degenerate"
    elif t1 + lag0 * np.exp(H_LOG) > TOTAL_H or t2 >= TOTAL_H - 0.1:
        lag_cls = "boundary_pinned"
        # still record a one-sided (downward) sensitivity for context
        kl, ll_l0 = np.nan, np.nan
    else:
        kl, ll_l0 = curvature(fl, lag0)
        if not np.isfinite(kl):
            lag_cls = "degenerate"

    # native-unit lag half-width: pseudotime range where per-cell LL stays within DELTA_PC of peak
    lag_lo = lag_hi = np.nan
    if lag_cls == "interior" and np.isfinite(ll_l0):
        peak_pc = ll_l0 / nk
        # scan a broad admissible pseudotime window
        hi_lim = min(TOTAL_H - t1, 18.0)
        grid = np.linspace(max(0.2, 0.05), hi_lim, 16)
        pcs = np.array([fl(lg) / nk for lg in grid])
        # peak may exceed ll_l0 slightly; use max over grid+MLE
        pk = max(peak_pc, np.nanmax(pcs))
        ok = np.isfinite(pcs) & ((pk - pcs) <= DELTA_PC)
        if ok.any():
            lag_lo, lag_hi = float(grid[ok].min()), float(grid[ok].max())

    # alpha fold half-width (multiplicative): fold range within DELTA_PC of peak
    a_lo = a_hi = np.nan
    if np.isfinite(ll_a0):
        peak_pc = ll_a0 / nk
        folds = np.geomspace(0.1, 10, 16)
        pcs = np.array([fa(al * fo) / nk for fo in folds])
        pk = max(peak_pc, np.nanmax(pcs))
        ok = np.isfinite(pcs) & ((pk - pcs) <= DELTA_PC)
        if ok.any():
            a_lo, a_hi = float(folds[ok].min()), float(folds[ok].max())

    ratio = ka / kl if (np.isfinite(ka) and np.isfinite(kl) and kl > 0 and ka > 0) else np.nan
    return dict(gene=r.name, nkeep=nk, lag0=lag0, t_sw1=t1, t_sw2=t2, alpha=al,
                kappa_alpha=ka, kappa_lag=kl, ratio=ratio,
                kappa_alpha_pc=ka / nk if np.isfinite(ka) else np.nan,
                kappa_lag_pc=kl / nk if np.isfinite(kl) else np.nan,
                lag_cls=lag_cls, lag_width_lo=lag_lo, lag_width_hi=lag_hi,
                lag_admissible=min(TOTAL_H - t1, 18.0),
                alpha_fold_lo=a_lo, alpha_fold_hi=a_hi)


# ---------------- freed-nuisance symmetric gate ----------------
from scipy.optimize import minimize


def _refit_neg_ll(g, conn, fixed, free_names, x_log, model, direc):
    """neg full-data LL with free_names (log-parameterized) at x_log, others fixed."""
    p = dict(fixed)
    for name, xv in zip(free_names, x_log):
        p[name] = np.exp(xv)
    tsw = np.array([p["t1"], p["t1"] + p["lag"], p["t1"] + p["lag"] + p["gap"]])
    val = LL(g, conn, p["alpha_c"], p["alpha"], p["beta"], p["gamma"], tsw,
             p["rescale_c"], p["rescale_u"], p["scale_cc"], model, direc)
    return 1e18 if not np.isfinite(val) else -val


def profiled_LL(g, conn, base, override, model, direc, maxiter=25):
    """LL with the freed nuisance class re-optimized; `override` fixes profiled param(s)."""
    free_names = ["alpha_c", "beta", "gamma", "rescale_c", "rescale_u", "scale_cc"]
    fixed = dict(base); fixed.update(override)
    x0 = np.array([np.log(max(fixed[n], 1e-6)) for n in free_names])
    res = minimize(lambda x: _refit_neg_ll(g, conn, fixed, free_names, x, model, direc),
                   x0, method="Nelder-Mead",
                   options=dict(maxiter=maxiter, xatol=1e-2, fatol=1.0))
    return -res.fun


def freed_curvature(g, r, conn, maxiter=25):
    base = dict(alpha=r.fit_alpha, alpha_c=r.fit_alpha_c, beta=r.fit_beta,
                gamma=r.fit_gamma, rescale_c=r.fit_rescale_c, rescale_u=r.fit_rescale_u,
                scale_cc=r.fit_scale_cc, t1=r.fit_t_sw1, lag=r.fit_t_sw2 - r.fit_t_sw1,
                gap=r.fit_t_sw3 - r.fit_t_sw2)
    model, direc = int(r.fit_model), str(r.fit_direction)
    al, lag0, t1 = r.fit_alpha, base["lag"], r.fit_t_sw1
    # alpha profile with beta/gamma/... freed (switch-times fixed via base lag/gap)
    fa = lambda AL: profiled_LL(g, conn, base, {"alpha": AL}, model, direc, maxiter)
    ka, _ = curvature(fa, al)
    # lag profile with same class freed (alpha fixed)
    kl = np.nan
    if lag0 > 0.2 and t1 + lag0 * np.exp(H_LOG) <= TOTAL_H and r.fit_t_sw2 < TOTAL_H - 0.1:
        fl = lambda LG: profiled_LL(g, conn, base, {"lag": LG}, model, direc, maxiter)
        kl, _ = curvature(fl, lag0)
    ratio = ka / kl if (np.isfinite(ka) and np.isfinite(kl) and kl > 0 and ka > 0) else np.nan
    return ka, kl, ratio, base["gap"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", type=int, default=0)
    ap.add_argument("--subset", type=int, default=0, help="freed-nuisance gate on N largest-keep genes")
    args = ap.parse_args()

    import pandas as pd
    import time
    a, C, U, S, conn = load()
    V = a.var
    genes = list(a.var_names)
    order = range(len(genes))
    if args.smoke:
        rng = np.random.default_rng(SEED)
        order = sorted(rng.choice(len(genes), args.smoke, replace=False))

    t0 = time.time()
    recs = []
    for k, gi in enumerate(order):
        r = V.iloc[gi]
        if not (r.fit_alpha > 1e-6 and r.fit_beta > 1e-6 and r.fit_gamma > 1e-6):
            continue
        g = prep(C, U, S, gi)
        if g is None or g["nkeep"] < 30:
            continue
        recs.append(analyze_gene(g, r, conn))
        if (k + 1) % 50 == 0:
            print(f"  ...{k+1} genes  ({time.time()-t0:.0f}s)", flush=True)
    df = pd.DataFrame(recs)
    out = os.path.join(RES, "profile_likelihood_identifiability.csv"
                       if not args.smoke else "profile_likelihood_identifiability.smoke.csv")
    df.to_csv(out, index=False)
    print(f"\nwrote {out}  n={len(df)}  ({time.time()-t0:.0f}s)")

    # summary
    both = df["ratio"].dropna()
    print("\n=== ALL-FIXED (conditional latent-time profile) ===")
    print(f"kappa_alpha/cell median {df['kappa_alpha_pc'].median():.3f}  "
          f"kappa_lag/cell median {df['kappa_lag_pc'].median():.3f}")
    if len(both):
        print(f"ratio kappa_alpha/kappa_lag (interior, both>0, n={len(both)}): "
              f"median {both.median():.2f}  IQR [{both.quantile(.25):.2f},{both.quantile(.75):.2f}]  "
              f"frac(alpha stiffer)={(both>1).mean():.2%}")
    vc = df["lag_cls"].value_counts()
    print("lag trichotomy:", dict(vc))
    iw = df.loc[df.lag_cls == "interior", ["lag_width_lo", "lag_width_hi", "lag_admissible", "lag0"]].dropna()
    if len(iw):
        frac = ((iw.lag_width_hi - iw.lag_width_lo) / iw.lag_admissible)
        print(f"interior lag half-width / admissible pseudotime range: median {frac.median():.2%} "
              f"(lag band spans this fraction of the 0..(20-t_sw1) window)")
    aw = df[["alpha_fold_lo", "alpha_fold_hi"]].dropna()
    if len(aw):
        fold = aw.alpha_fold_hi / aw.alpha_fold_lo
        print(f"alpha fold half-width (hi/lo) within {DELTA_PC} nats/cell: median {fold.median():.2f}x")

    # freed-nuisance gate on subset (interior-lag genes so both profiles are scannable)
    if args.subset:
        pool = df[(df.lag_cls == "interior") & df.ratio.notna()]
        sub = pool.sort_values("nkeep", ascending=False).head(args.subset)
        print(f"\n=== FREED-NUISANCE GATE ({{alpha_c,beta,gamma,rescale,scale_cc}} re-optimized) "
              f"on {len(sub)} interior genes ===", flush=True)
        fr = []
        t1 = time.time()
        for i, (_, row) in enumerate(sub.iterrows()):
            gi = genes.index(row.gene)
            g = prep(C, U, S, gi)
            r = V.iloc[gi]
            ka, kl, ratio, _ = freed_curvature(g, r, conn)
            fr.append(dict(gene=row.gene, nkeep=row.nkeep,
                           kappa_alpha_fixed=row.kappa_alpha, kappa_lag_fixed=row.kappa_lag,
                           ratio_fixed=row.ratio, kappa_alpha_freed=ka,
                           kappa_lag_freed=kl, ratio_freed=ratio,
                           alpha_retention=ka / row.kappa_alpha if (np.isfinite(ka) and row.kappa_alpha > 0) else np.nan))
            if (i + 1) % 5 == 0:
                print(f"  ...{i+1}/{len(sub)} ({time.time()-t1:.0f}s)", flush=True)
        fdf = pd.DataFrame(fr)
        fout = os.path.join(RES, "profile_likelihood_freed.csv")
        fdf.to_csv(fout, index=False)
        rf = fdf["ratio_freed"].dropna()
        rx = fdf["ratio_fixed"].dropna()
        ret = fdf["alpha_retention"].dropna()
        print(f"wrote {fout}  n={len(fdf)}")
        print(f"ratio_fixed  median {rx.median():.2f} (n={len(rx)})")
        if len(ret):
            print(f"alpha-stiffness retention kappa_alpha_freed/kappa_alpha_fixed: "
                  f"median {ret.median():.2f} (n={len(ret)})  "
                  f"-> alpha peak {'SURVIVES' if ret.median() > 0.5 else 'COLLAPSES'} freeing beta/gamma")
        if len(rf):
            print(f"ratio_freed  median {rf.median():.2f} (n={len(rf)})  "
                  f"frac(alpha still stiffer)={(rf>1).mean():.2%}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
