# Evidence Bundle

## Scope Summary

- Topic: `epigenomic-lag`
- Research question: gene별 chromatin-transcription lag structure를 정량화하고 epigenetic drug response timing 예측으로 연결할 수 있는 method와 evidence를 비교한다.
- Inclusion: paired chromatin accessibility + RNA 또는 multiome data를 활용하고, chromatin state와 transcription/RNA dynamics의 시간적 관계를 다루는 method paper.
- Current evidence set (full-analysis, 11편): velocity method — `@li2023multivelo`, `@li2025multivelovae`, `@hong2026moflow`, `@li2023celldancer`, `@nomura2024mmvelo`, `@cui2024deepvelo`, `@mizukoshi2024deepkinet`, `@elkazwini2026crakvelo`; benchmark — `@luo2026velocitybenchmark`; biology(HSPC chromatin priming) — `@safi2022chromatinpriming`, `@martin2023hspcchromatin`.
- 2026-06-12 승격: 직전 abstract-only 4편(`@elkazwini2026crakvelo`, `@luo2026velocitybenchmark`, `@safi2022chromatinpriming`, `@martin2023hspcchromatin`)이 PDF 확보 + core/lens/methodology-brief 완료로 **full-analysis로 승격**. 정량 비교가 이제 가능. `@martin2023hspcchromatin`은 review→primary research article(ATAC-seq + CRISPRi)로 자료 유형 정정됨.

## Paper Records

### `li-2023-multivelo` — MultiVelo

- Identity: Li et al., 2023, *Nature Biotechnology*, DOI `10.1038/s41587-022-01476-y`.
- Topic relevance: chromatin accessibility $c(t)$를 RNA velocity ODE 안에 넣어 priming/decoupling을 정량화한 foundational method.
- Research question: RNA-only velocity가 놓치는 chromatin priming과 chromatin-transcription decoupling을 paired multiome에서 어떻게 모델링할 것인가?
- Method / assay / dataset:
  - Method: 3-ODE model + EM latent time + gene state classification.
  - Data: E18 mouse brain, SHARE-seq mouse skin, fetal human cortex, human HSPC 10x Multiome.
- Main claims:
  - chromatin을 넣으면 RNA-only velocity의 backflow와 priming 미포착 문제가 줄어든다.
  - gene을 M1/M2로 나누어 chromatin closing과 transcription repression의 temporal order를 해석할 수 있다.
- Key results:
  - Mouse skin Spearman 0.51 vs scVelo 0.44.
  - Mouse brain state distribution: induction-only 29.5%, repression-only 2.4%, M1 41.4%, M2 26.7%.
  - Median priming 21%, decoupling 19% of total time.
  - Simulation correct model assignment 985/1000 genes.
- Limitations:
  - 저자 명시: TF lag mechanism은 association이고 causal proof는 아님.
  - 해석: single c per gene으로 enhancer-specific kinetics를 볼 수 없음.
  - 해석: transcriptional boost와 simultaneous emergence는 저자가 미해결로 명시.
- Follow-up possibility:
  - 우리 HSPC에서 M1/M2와 cell-cycle confound를 재점검.
  - per-enhancer kinetics로 확장.
- Evidence sources:
  - `analysis/epigenomic-lag/li-2023-multivelo/li-2023-multivelo_core.md`
  - `analysis/epigenomic-lag/li-2023-multivelo/li-2023-multivelo_lens-academic.md`
- Status: `full-analysis`

### `li-2025-multivelovae` — MultiVeloVAE

- Identity: Li et al., 2025, *Nature Communications*, DOI `10.1038/s41467-025-66287-6`.
- Topic relevance: MultiVelo를 continuous, cell-specific, multi-sample, differential-test capable framework로 확장.
- Research question: multi-lineage/multi-sample/partially overlapping modality setting에서 chromatin-RNA dynamics를 probabilistic하게 추정하고 test할 수 있는가?
- Method / assay / dataset:
  - Method: cVAE + ODE decoder, shared latent time, continuous $k_c$/$\rho$, $\delta$/$\kappa$, Bayesian differential test.
  - Data: 10 RNA-only benchmark, EB 10x Multiome, HSPC multi-sample, macrophage/DC, mixed BMMC scRNA + HSPC multiome.
- Main claims:
  - MultiVelo discrete state를 continuous cell-specific coupling/decoupling factor로 일반화.
  - batch correction과 velocity inference를 post hoc chaining 없이 통합.
  - differential dynamics와 in silico perturbation을 velocity framework에서 수행.
- Key results:
  - RNA-only benchmark 10개 dataset에서 6 baseline 대비 전반적 우위.
  - EB dataset에서 NANOG+ root 및 3 germ layer trajectory 회복.
  - HSPC batch 통합에서 scVI/Scanorama 대비 biological conservation 우위.
  - macrophage vs DC driver dynamics 식별.
  - SPI1/GATA1 KO in silico perturbation.
- Limitations:
  - 저자 명시: mature/quiescent cell type에서 RNA quality 의존성.
  - 저자 명시: de novo training 의존, atlas-level pretrained parameter 부재.
  - 저자 명시/peer review: gene-level c aggregation으로 individual cis-regulatory element 직접 modeling 부재.
  - 해석: FDR calibration, perturbation wet-lab validation, hyperparameter sensitivity가 부족.
- Follow-up possibility:
  - 우리 HSPC에서 MultiVelo state vs MultiVeloVAE $\delta/\kappa$ concordance.
  - differential test FDR calibration.
  - multi-donor regularization robustness test.
- Evidence sources:
  - `analysis/epigenomic-lag/li-2025-multivelovae/li-2025-multivelovae_core.md`
  - `analysis/epigenomic-lag/li-2025-multivelovae/li-2025-multivelovae_lens-academic.md`
- Status: `full-analysis`

### `hong-2026-moflow` — MoFlow

