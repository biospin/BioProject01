# Lens — Academic — Trevino 2021 (Developing Human Cortex Multi-ome)

> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기 사용. 근거는 `trevino-2021-cortex_core.md` + 원문 PDF 본문.

## Limitations

### 저자가 명시한 한계
- 데이터가 mid-gestation 8주(PCW16~24)에 국한. 더 이른/늦은 시점이 있어야 gliogenesis·neuronal maturation을 더 보고 astrocyte precursor를 adult subtype에 연결할 수 있음(§Limitations).
- singleome scATAC-seq를 scRNA-seq에 data-integration으로 묶고 cell 간 lineage 관계를 추론하는 것이 한계. multiome이 많은 inference를 검증하지만 전부는 아님(§Limitations).
- cell-type-specific BPNet model은 해당 cell type에 peak이 *존재하는* variant에 대해서만 영향 평가 가능 → larger overlapping mutation set을 pseudobulk peak call에서 score할 때 significance를 희생(§Limitations).
- prioritized noncoding *de novo* mutation의 deleterious nature는 cognate cell type에서 분자 검증이 필요(미실시, §Limitations).

### 분석자가 판단한 한계
- **부족한 점**: CRE-gene link와 GPC의 "predictive chromatin"은 모두 *상관* 기반(Spearman, LM). multiome 교차검증($r=0.62$)도 cell-correspondence를 검증할 뿐 enhancer→gene의 *causal direction*은 검증하지 않는다.
  - **왜 중요한가**: 논문 핵심 서사("lineage-defining TF의 enhancer가 expression보다 먼저 active → epigenetic priming → ratchet")는 causal 메커니즘을 함의하지만 제시 근거는 association·예측이다.
  - **어떤 증거가 부족한가**: enhancer perturbation(CRISPRi) 후 target gene·motif accessibility·fate가 함께 바뀌는지, 또는 TF knockdown 후 GPC chromatin이 닫히는지에 대한 직접 실험.
- **부족한 점**: pseudotime이 분석의 시간 축인데(differential signal이 gestational time보다 pseudotime에 더 연관이라는 이유로 전환), TF wave·synergy 감소·branch priming이 *실제 시간* 구조인지 RNA velocity diffusion artifact인지 분리 안 됨.
  - **왜 중요한가**: 본 프로젝트의 activation/shutdown lag는 wall-clock 환산이 핵심인데, 이 논문은 pseudotime↔wall-clock 매핑을 제공하지 않는다(CLAUDE.md §방법론 주의 1).
  - **어떤 증거가 부족한가**: time-stamped(EdU/birthdating) 또는 다중 PCW 정밀 sampling으로 pseudotime을 calibrate.
- **부족한 점**: cell cycle을 covariate로 통제한 분석이 없다. 오히려 Figure 6은 cycling cell의 chromatin priming을 *결과*로 제시한다.
  - **왜 중요한가**: GPC chromatin–expression 상관과 cycling branch 신호가 burst kinetics/cell-cycle phase에 의해 부분적으로 confound될 수 있다(CLAUDE.md §방법론 주의 2). branch A/C는 유의(K-S 1.6e-13/5.1e-15)지만 B는 비유의(1.8e-1)인데, 이 비대칭의 생물학적 vs 기술적 원인이 구분되지 않음.

### 설명이 매끄럽지 않은 지점
- **연결이 약한 주장**: "highly cooperative regulation … resistant to perturbation … ratchet"(§Discussion)은 매력적 모델이지만, 본문 evidence는 motif synergy score(Figure 3G/3I)와 GPC enhancer 수다. perturbation resistance 자체는 측정되지 않았다.
  - 현재 근거: early TF의 motif synergy↑, late TF(MEF2C 등) synergy↓.
  - 더 필요한 근거: 실제 perturbation 후 회복(resilience) 정량.
- **연결이 약한 주장**: ASD enrichment가 early RG에서 OR=1.909(p=0.004)로 최고지만, GluN cluster들의 >1.2-fold와 함께 보면 effect size가 크지 않고 prioritized mutation 수도 작다(case 262 vs control 232; SFARI-nearest case 24 vs 17). 단일 cohort(SSC) 기반.
  - 현재 근거: BPNet effect-size scoring + Fisher test.
  - 더 필요한 근거: 독립 ASD cohort(예: SPARK/MSSNG) 재현, permutation 기반 FDR(CLAUDE.md §방법론 주의 5).

