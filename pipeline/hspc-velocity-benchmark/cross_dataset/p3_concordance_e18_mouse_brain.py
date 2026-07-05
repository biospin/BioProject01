#!/usr/bin/env python3
"""P3 concordance — Track D (E18 mouse brain) replication of the HSPC lag/α finding.

핵심 질문: HSPC 결론 "gene별 chromatin→transcription **lag은 method-robust하지 않지만**
transcription rate **α는 robust(cross-method ρ≈0.88)**"가 비-조혈(태아 뇌)에서 재현되나?

두 축으로 검정(각각 gene-axis 요구가 다름 — advisor):
  A. **Within-E18 cross-method** (동일 데이터셋, 같은 gene축 → 매핑 불필요):
     - α robust leg: floor·MV·VAE 사이 fit α pairwise Spearman
     - lag fragile leg: chromatin-aware 2개(MV, VAE) 사이 lag *크기* rank Spearman
       (floor는 RNA-only라 lag 없음 → lag는 MV×VAE만 가능)
  B. **Cross-dataset HSPC↔E18** (다른 데이터셋; mouse Title-case ≠ human UPPER →
     반드시 uppercase 매핑 후 교집합, 안 하면 shared≈0 = STATUS.md trap #1):
     - MV lag-크기 rank (HSPC↔E18) vs α rank (HSPC↔E18)

lag 정의:
  - MultiVelo: fit_t_sw2 − fit_t_sw1 (pseudotime; 4-state 단조정렬 → **sign 구조적 양수=무정보**, 크기 rank만)
  - MultiVeloVAE: 1/vae_alpha_c − 1/vae_alpha (chromatin 개방 시간 − RNA 유도 시간; sign 가변)
sign-agreement은 **양쪽 sign-informative일 때만** 유효 → MV(구조적)×VAE는 무의미(p3_concordance.py와 동일 규칙).

실행: conda run -n scv-preprocess python cross_dataset/p3_concordance_e18_mouse_brain.py
출력: results/concordance_e18_mouse_brain.md
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DS = "e18_mouse_brain"
MIN_SHARED = 10


def load(path: Path):
    if not path.exists():
        return None
    d = pd.read_csv(path, index_col=0)
    return d[d["fit_likelihood"].notna()] if "fit_likelihood" in d.columns else d


def rho_line(a: pd.Series, b: pd.Series, label: str, sign_informative=False):
    """shared index Spearman. sign_informative=True면 sign-agreement도 계산."""
    a, b = a.dropna(), b.dropna()
    sh = sorted(set(a.index) & set(b.index))
    n = len(sh)
    if n < MIN_SHARED:
        return f"- **{label}**: shared {n} (<{MIN_SHARED}) → 비정보(생략)", None, n
    av, bv = a.loc[sh].astype(float), b.loc[sh].astype(float)
    rho, p = spearmanr(av, bv)
    extra = ""
    if sign_informative:
        sa = float((np.sign(av) == np.sign(bv)).mean())
        extra = f" | sign-agreement {sa:.1%}"
    return f"- **{label}** (shared {n}): Spearman **{rho:+.3f}** (p={p:.2g}){extra}", float(rho), n


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    # ── E18 arms ──
    e_fl = load(RESULTS / f"rna_only_dynamical_genes_{DS}.csv")
    e_mv = load(RESULTS / f"multivelo_genes_{DS}.csv")
    e_vae = load(RESULTS / f"multivelovae_genes_{DS}.csv")
    # ── HSPC baselines (cross-dataset) ──
    h_mv = load(RESULTS / "multivelo_genes.csv")
    h_fl = load(RESULTS / "rna_only_dynamical_genes.csv")

    L = [f"# P3 concordance — Track D: E18 mouse brain replication of HSPC lag/α finding", "",
         "> 질문: HSPC 결론 **\"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.88)\"**가 "
         "비-조혈(E18 태아 뇌 10x Multiome, MultiVelo 튜토리얼 데이터)에서 재현되나?", "",
         "## 실행된 method arm", ""]
    arms = [("scVelo floor (RNA-only)", e_fl, "fit_alpha"),
            ("MultiVelo (chromatin-aware)", e_mv, "fit_alpha / fit_t_sw*"),
            ("MultiVeloVAE (chromatin-aware)", e_vae, "vae_alpha / vae_alpha_c")]
    L.append("| arm | fit gene | rate/lag 컬럼 |")
    L.append("|---|---|---|")
    for name, d, cols in arms:
        L.append(f"| {name} | {len(d) if d is not None else '**없음**'} | {cols} |")
    L.append("")

    # ── A. Within-E18 cross-method ──
    L += ["## A. Within-E18 cross-method concordance", "",
          "동일 데이터셋·동일 gene축 → ortholog/case 매핑 불필요.", ""]

    # A1. α (rate) — robust leg
    L += ["### A1. transcription rate α (robust leg 기대)", ""]
    alpha = {}
    if e_fl is not None and "fit_alpha" in e_fl: alpha["floor"] = e_fl["fit_alpha"]
    if e_mv is not None and "fit_alpha" in e_mv: alpha["MV"] = e_mv["fit_alpha"]
    if e_vae is not None and "vae_alpha" in e_vae: alpha["VAE"] = e_vae["vae_alpha"]
    a_rhos = []
    names = list(alpha)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            A, B = names[i], names[j]
            line, r, n = rho_line(alpha[A], alpha[B], f"α: {A} × {B}")
            L.append(line)
            if r is not None:
                a_rhos.append(r)
    if not a_rhos:
        L.append("- α 비교 가능한 method 쌍 없음 (2개+ arm 필요).")
    L.append("")

    # A2. lag — fragile leg (chromatin-aware 2개 필요: MV × VAE)
    L += ["### A2. chromatin→transcription lag (fragile leg 기대)", "",
          "> floor는 RNA-only라 lag 없음 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정 가능.", ""]
    lag = {}
    if e_mv is not None and {"fit_t_sw1", "fit_t_sw2"} <= set(e_mv.columns):
        lag["MV"] = (e_mv["fit_t_sw2"] - e_mv["fit_t_sw1"])          # sign 구조적
    if e_vae is not None and {"vae_alpha_c", "vae_alpha"} <= set(e_vae.columns):
        lag["VAE"] = (1.0 / e_vae["vae_alpha_c"].clip(1e-6) - 1.0 / e_vae["vae_alpha"].clip(1e-6))  # sign 가변
    lag_rho = None
    if len(lag) >= 2:
        line, lag_rho, n = rho_line(lag["MV"].abs(), lag["VAE"].abs(),
                                    "lag **크기** rank: MV × VAE")
        L.append(line)
        L.append("- ⚠️ sign-agreement 생략: MultiVelo lag sign은 4-state 단조정렬로 **구조적 양수(무정보)** → "
                 "MV×VAE 방향 일치는 정의상 의미 없음(양쪽 sign-informative일 때만 유효, p3_concordance.py 규칙).")
    else:
        L.append(f"- chromatin-aware lag method {len(lag)}개 ({list(lag)}) → 2개+ 필요. "
                 "VAE 완주 후 MV×VAE lag concordance 산출됨.")
    L.append("")

    # ── B. Cross-dataset HSPC ↔ E18 (uppercase 매핑) ──
    L += ["## B. Cross-dataset HSPC ↔ E18 (mouse→UPPER 매핑)", "",
          "> mouse Title-case(Gata1) ≠ human UPPER(GATA1) → uppercase 후 교집합. "
          "매핑 안 하면 shared≈0 (STATUS.md trap #1).", ""]
    b_lag_rho = b_alpha_rho = None
    if h_mv is not None and e_mv is not None:
        e_mv_u = e_mv.copy(); e_mv_u.index = e_mv_u.index.str.upper()
        e_mv_u = e_mv_u[~e_mv_u.index.duplicated()]
        raw_shared = len(set(h_mv.index) & set(e_mv.index))
        up_shared = len(set(h_mv.index) & set(e_mv_u.index))
        L.append(f"- shared gene: raw(case mismatch) **{raw_shared}** → uppercase 매핑 후 **{up_shared}** "
                 "(trap 실측: 매핑 없으면 near-zero).")
        # MV lag magnitude rank
        h_lag = (h_mv["fit_t_sw2"] - h_mv["fit_t_sw1"]).abs()
        e_lag = (e_mv_u["fit_t_sw2"] - e_mv_u["fit_t_sw1"]).abs()
        line, b_lag_rho, n = rho_line(h_lag, e_lag, "MV lag 크기 rank: HSPC × E18")
        L.append(line)
        # alpha rank
        line, b_alpha_rho, n = rho_line(h_mv["fit_alpha"], e_mv_u["fit_alpha"],
                                        "MV α rank: HSPC × E18")
        L.append(line)
        # floor alpha rank (sanity, chromatin 무관)
        if h_fl is not None and e_fl is not None:
            e_fl_u = e_fl.copy(); e_fl_u.index = e_fl_u.index.str.upper()
            e_fl_u = e_fl_u[~e_fl_u.index.duplicated()]
            line, r, n = rho_line(h_fl["fit_alpha"], e_fl_u["fit_alpha"],
                                  "floor α rank: HSPC × E18 (sanity)")
            L.append(line)
    else:
        L.append("- HSPC 또는 E18 MultiVelo csv 없음 → cross-dataset 비교 skip.")
    L.append("")

    # ── 판정 ──
    L += ["## 판정 — 'lag-fragile / α-robust' 패턴 재현?", ""]

    def _fmt(x): return f"{x:+.3f}" if x is not None else "N/A"
    a_alpha_med = float(np.median(a_rhos)) if a_rhos else None
    L.append(f"- Within-E18 α (cross-method) Spearman: {[f'{r:+.2f}' for r in a_rhos] or 'N/A'} "
             f"(중앙값 {_fmt(a_alpha_med)})")
    L.append(f"- Within-E18 lag 크기 rank (MV×VAE): {_fmt(lag_rho)}")
    L.append(f"- Cross-dataset HSPC↔E18: lag 크기 rank {_fmt(b_lag_rho)} vs α rank {_fmt(b_alpha_rho)}")
    L.append("")

    # verdict logic
    verdict, why = _verdict(a_alpha_med, lag_rho, b_lag_rho, b_alpha_rho)
    L.append(f"### → **{verdict}**")
    L.append(f"- {why}")
    L += ["",
          "## caveat (필수)",
          "- lag 크기 rank만 비교(방향 아님): MultiVelo sign은 4-state 단조정렬로 구조적 양수(무정보).",
          "- 단일 외부 데이터셋 replication 1건 — 강한 일반화 주장 금지. HSPC + human_brain + E18 3개 축의 "
          "일관성으로만 서사.",
          "- concordance는 *전역* per-gene fit rank (within-lineage 아님). E18 lineage(제공 celltype)는 "
          "load-bearing 아님.",
          "- E18 spliced/unspliced와 HSPC의 것은 서로 다른 원천 → cross-dataset rank에 noise만 추가 "
          "(낮은 rho=lag fragile에 보수적, 높은 rho=강한 신호).", ""]

    out = RESULTS / f"concordance_{DS}.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n✓ → {out}")
    return 0


def _verdict(a_alpha, lag_within, b_lag, b_alpha):
    """재현 판정. α robust(높음) + lag fragile(낮음) = 재현."""
    def hi(x): return x is not None and abs(x) > 0.5
    def lo(x): return x is not None and abs(x) <= 0.3
    alpha_robust = hi(a_alpha) or hi(b_alpha)
    # lag fragile 근거: within-E18 MV×VAE 낮음 또는 cross-dataset 낮음
    lag_fragile_within = lo(lag_within)
    lag_fragile_cross = lo(b_lag)
    lag_tested = (lag_within is not None) or (b_lag is not None)

    if not alpha_robust and a_alpha is None and b_alpha is None:
        return ("판정 보류 — α/lag 지표 부족",
                "필요한 arm(최소 floor+MV, lag는 MV+VAE)이 아직 안 끝남.")
    if alpha_robust and (lag_fragile_within or lag_fragile_cross):
        legs = []
        if lag_within is not None:
            legs.append(f"within-E18 MV×VAE lag {lag_within:+.2f}")
        if b_lag is not None:
            legs.append(f"cross-dataset lag {b_lag:+.2f}")
        return ("재현 YES — 'lag-fragile / α-robust' 패턴 재현",
                f"α는 cross-method/cross-dataset에서 강함(≈{a_alpha if a_alpha is not None else b_alpha:+.2f}), "
                f"lag는 약함({', '.join(legs)}). HSPC 서사 일치.")
    if alpha_robust and not lag_tested:
        return ("재현 PARTIAL — α-robust만 확인",
                "α robust leg 재현. lag fragile leg는 chromatin-aware 2번째(VAE) 완주 또는 "
                "cross-dataset MV lag rank 필요.")
    if alpha_robust and not (lag_fragile_within or lag_fragile_cross):
        return ("재현 PARTIAL — α-robust 확인, lag는 예상보다 강함",
                f"α robust이나 lag rank가 |r|>0.3 (within {lag_within}, cross {b_lag}) — "
                "E18에서는 lag가 HSPC보다 덜 fragile할 수 있음. 정직하게 보고.")
    return ("재현 약함/불명확",
            f"α robust={alpha_robust}, lag fragile(within)={lag_fragile_within}, "
            f"lag fragile(cross)={lag_fragile_cross} — 지표 재확인 필요.")


if __name__ == "__main__":
    sys.exit(main())
