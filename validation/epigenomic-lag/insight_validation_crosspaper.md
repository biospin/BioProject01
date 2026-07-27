# Cross-Paper Insight Validation — epigenomic lag (CI-01~CI-08)

- Owner: jmryu
- Issue: BIOP01-19 산출물에 대한 검증 (BIOP01-12 체계 적용)
- 검증 대상: `analysis/epigenomic-lag/_evidence/week2/insight.md`의 Insight 목록
- 근거: `evidence_bundle.md` (E-01~E-15) 및 각 논문 `full.md`
- 작성일: 2026-07-27

## Summary

cross-paper insight 8건을 6기준(Evidence/Logic/Scope/Novelty/Actionability/Risk)으로 검증했다.
**Valid 4건, Overstated 2건, Needs Evidence 1건, Rejected 1건.** (CI-07은 2차 문헌 조사 후 Valid → Overstated 하향)

가장 중요한 결과는 **CI-02가 Rejected**라는 점이다. "두 후속 논문의 비판 방향이 정반대"라는 주장이 근거를 다시 읽으면 성립하지 않고, 오히려 **같은 방향**을 가리킨다. 아래 §CI-02에 상세를 적었고 `insight.md`를 정정했다.

## 6기준 판정표

| ID | Evidence | Logic | Scope | Novelty | Actionability | Risk |
|---|---|---|---|---|---|---|
| CI-01 | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| CI-02 | ✅ | ❌ | ✅ | ✅ | ⚠️ | ❌ |
| CI-03 | ✅ | ⚠️ | ⚠️ | ✅ | ✅ | ⚠️ |
| CI-04 | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| CI-05 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CI-06 | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| CI-07 | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| CI-08 | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ |

## Validation 결과

