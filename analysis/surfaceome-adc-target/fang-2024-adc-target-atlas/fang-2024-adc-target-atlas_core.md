## Executive Summary

- **무엇**: 19개 고형암종에 걸쳐 세포 표면 단백질(surfaceome)을 전사체·단백체·유전체 통합 알고리즘으로 체계적으로 분석하여 ADC 타겟 발굴 landscape를 제시한 범-암종 atlas. 75개 고유 타겟 후보와 165개 target-indication 조합을 도출.
- **모델 / 방법**: TCGA + GTEx 기반 DESeq2 차등발현 분석 → HPA/HPM 정상조직 발현 binning → BloodSpot 조혈모세포 발현 배제 → 기능 유전체 mRNA 프로파일링으로 단백질 과발현율 예측 → OncokB 기반 유전체 annotation → 12개 기준 종합 평가 알고리즘.
- **핵심 결과**:
  - ① 75개 세포 표면 단백질 후보 + 165개 target-indication 조합 최종 선별 (20,242 HUGO gene 출발)
  - ② 기존 ADC R&D에서 보고되지 않은 35개 후보 포함
  - ③ ClinicalTrials.gov 760개 ADC 임상시험에서 159개 ADC 확인 → 72개가 고형암 대상 개입 평가 중 (36개 고유 타겟)
  - ④ 이 중 72개 ADC가 36개 unique 타겟에 적용, BRCA가 가장 많은 ADC 평가 (n_ADC = 28, n_study = 139)
  - ⑤ 90개 후보 대상 유전체 분석: ERBB2, EGFR, MET, FGFR3가 oncogenic driver로 자주 변이
- **우리 적용**: NCCHE Gastric / SEV BRCA CTC에서 발굴된 표면 단백질 후보를 본 atlas의 165개 target-indication 조합 및 과발현율(Supplementary Table 4, 6)과 교차 검증 — `BD-opportunity` + `academic-citation` 용도.
- **심층**: 한계·재현 ROI는 `fang-2024-adc-target-atlas_lens-academic.md` / `fang-2024-adc-target-atlas_lens-industry.md` / `fang-2024-adc-target-atlas_methodology-brief.md` 참고.

---

## Identity

- **Title**: The target atlas for antibody-drug conjugates across solid cancers
- **Authors**: Jiacheng Fang, Lei Guo, Yanhao Zhang, Qing Guo, Ming Wang, Xiaoxiao Wang
- **Year**: 2023 (published online: 21 December 2023)
- **Venue**: Cancer Gene Therapy (2024) 31:273–284
- **DOI**: 10.1038/s41417-023-00701-3
- **Affiliations**: Interdisciplinary Institute of Medical Engineering, Fuzhou University; State Key Laboratory of Environmental and Biological Analysis, Hong Kong Baptist University; School of Ecology and Environment, Zhengzhou University; Department of Chemistry, Hong Kong Baptist University; College of Food Science & Engineering, Northwest University
- **Received / Accepted**: 2 May 2023 / 15 November 2023
- **Corresponding authors**: Lei Guo (gankLei@fzu.edu.cn), Ming Wang (wangming@nwu.edu.cn), Xiaoxiao Wang (wangxiaoxiao_523@163.com)
- **Funding**: American Association for Cancer Research (AACR Project GENIE registry 언급)
- **COI**: The authors declare no competing interests.
- **Citation key**: `fang2023adctargetatlas`
- **Note**: paper-info.yaml의 year 필드가 2024로 기재되어 있으나 실제 출판연도는 2023 (online 2023-12-21). volume 31 (2024)은 인쇄 연도.

---

## Background

#### 배경 스토리

- **문제의 출발점**: ADC(Antibody-Drug Conjugate)는 종양세포 표면 항원에 특이적으로 결합하는 단클론 항체(mAb)에 강력한 화학요법 payload를 링커로 연결한 복합체다. 고형암 치료에서 ADC의 선별적 타겟 결합은 치료 효능과 독성 안전역(therapeutic window)을 동시에 결정하는 핵심 변수다. WHO 2020 데이터 기준 전 세계 암 신규 발생 19.3 million 건 중 92.85%가 고형암이며, 9.3 million이 암 관련 사망이다. 이 규모의 미충족 의료 수요에 비해 2019~2022년 FDA 승인 ADC 10개 중 7개만이 고형암 적응증이다.

- **선행 접근 A (개별 타겟 중심 연구)**: 기존 ADC 개발은 HER2, TROP2, HER3, NECTIN4, FOLR1 등 *개별 검증된 타겟*을 중심으로 진행되었다. HER2-T-DM1, DS-8201(trastuzumab deruxtecan)이 그 예다. DS-8201은 HER2-양성 전이성 유방암에서 overall response rate 60.9%, disease-control rate 97.3%를 달성했다(본문 §Introduction, ref.5).

- **A의 한계**: 개별 타겟 접근은 *종양 조직 vs. 대응 정상 조직*만 비교하고, 다른 정상 조직에서의 *전신 발현(systemic expression)*은 충분히 고려하지 못했다. BR96-doxorubicin은 Lewis(y) 항원의 위 점막 세포 발현으로 인한 출혈성 위염을 유발했고, CD44v6 지향 Bivatuzumab mertansine과 BAY794620 타겟 CA9는 표피 독성과 위장관 독성을 야기했다 — 이는 정상 조직 발현 과소평가의 결과였다.

