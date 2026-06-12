# Safi et al., 2022 — Concurrent stem- and lineage-affiliated chromatin programs precede hematopoietic lineage restriction

> 근거: `sources/safi-2022-chromatin-priming.pdf` (Cell Reports 39(6):110798, 26 pages 본문+STAR Methods), supplementary `sources/mmc1.pdf` (Figures S1–S7), `sources/mmc2–6.xlsx` (Tables S1–S5), `sources/mmc7.pdf`.
> Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. 본문 밖 정보는 `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:`로 분리한다.

## Executive Summary

- **무엇**: mouse LSK HSPC를 single-cell ATAC-seq로 분석해, lineage commitment에 *선행*하여 stem-like chromatin program과 multi-lineage(lympho-myeloid + MegE) chromatin program을 *동시에* 보유하는 중간 transition 집단을 정의. 이 집단은 `LSKFlt3int CD9high` immunophenotype으로 prospective isolation 가능하다는 것이 핵심 contribution.
- **모델 / 방법**: scATAC-seq (8개 sorted HSPC 집단) → 571 JASPAR TFBS motif accessibility 정량 → cell을 lineage trajectory pseudotime으로 정렬 → Python `ruptures` 라이브러리의 change-point detection으로 motif accessibility가 급변하는 transition point를 cell마다 검출 → change-point density로 transition zone 위치 결정. scRNA-seq·sc-qPCR·transplantation·in vitro clonogenic assay로 직교 검증.
- **핵심 결과**:
  - ① scATAC-seq 2,680 cells, 약 283,358 peaks(107,011 distal + 37,945 promoter-proximal). LT-HSC가 chromatin 기준 2개 cluster로, ST-HSC/MPP2는 6개 cluster로 분산 — immunophenotype 집단 내부 chromatin heterogeneity 큼 (Figure 1, 2).
  - ② lympho-myeloid trajectory의 *가장 이른* transition point가 `LSKFlt3int CD9high`-dominated cluster 3에 mapping. 이 cell들은 stem-like(FoxO, Hox, Spi1 등) motif와 lineage-specific motif를 동시에 보유 (Figure 3).
  - ③ `CD9high` cell 중 stem cell marker CD150 co-expression은 소수에 그침(minority); distal peak은 promoter-proximal보다 cell type 분리력이 높음(homogeneity score 0.434 vs 0.246) (Figure 1A, 2E/2F).
  - ④ 기능 검증: `CD9high` single-cell clone의 30%가 multi-lineage progeny(24% myeloid B + 6% myeloid-erythroid) — `CD9low`(5.7%)보다 높음. transplantation에서 short-term myeloid + long-term lymphoid output을 보이나 long-term self-renewal(LSK repopulation) 없음 (Figure 6, 7).
  - ⑤ scRNA-seq(523 CD9high cells)에서 cluster 3에 30% enrich(p<10⁻⁵), HSC-like primitive signature. SPI1/PU.1 motif는 lympho-myeloid 축으로, GATA1 motif는 MegE 축으로 progressive하게 갈라짐(anti-correlation, crossover) (Figure 4, 3O).
- **우리 적용**: 우리 activation lag 가설(chromatin이 transcription·commitment보다 먼저 열린다)을 *같은 HSPC system*에서 chromatin-side로 뒷받침하는 정황 근거. 단 scATAC-seq *단독*(paired multiome 아님)이고 transition point의 축이 *pseudotime*이라 gene별 lag의 wall-clock 정량 직접 근거로는 쓸 수 없음 — `academic-citation`(선행성 주장의 supporting citation)이 1차 use_case, `methodology-reference`(change-point pseudotime 검출 절차)가 2차.
- **심층**: 한계·재현 ROI는 `safi-2022-chromatin-priming_lens-academic.md` / `safi-2022-chromatin-priming_lens-industry.md` / `safi-2022-chromatin-priming_methodology-brief.md` 참고.

## Identity

- **Title**: Concurrent stem- and lineage-affiliated chromatin programs precede hematopoietic lineage restriction
- **Authors**: Fatemeh Safi, Parashar Dhapola, Sarah Warsi, Mikael Sommarin, Eva Erlandsson, Jonas Ungerbäck, Rebecca Warfvinge, Ewa Sitnicka, David Bryder, Charlotta Böiers, Ram Krishna Thakur (co-corr.), Göran Karlsson (co-corr., lead contact). Division of Molecular Hematology, Lund Stem Cell Center, Lund University.
- **Year / Venue**: 2022, Cell Reports 39(6):110798 (open access, CC BY-NC-ND). Received 2020-04-30, Accepted 2022-04-15, Published 2022-05-10.
- **DOI**: 10.1016/j.celrep.2022.110798  |  **PMID**: 35545037
- **Citation key**: `safi2022chromatinpriming`
- **검토필요(erratum)**: `safi-2022-chromatin-priming_abstract.md`는 2023 erratum(Cell Rep. 2023;42(10):113357) 존재를 기록. 본 PDF에는 erratum 내용이 포함되지 않으므로 어떤 figure/수치가 정정되었는지 본 분석에 반영되지 않음. 인용·재현 전 erratum 원문 대조 필요.

