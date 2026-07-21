#!/usr/bin/env python3
"""p4_permutation_fdr.py — P4 multiple-testing (DESIGN §5.5, §4C).

§85: 공조절 gene 비독립 → parametric FDR anti-conservative → **permutation FDR**.
이 스크립트는 CSV 수준에서 *tractable*하게 두 검정을 수행(재-fit 불필요):

  (A) cross-method lag concordance 유의성 — sign-가변 method 쌍에서 관측 Spearman ρ가
      **gene-label shuffle null**(gene 짝을 무작위화)보다 강한가? two-sided 경험적 p →
      BH-FDR(쌍 family). "near-chance 일치"가 정말 chance인지 직접 검정.

  (B) per-gene cross-method **sign-consistency** agreement-set (§4C 2차) —
      각 gene의 sign-가변 method 부호가 얼마나 일치하나 → sign-shuffle null로 per-gene
      경험적 p → BH-FDR. FDR<0.10 = '방향 일치 agreement-set'.

⚠️ 범위: §85가 명시한 *lineage 내 pseudotime/cell shuffle* per-gene lag-크기 FDR은
   method별 재-fit(GPU 다수 회)이 필요 → 본 단계 밖. chromatin-driver 질문은
   이미 scrambled-chromatin null(`scrambled_null.md`)이 답함. 본 스크립트는 method-간
   일치도의 유의성(우리 핵심 결과의 통계적 뒷받침)에 집중.

실행: conda run -n scv-preprocess python scripts/p4_permutation_fdr.py
출력: results/permutation_fdr.md
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
sys.path.insert(0, str(HERE / "scripts"))
from p3_concordance import METHODS, load   # 동일 lag 정의 재사용 (단일 출처)

N_PERM = 10000
SEED = 20260701
FDR_Q = 0.10


def bh_fdr(pvals):
    """Benjamini-Hochberg q-values."""
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    q = np.empty(n)
    prev = 1.0
    for rank, idx in enumerate(order[::-1]):       # 큰 p부터
        i = n - rank                                # 1-based rank
        prev = min(prev, p[idx] * n / i)
        q[idx] = prev
    return q


def get_lag(m, data):
    """method m의 gene→lag(median) Series (NaN 제거)."""
    return METHODS[m]["lag"](data[m]).dropna()


def test_A_concordance(data, rng):
    """sign-가변 method 쌍의 Spearman ρ를 gene-label shuffle null과 비교."""
    methods = [m for m in data if METHODS[m].get("sign_informative") and METHODS[m].get("lag")]
    rows = []
    for a in range(len(methods)):
        for b in range(a + 1, len(methods)):
            ma, mb = methods[a], methods[b]
            la, lb = get_lag(ma, data), get_lag(mb, data)
            shared = la.index.intersection(lb.index)
            if len(shared) < 10:
                continue
            x = la.loc[shared].to_numpy()
            y = lb.loc[shared].to_numpy()
            rho_obs, p_param = spearmanr(x, y)
            # permutation null: y의 gene 순서를 셔플 (gene 짝 무작위화)
            null = np.empty(N_PERM)
            for k in range(N_PERM):
                null[k] = spearmanr(x, rng.permutation(y))[0]
            # two-sided 경험적 p (+1 smoothing)
            p_perm = (np.sum(np.abs(null) >= abs(rho_obs)) + 1) / (N_PERM + 1)
            rows.append(dict(pair=f"{ma}×{mb}", n=len(shared),
                             rho=rho_obs, p_param=p_param, p_perm=p_perm))
    df = pd.DataFrame(rows)
    if len(df):
        df["q_bh"] = bh_fdr(df["p_perm"].to_numpy())
    return df


def test_B_agreement_set(data, rng):
    """per-gene cross-method sign-consistency → sign-shuffle null → FDR."""
    methods = [m for m in data if METHODS[m].get("sign_informative") and METHODS[m].get("lag")]
    # gene × method 부호 행렬 (sign(lag); 0/NaN 제외)
    sign = {}
    for m in methods:
        lg = get_lag(m, data)
        sign[m] = np.sign(lg[lg != 0])
    S = pd.DataFrame(sign)                         # gene × method, NaN=결측
    S = S[S.notna().sum(axis=1) >= 2]              # ≥2 method에 관측된 gene만
    if not len(S):
        return pd.DataFrame(), {}
    # 통계량: 부호 일치도 = |mean(부호)| (1=완전일치, 0=반반)
    def consistency(row):
        v = row.dropna().to_numpy()
        return abs(v.mean())
    obs = S.apply(consistency, axis=1)
    n_meth = S.notna().sum(axis=1)
    # null: 각 method 부호를 ±대칭 무작위(부호 가설 = 무작위 ±) → method별 부호 셔플
    # gene별 관측 method 수에 맞춘 null 분포를 group별로 생성
    null_by_k = {}
    for k in sorted(n_meth.unique()):
        # k개 ±1 무작위의 |mean| 분포
        draws = rng.integers(0, 2, size=(N_PERM, int(k))) * 2 - 1
        null_by_k[k] = np.abs(draws.mean(axis=1))
    pgene = np.array([
        (np.sum(null_by_k[int(n_meth.loc[g])] >= obs.loc[g]) + 1) / (N_PERM + 1)
        for g in S.index
    ])
    out = pd.DataFrame({"n_method": n_meth.values, "consistency": obs.values,
                        "p_perm": pgene}, index=S.index)
    out["q_bh"] = bh_fdr(pgene)
    summary = dict(n_tested=len(out),
                   n_sig=int((out["q_bh"] < FDR_Q).sum()),
                   exp_false=FDR_Q)
    return out.sort_values("q_bh"), summary


def main():
    rng = np.random.default_rng(SEED)
    data = {m: d for m, d in ((m, load(m)) for m in METHODS) if d is not None}
    methods_sv = [m for m in data if METHODS[m].get("sign_informative") and METHODS[m].get("lag")]

    L = ["# P4 — Permutation FDR (DESIGN §5.5)", "",
         f"- N_perm={N_PERM}, seed={SEED}, FDR q<{FDR_Q} (BH).",
         f"- sign-가변 method: {methods_sv}",
         "> §85 권고대로 permutation 기반(공조절 gene 비독립). 범위·null 정의는 스크립트 docstring 참조.",
         ""]

    # (A)
    dfA = test_A_concordance(data, rng)
    L += ["## A. Cross-method lag concordance 유의성 (gene-label shuffle null)", ""]
    if len(dfA):
        L.append("| pair | n | Spearman ρ | p(param) | p(perm) | q(BH) | 유의(q<0.10) |")
        L.append("|---|---|---|---|---|---|---|")
        for _, r in dfA.iterrows():
            sig = "✅" if r["q_bh"] < FDR_Q else "—"
            L.append(f"| {r['pair']} | {int(r['n'])} | {r['rho']:+.3f} | "
                     f"{r['p_param']:.3f} | {r['p_perm']:.4f} | {r['q_bh']:.3f} | {sig} |")
        n_sig = int((dfA["q_bh"] < FDR_Q).sum())
        L += ["", f"→ {n_sig}/{len(dfA)} 쌍이 gene-label shuffle null 대비 유의. "
              "**유의해도 |ρ|가 작으면 effect는 약함**(통계적 유의 ≠ 강한 일치)."]
    else:
        L.append("- 비교 가능한 sign-가변 method 쌍 부족.")
    L.append("")

    # (B)
    dfB, summ = test_B_agreement_set(data, rng)
    L += ["## B. Per-gene cross-method sign-consistency agreement-set (§4C 2차)", ""]
    if len(dfB):
        L += [f"- 검정 gene(≥2 method 관측) = {summ['n_tested']}, "
              f"**FDR<{FDR_Q} agreement-set = {summ['n_sig']} gene**.",
              "- consistency = |mean(sign)| (1=전 method 동부호, 0=반반). "
              "null = 부호 무작위 ±.", ""]
        if summ["n_sig"]:
            L.append("| gene | n_method | consistency | q(BH) |")
            L.append("|---|---|---|---|")
            for g, r in dfB[dfB["q_bh"] < FDR_Q].head(40).iterrows():
                L.append(f"| {g} | {int(r['n_method'])} | {r['consistency']:.2f} | {r['q_bh']:.3f} |")
        else:
            L.append("> ⚠️ **agreement-set 비어 있음** — 어떤 gene도 method 간 부호가 "
                     "무작위 이상으로 일관되지 않음. = lag 방향은 method-민감(H1 강화). "
                     "대부분 gene이 2 method에만 관측되어 검정력도 제한적.")
    else:
        L.append("- 검정 가능 gene 부족.")
    L += ["", "---",
          "### 해석 (DESIGN §4 reframe)",
          "- 이 벤치마크는 *accuracy*가 아니라 *reproducibility/consistency*를 측정(ground truth 없음).",
          "- A·B가 유의하지 않거나 effect가 작으면 → **lag 방향/순위는 method 선택에 민감**, "
          "강건한 건 construct-validity marker(§2)뿐 — H1 핵심 결론과 정합.",
          "- ⚠️ 미수행(범위 밖): lineage 내 pseudotime-shuffle per-gene lag-크기 FDR(재-fit 필요), "
          "marker enrichment hypergeometric(§4C 2차, regulator 리스트 확정 후)."]

    out = RES / "permutation_fdr.md"
    out.write_text("\n".join(L) + "\n")
    print(f"[p4-fdr] ✓ → {out.name}", flush=True)
    if len(dfA):
        print(dfA.to_string(index=False), flush=True)
    if len(dfB):
        print(f"[p4-fdr] agreement-set(FDR<{FDR_Q}) = {summ['n_sig']}/{summ['n_tested']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
