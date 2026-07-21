#!/usr/bin/env python3
"""P3 concordance (hardened) — HSPC→macrophage differentiation replication of the HSPC lag/α finding.

핵심 질문: HSPC 결론 "gene별 chromatin→transcription **lag은 method-robust하지 않지만**
transcription rate **α는 robust(cross-method ρ≈0.88)**"가 **같은 human 조혈축의 하류(단핵구→대식세포
분화; MultiVeloVAE 신규 데이터셋)**에서 재현되나? — same-lineage 하류 확장, drug-timing endpoint 근접.

BMMC 스크립트를 미러하되 **하드닝**: point Spearman에 더해
  - **paired-over-genes bootstrap 95% CI** (parametric Steiger/Meng 금지; ANALYSIS-EXTENSIONS #1·#5),
  - **paired Δρ = ρ_α − ρ_lag** (한 resample당 index 1회 draw, 두 ρ 동일 gene set) — dissociation,
  - **TOST 등가경계 |ρ|<0.2** (lag를 'failure-to-reject'가 아니라 등가로 프레이밍),
scripts/p3_identifiability_dissociation.py의 boot_ci/boot_dr/tost_verdict와 정합(동일 B/SEED/정의).
human↔human이라 case/ortholog 매핑 불필요; 방어적 uppercase 정규화만.

두 축:
  A. Within-macrophage cross-method: α(floor·MV·VAE pairwise) robust / lag(MV×VAE 크기) fragile + Δρ
  B. Cross-dataset HSPC↔macrophage: MV lag-크기 rank vs α rank (+ floor α sanity)

lag 정의 (p3_concordance.py / BMMC와 동일):
  - MultiVelo:    fit_t_sw2 − fit_t_sw1 (pseudotime; 4-state 단조정렬 → sign 구조적 양수=무정보, 크기 rank만)
  - MultiVeloVAE: 1/vae_alpha_c − 1/vae_alpha (sign 가변)

⚠️ 데이터셋 caveat (build_macrophage.py 참조):
  - figshare postpro는 **HVG 필터+scVelo moments 완료**(layers Ms/Mu). raw spliced/unspliced 부재 시
    moment fallback → 공통 전처리 분기점이 다른 3종보다 pre-baked(방법론 #5). concordance엔 noise만
    추가(lag-fragile에 보수적). Methods에 명시.
  - concat에서 macrophage batch(9060-MV-3)만 subset(HSPC leakage 차단).

입력 계약(리더 GPU 런 산출; 기존 3종 규약과 동일, index=gene):
  results/rna_only_dynamical_genes_macrophage.csv   컬럼: fit_alpha, fit_likelihood
  results/multivelo_genes_macrophage.csv            컬럼: fit_alpha, fit_t_sw1, fit_t_sw2, fit_likelihood
  results/multivelovae_genes_macrophage.csv         컬럼: vae_alpha, vae_alpha_c, vae_likelihood

실행(scv-preprocess env):
  conda run -n scv-preprocess python cross_dataset/p3_concordance_macrophage.py
셀프검증(기존 BMMC fits로 커밋 숫자 재현; 커밋 파일 미수정):
  conda run -n scv-preprocess python cross_dataset/p3_concordance_macrophage.py \
      --ds GSE194122_bmmc --out /tmp/_bmmc_check.md --csv /tmp/_bmmc_check.csv
출력: results/concordance_macrophage.md + results/concordance_macrophage.csv
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MIN_SHARED = 10
B_DEFAULT = 10000
SEED = 20260707          # p3_identifiability_dissociation.py와 동일(재현성)
TOST_BOUND = 0.20        # ANALYSIS-EXTENSIONS 사전선언 등가경계


# ── 입출력 ──────────────────────────────────────────────────────────
def load(path: Path):
    if not path.exists():
        return None
    d = pd.read_csv(path, index_col=0)
    d = d[d["fit_likelihood"].notna()] if "fit_likelihood" in d.columns else d
    return d[~d.index.duplicated()]


def _upper(d):
    if d is None:
        return None
    d = d.copy()
    d.index = d.index.astype(str).str.upper()
    return d[~d.index.duplicated()]


# ── 통계 (scripts/p3_identifiability_dissociation.py와 동일 구현) ──
def fast_spear(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = rankdata(a), rankdata(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def boot_ci(a: np.ndarray, b: np.ndarray, rng, B: int, level=95):
    n = len(a)
    point = fast_spear(a, b)
    dist = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, n)
        dist[i] = fast_spear(a[idx], b[idx])
    lo, hi = np.percentile(dist, [(100 - level) / 2, 100 - (100 - level) / 2])
    return point, float(lo), float(hi)


def boot_dr(xa, ya, xl, yl, rng, B: int, level=95):
    """Paired Δρ = ρ_α − ρ_lag: 한 resample당 index 1회 draw, 두 ρ 동일 set."""
    n = len(xa)
    p_a, p_l = fast_spear(xa, ya), fast_spear(xl, yl)
    dd = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, n, n)
        dd[i] = fast_spear(xa[idx], ya[idx]) - fast_spear(xl[idx], yl[idx])
    q = [(100 - level) / 2, 100 - (100 - level) / 2]
    lo, hi = (float(x) for x in np.percentile(dd, q))
    return dict(rho_a=p_a, rho_l=p_l, dr=p_a - p_l, dr_lo=lo, dr_hi=hi, dr_mean=float(dd.mean()))


def tost_verdict(lo, hi, bound=TOST_BOUND):
    ok = (lo > -bound) and (hi < bound)
    txt = (f"EQUIVALENT (CI ⊂ [−{bound:.1f},+{bound:.1f}])" if ok
           else f"NOT equivalent (CI exits [−{bound:.1f},+{bound:.1f}])")
    return ok, txt


def _pair(a: pd.Series, b: pd.Series):
    a, b = a.dropna(), b.dropna()
    sh = sorted(set(a.index) & set(b.index))
    return sh, a.loc[sh].astype(float).values, b.loc[sh].astype(float).values


def emit(L, rows, section, label, a, b, rng, B, sign_note=None, tost=False):
    """point Spearman + bootstrap 95% CI 한 줄 + CSV row."""
    sh, av, bv = _pair(a, b)
    n = len(sh)
    if n < MIN_SHARED:
        L.append(f"- **{label}**: shared {n} (<{MIN_SHARED}) → 비정보(생략)")
        rows.append(dict(section=section, comparison=label, n_shared=n,
                         rho=np.nan, ci_lo=np.nan, ci_hi=np.nan, note="insufficient"))
        return None
    rho, lo, hi = boot_ci(av, bv, rng, B)
    _, p = spearmanr(av, bv)
    extra = f" (p={p:.2g})"
    note = ""
    if tost:
        ok, txt = tost_verdict(lo, hi)
        extra += f" | TOST |ρ|<{TOST_BOUND}: **{txt}**"
        note = "EQUIVALENT" if ok else "not-equivalent"
    L.append(f"- **{label}** (shared {n}): Spearman **{rho:+.3f}** 95%CI "
             f"[{lo:+.3f}, {hi:+.3f}]{extra}")
    if sign_note:
        L.append(f"  - ⚠️ {sign_note}")
    rows.append(dict(section=section, comparison=label, n_shared=n,
                     rho=round(rho, 4), ci_lo=round(lo, 4), ci_hi=round(hi, 4), note=note))
    return dict(sh=sh, av=av, bv=bv, rho=rho, lo=lo, hi=hi)


def main(argv=None):
    ap = argparse.ArgumentParser(description="hardened macrophage concordance (+bootstrap CI, TOST)")
    ap.add_argument("--ds", default="macrophage",
                    help="dataset suffix (기본 macrophage; 셀프검증 시 GSE194122_bmmc 등)")
    ap.add_argument("--hspc-mv", default="multivelo_genes.csv", help="HSPC MultiVelo baseline")
    ap.add_argument("--hspc-floor", default="rna_only_dynamical_genes.csv", help="HSPC floor baseline")
    ap.add_argument("--out", default=None, help="MD 출력(기본 results/concordance_<ds>.md)")
    ap.add_argument("--csv", default=None, help="CSV 출력(기본 results/concordance_<ds>.csv)")
    ap.add_argument("-B", "--bootstrap", type=int, default=B_DEFAULT)
    args = ap.parse_args(argv)

    DS = args.ds
    out_md = Path(args.out) if args.out else RESULTS / f"concordance_{DS}.md"
    out_csv = Path(args.csv) if args.csv else RESULTS / f"concordance_{DS}.csv"
    B = args.bootstrap
    rng = np.random.default_rng(SEED)
    RESULTS.mkdir(parents=True, exist_ok=True)

    b_fl = load(RESULTS / f"rna_only_dynamical_genes_{DS}.csv")
    b_mv = load(RESULTS / f"multivelo_genes_{DS}.csv")
    b_vae = load(RESULTS / f"multivelovae_genes_{DS}.csv")
    h_mv = load(RESULTS / args.hspc_mv)
    h_fl = load(RESULTS / args.hspc_floor)

    rows: list[dict] = []
    L = [f"# P3 concordance (hardened) — {DS} replication of HSPC lag/α finding", "",
         f"> Paired-over-genes bootstrap B={B:,}, seed={SEED} (deterministic percentile 95% CI). "
         "lag는 'failure-to-reject'가 아니라 TOST 등가(|ρ|<0.2)로 프레이밍.", "",
         "> 질문: HSPC 결론 **\"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.9)\"**가 "
         f"**{DS}**(같은 human 조혈축)에서 재현되나?", "",
         "## 실행된 method arm", "",
         "| arm | fit gene | rate/lag 컬럼 |", "|---|---|---|"]
    for name, d, cols in [("scVelo floor (RNA-only)", b_fl, "fit_alpha"),
                          ("MultiVelo (chromatin-aware)", b_mv, "fit_alpha / fit_t_sw*"),
                          ("MultiVeloVAE (chromatin-aware)", b_vae, "vae_alpha / vae_alpha_c")]:
        L.append(f"| {name} | {len(d) if d is not None else '**없음**'} | {cols} |")
    L.append("")

    # ── A. Within-dataset cross-method ──
    L += [f"## A. Within-{DS} cross-method concordance", "", "동일 데이터셋·동일 gene축.", "",
          "### A1. transcription rate α (robust leg 기대) — bootstrap 95% CI", ""]
    a_rhos = []
    alpha = {}
    if b_fl is not None and "fit_alpha" in b_fl: alpha["floor"] = b_fl["fit_alpha"]
    if b_mv is not None and "fit_alpha" in b_mv: alpha["MV"] = b_mv["fit_alpha"]
    if b_vae is not None and "vae_alpha" in b_vae: alpha["VAE"] = b_vae["vae_alpha"]
    names = list(alpha)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            A, C = names[i], names[j]
            res = emit(L, rows, "A1_alpha_within", f"α: {A} × {C}", alpha[A], alpha[C], rng, B)
            if res:
                a_rhos.append(res["rho"])
    if not a_rhos:
        L.append("- α 비교 가능한 method 쌍 없음 (2개+ arm 필요).")
    L.append("")

    # A2. lag magnitude — fragile leg (MV × VAE) + TOST
    L += ["### A2. chromatin→transcription lag (fragile leg 기대) — magnitude rank + TOST", "",
          "> floor는 RNA-only라 lag 없음 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정.", ""]
    lag = {}
    if b_mv is not None and {"fit_t_sw1", "fit_t_sw2"} <= set(b_mv.columns):
        lag["MV"] = (b_mv["fit_t_sw2"] - b_mv["fit_t_sw1"])
    if b_vae is not None and {"vae_alpha_c", "vae_alpha"} <= set(b_vae.columns):
        lag["VAE"] = (1.0 / b_vae["vae_alpha_c"].clip(1e-6) - 1.0 / b_vae["vae_alpha"].clip(1e-6))
    lag_res = None
    if len(lag) >= 2:
        lag_res = emit(L, rows, "A2_lag_within", "lag **크기** rank: MV × VAE",
                       lag["MV"].abs(), lag["VAE"].abs(), rng, B,
                       sign_note="sign-agreement 생략: MultiVelo lag sign은 4-state 단조정렬로 구조적 양수(무정보).",
                       tost=True)
    else:
        L.append(f"- chromatin-aware lag method {len(lag)}개 ({list(lag)}) → 2개+ 필요(VAE 완주 후 산출).")
    L.append("")

    # A3. paired Δρ dissociation (α ≫ lag), CI excludes 0?
    L += ["### A3. paired Δρ = ρ_α − ρ_lag (dissociation, CI가 0 제외?)", "",
          "> 한 resample당 index 1회 draw로 두 ρ를 동일 gene set에서 계산(paired). "
          "헤드라인은 등가가 아니라 **dissociation**(Δρ CI가 0 제외).", ""]
    dr = None
    if len(lag) >= 2 and "MV" in alpha and "VAE" in alpha:
        a_sh, _, _ = _pair(alpha["MV"], alpha["VAE"])
        l_sh, _, _ = _pair(lag["MV"].abs(), lag["VAE"].abs())
        common = sorted(set(a_sh) & set(l_sh))
        if len(common) >= MIN_SHARED:
            amv = alpha["MV"].loc[common].astype(float).values
            avae = alpha["VAE"].loc[common].astype(float).values
            lmv = lag["MV"].abs().loc[common].astype(float).values
            lvae = lag["VAE"].abs().loc[common].astype(float).values
            dr = boot_dr(amv, avae, lmv, lvae, rng, B)
            excl = dr["dr_lo"] > 0
            L += [f"- ρ_α(MV×VAE) = **{dr['rho_a']:+.3f}**, ρ_lag(MV×VAE) = **{dr['rho_l']:+.3f}** "
                  f"(공통 {len(common)} gene)",
                  f"- **Δρ = {dr['dr']:+.3f}** 95%CI **[{dr['dr_lo']:+.3f}, {dr['dr_hi']:+.3f}]** "
                  f"(bootstrap mean {dr['dr_mean']:+.3f})",
                  f"  → CI가 0을 {'**제외** — dissociation 성립(α ≫ lag)' if excl else '포함 — 재검토'}."]
            rows.append(dict(section="A3_dissociation", comparison="Δρ = ρ_α − ρ_lag (MV×VAE)",
                             n_shared=len(common), rho=round(dr["dr"], 4),
                             ci_lo=round(dr["dr_lo"], 4), ci_hi=round(dr["dr_hi"], 4),
                             note="dr_excludes_0" if excl else "dr_includes_0"))
        else:
            L.append(f"- α∩lag 공통 gene {len(common)} (<{MIN_SHARED}) → Δρ 생략.")
    else:
        L.append("- α(MV,VAE)+lag(MV,VAE) 모두 필요 → VAE 완주 후 산출.")
    L.append("")

    # ── B. Cross-dataset HSPC ↔ dataset ──
    L += [f"## B. Cross-dataset HSPC ↔ {DS} (human↔human, 직접 gene 매칭) — bootstrap 95% CI", "",
          "> 둘 다 human 조혈 → gene SYMBOL 축 직접 겹침(case/ortholog 매핑 불필요). "
          "방어적 uppercase 정규화만.", ""]
    b_lag_rho = b_alpha_rho = None
    hmv, bmv = _upper(h_mv), _upper(b_mv)
    if hmv is not None and bmv is not None:
        L.append(f"- shared gene (HSPC × {DS} MultiVelo): "
                 f"**{len(set(hmv.index) & set(bmv.index))}**")
        if {"fit_t_sw1", "fit_t_sw2"} <= set(hmv.columns) and {"fit_t_sw1", "fit_t_sw2"} <= set(bmv.columns):
            h_lag = (hmv["fit_t_sw2"] - hmv["fit_t_sw1"]).abs()
            e_lag = (bmv["fit_t_sw2"] - bmv["fit_t_sw1"]).abs()
            r = emit(L, rows, "B_cross", f"MV lag 크기 rank: HSPC × {DS}", h_lag, e_lag, rng, B, tost=True)
            b_lag_rho = r["rho"] if r else None
        r = emit(L, rows, "B_cross", f"MV α rank: HSPC × {DS}", hmv["fit_alpha"], bmv["fit_alpha"], rng, B)
        b_alpha_rho = r["rho"] if r else None
        hfl, bfl = _upper(h_fl), _upper(b_fl)
        if hfl is not None and bfl is not None:
            emit(L, rows, "B_cross", f"floor α rank: HSPC × {DS} (sanity)",
                 hfl["fit_alpha"], bfl["fit_alpha"], rng, B)
    else:
        L.append(f"- HSPC 또는 {DS} MultiVelo csv 없음 → cross-dataset 비교 skip.")
    L.append("")

    # ── 판정 ──
    L += ["## 판정 — 'lag-fragile / α-robust' 패턴 재현?", ""]
    def _fmt(x): return f"{x:+.3f}" if x is not None else "N/A"
    a_alpha_med = float(np.median(a_rhos)) if a_rhos else None
    lag_within = lag_res["rho"] if lag_res else None
    L.append(f"- Within-{DS} α (cross-method) Spearman 중앙값: {_fmt(a_alpha_med)} "
             f"({[f'{r:+.2f}' for r in a_rhos] or 'N/A'})")
    L.append(f"- Within-{DS} lag 크기 rank (MV×VAE): {_fmt(lag_within)}"
             + (f" 95%CI [{lag_res['lo']:+.3f}, {lag_res['hi']:+.3f}]" if lag_res else ""))
    if dr:
        L.append(f"- Δρ dissociation: {dr['dr']:+.3f} 95%CI [{dr['dr_lo']:+.3f}, {dr['dr_hi']:+.3f}]")
    L.append(f"- Cross-dataset HSPC↔{DS}: lag 크기 rank {_fmt(b_lag_rho)} vs α rank {_fmt(b_alpha_rho)}")
    L.append("")
    verdict, why = _verdict(a_alpha_med, lag_within, b_lag_rho, b_alpha_rho, dr)
    L += [f"### → **{verdict}**", f"- {why}", "",
          "## caveat (필수)",
          "- lag 크기 rank만 비교(방향 아님): MultiVelo sign은 4-state 단조정렬로 구조적 양수(무정보).",
          "- 'lag not robust'는 실패-미기각이 아니라 **TOST 등가(|ρ|<0.2)** + 부트스트랩 CI로 프레이밍. "
          "Δρ CI가 0을 제외하면 dissociation(α ≫ lag)이 핵심 주장.",
          f"- replication {DS} 1건 — 강한 일반화 금지. HSPC+human_brain+E18+BMMC+macrophage 축 일관성으로만 서사.",
          "- concordance는 *전역* per-gene fit rank(within-lineage 아님).",
          "- ⚠️ **전처리 분기점(중요)**: figshare postpro는 저자 그래프에서 HVG 필터+scVelo moments 완료"
          "(Ms/Mu). raw spliced/unspliced 부재 시 moment fallback → 다른 3종보다 pre-baked(방법론 #5). "
          "human_brain 외부-제공 spliced/unspliced caveat보다 강함 — Methods 명시. cross rank엔 noise만 추가"
          "(낮은 rho=lag fragile에 보수적).", ""]

    out_md.write_text("\n".join(L), encoding="utf-8")
    pd.DataFrame(rows, columns=["section", "comparison", "n_shared", "rho", "ci_lo", "ci_hi", "note"]
                 ).to_csv(out_csv, index=False)
    print("\n".join(L))
    print(f"\n✓ MD  → {out_md}")
    print(f"✓ CSV → {out_csv}")
    return 0


def _verdict(a_alpha, lag_within, b_lag, b_alpha, dr):
    def hi(x): return x is not None and abs(x) > 0.5
    def lo(x): return x is not None and abs(x) <= 0.3
    alpha_robust = hi(a_alpha) or hi(b_alpha)
    lag_fragile = lo(lag_within) or lo(b_lag)
    dr_ok = dr is not None and dr["dr_lo"] > 0
    lag_tested = (lag_within is not None) or (b_lag is not None)
    if not alpha_robust and a_alpha is None and b_alpha is None:
        return ("판정 보류 — α/lag 지표 부족", "필요한 arm(최소 floor+MV, lag는 MV+VAE)이 아직 안 끝남.")
    if alpha_robust and (lag_fragile or dr_ok):
        legs = []
        if lag_within is not None: legs.append(f"within MV×VAE lag {lag_within:+.2f}")
        if b_lag is not None: legs.append(f"cross lag {b_lag:+.2f}")
        if dr is not None: legs.append(f"Δρ {dr['dr']:+.2f} CI[{dr['dr_lo']:+.2f},{dr['dr_hi']:+.2f}]")
        return ("재현 YES — 'lag-fragile / α-robust' 패턴 재현",
                f"α robust(≈{a_alpha if a_alpha is not None else b_alpha:+.2f}), lag 약함/dissociation "
                f"({', '.join(legs)}). HSPC same-lineage 서사 일치.")
    if alpha_robust and not lag_tested:
        return ("재현 PARTIAL — α-robust만 확인", "lag fragile leg는 VAE 완주/cross MV lag rank 필요.")
    if alpha_robust and not lag_fragile:
        return ("재현 PARTIAL — α-robust 확인, lag는 예상보다 강함",
                f"α robust이나 lag |r|>0.3 (within {lag_within}, cross {b_lag}) — 정직 보고.")
    return ("재현 약함/불명확",
            f"α robust={alpha_robust}, lag fragile={lag_fragile}, Δρ_ok={dr_ok} — 지표 재확인.")


if __name__ == "__main__":
    sys.exit(main())
