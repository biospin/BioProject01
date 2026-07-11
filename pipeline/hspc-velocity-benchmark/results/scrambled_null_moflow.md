# MoFlow scrambled-chromatin 음성대조 검정 (Track C / novelty_strategy §4.2)

> 원본 MoFlow(`moflow_genes.csv` + `moflow.h5ad`) vs **ATAC within-lineage 셔플** 재fit
> (`moflow_scrambled_genes.csv` + `moflow_scrambled.h5ad`). lag = MoFlow DTW **c–s lag**(chromatin→spliced).
> MultiVelo 음성대조(`scrambled_null.md`)와 **apples-to-apples**: 동일 `scramble_within_lineage()`
> + 동일 `RANDOM_SEED`(raw ATAC 행 permute) → 동일 `smooth_chrom()`(knn_smooth_chrom 등가) 재smooth
> → new `Mc` → 나머지 fit 설정은 원본 full run과 동일. GPU cuda:1(`CUDA_VISIBLE_DEVICES=1`), runtime 6473s.
> 원본 gene 636 / 셔플 gene 633 / 공통 632. 셔플 sanity: 6 lineage 100% cell permute, per-gene marginal 상관 1.0000
> (marginal·lineage 구성 보존, cell 수준 chromatin↔RNA 결합만 파괴), Mc 실제 변화.

## 결론 (요약)
**MoFlow lag은 ATAC 셔플을 견딘다 — chromatin 채널은 MoFlow의 fit도 lag도 구동하지 않는다.** 이로써
"lag은 chromatin이 아니라 **모델 구조**에서 나온다"는 결론이 **switch-time method(MultiVelo) 한 종에서
DTW/deep-learning relay-velocity method(MoFlow)까지 아키텍처가 다른 두 번째 method로 일반화**된다. 근거:
1. **[핵심 discriminator] chromatin 채널이 fit을 안 바꾼다.** 셔플 후 chromatin transcription rate 크기
   `|alpha_c|` median 0.5008→0.4991 (**Wilcoxon p=0.52, 무변화**), chromatin velocity `|velo_c|`
   0.1152→0.1094 (**p=0.12, 무변화**), 학습 loss median 0.1474→0.1449 (Δ=−0.0025, **fit이 나빠지지
   않음 — 오히려 미세 감소**). chromatin↔RNA 결합을 파괴해도 MoFlow fit 품질이 **저하되지 않으므로**
   chromatin은 fit에 실질 기여를 안 한다. (MultiVelo에서 likelihood_c 0.239→0.237 무변화와 동형이다.)
2. **lag 분포가 통계적으로 동일하다.** cs_lag(median 요약): Mann–Whitney **p=0.377**, KS **p=0.176** → 차이 없음.
   chromatin-leading(cs_lag>0) 비율 44.8%→38.9% (~6pt 소폭 감소, 균형대 유지 — 붕괴 아님).
3. **[lag의 직접 검정] per-gene lag이 보존된다.** signed Spearman **ρ=+0.52**(p=6e-46), sign-agreement 59.5%,
   Wilcoxon paired **p=0.17**(체계적 이동 없음). MoFlow lag은 fit 파라미터가 아니라 fit **이후** `Mc`를
   pseudotime으로 binning하는 **post-hoc DTW**이므로, chromatin이 lag에 들어오는 경로가 둘 —
   (a) fit→pseudotime, (b) `Mc`→DTW c-curve 직접 — 이다. §3은 두 경로를 모두 포함한 **lag의 직접 검정**이고,
   §1은 (a) 경로(pseudotime 축)가 chromatin-구동이 아님을 확인하는 **보강**이다(§4 참조).

셔플에도 (1) chromatin 채널이 fit에 실질 기여를 안 하고 (2) lag 분포가 그대로이며 (3) gene 수준 lag이
유지되는 **세 축의 수렴**은 **"MoFlow의 c–s lag 역시 chromatin 신호가 아니라 모델 구조(pseudotime 위 RNA
동역학 정렬)에서 나온다"**는 확증이다. **weak≠zero**: chromatin의 *주변적(marginal)* 기여는 있으나(loss
Wilcoxon p=1.6e-10로 미세 이동 검출, chromatin-leading 비율 소폭 표류) 지배적 요인은 아니다 — MultiVelo와 동일한 패턴이다.

