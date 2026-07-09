#!/usr/bin/env python3
"""P3 concordance — HSPC→macrophage differentiation replication of the HSPC lag/α finding.

핵심 질문: HSPC 결론 "gene별 chromatin→transcription **lag은 method-robust하지 않지만**
transcription rate **α는 robust(cross-method ρ≈0.88)**"가 **같은 human 조혈축의 하류(단핵구→대식세포
분화; MultiVeloVAE 신규 데이터셋)**에서 재현되나? — same-lineage 하류 확장, drug-timing endpoint 근접.

BMMC 스크립트를 미러(human↔human이라 case/ortholog 매핑 불필요; HSPC와 gene SYMBOL 축 직접 겹침).
방어적으로 양쪽 uppercase 정규화만 적용.

두 축:
  A. Within-macrophage cross-method (동일 데이터셋):
     - α robust leg: floor·MV·VAE 사이 fit α pairwise Spearman
     - lag fragile leg: chromatin-aware 2개(MV, VAE) 사이 lag *크기* rank Spearman
  B. Cross-dataset HSPC↔macrophage (같은 human 조혈, 직접 gene 매칭):
     - MV lag-크기 rank vs α rank

lag 정의 (p3_concordance.py / BMMC와 동일):
  - MultiVelo:    fit_t_sw2 − fit_t_sw1 (pseudotime; 4-state 단조정렬 → sign 구조적 양수=무정보, 크기 rank만)
  - MultiVeloVAE: 1/vae_alpha_c − 1/vae_alpha (sign 가변)
sign-agreement은 양쪽 sign-informative일 때만 유효 → MV(구조적)×VAE는 무의미.

⚠️ 데이터셋 caveat (build_macrophage.py 참조):
  - figshare postpro는 **HVG 필터+moments 완료**(Ms/Mu). raw spliced/unspliced 없으면 moment fallback →
    공통 전처리 분기점이 다른 3종과 어긋남(방법론 #5). concordance엔 noise만 추가(lag-fragile에 보수적).
  - concat에서 macrophage batch(9060-MV-3)만 subset(HSPC leakage 차단).

실행: conda run -n scv-preprocess python cross_dataset/p3_concordance_macrophage.py
출력: results/concordance_macrophage.md
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DS = "macrophage"
MIN_SHARED = 10


def load(path: Path):
    if not path.exists():
        return None
    d = pd.read_csv(path, index_col=0)
    return d[d["fit_likelihood"].notna()] if "fit_likelihood" in d.columns else d


def _upper(d):
    """human↔human 방어적 uppercase 정규화 (중복 index 제거)."""
    if d is None:
        return None
    d = d.copy()
    d.index = d.index.astype(str).str.upper()
    return d[~d.index.duplicated()]


def rho_line(a: pd.Series, b: pd.Series, label: str, sign_informative=False):
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
    # ── macrophage arms ──
    b_fl = load(RESULTS / f"rna_only_dynamical_genes_{DS}.csv")
    b_mv = load(RESULTS / f"multivelo_genes_{DS}.csv")
    b_vae = load(RESULTS / f"multivelovae_genes_{DS}.csv")
    # ── HSPC baselines (cross-dataset) ──
    h_mv = load(RESULTS / "multivelo_genes.csv")
    h_fl = load(RESULTS / "rna_only_dynamical_genes.csv")

    L = ["# P3 concordance — HSPC→macrophage differentiation replication of HSPC lag/α finding", "",
         "> 질문: HSPC 결론 **\"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.88)\"**가 "
         "**같은 human 조혈축의 하류(단핵구→대식세포 분화; MultiVeloVAE 신규 데이터셋)**에서 재현되나? — "
         "same-lineage 하류 확장.", "",
         "## 실행된 method arm", ""]
    arms = [("scVelo floor (RNA-only)", b_fl, "fit_alpha"),
            ("MultiVelo (chromatin-aware)", b_mv, "fit_alpha / fit_t_sw*"),
            ("MultiVeloVAE (chromatin-aware)", b_vae, "vae_alpha / vae_alpha_c")]
    L.append("| arm | fit gene | rate/lag 컬럼 |")
    L.append("|---|---|---|")
    for name, d, cols in arms:
        L.append(f"| {name} | {len(d) if d is not None else '**없음**'} | {cols} |")
    L.append("")

    # ── A. Within-macrophage cross-method ──
    L += ["## A. Within-macrophage cross-method concordance", "",
          "동일 데이터셋·동일 gene축.", ""]

    # A1. α (rate) — robust leg
    L += ["### A1. transcription rate α (robust leg 기대)", ""]
    alpha = {}
    if b_fl is not None and "fit_alpha" in b_fl: alpha["floor"] = b_fl["fit_alpha"]
    if b_mv is not None and "fit_alpha" in b_mv: alpha["MV"] = b_mv["fit_alpha"]
    if b_vae is not None and "vae_alpha" in b_vae: alpha["VAE"] = b_vae["vae_alpha"]
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

    # A2. lag — fragile leg (MV × VAE)
    L += ["### A2. chromatin→transcription lag (fragile leg 기대)", "",
          "> floor는 RNA-only라 lag 없음 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정 가능.", ""]
    lag = {}
    if b_mv is not None and {"fit_t_sw1", "fit_t_sw2"} <= set(b_mv.columns):
        lag["MV"] = (b_mv["fit_t_sw2"] - b_mv["fit_t_sw1"])          # sign 구조적
    if b_vae is not None and {"vae_alpha_c", "vae_alpha"} <= set(b_vae.columns):
        lag["VAE"] = (1.0 / b_vae["vae_alpha_c"].clip(1e-6) - 1.0 / b_vae["vae_alpha"].clip(1e-6))
    lag_rho = None
    if len(lag) >= 2:
        line, lag_rho, n = rho_line(lag["MV"].abs(), lag["VAE"].abs(),
                                    "lag **크기** rank: MV × VAE")
        L.append(line)
        L.append("- ⚠️ sign-agreement 생략: MultiVelo lag sign은 4-state 단조정렬로 **구조적 양수(무정보)**.")
    else:
        L.append(f"- chromatin-aware lag method {len(lag)}개 ({list(lag)}) → 2개+ 필요. "
                 "VAE 완주 후 MV×VAE lag concordance 산출됨.")
    L.append("")

    # ── B. Cross-dataset HSPC ↔ macrophage (직접 gene 매칭, human↔human) ──
    L += ["## B. Cross-dataset HSPC ↔ macrophage (human↔human, 직접 gene 매칭)", "",
          "> 둘 다 human 조혈 → gene SYMBOL 축 직접 겹침(case/ortholog 매핑 불필요, "
          "E18의 trap #1 해당 없음). 방어적 uppercase 정규화만 적용.", ""]
    b_lag_rho = b_alpha_rho = None
    h_mv_u, b_mv_u = _upper(h_mv), _upper(b_mv)
    if h_mv_u is not None and b_mv_u is not None:
        up_shared = len(set(h_mv_u.index) & set(b_mv_u.index))
        L.append(f"- shared gene (HSPC × macrophage MultiVelo): **{up_shared}** "
                 "(same-lineage human → 교집합 큼).")
        h_lag = (h_mv_u["fit_t_sw2"] - h_mv_u["fit_t_sw1"]).abs()
        e_lag = (b_mv_u["fit_t_sw2"] - b_mv_u["fit_t_sw1"]).abs()
        line, b_lag_rho, n = rho_line(h_lag, e_lag, "MV lag 크기 rank: HSPC × macrophage")
        L.append(line)
        line, b_alpha_rho, n = rho_line(h_mv_u["fit_alpha"], b_mv_u["fit_alpha"],
                                        "MV α rank: HSPC × macrophage")
        L.append(line)
        h_fl_u, b_fl_u = _upper(h_fl), _upper(b_fl)
        if h_fl_u is not None and b_fl_u is not None:
            line, r, n = rho_line(h_fl_u["fit_alpha"], b_fl_u["fit_alpha"],
                                  "floor α rank: HSPC × macrophage (sanity)")
            L.append(line)
    else:
        L.append("- HSPC 또는 macrophage MultiVelo csv 없음 → cross-dataset 비교 skip.")
    L.append("")

    # ── 판정 ──
    L += ["## 판정 — 'lag-fragile / α-robust' 패턴 재현?", ""]

    def _fmt(x): return f"{x:+.3f}" if x is not None else "N/A"
    a_alpha_med = float(np.median(a_rhos)) if a_rhos else None
    L.append(f"- Within-macrophage α (cross-method) Spearman: {[f'{r:+.2f}' for r in a_rhos] or 'N/A'} "
             f"(중앙값 {_fmt(a_alpha_med)})")
    L.append(f"- Within-macrophage lag 크기 rank (MV×VAE): {_fmt(lag_rho)}")
    L.append(f"- Cross-dataset HSPC↔macrophage: lag 크기 rank {_fmt(b_lag_rho)} vs α rank {_fmt(b_alpha_rho)}")
    L.append("")

    verdict, why = _verdict(a_alpha_med, lag_rho, b_lag_rho, b_alpha_rho)
    L.append(f"### → **{verdict}**")
    L.append(f"- {why}")
    L += ["",
          "## caveat (필수)",
          "- lag 크기 rank만 비교(방향 아님): MultiVelo sign은 4-state 단조정렬로 구조적 양수(무정보).",
          "- 단일 macrophage sample(9060-MV-3) replication 1건 — 강한 일반화 주장 금지. "
          "HSPC + human_brain + E18 + BMMC + macrophage 축의 일관성으로만 서사.",
          "- concordance는 *전역* per-gene fit rank (within-lineage 아님). macrophage lineage annotation은 "
          "load-bearing 아님.",
          "- ⚠️ **전처리 분기점 차이(중요)**: figshare postpro는 저자 그래프에서 HVG 필터+scVelo moments 완료 "
          "(layers Ms/Mu). raw spliced/unspliced 부재 시 moment fallback → 우리 공통 전처리(방법론 #5) 분기점이 "
          "다른 3종보다 더 pre-baked. human_brain의 외부-제공 spliced/unspliced caveat보다 강함 — Methods에 명시. "
          "cross-dataset rank에 noise만 추가(낮은 rho=lag fragile에 보수적).", ""]

    out = RESULTS / f"concordance_{DS}.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n✓ → {out}")
    return 0


def _verdict(a_alpha, lag_within, b_lag, b_alpha):
    def hi(x): return x is not None and abs(x) > 0.5
    def lo(x): return x is not None and abs(x) <= 0.3
    alpha_robust = hi(a_alpha) or hi(b_alpha)
    lag_fragile_within = lo(lag_within)
    lag_fragile_cross = lo(b_lag)
    lag_tested = (lag_within is not None) or (b_lag is not None)

    if not alpha_robust and a_alpha is None and b_alpha is None:
        return ("판정 보류 — α/lag 지표 부족",
                "필요한 arm(최소 floor+MV, lag는 MV+VAE)이 아직 안 끝남.")
    if alpha_robust and (lag_fragile_within or lag_fragile_cross):
        legs = []
        if lag_within is not None:
            legs.append(f"within-macrophage MV×VAE lag {lag_within:+.2f}")
        if b_lag is not None:
            legs.append(f"cross-dataset lag {b_lag:+.2f}")
        return ("재현 YES — 'lag-fragile / α-robust' 패턴 재현",
                f"α는 cross-method/cross-dataset에서 강함(≈{a_alpha if a_alpha is not None else b_alpha:+.2f}), "
                f"lag는 약함({', '.join(legs)}). HSPC same-lineage 서사 일치.")
    if alpha_robust and not lag_tested:
        return ("재현 PARTIAL — α-robust만 확인",
                "α robust leg 재현. lag fragile leg는 chromatin-aware 2번째(VAE) 완주 또는 "
                "cross-dataset MV lag rank 필요.")
    if alpha_robust and not (lag_fragile_within or lag_fragile_cross):
        return ("재현 PARTIAL — α-robust 확인, lag는 예상보다 강함",
                f"α robust이나 lag rank가 |r|>0.3 (within {lag_within}, cross {b_lag}) — "
                "정직하게 보고.")
    return ("재현 약함/불명확",
            f"α robust={alpha_robust}, lag fragile(within)={lag_fragile_within}, "
            f"lag fragile(cross)={lag_fragile_cross} — 지표 재확인 필요.")


if __name__ == "__main__":
    sys.exit(main())
