#!/usr/bin/env python3
"""P2 — MultiVelo per-lineage refit ("진짜 within-lineage H1"). DESIGN §2,§3; CLAUDE.md #2.

전역 fit은 모든 lineage를 한 pseudotime 축에 섞어 gene당 switch time 1값만 준다.
lineage_lag.md의 lineage별 분포는 그 전역 lag을 dominant-expression으로 *귀속*한 것뿐
(per-lineage fit 아님). 진짜 within-lineage lag 일치도를 보려면 lineage별로 따로 fit해야 한다.

설계: 각 terminal lineage L 마다 cells = HSC/MPP(root) ∪ L 로 부분집합 →
  P1과 동일 substrate 재구성(filter_and_normalize→HVG→moments→umap) →
  knn_smooth_chrom(부분집합 그래프) → recover_dynamics_chrom →
  gene별 switch time(fit_t_sw1/2) = within-lineage chromatin→transcription lag.
root(HSC/MPP)를 포함시키는 이유: MultiVelo 4-state 모델은 induction/repression switch를
pseudotime 전 구간에서 fit 하므로 progenitor→terminal 분화 trajectory가 필요(terminal cell만으론
초기 chromatin 동역학 소실). p2_multivelo.py(전역)와 substrate·파라미터 동일, cell subset만 다름.

실행 (mv env):
  conda run --no-capture-output -n mv python -u \
      pipeline/hspc-velocity-benchmark/scripts/p2_multivelo_perlineage.py        # full (5 lineage)
  ... p2_multivelo_perlineage.py --genes 20                  # 스모크(소수 gene, 파이프라인만 검증)
  ... p2_multivelo_perlineage.py --lineages Myeloid,Erythroid # 일부 lineage만

출력:
  - data/velocity/multivelo_perlineage/<lin>.h5ad           (gitignore)
  - results/lineage_refit/<lin>_genes.csv                   (gene별 switch/rate, tracked)
  - results/runtime.csv                                     (append; lineage tag)
"""
from __future__ import annotations
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import time as _time
import scanpy as sc
import scvelo as scv
import anndata as ad
import multivelo as mv
try:
    import torch; torch.set_num_threads(1)
except Exception:
    pass
import p1_config as p1
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

METHOD = "multivelo_perlineage"
ROOT_LINEAGE = "HSC/MPP"


def fit_one_lineage(rna_full, atac_full, lin, n_genes_smoke=0):
    """root∪lin 세포로 MultiVelo 재fit → (genes_df, adata_result, n_cells, sec)."""
    mask = rna_full.obs["lineage"].isin([ROOT_LINEAGE, lin]).values
    rna = rna_full[mask].copy()
    atac = atac_full[rna.obs_names].copy()
    n_root = int((rna.obs["lineage"] == ROOT_LINEAGE).sum())
    n_term = int((rna.obs["lineage"] == lin).sum())
    print(f"[{lin}] cells {rna.n_obs} (root {n_root} + {lin} {n_term})", flush=True)

    # RNA: 전역 fit과 동일 substrate (counts 시작 → 정규화 → HVG → moments)
    if "counts" in rna.layers:
        rna.X = rna.layers["counts"].copy()
    with timer() as t:
        scv.pp.filter_and_normalize(rna, min_shared_counts=cfg.MIN_SHARED_COUNTS)
        if "highly_variable" not in rna.var.columns:
            sc.pp.highly_variable_genes(rna, n_top_genes=cfg.N_TOP_GENES)
        rna = rna[:, rna.var["highly_variable"]].copy()
        scv.pp.moments(rna, n_pcs=cfg.N_PCS, n_neighbors=cfg.N_NEIGHBORS)
        if "X_umap" not in rna.obsm:
            sc.tl.umap(rna, random_state=cfg.RANDOM_SEED)

        shared = [g for g in rna.var_names if g in set(atac.var_names)]
        if n_genes_smoke:
            shared = shared[:n_genes_smoke]
        rna = rna[:, shared].copy()
        atac = atac[rna.obs_names, shared].copy()
        print(f"  [{lin}] shared gene {len(shared)}, cells {rna.n_obs}", flush=True)

        mv.knn_smooth_chrom(atac, conn=rna.obsp["connectivities"])

        nj = cfg.MV_NJOBS if cfg.MV_PARALLEL else None
        chunk = max(1, cfg.MV_CHUNK)
        parts, _t0 = [], _time.perf_counter()
        for i in range(0, len(shared), chunk):
            sub = shared[i:i + chunk]
            res = mv.recover_dynamics_chrom(
                rna[:, sub].copy(), atac[:, sub].copy(),
                max_iter=5, device="cpu", parallel=cfg.MV_PARALLEL, n_jobs=nj)
            parts.append(res)
            done = min(i + chunk, len(shared)); el = _time.perf_counter() - _t0
            eta = el / done * (len(shared) - done)
            print(f"  [{lin}] {done}/{len(shared)} genes | {el/60:.1f}min, ETA ~{eta/60:.0f}min",
                  flush=True)
        adata_result = ad.concat(parts, axis=1, merge="first") if len(parts) > 1 else parts[0]

    keep = [c for c in adata_result.var.columns if c.startswith("fit_")]
    genes = adata_result.var[keep].copy(); genes.index.name = "gene"
    return genes, adata_result, rna.n_obs, t.sec


