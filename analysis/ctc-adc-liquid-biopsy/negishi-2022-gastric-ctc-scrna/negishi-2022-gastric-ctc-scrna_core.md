# negishi-2022-gastric-ctc-scrna — Core Analysis

## Executive Summary

- **무엇**: 전이성 위암 환자의 단일 CTC를 surface antigen-independent MCA/GCM 방법으로 분리해 전체 전사체를 sequencing함으로써, 위암 CTC의 EMT 서브그룹 구조와 혈소판-CTC 상호작용이 EMT 유도 및 화학내성 획득에 기여한다는 메커니즘을 제시한 탐색적 연구.
- **모델 / 방법**: 8 µm 포어 마이크로캐비티 어레이(MCA)로 크기 기반 CTC 농축 → 하이드로겔 캡슐화로 단일세포 분리(GCM) → Quartz-seq 기반 poly-A tailing WTA → RNA-seq (Illumina HiSeq 2500, 50-base, 5 M reads/cell) → Seurat 비지도 클러스터링 + UMAP → DAVID gene ontology (GO) 분석.
- **핵심 결과**:
  - ① 27명 환자 혈액 112개 CTC 후보 중 43.8% (49/112)가 QC 통과 — 기존 CellSearch 대비 현저히 높은 mesenchymal CTC 포함 검출.
  - ② 47개 CTC에서 대부분 mesenchymal marker 발현 높고 epithelial marker 낮음 — EMT가 위암 CTC 주요 표현형.
  - ③ UMAP 비지도 클러스터링으로 Subgroup A (EMT + 전사 활성화), B (혈소판 부착), C (epithelial, 대사 활성) 3종 서브그룹 식별.
  - ④ Subgroup A는 화학치료 비반응·장기 치료력 환자에 집중 → 화학내성 association 시사.
  - ⑤ Subgroup C (epithelial) 환자 2명 모두 혈액 채취 1개월 이내 사망 → 예후 불량 association.
- **우리 적용**: 위암 CTC의 EMT·혈소판 상호작용 메커니즘 및 subgroup 임상 의의 — ADC target 선정 및 액체생검 기반 진단 마커 연구의 academic-citation + BD 참고 자료.
- **심층**: 한계·재현 ROI는 `negishi-2022-gastric-ctc-scrna_lens-academic.md` / `negishi-2022-gastric-ctc-scrna_lens-industry.md` / `negishi-2022-gastric-ctc-scrna_methodology-brief.md` 참고.

---

## Identity

- **Title**: Transcriptomic profiling of single circulating tumor cells provides insight into human metastatic gastric cancer
- **Authors**: Ryo Negishi, Hitomi Yamakawa, Takeru Kobayashi, Mayuko Horikawa, Tatsu Shimoyama, Fumiaki Koizumi, Takeshi Sawada, Keisuke Oboki, Yasushi Omuro, Chikako Funasaka, Akihiko Kageyama, Yusuke Kanemasa, Tsuyoshi Tanaka, Tadashi Matsunaga & Tomoko Yoshino
- **Year**: 2022
- **Venue**: Communications Biology 5, 20
- **DOI**: 10.1038/s42003-021-02937-x
- **Citation key**: `negishi2022gastricctcscrna`
- **Received**: 2020-12-15 / **Accepted**: 2021-12-01 / **Published online**: 2022-01-11
- **Affiliations**: Tokyo University of Agriculture and Technology (공학부 생명科学科); Tokyo Metropolitan Cancer and Infectious Diseases Center Komagome Hospital (화학요법과, 검사과); Tokyo Metropolitan Institute of Medical Science

---

## Background

### 배경 스토리

- **문제의 출발점**: 전이성 위암은 5년 생존율 <10%이며 화학요법 내성이 잦다. 내성·전이 메커니즘을 조직 생검 없이 실시간으로 파악할 수단이 필요하다. CTC는 ctDNA·exosome과 함께 액체생검의 주요 표적으로, 종양 구성·침습성·약제 감수성에 대한 정보를 직접 제공할 수 있는 세포 단위 자료다 (Introduction §1).

- **선행 접근 A — EpCAM 기반 CellSearch**: 현재 FDA 승인된 CTC 검출 표준 방법. EpCAM 항체 친화도 기반으로 epithelial 표현형 세포를 포착한다. 다른 암종에서 예후 예측 유효성이 보고되었고 위암에서도 활용된다 (ref. 26, 27).

- **A의 한계**: 위암 CTC에서 EpCAM-positive 수가 다른 암종보다 낮다. EMT를 거쳐 mesenchymal 표현형으로 전환된 CTC는 EpCAM 발현이 소실되어 CellSearch로 검출되지 않는다 (ref. 28). 선행 연구(RNA-ISH로 vimentin·twist 발현 CTC 동정; ref. 30)에서 mesenchymal CTC의 존재가 확인되었으나 분자 메커니즘은 불명확했다 — 대상 유전자 수가 극히 제한적이었기 때문이다.