- **선행 접근 B (부분적 통합 데이터베이스)**: TCGA, HPA, GTEx 등 공개 데이터베이스를 이용한 범-암종 분석 시도들이 있었다. Perna et al. 2017(Cancer Cell — AML 대상 CAR-T 항원 선별)은 선례지만 단일 암종·단일 모달리티였다.

- **B의 한계**: 다중 암종 + 전사체·단백체·유전체 통합 + ADC 타겟 특화 12가지 기준(내재화, trafficking route, 세포외 도메인 구조, 암 줄기세포 발현 등)을 동시에 고려한 *체계적 pan-cancer surfaceome atlas*는 부재했다.

- **이 논문으로 이어지는 gap**: ADC 타겟 후보 선별은 단순 발현 비율이 아니라 ① 발현 균일성(heterogeneity 저감), ② HSC/MPP 발현 배제, ③ 타겟 절대 발현 수준, ④ internalization 효율, ⑤ trafficking route, ⑥ 단클론 항체 개발 난이도, ⑦ 생물학적 기능(종양 형성에 기여 여부) 등 다차원적 평가가 필요하다. 이 논문은 이 갭을 알고리즘화하여 최초로 pan-solid-cancer ADC target atlas를 구축했다.

#### 기본 개념

- **ADC 구성 3요소**: ① 항원 특이적 mAb (targeting), ② 링커 (안정성·절단 시점 조절), ③ payload cytotoxic agent (MMAE, DM1, DXd 등). 각 요소가 독립적으로 약물동력학에 기여하므로 타겟 항원 선택이 세 요소 최적화의 출발점.
- **Surfaceome**: 세포 표면에 위치하는 전체 단백질 세트. 전체 인간 proteome의 ~26%를 차지. 항체 접근 가능성(antibody accessibility) 측면에서 ADC 타겟의 일차 선택 풀.
- **BloodSpot 필터링**: 조혈모세포(HSC), Lin⁻CD34⁺CD38⁻ 조혈 다능성 전구세포(MPP) 발현이 높으면 ADC가 이 세포 집단을 고갈시켜 혈액독성을 유발할 수 있다. BloodSpot 데이터베이스(ref.28)를 활용해 이 발현이 높은 단백질을 배제했다.
- **기능 유전체 mRNA 프로파일링 (Functional Genomic mRNA Profiling)**: 유전체 변이(transcriptional component, CNV 등)가 mRNA 발현에 미치는 효과를 principal component analysis로 보정하여 단백질 수준 과발현율을 예측하는 방법(ref.24).
- **Mann-Whitney U test**: 비모수 2군 비교 검정. 이 논문은 종양 vs. 정상 조직 차등발현 분석과 유전자 변이 유무에 따른 발현 차이 분석 모두에 적용.

#### 이 논문의 필요성

- **핵심 이유**: FDA 승인 및 임상 중인 ADC 타겟이 정상 조직에서도 상당 발현을 보이는 사례(CD166/ALCAM, CD56/NCAM1의 신장·간·폐·심장 발현)가 독성으로 이어질 수 있음에도, 이를 체계적으로 평가한 범-암종 atlas가 없었다.
- **기존 방법으로 부족했던 지점**: 표적 선택이 *단일 암종의 종양-정상 비교*에 국한되어 전신 정상 조직 발현 landscape를 과소평가했다.
- **이 논문이 해결하려는 방향**: 전사체·단백체·유전체 통합 데이터를 기반으로 12개 기준을 알고리즘화하여, 이전에 ADC R&D에서 보고되지 않은 신규 후보 35개를 포함한 75개 타겟·165개 target-indication 조합을 체계적으로 제시.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: 19개 고형암종에서 ADC 타겟으로서 적합한 세포 표면 단백질을 체계적으로 발굴하고 우선순위화.
- **입력**: ① TCGA + GTEx RNA-seq (RNAseqDB, 9,109개 고품질 샘플, 14개 정상 조직 + 19개 고형암종) ② HPA IHC 기반 정상 조직 단백질 발현 데이터 ③ HPA/FANTOM5/GTEx RNA 발현 consensus NX 값 ④ Human Proteome Map (HPM) LC-MS/MS 단백질체 데이터 ⑤ HPA Subcellular Location 데이터 (6176 entry) + COMPARTMENTS 데이터베이스 ⑥ OncokB 유전체 annotation (682개 암 유전자, 임상 actionability 정보) ⑦ BloodSpot 조혈세포 발현 데이터 ⑧ ClinicalTrials.gov ADC 임상 데이터 (760개 등록 시험)
- **출력**: 75개 고유 ADC 타겟 후보 + 165개 target-indication 조합 목록 (Supplementary Table 4); 각 타겟의 12개 기준 점수 (Supplementary Table 6)
- **추정 대상**: 각 타겟의 종양 선택성(differential expression), 정상 조직 안전성, 과발현율, 내재화 가능성, HSC/MPP 영향.
- **중요한 hidden assumption**: RNA 발현 수준이 단백질 표면 발현 수준을 충분히 대리한다고 가정. 번역 후 조절(post-translational regulation), 단백질 turnover, membrane trafficking 효율은 직접 측정되지 않음.

#### 확률 / 통계학적 구조

