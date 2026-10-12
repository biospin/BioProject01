#!/usr/bin/env python3
"""P5 — Robustness checks not covered by the current appendices. Existing fits only, no refitting.

  R1 harmonized α-vs-lag: one method pair, one common gene set, every lag
     convention side by side, each with a paired Δρ against α on the SAME bootstrap draw.
  R2 abundance-residualized concordance: partial Spearman of the
     cross-method pair given HSPC mean expression (rank-residualized).
  R3 dependence-aware bootstrap: genes resampled in co-expression modules
     (hierarchical clusters of the Ms gene-gene correlation) instead of independently.
  R4 curvature coordinates: the profile curvatures are in ln-parameter units as submitted;
     re-express the lag linearly in pseudotime-horizon units as a sensitivity.
  R5 MultiVelo lag definition: priming interval fit_t_sw1 (MultiVelo's Δt_priming) against
     the coupled-on length fit_t_sw2 − fit_t_sw1 used in the paper.

Definitions reused verbatim from p3_identifiability_dissociation.py:
  MultiVelo α = fit_alpha, α_c = fit_alpha_c, lag = fit_t_sw2 − fit_t_sw1 (structural sign)
  MultiVeloVAE α = vae_alpha, α_c = vae_alpha_c, lag = 1/vae_alpha_c − 1/vae_alpha (rate proxy)
  MoFlow lag = cs_lag_median (DTW, sign-variable)

실행: ~/miniforge3/envs/scv-preprocess/bin/python scripts/p17_post_review_robustness.py [--selftest]
출력: results/post_review_robustness.gen.md, results/post_review_robustness.csv
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
H5 = HERE / "data" / "velocity" / "multivelo.h5ad"
B = 10000
SEED = 20261010
TOTAL_H = 20.0  # MultiVelo pseudotime horizon, p3_profile_likelihood.py L68


# ---------------------------------------------------------------- estimators
def spear(a, b):
    return float(np.corrcoef(rankdata(a), rankdata(b))[0, 1])


def rank_resid(x, z):
    """Residual of rank(x) after OLS on rank(z)."""
    rx, rz = rankdata(x), rankdata(z)
    Z = np.column_stack([np.ones_like(rz), rz])
    beta, *_ = np.linalg.lstsq(Z, rx, rcond=None)
    return rx - Z @ beta


def partial_spear(a, b, z):
    """Spearman partial correlation of a and b given z."""
    return float(np.corrcoef(rank_resid(a, z), rank_resid(b, z))[0, 1])


def draw_idx(rng, n, groups=None):
    """Gene bootstrap index. groups=None: iid genes. Otherwise resample whole groups."""
    if groups is None:
        return rng.integers(0, n, n)
    labels = np.unique(groups)
    members = {g: np.flatnonzero(groups == g) for g in labels}
    pick = rng.choice(labels, size=len(labels), replace=True)
    return np.concatenate([members[g] for g in pick])


def boot_pair(stat_a, stat_b, n, rng, groups=None, b=B):
    """Paired bootstrap of stat_a, stat_b and their difference on the SAME index draw.
    stat_*: callable(idx) -> float. Returns point estimates and percentile 95% CIs."""
    full = np.arange(n)
    pa, pb = stat_a(full), stat_b(full)
    da = np.empty(b); db = np.empty(b)
    for i in range(b):
        idx = draw_idx(rng, n, groups)
        da[i] = stat_a(idx); db[i] = stat_b(idx)
    ci = lambda d: tuple(float(x) for x in np.nanpercentile(d, [2.5, 97.5]))
    return dict(a=pa, b=pb, d=pa - pb, a_ci=ci(da), b_ci=ci(db), d_ci=ci(da - db))


# ---------------------------------------------------------------- self-test
def selftest():
    """Truth-known inputs. Each check must fail on a wrong implementation."""
    rng = np.random.default_rng(0)
    n = 4000
    z = rng.normal(size=n)
    # (1) a and b share only z -> partial ≈ 0 while the raw correlation is large
    a = z + 0.3 * rng.normal(size=n); b = z + 0.3 * rng.normal(size=n)
    assert spear(a, b) > 0.8, spear(a, b)
    assert abs(partial_spear(a, b, z)) < 0.05, partial_spear(a, b, z)
    # (2) a and b share a component independent of z -> partial clearly > 0
    s = rng.normal(size=n)
    a = z + s + 0.3 * rng.normal(size=n); b = z + s + 0.3 * rng.normal(size=n)
    assert partial_spear(a, b, z) > 0.7, partial_spear(a, b, z)
    # (3) sign: anti-shared component -> negative partial
    a = z + s; b = z - s
    assert partial_spear(a, b, z) < -0.7, partial_spear(a, b, z)
    # (4) clustered data: module bootstrap CI must be wider than iid-gene CI
    k, m = 40, 25                                   # 40 modules x 25 genes
    g = np.repeat(np.arange(k), m)
    shared = np.repeat(rng.normal(size=k), m)       # module-level effect common to both
    x = shared + 0.2 * rng.normal(size=k * m); y = shared + 0.2 * rng.normal(size=k * m)
    st = lambda idx: spear(x[idx], y[idx])
    w_iid = np.diff(boot_pair(st, st, k * m, np.random.default_rng(1), None, 2000)["a_ci"])[0]
    w_mod = np.diff(boot_pair(st, st, k * m, np.random.default_rng(1), g, 2000)["a_ci"])[0]
    assert w_mod > 2 * w_iid, (w_iid, w_mod)
    # (5) module bootstrap with singleton modules equals the iid bootstrap in distribution
    w_single = np.diff(boot_pair(st, st, k * m, np.random.default_rng(1), np.arange(k * m), 2000)["a_ci"])[0]
    assert abs(w_single - w_iid) / w_iid < 0.15, (w_single, w_iid)
    # (6) paired difference of identical statistics is exactly zero
    r = boot_pair(st, st, k * m, np.random.default_rng(2), None, 200)
    assert r["d"] == 0 and r["d_ci"] == (0.0, 0.0)
    print("selftest: 6/6 passed")


# ---------------------------------------------------------------- data
def load(name):
    d = pd.read_csv(RES / name, index_col=0)
    if "fit_likelihood" in d.columns:
        d = d[d["fit_likelihood"].notna()]
    d.index = [str(x).upper() for x in d.index]
    return d[~d.index.duplicated()]


def gene_modules(genes, ks):
    """Hierarchical co-expression modules on the MultiVelo Ms layer (average linkage on 1 − r)."""
    import anndata as ad
    a = ad.read_h5ad(H5, backed="r")
    names = [str(x).upper() for x in a.var_names]
    pos = [names.index(gn) for gn in genes]
    X = np.asarray(a.layers["Ms"][:, pos].toarray() if hasattr(a.layers["Ms"], "toarray")
                   else a.layers["Ms"][:, pos], dtype=float)
    C = np.corrcoef(X.T)
    D = np.clip(1.0 - C, 0, 2); np.fill_diagonal(D, 0)
    Lk = linkage(squareform(D, checks=False), method="average")
    return {k: fcluster(Lk, t=k, criterion="maxclust") for k in ks}


# ---------------------------------------------------------------- main
def main():
    rng = np.random.default_rng(SEED)
    mv, vae, mo = load("multivelo_genes.csv"), load("multivelovae_genes.csv"), load("moflow_genes.csv")
    ab = load("coupling_per_gene.csv")["abundance"]
    rows, L = [], ["# Post-review robustness checks (machine output, do not edit)", "",
                   f"> B={B:,}, seed={SEED}, percentile 95% CIs. Existing fits only.", ""]

    def add(analysis, metric, n, point, ci):
        rows.append(dict(analysis=analysis, metric=metric, n=n, point=point, ci_lo=ci[0], ci_hi=ci[1]))
        L.append(f"| {analysis} | {metric} | {n} | {point:+.3f} | [{ci[0]:+.3f}, {ci[1]:+.3f}] |")

    # ---- shared gene set: MV ∩ VAE (the headline pair) and MV ∩ VAE ∩ MoFlow (common set)
    sh = sorted(set(mv.index) & set(vae.index))
    A, V = mv.loc[sh], vae.loc[sh]
    x = dict(
        alpha=(A.fit_alpha.values, V.vae_alpha.values),
        alpha_c=(A.fit_alpha_c.values, V.vae_alpha_c.values),
        lag_native_mag=(np.abs(A.fit_t_sw2 - A.fit_t_sw1).values,
                        np.abs(1 / V.vae_alpha_c.clip(1e-6) - 1 / V.vae_alpha.clip(1e-6)).values),
        lag_rateproxy_signed=((1 / A.fit_alpha_c.clip(1e-6) - 1 / A.fit_alpha.clip(1e-6)).values,
                              (1 / V.vae_alpha_c.clip(1e-6) - 1 / V.vae_alpha.clip(1e-6)).values),
    )
    x["lag_rateproxy_mag"] = tuple(np.abs(v) for v in x["lag_rateproxy_signed"])
    n = len(sh)
    sp = lambda key: (lambda idx: spear(x[key][0][idx], x[key][1][idx]))

    L += ["## Contract: headline numbers reproduce", "",
          "| analysis | metric | n | point | 95% CI |", "|---|---|---|---|---|"]
    r0 = boot_pair(sp("alpha"), sp("lag_native_mag"), n, rng)
    add("contract_MVxVAE", "rho_alpha", n, r0["a"], r0["a_ci"])
    add("contract_MVxVAE", "rho_lag_native_mag", n, r0["b"], r0["b_ci"])
    assert abs(r0["a"] - 0.882) < 5e-4 and abs(r0["b"] - 0.163) < 5e-4, (r0["a"], r0["b"])

    # ---- R1 harmonized: same pair, same genes, every lag convention, paired Δρ vs α
    L += ["", "## R1 Harmonized: MultiVelo × MultiVeloVAE, one gene set, every convention", "",
          f"> n={n} genes common to both methods. Δρ = ρ_α − ρ_output on the same bootstrap draw.", "",
          "| analysis | metric | n | point | 95% CI |", "|---|---|---|---|---|"]
    for key in ["alpha_c", "lag_native_mag", "lag_rateproxy_signed", "lag_rateproxy_mag"]:
        r = boot_pair(sp("alpha"), sp(key), n, rng)
        add(f"R1_{key}", "rho", n, r["b"], r["b_ci"])
        add(f"R1_{key}", "delta_rho_alpha_minus", n, r["d"], r["d_ci"])

    # common set with MoFlow: α pair stays MV×VAE; three lag pairs on identical genes
    sh3 = sorted(set(sh) & set(mo.index[mo.cs_lag_median.notna()]))
    A3, V3, M3 = mv.loc[sh3], vae.loc[sh3], mo.loc[sh3]
    lag3 = dict(MV=(A3.fit_t_sw2 - A3.fit_t_sw1).values,
                VAE=(1 / V3.vae_alpha_c.clip(1e-6) - 1 / V3.vae_alpha.clip(1e-6)).values,
                MoFlow=M3.cs_lag_median.values)
    a3 = (A3.fit_alpha.values, V3.vae_alpha.values)
    n3 = len(sh3)
    L += ["", f"### Three-method common gene set (n={n3})", "",
          "| analysis | metric | n | point | 95% CI |", "|---|---|---|---|---|"]
    st_a3 = lambda idx: spear(a3[0][idx], a3[1][idx])
    for p, q in [("MV", "VAE"), ("MV", "MoFlow"), ("VAE", "MoFlow")]:
        for conv, f in [("mag", np.abs), ("signed", lambda v: v)]:
            if conv == "signed" and "MV" in (p, q):
                continue  # MultiVelo lag sign is structural (always positive)
            st = lambda idx, p=p, q=q, f=f: spear(f(lag3[p])[idx], f(lag3[q])[idx])
            r = boot_pair(st_a3, st, n3, rng)
            add(f"R1c_{p}x{q}_{conv}", "rho", n3, r["b"], r["b_ci"])
            add(f"R1c_{p}x{q}_{conv}", "delta_rho_alpha_minus", n3, r["d"], r["d_ci"])
    r = boot_pair(st_a3, st_a3, n3, rng, b=2000)
    add("R1c_alpha_MVxVAE", "rho", n3, r["a"], r["a_ci"])

    # ---- R2 abundance-residualized concordance
    sha = sorted(set(sh) & set(ab.dropna().index))
    z = ab.loc[sha].values
    ia = np.array([sh.index(g) for g in sha])
    na = len(sha)
    L += ["", "## R2 Abundance-residualized cross-method concordance (MV × VAE)", "",
          f"> Partial Spearman given HSPC mean Ms expression, n={na}.", "",
          "| analysis | metric | n | point | 95% CI |", "|---|---|---|---|---|"]
    for key in ["alpha", "alpha_c", "lag_native_mag"]:
        u, v = x[key][0][ia], x[key][1][ia]
        raw = lambda idx, u=u, v=v: spear(u[idx], v[idx])
        par = lambda idx, u=u, v=v: partial_spear(u[idx], v[idx], z[idx])
        r = boot_pair(raw, par, na, rng)
        add(f"R2_{key}", "rho_raw", na, r["a"], r["a_ci"])
        add(f"R2_{key}", "rho_partial_abundance", na, r["b"], r["b_ci"])
    for meth, col in [("MV", 0), ("VAE", 1)]:
        u = x["alpha"][col][ia]
        r = boot_pair(lambda idx, u=u: spear(u[idx], z[idx]),
                      lambda idx, u=u: spear(u[idx], z[idx]), na, rng, b=2000)
        add(f"R2_alpha_{meth}_vs_abundance", "rho", na, r["a"], r["a_ci"])
    ua, va_ = x["alpha"][0][ia], x["alpha"][1][ia]
    ul, vl = x["lag_native_mag"][0][ia], x["lag_native_mag"][1][ia]
    r = boot_pair(lambda idx: partial_spear(ua[idx], va_[idx], z[idx]),
                  lambda idx: partial_spear(ul[idx], vl[idx], z[idx]), na, rng)
    add("R2_partial", "delta_rho_alpha_minus_lag", na, r["d"], r["d_ci"])

    # ---- R3 module bootstrap of the headline Δρ
    mods = gene_modules(sh, [10, 20, 50, 100])
    L += ["", "## R3 Dependence-aware bootstrap of Δρ = ρ_α − ρ_lag (MV × VAE, native magnitude)", "",
          "> Genes resampled as whole co-expression modules (average-linkage clusters of the Ms",
          "> gene-gene correlation). K = number of modules; iid = independent genes.", "",
          "| analysis | metric | n | point | 95% CI |", "|---|---|---|---|---|"]
    r = boot_pair(sp("alpha"), sp("lag_native_mag"), n, rng)
    add("R3_iid", "delta_rho", n, r["d"], r["d_ci"])
    for k, g in mods.items():
        r = boot_pair(sp("alpha"), sp("lag_native_mag"), n, rng, groups=g)
        sizes = np.bincount(g)[1:]
        add(f"R3_modules_K{k}(largest={sizes.max()})", "delta_rho", n, r["d"], r["d_ci"])
        add(f"R3_modules_K{k}(largest={sizes.max()})", "rho_lag", n, r["b"], r["b_ci"])

    # ---- R4 curvature coordinates
    pl = pd.read_csv(RES / "profile_likelihood_identifiability.csv")
    pl = pl[(pl.lag_cls == "interior") & (pl.kappa_alpha_pc > 0) & (pl.kappa_lag_pc > 0)]
    log_ratio = pl.kappa_alpha_pc / pl.kappa_lag_pc
    # κ on ln-lag → κ on lag/TOTAL_H: multiply by (TOTAL_H / lag0)^2
    hz_ratio = pl.kappa_alpha_pc / (pl.kappa_lag_pc * (TOTAL_H / pl.lag0) ** 2)
    L += ["", "## R4 Curvature coordinates (fixed-nuisance profile)", "",
          f"> n={len(pl)}: genes whose lag profile is interior (of 302) and whose α and lag curvatures",
          ">   are both finite and positive. α has no interior/boundary classification.",
          "> As submitted both curvatures are −d²LL/d(ln θ)² per cell (log coordinates).",
          "> Sensitivity: lag expressed linearly as a fraction of the pseudotime horizon (lag/20),",
          ">   with α kept in log coordinates. Neither coordinate system is canonical.", "",
          "| coordinates | median κ_α/κ_lag | IQR | α stiffer (%) |", "|---|---|---|---|"]
    for lbl, s in [("ln α vs ln lag (as submitted)", log_ratio), ("ln α vs lag/horizon", hz_ratio)]:
        L.append(f"| {lbl} | {s.median():.2f} | [{s.quantile(.25):.2f}, {s.quantile(.75):.2f}] | "
                 f"{100 * (s > 1).mean():.1f} |")
        rows.append(dict(analysis=f"R4_{lbl}", metric="median_ratio", n=len(pl), point=float(s.median()),
                         ci_lo=float(s.quantile(.25)), ci_hi=float(s.quantile(.75))))
    L.append(f"\nlag0 among these genes: median {pl.lag0.median():.2f}, range "
             f"[{pl.lag0.min():.2f}, {pl.lag0.max():.2f}] pseudotime units")
    cls = pd.read_csv(RES / "profile_likelihood_identifiability.csv").lag_cls.value_counts()
    L.append(f"lag class counts: {cls.to_dict()}")

    # ---- R5 MultiVelo priming interval (fit_t_sw1) instead of fit_t_sw2 − fit_t_sw1
    # multivelo 0.1.5 dynamical_chrom_func.py: state0 (t ≤ t_sw1) is primed (chromatin open,
    # no transcription), so t_sw1 = t_i = Δt_priming (to = 0 for models 1 and 2). fit_t_sw2 − fit_t_sw1
    # is the length of the coupled-on state: t_c − t_i (model 1) or t_r − t_i (model 2).
    mods_used = A.fit_model.value_counts().to_dict()
    pr = dict(MV=A.fit_t_sw1.values,
              VAE=np.abs(1 / V.vae_alpha_c.clip(1e-6) - 1 / V.vae_alpha.clip(1e-6)).values)
    L += ["", "## R5 MultiVelo lag definition: priming interval (t_sw1) vs coupled-on length (t_sw2 − t_sw1)", "",
          f"> MultiVelo models among the {n} MV × VAE genes: {mods_used}. Partner lags are magnitudes.",
          "> Δρ = ρ_α − ρ_lag on the same bootstrap draw.", "",
          "| analysis | metric | n | point | 95% CI |", "|---|---|---|---|---|"]
    for lbl, mvlag in [("coupled_on", np.abs(A.fit_t_sw2 - A.fit_t_sw1).values), ("priming", pr["MV"])]:
        st = lambda idx, u=mvlag: spear(u[idx], pr["VAE"][idx])
        r = boot_pair(sp("alpha"), st, n, rng)
        add(f"R5_MVxVAE_{lbl}", "rho", n, r["b"], r["b_ci"])
        add(f"R5_MVxVAE_{lbl}", "delta_rho_alpha_minus", n, r["d"], r["d_ci"])
    for lbl, mvlag in [("coupled_on", lag3["MV"]), ("priming", A3.fit_t_sw1.values)]:
        st = lambda idx, u=mvlag: spear(u[idx], np.abs(lag3["MoFlow"])[idx])
        r = boot_pair(st_a3, st, n3, rng)
        add(f"R5_MVxMoFlow_{lbl}", "rho", n3, r["b"], r["b_ci"])
        add(f"R5_MVxMoFlow_{lbl}", "delta_rho_alpha_minus", n3, r["d"], r["d_ci"])
    pin = pd.read_csv(RES / "profile_likelihood_identifiability.csv")
    if "fit_direction" not in pin.columns:
        pin["gene"] = pin.gene.astype(str).str.upper()
        pin = pin.merge(mv[["fit_direction"]], left_on="gene", right_index=True, how="left")
    bnd = pin[pin.lag_cls != "interior"]
    L.append(f"\nnon-interior lag classes by MultiVelo fit_direction: "
             f"{bnd.groupby(['lag_cls', 'fit_direction']).size().to_dict()}")
    L.append(f"all fitted genes by fit_direction: {pin.fit_direction.value_counts().to_dict()}")

    (RES / "post_review_robustness.gen.md").write_text("\n".join(L) + "\n")
    pd.DataFrame(rows).to_csv(RES / "post_review_robustness.csv", index=False)
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    sys.exit(main())
