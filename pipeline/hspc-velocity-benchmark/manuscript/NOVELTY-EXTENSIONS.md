# Novelty Extensions — post-4-dataset-replication (highest-leverage additions)

> novelty-strategist deliverable. **Extends** `manuscript/novelty_strategy.md` (2026-07-05) — does not
> repeat the landscape. Trigger: the 4-dataset replication (HSPC + human_brain + E18 mouse brain + human
> BMMC) is COMPLETE (`results/FINDINGS.md` §7) and the 2nd causal control (MoFlow ATAC-shuffle) closed
> limitation #4. Question answered here: given the story is now empirically solid, what 1–2 NEW additions
> most raise the paper's ceiling, and the cheapest way to establish each.
> Advisor consulted before writing. Scoop re-searched 2026-07-07 (below). Written 2026-07-07.

---

## TL;DR

- **The sharpest framing is not new evidence — it is a new NAME for the evidence you already have:**
  elevate "the lag is a **model-structural artifact**" → "the lag is **not identifiable** from multiome
  snapshots under the current model class, whereas α is." Same claim, one tier higher, and it is what
  earns Genome Biology / Cell Reports Methods instead of reading as "another no-universal-winner benchmark."
- **#1 new addition (drop-everything-for-a-week): a within-method practical-identifiability demonstration.**
  Profile the MultiVelo objective along the lag direction vs the α direction on already-fit genes. If the
  likelihood is near-flat along lag but sharp along α, you convert "non-identifiable" from an
  *interpretation* into a *demonstrated property*. CPU-only, reuses existing fits, no new data, well inside
  a week. Raises the ceiling more than a 5th replication dataset would.
- **#2 addition: the drug-timing bridge falls out of the identifiability frame for free** — no wet-lab, no
  scoop-risky public join. The quantity the original motivation wanted (lag) is non-identifiable; the
  quantity that IS identifiable and transferable (α, via day0-ATAC→α) is what a timing model must consume.
  State it as a **design principle established by this paper**, not a validated prediction.
- **Do NOT headline the cross-dataset α gradient (0.55 > 0.475 > 0.32).** It is n=3 on confounded points
  (tissue × species × stage bundled). Keep it as *suggestive support*; the durable claim is the categorical
  3-vs-3 contrast (α transfers everywhere, lag transfers nowhere), which you already own.
- **Scoop: clear on the identifiability angle.** Two NEW adjacent works to cite-and-differentiate (HALO,
  ArchVelo preprint); neither audits lag robustness or frames it as non-identifiable.

---

## 1. The single sharpest framing (committed)

**Thesis (one sentence):**
> In chromatin-informed single-cell velocity, the per-gene chromatin→transcription lag is **not identifiable**
> from multiome snapshots under the current model class — it is not constrained by the chromatin data
> (invariant to ATAC shuffling), not reproducible across methods, and not predictable from baseline —
> whereas the transcription rate α is identifiable and transferable across methods and datasets;
> timing-prediction models should be built on α (recoverable from day0 ATAC), not the lag.

**Why this framing, and why it clears the three constraints the task names:**

- **(a) Defensibly novel.** The prevailing published position is the *opposite* — that these
  chromatin→transcription lags are "substantive biological phenomena … distinguished from technical
  artifacts" (MoFlow, MultiVelo, and the priming literature all present the lag as a biological readout).
  A causal + identifiability falsification of that consensus is a genuine advance, not an incremental
  benchmark. The RNA-only identifiability literature exists (telegraph-model practical non-identifiability;
  Bayesian velocity identifiability) but **no one has brought the identifiability lens to the *cross-modal*
  chromatin-lag, and no one adds a causal shuffle control.** That two-part move is the white space.

- **(b) Not a MultiVelo takedown (desk-reject-safe).** Non-identifiability is a property of the
  **data + model class**, so there is no villain method — MultiVelo, MoFlow, MultiVeloVAE, CRAK-Velo all
  inherit it. This is structurally *not* an attack on any one tool; it explains *why* four independent,
  well-engineered methods disagree (different priors/regularizers land on different values of an
  unconstrained parameter). That is the most desk-reject-proof way to state the result.

- **(c) Constructive.** The frame unifies every asset you have under one concept AND hands the field a
  positive rule (use α / day0-ATAC→α). It is a critique that ends in a usable design principle, not an
  opinion piece.

**Why "not identifiable" beats the prior doc's "model-structural artifact":** identical evidence, but the
identifiability name (i) is a recognized, rigorous category reviewers respect, (ii) makes the
class-generality explicit (no single method to blame), and (iii) predicts the exact experiment in §2 that
turns interpretation into demonstration. Keep "model-structural" as the plain-language gloss in the abstract.

**How your existing evidence maps onto the frame (all already in `FINDINGS.md` — nothing new needed to
make the argument, only to *demonstrate* it — see §2):**

