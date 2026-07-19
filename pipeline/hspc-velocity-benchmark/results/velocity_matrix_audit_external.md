# 층② velocity 행렬 불일치의 외부 재현 (BIOP01-60)

> 2026-07-19. 사전등록 = `manuscript/PREREGISTRATION_velocity_matrix.md` **부록**(외부 데이터를 열기 전에 봉인).
> 실행 = `scripts/p10c_velocity_matrix_external.py`. 지표·제외규칙은 HSPC 본편(`p10`)과 **동일**하다 — 외부에 맞춰 정의를 바꾸지 않았다.
> 추가 fit 없음. 이미 fitting돼 있던 arm만 사용.

## 0. 한 줄

**재현됐다 (4/4).** HSPC에서 본 순서 — *multiome 방법끼리의 일치가 크로마틴을 안 쓰는 RNA-only 기준선을 넘지 못한다* — 가 외부 네 시스템 전부에서 반복됐고, 네 곳 모두 paired Δ의 95% CI가 0을 배제했다.

## 1. 판정 — **REPLICATED** (사전등록 부록 §E: 4개 중 3개 이상)

주 판정 지표는 봉인된 규약(§2-4)대로 **원척도 코사인**이다. 중심화는 보조로 함께 싣는다.

| 시스템 | arm | 세포 | 사용 유전자 | MM | M-RNA | **paired Δ [95% CI] (원척도)** | 판정 | Δ (중심화) |
|---|---|---|---|---|---|---|---|---|
| gastrulation (GSE205117, mouse) | 4 | 10,779 | 847 | +0.060 | +0.189 | **−0.159** [−0.162, −0.156] | ✅ | −0.172 |
| macrophage | 3 | 3,572 | 702 | +0.280 | +0.432 | **−0.152** [−0.170, −0.134] | ✅ | −0.407 |
| BMMC (GSE194122) | 3 | 2,850 | 232 | −0.055 | +0.235 | **−0.289** [−0.300, −0.278] | ✅ | −0.281 |
| E18 mouse brain | 3 | 4,423 | 973 | +0.108 | +0.268 | **−0.184** [−0.191, −0.176] | ✅ | −0.182 |
| *(참고) HSPC 본편* | 5 | 21,878 | 354 | *−0.139* | *+0.080* | *−0.206* [−0.207, −0.205] | *기준* | — |

Δ = (multiome×multiome 평균) − (multiome×RNA-only 평균), 세포 단위 paired 부트스트랩 B=1,000, seed 20260719. **네 시스템 모두 음수이고 CI가 0을 배제한다.** 반대 방향(Δ가 유의하게 양수)인 시스템은 **0/4**. 원척도와 중심화 **두 지표에서 각각 4/4로 같은 판정**이 나와, 결론이 지표 선택에 의존하지 않는다.

> **규약 이탈 기록(자체 발견·정정).** 최초 실행은 중심화 코사인을 주 판정에 썼다. 봉인된 §2-4는 주 분석을 **원척도**로, 중심화는 사후 진단으로 정해 두었으므로 이는 규약 이탈이다. 결과를 보기 전 정의를 바꾸는 대신, **원척도로 다시 판정하고 중심화를 보조로 내렸다.** 두 지표의 판정이 같아 결론은 바뀌지 않았지만, 바뀌었더라도 원척도를 따랐을 것이다. 정정 전 중심화 기준 값도 위 표 마지막 열에 그대로 남긴다.

## 2. 쌍별 중심화 코사인 — 어디서나 최상위가 RNA-only 짝이다

| 시스템 | 쌍 | 종류 | 중심화 | 부호 일치 |
|---|---|---|---|---|
| gastrulation | MultiVelo × MoFlow | MM | −0.000 | 50.5% |
| gastrulation | MultiVelo × MultiVeloVAE | MM | +0.240 | 54.4% |
| gastrulation | MoFlow × MultiVeloVAE | MM | +0.001 | 49.6% |
| gastrulation | **MultiVelo × scVelo(RNA)** | M-RNA | **+0.432** | 60.2% |
| gastrulation | MoFlow × scVelo(RNA) | M-RNA | −0.001 | 48.2% |
| gastrulation | MultiVeloVAE × scVelo(RNA) | M-RNA | +0.239 | 59.4% |
| macrophage | MultiVelo × MultiVeloVAE | MM | −0.166 | 57.3% |
| macrophage | **MultiVelo × scVelo(RNA)** | M-RNA | **+0.578** | 64.9% |
| macrophage | MultiVeloVAE × scVelo(RNA) | M-RNA | +0.027 | 65.9% |
| BMMC | MultiVelo × MultiVeloVAE | MM | −0.110 | 61.0% |
| BMMC | **MultiVelo × scVelo(RNA)** | M-RNA | **+0.392** | 69.3% |
| BMMC | MultiVeloVAE × scVelo(RNA) | M-RNA | −0.015 | 74.7% |
| E18 brain | MultiVelo × MultiVeloVAE | MM | +0.108 | 55.6% |
| E18 brain | **MultiVelo × scVelo(RNA)** | M-RNA | **+0.283** | 63.1% |
| E18 brain | MultiVeloVAE × scVelo(RNA) | M-RNA | +0.243 | 59.9% |

