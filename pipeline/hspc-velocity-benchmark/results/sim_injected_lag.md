# P5 accuracy arm — injected-lag simulator (DESIGN §5)

- 200 gene × 600 cell, injected τ∈[−0.2,0.2] pseudotime, β=2.0 γ=1.0, seed=20260701. 인과 chromatin→RNA 구조라 s는 항상 c보다 늦다(true_lag>0).
- ground truth = 경험적 t50(s)−t50(c) [bin]. estimator = 부호 수정된 DTW c-s lag(`p2_crakvelo_lag.dtw_lag`).

## 회복력 (noise 스윕)

| noise σ | n | Spearman(true, recovered) | sign(+) 비율 | 과소추정 |
|---|---|---|---|---|
| 0.00 | 200 | -0.891 (p=9.0e-70) | 74.0% | 0.06× |
| 0.05 | 200 | -0.420 (p=5.8e-10) | 71.5% | 0.04× |
| 0.15 | 200 | -0.118 (p=9.7e-02) | 49.5% | 0.00× |
| 0.30 | 200 | -0.201 (p=4.3e-03) | 26.5% | -0.03× |
| 0.50 | 200 | -0.316 (p=5.1e-06) | 11.0% | -0.09× |

![sim](figures/sim_injected_lag.png)

## 해석

- **부호 반전 + 크기 붕괴(핵심 — 2026-07-01 정정)**: 잡음 없는 조건에서 Spearman(true,rec)=**−0.891**이다. ⚠️ 이는 "순위를 못 recover함"이 **아니라** — |ρ|=0.89는 estimator가 true-lag 순위를 **강하게 추적**한다는 뜻이다(무정보라면 ρ≈0). 문제는 **부호가 뒤집히고**(음의 상관) **크기가 붕괴**한다는 데 있다(과소추정 0.06×, true_lag는 20~50 bin인데 recovered는 −6~7 bin). 여러 kinetic 설정(β,γ,θ 스윕)에서도 ρ는 일관되게 음수이며(−0.41~−0.86) → **crakvelo manual-DP DTW estimator는 매끄러운 동역학에서 offset을 대각선으로 붕괴시켜 부호를 반전하고 크기를 포화시킨다**(shape-dependent construct 아티팩트). 즉 "lag은 recover 불가"가 아니라 "이 특정 construct가 smooth regime에서 부호와 크기를 왜곡한다"는 것이다.
  - ⚠️ **정정 사유(honesty)**: 이전 문구 "크기/순위 회복 실패"는 |ρ|=0.89를 무정보처럼 읽은 **오해석**이었다. estimator는 rank를 추적하되 부호와 크기가 shape에 의존해 붕괴한다는 것이 정확한 진술이다. 상세는 memory `crakvelo-dtw-lag-shape-dependence` 참조.
  - **스코프**: 이 arm은 **crakvelo manual-DP estimator만** 테스트한다(§한계 ③). MoFlow `fastdtw`와 MultiVelo switch-time은 미검정이므로 → 핵심 H1(moflow×multivelo×mvvae 무상관, α robust ρ=0.88)은 이 construct에 **의존하지 않아 독립적으로 생존한다**.
- **부호도 regime에 의존**: 잡음 없는 조건에서 sign(+)이 74.0%이나 kinetic 설정을 바꾸면 24~78%로 요동치고, noise σ≥0.15에서 ~50%(무정보)로 붕괴한다. → 부호조차 매끄러운 실데이터에서는 신뢰가 제한적이다.
- **Task 1 부호 수정과의 관계(모순 아님)**: Task 1은 manual DP가 reference(MoFlow fastdtw)와 *반대*였던 명백한 구현 버그를 고친 것이다(sharp 신호와 marker로 검증). 본 simulator는 *수정 후에도* estimator 자체가 매끄러운 동역학에서 한계를 가짐을 정량화한다. 즉 '버그 수정은 옳고, estimator는 그래도 부정확하다'.
- **H1과의 연결(정정된 스코프)**: 이 arm이 보이는 것은 "lag은 원리적으로 recover 불가"가 **아니라**, **crakvelo manual-DP DTW construct가 부호와 크기를 shape에 의존해 왜곡**한다는 것이다(rank는 추적한다). 따라서 이 arm은 **CRAK-Velo lag을 cross-method 비교에서 신뢰하지 말라**는 근거이지, lag 개념 자체의 부정이 아니다. 핵심 H1의 cross-method 비robust 결론은 **moflow fastdtw × multivelo switch-time × mvvae rate**(이 construct 미사용)에서 이미 성립하며 α robust(ρ=0.88)도 독립적이다. → 박상준 cross-review(BIOP01-25)에 대비하면: **우리 주장은 "lag은 절대 예측 못 함"이 아니라 "method를 바꾸면(cross-method) lag이 살아남지 않는다"**로 정밀하게 스코프를 좁힌 것이다. 그의 단일 파이프라인 내 lag 예측 성공과 양립 가능하다.
- ⚠️ 한계: ① 1-switch causal kinetic이라 s가 항상 c에 후행하므로 → RNA-leading(음수 lag) 케이스가 생성되지 않아 부호 *판별력*은 미검정이다. ② Gaussian noise는 burst/ambient를 반영하지 않으므로 → 회복력은 **상한**이다. ③ 본 arm은 crakvelo식 manual-DP estimator를 대상으로 하며, MoFlow fastdtw와 MultiVelo switch-time을 동일 합성데이터에 적용하는 method 확장은 다음 단계다.

