#!/usr/bin/env python
"""
층② velocity 행렬 불일치의 **외부 재현** (BIOP01-60).

사전등록 = manuscript/PREREGISTRATION_velocity_matrix.md 부록(외부 데이터를 열기 전에 봉인).
지표·제외규칙은 HSPC 본편(p10)과 **동일**하다 — 외부에 맞춰 정의를 바꾸지 않는다.

재현 검정 대상: multiome 방법끼리의 일치가 multiome x RNA-only 기준선을 넘지 못한다는 **순서**.
재현 불가(명시): ATAC-shuffle 인과 대조(외부에 scrambled arm 없음), 시스템별 재현성 천장(refit 없음).
"""
import csv
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p10_velocity_matrix_audit import (B_BOOT, SEED, _names, boot_median_ci,
                                       cos_cols, cos_rows, load, sign_agreement)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, "data", "velocity")
OUT = os.path.join(ROOT, "results")
RNA_ONLY = "scVelo(RNA)"

SYSTEMS = {
    "gastrulation (GSE205117, mouse)": {
        "MultiVelo":    ("multivelo_gse205117.h5ad", "velo_s"),
        "MoFlow":       ("moflow_gse205117.h5ad", "velo_s"),
        "MultiVeloVAE": ("multivelovae_gse205117.h5ad", "vae_velocity"),
        RNA_ONLY:       ("rna_only_dynamical_gse205117.h5ad", "velocity"),
    },
    "macrophage": {
        "MultiVelo":    ("multivelo_macrophage.h5ad", "velo_s"),
        "MultiVeloVAE": ("multivelovae_macrophage.h5ad", "vae_velocity"),
        RNA_ONLY:       ("rna_only_dynamical_macrophage.h5ad", "velocity"),
    },
    "BMMC (GSE194122)": {
        "MultiVelo":    ("multivelo_GSE194122_bmmc.h5ad", "velo_s"),
        "MultiVeloVAE": ("multivelovae_GSE194122_bmmc.h5ad", "vae_velocity"),
        RNA_ONLY:       ("rna_only_dynamical_GSE194122_bmmc.h5ad", "velocity"),
    },
    "E18 mouse brain": {
        "MultiVelo":    ("multivelo_e18_mouse_brain.h5ad", "velo_s"),
        "MultiVeloVAE": ("multivelovae_e18_mouse_brain.h5ad", "vae_velocity"),
        RNA_ONLY:       ("rna_only_dynamical_e18_mouse_brain.h5ad", "velocity"),
    },
}


