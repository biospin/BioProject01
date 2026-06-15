#!/usr/bin/env python3
"""P3 — method 간 lag 일치도 + construct-validity (DESIGN §4B/§6).

현재 가능한 부분(전역 fit 기준):
  1. construct-validity sign check — known marker gene에서 MultiVelo lag(sw2-sw1) 부호가 타당한가.
  2. method 간 timing 일치도 — shared gene에서 Spearman(floor fit_t_ vs MultiVelo fit_t_sw2) + rate params.
  3. MultiVelo lag 분포(중앙값, chromatin-leads 비율).

⚠️ 한계(명시): switch time은 *전역* fit(gene당 1값)이라 진짜 within-lineage 일치도는
   per-lineage fit이 필요(추후). H1 stability(bootstrap)·다중 chromatin-aware method 일치도는
   MultiVeloVAE/MoFlow arm 추가 후. 이 스크립트는 method가 늘면 자동 확장(METHODS dict).

실행: conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p3_concordance.py
출력: results/concordance.md, results/concordance_shared.csv
"""
from __future__ import annotations
import sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import p2_config as cfg
import p1_config as p1

# method → (csv, lag 정의). lag = chromatin→transcription (양수=chromatin 선행).
METHODS = {
    "multivelo": dict(csv=cfg.RESULTS / "multivelo_genes.csv",
                      lag=lambda d: d["fit_t_sw2"] - d["fit_t_sw1"],
                      timing="fit_t_sw2"),                  # RNA 유도 switch
    # floor(scVelo)는 chromatin 없음 → lag 없음. timing(fit_t_)만 비교용.
    "scvelo_floor": dict(csv=cfg.RESULTS / "rna_only_dynamical_genes.csv",
                         lag=None, timing="fit_t_"),
}
# construct-validity marker (lineage). 양수 lag(chromatin 선행) 기대.
MARKERS = {k: v for k, v in p1.LINEAGE_MARKERS.items()}


def load(m):
    d = pd.read_csv(METHODS[m]["csv"], index_col=0)
    return d[d["fit_likelihood"].notna()] if "fit_likelihood" in d else d


def main():
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    L = ["# P3 — Concordance & construct-validity", ""]
    data = {m: load(m) for m in METHODS}
    for m, d in data.items():
        L.append(f"- **{m}**: fit gene {len(d)}")
    L.append("")

    # 1. MultiVelo lag 분포
    mv = data["multivelo"]
    lag = METHODS["multivelo"]["lag"](mv).dropna()
    pos = float((lag > 0).mean())
    L += ["## 1. MultiVelo lag (fit_t_sw2 − fit_t_sw1, pseudotime)",
          f"- n={len(lag)}, median **{lag.median():.2f}**, mean {lag.mean():.2f}, "
          f"IQR [{lag.quantile(.25):.2f}, {lag.quantile(.75):.2f}]",
          f"- lag>0 비율 {pos:.1%}",
          "- ⚠️ **구조적 caveat**: MultiVelo 4-state는 switch time을 **단조 정렬**(t_sw1<t_sw2<t_sw3)하므로 "
          "`sw2−sw1`은 *정의상 항상 양수*다. 따라서 100%는 priming 증거가 아니라 모델 제약 — "
          "**sign은 무정보, lag *크기*의 gene간 변이만 정보**다. 진짜 directional sign check는 "
          "sign이 가변인 method(MoFlow DTW c-s lag 등)에서 수행해야 함(DESIGN §4B).", ""]

    # 2. construct-validity: marker gene lag 부호
    L += ["## 2. Construct-validity — marker gene lag (크기)", "",
          "> sign은 §1 caveat대로 구조적 양수 → 여기선 **lag 크기**(gene간 변이)를 본다.",
          "",
          "| lineage | gene | lag(sw2-sw1) | sw1 | sw2 |", "|---|---|---|---|---|"]
    cv_rows = 0
    for lin, gs in MARKERS.items():
        for g in gs:
            if g in mv.index:
                s1, s2 = mv.loc[g, "fit_t_sw1"], mv.loc[g, "fit_t_sw2"]
                lg = s2 - s1
                L.append(f"| {lin} | {g} | {lg:.2f} | {s1:.2f} | {s2:.2f} |")
                cv_rows += 1
    if cv_rows == 0:
        L.append("| — | (fit된 marker 없음) | | | |")
    L.append("")

    # 3. method 간 timing 일치도 (shared gene)
    L += ["## 3. Method 간 timing 일치도 (shared fit gene)", ""]
    fl = data["scvelo_floor"]
    shared = sorted(set(mv.index) & set(fl.index))
    L.append(f"- floor ∩ MultiVelo shared fit gene: **{len(shared)}**")
    out_shared = None
    if len(shared) >= 10:
        a = fl.loc[shared, "fit_t_"].astype(float)
        b = mv.loc[shared, "fit_t_sw2"].astype(float)
        rho, p = spearmanr(a, b)
        L.append(f"- Spearman(floor fit_t_, MultiVelo fit_t_sw2) = **{rho:.3f}** (p={p:.2g}) "
                 f"— RNA 유도 timing 일치도(sanity)")
        # rate params 교차 일치도
        for prm in ["fit_alpha", "fit_beta", "fit_gamma"]:
            if prm in fl and prm in mv:
                r, _ = spearmanr(fl.loc[shared, prm].astype(float),
                                 mv.loc[shared, prm].astype(float))
                L.append(f"  - Spearman({prm}) = {r:.3f}")
        out_shared = pd.DataFrame({
            "floor_t": a, "mv_t_sw2": b,
            "mv_lag_sw2_sw1": (mv.loc[shared, "fit_t_sw2"] - mv.loc[shared, "fit_t_sw1"]).astype(float),
        })
    else:
        L.append("- shared gene 부족(<10) → 일치도 생략")
    L.append("")

    # 4. 한계/다음
    L += ["## 4. 한계 · 다음 (DESIGN §4)",
          "- ⚠️ switch time은 *전역* fit → 진짜 within-lineage 일치도는 per-lineage fit 필요(추후).",
          "- ⚠️ H1(agreement gene의 bootstrap lag-sign stability)·다중 chromatin-aware method 일치도는 "
          "**MultiVeloVAE/MoFlow arm 추가 후** (현재 chromatin-aware=MultiVelo 단독).",
          "- sign-agreement vs rank-corr 분리 보고 원칙: method가 2+ chromatin-aware일 때 적용.", ""]

    out_md = cfg.RESULTS / "concordance.md"
    out_md.write_text("\n".join(L), encoding="utf-8")
    if out_shared is not None:
        out_shared.to_csv(cfg.RESULTS / "concordance_shared.csv")
    print("\n".join(L))
    print(f"\n✓ → {out_md.name}" + ("" if out_shared is None else " + concordance_shared.csv"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
