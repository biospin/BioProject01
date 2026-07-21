# Lens — Industry — Hong 2026 MoFlow

> Citation: `@hong2026moflow`. 학술적 한계·다음 논문·citation 후보는 `hong-2026-moflow_lens-academic.md`에 분리. 본 노트는 *산업·규제·BD* 관점. 직접 sibling `@li2025multivelovae`(MultiVeloVAE)와 cross-reference 빈번.

---

## 1. Categorization

> 본 섹션 값은 `paper-info.yaml`의 `categorization` 블록과 동기화.

### Domain (자동 추출, 검토 표시)

- `single-cell-genomics`
- `epigenomics`
- `RNA velocity`
- `deep learning` (PyTorch / DNN)
- `multi-omics`
- `computational-methods`
- `chromatin-rna-coupling`
- (검토: 추가 후보 `neurodevelopment` — 4개 dataset 중 3개가 brain. application 위주이므로 domain은 *method*에 집중)

### Use case (vocabulary 6개 중 1~3개)

- **`methodology-reference`**: MoFlow의 *relay velocity + chromatin-aware 두 DNN + 2-stage 학습* 구조는 우리 epigenomic-lag 분석에 *직접 차용 또는 변형* 가능. *latent time-free*라는 design choice가 우리 cell-cycle confounded HSPC dataset에 적합한지 검토.
- **`pipeline-applicable`**: 우리 HSPC 10x Multiome dataset에 *코드 그대로* 적용 가능 (PyTorch Lightning, Python). MultiVelo와 동일 preprocessing 입력. *MultiVeloVAE와 동시 운영* 권장 (lens-academic § "MoFlow vs MultiVeloVAE 비교" 참조).
- **`academic-citation`**: `hong-2026-moflow_lens-academic.md`의 Citation 후보 참조. *epigenomic lag biology의 mechanistic interpretation* (Fig. 7) reference, *MultiVelo gene-specific latent time over-correction*의 정량 evidence (Fig. 3g, 129 reversal gene) reference.

### Importance (1개 종합 등급)

- **Level**: 상
- **Perspective (1문장)**: 우리 epigenomic-lag 연구의 *직접 적용 candidate* + `@li2025multivelovae` 와 함께 *post-MultiVelo extension의 두 갈래 baseline*. MoFlow의 *latent-time-free + DAC + DTW lag* 분석이 우리 연구 outcome (gene별 chromatin–RNA lag 정량 + drug response timing 예측)과 정합.

---

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size**:
  - Human Brain: 4,693 cells × 842 genes (본문 명시).
  - Mouse Skin: 본문 `미제공:` — `해석: Ma 2020 + Li 2023 처리 따라 ~6,000 cells 수준 추정.`
  - Mouse Brain (E18): 본문 `미제공:` — `해석: 10x Genomics 5k dataset 따라 ~5,000 cells 수준 추정.`
  - HSPC: 본문 `미제공:` — `해석: Li 2023 따라 ~11,605 cells 수준 추정.`
  - 모든 dataset이 *이전 publication 재사용* — *MoFlow paper에서 신규 생산 데이터 0개*.
  - 본문에 cell·gene 수가 *4개 중 1개만* 명시. `검토필요: 정확한 수치는 reference dataset (Trevino 2021, Ma 2020, Li 2023) 참조 필요.`

- **Cohort 편향**:
  - 4개 dataset 모두 *서로 다른 cohort + 서로 다른 platform* — *cohort-specific bias 분산 효과*는 있음.
  - 그러나 *동일 cohort 내 multi-donor*는 1개도 없음. 모든 dataset이 *single source*.
  - 인종/성별/연령 정보: human brain (Trevino 2021), HSPC (Li 2023)는 각각 *original publication 참조* — MoFlow 본문에 추가 정보 없음. `검토필요: 우리가 이 method를 우리 cohort에 적용할 때 동일 demographic profile 가정이 적절한지 확인.`
  - mouse dataset 2개 (skin, brain): mouse strain, 성별, 나이 본문 미명시.

