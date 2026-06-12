# Martin et al., 2023 — HSPC Chromatin Accessibility Dynamics — core

> 근거: `sources/martin-2023-hspc-chromatin.pdf` (Stem Cells 2023, 41(5):520-539, 20 pages) 및 `sources/sxad022_suppl_supplementary_materials.pdf`. Source grounding 원칙은 `skills/source-grounding/SKILL.md`를 따른다. `해석:` / `외부 맥락:` / `추정:` / `미제공:` / `질문:` / `검토필요:` 표기를 동일하게 사용한다.
> 자료유형: **primary research article**. PDF 1페이지 header가 "Original Research"이고, Results 섹션·실험 Figure·Table·CRISPRi perturbation을 직접 수행한다. 이전 `document_type=review` 기록은 오기였으며 `paper`로 정정함.

## Executive Summary

- **무엇**: mouse hematopoiesis에서 13개 functionally defined cell type(HSC→progenitor→mature)의 chromatin accessibility를 ATAC-seq로 mapping해, 분화 동안 lineage-primed cis-regulatory element(CRE)의 운명을 추적하고 HSC-unique CRE를 CRISPRi로 기능 검증한 연구.
- **모델 / 방법**: bulk ATAC-seq (FACS-purified 13 cell type, replicate $n=2$) → IDR peak calling → master peak-list 92,842 peaks → chromVAR 정규화 + PCA/UMAP/hierarchical clustering → HOMER motif·GREAT GO annotation → dCas9-KRAB CRISPRi mouse로 CRE→유전자 functional link.
- **핵심 결과**:
  - ① HSC가 모든 progeny보다 ATAC peak 수(70,731)와 cumulative signal이 가장 높음 (Fig 1B,C; Table 1) → global chromatin이 가장 열린 상태.
  - ② 13 cell type이 erythromyeloid vs lymphoid 두 cluster로 분리, HSC·MPP는 erythromyeloid 쪽에 association (Fig 4 PCA/UMAP/hierarchical).
  - ③ lineage-primed CRE는 분화 중 대부분 닫히고, 각 lineage에서 HSC-primed peak의 25% 미만만 unipotent 단계까지 accessibility 유지 (Fig 6C).
  - ④ HSC-unique peak 3,026개(92.7% non-promoter)는 erythropoiesis 조절요소(ELF3/CTCFL/NF-E2/Runx motif, "definitive erythrocyte differentiation" GO)에 enrich (Fig 7A-G).
  - ⑤ CRISPRi: CD81 promoter silencing으로 proof-of-concept 확립, CD115 promoter·enhancer 둘 다 표적 시 CD115+ 세포 빈도 유의 감소; CD11b는 promoter만 유의, putative enhancer는 무효 (Fig 7I-L).
- **우리 적용**: activation lag 가설의 *생물학적 방향성* 배경 문헌 (chromatin opening이 transcription/계통확정에 선행하는 priming 구조를 직접 제시). use_case: academic-citation, methodology-reference. 다만 paired RNA·시간 단위 lag 정량은 없음.
- **심층**: 한계·재현 ROI는 `martin-2023-hspc-chromatin_lens-academic.md` / `martin-2023-hspc-chromatin_lens-industry.md` / `martin-2023-hspc-chromatin_methodology-brief.md` 참고.

## Identity

- **title**: Dynamics of Chromatin Accessibility During Hematopoietic Stem Cell Differentiation Into Progressively Lineage-Committed Progeny
- **authors**: Martin EW, Rodriguez y Baena A, Reggiardo RE, Worthington AK, Mattingly CS, Poscablo DM, Krietsch J, McManus MT, Carpenter S, Kim DH, Forsberg EC (corresponding)
- **year / venue**: 2023, *Stem Cells* 41(5):520-539 (Oxford University Press). Advance access 2023-03-22.
- **DOI / ID**: 10.1093/stmcls/sxad022 · PMID 36945732 · PMCID PMC10183972
- **citation key**: `martin2023hspcchromatin`
- **affiliation**: Institute for the Biology of Stem Cells, UC Santa Cruz (Forsberg lab); UCSF (McManus).
- **선행 자기인용**: Martin EW, Krietsch J, Reggiardo RE et al. *Epigenetics Chromatin* 2021;14:1-15 (ref 20) — HSC multilineage gene priming 최초 보고. 본 논문은 그 사이 oligopotent 구간으로 확장.

