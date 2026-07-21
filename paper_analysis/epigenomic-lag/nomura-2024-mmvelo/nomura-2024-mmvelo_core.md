# mmVelo: A deep generative model for estimating cell state-dependent dynamics across multiple modalities

Citation: `@nomura2024mmvelo` — Nomura S, Kojima Y, Minoura K, Hayashi S, Abe K, Hirose H, Shimamura T. bioRxiv preprint (2024). DOI: 10.1101/2024.12.11.628059. 본 분석은 `sources/nomura-2024-mmvelo.pdf` (27 페이지, bioRxiv v1 / December 17, 2024 posting) 기반.

> **Preprint disclaimer**: 본 자료는 *peer review를 거치지 않은* bioRxiv preprint이다. PDF 각 페이지 footer에 "this preprint (which was not certified by peer review) is the author/funder"로 명시. 모든 수치·claim은 peer-review 전 결과로 취급하고 정식 출판 버전이 나오면 재검증한다 (`검토필요:` 표시).

## Executive Summary

- **무엇**: scRNA-seq splicing kinetics 기반 RNA velocity를 multimodal cell-state 공간으로 끌어올린 뒤 ATAC decoder로 다시 mapping해 **single-peak resolution chromatin velocity**를 추정하는 mixture-of-experts variational autoencoder (PDF p.1 Abstract, p.3 §2.1).
- **모델 / 방법**: Multimodal MoE-VAE로 latent $z_n$ 추론 후, RNA splicing kinetics로 observed velocity target $ds_n/dt_{\text{obs}} = \tanh(\beta \odot C^u \odot f^u(z_n) - \gamma \odot C^s \odot f^s(z_n)) / \|\cdot\|_2$ 를 만들고, transition encoder $q(d_n|z_n)$가 short-step transition을 추정. Chromatin velocity는 $\Delta \text{ATAC} = C^a \odot (f^a(z_n + \rho d_n) - f^a(z_n))$ ($\rho = 0.01$)로 *peak-level decoder를 통과한 차분*으로 정의 (PDF p.13–14 §5.4–5.5).
- **핵심 결과**:
  - ① **10x E18 mouse brain** — Neurod2 promoter (`chr11:98329299-98330151`) vs enhancer (`chr11:98320243-98320844`) 두 peak에서 enhancer→promoter→spliced mRNA 순서의 lag을 직접 시각화 (PDF p.4 §2.2, Fig 2c-e). Peak-level chromatin velocity로 9 Leiden 클러스터를 만들고 cluster F에서 Zbtb2를 chromatin-remodeler regulator로 동정.
  - ② **SHARE-seq mouse skin (hair follicle, GSE140203)** — hair shaft-cuticle/cortex lineage에서 spliced/unspliced/gene-aggregated/peak-level 네 가지 velocity consistency score에서 mmVelo가 scVelo·MultiVelo보다 일관되게 높음. Peak-level (Fig S3m)은 mmVelo only — scVelo/MultiVelo는 *peak-level velocity를 정의조차 못함* (PDF p.4 §2.3, p.26 Fig S3j-m).
  - ③ **Human cerebral cortex (Trevino 2021, GSE162170)** — 101,644 TF-peak 회귀로 *지역적으로 모인* regulatory peak (TF-targeted vs random, Wilcoxon p<0.01) 와 100 kb 이내 TF-regulated peak 농축 확인 (PDF p.6 §2.4, Fig 4c,d). Lef1 locus에서 Elf1·Nfe2l3 peak 분배.
  - ④ **Missing-modality velocity (PCW21 human cortex)** — scATAC-only로 RNA velocity, scRNA-only로 chromatin velocity를 cross-modal 추정해 10-NN multiome velocity와 cosine similarity 비교 (PDF p.9 §2.5, Fig 5b). 3-multiome + 4-singleome = 총 7 individual로 inter-sample variability 분석.
- **우리 적용**: epigenomic-lag 프로젝트의 Week2 *gene-level chromatin aggregation* gap을 직접 메우는 후보. **하지만 peak-level "lag"은 latent transition $\rho d_n$ 한 step에서 ATAC decoder를 두 번 호출한 차분으로 정의**되어, MultiVelo처럼 *per-peak ODE rate*를 estimate하지 않는다 → 우리 lag framework에 차용할 때는 ablation 후 적용 (use_case: `methodology-reference`, `pipeline-applicable`, `academic-citation`).
- **심층**: 한계·재현 ROI는 `nomura-2024-mmvelo_lens-academic.md` / `nomura-2024-mmvelo_lens-industry.md` / `nomura-2024-mmvelo_methodology-brief.md` 참고.

## Identity

