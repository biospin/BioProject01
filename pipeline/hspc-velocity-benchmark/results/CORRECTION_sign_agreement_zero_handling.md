# 정정 — 방향 sign-agreement의 "0=미정" 처리 결함 (2026-07-19)

> 발견 경위: 블로그 8편 content-fidelity-auditor가 `per_gene_direction_summary.md`(44.2/55.0/44.0)와 `two_mechanisms_classification.md`(32.4/48.1/38.6)가 **같은 n에서 다른 일치율**을 보고한다고 지적 → 원인 추적.

## 문제
`cs_lag_median`에 **정확히 0인 값이 다수** 존재한다(MoFlow 76/636, CRAK-Velo 135/868; MoFlow×CRAK 공유 330개 중 **91개**가 한쪽 이상 0). 0은 **방향 미정**인데, 두 계산이 이를 서로 다르게 강제 분류했다:
- `np.sign(x)==np.sign(y)` (p3_concordance.py, `concordance.md`, `FINDINGS.md`, 그리고 draft 본문의 "48%"): sign(0)=0을 **제3의 범주**로 취급 → 0과 양수/음수는 항상 불일치 → **일치율이 깎인다**.
- `(x>0)==(y>0)` (`p8_per_gene_direction_table.py`, `per_gene_direction_summary.md`): 0을 **RNA-first로 밀어 넣음** → 일치율이 **부풀려진다**.
- 확인: 0이 하나도 없는 `cs_lag_mean`에서는 두 방식이 **41.2%로 동일**하다. 즉 차이는 전적으로 0 처리 아티팩트다.

## 정정된 값 (0 = 방향 미정으로 **제외**, 이항검정 vs 50%)
| 쌍 | 기준 | 제외 후 n | 일치율 | 이항 p |
|---|---|---|---|---|
| MoFlow × CRAK-Velo | cs_lag_median | 239 (91 제외) | **42.3%** | 0.020 (우연보다 **낮음**) |
| MoFlow × MultiVeloVAE | cs_lag_median | 560 (76 제외) | **54.6%** | 0.031 |
| CRAK-Velo × MultiVeloVAE | cs_lag_median | 277 (57 제외) | 46.6% | 0.279 (n.s.) |
| MoFlow × CRAK-Velo | cs_lag_mean | 330 | 41.2% | 0.002 |
| MoFlow × MultiVeloVAE | cs_lag_mean | 636 | 53.6% | 0.074 |
| CRAK-Velo × MultiVeloVAE | cs_lag_mean | 334 | 49.4% | 0.870 (n.s.) |

## 결론에 미치는 영향 — **정성적 결론은 불변, 숫자는 정정 필요**
- **불변**: 전 쌍이 우연(50%)에서 ±9%p 이내이고 한 쌍은 유의하게 *아래*다. **per-gene 방향은 method 간에 재현되지 않는다**는 결론은 0 처리 방식과 무관하게 견고하다.
- **정정 필요**: 
  - draft 본문의 *"MoFlow versus MultiVeloVAE sign-agreement was 48%, i.e. chance"* → 0(미정) 제외 시 **54.6%(n=560, 이항 p=0.031)**. "정확히 우연"이라는 표현은 부정확하며, "우연에 가깝고 사용 가능한 수준과 거리가 멀다"로 바꾼다.
  - `two_mechanisms_classification.md`(32.4/48.1/38.6)와 `per_gene_direction_summary.md`(44.2/55.0/44.0)는 **둘 다 0 처리를 명시하지 않은 값**이므로 위 표로 대체하고 처리 방식을 명기한다.
  - 블로그 8편이 인용한 32.4/48.1/38.6도 동일 정정 대상.

## 후속 (권고, 미실행)
- `scripts/p3_concordance.py`의 sign-agreement 계산에 **0=미정 제외**를 명시적으로 추가하고 제외 개수를 함께 보고하도록 수정. 이는 `concordance.md`·`FINDINGS.md` 재생성으로 이어지므로 검증 게이트와 함께 처리해야 한다(이번 정정에서는 문서에 정정값을 명기하는 데 그치고 스크립트는 건드리지 않았다).
- 근본적으로 **DTW median lag이 정확히 0을 자주 산출**한다는 사실 자체가 방향 지표의 해상도 한계를 보여주는 부수 관찰이다(미정 비율 MoFlow 12%·CRAK 16%).