| Existing result | Identifiability reading |
| --- | --- |
| Cross-method concordance ≈0 (|ρ|≤0.08, sign 48%) | signature of a non-identified parameter: methods with different regularizers land on different values |
| ATAC-shuffle leaves lag unchanged (likelihood 0.239→0.237, ρ=0.72; 2nd method MoFlow ρ=0.52) | the **likelihood is flat w.r.t. the chromatin↔RNA coupling** → lag not identifiable *from the chromatin data* |
| Held-out lag not predictable from day0 ATAC (ρ≈chance) | no external variable constrains it either |
| α cross-method ρ=0.88, day0-ATAC→α held-out ρ=+0.31, transfers cross-dataset | α is the identifiable, transferable parameter |

**Venue tier:** unchanged from the prior call — **Genome Biology or Cell Reports Methods** (methods audit
+ causal control + constructive invariant). Bioinformatics fallback. The identifiability framing is what
*earns* that tier; the same evidence under a "concordance benchmark" title reads as incremental over the
two 2026 benchmarks.

---

## 2. #1 new addition — within-method practical-identifiability demonstration (the drop-everything-for-a-week)

**What it adds.** Today the non-identifiability claim is *inferred* from three empirical symptoms
(non-concordance, shuffle-invariance, non-predictability). This addition **demonstrates it directly** as a
property of the objective function, which is the difference between "we interpret this as an artifact" and
"we show the data cannot constrain this parameter." It is the single biggest ceiling-raiser available and
it needs no new data or GPU.

**Cheapest experiment.** On MultiVelo's already-fit genes (reuse the existing fits — no re-fitting the
model from scratch):
1. For each gene, fix α at its MLE. Scan the **switch-time-difference (the lag)** over a wide range,
   re-optimizing the nuisance parameters at each grid point, and record the data log-likelihood → a
   **profile likelihood along the lag direction.**
2. Do the mirror scan **along α** (fix the lag, scan α) → profile likelihood along α.
3. **Prediction that discriminates:** the lag profile is **near-flat** over a broad range (a flat valley =
   practically non-identifiable), while the α profile is **sharply peaked** (identifiable). Summarize per
   gene as a curvature/width ratio and show the population distribution (lag-flat, α-sharp).
4. This composes with the shuffle result you already have (likelihood flat under chromatin scrambling =
   flat along the chromatin-coupling axis specifically) into one coherent statement: *the objective is
   uninformative about the lag along multiple axes, informative about α.*

**Cost.** CPU-only, per-gene, single-method, reuses existing MultiVelo fits and the model's own likelihood
function. Comfortably inside one week. Optionally repeat the scan on MoFlow to show it is class-wide, but
**MultiVelo alone establishes the claim** — do not gate the week on the second method.

**Risk.** (i) The profile may turn out only *partially* flat (identifiable in a subset of genes). That is
still a strong, honest result — "the lag is identifiable only for the minority of genes with sharp
switch-time separation; genome-wide it is not" — and it would neatly explain MoFlow's weak "consistent
subset." (ii) Re-optimizing nuisance params at each grid point can be fiddly per method; mitigate by
starting from the MLE and using a coarse grid first. (iii) If the lag profile is *sharp* (identifiable),
the identifiability headline is falsified — but then the shuffle-invariance result would already be
contradictory, so this is a genuine, cheap internal-consistency check on your own central claim. Running
it protects you from a reviewer running it.

---

## 3. #2 new addition — the drug-timing bridge, reframed with zero wet-lab

**What it adds.** The paper opened with a drug-response-timing motivation (`drug_timing_arm_scout.md`
verdict: no public dataset clears the timing gate → wet-lab required). The identifiability frame lets you
**honor that motivation without the wet-lab and without the scoop-risky public join** the scout ruled out.
The logic is now a *result*, not a promise:

> The property a baseline→timing predictor requires is that the input feature be **gene-intrinsic and
> transferable across systems** (the scout's own R2 constraint: only gene-intrinsic features cross
> systems). This paper establishes empirically *which* velocity-derived quantity has that property: the
> non-identifiable lag does not transfer (cross-dataset ρ ≈ noise everywhere), while α does (cross-dataset
> ρ up to +0.55, day0-ATAC→α held-out +0.31). Therefore any epigenetic-drug timing model built on the
> chromatin-lag is built on a non-transferable, non-identifiable feature; the correct design consumes α /
> the day0-ATAC→α path.

**Cheapest experiment.** Essentially **zero** — it is a framing/writing move over results you already have
(FINDINGS §6–7). The only optional add: cite Todorovski's public decay-t½ (GSE229314) as the *external
control feature* the design principle would sit next to (per `drug_timing_arm_scout.md` §3.1), stated as
"here is the transferable-feature slot a future timing model fills," not as a run.

