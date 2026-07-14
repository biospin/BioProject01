#!/usr/bin/env python
"""사전등록 채점기 — GSE205117(mouse gastrulation) 5번째 cross-dataset 재현 검정.

`manuscript/PREREGISTRATION_gse205117.md`의 봉인된 6개 예측을 **기계적으로** 통과/실패 판정한다.
사후 구제(post-hoc rescue)를 구조적으로 막는 것이 이 스크립트의 존재 이유다:

  - 임계·pair 선택·불일치 정의를 **fit CSV가 존재하기 전에** 코드로 고정했다(이 파일의 커밋 시점이 봉인).
  - 결과가 나쁘면 나쁜 대로 FAIL을 찍는다. 임계를 사후에 바꾸려면 git 이력에 남는다.

실행 (fit 3종 도착 후, kkkim 서버 scv-preprocess env):
    conda run --no-capture-output -n scv-preprocess python cross_dataset/p3_prereg_gse205117.py

입력 계약 (macrophage와 동일 규약, 첫 컬럼 = gene):
    results/rna_only_dynamical_genes_gse205117.csv   fit_alpha, fit_likelihood
    results/multivelo_genes_gse205117.csv            fit_alpha, fit_t_sw1, fit_t_sw2, fit_likelihood
    results/multivelovae_genes_gse205117.csv         vae_alpha, vae_alpha_c
    results/multivelo_genes.csv                      (HSPC, cross-dataset 축)
    results/moflow_genes_gse205117.csv               (선택 — 있으면 예측5를 HSPC 원정의로 채점)

출력: results/prereg_gse205117_scorecard.md  (+ .csv)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# 통계 구현은 검증된 macrophage 스크립트에서 그대로 재사용(중복 정의 금지 → 정의 드리프트 방지).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p3_concordance_macrophage import (  # noqa: E402
    RESULTS, SEED, B_DEFAULT, load, _upper, fast_spear, boot_ci, boot_dr, _pair,
)

SUFFIX = "_gse205117"

# ── 봉인된 임계 (PREREGISTRATION_gse205117.md 표와 1:1. 변경 금지 — 바꾸면 git에 남는다) ──
T1_ALPHA_WITHIN = 0.50   # 예측1: within cross-method α ρ ≥ 0.50
T2_LAG_WITHIN = 0.15     # 예측2: within cross-method lag ρ ≤ 0.15 (≈0)
T3_DELTA_RHO = 0.35      # 예측3: Δρ = ρ_α − ρ_lag ≥ 0.35
T4_CROSS_ALPHA = 0.20    # 예측4: cross α > +0.20 且 cross α > cross lag

# ── 채점 규칙: 사전등록 표가 문장 수준이라 아래 조작정의를 **데이터 보기 전에** 확정한다 ──
# (R1) 예측1의 "cross-method α"는 pair가 셋(floor×MV, floor×VAE, MV×VAE)이라 모호 → **median**을 헤드라인으로
#      쓴다. macrophage 보고(§판정)가 median을 쓴 전례와 동일. 세 pair 전부 표에 적는다.
# (R2) 예측2의 lag은 floor에 lag이 없으므로 **MV×VAE 단일 pair**. 모호성 없음.
#      MultiVelo lag 부호는 4-state 단조정렬로 구조적 양수(무정보) → **크기(rank)만** 비교. sign 검정 안 함.
# (R3) 예측3의 Δρ은 **동일 gene set에서 paired** 계산(boot_dr) — ρ_α(MV×VAE) − ρ_lag(MV×VAE).
#      서로 다른 gene set의 두 ρ를 빼는 것은 금지(가드레일).
# (R4) 예측5의 per-gene 불일치는 HSPC 원정의(`scripts/p3_identifiability_vs_snr.py` L6-12)를 **그대로** 따른다:
#         mv_lag = fit_t_sw2 − fit_t_sw1   (**부호 유지**. MV는 4-state 단조라 어차피 ≥0)
#         mf_lag = cs_lag_median            (**부호 유지** — MoFlow DTW lag은 음수 가능. abs 금지!)
#         rank   = pandas .rank(pct=True) = r/n   (0<r/n≤1)
#         lag_disagree   = |mv_lag_r − mf_lag_r| ;  alpha_disagree = |mv_alpha_r − vae_alpha_r|
#      → HSPC 기준값 lag 0.317 vs α 0.078 과 **같은 자로 재야** 비교가 성립한다.
#      ⚠️ 2026-07-13 kkkim이 사전등록에 **MoFlow arm 포함을 확정**(fit 산출 전 봉인) → 원정의로 채점한다.
#         MoFlow fit이 없으면 이는 **봉인된 결정과의 이탈**이므로, 조용히 VAE로 치환하지 않고
#         scorecard·stderr에 **이탈로 명시 경고**한다. 파일은 있는데 컬럼이 없으면 **하드 실패**(추측 금지).
# (R5) mouse → cross-dataset 축은 E18과 동일하게 **uppercase ortholog 매핑**(_upper). 완벽하지 않으며
#      누락분은 noise만 더해 "lag fragile" 결론에 **보수적**으로 작용한다.

# 예측2·3(concordance ρ, Δρ)용 lag = **크기 rank**(가드레일: MV 부호는 구조적 양수라 무정보).
LAG_MV = lambda d: (d["fit_t_sw2"] - d["fit_t_sw1"]).abs()          # noqa: E731
LAG_VAE = lambda d: (1.0 / d["vae_alpha_c"].clip(lower=1e-6)        # noqa: E731
                     - 1.0 / d["vae_alpha"].clip(lower=1e-6)).abs()

# 예측5(per-gene 불일치)용 lag = HSPC 원정의 — **부호 유지**(abs 금지). 위와 목적이 다르다.
SIGNED_LAG_MV = lambda d: d["fit_t_sw2"] - d["fit_t_sw1"]           # noqa: E731
MOFLOW_LAG_COL = "cs_lag_median"                                     # HSPC 원정의가 쓴 바로 그 컬럼


def pct_rank(v: np.ndarray) -> np.ndarray:
    """pandas .rank(pct=True) 와 동일 = 평균rank / n. HSPC 원정의(L10)와 자를 맞춘다."""
    from scipy.stats import rankdata
    return rankdata(v) / len(v)


def disagree_median(a: pd.Series, b: pd.Series) -> tuple[float, int]:
    """per-gene 불일치 median = median(|pct_rank_a − pct_rank_b|). rank는 공통 gene 안에서 계산."""
    sh, va, vb = _pair(a, b)
    if len(sh) < 10:
        return float("nan"), len(sh)
    return float(np.median(np.abs(pct_rank(va) - pct_rank(vb)))), len(sh)


def verdict(ok: bool | None) -> str:
    return "❌ FAIL" if ok is False else ("✅ PASS" if ok else "⚠️ N/A")


def main() -> int:
    rng = np.random.default_rng(SEED)
    B = B_DEFAULT

    fl = load(RESULTS / f"rna_only_dynamical_genes{SUFFIX}.csv")
    mv = load(RESULTS / f"multivelo_genes{SUFFIX}.csv")
    vae = load(RESULTS / f"multivelovae_genes{SUFFIX}.csv")
    mof = load(RESULTS / f"moflow_genes{SUFFIX}.csv")          # 선택 arm
    h_mv = load(RESULTS / "multivelo_genes.csv")              # HSPC 축

    missing = [n for n, d in [("floor", fl), ("multivelo", mv), ("multivelovae", vae)] if d is None]
    if missing:
        print(f"[중단] fit CSV 없음: {missing} — heavy-run 완료 후 실행하세요.", file=sys.stderr)
        return 2

    L: list[str] = ["# 사전등록 채점표 — GSE205117 (mouse gastrulation) 5번째 cross-dataset", "",
                    "> `manuscript/PREREGISTRATION_gse205117.md`의 봉인된 6개 예측을 기계적으로 채점한다.",
                    f"> paired bootstrap B={B:,}, seed={SEED}. **결과가 나쁘면 나쁜 대로 FAIL을 적는다(사후 구제 금지).**",
                    ""]
    rows: list[dict] = []

    # ── 예측 1: within cross-method α (median of 3 pairs) ──────────────
    a_pairs: dict[str, float] = {}
    for lab, x, y in [("floor×MV", fl.get("fit_alpha"), mv.get("fit_alpha")),
                      ("floor×VAE", fl.get("fit_alpha"), vae.get("vae_alpha")),
                      ("MV×VAE", mv.get("fit_alpha"), vae.get("vae_alpha"))]:
        if x is None or y is None:
            continue
        sh, va, vb = _pair(x, y)
        if len(sh) >= 10:
            pt, lo, hi = boot_ci(va, vb, rng, B)
            a_pairs[lab] = pt
            L.append(f"- α **{lab}** (shared {len(sh)}): Spearman **{pt:+.3f}** 95%CI [{lo:+.3f}, {hi:+.3f}]")
            rows.append(dict(section="within_alpha", label=lab, n=len(sh), rho=pt, lo=lo, hi=hi))
    a_med = float(np.median(list(a_pairs.values()))) if a_pairs else float("nan")
    p1 = bool(a_med >= T1_ALPHA_WITHIN) if a_pairs else None

    # ── 예측 2: within cross-method lag (MV×VAE, 크기 rank만) ───────────
    lag_mv, lag_vae = LAG_MV(mv), LAG_VAE(vae)
    sh_l, la, lb = _pair(lag_mv, lag_vae)
    p2 = p3 = None
    lag_rho = dr = float("nan")
    if len(sh_l) >= 10:
        lag_rho, l_lo, l_hi = boot_ci(la, lb, rng, B)
        p2 = bool(lag_rho <= T2_LAG_WITHIN)
        L += ["", f"- lag 크기 rank **MV×VAE** (shared {len(sh_l)}): Spearman **{lag_rho:+.3f}** "
              f"95%CI [{l_lo:+.3f}, {l_hi:+.3f}]",
              "  - sign 검정 생략: MultiVelo lag 부호는 4-state 단조정렬로 구조적 양수(무정보)."]
        rows.append(dict(section="within_lag", label="MV×VAE", n=len(sh_l), rho=lag_rho, lo=l_lo, hi=l_hi))

        # ── 예측 3: paired Δρ (동일 gene set) ──────────────────────────
        common = sorted(set(mv["fit_alpha"].dropna().index) & set(vae["vae_alpha"].dropna().index)
                        & set(lag_mv.dropna().index) & set(lag_vae.dropna().index))
        if len(common) >= 10:
            d = boot_dr(mv["fit_alpha"].loc[common].astype(float).values,
                        vae["vae_alpha"].loc[common].astype(float).values,
                        lag_mv.loc[common].astype(float).values,
                        lag_vae.loc[common].astype(float).values, rng, B)
            dr = d["dr"]
            p3 = bool(dr >= T3_DELTA_RHO)
            L += ["", f"- **Δρ = ρ_α − ρ_lag = {dr:+.3f}** 95%CI [{d['dr_lo']:+.3f}, {d['dr_hi']:+.3f}] "
                  f"(paired, 공통 {len(common)} gene)"]
            rows.append(dict(section="delta_rho", label="MV×VAE", n=len(common), rho=dr,
                             lo=d["dr_lo"], hi=d["dr_hi"]))

    # ── 예측 4: cross-dataset HSPC ↔ gastrulation (uppercase ortholog) ──
    p4 = None
    x_a = x_l = float("nan")
    if h_mv is not None:
        hu, gu = _upper(h_mv), _upper(mv)
        sh_a, ha, ga = _pair(hu["fit_alpha"], gu["fit_alpha"])
        sh_x, hl, gl = _pair(LAG_MV(hu), LAG_MV(gu))
        if len(sh_a) >= 10 and len(sh_x) >= 10:
            x_a, xa_lo, xa_hi = boot_ci(ha, ga, rng, B)
            x_l, xl_lo, xl_hi = boot_ci(hl, gl, rng, B)
            p4 = bool(x_a > T4_CROSS_ALPHA and x_a > x_l)
            L += ["", f"- cross **α rank** HSPC×gastrulation (shared {len(sh_a)}): **{x_a:+.3f}** "
                  f"95%CI [{xa_lo:+.3f}, {xa_hi:+.3f}]",
                  f"- cross **lag 크기 rank** HSPC×gastrulation (shared {len(sh_x)}): **{x_l:+.3f}** "
                  f"95%CI [{xl_lo:+.3f}, {xl_hi:+.3f}]",
                  "  - ⚠️ mouse→human은 uppercase ortholog 매핑(E18 전례). 누락분은 noise만 더해 결론에 보수적."]
            rows += [dict(section="cross_alpha", label="HSPC×gastr", n=len(sh_a), rho=x_a, lo=xa_lo, hi=xa_hi),
                     dict(section="cross_lag", label="HSPC×gastr", n=len(sh_x), rho=x_l, lo=xl_lo, hi=xl_hi)]

    # ── 예측 5: per-gene 재현 격차 — HSPC 원정의(부호 유지 MV vs MoFlow cs_lag_median) ──
    deviation = None
    if mof is not None:
        if MOFLOW_LAG_COL not in mof.columns:
            # 파일은 있는데 원정의 컬럼이 없다 → 추측하지 않고 하드 실패.
            print(f"[중단] moflow_genes{SUFFIX}.csv에 '{MOFLOW_LAG_COL}' 컬럼이 없습니다 "
                  f"(있는 컬럼: {list(mof.columns)[:8]}). HSPC 원정의로 채점할 수 없습니다.",
                  file=sys.stderr)
            return 3
        lag_a, lag_b = SIGNED_LAG_MV(mv), mof[MOFLOW_LAG_COL]
        lag_src = f"MoFlow `{MOFLOW_LAG_COL}` (HSPC 원정의, 부호 유지)"
    else:
        # 사전등록(2026-07-13)이 MoFlow 포함을 봉인했으므로, 부재는 '이탈'이다. 조용히 넘어가지 않는다.
        lag_a, lag_b = lag_mv, lag_vae
        lag_src = "MultiVeloVAE 치환 (⚠️ **봉인된 결정과의 이탈**)"
        deviation = (f"봉인된 사전등록(2026-07-13)은 예측5를 **MoFlow 원정의**로 채점하도록 확정했으나, "
                     f"`results/moflow_genes{SUFFIX}.csv`가 없어 MV×VAE로 치환했다. "
                     f"**이 채점은 사전등록대로가 아니다** — MoFlow arm 산출 후 재채점할 것.")
        print(f"[경고] {deviation}", file=sys.stderr)

    d_lag, n_lag = disagree_median(lag_a, lag_b)
    d_alpha, n_alpha = disagree_median(mv["fit_alpha"], vae["vae_alpha"])   # α는 원정의대로 MV vs VAE
    p5 = bool(d_lag > d_alpha) if not (np.isnan(d_lag) or np.isnan(d_alpha)) else None
    L += ["", f"- per-gene 불일치 median — **lag {d_lag:.3f}** (n={n_lag}, MV vs {lag_src}) "
          f"vs **α {d_alpha:.3f}** (n={n_alpha}, MV vs VAE)",
          "  - 불일치 = |pct_rank_A − pct_rank_B| (HSPC 원정의 `p3_identifiability_vs_snr.py`와 동일 자).",
          "  - HSPC 기준: lag **0.317** vs α **0.078** (α ~4배 재현). macrophage(치환 정의): 0.280 vs 0.061."]
    if deviation:
        L += [f"  - ⚠️ {deviation}"]
    rows.append(dict(section="per_gene_disagree", label=f"lag[{lag_src}]|alpha", n=n_lag,
                     rho=d_lag, lo=d_alpha, hi=np.nan))

    # ── 예측 6: priming 극대에서도 fragile = #2 且 #3 ──────────────────
    p6 = None if (p2 is None or p3 is None) else bool(p2 and p3)

    # ── 채점표 ─────────────────────────────────────────────────────────
    L += ["", "## 봉인된 예측 채점", "",
          "| # | 예측 | 사전 임계 | 실측 | 판정 |", "|---|---|---|---|---|",
          f"| 1 | within cross-method α 재현 | ρ ≥ {T1_ALPHA_WITHIN:.2f} | median **{a_med:+.3f}** "
          f"({', '.join(f'{k} {v:+.2f}' for k, v in a_pairs.items())}) | {verdict(p1)} |",
          f"| 2 | within cross-method lag 재현 | ρ ≤ {T2_LAG_WITHIN:.2f} | **{lag_rho:+.3f}** | {verdict(p2)} |",
          f"| 3 | α > lag 순서 | Δρ ≥ {T3_DELTA_RHO:.2f} | **{dr:+.3f}** | {verdict(p3)} |",
          f"| 4 | cross HSPC↔gastrulation | cross α > {T4_CROSS_ALPHA:+.2f} 且 > cross lag | "
          f"α **{x_a:+.3f}** / lag **{x_l:+.3f}** | {verdict(p4)} |",
          f"| 5 | per-gene 재현 격차 | lag 불일치 > α 불일치 | **{d_lag:.3f}** vs **{d_alpha:.3f}** | {verdict(p5)} |",
          f"| 6 | priming 극대에서도 fragile | #2 且 #3 | — | {verdict(p6)} |",
          ""]

    res = [p1, p2, p3, p4, p5, p6]
    n_pass, n_fail = sum(x is True for x in res), sum(x is False for x in res)
    L += [f"**종합: {n_pass} PASS / {n_fail} FAIL / {sum(x is None for x in res)} N/A**", ""]
    if n_fail:
        L += ["> ⚠️ **실패한 예측이 있다. 사전등록 원칙상 임계를 사후에 조정하지 않는다** — "
              "실패는 실패로 보고하고, 그것이 무엇을 뜻하는지 논의한다.", ""]
    if deviation:
        L += [f"> 🚨 **사전등록 이탈**: {deviation}", ""]
    L += ["## caveat",
          "- replication 1건 — 강한 일반화 금지. 5축(HSPC + 4 external) 순서 일관성으로만 서술.",
          "- cross-dataset은 uppercase ortholog(mouse→human) — 불완전 매핑, 결론에 보수적.",
          "- lag은 크기 rank만 비교(방향 아님): MultiVelo 부호는 구조적 양수(무정보).",
          "- concordance는 *전역* per-gene fit rank(within-lineage 아님).", ""]

    out = RESULTS / f"prereg{SUFFIX}_scorecard.md"
    out.write_text("\n".join(L), encoding="utf-8")
    pd.DataFrame(rows).to_csv(RESULTS / f"prereg{SUFFIX}_scorecard.csv", index=False)
    print("\n".join(L))
    print(f"\n[완료] {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
