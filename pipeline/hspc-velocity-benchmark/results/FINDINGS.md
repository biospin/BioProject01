# FINDINGS — HSPC velocity 벤치마크 결과·해석 종합

> **이 문서는 결과와 해석의 canonical 종합본이다.** 개별 분석 md(`concordance.md`, `h1_lag_diagnostic.md`,
> `scrambled_null.md`, `confound.md`, `cellcycle_genelevel.md`, `lineage_lag.md`)에 상세 근거를 명시하고,
> 여기서는 그것들을 연구 질문에 맞춰 한 줄로 결과+해석으로 묶고 통합 결론을 낸다.
> 새 분석이 끝날 때마다 갱신한다. 진행 상태는 `../PROGRESS-LIVE.md`, 현황은 `../../../HANDOFF.md`.
> 최종 갱신: **2026-07-09** (§8 profile-likelihood 실질 식별성: `profile_likelihood_identifiability.md` — lag-fragile/α-robust를 목적함수 성질로 승격).

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
| **4-way H1** (+CRAK-Velo) | ✅ | `concordance.md` §3.5 + `crakvelo_sign_check.md` |
| permutation FDR (P4) | ✅ | `permutation_fdr.md` |
| **clean concordance gate** (CRAK-비의존 재계산, MultiVelo sign 방법론 정정) | ✅ | `clean_concordance_gate.md` |
| **MoFlow-subset held-out 대질** (held-out MVVAE + ATAC-shuffle 인과통제) | ✅ | `moflow_subset_confrontation.md` |
| accuracy arm — injected-lag simulator | ✅ | `sim_injected_lag.md` |
| bootstrap lag-sign stability | ✅ (표집-하한) | `bootstrap_stability.md` |
| P5 baseline→timing 모델 (held-out lineage, Mc proxy) | ✅ (prototype) | `lag_model.md` |
| **per-lineage refit** (5 lineage 따로 fit, cross-lineage lag 일치도) | ✅ | `lineage_refit.md` |
| **실제 day0 ATAC feature 어셈블 + 모델** | ✅ | `atac_baseline_features.md` + `lag_model_atac.md` |
| **cross-dataset replication** (human_brain + E18 mouse brain + human BMMC + macrophage) | ✅ | `concordance_human_brain.md` + `concordance_e18_mouse_brain.md` + `concordance_GSE194122_bmmc.md` + `concordance_macrophage.md` |
| **α_c 전체-refit bootstrap stability** (B=12, 485 gene 재fit) | ✅ | `bootstrap_refit.md` |
| **profile-likelihood 실질 식별성** (§8, MultiVelo 목적함수 곡률비 α vs lag) | ✅ | `profile_likelihood_identifiability.md` |
| drug perturbation arm | ⬜ 대기(데이터) | — |

---

## ★ 통합 결론 (현재까지)
**chromatin→transcription lag은 gene 수준에서 method-robust한 양이 아니다.** 크기·방향 모두 method 간
일치도가 높지 않으며(H1 실패 — **CRAK-비의존 clean headline**: 3-method magnitude concordance |ρ|≤0.08 {mv×moflow −0.04, mv×mvvae −0.01, moflow×mvvae +0.08} + 2-method sign-agreement 48%≈chance. permutation-FDR **agreement-set 0/598은 부호 가변 method 3개가 필요해 CRAK 포함 시에만 정의된다 → CRAK에 의존하므로 대표 결과에서 빼고 CRAK 민감도 분석(보조)으로 다룬다**; 2026-07-05 `clean_concordance_gate.md`), 음성대조는 한 method(MultiVelo)의 lag가
chromatin 신호가 아니라 모델 구조에서 나옴을 입증했다. **(a) 전사율 α(method 간 ρ=0.88), (b) 집단 수준 방향 균형(~50/50, 두 method 수렴), (c) canonical priming marker 방향(method 간 일치)만이 robust 했다.**
→ drug-timing 모델은 lag을 단일 method 값으로 쓰면 안 되고, **method 불확실성을 명시적으로 반영**해야 한다.
이 'α > lag' 순서는 **네 외부 데이터셋(성인 human_brain·태아 E18 mouse brain·same-tissue human BMMC·HSPC-직계 macrophage)에서도 보존된다**(§7). 이는 HSPC 한 데이터셋에서만 나온 우연이 아니다. cross-dataset α는 조직이 멀수록 순서대로 낮아지지만(단조 감소; HSPC-직계 macrophage +0.643 > BMMC +0.55 > human_brain +0.475 > E18 +0.32) lag은 어디서도 무신호다(+0.05~+0.19).
게다가 이 'α > lag' 순서는 **MultiVelo 목적함수 자체를 뜯어봐도 확인된다**(§8). 목적함수(우도)를 α 값 쪽으로 흔들면 점수가 급격히 나빠지지만(α는 데이터로 잘 정해진다), lag 쪽으로 흔들면 점수가 거의 변하지 않는다(lag은 데이터로 잘 정해지지 않는다). 유전자별로 α 쪽 민감도가 lag 쪽보다 중앙값 **3.53×** 크고, α가 더 민감한 유전자가 **94.57%**다. 즉 lag이 method 간 재현되지 않는 것은 잡음이 아니라 목적함수가 애초에 lag을 데이터로 잘 결정하지 못하기 때문이며, 관찰이 메커니즘으로 설명된다.

---

## 발견별 결과·해석

### 1. H1 — cross-method lag 일치도: **약함/실패**
- **lag 크기 무상관**: pairwise Spearman multivelo×moflow **−0.04**(p=0.38), multivelo×multivelovae **−0.01**(p=0.81),
  moflow×multivelovae **+0.08**(p=0.04). 정의를 apples-to-apples로 통일해도 **+0.12**에 그친다(`h1_lag_diagnostic`).
- **방향 ~50/50**: 부호 가변 method 모두 chromatin-leads 비율 MoFlow **44.8%** / MultiVeloVAE **49.3%** → 전역
  'chromatin이 transcription을 prime한다' **데이터 미지지**. (MultiVelo 100%는 switch-time 단조정렬(스위치 시점을 순서대로 정렬) 모델 제약이 만든 아티팩트다.)
