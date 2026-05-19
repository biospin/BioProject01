# Paper Analysis Skill

## Purpose
This skill guides an analysis agent to read a biomedical research paper systematically and produce a reproducible, structured review. The goal is not a casual summary, but a disciplined analysis that remains usable after `/compact`, `/clear`, or `/reset`.

## When to use
Use this skill when the user asks to analyze, review, summarize, critique, compare, or extract insights from a scientific paper, especially in bioinformatics, genomics, epigenomics, multi-omics, computational biology, RNA velocity, chromatin dynamics, or single-cell trajectory analysis.

## Core principles
1. Ground every claim in the paper.
2. Separate what the paper states from your interpretation.
3. Prefer precision over flashy wording.
4. Identify assumptions, limitations, and missing information explicitly.
5. For computational or biomedical papers, pay close attention to data, model design, evaluation, and biological interpretation.

## Required inputs
- Paper PDF, DOI, PMID, arXiv link, journal URL, or local file path
- Optional user context:
  - why this paper matters
  - target audience level
  - whether the user wants a short summary or a deep critique
  - whether comparison to another paper is needed

## Reading workflow
Follow this order unless the user asks otherwise.

### Step 1. Paper identification
Extract and report:
- Title
- Authors
- Year
- Journal / venue
- DOI / URL if available
- Paper type: method / benchmark / review / dataset / clinical / mechanistic / other

### Step 2. Executive overview
Write one compact paragraph covering:
- What problem the paper addresses
- Why the problem matters
- What the authors claim is new
- What the main result is

### Step 3. Research question and motivation
Identify:
- Primary research question
- Secondary questions if any
- Biological or clinical motivation
- Why prior approaches were insufficient

If the motivation is vague, overstated, or weakly justified, say so clearly.

**Project connection**: Evaluate how the paper relates to gene-specific **activation lag** (chromatin opening → transcription onset) and **shutdown lag** (transcription shutdown → chromatin closing). State whether the paper contributes methods, data, or ideas relevant to predicting chromatin-transcription timing.

### Step 4. Methodology
Describe the study design in a structured way.

For computational papers, extract:
- Input data types
- Preprocessing steps
- Features used
- Model architecture or algorithm
- Training strategy
- Baselines
- Hyperparameter or implementation details if available

For experimental papers, extract:
- Sample source
- Experimental design
- Controls
- Assays / platforms
- Replicates
- Inclusion / exclusion logic if stated

If key details are missing and this limits reproducibility, flag that explicitly.

### Step 5. Dataset and experimental setup
Report:
- Dataset name(s)
- Species / tissue / condition
- Sample size or cell number
- Modality (e.g. RNA-seq, ATAC-seq, multiome, imaging)
- Train/validation/test split if applicable
- External validation datasets if any

Also check:
- Is the dataset size adequate for the claims?
- Is there a risk of data leakage?
- Are comparison groups fair?

### Step 6. Key results
Summarize the main results in order of importance.

For each key result, include:
- What was tested
- **Authors' claim**
- **Evidence presented** (metric, figure, table, experiment, or analysis)
- **My assessment**
- Strength of support: **Strong** / **Moderate** / **Weak** / **Unsupported**
- Caveats or alternative explanations

Do not just restate the conclusion. Separate the authors' claim, the evidence they provide, and your evaluation of how convincing that evidence is.

### Step 7. Biological or domain interpretation
For biomedical papers, explain:
- What the results mean biologically
- Whether the interpretation is based on direct evidence or indirect inference
- Whether conclusions are mechanistic, predictive, associative, or speculative

If the paper blurs correlation and causation, point that out.

### Step 8. Strengths
List concrete strengths such as:
- Strong study design
- Clear novelty
- Good validation strategy
- Useful benchmark comparisons
- High-quality multimodal integration
- Practical reproducibility

Avoid vague praise.

### Step 9. Limitations and risks
List concrete limitations such as:
- Small sample size
- Missing controls
- Weak baseline comparisons
- Overfitting risk
- Batch effect or confounding risk
- Lack of external validation
- Biological over-interpretation
- Incomplete reproducibility details

If a limitation materially affects confidence, explain how.

### Step 10. Comparison to prior work
When possible, compare the paper to prior methods or concepts mentioned in the paper.
Focus on:
- What is genuinely new
- What is incremental
- What trade-offs exist
- Whether the claimed novelty seems justified

