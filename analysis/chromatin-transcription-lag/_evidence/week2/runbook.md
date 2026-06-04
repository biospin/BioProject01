# Week2 Runbook

## Goal
Build the evidence inputs needed for `BIOP01-21` and then generate `insight.md`.

## Step 1. Confirm paper set
Start with these three papers:
1. MultiVelo
2. MultiVeloVAE
3. MoFlow

If one paper is inaccessible, replace it only with a paper that still models chromatin-RNA timing directly.

## Step 2. Run per-paper analysis
Use `Skills/paper-analysis.md` for each paper.

Recommended prompt:

```text
Read this paper and analyze it using `Skills/paper-analysis.md`.
Save the result under `analysis/` with a clear paper-specific filename.
Focus especially on:
- how the paper defines timing between chromatin and transcription
- whether it estimates gene-specific activation lag or shutdown lag
- what assumptions it makes about pseudotime, latent time, or trajectory ordering
- what parts are useful for Step 1, Step 2, and Step 3 of this project
```

## Step 3. Fill `papers.jsonl`
For each paper, update:
- `year`
- `venue`
- `doi_or_url`
- `data_modalities`
- `datasets`
- `method_summary`
- `assay_summary`
- `main_results`
- `limitations`
- `project_relevance`

## Step 4. Fill `comparison_table.md`
Reduce each paper to directly comparable rows:
- assay and dataset
- timing concept
- algorithmic core
- strongest contribution
- most important limitation
- mapping to project Step 1, 2, 3

## Step 5. Fill `evidence_bundle.md`
Convert the paper analyses into short evidence blocks.
Keep only evidence that can support cross-paper claims.

## Step 6. Generate `insight.md`
Use `Skills/insight-agent.md`.

Recommended prompt:

```text
Use `Skills/insight-agent.md`.
Read:
- `analysis/chromatin-transcription-lag/_evidence/week2/papers.jsonl`
- `analysis/chromatin-transcription-lag/_evidence/week2/comparison_table.md`
- `analysis/chromatin-transcription-lag/_evidence/week2/evidence_bundle.md`

Write `analysis/chromatin-transcription-lag/_evidence/week2/insight.md`.
Only use the four required sections:
- Field Flow
- Differentiation Map
- Repeated Limitations
- Unresolved Gaps
```

## Minimum completion standard
- `papers.jsonl` contains three usable records
- `comparison_table.md` is fully populated
- `evidence_bundle.md` contains one evidence block per paper
- `insight.md` contains the required four sections and project implications
