# P5 — Bootstrap lag-sign stability (DESIGN §4D, §4C 1차)

- crakvelo fit, 868 velocity-gene × 40 bootstrap(cell 복원추출), N_BIN=50, seed=20260701.
- sign_flip = min(부호>0 비율, 부호<0 비율). 0=완전 안정, 0.5=완전 불안정(동전).
- ⚠️ latent_time 고정(전체 re-fit 아님) → **stability 하한**.

## 결과

- **부호 안정 gene(sign_flip<0.10) = 83.3%**, median sign_flip = 0.000.
- lag CV median = 0.68 (|mean| 대비 변동).

### 가장 안정 / 불안정 gene (sign_flip)

| | gene | lag_mean | sign_flip | cv |
|---|---|---|---|---|
| 안정 | PRDM16 | -0.46 | 0.000 | 1.04 |
| 안정 | UTS2 | -0.93 | 0.000 | 0.72 |
| 안정 | PADI4 | +0.36 | 0.000 | 1.31 |
| 안정 | HSPG2 | +0.00 | 0.000 | nan |
| 안정 | RUNX3 | +0.57 | 0.000 | 0.84 |
| 안정 | CD52 | -1.88 | 0.000 | 0.89 |
| 안정 | ZBTB8A | -3.36 | 0.000 | 0.23 |
| 안정 | CLSPN | +2.27 | 0.000 | 1.47 |
| 불안정 | CD38 | +5.11 | 0.500 | 1.45 |
| 불안정 | SRGAP1 | +5.05 | 0.500 | 2.44 |
| 불안정 | ZDHHC14 | -0.36 | 0.475 | 9.30 |
| 불안정 | DENND2C | +3.08 | 0.425 | 2.36 |
| 불안정 | RTN1 | -0.82 | 0.425 | 4.64 |
| 불안정 | COL24A1 | -0.23 | 0.375 | 21.20 |
| 불안정 | EGF | +0.24 | 0.375 | 9.22 |
| 불안정 | PRR5L | -1.50 | 0.375 | 8.21 |

## 해석
- per-gene lag 부호는 cell 표집에 대체로 안정(median flip 0.000, 안정 83%).
- ⚠️ **이건 안정성의 *가장 약한* 형태**: latent_time·fit 고정 하에 *표집 노이즈*만 본 것. → cross-method 불일치(H1)·정확도 실패(simulator)와 **모순 아님**. lag은 '한 fit 안에선 표집에 안정'하지만 'method/정확도엔 비robust'. 진짜 stability(전체 re-fit 반복)는 이보다 낮음(GPU 반복 fit 시 측정).
- 용도: §71-C agreement-set 1차 기준(표집 안정 gene 우선)·P5 target gene 선별 필터로 사용.
