# Trevino 2021 — Developing Human Cortex Multi-ome — Core Analysis

## Executive Summary

- **무엇**: 임신 중기(PCW16~24) human cerebral cortex에서 scRNA-seq, scATAC-seq, 그리고 같은 cell의 joint multiome을 함께 측정해, corticogenesis(피질 발생)의 cell-type/state별 regulatory element activity를 single-cell로 지도화하고 이를 ASD noncoding *de novo* mutation 해석에 연결한 Cell 2021 Resource paper.
- **모델 / 방법**: (1) scATAC gene activity score와 scRNA expression을 CCA(canonical correlation analysis)로 cell-level 통합, (2) pseudobulk 위에서 CRE accessibility–gene expression의 Spearman 상관으로 enhancer-gene link($n=64{,}878$ singleome) 추론, link 수가 많고 상관이 높은 185개 유전자를 "predictive chromatin을 가진 유전자(GPC, gene with predictive chromatin)"로 정의, (3) RNA velocity 기반 diffusion으로 pseudotime을 부여해 differentiation trajectory 위에서 TF motif activity와 expression의 wave를 분석, (4) base-pair-resolution CNN(BPNet 기반)을 cluster별 ATAC profile에 학습시켜 noncoding variant의 cell-type-specific disruption score를 계산.
- **핵심 결과**:
  - ① **Atlas 규모** — 57,868 single-cell transcriptome + 31,304 single-cell epigenome(filtering 후), 657,930 accessible peak, 4개 sample(PCW16/20/21/24). singleome CCA에서 64,878 CRE-gene link, multiome 8,981 cell에서 40,181/(40,181+23,849) link가 교차 확인.
  - ② **GPC / lineage-determining TF** — 185개 GPC는 transcription regulator·DNA-binding TF activity에 강하게 enrich되고(GO), early differentiating cell에서 active chromatin state를 먼저 획득. predictive chromatin 상관은 singleome vs multiome에서 $r=0.62$ ($P<2.2\times10^{-16}$)로 재현.
  - ③ **Trajectory의 TF wave** — GluN(glutamatergic neuron) 계통에서 13,989개 dynamic CRE-gene link를 5개 cluster로 분할, motif가 PAX6 → SOX2/6/9·GLI3·ASCL1 → EOMES·NFIA·NFIB·NEUROD1 → NEUROD2·BHLHE22·MEF2C 순으로 sequential wave. 초기에는 TF coordination/synergy 높고 후기 TF는 더 독립적으로 작동.
  - ④ **Glial 이원성** — astrocyte precursor가 A1-HES(HES4/CAV2↑)와 A2-OLIG(SPARCL1/ID3/IGFBP7↑) 두 집단으로 갈리며, OLIG1 vs SOX21 motif accessibility로 구분. ASCL1⁺/OLIG1⁺ 다능성 glial progenitor(mGPC)가 astrocyte·oligodendrocyte 공통 전구체로 제안.
  - ⑤ **ASD variant** — 1,902 family(An et al. 2018)의 *de novo* noncoding mutation을 분석. peak-level naive overlap은 enrichment 없음(GluN6 OR=1.02, p=1.0)이나, BPNet disruption score를 쓰면 early RG cluster에서 OR=1.909(Fisher p=0.004), GluN2/3/4/6/9에서 >1.2-fold enrichment. CTCF·NRF1·E-box/bHLH·homeobox motif가 자주 disrupt.
- **우리 적용**: `methodology-reference`(CCA peak-gene linking, pseudotime 위 motif-expression wave, BPNet variant scoring) + `academic-citation` + `pipeline-applicable`. GSE162170은 후속 multiome velocity 논문(MultiVelo, MultiVeloVAE)이 fetal human cortex benchmark로 재사용하는 reference dataset이라 본 프로젝트 Dataset 3의 원 출처.
- **심층**: 한계·재현 ROI는 `trevino-2021-cortex_lens-academic.md` / `trevino-2021-cortex_lens-industry.md` / `trevino-2021-cortex_methodology-brief.md` 참고.

## Identity

- **Title**: Chromatin and gene-regulatory dynamics of the developing human cerebral cortex at single-cell resolution
- **Authors**: Trevino, Alexandro E.; Müller, Fabian; Andersen, Jimena; Sundaram, Lakshman; Kathiria, Arwa; Shcherbina, Anna; Farh, Kyle; Chang, Howard Y.; Pașca, Anca M.; Kundaje, Anshul; Pașca, Sergiu P.; Greenleaf, William J. (Trevino·Müller·Andersen·Sundaram contributed equally; co-corresponding S.P.P. + W.J.G.)
- **Year / Venue**: 2021, Cell 184(19):5053–5069.e23 (Resource). Received 2020-12-29, accepted 2021-07-28, published 2021-08-13(online)/09-16.
- **DOI / PMID**: `10.1016/j.cell.2021.07.039`, PMID `34390642`
- **Citation key**: `@trevino2021cortex`
- **Source boundary**: 분석 근거는 `sources/trevino-2021-cortex.pdf`(main text + Figure 1–7, Discussion/Limitations) 본문. STAR Methods 세부와 supplementary table/figure(Figures S1–S8, Table S1–S6)는 online supplemental에 있고 로컬에 없어 `미제공:`로 표시. `sources/abstract.txt`, `sources/data_GSE162170.url` 보조.

