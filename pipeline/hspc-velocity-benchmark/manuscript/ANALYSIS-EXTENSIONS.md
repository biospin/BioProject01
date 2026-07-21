# ANALYSIS-EXTENSIONS — story-strengthening 추가 분석 설계 (2026-07-07)

> research-methodologist 설계 + advisor 리뷰 + novelty-strategist thesis + 즉석 경험 검증(α/β/γ cross-method) 종합.
> **통합 thesis(재프레이밍):** lag은 multiome 스냅샷 + 현 모델군에서 **식별 불가(non-identifiable)** — chromatin에 구속되지 않고(ATAC shuffle 불변), method 간 재현 안 되고, baseline로 예측 안 됨. 반면 **α *만*이 식별 가능한 불변량**(RNA-pinned; ATAC 없는 floor도 ρ≈0.85로 회복). timing 예측은 lag이 아니라 α(day0 ATAC로 회복 가능) 위에 지어야 한다. → MultiVelo 저격이 아니라 data+model-class의 성질이라 desk-reject 방어.

## 경험 검증(이번 세션 즉석, 기존 CSV)
| 파라미터 | floor×MV | floor×VAE | MV×VAE | 판정 |
|---|---|---|---|---|
| α 전사율 | +0.818 | +0.889 | +0.882 | **robust (RNA-pinned)** |
| β splicing | −0.011 | +0.296 | +0.080 | fragile |
| γ degradation | +0.401 | −0.099 | −0.109 | fragile |
| α_c chromatin | — | — | +0.291 | fragile |
→ **PREMISE 수정:** "rate constants robust"는 거짓. **"α만 식별 불변, α_c·β·γ 전부 fragile"** 이 정확·더 강함.

