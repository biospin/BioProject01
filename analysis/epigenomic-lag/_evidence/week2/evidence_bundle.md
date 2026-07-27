# Evidence Bundle — epigenomic lag

`insight-agent` 입력용 근거 묶음. 모든 항목은 각 논문 `full.md`에서 확인된 내용이며, caveat은 `full.md`의 "해석 시 주의점" 및 "분석자가 판단한 한계"에서 가져왔다.

## A. Method 계보 근거

**E-01 — MultiVelo가 chromatin을 velocity ODE의 시간 변수로 통합**
- 논문: MultiVelo
- 관찰: `c`, `u`, `s`를 하나의 ODE system으로 묶고 latent time, switch time, rate parameter, state를 동시 추정. priming = `ti - to`, decoupling = `tr - tc`로 정량화.
- 근거: Figure 1a-g. mouse brain median primed interval 21%, decoupled interval 19%.
- Caveat: Figure 1은 model assumption과 simulated behavior 설명이므로 실제 biological frequency는 dataset 결과로 확인해야 한다.

**E-02 — MultiVeloVAE가 discrete state를 continuous factor로 일반화**
- 논문: MultiVeloVAE
- 관찰: MultiVelo의 primed/coupled/decoupled discrete 배정을 `kappa`(coupling), `delta = kc - rho`(decoupling)라는 cell-specific 연속값으로 대체. shared latent time으로 gene별 time 충돌을 제거.
- 근거: Figure 1a-b, Figure 5a-b. 저자가 MultiVelo의 한계를 "population 전체에 하나의 parameter set, discrete state 배정"으로 명시.
- Caveat: 저자 4인이 MultiVelo와 겹친다(Chen Li, Virgilio, Collins, Welch). 같은 연구실의 자기 후속이므로 비교가 독립적이지 않다.

**E-03 — MoFlow가 latent time 자체를 제거**
- 논문: MoFlow
- 관찰: global latent time과 fixed gene class 없이 local neighbor를 짧은 시간 뒤 future state로 보고 cosine distance를 줄이는 relay 방식. chromatin opening(`k=1`)/closing(`k=0`)을 모두 평가해 낮은 angular error를 선택.
- 근거: Figure 1a-c.
- Caveat: 저자진(Ari Hong, Sangseon Lee, Kwangsoo Kim)이 MultiVelo/MultiVeloVAE와 완전히 겹치지 않는 독립 그룹이다. 반면 chromatin state `k` 선택이 angular error 기반이라 실제 chromatin remodeling event의 직접 관측은 아니다.

## B. 성능 비교 근거

**E-04 — MultiVelo의 정량 우위는 Spearman 1건**
- 논문: MultiVelo
- 관찰: mouse skin에서 latent time과 Palantir pseudotime의 Spearman 0.51 (scVelo 0.44).
- 근거: Figure 4, Results.
- Caveat: 나머지 dataset(mouse brain, HSPC, fetal brain)의 우위 근거는 UMAP stream plot의 biological plausibility 중심이며 동일 metric으로 통일되어 있지 않다.

**E-05 — MoFlow의 정량 우위는 CBDir 1건**
- 논문: MoFlow
- 관찰: developing human brain cortex(4,693 cells / 842 genes)에서 CBDir MoFlow 0.362, MultiVelo 0.211, scVelo 0.211, cellDancer −0.015.
- 근거: Figure 2d, Results.
- Caveat: E18 mouse brain과 HSPC의 CBDir exact value는 본문에 없고 Figure/Supplementary Table 1에 의존한다.

**E-06 — MultiVeloVAE의 정량 근거는 본문에 거의 없음**
- 논문: MultiVeloVAE
- 관찰: RNA-only 10개 dataset, multi-omic 5개 dataset에서 개선을 보고하나 exact value는 Source Data / Supplementary Fig. 4·19 의존.
- 근거: Figure 2f, Figure 3g/3h, Figure 4d/e.
- Caveat: 분석자가 명시적으로 지적한 한계. "본문에는 주로 방향성/상대 우위가 제시된다."

## C. 같은 dataset, 다른 결론

**E-07 — mouse skin Wnt3에 대한 3자 해석 불일치**
- 논문: 3편 모두
- 관찰:
  - MultiVelo: Wnt3는 induction-only priming gene. DTW로 maximum `c-s` delay가 normalized time range 1 중 0.6.
  - MultiVeloVAE: **MultiVelo가 IRS lineage 전체를 priming으로 잘못 해석**한다고 지적. MultiVeloVAE는 진짜 priming lineage와 IRS lineage를 분리.
  - MoFlow: Wnt3와 Trps1은 **MoFlow와 MultiVelo가 모두 잘 잡았다**고 평가.
- 근거: MultiVelo Figure 4d-f / MultiVeloVAE Figure 3f, Results / MoFlow Figure 5d-e.
- Caveat: 세 논문의 평가 기준이 다르다(정량 DTW lag / lineage 분리 정확도 / gene-wise velocity 방향). 동일 기준 재평가가 없으면 어느 해석이 옳은지 결정할 수 없다.

