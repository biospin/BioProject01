# Cross-Dataset External Replication — 즉시 실행 가이드

> **목적**: BIOP01 벤치마크 결과(method 순위·lag sign)를 외부 multiome 1개로 재현.
> P5 replication 조건 충족. 데이터 받으면 이 문서만 보고 바로 실행 가능.

---

## 0. 체크리스트 (시작 전 5분)

```bash
# 1) conda env 살아있는지
conda env list | grep -E "scv-preprocess|mv|torch"

# 2) 원본 HSPC 결과 있는지 (비교 기준)
ls ~/project/BioProject01/pipeline/hspc-velocity-benchmark/results/
#   → multivelo_genes.csv, rna_only_genes.csv, concordance.md 있어야 함

# 3) 디스크 여유 (최소 50GB)
df -h ~/project/
```

---

## 1. 데이터 준비

### 옵션 A: GEO 공개 데이터 (박상준 skin / 전연수 brain / 이건규 mouse brain)
```bash
# 팀원에게 GEO accession 받은 후
DATASET_ID="GSExxxxxx"   # ← 여기에 넣기
DATASET_NAME="skin"      # ← skin / human_brain / mouse_brain

mkdir -p ~/project/BioProject01/pipeline/hspc-velocity-benchmark/data/${DATASET_NAME}
cd ~/project/BioProject01/pipeline/hspc-velocity-benchmark/data/${DATASET_NAME}

# CellRanger ARC 결과 구조 확인 (HSPC와 동일해야 함)
# 필요 파일: barcodes.tsv.gz, features.tsv.gz, matrix.mtx.gz (RNA + ATAC 각각)
#            vel_spliced.loom, vel_unspliced.loom
```

### 옵션 B: 팀원이 처리된 h5ad/h5mu 직접 공유
```bash
# 팀원에게 요청할 파일:
# - rna_spliced_unspliced.h5ad (spliced/unspliced layer 포함)
# - atac_peaks.h5ad (gene-level aggregated)
# 이 경우 P1 건너뛰고 바로 P2부터

scp 팀원서버:/path/to/rna_spliced_unspliced.h5ad \
    ~/project/BioProject01/pipeline/hspc-velocity-benchmark/cross_dataset/${DATASET_NAME}/
```

---

## 2. config 생성 (2분)

```bash
DATASET_NAME="skin"   # ← 바꾸기
cp ~/project/BioProject01/pipeline/hspc-velocity-benchmark/cross_dataset/config_template.py \
   ~/project/BioProject01/pipeline/hspc-velocity-benchmark/cross_dataset/config_${DATASET_NAME}.py

# 편집: ROOT, DATA, SAMPLES 섹션만 수정
nano ~/project/BioProject01/pipeline/hspc-velocity-benchmark/cross_dataset/config_${DATASET_NAME}.py
```

---

## 3. P1 전처리 실행 (raw 데이터 있을 때만)

```bash
cd ~/project/BioProject01/pipeline/hspc-velocity-benchmark/scripts

# config 포인터 설정
export CROSS_DATASET_CONFIG="../cross_dataset/config_${DATASET_NAME}.py"

HDF5_USE_FILE_LOCKING=FALSE conda run --no-capture-output -n scv-preprocess \
  python -u p1_build.py --config "$CROSS_DATASET_CONFIG" \
  > /tmp/p1_${DATASET_NAME}.log 2>&1 &
echo "P1 PID: $! — 로그: /tmp/p1_${DATASET_NAME}.log"
```

---

## 4. P2 MultiVelo 실행 (핵심 — H1 비교용)

```bash
cd ~/project/BioProject01/pipeline/hspc-velocity-benchmark/scripts

# MultiVelo (CPU, ~2h)
HDF5_USE_FILE_LOCKING=FALSE OMP_NUM_THREADS=1 \
  conda run --no-capture-output -n mv \
  python -u p2_multivelo.py --dataset $DATASET_NAME \
  > /tmp/p2_mv_${DATASET_NAME}.log 2>&1 &
echo "MultiVelo PID: $!"

# RNA-only floor
HDF5_USE_FILE_LOCKING=FALSE \
  conda run --no-capture-output -n mv \
  python -u p2_rna_only.py --dataset $DATASET_NAME \
  > /tmp/p2_rna_${DATASET_NAME}.log 2>&1 &
```

---

## 5. P3 concordance (HSPC 결과와 비교)

```bash
# HSPC vs 새 dataset lag-sign rank 비교
HDF5_USE_FILE_LOCKING=FALSE \
  conda run --no-capture-output -n mv \
  python -u p3_concordance.py --dataset $DATASET_NAME --compare-to hspc \
  > /tmp/p3_${DATASET_NAME}.log 2>&1

# 결과 확인
cat ~/project/BioProject01/pipeline/hspc-velocity-benchmark/results/concordance_${DATASET_NAME}.md
```

---

## 6. GPU 버전 (류재면 회사 GPU or BIOP02 GPU free 후)

```bash
# MultiVeloVAE GPU
HDF5_USE_FILE_LOCKING=FALSE \
  conda run --no-capture-output -n torch \
  python -u p2_multivelovae.py --dataset $DATASET_NAME --gpu \
  > /tmp/p2_vae_${DATASET_NAME}.log 2>&1 &

# MoFlow GPU
PYTHONPATH=../ext/MoFlow/src \
  HDF5_USE_FILE_LOCKING=FALSE \
  conda run --no-capture-output -n torch \
  python -u p2_moflow.py --dataset $DATASET_NAME --gpu \
  > /tmp/p2_moflow_${DATASET_NAME}.log 2>&1 &
```

---

## 7. 결과 해석

```bash
# 핵심 질문: HSPC에서 상위 lag gene이 새 dataset에서도 일관적인가?
python -c "
import pandas as pd
hspc = pd.read_csv('results/multivelo_genes.csv', index_col=0)
new  = pd.read_csv('results/multivelo_genes_${DATASET_NAME}.csv', index_col=0)
common = hspc.index.intersection(new.index)
from scipy.stats import spearmanr
r, p = spearmanr(hspc.loc[common,'switch_time'], new.loc[common,'switch_time'])
print(f'공통 gene: {len(common)}, Spearman(lag rank): r={r:.3f}, p={p:.3e}')
print('→ |r| > 0.3 이면 외부 재현 성공 기준 (단일 replication)')
"
```

---

## 담당별 연락 포인트

| 담당 | 역할 | 요청 내용 |
|---|---|---|
| 박상준 | mouse skin multiome | GEO accession or processed h5ad 공유 |
| 전연수 | human brain multiome | GEO accession or processed h5ad 공유 |
| 이건규 | mouse brain | 7/7 이후 가능, 그 전엔 kkkim or 서정한 |
| 류재면 | 회사 GPU 제공 | GPU 사양·접속 방법·사용 일정 확인 |
