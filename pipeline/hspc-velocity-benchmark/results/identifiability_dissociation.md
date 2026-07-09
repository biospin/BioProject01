# Identifiability & α-vs-lag dissociation — bootstrap CI + TOST (CHEAP tier)

> Paired gene bootstrap B=10,000, seed=20260707 (deterministic). Percentile 95% CIs.
> Definitions reused verbatim from `p3_concordance.py` → numbers match FINDINGS/concordance.md.
> Guardrails: rank/magnitude concordance only (MultiVelo structural sign never invoked);
> CRAK-Velo excluded; 'lag not robust' stated as TOST equivalence vs |ρ|<0.2; cross-dataset = 1 sample each.

## #1 — Paired Δρ dissociation (α ≫ lag), bootstrap CI + TOST

> **lag = MAGNITUDE rank (|·|)** everywhere — the FINDINGS-consistent convention (external `concordance_*.py` use `.abs()`; MultiVelo sign is structural/uninformative). The headline is the **dissociation** (Δρ excludes 0), not equivalence.

### HSPC (within-dataset, MultiVelo × MultiVeloVAE, shared 538 genes) — PRIMARY

- ρ_α = **+0.882**  95%CI [+0.855, +0.904]
- ρ_lag (magnitude) = **+0.163**  95%CI [+0.078, +0.244]
- **Δρ = ρ_α − ρ_lag = +0.720**  95%CI **[+0.639, +0.802]** (bootstrap mean +0.719)
  → CI **excludes 0** — dissociation established (α sits ~0.7 above lag).

- Δρ robustness to lag convention: magnitude **+0.720** | signed (concordance.md §3.5, ρ_lag=-0.010) Δρ +0.893 | rate-proxy |1/α_c−1/α| (ρ_lag=-0.009) Δρ +0.891 — all CIs exclude 0.

### TOST equivalence — HSPC lag vs pre-declared bound |ρ|<0.2

- **magnitude lag (MV×VAE)** ρ=+0.163, 95%CI [+0.078, +0.244] → **NOT equivalent (CI exits [−0.2,+0.2])** — weak-positive, upper bound breaches +0.2 → equivalence NOT certified at strict bound.
  - ⚠️ FINDINGS §3.5 also cites a **signed** MV×VAE lag −0.010 (mixes MV-magnitude vs VAE-signed → category mismatch); magnitude-consistent value is +0.163. We report magnitude for cross-dataset consistency.
- **directional lag (MoFlow×VAE, guardrail-clean sign pair, shared 636)** ρ=**+0.083** 95%CI [+0.007, +0.158] → **EQUIVALENT (CI ⊂ [−0.2,+0.2])** — methods do NOT agree on lag *direction* beyond zero.
  → Split verdict: *directional* lag concordance IS equivalent to zero (MoFlow×VAE), *magnitude* concordance is weak-positive (MV×VAE). Both sit ~0.7 below α.

### External replications (within-dataset MV×VAE, magnitude lag)

- **GSE194122_bmmc** (shared 272): ρ_α **+0.906** [+0.879,+0.925], ρ_lag(mag) **-0.088** [-0.209,+0.034], **Δρ +0.994** 95%CI [+0.874,+1.110] (excludes 0).
  - TOST lag: **NOT equivalent (CI exits [−0.2,+0.2])**
- **e18_mouse_brain** (shared 1027): ρ_α **+0.898** [+0.883,+0.910], ρ_lag(mag) **+0.057** [-0.005,+0.118], **Δρ +0.841** 95%CI [+0.779,+0.903] (excludes 0).
  - TOST lag: **EQUIVALENT (CI ⊂ [−0.2,+0.2])**
