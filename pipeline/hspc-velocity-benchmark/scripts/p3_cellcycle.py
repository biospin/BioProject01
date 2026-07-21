#!/usr/bin/env python3
"""P3 — cell-cycle confound *gene-level* 심화 (p3_confound 보완).

p3_confound.py는 *세포* 수준(S_score vs lag-gene 평균발현 ρ≈0.33)을 봤다. 여기선 *gene* 수준에서
"cell-cycle가 lag 추정 자체를 편향시키는가"를 refit 없이 직접 검정한다 → regressed refit이
정말 필요한지의 게이트.

검정:
  1. fit된 lag gene 중 cell-cycle gene(S/G2M) 비율 + lag 분포 비교(cell-cycle vs 나머지, Mann-Whitney).
  2. cell-cycle gene 제외 시 lag 분포(median/IQR) 변화 — 결론이 cell-cycle gene에 의존하는가.
  3. (세포) S_score/G2M_score가 pseudotime/lineage와 구조적으로 얽혔는가(진짜 confound vs 무관 변이).

결정 규칙: cell-cycle gene의 lag이 유의하게 다르고(p<0.05) 비율이 높으면(>10%) → regressed refit 필요.
          아니면 cell-cycle는 lag 결론에 비편향 → 통제 불요(또는 sensitivity로만 보고).

실행: conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p3_cellcycle.py
출력: results/cellcycle_genelevel.md
"""
from __future__ import annotations
import sys
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
import scanpy as sc
import p1_config as p1
import p2_config as cfg
from p3_confound import CELL_CYCLE_GENES_S, CELL_CYCLE_GENES_G2M


def main():
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    L = ["# P3 — Cell-cycle confound (gene-level, refit 없이)", ""]

    mv_csv = cfg.RESULTS / "multivelo_genes.csv"
    if not mv_csv.exists():
        print("multivelo_genes.csv 없음 — 종료"); return 1
    mv = pd.read_csv(mv_csv, index_col=0)
    mv = mv[mv["fit_likelihood"].notna()]
    lag = (mv["fit_t_sw2"] - mv["fit_t_sw1"]).dropna()
    cc_genes = set(CELL_CYCLE_GENES_S) | set(CELL_CYCLE_GENES_G2M)

    # ── 1. fit lag gene 중 cell-cycle 비율 + lag 분포 비교 ──
    is_cc = lag.index.isin(cc_genes)
    lag_cc, lag_other = lag[is_cc], lag[~is_cc]
    frac = is_cc.mean()
    L += ["## 1. fit lag gene 중 cell-cycle gene",
          f"- fit lag gene n={len(lag)} 중 cell-cycle gene **{is_cc.sum()}개 ({frac:.1%})**",
          f"- cell-cycle gene lag: n={len(lag_cc)}, median {lag_cc.median():.2f}" if len(lag_cc) else "- cell-cycle gene fit 없음",
          f"- 나머지 gene lag: n={len(lag_other)}, median {lag_other.median():.2f}"]
    if len(lag_cc) >= 3 and len(lag_other) >= 3:
        u, p = mannwhitneyu(lag_cc, lag_other, alternative="two-sided")
        L.append(f"- Mann-Whitney(cell-cycle lag vs 나머지) p={p:.3g} "
                 f"→ {'유의차 ⚠️' if p < 0.05 else '유의차 없음 ✓'}")
    else:
        p = None
        L.append("- (cell-cycle fit gene 부족 → 검정 생략)")
    L.append("")

    # ── 2. cell-cycle gene 제외 시 lag 분포 변화 ──
    lag_excl = lag[~is_cc]
    L += ["## 2. cell-cycle gene 제외 시 lag 분포 변화",
          f"- 전체:        median {lag.median():.2f}, IQR [{lag.quantile(.25):.2f}, {lag.quantile(.75):.2f}]",
          f"- CC 제외:     median {lag_excl.median():.2f}, IQR [{lag_excl.quantile(.25):.2f}, {lag_excl.quantile(.75):.2f}]",
          f"- median 변화 {abs(lag.median()-lag_excl.median()):.3f} pseudotime "
          f"→ {'작음(결론 안정) ✓' if abs(lag.median()-lag_excl.median())<0.5 else '큼 ⚠️'}", ""]

    # ── 3. 세포: cell-cycle score가 pseudotime/lineage와 구조적으로 얽혔나 ──
    L += ["## 3. cell-cycle score vs trajectory 구조 (진짜 confound 여부)"]
    rna = sc.read_h5ad(p1.OUT_RNA)
    s_g = [g for g in CELL_CYCLE_GENES_S if g in rna.var_names]
    g2m_g = [g for g in CELL_CYCLE_GENES_G2M if g in rna.var_names]
    if s_g and g2m_g:
        sc.tl.score_genes_cell_cycle(rna, s_genes=s_g, g2m_genes=g2m_g, random_state=p1.RANDOM_SEED)
        ptkey = next((k for k in ("latent_time", "dpt_pseudotime", "palantir_pseudotime",
                                  "velocity_pseudotime") if k in rna.obs), None)
        if ptkey:
            for sc_key in ("S_score", "G2M_score"):
                rho, pp = spearmanr(rna.obs[ptkey], rna.obs[sc_key])
                L.append(f"- Spearman({ptkey}, {sc_key}) = {rho:+.3f} (p={pp:.2g})")
            L.append("- → |ρ|이 크면 cell-cycle가 trajectory 따라 구조적(통제 시 신호 일부 제거 위험), "
                     "작으면 lag에 직교(통제 안전).")
        else:
            L.append("- pseudotime obs 없음 → trajectory 얽힘 검정 생략 (P3 pseudotime 산출 후)")
        lin_key = next((k for k in ("lineage", "celltype", "cell_type") if k in rna.obs), None)
        if lin_key:
            ph = pd.crosstab(rna.obs[lin_key], rna.obs["phase"], normalize="index")
            cyc = (ph.get("S", 0) + ph.get("G2M", 0))
            L.append(f"- lineage별 cycling(S+G2M) 비율: "
                     + ", ".join(f"{k} {v:.0%}" for k, v in cyc.sort_values(ascending=False).items()))
    else:
        L.append("- cell-cycle marker 부족 — 생략")
    L.append("")

    # ── 결정 ──
    needs = (p is not None and p < 0.05 and frac > 0.10) or \
            (abs(lag.median() - lag_excl.median()) >= 0.5)
    L += ["## 결정",
          f"- regressed refit 필요? **{'예 — 통제 후 lag 재산출 권장' if needs else '아니오 — cell-cycle는 lag 결론에 비편향(sensitivity로만 보고)'}**",
          f"  - 근거: cell-cycle gene 비율 {frac:.1%}, lag 차이 검정 p="
          f"{'%.3g' % p if p is not None else 'NA'}, CC제외 median 변화 "
          f"{abs(lag.median()-lag_excl.median()):.3f}.",
          "- (full regressed refit = p2_multivelo.py --regress-cellcycle, ~수 h)"]

    out = cfg.RESULTS / "cellcycle_genelevel.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n✓ → {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
