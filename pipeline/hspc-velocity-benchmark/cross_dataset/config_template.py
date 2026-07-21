"""Cross-dataset replication config template.

RUNBOOK.md의 지시에 따라 이 파일을 복사해서 config_<dataset>.py로 저장 후 편집한다.

⚠️ 중요(2026-07-01 정정): 아래 LINEAGE_MARKERS/RARE_LINEAGES를 p1_config에서
그대로 import하는 것은 **human HSPC(조혈) 전용**이라 mouse skin·human brain에
그대로 쓰면 annotation이 틀린다(세포종·marker가 완전히 다름). 모든 P3/P4 지표가
within-lineage라 lineage annotation이 틀리면 replication 자체가 무의미하다.
→ **dataset별로 LINEAGE_MARKERS·RARE_LINEAGES·QC를 조직/species에 맞게 재정의**할 것.
   (N_HVG/N_PCS/N_NEIGHBORS/LEIDEN_RES 등 method 하이퍼파라미터는 공정 비교 위해 동일 유지.)
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

# method 하이퍼파라미터는 공정 비교 위해 HSPC와 동일 유지.
from p1_config import (N_HVG, N_PCS, N_NEIGHBORS, LEIDEN_RES, RANDOM_SEED)

# ⚠️ 아래는 조직/species별로 반드시 재정의 (HSPC 조혈 marker 그대로 쓰면 annotation 틀림).
#    데이터 도착 후 해당 조직의 표준 marker/QC로 교체할 것.
from p1_config import (QC, LINEAGE_MARKERS, RARE_LINEAGES)   # TODO: dataset별 재정의

OUT_RNA    = OUT / "rna_spliced_unspliced.h5ad"
OUT_ATAC   = OUT / "atac_peaks.h5ad"
OUT_MUDATA = OUT / f"{DATASET_NAME}_multiome_common.h5mu"

# species별 mitochondria 유전자 prefix
MITO_PREFIX = "mt-" if SPECIES == "mouse" else "MT-"
