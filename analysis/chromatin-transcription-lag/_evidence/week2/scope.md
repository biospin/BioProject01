# Scope

## Topic
Cross-paper insight extraction for gene-specific chromatin-transcription lag modeling.

## Research Question
How do recent multi-omic dynamics papers define, estimate, and interpret gene-specific timing gaps between chromatin accessibility change and transcriptional change, and what unresolved gaps remain before those signals can support perturbation or drug response timing prediction?

## Keywords
- chromatin transcription lag
- multiome dynamics
- RNA velocity
- chromatin accessibility timing
- MultiVelo
- MultiVeloVAE
- MoFlow
- gene-specific lag
- priming interval
- decoupling interval

## Include Criteria
- Primary research paper, method paper, or benchmark paper
- Uses paired or aligned chromatin and RNA signals, or explicitly models timing between them
- Contains a method, metric, or interpretation directly relevant to activation lag or shutdown lag
- Includes enough methodological detail to compare data modality, model assumptions, outputs, and limitations

## Exclude Criteria
- Pure single-modality RNA-only or ATAC-only paper with no timing bridge to the other modality
- Review article without new method or empirical result
- Paper focused only on visualization or embedding without interpretable timing output
- Paper whose full text cannot be accessed well enough to extract evidence

## Initial Paper Set
1. MultiVelo
2. MultiVeloVAE
3. MoFlow

## Expected Output
- `papers.jsonl`: structured paper records for cross-paper comparison
- `comparison_table.md`: side-by-side comparison of method, assay, dataset, result, limitation
- `evidence_bundle.md`: curated evidence blocks for the Insight Agent
- `insight.md`: cross-paper insight report with required four sections

## Insight Rules
- Do not restate each paper independently unless needed as evidence.
- Every insight must connect at least two papers, or connect one paper to the project's 3-step framework.
- Distinguish `authors' claim` from `our interpretation`.
- Prefer unresolved methodological gaps over generic praise.
