# 설계 adversarial 검토 — research-methodologist (2026-06-13)

> 대상: `DESIGN.md` v1. 판정: **REVISE — 그대로 실행 금지.**
> 우리 repo 교차검증(`analysis/epigenomic-lag/li-2023-multivelo_core.md` L194, L422, L387):
> - cell 수 **11,605** 확정 (1,000 genes joint-filtered, 936 variable fit, 11 Leiden cluster). 검토자의 "~2,000"은 오류.
> - **day0+day7 Seurat 통합** 확정 → H2 confound 지적 유효.
> - 원논문이 **cell cycle regress-out**, **single donor in vitro day7 배양** → composition shift 실재.

## BLOCKER
1. **H1 success criterion 순환** — method 행동으로 gene을 고르고(둘 다 high-confidence) 그 set의 known-marker enrichment를 whole-genome 대비 검정 = 순환. velocity는 원래 dynamic·high-variance gene(=marker)에 반응. 틀린 lag로 agree해도 통과. → enrichment를 *dynamic-gene background*로, 1차 기준은 **bootstrap lag-sign stability**(agreement gene이 더 재현적)로.
2. **H2 wall-clock anchor 비유효** — (a) day0/day7은 batch 제거 목적 통합 → day label이 batch와 aliased, (b) 2 timepoint = 1 interval(보정곡선 불가, 방향만), (c) day0→day7은 *cell-type composition shift*(분화)이지 within-cell clock 전진이 아님 → within-cell lag 검증에 category error. → H2를 "confounded directional sanity check"로 강등, method 선정 결정에서 배제, permuted-day-label control 추가, **wall-clock 단위 lag는 이 데이터로 불가**임을 명시.
3. **lag ground truth 부재** — labeling·time-course·perturbation·simulator 전무. §4B의 모든 lag metric은 *cross-method consistency*이지 accuracy 아님. → §0/§6를 reproducibility/stability/consistency로 reframe + **injected-lag chromatin-aware simulator**(BEELINE/SERGIO fork)를 유일 accuracy arm(secondary)으로 추가.
4. **RNA-only baseline + scrambled-chromatin ablation을 REQUIRED로** — 프로젝트 명제="chromatin이 lag 정보를 더한다". RNA-only floor 없이는 chromatin 기여 증명 불가; ATAC permutation 음성대조 없이는 chromatin 채널이 장식인지 모름. (현재 "optional sanity"는 부적절.)
5. **CRAK-Velo lag proxy confound** — CRAK-Velo는 lag 미출력 → proxy를 우리가 발명. 한 참가자만 metric을 만들어주는 것 = 그 참가자 결과 해석 불가. → 기본 **direction axis(A)에만** 포함, lag axis(B/C)는 proxy가 독립 검증(switch time 대비 사전 임계 통과) 통과 후에만, 그때도 "proxy-derived" 플래그 + 1차 결정 제외.

## MAJOR
- **null/test 미정** (H1 "구분된다"의 통계량·null·단위 부재) → 사전등록: marker=hypergeometric(dynamic-gene background)+permutation-FDR, stability=gene 단위 paired bootstrap, pass 임계 사전 고정.
- **multiple testing family 미정** → permutation FDR(lineage 내 cell/pseudotime shuffle) 권장(공조절 gene 비독립 → parametric FDR anti-conservative). 4 method × 수천 gene × bootstrap family 경계 명시.
- **power/n** → n=11,605 확정(해결). 단 4–5 lineage로 쪼개면 low-expression gene CI 넓음 → expression/coverage floor 사전 commit. method n=4는 추론 모집단 없음 → concordance는 *descriptive*(gene축 bootstrap CI)로만.
- **MultiVelo home-field** — annotation/preprocessing이 MultiVelo 기준 → method-agnostic Leiden/marker annotation을 velocity 실행 전 freeze, MultiVelo-native 대비 sensitivity.
- **method 비독립 (H1)** — MoFlow⊃cellDancer, MultiVeloVAE⊃MultiVelo 계보 → 공유 bias로 agree 가능. agreement는 necessary-not-sufficient, 독립 계열 method 1개 tie-breaker + stability 병행.
- **lag 정의 incomparability** — DTW lag/δ·κ(rate)/switch time(scalar)/region-kinetic은 같은 latent lag의 monotone 변환 아님. → sign-agreement와 rank-correlation **분리 보고**, monotonicity 가정 명시 또는 sign-only로 강등, known-gene **construct-validity sign check**.
- **누락 confound**: ambient RNA/doublet(SoupX/CellBender/Scrublet — unspliced 민감, agree로 위장), ATAC depth/peak batch(joint peak calling 확인, timepoint별 QC), lineage-specific kinetics(**within-lineage 계산 후 집계**), composition imbalance(희소 lineage=MK/platelet은 n 적어 불안정→"disagreement"가 sampling artifact).
- **cell cycle/burst 미operationalize** — "covariate 통제"만. lag에 사후 covariate 못 넣음 → cycle score로 stratify 또는 quiescent cell 한정, cycling 포함/제외 양쪽 보고. (원논문도 cycle regress-out.)
- **method-specific smoothing/kNN** — neighbor graph가 model보다 결과 좌우 가능 → 공통 graph ablation(native vs 공통) 추가.
- **CBDir/GCBDir = direction metric, lag 품질 아님** — annotation bias 상속, 굵은 lineage 방향만 보상. → trajectory sanity tie-breaker로 명시, 1차 결정은 lag-specific B/C/D로.
- **external replication 부재** — 단일 데이터(=MultiVelo home). 최소한 ranking을 팀의 다른 multiome(mouse brain/skin)로 외부 재현.

## MINOR
- DeepKINET "negative correlation = fail"은 set value 없으면 *self-consistency*(validity 아님) → stability로 rename.

## TOP 5 (실행 전 필수)
1. H1 순환 제거: marker enrichment(whole-genome) → **bootstrap lag-sign stability** 1차 + dynamic-gene background enrichment 2차, null/test/단위/임계 사전등록.
2. H2 강등: batch-aliased·1 interval·composition shift → confounded directional sanity only, permuted-day-label control, wall-clock 단위 불가 명시, method 결정에서 배제.
3. RNA-only baseline + scrambled-chromatin ablation **REQUIRED**(+ no-lag null).
4. lag metric을 consistency/stability로 reframe + injected-lag simulator를 유일 accuracy arm(secondary).
5. 정의 incomparability·CRAK-Velo proxy 격리: sign/rank 분리, known-gene construct check, CRAK-Velo는 axis A only(검증 전).

## 교차 must-do
- ~~cell-count 모호~~ → 11,605 확정(repo 검증). 단 lineage별 expression floor 필요.
- 모든 concordance/lag 비교는 **lineage 내**에서(pooling은 method 차이와 composition 혼동).
