# Ma 2020 — SHARE-seq / Chromatin Potential — Academic Lens

근거: `ma-2020-shareseq_core.md`, `sources/abstract.txt`, `paper-info.yaml`. 원문 PDF·supplementary는 sources에 없으므로 core.md(이미 source-grounded)와 abstract를 1차 근거로 삼는다. 본문 사실이 아닌 분석자 판단은 `해석:` / `추정:` / `질문:` / `검토필요:` / `미제공:`으로 분리했다.

## Limitations

### 저자가 명시한 한계

- chromatin potential은 lineage tracing이 아니라 paired snapshot의 nearest-neighbor inference다. 저자 본인이 Discussion에서 primed chromatin state는 lineage *choice*가 아니라 lineage *bias*일 수 있다고 구분한다 (core.md Results §Dataset 5).
- chromatin potential arrow의 일부 long arrows는 assay noise, low-dimensional embedding error, technical bias에서 올 수 있다고 명시한다. 따라서 arrow를 fate commitment로 직접 읽지 말라고 저자가 선을 긋는다 (core.md Figure 5 해석 시 주의점).
- computational pairing 정확도가 tissue·depth에 민감하다는 점을 저자가 직접 보였다. 같은 cluster assignment 기준 skin 74.9%, brain 36.7%, low depth/low cell number에서 error 증가 (core.md Background, Dataset 3). 이는 "paired measurement가 왜 필요한가"를 정당화하는 근거인 동시에, separate-modality integration의 신뢰 범위를 저자 스스로 좁혀둔 한계 진술이다.

### 분석자가 판단한 한계

- 부족한 점: chromatin potential의 핵심 가정인 "현재 dataset 안에 future RNA state에 해당하는 cell이 관측되어 있어야 한다"가 검증되지 않은 채로 method가 작동한다 (core.md Methods §Chromatin potential, hidden assumption). 즉 trajectory가 충분히 sampled되었다는 전제가 만족되는지에 대한 정량 진단(예: missing intermediate state 비율, neighbor 거리 분포)이 제시되지 않는다.
  - 왜 중요한가: hair follicle은 비교적 연속적이고 잘 sampled된 lineage라 이 가정이 우연히 충족되었을 수 있다. sparse하거나 discrete한 transition을 갖는 system(예: HSPC의 commitment branch)에서는 같은 kNN matching이 가까운 가짜 future를 가리킬 수 있다.
  - 어떤 증거가 부족한가: trajectory completeness에 대한 sensitivity analysis. cell을 의도적으로 down-sample해 intermediate state를 제거했을 때 chromatin potential arrow가 얼마나 망가지는지 보여주는 실험이 빠져 있다.

- 부족한 점: "DORC accessibility가 RNA expression보다 먼저 변한다"는 중심 claim이 pseudotime ordering과 residual에 의존한다. residual이 positive인 lineage가 92%라는 수치(core.md Dataset 5)는 강한 신호지만, 이 ordering은 wall-clock time이 아니라 inferred pseudotime 위의 순서다.
  - 왜 중요한가: 본 프로젝트의 목표인 gene별 chromatin-transcription lag 정량화로 넘어가는 순간, "먼저"의 단위가 곧장 문제가 된다. SHARE-seq snapshot에서 얻은 lag는 pseudotime 단위이고, epigenetic drug response timing 예측에 쓰려면 wall-clock으로의 환산이 별도로 입증되어야 한다 (CLAUDE.md 방법론 주의 1).
  - 어떤 증거가 부족한가: pseudotime↔실제 시간 anchoring. 저자는 Anagen III/VI 같은 biological stage로 inferred root/branch를 맞추긴 했지만(core.md Figure 5 j-k), 이는 stage 일치이지 시간 calibration이 아니다.

- 부족한 점: residual을 "chromatin이 RNA보다 먼저 활성화되는 구간"으로 정량화하지만(core.md Background §residual), residual이 burst kinetics나 measurement asymmetry의 artifact가 아닌지에 대한 통제가 보이지 않는다.
  - 왜 중요한가: ATAC와 RNA는 detection sensitivity와 dynamic range가 다르다. accessibility는 binary-ish하게 빨리 saturate되고 RNA induction은 burst로 천천히 쌓이는 경향이 있어, "chromatin이 먼저"라는 신호의 일부가 두 modality의 측정 특성 차이에서 올 수 있다. 본 프로젝트에서 mean expression·variance scaling을 covariate로 통제하지 않으면 lag estimate가 artifact가 될 수 있다는 주의(CLAUDE.md 방법론 주의 2)와 직접 맞닿는다.
  - 어떤 증거가 부족한가: matched null. 시간 순서가 없는 gene(housekeeping 또는 simultaneous regulation으로 알려진 gene)에서 residual이 0 근처에 분포하는지 보여주는 negative control. 92%라는 수치도 적절한 baseline 분포 없이는 해석이 어렵다.

