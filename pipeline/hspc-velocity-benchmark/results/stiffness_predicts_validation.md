# 목적함수 곡률(내부 식별성)이 외부 측정-검증을 예측한다 — velocity rate 신뢰의 제1원리 기준

> make-or-break A (2026-07-18). profile-likelihood 강성을 α·α_c·β·γ 전 rate로 확장(`scripts/p5_stiffness_all_params.py`,
> `p3_profile_likelihood`의 목적함수·latent-time 재최적화 재사용) → 내부 식별성 랭킹이 외부 측정 ground truth와 일치하는지 검정.
> 산출: `results/stiffness_all_params.csv` (538 gene 중 n=506 유효 곡률).

## 결과 — 강성 랭킹 (median per-cell κ, 높을수록 stiff=식별 가능)
| rate | κ/cell median | frac>0 | 외부 측정-검증 (`external_rate_validation.md`) |
|---|---|---|---|
| **α** 전사율 | **+7.98** | 94.5% | ✅ **실측 TT-seq 합성율 회복** (non-HK ρ +0.24~+0.29, 3 method CI 0 배제) |
| α_c 개방속도 | +7.32 | 97.4% | (직접 측정 없음 — lag 통해 fragile) |
| β splicing | +4.86 | 84.8% | (직접 측정 없음) |
| **γ** 분해율 | **+1.72** | 90.7% | ❌ **역방향** (MOLM13 ρ(γ,k_deg) −0.224, CI 0 배제; 어느 method도 미회복) |

## 짝지은 통계 (per-gene, n=506) — 랭킹 견고
- **α > γ: median Δ=+4.94, 78.1% gene, Wilcoxon p=1.35e-39**. α/γ 강성비 median **3.4배**.
- α > β 67.2% (p=1.7e-18) · β > γ 61.5% (p=5.1e-12) · α_c > γ 73.3% (p=1.1e-30). **전 pairwise p<1e-11**.
- per-gene: γ가 4개 중 최저 sloppy인 비율 **49.4%**, α가 최고 stiff 36.6%(α·α_c 근접해 상위 교대).

## 판정 — **식별성 랭킹 = 측정검증 랭킹** (곡률이 신뢰를 예측)
목적함수 곡률만으로(외부 데이터 없이) 산출한 강성 순서 **α ≫ α_c > β > γ** 에서, **외부 실측 ground truth가 있는 두 극단이 순서대로 검증**된다:
- **최고 stiff α** → 실측 합성율을 회복(measurement-real).
- **최저 sloppy γ** → 실측 분해율에 대해 **역방향**(measurement-anti).

즉 **MultiVelo 목적함수의 기하가, 어느 velocity 출력이 측정으로 신뢰 가능한지를 *사전에* 말해준다.** 이는 순수 cross-method 재현성(내부)이나 외부검증(단독)을 넘어, **둘을 잇는 제1원리 신뢰 기준**이다 — 논문의 양성 헤드라인 자산.

## 정직한 한계
- 직접 외부 측정이 있는 rate는 **α(합성)·γ(분해) 둘뿐**. α_c·β는 내부 랭킹을 채우나 외부검증은 미확인(측정 데이터 부재). 따라서 "곡률→검증"은 **양 극단에서 확증**, 중간 2개는 a priori 순서 제공.
- MultiVelo 단일 method의 우도 기하. 단 α는 method 간 robust(ρ=0.88)라 α-강성은 method-견고.
- freed-nuisance에서 α 곡률이 0.19×로 축소되나(fixed 상한), 랭킹(α≫γ)은 보수적 기준에서도 유지.