> **셔플 ρ=0.52 vs method-swap ρ=0.08** (`moflow_directional_check.md`의 MoFlow×MultiVeloVAE lag ρ):
> chromatin을 **파괴**해도 per-gene lag은 ρ=0.52로 유지되는데, chromatin을 **그대로 둔 채 method만 바꾸면**
> ρ=0.08로 붕괴한다. lag이 chromatin-구동이라면 chromatin 파괴(셔플)가 method 교체보다 lag을 **더** 흩뜨려야
> 하는데 정반대다 → "ρ=0.52 = 보존(붕괴 아님)"을 same-ATAC 재fit 상한 없이 정박(anchor)하며, "lag은
> model-structural·method-specific"을 직접 보강한다. (두 ρ 모두 단위/정의 confound가 있어 **정성적**으로만 사용한다.)

## 1. chromatin 채널 fit-quality (핵심 discriminator; n=632 공통 gene)
| 지표 | 원본 median | scrambled median | Δ | Wilcoxon paired p | 해석 |
|---|---|---|---|---|---|
| `loss` (학습 loss, ↓=좋음) | 0.1474 | 0.1449 | **−0.0025** | 1.6e-10 | fit **저하 없음**(미세 개선) |
| `|alpha_c|` (chromatin rate) | 0.5008 | 0.4991 | −0.0016 | **0.515** | **무변화** |
| `|velo_c|` (chromatin velocity) | 0.1152 | 0.1094 | −0.0058 | **0.120** | **무변화** |

> chromatin↔RNA 결합을 파괴해도 chromatin rate/velocity 크기가 통계적으로 불변이고 fit이 나빠지지 않으면,
> chromatin 채널이 fit에 실질 기여를 안 한다는 뜻이다. loss의 유의한 미세 이동(p=1.6e-10)은 n=632 paired가
> 아주 작은 체계적 차이를 잡아낸 것으로, **방향이 저하가 아니라 소폭 개선**이라 "chromatin 무기여" 결론을
> 약화시키지 않는다. (MultiVelo Wilcoxon p=0.0003의 미세 이동과 동일 성격이다.)

## 2. lag 분포: 원본 vs scrambled
| | n | median | mean | IQR | %>0 (chromatin-leading) |
|---|---|---|---|---|---|
| 원본 (cs_lag_median) | 636 | 0.0000 | −0.0146 | [−0.143, 0.095] | 44.8% |
| scrambled (cs_lag_median) | 633 | 0.0000 | −0.0213 | [−0.143, 0.095] | 38.9% |
| 원본 (cs_lag_mean) | 636 | 0.0082 | −0.0129 | [−0.150, 0.105] | 51.3% |
| scrambled (cs_lag_mean) | 633 | −0.0176 | −0.0197 | [−0.133, 0.097] | 46.1% |

- cs_lag_median: Mann–Whitney U **p=0.377**, KS D=0.061 **p=0.176** → 분포 동일.
- cs_lag_mean: Mann–Whitney U **p=0.455**, KS D=0.080 **p=0.032**(경계적 유의) → 평균요약에선 KS가 미세
  차이를 잡지만 MW는 무변화. chromatin-leading 비율은 두 요약 모두 ~5–6pt 감소하나 **균형대(≈40–50%)를
  유지** → MultiVelo의 100%(구조적 tautology)와 달리 MoFlow는 원래도 균형이었고 셔플 후에도 붕괴하지 않는다.

## 3. per-gene lag: 셔플이 gene 수준 lag을 흩뜨리나 (n=632 공통 gene)
| 요약 | signed Spearman ρ | |lag| Spearman ρ | sign-agreement | Wilcoxon paired p | 상대변화 median |
|---|---|---|---|---|---|
| cs_lag_median | **+0.524** (p=6e-46) | +0.224 (p=1e-08) | 59.5% | 0.173 | 1.00 |
| cs_lag_mean | **+0.518** (p=1e-44) | +0.240 (p=1e-09) | 67.6% | 0.098 | 0.88 |

> signed ρ≈0.52, sign-agreement가 chance(50%) 위, Wilcoxon로 체계적 이동 없음 → gene 수준 lag이 셔플에
> 대체로 **둔감하다**(chromatin이 gene별 lag 방향을 결정하지 않음). cs_lag는 Mc·Mu·Ms·pseudotime에 의존하는데
> 이 중 **Mc만 셔플**(Mu/Ms 불변)했음에도 lag이 유지되는 것은 lag이 RNA 측 동역학·pseudotime 정렬에서
> 주로 결정됨을 시사한다(= chromatin-구동 아님). |lag| ρ은 0.22로 약하지만 양수이고 유의하다.

