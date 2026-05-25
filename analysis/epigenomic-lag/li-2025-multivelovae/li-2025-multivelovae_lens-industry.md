# Lens — Industry — Li 2025 MultiVeloVAE

> Citation: `@li2025multivelovae`. 학술적 한계·다음 논문·citation 후보는 `li-2025-multivelovae_lens-academic.md`에 분리. 본 노트는 *산업·규제·BD* 관점. 직접 predecessor `@li2023multivelo`(MultiVelo)와 cross-reference.

---

## 1. Categorization

> 본 섹션 값은 `paper-info.yaml`의 `categorization` 블록과 동기화.

### Domain (자동 추출, 검토 표시)

- `single-cell-genomics`
- `epigenomics`
- `RNA velocity`
- `variational inference` (deep learning)
- `multi-omics`
- `computational-methods`
- (검토: 추가 후보 `hematopoiesis`, `embryonic-development`, `macrophage-differentiation` — 본 paper의 *적용 dataset* 위주이므로 domain보다 application으로 둠)

### Use case (vocabulary 6개 중 1~3개)

- **`methodology-reference`**: continuous coupling/decoupling factor + cVAE multi-sample inference + Bayesian differential dynamics test의 *알고리즘 자체*가 우리 epigenomic-lag 분석에 차용 가능. 특히 우리 HSPC 10x Multiome 외 추가 sample을 통합할 때 필수.
- **`pipeline-applicable`**: 우리 HSPC 10x Multiome dataset에 *코드 그대로* 적용 가능 (Python, scanpy/AnnData 호환). MultiVelo 대비 GPU 가속으로 runtime 단축. 다만 우리 환경에 GPU (RTX 3060 12 GB 이상) 필요 확인.
- **`academic-citation`**: `li-2025-multivelovae_lens-academic.md`의 Citation 후보가 풍부 — proposal/논문 introduction의 multi-omic velocity 분야 *state-of-the-art* reference. MultiVelo (`@li2023multivelo`) 인용 옆에 *후속 method*로 자동 페어링.

### Importance (1개 종합 등급)

- **Level**: 상
- **Perspective (1문장)**: 우리 HSPC 10x Multiome pipeline의 *직접 후속/대체 후보*이며, multi-sample 통합 + continuous (δ, κ) + Bayesian differential test가 MultiVelo로 못 했던 분석을 *바로 가능*하게 해주는 epigenomic-lag topic의 핵심 reference.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**:
  - EB: 4,240 cells × 3,138 genes (신규, single experiment).
  - HSPC×2 integration: 17,667 cells × 892 genes (다른 donor, 같은 protocol).
  - HSPC + macrophage: 9,908 cells × 929 genes (같은 sample의 cytokine treatment paired).
  - HSPC×2 + BMMC scRNA: 27,841 cells × 1,044 genes.
  - 신규 dataset 모두 *single experiment per condition*. inter-donor biological replicate는 HSPC만 2 donor.
  - `해석: cell scale은 *충분히 큼* (모든 dataset 4k+ cells). 그러나 *biological replicate* (donor / experimental session)는 여전히 적음. 의료·임상 grade evidence로는 추가 cohort 검증 필요.`

- **Cohort 편향**:
  - HSPC donor: Fred Hutch Hematology core의 mobilized PBMC, U Michigan IRB exempt — 인종/성별/연령 정보 paper에 미명시. `검토필요: dbGaP phs002915.v2.p1 protocol 확인 필요.`
  - macrophage: 같은 HSPC source의 cytokine-treated (MSM medium, 7-day) — *single donor*.
  - EB: 단일 iPSC line. iPSC line 다양성 미검증.
  - BMMC: ref. 48 Ainciburu 2023, single healthy donor (myeloid malignancy aging study에서 가져온 healthy control). `검토필요: ref. 48 donor 정보 확인 필요.`

