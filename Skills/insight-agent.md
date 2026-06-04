# Insight Agent Skill

## Purpose
This skill turns paper-level evidence into cross-paper insight. It should read `papers.jsonl`, `comparison_table.md`, and `evidence_bundle.md`, then generate `insight.md` focused on field structure, repeated patterns, and unresolved gaps.

## When to use
Use this skill when the user wants:
- cross-paper insight instead of single-paper summary
- a synthesis of methods, assays, strengths, and limitations
- project-oriented interpretation for chromatin-transcription lag research

## Inputs
- `analysis/<topic>/_evidence/week2/papers.jsonl`
- `analysis/<topic>/_evidence/week2/comparison_table.md`
- `analysis/<topic>/_evidence/week2/evidence_bundle.md`
- Optional: per-paper analysis files produced by `Skills/paper-analysis.md`

## Core distinction
- `Summary`: what each paper says on its own
- `Insight`: what becomes visible only after comparing papers, assumptions, outputs, and blind spots

## Required output sections
Generate `insight.md` with exactly these sections:
1. `Field Flow`
2. `Differentiation Map`
3. `Repeated Limitations`
4. `Unresolved Gaps`

Each section must include:
- at least one cross-paper statement
- at least one concrete evidence anchor
- one short `Project implication` line

## Analysis rules
1. Prefer comparison over narration.
2. Separate `authors' claim` from `inference`.
3. Call out when two papers use the same dataset but support different conclusions.
4. Distinguish pseudotime ordering from real-time kinetics.
5. Highlight what is sufficient for Step 1, suggestive for Step 2, and still missing for Step 3.

## Output style
- Dense and specific
- No generic praise
- No bullet list of isolated paper summaries unless used as evidence
- Name limitations in operational terms: uncertainty, confounding, missing validation, weak transferability, missing perturbation evidence

## Recommended prompt
Use the following instruction pattern:

```text
Read `papers.jsonl`, `comparison_table.md`, and `evidence_bundle.md`.
Write `insight.md` with the four required sections only:
Field Flow, Differentiation Map, Repeated Limitations, Unresolved Gaps.

Do not summarize papers independently unless needed as evidence.
Focus on cross-paper patterns relevant to activation lag, shutdown lag, and response-time prediction.
Mark any unsupported leap as Inference.
End each section with `Project implication: ...`
```
