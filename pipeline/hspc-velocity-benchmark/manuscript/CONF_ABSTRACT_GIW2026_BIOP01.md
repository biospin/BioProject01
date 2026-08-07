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

Multiome RNA-velocity methods emit several per-gene quantities — a transcription rate α, a
degradation rate γ, and a chromatin-to-transcription lag — each proposed as a biological
readout. A derived quantity is usable only if it is reliable: reproducible across algorithms
and consistent with independent measurement. Across up to five velocity arms (an RNA-only
scVelo floor plus MultiVelo, MultiVeloVAE, MoFlow and CRAK-Velo) on human hematopoietic stem
and progenitor cells (10x Multiome), we tested each output on four axes: cross-method
reproducibility, a causal within-lineage ATAC-shuffle control, replication in five external
multiomes, and anchoring to measured synthesis and degradation rates. Only α reproduced across
methods (Spearman ρ=0.88); the lag reproduced weakly in magnitude (strongest pair +0.163), only
at chance in sign (54.6%), and was unchanged by ATAC shuffling, marking it model-structural. γ
was fragile (ρ≈−0.1) and ran reversed against measured half-life (−0.224). Fitted α tracked
measured synthesis (+0.24 to +0.29), but transcript abundance tracked it at least as strongly
(+0.410 versus +0.262) — consistency evidence, not α-specific accuracy. The α-over-lag ordering
held in all six systems; the sixth was preregistered and passed six-of-six, sealed before
fitting. Trust α against an abundance baseline; treat lag, sign, timing and γ as requiring
orthogonal validation.

<!-- 199단어(≤200 CFP 상한). 이건규 critic(BIOP01-87) 🔴A abundance confound·🔴B 사전등록 범위·
🟡C 단어수·🟡D γ 역방향·🟡E lag 수치 전부 반영. 수치는 draft_v2·results 실측(이건규 line-by-line 대조).
long abstract(2p)에서 필수 분리: (1) per-gene lag층 ATAC-shuffle vs velocity-matrix층 철회(draft L117)를
층 구분, (2) "Only α" 범위=per-gene(집단수준 robust 2종은 별도), (3) 그림=Fig1(lag vs α) + Fig4(외부앵커+
abundance 대조 막대) 우선, Fig7(지도)은 마지막. -->
