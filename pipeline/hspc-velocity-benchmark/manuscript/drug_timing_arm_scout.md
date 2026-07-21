# Drug-timing arm — data verification + design lock (literature scout)

> Scope: unblock **Part 2** of `PAPER-PLAN.md` (predict epigenetic-drug response *timing* from baseline
> chromatin→transcription coupling). The arm is blocked on **data**, not compute. This is the
> data-verification + design deliverable, not a run.
> Author: literature-scout. Date accessed: **2026-07-06**. All accessions re-verified this session
> against GEO `acc.cgi` and the source papers (not the prior one-line summaries).

---

## 0. Verdict (decisive)

**No public dataset clears the full gate** (epigenetic drug + ≥3 *transcriptome* timepoints +
hematopoietic + single-cell/multiome bonus). Re-verification this session **tightened, not loosened**,
the earlier conclusion:

- **GSE256354** (human AML, HMA, single-cell multi-omics — the most attractive on paper) collects
  single-cell data at a **single 72 h timepoint** → fails the ≥3-timepoint gate.
- **GSE190785** (human AML, LSD1i — the candidate that looked best on drug + hours-grid + human)
  has its 2/6/24 h grid **only in CUT&Tag chromatin**; the **bulk RNA-seq is a single 24 h endpoint**
  drug-condition comparison → fails the transcriptome-timecourse gate.
- **GSE229314** (Todorovski, the scoop) — its fine 5 min–12 h grid is the **SLAM/TT-seq baseline
  decay-measurement** grid, *not* a drug-response outcome timecourse; drug readout is 2 h + 6 h discrete,
  bulk, no ATAC.
- **GSE201662** is the **only** candidate meeting the literal ≥3-*designed*-timepoint transcriptome
  bar (5 d / 14 d / 4 wk) — but it is mouse, bulk, days-to-weeks scale, IDH1-inhibitor (only
  *indirectly* epigenetic), the 4 wk arm is a **relapse regime change** (not a monotonic onset curve),
  and n = 14 total → **unusable for a per-gene kinetic t½ fit**.

**Recommendation:** treat the arm as **wet-lab-required for the headline timing claim.** Use public
data only in two supporting roles: (i) **GSE229314's decay t½** as the *mandatory control feature*
and the scoop reference; (ii) **GSE201662** as a *feasibility/plumbing demonstrator only* (does the
join + nested-model machinery run end-to-end on a coarse monotonic-trend proxy?), explicitly **not**
a validation of the timing hypothesis. Do **not** headline any chromatin-lag→timing result on
GSE201662. This matches — and hardens — the 2026-06-14 lit-search conclusion.

---

## 1. Candidate verification table (re-verified 2026-07-06)

