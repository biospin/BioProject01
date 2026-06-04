# Evidence Bundle

This file is the direct handoff to the Insight Agent. Keep it compact, factual, and citation-oriented.

## Project Frame
- Goal: estimate gene-specific `activation lag` and `shutdown lag`
- Step 1: quantify lag from multiome or time-resolved chromatin/RNA data
- Step 2: predict lag from baseline epigenomic features
- Step 3: test whether lag predicts perturbation or drug response timing

## Evidence Block Template

### [Paper ID]
- Full citation:
- Data modality:
- Main biological system:
- Timing concept:
- What the authors claim:
- What evidence they provide:
- What this paper enables for our project:
- What it still does not solve:
- Key limitation:
- Quote-ready figure / table / method anchors:

## Cross-Paper Questions
1. Which papers estimate lag directly, and which only imply it?
2. Which methods operate at gene level, cell level, or trajectory level?
3. Which assumptions block translation from pseudotime lag to wall-clock response timing?
4. Which features appear most plausible for Step 2 prediction?
5. What is still missing for Step 3 validation?

## Seed Evidence

### MultiVelo
- Full citation: Li et al., Nature Biotechnology, 2023.
- Data modality: paired chromatin accessibility + unspliced/spliced RNA.
- Main biological system: embryonic mouse brain, mouse skin, human HSPC, human fetal brain.
- Timing concept: priming interval, decoupling interval, Model 1 vs Model 2.
- What the authors claim: joint chromatin-RNA dynamics improves cell-fate prediction and reveals two regulatory orderings.
- What evidence they provide: ODE-based fits, improved trajectory consistency, cross-dataset gene regime patterns.
- What this paper enables for our project: a direct conceptual precursor for activation lag and shutdown lag.
- What it still does not solve: continuous gene-specific lag with uncertainty and real-time calibration.
- Key limitation: timing remains in latent units and response-time validation is absent.
- Quote-ready figure / table / method anchors: see local analysis `BioProject01/analysis/multivelo-analysis.ref.md`.

### MultiVeloVAE
- Full citation: Li et al., Nature Communications, 2025.
- Data modality: paired chromatin accessibility + unspliced/spliced RNA.
- Main biological system: multi-sample lineage-resolved multiome systems including HSPC.
- Timing concept: continuous cell-specific coupling and decoupling factors.
- What the authors claim: cell-specific and sample-aware dynamics recover lineage-specific regulatory differences better than discrete gene-only framing.
- What evidence they provide: posterior-based inference, differential dynamics testing, continuous decoupling analysis.
- What this paper enables for our project: a better bridge from discrete regime labels to continuous lag-like variables.
- What it still does not solve: explicit activation/shutdown lag variables linked to perturbation timing.
- Key limitation: richer model, but still indirect for Step 3.
- Quote-ready figure / table / method anchors: official article sections on decoupling factor and cell-specific rates.

### MoFlow
- Full citation: Nature Communications, 2025.
- Data modality: paired chromatin accessibility + RNA.
- Main biological system: SHARE-seq mouse skin and E18 mouse brain.
- Timing concept: signed chromatin-to-spliced RNA lag interpreted directly.
- What the authors claim: relay velocity modeling captures interpretable dynamic chromatin-transcription regulation beyond fixed latent-time assumptions.
- What evidence they provide: lineage trajectory recovery, lag sign interpretation, comparison against prior velocity methods.
- What this paper enables for our project: the closest existing method to direct gene-specific lag estimation.
- What it still does not solve: pathway-level coordination and perturbation-time validation.
- Key limitation: missing long-range regulatory context and memory effects.
- Quote-ready figure / table / method anchors: official article sections on positive/negative lag and method limitations.

## Minimum Evidence Standard
- Every claim in `insight.md` should map back to a concrete paper and evidence block.
- Avoid claims that are supported by only vague discussion text.
- Mark uncertain interpretations explicitly as `Inference`.
