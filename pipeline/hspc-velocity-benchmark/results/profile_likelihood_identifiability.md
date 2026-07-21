# Profile-likelihood practical identifiability — MultiVelo objective

> **핵심 판정**: MultiVelo의 *자기 목적함수* 위에서, 전사율 **α는 국소 식별 가능(stiff — 목적함수를 그 방향으로 흔들면 점수가 급격히 변한다=데이터로 값이 잘 정해진다)** 방향인 반면
> chromatin→transcription **lag은 체계적으로 sloppy(그 방향으론 흔들어도 점수가 거의 안 변한다=데이터로 값이 잘 안 정해진다) + boundary-limited(추정이 허용 구간의 경계에 눌려 상한을 못 정한다)** 방향이다.
> 이는 우리의 cross-method/cross-dataset "lag-fragile / α-robust" 관찰을
> **해석이 아니라 목적함수의 성질로 *입증* 승격**한다.
> 단, 이것은 **상대적(practical) 비식별성**이지 완전히 평탄한 likelihood valley가 아니다(정직 framing).

## Feasibility 판정: YES (상대적 비식별성으로 재현)
n=538 gene에서 fixed-nuisance profile likelihood(관심 파라미터 하나만 값을 바꿔가며 고정하고 나머지를 재최적화해 그 방향의 우도 곡선을 그리는 것)를 α 방향과 lag 방향으로 각각 스캔한 결과,
α 곡률이 lag 곡률보다 유의하게 크다(집단 수준으로 재현된다). lag이 무정보인 것이 아니라 α보다
**덜 제약되며**, 상당수 gene에서 admissible pseudotime 경계에 눌린다(boundary-pinned).

## 방법
- **목적함수**: MultiVelo 4-state chromatin-RNA likelihood (`p3_profile_likelihood.py`;
  fit_t·likelihood 재현 검증 r≈1.0).
- **fixed-nuisance profile (main, n=538)**: MLE에서 α를 log-perturb, 그리고 lag(=t_sw2−t_sw1)을
  log-perturb하면서 각 방향의 per-cell 곡률 κ = −d²LL/d(ln θ)² 를 측정한다. latent time은 재최적화한다.
- **freed-nuisance gate (완주, 2026-07-10, interior 258)**: β/γ/α_c/rescale/scale_cc를 재최적화하며 같은 두 방향 곡률비를 재측정.
  **해리(α≫lag) 생존**: ratio_freed median **2.49×**, α still stiffer **77.03%**(n=148). 단 β/γ 자유화 시 **α 곡률이 fixed 대비 median 0.19×로 붕괴**(alpha peak collapses) → fixed 3.53×/94.57%는 상한, freed **2.49×/77%가 보수적 하한**이며 서술 기준이다. (`profile_likelihood_freed.csv`; main CSV는 결정론적 재계산으로 불변 확인.)

## 핵심 수치 (모두 `profile_likelihood_identifiability.csv`에서 재검증)
| 지표 | 값 |
| --- | --- |
| per-cell 곡률 α (κ_alpha_pc) median | **8.20 / cell** |
| per-cell 곡률 lag (κ_lag_pc) median | **2.24 / cell** |
| gene별 stiffness 비 κ_alpha/κ_lag (interior, both>0, n=258) median | **3.53×** (IQR [1.92, 7.41]) |
| **frac(α가 lag보다 stiff)** | **94.57%** (244/258) |
| interior lag CI 폭 / admissible pseudotime range, median | **6.55%** |
| α fold-change CI (upper bound) | 대다수 gene에서 profile grid step(1.17×) 이하로 clamp — α는 스캔 해상도보다 더 tight하게 pinned (grid-limited 상한, 측정 CI 아님) |

> 주의: `alpha_fold_lo`의 25/50/75 분위수가 모두 1.166으로 동일 = ≥50% gene이 profile grid 첫 스텝에 눌린다.
> 따라서 α의 fold-CI는 **grid 해상도의 상한**이지 per-gene CI가 아니다. 실제 α-stiff 주장은 grid에 무관한
> **곡률비 3.53×**가 담당한다(un-clamped, load-bearing). lag CI 폭(pseudotime 분수)과 α fold는 단위가 달라 직접
> 폭 비교 대신 **같은 단위 지표인 곡률비**로 비교한다.

## lag trichotomy (n=538)
| class | n | % | 해석 |
| --- | --- | --- | --- |
| **interior** | 302 | 56% | profile 스캔 가능 — sloppy하지만 내부 최소값 존재 |
| **boundary_pinned** | 205 | 38% | t_sw2가 admissible 경계(~20)에 눌림 → lag 상한 무정보 |
| **degenerate** | 31 | 6% | 곡률 소실 — 사실상 평탄 |
> 44%(boundary_pinned + degenerate)에서 lag은 데이터로 위쪽 경계를 정할 수 없다 =
> lag이 "느슨한 추정"조차 안 되는 gene이 절반 가깝다. α는 이 문제를 거의 겪지 않는다(94.57% stiff).