- **Replication 부족**:
  - **Cross-cohort replication 없음.** 같은 cell type (HSPC) 결과가 *다른 lab의 published HSPC multi-omic dataset*에서도 재현되는지 미검증.
  - `해석: 두 HSPC sample (Fig. 4)이 *같은 protocol*에서 inter-donor variability를 일부 보여주지만, *완전 independent lab*의 검증은 부재. 본 paper의 모든 priming/decoupling pattern은 *현 시점에서 single lab observation*.`

- **Selection bias**:
  - Gene filtering: highly variable gene + 10% cells expressed threshold (§"Automated data preprocessing"). Threshold sensitivity 분석 부재.
  - Cell QC: MAD (median absolute deviation) 기반 outlier 자동 제거 (Supplementary Fig. 22a). same threshold across all datasets라고만 명시.
  - cell cycle effect: RNA expression에서만 regress out — *unspliced/spliced count는 unchanged*. 이는 MultiVelo (`@li2023multivelo`)와 동일한 한계.
  - Macrophage vs DC: DC cluster n=221, Macrophage n=850. 4배 차이 cluster size에서 Bayes factor가 robust한지 별도 검증 부재.

- **Multiple testing**:
  - Differential dynamics test: posterior expected FDP control (Eq. 25), default α_FDR=0.05.
  - 다만 Fig. 6b volcano plot의 displayed p-values는 *unadjusted* — caption에서 "have been verified to have a False Discovery Rate < 0.05"로 명시이나, 검증 protocol 본문 미상세.
  - `해석: FDR < 0.05 verification은 *self-evaluated posterior expectation* — 실제 calibration (permutation, known null set)은 부재. clinical grade decision making에는 추가 validation 필요.`

### 2.2 임상·기술적 제약

- **Tissue/sample 가용성**:
  - 10x Multiome, scRNA-seq: 일반 lab에서 routine.
  - HSPC: CD34+ FACS sorting 필요. CGT (cell & gene therapy) 회사면 routine.
  - EB / iPSC differentiation: iPSC line 보유 + Aggrewell400 등 plate 필요. 일반 lab에서 setup 가능.
  - macrophage in vitro differentiation: MSM (Myeloid Expansion Supplement II + IL-6) 등 specific cytokine cocktail.

- **장비·시약 가용성**:
  - 10x Chromium + Illumina NovaSeq6000 (standard).
  - STARsolo (ref. 70) alignment — CellRanger ARC와 dual track.
  - Scenic+ + cisTopic + chromVAR + ChromHMM (downstream multi-omic analysis).
  - cross-language stack 부담 적음 — *대부분 Python 환경*. R (Seurat WNN smoothing)이 MultiVelo와 달리 *MultiVeloVAE에선 명시 부재*.

- **계산 자원**:
  - 개발 환경: **Intel i3-12100F + NVIDIA RTX 3060 12 GB + 64 GB RAM, Arch Linux** (§"Development and testing environment", p21).
  - GPU 가속이 *핵심*. MultiVelo는 CPU-only EM이었으나 MultiVeloVAE는 GPU gradient descent.
  - `해석: RTX 3060 12 GB는 *consumer-grade GPU*. 일반 lab 환경에서 접근 가능. cloud HPC 없이도 실행 가능 — 단 우리 워크스테이션의 GPU 보유 여부 확인 필요.`
  - VRAM 12 GB: 27k cell × 1k gene + neural network parameter가 fit하는 수준.
  - `미제공: 100k+ cell scaling 시 VRAM / runtime 추정치 본문 부재. 우리 dataset이 100k 이상이면 batch training + gradient accumulation 추가 필요 예상.`

- **Turnaround time**:
  - Raw FASTQ → CellRanger ARC + STARsolo → preprocessing → MultiVeloVAE training (2-stage EM). 일반적으로 *수 일* (CellRanger 수 시간 + preprocessing 수 시간 + model training 수 시간).
  - MultiVelo 대비 *significantly faster* model training (Fig. 3h) — 단 정확 minute 수치 본문 미보고.
  - `해석: 임상 의사결정 turnaround (수 일 ~ 1주)에 *연구 모드*로는 fit. 단 *real-time clinical decision* (시간 단위)에는 여전히 부적합 — 본 paper의 use case는 research / discovery.`

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**:
  - 본 paper는 *research tool*. 직접적 IVD/LDT/SaMD/drug pathway 해당 없음.
  - 그러나 *companion biomarker discovery*에 활용 시 (예: hematologic malignancy differentiation stage 분류, immunotherapy response prediction), 후속 ASSAY와 함께 *LDT/IVD pathway*에 들어갈 가능성.
  - In silico TF perturbation 기능은 *drug target nomination* 단계의 *exploratory tool* — regulatory에는 추가 wet-lab validation 필수.

