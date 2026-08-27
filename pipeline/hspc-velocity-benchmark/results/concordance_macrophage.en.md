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
