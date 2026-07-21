# Lens — Industry — Cui 2024 DeepVelo

> `@cui2024deepvelo` — `Genome Biology` 25:27 (2024). DOI: 10.1186/s13059-023-03148-9. Open Access (CC BY 4.0). Code: github.com/bowang-lab/DeepVelo (MIT license). 분석 근거: `cui-2024-deepvelo_core.md`, `cui-2024-deepvelo_lens-academic.md`, sources/cui-2024-deepvelo.pdf.

## 1. Categorization

> 이 섹션은 `paper-info.yaml`의 `categorization` 블록과 동기화된다.

### Domain (자동 추출, 검토 표시)

- `single-cell-genomics`
- `RNA velocity`
- `deep-learning`
- `single-cell-transcriptomics`
- `(secondary)` `tumor-heterogeneity` — PA application (Fig. 7).

### Use case (vocabulary 6개 중 1~3개)

- **`methodology-reference`** — 우리 MoFlow / MultiVeloVAE 후속 분석에서 *cell-specific kinetics rationale의 직접 source*. continuity assumption + GCN message passing은 *우리 future epigenomic-lag method 설계의 학습 framework 후보*.
- **`academic-citation`** — 본인 논문 / 제안서 introduction에서 *RNA velocity 2세대 (cell-specific rate)*의 motivation 인용. *multifaceted gene 비율 0.58* 같은 통계는 *cell-specific method 필요성*의 quantitative quotation으로 유용.
- (선택적) **`BD-opportunity`** — Bo Wang 그룹은 Vector Institute / UHN 기반의 *active velocity·multi-omic 연구 hub*. 향후 *공동연구·라이선싱 candidate watch list*에 포함 의미 있음.

### Importance (1개 종합 등급)

- **Level**: 중
- **Perspective**: DeepVelo는 RNA-only로 *epigenomic-lag direct method가 아님*. 그러나 *MoFlow / MultiVeloVAE / cellDancer / VeloVAE 후속 method의 정확한 background reference*로서 *method genealogy 분석에 필수*. 우리 파이프라인 직접 적용은 unlikely, *citation + methodology insight 활용*이 우선.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크

- **Sample size 다양함**:
  - 발달 dataset: dentate gyrus $n = 2{,}930$ cells, organogenesis 30,000 cells, hindbrain n cell 미명시.
  - PA tumor: $n = 3$ patient (Sample 1: 1,644 tumor cell; Sample 2: 3,669; Sample 3: 3,054). *임상 연구로는 매우 작은 cohort* — *prognostic biomarker generalization 어려움*.
- **Cohort 편향**:
  - 모든 발달 dataset *mouse*.
  - PA *3 patient 모두 male, age 7–15* — *sex / age / disease subtype generalization 부재*.
  - 다양한 organ / 다양한 종 / 다양한 disease state benchmark 없음 — *human adult tissue evidence 부재*.
- **Replication 부족**:
  - PA discovery (immunogenicity heterogeneity)가 *3 patient 모두에서 동일 패턴*은 *convergent evidence*지만 *external cohort validation* 없음. `해석:` $n=3$ cohort로는 *regulatory-grade evidence* 부족.
- **Selection bias**:
  - PA 분석은 *tumor cell만 추출 (microglia, T-cell 제외)*. selection 자체는 합당하나 *tumor / microenvironment 경계 cell* (e.g., epithelial-immune crosstalk)이 *손실*될 가능성.
  - QC threshold: mitochondrial < 5%, non-zero gene > 200 (Seurat default) — *standard*. 그러나 *threshold-sensitivity analysis 없음*.
- **Multiple testing**:
  - Mann-Whitney U $p$-value 보고 시 *BH correction 명시 없음* (method 비교 자체는 single test로 정당화 가능).
  - Pathway enrichment는 FDR-corrected (ActivePathways) — 적절.
  - PA pathway 분석은 *sample × branch × pathway*의 multi-level test — multiple testing burden 명시 부족.
- **검토필요**: PA에서 *3 sample 사이의 cross-sample comparison*에 대한 statistical model (random effect, hierarchical Bayes 등) 부재 — *sample-level pooling이 적절한지* 미검증.

### 2.2 임상·기술적 제약

- **Tissue/sample 가용성**:
  - 발달 dataset: 모두 GEO 공개. 재현 가능성 양호.
  - PA: *EGAS00001003170 controlled access EGA* — *data access committee 승인 필요*. 산업에서 재현하려면 *EGA application + IRB / DTA* 절차 필요.