- **gene 수준 방향 불일치**: moflow×multivelovae sign-agreement은 **48%**로 우연 수준이다.
- **4-way 확장(+CRAK-Velo)**: CRAK-Velo lag 부호 버그(`dtw_lag`이 MoFlow `fastdtw`와 반대) **검증·수정**(`crakvelo_sign_check.md`) 후
  moflow×crakvelo Spearman **−0.151**, crakvelo×multivelovae **−0.04** — 4번째 method를 넣어도 무상관이거나 약한 음의 일치를 보인다. CRAK-Velo도 chromatin-leads가 **41.1%**로 균형이다.
  단 canonical priming marker(CSF1R·S100A9 등)는 두 method 모두 chromatin-leading(양수)으로 **일치** → 강건한 건 marker뿐.
- **permutation FDR(P4) 통계 확증**(`permutation_fdr.md`, N=10⁴): (A) cross-method ρ은 2/3 쌍이 gene-label shuffle null 대비 유의하나 **effect가 극약하고(|ρ|≤0.15) 방향이 불일치한다**.
  (B) per-gene cross-method sign-consistency **agreement-set = 0/598 gene**(FDR<0.10) → **공집합**. 어떤 gene도 method 간 lag 방향이 무작위 이상으로 일관되지 않는다.
- **⚠️ clean-gate 정정(2026-07-05, `clean_concordance_gate.md`)**: (B)의 0/598은 부호 가변 method 3개(moflow, **crakvelo**, mvvae)를 요구한다. MultiVelo lag은 구조적 100% 양수(switch-time 단조정렬)라 *sign*-consistency 검정에 넣을 수 없고(null 오지정), 따라서 clean 부호 가변 method는 {moflow, mvvae} 2개뿐 → 2-method sign FDR은 min p_perm≈0.50으로 **원리적 power-bound(신호 무관 0)**. 즉 **0/598은 본질적으로 CRAK-의존** → **CRAK 민감도 arm으로 강등**. **CRAK-비의존 clean headline은 magnitude concordance**(clean 3-way |ρ|≤0.08, verify-gate `p3_concordance.py`가 재계산) + 2-method sign-agreement 48%(chance). MultiVelo는 sign이 아니라 magnitude/rank 검정에만 참여(lag 크기는 gene간 변이 有). *reframe이지 method-swap이 아님* — {mv,moflow,mvvae}로 sign 검정 재실행 금지(상수-부호 오류 재도입).
- **근원 진단**: lag을 결정하는 **chromatin opening rate α_c가 method-민감**(ρ=0.29)인 반면 전사율 α는 강건하다(ρ=0.88).
  → lag이 α_c의 method 민감성을 그대로 상속.
> 해석: "어느 gene이 chromatin 선행인지"는 method를 바꾸면 달라진다(비robust, 4-way·FDR로 확증). 단 집단 수준 방향 균형 + canonical marker는 method 간 수렴한다(robust).

### 2. 음성대조 — chromatin은 MultiVelo lag을 구동하지 않음
- ATAC를 within-lineage 셔플(chromatin↔RNA 결합 파괴) 후 재fit → lag 분포 원본과 **통계적으로 동일**
  (Mann–Whitney p=0.20, KS p=0.51), per-gene lag **ρ=0.72** 보존, chromatin likelihood 0.239→0.237(불변).
- 단 Wilcoxon paired p=0.0003 (median 5.87→5.48 소폭 감소)은 chromatin의 **marginal 기여**만 나타낸다.
> 해석: MultiVelo lag은 chromatin 신호가 아니라 **모델 구조(switch-time 순서)·gene 고유 RNA 동역학**에서 나온다.
> §1의 'MultiVelo 100% chromatin-leads = 아티팩트' 결론을 음성대조로 독립적으로 확증한다.

### 3. Confound — lag 결론 비편향
- **cell-cycle**: 세포 수준 ρ≈0.33–0.36(S/G2M score vs expr)이지만 **gene 수준은 비편향** — fit lag gene 중
  CC gene 1.9%(10개), CC lag vs 나머지 Mann-Whitney p=0.86, CC 제외 시 median 변화 0.037. 세포 수준 ρ이 이렇게 나오는 까닭은
  **cycling이 lineage와 강결합**(MK 88%↔HSC 3%)이기 때문이고, within-lineage 분석이 이미 이를 통제한다. → **global regress_out 미수행**(분화신호 제거 위험).
- **burst**: lag↔α Spearman −0.24(중간, |ρ|<0.5 → 허용; regularized 회귀 시 반영).
- **ambient/doublet**: scrublet 적용, doublet median 0.045, pct_mito median 10.4%(QC max 20%) — 정상이다.

### 4. Within-lineage lag 분포 (참고, 전역 fit 기반)
- MultiVelo lag median은 lineage별 4.3–7.4 pseudotime이다(Erythroid 최저, Lymphoid 최고). 전부 100%>0이다(§1 구조 caveat).
- ⚠️ 전역 fit을 dominant-expression으로 귀속한 근사이며, **실제 within-lineage 일치도는 per-lineage refit이 필요하다**(대기).
- rare lineage(MK/Baso·Eo·Mast/pDC) uncertainty는 별도로 다룬다.

### 5. lag의 robustness 3각 검정 — accuracy·stability·predictability (2026-07-01)
- **(accuracy) injected-lag simulator** (`sim_injected_lag.md`, **2026-07-01 스코프 정정**): 잡음 없는 조건에서 Spearman(true,rec)은 **−0.89**이다.
  ⚠️ 이는 "순위 회복 실패"가 **아니다** — |ρ|=0.89는 estimator가 true-lag 순위를 **강하게 추적**한다는 뜻이다. 문제는 **부호 반전 + 크기 붕괴**다(과소추정 0.06×, kinetic 설정 전반 일관 음수, sign+ 24~78% shape-의존).
  즉 **crakvelo manual-DP DTW construct가 매끄러운 동역학에서 부호·크기를 왜곡**하는 shape-아티팩트이지 "lag은 원리적으로 recover 불가"가 아니다. **스코프: 이 arm은 crakvelo estimator만 테스트 → CRAK-Velo lag을 cross-method 비교에서 신뢰하지 말라는 근거**. 핵심 H1(moflow×multivelo×mvvae, α robust)은 이 construct 미사용 → 독립 생존.
