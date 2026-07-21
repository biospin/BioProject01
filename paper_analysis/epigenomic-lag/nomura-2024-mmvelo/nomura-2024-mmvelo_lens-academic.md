# Lens — Academic — Nomura 2024 mmVelo

> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 본 문서는 *학술적* 한계만 다룬다 (산업·규제는 `nomura-2024-mmvelo_lens-industry.md`).
>
> 본 paper는 **bioRxiv preprint (peer-review 전)** 이므로 본 lens도 "peer-review를 거치지 않은 자료를 학술적으로 다룰 때의 가중치"를 전제로 작성.

## 1. Limitations

### 1.1 저자가 명시한 한계 (PDF p.11 §4 "Limitations of the Study")

저자가 직접 적은 세 항목.

- **RNA velocity 의존**: mmVelo는 cell-state dynamics 추정 자체가 RNA velocity (splicing kinetics ODE)에 anchor되어 있으므로 *RNA velocity가 잘 동작하지 않는 system* (Bergen et al. 2021가 정리한 mature tissue, 일부 development 단계)에는 적용 불가. 저자는 "단 hair follicle처럼 전통 RNA velocity가 어려웠던 system에도 SHARE-seq paper (S. Ma 2020)에서 본 방법으로 다뤄진 바 있으므로 적용 가능 범위가 좁지만은 않다"는 *반박성 단서*를 함께 제시.
- **Smoothed profile 사용**: sparsity 보완을 위해 k=50 NN 평균 (Gorin 2022, Zheng 2023이 RNA velocity 일반에서 비판한 부분)을 사용 → *count modeling 확장* (Gorin & Pachter 2022; Lederer 2024)이 future direction.
- **Single kinetic rate 가정**: $\beta, \gamma$가 gene 별로 *한 쌍*. *Variable kinetic rate* (S. Li 2023 cellDancer; Mizukoshi 2024 DeepKINET — 본 저자그룹의 후속 paper) 도입이 future direction.

해석: 저자 한계는 *기술적 future work* 위주이고, *방법론의 핵심 가정* (예: "공통 $d_n$에 모든 modality decoder가 mapping된다"는 가정 자체에 대한 한계)은 명시하지 않았다.

### 1.2 분석자가 판단한 한계

#### (a) Peer review 부재 — preprint 일반 리스크

- PDF 모든 페이지 footer에 *"this preprint (which was not certified by peer review)"* 명시. 저자는 정식 publication 후 *재실험 / 추가 ablation / 다른 cohort validation*이 요청될 가능성이 큼. 본 분석의 모든 수치 인용은 *preprint v1 (2024-12-17)* 기준이며 publication 시 변경 가능.

#### (b) "Single-peak chromatin velocity"의 정의가 *latent transition projection*이지 *peak-specific ODE rate가 아니다*

- $\Delta \text{ATAC}_{np} = C_p^a \odot (f_p^a(z_n + \rho d_n) - f_p^a(z_n))$ (PDF p.14 §5.5) 식에서 *peak-specific parameter*는 decoder weight 와 $C_p^a$ scale 뿐이다. 모든 peak이 *동일한 transition $d_n$* 한 step을 공유. 이것은 *peak level의 신호 분해*는 가능하지만 *peak 마다 다른 kinetic rate*가 존재하지 않으므로, MultiVelo의 *Model 1 (induction) / Model 2 (repression) 구분이나 switch time inference*가 직접 mapping되지 않는다.
- 검토필요: epigenomic-lag 프로젝트에서 *promoter switch time vs enhancer switch time* 같은 *gene-내부 lag 정량*을 하려면, mmVelo decoder의 차분 값에 추가로 *pseudotime을 따라가는 switch detection* 알고리즘을 얹어야 한다.

#### (c) Benchmark 범위가 좁다

- Velocity consistency score 비교는 *SHARE-seq mouse skin*의 *hair shaft-cuticle/cortex lineage 한 개*에서만 수행 (PDF p.4 §2.3, PDF p.15 §5.7). 저자는 "(1) sufficient cell number, (2) modest orthogonal expansion"이라는 이유를 댔지만, *cherry-picking risk*가 존재.
- *10x mouse brain*과 *human cortex*에서는 *consistency score 직접 비교*가 보고되지 않음 → MultiVelo 대비 *peak-level resolution* 외의 *수치 우위*가 dataset-general한지 미검증.

