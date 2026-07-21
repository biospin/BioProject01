# Reference expansion candidates — draft_v2.md ([1]–[26] → Genome Biology range 50–85)

**Status:** candidate list only. `draft_v2.md` / `draft_v2_ko.md` were **not** modified (BIOP01-61 constraint).
**Date:** 2026-07-19. **Ticket:** BIOP01-61 (item 3).

## Verification protocol (applies to every entry below)

Every candidate was resolved against the **CrossRef REST API** (`api.crossref.org`), and the bibliographic
fields below (authors, year, container-title, volume, issue, page, DOI) are **copied verbatim from the
returned JSON** — not from memory. Query script:
`/tmp/claude-10005/-home-kkkim-project/db9fddb6-6b72-477b-b80e-58da5ed4e708/scratchpad/cr.py`
(uses `query.bibliographic` for titles, `works/<DOI>` for known DOIs).

Two entries required a second source because CrossRef alone could not disambiguate them:
- **C27 (Todorovski)** — identified by resolving GEO accession **GSE229305** → its linked **PMID 39372038**
  → PubMed record → then confirmed by CrossRef DOI lookup. Both steps are recorded in the entry.
- **C7/C8 (DeepVelo)** — two *distinct* tools share the name; both are listed separately with their own DOIs.

**Nothing below is included on recall.** Any paper I could not resolve to a CrossRef record was dropped
rather than guessed. Preprints are labelled `[Preprint]`, matching the existing style of refs [13], [18], [19].

**Dedup check performed against [1]–[26].** Notably excluded because already cited:
veloVI (= [7], Gayoso 2024), scKINETICS (= [6], Su 2023), SHARE-seq / chromatin potential (= [14], Ma 2020),
Trevino fetal cortex (= [15]), MultiVelo/MultiVeloVAE/MoFlow/CRAK-Velo (= [1]–[4]), Bergen 2021 perspective (= [9]),
Gorin 2022 (= [10]), Marot-Lassauzaie 2022 (= [11]).
Also note: the primary dataset **GSE209878 is the MultiVelo paper's own data**, so [1] already serves as its source
citation — no separate dataset reference is needed.

**Priority tiers.** `A` = I judge this close to mandatory for a GB submission (foundational method the draft
actually uses, or a literature the draft borrows terminology from without citing). `B` = strengthens breadth,
safe to trim if the count runs long.

---

## Area 1 — RNA velocity methodological genealogy

### C1 [A] velocyto — the original RNA velocity paper (**currently uncited**)
- La Manno Gioele, Soldatov Ruslan, Zeisel Amit, Braun Emelie, Hochgerner Hannah, Petukhov Viktor, et al.
  "RNA velocity of single cells." *Nature* **560**(7719), 494–498 (2018). doi:10.1038/s41586-018-0414-6
- **Verified:** CrossRef `works/10.1038/s41586-018-0414-6` returned this exact title, author list, journal, volume, issue, pages.
- **Insert at:** Background, first sentence — *"RNA velocity infers the direction and speed of transcriptional change from the balance of unspliced and spliced mRNA, and a family of chromatin-informed extensions now couples this to single-cell ATAC…"*
  Also Methods §Datasets, where velocyto is used as a tool: *"with spliced and unspliced recovered from the GEX BAM by velocyto"*.
- **Why:** the founding paper of the entire field and a tool the Methods actually run; its absence is the single most visible gap.

### C2 [A] scVelo — the RNA-only floor's actual method paper (**currently uncited**)
- Bergen Volker, Lange Marius, Peidli Stefan, Wolf F. Alexander, Theis Fabian J.
  "Generalizing RNA velocity to transient cell states through dynamical modeling." *Nature Biotechnology* **38**(12), 1408–1414 (2020). doi:10.1038/s41587-020-0591-3
- **Verified:** CrossRef `works/10.1038/s41587-020-0591-3`, exact title/author/venue match.
- **Insert at:** Methods §Velocity methods and the RNA-only floor — *"Five arms were fit: an RNA-only floor (scVelo dynamical model, no chromatin channel)…"*; and Results §"The fitted transcription rate α…" at *"the textbook scVelo dynamical γ (the RNA-only floor) came out reversed"*.
- **Why:** the draft's entire baseline arm is scVelo's dynamical model, and a headline negative result (γ = −0.224 reversal) is attributed to it by name; ref [9] is the 2021 perspective, not the method.

### C3 [A] VeloAE
- Qiao Chen, Huang Yuanhua. "Representation learning of RNA velocity reveals robust cell transitions."
  *Proceedings of the National Academy of Sciences* **118**(49), e2105859118 (2021). doi:10.1073/pnas.2105859118
- **Verified:** CrossRef top hit, exact title match, journal/volume/issue/article-number as shown.
- **Insert at:** Background — after *"the RNA-only generative velocity our floor builds on (veloVI … [7]; the RNA-only Bayesian veloVAE [8]…) frame the landscape."*
- **Why:** low-dimensional-projection velocity is a distinct family the landscape sentence currently omits.

### C4 [A] UniTVelo
- Gao Mingze, Qiao Chen, Huang Yuanhua. "UniTVelo: temporally unified RNA velocity reinforces single-cell trajectory inference."
  *Nature Communications* **13**(1), 6586 (2022). doi:10.1038/s41467-022-34188-7
- **Verified:** CrossRef exact title match; journal/volume/article-number verbatim.
- **Insert at:** same landscape sentence as C3.
- **Why:** unified-latent-time formulation — directly relevant because the draft's lag is defined from switch times on a latent-time axis.

### C5 [A] cellDancer
- Li Shengyu, Zhang Pengzhi, Chen Weiqing, Ye Lingqun, Brannan Kristopher W., Le Nhat-Tu, et al.
  "A relay velocity model infers cell-dependent RNA velocity." *Nature Biotechnology* **42**(1), 99–108 (2024). doi:10.1038/s41587-023-01728-5
- **Verified:** CrossRef exact title match. (Searching the string "cellDancer" alone returns unrelated records — the tool name is not in the title; resolved via the actual title.)
- **Insert at:** same landscape sentence as C3.
- **Why:** cell-specific (non-shared) kinetic rates — the direct counter-design to the per-gene global rates whose reproducibility the paper measures.