- **Analytical / Clinical validation**:
  - Analytical: *self-reported benchmark* (Fig. 2f, 3g) 외에 *FDA-grade* (LOD, LOQ, precision, accuracy, repeatability, reproducibility) 검증 아님. Bayesian differential test의 FDR calibration도 *posterior expected*이지 *empirical*이 아님.
  - Clinical: 없음. 본 paper는 method development.

- **GMP / GLP**:
  - 본 paper는 *research GLP-style*. clinical-grade GMP는 별도 검증 필요.
  - HSPC sample: Stemspan II 7-day + MSM 7-day in vitro 배양 — *research-grade serum-free*. clinical CGT (GMP-grade serum-free, batch release testing) 표준 아님.

- **IRB / consent**:
  - HSPC: Fred Hutch Hematology Core에서 anonymized mobilized PBMC 구매 후 informed consent 확보. U Michigan IRB가 *exempt* 결정 — "the project involves only biological specimens that cannot be linked to a specific individual" (§"Ethics statement", p20). 한국 IRB 기준과 다를 수 있으므로 *우리 환경에 적용 시 별도 IRB review 필요*.
  - EB: iPSC line이 paper에 명시되지 않음 — `검토필요: iPSC line 출처 + ethics 확인 필요. publicly available iPSC line이면 IRB 부담 적음.`
  - BMMC: ref. 48 Ainciburu 2023 (eLife)에서 가져옴 — ref. 48의 ethics 확인 필요.
  - `검토필요: 우리가 본 dataset을 다른 분석에 사용 시 GSE284047 NCBI submission의 human subject protection 정보 확인 필요. raw FASTQ는 dbGaP phs002915.v2.p1로 *restricted access*.`

- **Label·indication**: 해당 없음 (research tool).

- **Reproducibility for audit**:
  - 코드 GitHub open: github.com/welch-lab/MultiVeloVAE, **BSD-3-Clause license** (§"Code availability", p21).
  - Zenodo archive: DOI 10.5281/zenodo.17268254.
  - PyPI 설치 가능.
  - Processed data: figshare DOI 10.6084/m9.figshare.30280333 (post-processed AnnData).
  - Raw data: GEO GSE284047 (processed open) + dbGaP phs002915.v2.p1 (raw FASTQ restricted).
  - `해석: BSD-3-Clause는 *상업 사용 허용* (MIT보다 약간 strict — copyright notice 유지 의무). 우리 commercial product에 embed 가능. paper는 CC BY-NC-ND 4.0 (non-commercial, no derivatives)이지만 *코드는 별도 BSD-3-Clause*라 코드 사용 자유.`

### 2.4 권위·신뢰 가중치

- **출처 1차/2차**:
  - **1차 출처**: peer-reviewed *Nature Communications* (open access, 2025). Welch lab의 flagship multi-omic velocity method paper (MultiVelo 이후 follow-up).
- **Peer review 여부**: peer-reviewed (Hongyu Dong co-reviewed with Yuhao Chen and Boqiang Hu, Jianhua Xing, 그리고 anonymous reviewer가 contributor로 명시 — §"Peer review information", p23).
- **저자 이해상충 (COI)**: "The authors declare no competing interests" 명시 (§"Competing interests", p23).
- **Funding source**:
  - NIH grants — R01AI149669 (K.L.C., J.D.W.), R01HG010883, UM1MH130966 (J.D.W.), F31AI177258 (C.L.), F31AI15504 (M.C.V.).
  - University of Michigan Flow Cytometry Core + Advanced Genomics Core support.
  - *공공 funding only*, corporate sponsorship 없음 → 결과 편향 우려 낮음.