| ID | Insight | Status | Reason | Evidence | Risk / Next Check |
|---|---|---|---|---|---|
| CI-01 | timing 연구가 discrete ordering → continuous factor → 시간축 제거된 signed lag 방향으로 확장됐다 | **Needs Evidence** | 세 논문의 개별 특성은 정확하나, 이를 "모델이 부과하는 시간 구조를 걷어내는" 단일 축으로 묶는 것은 서사다. MultiVeloVAE는 gene-specific time을 shared time으로 바꿔 **시간 구조를 오히려 강화**한 측면이 있어 축 위에 깔끔히 놓이지 않는다. | E-01, E-02, E-03. MultiVelo discrete 4-state + gene-specific latent time / MultiVeloVAE `kappa`·`delta` + shared latent time / MoFlow latent time 제거 + local relay | 논문 3편·시점 3개로 field trend를 주장하는 것은 표본이 얇다. velocity method를 10편 이상으로 확장해 재검토해야 한다. braveji 발표가 같은 축을 제시했으나 **동일 3편에서 도출**된 것이라 독립 근거가 아니다. |
| CI-02 | MultiVeloVAE와 MoFlow가 latent time fitting을 문제 삼는 방향이 정반대다 | **Rejected** | 근거를 다시 읽으면 **같은 방향**이다. MoFlow가 지적한 "canonical order로 정렬"은 chromatin이 RNA를 선행하는 방향, 즉 priming 방향이다. MultiVeloVAE가 지적한 "priming 과잉 배정"도 같은 방향이다. 두 논문 모두 MultiVelo fitting이 **priming/canonical 신호를 과다 생성**한다고 말한다. | MoFlow Figure 3f-g: gene-specific latent time에서 negative lag 소멸 → canonical order 정렬 / MultiVeloVAE Figure 3f: MultiVelo가 IRS lineage 전체를 priming으로 오판 | 정정판(CI-02R)으로 대체했다. "방향이 반대"가 아니라 "두 독립 논문이 같은 편향을 서로 다른 증상으로 관찰"이 옳으며, 이쪽이 오히려 근거가 강하다. |
| CI-03 | 동일 dataset의 동일 gene(`Wnt3`)에 대해 세 논문의 판정이 갈린다 | **Overstated** | 세 논문이 `Wnt3`를 다룬 것과 서술이 다른 것은 사실이다. 그러나 **평가 대상이 서로 다르다.** MoFlow는 gene-wise velocity **방향**을, MultiVeloVAE는 priming의 **lineage 배정**을 평가한다. 방향은 맞히면서 lineage 배정을 틀릴 수 있으므로 논리적 모순이 아니다. "불일치"라는 표현이 근거를 넘는다. | MultiVelo Figure 4d-f (induction-only priming, max `c-s` delay 0.6) / MultiVeloVAE Figure 3f / MoFlow Figure 5d-e (`Wnt3`·`Trps1`은 양쪽 다 양호, 실패 gene은 `Padi3`·`Myo10`·`Notch1`) | "서술이 갈린다"까지만 주장하고 "모순"은 빼야 한다. 동일 기준(같은 metric)으로 `Wnt3`를 재평가하기 전에는 판정 불가. 원 insight의 "평가 기준이 달라 결정 불가"라는 단서는 유지되므로 폐기가 아니라 표현 조정 대상이다. |
| CI-04 | negative `c-s` lag가 biological signal인지 method artifact인지 분리되지 않았고 양쪽 다 ground truth가 없다 | **Valid** | 저자 스스로 open question으로 제기한 내용이며, 여기에 "MultiVelo fitting은 이 신호를 지운다"는 cross-paper 관찰이 더해진다. 과장 없이 불확실성을 그대로 기술한다. | MoFlow Figure 3f-g (400개 초과 gene ≥25% bin, 129개 gene >75% bin sign reversal), Figure 7 (NIH3T3 half-life), MoFlow open question 3 | Novelty가 부분적이다. MoFlow의 open question을 상당 부분 재진술한다. 고유 기여는 "MultiVelo 쪽도 ground truth가 없다"는 대칭성 지적에 한정된다. |
| CI-05 | perturbation 부재·wall-clock 부재·gene-level aggregation·benchmark 불일치가 3편 전부의 구조적 한계다 | **Valid** | 4개 항목 각각이 3편 모두에서 저자 또는 분석자 진술로 확인된다. 예외(MultiVeloVAE의 wall-clock 부분 진전)를 별도 표기해 과잉 일반화를 피했다. | E-10, E-11, E-12, E-14. 각 항목이 논문별 `full.md`의 "저자가 명시한 한계" 또는 "분석자가 판단한 한계"에 대응 | 3편 표본에서 "field 구조적 한계"로 승격하는 것은 여전히 확대다. 다만 네 항목 모두 예외 없이 관찰돼 개별 논문 약점보다는 공통 조건일 개연성이 높다. |
| CI-06 | uncertainty 부재는 3편 공통이 아니다. MultiVeloVAE가 해결했으나 `c-s` lag 자체의 credible interval은 3편 중 없다 | **Valid** | 반증 사례를 명시적으로 제시하는 형태의 주장이며 근거가 직접적이다. 통설(3편 공통 한계) 정정으로서 가치가 있다. | MultiVeloVAE Figure 3e (cell-state uncertainty), Figure 5e (posterior-sampled dynamics + credible interval), Figure 6 (Bayes factor) / MultiVelo·MoFlow 해당 기능 없음 | 후반부 주장은 다소 형식적이다. MultiVeloVAE는 DTW `c-s` lag를 **산출하지 않으므로**(연속 factor `delta` 사용) credible interval이 없는 것이 당연하다. "lag 추정에 불확실성을 붙인 논문이 없다"로 읽어야 의미가 있다. |
| CI-07 | 세 논문 모두 lag를 output으로만 다루고 예측 대상으로 두지 않았다. baseline feature → lag 예측은 scope 내 선례가 없다 | **Overstated** *(2차 검증에서 하향)* | 1차에서는 범위를 3편으로 명시한 점을 들어 Valid로 뒀으나, scope 밖 문헌 조사 결과 Ma et al.(SHARE-seq)·COPI·SCARlink 등 **선례가 존재**한다. "본 3편에 없음"은 참이지만 이를 G-2의 novelty 근거로 확장한 부분이 과하다. | E-15 + 2차 조사(아래 §CI-07 재검증) | signed per-gene lag **magnitude**를 회귀 target으로 둔 사례는 미확인이므로 축소판은 살아남는다. G-4(lag 부호의 method 의존성) 선결 조건도 유효하다. |
| CI-08 | MultiVeloVAE는 같은 연구실 자기 후속, MoFlow는 독립 그룹이므로 동일 비판이라도 증거 무게가 다르다 | **Valid** | 저자 명단 대조로 직접 확인되는 사실이며, 자기비교 편향은 표준적인 방법론적 고려사항이다. | MultiVelo(Chen Li, Virgilio, Collins, Welch) ∩ MultiVeloVAE(Chen Li, Gu, Virgilio, Lee, Collins, Welch) = 4인 / MoFlow(Ari Hong, Sangseon Lee, Kwangsoo Kim) ∩ 나머지 = 0인 | Novelty가 낮다. paper-network가 통상 수행하는 계보 분석에 해당한다. 다만 CI-02R의 신뢰도를 뒷받침하는 전제로 기능하므로 유지 가치가 있다. |

