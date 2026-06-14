"""P2 (method 실행) 공통 설정 — velocity method head-to-head (DESIGN §2,§7).

입력 = P1 공통 substrate (rna spliced/unspliced + atac gene-level + lineage).
arm: RNA-only floor / chromatin-aware / scrambled-chromatin(null) / graph ablation.
각 method는 격리 env에서 실행: RNA-only=scv-preprocess, MultiVelo=mv, VAE/MoFlow=torch, CRAK-Velo=tf.
"""
from pathlib import Path
import p1_config as p1

ROOT = p1.ROOT                              # pipeline/hspc-velocity-benchmark
PROC = p1.OUT                               # data/processed (P1 산출)
OUT_VELO = ROOT / "data" / "velocity"       # per-method 대용량 출력 (gitignore)
RESULTS = ROOT / "results"                  # tracked 요약 (csv/md)

IN_RNA = p1.OUT_RNA                         # rna_spliced_unspliced.h5ad
IN_ATAC = p1.OUT_ATAC                       # atac_peaks.h5ad (gene-level)
IN_MUDATA = p1.OUT_MUDATA                   # hspc_multiome_common.h5mu

# velocity gene set / graph (P1과 동일 파라미터로 공정성 유지)
N_TOP_GENES = 2000
N_PCS = p1.N_PCS
N_NEIGHBORS = p1.N_NEIGHBORS
RANDOM_SEED = p1.RANDOM_SEED
MIN_SHARED_COUNTS = 20                      # scVelo filter_and_normalize
N_JOBS = 4                                  # recover_dynamics 병렬 (CPU)
# MultiVelo 병렬: OMP_NUM_THREADS=1 고정 시 loky 워커가 fork-safe → 병렬 가능 가정
#   (thread oversubscription이 macOS SIGSEGV 원인이었음). 검증 후 확정.
MV_PARALLEL = True
MV_NJOBS = 6

RUNTIME_CSV = RESULTS / "runtime.csv"       # method×runtime/memory 누적 (DESIGN §4D)
