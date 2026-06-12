# Evidence Bundle

## Scope Summary

- Topic: `epigenomic-lag`
- Research question: gene별 chromatin-transcription lag structure를 정량화하고 epigenetic drug response timing 예측으로 연결할 수 있는 method와 evidence를 비교한다.
- Inclusion: paired chromatin accessibility + RNA 또는 multiome data를 활용하고, chromatin state와 transcription/RNA dynamics의 시간적 관계를 다루는 method paper.
- Current evidence set: `@li2023multivelo`, `@li2025multivelovae`, `@hong2026moflow`, `@li2023celldancer`, `@nomura2024mmvelo`, `@cui2024deepvelo`, `@mizukoshi2024deepkinet`.

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

## Missing Evidence

- PDF 필요: 7개 paper 모두 source와 full analysis 있음 (cellDancer/DeepVelo/DeepKINET/mmVelo는 light → full 승급 완료).
- full analysis 필요: 없음.
- 확인할 metadata:
  - MoFlow GitHub license.
  - MultiVeloVAE benchmark exact numeric matrix는 source data xlsx에서 추가 추출 가능.
  - MoFlow 129 reversal genes list와 cluster 10 gene set은 supplementary/source data에서 추가 추출 필요.
  - mmVelo: github.com/nomuhyooon/mmVelo의 explicit license 확인 (PDF footer는 CC-BY 4.0, code repo는 별도 확인 필요). `검토필요: peer-review 출간 모니터링`.
  - mmVelo Fig S3 box plot 정확 수치 (median, IQR, p-value)는 본문 textual report에 없음 — source data 또는 후속 출간본에서 확인 필요.
- 신규 확인 필요 (DeepKINET 도입 결과):
  - *chromatin-aware simulator* 후보 (BEELINE, MultiVelo authors의 simulation script 등)가 *cluster별 lag* (time 단위)를 inject할 수 있는지 검토 — DeepKINET SERGIO 변형이 rate (1/time)을 inject하는 것과 단위/메커니즘이 다름.
  - *DeepKINET-Multiome* 형태의 chromatin-aware extension 후속 publication 모니터링 (Welch lab 또는 Shimamura lab).