## 정정판

원 insight를 대체한다.

| ID | Insight | 근거 |
|---|---|---|
| **CI-02R** | MultiVeloVAE와 MoFlow는 저자가 겹치지 않는 독립적 관찰에서, MultiVelo의 gene-specific latent time fitting이 **priming/canonical 방향 신호를 과다 생성**한다는 동일한 편향을 서로 다른 증상으로 지적한다. MultiVeloVAE는 priming lineage 과잉 배정으로, MoFlow는 non-canonical lag의 소거로 나타난다. | E-07, E-08, CI-08 |

CI-02R은 원 CI-02보다 **근거가 강하다.** 두 독립 그룹이 같은 결론에 도달한 것이 서로 다른 결론을 낸 것보다 증거력이 높기 때문이다. 원 주장은 대비를 만들려다 근거를 잘못 읽은 사례다.

## 토론 준비

1. **가장 설득력 있는 insight**: CI-05. 4개 항목 각각이 3편 모두에서 저자 또는 분석자 진술로 직접 확인되며 예외를 명시했다.
2. **근거 부족/과장**: CI-02(Rejected)와 CI-03(Overstated). 둘 다 **논문 간 대비를 만들려는 압력**에서 나왔다. cross-paper insight를 뽑을 때 "차이"를 찾으려는 편향이 작동한다는 점이 이번 검증의 가장 큰 교훈이다.
3. **Validation Agent 필수 기준**: Logic이 결정적이었다. CI-02는 Evidence가 ✅였는데도 Rejected다. 근거 문장이 실재하는 것과 그 문장들이 주장한 관계를 지지하는 것은 별개이며, Evidence만 통과시키면 잡히지 않는다.
4. **결과가 서로 다를 때**: 두 논문이 같은 대상을 평가했는지 먼저 확인해야 한다. CI-03은 이 확인을 건너뛰어 서로 다른 속성에 대한 서술을 "모순"으로 읽었다.
5. **출력 형식**: week3의 7열 표(`ID / Paper / Insight / Status / Reason / Evidence / Risk`)를 유지하되, cross-paper insight는 Paper 열이 다수라 6기준 판정표를 별도로 두는 편이 읽기 쉽다.

## CI-07 재검증 — scope 밖 문헌 조사 결과 (2026-07-27, 2차)

1차 검증에서 CI-07을 `Valid`로 두면서 "novelty 주장으로 쓰려면 scope 밖 문헌 조사가 필수"라고 단서를 달았다. 조사를 수행한 결과 **선례가 존재하며, CI-07을 `Overstated`로 하향한다.**

### 발견된 선례

