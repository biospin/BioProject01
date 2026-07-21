# P3 — Confound 분석 (cell cycle / burst / ambient)

multivelo lag gene 수: 538
scVelo floor gene 수: 730

## (a) Cell Cycle
- S marker 42/43, G2M marker 52/54 found
- phase 분포: {'G1': 11674, 'G2M': 5191, 'S': 5013}
- lag gene 중 S marker 비율: 0.006 vs 전체 0.001
- lag gene 중 G2M marker 비율: 0.013 vs 전체 0.001
- → 비율 차이 작을수록 cell cycle 편향 낮음
- Spearman(S_score, lag-gene mean spliced expr) = 0.326 (p=0)
- Spearman(G2M_score, lag-gene mean spliced expr) = 0.356 (p=0)
- → |ρ|>0.3 이면 cell cycle confound 의심 → 회귀 통제 검토 필요

## (b) Burst parameter 공선성 (α ~ lag)
- n=538 shared gene
- Spearman(MultiVelo lag, fit_alpha) = -0.242 (p=1.3e-08)
- → |ρ|>0.5 = lag↔α 강공선 → regularized 회귀 필요(DESIGN §5.6)

## (c) Ambient / Doublet (QC 요약)
- doublet_score n=21878, median 0.045, 99th pct 0.268
- P1에서 scrublet 적용(predicted_doublet 제거). 잔여 고점수 세포 비율 낮음.
- pct_mito: median 10.4%, 99th 19.3% (QC max 20.0%)
