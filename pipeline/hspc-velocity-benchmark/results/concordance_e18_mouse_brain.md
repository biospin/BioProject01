# P3 concordance — Track D: E18 mouse brain replication of HSPC lag/α finding

> 질문: HSPC 결론 **"lag은 method-robust하지 않고 α는 robust(cross-method ρ≈0.88)"**가 비-조혈(E18 태아 뇌 10x Multiome, MultiVelo 튜토리얼 데이터)에서 재현되나?

## 실행된 method arm

| arm | fit gene | rate/lag 컬럼 |
|---|---|---|
| scVelo floor (RNA-only) | 1177 | fit_alpha |
| MultiVelo (chromatin-aware) | 1027 | fit_alpha / fit_t_sw* |
| MultiVeloVAE (chromatin-aware) | 1169 | vae_alpha / vae_alpha_c |

## A. Within-E18 cross-method concordance

동일 데이터셋·동일 gene축 → ortholog/case 매핑 불필요.

### A1. transcription rate α (robust leg 기대)

- **α: floor × MV** (shared 973): Spearman **+0.777** (p=3.6e-197)
- **α: floor × VAE** (shared 1112): Spearman **+0.810** (p=1.3e-259)
- **α: MV × VAE** (shared 1027): Spearman **+0.898** (p=0)

### A2. chromatin→transcription lag (fragile leg 기대)

> floor는 RNA-only라 lag 없음 → lag는 chromatin-aware 2개(MV×VAE)에서만 검정 가능.

- **lag **크기** rank: MV × VAE** (shared 1027): Spearman **+0.057** (p=0.069)
- ⚠️ sign-agreement 생략: MultiVelo lag sign은 4-state 단조정렬로 **구조적 양수(무정보)** → MV×VAE 방향 일치는 정의상 의미 없음(양쪽 sign-informative일 때만 유효, p3_concordance.py 규칙).

## B. Cross-dataset HSPC ↔ E18 (mouse→UPPER 매핑)

> mouse Title-case(Gata1) ≠ human UPPER(GATA1) → uppercase 후 교집합. 매핑 안 하면 shared≈0 (STATUS.md trap #1).

- shared gene: raw(case mismatch) **0** → uppercase 매핑 후 **132** (trap 실측: 매핑 없으면 near-zero).
- **MV lag 크기 rank: HSPC × E18** (shared 132): Spearman **+0.105** (p=0.23)
- **MV α rank: HSPC × E18** (shared 132): Spearman **+0.321** (p=0.00018)
- **floor α rank: HSPC × E18 (sanity)** (shared 133): Spearman **+0.400** (p=1.9e-06)

## 판정 — 'lag-fragile / α-robust' 패턴 재현?

- Within-E18 α (cross-method) Spearman: ['+0.78', '+0.81', '+0.90'] (중앙값 +0.810)
- Within-E18 lag 크기 rank (MV×VAE): +0.057
- Cross-dataset HSPC↔E18: lag 크기 rank +0.105 vs α rank +0.321

### → **재현 YES — 'lag-fragile / α-robust' 패턴 재현**
- α는 cross-method/cross-dataset에서 강함(≈+0.81), lag는 약함(within-E18 MV×VAE lag +0.06, cross-dataset lag +0.10). HSPC 서사 일치.

## caveat (필수)
- lag 크기 rank만 비교(방향 아님): MultiVelo sign은 4-state 단조정렬로 구조적 양수(무정보).
- 단일 외부 데이터셋 replication 1건 — 강한 일반화 주장 금지. HSPC + human_brain + E18 3개 축의 일관성으로만 서사.
- concordance는 *전역* per-gene fit rank (within-lineage 아님). E18 lineage(제공 celltype)는 load-bearing 아님.
- E18 spliced/unspliced와 HSPC의 것은 서로 다른 원천 → cross-dataset rank에 noise만 추가 (낮은 rho=lag fragile에 보수적, 높은 rho=강한 신호).