- Identity: Hong et al., 2026, *Nature Communications*, DOI `10.1038/s41467-025-67259-6`.
- Topic relevance: latent time-free relay velocity로 chromatin-transcription lag를 직접 정량하는 post-MultiVelo extension.
- Research question: fixed gene labels와 latent time 없이 local neighbor displacement와 chromatin-aware DNN으로 cell-specific chromatin-transcription kinetics를 추정할 수 있는가?
- Method / assay / dataset:
  - Method: cellDancer-style relay velocity + chromatin/RNA DNN heads, Mahalanobis neighbor cosine loss, opening/closing lower-loss selection, DTW c-s lag, m1/m2, DAC score.
  - Data: human brain cortex, mouse skin, mouse brain, human HSPC reused datasets.
- Main claims:
  - latent time-free local relay velocity가 MultiVelo latent-time over-correction을 회피.
  - cell-specific kinetics가 cell-state heterogeneity를 더 잘 포착.
  - CBDir에서 MultiVelo/cellDancer/scVelo를 outperform.
- Key results:
  - Human brain CBDir 0.362 vs MultiVelo 0.211.
  - Mouse skin CBDir 0.144 vs MultiVelo 0.115.
  - Mouse brain CBDir 0.535 vs MultiVelo 0.155.
  - Human HSPC CBDir 0.191 vs MultiVelo 0.063.
  - Fig. 7에서 negative c-s lag mechanism을 rapid RNA turnover/export와 nuclear sequestration/conditional export로 해석.
- Limitations:
  - 저자 명시: long-range enhancer-promoter interaction, transcriptional memory, motif-level regulation 직접 modeling 부재.
  - 저자 명시: gene-wise inference라 pathway-level coordination 제한.
  - 해석: CBDir 단일 metric 의존, ablation 부족, multi-sample/differential test/uncertainty 없음.
  - 검토필요: code license 확인 필요.
- Follow-up possibility:
  - MoFlow vs MultiVeloVAE head-to-head.
  - MoFlow score와 MultiVeloVAE $\delta/\kappa$ concordance.
  - cluster 10 polycomb/speckle hypothesis 재검증.
- Evidence sources:
  - `analysis/epigenomic-lag/hong-2026-moflow/hong-2026-moflow_core.md`
  - `analysis/epigenomic-lag/hong-2026-moflow/hong-2026-moflow_lens-academic.md`
- Status: `full-analysis`

### `li-2023-celldancer` — cellDancer

- Identity: Li, Zhang, Chen, Ye, Wang et al., 2024, *Nature Biotechnology*, DOI `10.1038/s41587-023-01728-5`.
- Topic relevance: MoFlow의 *직접 predecessor*. RNA-only relay velocity framework로 cell-specific kinetics를 *latent time 추정 없이* 학습. chromatin은 §Discussion p9에서 *"could be likewise included"* future direction으로만 언급 — MoFlow가 그 future direction을 실제 구현.
- Research question: multi-stage/multi-lineage scRNA-seq에서 universal kinetic rate assumption 없이 *cell-specific* transcription/splicing/degradation rate를 추정할 수 있는가?
- Method / assay / dataset:
  - Method: gene별 독립 DNN으로 $(u, s) \to (\alpha, \beta, \gamma)$ mapping. *local neighbor cosine similarity max* loss (PDF §Introduction p2, core p.61).
  - Data: scRNA-seq simulation, erythroid maturation, hippocampus development, mouse pancreas (Supp Table 1 비교).
- Main claims:
  - cell-specific kinetics를 *local neighbor displacement*만으로 학습 가능 (PDF §Introduction p2).
  - global latent time 추정 불필요 → ODE analytic solution 불필요 → 다른 ODE (multi-omic chromatin velocity) 확장 가능 (§Discussion p9, core p.111).
  - multi-stage/multi-lineage/dropout/sparse setting에서 scVelo·DeepVelo·VeloVAE 대비 4–30배 simulation accuracy (Supp Table 1, core p.66).
- Key results:
  - Simulation에서 cell-specific kinetic rate 회복 (cellDancer core p.67).
  - 외부 후속 paper (MoFlow Supp Table 1)가 chromatin-aware dataset에서 cellDancer CBDir를 재평가했을 때: HSPC $-0.056$, SHARE-seq $0.026$, cortex $-0.015$ — *RNA-only 본질적 한계*가 quantitative하게 드러남 (cellDancer core p.270, p.488).
- Limitations:
  - 저자 명시: chromatin/multi-omic은 §Discussion future work로만 (core p.152).
  - 해석: real-data benchmark가 정량 directional accuracy metric (CBDir 등) 없이 *시각적 평가만* (core p.270).
  - 해석: gene별 독립 DNN training이라 *cross-gene coordination*은 fit하지 않음.
- Follow-up possibility:
  - MoFlow의 성능 향상이 *relay velocity 계승 자체* 때문인지 *chromatin modality 추가* 때문인지를 분리하는 ablation.
- Evidence sources:
  - `analysis/epigenomic-lag/li-2023-celldancer/li-2023-celldancer_core.md` §Introduction/§Methods/§Discussion 인용 다수
  - `analysis/epigenomic-lag/li-2023-celldancer/li-2023-celldancer_lens-academic.md` Limitations
- Status: `full-analysis`

### `nomura-2024-mmvelo` — mmVelo (preprint)

- Identity: Nomura, Kojima, Minoura, Hayashi, Abe, Hirose, Shimamura, bioRxiv preprint v1 2024-12-17, DOI `10.1101/2024.12.11.628059`. **Not peer-reviewed.** License CC-BY 4.0 (PDF footer). Code: github.com/nomuhyooon/mmVelo (PDF p.23 §10.3).
- Topic relevance: *single-peak chromatin velocity*를 *decoder-level resolution*으로 정의해 세 multiome velocity paper의 gene-level chromatin aggregation 한계를 *부분적으로* 메우는 후보. MultiVelo와 *직접 benchmark*함 (SHARE-seq hair shaft-cuticle/cortex lineage, Fig S3j-m).
- Research question: RNA velocity-derived cell-state dynamics를 chromatin accessibility로 확장해 *single-peak resolution* peak-level chromatin dynamics와 cross-modal generation을 동시에 달성할 수 있는가?
- Method / assay / dataset:
  - Method: mixture-of-experts variational autoencoder. latent $z_n$ + transition encoder $q(d_n | z_n)$ + modality-specific decoders. Chromatin velocity는 $\Delta \text{ATAC} = C^a \odot (f^a(z_n + \rho d_n) - f^a(z_n))$ ($\rho = 0.01$)로 *동일 latent transition* $d_n$을 *peak-specific decoder branch* $f_p^a$에 통과시킨 차분으로 정의 (PDF p.13–14 §5.4–5.5, core p.120).
  - 핵심 메커니즘: **Per-peak ODE rate는 없음** — 모든 peak이 *공통 transition* $d_n$을 공유하되, decoder output dimension이 peak 단위라 *서로 다른 magnitude/sign*을 가질 수 있음 (PDF p.13–14, core p.120). MultiVelo의 per-gene ODE rate ($\alpha_c, \alpha_o, \beta, \gamma$) 같은 *peak-specific kinetic parameter*는 부재.
  - Data: 10x E18 mouse brain, SHARE-seq mouse skin (GSE140203), human cerebral cortex (Trevino 2021 GSE162170), PCW21 human cortex (multiome + scRNA-only + scATAC-only).
