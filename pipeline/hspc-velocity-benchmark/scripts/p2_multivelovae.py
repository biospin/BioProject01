#!/usr/bin/env python3
"""P2 — MultiVeloVAE (chromatin-aware, probabilistic multi-sample cVAE). DESIGN §2. H1 한 축.

DL arm: **GPU 머신에서 실행 권장** (CPU full run ~1–2일 — env/GPU-SETUP.md §런타임).
입력 = p2_dl_prep.py 산출(dl_input_rna: Ms/Mu/leiden/X_umap, dl_input_atac: Mc).

API(welch-lab paper-notebooks 기준): VAEChrom(adata, adata_atac, device, cluster_key, embed).train()
출력 rate = var['{key}_alpha_c/alpha/beta/gamma/scaling_c/u/likelihood'] + velocity layer.
lag proxy = chromatin opening(alpha_c) 대비 transcription 유도 시점 → P3에서 정의(δ/κ).

실행:
  conda run -n torch python pipeline/hspc-velocity-benchmark/scripts/p2_multivelovae.py [--genes N] [--gpu]
출력: results/multivelovae_genes.csv, data/velocity/multivelovae.h5ad, runtime.csv

⚠️ scipy<1.14 필요(노트북이 sparse .A 사용). GPU torch는 device='cuda:0'.
"""
from __future__ import annotations
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys
import scanpy as sc
import multivelovae as vv
import p2_config as cfg
from p2_util import timer, peak_mem_mb, log_runtime

METHOD = "multivelovae"


def main(n_genes=0, gpu=False):
    cfg.OUT_VELO.mkdir(parents=True, exist_ok=True); cfg.RESULTS.mkdir(parents=True, exist_ok=True)
    tag = ".smoke" if n_genes else ""
    rna = sc.read_h5ad(cfg.OUT_VELO / "dl_input_rna.h5ad")
    atac = sc.read_h5ad(cfg.OUT_VELO / "dl_input_atac.h5ad")
    if n_genes:
        g = list(rna.var_names[:n_genes]); rna = rna[:, g].copy(); atac = atac[:, g].copy()
    var0 = set(rna.var.columns)               # train 후 추가되는 fit 컬럼 식별용
    print(f"MultiVeloVAE: {rna.n_vars} genes, {rna.n_obs} cells, gpu={gpu}")

    with timer() as t:
        model = vv.VAEChrom(rna, atac, device=("cuda:0" if gpu else "cpu"),
                            plot_init=False, cluster_key="leiden", embed="umap")
        model.train(plot=False)
    print(f"학습 done in {t.sec}s")

    new_cols = [c for c in rna.var.columns if c not in var0]   # {key}_alpha_c/alpha/beta/gamma/...
    genes = rna.var[new_cols].copy(); genes.index.name = "gene"
    out_csv = cfg.RESULTS / f"multivelovae_genes{tag}.csv"; genes.to_csv(out_csv)
    print(f"✓ fit {genes.shape}, cols={new_cols[:8]}... → {out_csv.name}")

    rna.write_h5ad(cfg.OUT_VELO / f"multivelovae{tag}.h5ad")
    log_runtime(cfg.RUNTIME_CSV, method=METHOD, arm="chromatin_aware",
                n_cells=rna.n_obs, n_genes=rna.n_vars, wall_sec=t.sec, peak_mb=peak_mem_mb(),
                note=f"cVAE δ/κ; gpu={gpu}; smoke n={n_genes}" if n_genes else f"cVAE δ/κ; gpu={gpu}")
    return 0


if __name__ == "__main__":
    n = int(sys.argv[sys.argv.index("--genes") + 1]) if "--genes" in sys.argv else 0
    sys.exit(main(n_genes=n, gpu=("--gpu" in sys.argv)))
