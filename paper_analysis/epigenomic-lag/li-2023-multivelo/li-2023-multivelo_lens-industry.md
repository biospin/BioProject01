# Lens — Industry — Li 2023 MultiVelo

> Citation: `@li2023multivelo`. 학술적 한계·다음 논문·citation 후보는 `li-2023-multivelo_lens-academic.md`에 분리. 본 노트는 *산업·규제·BD* 관점.

---

## 1. Categorization

> 본 섹션 값은 `paper-info.yaml`의 `categorization` 블록과 동기화.

### Domain (자동 추출, 검토 표시)

- `single-cell-genomics`
- `epigenomics`
- `RNA velocity`
- `computational-methods`
- `multi-omics`
- (검토: 추가 후보 `hematopoiesis`, `neurodevelopment` — 본 paper의 *적용 dataset* 위주이므로 domain보다 application으로 둠)

### Use case (vocabulary 6개 중 1~3개)

- **`methodology-reference`**: chromatin–transcription lag을 정량하는 우리 분석에 *직접 차용 가능*. ODE 형태 + EM + 4 state assignment.
- **`pipeline-applicable`**: 우리 HSPC 10x Multiome 또는 organoid multi-omic dataset에 *코드 그대로* 적용 가능 (Python, scanpy/AnnData 호환).
- **`academic-citation`**: `li-2023-multivelo_lens-academic.md`의 Citation 후보가 풍부 — proposal/논문 introduction의 prior work 인용 핵심.

### Importance (1개 종합 등급)

- **Level**: 상
- **Perspective (1문장)**: HSPC 10x Multiome pipeline에 *바로 차용 가능*하고, chromatin–RNA lag 정량 알고리즘이 우리 epigenomic-lag topic의 *foundational reference*이며 후속 multi-omic velocity (MultiVelo-VAE 등) 비교 baseline.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**:
  - Mouse brain: 3,365 cells. Mouse skin: 6,436. HSPC: 11,605 (가장 큼, single donor). Human brain: 4,693.
  - *single donor / single batch* 비중이 높다. HSPC는 *single donor* 명시 (Methods §"Human HSPCs": "Freshly thawed cells from a single donor").
  - `해석: 의료·임상 grade evidence로는 부족. n cell 수가 11k라도 *biological replicate*가 1 donor면 inter-donor variance 검증 불가.`
- **Cohort 편향**:
  - 인종/성별 정보 미명시 (HSPC: Fred Hutch Hematology Core B 구매, donor characteristic 비공개).
  - Mouse는 dataset마다 strain 미상.
- **Replication 부족**:
  - Same-method *cross-cohort replication 없음*. Mouse brain의 결과 (M1:M2 = 41:27)가 *다른 lab*에서도 같은 비율 나오는지 미검증.
  - `해석: 단일 lab의 single dataset에서 도출된 모든 ratio는 *추정치*. 다른 cohort에서 재현하기 전에는 absolute number 인용 주의.`
- **Selection bias**:
  - Gene filtering: likelihood threshold (default 0.05, mouse skin 0.07, HSPC 0.02). thresholds가 *결과에 미치는 영향* 별도 ablation 부재.
  - HSPC에서 cell cycle score regress-out — *removed information*이 priming dynamics에 영향 줄 가능.
- **Multiple testing**:
  - GO enrichment에서 *FDR < 0.002* 명시 (HSPC). Mouse brain GO terms는 *FDR-significant*라고만 명시.
  - 단순 비교 (e.g., Wilcoxon between M1 and M2 expression total) p value는 *single test*. 그러나 ChIP-seq histone mark 3개 × 2 model 비교에서 *Bonferroni-style correction 미적용* — H3K4me3 p=0.016이 6 tests burden 하에서는 *borderline*.

### 2.2 임상·기술적 제약

- **Tissue/sample 가용성**:
  - 10x Multiome, SHARE-seq: 일반적 lab에서 접근 가능한 platform. Mouse는 routine.
  - HSPC: CD34+ FACS sorting 필요. CGT (cell & gene therapy) 회사면 routine.
  - Fetal human cortex: *희귀 sample*. tissue acquisition (consent, regulatory) 자체가 bottleneck.
- **장비·시약 가용성**:
  - 10x Chromium + Illumina NovaSeq 등 standard scRNA-seq + scATAC-seq stack.
  - WNN smoothing은 Seurat V4 (R), 나머지 분석은 scanpy/scVelo (Python) — *cross-language stack* 부담.