**Risk.** Overclaiming. Guardrail: present this as a **design principle established by the robustness/
identifiability results**, explicitly NOT a validated timing prediction (no timing ground truth exists).
One paragraph in Discussion, not a results section. This keeps the drug motivation as bookend narrative
(why the question matters) without inviting "you never tested timing" — because the honest claim is "we
show which feature is *eligible* to be tested."

---

## 4. What NOT to do (guardrails the advisor flagged)

- **Do not headline the cross-dataset α gradient (BMMC 0.55 > human_brain 0.475 > E18 0.32).** It is a
  monotonic trend on **n=3 confounded points** (tissue, species, and developmental stage all covary; each
  new point = a full pipeline run). A reviewer will shred a "conservation gradient" as an over-read slope.
  The **durable** version is the categorical, consistent-direction contrast you already own: **α transfers
  cross-dataset in all 3 externals (all positive, up to 0.55) while lag transfers in none (all ≈noise).**
  Report the ordering as *suggestive, n=3, confounds named*; make the 3-vs-3 contrast load-bearing instead.
- **Do not re-run the {mv, moflow, mvvae} sign-FDR** (re-introduces the constant-sign error the clean gate
  fixed; `clean_concordance_gate.md`). Headline stays the magnitude concordance.
- **Do not oversell day0-ATAC→α (+0.31)** as "the signal to use" — promising-but-modest (prior doc §2 guard).

---

## 5. SCOOP check (re-searched 2026-07-07, identifiability angle specifically)

**Verdict: the identifiability framing is CLEAR of scoop.** Targeted searches
("multiome velocity … non-identifiable / practical identifiability / profile likelihood / sloppy
parameters", "chromatin transcription lag not identifiable model artifact shuffle causal control") returned
**no** work framing the cross-modal chromatin-lag as non-identifiable, and **no** work applying a causal
shuffle control to it. The RNA-only identifiability literature (telegraph-model practical non-identifiability
[PMC12646643]; Bayesian velocity identifiability discussions) is adjacent and should be cited as "we bring
this lens to the *cross-modal* lag and add a causal control" — it does not touch the multiome lag.

**Two NEW adjacent works surfaced (not in `related_work.md`) — add as cite-and-differentiate / adjacent:**

| Work | Verified? | Label | Exact difference (why it does not scoop) |
| --- | --- | --- | --- |
| **HALO — hierarchical causal modeling for single-cell multi-omics** (Nat Commun 2025, s41467-025-63921-1) | URL confirmed via search; details [VERIFY] before citing | **must-cite-and-differentiate** | Models chromatin→transcription coupling *causally* as a method; it **proposes** a causal model, it does **not** audit whether the inferred lag is method-robust or identifiable, and runs no shuffle null. Cite as "causal-modeling neighbor"; our claim (the lag is not identifiable/robust) is orthogonal and, if anything, a caution their downstream users need. |
| **ArchVelo** (bioRxiv 2025.09.14.676182; also listed as Nat Commun 2026 s41467-026-74000-4 in `related_work.md` [5], author list still [VERIFY]) | preprint URL confirmed; the two records may be preprint+published of the same work — **reconcile before citing** | **adjacent** | Archetypal multi-omic velocity method benchmarked on hematopoiesis + brain; another same-family arm reporting lag/latent-time as a biological readout. Not a robustness audit. Strengthens our "every method reports the lag as signal, none audits it" line. |

**Threats re-confirmed as handled (no change):** MoFlow "consistent subset" (converted to supporting
result, `moflow_subset_confrontation.md`); the two 2026 general benchmarks (Cell Reports Methods 17-study;
bioRxiv 697314) score velocity *direction*, not lag; Todorovski 2024 (drug-arm scoop) neutralized by the
decay-controlled design in `drug_timing_arm_scout.md`. No 2025–2026 work reports velocity/chromatin-lag
non-robustness as a thesis.

**Action before submission:** verify HALO's scope (does it touch lag reproducibility at all?) and reconcile
the ArchVelo preprint-vs-published records + author list. Both are quick CrossRef/abstract checks; neither
threatens the thesis.

---

## 6. Honest verdict (extends prior §5)

The prior doc's "GO, re-order not re-scope" stands, and the 4-dataset replication + 2nd causal control have
**earned** the venue tier. The one remaining ceiling-raiser is *conceptual, not empirical*: rename the
central result from "model-structural artifact" to "**not identifiable under the model class**," and back
that name with the one cheap experiment that turns it from interpretation into demonstration.

**Single highest-leverage next move:** run the **within-method profile-likelihood demonstration (§2)** —
CPU, reuses existing fits, one week — and write the paper under the identifiability thesis (§1), with the
drug-timing design principle (§3) as the closing bridge. This does more for the paper's ceiling than any
5th replication dataset (e.g. SHARE-seq), because it converts the load-bearing claim from empirical
pattern into demonstrated property of the objective function.
