# FINDINGS — HSPC velocity 벤치마크 결과·해석 종합

> **이 문서가 결과+해석의 canonical 종합본이다.** 개별 분석 md(`concordance.md`, `h1_lag_diagnostic.md`,
> `scrambled_null.md`, `confound.md`, `cellcycle_genelevel.md`, `lineage_lag.md`)는 상세 근거이고,
> 여기서는 그것들을 연구 질문에 맞춰 한 줄 결과+해석으로 묶고 통합 결론을 낸다.
> 새 분석이 끝날 때마다 갱신. 진행 상태는 `../PROGRESS-LIVE.md`, 현황은 `../../../HANDOFF.md`.
> 최종 갱신: **2026-07-06** (§7 cross-dataset replication 신설: `concordance_human_brain.md`, `concordance_e18_mouse_brain.md`).

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
| **진짜 day0 ATAC feature 어셈블 + 모델** | ✅ | `atac_baseline_features.md` + `lag_model_atac.md` |
| **cross-dataset replication** (human_brain + E18 mouse brain) | ✅ | `concordance_human_brain.md` + `concordance_e18_mouse_brain.md` |
| drug perturbation arm | ⬜ 대기(데이터) | — |
| α_c 전체-refit bootstrap stability | ⬜ 대기(GPU) | — |

---

## ★ 통합 결론 (현재까지)
**chromatin→transcription lag은 gene 수준에서 method-robust한 양이 아니다.** 크기·방향 모두 method 간
일치하지 않으며(H1 실패 — **CRAK-비의존 clean headline**: 3-method magnitude concordance |ρ|≤0.08 {mv×moflow −0.04, mv×mvvae −0.01, moflow×mvvae +0.08} + 2-method sign-agreement 48%≈chance. permutation-FDR **agreement-set 0/598은 sign-가변 method 3개가 필요해 CRAK 포함 시에만 정의됨 → CRAK 민감도 arm으로 강등**; 2026-07-05 `clean_concordance_gate.md`), 음성대조는 한 method(MultiVelo)의 lag이
chromatin 신호가 아니라 모델 구조에서 나옴을 보였다. **robust한 것은 (a) 전사율 α(method 간 ρ=0.88), (b) 집단 수준 방향 균형(~50/50, 두 method 수렴), (c) canonical priming marker 방향(method 간 일치)뿐.**
→ drug-timing 모델은 lag을 단일 method 값으로 쓰면 안 되고, **method 불확실성을 명시적으로 반영**해야 한다.
이 'α > lag' 순서는 **두 외부 데이터셋(성인 human_brain·태아 E18 mouse brain)에서도 보존**(§7) — HSPC 단일 데이터의 우연이 아니다.

---

## 발견별 결과·해석

### 1. H1 — cross-method lag 일치도: **약함/실패**
- **lag 크기 무상관**: pairwise Spearman multivelo×moflow **−0.04**(p=0.38), multivelo×multivelovae **−0.01**(p=0.81),
  moflow×multivelovae **+0.08**(p=0.04). 정의를 apples-to-apples로 통일해도 **+0.12**에 그침(`h1_lag_diagnostic`).
- **방향 ~50/50**: sign-가변 method 모두 chromatin-leads 비율 MoFlow **44.8%** / MultiVeloVAE **49.3%** → 전역
  'chromatin이 transcription을 prime한다' **데이터 미지지**. (MultiVelo 100%는 switch-time 단조정렬 모델 제약 아티팩트.)
- **gene 수준 방향 불일치**: moflow×multivelovae sign-agreement **48%**(우연).
- **4-way 확장(+CRAK-Velo)**: CRAK-Velo lag 부호 버그(`dtw_lag`이 MoFlow `fastdtw`와 반대) **검증·수정**(`crakvelo_sign_check.md`) 후
  moflow×crakvelo Spearman **−0.151**, crakvelo×multivelovae **−0.04** — 4번째 method를 넣어도 무상관/약한 음의 일치. CRAK-Velo도 chromatin-leads **41.1%**(균형).
  단 canonical priming marker(CSF1R·S100A9 등)는 두 method 모두 chromatin-leading(양수)으로 **일치** → 강건한 건 marker뿐.