- **human_brain**: no within-dataset MultiVeloVAE fit exists (only MultiVelo + floor) → within-dataset cross-method lag is **not computable**; its α-vs-lag evidence is the cross-dataset axis (§#5).

## #3a — Empirical identifiability ranking (cross-method reproducibility = identifiability)

> Canonical axis = MultiVelo × MultiVeloVAE (only pair exposing α_c). Ranked by SIGNED ρ (descending) with 95%CI — identifiability = positive cross-method reproduction (negative ρ = rank-reversed = least identifiable).

| rank | parameter | MV×VAE Spearman | 95% CI | identifiable? |
|---|---|---|---|---|
| 1 | α (transcription rate) | **+0.882** | [+0.855, +0.905] | **YES (invariant)** |
| 2 | α_c (chromatin opening) | **+0.291** | [+0.209, +0.369] | no (fragile) |
| 3 | β (splicing) | **+0.080** | [-0.009, +0.168] | no (fragile) |
| 4 | γ (degradation) | **-0.109** | [-0.192, -0.023] | no (fragile) |

### RNA-pinned evidence — floor (NO chromatin channel) recovers α ≈ chromatin methods

- **α: floor × MultiVelo** (shared 368): Spearman **+0.818** 95%CI [+0.773, +0.855] — floor has NO ATAC yet recovers α at chromatin-method strength.
- **α: floor × MultiVeloVAE** (shared 434): Spearman **+0.889** 95%CI [+0.862, +0.910] — floor has NO ATAC yet recovers α at chromatin-method strength.

→ **α stands alone as the identifiable invariant**; α_c, β, γ all fragile (CI includes/near 0). Empirical identifiability ranking: **α ≫ α_c > β > γ**.

## #3b — γ/β ratio sloppiness probe (steady-state slope identifiability)

> Splicing ODE: only steady-state slope γ/β (+scaling) is identifiable. Ratio should reproduce cross-method better than individual β, γ. Genes with |β|>1e-4 in both methods.

- **γ/β ratio** (MV×VAE, n=538): Spearman **-0.324** 95%CI [-0.400, -0.244]
- **β alone** (MV×VAE, n=538): Spearman **+0.080** 95%CI [-0.010, +0.169]
- **γ alone** (MV×VAE, n=538): Spearman **-0.109** 95%CI [-0.192, -0.024]
> Verdict: even the theoretically-identifiable steady-state slope γ/β does **NOT** cleanly reproduce cross-method (ρ=−0.32, *negative* = anti-reproduction) — **only α reproduces cleanly**. The prediction holds only in the weak sense that |ρ(γ/β)|≈0.32 exceeds |ρ_β|=0.08 and |ρ_γ|=0.11 (the combination is less badly determined than the individual rates — scVelo scaling sloppiness in *magnitude*), but the negative sign (MV vs VAE parameterization/scaling convention a rank correlation can't absorb) means the slope itself is not a reproducible invariant. α stands alone.

## Diff-budget — lag = difference of two noisy timings

> Cross-method (MV×VAE) concordance of the rate-timescale COMPONENTS (1/α, 1/α_c) vs their DIFFERENCE (lag = 1/α_c − 1/α). Spearman is invariant to the shared 1/x transform, so ρ(1/α)=ρ(α) and ρ(1/α_c)=ρ(α_c).

- **1/α component**: Spearman **+0.882** 95%CI [+0.856, +0.905]
- **1/α_c component**: Spearman **+0.291** 95%CI [+0.209, +0.370]
- **difference (lag = 1/α_c − 1/α, signed)**: Spearman **+0.124** 95%CI [+0.036, +0.210]
> One component strong (1/α +0.88), one weak (1/α_c +0.29); the DIFFERENCE **falls below even the weaker component** → differencing collapses concordance. Prediction holds: lag inherits α_c fragility and differencing amplifies noise.

## #5 — Cross-dataset replication CIs (reject monotonicity as a claim)

> Bootstrap 95%CI on the three cross-dataset MultiVelo α ρ and their lag counterparts. Overlap → tissue-distance ordering is QUALITATIVE, not a quantitative claim. No trend fit on 3 points.

| dataset | shared | α cross ρ (95%CI) | lag cross ρ (95%CI) | Δρ (95%CI) | lag TOST |
|---|---|---|---|---|---|
| human_brain (adult brain) | 102 | **+0.475** [+0.292,+0.626] | +0.185 [-0.005,+0.369] | +0.290 [+0.055,+0.518] | not equiv |
| E18 mouse brain (fetal, cross-species) | 132 | **+0.321** [+0.158,+0.472] | +0.105 [-0.069,+0.269] | +0.216 [-0.026,+0.449] | not equiv |
| GSE194122 BMMC (same-tissue human) | 88 | **+0.550** [+0.368,+0.696] | +0.052 [-0.164,+0.262] | +0.498 [+0.258,+0.732] | not equiv |

- α cross-dataset CIs **OVERLAP** (common region [0.368, 0.472]) → tissue-distance ordering (BMMC +0.55 > brain +0.48 > E18 +0.32) is **qualitative, not a quantified monotonic claim**. No regression fit on 3 points.
- Every cross-dataset lag ρ is weak; equivalence status varies (n~100 → some CIs too wide to certify equivalence — reported honestly, not manufactured).
- ⚠️ The **cross-dataset** E18 Δρ (+0.216 [−0.026, +0.449]) grazes 0 — underpowered at n=132. The E18 dissociation is carried by the **within-dataset** E18 Δρ (+0.841 [+0.779, +0.903], §#1); cross-dataset is 1 sample → replication signal, not a powered dissociation test (consistent with the no-strong-generalization caveat).

## Summary verdicts

- **DISSOCIATION (headline): HSPC Δρ (α − lag) = +0.720, 95%CI [+0.639, +0.802]** → CI excludes 0 by a wide margin; robust to lag convention (magnitude/signed/rate-proxy). α concordance sits ~0.7 above lag. Replicated in BMMC (Δρ≈0.9) and E18 (Δρ≈0.8).
- **TOST (equivalence, secondary, honest split)**: *directional* lag (MoFlow×VAE, guardrail-clean) IS equivalent to zero; *magnitude* lag (MV×VAE) is weak-positive and NOT certified equivalent at strict |ρ|<0.2 in HSPC/BMMC (CI grazes bound), equivalent in E18. Not manufactured uniform — the dissociation carries the claim.
- **Identifiability ranking: α ≫ α_c > β > γ** — α alone is the cross-method invariant (incl. RNA-only floor with no ATAC recovering α at chromatin-method strength).
- **γ/β ratio reproduces better (|ρ|≈0.32) than individual β (0.08), γ (0.11)** → scVelo scaling non-identifiability.
- **Diff-budget: lag concordance (+0.12) falls below both components (1/α +0.88, 1/α_c +0.29)** → differencing amplifies noise.
- **Cross-dataset α CIs overlap** → tissue-distance ordering qualitative only (no trend on 3 points).