## Background

### 배경 스토리

- **문제의 출발점**: cortical development의 genetic perturbation은 ASD를 포함한 neurodevelopmental disease로 이어진다(§Introduction; Rubenstein 2011, Zhou et al. 2019 인용). 그러나 ASD-associated genetic variant가 어떤 cell state에서 어떤 cis-regulatory element를 교란하는지는 아직 미해결이라고 저자가 직접 명시한다("it is still unknown how genetic variants … interfere with the genetic programs underlying the development of the cerebral cortex").
- **Corticogenesis의 복잡성**: apical/basal radial glia(RG)의 확장, ventricular/subventricular zone(VZ/SVZ)에서의 intermediate progenitor 생성, glutamatergic neuron의 inside-out 생성, astrocyte·oligodendrocyte 분화가 동시에 진행된다. GABAergic neuron·microglia 등은 dorsal forebrain 밖에서 이주해 합류한다(Greig et al. 2013, Molnár et al. 2019 등 인용).
- **선행 접근의 한계**: regulatory element 활성과 disease variant의 시점·cell type을 분해하려면 chromatin과 gene expression state를 모두 single-cell로 보아야 하는데, 두 modality를 따로 보면 같은 cell에서 transcript output과 regulatory state를 직접 묶지 못해 enhancer-gene link가 간접 추론에 머문다(§Introduction).
- **이 논문으로 이어지는 gap**: 저자는 scRNA-seq, scATAC-seq, 그리고 *같은 cell*의 multiome을 한 sample 셋에서 측정하여 cell-type별 regulatory map을 만들고, 이를 ASD noncoding mutation 해석에 연결한다.

### 기본 개념

- **Cis-regulatory element (CRE)**: promoter/enhancer 등 gene expression을 조절하는 noncoding genomic element. 본 논문 핵심 신호는 chromatin accessibility와 linked gene expression의 공변(co-variation)이다.
- **Gene activity score**: 한 유전자 주변 local chromatin accessibility를 합산해 정의한 ATAC 기반 발현 proxy(Pliner et al. 2018 방식 인용). RNA expression과의 상관 비교 기준이 된다.
- **GPC (gene with predictive chromatin)**: 인근 putative enhancer 수가 많고 gene activity–expression 상관이 높은 유전자 class(저자 신규 정의). 185개로 정의. 외부의 "super-enhancer"·"super-interactive promoter" 개념과 유사하다고 저자가 직접 언급(§Discussion).
- **Pseudotime**: RNA velocity(La Manno et al. 2018, Bergen et al. 2020) 기반 diffusion으로 부여한 연속 발생 순서 축. wall-clock time(gestational week)과는 별개로 다룬다 — 저자는 "differential expression이 gestational time보다 pseudotime에 더 연관"이라고 보고하고 분석을 pseudotime 축으로 전환한다.
- **Base-pair-resolution neural network (BPNet)**: genomic sequence → cluster별 pseudobulk ATAC profile/count를 예측하는 CNN. dilation + residual skip 구조(Avsec et al. 2020 BPNet 인용). DeepLIFT/ISM 류 importance score로 variant의 local disruption을 평가.

## Methods

### 자료 유형과 분석 깊이

- 이 논문은 순수 algorithm paper가 아니라 **experimental atlas + regulatory genomics finding** paper다. 따라서 method는 (a) data generation protocol, (b) 통합·linkage·trajectory의 통계 구조, (c) deep-learning variant scoring을 중심으로 정리한다.
- `미제공:` STAR Methods 세부(cell dissociation, library 조건, 정확한 QC threshold, peak calling parameter, BPNet hyperparameter, train/test fold 정의)는 online STAR Methods에 있고 로컬에 없다. 본문에 언급된 수준까지만 단정한다.

### 이 method가 푸는 문제

- **Formal task**: developing human cortex의 cell state에 대해 (i) chromatin accessibility와 gene expression을 cell-level로 통합, (ii) CRE–gene link 추정, (iii) differentiation trajectory(pseudotime)를 따른 TF motif activity·expression dynamics, (iv) noncoding variant의 cell-type-specific regulatory disruption을 추정.
- **입력**: 4 sample(PCW16/20/21/24)의 scRNA-seq + scATAC-seq("singleome", 따로 측정) 및 PCW21의 10x Multiome(같은 cell), ASD cohort의 *de novo* noncoding mutation, 그리고 hg genome sequence.
- **출력**: cell type/state atlas, 64,878 CRE-gene link, 185 GPC, GluN trajectory의 5-cluster dynamic link + sequential TF motif wave, glial gene module 14개, cluster별 BPNet model과 variant disruption score.