- **Title**: mmVelo: A deep generative model for estimating cell state-dependent dynamics across multiple modalities
- **Authors**: Satoshi Nomura¹, Yasuhiro Kojima², Kodai Minoura¹,³, Shuto Hayashi⁴, Ko Abe⁴, Haruka Hirose⁴, Teppei Shimamura¹,⁴† (¹Nagoya Univ. Medicine, ²National Cancer Center, ³Japanese Red Cross Aichi, ⁴Institute of Science Tokyo)
- **Year / Venue**: 2024 — bioRxiv preprint v1 (posted 2024-12-17), document_type `preprint`. **Not peer-reviewed.**
- **DOI**: 10.1101/2024.12.11.628059
- **License**: CC-BY 4.0 (PDF 각 페이지 footer)
- **Citation key**: `nomura2024mmvelo`
- **Code**: https://github.com/nomuhyooon/mmVelo (PyTorch implementation, PDF p.23 §10.3)
- **Datasets**: 10x E18 mouse brain (10x Genomics public), SHARE-seq mouse skin (GEO `GSE140203`), human cerebral cortex (GEO `GSE162170`, Trevino et al. 2021) — PDF p.23 §10.3.

## Background

### 문제의 출발점

Single-cell multiomics (SNARE-seq, Paired-seq, SHARE-seq, 10x Multiome)는 한 cell에서 transcriptome + regulome을 동시에 측정해 *cross-modal regulatory relationship*을 추정할 토대를 제공하지만, sequencing이 destructive이므로 *time snapshot* 만을 준다 (PDF p.1–2 §1). 시간 정보를 회복하려는 두 가지 표준 경로 — trajectory inference, RNA velocity — 모두 한계:

- **Trajectory inference** (Trapnell, Haghverdi, Setty, Palantir 등): graph 위 1D pseudotime을 부여. *방향성*은 별도 prior가 필요하고, 1D timeline에 직교하는 변화는 잡지 못한다 (PDF p.2 §1).
- **RNA velocity** (La Manno 2018, scVelo): unspliced/spliced ratio + splicing kinetics ODE로 *short-step time derivative*를 prior 없이 산출. 그러나 (1) RNA modality에만 정의되고, (2) chromatin accessibility 같은 다른 modality로 *직접 확장 불가* (PDF p.2 §1).

### 기존 chromatin-dynamics 방법의 gap (mmVelo의 표적)

저자가 명시적으로 비교하는 두 선행 방법:

1. **MultiVelo** (`@li2023multivelo`, Nat Biotechnol 2023) — RNA velocity ODE에 chromatin accessibility의 *gene-level* ODE를 추가. *"this aggregates the peak accessibility for each gene, making it difficult to determine the dynamics at the resolution of the single-peak level"* (PDF p.2 §1). 즉 promoter·distal enhancer가 한 gene 안에서 평균되어 서로 다른 timing이 사라진다.
2. **Chromatin Velocity** (Tedesco 2022, Nat Biotechnol) — heterochromatin/euchromatin 동시측정 데이터를 spliced/unspliced 처럼 다룸. *single-peak level* dynamics는 가능하지만 (1) 특수 측정 기술 필요, (2) gene expression이 같이 측정되지 않아 cross-modal regulation 추론이 불가 (PDF p.2 §1).

저자 주장: *"a method that can simultaneously estimate dynamic changes in gene expression and chromatin accessibility at a single-peak resolution has not yet been developed"* (PDF p.2 §1).

### 본 논문의 필요성

mmVelo는 (a) standard 10x Multiome / SHARE-seq 데이터를 (b) splicing kinetics 기반 RNA velocity로 cell-state dynamics를 잡고 (c) multimodal representation learning으로 peak-level ATAC decoder까지 연결해 *single-peak chromatin velocity + cross-modal generation*을 동시에 달성한다는 포지셔닝.

해석: 본 논문은 *기술적 gap-filling* 위치이며, biological discovery보다 **methodology contribution**이 핵심이다. epigenomic-lag 관점에서 보면 promoter–enhancer 시간 분리(Fig 2e의 Neurod2 enhancer→promoter→mRNA 순서)는 SHARE-seq paper (S. Ma et al., 2020, Fig 2e에서 직접 인용)가 "regulatory regions accessible prior to gene expression"이라 보고한 *기존 관찰의 재현*이며, mmVelo는 그것을 *정량 framework*로 옮겨주는 것이다.

## Methods

### Formal task

입력: per-cell triplet $(a_n, u_n, s_n)$ — chromatin accessibility (peak $p$ index), unspliced mRNA, spliced mRNA (gene $g$ index). 출력: 각 modality의 *temporal derivative* ($\Delta \text{ATAC}$, $\Delta \text{unspliced}$, $\Delta \text{spliced}$) at single-cell, single-peak / single-gene resolution.

### Probabilistic / Statistical 구조

3-stage 학습 (PDF p.11 §5.1):

#### Stage 1 — Multimodal cell-state inference (MoE-VAE)

Generative model (PDF p.12 §5.2):

$$z_n \sim \mathcal{N}(0, I)$$

$$\ell_n^a \sim \mathrm{LogNormal}(\mu_{\ell_a}, \sigma_{\ell_a}^2), \quad \ell_n^r \sim \mathrm{LogNormal}(\mu_{\ell_r}, \sigma_{\ell_r}^2)$$

