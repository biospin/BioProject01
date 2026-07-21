#!/usr/bin/env python3
"""HSPC→macrophage differentiation 10x Multiome → processed h5ad (build+finalize 합침).

cross-dataset 재현 5번(same-lineage 하류 확장; MultiVeloVAE 신규 데이터셋, human 조혈→대식세포).
figshare post-processed AnnData 2개(RNA=Ms/Mu, ATAC=gene-level)를 받아 HSPC/human_brain/E18/BMMC와
**동일 스키마**(rna_spliced_unspliced.h5ad + atac_gene.h5ad)로 마감한다.

입력 (config_macrophage.DATA = data/macrophage; figshare 10.6084/m9.figshare.30280333):
  - RNA : 8489-MV-1-9060-MV-3_adata_postpro_concat.h5ad       (HSPC 8489-MV-1 + macrophage 9060-MV-3 concat)
  - ATAC: 8489-MV-1-9060-MV-3_adata_atac_postpro_concat.h5ad  (gene-level chromatin, 동일 obs_names)

산출 (config_macrophage.OUT = data/processed_macrophage):
  - rna_spliced_unspliced.h5ad : cells×genes, layers{spliced,unspliced(,counts)}, obs{batch,leiden,lineage}
  - atac_gene.h5ad             : cells×genes, gene-level accessibility (figshare 제공 gene축 그대로)

⚠️ 두 가지 형태 주의 (2026-07-09 verify):
 1) **batch subset**: concat은 HSPC(8489-MV-1)+macrophage(9060-MV-3) 2 batch. macrophage batch만 남겨
    primary(HSPC) leakage 차단. MACRO_BATCH는 실제 obs['batch'] category로 확정(아래 guard가 목록 출력).
 2) **layer 형태**: postpro RNA는 scVelo moments 완료(layers Ms/Mu). raw spliced/unspliced count layer가
    유지 안 됐을 수 있음(byte-scan은 Ms/Mu만 발견). 아래 _resolve_velocity_layers()가:
       (a) raw spliced/unspliced 있으면 그대로 사용(이상적; 다른 3종과 동일 전처리 분기),
       (b) 없고 Ms/Mu만 있으면 **moment fallback**(spliced←Ms, unspliced←Mu)으로 진행하되
           WARNING + obs['velocity_layer_source']='moments_fallback' 플래그를 남긴다.
       → (b)는 공통 전처리 분기점이 어긋남(방법론 #5). Methods에 명시. concordance엔 노이즈만 추가(보수적).

실행 (scv-preprocess env):
  conda run --no-capture-output -n scv-preprocess python -u cross_dataset/build_macrophage.py
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import scanpy as sc
import anndata as ad

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                                   # pipeline/hspc-velocity-benchmark
DATA = ROOT / "data" / "macrophage"
RNA_H5AD  = DATA / "8489-MV-1-9060-MV-3_adata_postpro_concat.h5ad"
ATAC_H5AD = DATA / "8489-MV-1-9060-MV-3_adata_atac_postpro_concat.h5ad"
OUT = ROOT / "data" / "processed_macrophage"
OUT.mkdir(parents=True, exist_ok=True)

# concat 2 batch 중 macrophage sample만. 실제 obs['batch'] category로 확정(guard가 목록 출력).
# figshare 설명: "8489-MV-1-9060-MV-3 = One HSPC + one macrophage" → 9060-MV-3 = macrophage.
# ⚠️ 실측(2026-07-09, kkkim heavy-run): figshare postpro는 batch를 sample ID가 아니라 timepoint로 재라벨함
#    (obs['batch']={'Day 7':6336,'Day 14':3572}). batch×leiden 교차표로 대응 확정:
#    Day 7 = HSC/CMP/MEP/Prog*/Megakaryocyte (M1·M2 Macrophage 0) = HSPC sample(8489-MV-1);
#    Day 14 = MDP/Monocyte/M1·M2 Macrophage(479/371) = macrophage 분화 sample(9060-MV-3).
#    → 'Day 14' subset = macrophage sample(HSPC leakage 차단, 설계 의도 그대로).
#    또 raw spliced/unspliced layer 존재(nnz 35.6%) → moment fallback 불필요(계약보다 나음).
MACRO_BATCH_CANDIDATES = ("Day 14", "9060-MV-3", "9060-MV", "9060MV3", "9060")   # 우선순위; 첫 일치 사용
# HSPC와 동일 하이퍼파라미터 (공정 비교)
N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, SEED = 2000, 30, 30, 1.0, 0
QC = dict(min_genes=100, max_genes=8000, max_pct_mito=20.0)   # ⚠️ min_genes: figshare postpro는 929 HVG로 축소 + 저자 QC 완료(obs['outlier'] all False)라 HSPC 전전사체 기준 500은 Day14 3572→76 파괴. 실측 median nonzero=320/929 → 100=방어적 no-op(3572/3572 유지). 원 의도("대체로 no-op") 복원.
RARE = {"DC", "Cycling"}

# lineage marker (config_macrophage와 동일; build 시 var_names 필터)
LINEAGE_MARKERS = {
    "HSPC":       ["CD34", "KIT", "PROM1", "SPINK2", "AVP", "HLF", "MLLT3"],
    "GMP":        ["MPO", "ELANE", "AZU1", "PRTN3", "CTSG", "LYST"],
    "Monocyte":   ["CD14", "LYZ", "FCN1", "S100A8", "S100A9", "VCAN", "CSF1R", "CSF3R"],
    "Macrophage": ["CD68", "CD163", "MRC1", "MERTK", "MARCO", "MSR1", "APOE",
                   "C1QA", "C1QB", "C1QC", "ITGAM", "SPP1"],
    "DC":         ["FCER1A", "CD1C", "CLEC10A", "IRF8"],
    "Cycling":    ["MKI67", "TOP2A", "CENPF", "ASPM"],
}


def _pick_batch(obs: pd.DataFrame) -> str:
    """obs['batch'] category에서 macrophage batch를 확정. 못 찾으면 목록 출력 후 에러."""
    if "batch" not in obs.columns:
        raise RuntimeError("obs['batch'] 없음 — concat 형태 확인 필요")
    cats = [str(x) for x in pd.unique(obs["batch"])]
    for cand in MACRO_BATCH_CANDIDATES:
        for c in cats:
            if cand.lower() in c.lower():
                return c
    raise RuntimeError(
        f"macrophage batch 자동식별 실패. obs['batch'] 목록={cats}. "
        f"MACRO_BATCH_CANDIDATES를 실제 라벨로 맞춰라.")


def _resolve_velocity_layers(rna: ad.AnnData) -> str:
    """spliced/unspliced 우선, 없으면 Ms/Mu moment fallback. 사용 소스 문자열 반환."""
    lyr = set(rna.layers.keys())
    if {"spliced", "unspliced"} <= lyr:
        # 이상적: raw count layer 존재 → 다른 3종과 동일 전처리 분기
        return "raw_spliced_unspliced"
    if {"Ms", "Mu"} <= lyr:
        print("[WARN] raw spliced/unspliced layer 없음 → Ms/Mu moment fallback 사용. "
              "공통 전처리 분기점이 다른 3종과 어긋남(방법론 #5) — Methods에 명시.", flush=True)
        rna.layers["spliced"] = rna.layers["Ms"].copy()
        rna.layers["unspliced"] = rna.layers["Mu"].copy()
        rna.obs["velocity_layer_source"] = "moments_fallback"
        return "moments_fallback"
    raise RuntimeError(f"velocity layer 없음. layers={sorted(lyr)} — "
                       f"spliced/unspliced 또는 Ms/Mu 필요.")


def main():
    sc.settings.verbosity = 1

    # ── RNA (figshare postpro concat) ──
    print(f"[RNA] read {RNA_H5AD.name}", flush=True)
    rna = sc.read_h5ad(RNA_H5AD)
    rna.var_names_make_unique()
    print(f"  RNA(concat) {rna.shape}, layers={sorted(rna.layers)}, "
          f"batches={[str(x) for x in pd.unique(rna.obs.get('batch', pd.Series([], dtype=str)))]}",
          flush=True)

    # ── macrophage batch만 subset (HSPC leakage 차단) ──
    macro_batch = _pick_batch(rna.obs)
    n0 = rna.n_obs
    rna = rna[rna.obs["batch"].astype(str) == macro_batch].copy()
    print(f"[subset] batch=={macro_batch}: {n0} → {rna.n_obs} cells (macrophage only)", flush=True)
    assert rna.n_obs >= 500, f"macrophage batch cells {rna.n_obs} < 500 — batch 라벨 확인"

    # ── velocity layer 확정(raw 우선 / Ms·Mu fallback) ──
    vsrc = _resolve_velocity_layers(rna)
    rna.X = (rna.layers["spliced"] + rna.layers["unspliced"]).copy()
    rna.obs["dataset"] = "macrophage"

    # ── QC on RNA (postpro라 대체로 no-op; 방어적) ──
    rna.var["mito"] = rna.var_names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(rna, inplace=True, percent_top=None)
    if rna.var["mito"].any():
        rna.obs["pct_mito"] = (np.asarray(rna[:, rna.var["mito"]].X.sum(1)).ravel()
                               / np.asarray(rna.X.sum(1)).ravel() * 100)
    else:
        rna.obs["pct_mito"] = 0.0
    m0 = rna.n_obs
    sc.pp.filter_cells(rna, min_genes=QC["min_genes"])
    rna = rna[(rna.obs["n_genes_by_counts"] <= QC["max_genes"])
              & (rna.obs["pct_mito"] <= QC["max_pct_mito"])].copy()
    print(f"[QC] {m0} → {rna.n_obs} cells (mito≤{QC['max_pct_mito']}, genes {QC['min_genes']}~{QC['max_genes']})",
          flush=True)

    # ── ATAC (figshare postpro; gene-level, 동일 obs_names) ──
    print(f"[ATAC] read {ATAC_H5AD.name}", flush=True)
    atac_gene = sc.read_h5ad(ATAC_H5AD)
    atac_gene.var_names_make_unique()
    # RNA와 동일 cell로 정렬(subset+QC 반영). obs_names 교집합.
    common = [c for c in rna.obs_names if c in set(atac_gene.obs_names)]
    print(f"[align] RNA∩ATAC(gene) cells: {len(common)} "
          f"(RNA {rna.n_obs}, ATAC {atac_gene.n_obs})", flush=True)
    assert len(common) >= 500, f"교집합 {len(common)} < 500 — obs_names 정합 확인"
    rna = rna[common].copy()
    atac_gene = atac_gene[common].copy()

    # ── 정규화 + HVG + graph (HSPC p1_build 순서 복제) ──
    # postpro X는 이미 normalize/log 상태일 수 있으나, 우리 spliced+unspliced 합에서 재시작
    rna.layers["counts"] = rna.X.copy()
    sc.pp.normalize_total(rna, target_sum=1e4)
    sc.pp.log1p(rna)
    sc.pp.highly_variable_genes(rna, n_top_genes=min(N_HVG, rna.n_vars))
    sc.pp.pca(rna, n_comps=min(N_PCS, rna.n_vars - 1), random_state=SEED)
    sc.pp.neighbors(rna, n_neighbors=N_NEIGHBORS, random_state=SEED)
    sc.tl.leiden(rna, resolution=LEIDEN_RES, random_state=SEED, key_added="leiden")
    print(f"[graph] leiden clusters: {rna.obs['leiden'].nunique()}, "
          f"HVG: {int(rna.var['highly_variable'].sum())}", flush=True)

    # ── lineage annotation (marker score_genes → Leiden argmax) ──
    lin_scores = {}
    for lin, mk in LINEAGE_MARKERS.items():
        present = [g for g in mk if g in rna.var_names]
        if not present:
            continue
        sc.tl.score_genes(rna, present, score_name=f"_score_{lin}")
        lin_scores[lin] = f"_score_{lin}"
    if lin_scores:
        score_df = rna.obs[list(lin_scores.values())]
        score_df.columns = list(lin_scores.keys())
        cluster_lin = {}
        for cl in rna.obs["leiden"].cat.categories:
            m = rna.obs["leiden"] == cl
            cluster_lin[cl] = score_df.loc[m].mean(0).idxmax()
        rna.obs["lineage"] = rna.obs["leiden"].map(cluster_lin).astype("category")
    else:
        rna.obs["lineage"] = rna.obs["leiden"]
    rna.obs["lineage_rare"] = rna.obs["lineage"].astype(str).isin(RARE)
    print("  lineage 분포:\n    "
          + rna.obs["lineage"].value_counts().to_string().replace("\n", "\n    "), flush=True)

    # ── ATAC gene-level 정규화(figshare가 raw면 정규화; 이미 정규화면 방어적 재적용) ──
    atac_gene.obs["dataset"] = "macrophage"
    atac_gene.obs["lineage"] = pd.Categorical(
        pd.Index(atac_gene.obs_names).map(pd.Series(rna.obs["lineage"].astype(str).values,
                                                    index=rna.obs_names)))
    atac_gene.obs["leiden"] = pd.Categorical(
        pd.Index(atac_gene.obs_names).map(pd.Series(rna.obs["leiden"].astype(str).values,
                                                    index=rna.obs_names)))
    if "counts" not in atac_gene.layers:
        atac_gene.layers["counts"] = atac_gene.X.copy()
    sc.pp.normalize_total(atac_gene, target_sum=1e4)
    sc.pp.log1p(atac_gene)

    # cross-env 호환: uns None 값 제거
    def _portable(a):
        a.uns.pop("log1p", None)
        for k in list(a.uns):
            if a.uns[k] is None:
                del a.uns[k]
    _portable(rna); _portable(atac_gene)

    rna.write_h5ad(OUT / "rna_spliced_unspliced.h5ad")
    atac_gene.write_h5ad(OUT / "atac_gene.h5ad")
    print(f"[RNA] → rna_spliced_unspliced.h5ad {rna.shape} (velocity_layer_source={vsrc})", flush=True)
    print(f"[ATAC] → atac_gene.h5ad {atac_gene.shape}", flush=True)

    shared_g = sorted(set(rna.var_names) & set(atac_gene.var_names))
    print(f"[VERIFY] RNA↔ATAC obs identical: "
          f"{np.array_equal(rna.obs_names.to_numpy(), atac_gene.obs_names.to_numpy())}", flush=True)
    print(f"[VERIFY] RNA∩ATAC(gene) common genes: {len(shared_g)}", flush=True)
    for lyr in ("spliced", "unspliced"):
        M = rna.layers[lyr]
        nnz = (M.nnz / np.prod(M.shape)) if sp.issparse(M) else float((M != 0).mean())
        print(f"[VERIFY] {lyr} nnz={nnz:.4f} (must be >0)", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