- Main claims:
  - *Single-peak resolution* chromatin velocity를 추정 (PDF p.1 Abstract, p.3 §2.1).
  - cross-modal generation으로 missing modality dynamics를 추론 (PDF p.9 §2.5).
  - chromatin accessibility regulation에 중요한 TF를 식별 (PDF p.6 §2.4, 101,644 TF-peak pair).
- Key results:
  - **Neurod2 enhancer→promoter→spliced mRNA 순서** 정량적 재현 (PDF p.4 §2.2, Fig 2c-e). 이는 SHARE-seq paper (S. Ma 2020)의 *"regulatory regions accessible prior to gene expression"* 관찰의 정량 재현.
  - SHARE-seq hair shaft-cuticle/cortex lineage에서 spliced/unspliced/gene-aggregated/peak-level 네 가지 consistency score 모두 mmVelo > scVelo·MultiVelo (Fig S3j-m, PDF p.4 §2.3, p.26). **Peak-level (Fig S3m)은 mmVelo only** — scVelo/MultiVelo는 peak-level velocity 자체를 정의 못함.
  - 101,644 TF-peak pair (PDF p.6 §2.4, Fig 4c,d): TF-regulated peak의 genomic distance가 random pair보다 짧음 (Wilcoxon p<0.01), 100 kb 이내 농축 → *local regulation* 구조 반영.
- Limitations:
  - **Preprint** (peer review 전 결과). PDF 각 페이지 footer에 명시.
  - 해석: peak-level "velocity"가 *peak-specific ODE rate*가 아니라 *decoder branch-level resolution*이므로 *kinetic interpretation*은 신중해야 함 (core p.120).
  - 검토필요: $\rho = 0.01$, $\kappa = 1$ 같은 hyperparameter sensitivity 실험이 PDF에 없음 (core p.146).
  - 검토필요: Fig S3 box plot의 정확한 수치 (median, IQR, p-value)가 본문 textual report에 없음 (core p.176).
- Follow-up possibility:
  - mmVelo peak-level chromatin velocity와 MoFlow gene-level c-s lag를 같은 dataset (SHARE-seq, HSPC)에서 직접 비교.
  - peer-review 출간 모니터링.
- Evidence sources:
  - `analysis/epigenomic-lag/nomura-2024-mmvelo/nomura-2024-mmvelo_core.md` Executive Summary/§Methods/§Results (PDF p.1–14, p.23, p.26 다수)
  - `analysis/epigenomic-lag/nomura-2024-mmvelo/nomura-2024-mmvelo_lens-academic.md`
- Status: `full-analysis` (preprint-tier)

### `cui-2024-deepvelo` — DeepVelo

- Identity: Cui, Maan, Vladoiu, Zhang, Taylor, Wang, 2024, *Genome Biology*, DOI `10.1186/s13059-023-03148-9`.
- Topic relevance: *cell-specific kinetics rationale*의 RNA-only predecessor. MultiVeloVAE / MoFlow가 cell-specific kinetics로 이동한 *직접 배경* reference. chromatin은 다루지 않음.
- Research question: complex multi-lineage scRNA-seq에서 *cell-agnostic kinetic rate* 가정을 완화해 velocity inference를 개선할 수 있는가?
- Method / assay / dataset:
  - Method: GCN encoder ($H^{(l+1)} = \sigma(\tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H^{(l)} W^{(l)})$, Eq. 3) + fully-connected decoder가 $(\alpha_{i,g}, \beta_{i,g}, \gamma_{i,g}) \in \mathbb{R}^{N \times D}$ 출력. Velocity $\tilde{v}_i = \beta_i u_i - \gamma_i s_i$ (Eq. 4). *Continuity loss* $L_c = L^{+} + L^{-} + L_{\text{Pearson}}$ (Eq. 14)로 self-supervised training (PDF p.3, core p.8).
  - Data: dentate gyrus, pancreatic endocrinogenesis, hindbrain development, organogenesis, mouse gastrulation, tumor heterogeneity 등 RNA-only multi-lineage datasets.
- Main claims:
  - *cell-specific kinetics*가 multi-lineage / time-dependent dynamics에서 기존 RNA velocity 대비 적합 (PDF §Background p2, core p.40).
  - GCN + continuity loss 조합이 (a) single cell noise smoothing과 (b) predefined cyclic pattern 회피를 동시에 달성 (PDF §"DeepVelo model" p3, core p.67).
  - scRNA-seq dataset의 *58% gene*이 multi-faceted kinetics를 보임 (Supp Fig. S3) — cell-agnostic 가정이 평균적으로도 부적합 (core p.65).
- Key results:
  - 여러 developmental/pathological datasets에서 더 consistent한 velocity와 driver gene signal (Springer page).
  - cellDancer 대비: cellDancer는 *cell-specific 시도했지만 direction 약하고 over-smoothed* (core p.66).
- Limitations:
  - chromatin modality 없음.
  - posterior uncertainty 없음 — *continuity score / correlation score*가 confidence proxy일 뿐 (core p.97).
  - 해석: kinetic rate biochemical validation은 별도 metabolic labeling이나 perturbation 필요.