- **permutation FDR(P4) 통계 확증**(`permutation_fdr.md`, N=10⁴): (A) cross-method ρ은 2/3 쌍이 gene-label shuffle null 대비 유의하나 **effect 극약(|ρ|≤0.15)·방향 불일치**.
  (B) per-gene cross-method sign-consistency **agreement-set = 0/598 gene**(FDR<0.10) → **공집합**. 어떤 gene도 method 간 lag 방향이 무작위 이상으로 일관되지 않음.
- **⚠️ clean-gate 정정(2026-07-05, `clean_concordance_gate.md`)**: (B)의 0/598은 sign-가변 method 3개(moflow, **crakvelo**, mvvae)를 요구한다. MultiVelo lag은 구조적 100% 양수(switch-time 단조정렬)라 *sign*-consistency 검정에 넣을 수 없고(null 오지정), 따라서 clean sign-가변 method는 {moflow, mvvae} 2개뿐 → 2-method sign FDR은 min p_perm≈0.50으로 **원리적 power-bound(신호 무관 0)**. 즉 **0/598은 본질적으로 CRAK-의존** → **CRAK 민감도 arm으로 강등**. **CRAK-비의존 clean headline은 magnitude concordance**(clean 3-way |ρ|≤0.08, verify-gate `p3_concordance.py`가 재계산) + 2-method sign-agreement 48%(chance). MultiVelo는 sign이 아니라 magnitude/rank 검정에만 참여(lag 크기는 gene간 변이 有). *reframe이지 method-swap이 아님* — {mv,moflow,mvvae}로 sign 검정 재실행 금지(상수-부호 오류 재도입).
- **근원 진단**: lag을 결정하는 **chromatin opening rate α_c가 method-민감**(ρ=0.29)인 반면 전사율 α는 강건(ρ=0.88).
  → lag이 α_c의 method 민감성을 그대로 상속.
> 해석: "어느 gene이 chromatin 선행인지"는 method를 바꾸면 달라진다(비robust, 4-way·FDR로 확증). 단 집단 수준 방향 균형 + canonical marker는 method 간 수렴(robust).

### 2. 음성대조 — chromatin은 MultiVelo lag을 구동하지 않음
- ATAC를 within-lineage 셔플(chromatin↔RNA 결합 파괴) 후 재fit → lag 분포 원본과 **통계적으로 동일**
  (Mann–Whitney p=0.20, KS p=0.51), per-gene lag **ρ=0.72** 보존, chromatin likelihood 0.239→0.237(불변).
- 단 Wilcoxon paired p=0.0003 (median 5.87→5.48 소폭 감소) = chromatin의 **marginal 기여**만.
> 해석: MultiVelo lag은 chromatin 신호가 아니라 **모델 구조(switch-time 순서)·gene 고유 RNA 동역학**에서 나온다.
> §1의 'MultiVelo 100% chromatin-leads = 아티팩트' 결론을 음성대조로 독립 확증.

### 3. Confound — lag 결론 비편향
- **cell-cycle**: 세포 수준 ρ≈0.33–0.36(S/G2M score vs expr)이지만 **gene 수준은 비편향** — fit lag gene 중
  CC gene 1.9%(10개), CC lag vs 나머지 Mann-Whitney p=0.86, CC 제외 시 median 변화 0.037. 세포-수준 ρ의 정체는
  **cycling이 lineage와 강결합**(MK 88%↔HSC 3%)이라 within-lineage 분석이 이미 통제. → **global regress_out 미수행**(분화신호 제거 위험).
- **burst**: lag↔α Spearman −0.24(중간, |ρ|<0.5 → 허용; regularized 회귀 시 반영).
- **ambient/doublet**: scrublet 적용, doublet median 0.045, pct_mito median 10.4%(QC max 20%) — 정상.

### 4. Within-lineage lag 분포 (참고, 전역 fit 기반)
- MultiVelo lag median은 lineage별 4.3–7.4 pseudotime(Erythroid 최저, Lymphoid 최고). 전부 100%>0(§1 구조 caveat).
- ⚠️ 전역 fit을 dominant-expression으로 귀속한 근사 — **진짜 within-lineage 일치도는 per-lineage refit 필요**(대기).
- rare lineage(MK/Baso·Eo·Mast/pDC) uncertainty 별도.