- **(stability) bootstrap lag-sign** (`bootstrap_stability.md`): fit 고정·cell 복원추출에선 부호가 83% 안정이다(median flip 0).
  단 **가장 약한 안정성**(표집 잡음만) — cross-method·정확도 비robust와 모순은 아니다. 실제 re-fit stability는 더 낮을 것이다.
- **(predictability) baseline→timing 모델** (`lag_model.md`): 순수 baseline chromatin feature(HSC/MPP 접근성·dynamic-range)만으로는
  lag을 lineage 간 예측하지 못한다(held-out ρ=**−0.21**). +fit kinetic feature 넣으면 ρ=+0.59지만 이는 **순환**이다(fit_alpha_c가 MultiVelo lag을 기계적으로 결정).
  → drug-timing 모델은 단일 lag 값이 아니라 baseline feature 자체·α를 써야 함을 모델 수준에서 확인.
> 종합: lag은 *한 fit 안에선 표집-안정*하지만 **method-비robust(H1·P4) + baseline 비예측(P5)**이다. (accuracy arm은 crakvelo construct의 shape-왜곡을 보인 것이지 "lag 원리적 회복 불가"가 아니라 "그 construct를 cross-method에서 신뢰 말라"는 뜻이며, 핵심 H1은 독립이다.)

### 6. cross-lineage lag 일치도 + 실제 day0 ATAC feature (2026-07-01)
- **(within-method, cross-lineage) per-lineage refit** (`lineage_refit.md`): 5개 terminal lineage를 root∪L로 **따로 fit한다**.
  cross-lineage lag magnitude Spearman ρ median=**0.349**(범위 0.234~0.513, 양수 10/10) = **약함/경계**다. 대조군 α_c는 ρ median=**0.483**(더 robust) → H1 패턴(α robust > lag)이 lineage 축에서도 재현. 전역 fit과의 ρ 0.23~0.46 → 전역 fit이 lineage 신호를 뭉갬(refit 정당).
- **(실제 ATAC feature)** `atac_baseline_features.md`: crakvelo 197,482 peak에서 **day0 HSC/MPP 8,583 세포** 기준 gene별 promoter(±2kb)/enhancer(±100kb distal) 접근성 어셈블(511 gene) → §5 한계 ①(moflow Mc smoothed proxy) 해소.
- **(예측가능성 이중 대조)** `lag_model_atac.md`: 같은 baseline feature·모델로 held-out lineage 예측 —
  **robust α는 실제 ATAC로 예측된다(ρ=+0.309, 6 lineage 전부 양수)**, Mc proxy(−0.089)는 실패한다. 반면 **비robust lag은 ATAC로도 비예측(ρ=+0.05≈chance)**이다.
  → **같은 feature가 robust target(α)은 예측하고 비robust target(lag)은 못 한다** = H1이 *예측가능성* 축에서도 재확인 + day0 ATAC 어셈블의 가치 입증. atac+mc(+0.285)가 ATAC 단독을 못 넘음 → Mc proxy는 추가 정보 없음.

### 7. cross-dataset replication — 다른 조직·종에서 'lag-fragile / α-robust' 재현 (2026-07-06)
HSPC 한 데이터셋에서만 나온 산물이 아님을 **네 외부 multiome**으로 검정한다(same-tissue human BMMC·HSPC-직계 macrophage 포함). **핵심은 절대값이 아니라 α > lag 순서의 보존이다.**
- **(A) human_brain (성인 뇌 multiome, HSPC↔human_brain MultiVelo)** `concordance_human_brain.md`:
  cross-dataset α rank Spearman **+0.475**(재현✅, p=4.5e-7) vs lag 크기 rank **+0.185**(약함, p=0.06). floor timing +0.002(sanity). → α는 데이터셋을 넘어 rank 보존, lag은 안 됨.
- **(B) E18 mouse brain (태아 뇌 multiome, MultiVelo 튜토리얼 데이터)** `concordance_e18_mouse_brain.md`:
  - **within-E18 cross-method α**(floor×MV×VAE, 같은 gene축): Spearman 0.78 / 0.81 / **0.90**(중앙값 **+0.81**) — HSPC의 α-robust leg(ρ=0.88)이 비-조혈에서 **강하게 재현된다**.
  - **within-E18 lag 크기 rank**(MV×VAE): **+0.057** — lag-fragile leg를 재현한다(HSPC MV×VAE −0.01과 정합).
  - **cross-dataset HSPC↔E18**(mouse→UPPER 매핑 후 shared 132): α rank **+0.32**(p=2e-4) vs lag 크기 rank **+0.10**(p=0.23), floor α sanity +0.40.
- **(C) human BMMC (GSE194122, donor09/site4, HSPC와 같은 조혈 축 — same-tissue 최근접 재현, 우리가 GEX BAM velocyto로 spliced/unspliced 복구)** `concordance_GSE194122_bmmc.md`:
  - **within-BMMC cross-method α**(floor×MV×VAE, 같은 gene축): Spearman +0.82 / +0.85 / **+0.91**(중앙값 **+0.851**) — α-robust leg가 **같은 조직에서 가장 강하게 재현된다**(HSPC ρ=0.88과 정합).
  - **within-BMMC lag 크기 rank**(MV×VAE): **−0.088**(p=0.15) — lag-fragile leg를 재현한다(HSPC MV×VAE −0.01, E18 +0.06과 정합).
  - **cross-dataset HSPC↔BMMC**(human↔human, SYMBOL 직접 매칭 shared 88): α rank **+0.550**(p=2.9e-8) vs lag 크기 rank **+0.052**(p=0.63), floor α sanity +0.558. → same-tissue라 human_brain·E18보다 cross-dataset α가 강함(0.55).