- **선행 접근 B — 상업용 단일세포 분리 시스템**: VyCap Puncher, DEPArray, ALS CellColector, RareCytes CyteFinder 등이 개발되어 있으나, CTC 농축 단계와 단일세포 분리 단계가 통합되어 있지 않아 sample handling 중 CTC 손실 위험이 있다 (ref. 33–36). 또한 Droplet/nanowell/FACS 기반 시스템은 rare cell을 random population에서 분리하는 방식이라 CTC 같은 극희귀 세포 회수에 부적합하다.

- **이 논문으로 이어지는 gap**: 위암에서 단일 CTC 전사체 분석이 보고된 적이 없다. EMT 유도 메커니즘, 혈소판과의 상호작용, 화학내성 관련 transcriptome을 단일세포 해상도로 특성화하는 것이 CTC 연구의 핵심 공백이었다.

### 기본 개념

- **CTC (순환 종양세포)**: 원발 종양에서 혈관으로 탈락해 혈류를 순환하는 세포. 전이의 주요 경로이며, 액체생검 표적으로 종양 이형성·약제 내성 정보를 담는다.
- **EMT (epithelial-mesenchymal transition, 상피-간엽 전이)**: 상피세포가 간엽세포 표현형으로 전환되는 과정. CTC에서 EpCAM·cytokeratin 발현이 감소하고 vimentin·CDH11 등 mesenchymal marker가 증가한다. 전이 및 화학내성 획득과 연관된다.
- **MCA (microcavity array, 마이크로캐비티 어레이)**: 8 µm 포어 직경의 니켈 제조 필터. 크기 기반으로 혈액 중 CTC를 농축한다 — WBC (백혈구) 오염을 최소화하면서 mesenchymal CTC 포함 다양한 표현형 포착 가능.
- **GCM (gel-based cell manipulation, 젤 기반 세포 조작)**: 하이드로겔(PEGDA) 캡슐화로 단일세포를 분리하는 기술. Droplet 기반과 달리 반응 부피가 매우 작아(0.4 µL) 수분 오염 없이 WTA 수율이 높다.
- **WTA (whole transcriptome amplification, 전체 전사체 증폭)**: 단일세포의 mRNA 전체를 증폭. 본 논문은 Quartz-seq 기반 poly-A tailing 방식 사용. 세포 크기·mRNA 양에 비례한 cDNA 수율을 보인다.
- **UMAP (Uniform Manifold Approximation and Projection)**: 고차원 전사체 데이터를 2차원으로 축소해 클러스터 구조를 시각화하는 비선형 차원 축소 방법. Seurat 패키지 내 공유 최근접 이웃(shared nearest neighbor) 기반 클러스터링과 함께 사용.

### 이 논문의 필요성

- **핵심 이유**: 위암 CTC에 대한 단일세포 전사체 데이터가 전무하다. 소수 마커(vimentin, twist) 기반 RNA-ISH와 달리, 전체 전사체 분석이 EMT 서브그룹 구조와 혈소판 연관 메커니즘을 식별할 수 있는 해상도를 제공한다.
- **기존 방법으로 부족했던 지점**: EpCAM 의존성 — mesenchymal CTC 누락. 소수 마커 — 메커니즘 정보 부족. 단일세포 분리와 sequencing의 미통합 — 효율·오염 문제.
- **이 논문이 해결하려는 방향**: MCA 크기 선택 + GCM 단일세포 분리 + Quartz-seq WTA의 파이프라인으로 EpCAM-independent하게 위암 단일 CTC를 전사체 수준에서 특성화하고, 그 결과에서 임상적으로 의미 있는 서브그룹을 도출한다.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 전이성 위암 환자 말초혈액에서 EpCAM-independent 방법으로 단일 CTC를 분리하고 전체 전사체를 sequencing하여, 위암 CTC의 transcriptomic 이형성 구조를 규명한다.
- **입력**: 환자 말초혈액 1–3 mL; 암세포주 spike-in (양성 대조군 NCI-H1975, AGS, NCI-N87, SNU-1).
- **출력**: 단일 CTC별 전체 전사체(RNA-seq reads → RPM 기반 gene expression matrix) + 비지도 클러스터링 서브그룹 레이블 + 임상 표현형 연관성.
- **추정 대상**: CTC의 transcriptional 서브그룹 구조 (EMT/혈소판/epithelial); 서브그룹별 임상 예후 연관성.
- **중요한 hidden assumption**: RPM < 1.0을 미발현으로 정의 (arbitrary threshold). 미토콘드리아 유전자 비율 >25%를 저품질로 제거. Poly-A tailing WTA는 3' 편향을 일으키며 CTC에서 더 강하게 관찰됨 — 유전자 검출 수가 세포주보다 낮을 수 있음.