| Accession | Epigenetic drug? | ≥3 *transcriptome* timepoints? | sc or bulk transcriptome | Assay(s) | Organism / system | Gene-axis → human HSPC | Public / retrievable | Gate |
|---|---|---|---|---|---|---|---|---|
| **GSE229314** (Todorovski 2024) | Transcriptional inhibitors JQ1 (BRD4), A-485 (p300/CBP), AZ-5576 / THZ531 (CDK9/12), ActD — chromatin-adjacent, not classic chromatin-*writer* modulators | **No.** Drug-response readout = **2 h (SLAM+inhibitor) + 6 h (MAC-seq)**, discrete. The 5 min–12 h grid = SLAM/TT-seq **baseline decay** measurement, not a drug-response outcome | **bulk** | SLAM-seq, TT-seq, MAC-seq, total RNA-seq | human **K562, THP-1** (leukemia lines) | human, direct gene symbols; leukemia line ≠ HSPC | **Open** (released 2023-04-17; 89 samples; SuperSeries) | **FAIL** (no drug timecourse; bulk; no ATAC) — but = **decay-control source + scoop ref** |
| **GSE256354** (Bond 2025, *Leukemia*) | **Yes** — decitabine (DAC) + azacitidine (AZA), bona-fide HMA/DNMTi | **No.** "every 24 h for 72 h … after 72 h (day 3), cells collected for single-cell analyses." Single-cell profiling at **one 72 h timepoint**. Later day 6/10/17 = colony assays, not sc profiling | **single-cell** (scNMT-seq for HL-60; scTEM-seq for MOLM-13/MV-4-11 = RNA + methylation) | scNMT-seq, scTEM-seq, RNA-seq, methylation | human **HL-60, MOLM-13, MV-4-11** (leukemia lines) | human, direct; leukemia line ≠ HSPC | **Open** (released 2025-07-21; 2,765 samples) | **FAIL** (single timepoint; sc, but no timing axis; methylation not ATAC) |
| **GSE201662** | IDH1 inhibitor **AG-120 / ivosidenib** (± AZA in the broader study) — *indirectly* epigenetic (blocks 2-HG → restores TET / KDM demethylation), not a direct chromatin-modifier | **Yes (literal)** — **3 designed durations: 5 d, 14 d, 4 wk-relapse**. ⚠ 4 wk = **relapse regime change**, not a monotonic response-onset point | **bulk** | bulk RNA-seq | **mouse** IDH1-mutant AML (sorted leukemic progenitors) | **mouse → human ortholog** mapping required | **Open** (public 2022-08-17; **14 samples**) | **PARTIAL / unusable-for-timing** (only dataset meeting ≥3-timepoint bar, but mouse + coarse days + relapse regime + n=14 → no per-gene t½ fit) |
| **GSE190785** (Dual FLT3/LSD1, MYC-SE study) | **Yes** — LSD1i **GSK2879552** (+ FLT3i quizartinib) — bona-fide histone-demethylase inhibitor | **No.** Bulk RNA-seq = **single 24 h endpoint**, drug-condition comparison (DMSO / quiz / GSK / combo × 3 reps). 2/6/24 h grid exists **only in CUT&Tag** (chromatin) | **bulk** (+ scATAC, ChIP, ATAC, CUT&Tag/RUN) | bulk RNA-seq, ATAC-seq, scATAC-seq, ChIP-seq, CUT&Tag, CUT&RUN | human **MOLM13 + primary AML** (67 samples) | human, direct; leukemia line ≠ HSPC | **Open** | **FAIL** (RNA is single-timepoint condition comparison; timecourse only in chromatin assay) |

Reference (not a pairing candidate): **GSE120715** (Bhagwat, I-BET / BETi) = baseline chromatin →
drug **sensitivity** (magnitude), no timecourse — conceptual reference for "baseline chromatin →
response," not timing. Broad NCBI/GEO + web re-search (2026-07-06) surfaced **no** human, in-vitro,
epigenetic-drug scRNA/multiome **timecourse** with ≥3 post-treatment transcriptome timepoints.
Nearest adjacent hits (GSE141834 T47D dexamethasone 1–18 h; clinical pembrolizumab+decitabine sc)
are non-hematopoietic-in-vitro or glucocorticoid / controlled-access → out of gate.

**Gate legend:** epigenetic drug + **≥3 timepoints in the transcriptome readout** (the axis that
defines "timing") + single-cell/multiome bonus + hematopoietic + gene-axis matchable to human HSPC +
openly retrievable.

---

## 2. Recommendation

**None qualifies for a validating proof-of-concept.** Be explicit about *why the gate is not a
formality*: "timing" is defined on the **transcriptome time axis**, and every human/epigenetic-drug
candidate collapses that axis to a **single timepoint** (GSE256354 72 h; GSE190785 RNA 24 h) or has
**no drug timecourse at all** (GSE229314 = 2 h/6 h discrete). The only dataset with ≥3 *designed*
transcriptome timepoints (GSE201662) buys the timepoints at the cost of species (mouse), resolution
(days–weeks vs the hours-scale of chromatin→transcription coupling), power (n = 14), drug class
(IDH1-metabolic, not a chromatin writer), and — decisively — a **relapse regime change at 4 wk** that
breaks the monotonic-onset assumption a t½ fit requires.

**Decision:**
- **Headline timing claim → wet-lab.** Minimal same-system experiment (removes both the cell-context
  confound and the scoop): CD34+ HSPC or MOLM-13 — (i) 1× untreated 10x Multiome baseline; (ii) HMA
  (decitabine) *or* HDACi (panobinostat/SAHA) *or* BETi (JQ1) scRNA-seq (multiome ideal) at
  **0 / 2 / 6 / 12 / 24 / 48 h**. This is the only path that yields a genuine per-gene onset curve in
  a system where baseline chromatin-lag is measured in the *same* cells.