### 5. lag의 robustness 3각 검정 — accuracy·stability·predictability (2026-07-01)
- **(accuracy) injected-lag simulator** (`sim_injected_lag.md`, **2026-07-01 스코프 정정**): 무noise Spearman(true,rec)=**−0.89**.
  ⚠️ 이는 "순위 회복 실패"가 **아님** — |ρ|=0.89는 estimator가 true-lag 순위를 **강하게 추적**한다는 뜻. 문제는 **부호 반전 + 크기 붕괴**(과소추정 0.06×, kinetic 설정 전반 일관 음수, sign+ 24~78% shape-의존).
  즉 **crakvelo manual-DP DTW construct가 매끄러운 동역학에서 부호·크기를 왜곡**하는 shape-아티팩트이지 "lag은 원리적으로 recover 불가"가 아님. **스코프: 이 arm은 crakvelo estimator만 테스트 → CRAK-Velo lag을 cross-method 비교에서 신뢰하지 말라는 근거**. 핵심 H1(moflow×multivelo×mvvae, α robust)은 이 construct 미사용 → 독립 생존.
- **(stability) bootstrap lag-sign** (`bootstrap_stability.md`): fit 고정·cell 복원추출에선 부호 83% 안정(median flip 0).
  단 **가장 약한 안정성**(표집 노이즈만) — cross-method·정확도 비robust와 모순 아님. 진짜 re-fit stability는 더 낮을 것.
- **(predictability) baseline→timing 모델** (`lag_model.md`): 순수 baseline chromatin feature(HSC/MPP 접근성·dynamic-range)만으로는
  lag을 lineage 간 예측 못 함(held-out ρ=**−0.21**). +fit kinetic feature 넣으면 ρ=+0.59지만 이는 **순환**(fit_alpha_c가 MultiVelo lag을 기계적으로 결정).
  → drug-timing 모델은 단일 lag 값이 아니라 baseline feature 자체·α를 써야 함을 모델 수준에서 확인.
> 종합: lag은 *한 fit 안에선 표집-안정*하지만 **method-비robust(H1·P4) + baseline 비예측(P5)**. (accuracy arm은 crakvelo construct의 shape-왜곡을 보인 것 — "lag 원리적 회복 불가"가 아니라 "그 construct를 cross-method에서 신뢰 말라"; 핵심 H1은 독립.)

### 6. cross-lineage lag 일치도 + 진짜 day0 ATAC feature (2026-07-01)
- **(within-method, cross-lineage) per-lineage refit** (`lineage_refit.md`): 5개 terminal lineage를 root∪L로 **따로 fit**.
  cross-lineage lag magnitude Spearman ρ median=**0.349**(범위 0.234~0.513, 양수 10/10) = **약함/경계**. 대조군 α_c는 ρ median=**0.483**(더 robust) → H1 패턴(α robust > lag)이 lineage 축에서도 재현. 전역 fit과의 ρ 0.23~0.46 → 전역 fit이 lineage 신호를 뭉갬(refit 정당).
- **(진짜 ATAC feature)** `atac_baseline_features.md`: crakvelo 197,482 peak에서 **day0 HSC/MPP 8,583 세포** 기준 gene별 promoter(±2kb)/enhancer(±100kb distal) 접근성 어셈블(511 gene) → §5 한계 ①(moflow Mc smoothed proxy) 해소.
- **(예측가능성 이중 대조)** `lag_model_atac.md`: 같은 baseline feature·모델로 held-out lineage 예측 —
  **robust α는 진짜 ATAC로 예측됨(ρ=+0.309, 6 lineage 전부 양수)**, Mc proxy(−0.089)는 실패. 반면 **비robust lag은 ATAC로도 비예측(ρ=+0.05≈chance)**.
  → **같은 feature가 robust target(α)은 예측하고 비robust target(lag)은 못 한다** = H1이 *예측가능성* 축에서도 재확인 + day0 ATAC 어셈블의 가치 입증. atac+mc(+0.285)가 ATAC 단독을 못 넘음 → Mc proxy는 추가 정보 없음.

### 7. cross-dataset replication — 다른 조직·종에서 'lag-fragile / α-robust' 재현 (2026-07-06)
HSPC 한 데이터셋의 우연이 아님을 두 외부 multiome으로 검정. **핵심은 절대값이 아니라 α > lag 순서의 보존.**
- **(A) human_brain (성인 뇌 multiome, HSPC↔human_brain MultiVelo)** `concordance_human_brain.md`:
  cross-dataset α rank Spearman **+0.475**(재현✅, p=4.5e-7) vs lag 크기 rank **+0.185**(약함, p=0.06). floor timing +0.002(sanity). → α는 데이터셋을 넘어 rank 보존, lag은 안 됨.