- **Replication 부족**:
  - **Cross-cohort replication 없음.** MoFlow의 모든 결과가 *single dataset per cell type* — 다른 lab의 같은 cell type dataset에서 재현 미검증.
  - **MultiVelo 비교의 robust 검증 부재**: MultiVelo CBDir 0.211 (human brain)이 MultiVelo *original paper* (`@li2023multivelo`)의 같은 dataset 결과와 일치하는지 확인 부재. `검토필요: preprocessing parameter 차이로 인한 변동성 가능.`
  - 본 paper의 모든 결과는 *현 시점에서 single lab observation*. `해석: clinical / regulatory grade 검증으로는 추가 cohort 필요.`

- **Selection bias**:
  - Gene filtering: WNN smoothing + Li 2023 preprocessing 기반. 본 paper에서 *추가 gene QC* 본문 명시 없음.
  - Cell QC: reference dataset의 *기존 QC*를 그대로 사용. *threshold sensitivity* 본문 부재.
  - cell-cycle effect: 본 paper 본문에서 *cell-cycle regression 언급 부재*. `검토필요: Li 2023 preprocessing에서 cell-cycle regress out된 dataset을 그대로 사용한 것으로 추정 — 우리 데이터 적용 시 명시적 처리 필요.`
  - m1/m2 score 90th percentile threshold (Supp Fig. 6): *Mouse Skin은 90% 이상에서만 significant*. *dataset-specific tuning* 필요 — clinical-grade *robust default*가 없는 점.

- **Multiple testing**:
  - Fig. 2f, g, j, 4f, Supp Fig. 4b: 2-sided t-test, p < 0.001 ***. *adjustment 본문 부재*.
  - Fig. 5c: Mann–Whitney U test, 4 group pairwise. *adjustment 본문 부재*.
  - Fig. 7e: one-sided KS test, 16 cluster × 4 half-life type = 64 test. *adjustment 본문 부재* — `검토필요: Bonferroni / BH adjustment 필요`.
  - Fig. 7g: Fisher's exact, 12 cluster × 2 gene set = 24 test. *adjustment 본문 부재*.
  - Supp Data 1–3 (GO enrichment): DAVID `PValue` 보고, *FDR 명시 부재*. `검토필요: DAVID 자체에서 FDR (Benjamini) column이 있는지 xlsx 추가 확인 필요.`
  - `해석: GO enrichment p-value를 직접 인용 시 *non-corrected p*임을 인지. clinical decision-making에는 추가 validation 필요.`

### 2.2 임상·기술적 제약

- **Tissue / sample 가용성**:
  - 10x Multiome (RNA + ATAC): 표준 commercial assay. *일반 lab에서 routine*.
  - SHARE-seq: 학술 protocol — 보다 specialized. commercial 가능 vendor 제한적.
  - 우리 *HSPC 10x Multiome*는 *direct applicable* — protocol overlap 완벽.

- **장비 · 시약 가용성**:
  - 10x Chromium controller + Illumina NovaSeq6000: 표준.
  - velocyto + scanpy + scVelo + Seurat v4 WNN: open-source Python + R stack.
  - PyTorch Lightning: open-source.
  - DAVID, GSEApy: open-source.
  - cross-language 부담: R (Seurat WNN) + Python — *MultiVelo와 동일*.

- **계산 자원**:
  - GPU: *paper 본문 부재* — `미제공:`. Reporting Summary도 hardware 정보 부재.
  - `해석: PyTorch Lightning + DNN 학습이므로 GPU 권장. CPU도 가능하나 *training time*이 길 가능성.`
  - VRAM 요구: 본문 미명시. DNN architecture (3-layer 64-48-32)는 *작은 편* — 소비자급 GPU (RTX 3060 12 GB 수준) 충분 예상.
  - `해석: MultiVeloVAE는 RTX 3060 12 GB + 64 GB RAM 명시. MoFlow도 비슷한 수준일 것으로 추정 — *우리 워크스테이션의 GPU 보유 여부 확인 필요*.`
  - 100k+ cell scaling: `미제공:` — 본 paper의 dataset이 모두 ~5,000–11,605 cells 수준. *우리 데이터가 더 크면 batch training 전략 필요할 수 있음*.

