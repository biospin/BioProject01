# yu-2016-her2-ctc-dynamic — Core Analysis

## Executive Summary

- **무엇**: ER+/HER2− 전이성 유방암 환자의 CTC (circulating tumor cell) 내에서 HER2+ 및 HER2− 세포가 자발적으로 상호전환(interconversion)하는 동적 상태를 규명하고, 이 이질성이 화학요법 내성 및 암 진행에 미치는 역할을 밝힌 전임상·임상 통합 연구.
- **모델 / 방법**: CTC-iChip 미세유체 플랫폼으로 생존 CTC 분리 → FACS 정제 → scRNA-seq / TMT 기반 정량 proteomics / confocal lineage tracing / 55종 약물 스크리닝 / orthotopic mouse xenograft (NSG mice, n=8/조건).
- **핵심 결과**:
  - ① 19명 ER+/HER2− 전이성 유방암 환자 중 16/19명(84%)에서 HER2+ CTC 획득 확인; scRNA-seq bimodal 분포 p=7.5e-6 (n=22)
  - ② HER2− CTCs가 4주 내 HER2+ 딸세포 자발 생성 (Brx-82: 42%, Brx-142: 46%); 역방향 전환 효율 훨씬 낮음(5–11%)
  - ③ HER2+ CTCs — multi-RTK (RTK: receptor tyrosine kinase) pro-growth 상태; HER2− CTCs — Notch/DNA damage 경로 활성 + 화학요법 내성
  - ④ 파클리탁셀 + Notch 저해제(γ-secretase inhibitor) 병용이 파클리탁셀 단독 대비 종양 재발을 유의하게 지연 (Two-way ANOVA p<0.0001, n=8)
- **우리 적용**: HER2 표적 ADC 또는 병용 요법 개발 시 HER2 이질성의 동적 전환을 고려해야 함을 지지하는 academic-citation + BD-opportunity 레퍼런스.
- **심층**: 한계·재현 ROI는 `yu-2016-her2-ctc-dynamic_lens-academic.md` / `yu-2016-her2-ctc-dynamic_lens-industry.md` / `yu-2016-her2-ctc-dynamic_methodology-brief.md` 참고.

---

## Identity

- **Title**: HER2 expression identifies dynamic functional states within circulating breast cancer cells
- **Authors**: Nicole Vincent Jordan, Aditya Bardia, Ben S. Wittner, Cyril Benes, Matteo Ligorio, Yu Zheng, Min Yu, Tilak K. Sundaresan, Joseph A. Licausi, Rushil Desai, Ryan M. O'Keefe, Richard Y. Ebright, Myriam Boukhali, Srinjoy Sil, Maristela L. Onozato, Anthony J. Iafrate, Ravi Kapur, Dennis Sgroi, David T. Ting, Mehmet Toner, Sridhar Ramaswamy, Wilhelm Haas, Shyamala Maheswaran†, Daniel A. Haber†
- **Year**: 2016
- **Venue**: Nature, 537(7618): 102–106
- **DOI**: 10.1038/nature19328
- **Citation key**: jordan2016her2ctc
- **Affiliations**: Massachusetts General Hospital Cancer Center / Harvard Medical School (Department of Medicine, Surgery, Pathology); Center for Bioengineering in Medicine and Shriners Hospital; Howard Hughes Medical Institute
- **Corresponding authors**: Daniel A. Haber (dhaber@mgh.harvard.edu); Shyamala Maheswaran (smaheswaran@mgh.harvard.edu)
- **Data availability**: scRNA-seq → GEO accession GSE75367; Mass spectrometry raw data → MassIVE accession MSV000079419
- **IRB**: IRB DF/HCC 05-300 (blood); IRB 2002-P-002059 (tumor specimens)

---

## Background

### 배경 스토리