- **계산 자원**:
  - Intel i7-9750H 12-thread CPU, 32 GB RAM, *no GPU*.
  - Peak memory 2.9 GB (HSPC), runtime 124 min — 일반 워크스테이션에서 실행 가능.
  - 단 *100k+ cell scaling*은 미검증. 임상 cohort scale (수만 sample × 수만 cell)에서는 cloud HPC 필요 예상.
- **Turnaround time**:
  - Raw FASTQ → CellRanger ARC → preprocessing (WNN, peak aggregation) → MultiVelo fit. CellRanger ARC 자체가 수 시간~1일. MultiVelo fit이 ~2시간. 전체 *수 일*. → *임상 의사결정 turnaround*로는 부적합 (clinical trial enrollment 시 1주일 안에 결과 나와야 하는 use case에는 부적합).

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**:
  - 본 paper는 *research tool*. 직접적 IVD/LDT/SaMD/drug pathway 해당 없음.
  - 그러나 *companion biomarker discovery*에 활용 시 (예: 특정 hematological malignancy의 differentiation stage 분류), 후속 ASSAY와 함께 *LDT 또는 IVD pathway*에 들어갈 가능성.
- **Analytical / Clinical validation**:
  - Analytical: 본 paper의 simulation (98.5% model assignment accuracy)이 *analytical reference*. 그러나 *FDA-grade* (LOD, LOQ, precision, accuracy, repeatability, reproducibility) 검증 아님.
  - Clinical: 없음. 본 paper는 cell biology 발견이 주된 목적.
- **GMP / GLP**:
  - 본 paper는 *research GLP-style*. clinical-grade GMP는 별도 검증 필요.
  - HSPC sample은 Stemspan II 7일 in vitro 배양 — clinical CGT 표준 (예: GMP-grade serum-free) 아님.
- **IRB / consent**:
  - HSPC: Fred Hutch Hematology Core B 구매 — IRB consent 가정. Paper에 *명시적 consent statement 없음* (Acknowledgement에 "Cooperative Center of Excellence in Hematology grant DK106829" 언급, IRB 명시는 미제공).
  - `검토필요: 우리가 본 dataset을 다른 분석에 사용 시 GSE209878 NCBI submission에 *human subject* protection 정보 확인 필요.`
- **Label·indication**: 해당 없음 (research tool).
- **Reproducibility for audit**:
  - 코드 GitHub open (welch-lab/MultiVelo).
  - Raw FASTQ: dbGaP phs002915.v1.p1 *restricted access* (HSPC만).
  - 나머지 dataset: GEO (mouse skin GSE140203, human brain GSE162170, ChIP-seq GSE70677). 10x mouse brain은 10x Genomics 공식 dataset.
  - Processed files: GSE209878 (HSPC) open.
  - `해석: code + processed data는 audit 가능. raw FASTQ는 dbGaP barrier — clinical reproducibility는 추가 절차 필요.`

### 2.4 권위·신뢰 가중치

- **출처 1차/2차**:
  - **1차 출처**: peer-reviewed *Nature Biotechnology*. Welch lab의 *flagship method paper*.
- **Peer review 여부**: peer-reviewed (Yuanhua Huang 등 reviewer 명시).
- **저자 이해상충 (COI)**: 저자 "declare no competing interests" 명시.
- **Funding source**:
  - NIH grants (R01AI149669, R01HG010883, F31AI155047, T32GM070449, T32GM007315), Cooperative Center of Excellence in Hematology (DK106829), Rackham Regents Fellowship — *공공 funding*, corporate sponsorship 없음. → *결과 편향 우려 낮음*.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관의 자산화 가능성**:
  - Joshua D. Welch lab — University of Michigan. 학술 lab으로 *startup 창업 정보는 paper에 없음*. (`질문: LinkedIn / Crunchbase로 Welch lab spin-off 확인 필요.`)
  - MultiVelo code Open source (GitHub) → license가 일반적 OSS면 우리가 자유롭게 사용 가능. 단 *우리 commercial product에 통합* 시 license condition 재확인.
  - Patent: paper에 patent application 명시 없음. 가능성은 *낮음* (open-source method paper의 통상 패턴).
- **공동연구 후보**:
  - Welch lab은 *open source, 활발한 GitHub maintenance, 다수 single-cell tool (LIGER, MultiVelo) 발표* — 공동연구 / visiting 친화적.
  - Welch는 single-cell multi-omic 분야 *active player*. 우리가 HSPC multiome 데이터로 contact할 수 있는 reasonable angle.