## Background

### 풀고자 한 문제

고전 hematopoiesis 모델은 LT-HSC를 정점으로 MPP1–4를 거쳐 lineage가 단계적으로 갈라지는 hierarchy로 본다. 그러나 single-cell 분석이 축적되면서 HSPC를 "sharply demarcated gene expression program이 없는 low-primed cloud"로 보는 continuum 관점이 부상했다(Velten 2017; Giladi 2018; Laurenti & Gottgens 2018 — 본문 인용). 이 cloud 모델에서는 lineage option이 *언제*, *어느 stem-like 단계*에서, *어떤 분자 사건*으로 처음 manifest되는지가 불명확하다.

본문이 짚는 gap의 핵심: priming event를 *gene expression* 수준에서 찾으려 하면, 초기 transitional cell이 발현하는 lineage-specific TF가 *low-expressed*라서 scRNA-seq로 신뢰성 있게 검출되지 않는다(Discussion에서 Weinreb 2020 인용하며 "gene expression does not adequately delineate subtle heterogeneity within the HSC pool"이라 명시). 따라서 transcription보다 더 앞선·더 안정적인 readout이 필요하다.

### 이 논문의 전략과 기본 개념

- **읽기 layer를 chromatin으로 옮김**: lineage priming을 *chromatin accessibility*(scATAC-seq)로 측정. distal regulatory region과 그 안의 TF motif가 cell type을 정의한다는 전제(Buenrostro 2015, 2018; Andersson 2014 — 본문 인용).
- **CD9 marker 가설**: CD9(tetraspanin)는 모든 murine BM HSC에 발현(Karlsson 2013)하고, 동시에 megakaryocyte priming과 연관(Nakamura-Ishizu 2018)된다. 저자는 Flt3 발현 spectrum 위에서 CD9 수준이 chromatin 상태를 가른다고 가정.
- **Flt3int 구간의 미탐구성**: Flt3⁻ stem과 Flt3high LMPP 사이의 *Flt3int* 구간은 multipotency 측면에서 거의 연구되지 않았다. 저자는 이 구간을 chromatin으로 해부하면 multipotency→lineage restriction transition을 잡을 수 있다고 봄.

해석: 이 paper의 논리적 출발점은 우리 프로젝트와 정확히 같다 — "transcription은 늦거나 약하게 켜지므로, 더 앞선 chromatin signal을 읽어 priming/commitment의 시점을 잡자." 우리는 그 시간차(lag) 자체를 정량하려 하고, 이 paper는 chromatin이 commitment에 *선행한다는 정성적 사실*을 입증하는 데 집중한다.

## Methods

biology-finding paper이므로 protocol/분석 파이프라인 요약 깊이로 정리한다. 확률모델 중심 method paper가 아니다.

### Formal task

각 cell $c$에 대해 571개 JASPAR TFBS motif $m$의 accessibility profile $A_{c,m}$을 distal·promoter-proximal peak으로 나눠 정량하고, cell을 lineage trajectory pseudotime $t_c$로 정렬한 뒤, motif accessibility가 ongoing trend에서 *크게 이탈*하는 지점(change point)을 cell마다 검출한다. 검출된 change point의 밀도가 높은 pseudotime 구간이 "transition zone"이며, 그 zone에 어떤 immunophenotype·motif program이 mapping되는지를 본다.

### 핵심 파이프라인 (scATAC-seq)

