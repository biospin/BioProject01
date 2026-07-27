# Cross-Paper Insight — epigenomic lag

- 대상 논문: 3편 (MultiVelo 2023, MultiVeloVAE 2025, MoFlow 2026)
- 입력: `papers.jsonl`, `evidence_bundle.md`, `scope.md`
- Owner: jmryu · Issue: BIOP01-19
- 작성일: 2026-07-27

---

## 1. Field Flow

**MultiVelo (2023, Nat Biotechnol)** — chromatin accessibility `c`를 RNA velocity ODE의 시간 변수로 처음 통합했다. 핵심 기여는 성능이 아니라 **어휘**다. priming(`ti - to`)과 decoupling(`tr - tc`)이라는 구간을 정의하고, chromatin closing과 transcriptional repression의 순서로 model 1 / model 2를 나눴다. 시간축은 gene-specific latent time이고 상태는 4개 discrete state로 배정된다. [E-01]

**MultiVeloVAE (2025, Nat Commun)** — MultiVelo의 두 가지 전제를 풀었다. ① population 전체에 하나의 parameter set → cell-specific `kc`, `rho`. ② discrete state 배정 → 연속값 `kappa`(coupling), `delta = kc - rho`(decoupling). 여기에 shared latent time으로 gene 간 time 충돌을 없애고, posterior 기반 Bayesian differential testing을 추가했다. [E-02]

**MoFlow (2026, Nat Commun)** — 앞의 두 논문이 유지한 **latent time 자체를 버렸다.** cellDancer의 local relay(transcriptome-only)에 chromatin을 결합해, global 시간축 없이 local neighbor 전이만으로 cell-specific kinetics를 추정한다. 그 결과 canonical `c → u → s` 순서를 따르지 않는 **negative `c-s` lag**를 artifact가 아닌 해석 대상으로 남겼다. [E-03]

**축:** chromatin-RNA timing 연구는 `discrete state ordering → continuous decoupling factor → 시간축을 제거한 signed lag` 방향으로, 즉 **모델이 부과하는 시간 구조를 하나씩 걷어내는** 방향으로 확장되고 있다.

**계보의 성격 차이 (해석에 중요):** MultiVeloVAE는 MultiVelo와 저자 4인(Chen Li, Virgilio, Collins, Welch)이 겹치는 **같은 연구실의 자기 후속**이다. 반면 MoFlow는 저자가 전혀 겹치지 않는 **독립 그룹의 반론**이다. 따라서 "MultiVelo의 한계"라는 동일한 지적이라도 두 논문에서 무게가 다르며, 특히 MoFlow가 MultiVelo를 baseline으로 이긴 결과는 자기평가 편향에서 상대적으로 자유롭다. [E-02, E-03]

---

## 2. Differentiation Map

| Paper | Strong point | Weak point |
|---|---|---|
| **MultiVelo** | 개념적 foundation(priming/decoupling/model 1·2), 4개 대형 multiome dataset, disease SNP timing까지 확장 | 시간축·상태가 모두 고정, uncertainty 없음, 정량 우위 근거가 Spearman 1건뿐 |
| **MultiVeloVAE** | 유일하게 uncertainty·differential testing 제공, multi-sample/partial modality 지원, RNA-only에서도 동작 | lag를 직접 산출하지 않음(연속 factor로 대체), exact benchmark value가 본문에 거의 없음 |
| **MoFlow** | signed lag 해석이 가장 직접적, latent time 가정 제거, CBDir 정량 우위 명시 | gene-wise scope(pathway-level 불가), half-life 해석이 외부 cell line 의존, uncertainty 없음 |

### 같은 dataset, 다른 결론

세 논문은 dataset이 크게 겹친다 — SHARE-seq mouse skin, E18 mouse brain, human HSPC, 발달기 human brain을 모두 공유한다. 그런데 겹치는 지점에서 결론이 갈린다.

