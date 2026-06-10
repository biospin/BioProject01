# hu-2021-cancer-surfaceome-atlas_core.md

## Executive Summary

- **무엇**: 암 세포 표면 단백체(surfaceome) 전체를 pan-cancer 규모로 체계화한 atlas — GESP(gene encoding surface protein) 3,567개를 정의하고, 발현·게놈 변이·세포 의존성·수용체-리간드 상호작용·면역 조절까지 통합해 치료 타깃 1,433개를 제시.
- **모델 / 방법**: 9개 독립 자원의 weighted vote로 core GESP score를 산출(score ≥ 4 기준), COMPARTMENT·GO·문헌 검색으로 세포내 단백질 제거 → 5개 알고리즘(SPM, TissueEnrich, pSI, SSEA, MWW)의 specificity score 합산으로 cancer-specific GESP(caGESP) 409개 식별.
- **핵심 결과**:
  - ① Pan-cancer GESP 3,567개 정의 — FDA 승인 CAR-T·ADC·항체 타깃의 97.0% 이상이 core GESP score ≥ 4 충족.
  - ② caGESP 409개 식별 (33개 암종, 중앙 16개/암종); 13.4% (55/409)는 현재 임상에서 CAR-T·ADC·항체 치료제로 개발 중.
  - ③ 'AND CAR-T' 전략 후보 쌍 179개, 'iCAR-T' 전략 후보 쌍 443개 pan-cancer 식별.
  - ④ 재발성 SCNA 보유 caGESP 989개 확인; 37.8% (54/143)는 CRISPR 기반 pan-cancer M-score 양성으로 세포 성장에 관련.
  - ⑤ 수용체-리간드 쌍 1,278개 예측 — 99.2%가 TCGA에서 유의하게 공동 발현.
  - ⑥ 치료 타깃 1,433개 식별; 86개/암종 평균 (범위: 15~205).