### 확률 / 통계학적 구조

- **Model family**: 비지도 군집화 (unsupervised clustering). 확률 모델이 아닌 graph 기반 Seurat 파이프라인 사용. PCA → shared nearest neighbor graph → Louvain 알고리즘 클러스터링 → UMAP 시각화.
- **Likelihood / objective**: 클러스터링 objective는 Seurat의 resolution parameter 기반 공유 최근접 이웃 그래프 분리. 명시적 likelihood 없음.
- **Prior / regularization**: 미제공 — Seurat resolution parameter 값 본문 명시 없음.
- **Latent variable / hidden state**: CTC subgroup label (A, B, C) = latent cluster assignment.
- **Inference / optimization**: 
  - 전처리: Trimmomatic-0.36-5 → HISAT2 2.1.0 (hg19 alignment) → HTseq (read count) → RPM 변환 (read count ÷ total reads × 10^6).
  - 차원 축소: R stats v3.6.2의 log-normalization → PCA → UMAP.
  - 클러스터링: Seurat shared nearest neighbor method.
  - GO 분석: DAVID v6.8 (p < 0.05 유의 유전자 적용).
- **통계 검정**: RNA-seq 외 통계는 Welch's t-test (two-tailed, α = 0.05). Supplementary Fig. 3A의 GCM vs. micromanipulation cDNA yield 차이: p = 0.003. 평균 길이 차이: p = 0.147.
- **Noise, sparsity, uncertainty 처리**: GAPDH 발현 확인으로 QC (GAPDH undetectable → 제외). 미토콘드리아 유전자 비율 > 25% 세포 제거. PTPRC (CD45) WBC 마커 발현 세포 오염 평가 (1개 CTC 후보에서 weak 발현 확인, 제외하지 않음).

### 핵심 method insight

- **기존 방법의 한계**: CellSearch/RareCytes 등은 EpCAM 항체 친화도에 의존하여 EMT 진행 CTC를 포착하지 못한다. 또한 CTC 농축과 단일세포 분리가 분리된 단계로 처리 중 세포 손실이 일어난다.
- **이 논문이 바꾼 가정**: CTC 분리 기준을 항원 특성이 아닌 세포 크기(8 µm 포어)로 전환. 이로써 EpCAM-negative mesenchymal CTC를 포함한 다양한 표현형을 포착한다.
- **새로 추가한 구조**: MCA(크기 농축) + GCM(하이드로겔 단일세포 캡슐화)의 통합 파이프라인. GCM은 수분 오염 없이 극소용량(0.4 µL) 반응을 가능하게 해 WTA 수율을 micromanipulation 대비 2배 높였다 (80.6 ± 33.6 ng vs. 40.3 ± 29.4 ng, p = 0.003; Supplementary Fig. 3A).
- **이 변화가 중요한 이유**: 위암에서 대다수 CTC가 EMT를 거쳤기 때문에 EpCAM-based 방법으로는 대부분 놓친다. 본 방법은 mesenchymal CTC를 포함해 96% (26/27 환자) 검출 성공률을 달성했다 (Discussion).

### 이전 방법과의 차이

- **Baseline**: CellSearch (EpCAM 기반) + 종래 micromanipulation WTA.
- **공통점**: mRNA 전사체를 sequencing하는 전략; 액체생검 CTC 사용.
- **차이점**: EpCAM → size-based 분리; micromanipulation → GCM 하이드로겔 캡슐화; CTC 농축과 단일세포 분리 통합 파이프라인.
- **차이가 크게 나타나는 조건**: EMT가 진행된 CTC (EpCAM 소실 세포)를 포함하는 상황; 소량 혈액(1 mL) 기반 단일세포 분석.

### 효과가 Results에서 나타난 방식

- **Benchmark**: 위암 환자 27명 임상 코호트; 암세포주 spike-in 대조군.
- **Metric**: QC pass rate, nFeature/nCount, cDNA yield, EMT marker 발현 score, GO enrichment p-value, 임상 outcome 연관성.
- **개선된 결과**: 기존 보고(11–85% 검출)보다 높은 96% 환자 검출, QC pass rate 43.8%, CTC cDNA yield median ~850 bp.
- **정성적 효과**: EMT marker 풍부 CTC를 포함하여 위암 CTC의 생물학적 이형성을 3개 서브그룹으로 분류. 서브그룹 A와 C의 임상 예후 association 도출.

### Method 관점의 한계

