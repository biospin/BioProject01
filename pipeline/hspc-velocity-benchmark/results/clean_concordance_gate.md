# Clean concordance gate — agreement-set의 CRAK 비의존 재계산 (2026-07-05)

> **"0/598 agreement-set" 헤드라인의 정확성 게이트**(novelty_strategy §0/§4.0).
> 공개된 agreement-set은 부호 가변 method = `{moflow, crakvelo, multivelovae}`에서 계산되며 —
> CRAK-Velo를 **포함**하고(우리가 버그로 지적한 method: `crakvelo_sign_check.md`) MultiVelo를 **제외**한다.
> 이 노트는 깨끗한(clean) method 집합에서 재계산하고, MultiVelo에 대한 실질적 방법론 판단을 밝히며,
> 빈 agreement-set 결론이 CRAK 없이도 유지되는지 판정한다.
> 기존 lag 표(`multivelo/moflow/crakvelo/multivelovae_genes.csv`)의 순수 재분석이며, 새 fit은 없다.
> lag 정의는 `p3_concordance.py::METHODS`(단일 출처)에서 그대로 재사용한다. N_perm=10⁴, seed=20260701, FDR<0.10.

---

## 0. 실질적 방법론 판단 — MultiVelo는 *부호*-일관성 검정에 들어갈 수 없다

MultiVelo의 lag(`fit_t_sw2 − fit_t_sw1`)은 **100% 양수**(n=538)인데, 4-state 모델이 switch time을 **단조 순서로
정렬**하기 때문이다(t_sw1<t_sw2<t_sw3). 따라서 per-gene *부호*는 **구조적 상수(+)**여서 판별 정보를 전혀 담지
못한다. 부호가 상수인 method를 per-gene 부호-일관성 검정에 넣으면:
- **null을 잘못 설정한다**(null은 각 method의 부호를 무작위 ±로 뽑는데, MultiVelo는 +로 고정), 그리고
- 통계량 `|mean(sign)|`을 위쪽으로, 비대칭적으로 **편향시킨다**(chromatin-leading 합의만 보상할 수 있음).