ATAC: $w_{np}^a | z_n \sim \mathrm{Gamma}(f_p^a(z_n), \theta_p^a)$, dropout indicator $h_{np}^a | z_n \sim \mathrm{Bernoulli}(g_p^a(z_n))$, 최종 observation은 **zero-inflated negative binomial** with mean $\frac{\ell_n^a}{\exp(\mu_{\ell_a} + \sigma_{\ell_a}^2/2)} C_p^a f_p^a(z_n)$ (peak-specific dispersion $\theta_p^a$, zero-inflation $g_p^a(z_n)$).

RNA (spliced·unspliced): negative binomial, gene-specific dispersion $\theta_g^s, \theta_g^u$.

여기서 $C_p^a = \mathbb{E}[a_p | a_p > 0]$ 등은 **average accessibility scale**이다 — 이 한 값이 *peak-level* parameterization을 만든다 (per-peak 별 decoder 출력 $f_p^a(z_n)$이 존재한다는 것이 핵심).

Variational posterior는 **mixture of experts** (Shi 2019, Minoura 2021):

$$q(z_n | a_n, s_n, u_n) = \tfrac{1}{2}\left( q(z_n | a_n) + q(z_n | s_n, u_n) \right)$$

ELBO: 

$$\log p(a_n, s_n, u_n) \geq \mathbb{E}_q [\log p(a_n | z_n, \ell_n^a) + \log p(s_n, u_n | z_n, \ell_n^r)] - \mathrm{KL}[q(z_n | \cdot) \| p(z_n)] - \mathrm{KL}[\text{scaling factors}]$$

stratified sampling으로 추정 (PDF p.13 Eq. 1).

#### Stage 2 — Smoothed-profile decoder fine-tuning (PDF p.13 §5.3)

Sparsity 보완을 위해 *k=50 NN* 이웃 cell의 size-corrected log1p count의 평균 $\mu_{np}^a, \mu_{ng}^s, \mu_{ng}^u$를 target으로, Gaussian likelihood로 decoder 만 fine-tune (encoder fix).

#### Stage 3 — Cell-state dynamics inference (PDF p.13–14 §5.4)

핵심 trick. Transition $d_n \sim \mathcal{N}(0, I)$, scale $\rho = 0.01$. Observed velocity target:

$$\frac{ds_n}{dt}\bigg|_{\text{obs}} = \frac{\tanh(\beta \odot C^u \odot f^u(z_n) - \gamma \odot C^s \odot f^s(z_n))}{\|\tanh(\beta \odot C^u \odot f^u(z_n) - \gamma \odot C^s \odot f^s(z_n))\|_2}$$

이는 *splicing kinetics* (La Manno 2018) ODE $\dot s = \beta u - \gamma s$를 decoder output으로 옮긴 형태이며, tanh로 *gene 간 scale을 평탄화*해 highly expressed gene이 dominate하지 않게 만든다. $\beta \in \mathbb{R}^g$ (splicing rate vector), $\gamma \in \mathbb{R}^g$ (degradation rate vector)는 learnable parameter로 steady-state RNA velocity로 초기화하고 deviation regularization 추가 (PDF p.14).

Predicted velocity (mapping):

$$\frac{ds_n}{dt} | z_n, d_n \sim \mathrm{vMF}\left(\frac{\tanh(C^s \odot (f^s(z_n + \rho d_n) - f^s(z_n)))}{\|\tanh(C^s \odot (f^s(z_n + \rho d_n) - f^s(z_n)))\|_2}, \kappa\right)$$

with concentration $\kappa = 1$. 여기서 vMF (von Mises-Fisher distribution)는 unit sphere 위의 directional distribution으로, *방향 일치도*를 likelihood로 다루겠다는 의도.

ELBO:

$$\log p(ds_n/dt) \geq \mathbb{E}_q [\log p(ds_n/dt | z_n, d_n)] - \mathrm{KL}[q(z_n|\cdot)\|p(z_n)] - \mathbb{E}_q[\mathrm{KL}[q(d_n|z_n)\|p(d_n)]]$$

#### Chromatin / RNA velocity formula (PDF p.14 §5.5)

학습 후, *peak-level* chromatin velocity는 *동일한 transition* $\rho d_n$을 ATAC decoder $f^a$에 통과시킨 차분:

$$\Delta \text{ATAC}_{np} = C_p^a \odot (f_p^a(z_n + \rho d_n) - f_p^a(z_n))$$

$$\Delta \text{unspliced}_{ng} = C_g^u \odot (f_g^u(z_n + \rho d_n) - f_g^u(z_n))$$

$$\Delta \text{spliced}_{ng} = C_g^s \odot (f_g^s(z_n + \rho d_n) - f_g^s(z_n))$$

**해석: 이 식이 "single-peak chromatin velocity"의 정체다.** Per-peak *ODE rate*가 아니라, *공통 transition* $d_n$ (cell-state 공간의 한 방향)을 **peak-specific decoder branch** $f_p^a$에 통과시켜 만든 *projected* 시간 도함수. 모든 peak이 같은 latent transition을 *공유*하되, decoder output dimension이 peak 단위이므로 *서로 다른 magnitude와 sign*을 가질 수 있다. MultiVelo의 per-gene ODE rate ($\alpha_c, \alpha_o, \beta, \gamma$) 같은 *peak-specific kinetic parameter*는 존재하지 않는다.

### 핵심 method insight