- 부족한 점: cell cycle이 confound로 남아 있다. proliferating basal cells는 RNA에서 cell cycle gene으로 coherent cluster를 만들지만 chromatin에서는 4가지 dimensionality reduction 중 어느 것에서도 coherent cluster로 나오지 않는다(core.md Dataset 3 예외). 저자는 이를 modality mismatch의 흥미로운 사례로 제시하지만, chromatin potential·DORC residual 계산에서 cell cycle phase를 covariate로 통제했는지는 core.md 근거 범위에서 확인되지 않는다.
  - 왜 중요한가: cell cycle은 accessibility와 expression을 동시에 흔드는 대표적 confound다. 통제하지 않으면 differentiation lineage 신호에 cell cycle 신호가 섞여 들어간다.
  - 미제공: cell cycle phase별 chromatin potential / lag estimate는 core.md·abstract 근거 범위에 없다.

- 부족한 점: peak-gene association이 correlation 기반이라는 점은 저자도 인정하지만(core.md Methods §cis), DORC를 super-enhancer·lineage-determining gene과 연결하는 해석은 association을 regulatory function으로 한 단계 끌어올린다. causal evidence(TF/enhancer perturbation, lineage tracing)는 없다.
  - 왜 중요한가: "chromatin이 RNA를 prime한다"는 인과적 어휘가 paper 전체에 깔려 있는데, 제시된 것은 temporal association이다. 후속 모델이 이 association을 causal prior로 그대로 쓰면 오류가 전파된다.
  - 어떤 증거가 부족한가: DORC 또는 그 안의 TF motif를 perturb했을 때 target gene induction이 실제로 지연·소실되는지 보이는 실험. core.md Figure 4의 Lef1/Hoxc13 motif가 Wnt3 DORC activation에 선행한다는 모델은 motif enrichment + timing이지 perturbation이 아니다.

### 설명이 매끄럽지 않은 지점

- 연결이 약한 주장: chromatin potential이 RNA velocity보다 "early lineage bias를 더 잘 잡는다"는 비교.
  - 현재 논문에서 제시한 근거: early stage에서 chromatin potential의 prediction reach가 더 길고 late pseudotime에서는 RNA velocity가 더 길다, KS test p < 2.2 × 10^{-16} (core.md Dataset 5, Figure 5 l).
  - 더 필요해 보이는 근거: 두 method는 측정 대상과 timescale이 다르다(velocity는 spliced/unspliced 비, potential은 DORC↔future RNA matching). "reach가 길다"가 더 이른 신호인지, 아니면 단지 embedding 위 거리 척도가 달라서인지 분리되지 않는다. 해석: ground-truth lineage label(예: hair follicle lineage tracing reporter)에 대한 두 method의 prediction accuracy를 같은 척도로 비교해야 "어느 쪽이 더 이른 fate를 맞히는가"가 깔끔해진다. 현재는 두 화살표의 길이 분포 차이에 가깝다.

- 연결이 약한 주장: DORC와 super-enhancer overlap이 chromatin priming의 mechanistic support라는 서술.
  - 현재 논문에서 제시한 근거: DORC-regulated gene이 known super-enhancer와 overlap하고 lineage gene에 enriched (core.md Dataset 4).
  - 더 필요해 보이는 근거: overlap의 exact p-value/effect size가 core.md가 확인한 crawl text에 없다(core.md Dataset 4 통계/재현성). 검토필요: supplementary를 확보해 overlap이 genome-wide expectation 대비 유의한지, 단순히 super-enhancer가 본래 peak이 많은 영역이라 DORC cutoff(peak ≥10)에 자동으로 걸리는 건 아닌지 확인이 필요하다.

- 연결이 약한 주장: 비용 우위($433 / 100,000 cells vs sci-CAR $30,000 초과)가 assay의 장점으로 반복 제시된다(core.md Methods, Dataset 2).
  - 현재 논문에서 제시한 근거: 저자 hands-on condition 기준 library prep cost.
  - 더 필요해 보이는 근거: 이는 academic lens의 핵심은 아니지만, reagent price·sequencing cost·labor·failure rate가 빠진 library prep만의 숫자다(core.md Dataset 2 주의점). 인용 시 "library prep cost"로 한정해야 한다. (상용화·BD 관점은 lens-industry 담당.)

