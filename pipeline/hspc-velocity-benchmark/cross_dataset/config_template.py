"""Cross-dataset replication config template.

RUNBOOK.md의 지시에 따라 이 파일을 복사해서 config_<dataset>.py로 저장 후
아래 ── 수정 필요 ── 섹션만 편집한다.
나머지(QC/HVG/lineage marker 등)는 HSPC와 동일하게 유지해야 공정한 비교.
"""
from pathlib import Path
import sys

# ── 수정 필요 ──────────────────────────────────────────────────────
DATASET_NAME = "skin"                               # 짧은 식별자 (경로·파일명에 사용)
SPECIES      = "human"                              # human / mouse
TISSUE       = "skin"                               # 설명용
GEO_ACCESSION = "GSExxxxxx"                         # 알면 기입

ROOT   = Path(__file__).resolve().parents[1]        # pipeline/hspc-velocity-benchmark
DATA   = ROOT / "data" / DATASET_NAME               # raw 데이터 위치
OUT    = ROOT / "data" / f"processed_{DATASET_NAME}"

# 샘플별 디렉터리 & timepoint 라벨 (CellRanger ARC 결과 구조)
# 단일 샘플이면 하나만, 멀티 샘플이면 아래처럼 여러 개
SAMPLES = {
    "S1": {"timepoint": "ctrl", "dir": DATA / "sample1"},
    # "S2": {"timepoint": "treat", "dir": DATA / "sample2"},
}
# ── 여기까지 ──────────────────────────────────────────────────────

# 아래는 HSPC와 동일 유지 (공정 비교 위해 바꾸지 말 것)
from p1_config import (QC, N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES,
                        RANDOM_SEED, LINEAGE_MARKERS, RARE_LINEAGES)

OUT_RNA    = OUT / "rna_spliced_unspliced.h5ad"
OUT_ATAC   = OUT / "atac_peaks.h5ad"
OUT_MUDATA = OUT / f"{DATASET_NAME}_multiome_common.h5mu"

# species별 mitochondria 유전자 prefix
MITO_PREFIX = "mt-" if SPECIES == "mouse" else "MT-"