1. **"Velocity as a projection of latent transition"** — 모든 modality의 velocity가 *동일한 $d_n$* 한 step에서 *modality-specific decoder*를 두 번 호출한 차분이다. 따라서 modality 간 *방향 일치*가 자연스럽고, peak·gene 어느 단위든 decoder가 output할 수 있는 것은 다 velocity가 정의된다.
2. **Splicing kinetics는 *anchor*에만 사용** — $\beta u - \gamma s$ ODE는 *학습 target*을 만드는 데만 사용되고, 학습된 decoder들은 chromatin/RNA를 *동시에* 한 방향으로 움직이게 된다. 즉 chromatin velocity의 *방향성 prior*가 RNA splicing에 anchored.
3. **MoE-VAE로 *missing modality*가 자연스럽게 처리** — $q(z_n | a_n)$과 $q(z_n | s_n, u_n)$이 따로 학습되므로 inference 시 *하나만* 주어져도 cell-state inference 가능. 이것이 §2.5 cross-modal generation의 토대.
4. **Gene-gene coherence** — 전통 RNA velocity가 gene마다 *독립* ODE를 푸는 반면, mmVelo는 *low-dim manifold* 위의 $d_n$ 한 방향에 모든 gene이 묶이므로 *coherence* 보장 (PDF p.3 §2.1, Nagaharu 2022).

### 이전 방법과의 핵심 차이 (요약 표)

| 항목 | mmVelo | MultiVelo (`@li2023multivelo`) | MoFlow (`@hong2026moflow`) | MultiVeloVAE (`@li2025multivelovae`) | Chromatin Velocity (Tedesco 2022) |
|---|---|---|---|---|---|
| Chromatin 단위 | **per-peak** (decoder output) | per-gene (aggregate) | per-gene (relay) | per-gene (cVAE) | per-peak (heterochromatin/euchromatin) |
| Per-unit kinetic ODE rate | **없음** (decoder + 공통 $d_n$) | 있음 ($\alpha_c, \alpha_o, \beta, \gamma$ per gene) | 있음 (relay velocity) | 있음 (cVAE rates) | 있음 |
| RNA modality 필요? | yes (splicing anchor) | yes | yes | yes | **no** (별도 측정 기술) |
| Cross-modal generation | yes (MoE-VAE) | no | no | yes (cVAE 측면) | no |
| Benchmark vs MultiVelo | **yes** (Fig S3j-m) | — | yes | yes | no |

### Method 한계 (저자가 직접 명시한 부분, PDF p.11 §4)

- RNA velocity 기반이므로 RNA velocity가 잘 안 되는 system (예: 일부 mature 조직)에는 적용 불가 (Bergen et al. 2021).
- *smoothed profile* 사용 — sparsity는 줄지만 *batch / cell-cycle confound*가 흡수될 위험 (Gorin 2022, Zheng 2023).
- Splicing kinetics를 **single kinetic rate** ($\beta, \gamma$ gene 별 한 쌍) 으로 가정 — *variable kinetic rate* (S. Li 2023 cellDancer, Mizukoshi 2024 DeepKINET)는 future direction.
- *Count modeling*이 ZINB로 들어가긴 하지만 smoothed Gaussian fine-tuning 단계가 count 정보를 일부 잃을 수 있음 (Gorin & Pachter 2022, Lederer 2024).

검토필요: $\rho = 0.01$, $\kappa = 1$ 같은 hyperparameter가 모든 dataset에서 고정되었는지 PDF supplementary에서 sensitivity 실험을 찾지 못함 (본문에 명시 없음; bioRxiv preprint이라 supplementary가 본 PDF에 다 embedded 되어있고 Fig S1-S4까지만 존재).

## Results

### Dataset 1 — 10x Multiome embryonic mouse brain (E18) (PDF p.4 §2.2, Fig 2, Fig S2)

**Trajectory recovery**: UMAP 위 cell-state velocity와 chromatin velocity stream plot 모두 known cortex 발달 경로 (radial glia → IPC → excitatory neurons; 내층부터 외층으로 inside-out migration)를 정확히 따라감 (Fig 2a,b).

**Single-peak chromatin velocity 데모 — Neurod2**:
- Promoter `chr11:98329299-98330151` (Fig 2c): 분화 초기에만 accessibility 상승.
- Enhancer `chr11:98320243-98320844` (Fig 2d): 초기 상승 후 *후속 downregulation* — promoter와 다른 시간 프로파일.
- Fig 2e (pseudotime axis): enhancer → promoter → spliced mRNA *순차적* 변화 확인. 이것이 SHARE-seq paper (S. Ma 2020)의 *"regulatory regions accessible prior to gene expression"* 관찰의 정량적 재현.

**Peak clustering (Fig 2f)**: chromatin velocity 위 Leiden clustering (resolution 0.8, cosine similarity) → 9개 peak cluster, pseudotime 따라 *synchronous*하게 변하는 패턴.

**Motif enrichment + TF identification (Fig 2g,h)**: pycisTarget으로 cluster별 motif enrichment → cluster F의 **Zbtb2**가 chromatin velocity와 TF 발현 강한 상관. Zbtb2는 chromatin remodeler + histone chaperone recruit하여 differentiation 조절 (Olivieri 2021 인용).