def main(n_genes_smoke=0, lineages=None):
    out_velo = cfg.OUT_VELO / "multivelo_perlineage"
    out_res = cfg.RESULTS / "lineage_refit"
    out_velo.mkdir(parents=True, exist_ok=True)
    out_res.mkdir(parents=True, exist_ok=True)
    scv.settings.verbosity = 1
    tag = ".smoke" if n_genes_smoke else ""

    rna_full = sc.read_h5ad(p1.OUT_RNA)
    atac_full = sc.read_h5ad(cfg.IN_ATAC)
    print(f"load RNA {rna_full.shape} layers={list(rna_full.layers)} | ATAC {atac_full.shape}")
    if "spliced" not in rna_full.layers:
        print("✗ spliced/unspliced 없음 — P1 점검"); return 1
    if "lineage" not in rna_full.obs.columns:
        print("✗ lineage 라벨 없음 — P1 점검"); return 1

    all_terminals = [l for l in rna_full.obs["lineage"].dropna().unique() if l != ROOT_LINEAGE]
    targets = lineages if lineages else sorted(all_terminals)
    targets = [l for l in targets if l in set(all_terminals)]
    print(f"per-lineage refit targets: {targets}")

    for lin in targets:
        slug = lin.replace("/", "-").replace(" ", "")
        try:
            genes, adata_result, n_cells, sec = fit_one_lineage(
                rna_full, atac_full, lin, n_genes_smoke)
        except Exception as e:
            print(f"✗ [{lin}] fit 실패: {type(e).__name__}: {e}", flush=True)
            continue
        out_csv = out_res / f"{slug}_genes{tag}.csv"
        genes.to_csv(out_csv)
        print(f"✓ [{lin}] gene fit {genes.shape} → {out_csv.relative_to(cfg.ROOT)}", flush=True)
        out_h5 = out_velo / f"{slug}{tag}.h5ad"
        adata_result.write_h5ad(out_h5)
        log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=f"perlineage:{lin}",
                    n_cells=n_cells, n_genes=genes.shape[0], wall_sec=sec,
                    peak_mb=peak_mem_mb(),
                    note=f"root∪{lin}; smoke n={n_genes_smoke}" if n_genes_smoke
                         else f"root∪{lin} per-lineage refit")
    print("다음: p3_lineage_refit.py (within-lineage lag 일치도 H1 재평가)")
    return 0


if __name__ == "__main__":
    n = 0
    lins = None
    if "--genes" in sys.argv:
        n = int(sys.argv[sys.argv.index("--genes") + 1])
    if "--lineages" in sys.argv:
        lins = sys.argv[sys.argv.index("--lineages") + 1].split(",")
    sys.exit(main(n_genes_smoke=n, lineages=lins))
