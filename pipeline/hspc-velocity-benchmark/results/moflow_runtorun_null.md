# MoFlow run-to-run null — 세포·ATAC 고정, 독립 재실행만 반복

> 생성 = `scripts/p10g_moflow_runtorun_null_audit.py` (fit = `scripts/p2_moflow_runtorun_refit.py`).
> 신규 격리 산출물이다. `velocity_matrix_audit.*` · `scrambled_null_moflow.md` · `FINDINGS.md` · draft 는 읽기만 하고 건드리지 않는다.

## 0. 무엇을 재는가

층② 세포x유전자 velocity 행렬 감사에서 MoFlow가 낀 근접-0 세 쌍은 method 간 실제 불일치인지 MoFlow 한 arm의 내부 불안정인지 구분되지 않았다(REVIEW-GB-2026-07-19b MAJOR-1). MultiVelo가 이미 가진 재현성 천장(재표본 재적합 대비 +0.826~+0.887)의 대응물을, MoFlow는 세포 bootstrap이 없으므로 **동일 입력 독립 재실행**으로 잰다.

## 1. 근접-0 세 쌍 원값 (재계산 아님, 대조용)

| pair | cell_cos_excess (원값, `velocity_matrix_audit.json`) | 중심화 코사인 (재계산) |
|---|---|---|
| MultiVelo × MoFlow | -0.0121 | -0.0118 |
| MoFlow × CRAK-Velo | +0.0026 | +0.0019 |
| MoFlow × MultiVeloVAE | +0.0030 | +0.0019 |

## 2. MoFlow 재현성 천장 (원본 vs 독립 재실행)

| run | n_cell | n_gene | 중심화 코사인 [95% CI] | raw 중앙값 | 세포-셔플 null | raw 초과분 | 부호일치 |
|---|---|---|---|---|---|---|---|
| 1 | 21878 | 354 | +0.9999 [+0.9999, +0.9999] | +0.9997 | +0.3672 | +0.6326 | 99.8% |
| 2 | 21878 | 354 | +0.9999 [+0.9999, +0.9999] | +0.9997 | +0.3674 | +0.6324 | 99.8% |

run1 대 run2(원본을 거치지 않은 직접 비교, n_gene=354): 중심화 코사인 +1.0000 [+1.0000, +1.0000]

## 3. 셔플 Δ 재계산 (봉인 수치 재현)

원본×MoFlow-scr 중심화 코사인 재계산 +0.1126 [+0.1112, +0.1139] (n_gene=353) — 봉인 보고 +0.113(`velocity_matrix_audit.md` §6)과 대조.

## 4. 판정 대비 봉인 기준

**MOFLOW-REPRODUCIBLE (근접-0 쌍은 arm 불안정으로 설명 안 됨)**

- 가장 보수적인 run의 lower CI(천장) +0.9999 vs 근접-0 세 쌍 중심화 코사인 |값| 최댓값 0.0118 → True

## 5. 한계

- 재실행 축만 쟀다. MultiVelo 처럼 세포 재표본까지 곱한 이중 축은 MoFlow에 없다(전체 세포 단일 fit 구조이므로 bootstrap 축 자체가 성립하지 않는다).
- run 수는 2로 적다. 분산 추정의 정밀도는 MultiVelo의 6-refit 천장보다 낮다.
- 이 감사는 `velo_s`(cell x gene velocity 행렬) 축만 본다. DTW c-s lag(`cs_lag_median`) 축의 재현성 상한은 별도이며 `scrambled_null_moflow.md` §4의 유보가 그대로 유효하다.
- 판정은 중심화 코사인 기준으로 봉인했다. raw 초과분(§1~2 표)은 대조용으로만 병기한다.

## 산출물

`results/moflow_runtorun_null.json` · `scripts/p10g_moflow_runtorun_null_audit.py` · `scripts/p2_moflow_runtorun_refit.py`