## Background

**문제의 큰 그림.** Hematopoiesis는 multipotent HSC가 epigenetic·transcriptional 변화를 거쳐 lineage-restricted progenitor로 분화하는 과정이다. classical model에서 HSC → MPP → CMP/CLP → unipotent progenitor(MEP/GMP, ProB/ProT) → mature cell(MkP/EP/GM, B/T)로 fate가 점진적으로 제한된다 (Fig 1A). 본 논문은 stem cell biology의 두 미해결 질문을 명시한다: (1) epigenetic identity가 cell type의 lineage potential에 어떻게 기여하는가, (2) chromatin remodeling의 cascade가 이후 fate decision을 어떻게 좌우하는가.

**Priming 개념.** 저자들은 "priming"을 *target gene이 아직 발현되지 않았는데도 그 putative target의 CRE가 미리 열려 있는 chromatin accessibility 상태*로 정의한다. lineage가 결정되기 전에 lineage-specific CRE가 열려 있으면 그 세포는 해당 계통으로 갈 *잠재력(potential)* 을 epigenetic으로 보유한 것이다. Promoter는 Pol II 기구를 모으지만, non-promoter CRE(enhancer)가 cell type-specific transcription에 필수적이며 lineage-determining TF의 binding site로 작동한다.

**이 논문 직전의 공백.** 저자들의 선행 연구(ref 20)는 HSC와 unipotent lineage cell 사이에서만 공유되는 open CRE가 known lineage-specific TF motif에 enrich됨을 보였다(= multilineage gene priming). 그러나 HSC와 unipotent cell *사이에 위치한 oligopotent progenitor*(CMP/CLP/MEP) 구간의 chromatin dynamics는 규명되지 않았다. 본 연구의 가설: "selective HSC-primed lineage-specific CRE가 분화 전 과정에서 계속 accessible하게 유지된다."

**왜 ATAC-seq + CRISPRi인가.** accessibility mapping(상관)만으로는 CRE의 *기능적 인과*를 알 수 없다. 저자들은 functionally defined progenitor 7종을 FACS로 분리해 ATAC-seq를 수행하고(선행 데이터의 HSC + 5 unilineage와 통합해 13종), 후보 CRE를 CRISPRi(dCas9-KRAB)로 silencing해 lineage-specific gene expression과의 인과를 검증했다.

## Methods

> formal task: bulk ATAC-seq의 chromatin accessibility 신호로부터 (a) cell type 간 정량적 peak 차이, (b) 분화 trajectory를 따른 lineage-primed CRE의 유지/소실 dynamics, (c) HSC-unique CRE의 functional necessity를 추정한다.

### 실험·데이터 구조

- **세포 모델**: 8-12주령 C57BL/6 wild-type mouse bone marrow. FACS로 13 cell type 분리 — HSC, MPP, CMP, GMP, GM, MEP, MkP, EP, CLP, ProB, B, ProT, T. 본 연구에서 7 progenitor를 새로 ATAC-seq, 선행(ref 20)의 HSC + 5 unilineage(MkP/EP/GM/B/T)와 통합. FACS gating은 cKit/Lineage/Sca1/Flk2/Slamf1(CD150)/CD34/FcγRII/Il7rα marker 조합으로 정의(Experimental Procedures, p.534-535).
- **ATAC-seq**: Buenrostro et al. (ref 24) 프로토콜. replicate $n=2$. ENCODE ATAC-seq pipeline v1.1.6/1.4.2, mm10, default parameter (v1.4.2: `atac.multimapping=0`, `atac.smooth_win=150`, `atac.enable_idr=true`, `atac.idr_thresh=0.1`). HiSeq2500 100×100 paired-end deep sequencing.
- **CRISPRi mouse**: site-specific integrase로 H11 safe harbor에 CAG-driven dCas9-KRAB(ZNF10) cassette 삽입한 transgenic mouse. 기존 mCherry/Puro CRISPRi mouse(ref 62)와 유사하나 resistance gene 없음.

### 분석 구조