1. **세포·라이브러리** (STAR Methods, Figure S1): mouse BM에서 8개 집단을 FACS sort — LT-HSC, ST-HSC, MPP2, pre-MegE, LMPP, 그리고 Flt3int 구간을 `LSKFlt3int`, `LSKFlt3int CD9high`, `LSKFlt3int CD9low`로 분할. 10x Chromium scATAC v1.1, NovaSeq.
2. **Cell identification** (STAR Methods): cellranger-atac v1.1.0, mm10 정렬, MAPQ>20. MACS2(`-s 150 --nomodel --shift -75 --extsize 150`)로 peak. mitochondrial contamination >3 또는 <−1(log2) cell 제거, doublet은 10x ad hoc script로 제거. supplementary Figure S3A에 집단별 cell 수 명시(LT-HSC 509, ST-HSC 230, MPP2 181, pre-MegE 495 등). 본문은 총 2,680 cells 분석.
3. **Peak / motif** : FIMO(MEME suite 4.12.0)로 571 JASPAR motif scan. peak을 TSS −2,000~+500 region은 "proximal", 그 밖은 "distal"로 분류. 약 283,358 peaks → 107,011 distal + 37,945 promoter-proximal(나머지는 gene body). cell-motif matrix를 motif별로 distal·proximal 따로 생성.
4. **Cell-motif 정규화·correlation**: cell-motif 값을 column sum으로 나누고 1,000 scaling factor 곱 → z-score. cluster-cluster correlation은 Pearson $r$. cluster는 scipy `ward` linkage. Seurat cluster와 motif cluster의 일치도는 Homogeneity metric(scikit-learn)으로 평가 — distal 0.434 vs proximal 0.246으로 distal이 cell type 분리력 우위.
5. **Cluster·trajectory**: Seurat v3.0.1, vst로 top 2,000 variable peak, PCA→UMAP(20 PC, 20 neighbors). resolution 0.75/0.1로 fine(12 cluster)·coarse(3 cluster) 두 단계. trajectory는 Slingshot v1.2, LT-HSC가 든 terminal cluster를 origin으로, 두 terminal cluster(8=lympho-myeloid, 12=MegE)로 minimum spanning tree.
6. **Change-point detection** (핵심): Python `ruptures` 라이브러리(offline change-point detection)의 sliding-window 방법으로, *각 TFBS motif의 pseudotime-ordered accessibility profile*에서 trend가 sharp하게 증가/감소하는 지점을 1개 검출. 571 motif의 change point를 cell 단위로 aggregate → 각 cell이 change point로 marked된 횟수(density)를 rolling window(window=100)로 smoothing해 trajectory별로 표시.
7. **Motif redundancy 통제**: motif sequence 중복을 Cohen's kappa로 정량. kappa cutoff 0.75에서 571→389 unique motif로 줄여 change-point 분석을 재수행 — 결과 robust(Figure S4B–S4E).
8. **Enhancer 분석**: distal peak을 FANTOM5 mouse enhancer(mm9→mm10 liftover, ±1kb 확장)와 교차 → 12,438 putative enhancer. TF-IDF 정규화 후 hierarchical clustering으로 20 enhancer cluster. motif enrichment는 Fisher's exact + Benjamini-Hochberg(FDR 5%).
9. **promoter accessibility / 'gene score'**: TSS −1,000~+250 region cut-site 정량, Nabo의 library size normalization.
10. **SnapATAC 교차검증**: SnapATAC v1.0.0로 5,000-bp bin → diffusion map(50 eigenvector, 앞 16개) → kNN(k=50). 별도 패키지에서도 8개 HSPC 집단이 broadly 동일 배치(Figure S3F).

### 직교 검증 layer

- **scRNA-seq** (10x Chromium V2): `LSKCD34+Flt3int`(1,720), `CD9high`(523), `CD9low`(219) cells. Seurat 정규화, cell-cycle(G2M/S) regress-out, BloodSpot으로 cell type annotation, Nabo v0.3.0로 CD9high/CD9low를 LSKFlt3int graph에 projection. Poisson model로 cluster enrichment 유의성(α=10⁻⁵).
- **sc-qPCR** (Fluidigm BioMark 96.96): LSKCD34+Flt3int 192 cells, index-sorted, 192개 TaqMan assay. SCExV의 random forest로 5개 subpopulation.
- **In vivo transplantation**: 50–100 donor cell + competitor를 lethally irradiated recipient에. PB를 week 2–16 추적, BM repopulation, secondary transplant. Student's t / MANOVA / type-2 ANOVA.
- **In vitro**: OP9 switch-culture(단일 clone을 erythroid/B 조건으로 분할), myeloid differentiation, CFU, CFU-MK, MegE suspension culture.

### 이전 방법과의 차이

- scRNA-seq 기반 continuum 모델(Velten 2017; Giladi 2018)은 *expression*으로 priming을 본다. 본 paper는 *chromatin*으로 옮겨, 저발현 lineage TF가 expression에서 놓치는 transition state를 검출.
- Yu et al. 2017(landmark): single clone에서 lineage-specific methylation/chromatin 차이는 보이나 mRNA에는 "no remarkable difference" — 즉 chromatin이 expression보다 먼저 갈라진다는 선행 근거. 본 paper는 이를 prospectively isolable한 단일 immunophenotype(`CD9high`)으로 구체화.

### Method 한계 (저자·분석자)

