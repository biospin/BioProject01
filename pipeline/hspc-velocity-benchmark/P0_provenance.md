# P0 — provenance · 환경 · 사전체크 (HSPC velocity benchmark)

> branch: `kkkim-pipeline` · 2026-06-13 · DESIGN.md Phase P0.
> 성격: 데이터/머신이 필요한 항목은 *본인 머신에서 실행*하도록 명령·스크립트로 정리. 검증 가능한 항목(license 등)은 완료 표시.

---

## 1. 데이터 출처 (GSE209878)

- **GEO**: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE209878 (PMID 36229609). Human HSPC, paired 10x Multiome, single donor (mobilized CD34+). MultiVelo 원논문 데이터.
- **확정 규모**(repo `li-2023-multivelo_core.md`): 통합 후 11,605 cells · 1,000 genes(joint filtered) · 936 variable fit · 11 Leiden cluster · ~3,939 peaks. (아래는 통합 전 *raw per-sample*.)
- **2 sample = 2 timepoint** (GSM title로 확정 2026-06-13): `3423-MV-1` = **day0** ("RNA HSPC, 0th day, rep1", GSM6403408/09), `3423-MV-2` = **day7** (GSM6403410/11). → timepoint는 *sample 정체성*으로 보존되어 통합 객체 컬럼 유실과 무관(H2 게이트 부분 해소).

### 재현 다운로드 (다른 PC에서도 그대로)
```bash
bash pipeline/hspc-velocity-benchmark/scripts/download_data.sh   # → data/GSE209878/MV-1, MV-2 (~1.9 GB)
```
스크립트가 받는 핵심 파일 (sample당, **fragments 9.4GB는 불필요** — peak count가 matrix에 이미 포함):

| 파일 | 내용 | 크기 | URL (base) |
|---|---|---|---|
| `matrix.mtx.gz` | CellRanger ARC 통합 matrix (**GEX + ATAC Peaks**) | MV-1 582MB / MV-2 816MB | `…/series/GSE209nnn/GSE209878/suppl/GSE209878_3423-MV-{1,2}_matrix.mtx.gz` |
| `features.tsv.gz` / `barcodes.tsv.gz` | feature(=gene+peak) · cell 식별자 | 3MB / <1MB | 같은 GSE suppl |
| `feature_linkage.bedpe.gz` | peak–gene linkage | 소 | 같은 GSE suppl |
| `gex.loom.gz` | velocyto spliced/unspliced (velocity 입력) | MV-1 164MB / MV-2 274MB | `…/samples/GSM6403nnn/GSM640340{8,→MV-1}, {GSM6403410→MV-2}/suppl/` |
| `peak_annotation.tsv.gz` | peak→gene 주석 | 소 | `…/samples/…/GSM6403409(MV-1), GSM6403411(MV-2)/suppl/` |

- *받지 않는 것*: `GSE209878_RAW.tar`(9.8GB 전체), `*_atac_fragments.tsv.gz`(MV-1 4.3GB + MV-2 5.1GB; peak 재호출용 — 보통 불필요, 필요 시 `download_data.sh` 맨 아래 OPTIONAL 주석 해제).
- 저장 위치: `pipeline/hspc-velocity-benchmark/data/` (**gitignore — 커밋 금지**). raw + intermediate 200–500GB 여유 확보.
- *주의*: GEO raw에는 저자 통합·annotation 객체(11,605 cells + lineage label)가 없다 → 그건 P1 통일 전처리에서 method-agnostic하게 재생성(DESIGN §3).

---

## 2. 환경 전략 — **프레임워크별 격리 env 필수** (P0 핵심 발견)

method들이 **딥러닝 프레임워크가 충돌**한다 → 단일 env 불가. conda env를 프레임워크별로 분리한다.

| env | 포함 method | 핵심 스택 | 설치 |
|---|---|---|---|
| `scv-preprocess` | 공통 전처리 (P1) | scanpy, anndata, muon, snapatac2, numpy/pandas/scipy | conda + pip |
| `mv` | MultiVelo, scVelo(RNA-only floor) | multivelo, scvelo, scanpy (numba; **GPU 불요**) | `pip install multivelo scvelo` |
| `torch` | MultiVeloVAE, MoFlow | **PyTorch**(+Lightning) | `pip install` from welch-lab/MultiVeloVAE, AriHong/MoFlow |
| `tf` | CRAK-Velo, cellDancer | **TensorFlow** (UniTVelo 계열) + cisTopic | github StatBiomed/CRAK-Velo, `pip install celldancer` |

- **이유**: PyTorch(MultiVeloVAE/MoFlow) ↔ TensorFlow(CRAK-Velo/cellDancer)를 한 env에 두면 CUDA/버전 충돌. 격리가 안전.
- **GPU**: 1대면 충분(§7b). `torch`·`tf` env만 GPU 사용, `mv`는 CPU. 동일 GPU를 순차 점유.
- 각 env의 정확한 version pin은 1-fit 성공 후 `env/<name>.lock.yml`로 동결(재현성).

---

## 3. 사전체크 (DESIGN §8) — 상태

| 체크 | 상태 | 비고 |
|---|---|---|
| cell 수 | ✅ 11,605 | repo 검증 |
| method code license | ✅ | MultiVelo(welch BSD계열) / MultiVeloVAE **BSD-3** / MoFlow **MIT** / CRAK-Velo **BSD-3** / mmVelo **미확인**(선택 arm 보류) |
| GPU 필요성 | ✅ 선택 | CPU 충분, 1 GPU면 CRAK-Velo·bootstrap 가속 |
| **per-cell timepoint(day0/day7) 라벨 보존** | ⏳ 데이터 필요 | `scripts/check_data.py`로 확인 |
| **joint peak calling + timepoint ATAC QC** | ⏳ 데이터 필요 | check_data.py + fragments QC |
| **CPU/GPU 1-fit 시간·메모리** | ⏳ 머신 필요 | env 구축 후 method당 1회 측정 |
| **CBDir+GCBDir 단일 구현** | ⏳ | scVelo/UniTVelo metric util 조사 — 동일 input서 둘 다 계산 가능한지 |
| **CRAK-Velo lag proxy pilot** | ⏳ 데이터 필요 | 5–10 gene, switch time 대비 |
| **simulator(BEELINE/SERGIO) 후보** | ⏳ | injected-lag 가능 fork 조사 (DESIGN §5 accuracy arm) |
| dataset-info.yaml | ✅ | `analysis/_datasets/tenx-hspc-multiome-gse209878/dataset-info.yaml` |

---

## 4. 데이터-의존 사전체크 실행법

데이터를 `data/`에 받은 뒤:
```bash
python3 pipeline/hspc-velocity-benchmark/scripts/check_data.py <path-to-.h5ad-or-.h5mu>
```
→ cell/gene/peak 수, per-cell timepoint 라벨 유무, cluster/lineage annotation, spliced/unspliced layer, ATAC modality 유무를 보고. DESIGN §8의 데이터-의존 체크(특히 H2 가능 여부 = timepoint 라벨 보존)를 한 번에 답한다.

---

## 5. 다음 (P0 종료 조건)
1. 데이터 `data/`에 확보 → `check_data.py` 실행 → timepoint 라벨·peak·layer 확인.
2. `mv` env부터 구축 → MultiVelo 1-fit 재현(원논문 124분 CPU 대조) → 시간·메모리 기록.
3. CBDir/GCBDir 구현 소재 확정, simulator 후보 1개 선정.
4. 모두 통과 시 P1(통일 전처리) 진입.