- **Public-data role = supporting, not validating.**
  - **GSE229314 t½ (6,580 genes)** → the *mandatory decay control* feature (§3) and the SOTA baseline
    bar (their AUC 0.86–0.94) our full model must beat incrementally.
  - **GSE201662** → optional **feasibility demonstrator**: prove the join + nested-model + ortholog
    machinery runs end-to-end against a *coarse ordinal / monotonic-trend* outcome (§3), never a t½.
    Frame in-paper as a plumbing/robustness check, not evidence for H_main.

---

## 3. Locked analysis design (applies to whichever outcome is chosen)

### 3.1 Mandatory-control nested model (non-negotiable — this is what defends against the scoop)

Fit two nested models per outcome and report the **increment**:

```
base:  response_timing ~ decay_t½                     (Todorovski's required control)
full:  response_timing ~ decay_t½ + chromatin_lag     (+ ATAC promoter/enhancer, burst as covariates)
report: ΔR²(full−base), ΔAUC, likelihood-ratio test p, on chromosome/lineage-blocked hold-outs
```

Rationale (R4): Todorovski 2024 showed baseline **mRNA decay** drives drug down-regulation
selectivity. If we report chromatin-lag's predictive power **without** decay in the model, the claim
collapses to "decay re-measured via chromatin" = scoop **high**. The contribution only exists as
**ΔR²/ΔAUC of chromatin-lag *over and above* decay**. Report decay-only performance explicitly next
to the full model so the increment is legible.

### 3.2 Per-gene timing target extraction (from the outcome timecourse)

- **Preferred (wet-lab hours-grid, ≥4–6 points):** per-gene response curve `y(t)` (log2 fold-change
  vs 0 h, or absolute normalized level) fit with a **monotonic sigmoid** `y(t)=y∞ + (y0−y∞)/(1+e^((t−t½)/τ))`
  or **single-exponential** `y(t)=y∞+(y0−y∞)e^(−k t)`. Targets = **t½ (half-response time)** and/or
  **onset** (first t crossing a fraction of y∞) and/or **rate k**. Choose target after seeing the
  time grid (open decision in PAPER-PLAN §9). Require a fit-quality gate (R² of the per-gene fit) and
  drop genes with a flat / non-monotonic / non-significant response — timing is undefined for
  non-responders.
- **GSE201662 feasibility mode (coarse, 3 points, 4 wk = relapse):** a 2-parameter sigmoid/exponential
  is **not identifiable** from 3 coarse points where one is a regime change — **do not fit t½.**
  Restrict to an **ordinal "early vs late responder"** label from the {5 d, 14 d} on-treatment arms
  only (exclude the 4 wk relapse arm from the timing target), and report **AUC of ordinal
  classification**, framed strictly as a plumbing check. State this limitation inline.

### 3.3 Joining baseline HSPC features to the drug system (gene-intrinsic restriction — R2)

- Join key = **gene** (symbol/Ensembl; **mouse→human ortholog** for GSE201662, one-to-one high-confidence
  orthologs only, flagged as a limitation).
- **Only gene-intrinsic baseline features cross systems**: chromatin→transcription **lag** (Part 1),
  **burst kinetics**, spliced/unspliced ratio, decay t½. **Do not** transfer cell-type-specific
  absolute accessibility *values* across systems; where ATAC promoter/enhancer accessibility is used,
  treat it as a HSPC-baseline covariate whose transfer validity is itself a stated assumption, not a
  fact. This is the R2 mitigation: predict from properties plausibly gene-intrinsic, not from the
  donor cell state.

### 3.4 Confounds to state honestly (cross-cell-line / cross-species pairing)

1. **Cell-context mismatch (max confound):** baseline = normal-ish human HSPC (GSE209878); outcome =
   leukemia line (or mouse AML). Gene-intrinsic restriction mitigates but does **not remove** it.
2. **Triple-system stacking:** if outcome = GSE201662 (mouse), decay = GSE229314 (human K562/THP-1),
   baseline lag = human HSPC → **three** systems stitched by gene, not the two-system pairing
   PAPER-PLAN anticipated. Each additional system compounds the context confound. Prefer collapsing to
   two systems (wet-lab: baseline + outcome in *one* system; decay measured or DB-sourced in that same
   system) wherever possible.
