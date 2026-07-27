> ⚠️ **역사 문서.** 여기서 견주는 `draft.md`는 v1이며 폐기됐다. **정본은 `draft_v2.md`·`draft_v2_ko.md`**다.

# GB_BENCHMARK.md — Genome Biology format/structure benchmark for our velocity-lag audit paper

> **Purpose.** A *format/structure* benchmark (not a content review) to target our manuscript
> (`draft.md`) to the Genome Biology (GB) benchmark/audit genre. Built by fetching real, recently
> published GB papers, extracting their structural template, and synthesizing a consensus skeleton +
> gap analysis against our current draft.
> Prepared 2026-07-18 for the manuscript-writer / paper-critic loop. **Preparation only — no edits to draft.md.**
>
> **Sourcing honesty (read before using quotes):** article structure below was extracted with WebFetch,
> which *summarizes* pages. Section-order / figure-count / declaration facts were cross-checked against the
> PMC full text and are reliable. **The verbatim quotes in the framing crib sheet (§5) were returned by a
> summarizing fetch and MUST be re-verified character-for-character against the source PDF before being
> pasted into the manuscript** (one Abdelaal recommendation quote came back truncated; flagged inline).
> GB article pages (`genomebiology.biomedcentral.com`, `link.springer.com`) auth-wall WebFetch — the
> fetchable mirror is **PMC** (`pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx`).

---

## 1. Exemplar table

Genre-match tiers (from the task): **1** = RNA-velocity / multiome benchmark or robustness-audit in GB;
**2** = single-cell method benchmark/comparison/evaluation in GB; **3** = cautionary / guidelines /
meta / negative-result computational-genomics paper in GB.

**Genre-1 finding up front:** *there is no pure RNA-velocity (or multiome-velocity) benchmark/robustness-audit
paper in Genome Biology.* GB's velocity content is **method papers** (CRAK-Velo 2026, DeepKINET 2024) — the exact
family we audit, but method-genre, not benchmark-genre. The velocity *benchmarks* live in Cell Reports Methods /
PLoS Comp Biol / bioRxiv (refs [12],[13] in our draft), not GB. **This is a real coverage gap, and it is also our
opening: our paper would be the first velocity-focused robustness audit in GB.** The structural spine below is
therefore anchored on GB *benchmark-of-X-methods* papers (tier 2), which share our exact question-first / axis-organized
skeleton; the GB velocity method papers are used only as **convention references** (declarations, data-availability,
velocity-citation style), NOT as structural models.