### 확률 / 통계학적 구조

- **Cell-level 통합 (CCA)**: scATAC에서 유전자별 gene activity score를 만들고, scRNA expression과 canonical correlation analysis로 정렬해 각 modality cell을 다른 modality의 nearest neighbor에 matching(Stuart et al. 2019 방식 인용). 50-NN 기반 cluster 할당이 single nearest neighbor보다 일치도를 높였다(Figures S4A–S4B).
- **CRE-gene linkage**: pseudobulk aggregate(majority cluster·ATAC cluster·time으로 annotate한 200 pseudobulk) 위에서 gene-distal CRE accessibility와 gene expression의 상관을 계산(Corces et al. 2018 방식). 한 gene은 median 5개 CRE에 link($n=64{,}878$ link). linked CRE는 unlinked보다 cell-type-specific 3D promoter-centric interaction(Song et al. 2020)에 의해 뒷받침될 가능성이 높음(Wilcoxon $p<2.2\times10^{-16}$).
- **GPC 정의**: gene activity–expression 상관 상위 + linked CRE >10인 유전자 185개. GO상 transcription regulator/DNA-binding TF activity에 강하게 enrich.
- **Pseudotime / trajectory**: RNA velocity diffusion으로 cell별 pseudotime 부여, RNA cell의 pseudotime을 nearest ATAC neighbor로 transfer. GluN lineage에서 13,989 dynamic CRE-gene link를 $k$-means $k=5$로 분할(363 pseudotime-bin pseudobulk).
- **Motif synergy / family accessibility**: chromVAR류 TF motif activity(Schep et al. 2017)와 expression의 상관·synergy를 31 TF × 24 motif cluster로 묶어 분석.
- **Glial module**: fuzzy c-means clustering($c=14$ module)으로 co-expressed gene module을 정의, cell이 여러 module에 부분 소속되도록 허용(soft assignment). module centroid 간 pairwise Jaccard >0.2로 connectivity 그림.
- **BPNet variant scoring**: cluster별 250,000+ ATAC peak + 2,114 bp sequence context로 CNN 학습. GC·density-matched genomic background로 bias 보정. held-out chromosome 5-fold CV에서 예측-관측 Tn5 coverage 상관(GluN6 mean Spearman $\rho=0.58$). variant는 ref/alt 예측 count의 allelic fold-change 기반 local disruption score로 평가.

### 핵심 method insight

- **같은 cell의 multiome으로 singleome 추론을 검증**: singleome은 modality를 따로 측정하므로 cell-cell 대응이 추정값이다. PCW21 multiome(대응이 known)에서 CCA를 적용해 53%의 inferred link가 직접 확인되고($40{,}181$), GPC 상관이 $r=0.62$로 재현됨으로써 singleome 추론의 신뢰도를 보강한다(Figure 2H–2I).
- **lineage-defining TF의 chromatin이 expression보다 먼저 active**: GPC(주로 TF)는 많은 linked enhancer를 통해 early differentiating cell에서 active chromatin state를 먼저 획득 → lineage commitment의 epigenetic priming 가설로 연결.
- **noncoding variant는 peak annotation이 아니라 sequence model이 필요**: naive peak overlap은 ASD enrichment를 못 잡지만(OR≈1.0), base-pair-resolution model의 effect-size scoring이 있어야 cell-type-specific enrichment가 드러난다 — 본 논문의 가장 결정적 method 주장.

### 이전 방법과 차이

- bulk ChIP/ATAC 대비: cell type·cell state 해상도를 유지하면서 enhancer-gene link를 추론. (CLAUDE.md §방법론 주의 4의 "bulk ChIP cell type 해상도 손실" 문제를 multiome ATAC peak으로 우회.)
- 단순 peak-overlap 기반 variant annotation 대비: BPNet effect-size scoring으로 sparse causal mutation의 specificity를 확보.

### Results에서의 효과

- singleome↔multiome 교차 검증으로 link/GPC 신뢰도 확보(Figure 2H–2I).
- pseudotime 축 전환이 differential signal을 더 잘 분리(gestational time 대비; §Results).
- BPNet scoring이 ASD enrichment를 early RG에서 OR 1.909로 드러냄(naive overlap OR≈1.0과 대비).

### Method 한계

