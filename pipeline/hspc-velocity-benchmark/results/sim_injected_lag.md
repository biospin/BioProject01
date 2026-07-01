# P5 accuracy arm — injected-lag simulator (DESIGN §5)

- 200 gene × 600 cell, injected τ∈[−0.2,0.2] pseudotime, β=2.0 γ=1.0, seed=20260701. 인과 chromatin→RNA → s는 항상 c보다 늦음(true_lag>0).
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

- **부호 반전 + 크기 붕괴(핵심 — 2026-07-01 정정)**: 무noise Spearman(true,rec)=**−0.891**. ⚠️ 이는 "순위를 못 recover함"이 **아니라** — |ρ|=0.89는 estimator가 true-lag 순위를 **강하게 추적**한다는 뜻(무정보라면 ρ≈0). 문제는 **부호가 뒤집히고**(음의 상관) **크기가 붕괴**(과소추정 0.06×, true_lag 20~50 bin인데 recovered −6~7 bin)한다는 것. 여러 kinetic 설정(β,γ,θ 스윕)에서도 ρ 일관 음수(−0.41~−0.86) → **crakvelo manual-DP DTW estimator는 매끄러운 동역학에서 offset을 대각선으로 붕괴시켜 부호를 반전·크기를 포화시킨다**(shape-dependent construct 아티팩트). 즉 "lag은 recover 불가"가 아니라 "이 특정 construct가 smooth regime에서 부호·크기를 왜곡".
  - ⚠️ **정정 사유(honesty)**: 이전 문구 "크기/순위 회복 실패"는 |ρ|=0.89를 무정보처럼 읽은 **오해석**이었음. estimator는 rank를 추적하되 부호·크기가 shape-의존으로 붕괴하는 것이 정확한 진술. 상세: memory `crakvelo-dtw-lag-shape-dependence`.
  - **스코프**: 이 arm은 **crakvelo manual-DP estimator만** 테스트(§한계 ③). MoFlow `fastdtw`·MultiVelo switch-time은 미검정 → 핵심 H1(moflow×multivelo×mvvae 무상관, α robust ρ=0.88)은 이 construct에 **의존하지 않아 독립 생존**.
- **부호도 regime 의존**: 무noise sign(+) 74.0%이나 kinetic 설정 바꾸면 24~78%로 요동, noise σ≥0.15에서 ~50%(무정보)로 붕괴. → 부호조차 매끄러운 실데이터에서 신뢰 제한적.
- **Task 1 부호 수정과의 관계(모순 아님)**: Task 1은 manual DP가 reference(MoFlow fastdtw)와 *반대*였던 명백한 구현 버그를 고친 것(sharp 신호·marker로 검증). 본 simulator는 *수정 후에도* estimator 자체가 매끄러운 동역학에서 한계임을 정량화. 즉 '버그 수정은 옳고, estimator는 그래도 부정확'.
- **H1과의 연결(정정된 스코프)**: 이 arm이 보이는 것은 "lag은 원리적으로 recover 불가"가 **아니라**, **crakvelo manual-DP DTW construct가 부호·크기를 shape-의존으로 왜곡**한다는 것(rank는 추적). 따라서 이 arm은 **CRAK-Velo lag을 cross-method 비교에서 신뢰하지 말라**는 근거이지, lag 개념 자체의 부정이 아니다. 핵심 H1의 cross-method 비robust 결론은 **moflow fastdtw × multivelo switch-time × mvvae rate**(이 construct 미사용)에서 이미 성립하고 α robust(ρ=0.88)도 독립. → 박상준 cross-review(BIOP01-25) 대비: **우리 주장은 "lag은 절대 예측 못 함"이 아니라 "method 바꾸면(cross-method) lag이 안 살아남는다"**로 정밀 스코프. 그의 단일 파이프라인 내 lag 예측 성공과 양립 가능.
- ⚠️ 한계: ① 1-switch causal kinetic이라 s가 항상 c에 후행 → RNA-leading(음수 lag) 케이스 미생성, 부호 *판별력*은 미검정. ② Gaussian noise는 burst/ambient 미반영 → 회복력 **상한**. ③ 본 arm은 crakvelo식 manual-DP estimator 대상; MoFlow fastdtw·MultiVelo switch-time을 동일 합성데이터에 적용하는 method 확장은 다음 단계.
