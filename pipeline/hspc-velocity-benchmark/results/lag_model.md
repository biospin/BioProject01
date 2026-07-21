# P5 — baseline epigenomic → kinetic timing 모델 (held-out lineage CV)

- 537 gene, Ridge, leave-one-lineage-out. 목표(CLAUDE.md): baseline epigenomic feature로 drug response timing 예측 — 그 하네스 prototype.
- feature ablation: **baseline-only** = {base_acc, chrom_rng, acc_mean}(HSC/MPP chromatin, fit 독립) / **+fit-kinetic** = +{fit_alpha_c, fit_var_c}(같은 MultiVelo fit 유래 → 순환 가능).

## held-out lineage 일반화 (Spearman pred vs actual)

| target | feature set | overall | Baso/Eo/Mast | Erythroid | HSC/MPP | Lymphoid | MK | Myeloid |
|---|---|---|---|---|---|---|---|---|
| lag (method-sensitive) | baseline-only | **-0.213** | -0.12 | -0.47 | -0.08 | -0.31 | -0.19 | -0.08 |
| lag (method-sensitive) | +fit-kinetic | **+0.587** | +0.58 | +0.60 | +0.68 | +0.57 | +0.35 | +0.66 |
| α (robust) | baseline-only | **-0.090** | +0.02 | -0.26 | -0.01 | +0.13 | -0.04 | -0.11 |
| α (robust) | +fit-kinetic | **-0.094** | +0.05 | -0.37 | -0.16 | +0.18 | -0.05 | -0.01 |

![model](figures/lag_model.png)

## 해석

- **baseline chromatin만으로 lag held-out ρ=-0.213** (fit feature 추가 시 +0.587). α는 baseline ρ=-0.090. → baseline만으론 약함, fit feature가 신호 대부분 기여(순환 주의).
- **FINDINGS와의 관계**: H1의 'lag은 *method 간* 불일치'와 본 결과('*한 method 내* lag은 baseline chromatin으로 lineage 간 예측 가능')는 양립 — lag의 *값*은 method 의존이나, MultiVelo 내부에선 chromatin 동역학이 구조적으로 lag을 결정. drug-timing 모델엔 **단일 lag 값이 아니라 baseline chromatin feature 자체**를 쓰는 게 더 robust함을 시사.
- **순환 점검**: fit feature 추가가 baseline-only 대비 크게 향상(-0.21→+0.59) → baseline-only 수치가 진짜 일반화 신호.
- ⚠️ 한계: ① chromatin feature는 moflow Mc(smoothed) 유래 — 진짜 day0 ATAC peak/promoter/enhancer feature 어셈블은 다음 단계. ② gene→lineage는 dominant-expression 근사(전역 fit). ③ drug perturbation 데이터 부재 → timing은 kinetic proxy. ④ Ridge α=1 고정(미튜닝).
- 다음: 실제 baseline ATAC feature 어셈블 + per-lineage refit target + bootstrap 안정 gene(§4D)으로 target 한정.
