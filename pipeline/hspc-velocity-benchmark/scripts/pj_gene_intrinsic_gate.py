#!/usr/bin/env python
"""
gene_intrinsic_gate.py — proxy-join §2 GATE (BIOP01-23)

목적: Todorovski(K562/THP-1, leukemia)의 gene별 mRNA half-life(t½)를
      우리 HSPC chromatin-lag 분석에 *차용*해도 되는지 판정한다.
판정 근거: t½가 cell-type 간 'gene-intrinsic'하게 보존되는가
           (= 다른 cell type t½와의 gene-wise 상관/순위 보존).
출력: PASS / CONDITIONAL / FAIL + 지표표 + 플롯.

⚠️ 스캐폴드. 데이터 경로(CONFIG)와 컬럼명은 데이터 확보 후 채울 것.
    HSPC 직접 t½는 희귀 → 여러 cell-type t½ 패널로 '보존성 일반론'을 보고,
    조혈계에 가까운 소스에 가중(아래 NOTE).
의존: pandas, numpy, scipy, matplotlib  (mv / scv-preprocess env에 포함)
실행: python gene_intrinsic_gate.py
"""
from __future__ import annotations
import os, json
import numpy as np
import pandas as pd
from scipy import stats

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG  (← 데이터 확보 후 채우기)
# ─────────────────────────────────────────────────────────────────────────────
CONFIG = {
    # 기준 t½ (우리가 차용하려는 것): Todorovski K562. 컬럼: gene symbol, half-life(hour)
    "reference_hl": {"path": "data/todorovski_k562_halflife.csv",
                     "gene_col": "gene", "hl_col": "t_half_h"},
    # 비교 t½ 패널 (cell-type 보존성 평가). 조혈계/혈액암 우선. 여러 개 권장.
    #   NOTE: HSPC 직접 t½가 없으면 (a) 혈액암 cell line, (b) 정상 면역세포,
    #         (c) 일반 cell line(HeLa/HepG2 등 compiled atlas)로 보존성 일반론.
    "comparison_hl": {
        # (a) 조혈계 same-study(Todorovski THP-1, AML monocytic) — 같은 SLAM-seq/lab → cell-type차만 격리, 낙관 상한.
        "thp1_todorovski":   {"path": "data/halflife_thp1.csv",    "gene_col": "gene", "hl_col": "t_half_h"},
        # (a) 조혈계 cross-study(RNADecayCafe MOLM13, AML) — 독립 lab·독립 파이프라인 → cross-dataset 전이 대표치(주 gate 지표).
        "molm13_rnadecaycafe": {"path": "data/halflife_molm13.csv", "gene_col": "gene", "hl_col": "t_half_h"},
        # (b) 일반 atlas cross-study(RNADecayCafe HEK293T, 비조혈) — cross-tissue 하한 참고.
        "hek293t_rnadecaycafe": {"path": "data/halflife_hek293t.csv", "gene_col": "gene", "hl_col": "t_half_h"},
    },
    # housekeeping gene 목록(보존성 상한 reference; 보통 가장 잘 보존됨). 한 줄 1 gene.
    "housekeeping_list": "data/housekeeping.txt",
    # 발현량 stratify용(선택): gene별 baseline expression (저발현 t½는 추정 불안정)
    "expression_tab": None,   # {"path":..., "gene_col":..., "expr_col":...} 또는 None
    "out_dir": "proxy_join/out_gate",
    # 판정 임계 (Spearman ρ, log t½ 기준). 조정 가능.
    "rho_pass": 0.50,         # ρ≥0.50 → PASS
    "rho_conditional": 0.30,  # 0.30≤ρ<0.50 → CONDITIONAL(한계 명시 + 잔차 흡수)
    # 그 미만 → FAIL(차용 무효 → win1 대안: K562 자체 ATAC로 lag proxy)
    "winsor": 0.01,           # 양끝 1% winsorize (t½ outlier)
}

