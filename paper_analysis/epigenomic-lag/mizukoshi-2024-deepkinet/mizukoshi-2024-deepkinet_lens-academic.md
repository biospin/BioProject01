# Lens — Academic — Mizukoshi 2024 DeepKINET

Citation key: `@mizukoshi2024deepkinet`. Core analysis: `mizukoshi-2024-deepkinet_core.md`. 본 lens는 *학계 시선*만 다룬다 — 후속 논문 아이디어, 분석자 판단, citation 후보. 산업/규제/임상 관점은 `mizukoshi-2024-deepkinet_lens-industry.md`로 분리.

## 1. Limitations

### 1.1 저자가 명시한 한계 (Discussion, p.12–13)

저자는 한계 4가지를 직접 명시한다 (인용 원문 + 분석자 보강).

1. **Unified model로 splice/deg rate 동시 추정 → 두 rate 간 잔여 correlation**
   - 원문: "Employs a unified model to estimate splicing and degradation rates, which can lead to correlation trends among these rates (Additional file 1: Fig. S1d, S2c, S5)" (p.12).
   - 저자 반박: cellDancer/DeepVelo보다 *상대적으로 낮은* 상관이라 인정 가능하다고 주장. Sup. Fig. S5에서 정량.
   - 해석: "weakly correlated" (Sup. Fig. S5 caption)라고 직접 명시함에도 *상대 비교*만 valid라 인정한 셈.

2. **Simultaneous velocity-rate estimation의 underdetermination**
   - 원문: "the simultaneous estimation of RNA velocity and kinetic rates presents a challenge, indicating the need for further methodological enhancements and additional constraints for improved accuracy" (p.12).
   - 즉 모델이 *수학적으로 underdetermined*. 본 논문은 2-stage decoupling + cell-state smoothness로 *완화*했을 뿐 *해결*은 안 함.

3. **Transcription rate cell-uniform 가정 유지**
   - 원문: "by extending DeepKINET, the assumption of fixed transcription rates for each gene can also be eliminated. However, this would increase the number of parameters" (p.12). 직접 MultiVelo [@li2023multivelo Ref. 46]를 인용하며 "transcription rate determined based on chromatin accessibility ... is more realistic" 인정.
   - 우리 입장에서 흥미: DeepKINET 저자가 *epigenomic-lag 방향*을 ideal extension으로 직접 지목.

4. **mRNA isoform 미구별**
   - 원문: "the current limitations of RNA velocity analysis in distinguishing mRNA isoforms ... particularly relevant to diseases such as cancer, where alternative splicing is prevalent" (p.13). isoform 구별이 본질인 SF3B1 mutation 분석에서도 자체 한계.

### 1.2 분석자가 판단한 한계 (저자 미언급)

1. **Simulation self-favorable risk**
   - 검토필요: SERGIO source code를 *저자가 수정*해 cluster별 rate를 inject (Methods p.15). DeepKINET이 추정하는 ground-truth structure(*cell state → rate*)가 simulation의 generation structure와 *너무 잘 정합*할 가능성. cellDancer/DeepVelo는 *다른 inductive bias*라 disadvantage.
   - 후속 실험 후보: 같은 SERGIO 변형이 아니라 *완전 다른 simulator*(예: dyngen, BEELINE) 또는 *cell-level rate variation*을 inject한 simulation으로 cross-check.

2. **Metabolic-labeling ground truth가 Dynamo에 의존**
   - 본문 p.5: "values obtained from the metabolic labeling experiments depended on the assumptions of the mathematical model used and did not represent the perfect ground truth". 즉 scEU-seq/scNT-seq의 *raw temporal data*가 ground truth가 아니라 *Dynamo가 후처리한 cluster-level rate*가 ground truth. Dynamo의 model assumption이 잘못되면 *모두* 잘못된 비교.
   - 해석: 진정한 ground truth는 *labeled RNA fraction의 raw temporal kinetics*인데, 본 논문은 그것을 직접 쓰지 않고 *Dynamo의 cluster-level kinetic estimate*를 ground truth로 쓴다. circularity 위험.

3. **Cluster-level aggregation으로 cell-level claim 검증**
   - DeepKINET의 contribution은 *cell-level rate*인데 ground truth는 *cluster-level*. 즉 evaluation은 cluster-level까지만 가능하고 *진정한 cell-level heterogeneity의 fidelity*는 검증되지 않음.
   - 후속 실험 후보: scEU-seq raw labeled fraction을 cell-level로 *직접* 모델링하는 hierarchical benchmark.

4. **Single-cell-level rate 정확도 수치 자체가 부재**
   - 본문은 *box plot/scatter*만 제시하고 정확한 Pearson $r$, RMSE, rank concordance 수치를 텍스트에 명시하지 않음.
   - 검토필요: median/IQR이라도 본문 텍스트로 적었어야 reproducibility 측면에서 의미가 명확.

