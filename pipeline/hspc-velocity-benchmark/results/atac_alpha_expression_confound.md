# P5b — baseline ATAC→α 가 발현(abundance) confound인지 검정

> BIOP01-42(brain, sjpark) self-review에서 baseline chromatin→α(+0.212)가 발현 통제 시 +0.013으로 소멸. HSPC 원고 대응 주장(draft_v2 L81, real-atac held-out ρ=+0.309)의 동일 위험을 확인.

- gene 472종, target=fit_alpha, leave-one-lineage-out Ridge(원 p5_lag_model_atac.py 재사용).
- 발현=coupling_per_gene.csv 의 abundance(steady-state spliced), log1p.

## held-out lineage 일반화 (Spearman pred vs actual α)

| feature set | held-out ρ |
|---|---|
| atac (원 주장) | **+0.309** |
| abund (발현만) | **+0.724** |
| abund+atac | **+0.708** |
| ATAC 증분(abund+atac − abund) | **-0.016** |

## 발현 통제 부분상관

- ATAC-pred α ↔ actual α: raw ρ=+0.309 → **발현통제 partial ρ=+0.112** (n=472).
- 참고: abundance ↔ α raw ρ=+0.785.

### 개별 ATAC feature vs α (raw → 발현통제 partial)

| feature | raw ρ | partial ρ (|abundance) |
|---|---|---|
| prom_acc | -0.128 | -0.453 |
| enh_acc | +0.228 | -0.049 |
| enh_sum | +0.318 | -0.009 |
| prom_enh_ratio | -0.246 | -0.292 |
| n_enh | +0.352 | +0.084 |

## 판정

- **ATAC 신호가 발현으로 상당 부분 설명됨 (confound 위험)**.
  기준: abund+atac 가 abund 를 +0.05 이상 상회(증분 -0.016) **그리고** 발현통제 partial |ρ|≥0.10 (=+0.112).
- brain(+0.212→+0.013 소멸)과 대비해 HSPC의 결과를 위 수치로 정직히 보고.
- ⚠️ abundance=steady-state spliced는 α와 구조적으로 연관(정상상태 abundance≈α/γ)이라 부분상관은 보수적(과통제 가능). 증분 CV와 함께 읽는다.
