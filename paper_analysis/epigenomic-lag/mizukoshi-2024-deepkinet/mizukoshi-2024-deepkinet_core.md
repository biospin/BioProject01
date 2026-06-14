# DeepKINET: a deep generative model for estimating single-cell RNA splicing and degradation rates

Citation: `@mizukoshi2024deepkinet` — Mizukoshi C, Kojima Y, Nomura S, Hayashi S, Abe K, Shimamura T. *Genome Biology* 25:229 (2024). DOI: 10.1186/s13059-024-03367-8.

> Full analysis. 근거는 `sources/mizukoshi-2024-deepkinet.pdf` (21페이지 본문)와 `sources/mizukoshi-2024-deepkinet-supp-1-figures.pdf` (Supplementary Figures S1~S5)이다. Supplementary 2 (Reporting Summary, docx)는 본 환경에서 직접 파싱 불가 — `미제공:`으로 표기.

## Executive Summary

- **무엇**: scRNA-seq의 unspliced/spliced count만으로 *세포 단위* splicing rate $\beta_n$과 degradation rate $\gamma_n$을 추정하는 deep generative kinetic model. scVelo/VeloVI의 "gene별 uniform rate" 가정을 깨고 cell-state-dependent rate를 추정 (§Background, p.2; §Methods p.13–14).
- **모델 / 방법**: VAE로 latent cell state $z_n$과 small change $d_n$을 학습 → encoder/decoder freeze → $z_n$을 입력으로 받는 rate decoder 두 개($\beta_n$, $\gamma_n$)를 추가 학습. RNA velocity 방정식 $\hat{u}_n \approx l_{un}\,\frac{\partial\theta(z_n)/\partial z_n \cdot d_n + dt\cdot\gamma_n s_n}{dt\cdot\beta_n}$로 unspliced 재구성 (Eq. 1–2, Methods p.13–14).
- **핵심 결과**:
  - ① Simulated data (SERGIO) — 20 dropout 조건 + 14 cell-number 조건 각 10 dataset에서 set-vs-estimated rate correlation이 cellDancer/DeepVelo보다 *항상* 높고 negative correlation 없음 (Fig. 2b–c, p.4).
  - ② scEU-seq cell-cycle PULSE — Dynamo-derived rate와의 correlation 100회 반복 시 splicing은 cellDancer/DeepVelo와 comparable, degradation에서 단독 우위, cellDancer는 negative correlation (Fig. 3b, p.6).
  - ③ scNT-seq hematopoiesis — 두 시간 batch 간 degradation rate ratio가 Dynamo와 상관, cellDancer/DeepVelo 능가 (Fig. S3c).
  - ④ Forebrain (La Manno 2018) + Breast cancer (Liu 2022) + MDS-RS SF3B1 (Adema 2022) — RBP target enrichment, RBFOX1/2, RBM47, SF3B1 mutation으로 target splicing rate 유의 감소 등 mechanistic 응용 (Fig. 4–6).
- **우리 적용**: chromatin은 안 다루지만 Week2 validation_report claim C8의 *kinetic-rate validation reference*. metabolic-labeling benchmark 설계 논리를 chromatin-transcription lag validation으로 이식할 수 있는지 별도 평가 필요 — `methodology-reference` + `academic-citation`.
- **심층**: 한계와 단일-모델 splice/deg 상관 문제, simultaneous velocity-rate 추정의 indeterminacy는 `mizukoshi-2024-deepkinet_lens-academic.md`, scEU-seq/scNT-seq 자체 시도 feasibility는 `mizukoshi-2024-deepkinet_lens-industry.md`, 1페이지 ROI 판단은 `mizukoshi-2024-deepkinet_methodology-brief.md` 참고.

## Identity

- **Title**: DeepKINET: a deep generative model for estimating single-cell RNA splicing and degradation rates
- **Authors**: Chikara Mizukoshi (Nagoya U.), Yasuhiro Kojima (NCC + TMDU), Satoshi Nomura, Shuto Hayashi, Ko Abe, Teppei Shimamura
- **Year / Venue**: 2024-09-06, *Genome Biology* 25:229 (Method, Open Access)
- **DOI**: 10.1186/s13059-024-03367-8
- **Citation key**: `mizukoshi2024deepkinet`
- **Code / data**: https://github.com/3254c/DeepKINET (MIT) — Zenodo 10.5281/zenodo.13054695 (Availability, p.18).
- **Author contributions**: Y.K. conceived the method, K.A. conceived simulation-validation idea, C.M. coded/ran experiments, Y.K. & T.S. supervised (p.18). 책임저자는 ML 방법론 (Kojima·Shimamura)과 임상 RNA biology (Nagoya 의대) 교집합.