**① `Wnt3` 3자 불일치 — 동일 gene, 동일 dataset, 세 가지 판정** [E-07]
세 논문 모두 SHARE-seq mouse skin의 `Wnt3`를 대표 사례로 분석했다.
- MultiVelo: induction-only **priming** gene. DTW maximum `c-s` delay가 normalized time range 1 중 0.6.
- MultiVeloVAE: MultiVelo가 **IRS lineage 전체를 priming으로 잘못 해석**했다고 지적. 진짜 priming lineage와 IRS lineage를 분리해야 한다.
- MoFlow: `Wnt3`는 **MoFlow와 MultiVelo가 모두 잘 잡았다**고 평가. 문제 gene은 오히려 `Padi3`, `Myo10`, `Notch1`이며 여기서 MultiVelo가 실패한다.

즉 MultiVelo의 `Wnt3` 처리에 대해 후속 두 논문의 평가가 정반대다. 평가 기준이 각각 정량 DTW lag / lineage 분리 정확도 / gene-wise velocity 방향으로 달라서, 동일 기준 재평가 없이는 결정할 수 없다.

**② latent time fitting이 lag 부호를 뒤집는다** [E-08]
MoFlow pseudotime과 MultiVelo **global** latent time에서는 `PDGFRA`/`MAP3K1`의 negative `c-s` lag가 보이는데, MultiVelo **gene-specific** latent time에서는 그 lag가 사라지고 canonical order로 정렬된다. 400개 초과 gene이 최소 25% time bin에서, 129개 gene이 75% 초과 bin에서 sign reversal을 보였다.

MoFlow는 이를 "biological order에 맞추려는 over-correction"으로 해석한다. 그러나 반대 방향, 즉 MoFlow의 local relay가 noise를 lag로 포착했을 가능성은 배제되지 않았다. **양쪽 모두 ground truth가 없다.** 이것이 이 field에서 가장 크게 열려 있는 방법론적 분쟁이다.

**③ 두 후속 논문이 MultiVelo를 비판하는 방향이 서로 반대다**
MultiVeloVAE는 MultiVelo가 priming을 **과잉 배정**한다고 보고(Wnt3 IRS lineage), MoFlow는 MultiVelo가 non-canonical lag를 **과잉 교정**한다고 본다. 둘 다 gene-specific latent time fitting의 부작용을 지적하지만 증상이 정반대다. 이는 latent time fitting이 단일 방향 bias가 아니라 **데이터 조건에 따라 양방향으로 왜곡**될 수 있음을 시사한다.

---

## 3. Repeated Limitations

각 항목의 관찰 편수와 예외를 명시한다. 3편은 "공통"을 주장하기에 작은 표본이므로 예외를 뭉뚱그리지 않는다.

| # | 공통 한계 | 관찰된 논문 | 예외 |
|---|---|---|---|
| L-1 | **perturbation / causal validation 부재** — 모든 lag가 temporal association | 3편 전부 [E-10] | 없음 |
| L-2 | **wall-clock calibration 부재** — 모든 timing이 pseudotime 단위 | 3편 전부 [E-11] | MultiVeloVAE 부분 예외: capture time prior로 real unit 연결 가능성 언급, MEF reprogramming 0–28일 6 time point 사용. 단 lag 자체의 시간 단위 calibration은 미수행 |
| L-3 | **gene-level chromatin aggregation** — enhancer-specific timing 손실 | 3편 전부 [E-12] | 없음. MultiVeloVAE는 `summed` accessibility임을 저자가 명시, MoFlow는 long-range enhancer-promoter 미모델링을 명시 |
| L-4 | **benchmark metric 불일치** — 동일 preprocessing·metric의 통합 비교표가 어느 논문에도 없음 | 3편 전부 [E-14] | 없음 |
| L-5 | **lag 추정치의 uncertainty interval 부재** | MultiVelo, MoFlow (2편) [E-13] | **MultiVeloVAE가 해결** — posterior, credible interval, cell-state uncertainty, Bayes factor 제공 |

