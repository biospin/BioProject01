#!/usr/bin/env python3
"""P3 — within-dataset cross-method concordance for external datasets, MoFlow arm added.

목적: 외부 4종(human_brain·e18_mouse_brain·GSE194122_bmmc·macrophage)의 lag-fragile leg가
지금까지 단일 method 쌍(MV×MultiVeloVAE)뿐이던 것에 **두 번째 쌍 MV×MoFlow**를 붙인다
(draft_v2 L171 / FINDINGS L127 한계 대응). α-robust leg(floor×MV×VAE)는 MoFlow가 α를 내지
않으므로 불변 — 여기선 문맥으로만 재계산해 α≫lag 순서 보존을 확인한다.

규약(FINDINGS/verify-gate와 동일):
  - MV lag        = fit_t_sw2 − fit_t_sw1  (4-state 단조정렬 → 구조적 양수 → |MV|=MV)
  - MoFlow lag    = cs_lag_median          (DTW c-s lag, sign 가변)
  - VAE lag       = 1/vae_alpha_c − 1/vae_alpha  (rate-proxy, sign 가변)
  - α             = MV fit_alpha / VAE vae_alpha / floor fit_alpha
  - signed convention   : Spearman(lagA, lagB)
  - magnitude convention: Spearman(|lagA|, |lagB|)   ← FINDINGS headline 규약
  - paired bootstrap 95% CI: B=10000, seed=20260707 (p3_identifiability_dissociation.py와 동일)

산출: results/concordance_moflow_external.csv (+ .md 파이프라인 아티팩트)
실행: conda run -n scv-preprocess python p3_moflow_external_concordance.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata

RESULTS = Path(__file__).resolve().parent.parent / "results"
B = 10000
SEED = 20260707
MIN_SHARED = 10
# gse205117(gastrulation): 이미 MoFlow가 돌아 있어(moflow_genes_gse205117.csv) read-only로 포함.
# within-dataset MV×MoFlow를 비교 sibling으로 얻는다("gastrulation 건드리지 말 것"=재-fit 금지, read-only는 허용).
DATASETS = ["human_brain", "e18_mouse_brain", "GSE194122_bmmc", "macrophage", "gse205117"]


def load(name: str) -> pd.DataFrame | None:
    p = RESULTS / name
    if not p.exists():
        return None
    d = pd.read_csv(p, index_col=0)
    if "fit_likelihood" in d.columns:
        d = d[d["fit_likelihood"].notna()]
    return d[~d.index.duplicated()]


def fast_spear(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = rankdata(a), rankdata(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def boot_ci(a: np.ndarray, b: np.ndarray, rng, level=95):
    n = len(a)
    point = fast_spear(a, b)
    dist = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, n)
        dist[i] = fast_spear(a[idx], b[idx])
    lo, hi = np.percentile(dist, [(100 - level) / 2, 100 - (100 - level) / 2])
    return point, float(lo), float(hi), n


def series_lag(ds):
    """Return dict of gene-indexed lag/alpha Series available for dataset ds."""
    out = {}
    mv = load(f"multivelo_genes_{ds}.csv")
    if mv is not None and {"fit_t_sw1", "fit_t_sw2"} <= set(mv.columns):
        out["mv_lag"] = (mv["fit_t_sw2"] - mv["fit_t_sw1"]).dropna()
        if "fit_alpha" in mv.columns:
            out["mv_alpha"] = mv["fit_alpha"].dropna()
    vae = load(f"multivelovae_genes_{ds}.csv")
    if vae is not None and {"vae_alpha_c", "vae_alpha"} <= set(vae.columns):
        out["vae_lag"] = (1.0 / vae["vae_alpha_c"].clip(1e-6)
                          - 1.0 / vae["vae_alpha"].clip(1e-6)).dropna()
        out["vae_alpha"] = vae["vae_alpha"].dropna()
    fl = load(f"rna_only_dynamical_genes_{ds}.csv")
    if fl is not None and "fit_alpha" in fl.columns:
        out["floor_alpha"] = fl["fit_alpha"].dropna()
    mo = load(f"moflow_genes_{ds}.csv")
    if mo is not None and "cs_lag_median" in mo.columns:
        valid = mo["cs_lag_median"].dropna()
        if len(valid) > 0:
            out["moflow_lag"] = valid
        else:
            # MoFlow velocity fit OK but DTW c-s lag undefined (all-NaN). e18: velo_s_pseudotime
            # collapsed (99% cells at t≈1.0, 15/20 empty bins) → fastdtw IndexError on NaN.
            out["_moflow_note"] = f"MoFlow fit OK({len(mo)} genes) but cs_lag all-NaN (collapsed velo-pseudotime)"
    elif mo is None:
        out["_moflow_note"] = "moflow csv 없음"
    return out


def pair(rows, ds, label, A, B_, s, rng, kind):
    """kind: 'signed' or 'magnitude' (lag) or 'alpha'. Adds a row if shared>=MIN_SHARED."""
    if A not in s or B_ not in s:
        uses_moflow = "moflow" in A or "moflow" in B_
        miss = s.get("_moflow_note", "method(s) 없음") if uses_moflow else "method(s) 없음"
        rows.append(dict(dataset=ds, comparison=label, convention=kind,
                         rho=np.nan, ci_lo=np.nan, ci_hi=np.nan, n_shared=0,
                         note=miss))
        return None
    sh = sorted(set(s[A].index) & set(s[B_].index))
    a, b = s[A].loc[sh].astype(float).values, s[B_].loc[sh].astype(float).values
    if kind == "magnitude":
        a, b = np.abs(a), np.abs(b)
    if len(sh) < MIN_SHARED:
        rows.append(dict(dataset=ds, comparison=label, convention=kind,
                         rho=np.nan, ci_lo=np.nan, ci_hi=np.nan, n_shared=len(sh),
                         note=f"shared<{MIN_SHARED}"))
        return None
    rho, lo, hi, n = boot_ci(a, b, rng)
    rows.append(dict(dataset=ds, comparison=label, convention=kind,
                     rho=round(rho, 4), ci_lo=round(lo, 4), ci_hi=round(hi, 4),
                     n_shared=n, note=""))
    return rho


def main():
    rows = []
    for ds in DATASETS:
        rng = np.random.default_rng(SEED)
        s = series_lag(ds)
        # --- NEW lag pair: MV × MoFlow ---
        pair(rows, ds, "MV×MoFlow lag", "mv_lag", "moflow_lag", s, rng, "magnitude")
        pair(rows, ds, "MV×MoFlow lag", "mv_lag", "moflow_lag", s, rng, "signed")
        # --- existing lag pair: MV × VAE ---
        pair(rows, ds, "MV×VAE lag", "mv_lag", "vae_lag", s, rng, "magnitude")
        pair(rows, ds, "MV×VAE lag", "mv_lag", "vae_lag", s, rng, "signed")
        # --- α leg (context, unchanged by MoFlow) ---
        pair(rows, ds, "floor×MV alpha", "floor_alpha", "mv_alpha", s, rng, "alpha")
        pair(rows, ds, "MV×VAE alpha", "mv_alpha", "vae_alpha", s, rng, "alpha")
        pair(rows, ds, "floor×VAE alpha", "floor_alpha", "vae_alpha", s, rng, "alpha")

    df = pd.DataFrame(rows)
    out_csv = RESULTS / "concordance_moflow_external.csv"
    df.to_csv(out_csv, index=False)

    # --- pipeline md artifact (script-emitted) ---
    L = ["# P3 within-dataset cross-method concordance — MoFlow arm (외부 4종)", "",
         "> 목적: lag-fragile leg에 **두 번째 method 쌍 MV×MoFlow** 추가(기존 MV×VAE 단독 한계 대응).",
         f"> paired bootstrap 95% CI: B={B}, seed={SEED}. MV lag=fit_t_sw2−fit_t_sw1(구조적 양수),",
         "> MoFlow lag=cs_lag_median, VAE lag=1/α_c−1/α. magnitude=|lag| rank(headline), signed=원값 rank.", ""]
    for ds in DATASETS:
        L.append(f"## {ds}")
        sub = df[df.dataset == ds]
        L.append("| comparison | convention | Spearman ρ | 95% CI | n_shared | note |")
        L.append("|---|---|---|---|---|---|")
        for _, r in sub.iterrows():
            ci = "—" if pd.isna(r.rho) else f"[{r.ci_lo:+.3f}, {r.ci_hi:+.3f}]"
            rho = "—" if pd.isna(r.rho) else f"{r.rho:+.3f}"
            L.append(f"| {r.comparison} | {r.convention} | {rho} | {ci} | {int(r.n_shared)} | {r.note} |")
        L.append("")
    L += ["## caveat (필수)",
          "- MV 4-state는 switch-time 단조정렬 → MV lag은 구조적 양수, sign 무정보 → **magnitude rank**가 headline.",
          "- MoFlow velo 행렬은 재현성 높으나(run-to-run +0.9999) **cs_lag_median(DTW) 축 재현성 밴드는 별도로 느슨**",
          "  (`moflow_runtorun_null.md` §5) → 단일-fit ρ 점추정을 신호로 과대해석 금지, CI로 판단.",
          "- α leg(floor×MV×VAE)는 MoFlow가 α를 내지 않아 **불변** — 여기선 문맥용 재계산일 뿐 MoFlow가 강화하지 않음.",
          "- human_brain은 VAE 미실행 → MoFlow가 이 데이터셋의 **첫** within-dataset lag 파트너(두 번째 아님).",
          "- 각 replication 1 donor/샘플 — 강한 일반화 금지. BMMC는 shared gene 적어 CI 넓음.", ""]
    (RESULTS / "concordance_moflow_external.md").write_text("\n".join(L), encoding="utf-8")
    print(df.to_string(index=False))
    print(f"\n✓ → {out_csv.name} + concordance_moflow_external.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