## Background

본 논문이 풀려는 문제는 *RNA velocity의 "uniform kinetic rate" 가정 깨기*다 (§Background, p.1–2).

핵심 배경:

- mRNA splicing과 degradation은 gene expression 정밀 조절에 필수이며 splicing 이상은 cancer를 비롯한 질환과 직결된다 (Ref. 1–2).
- 기존 kinetic-rate 추정은 크게 두 갈래.
  - **Metabolic labeling** (scEU-seq [Battich 2020, Ref. 3], scNT-seq [Qiu 2020, Ref. 4]): time resolution을 제공하지만 *특수 labeling 실험*이 필요 → 일반 scRNA-seq에 즉시 적용 불가.
  - **RNA velocity** (Velocyto [La Manno 2018, Ref. 5], scVelo [Bergen 2020, Ref. 6], VeloVI [Gayoso 2024, Ref. 7]): unspliced/spliced 만으로 동역학을 추정하지만 *gene별로 모든 cell에 같은 $\beta$, $\gamma$* 가정 → biological variation을 misrepresent할 우려가 있다고 비판받음.
- cellDancer [Li 2023, Ref. 8 — `@li2023celldancer`]는 neighboring cell info와 deep NN으로 cell-specific rate를 추정하지만 *주 목적이 velocity 정확도*라 kinetic rate 자체의 정확도는 별도로 검증되지 않았다고 저자가 지적.

이 gap에서 DeepKINET는 "deep generative model + cell state"로 single-cell 단위 $\beta_n$, $\gamma_n$을 추정하고 *simulation + metabolic labeling으로 직접 validation*하겠다고 선언한다 (p.2 마지막 단락). 저자 표현: "the first instance in which such kinetic rates have been estimated and validated for accuracy at the single-cell level using both simulated and metabolic labeling data" (Discussion, p.12).

해석: 이 framing은 두 가지 의미를 갖는다. (1) cellDancer/DeepVelo 대비 *validation* 자체가 contribution. (2) metabolic labeling이 RNA-only kinetics에서 그나마 ground-truth 역할을 하는 standard로 자리 잡고 있다는 분야적 합의를 깔고 있다. 후자가 우리 Week2 validation_report C8의 출발점이다.

## Methods

### 1. Formal task

입력: scRNA-seq의 unspliced count $u_n\in\mathbb{R}^g$, spliced count $s_n\in\mathbb{R}^g$ (각 cell $n$, $g$ genes).

출력: cell별 splicing rate $\beta_n\in\mathbb{R}^g$, degradation rate $\gamma_n\in\mathbb{R}^g$ + latent cell state $z_n\in\mathbb{R}^D$ (default $D=20$) + latent velocity direction $d_n\in\mathbb{R}^D$ (Methods §Derivation, p.13).

### 2. 확률/통계 구조 — 2-stage VAE

**Stage 1: cell state VAE + RNA velocity (VICDYF [Nagaharu 2022, Ref. 9] 계승).**

Prior:

$$
p(z_n) = \mathcal{N}(0, I), \quad p(d_n) = \mathcal{N}(0, \rho I), \quad \rho = 0.01
$$

$\rho$는 $d_n$이 $z_n$ 대비 *작은* perturbation이어야 한다는 제약 (VICDYF 기본값 그대로).

Likelihood (둘 다 Poisson; negative binomial도 옵션이지만 본 논문 모든 실험은 Poisson):

$$
\hat{s}_n = l_{sn}\,\theta(z_n), \qquad p(s_n \mid z_n) = \mathrm{Poisson}(\hat{s}_n)
$$

여기서 $l_{sn}\in\mathbb{R}^g$는 single cell의 spliced count library size, $\theta(\cdot)$는 hidden unit 100 × 1 layer + LayerNorm decoder.

