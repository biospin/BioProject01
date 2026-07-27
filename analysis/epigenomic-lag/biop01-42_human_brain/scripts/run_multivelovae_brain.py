"""BIOP01-42 옵션 A — MultiVeloVAE 정제 (§7 최약축). velo-torch GPU cuda:0.
p2_dl_prep.py + p2_multivelovae.py 로직을 brain h5ad에 self-contained로 적용.
prep: filter_normalize→HVG2000→moments(Ms/Mu)→umap→leiden→shared gene→ATAC smoothing(Mc)
fit: vv.VAEChrom(rna, atac, cuda:0, cluster_key=leiden, embed=umap).train() → var alpha."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
# multivelovae가 tqdm.notebook을 쓰는데 스크립트 컨텍스트라 실패 → 콘솔 tqdm으로 몽키패치 (import 전에)
import tqdm.std, tqdm.notebook, tqdm.auto
tqdm.notebook.tqdm = tqdm.std.tqdm
tqdm.notebook.trange = tqdm.std.trange
tqdm.auto.tqdm = tqdm.std.tqdm
tqdm.auto.trange = tqdm.std.trange
import numpy as np, scipy.sparse as sp
import scanpy as sc, scvelo as scv, multivelovae as vv
import time

DIR = "/workspace/data/cache/biop01/human_brain_GSE162170"

def smooth_chrom(atac, conn):
    A = conn.copy().tocsr().astype(float)
    A = A + sp.eye(A.shape[0], format="csr")
    A = sp.diags(1.0 / np.asarray(A.sum(1)).ravel()) @ A
    X = atac.X.tocsr() if sp.issparse(atac.X) else atac.X
    atac.layers["Mc"] = A @ X
    return atac

rna = sc.read_h5ad(f"{DIR}/brain_rna.h5ad")
atac = sc.read_h5ad(f"{DIR}/brain_atac.h5ad")
print(f"load RNA {rna.shape} | ATAC {atac.shape}", flush=True)

scv.pp.filter_genes(rna, min_shared_counts=20)           # 분해 시퀀스(filter_and_normalize inf 회피)
scv.pp.normalize_per_cell(rna)
sc.pp.log1p(rna)
sc.pp.highly_variable_genes(rna, n_top_genes=2000)
rna = rna[:, rna.var["highly_variable"]].copy()
scv.pp.moments(rna, n_pcs=30, n_neighbors=30)            # Ms/Mu
sc.tl.umap(rna, random_state=0)                          # X_umap
sc.tl.leiden(rna, random_state=0)                        # VAEChrom cluster_key
print(f"prep done: {rna.shape}, leiden {rna.obs['leiden'].nunique()} clusters", flush=True)

shared = [g for g in rna.var_names if g in set(atac.var_names)]
rna = rna[:, shared].copy()
atac = atac[rna.obs_names, shared].copy()
# ATAC gene activity 정규화 (raw는 스케일이 커 VAE ELBO NaN 유발) — per-cell normalize + log1p
sc.pp.normalize_total(atac, target_sum=1e4)
sc.pp.log1p(atac)
atac = smooth_chrom(atac, rna.obsp["connectivities"])
# 입력 진단 (NaN/inf/스케일)
import numpy as _np
for nm, arr in [("Ms", rna.layers["Ms"]), ("Mu", rna.layers["Mu"]), ("Mc", atac.layers["Mc"])]:
    a = arr.toarray() if sp.issparse(arr) else _np.asarray(arr)
    print(f"  [진단] {nm}: min={_np.nanmin(a):.3g} max={_np.nanmax(a):.3g} nan={_np.isnan(a).sum()} inf={_np.isinf(a).sum()}", flush=True)
for a in (rna, atac):
    a.uns.pop("log1p", None)
    for k in list(a.uns):
        if a.uns[k] is None: del a.uns[k]
print(f"DL 입력: shared gene {len(shared)}, cells {rna.n_obs}", flush=True)

var0 = set(rna.var.columns)
t0 = time.time()
model = vv.VAEChrom(rna, atac, device="cuda:0", plot_init=False, cluster_key="leiden", embed="umap")
model.train(plot=False)
print(f"VAE 학습 done in {time.time()-t0:.0f}s", flush=True)
model.save_anndata()
new_cols = [c for c in rna.var.columns if c not in var0]
genes = rna.var[new_cols].copy(); genes.index.name = "gene"
genes.to_csv(f"{DIR}/brain_multivelovae_genes.csv")
rna.write_h5ad(f"{DIR}/brain_multivelovae.h5ad")
print(f"✓ VAE fit {genes.shape}, new cols={new_cols[:10]}")
print("DONE_VAE", flush=True)