- Follow-up possibility:
  - MoFlow/MultiVeloVAE의 cell-specific kinetics 필요성 background citation으로 사용.
- Evidence sources:
  - `analysis/epigenomic-lag/cui-2024-deepvelo/cui-2024-deepvelo_core.md` §Background/§Model/§Implementation
  - `analysis/epigenomic-lag/cui-2024-deepvelo/cui-2024-deepvelo_lens-academic.md`
- Status: `full-analysis`

### `mizukoshi-2024-deepkinet` — DeepKINET

- Identity: Mizukoshi, Kojima, Nomura, Hayashi, Abe, Shimamura, 2024, *Genome Biology*, DOI `10.1186/s13059-024-03367-8`.
- Topic relevance: chromatin은 직접 다루지 않지만 *2-stage VAE + cell-specific splicing/degradation rate decoders + metabolic labeling benchmark*라는 *evaluation framework*가 우리 epigenomic-lag validation design에 *framework 수준에서* 직접 참고 가능. C8 transferability map의 1차 source.
- Research question: scRNA-seq에서 *single-cell* splicing/degradation rates를 추정하고 metabolic labeling data로 kinetic-rate accuracy를 평가할 수 있는가?
- Method / assay / dataset:
  - Stage 1 (PDF p.13–14, core p.55): VAE로 latent cell state $z_n$과 small change $d_n$ 학습, gene-specific cell-uniform $\beta, \gamma$로 unspliced 재구성 (VICDYF 계승).
  - Stage 2 (PDF p.14, core p.111): Stage 1 encoder/decoder $\phi, \theta$를 **freeze**하고, $z_n \to (\beta_n, \gamma_n)$ neural network 두 개를 추가 학습. 같은 ELBO loss.
  - Data: simulated SERGIO (cluster별 rate inject), scEU-seq cell-cycle PULSE/CHASE (GSE128365), scNT-seq hematopoiesis, forebrain, breast cancer, SF3B1 mutation 7환자+2healthy.
- Main claims:
  - *the first instance in which such kinetic rates have been estimated and validated for accuracy at the single-cell level using both simulated and metabolic labeling data* (Discussion p.12, core p.41).
  - cellDancer/DeepVelo 대비 *kinetic-rate estimation* 우수, splicing은 comparable (core p.251-254).
- Key results:
  - Simulation (SERGIO 20×10 dropout + 13×10 cell-number): set-vs-estimated rate correlation이 cellDancer/DeepVelo보다 *항상* 높고 negative correlation 없음 (Fig. 2b–c, PDF p.4).
  - scEU-seq PULSE/CHASE 100회 반복 box plot: splicing comparable, **degradation에서 DeepKINET 단독 positive** — cellDancer는 *명백한 negative correlation* (Fig 3b, PDF p.6, core p.197).
  - scNT-seq hematopoiesis: 두 time batch 간 degradation rate ratio가 Dynamo와 상관, cellDancer/DeepVelo 능가 (Fig S3c).
  - 저자 *직접* MultiVelo [@li2023multivelo Ref. 46] 인용 (Discussion p.12, core p.165, lens-academic p.21): *"transcription rate determined based on chromatin accessibility ... is more realistic"* 인정 — DeepKINET 후속이 MultiVelo-style chromatin-aware extension이 될 수 있다고 *저자 본인이* 신호.
- Limitations:
  - chromatin modality 없음.
  - 저자 명시: ground truth는 *Dynamo-derived cluster-level rate* — Dynamo 자체도 model assumption 의존 (core p.299).
  - Splicing/degradation indeterminacy를 *해결*하지 못함 — 2-stage decoupling으로 *완화*만 (lens-academic p.18).
  - 검토필요: SERGIO source code를 *저자가 수정*해 cluster별 rate inject → self-favorable risk 가능 (lens-academic p.30).
- Follow-up possibility:
  - **chromatin-aware DeepKINET** ("DeepKINET-Multiome") — 저자 본인이 Discussion p.12에서 신호한 방향 (lens-academic §2.1).
  - 우리 epigenomic-lag method validation에 *2-stage decoupling + 100-repeat box-plot + negative correlation fail rule + cluster-level simulation benchmark* 차용.
- Evidence sources:
  - `analysis/epigenomic-lag/mizukoshi-2024-deepkinet/mizukoshi-2024-deepkinet_core.md` §Methods/§Results/§Discussion
  - `analysis/epigenomic-lag/mizukoshi-2024-deepkinet/mizukoshi-2024-deepkinet_lens-academic.md` §3 Validation design transferability (직접 transferability map 정의)
- Status: `full-analysis`

### `el-kazwini-2026-crakvelo` — CRAK-Velo (full-analysis)

- Identity: El Kazwini, Gao, Kouadri Boudjelthia, Cai, Huang, Sanguinetti, 2026, *Genome Biology* (Article in Press, unedited manuscript), DOI `10.1186/s13059-026-04086-y` (online 2026-05-05). bioRxiv preprint `10.1101/2024.09.12.612736`. PDF + Additional file 1/2 확보.
- Topic relevance: UniTVelo를 chromatin-aware로 확장한 semi-mechanistic velocity. MultiVelo보다 단순·빠른 대안. **우리 HSPC(GSE209878)에서 MultiVelo와 동일 데이터·동일 annotation으로 직접 head-to-head가 가능한 1순위 비교 baseline.**
- Research question: RNA velocity 결과를 chromatin region–gene interaction과 연결하면서, transcription rate를 chromatin accessibility로 직접 구성해 더 단순·빠르게 추정할 수 있는가?
- Method / assay / dataset:
  - Method: UniTVelo RBF spliced model(Eq.4–7) 계승 + scATAC 유래 transcription rate $c^g = \eta_g \sum_r^{R_g} w_r^g f(\phi_r^n)$ (Eq.8–10, cisTopic으로 $\phi_r$ smoothing). unspliced 미분을 RNA-only 형태(Eq.6)와 ATAC-derived 형태 $u'^{ATAC}_g = c^g - \beta_g \hat{u}_g$ (Eq.11)로 정의해 가중 NLL $l(\theta_g) = \pi b_g^2(\sum |x-\hat{x}|^2 + k|\hat{u}' - u'^{ATAC}|^2) - \log b_g$ (Eq.13)로 reconcile. gene별 region weight $w_r^g$ 추정. gradient descent, dataset당 10,000 epochs.
  - Data: 세 dataset 모두 paired 10x Multiome — HSPC(GSE209878, 11,605/2,000/3,939), E18 mouse brain(3,365/2,000/4,002), human cerebral cortex(GSE162170, 4,693/954/844).