5. **RBP target list = bulk eCLIP**
   - Fig. 4의 RBP target은 CLIPdb [Yang 2015 Ref. 51] bulk eCLIP. cell-type-specific binding 차이 무시. 따라서 "target gene이 RBP expression과 유의하게 상관"이라는 결과는 *bulk-level expectation*이 cell-level rate에 reflect된다는 weaker claim.

6. **MDS-RS SF3B1 결과의 interpretive circularity**
   - 저자 본인이 p.11에서 인정: alternative 3' splice site usage는 *intron retention*처럼 보이고 → unspliced read 증가 → RNA velocity 정의상 *낮은 splicing rate*. 즉 "SF3B1 mutant에서 splicing rate가 낮게 보인다"는 결과는 *model 정의의 결과*이지 splicing kinetics 자체에 대한 *독립* validation은 아님.

### 1.3 매끄럽지 않은 연결

- **Fig. 2 → Fig. 3 transition**: simulation에서 DeepKINET이 splicing과 degradation 모두 우위였는데 scEU-seq에서는 *splicing만 comparable*. 왜 metabolic labeling에서 splicing 우위가 사라지는지에 대한 설명이 본문에 부재. 검토필요.
- **Fig. 4 RBP 해석 ↔ 본문 Discussion**: forebrain의 RBP-target rate correlation이 *기계적*으로 validation 역할을 했는데 Discussion에는 직접 언급 없이 "biological application"으로만 처리. RBP-rate correlation = *cell-type 외부 biology에 대한 model 정확도*라는 명시적 framing이 빠짐.

## 2. 다음 논문 아이디어

분석자 판단 — 본 paper에서 출발해 *직접 후속*으로 쓸 만한 4가지.

### 2.1 (직접 후속) Chromatin-aware DeepKINET — "DeepKINET-Multiome"

저자 본인이 Discussion p.12에서 신호한 방향. MultiVelo [@li2023multivelo]의 chromatin-driven transcription rate modeling을 DeepKINET 골격에 결합.

- 입력: scRNA-seq (unspliced/spliced) + ATAC-seq peak.
- 모델 확장: transcription rate $\alpha_n$도 cell-state-dependent로 modeling. Stage 0 추가 — chromatin accessibility encoder.
- Validation: 본 논문이 쓴 metabolic labeling benchmark + multiome chromatin opening dynamics.
- 우리 stack과 직접 연결: 우리 epigenomic-lag 정의 ($t_{open} \to t_{transcription}$)와 부합.

### 2.2 (방법론 borrow) Lag-aware validation benchmark for multiome velocity

DeepKINET이 *RNA-only* kinetic rate에 metabolic labeling benchmark를 *standard*로 만들었듯, *multiome lag* 추정에도 ground-truth proxy benchmark가 필요.

- Proxy 후보:
  - scEU-seq + ATAC (이런 dataset 부재 — 검토필요, *실험 design*이 우리 후속 contribution가 될 수 있음).
  - SLAM-seq + Multiome (technical 결합 가능성?).
  - 합성 promoter perturbation (CRISPR activator + time-resolved multiome).

### 2.3 (학술 contribution) Cell-level rate fidelity audit framework

본 paper의 한 가지 큰 빈틈 — cell-level rate ground truth 부재. 우리가 *single-cell-level metabolic labeling*을 활용해 cluster-level이 아닌 *cell-level*에서 DeepKINET/cellDancer/DeepVelo의 rate fidelity를 audit하는 framework를 짤 수 있음. 결과 자체로 method 비교 review가 됨.

### 2.4 (BD-conscious) Splicing factor mutation × therapeutic response single-cell map

SF3B1 mutation (MDS-RS) 외에 SRSF2, U2AF1 등 다른 splicing factor mutation에 DeepKINET을 *체계적*으로 적용해 splicing-rate alteration map → therapy response prediction. 본 paper는 SF3B1 한 케이스에 그침. 임상 응용 가능성 있음 — `lens-industry`에 BD-opportunity로 cross-link.

## 3. Validation design transferability — chromatin-transcription lag으로 이식 가능한가?

> 본 sub-section은 Week2 validation_report claim C8을 *직접* 보강한다.

### 3.1 DeepKINET validation design 분해

본 paper의 validation은 3-layer 구조다.

| Layer | Ground truth source | Resolution | 모델이 추정하는 양 |
|---|---|---|---|
| L1: Simulation | SERGIO에 inject한 cluster별 set rate | cluster-level | $\beta_n, \gamma_n$ |
| L2: Metabolic labeling (scEU-seq) | Dynamo가 cluster-level kinetic rate로 후처리 | cluster-level (≈30 cluster) | $\beta_n, \gamma_n$ |
| L3: Metabolic labeling (scNT-seq) | Dynamo가 time batch별 degradation rate ratio로 후처리 | batch-level (2 batch) | $\gamma_n$ ratio |