### C6 [B] Dynamo
- Qiu Xiaojie, Zhang Yan, Martin-Rufino Jorge D., Weng Chen, Hosseinzadeh Shayan, Yang Dian, et al.
  "Mapping transcriptomic vector fields of single cells." *Cell* **185**(4), 690–711.e45 (2022). doi:10.1016/j.cell.2021.12.045
- **Verified:** CrossRef `works/10.1016/j.cell.2021.12.045`, exact match.
- **Insert at:** Background landscape sentence; alternatively Discussion — *"deeper sequencing, finer time resolution or metabolic labeling could yet render the lag identifiable."*
- **Why:** Dynamo is the canonical metabolic-labeling-based absolute-rate framework, which is exactly the remedy the Discussion gestures at without citing.

### C7 [B] DeepVelo (Chen/Gerstein version — **name collision, disambiguated**)
- Chen Zhanlin, King William C., Hwang Aheyon, Gerstein Mark, Zhang Jing.
  "DeepVelo: Single-cell transcriptomic deep velocity field learning with neural ordinary differential equations."
  *Science Advances* **8**(48), eabq3745 (2022). doi:10.1126/sciadv.abq3745
- **Verified:** CrossRef exact title match; note the CrossRef title string carries italic markup around "DeepVelo".
- **Insert at:** Background landscape sentence.
- **Why:** neural-ODE velocity family. **Cite together with C8 or not at all** — citing "DeepVelo" unqualified is ambiguous.

### C8 [B] DeepVelo (Cui/Wang version — **name collision, disambiguated**)
- Cui Haotian, Maan Hassaan, Vladoiu Maria C., Zhang Jiao, Taylor Michael D., Wang Bo.
  "DeepVelo: deep learning extends RNA velocity to multi-lineage systems with cell-specific kinetics."
  *Genome Biology* **25**(1), 27 (2024). doi:10.1186/s13059-023-03148-9
- **Verified:** CrossRef exact title match; distinct DOI, distinct author set, distinct venue from C7.
- **Insert at:** Background landscape sentence.
- **Why:** cell-specific kinetics in a multi-lineage setting — the same regime as HSPC; also a *Genome Biology* paper, useful for venue fit.

### C9 [B] LatentVelo
- Farrell Spencer, Mani Madhav, Goyal Sidhartha. "Inferring single-cell transcriptomic dynamics with structured latent gene expression dynamics."
  *Cell Reports Methods* **3**(9), 100581 (2023). doi:10.1016/j.crmeth.2023.100581
- **Verified:** CrossRef exact title match. (The tool name "LatentVelo" is not in the title; searching it alone returns unrelated records.)
- **Insert at:** Background landscape sentence.
- **Why:** latent-space dynamical velocity; completes the deep-generative branch alongside [7] and [8].

### C10 [B] cell2fate
- Aivazidis Alexander, Memi Fani, Kleshchevnikov Vitalii, Er Sezgin, Clarke Brian, Stegle Oliver, et al.
  "Cell2fate infers RNA velocity modules to improve cell fate prediction." *Nature Methods* **22**(4), 698–707 (2025). doi:10.1038/s41592-025-02608-3
- **Verified:** CrossRef returned both the 2023 bioRxiv preprint (doi:10.1101/2023.08.03.551650) and this peer-reviewed version; **the journal version is cited**.
- **Insert at:** Background landscape sentence, or Discussion §Consequence for downstream timing prediction.
- **Why:** module-level (rather than per-gene) velocity is the natural response to per-gene unreliability — supports the draft's own routing recommendation.

### C11 [B] Pyro-Velocity `[Preprint]`
- Qin Qian, Bingham Eli, La Manno Gioele, Langenau David M., Pinello Luca.
  "Pyro-Velocity: Probabilistic RNA Velocity inference from single-cell data." bioRxiv (2022). doi:10.1101/2022.09.12.507691 `[Preprint]`
- **Verified:** CrossRef `posted-content` record, exact title match. No journal version found in CrossRef as of this check.
- **Insert at:** Background landscape sentence, near the uncertainty-quantification clause *"(veloVI, which adds posterior velocity uncertainty [7]…)"*.
- **Why:** Bayesian posterior uncertainty over velocity — the same concern the draft's bootstrap CIs and [16] address.

### C12 [B] mmVelo `[Preprint]`
- Nomura Satoshi, Kojima Yasuhiro, Minoura Kodai, Hayashi Shuto, Abe Ko, Hirose Haruka, et al.
  "mmVelo: A deep generative model for estimating cell state-dependent dynamics across multiple modalities."
  bioRxiv (2024). doi:10.1101/2024.12.11.628059 `[Preprint]`
- **Verified:** CrossRef `posted-content`, exact title match.
- **Insert at:** Background, in the multiome-methods enumeration alongside [5] and [6] — *"Same-family alternatives (archetypal ATAC-plus-RNA trajectory modeling [5]; regulatory velocity from differential-accessibility priors [6])…"*
- **Why:** a multimodal velocity arm already logged in this project's own `dataset-info.yaml` as a related method; completes the multiome-family census a reviewer will check for.

### C13 [A] CellRank
- Lange Marius, Bergen Volker, Klein Michal, Setty Manu, Reuter Bernhard, Bakhti Mostafa, et al.
  "CellRank for directed single-cell fate mapping." *Nature Methods* **19**(2), 159–170 (2022). doi:10.1038/s41592-021-01346-6
- **Verified:** CrossRef `works/10.1038/s41592-021-01346-6` (the free-text search returns only the 2020 preprints; the journal record was pulled by DOI).
- **Insert at:** Results §"The cell×gene velocity matrix does not reproduce across methods either" — *"the cell×gene velocity matrix that every method emits before any embedding projection."*
- **Why:** CellRank is *the* main downstream consumer of the velocity matrix; the draft's reliability map is a statement about what CellRank-style consumers are fed.

### C14 [B] CellRank 2
- Weiler Philipp, Lange Marius, Klein Michal, Pe'er Dana, Theis Fabian. "CellRank 2: unified fate mapping in multiview single-cell data."
  *Nature Methods* **21**(7), 1196–1205 (2024). doi:10.1038/s41592-024-02303-9
