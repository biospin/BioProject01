# Lens — Academic — Safi et al., 2022 (chromatin priming)

> 근거: `safi-2022-chromatin-priming_core.md` + `sources/safi-2022-chromatin-priming.pdf`.
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.

### Limitations

#### 저자가 명시한 한계
- (Limitations of the study) 같은 cell에서 chromatin과 lineage를 동시에 잡기 위해 mitochondrial-mutation 기반 lineage tracking(Ludwig 2019; Xu 2019)을 시도했으나, 작은 HSPC 집단을 여러 mouse에서 pooling해야 했기 때문에 clear lineage track을 검출하지 못함(data not shown). 저자는 future sc-multi-omics + lineage tracing이 transition state를 더 정확히 잡을 것으로 기대.
- (Discussion) 저발현 lineage-specific TF는 scRNA-seq로 신뢰성 있게 검출되지 않아(Weinreb 2020 인용) early transitional state 식별이 expression만으로는 불가능 — 이것이 chromatin readout을 채택한 이유이자 동시에 transcription-side 검증의 한계.

#### 분석자가 판단한 한계
- **부족한 점**: scATAC-seq와 scRNA-seq가 *서로 다른 cell batch*에서 측정되고 computational projection(Nabo, scmap, mapping score)으로만 연결됨. paired multiome이 아니다.
  - 왜 중요한가: 이 paper의 중심 주장 "chromatin program이 frank gene expression에 선행한다"는 *같은 cell*에서 chromatin opening과 transcription onset의 시점을 비교해야 직접 입증된다. 현재는 두 modality를 *집단 수준 projection*으로 대응시킨 association이다.
  - 어떤 증거가 부족한가: 같은 single cell의 promoter ATAC(또는 enhancer) accessibility와 그 gene의 nascent/mature transcript를 동시에 읽은 데이터. 이것이 있어야 enhancer cluster 15/16 opening → DE gene 발현의 시간 순서가 *추론*이 아닌 *측정*이 된다.
- **부족한 점**: transition point의 축이 Slingshot pseudotime(differentiation ordering)이며 wall-clock time이 아니다.
  - 왜 중요한가: "precede"는 pseudotime ordering상의 선행으로만 보장된다. CLAUDE.md 방법론 주의 1(pseudotime ≠ wall-clock)에 정확히 해당. lineage priming chromatin이 시간(hr/day)으로 commitment보다 먼저인지는 입증되지 않음.
- **부족한 점**: change-point detection이 *motif 단위*이고 trajectory별 *single change point*만 검출(ruptures sliding-window, 1개 detect).
  - 왜 중요한가: gene-level lag 구조나 다중 transition을 잡지 못한다. transition을 "한 지점"으로 환원하므로, 점진적·다단계 priming(stem→bipotent→committed)을 단일 zone으로 압축할 위험.
- **부족한 점**: cell cycle confound가 scRNA-seq에서만 regress-out됨. scATAC-seq의 motif accessibility/change-point는 cell-cycle 통제 없음(본문은 CD9 분포가 cell-cycle status와 독립이라 기술하나 이는 marker 분포 수준).
  - 왜 중요한가: CLAUDE.md 방법론 주의 2(cell cycle을 covariate로 통제하지 않으면 lag/accessibility estimate가 artifact). chromatin accessibility는 cell-cycle phase에 민감하므로 transition zone이 부분적으로 proliferation 신호일 수 있음.

#### 설명이 매끄럽지 않은 지점
- **연결이 약한 주장**: "stem-like와 lineage-affiliated program을 *concurrent*하게 한 cell이 보유한다."
  - 현재 근거: pseudotime-ordered cell의 motif accessibility heatmap(Figure 3D)에서 cluster 3 cell이 두 program의 motif를 모두 보유. SPI1/GATA1 anti-correlation(Figure 3O).
  - 더 필요한 근거: concurrent가 *같은 단일 cell의 동시 open*인지, 아니면 cluster 3 안에서 서로 다른 cell이 각각 stem/lineage program을 가져 *집단 평균*으로 concurrent처럼 보이는지 구분 필요. single-cell co-accessibility(같은 cell에서 stem motif와 lineage motif가 동시에 open인 cell 비율)를 직접 제시하면 강해진다.
- **연결이 약한 주장**: enhancer cluster opening이 DE gene 발현을 "primes"한다(인과적 뉘앙스).
  - 현재 근거: nearest-enhancer(within 100kb) + bootstrap Poisson enrichment(별도 cell).
  - 더 필요한 근거: 이는 nearest-pairing association. enhancer-gene linkage(co-accessibility, HiC, eQTL)나 perturbation(enhancer deletion/CRISPRi 후 DE gene 변화) 없이 causal "prime"으로 읽으면 과해석.

#### 정리되지 않은 질문
- 질문: cluster 3(CD9high)의 *individual* cell 중 몇 %가 stem motif와 lympho-myeloid+MegE motif를 *동시에* open하고 있나? 집단 평균 concurrent vs single-cell concurrent의 구분이 핵심 주장의 강도를 결정.
- 질문: SPI1/GATA1 crossover point(Figure 3O)가 multipotency 소실 표지라면, 그 point의 cell을 prospectively 분리해 transplant하면 self-renewal/multipotency가 정확히 어디서 꺾이나?