L1은 *self-defined* ground truth (저자가 만든 simulator 변형). L2/L3는 *external temporal* ground truth (labeling experiment + 후처리).

### 3.2 이식 가능한 elements

다음은 chromatin-transcription lag validation으로 *바로* 이식할 수 있다.

- **2-stage decoupling 학습 전략**: 안정된 latent dynamics 위에 *별도 decoder*로 secondary kinetic parameter를 추정. 우리 lag 추정 모델에도 적용 가능 — 먼저 chromatin/RNA joint VAE → freeze → lag decoder 학습.
- **Cluster-level set-value scatter benchmark (L1)**: 우리도 simulator에 *cluster별 lag*를 inject하고 추정 lag와 correlation. 곧바로 SERGIO 변형 + chromatin opening simulator 결합으로 가능 — 단 chromatin-aware simulator 자체가 검토 필요 (BEELINE, MultiVelo authors의 simulation script 등 후보).
- **Multi-method comparison framework**: 동일 dataset에 *경쟁 method 100회 반복* → box plot으로 분산까지 평가하는 방식. MultiVelo/MultiVeloVAE/MoFlow에 동일 design 적용 가능.
- **Negative-correlation 기준의 "fail" 정의**: cellDancer가 degradation에서 negative correlation 보였다는 사실 자체가 *signal*. lag 추정에서도 *방향(부호)이 wrong*하면 명시적 fail로 처리하는 evaluation rule 정립.

### 3.3 이식 *못* 하는 elements

- **scEU-seq/scNT-seq의 *RNA labeling temporal resolution* → chromatin lag로 직접 mapping 불가**
  - scEU-seq는 5-EU(나 동족)가 *RNA 합성*에 incorporate. *chromatin opening* event를 직접 label하지 않음. Chromatin opening의 *temporal* ground truth를 위해서는 *별도 labeling 화학*이 필요 — 현 시점에서 표준 single-cell assay 없음.
  - 외부 맥락: ATAC-see/CUT&Tag 등의 chromatin-state assay는 *snapshot*만 제공, *temporal* dynamics는 *별도 시점 cohort + 합산 pseudotime*으로만 추론.

- **Dynamo의 후처리 step → lag 추정에 동등 후처리 없음**
  - DeepKINET은 *Dynamo가 metabolic labeling을 kinetic rate로 변환한 결과*를 ground truth로 씀. lag 추정의 경우 동등한 "external method가 ground-truth lag를 산출"하는 step이 부재. MultiVelo의 switch time을 ground truth로 쓰면 *circularity* (이는 우리가 검증하려는 method 자체).

- **L1 simulation의 rate 단위와 lag 단위 차이**
  - DeepKINET simulation은 *rate (1/time)* 단위로 inject. lag는 *time 단위*. simulation에서 lag를 inject하려면 chromatin opening event time과 transcription start time을 *명시적*으로 정해야 함 → simulator 자체 재설계 필요.

### 3.4 종합 — Week2 C8에 대한 정리

C8의 현재 표현 ("validation design reference로 제한") + 본 sub-section의 분해 결과를 종합하면 다음 update가 가능.

| 요소 | 이식 가능? | 비고 |
|---|---|---|
| 2-stage decoupling 학습 방식 | ✅ | 즉시 차용 가능 (methodology-reference) |
| Cluster-level simulation benchmark | ⚠️ 부분 | chromatin-aware simulator 자체 검토 필요 |
| Multi-method 100회 반복 evaluation | ✅ | metric만 lag-적합한 것으로 교체 |
| Negative-correlation = fail 규칙 | ✅ | 즉시 차용 |
| Metabolic labeling temporal ground truth → lag | ❌ | chromatin labeling 표준 부재 |
| Dynamo-style external rate 후처리 → lag | ❌ | 동등 external method 부재 |

결론: DeepKINET의 *evaluation framework 자체*는 transferable. *labeling data 자체*는 transferable 아님. 따라서 Week2 C8을 "validation design reference + framework borrow 가능, labeling ground truth ≠ chromatin labeling ground truth" 양면으로 분해 표현이 더 정확.

## 4. Final Takeaways

- DeepKINET은 *RNA-only* kinetic rate에 *metabolic-labeling benchmark*를 standard로 자리잡게 한 reference paper. 우리 epigenomic-lag 분야에서 *동등한 ground-truth framework*가 부재하다는 사실이 명확해짐.
- 저자가 Discussion에서 직접 MultiVelo를 ideal extension으로 지목 → 우리 stack과의 자연스러운 연결점.
- 가장 흥미로운 후속 idea: chromatin-aware DeepKINET ("DeepKINET-Multiome") + scEU-seq + Multiome 실험 design.

