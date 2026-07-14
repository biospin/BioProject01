# 사전등록 채점표 — GSE205117 (mouse gastrulation) 5번째 cross-dataset

> `manuscript/PREREGISTRATION_gse205117.md`의 봉인된 6개 예측을 기계적으로 채점한다.
> paired bootstrap B=10,000, seed=20260707. **결과가 나쁘면 나쁜 대로 FAIL을 적는다(사후 구제 금지).**

- α **floor×MV** (shared 846): Spearman **+0.911** 95%CI [+0.897, +0.923]
- α **floor×VAE** (shared 1001): Spearman **+0.927** 95%CI [+0.915, +0.937]
- α **MV×VAE** (shared 969): Spearman **+0.953** 95%CI [+0.946, +0.959]

- lag 크기 rank **MV×VAE** (shared 969): Spearman **-0.026** 95%CI [-0.089, +0.038]
  - sign 검정 생략: MultiVelo lag 부호는 4-state 단조정렬로 구조적 양수(무정보).

- **Δρ = ρ_α − ρ_lag = +0.979** 95%CI [+0.916, +1.041] (paired, 공통 969 gene)

- cross **α rank** HSPC×gastrulation (shared 111): **+0.415** 95%CI [+0.244, +0.561]
- cross **lag 크기 rank** HSPC×gastrulation (shared 111): **+0.028** 95%CI [-0.165, +0.224]
  - ⚠️ mouse→human은 uppercase ortholog 매핑(E18 전례). 누락분은 noise만 더해 결론에 보수적.

- per-gene 불일치 median — **lag 0.307** (n=969, vs MultiVeloVAE (**치환** — MoFlow arm 부재, R4에 사전 선언)) vs **α 0.052** (n=969, MV×VAE)
  - 불일치 = |정규화 rank_A − rank_B| (HSPC 원정의). HSPC 기준: lag 0.317 vs α 0.078.

## 봉인된 예측 채점

| # | 예측 | 사전 임계 | 실측 | 판정 |
|---|---|---|---|---|
| 1 | within cross-method α 재현 | ρ ≥ 0.50 | median **+0.927** (floor×MV +0.91, floor×VAE +0.93, MV×VAE +0.95) | ✅ PASS |
| 2 | within cross-method lag 재현 | ρ ≤ 0.15 | **-0.026** | ✅ PASS |
| 3 | α > lag 순서 | Δρ ≥ 0.35 | **+0.979** | ✅ PASS |
| 4 | cross HSPC↔gastrulation | cross α > +0.20 且 > cross lag | α **+0.415** / lag **+0.028** | ✅ PASS |
| 5 | per-gene 재현 격차 | lag 불일치 > α 불일치 | **0.307** vs **0.052** | ✅ PASS |
| 6 | priming 극대에서도 fragile | #2 且 #3 | — | ✅ PASS |

**종합: 6 PASS / 0 FAIL / 0 N/A**

## caveat
- replication 1건 — 강한 일반화 금지. 5축(HSPC + 4 external) 순서 일관성으로만 서술.
- cross-dataset은 uppercase ortholog(mouse→human) — 불완전 매핑, 결론에 보수적.
- lag은 크기 rank만 비교(방향 아님): MultiVelo 부호는 구조적 양수(무정보).
- concordance는 *전역* per-gene fit rank(within-lineage 아님).
