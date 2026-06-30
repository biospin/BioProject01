# scrambled-chromatin 음성대조 검정 (P3 / DESIGN §43·§75)

> 원본 MultiVelo vs **ATAC within-lineage 셔플** 재fit. shared gene n=538. lag = fit_t_sw2 − fit_t_sw1.

## 결론 (요약)
**chromatin 채널은 MultiVelo lag을 구동하지 않는다(기여 미미).** ATAC를 셔플(chromatin↔RNA 결합 파괴)해도 lag **분포**는 통계적으로 동일(Mann–Whitney p=0.196, KS p=0.507)하고, per-gene lag도 대부분 보존(Spearman ρ=0.721, 상대변화 median 15%). → MultiVelo의 chromatin→transcription lag은 chromatin 신호가 아니라 **모델 구조(switch-time 단조 순서)·gene 고유 RNA 동역학**에서 나오는 값. 이는 H1의 'MultiVelo 100% chromatin-leads는 아티팩트' 결론을 음성대조로 확증. 단 Wilcoxon paired(p=0.0003)로 **작은 체계적 이동**(median 5.868→5.475, 셔플 시 소폭 감소)은 검출됨 → chromatin이 lag 크기를 미세하게 부풀리는 **주변적(marginal) 기여**는 있으나 지배적 요인은 아님.

## 1. lag 분포: 원본 vs scrambled
| | n | median | mean | IQR | %>0 |
|---|---|---|---|---|---|
| 원본 | 538 | 5.868 | 6.289 | [3.028, 8.998] | 100.0% |
| scrambled | 538 | 5.475 | 5.946 | [2.598, 8.475] | 100.0% |

- Mann–Whitney U(분포 동일성): p=0.1957 (차이 없음)
- KS 2-sample: D=0.050, p=0.5074 (차이 없음)
- Wilcoxon paired(이동): p=0.0003

## 2. per-gene lag: 셔플이 gene 수준 lag을 흩뜨리나
- 원본 vs scrambled lag **Spearman ρ=0.721** (p=0.0000), Pearson r=0.720
- gene별 lag 상대변화 median **14.7%**

> ρ이 높고 상대변화가 작을수록 lag이 chromatin이 아니라 **gene 고유 RNA 동역학**에서 결정됨을 의미(chromatin 셔플에 둔감).

## 3. chromatin 적합 품질 (chromatin 채널 기여도)
| 지표 | 원본 median | scrambled median |
|---|---|---|
| fit_alpha_c (chromatin rate) | 0.0562 | 0.0506 |
| fit_likelihood_c (chromatin lik) | 0.2390 | 0.2365 |
| fit_likelihood (전체 lik) | 0.0419 | 0.0400 |

> chromatin likelihood가 셔플 후에도 비슷하면 chromatin 채널이 적합을 거의 안 바꿈.

## 한계
- MultiVelo 단일 method 음성대조(switch-lag 정의). DTW-lag method(MoFlow)·CRAK-Velo의 scramble은 별도 필요(후속).
- 셔플은 within-lineage cell permutation(per-gene marginal·lineage 구성 보존). lineage 간 chromatin 차이는 보존되므로 보수적 null.
- seed 고정(p2_config.RANDOM_SEED). 1회 realization (multi-seed 분산은 후속).

