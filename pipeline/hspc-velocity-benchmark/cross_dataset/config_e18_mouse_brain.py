"""Cross-dataset replication config — E18 mouse brain 10x Multiome (MultiVelo tutorial dataset).

cross-dataset 재현 2번 데이터셋 (Track D). 비-조혈 조직(태아 뇌)에서 HSPC 핵심 결론
  "gene별 chromatin→transcription lag은 method-robust하지 않지만 transcription rate α는 robust(cross-method ρ≈0.88)"
가 재현되는지 검정.

이 데이터셋은 MultiVelo 공식 튜토리얼 데이터라 mv.aggregate_peaks_10x P1 경로가 거의 그대로 적용된다
(human_brain은 tsv 전처리였지만 E18은 loom + filtered_feature_bc_matrix + peak_annotation + feature_linkage
 → HSPC p1_build와 동일한 ATAC 집계 경로).

⚠️ human hematopoiesis LINEAGE_MARKERS를 mouse brain에 강제하지 않는다(advisor·task 지시).
   제공된 cell_annotations.tsv의 celltype을 obs['celltype']/obs['lineage']로 직접 사용
   (concordance는 *전역* per-gene fit rank라 lineage는 load-bearing 아님 — p3_crossdataset caveat 참조).
   method 하이퍼파라미터(N_HVG/N_PCS/N_NEIGHBORS/LEIDEN_RES/RANDOM_SEED)는 공정 비교 위해 HSPC와 동일.
"""
from pathlib import Path

# ── 데이터셋 식별 ──────────────────────────────────────────────────
DATASET_NAME  = "e18_mouse_brain"
SPECIES       = "mouse"
TISSUE        = "E18 embryonic brain"
GEO_ACCESSION = "10x_e18_mouse_brain_fresh_5k"   # no GSE; CellRanger-ARC 1.0.0 demo

ROOT = Path(__file__).resolve().parents[1]        # pipeline/hspc-velocity-benchmark
DATA = ROOT / "data" / DATASET_NAME               # raw (loom + filtered_feature_bc_matrix + annotations)
OUT  = ROOT / "data" / f"processed_{DATASET_NAME}"

# 단일 sample (MultiVelo 튜토리얼). day/timepoint 라벨 없음(발생 스냅샷 1개).
SAMPLES = {
    "E18": {"timepoint": "e18", "dir": DATA},
}

# method 하이퍼파라미터는 공정 비교 위해 HSPC와 동일 유지.
from p1_config import (N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, RANDOM_SEED)

# ── QC (mouse embryonic brain) ──
QC = {
    "min_genes_per_cell": 500,
    "max_genes_per_cell": 9000,     # 뉴런 유전자 다양성 높음 → 상한 완화(human_brain과 동일)
    "max_pct_mito": 15.0,
    "min_cells_per_gene": 10,
    "min_counts_per_cell": 1000,
    "min_peaks_per_cell": 1000,
    "min_cells_per_peak": 10,
    "doublet_method": "scrublet",
}

# ── lineage: 제공된 cell_annotations.tsv celltype 사용(marker 강제 안 함) ──
# build_e18_mouse_brain.py가 obs['celltype']→obs['lineage']로 직접 이식. 여기 marker dict는
# p1_config override 계약 충족용 빈 dict(p2 arm은 marker 미사용; concordance는 전역 fit rank).
LINEAGE_MARKERS = {}
RARE_LINEAGES = {"Microglia", "Cajal-Retzius"}   # 희소 celltype (uncertainty 별도 — 방법론 #2)

# ── 산출물 경로 (dataset suffix로 HSPC/human_brain 결과 덮어쓰기 방지) ──
OUT_RNA    = OUT / "rna_spliced_unspliced.h5ad"
OUT_ATAC   = OUT / "atac_gene.h5ad"       # gene-level (mv.aggregate_peaks_10x)
OUT_MUDATA = OUT / f"{DATASET_NAME}_multiome_common.h5mu"

# species별 mitochondria 유전자 prefix (mouse = mt-)
MITO_PREFIX = "mt-"