### 정리되지 않은 질문
- 질문: A1-HES / A2-OLIG 두 astrocyte precursor가 adult protoplasmic/fibrous/interlaminar subtype과 실제로 대응하는가? 본문은 speculation에 머문다(Figure 5F는 독립 dataset에서 distinct하다는 것까지만).
- 질문: mGPC(ASCL1⁺/OLIG2⁺)가 astrocyte와 oligodendrocyte의 *공통* multipotent progenitor라는 가설은 marker colocalization·module overlap 기반인데, 단일 cell lineage tracing(예: clonal barcoding) 없이 fate bipotency를 단정할 수 있는가?
- 질문: ASD control noncoding variant set은 GC content·mappability·mutational context·accessibility를 어떻게 matching했는가? (BPNet은 GC/density-matched background로 학습한다고 했으나 case/control mutation matching 절차는 STAR Methods 확인 필요 — `검토필요:`)

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장
- §Results(GPC 정의): "genes whose expression could be well predicted from local single chromatin accessibility … 185 genes with predictive chromatin (GPCs) … linked to >10 CREs"
  - 사용 시나리오: 본인 introduction에서 chromatin accessibility가 expression을 예측하는 highly-regulated gene class를 정의할 때.
  - BibTeX key: `@trevino2021cortex`
- §Discussion: "coordinated effect of many enhancers on lineage-defining factors makes the expression of those factors more resistant to perturbation … enhancers might act as a ratchet"
  - 사용 시나리오: lineage commitment의 epigenetic stabilization 가설을 motivation으로 인용(단 association임을 명시).
  - BibTeX key: `@trevino2021cortex`
- §Discussion(method 주장): "modeling of the regulatory potential of individual base pairs was crucial … as simple overlap with open chromatin regions did not provide the required specificity"
  - 사용 시나리오: 본인 paper에서 peak-overlap annotation 한계를 짚고 sequence model 필요성을 주장할 때.
  - BibTeX key: `@trevino2021cortex`

### 인용 가능 수치
- 57,868 scRNA cell + 31,304 scATAC cell, 657,930 peak, 64,878 CRE-gene link(median 5 CRE/gene); multiome 8,981 cell에서 53%(40,181) 직접 확인 (§Results, Figure 2H)
  - 사용 시나리오: fetal human cortex multiome reference scale·link validation 인용.
  - BibTeX key: `@trevino2021cortex`
- BPNet early RG ASD mutation OR=1.909(Fisher p=0.004) vs naive peak overlap OR=1.02(p=1.0), fetal-heart control OR=0.97~1.01(p=1.0) (§Results, Figure 7C)
  - 사용 시나리오: cell-type-specific sequence model이 naive annotation보다 disease variant를 더 잘 prioritize한다는 근거.
  - BibTeX key: `@trevino2021cortex`
- singleome vs multiome GPC 상관 $r=0.62$, $P<2.2\times10^{-16}$ (Figure 2I)
  - 사용 시나리오: singleome 기반 enhancer-gene link 추론의 신뢰도 근거.
  - BibTeX key: `@trevino2021cortex`

### 인용 가능 Figure/Table
- Figure 3F (§Results): GluN trajectory의 TF expression–motif activity sequential wave(PAX6→SOX/ASCL1→EOMES/NFI/NEUROD1→NEUROD2/MEF2C).
  - 사용 시나리오: corticogenesis TF cascade를 review/발표에서 도식으로 인용.
  - BibTeX key: `@trevino2021cortex`
- Figure 7A (§Results): scATAC peak + sequence → CNN → de novo variant prioritization pipeline schematic.
  - 사용 시나리오: noncoding variant interpretation workflow를 본인 method 비교에 인용.
  - BibTeX key: `@trevino2021cortex`

## Final Takeaways
- **이 논문의 가장 큰 의미**: 같은 cell의 multiome으로 검증된 fetal human cortex enhancer-gene link atlas + cell-type-specific sequence model로 ASD noncoding variant를 prioritize한 reference. 후속 multiome velocity 연구의 human cortex benchmark.
- **다음 논문으로 이어질 아이디어**:
  - GPC enhancer / lineage TF를 CRISPRi로 perturb해 "ratchet" 가설(perturbation resistance)을 직접 측정.
  - GSE162170 multiome subset에 MultiVelo/MultiVeloVAE를 적용해 motif accessibility→target expression의 *명시적 lag*를 정량화(본 논문이 안 한 부분).
  - 독립 ASD cohort(SPARK)에서 BPNet prioritization 재현 + permutation FDR.
- **설명을 더 매끄럽게 만들 방법**: pseudotime을 birthdating/다중 PCW sampling으로 calibrate해 wall-clock 환산을 제공하면 "wave/priming" 서사가 시간 구조로 단단해진다.
- **우선순위가 높은 후속 실험/분석**: (1) 우리 chromatin–transcription lag framework로 GSE162170 multiome에 activation lag를 측정해 본 논문의 sequential-motif 관찰과 정렬, (2) cell cycle phase를 covariate로 통제한 GPC 상관 재계산으로 confound 분리.