- **차등발현 분석**: DESeq2 패키지, Benjamini-Hochberg adjusted p-value ≤ 0.01, $\log_2\text{FoldChange} \geq 1.0$ 임계값. 19개 고형암종 × 20,242 HUGO gene.
- **발현 binning (정상 조직)**: HPA IHC 발현을 High / Medium / Low / Not Detected / Not Available 5 범주로 분류. HPM log₁₀ 변환 후 Broyden-Fletcher-Goldfarb-Shanno 알고리즘으로 피크 최대값·표준편차 추정. peak 상위 1σ 이상 = High, peak 하위 1σ 이하 = Low, 그 사이 = Medium, 이하 Not Detected. RNA consensus NX: 20~40 = Medium, >40 = High, 1~20 = Low, <1 = Not Detected.
- **RNA-seq 표준화**: 모든 샘플에 대해 TPM(Transcripts per million) 변환, gene length 정규화, depth 정규화. TCGA와 GTEx 간 normalization은 project-level inter-normalization step을 포함 (ref.27 Wang et al. 2018).
- **과발현율 예측**: Principal Component Analysis (PCA)를 이용한 기능 유전체 mRNA 프로파일링. $n$개의 transcriptional component와 해당 eigenvalue를 추출 → multiple linear regression으로 non-genetic regulatory factor 보정 → 암종별 과발현율 백분율 계산 (threshold: 97.5 percentile of functional genomic mRNA signal of normal tissues).
- **통계 검정**: 종양 vs. 정상 비교 및 변이 유무 비교 모두 비모수 Mann-Whitney U 검정. 그룹 ≥3 비교는 비모수 Kruskal-Wallis one-way ANOVA. 모든 p-value는 Benjamini-Hochberg 보정.
- **유전자 변이 발현 상관**: 변이 유무에 따른 FC를 volcano plot + bubble plot으로 시각화 (OmicCircos 패키지, ref.23).

#### 핵심 method insight

- **기존 방법의 한계**: 기존 ADC 타겟 선별은 종양-정상 발현 비율(paired tumor/normal comparison)에 집중했다. 그러나 ①해당 암종 정상 조직만 비교하고 다른 정상 조직 전신 발현은 무시했으며, ② HSC/MPP 발현에 의한 혈액 독성 예측이 빠졌고, ③ 내재화 효율·trafficking route·세포외 도메인 크기 같은 ADC 특화 기준이 체계적으로 통합되지 않았다.
- **이 논문이 바꾼 가정**: 타겟 적합성은 *단일 비율*이 아니라 *12개 다차원 기준*의 종합 평가로 결정된다. 특히 전신 정상 조직(32개 정상 조직 카테고리) 발현을 체계화하고, BloodSpot으로 HSC/MPP 독성 리스크를 사전 배제했다.
- **새로 추가한 변수**: ① 기능 유전체 mRNA 프로파일링으로 추정한 단백질 과발현율(protein overexpression rate), ② 암 줄기세포(CSC) 특이 발현(BloodSpot 기반 bone marrow Lin⁻CD34⁺CD38⁻CD90⁺CD45RA⁻ HSC 발현 배제), ③ 12개 drubability 기준 종합 radar chart.
- **이 변화가 중요한 이유**: 기존에 알려지지 않은 35개 신규 후보를 발굴하고, 임상 데이터와 통합해 실제 ADC 개발 pipeline과의 교차 검증이 가능해졌다.

#### 이전 방법과의 차이

- **Baseline**: TCGA 단일 데이터베이스 기반 종양-정상 비교, 개별 암종 연구, Perna et al. 2017 방식의 단일 omics 타겟 선별.
- **공통점**: DESeq2 차등발현 분석, TCGA mRNA 데이터 활용, 정상 조직 발현 배제 논리.
- **차이점**: ① 전사체 + 단백체 (IHC + LC-MS/MS) + 유전체 통합, ② 32개 정상 조직 카테고리 통일 + 재배열, ③ 기능 유전체 mRNA 프로파일링으로 단백질 과발현율 *예측*, ④ 12개 ADC 특화 평가 기준 동시 적용, ⑤ BloodSpot HSC/MPP 배제.
- **차이가 크게 나타나는 조건**: 정상 조직 발현이 높지만 종양 선택성도 높은 타겟(예: CD276 — 여러 target-indication에 걸쳐 발현되나 paired indication에서는 낮은 차별성)을 처리할 때. 본 알고리즘은 이런 경우 타겟을 배제하지 않고 12개 기준으로 세분화 평가했다.

#### 효과가 Results에서 나타난 방식

- 20,242 HUGO gene → 219 DEG 후보 → 90 candidate → 75 unique target / 165 target-indication 조합으로 좁아지는 funnel 구조가 Results에서 단계별로 제시됨 (Supplementary Tables 3, 4).
- 기능 유전체 mRNA 프로파일링으로 243개 target-indication 중 >10% 과발현율이 75% 이상에서 관찰됨; 24개에서 >75%, 41개에서 >50% (Supplementary Table 6).
- Ablation 성격의 검증: BloodSpot 필터 적용 전후 후보 수 변화가 명시되지는 않으나, 알고리즘 단계별 후보 감소가 Supplementary Tables에 기록됨.

#### Method 관점의 한계

- **RNA→단백질 가정**: 전사체 발현이 단백질 표면 발현을 완전히 반영한다는 가정. ERBB2의 경우 BRCA에서 mRNA-protein 상관이 높으나(Fig. 6b), 일부 암종에서 Pearson r이 낮다 — 이 가정이 모든 타겟·암종에 동일하게 성립하지 않음.
- **IHC 한계**: HPA IHC 기반 정상 조직 발현은 항체 품질에 의존. 낮은 풍부도 단백질 검출에 기술적 한계.
- **표본 크기 불균형**: 암종별 TCGA 샘플 수가 다르며 (BRCA n=139 study, UVM n=1 study), 일부 희귀 암종은 소수 샘플 기반 발현 추정.
- **BloodSpot 기준**: Lin⁻CD34⁺CD38⁻CD90⁺CD45RA⁻ HSC와 Lin⁻CD34⁺CD38⁻ MPP 발현 차단 기준이 엄격하지만, 다른 정상 조혈 세포 아형에 대한 독성은 이 필터만으로 완전히 예측되지 않음.

