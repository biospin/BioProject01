# BIOINFO/GIW ISCB-Asia 2026 — BIOP01 초록 초안

> 학회: BIOINFO 2026 / GIW XXXV / ISCB-Asia (2026-11-17~20, 연세대). 초록 마감 2026-08-15.
> 제출: 200단어 초록(블라인드 — 소속·직위 금지) + (구두 희망 시) 최대 2p long abstract.
> 신청: (ii) talk and poster 권장(구두 탈락 시 자동 포스터). Oxford Abstract 시스템.
> 트랙 적합: General Computational Biology / Multi-omics Integration and Foundation Models.
> 근거: manuscript/draft_v2.md(GB 원고). 수치는 draft_v2·results 실측(지어낸 값 없음).
> ⚠️ 블라인드라 저자·소속 미기재. 최종 제출 전 kkkim 검토 + 팀 확정(BIOP01-86).

## Title
A reliability map for per-gene multiome RNA velocity parameters in single-cell kinetics

## Abstract (~200 words, blind)

Chromatin-informed ("multiome") RNA-velocity methods emit several per-gene quantities — a
transcription rate α, a degradation rate γ, and a chromatin-to-transcription lag — each
proposed as a biological readout. A derived quantity is usable only if it is reliable:
reproducible across reasonable algorithms and, where possible, consistent with an independent
measurement. Across up to five velocity arms (an RNA-only scVelo floor plus MultiVelo,
MultiVeloVAE, MoFlow and CRAK-Velo) on human hematopoietic stem and progenitor cells profiled
by 10x Multiome, we tested each output on four axes: cross-method reproducibility
(permutation-FDR), a causal within-lineage ATAC-shuffle control, cross-dataset replication in
five external multiomes (one preregistered), and external anchoring to measured synthesis
(K562 TT-seq) and degradation rates. Only the transcription rate α reproduced across methods
(Spearman ρ=0.88); the lag and γ did not — the lag reproduced weakly in magnitude and only at
chance in sign, and shuffling ATAC left it unchanged, marking it model-structural rather than
chromatin-driven. The α-over-lag ordering held in all six systems and passed a preregistered
six-of-six scorecard sealed before any fit. We distil these results into a velocity-output
reliability map with a concrete routing rule: trust α and rate-derived signals; treat the lag,
its sign, absolute timing, and γ as requiring orthogonal validation.

<!-- 단어 수 목표 ~200. 초과 시 마지막 문장부터 압축. long abstract(2p)는 draft_v2 Results·Fig1/Fig7에서 파생. -->