- **Turnaround time**:
  - Raw FASTQ → Cell Ranger ARC + velocyto → preprocessing → MoFlow 학습 (max 200 epoch, early stopping).
  - 본문 명시 runtime 부재 — `미제공:`.
  - `해석: MultiVelo가 HSPC dataset에서 124 min (12-thread CPU)이라 가정 시, MoFlow는 GPU + DNN이므로 *수십 분 ~ 1시간* 수준 추정. 단 정확 수치 없음.`
  - 임상 의사결정 turnaround (수 일 ~ 1주)에 *research 모드*로는 fit. *real-time clinical decision* (시간 단위)에는 부적합.

### 2.3 규제·QA·RA 관점

- **FDA / EMA pathway**:
  - 본 paper는 *research tool*. 직접적 IVD / LDT / SaMD / drug pathway 해당 없음.
  - 우리가 MoFlow를 *companion biomarker discovery* (예: hematologic malignancy의 분화 stage 분류, drug response timing 예측)에 활용 시 *후속 ASSAY* + clinical validation 필수.
  - epigenomic-lag 정량이 *drug response timing prediction*으로 발전 시 *prognostic biomarker pathway* (예: FDA *Software as a Medical Device*) 가능 — 단 추가 임상 validation 단계 필요.

- **Analytical / Clinical validation**:
  - Analytical: *self-reported CBDir* (Supp Table 1) 외 *FDA-grade* (LOD, LOQ, precision, accuracy, repeatability, reproducibility) 검증 *아님*.
  - Clinical: 없음. 본 paper는 method development.
  - *Single-seed*, *single-run* 결과 — variance / reproducibility 본문 미보고. `검토필요: 우리가 적용 시 multiple random seed 학습 + variance 측정 필요.`

- **GMP / GLP**:
  - 본 paper는 *research grade*. 모든 dataset이 *publicly available secondary data analysis* — IRB / ethics는 *original publication* 차원.
  - Stemspan II + CD34+ HSPC 같은 *clinical CGT GMP* 표준 없음 (Li 2023 dataset 그대로 재사용).

- **IRB / consent**:
  - 본 paper의 모든 dataset이 *secondary analysis* — primary IRB 없음.
  - human brain (Trevino 2021): *original publication ethics 참조*. fetal cortex data.
  - HSPC (Li 2023): Fred Hutch Hematology Core mobilized PBMC, U Michigan IRB exempt.
  - 우리 환경에 적용 시 *우리 환자/donor IRB review 별도 필요* (한국 기관 기준).

- **Label · indication**: 해당 없음 (research tool).

- **Reproducibility for audit**:
  - 코드: https://github.com/AriHong/MoFlow (PyTorch Lightning).
  - Zenodo archive: DOI 10.5281/zenodo.17666878 (Hong 2025, ref. 47).
  - License: `검토필요:` — paper Code availability에 license 명시 없음. GitHub 페이지 직접 확인 필요.
  - Demo notebook: GitHub `/notebook` directory에 있다고 Reporting Summary 명시.
  - Hyperparameter: default 값만 본문에 (learning rate 0.001, weight decay 0.04, layer (64, 48, 32), 20 epoch warm-up, 200 epoch max, 40 neighbor, 90th percentile m1/m2 threshold). *사용자 modifiable* via command line interface.
  - `해석: open-source 코드 + Zenodo archive + Demo notebook으로 reproducibility 기본 보장. 단 license 부재 시 *상용 사용 제약* — 우리 사내 / 외부 BD 시 검토 필요.`

### 2.4 결과의 신뢰도 (정량 evidence 강도)

- **강한 evidence**:
  - 4-dataset × 4-method CBDir matrix (Supp Table 1) — MoFlow가 4/4 best, 격차도 명확.
  - MultiVelo Model 1/2 gene과 MoFlow m1/m2 score의 정합 (p < 0.001 ***, multi-dataset Fig. 2f, g, 4f, Supp Fig. 4b).
  - cell-type-specific transcriptional state heterogeneity in mGPC/OPC (Fig. 3c).
  - 129 gene이 MultiVelo gene-specific time에서 75% bin sign reversal (Supp Fig. 2c, d).
  - Cluster 0 GO BP enrichment in mouse brain: cell division p = 5.20e−42 (Supp Data 3).
  - LCHA group GO BP enrichment: chromosome segregation p = 0.0019 (Supp Data 2 `lcha_GO`).

