# DATA-HUNT — targeted data + literature hunt to harden the velocity-lag paper

> Literature-scout deliverable. Three **targeted** hunts (not a landscape redo — see
> `related_work.md` for the standing landscape/scoop and `drug_timing_arm_scout.md` for the prior
> drug-data gate). Date accessed **2026-07-07**. Each hit carries an accession/DOI/URL, an honest
> **fit verdict**, and **what it enables**. Bibliographic detail verified against GEO `acc.cgi` /
> source pages this session; items I could not fully fetch are flagged inline.
>
> Story being hardened: chromatin→transcription **lag** is method-fragile; transcription rate **α**
> is method-robust (cross-method ρ=0.88) and predictable from day0 ATAC baseline (held-out lineage
> ρ=+0.31); replicated across 4 multiome datasets (`FINDINGS.md` §7). Original goal = predict
> epigenetic-drug response **timing** from the baseline epigenome; no wet-lab timecourse yet.

---

## HUNT 1 — External orthogonal validation of α robustness

**Question answered:** does our *fitted* transcription rate α correlate with an *experimentally
measured* RNA synthesis/production rate? This adds an **accuracy** leg to the existing
cross-*method* reproducibility leg (α ρ=0.88). The biophysical analog is exact:
scVelo/MultiVelo **α ≡ TT-seq production rate ≡ SLAM-seq synthesis rate**.