- **Peak calling**: 각 cell type의 replicate 2개를 IDR(irreproducible discovery rate, ref 29)로 reproducible peak 산출.
- **Master peak-list**: 13 cell type의 IDR peak을 concatenate·sort 후 chromVAR(ref 44)의 `filterPeaks`로 nonoverlapping 필터링 → **92,842 peaks**. GC bias 보정 후 fragment count.
- **정규화·차원축소**: chromVAR deviation을 $\log(1+x)$ scale, center, 분산 상위(above-median coefficient of variation) peak만 남겨 PCA(`prcomp`) → UMAP(`uwot`) → hierarchical clustering(correlation). plot은 `ggplot2`.
- **차등 peak 비교**: `mergePeaks` (`-d given`, `-venn`)로 cell type 쌍 간 gained/lost peak 산출. KLS(=HSC/MPP 통합) 대비 CMP/CLP, MEP 대비 MkP/EP 등 branchpoint별 비교.
- **Annotation**: HOMER `annotatePeaks.pl`로 promoter(±500bp TSS) vs non-promoter 분류, `findMotifsGenome.pl`로 motif enrichment, `makeTagDirectory`+`-hist`로 cumulative signal histogram(±250bp). GREAT(ref 32,33)로 non-promoter peak → target gene → GO term(basal+extension, proximal 2kb up/1kb down, distal 1Mb).
- **HSC-unique peak**: HSC peak을 나머지 12 cell type의 peak에 대해 필터 → HSC에만 있는 3,026 peak.
- **Lineage-primed peak**: HSC와 각 unipotent cell이 *배타적으로* 공유하는 peak(선행 정의) → Supplementary Tables S1-S5. `bedtools intersect`로 intermediate progenitor에서의 유지 여부 정량.
- **CRISPRi readout**: CRISPRi mouse HSPC를 lentivirus(sgRNA)로 transduce, 분화 배지에서 배양 후 표적 유전자의 cell-surface protein을 flow cytometry로 정량(CD81, CD115/Csf1r, CD11b/Itgam). dual-guide vector(ref 63)로 promoter + putative enhancer 동시 표적. 통계 GraphPad Prism 9.

### 핵심 method insight

- 13개 functionally defined cell type을 하나의 master peak-list로 통합해 *분화 축 전체*를 동일 좌표계에서 비교 — branchpoint(CMP/CLP, MkP/EP)별 gained/lost peak를 정량 가능.
- "primed peak"을 HSC와 unipotent cell의 배타 공유 peak으로 조작적 정의 → intermediate progenitor에서 그 peak이 *유지되는지*를 추적해 priming의 *지속성*을 정량화.
- ATAC accessibility(상관)를 CRISPRi(인과)로 연결 — distal CRE까지 native chromatin context에서 기능 검증.

### 이전 방법과의 차이

- 선행 연구(ref 20)는 HSC + unipotent endpoint만 다뤘다. 본 연구는 oligopotent intermediate(CMP/CLP/MEP)를 추가해 분화 *trajectory*를 채웠다.
- 단순 accessibility map을 넘어 *CRISPRi mouse 기반 functional validation*을 결합 — accessibility-only study와의 핵심 차별점.

### Method 한계 (본문 근거)

- bulk ATAC-seq: cell type별 FACS purification에 의존. single-cell이 아니므로 population 내 heterogeneity·intermediate state는 평균화됨.
- `미제공:` peak count·cumulative signal이 input cell 수·library depth에 민감한데, 본문은 "careful quality control of individual and replicate samples"만 언급하고 cell number/depth normalization의 구체 절차를 본문에 수치로 제시하지 않음. `검토필요:` HSC의 "greater accessibility"가 technical covariate를 완전히 통제한 결과인지 supplementary methods 추가 확인 필요.
- replicate $n=2$ — 통계적 검정력이 제한적. HSC 2 sample은 hierarchical clustering에서 인접하지 않은 유일한 쌍(p.535) → HSC replicate variability 존재.
- `미제공:` RNA / transcription readout(paired RNA, multiome)을 직접 측정하지 않음. expression은 외부 GEXC database(ref 31)에서 가져옴 — accessibility-expression 상관이 *같은 세포의 동시 측정*이 아님.

## Results

### Dataset

- **이 연구 (GSE184851)**: mouse BM, 13 cell type, ATAC-seq replicate $n=2$. master peak-list 92,842 peaks.
- **선행 (GSE162949)**: HSC + 5 unilineage(MkP/EP/GM/B/T)의 ATAC-seq (Martin 2021, ref 20). 본 연구에서 통합.
- expression reference: Gene Expression Commons(GEXC, ref 31).