## 4. 근거 구조 / caveat (verdict 해석 주의)
- **verdict = §1·§2·§3의 수렴이며, §1 단독이 아니다.** MoFlow lag은 fit 파라미터가 아니라 **post-hoc DTW**
  (fit 후 `Mc`/`Ms`를 pseudotime으로 binning)이므로, chromatin이 lag에 들어오는 경로가 (a) fit→pseudotime,
  (b) `Mc`→DTW c-curve **직접** 두 갈래다. **§1(alpha_c/velo_c 무변화)은 (a) 경로만** 검정한다 —
  chromatin이 fit·pseudotime을 구동 안 함을 보여 §3이 trivially rigged가 아님을 보강할 뿐, 그 자체로 lag을
  검정하지 못한다. **lag의 직접 검정은 §3(ρ=0.52 보존)** 이며, (b) 경로까지 포함한다. 즉 "fit-무감 = lag-무감"의
  단순 치환은 post-hoc readout에 대해 성립하지 않는다(methodologist가 노릴 지점). → **§3이 직접 증거,
  §1이 보강, §2가 분포 확인, 셋의 수렴으로 "survives"**. (MultiVelo에선 lag=`sw2−sw1`가 fit 파라미터라
  likelihood_c가 lag에 직접 작용 → §1이 곧 직접 증거였다. MoFlow는 구조가 달라 근거 배선이 다르다.)
- **per-gene ρ의 신뢰도 상한은 미상이다.** MoFlow c–s lag은 (a) 부호 가변이고 `crakvelo_sign_check` 기준 양수=chromatin선행,
  (b) **매끄러운 kinetic에서 per-gene 부호 불안정**(`crakvelo_dtw_lag_shape_dependence`), (c) MoFlow fit이
  stochastic이라 **동일 ATAC 재fit도 완벽 재현되지 않는다**. same-ATAC 재fit test-retest 상한이 없어 ρ=0.52의 절대
  높낮이는 단정 못 하나 — 위 §3의 **셔플 ρ=0.52 vs method-swap ρ=0.08** 대비가 "붕괴 아님"을 상한 없이
  정박한다(정성적).
- **dropped genes**: 원본 636 → 셔플 633, 공통 632. 셔플에서 빠진 4개(AC004053.1·CCL5·CLEC7A·JCHAIN, lncRNA/
  immune 혼합)·새로 든 1개(TMEM40)는 **4/636=0.6%**로 fit-ability 경계 gene의 stochastic dropout이며 특정
  chromatin-의존 class에 편중되지 않는다(= "chromatin-의존 gene이 셔플서 fit 실패" 아님). 모든 paired 통계는 632 공통 gene 기준이다.
- **셔플 정의**: within-lineage cell permutation(per-gene marginal·lineage 구성 보존; lineage 간 chromatin
  차이 보존 → 보수적 null). MultiVelo 음성대조와 **동일 seed·동일 함수**로 apples-to-apples로 맞췄다.
- **MoFlow real run과 동일 한계 계승**: ATAC batch, DTW c–s lag construct의 sign convention
  (`crakvelo_sign_check.md`), gene별 pseudotime 아닌 global time 사용.
- **단일 realization**(seed 고정, RANDOM_SEED)이다. multi-seed 분산·동일-ATAC 재fit reliability 상한은 후속이다.
- KS는 cs_lag_mean에서 경계적으로 유의하다(p=0.032). 평균요약이 median요약보다 tail에 더 민감하기 때문이다. 두 요약
  모두 MW는 무변화라 분포 동일 결론은 유지하되, "완전 동일"이 아닌 "통계적으로 구별 안 되는 수준 + 미세 marginal 기여"로 서술한다.

