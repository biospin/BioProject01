#!/usr/bin/env python3
"""p3_crakvelo_sign_check.py — CRAK-Velo lag sign convention 검증 (2 갈래).

(a) 코드 convention 단위검증: chromatin이 명백히 선행하는 합성 신호 → dtw_lag이 양수를
    돌려주는지 결정론적으로 확인. (생물학 무관, 코드 부호만.)
(b) 생물학/method 일치: crakvelo_genes.csv를 moflow(동형 정의, 양수=chromatin선행) 및
    알려진 Myeloid marker와 대조. 868-gene velocity subset에 marker가 있는지 명시.

산출: stdout만(staging). FINDINGS 반영은 사람이 판단.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent.parent
RES = HERE / "results"
sys.path.insert(0, str(HERE / "scripts"))
from p2_crakvelo_lag import dtw_lag, zbin, N_BIN  # 동일 함수 재사용


def synth_sign_test():
    """chromatin이 spliced보다 SHIFT bin 먼저 상승 → dtw_lag 양수 기대."""
    print("=== (a) 코드 sign convention 단위검증 ===", flush=True)
    t = np.linspace(0, 1, 600)
    order = np.argsort(t)  # 이미 정렬
    sig = lambda x, c: 1 / (1 + np.exp(-(x - c) * 25))  # sigmoid 스위치
    results = []
    for shift, name in [(0.15, "chromatin 선행(+기대)"),
                        (-0.15, "spliced 선행(−기대)"),
                        (0.0, "동시(≈0 기대)")]:
        c = sig(t, 0.5 - shift / 2)        # shift>0 → c가 더 일찍 상승
        s = sig(t, 0.5 + shift / 2)
        cb, sb = zbin(c, order, N_BIN), zbin(s, order, N_BIN)
        mean_l, med_l = dtw_lag(cb, sb)
        ok = (np.sign(med_l) == np.sign(shift)) or (shift == 0 and abs(med_l) <= 2)
        results.append(ok)
        print(f"  shift={shift:+.2f} [{name}] → lag median={med_l:+.2f} mean={mean_l:+.2f}  "
              f"{'✓' if ok else '✗ 부호불일치!'}", flush=True)
    verdict = "PASS — 코드 convention 정상(양수=chromatin선행)" if all(results) \
        else "FAIL — dtw_lag 부호가 docstring과 반대!"
    print(f"  >>> {verdict}", flush=True)
    return all(results)


def bio_check():
    print("\n=== (b) marker / method 일치 ===", flush=True)
    crak = pd.read_csv(RES / "crakvelo_genes.csv", index_col=0)
    mof = pd.read_csv(RES / "moflow_genes.csv", index_col=0)
    print(f"  crakvelo n={len(crak)}, moflow n={len(mof)}", flush=True)

    # 알려진 Myeloid(chromatin priming 기대) marker가 velocity subset에 있나
    myelo = ["AZU1", "ELANE", "MPO", "PRTN3", "CTSG", "LYZ", "CSF1R",
             "S100A8", "S100A9", "CEBPA", "CEBPE", "SPI1", "MPO", "LCN2"]
    present = [m for m in dict.fromkeys(myelo) if m in crak.index]
    print(f"  crakvelo에 있는 Myeloid marker: {present or '없음'}", flush=True)
    for m in present:
        print(f"    {m}: crak_median={crak.loc[m,'cs_lag_median']:+.2f}", flush=True)

    # method 간 sign 일치 (동형 정의 moflow와)
    shared = crak.index.intersection(mof.index)
    cs = crak.loc[shared, "cs_lag_median"]
    ms = mof.loc[shared, "cs_lag_median"]
    nz = (cs != 0) & (ms != 0)
    sign_agree = (np.sign(cs[nz]) == np.sign(ms[nz])).mean()
    rho, p = spearmanr(cs, ms)
    print(f"  moflow×crakvelo shared={len(shared)} (both nonzero={nz.sum()})", flush=True)
    print(f"    sign-agreement={sign_agree:.1%}  (50%=무정보; <<50%=부호반전 의심)", flush=True)
    print(f"    Spearman(magnitude rank)={rho:+.3f} (p={p:.3f})", flush=True)

    # 전체 방향 편향
    lead = (crak["cs_lag_median"] > 0).mean()
    print(f"  crakvelo chromatin-leads(>0)={lead:.1%}  median={crak['cs_lag_median'].median():+.2f}", flush=True)
    return sign_agree, rho


if __name__ == "__main__":
    code_ok = synth_sign_test()
    sign_agree, rho = bio_check()
    print("\n=== 종합 ===", flush=True)
    print(f"  코드 convention: {'정상' if code_ok else '반전 — 수정 필요'}", flush=True)
    print(f"  biological sign 신뢰도: sign-agree={sign_agree:.1%}, rho={rho:+.3f}", flush=True)