### HSC가 가장 높은 global accessibility

7 progenitor를 FACS 분리 후 ATAC-seq → IDR peak count 순위: **HSC > MPP > lineage-committed progenitor** (Fig 1B). Table 1 수치(IDR peak): HSC 70,731, MPP 63,369, CLP 47,054, CMP 46,431, GMP 42,447, GM 30,529, MEP 50,483, EP 38,007, MkP 47,363, ProB 46,790, **B 70,358**, ProT 61,141, T 51,832 (master 92,842). cumulative signal(HOMER histogram)도 HSC가 모든 progenitor보다 압도적으로 높음 (Fig 1C). → epigenetic stem cell priming 가설과 일관. (`해석:` B cell의 peak 수가 HSC에 근접(70,358)한 점은 본문이 강조하지 않음 — 단순 "HSC가 progenitor보다 높다"는 progenitor 한정 진술.)

### Cell type-specific gene과 accessibility 상관

GEXC로 각 progenitor에서 specifically expressed gene 목록 생성 → 그 gene의 promoter에 overlap하는 unique peak에서 cell type-specific read accumulation 관찰, 다른 cell type에서는 minimal signal (Fig 1D,E). → accessibility mapping이 lineage-specific 신호를 해상.

### Lymphoid commitment가 myelopoiesis보다 더 광범위한 remodeling

KLS(HSC+MPP) 대비 CMP/CLP의 gained/lost peak 비교(Fig 2). CLP가 CMP보다 총 altered peak(13,015 vs 12,277)·promoter peak(1,626 vs 1,054) 모두 많음(Chi-square: 전체 $p<.001$, promoter $p<.0001$; non-promoter는 ns $p=0.42$). CMP gained peak은 "Negative Regulation of B-cell Activation" GO + Gata motif enrich; CLP gained peak은 immune response GO + IRF8/SpiB motif. → 첫 branchpoint에서 lymphoid 분화가 myeloid보다 chromatin remodeling(특히 promoter)을 더 많이 요구.

### Megakaryocyte-Erythroid branch (MEP → MkP/EP)

MEP 대비 MkP/EP의 altered peak ~18,000개(Fig 3). MkP는 ~77%가 gained peak, EP는 ~61%가 lost peak(Fig 3C) — 방향이 반대. MkP gained는 megakaryopoiesis/platelet phenotype + Etv2/Fli1/ETS1 motif; EP gained는 erythrocyte morphology/hemoglobin phenotype + Gata1/2/4 motif. 예시: *Alox5ap*는 MEP에서 MkP-specific enhancer가 미리 열려 priming, MkP에서 고발현(Fig 3J,K).

### Erythromyeloid vs Lymphoid 두 cluster

PCA·UMAP·hierarchical clustering 모두 13 cell type을 erythromyeloid와 lymphoid 두 cluster로 분리(Fig 4). HSC·MPP는 erythromyeloid quadrant에 위치. sub-cluster: MkP-CMP, MEP-EP, ProB-B-CLP, ProT-T. replicate 일치도 높음(HSC 2 sample 제외 — 유일하게 인접하지 않음). → HSC/MPP의 erythromyeloid 편향은 HSC가 적혈구를 우세 생산한다는 선행 functional 결과(ref 6)와 일관.

### Known locus 검증: β-globin, Rag

β-globin cluster(Fig 5A): EP-selective HS3/βminor promoter accessibility, LCR HS site에서 erythroid-lineage 특이 accessibility. Rag locus(Fig 5C): Rag1/Rag2 promoter·D3 CRE가 lymphoid(CLP/ProB/B/ProT/T) 특이 accessible, ASE는 ProT 특이. → 잘 알려진 CRE를 정확히 재현, dataset 신뢰성 확인.

### Lineage priming의 선택적 유지

HSC-primed lineage-specific peak(Supplementary Tables S1-S5)이 intermediate progenitor에서 유지되는지 추적(Fig 6). 모든 progenitor가 5 lineage primed peak을 일부 포함하나 분포는 lineage-bias(erythromyeloid progenitor는 EP/MkP-primed에 enrich, lymphoid progenitor는 B/T-primed에 enrich; Chi-square). 핵심 정량: **HSC-primed peak의 25% 미만만** 분화 trajectory 끝까지 accessibility 유지(lineage별 17% MkP, 11% EP, 13% GM, 12% B, 26% T; Fig 6C, Supplementary Table S6). 약 10%가 promoter. → priming은 광범위하게 시작되나 대부분 닫히고, 소수의 persistent CRE만 fate를 강화.