**결정:** MultiVelo는 **크기(magnitude)/순위(rank) concordance 검정에만** 참여한다(그 lag *크기*는 정당하게
변한다, 4.3–7.4 pt). **부호-일관성 agreement-set에는 결코 넣지 않는다.** 이는 프로젝트 원칙("부호가 아니라 lag
*크기* 순위를 비교하라; MultiVelo 부호는 구조적으로 양수여서 정보가 없다")과 일치한다.

**귀결(핵심):** 부호 정보를 갖고 버그가 없는 method는 정확히 **{MoFlow, MultiVeloVAE} = 2개**다. 2-method
부호-일관성 FDR은 **퇴화(degenerate)한다** — per-gene 최소 달성 가능 p ≈ 0.50(일치→0.50, 불일치→1.0)이라,
신호와 무관하게 쓸 만한 어떤 FDR에서도 agreement-set은 자명하게 0이다(아래에서 경험적으로 확인, min p_perm=0.499).
**깨끗한 3-method 부호 검정은 존재하지 않는다.** 부호 정보를 가진 method를 3개로 만드는 유일한 길은 CRAK-Velo를
더하는 것이므로 — **0/598 agreement-set은 단지 CRAK에 오염된 것이 아니라 본질적으로 CRAK에 의존한다.**
따라서 깨끗한, CRAK 비의존 증거는 agreement-set이 아니라 **크기(magnitude) concordance**에서 나와야 한다.

## 1. 부호 관례 검증 (결합 전)

코드베이스 `cs_lag_median`: **양수 = chromatin-leading**(myeloid priming marker에서 확인) — AZU1 **+0.38**,
PRTN3 **+0.38**, CTSG **+0.31**, ELANE **+0.19**, MPO **+0.10**(CSF1R −0.05, 0에 가까운 예외). 이는
**MoFlow 논문의 "음의 c-s lag = chromatin-leading" 표현과 정반대 극성**이며 — 논문과 코드베이스 사이의 부호
반전이므로, 어떤 "chromatin-leading" 부분집합을 정의하든 반드시 명시해야 한다(`moflow_subset_confrontation.md` 참조).
MultiVeloVAE lag = `1/α_c − 1/α`는 자체 의미를 갖는다(양수 = chromatin 전이가 더 느림); 이 method는 method 간
절대 크기가 아니라 순위/부호-일치에서만 결합한다.

## 2. 깨끗한 크기 concordance — CRAK 비의존 헤드라인

signed lag의 쌍별 Spearman 순위(permutation p, gene-label shuffle null):

| pair | n | Spearman ρ | \|ρ\| | p(perm) | set |
|---|---|---|---|---|---|
| multivelo×moflow | 537 | −0.038 | 0.038 | 0.384 | **CLEAN 3-way** |
| multivelo×multivelovae | 538 | −0.010 | 0.010 | 0.808 | **CLEAN 3-way** |
| moflow×multivelovae | 636 | +0.083 | 0.083 | 0.032 | **CLEAN 3-way** |
| multivelo×crakvelo | 287 | +0.003 | 0.003 | 0.963 | CRAK sensitivity |
| moflow×crakvelo | 330 | −0.151 | 0.151 | 0.007 | CRAK sensitivity |
| crakvelo×multivelovae | 334 | −0.040 | 0.040 | 0.463 | CRAK sensitivity |

**깨끗한 3-way(MultiVelo × MoFlow × MultiVeloVAE): 모든 |ρ| ≤ 0.083.** 명목상 유의한 유일한 쌍
(moflow×multivelovae, +0.083)도 무시할 만한 효과다; CRAK를 더하면 오히려 더 음수/비일관이 된다
(moflow×crak = −0.151, +0.083과 부호 불일치). 어떤 method 집합도 의미 있는 method 간 per-gene lag concordance를
보이지 않는다.

**깨끗한 2-method 부호-일치**(moflow×multivelovae) = **48.1%** = 우연 수준(chance).

## 3. Agreement-set FDR — 깨끗한 것, 시연용-무효, 민감도

| method set | n_tested | agreement-set (FDR<0.10) | min p_perm | note |
|---|---|---|---|---|
| **{moflow, mvvae}** (clean sign-informative) | 560 | **0** | 0.499 | 유효하나 **검정력 제한(power-bounded)** (2-method degenerate) |
| {multivelo, moflow, mvvae} | 628 | 0 | 0.249 | **무효(INVALID)** (MultiVelo 상수 부호가 검정을 편향) — 시연용일 뿐; 헤드라인 아님 |
| {moflow, crakvelo, mvvae} | 598 | **0** | 0.248 | **CRAK 민감도** — 공개된 p4를 정확히 재현(self-check ✓) |

Self-check: 나의 재구현은 공개된 p4 `{moflow, crakvelo, mvvae}` = **0/598**을 정확히 재현한다.

## 4. 판정

**이 결론은 CRAK 없이도 유지된다; 다만 핵심 통계량은 갈아타야 한다.** "per-gene chromatin→transcription
lag은 method 재현되지 않는다"는 깨끗한 method 집합에서 성립한다 — 깨끗한 3-way 크기 concordance |ρ| ≤ 0.08,
깨끗한 2-method 부호-일치 48% ≈ 우연 수준이며, **둘 다 CRAK-Velo를 쓰지 않는다.** 그러나 특정한 "0/598
agreement-set" 수치는 *본질적으로* CRAK에 의존한다(부호 정보를 가진 method 3개가 필요한데 MultiVelo는 부호가
구조적이다). 따라서 그것은 헤드라인이 아니라 **CRAK 포함 보조 민감도 분석으로 강등해야 한다(대표 결과에서 빼고
민감도 분석으로 다룸).** 헤드라인은 크기 concordance로 재구성한다(이 통계량은 검증 게이트 `p3_concordance.py`가
재계산하는 것이기도 하다; `p4_permutation_fdr.py`는 게이트가 커버하지 않는다). **이것은 재구성(reframe)이지
method 교체(method-swap)가 아니다** — "깨끗한 3-way 0/598" 수치를 지키려고 {multivelo, moflow, mvvae}에 부호
검정을 돌리지 말라; 그렇게 하면 지금 고치고 있는 바로 그 상수-부호 오류를 슬그머니 다시 들여오는 것이다.

---

# Clean concordance gate — CRAK-independent recompute of the agreement-set (2026-07-05)

> **Correctness gate for the "0/598 agreement-set" headline** (novelty_strategy §0/§4.0).
> The published agreement-set is computed over sign-variable method = `{moflow, crakvelo, multivelovae}` —
> it **includes CRAK-Velo** (the arm we flagged buggy: `crakvelo_sign_check.md`) and **excludes MultiVelo**.
> This note recomputes on a clean method set, states the substantive methods call about MultiVelo, and
> rules whether the empty-agreement-set conclusion survives CRAK-free.
> Pure re-analysis of existing lag tables (`multivelo/moflow/crakvelo/multivelovae_genes.csv`); no new fits.
> Lag definitions reused verbatim from `p3_concordance.py::METHODS` (single source). N_perm=10⁴, seed=20260701, FDR<0.10.

---

## 0. Substantive methods call — MultiVelo cannot enter a *sign*-consistency test