- **Verified:** CrossRef exact title match.
- **Insert at:** with C13, or Discussion §Consequence for downstream timing prediction.
- **Why:** shows the field already routes around raw velocity toward multiview kernels — supports the draft's routing rule rather than contradicting it.

---

## Area 2 — velocity critique and limitations

### C15 [A] Zheng et al. — "Pumping the brakes"
- Zheng Shijie C., Stein-O'Brien Genevieve, Boukas Leandros, Goff Loyal A., Hansen Kasper D.
  "Pumping the brakes on RNA velocity by understanding and interpreting RNA velocity estimates."
  *Genome Biology* **24**(1), 246 (2023). doi:10.1186/s13059-023-03065-x
- **Verified:** CrossRef exact title match; journal version (the 2022 bioRxiv preprint has a slightly different subtitle and is *not* what is cited).
- **Insert at:** Background — *"The velocity-critique literature is emphatic that many velocity readouts fail even this — violated model assumptions and multiple kinetic regimes produce wrong velocities [9], the pipelines carry many user-set hyperparameters and are often not actionable [10]…"*
- **Why:** the most-cited critique of velocity *estimates* (as opposed to the vector field), published in the target journal, and currently absent from a critique list that reads as complete.

### C16 [A] VeloCycle — statistical inference and identifiability for velocity
- Lederer Alex R., Leonardi Maxine, Talamanca Lorenzo, Bobrovskiy Daniil M., Herrera Antonio, Droin Colas, et al.
  "Statistical inference with a manifold-constrained RNA velocity model uncovers cell cycle speed modulations."
  *Nature Methods* **21**(12), 2271–2286 (2024). doi:10.1038/s41592-024-02471-8
- **Verified:** CrossRef exact title match; author order copied from the journal record (the preprint record has a different author ordering).
- **Insert at:** Results §"The dissociation is a property of the objective function" — *"the weak identifiability of the velocity switch-time itself was established by ConsensusVelo through likelihood flatness and Fisher information [16]"*.
- **Why:** the other major "put velocity on a statistical-inference footing" paper; alongside [16] it establishes that the draft's identifiability framing is a live literature, not an isolated claim.

### C17 [B] Barile et al. — kinetics validated against an orthogonal readout
- Barile Melania, Imaz-Rosshandler Ivan, Inzani Isabella, Ghazanfar Shila, Nichols Jennifer, Marioni John C., et al.
  "Coordinated changes in gene expression kinetics underlie both mouse and human erythroid maturation."
  *Genome Biology* **22**(1), 197 (2021). doi:10.1186/s13059-021-02414-y
- **Verified:** CrossRef exact title match.
- **Insert at:** Background — *"The second face of reliability is external and is almost never tested for velocity: does a fitted rate recover an independently measured kinetic quantity?"*
- **Why:** one of the few prior studies that compares inferred kinetics to an orthogonal measurement in a haematopoietic lineage; qualifies "almost never" honestly and pre-empts a reviewer objection. Also a *Genome Biology* paper.

---

## Area 3 — single-cell multiome / chromatin accessibility methodology

### C18 [A] ArchR
- Granja Jeffrey M., Corces M. Ryan, Pierce Sarah E., Bagdatli S. Tansu, Choudhry Hani, Chang Howard Y., et al.
  "ArchR is a scalable software package for integrative single-cell chromatin accessibility analysis."
  *Nature Genetics* **53**(3), 403–411 (2021). doi:10.1038/s41588-021-00790-6
- **Verified:** CrossRef exact title match. (An Author Correction exists at doi:10.1038/s41588-021-00850-x — cite the primary record.)
- **Insert at:** Methods §Common preprocessing and method branch — *"ATAC aggregation differed by dataset provenance (HSPC via `mv.aggregate_peaks_10x`; BMMC via gencode-proximity aggregation of the processed peak matrix; gastrulation via GEO fragments over gene bodies ±10 kb)"*.
- **Why:** the draft performs three *different* ad-hoc peak-to-gene aggregations and calls this "conservative noise"; citing the standard aggregation frameworks shows the choice was informed rather than improvised.

### C19 [A] Signac
- Stuart Tim, Srivastava Avi, Madad Shaista, Lareau Caleb A., Satija Rahul. "Single-cell chromatin state analysis with Signac."
  *Nature Methods* **18**(11), 1333–1341 (2021). doi:10.1038/s41592-021-01282-5
- **Verified:** CrossRef exact title match (journal record; the CRAN package record and the 2020 preprint were rejected).
- **Insert at:** with C18.
- **Why:** the reference gene-activity/peak-aggregation implementation the draft's aggregation must be positioned against.

### C20 [B] Seurat WNN — the multiome integration standard
- Hao Yuhan, Hao Stephanie, Andersen-Nissen Erica, Mauck William M., Zheng Shiwei, Butler Andrew, et al.
  "Integrated analysis of multimodal single-cell data." *Cell* **184**(13), 3573–3587.e29 (2021). doi:10.1016/j.cell.2021.04.048
- **Verified:** CrossRef `works/10.1016/j.cell.2021.04.048`, exact match.
- **Insert at:** Methods §Datasets — *"day0 and day7 integrated, 21,878 cells"* / the batch-integration caveat.
- **Why:** the primary dataset is Seurat-integrated, and the pseudotime-vs-wall-clock caveat hinges on that integration.

### C21 [B] cisTopic
- Bravo González-Blas Carmen, Minnoye Liesbeth, Papasokrati Dafni, Aibar Sara, Hulselmans Gert, Christiaens Valerie, et al.
  "cisTopic: cis-regulatory topic modeling on single-cell ATAC-seq data." *Nature Methods* **16**(5), 397–400 (2019). doi:10.1038/s41592-019-0367-1
- **Verified:** CrossRef exact title match.
- **Insert at:** with C18/C19.
- **Why:** the topic-model alternative to peak aggregation; shows the aggregation choice was one of several.

### C22 [B] chromVAR
- Schep Alicia N, Wu Beijing, Buenrostro Jason D, Greenleaf William J. "chromVAR: inferring transcription-factor-associated accessibility from single-cell epigenomic data."
  *Nature Methods* **14**(10), 975–978 (2017). doi:10.1038/nmeth.4401