## 스켑틱 리뷰어가 때리는 곳
- **O1(존재론):** "방법이 lag을 못 재거나 데이터에 lag이 없어 null이 무의미." → 양성대조(#2)+등가검정(#1).
- **O2(엄밀):** "0.88 vs 0.05는 eyeball 상관 둘, dissociation 검정 아님." → paired Δρ bootstrap(#1).
- **O3(method 선택):** "나쁜 method 골랐다." → identifiability(#3)+기존 4-dataset 재현.
- 현재 draft은 point ρ+p만, **headline 상관에 CI 없고 α-vs-lag 차이 검정 없음** — 가장 값싸고 큰 공백.

## Ranked (narrative value ÷ cost)

### #1 — paired Δρ dissociation + CI + TOST 등가 [CHEAP; O2·O1절반]
- 가설: `Δρ = ρ_α − ρ_lag > 0`, bootstrap CI가 0 제외; lag은 *0과 등가*.
- 방법: 유전자 paired bootstrap B=10⁴ — 매 resample이 **같은 gene index**에서 ρ_α, ρ_lag 동시 계산 → Δρ percentile CI. **parametric Steiger/Meng 금지**(Spearman rank는 이변량정규 위반) → bootstrap-over-genes. 모든 ρ(α,α_c,β,γ,lag)에 CI, HSPC+4 dataset. **TOST** 사전경계 |ρ|<0.2: lag CI가 [−0.2,+0.2] 안에 완전히 들어가는가 → "0과 등가" 라이선스(p>0.05는 못 함).
- 입력: 기존 CSV(multivelo/multivelovae/rna_only/moflow + 4 external). `p3_concordance.py` 패턴 재분석 1개.
- null: Δρ CI가 0 포함 → 지금 값싸게 re-scope. TOST 실패 → "약하게 robust"로 강등. 어느 쪽이든 더 방어적.

### #2 — 다중 method 양성대조(합성 injected lag) [REFIT, modest GPU; 최고 절대값, O1·O3]
- 기존 `sim_injected_lag.md`는 **CRAK DTW 하나만**(smooth kinetic에서 sign 반전) — 한 estimator 진술이지 identifiability/cross-method 진술 아님.
- 가설: lag이 식별 가능할 때(sharp switch·고SNR) 독립 method들이 **일치**; smooth/저SNR(실 HSPC 대응)에서만 갈림 → 네거티브는 **regime-specific**.
- 방법: 합성 생성기 1개(#3와 공유): 알려진 α,α_c,β,γ + 주입 lag의 chromatin→RNA ODE, **SNR × switch-sharpness** sweep. lag 정의가 가장 가까운 **MoFlow fastdtw + MultiVelo switch-time** 2종에 통과(VAE 선택). **CRAK estimator 읽지 않음**(smooth artifact 기지). sweep 칸마다 cross-method concordance + ground-truth 회복.
- 부수효과(advisor): permutation-FDR "0/598"의 **검정력 보정** — 알려진 concordant lag 주입 시 FDR 기계가 잡아내는지 → "effect size X에서 concordance 검출력 입증된 0/598"은 citable, "0/598" 단독은 아님.
- 비용: 합성-입력 harness — 진짜 비용은 **format plumbing**(합성 c/u/s를 MultiVelo chromatin채널+latent-time / MoFlow 포맷). GPU 소량. `mv`/`torch` env.
- null: sharp에서도 method 불일치 → 오히려 **더 강한 비식별** 주장. sharp positive control로 설계하고 이쪽으로 설계하지 말 것.

### #3 — identifiability: param-recovery + 랭킹 + γ/β 비 [CHEAP + #2 무임승차; O3·메커니즘]
- profile-likelihood는 MultiVelo objective/Hessian 노출 필요(내부 취약) → **parameter-recovery**로 재구성(#2 harness에서 scatter 자동).
- **3a[CHEAP] 경험 식별성 랭킹:** 모든 kinetic param을 cross-method concordance로 순위("재현성=경험적 식별성 proxy"). 이미 계산: α +0.88 ≫ α_c +0.29 > β +0.08 > γ −0.11 → **α 단독**.
- **3b[CHEAP] γ/β 비 — sloppiness probe:** splicing ODE는 정상상태 기울기 γ/β + scale만 식별. γ/β 비 concordance vs 개별 β·γ. 비는 재현되는데 개별은 안 되면 = 교과서 scVelo scaling 비식별, 무료.
- **3c[FREE·#2]:** 회복-vs-참 scatter(α 대각선, 나머지 degenerate).

### #4 — 양성 생물학 salvage: priming marker "예외가 규칙을 증명" [CHEAP; nihilism 방어]
- 가설: priming 신호가 생물학적으로 강한 canonical marker에서는 chromatin-lead 방향이 cross-method 재현.
- 방법: marker set **사전 선언·동결**(CSF1R,S100A9,MPO,ELANE,AZU1,LYZ,GATA2,ITGA2B,VWF,IRF8…). 무작위 동일크기 gene-set permutation 대비 sign-agreement/concordance 상승 검정. `bootstrap_stability`(sign_flip<0.10)과 교집합 선택.
- **지뢰:** 모든 sign/FDR 검정은 **MoFlow × VAE 만** — MultiVelo의 구조적 상수-양수 sign 절대 금지(CRAK 의존 0/598 재생산). MultiVelo는 크기/rank에만 참여.
- null: marker조차 enrichment 없으면 주장 폐기 → 네거티브가 더 깔끔.

### #5 — cross-dataset 재현 방어적 CI (monotonicity headline 거부) [CHEAP]
- cross-dataset α ρ(0.55/0.475/0.32)+lag에 bootstrap 95% CI → **CI 겹침 → 순서는 정성적**.
- 후보(e) "monotonicity 정량화" **거부** — 3점에 divergence-time 회귀는 overfit, 리뷰어가 간파. CI/caveat만.

### 무료 add-on(#1 스크립트에 병합): "lag = 두 잡음 timing의 차" 분산예산
- lag은 **적당히 식별된 두 양의 차**(t_sw2−t_sw1, 또는 1/α_c−1/α); 차분은 노이즈 증폭. 성분들 concordance vs 차의 concordance 비교 → 성분은 중간, 차는 ≈0 붕괴 → 보편적 설명("두 잡음 timing 빼기"), 무비용, α_c-상속 논증 보완.

## 외부검증(advisor #2, 재해석)
- **γ vs 빌려온 mRNA t½**(proxy-join, t½=ln2/γ): 원래 "free external validation"이나 γ가 method-fragile로 확인됨 → "외부 ground truth 있는 γ조차 신뢰 회복 안 됨, α만 식별"의 일부로 재프레이밍. floor γ(floor×MV +0.40)로 t½ 대조 시도는 여전히 유효(어느 method가 실측 분해율 회복하나).
- **α vs SLAM/4sU/Pol II**(literature-scout DATA-HUNT 대기): 있으면 α 외부검증 최강.

## 지연/하위
- optimizer-vs-model α_c 분해 — multi-seed refit 필요. 단 `bootstrap_refit_pergene.csv`에 within-method α_c 분산이 이미 있으면 CHEAP로 승격, 먼저 확인.
- 2차 ATAC-shuffle 대조 — **이미 done**(`scrambled_null_moflow.md`, MoFlow lag shuffle 생존). 인용만.
- 약물 arm — 원 P5 목표, 신규데이터·timing ground truth 없음. future work, gap 정직 정량.

## Sequencing
1. **#1 먼저** — headline 통계+게이트(Δρ CI 0 포함 시 re-scope); #3a/#3b/#5가 소비할 CI 생산.
2. **#3a+#3b+분산예산** — 같은 재분석 pass.
3. **#2** — 유일하게 할 값어치 있는 REFIT; #3c 무임승차. O1/O3 flagship.
4. **#4** → **#5**(#1 bootstrap과 묶음).

## Guardrails
- sign 검정은 {MoFlow, VAE}만; CRAK은 sensitivity 전용·합성대조 readout 금지.
- 모든 headline ρ에 bootstrap CI.
- "lag not robust"는 *등가(equivalence)*로, failure-to-reject 아님.
- cross-dataset 재현 각 1샘플 → 4축 일관성으로만, 강한 일반화 금지.

## 데이터 가용성(확인됨)
- α/β/γ: floor+MV+VAE (HSPC + 3 external). α_c: MV+VAE만. MoFlow/CRAK CSV는 `cs_lag_*`만(rate 컬럼 없음) → #3은 MV/VAE/floor로 제한, #2는 MoFlow를 합성데이터에 *fit*해야(CSV 읽기 불가).
