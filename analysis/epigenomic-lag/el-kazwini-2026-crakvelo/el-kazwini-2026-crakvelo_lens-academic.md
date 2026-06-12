# Lens — Academic

> 근거: `el-kazwini-2026-crakvelo_core.md` (Background / Methods / Results / Figures / Tables) + sources PDF.
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 본문 밖 정보·추론은 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` prefix로 분리한다.

## Limitations

### 저자가 명시한 한계

- **HCC dataset의 region-level 불안정**: low coverage(gene ~1,000, 10kb window 내 region 보유 gene ~50%; 다른 두 dataset 78–87%)로 인해 inferred flow는 일관하나 region-level inference가 topic 수·window size perturbation에 변동(Additional file 2). 저자가 직접 인정.
- **terminal state 식별 공통 실패**: mouse brain에서 세 method 모두 ependymal cell을 terminal state로 식별하지 못함(core.md Results §Dataset 2). CRAK-Velo도 못 푸는 한계임을 본문에 명시.

### 분석자가 판단한 한계

- **부족한 점**: 공식 ablation 부재. chromatin term(Eq. 11 + reconcile 항 Eq. 13 둘째 항)을 끄고 켜는 직접 ablation이 없다.
  - 왜 중요한가: "chromatin 통합이 개선을 만든다"는 핵심 주장의 인과를 분리하려면 같은 코드에서 chromatin term만 제거한 비교가 필요. 현재는 UniTVelo(별개 RNA-only method)와의 비교로 대신하는데, UniTVelo와 CRAK-Velo는 likelihood·초기화·구현이 달라 격차가 *순수 chromatin 효과*인지 *구현 차이*인지 분리 안 됨.
  - 어떤 증거가 부족한가: `k=0`(chromatin penalty 무효화) 또는 region weight 무작위화(permutation) 대조군.
- **부족한 점**: CBDir·KNN accuracy에 통계적 유의성 표기 부재.
  - 왜 중요한가: Fig 1d / 2e의 histogram "우측 이동"은 시각적으로 명확하나, gene 단위 paired 비교의 유의성(예: Wilcoxon signed-rank)·effect size·CI가 없어 우위의 정량적 강도를 알 수 없다.
  - 어떤 증거가 부족한가: paired test p-value, median accuracy 차이 + bootstrap CI.
- **부족한 점**: 예시 gene 선택의 대표성.
  - 왜 중요한가: Fig 1c(HDC/ADCY6/STOM), 2d(Tle4/Fabp7/Ccnd2)는 저자가 고른 gene으로 cherry-picking 여지. 전체 histogram(Fig 1d/2e)이 있어 부분 완화되지만, FOXP2(HCC)에서는 MultiVelo가 약간 우위(0.428 vs 0.395)인 사례도 존재 → 일관된 우위가 아님.

### 설명이 매끄럽지 않은 지점

- **연결이 약한 주장**: "chromatin engagement가 transcriptional change를 *선행(anticipates)*한다"(core.md Results §Dataset 2, Jag2).
  - 현재 제시한 근거: KLF1·Jag2 region kinetic plot에서 accessibility 상승이 unspliced 상승보다 pseudotime상 앞섬(시각적).
  - 더 필요해 보이는 근거: 이는 *association*이지 causal anticipation이 아니다. pseudotime은 모델이 추론한 latent ordering이고, accessibility를 pseudotime 순으로 재배열(Eq. 9–10)했으므로 "선행"이 모델 가정의 산물일 수 있다. 독립 시간축(metabolic labeling, time-course) 또는 perturbation(해당 region CRISPRi 후 발현 변화)이 필요.
- **연결이 약한 주장**: TF enrichment가 "model interpretability"를 입증한다는 논리(core.md Fig 1f/2f).
  - 현재 근거: high-weight region에 IKZF1/MEIS1(HSPC), Pou3f2/Sox2(brain) ChIP-seq binding이 log-enrichment >0.
  - 더 필요해 보이는 근거: 해당 조직에서 활성인 TF는 accessible region 일반에 풍부하므로, *high-weight region에 특이적*인지 보려면 weight-matched random region 대조 또는 weight 무작위화 null이 필요(현재 null은 "expected by chance"=전체 accessible region 대비 P_global, core.md Methods §4.7 Eq. — 부분적으로만 통제).

### 정리되지 않은 질문

- 질문: $k$ hyperparameter — 본문 Eq. 13 설명의 "k=0.5"와 dataset-adaptive $k=G/R$(Eq. 15), $k=(G/R)(\mathbb{E}[n_{RNA}]/\mathbb{E}[n_{ATAC}])$(Eq. 16)의 관계가 모호. 0.5는 noise scaling 상수이고 $G/R$은 별도 항인가? 재현 시 정확한 $k$ 값을 알아야 함(Article in Press 교정 대상 가능).
- 질문: region weight $w_r^g$의 identifiability — 한 gene window에 많은 region이 있고 모두 비슷하게 accessible하면 $w_r^g$가 unique하게 추정되는가, 아니면 degenerate? HCC 민감성이 이 문제의 징후일 수 있음.
- 질문: cell cycle confound. velocity field가 cell cycle gene에 끌려가는 문제는 RNA velocity 전반의 약점인데, CRAK-Velo가 이를 어떻게 다루는지(또는 안 다루는지) 본문에 없음(미제공:).

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장
- Background(p.3): "yet all of these methods need to specify or learn from data the transcription rate of individual genes in each cell. This either imposes significant constraints on the models … or greatly expands the number of parameters"
  - 사용 시나리오: 본인 introduction에서 *RNA-only velocity의 transcription-rate 추정 한계*를 짚을 때.
  - BibTeX key: `@elkazwini2026crakvelo`
- Results(p.3): MultiVelo가 HSPC에서 "biologically dubious flow from erythrocytes to granulocytes"를 추정한다는 관찰.
  - 사용 시나리오: 본인 발표에서 *기존 chromatin-aware velocity(MultiVelo)도 spurious flow를 낸다*는 점을 들 때(우리 lag 분석의 baseline 비판 근거).
  - BibTeX key: `@elkazwini2026crakvelo`
- Conclusion(p.9): "compared to the recent method MultiVelo, CRAK-Velo offers both a simpler (and faster) … approach and a clear interpretation of how individual chromatin regions shape transcriptional trajectories"
  - 사용 시나리오: method 선택 정당화 — 우리가 CRAK-Velo를 baseline에 넣는 이유.
  - BibTeX key: `@elkazwini2026crakvelo`

### 인용 가능 수치
- HSPC run-time CRAK-Velo 15h vs MultiVelo >24h (Table S1, Additional file 1)
  - 사용 시나리오: 본인 method 비교표에서 chromatin-aware velocity의 계산 비용 인용.
  - BibTeX key: `@elkazwini2026crakvelo`
- HSPC 전처리 규모 11,605 cells / 2,000 genes / 3,939 regions, region = TSS ±10kb, ≥800 cells 검출 (core.md Results §Dataset 1, Methods §4.1)
  - 사용 시나리오: 우리 GSE209878 전처리 셋업과 직접 비교(동일 데이터).
  - BibTeX key: `@elkazwini2026crakvelo`

### 인용 가능 Figure/Table
- Figure 1b (CBDir histogram)
  - HSPC 6개 expected transition에 대해 세 method의 directional consistency를 정량 비교.
  - 사용 시나리오: 본인 review/발표에서 velocity 방향 정확도 평가 metric(CBDir) 사용 예시로 재현.
  - BibTeX key: `@elkazwini2026crakvelo`
- Figure 1g / 2h (region kinetic + weight arrow plot)
  - gene별 chromatin region accessibility와 unspliced RNA의 temporal coupling을 region weight로 시각화.
  - 사용 시나리오: 우리 chromatin–transcription lag 시각화 포맷의 reference template.
  - BibTeX key: `@elkazwini2026crakvelo`

## Final Takeaways

- **이 논문의 가장 큰 의미**: chromatin accessibility를 RNA velocity의 *production rate로 직접 구성*(Eq. 8–11)하고, 그 부산물로 gene별 region weight $w_r^g$를 추정해 *해석 가능한 regulatory layer*를 얻는다. MultiVelo보다 단순·빠르면서 동일 HSPC 데이터에서 더 정확한 terminal state·deconvolution을 보였다.
- **다음 논문으로 이어질 아이디어**:
  - chromatin term ablation($k=0$, region weight permutation)으로 chromatin 통합의 인과적 기여를 분리한 정량 연구.
  - region weight의 identifiability를 simulation으로 점검(여러 correlated region 시나리오) → HCC 민감성의 원인 규명.
  - "anticipation" 주장을 metabolic-labeling 또는 region-CRISPRi로 검증(association → causal).
- **설명을 더 매끄럽게 만들 방법**: CBDir·KNN을 paired test + effect size + CI로 보고하고, TF enrichment에 weight-matched random region null을 추가.
- **우선순위가 높은 후속 실험/분석**: 우리 GSE209878 HSPC에서 CRAK-Velo vs MultiVelo를 head-to-head로 돌리고, region kinetic plot의 accessibility-peak와 unspliced-peak pseudotime 차이를 *gene별 lag 수치*로 후처리하는 파이프라인 구축(우리 핵심 deliverable과 직결).
