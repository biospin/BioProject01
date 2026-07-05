#!/usr/bin/env python3
"""P2 — MultiVelo (chromatin-aware baseline). DESIGN §2,§3.

RNA spliced/unspliced + gene-level ATAC를 공유 neighbor graph로 결합해 4-state
chromatin model을 fit → gene별 switch time(chromatin/RNA) = chromatin→transcription lag 원천.

핵심: knn_smooth_chrom(conn=...)로 **P1 공유 그래프**를 그대로 써서 Seurat WNN export 없이 실행
(DESIGN §3 shared-graph 공정성). native-WNN ablation은 후속.

실행 (mv env):
  conda run --no-capture-output -n mv python -u \
      pipeline/hspc-velocity-benchmark/scripts/p2_multivelo.py            # full
  ... p2_multivelo.py --genes 20      # 스모크 테스트(소수 gene, 파이프라인만 검증)

출력:
  - data/velocity/multivelo[.smoke].h5ad            (gitignore)
  - results/multivelo_genes[.smoke].csv             (gene별 switch/rate, tracked)
  - results/runtime.csv                             (append; smoke는 note에 표시)
"""
from __future__ import annotations
# macOS: BLAS+torch nested threading이 recover_dynamics_chrom에서 serial 데드락/병렬 SIGSEGV 유발.
# numpy import 전에 스레드 1로 고정해야 함.
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import scanpy as sc
import scvelo as scv
import anndata as ad
import multivelo as mv
try:
    import torch; torch.set_num_threads(1)
except Exception:
    pass
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

METHOD = "multivelo"


def main(n_genes_smoke=0):
    cfg.OUT_VELO.mkdir(parents=True, exist_ok=True)
    cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    scv.settings.verbosity = 1
    arm = "chromatin_aware"
    tag = cfg.SUFFIX + (".smoke" if n_genes_smoke else "")   # cross-dataset suffix + smoke

    rna = sc.read_h5ad(cfg.IN_RNA)
    atac = sc.read_h5ad(cfg.IN_ATAC)
    print(f"load RNA {rna.shape} layers={list(rna.layers)} | ATAC {atac.shape}")
    if "spliced" not in rna.layers:
        print("✗ spliced/unspliced 없음 — P1 점검"); return 1

    # RNA: floor와 동일 substrate (counts 시작 → 정규화 → HVG → moments)
    if "counts" in rna.layers:
        rna.X = rna.layers["counts"].copy()
    with timer() as t:
        scv.pp.filter_and_normalize(rna, min_shared_counts=cfg.MIN_SHARED_COUNTS)
        if "highly_variable" not in rna.var.columns:
            sc.pp.highly_variable_genes(rna, n_top_genes=cfg.N_TOP_GENES)
        rna = rna[:, rna.var["highly_variable"]].copy()
        scv.pp.moments(rna, n_pcs=cfg.N_PCS, n_neighbors=cfg.N_NEIGHBORS)
        if "X_umap" not in rna.obsm:                 # recover_dynamics_chrom embedding 요구
            sc.tl.umap(rna, random_state=cfg.RANDOM_SEED)

        # 공유 gene 축 (RNA velocity gene ∩ ATAC gene-level)
        shared = [g for g in rna.var_names if g in set(atac.var_names)]
        if n_genes_smoke:
            shared = shared[:n_genes_smoke]
        rna = rna[:, shared].copy()
        atac = atac[rna.obs_names, shared].copy()      # cell/gene 정렬
        print(f"shared gene set: {len(shared)} (smoke={bool(n_genes_smoke)}), cells {rna.n_obs}")

        # chromatin smoothing: P1 공유 그래프(connectivities) 사용
        mv.knn_smooth_chrom(atac, conn=rna.obsp["connectivities"])

        # 4-state chromatin model fit (병목). ⚠️ 결과는 새 adata로 *반환*됨 (in-place 아님).
        # loky 병렬은 OMP=1 고정 시 fork-safe(SIGSEGV 회피, 상단 env 참조).
        # gene을 chunk로 나눠 호출 → chunk마다 진행/ETA 출력 (단일 호출은 중간 진행 안 보임).
        import time as _time
        nj = cfg.MV_NJOBS if cfg.MV_PARALLEL else None
        chunk = max(1, cfg.MV_CHUNK)
        parts, _t0 = [], _time.perf_counter()
        for i in range(0, len(shared), chunk):
            sub = shared[i:i + chunk]
            # ⚠️ 청크의 gene이 전부 low-quality면 recover_dynamics_chrom이
            # ValueError('None of the genes were fitted...')를 던진다. 그 청크만
            # skip해야 앞선 성공 청크(수백 gene)가 통째로 버려지지 않는다.
            try:
                res = mv.recover_dynamics_chrom(
                    rna[:, sub].copy(), atac[:, sub].copy(),
                    max_iter=5, device="cpu", parallel=cfg.MV_PARALLEL, n_jobs=nj)
                parts.append(res)
            except ValueError as e:
                print(f"  [multivelo] chunk {i}:{i+chunk} 전부 low-quality → skip ({e})",
                      flush=True)
            done = min(i + chunk, len(shared)); el = _time.perf_counter() - _t0
            eta = el / done * (len(shared) - done)
            print(f"  [multivelo] {done}/{len(shared)} genes | {el/60:.1f}min elapsed, "
                  f"ETA ~{eta/60:.0f}min", flush=True)
        if not parts:
            print("✗ 모든 청크가 low-quality — fit된 gene 없음"); return 1
        adata_result = ad.concat(parts, axis=1, merge="first") if len(parts) > 1 else parts[0]
    print(f"done in {t.sec}s")

    # gene별 switch time(fit_t_sw1/2/3) = chromatin→transcription lag 원천 + rates
    keep = [c for c in adata_result.var.columns if c.startswith("fit_")]
    genes = adata_result.var[keep].copy(); genes.index.name = "gene"
    out_csv = cfg.RESULTS / f"multivelo_genes{tag}.csv"
    genes.to_csv(out_csv)
    print(f"✓ gene fit {genes.shape}, cols={keep[:8]}... → {out_csv.name}")

    out_h5 = cfg.OUT_VELO / f"multivelo{tag}.h5ad"
    adata_result.write_h5ad(out_h5)
    print(f"✓ adata → {out_h5}")

    log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm=arm,
                n_cells=rna.n_obs, n_genes=rna.n_vars, wall_sec=t.sec,
                peak_mb=peak_mem_mb(),
                note=f"shared-graph; smoke n={n_genes_smoke}" if n_genes_smoke
                     else "shared-graph (native-WNN ablation은 후속)")
    print("다음: P3 within-lineage 지표 (RNA-only floor vs MultiVelo lag 일치도)")
    return 0


if __name__ == "__main__":
    n = 0
    if "--genes" in sys.argv:
        n = int(sys.argv[sys.argv.index("--genes") + 1])
    sys.exit(main(n_genes_smoke=n))