- **Verified:** CrossRef exact title match.
- **Insert at:** Results §"The lag is unpredictable from baseline features that predict α" — *"Assembling real day0 ATAC promoter and enhancer accessibility (511 genes over 8,583 day0 HSC/MPP cells)"*.
- **Why:** the standard alternative featurization of baseline accessibility; a reviewer will ask why promoter/enhancer counts rather than TF-motif deviations.

### C23 [B] MOFA+
- Argelaguet Ricard, Arnol Damien, Bredikhin Danila, Deloro Yonatan, Velten Britta, Marioni John C., et al.
  "MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data."
  *Genome Biology* **21**(1), 111 (2020). doi:10.1186/s13059-020-02015-1
- **Verified:** CrossRef exact title match.
- **Insert at:** Background, near the multiome-methods enumeration; or Methods §Common preprocessing.
- **Why:** the non-kinetic multiome-integration baseline — what one does with paired data if one does *not* fit a velocity model. Also *Genome Biology*.

### C24 [B] sci-CAR — origin of paired RNA+ATAC profiling
- Cao Junyue, Cusanovich Darren A., Ramani Vijay, Aghamirzaie Delasa, Pliner Hannah A., Hill Andrew J., et al.
  "Joint profiling of chromatin accessibility and gene expression in thousands of single cells."
  *Science* **361**(6409), 1380–1385 (2018). doi:10.1126/science.aau0730
- **Verified:** CrossRef `works/10.1126/science.aau0730`, exact match.
- **Insert at:** Background, first sentence — *"a family of chromatin-informed extensions now couples this to single-cell ATAC"*.
- **Why:** the assay-origin citation for paired multiome; [14] covers SHARE-seq but not the sci-CAR lineage.

---

## Area 4 — metabolic-labeling measurement of RNA kinetics

### C25 [A] TT-seq (**the draft names this source in Methods with no citation**)
- Schwalb Björn, Michel Margaux, Zacher Benedikt, Frühauf Katja, Demel Carina, Tresch Achim, et al.
  "TT-seq maps the human transient transcriptome." *Science* **352**(6290), 1225–1228 (2016). doi:10.1126/science.aad9841