# ─────────────────────────────────────────────────────────────────────────────
# 로딩 / 정규화
# ─────────────────────────────────────────────────────────────────────────────
def load_halflife(path: str, gene_col: str, hl_col: str) -> pd.Series:
    """CSV/TSV → Series(index=정규화 gene symbol, value=t½ hour). 중복은 median, t½>0만."""
    sep = "\t" if path.endswith((".tsv", ".txt")) else ","
    df = pd.read_csv(path, sep=sep)
    s = (df[[gene_col, hl_col]]
         .assign(**{gene_col: lambda d: d[gene_col].astype(str).str.strip().str.upper()})
         .dropna())
    s = s[s[hl_col] > 0]
    return s.groupby(gene_col)[hl_col].median()

def load_gene_list(path: str) -> set[str]:
    if not path or not os.path.exists(path):
        return set()
    return {ln.strip().upper() for ln in open(path) if ln.strip()}

def winsorize(x: np.ndarray, p: float) -> np.ndarray:
    lo, hi = np.nanquantile(x, [p, 1 - p])
    return np.clip(x, lo, hi)

# ─────────────────────────────────────────────────────────────────────────────
# 보존성 지표 (a=reference, b=comparison; 둘 다 t½ Series)
# ─────────────────────────────────────────────────────────────────────────────
def conservation(a: pd.Series, b: pd.Series, winsor: float) -> dict:
    common = a.index.intersection(b.index)
    if len(common) < 50:
        return {"n_overlap": int(len(common)), "note": "overlap<50 — 신뢰 불가"}
    av = winsorize(a.loc[common].to_numpy(float), winsor)
    bv = winsorize(b.loc[common].to_numpy(float), winsor)
    la, lb = np.log10(av), np.log10(bv)          # t½는 로그정규에 가까움
    rho, p_rho = stats.spearmanr(av, bv)         # 순위 보존(주 지표)
    r_log, _   = stats.pearsonr(la, lb)          # log 선형 상관
    diff = la - lb                                # Bland–Altman(log10 t½ 차이)
    # top/bottom decile 순위 일치 (Jaccard)
    qa_hi, qb_hi = np.quantile(av, .9), np.quantile(bv, .9)
    qa_lo, qb_lo = np.quantile(av, .1), np.quantile(bv, .1)
    hi = (set(np.array(common)[av >= qa_hi]) & set(np.array(common)[bv >= qb_hi]))
    hi_union = (set(np.array(common)[av >= qa_hi]) | set(np.array(common)[bv >= qb_hi]))
    lo = (set(np.array(common)[av <= qa_lo]) & set(np.array(common)[bv <= qb_lo]))
    lo_union = (set(np.array(common)[av <= qa_lo]) | set(np.array(common)[bv <= qb_lo]))
    return {
        "n_overlap": int(len(common)),
        "spearman_rho": round(float(rho), 3), "spearman_p": float(p_rho),
        "pearson_log": round(float(r_log), 3),
        "ba_bias_log10": round(float(np.mean(diff)), 3),
        "ba_loa_log10": [round(float(np.mean(diff) - 1.96*np.std(diff)), 3),
                         round(float(np.mean(diff) + 1.96*np.std(diff)), 3)],
        "top_decile_jaccard": round(len(hi)/max(len(hi_union), 1), 3),
        "bottom_decile_jaccard": round(len(lo)/max(len(lo_union), 1), 3),
    }

def stratified(a: pd.Series, b: pd.Series, hk: set[str], winsor: float) -> dict:
    """housekeeping(보존 상한) vs 나머지로 층화 — HK가 높고 나머지가 낮으면 cell-type-specific gene 차용 위험."""
    out = {}
    if hk:
        out["housekeeping"] = conservation(a[a.index.isin(hk)], b[b.index.isin(hk)], winsor)
        out["non_housekeeping"] = conservation(a[~a.index.isin(hk)], b[~b.index.isin(hk)], winsor)
    return out

# ─────────────────────────────────────────────────────────────────────────────
# 판정
# ─────────────────────────────────────────────────────────────────────────────
def gate_decision(rhos: list[float], cfg: dict) -> str:
    rhos = [r for r in rhos if r is not None and not np.isnan(r)]
    if not rhos:
        return "FAIL (no usable comparison)"
    med = float(np.median(rhos))
    if med >= cfg["rho_pass"]:
        return f"PASS (median ρ={med:.2f}) — t½ 차용 정당, 한계만 명시"
    if med >= cfg["rho_conditional"]:
        return (f"CONDITIONAL (median ρ={med:.2f}) — 차용하되 cell-type 차이를 잔차/공변량으로 흡수, "
                f"민감도 분석 필수, 결론 보수적 서술")
    return (f"FAIL (median ρ={med:.2f}) — 차용 무효. win1 대안: K562 자체 ATAC public으로 "
            f"lag proxy 재현하거나 proxy-join 포기")