- **약한 assumption**: RPM 1.0 cutoff의 생물학적 근거 미제공. GAPDH 발현만으로 RNA quality를 판단하는 단순화.
- **구현상의 부담**: 수동 단일세포 분리(GCM)가 여전히 기술 집약적이고 처리량이 낮다. 5 M reads/cell는 기존 scRNA-seq 표준(~10 M reads)보다 낮다.
- **일반화가 불확실한 조건**: 단일 기관 코호트, 소규모(n = 27 환자, 47 CTC 최종 분석). 위암 이외 암종에서의 적용성 불명확.

---

## Results

### Dataset별 결과

#### Dataset 1 — 기술 검증: GCM vs. micromanipulation (암세포주 spike-in)

- **Dataset**: NCI-H1975 (폐암세포주) 단일세포, n = 11 (micromanipulation), n = 16 (GCM).
- **목적**: MCA/GCM 방법의 WTA 수율·품질을 종래 micromanipulation과 비교 검증.
- **사용한 데이터 규모**: 각 방법 8–16 단일세포; qPCR (11 유전자) 발현 cluster analysis로 방법 간 차이 평가.
- **Baseline / 비교 대상**: Micromanipulation (유리 모세관 기반).
- **주요 수치**:
  - cDNA yield: GCM 80.6 ± 33.6 ng vs. micromanipulation 40.3 ± 29.4 ng (p = 0.003; Supplementary Fig. 3A).
  - 평균 cDNA 길이: GCM 1022.9 ± 134.4 bp vs. micromanipulation 930 ± 169.0 bp (p = 0.147; Supplementary Fig. 3B).
  - cDNA yield >10 ng/assay를 qPCR 분석 기준치로 설정 (Fig. 1B).
- **정성 결과**: 11 유전자 qPCR cluster analysis에서 두 방법 간 발현 패턴 차이 없음 (clustering에서 방법별 분리 미관찰; Fig. 1C). GCM이 성능 동등 이상 확인.
- **논문 주장과의 연결**: GCM이 기존 방법 대비 수율에서 우월하며, 유전자 발현 패턴에서 동등 — 이후 임상 CTC 분석의 방법적 기반.

#### Dataset 2 — 전이성 위암 환자 CTC 분리 및 QC

- **Dataset**: 전이성 위암 환자 27명 혈액 (2017년 4월 ~ 2019년 10월, 도쿄 도립 암·감염증센터 코마고메 병원). 화학요법 치료 중 n = 24; 화학요법 미치료 n = 3 (보충: 각 환자 혈액 1–3 mL 사용).
- **목적**: 임상 혈액에서 CTC 분리 성공률 및 RNA quality QC.
- **사용한 데이터 규모**: 112개 CTC 후보 (26/27 환자에서 검출); 건강인 혈액 1건 (음성 대조군).
- **주요 수치**:
  - 분리 CTC 후보 수: 0–13개/환자 (Fig. 2B 참조).
  - GAPDH 발현 기반 QC: 49/112 = 43.8% pass.
  - cDNA yield 범위: 0.1–99.3 ng/cell (Fig. 1B).
  - 검출 transcript 수: CTC는 1183–11,230 개 (평균 4064 ± 1967), 암세포주 단일세포는 4376–12,084 개 (평균 n=12).
  - 미토콘드리아 유전자 비율: 평균 5.07%, 중앙값 1.33% (범위 0.02–68.17%). >25% 제거 후 최종 47 CTC 분석.
- **정성 결과**: PTPRC (CD45) WBC 마커는 CTC 후보 48/49에서 음성 (1개 weak 발현이나 발현량 매우 낮아 분석 포함). 건강인 혈액에서 CTC 후보 미검출.
- **논문 주장과의 연결**: 96% 검출 성공률은 기존 보고(11–85%)보다 높다 — EpCAM-independent 크기 선택의 장점.

#### Dataset 3 — 단일 CTC 발현 패턴 분석: 알려진 마커 (n = 47 CTC)

- **Dataset**: 최종 47 CTC + 12 암세포주 단일세포 (AGS, NCI-N87 각 3개, SNU-1 6개).
- **목적**: 위암 CTC의 EMT 상태, 줄기세포성, 증식능력 특성화.
- **Metric**: RPM 기반 발현 heatmap; epithelial score (KRT family, EpCAM) vs. mesenchymal score (ZEB2, CDH11, vimentin 등) scatter plot.
- **주요 수치**:
  - RHOA 또는 CTNNB1: 47/47 (100%) CTC 발현.
  - 상피 마커 발현 CTC: 23/47 (KRT 유전자 발현 세포); 대부분 낮은 EpCAM·KRT.
  - 줄기세포 마커 CD44: 8/47 (16%) CTC 발현.
  - ITGA2: 22/47 (45%) CTC 발현.
  - Ki67 (MKI67): 거의 미검출 — 세포 증식 정지 상태.