- **Verified:** CrossRef exact title match (a same-issue editor's summary "TT-Seq maps a transient transcriptome" was rejected as the wrong record).
- **Insert at:** Methods §External rate validation — *"a second source, Schwalb 2016 K562 TT-seq, GSE75792"* — and Results §"A second external source was null": *"An independent second α source (Schwalb 2016 K562 TT-seq, GSE75792) was null"*.
- **Why:** **highest priority in this area.** The draft refers to "Schwalb 2016" by author-year in two places and it has no entry in [1]–[26] — a straightforward citation defect.

### C26 [A] SLAM-seq
- Herzog Veronika A, Reichholf Brian, Neumann Tobias, Rescheneder Philipp, Bhat Pooja, Burkard Thomas R, et al.
  "Thiol-linked alkylation of RNA to assess expression dynamics." *Nature Methods* **14**(12), 1198–1204 (2017). doi:10.1038/nmeth.4435
- **Verified:** CrossRef exact title match (the Protocol Exchange record doi:10.1038/protex.2017.105 was rejected).
- **Insert at:** Background — *"Metabolic-labeling assays (TT-seq for synthesis, SLAM-seq half-lives for degradation) now make this test possible"*; also Methods §External rate validation.
- **Why:** the assay that produces the half-life ground truth against which γ fails — the paper's second headline negative result.

### C27 [A] Todorovski et al. — the actual source of GSE229305 (**named in Methods, uncited**)
- Todorovski Izabela, Tsang Mary-Jane, Feran Breon, Fan Zheng, Gadipally Sreeja, Yoannidis David, et al.
  "RNA kinetics influence the response to transcriptional perturbation in leukaemia cell lines."
  *NAR Cancer* **6**(4), zcae039 (2024). doi:10.1093/narcan/zcae039
- **Verified (two-step):** GEO **GSE229305** page gives title *"RNA decay defines the therapeutic response to transcriptional perturbation in leukemia [TTseq K562 production rates]"*, contributors Todorovski/Johnstone/Vervoort, linked **PMID 39372038**; PubMed 39372038 gives the citation above; CrossRef `works/10.1093/narcan/zcae039` returned matching title/authors/venue/volume/issue/article-number.
- **Insert at:** Methods §External rate validation — *"α versus measured K562 TT-seq synthesis rate (GSE229305, Todorovski 2024…)"*; and Results — *"the measured K562 TT-seq synthesis rate (GSE229305, the same study as the half-life panel)"*.
- **Why:** **the paper's entire external-validation axis rests on this dataset** and it is currently cited only as an accession + author-year. Note the journal title uses "leukaemia"; GEO's series title differs — do not conflate them.

### C28 [B] scEU-seq
- Battich Nico, Beumer Joep, de Barbanson Buys, Krenning Lenno, Baron Chloé S., Tanenbaum Marvin E., et al.
  "Sequencing metabolically labeled transcripts in single cells reveals mRNA turnover strategies."
  *Science* **367**(6482), 1151–1156 (2020). doi:10.1126/science.aax3072
- **Verified:** CrossRef exact title match.
- **Insert at:** Discussion — *"deeper sequencing, finer time resolution or metabolic labeling could yet render the lag identifiable."*
- **Why:** the concrete single-cell realization of the remedy the Discussion proposes; makes the limitation constructive.

### C29 [B] sci-fate
- Cao Junyue, Zhou Wei, Steemers Frank, Trapnell Cole, Shendure Jay. "Sci-fate characterizes the dynamics of gene expression in single cells."
  *Nature Biotechnology* **38**(8), 980–988 (2020). doi:10.1038/s41587-020-0480-9
- **Verified:** CrossRef exact title match.
- **Insert at:** with C28.
- **Why:** combinatorial-indexing labeling at scale — the throughput-feasible version of the same remedy.

### C30 [B] scSLAM-seq
- Erhard Florian, Baptista Marisa A. P., Krammer Tobias, Hennig Thomas, Lange Marius, Arampatzi Panagiota, et al.
  "scSLAM-seq reveals core features of transcription dynamics in single cells." *Nature* **571**(7765), 419–423 (2019). doi:10.1038/s41586-019-1369-y
- **Verified:** CrossRef exact title match (a Faculty Opinions recommendation record was rejected).
- **Insert at:** with C28/C29, or Background at the metabolic-labeling sentence.
- **Why:** demonstrates that per-cell nascent/old separation is achievable — the direct experimental alternative to inferring the lag.

---

## Area 5 — identifiability and sloppy-model theory (**terminology used, currently uncited**)

### C31 [A] Gutenkunst et al. — the origin of "sloppy"
- Gutenkunst Ryan N, Waterfall Joshua J, Casey Fergal P, Brown Kevin S, Myers Christopher R, Sethna James P.
  "Universally Sloppy Parameter Sensitivities in Systems Biology Models." *PLoS Computational Biology* **3**(10), e189 (2007). doi:10.1371/journal.pcbi.0030189
- **Verified:** CrossRef exact title match. **Caution:** CrossRef also returns an "eor" (early-online) stub at doi:10.1371/journal.pcbi.0030189.eor with year 2005 and volume "preprint" — that record is *not* the citable one; use the DOI above.
- **Insert at:** Results heading and body of §"The dissociation is a property of the objective function: α is stiff, the lag is sloppy" — *"This is a relative (practical) non-identifiability of the lag direction, not a fully flat valley."*
- **Why:** **highest priority in this area.** The paper's central metaphor ("stiff"/"sloppy") is a technical term of art from this literature and is currently used with no attribution — a GB reviewer will flag it immediately.

### C32 [A] Raue et al. — profile-likelihood identifiability, the method the draft runs
- Raue A., Kreutz C., Maiwald T., Bachmann J., Schilling M., Klingmüller U., et al.
  "Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood."
  *Bioinformatics* **25**(15), 1923–1929 (2009). doi:10.1093/bioinformatics/btp358
- **Verified:** CrossRef exact title match.
- **Insert at:** Methods §Profile-likelihood identifiability and its alignment with external validation — *"MultiVelo's objective (likelihood) was profiled along the α axis and the lag axis … with latent time re-optimized at each scan point"*; and the structural/practical distinction in Discussion.
- **Why:** the draft's method *is* profile likelihood, and its structural-vs-practical non-identifiability distinction comes from here. Ref [17] is a single-cell application, not the methodological source.

### C33 [A] Transtrum et al. — geometry of sloppy models
- Transtrum Mark K., Machta Benjamin B., Sethna James P. "Geometry of nonlinear least squares with applications to sloppy models and optimization."
  *Physical Review E* **83**(3), 036701 (2011). doi:10.1103/physreve.83.036701
- **Verified:** CrossRef exact title match.
- **Insert at:** Results §"α is stiff, the lag is sloppy" — *"Per-cell curvature was far higher for α than for the lag (median 8.20 versus 2.24 per cell)."*
- **Why:** the curvature/stiff-direction formalism the draft's κ_α/κ_lag ratio implements.

### C34 [B] Transtrum et al. — sloppiness perspective
- Transtrum Mark K., Machta Benjamin B., Brown Kevin S., Daniels Bryan C., Myers Christopher R., Sethna James P.
  "Perspective: Sloppiness and emergent theories in physics, biology, and beyond." *The Journal of Chemical Physics* **143**(1), 010901 (2015). doi:10.1063/1.4923066
- **Verified:** CrossRef exact title match.
- **Insert at:** Discussion — where the draft argues the dissociation is a property of the objective rather than of any method.
- **Why:** frames the α-stiff/lag-sloppy dissociation as an instance of a general phenomenon, which strengthens the generality claim without overreaching. Note this also *tempers* novelty — the draft should cite it and then state what is new (the multiome/lag-specific dissociation).

### C35 [B] Kreutz et al. — profile likelihood in systems biology
- Kreutz Clemens, Raue Andreas, Kaschek Daniel, Timmer Jens. "Profile likelihood in systems biology." *The FEBS Journal* **280**(11), 2564–2571 (2013). doi:10.1111/febs.12276
- **Verified:** CrossRef exact title match.
- **Insert at:** Methods §Profile-likelihood, with C32.
- **Why:** justifies the fixed-nuisance vs freed-nuisance profiling regimes the draft reports as bound and conservative estimate.

### C36 [B] Villaverde et al. — structural identifiability
- Villaverde Alejandro F., Barreiro Antonio, Papachristodoulou Antonis. "Structural Identifiability of Dynamic Systems Biology Models."
  *PLOS Computational Biology* **12**(10), e1005153 (2016). doi:10.1371/journal.pcbi.1005153
- **Verified:** CrossRef exact title match.
- **Insert at:** Discussion — *"the profile-likelihood result is a relative (practical) non-identifiability, not a fully flat valley"*.
- **Why:** supports the draft's careful practical-vs-structural hedge, which is currently asserted without a reference.

### C37 [B] Simpson & Maclaren — profile-likelihood workflow
- Simpson Matthew J., Maclaren Oliver J. "Profile-Wise Analysis: A profile likelihood-based workflow for identifiability analysis, estimation, and prediction with mechanistic mathematical models."
  *PLOS Computational Biology* **19**(9), e1011515 (2023). doi:10.1371/journal.pcbi.1011515
- **Verified:** CrossRef returned both the 2022 preprint (doi:10.1101/2022.12.14.520367) and this journal version; **the journal version is cited**.
- **Insert at:** Methods §Profile-likelihood.
- **Why:** a current, citable workflow standard for exactly the analysis performed — useful if a reviewer asks whether the profiling protocol is standard.

---

## Area 6 — haematopoietic differentiation biology

### C38 [A] Velten et al. — continuous HSPC commitment
- Velten Lars, Haas Simon F., Raffel Simon, Blaszkiewicz Sandra, Islam Saiful, Hennig Bianca P., et al.
  "Human haematopoietic stem cell lineage commitment is a continuous process." *Nature Cell Biology* **19**(4), 271–281 (2017). doi:10.1038/ncb3493
- **Verified:** CrossRef exact title match.
- **Insert at:** Background, second paragraph — *"Our own motivating goal is to predict the timing of epigenetic-drug responses…"*; or Results §replication where lineages are enumerated.
- **Why:** the biological justification for treating HSPC as a continuum and for within-lineage analysis; the draft is a HSPC paper with essentially no HSPC-biology citations.

### C39 [A] Laurenti & Göttgens — haematopoiesis landscape review
- Laurenti Elisa, Göttgens Berthold. "From haematopoietic stem cells to complex differentiation landscapes."
  *Nature* **553**(7689), 418–426 (2018). doi:10.1038/nature25022
- **Verified:** CrossRef exact title match (a Faculty Opinions record was rejected).
- **Insert at:** Background, at the first mention of *"human hematopoietic stem and progenitor cells (HSPCs)"* (Abstract §Background / Background §1).
- **Why:** the standard review citation for the system; a GB reviewer expects the biology to be anchored.

### C40 [B] Buenrostro et al. — regulatory landscape of human haematopoiesis
- Buenrostro Jason D., Corces M. Ryan, Lareau Caleb A., Wu Beijing, Schep Alicia N., Aryee Martin J., et al.
  "Integrated Single-Cell Analysis Maps the Continuous Regulatory Landscape of Human Hematopoietic Differentiation."
  *Cell* **173**(6), 1535–1548.e16 (2018). doi:10.1016/j.cell.2018.03.074
- **Verified:** CrossRef exact title match.
- **Insert at:** Background — the *"chromatin potential"* sentence, next to [14].
- **Why:** the chromatin-priming evidence *specifically in haematopoiesis*, i.e. the system this paper tests; [14] and [15] are skin and cortex.

### C41 [B] Setty et al. — Palantir
- Setty Manu, Kiseliovas Vaidotas, Levine Jacob, Gayoso Adam, Mazutis Linas, Pe'er Dana.
  "Characterization of cell fate probabilities in single-cell data with Palantir." *Nature Biotechnology* **37**(4), 451–460 (2019). doi:10.1038/s41587-019-0068-4
- **Verified:** CrossRef exact title match (an Author Correction exists at doi:10.1038/s41587-019-0282-0 — cite the primary record).
- **Insert at:** Methods §Datasets / the pseudotime caveat — *"Pseudotime is not wall-clock"*.
- **Why:** the standard HSPC pseudotime/fate-probability method; anchors the pseudotime caveat in an actual method.

### C42 [B] Weinreb et al. — lineage tracing as fate ground truth
- Weinreb Caleb, Rodriguez-Fraticelli Alejo, Camargo Fernando D., Klein Allon M.
  "Lineage tracing on transcriptional landscapes links state to fate during differentiation." *Science* **367**(6479), eaaw3381 (2020). doi:10.1126/science.aaw3381
- **Verified:** CrossRef exact title match.
- **Insert at:** Discussion §Consequence for downstream timing prediction — *"validating the ATAC-to-α-to-timing route against a perturbation ground truth is the natural next step"*.
- **Why:** the field's actual ground truth for fate in haematopoiesis; names a concrete validation route instead of an abstract one.

### C43 [A] Cowland & Borregaard — granulopoiesis and neutrophil granules
- Cowland Jack B., Borregaard Niels. "Granulopoiesis and granules of human neutrophils." *Immunological Reviews* **273**(1), 11–28 (2016). doi:10.1111/imr.12440
- **Verified:** CrossRef exact title match.
- **Insert at:** Results §"Only the transcription rate α…" — *"the granule markers MPO, ELANE, AZU1, LYZ and S100A9 were chromatin-leading in every method that scored them"* and *"The unanimous chromatin-leading set is enriched for the azurophil-granule programme (Reactome neutrophil degranulation…)"*.
- **Why:** the draft names five granule genes and an azurophil-granule programme with no biology citation; this is the reference work on the staged granule programme.

### C44 [B] Borregaard — neutrophil development
- Borregaard Niels. "Neutrophils, from Marrow to Microbes." *Immunity* **33**(5), 657–670 (2010). doi:10.1016/j.immuni.2010.11.011
- **Verified:** CrossRef exact title match.
- **Insert at:** with C43.
- **Why:** the developmental-staging account that makes "azurophil granule = early" meaningful to a non-haematology reader.

### C45 [B] Borregaard et al. — granule protein library
- Borregaard Niels, Sørensen Ole E., Theilgaard-Mönch Kim. "Neutrophil granules: a library of innate immunity proteins."
  *Trends in Immunology* **28**(8), 340–345 (2007). doi:10.1016/j.it.2007.06.002
- **Verified:** CrossRef exact title match.
- **Insert at:** with C43, at the Reactome-enrichment sentence.
- **Why:** identifies MPO/ELANE/AZU1 as the azurophil set specifically — makes the enrichment statement checkable.

### C46 [A] Reactome — the enrichment resource actually used
- Gillespie Marc, Jassal Bijay, Stephan Ralf, Milacic Marija, Rothfels Karen, Senff-Ribeiro Andrea, et al.
  "The reactome pathway knowledgebase 2022." *Nucleic Acids Research* **50**(D1), D687–D692 (2022). doi:10.1093/nar/gkab1028
- **Verified:** CrossRef `works/10.1093/nar/gkab1028`, exact match. (Free-text search returns individual Reactome pathway records, not the database paper — resolved by DOI.)
- **Insert at:** Results — *"(Reactome neutrophil degranulation, adjusted p=9.4e-04 against a background restricted to the genes we could score)"*.
- **Why:** a named database used for a reported p-value must be cited; **confirm the Reactome release version actually used before adopting this year's citation.**

---

## Area 7 — benchmarking methodology, statistics and reproducibility

### C47 [A] Weber et al. — benchmarking guidelines
- Weber Lukas M., Saelens Wouter, Cannoodt Robrecht, Soneson Charlotte, Hapfelmeier Alexander, Gardner Paul P., et al.
  "Essential guidelines for computational method benchmarking." *Genome Biology* **20**(1), 125 (2019). doi:10.1186/s13059-019-1738-8
- **Verified:** CrossRef exact title match.
- **Insert at:** Background — *"We therefore treat the velocity outputs not as findings but as candidates to be sorted by reliability."*; or Methods §Concordance statistics.
- **Why:** this is a benchmarking paper submitted to the journal that published the benchmarking guidelines; citing them signals compliance (neutrality, common preprocessing, preregistered criteria) — all of which the draft actually does.

### C48 [A] Nosek et al. — preregistration
- Nosek Brian A., Ebersole Charles R., DeHaven Alexander C., Mellor David T. "The preregistration revolution."
  *Proceedings of the National Academy of Sciences* **115**(11), 2600–2606 (2018). doi:10.1073/pnas.1708274114
- **Verified:** CrossRef `works/10.1073/pnas.1708274114`, exact match. (Free-text search returns the OSF preprint doi:10.31219/osf.io/2dxu5 — the PNAS record was pulled by DOI.)
- **Insert at:** Results §"The α-robust, lag-fragile ordering replicates…" — *"was tested by **preregistration**: six predictions with pre-declared thresholds were sealed by commit hash before any velocity fit or concordance existed"*; and Methods §Preregistration protocol.
- **Why:** the draft's most distinctive methodological move is preregistration in a computational-biology benchmark; it currently has no methodological citation. This makes the move legible as an established practice rather than an idiosyncrasy.

### C49 [B] Sonrel et al. — benchmark meta-analysis
- Sonrel Anthony, Luetge Almut, Soneson Charlotte, Mallona Izaskun, Germain Pierre-Luc, Knyazev Sergey, et al.
  "Meta-analysis of (single-cell method) benchmarks reveals the need for extensibility and interoperability."
  *Genome Biology* **24**(1), 119 (2023). doi:10.1186/s13059-023-02962-5
- **Verified:** CrossRef exact title match (journal version; the 2022 preprint has the same title and was rejected in favour of the published record).
- **Insert at:** Background — *"Two 2026 benchmarks establish that velocity direction is method-dependent with no universal winner [12,13]"*.
- **Why:** documents that single-cell benchmarks are frequently not extensible or reusable — the framing for why this paper ships deterministic recomputation scripts.

### C50 [B] Luecken et al. — a model benchmark design
- Luecken Malte D., Büttner M., Chaichoompu K., Danese A., Interlandi M., Mueller M. F., et al.
  "Benchmarking atlas-level data integration in single-cell genomics." *Nature Methods* **19**(1), 41–50 (2022). doi:10.1038/s41592-021-01336-8
- **Verified:** CrossRef exact title match (a Faculty Opinions record was rejected).
- **Insert at:** with C47, in the Background benchmarking framing.
- **Why:** the field-standard example of a multi-metric, multi-dataset benchmark; a design precedent for the four-axis reliability map.

### C51 [A] Benjamini & Hochberg — the FDR procedure used throughout
- Benjamini Yoav, Hochberg Yosef. "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing."
  *Journal of the Royal Statistical Society Series B: Statistical Methodology* **57**(1), 289–300 (1995). doi:10.1111/j.2517-6161.1995.tb02031.x
- **Verified:** CrossRef exact title match.
- **Insert at:** Methods §Concordance statistics — *"Cross-method sign-consistency was tested by permutation FDR (gene-label shuffle null, N=10⁴, FDR<0.10)"*; also §Confound controls — *"multiple testing across genes used permutation FDR"*.
- **Why:** FDR control appears in the abstract, the results and two Methods subsections with no statistical citation.

### C52 [A] Schuirmann — TOST equivalence testing
- Schuirmann Donald J. "A comparison of the Two One-Sided Tests Procedure and the Power Approach for assessing the equivalence of average bioavailability."
  *Journal of Pharmacokinetics and Biopharmaceutics* **15**(6), 657–680 (1987). doi:10.1007/bf01068419
- **Verified:** CrossRef exact title match (rejected several table/figure component records).
- **Insert at:** Results §replication — *"macrophage +0.865 versus +0.074 (equivalent to 0 by TOST)"*.
- **Why:** an equivalence claim ("equivalent to 0") is asserted via TOST with no citation; equivalence testing is unfamiliar enough in this literature that a reviewer will want the source.

### C53 [B] Peng — reproducible computational research
- Peng Roger D. "Reproducible Research in Computational Science." *Science* **334**(6060), 1226–1227 (2011). doi:10.1126/science.1213847
- **Verified:** CrossRef exact title match.
- **Insert at:** Background reproducibility paragraph, with [20]–[26]; or Methods §Datasets and code availability.
- **Why:** the computational-science counterpart to [20]–[26], which are all wet-lab/psychology; the draft's own claim is computational.

### C54 [B] Munafò et al. — manifesto for reproducible science
- Munafò Marcus R., Nosek Brian A., Bishop Dorothy V. M., Button Katherine S., Chambers Christopher D., Percie du Sert Nathalie, et al.
  "A manifesto for reproducible science." *Nature Human Behaviour* **1**(1), 0021 (2017). doi:10.1038/s41562-016-0021
- **Verified:** CrossRef `works/10.1038/s41562-016-0021`, exact match (free-text search returns a Faculty Opinions record — resolved by DOI).
- **Insert at:** Background reproducibility paragraph, with [23]–[25].
- **Why:** connects the diagnosis in [20]–[26] to the remedies this paper applies (preregistration, negative controls, deterministic recomputation).

### C55 [B] Wilkinson et al. — FAIR principles
- Wilkinson Mark D., Dumontier Michel, Aalbersberg IJsbrand Jan, Appleton Gabrielle, Axton Myles, Baak Arie, et al.
  "The FAIR Guiding Principles for scientific data management and stewardship." *Scientific Data* **3**(1), 160018 (2016). doi:10.1038/sdata.2016.18
- **Verified:** CrossRef `works/10.1038/sdata.2016.18`, exact match.
- **Insert at:** Methods §Datasets and code availability — *"Analysis code, the sealed preregistration, and the deterministic recomputation scripts … are archived at `<FILL: repository/DOI + license>`."*
- **Why:** justifies the archiving/licensing plan the `<FILL>` will resolve to.

### C56 [B] SCANPY — the analysis framework
- Wolf F. Alexander, Angerer Philipp, Theis Fabian J. "SCANPY: large-scale single-cell gene expression data analysis."
  *Genome Biology* **19**(1), 15 (2018). doi:10.1186/s13059-017-1382-0
- **Verified:** CrossRef exact title match.
- **Insert at:** Methods §Common preprocessing and method branch.
- **Why:** the preprocessing stack every arm shares; a tools-citation gap. Also *Genome Biology*.

### C57 [B] Scrublet — named in Methods, uncited
- Wolock Samuel L., Lopez Romain, Klein Allon M. "Scrublet: Computational Identification of Cell Doublets in Single-Cell Transcriptomic Data."
  *Cell Systems* **8**(4), 281–291.e9 (2019). doi:10.1016/j.cels.2018.11.005
- **Verified:** CrossRef exact title match.
- **Insert at:** Methods §Confound controls — *"Ambient/doublet: scrublet applied, doublet median 0.045"*.
- **Why:** a named tool with a reported number and no citation.

### C58 [B] STARsolo — named in Methods, uncited `[Preprint]`
- Kaminow Benjamin, Yunusov Dinar, Dobin Alexander. "STARsolo: accurate, fast and versatile mapping/quantification of single-cell and single-nucleus RNA-seq data."
  bioRxiv (2021). doi:10.1101/2021.05.05.442755 `[Preprint]`
- **Verified:** CrossRef `posted-content`, exact title match. No peer-reviewed version located in CrossRef at this check — **label `[Preprint]`**; alternatively cite STAR (Dobin 2013) instead, which was **not** verified in this pass and must be checked before use.
- **Insert at:** Methods §Datasets — *"mouse gastrulation (GSE205117 … GEX via STARsolo Velocyto raw…)"*.
- **Why:** the quantification tool for the preregistered external dataset; a named tool with no citation.

### C59 [B] SEACells — HSPC multiome resource
- Persad Sitara, Choo Zi-Ning, Dien Christine, Sohail Noor, Masilionis Ignas, Chaligné Ronan, et al.
  "SEACells infers transcriptional and epigenomic cellular states from single-cell genomics data."
  *Nature Biotechnology* **41**(12), 1746–1757 (2023). doi:10.1038/s41587-023-01716-9
- **Verified:** CrossRef exact title match (journal version; the 2022 preprint has a different title punctuation and was rejected).
- **Insert at:** Methods §Common preprocessing, or Discussion where sparsity/SNR is discussed — Results §synthetic positive control: *"Cross-method lag disagreement is thus a property of the (low-SNR, smooth) regime that real HSPC occupies."*
- **Why:** metacell aggregation is the standard response to the low-SNR regime the draft blames for lag non-identifiability; citing it makes the SNR argument constructive and pre-empts "why not aggregate?".

---

## Summary

**Current: 26 refs. Verified candidates: 59. Projected ceiling: 85** — at the top of the Genome Biology
original-research range, so the list is intended to be **trimmed, not adopted wholesale**.

Recommended landing zone:

| Adoption | Count | Total refs | Comment |
|---|---|---|---|
| Tier A only | 24 | **50** | bottom of GB range; fixes every outright citation defect |
| Tier A + selected B | ~40 | **~66** | mid-range; recommended target |
| All candidates | 59 | **85** | top of range; likely over-cited for the paper's length |

### Distribution by area

| # | Area | Candidates | Tier A | Tier B |
|---|---|---|---|---|
| 1 | RNA velocity methodological genealogy | 14 (C1–C14) | 6 | 8 |
| 2 | Velocity critique and limitations | 3 (C15–C17) | 2 | 1 |
| 3 | Multiome / chromatin accessibility methodology | 7 (C18–C24) | 2 | 5 |
| 4 | Metabolic-labeling rate measurement | 6 (C25–C30) | 3 | 3 |
| 5 | Identifiability and sloppy-model theory | 7 (C31–C37) | 3 | 4 |
| 6 | Haematopoietic differentiation biology | 9 (C38–C46) | 4 | 5 |
| 7 | Benchmarking, statistics, reproducibility | 13 (C47–C59) | 4 | 9 |
| | **Total** | **59** | **24** | **35** |

### Outright citation defects in the current draft (fix regardless of final count)

These are places where the draft **names a source, tool or database in running text with no reference entry**.
Note this is a **housekeeping category orthogonal to the A/B literature tiers**: C57 (scrublet) and C58 (STARsolo)
are tier B as *literature*, but as *tool citations* they should be fixed regardless of how far the B list is trimmed.

| Draft text | Candidate |
|---|---|
| "Schwalb 2016 K562 TT-seq, GSE75792" (Methods + Results, twice) | **C25** |
| "GSE229305, Todorovski 2024" (Methods + Results, the external-validation axis) | **C27** |
| "scVelo dynamical model" as the RNA-only floor; "the textbook scVelo dynamical γ" | **C2** |
| "recovered from the GEX BAM by velocyto" | **C1** |
| "α is stiff, the lag is sloppy" (section title + argument) | **C31**, **C33** |
| profile-likelihood method; structural vs practical non-identifiability | **C32** |
| "permutation FDR (… FDR<0.10)" | **C51** |
| "equivalent to 0 by TOST" | **C52** |
| "Reactome neutrophil degranulation, adjusted p=9.4e-04" | **C46** |
| "scrublet applied, doublet median 0.045" | **C57** |
| "GEX via STARsolo Velocyto raw" | **C58** |
| granule markers MPO/ELANE/AZU1 + "azurophil-granule programme" | **C43** |

### Notes and cautions for whoever integrates this

1. **Do not renumber blindly.** Refs [1]–[26] are cited by number throughout the body and the figure captions.
2. **C7/C8 are two different tools named DeepVelo.** Cite both or neither; never "DeepVelo [n]" alone.
3. **C34 (Transtrum 2015) cuts both ways** — it frames the dissociation as a general phenomenon, which slightly
   tempers novelty. Recommend citing it *and* stating explicitly what is new (the lag-specific, multiome dissociation).
4. **C46 (Reactome)** — confirm the release version actually used before citing the 2022 database paper.
5. **C58 (STARsolo)** is preprint-only as far as CrossRef shows. The alternative (STAR, Dobin 2013) was **not**
   verified in this pass and must be CrossRef-checked before being substituted.
6. **Author lists are truncated at 6 + "et al."** by the verification script. The DOI is the durable anchor;
   any entry showing "et al." must have its full author list re-pulled at bibliography-assembly time, since
   Genome Biology has its own author-listing rules.
7. **Not verified, therefore not listed:** a source publication for GSE194122 (the BMMC NeurIPS benchmark dataset)
   and for the 10x "Fresh Embryonic E18 Mouse Brain 5k" demo. Neither resolved to a citable CrossRef record here;
   they remain accession-only citations unless someone verifies a source independently.