### HSC-unique peak = erythropoiesis-primed

HSC-unique peak **3,026개**, 92.7%(2,805)가 non-promoter(Fig 7A,B). de novo motif: ELF3($1e{-}168$, 62.4% target), CTCFL, NF-E2, RUNX 상위(Fig 7C). GREAT top GO "definitive erythrocyte differentiation"(Fig 7D) — 14 gene이 link, 그중 *Ncor1, Tgfbr3, Zfpm1(FOG-1), Smarca4* 4개는 erythropoiesis에 known role. 예시 CRE: Ncor1-CRE(NF-E2+Foxo1 motif), Zfpm1-CRE(ELF3), Tgfbr3-CRE(CTCFL+Foxo1)(Fig 7E-G). → HSC-unique CRE는 self-renewal/multilineage보다 *erythroid fate priming*에 강하게 치우침.

### CRISPRi functional validation

- **Proof-of-concept (Fig 7I)**: CD81 promoter 표적 sgRNA로 HSPC에서 CD81 cell-surface 발현 유의 감소(scrambled 대비, $p<.01$, $n=4$). → CRISPRi mouse HSPC에서 효율적·선택적 silencing 작동 확인.
- **분화 후 distal CRE 검증 (Fig 7K,L)**: dual-guide로 promoter + putative enhancer 동시 표적, 5일 분화 후 측정.
  - **CD115(Csf1r)**: promoter 또는 putative CRE 표적 *둘 다* CD115+ 세포 빈도 유의 감소($p<.0001$). → 이 distal CRE는 CD115 발현에 필수.
  - **CD11b(Itgam)**: promoter 표적은 CD11b+ 빈도 유의 감소($p<.001$)하나, putative enhancer 표적은 ns(무효). → 모든 putative CRE가 기능적이지 않음을 보여주는 음성 대조.

### 전체 결과 요약

분화는 highly dynamic하며 HSC가 가장 열린 chromatin을 가진다. 두 major branchpoint(CMP/CLP, MkP/EP)에서 차등 priming이 뚜렷하고, lymphoid 분화가 promoter remodeling을 더 요구한다. HSC priming의 대부분은 분화 중 닫히고 소수 persistent CRE만 fate를 강화한다. HSC-unique CRE는 erythroid 편향. CRISPRi로 ATAC 기반 CRE 후보를 기능 검증 가능함을 입증(CD115 양성, CD11b enhancer 음성).

## Figures

### Figure 1 — ATAC-seq map 개관, HSC accessibility 최고

#### 패널별 설명
- **A**: 분화 계통도. HSC→MPP→{CMP,CLP}→{MEP,GMP / ProB,ProT}→{MkP,EP,GM / B,T}. 본 연구 새 데이터(7 progenitor)와 선행 데이터(HSC,MkP,EP,GM,B,T) 통합 표시.
- **B**: cell type별 IDR peak 수 막대. HSC 최다, MPP 다음.
- **C**: peak center ±250bp cumulative ATAC signal. HSC가 압도적 peak.
- **D**: HSC/MEP/ProB/ProT 4종의 cell type-specific expression pattern(GEXC 색상). 어느 cell type에서 active한지.
- **E**: 각 cell type의 specifically expressed gene promoter에서의 average signal — cell type-specific accumulation(HSC 34, MEP 16, ProB 29, ProT 12 promoter peaks).

#### 본문에서 강조한 비교
HSC가 peak 수와 cumulative signal 양쪽에서 모든 progenitor를 능가 → epigenetic stem cell priming.

#### 해석 시 주의점
`검토필요:` peak 수는 input cell·depth 민감 지표. 정규화 절차의 본문 수치 부족(Method 한계 참고).

### Figure 2 — 첫 branchpoint(CMP vs CLP) peak dynamics