### 정리되지 않은 질문

- 질문: chromatin potential의 kNN($k=10$)에서 k 선택이 arrow 방향에 얼마나 민감한가? k에 대한 robustness가 core.md 근거 범위에 없다. 본 프로젝트에서 lag structure를 뽑을 때 같은 민감도가 재현될 가능성이 높다.
- 질문: residual 92%라는 수치의 분모가 무엇인가(DORC-regulated gene 전체인지, lineage별인지). core.md는 "DORC-regulated genes/lineages 대부분"이라고만 적고 있어, gene 단위 다중검정(CLAUDE.md 방법론 주의 5)이 어떻게 처리됐는지 불명확하다. 검토필요: STAR Methods에서 residual의 유의성 판정과 multiple testing correction을 확인해야 한다.
- 질문: 이 chromatin-leads-RNA 순서가 hair follicle 밖에서도 유지되는가? skin은 강한 신호를 보였지만 brain pairing accuracy가 36.7%였던 것을 보면, tissue마다 두 modality의 coupling 강도가 다를 수 있다. 본 프로젝트 Dataset인 HSPC multiome(GSE209878)에서 같은 priming 패턴이 나오는지는 별도 검증 사안이다.
- 질문: shutdown lag(transcription이 꺼진 뒤 chromatin이 닫히는 시간)는 이 paper에서 다루지 않는다. chromatin potential은 activation 방향(열림→발현)만 모델링한다. 미제공: chromatin closing이 RNA shutdown에 선행/후행하는지에 대한 분석은 본문에 없다. 본 프로젝트의 activation lag / shutdown lag 양방향 정의 중 한쪽만 이 paper로 grounding된다.

## Final Takeaways

- 이 논문의 가장 큰 의미: 같은 cell에서 ATAC와 RNA를 동시에 측정해, "chromatin accessibility가 RNA induction에 선행한다"는 직관을 paired data로 직접 보인 foundational resource다. 본 프로젝트의 chromatin-transcription lag라는 개념 자체의 출발점이고, GSE140203 mouse skin이 후속 MultiVelo(li-2023-multivelo)·MultiVeloVAE(li-2025-multivelovae)에서 재사용되는 benchmark의 원 출처다.

- 다음 논문으로 이어질 아이디어:
  - chromatin potential의 nearest-neighbor future matching을 generative kinetic model로 교체하기. 해석: 이 방향이 정확히 후속 MultiVelo가 ODE 기반 relay velocity로 간 길이다(core.md 분석 메모). 본 프로젝트는 거기서 한 발 더 나아가 gene별 activation lag / shutdown lag를 *명시적 파라미터*로 추정하는 모델을 제안할 수 있다.
  - residual/lag estimate에 대한 confound-통제 frame 추가. burst kinetics(mean·variance scaling)와 cell cycle phase를 covariate로 넣은 뒤에도 "chromatin이 먼저"가 남는 gene만 추려, artifact가 아닌 진짜 priming gene set을 정의한다. 이 정제된 gene set이 본 프로젝트의 baseline epigenomic feature 후보가 된다.
  - tissue 일반화 실험. 같은 chromatin potential / lag 추출 파이프라인을 skin, brain, HSPC multiome에 동일하게 적용해, lag 구조가 tissue-invariant한 gene과 tissue-specific한 gene을 분리한다. brain pairing 36.7%라는 신호는 tissue마다 coupling이 다를 수 있다는 경고로, 이 실험의 정당화 근거가 된다.

- 설명을 더 매끄럽게 만들 방법:
  - "chromatin이 RNA를 prime한다"는 인과 어휘를 association 수준으로 명시 분리하거나, perturbation(CRISPRi로 DORC/enhancer를 끈 뒤 target gene induction 지연 측정)으로 한 케이스라도 causal anchor를 넣으면 claim과 evidence의 gap이 좁아진다.
  - residual·chromatin potential에 negative control(simultaneous 또는 RNA-leads gene)을 추가해, 92%·prediction reach 같은 수치를 baseline 분포 위에서 해석 가능하게 만든다.
  - pseudotime 위의 "먼저"를 최소 한 lineage에서라도 실제 시간(예: pulse-chase, EdU, 또는 known stage 간격)에 anchoring하면, lag를 wall-clock으로 옮길 때의 핵심 약점이 보강된다.