- **Author 첫번째 두 명 equal contribution**: Chen Li, Yichen Gu — 두 명이 main developer.

---

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관의 자산화 가능성**:
  - Joshua D. Welch lab — University of Michigan. 학술 lab, *startup 창업 정보 paper에 없음*. (`질문: LinkedIn / Crunchbase로 Welch lab spin-off 확인. MultiVelo / MultiVeloVAE / VeloVAE / LIGER 등 method 다수 보유 — IP licensing 활동 여부.`)
  - MultiVeloVAE code: **BSD-3-Clause** (Open Source). 우리 commercial product에 *직접 embed 가능* (copyright notice 유지 + Welch lab acknowledgement).
  - Patent: paper에 patent application 명시 없음. 가능성 *낮음* (open-source method paper의 통상 패턴).

- **공동연구 후보**:
  - Welch lab은 *open source, 활발한 GitHub maintenance, PyPI publication, Zenodo archiving* — 공동연구·visiting 친화적.
  - Welch는 single-cell multi-omic 분야 active player. 우리가 HSPC multiome 데이터로 contact할 reasonable angle.
  - paper의 co-author Maria C. Virgilio + Kathleen L. Collins (HSPC wet-lab side) — wet-lab 협업 partner 후보.

- **경쟁사 관찰**:
  - 본 paper와 직접 경쟁: scVelo (ref. 5, Bergen lab, MPI Munich), UniTVelo (ref. 10, Huang lab, HKU), DeepVelo (ref. 11, Cui lab, U of Waterloo), cellDancer (ref. 12, Wang lab), VeloVI (ref. 13, Yosef lab, UC Berkeley), PyroVelocity (ref. 14, Pinello lab, Harvard/MGH).
  - 우리 영역 경쟁사가 MultiVeloVAE를 *언급/사용/extend*했는지 모니터링 필요. paper가 2025년 11월 게재라 *follow-up*은 아직 적을 가능성.
  - MultiVelo (`@li2023multivelo`)가 이미 *de facto standard*로 자리잡은 상태에서 MultiVeloVAE가 *후속 standard*가 될 가능성.

- **시장 영향**:
  - Single-cell multi-omic *tool 시장*의 *state-of-the-art* 유지. 우리가 multi-omic 분석 service 제공 시 *고객 expectation*에 MultiVeloVAE 포함될 가능성.
  - Bayesian differential dynamics test가 *novel*하므로 *patent / SaaS feature*로 차별화 가능.

### 3.2 Commercialization-candidate (자체 제품화)

- **제품 카테고리 후보**:
  - **Software (SW)**: 자체 multi-omic analysis platform 또는 cloud SaaS에 MultiVeloVAE 통합 (BSD-3-Clause 이므로 직접 wrapping). 단순 wrapping은 *차별화 어려움* — 가치는 *vertical-specific UX* (예: HSPC differentiation dashboard, organoid 분화 monitoring)에 있음.
  - **Diagnostic (Dx)**: 직접적 Dx 아님. 단 *differentiation stage signature* (cell-type-specific δ/κ pattern, lineage-specific priming gene)를 *biomarker panel*로 가공하면 hematologic malignancy stratification, immunotherapy response prediction에 활용 가능 (장기 R&D).
  - **Service**: multi-omic differentiation analysis as a *contract service* (CRO offering). MultiVeloVAE + downstream interpretation 일괄 제공.
  - **Therapeutic**: 직접적 therapeutic 후보 없음. 단 *in silico TF perturbation (Fig. 7)*이 *drug target nomination*에 기여 가능 (장기 R&D pipeline).

- **기술적 성숙도 (TRL)**:
  - Method 자체: TRL 4–5 (academic validation 완료, peer-reviewed, open-source, multiple dataset benchmark). MultiVelo 대비 *후속 method이며 더 자세한 statistical framework + GPU production-ready*.
  - 산업 제품화 (SaaS/CRO): TRL 2–3 (concept).

