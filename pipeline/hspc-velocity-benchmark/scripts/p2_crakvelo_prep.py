#!/usr/bin/env python
"""
p2_crakvelo_prep.py — CRAK-Velo arm 입력 substrate 생성.

CRAK-Velo는 다른 arm과 달리 **peak-level ATAC + region 좌표 + cisTopic** 을 요구한다.
P1은 ATAC를 gene-level로 집계(공통 gene 축)했으므로, 여기서 raw GSE209878 peak matrix로부터
day0/day7 공통 **consensus peak 축**을 재구성한다.

⚠️ 방법론 caveat (산출 문서에도 명기):
  - day0(MV-1)/day7(MV-2) peak은 CellRanger-ARC가 sample별 독립 호출 → 정확일치 62개뿐.
    따라서 두 sample peak union → 좌표 overlap merge(consensus) → 각 sample count를
    consensus interval에 합산하는 표준 consensus-peak 방식 사용.
  - ATAC는 batch(day0/day7) 미보정 — 기존 통합 벤치마크가 안고 있는 caveat와 동일.
  - fragments 미보유(9.4GB 미다운) → peak-count overlap-합산(재정량 아님). 근사.

산출:
  data/velocity/crakvelo_atac_prepro.h5ad  cell × consensus-peak, var[chrom,chromStart,chromEnd]
  data/velocity/crakvelo_rna_prepro.h5ad   cell × gene(coords有), layers spliced/unspliced/counts
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import scanpy as sc
import anndata as ad
from scipy import sparse

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data"
RAW = DATA / "GSE209878"
OUT = DATA / "velocity"
SAMPLES = ["MV-1", "MV-2"]
GENCODE = DATA / "ref" / "gencode.v44.basic.annotation.gtf.gz"


def log(m):
    print(f"[crak-prep] {m}", flush=True)


# ---------- 1. canonical 21,878 cell obs ----------
ref = ad.read_h5ad(DATA / "processed" / "atac_peaks.h5ad", backed="r")
ref_obs = ref.obs.copy()  # index: MV-1_<core>; cols sample/timepoint/batch/lineage/lineage_rare/leiden
ref_cells = set(ref_obs.index)
log(f"canonical cells: {len(ref_cells)}")


# ---------- 2. sample별 peak-level ATAC 로드 ----------
def load_sample_peaks(sample):
    d = RAW / sample
    feat = pd.read_csv(d / "features.tsv.gz", sep="\t", header=None,
                       names=["id", "name", "type", "chrom", "start", "end"])
    a = sc.read_mtx(d / "matrix.mtx.gz").T  # features x cells -> cells x features
    bc = pd.read_csv(d / "barcodes.tsv.gz", header=None)[0].astype(str)
    a.obs_names = [f"{sample}_{b.split('-')[0]}" for b in bc]
    is_peak = (feat["type"] == "Peaks").values
    a = a[:, is_peak].copy()
    pf = feat.loc[is_peak].reset_index(drop=True)
    a.var_names = pf["name"].values
    a.var["chrom"] = pf["chrom"].values
    a.var["start"] = pf["start"].astype(int).values
    a.var["end"] = pf["end"].astype(int).values
    keep = a.obs_names.isin(ref_cells)
    a = a[keep].copy()
    log(f"{sample}: peaks {a.shape[1]}, cells {a.shape[0]} (canonical 매칭)")
    return a


per = {s: load_sample_peaks(s) for s in SAMPLES}


# ---------- 3. consensus peak 축 (union -> 좌표 merge) ----------
# 모든 sample peak interval 수집
rows = []
for s in SAMPLES:
    v = per[s].var
    rows.append(pd.DataFrame({"chrom": v["chrom"].values,
                              "start": v["start"].values,
                              "end": v["end"].values,
                              "sample": s,
                              "local": np.arange(v.shape[0])}))
allp = pd.concat(rows, ignore_index=True)

# chrom별 정렬 후 overlapping interval merge -> consensus_id
allp = allp.sort_values(["chrom", "start", "end"]).reset_index(drop=True)
consensus = []          # (chrom, start, end)
cons_id = np.empty(len(allp), dtype=np.int64)
cur_chrom = None
cur_start = cur_end = -1
cid = -1
for i, (chrom, start, end) in enumerate(zip(allp["chrom"], allp["start"], allp["end"])):
    if chrom != cur_chrom or start > cur_end:   # 새 consensus interval (겹침 없음)
        cid += 1
        consensus.append([chrom, start, end])
        cur_chrom, cur_start, cur_end = chrom, start, end
    else:                                        # 겹침 -> 기존 interval 확장
        if end > cur_end:
            cur_end = end
        consensus[cid][2] = cur_end
    cons_id[i] = cid
allp["cons_id"] = cons_id
ncons = len(consensus)
cons_df = pd.DataFrame(consensus, columns=["chrom", "chromStart", "chromEnd"])
cons_df["peak"] = (cons_df["chrom"] + ":" + cons_df["chromStart"].astype(str)
                   + "-" + cons_df["chromEnd"].astype(str))
log(f"consensus peaks: {ncons} (union {len(allp)} local peaks)")


# ---------- 4. 각 sample count -> consensus 축으로 합산 ----------
def remap(sample):
    a = per[sample]
    sub = allp[allp["sample"] == sample]
    # local peak idx -> consensus idx indicator (nlocal x ncons)
    M = sparse.csr_matrix(
        (np.ones(len(sub)), (sub["local"].values, sub["cons_id"].values)),
        shape=(a.shape[1], ncons))
    Xc = a.X.tocsr() @ M           # cells x ncons
    return ad.AnnData(X=Xc, obs=a.obs.copy(),
                      var=cons_df.set_index("peak")[["chrom", "chromStart", "chromEnd"]])


parts = [remap(s) for s in SAMPLES]
atac = ad.concat(parts, axis=0, join="outer", merge="first")
atac.var = cons_df.set_index("peak")[["chrom", "chromStart", "chromEnd"]]
# canonical 순서로 정렬 + obs 메타 부여
atac = atac[ref_obs.index].copy()
for c in ["sample", "timepoint", "batch", "lineage", "lineage_rare", "leiden"]:
    atac.obs[c] = ref_obs[c].values
atac.X = sparse.csr_matrix(atac.X)
log(f"ATAC consensus adata: {atac.shape}")
OUT.mkdir(parents=True, exist_ok=True)
atac.write_h5ad(OUT / "crakvelo_atac_prepro.h5ad")
log(f"wrote {OUT/'crakvelo_atac_prepro.h5ad'}")


# ---------- 5. RNA substrate + gene 좌표(gencode) ----------
rna = ad.read_h5ad(DATA / "processed" / "rna_spliced_unspliced.h5ad")
rna = rna[ref_obs.index].copy()

# gencode gene span (gene_name -> chrom, min(start), max(end))
log("gencode parse...")
import gzip
spans = {}
with gzip.open(GENCODE, "rt") as fh:
    for line in fh:
        if line.startswith("#"):
            continue
        f = line.split("\t")
        if f[2] != "gene":
            continue
        chrom, start, end = f[0], int(f[3]), int(f[4])
        attr = f[8]
        # gene_name "XXX"
        k = attr.find('gene_name "')
        if k < 0:
            continue
        name = attr[k + 11: attr.find('"', k + 11)]
        if name in spans:
            c, s0, e0 = spans[name]
            spans[name] = (c, min(s0, start), max(e0, end))
        else:
            spans[name] = (chrom, start, end)
log(f"gencode genes: {len(spans)}")

gn = rna.var_names
chrom = np.array([spans[g][0] if g in spans else None for g in gn], dtype=object)
start = np.array([spans[g][1] if g in spans else -1 for g in gn], dtype=np.int64)
end = np.array([spans[g][2] if g in spans else -1 for g in gn], dtype=np.int64)
has = chrom != None
rna.var["chrom"] = chrom
rna.var["chromStart"] = start
rna.var["chromEnd"] = end
rna = rna[:, has].copy()   # 좌표 있는 gene만 (intersection 필수)
log(f"RNA with coords: {rna.shape} (matched {has.sum()}/{len(gn)})")
rna.write_h5ad(OUT / "crakvelo_rna_prepro.h5ad")
log(f"wrote {OUT/'crakvelo_rna_prepro.h5ad'}")
log("DONE")
