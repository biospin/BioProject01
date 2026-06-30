# P3 — per-lineage refit lag 일치도 (진짜 within-lineage H1)

> p2_multivelo_perlineage.py: 각 terminal lineage를 root(HSC/MPP)∪L 세포로 **따로 fit**.
> lineage_lag.md(전역 fit + dominant-귀속)을 진짜 per-lineage fit으로 대체.
> MultiVelo lag = fit_t_sw2−fit_t_sw1; sign은 구조적(항상 양수)이라 magnitude rank만 평가.

## A. lineage별 lag 분포 (per-lineage refit)

| lineage | n_gene | median_lag | mean_lag | IQR_low | IQR_high | median_α_c |
|---|---|---|---|---|---|---|
| Baso-Eo-Mast ⚠️rare | 476 | 6.85 | 7.93 | 3.98 | 10.26 | 0.036 |
| Erythroid | 487 | 7.21 | 7.80 | 4.22 | 9.59 | 0.035 |
| Lymphoid | 446 | 7.02 | 8.21 | 4.45 | 10.83 | 0.038 |
| MK ⚠️rare | 470 | 7.23 | 7.97 | 4.89 | 10.15 | 0.033 |
| Myeloid | 484 | 6.47 | 6.80 | 3.46 | 9.40 | 0.040 |

## B. cross-lineage lag magnitude 일치도 (Spearman rank)

> 같은 gene의 lag이 분화경로(lineage)와 무관하게 robust한가? = gene-intrinsic 검정.

| lineage A | lineage B | n_shared | Spearman ρ | p |
|---|---|---|---|---|
| Baso-Eo-Mast | Erythroid | 464 | 0.346 | 1.6e-14 |
| Baso-Eo-Mast | Lymphoid | 438 | 0.298 | 1.9e-10 |
| Baso-Eo-Mast | MK | 454 | 0.381 | 3.8e-17 |
| Baso-Eo-Mast | Myeloid | 455 | 0.234 | 4.6e-07 |
| Erythroid | Lymphoid | 436 | 0.352 | 3.8e-14 |
| Erythroid | MK | 462 | 0.513 | 2e-32 |
| Erythroid | Myeloid | 460 | 0.353 | 5.9e-15 |
| Lymphoid | MK | 435 | 0.362 | 7e-15 |
| Lymphoid | Myeloid | 432 | 0.334 | 9.9e-13 |
| MK | Myeloid | 452 | 0.248 | 9.2e-08 |

- **요약**: 쌍별 ρ median=0.349, range [0.234, 0.513], 양수 쌍 10/10.

## D. α_c cross-lineage 일치도 (대조군: H1에서 α 계열은 robust)

| lineage A | lineage B | n_shared | Spearman ρ | p |
|---|---|---|---|---|
| Baso-Eo-Mast | Erythroid | 464 | 0.497 | 2.2e-30 |
| Baso-Eo-Mast | Lymphoid | 438 | 0.406 | 8.8e-19 |
| Baso-Eo-Mast | MK | 454 | 0.524 | 2.5e-33 |
| Baso-Eo-Mast | Myeloid | 455 | 0.403 | 3.1e-19 |
| Erythroid | Lymphoid | 436 | 0.507 | 7.1e-30 |
| Erythroid | MK | 462 | 0.684 | 4.4e-65 |
| Erythroid | Myeloid | 460 | 0.467 | 2.5e-26 |
| Lymphoid | MK | 435 | 0.525 | 3.7e-32 |
| Lymphoid | Myeloid | 432 | 0.468 | 6.3e-25 |
| MK | Myeloid | 452 | 0.406 | 2.2e-19 |

- **요약**: α_c 쌍별 ρ median=0.483 (lag 0.349와 비교 — α_c가 더 robust하면 H1 패턴 재현).

## C. per-lineage refit vs 전역 fit lag (Spearman)

> per-lineage fit이 전역 fit과 얼마나 다른가? (낮으면 전역 fit이 lineage 신호를 뭉갬)

| lineage | n_shared | Spearman ρ | p |
|---|---|---|---|
| Baso-Eo-Mast | 469 | 0.306 | 1.2e-11 |
| Erythroid | 478 | 0.299 | 2.4e-11 |
| Lymphoid | 436 | 0.259 | 4.2e-08 |
| MK | 465 | 0.233 | 3.6e-07 |
| Myeloid | 480 | 0.460 | 1.7e-26 |

## 결론

- cross-lineage lag magnitude ρ median = **0.349** → **lag cross-lineage 일치도 약함(경계)**.
- 전역 3-way H1(cross-method lag 무상관)에 더해, within-method cross-lineage 축에서도 lag 일치도를 평가 → H1(lag 비robust) 강건성 검정.