- **문제의 출발점**: HER2(ERBB2) 유전자 증폭·과발현은 전통적으로 trastuzumab, lapatinib 등 표적치료의 필수 선별 기준이다. 그러나 ER+/HER2− 진단을 받은 전이성 유방암 환자에서 치료 경과 중 HER2를 발현하는 CTC가 출현한다는 임상 보고가 있었다(references 1, 2). 이 HER2 이질성이 표적치료 결정에 어떤 의미를 갖는지, 단순한 유전적 변이 획득인지 아니면 역전 가능한 표현형 전환인지는 불명확했다.
- **선행 접근 A — 정적 CTC 분석**: CellSearch 기반 CTC enumeration은 HER2 양성 여부를 단일 시점에서 판별하지만, 세포 내 분자 상태 변화를 추적하거나 생존 세포를 기능 실험에 사용하는 것이 불가능했다.
- **A의 한계**: 이질적 HER2 발현 분포, 세포 집단의 동적 재구성, 약물 노출에 따른 상태 전환을 포착할 수 없다.
- **선행 접근 B — CTC-iChip + 생존 CTC 배양**: Ozkumur et al. 2013과 Yu et al. 2014 (references 3, 4)가 미세유체 장치 기반 생존 CTC 분리 및 ex vivo 배양을 가능하게 했다. 이로써 단일세포 분자 분석 및 xenograft 이식 실험이 현실화됐다.
- **B에도 남은 한계**: HER2+ CTC가 유전자 증폭 없이 발생하는 기전, 두 상태의 기능적 비대칭성, 상호전환 가능 여부, 이 이질성을 표적화하는 치료 전략은 검증되지 않았다.
- **이 논문으로 이어지는 gap**: ① HER2+/HER2− 전환이 자발적이고 bidirectional인지; ② 두 상태가 서로 다른 약물 감수성을 갖는지; ③ 두 상태를 동시에 표적화하면 단독 요법 대비 치료 효과가 우월한지.

### 기본 개념

- **CTC (circulating tumor cell)**: 원발/전이 종양에서 혈액으로 유출된 암세포. 액체생검 마커로 종양 이질성 실시간 모니터링에 활용.
- **HER2 (ERBB2)**: 막관통 receptor tyrosine kinase. 유전자 증폭 시 trastuzumab/pertuzumab/lapatinib 등 표적치료 적용. 본 논문에서는 유전자 증폭이 아닌 발현 수준의 표현형 전환을 다룬다.
- **CTC-iChip**: 전혈에서 CD45+/CD66b+/CD16+ 백혈구를 면역자기 방식으로 고갈하여 EpCAM+/HER2+ CTC를 농축하는 미세유체 장치. 생존 세포 회수로 배양·단일세포 분석에 사용 가능.
- **FACS (fluorescence-activated cell sorting)**: HER2 발현 수준 기반 세포 정제. GFP 태그와 조합하면 lineage tracing 가능.
- **scRNA-seq**: 단일세포 전체 transcriptome 측정. ERBB2 RPM 분포의 bimodality를 통계 검증.
- **Notch 경로**: 세포 간 신호전달. HER2− CTC에서 활성화되며 HES/HEY, NRF2 하위 경로를 통해 항산화·약물 내성과 연결된다.

### 이 논문의 필요성

- **핵심 이유**: ER+/HER2− 환자가 전이 진행 중 HER2+ CTC를 획득하더라도, 이 세포가 HER2-증폭 암처럼 HER2 표적치료에 반응하는지 알 수 없었다.
- **기존 방법으로 부족했던 지점**: 정적 분자 프로파일링은 상태 전환 속도와 방향성, 각 상태의 약물 취약성을 측정하지 못한다.
- **이 논문이 해결하려는 방향**: 생존 CTC + lineage tracing으로 상호전환을 직접 관찰하고, proteomics/scRNA-seq로 각 상태의 분자적 기반을 규명하며, 병용 치료 전략을 전임상으로 검증한다.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: ER+/HER2− 전이성 유방암 CTC에서 HER2+/HER2− 상호전환의 빈도·방향성, 각 상태의 분자 경로 차이와 약물 감수성 차이를 정량화하고, 이를 근거로 한 병용 치료의 전임상 효능을 검증한다.
- **입력**: 환자 신선 혈액 / 3개 환자 유래 CTC 배양 세포주(Brx-42, Brx-82, Brx-142) / NSG 마우스 orthotopic mammary fat pad xenograft
- **출력**: HER2 상태 분류·전환율, 분자 경로 활성화 프로파일(protein, mRNA), 약물 IC50, 종양 성장 곡선, 전이 빈도
- **추정 대상**: HER2 상태 전환의 속도 및 방향성 비대칭, 각 상태를 표적화할 수 있는 약물 취약점
- **중요한 hidden assumption**: HER2 ≤1 RPM = HER2−, >10 RPM = HER2+ 컷오프가 생물학적 상태를 대표한다는 가정; FACS 정제 후 세포의 재도말이 in vivo 환경을 부분적으로 대표한다는 가정.