- **CCA 통합의 inference 한계**: 저자가 §Limitations에서 직접 — singleome scATAC를 scRNA에 data-integration으로 묶고 cell 간 lineage 관계를 추론하는 것은 한계. multiome이 많은 추론을 검증하지만 전부는 아님.
- **pseudotime ≠ wall-clock**: lag/순서는 pseudotime 단위. 실제 시간 검증은 별도 필요(본 프로젝트 CLAUDE.md §방법론 주의 1과 정확히 일치).
- **cell-type-specific model의 peak 의존**: 해당 cell type에 peak이 있는 variant만 평가 가능(저자 명시).
- **causal proof 부재**: CRE-gene link와 variant disruption은 강한 association·예측이며, deleterious nature의 분자 검증은 cognate cell type에서 미실시(저자 명시).

## Results

### Dataset 1 — Singleome scRNA-seq + scATAC-seq atlas (PCW16/20/21/24)

- **규모**: filtering 후 57,868 single-cell transcriptome, 31,304 single-cell epigenome, 657,930 accessible peak(potential CRE). 4 primary sample(PCW16/20/21/24)(§Results "A single-cell regulatory atlas").
- **검증 marker**: immunohistochemistry(IHC)로 CTIP2⁺ cell이 cortical plate(CP), SOX9⁺ cell이 VZ/SVZ/oSVZ, GFAP⁺ scaffold가 neocortex 전반, KI67이 GFAP⁺·PPP1R17⁺ IPC와 colocalize(Figure 1B–1C, S1I–S1J)로 atlas annotation 뒷받침.
- **cell type**: RG(vRG: FBXO32/CTGF; oRG: MOXD1/HOPX; early RG PCW16: NPY/FGFR3; late RG PCW20–24: CD9/GPX3), cycling(TOP2A/KI67), tRG(CRYAB/NR4A1/FOXJ1), mGPC(ASCL1/OLIG2/PDGFRA/EGFR), OPC/Oligo(SOX10/NKX2.2/MBP), nIPC(EOMES/PPP1R17/NEUROG1), GluN(BCL11B/CTIP2, SATB2, SLC17A7/VGLUT1), SP(NR4A2/CRYM), IN(DLX2/GAD2; MGE: LHX6/SST; CGE: SP8/NR2F2; PSB: MEIS2/ETV1), MG(AIF1/CCL3), EC(CLDN5/PECAM1), Peric(FOXC2/PDGFRB), VLMC(COL1A1/LUM), RBC(HEMGN)(Figure 1F–1H, Table S1).
- **재현성**: 두 독립 prior scRNA-seq dataset(Bhaduri et al. 2020, Polioudakis et al. 2019)을 manifold에 projection해 cell type Jaccard 일치 높음(Figure S2). cycling progenitor만 chromatin landscape에 직접 매핑 안 됨(예외, §Results).

### Dataset 2 — Multiome (PCW21, 같은 cell)

- **규모**: 두 modality 모두 high-quality인 8,981 cell(Table S2, Figures S3N–S3T).
- **link 교차검증**: CRE-gene linking을 multiome(대응 known)에 적용 → 40,181 inferred peak-gene link(53%)가 직접 확인, 추가 23,849 link 신규 식별(Figure 2H). singleome vs multiome GPC 상관 $r=0.62$ ($P<2.2\times10^{-16}$)(Figure 2I).
- **의미**: singleome 추론이 known-correspondence dataset에서 대체로 검증됨.

### Dataset 3 — GluN differentiation trajectory (TF wave)

- 13,989 dynamic CRE-gene link를 pseudotime 따라 5 cluster로 분할(363 pseudobulk; Figure 3C, Table S3). early-pseudotime link는 cell division·neural precursor(GO), late link는 morphogenesis·migration·maturation에 enrich(Figure 3D).
- ASD susceptibility gene(Abrahams et al. 2013)은 intermediate~late interaction에 더 link(Figure 3D).
- cluster별 TF motif: early=ZNF740/KLF16/SP1·2/ASCL1, intermediate~late=NEUROD1/2·NEUROG1·MEF2C(Figure 3E).
- TF expression × motif accessibility 동기화 wave: PAX6 → SOX2/6/9·GLI3·ASCL1 → EOMES·NFIA·NFIB·NEUROD1 → NEUROD2·BHLHE22·MEF2C(31 TF × 24 motif cluster; Figure 3F).
- motif synergy 3 class: (1) early 중간 synergy(SOX/GLI/PAX), (2) intermediate 강한 family-내 synergy(NFI/TBX/EOMES), (3) late 저-cooperative·독립(NEUROD2/BHLHE22/MEF2C)(Figure 3G–3I). 초기 TF coordination 높고 후기일수록 더 적은 TF가 독립적으로.
- **migrating neuron 비교**: early(PCW16) vs late(PCW20–24)에서 LIMCH1/RUNX1/SNCB/DOK5↑, AP-1(JUN/FOS)·heat shock(HSPA1A/B)·DUSP1↓(Figure S4J, Table S3). 단 neurogenesis 관련 DEG는 의외로 적어, 변이가 gestational time보다 pseudotime에 더 연관.