---

## Results

#### Dataset별 결과

##### Dataset 1 — ClinicalTrials.gov + PubMed ADC 임상시험 데이터셋

- **Dataset**: ClinicalTrials.gov + PubMed, 검색 기준일 2022-12-31. 검색어: 'antibody-drug conjugate', 'cancer', 'tumour', 'oncology' 조합. ASCO 2022, ECCO 2022, ESMO 2022 포함.
- **목적**: 현재 고형암 ADC 개발 landscape 파악 및 타겟 분포 확인.
- **사용한 데이터 규모**: 760개 등록 임상시험, 159개 ADC 확인, 67개 unique antigen.
- **주요 수치**:
  - 159개 ADC 중 72개가 고형암 대상 개입 평가 (36개 unique 타겟, 227개 시험)
  - 118개 시험: 51개 ADC 완료 / 46개: 31개 ADC 종료(terminated) / 6개 ADC의 5개 시험 상태 불명
  - Phase I: 163개 / Phase II: 127개 / Phase I-II: 65개 / Phase III: 37개 / Phase III-IV: 4개 / Phase IV: 1개
  - 67개 unique antigen 중 21개가 HER2-directed (20+1 from Phase I/II/III 각각 최소 1개)
  - BRCA: n_ADC = 28, n_study = 139 (가장 많음); pan-cancer: n_ADC = 73, n_study = 113; NSCLC & SCLC: n_ADC = 21, n_study = 43
  - 현재 개입 평가 중인 타겟: HER2(21개 ADC), TROP2(5개), MSLN(4개), FOLR1(3개) (Fig. 1c)
- **정성 결과**: BRCA가 2006년 이후 매년 신규 임상 시작되는 유일 암종. 임상 개발의 압도적 집중이 관찰됨. LIHC는 적합 타겟이 거의 없어 ADC 시험이 없음 (Fig. 1d 발현 낮음으로 설명).
- **논문 주장과의 연결**: 기존 임상 ADC는 HER2 등 소수 타겟에 집중되어 있으며, 신규 발굴이 필요함을 동기화.

##### Dataset 2 — RNAseqDB + TCGA + GTEx (차등발현 분석)

- **Dataset**: RNAseqDB (github.com/mskcc/RNAseqDB), 9,109개 고품질 샘플, 14개 정상 조직 + 19개 고형암종. TCGA phenotype (UCSC Xena), GTEx RNA-seq.
- **목적**: 종양에서 유의하게 과발현되는 세포 표면 단백질 후보 도출.
- **사용한 데이터 규모**: 20,242 HUGO gene 출발 → DESeq2 (BH-adjusted p ≤ 0.01, log₂FC ≥ 1.0) → 막단백질 annotation dataset 6,176 entry와 교차.
- **주요 수치**:
  - 90개 타겟 후보 (+ 225개 target-indication 조합)가 알고리즘 도출 (후속 refinement 전; Results §Assembling)
  - 87개 후보 + 225개 target-indication 조합 → 12개 기준 전수 평가 후 84개 후보 + 213개 target-indication으로 좁혀짐
  - 최종: 75개 unique target + 165개 target-indication (Supplementary Table 4)
  - CELSR1, GPR87, OR51E1, SLC2A12, VANGL1은 32개 정상 조직 모두에서 medium 이상 발현 없음 (Fig. 2)
  - MUC17-STAD 조합: 위암 조직 vs. 정상 위 조직 log₂FC가 최고 수준으로 9.8 (Fig. 2)
  - VTCN1-UCEC, DSC3-LUSC, GPR87-LUSC: FC = 8.1 / 8.1 / 7.8 (각각)
- **통계**: BH-adjusted p-value ≤ 0.01, log₂FC ≥ 1.0 임계값. Mann-Whitney U 검정.
- **정성 결과**: CD276은 많은 target-indication에 걸쳐 발현되나 paired indication 대비 낮은 차별성을 보여 "고집적 ADC target"의 대표 사례이나 정상 조직 안전성 이슈가 있다.
- **논문 주장과의 연결**: 종양 선택성을 단순 발현 배수로 평가하면 CD276 같은 케이스를 놓치게 된다 → 정상 조직 전체 프로파일 검토의 중요성.

##### Dataset 3 — HPA / HPM / FANTOM5 / GTEx 정상 조직 발현

- **Dataset**: Human Protein Atlas (HPA) IHC 기반 정상 조직 발현 + Human Proteome Map (HPM) LC-MS/MS + RNA consensus (HPA, GTEx, FANTOM5). 32개 unique 정상 조직 카테고리로 정리.
- **목적**: 타겟 단백질의 전신 정상 조직 발현 평가 — on-target, off-tumor 독성 예측.
- **주요 수치**:
  - CD166(ALCAM)과 CD56(NCAM1): 신장·간·폐·심장에서 high 발현 확인 (Fig. 1a, right panel)
  - TACSTD2(TROP2): 14.5% target-indication 조합에서 식도 정상 조직 발현 수준이 타겟 발현 수준 이하 → 식도는 가장 불리한 정상 조직 환경 (Results §Differential gene expression)
  - TNFRSF21, TPBG: 방광 정상 조직 발현 > paired tumor 조직 발현
  - DLK1: LIHC에서 정상 부신샘, 골수, 뇌, 난소, 고환보다 발현 낮음