- **정성 결과**: 대부분 CTC가 mesenchymal gene 발현 score가 세포주보다 높았으며 (Fig. 3B), 일부 epithelial CTC(G_12, G_25)도 관찰. 증식 마커 Ki67 미검출 → cell cycle arrest 시사.
- **논문 주장과의 연결**: 다수 위암 CTC가 EMT를 경험했으며 이질적 표현형 혼재 — 단일 마커 기반 검출·분류의 한계 재확인.

#### Dataset 4 — 비지도 클러스터링: 3개 서브그룹 식별 (n = 47 CTC + 12 세포주)

- **Dataset**: 47 CTC + 12 세포주, Seurat 비지도 클러스터링.
- **목적**: 전사체 패턴 기반 CTC 이형성의 구조적 분류.
- **Baseline / 비교 대상**: 3개 암세포주 (AGS, N87, SNU-1) — 세포주 대부분 Subgroup C에 속함.
- **주요 결과**:
  - **Subgroup A**: EMT 관련 전사인자 (ZEB2, MEF2D, NFKB1A, GATA1, GATA2) 고발현; 전사 활성화 관련 유전자 (KMT2A 등) 발현; nFeature 평균 4805 ± 1412 genes.
    - GO enrichment: GO:0045893 (positive regulation of transcription, DNA-templated; p = 2.08E-07), GO:0045944 (RNA pol II promoter transcription 양성 조절; p = 8.55E-05), hsa05202 (Transcriptional misregulation in cancer; p = 1.48E-07) (Fig. 5B).
    - 임상 연관: 화학치료 비반응·장기 치료 이력 환자에서 Subgroup A CTC 검출 — 화학내성 association (Supplementary Table 3).
  - **Subgroup B**: 혈소판 관련 유전자 (PF4, PPBP, ITGA2B, SPARC, TGFB1, ITGA2) 고발현; nFeature 평균 2418 ± 845 genes (A보다 낮음).
    - GO enrichment: GO:0002576 (platelet degranulation; p = 1.64E-07), GO:0070527 (platelet aggregation; p = 0.0217) (Fig. 5B).
    - 해석: 혈소판이 부착된 CTC. TGF-β/SMAD 신호 → NF-κB 경로 → EMT 유도 연결 가능성 제시.
  - **Subgroup C**: 상피 마커 (EpCAM, KRT8, KRT18, KRT19) 고발현; 세포주와 유사한 대사 유전자 발현; Proliferative gene 발현.
    - 임상 연관: Subgroup C 환자 2명 모두 혈액 채취 1개월 이내 사망 (Supplementary Table 1, overall survival 27일, 10일).
- **통계**: 서브그룹 간 nCount에서 유의한 차이 없음 (Supplementary Fig. 5). nFeature는 A > B 뚜렷.

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 위암 CTC의 대부분이 EMT를 경험 — KRT/EpCAM 발현 낮고 mesenchymal marker 높음. 동시에 cell cycle 정지 (Ki67 미검출).
- **가장 중요한 수치**: Subgroup A GO p = 2.08E-07 (transcription regulation); Subgroup B GO p = 1.64E-07 (platelet degranulation). 환자 검출률 96% (26/27). QC pass rate 43.8%.
- **baseline 대비 차이**: 세포주(Subgroup C에 집중)와 대부분 CTC(Subgroup A, B)가 UMAP에서 명확히 분리 → 세포주 기반 연구가 CTC 생물학을 대표하지 못함 시사.
- **결과 해석 시 주의점**: Subgroup A와 화학내성의 연관은 후향적·소규모 관찰이며, Supplementary Table 3에서 환자 수 제한적. Subgroup C 예후 불량 역시 n = 2에 불과.

---

## Figures

#### Figure 1 — Single-cell isolation and gene expression analysis based on MCA and GCM

- **이 Figure가 필요한 이유**: 논문 전체의 기술적 플랫폼을 제시하고, MCA/GCM 방법이 micromanipulation 대비 성능이 동등하거나 우수함을 입증하기 위해 배치.
- **이 Figure가 뒷받침하는 주장**: MCA/GCM 기반 단일세포 분리가 RNA-seq에 충분한 품질의 cDNA를 산출하며, 방법 차이가 유전자 발현 결과에 영향을 주지 않는다.