**L-1 ~ L-4는 개별 논문의 약점이 아니라 field 전체의 구조적 한계다.** 세 논문이 서로를 baseline으로 인용하면서도 공통 평가 기준을 만들지 않았고(L-4), 그 결과 §2의 Wnt3 불일치와 lag 부호 분쟁이 해소되지 못한 채 누적되고 있다.

**L-5는 공통 한계가 아니다.** 참고 발표자료 등에서 이를 3편 공통으로 기술한 경우가 있으나, MultiVeloVAE는 uncertainty를 명시적으로 제공하므로 사실과 다르다. 다만 MultiVeloVAE의 uncertainty는 latent state/time과 velocity에 대한 것이고, **`c-s` lag 자체에 대한 credible interval을 보고한 논문은 3편 중 하나도 없다.** 이 형태로 기술해야 정확하다.

---

## 4. Unresolved Gaps

| # | Gap | 선례 유무 | 비고 |
|---|---|---|---|
| G-1 | pseudotime → wall-clock 시간 단위 calibration | 부분적 (MultiVeloVAE capture time prior) | L-2에서 파생. lag를 시간 단위로 말하려면 선결 |
| G-2 | **baseline epigenomic feature → lag 예측** | **선례 없음 (본 scope 내)** | ★ 프로젝트 핵심 novelty 후보. 아래 상술 |
| G-3 | enhancer / peak-level lag resolution | 없음 | MultiVeloVAE open question 3번(peak-level ODE)으로만 제기됨 |
| G-4 | negative lag의 mechanism 분해 (RNA export vs nuclear capture bias vs normalization artifact) | 없음 | MoFlow open question 3번. §2-② 분쟁의 해소 조건 |
| G-5 | lag 추정의 multi-sample / multi-donor robustness | 없음 | MultiVeloVAE가 multi-sample velocity는 다루나 lag robustness는 미평가 |
| G-6 | perturbation 기반 causal 검증 | 없음 | L-1에서 파생. 세 논문 모두 후속 과제로만 언급 |

### G-2 상술 — 이 프로젝트의 핵심 novelty 후보

세 논문 모두 lag를 **model fitting의 산출물(output)** 로 다룬다. MultiVelo는 priming/decoupling interval length를, MoFlow는 DTW `c-s` lag를, MultiVeloVAE는 `delta = kc - rho`를 내놓지만, 셋 다 velocity model을 데이터에 맞춘 뒤 나오는 부산물이다.

**lag를 예측 대상(target)으로 두고, baseline 시점의 epigenomic feature에서 lag를 회귀·분류한 분석은 세 편 어디에도 없다.** [E-15]

이 전환이 의미 있는 이유는 두 가지다.
1. **실용적** — lag를 예측할 수 있으면 multi-omic 측정 없이 baseline chromatin 정보만으로 timing을 추정할 수 있다. BIOP01의 "Epigenetic Therapy 기반 response time 예측" 방향과 직접 연결된다.
2. **방법론적** — 예측 과제는 held-out 평가를 강제한다. 이는 L-4(benchmark metric 불일치)와 L-5(uncertainty 부재)를 우회하는 경로가 된다. lag를 맞히는지 여부는 velocity model 간 우열 논쟁과 독립적으로 채점 가능하다.

**단, 선결 조건이 있다.** §2-②에서 확인했듯 lag 부호 자체가 method에 따라 뒤집힌다. 예측 target이 method artifact라면 예측 성능은 무의미하다. 따라서 **G-4(lag mechanism 분해)가 G-2의 선결 과제**이며, 최소한 MultiVelo와 MoFlow 두 method에서 동시에 재현되는 lag만 target으로 삼는 등의 방어가 필요하다.