## 5. FINDINGS 반영 (한계 #4 해소 → 일반화)
- `FINDINGS.md` 한계 #4("음성대조는 MultiVelo 단일 method")를 **2번째 method(MoFlow)로 확장한다**.
- 반영 문구(제안, Track A가 병합): *"chromatin→transcription lag이 model-structural(chromatin 미구동)이라는
  음성대조 결론은 이제 switch-time method(MultiVelo)와 DTW/deep-learning relay-velocity method(MoFlow) —
  아키텍처가 서로 다른 두 method에서 재현된다. MoFlow도 within-lineage ATAC 셔플 후 chromatin rate/velocity
  크기가 불변(alpha_c p=0.52, velo_c p=0.12)이고 fit이 저하되지 않으며(loss 무저하) lag 분포가 통계적으로
  동일(MW p=0.38, KS p=0.18)하다. → 'lag은 한 method의 quirk가 아니라 chromatin-informed velocity의 일반
  속성'."*  ※ 이 md는 Track A가 FINDINGS.md에 병합한다. 이 파일은 FINDINGS.md를 직접 수정하지 않는다.

---
_재계산: `conda run -n velo-torch python scripts/p3_scrambled_null_moflow.py` (입력 `results/moflow_scrambled_genes.csv`
+ `data/velocity/moflow{,_scrambled}.h5ad`). fit: `scripts/p2_moflow_scrambled.py` (cuda:1, seed=RANDOM_SEED)._

---

# MoFlow scrambled-chromatin negative control test (Track C / novelty_strategy §4.2)

> Original MoFlow (`moflow_genes.csv` + `moflow.h5ad`) vs **ATAC within-lineage shuffle** refit
> (`moflow_scrambled_genes.csv` + `moflow_scrambled.h5ad`). lag = MoFlow DTW **c–s lag** (chromatin→spliced).
> **Apples-to-apples** with the MultiVelo negative control (`scrambled_null.md`): same `scramble_within_lineage()`
> + same `RANDOM_SEED` (permute raw ATAC rows) → same `smooth_chrom()` (knn_smooth_chrom equivalent) re-smooth
> → new `Mc` → the remaining fit settings identical to the original full run. GPU cuda:1 (`CUDA_VISIBLE_DEVICES=1`), runtime 6473s.
> Original gene 636 / shuffled gene 633 / common 632. Shuffle sanity: 6 lineages 100% cell permute, per-gene marginal correlation 1.0000
> (marginal and lineage composition preserved, only cell-level chromatin↔RNA coupling destroyed), Mc actually changes.

## Conclusion (summary)
**MoFlow lag withstands ATAC shuffling — the chromatin channel drives neither MoFlow's fit nor its lag.** With this,
the conclusion that "lag arises not from chromatin but from **model structure**" **generalizes from one switch-time
method (MultiVelo) to a second method of a different architecture — a DTW/deep-learning relay-velocity method
(MoFlow)**. Evidence:
1. **[core discriminator] the chromatin channel does not change the fit.** After shuffling, chromatin transcription rate
   magnitude `|alpha_c|` median 0.5008→0.4991 (**Wilcoxon p=0.52, no change**), chromatin velocity `|velo_c|`
   0.1152→0.1094 (**p=0.12, no change**), training loss median 0.1474→0.1449 (Δ=−0.0025, **fit does not
   worsen — if anything a slight decrease**). Because destroying the chromatin↔RNA coupling **does not degrade**
   MoFlow fit quality, chromatin makes no substantive contribution to the fit. (Isomorphic to MultiVelo's
   likelihood_c 0.239→0.237 no-change.)
2. **The lag distribution is statistically identical.** cs_lag (median summary): Mann–Whitney **p=0.377**, KS **p=0.176** → no difference.
   chromatin-leading (cs_lag>0) fraction 44.8%→38.9% (~6pt slight decrease, balance retained — not a collapse).
3. **[direct test of lag] per-gene lag is preserved.** signed Spearman **ρ=+0.52** (p=6e-46), sign-agreement 59.5%,
   Wilcoxon paired **p=0.17** (no systematic shift). MoFlow lag is not a fit parameter but a **post-hoc DTW** that,
   **after** the fit, bins `Mc` into pseudotime, so chromatin has two paths into lag —
   (a) fit→pseudotime, (b) `Mc`→DTW c-curve directly. §3 is a **direct test of lag** that includes both paths, and
   §1 is a **reinforcement** that confirms the (a) path (the pseudotime axis) is not chromatin-driven (see §4).

The **convergence of three axes** under shuffling — (1) the chromatin channel makes no substantive contribution to the fit,
(2) the lag distribution is unchanged, and (3) gene-level lag is preserved — is a confirmation that **"MoFlow's c–s lag,
too, arises not from the chromatin signal but from model structure (alignment of RNA dynamics along pseudotime)."**
**weak≠zero**: chromatin does make a *marginal* contribution (loss Wilcoxon p=1.6e-10 detects a tiny shift,
chromatin-leading fraction drifts slightly), but it is not the dominant factor — the same pattern as MultiVelo.

