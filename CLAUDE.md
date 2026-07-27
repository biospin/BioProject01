# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

BioProject01 is a scientific paper analysis system for computational biology research, particularly multi-omic single-cell papers. It uses agent-based skill routing to decompose papers into structured Korean-language markdown analyses stored under `analysis/<topic>/<paper-title>/`.

There is no build system, no test suite, and no package manifest — this is a workflow-driven agent system, not a software package.

## Skill Routing

`AGENTS.md` is the authoritative router. Skills are organized by **analysis task**, not by paper section.

| Agent | Skill | When |
|---|---|---|
| Figure 1 Decode | `skills/fig1-decode/SKILL.md` | Always first, at the start of any paper analysis |
| Claim Extract | `skills/claim-extract/SKILL.md` | After fig1-decode |
| Quality Gate | `skills/quality-gate/SKILL.md` | After claim-extract, before any deep reading |
| Results Scan | `skills/results-scan/SKILL.md` | Only if quality-gate verdict is "보통" or better |
| Apply Map | `skills/apply-map/SKILL.md` | After results-scan |
| Takeaway | `skills/takeaway/SKILL.md` | After results-scan |
| Method Reference | `skills/method-ref/SKILL.md` | On-demand, when a method needs explaining |
| Paper Scrapper | `skills/paper-scrapper/SKILL.md` | 2+ papers, when cross-paper comparison material is needed |
| Insight Agent | `skills/insight-agent/SKILL.md` | After paper-scrapper |
| Paper Network | `skills/paper-network/SKILL.md` | Only when 2+ papers are analyzed |
| Paper QA | `skills/paper-qa/SKILL.md` | Questions about an already-analyzed paper |
| Claim Verify | `skills/claim-verify/SKILL.md` | When an insight's evidence needs verifying |
| Paper Digest | `skills/paper-digest/SKILL.md` | When a 1-page summary in the paper's own order is requested |
| Slide Deck | `skills/slide-deck/SKILL.md` | Only when the user explicitly requests slides |

Each skill directory contains a `SKILL.md` (full specification) and `agents/openai.yaml` (agent interface config). Always read the relevant `SKILL.md` before executing a skill.

`skills/_archive/` holds the retired section-based skills (`full-background`, `full-overview`, `full-methods`, `full-results`, `full-discussion`, `full-slides`, `abstract-analysis`, `insight-validation`, `question`). Do not route to them.

`skills/full-figure/` is not a routed agent and has no `SKILL.md` or `agents/` config. It is kept only as the home of the panel extraction script (see below), which `results-scan` calls directly; `skills/full-figure/README.md` holds the figure-interpretation principles `results-scan` refers to. Do not add it to the routing table.

## Single-Paper Workflow

1. Determine the topic and prepare `analysis/<topic>/`.
2. **fig1-decode** — grasp the core approach via Figure 1; fall back to Introduction + Discussion arc if Figure 1 is uninformative.
3. **claim-extract** — pull core claims and the gap from Abstract / Introduction.
4. **quality-gate** — assess journal tier, author institutions, evidence quality, paper mill risk.
   - Verdict "읽지 않음 권고" → stop the analysis here and tell the user.
   - Verdict "낮음" → tell the user and confirm whether to continue.
5. **results-scan** — organize datasets, numeric results, and Figure evidence.
6. **apply-map** — assess how the paper applies to the user's own research.
7. **takeaway** — capture open questions and next directions.
8. **method-ref** — run at the point where results-scan or apply-map needs a method explained.
9. Save to `analysis/<topic>/<paper-title>/full.md`.

## Multi-Paper Workflow

1. Run the single-paper workflow for each paper.
2. **paper-scrapper** — structure each `full.md` into `scope.md` / `papers.jsonl` / `comparison_table.md` / `evidence_bundle.md`.
3. **insight-agent** — produce cross-paper insights in four sections: Field Flow, Differentiation Map, Repeated Limitations, Unresolved Gaps.
4. **paper-network** — analyze author overlap, institutional clusters, corporate ties, research lineage.

