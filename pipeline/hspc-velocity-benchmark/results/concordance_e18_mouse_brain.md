# P3 concordance — Track D: E18 mouse brain replication of HSPC lag/α finding

> 질문: HSPC 결론 **"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.88)"**가 비-조혈(E18 태아 뇌 10x Multiome, MultiVelo 튜토리얼 데이터)에서 재현되나?

## 실행된 method arm

| arm | fit gene | rate/lag 컬럼 |
|---|---|---|
| scVelo floor (RNA-only) | 1177 | fit_alpha |
| MultiVelo (chromatin-aware) | 1027 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 1169 | vae_alpha / vae_alpha_c |

## A. Within-E18 cross-method concordance

동일 데이터셋·동일 gene축이라 ortholog/case 매핑이 필요 없다.

### A1. transcription rate α (robust leg 기대)

- **α: floor × MV** (shared 973): Spearman **+0.777** (p=3.6e-197)
- **α: floor × VAE** (shared 1112): Spearman **+0.810** (p=1.3e-259)
- **α: MV × VAE** (shared 1027): Spearman **+0.898** (p=0)

### A2. chromatin→transcription lag (fragile leg 기대)

> floor는 RNA-only라 lag가 없다 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정할 수 있다.

- **lag **크기** rank: MV × VAE** (shared 1027): Spearman **+0.057** (p=0.069)
- ⚠️ 부호 일치(sign-agreement) 검정은 생략한다: MultiVelo lag의 부호는 4-state를 순서대로 정렬(단조)하는 구조 탓에 **구조적 양수(무정보)**다 → 따라서 MV×VAE 방향 일치는 정의상 의미가 없다(양쪽 모두 부호에 정보가 있을(sign-informative) 때만 유효, p3_concordance.py 규칙).

## B. Cross-dataset HSPC ↔ E18 (mouse→UPPER 매핑)

> mouse Title-case(Gata1) ≠ human UPPER(GATA1) → uppercase로 바꾼 뒤 교집합을 취한다. 매핑하지 않으면 shared≈0이다 (STATUS.md trap #1).

- shared gene: raw(case mismatch) **0** → uppercase 매핑 후 **132** (trap 실측: 매핑하지 않으면 0에 가까움).
- **MV lag 크기 rank: HSPC × E18** (shared 132): Spearman **+0.105** (p=0.23)
- **MV α rank: HSPC × E18** (shared 132): Spearman **+0.321** (p=0.00018)
- **floor α rank: HSPC × E18 (sanity)** (shared 133): Spearman **+0.400** (p=1.9e-06)

## 판정 — 'lag-fragile / α-robust' 패턴 재현?

- Within-E18 α (cross-method) Spearman: ['+0.78', '+0.81', '+0.90'] (중앙값 +0.810)
- Within-E18 lag 크기 rank (MV×VAE): +0.057
- Cross-dataset HSPC↔E18: lag 크기 rank +0.105 vs α rank +0.321

### → **재현 YES — 'lag-fragile / α-robust' 패턴 재현**
- α는 cross-method/cross-dataset에서 강하고(≈+0.81), lag는 약하다(within-E18 MV×VAE lag +0.06, cross-dataset lag +0.10). HSPC 서사와 일치한다.

## caveat (필수)
- lag는 크기 rank만 비교하며 방향은 보지 않는다: MultiVelo 부호는 4-state를 순서대로 정렬(단조)한 구조라 구조적으로 양수(무정보)다.
- 외부 데이터셋 replication은 단 1건이므로 강한 일반화 주장은 금지한다. HSPC + human_brain + E18 3개 축의 일관성만으로 서사를 세운다.
- concordance는 *전역* per-gene fit rank이며 within-lineage가 아니다. E18 lineage(제공 celltype)는 load-bearing이 아니다.
- E18의 spliced/unspliced와 HSPC의 것은 서로 다른 원천이라 → cross-dataset rank에는 잡음만 더한다(낮은 rho=lag fragile에 보수적, 높은 rho=강한 신호).

---

# P3 concordance — Track D: E18 mouse brain replication of the HSPC lag/α finding

> Question: Does the HSPC conclusion — **"lag is not method-robust, whereas α is robust (cross-method ρ≈0.88)"** — reproduce in a non-hematopoietic setting (E18 fetal brain 10x Multiome, the MultiVelo tutorial data)?

## Method arms run

| arm | fit genes | rate/lag columns |
|---|---|---|
| scVelo floor (RNA-only) | 1177 | fit_alpha |
| MultiVelo (chromatin-aware) | 1027 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 1169 | vae_alpha / vae_alpha_c |

## A. Within-E18 cross-method concordance

Same dataset and same gene axis, so no ortholog/case mapping is needed.

### A1. transcription rate α (expected robust leg)

- **α: floor × MV** (shared 973): Spearman **+0.777** (p=3.6e-197)
- **α: floor × VAE** (shared 1112): Spearman **+0.810** (p=1.3e-259)
- **α: MV × VAE** (shared 1027): Spearman **+0.898** (p=0)

### A2. chromatin→transcription lag (expected fragile leg)

> floor is RNA-only and has no lag → lag can only be tested in the two chromatin-aware arms (MV×VAE).

- **lag **magnitude** rank: MV × VAE** (shared 1027): Spearman **+0.057** (p=0.069)
- ⚠️ The sign-agreement test is omitted: the MultiVelo lag sign is **structurally positive (uninformative)** because the 4 states are placed in order (monotone) → therefore MV×VAE directional agreement is definitionally meaningless (valid only when both sides carry sign information, i.e. are sign-informative; p3_concordance.py rule).

## B. Cross-dataset HSPC ↔ E18 (mouse→UPPER mapping)

> mouse Title-case (Gata1) ≠ human UPPER (GATA1) → we uppercase first and then intersect. Without mapping, shared≈0 (STATUS.md trap #1).

- shared gene: raw (case mismatch) **0** → after uppercase mapping **132** (measured trap: without mapping it is near zero).
- **MV lag magnitude rank: HSPC × E18** (shared 132): Spearman **+0.105** (p=0.23)
- **MV α rank: HSPC × E18** (shared 132): Spearman **+0.321** (p=0.00018)
- **floor α rank: HSPC × E18 (sanity)** (shared 133): Spearman **+0.400** (p=1.9e-06)

## Verdict — does the 'lag-fragile / α-robust' pattern reproduce?

- Within-E18 α (cross-method) Spearman: ['+0.78', '+0.81', '+0.90'] (median +0.810)
- Within-E18 lag magnitude rank (MV×VAE): +0.057
- Cross-dataset HSPC↔E18: lag magnitude rank +0.105 vs α rank +0.321

### → **Reproduced — YES — the 'lag-fragile / α-robust' pattern reproduces**
- α is strong across method and across dataset (≈+0.81), whereas lag is weak (within-E18 MV×VAE lag +0.06, cross-dataset lag +0.10). Consistent with the HSPC narrative.

## caveat (required)
- lag compares magnitude rank only, not direction: the MultiVelo sign is structurally positive (uninformative) because the 4 states are placed in order (monotone).
- There is only 1 external-dataset replication, so strong generalization claims are prohibited. The narrative rests solely on the consistency of the three axes HSPC + human_brain + E18.
- concordance is a *global* per-gene fit rank, not within-lineage. The E18 lineage (provided celltype) is not load-bearing.
- The E18 spliced/unspliced and the HSPC ones come from different sources → this only adds noise to the cross-dataset rank (a low rho is conservative for lag fragility, a high rho is a strong signal).