- 우선순위가 높은 후속 실험 / 분석:
  1. confound-통제 후 priming gene set 재정의 (burst kinetics + cell cycle covariate) — 본 프로젝트 feature engineering의 직접 입력. 비용이 가장 낮고 영향이 크다.
  2. trajectory completeness에 대한 down-sampling sensitivity — chromatin potential의 hidden assumption을 정량 진단. 후속 lag 모델의 신뢰 조건을 정하는 데 필요하다.
  3. DORC perturbation(CRISPRi) 1~2개 lineage gene 케이스 — association을 causal로 끌어올리는 최소 실험. 비용은 높지만 paper 전체 claim의 anchor.

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Abstract: "During lineage commitment, chromatin accessibility at DORCs precedes gene expression, suggesting that changes in chromatin accessibility may prime cells for lineage commitment."
  - 사용 시나리오: 본인 introduction에서 chromatin-transcription lag / chromatin priming의 직접 선행 근거를 제시할 때. lag 개념의 foundational citation.
  - BibTeX key: `@ma2020shareseq`
- §Abstract: "We computationally infer chromatin potential as a quantitative measure of chromatin lineage-priming and use it to predict cell fate outcomes."
  - 사용 시나리오: 본인 method가 chromatin potential의 nearest-neighbor inference를 generative/kinetic model로 발전시킨다고 위치 지을 때 (prior approach 한계 짚기).
  - BibTeX key: `@ma2020shareseq`
- core.md Methods §Chromatin potential(저자 Discussion): primed chromatin state는 lineage *choice*가 아니라 lineage *bias*일 수 있다.
  - 사용 시나리오: 본인 paper에서 snapshot 기반 lag inference의 한계를 논할 때, 원저자도 bias/choice를 구분했음을 인용.
  - BibTeX key: `@ma2020shareseq`
- core.md Figure 5(저자): chromatin potential long arrows 일부는 assay noise·embedding error·technical bias에서 올 수 있다.
  - 사용 시나리오: lag/velocity arrow를 commitment로 과해석하지 말아야 한다는 주의를 본인 discussion에서 강화할 때.
  - BibTeX key: `@ma2020shareseq`

### 인용 가능 수치

- 34,774 high-quality paired profiles (adult mouse skin) (core.md Dataset 3, Abstract)
  - 사용 시나리오: 본 프로젝트 Dataset 2(GSE140203)의 규모·출처를 명시할 때.
  - BibTeX key: `@ma2020shareseq`
- 63,110 peak-gene associations (adult mouse skin); GM12878 13,277 (p < 0.05, FDR = 0.11) (core.md Dataset 4)
  - 사용 시나리오: cis peak-gene association의 scale을 baseline으로 인용하거나, FDR 수준을 비교 기준으로 쓸 때.
  - BibTeX key: `@ma2020shareseq`
- residual positive 92% of DORC-regulated genes/lineages; KS test p < 2.2 × 10^{-16} (chromatin potential vs RNA velocity reach) (core.md Dataset 5)
  - 사용 시나리오: "chromatin이 RNA에 선행"의 정량적 강도를 인용. 단 분모·multiple testing은 검토필요 표시 후 사용.
  - BibTeX key: `@ma2020shareseq`
- computational pairing accuracy: skin 74.9% vs brain 36.7% (same-cluster assignment) (core.md Background, Dataset 3)
  - 사용 시나리오: separate-modality integration의 한계, paired measurement의 필요성을 논증할 때. tissue별 coupling 차이의 근거로도.
  - BibTeX key: `@ma2020shareseq`

### 인용 가능 Figure/Table

- Figure 4 (core.md Figures §Figure 4 — lineage priming)
  - DORC accessibility onset이 promoter/nascent/mature RNA onset보다 선행하는 Wnt3 사례와 TF(Lef1/Hoxc13) motif timing을 보여준다.
  - 사용 시나리오: 본인 review·발표에서 chromatin-leads-RNA temporal ordering의 대표 도식으로 재현/인용.
  - BibTeX key: `@ma2020shareseq`
- Figure 5 (core.md Figures §Figure 5 — chromatin potential)
  - chromatin potential vector(scATAC UMAP arrows)와 RNA velocity 비교, TAC heterogeneity model.
  - 사용 시나리오: snapshot 기반 fate-direction inference의 개념 도식, 그리고 본인 method와의 비교 baseline으로.
  - BibTeX key: `@ma2020shareseq`
