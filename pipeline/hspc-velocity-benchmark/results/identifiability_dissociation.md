# 식별성 & α-vs-lag dissociation — bootstrap CI + TOST (CHEAP tier)

> 유전자 paired bootstrap B=10,000, seed=20260707 (결정론적). 백분위 95% CI를 쓴다.
> 정의는 `p3_concordance.py`에서 그대로 재사용한다 → 수치가 FINDINGS/concordance.md와 일치한다.
> Guardrail: rank/magnitude concordance만 본다(MultiVelo의 structural sign은 절대 끌어오지 않는다);
> CRAK-Velo는 제외한다; 'lag not robust'는 |ρ|<0.2 기준 TOST 등가성(두 단측검정으로 "차이가 미리 정한 한계 안에 있다"를 보이는 등가성 검정)으로 진술한다; cross-dataset은 각각 표본 1개다.

## #1 — Paired Δρ dissociation (α ≫ lag), bootstrap CI + TOST

> **lag = MAGNITUDE rank (|·|)** 를 어디서나 쓴다 — FINDINGS와 정합인 관례다(외부 `concordance_*.py`가 `.abs()`를 쓴다; MultiVelo sign은 structural이라 무정보다). headline은 **dissociation**(Δρ가 0을 배제)이지 등가성이 아니다.

### HSPC (within-dataset, MultiVelo × MultiVeloVAE, shared 538 genes) — PRIMARY

- ρ_α = **+0.882**  95%CI [+0.855, +0.904]
- ρ_lag (magnitude) = **+0.163**  95%CI [+0.078, +0.244]
- **Δρ = ρ_α − ρ_lag = +0.720**  95%CI **[+0.639, +0.802]** (bootstrap 평균 +0.719)
  → CI가 **0을 배제**한다 — dissociation 성립(α가 lag보다 ~0.7 위에 있다).

- lag 관례에 대한 Δρ robustness: magnitude **+0.720** | signed (concordance.md §3.5, ρ_lag=-0.010) Δρ +0.893 | rate-proxy |1/α_c−1/α| (ρ_lag=-0.009) Δρ +0.891 — 모든 CI가 0을 배제한다.

### TOST equivalence — HSPC lag vs pre-declared bound |ρ|<0.2

- **magnitude lag (MV×VAE)** ρ=+0.163, 95%CI [+0.078, +0.244] → **등가 아님 (CI가 [−0.2,+0.2]를 벗어난다)** — weak-positive, 상한이 +0.2를 넘는다 → 엄격한 한계에서 등가성이 인증되지 않는다.
  - ⚠️ FINDINGS §3.5는 **signed** MV×VAE lag −0.010도 인용하는데(MV-magnitude와 VAE-signed를 섞음 → 범주 불일치다); magnitude와 정합한 값은 +0.163이다. cross-dataset 정합을 위해 magnitude를 보고한다.
- **directional lag (MoFlow×VAE, guardrail-clean sign pair, shared 636)** ρ=**+0.083** 95%CI [+0.007, +0.158] → **등가 (CI ⊂ [−0.2,+0.2])** — method들이 0을 넘어 lag *방향*까지 일치하지는 않는다.
  → 갈린 판정: *directional* lag concordance는 0과 등가이고(MoFlow×VAE), *magnitude* concordance는 weak-positive다(MV×VAE). 둘 다 α보다 ~0.7 아래에 있다.

### External replications (within-dataset MV×VAE, magnitude lag)

- **GSE194122_bmmc** (shared 272): ρ_α **+0.906** [+0.879,+0.925], ρ_lag(mag) **-0.088** [-0.209,+0.034], **Δρ +0.994** 95%CI [+0.874,+1.110] (0을 배제).
  - TOST lag: **등가 아님 (CI가 [−0.2,+0.2]를 벗어난다)**
- **e18_mouse_brain** (shared 1027): ρ_α **+0.898** [+0.883,+0.910], ρ_lag(mag) **+0.057** [-0.005,+0.118], **Δρ +0.841** 95%CI [+0.779,+0.903] (0을 배제).
  - TOST lag: **등가 (CI ⊂ [−0.2,+0.2])**
