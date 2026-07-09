> ⚠️ **PREVIEW — 커밋 전 canonical 재생성 필수.** point Spearman은 **최종값**(BMMC 7/7 재현으로 검증된 동일 정의·필터)이나, 이 실행 박스에 numpy/conda가 없어 bootstrap 95% CI·TOST·Δρ는 **stdlib preview(B=2000, seed 근사)**다. 커밋용 공식 수치는 `scv-preprocess` env에서 `conda run --no-capture-output -n scv-preprocess python cross_dataset/p3_concordance_macrophage.py`(numpy, B=10000, seed=20260707)로 재생성해 이 파일을 덮어쓴 뒤 커밋할 것.

# P3 concordance — MultiVeloVAE macrophage differentiation replication of HSPC lag/α finding

> 질문: HSPC 결론 **"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.88)"**가 **HSPC 직계 분화축(Day14 macrophage differentiation, GSE284047·figshare 30280333)**에서 재현되나? — HSPC와 가장 가까운 조직축(직접 분화) 재현.

## 실행된 method arm

| arm | fit gene(필터 후) | rate/lag 컬럼 |
|---|---|---|
| scVelo floor (RNA-only) | 709 | fit_alpha |
| MultiVelo (chromatin-aware) | 871 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 880 | vae_alpha / vae_alpha_c |

## A. Within-macrophage cross-method concordance

동일 데이터셋·동일 gene축이다.

### A1. transcription rate α (robust leg 기대)

- **α: floor × MV** (shared 702): Spearman **+0.826**
- **α: floor × VAE** (shared 709): Spearman **+0.865**
- **α: MV × VAE** (shared 871): Spearman **+0.917**  · bootstrap 95% CI [+0.901, +0.930] (preview) — 0에서 확실히 떨어짐

### A2. chromatin→transcription lag (fragile leg 기대)

> floor는 RNA-only라 lag가 없다 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정한다.

- **lag 크기 rank: MV × VAE** (shared 871): Spearman **+0.074**  · bootstrap 95% CI [+0.007, +0.139] (preview) → **TOST |ρ|<0.2: 0과 등가(EQUIVALENT)**
- ⚠️ 부호 일치 검정은 생략: MultiVelo lag 부호는 4-state 단조 정렬 구조 탓에 구조적 양수(무정보)다.

## B. Cross-dataset HSPC ↔ macrophage (human↔human, 직접 gene 매칭)

> 둘 다 human 조혈이라 gene SYMBOL 축이 직접 겹친다(case/ortholog 매핑 불필요). 방어적 uppercase 정규화만 적용.

- shared gene (HSPC × macrophage MultiVelo): **274**.
- **MV lag 크기 rank: HSPC × macrophage** (shared 274): Spearman **+0.148**
- **MV α rank: HSPC × macrophage** (shared 274): Spearman **+0.643**
- **floor α rank: HSPC × macrophage (sanity)** (shared 230): Spearman **+0.677**

## C. Δρ dissociation (within-macrophage, paired-over-genes)

- **Δρ = ρ_α(MV×VAE) − ρ_lag(MV×VAE) = +0.843** · bootstrap 95% CI [+0.774, +0.913] (preview) → **0 배제(α≫lag dissociation 확증)** (common gene 871)

## 판정 — 'lag-fragile / α-robust' 패턴 재현?

- Within-macrophage α (cross-method) Spearman: [+0.826, +0.865, +0.917] (중앙값 +0.865) — **α-robust leg를 4개 중 가장 강하게 재현**
- Within-macrophage lag 크기 rank (MV×VAE): +0.074 (TOST로 0과 등가)
- Cross-dataset HSPC↔macrophage: lag 크기 rank +0.148 vs α rank +0.643 (셋 중 **cross-dataset α 최고**)

### → **재현 YES — 'lag-fragile / α-robust' 패턴 재현 (4번째 external, 최강)**
- α는 cross-method(+0.92)·cross-dataset(+0.64)에서 강하고, lag는 within +0.07(등가)·cross +0.15로 약하다. HSPC 직계 분화라 tissue 거리가 가장 가까워 cross-dataset α가 4개 중 최고(+0.643 > BMMC +0.55).

