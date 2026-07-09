# Profile-likelihood practical identifiability — MultiVelo objective

> **핵심 판정**: MultiVelo의 *자기 목적함수* 위에서, 전사율 **α는 국소 식별 가능(stiff)** 방향인 반면
> chromatin→transcription **lag은 체계적으로 sloppy + boundary-limited** 방향이다.
> 이는 우리의 cross-method/cross-dataset "lag-fragile / α-robust" 관찰을
> **해석이 아니라 목적함수의 성질로 *입증* 승격**한다.
> 단, 이것은 **상대적(practical) 비식별성**이지 완전히 평탄한 likelihood valley가 아니다(정직 framing).

## Feasibility 판정: YES (상대적 비식별성으로 재현)
n=538 gene에서 fixed-nuisance profile likelihood를 α 방향과 lag 방향으로 각각 스캔한 결과,
α 곡률이 lag 곡률보다 유의하게 크다(집단 수준으로 재현). lag이 무정보인 것이 아니라 α보다
**덜 constrain**되며, 상당수 gene에서 admissible pseudotime 경계에 눌린다(boundary-pinned).

## 방법
- **목적함수**: MultiVelo 4-state chromatin-RNA likelihood (`p3_profile_likelihood.py`;
  fit_t·likelihood 재현 검증 r≈1.0).
- **fixed-nuisance profile (main, n=538)**: MLE에서 α를 log-perturb, 그리고 lag(=t_sw2−t_sw1)을
  log-perturb하면서 각 방향의 per-cell 곡률 κ = −d²LL/d(ln θ)² 를 측정. latent time은 재최적화.
- **freed-nuisance gate (부분)**: β/γ/α_c/rescale/scale_cc 를 재최적화하며 같은 두 방향 곡률비를 재측정.
  현재 CSV는 부분(stale smoke, 사용 가능한 ratio_freed n=1: LMNA 5.30x) — **main(538)이 주장을 담당**하고
  freed는 방향 확인용 보조. (전체 재실행은 main CSV를 덮어쓰므로 이번 마무리 단계에선 미실행.)

## 핵심 수치 (모두 `profile_likelihood_identifiability.csv`에서 재검증)
| 지표 | 값 |
| --- | --- |
| per-cell 곡률 α (κ_alpha_pc) median | **8.20 / cell** |
| per-cell 곡률 lag (κ_lag_pc) median | **2.24 / cell** |
| gene별 stiffness 비 κ_alpha/κ_lag (interior, both>0, n=258) median | **3.53×** (IQR [1.92, 7.41]) |
| **frac(α가 lag보다 stiff)** | **94.57%** (244/258) |
| interior lag CI 폭 / admissible pseudotime range, median | **6.55%** |
| α fold-change CI (upper bound) | 대다수 gene에서 profile grid step(1.17×) 이하로 clamp — α는 스캔 해상도보다 더 tight하게 pinned (grid-limited 상한, 측정 CI 아님) |

> 주의: `alpha_fold_lo`의 25/50/75 분위수가 모두 1.166으로 동일 = ≥50% gene이 profile grid 첫 스텝에 눌림.
> 따라서 α의 fold-CI는 **grid 해상도의 상한**이지 per-gene CI가 아니다. 실제 α-stiff 주장은 grid에 무관한
> **곡률비 3.53×**가 담당(un-clamped, load-bearing). lag CI 폭(pseudotime 분수)과 α fold는 단위가 달라 직접
> 폭 비교 대신 **같은 단위 지표인 곡률비**로 비교한다.

## lag trichotomy (n=538)
| class | n | % | 해석 |
| --- | --- | --- | --- |
| **interior** | 302 | 56% | profile 스캔 가능 — sloppy하지만 내부 최소값 존재 |
| **boundary_pinned** | 205 | 38% | t_sw2가 admissible 경계(~20)에 눌림 → lag 상한 무정보 |
| **degenerate** | 31 | 6% | 곡률 소실 — 사실상 평탄 |
> 44%(boundary_pinned + degenerate)에서 lag은 데이터로 위쪽 경계를 정할 수 없다 =
> lag이 "느슨한 추정"조차 안 되는 gene이 절반 가까이. α는 이 문제를 거의 겪지 않는다(94.57% stiff).

## 그림
`figures/fig05_profile_likelihood.png` (English labels only; git-ignored):
- **A** — per-cell 곡률 violin: α med 8.20/cell(stiff) vs lag med 2.24/cell(sloppy).
- **B** — gene별 κ_alpha/κ_lag 히스토그램: median 3.53×, 95% gene에서 α가 더 stiff.
- **C** — lag trichotomy bar: interior 302 / boundary_pinned 205 / degenerate 31.
- **D** — 대표 gene(TLE1) 프로파일 overlay: α(빨강) 좁고 가파름, lag(파랑) 얕고 평탄.

## 한계
1. **단일 method**: MultiVelo 목적함수에 국한. "α가 lag보다 식별 가능"은 *이 우도*의 기하학적 성질.
   다른 method의 목적함수 형태는 다를 수 있음(단, cross-method 관찰과 방향 정합).
2. **freed-nuisance 부분**: nuisance 재최적화 게이트는 부분(사용가능 n=1). main fixed-nuisance(538)가
   주장을 담당. 완전 게이트는 후속(main CSV 보호 위해 별도 출력 경로로 재실행 필요).
3. **상대적 비식별성**: 완전 평탄 valley가 아니라 α 대비 상대적으로 sloppy — 과대 주장 금지.
4. **boundary는 admissible pseudotime range 설정에 부분 의존**(TOTAL_H) — 경계 눌림은 데이터+파라미터화 상호작용.

## 정합성 (다른 arm과)
- **dissociation**(`identifiability_dissociation.md`): lag과 α의 추정 불확실성이 분리됨과 정합.
- **external rate validation**(`external_rate_validation*.md`): α가 외부에서 재현되는 것과 정합.
- **cross-dataset §7**: within/cross-dataset에서 α-robust ≫ lag-fragile 순서와 같은 방향.
→ 이 데모는 그 관찰들의 *메커니즘*(우도 기하)을 제공: lag이 재현 안 되는 이유는 노이즈가 아니라
  목적함수가 lag 방향으로 애초에 덜 정보적이기 때문.

## 재현 커맨드
```bash
cd pipeline/hspc-velocity-benchmark
# main identifiability (이미 완성 — 재계산 불필요, 재현 시에만):
conda run --no-capture-output -n mv python -u scripts/p3_profile_likelihood.py
# figure:
conda run --no-capture-output -n mv python figures/fig05_profile_likelihood.py
# freed-nuisance 부분 게이트(별도 subset, main CSV 덮어씀 주의):
conda run --no-capture-output -n mv python -u scripts/p3_profile_likelihood.py --subset 30
```