---

# P5 accuracy arm — injected-lag simulator (DESIGN §5)

- 200 genes × 600 cells, injected τ∈[−0.2,0.2] pseudotime, β=2.0 γ=1.0, seed=20260701. Causal chromatin→RNA, so s always lags c (true_lag>0).
- ground truth = empirical t50(s)−t50(c) [bin]. estimator = sign-corrected DTW c-s lag (`p2_crakvelo_lag.dtw_lag`).

## Recovery (noise sweep)

| noise σ | n | Spearman(true, recovered) | sign(+) fraction | underestimation |
|---|---|---|---|---|
| 0.00 | 200 | -0.891 (p=9.0e-70) | 74.0% | 0.06× |
| 0.05 | 200 | -0.420 (p=5.8e-10) | 71.5% | 0.04× |
| 0.15 | 200 | -0.118 (p=9.7e-02) | 49.5% | 0.00× |
| 0.30 | 200 | -0.201 (p=4.3e-03) | 26.5% | -0.03× |
| 0.50 | 200 | -0.316 (p=5.1e-06) | 11.0% | -0.09× |

![sim](figures/sim_injected_lag.png)

## Interpretation

- **Sign flip + magnitude collapse (key — corrected 2026-07-01)**: at zero noise, Spearman(true,rec)=**−0.891**. ⚠️ This is **not** "failure to recover the rank" — |ρ|=0.89 means the estimator **strongly tracks** the true-lag rank (an uninformative estimator would give ρ≈0). The problem is that **the sign flips** (negative correlation) and **the magnitude collapses** (underestimation 0.06×, true_lag is 20~50 bin but recovered is −6~7 bin). Across several kinetic settings (β,γ,θ sweeps) ρ is consistently negative (−0.41~−0.86) → **the crakvelo manual-DP DTW estimator collapses the offset onto the diagonal under smooth dynamics, flipping the sign and saturating the magnitude** (a shape-dependent construct artifact). That is, not "lag cannot be recovered" but "this particular construct distorts sign and magnitude in the smooth regime."
  - ⚠️ **Reason for correction (honesty)**: the earlier wording "magnitude/rank recovery failure" was a **misinterpretation** that read |ρ|=0.89 as if uninformative. The accurate statement is that the estimator tracks rank but sign and magnitude collapse in a shape-dependent way. Details: see memory `crakvelo-dtw-lag-shape-dependence`.
  - **Scope**: this arm tests **only the crakvelo manual-DP estimator** (§limitation ③). MoFlow `fastdtw` and MultiVelo switch-time are not tested → the core H1 (moflow×multivelo×mvvae no correlation, α robust ρ=0.88) does **not depend on this construct and survives independently**.
- **The sign is also regime-dependent**: at zero noise sign(+) is 74.0%, but changing the kinetic setting makes it swing between 24~78%, and at noise σ≥0.15 it collapses to ~50% (uninformative). → Even the sign has limited reliability on smooth real data.
- **Relation to the Task 1 sign correction (not a contradiction)**: Task 1 fixed a clear implementation bug where manual DP was *opposite* to the reference (MoFlow fastdtw) (verified with sharp signals and markers). This simulator quantifies that *even after the fix* the estimator itself is limited under smooth dynamics. That is, 'the bug fix is correct, and the estimator is still inaccurate'.
- **Link to H1 (corrected scope)**: what this arm shows is **not** "lag cannot in principle be recovered," but that **the crakvelo manual-DP DTW construct distorts sign and magnitude in a shape-dependent way** (rank is tracked). Therefore this arm is grounds for **not trusting CRAK-Velo lag in cross-method comparison**, not a negation of the lag concept itself. The core H1 cross-method non-robustness conclusion already holds on **moflow fastdtw × multivelo switch-time × mvvae rate** (which do not use this construct), and α robustness (ρ=0.88) is independent. → For the Park Sang-jun cross-review (BIOP01-25): **our claim is not "lag can never be predicted" but "when you change method (cross-method), lag does not survive"** — a precisely scoped claim. It is compatible with his successful lag prediction within a single pipeline.
- ⚠️ Limitations: ① The 1-switch causal kinetic makes s always trail c → RNA-leading (negative lag) cases are not generated, so sign *discriminability* is not tested. ② Gaussian noise does not reflect burst/ambient → recovery is an **upper bound**. ③ This arm targets the crakvelo-style manual-DP estimator; extending the method by applying MoFlow fastdtw and MultiVelo switch-time to the same synthetic data is the next step.