### Dataset 2 — SHARE-seq mouse skin hair follicle (GSE140203) (PDF p.4–6 §2.3, Fig 3, Fig S3)

**Trajectory + benchmark**: TAC → IRS / medulla / hair shaft-cuticle/cortex 분화 방향 정확히 재현 (Fig 3a,b). **hair shaft-cuticle/cortex lineage**에서 velocity consistency score (Methods §5.7):

$$\mathrm{score} = \sum_t \frac{1}{|C_t|}\sum_{c \in C_t} (\bar X_{t+1} - \bar X_t) \mathrm{sgn}(v_c)$$

(pseudotime 10 bin, log-normalized count, observed-vs-direction agreement)

- **Fig S3j (spliced mRNA velocity)**: mmVelo > scVelo, mmVelo > MultiVelo.
- **Fig S3k (unspliced mRNA velocity)**: mmVelo가 일관되게 높음.
- **Fig S3l (gene-aggregated chromatin velocity)**: mmVelo vs MultiVelo (scVelo는 chromatin velocity를 정의할 수 없어 제외).
- **Fig S3m (peak-level chromatin velocity)**: **mmVelo only** — scVelo와 MultiVelo 모두 peak-level velocity 자체를 정의 못함.

검토필요: 본 분석에는 PDF의 box plot에서 *정확한 수치 (median, IQR, p-value)*를 OCR/text로 뽑을 수 없음. Fig caption에 "consistency score by mmVelo, scVelo, MultiVelo"라 적혀있고 본문에는 "higher accuracy than existing models"라고만 명시 (PDF p.4 §2.3).

**Peak clustering + motif enrichment (Fig 3c,d)**: 9 cluster, 각 cluster motif enrichment로 **Nfix** (NFI TF, stem cell identity 유지, Adam 2020) 와 **Hoxc13** (hair follicle 분화 필수, Jave-Suarez 2002) 동정.

**Motif velocity (Fig 3e-g)**: chromVAR motif deviation score $y_n = (a(z_n)^T m - e_n^T m)/(e_n^T m)$ 의 시간 도함수 

$$\frac{dy_n}{dt} = \left(\frac{dy_n}{dz_n}\right)^T \frac{dz_n}{dt} = \left(\frac{dy_n}{dz_n}\right)^T d_n$$

(PDF p.15 §5.8). UMAP 위에서 hair follicle 분화 연속체 재현. **Hoxc13 (hair shaft)** 과 **Gata3 (internal root sheath; Kaufman 2003)** motif velocity가 분화 방향과 gene expression과 동기화.

### Dataset 3 — Human cerebral cortex / TF-peak regulation (PDF p.6–8 §2.4, Fig 4)

**Three-step regulatory inference** (SCENIC+ framework 확장):

1. Leiden cluster of peaks → pycisTarget motif enrichment → candidate TFs.
2. GRNBoost2로 *chromatin velocity*를 TF mRNA로 regress, feature importance 계산.
3. Permutation test (TF expression matrix를 cell 방향으로 5번 shuffle, gene 방향은 보존) → BH 보정 FDR 0.001로 regulatory edge 추출.

총 **101,644 TF-peak pair** 추론.

**Validation 1 — CRM score (Fig 4b)**: TF-regulated peak의 cis-regulatory module score가 non-regulated peak보다 높음 (Wilcoxon p<0.05) → 동정된 TF-peak 페어가 실제 motif sequence를 가짐.

**Validation 2 — Genomic distance (Fig 4c,d)**: TF-regulated peak 끼리의 genomic distance가 random pair보다 짧음 (Wilcoxon p<0.01). 100 kb 이내에 concentration → TAD 같은 *local regulation* 구조 반영.

**Example — Lef1 locus (Fig 4e, `chr3:130,800,000–131,350,000`)**: 각 peak마다 가장 강한 positive regulator TF 표시. **Elf1**과 **Nfe2l3**이 다수 regulatory sequence 담당, Elf1은 *coding region 근처에 집중* — transcription elongation factor 역할과 일치 (Prather 2005).

### Dataset 4 — Cross-modal generation / missing-modality velocity (PDF p.9 §2.5, Fig 5, Fig S4)

**Proof-of-concept simulation**: human cortical multiome 3 sample 중 한 sample의 RNA 인위적 제거, 다른 sample의 ATAC 인위적 제거 → 제거된 modality의 velocity를 cross-modal inference 후 *10-NN multiome cell의 average velocity*와 cosine similarity (Fig 5b violin).

**Real-data application — PCW21 human cortex (Trevino 2021)**: scRNA-seq + scATAC-seq + Multiome 통합. 
- Chromatin velocity from scRNA-seq alone, RNA velocity from scATAC-seq alone — 둘 다 알려진 differentiation 방향 (Cyc.Prog → nIPC → GluN; mGPC/OPC) 정확히 capture (Fig 5c,d).
- GluN lineage에서 missing-modality chromatin velocity heatmap이 observed accessibility 변화와 일치 (Fig 5e, Fig S4j,k는 mRNA velocity 측면).