MultiVelo's lag (`fit_t_sw2 − fit_t_sw1`) is **100% positive** (n=538) because the 4-state model **monotonically
orders** switch times (t_sw1<t_sw2<t_sw3). Its per-gene *sign* is therefore a **structural constant (+)**, carrying
zero discriminating information. Putting a constant-sign method into a per-gene sign-consistency test:
- **misspecifies the null** (the null draws each method's sign random ±; MultiVelo is fixed +), and
- **biases the statistic** `|mean(sign)|` upward and asymmetrically (it can only reward chromatin-leading consensus).

**Decision:** MultiVelo participates **only in the magnitude/rank concordance test** (its lag *magnitude* varies
legitimately, 4.3–7.4 pt), **never in the sign-consistency agreement-set.** This matches the project discipline
("compare lag *magnitude* rank, not sign; MultiVelo sign is structurally positive/uninformative").

**Consequence (load-bearing):** the sign-informative, non-buggy methods are exactly **{MoFlow, MultiVeloVAE} = 2**.
A 2-method sign-consistency FDR is **degenerate** — per-gene min achievable p ≈ 0.50 (agree→0.50, disagree→1.0),
so the agreement-set is trivially 0 at any usable FDR *regardless of signal* (confirmed empirically below,
min p_perm=0.499). **There is no clean 3-method sign test.** The only way to reach 3 sign-informative methods is
to add CRAK-Velo — so the **0/598 agreement-set is intrinsically CRAK-dependent, not merely CRAK-contaminated.**
The clean, CRAK-independent evidence must therefore come from the **magnitude concordance**, not the agreement-set.

## 1. Sign-convention verification (before combining)

Codebase `cs_lag_median`: **positive = chromatin-leading** (confirmed on myeloid priming markers) — AZU1 **+0.38**,
PRTN3 **+0.38**, CTSG **+0.31**, ELANE **+0.19**, MPO **+0.10** (CSF1R −0.05, near-zero exception). This is the
**opposite polarity to the MoFlow paper's "negative c-s lag = chromatin-leading" wording** — a paper-vs-codebase
sign flip that must be stated when defining any "chromatin-leading" subset (see `moflow_subset_confrontation.md`).
MultiVeloVAE lag = `1/α_c − 1/α` has its own semantics (positive = chromatin transitions slower); it is combined
only on rank/sign-agreement, never on absolute magnitude across methods.

## 2. Clean magnitude concordance — CRAK-independent headline

Pairwise Spearman rank of signed lag (permutation p, gene-label shuffle null):

| pair | n | Spearman ρ | \|ρ\| | p(perm) | set |
|---|---|---|---|---|---|
| multivelo×moflow | 537 | −0.038 | 0.038 | 0.384 | **CLEAN 3-way** |
| multivelo×multivelovae | 538 | −0.010 | 0.010 | 0.808 | **CLEAN 3-way** |
| moflow×multivelovae | 636 | +0.083 | 0.083 | 0.032 | **CLEAN 3-way** |
| multivelo×crakvelo | 287 | +0.003 | 0.003 | 0.963 | CRAK sensitivity |
| moflow×crakvelo | 330 | −0.151 | 0.151 | 0.007 | CRAK sensitivity |
| crakvelo×multivelovae | 334 | −0.040 | 0.040 | 0.463 | CRAK sensitivity |

**Clean 3-way (MultiVelo × MoFlow × MultiVeloVAE): all |ρ| ≤ 0.083.** The one nominally-significant pair
(moflow×multivelovae, +0.083) is a negligible effect; adding CRAK only makes it more negative/incoherent
(moflow×crak = −0.151, sign disagreement with the +0.083). No method set shows meaningful cross-method
per-gene lag concordance.

**Clean 2-method sign-agreement** (moflow×multivelovae) = **48.1%** = chance.

## 3. Agreement-set FDR — clean, invalid-for-demonstration, and sensitivity

| method set | n_tested | agreement-set (FDR<0.10) | min p_perm | note |
|---|---|---|---|---|
| **{moflow, mvvae}** (clean sign-informative) | 560 | **0** | 0.499 | valid but **power-bounded** (2-method degenerate) |
| {multivelo, moflow, mvvae} | 628 | 0 | 0.249 | **INVALID** (MultiVelo constant sign biases test) — shown only to demonstrate; not a headline |
| {moflow, crakvelo, mvvae} | 598 | **0** | 0.248 | **CRAK sensitivity** — reproduces published p4 exactly (self-check ✓) |

Self-check: my reimplementation reproduces the published p4 `{moflow, crakvelo, mvvae}` = **0/598** exactly.

## 4. Verdict

**The conclusion survives CRAK-free; the load-bearing statistic must pivot.** "Per-gene chromatin→transcription
lag is not method-reproducible" holds on the clean method set — clean 3-way magnitude concordance |ρ| ≤ 0.08 and
clean 2-method sign-agreement 48% ≈ chance, **neither of which uses CRAK-Velo.** But the specific "0/598
agreement-set" number is *intrinsically* CRAK-dependent (it needs 3 sign-informative methods, and MultiVelo is
sign-structural), so it must be **demoted to a CRAK-inclusive sensitivity arm**, not the headline. Reframe the
headline onto the magnitude concordance (also the statistic the verify-gate `p3_concordance.py` recomputes;
`p4_permutation_fdr.py` is not gate-covered). **This is a reframe, not a method-swap** — do not run the sign test
over {multivelo, moflow, mvvae} to preserve a "clean 3-way 0/598" number; that silently reintroduces the exact
constant-sign error being fixed.