## 5. Citation 후보 (본인 논문·제안서·학회 발표용)

### 5.1 인용 가능 문장

- §Background, p.2: "this approach has been criticized for assuming uniform kinetic rates across cells, which may cause misrepresentation of true biological variation. While transcription rates have been modeled to account for cell-to-cell variability, methods such as scVelo and VeloVI have assumed uniform splicing and degradation rates for each gene"
  - 사용 시나리오: 본인 introduction에서 *기존 RNA velocity 한계*를 압축 인용. 한 문장으로 scVelo/VeloVI를 *uniform rate 한계*로 묶음.
  - BibTeX key: `@mizukoshi2024deepkinet`

- §Discussion, p.12: "An existing method MultiVelo uses multi-omics data (gene expression and chromatin accessibility) as input and assumes that transcription rates are determined based on chromatin accessibility near the gene. ... MultiVelo's modeling is more realistic than estimating transcription rates using only scRNA-seq data"
  - 사용 시나리오: 우리 *epigenomic-lag* paper의 motivation에서 "RNA-only method 저자도 chromatin-aware extension을 ideal로 인정한다"는 evidence로 인용.
  - BibTeX key: `@mizukoshi2024deepkinet`

- §Results, p.5: "values obtained from the metabolic labeling experiments depended on the assumptions of the mathematical model used and did not represent the perfect ground truth. Nevertheless, the temporal resolution inherent in the metabolic experimental data lost in scRNA-seq provides a benchmark from which to assess the similarity to extrapolated kinetic rates"
  - 사용 시나리오: 본인 validation 섹션에서 "labeling data = imperfect but standard ground truth proxy"라는 framing 인용.
  - BibTeX key: `@mizukoshi2024deepkinet`

- §Discussion, p.12: "the first instance in which such kinetic rates have been estimated and validated for accuracy at the single-cell level using both simulated and metabolic labeling data"
  - 사용 시나리오: 우리 *epigenomic-lag* 후속 method의 contribution을 *"DeepKINET이 RNA-only에서 한 것을 chromatin-RNA lag에서 한다"*고 직접 대조할 때.
  - BibTeX key: `@mizukoshi2024deepkinet`

- §Discussion, p.12 (한계 인정): "The simultaneous estimation of RNA velocity and kinetic rates presents a challenge, indicating the need for further methodological enhancements and additional constraints"
  - 사용 시나리오: 본인 proposal에서 "simultaneous velocity/rate estimation의 indeterminacy"를 명시한 *저자 본인 인정* citation으로 활용.
  - BibTeX key: `@mizukoshi2024deepkinet`

### 5.2 인용 가능 수치

- *Latent dimension 기본값 $D=20$* (Methods, p.13). 사용 시나리오: 본인 모델의 latent dim 결정 근거 reference.
- *Cluster 수 6~30, cluster당 100 cells* (Methods, p.15). 사용 시나리오: 본인 simulation benchmark의 cluster scale 설계 근거.
- *Breast cancer dataset cell count 15,269 primary + 642 metastatic* (Results, p.10). 사용 시나리오: 본인 메타분석에서 metastasis vs primary cell imbalance 사례.
- *7 MDS-RS + 2 healthy = 9 samples로 conditional VAE training* (Results, p.10). 사용 시나리오: small cohort에서 conditional VAE가 의미 있는 신호 추출했다는 sample-size precedent.

### 5.3 인용 가능 Figure/Table

- Figure 2 (p.4): cellDancer/DeepVelo가 degradation rate에서 negative correlation 보이는 *명확한 box plot*. 사용 시나리오: 우리 review/proposal에서 *cell-specific RNA velocity method의 fragility* 입증 도식으로 재인용.
- Figure 3b (p.6): scEU-seq PULSE에서 100회 반복 box plot. 사용 시나리오: *labeling data benchmark의 reproducibility 평가 표준* 사례로 인용.
- Sup. Fig. S5: split-deg correlation 종합. 사용 시나리오: 본인 model의 *parameter independence* 평가에서 비교 baseline으로 인용.

## 6. 후속 자기 질문

- 질문: scEU-seq raw labeled fraction을 cell-level로 직접 modeling하는 hierarchical Bayesian benchmark를 누가 이미 만들었는가? Dynamo 이외 후속 method 검색 필요.
- 질문: DeepKINET-Multiome (chromatin-aware extension)을 누군가 이미 시도했는가? MultiVelo authors (Welch lab) 후속 publication 모니터링.
- 질문: alternative 3' splice site 효과를 *splicing rate 감소*로 모델링하는 본 paper 해석이 정량 isoform-level analysis로 확인된 적이 있는가? — supplementary 추가 figure 없음.

마지막 갱신: 2026-05-26