Velocity는 latent space에서 small change $d_n$을 *decoder Jacobian*으로 push-forward한 값으로 정의 (functorch 사용, central difference 아님):

$$
v_n = \frac{\partial \theta(z_n)}{\partial z_n}\, d_n \quad (\text{Eq. 1, p.13})
$$

RNA velocity 미분방정식으로 unspliced 평균을 spliced와 rate로 표현:

$$
\hat{u}_n \approx l_{un}\,\frac{v_n + dt\,\gamma\, s_n}{dt\,\beta} \quad (\text{Eq. 2})
$$

여기서 $\beta, \gamma\in\mathbb{R}^g$는 *gene-specific이지만 cell-uniform* (Stage 1 단계). $dt=1$. 결합:

$$
\hat{u}_n \approx l_{un}\,\frac{\tfrac{\partial \theta(z_n)}{\partial z_n}\,d_n + dt\,\gamma\,s_n}{dt\,\beta}, \quad p(u_n\mid z_n, d_n)=\mathrm{Poisson}(\hat{u}_n)
$$

Variational posterior:

$$
q(z_n \mid s_n, u_n) = \mathcal{N}\big(\mu_\phi(s_n, u_n), \mathrm{diag}(\sigma_\phi(s_n, u_n))\big)
$$

$$
q(d_n \mid z_n) = \mathcal{N}\big(\mu'_\phi(z_n), \mathrm{diag}(\sigma'_\phi(z_n))\big)
$$

Encoder $\mu_\phi$는 hidden unit 100 × 2 layer + LayerNorm, $\mu'_\phi$는 100 × 1 layer + LayerNorm.

Loss는 ELBO:

$$
\mathcal{L}(\theta, \phi) \geq -\log p(s_n \mid z_n') - \log p(u_n \mid z_n', d_n') + \mathrm{KL}\big(q(z_n\mid s_n,u_n)\,\|\,p(z_n)\big) + \mathrm{KL}\big(q(d_n\mid z_n')\,\|\,p(d_n)\big)
$$

Optimizer: AdamW, lr=0.001, mini-batch 100, early stop = "10 epoch 평균 loss가 10 epoch 동안 갱신 안 될 때" (p.14).

**Stage 2: cell-specific rate decoder.**

Stage 1의 encoder/decoder $\phi, \theta$를 *freeze*하고, $z_n$ → $(\beta_n, \gamma_n)$ neural network 두 개를 새로 학습. 같은 ELBO loss를 쓰되 unspliced reconstruction에 $\beta, \gamma$를 $\beta_n, \gamma_n$으로 치환 (p.14):

$$
\hat{u}_n \approx l_{un}\,\frac{\tfrac{\partial \theta(z_n)}{\partial z_n}\,d_n + dt\,\gamma_n\,s_n}{dt\,\beta_n}
$$

저자 표현: "By estimating the splicing and degradation rates as cell-state-dependent values, the rates for cells with similar cell states will be similar, weakening the indeterminacy of the solution" (p.14).

### 3. Conditional VAE (multi-sample)

Multiple samples/batch 처리를 위해 batch indicator $b_n \in \{0,1\}^B$를 encoder/decoder에 추가 (Kingma 2014 [Ref. 40]):

$$
q(z_n \mid s_n, u_n, b_n) = \mathcal{N}\big(\mu_\phi(s_n, u_n, b_n), \mathrm{diag}(\sigma_\phi(s_n, u_n, b_n))\big), \quad \hat{s}_n = l_{sn}\,\theta(z_n, b_n)
$$

SF3B1 mutation 분석(7 환자 + 2 healthy)과 scNT-seq hematopoiesis (시간 batch)에서 사용 (p.14, p.16).

### 4. 핵심 method insight — 무엇이 새로운가

해석: 핵심 trick은 *2-stage decoupling*이다.

1. Stage 1에서 VAE가 *cell state → expression*과 *latent velocity*를 안정적으로 학습. 이때 $\beta, \gamma$는 cell-uniform이라 indeterminacy가 거의 없음.
2. Stage 2에서 encoder/decoder는 고정한 채 $z_n$ → $(\beta_n, \gamma_n)$만 학습. 이 *분리* 덕분에 cell-specific rate가 자연스럽게 "비슷한 cell state는 비슷한 rate"라는 *smoothness regularization* 효과를 얻음.

