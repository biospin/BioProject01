"""Cross-dataset replication config — mouse gastrulation E7.5–8.75 10x Multiome (GSE205117).

5번째 cross-dataset 재현(사전등록: manuscript/PREREGISTRATION_gse205117.md). priming 극대(gastrulation)에서도
'α robust / lag fragile'가 유지되는지 확증. skin(#5) NO-GO 대체 채택.

── 취득 경로 ──────────────────────────────────────────────────────────
  - GEX : raw fastq(SRA) → 우리 STARsolo Velocyto(4 rep1 시점) → spliced/unspliced.
          E7.5=SRR19450575 · E8.0=SRR19450564 · E8.5=SRR19450560 · E8.75=SRR19450574.
  - ATAC: GEO 제공 processed fragments.tsv.gz(sample별). raw 정렬·cellranger-arc 불필요.
          E7.5=GSM6205427 · E8.0=GSM6205430 · E8.5=GSM6205434 · E8.75=GSM6205436.
  - peak→gene: **우리 자체 집계**(gencode vM25 gene body ±10kb). provider gene-activity 미사용(preprocessing confound 회피, repo 원칙).

── 종/축 주의 ─────────────────────────────────────────────────────────
  - mouse → cross-dataset 축은 E18과 동일하게 uppercase ortholog 매핑(_upper, 채점기에서 처리).
  - RNA var_names = mouse gene SYMBOL(STARsolo features col2, version 제거). ATAC 집계도 동일 SYMBOL 축.
  - method 하이퍼파라미터(N_HVG/N_PCS/N_NEIGHBORS/LEIDEN_RES/SEED)는 공정 비교 위해 HSPC와 동일.
  - lineage/marker는 concordance에 비-load-bearing(전역 per-gene fit rank; BMMC/macrophage 규약).
"""
from pathlib import Path

DATASET_NAME  = "gse205117"
SPECIES       = "mouse"
TISSUE        = "gastrulation (E7.5–E8.75) 10x Multiome"
GEO_ACCESSION = "GSE205117"

ROOT = Path(__file__).resolve().parents[1]        # pipeline/hspc-velocity-benchmark
DATA = ROOT / "data" / "gse205117"                # (build가 GEX solo + ATAC frag에서 직접 마감)
OUT  = ROOT / "data" / f"processed_{DATASET_NAME}"

# 4 rep1 시점: GEX SRR ↔ ATAC GSM(fragments) 매칭.
SAMPLES = {
    "E7.5":  {"gex_srr": "SRR19450575", "atac_gsm": "GSM6205427"},
    "E8.0":  {"gex_srr": "SRR19450564", "atac_gsm": "GSM6205430"},
    "E8.5":  {"gex_srr": "SRR19450560", "atac_gsm": "GSM6205434"},
    "E8.75": {"gex_srr": "SRR19450574", "atac_gsm": "GSM6205436"},
}

# method 하이퍼파라미터는 공정 비교 위해 HSPC와 동일.
from p1_config import (N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, RANDOM_SEED)

# QC (mouse; HSPC/human_brain와 정합 상한). STARsolo CellRanger2.2 세포필터 후라 대체로 방어적.
QC = {
    "min_genes_per_cell": 500,
    "max_genes_per_cell": 9000,
    "max_pct_mito": 15.0,
    "min_cells_per_gene": 10,
    "doublet_method": "none",   # provider doublet call 없음
}

# mouse gastrulation lineage marker (mouse symbol case; score_genes → Leiden argmax).
# concordance는 전역 fit rank라 lineage 비-load-bearing. 있는 marker만 사용.
LINEAGE_MARKERS = {
    "Epiblast":       ["Pou5f1", "Nanog", "Utf1", "Slc7a3", "Dppa5a"],
    "PrimitiveStreak":["T", "Mixl1", "Fgf8", "Wnt3", "Nkx1-2"],
    "Mesoderm":       ["Mesp1", "Tbx6", "Hand1", "Gata4", "Snai1", "Lefty2"],
    "Endoderm":       ["Foxa2", "Sox17", "Cer1", "Foxa1", "Trh"],
    "Ectoderm":       ["Sox2", "Pax6", "Sox1", "Nes", "Six3"],
    "Blood":          ["Gata1", "Klf1", "Hba-a1", "Runx1", "Hbb-bh1", "Gypa"],
    "Cardiac":        ["Nkx2-5", "Myl7", "Tnnt2", "Hand2"],
}
# rare lineage = within-lineage 지표에서 uncertainty 별도 보고(방법론 #2)
RARE_LINEAGES = {"Cardiac", "Blood"}

# ── 산출물 경로 (dataset suffix로 다른 데이터셋 결과 덮어쓰기 방지) ──
OUT_RNA    = OUT / "rna_spliced_unspliced.h5ad"
OUT_ATAC   = OUT / "atac_gene.h5ad"        # gene-level (우리 gene-window 집계)
OUT_MUDATA = OUT / f"{DATASET_NAME}_multiome_common.h5mu"
OUT_QC_REPORT = OUT / "qc_report.md"

# mouse mitochondria prefix = mt-
MITO_PREFIX = "mt-"