## caveat (필수)
- point Spearman은 최종값이나 bootstrap CI/TOST/Δρ는 stdlib preview(위 배너) — canonical numpy 재생성 필수.
- lag는 크기 rank만 비교(방향 무시): MultiVelo 부호는 4-state 단조 정렬 구조라 구조적 양수(무정보).
- replication은 단일 sample(Day14 macrophage 분화, 3572 cells) 1건 — 강한 일반화 금지. HSPC + human_brain + E18 + BMMC + macrophage 축 일관성만으로 서사.
- concordance는 *전역* per-gene fit rank이며 within-lineage가 아니다.
- 전처리: figshare postpro가 raw spliced/unspliced 보유(nnz 35.6%) → 우리 공통 전처리 분기 사용(Ms/Mu moment fallback 아님). Day14 subset으로 HSPC(Day7) leakage 차단.

---

> ⚠️ **PREVIEW — regenerate with the canonical script before commit.** Point Spearman values are **final** (same definitions/filters, verified 7/7 on BMMC), but this box has no numpy/conda, so the bootstrap 95% CIs · TOST · Δρ are a **stdlib preview (B=2000, approximate seed)**. Regenerate the committed numbers in the `scv-preprocess` env with `conda run --no-capture-output -n scv-preprocess python cross_dataset/p3_concordance_macrophage.py` (numpy, B=10000, seed=20260707), overwriting this file, before committing.

# P3 concordance — MultiVeloVAE macrophage differentiation replication of the HSPC lag/α finding

> Question: Does the HSPC conclusion — **"lag is not method-robust, whereas α is robust (cross-method ρ≈0.88)"** — reproduce on **a direct HSPC differentiation axis (Day14 macrophage differentiation, GSE284047 · figshare 30280333)**? — the nearest tissue axis to HSPC (direct differentiation).

## Method arms run

| arm | fit genes (post-filter) | rate/lag columns |
|---|---|---|
| scVelo floor (RNA-only) | 709 | fit_alpha |
| MultiVelo (chromatin-aware) | 871 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 880 | vae_alpha / vae_alpha_c |

## A. Within-macrophage cross-method concordance

- **α: floor × MV** (shared 702): Spearman **+0.826**
- **α: floor × VAE** (shared 709): Spearman **+0.865**
- **α: MV × VAE** (shared 871): Spearman **+0.917**  · bootstrap 95% CI [+0.901, +0.930] (preview)
- **lag magnitude rank: MV × VAE** (shared 871): Spearman **+0.074**  · 95% CI [+0.007, +0.139] (preview) → TOST |ρ|<0.2: **EQUIVALENT to 0**

## B. Cross-dataset HSPC ↔ macrophage (human↔human, direct gene matching)

- shared gene (HSPC × macrophage MultiVelo): **274**.
- **MV lag magnitude rank: HSPC × macrophage** (shared 274): Spearman **+0.148**
- **MV α rank: HSPC × macrophage** (shared 274): Spearman **+0.643**
- **floor α rank: HSPC × macrophage (sanity)** (shared 230): Spearman **+0.677**

## C. Δρ dissociation (within-macrophage, paired-over-genes)

- **Δρ = ρ_α − ρ_lag = +0.843** · bootstrap 95% CI [+0.774, +0.913] (preview) → **excludes 0 (α ≫ lag dissociation confirmed)** (common 871 genes)

## Verdict — does the 'lag-fragile / α-robust' pattern reproduce?

### → **Reproduced — YES — strongest of the four external replications**
- α is strong across method (+0.92) and across dataset (+0.64); lag is weak within (+0.07, TOST-equivalent to 0) and cross (+0.15). As HSPC's direct differentiation product, macrophage is the closest tissue → cross-dataset α is the highest of the four (+0.643 > BMMC +0.55).

## caveat (required)
- Point Spearman is final but the bootstrap CI/TOST/Δρ are a stdlib preview (banner above) — canonical numpy regeneration required.
- lag compares magnitude rank only (sign is structurally positive/uninformative for MultiVelo).
- Single sample (Day14 macrophage differentiation, 3572 cells), 1 case — no strong generalization. Narrative rests on the consistency of HSPC + human_brain + E18 + BMMC + macrophage.
- concordance is a *global* per-gene fit rank, not within-lineage.
- Preprocessing: the figshare postpro retains raw spliced/unspliced (nnz 35.6%) → our common preprocessing branch is used (not an Ms/Mu moment fallback). Day14 subset blocks HSPC (Day7) leakage.