- **우리 적용**: caGESP 목록과 ADC 타깃 근거 데이터로 ADC 파이프라인 타깃 우선순위 결정에 직접 활용 가능 (`pipeline-applicable` + `BD-opportunity`). TCSA 포털(http://fcgportal.org/TCSA)에서 공개 데이터 접근 가능.
- **심층**: 한계·재현 ROI는 `hu-2021-cancer-surfaceome-atlas_lens-academic.md` / `hu-2021-cancer-surfaceome-atlas_lens-industry.md` / `hu-2021-cancer-surfaceome-atlas_methodology-brief.md` 참고.

---

## Identity

- **Title**: The Cancer Surfaceome Atlas integrates genomic, functional and drug response data to identify actionable targets
- **Authors**: Zhongyi Hu, Jiao Yuan, Meixiao Long, Junjie Jiang, Youyou Zhang, Tianli Zhang, Mu Xu, Yi Fan, Janos L. Tanyi, Kathleen T. Montone, Omid Tavana, Ho Man Chan, Xiaowen Hu, Robert H. Vonderheide, Lin Zhang
- **Year**: 2021
- **Venue**: Nature Cancer, Vol 2, pp. 1406–1422, December 2021
- **DOI**: 10.1038/s43018-021-00282-w
- **Citation key**: `@hu2021cancersurfaceomeatlas`
- **Document type**: Analysis (resource paper)
- **Received**: 14 January 2021; **Accepted**: 1 October 2021; **Published online**: 13 December 2021
- **Corresponding authors**: Xiaowen Hu (xiaowenh@upenn.edu), Robert H. Vonderheide (rhv@upenn.edu), Lin Zhang (linzhang@upenn.edu)

---

## Background

### 배경 스토리

- **문제의 출발점**: 세포 표면 단백질(SP, surface protein)은 세포 외부와의 통신을 제어하며, 영양·이온 수송, 수용체 신호전달, 면역 인식 등 핵심 기능을 담당한다. 적어도 FDA 승인 약물의 60% 이상이 SP를 타깃으로 하며, 현재 임상 개발 중인 CAR-T·ADC·항체 치료제의 직접 결합 대상이 SP다. 그러나 대부분 환자들이 이 치료들로 혜택을 보지 못하는 이유 중 하나가 종양 세포 표면에서 타깃화 가능한 단백질의 체계적 식별과 우선순위 결정이 어렵기 때문이다.

- **선행 접근 A — 단일 자원 기반 서페이스오믹스**: CSPA(cell surface protein atlas, mass spectrometry 기반), HPA(human protein atlas), TOPDB(topology DB)같은 실험적 자원과 SURFY·UniProt·COMPARTMENT 같은 계산 자원이 SP를 각각 독립적으로 식별·예측했다. 고처리량 전사체(GTEx n=7,429, TCGA n=9,807)와 단백체(CPTAC) 데이터, CRISPR 스크린(DepMap, Project Score)도 암종별 유전자 발현과 필수성 정보를 제공했다.

- **A의 한계**: 각 자원은 서로 다른 검출 원리를 갖기 때문에 커버리지와 false positive rate가 자원마다 다르다. 단일 자원 의존 시 불완전한 커버리지와 false positive가 불가피하다. 더 근본적으로는, 기존 접근들이 정상조직 대비 암 특이 발현의 체계적 계층화, 수용체-리간드 네트워크의 pan-cancer 정량화, 세포 필수성, 게놈 변이를 하나의 통합 체계로 묶지 못했다.

- **선행 접근 B — 부분 통합 분석**: GTEx·TCGA 기반 단일 암종 또는 일부 암종 대상 서페이스오믹스 연구들이 있었으나, 33개 암종 전체를 포괄하거나, CAR-T 조합 타깃(AND/iCAR-T logic gate)을 예측하거나, 약물 반응 데이터와 연결하는 단계에는 이르지 못했다.

- **이 논문으로 이어지는 gap**: 암종 전체를 포괄하는 단일 통합 surfaceome database, 암 특이 발현의 신뢰도 계층화, logic-gated CAR-T 설계를 위한 조합 타깃, 기능적 필수성과 게놈 변이를 통합한 치료 가능성 우선순위 배정 체계 — 이 모든 것의 공백이 본 논문의 동기다.

### 기본 개념

- **GESP (gene encoding surface protein)**: 세포 표면막에 적어도 1개의 아미노산이 노출된 단백질을 코딩하는 유전자. 4유형: ① integral bitopic/polytopic (세포 외부에 돌출, 다중 막관통), ② integral monotopic 외부면 (외부에만 위치), ③ integral monotopic 내부면 (내부막 면), ④ 다른 세포내 막 단백질 (Fig. 1a). 유형 ③과 ④는 일부 하류 분석(면역치료 타깃)에서 제외.

- **Core GESP score**: 9개 독립 자원에서 weight를 합산한 앙상블 신뢰도 점수. 실험적 자원이 높은 가중치(CSPA weight=3, HPA=2, TOPDB=2), 계산 예측은 낮은 가중치(SURFY=3, 나머지=1). 내부막 단백질은 음성 제어로 사용. Score ≥ 4 cutoff는 임상 타깃 97% 포함 + false positive/negative < 5% 기준으로 empirical 결정 (Fig. 1b,c).

- **caGESP (cancer-specific GESP)**: 특정 암종에서 정상조직 대비 선택적으로 발현되는 GESP. 5가지 독립 계산 알고리즘(SPM, TissueEnrich, pSI, SSEA, MWW)의 specificity score 합산으로 식별. Tier 1 (high confidence, stringent) / Tier 2 (moderate) / Tier 3 (less stringent) 3단계 신뢰도.

- **AND CAR-T / iCAR-T logic gate**: AND CAR-T는 종양 세포에서 두 caGESP가 동시에 발현될 때만 종양 세포 살상 — 단일 타깃의 'on-target off-tumor' 독성을 감소시키는 전략. iCAR-T는 inhibitory signaling domain을 이용해 caGESP가 정상조직에서 발현될 때 CAR-T 활성화를 억제하는 전략.

- **mIAM (membrane-bound immunological accessory molecule, 막 결합 면역 보조 분자)**: 생리적·병리적 조건에서 면역 반응을 조절하는 막 결합 단백질. GESP의 17.21%를 차지하며 종양 세포와 stromal cell 간 상호작용을 매개한다 (Fig. 1f).

### 이 논문의 필요성

- **핵심 이유**: 현재 임상에서 사용 중인 ADC·항체·CAR-T의 타깃이 전체 surfaceome의 2.5%에 불과하고, GESP의 66.8%가 기능 미탐구(understudied, Pubtator score < 150) 상태다.
- **기존 방법으로 부족했던 지점**: 암 특이 발현 신뢰도 계층화 체계 부재, 수용체-리간드 네트워크 pan-cancer 규모 정량화 미흡, CAR-T 조합 타깃 예측 방법론 부재.
- **이 논문이 해결하려는 방향**: 9개 자원 통합 GESP list + 33개 암종 pan-cancer 발현 특이성 + CRISPR 필수성 + 게놈 변이 + 약물 반응 + 수용체-리간드 네트워크를 하나의 공개 atlas(TCSA, http://fcgportal.org/TCSA)로 통합.

---

## Methods

### 이 method가 푸는 문제

- **Formal task**: 인간 게놈에서 GESP 전체를 정의하고, 33개 암종에서 암 특이적으로 발현되는 caGESP를 체계적으로 식별하며, 게놈 변이·세포 의존성·수용체-리간드 상호작용·약물 반응과 통합 분석.
- **입력**: 9개 surfaceome 자원 (실험적 3종 + 계산적 6종), TCGA RNA-seq (n=9,807), GTEx RNA-seq (n=7,429), CPTAC 단백체 (5개 암종), DepMap/Score CRISPR 스크린, TCGA 게놈(CNA, mutation, fusion), scRNA-seq (13개 암종), 수용체-리간드 데이터베이스 6종.
- **출력**: GESP 3,567개 목록, caGESP 409개 목록 (3-tier), AND CAR-T/iCAR-T 쌍, mIAM 614개, 치료 타깃 1,433개, TCSA 포털.
- **추정 대상**: 각 GESP의 표면 위치 신뢰도(core GESP score), 암종별 발현 특이성(specificity score), 수용체-리간드 쌍 신뢰도, 세포 성장 의존성.
- **중요한 hidden assumption**: mRNA 발현이 표면 단백질 발현을 대리한다고 간주. 면역세포 침윤이 발현 신호를 오염시킬 가능성이 있어 hematopoietic cell에서 고발현 GESP는 hematologic malignancy 이외 분석에서 제외.

### 확률 / 통계학적 구조

- **Model family**: 통합 가중치 투표(weighted vote ensemble) + 다중 알고리즘 rank aggregation. Bayesian generative model이 아닌 결정론적(deterministic) 파이프라인.

- **Core GESP score 산출**: 9개 자원의 weight 합산 점수. 실험적 증거(CSPA weight=3, HPA=2, TOPDB=2), 계산 예측(SURFY=3, UniProt=1, COMPARTMENT=1, PANTHER=1, HMPAs=1, Rabbits=1). 내부막 단백질은 음성 제어. Cutoff score ≥ 4는 known GESP·non-GESP·임상 타깃 분포를 사용해 empirically 결정 — false positive/negative 각각 < 5% (Fig. 1c).

- **caGESP specificity score**: 5개 알고리즘의 이진 결과를 합산:
  $$SS = \sum_{k=1}^{5} w_k, \quad w_k \in \{0, 1, 2\}$$
  $w_k = 2$ (stringent criteria 양성), $w_k = 1$ (less stringent 양성), $w_k = 0$ (음성). Cutoff $SS \geq 3$으로 caGESP 정의. Tier 1: 적어도 2개 알고리즘에서 stringent; Tier 2: 1개 stringent + 1개 less stringent; Tier 3: less stringent 3개 이상.

- **5개 특이성 알고리즘**:
  - **SPM** (TiSGeD v1.0 기반): 각 유전자의 관측 발현 패턴과 해당 암종에서만 완전히 발현되는 인위적 패턴 사이의 cosine 유사도. SPM > 0.99 → stringent, > 0.9 → moderate.
  - **TissueEnrich v1.0**: GeneRetrieval 함수 기반 fold change. 암종에서 모든 정상조직 대비 ≥ 5배 → stringent, 평균 이상 → moderate.
  - **pSI v1.1**: 암종 내 각 유전자 발현의 순위 기반 확률. pSI < 0.001 → stringent, < 0.01 → moderate.
  - **SSEA** (GSEA v1.17.0 기반): 암종 vs. 각 정상조직 쌍별 비교에서 normalized enrichment score로 차등 발현 평가. Percentile rank > 0.99 → stringent, > 0.9 → moderate.
  - **MWW test** (limma 기반): Mann-Whitney-Wilcoxon test로 암종 vs. 각 정상조직 발현 비교. 평균 percentile rank > 0.99 → stringent, > 0.9 → moderate.

- **AND CAR-T 쌍 priority score**: caGESP 쌍의 상호 배타성을 조직 수준 z-score로 정량화.
  $$\text{Priority score} = \sum_{k=1}^{29} |z_{1k} z_{2k}| \cdot w_k$$
  $$w_k = \begin{cases} 0 & \text{if } z_{1k} < 0 \\ 1 & \text{if } z_{1k} z_{2k} < 0 \\ -1 & \text{if } z_{1k} > 0, z_{2k} > 0 \end{cases}$$
  여기서 $z_{1k}$, $z_{2k}$는 조직 $k$에서 caGESP 쌍의 tissue-type-level z-score. 쌍이 높은 priority score → 더 좋은 AND CAR-T 후보.

- **iCAR-T 쌍 priority score**: 같은 구조이나 $w_k$ 부호 반전. ndGESP(정상조직에서만 발현)와 caGESP의 공동발현을 조직·샘플 수준에서 평가.

- **Receptor-ligand 통합 score**: DLRP·HPMR·IUHPAR (weight 2 each) + HPRD·STRING exp·STRING BINDING (weight 1 each). 합산 ≥ 2인 쌍을 후보로 선정. Pearson's test (표본 크기 ≥ 10, adjusted P < 0.05) 기반 공동발현 유의성 확인.

- **CRISPR 필수성**: DepMap + Project Score의 두 독립 CRISPR 스크린 통합 (Pacini et al. 방법). common essential (90th percentile 방법) 및 strongly selective (skewed-LRT > 100, bimodal-LRT > 125) 분류.

- **G-score (copy number)**: GISTIC v2.0.23으로 재발성 focal CNA 식별; pan-cancer G-score는 암종별 G-score 앙상블. Cutoff는 elbow method (증폭 0.62, 결실 0.73).

- **M-score (mutation)**: OncodriveFM + OncoDriveCLUST + ActiveDriver + HotSpot3D 기반 드라이버 돌연변이 예측. Pan-cancer M-score ≥ 0.10 cutoff (elbow method).

- **Noise, sparsity, uncertainty 처리**: Hematopoietic malignancy 분석 시 면역세포 오염 제거 목적으로 30개 hematopoietic 조직 유형 RNA-seq 활용. Spearman/Pearson correlation에 BH FDR 보정. TCGA 분석 시 한 환자에 복수 프로파일이 있으면 단일 파일 선택 규칙 적용.

### 핵심 method insight

- **기존 방법의 한계**: 단일 자원 기반 서페이스오믹스는 커버리지 불완전 + false positive 과다. 암 특이성 분석 시 단일 알고리즘 의존으로 노이즈 취약. CAR-T 타깃 선택이 단일 단백질 발현 수준에 머물러 'on-target off-tumor' 독성 해결 불가.
- **이 논문이 바꾼 가정**: Weighted ensemble로 커버리지-특이성 trade-off 완화. caGESP 신뢰도를 연속 점수 대신 3-tier로 계층화해 연구자 활용 유연성 확보. 두 표면 단백질의 조합 발현 패턴이 단일 단백질보다 암 특이성이 높다는 Boolean logic gate 가정 도입.
- **새로 추가한 변수 또는 구조**: mIAM 서브셋 체계화, AND/iCAR-T 쌍 priority score, G-score/M-score/fusion score의 pan-cancer 통합, scRNA-seq 기반 미세환경 내 발현 특이성.
- **이 변화가 중요한 이유**: 임상 개발 중인 타깃의 13.4%를 atlas가 독립적으로 재발굴 → approach의 높은 precision 확인. 나머지 86.6%는 신규 후보.

### 이전 방법과의 차이

- **Baseline**: Bausch-Fluck et al. 2018 (*Proc. Natl Acad. Sci. USA*) in silico human surfaceome (SURFY 기반). 단일 계산 자원, 발현 특이성·게놈 변이·임상 연결 없음.
- **공통점**: SP 예측에 UniProt topology annotation 활용.
- **차이점**: 본 논문은 실험적 mass spectrometry 자원(CSPA, HPA) 포함 + 9개 자원 ensemble로 커버리지와 신뢰도 동시 향상. 발현·게놈·기능·약물 반응의 다차원 통합.
- **차이가 크게 나타나는 조건**: Hematologic malignancy에서 면역세포 오염 처리가 필요한 경우, logic-gated CAR-T 설계처럼 다중 타깃 조합이 필요한 경우.

### 효과가 Results에서 나타난 방식

- Core GESP score ≥ 4 cutoff: FDA 승인/임상 중인 CAR-T·ADC·항체 타깃의 97.0%를 포함 (Fig. 1c).
- caGESP 식별 5-알고리즘 합산: 기존 임상 caGESP 55/409 (13.4%) 재발굴 — 알고리즘 독립적 validation.
- AND CAR-T 쌍 priority score: PAAD에서 MSLN-TM4SF4, LIHC에서 GPC3-TM4SF5 같은 암 특이성 높은 쌍 확인.
- 수용체-리간드 쌍: 1,278쌍 중 99.1%/99.2% (GTEx/TCGA)에서 유의한 공동발현 확인 (Pearson's, adjusted P < 0.05).

### Method 관점의 한계

- mRNA-단백질 상관이 모든 GESP에서 동일하지 않음 (GESP에서 positive correlation 41.0% vs. non-GESP 25.2% — 개선되었지만 완전하지 않음).
- 5개 특이성 알고리즘이 모두 발현 데이터 기반 — 단백질 번역 후 변형(glycosylation, shedding, cleavage)은 반영 안 됨.
- in vitro CRISPR 스크린 기반 필수성은 in vivo 종양 미세환경에서 다를 수 있음.
- 정상 testis 조직 RNA-seq 제외로 cancer-testis 항원 오염을 줄였지만, TGCT 분석에서는 포함해 일관성 주의.

---

## Results

### Dataset별 결과

#### Dataset 1 — GESP 정의 (GTEx + TCGA + 9개 surfaceome 자원)

- **Dataset**: GTEx (n=7,429, 30개 조직 유형), TCGA (n=9,807, 33개 암종), 9개 surfaceome 자원.
- **목적**: 인간 게놈에서 GESP 정의 및 core score cutoff 설정.
- **사용한 데이터 규모**: ENSEMBL GENCODE v.23 기반 전체 단백질 코딩 유전자 → 후보 3,933개 → 최종 GESP 3,567개.
- **주요 수치**: 3,567개 GESP; GPCR 23.1%, mIAM 17.21%, ion channel 9.8%, kinase 3.36%, enzyme 9.81%, transporter 8.83% (Fig. 1e). FDA 임상 타깃의 97.0%가 core GESP score ≥ 4.

#### Dataset 2 — 발현 특성 분석

- **Dataset**: GTEx (n=7,429) + TCGA (n=9,807) RNA-seq; CPTAC 단백체 (5개 암종).
- **목적**: GESP 발현의 암 특이성 및 mRNA-단백질 상관 확인.
- **주요 수치**:
  - Ubiquitous 발현 GESP: 22.1%; non-GESP: 48.4%.
  - Tissue specificity index (tau value) 기반 cancer-type-specific: GESP 44.5% vs. non-GESP 24.1% (OR=2.5, P=7.4×10⁻⁹⁸; Fig. 2d).
  - mRNA-단백질 positive Spearman correlation: GESP 41.0% vs. non-GESP 25.2% (OR=2.2, P=1.2×10⁻¹⁹; Fig. 2j).
  - GSEA에서 positively correlated genes이 GESPs 및 peroxisome 위치 유전자 집합에서 유의하게 농축 (1,000 permutation, gene set size 및 다중 비교 보정 후; Fig. 2k).
- **통계**: Fisher's exact test (양측), BH correction 적용.
- 해석: OR=2.2의 mRNA-단백질 상관은 GESPs에서 전반적으로 우수하지만 개별 유전자 수준에서는 예외가 상당 — 단백체 검증이 고우선순위 타깃에 권장.

#### Dataset 3 — caGESP 409개 식별

- **Dataset**: TCGA (n=9,807) + GTEx (n=7,429); hematopoietic cell RNA-seq 30개 조직.
- **목적**: 암종 특이적으로 발현되는 GESP 식별 및 신뢰도 계층화.
- **주요 수치**:
  - 409개 unique caGESP; 암종당 중앙값 16개 (Fig. 3c).
  - 13.4% (55/409)가 CAR-T·ADC·항체 임상 개발 중 (Fig. 3f).
  - 26.4% (128/409)가 2개 이상 암종에서 공유 (Fig. 3b) — 공통 oncogenic 신호 시사.
  - CLDN6(OV, TGCT, UCS), CEACAM5(COAD, READ, STAD, ESCA, PAAD), CD276(SARC)이 대표 caGESP로 제시 (Fig. 3e).

#### Dataset 4 — Logic-gated CAR-T 쌍 예측

- **Dataset**: GTEx (n=7,429), TCGA caGESP 발현 데이터.
- **목적**: 'on-target off-tumor' 독성 최소화 AND CAR-T 및 iCAR-T 후보 쌍 식별.
- **주요 수치**:
  - AND CAR-T: 179개 unique 쌍 (15개 암종, 평균 12쌍/암종; Fig. 4d). 대표: MSLN-TM4SF4 for PAAD, GPC3-TM4SF5 for LIHC.
  - iCAR-T: 443개 unique 쌍 (21개 암종, 평균 25쌍/암종; Fig. 4h). 대표: CA9-SLC26A9 for KIRC, GPA33-TMIGD1 for chronic obstructive airway disease.

#### Dataset 5 — 재발성 게놈 변이

- **Dataset**: TCGA 게놈 (CNA: SNP array n=10,950; mutation: WES n=10,224; fusion: RNA-seq n=9,799).
- **목적**: 암 드라이버로서 GESP의 재발성 변이 특성화.
- **주요 수치**:
  - SCNA: 989/3,567 GESP에서 재발성 CNA; 50.2% (497/989)는 단일 암종 특이.
  - Pan-cancer G-score (증폭/결실) 양성: 19.8% (200/989), 113개 증폭 + 81개 결실.
  - Recurrent mutation GESP: 143개; 73.4% (105/143)는 단일 암종 특이. GNAQ는 UVM에서 50% mutation frequency.
  - Pan-cancer M-score ≥ 0.10: 54/143 (37.8%); CTNNB1, EGFR, FAT1, GNAQ 최고 순위 (Fig. 5c).
  - Recurrent GESP fusions: 484/6,280 (7.7%); 임상 cutoff 충족 86/1,771 GESPs (4.9%). TMPRSS2-ERG (n=177), FGFR3-TACC3 (n=36), NCOR2-SCARB1 (n=12), CCDC6-RET (n=12), ETV6-NTRK3 (n=10) (Fig. 5d).
  - 재발성 돌연변이의 지배적 유형: missense (37.3~85.7%); 지배적 재발성 돌연변이 유형: heterozygous (56.9~92.8%).
  - ABSOLUTE 기반 41.5% 이상 재발성 돌연변이가 early event; 52.5% 이상이 clonal alteration.

#### Dataset 6 — CRISPR 세포 성장 의존성

- **Dataset**: DepMap + Project Score (n=1,200 cancer cell lines, 28개 암종).
- **목적**: GESP의 세포 필수성 특성화.
- **주요 수치**:
  - GESP 중 common essential + strongly selective: 4.1% vs. non-GESP 14.0% — GESP 대부분 세포 성장에 비필수 (Extended Data Fig. 8a).
  - 필수 GESP 중 mRNA 발현-의존성 유의하고 양의 상관: 43/117 (36.8%). 이 중 7개는 재발성 증폭 + copy number와 양의 상관.
  - FDA 승인 anticancer drug 타깃 3개 GESP 포함 (Extended Data Fig. 8d).

#### Dataset 7 — 수용체-리간드 상호작용 네트워크

- **Dataset**: 6개 DB 통합 + DeepLoc 기반 예측.
- **목적**: 암에서 탈조절된 수용체-리간드 쌍 식별.
- **주요 수치**:
  - 1,278쌍 예측 (통합 score ≥ 2). 수용체 1개당 평균 2.8개 리간드 (범위 1~22); 리간드 1개당 평균 2.7개 수용체 (범위 1~13).
  - 99.1% (1,267/1,278) + 99.2% (1,268/1,278)쌍이 각각 GTEx·TCGA에서 유의한 공동발현 (Pearson's, adjusted P < 0.05, n ≥ 10; Fig. 6e,f).
  - 166개 caGESP-associated 수용체-리간드 쌍. CD70-CD27 (KIRC), ULBP2-KLRK1 (HNSC) — 임상 CAR-T 개발 중인 2쌍 포함 (Fig. 6h).

#### Dataset 8 — mIAM 특성화 및 scRNA-seq

- **Dataset**: scRNA-seq 13개 암종 (Supplementary Table 5); 614개 mIAM; cancer cell line n=1,200 (28개 암종).
- **목적**: 종양 미세환경에서 mIAM의 세포 유형별 발현 및 IFN 신호 연관성 확인.
- **주요 수치**:
  - 488/614 (79.5%) mIAM이 암 세포주에서 발현 (>5% 세포); 126 (20.5%)은 undetectable.
  - 72.3% (444/614)는 selectively expressed; 7.2% (44/614)는 ubiquitous.
  - ISG 양성 상관 mIAM 비율이 게놈 전체보다 유의하게 높음 (OR=1.5, P=1.9×10⁻⁴; Fig. 7h). 112개 mIAM에서 ISG 양성 상관 농축.
  - Co-stimulatory/co-inhibitory 분자가 ISG와 강하게 연관 (Fig. 7i).

#### Dataset 9 — 치료 타깃 1,433개 및 TCSA

- **Dataset**: TCGA 33개 암종; Open Targets, PHAROS, FDA 승인 anticancer drug 162개.
- **목적**: 치료 타깃으로서 GESP 종합 평가 및 TCSA 포털 구축.
- **주요 수치**:
  - FDA 승인 anticancer immune/targeted drug 중 64.8% (105/162)가 GESPs 직접 타깃. 세부: CAR-T 100%, ADC 100%, antibody drug 82.8%, small molecule 47.7% (Fig. 8b).
  - 현재 drug target: 전체 surfaceome의 2.5%에 불과.
  - 치료 타깃 후보 1,433개; 33개 암종; 평균 86개/암종 (범위 15~205; Fig. 8d,e).
  - Open Targets 기준 druggable GESP: ~36.0%가 small molecule 타깃 가능성 (10.5% Clinical_Precedence, 14.0% Discovery_Precedence, 11.0% Predicted_Tractable; Fig. 8a).
  - PHAROS 기준 66.8%가 understudied (Pubtator score < 150).

### 전체 결과 요약

- **반복적으로 관찰된 패턴**: GESPs는 non-GESPs 대비 더 암 유형 특이적 발현, 더 높은 mRNA-단백질 상관, 더 낮은 세포 필수성(in vitro)을 일관되게 보임.
- **가장 중요한 수치**: 현재 전체 surfaceome의 2.5%만 anticancer drug 타깃 → 1,433개 신규 후보 제시로 탐색 공간 대폭 확장.
- **Baseline 대비 차이**: Bausch-Fluck et al. 2018 단일 계산 자원 대비 9개 자원 통합으로 실험적 evidence 기반 커버리지 확장 + 임상 개발 타깃 97% 재발굴로 precision 확인.
- **결과 해석 시 주의점**: mRNA-단백질 상관 불완전; 2D 세포주 기반 CRISPR 필수성은 in vivo와 다를 수 있음; 발현 atlas는 기능적 검증을 대체하지 않음. 무작위화/블라인딩 해당 없음 (순수 계산 연구).

---

## Figures

### Figure 1

- **이 Figure가 필요한 이유**: GESP 정의 체계와 core GESP score 산출 워크플로우를 보여주어, atlas 전체의 자원 신뢰도를 투명하게 제시하고 임상 타깃 포함률로 cutoff를 정당화.
- **이 Figure가 뒷받침하는 주장**: 9개 자원 weighted vote로 GESP를 정의하면 임상 타깃의 97%를 포함하는 high-precision list를 얻을 수 있다.

#### 패널별 설명
- **a**: 세포막 단백질 4유형 모식도.
- **b**: 9개 자원의 weight 및 워크플로우 다이어그램 (CSPA weight=3, HPA=2, TOPDB=2, SURFY=3, 나머지=1).
- **c**: Core GESP score 분포 (known GESPs, non-GESPs, CAR-T/ADC/antibody 타깃). Score ≥ 4에서 97% 임상 타깃 포함.
- **d**: 9개 자원 기준 2,872개 유전자 히트맵 — known GESP·non-GESP·임상 타깃 위치 시각화.
- **e**: GESP 기능군 파이차트 (GPCR 23.1%, mIAM 17.21%, IC 9.8%, enzyme 9.81%, kinase 3.36%, transporter 8.83%, Other 47.5%).
- **f**: mIAM 기능군별 Scaled Venn diagram.

#### 본문에서 강조한 비교
- Known GESP vs. non-GESP vs. 임상 타깃의 core GESP score 분포. Score ≥ 4에서 false positive/negative 각각 < 5%.

#### 해석 시 주의점
- Cutoff 4는 empirical 결정. 새 실험 데이터 추가 시 재보정 필요.

---

### Figure 2

- **이 Figure가 필요한 이유**: GESP의 mRNA-단백질 상관 및 암 특이성이 non-GESP보다 유의하게 높다는 두 가지 주장을 다차원 데이터로 입증해, RNA-seq 기반 caGESP 식별의 생물학적 valid성을 지지.
- **이 Figure가 뒷받침하는 주장**: mRNA expression of GESPs can be used to predict protein expression across cancers; GESPs are significantly more cancer-type specific than non-GESPs.

#### 패널별 설명
- **a,b**: GTEx (n=7,429)·TCGA (n=9,807) RNA-seq 샘플 구성 버블차트.
- **c**: 0~6, 7~25, 26~33개 암종에서 검출 가능한 유전자 비율 — GESPs vs. non-GESPs.
- **d**: Tau value 분포 히스토그램 — GESPs 44.5% vs. non-GESPs 24.1% (OR=2.5, P=7.4×10⁻⁹⁸).
- **e,f**: 세포내 위치별 암 특이 유전자 비율 및 OR bubble plot.
- **g**: t-SNE — pan-TCGA + GTEx 발현 기반 조직 클러스터링.
- **h**: 전립선암 t-SNE 클로즈업 (GTEx 정상, 종양 인접, 종양 명확 분리).
- **i**: Spearman correlation mRNA vs. 단백질 (5개 암종 CPTAC).
- **j**: GESPs vs. non-GESPs positive Spearman correlation 비율 히스토그램 — OR=2.2, P=1.2×10⁻¹⁹.
- **k**: 세포내 위치별 enrichment score bubble plot — GESPs + peroxisome 유의 농축.

#### 본문에서 강조한 비교
- mRNA-단백질 positive correlation: GESP 41.0% vs. non-GESP 25.2%. GSEA (1,000 permutation)에서 GESPs 및 peroxisome 유전자 집합에서 통계적 농축 확인.

#### 해석 시 주의점
- OR=2.2이지만 overlap 상당. 상관 관계는 인과 관계가 아님.

---

### Figure 3

- **이 Figure가 필요한 이유**: caGESP 식별 워크플로우와 결과를 제시해 atlas의 핵심 출력물(409개 caGESP + 3-tier 신뢰도)의 근거를 보여줌.
- **이 Figure가 뒷받침하는 주장**: 5-알고리즘 앙상블이 임상 개발 중인 타깃을 재발굴(13.4%)하며, tier-1 caGESP가 가장 높은 임상적 관련성을 가진다.

#### 패널별 설명
- **a**: caGESP 식별 워크플로우 — TCGA + UCSC Toil RNA-seq → 5개 알고리즘 → specificity score → hematopoietic 제외.
- **b**: 409개 caGESP의 암종 간 공유 수 분포 — 128개 (26.4%)가 ≥ 2개 암종 공유.
- **c**: 암종별 caGESP 수 및 tier 비율.
- **d**: GTEx vs. TCGA 발현 히트맵 — caGESP tier별 발현 abundance.
- **e**: CLDN6, CEACAM5, CD276 발현 프로파일 (정상 GTEx vs. 암종별 FPKM).
- **f**: 33개 암종별 caGESP 목록과 임상 개발 현황 bubble plot.

#### 본문에서 강조한 비교
- Tier 1 중 55/409 (13.4%)가 이미 임상에서 개발 중. CLDN6, CEACAM5, CD276이 대표 예시.

#### 해석 시 주의점
- 5-알고리즘 all-transcriptomic 접근 — 발현만으로 확인. 기능적 표면 접근성 및 단백질 수준 미검증.

---

### Figure 4

- **이 Figure가 필요한 이유**: 단일 caGESP 타깃의 'on-target off-tumor' 독성 한계를 극복하는 logic-gated CAR-T 전략을 정량적으로 지원.
- **이 Figure가 뒷받침하는 주장**: 발현 배타성 기반 caGESP 쌍 탐색으로 AND CAR-T 및 iCAR-T 설계의 체계적 후보 제공 가능.

#### 패널별 설명
- **a**: AND CAR-T logic gate 모식도 (truth table 포함).
- **b,c**: AND CAR-T 쌍 발굴 워크플로우 및 대표 사례 (MSLN-TM4SF4 for PAAD, GPC3-TM4SF5 for LIHC) 발현 box plot.
- **d**: AND CAR-T 쌍 암종별 분포 (179쌍).
- **e,f**: iCAR-T logic gate 모식도 및 워크플로우.
- **g**: iCAR-T 후보 쌍 대표 사례 (CA9-SLC26A9 for KIRC, GPA33-TMIGD1).
- **h**: iCAR-T 쌍 암종별 분포 (443쌍).

#### 본문에서 강조한 비교
- AND CAR-T: caGESP가 암종에서 공동발현 + 정상조직에서 상호 배타적 발현이 핵심 선택 기준. Priority score로 정량화.

#### 해석 시 주의점
- 발현 배타성이 in vitro/in vivo 기능적 특이성을 보장하지 않음. 조합 타깃의 실제 AND gate 효율은 별도 검증 필요.

---

### Figure 5

- **이 Figure가 필요한 이유**: 게놈 변이(SCNA, 돌연변이, fusion)가 caGESP에서 어떻게 농축되는지 보여줘 발현 데이터 외 암 드라이버 evidence 추가.
- **이 Figure가 뒷받침하는 주장**: 재발성 게놈 변이를 보이는 caGESP가 치료적으로 actionable하다.

#### 패널별 설명
- **a,b**: SCNA G-score (copy gain/loss) bubble plot — 암종 × 타깃 유전자.
- **c**: Mutation M-score bubble plot — CTNNB1·GNAQ·ERBB2·EGFR 강조.
- **d**: Fusion event 수 bubble plot — TMPRSS2 압도적 최다.

#### 본문에서 강조한 비교
- GNAQ는 UVM에서 50% mutation frequency — 극단적 암 특이성. ERBB2는 11개 암종에서 재발성 증폭.

#### 해석 시 주의점
- G-score/M-score는 통계적 재발성 기준. 특정 환자에서 functional impact는 별도 검증 필요.

---

### Figure 6

- **이 Figure가 필요한 이유**: GESP의 수용체로서 기능에 초점을 맞추어, 암에서 극적으로 탈조절된 수용체-리간드 네트워크를 정량화.
- **이 Figure가 뒷받침하는 주장**: 세포간 통신이 종양형성 중 극적으로 변화하며, 이를 정량화하면 ligand-based 타깃 발굴이 가능하다.

#### 패널별 설명
- **a**: GESP 수용체와 리간드 (soluble + cell membrane-associated) 모식도.
- **b**: 6개 DB 통합 워크플로우 및 통합 score.
- **c,d**: 수용체당 리간드 수, 리간드당 수용체 수 density cloud/bar plot.
- **e**: TCGA 종양·인접 정상·GTEx 정상 조직별 수용체-리간드 쌍 발현 수 violin plot.
- **f**: 수용체-리간드 공동발현 unsupervised cluster heatmap — 종양과 정상조직 뚜렷한 분리.
- **g**: caGESP 수용체-리간드 쌍 Circos plot.
- **h**: CAR-T 임상 개발 사례 2쌍 (CD70-CD27 for KIRC, ULBP2-KLRK1 for HNSC) 발현.

#### 본문에서 강조한 비교
- 99.1%/99.2%의 수용체-리간드 쌍이 GTEx/TCGA에서 유의한 공동발현 → atlas 생물학적 validity 지지.

#### 해석 시 주의점
- Pearson's test 기반 공동발현은 상관이지 기능적 상호작용 증명이 아님.

---

### Figure 7

- **이 Figure가 필요한 이유**: mIAM의 scRNA-seq 기반 세포 유형별 발현과 IFN 신호 연관성을 보여줘 종양 면역 조절에서 mIAM의 역할을 지지.
- **이 Figure가 뒷받침하는 주장**: mIAM은 종양 세포에서 IFN 신호와 유의하게 연관되며, costimulatory/co-inhibitor 분자가 그 중심에 있다.

#### 패널별 설명
- **a-c**: macrophage/DC, stromal, 종양 세포에서 614개 mIAM의 Spearman correlation heatmap.
- **d**: 종양 세포 vs. stromal 세포의 Spearman correlation 분포 비교 — 종양 세포 이질성 높음.
- **e**: mIAM 발현 분포 유형 분류 (ubiquitous 7.2%, selectively expressed 72.3%).
- **f**: PRLR (lineage-enriched), CD274/PD-L1 (right-skewed), IL15RA (bimodal-like) 대표 발현 density plot.
- **g,h**: mIAM-신호경로 correlation heatmap + ISG 연관 volcano plot.
- **i**: ISG 양성 mIAM의 기능군 enrichment.
- **j,k**: ISG 양성 mIAM의 기능군 (Venn + bubble plot).
- **l**: CellPhoneDB 기반 BRCA에서 세포 유형별 mIAM 매개 상호작용 수 (Circos).

#### 본문에서 강조한 비교
- mIAM-ISG 양성 상관 비율이 게놈 전체보다 유의하게 높음 (OR=1.5, P=1.9×10⁻⁴). Co-stimulatory/co-inhibitory 분자가 ISG 신호와 강하게 연관.

#### 해석 시 주의점
- scRNA-seq 기반이므로 낮은 coverage 가능성. CellPhoneDB 예측은 in silico — 실험 검증 필요.

---

### Figure 8

- **이 Figure가 필요한 이유**: TCSA atlas의 임상적 활용 가능성을 FDA 승인 약물·임상 개발 약물 분석과 TCSA 포털 소개로 직접 연결.
- **이 Figure가 뒷받침하는 주장**: 현재 drug target으로 쓰이는 GESPs가 전체 surfaceome의 2.5%에 불과하므로 신규 1,433개 후보의 임상적 잠재력이 크다.

#### 패널별 설명
- **a**: Open Targets + PHAROS 기반 druggability 분류 river plot (GESPs 35.9% clinical/discovery/predicted).
- **b**: FDA 승인 + 임상 개발 anticancer drug 중 GESP 직접 타깃 비율 (CAR-T 100%, ADC 100%, antibody 82.8%, small molecule 47.7%).
- **c**: FDA 승인/임상 개발 약물 타깃 vs. GESP 전체 Venn diagram.
- **d**: FDA 승인/임상 개발/신규 타깃에서 게놈-기능 특성 분포 sunburst chart.
- **e**: 33개 암종별 치료 타깃 수 bubble map.
- **f**: TCSA 포털 구조 개요.

#### 본문에서 강조한 비교
- FDA 승인 162개 anticancer drug 중 64.8%가 GESPs를 직접 타깃. 그러나 현재 사용 중인 타깃은 전체 surfaceome의 2.5%에 불과.

#### 해석 시 주의점
- 'Druggable' 판정은 bioinformatic 예측 기반. 1,433개 신규 타깃은 후보 목록이며 기능 검증 없음.

---

## Tables

본문에 정식 Table 없음.

주요 데이터는 Supplementary Tables (xlsx, MOESM2-14)에 수록:
- **Supp. Table 1**: GESP 식별에 사용된 9개 자원 목록.
- **Supp. Table 2**: GESP 3,567개 전체 목록 + core GESP score.
- **Supp. Table 3,4**: RNA-seq 샘플 수 (GTEx, TCGA).
- **Supp. Table 5**: scRNA-seq 13개 암종 데이터셋 목록.
- **Supp. Table 6**: scRNA-seq 세포 유형별 GESP 발현.
- **Supp. Table 7**: CPTAC 단백체 데이터 목록.
- **Supp. Table 8**: caGESP 식별 알고리즘 파라미터.
- **Supp. Table 9**: caGESP 409개 목록 (3-tier + 암종별).
- **Supp. Table 10,11**: AND CAR-T / iCAR-T 쌍 목록.
- **Supp. Table 12,13**: SCNA G-score + pan-cancer G-score.
- **Supp. Table 14,15**: GESP 돌연변이 목록 + hotspot mutation.
- **Supp. Table 16,17,18**: M-score, mutation type, clonal status.
- **Supp. Table 21,22**: Fusion transcript 데이터.
- **Supp. Table 23**: 재발성 GESP fusion 목록.
- **Supp. Table 24,25**: DepMap/Score CRISPR 데이터.
- **Supp. Table 26**: GESP essential 분류.
- **Supp. Table 28**: 재발성 증폭 + 의존성 상관 GESPs.
- **Supp. Table 29,30,31**: 수용체-리간드 DB, 예측 쌍 목록.
- **Supp. Table 32**: mIAM 발현 분류.
- **Supp. Table 34**: ISG 연관 mIAM.
- **Supp. Table 36,37,38**: PHAROS/Open Targets druggability, FDA/임상 약물 목록.
- **Supp. Table 39,40**: 암종별 치료 타깃 목록.

---

## Supplementary Information

- **MOESM1 (Reporting Summary, 5 pages)**: Nature Portfolio 표준 Reporting Summary. 통계 보고 확인: 정확한 n 명시, 통계 검정 기술, 다중 비교 보정, effect size 추정 포함. 소프트웨어: GISTIC v2.0.23, HAPSEG v1.1.1, ABSOLUTE v1.0.6, MutSigCV v1.4, OncoDriveFM v1.0.1, ActiveDriver v0.10, HotSpot3D v0.0.10; SPM (TiSGeD v1.0), TissueEnrich v1.0, pSI v1.1, SSEA (GSEA v1.17.0), MWW (limma); scMatch v1.0, LTMG v1.0, CellPhoneDB v2.1.4. 데이터: 모두 공개 DB(TCGA, GTEx, CPTAC, DepMap 등). 재현 불가 실험 없음 (순수 계산 연구). Sample size는 사용 가능한 DB 케이스 수로 결정 (통계적 선결 없음).
- **MOESM2-14 (xlsx Supplementary Tables)**: 위 Tables 섹션 참조. TCSA 포털 (http://fcgportal.org/TCSA)에서 모든 데이터 공개.
- **Extended Data Figures 1-9**: 본문 주요 분석의 보완 결과 — GESP 계층별 발현, 세포 필수성 세부 분석, iCAR-T 추가 사례, 수용체-리간드 클러스터 등. 코드: https://github.com/fcgportal/TCSA.

---

## 분석 자체에 대한 메모

- **mRNA proxy 한계**: 단백질 발현 상관이 41%에 그치는 만큼, 고우선순위 caGESP는 단백체 수준 검증이 필요. CPTAC 데이터가 5개 암종에 한정되어 나머지 28개 암종은 단백체 gap이 있다.
- **scRNA-seq 커버리지**: 13개 암종에서만 수집된 scRNA-seq data는 mIAM 분석의 암종 커버리지를 제한. Bulk RNA-seq 결과와의 일관성 추가 확인 권장.
- **Logic-gated CAR-T 기능 검증 부재**: AND CAR-T 및 iCAR-T 후보 쌍 선정이 발현 배타성에만 기반. 실제 AND-gate 신호 효율 및 in vivo 특이성은 실험 검증 미완.
- **재현**: 코드는 https://github.com/fcgportal/TCSA 공개. 데이터는 TCGA/GTEx/CPTAC 공개 포털. 주요 소프트웨어 버전이 Reporting Summary에 명시되어 있어 재현성 수준 높음.

---

## Executive Summary

- **무엇**: 외부 맥락: 범-암종 세포 표면 단백체(surfaceome) atlas — 게놈(TCGA), 단백체(CPTAC), 이미징(HPA) 데이터를 통합하여 암 표면 단백질 지형도를 구축. 각 표면 단백질의 종양 선택성, 정상 조직 발현, 면역 연관성을 정량화.
- **핵심 발견**: 외부 맥락: 2,886개 surfaceome 단백질 중 암종별 선택적 발현 패턴 규명. 기존 알려진 ADC/치료 타겟(HER2, EGFR 등) 외 신규 표면 단백질 후보 발굴. 구체 수치: 미제공.
- **우리 적용**: (1) NCCHE Gastric / SEV BRCA CTC 발현 표면 단백질의 외부 검증 기준 atlas. (2) CytoGen Tier 분류에서 ADC-Ready / Promising 타겟의 surfaceome 선택성 점수 비교. (3) 범-암종 데이터베이스로 NCCHE 다중 암종(위암/췌장암/대장암/담도암) 각각의 타겟 우선순위화에 활용.

---

## Identity

- **Title**: Cancer Surfaceome Atlas integrates genomic, proteomic and imaging data
- **Authors**: Hu, Z. et al. (full 저자 목록: 미제공 — 전문 확인 필요)
- **Venue / Year**: *Cancer Cell*, 2021.
- **Funding**: 미제공.
- **COI**: 미제공.
- **Citation key**: `hu2021cancersurfaceomeatlas`
- **주의**: sources/abstract.txt의 DOI(10.1016/j.ccell.2022.10.021)는 Strand 2022 DCIS Cancer Cell 논문으로 오기재. 실제 Hu 2021 Cancer Surfaceome Atlas 논문의 DOI 별도 확인 필요.

---

## Background

- 외부 맥락: 세포 표면 단백질(surfaceome)은 전체 인간 proteome의 약 26%를 차지하며, 항체 접근성이 있어 ADC, CAR-T, 이중특이항체 등 다양한 항암 모달리티의 타겟이 됨.
- 외부 맥락: 기존 암 유전체 연구(TCGA)는 전사체/유전체 중심 — 표면 단백질의 실제 발현 수준과 종양 선택성을 직접 측정한 통합 자원이 부족했음.
- 외부 맥락: CPTAC(Clinical Proteomic Tumor Analysis Consortium) 데이터와 Human Protein Atlas(HPA) 이미징 데이터를 게놈 데이터와 통합하면 RNA-protein 상관성 한계를 극복하고 실제 표면 단백질 발현을 보다 정확히 추정 가능.
- 이 연구의 필요성: ADC 타겟 발굴 및 면역항암 전략 설계를 위한 체계적 surfaceome 참조 자원 구축.

---

## Methods (abstract 범위)

- 미제공 — 전문 PDF 미확보. 외부 맥락: 예상 방법:
  - TCGA 전사체 데이터: 범-암종 surfaceome 유전자 발현 정량
  - CPTAC 단백체 데이터: RNA 발현과 단백질 발현 상관성 검증
  - HPA 단백질 이미징: 조직 수준 단백질 발현 패턴 시각화
  - 정상 조직 대비 종양 발현 비교: 종양 선택성 점수화
  - Surfaceome 정의: Almen 2009 등 기존 surfaceome 데이터베이스 참조
- 실제 방법: 미제공.

---

## Results (abstract 범위)

- 미제공 — 전문 PDF 미확보. 외부 맥락: 예상 결과:
  - 암종별 선택적 표면 단백질 목록 및 종양 선택성 점수
  - 면역 관련 표면 단백질(immune checkpoint ligand 포함) 발현 패턴
  - 기존 치료 타겟과 신규 후보 비교 우선순위 표
- 실제 결과: 미제공.

---

## Analysis Notes (CytoGen 맥락)

- **NCCHE Multi-cancer 활용**: NCCHE 4개 암종(Gastric/STAD, Pancreatic/PAAD, Colon/COAD, Biliary/CHOL) 각각의 CTC 표면 발현 프로파일을 본 atlas와 비교 시 암종별 타겟 선택성 외부 검증.
- **CytoGen Tier 연동**: Tier1 ADC-Ready 타겟(CLDN18.2, HER2, TROP2 등)이 본 atlas에서 해당 암종 최상위 선택성을 보이는지 확인 → Tier 분류 근거 보강.
- **면역 관련 표면 단백질**: CD155(PVR), HLA-E 등 면역 회피 관련 표면 단백질이 atlas에 포함되었다면 CTC 면역 회피 분석과 연결.
- **주의**: sources/abstract.txt 오입력 상태. 실제 논문 확인 후 재분석 필요.
