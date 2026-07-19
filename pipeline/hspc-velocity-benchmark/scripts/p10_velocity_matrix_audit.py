#!/usr/bin/env python
"""
층② 세포x유전자 velocity 행렬 감사 (BIOP01-59).

사전등록: manuscript/PREREGISTRATION_velocity_matrix.md — 정의·제외규칙·판정기준은 그 문서에 봉인돼 있다.
여기서는 그 규약을 그대로 실행만 한다.

  ① 유전자별 kinetic 모수  ← 현 논문이 감사한 층
  ② 세포x유전자 velocity 행렬 v = beta*u - gamma*s  ← 이 스크립트
  ③ 임베딩 화살표

핵심은 코사인 값 자체가 아니라 두 대조다:
  (A) multiome끼리 일치 > multiome vs RNA-only 일치 인가 (크로마틴이 방향에 기여하나)
  (B) ATAC-shuffle에서 행렬이 무너지나 (인과)
"""
import json
import os
import sys

import h5py
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V = os.path.join(ROOT, "data", "velocity")
OUT = os.path.join(ROOT, "results")
SEED = 20260719
B_BOOT = 1000

ARMS = {
    "MultiVelo":     (os.path.join(V, "multivelo.h5ad"), "velo_s"),
    "MoFlow":        (os.path.join(V, "moflow.h5ad"), "velo_s"),
    "CRAK-Velo":     (os.path.join(V, "crakvelo_fit/checkpoints/HSPC_CRAKVelo/0630_171200/adata_rna_fit.h5ad"), "velocity"),
    "MultiVeloVAE":  (os.path.join(V, "multivelovae.h5ad"), "vae_velocity"),
    "scVelo(RNA)":   (os.path.join(V, "rna_only_dynamical.h5ad"), "velocity"),
}
SCRAMBLED = {
    "MultiVelo-scr": (os.path.join(V, "multivelo_scrambled.h5ad"), "velo_s"),
    "MoFlow-scr":    (os.path.join(V, "moflow_scrambled.h5ad"), "velo_s"),
}
MULTIOME = ["MultiVelo", "MoFlow", "CRAK-Velo", "MultiVeloVAE"]
RNA_ONLY = "scVelo(RNA)"


def _names(path, grp):
    with h5py.File(path, "r") as f:
        g = f[grp]
        idx = g.attrs.get("_index", "_index")
        d = g[idx][:]
    return np.array([x.decode() if isinstance(x, bytes) else x for x in d])


def load(path, layer, genes):
    """genes(이름 리스트) 순서대로 velocity 열을 뽑는다. 이름 정렬 — 위치 정렬 아님."""
    var = _names(path, "var")
    pos = {g: i for i, g in enumerate(var)}
    cols = np.array([pos[g] for g in genes])
    order = np.argsort(cols)          # h5py fancy index는 증가 순서만 허용
    with h5py.File(path, "r") as f:
        sub = f["layers"][layer][:, cols[order]]
    back = np.empty_like(order)
    back[order] = np.arange(len(order))
    return np.asarray(sub[:, back], dtype=np.float32)


def cos_rows(A, B):
    """행(세포)별 코사인."""
    num = np.einsum("ij,ij->i", A, B)
    den = np.linalg.norm(A, axis=1) * np.linalg.norm(B, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, num / den, np.nan)


def cos_cols(A, B):
    """열(유전자)별 코사인."""
    num = np.einsum("ij,ij->j", A, B)
    den = np.linalg.norm(A, axis=0) * np.linalg.norm(B, axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, num / den, np.nan)


def sign_agreement(A, B):
    """(cell,gene) 부호 일치율. 어느 한쪽이라도 정확히 0이면 방향 미정으로 제외(사전등록 2-3)."""
    nz = (A != 0) & (B != 0)
    n = int(nz.sum())
    if n == 0:
        return np.nan, 0, int(A.size)
    agree = float(((A[nz] > 0) == (B[nz] > 0)).mean())
    return agree, n, int(A.size - n)


def boot_median_ci(x, rng, b=B_BOOT):
    x = x[np.isfinite(x)]
    if x.size == 0:
        return (np.nan, np.nan, np.nan)
    idx = rng.integers(0, x.size, size=(b, x.size))
    meds = np.median(x[idx], axis=1)
    return float(np.median(x)), float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))