### 확률 / 통계학적 구조

- **Model family**: 정량 실험 + 빈도론적 통계 검정. 확률적 generative model 없음.
- **HER2 bimodality 검증**: Hartigans' dip test (`diptest` R-package), $\log_{10}(\text{RPM}+1)$ 기반. p = 7.5e-6 (n=22). 두 개 mode 검증에는 R density function 추가 사용.
- **HER2 분류 threshold**: HER2 >10 RPM = HER2+; HER2 ≤1 RPM = HER2−. scRNA-seq 기반 정의.
- **세포 증식·전환율**: Two-way ANOVA (p<0.0001, p<0.01), T-test (p<0.0001, p<0.05).
- **전이 빈도**: Extended Data Fig. 2d 표 — Fisher's exact test 함축 (p=0.05, p=0.009, n=8).
- **종양 성장 곡선**: Two-way ANOVA (in vivo, n=8).
- **GSEA**: Pathway Interaction Database (PID) + KEGG (MSigDB v4). FDR ≤0.25, nominal p-value <0.05. MS 데이터는 HER2-high vs HER2-low 간 $\log_2$ fold-change를 pre-ranked 입력으로 사용.
- **Proteomics FDR**: 펩타이드/단백질 할당 FDR <1% (SEQUEST + linear discriminant analysis).
- **TMT 정규화**: (1) 모든 TMT 채널 단백질 강도 → 채널 내 단백질 median average protein intensity 기준 정규화; (2) 채널 간 median intensity의 median으로 2차 보정.

### 핵심 method insight

- **기존 방법의 한계**: 정적 IHC/FISH는 증폭 여부만 판별하고 표현형 전환을 추적하지 못한다. 대량 CTC 검출 방법은 생존 세포를 반환하지 않아 기능 실험이 불가.
- **이 논문이 바꾼 가정**: HER2 발현 상태는 고정된 유전 특성이 아니라 역전 가능한 표현형 상태(phenotypic state)다. 두 상태는 동적 평형을 유지하며 환경 스트레스에 의해 전환 속도가 바뀐다.
- **새로 추가한 구조**: GFP-태그 lineage tracing (GFP+/HER2− → HER2+ 또는 GFP+/HER2+ → HER2− 딸세포 추적); 단일 세포 유래 colony의 크기별 HER2 전환 빈도 측정; TMT proteomics(>6300 단백질) + scRNA-seq 통합.
- **이 변화가 중요한 이유**: HER2+ 획득이 비가역적 유전 변이가 아닌 가역적 표현형 전환임을 증명하면, 표준 HER2 검사로는 치료 결정이 불완전하고, 두 상태를 동시에 표적화하는 전략이 필요하다는 논리가 성립한다.

### 이전 방법과의 차이

- **Baseline**: CellSearch CTC enumeration, 고정 세포 HER2 IHC/FISH
- **공통점**: HER2 단백질/유전자를 마커로 사용
- **차이점**: CTC-iChip은 생존 세포를 회수해 배양·정렬·단일세포 분석·xenograft 이식 직접 적용 가능. 동적 전환 실험(4–8주 추적) + scRNA-seq + proteomics 통합.
- **차이가 크게 나타나는 조건**: 다중 치료 후 생존 CTC 비율이 낮은 전이 진행 단계, HER2 발현이 이질적으로 분포하는 환자 샘플.

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: 19명 환자 CTC, 3개 CTC 세포주(Brx-42, Brx-82, Brx-142), NSG 마우스 xenograft (n=8/조건)
- **핵심 metric**: HER2+ 비율(%), 상호전환률(%), Ki67+ 비율, metastatic frequency, tumor photon flux, drug IC50
- **개선된 결과**: Ki67+ HER2+ > HER2− (p<0.0001, Brx-142); metastatic frequency HER2+ > HER2− (p=0.009, Brx-142); 파클리탁셀+Notch 저해제 병용 > 파클리탁셀 단독 (p<0.0001)
- **정성적 효과**: HER2+ — multi-RTK phosphorylation 활성; HER2− — Notch/DNA damage 경로 + γ-secretase inhibitor 감수성; Lapatinib IC50 HER2+ CTC ~1 μM (HER2-amplified SKBR3 5 nM의 ~200배) — oncogene addiction 없음.