**E-08 — latent time fitting이 lag 부호를 뒤집는다**
- 논문: MoFlow (대상: MultiVelo)
- 관찰: MoFlow pseudotime과 MultiVelo **global** latent time에서는 PDGFRA/MAP3K1의 negative `c-s` lag가 보이지만, MultiVelo **gene-specific** latent time에서는 같은 lag가 사라지고 canonical order로 정렬된다. 400개 초과 gene이 최소 25% time bin에서, 129개 gene이 75% 초과 bin에서 sign reversal.
- 근거: MoFlow Figure 3f-g, Results.
- Caveat: MoFlow는 이를 "over-correction"으로 해석하지만, 반대로 MoFlow의 local relay가 noise를 lag로 잡았을 가능성은 배제되지 않았다. 양쪽 모두 ground truth가 없다.

**E-09 — negative lag가 biological signal이라는 근거**
- 논문: MoFlow
- 관찰: decoupling-sOff region의 mGPC/OPC cell 중 63%가 Allen Brain Atlas에서 OPC로 embedding (complementary region 20%). cluster 0·3·10은 short nuclear half-life와 fast export, cluster 1·2는 prolonged retention.
- 근거: Figure 3h, Figure 7e-g.
- Caveat: half-life는 NIH3T3 cell line 외부 데이터이며 brain development에서 직접 측정된 값이 아니다. 10x Multiome은 nuclear RNA를 측정하므로 degradation처럼 보이는 현상이 nuclear export일 수 있다.

## D. 공통 한계 근거

**E-10 — perturbation validation 부재 (3편 공통)**
- MultiVelo: "priming/decoupled gene을 perturb-seq 또는 CRISPRi/CRISPRa로 검증" 필요 (Final Takeaways). SNP 분석은 temporal association이며 causal evidence 아님.
- MultiVeloVAE: in silico SPI1/GATA1 KO는 `c, u, s`를 0으로 두는 simulation이며 실제 CRISPR 결과가 아님 (Figure 7 주의점).
- MoFlow: chromatin state `k` 선택과 DDR 해석 모두 direct perturbation 없음.
- Caveat: 3편 모두 저자 또는 분석자가 명시. 예외 없음.

**E-11 — wall-clock calibration 부재 (3편 공통, 부분 예외 1)**
- 모든 timing 산출물이 pseudotime / latent time 단위.
- 부분 예외: MultiVeloVAE는 capture time prior가 있으면 hours/days 같은 real temporal unit과 연결할 수 있다고 서술하고, MEF reprogramming dataset에서 0-28일 6 time point를 사용했다. 다만 lag 자체를 실제 시간 단위로 calibration한 결과는 제시하지 않았다.
- Caveat: "3편 공통"으로 뭉뚱그리면 MultiVeloVAE의 부분 진전을 놓친다.

**E-12 — gene-level chromatin aggregation (3편 공통)**
- MultiVelo: gene 주변 peak를 aggregate.
- MultiVeloVAE: gene-linked peak의 **summed** accessibility `c`를 모델링하므로 individual cis-regulatory element effect는 downstream correlation/MI로만 추론 (Figure 5 주의점, 저자 명시).
- MoFlow: long-range enhancer-promoter interaction을 명시적으로 모델링하지 않음 (저자 명시 한계 1).
- Caveat: 세 논문 모두 enhancer-level timing 해상도가 없다. peak-level ODE는 MultiVeloVAE의 open question 3번으로 남아 있다.

**E-13 — uncertainty interval 부재 (2편, 1편은 해결)**
- MultiVelo: lag-like estimate에 credible/confidence interval 없음.
- MoFlow: 동일하게 없음.
- **예외**: MultiVeloVAE는 posterior sampling, credible interval, cell-state uncertainty를 제공하고 Bayes factor 기반 differential testing까지 수행한다 (Figure 3e, Figure 5e, Figure 6).
- Caveat: 이 항목을 "3편 공통 한계"로 기술하면 사실과 다르다.

**E-14 — benchmark metric 불일치 (3편 공통)**
- MultiVelo: dataset마다 metric이 통일되지 않음 (분석자 지적).
- MoFlow: exact numerical metric이 모든 dataset에 동일하게 제공되지 않음 (분석자 지적).
- MultiVeloVAE: exact value가 Source Data/Supplementary 의존 (분석자 지적).
- Caveat: 세 논문이 서로를 baseline으로 인용하지만 동일 preprocessing·동일 gene selection·동일 metric의 통합 비교표는 어느 논문에도 없다.

## E. 프로젝트 연결 근거

**E-15 — baseline epigenomic feature로 lag를 예측한 선례 없음**
- 관찰: 세 논문 모두 lag를 **추정 결과(output)** 로 산출한다. lag를 **예측 대상(target)** 으로 두고 baseline chromatin feature에서 회귀·분류한 분석은 세 편 어디에도 없다.
- 근거: 각 논문 key_outputs 항목 (`papers.jsonl`). MultiVelo는 interval length, MoFlow는 DTW lag, MultiVeloVAE는 `delta`를 산출하나 모두 model fitting의 부산물이다.
- Caveat: 본 분석 범위는 selected 3편이다. scope 밖 literature에 선례가 있을 가능성은 배제하지 못한다.