def main():
    rng = np.random.default_rng(SEED)

    # ---- 1. 공유 세포·유전자 -------------------------------------------------
    obs = {k: _names(p, "obs") for k, (p, _) in ARMS.items()}
    ref_cells = obs["MultiVelo"]
    for k, o in obs.items():
        assert len(o) == len(ref_cells) and (o == ref_cells).all(), f"{k}: 세포 순서 불일치"
    var = {k: _names(p, "var") for k, (p, _) in ARMS.items()}
    shared = sorted(set.intersection(*[set(v) for v in var.values()]))
    print(f"[1] 공유 세포 {len(ref_cells)} / 5-arm 공유 유전자 {len(shared)}", flush=True)

    # ---- 2. 적재 + 사전등록 제외규칙 ----------------------------------------
    mats = {}
    for k, (p, l) in ARMS.items():
        mats[k] = load(p, l, shared)
        print(f"    적재 {k:14s} {mats[k].shape}", flush=True)

    shared = np.array(shared)
    ok = np.ones(len(shared), bool)
    nan_drop, var_drop = {}, {}
    for k, M in mats.items():
        bad_nan = ~np.isfinite(M).all(axis=0)
        bad_var = np.nanstd(M, axis=0) == 0
        nan_drop[k] = int(bad_nan.sum())
        var_drop[k] = int((bad_var & ~bad_nan).sum())
        ok &= ~(bad_nan | bad_var)
    genes = shared[ok]
    mats = {k: M[:, ok] for k, M in mats.items()}
    print(f"[2] NaN 제외 {nan_drop} / 분산0 제외 {var_drop} → 사용 유전자 {len(genes)}", flush=True)
    if len(genes) < 100:
        print("!! 사용 유전자 < 100 → 사전등록상 INCONCLUSIVE", flush=True)

    # 민감도용: 유전자별 SD로 나눔(중심화 없음 — 부호 보존)
    sd = {k: M.std(axis=0, keepdims=True) for k, M in mats.items()}
    smats = {k: M / np.where(sd[k] > 0, sd[k], 1.0) for k, M in mats.items()}

    # ---- 3. 쌍별 지표 --------------------------------------------------------
    names = list(ARMS)
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    perm = rng.permutation(len(ref_cells))     # 세포 짝 셔플 null
    rows = []
    percell = {}
    for a, b in pairs:
        A, Bm = mats[a], mats[b]
        pc = cos_rows(A, Bm)
        percell[(a, b)] = pc
        med, lo, hi = boot_median_ci(pc, rng)
        null_pc = np.nanmedian(cos_rows(A, Bm[perm]))
        pg = cos_cols(A, Bm)
        pcs = cos_rows(smats[a], smats[b])
        sa, n_used, n_ex = sign_agreement(A, Bm)
        kind = ("multiome×multiome" if a in MULTIOME and b in MULTIOME
                else "multiome×RNA-only")
        rows.append(dict(pair=f"{a} × {b}", kind=kind,
                         cell_cos_median=med, ci_lo=lo, ci_hi=hi,
                         cell_cos_null_shuffled=float(null_pc),
                         cell_cos_excess=med - float(null_pc),
                         cell_cos_median_sdscaled=float(np.nanmedian(pcs)),
                         gene_cos_median=float(np.nanmedian(pg)),
                         gene_cos_frac_pos=float(np.nanmean(pg > 0)),
                         sign_agreement=sa, n_sign_used=n_used, n_sign_excluded_zero=n_ex))
        print(f"    {a:14s}×{b:14s} cell-cos {med:+.3f} (null {null_pc:+.3f}) "
              f"gene-cos {np.nanmedian(pg):+.3f} sign {sa:.1%}", flush=True)

    # ---- 4. 대조 A: multiome끼리 vs RNA-only 기준선 (세포 단위 paired) --------
    mm = [p for p in pairs if p[0] in MULTIOME and p[1] in MULTIOME]
    mr = [p for p in pairs if RNA_ONLY in p]
    mm_cell = np.nanmean(np.vstack([percell[p] for p in mm]), axis=0)
    mr_cell = np.nanmean(np.vstack([percell[p] for p in mr]), axis=0)
    d = mm_cell - mr_cell
    d_med, d_lo, d_hi = boot_median_ci(d, rng)
    mm_med, mm_lo, mm_hi = boot_median_ci(mm_cell, rng)
    mr_med, mr_lo, mr_hi = boot_median_ci(mr_cell, rng)
    contrastA = dict(mm_median=mm_med, mm_ci=[mm_lo, mm_hi],
                     mr_median=mr_med, mr_ci=[mr_lo, mr_hi],
                     paired_delta_median=d_med, paired_delta_ci=[d_lo, d_hi],
                     ci_disjoint=bool(mm_lo > mr_hi),
                     delta_excludes_zero=bool(d_lo > 0))
    print(f"[4] 대조A multiome×multiome {mm_med:+.3f} [{mm_lo:+.3f},{mm_hi:+.3f}] vs "
          f"multiome×RNA-only {mr_med:+.3f} [{mr_lo:+.3f},{mr_hi:+.3f}] | "
          f"paired Δ {d_med:+.3f} [{d_lo:+.3f},{d_hi:+.3f}]", flush=True)

    # ---- 5. 대조 B: ATAC-shuffle 인과 ---------------------------------------
    contrastB = []
    for arm, scr in (("MultiVelo", "MultiVelo-scr"), ("MoFlow", "MoFlow-scr")):
        sp, sl = SCRAMBLED[scr]
        svar = set(_names(sp, "var"))
        sub = np.array([g for g in genes if g in svar])
        if len(sub) < 50:
            continue
        keep = np.isin(genes, sub)
        S = load(sp, sl, list(genes[keep]))
        A = mats[arm][:, keep]
        good = np.isfinite(S).all(axis=0) & (S.std(axis=0) > 0)
        A, S = A[:, good], S[:, good]
        self_scr = cos_rows(A, S)
        m, lo, hi = boot_median_ci(self_scr, rng)
        # 기준자: 같은 유전자 부분집합에서 다른 method와의 코사인
        others = {}
        for o in MULTIOME:
            if o == arm:
                continue
            om = mats[o][:, keep][:, good]
            others[o] = float(np.nanmedian(cos_rows(A, om)))
        sa, n_used, n_ex = sign_agreement(A, S)
        contrastB.append(dict(arm=arm, n_genes=int(good.sum()),
                              self_vs_scrambled_median=m, ci=[lo, hi],
                              sign_agreement=sa, n_sign_used=n_used,
                              n_sign_excluded_zero=n_ex,
                              vs_other_methods=others))
        print(f"[5] 대조B {arm} 원본×ATAC셔플 cell-cos {m:+.3f} [{lo:+.3f},{hi:+.3f}] "
              f"(sign {sa:.1%}) vs 다른 method {others}", flush=True)

    # ---- 6. 사전등록 판정 ----------------------------------------------------
    A_pass = contrastA["ci_disjoint"] and contrastA["delta_excludes_zero"]
    # 크로마틴이 인과적이면: 원본×셔플이 원본×다른method 보다 낮아야 한다(셔플로 무너짐)
    B_pass = all(c["self_vs_scrambled_median"] < min(c["vs_other_methods"].values())
                 for c in contrastB) if contrastB else False
    if len(genes) < 100:
        verdict = "INCONCLUSIVE"
    elif A_pass and B_pass:
        verdict = "POSITIVE"
    else:
        verdict = "NEGATIVE"
    print(f"[6] 판정: {verdict}  (대조A pass={A_pass}, 대조B pass={B_pass})", flush=True)

    res = dict(seed=SEED, n_cells=int(len(ref_cells)), n_genes_used=int(len(genes)),
               nan_dropped=nan_drop, zerovar_dropped=var_drop,
               pairs=rows, contrastA=contrastA, contrastB=contrastB,
               A_pass=bool(A_pass), B_pass=bool(B_pass), verdict=verdict)
    with open(os.path.join(OUT, "velocity_matrix_audit.json"), "w") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    import csv
    with open(os.path.join(OUT, "velocity_matrix_audit_pairs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("saved: results/velocity_matrix_audit.json, _pairs.csv")


if __name__ == "__main__":
    sys.exit(main())