두 가지가 눈에 띈다.

1. **다섯 시스템 전부에서 최상위 쌍이 `MultiVelo × scVelo(RNA-only)`다** (HSPC +0.583 · gastrulation +0.432 · macrophage +0.578 · BMMC +0.392 · E18 +0.283). HSPC 본편에서 한 시스템 관찰로만 적었던 것이 **5/5로 반복된다.** 단 이는 MultiVelo에 붙는 진술이지 multiome 계열의 성질이 아니다(§4 경합 설명 참조).
2. **MoFlow는 어느 쪽과도 안 맞는다.** gastrulation에서 MultiVelo −0.000, MultiVeloVAE +0.001, scVelo −0.001, 부호 일치 48~51%. HSPC에서 본 것과 같다(MoFlow의 모든 쌍이 ~0).

## 3. ★ 재현할 수 **없는** 것 — 사전등록 §D대로

- **인과 대조(ATAC-shuffle)는 외부에서 재현 불가.** 외부에 scrambled arm이 없다. **크로마틴이 행렬에 인과적으로 무력하다는 결론은 HSPC·MultiVelo 한정으로 남는다.** 이번 재현이 넓힌 것은 *방법 간 불일치* 쪽이지 *인과* 쪽이 아니다.
- **시스템별 재현성 천장을 못 잰다.** 외부에 bootstrap refit이 없다. HSPC 천장(중심화 +0.872)을 참조로 쓰되 **시스템마다 천장이 다를 수 있다**. 따라서 외부 수치는 "천장 대비 얼마나 낮은가"가 아니라 **기준선 대비 순서**로만 읽는다 — 판정 기준을 Δ 하나로 잡은 이유가 이것이다.
- macrophage·BMMC·E18은 multiome arm이 2개뿐이라 multiome×multiome 쌍이 **각 1개**다. multiome끼리의 불일치를 이 세 시스템에서 "여러 쌍으로" 확인한 것은 아니다. 3쌍을 가진 시스템은 gastrulation뿐.

## 4. 경합 설명 (숨기지 않고 적는다)

`MultiVelo × scVelo` 가 어디서나 최상위인 데에는 **"살아남는 건 RNA 성분이다"** 말고 다른 설명이 있다. 두 방법은 **모델 형태가 가깝다** — 둘 다 같은 Ms/Mu 위에서 고전적 ODE 잔차 형태로 velocity를 만든다. 반면 MultiVeloVAE와 MoFlow는 신경망 기반이다. 그렇다면 이 일치는 *공유된 RNA 정보* 때문일 수도, *공유된 모델 형태* 때문일 수도 있고 **이 설계로는 둘을 나눌 수 없다.**

이 경합이 결론을 흔드는가: **흔들지 않는다.** 사전등록한 판정 대상은 "multiome끼리가 기준선을 넘는가"이고 그 답은 5/5로 아니오다. 어느 설명을 택하든 **multiome 방법들이 서로 재현하지 않는다**는 사실은 그대로다. 다만 "재현되는 건 RNA 쪽"이라는 *해석*은 이 경합 때문에 **여전히 승격하지 않는다.**

## 5. 이게 논문에서 하는 일

- 층② 결과가 **HSPC 단일 시스템에서 5개 시스템**으로 올라간다. 논문의 나머지 결론(α-강건·lag-취약 순서가 6개 시스템에서 유지)과 **같은 골격**을 쓰게 된다.
- 리뷰어의 "n=1 시스템" 지적이 닫힌다.
- **헤드라인 승격은 여전히 없다.** supporting 등급 유지.
- 인과 결론의 범위 제한(HSPC·MultiVelo)은 **오히려 더 또렷하게 적어야 한다** — 재현된 것과 재현되지 않은 것이 이제 명확히 갈리기 때문이다.

## 산출물
`results/velocity_matrix_audit_external_pairs.csv` · `results/velocity_matrix_audit_external.json` · `scripts/p10c_velocity_matrix_external.py`