이 설계가 cellDancer/DeepVelo와 결정적으로 다른 점은 "velocity를 refine하려고 cell-specific rate를 쓰는" 것이 아니라, "안정된 latent dynamics 위에 *rate decoder를 따로 얹어* rate 자체를 estimand로 삼는다"는 것 (Discussion, p.12).

### 5. 이전 방법과 차이

| Method | Cell-specific rate? | 1차 목표 | Indeterminacy 대응 |
|---|---|---|---|
| Velocyto [@La Manno 2018 Ref. 5] | No (cell-uniform) | Velocity 방향 | 가정 자체로 회피 |
| scVelo [@bergen 2020 Ref. 6] | No | Latent time + velocity | 가정 자체로 회피 |
| VeloVI [@Gayoso 2024 Ref. 7] | No (gene-specific만) | Velocity (deep generative) | 가정 자체로 회피 |
| cellDancer [@li2023celldancer Ref. 8] | Yes | *Velocity 정확도 refine* | 명시적 대응 부재 |
| DeepVelo [@cui2024deepvelo Ref. 12] | Yes | Velocity (multi-lineage) | 명시적 대응 부재 |
| **DeepKINET (본 논문)** | **Yes** | ***Kinetic rate 자체 + validation*** | **2-stage decoupling + cell-state smoothing** |

해석: 본 논문이 cellDancer/DeepVelo를 *직접* 비교 대상으로 삼은 이유는 명확하다. cell-specific rate를 산출하는 *유일한* 선행 방법들이고, scVelo/Velocyto는 "uniform rate를 가정하므로 비교 자체가 unfair" (p.4)라고 명시.

### 6. Validation 데이터셋 셋업 (Method 후반부, p.15–16)

- **Simulation** — SERGIO v1.0.0 [Dibaeinia 2020 Ref. 11], DS6 differentiation network. 저자가 SERGIO source를 *수정*해 cluster별 $\beta, \gamma$ 변화 허용. Base rate × Uniform(0.5, 1.5), cluster별 × Uniform(0.75, 1.25). cluster당 100 cells. Dropout 20조건 (shape=1, percentile 0→95 5단계), cell-number 13조건. 각 조건 10 dataset.
- **scEU-seq cell-cycle** [Battich 2020 Ref. 3, GSE128365] — Dynamo의 `recipe_kin_data` / `recipe_deg_data` 수정 버전으로 cluster별 ground-truth-ish rate 계산. PULSE/CHASE 분리, cluster당 동일 cell 수 (6~30 cluster). DeepKINET·cellDancer·DeepVelo 각각 100회 반복.
- **scNT-seq hematopoiesis** [Qiu 2020 Ref. 4, Qiu 2022 Ref. 13] — 두 time batch에서 Dynamo로 cluster-level degradation rate, DeepKINET conditional VAE로 batch label 처리. unspliced/spliced moment 상관 > 0.7인 75 gene 제외.

### 7. Method 한계 (저자가 명시한 것)

저자 표현 (Discussion, p.12):

1. "Employs a unified model to estimate splicing and degradation rates, which can lead to correlation trends among these rates (Additional file 1: Fig. S1d, S2c, S5)" — splicing rate와 degradation rate가 같은 모델에서 동시에 나오므로 *완전 독립 추정은 불가*. 다만 본 논문은 cellDancer/DeepVelo보다 *상대적으로 낮은* 상관을 보고.
2. "The simultaneous estimation of RNA velocity and kinetic rates presents a challenge, indicating the need for further methodological enhancements and additional constraints" — velocity와 rate의 동시 추정 자체가 underdetermined.
3. "Eliminating the assumption of fixed transcription rates ... would increase the number of parameters, and further investigation is required" — 본 논문은 transcription rate는 여전히 cell-uniform 가정. MultiVelo [@li2023multivelo Ref. 46] 같이 chromatin accessibility로 transcription rate를 modeling하는 접근이 더 현실적이라고 *직접 언급*.
4. "RNA velocity analysis in distinguishing mRNA isoforms" 제약 — alternative splicing이 본질인 cancer 등에 적용 시 isoform 구분 부재가 한계 (p.13).

