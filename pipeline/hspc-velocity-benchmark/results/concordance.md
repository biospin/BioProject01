# P3 — Concordance & construct-validity

- **multivelo**: fit gene 538
- **moflow**: fit gene 636
- **crakvelo**: fit gene 868
- **multivelovae**: fit gene 641
- **scvelo_floor**: fit gene 487

## 1. MultiVelo lag (fit_t_sw2 − fit_t_sw1, pseudotime)
- n=538, median **5.87**, mean 6.29, IQR [3.03, 9.00]
- lag>0 비율 100.0%
- ⚠️ **구조적 caveat**: MultiVelo 4-state는 switch time을 **단조 정렬**(t_sw1<t_sw2<t_sw3)하므로 `sw2−sw1`은 *정의상 항상 양수*다. 따라서 100%는 priming 증거가 아니라 모델 제약 — **sign은 무정보, lag *크기*의 gene간 변이만 정보**다. 진짜 directional sign check는 sign이 가변인 method(MoFlow DTW c-s lag 등)에서 수행해야 함(DESIGN §4B).

## 1.5 Directional lag (sign-가변 method) — chromatin 선행 여부
> MultiVelo와 달리 sign이 구조 제약 없는 method만 방향을 답할 수 있다(DESIGN §4B).

- **moflow** (n=636): median +0.000, chromatin-leads(>0) **44.8%** / rna-leads(<0) 43.2% | Wilcoxon p=0.0309 → 방향 편향 미미(median≈0)
- **crakvelo** (n=868): median +0.000, chromatin-leads(>0) **41.1%** / rna-leads(<0) 43.3% | Wilcoxon p=0.0171 → 방향 편향 미미(median≈0)
- **multivelovae** (n=641): median -0.002, chromatin-leads(>0) **49.3%** / rna-leads(<0) 50.7% | Wilcoxon p=7.68e-06 → 방향 편향 미미(median≈0)
> ~50/50면 전역 'chromatin이 transcription을 prime한다'는 데이터 미지지 (MultiVelo의 100%는 §1 모델 제약 아티팩트).

## 2. Construct-validity — marker gene lag (크기)

> sign은 §1 caveat대로 구조적 양수 → 여기선 **lag 크기**(gene간 변이)를 본다.

| lineage | gene | lag(sw2-sw1) | sw1 | sw2 |
|---|---|---|---|---|
| HSC/MPP | HLF | 3.05 | 8.67 | 11.73 |
| HSC/MPP | CRHBP | 11.20 | 8.83 | 20.03 |
| HSC/MPP | MEIS1 | 3.76 | 3.02 | 6.77 |
| Erythroid | TFRC | 8.46 | 11.54 | 20.00 |
| MK | ITGA2B | 4.49 | 6.62 | 11.11 |
| MK | VWF | 4.28 | 9.38 | 13.66 |
| Myeloid | MPO | 7.88 | 2.17 | 10.05 |
| Myeloid | ELANE | 12.06 | 7.66 | 19.72 |
| Myeloid | AZU1 | 7.24 | 6.86 | 14.10 |
| Myeloid | LYZ | 14.10 | 5.91 | 20.00 |
| Myeloid | CSF1R | 12.93 | 7.08 | 20.01 |
| Baso/Eo/Mast | CPA3 | 10.21 | 2.73 | 12.94 |
| Baso/Eo/Mast | GATA2 | 7.02 | 0.99 | 8.02 |
| pDC | IRF8 | 2.09 | 3.59 | 5.68 |
| pDC | TCF4 | 6.70 | 3.47 | 10.18 |

## 3. Method 간 timing 일치도 (shared fit gene)

- floor ∩ MultiVelo shared fit gene: **368**
- Spearman(floor fit_t_, MultiVelo fit_t_sw2) = **0.038** (p=0.47) — RNA 유도 timing 일치도(sanity)
  - Spearman(fit_alpha) = 0.818
  - Spearman(fit_beta) = -0.011
  - Spearman(fit_gamma) = 0.401

## 3.5 Chromatin-aware lag 일치도 (H1, DESIGN §4B)

> ✅ **CRAK-Velo lag 부호 검증·수정 완료(2026-07-01, `crakvelo_sign_check.md`)**: `dtw_lag`이 MoFlow와 반대 부호(버그)였음 → `i−j`로 통일(양수=chromatin선행), 단위·marker 검증. 아래 crakvelo 관련 수치는 **수정 후** 값.

- lag 산출 method: ['multivelo', 'moflow', 'crakvelo', 'multivelovae']
- **multivelo×moflow** (shared 537): Spearman(rank) **-0.038** (p=0.38) | sign-agreement 생략(한쪽 sign 구조적)
- **multivelo×crakvelo** (shared 287): Spearman(rank) **0.003** (p=0.96) | sign-agreement 생략(한쪽 sign 구조적)
- **multivelo×multivelovae** (shared 538): Spearman(rank) **-0.010** (p=0.81) | sign-agreement 생략(한쪽 sign 구조적)
- **moflow×crakvelo** (shared 330): Spearman(rank) **-0.151** (p=0.006) | sign-agreement **32.4%**
- **moflow×multivelovae** (shared 636): Spearman(rank) **0.083** (p=0.036) | sign-agreement **48.1%**
- **crakvelo×multivelovae** (shared 334): Spearman(rank) **-0.040** (p=0.47) | sign-agreement **38.6%**
> rank-corr와 sign-agreement는 분리 보고(병합 금지, DESIGN §4B).

## 3.6 진단 — per-rate 일치 + apples-to-apples lag

- **multivelo×multivelovae** (shared 538) — 같은 정의로 통일 비교:
  - Spearman(alpha_c) = +0.291 (p=5.7e-12) ⚠️
  - Spearman(alpha) = +0.882 (p=1e-177)
  - Spearman(beta) = +0.080 (p=0.064)
  - Spearman(gamma) = -0.109 (p=0.012)
  - **rate-proxy lag(1/α_c−1/α) 통일**: Spearman +0.124 (p=0.0039) | sign-agreement 49.8%
> α는 강건하나 lag을 결정하는 α_c가 method-민감 → lag 불일치의 근원. 상세 `h1_lag_diagnostic.md`.

## 4. 한계 · 다음 (DESIGN §4)
- ⚠️ switch time은 *전역* fit → 진짜 within-lineage 일치도는 per-lineage fit 필요(추후).
- ⚠️ H1 bootstrap lag-sign stability는 반복 fit 필요(GPU에서 DL arm 반복 시).
- MoFlow c-s lag은 sign 가변 → construct-validity directional check의 1차 대상.