**Inter-individual variability analysis (Fig 5f-h)**: 3 multiome + 4 singleome = **7 specimens**. pseudotime 10 bin마다 sample 간 평균 velocity의 variance.
- ATAC velocity의 variability가 RNA velocity보다 먼저 크게 증가 → chromatin이 inter-individual 변동을 먼저 반영.
- Q4 bin의 top-10% variability peak → GREAT으로 hypergeometric enrichment → cerebral cortex development 또는 neurological disorder 관련 gene (Witoelar 2018, X. Zhang 2023, L. Ma 2020 등 인용).

### 전체 결과 요약

- mmVelo는 *peak-level chromatin velocity*라는 새로운 output을 정의하고 (decoder branch의 차분), MultiVelo / scVelo가 *정의조차 못하는* 영역에서 consistency score를 보고.
- Gene-level metric에서도 mmVelo가 scVelo·MultiVelo보다 높지만 *정확한 수치는 PDF Fig S3 box plot에서 본문 textual report 없음* (검토필요).
- Cross-modal generation은 *제한된 proof-of-concept* (3-sample simulation + 1 PCW21 real)이며, 다양한 tissue에서의 robustness는 미보고.

### Ablation / sensitivity

미제공: 본 PDF에는 explicit *ablation table* (e.g., MoE-VAE 빼고 product-of-experts 사용 시) 없음. $\rho$, $\kappa$, k=50 NN size, AdamW learning rate (0.0001 / 0.01), 500 epoch, early-stopping 30 epoch 같은 hyperparameter는 Methods §5.6에 *단일 default*로만 기록.

## Figures

본문 Figure는 5개 (Fig 1–5), Supplementary Figure는 4개 (Fig S1–S4). bioRxiv preprint이므로 별도 supplementary file 없이 모두 본 PDF (p.24–27) 안에 embedded.

### Fig 1 — Overview of mmVelo (PDF p.3)

#### 패널별 설명

- 단일 panel schematic. 입력 (multiome data) → cell state space (MoE-VAE) → cell-state dynamics (splicing kinetics anchored) → modality-specific velocity (RNA, ATAC). Downstream: TF motif accessibility rate 추정, peak 단위 TF regulator 동정, missing-modality velocity 추정.

#### 본문에서 강조한 비교

- *Single-peak resolution* (vs MultiVelo gene-level) 와 *missing-modality velocity* (vs scMM·MultiVI의 missing-modality *profile* 추정)이 핵심 차별점이라 PDF p.3 마지막 문단·p.4 첫 문단에서 강조.

#### 해석 시 주의점

- 해석: schematic이라 *연산 순서*가 모호하다. 실제로는 3-stage 학습 (cell state → smoothed decoder fine-tune → dynamics)이며 *별도 freeze* 단계가 있음 (PDF p.13–14). Fig 1만 보고 end-to-end joint training이라 오해하지 말 것.

### Fig 2 — mmVelo on embryonic mouse brain (PDF p.5)

#### 패널별 설명

- **a-b**: UMAP + stream plot. (a) cell-state dynamics, (b) chromatin velocity. Cell type label (IPC, RG, Astro, OPC, V-SVZ).
- **c-d**: Neurod2 promoter (`chr11:98329299-98330151`) (c) vs enhancer (`chr11:98320243-98320844`) (d) UMAP. 좌측 accessibility, 우측 chromatin velocity.
- **e**: pseudotime 축 위 Neurod2 *세 modality* (enhancer ATAC, promoter ATAC, spliced mRNA) dynamics overlay.
- **f**: peak-level chromatin velocity (좌) 와 accessibility (우) heatmap pseudotime-bin × 9 cluster.
- **g-h**: cluster C (g) / cluster F (h) 의 motif enrichment + 대표 TF의 평균 chromatin velocity와 expression trace.

#### 본문에서 강조한 비교

- *enhancer → promoter → spliced mRNA* 순서 (Fig 2e) — S. Ma 2020 (SHARE-seq) 관찰의 정량적 재현.
- cluster F의 *Zbtb2* 가 chromatin remodeler regulator (Olivieri 2021)로 새로 지목.

#### 해석 시 주의점

- 검토필요: Fig 2e의 *y축 단위*는 PDF caption에 단순히 "Dynamics of Neurod2 in each modality"라 적혀 있어 normalized accessibility / velocity 단위인지 명확하지 않음. 본문 §2.2 "trend" 표현만 있고 quantitative gap (몇 pseudotime unit)은 미보고.
- 해석: enhancer→promoter→mRNA 시간 순서가 시각적으로 보이지만 *통계적 검정* (예: switch-time inference나 cross-correlation)이 없어 *peak-level lag estimate*는 정량화되지 않음 → epigenomic-lag 프로젝트 입장에서는 *방법 자체는 가능*하나 *논문이 보고하는 lag 수치*는 없다.

### Fig 3 — mmVelo on mouse hair follicle (PDF p.7)

#### 패널별 설명