### Dataset 4 — Glial lineage gene modules

- fuzzy c-means $c=14$ module로 glial expression program 분해(Figure 4A–4B, Table S4). cycling("Cyc") cell에 뿌리, time과 상관(Figure 4B).
- glial maturation gene FOXJ1(ependymal)·AQP4(astro)·MBP(oligo)는 late-pseudotime module(m5/m2/m7), cell division/progenitor gene(TOP2A/NR2F1/NFIC)은 early(m10/m6/m3)(Figure 4C, S5F).
- 세 program이 cycling에서 분기: (1) ASCL1⁺(m3/m8)→EOMES⁺ nIPC, (2) HES4⁺(m6)→astrocyte/ependymal, (3) ASCL1⁺/OLIG1⁺(m12/m1/m4)→astro+oligo 두 endpoint(Figure 4F–4G).
- mGPC가 astroglia(GFAP/HOPX/EGFR/ASCL1)와 oligodendrocyte progenitor(OLIG2/PDGFRA) marker 동시 발현 → 공통 multipotent glial progenitor 가설. IHC로 ASCL1/OLIG2/EGFR가 SVZ/IFL/oSVZ/OFL/SP에서 colocalize(Figure 4I, S7A–S7B); SPARCL1/PDGFRA colocalize(Figure 4K).
- module GO: m6 "cation/metal ion binding"(astrocyte metal homeostasis), m5(FOXJ1⁺) dynein/microtubule(CSF 순환). IHC로 TFAP2C(m6)=VZ/SVZ, PBXIP1(m2)=VZ RG→CP astrocyte, CRYAB(m9)=tRG VZ(Figure S6).

### Dataset 5 — Astrocyte precursor heterogeneity (A1-HES vs A2-OLIG)

- astrocyte module(m2/m13/m14; AQP4/TNC/ALDH2/APOE)이 상호 연결되나 differential motif enrichment로 두 갈래 분리(Figure 5A–5B): m13 enhancer=ASCL1/NHLH1(bHLH) motif, m14=SOX21 motif.
- bHLH OLIG1 expression이 ASCL1/NHLH1 accessibility와 상관(Spearman $\rho=0.34$, $0.36$); SOX21은 cortical organoid astrocyte maturation 조절자로 기존 nominate(Trevino et al. 2020).
- Louvain 재클러스터링으로 A1-HES(HES4/CAV2↑)와 A2-OLIG(SPARCL1/ID3/IGFBP7↑) 두 astrocyte precursor 정의(Figure 5C–5D, Table S5, S8C).
- 독립 dataset(Bhaduri et al. 2020)에서도 두 class의 gene set이 distinct population에 발현되며 cortical area 차이로는 설명 안 됨(Figure 5E–5F) → primate-specific interlaminar/protoplasmic/fibrous astrocyte 같은 adult subtype 대응 가능성(Hodge 2019, Oberheim 2009).

### Dataset 6 — Chromatin state links GPCs to lineage in cycling cells

- glial-centric module과 cell-cycle signature가 강하게 연관(Figure 6A; Pearson $r=0.89$, $0.91$).
- 13,378 glial scATAC cell의 pseudobulk를 module-derived manifold에 projection: cluster10(mGPC)→ASCL1⁺/OLIG2⁺ astro 구역, cluster9(late RG)→ependymal+HES4⁺ astro endpoint(Figure 6B). RNA에서 명확한 cycling cluster는 ATAC에서 세 distinct branch(A/B/C)로 분할(Figure 6C).
- 세 branch 모두 GPC chromatin activity에 enrich, top GPC가 bHLH(BHLHE40/OLIG1/OLIG2/NEUROD6/NEUROD)(Figure 6D–6E). branch별 chromatin이 이미 differentiated state의 signature를 가짐 → "cycling progenitor가 future fate로 epigenetic priming" 가설(Figure 6F–6G).

### Dataset 7 — Deep-learning prioritization of ASD noncoding *de novo* mutations

- An et al. 2018, Simons Simplex Collection 1,902 family, 200,000+ noncoding *de novo* mutation(Table S6).
- **naive peak overlap**: cell-type-specific peak에 ASD mutation enrichment 없음(GluN6 OR=1.02, Fisher $p=1.0$; Figure S8F).
- **BPNet**: cluster별 CNN 학습(5-fold CV, GluN6 mean Spearman $\rho=0.58$; Figure S8H, Table S6). high-effect-size mutation의 case-vs-control enrichment 계산:
  - early RG에서 최고 enrichment(OR=1.909, Fisher $p<0.05$; Figure 7B, Table S6). robust to threshold(Figures S8I–S8J).
  - GluN2/3/4/6/9 >1.2-fold enrichment(Gandal 2018, Li 2018a, Parikshak 2013 등과 일치).
  - control(human fetal heart enhancer로 학습한 BPNet 또는 naive fetal heart overlap)은 enrichment 없음(OR=1.01/0.97, p=1.0) → 효과가 disease-relevant cell state model에 특이.