- Main claims:
  - chromatin을 transcription rate production term으로 직접 구성해 RNA-only(UniTVelo)보다 biologically consistent한 flow·terminal state를 얻는다.
  - MultiVelo 대비 simpler and faster이면서 동일 HSPC에서 더 정확하다.
  - region weight $w_r^g$로 cis-regulatory region–gene interaction을 정량해 해석 layer를 제공한다.
- Key results:
  - HSPC(GSE209878): CBDir 세 method 중 최고, platelet terminal state 정확 식별(UniTVelo 실패, MultiVelo는 erythrocyte→granulocyte spurious flow). KNN cell-type accuracy 다수 gene 우위(HDC 0.259 vs MultiVelo 0.183) (Fig 1).
  - E18 mouse brain: Upper/Deeper Layer 독립 terminal 정확 식별(MultiVelo·UniTVelo는 spurious Upper→Deeper flow) (Fig 2).
  - Run-time(Table S1): HSPC 15h vs MultiVelo >24h, HCC 6h vs 24h — 세 dataset 모두 MultiVelo보다 빠름.
  - HCC($G>R$): flow는 일관하나 region-level inference가 low coverage(window 내 region 보유 gene ~50%)로 hyperparameter에 민감.
- Limitations:
  - 저자 명시: HCC region-level inference 불안정; mouse brain ependymal cell terminal 식별 세 method 공통 실패.
  - 해석: 공식 ablation(chromatin term on/off, $k=0$, weight permutation) 부재 — UniTVelo 비교는 ablation을 부분 대신할 뿐 순수 chromatin 효과와 구현 차이가 분리 안 됨.
  - 해석: CBDir·KNN에 통계 검정·CI·시드 분산 없음; 예시 gene cherry-picking 여지(FOXP2는 MultiVelo 약간 우위).
  - `검토필요:` **chromatin–transcription lag를 명시 parameter로 출력하지 않음** — KLF1/Jag2 region kinetic plot의 지연은 pseudotime 축 시각화이므로 gene별 lag 수치는 후처리 필요.
  - `검토필요:` $k$($k=0.5$ vs Eq.15/16), topic 수($T=20/30/50$), supplementary Table 번호(S1/S2) 본문·캡션 불일치 — Article in Press 교정 대상.
- Follow-up possibility:
  - 우리 GSE209878 HSPC에서 CRAK-Velo vs MultiVelo head-to-head(본 논문이 이미 그 셋업).
  - region kinetic plot의 accessibility-peak와 unspliced-peak pseudotime 차이를 gene별 lag 수치로 후처리하는 파이프라인 구축(우리 핵심 deliverable 직결).
- Evidence sources:
  - `analysis/epigenomic-lag/el-kazwini-2026-crakvelo/el-kazwini-2026-crakvelo_core.md` Executive Summary/Methods/Results/Figures
  - `analysis/epigenomic-lag/el-kazwini-2026-crakvelo/el-kazwini-2026-crakvelo_lens-academic.md` Limitations/Citation/Final Takeaways
- Status: `full-analysis`

### `luo-2026-velocity-benchmark` — RNA velocity benchmark (full-analysis)

- Identity: Luo, Ren, Yang, You, Zhou, Qin, Li, 2026, *Cell Reports Methods* 6(4):101367 (PMC13106975). bioRxiv preprint `10.1101/2025.08.02.668272`. PDF + STAR Methods + mmc1/mmc2 확보. 저자 소속: Department of Hematology, Xiamen University.
- Topic relevance: 15개 RNA velocity method를 17 real + 3 simulation dataset에서 벤치마크. **우리 HSPC(GSE209878)가 Dataset12로 직접 사용됨 — 단 MultiVelo는 `rna_only=True`(ATAC 비활성)로만 평가되어 multi-omic 강점은 미측정.**
- Research question: RNA velocity inference에서 어떤 method를 언제 써야 하는지에 대한 evidence-based scenario별 best-practice를 수립할 수 있는가?
- Method / assay / dataset:
  - Method: 15 method(ODE 5: velocyto·scVelo-sto·scVelo-dyn·**MultiVelo(`rna_only=True`)**·CellRank / ML 4: UniTVelo·Dynamo-sto·Pyro-Velocity·cell2fate / DL 6: veloAE·veloVI·veloVAE·LatentVelo·cellDancer·DeepVelo)를 4 metric으로 평가 — accuracy CBDir(ground-truth $A\to B$ 방향 cosine), ICCoh·Vcs(내부 일관성/smoothness), A1/A2(method agreement). downsampling(0.4–0.8 ×5)·HVG·dyngen simulation로 stability, time·memory로 usability.
  - Data: 17 real dataset — Dataset1 pancreas(GSE132188) … **Dataset12 human HSPC(GSE209878, transition HSC→MPP/MPP→LMPP/MEP→Erythrocyte/GMP→Granulocyte)** … Dataset16 embryonic mouse brain 10x multiome, Dataset17 mouse hematopoiesis(GSE81682). + 3 dyngen simulation.
- Main claims:
  - 모든 평가를 압도하는 단일 method 없음("no single method exhibited superior performance in all the assessments").
  - 단일 method 의존 대신 multiple method 결과의 cross-method consistency(특히 downstream biological interpretation)를 비교하라.
  - scenario별 권고: large atlas→veloVI/DeepVelo/Dynamo-sto/scVelo-sto, low-quality→UniTVelo/LatentVelo/veloVI/Pyro-Velocity, complex topology→DeepVelo/veloVI/LatentVelo.