- **경쟁사 관찰**:
  - 우리 영역 경쟁사가 MultiVelo를 *언급/사용*했는지 *모니터링 필요*. Gao 2024 MultiVeloVAE (extension paper) 등 *follow-up*이 이미 나옴 → MultiVelo가 *de facto standard*로 자리잡는 중.
- **시장 영향**:
  - Single-cell multi-omic *tool 시장*에 직접 영향. 우리가 multi-omic 분석 service 제공 시 *고객 expectation*에 MultiVelo가 포함될 가능성.

### 3.2 Commercialization-candidate (자체 제품화)

- **제품 카테고리 후보**:
  - **Software (SW)**: 자체 multi-omic analysis platform 또는 cloud SaaS에 MultiVelo 통합 (open-source 이므로 직접 wrapping). 단순한 패키지 wrapping은 *차별화 어려움* — 가치는 *vertical-specific UX* (e.g., HSPC differentiation diagnostic dashboard)에 있음.
  - **Diagnostic (Dx)**: 직접적 Dx 아님. 단 *differentiation stage signature* (e.g., M1/M2 enriched gene set)를 *biomarker panel*로 가공하면 hematological malignancy stratification에 활용 가능 (장기).
  - **Service**: multi-omic differentiation analysis as a *contract service* (CRO offering). MultiVelo + downstream interpretation 일괄 제공.
  - **Therapeutic**: 직접적 therapeutic 후보 없음. 단 *MultiVelo로 발견한 disease SNP–gene lag*가 drug target nomination에 기여 가능 (장기 R&D).
- **기술적 성숙도 (TRL)**:
  - Method 자체: TRL 4–5 (academic validation 완료, 산업 적용은 미검증).
  - 산업 제품화 (SaaS/CRO): TRL 2–3 (concept).
- **IP 자유도**:
  - 본 paper의 method는 open-source. 우리가 *변형 + 우리 use case 특화*하면 *우리 IP 보호 가능*.
  - Underlying ODE는 *수학적 model*로 patent 어려움. 단 *specific algorithm + pipeline + UI*는 patent 가능.
- **MVP 시나리오**:
  - **MVP 1 — HSPC differentiation dashboard**: HSPC multiome dataset → MultiVelo fit → M1/M2 gene list + priming/decoupling timeline + 4 state cell-gene assignment 시각화 → React/Streamlit UI. 1개월 prototyping.
  - **MVP 2 — Drug response multi-omic velocity**: 약물 처리 cell의 multi-omic time-course → MultiVelo로 *response onset* 정량. CRO offering.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**:
  - 우리 *HSPC 10x Multiome*과 *동일 platform*. dataset 형식 (10x AnnData) 그대로 input.
  - 우리 organoid multi-omic, neural differentiation system에도 *바로 적용* 가능.
- **자원 가능성**:
  - 우리 환경 (워크스테이션 32 GB RAM, optional GPU)에서 *바로 실행* 가능. GPU 불필요.
  - 우리 팀 역량 (scanpy, scVelo 사용 경험)으로 *바로 운영* 가능.
- **전략적 방향 fit**:
  - 우리 *epigenomic-lag topic*의 foundational reference. 후속 분석 (MultiVeloVAE, chromatin velocity 등) 비교의 *baseline*.
  - 우리가 chromatin–RNA coupling을 quantify하는 *모든 후속 작업*의 starting point.
- **빠진 capability**:
  - *Wet lab perturbation*: causal validation은 우리도 동일하게 wet lab 필요 (별도 CRO 또는 collaborator).
  - *Spatial multi-omic*: spatial 정보 결합은 별도 framework 필요.

### 3.4 후속 BD·제품 액션 후보

- **우리 HSPC dataset에서 MultiVelo 실행**
  - 누가: 본인 (technical lead)
  - 언제: 다음 sprint (2주 내)
  - 자원: 워크스테이션 1대, 코드 install (1일), 우리 dataset preprocessing (3일), MultiVelo fit (2시간), 결과 해석 (3일)
  - 성공 기준: 우리 HSPC에서 ① M1/M2 gene list 추출, ② priming 시간 분포, ③ velocity stream이 known lineage hierarchy와 일치하는지 확인.

- **Welch lab contact (선택)**
  - 누가: 본인 + (BD lead 선택적)
  - 언제: 우리 HSPC 결과 산출 후 (1개월 내)
  - 자원: 이메일 1통, 우리 결과 1-page summary
  - 성공 기준: ① 협업 가능성 탐색 + ② 우리 dataset이 Welch lab의 follow-up paper에 reference로 들어갈 가능성 + ③ 우리가 MultiVelo 변형 개발 시 review 받을 채널 확보.