If the paper cites tools relevant to epigenomics or multi-omics (e.g. MultiVelo, MultiVeloVAE, MoFlow), explain the distinction carefully.

**Project connection**: Assess whether the paper's approach could be used or adapted to estimate gene-specific activation lag / shutdown lag, or to predict epigenetic drug response timing. Identify any concepts, datasets, or methods that map to the project's 3-step framework: lag quantification → baseline feature prediction → perturbation validation.

### Step 11. Reproducibility assessment
Assess whether a skilled reader could reproduce the work.
Check for:
- Data availability
- Code availability
- Parameter details
- Software / package versions
- Random seed or training details
- Statistical test details
- Figure-to-method consistency

Rate reproducibility as one of:
- High
- Moderate
- Low

Explain the rating briefly.

### Step 12. Final verdict
End with four short sections:
- **Take-home message**
- **What I would trust**
- **What I would verify independently**
- **Who this paper is useful for**

### Step 13. Project utility assessment
Assess how useful this paper is for the current project using one of the following labels:
- **Directly usable**
- **Adaptable with modification**
- **Conceptually informative only**
- **Not useful for this project**

Explain:
- which part of the paper is useful
- how it maps to the project's 3-step framework (lag quantification → baseline feature prediction → perturbation validation)
- what still needs to be added, adapted, or validated before use

## Output format
Unless the user asks otherwise, use this structure exactly:

1. Paper Info
2. Executive Overview (3-5 sentences)
3. Research Question & Motivation (1-2 paragraphs)
4. Methods (1-2 paragraphs)
5. Dataset & Experimental Setup (1 paragraph + table if multiple datasets)
6. Key Results (2-4 sentences per key result)
7. Biological / Practical Interpretation (1-2 paragraphs)
8. Strengths (3-5 bullet points)
9. Limitations (3-5 bullet points)
10. Comparison to Prior Work (1-2 paragraphs)
11. Reproducibility Assessment (checklist + rating)
12. Final Verdict (4 short sections, 1-3 sentences each)
13. Project Utility Assessment (label + short justification)

## Output file
Save the analysis result as `analysis/<paper-short-name>-analysis.md` in the repository. Use a lowercase, hyphenated short name derived from the paper title or method name (e.g. `analysis/multivelo-analysis.md`).

## Domain-specific checks for bioinformatics / epigenomics papers
When relevant, explicitly inspect the following:
- Is the prediction target clearly defined?
- Are covariates or confounders handled? (batch, cell cycle, sequencing depth, donor effects)
- Is pseudotime being over-interpreted as real time?
- Does the paper quantify gene-specific lag explicitly, or only imply temporal ordering qualitatively?
- Does it show the ordering between chromatin change and transcription change directly, or only infer it indirectly?
- Does it use paired multiome data, or indirect cross-modality integration?
- Is there perturbation, time-course, or external validation supporting temporal claims?
- Does it capture gene-level heterogeneity, or mainly report global trends?
- Are multimodal signals aligned fairly across modalities?
- Are baseline methods appropriate and competitive?
- Are evaluation metrics suitable for the biological question?
- Are uncertainty and variance reported?
- Are claims about mechanism actually supported by the data?
- Are gene-level or peak-level multiple testing corrections described?
- Is the biological validation independent from the training signal?

## Behavior rules
- If the full paper is not accessible (e.g. paywall, broken link), attempt to retrieve information via WebFetch or WebSearch using the DOI, title, or PMID.
- If only partial information is available after fallback, clearly state which sections could not be assessed.
- If only the abstract is available, do not pretend to have reviewed the full methods or results.
- If figures or tables are referenced but not available, say so.
- If the user wants a shorter answer, keep the same logical structure in compressed form.
- If the paper is weak, say so directly but fairly.

## Optional add-ons
If the user requests, also provide one or more of these:
- Figure-by-figure interpretation
- Reviewer-style critique
- Journal club presentation notes
- Comparison table versus another paper
- Follow-up experiment suggestions
- Plain-language summary for non-experts

## Example invocation
- `/paper-analysis` <paper path or URL>
- Analyze this paper using my `paper-analysis` skill: <paper path or URL>
- Review this paper critically with the `paper-analysis` skill and focus on reproducibility.
- Compare these two papers using the `paper-analysis` skill.
