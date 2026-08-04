#!/usr/bin/env python3
"""p5b_atac_alpha_expression_confound.py — "baseline ATAC → α(ρ=+0.309)"가 발현 confound인지 검정.

배경: BIOP01-42(human brain, sjpark) self-review에서 "baseline chromatin→α +0.212"가
      발현(abundance) confound로 드러남(발현 통제 시 +0.013로 소멸). HSPC 원고(draft_v2 L81)
      의 대응 주장 "real day0 ATAC가 held-out lineage에서 α를 예측(ρ=+0.309)"도 같은 confound
      위험이 있어, 발현을 통제하고도 ATAC의 α 예측력이 남는지 확인한다.

방법(p5_lag_model_atac.py의 leave-one-lineage-out Ridge를 그대로 재사용, target=α):
  feature set 비교
    atac         : {prom_acc, enh_acc, enh_sum, prom_enh_ratio, n_enh}   (원 주장)
    abund        : {abundance}                                            (발현만)
    abund+atac   : 합집합
  판정: abund+atac 이 abund 를 유의미하게 못 넘으면 ATAC 신호 = 발현 confound.
  보강: 발현 통제 부분상관 partial Spearman(ATAC-pred α, actual α | abundance),
        및 개별 ATAC feature vs α의 발현통제 부분상관.

입력: results/lag_model_atac.csv (gene, fit_alpha, ATAC features, lineage)
      results/coupling_per_gene.csv (gene, abundance)
출력: results/atac_alpha_expression_confound.md
실행: conda run -n scv-preprocess python scripts/p5b_atac_alpha_expression_confound.py
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, rankdata
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
SEED = 20260701
MIN_LINEAGE_N = 15
ATAC_F = ["prom_acc", "enh_acc", "enh_sum", "prom_enh_ratio", "n_enh"]


def loo_lineage_cv(X, y, lineages, feat_cols):
    """p5_lag_model_atac.py와 동일한 leave-one-lineage-out Ridge."""
    pred = pd.Series(np.nan, index=X.index)
    per = {}
    lins = [l for l in lineages.unique() if (lineages == l).sum() >= MIN_LINEAGE_N]
    for hold in lins:
        tr, te = lineages != hold, lineages == hold
        if tr.sum() < 20:
            continue
        sc = StandardScaler().fit(X.loc[tr, feat_cols])
        m = Ridge(alpha=1.0).fit(sc.transform(X.loc[tr, feat_cols]), y[tr])
        pred[te] = m.predict(sc.transform(X.loc[te, feat_cols]))
        if te.sum() >= 8:
            per[hold] = spearmanr(y[te], pred[te])[0]
    ok = pred.notna() & y.notna()
    overall = spearmanr(y[ok], pred[ok])[0] if ok.sum() > 8 else np.nan
    return pred, overall


def partial_spearman(x, y, z):
    """Spearman(x, y | z) — rank 변환 후 z(rank)에 대한 잔차 상관."""
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    rx, ry, rz = rankdata(x[m]), rankdata(y[m]), rankdata(z[m])
    Z = np.column_stack([np.ones_like(rz), rz])
    def resid(r):
        beta, *_ = np.linalg.lstsq(Z, r, rcond=None)
        return r - Z @ beta
    ex, ey = resid(rx), resid(ry)
    r = np.corrcoef(ex, ey)[0, 1]
    return r, int(m.sum())


def main():
    np.random.seed(SEED)
    df = pd.read_csv(RES / "lag_model_atac.csv", index_col=0)
    coup = pd.read_csv(RES / "coupling_per_gene.csv").set_index("gene")["abundance"]
    df["abundance"] = coup.reindex(df.index)
    # log1p 발현(강한 우편향 완화; Spearman이라 단조변환엔 불변이나 Ridge 입력 안정화)
    df["abundance_log"] = np.log1p(df["abundance"])

    need = ["fit_alpha", "lineage", "abundance_log"] + ATAC_F
    df = df.dropna(subset=need).copy()
    n = len(df)

    SETS = {
        "atac": ATAC_F,
        "abund": ["abundance_log"],
        "abund+atac": ["abundance_log"] + ATAC_F,
    }
    ov, preds = {}, {}
    for name, cols in SETS.items():
        pred, overall = loo_lineage_cv(df[cols + ["fit_alpha"]], df["fit_alpha"], df["lineage"], cols)
        ov[name] = overall
        preds[name] = pred
        print(f"[confound] α  [{name:11s}] held-out ρ = {overall:+.3f}", flush=True)

    # 발현통제 부분상관: ATAC-only pred vs actual α, abundance 통제
    ok = preds["atac"].notna()
    pr_partial, npart = partial_spearman(
        preds["atac"][ok].to_numpy(), df["fit_alpha"][ok].to_numpy(),
        df["abundance_log"][ok].to_numpy())
    # 원자료 상관 참고
    r_atacpred_alpha = spearmanr(preds["atac"][ok], df["fit_alpha"][ok])[0]
    r_abund_alpha = spearmanr(df["abundance_log"], df["fit_alpha"])[0]
    # 개별 ATAC feature의 발현통제 부분상관 (in-sample)
    feat_part = {}
    for f in ATAC_F:
        rr, _ = partial_spearman(df[f].to_numpy(), df["fit_alpha"].to_numpy(),
                                 df["abundance_log"].to_numpy())
        r0 = spearmanr(df[f], df["fit_alpha"])[0]
        feat_part[f] = (r0, rr)

    incr = ov["abund+atac"] - ov["abund"]
    survives = (ov["abund+atac"] > ov["abund"] + 0.05) and (abs(pr_partial) >= 0.10)

    L = ["# P5b — baseline ATAC→α 가 발현(abundance) confound인지 검정", "",
         "> BIOP01-42(brain, sjpark) self-review에서 baseline chromatin→α(+0.212)가 발현 통제 시 "
         "+0.013으로 소멸. HSPC 원고 대응 주장(draft_v2 L81, real-atac held-out ρ=+0.309)의 동일 "
         "위험을 확인.", "",
         f"- gene {n}종, target=fit_alpha, leave-one-lineage-out Ridge(원 p5_lag_model_atac.py 재사용).",
         "- 발현=coupling_per_gene.csv 의 abundance(steady-state spliced), log1p.", "",
         "## held-out lineage 일반화 (Spearman pred vs actual α)", "",
         "| feature set | held-out ρ |",
         "|---|---|",
         f"| atac (원 주장) | **{ov['atac']:+.3f}** |",
         f"| abund (발현만) | **{ov['abund']:+.3f}** |",
         f"| abund+atac | **{ov['abund+atac']:+.3f}** |",
         f"| ATAC 증분(abund+atac − abund) | **{incr:+.3f}** |", "",
         "## 발현 통제 부분상관", "",
         f"- ATAC-pred α ↔ actual α: raw ρ={r_atacpred_alpha:+.3f} → **발현통제 partial ρ={pr_partial:+.3f}** (n={npart}).",
         f"- 참고: abundance ↔ α raw ρ={r_abund_alpha:+.3f}.", "",
         "### 개별 ATAC feature vs α (raw → 발현통제 partial)", "",
         "| feature | raw ρ | partial ρ (|abundance) |",
         "|---|---|---|"]
    for f in ATAC_F:
        r0, rr = feat_part[f]
        L.append(f"| {f} | {r0:+.3f} | {rr:+.3f} |")
    L += ["", "## 판정", "",
          f"- **{'ATAC 신호가 발현 통제 후에도 유지됨 (confound 아님)' if survives else 'ATAC 신호가 발현으로 상당 부분 설명됨 (confound 위험)'}**.",
          f"  기준: abund+atac 가 abund 를 +0.05 이상 상회(증분 {incr:+.3f}) **그리고** 발현통제 partial |ρ|≥0.10 (={pr_partial:+.3f}).",
          "- brain(+0.212→+0.013 소멸)과 대비해 HSPC의 결과를 위 수치로 정직히 보고.",
          "- ⚠️ abundance=steady-state spliced는 α와 구조적으로 연관(정상상태 abundance≈α/γ)이라 "
          "부분상관은 보수적(과통제 가능). 증분 CV와 함께 읽는다."]
    out = RES / "atac_alpha_expression_confound.md"
    out.write_text("\n".join(L) + "\n")
    print(f"[confound] survives={survives}  incr={incr:+.3f}  partial={pr_partial:+.3f}", flush=True)
    print(f"[confound] ✓ → {out.name}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