- Key results:
  - Accuracy 전반 낮음(17 real 평균 CBDir ≈0.1): 최고 veloVI 0.23, 다음 Pyro-Velocity 0.17; veloVAE 다수 dataset에서 방향 역전(Fig 2A).
  - complexity↑→accuracy↓: human bone marrow(Dataset4) 평균 CBDir −0.193, mature PBMC(Dataset11) 대부분 method가 biology와 반대 방향.
  - ICCoh 대부분 ≥0.7(LatentVelo 0.99, UniTVelo·MultiVelo 0.96)이나 저자는 over-smoothing 신호일 수 있다고 경고; A1 대부분 <0.4(method 간 큰 불일치).
  - Usability: DeepVelo·veloVI가 time·memory 우수, cellDancer·MultiVelo는 실행시간 長(Fig 6C).
- Limitations:
  - 저자 명시: CBDir이 pre-defined ground-truth(annotation bias)에 의존; high ICCoh가 over-smoothing일 수 있음; method 불일치는 inference error가 아니라 model architecture 차이일 수 있음.
  - `해석:` **MultiVelo·Chromatin Velocity 등 epigenome-integrating method를 `rna_only=True`로만 평가** — 우리 epigenomic-lag에 정작 필요한 multi-omic(ATAC 켠) 모드 성능이 측정되지 않음. Dataset16이 multiome인데도 ATAC 활용 평가는 없음.
  - `미제공:` Dataset12(HSPC) 단독 method 순위의 수치 표가 본문에 없음(합산 분포 위주) — hematopoietic branching 순위는 mmc1/mmc2/원자료 별도 추출 필요.
  - `해석:` 최고 CBDir 0.23·전체 평균 ≈0.1로 절대 정확도 낮음 — 권고는 상대 순위일 뿐 절대 신뢰도를 보장하지 않음.
- Follow-up possibility:
  - multi-omic 모드를 켠 velocity benchmark — HSPC(Dataset12)·embryonic brain(Dataset16)에서 ATAC 켠 MultiVelo CBDir 재측정(우리 목표 직결 빈칸).
  - Dataset12(GSE209878)+Dataset17(GSE81682)만으로 hematopoietic branching 특화 mini-benchmark.
- Evidence sources:
  - `analysis/epigenomic-lag/luo-2026-velocity-benchmark/luo-2026-velocity-benchmark_core.md` Executive Summary/Methods/Results/Tables
  - `analysis/epigenomic-lag/luo-2026-velocity-benchmark/luo-2026-velocity-benchmark_lens-academic.md` Limitations/Citation/Final Takeaways
- Status: `full-analysis`

### `safi-2022-chromatin-priming` — concurrent stem/lineage chromatin priming (full-analysis)

- Identity: Safi, Dhapola, Warsi, Sommarin, …, Karlsson, 2022, *Cell Reports* 39(6):110798, DOI `10.1016/j.celrep.2022.110798`, PMID 35545037. 2023 erratum(Cell Rep 42(10):113357) 존재(본 PDF에 미반영). PDF + mmc1–7 확보.
- Topic relevance: mouse LSK HSPC scATAC-seq로 commitment에 선행하는 concurrent stem/lineage chromatin priming을 chromatin-side로 입증 — activation lag 가설의 정성적 선행성을 같은 HSPC 축에서 뒷받침. **단 paired multiome이 아니고 transition 축이 pseudotime이라 gene별 lag 정량의 직접 근거는 아님.**
- Research question: HSPC에서 cellular-fate option이 어느 stem-like 단계에서 lineage priming으로 처음 시작되는가를 chromatin accessibility 수준에서 규명.
- Method / assay / dataset:
  - Method: scATAC-seq(8 sorted populations) → 571 JASPAR TFBS motif accessibility 정량(distal/proximal 분리) → Slingshot pseudotime 정렬 → Python `ruptures` change-point detection으로 motif accessibility 급변 transition point 검출(motif당 1개). change-point density로 transition zone 위치. scRNA-seq·sc-qPCR·transplant·in vitro clonogenic assay로 직교 검증.
  - Data: mouse LSK HSPC scATAC 2,680 cells(~283,358 peaks = 107,011 distal + 37,945 promoter-proximal); scRNA-seq는 **다른 cell batch**(2,462 cells), computational projection으로 연결. paired multiome 아님.
- Main claims:
  - lineage commitment에 앞서 stem-like + lineage-affiliated(lympho-myeloid + MegE) chromatin program을 *동시* 보유하는 prospectively isolable한 `LSKFlt3int CD9high` 중간 집단이 존재한다.
  - chromatin program(특히 distal enhancer/TF motif)이 lineage commitment와 frank gene expression에 *선행*한다.
  - 이 집단은 multi-lineage capacity는 있으나 long-term self-renewal은 없는 transition state다.
- Key results:
  - distal homogeneity score 0.434 vs proximal 0.246 — distal regulatory region이 cell type 분리력 우위(Fig 2E/2F).
  - lympho-myeloid trajectory의 *가장 이른* transition point가 CD9high-dominated cluster 3에 mapping; cluster 3가 stem-like(FoxO/Hox/Spi1) + lineage-specific motif 동시 보유(Fig 3).
  - scRNA-seq cluster 3에 CD9high 30% enrich(Poisson p<10⁻⁵), HSC-like signature; SPI1↑(lympho-myeloid) vs GATA1↑(MegE) 개별 cell anti-correlation crossover(Fig 4, 3O).
  - 기능 검증: CD9high single clone의 30%가 multi-lineage progeny(CD9low 5.7%); transplant에서 short-term myeloid + long-term lymphoid이나 long-term self-renewal 없음(Fig 6,7).
- Limitations:
  - `해석:` **paired multiome이 아님** — scATAC↔scRNA를 computational projection으로 연결하므로 같은 cell의 opening→transcription lag를 직접 계산 못함.
  - `검토필요:` transition point 축이 Slingshot **pseudotime**(differentiation ordering)이고 wall-clock time이 아님 — "precede"는 ordering상 선행성.
  - `해석:` change-point가 motif 단위·trajectory별 single point만 검출; "concurrent"가 single-cell co-accessibility인지 집단 평균인지 구분 부족.
  - `해석:` mouse LSK이므로 human HSPC cross-species 일반화는 선결 과제(우리 GSE209878은 human).
  - `검토필요:` 본문 Data availability(GSE173075/173076) vs STAR Methods(GSE148746) accession 불일치; 2023 erratum 미반영.