Cross-paper output goes to `analysis/<topic>/_evidence/week2/`. This path is negated in `.gitignore` so it stays tracked while per-paper `full.md` remains ignored.

## Output Conventions

- Input PDFs go in `papers/` (gitignored).
- Output goes in `analysis/<topic>/<paper-title>/full.md` (gitignored).
- Topic folder: kebab-case of user-provided topic (e.g., `epigenomic lag` → `epigenomic-lag`).
- Paper folder: exact paper title, or PDF filename if title cannot be reliably extracted.
- If the topic is not stated, infer it from conversation context; ask briefly only if inference is impossible.
- `full.md` is mandatory per paper. Optional, produced only on request: `digest.md` (paper-digest), `slides/` (slide-deck), `figures/` (extracted panels).

## Language Rules

- Default output language: **Korean**.
- `AGENTS.md` holds the canonical list of scientific terms to keep in English. Individual skills defer to that list.
- Broadly: biology/genomics (`RNA`, `DNA`, `TF`, `SNP`, `chromatin`, `single-cell`, `multi-omics`, `RNA velocity`, `ATAC-seq`, `pseudotime`), data/experiment (`baseline`, `dataset`, `benchmark`, `metric`, `Figure`, `panel`, `ablation`, `control`), and stats/ML (`likelihood`, `prior`, `posterior`, `latent variable`, `ODE`, `loss function`, `regularization`, `variational inference`, `Bayesian`) terms stay in English.
- For non-standard English terms, add a short Korean explanation on first use.
- Do not write full English sentences in output.

## Figure Panel Extraction Script

The only executable in this repo is `skills/full-figure/scripts/extract_panels.py`. It extracts figure panels from PDFs.

**Dependencies:** `pip install pymupdf pillow`

```bash
# Basic usage
python3 skills/full-figure/scripts/extract_panels.py papers/paper.pdf \
  --page 5 --figure Figure2 --figure-bbox 72,120,540,650 \
  --out analysis/<topic>/<paper-title>/figures

# For complex layouts, pass explicit panel coordinates as JSON
python3 skills/full-figure/scripts/extract_panels.py papers/paper.pdf \
  --spec figure2-panels.json --out analysis/<topic>/<paper-title>/figures
```

Outputs: `figure_N_panel_01_a.png`, `*_manifest.json`, `*_debug.png`.

## Slides Workflow

Only generate slides when the user explicitly requests them ("슬라이드", "발표자료", "slides", "presentation"). Slides are never auto-generated during paper analysis.

- Use `skills/slide-deck/SKILL.md` + `design.md` (visual design spec).
- Requires `analysis/<topic>/<paper-title>/full.md` to exist first; do not invent slide content without it.
- Depends on the external `openclaw-slides` skill at `/Users/jamie/.openclaw/workspace/skills/openclaw-slides/SKILL.md`. If absent, install it with `openclaw skills install openclaw-slides` before proceeding.
- Capture figure images from the source PDF with `mutool draw` (not `extract_panels.py`) into `slides/assets/figures/`, named `figure-1.png` / `figure-2a-c.png`; keep each image ≤ half the slide area.
- Output: `slides/index.html` (single-page, opens directly from the filesystem without a server) and `slides/speaker-notes.md`.
- Do not render video unless explicitly requested.

## Architecture Notes

- `AGENTS.md` is the router — it defines workflows and routing tables, but all substantive rules live in the individual `SKILL.md` files. When the two disagree, `AGENTS.md` wins and this file should be updated to match.
- `design.md` is a visual design system spec (Lovable-inspired: warm cream backgrounds, Campora Plain typography) used exclusively by `slide-deck`.
- `analysis/` and `papers/` are both gitignored. Committed content is only workflow definitions and skill specs.