- **중간 evidence**:
  - Hephl1, Padi3, Myo10, Notch1, Trps1, Wnt3 gene velocity 정확도 (Fig. 4g, 5d) — 정성 비교 위주.
  - DNA damage response gene의 RG checkpoint function (Fig. 6g, Supp Fig. 4f-h) — `해석: 외부 reference 인용으로 가설 정립`.
  - Cluster 10 polycomb/speckle 가설 (Fig. 7g, Khyzha 2025 ref. 44) — `해석: MALAT1, XIST 포함 시 circular reasoning 가능성`.

- **약한 evidence**:
  - Hyperparameter sensitivity (Supp Fig. 6의 m1/m2 threshold만, 다른 hyperparameter ablation 없음).
  - Single-run results — variance 미보고.
  - MultiVelo와 cellDancer 결과가 *each method의 original publication과 일치*하는지 확인 부재.

- **결론**: research grade evidence 충분. clinical / regulatory 사용에는 *추가 robust validation 필요*.

---

## 3. BD value & 상용화 가능성

### 3.1 BD value (외부 자산 라이선싱·공동연구·경쟁사)

- **License**: paper는 CC BY-NC-ND 4.0 (Creative Commons, *commercial 사용 금지*, *adapted material 재배포 금지*). 코드 license 부재 (`검토필요:`).
- **Commercial use**: paper 자체는 *non-commercial only* — 상업적 분석 서비스 제공 시 *코드 license 확인 + 저자 연락 필요*.
- **공동연구 / 라이선싱 후보**:
  - **Seoul National University Hospital (Kwangsoo Kim, corresponding)** — 한국 내 임상 데이터와 결합 시 *natural collaboration partner*. KNIH grant (2024-ER-0801-01) funded.
  - **Inha University AI Department (Sangseon Lee, corresponding)** — AI Convergence Innovation Human Resources Development (RS-2022-00155915) IITP grant + Bio&Medical Technology NRF (RS-2022-NR067309) funded. AI methodology refinement에 협업 가능.
  - **Seoul National University Bioinformatics (Ari Hong, first author)** — Basic Science Research Program (RS-2024-00410829) MOE funded.
  - `해석: 한국 내 연구진 — 우리 (kkkim) 같은 한국 환경 적용 + 공동연구에 *언어 / 시간대 / 협업 효율* 좋음.`
- **경쟁자**:
  - **MultiVelo (`@li2023multivelo`)** — Welch lab (U Michigan). Open-source MIT-style (예상). 가장 성숙한 multi-omic velocity framework.
  - **MultiVeloVAE (`@li2025multivelovae`)** — Welch lab. BSD-3-Clause license. *직접 sibling*.
  - **cellDancer (Li 2024, Nat Biotechnol)** — Shengyu Li et al. 개발. open-source.
  - **scVelo (Bergen 2020)** — Helmholtz Munich. open-source MIT.
  - `해석: MoFlow는 Welch lab의 *MultiVelo + MultiVeloVAE 강자*와 *직접 경쟁 / 보완* 위치. 단 *한국 발*이라는 점이 한국 내 협업/BD에는 advantage.`

### 3.2 자체 제품화 (Dx / assay / SW / therapeutic)

- **Dx (진단 키트)**: 직접 candidate 아님. 그러나 *epigenomic lag biomarker*가 향후 *prognostic / predictive biomarker*로 확립 시, MoFlow가 *biomarker discovery tool*로 사용. 직접 제품화는 *bioinformatics service / SaaS* 형태 가능.

- **Assay (분석 service)**:
  - 우리가 *HSPC multiome 분석 service* 제공 시 MoFlow를 *internal tool*로 활용 가능 (단 license 확인 필요).
  - service offering: "HSPC differentiation trajectory 분석 + epigenomic lag 정량 + drug response timing 예측 report".
  - 가격대: *1 sample 기준 수백만 원 ~ 1천만 원* 수준 (multi-omic library prep + sequencing + bioinformatics).

