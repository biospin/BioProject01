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

# ── lineage marker (method-agnostic annotation; score_genes → Leiden cluster argmax) ──
# HSPC multiome 표준 marker. var_names에 있는 것만 사용. 모든 P3/P4 지표는 within-lineage.
LINEAGE_MARKERS = {
    "HSC/MPP":       ["CD34", "AVP", "HLF", "CRHBP", "MLLT3", "MEIS1"],
    "Erythroid":     ["GATA1", "KLF1", "HBB", "HBA1", "GYPA", "ALAS2", "TFRC"],
    "MK":            ["PF4", "PPBP", "ITGA2B", "GP9", "VWF"],          # rare
    "Myeloid":       ["SPI1", "MPO", "ELANE", "AZU1", "LYZ", "CSF1R", "CD14"],
    "Lymphoid":      ["IL7R", "DNTT", "CD79A", "EBF1", "VPREB1"],
    "Baso/Eo/Mast":  ["MS4A2", "CPA3", "HDC", "GATA2"],               # rare
    "pDC":           ["IRF8", "IRF7", "TCF4", "LILRA4"],              # rare
}
# rare lineage = within-lineage 지표에서 uncertainty 별도 보고 (CLAUDE.md 방법론 #2)
RARE_LINEAGES = {"MK", "Baso/Eo/Mast", "pDC"}

# ── 산출물 경로 ──
OUT_RNA = OUT / "rna_spliced_unspliced.h5ad"   # spliced/unspliced layer 포함 통합 RNA
OUT_ATAC = OUT / "atac_peaks.h5ad"             # peak matrix
OUT_MUDATA = OUT / "hspc_multiome_common.h5mu" # 공통 branch 최종 (rna+atac, timepoint, annotation)
OUT_QC_REPORT = OUT / "qc_report.md"

# ── cross-dataset 주입 (RUNBOOK 배선 gap ①) ──────────────────────────────────
# CROSS_DATASET_CONFIG env가 config_<dataset>.py를 가리키면 그 모듈의 dataset-specific
# 속성(경로·QC·marker)으로 이 모듈 globals를 override 한다. env 미설정 시 HSPC 동작 불변.
# (PYTHONPATH shim은 `python script.py` 실행 시 script 디렉터리가 sys.path[0]로 먼저 잡혀
#  무력화되므로 env 방식 채택. method 하이퍼파라미터 N_HVG/N_PCS/... 는 공정 비교 위해 유지.)
import os as _os
_XDS = _os.environ.get("CROSS_DATASET_CONFIG")
if _XDS:
    import importlib.util as _ilu
    _xp = Path(_XDS)
    if not _xp.is_absolute():
        _xp = (Path(__file__).resolve().parent / _XDS).resolve()
    _spec = _ilu.spec_from_file_location("_cross_dataset_config", _xp)
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)  # config_<dataset>은 `from p1_config import N_HVG...` (이 모듈 상단서 이미 정의됨 → 순환 안전)
    for _k in ("DATASET_NAME", "SPECIES", "TISSUE", "GEO_ACCESSION", "DATA", "OUT", "SAMPLES",
               "QC", "LINEAGE_MARKERS", "RARE_LINEAGES", "OUT_RNA", "OUT_ATAC", "OUT_MUDATA",
               "MITO_PREFIX", "OUT_QC_REPORT"):
        if hasattr(_mod, _k):
            globals()[_k] = getattr(_mod, _k)
    print(f"[p1_config] cross-dataset override ← {_xp.name} "
          f"(DATASET={globals().get('DATASET_NAME')}, OUT={OUT})")