| 연구 | 무엇을 했나 | G-2와의 거리 |
|---|---|---|
| **Ma et al., SHARE-seq** (Cell, 2020) | `Wnt3` DORC에서 enhancer peak → promoter → nascent RNA → mature RNA의 **순차적 활성화 시점**을 추적하고 accessibility onset과 expression onset 사이 lag를 **0.20 / 0.13 pseudotime unit**으로 정량화. chromatin potential을 lineage-priming의 정량 지표로 삼아 cell fate를 예측 | 가장 가깝다. lag를 정량화하고 예측에 사용했다. 다만 예측 대상은 **cell fate**이지 lag 자체가 아니다 |
| **COPI** (Cell Reports, 2020) | promoter accessibility에서 Chromatin Opening Potential Index를 계산해 gene의 **transcription potential**을 점수화. 부분적으로 열린 promoter를 가진 poised gene을 식별 | baseline chromatin에서 "앞으로 켜질 gene"을 예측한다. G-2의 문제 설정과 구조가 같다 |
| **SCARlink** (Nat Genet, 2024) | tile 단위 accessibility에서 regularized Poisson regression으로 single-cell expression을 예측하고, 예측/관측 차이로 **chromatin potential vector field**를 산출. mouse skin·BMMC·pituitary·developing human cortex에 적용 | baseline chromatin → expression 회귀는 확립돼 있다. dataset도 본 scope 3편과 겹친다 |
| splicing kinetics 예측 (bioRxiv, 2021) | 92개 sequence feature, 120개 RBP feature 등에서 random forest로 **splicing kinetic rate**를 예측 | target이 lag는 아니지만 "feature → kinetic parameter 회귀"라는 문제 형태가 동일하다 |

### 판정

**CI-07 → `Overstated`.** 원 문장은 "본 scope 3편 기준"으로 범위를 명시했으므로 문자 그대로는 여전히 참이다. 그러나 이를 `insight.md` §4 G-2에서 "프로젝트 핵심 novelty 후보"로 확장한 부분이 근거를 넘는다. baseline epigenomic feature에서 timing/potential을 예측하는 문제는 **이미 여러 형태로 시도됐다.**

살아남는 축소판은 다음과 같다.

> **signed per-gene lag magnitude**를 회귀 target으로 직접 예측한 사례는 확인되지 않았다. 기존 연구는 (a) lag를 기술 통계로 정량화하거나(Ma et al.), (b) 활성화 여부·potential을 점수화하거나(COPI), (c) expression level을 예측한다(SCARlink). lag의 **크기와 부호**를 예측 대상으로 둔 설정은 별개다.

이 축소판도 novelty로 쓰려면 추가 검증이 필요하다. 위 조사는 웹 검색 기반이며 체계적 문헌 조사가 아니다.

### G-3도 정정 대상

`insight.md` §4에서 **G-3(enhancer/peak-level lag resolution)을 "선례 없음"** 으로 적었으나 **틀렸다.** Ma et al.은 `Wnt3` DORC에서 개별 enhancer peak가 promoter보다 먼저 활성화되는 순서를 이미 추적했다. enhancer 단위 timing 분석의 선례가 존재한다.

### scope 설계 결함

`scope.md`는 SHARE-seq 원 논문(Ma et al.)을 "velocity model을 제안하지 않음(포함 기준 3 미충족)"으로 제외했다. velocity method 비교에는 타당한 기준이었으나, 그 결과 **gap 분석에서 가장 중요한 선례를 시야에서 제거**했다. 세 논문 모두 이 논문의 `Wnt3` 분석을 재현 대상으로 삼고 있었는데도 그렇다.

교훈: 포함/제외 기준을 method 비교 목적으로 세우면 Unresolved Gaps 섹션의 "선례 없음" 판정이 구조적으로 편향된다. **gap 판정은 scope 밖 문헌까지 확인한 뒤 내려야 한다.**

## Next Work

- CI-01: velocity method를 10편 이상으로 확장해 field flow 축 재검토
- CI-03: 동일 metric으로 `Wnt3` 재평가, 또는 "서술 차이"까지로 표현 축소
- CI-07: scope 밖 문헌 조사로 "baseline feature → lag 예측" 선례 확인. G-4 선결 여부 함께 판단
- 검증 결과를 `insight.md`에 반영 완료 (CI-02 → CI-02R 대체, CI-03 표현 조정)