| # | Title (abbrev.) | DOI / URL | Year | Tier | Why it is a good structural model |
|---|---|---|---|---|---|
| E1 | A comparison of automatic cell identification methods for single-cell RNA sequencing data (Abdelaal et al.) | 10.1186/s13059-019-1795-z · [PMC6734286](https://pmc.ncbi.nlm.nih.gov/articles/PMC6734286/) | 2019 | **2** | Canonical GB "benchmark of X methods": structured abstract → Background → task-organized Results → recommendation → Methods-after. Decision guidance = **summary heatmap figure (Fig 8) + prose**, plus inventory **Table 1 (methods) / Table 2 (datasets)**. Closest structural twin to us. |
| E2 | A systematic evaluation of single-cell RNA-sequencing imputation methods (Hou et al.) | 10.1186/s13059-020-02132-x · [PMC7450705](https://pmc.ncbi.nlm.nih.gov/articles/PMC7450705/) | 2020 | **2** | Same skeleton; Results organized by **downstream-analysis axis** (DE / clustering / trajectory) — direct analog to our per-axis Results (concordance / causal / predictability / identifiability). States variability finding confidently. |
| E3 | Benchmarking multi-slice integration and downstream applications in spatial transcriptomics data analysis | 10.1186/s13059-025-03796-z · [PMC12477787](https://pmc.ncbi.nlm.nih.gov/articles/PMC12477787/) | 2025 | **2** | *Recent* genre-matched GB benchmark; structured ~300-word abstract, task-organized Results, explicit "no single method performs optimally" + technology-specific recommendation prose. Proves the template is current, not dated. |
| E4 | Meta-analysis of (single-cell method) benchmarks reveals the need for extensibility and interoperability | 10.1186/s13059-023-02962-5 · [PMC10189979](https://pmc.ncbi.nlm.nih.gov/articles/PMC10189979/) | 2023 | **3** | Benchmark-*of*-benchmarks; gives GB's conventions on **neutrality / scrutinizing method-paper claims** (directly supports our audit framing) and the declarations/reproducibility norms. |
| E5 | Essential guidelines for computational method benchmarking (Weber et al.) | 10.1186/s13059-019-1738-8 · [PMC6584985](https://pmc.ncbi.nlm.nih.gov/articles/PMC6584985/) | 2019 | **3** | GB's own rulebook for benchmark papers → **gold source for the framing crib sheet** ("no single winner", "report a set", "transparently discuss limitations"). NOTE: a *Review* (Introduction-not-Background skeleton) — use for language/conventions, NOT as structural model. |
| E6 | DeepKINET: a deep generative model for estimating single-cell RNA splicing and degradation rates (Mizukoshi et al.) | 10.1186/s13059-024-03367-8 · [PMC11378460](https://pmc.ncbi.nlm.nih.gov/articles/PMC11378460/) | 2024 | **1 (topical) / method-genre** | GB velocity-kinetics **method** paper covering the *exact* α/β/γ splicing–degradation rates we anchor. **Convention reference only**: GB declarations block, data-availability (GEO + Zenodo + MIT), how velocity/scVelo/MultiVelo lit is cited. |
| E7 | CRAK-Velo: chromatin accessibility kinetics integration improves RNA velocity estimation (El Kazwini et al.) | 10.1186/s13059-026-04086-y · PMID 42087173 (no PMC yet) | 2026 | **1 (topical) / method-genre** | The GB multiome-velocity method we benchmark (our ref [4]). **Full text not fetchable** (2026, auth-walled everywhere, no PMC mirror). Abstract confirmed: narrative, GB. Convention reference only. |

---

## 2. Per-exemplar structural extract

### E1 — Abdelaal 2019 (tier 2, primary structural twin)
- **Section order:** Background → Results → Discussion → Conclusions → Methods. (Background, not Introduction.)
- **Results subsections (verbatim, declarative-sentence style):** "Benchmarking automatic cell identification methods (intra-dataset evaluation)"; "All classifiers perform well in intra-dataset experiments"; "Performance evaluation across different annotation levels"; "Incorporating prior-knowledge does not improve intra-dataset performance on PBMC data"; "The performance of prior-knowledge classifiers strongly depends on the selected marker genes"; "Classification performance depends on dataset complexity"; "Performance evaluation across datasets (inter-dataset evaluation)"; "Rejection option evaluation"; "Performance sensitivity to the input features"; "Scalability…"; "Running time evaluation".
- **Abstract:** structured **Background / Results / Conclusions**, ~280 words.
- **Main figures = 8** (Fig 1–8; Fig 8 = "Summary of the performance of all classifiers…" — the decision-guidance **heatmap**). **Main tables = 2**: Table 1 = methods inventory, Table 2 = datasets inventory. Performance summary is a *figure*, not a table.
- **Methods:** after Conclusions; ~13 named subsections (Classification methods, Datasets, Data preprocessing, Intra-/Inter-dataset classification, Performance evaluation metrics, Feature selection, Scalability, Rejection, Benchmarking pipeline).
- **Recommendation framing:** picks a best default *with* named strong alternatives (SVM_rejection best; SVM / singleCellNet / scmapcell / scPred as alternatives) — no universal winner. (Verbatim recommendation sentence came back **truncated** — "We recommend the use of the general-purpose SVM_rejection classifier (with a linear kernel) since it has a better performance compared to…" — reverify before quoting.)
- **Declarations:** *Availability of data and materials* — "The filtered datasets… can be downloaded from Zenodo (10.5281/zenodo.3357167). The source code is available in the GitHub repository, at https://github.com/tabdelaal/scRNAseq_Benchmark [52], and in the Zenodo repository, at 10.5281/zenodo.3369158 [53]." *Competing interests* — "The authors declare that they have no competing interests."
- **References ≈ 53.**

### E2 — Hou 2020 (tier 2, downstream-axis Results twin)
- **Section order:** Background → Results → Discussion → Conclusions → Methods.
- **Results subsections (verbatim):** "Similarity between bulk RNA-seq and imputed scRNA-seq data"; "Impact of scRNA-seq imputation on identifying differentially expressed genes"; "Impact of scRNA-seq imputation on unsupervised clustering"; "Impact of scRNA-seq imputation on inferring pseudotemporal trajectories". → **Results organized by downstream-analysis axis**, each a self-contained "does the method survive this test?" unit — the exact shape of our R1–R7 axes.
- **Abstract:** structured **Background / Results / Conclusions**, ~200 words.
- **Main figures = 6.** Main tables mostly pushed to supplementary (Additional files 2–6).
- **Methods:** after Conclusions.
- **Recommendation framing (verbatim):** "However, the performance of methods varied across evaluation criteria, experimental protocols, datasets, and downstream analyses." — a confident *variability* statement (no single method best).
- **Declarations:** standard GB block (Availability/Competing not returned verbatim by fetch; CC-BY 4.0). **References ≈ 83.**

### E3 — Spatial multi-slice benchmark 2025 (tier 2, recent template check)
- **Section order:** Background → Results → Discussion → Conclusions → Methods. (Identical to E1/E2.)
- **Results subsections (verbatim):** "Overview of the overall framework"; "Benchmarking multi-slice integration"; "Benchmarking spatial clustering"; "Benchmarking spatial alignment"; "Benchmarking slice representation"; "Overall performance analysis of each method across all datasets" (final overall-summary subsection — analog to our synthesis/decision-map).
- **Abstract:** structured **Background / Results / Conclusions**, ~300 words.
- **Main figures = 6.** Main tables: 1 (a supplementary Table S1). Overall performance = summary figure.
- **Methods:** after Conclusions (datasets, benchmarking methods, metrics, alignment, representation).
- **Recommendation framing (verbatim):** "Our benchmarking results indicate that no single method performs optimally across all scenarios and data types." + technology-specific prose guidance (CellCharter / Banksy / PASTE-SPACEL per task).
- **Declarations:** *Data availability* — "All of these datasets are uploaded to Zenodo (https://doi.org/10.5281/zenodo.14906156)." *Competing interests* — "The authors declare no competing interests." **References ≈ 52.**

### E4 — Meta-analysis of benchmarks 2023 (tier 3, neutrality/audit conventions)
- **Section order:** Background → State-of-the-art in benchmarking → Overall design of benchmarks → Code/data availability, reproducibility, and technical aspects → Conclusions → The future of benchmarking → Methods. (Essay-style GB benchmark; still Background-first, Methods-last.)
- **Abstract:** narrative-ish (Background/Results/Conclusions implied), ~250 words.
- **Main figures = 2; main tables = 1** ("List of guidelines discussed… and their benefit for the community" — a *guidelines table*, an analog format to our Table 2 decision map).
- **Audit-framing (verbatim):** "Ultimately, it is almost a foregone conclusion that a newly proposed method will report comparatively strong performance. Thus, claims from individual method development papers need to be scrutinized, preferably from a neutral (i.e. independent) standpoint." → **direct license for our neutral-audit framing** (we scrutinize MultiVelo/MoFlow's lag claims).
- **Declarations:** code on GitHub + Zenodo snapshot DOI; "The authors declare no competing interests." **References ≈ 32.**

### E5 — Weber 2019 Essential guidelines (tier 3, framing crib source)
- **Section order (Review genre — Introduction, not Background):** Introduction → Defining the purpose and scope → Selection of methods → Selection (or design) of datasets → Parameters and software versions → Evaluation criteria: key quantitative performance metrics → Evaluation criteria: secondary measures → Interpretation, guidelines, and recommendations → Publication and reporting of results → Enabling future extensions → Reproducible research best practices → Discussion.
- **Use:** language/conventions only (do NOT copy this skeleton — it's a review, not an IMRaD benchmark). See §5 for verbatim crib quotes.

### E6 — DeepKINET 2024 (tier 1 topical / method-genre; convention reference)
- **Section order:** Background → Results (subsections: "Conceptual view of DeepKINET"; "Simulated data to demonstrate accuracy…"; "Accuracy… evaluated using metabolic labeling data"; "…investigate functions of RNA-binding proteins"; "…reveals heterogeneity in cancer cell populations"; "…changes in splicing due to mutations…") → Discussion → Methods → Declarations. (**Method-genre tell:** Results lead with "conceptual view of our method" and are organized as "our method does X" — NOT what we want; contrast with E1–E3 axis-organized Results.)
- **Abstract:** **narrative/unstructured**, ~165 words. (Method papers in GB often use narrative abstracts; benchmarks use structured — pick structured, per E1–E3.)
- **Main figures = 6; main tables = 0; supplementary = 5 figs (Additional file 1).** **Methods after Discussion.**
- **Declarations (verbatim, the GB convention we should mirror):** Ethics ("Not applicable."); Consent for publication ("All authors have reviewed and consented…"); Competing interests ("The authors declare no competing interests."); *Availability of data and materials* — "Code and modified SERGIO available at https://github.com/3254c/DeepKINET and Zenodo (10.5281/zenodo.13054695, MIT license). Datasets: pancreas (GSE132188), cell cycle (GSE128365), forebrain (SRP129388), breast cancer (GSE167036)." Funding (grant IDs); Authors' contributions (initials + role). **References ≈ 57.**
- **Velocity-citation style:** cites velocyto/scVelo/veloVI/cellDancer/DeepVelo/MultiVelo by number; explicitly names scVelo's "uniform kinetic rates across cells" limitation as motivation — same rhetorical move we use.

### E7 — CRAK-Velo 2026 (tier 1 topical / method-genre; abstract only)
- **Only the abstract is retrievable** (2026; no PMC mirror; Springer/BMC auth-wall). Narrative abstract, confirmed Genome Biology 27(1), DOI 10.1186/s13059-026-04086-y, authors El Kazwini, Gao, Kouadri Boudjelthia, Cai, Huang, Sanguinetti. **Structural template not extractable — coverage gap (see report).**

---

## 3. Synthesized Genome Biology format template for OUR paper

Consensus is unambiguous across the three genre-matched benchmarks (E1/E2/E3), and it **empirically confirms the
spec already asserted in WRITING_PLAN §0** (Background-not-Introduction, structured abstract, Methods-after).

**Section skeleton (adopt exactly):**
```
Title  (declarative + genre signal — see §5)
Abstract  (STRUCTURED: Background / Results / Conclusions)
Background
Results
  <declarative-sentence subsection headings, one per evaluation axis, NO "R1./R2." numbering>
  … final subsection = the synthesis / confidence-map ("Overall …" per E3)
Discussion
Conclusions
Methods            (after Conclusions; many named subsections)
Declarations       (Ethics / Consent / Competing interests / Availability of data and materials / Funding / Authors' contributions / Acknowledgements)
References
```

**Abstract style & budget:** structured Background/Results/Conclusions, **~250–320 words total** (E1 280, E2 200, E3 300).
Our current abstract is ~490 words → **must be cut ~35%** (see §4).

**Figure/table budget (genre norm):**
- **Main figures: 6–8.** (E1 8, E2 6, E3 6, E6 6.) Our 5 main figures is *slightly under* norm — fine, and there is headroom to promote one supplementary panel (e.g. the causal ATAC-shuffle, R2) to a main figure.
- **Main tables: 1–2**, and the genre uses them as **inventories** (E1 Table 1 = methods, Table 2 = datasets). The **performance/decision summary is usually a FIGURE (heatmap, E1 Fig 8 / E3 overall-summary)**, occasionally a guidelines *table* (E4 Table 1).
- **Supplementary:** liberal (Additional files); benchmarks routinely push secondary tables + confound analyses there.

**Methods positioning:** after Conclusions, ~10–13 named subsections (E1 has 13). Ours already matches.

**Declarations block (adopt verbatim skeleton, GB-standard across E1/E3/E6):**
```
Ethics approval and consent to participate
Consent for publication
Competing interests
Availability of data and materials   ← list EVERY accession + code repo (GitHub) + archival Zenodo DOI + license
Funding
Authors' contributions               ← initials + CRediT-style roles
Acknowledgements
```

**References:** GB benchmarks cite **~50–85** (E1 53, E2 83, E3 52, E6 57; only the short meta-essay E4 is 32).
Target **≥50** (our draft's 19 is far below genre norm — §4).

**Genre framing (how GB benchmarks avoid "failure-story" tone):** they (a) title neutrally around the *task*, not the
loser; (b) state the negative confidently as *variability / no-single-winner* ("no single method performs optimally…",
E3); (c) always pair the negative with **actionable guidance** (a recommended set + per-context advice); (d) invoke
**neutrality** as a virtue (E4: method-paper claims "need to be scrutinized… from a neutral standpoint"). Our asymmetric
result (**lag fails, α holds**) is *stronger* than "no clear winner" — we can borrow the confident register and add a
clean dissociation, which reads as a *finding*, not a *failure*.

---

## 4. Gap analysis — our `draft.md` vs the exemplars (actionable checklist)

Our draft is already close (Background-first, structured abstract, Methods-after, full declarations). The gaps are
budget/format/citation, not skeleton. Ordered by impact:

- [ ] **G1 — Trim the abstract (~490 → ≤320 words).** Real GB benchmark abstracts are 200–300 words; our Results
      paragraph alone (~250) exceeds a whole GB abstract. Keep the 4–5 headline numbers (lag |ρ|≤0.08 / sign 48% /
      α ρ=0.88 / 6-of-6 preregistered / TT-seq anchor); move the curvature-ratio, diff-budget, per-method CI detail
      to Results. Keep the structured Background/Results/Conclusions labels.
- [ ] **G2 — Drop the "R1.–R7." numeric prefixes on Results subsections.** GB benchmarks (E1/E2/E3) use *unnumbered
      declarative-sentence* headings ("Chromatin does not drive the lag: a causal negative control" is already perfect;
      just delete "R2."). Keep the sentence content; remove the R#.
- [ ] **G3 — Expand references to ≥50.** Draft has 19; genre norm is 50–85. Fully cite every dataset (6 systems),
      every velocity method + RNA-only floor, the velocity-critique corpus, identifiability precedents, and the two
      TT-seq/half-life sources. This is the single most visible "not a GB benchmark yet" tell.
- [ ] **G4 — Add two GB-standard inventory tables** (E1 convention): a **methods table** (5 velocity arms: model
      family, chromatin channel Y/N, lag definition, sign convention) and a **datasets table** (6 systems: accession,
      species/tissue, #cells, platform, role). These currently live only as Methods prose + are conflated into Table 1.
      GB reviewers expect the inventory tables to be separate and up front.
- [ ] **G5 — Decision guidance: keep Table 2, but add a summary FIGURE.** The genre-dominant form of decision guidance
      is a **summary heatmap** (E1 Fig 8; E3 "overall performance" figure), not only a table. Table 2 (confidence
      decision map) is defensible and on-genre (E4 uses a guidelines table), but add a compact "velocity-output ×
      axis (reproducible / causal / predictable / anchored)" heatmap as a main figure so the guidance reads visually
      like a GB benchmark. (Also satisfies G-fig headroom in §3.)
- [ ] **G6 — Promote the causal negative control (R2) to a main figure.** It is our most distinctive contribution vs
      prior velocity benchmarks (E4's neutrality point), currently only "(supp fig possible)". A main figure here lands
      the audit's novelty and uses available figure budget (5→6, within norm).
- [ ] **G7 — Complete `Availability of data and materials` to GB spec** (E6/E1 pattern): resolve the two `<FILL:
      accession>` brain datasets, and replace `<FILL: repository/DOI>` with GitHub URL + archival **Zenodo DOI +
      license**. Every accession must be listed inline. This is a hard GB requirement, not cosmetic.
- [ ] **G8 — Final Results subsection = explicit synthesis** (E3 "Overall performance…"). Our confidence-map narrative
      currently sits in Discussion + Table 2; add a short closing Results subsection that states the synthesis *as a
      result* (which outputs are real vs shadows), so the decision map is earned in Results, mirroring the genre.
- [ ] **G9 — Title: keep but sharpen the neutral/task framing.** Current title ("Which velocity outputs are real and
      which are shadows of the model? A cross-method robustness audit…") is already on-genre (question + "robustness
      audit"). Optional: ensure the subtitle carries the *actionable* half (confidence map) so it doesn't read as pure
      negative. No change strictly required.
- [ ] **G10 — Declarations skeleton is complete** (Ethics/Consent/Competing/Availability/Funding/Contributions/
      Acknowledgements all present). No structural gap — only the `<FILL>` content (G7 + author fields).

**Already conformant (no action):** Background-not-Introduction ✔; structured abstract labels ✔; Methods after
Conclusions with named subsections ✔; declarations block present ✔; declarative-sentence subsection headings ✔;
keeping Table 1 (reproducibility) and Table 2 (decision map) un-fused ✔ (matches E4's separate guidelines table).

---

## 5. Framing crib sheet — stating a negative/cautionary result confidently (GB register)

Real GB-benchmark sentence patterns for our headline "**the chromatin→transcription lag is not robustly reproducible**".
**Reverify each quote against the source PDF before pasting** (WebFetch summarizes; wording may be lightly off).

1. **No-single-winner, stated flatly (E3, spatial 2025, DOI 10.1186/s13059-025-03796-z):**
   > "Our benchmarking results indicate that no single method performs optimally across all scenarios and data types."
   *Our analog:* "Across five methods and six datasets, no method's per-gene lag reproduces another's — while the
   transcription rate α reproduces across all of them."

2. **Confident variability, no hedging (E2, Hou 2020, DOI 10.1186/s13059-020-02132-x):**
   > "However, the performance of methods varied across evaluation criteria, experimental protocols, datasets, and
   > downstream analyses."
   *Our analog:* "The lag varied across methods, datasets, and evaluation axes; α did not — a dissociation, not a tie."

3. **Neutral-audit license — scrutinize method-paper claims (E4, meta-analysis 2023, DOI 10.1186/s13059-023-02962-5):**
   > "Ultimately, it is almost a foregone conclusion that a newly proposed method will report comparatively strong
   > performance. Thus, claims from individual method development papers need to be scrutinized, preferably from a
   > neutral (i.e. independent) standpoint."
   *Our analog:* frames why we re-test MoFlow's "consistent-subset" lag agreement and MultiVelo's 100%-chromatin-leads
   from a neutral standpoint rather than accepting the originating papers' favorable reports.

4. **Report a robust SET, not a single value + give guidance (E5, Weber 2019, DOI 10.1186/s13059-019-1738-8):**
   > "it is unlikely that a single method will perform best across all metrics"
   > "a good strategy is to use rankings from multiple metrics to identify a set of consistently high-performing
   > methods, and then highlight the different strengths of these methods"
   *Our analog:* the confidence decision map (Table 2) — trust the robust SET (α, rate-derived, population balance),
   flag the fragile outputs (lag, sign, absolute timing).

5. **Limitations as a virtue, not a confession (E5, Weber 2019):**
   > "Limitations of the benchmark should be transparently discussed."
   > "Without a thorough discussion of limitations, a benchmark runs the risk of misleading readers; in extreme cases,
   > this may even harm the broader research field."
   *Our analog:* our load-bearing caveats (single-method-pair leg outside HSPC; single-sample replications;
   relative/practical—not flat—non-identifiability; pseudotime≠wall-clock) are stated up front as scope, GB-style.

**Register note:** every GB benchmark pairs the negative with *actionable guidance* in the same breath (recommended set
+ per-context advice). Our paper is one step stronger than "no clear winner": it is an **asymmetric dissociation**
(one derived quantity is robust and externally anchored, another is a model artifact). Lead with that asymmetry — it
reads as a positive finding about α plus a boundary on lag, not as a failure story.

---

## Appendix — coverage gaps / could-not-fetch
- **CRAK-Velo (E7, GB 2026):** full text un-fetchable (no PMC mirror yet; Springer/BMC auth-wall; abstract only). Its
  internal structure is not in this benchmark. Low impact — it is a method paper used as a convention reference, and
  DeepKINET (E6) covers the GB velocity-method conventions with full text.
- **No genre-1 exemplar exists** (velocity/multiome benchmark in GB). Substituted: tier-2 GB single-cell benchmarks
  (E1–E3) for the structural spine + tier-1 GB velocity *method* papers (E6/E7) for conventions. Reported as a finding.
- **Verbatim quotes (§5):** returned by summarizing fetch; flagged for character-level reverification before manuscript use.
- **Some declarations** (Hou E2 Availability/Competing) not returned verbatim by the fetch; the GB-standard block
  (shown fully via E1/E6) applies.