def run_system(name, arms, rng):
    paths = {k: (os.path.join(V, f), l) for k, (f, l) in arms.items()}
    obs = {k: _names(p, "obs") for k, (p, _) in paths.items()}
    # 세포는 이름 교집합으로 정렬 — 외부 arm은 세포 순서가 같다는 보장이 없다
    shared_cells = sorted(set.intersection(*[set(o) for o in obs.values()]))
    var = {k: set(_names(p, "var")) for k, (p, _) in paths.items()}
    shared = sorted(set.intersection(*var.values()))

    mats = {}
    for k, (p, l) in paths.items():
        M = load(p, l, shared)
        pos = {c: i for i, c in enumerate(obs[k])}
        mats[k] = M[np.array([pos[c] for c in shared_cells])]

    shared = np.array(shared)
    ok = np.ones(len(shared), bool)
    dropped = {}
    for k, M in mats.items():
        bad = (~np.isfinite(M).all(axis=0)) | (np.nan_to_num(M).std(axis=0) == 0)
        dropped[k] = int(bad.sum())
        ok &= ~bad
    genes = shared[ok]
    mats = {k: M[:, ok] for k, M in mats.items()}
    cent = {k: M - M.mean(axis=0, keepdims=True) for k, M in mats.items()}
    print(f"\n=== {name}: 세포 {len(shared_cells)} / 공유 유전자 {len(shared)} "
          f"-> 사용 {len(genes)} (제외 {dropped})", flush=True)
    if len(genes) < 100:
        print("   !! 사용 유전자 < 100 -> INCONCLUSIVE", flush=True)

    names_l = [k for k in arms if k != RNA_ONLY] + [RNA_ONLY]
    perm = rng.permutation(len(shared_cells))
    rows, percell = [], {}
    for i, a in enumerate(names_l):
        for b in names_l[i + 1:]:
            pc = cos_rows(mats[a], mats[b])
            pcc = cos_rows(cent[a], cent[b])
            # 봉인된 규약(사전등록 §2-4): **주 판정은 원척도**. 중심화는 보조.
            percell[(a, b)] = (pc, pcc)
            null = float(np.nanmedian(cos_rows(mats[a], mats[b][perm])))
            gperm = rng.permutation(len(genes))
            pg = cos_cols(mats[a], mats[b])
            null_pg = float(np.nanmedian(cos_cols(mats[a], mats[b][:, gperm])))
            sa, n_used, n_ex = sign_agreement(mats[a], mats[b])
            kind = "multiome x RNA-only" if RNA_ONLY in (a, b) else "multiome x multiome"
            rows.append(dict(system=name, pair=f"{a} x {b}", kind=kind,
                             cell_cos_median=float(np.nanmedian(pc)),
                             cell_cos_null_shuffled=null,
                             cell_cos_excess=float(np.nanmedian(pc)) - null,
                             centered_cos_median=float(np.nanmedian(pcc)),
                             gene_cos_median=float(np.nanmedian(pg)),
                             gene_cos_null_gene_shuffled=null_pg,
                             gene_cos_excess=float(np.nanmedian(pg)) - null_pg,
                             sign_agreement=sa, n_sign_used=n_used,
                             n_sign_excluded_zero=n_ex))
            print(f"   {a:14s} x {b:14s} [{kind:19s}] raw {np.nanmedian(pc):+.3f} "
                  f"(null {null:+.3f}) centered {np.nanmedian(pcc):+.3f} sign {sa:.1%}",
                  flush=True)

    mm = [p for p in percell if RNA_ONLY not in p]
    mr = [p for p in percell if RNA_ONLY in p]
    out = dict(system=name, n_cells=len(shared_cells), n_genes=int(len(genes)),
               n_mm_pairs=len(mm), n_mr_pairs=len(mr),
               inconclusive=bool(len(genes) < 100))
    for idx, tag in ((0, "raw"), (1, "centered")):
        mm_cell = np.nanmean(np.vstack([percell[p][idx] for p in mm]), axis=0)
        mr_cell = np.nanmean(np.vstack([percell[p][idx] for p in mr]), axis=0)
        d_med, d_lo, d_hi = boot_median_ci(mm_cell - mr_cell, rng, B_BOOT)
        out[f"mm_median_{tag}"] = float(np.nanmedian(mm_cell))
        out[f"mr_median_{tag}"] = float(np.nanmedian(mr_cell))
        out[f"paired_delta_{tag}"] = d_med
        out[f"ci_{tag}"] = [d_lo, d_hi]
        out[f"replicated_{tag}"] = bool(d_med <= 0 and d_hi < 0)
        out[f"contradicted_{tag}"] = bool(d_med > 0 and d_lo > 0)
        print(f"   >> [{tag:8s}] mm {np.nanmedian(mm_cell):+.3f} vs m-RNA "
              f"{np.nanmedian(mr_cell):+.3f} | paired delta {d_med:+.3f} "
              f"[{d_lo:+.3f}, {d_hi:+.3f}] 재현={out[f'replicated_{tag}']}", flush=True)
    # 주 판정 = 봉인된 규약대로 원척도
    out["replicated"] = out["replicated_raw"]
    out["contradicted"] = out["contradicted_raw"]
    return rows, out


def main():
    rng = np.random.default_rng(SEED)
    all_rows, summ = [], []
    for name, arms in SYSTEMS.items():
        r, s = run_system(name, arms, rng)
        all_rows += r
        summ.append(s)

    n_rep = sum(s["replicated"] for s in summ)
    n_con = sum(s["contradicted"] for s in summ)
    verdict = ("REPLICATED" if n_rep >= 3 else
               "NOT GENERALIZED" if n_con >= 2 else "MIXED")
    print(f"\n=== 사전등록 판정: {verdict}  (재현 {n_rep}/4, 반대 {n_con}/4)", flush=True)

    with open(os.path.join(OUT, "velocity_matrix_audit_external_pairs.csv"), "w",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_rows[0]))
        w.writeheader()
        w.writerows(all_rows)
    with open(os.path.join(OUT, "velocity_matrix_audit_external.json"), "w") as f:
        json.dump(dict(seed=SEED, systems=summ, pairs=all_rows,
                       n_replicated=n_rep, n_contradicted=n_con, verdict=verdict),
                  f, indent=2, ensure_ascii=False)
    print("saved: results/velocity_matrix_audit_external_pairs.csv, _external.json")


if __name__ == "__main__":
    sys.exit(main())