검토필요: "Velocity와 rate 동시 추정의 indeterminacy"가 정확히 어떤 metric으로 측정되는지(예: Hessian의 condition number)는 본문에 정량화되지 않음. Sup. Fig. S1d, S2c, S5는 split-deg correlation을 *방법 간 비교*만 함.

## Results

### Dataset 1 — Simulated SERGIO data (Fig. 2 + Fig. S1)

저자 표현: "DeepKINET's accuracy exceeds that of cellDancer and DeepVelo" (Fig. 2b 캡션).

**Dropout 변화 실험 (Fig. 2b)**: 20 dropout 조건 × 10 dataset = 200 dataset. set-rate vs estimated-rate Pearson correlation을 scatter plot으로 보고.

- DeepKINET: splicing/degradation 모두 *positive correlation* 유지.
- cellDancer: splicing positive but degradation **negative**.
- DeepVelo: splicing **negative**, degradation positive지만 DeepKINET보다 낮음.

**Cell-number 변화 실험 (Fig. 2c)**: 13 cell-number 조건 × 10 dataset = 130 dataset. Box plot.

- DeepKINET: 항상 positive correlation, cell 수 작아도 안정.
- cellDancer: splicing은 positive지만 안정화에 더 많은 cell 필요. degradation은 *cell 수가 늘어도 정확도가 떨어짐* (p.5).
- DeepVelo: cell 수 증가에도 splicing 추정 안정 불가.

**Split-deg 독립성 (Fig. S1d)**: estimated $\beta_n$과 $\gamma_n$ 사이 상관이 DeepKINET이 가장 낮음 → "splicing/degradation을 독립적으로 추정 가능"이라고 결론 (p.5).

해석: simulation은 *DeepKINET 자체 룰로 만든 SERGIO 변형*이라 self-favorable risk가 있다. 다만 저자가 "rate 변화는 cluster별 uniform 분포에서 sampling"이라고 명시했고, 같은 dataset에 cellDancer/DeepVelo를 동일 조건으로 돌렸으므로 *relative comparison*은 fair.

### Dataset 2 — scEU-seq cell-cycle (Fig. 3 + Fig. S2)

**PULSE 실험 (Fig. 3b)**: 100회 반복. Dynamo-derived rate와의 correlation box plot.

- DeepKINET: splicing/degradation 모두 positive correlation. negative 한 번도 없음.
- cellDancer: degradation에서 *명백한 negative correlation*.
- DeepVelo: degradation에서 CHASE 실험만 negative.
- Splicing rate 정확도는 DeepKINET ≈ cellDancer ≈ DeepVelo (저자 표현: "comparable performance").
- Degradation rate에서 DeepKINET 단독 우위.

**CHASE 실험 (Fig. S2b)**: 동일 결과 패턴. 저자는 "PULSE가 cell-cycle 분포 균등이라 더 reliable" (p.5)이라 언급.

**Gene clustering by rate (Fig. 3c–e)**: PULSE rate로 gene cluster 9 추출 → GO term "cell cycle" 풍부 (g:Profiler, BH correction). splice/deg correlation 양상으로 gene 분류.

검토필요: Pearson correlation 값의 *정확한 수치*(예: median 0.X)는 본문 텍스트에 명시되지 않음. Box plot 값만 제공. PDF 추출에서도 수치 미발견 — 검토필요.

### Dataset 3 — scNT-seq hematopoiesis (Fig. S3)

저자: "DeepKINET estimated the differentiation trajectory of hematopoietic cells, which was consistent with the results in the Dynamo paper" (p.6).

- 두 time batch 간 degradation rate ratio를 Dynamo값과 비교.
- DeepKINET이 cellDancer/DeepVelo를 능가 (Fig. S3c).
- Conditional VAE로 batch effect 처리 (time을 batch label로 사용, p.16).

해석: scNT-seq는 *transcription + degradation*까지 dynamo로 추정 가능한데 본 논문은 *degradation ratio만* 비교했다. transcription rate는 본 논문 모델에서 cell-uniform이므로 비교 자체가 불가했을 것.

### Dataset 4 — Mouse forebrain (Fig. 4)

[La Manno 2018 Ref. 5, SRP129388]. 신경 differentiation trajectory. RBP target analysis.