- **장비·시약 가용성**:
  - 10x Chromium V1 (구버전) + Smart-seq2 기반 dataset 혼재. *최신 platform (10x Chromium X, Singleron, BD Rhapsody)*에서 동일 동작 미검증.
  - CellRanger v7.0.1, Kallisto, Alevin-Fry v0.8.0 등 *복수 preprocessing pipeline* — *standardization 부족*.
- **계산 자원**:
  - GPU 없이도 동작 (CPU $4\times$ faster than scVelo dynamical). GPU 사용 시 $10$–$20\times$ — *small lab / clinical setting에서도 적용 가능* (Bo Wang 그룹의 강점).
  - Full-batch training (batch = $N$ cells) — *RAM 부담*. 100k cell 이상은 *GPU 메모리 한계 가능*. 본 paper benchmark 최대 30k.
- **Turnaround time**:
  - Hindbrain 13,501 cells 36초 (GPU). *임상 의사결정 turnaround*로는 *매우 빠름*. 단 *preprocessing 시간* (loom 생성, kallisto alignment)이 제외된 시간.

### 2.3 규제·QA·RA 관점

- **FDA/EMA pathway**:
  - 현재 형태로는 *research tool* — 직접적 IVD / LDT / SaMD pathway 해당 없음.
  - PA immunogenicity discovery가 *prognostic biomarker*로 발전하면 *SaMD (Software as Medical Device)* 또는 *companion diagnostic* pathway 가능. 그러나 *clinical validation 단계* 필요 — 본 paper는 *proof of concept*.
- **Analytical / Clinical validation**:
  - *Analytical validation*: hyperparameter robustness (Supp Note S1, $n=5000$ sweep)는 *technical reproducibility* evidence. 그러나 *precision / accuracy / LOD* 같은 IVD-grade metric 없음.
  - *Clinical validation*: 없음. PA discovery는 *prognosis 데이터 부재*.
- **GMP / GLP**:
  - 해당 없음 — *research tool*. 실험은 standard scRNA-seq protocol 사용.
- **IRB / consent**:
  - 발달 dataset: animal 또는 human sample 모두 *publicly available* — IRB 별도 불필요.
  - PA: EGA controlled access — *원 IRB는 Vladoiu 2019* (ref. 11)에서 처리. 본 paper는 secondary analysis.
- **Label·indication**:
  - 해당 없음 — *research tool*.
- **Reproducibility for audit**:
  - Code public (MIT license, GitHub, Zenodo DOI 10.5281/zenodo.10251639) — *FDA audit 가능 수준의 공개*.
  - Processed data Figshare (10.6084/m9.figshare.24716592.v1).
  - 단 *full pipeline (raw fastq → loom → DeepVelo output)*의 *end-to-end reproducibility script* 부재 가능 — `검토필요:`.

### 2.4 권위·신뢰 가중치

- **출처 1차**: 1차 출처 — peer-reviewed *Genome Biology* (IF 11.3 정도, 2023 기준). BMC Group / Springer.
- **Peer review 여부**: peer-reviewed. Review history *Additional file 11*로 공개. Editor: Veronique van den Berghe.
- **저자 COI**: Bo Wang serves on Strategic Advisory Board of Vevo Therapeutics Inc. (Vevo Therapeutics는 single-cell biology + AI 기반 startup) — *COI 명시*. 다른 저자 없음. `해석:` Vevo가 *DeepVelo를 상업화*했는지는 본문에 없음. `질문:` Vevo Therapeutics website 확인.
- **Funding source**: NSERC (Canadian public), CIFAR AI Chairs, Peter Munk Cardiac Centre AI Fund (UHN) — *primarily Canadian public funding*. *corporate sponsorship 없음* — funding-side COI 낮음.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)

- **저자/기관의 자산화 가능성**:
  - Bo Wang lab (Vector Institute / University Health Network / University of Toronto): *single-cell AI hub*. Vector Institute는 Geoffrey Hinton 설립의 *Canada AI 기관*. UHN은 *clinical multi-omic data 접근 가능*.
  - Bo Wang의 *Vevo Therapeutics SAB role*: Vevo는 *cell-based therapeutics + AI driven cell phenotyping*. DeepVelo가 Vevo의 *cell selection / characterization 파이프라인*에 차용될 가능성. `해석:` direct evidence 없음.
  - Patent 보유 여부: 본 paper 본문에는 patent 명시 없음. `질문:` Bo Wang lab 또는 UHN의 patent filing 확인.
