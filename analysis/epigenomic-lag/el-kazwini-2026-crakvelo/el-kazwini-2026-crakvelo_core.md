# CRAK-Velo — Core Analysis

> 근거: `sources/el-kazwini-2026-crakvelo.pdf` (Genome Biology, Article in Press, 17 pages), `sources/13059_2026_4086_MOESM1_ESM.pdf` (Additional file 1 — 인간 cerebral cortex 데이터셋 + run-time), `sources/13059_2026_4086_MOESM2_ESM.pdf` (Additional file 2 — sensitivity analysis), `sources/abstract.txt`.
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 본문 밖 정보·추론은 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` prefix로 분리한다.

## Executive Summary

- **무엇**: RNA velocity 추정에 chromatin accessibility kinetics를 직접 결합하는 semi-mechanistic model **CRAK-Velo**를 제안. RNA-only velocity가 풀지 못한 "velocity 결과를 underlying regulatory process와 연결" 문제를 chromatin region–gene interaction 수준에서 해결한다고 주장. UniTVelo를 base로 확장한, MultiVelo보다 단순·빠른 chromatin-aware velocity.
- **모델 / 방법**: gene $g$의 unspliced 미분을 두 형태로 동시 정의 — RBF 기반 RNA-only 형태 $\hat{u}'_g(t)$와 scATAC 유래 형태 $u'^{ATAC}_g(t) = c^g(t) - \beta_g \hat{u}_g(t)$. 두 형태를 가중 negative log-likelihood $l(\theta_g)=\pi b_g^2\big(\sum_i |x_g^i-\hat{x}_g^i|^2 + k\,|\hat{u}'_g(t)-u'^{ATAC}_g(t)|^2\big)-\log(b_g)$로 reconcile하고, gene별로 region weight $w_r^g$를 추정. accessibility는 cisTopic($\phi_r^n$)으로 smoothing.
- **핵심 결과**:
  - ① HSPC 10x Multiome (GSE209878, 11,605 cells / 2,000 genes / 3,939 regions) — CBDir에서 세 method 중 최고, platelet을 terminal state로 정확히 식별(UniTVelo 실패, MultiVelo는 erythrocyte→granulocyte의 생물학적으로 의심스러운 flow 추정); KNN cell-type 분류 정확도 다수 gene에서 우위(예: HDC 0.259 vs MultiVelo 0.183).
  - ② E18 mouse brain 10x Multiome (3,365 / 2,000 / 4,002) — Upper/Deeper Layer를 독립 terminal state로 정확 식별(MultiVelo·UniTVelo는 spurious Upper→Deeper flow), latent time도 생물학적으로 일관.
  - ③ Human cerebral cortex 10x Multiome (4,693 / 954 / 844, Additional file 1) — flow는 일관하나 region-level inference는 low coverage(genes ~1,000, 10kb window 내 region 보유 gene ~50%)로 hyperparameter에 민감.
  - ④ Run-time(Table S1): HSPC 15h vs MultiVelo >24h, HCC 6h vs 24h — CRAK-Velo가 일관되게 빠름.
- **우리 적용**: 우리 HSPC 10x Multiome(GSE209878) lag 분석에 **직접 적용 가능**(pipeline-applicable) — 본 논문이 *바로 그 GSE209878 HSPC*에서 MultiVelo 대비 우위를 보고. 단 CRAK-Velo는 chromatin–transcription "lag"를 명시 parameter로 내보내지 않으므로(methodology-reference), region kinetic plot의 temporal coupling을 우리 lag 정의로 재가공해야 함.
- **심층**: 한계·재현 ROI는 `el-kazwini-2026-crakvelo_lens-academic.md` / `el-kazwini-2026-crakvelo_lens-industry.md` / `el-kazwini-2026-crakvelo_methodology-brief.md` 참고.

## Identity

- **Title**: CRAK-Velo: chromatin accessibility kinetics integration improves RNA velocity estimation
- **Authors**: Nour El Kazwini, Mingze Gao, Idris Kouadri Boudjelthia, Fangxin Cai, Yuanhua Huang, Guido Sanguinetti (corresponding: Yuanhua Huang yuanhua@hku.hk, Guido Sanguinetti gsanguin@sissa.it)
- **Year**: 2026 (Received 18 Oct 2024, Accepted 16 Apr 2026, Published online 05 May 2026; preprint bioRxiv 10.1101/2024.09.12.612736)
- **Venue**: Genome Biology (Article in Press — unedited manuscript)
- **DOI**: 10.1186/s13059-026-04086-y
- **Citation key**: `elkazwini2026crakvelo`
- **소속**: SISSA (Trieste, Italy) — Theoretical and Scientific Data Science; University of Hong Kong — School of Biomedical Sciences / Dept. of Statistics and Actuarial Science.

## Background

- RNA velocity (La Manno et al. 2018, [11])는 sequencing의 destructive 특성으로 cellular dynamics를 직접 관찰 못 하는 문제를 splicing 정보로 우회한다. spliced/unspliced read 비율로 각 gene이 sequencing 시점에 up-regulated인지 repressed인지 판정하고, cell population 수준에서 발생·적응 과정을 추론한다.
- 후속 연구들([12]–[17])은 RNA velocity를 확장·정교화했으나, *모두 transcription rate를 데이터로부터 specify하거나 학습해야* 한다. 이 때문에 (a) transcription rate를 binary switch 등으로 postulate하면 모델에 강한 constraint가 걸리거나, (b) 자유롭게 학습하면 parameter 수가 크게 늘어난다.
- 대안은 chromatin accessibility 같은 epigenomic 정보로 transcription rate를 설명하는 것이며, SNARE-seq([18]), SHARE-seq([15]), 10x Genomics Multiome 같은 multi-omic single-cell 기술로 이런 데이터가 점점 가용해졌다.
- 이 아이디어를 가장 먼저 본격 활용한 것이 **MultiVelo**([19]) — chromatin accessibility와 expression을 differential equations latent variable model로 통합한다.
- 본 논문의 출발점: MultiVelo는 정교하지만(elegant) 복잡하다. CRAK-Velo(ChRomatin Accessibility Kinetics in RNA Velocity)는 *더 단순한 모델*로 chromatin accessibility를 개별 gene transcription rate 추정에 직접 통합한다. 동시에 region–gene interaction 해석이라는 부가 가치를 노린다.
- 해석: 본 연구의 정체성은 "새 패러다임"이 아니라 "UniTVelo의 chromatin-aware 확장 + 더 단순·빠른 MultiVelo 대안"이다. 두 선행 method(UniTVelo, MultiVelo)를 명시적 비교 대상으로 두는 method paper.

## Methods

본 논문은 computational methods 중심 paper이므로 Full depth로 분석한다.

### 이 method가 푸는 문제

- **Formal task**: paired single-cell multi-omics(scRNA-seq + scATAC-seq, 10x Multiome)에서, 각 gene $g$의 unspliced/spliced dynamics를 추정하되 transcription rate를 *chromatin accessibility로 설명*하면서 동시에 RNA-only 추정과 정합되도록 reconcile.
- **입력**: (1) scRNA-seq의 spliced $s$, unspliced $u$ count (UniTVelo와 동일 전처리, HVG default 2,000); (2) scATAC-seq의 cis-regulatory region accessibility — cisTopic으로 smoothing.
- **출력**: gene별 phase portrait parameter $\theta_g$, region weight $\{w_r^g\}$, 세포별 unified pseudotime $t_n$, velocity field.
- **추정 대상**: $\theta_g = (\{w_r^g\}, \eta_g, h_g, a_g, \tau_g, \gamma_g, \beta_g, b_g, o_g, i_g)$ for $r \in (1,\dots,R_g)$ (Eq. 12), 그리고 cell time $t_{ng}$.
- **중요한 hidden assumption**: gene 주변 window($R_g = 10^4$ bp, 즉 TSS 기준 상·하류 10kb) 안의 cis-regulatory region이 그 gene의 transcription rate를 제어한다. 한 gene에 여러 region이 연관되지만 특정 조건에서는 *소수 region만* 발현을 제어한다(low-entropy 가정).

### 확률 / 통계학적 구조

- **Model family**: semi-mechanistic — RNA dynamics는 ODE 형태의 mechanistic 골격, transcription rate는 chromatin으로부터 데이터-드리븐하게 구성. 완전 mechanistic ODE도 순수 학습 기반도 아니다.
- **scATAC smoothing (cisTopic)**: binary·sparse scATAC를 topic model로 smoothing. 세포 $n$의 topic 분포 $\lambda^n=(\lambda_1^n,\dots,\lambda_T^n)$ (Eq. 1), region $r$의 topic loading $\psi_r=(\psi_r^1,\dots,\psi_r^T)$ (Eq. 2)로 open probability를 $\phi_r^n = \sum_i^T \lambda_i^n \psi_r^i$ (Eq. 3)로 계산. Gibbs sampler, 3,000 samples, thinning every 10, $T=30$.
- **RNA-only unspliced 미분 (UniTVelo 계승)**: spliced를 RBF로 $\hat{s}_g(t) = h_g e^{-a_g(t_{ng}-\tau_g)^2} + o_g$ (Eq. 4), unspliced를 $\hat{u}_g(t) = \frac{\hat{s}'_g(t) - \gamma_g \hat{s}_g(t)}{\beta_g} + i_g$ (Eq. 5)로 정의. 시간 미분으로 $\hat{u}'_g(t) = \frac{[-2a_g(t-\tau_g)+\gamma_g]\hat{s}'_g(t) - 2a_g\hat{s}_g(t)}{\beta_g^2}$ (Eq. 6), $\hat{s}'_g(t) = -2a_g(t-\tau_g)\hat{s}_g(t)$ (Eq. 7).
- **scATAC 유래 transcription rate**: gene $g$ window 내 region 집합($R_g$)으로 ATAC-derived transcription rate $c^g = \eta_g \sum_r^{R_g} c_r^g(t)$ (Eq. 8). region별 dynamic accessibility는 $c_r^g = w_r^g f(\phi_r^n(t))$ (Eq. 9), normalization $f(\phi_r(t_n)) = \frac{\phi_r^n - \phi_r^{min}}{\phi_r^{max} - \phi_r^{min}}$ (Eq. 10). $c_r^g(t)$는 cell의 accessibility를 unified pseudotime $t_n$ 순서로 재배열해 구성. region weight $w_r^g$가 추정 대상.
- **scATAC 유래 unspliced 미분**: $u'^{ATAC}_g(t) = c^g(t) - \beta_g \hat{u}_g(t)$ (Eq. 11). 즉 unspliced 변화 = chromatin 유래 production rate − degradation.
- **Bespoke likelihood (핵심)**: unspliced 미분의 두 형태(Eq. 6 RNA-only, Eq. 11 ATAC-derived)를 negative log-likelihood로 reconcile. $l(\theta_g) = \pi b_g^2\big(\sum_i^N |x_g^i - \hat{x}_g^i|^2 + k\,|\hat{u}'_g(t) - u'^{ATAC}_g(t)|^2\big) - \log(b_g)$ (Eq. 13), $b_g = \frac{1}{\sqrt{2\pi}\sigma_g}$ (Eq. 14). 여기서 $x_g^i=(u_g^i,s_g^i)$는 관측, $\hat{x}_g^i$는 모델 추정. 첫 항은 phase portrait fit(UniTVelo), 둘째 항은 RNA 미분과 ATAC 미분의 불일치 penalty.
- **noise weighting $k$**: scATAC noise가 inference에 미치는 영향을 조절. 첫 두 dataset은 $k = G/R$ (Eq. 15, $G$=gene 수, $R$=region 수). 셋째 dataset($G>R$, scATAC가 더 noisy)은 $k = \frac{G}{R}\cdot\frac{\mathbb{E}[n^c_{RNA}]}{\mathbb{E}[n^c_{ATAC}]}$ (Eq. 16). $k=0.5$로 명시된 부분(Eq. 13 설명문)과 dataset별 $k$ 공식의 관계는 검토필요(검토필요: Eq. 13 본문 "k=0.5"와 Eq. 15/16의 dataset-adaptive $k$가 동일 $k$인지 별개 scaling인지 본문에서 명확하지 않음).
- **Inference / optimization**: UniTVelo와 동일한 절차. gradient descent로 negative log-likelihood 반복 최소화 — (i) $t^n$ 고정 하에 $\theta_g$ gradient 업데이트, (ii) $\theta_g$ 고정 하에 Euclidean distance 최소화로 cell time $t_{ng}$ 재할당, (iii) unified pseudotime $t_n$ 계산, (iv) region $\phi_r$를 unified pseudotime 순으로 정렬. non-informative init, 초기 $t_n=0.5$, dataset당 10,000 epochs.

### 핵심 method insight

- **기존 방법의 한계**: UniTVelo는 transcription rate를 *순수 데이터-드리븐 parametric(RBF) 추정*만으로 다뤄 chromatin 정보를 못 쓴다. MultiVelo는 chromatin을 differential-equations latent variable model로 통합하지만 복잡하고 느리다.
- **이 논문의 바꾼 가정**: transcription rate를 RNA-only로만 추정하지 않고, scATAC 유래 production rate $c^g(t)$ (Eq. 8–11)로 *직접* 구성해 RNA-only 추정과 likelihood 안에서 reconcile(Eq. 13 둘째 항).
- **새로 추가한 변수**: region weight $w_r^g$ — gene $g$의 transcription에 대한 개별 cis-regulatory region의 기여도. 이것이 부가 산출물(region-gene interaction, entropy ranking, TF enrichment)의 토대.
- **이 변화가 중요한 이유**: 두 가지 목표를 동시 달성 — (1) chromatin 정보로 transcription rate 추정을 *regularize*해 chromatin과 일관되게 만들고, (2) 각 regulatory region이 transcriptional dynamics에 주는 영향을 *정량화*한다. 후자는 RNA-only velocity로는 불가능한 해석 layer.

### 이전 방법과의 차이

- **Baseline**: UniTVelo([12], RNA-only RBF velocity), MultiVelo([19], chromatin-aware DE latent variable model).
- **공통점**: UniTVelo의 RBF spliced model(Eq. 4–7), unified pseudotime, gradient descent optimization, phase-portrait likelihood를 그대로 계승. region이 window 내 없는 gene의 loss는 UniTVelo와 동일.
- **차이점**: UniTVelo 대비 — unspliced 미분의 scATAC 유래 형태(Eq. 11)와 reconcile 항(Eq. 13 둘째 항)을 추가, region weight $w_r^g$ 추정. MultiVelo 대비 — latent variable DE 통합이 아니라 transcription rate를 chromatin으로 직접 구성하는 *더 단순한* 방식, 그리고 region-level 해석 산출물 제공.
- **차이가 크게 나타나는 조건**: terminal state 식별(HSPC platelet, mouse brain Upper/Deeper Layer)과 cell-type deconvolution에서 우위. 단 region-level inference는 coverage 낮은 dataset(HCC)에서 불안정.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: HSPC(GSE209878), E18 mouse brain, human cerebral cortex(HCC, supplementary). metric — CBDir(cross-boundary direction), KNN cell-type classifier accuracy, GO/TF enrichment.
- **개선된 결과**: CBDir에서 CRAK-Velo histogram이 expected biological transition에 가장 부합(Fig 1b), platelet terminal state 정확 식별. KNN accuracy가 다수 gene에서 우위(Fig 1c,d / 2d,e). region weight로 GO·TF enrichment(IKZF1, MEIS1 등)·entropy ranking 산출(Fig 1e,f / 2f,g).
- **Ablation 근거**: 미제공 — 공식 ablation(chromatin term 제거 시 성능 변화)은 본문·supplementary에 없음. 대신 *baseline 비교*(UniTVelo=chromatin 미사용, MultiVelo=다른 chromatin 통합)가 ablation 역할을 부분적으로 대신. 해석: chromatin term을 끄면 UniTVelo가 되므로 UniTVelo와의 격차가 chromatin 통합 효과로 읽힌다.
- **정성적 효과**: KLF1(erythroid), Jag2(neuronal) region kinetic plot에서 chromatin accessibility와 unspliced RNA의 temporal coupling(accessibility 먼저 상승→발현 지연 반응) 시각화(Fig 1g / 2h).

### Method 관점의 한계

- **약한 assumption**: 10kb window가 cis-regulation을 포착한다는 가정 — long-range enhancer는 누락. coverage 낮으면(HCC, gene의 ~50%만 window 내 region 보유) region inference 불안정(Additional file 2).
- **구현/학습 부담**: cisTopic Gibbs sampler 선행 단계 필요(GPU 권장, T=50 기준 HSPC 3h). dataset당 10,000 epochs.
- **lag 명시성 부재**: 검토필요 — CRAK-Velo는 chromatin–transcription "lag"를 별도 parameter로 출력하지 않는다. KLF1/Jag2 plot의 지연은 dynamical system의 부산물로 *시각화*될 뿐, gene별 lag 수치를 직접 내보내는 인터페이스는 본문에 없음. 우리 lag 정의 적용 시 후처리 필요.
- **일반화 불확실 조건**: $G>R$이고 scATAC가 noisy한 dataset에서 $k$ 보정(Eq. 16)이 필요했음 — 데이터 regime별 hyperparameter 민감성.

## Results

세 dataset 모두 paired 10x Multiome. baseline은 UniTVelo(RNA-only)와 MultiVelo(chromatin-aware). 통계 유의성은 enrichment(log-enrichment, p-value) 외에는 명시적 통계 검정 부재 — 주로 정성·정량 비교(CBDir, KNN accuracy histogram). 미제공: confidence interval, p-value(CBDir·KNN), 반복 시드 분산은 본문에 제시되지 않음.

### Dataset 1 — HSPC 10x Multiome (human, GSE209878; MultiVelo 원본 데이터)

- 규모: 전처리 후 11,605 cells / 2,000 genes / 3,939 regions (region은 ≥800 cells에서 검출 + TSS ±10kb). cell annotation은 MultiVelo([19])를 그대로 사용.
- **Velocity field (Fig 1a)**: CRAK-Velo는 세 terminal state(granulocyte, erythrocyte, platelet)를 분리 식별. UniTVelo(RNA-only)는 platelet을 terminal로 식별 실패. MultiVelo는 erythrocyte→granulocyte의 *생물학적으로 의심스러운 flow*를 추정. 이 challenging benchmark는 [19] Fig5에서 chromatin 통합이 spurious velocity를 교정함을 보이려 쓰인 것.
- **CBDir (Fig 1b)**: HSC→MPP, MPP→LMPP, LMPP→GMP, GMP→Granulocyte, MEP→Erythrocyte, Prog MK→Platelet 6개 expected transition에 대한 histogram. CRAK-Velo가 세 method 중 평균 CBDir(black dashed line) 최고, UniTVelo는 음수대(역방향), MultiVelo는 중간. CRAK-Velo flow의 우월성이 명확.
- **Cell-type deconvolution (Fig 1c,d)**: KNN(k=5, Euclidean, train 70%/test 30%) cell-type classifier accuracy. accessibility-unspliced space가 phase space(spliced-unspliced)보다 cell type을 잘 분리. 예시 gene — HDC: CRAK-Velo 0.259 vs MultiVelo 0.183 vs phase 0.213; ADCY6: 0.377 vs 0.165 vs 0.189; STOM: 0.341 vs 0.153 vs 0.182. 전체 gene histogram(Fig 1d)에서 CRAK-Velo가 MultiVelo·phase space 대비 *훨씬 많은 gene*에서 높은 accuracy(분포 우측 이동).
- **Region-gene interaction / entropy ranking (Fig 1e,f,g)**: region weight $w_r^g$ 분포로 entropy metric 정의, top 20% low-entropy gene에 GO 분석 → Immune System, Neutrophil Degranulation, Hematopoietic cell lineage, Platelet Activation 등 조혈·계통 특이 pathway enrichment(Fig 1e). high-weight region의 TF binding(ChIP-Atlas, [22]) log-enrichment → IKZF1(Ikaros, 림프계 commitment), MEIS1(HSC self-renewal) 등 well-characterized TF 상위(Fig 1f). KLF1(erythroid) region kinetic plot(Fig 1g) — proximal high-accessibility region이 먼저 열렸다가 감소하며 transient expression 유도, 발현은 region activity에 *지연 반응*. arrow plot으로 region weight를 TSS 거리별 시각화: proximal region이 activation 시 dominant.

### Dataset 2 — E18 mouse brain 10x Multiome (mouse embryonic brain, day 18)

- 규모: 전처리 후 3,365 cells / 2,000 genes / 4,002 regions (region ≥400 cells + TSS ±10kb). cell type은 MultiVelo annotation(RG, Astro, OPC, IPC, V-SVZ, Upper Layer, Deeper Layer, Ependymal, Subplate).
- **Velocity field (Fig 2a)**: 세 method 모두 broadly similar flow지만, Upper/Deeper Layer terminal state 경계 dynamics에서 차이.
- **PAGA transition (Fig 2b)**: MultiVelo·UniTVelo는 *spurious Upper Layer→Deeper Layers flow* 추정. CRAK-Velo는 두 cell state를 독립 terminal differentiated state로 정확 식별.
- **Latent time (Fig 2a)**: MultiVelo·UniTVelo는 deeper layer가 upper layer *이후* 발생한다고 예측(생물학적으로 부정확). CRAK-Velo는 둘에 유사 pseudotime 할당(생물학적으로 일관). 단 세 method 모두 ependymal cell을 terminal state로 식별 실패(공통 한계).
- **Cell-type deconvolution (Fig 2d,e)**: 예시 gene Tle4 CRAK-Velo 0.593 vs MultiVelo 0.367; Fabp7 0.617 vs 0.361; Ccnd2 0.572 vs 0.389. 전체 gene(Fig 2e)에서도 CRAK-Velo 유의한 우위.
- **Region-gene interaction (Fig 2f,g,h)**: high-weight region TF enrichment(Fig 2f) — Pou3f2(neuronal differentiation/identity), Sox2(NSC self-renewal), Junb 상위. low-entropy gene GO(Fig 2g) — Nervous System Development, Axon Guidance, Neuron Projection Guidance 등. Jag2(Notch ligand) region kinetic(Fig 2h) — pseudotime 진행에 따라 proximal element가 Jag2 발현 상승 직전에 dominant, KLF1과 유사한 구조적 region activity 순서. 저자 주장: chromatin engagement가 transcriptional change를 *동반할 뿐 아니라 선행(anticipates)*.

### Dataset 3 — Human cerebral cortex 10x Multiome (HCC, Additional file 1, [Trevino 2021 Cell])

- 규모: 4,693 cells / 954 genes / 844 regions (scRNA-seq는 MultiVelo 전처리 그대로, region은 TSS ±10kb). $G>R$ regime이라 $k$ 보정(Eq. 16) 적용.
- **결과(Fig S1)**: main figure와 유사 구성(velocity field a, PAGA b, deconvolution c·d, TF enrichment e, GO f, DLGAP2 region kinetic g). deconvolution 예시 — EGR1 CRAK-Velo 0.350 vs MultiVelo 0.255; EOMES 0.478 vs 0.410; FOXP2 0.395 vs 0.428(이 gene은 MultiVelo가 약간 우위). 전체적으로 CRAK-Velo 우세하나 gene별로 혼재. TF: SOX3, BMI1, SUZ12 등 상위. GO: Response to Fibroblast Growth Factor, Neuron Differentiation 등.
- **한계 명시**: 이 dataset은 low coverage — pre-selection 통과 gene ~1,000개, 10kb window 내 region 보유 gene ~50%(다른 두 dataset은 78–87%). flow는 일관하나 *region-level inference가 hyperparameter에 민감*(Additional file 2).

### 전체 결과 요약 (Run-time & Robustness)

- **Run-time (Table S1, Additional file 1)**: hours of compute. HSPC — CRAK-Velo 15 vs MultiVelo >24 vs cisTopic(T=50) 3; Mouse brain — 2 vs 4 vs 0.5; HCC — 6 vs 24 vs 2. CRAK-Velo가 세 dataset 모두 MultiVelo보다 빠름(cisTopic은 별도 선행 step, GPU). CPU: Intel Xeon Platinum 8276/L 2.4GHz, Gibbs sampler는 NVIDIA A100-PCIE-40GB.
- **Sensitivity (Additional file 2, Fig S1/S2)**: topic 수($T=20$ vs $T=50$, 본문 Fig S1 캡션은 $T=20,50$이나 sensitivity 본문은 $T=30,50$로 기술 — 검토필요: $T$ 값 표기 불일치)와 window size(10kb vs 20kb) 변화에 대한 velocity field·$\phi$·$c^g$ 상관 histogram. HSPC·mouse brain은 두 perturbation에 *remarkably robust*(velocity field 상관 대부분 >0.95, >0.9). HCC는 flow는 일관하나 region-level inference가 변동(low coverage 때문).

## Figures

### Figure 1 — HSPC differentiation (main)

#### 패널별 설명
- **(a)** 세 method(CRAK-Velo / UniTVelo / MultiVelo)의 velocity field를 UMAP에 화살표로 표시. cell type별 색. CRAK-Velo가 platelet 포함 3 terminal state 식별.
- **(b)** 6개 expected transition(HSC→MPP 등)별 CBDir histogram, method별 평균(dashed). CRAK-Velo flow 우월성 정량화.
- **(c)** 3개 gene(HDC, ADCY6, STOM)에 대해 phase space(s vs u, 1행) vs accessibility-unspliced space($c^g$ vs u, CRAK-Velo 2행 / MultiVelo 3행). 각 subplot 하단에 KNN accuracy.
- **(d)** 전 gene KNN accuracy histogram — CRAK-Velo / MultiVelo / Phase space 3분포 비교.
- **(e)** low-entropy gene GO dotplot(combined score, % genes in set, log p).
- **(f)** high-weight region TF binding log-enrichment bar(IKZF1, MEIS1, EP300 등 내림차순).
- **(g)** KLF1 — region kinetic plot(좌: region별 accessibility $c_r^g$, 우: normalized unspliced $u$ vs pseudotime), TF binding site intersection bar(거리 $d$별), region weight $w_r^g$ arrow plot(TSS 거리별).

#### 본문에서 강조한 비교
- UniTVelo는 RNA-only라 platelet terminal 식별 실패; MultiVelo는 erythrocyte→granulocyte spurious flow. CRAK-Velo만 세 terminal state 정확(panel a, b).
- chromatin-accessibility space가 cell type 분리에 우월, 특히 *매우 많은 gene에서* MultiVelo 대비 큰 accuracy 향상(panel d).

#### 해석 시 주의점
- 해석: panel c의 예시 gene 3개는 저자가 고른 것으로 cherry-picking 여지. 전체 분포(panel d)가 더 신뢰할 근거.
- 검토필요: panel g의 region kinetic plot에서 "지연(delay)"이 wall-clock time이 아니라 inferred pseudotime 축임에 유의 — 우리 lag(시간 단위) 정의와 직접 매핑되지 않음.

### Figure 2 — E18 mouse brain (main)

#### 패널별 설명
- **(a)** velocity field streamline(UMAP), pseudotime 색. **(b)** PAGA graph(cell type transition). **(c)** subplate/Upper/Deeper Layer 경계 bifurcating flow 상세(inset). **(d)** 3 gene(Tle4, Fabp7, Ccnd2) deconvolution, KNN accuracy. **(e)** 전 gene accuracy histogram. **(f)** TF log-enrichment(Pou3f2, Sox2, Junb 등). **(g)** low-entropy gene GO dotplot. **(h)** Jag2 region kinetic + TF intersection + weight arrow plot.

#### 본문에서 강조한 비교
- MultiVelo·UniTVelo는 Upper→Deeper spurious flow(panel b) + deeper가 나중에 발생한다는 부정확한 latent time(panel a). CRAK-Velo만 두 layer 독립 terminal + 유사 pseudotime.
- chromatin space deconvolution 우위(panel d, e).

#### 해석 시 주의점
- 세 method 모두 ependymal cell terminal 식별 실패 — CRAK-Velo도 못 푸는 공통 한계(본문 명시).

### Extended Data / Supplementary Figures
- **Fig S1 (Additional file 1)**: HCC dataset에 대한 Fig 1/2 analogous 패널(a–g). DLGAP2 region kinetic 포함.
- **Fig S1/S2 (Additional file 2)**: sensitivity analysis — topic 수, window size 변화에 대한 velocity field·$\phi$·$c^g$ 상관 histogram(dataset별 행). HCC만 region-level 민감.

## Tables

본문(main text)에 정식 Table 없음. 모든 Table은 supplementary.

- **Table S1 (Additional file 1)**: 세 dataset(HSPC, Mouse brain, HCC)에 대한 CRAK-Velo / MultiVelo / cisTopic run-time(hours). HSPC 15 / >24 / 3; Mouse brain 2 / 4 / 0.5; HCC 6 / 24 / 2. CRAK-Velo가 MultiVelo보다 일관되게 빠름을 입증 — Conclusion의 "simpler (and faster)" 주장의 근거.
- **Table S2 (Additional file 1에 언급)**: 본문 Results에서 "a data set included in the additional files (Additional file 1: Table S2)"로 언급. 미제공: Table S2의 실제 내용은 확보한 supplementary PDF에 별도 표로 나타나지 않음(Additional file 1에는 Fig S1 + Table S1만 존재) — 검토필요: 본문의 Table S1/S2 번호 참조와 supplementary 실제 번호가 어긋남(본문은 run-time을 Table S1로, HCC dataset을 Table S2로 지칭하나 supplementary에는 Table S1 run-time만 존재).

## Supplementary Information

- **Additional file 1** (`13059_2026_4086_MOESM1_ESM.pdf`): (§1) HCC dataset 성능(Fig S1, Trevino 2021 Cell 데이터); (§2) Performance comparison + Table S1 run-time.
- **Additional file 2** (`13059_2026_4086_MOESM2_ESM.pdf`): hyperparameter sensitivity(topic 수 $T$, window size). HSPC·mouse brain robust, HCC는 region-level inference 민감(coverage 낮음).
- **Data availability**: E18 mouse brain — 10x website(fresh-embryonic-e18-mouse-brain-5-k); HSPC — GEO GSE209878(preprocessed는 MultiVelo tutorial); human brain — GEO GSE162170(+ 저자 GitHub). TF ChIP-seq — ChIP-Atlas([22], hg38 Blood/Neural, mm10 Neural).
- **Code availability**: CRAK-Velo — Zenodo 10.5281/(records/19247214), GitHub StatBiomed/CRAK-Velo; cisTopic python 구현 — github.com/Nour899/cisTopic. Jupyter notebook으로 모든 figure 재현 workflow 제공.

## 분석 자체에 대한 메모

- 질문: 우리 HSPC GSE209878 lag 분석에서 CRAK-Velo를 MultiVelo와 나란히 돌리면, *동일 데이터·동일 annotation*이므로 직접 head-to-head가 가능하다(본 논문이 이미 그 셋업). 그러나 우리가 원하는 산출물은 gene별 chromatin–transcription "lag" 수치 → CRAK-Velo가 출력하는 것은 region weight $w_r^g$ + region kinetic plot이다. lag를 얻으려면 region accessibility peak과 unspliced peak의 pseudotime 차이를 후처리로 계산해야 함. 별도 검증 필요.
- 검토필요: $k$ hyperparameter($k=0.5$ vs Eq. 15/16 dataset-adaptive), topic 수 표기($T=20/30/50$ 혼재), supplementary Table 번호(S1/S2) — 세 곳에서 본문·캡션 불일치. Article in Press(unedited manuscript)라 최종본에서 교정될 가능성. PDF 최종판 재확인 권장.
- 미제공: 공식 ablation(chromatin term on/off), CBDir·KNN의 통계 검정·CI·반복 시드 분산, lag의 명시적 정량화는 본문·supplementary에 없음.