- **(D) macrophage differentiation (GSE284047·figshare 30280333, Day14 HSPC 직계 분화 — 가장 가까운 조직축; figshare postpro가 raw spliced/unspliced 보유 nnz 35.6% → 공통 전처리 분기)** `concordance_macrophage.md`:
  - **within-macrophage cross-method α**(floor×MV×VAE, 같은 gene축): Spearman +0.826 / +0.865 / **+0.917**(중앙값 **+0.865**) — α-robust leg가 **4개 외부 중 가장 강하게 재현**.
  - **within-macrophage lag 크기 rank**(MV×VAE): **+0.074**(TOST |ρ|<0.2 → 0과 등가) — lag-fragile leg 재현.
  - **cross-dataset HSPC↔macrophage**(human↔human, SYMBOL 직접 매칭 shared 274): α rank **+0.643**(95%CI [+0.554,+0.719], p=2.5e-33) vs lag 크기 rank **+0.148**(95%CI [+0.027,+0.263], p=0.014), floor α sanity +0.677. HSPC 직계라 **cross-dataset α가 넷 중 최고**. Δρ=ρ_α−ρ_lag=**+0.843**(95%CI [+0.773,+0.912], 0 배제=dissociation). ✅ canonical numpy(B=10000, seed=20260707) 확정(2026-07-10).
> 판정: **within-dataset에선 α-robust/lag-fragile 순서가 강하게 재현**(macrophage within α 0.865 ≫ lag 0.07; BMMC within α 0.85 ≫ lag −0.09; E18 within α 0.81 ≫ lag 0.06)되고, **cross-dataset α는 조직 거리에 단조 감쇠하나 lag은 어디서도 무신호**: HSPC-직계 macrophage α **+0.643** > same-tissue human BMMC **+0.55** > 성인 human_brain **+0.475** > cross-species E18 **+0.32**, 반면 lag은 네 축 모두 +0.05~+0.19 잡음이다. 즉 "α가 종을 넘어 보존된다"는 강한 주장이 아니라 **"어느 데이터셋에서 재도, α가 lag보다 method·데이터셋에 robust하다"는 순서 진술**이 5개 축(HSPC + human_brain + E18 + BMMC + macrophage)에서 일관된다.
> ⚠️ 정직 caveat: lag-fragile leg는 within-dataset에서 **단일 method 쌍(MV×VAE)에만 근거한다**(BMMC·E18·macrophage 모두 MoFlow/CRAK 미실행 → HSPC 3쌍보다 얇음). 네 replication 모두 각 1 donor/샘플 — 강한 일반화 금지, 다섯 축 일관성으로만 서사한다. BMMC ATAC는 processed peak matrix의 gencode-proximity 집계다(HSPC의 mv.aggregate_peaks_10x와 구현 상이 → cross rank에 보수적 잡음). macrophage p·CI는 canonical numpy(B=10000) 확정(2026-07-10, §7-D).

### 8. profile-likelihood 실질 식별성 — 'lag-fragile / α-robust'를 목적함수 성질로 입증 (2026-07-09)
cross-method/cross-dataset의 관찰(§1·§6·§7)이 *왜* 생기는지를 MultiVelo **자기 목적함수** 위에서 검정한다. fixed-nuisance profile likelihood를 α 방향과 lag(=t_sw2−t_sw1) 방향으로 각각 스캔한다(latent time 재최적화, n=538 gene; `p3_profile_likelihood.py`, fit·likelihood 재현 r≈1.0).
- **α는 stiff, lag은 sloppy**: per-cell 곡률 median α **8.20/cell** ≫ lag **2.24/cell**. gene별 stiffness 비 κ_alpha/κ_lag(interior both>0, n=258) median **3.53×**(IQR [1.92, 7.41]), **α가 lag보다 stiff한 gene 94.57%**(244/258).
- **lag trichotomy(n=538)**: interior 302(56%) / boundary_pinned 205(38%) / degenerate 31(6%). 즉 **44%에서 lag은 admissible 경계에 눌리거나 곡률 소실** → 데이터로 상한조차 못 정함. interior lag CI 폭/admissible range median **6.55%**(α-vs-lag 비교는 같은 단위 지표인 곡률비 3.53×로 함).
- **판정**: MultiVelo 목적함수는 **lag 방향으로 실질적으로 비식별(평탄에 가깝고 boundary-limited), α 방향으로 식별 가능(sharp)**이다. lag이 재현 안 되는 것은 잡음이 아니라 우도가 lag 방향으로 애초에 덜 정보적이기 때문이다. **상대적(practical) 비식별성**이며 완전 평탄 valley는 아니다(정직 framing). dissociation·external rate validation과 정합 → 관찰이 메커니즘으로 승격.
- **스코프/한계**: MultiVelo 단일 method의 우도 기하; freed-nuisance 게이트(β/γ/α_c/rescale/scale_cc 재최적화)는 **부분(사용가능 n=1)** — main fixed-nuisance(538)가 주장을 담당한다. (`results/profile_likelihood_identifiability.md`, `figures/fig05_profile_likelihood.png`)

---

## drug-timing 목표(P5)와의 연결
- **쓸 수 있는 robust 신호**: 전사율 α(method 간 ρ=0.88), 집단 수준 방향 균형이다.
- **그대로 쓰면 안 되는 것**: gene별 lag 크기·방향이다(method 민감). baseline feature로 넣으려면 method 불확실성을
  uncertainty로 모델에 반영하거나, α_c 추정 안정화(bootstrap/per-lineage) 후 사용한다.
- 4-way H1(CRAK-Velo 추가) + permutation FDR로 이 결론의 견고성을 **확증 완료** — 4번째 method·permutation null에서도 lag 일치도는 약하고 agreement-set은 공집합이다.
- §5 3각 검정(accuracy·stability·predictability)로 추가 확증: **baseline chromatin으로 lag 비예측(held-out ρ=−0.21)** + accuracy arm은 crakvelo construct가 shape-의존 왜곡(cross-method 신뢰 불가 근거) → "lag을 단일 값으로 쓰지 말라"가 모델 수준에서도 성립. baseline feature·α 중심 + bootstrap 안정 gene 한정이 다음 방향이다.
- §6에서 **실제 day0 ATAC feature로 α(robust)는 held-out lineage 예측됨(ρ=+0.31)**을 확인 → drug-timing 모델의 입력은 lag이 아니라 **day0 ATAC promoter/enhancer 접근성 → α** 경로로 가는 것이 데이터로 지지됨. 다음은 drug perturbation arm(timing ground truth)으로 이 proxy 경로를 검증한다.

