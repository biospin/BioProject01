#!/usr/bin/env python3
"""fig01 — P2 결과 요약: MultiVelo lag 분포 + method 간 일치도 + marker lag.

입력: results/multivelo_genes.csv, results/rna_only_dynamical_genes.csv (+ p1_config marker)
출력: figures/fig01_p2_concordance.png  (이미지는 gitignore, 이 스크립트만 tracked)

실행: conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/figures/fig01_p2_concordance.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import p2_config as cfg
import p1_config as p1

mv = pd.read_csv(cfg.RESULTS / "multivelo_genes.csv", index_col=0)
fl = pd.read_csv(cfg.RESULTS / "rna_only_dynamical_genes.csv", index_col=0)
mv = mv[mv["fit_likelihood"].notna()]; fl = fl[fl["fit_likelihood"].notna()]
lag = (mv["fit_t_sw2"] - mv["fit_t_sw1"]).dropna()
shared = sorted(set(mv.index) & set(fl.index))

fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))

# A. MultiVelo lag 분포 (크기; sign은 구조적이라 무정보 — 캡션 명시)
ax[0].hist(lag, bins=40, color="#4C72B0", edgecolor="white")
ax[0].axvline(lag.median(), color="crimson", ls="--", label=f"median {lag.median():.2f}")
ax[0].set(title=f"A. MultiVelo lag (sw2-sw1), n={len(lag)}",
          xlabel="lag (pseudotime) — magnitude only (sign structural)", ylabel="genes")
ax[0].legend()

# B. rate(alpha) 교차 일치도 — 강함(0.82); timing은 약함을 대비로
a = fl.loc[shared, "fit_alpha"].astype(float); b = mv.loc[shared, "fit_alpha"].astype(float)
r_a, _ = spearmanr(a, b)
ax[1].scatter(np.log1p(a), np.log1p(b), s=10, alpha=0.5, color="#55A868")
ax[1].set(title=f"B. transcription rate alpha (Spearman {r_a:.2f})",
          xlabel="floor log1p(α)", ylabel="MultiVelo log1p(α)")

# C. timing(switch) 불일치 — 대비
ta = fl.loc[shared, "fit_t_"].astype(float); tb = mv.loc[shared, "fit_t_sw2"].astype(float)
r_t, _ = spearmanr(ta, tb)
ax[2].scatter(ta, tb, s=10, alpha=0.5, color="#C44E52")
ax[2].set(title=f"C. absolute timing (Spearman {r_t:.2f})",
          xlabel="floor fit_t_", ylabel="MultiVelo fit_t_sw2")

fig.suptitle("P2 — RNA-only floor vs MultiVelo (shared {} genes): rates agree, absolute timing does not"
             .format(len(shared)), y=1.02, fontsize=11)
fig.tight_layout()
out = Path(__file__).resolve().parent / "fig01_p2_concordance.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print(f"✓ saved {out.name} | lag median {lag.median():.2f}, α-Spearman {r_a:.2f}, timing-Spearman {r_t:.2f}")