- **SW (software product / SaaS)**:
  - MoFlow 자체는 *non-commercial* — 우리 SaaS에 직접 embed 불가.
  - 대신 *MoFlow의 algorithm을 reference로 한 우리 자체 implementation* + *우리 cohort에 fine-tuned model* 가능.
  - SaaS 형태: cloud-hosted multi-omic velocity pipeline (Google Colab / AWS) + GUI report — 기존 *Loom / Scanpy / scVelo* 기반 service 위에 *post-MultiVelo extension 추가*.

- **Therapeutic discovery**:
  - MoFlow가 *DNA damage response gene의 RG-specific transcriptional activation* 발견 (Fig. 6) — *brain progenitor cell의 stress response*가 *therapeutic target* 후보. 그러나 *target nomination tool*로의 응용은 추가 validation 필요.
  - MoFlow는 *in silico perturbation 미지원* — drug target nomination에는 `@li2025multivelovae` 또는 Dynamo / CellOracle와 결합 필요.

- **결론**: MoFlow 자체의 *직접 제품화*보다는 *우리 bioinformatics service* 또는 *우리 자체 implementation의 reference algorithm*으로 활용. *우리 epigenomic-lag 연구의 outcome (drug response timing prediction)을 product화*할 때 MoFlow를 *building block 중 하나*로.

### 3.3 우리 epigenomic-lag pipeline에 BD-value 추정

- **시나리오 A — MoFlow를 우리 HSPC pipeline에 직접 통합**:
  - **가치**: MultiVelo 외에 *latent-time-free + cell-specific kinetic* 결과로 *robust dual-method analysis*. backflow / over-correction 양쪽 위험 분산.
  - **비용**: 2-3주 sprint (install + GPU 환경 검증 + preprocessing + fit + 결과 해석).
  - **ROI**: 우리 pipeline의 *결과 신뢰도 증가*. method-specific artifact 방어.

- **시나리오 B — MoFlow + MultiVeloVAE 두 method 동시 운영 (분석자 권장)**:
  - **가치**: 두 framework의 *agree/disagree 영역*을 cross-validation으로. 단일 method 의존의 false discovery 방지.
  - **비용**: 4-6주 sprint (MoFlow + MultiVeloVAE 각각 적용 + 결과 비교 + cross-validation report).
  - **ROI**: 우리 *epigenomic-lag biomarker* 후보의 *high confidence* 결과. *publication / IND / clinical trial design*에 사용 가능한 *robust evidence*.

- **시나리오 C — MoFlow algorithm을 우리 자체 implementation의 reference**:
  - **가치**: MoFlow의 *core insight* (latent time-free + chromatin scenario selection + 2-stage 학습)를 우리 자체 코드로. *license 제약 회피* + *우리 data에 customize*.
  - **비용**: 2-3개월 sprint (코드 작성 + validation + benchmark).
  - **ROI**: long-term *우리 IP* + *cross-paper extension* 가능 + *SaaS product* base.

---

## 4. 전문가 코멘트 (등급 + 우선순위)

### 4.1 종합 등급

- **MoFlow paper 자체 등급**: 상.
- **이유**: ① 우리 *epigenomic-lag 연구 주제와 직접 정합* — Fig. 7의 c-s lag 분석 + DAC-based gene grouping이 우리 outcome (gene별 chromatin–RNA lag 정량 + drug response timing 예측)과 1:1 mapping. ② `@li2025multivelovae`와 함께 *post-MultiVelo extension의 두 갈래 baseline*. ③ 한국 발 paper로 *공동연구 / 협업 advantage*. ④ open-source code + Demo notebook으로 *재현 부담 낮음*.

### 4.2 우선순위 (3개월 horizon)

- **즉시 (1-2주)**: 본 paper full analysis 완료 (✓ 본 노트 + core/lens 작성으로 완료).
- **단기 (2-4주)**: 우리 HSPC dataset에 MoFlow 적용 + MultiVelo / MultiVeloVAE와 head-to-head 비교. 정확한 CBDir / runtime / memory + cell-type-specific score 비교.
- **중기 (1-3개월)**: MoFlow의 *cluster 10 polycomb/speckle 발견*이 우리 HSPC에서 재현되는지 확인. *general mechanism*인지 *brain-specific*인지 판단.
- **장기 (3-6개월)**: 두 method (MoFlow + MultiVeloVAE)의 결과를 *cross-validated epigenomic lag biomarker*로 정립. paper / proposal submission.

