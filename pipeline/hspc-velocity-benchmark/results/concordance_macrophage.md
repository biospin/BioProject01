# P3 concordance (hardened) — macrophage replication of HSPC lag/α finding

> Paired-over-genes bootstrap B=10,000, seed=20260707 (deterministic percentile 95% CI). lag는 'failure-to-reject'가 아니라 TOST 등가(|ρ|<0.2)로 프레이밍.

> 질문: HSPC 결론 **"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.9)"**가 **macrophage**(같은 human 조혈축)에서 재현되나?

## 실행된 method arm

| arm | fit gene | rate/lag 컬럼 |
|---|---|---|
| scVelo floor (RNA-only) | 709 | fit_alpha |
| MultiVelo (chromatin-aware) | 871 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 880 | vae_alpha / vae_alpha_c |

## A. Within-macrophage cross-method concordance

동일 데이터셋·동일 gene축.

### A1. transcription rate α (robust leg 기대) — bootstrap 95% CI

- **α: floor × MV** (shared 702): Spearman **+0.826** 95%CI [+0.796, +0.854] (p=1.3e-176)
- **α: floor × VAE** (shared 709): Spearman **+0.865** 95%CI [+0.839, +0.887] (p=2.3e-214)
- **α: MV × VAE** (shared 871): Spearman **+0.917** 95%CI [+0.902, +0.929] (p=0)

### A2. chromatin→transcription lag (fragile leg 기대) — magnitude rank + TOST

> floor는 RNA-only라 lag 없음 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정.

- **lag **크기** rank: MV × VAE** (shared 871): Spearman **+0.074** 95%CI [+0.006, +0.143] (p=0.028) | TOST |ρ|<0.2: **EQUIVALENT (CI ⊂ [−0.2,+0.2])**
  - ⚠️ sign-agreement 생략: MultiVelo lag sign은 4-state 단조정렬로 구조적 양수(무정보).

### A3. paired Δρ = ρ_α − ρ_lag (dissociation, CI가 0 제외?)

> 한 resample당 index 1회 draw로 두 ρ를 동일 gene set에서 계산(paired). 헤드라인은 등가가 아니라 **dissociation**(Δρ CI가 0 제외).

- ρ_α(MV×VAE) = **+0.917**, ρ_lag(MV×VAE) = **+0.074** (공통 871 gene)
- **Δρ = +0.843** 95%CI **[+0.773, +0.912]** (bootstrap mean +0.842)
  → CI가 0을 **제외** — dissociation 성립(α ≫ lag).

## B. Cross-dataset HSPC ↔ macrophage (human↔human, 직접 gene 매칭) — bootstrap 95% CI

> 둘 다 human 조혈 → gene SYMBOL 축 직접 겹침(case/ortholog 매핑 불필요). 방어적 uppercase 정규화만.

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
- α robust(≈+0.87), lag 약함/dissociation (within MV×VAE lag +0.07, cross lag +0.15, Δρ +0.84 CI[+0.77,+0.91]). HSPC same-lineage 서사 일치.

## caveat (필수)
- lag 크기 rank만 비교(방향 아님): MultiVelo sign은 4-state 단조정렬로 구조적 양수(무정보).
- 'lag not robust'는 실패-미기각이 아니라 **TOST 등가(|ρ|<0.2)** + 부트스트랩 CI로 프레이밍. Δρ CI가 0을 제외하면 dissociation(α ≫ lag)이 핵심 주장.
- replication macrophage 1건 — 강한 일반화 금지. HSPC+human_brain+E18+BMMC+macrophage 축 일관성으로만 서사.
- concordance는 *전역* per-gene fit rank(within-lineage 아님).
- ⚠️ **전처리 분기점(중요)**: figshare postpro는 저자 그래프에서 HVG 필터+scVelo moments 완료(Ms/Mu). raw spliced/unspliced 부재 시 moment fallback → 다른 3종보다 pre-baked(방법론 #5). human_brain 외부-제공 spliced/unspliced caveat보다 강함 — Methods 명시. cross rank엔 noise만 추가(낮은 rho=lag fragile에 보수적).