**How to run it (pre-register, so a null can't be mis-read):** per-gene **Spearman** of
HSPC-fitted α (restricted to your existing fit-quality-gated genes) vs the measured synthesis rate,
joined by gene symbol. Interpretation is **asymmetric**: a positive ρ supports "α captures a
gene-intrinsic synthesis-rate ordering that generalizes across context"; a **null does NOT mean α
is inaccurate** — it is confounded by cell-context mismatch (dynamic HSPC vs near-steady-state
leukemia line) and by the fact that **absolute α is not identifiable** (see Hunt 3 / BayVel), so the
test is deliberately rank-based, never absolute-value.

Why cross-context rather than same-cell: the ideal is to fit α in the *same* cells where synthesis
is measured, but K562/THP-1 are stable proliferating lines sitting near steady state → the dynamical
α is poorly identified there. Fitting α in the dynamic HSPC and validating against the measured
leukemia rate is the pragmatic, defensible choice — reinforce it, don't apologize for it.

### 1A. GSE229314 — Todorovski et al. 2024 (SLAM-seq + TT-seq, K562/THP-1) — **BEST HIT**
- **ID / refs:** GEO **GSE229314**; Todorovski et al., *NAR Cancer* 6(4):zcae039 (2024), PMID
  39372038, PMC11447529. Associated preprint: *"RNA decay defines the response to transcriptional
  perturbation in leukaemia,"* bioRxiv 2022.04.06.487057.
  https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE229314
- **What it measures (verified this session on `acc.cgi`):** SLAM-seq, **TT-seq**, MAC-seq, total
  RNA-seq, 3′ mRNA-seq in **K562 and THP-1**. The TT-seq arm ships samples explicitly labelled
  **"production rates"** → genome-wide **per-gene synthesis rate** is extractable (not merely
  decay/half-life). Untreated `no4sU_control` / `UT` samples give the **baseline** rate we need.
- **Fit verdict: STRONG — the elegant call, and dual-use.** GSE229314 is *already in the paper* as
  the mandatory mRNA-decay control (`drug_timing_arm_scout.md` §3.1). The same dataset yields both
  the decay t½ (control feature) **and** the TT-seq production rate (α ground truth) — one join,
  two roles, no new provenance. Crucially, **K562 ≈ erythroid/megakaryocytic and THP-1 ≈ monocytic
  leukemias** — they map onto HSPC output lineages, so "leukemia line ≠ HSPC" (the framing in the
  prior scout) understates the fit: these are hematopoietic-lineage cells, a materially better match
  than a generic line.
- **What it enables:** the first *accuracy* check on α — "our method-robust α tracks a directly
  measured hematopoietic synthesis rate" — turning the α story from "reproducible across methods"
  into "reproducible **and** anchored to experiment." Also lets you show the dissociation cleanly:
  α validates against synthesis rate; the fragile lag has no such external anchor.

### 1B. GSE75792 — Schwalb et al. 2016 (TT-seq, K562) — independent 2nd synthesis source
- **ID / refs:** GEO **GSE75792**; Schwalb, Michel, Zacher, … Gagneur, Cramer, *"TT-seq maps the
  human transient transcriptome,"* *Science* 352(6290):1225–1228 (2016),
  doi:10.1126/science.aad9841. https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE75792
- **What it measures:** TT-seq + 4sU-seq + total-RNA-seq in **K562**; the paper reports genome-wide
  **synthesis and degradation rates**. ⚠️ GEO supplementaries are **binned count / exon-intron
  transcript-count tables**, not a ready-made per-gene rate table — per-gene synthesis rates must be
  **recomputed** (or pulled from the paper's Table S / the Gagneur-lab pipeline) before use. Verify
  the rate table is reconstructible before listing as "extractable."
- **Fit verdict: GOOD (independent replication of 1A).** Same cell line (K562) but a *different lab,
  different year, different pipeline* → a **two-source concordance** of α-vs-synthesis is far
  stronger than a single source. Use it to show the α validation is not an artifact of Todorovski's
  particular quantification.
- **What it enables:** a robustness-of-the-validation check — if HSPC-α correlates with **both**
  Todorovski and Schwalb K562 synthesis rates, the accuracy claim is doubly grounded.

### 1C. ENCODE K562 RNA Pol II (POLR2A) ChIP-seq — tertiary occupancy proxy (completeness)
- **ID / refs:** ENCODE K562 **POLR2A** ChIP-seq (e.g. ENCSR000EHL and related), portal
  https://www.encodeproject.org (search "K562 POLR2A ChIP-seq"). Related: Gressel et al., *"The
  pause-initiation limit restricts transcription activation,"* *eLife* 2019 (PMC6689055) — K562
  productive-initiation frequencies.
- **Fit verdict: WEAK / tertiary.** Pol II *occupancy* ≠ synthesis rate — promoter-proximal
  **pausing** decouples occupancy from productive output, so this is a noisier proxy than TT-seq /
  SLAM. Include only to complete the modality sweep (metabolic-label → nascent → Pol II) the task
  named; do not headline.
- **What it enables:** a one-line "consistent with occupancy too" supporting sentence at most.

### Honest gap (Hunt 1)
**No primary human CD34+ HSPC metabolic-labeling / nascent-RNA dataset exists** (broad GEO + web
re-search this session: SLAM/4sU/TT/PRO-seq in primary HSPC returned none; all hematopoietic hits
are leukemia lines K562/THP-1). State this plainly. The nearest-to-HSPC synthesis ground truth is
hematopoietic-**leukemia** (K562/THP-1), which is why the validation must be framed as a
**cross-context gene-intrinsic rank test**, not a same-cell calibration.

---

## HUNT 2 — Bridge to the drug-timing goal without new wet-lab

**Question answered:** is there any public epigenetic-drug perturbation dataset with ≥3 timepoints
(any cell type) that could test "baseline chromatin/α predicts response **kinetics**" in a weak
cross-cell form? **Verdict up front: still no clean clearer** — this hunt confirms and slightly
extends the prior scout's conclusion. Two new weak-form options appear (LINCS, a bulk HDACi
microarray series), and both are feasibility/plumbing-grade only.

### 2A. GSE43010 — SAHA (vorinostat) transcriptome time series, BJ / BJ-LTSTERas — **BEST HIT (literal ≥3-tp clearer)**
- **ID / refs:** GEO **GSE43010** (via PMC4211306, *"Systematic Analysis of Time-Series Gene
  Expression Data on Tumor Cell-Selective Apoptotic Responses to HDAC Inhibitors"*).
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4211306/
- **What it is (verified):** **HDAC inhibitor SAHA/vorinostat** (bona-fide epigenetic drug),
  **3 genuine timepoints (4 h, 12 h, 24 h)**, Affymetrix HG-U133 Plus 2.0 **microarray**, **bulk**,
  in normal (BJ) vs transformed (BJ-LTSTERas) fibroblasts.
- **Fit verdict: PARTIAL — the Hunt-2 analog of how GSE201662 was handled.** It is the *only* new
  find that literally clears the ≥3-transcriptome-timepoint bar with a real epigenetic drug. But:
  **fibroblasts, not hematopoietic**; bulk microarray (coarse, no single-cell, no ATAC); only 3
  points over 24 h. Use **strictly as a feasibility/plumbing demonstrator** — prove the
  join + per-gene monotonic-response fit + nested decay-vs-lag model runs end-to-end against a real
  3-point HDACi curve — **never as validation** of the chromatin-lag→timing hypothesis. Exactly the
  role `drug_timing_arm_scout.md` §2 assigns GSE201662; GSE43010 is a cleaner plumbing target
  (real epigenetic drug, human, hours-scale) but a worse biological match (fibroblast).
- **What it enables:** an honest "the machinery works on a real HDACi 3-point series" figure, framed
  as a robustness/plumbing check, plus a per-gene onset-rate proof-of-concept the wet-lab arm would
  later replace.

### 2B. LINCS L1000 (GSE92742) — HDACi/DNMTi/BETi at scale — **does NOT clear the ≥3-tp bar**
- **ID / refs:** GEO **GSE92742** (LINCS Phase I, Broad); portal clue.io/data. ~1.3M profiles,
  >40k perturbagens, >70 cell lines, incl. vorinostat and other HDAC/DNMT/BET modulators.
- **Fit verdict: WEAK — explicitly does not clear the gate.** For most compound×cell combinations
  LINCS L1000 has **only 6 h + 24 h = 2 timepoints**, on **~978 landmark genes** (rest imputed).
  That is a 6 h→24 h slope/direction proxy, **not** a ≥3-point kinetic curve — it clears the bar no
  better than the prior 4 candidates. Its value is *scale + many cell lines* (incl. hematopoietic
  lines), not timing resolution.
- **What it enables:** at most a coarse **cross-cell direction/early-vs-late** sanity check
  (does a baseline-α/chromatin feature predict the 6→24 h *sign or slope* of response across many
  lines?). State the 2-timepoint / 978-gene limitation inline; do not present LINCS as a timing
  validation.

### 2C. sci-Plex (GSE139944) — HDACi in K562/A549/MCF7 — dose axis, not time axis
- **ID / refs:** GEO **GSE139944** (⚠️ confirm accession at use); Srivatsan et al., *"Massively
  multiplex chemical transcriptomics at single-cell resolution,"* *Science* 367(6473):45–51 (2020).
- **Fit verdict: WEAK / wrong axis.** Single-cell, includes HDAC inhibitors (vorinostat,
  pracinostat, etc.) in three lines — but the resolved axis is **dose (7 doses) at a single 24 h
  timepoint**, so it supports **dose-response, not timing**. Its **K562** arm is hematopoietic.
- **What it enables:** at most a **dose-response** sanity check (does baseline chromatin/α predict
  HDACi dose-sensitivity in K562?) — a magnitude claim, adjacent to but not the timing claim. Note
  it collapses the time axis exactly as GSE256354/GSE190785 did.

### 2D. Perturb-seq / epigenetic CRISPR screens — close-out (one line)
- Epigenetic Perturb-seq is **genetic (CRISPRi/KO of chromatin regulators), single-timepoint** — not
  pharmacological and not time-resolved (surveyed via PerturBase, *Nucleic Acids Res* 2025, NAR
  D1099). It cannot support a **drug**-timing kinetics claim. Closed.

### Net for Hunt 2
The prior scout's verdict **holds and hardens**: **no public single-cell, ≥3-timepoint,
epigenetic-drug transcriptome timecourse exists.** The headline timing claim remains **wet-lab
required**. Public data supports only (i) GSE43010 as a bulk HDACi 3-point *plumbing* demonstrator,
(ii) LINCS as a coarse 2-timepoint cross-cell *direction* proxy, (iii) sci-Plex K562 as a *dose*
sanity check — each explicitly framed as supporting, never validating. Combine with the mandatory
decay-controlled nested model (`drug_timing_arm_scout.md` §3.1) or the scoop risk vs Todorovski
escalates.

---

## HUNT 3 — Fresh scoop check (2025–2026)

**Three new items to cite; none scoops the specific negative result; one needs a proof-stage read.**

### 3A. Liu et al. 2026 — "Comprehensive benchmarking of RNA velocity methods across single-cell datasets" — **watch item, cite + differentiate**
- **ID / refs:** Jin Liu, Yida Wu, Chuihan Kong, Xu Liao, Zhixiang Lin, Xiaobo Sun. Research Square
  **rs-8708834**, doi:10.21203/rs.3.rs-8708834/v1 (posted **Feb 2026**).
  https://www.researchsquare.com/article/rs-8708834/v1
- **What it is:** 19 tools / 30 methods; 25 splicing-dynamics methods scored on **directional
  consistency, temporal precision, "negative-control robustness," sequencing-depth stability**, plus
  **5 multimodal-enhanced methods** on a "multimodal integration task." Headline: a **trade-off
  between directional consistency and negative-control robustness**.
- **Why it is the one to watch:** its phrase **"negative-control robustness"** *verbally collides*
  with our differentiator (c) — the causal within-lineage ATAC-shuffle control. But the collision is
  almost certainly superficial: in velocity benchmarks "negative-control robustness" conventionally
  means **does the method emit spurious velocity on null/steady-state/shuffled data for the velocity
  *direction*** — a randomized-baseline check on the **velocity vector**, whereas ours is an
  **ATAC-shuffle applied to the per-gene chromatin→transcription *lag***. Different object
  (direction vs lag) and different construction. And the "multimodal integration task" scores
  **integration/direction quality**, **not a per-gene lag concordance**.
- **Fit verdict on scoop: LOW risk, but confirm at proof stage.** ⚠️ I could not fetch the full PDF
  this session (size/403). **Before submission, read its negative-control and multimodal sections
  and confirm two things:** (1) it scores velocity direction/latent-time, **not** a per-gene
  chromatin→transcription lag concordance; (2) its "negative control" is a shuffled/null-data
  direction baseline, **not** a chromatin-shuffle-on-lag causal test. If both hold (expected), cite
  it as the third general benchmark (alongside refs [12],[13] in `related_work.md`) and differentiate
  in one sentence: *they score velocity direction under a null-data robustness axis; we score the
  cross-method reproducibility of the lag quantity with a causal chromatin-shuffle control.* If
  either is closer than expected, that is the real scoop risk — resolve it before writing the claim.

### 3B. BayVel (Bertoni et al.) 2025 — identifiability of the velocity ODE — **must-cite, supports premise**
- **ID / refs:** *"BayVel: A Bayesian Framework for RNA Velocity Estimation in Single-Cell
  Transcriptomics,"* **arXiv:2505.03083** (May 2025). https://arxiv.org/abs/2505.03083
- **What it says:** scVelo's velocity ODE suffers **identifiability problems**, heuristic
  preprocessing, and no uncertainty quantification; BayVel adds group-specific switching points and a
  subgroup structure for **more identifiable** elapsed-time estimation — yet still finds some real-data
  velocities violate biological expectation, "strengthening concerns about RNA velocity's
  applicability."
- **Fit verdict: SUPPORTING, no scoop.** It formalizes exactly our premise that a velocity-derived
  quantity must be robustness-checked, and gives the principled reason our **absolute** α/lag are not
  point-identifiable → **our α validation (Hunt 1) must stay rank-based.** One sentence links the two:
  *because the velocity ODE is only identifiable up to reparametrization (BayVel), we validate α by
  rank, not absolute value.* It is RNA-only and proposes a fix — it does not touch chromatin-lag
  concordance, so no novelty threat.

### 3C. TIVelo 2025 — RNA-only matches MultiVelo; multiome adds little — **supporting cite**
- **ID / refs:** *"TIVelo: RNA velocity estimation leveraging cluster-level trajectory inference,"*
  *Nature Communications* **16** (2025), s41467-025-61628-x, PMC12234748. (Confirm article number at
  proof.) https://www.nature.com/articles/s41467-025-61628-x
- **What it says:** an RNA-only method achieves comparable-or-better trajectories than the
  chromatin-using MultiVelo, and it notes MultiVelo's velocity does not always reflect the true
  erythroid trajectory.
- **Fit verdict: SUPPORTING, no scoop.** Independent evidence that **the chromatin modality does not
  reliably add robustness** on top of RNA — congruent with our α-robust/lag-fragile split and with the
  MultiVelo-lag-is-model-structural negative control. Cite as external corroboration; it benchmarks
  velocity *direction/trajectory*, not the lag quantity, so it is complementary, not competing.

### Scoop bottom line
Nothing found in 2025–2026 scoops the **specific** contribution (systematic multi-arm per-gene lag
concordance + permutation-FDR agreement test + causal ATAC-shuffle control + α-robust/lag-fragile
dissociation). Standing verdict from `related_work.md` (**NOVEL, partially anticipated by MoFlow's
incidental subset comparison; scoop low-to-moderate**) is unchanged. The only new action item is the
**proof-stage read of Liu et al. 2026** to confirm its "negative-control robustness" axis is
direction-on-null-data, not lag-on-chromatin-shuffle.

---

## Sources (URLs consulted 2026-07-07)
- GSE229314 (Todorovski, SLAM/TT/MAC-seq, K562/THP-1): https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE229314 · preprint https://www.biorxiv.org/content/10.1101/2022.04.06.487057v2.full · paper PMID 39372038 / PMC11447529
- GSE75792 (Schwalb/Cramer TT-seq K562, *Science* 2016): https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE75792 · https://www.science.org/doi/10.1126/science.aad9841
- ENCODE K562 POLR2A ChIP-seq: https://www.encodeproject.org · pause-initiation limit (Gressel eLife 2019): https://pmc.ncbi.nlm.nih.gov/articles/PMC6689055/
- SLAM-Drop-seq (single-cell kinetic rates, method ref): https://pmc.ncbi.nlm.nih.gov/articles/PMC10568207/
- GSE43010 / HDACi SAHA time series (4/12/24 h, BJ): https://pmc.ncbi.nlm.nih.gov/articles/PMC4211306/
- LINCS L1000 (GSE92742): https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0201937
- sci-Plex (Srivatsan 2020, GSE139944): https://www.science.org/doi/10.1126/science.aax6234 · https://pmc.ncbi.nlm.nih.gov/articles/PMC7289078/
- PerturBase (Perturb-seq DB, NAR 2025): https://academic.oup.com/nar/article/53/D1/D1099/7815638
- Liu et al. 2026 comprehensive velocity benchmark (rs-8708834): https://www.researchsquare.com/article/rs-8708834/v1
- BayVel (arXiv:2505.03083, 2025): https://arxiv.org/abs/2505.03083
- TIVelo (Nat Commun 2025, s41467-025-61628-x): https://www.nature.com/articles/s41467-025-61628-x · https://pmc.ncbi.nlm.nih.gov/articles/PMC12234748/

---

## 스쿱 리스크 해소 — Liu et al. 2026 (rs-8708834) [2026-07-07 확인]

PDF 직접취득은 403/10MB로 실패. 대신 검색 확인된 task 구조로 판정:
- Liu 2026 = 30 method × **8 task**(core: **directional consistency / temporal precision / negative-control robustness / sequencing-depth stability**), multimodal 5종(MultiVelo·Chromatin Velocity 등)은 별도 **"multimodal integration" task**로만 평가.
- 핵심 문구: "trade-off between directional consistency and negative-control robustness" → 그들의 "negative control robustness"는 **velocity 방향성**(null/무작위 데이터에서 spurious velocity 생성 여부)의 axis. splicing-dynamics 전체에 적용하는 일반 지표.
- **per-gene chromatin→transcription LAG의 cross-method 일치는 평가하지 않음**(multimodal은 integration만).
- **판정: 어휘 충돌(‘negative control’)뿐, 스쿱 아님.** 우리 축 = per-gene lag의 (a)비식별성·(b)ATAC-shuffle *인과대조*·(c)cross-method lag concordance = 다른 양·다른 대조. 동시기 벤치마크로 **인용+차별화** 처리. (proof stage에서 PDF 확보되면 negative-control 정의 원문 1줄 재확인 권장 — 잔여 불확실성 낮음.)