- **IP 자유도**:
  - 본 paper의 method는 open-source (BSD-3-Clause). 우리가 *변형 + 우리 use case 특화*하면 *우리 IP 보호 가능*.
  - Underlying VAE + ODE는 *수학적 model*로 patent 어려움. 단 *specific algorithm + pipeline + UI + GCBDir metric implementation*는 patent 가능.
  - Bayesian differential dynamics test (Eq. 22-25)는 *novel framework* — 변형 patent 가능성 검토 가치.

- **MVP 시나리오**:
  - **MVP 1 — HSPC differentiation dashboard (continuous version)**: 우리 HSPC multi-sample multi-omic dataset → MultiVeloVAE fit → cell-type-specific (δ, κ) heatmap + priming/decoupling gene rank + differential dynamics volcano plot → React/Streamlit UI. 1-2개월 prototyping.
  - **MVP 2 — Multi-sample drug response analyzer**: 약물 처리 vs 미처리 cell multi-omic time-course → MultiVeloVAE cVAE로 두 sample integration + differential dynamics test로 *drug-induced driver gene* 식별. CRO offering or internal R&D tool.
  - **MVP 3 — In silico TF KO simulator**: pre-trained MultiVeloVAE model에 TF gene 입력 → perturbation force UMAP + fate probability change → drug target nomination 후보 자동 추출.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**:
  - 우리 *HSPC 10x Multiome*과 *동일 platform*. dataset 형식 (10x AnnData) 그대로 input. 본 paper의 HSPC dataset이 우리 *완전 같은 cell type + platform*.
  - 우리 organoid multi-omic, neural differentiation system에도 *바로 적용* 가능.
  - 우리가 *추가 sample*을 확보했을 때 cVAE multi-sample inference로 *MultiVelo로 불가능했던 통합 분석* 가능.

- **자원 가능성**:
  - 우리 환경에 GPU (RTX 3060 12 GB 또는 동급 이상) 필요. `질문: 우리 워크스테이션에 GPU 보유 여부 + VRAM 사양 확인 필요.`
  - 메모리: 64 GB RAM 권장. 우리 32 GB 환경에서는 *조심해서 batch size 조정* 필요.
  - 팀 역량 (scanpy, PyTorch, scVI 경험)으로 운영 가능. MultiVelo 운영 경험이 있으면 *직접 transfer*.

- **전략적 방향 fit**:
  - 우리 *epigenomic-lag topic*의 핵심 후속 reference. MultiVelo와 함께 *foundational tool*.
  - 우리가 chromatin–RNA coupling을 quantify하는 *모든 후속 작업*의 starting point — MultiVelo의 *upgrade*.
  - 우리 multi-sample 분석 (예: cohort comparison, drug response time-course)에 *바로 적용 가능*.

- **빠진 capability**:
  - *Wet lab perturbation 검증*: in silico KO 결과는 *예측*이며 wet-lab Perturb-seq 검증 별도 필요.
  - *Spatial multi-omic*: spatial 정보 결합은 별도 framework 필요.
  - *Atlas-level pre-training*: Discussion에서 future work로 언급 — 우리가 직접 구현하면 *unique IP* 확보 가능.
  - *Mature cell type fitting*: 본 paper도 한계 명시 — PBMC 등 mature population에는 부적합.

### 3.4 후속 BD·제품 액션 후보

- **우리 HSPC dataset에서 MultiVeloVAE 실행 (priority 1)**
  - 누가: 본인 (technical lead)
  - 언제: 다음 sprint (2-3주 내)
  - 자원: GPU 환경 1대 (RTX 3060 12 GB+), 코드 install (1일), 우리 dataset preprocessing (3일), MultiVeloVAE fit (수 시간 GPU), 결과 해석 (3일), MultiVelo 결과와 head-to-head 비교 (3일)
  - 성공 기준: ① 우리 HSPC에서 cell-type-specific (δ, κ) gradient 식별, ② MultiVelo discrete 4 state assignment와 confusion matrix, ③ velocity stream이 known lineage hierarchy와 일치, ④ runtime이 MultiVelo 대비 단축 확인.