## 핵심 한계
1. **Pseudotime ≠ wall-clock**: day0/day7 batch 통합 → lag은 pseudotime 단위. wall-clock anchor는 불가하다(H2 강등).
2. lag 정의가 method마다 다름(switch-timing vs rate-timescale vs DTW) → 비교는 rank·sign 분리 보고.
3. 전역 fit 기반이다(per-lineage refit 미완). bootstrap stability는 미완이다.
4. ~~음성대조는 MultiVelo 단일 method~~ → **해소(2026-07-06)**: MoFlow(구조 독립 2번째 method)로 ATAC-shuffle 음성대조 확장 완료(`scrambled_null_moflow.md`). MoFlow lag도 셔플 생존(per-gene ρ=0.52 ≫ method-swap ρ=0.08, chromatin-채널 fit-quality 불변) → "lag은 model-structural, not chromatin-driven"이 두 method로 일반화. (CRAK-Velo scramble은 후속이다.)

---

# FINDINGS — HSPC velocity benchmark: consolidated results & interpretation

> **This document is the canonical consolidation of results + interpretation.** The individual analysis mds (`concordance.md`, `h1_lag_diagnostic.md`,
> `scrambled_null.md`, `confound.md`, `cellcycle_genelevel.md`, `lineage_lag.md`) are the detailed evidence; here we bundle them
> into one-line result+interpretation entries aligned to the research questions and draw an integrated conclusion.
> Updated whenever a new analysis finishes. Progress status in `../PROGRESS-LIVE.md`, current status in `../../../HANDOFF.md`.
> Last updated: **2026-07-10** (§7 4th external: **`concordance_macrophage.md` (HSPC-직계 macrophage added)** — canonical numpy CI 확정; 앞 3종: `concordance_human_brain.md`, `concordance_e18_mouse_brain.md`, `concordance_GSE194122_bmmc.md`).

## Research question (goal)
Quantify per-gene **chromatin→transcription lag** (activation/shutdown timing difference) so that baseline epigenomic
features can **predict epigenetic drug response timing**. Primary dataset = Human HSPC 10x Multiome
(GSE209878, day0+day7 integrated, 21,878 cells). As a prerequisite, we first run a **velocity method head-to-head benchmark**
to test "is lag a method-robust quantity" (H1).

## Analysis status
| Analysis | Status | Output |
|---|---|---|
| 3-way H1 (multivelo×moflow×multivelovae lag concordance) | ✅ | `concordance.md` §1.5/§3.5/§3.6 |
| H1 lag no-correlation diagnostic (definition consistency) | ✅ | `h1_lag_diagnostic.md` |
| scrambled-chromatin negative control | ✅ | `scrambled_null.md` |
| confound (cell-cycle/burst/ambient) | ✅ | `confound.md` + `cellcycle_genelevel.md` |
| within-lineage lag distribution | ✅ | `lineage_lag.md` |
| **4-way H1** (+CRAK-Velo) | ✅ | `concordance.md` §3.5 + `crakvelo_sign_check.md` |
| permutation FDR (P4) | ✅ | `permutation_fdr.md` |
| **clean concordance gate** (CRAK-independent recomputation, MultiVelo sign methodology correction) | ✅ | `clean_concordance_gate.md` |
| **MoFlow-subset held-out confrontation** (held-out MVVAE + ATAC-shuffle causal control) | ✅ | `moflow_subset_confrontation.md` |
| accuracy arm — injected-lag simulator | ✅ | `sim_injected_lag.md` |
| bootstrap lag-sign stability | ✅ (sampling lower-bound) | `bootstrap_stability.md` |
| P5 baseline→timing model (held-out lineage, Mc proxy) | ✅ (prototype) | `lag_model.md` |
| **per-lineage refit** (5 lineages fit separately, cross-lineage lag concordance) | ✅ | `lineage_refit.md` |
| **real day0 ATAC feature assembly + model** | ✅ | `atac_baseline_features.md` + `lag_model_atac.md` |
| **cross-dataset replication** (human_brain + E18 mouse brain + human BMMC + macrophage) | ✅ | `concordance_human_brain.md` + `concordance_e18_mouse_brain.md` + `concordance_GSE194122_bmmc.md` + `concordance_macrophage.md` (points final · canonical CI pending) |
| drug perturbation arm | ⬜ waiting (data) | — |
| α_c full-refit bootstrap stability | ⬜ waiting (GPU) | — |

---

## ★ Integrated conclusion (so far)
**chromatin→transcription lag is not a method-robust quantity at the gene level.** Both magnitude and direction disagree across
methods (H1 failure — **CRAK-independent clean headline**: 3-method magnitude concordance |ρ|≤0.08 {mv×moflow −0.04, mv×mvvae −0.01, moflow×mvvae +0.08} + 2-method sign-agreement 48%≈chance. permutation-FDR **the agreement-set 0/598 requires 3 sign-variable methods, so it is defined only when CRAK is included → demoted to a CRAK sensitivity arm**; 2026-07-05 `clean_concordance_gate.md`), and the negative control showed that one method's (MultiVelo) lag
comes from model structure rather than from the chromatin signal. **What is robust is only (a) transcription rate α (cross-method ρ=0.88), (b) population-level directional balance (~50/50, two methods converge), (c) canonical priming-marker direction (agrees across methods).**
→ the drug-timing model must not use lag as a single-method value, and must **explicitly reflect method uncertainty**.
This 'α > lag' ordering is **preserved across four external datasets (adult human_brain · fetal E18 mouse brain · same-tissue human BMMC · HSPC-direct macrophage)** as well (§7). This is not a coincidence arising from the single HSPC dataset alone. Cross-dataset α is monotone with tissue distance (HSPC-direct macrophage +0.643 > BMMC +0.55 > human_brain +0.475 > E18 +0.32), whereas lag is signal-free everywhere (+0.05~+0.19).
Moreover this ordering is **promoted to *proven* by the geometric properties of MultiVelo's own objective function** (§8): via profile-likelihood, α is stiff (identifiable) while lag is sloppy + boundary-limited (median per-gene κ_alpha/κ_lag **3.53×**, α more stiff in **94.57%** of genes). That is, lag failing to reproduce is not noise — it is because the objective function is inherently less informative in the lag direction; the observation is backed by mechanism.