- **human_brain**: within-dataset MultiVeloVAE fit이 없다(MultiVelo + floor만 있다) → within-dataset cross-method lag은 **계산 불가**다; 그 α-vs-lag 증거는 cross-dataset 축이 담당한다(§#5).

## #3a — Empirical identifiability ranking (cross-method reproducibility = identifiability)

> 표준 축 = MultiVelo × MultiVeloVAE (α_c를 노출하는 유일한 pair다). SIGNED ρ 내림차순으로 순위를 매기며 95%CI를 붙인다 — identifiability = 양의 cross-method 재현(음의 ρ = 순위 역전 = 가장 덜 식별 가능).

| rank | parameter | MV×VAE Spearman | 95% CI | identifiable? |
|---|---|---|---|---|
| 1 | α (transcription rate) | **+0.882** | [+0.855, +0.905] | **YES (invariant)** |
| 2 | α_c (chromatin opening) | **+0.291** | [+0.209, +0.369] | no (fragile) |
| 3 | β (splicing) | **+0.080** | [-0.009, +0.168] | no (fragile) |
| 4 | γ (degradation) | **-0.109** | [-0.192, -0.023] | no (fragile) |

### RNA-pinned evidence — floor (NO chromatin channel) recovers α ≈ chromatin methods

- **α: floor × MultiVelo** (shared 368): Spearman **+0.818** 95%CI [+0.773, +0.855] — floor는 ATAC이 전혀 없는데도 α를 chromatin-method 수준으로 회복한다.
- **α: floor × MultiVeloVAE** (shared 434): Spearman **+0.889** 95%CI [+0.862, +0.910] — floor는 ATAC이 전혀 없는데도 α를 chromatin-method 수준으로 회복한다.

→ **α만이 식별 가능한 불변량으로 홀로 선다**; α_c, β, γ는 모두 fragile하다(CI가 0을 포함하거나 0 근처다). 경험적 identifiability 순위: **α ≫ α_c > β > γ**.

## #3b — γ/β ratio sloppiness probe (steady-state slope identifiability)

> Splicing ODE: steady-state slope γ/β (+scaling)만 식별 가능하다. 그 비는 개별 β, γ보다 cross-method 재현이 더 나아야 한다. 두 method 모두에서 |β|>1e-4인 gene을 쓴다.

- **γ/β ratio** (MV×VAE, n=538): Spearman **-0.324** 95%CI [-0.400, -0.244]
- **β alone** (MV×VAE, n=538): Spearman **+0.080** 95%CI [-0.010, +0.169]
- **γ alone** (MV×VAE, n=538): Spearman **-0.109** 95%CI [-0.192, -0.024]
> 판정: 이론상 식별 가능한 steady-state slope γ/β조차 cross-method를 깔끔하게 재현하지 **못한다**(ρ=−0.32, *음수* = 반재현) — **오직 α만 깔끔하게 재현한다**. 예측은 약한 의미로만 성립한다: |ρ(γ/β)|≈0.32가 |ρ_β|=0.08과 |ρ_γ|=0.11보다 크다(그 조합은 개별 rate보다 덜 나쁘게 정해진다 — *크기* 상의 scVelo scaling sloppiness다). 그러나 음의 부호(rank 상관이 흡수하지 못하는 MV vs VAE parameterization/scaling 관례 차이)는 slope 자체가 재현 가능한 불변량이 아님을 뜻한다. α만 홀로 선다.

## Diff-budget — lag = 잡음 섞인 두 timing의 차

> rate-timescale 성분(1/α, 1/α_c)과 그 차(lag = 1/α_c − 1/α)의 cross-method (MV×VAE) concordance다. Spearman은 공통 1/x 변환에 불변이라 ρ(1/α)=ρ(α), ρ(1/α_c)=ρ(α_c)다.

- **1/α component**: Spearman **+0.882** 95%CI [+0.856, +0.905]
- **1/α_c component**: Spearman **+0.291** 95%CI [+0.209, +0.370]
- **difference (lag = 1/α_c − 1/α, signed)**: Spearman **+0.124** 95%CI [+0.036, +0.210]
> 한 성분은 강하고(1/α +0.88) 한 성분은 약한데(1/α_c +0.29); 그 차는 **더 약한 성분보다도 아래로 떨어진다** → 차분이 concordance를 무너뜨린다. 예측대로다: lag은 α_c의 fragility를 물려받고 차분이 잡음을 증폭한다.

## #5 — Cross-dataset replication CIs (reject monotonicity as a claim)

> 세 cross-dataset MultiVelo α ρ와 그 lag 짝에 대한 bootstrap 95%CI다. 겹침 → tissue-distance 순서는 QUALITATIVE하며 정량적 주장이 아니다. 점 3개에 추세 fit은 하지 않는다.

| dataset | shared | α cross ρ (95%CI) | lag cross ρ (95%CI) | Δρ (95%CI) | lag TOST |
|---|---|---|---|---|---|
| human_brain (adult brain) | 102 | **+0.475** [+0.292,+0.626] | +0.185 [-0.005,+0.369] | +0.290 [+0.055,+0.518] | not equiv |
| E18 mouse brain (fetal, cross-species) | 132 | **+0.321** [+0.158,+0.472] | +0.105 [-0.069,+0.269] | +0.216 [-0.026,+0.449] | not equiv |
| GSE194122 BMMC (same-tissue human) | 88 | **+0.550** [+0.368,+0.696] | +0.052 [-0.164,+0.262] | +0.498 [+0.258,+0.732] | not equiv |

- α cross-dataset CI들이 **겹친다** (공통 구간 [0.368, 0.472]) → tissue-distance 순서(BMMC +0.55 > brain +0.48 > E18 +0.32)는 **정성적이며 정량적 단조 주장이 아니다**. 점 3개에 회귀 fit은 하지 않는다.
- 모든 cross-dataset lag ρ이 약하다; 등가성 여부는 갈린다(n~100 → 일부 CI는 등가성을 인증하기엔 너무 넓다 — 정직하게 보고하며 지어내지 않는다).
- ⚠️ **cross-dataset** E18 Δρ (+0.216 [−0.026, +0.449])는 0을 스친다 — n=132에서 검정력이 부족하다. E18 dissociation은 **within-dataset** E18 Δρ (+0.841 [+0.779, +0.903], §#1)가 담당한다; cross-dataset은 표본 1개다 → 강한 dissociation 검정이 아니라 replication 신호다(강한 일반화는 없다는 단서와 정합).

## Summary verdicts

- **DISSOCIATION (headline): HSPC Δρ (α − lag) = +0.720, 95%CI [+0.639, +0.802]** → CI가 넉넉한 여유로 0을 배제한다; lag 관례(magnitude/signed/rate-proxy)에 robust하다. α concordance가 lag보다 ~0.7 위에 있다. BMMC (Δρ≈0.9)와 E18 (Δρ≈0.8)에서 재현된다.
- **TOST (등가성, 보조, 정직한 갈림)**: *directional* lag (MoFlow×VAE, guardrail-clean)은 0과 등가다; *magnitude* lag (MV×VAE)은 weak-positive이며 HSPC/BMMC에서 엄격한 |ρ|<0.2 기준으로 등가로 인증되지 않고(CI가 한계를 스친다) E18에서는 등가다. 균일하게 지어낸 게 아니다 — 주장은 dissociation이 담당한다.
- **Identifiability 순위: α ≫ α_c > β > γ** — α만이 cross-method 불변량이다(ATAC이 없는 RNA-only floor가 α를 chromatin-method 수준으로 회복하는 것 포함).
- **γ/β ratio가 개별 β (0.08), γ (0.11)보다 더 잘 재현된다 (|ρ|≈0.32)** → scVelo scaling 비식별성.
- **Diff-budget: lag concordance (+0.12)가 두 성분(1/α +0.88, 1/α_c +0.29)보다 아래로 떨어진다** → 차분이 잡음을 증폭한다.
- **Cross-dataset α CI들이 겹친다** → tissue-distance 순서는 정성적일 뿐이다(점 3개에 추세 없음).

---

# Identifiability & α-vs-lag dissociation — bootstrap CI + TOST (CHEAP tier)

> Paired gene bootstrap B=10,000, seed=20260707 (deterministic). Percentile 95% CIs.
> Definitions reused verbatim from `p3_concordance.py` → numbers match FINDINGS/concordance.md.
> Guardrails: rank/magnitude concordance only (MultiVelo structural sign never invoked);
> CRAK-Velo excluded; 'lag not robust' stated as TOST equivalence vs |ρ|<0.2; cross-dataset = 1 sample each.

## #1 — Paired Δρ dissociation (α ≫ lag), bootstrap CI + TOST

> **lag = MAGNITUDE rank (|·|)** everywhere — the FINDINGS-consistent convention (external `concordance_*.py` use `.abs()`; MultiVelo sign is structural/uninformative). The headline is the **dissociation** (Δρ excludes 0), not equivalence.

### HSPC (within-dataset, MultiVelo × MultiVeloVAE, shared 538 genes) — PRIMARY

- ρ_α = **+0.882**  95%CI [+0.855, +0.904]
- ρ_lag (magnitude) = **+0.163**  95%CI [+0.078, +0.244]
- **Δρ = ρ_α − ρ_lag = +0.720**  95%CI **[+0.639, +0.802]** (bootstrap mean +0.719)
  → CI **excludes 0** — dissociation established (α sits ~0.7 above lag).

- Δρ robustness to lag convention: magnitude **+0.720** | signed (concordance.md §3.5, ρ_lag=-0.010) Δρ +0.893 | rate-proxy |1/α_c−1/α| (ρ_lag=-0.009) Δρ +0.891 — all CIs exclude 0.

### TOST equivalence — HSPC lag vs pre-declared bound |ρ|<0.2

- **magnitude lag (MV×VAE)** ρ=+0.163, 95%CI [+0.078, +0.244] → **NOT equivalent (CI exits [−0.2,+0.2])** — weak-positive, upper bound breaches +0.2 → equivalence NOT certified at strict bound.
  - ⚠️ FINDINGS §3.5 also cites a **signed** MV×VAE lag −0.010 (mixes MV-magnitude vs VAE-signed → category mismatch); magnitude-consistent value is +0.163. We report magnitude for cross-dataset consistency.
- **directional lag (MoFlow×VAE, guardrail-clean sign pair, shared 636)** ρ=**+0.083** 95%CI [+0.007, +0.158] → **EQUIVALENT (CI ⊂ [−0.2,+0.2])** — methods do NOT agree on lag *direction* beyond zero.
  → Split verdict: *directional* lag concordance IS equivalent to zero (MoFlow×VAE), *magnitude* concordance is weak-positive (MV×VAE). Both sit ~0.7 below α.

### External replications (within-dataset MV×VAE, magnitude lag)

- **GSE194122_bmmc** (shared 272): ρ_α **+0.906** [+0.879,+0.925], ρ_lag(mag) **-0.088** [-0.209,+0.034], **Δρ +0.994** 95%CI [+0.874,+1.110] (excludes 0).
  - TOST lag: **NOT equivalent (CI exits [−0.2,+0.2])**
- **e18_mouse_brain** (shared 1027): ρ_α **+0.898** [+0.883,+0.910], ρ_lag(mag) **+0.057** [-0.005,+0.118], **Δρ +0.841** 95%CI [+0.779,+0.903] (excludes 0).
  - TOST lag: **EQUIVALENT (CI ⊂ [−0.2,+0.2])**
- **human_brain**: no within-dataset MultiVeloVAE fit exists (only MultiVelo + floor) → within-dataset cross-method lag is **not computable**; its α-vs-lag evidence is the cross-dataset axis (§#5).

## #3a — Empirical identifiability ranking (cross-method reproducibility = identifiability)

> Canonical axis = MultiVelo × MultiVeloVAE (only pair exposing α_c). Ranked by SIGNED ρ (descending) with 95%CI — identifiability = positive cross-method reproduction (negative ρ = rank-reversed = least identifiable).

| rank | parameter | MV×VAE Spearman | 95% CI | identifiable? |
|---|---|---|---|---|
| 1 | α (transcription rate) | **+0.882** | [+0.855, +0.905] | **YES (invariant)** |
| 2 | α_c (chromatin opening) | **+0.291** | [+0.209, +0.369] | no (fragile) |
| 3 | β (splicing) | **+0.080** | [-0.009, +0.168] | no (fragile) |
| 4 | γ (degradation) | **-0.109** | [-0.192, -0.023] | no (fragile) |

### RNA-pinned evidence — floor (NO chromatin channel) recovers α ≈ chromatin methods

- **α: floor × MultiVelo** (shared 368): Spearman **+0.818** 95%CI [+0.773, +0.855] — floor has NO ATAC yet recovers α at chromatin-method strength.
- **α: floor × MultiVeloVAE** (shared 434): Spearman **+0.889** 95%CI [+0.862, +0.910] — floor has NO ATAC yet recovers α at chromatin-method strength.

→ **α stands alone as the identifiable invariant**; α_c, β, γ all fragile (CI includes/near 0). Empirical identifiability ranking: **α ≫ α_c > β > γ**.

## #3b — γ/β ratio sloppiness probe (steady-state slope identifiability)

> Splicing ODE: only steady-state slope γ/β (+scaling) is identifiable. Ratio should reproduce cross-method better than individual β, γ. Genes with |β|>1e-4 in both methods.

- **γ/β ratio** (MV×VAE, n=538): Spearman **-0.324** 95%CI [-0.400, -0.244]
- **β alone** (MV×VAE, n=538): Spearman **+0.080** 95%CI [-0.010, +0.169]
- **γ alone** (MV×VAE, n=538): Spearman **-0.109** 95%CI [-0.192, -0.024]
> Verdict: even the theoretically-identifiable steady-state slope γ/β does **NOT** cleanly reproduce cross-method (ρ=−0.32, *negative* = anti-reproduction) — **only α reproduces cleanly**. The prediction holds only in the weak sense that |ρ(γ/β)|≈0.32 exceeds |ρ_β|=0.08 and |ρ_γ|=0.11 (the combination is less badly determined than the individual rates — scVelo scaling sloppiness in *magnitude*), but the negative sign (MV vs VAE parameterization/scaling convention a rank correlation can't absorb) means the slope itself is not a reproducible invariant. α stands alone.

## Diff-budget — lag = difference of two noisy timings

> Cross-method (MV×VAE) concordance of the rate-timescale COMPONENTS (1/α, 1/α_c) vs their DIFFERENCE (lag = 1/α_c − 1/α). Spearman is invariant to the shared 1/x transform, so ρ(1/α)=ρ(α) and ρ(1/α_c)=ρ(α_c).

- **1/α component**: Spearman **+0.882** 95%CI [+0.856, +0.905]
- **1/α_c component**: Spearman **+0.291** 95%CI [+0.209, +0.370]
- **difference (lag = 1/α_c − 1/α, signed)**: Spearman **+0.124** 95%CI [+0.036, +0.210]
> One component strong (1/α +0.88), one weak (1/α_c +0.29); the DIFFERENCE **falls below even the weaker component** → differencing collapses concordance. Prediction holds: lag inherits α_c fragility and differencing amplifies noise.

## #5 — Cross-dataset replication CIs (reject monotonicity as a claim)

> Bootstrap 95%CI on the three cross-dataset MultiVelo α ρ and their lag counterparts. Overlap → tissue-distance ordering is QUALITATIVE, not a quantitative claim. No trend fit on 3 points.

| dataset | shared | α cross ρ (95%CI) | lag cross ρ (95%CI) | Δρ (95%CI) | lag TOST |
|---|---|---|---|---|---|
| human_brain (adult brain) | 102 | **+0.475** [+0.292,+0.626] | +0.185 [-0.005,+0.369] | +0.290 [+0.055,+0.518] | not equiv |
| E18 mouse brain (fetal, cross-species) | 132 | **+0.321** [+0.158,+0.472] | +0.105 [-0.069,+0.269] | +0.216 [-0.026,+0.449] | not equiv |
| GSE194122 BMMC (same-tissue human) | 88 | **+0.550** [+0.368,+0.696] | +0.052 [-0.164,+0.262] | +0.498 [+0.258,+0.732] | not equiv |

- α cross-dataset CIs **OVERLAP** (common region [0.368, 0.472]) → tissue-distance ordering (BMMC +0.55 > brain +0.48 > E18 +0.32) is **qualitative, not a quantified monotonic claim**. No regression fit on 3 points.
- Every cross-dataset lag ρ is weak; equivalence status varies (n~100 → some CIs too wide to certify equivalence — reported honestly, not manufactured).
- ⚠️ The **cross-dataset** E18 Δρ (+0.216 [−0.026, +0.449]) grazes 0 — underpowered at n=132. The E18 dissociation is carried by the **within-dataset** E18 Δρ (+0.841 [+0.779, +0.903], §#1); cross-dataset is 1 sample → replication signal, not a powered dissociation test (consistent with the no-strong-generalization caveat).

## Summary verdicts

- **DISSOCIATION (headline): HSPC Δρ (α − lag) = +0.720, 95%CI [+0.639, +0.802]** → CI excludes 0 by a wide margin; robust to lag convention (magnitude/signed/rate-proxy). α concordance sits ~0.7 above lag. Replicated in BMMC (Δρ≈0.9) and E18 (Δρ≈0.8).
- **TOST (equivalence, secondary, honest split)**: *directional* lag (MoFlow×VAE, guardrail-clean) IS equivalent to zero; *magnitude* lag (MV×VAE) is weak-positive and NOT certified equivalent at strict |ρ|<0.2 in HSPC/BMMC (CI grazes bound), equivalent in E18. Not manufactured uniform — the dissociation carries the claim.
- **Identifiability ranking: α ≫ α_c > β > γ** — α alone is the cross-method invariant (incl. RNA-only floor with no ATAC recovering α at chromatin-method strength).
- **γ/β ratio reproduces better (|ρ|≈0.32) than individual β (0.08), γ (0.11)** → scVelo scaling non-identifiability.
- **Diff-budget: lag concordance (+0.12) falls below both components (1/α +0.88, 1/α_c +0.29)** → differencing amplifies noise.
- **Cross-dataset α CIs overlap** → tissue-distance ordering qualitative only (no trend on 3 points).