- `미제공:` paired multiome 아님. scATAC-seq와 scRNA-seq는 *서로 다른 cell batch*에서 측정 후 computational projection으로 연결. 같은 cell에서 chromatin opening과 transcription onset을 동시에 읽지 않으므로 gene별 *lag*를 직접 계산할 수 없다.
- `검토필요:` transition point의 x축은 *Slingshot pseudotime*(differentiation ordering)이지 wall-clock time이 아니다. "precede"는 pseudotime ordering상의 선행성. CLAUDE.md 방법론 주의 1(pseudotime ≠ wall-clock)에 정확히 해당.
- 저자 한계(Limitations): 작은 HSPC 집단을 여러 mouse에서 pooling → mitochondrial-mutation 기반 lineage tracking(Ludwig 2019; Xu 2019)으로 같은 cell의 chromatin+lineage를 잡으려 했으나 clear lineage track 검출 실패(data not shown).
- `미제공:` cell cycle은 scRNA-seq에서만 regress-out. scATAC-seq의 change-point/motif accessibility가 cell cycle로 confound되는지 별도 통제는 본문에 없음(단 Figure 4 주변에서 CD9 분포는 cell-cycle status와 독립이라 기술).

## Results

### Dataset 1 — scATAC-seq of 8 sorted HSPC populations (GSE173075 / 본문 Data availability)

- 총 2,680 cells. fragment size distribution은 ATAC 특성, TSS 고농축, 평균 25×10³ peak-region cut-site, Tn5 insertion의 약 67%가 aggregate peak 내. 총 약 283,358 peaks → 107,011 distal + 37,945 promoter-proximal(나머지 gene body) (Figure S2, S3; Table S1).
- **immunophenotype 내부 chromatin heterogeneity**: fine clustering 12개 cluster. LT-HSC가 chromatin 기준 2개 cluster(1, 2)로 — cluster 2가 LT-HSC의 >60%, ST-HSC로도 permeate. 고전 ST-HSC/MPP1 immunophenotype은 6개 cluster(2–7, 9)에, LSKFlt3int·pre-MegE도 3개 이상 cluster에 분산 (Figure 2C, 2D). 즉 surface marker 집단 ≠ chromatin 상태 집단.
- **distal > proximal 분리력**: distal peak의 cell-cluster 분리 homogeneity score 0.434 vs proximal 0.246. distal regulatory region이 cell type을 더 uniquely 정의 (Figure 2E, 2F).
- **TF motif lineage 특이성** (Figure 1D–1F): primitive cell·lympho-myeloid는 TEAD·FoxO motif 고접근성, lympho-myeloid는 SPI1/PU.1, MegE는 GATA1-TAL1·KLF motif 고접근성 — lineage-specifying TF accessibility가 lineage-affiliated chromatin과 일치.

### Dataset 2 — `LSKFlt3int CD9high` 집단의 동시적 chromatin signature (핵심 발견)

- **CD9가 Flt3int를 chromatin 상태로 분할** (Figure 2A–2G): HSC-like CD9 표면 수준이 LSKFlt3int 소수에서 검출되고, LMPP는 거의 전부 CD9low. UMAP에서 `CD9high`(yellow)는 ST-HSC/LSKFlt3int 경계를 가로지르는 continuum, `CD9low`(blue)는 LMPP 옆에 juxtapose — 두 집단은 LSKFlt3int 안에서 separate·non-overlapping. distal-peak correlation에서 `CD9high`(cluster 3)는 LT-HSC와 가장 높은 chromatin similarity, `CD9low`(cluster 7)는 LMPP와 강한 상관.
- **CD150 co-expression은 minority**: `LSKFlt3int CD9high` cell 중 stem marker CD150 co-express는 *소수에 그침* — LSKFlt3⁻ CD9high HSC와 대조적. 즉 CD9high는 stem-like이되 정점 stem은 아님 (Figure 1A).
- **동시적 stem + multi-lineage program** (Figure 3D, 3K): lympho-myeloid trajectory에서 *가장 이른* transition point가 `CD9high`-dominated cluster 3에 mapping. 이 cluster 3 cell은 stem-like motif(FoxO, Hox family, Spi1, Etv6, Runx family, Mecom)를 동시에 보유 — "unique concurrent accessibility of stem-like and lineage-specific TF motifs." 또한 lympho-myeloid program과 MegE program을 *동시에* 획득(Figure 3M에서 CD9high cell이 MegE TF cluster 20, 예: GATA1 motif에도 노출).
- **TF crossover** (Figure 3O): SPI1(PU.1) motif는 lympho-myeloid 축으로 progressive 증가, GATA1 motif는 MegE 축으로 증가하며 lympho-myeloid 축에서는 감소 — 개별 cell 수준 anti-correlation. CD9high cell의 downstream에서 SPI1 motif accessibility가 GATA1보다 높아지는 crossover point가 multipotency 소실의 표지일 가능성. CD9low cell은 GATA1 motif accessibility가 뚜렷이 감소(MegE 잠재력 상실).

### Dataset 3 — Enhancer 수준 early lineage priming (Figure 5)

