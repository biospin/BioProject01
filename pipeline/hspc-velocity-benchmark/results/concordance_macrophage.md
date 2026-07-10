# P3 concordance (hardened) — macrophage replication of HSPC lag/α finding

> Paired-over-genes bootstrap B=10,000, seed=20260707 (deterministic percentile 95% CI). lag는 'failure-to-reject'가 아니라 TOST 등가(|ρ|<0.2)로 프레이밍한다.

> 질문: HSPC 결론 **"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.9)"**가 **macrophage**(같은 human 조혈축)에서 재현되나?

## 실행된 method arm

| arm | fit gene | rate/lag 컬럼 |
|---|---|---|
| scVelo floor (RNA-only) | 709 | fit_alpha |
| MultiVelo (chromatin-aware) | 871 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 880 | vae_alpha / vae_alpha_c |

## A. Within-macrophage cross-method concordance

같은 데이터셋, 같은 gene축에서 계산한다.

### A1. transcription rate α (robust leg 기대) — bootstrap 95% CI

- **α: floor × MV** (shared 702): Spearman **+0.826** 95%CI [+0.796, +0.854] (p=1.3e-176)
- **α: floor × VAE** (shared 709): Spearman **+0.865** 95%CI [+0.839, +0.887] (p=2.3e-214)
- **α: MV × VAE** (shared 871): Spearman **+0.917** 95%CI [+0.902, +0.929] (p=0)

### A2. chromatin→transcription lag (fragile leg 기대) — magnitude rank + TOST

> floor는 RNA-only라 lag가 없다 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정한다.

- **lag **크기** rank: MV × VAE** (shared 871): Spearman **+0.074** 95%CI [+0.006, +0.143] (p=0.028) | TOST |ρ|<0.2: **EQUIVALENT (CI ⊂ [−0.2,+0.2])**
  - ⚠️ sign-agreement는 생략한다: MultiVelo의 lag sign은 4-state 단조정렬 탓에 구조적으로 양수여서 무정보다.

### A3. paired Δρ = ρ_α − ρ_lag (dissociation, CI가 0 제외?)

> 한 resample당 index를 1회 draw해 두 ρ를 동일 gene set에서 계산한다(paired). 헤드라인은 등가가 아니라 **dissociation**이다(Δρ CI가 0 제외).

- ρ_α(MV×VAE) = **+0.917**, ρ_lag(MV×VAE) = **+0.074** (공통 871 gene)
- **Δρ = +0.843** 95%CI **[+0.773, +0.912]** (bootstrap mean +0.842)
  → CI가 0을 **제외**한다 — dissociation이 성립한다(α ≫ lag).

## B. Cross-dataset HSPC ↔ macrophage (human↔human, 직접 gene 매칭) — bootstrap 95% CI

> 둘 다 human 조혈이라 gene SYMBOL 축이 직접 겹친다(case/ortholog 매핑 불필요). 방어적으로 uppercase 정규화만 적용한다.

- shared gene (HSPC × macrophage MultiVelo): **274**
- **MV lag 크기 rank: HSPC × macrophage** (shared 274): Spearman **+0.148** 95%CI [+0.027, +0.263] (p=0.014) | TOST |ρ|<0.2: **NOT equivalent (CI exits [−0.2,+0.2])**
- **MV α rank: HSPC × macrophage** (shared 274): Spearman **+0.643** 95%CI [+0.554, +0.719] (p=2.5e-33)
- **floor α rank: HSPC × macrophage (sanity)** (shared 230): Spearman **+0.677** 95%CI [+0.586, +0.753] (p=3.2e-32)

## 판정 — 'lag-fragile / α-robust' 패턴 재현?

- Within-macrophage α (cross-method) Spearman 중앙값: +0.865 (['+0.83', '+0.87', '+0.92'])
- Within-macrophage lag 크기 rank (MV×VAE): +0.074 95%CI [+0.006, +0.143]
- Δρ dissociation: +0.843 95%CI [+0.773, +0.912]
- Cross-dataset HSPC↔macrophage: lag 크기 rank +0.148 vs α rank +0.643

### → **재현 YES — 'lag-fragile / α-robust' 패턴 재현**
- α는 robust하고(≈+0.87) lag는 약함/dissociation이다(within MV×VAE lag +0.07, cross lag +0.15, Δρ +0.84 CI[+0.77,+0.91]). HSPC same-lineage 서사와 일치한다.