3. **Feature-intersection power:** the ΔR² test only has power on genes present in **all** joined
   layers — Todorovski's 6,580 t½ genes ∩ HSPC-lag genes ∩ (ortholog-mapped) outcome-responder genes.
   Report the expected intersection size up front as a feasibility caveat; a small intersection can
   make the incremental test underpowered regardless of effect size.
4. **Drug-class heterogeneity:** IDH1i (GSE201662) acts through metabolic → demethylation, a different
   mechanism from HMA/HDACi/BETi. Cross-drug generalization is a separate claim; do not pool.
5. **Pseudotime ≠ wall-clock** (CLAUDE.md #1): Part 1 lag is in pseudotime units; the outcome timing is
   in wall-clock hours/days. The model relates a pseudotime-scaled *feature* to a wall-clock *outcome* —
   legitimate as prediction, but state that lag is not itself a wall-clock rate.
6. **Multiple testing / leakage** (CLAUDE.md #4, PAPER-PLAN §5): chromosome/lineage-blocked hold-outs,
   permutation null for the ΔR²/ΔAUC significance.

---

## 4. Scoop boundary vs Todorovski 2024 (design must defend all four axes)

Todorovski et al. 2024, *NAR Cancer* 6(4):zcae039 (PMID 39372038; PMC11447529; GSE229314) is the
nearest prior work. Our differentiator = **four simultaneously non-overlapping axes**:

| Axis | Todorovski 2024 | This project | Non-overlap |
|---|---|---|---|
| Baseline feature | mRNA **decay rate / t½** (RNA-side, downstream) | **chromatin→transcription lag** (chromatin-side, upstream) | ✔ opposite ends of the production→decay axis |
| Measurement dimension | **bulk** SLAM/TT/MAC-seq | **single-cell / 10x multiome** (RNA+ATAC same cell) | ✔ |
| Outcome | down-regulation **magnitude / inhibitor class** (2 h/6 h discrete) | response **timing** (t½ / onset) | ✔ they never model a time axis |
| System | leukemia **cell line** (K562/THP-1) | human **HSPC** (primary) baseline | ✔ |

Only the *frame* ("baseline kinetic feature → transcriptional-drug response") overlaps. Todorovski
explicitly **excludes chromatin** ("whether a gene will or will not respond is … independent of the
chromatin state") and does **not** measure accessibility — so the residual variance we target is
white space *they name in their own paper*. **The scoop stays "medium, conditionally downgradable"
only if §3.1's decay-controlled incremental design is executed.** Reporting chromatin-lag alone,
uncontrolled for decay, or an outcome of magnitude-not-timing → scoop escalates to **high**. Must-cite
and contrast their Fig 2 (decay→response AUC 0.86–0.94 = the bar), Fig 1 (SE down but selectivity
unexplained = the white space), Fig 3 (73-compound generalization).

---

## Sources (verified 2026-07-06)

- GSE201662 — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE201662 (mouse IDH1m AML, AG-120, 5 d/14 d/4 wk-relapse, bulk RNA, 14 samples, open)
- GSE256354 — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE256354 (human AML, DAC/AZA, single-cell 72 h, open); paper: Bond et al., *Leukemia* 2025 — https://www.nature.com/articles/s41375-025-02693-5 ; PMC12380606 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12380606/ (Methods: "after 72 h (day 3), cells collected for single-cell analyses")
- GSE229314 — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE229314 (Todorovski 2024, human K562/THP-1, bulk SLAM/TT/MAC-seq, open); PMID 39372038 / PMC11447529
- GSE190785 — https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE190785 (human MOLM13+primary AML, quizartinib+LSD1i GSK2879552; bulk RNA single 24 h; 2/6/24 h only in CUT&Tag; open)
- GSE120715 (I-BET sensitivity reference); GSE141834 (T47D dexamethasone, non-heme, adjacent) — via GEO/web re-search 2026-07-06
- Prior internal: `PAPER-PLAN.md`; `paper_analysis/epigenomic-lag/_evidence/lit-search/epigenetic-drug-timecourse.md`; `paper_analysis/epigenomic-lag/todorovski-2024-rna-kinetics/todorovski-2024_scoop-analysis.md`