---

## Results & interpretation by finding

### 1. H1 — cross-method lag concordance: **weak/failure**
- **lag magnitude uncorrelated**: pairwise Spearman multivelo×moflow **−0.04** (p=0.38), multivelo×multivelovae **−0.01** (p=0.81),
  moflow×multivelovae **+0.08** (p=0.04). Even after unifying the definition apples-to-apples, only **+0.12** (`h1_lag_diagnostic`).
- **direction ~50/50**: among all sign-variable methods, chromatin-leads fraction MoFlow **44.8%** / MultiVeloVAE **49.3%** → the global
  claim 'chromatin primes transcription' is **not supported by the data**. (MultiVelo 100% is an artifact of the switch-time monotone-ordering model constraint.)
- **gene-level direction disagreement**: moflow×multivelovae sign-agreement **48%** (chance).
- **4-way extension (+CRAK-Velo)**: after **verifying·correcting** the CRAK-Velo lag sign bug (`dtw_lag` had opposite sign to MoFlow `fastdtw`) (`crakvelo_sign_check.md`),
  moflow×crakvelo Spearman **−0.151**, crakvelo×multivelovae **−0.04** — adding a 4th method still gives uncorrelated/weak-negative agreement. CRAK-Velo also chromatin-leads **41.1%** (balanced).
  But the canonical priming markers (CSF1R·S100A9 etc.) are chromatin-leading (positive) in both methods and **agree** → only the markers are robust.
- **permutation FDR (P4) statistical confirmation** (`permutation_fdr.md`, N=10⁴): (A) cross-method ρ is significant vs the gene-label shuffle null for 2/3 pairs, but the **effect is extremely weak (|ρ|≤0.15) and directionally inconsistent**.
  (B) per-gene cross-method sign-consistency **agreement-set = 0/598 genes** (FDR<0.10) → **empty set**. No gene has cross-method lag direction consistent beyond random.
- **⚠️ clean-gate correction (2026-07-05, `clean_concordance_gate.md`)**: the 0/598 in (B) requires 3 sign-variable methods (moflow, **crakvelo**, mvvae). MultiVelo lag is structurally 100% positive (switch-time monotone ordering) so it cannot enter the *sign*-consistency test (null misspecified); therefore the clean sign-variable methods are only {moflow, mvvae}, 2 of them → the 2-method sign FDR has min p_perm≈0.50, a **principled power-bound (0 regardless of signal)**. That is, **0/598 is essentially CRAK-dependent → demoted to a CRAK sensitivity arm**. The **CRAK-independent clean headline is magnitude concordance** (clean 3-way |ρ|≤0.08, recomputed by the verify-gate `p3_concordance.py`) + 2-method sign-agreement 48% (chance). MultiVelo participates only in the magnitude/rank test, not the sign test (lag magnitude does vary across genes). *This is a reframe, not a method-swap* — do not re-run the sign test with {mv,moflow,mvvae} (reintroduces the constant-sign error).
- **root diagnosis**: the **chromatin opening rate α_c that determines lag is method-sensitive** (ρ=0.29), whereas the transcription rate α is robust (ρ=0.88).
  → lag inherits α_c's method sensitivity directly.
> Interpretation: "which gene is chromatin-leading" changes when you switch methods (non-robust, confirmed by 4-way·FDR). But the population-level directional balance + canonical markers converge across methods (robust).

### 2. Negative control — chromatin does not drive MultiVelo lag
- after within-lineage shuffling of ATAC (breaking the chromatin↔RNA coupling) and re-fitting → the lag distribution is **statistically identical**
  to the original (Mann–Whitney p=0.20, KS p=0.51), per-gene lag **ρ=0.72** preserved, chromatin likelihood 0.239→0.237 (unchanged).
- only the Wilcoxon paired p=0.0003 (median 5.87→5.48, slight decrease) = a **marginal contribution** of chromatin.
> Interpretation: MultiVelo lag comes from the **model structure (switch-time order) · gene-intrinsic RNA dynamics**, not from the chromatin signal.
> This independently confirms via the negative control §1's conclusion that 'MultiVelo 100% chromatin-leads = artifact'.

### 3. Confound — lag conclusion unbiased
- **cell-cycle**: cell-level ρ≈0.33–0.36 (S/G2M score vs expr), but the **gene level is unbiased** — among fit-lag genes,
  CC genes are 1.9% (10 genes), CC lag vs the rest Mann-Whitney p=0.86, median change 0.037 when CC excluded. The cell-level ρ arises
  because **cycling is strongly coupled to lineage** (MK 88%↔HSC 3%), so within-lineage analysis already controls it. → **no global regress_out performed** (risk of removing differentiation signal).
- **burst**: lag↔α Spearman −0.24 (moderate, |ρ|<0.5 → acceptable; reflected in regularized regression).
- **ambient/doublet**: scrublet applied, doublet median 0.045, pct_mito median 10.4% (QC max 20%) — normal.

### 4. Within-lineage lag distribution (reference, based on global fit)
- MultiVelo lag median is 4.3–7.4 pseudotime per lineage (Erythroid lowest, Lymphoid highest). All 100%>0 (§1 structural caveat).
- ⚠️ an approximation attributing the global fit by dominant-expression — **true within-lineage concordance needs per-lineage refit** (pending).
- rare lineage (MK/Baso·Eo·Mast/pDC) uncertainty reported separately.