- Follow-up possibility:
  - 우리 GSE209878 human HSPC paired multiome에서 같은 cell의 promoter ATAC change point와 transcription onset change point의 pseudotime 차이를 lag proxy로 정의(Safi change-point density 절차 차용).
  - Safi의 lineage-primed enhancer cluster 15·16 좌표가 우리 HSPC ATAC peak과 겹치는지 비교.
- Evidence sources:
  - `analysis/chromatin-rna-coupling/safi-2022-chromatin-priming/safi-2022-chromatin-priming_core.md` Executive Summary/Methods/Results/Figures
  - `analysis/chromatin-rna-coupling/safi-2022-chromatin-priming/safi-2022-chromatin-priming_lens-academic.md` Limitations/Citation/Final Takeaways
- Status: `full-analysis`

### `martin-2023-hspc-chromatin` — HSPC chromatin accessibility dynamics (full-analysis)

- Identity: Martin, Rodriguez y Baena, Reggiardo, Worthington, …, Forsberg, 2023, *Stem Cells* 41(5):520-539, DOI `10.1093/stmcls/sxad022`, PMID 36945732, PMC10183972. PDF + supplementary 확보. **자료 유형 정정: review → primary research article**(PDF header "Original Research", Results·실험 Figure·CRISPRi 직접 수행).
- Topic relevance: mouse hematopoiesis 13 cell type의 ATAC-seq + CRISPRi primary article. chromatin priming이 transcription/commitment에 선행한다는 방향성을 같은 hematopoietic 축에서 직접 보이고 **CRISPRi로 accessibility→expression 인과까지 연결** — activation lag 가설의 생물학적 방향성 배경.
- Research question: 분화 과정에서 epigenetic identity가 lineage potential에 어떻게 기여하고, lineage-primed CRE가 분화 trajectory를 따라 어떻게 유지/소실되는가?
- Method / assay / dataset:
  - Method: bulk ATAC-seq(13 FACS-purified cell type, replicate n=2) → IDR peak → master peak-list 92,842 peaks → chromVAR 정규화 + PCA/UMAP/hierarchical clustering → HOMER motif·GREAT GO → HSC와 unipotent cell 배타 공유 'primed peak' 추적 → dCas9-KRAB **CRISPRi**로 후보 CRE silencing 후 cell-surface protein flow cytometry 정량.
  - Data: mouse BM ATAC-seq 13 cell type(GSE184851 + 선행 GSE162949); CRISPRi mouse(CD81/CD115/CD11b). expression reference는 외부 GEXC database — **paired RNA/multiome 아님**.
- Main claims:
  - selective HSC-primed lineage-specific CRE 중 소수만(lineage별 25% 미만) 분화 전 과정 accessible 유지되고 대부분 닫힌다.
  - 13 cell type이 erythromyeloid vs lymphoid 두 cluster로 분리되고 HSC/MPP는 erythromyeloid에 편향.
  - HSC가 가장 높은 global accessibility를 보이며 HSC-unique CRE는 erythroid fate priming에 치우침; CRISPRi로 accessibility→expression 인과 확립.
- Key results:
  - HSC IDR peak 70,731(master 92,842)로 progenitor 중 최다, cumulative signal도 최고(Table 1, Fig 1B/1C).
  - HSC-primed peak의 25% 미만만 분화 끝까지 유지(17% MkP/11% EP/13% GM/12% B/26% T)(Fig 6C).
  - HSC-unique peak 3,026개, 92.7% non-promoter, ELF3/CTCFL/NF-E2/RUNX motif + "definitive erythrocyte differentiation" GO enrich(Fig 7A-D).
  - CRISPRi: CD81 promoter proof-of-concept(p<.01); CD115 promoter·enhancer 둘 다 silencing 시 CD115+ 유의 감소(p<.0001); **CD11b enhancer는 ns** — 모든 putative CRE가 기능적이지 않음(Fig 7I-L).
- Limitations:
  - `해석:` **paired RNA/multiome 직접 측정 없음**(expression은 외부 GEXC) — accessibility-expression이 같은 cell 동시 측정이 아니므로 시간 단위 lag 정량 불가, priming 방향성 근거로만 사용.
  - `해석:` bulk ATAC-seq(single-cell 아님)라 population 내 heterogeneity·intermediate state 평균화.
  - `검토필요:` peak count·cumulative signal이 cell 수·library depth에 민감한데 정규화 절차 본문 수치 약함 — "HSC가 가장 열림" 인용 시 caveat 동반.
  - `해석:` replicate n=2(HSC 2 sample은 clustering에서 유일 비인접); genome-wide priming 주장의 인과 검증은 CRISPRi 3 locus에 한정.
- Follow-up possibility:
  - Martin의 mouse HSC-unique/lineage-primed CRE 좌표를 우리 Human HSPC GSE209878 ATAC peak에 mm10→hg38 liftover로 mapping해 baseline primed-CRE feature 정의.
  - 우리 multiome에서 "열렸으나 미발현" CRE 비율을 lineage별로 추정해 본 논문의 <25% 유지 통계와 비교.
- Evidence sources:
  - `analysis/chromatin-rna-coupling/martin-2023-hspc-chromatin/martin-2023-hspc-chromatin_core.md` Executive Summary/Methods/Results/Tables
  - `analysis/chromatin-rna-coupling/martin-2023-hspc-chromatin/martin-2023-hspc-chromatin_lens-academic.md` activation lag 배경/Limitations/Citation
- Status: `full-analysis`

## Cross-Paper Signals

- 반복되는 문제:
  - 모든 method가 gene-level chromatin aggregation을 기본으로 사용해 enhancer/promoter별 distinct kinetics를 직접 모델링하지 못한다.
  - causal validation은 공통적으로 부족하다. TF/motif lag, $\delta/\kappa$, MoFlow lag cluster 모두 association 또는 model-derived inference 중심이다.
  - cell cycle 또는 mature/quiescent cell context에서 velocity inference 신뢰도 문제가 반복된다.