- **a-b**: UMAP + stream plot. TAC, IRS, medulla, hair shaft-cuticle/cortex.
- **c**: peak-level chromatin velocity heatmap, 9 cluster.
- **d**: 각 cluster top enriched TF motifs (text label).
- **e**: motif velocity UMAP (motif 단위 차원 축소).
- **f-g**: Hoxc13 (f), Gata3 (g) — motif activity (좌), motif velocity (중), spliced mRNA (우) UMAP.

#### 본문에서 강조한 비교

- motif velocity가 gene expression과 동기화 → *cistrome regulation*과 *transcription*이 동시에 움직임.
- Hoxc13 (hair shaft 결정), Gata3 (IRS 결정)이 각 lineage 마다 motif velocity로 잘 분리됨.

#### 해석 시 주의점

- 해석: Fig 3e의 *motif velocity UMAP*은 motif 단위 차원축소이므로 cell 수가 아니라 motif 수만큼 점이 찍힌다는 점 caption만 보고 헷갈릴 수 있음.
- 검토필요: Hoxc13 vs Gata3가 *서로 다른 lineage에서 활성화*되는지에 대한 *정량적* 분리 (예: AUROC, separation index)는 보고되지 않음.

### Fig 4 — TF-peak regulation in human cortex (PDF p.8)

#### 패널별 설명

- **a**: 3-step regulatory inference pipeline 도식.
- **b**: scatter plot, x=non-targeted peak CRM score, y=TF-targeted peak CRM score. 각 점이 한 TF motif.
- **c**: scatter, x=TF-targeted peak 간 genomic distance, y=non-targeted peak 간 genomic distance, 같은 chromosome.
- **d**: log-relative frequency distribution of peak-peak distance, targeted vs non-targeted.
- **e**: Lef1 locus (`chr3:130.8M–131.35M`) browser-style view. peak 별 best regulator TF label.

#### 본문에서 강조한 비교

- CRM score 차이 p<0.05 (Wilcoxon).
- TF-regulated peak distance < random p<0.01 (Wilcoxon).
- TF-regulated peak이 ~100 kb 이내 concentration → TAD-scale 가설과 정합.
- Lef1 locus에서 Elf1이 coding region 근처에 위치 — 알려진 *transcription elongation factor* 역할과 일치 (Prather 2005).

#### 해석 시 주의점

- 해석: validation은 *간접*이다 (CRM score는 motif presence 가중치, distance는 prior). *직접적* perturbation (TF KO/KD 후 peak accessibility 변화)이 없으므로 *causal regulation* 주장은 무리.
- 검토필요: 101,644 TF-peak 쌍의 *FDR 0.001 cutoff*가 너무 보수적인지 / 너무 관대한지 (multiple testing scale)에 대한 sensitivity는 없음.

### Fig 5 — Missing-modality velocity (PDF p.10)

#### 패널별 설명

- **a**: 실험 diagram. multiome + scRNA-only + scATAC-only → joint inference.
- **b**: cosine similarity violin (simulated missing-modality velocity vs 10-NN multiome velocity).
- **c**: stream plot — chromatin velocity inferred from scRNA-seq (좌) vs from multiome+scATAC (우).
- **d**: stream plot — RNA velocity inferred from scATAC-seq (좌) vs from multiome+scRNA (우).
- **e**: GluN lineage chromatin velocity heatmap (scRNA-source vs scATAC-source vs observed accessibility).
- **f**: excitatory neuron lineage UMAP colored by pseudotime bin.
- **g**: average inter-sample variability of chromatin velocity (좌) / RNA velocity (우) per pseudotime bin.
- **h**: top-10% variability peak이 enriched된 gene (Q4 bin), GREAT hypergeometric.

#### 본문에서 강조한 비교

- chromatin velocity *fluctuation*이 RNA velocity *fluctuation*보다 *먼저* 증가 → chromatin이 *upstream*에서 inter-individual 변동을 흡수.
- Top variability peak이 cortex 발달 / 신경 질환 관련 gene과 enrichment.

#### 해석 시 주의점

- 해석: "missing modality"라 하지만 *동일 cohort* (Trevino 2021) 내에서 simulation했으므로 *batch effect*나 *기관 간 차이*에는 robust하지 않을 가능성. 외부 cohort cross-validation은 미보고.
- 미제공: 다른 missing-modality method (scMM, MultiVI)와의 *velocity 측면 head-to-head*는 없음 — *profile* 측면에서만 비교됨 (Discussion에서 언급, PDF p.11).

### Extended Data Figures (Fig S1–S4)

- **Fig S1** (PDF p.24): mmVelo graphical model. (a) cell state inference, (b) cell state dynamics inference.
- **Fig S2** (p.25): E18 mouse brain. (a-c) peak/gene-wise imputation correlation (ATAC, unspliced, spliced). (d-e) cell-wise size factor correlation. (f-h) smoothed profile imputation. (i) pseudotime UMAP.
- **Fig S3** (p.26): SHARE-seq mouse skin. (a-i) Fig S2와 동일 구조. **(j-m) velocity consistency score box plot** — (j) spliced, (k) unspliced, (l) gene-aggregated chromatin, (m) peak-level chromatin. (l)은 scVelo 제외, (m)은 scVelo + MultiVelo 모두 제외 (정의 불가).
- **Fig S4** (p.27): human cortical development. (a-i) Fig S2와 동일 구조. (j-k) unspliced/spliced mRNA velocity heatmap (scATAC-source vs scRNA-source vs observed).

