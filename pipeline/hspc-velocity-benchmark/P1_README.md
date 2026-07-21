# P1 — 통일 전처리 (공통 branch)

> DESIGN §3 구현. "공통까지 동일 → 이후 method-specific 분기"로 method 차이를 preprocessing
> 차이와 분리(C2). scv-preprocess env에서 실행.

## 실행
```bash
# 0) loom 압축 해제 (scvelo가 .loom 직접 읽음)
gunzip -k pipeline/hspc-velocity-benchmark/data/GSE209878/MV-1/gex.loom.gz
gunzip -k pipeline/hspc-velocity-benchmark/data/GSE209878/MV-2/gex.loom.gz
# 1) 빌드
conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/p1_build.py
# 2) 검증
conda run -n scv-preprocess python pipeline/hspc-velocity-benchmark/scripts/check_data.py \
    pipeline/hspc-velocity-benchmark/data/processed/hspc_multiome_common.h5mu
```

## 파이프라인 (p1_build.py)
1. **load_sample** — CellRanger ARC matrix(GEX+Peaks) `sc.read_10x_mtx(gex_only=False)` → GEX/Peaks 분리, velocyto loom의 spliced/unspliced 병합, `timepoint`(day0/day7)·`sample` 라벨.
2. **qc_sample** — per-sample QC(min/max genes, %mito) + scrublet doublet 제거. ATAC를 통과 cell로 정렬.
3. **결합** — 두 timepoint concat(per-cell `timepoint` 보존), ~11,605 cells 근처 목표.
4. **공통 정규화/HVG/graph** — normalize_total+log1p, HVG 2,000, PCA 30, neighbors 30(공통 graph = shared-graph ablation 기준).
5. **method-agnostic annotation** — Leiden(res 1.0). MultiVelo-native annotation 비의존(DESIGN §3 home-field 제거).
6. **저장** — `data/processed/`: `rna_spliced_unspliced.h5ad`, `atac_peaks.h5ad`, `hspc_multiome_common.h5mu`.

## 조정 필요 (TODO — raw 분포 보고)
- `p1_config.QC` 임계값: 먼저 QC 분포를 보고 min_genes/%mito 등 조정 (현재는 합리적 default).
- **loom↔ARC barcode 매칭**: velocyto barcode 접두/접미가 ARC와 다르면 `scv.utils.clean_obs_names`로 양쪽 정규화 후 merge (p1_build에 TODO 표시).
- **ATAC 정규화**: 현재 normalize_total+log1p. method가 TF-IDF/LSI를 요구하면 교체 (CRAK-Velo/MultiVelo 요구 확인).
- **lineage 라벨**: Leiden cluster → marker 기반 lineage(erythroid GATA1/KLF1, myeloid SPI1/MPO, …) 매핑은 별도 annotate 단계로 추가.
- **ambient RNA**: scrublet(doublet)만 포함. ambient(CellBender/SoupX)는 필요 시 별도(검토자 지적).

## 다음 (P2)
공통 MuData → method별 분기 실행(MultiVelo/MultiVeloVAE/MoFlow/CRAK-Velo + RNA-only floor + scrambled-chromatin). native vs 공통 graph ablation 포함.