- high-effect-size mutation 인근 gene이 SFARI DB에 1.4-fold enrich(case $n=24$ vs control $n=17$; Figure 7D). 자주 disrupt되는 motif=CTCF, NRF1(GABRB1 조절), E-box/bHLH(ASCL1/NEUROD6), homeobox(PAX5)(Figure 7E, Table S6).
- **사례**: (1) NFIA intron의 case mutation이 GluN6 BPNet에서 NFIA motif disrupt → NFIA auto-regulatory feedback 교란 가능(Figure 7F, S8M; NFIA LOF은 ASD 연관 Iossifov 2014). (2) nIPC에서 NPY TSS 90 kb upstream intergenic enhancer의 mutation이 CTCF binding site/chromatin loop anchor disrupt(Figure 7G, S8N; NPY receptor deletion ASD 연관 Ramanathan 2004).

### 전체 결과 요약

- 반복 패턴: chromatin accessibility를 같은 developmental trajectory 위에 놓으면 lineage commitment에 앞선 regulatory priming(early active chromatin, cycling cell의 branch-specific chromatin)이 드러난다.
- 가장 결정적 claim: ASD noncoding *de novo* variation은 peak annotation이 아니라 cell-type-specific base-pair-resolution model로만 enrichment·후보화가 가능하며, early RG·deep-layer GluN cluster에 집중된다.
- `해석:` 핵심은 strong association + predictive disruption score다. perturbation 기반 causal 검증은 본 논문에 없다(저자도 §Limitations에서 인정).

## Figures

### Figure 1 — A single-cell epigenomic atlas of the human cerebral cortex

#### 패널별 설명
- A: time·profiling method·cell type schematic(PCW16/20/21/24, scATAC-seq + scRNA-seq, layer 모식).
- B: SOX9/CTIP2 IHC(CP/SP/OFL/oSVZ/IFL/SVZ/VZ, PCW17). C: GFAP/KI67/PPP1R17 multimodal IHC(PCW17). scale bar 500 µm(B,C), 100 µm(inset).
- D: gene expression(좌)·peak accessibility(우) UMAP, time으로 색.
- E: SOX9/EOMES/NEUROD2/DLX2의 gene expression·gene activity·TF motif activity 3행 비교.
- F: cluster별 색의 scRNA(57,868 cell)·scATAC(31,304 cell) UMAP. G: scRNA cluster별 marker gene expression dotplot. H: scATAC cluster별 marker gene activity dotplot.

#### 본문에서 강조한 비교
- 세 metric(expression/activity/motif)이 같은 corticogenesis TF(SOX9/EOMES/NEUROD2/DLX2)에서 ascribed role(RG/IPC/GluN/IN)과 일치(Figure 1E). atlas 규모(57,868 + 31,304)와 657,930 peak이 본문 도입 수치.

#### 해석 시 주의점
- B/C는 PCW17 IHC(scRNA/scATAC sample은 PCW16/20/21/24) — IHC tissue와 sequencing sample이 동일 PCW가 아님에 주의.

### Figure 2 — Integrative and multiomic gene regulatory dynamics

#### 패널별 설명
- A: singleome 생성·CCA 통합 schematic. B: ATAC→RNA, RNA→ATAC matched cell UMAP. C: 64,878 link의 ATAC signal·gene expression heatmap(200 pseudobulk, k-means $k=20$, 10,000 row 표시).
- D: gene activity–RNA 상관 vs linked enhancer 수 산점도(LM $P<2.2\times10^{-16}$), GPC(185) 정의. E: GPC GO enrichment(transcription regulator/DNA-binding TF activity).
- F: multiome 생성 schematic. G: multiome scRNA/scATAC cluster UMAP(8,981 cell). H: singleome vs multiome link Venn(36,193 / 40,181 / 23,849). I: GPC 상관 singleome vs multiome 산점도($r=0.62$, $P<2.2\times10^{-16}$).

#### 본문에서 강조한 비교
- D의 "enhancer 수↑ → 상관↑" 추세가 GPC 정의 근거. H/I가 singleome 추론의 multiome 교차검증(53% 직접 확인, $r=0.62$).

#### 해석 시 주의점
- C heatmap은 시각화를 위해 10,000 row만 random sampling(전체 64,878 link 아님). 상관은 association이며 causal link 아님.

### Figure 3 — Molecular signatures of cortical glutamatergic neurons