### 5. lag robustness triangulation — accuracy·stability·predictability (2026-07-01)
- **(accuracy) injected-lag simulator** (`sim_injected_lag.md`, **2026-07-01 scope correction**): noise-free Spearman(true,rec)=**−0.89**.
  ⚠️ this is **not** a "rank recovery failure" — |ρ|=0.89 means the estimator **strongly tracks** the true-lag rank. The problem is **sign inversion + magnitude collapse** (underestimation 0.06×, consistently negative across kinetic settings, sign+ 24~78% shape-dependent).
  That is, the **crakvelo manual-DP DTW construct is a shape-artifact that distorts sign·magnitude on smooth dynamics**, not "lag is fundamentally unrecoverable". **Scope: this arm tests only the crakvelo estimator → grounds for not trusting CRAK-Velo lag in cross-method comparison**. The core H1 (moflow×multivelo×mvvae, α robust) does not use this construct → survives independently.
- **(stability) bootstrap lag-sign** (`bootstrap_stability.md`): with fit fixed·cells bootstrap-resampled, sign is 83% stable (median flip 0).
  But this is the **weakest stability** (sampling noise only) — not in contradiction with the cross-method·accuracy non-robustness. True re-fit stability would be lower.
- **(predictability) baseline→timing model** (`lag_model.md`): pure baseline chromatin features (HSC/MPP accessibility·dynamic-range) alone
  cannot predict lag across lineages (held-out ρ=**−0.21**). Adding +fit kinetic features gives ρ=+0.59 but this is **circular** (fit_alpha_c mechanically determines MultiVelo lag).
  → confirmed at the model level that the drug-timing model should use baseline features themselves·α, not a single lag value.
> Overall: lag is *sampling-stable within a single fit* but **method-non-robust (H1·P4) + baseline-non-predictable (P5)**. (The accuracy arm showed a shape-dependent distortion of the crakvelo construct — not "lag fundamentally unrecoverable" but "do not trust that construct across methods"; the core H1 is independent.)

### 6. cross-lineage lag concordance + real day0 ATAC feature (2026-07-01)
- **(within-method, cross-lineage) per-lineage refit** (`lineage_refit.md`): the 5 terminal lineages are **fit separately** on root∪L.
  cross-lineage lag magnitude Spearman ρ median=**0.349** (range 0.234~0.513, positive 10/10) = **weak/borderline**. The control α_c has ρ median=**0.483** (more robust) → the H1 pattern (α robust > lag) reproduces on the lineage axis too. ρ 0.23~0.46 vs the global fit → the global fit smears the lineage signal (justifies refit).
- **(real ATAC feature)** `atac_baseline_features.md`: from crakvelo's 197,482 peaks, assembled per-gene promoter (±2kb)/enhancer (±100kb distal) accessibility on the **day0 HSC/MPP 8,583 cells** (511 genes) → resolves §5 limitation ① (moflow Mc smoothed proxy).
- **(predictability double control)** `lag_model_atac.md`: held-out lineage prediction with the same baseline features·model —
  **robust α is predicted by the real ATAC (ρ=+0.309, positive in all 6 lineages)**, the Mc proxy (−0.089) fails. Meanwhile the **non-robust lag is non-predictable even with ATAC (ρ=+0.05≈chance)**.
  → **the same feature predicts the robust target (α) but not the non-robust target (lag)** = H1 reconfirmed on the *predictability* axis too + proves the value of the day0 ATAC assembly. atac+mc (+0.285) does not exceed ATAC alone → the Mc proxy adds no information.

### 7. cross-dataset replication — reproducing 'lag-fragile / α-robust' in other tissues·species (2026-07-06)
Tested across **four external multiomes** (including same-tissue human BMMC and HSPC-direct macrophage) that this is not a coincidence arising from one HSPC dataset alone. **The key is not the absolute value but the preservation of the α > lag ordering.**
- **(A) human_brain (adult brain multiome, HSPC↔human_brain MultiVelo)** `concordance_human_brain.md`:
  cross-dataset α rank Spearman **+0.475** (reproduced✅, p=4.5e-7) vs lag magnitude rank **+0.185** (weak, p=0.06). floor timing +0.002 (sanity). → α preserves rank across datasets, lag does not.
- **(B) E18 mouse brain (fetal brain multiome, MultiVelo tutorial data)** `concordance_e18_mouse_brain.md`:
  - **within-E18 cross-method α** (floor×MV×VAE, same gene axis): Spearman 0.78 / 0.81 / **0.90** (median **+0.81**) — HSPC's α-robust leg (ρ=0.88) **strongly reproduces** in non-hematopoietic tissue.
  - **within-E18 lag magnitude rank** (MV×VAE): **+0.057** — reproduces the lag-fragile leg (consistent with HSPC MV×VAE −0.01).
  - **cross-dataset HSPC↔E18** (after mouse→UPPER mapping, shared 132): α rank **+0.32** (p=2e-4) vs lag magnitude rank **+0.10** (p=0.23), floor α sanity +0.40.
- **(C) human BMMC (GSE194122, donor09/site4, same hematopoietic axis as HSPC — same-tissue nearest replication, we recovered spliced/unspliced via GEX BAM velocyto)** `concordance_GSE194122_bmmc.md`:
  - **within-BMMC cross-method α** (floor×MV×VAE, same gene axis): Spearman +0.82 / +0.85 / **+0.91** (median **+0.851**) — the α-robust leg **reproduces most strongly in the same tissue** (consistent with HSPC ρ=0.88).
  - **within-BMMC lag magnitude rank** (MV×VAE): **−0.088** (p=0.15) — reproduces the lag-fragile leg (consistent with HSPC MV×VAE −0.01, E18 +0.06).
  - **cross-dataset HSPC↔BMMC** (human↔human, direct SYMBOL matching, shared 88): α rank **+0.550** (p=2.9e-8) vs lag magnitude rank **+0.052** (p=0.63), floor α sanity +0.558. → being same-tissue, cross-dataset α is stronger than human_brain·E18 (0.55).