> **shuffle ρ=0.52 vs method-swap ρ=0.08** (the MoFlow×MultiVeloVAE lag ρ in `moflow_directional_check.md`):
> even when chromatin is **destroyed**, per-gene lag holds at ρ=0.52, whereas **leaving chromatin intact and only swapping the method**
> collapses it to ρ=0.08. If lag were chromatin-driven, destroying chromatin (shuffle) should scatter lag **more** than
> swapping the method, but the opposite holds → this anchors "ρ=0.52 = preserved (not a collapse)" without a same-ATAC refit
> ceiling, and directly reinforces "lag is model-structural and method-specific." (Both ρ carry unit/definition confounds,
> so they are used **qualitatively** only.)

## 1. chromatin channel fit-quality (core discriminator; n=632 common genes)
| metric | original median | scrambled median | Δ | Wilcoxon paired p | interpretation |
|---|---|---|---|---|---|
| `loss` (training loss, ↓=better) | 0.1474 | 0.1449 | **−0.0025** | 1.6e-10 | **no degradation** (slight improvement) |
| `|alpha_c|` (chromatin rate) | 0.5008 | 0.4991 | −0.0016 | **0.515** | **no change** |
| `|velo_c|` (chromatin velocity) | 0.1152 | 0.1094 | −0.0058 | **0.120** | **no change** |