- distal peak ∩ FANTOM5 enhancer = 12,438 putative enhancer, 20 cluster.
- lympho-myeloid 축: enhancer cluster 15(n=1,289)가 cluster 3(`CD9high` 포함)에서 dramatically 증가, master regulator(SPI1, SPIC, RUNX1, ETV6) motif enrich.
- MegE 축: enhancer cluster 16(n=1,024)이 cluster 3에서 gain 시작→cluster 10(early MegE)에서 saturate, GATA family·CTCF motif enrich.
- scATAC+scRNA 통합(bootstrap, Poisson, <0.01): `CD9high`에서 발현 up된 gene이 이 early-lineage enhancer와 nearest pairing → "frank lineage commitment가 gene expression 수준에서 일어나기 전에 multipotent `CD9high` progenitor의 chromatin에서 먼저 primed."

### Dataset 4 — scRNA-seq / sc-qPCR molecular validation (Figure 4, 6A–6D)

- scRNA-seq 10 cluster(총 2,462 cells). `CD9high`는 cluster 3에 preferential enrich(median mapping score 최고, cluster 3의 30%가 `CD9high`; Poisson p<10⁻⁵). cluster 3 radar plot은 HSC-like signature. `CD9low`는 cluster 1(LMPP/pre-GMP 유사)에 enrich(p<0.01).
- SLAM-marker progenitor(Fraticelli-Rodriguez 참조)로 projection: `CD9high` cluster 3의 75%가 multipotent SLAM-defined LT-/ST-HSC로, `CD9low` cluster 1의 80%가 lineage-committed MPP3/4로 mapping. scmap으로도 유사.
- sc-qPCR: CD9high cell이 더 primitive molecular signature(green subpopulation)이면서 differentiation marker CD48도 low 발현.

### Dataset 5 — 기능 검증: multi-lineage 잠재력 있으나 self-renewal 없음 (Figure 6, 7)

- **In vitro clonal switch-culture** (Figure 7C, 7D): `CD9high` single clone의 30%가 multi-lineage(24% myeloid B + 6% myeloid-erythroid), `CD9low`는 5.7%(4.2% myeloid B + 1.6% myeloid-erythroid).
- **CFU / MegE**: `CD9high`의 CFC capacity가 `CD9low`보다 높음(Figure 7E). megakaryocyte 잠재력은 LT-HSC와 `CD9high`에만(Figure 7F–7H). LSKFlt3int CD9high의 14.7%가 megakaryocyte, 21.8%가 erythroid progeny(`CD9low`는 3.7%, 13.3%).
- **In vivo transplantation** (Figure 6E–6I): `CD9high` 이식 시 short-term myeloid + long-term lymphoid output, engraftment는 LMPP 닮음. 그러나 long-term LSK(stem) compartment repopulation 없음 → self-renewal capacity 없음. 9일 culture 후에도 LSK profile 일부 유지(`CD9low`는 빠르게 상실).

### 전체 결과 요약

`LSKFlt3int CD9high` cell은 stem cell과 committed progenitor *사이*의 transition state로, single cell 안에서 stem-like chromatin과 lympho-myeloid+MegE chromatin program을 *동시에* 보유한다. 기능적으로 multi-lineage(in vitro·in vivo)이나 long-term self-renewal은 없다. CD9가 down되고 Flt3가 up될 때 multipotency가 lineage commitment로 넘어가는 "tug of war"를 chromatin 수준에서 포착했다. 핵심 주장: *chromatin program(특히 distal enhancer/TF motif)이 lineage commitment와 frank gene expression보다 선행*한다.

#### Simulation / ablation 성격의 robustness 체크

- motif redundancy ablation: kappa 0.75로 571→389 unique motif 축소 후 change-point 재수행, 결과 robust(Figure S4B–S4E).
- 별도 패키지(SnapATAC) 교차검증: 8개 HSPC 집단 배치 broadly 일치(Figure S3F).
- 별도 algorithm(scmap) 교차검증: SLAM projection 결과 유사.
- 통계 유의성: scRNA-seq cluster enrichment Poisson p<10⁻⁵(cluster 3) / p<0.01(cluster 1); enhancer-gene pairing bootstrap 1,000 iteration, <0.01; in vitro/in vivo는 Student's t / MANOVA / type-2 ANOVA, *p<0.05, **p<0.01, ***p<0.001.

## Figures

### Figure 1 — scATAC-seq가 early HSPC heterogeneity를 포착

#### 패널별 설명
- (A) LT-HSC, ST-HSC, `LSKFlt3int`, LMPP, `LSKFlt3int CD9high`, `LSKFlt3int CD9low`, pre-MegE를 Flt3·CD9·CD34·SLAM marker 조합으로 분리하는 FACS·sort schematic.
- (B) scATAC-seq cell의 UMAP, sorted 집단 색.
- (C) 동일 UMAP의 3개 coarse cluster.
- (D–F) primitive(D), lympho-myeloid(E), MegE(F) cluster의 571 TFBS enrichment scatter — x축 distal relative p-value, y축 promoter relative p-value. primitive=TEAD/FoxO, lympho-myeloid=SPI1, MegE=GATA1-TAL1/KLF.

