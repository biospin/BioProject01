# P0 — provenance · 환경 · 사전체크 (HSPC velocity benchmark)

> branch: `kkkim-pipeline` · 2026-06-13 · DESIGN.md Phase P0.
> 성격: 데이터/머신이 필요한 항목은 *본인 머신에서 실행*하도록 명령·스크립트로 정리. 검증 가능한 항목(license 등)은 완료 표시.

---

## 1. 데이터 출처 (GSE209878)

- **GEO**: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE209878 (PMID 36229609). Human HSPC, paired 10x Multiome, day0+day7, single donor.
- **확정 규모**(repo `li-2023-multivelo_core.md`): 11,605 cells · 1,000 genes(joint filtered) · 936 variable fit · 11 Leiden cluster · ~3,939 peaks.
- **다운로드 경로 2가지**:
  1. *raw/processed (1차)* — GEO GSE209878 supplementary (CellRanger ARC 출력 + 저자 제공 처리 객체).
     ```bash
     # GEO supplementary 묶음 (실제 파일명은 GEO 페이지에서 확인)
     # 예: GSE209878_RAW.tar, *_matrix.h5, *_atac_fragments.tsv.gz 등
     ```
  2. *MultiVelo tutorial 전처리본 (빠른 시작)* — MultiVelo(`welch-lab/MultiVelo`) HSPC 튜토리얼이 제공하는 전처리 AnnData/loom. spliced/unspliced + ATAC peak이 이미 정리돼 있어 P1 진입이 빠름. `검토필요:` 정확한 호스팅 URL은 MultiVelo repo 튜토리얼에서 확정.
- 저장 위치: `pipeline/hspc-velocity-benchmark/data/` (**gitignore — 커밋 금지**). raw + intermediate 200–500GB 여유 확보.

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