#### 패널별 설명
- **A**: KLS(HSC/MPP) 대비 CMP/CLP gained·lost peak Venn schematic.
- **B-D**: altered peak 총수(B), promoter(C), non-promoter(D). CLP > CMP (전체 $p<.001$, promoter $p<.0001$, non-promoter ns $p=0.42$).
- **E-H**: gained/lost peak의 GREAT GO + HOMER motif. CMP gained(E)=Gata motif/B-cell neg reg; CLP gained(F)=IRF8/SpiB/immune; CMP lost(G)=PU.1/ETS; CLP lost(H)=CTCF/Gata.

#### 본문에서 강조한 비교
lymphoid(CLP) 분화가 myeloid(CMP)보다 더 많은 chromatin remodeling, 특히 promoter 영역.

#### 해석 시 주의점
de novo activation + silencing의 조합으로 fate 전환 — gained와 lost를 함께 봐야 함.

### Figure 3 — MkP vs EP branch

#### 패널별 설명
- **A,B**: MEP→MkP/EP schematic + 비교 Venn.
- **C-E**: altered peak(C), promoter(D), non-promoter(E). MkP ~77% gained, EP ~61% lost.
- **F,G**: MkP gained(megakaryopoiesis phenotype, Etv2/Fli1)·EP gained(erythrocyte, Gata).
- **H,I**: motif table.
- **J,K**: *Alox5ap* locus track + 발현. MEP에서 MkP-specific enhancer priming.

#### 본문에서 강조한 비교
같은 모세포(MEP)에서 두 자손이 반대 방향(gain vs loss)으로 remodeling.

#### 해석 시 주의점
`해석:` "MEP가 EP 쪽으로 biased" 가능성 — EP-primed peak이 MEP signal의 대부분을 차지(본문 Discussion).

### Figure 4 — 두 cluster(erythromyeloid / lymphoid)

#### 패널별 설명
- **A**: PCA. PC1 0.223, PC2 0.154. erythromyeloid vs lymphoid 사분면 분리. HSC/MPP는 erythromyeloid.
- **B**: UMAP. 동일 분리.
- **C**: hierarchical clustering heatmap. 2 cluster + 4 sub-cluster. replicate 인접(HSC 2 sample 제외).

#### 본문에서 강조한 비교
HSC/MPP의 erythromyeloid 편향 = 적혈구 우세 생산(ref 6)의 epigenetic 근거.

#### 해석 시 주의점
HSC 2 replicate가 hierarchical clustering에서 분리됨(MPP가 사이에 끼어듦) → HSC accessibility의 sample variability(p.535).

### Figure 5 — 알려진 locus 검증 (β-globin, Rag)

#### 패널별 설명
- **A**: β-globin cluster track. LCR HS site, βmajor/βminor, EP-selective accessibility.
- **B**: Rag1/Rag2 GEXC expression(lymphoid 특이).
- **C**: Rag locus track. promoter·D3·Erag·ASE의 cell type별 accessibility(IDR peak box).

#### 본문에서 강조한 비교
잘 알려진 erythroid·lymphoid CRE를 dataset이 정확히 재현 → novel CRE 발굴 신뢰 근거.

#### 해석 시 주의점
βglobin HS2의 GMP/MkP/ProT 비예상 accessibility는 "permissive" chromatin state 가능성으로 해석(본문).

### Figure 6 — primed CRE의 선택적 유지

#### 패널별 설명
- **A**: 5 lineage primed peak의 cell type별 cumulative signal histogram.
- **B**: progenitor별 primed peak 분포(% of total). lineage-bias enrichment(Chi-square 유의).
- **C**: HSC-primed peak이 분화 trajectory 따라 유지되는지 heatmap. 17%(MkP)/11%(EP)/13%(GM)/12%(B)/26%(T)만 유지.
- **D,E**: *Fcnb*(GM), *Wnt8b*(T) primed CRE 예시 track.

#### 본문에서 강조한 비교
priming은 광범위하나 대부분 닫힘 — persistent CRE는 25% 미만.

#### 해석 시 주의점
`해석:` CLP가 HSC/MPP와 priming 분포가 유의하게 다르지 않음(Fig 6B, Chi-square $p>.01$) → CLP의 일부 priming은 in vivo로 구현되지 않는 "inherited" priming일 수 있다(본문 Discussion, ref 69 in vitro reignite 가능).

### Figure 7 — HSC-unique CRE와 CRISPRi 검증