#### 본문에서 강조한 비교
distal·proximal 두 축으로 lineage-specifying TF가 lineage-affiliated chromatin과 일치함을 보임.

#### 해석 시 주의점
- `검토필요:` (A)의 sort gate 정밀도(특히 CD9high vs CD9low 경계)는 mmc1 Figure S1A purity check에서 확인. CD9high가 LSKFlt3int의 소수 fraction이라 sort 오염이 결과에 영향 줄 수 있음.

### Figure 2 — CD9가 LSKFlt3int를 distinct chromatin profile로 분할

#### 패널별 설명
- (A) LSK 안 CD9high 분포 FACS.
- (B) chromatin 기준 UMAP에서 `CD9high`(yellow)·`CD9low`(blue) 위치.
- (C) 12개 fine cluster UMAP.
- (D) sorted 집단별 cluster 점유율 heatmap(LT-HSC가 cluster 1·2 양쪽, ST-HSC/MPP2가 여러 cluster).
- (E, F) 571 TFBS 기반 cell-cell correlation heatmap — distal(E, homogeneity 0.434) vs promoter(F, 0.246).
- (G) cluster-cluster Pearson r heatmap(distal): CD9high(cluster 3)–LT-HSC 高, CD9low(cluster 7)–LMPP(cluster 8) 高.

#### 본문에서 강조한 비교
CD9high·CD9low가 LSKFlt3int 안에서 separate·non-overlapping → 두 chromatin state.

#### 해석 시 주의점
- 해석: cluster 번호와 sorted 집단의 many-to-many mapping이 이 paper의 중심 메시지(immunophenotype ≠ chromatin state). cluster 3 = "CD9high-dominated"라는 표현은 dominated이지 exclusive가 아님에 주의.

### Figure 3 — stem→lineage transition의 TF motif accessibility 동역학 (가장 중요)

#### 패널별 설명
- (A, F) lympho-myeloid(A)·MegE(F) trajectory의 cell density, pseudotime 색(dark blue early, yellow late). UMAP 강조(B, G).
- (C, H) trend change point의 빈도 area plot(change-point density). lympho-myeloid의 *가장 이른* transition point가 CD9high-dominated cluster 3에 mapping.
- (D, I) 571 TFBS를 20 cluster로, pseudotime-ordered cell heatmap(early→late). TF cluster 번호 좌측.
- (E, J) 대표 TF의 cumulative accessibility를 UMAP에 (E: HOXA9-10, FoxO1, SPI1, RUNX1, MYB, GFI1A/B; J: MegE 축의 GATA family, KLF, MAX::MYC 등).
- (K, M) TF cluster 3·18(lympho-myeloid)/4·18(MegE)의 cluster별 accessibility box plot.
- (L, N) SPI1(L)·GATA1(N) motif의 scaled pseudotime별 accessibility(distal·promoter), 두 trajectory 비교.
- (O) lympho-myeloid pseudotime-ordered cell에서 SPI1·GATA1 z-score crossover, CD9high·CD9low density bar.

#### 본문에서 강조한 비교
- cluster 3(CD9high)이 stem-like + lineage-specific motif를 *동시에* 보유(E의 FoxO/Hox + Spi1/Etv6/Runx/Mecom).
- SPI1↑(lympho-myeloid) vs GATA1↑(MegE)의 개별 cell 수준 anti-correlation·crossover.

#### 해석 시 주의점
- `검토필요:` (C/H)의 x축, (L/N/O)의 x축은 모두 *scaled pseudotime / pseudotime-ordered cells*. "transition point가 CD9high에 먼저 온다"는 *ordering상의 선행성*이지 시간(hr) 선행이 아님. 우리 lag 정량 적용 시 결정적 제한.
- 해석: change-point density(C/H)가 transition zone을 정의하는 방식은 우리 activation-lag 검출에 차용할 여지가 있는 절차(methodology-reference). 단 motif 단위이지 gene 단위가 아니고, single trajectory에 1 change point만 검출.

### Figure 4 — scRNA-seq가 CD9 수준에 따른 primitive signature gradient 검증

#### 패널별 설명
- (A) LSKFlt3int scRNA-seq 10 cluster UMAP(2,462 cells).
- (B) Flt3int·CD9low·CD9high overlay.
- (C–F) CD9high(C, D)·CD9low(E, F) projection과 cluster별 mapping score box plot.
- (G, H) cluster별 분류 비율·post-assignment enrichment(CD9high가 cluster 3, CD9low가 cluster 1에 enrich).
- (I–N) cluster 3(I–K)·cluster 1(L–N)의 UMAP/DDRTree/radar — cluster 3=HSC-like, cluster 1=LMPP/pre-GMP-like.
- (O) pseudotime별 cell density: CD9high가 early에 accumulate.

