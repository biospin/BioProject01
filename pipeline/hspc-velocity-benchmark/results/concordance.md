# P3 — Concordance & construct-validity

- **multivelo**: fit gene 538
- **scvelo_floor**: fit gene 487

## 1. MultiVelo lag (fit_t_sw2 − fit_t_sw1, pseudotime)
- n=538, median **5.98**, mean 6.41, IQR [3.14, 9.17]
- lag>0 비율 100.0%
- ⚠️ **구조적 caveat**: MultiVelo 4-state는 switch time을 **단조 정렬**(t_sw1<t_sw2<t_sw3)하므로 `sw2−sw1`은 *정의상 항상 양수*다. 따라서 100%는 priming 증거가 아니라 모델 제약 — **sign은 무정보, lag *크기*의 gene간 변이만 정보**다. 진짜 directional sign check는 sign이 가변인 method(MoFlow DTW c-s lag 등)에서 수행해야 함(DESIGN §4B).

## 2. Construct-validity — marker gene lag (크기)

> sign은 §1 caveat대로 구조적 양수 → 여기선 **lag 크기**(gene간 변이)를 본다.

| lineage | gene | lag(sw2-sw1) | sw1 | sw2 |
|---|---|---|---|---|
| HSC/MPP | HLF | 2.68 | 5.09 | 7.76 |
| HSC/MPP | CRHBP | 11.32 | 8.71 | 20.04 |
| HSC/MPP | MEIS1 | 3.93 | 2.53 | 6.45 |
| Erythroid | TFRC | 8.28 | 11.73 | 20.02 |
| MK | ITGA2B | 4.58 | 6.50 | 11.08 |
| MK | VWF | 4.08 | 8.25 | 12.33 |
| Myeloid | MPO | 8.03 | 2.20 | 10.22 |
| Myeloid | ELANE | 11.40 | 8.26 | 19.66 |
| Myeloid | AZU1 | 7.36 | 6.93 | 14.29 |
| Myeloid | LYZ | 14.14 | 5.87 | 20.01 |
| Myeloid | CSF1R | 12.58 | 7.42 | 20.00 |
| Baso/Eo/Mast | CPA3 | 13.11 | 2.34 | 15.45 |
| Baso/Eo/Mast | GATA2 | 7.08 | 1.15 | 8.23 |
| pDC | IRF8 | 2.15 | 3.65 | 5.80 |
| pDC | TCF4 | 5.55 | 3.38 | 8.93 |

## 3. Method 간 timing 일치도 (shared fit gene)

- floor ∩ MultiVelo shared fit gene: **368**
- Spearman(floor fit_t_, MultiVelo fit_t_sw2) = **0.074** (p=0.16) — RNA 유도 timing 일치도(sanity)
  - Spearman(fit_alpha) = 0.816
  - Spearman(fit_beta) = -0.079
  - Spearman(fit_gamma) = 0.419

## 4. 한계 · 다음 (DESIGN §4)
- ⚠️ switch time은 *전역* fit → 진짜 within-lineage 일치도는 per-lineage fit 필요(추후).
- ⚠️ H1(agreement gene의 bootstrap lag-sign stability)·다중 chromatin-aware method 일치도는 **MultiVeloVAE/MoFlow arm 추가 후** (현재 chromatin-aware=MultiVelo 단독).
- sign-agreement vs rank-corr 분리 보고 원칙: method가 2+ chromatin-aware일 때 적용.
