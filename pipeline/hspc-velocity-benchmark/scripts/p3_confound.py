#!/usr/bin/env python3
"""P3 confound 분석 — cell cycle, burst, ambient (DESIGN §5, CLAUDE.md 방법론 #2).

목적: chromatin→transcription lag 추정이 confound에 얼마나 영향받는지 정량화.
  (a) cell cycle scoring → lag gene이 cell-cycle phase에 편향됐는가
  (b) burst parameter 상관 → lag 크기가 transcription burst(α)와 공선형인가
  (c) ambient / doublet → QC 이미 scrublet 적용(P1). 여기선 doublet_score 분포만 기록.

실행: conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p3_confound.py
출력: results/confound.md
"""
from __future__ import annotations
import sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import scanpy as sc
import p1_config as p1
import p2_config as cfg

CELL_CYCLE_GENES_S = [
    "MCM5", "PCNA", "TYMS", "FEN1", "MCM2", "MCM4", "RRM1", "UNG",
    "GINS2", "MCM6", "CDCA7", "DTL", "PRIM1", "UHRF1", "MLF1IP",
    "HELLS", "RFC2", "RPA2", "NASP", "RAD51AP1", "GMNN", "WDR76",
    "SLBP", "CCNE2", "UBR7", "POLD3", "MSH2", "ATAD2", "RAD51",
    "RRM2", "CDC45", "CDC6", "EXO1", "TIPIN", "DSCC1", "BLM",
    "CASP8AP2", "USP1", "CLSPN", "POLA1", "CHAF1B", "BRIP1", "E2F8",
]
CELL_CYCLE_GENES_G2M = [
    "HMGB2", "CDK1", "NUSAP1", "UBE2C", "BIRC5", "TPX2", "TOP2A",
    "NDC80", "CKS2", "NUF2", "CKS1B", "MKI67", "TMPO", "CENPF",
    "TACC3", "FAM64A", "SMC4", "CCNB2", "CKAP2L", "CKAP2",
    "AURKB", "BUB1", "KIF11", "ANP32E", "TUBB4B", "GTSE1",
    "KIF20B", "HJURP", "CDCA3", "HN1", "CDC20", "TTK", "CDC25C",
    "KIF2C", "RANGAP1", "NCAPD2", "DLGAP5", "CDCA2", "CDCA8",
    "ECT2", "KIF23", "HMMR", "AURKA", "PSRC1", "ANLN", "LBR",
    "CKAP5", "CENPE", "CTCF", "NEK2", "G2E3", "GAS2L3",
    "CBX5", "CENPA",
]