### 4.3 활용 시나리오 (구체 예)

- **시나리오 1 — 우리 HSPC pipeline 1차 적용**:
  - Input: 우리 HSPC 10x Multiome data (donor 1–N).
  - 처리: WNN smoothing + Li 2023과 동일 preprocessing → MoFlow 학습 (default hyperparameter) → CBDir 측정 + cell type별 velocity stream + gene별 m1/m2 + DAC$\alpha$ + DAC$c$ + DTW c-s lag.
  - Output: ① 우리 데이터의 *HSPC bifurcation trajectory accuracy* CBDir 수치, ② cluster별 GO BP enrichment + LCHA / HCHA / HCLA / LCLA grouping, ③ chromatin–RNA negative lag gene 후보 list + cluster 10-type unique pattern 발견 여부.
  - 결과 활용: 우리 연구 main result + MultiVeloVAE 결과와 cross-validation.

- **시나리오 2 — 우리 자체 epigenomic-lag biomarker 식별**:
  - MoFlow + MultiVeloVAE 양쪽에서 *agree하는 high-confidence gene* 추출.
  - 우리 HSPC에서 *drug response timing prediction의 feature*로 사용 — baseline epigenomic feature → gene별 lag → drug response timing.
  - 우리 paper / proposal의 *novel contribution*: "Dual-method consensus epigenomic lag biomarker".

- **시나리오 3 — 한국 KAIST / SNUH / Inha University 공동연구**:
  - 본 paper 저자 (Ari Hong, Sangseon Lee, Kwangsoo Kim) 한국 거점.
  - 공동 grant proposal (NRF / KNIH / IITP) — *MoFlow + 우리 HSPC pipeline 통합* 또는 *MoFlow extension* 주제.
  - 협업 가치: ① 저자의 *MoFlow internal know-how* 직접 access, ② 한국 환경 데이터 결합, ③ Korean Cell Atlas 같은 *national-level 자원*과 연계 가능성.

### 4.4 본인 재회고 (의사결정자 1인 시점)

- **이 paper를 어떤 시점에 다시 펴봐야 하는가**:
  - 우리 HSPC 10x Multiome dataset이 *준비될 때마다* MoFlow 적용 vs MultiVeloVAE 비교 — *standard workflow에 통합*.
  - `@li2025multivelovae`와의 head-to-head 비교 결과 review 시.
  - 우리 *epigenomic-lag biomarker* publication 작성 시 — Methods + Discussion에서 MoFlow 비교 인용.
  - 우리 *drug response timing prediction* 모델의 feature engineering 단계 — m1/m2 / DAC / DTW lag 같은 MoFlow feature 차용 가능성 검토.
  - 한국 내 협업 grant proposal 작성 시 — 저자 그룹과의 collaboration 후보.

- **본인 우려**:
  - **우려 1**: GPU 사양 / runtime / scaling 정보 *완전 부재* — 우리 인프라 fit 확인이 첫 단계.
  - **우려 2**: Ablation 부재 + single-run results — 우리가 직접 ablation 수행하지 않으면 *어떤 hyperparameter가 결정적*인지 모르고 진행해야.
  - **우려 3**: cluster 10 polycomb/speckle 발견의 *circular reasoning* 위험 — MALAT1, XIST 제외 후 재현 필요.
  - **우려 4**: CBDir 단일 metric — `@li2025multivelovae`의 GCBDir이 더 robust. 우리가 직접 GCBDir 측정 필요.
  - **우려 5**: 신규 dataset 부재 + multi-sample 통합 부재 — 우리 *multi-donor HSPC* 시나리오에 *limit*.
  - **우려 6**: Code license 부재 (`검토필요:`) — *상업적 사용* 또는 *우리 SaaS embed* 시 author 직접 contact 필요.

