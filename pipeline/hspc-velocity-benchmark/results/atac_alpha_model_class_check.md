# P5c — baseline ATAC→α 의 약한 신호가 선형 모형 탓인가

> 2026-08-30, kkkim. `atac_alpha_expression_confound.md`(P5b)의 후속 견고성 점검.
> **상태: 탐색적.** 커밋·원고 반영 전 팀 검토 필요.

## 왜

P5b에서 baseline ATAC→α 는 raw held-out ρ=+0.309, 발현 통제 partial ρ=+0.112 (n=472)로
발현 confound에 크게 잠식됐다. 리뷰어가 물을 수 있는 반론이 하나 남는다.
**"선형 모형이라 비선형 관계를 놓친 것 아닌가."** 모형 계열을 바꿔 확인한다.

## 방법

- 특징: `atac_baseline_features.csv`의 진짜 ATAC peak 6종
  (prom_acc, enh_acc, enh_sum, n_prom, n_enh, prom_enh_ratio)
- 표적: `lag_model.csv`의 `fit_alpha`, 계보 라벨도 같은 파일
- 분할: Leave-One-Lineage-Out (계보 6개). P5b와 같은 계보 홀드아웃 규약
- 발현 통제: `coupling_per_gene.csv`의 abundance에 대해 예측·실측을 각각 순위 회귀한 잔차끼리 상관
- 모형: RidgeCV(선형), RandomForest(500, min_samples_leaf=5), GradientBoosting(기본)

## 재현 확인

선형 모형이 P5b 수치를 재현한다. **held-out ρ=+0.304**(기록 +0.309),
**partial ρ=+0.109**(기록 +0.112), **n=472**(기록 n=472). 설정이 일치한다.

## 결과

| 모형 | held-out ρ | p | 발현 통제 partial ρ |
|---|---|---|---|
| linear (RidgeCV) | **+0.304** | 1.47e-11 | **+0.109** |
| RandomForest | +0.178 | 1.02e-04 | +0.013 |
| GradientBoosting | +0.206 | 6.64e-06 | +0.056 |

개별 특징의 fit_alpha 상관: enh_n +0.352, enh_sum +0.318, enh_acc +0.228,
prom_enh_ratio −0.246, prom_acc −0.128, n_prom +0.046

## 해석

**비선형 모형은 선형을 넘지 못하고 오히려 떨어진다.** 발현을 통제하면 격차가 더 벌어져
RandomForest의 partial은 +0.013으로 사실상 0이다. n=472에 특징 6개인 조건에서 유연한 모형이
과적합해 일반화가 나빠지는 전형적인 양상이다.

따라서 "선형 모형이라 신호를 놓쳤다"는 반론은 닫힌다. ATAC→α 신호가 발현 통제 후 약한 것은
모형 계열의 한계가 아니라 신호 자체의 성질이다. P5b의 결론을 약화시키지 않고 오히려 보강한다.

## 한계

- 계보 홀드아웃 한 규약만 봤다. 유전자 무작위 분할은 확인하지 않았다.
- 하이퍼파라미터를 조정하지 않았다(기본값 + 최소 규제). 튜닝하면 비선형이 선형에 근접할 수는
  있으나 넘어설 근거는 이 표본 크기에서 기대하기 어렵다.
- 발현 통제는 순위 선형 잔차 방식이다. P5b가 쓴 통제 방식과 완전히 동일한지 대조하지 않았다.

재현: `scripts/p5c_alpha_model_class_check.py`