- **Welch lab contact (전략적)**
  - 누가: 본인 + (BD lead 선택적)
  - 언제: 우리 HSPC + MultiVeloVAE 결과 산출 후 (1-2개월 내)
  - 자원: 이메일 1통, 우리 결과 1-page summary, 우리 dataset 공유 가능성 sounding
  - 성공 기준: ① 협업 가능성 탐색 + ② 우리 dataset이 Welch lab의 future paper에 reference 가능성 + ③ MultiVeloVAE 변형 / atlas-level pre-training 등 *공동 발전* 채널 확보.

- **MultiVelo → MultiVeloVAE migration 사내 결정**
  - 누가: 본인 + 팀
  - 언제: 다음 분기 R&D 리뷰
  - 자원: 비교 결과 슬라이드 5-10장 (우리 HSPC head-to-head + ROI 분석)
  - 성공 기준: 팀이 *MultiVelo를 MultiVeloVAE로 대체 또는 병행*하기로 결정. cell-type-specific 분석이 우리 핵심 question에 가치 추가하는지 평가.

- **License / patent landscape 정밀 검토**
  - 누가: BD lead (외부 IP counsel optional)
  - 언제: 우리가 MultiVeloVAE를 *우리 commercial product*에 embed 결정 시점
  - 자원: BSD-3-Clause LICENSE 확인 (이미 paper에서 명시) + Welch lab patent application 조사 1일
  - 성공 기준: BSD-3-Clause 조건 (copyright notice 유지, attribution) 준수 가능 확인, patent 회피 routes 명시.

- **Bayesian differential dynamics test의 우리 use case 적용** (장기)
  - 누가: 본인 + 통계 담당
  - 언제: 다음 분기 이후
  - 자원: 본 paper §"MultiVeloVAE identifies genes with differential dynamics..." 재구현 1주 + 우리 dataset 적용 1주
  - 성공 기준: 우리 *cohort comparison* (정상 vs 질환 등) 또는 *time-course* (drug treatment) data에서 driver gene 식별 가능.

- **Atlas-level pre-training prototype 검토** (장기, opportunistic)
  - 누가: 본인 + 협력 외부 partner
  - 언제: 6-12개월
  - 자원: HCA / public consortium HSPC + macrophage data 수집, pre-training 코드 변형
  - 성공 기준: pre-trained model이 새 dataset에서 fine-tuning만으로 robust velocity → *우리 IP*로 후속 product.

---

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 상
- **Perspective (1문장)**: 우리 HSPC 10x Multiome pipeline의 *직접 후속/대체 후보*이며, multi-sample 통합 + continuous (δ, κ) + Bayesian differential test가 MultiVelo로 못 했던 분석을 *바로 가능*하게 해주는 epigenomic-lag topic의 핵심 reference.
- **등급 근거**:
  - 본 paper의 HSPC dataset이 *우리 dataset과 동일 platform* + 같은 protocol 계열 (CD34+ STIF expansion). fit 결과 직접 비교 가능.
  - Code (welch-lab/MultiVeloVAE) GitHub open, **BSD-3-Clause** → *우리 commercial product embed 가능*.
  - Continuous (δ, κ) + cell-specific (k_c, ρ)이 우리 *cell-type-specific epigenomic-lag*  연구 question에 직접 매칭.
  - cVAE multi-sample inference는 우리가 추가 sample 확보 시 *바로 적용 가능* — MultiVelo로는 불가.
  - Bayesian differential dynamics test는 우리 *cohort comparison / drug time-course* 분석에 unique value.
  - GPU 가속으로 MultiVelo의 CPU EM 대비 *significantly faster* — 우리 production pipeline에 더 적합.
  - Peer-reviewed Nature Communications, *single-cell multi-omic 분야 standard급 reference*가 될 가능성.
  - 단점: ① cell cycle confound 처리는 본 paper도 *partial* (MultiVelo와 동일 한계 계승), ② mature cell type (PBMC 등) 분석 부적합 (Discussion 명시), ③ inter-donor replication 부족.

