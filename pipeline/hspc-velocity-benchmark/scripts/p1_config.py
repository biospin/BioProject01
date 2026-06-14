"""P1 통일 전처리 설정 — 모든 임계값을 한 곳에. (DESIGN §3 공통 branch)

여기 값들은 *공통 branch* 기준. method-specific 전처리는 각 method 실행 단계에서.
임계값은 raw QC 분포를 보고 조정한다(아래 TODO).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]        # pipeline/hspc-velocity-benchmark
DATA = ROOT / "data" / "GSE209878"
OUT = ROOT / "data" / "processed"                  # 산출물(gitignore)

# sample = timepoint (GSM title 확정: MV-1=day0, MV-2=day7)
SAMPLES = {
    "MV-1": {"timepoint": "day0", "dir": DATA / "MV-1"},
    "MV-2": {"timepoint": "day7", "dir": DATA / "MV-2"},
}

# ── QC 임계값 (TODO: raw 분포 보고 조정 — qc_report 먼저 생성) ──
QC = {
    "min_genes_per_cell": 500,      # RNA
    "max_genes_per_cell": 8000,
    "max_pct_mito": 20.0,
    "min_cells_per_gene": 10,
    "min_counts_per_cell": 1000,
    # ATAC
    "min_peaks_per_cell": 1000,
    "min_cells_per_peak": 10,
    "doublet_method": "scrublet",   # per-sample 적용 후 merge
}

# ── 정규화 / HVG / graph ──
N_HVG = 2000                         # 원논문과 동일 스케일
N_PCS = 30
N_NEIGHBORS = 30                     # 공통 neighbor graph (shared-graph ablation 기준)
LEIDEN_RES = 1.0                     # method-agnostic annotation (DESIGN §3)
RANDOM_SEED = 0

# ── 산출물 경로 ──
OUT_RNA = OUT / "rna_spliced_unspliced.h5ad"   # spliced/unspliced layer 포함 통합 RNA
OUT_ATAC = OUT / "atac_peaks.h5ad"             # peak matrix
OUT_MUDATA = OUT / "hspc_multiome_common.h5mu" # 공통 branch 최종 (rna+atac, timepoint, annotation)
OUT_QC_REPORT = OUT / "qc_report.md"