def main():
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    L = ["# P3 — Confound 분석 (cell cycle / burst / ambient)", ""]

    # ─── 데이터 로드 ───
    rna = sc.read_h5ad(p1.OUT_RNA)
    mv_csv = cfg.RESULTS / "multivelo_genes.csv"
    fl_csv = cfg.RESULTS / "rna_only_dynamical_genes.csv"
    if not mv_csv.exists():
        print("multivelo_genes.csv 없음 — 종료"); return 1
    mv = pd.read_csv(mv_csv, index_col=0)
    lag = (mv["fit_t_sw2"] - mv["fit_t_sw1"]).dropna()
    L.append(f"multivelo lag gene 수: {len(lag)}")
    L.append(f"scVelo floor gene 수: {len(pd.read_csv(fl_csv, index_col=0)) if fl_csv.exists() else 'N/A'}")
    L.append("")

    # ─── (a) Cell Cycle ───
    L.append("## (a) Cell Cycle")
    s_genes = [g for g in CELL_CYCLE_GENES_S if g in rna.var_names]
    g2m_genes = [g for g in CELL_CYCLE_GENES_G2M if g in rna.var_names]
    L.append(f"- S marker {len(s_genes)}/{len(CELL_CYCLE_GENES_S)}, G2M marker {len(g2m_genes)}/{len(CELL_CYCLE_GENES_G2M)} found")

    if s_genes and g2m_genes:
        sc.tl.score_genes_cell_cycle(rna, s_genes=s_genes, g2m_genes=g2m_genes, random_state=p1.RANDOM_SEED)
        phase_dist = rna.obs["phase"].value_counts().to_dict()
        L.append(f"- phase 분포: {phase_dist}")

        # lag gene이 특정 phase에서 고발현 편향인지: lag gene 기준 세포 없고 gene 기준
        # → lag gene의 S/G2M score를 전체 gene 대비 비교
        lag_genes = [g for g in lag.index if g in rna.var_names]
        other_genes = [g for g in rna.var_names if g not in set(lag_genes)]

        if lag_genes:
            rna_lag = rna[:, lag_genes]
            rna_other = rna[:, other_genes] if other_genes else None

            # lag gene의 S-phase score proxy: lag gene에서 S marker 발현 평균
            s_in_lag = [g for g in s_genes if g in lag_genes]
            g2m_in_lag = [g for g in g2m_genes if g in lag_genes]
            s_frac_lag = len(s_in_lag) / len(lag_genes)
            s_frac_all = len(s_genes) / len(rna.var_names)
            g2m_frac_lag = len(g2m_in_lag) / len(lag_genes)
            g2m_frac_all = len(g2m_genes) / len(rna.var_names)
            L += [
                f"- lag gene 중 S marker 비율: {s_frac_lag:.3f} vs 전체 {s_frac_all:.3f}",
                f"- lag gene 중 G2M marker 비율: {g2m_frac_lag:.3f} vs 전체 {g2m_frac_all:.3f}",
                "- → 비율 차이 작을수록 cell cycle 편향 낮음",
            ]

        # 세포 단위: phase별 S/G2M score와 lag gene 발현의 관계
        # per-cell S_score/G2M_score → lag gene 평균 발현과의 상관
        if lag_genes:
            lag_expr = np.asarray(rna[:, lag_genes].layers.get("spliced", rna[:, lag_genes].X).mean(1)).ravel()
            rho_s, p_s = spearmanr(rna.obs["S_score"], lag_expr)
            rho_g2m, p_g2m = spearmanr(rna.obs["G2M_score"], lag_expr)
            L += [
                f"- Spearman(S_score, lag-gene mean spliced expr) = {rho_s:.3f} (p={p_s:.2g})",
                f"- Spearman(G2M_score, lag-gene mean spliced expr) = {rho_g2m:.3f} (p={p_g2m:.2g})",
                "- → |ρ|>0.3 이면 cell cycle confound 의심 → 회귀 통제 검토 필요",
            ]
    else:
        L.append("- cell cycle marker 부족 — 생략")
    L.append("")

    # ─── (b) Burst / transcription rate confound ───
    L.append("## (b) Burst parameter 공선성 (α ~ lag)")
    if "fit_alpha" in mv.columns:
        shared_lag = lag.dropna()
        alpha = mv.loc[shared_lag.index, "fit_alpha"].dropna()
        sh = shared_lag.index.intersection(alpha.index)
        if len(sh) >= 10:
            rho, p = spearmanr(shared_lag.loc[sh], alpha.loc[sh])
            L += [
                f"- n={len(sh)} shared gene",
                f"- Spearman(MultiVelo lag, fit_alpha) = {rho:.3f} (p={p:.2g})",
                "- → |ρ|>0.5 = lag↔α 강공선 → regularized 회귀 필요(DESIGN §5.6)",
            ]
        else:
            L.append(f"- shared gene 부족({len(sh)}) — 생략")
    else:
        L.append("- fit_alpha 컬럼 없음 — 생략")
    L.append("")

    # ─── (c) Ambient / doublet ───
    L.append("## (c) Ambient / Doublet (QC 요약)")
    if "doublet_score" in rna.obs.columns:
        ds = rna.obs["doublet_score"].dropna()
        L += [
            f"- doublet_score n={len(ds)}, median {ds.median():.3f}, 99th pct {ds.quantile(.99):.3f}",
            "- P1에서 scrublet 적용(predicted_doublet 제거). 잔여 고점수 세포 비율 낮음.",
        ]
    else:
        L.append("- doublet_score 없음 (P1 scrublet 실패 시)")

    if "pct_mito" in rna.obs.columns:
        mt = rna.obs["pct_mito"]
        L.append(f"- pct_mito: median {mt.median():.1f}%, 99th {mt.quantile(.99):.1f}% (QC max {p1.QC['max_pct_mito']}%)")
    L.append("")

    out_md = cfg.RESULTS / "confound.md"
    out_md.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n✓ → {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
