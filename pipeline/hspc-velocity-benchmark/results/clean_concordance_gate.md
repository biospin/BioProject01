# Clean concordance gate — CRAK-independent recompute of the agreement-set (2026-07-05)

> **Correctness gate for the "0/598 agreement-set" headline** (novelty_strategy §0/§4.0).
> The published agreement-set is computed over sign-변가능 method = `{moflow, crakvelo, multivelovae}` —
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