### 4.2 활용 우선순위

- **지금 (이번 sprint)**: 우리 HSPC dataset에 MultiVeloVAE 설치 + 실행 → MultiVelo 결과와 head-to-head 비교. *2-3주 안에 결과 1개*.
- **다음 분기**: ① 결과 R&D 리뷰 발표 + ② MultiVelo → MultiVeloVAE migration 결정 + ③ Welch lab contact (필요 시) + ④ multi-sample 통합 use case (예: 추가 donor HSPC dataset 확보 후) 시범 적용.
- **장기**: ① cell cycle confound 사내 sub-pipeline 개발 (MultiVelo + MultiVeloVAE 공통 한계 해결), ② Bayesian differential dynamics test의 cohort comparison 활용, ③ atlas-level pre-training prototype (우리 IP 후보), ④ in silico TF perturbation을 drug target nomination에 활용.

### 4.3 발표·미팅에서 들이밀 시점

- **본인 학회 발표 / 본인 논문 introduction**: RNA velocity의 *multi-omic + multi-sample + statistical testing* state-of-the-art로 인용. MultiVelo 옆에 *후속 method*로 자동 페어링.
- **사내 R&D 리뷰**: 우리 HSPC 분석 결과 발표 시 backbone method로 명시. MultiVelo 대비 cell-type-specific gradient 가시화 + multi-sample 통합 가능성 강조.
- **BD 미팅**: 우리 multi-omic analysis capability를 *외부에 시연*할 때 MultiVeloVAE 결과 + Bayesian differential dynamics test를 deck에 포함. 차별화 포인트.
- **외부 컨퍼런스 / 키노트**: epigenomic regulation + RNA velocity 관련 발표면 *state-of-the-art reference*로 인용.
- **사내 newsletter**: MultiVelo → MultiVeloVAE 전환의 *사내 알림*.

### 4.4 추가 탐색 필요 영역

- **질문**: 우리 워크스테이션의 GPU 환경 (RTX 3060 12 GB 이상?) 확인 필요. 미보유면 cloud GPU 또는 GPU upgrade 계획 필요.
- **질문**: Welch lab이 MultiVeloVAE 관련 startup 창업했는지 LinkedIn / Crunchbase 확인 필요. → BD-opportunity 평가에 영향.
- **질문**: 우리 HSPC dataset에 MultiVeloVAE 돌리면 cell cycle confound는 어떻게 처리? MultiVelo와 동일하게 RNA에서만 regress out? 우리가 추가 ablation (cell cycle phase별 separate fit) 수행할 가치 있나?
- **질문**: BSD-3-Clause 조건 (copyright notice 유지)가 우리 SaaS deployment에서 어떤 형태로 노출되어야 하는가? frontend / API docs 둘 다 attribution 필요?
- **질문**: MultiVeloVAE의 in silico TF KO (Fig. 7e-h)가 우리 *drug target nomination* workflow에 직접 활용 가능한가? wet-lab 검증 candidate gene 1-3개 선정에 어떻게 활용?
- **질문**: Bayesian differential dynamics test (Fig. 6)의 *FDR calibration*이 우리 use case (e.g., 정상 vs 질환 cohort)에서 어떻게 검증할 것인가? known null gene set (housekeeping)에서 nominal vs realized FDR 확인 protocol 설계 필요.
- **질문**: 본 paper에서 발견된 PROS1 / LGMN / LGALS3 macrophage driver gene이 우리 macrophage / immune 분석에 활용 가능한 *biomarker candidate*인가? 사내 catalog와 cross-reference.
- **질문**: 27,841 cell partial integration (Fig. 7) 결과의 *practical limit*는? 우리 cohort study 시 어느 정도 sample 수까지 통합 가능 (VRAM 12 GB 기준)?
- **질문**: GSE284047 (신규 dataset 3종) processed AnnData를 figshare에서 다운로드해 우리 lab의 *외부 reference baseline*으로 활용 가능한가? license 확인.