##### 패널별 설명
- **a**: MCA/GCM 4단계 workflow 모식도 — 여과(8 µm 포어) → 형광 염색(CellTracker Green + Hoechst 33342 + anti-CD45) → 하이드로겔 캡슐화(PEGDA + 광개시제, λ = 365 nm) → 단일세포 트위저 분리.
- **b**: WTA cDNA yield 바이올린 플롯. x축: 세포주(NCI-H1975, AGS, SNU-1, NCI-N87) + Gastric CTC. y축: cDNA yield (ng). Gastric CTC는 0.1–99.3 ng로 세포주보다 변동이 큼 — mRNA 양의 세포 간 이질성 반영.
- **c**: 16개 단일세포(NCI-H1975, micromanipulation n=8 + GCM n=8)의 11 유전자 qPCR 발현 cluster heatmap. 두 방법이 섞여 있으며 방법 기반 클러스터 분리 없음 — 방법 동등성 확인.

##### 본문에서 강조한 비교
- GCM vs. micromanipulation cDNA yield (p = 0.003) — GCM 우월; 평균 길이는 차이 없음 (p = 0.147).

##### 해석 시 주의점
- cDNA yield 차이가 있어도 gene expression 패턴이 같은지는 qPCR 11개 유전자 기반 확인에 불과. 전체 전사체 수준 동등성은 추가 검증 필요.

---

#### Figure 2 — Isolation of gastric CTCs and RNA-seq analysis

- **이 Figure가 필요한 이유**: 임상 CTC 분리 결과와 QC 과정(GAPDH 발현, gene body coverage)을 보여주어 이후 분석에 사용되는 데이터의 신뢰성을 제시.
- **이 Figure가 뒷받침하는 주장**: CTC 후보가 WBC와 구별되며(CD45 음성), RNA 품질이 전사체 분석에 충분하다.

##### 패널별 설명
- **a**: CTC 후보(CellTracker Green+/CD45−/Hoechst+) vs. WBC(CD45+ 적색) 형광 이미지. Scale bar = 50 µm.
- **b**: 27명 환자별 분리 세포 수 및 GAPDH 발현 세포 수 표. 총 112개 후보에서 49개 QC pass. G5 환자 데이터 N/A (기술 오류).
- **c**: 단일 SNU-1 세포 (상) 및 단일 CTC (하)의 gene body coverage 곡선. SNU-1은 완만한 5'→3' 편향, CTC는 더 강한 3' 편향 — mRNA 분해(세포사멸 초기) 시사.

##### 본문에서 강조한 비교
- Gene body coverage 3' 편향이 CTC에서 SNU-1보다 더 강함 — "CTC RNA는 apoptosis로 인해 세포질 mRNA가 분해되기 시작한 상태일 가능성" (Discussion).

##### 해석 시 주의점
- Gene body 3' 편향은 poly-A tailing WTA의 기본 특성. CTC 특이적 분해 여부를 이것만으로 단정하기 어렵다.

---

#### Figure 3 — Targeted analysis of single-cell RNA-seq data

- **이 Figure가 필요한 이유**: 알려진 위암·EMT·줄기세포 마커를 targeted 분석해 위암 CTC가 EMT 표현형을 주로 가지며 증식 정지 상태임을 보이기 위해.
- **이 Figure가 뒷받침하는 주장**: 대다수 위암 CTC는 EMT를 경험했으며, 일부는 epithelial 표현형을 보유한다.

##### 패널별 설명
- **a**: Housekeeping, Gastric, Epithelial, Mesenchymal, Stem, Proliferation 마커 카테고리별 heatmap. 색상: log10(RPM+1); 적색 = 고발현, 청색 = 저발현. 대부분 CTC에서 mesenchymal 마커 적색, epithelial 마커 청색.
- **b**: 상피 유전자 발현 점수 (x축) vs. 간엽 유전자 발현 점수 (y축) scatter plot. AGS·N87 (AGS, N87 세포주) = 상피 방향; 대부분 CTC = 간엽 방향; SNU-1 = 중간. EMT 진행의 연속체적 분포 확인.
- **c**: EMT 모식도 — epithelial cancer cell (cytokeratin, EpCAM 등) → ZEB2/SNAI1 등에 의해 → mesenchymal cancer cell (vimentin, CDH11 등). 증식능력 감소 도해.

##### 해석 시 주의점
- EMT score는 선택된 마커 유전자 집합에 의존. 다른 마커 세트로 점수를 계산하면 결과가 달라질 수 있다.

---

#### Figure 4 — Gene expression and clustering of gastric CTCs

- **이 Figure가 필요한 이유**: Seurat UMAP 클러스터링으로 CTC의 전사체 기반 서브그룹 구조와 각 서브그룹의 characteristic gene 발현 패턴을 보여주기 위해 배치.
- **이 Figure가 뒷받침하는 주장**: 위암 CTC는 전사체 수준에서 최소 3개의 생물학적으로 구별되는 서브그룹으로 나뉜다.

