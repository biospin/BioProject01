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

- **크기/순위 회복 실패(핵심)**: s가 window 내 100% 완료(truncation 아님)인데도 무noise Spearman(true,rec)=-0.891(음수=순위 역전), 과소추정 0.06× (true_lag 20~50 bin인데 recovered −6~7 bin). 여러 kinetic 설정(β,γ,θ 스윕)에서도 Spearman이 일관 음수(−0.41~−0.86) → **DTW c-s lag(manual DP)은 매끄러운 동역학에서 lag *크기·순위*를 회복 못 함**(DTW가 stretch로 정렬해 offset 포화·역전).
- **부호도 regime 의존**: 무noise sign(+) 74.0%이나 kinetic 설정 바꾸면 24~78%로 요동, noise σ≥0.15에서 ~50%(무정보)로 붕괴. → 부호조차 매끄러운 실데이터에서 신뢰 제한적.
- **Task 1 부호 수정과의 관계(모순 아님)**: Task 1은 manual DP가 reference(MoFlow fastdtw)와 *반대*였던 명백한 구현 버그를 고친 것(sharp 신호·marker로 검증). 본 simulator는 *수정 후에도* estimator 자체가 매끄러운 동역학에서 한계임을 정량화. 즉 '버그 수정은 옳고, estimator는 그래도 부정확'.
- **H1과의 연결**: ground truth가 있어도 construct가 lag 크기/순위/부호를 신뢰성 있게 못 recover → **method 간 lag 불일치(H1 실패)는 noise뿐 아니라 construct 자체의 정확도 한계**가 근원. robust한 건 α(ρ=0.88)·집단 방향균형·canonical marker뿐이라는 FINDINGS 결론을 정량적으로 뒷받침.
- ⚠️ 한계: ① 1-switch causal kinetic이라 s가 항상 c에 후행 → RNA-leading(음수 lag) 케이스 미생성, 부호 *판별력*은 미검정. ② Gaussian noise는 burst/ambient 미반영 → 회복력 **상한**. ③ 본 arm은 crakvelo식 manual-DP estimator 대상; MoFlow fastdtw·MultiVelo switch-time을 동일 합성데이터에 적용하는 method 확장은 다음 단계.