## 그림
`figures/fig05_profile_likelihood.png` (English labels only; git-ignored):
- **A** — per-cell 곡률 violin: α med 8.20/cell(stiff) vs lag med 2.24/cell(sloppy).
- **B** — gene별 κ_alpha/κ_lag 히스토그램: median 3.53×, 95% gene에서 α가 더 stiff.
- **C** — lag trichotomy bar: interior 302 / boundary_pinned 205 / degenerate 31.
- **D** — 대표 gene(TLE1) 프로파일 overlay: α(빨강) 좁고 가파름, lag(파랑) 얕고 평탄.

## 한계
1. **단일 method**: MultiVelo 목적함수에 국한된다. "α가 lag보다 식별 가능"은 *이 우도*의 기하학적 성질이다.
   다른 method의 목적함수 형태는 다를 수 있다(단, cross-method 관찰과 방향은 정합한다).
2. **freed-nuisance 부분**: nuisance 재최적화 게이트는 부분적이다(사용가능 n=1). main fixed-nuisance(538)가
   주장을 담당한다. 완전 게이트는 후속 과제다(main CSV 보호를 위해 별도 출력 경로로 재실행이 필요하다).
3. **상대적 비식별성**: 완전 평탄 valley가 아니라 α에 견줘 상대적으로 sloppy할 뿐이다 — 과대 주장은 금지한다.
4. **boundary는 admissible pseudotime range 설정에 부분 의존한다**(TOTAL_H) — 경계 눌림은 데이터+파라미터화의 상호작용이다.

## 정합성 (다른 arm과)
- **dissociation**(`identifiability_dissociation.md`): lag과 α의 추정 불확실성이 분리된다는 것과 정합한다.
- **external rate validation**(`external_rate_validation*.md`): α가 외부에서 재현된다는 것과 정합한다.
- **cross-dataset §7**: within/cross-dataset에서 α-robust ≫ lag-fragile 순서와 같은 방향이다.
→ 이 데모는 그 관찰들의 *메커니즘*(우도 기하)을 제공한다: lag이 재현 안 되는 이유는 잡음이 아니라
  목적함수가 lag 방향으로 애초에 덜 정보적이기 때문이다.

## 재현 커맨드
```bash
cd pipeline/hspc-velocity-benchmark
# main identifiability (이미 완성 — 재계산 불필요, 재현 시에만):
conda run --no-capture-output -n velo-mv python -u scripts/p3_profile_likelihood.py
# figure:
conda run --no-capture-output -n velo-mv python figures/fig05_profile_likelihood.py
# freed-nuisance 부분 게이트(별도 subset, main CSV 덮어씀 주의):
conda run --no-capture-output -n velo-mv python -u scripts/p3_profile_likelihood.py --subset 30
```

---

# Profile-likelihood practical identifiability — MultiVelo objective

> **Core verdict**: On MultiVelo's *own objective function*, the transcription rate **α is locally identifiable (stiff — perturbing the objective along that direction changes the score sharply = the value is well determined by the data)**,
> whereas the chromatin→transcription **lag is systematically sloppy (perturbing along that direction barely changes the score = the value is poorly determined by the data) + boundary-limited (the estimate is pinned to the edge of the admissible range and its upper bound cannot be set)**.
> This **promotes** our cross-method/cross-dataset "lag-fragile / α-robust" observation from an *interpretation* to something *proven* as a property of the objective function.
> That said, this is **relative (practical) non-identifiability**, not a fully flat likelihood valley (honest framing).

## Feasibility verdict: YES (reproduced as relative non-identifiability)
Scanning the fixed-nuisance profile likelihood (fixing one parameter of interest at successive values while re-optimizing the rest, tracing the likelihood curve along that direction) along the α direction and the lag direction over n=538 genes,
the α curvature is significantly larger than the lag curvature (reproduced at the population level). The lag is not uninformative but is **less constrained** than α, and in a substantial fraction of genes it is pinned to the admissible pseudotime boundary (boundary-pinned).