- **(D) macrophage differentiation (GSE284047 · figshare 30280333, Day14 HSPC-direct differentiation — the nearest tissue axis; the figshare postpro retains raw spliced/unspliced nnz 35.6% → common preprocessing branch)** `concordance_macrophage.md`:
  - **within-macrophage cross-method α** (floor×MV×VAE, same gene axis): Spearman +0.826 / +0.865 / **+0.917** (median **+0.865**) — the α-robust leg **reproduces most strongly of the four externals**.
  - **within-macrophage lag magnitude rank** (MV×VAE): **+0.074** (TOST |ρ|<0.2 → equivalent to 0) — reproduces the lag-fragile leg.
  - **cross-dataset HSPC↔macrophage** (human↔human, direct SYMBOL matching, shared 274): α rank **+0.643** (95%CI [+0.554,+0.719], p=2.5e-33) vs lag magnitude rank **+0.148** (95%CI [+0.027,+0.263], p=0.014), floor α sanity +0.677. As HSPC's direct differentiation product, **cross-dataset α is the highest of the four**. Δρ=ρ_α−ρ_lag=**+0.843** (95%CI [+0.773,+0.912], excludes 0 = dissociation). ✅ canonical numpy (B=10000, seed=20260707) confirmed (2026-07-10).
> Verdict: **within-dataset the α-robust/lag-fragile ordering reproduces strongly** (macrophage within α 0.865 ≫ lag 0.07; BMMC within α 0.85 ≫ lag −0.09; E18 within α 0.81 ≫ lag 0.06), and **cross-dataset α decays monotonically with tissue distance while lag is signal-free everywhere**: HSPC-direct macrophage α **+0.643** > same-tissue human BMMC **+0.55** > adult human_brain **+0.475** > cross-species E18 **+0.32**, whereas lag is +0.05~+0.19 noise on all four axes. That is, not the strong claim "α is preserved across species" but rather the **ordering statement "in whatever dataset, α is more robust to method·dataset than lag"**, consistent across 5 axes (HSPC + human_brain + E18 + BMMC + macrophage).
> ⚠️ honest caveat: the lag-fragile leg rests within-dataset on **only a single method pair (MV×VAE)** (BMMC·E18·macrophage all have MoFlow/CRAK unrun → thinner than HSPC's 3 pairs). All four replications are 1 donor/sample each — no strong generalization; the narrative rests only on the consistency of the five axes. BMMC ATAC is a gencode-proximity aggregation of the processed peak matrix (implementation differs from HSPC's mv.aggregate_peaks_10x → conservative noise on the cross rank). macrophage points are final but p·CI await canonical numpy regeneration (§7-D).

### 8. profile-likelihood practical identifiability — proving 'lag-fragile / α-robust' as an objective-function property (2026-07-09)
Testing *why* the cross-method/cross-dataset observations (§1·§6·§7) arise, on MultiVelo's **own objective function**. A fixed-nuisance profile likelihood is scanned separately in the α direction and the lag (=t_sw2−t_sw1) direction (latent time re-optimized, n=538 genes; `p3_profile_likelihood.py`, fit·likelihood reproduction r≈1.0).
- **α is stiff, lag is sloppy**: per-cell curvature median α **8.20/cell** ≫ lag **2.24/cell**. per-gene stiffness ratio κ_alpha/κ_lag (interior both>0, n=258) median **3.53×** (IQR [1.92, 7.41]), **α stiffer than lag in 94.57%** of genes (244/258).
- **lag trichotomy (n=538)**: interior 302 (56%) / boundary_pinned 205 (38%) / degenerate 31 (6%). That is, in **44% lag is pinned to the admissible boundary or has vanishing curvature** → the data cannot even set an upper bound. interior lag CI width/admissible range median **6.55%** (the α-vs-lag comparison uses the same-unit metric, the curvature ratio 3.53×).
- **Verdict**: MultiVelo's objective function is **practically non-identifiable in the lag direction (near-flat and boundary-limited), identifiable in the α direction (sharp)**. lag failing to reproduce is not noise — it is because the likelihood is inherently less informative in the lag direction. This is **relative (practical) non-identifiability**, not a fully flat valley (honest framing). Consistent with the dissociation·external rate validation → the observation is promoted to mechanism.
- **Scope/limitations**: the likelihood geometry of the single MultiVelo method; the freed-nuisance gate (β/γ/α_c/rescale/scale_cc re-optimized) is **partial (usable n=1)** — the main fixed-nuisance (538) carries the claim. (`results/profile_likelihood_identifiability.md`, `figures/fig05_profile_likelihood.png`)

---

## Connection to the drug-timing goal (P5)
- **usable robust signal**: transcription rate α (cross-method ρ=0.88), population-level directional balance.
- **not to be used as-is**: per-gene lag magnitude·direction (method-sensitive). To use as a baseline feature, reflect method uncertainty
  in the model as uncertainty, or use after stabilizing α_c estimation (bootstrap/per-lineage).
- The 4-way H1 (+CRAK-Velo) + permutation FDR have **confirmed** the robustness of this conclusion — even with a 4th method·permutation null, lag concordance is weak and the agreement-set is empty.
- The §5 triangulation (accuracy·stability·predictability) adds confirmation: **lag non-predictable from baseline chromatin (held-out ρ=−0.21)** + the accuracy arm shows the crakvelo construct's shape-dependent distortion (grounds for cross-method untrustworthiness) → "do not use lag as a single value" holds at the model level too. baseline-feature·α-centric + restriction to bootstrap-stable genes is the next direction.
- §6 confirmed that **the real day0 ATAC feature predicts α (robust) on held-out lineages (ρ=+0.31)** → the data support routing the drug-timing model input through **day0 ATAC promoter/enhancer accessibility → α**, not lag. Next is validating this proxy route with a drug perturbation arm (timing ground truth).

## Key limitations
1. **Pseudotime ≠ wall-clock**: day0/day7 batch-integrated → lag is in pseudotime units. wall-clock anchor impossible (H2 demoted).
2. lag definition differs per method (switch-timing vs rate-timescale vs DTW) → comparisons reported separately by rank·sign.
3. based on global fit (per-lineage refit incomplete). bootstrap stability incomplete.
4. ~~negative control is a single method, MultiVelo~~ → **resolved (2026-07-06)**: extended the ATAC-shuffle negative control with MoFlow (a structurally independent 2nd method) (`scrambled_null_moflow.md`). MoFlow lag also survives the shuffle (per-gene ρ=0.52 ≫ method-swap ρ=0.08, chromatin-channel fit-quality unchanged) → "lag is model-structural, not chromatin-driven" generalizes to two methods. (CRAK-Velo scramble is follow-up.)