- **정성 결과**: 폐(liver), 담낭, 췌장은 타겟 발현이 paired indication 대비 정상 조직에서 낮아 가장 유리한 환경. 식도는 가장 비우호적.
- **논문 주장과의 연결**: 임상 ADC 타겟들도 다수 정상 조직에서 high 발현을 보인다 → 타겟 선택 시 전신 발현 평가가 필수적.

##### Dataset 4 — 기능 유전체 mRNA 프로파일링 + 단백질 과발현율 예측

- **Dataset**: TCGA + GTEx RNA-seq. 22개 tumor subtype (유방암 4개 subtype 포함: ER-/HER2+, ER+/HER2-, ER+/HER2+, TNBC 등).
- **목적**: 환자 내 유전체 이질성(genomic heterogeneity)을 보정한 단백질 과발현율 예측.
- **주요 수치**:
  - 243개 target-indication 중 >75% 이상에서 >10% 과발현율 관찰 (p.281)
  - 24개 target-indication: >75% 샘플에서 과발현율 >75% (green circle, Fig. 5)
  - 41개 in 54 target-indication: >50% (Fig. 5)
  - BRCA에서 HER2 과발현율: ER-/HER2+ 및 ER+/HER2+ 에서 >77% (highest)
  - TNBC에서 VCAM1 과발현율: 52% (가장 높은 예측 과발현율)
  - TNBC에서 CD276(B7-H3) 과발현율: 43%
  - KIRC에서 CA9 과발현율: 93% (가장 높음)
  - KIRC에서 HAVCR1: 100%, KICH에서: 78%
  - BLCA에서 UPK1B: 67% (가장 높은 예측 과발현율)
  - COREAD에서 RNF43: 78%, NOX1: 53%
  - LIHC에서 TM4SF4, GPC3, FGFR4: top 3 (구체 수치는 Fig. 5 참조, 본문 명시값 없음)
  - PRAD: 75% 이상 샘플에서 과발현되는 타겟 최대 암종 — TRPM8, SLC2A12, SLC30A4, OR51E2 포함
- **논문 주장과의 연결**: 단순 발현 차등보다 *환자 내 과발현율 예측*이 ADC 효과를 예측하는 더 적절한 지표임을 주장.

##### Dataset 5 — OncokB + TCGA MAF (유전체 기반)

- **Dataset**: OncokB (oncokb.org), TCGA MAF("Multi-Center Mutation Calling in Multiple Cancers"), 13개 고형암종 146개 target-indication 조합.
- **목적**: 타겟 항원의 유전체 변이(돌연변이, CNV, amplification)가 발현에 미치는 영향 분석.
- **주요 수치**:
  - 13개 암종 146개 조합 중 65개 조합에서 변이 유전자가 표적 발현과 유의한 상관 (51개 타겟, Fig. 4a)
  - TP53 변이: 가장 광범위한 연관. BRCA에서 BMPR1B 발현이 TP53 변이 샘플에서 4.9배 낮음; KCNE4, SLC39A6는 각각 76.1%, 72.5% 발현 감소
  - BRAF 변이: THCA에서 TACSTD2 발현 3.9배 상승 (58.8% THCA 샘플)
  - FGFR3 발현: BLCA의 13.4% TP53 유전자 변이 샘플에서 3.4배 상승
  - ERBB2_PTEN: BRCA 57.4% 샘플에서 FC = -3.2 (down)
  - EGFR: LUAD에서 가장 흔한 돌연변이 (exon 19 결실 2.6%, exon 21 L858R 1.3%, exon 20 삽입 1.3%)
  - ERBB2: BRCA에서 amplification(12.4%) + mutation(3.4%)
  - EGFR 돌연변이 중 LUAD에서는 exon 19 결실 26.1%, L858R 5.3%, exon 20 삽입 11.5% (LUAD 비율)
- **정성 결과**: TP53 변이가 가장 광범위하게 타겟 발현에 영향. 병리 stage별로도 발현이 다르며 (Fig. 4c — IGF1R BRCA는 stage I에서 상승, stage II/III에서 하강), 전이 상태에 따라 APOLD1, ST14가 단계적 변화.
- **논문 주장과의 연결**: 유전체 이질성이 ADC 치료 효과에 영향을 미치므로 타겟 선별 시 oncogenomic context 반영이 필요함.

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 현재 임상 ADC 타겟(HER2, TROP2 등)은 여러 정상 조직에서 medium-high 발현을 보임 — 이것이 ADC 임상 독성의 주요 원인이 될 수 있음. 반면 알고리즘이 선별한 신규 후보들은 더 제한된 정상 조직 발현을 보이는 경향이 있다.
- **가장 중요한 수치**: 75개 unique ADC 타겟 + 165개 target-indication 조합; 기존 ADC R&D에서 보고되지 않은 35개 신규 후보; 과발현율 >75% (24개 target-indication).
- **baseline 대비 차이**: 기존 개별 타겟 접근 대비, 이 atlas는 12개 기준 동시 평가로 이전에 간과된 타겟과 독성 리스크를 병렬 제시.
- **결과 해석 시 주의점**:
  - RNA 발현 기반이므로 단백질 수준 직접 검증 미수행.
  - 비모수 통계를 썼고 p-value는 BH 보정됐으나 개별 수치의 95% CI는 Figure에 명시되지 않음.
  - 희귀 암종(UVM, TGCT 등)은 샘플 수가 매우 적어 발현 추정 불확실.
  - 미제공: 35개 신규 후보 각각에 대한 개별 통계(p-value, CI)는 본문에 없음 — Supplementary Table 참조 필요.

