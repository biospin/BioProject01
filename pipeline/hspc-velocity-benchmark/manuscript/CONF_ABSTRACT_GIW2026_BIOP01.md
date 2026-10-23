# BIOINFO/GIW ISCB-Asia 2026 — BIOP01 초록 (v2, 2026-10-23)

> v2: ML4H Submission 294 반박문(10/13) 정정 반영(BIOP01-90). v1(8/15 Oxford Abstracts 제출본)은 94aa054.
> 바꾼 것: lag 정의별 값(priming +0.364, coupled-on +0.163, 같은 공식 −0.009), ATAC 셔플 "causal·model-structural" 삭제 후
> "세포 수준 짝을 깨도 보존"으로 축소, 부호 54.6%를 "at chance" 대신 "near 50%", α는 발현량 넘는 재현(+0.715)은 있으나
> kinetic 정확도 미확인, 사전등록은 한 시스템뿐임을 명시, routing을 "발현량 먼저, α는 그 위에만"으로 변경.
> 수치는 모두 v2 long abstract(CONF_LONGABSTRACT_GIW2026_BIOP01.md)와 같은 출처다.
> ⚠️ 채택 초록은 Briefings in Bioinformatics supplement에 실린다. 카메라레디에서 초록 교체가 허용되는지 주최측 안내를 확인한 뒤 Oxford Abstracts에 반영한다.

> 학회: BIOINFO 2026 / GIW XXXV / ISCB-Asia (2026-11-17~20, 연세대). 초록 마감 2026-08-15.
> 제출: 200단어 초록(블라인드 — 소속·직위 금지) + (구두 희망 시) 최대 2p long abstract.
> 신청: (ii) talk and poster 권장(구두 탈락 시 자동 포스터). Oxford Abstract 시스템.
> 트랙 적합: General Computational Biology / Multi-omics Integration and Foundation Models.
> 근거: manuscript/draft_v2.md(GB 원고). 수치는 draft_v2·results 실측(지어낸 값 없음).
> ⚠️ 블라인드라 저자·소속 미기재. 최종 제출 전 kkkim 검토 + 팀 확정(BIOP01-86).

## Title
A reliability map for per-gene multiome RNA velocity parameters in single-cell kinetics

## Abstract (~200 words, blind)

Multiome RNA-velocity methods emit several per-gene quantities, a transcription rate α, a
degradation rate γ and a chromatin-to-transcription lag, each offered as a readout. A
derived quantity is usable only if it is reliable: reproducible across algorithms and consistent
with independent measurement. Across up to five velocity arms (an RNA-only scVelo floor plus
MultiVelo, MultiVeloVAE, MoFlow and CRAK-Velo) on human hematopoietic stem and progenitor cells,
we tested each output on four axes: cross-method reproducibility, a within-lineage
ATAC shuffle, replication in five external multiomes, and anchoring to measured
rates. Only α reproduced across methods (Spearman ρ=0.88). The lag did not reproduce
under any definition (MultiVelo priming +0.364, coupled-on duration +0.163, one
identical formula −0.009), sign agreement stayed near 50% (54.6%), and it largely survived
destroying cell-level chromatin–RNA pairing. γ was fragile (ρ≈−0.1) and ran reversed
against measured half-life (−0.224). α stayed reproducible beyond abundance (partial ρ=+0.715), but
abundance tracked measured synthesis at least as strongly (+0.410 versus +0.262), so α's kinetic
accuracy is not established. The α-over-lag ordering held in all six systems; the one
preregistered system passed six-of-six sealed predictions. Enter abundance first and add α
only beyond it; do not use lag, sign, timing or γ without orthogonal validation.

<!-- (v1 메모) 199단어(≤200 CFP 상한). 이건규 critic(BIOP01-87) 🔴A abundance confound·🔴B 사전등록 범위·
🟡C 단어수·🟡D γ 역방향·🟡E lag 수치 전부 반영. 수치는 draft_v2·results 실측(이건규 line-by-line 대조).
long abstract(2p)에서 필수 분리: (1) per-gene lag층 ATAC-shuffle vs velocity-matrix층 철회(draft L117)를
층 구분, (2) "Only α" 범위=per-gene(집단수준 robust 2종은 별도), (3) 그림=Fig1(lag vs α) + Fig4(외부앵커+
abundance 대조 막대) 우선, Fig7(지도)은 마지막. -->
