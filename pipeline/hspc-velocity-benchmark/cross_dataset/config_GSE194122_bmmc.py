"""Cross-dataset replication config — human bone marrow BMMC 10x Multiome (GSE194122, NeurIPS 2021).

cross-dataset 재현 4번 데이터셋. **HSPC(GSE209878) 원본과 같은 조직축(human hematopoiesis)** →
동일 lineage(HSC/MPP·Erythroid·Myeloid·Lymphoid·MK…)라 same-tissue 최근접 replication.
gene ID 축이 UPPER-case로 HSPC와 직접 겹쳐 ortholog/case 매핑 불필요(E18와 다름).

이 데이터셋만의 특이점: GEO deposit이 processed h5ad에 layers=['counts']만 담고 spliced/unspliced가
없다 → **donor09(site4, SRR17693266) GEX possorted BAM에 velocyto run**을 돌려 loom을 복구한다.
ATAC는 processed h5ad의 peak matrix(116490 peaks, 'chr1-9776-10668' 표기)를 그대로 쓴다
(ARC peak_annotation/feature_linkage 미제공 → human_brain과 동일하게 gencode-proximity peak→gene 집계).

⚠️ 단일 donor(site4/donor9, 4325 cells) scope. E18/human_brain도 각 단일 set이었으니 정합.
   lineage = 제공된 obs['cell_type'](HSC, G/M prog, MK/E prog, Erythroblast, Lymph prog, …) 직접 사용
   (human hematopoiesis marker 강제 안 함; concordance는 전역 per-gene fit rank라 lineage 비-load-bearing).
   method 하이퍼파라미터(N_HVG/N_PCS/N_NEIGHBORS/LEIDEN_RES/RANDOM_SEED)는 공정 비교 위해 HSPC와 동일.
"""
from pathlib import Path

# ── 데이터셋 식별 ──────────────────────────────────────────────────
DATASET_NAME  = "GSE194122_bmmc"
SPECIES       = "human"
TISSUE        = "bone marrow mononuclear cells (BMMC)"
GEO_ACCESSION = "GSE194122"                       # NeurIPS 2021 multimodal; donor09=SRR17693266

ROOT = Path(__file__).resolve().parents[1]        # pipeline/hspc-velocity-benchmark
DATA = ROOT / "data" / "GSE194122"                # processed h5ad + recovered BAM/loom
OUT  = ROOT / "data" / f"processed_{DATASET_NAME}"

# 단일 donor (site4/donor9). day/timepoint 라벨 없음(성인 BM 스냅샷 1개).
SAMPLES = {
    "s4d9": {"timepoint": "adult_bm", "dir": DATA},
}

# method 하이퍼파라미터는 공정 비교 위해 HSPC와 동일 유지.
from p1_config import (N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, RANDOM_SEED)

# ── QC (human BMMC) ── HSPC/human_brain과 정합. 상한은 조혈이라 human_brain(9000)보다 조임.
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

# ── lineage: 제공된 obs['cell_type'] 사용(marker 강제 안 함, E18 규약과 동일) ──
# build_GSE194122_bmmc.py가 obs['cell_type']→obs['lineage']로 직접 이식.
# 여기 marker dict는 p1_config override 계약 충족용 빈 dict(concordance는 전역 fit rank).
LINEAGE_MARKERS = {}
# 희소 조혈 celltype (uncertainty 별도 — 방법론 #2). donor09 분포 기준 저빈도.
RARE_LINEAGES = {"pDC", "cDC2", "Plasma cell", "MK/E prog", "Normoblast", "ID2-hi myeloid prog", "ILC"}

# ── 산출물 경로 (dataset suffix로 HSPC/human_brain/e18 결과 덮어쓰기 방지) ──
OUT_RNA    = OUT / "rna_spliced_unspliced.h5ad"
OUT_ATAC   = OUT / "atac_gene.h5ad"       # gene-level (gencode-proximity 집계)
OUT_MUDATA = OUT / f"{DATASET_NAME}_multiome_common.h5mu"

# species별 mitochondria 유전자 prefix (human = MT-)
MITO_PREFIX = "MT-"