**선례 없음의 범위:** 본 분석은 selected 3편 기준이다. scope 밖 literature에 선례가 있을 가능성은 배제하지 못한다. novelty 주장 전에 별도 문헌 조사가 필요하다.

---

## Insight 목록 (validation 입력용)

`claim-verify` 또는 Validation Agent가 그대로 받을 수 있는 형식. 근거 ID는 `evidence_bundle.md` 참조.

| ID | Insight | 관련 논문 | 근거 ID |
|---|---|---|---|
| CI-01 | chromatin-RNA timing 연구는 discrete ordering → continuous factor → 시간축 제거된 signed lag 순으로, 모델이 부과하는 시간 구조를 걷어내는 방향으로 확장됐다 | 3편 | E-01, E-02, E-03 |
| CI-02 | MultiVeloVAE와 MoFlow는 모두 gene-specific latent time fitting을 문제 삼지만 지적 방향이 정반대다(priming 과잉 배정 vs lag 부호 과잉 교정). latent time 왜곡은 단일 방향 bias가 아니다 | 3편 | E-07, E-08 |
| CI-03 | 동일 dataset의 동일 gene(`Wnt3`)에 대해 세 논문의 판정이 갈리며, 평가 기준이 서로 달라 현재 근거로는 결정 불가하다 | 3편 | E-07 |
| CI-04 | negative `c-s` lag가 biological signal인지 method artifact인지 분리되지 않았고, 양쪽 모두 ground truth가 없다 | MoFlow, MultiVelo | E-08, E-09 |
| CI-05 | perturbation validation 부재·wall-clock 부재·gene-level aggregation·benchmark 불일치는 3편 전부에서 관찰되는 field의 구조적 한계다 | 3편 | E-10, E-11, E-12, E-14 |
| CI-06 | uncertainty 부재는 3편 공통이 아니다. MultiVeloVAE가 해결했으나, `c-s` lag 자체에 credible interval을 보고한 논문은 3편 중 없다 | 3편 | E-13 |
| CI-07 | 세 논문 모두 lag를 model fitting의 output으로만 다루고 예측 대상으로 두지 않았다. baseline epigenomic feature → lag 예측은 본 scope 내 선례가 없다 | 3편 | E-15 |
| CI-08 | MultiVeloVAE는 같은 연구실 자기 후속이고 MoFlow는 독립 그룹 반론이므로, 동일한 MultiVelo 비판이라도 증거 무게가 다르다 | 3편 | E-02, E-03 |

### 3주차 검증 결과(I-01~I-06)와의 관계

week3 `validation/epigenomic-lag/insight_validation_week3.md`의 I-01~I-06은 **논문별 insight**(각 논문이 무엇을 보였는가)였다. 위 CI-01~CI-08은 **논문 간 관계**에서만 성립하는 insight로, 서로 대체 관계가 아니라 층이 다르다.

정합성 확인 결과:
- I-01(MultiVelo chromatin 통합), I-03(MoFlow local relay), I-05(MultiVeloVAE continuous rate)는 CI-01의 Field Flow 세 마디에 각각 대응한다. 모순 없음.
- I-02·I-04·I-06이 공통으로 지목한 "perturbation 없이는 causal로 확장 불가"는 CI-05의 L-1과 동일한 관찰이다. 독립 도출 후 일치.
- I-04(negative `c-s` lag는 biological signal일 수 있음, Status `Needs Evidence`)는 CI-04로 확장된다. week3는 근거 부족만 지적했으나, CI-04는 **method artifact 가능성**이라는 구체적 대안 가설을 추가한다.
- **week3에 없던 항목:** CI-02, CI-03, CI-08. 특히 `Wnt3` 3자 불일치(CI-03)와 latent time 양방향 왜곡(CI-02)은 단일 논문 분석에서는 보이지 않는 지점이다.

CI-01~CI-08은 아직 검증 전이다. Validation Agent 입력으로 넘긴다.