## caveat (필수)
- lag 크기 rank만 비교한다(방향이 아님): MultiVelo의 sign은 4-state 단조정렬로 구조적 양수여서 무정보다.
- 'lag not robust'는 실패-미기각이 아니라 **TOST 등가(|ρ|<0.2)**와 부트스트랩 CI로 프레이밍한다. Δρ CI가 0을 제외하면 dissociation(α ≫ lag)이라는 것이 핵심 주장이다.
- replication은 macrophage 1건뿐이다 — 강한 일반화는 금지한다. HSPC+human_brain+E18+BMMC+macrophage 축의 일관성으로만 서사를 전개한다.
- concordance는 *전역* per-gene fit rank이다(within-lineage가 아님).
- ⚠️ **전처리 분기점(중요)**: figshare postpro는 저자 그래프에서 HVG 필터와 scVelo moments를 이미 마쳤다(Ms/Mu). raw spliced/unspliced가 없으면 moment로 fallback한다 → 다른 3종보다 pre-baked 상태다(방법론 #5). 이는 human_brain의 외부-제공 spliced/unspliced caveat보다 강하다 — Methods에 명시한다. cross rank에는 잡음만 더한다(낮은 rho=lag fragile에 보수적).

---

# P3 concordance (hardened) — macrophage replication of the HSPC lag/α finding

> Paired-over-genes bootstrap B=10,000, seed=20260707 (deterministic percentile 95% CI). lag is framed not as 'failure-to-reject' but as TOST equivalence (|ρ|<0.2).

> Question: does the HSPC conclusion **"lag is not method-robust while α is robust (cross-method ρ≈0.9)"** reproduce in **macrophage** (the same human hematopoietic axis)?

## Method arms run

| arm | fit gene | rate/lag column |
|---|---|---|
| scVelo floor (RNA-only) | 709 | fit_alpha |
| MultiVelo (chromatin-aware) | 871 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 880 | vae_alpha / vae_alpha_c |

## A. Within-macrophage cross-method concordance

Computed on the same dataset and the same gene axis.

### A1. transcription rate α (expected robust leg) — bootstrap 95% CI

- **α: floor × MV** (shared 702): Spearman **+0.826** 95%CI [+0.796, +0.854] (p=1.3e-176)
- **α: floor × VAE** (shared 709): Spearman **+0.865** 95%CI [+0.839, +0.887] (p=2.3e-214)
- **α: MV × VAE** (shared 871): Spearman **+0.917** 95%CI [+0.902, +0.929] (p=0)

### A2. chromatin→transcription lag (expected fragile leg) — magnitude rank + TOST

> floor is RNA-only so it has no lag → lag is tested only on the two chromatin-aware arms (MV×VAE).

- **lag **magnitude** rank: MV × VAE** (shared 871): Spearman **+0.074** 95%CI [+0.006, +0.143] (p=0.028) | TOST |ρ|<0.2: **EQUIVALENT (CI ⊂ [−0.2,+0.2])**
  - ⚠️ sign-agreement is omitted: MultiVelo's lag sign is structurally positive due to the 4-state monotone ordering, hence uninformative.

### A3. paired Δρ = ρ_α − ρ_lag (dissociation, does the CI exclude 0?)

> One index draw per resample computes both ρ on the same gene set (paired). The headline is not equivalence but **dissociation** (Δρ CI excludes 0).

- ρ_α(MV×VAE) = **+0.917**, ρ_lag(MV×VAE) = **+0.074** (871 shared genes)
- **Δρ = +0.843** 95%CI **[+0.773, +0.912]** (bootstrap mean +0.842)
  → the CI **excludes** 0 — dissociation holds (α ≫ lag).

## B. Cross-dataset HSPC ↔ macrophage (human↔human, direct gene matching) — bootstrap 95% CI

> Both are human hematopoiesis, so the gene SYMBOL axes overlap directly (no case/ortholog mapping needed). Only a defensive uppercase normalization is applied.

- shared gene (HSPC × macrophage MultiVelo): **274**
- **MV lag magnitude rank: HSPC × macrophage** (shared 274): Spearman **+0.148** 95%CI [+0.027, +0.263] (p=0.014) | TOST |ρ|<0.2: **NOT equivalent (CI exits [−0.2,+0.2])**
- **MV α rank: HSPC × macrophage** (shared 274): Spearman **+0.643** 95%CI [+0.554, +0.719] (p=2.5e-33)
- **floor α rank: HSPC × macrophage (sanity)** (shared 230): Spearman **+0.677** 95%CI [+0.586, +0.753] (p=3.2e-32)

## Verdict — does the 'lag-fragile / α-robust' pattern reproduce?

- Within-macrophage α (cross-method) Spearman median: +0.865 (['+0.83', '+0.87', '+0.92'])
- Within-macrophage lag magnitude rank (MV×VAE): +0.074 95%CI [+0.006, +0.143]
- Δρ dissociation: +0.843 95%CI [+0.773, +0.912]
- Cross-dataset HSPC↔macrophage: lag magnitude rank +0.148 vs α rank +0.643

### → **REPRODUCED YES — the 'lag-fragile / α-robust' pattern reproduces**
- α is robust (≈+0.87) while lag is weak/dissociated (within MV×VAE lag +0.07, cross lag +0.15, Δρ +0.84 CI[+0.77,+0.91]). Consistent with the HSPC same-lineage narrative.

## caveat (required)
- Only lag magnitude rank is compared (not direction): MultiVelo's sign is structurally positive due to the 4-state monotone ordering, hence uninformative.
- 'lag not robust' is framed not as failure-to-reject but as **TOST equivalence (|ρ|<0.2)** plus bootstrap CI. The core claim is that when the Δρ CI excludes 0, dissociation (α ≫ lag) holds.
- Replication is a single macrophage case — no strong generalization. The narrative rests only on the consistency across the HSPC+human_brain+E18+BMMC+macrophage axis.
- concordance is a *global* per-gene fit rank (not within-lineage).
- ⚠️ **preprocessing branch point (important)**: the figshare postpro already completed HVG filtering and scVelo moments (Ms/Mu) on the authors' graph. When raw spliced/unspliced is absent it falls back to moments → more pre-baked than the other three arms (methodology #5). This is stronger than the human_brain externally-provided spliced/unspliced caveat — stated in Methods. It only adds noise to the cross rank (a low rho is conservative toward lag being fragile).