## Tables

본문에 정식 numbered Table 없음. 모든 정량 비교는 Figure (특히 Fig S3j-m box plot, Fig 4b-d) 안에 시각적으로만 표현되어 *raw 수치 table*은 본 PDF에 미수록.

미제공: peer-reviewed publication 시 추가될 가능성이 있는 *benchmark metric table* (예: mean ± std consistency score per method per modality) 은 현재 본 preprint에 없음. github code repository에서 reproducible script로 확인 필요 (검토필요).

## Supplementary Information

- **Supplementary Figures**: Fig S1–S4 (위 §Figures 참조). PDF p.24–27.
- **Resource availability** (PDF p.23 §10): code https://github.com/nomuhyooon/mmVelo (PyTorch). Zenodo deposit은 "for publication" 시점 — 즉 publication accepted 전에는 GitHub만 존재.
- **Data availability**: 10x Multiome E18 mouse brain (10x Genomics public), SHARE-seq mouse skin GSE140203, human cortical development GSE162170.
- **License**: CC-BY 4.0 (PDF 모든 페이지 footer).
- **Acknowledgements/Funding**: JSPS (20H04281, 22H04839, 22H04925, 23H04938, 20K22839), AMED (JP22ek0109488, JP22ama221215, JP22ama221501, JP22wm0425007, JP23wm0325068, JP23tm0424226), JST Moonshot R&D JPMJMS2025, ACT-X JPMJAX20AB. Supercomputing: Shirokane (Tokyo U Human Genome Center), TSUBAME3.0 (Tokyo Tech), ABCI (AIST). Editage 영문교정.
- **Author contributions** (PDF p.22): Y.K., K.M. conceived idea. N.S. formulated model & ran experiments under Y.K., T.S. supervision. S.H., K.A., H.H. advised on model & downstream analyses.
- **Competing interests**: None declared (PDF p.23 §9).

미제공: bioRxiv preprint이라 *Supplementary Tables* (S1, S2, ...) 별도 파일 없음 — 본 PDF 안에 모든 supplementary 정보가 embedded (Fig S1-S4와 Methods §5만).

## 분석 자체에 대한 메모

- **C7 (Week2 validation_report) 직접 답변**: mmVelo는 "single-peak chromatin velocity"를 진정한 *peak-level resolution*으로 출력한다 — 단 그 의미는 *peak-specific ODE rate가 아니라* "공통 latent transition $d_n$을 peak-specific decoder branch $f_p^a$에 통과시킨 차분"이다 (PDF p.14 §5.5 의 $\Delta \text{ATAC} = C^a \odot (f^a(z_n + \rho d_n) - f^a(z_n))$). MultiVelo가 *gene 단위 ODE*로 promoter/enhancer를 평균하는 것과 달리, mmVelo는 *decoder output dimension*이 peak이라 *peak마다 다른 velocity 값*을 산출 가능하므로 "single-peak resolution"이라는 표현은 **claim level에서 supported** (overclaim 아님). 단 *kinetic rate inference*가 아니므로 "promoter switch time vs enhancer switch time" 같은 *MultiVelo Model 1/2 식의 lag 정량*은 직접 제공하지 않는다 → 우리 lag framework에 차용하려면 *mmVelo decoder의 차분*에서 *pseudotime-level switch detection*을 추가로 빼야 함.
- **MultiVelo direct benchmark**: SHARE-seq mouse skin hair shaft-cuticle/cortex lineage에서 *velocity consistency score* 기준으로 mmVelo가 MultiVelo를 능가한다고 보고 (PDF p.4 §2.3, Fig S3j-m). *정확한 수치는 본문에 없음* (box plot만), 그러나 *gene-aggregated chromatin*과 *peak-level*에서는 MultiVelo가 *정의조차 못함* (Fig S3l-m caption). 즉 head-to-head 비교가 *제한적이지만 존재*.
- **Cross-paper integration 우선순위**:
  - `@li2023multivelo`와 *동일 dataset (SHARE-seq mouse skin)*에서 비교 가능 → Week2 evidence_bundle에 head-to-head row 추가 가치 큼.
  - `@mizukoshi2024deepkinet` (DeepKINET, 같은 저자 그룹)는 *variable kinetic rate* 후속 — 이 라인의 follow-up paper 추적 필요.
  - `@hong2026moflow` (MoFlow, gene-level relay velocity)와는 *peak-level vs relay* 축에서 보완관계.
- **검토 우선**: GitHub `nomuhyooon/mmVelo` repository의 *README quality / dependency / Zenodo 등록 상태*를 직접 cloning해 확인하면 pipeline-applicable 등급을 더 단단히 매길 수 있음 — 현재는 PDF만으로 *code 존재만* 확인.
- **질문**: $\rho = 0.01$이 모든 dataset에 고정인데, *cell-state space scale*이 dataset 마다 다를 텐데 동일 $\rho$가 consistent한 short-step transition을 보장할까? Sensitivity 실험 부재.