## Final Takeaways

- **이 논문의 가장 큰 의미**: HSPC continuum에서 multipotency→lineage restriction transition을, *prospectively isolable한 단일 immunophenotype(`LSKFlt3int CD9high`)* 으로 고정하고, 그 transition state가 stem-like + multi-lineage chromatin program을 동시에 보유함을 chromatin·transcription·기능 검증으로 일관되게 보임. "chromatin priming이 commitment·frank expression에 선행"한다는 *정성적 선행성*을 같은 system에서 입증.
- **다음 논문으로 이어질 아이디어**:
  - paired multiome(10x Multiome ATAC+GEX)으로 `CD9high` transition 구간을 재측정 → 같은 cell에서 enhancer/promoter opening과 transcript onset의 pseudotime 차이를 *직접* 정량. (우리 GSE209878 human HSPC가 바로 이 데이터 형식.)
  - mitochondrial lineage tracing의 pooling 한계를 single-mouse 대용량 sort 또는 transgenic barcoding으로 우회 → 같은 clone에서 chromatin state와 실제 lineage output 연결.
  - SPI1/GATA1 crossover point cell의 functional fate map(barcoded transplant).
- **설명을 더 매끄럽게 만들 방법**: (1) single-cell co-accessibility로 "concurrent"를 집단 평균이 아닌 cell 단위로 입증. (2) cell-cycle을 scATAC change-point 분석의 covariate로 통제. (3) enhancer-gene linkage를 nearest가 아닌 co-accessibility/HiC로 보강.
- **우선순위가 높은 후속 실험/분석**: paired multiome 재측정 + same-cell lag 정량. 우리 프로젝트가 정확히 이 gap을 메우는 작업이므로, 이 paper는 우리 결과의 *선행성 주장 supporting citation*으로 최적.

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장
- §Summary/Discussion: "concurrently display stem-like and lineage-affiliated chromatin signatures, pointing to a simultaneous gain of both lympho-myeloid and megakaryocyte-erythroid programs"
  - 사용 시나리오: 우리 논문 introduction에서 "chromatin priming이 lineage commitment에 선행한다"는 prior evidence를 같은 HSPC system에서 인용할 때.
  - BibTeX key: `@safi2022chromatinpriming`
- §Discussion: gene expression "does not adequately delineate subtle heterogeneity within the HSC pool" (Weinreb 2020 맥락 인용)
  - 사용 시나리오: 우리 논문에서 *왜 transcription만으로는 lag/priming을 못 잡고 chromatin readout이 필요한가*를 정당화할 때.
  - BibTeX key: `@safi2022chromatinpriming`
- §Results: "the most distinct TFBS motifs in these enhancers are established lineage-affiliated master regulators like SPI1, SPIC, RUNX1, and ETV6" (lympho-myeloid enhancer cluster 15)
  - 사용 시나리오: lineage-specifying TF의 chromatin 선행성을 보일 때 motif-level 근거로.
  - BibTeX key: `@safi2022chromatinpriming`
- §Results: "frank lineage commitment ... at the level of gene expression is first primed by the chromatin of multipotent LSKFlt3intCD9high progenitors"
  - 사용 시나리오: 우리 핵심 주장(chromatin이 expression에 선행)과 *직접 동형*인 문장 — discussion에서 우리 결과를 이 선행 결과와 나란히 둘 때.
  - BibTeX key: `@safi2022chromatinpriming`

### 인용 가능 수치
- scATAC-seq 2,680 cells, 약 283,358 peaks (107,011 distal + 37,945 promoter-proximal); distal homogeneity score 0.434 vs proximal 0.246 (§Results, Figure 2E/2F)
  - 사용 시나리오: distal regulatory region이 cell type 분리력이 높다는 근거로(우리 feature 선택에서 distal enhancer 우선 논거).
  - BibTeX key: `@safi2022chromatinpriming`
- `CD9high` single clone의 30%가 multi-lineage progeny, `CD9low`는 5.7% (§Results, Figure 7C/7D); 571 JASPAR TFBS motif change-point 분석(§Methods)
  - 사용 시나리오: chromatin priming의 기능적 결과(multi-lineage 출력) 정량 인용.
  - BibTeX key: `@safi2022chromatinpriming`

### 인용 가능 Figure/Table
- Figure 3 (§Results)
  - stem→lineage transition을 따라 TF motif accessibility change-point density와 SPI1/GATA1 crossover를 보임.
  - 사용 시나리오: 우리 review/발표에서 *pseudotime을 따라 chromatin이 먼저 갈라진다*를 보이는 대표 도식으로 재인용.
  - BibTeX key: `@safi2022chromatinpriming`
- Figure 1A (§Results)
  - `CD9high`/`CD9low`를 포함한 HSPC sort schematic — prospective isolation 전략.
  - 사용 시나리오: transition state를 marker로 분리할 수 있음을 보일 때.
  - BibTeX key: `@safi2022chromatinpriming`