### Method 관점의 한계

- **약한 assumption**: RPM 컷오프 설정이 데이터 기반이나 중간값 세포(1–10 RPM)의 상태 분류 불명확.
- **구현 부담**: CTC-iChip은 연구 플랫폼. 임상 루틴 전환 어려움. scRNA-seq에서 $10^5$ reads 미만 및 CD45 RPM >10 세포 제외로 세포 손실 발생.
- **일반화 제한**: 마우스 실험 무작위 배정·눈가림 없음 (Methods 직접 명시). 파일럿 연구(n=19) — 치료 개입 수와 HER2+ 빈도 상관관계의 통계적 유의성 검증 불충분.

---

## Results

### Dataset별 결과

#### Dataset 1 — 환자 CTC (n=19명 ER+/HER2− 전이성 유방암)

- **Dataset**: 19명 ER+/HER2− 전이성 유방암 환자 신선 혈액. CTC-iChip + imaging flow cytometry (EpCAM, HER2 staining).
- **목적**: 임상 환자에서 HER2+ CTC 획득 빈도 및 유전자 증폭과의 관계 확인.
- **데이터 규모**: 19명 환자; 22개 단일 CTC scRNA-seq (Brx-42, Brx-82 환자). HER2+ CTC 비율 median 22%, range 4–58%.
- **Baseline / 비교 대상**: ER+/HER2− 원발암 (FISH로 ERBB2 증폭 없음 확인); 전이 병변 IHC; HER2-amplified 대조군.
- **주요 수치**:
  - 16/19명(84%) HER2+ CTC 보유
  - scRNA-seq bimodal 분포 p=7.5e-6 (Hartigans' dip test, n=22)
  - HER2+ 중앙값 133 RPM (범위 32–217); HER2− ≤1 RPM
  - ER−/PR−/HER2− TNBC 환자 2/13명도 HER2+/HER2− CTC 공존
- **정성 결과**: 전이 병변 IHC에서 원발암 대비 HER2 염색 증가. FISH로 ERBB2 증폭 없음 — HER2 과발현이 복제수 변화 없이 발생.
- **논문 주장과의 연결**: HER2+ CTC 획득은 유전자 증폭과 무관한 표현형 변화.

#### Dataset 2 — CTC 세포주 상호전환 실험 (Brx-42, Brx-82, Brx-142)

- **Dataset**: 3개 환자 유래 CTC 배양 세포주. FACS-GFP 태그 + confocal microscopy lineage tracing. Single cell-derived colony 분석.
- **목적**: HER2+↔HER2− 자발적 상호전환 속도 및 방향성 비대칭 정량화.
- **데이터 규모**: n=3 S.D. error bar; single cell colony n=20.
- **주요 수치**:
  - HER2− → HER2+ 4주: Brx-82 42%, Brx-142 46%
  - HER2+ → HER2− 4주: Brx-82 5%, Brx-142 11%
  - 8주 후 parental HER2+/HER2− 조성 거의 회복
  - Colony 크기별 HER2− → HER2+ 전환: 5–9 cell 단계 6.5%; 10–19 cell 47%; >20 cell 59%
  - Colony 전환 T-test p<0.0001 (n=20)
  - In vivo: GFP+/HER2− → GFP+/HER2+ 44%; GFP+/HER2+ → GFP+/HER2− 21% (Fig. 2f; T-test p<0.05 상단, p<0.0001 하단; n=8)
- **정성 결과**: In vivo orthotopic tumor에서도 HER2− 유래 종양에 HER2+ 세포 출현, vice versa. 8주 추적 시 parental 조성 회복.
- **논문 주장과의 연결**: 상호전환은 자발적이고 bidirectional이며, HER2− → HER2+가 효율 우세 — 정상 배양에서 HER2+ 세포가 유지되는 기전.

#### Dataset 3 — 기능적 차이 및 분자 프로파일

- **Dataset**: Brx-42, Brx-82, Brx-142 FACS-정제 subpopulation. Orthotopic injection (NSG, n=8). TMT proteomics (>6300 proteins, n=2 biological replicates/cell line).
- **목적**: HER2+/HER2− 증식·종양형성·전이·분자 경로 차이 정량화.
- **주요 수치**:
  - Ki67+ HER2+ > HER2− (T-test p<0.0001, Brx-142)
  - Cleaved caspase 3 / Annexin V-FITC: HER2+ vs HER2− 차이 없음 (N.S.)
  - Metastatic frequency: HER2+ 6/8 (Brx-82, p=0.05), 7/8 (Brx-142, p=0.009) vs HER2− 2/8 each
  - Tumor initiation from 200 cells: N.S. (HER2+ vs HER2−, n=8)
  - Proteomics: HER2+/HER2− 차이 Pearson r 0.71–0.81 (세포주 간 일관); 같은 상태의 세포주 간 r = −0.22 ~ −0.063
  - scRNA-seq: 15/32 공유 경로가 HER2+ CTCs에서 농축 (Venn; protein+RNA 교집합)
- **정성 결과**: HER2+ — RTK phosphorylation (HER2, HER3, HER4, INSR, AXL/DTK, EPHA1, EPHA2), ERBB downstream, IGF1, MET 농축 (GSEA FDR ≤0.25). HER2− — Notch (HES/HEY, PS1), DNA damage (AuroraB, ATM, ATR, Fanconi) 농축.
- **논문 주장과의 연결**: HER2+는 증식·전이 우세; HER2−는 stress 내성·embryonic pathway 활성 상태.

#### Dataset 4 — 약물 스크리닝 및 Notch 경로 조작

- **Dataset**: 55종 약물 패널 (clinical relevance + epigenetic/stem cell pathway). HER2+/HER2− FACS-정제 (Brx-42, Brx-82, Brx-142). n=6, 3 독립 농도 (triplicate on duplicate plates).
- **목적**: 두 상태의 차별적 약물 감수성 규명 + HER2 억제 → Notch 활성화 연결 검증.
- **주요 수치**:
  - Lapatinib IC50 HER2+ CTC: ~1 μM vs SKBR3 (HER2-amplified) IC50=5 nM
  - HER2+IGF1R 이중 억제 → HER2+에 세포독성, HER2−에는 없음
  - 파클리탁셀/독소루비신/5-FU: HER2− 내성 > HER2+
  - γ-secretase inhibitor: HER2− 감수성 > HER2+
  - H2O2 (10 mM) 또는 docetaxel (1 nM) 처리 96시간: HER2+ → HER2− 30% 전환 (>70% 생존)
  - Single cell colony 5–9 cell 45%, >10 cell 62% HER2− 딸세포 출현 (T-test p<0.05, n=10)
- **In vivo 병용 치료**:
  - Paclitaxel 단독: 2주 후 39% HER2+, 7주 후 74% HER2+ (재발 종양에서 HER2+ 회복)
  - Paclitaxel + Notch inhibitor (LY-411575 또는 RO4929097): 재발 유의 지연 (Two-way ANOVA p<0.0001, n=8)
  - Notch inhibitor 단독: 종양 성장에 효과 없음
- **논문 주장과의 연결**: 파클리탁셀이 HER2+ → HER2− 전환을 유도 → Notch-sensitive HER2− 세포 증가 → Notch 저해제와 시너지.

### 전체 결과 요약

- **반복 패턴**: HER2+/HER2− 전환은 3개 독립 CTC 세포주 모두에서 일관되게 관찰됨. Stress (화학요법, 산화 스트레스)는 HER2+ → HER2− 전환을 촉진.
- **가장 중요한 수치**: 병용 요법 p<0.0001 (n=8); metastatic frequency p=0.009 (Brx-142); 8주 후 parental 조성 회복.
- **baseline 대비 차이**: Lapatinib IC50 HER2+ CTC ≈200배 높음 vs HER2-amplified SKBR3. Notch inhibitor 감수성 HER2− 특이적.
- **결과 해석 시 주의점**: 마우스 실험 무작위 배정·눈가림 없음. 파일럿 규모(n=19 환자). 환자별 CTC 세포주 간 proteome 이질성 존재.

---

## Figures

### Figure 1. Distinct properties of HER2+ and HER2− CTC subpopulations from patients with advanced ER+/HER2− breast cancer

- **이 Figure가 필요한 이유**: HER2+ CTC 획득이 임상 환자에서 빈번하게 발생하고, 유전자 증폭과 무관하며, 배양 세포주에서도 재현됨을 다중 방법론으로 동시에 증명하기 위해.
- **이 Figure가 뒷받침하는 주장**: HER2+ CTC는 원발암 HER2 상태와 무관하게 전이 진행 중 획득되며, 기능적으로 더 증식적이다.

##### 패널별 설명
- **a**: 환자 Brx-42, Brx-82 혈액에서 CTC-iChip 분리 후 imaging flow cytometry. EpCAM (yellow), HER2 (green). HER2+ CTC 비율: Brx-42 43%, Brx-82 13%.
- **b**: 22개 단일 CTC scRNA-seq ERBB2 RPM 분포. HER2− ≤1 RPM vs HER2+ median 133 RPM (32–217). Bimodal: p=7.5e-6.
- **c**: 환자 matched 원발암 vs 전이 병변 IHC. HER2+ 염색 전이 병변에서 증가. HER2-amplified 대조군과 비교.
- **d**: 배양 CTC (Brx-82, Brx-142) FACS — HER2+: 26.5%, 31.1% / HER2−: 73.9%, 68.9%.
- **e**: FACS-정제 HER2+ vs HER2− Ki67 증식 비교. HER2+ > HER2−. Two-way ANOVA p<0.01 (Brx-82), p<0.0001 (Brx-142); n=6; S.D.
- **f**: Orthotopic mammary fat pad 종양. HER2+ 유래 더 빠른 성장. Two-way ANOVA p<0.0001; n=8; S.D.

##### 본문에서 강조한 비교
- HER2+ vs HER2− 증식 차이(Ki67), 종양 성장 속도 차이가 핵심 비교.
- FISH로 ERBB2 증폭 없음 — HER2 과발현이 복제수 변화 없이 발생한다는 점 강조.

##### 해석 시 주의점
- Fig. 1f의 종양 성장 비교는 FACS-정제 후 주입 초기 데이터. 장기 추적 시 HER2+/HER2− interconversion 발생해 혼합됨 — Extended Data Fig. 2c에서 확인.

---

### Figure 2. Interconversion of HER2+ and HER2− phenotypes

- **이 Figure가 필요한 이유**: 두 상태가 고정이 아니라 자발적으로 상호전환됨을 in vitro + in vivo 두 방법으로 동시에 입증하기 위해.
- **이 Figure가 뒷받침하는 주장**: HER2+/HER2− 공존은 정적 이질성이 아니라 동적 평형이다.

##### 패널별 설명
- **a**: GFP-tagged HER2−/HER2+ CTCs 4주 배양 후 FACS. 양방향 전환 확인. HER2− → HER2+ 효율 높음(Brx-82: 42%, Brx-142: 46%); HER2+ → HER2− 낮음(5–11%).
- **b**: 8주 시계열. Parental 조성 회복 궤적. n=3; S.D.
- **c**: Single cell-derived colony confocal (EpCAM/HER2 공염색). 5–9 cell 단계부터 전환 세포 출현. n=20.
- **d**: Colony 크기별 전환율 정량 (HER2− → HER2+ 상단, HER2+ → HER2− 하단). T-test p<0.0001; n=20; S.D.
- **e**: Orthotopic xenograft — HER2− 유래 종양에 HER2+ 세포 IHC 출현, vice versa. n=8.
- **f**: Mixed GFP-tagged experiment — GFP+/HER2− → HER2+: 44%; GFP+/HER2+ → HER2−: 21%. T-test p<0.05 (상), p<0.0001 (하); n=8; S.D.

##### 본문에서 강조한 비교
- HER2− → HER2+ 전환 빈도가 역방향보다 유의하게 높음. 증식 속도 차이만으로는 이 조성이 설명되지 않으므로 실제 phenotypic switching이 필요함을 논증.

##### 해석 시 주의점
- GFP-tagging이 세포 표현형에 영향을 줄 가능성. 전환율은 특정 시점 스냅샷 기준이므로 연속적인 동역학 모델링은 미제공.

---

### Figure 3. Molecular pathways differentially activated in HER2− versus HER2+ cultured CTCs

- **이 Figure가 필요한 이유**: HER2+/HER2− 상태 전환의 분자적 기반을 규명하고, 각 상태를 표적화할 수 있는 경로를 제안하기 위해.
- **이 Figure가 뒷받침하는 주장**: HER2+ 상태는 multi-RTK pro-growth, HER2− 상태는 Notch/DNA damage 활성이다.

##### 패널별 설명
- **a**: 3개 CTC 세포주 TMT proteomics scatter (6349 단백질). HER2+ vs HER2− 차이의 세포주 간 Pearson r: Brx-82 vs Brx-142 = 0.71–0.81; 같은 상태 내 세포주 간 r = −0.22 ~ −0.063.
- **b**: HER2+ CTCs에서 농축된 단백질 네트워크 + GSEA 경로 bar chart. ERBB downstream, ERBB2/3, IGF1, MET, AV3 integrin, E/N-cadherin 등.
- **c**: HER2− CTCs 농축 경로. HES/HEY (Notch), PS1, ATM, ATR, AuroraB, Fanconi. GSEA FDR ≤0.25.
- **d**: Lapatinib/siHER2로 HER2 억제 → HER2+ CTCs에서 NOTCH1, JAG1, DLL1, HES1, HEY1, HEY2 mRNA 증가. p<0.05; n=6; S.E.M.

##### 본문에서 강조한 비교
- HER2 발현과 NOTCH1 발현 간 inverse 상관 (scRNA-seq, western blot, IF 세 가지 방법). HER2 억제가 능동적으로 Notch 경로를 활성화한다는 인과적 해석 제공.

##### 해석 시 주의점
- MS/scRNA-seq 비교는 세포주 n=2 biological replicates. 경로 분석 기반 결론. 직접적인 TF 결합 등 mechanistic 증거는 미제공.

---

### Figure 4. Cooperative targeting of HER2+ and HER2− CTC subpopulations suppresses tumor growth

- **이 Figure가 필요한 이유**: 분자 프로파일에서 예측된 약물 취약성을 실험적으로 검증하고, 병용 치료의 전임상 우월성을 증명하기 위해.
- **이 Figure가 뒷받침하는 주장**: HER2+/HER2− 이질성을 동시에 표적화하는 병용 치료가 단독 요법보다 지속적인 종양 억제를 달성한다.

##### 패널별 설명
- **a**: Lapatinib dose-response: HER2+ CTC IC50 ~1 μM (SKBR3 5 nM 대비). HER2+IGF1R 이중 억제 → HER2+ 선택적 세포독성. n=6; S.D.
- **b**: Docetaxel: HER2− 내성 > HER2+. Notch inhibitor (BMS-708163): HER2− 감수성 > HER2+. n=6; S.D.
- **c**: siHER2 또는 lapatinib으로 HER2 억제 → NOTCH1, JAG1, DLL1, HES1, HEY1, HEY2 mRNA 유도. p<0.05; n=6; S.E.M.
- **d**: H2O2 (10 mM) 또는 docetaxel (1 nM) 96시간 처리 → HER2+ → HER2− 30% 전환 (FACS).
- **e**: Single cell HER2+ colony에서 H2O2 처리 후 HER2− 딸세포 신속 출현 (confocal). n=10.
- **f**: Paclitaxel 처리 후 HER2+ 종양에서 HER2+ 세포 감소 → 재발 시 HER2+ 재회복. HER2− 유래 종양은 paclitaxel 효과 제한적. p-value T-test <0.05; n=8.
- **g**: Paclitaxel + Notch inhibitor (RO4929097 또는 LY-411575) 병용 vs 단독 비교. 재발 유의 지연. Two-way ANOVA p<0.0001; n=8.

##### 본문에서 강조한 비교
- Paclitaxel 단독: 초기 수축 후 HER2+ 회복·재발. 병용: HER2− 세포(Notch-sensitive)까지 억제 → 지속 suppression. Notch inhibitor 단독: 효과 없음 — 따라서 순서 의존적 파클리탁셀 선행이 아닌 동시 투여로 검증.

##### 해석 시 주의점
- 마우스 실험 무작위 배정·눈가림 없음. In vivo pharmacokinetics/dynamics 데이터 미제공. Notch inhibitor 독성 프로파일 논의 없음.

---

## Tables

본문에 별도 번호를 갖는 정식 Table 없음.

Extended Data Figure 내 삽입 표 형태 데이터:
- **Extended Data Fig. 2d — Metastatic Frequency from Orthotopic Injections**: Brx-82 HER2+ 6/8 vs HER2− 2/8 (p=0.05); Brx-142 HER2+ 7/8 vs HER2− 2/8 (p=0.009); n=8.
- **Extended Data Fig. 2e — Tumor Initiation from 200 Cells**: Brx-82 HER2+ 8/8 vs HER2− 8/8 (p=NS); Brx-142 HER2+ 4/8 vs HER2− 3/8 (p=NS); n=8 — 종양 형성 능력은 동등.

**Supplementary Tables** (본문 언급, xlsx 파일):
- Supplementary Table 1: 환자 임상 정보 및 HER2+/HER2− 비율
- Supplementary Table 2: HER2+/HER2− 세포주 간 돌연변이 비교 — 식별되는 구별 돌연변이 없음
- Supplementary Tables 3, 4: TMT proteomics 전체 단백질 + GSEA 결과
- Supplementary Table 5: 55종 약물 목록
- Supplementary Table 6: Drug screen IC50 데이터 전체

---

## Supplementary Information

- **Extended Data Fig. 1**: 19명 환자 HER2+/HER2− CTC 분포 bar graph (median 22% HER2+, range 4–58%); ERBB2 scRNA-seq 시계열(질병 진행 시 HER2+ 비율 증가); TNBC 13명 HER2+/HER2− 분포; FISH 증폭 없음; CTC 세포주 IF; FACS bimodality; ERBB2 FISH HER2+ vs HER2− subpopulation.
- **Extended Data Fig. 2**: Ki67/CC3 IF; Annexin V-FITC; 종양 성장 곡선(Brx-82); Metastatic frequency 표; Limiting dilution 종양형성 표.
- **Extended Data Fig. 3**: GFP lineage tracing FACS 28일 시계열(Brx-82); HER2+/HER2− 증식 속도 비교; In vivo HER2 interconversion IHC; GFP/HER2 병용 IHC.
- **Extended Data Fig. 4**: MS proteomics scatter (Brx-82/Brx-142); Phospho-RTK array (HER2+: RTK 인산화 활성, HER2−: 없음); scRNA-seq volcano plot; Venn diagram (protein+RNA HER2+ 특이 경로 15개 공유).
- **Extended Data Fig. 5**: 55종 약물 heat map (HER2+/HER2−, Brx-142/Brx-82); Lapatinib/docetaxel/5-FU/Notch inhibitor dose-response.
- **Extended Data Fig. 6**: NOTCH1 western blot; Notch ICD 과발현 → Notch 유전자 발현 증가; siHER2 → Notch 유전자 유도; HER2 억제 → NRF2-driven 사이토보호 유전자 증가(GCLC, GGT1, GPX1, GPX4, HMOX1); Paclitaxel 처리 후 종양/CTC HER2 조성 변화; 병용 치료 종양 성장 곡선(Brx-142).

---

## 분석 자체에 대한 메모

- 본 논문은 5페이지 main text + 6개 Extended Data Figure + 6개 Supplementary Table의 고밀도 Nature Letter 형식이다. 주요 수치들이 Extended Data Figure caption에 분산되어 있어 통합이 필요하다.
- Supplementary Tables (특히 Table 1 환자 임상 정보, Tables 3–4 proteomics 전체 데이터, Table 6 약물 IC50)은 xlsx 파일로 제공되나 본 분석에서 직접 접근하지 않았다. 상세 수치 검증은 해당 파일 확인 필요.
- 무작위 배정·눈가림 없는 마우스 실험 — Methods에 직접 명시된 한계. 통계 해석 시 주의.
- ALDH1 stem cell marker가 HER2+/HER2− 모두에서 유사하게 발현된다는 Discussion 언급은 main text에 직접 데이터 없음 (Supplementary에 있을 것으로 추정) — 검토 필요.
- scRNA-seq 데이터(GSE75367)와 MS 데이터(MSV000079419)는 공개 접근 가능 — 독립 재분석 여지 있음.