##### 패널별 설명
- **a**: UMAP plot. 점: AGS (연어색), N87 (청색), SNU-1 (보라), CTC (녹색). CTC 대부분 Subgroup A + B; 세포주 대부분 Subgroup C.
- **b**: 각 서브그룹 상위 30개 과발현 유전자 heatmap. 보라 = 저발현, 노란색 = 고발현.
- **c**: 4가지 유전자 카테고리(EMT-related, Epithelial, Platelet-related, TGF-β stimulated) 바이올린 플롯. 각 서브그룹(A, B, C) 비교.

##### 본문에서 강조한 비교
- Subgroup A: ZEB2, MEF2D, NFKB1A, GATA1, GATA2, SERPINE1 고발현 (EMT 전사 인자군).
- Subgroup B: PF4, PPBP, ITGA2B, TGFB1, SPARC, ITGA2 고발현 (혈소판 관련).
- Subgroup C: EPCAM, KRT8, KRT10, KRT17, KRT18, KRT19 고발현; CDKN1A/CDKN1B TGF-β 하위 신호 발현은 Subgroup A + B에서 확인.

##### 해석 시 주의점
- 세포주(Subgroup C)와 실제 CTC(A, B)의 UMAP 분리는 세포주가 CTC를 대표하지 못함을 시사하지만, Subgroup C가 일부 CTC(epithelial CTCs)를 포함한다는 점도 주목해야 함.

---

#### Figure 5 — Comparison of Subgroup A and B

- **이 Figure가 필요한 이유**: A와 B 서브그룹 간 발현 유전자 수 및 GO 분석을 정량적으로 비교하여 두 서브그룹의 기능적 차이를 뒷받침하기 위해.
- **이 Figure가 뒷받침하는 주장**: Subgroup A는 전사 조절 활성이 높고, Subgroup B는 혈소판 기능 관련 GO 범주가 유의하게 농축된다.

##### 패널별 설명
- **a**: Subgroup A vs. B 발현 유전자 수(RPM > 1) 바이올린 플롯. Subgroup A 4805 ± 1412 genes > Subgroup B 2418 ± 845 genes.
- **b**: GO enrichment 결과 표. Subgroup A: transcription regulation (p = 2.08E-07, 8.55E-05), cancer transcriptional misregulation (p = 1.48E-07). Subgroup B: platelet degranulation (p = 1.64E-07), platelet aggregation (p = 0.0217).

##### 본문에서 강조한 비교
- nCount는 두 서브그룹 간 유의한 차이 없음 (Supplementary Fig. 5) → nFeature 차이가 read depth가 아닌 생물학적 차이.

##### 해석 시 주의점
- Subgroup B의 낮은 nFeature가 기술적 RNA 품질 저하 가능성을 완전히 배제하기 어렵다. nCount 비교만으로는 불충분.

---

## Tables

### Table 1 — Summary of patients (본문 p. 10)

- **이 Table이 필요한 이유**: 코호트의 임상 특성(성별, 나이, 전이 부위, 치료 이력, 반응성)을 제시하여 CTC 서브그룹과 임상 표현형의 연관성 해석 기반을 마련.
- **이 Table이 뒷받침하는 주장**: 연구 코호트는 진행성/전이성 위암 환자들로, 다양한 치료 이력과 전이 패턴을 보유.

#### 표 구조
- Row: 환자 ID (G1–G27)
- Column: Sex, Age, Metastasis site, Treatment at time of CTC collection, Response, Prior treatment

#### 핵심 수치
- 총 27명; 남 18명, 여 9명; 연령 52–81세.
- CTC 채취 시점에 화학요법 투여 중인 환자 24명; 미투여 3명.
- 반응 평가 가능 환자 중 Response로 분류: G9, G10, G14, G15, G19, G20, G24, G25, G26 등.
- PD (Progressive Disease) 환자: G1, G5, G11, G13.
- 전이 부위: 간, 복막, 식도, 폐, 췌장, 림프절 등 다양.

#### 본문에서 강조한 비교
- Subgroup A CTC가 검출된 환자들은 1차 치료 실패 후 장기 치료 이력(치료 교체 횟수)이 많은 경향 (Supplementary Table 3; Supplementary Fig. 7B).
- Subgroup C CTC(epithelial)를 보인 환자 G12, G25는 혈액 채취 후 각각 27일, 171일 생존 — n = 2로 결론 도출 제한적.

#### 해석 시 주의점
- 치료 반응 평가는 본문에서 일부 환자만 가능 (N/A 다수). Subgroup 임상 연관성 해석 시 치료 반응·N/A 환자 비율 고려 필요.

---

### Supplementary Table 1 — CTC subgroup classification and overall survival

- **이 Table이 필요한 이유**: 각 환자에서 Subgroup A, B, C CTC 수 및 사망 여부를 제시해 임상 예후와의 연관성을 평가하기 위한 핵심 데이터.
- **이 Table이 뒷받침하는 주장**: Subgroup C CTC가 검출된 환자는 불량 예후 가능성 시사.

