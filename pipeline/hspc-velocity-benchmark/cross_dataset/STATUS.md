# Cross-Dataset External Replication — 실행 상태 (LIVE)

> ## ⏭️ 재로그인 시 즉시 이어서 할 것 (2026-07-05 저장)
> **다운로드·build·finalize 전부 완료됨** (아래 실측 확인). "다운로드 에러"로 보인 건 세션 종료였고 산출물은 완결 상태.
> **남은 것 = P2 → P3.** 순서:
> 1. **RNA-only floor (빠름)** — wiring end-to-end 검증 겸:
>    ```bash
>    cd pipeline/hspc-velocity-benchmark/scripts
>    CROSS_DATASET_CONFIG=../cross_dataset/config_human_brain.py CROSS_DATASET_SUFFIX=_human_brain \
>      HDF5_USE_FILE_LOCKING=FALSE conda run --no-capture-output -n scv-preprocess python -u p2_rna_only.py
>    # 성공 = results/rna_only_dynamical_genes_human_brain.csv 생성
>    ```
> 2. **MultiVelo (~2h CPU, background+log)** — SUFFIX write 확인됨(p2_multivelo.py L47/L101 `tag=cfg.SUFFIX+...` → `multivelo_genes_human_brain.csv`, HSPC 결과 안 덮음):
>    ```bash
>    CROSS_DATASET_CONFIG=../cross_dataset/config_human_brain.py CROSS_DATASET_SUFFIX=_human_brain \
>      HDF5_USE_FILE_LOCKING=FALSE conda run --no-capture-output -n mv python -u p2_multivelo.py \
>      > ../cross_dataset/p2_multivelo_human_brain.log 2>&1 &
>    # (먼저 --genes 20 스모크로 fit 경로 검증 권장)
>    ```
> 3. **P3 concordance** — HSPC vs human_brain switch_time rank (Spearman). HSPC 백스톱 csv(`results/multivelo_genes.csv`, `rna_only_dynamical_genes.csv`) 둘 다 **git-tracked 확인됨** → concordance 양쪽 입력 확보.
> **환경 주의**: floor는 `scv-preprocess`(HSPC floor와 동일 env=공정 비교), MultiVelo만 `mv`. STATUS 하단 옛 wiring 예시가 floor를 `-n mv`로 적은 건 무시.

> **마지막 갱신:** 2026-07-05
> **배경:** 담당 조율 결과 — 박상준 님이 "kkkim 직접 데이터 분석 진행해도 된다" 허락, 전연수 님 무응답.
> → **kkkim이 자율적으로 공개 데이터 다운로드·전처리 진행**하기로 결정 (블로커 없음).
> 이 결정과 진행이 이전 세션에서 기록 없이 중단됨 → 본 문서가 canonical 진행판.

---

## 타깃 데이터셋 (우선순위)

| # | 데이터셋 | Accession | 종류 | 공개 형식 | 상태 |
|---|---|---|---|---|---|
| 1 | **human fetal cortex** | GSE162170 (Trevino 2021, Cell) | human multiome | ✅ processed matrix (**spliced/unspliced 제공**) | **다운로드 완료** |
| 2 | mouse skin | GSE140203 (SHARE-seq, Ma 2020) | SHARE-seq | ⚠️ `GSE140203_RAW.tar`만 (spliced/unspliced 없음 → raw 처리 필요) | 후순위(heavy) |
| 3 | mouse brain | 10x embryonic (미확정 accession) | 10x multiome | 미확인 | 후순위 |

**우선순위 근거:** GSE162170만이 (a) human이라 HSPC와 gene ID 축 직접 겹침(ortholog 불필요),
(b) 공개 supplement에 spliced/unspliced counts 직접 제공 → velocyto/BAM 재처리 불필요.
→ **human brain을 depth-first로 end-to-end(변환→P2→concordance) 완주**해 wiring을 검증하면 나머지 2개가 재사용.

## GSE162170 다운로드 완료 파일 (`data/human_brain/`)
- `GSE162170_multiome_rna_counts.tsv.gz` (24M)
- `GSE162170_multiome_spliced_rna_counts.tsv.gz` (11M) ← spliced
- `GSE162170_multiome_unspliced_rna_counts.tsv.gz` (15M) ← unspliced
- `GSE162170_multiome_atac_counts.tsv.gz` (150M) ← peak counts (sparse 로드 필수)
- `GSE162170_multiome_atac_consensus_peaks.txt.gz`
- `GSE162170_multiome_cell_metadata.txt.gz`
- `GSE162170_multiome_cluster_names.txt.gz`
- (미다운로드/선택) `..._atac_gene_activities.tsv.gz` (832M) — **사용 안 함**: provider gene-activity를 쓰면
  method와 preprocessing이 confound. HSPC와 동일한 peak→gene 집계를 우리가 수행.