- **Gene clustering** (splicing rate / degradation rate 별도로 cluster) → Fisher's exact test로 CLIPdb [Yang 2015 Ref. 51] eCLIP target 부합 (BH correction).
- **RBP expression vs target rate correlation** (Fig. 4c): target gene의 correlation이 non-target보다 *absolute value 유의*하게 크다 (Levene's test).
- **RBFOX1, RBFOX2** → target *splicing* rate와 양적 상관 (Fig. 4d, one-sided t-test). 외부 맥락: RBFOX1/2는 alternative splicing의 잘 알려진 regulator [Conboy 2017 Ref. 15] — 본 결과는 known biology와 부합.

### Dataset 5 — Breast cancer primary/metastatic (Fig. 5 + Fig. S4)

[Liu 2022 Ref. 19, GSE167036]. 환자 5의 epithelial cell (Cell Ranger + Velocyto + inferCNVpy로 cancer cell 추출, p.16). 15,269 primary + 642 metastatic.

- Splicing/degradation rate가 primary vs metastatic 사이에서 크게 변하는 gene 추출 (t-test, BH). 추출된 gene 중 KDM6A, PGR, PIK3CA, PRKAA1, TPM2, TP63, USP9X, TIMP2 등 8개가 *기존 metastasis 문헌*과 연결 (Ref. 20–27).
- RBM47 expression vs target splicing rate linear regression: primary와 metastatic 사이 slope가 다른 gene을 OLS interaction term ($\beta_2 = 0$ null)으로 검정, BH 보정. CD2AP, GFRA1, EPB41 같이 *breast cancer 외 cancer*에서 metastasis 연관된 gene들이 추출됨.

해석: 이 부분은 method validation이 아니라 *biological application*. 발견된 gene들이 known biology와 부합한다는 indirect validation으로 쓰는 논리.

### Dataset 6 — MDS-RS SF3B1 mutation erythroid lineage (Fig. 6)

[Adema 2022 Ref. 41]. 7 MDS-RS 환자 (SF3B1 mutation) + 2 healthy donor. Conditional VAE로 환자 batch 처리.

- SF3B1 target gene의 *splicing rate*가 mutant cell에서 유의하게 낮음 (one-sided paired t-test, Fig. 6d).
- 가장 크게 감소한 top 3: WAS, APOE, CHAC1 → 모두 hematologic malignancy/cancer 관련 (Ref. 42–45).
- SF3B1 expression-target rate correlation: mutant cell에서 낮아짐 (Fig. 6f).

저자 해석 (p.11): SF3B1 mutation은 alternative 3' splice site 사용을 유도 → unspliced로 잘못 분류되는 read 증가 → RNA velocity 모델의 "splicing rate" 정의에 따라 *낮은 splicing rate*로 보이는 것이 *consistent*. 즉 본 모델이 mutation-driven splicing 이상을 *기대 방향*으로 capture.

검토필요: 이 해석은 "RNA velocity의 splicing rate 정의가 alternative 3' SS shift를 *기능 저하*로 잘 모사한다"고 가정. 만약 alternative SS가 *기능적*이라면 이 framing이 over-interpretation일 가능성.

### 전체 결과 요약

| Validation 종류 | Dataset | DeepKINET vs cellDancer | DeepKINET vs DeepVelo |
|---|---|---|---|
| Simulation (정량 ground truth) | SERGIO 20×10 + 13×10 | 항상 우위 | 항상 우위 |
| Metabolic labeling (proxy ground truth) — splicing | scEU-seq PULSE/CHASE | comparable | comparable |
| Metabolic labeling — degradation | scEU-seq PULSE/CHASE | DeepKINET 단독 positive | DeepKINET 우위 (CHASE는 DeepVelo negative) |
| Metabolic labeling — degradation ratio | scNT-seq hematopoiesis | DeepKINET 우위 | DeepKINET 우위 |
| Independence (splice-deg 상관) | All | DeepKINET 더 낮음 | DeepKINET 더 낮음 |
| Biological consistency | Forebrain/Breast/MDS-RS | RBP, mutation effect와 부합 | — |

## Figures

### Figure 1 — Conceptual overview (p.3)

#### 패널별 설명
- (a) 입력 (unspliced/spliced) → DeepKINET pipeline → 출력 (cell별 kinetic rate). 응용으로 gene clustering, cell-population별 rate variation, RBP-target rate connection 3가지 표시.
- (b) mouse pancreas dataset — DeepKINET velocity를 UMAP에 투영 + PAGA [Wolf 2019 Ref. 10] trajectory.
- (c) 한 gene의 expression / splicing rate / degradation rate를 cell-level로 UMAP에 컬러 코드.

#### 본문에서 강조한 비교
- "DeepKINET addresses heterogeneity in kinetic rates spanning genes and cells, which is ignored by existing methods [5, 6]" (p.2).

#### 해석 시 주의점
- Pancreas는 정량 benchmark에 안 쓰임 — Fig. 1은 *시연*. cellDancer/DeepVelo 비교는 Fig. 2부터.

### Figure 2 — Simulated data benchmark (p.4)

#### 패널별 설명
- (a) Top-correlation gene 시각화 — 한 gene의 set rate와 estimated rate를 UMAP에 함께 표시.
- (b) 20 dropout × 10 dataset = 200 dataset의 mean correlation scatter.
- (c) 14 cell-number × 10 dataset box plot.

#### 본문에서 강조한 비교
- DeepKINET *항상* DeepVelo·cellDancer 능가. cellDancer degradation negative, DeepVelo splicing negative.

#### 해석 시 주의점
- Set rate는 *cluster별 uniform distribution sampling*이므로 single-cell heterogeneity를 *cluster* 수준으로만 inject. 실제 단일세포 heterogeneity 자체는 ground truth 부재 — 검토필요.

### Figure 3 — scEU-seq cell-cycle validation (p.6)

#### 패널별 설명
- (a) PULSE data의 Geminin-GFP/Cdt1-RFP 기반 cell-cycle embedding + DeepKINET cluster + velocity.
- (b) Dynamo rate vs DeepKINET/cellDancer/DeepVelo rate correlation box plot (100회).
- (c) splicing/degradation rate heatmap, cell은 cell-cycle 순으로 sort, gene은 cluster 순으로 sort.
- (d) Cluster 9 (cell-cycle gene 풍부)의 GO term.
- (e) splice-deg correlation 다른 gene 시각화.

#### 본문에서 강조한 비교
- "DeepKINET showed positive correlations, outperformed cellDancer and DeepVelo in terms of accuracy in degradation rates" (p.6).

#### 해석 시 주의점
- ground truth는 *Dynamo-derived cluster-level rate*. Dynamo 자체도 model assumption에 의존 (저자 명시 p.5). 따라서 strict ground truth가 아니라 "labeling data 기반 best estimate".

### Figure 4 — Forebrain RBP analysis (p.7)

#### 패널별 설명
- (a) PAGA trajectory of forebrain.
- (b) RBP target × kinetic-rate gene cluster Fisher's exact test dot heatmap.
- (c) RBP expression vs target/non-target rate correlation joint plot.
- (d) RBFOX1/RBFOX2 → target splicing rate box plot.
- (e) RBFOX1/2 expression + target splicing rate UMAP.

#### 본문에서 강조한 비교
- target gene rate-RBP expression correlation이 non-target보다 유의 (Levene's test).

#### 해석 시 주의점
- RBP target은 *bulk eCLIP* (CLIPdb)로 정의. cell-type-specific binding 차이는 반영 안 됨.

### Figure 5 — Breast cancer metastasis (p.10)

#### 패널별 설명
- (a) UMAP + velocity, primary→metastatic direction.
- (b) splicing/degradation rate 변화 큰 gene 상위 (t-test).
- (c) 그 gene들의 expression/rate UMAP.
- (d) RBM47 interaction term significant gene bar plot.
- (e) RBM47 vs CD2AP splicing rate scatter.

### Figure 6 — SF3B1 MDS-RS (p.11)

#### 패널별 설명
- (a) 환자별/mutation status별 UMAP.
- (b) PAGA trajectory.
- (c) SF3B1 expression UMAP.
- (d) gene별 SF3B1 mutant vs WT splicing rate scatter + paired t-test.
- (e) target vs non-target SF3B1-expression correlation.
- (f) WT vs mutant cell에서 SF3B1-target correlation 비교.

## Tables

본문에 정식 Table 없음. 모든 정량 결과는 Figure 안의 box plot/scatter로 제시. Supplementary에도 Table 없이 Figure만 5개. 검토필요: 정확한 correlation 수치가 본문에 텍스트로 명시되지 않은 점은 *재현 검증* 관점에서 약함.

## Supplementary Information

### Supplementary Figure 1 (simulation 보조)
- (a) UMAP + PAGA on simulated data — DeepKINET이 정확한 differentiation 방향 추정.
- (b) lowest-correlation gene 시각화 (실패 사례).
- (c) gene을 expression 합으로 quintile 나눠 quintile별 correlation box plot — 고발현 gene일수록 정확.
- (d) splice-deg correlation 비교 — DeepKINET이 가장 낮음.

### Supplementary Figure 2 (scEU-seq CHASE 보조)
- (a) CHASE embedding + cluster + velocity. "cell density biased"라고 명시.
- (b) CHASE correlation box plot. PULSE와 동일한 결론.
- (c) split-deg correlation. cellDancer/DeepVelo가 DeepKINET보다 높음.
- (d) expression quintile별 correlation.

### Supplementary Figure 3 (scNT-seq)
- (a) PAGA trajectory.
- (b) time cluster 정의.
- (c) Dynamo와의 degradation ratio correlation.
- (d) split-deg correlation.

### Supplementary Figure 4 (breast cancer 보조)
- (a) cancer type + velocity + PAGA.
- (b) highly variable RBP × target/non-target rate correlation.
- (c) RBM47 target/non-target splicing rate correlation (t-test).
- (d) interaction term significant gene 정렬.
- (e) RBM47 expression + CD2AP splicing rate UMAP.
- (f) interaction term가장 변화 없는 gene scatter (음성 통제).

### Supplementary Figure 5 (전체 split-deg correlation 정리)
- 모든 dataset에서 split-deg correlation을 100회 추정한 평균. DeepKINET이 *가장 낮음*. 다만 "weakly correlated"라고 인정 (caption).
- 캡션 문장: "Splicing and degradation are weakly correlated. However, the accuracy of DeepKINET has been confirmed with simulated data and metabolic label data; thus, it captures real values."

### Additional file 2 — Review history
본문은 링크만 (DOI 부록). 직접 확인 안 함 — 미제공.

### Reporting Summary (docx)
미제공: `sources/mizukoshi-2024-deepkinet-supp-2-reporting-summary.docx`는 본 분석 환경에서 직접 파싱 안 됨. Nature Portfolio standard form (statistical test, replication, randomization 체크리스트) 일반 포맷일 것으로 추정.

## 분석 자체에 대한 메모

- 본 paper는 epigenomic-lag *직접* method가 아니다. *kinetic-rate validation reference*로 우리 Week2 evidence bundle을 보강한다.
- 검토필요: Section "Validation using metabolic labeling experimental dataset" (Methods, p.15)이 chromatin lag validation으로 *어떻게 mapping*되는지는 별도 brainstorm 필요. lens-academic의 "validation design transferability" 섹션에서 정리.
- 질문: scEU-seq를 *우리 HSPC pipeline*에 *직접* 시도하면 어떤 cost/regulatory 문턱이 있는가 → lens-industry에서 다룸.
- 질문: DeepKINET이 추정하는 cell-specific $\beta_n$, $\gamma_n$을 *chromatin opening rate*와 동등하게 볼 수 있을까? RNA velocity 방정식의 $\beta$는 unspliced→spliced 변환이고 chromatin opening은 *전사 전 단계*이므로 동등 매핑은 불가. 그러나 "cell-state-dependent kinetic parameter를 deep generative model로 추정 + benchmark"라는 *방법론 골격*은 매우 transferable — 이 점이 academic-citation 가치의 핵심.
- 질문: Discussion p.12에서 저자가 *직접* MultiVelo [@li2023multivelo]를 언급하며 "transcription rate를 chromatin accessibility로 modeling하는 것이 더 현실적"이라 인정 → DeepKINET 후속 work가 MultiVelo-style extension이 될 수 있다고 *저자 본인이* 신호. 우리 epigenomic-lag stack과 직접 접점.