---

## Figures

#### Figure 1 — ADC 타겟 발현 프로파일 및 임상 개발 파이프라인 개요

- **이 Figure가 필요한 이유**: 기존 임상 ADC 타겟들이 정상 조직에서 어떤 발현 수준을 보이는지 시각화함으로써, 논문의 핵심 문제의식("임상 ADC 타겟도 정상 발현이 있다")을 직접 제시.
- **이 Figure가 뒷받침하는 주장**: 현재 임상 ADC 타겟의 정상 조직 발현 문제 + 임상 landscape 파악.

##### 패널별 설명

- **a (left panel)**: 19개 고형암종 × 36개 타겟 log₂FC heatmap (DESeq2). 왼쪽 컬러바: log₂FC >5 (진빨강) ~ <0 (파랑). p ≥ 0.05인 셀은 별도 표시. 검은색 박스는 각 타겟의 paired indication. 오른쪽 패널: 32개 정상 조직 그룹별 단백질 발현 수준 (High/Medium/Low/Not Detected/Not Available).
- **a (right panel)**: CD166(ALCAM), CD56(NCAM1)이 신장·간·폐·심장에서 high 발현. 임상 ADC 타겟 중 정상 조직 발현 high인 것들 다수 확인.
- **b**: 2006~2022년 연도별 신규 ADC 임상 시작 수 암종별 stacked bar. BRCA가 2006년 이후 매년 지속 증가 유일.
- **c**: 상위 5개 타겟(HER2, TROP2, MSLN, FOLR1, DLL3)으로 향한 임상-stage ADC 히스토그램. HER2에 21개 ADC 집중(Phase I가 가장 많음).
- **d**: pan-cancer에서 임상 중 및 승인된 ADC 타겟의 gene set enrichment score (GSEA enrichment score). LIHC에서 타겟 발현이 가장 낮음 → 해당 LUAD-ADC 집중의 이유 설명.

##### 본문에서 강조한 비교

- 비교 대상: 임상 ADC 타겟(HER2, TROP2 등) vs. 정상 조직 발현
- 관찰된 차이: LUAD에서는 타겟 발현이 high; LIHC에서는 표적 발현이 낮아 ADC 개발이 부진. 이 차이가 임상 집중도 차이를 설명.
- 이 차이가 의미하는 것: 발현 landscape가 ADC 개발 전략의 실질적 driver.

##### 해석 시 주의점

- log₂FC는 effect size estimate이며 통계적 유의성 별도 확인 필요 (p ≥ 0.05 표시 셀 참조).
- 해석: 임상 ADC 타겟들이 정상 조직에서도 발현된다는 사실을 *결과*로 제시하지만, 이것이 실제 독성과의 인과관계를 직접 증명하는 것은 아니다.

---

#### Figure 2 — 알고리즘 선별 ADC 타겟 후보군의 발현 프로파일

- **이 Figure가 필요한 이유**: Figure 1이 기존 임상 타겟을 보여줬다면, Figure 2는 알고리즘이 *새로 발굴한* 90개 후보의 발현 landscape를 제시. 신규 후보들의 타겟 선택성을 시각화.
- **이 Figure가 뒷받침하는 주장**: 알고리즘 선별 후보들이 보다 나은 종양 선택성과 정상 조직 안전성 프로파일을 가질 수 있음.

##### 패널별 설명

- **left panel**: 90개 후보 × 19개 암종 log₂FC heatmap. 검은 박스 = paired indication.
- **right panel**: 32개 정상 조직 단백질 발현 수준 (High/Medium/Low/Not Detected/Not Available). 많은 후보들이 대부분 정상 조직에서 Low 또는 Not Detected.
- CELSR1, CELSR2, GPR87, OR51E1, SLC2A12, VANGL1: 32개 정상 조직 전체에서 medium 이상 없음 — 잠재적으로 낮은 on-target off-tumor 독성.
- ERBB2, ERBB3은 brain을 제외한 정상 조직에서는 high 발현 없으나 brain에서는 있음.

##### 본문에서 강조한 비교

- CD276(B7-H3): 많은 target-indication 조합에 걸쳐 발현되나 paired indication 대비 낮은 절대 차별성. 그러나 ADC accumulation이 가장 높은 타겟으로 별도 논의.
- ERBB2-BRCA: ERBB2 mRNA-protein Pearson r이 BRCA에서 높으나 일부 암종에서 낮음 (Fig. 6b 참조).

##### 해석 시 주의점

- 미제공: 각 후보의 정상 조직 발현 제한 기준(≤ medium)이 임상 독성 예측으로 직접 연결되는지 독립적 검증 없음.

---

#### Figure 3 — 정상 조직별 타겟 항원 차등발현 프로파일 원형 시각화

- **이 Figure가 필요한 이유**: 개별 target-indication 조합의 정상 조직별 발현 차이를 circos plot으로 전체 조망 — 어떤 정상 조직에서 특정 타겟이 문제가 되는지 직관적으로 파악.
- **이 Figure가 뒷받침하는 주장**: 타겟 독성 프로파일이 암종·타겟·정상 조직의 3자 관계에 의해 결정됨.