> If, even after destroying the chromatin↔RNA coupling, chromatin rate/velocity magnitude is statistically invariant and the fit
> does not worsen, it means the chromatin channel makes no substantive contribution to the fit. The significant tiny shift in loss
> (p=1.6e-10) is n=632 paired picking up a very small systematic difference, and because its **direction is not degradation but a slight
> improvement**, it does not weaken the "chromatin no-contribution" conclusion. (Same in character as MultiVelo's Wilcoxon p=0.0003 tiny shift.)

## 2. lag distribution: original vs scrambled
| | n | median | mean | IQR | %>0 (chromatin-leading) |
|---|---|---|---|---|---|
| original (cs_lag_median) | 636 | 0.0000 | −0.0146 | [−0.143, 0.095] | 44.8% |
| scrambled (cs_lag_median) | 633 | 0.0000 | −0.0213 | [−0.143, 0.095] | 38.9% |
| original (cs_lag_mean) | 636 | 0.0082 | −0.0129 | [−0.150, 0.105] | 51.3% |
| scrambled (cs_lag_mean) | 633 | −0.0176 | −0.0197 | [−0.133, 0.097] | 46.1% |

- cs_lag_median: Mann–Whitney U **p=0.377**, KS D=0.061 **p=0.176** → distribution identical.
- cs_lag_mean: Mann–Whitney U **p=0.455**, KS D=0.080 **p=0.032** (borderline significant) → in the mean summary KS picks up a tiny
  difference but MW shows no change. The chromatin-leading fraction decreases by ~5–6pt in both summaries yet **stays in the balanced
  band (≈40–50%)** → unlike MultiVelo's 100% (a structural tautology), MoFlow was balanced to begin with and does not collapse after shuffling.

## 3. per-gene lag: does shuffling scatter gene-level lag? (n=632 common genes)
| summary | signed Spearman ρ | |lag| Spearman ρ | sign-agreement | Wilcoxon paired p | relative change median |
|---|---|---|---|---|---|
| cs_lag_median | **+0.524** (p=6e-46) | +0.224 (p=1e-08) | 59.5% | 0.173 | 1.00 |
| cs_lag_mean | **+0.518** (p=1e-44) | +0.240 (p=1e-09) | 67.6% | 0.098 | 0.88 |

> signed ρ≈0.52, sign-agreement above chance (50%), no systematic shift by Wilcoxon → gene-level lag is mostly **insensitive** to
> shuffling (chromatin does not determine the per-gene lag direction). cs_lag depends on Mc·Mu·Ms·pseudotime, yet with **only Mc shuffled**
> (Mu/Ms unchanged) lag is retained, which suggests lag is determined mainly by the RNA-side dynamics and pseudotime alignment
> (= not chromatin-driven). |lag| ρ is 0.22, weak but positive and significant.

## 4. evidence structure / caveats (careful reading of the verdict)
- **verdict = convergence of §1·§2·§3, not §1 alone.** MoFlow lag is not a fit parameter but a **post-hoc DTW**
  (after the fit, binning `Mc`/`Ms` into pseudotime), so chromatin has two paths into lag: (a) fit→pseudotime,
  (b) `Mc`→DTW c-curve **directly**. **§1 (alpha_c/velo_c no change) tests only path (a)** —
  showing chromatin does not drive the fit/pseudotime, it only reinforces that §3 is not trivially rigged, and by itself does not
  test lag. **The direct test of lag is §3 (ρ=0.52 preserved)**, which includes path (b) too. That is, the simple substitution
  "fit-insensitive = lag-insensitive" does not hold for a post-hoc readout (the spot a methodologist would target). → **§3 is the direct
  evidence, §1 the reinforcement, §2 the distribution check, and their convergence gives "survives".** (In MultiVelo, lag=`sw2−sw1`
  is a fit parameter, so likelihood_c acts directly on lag → §1 was itself the direct evidence. MoFlow's structure differs, so the evidence wiring differs.)
- **The reliability ceiling of per-gene ρ is unknown.** MoFlow c–s lag is (a) sign-variable and, per `crakvelo_sign_check`, positive=chromatin-leads,
  (b) **per-gene sign-unstable on smooth kinetics** (`crakvelo_dtw_lag_shape_dependence`), (c) because MoFlow fit is
  stochastic, **even a same-ATAC refit does not reproduce perfectly**. Without a same-ATAC refit test-retest ceiling, the absolute
  level of ρ=0.52 cannot be asserted — but the §3 contrast of **shuffle ρ=0.52 vs method-swap ρ=0.08** above anchors "not a collapse"
  without a ceiling (qualitatively).
- **dropped genes**: original 636 → shuffled 633, common 632. The 4 dropped under shuffling (AC004053.1·CCL5·CLEC7A·JCHAIN, an lncRNA/
  immune mix) and the 1 newly added (TMEM40) are **4/636=0.6%**, a stochastic dropout of fit-ability borderline genes, not concentrated in any
  particular chromatin-dependent class (= not "chromatin-dependent genes fail to fit under shuffling"). All paired statistics use the 632 common genes.
- **shuffle definition**: within-lineage cell permutation (preserving per-gene marginal and lineage composition; between-lineage chromatin
  differences preserved → conservative null). Matched apples-to-apples with the MultiVelo negative control using the **same seed and same function**.
- **Inherits the same limitations as the MoFlow real run**: ATAC batch, the sign convention of the DTW c–s lag construct
  (`crakvelo_sign_check.md`), use of global time rather than per-gene pseudotime.
- **Single realization** (seed fixed, RANDOM_SEED). Multi-seed variance and the same-ATAC refit reliability ceiling are follow-ups.
- KS is borderline significant on cs_lag_mean (p=0.032). This is because the mean summary is more tail-sensitive than the median summary. Since MW
  shows no change in both summaries, the distribution-identical conclusion holds, but it is stated not as "completely identical" but as
  "statistically indistinguishable + a tiny marginal contribution."

## 5. Reflection into FINDINGS (resolving limitation #4 → generalization)
- **Extends** `FINDINGS.md` limitation #4 ("the negative control is a single method, MultiVelo") **to a 2nd method (MoFlow)**.
- Proposed wording (Track A to merge): *"The negative-control conclusion that chromatin→transcription lag is model-structural
  (not chromatin-driven) is now reproduced across two methods of different architectures — a switch-time method (MultiVelo) and a
  DTW/deep-learning relay-velocity method (MoFlow). After within-lineage ATAC shuffling MoFlow too shows invariant chromatin rate/velocity
  magnitude (alpha_c p=0.52, velo_c p=0.12), an undegraded fit (loss no degradation), and a statistically identical lag distribution
  (MW p=0.38, KS p=0.18). → 'lag is not the quirk of a single method but a general property of chromatin-informed velocity'."*
  ※ This md is merged into FINDINGS.md by Track A. This file does not edit FINDINGS.md directly.

---
_Recompute: `conda run -n velo-torch python scripts/p3_scrambled_null_moflow.py` (input `results/moflow_scrambled_genes.csv`
+ `data/velocity/moflow{,_scrambled}.h5ad`). fit: `scripts/p2_moflow_scrambled.py` (cuda:1, seed=RANDOM_SEED)._
