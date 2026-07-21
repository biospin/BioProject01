# P3 — 전체 re-fit bootstrap: α_c vs lag 재fit 안정성

> p5_bootstrap_stability.py(fit 고정, stability 하한)가 남긴 미완 — **전체 re-fit 반복** — 수행.
> cell 15315~ (frac 0.70 비복원 subsample) 마다 MultiVelo 처음부터 재fit, canonical gene 고정. **12 refit**.

## 재fit 간 안정성 (per-gene)

| 수량 | gene | rank 일치도(쌍별 Spearman) | median CV |
|---|---|---|---|
| α_c (chromatin opening rate) | 485 | **+0.729** | 0.25 |
| α (transcription rate) | 485 | **+0.949** | 0.23 |
| lag (switch time 차) | 485 | **+0.624** | 0.31 |

> **부호(sign)는 stability 지표에서 제외.** MultiVelo lag = t_switch(chromatin) − t_switch(transcription)는 485/485 gene·전 12 refit에서 항상 양수라 flip이 구조적으로 불가능하다(모델의 causal ordering이 부호를 고정). 따라서 "flip 100% 안정"은 robustness가 아니라 tautology이며, 재fit 안정성은 오직 rank 일치도·CV로만 읽는다. (p5의 lag 부호 83% 안정은 dtw 기반 signed lag — 다른 정의라 비교 불가.)

## 해석

- **재fit 간 rank 일치도: α_c=+0.729 vs lag=+0.624, CV 0.25 vs 0.31.**
  → lag은 α_c보다 재fit 간 rank 재현성이 낮다(CV도 높음). H1('α 계열 robust, lag 비robust')과 **consistent** — 5개 확증 축 중 재fit-안정성 축 1개. (격차는 modest — 이 축 단독이 결론을 지지하는 건 아니고, 다른 4축과 함께 누적 근거.)
- '한 fit 안 표집 안정(p5_bootstrap_stability, fit 고정)'과 '전체 재fit 안정'은 다른 질문이며, drug-timing 관점에서 실질 stability는 후자(재fit).
- drug-timing 모델 시사: 재fit-robust한 α_c·α를 baseline-ATAC와 함께 쓰고(§6 lag_model_atac에서 α 예측 ρ=+0.31), lag은 재fit-불안정 → 단일 값 사용 금지·uncertainty 반영.
- ⚠️ subsample(비복원 frac 0.70) 기반 — 복원추출 아님(kNN graph 붕괴 회피). gene→canonical 고정.