##### 패널별 설명

- Circos plot: 각 target-indication 조합이 22개 정상 조직(숫자 1~22)과의 log₂FC로 연결되는 heatmap. 염색체 위치(cytobands)도 함께 표시.
- log₂FC >5 진빨강 ~ <0 파랑.
- FGFR3_BLCA, BMPR1B_BRCA, BMPR1B_KIRC, BMPR1B_PRAD, TSPAN5_KICH 등이 강한 양성 FC 표시.

##### 해석 시 주의점

- 이 Figure는 *어느 정상 조직이 타겟 발현 측면에서 잠재적으로 불리한가*를 스크리닝 목적으로 사용. 실제 독성 예측은 단백질 발현·임상 데이터로 추가 검증 필요.

---

#### Figure 4 — 유전체 변이와 타겟 발현의 상관성

- **이 Figure가 필요한 이유**: 환자 내 유전체 이질성이 타겟 발현에 영향을 줄 수 있으므로, ADC 효과 예측을 위해 oncogenomic context를 고려해야 한다는 주장의 근거.
- **이 Figure가 뒷받침하는 주장**: 타겟 발현은 정적이지 않고 유전체 변이에 따라 달라진다 → 환자 선별 시 바이오마커 맥락이 필요.

##### 패널별 설명

- **a**: Bubble-volcano plot — 6개 암종(KIRC, BRCA, PRAD, THCA, BLCA, CESC, LUAD, STAD, COAD, HNSC, LUSC, LIHC, UCS)별 target-mutation 조합의 log₂FC와 통계 유의성(-log₁₀ p-value). 버블 크기 = 변이 보유 환자 비율.
- **b**: Pie chart — coding/non-coding/disruptive 변이 유형별 발현 FC. 컬러 팬 = log₂FC 방향. TP53 관련 조합에서 coding disruptive 변이 비중이 높음.
- **c**: Rank-heatmap — 병리 stage별 발현 변화. IGF1R_BRCA는 stage I에서 상승(1.5), stage II/III에서 하강(-2.4 to -3.5). TACSTD2_BRCA는 stage II에서 -1.7 → 병리 stage에 따라 타겟 발현이 크게 변동됨.

##### 본문에서 강조한 비교

- TP53 변이 유무: BRCA에서 BMPR1B 발현이 4.9배 낮아짐 — TP53 변이가 타겟 발현에 가장 광범위한 영향.
- BRAF 변이 + TACSTD2(TROP2): THCA의 58.8% 샘플에서 3.9배 상승 — BRAF 변이 타겟층에서 TROP2-ADC 반응성이 높을 가능성.

##### 해석 시 주의점

- 발현 상관은 관찰이지 인과가 아님. TP53 변이 → BMPR1B 발현 감소가 실제 ADC 타겟 적합성 감소로 이어지는지는 functional validation 없이는 주장 불가.

---

#### Figure 5 — 기능 유전체 mRNA 프로파일링으로 예측한 타겟 단백질 과발현율

- **이 Figure가 필요한 이유**: RNA-seq 기반 발현 차이가 실제 환자 집단에서 얼마나 많은 비율에서 관찰되는지(과발현율) 예측함으로써 임상 적용 가능성을 정량화.
- **이 Figure가 뒷받침하는 주장**: 선별된 타겟 중 상당수가 임상 규모의 환자 집단에서 충분한 과발현율을 보여 ADC 치료 대상군이 될 수 있음.

##### 패널별 설명

- dot plot: Y축 = 75개 신규 타겟(갈색) + 기존 ADC 타겟(검정). X축 = 22개 tumor (sub)type. 점 크기 = 예측 과발현율(%).
- 녹색 원 = >75%, 빨간 원 = 50~75%.
- 선별 신규 타겟들이 특정 subtype에서 높은 과발현율 집중.

##### 해석 시 주의점

- 해석: 기능 유전체 mRNA 프로파일링 예측치는 실제 IHC/proteomics 검증과 다를 수 있다. 특히 단백질 turnover, post-translational modification, membrane trafficking 효율은 예측 모델에 포함되지 않음.
- VCAM1(TNBC 52%), HAVCR1(KIRC/KICH 100%/78%) 등 일부 예측치가 매우 높으나, 정상 조직 발현과의 종합 평가 후 최종 타겟 등급이 결정됨.

---

#### Figure 6 — EGFR, ERBB2, MET, FGFR3의 유전체 변이 및 다차원 ADC 타겟 평가

- **이 Figure가 필요한 이유**: 주요 oncogene driver(EGFR, ERBB2, MET, FGFR3)의 ADC 타겟으로서의 다차원 적합성을 radar chart로 종합 평가. 논문의 12개 기준 알고리즘의 구체적 적용 예시.
- **이 Figure가 뒷받침하는 주장**: 12개 기준 종합 평가가 개별 지표 단독 판단보다 타겟 우선순위화에 우월하다.

##### 패널별 설명

