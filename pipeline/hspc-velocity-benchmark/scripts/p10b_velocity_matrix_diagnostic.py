#!/usr/bin/env python
"""
p10 사후 진단 (BIOP01-59). 주 판정은 p10에서 이미 봉인된 규약으로 끝났다.
여기서는 왜 원척도 코사인에 큰 음수가 나오는지, 그 구조를 분해만 한다. **판정을 바꾸지 않는다.**

분해: 각 method의 velocity 행렬은 (세포 공통 평균 벡터) + (세포별 편차) 로 나뉜다.
원척도 코사인은 평균 벡터에 지배될 수 있고, 두 method의 평균 벡터가 반대로 정렬돼 있으면
세포별 정보와 무관하게 큰 음수가 나온다. 중심화 코사인이 그 잔여 세포별 일치를 본다.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p10_velocity_matrix_audit import (ARMS, MULTIOME, SCRAMBLED, _names, cos_rows,
                                       load)


def main():
    obs = _names(ARMS["MultiVelo"][0], "obs")
    var = {k: set(_names(p, "var")) for k, (p, _) in ARMS.items()}
    shared = sorted(set.intersection(*var.values()))
    mats = {k: load(p, l, shared) for k, (p, l) in ARMS.items()}
    shared = np.array(shared)
    ok = np.ones(len(shared), bool)
    for M in mats.values():
        ok &= np.isfinite(M).all(axis=0) & (np.nanstd(M, axis=0) > 0)
    mats = {k: M[:, ok] for k, M in mats.items()}
    genes = shared[ok]
    print(f"세포 {len(obs)} 유전자 {len(genes)}\n")

    print("[A] 평균 벡터가 차지하는 비중 — ||mean||^2 / mean(||row||^2)")
    for k, M in mats.items():
        mu = M.mean(axis=0)
        frac = float((mu @ mu) / np.mean(np.einsum("ij,ij->i", M, M)))
        print(f"    {k:14s} {frac:6.1%}   (1에 가까울수록 모든 세포가 같은 방향)")

    print("\n[B] 중심화(세포 공통 평균 제거) 후 세포별 코사인 중앙값 — 세포별 편차의 일치")
    names = list(ARMS)
    cent = {k: M - M.mean(axis=0, keepdims=True) for k, M in mats.items()}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            raw = float(np.nanmedian(cos_rows(mats[a], mats[b])))
            c = float(np.nanmedian(cos_rows(cent[a], cent[b])))
            kind = "MM" if (a in MULTIOME and b in MULTIOME) else "M-RNA"
            print(f"    [{kind:5s}] {a:14s}×{b:14s} raw {raw:+.3f} → centered {c:+.3f}")

    print("\n[C] 평균 벡터끼리의 코사인 (원척도 음수의 출처)")
    mus = {k: M.mean(axis=0) for k, M in mats.items()}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            c = float(mus[a] @ mus[b] / (np.linalg.norm(mus[a]) * np.linalg.norm(mus[b])))
            print(f"    {a:14s}×{b:14s} {c:+.3f}")

    print("\n[D] ATAC-shuffle 대조도 중심화해서 재확인")
    for arm, scr in (("MultiVelo", "MultiVelo-scr"), ("MoFlow", "MoFlow-scr")):
        sp, sl = SCRAMBLED[scr]
        svar = set(_names(sp, "var"))
        keep = np.isin(genes, np.array([g for g in genes if g in svar]))
        S = load(sp, sl, list(genes[keep]))
        A = mats[arm][:, keep]
        good = np.isfinite(S).all(axis=0) & (S.std(axis=0) > 0)
        A, S = A[:, good], S[:, good]
        Ac, Sc = A - A.mean(0, keepdims=True), S - S.mean(0, keepdims=True)
        print(f"    {arm:10s} n={good.sum():3d}  raw {np.nanmedian(cos_rows(A, S)):+.3f}"
              f"  centered {np.nanmedian(cos_rows(Ac, Sc)):+.3f}")

    # [E] 재현성 천장 — 같은 method를 세포 재표본으로 재적합했을 때의 일치.
    # 이게 없으면 "cross-method 일치가 0"이 측정 잡음 때문인지 진짜 불일치인지 구분되지 않는다.
    import glob
    print("\n[E] MultiVelo 원본 × bootstrap refit (같은 method 재적합 = 재현성 천장)")
    pos = {c: i for i, c in enumerate(obs)}
    A_full = mats["MultiVelo"]
    vals = []
    for p in sorted(glob.glob(os.path.join(os.path.dirname(ARMS["MultiVelo"][0]),
                                           "multivelo_bootstrap", "*.h5ad")))[:6]:
        rc = _names(p, "obs")
        rv = set(_names(p, "var"))
        g = [x for x in genes if x in rv]
        S = load(p, "velo_s", g)
        A = A_full[np.array([pos[c] for c in rc])][:, np.isin(genes, np.array(g))]
        good = np.isfinite(S).all(axis=0) & (S.std(axis=0) > 0)
        A, S = A[:, good], S[:, good]
        Ac, Sc = A - A.mean(0, keepdims=True), S - S.mean(0, keepdims=True)
        nz = (A != 0) & (S != 0)
        vals.append((float(np.nanmedian(cos_rows(A, S))),
                     float(np.nanmedian(cos_rows(Ac, Sc))),
                     float(((A[nz] > 0) == (S[nz] > 0)).mean())))
        print(f"    {os.path.basename(p):14s} n_cell={len(rc)} n_gene={good.sum():3d} "
              f"raw {vals[-1][0]:+.3f} centered {vals[-1][1]:+.3f} sign {vals[-1][2]:.1%}")
    v = np.array(vals)
    print(f"    중앙값 raw {np.median(v[:, 0]):+.3f} centered {np.median(v[:, 1]):+.3f} "
          f"sign {np.median(v[:, 2]):.1%}")


if __name__ == "__main__":
    sys.exit(main())