---

## 파이프라인 인터페이스 (코드 실측 — RUNBOOK보다 우선)

- `p1_build.py` → `import p1_config`, `p2_multivelo.py` → `import p2_config`, `p3_concordance.py` → `import p1_config, p2_config`.
- **RUNBOOK의 `--config`/`--dataset` argparse는 실재하지 않음.** config는 모듈명 `p1_config`로 하드코딩 import.
- `p2_config`의 입력/출력 경로는 전부 `p1_config`에서 파생(IN_RNA=p1.OUT_RNA, ...). → **주입 지점 = p1_config**.
- human brain은 processed spliced/unspliced 보유 → **P1(CellRanger ARC + velocyto loom) 건너뜀(RUNBOOK option B)**,
  대신 tsv → `data/processed_human_brain/{rna_spliced_unspliced,atac_peaks}.h5ad` 직접 생성.

## 실행 계획 (human brain)
- [x] domain gap 처리: `config_human_brain.py` (cortical marker/QC 재정의 완료)
- [x] GSE162170 multiome 다운로드
- [x] **변환** (`build_human_brain.py`): tsv → `rna_spliced_unspliced.h5ad`(8981×32581, X=spliced+unspliced, layers spliced/unspliced, symbol축) + `atac_peaks.h5ad`(8981×467315 peak-level sparse). RNA var_names unique 처리(중복 19).
- [x] **검증**: RNA↔ATAC obs_names 동일, 전부 finite, spliced nnz 2.5%/unspliced 3.8%.
- [x] **wiring gap 처리 (①③)**: `scripts/p1_config.py`에 `CROSS_DATASET_CONFIG` env override 블록 추가(env 미설정 시 HSPC byte-identical) + `p2_config.SUFFIX`(=`CROSS_DATASET_SUFFIX`) → p2_multivelo/p2_rna_only 출력명 suffix. **⚠️ PYTHONPATH shim은 실패**(`python script.py`가 script 디렉터리를 sys.path[0]로 먼저 잡아 무력화) → env 방식으로 확정. `run_all.sh` 대신 `CROSS_DATASET_CONFIG=... CROSS_DATASET_SUFFIX=_human_brain` 직접 지정.
- [x] **P1-equivalent finalize** (`finalize_human_brain.py`, **완료** 2026-07-05): QC(mito≤15/genes/Singlet) → counts layer → normalize_total(1e4)+log1p → HVG(2000) → PCA(30)+neighbors(30) → leiden → cortical lineage annotation. + **ATAC peak→gene 집계**(gencode v44 gene body ±10kb, GSE162170이 10x peak_annotation 미제공 → mv.aggregate_peaks_10x 불가 대체) → `atac_gene.h5ad`. config OUT_ATAC를 atac_gene.h5ad로 변경.
  - **산출 실측**: `rna_spliced_unspliced.h5ad` 8414×32581 (QC 8981→8414), layers=counts/spliced/unspliced, leiden+lineage 존재 — lineage: ExN 5014 / InN 1693 / RG 1172 / OPC 275 / Cycling 209 / Microglia 51. `atac_gene.h5ad` 8414×22432 (cell 정합).
- [ ] **P2 full**: RNA-only floor(`rna_only_dynamical_genes_human_brain.csv`) + MultiVelo(`multivelo_genes_human_brain.csv`, ~2h CPU)
- [ ] **P3 concordance**: HSPC vs human_brain switch_time rank (Spearman, RUNBOOK §7 style) → `results/concordance_human_brain.md`

## wiring 실행 명령 (확정)
```bash
cd pipeline/hspc-velocity-benchmark/scripts
CROSS_DATASET_CONFIG=../cross_dataset/config_human_brain.py CROSS_DATASET_SUFFIX=_human_brain \
  HDF5_USE_FILE_LOCKING=FALSE conda run --no-capture-output -n mv python -u p2_rna_only.py    # floor
#   ...p2_multivelo.py 도 동일 env로. 출력은 자동으로 *_human_brain.csv (HSPC 결과 보호).
```

## 알려진 함정 (advisor)
1. **mouse concordance**: `hspc.index ∩ new.index`가 mouse는 case 불일치(`Gata1`≠`GATA1`)로 ~0 → ortholog/case 매핑 선행 필수. human brain은 무관.
2. **ATAC**: provider gene_activities 쓰지 말고 HSPC와 동일 peak→gene 집계. 150M ATAC counts는 sparse 로드.
3. **foreign spliced/unspliced 주입**: dataset 내부 method 비교는 동일 입력 공유라 무편향. cross-dataset per-gene concordance엔 noise만 추가 → "lag fragile" 결론에 보수적. OK.