- **공동연구 후보**:
  - Code MIT license — *open collaboration friendly*.
  - GitHub maintenance: bowang-lab/DeepVelo active. `검토필요:` 최근 commit 빈도, issue response time.
  - 저자 group이 *consortium 참여* (Vector Institute Health Initiative, UHN AI Hub) — *open scientific collaboration 가능*.
- **경쟁사 관찰**:
  - Single-cell genomics AI 시장의 *경쟁 method*: cellDancer (`@li2023celldancer`), VeloVI, PyroVelocity, UniTVelo, MultiVelo, MultiVeloVAE — *모두 academic open source*. 상업적 솔루션 (예: 10x Genomics Cellenics, Latch, Seqera Tower)이 DeepVelo를 직접 통합한 사례 *미확인*.
- **시장 영향**:
  - *Cell-specific kinetics*는 single-cell field의 *2024 시점 mainstream concept*. DeepVelo는 *foundational reference*로 인용되지만 *최신 method (MultiVeloVAE, MoFlow)*가 더 인용됨. *시장 영향력은 *foundation reference* 수준*.

### 3.2 Commercialization-candidate (자체 제품화)

- **제품 카테고리 후보**:
  - **Software (SW)**: *cell-specific RNA velocity 분석 cloud SaaS*. 그러나 DeepVelo *단독으로는 차별화 부족* — MultiVeloVAE / MoFlow가 더 최신. *우리 자체 제품화는 비추*.
  - **Diagnostic (Dx)**: PA immunogenicity stratification → *immunotherapy response prediction* 후보. 그러나 *임상 cohort + validation 필요* — *DeepVelo 단독으로 Dx 후보화는 시기상조*.
  - **Service**: 자체 multi-omic 데이터 분석 service의 *backend method 후보 1*. 단, 차별화 약함.
- **기술적 성숙도 (TRL)**:
  - DeepVelo 자체: *TRL 4–5* (lab validation, multiple datasets). production-grade는 아님 (full-batch training scalability 미검증).
  - PA discovery: *TRL 2–3* (proof of concept, $n=3$).
- **IP 자유도**:
  - Patent 명시 없음. MIT license → *open implementation 가능*. 단 *후속 patent 가능성* — `검토필요:` Bo Wang lab patent landscape.
- **MVP 시나리오**:
  - 해당 없음 — DeepVelo 자체로 우리 product의 *MVP 후보 아님*. *MultiVeloVAE / MoFlow / 자체 epigenomic-lag method*가 더 합리적 MVP.

### 3.3 우리 파이프라인과의 fit

- **Dataset 호환**:
  - 우리 HSPC 10x Multiome (GSE209878)과 *modality mismatch* (DeepVelo는 RNA-only, 우리는 multiome). 직접 적용 시 *chromatin information 활용 불가*.
  - RNA-only mode로는 *baseline benchmark*로 사용 가능 — MultiVeloVAE / MoFlow 평가 시 비교 baseline.
- **자원 가능성**:
  - GPU 있음 (CLAUDE.md 명시) — 학습 가능.
  - 데이터 규모 호환 — 우리 HSPC dataset이 30k cell 이하면 full-batch training 가능.
  - Code Python + DGL + PyTorch — 우리 환경 호환.
- **전략적 방향과의 align**:
  - 우리 전략 = *epigenetic therapy 기반 response time 예측 → chromatin-transcription lag 정량화*. DeepVelo는 *transcription 단독* — *lag 정량화에 부적합*.
  - **방향 mismatch**. citation / methodology insight 활용이 적절.
- **빠진 capability**:
  - chromatin modality 처리 — DeepVelo 직접 활용으로는 불가.
  - epigenomic-lag 정량화 — 별도 method 필요 (MoFlow, MultiVeloVAE, 또는 자체 개발).

### 3.4 후속 BD·제품 액션 후보

- **DeepVelo benchmark 통합**
  - 누가: 본인 (분석 담당)
  - 언제: Week2 evidence expansion 시점 (지금 진행 중)
  - 자원: 분석 시간 ~ 1일 (이미 완료 — 본 분석)
  - 성공 기준: MoFlow / MultiVeloVAE evidence bundle에 DeepVelo의 *cell-specific kinetics rationale* 인용 가능.