#### 패널별 설명
- A: GluN trajectory 강조 UMAP. B: ATAC로 transfer한 pseudotime UMAP. C: 13,989 link의 CRE accessibility·expression heatmap(363 pseudobulk, $k=5$). D: 5 interaction cluster의 gene set GO. E: cluster별 TF motif enrichment(odds ratio·p). F: 31 dynamic TF × 24 motif cluster의 expression·motif activity heatmap(sequential wave). G: motif synergy(상삼각)·correlation(하삼각). H: motif cluster activity vs gene expression 상관. I: gene expression pseudotime vs mean motif synergy 산점도.

#### 본문에서 강조한 비교
- F의 PAX6→SOX/GLI/ASCL1→EOMES/NFI/NEUROD1→NEUROD2/BHLHE22/MEF2C wave. I에서 early TF 높은 synergy, late TF(특히 MEF2C) 낮은 synergy → 후기 독립성.

#### 해석 시 주의점
- pseudotime 축은 wall-clock 아님(저자도 명시). motif activity는 chromVAR류 추론값.

### Figure 4 — Regulatory logic of glial cell specification

#### 패널별 설명
- A: 12,632 RNA cell의 fuzzy c-means 재클러스터링·재투영(점=50-cell pseudobulk). B: 14 module × pseudobulk expression heatmap(cluster·sample·pseudotime annotate). C: 선택 module gene(TOP2A/NFIC/NR2F1/LMO2/FOXJ1/AQP4/MBP) expression. D: module gene UMAP(m6/m8/m5/m14). E: module centroid connectivity(Jaccard>0.2). F–H,J: 선택 module의 membership·expression(ASCL1/HES4/OLIG1; EOMES/AQP4/MBP; ASCL1/OLIG1/EGFR; PDGFRA/SPARCL1). I,K: ASCL1/OLIG1/EGFR 및 SPARCL1/PDGFRA IHC(PCW21, SVZ/IFL/oSVZ/OFL/SP), scale 50 µm.

#### 본문에서 강조한 비교
- F–G에서 cycling cluster로부터 ASCL1⁺(→EOMES), HES4⁺(→astro/ependymal), ASCL1⁺/OLIG1⁺(→astro+oligo 양 endpoint) 세 program 분기. I/K IHC가 mGPC 공통 전구체 colocalization 근거.

#### 해석 시 주의점
- fuzzy(soft) clustering이라 cell이 여러 module에 부분 소속 — module 경계가 hard 아님.

### Figure 5 — Astrocyte precursor heterogeneity

#### 패널별 설명
- A: AQP4/TNC/ALDH2/APOE module membership·expression. B: m13 vs m14 enhancer의 relative motif enrichment(NHLH1/ASCL1/KLF5 vs SOX21). C: glial pseudobulk Louvain 재클러스터링(A1-HES, A2-OLIG 표시). D: A1-HES vs A2-OLIG differential expression(DESeq2, BH FDR<1e-20; C16orf89/TEC/CAV2/WNT11/SOX3/HES4 vs IGFBP7/ID3/OLIG1/SPARCL1/HAS2/ETV4). E: 독립 fetal scRNA(Bhaduri 2020) UMAP, cortical area로 색. F: m13/m2 및 top 200 DEG의 mean scaled expression.

#### 본문에서 강조한 비교
- B의 OLIG1(bHLH) vs SOX21 motif accessibility가 두 astrocyte precursor 구분 축. E/F가 두 class가 cortical area 차이가 아님을 독립 dataset에서 확인.

#### 해석 시 주의점
- adult subtype(protoplasmic/fibrous/interlaminar) 대응은 저자의 speculation(`해석:` 수준 — 직접 검증 아님).

### Figure 6 — Chromatin state links GPCs to cell fates

#### 패널별 설명
- A: cell-cycle signature(MSigDB)와 module expression Pearson 상관 UMAP. B: 1,267 ATAC pseudobulk를 fuzzy clustering 공간에 projection schematic + 결과. C: cycling 구역으로의 chromatin projection(branch A/B/C). D: branch별 top 50 uniquely active gene heatmap + GPC 표시(K-S test: A 1.6e-13, B 1.8e-1, C 5.1e-15). E: branch별 GPC motif·expression dynamics(HES1/TFAP2C/RFX4/GLI3/OLIG1/OLIG2/NEUROD6/NEUROD4/EOMES/NHLH1). F: differential GPC만으로 branch 재투영. G: multiome scRNA/scATAC를 fuzzy 공간에 projection.

#### 본문에서 강조한 비교
- D의 K-S p값이 branch A/C의 GPC enrichment 유의성(B는 비유의). F에서 GPC chromatin만으로도 branch가 mature state 방향으로 이동 vs random gene set은 manifold 중심으로(Figure S8E) → cycling cell의 epigenetic priming 핵심 근거.