- **MultiVelo 결과를 슬라이드 / 사내 R&D 리뷰에서 발표**
  - 누가: 본인
  - 언제: 다음 분기 R&D 리뷰
  - 자원: slide 10장 (Fig. 1 schematic + 우리 HSPC 결과 3-4장)
  - 성공 기준: 팀이 *chromatin–RNA lag*를 이해 + 후속 wet lab 검증 candidate gene 1~3개 선정.

- **license / patent landscape 정밀 검토**
  - 누가: BD lead (외부 IP counsel optional)
  - 언제: 우리가 MultiVelo를 *우리 commercial product*에 embed 결정 시점
  - 자원: GitHub LICENSE 파일 + Welch lab patent application 조사 1일
  - 성공 기준: 우리 product distribution에 *legal 제약 없음* 또는 *명확한 license terms* 확인.

- **MultiVeloVAE 등 후속 paper 비교 분석** (장기)
  - 누가: 본인
  - 언제: 장기 (다음 분기 이후)
  - 자원: 후속 paper 분석 1주
  - 성공 기준: MultiVelo vs MultiVeloVAE 우열, 우리 use case에 어느 것이 적합 결정.

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective (1문장)**: HSPC 10x Multiome pipeline에 *바로 차용 가능*하고, chromatin–RNA lag 정량 알고리즘이 우리 epigenomic-lag topic의 *foundational reference*이며 후속 multi-omic velocity 비교 baseline.
- **등급 근거**:
  - 본 paper의 HSPC dataset (10x Multiome, day 0+7)이 *우리 현재 dataset과 동일 platform*. fit 결과를 직접 비교 가능.
  - Code (welch-lab/MultiVelo) GitHub open, scanpy/AnnData 호환 → *우리 환경에 바로 install*.
  - chromatin opening rate model이 *우리 핵심 문제 (epigenomic-lag)* 직결.
  - Peer-reviewed Nature Biotechnology, *single-cell multi-omic 분야 표준급 reference*. 후속 follow-up paper (MultiVeloVAE 등)가 *MultiVelo를 baseline*으로 인용.
  - 단 cell cycle confound 처리는 본 paper가 *partial* (regress-out만, separate fit ablation 없음) — 우리가 추가 작업 필요.

### 4.2 활용 우선순위

- **지금 (이번 sprint)**: 우리 HSPC dataset에 MultiVelo 실행. *2주 안에 결과 1개*.
- **다음 분기**: ① 결과 R&D 리뷰 발표 + ② MultiVeloVAE 등 follow-up paper 비교 분석 + ③ Welch lab contact (필요 시).
- **장기**: ① cell cycle confound 처리 사내 sub-pipeline 개발, ② 우리 commercial product에 embed 결정 (license + IP 검토 후).

### 4.3 발표·미팅에서 들이밀 시점

- **본인 학회 발표 / 본인 논문 introduction**: prior work로 인용. *RNA velocity의 chromatin extension*의 first major reference.
- **사내 R&D 리뷰**: 우리 HSPC dataset 분석 결과 발표 시 backbone method로 명시.
- **BD 미팅**: 우리가 multi-omic analysis capability를 *외부에 시연*할 때 MultiVelo 결과를 deck에 포함.
- **외부 컨퍼런스 / 키노트**: epigenomic regulation 관련 발표면 *foundational reference*로 인용.

### 4.4 추가 탐색 필요 영역

- **질문**: Welch lab이 MultiVelo 관련 startup 창업했는지 LinkedIn / Crunchbase 확인 필요. → BD-opportunity 평가에 영향.
- **질문**: MultiVeloVAE (Gao 2024) 외 다른 follow-up multi-omic velocity tool (예: chromatin velocity, MIRA, scMOMAT) 비교 필요. 우리 use case에 어느 것이 최적?
- **질문**: 우리 HSPC dataset에 MultiVelo 돌리면 cell cycle confound는 어떻게 처리? regress-out으로 충분? non-cycling subset만 따로 fit하는 ablation 필요?
- **질문**: MultiVelo 결과를 *clinical / regulatory grade* 로 끌어올리려면 어떤 추가 validation (analytical, clinical) 필요? FDA SaMD pathway 적용 시 starting point는?
- **질문**: open-source license 정확 확인 (MIT? Apache 2.0? GPL?) — 우리 commercial product에 embed 시 영향.
- **질문**: 6,968 GWAS SNP → 757 filtered → 3 group 분류 (Fig. 6g) 결과를 우리 hematological malignancy 관련 GWAS SNP에 적용 가능한가? 사내 disease SNP catalog와 cross-reference.