- **a**: EGFR, ERBB2, MET, FGFR3의 암종별 유전체 변이 빈도 bar chart (alteration, amplification, mutation type별 세분화). BLCA에서 FGFR3 mutation이 가장 빈번.
- **b**: ERBB2 mRNA vs. protein Pearson r (left) 및 ERBB2 mRNA vs. CNV Pearson r (right). BRCA에서 높은 mRNA-protein 상관, 일부 암종(RCC)에서 낮은 상관.
- **c**: ERBB2_BRCA radar chart — 12개 차원: 차등발현(Differential expression), 종양 내 절대 발현(Absolute levels in tumor), 발현 균일성(Expression homogeneity), 정상 발현(Normal expression), HSC/MPP 발현(HSC and MPP expression), 내재화(Internalization), 단클론 항체 개발 난이도(Difficulty for target antibody discovery), 단일/복수 transmembrane, 세포외 도메인 크기(Extracellular domain size), 세포외 도메인 상동성(Extracellular domain homology), 유전체 기반(Genetic basis), CSC 특성(CSCs features). 4개 색: Expression profile / Endocytosis / Biological function / Difficulty for target antibody discovery.
- **d**: EGFR_LUAD, FGFR3_BLCA, MET_LUAD, NECTIN4_BLCA radar chart 비교. NECTIN4_BLCA가 전반적으로 균형잡힌 고점수를 보이고, EGFR_LUAD는 발현 균일성이 낮음.

##### 본문에서 강조한 비교

- ERBB2_BRCA: 차등발현과 절대 발현은 높으나 internalization이 고려됐을 때 HER2 double epitope ADC(MEDI4276)가 too high internalization requirement로 문제 됨 (Discussion).
- MET_LUAD: 발현 프로파일과 NECTIN4_BLCA의 차이 — MET은 expression heterogeneity 때문에 성능이 제한.

##### 해석 시 주의점

- Radar chart 면적이 곧 "종합 점수"는 아님 — 12개 기준의 가중치가 동일하게 주어졌는지 본문에 명시되지 않음.
- 해석: ERBB2_BRCA가 가장 많은 ADC 임상시험의 타겟이 된 것은 이 radar chart에서도 overall 높은 점수로 뒷받침되지만, 발현 균일성과 정상 조직 발현 등 일부 차원은 개선의 여지를 시사.

---

## Tables

본문에 정식 Table 없음. 모든 정량 데이터는 Supplementary Tables에 수록.

**Supplementary Tables 목록** (본문 언급 기준):

- **Supplementary Table 1**: FDA 승인 ADC 목록 (15개)
- **Supplementary Table 2**: ClinicalTrials.gov 등록 ADC 임상 목록 (760개 시험, 159개 ADC)
- **Supplementary Table 3**: 알고리즘 도출 90개 타겟 + 243개 target-indication 조합 (초기 후보)
- **Supplementary Table 4**: 최종 75개 unique target + 165개 target-indication 조합
- **Supplementary Table 5**: 변이-타겟 발현 상관 (13개 암종 146개 조합)
- **Supplementary Table 6**: 22개 tumor subtype별 단백질 과발현율 예측값
- **Supplementary Figures 1–5**: 병리 stage별, 종양 크기별, 전이별 발현 변화 (APOLD1, ST14, MET, TACSTD2, CDH3 등)
- **Supplementary Figure 7**: RTK/RAS/MAP-Kinase pathway의 receptor tyrosine kinase 선별 목록

해석: 핵심 수치가 본문에 서술되어 있으나 raw data는 대부분 Supplementary Tables에만 있다. Supplementary Table 4의 165개 target-indication 조합과 Supplementary Table 6의 과발현율 데이터가 이 논문에서 가장 직접적으로 활용 가능한 산출물이다.

---

## Supplementary Information

- **Supplementary Methods**: MOESM1 (41417_2023_701_MOESM1_ESM.docx) — 임상시험 검색 전략, 알고리즘 세부 단계, 통계 방법 추가 설명.
- **Supplementary Data Tables**: MOESM2 (41417_2023_701_MOESM2_ESM.xlsx) — Supplementary Tables 1~6 원시 데이터.
- **Supplementary Figures 1–7**: 병리 stage, 종양 침윤, 전이 상태별 타겟 발현 변화; ERBB2, EGFR mRNA-CNV-protein 상관 (암종별); RTK/RAS/MAP-Kinase pathway receptor.
- 검토필요: MOESM1.docx 전체 내용과 MOESM2.xlsx의 Supplementary Table 4 (165개 target-indication 조합) 및 Table 6 (과발현율 데이터)를 직접 확인하여 NCCHE Gastric / SEV BRCA 적용 가능 타겟 목록 추출 필요.

---

## 분석 메모

- **DOI 정정**: 기존 paper-info.yaml의 DOI는 오기재 (Hao 2021 Seurat). 실제 DOI는 10.1038/s41417-023-00701-3, 저널 Cancer Gene Therapy, 출판 연도 2023 (volume 31 인쇄 연도 2024).
- **저자 표기**: paper-info.yaml의 `authors_short: Fang, J. et al.` — 제1저자 성은 Fang(방). 논문 본문 표기는 Jiacheng Fang.
- **Figure 수**: 총 6개 main figure (모두 multi-panel), Extended Data Figure 없음. Supplementary Figures 7개.
- 검토필요: Supplementary Table 4의 165개 target-indication 조합을 위암(STAD), 유방암(BRCA), 방광암(BLCA) 관점으로 추출하여 CytoGen Tier 분류 체계와 교차 비교 작업 필요.
- 질문: VCAM1(TNBC 52% 과발현 예측)은 본 atlas에서 신규 발굴 타겟인가 아닌가? Fig. 5에서 brown(신규)으로 표시되었음 — TNBC에서 VCAM1 표적 ADC 선행 임상 데이터 확인 필요.