#### 해석 시 주의점
- branch는 ATAC pseudobulk projection 기반 — RNA에는 distinct cycling cluster가 안 보였다는 점(Figure 6C 본문)과 함께 해석.

### Figure 7 — Disease association of gene regulatory elements

#### 패널별 설명
- A: mutation prioritization pipeline schematic(250,000+ cluster ATAC peak + 2,114 bp context → CNN(dilation/residual) → profile/count 예측 → SSC 1,902 family de novo variant → threshold scoring → case/control).
- B: cluster별 ASD de novo mutation enrichment UMAP(early RG·late RG·nIPC·IN2/3/4 high).
- C: prioritization method 비교 bar(naive vs scATAC-trained BPNet vs fetal heart; * Fisher OR=1.909, p=0.004).
- D: key mutation 100 kb 내 SFARI gene·all gene count(case vs control; 1.4-fold).
- E: case에서 control 대비 자주 disrupt되는 motif family(E-box/CACGTG, CTCF, POU, SOX1, NRF1 등).
- F: NFIA case mutation 예(GluN6, NFIA motif, ref/alt importance·predicted count·cluster track). G: NPY case mutation 예(early RG, CTCF motif).

#### 본문에서 강조한 비교
- C가 본 논문 핵심 method claim 시각화(naive overlap OR≈1.0 vs BPNet OR=1.909, fetal-heart control 무효). F/G가 mechanism 예시.

#### 해석 시 주의점
- enrichment는 high-effect-size predicted mutation에 한정(threshold 의존, robust 주장은 S8I–S8J). prioritized mutation의 deleterious nature는 분자 검증 안 됨(저자 §Limitations).

## Tables

본문에 inline 정식 Table(번호 매겨진 표)은 없다. 모든 표는 supplementary로, 본문이 참조한 것:
- **Table S1**: cell cluster·marker gene(Figure 1 annotation 근거).
- **Table S2**: CRE-gene linkage, multiome QC, link 통계(64,878 / 40,181 / 23,849).
- **Table S3**: GluN trajectory 5-cluster link, migrating neuron DEG.
- **Table S4**: glial fuzzy c-means 14 module·membership.
- **Table S5**: A1-HES vs A2-OLIG differential expression.
- **Table S6**: ASD de novo mutation, BPNet enrichment, disrupted motif.

`미제공:` 위 supplementary table 파일은 로컬 `sources/`에 없어 cell 단위 수치는 본문 인용 범위까지만 단정.

## Supplementary Information

- 본문이 참조한 supplementary figure: S1(IHC/marker 추가), S2(prior dataset projection·time bias), S3(QC·multiome processing·3D interaction·CCA matching), S4(GluN trajectory·pseudotime·adult cortex projection·migrating neuron), S5(glial module 추가·cell-cycle), S6(glial module IHC: TFAP2C/PBXIP1/CRYAB), S7(mGPC colocalization IHC), S8(BPNet CV·naive overlap·threshold robustness·conservation·NFIA/NPY 예시).
- `미제공:` STAR Methods 본문(cell dissociation, library, scRNA/scATAC/multiome processing, data analysis, IHC), supplementary figure/table 파일 모두 로컬에 없음. 정밀 재현 시 online supplemental(DOI 동일) 확보 필요.
- **데이터/코드**: GEO `GSE162170`(fetal human cortex 10x multiome + singleome) — 본 프로젝트 Dataset 3 원 출처. 코드 repo: `GreenleafLab/brain_comp`, `GreenleafLab/Brain_ASD`(`검토필요:` 정확한 figure 재현 범위는 STAR Methods Data/code availability 확인 필요).

## 분석 자체에 대한 메모

- `질문:` GluN trajectory의 TF wave(PAX6→…→MEF2C)와 motif synergy 감소를 우리 chromatin–transcription lag framework의 "activation lag" 가설과 어떻게 정렬할까? 본 논문은 lag를 명시적으로 정량화하지 않고 sequential motif activation으로만 본다 — pseudotime 축에서 motif accessibility와 target expression의 시차를 직접 측정한 figure는 없음.
- `검토필요:` BPNet의 정확한 architecture(layer 수, receptive field), train/test chromosome split, effect-size threshold 정의는 STAR Methods 확인 필요. variant scoring을 우리 HSPC multiome에 옮기려면 cluster별 peak count·model 재학습 비용 추정 필요.
- `검토필요:` GSE162170에서 multiome(PCW21, 8,981 cell)과 singleome을 어떻게 구분해 다운로드하는지(파일 단위) 확인 필요 — 후속 velocity 논문은 multiome subset을 쓴다.
- `미제공:` cell cycle phase를 covariate로 통제한 lag/link 분석은 본문에 없음. 본 프로젝트 CLAUDE.md §방법론 주의 2(cell cycle confound)와 직결 — Figure 6은 오히려 cycling cell의 chromatin priming을 *결과*로 다룬다.
