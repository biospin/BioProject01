"""Cross-dataset replication config — human HSPC→macrophage differentiation 10x Multiome
(MultiVeloVAE 신규 데이터셋; Li & Gu et al. Nat Commun 16, 11505, 2025).

cross-dataset 재현 5번 데이터셋. **HSPC(GSE209878)와 같은 human 조혈축**의 하류(단핵구→대식세포
분화)를 커버 → same-lineage 하류 확장이자 drug-timing endpoint(대식세포 성숙)에 가장 근접.
human이라 gene SYMBOL 축이 HSPC와 직접 겹쳐 ortholog/case 매핑 불필요(E18와 다름).

── accession / 취득 경로 (2026-07-09 verify) ────────────────────────────────
  - raw(GEO GSE284047)는 **dbGaP phs002915.v2.p1 제한접근**(환자 프라이버시) → 사용 불가.
  - 공개 경로 = **figshare 10.6084/m9.figshare.30280333 (CC BY 4.0)**, MultiVeloVAE post-processed AnnData.
  - macrophage 파일(= "One HSPC + one macrophage" concat):
      RNA : 8489-MV-1-9060-MV-3_adata_postpro_concat.h5ad       (189.86 MB, figshare file 58495783)
      ATAC: 8489-MV-1-9060-MV-3_adata_atac_postpro_concat.h5ad  ( 64.95 MB, figshare file 58495777, **gene-level**)

⚠️ velocity-ready 형태 주의 (build_macrophage.py가 처리):
  - postpro RNA는 **HVG 필터 + scVelo moments 완료** 상태(layers `Ms`/`Mu` 확인). raw spliced/unspliced
    count layer는 유지 안 된 것으로 보임(byte-scan 4구간 모두 Ms/Mu만, spliced/unspliced 없음).
    → 우리 공통 전처리(normalize→HVG→PCA→neighbors→moments) 분기점이 다른 3종과 어긋남(방법론 #5).
    human_brain의 "외부 제공 spliced/unspliced" caveat보다 더 pre-baked → Methods에 명시. concordance엔
    노이즈만 더해 "lag fragile" 결론에 보수적.
  - concat은 HSPC(8489-MV-1) + macrophage(9060-MV-3) 2 batch. **macrophage batch만 subset**해야
    우리 primary(HSPC)가 external set에 새는 leakage를 막는다. (build_macrophage.py MACRO_BATCH)

⚠️ LINEAGE_MARKERS/RARE_LINEAGES/QC는 HSPC 조혈에서 **재정의**(config_template §36 지시).
   method 하이퍼파라미터(N_HVG/N_PCS/N_NEIGHBORS/LEIDEN_RES/RANDOM_SEED)는 공정 비교 위해 HSPC와 동일 유지.
   marker는 build 시 var_names 존재 여부로 필터(있는 것만). concordance는 전역 per-gene fit rank라
   lineage 비-load-bearing(BMMC 규약과 동일).
"""
from pathlib import Path

# ── 데이터셋 식별 ──────────────────────────────────────────────────
DATASET_NAME  = "macrophage"
SPECIES       = "human"
TISSUE        = "HSPC-derived macrophage differentiation (in vitro)"
GEO_ACCESSION = "GSE284047"                       # raw=dbGaP phs002915.v2.p1(제한); 공개=figshare 30280333

ROOT = Path(__file__).resolve().parents[1]        # pipeline/hspc-velocity-benchmark
DATA = ROOT / "data" / "macrophage"               # figshare postpro h5ad 2개 위치
OUT  = ROOT / "data" / f"processed_{DATASET_NAME}"

# 단일 macrophage sample(9060-MV-3). timepoint 라벨 없음(in-vitro 분화 스냅샷 1개).
# (concat 원본은 HSPC+macrophage 2 batch — build가 macrophage batch만 subset)
SAMPLES = {
    "9060-MV-3": {"timepoint": "macro_diff", "dir": DATA},
}

# method 하이퍼파라미터는 공정 비교 위해 HSPC와 동일 유지.
from p1_config import (N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, RANDOM_SEED)

# ── QC (human; HSPC/BMMC와 정합) ──
# postpro는 이미 QC/HVG 통과 상태라 이 QC는 방어적 재적용(대체로 no-op). HSPC 상한과 정합.
QC = {
    "min_genes_per_cell": 500,
    "max_genes_per_cell": 8000,
    "max_pct_mito": 20.0,
    "min_cells_per_gene": 10,
    "min_counts_per_cell": 1000,
    "min_peaks_per_cell": 1000,
    "min_cells_per_peak": 10,
    "doublet_method": "scrublet",
}

# ── lineage marker (재정의: HSPC→monocyte→macrophage 분화축, human) ──
# score_genes → Leiden cluster argmax. build 시 var_names에 있는 marker만 사용.
# 모든 P3/P4 지표는 within-lineage; concordance는 전역 fit rank(lineage 비-load-bearing, BMMC 규약).
LINEAGE_MARKERS = {
    "HSPC":        ["CD34", "KIT", "PROM1", "SPINK2", "AVP", "HLF", "MLLT3"],           # 시작 progenitor
    "GMP":         ["MPO", "ELANE", "AZU1", "PRTN3", "CTSG", "LYST"],                    # granulo-mono 전구
    "Monocyte":    ["CD14", "LYZ", "FCN1", "S100A8", "S100A9", "VCAN", "CSF1R", "CSF3R"],
    "Macrophage":  ["CD68", "CD163", "MRC1", "MERTK", "MARCO", "MSR1", "APOE",
                    "C1QA", "C1QB", "C1QC", "ITGAM", "SPP1"],                            # 성숙 대식세포
    "DC":          ["FCER1A", "CD1C", "CLEC10A", "IRF8"],                                # rare(분지 가능)
    "Cycling":     ["MKI67", "TOP2A", "CENPF", "ASPM"],                                  # 증식 progenitor
}
# rare lineage = within-lineage 지표에서 uncertainty 별도 보고 (방법론 #2)
RARE_LINEAGES = {"DC", "Cycling"}

# ── 산출물 경로 (dataset suffix로 HSPC/human_brain/e18/bmmc 결과 덮어쓰기 방지) ──
OUT_RNA    = OUT / "rna_spliced_unspliced.h5ad"
OUT_ATAC   = OUT / "atac_gene.h5ad"       # gene-level (figshare adata_atac_postpro가 이미 gene축)
OUT_MUDATA = OUT / f"{DATASET_NAME}_multiome_common.h5mu"

# species별 mitochondria 유전자 prefix (human = MT-)
MITO_PREFIX = "MT-"