- **본인 action 결정**:
  - **(1) MoFlow를 *primary analysis tool 중 하나*로 등록** — 우리 epigenomic-lag pipeline의 *MultiVelo / MultiVeloVAE와 동급 baseline*. importance: 상.
  - **(2) 다음 sprint (2-3주)에서 head-to-head 비교 실행** — 동일 input HSPC dataset → MoFlow + MultiVeloVAE → CBDir + GCBDir + runtime + cell-type-specific score confusion matrix.
  - **(3) Cluster 10 발견의 *우리 HSPC 재현 확인*** — sprint 결과의 sub-task.
  - **(4) 저자 직접 contact** — license 확인 + 한국 내 collaboration 가능성 탐색 (Sangseon Lee, Kwangsoo Kim).

### 4.5 임원·BD 의사결정자에게 한 줄 요약

- **MoFlow는 우리 HSPC 10x Multiome pipeline의 *post-MultiVelo extension*의 *두 갈래 중 하나* — `@li2025multivelovae`와 동시 운영하여 *epigenomic-lag biomarker의 cross-validated discovery*를 가능하게 한다. 한국 발 paper로 *공동연구 advantage* 있음. 단 *상업적 license + scaling 정보* 사전 확인 필요.**

---

## 5. 부록 — 기록·검토 메모

### 5.1 미해결 질문 (analyst → user)

- `질문 1`: 우리 워크스테이션의 GPU 사양 (model, VRAM)? MoFlow가 *최소 어떤 GPU에서 동작*하는지 paper 미명시 — 우리 인프라 fit 확인 필요.
- `질문 2`: 우리 HSPC dataset의 정확 cell·gene 수? Li 2023 dataset 그대로 사용 vs 우리 자체 produce 여부.
- `질문 3`: MoFlow를 *상용 분석 service*에 embed할 의향 있는가? license (`검토필요:`) 확인 필요.
- `질문 4`: 저자 그룹 (Ari Hong, Sangseon Lee, Kwangsoo Kim)과 *공동연구 / collaboration*을 추진할 의향 있는가? 한국 내 grant matching 가능성.

### 5.2 추가 자료 fetch 필요

- `미제공`: github.com/AriHong/MoFlow 의 *license file* — 직접 GitHub fetch 필요.
- `미제공`: MoFlow의 *runtime + GPU 사양* — 코드 README 또는 issue tracker 확인.
- `미제공`: 4개 dataset의 정확한 cell·gene 수 (3개는 본문 명시 안 됨) — original dataset publication 또는 Li 2023과 비교.
- `미제공`: MoFlow가 *commercial license*로 추가 가능한지 — author 연락 필요.

### 5.3 분석 노트 자체에 대한 본인 self-note

- 본 분석은 `sources/hong-2026-moflow.pdf` (17 page main) + Supp 6종 (Supp-1 tables, Supp-2 description, Supp-3/4/5 xlsx, Supp-6 reporting summary) + `sources/abstract.txt`만을 근거로 한다. 외부 지식은 *모두* `해석:` / `외부 맥락:` / `미제공:` / `검토필요:` / `질문:` prefix로 분리.
- 가장 모호한 영역: GPU 사양 / runtime / scaling — 본 paper 전체 + Reporting Summary에 hardware 정보 부재.
- 가장 강한 evidence: Supp Table 1의 4-dataset × 4-method CBDir matrix + 본 paper의 *epigenomic lag mechanism interpretation* (Fig. 7 cluster 10 + half-life KS test + polycomb/speckle Fisher's exact).
- 가장 약한 evidence: ablation 부재, single-run results, hyperparameter sensitivity 미검증, cluster 10 결과의 MALAT1/XIST circular reasoning 위험.
- Cross-reference: `@li2023multivelo` (MultiVelo) + `@li2025multivelovae` (MultiVeloVAE)와 항상 함께 검토. 세 paper가 우리 *epigenomic-lag 연구의 핵심 method triplet*.

---

## 6. 결론 — 분석자의 한 줄

- **MoFlow는 우리 epigenomic-lag 연구의 *직접 적용 candidate*이며 `@li2025multivelovae`와 *post-MultiVelo extension의 두 갈래 baseline* 위치에 있다. 즉시 head-to-head 비교 + 우리 HSPC dataset에서 cluster 10-type 재현 확인 sprint를 권장한다.**

---