#### 본문에서 강조한 비교
CD9high→primitive(cluster 3, HSC signature), CD9low→committed(cluster 1, LMPP). scATAC와 같은 결론을 transcription에서도 재현.

#### 해석 시 주의점
- `미제공:` 이 scRNA-seq는 scATAC와 *다른 cell*. projection/mapping score로 연결한 것이므로 같은 cell의 chromatin-RNA 대응은 추론 수준.

### Figure 5 — early lineage specification 동안 enhancer 동역학

#### 패널별 설명
- (A, D) lympho-myeloid(A)·MegE(D) pseudotime-ordered cell의 12,438 enhancer z-score heatmap, 20 cluster.
- (B, E) enhancer cluster 15(lympho-myeloid)·16(MegE)의 cluster별 cumulative accessibility box plot — cluster 3에서 급증.
- (C, F) cluster 15(C)·16(F) enhancer의 TFBS enrichment scatter(C: SPI1/SPIC/ETV6/RUNX1; F: GATA family/CTCF).
- (G) CD9high(n=155)·CD9low(n=132) cell UMAP(scRNA cluster 3·1 대응).
- (H) CD9high vs CD9low DE volcano.
- (I) enhancer cluster별 DE gene 연관 유의성(bootstrap, 0.01 threshold).
- (J) enhancer cluster 1·15와 CD9high/CD9low gene의 Poisson null vs observed.
- (K) cluster 15/1/8 enhancer 연관 gene UMAP + gene list.

#### 본문에서 강조한 비교
CD9high에서 발현 up된 gene이 early-lineage enhancer(cluster 15/16)와 nearest pairing → 발현 commitment 전 chromatin이 먼저 primed.

#### 해석 시 주의점
- 해석: 이 통합(scATAC enhancer ↔ scRNA DE gene, nearest within 100kb + bootstrap)이 이 paper에서 chromatin-RNA 연결의 핵심. 그러나 *nearest-enhancer + 별도 cell* 기반이라 같은 cell의 enhancer opening→transcription 시간차는 아님.

### Figure 6 — CD9high는 multi-lineage 잠재력 있으나 long-term self-renewal 없음

#### 패널별 설명
- (A) LSKFlt3int 192 cell의 Fluidigm sc-qPCR heatmap(lympho-myeloid/G0/MegE subpopulation).
- (B) PCA 5 cluster.
- (C) marker gene radar(HSC/MegE vs lympho-myeloid).
- (D) green/red/purple cluster의 index-sort CD9·CD48·CD150.
- (E) competitive transplantation 설계(week 2–16).
- (F) donor reconstitution.
- (G) lineage distribution 시간 추이(myeloid early, B/T late).
- (H) week별 lineage output.
- (I) short-term reconstitution(50 donor).
- (J, K) 배양 중 LSK 유지·myeloid(Gr1+Mac1+) fraction(day 3/6/9).

#### 본문에서 강조한 비교
CD9high engraftment가 LMPP 닮음 + short-term myeloid/long-term lymphoid, LSK repopulation 없음 → MPP, self-renewal 없음.

#### 해석 시 주의점
- `검토필요:` Figure 6I/6B의 통계(MANOVA, type-2 ANOVA)와 n(집단당 4–6 mice, 2–3 independent exp). 효과 크기·CI는 figure legend·Prism 출력에 의존, 본문 inline 수치 제한적.

### Figure 7 — CD9가 Meg/Erythroid 잠재력과 상관

#### 패널별 설명
- (A) OP9 single-cell switch-culture 설계(day1 single cell→day4 split→erythroid/B 조건).
- (B) CD9high-derived GM/macrophage/B/erythroid clone FACS.
- (C) cloning frequency·lineage-positive clone fraction.
- (D) single clone의 lineage 분포(Er/GM/B 조합) — CD9high 30% multi-lineage.
- (E) 8일 배양 후 CFC capacity(CD9high>CD9low).
- (F) CFU-MK(LT-HSC·CD9high에만).
- (G, H) suspension culture의 Meg(G)·Er(H) generating clone fraction.

#### 본문에서 강조한 비교
CD9high single clone의 multi-lineage(특히 MegE) 잠재력이 CD9low보다 큼, LMPP는 MegE 잠재력 거의 없음.

#### 해석 시 주의점
- 해석: 이 기능 검증이 "chromatin priming이 실제 multi-lineage 출력으로 이어진다"를 입증하는 핵심. 단 clone-level 출력이지 single chromatin profile과 1:1 연결은 아님(index-sort 일부 제외).

### Extended Data / Supplementary Figures (mmc1.pdf)