- **(B) E18 mouse brain (태아 뇌 multiome, MultiVelo 튜토리얼 데이터)** `concordance_e18_mouse_brain.md`:
  - **within-E18 cross-method α**(floor×MV×VAE, 같은 gene축): Spearman 0.78 / 0.81 / **0.90**(중앙값 **+0.81**) — HSPC의 α-robust leg(ρ=0.88)이 비-조혈에서 **강하게 재현**.
  - **within-E18 lag 크기 rank**(MV×VAE): **+0.057** — lag-fragile leg 재현(HSPC MV×VAE −0.01과 정합).
  - **cross-dataset HSPC↔E18**(mouse→UPPER 매핑 후 shared 132): α rank **+0.32**(p=2e-4) vs lag 크기 rank **+0.10**(p=0.23), floor α sanity +0.40.
> 판정: **within-dataset에선 α-robust/lag-fragile 순서가 강하게 재현**(E18 within α 0.81 ≫ lag 0.06)되고, **cross-species로 가면 두 leg 모두 감쇠하되 순서는 보존**(E18 α 0.32 > lag 0.10; human_brain α 0.475 > lag 0.185). 즉 "α가 종을 넘어 보존된다"는 강한 주장이 아니라 **"어느 데이터셋에서 재도, α가 lag보다 method·데이터셋에 robust하다"는 순서 진술**이 3개 축(HSPC + human_brain + E18)에서 일관.
> ⚠️ 정직 caveat: **E18 lag-fragile leg는 단일 method 쌍(MV×VAE)에만 근거** — MoFlow/CRAK를 E18에 안 돌려 HSPC(3쌍)보다 얇다. human_brain·E18 모두 replication 1건씩 — 강한 일반화 금지, 세 축 일관성으로만 서사.

---

## drug-timing 목표(P5)와의 연결
- **쓸 수 있는 robust 신호**: 전사율 α(method 간 ρ=0.88), 집단 수준 방향 균형.
- **그대로 쓰면 안 되는 것**: gene별 lag 크기·방향(method 민감). baseline feature로 넣으려면 method 불확실성을
  uncertainty로 모델에 반영하거나, α_c 추정 안정화(bootstrap/per-lineage) 후 사용.
- 4-way H1(CRAK-Velo 추가) + permutation FDR로 이 결론의 견고성을 **확증 완료** — 4번째 method·permutation null에서도 lag 일치도는 약하고 agreement-set은 공집합.
- §5 3각 검정(accuracy·stability·predictability)로 추가 확증: **baseline chromatin으로 lag 비예측(held-out ρ=−0.21)** + accuracy arm은 crakvelo construct가 shape-의존 왜곡(cross-method 신뢰 불가 근거) → "lag을 단일 값으로 쓰지 말라"가 모델 수준에서도 성립. baseline feature·α 중심 + bootstrap 안정 gene 한정이 다음 방향.
- §6에서 **진짜 day0 ATAC feature로 α(robust)는 held-out lineage 예측됨(ρ=+0.31)**을 확인 → drug-timing 모델의 입력은 lag이 아니라 **day0 ATAC promoter/enhancer 접근성 → α** 경로로 가는 것이 데이터로 지지됨. 다음은 drug perturbation arm(timing ground truth)으로 이 proxy 경로를 검증.

## 핵심 한계
1. **Pseudotime ≠ wall-clock**: day0/day7 batch 통합 → lag은 pseudotime 단위. wall-clock anchor 불가(H2 강등).
2. lag 정의가 method마다 다름(switch-timing vs rate-timescale vs DTW) → 비교는 rank·sign 분리 보고.
3. 전역 fit 기반(per-lineage refit 미완). bootstrap stability 미완.
4. ~~음성대조는 MultiVelo 단일 method~~ → **해소(2026-07-06)**: MoFlow(구조 독립 2번째 method)로 ATAC-shuffle 음성대조 확장 완료(`scrambled_null_moflow.md`). MoFlow lag도 셔플 생존(per-gene ρ=0.52 ≫ method-swap ρ=0.08, chromatin-채널 fit-quality 불변) → "lag은 model-structural, not chromatin-driven"이 두 method로 일반화. (CRAK-Velo scramble은 후속.)