#### 패널별 설명
- **A,B**: HSC-unique peak Venn + 표(3,026 unique, 92.7% non-promoter).
- **C**: de novo motif(ELF3, CTCFL, NF-E2, RUNX 상위).
- **D**: GREAT GO("definitive erythrocyte differentiation" top).
- **E-G**: Ncor1/Zfpm1/Tgfbr3 CRE track + motif.
- **H**: CRISPRi mouse 실험 schematic(dCas9-KRAB@H11, isolate→transduce→culture→flow).
- **I**: CD81 promoter silencing proof-of-concept($p<.01$).
- **J**: CD115/CD11b locus + sgRNA 위치.
- **K**: CD115 promoter·enhancer 둘 다 유의 감소($p<.0001$).
- **L**: CD11b promoter 유의($p<.001$), enhancer ns.

#### 본문에서 강조한 비교
ATAC 기반 CRE 후보를 CRISPRi로 기능 검증 — distal enhancer까지(CD115 enhancer 양성). CD11b enhancer 음성으로 모든 후보가 기능적이지 않음을 보임.

#### 해석 시 주의점
`해석:` CD115 enhancer 양성은 강하나, n과 effect size(fold change)는 dot plot 수준 — 정확한 수치는 본문 figure caption에 막대/점으로만 제시.

## Tables

### Table 1 — cell type별 peak count·분포

13 cell type + master peak-list의 ATAC peak / promoter peak(±500bp TSS) / non-promoter peak(coding, intron, intergenic 세분) 수. 주요 수치: master 92,842; HSC 70,731(promoter 27,973); MPP 63,369; B 70,358. → HSC가 progenitor 중 최다 peak이라는 Fig 1B 주장을 수치로 뒷받침. non-promoter가 대부분(HSC 42,758 non-promoter vs 27,973 promoter)이라는 점도 enhancer-중심 분석의 근거.

## Supplementary Information

> `sources/sxad022_suppl_supplementary_materials.pdf`

- **Supplementary Tables S1-S5**: 각 unipotent cell(MkP/EP/GM/B/T)과 HSC가 배타적으로 공유하는 "exclusively primed peak" 목록(chr 위치, peak_id, scaled IDR, strand). Fig 6의 lineage-primed peak 정의의 source.
- **Supplementary Table S6**: 분화 끝까지 accessibility를 유지한 primed peak 목록(어느 S1-S5에서 왔는지 peak_id로 표시). Fig 6C의 source.
- **Supplementary Figure 1**: MEP에서 lost된 peak의 GREAT GO + HOMER motif. (A) MkP lost peak → erythropoiesis phenotype + Gata1/Gata:SCL motif. (B) EP lost peak → immune modulation/proliferation + chromatin remodeling motif. → MkP로 갈수록 erythropoiesis가 꺼진다는 Fig 3 해석 보강.
- **데이터/코드**: GEO GSE184851(이 연구), GSE162949(선행). UCSC genome browser custom track: `genome.ucsc.edu/s/ewmartin/atac_bw_mean_allpeaks`. ENCODE ATAC-seq pipeline, chromVAR, HOMER, GREAT, CRISPOR(sgRNA design)는 모두 public tool.

## 분석 자체에 대한 메모

- `질문:` 이 연구의 mouse HSC-unique peak / lineage-primed CRE 좌표를 우리 Human HSPC 10x Multiome(GSE209878)의 ATAC peak과 ortholog 좌표 수준에서 mapping하면, baseline epigenomic feature(primed CRE) 정의에 직접 쓸 수 있나? mm10→hg38 liftover 손실과 motif 보존 여부 확인 필요.
- `검토필요:` peak count·cumulative signal의 cell-number/depth normalization 절차가 본문 수치로 충분히 기술되지 않음 — "HSC가 가장 열려 있다"를 인용할 때 이 caveat를 함께 표기.
- `미제공:` 같은 세포에서 accessibility-expression 동시 측정(multiome)이 없으므로 chromatin opening과 transcription 사이의 *시간 lag* 정량은 이 논문으로 불가. priming의 방향성 근거로만 사용.
- `질문:` Fig 6C의 "25% 미만 유지"는 우리 activation lag 가설에 흥미로움 — 대부분의 primed CRE가 transcription 없이 닫힌다면, "열렸다가 발현으로 이어지는" CRE의 비율 자체가 lineage·CRE마다 다르다는 뜻. 우리 lag estimate에서 "열렸으나 미발현" CRE를 어떻게 처리할지 정책 필요.
