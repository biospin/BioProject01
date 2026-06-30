# FINDINGS — HSPC velocity 벤치마크 결과·해석 종합

> **이 문서가 결과+해석의 canonical 종합본이다.** 개별 분석 md(`concordance.md`, `h1_lag_diagnostic.md`,
> `scrambled_null.md`, `confound.md`, `cellcycle_genelevel.md`, `lineage_lag.md`)는 상세 근거이고,
> 여기서는 그것들을 연구 질문에 맞춰 한 줄 결과+해석으로 묶고 통합 결론을 낸다.
> 새 분석이 끝날 때마다 갱신. 진행 상태는 `../PROGRESS-LIVE.md`, 현황은 `../../../HANDOFF.md`.
> 최종 갱신: **2026-06-30**.

## 연구 질문 (목표)
gene별 **chromatin→transcription lag**(activation/shutdown 시점차)을 정량해서, baseline epigenomic
feature로 **epigenetic drug response timing**을 예측한다. 1차 데이터셋 = Human HSPC 10x Multiome
(GSE209878, day0+day7 통합 21,878 cell). 그 전제로 **velocity method head-to-head 벤치마크**를 돌려
"lag이 method-robust한 양인가"(H1)를 먼저 검정한다.

## 분석 현황
| 분석 | 상태 | 산출 |
|---|---|---|
| 3-way H1 (multivelo×moflow×multivelovae lag 일치도) | ✅ | `concordance.md` §1.5/§3.5/§3.6 |
| H1 lag 무상관 진단 (정의 정합성) | ✅ | `h1_lag_diagnostic.md` |
| scrambled-chromatin 음성대조 | ✅ | `scrambled_null.md` |
| confound (cell-cycle/burst/ambient) | ✅ | `confound.md` + `cellcycle_genelevel.md` |
| within-lineage lag 분포 | ✅ | `lineage_lag.md` |
| **4-way H1** (+CRAK-Velo) | 🔄 진행 중 | (cisTopic→fit→lag) |
| permutation FDR (P4) | ⬜ 대기 | — |
| α_c bootstrap stability / per-lineage refit | ⬜ 대기 | — |
| P5 drug-timing lag 모델 | ⬜ 대기 | — |

---

## ★ 통합 결론 (현재까지)
**chromatin→transcription lag은 gene 수준에서 method-robust한 양이 아니다.** 크기·방향 모두 method 간
일치하지 않으며(H1 실패), 음성대조는 한 method(MultiVelo)의 lag이 chromatin 신호가 아니라 모델 구조에서
나옴을 보였다. **robust한 것은 (a) 전사율 α(method 간 ρ=0.88), (b) 집단 수준 방향 균형(~50/50, 두 method 수렴)뿐.**
→ drug-timing 모델은 lag을 단일 method 값으로 쓰면 안 되고, **method 불확실성을 명시적으로 반영**해야 한다.

---

## 발견별 결과·해석

### 1. H1 — cross-method lag 일치도: **약함/실패**
- **lag 크기 무상관**: pairwise Spearman multivelo×moflow **−0.04**(p=0.38), multivelo×multivelovae **−0.01**(p=0.81),
  moflow×multivelovae **+0.08**(p=0.04). 정의를 apples-to-apples로 통일해도 **+0.12**에 그침(`h1_lag_diagnostic`).
- **방향 ~50/50**: sign-가변 method 모두 chromatin-leads 비율 MoFlow **44.8%** / MultiVeloVAE **49.3%** → 전역
  'chromatin이 transcription을 prime한다' **데이터 미지지**. (MultiVelo 100%는 switch-time 단조정렬 모델 제약 아티팩트.)
- **gene 수준 방향 불일치**: moflow×multivelovae sign-agreement **48%**(우연).
- **근원 진단**: lag을 결정하는 **chromatin opening rate α_c가 method-민감**(ρ=0.29)인 반면 전사율 α는 강건(ρ=0.88).
  → lag이 α_c의 method 민감성을 그대로 상속.
> 해석: "어느 gene이 chromatin 선행인지"는 method를 바꾸면 달라진다(비robust). 단 집단 수준 방향 균형은 두 독립 method가 수렴(robust).

### 2. 음성대조 — chromatin은 MultiVelo lag을 구동하지 않음
- ATAC를 within-lineage 셔플(chromatin↔RNA 결합 파괴) 후 재fit → lag 분포 원본과 **통계적으로 동일**
  (Mann–Whitney p=0.20, KS p=0.51), per-gene lag **ρ=0.72** 보존, chromatin likelihood 0.239→0.237(불변).
- 단 Wilcoxon paired p=0.0003 (median 5.87→5.48 소폭 감소) = chromatin의 **marginal 기여**만.
> 해석: MultiVelo lag은 chromatin 신호가 아니라 **모델 구조(switch-time 순서)·gene 고유 RNA 동역학**에서 나온다.
> §1의 'MultiVelo 100% chromatin-leads = 아티팩트' 결론을 음성대조로 독립 확증.

### 3. Confound — lag 결론 비편향
- **cell-cycle**: 세포 수준 ρ≈0.33–0.36(S/G2M score vs expr)이지만 **gene 수준은 비편향** — fit lag gene 중
  CC gene 1.9%(10개), CC lag vs 나머지 Mann-Whitney p=0.86, CC 제외 시 median 변화 0.037. 세포-수준 ρ의 정체는
  **cycling이 lineage와 강결합**(MK 88%↔HSC 3%)이라 within-lineage 분석이 이미 통제. → **global regress_out 미수행**(분화신호 제거 위험).
- **burst**: lag↔α Spearman −0.24(중간, |ρ|<0.5 → 허용; regularized 회귀 시 반영).
- **ambient/doublet**: scrublet 적용, doublet median 0.045, pct_mito median 10.4%(QC max 20%) — 정상.

### 4. Within-lineage lag 분포 (참고, 전역 fit 기반)
- MultiVelo lag median은 lineage별 4.3–7.4 pseudotime(Erythroid 최저, Lymphoid 최고). 전부 100%>0(§1 구조 caveat).
- ⚠️ 전역 fit을 dominant-expression으로 귀속한 근사 — **진짜 within-lineage 일치도는 per-lineage refit 필요**(대기).
- rare lineage(MK/Baso·Eo·Mast/pDC) uncertainty 별도.

---

## drug-timing 목표(P5)와의 연결
- **쓸 수 있는 robust 신호**: 전사율 α(method 간 ρ=0.88), 집단 수준 방향 균형.
- **그대로 쓰면 안 되는 것**: gene별 lag 크기·방향(method 민감). baseline feature로 넣으려면 method 불확실성을
  uncertainty로 모델에 반영하거나, α_c 추정 안정화(bootstrap/per-lineage) 후 사용.
- 4-way H1(CRAK-Velo 추가) + permutation FDR로 이 결론의 견고성을 마저 검정 중.

## 핵심 한계
1. **Pseudotime ≠ wall-clock**: day0/day7 batch 통합 → lag은 pseudotime 단위. wall-clock anchor 불가(H2 강등).
2. lag 정의가 method마다 다름(switch-timing vs rate-timescale vs DTW) → 비교는 rank·sign 분리 보고.
3. 전역 fit 기반(per-lineage refit 미완). bootstrap stability 미완.
4. 음성대조는 MultiVelo 단일 method(DTW-lag·CRAK-Velo scramble은 후속).