#### (d) Causal validation 부재

- TF-peak regulation 추론 (101,644 pair, FDR 0.001)의 validation이 *CRM motif score*와 *genomic distance*로만 이루어짐 (PDF p.6–8 §2.4, Fig 4b-d) — 둘 다 *간접 prior signal*이다. *TF perturbation (KO/KD)*이나 *CRISPRi enhancer perturbation* 같은 *causal validation*은 없음.
- 마찬가지로 Neurod2 enhancer→promoter→mRNA 시간 순서 (Fig 2e)도 *시각적 trend*일 뿐, *enhancer를 가렸을 때 mRNA가 안 올라온다*는 perturbation 증거는 없음.

#### (e) Cross-modal generation의 외부 validation 부재

- Missing-modality velocity proof-of-concept은 *동일 cohort* (Trevino 2021, PCW21) 안에서의 simulation. *서로 다른 batch / 기관 / age / disease state* 사이에서도 그 cosine similarity가 유지되는지는 미보고 (PDF p.9 §2.5).
- 미제공: scMM, MultiVI 등 *missing-modality profile inference* method와의 *velocity 측면 head-to-head*는 *Discussion에서만 언급되고 정량 비교 없음* (PDF p.11).

#### (f) Hyperparameter sensitivity 부재

- $\rho = 0.01$, $\kappa = 1$, k=50 NN, AdamW lr 0.0001/0.01, 500 epoch, ELBO early stop 30 epoch — 모두 *단일 default*. *Dataset 별 cell-state space scale*이 다른데 동일 $\rho$가 일관된 short-step transition을 보장한다는 검증이 없다 (PDF p.14 §5.6).
- 질문: 만약 $\rho$를 10배 키우면 chromatin velocity 방향이 그대로 보존될까? 본 분석에서는 코드를 직접 돌리지 않아 확인 불가.

#### (g) 통계적 검정의 *level*이 일관되지 않음

- Fig 4b CRM score는 *Wilcoxon p<0.05*, Fig 4c distance는 *p<0.01*, TF-peak regulation은 *BH FDR 0.001* — 모두 다른 cutoff. *multiple testing scale* (101,644 pair) 대비 FDR 0.001이 적절한지에 대한 sensitivity 부재.

#### (h) Reproducibility *코드 존재*는 하나 *peer-review*되지 않음

- GitHub https://github.com/nomuhyooon/mmVelo (PDF p.23 §10.3) 있으나 *Zenodo deposit은 publication 시점*이라고 명시 — *DOI-cited 버전 코드*는 아직 없음. 정식 publication 전이라 README / dependency / tutorial 품질 별도 검증 필요.

## 2. mmVelo vs MultiVelo / MoFlow / MultiVeloVAE: peak-level resolution claim 비판적 검토

이 sub-section은 Week2 validation_report C7의 직접 답변 역할.

### 2.1 "single-peak chromatin velocity" claim의 정확한 의미

PDF p.2 §1, p.3 §2.1, p.14 §5.5 종합:

- **Claim (저자 표현)**: *"mmVelo accurately estimates chromatin velocity at the single-peak resolution"* (PDF p.2 last paragraph), *"A unique feature of mmVelo is its ability to model chromatin accessibility at the peak level"* (PDF p.3 §2.1).
- **수식적 의미**: $\Delta \text{ATAC}_{np} = C_p^a \odot (f_p^a(z_n + \rho d_n) - f_p^a(z_n))$ — *peak $p$*마다 별도 decoder branch 출력, 따라서 *peak 마다 다른 velocity 값*이 산출된다.
- **수식적 함의 (분석자 해석)**: per-peak *kinetic rate parameter*가 존재하지 않는다. 모든 peak이 *공통 cell-state transition* $d_n$을 *peak-specific decoder weight*로만 differentiate. 즉 *resolution*은 *output level*에서 peak이지만 *dynamics generation*은 cell-state level에서 공통.

