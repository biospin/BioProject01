"""Cross-dataset replication config — human fetal cortex multiome (GSE162170, Trevino et al. 2021).

cross-dataset 재현 1번 데이터셋. human이라 HSPC와 gene ID 축이 직접 겹쳐(ortholog 매핑 불필요)
lag-sign/rank cross-dataset 비교가 가장 깔끔하다. 원논문(MultiVelo)에서 TF→motif accessibility
lag을 낸 데이터셋으로, TF cascade가 풍부해 "lag fragile / α robust" 결론 확증 후보.

⚠️ LINEAGE_MARKERS/RARE_LINEAGES/QC는 HSPC 조혈에서 **재정의**했다(config_template §36 지시).
   method 하이퍼파라미터(N_HVG/N_PCS/N_NEIGHBORS/LEIDEN_RES/RANDOM_SEED)는 공정 비교 위해 HSPC와 동일 유지.
   marker는 데이터 도착 후 var_names 존재 여부로 필터링됨(있는 것만 사용). SAMPLES는 실제 파일 구조 확인 후 확정.
"""
from pathlib import Path

# ── 데이터셋 식별 ──────────────────────────────────────────────────
DATASET_NAME  = "human_brain"                        # 경로·파일명 식별자
SPECIES       = "human"
TISSUE        = "fetal cerebral cortex"
GEO_ACCESSION = "GSE162170"                          # Trevino et al. 2021, Cell

ROOT = Path(__file__).resolve().parents[1]           # pipeline/hspc-velocity-benchmark
DATA = ROOT / "data" / DATASET_NAME                  # raw 데이터 위치
OUT  = ROOT / "data" / f"processed_{DATASET_NAME}"

# 샘플별 디렉터리 & 라벨 (실제 CellRanger ARC / 공개 파일 구조 확인 후 확정 — placeholder)
# GSE162170은 여러 pcw(발생 주령) multiome 샘플. pseudotime은 발생축, day 라벨은 confound(batch) 취급.
SAMPLES = {
    "S1": {"timepoint": "pcw_early", "dir": DATA / "sample1"},
    # "S2": {"timepoint": "pcw_late",  "dir": DATA / "sample2"},
}
# ── 여기까지 데이터 도착 후 확정 ──────────────────────────────────

# method 하이퍼파라미터는 공정 비교 위해 HSPC와 동일 유지.
from p1_config import (N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, RANDOM_SEED)

# ── QC (태아 뇌에 맞게; 대체로 HSPC와 유사하나 데이터로 튜닝) ──
QC = {
    "min_genes_per_cell": 500,
    "max_genes_per_cell": 9000,     # neuron은 유전자 다양성 높음 → 상한 완화
    "max_pct_mito": 15.0,           # 태아 뇌 표준(신경세포 mito 민감)
    "min_cells_per_gene": 10,
    "min_counts_per_cell": 1000,
    "min_peaks_per_cell": 1000,
    "min_cells_per_peak": 10,
    "doublet_method": "scrublet",
}

# ── lineage marker (재정의: 태아 대뇌피질 표준 세포종) ──
# Trevino 2021 / 표준 cortical development marker. score_genes → Leiden cluster argmax.
# 모든 P3/P4 지표는 within-lineage → annotation이 replication의 근본.
LINEAGE_MARKERS = {
    "RG":         ["VIM", "HES1", "PAX6", "SOX2", "GLI3", "HOPX", "PTPRZ1", "SLC1A3", "TNC"],  # radial glia
    "Cycling":    ["MKI67", "TOP2A", "CENPF", "ASPM", "CLSPN"],                                 # cycling progenitor
    "nIPC":       ["EOMES", "PPP1R17", "NEUROG1", "NEUROG2", "PENK"],                           # neuronal IPC
    "ExN":        ["NEUROD2", "NEUROD6", "TBR1", "SATB2", "BCL11B", "STMN2", "SLC17A7", "FEZF2"], # 흥분성(glutamatergic) 뉴런
    "InN":        ["DLX1", "DLX2", "DLX5", "GAD1", "GAD2", "SLC32A1", "LHX6", "SP8"],            # 억제성 interneuron
    "OPC":        ["OLIG1", "OLIG2", "PDGFRA", "SOX10", "EGFR"],                                 # oligo/glial progenitor (rare)
    "Microglia":  ["AIF1", "C1QB", "PTPRC", "CX3CR1", "P2RY12"],                                 # rare
}
# rare lineage = within-lineage 지표에서 uncertainty 별도 보고 (CLAUDE.md 방법론 #2)
RARE_LINEAGES = {"OPC", "Microglia"}

# ── 산출물 경로 (dataset suffix로 HSPC 결과 덮어쓰기 방지) ──
OUT_RNA    = OUT / "rna_spliced_unspliced.h5ad"
OUT_ATAC   = OUT / "atac_gene.h5ad"     # gene-level(finalize_human_brain.py 집계). peak-level 원본은 atac_peaks.h5ad
OUT_MUDATA = OUT / f"{DATASET_NAME}_multiome_common.h5mu"

# species별 mitochondria 유전자 prefix
MITO_PREFIX = "mt-" if SPECIES == "mouse" else "MT-"