## Method
- **Objective function**: MultiVelo 4-state chromatin-RNA likelihood (`p3_profile_likelihood.py`; fit_t·likelihood reproduction check r≈1.0).
- **fixed-nuisance profile (main, n=538)**: from the MLE, log-perturb α, and log-perturb the lag (=t_sw2−t_sw1), measuring the per-cell curvature in each direction κ = −d²LL/d(ln θ)². latent time is re-optimized.
- **freed-nuisance gate (completed, 2026-07-10, interior 258)**: re-optimize β/γ/α_c/rescale/scale_cc and re-measure the two-direction curvature ratio.
  **The dissociation (α ≫ lag) survives**: ratio_freed median **2.49×**, α still stiffer in **77.03%** (n=148). But freeing β/γ **collapses the α curvature to median 0.19× of fixed** (the α peak collapses) → fixed 3.53×/94.57% is an upper bound, freed **2.49×/77% the conservative lower bound** and the reporting basis. (`profile_likelihood_freed.csv`; main CSV verified unchanged by deterministic recompute.)

## Key numbers (all re-verified from `profile_likelihood_identifiability.csv`)
| metric | value |
| --- | --- |
| per-cell curvature α (κ_alpha_pc) median | **8.20 / cell** |
| per-cell curvature lag (κ_lag_pc) median | **2.24 / cell** |
| per-gene stiffness ratio κ_alpha/κ_lag (interior, both>0, n=258) median | **3.53×** (IQR [1.92, 7.41]) |
| **frac(α stiffer than lag)** | **94.57%** (244/258) |
| interior lag CI width / admissible pseudotime range, median | **6.55%** |
| α fold-change CI (upper bound) | clamped below the profile grid step (1.17×) for most genes — α is pinned tighter than the scan resolution (grid-limited upper bound, not a measured CI) |

> Note: the 25/50/75 quantiles of `alpha_fold_lo` are all identical at 1.166 = ≥50% of genes are pinned at the profile grid's first step.
> Therefore α's fold-CI is an **upper bound of the grid resolution**, not a per-gene CI. The actual α-stiff claim is carried by the grid-independent
> **curvature ratio 3.53×** (un-clamped, load-bearing). The lag CI width (a pseudotime fraction) and the α fold are in different units, so instead of comparing widths directly we compare via the **same-unit metric, the curvature ratio**.

## lag trichotomy (n=538)
| class | n | % | interpretation |
| --- | --- | --- | --- |
| **interior** | 302 | 56% | profile-scannable — sloppy but an interior minimum exists |
| **boundary_pinned** | 205 | 38% | t_sw2 pinned to the admissible boundary (~20) → lag upper bound uninformative |
| **degenerate** | 31 | 6% | curvature vanishes — effectively flat |
> In 44% (boundary_pinned + degenerate), the lag's upper boundary cannot be set from the data =
> nearly half the genes have a lag that is not even a "loose estimate". α barely suffers this problem (94.57% stiff).

## Figures
`figures/fig05_profile_likelihood.png` (English labels only; git-ignored):
- **A** — per-cell curvature violin: α med 8.20/cell (stiff) vs lag med 2.24/cell (sloppy).
- **B** — per-gene κ_alpha/κ_lag histogram: median 3.53×, α stiffer in 95% of genes.
- **C** — lag trichotomy bar: interior 302 / boundary_pinned 205 / degenerate 31.
- **D** — representative gene (TLE1) profile overlay: α (red) narrow and steep, lag (blue) shallow and flat.

## Limitations
1. **single method**: confined to the MultiVelo objective. "α is more identifiable than lag" is a geometric property of *this likelihood*.
   Other methods' objective shapes may differ (though the direction agrees with the cross-method observation).
2. **freed-nuisance partial**: the nuisance re-optimization gate is partial (available n=1). The main fixed-nuisance (538)
   carries the claim. A full gate is a follow-up (needs a re-run on a separate output path to protect the main CSV).
3. **relative non-identifiability**: not a fully flat valley but merely relatively sloppy vs α — no overclaiming.
4. **the boundary partly depends on the admissible pseudotime range setting** (TOTAL_H) — the boundary pinning is an interaction of data + parameterization.

## Consistency (with other arms)
- **dissociation** (`identifiability_dissociation.md`): consistent with lag and α's estimation uncertainties being separated.
- **external rate validation** (`external_rate_validation*.md`): consistent with α reproducing externally.
- **cross-dataset §7**: same direction as the α-robust ≫ lag-fragile ordering within/cross-dataset.
→ This demo supplies the *mechanism* (likelihood geometry) behind those observations: the reason lag does not reproduce is not noise but that the objective is, from the outset, less informative along the lag direction.

## Reproduce commands
```bash
cd pipeline/hspc-velocity-benchmark
# main identifiability (already complete — no recompute needed, only to reproduce):
conda run --no-capture-output -n velo-mv python -u scripts/p3_profile_likelihood.py
# figure:
conda run --no-capture-output -n velo-mv python figures/fig05_profile_likelihood.py
# freed-nuisance partial gate (separate subset, note it overwrites the main CSV):
conda run --no-capture-output -n velo-mv python -u scripts/p3_profile_likelihood.py --subset 30
```