#### 핵심 수치
- G12: Subgroup A=1, B=0, C=1, OS 27일, Death.
- G23: Subgroup A=10, B=0, C=1, OS 10일, Death.
- G2: Subgroup A=1, B=0, C=0, OS 880일, Live.
- G6: Subgroup A=2, B=0, C=0, OS 810일, Live.

#### 해석 시 주의점
- Subgroup C CTC 환자(G12, G23)에서 OS가 짧은 것은 n = 2에 불과. 인과성 해석은 극히 제한적.

---

### Supplementary Table 2 — List of overexpressed genes in each subgroup

- **이 Table이 필요한 이유**: 각 서브그룹의 상위 30개 과발현 유전자를 제시해 생물학적 기능 해석의 근거 마련.
- **핵심 내용**: 
  - Subgroup A: HHEX, MALAT1, NFKBIA, MEF2D, DENND4C, FAM65C, NEAT1 등 전사 조절 관련.
  - Subgroup B: PPBP, ACTB, FLNA, TMSB4X, PF4, CCL5, TREML1, MYL9 등 혈소판·세포골격 관련.
  - Subgroup C: MIEN1, S100A11, RPS 시리즈, RPL 시리즈, KRT19, HSP90AA1, HSPA8 등 대사·번역 관련.

---

## Supplementary Information

### Supplementary Figures (42003_2021_2937_MOESM1_ESM.pdf)

- **Supplementary Fig. 1**: WTA product 평균 길이 바이올린 플롯. 세포주(823–1360 bp 범위) 및 Gastric CTC (큰 변동폭). Gastric CTC에서 일부 >2000 bp 극단값 존재.
- **Supplementary Fig. 2**: NCI-H1975 total RNA를 Quartz-seq WTA — input RNA template(pg)와 cDNA yield(ng)의 선형 관계 확인 (n = 3, error bar = SD).
- **Supplementary Fig. 3**: GCM vs. micromanipulation 비교. A: yield p = 0.003 (GCM 우월). B: 평균 길이 p = 0.147 (차이 없음).
- **Supplementary Fig. 4**: 단일세포 library의 미토콘드리아 유전자 비율. Gastric CTC는 넓은 분포 (0–68.17%; 평균 5.07%; 중앙값 1.33%). >25% 기준으로 2개 세포 제거.
- **Supplementary Fig. 5**: Subgroup A, B, C 간 nCount vs. nFeature. nCount 차이 없음; nFeature: A > C > B.
- **Supplementary Fig. 6**: GO enrichment에서 확인된 유전자들의 서브그룹별 발현 바이올린 플롯. A: HHEX, LYST, MBTD1, MALAT1, MEF2D, PELI2. B: ACTB, TMSB4X, PPBP, FLNA, UBXN11, PF4.
- **Supplementary Fig. 7**: CTC 서브그룹 UMAP (A)과 치료 교체 횟수로 색상화한 UMAP (B). Subgroup A가 치료 교체 횟수 많은 환자에 집중.

### Supplementary Tables (42003_2021_2937_MOESM1_ESM.pdf)
- **Supplementary Table 1**: 환자별 CTC 서브그룹 수 + OS + Live/Death.
- **Supplementary Table 2**: 각 서브그룹 상위 30개 과발현 유전자 목록.
- **Supplementary Table 3**: 화학내성 관련 임상 정보 (치료 이력·교체 횟수; 본문 Fig. 7B 관련). 미제공: 본 보고서 작성 시 MOESM4 PDF 접근 가능 여부 확인 필요.

### Supplementary Data (MOESM3 xlsx)
- Supplementary Data 1–9 (Fig. 1B, 3A, 3B, 4B, 4C, 5A, 6 source data) — 정량 데이터.
- RNA-seq raw data: DRA011720 (DDBJ).

---

## 분석 자체에 대한 메모

- **누락 검증**: Subgroup A–화학내성 연관은 Supplementary Fig. 7B의 치료 교체 횟수 overlay와 Supplementary Table 3으로만 제시. 통계 검정(예: Kaplan–Meier, log-rank) 없이 시각적 관찰. 재현성 관련 별도 코호트 검증 없음.
- **후속 질문**: Subgroup B의 낮은 nFeature가 blood-borne platelet RNA 오염인지, 실제 CTC가 혈소판을 부착해 platelet RNA를 내재화한 것인지 구별 필요.
- **검토필요**: Supplementary Table 3 (화학내성 환자 임상 상세)은 MOESM4_ESM.pdf에 있을 것으로 추정 — 직접 확인 필요. 본 분석은 본문 기술과 Supplementary Table 1, 2에 근거.