# ─────────────────────────────────────────────────────────────────────────────
# 플롯 (선택; matplotlib 있으면)
# ─────────────────────────────────────────────────────────────────────────────
def plots(a, b, name, out_dir, winsor):
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    except Exception:
        return
    common = a.index.intersection(b.index)
    if len(common) < 50: return
    av = winsorize(a.loc[common].to_numpy(float), winsor)
    bv = winsorize(b.loc[common].to_numpy(float), winsor)
    fig, ax = plt.subplots(1, 2, figsize=(9, 4))
    ax[0].scatter(np.log10(av), np.log10(bv), s=6, alpha=.3)
    ax[0].set(xlabel="log10 t½ (K562/ref)", ylabel=f"log10 t½ ({name})", title="rank/log scatter")
    m = np.log10(av*bv)/2; d = np.log10(av) - np.log10(bv)
    ax[1].scatter(m, d, s=6, alpha=.3); ax[1].axhline(np.mean(d), color="r")
    ax[1].set(xlabel="mean log10 t½", ylabel="Δlog10 t½", title="Bland–Altman")
    fig.tight_layout(); fig.savefig(os.path.join(out_dir, f"gate_{name}.png"), dpi=120); plt.close(fig)

# ─────────────────────────────────────────────────────────────────────────────
def main():
    cfg = CONFIG
    os.makedirs(cfg["out_dir"], exist_ok=True)
    ref = load_halflife(**{k: cfg["reference_hl"][k] for k in ("path", "gene_col", "hl_col")})
    hk = load_gene_list(cfg["housekeeping_list"])
    if not cfg["comparison_hl"]:
        print("✗ comparison_hl 비어있음 — 비교 t½ 데이터(조혈계 우선)부터 확보 필요. (NOTE 참조)")
        return

    report, rhos = {"reference_n": int(ref.size), "sources": {}}, []
    for name, spec in cfg["comparison_hl"].items():
        comp = load_halflife(**{k: spec[k] for k in ("path", "gene_col", "hl_col")})
        res = conservation(ref, comp, cfg["winsor"])
        res["stratified"] = stratified(ref, comp, hk, cfg["winsor"])
        report["sources"][name] = res
        rhos.append(res.get("spearman_rho"))
        plots(ref, comp, name, cfg["out_dir"], cfg["winsor"])
        print(f"[{name}] n={res.get('n_overlap')} ρ={res.get('spearman_rho')} "
              f"top10%Jaccard={res.get('top_decile_jaccard')}")

    report["verdict"] = gate_decision(rhos, cfg)
    json.dump(report, open(os.path.join(cfg["out_dir"], "gate_report.json"), "w"),
              indent=2, ensure_ascii=False)
    print("\n=== GATE VERDICT ===\n" + report["verdict"])
    print(f"→ {cfg['out_dir']}/gate_report.json")

if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────────────────────────────────────
# NOTE — 비교 t½ 데이터 어디서:
#   · HSPC 직접 t½는 거의 없음. 차선 패널(여러 개로 robustness):
#       (a) 혈액암/면역세포 SLAM-seq·BRIC-seq half-life
#       (b) compiled atlas (예: Agarwal & Kelley 2022 'Saluki' 학습용 multi-cell-type t½)
#       (c) 일반 cell line(HeLa/HepG2/NIH3T3) — 하한 보존성 참고
#   · 판정 철학: HK gene은 어디서나 잘 보존 → '비-HK'에서도 ρ가 버티는지가 핵심.
#     비-HK ρ가 낮으면 cell-type-specific gene의 t½ 차용은 위험 → CONDITIONAL 이하.
#   · 통과해도 §4 모델에서 cell-type 차이를 공변량/잔차로 흡수하고, 결론은
#     "decay 통제 후 lag incremental"까지(timing 예측 아님, reframe 준수).
# ─────────────────────────────────────────────────────────────────────────────