- 방법론 차이:
  - MultiVelo: interpretable ODE + discrete state + EM latent time.
  - MultiVeloVAE: probabilistic generative framework + continuous factors + multi-sample/differential test.
  - MoFlow: deterministic local relay velocity + no latent time + cell-specific kinetics.
- dataset / assay 차이:
  - MultiVelo와 MoFlow는 기존 benchmark/reused multiome dataset 중심.
  - MultiVeloVAE는 신규 EB/HSPC/macrophage dataset과 mixed RNA-only/multiome setting을 포함.
- 공통 한계:
  - perturbation 또는 true time-labeled multiome ground truth 부족.
  - head-to-head 비교 metric이 통일되어 있지 않다. MoFlow는 CBDir, MultiVeloVAE는 GCBDir/다축 metric 중심.
- 후속 연구 후보:
  - 같은 HSPC input에서 MultiVelo, MultiVeloVAE, MoFlow를 통일 metric으로 직접 비교.
  - agreement/disagreement gene set을 high-confidence vs review-needed lag candidate로 분류.
  - enhancer-resolved 또는 peak-level lag modeling으로 gene-level c aggregation 한계 보완.
  - metabolic labeling 또는 time-stamped benchmark를 epigenomic-lag validation design에 차용.
  - `해석:` chromatin-aware velocity 후보가 늘어남(CRAK-Velo full-analysis 승격) → head-to-head benchmark 비교 대상은 MultiVelo·MultiVeloVAE·MoFlow + CRAK-Velo. CRAK-Velo는 **동일 GSE209878 HSPC에서 MultiVelo와 직접 비교**(동일 데이터·annotation)했고 MultiVelo 대비 단순·빠르며(run-time 15h vs >24h) terminal state·deconvolution 우위 — 우리 head-to-head의 가장 직접적인 진입점. 단 CRAK-Velo도 chromatin–transcription lag를 명시 parameter로 출력하지 않아 region kinetic의 peak-pseudotime 차이를 lag로 후처리해야 함.
  - `해석:` Luo benchmark는 "전 항목 우월 method 없음"을 17 real + 3 simulation으로 정량 입증 → 단일 default가 아니라 *우리 HSPC data에 대한 자체 검증*으로 정해야 한다. **우리 HSPC(GSE209878)는 Dataset12로 직접 포함됐으나 MultiVelo는 `rna_only=True`(ATAC 비활성)로만 평가** — 우리 epigenomic-lag에 정작 필요한 multi-omic 모드 성능은 이 benchmark가 측정하지 않았다. 따라서 RNA-only 순위만 차용하고 multi-omic 검증은 자체 수행 필요.
  - `해석:` biology-side(Safi 2022, Martin 2023)는 같은 HSPC 축에서 "chromatin priming이 commitment/transcription에 선행"한다는 *정성적 선행성*을 PDF 근거로 뒷받침 → activation lag 가설의 생물학적 plausibility 배경. Martin은 CRISPRi로 accessibility→expression 인과까지 보이나(단 CD11b enhancer는 ns), 둘 다 **paired RNA/시간 단위 lag를 정량하지 않으므로**(Safi: 다른 batch projection·pseudotime 축; Martin: 외부 GEXC·bulk) lag 정량의 직접 근거는 아니다. 둘 다 mouse라 human HSPC cross-species 일반화는 선결 과제.

## Missing Evidence

- PDF 확보·분석 완료: **11편 모두 full-analysis** (직전 abstract-only 4편 2026-06-12 승격). 직전 단계의 PDF 미확보 gap은 해소됨. 4편 PDF 확인으로 확정된 핵심 사실:
  - `el-kazwini-2026-crakvelo`: UniTVelo 확장 semi-mechanistic, MultiVelo 직접 경쟁. **동일 GSE209878 HSPC에서 MultiVelo 대비 우위 + run-time 15h vs >24h**. 단 lag를 명시 parameter로 출력 안 함. Article in Press(unedited)라 $k$/$T$/Table 번호 본문 불일치 — 최종본 교정 모니터링 필요.
  - `luo-2026-velocity-benchmark`: 15 method(MultiVelo 포함), 17 real + 3 simulation. **우리 HSPC = Dataset12(GSE209878). MultiVelo는 `rna_only=True`로만 평가** — multi-omic 성능 미측정. Dataset12 단독 method 순위 수치는 본문에 없어 mmc1/mmc2/원자료 추출 필요.
  - `safi-2022-chromatin-priming`: scATAC-seq 단독(paired multiome 아님) + pseudotime 축 → 정성적 priming 선행 지지, lag 정량 직접 근거 아님. **GSE accession 불일치(GSE173075/76 vs GSE148746) + 2023 erratum 미반영** — 재현·인용 전 확인.
  - `martin-2023-hspc-chromatin`: **review→primary research article 정정**(ATAC-seq + CRISPRi). paired RNA 없음(외부 GEXC), bulk. priming 방향성 + CRISPRi 인과 배경.
- 확인할 metadata:
  - MoFlow GitHub license.
  - MultiVeloVAE benchmark exact numeric matrix는 source data xlsx에서 추가 추출 가능.
  - MoFlow 129 reversal genes list와 cluster 10 gene set은 supplementary/source data에서 추가 추출 필요.
  - mmVelo: github.com/nomuhyooon/mmVelo의 explicit license 확인 (PDF footer는 CC-BY 4.0, code repo는 별도 확인 필요). `검토필요: peer-review 출간 모니터링`.
  - mmVelo Fig S3 box plot 정확 수치 (median, IQR, p-value)는 본문 textual report에 없음 — source data 또는 후속 출간본에서 확인 필요.
- 신규 확인 필요 (DeepKINET 도입 결과):
  - *chromatin-aware simulator* 후보 (BEELINE, MultiVelo authors의 simulation script 등)가 *cluster별 lag* (time 단위)를 inject할 수 있는지 검토 — DeepKINET SERGIO 변형이 rate (1/time)을 inject하는 것과 단위/메커니즘이 다름.
  - *DeepKINET-Multiome* 형태의 chromatin-aware extension 후속 publication 모니터링 (Welch lab 또는 Shimamura lab).
