# 식별가능성 vs SNR 분리 검정 (2026-07-12)

> **목적**: §8의 profile-likelihood 곡률(식별가능성)이 cross-method 재현성을 예측하는 것이, 단순 SNR/depth를 **넘어서는지** 검정. paper 전략(식별가능성 "법칙" 격상)의 make-or-break.
> 스크립트 `scripts/p3_identifiability_vs_snr.py` · 출력 `results/identifiability_vs_snr_output.txt`. 재계산 아님 — 기존 §8 per-gene 곡률(`profile_likelihood_identifiability.csv`) + P2 method별 추정(multivelo/moflow/mvvae) 병합.

## 방법
- N=537 유전자(4-method 공통). per-gene cross-method 불일치 = |rank_A − rank_B| (0=완전일치, 1=완전불일치). lag=MultiVelo(t_sw2−sw1) vs MoFlow(cs_lag); α=MultiVelo vs MVVAE.
- SNR 프록시 = `nkeep`(profile-likelihood admissible point 수 = depth/support, 곡률 크기와 독립적 측면).
- 검정: 곡률 κ_lag → lag 불일치 Spearman, 그리고 nkeep 통제 편상관.

## 결과
| 측정 | 값 |
|---|---|
| 재현성 격차(per-gene) | lag 불일치 median **0.317** vs α **0.078** (α ~4배 재현) |
| ρ(κ_lag, lag 불일치) | **−0.144** (p=0.012) — 방향 맞으나 **약함** |
| nkeep 통제 편상관 | **−0.069** (절반↓, 비유의) |
| ρ(nkeep, lag 불일치) | −0.153 (depth 단독이 곡률만큼 예측) |
| ρ(κ_lag, nkeep) | **+0.576** (곡률↔depth 강한 공선성) |

## 결론 (정직)
**강한 "식별가능성이 SNR을 넘어 재현성을 예측한다" 주장은 이 데이터로 방어 불가.**
- 곡률→재현성 신호가 ① 애초에 약하고(ρ=−0.14) ② 대부분 depth/SNR로 설명(통제 후 −0.07, 공선성 0.58).
- 즉 여기서 "sloppy"는 사실상 "저SNR/저depth". 리뷰어의 "곡률=그냥 SNR" 공격이 성립.

## 함의 (paper 전략)
- ❌ 사전등록 불가: "곡률이 SNR 넘어 재현성 예측"(discovery급 법칙 레버) → 폐기.
- ✅ 유지: (1) 재현성 격차(α robust/lag fragile, per-gene도 확인), (2) 2층 구분(within-method fit ≠ cross-method 신뢰), (3) 신뢰 결정지도.
- 메커니즘은 **정직하게**: lag는 두 switch-time의 **차이라 구조적 저SNR + sloppy(둘이 얽혀 분리 불가)**. 식별가능성이 SNR을 초월한다고 과주장 안 함. §8 상한(fixed 3.53×/94.57%)·기준(freed 2.49×/77%) 안에서 서술.
- **사후 구제 금지 원칙**(BIOP02 템플릿): 이 NULL을 NULL로 보고.