### 2.2 비교 — 다른 method들의 chromatin-RNA coupling 단위

| Method | 출처 | chromatin 단위 | per-unit kinetic rate? | RNA-coupling 방식 |
|---|---|---|---|---|
| **mmVelo** | `@nomura2024mmvelo` | **per-peak** (decoder branch) | 없음 (공통 $d_n$) | splicing kinetics anchor → multimodal decoder |
| **MultiVelo** | `@li2023multivelo` | per-gene (peak aggregate) | 있음 ($\alpha_c, \alpha_o, \beta, \gamma$ per gene; Model 1 vs Model 2) | gene-level chromatin ODE + RNA ODE coupled |
| **MultiVeloVAE** | `@li2025multivelovae` | per-gene (cVAE) | 있음 (cell·gene-specific rate via cVAE) | cVAE + decoupling factor |
| **MoFlow** | `@hong2026moflow` | per-gene (relay) | 있음 (relay velocity per gene) | DTW + relay-style transition |
| **Chromatin Velocity** (Tedesco 2022) | non-multiome | per-peak | 있음 (heterochromatin/euchromatin ratio ODE) | RNA 별도 측정 안 됨 |

### 2.3 "Peak-level resolution" claim의 진위 평가

**결론**: claim은 **자체로는 supported**이지만 **MultiVelo가 못하는 *모든* 것을 mmVelo가 하는 것은 아니다**.

- **supported**: peak 단위 velocity 출력 가능, scVelo/MultiVelo는 이 수준의 출력 자체가 불가 (Fig S3m caption 명시).
- **not supported (overclaim 위험)**: 본 paper가 *"peak-specific kinetic parameter"*를 추정한다고 *명시적으로* 주장한 적은 없으나, 독자가 "single-peak resolution = peak 마다 다른 ODE rate"로 오해할 위험이 있다. MultiVelo의 *Model 1/2 switch* 같은 *kinetic interpretability*는 mmVelo에 없다.
- **trade-off**: mmVelo는 *resolution*을 얻은 대신 *kinetic interpretability*를 일부 포기. *epigenomic lag*를 *kinetic parameter (chromatin opening rate, RNA induction rate)*로 정의하고 싶다면 MultiVelo가 더 직접적, *peak-level pseudotime 정렬*로 정의하고 싶다면 mmVelo가 더 직접적.

### 2.4 epigenomic-lag 프로젝트에 미치는 함의

해석: 우리 프로젝트가 "promoter–enhancer 시간 lag → drug response timing"이라는 hypothesis를 따른다면, mmVelo는 *peak-level dynamics output*을 제공하고, 그 위에 *switch-time detection / pseudotime cross-correlation*을 직접 얹어야 한다. MultiVelo / MultiVeloVAE 의 *kinetic rate*는 그대로 사용 가능하지만 peak-resolution이 없다. **세 method를 동일 dataset에서 돌려 비교**하는 것이 Week2 evidence_bundle의 다음 step.

질문: *enhancer–promoter lag*를 정량화할 때 mmVelo decoder output을 어떻게 *time unit*으로 환산할 것인가? $\rho = 0.01$은 *latent space scale*에서의 step size이고 *wall-clock time*과의 관계가 정의되지 않음 (PDF에 명시 없음, 검토필요).

## 3. 매끄럽지 않은 지점 (분석자 관찰)

- **Fig S3 box plot의 정확한 수치가 본문에 없다**. "higher accuracy than existing models"라는 *언어적* 표현만으로 *얼마나 더 높은지*를 알 수 없음 (PDF p.4 §2.3). peer-reviewed publication에서는 일반적으로 *median ± IQR 또는 effect size*가 본문 텍스트에 명시된다 → reviewer가 요청할 가능성 큼.
- **Validation 통계의 cutoff 일관성 부재** (위 1.2 (g)).
- **Discussion이 짧고 limitation 명시가 *기술적 future work*에 치우침** — *biological interpretation 한계*나 *causal claim 한계*는 다루지 않음.
- **TF perturbation validation 부재**에도 불구하고 "putative TFs that regulate chromatin accessibility" 같은 *regulation* 표현을 자주 사용 → reviewer가 *causal language 톤다운*을 요청할 가능성 있음.