- **Figure S1**: 8개 집단 FACS gating·purity check(sort purity >94%). cell 수 정량.
- **Figure S2**: 집단별 ATAC fragment size distribution·TSS enrichment(QC).
- **Figure S3**: barcode QC(LT-HSC 509, ST-HSC 230, MPP2 181, pre-MegE 495 등 cell 수), 선택 TF(HOXC9/TEAD4/SPI1/ETV6/YY2/GATA1)의 proximal·distal accessibility UMAP, SnapATAC UMAP(S3F).
- `미제공:` Figure S4–S7 패널 상세는 본 분석에서 caption 일부만 확인(S4=motif redundancy/de-redundancy, S5=scRNA cluster DE·scmap projection, S6=transplantation long-term, S7 등). 정량 인용 시 mmc1 해당 페이지 재확인 필요.

## Tables

본문에 정식 inline Table 없음. 모든 표는 supplementary(STAR Methods·figure legend에서 호출).

- **Table S1** (`mmc2.xlsx`): scATAC-seq peak 통계(distal/proximal/gene body 분류 등). Figure 1·S2/S3 관련.
- **Table S2** (`mmc3.xlsx`): lympho-myeloid trajectory TF cluster 2·3 등의 motif 목록. Figure 3 관련.
- **Table S3** (`mmc4.xlsx`): MegE trajectory TF cluster motif 목록. Figure 3 관련.
- **Table S4** (`mmc5.xlsx`): scRNA-seq cluster별 DE gene·cell type radar 입력. Figure 4·5 관련.
- **Table S5** (`mmc6.xlsx`): enhancer cluster(15/16/1/8 등)의 TFBS enrichment·CD9high/CD9low DE gene·enhancer-gene pair. Figure 5 관련.
- `미제공:` 각 xlsx의 sheet·열 상세는 본 분석에서 열어 확인하지 않음(파일 크기만 확인: mmc6가 611KB로 가장 큼). 정량 인용 시 sheet 직접 확인 필요.
- **Key resources table**(본문 e1–e4): 항체·TaqMan assay·소프트웨어(SEURAT, Slingshot v1.2, FIMO v4.12.0, ruptures, NABO, SnapATAC v1.0.0, Cell Radar, SCExV) 목록.

## Supplementary Information

- mmc1.pdf: Supplemental figures S1–S7 + legend.
- mmc2–6.xlsx: Tables S1–S5(위).
- mmc7.pdf: 추가 supplementary(본 분석에서 내용 미확인 — `미제공:`. 추정: data/code 또는 추가 method note. 인용 전 확인 필요).
- **Data·code availability 모순(중요)**:
  - 본문 *Data availability*(p.14 References 직전, Figure 3 legend 직후 본문)와 Key resources table의 "Deposited data"는 scATAC = **GSE173075**, scRNA-seq = **GSE173076**, sc-qPCR = OSF `https://osf.io/y3faj/`, 추가 scRNA-seq(Rodriguez-Fraticelli 2018) = GSE90742.
  - 그러나 STAR Methods의 *Resource Availability → Data and code availability*(p.e5)는 sequencing data가 **GSE148746**에 제출되었다고 적음.
  - `검토필요:` 같은 paper 안에서 accession이 GSE173075/173076 vs GSE148746로 *불일치*. 재현·재분석 전 GEO에서 어느 것이 유효한지 직접 확인 필요. (paper-info.yaml은 분석 시점에 이 accession을 명시하지 않았으므로 추가 기록 권장.)

## 분석 자체에 대한 메모

- `질문:` change-point density(Figure 3C/3H)를 *gene-level promoter accessibility + paired RNA*로 옮기면 우리 activation-lag 검출 절차의 prototype이 될까? 이 paper는 motif 단위·single change point·non-paired라 그대로는 lag 정량 불가. 우리 GSE209878(human HSPC 10x Multiome, paired)에서 *같은 cell*의 promoter ATAC change point와 transcription onset change point를 각각 잡아 그 pseudotime 차이를 lag proxy로 정의하는 변형이 가능할지 검토.
- `질문:` 이 paper는 mouse LSK. 우리는 human HSPC. CD9high transition state·SPI1/GATA1 crossover가 human multiome에서 재현되는지(cross-species)가 우리 모델 일반화의 선결 과제.
- `검토필요:` GSE accession 불일치(GSE173075/76 vs GSE148746), erratum(2023) 반영, mmc4–7 sheet 상세 — 셋 다 재현/정식 인용 전 확인.
- 해석: 이 paper의 우리 가설에 대한 기여는 **정성적 선행성(chromatin priming이 commitment·frank expression에 선행)을 같은 HSPC system에서, prospectively isolable한 단일 immunophenotype으로 입증**한 것. *정량적 gene-level lag*의 직접 근거는 아니다(non-paired, pseudotime 축, motif 단위). lens-academic·methodology-brief에서 이 판정을 본문 근거로 상술.
