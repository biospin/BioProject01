# P3 — Within-lineage lag 분포 (MultiVelo, 전역 fit 기반)

- fit gene 538, RNA에서 찾은 gene 538

## Lineage별 lag 요약 (전역 fit, gene dominant-expression 귀속)

| lineage | n_gene | median_lag | mean_lag | IQR_low | IQR_high | lag>0% |
|---|---|---|---|---|---|---|
| Baso/Eo/Mast ⚠️rare | 62 | 5.18 | 5.99 | 2.09 | 8.90 | 100.0% |
| Erythroid | 52 | 4.29 | 5.74 | 2.08 | 7.66 | 100.0% |
| HSC/MPP | 177 | 5.97 | 6.24 | 3.22 | 9.23 | 100.0% |
| Lymphoid | 48 | 7.43 | 6.94 | 2.47 | 9.46 | 100.0% |
| MK ⚠️rare | 137 | 5.87 | 6.42 | 3.36 | 8.47 | 100.0% |
| Myeloid | 62 | 6.68 | 6.39 | 3.32 | 9.02 | 100.0% |

> ⚠️ switch time은 전역 fit — lineage별 귀속은 dominant expression 기준이며 per-lineage fit이 아님.
> rare lineage(MK/Baso·Eo·Mast/pDC)는 uncertainty 별도 보고 필요(DESIGN §4, CLAUDE.md #2).

## scVelo floor fit_t_ lineage별 요약

| lineage | n_gene | median_fit_t |
|---|---|---|
| Baso/Eo/Mast | 75 | 5.94 |
| Erythroid | 38 | 6.29 |
| HSC/MPP | 128 | 7.45 |
| Lymphoid | 69 | 8.56 |
| MK | 120 | 6.57 |
| Myeloid | 57 | 6.52 |