## 4. 다음 논문 / 후속 연구 아이디어

### 4.1 Direct extensions

- **Peak-level lag 정량 framework**: mmVelo decoder output의 *peak 시계열* 위에 *switch-time detection* (Gaussian process / change-point) 알고리즘을 얹어 *promoter switch time - enhancer switch time*을 정량 → epigenomic-lag 프로젝트 핵심 산출물 후보.
- **MultiVelo + mmVelo hybrid**: MultiVelo의 *kinetic rate parameter*를 *gene-level prior*로 쓰고 mmVelo의 *peak-level decoder*로 fine-grained dynamics를 얹는 hybrid model. Discussion (PDF p.11)에서 저자도 이 방향을 future direction으로 언급.
- **Variable kinetic rate 통합**: 본 저자그룹의 *DeepKINET* (`@mizukoshi2024deepkinet`)이 variable rate를 다룬다 → mmVelo + DeepKINET 통합 자연스러움.

### 4.2 Validation gap을 메우는 연구

- **CRISPRi enhancer perturbation + mmVelo prediction**: Neurod2 enhancer를 CRISPRi로 가리고 promoter accessibility / spliced mRNA 시계열을 측정 → mmVelo가 예측한 *enhancer→promoter→mRNA lag*가 실제 인과인지 검증.
- **Cross-tissue cross-modal generation**: PCW21 cortex training, hippocampus / spinal cord test → cross-modal generation의 *generalization*을 평가.

### 4.3 Method 차용 후보 (우리 자체 연구)

- 우리 HSPC 10x Multiome 데이터 (GSE209878, kkkim/jamie 담당)에 mmVelo를 적용해 *peak-level chromatin velocity*를 산출 → MoFlow / MultiVelo와 *gene-level lag*와 비교해 *peak vs gene*의 *resolution premium*을 정량.

## 5. Citation 후보 (본인 논문/발표에서 인용할 후보 문장·수치)

| 사용 시나리오 | 인용 형식 |
|---|---|
| "Single-peak resolution chromatin velocity의 필요성 제기" | "MultiVelo and related per-gene aggregation methods cannot resolve the differential dynamics between promoter and enhancer of the same gene (Nomura et al., 2024 bioRxiv [`@nomura2024mmvelo`])" |
| "mmVelo는 SHARE-seq hair follicle benchmark에서 peak-level chromatin velocity를 *정의 가능한 유일한 방법*으로 보고" | "mmVelo is the only method that defines peak-level chromatin velocity in the SHARE-seq mouse skin benchmark, as scVelo and MultiVelo cannot infer velocity at this resolution (Nomura 2024 Fig S3m)" |
| "MoE-VAE 기반 missing-modality velocity는 multi-cohort integration의 새 방향" | "By using a mixture-of-experts variational autoencoder, mmVelo enables joint analysis of multiome data with single-modality scRNA-seq or scATAC-seq, expanding effective sample size (Nomura 2024 §2.5)" |
| "Causal validation 부재를 후속 연구의 motivation으로 인용" | "While mmVelo identifies TF-peak regulatory pairs at the chromatin velocity level, the validation relies on indirect signals (CRM scores, genomic proximity), motivating CRISPRi-based perturbation studies" |

BibTeX key: `@nomura2024mmvelo`

## 6. Final Takeaways

- Week2 evidence_bundle의 *gene-level chromatin aggregation* gap을 *기술적으로* 메우는 가장 직접적 후보.
- Peer review 전이므로 *preprint-tier evidence*로 다루되, **"peak-level chromatin velocity 정의가 가능한 method가 존재한다"는 *존재 증명*은 supported**.
- *Kinetic rate*가 아닌 *projected decoder difference*임을 명확히 인용 — 그렇지 않으면 MultiVelo의 ODE rate와 혼동.
- 후속 연구 우선순위: (1) mmVelo + 우리 HSPC dataset 적용 → peak-level lag 정량, (2) MultiVelo와 같은 dataset 동일 metric으로 head-to-head, (3) CRISPRi enhancer perturbation으로 causal validation.