- **Bo Wang lab follow-up paper 탐지**
  - 누가: 본인
  - 언제: 다음 분기
  - 자원: 1시간 paper-scrapper run
  - 성공 기준: Bo Wang lab의 *2024-2026 multi-omic velocity paper* 발견 여부 → 발견 시 별도 분석 폴더 생성.
- **Vevo Therapeutics 동향 watch**
  - 누가: BD lead (해당 시), 본인 (technical)
  - 언제: 장기 백로그
  - 자원: 분기별 30분
  - 성공 기준: Vevo가 DeepVelo 기반 cell selection을 *상업화*했는지 확인. *single-cell 기반 cell therapy company의 AI 파이프라인 모범사례* watch.

## 4. 전문가 코멘트

### 4.1 종합 등급

- **Level**: 중
- **Perspective**: cell-specific kinetics와 multi-lineage velocity 한계를 설명하는 *RNA-only reference*로 MoFlow / MultiVeloVAE의 배경 강화에 유용. 우리 파이프라인 직접 적용은 unlikely.
- **등급 근거**:
  - DeepVelo는 *cell-specific kinetic rate concept을 정립한 foundational paper 중 하나* — *methodology-reference 가치는 분명*.
  - 그러나 *epigenome-related modality 없음* → 우리 epigenomic-lag direct method가 아님.
  - 후속 method (MultiVeloVAE, MoFlow)가 *DeepVelo의 한계를 보완*했기 때문에 *최신 method first, DeepVelo는 background*.
  - PA tumor discovery는 *biological interest*는 있으나 *$n=3$ proof-of-concept*. *임상 implication을 위해서는 larger cohort + outcome data 필요*.
  - Code open source (MIT) + active GitHub + Zenodo DOI = *technical reproducibility는 양호*.

### 4.2 활용 우선순위

- **지금 (이번 sprint)**: Week2 evidence bundle에 *cell-specific kinetics motivation*과 *6 dataset benchmark 수치* 포함 (본 분석 완료).
- **다음 분기**: Bo Wang lab의 2024–2026 후속 paper 탐색 (multi-omic DeepVelo 또는 transformer 변형).
- **장기**: Vevo Therapeutics 동향 / DeepVelo 기반 산업 application 추적.

### 4.3 발표·미팅에서 들이밀 시점

- **본인 학회 발표 / 논문 introduction**: *RNA velocity 한계 → multi-omic 필요*로 transition할 때 *cell-specific kinetics necessity statement* 인용 (Citation 후보 §"인용 가능 문장").
- **사내 R&D 리뷰**: epigenomic-lag method 선택 시 *왜 DeepVelo 단독은 부족하고 MoFlow / MultiVeloVAE가 필요한지* 설명할 때.
- **BD 미팅**: Bo Wang lab과의 *공동연구 후보* 또는 *Vevo Therapeutics watch list*로 언급. 즉시 BD action priority는 낮음.
- **외부 컨퍼런스**: deep learning RNA velocity의 *method genealogy*를 시각화할 때.

### 4.4 추가 탐색 필요 영역

- 질문: Bo Wang lab의 2024–2026 후속 paper 또는 preprint 추적 — *multi-omic DeepVelo*, *transformer-based velocity*, *probabilistic DeepVelo* 출시 여부.
- 질문: Vevo Therapeutics가 *DeepVelo를 상업화*했는지, 또는 *cell-based therapy의 cell selection pipeline*에 활용했는지 LinkedIn / Crunchbase / press release 확인.
- 질문: GitHub `bowang-lab/DeepVelo` repository의 *최근 commit + issue activity*로 *maintenance 상태* 확인 — *우리가 의존하기 위한 stable version* 결정.
- 질문: DeepVelo가 *공식 단독으로 인용된 후속 multi-omic paper*가 어느 정도 되는지 — *2024–2026 인용 통계*로 *foundational reference로서의 시장 영향력* 측정.
- 검토필요: Bo Wang lab 또는 UHN의 *velocity-related patent filing* (USPTO / WIPO) 검색 → *IP freedom-to-operate*가 향후 자체 method 개발 시 영향 줄지.
- 검토필요: PA immunogenicity finding에 대한 *follow-up paper* — Vladoiu lab 또는 다른 PA 연구진이 *larger cohort*에서 같은 패턴을 재현했는지.
