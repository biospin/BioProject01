# cellatria-2025-npj-ai — Core Analysis

## Executive Summary

- **무엇**: 공개 scRNA-seq 데이터의 수동 ingestion — 논문 파싱 → 메타데이터 추출 → 저장소 다운로드 → 파이프라인 실행 — 전 과정을 단일 chatbot 인터페이스로 자동화하는 agentic AI 프레임워크(CellAtria) 및 동반 분석 파이프라인(CellExpress)을 제시.
- **모델 / 방법**: LLM(gpt-4o / gpt-4o-mini) + LangGraph 기반 directed graph 실행 아키텍처. LLM은 자연어 intent 해석 + pre-vetted tool orchestration만 담당; 분석 결정은 schema-validated tool이 수행. CellExpress는 Scanpy 기반 QC → 정규화 → batch 보정 → UMAP/t-SNE → clustering → cell type annotation 순차 파이프라인.
- **핵심 결과**:
  - ① 유아 PBMC (GSE213996, 18 samples, ~71,000 post-QC cells): CellExpress 단일 실행 ~30분. 원저자 annotation 대비 cell type composition Pearson r ≈ 0.99, major immune lineage 98% 일치.
  - ② 25개 공개 human scRNA-seq dataset (6개 암종, 290 samples): gpt-4o/gpt-4o-mini 모두 수동 개입 없이 100% 완료. 평균 agentic task 1.45 ± 1.25분(gpt-4o). CellExpress 평균 3.16분/dataset, ~39,000 ± 32,000 post-QC cells/dataset.
  - ③ One-shot 실행: 기사 URL 1개 → CellExpress 완료까지 10분 미만 vs. 동등 수동 작업 ~15 cumulative hours(저자 내부 기준).
- **우리 적용**: `pipeline-applicable` — CellExpress의 Scanpy 기반 표준 scRNA-seq preprocessing 파이프라인이 우리 HSPC multiome RNA 분석 전처리 단계에 직접 참조 가능. `academic-citation` — agentic bioinformatics 프레임워크 설계 논거로 인용 가능.
- **심층**: 한계·재현 ROI는 `cellatria-2025-npj-ai_lens-academic.md` / `cellatria-2025-npj-ai_lens-industry.md` / `cellatria-2025-npj-ai_methodology-brief.md` 참고.

---

## Identity

- **Title**: An agentic AI framework for ingestion and standardization of single-cell RNA-seq data analysis
- **Authors**: Nima Nouri, Ronen Artzi, Virginia Savova
- **Affiliation**: Oncology Data Science and Artificial Intelligence, AstraZeneca, Waltham, MA, USA
- **Year**: 2026 (online 2026-01-16; received 2025-09-09; accepted 2025-12-22)
- **Venue**: npj Artificial Intelligence, (2026) 2:8
- **DOI**: 10.1038/s44387-025-00064-0
- **Citation key**: nouri2026cellatria
- **Code**: https://github.com/AstraZeneca/cellatria (public)

---

## Background

#### 배경 스토리

- **문제의 출발점**: scRNA-seq 데이터가 공공 저장소(GEO, CZ CELLxGENE 등)에 대량 축적됐지만, 새로 발표된 dataset을 내부 분석 워크플로우에 통합하는 과정은 여전히 수동이고 전문가 의존적이다. 저자 기준 동등 수동 작업에는 약 15 cumulative hours가 소요된다.

- **선행 접근 A (ad-hoc code generation 방식)**: 일부 연구는 LLM이 런타임에서 직접 분석 코드를 생성하는 방식을 제안한다(CellAgent, BIA, BiomNI, Zhou et al. 2024). LLM의 유연한 코드 생성 능력으로 single-cell 분석을 자동화하려는 시도.

- **A의 한계**: (1) 재현성 — LLM 출력이 모델 버전·prompt 뉘앙스에 따라 달라진다. (2) hallucination 위험 — 논리 오류, state-of-the-art 방법과의 비호환성(training data 시간적 cutoff), domain-specific parameter 오용. (3) 임상·규제 환경에서 protocol 표준화 위반 위험. 저자들은 "extensive human oversight and debugging" 없이 과학적으로 불건전한 분석을 산출할 수 있다고 명시.

- **선행 접근 B (LLM-assisted pipelines)**: scExtract(Wu & Tang 2025)와 SCassist(Nagarajan et al. 2025)는 LLM-assisted pipeline을 탐색했다. 그러나 두 도구 모두 scripted 또는 command-line 실행에 의존하며 agentic planner나 conversational interface가 없어 multi-turn orchestration이 불가능하다.

- **이 논문으로 이어지는 gap**: LLM의 자연어 해석 능력과 pipeline 모듈화의 장점을 유지하면서, 코드 생성의 불확실성은 제거하고, 비전문가도 chatbot 인터페이스로 접근 가능한 end-to-end 자동화가 필요하다.

#### 기본 개념

- **Agentic AI system**: LLM이 자연어 intent를 해석하고 사전 정의된 computational tool들을 동적으로 조합·실행하는 시스템. LLM 자체가 코드를 작성하지 않고 tool invocation을 orchestrate한다.
- **LangGraph**: LLM agent의 실행 흐름을 directed graph로 인코딩하는 Python 프레임워크. state-aware modular function들로 구성. CellAtria의 architectural backbone.
- **GEO**: NCBI 공개 functional genomics 저장소. GSE(study-level) / GSM(sample-level) accession 체계.
- **CZ CELLxGENE Discover**: Chan Zuckerberg Initiative single-cell data platform. H5AD format 통합 dataset 제공.
- **Scanpy**: Python 기반 large-scale single-cell gene expression 분석 라이브러리. CellExpress의 computational core.

#### 이 논문의 필요성

- **핵심 이유**: 공개 scRNA-seq 데이터 재사용의 병목은 data interpretation과 scripting 전문성 의존이다. 이를 "shifting left — from specialist bioinformaticians to bench scientists"로 해소하면 throughput 증가 + analyst-driven 오류 감소가 동시에 가능하다.
- **기존 방법으로 부족했던 지점**: ad-hoc code generation은 재현성·안전성 문제, 기존 LLM-assisted tools는 conversational/agentic 기능 부재.
- **이 논문이 해결하려는 방향**: pre-vetted tool library를 LLM이 orchestrate하는 "LLM-mediated tool-centric paradigm"으로 유연성과 엄격성을 병렬 확보.

---

## Methods

#### 이 method가 푸는 문제

- **Formal task**: 공개 scRNA-seq study의 article URL 또는 PDF → structured metadata 추출 → public repository 데이터 다운로드 → standardized scRNA-seq processing → analysis-ready output 생성까지 전 과정 자동화.
- **입력**: (1) Article URL 또는 local PDF, (2) 직접 dataset download URL, (3) 자연어 user prompt
- **출력**: (1) structured metadata (JSON/CSV), (2) 다운로드·정리된 scRNA-seq raw data, (3) CellExpress 분석 결과 패키지 — annotated AnnData H5AD, HTML report, configuration JSON, QC-filtered AnnData
- **추정 대상**: 없음 — 통계 추정 모델이 아니라 orchestration + deterministic pipeline
- **중요한 hidden assumption**: LLM이 structured narrative convention(표준 섹션 구조, 일관된 biomedical terminology)을 따르는 과학 논문에서 잘 작동한다는 가정. 비구조적 콘텐츠에서는 성능 저하를 저자가 명시.

#### 시스템 아키텍처

**CellAtria 인터페이스 7개 구성요소** (Supplementary Fig. S1):
1. Persistent Chatbot Window: 내부 hidden state로 multi-turn 대화 연속성 관리
2. User Input Panel: 텍스트 prompt + PDF 업로드, 통합 execution handler
3. Real-time Log Viewer: user-agent transaction 실시간 상태 표시
4. Agent Backend Panel: agent 내부 reasoning, tool invocation 순서, backend response 단계별 표시
5. Embedded Terminal Panel: agent 런타임 환경 내 직접 shell 명령 실행
6. Interactive File Browser: 작업 디렉토리 탐색 및 파일 내용 검사
7. Export Utility: 세션별 machine-readable transcript + LLM metadata JSON 생성

**LangGraph 기반 실행 그래프**: agent 실행 흐름을 directed graph of modular, state-aware functions로 인코딩. 각 tool은 rigorously defined I/O behavior를 갖는 atomic function으로 구현됨.

#### CellAtria Modular Toolchain (32개 도구, Supplementary Fig. S2)

4개 operational domain으로 분류:
1. **Metadata Parsing & Semantic Structuring** (7개): `fetch_article_metadata_url`, `fetch_article_metadata_pdf`, `store_article_metadata_file`, `refine_article_metadata`, `fetch_geo_metadata`, `store_geo_metadata_file`, `refine_geo_metadata`
2. **Programmatic Data Retrieval & Organization** (12개): `download_geo`, `download_gsm`, `download_file`, `make_directory`, `list_directory`, `inspect_file`, `get_file_size`, `move_file`, `rename_file`, `remove_file_or_dir`, `set_working_directory`, `get_working_directory`
3. **Standardized File Handling & Pre-processing** (4개): `fix_10x_file_format`, `create_custom_csv`, `create_custom_json`, `create_custom_txt`
4. **CellExpress Pipeline** (9개): `get_cellexpress_info`, `configure_cellexpress`, `preview_cellexpress_config`, `reset_cellexpress_config`, `validate_cellexpress_config`, `run_cellexpress`, `review_cellexpress_log`, `terminate_cellexpress_job`, `check_cellexpress_status`

**LLM의 역할 제한**: LLM은 unstructured content 해석과 structured metadata 추론, 도구 orchestration만 담당. 모든 analytical decision은 fixed logic 또는 schema-validated default로 처리. LLM에 parameter choice를 위임하지 않는다. CellAtria는 RAG나 MCP를 사용하지 않는다.

#### Web/PDF 메타데이터 추출

- Journal URL: `requests` (v2.32.5)로 HTML 취득, `BeautifulSoup` (v4.13.3)으로 DOM-level 텍스트 추출
- Local PDF: `PyMuPDF` (`fitz`, v1.26.5)로 page별 paragraph-level 텍스트 추출
- 추출된 구조화 텍스트를 LLM에 전달해 metadata field(tissue, species, disease, accession identifiers 등) 추출

#### CellExpress Pipeline 세부 구조 (Fig. 2b)

Scanpy 기반 5단계 순차 실행:
1. **Quality Control**: global 또는 sample별. defaults — min UMI 750, min genes 250, min cell 3, max mitochondrial % 15
2. **Data Transformation**: normalization (target sum $10^4$), highly variable gene selection (top 2,000), scaling (max value 10)
3. **Dimensionality Reduction**: PCA (30 components) + UMAP + optional t-SNE
4. **Clustering**: graph-based Leiden (k-NN default k=15, resolution 0.6)
5. **Cell Type Annotation**: tissue-agnostic (SCimilarity) + tissue-specific (CellTypist), 선택적 병행

추가 모듈: doublet detection (Scrublet, default cutoff 0.25), batch correction (Harmony 또는 scVI)

**입력 형식 지원**: 10X Genomics Cell Ranger 출력(matrix/barcodes/features), HDF5 (.h5), AnnData H5AD, Parse Biosciences format, plain text (txt.gz), CSV-style (csv.gz)

**출력 패키지 4종**:
1. Finalized annotated AnnData (H5AD)
2. Interactive HTML report (QC metrics, 차원 축소, clustering, cell type annotation)
3. Configuration JSON (full audit trail)
4. QC-filtered AnnData (alternative workflow용)

#### 4단계 agentic execution narrative

저자가 정의한 canonical workflow 순서:
1. Dynamic metadata extraction
2. Dataset acquisition
3. File organization
4. Downstream analysis execution

각 module은 독립 호출 가능 (non-linear entry point 지원).

#### 실행 환경 및 LLM 설정

- LLM backend: Azure OpenAI (gpt-4o v2024-11-20, gpt-4o-mini v2024-07-18). Fine-tuning 없음. temperature 1.0, top-p 1.0
- Framework: LangGraph v0.5.4
- 실행 환경: Docker container (Python 3.12.9), AWS EC2 r6i.32xlarge (128 vCPUs, 1,024 GiB RAM)
- CellExpress는 detached mode background subprocess로 실행 → 세션 응답성 유지. stdout/stderr는 persistent log file로 redirect.

#### Hallucination 방지 3-layer safeguard

1. Tool-schema validation: ill-formed 또는 존재하지 않는 action 거부
2. Restricted invocation patterns: vetted tool sequence와 parameter만 허용
3. Boundary-aware system prompts: 능력 초과 시 decline 또는 defer 유도 (Supplementary Fig. S34)

#### 이전 방법과의 차이

| 항목 | Ad-hoc code generation | CellAtria |
|---|---|---|
| LLM 역할 | 분석 코드 직접 작성 | Tool orchestration만 |
| 재현성 | 모델 버전·prompt에 따라 가변 | Pre-vetted tool + schema-validated 고정 |
| 규제 적합성 | Protocol 표준화 어려움 | Docker 기반 GxP-compliant 환경 지원 |
| 인터페이스 | CLI/scripted | Conversational multi-turn chatbot |
| Hallucination 위험 | 코드 레벨까지 전파 가능 | Tool layer에서 차단 |

#### Method 관점의 한계

- LLM이 non-standard formatting(비정형 section header, 비표준 약어)을 가진 논문에서 metadata 추출 정확도 저하. 이 경우 해당 field를 "unavailable"로 표시(speculative inference 방지)
- LLM의 direct internet access 부재 → deterministic tool-mediated retrieval에만 의존. manuscript-reported metadata와 repository-level annotation 불일치가 agentic 실행 신뢰성에 영향
- downstream 특화 분석(pseudotime, trajectory, RNA velocity, splicing dynamics)은 CellExpress 범위 밖 — post-pipeline 단계로 위임
- 생성이 probabilistic하여 LLM별로 edge case 해석, 모호 instruction 처리에서 차이 발생. system designers가 tool layer를 지속적으로 강화해야 함

---

## Results

#### Dataset별 결과

##### Dataset 1 — Use case 1: URL 기반 메타데이터 추출 + GSE-level dataset 검색

- **Dataset**: 유아 2개월 PBMC 종단 전사체 연구 (Nouri et al. 2023, Nat. Commun. 14:7976; GEO: GSE204716)
- **목적**: CellAtria의 URL-driven 메타데이터 추출 + GEO study-wide dataset 다운로드 능력 검증
- **데이터 규모**: multi-turn dialogue로 GSM별 sample 정보 구조화. GSM6189249~GSM6189266 등 18 samples 확인 (Supplementary Figs. S3–S11)
- **정성 결과**: Article URL 수신 → multi-turn dialogue로 논문 파싱 → structured metadata(tissue: blood, species: Human, disease: Not disease-specific, data modality: scRNA-seq, data availability: GEO:GSE204716 and dbGAP:phs002926.v1.p1, publication date: 02 December 2023, publisher: Nature Communications) 추출 → JSON/CSV 저장 → 10X Genomics file naming 표준화. 실시간 log viewer가 각 tool invocation 성공 여부 표시.
- **논문 주장 연결**: "CellAtria effectively bridges literature discovery and structured dataset acquisition."

##### Dataset 2 — Use case 2: PDF 기반 메타데이터 추출 + GSM-level dataset 검색

- **Dataset**: NSCLC 환자 T cell 분석 (Pai et al. 2023, Cancer Cell 41:776; GEO: GSE185206, 총 199 samples)
- **목적**: publisher website scraping이 불가능한 상황에서 local PDF를 통한 메타데이터 추출 시연
- **데이터 규모**: GSM5608032, GSM5608033, GSM5608034 3개 sample 선택 다운로드
- **정성 결과**: PDF upload → structured metadata 추출(Project: Human NSCLC Tumor-specific T cells, publication date: April 10 2023, publisher: Elsevier Cancer Cell, authors 등) → GSM-level 개별 다운로드. Use case 1과 달리 fine-grained sample-level 검색.
- **논문 주장 연결**: "CellAtria enables flexible, fine-grained data acquisition even under restricted access conditions."

##### Dataset 3 — Use case 3: H5AD dataset 직접 URL 다운로드 + 파일 통합

- **Dataset**: CZ CELLxGENE Discover 두 curated collection (H5AD format)
  - 13개 연구, 8개 종양 유형 myeloid cell states (Guimarães et al. 2024, Nat. Commun. 15:5694)
  - 223명 환자, 9개 암종 immune checkpoint blockade 반응 (Gondal et al. 2025, Sci. Data 12:139)
- **정성 결과**: 사용자 제공 download URL → 파일 다운로드 → working directory 통합 → 메타데이터 파일 생성. Non-linear entry point에서의 tool 직접 호출 시연.

##### Dataset 4 — CellExpress Full Pipeline 검증 (GSE213996)

- **Dataset**: 유아 2개월 PBMC scRNA-seq (GSE213996), 인체 혈액
- **데이터 규모**: 18 samples, ~71,000 post-QC cells (Fig. S30 기준 AnnData dimension: 71,101 × 20,630)
- **QC thresholds**: min UMI 750, min genes 250, max mitochondrial 15%, Scrublet cutoff 0.25
- **Baseline**: 원저자 expert annotation
- **Metric**: Pearson correlation of cell type composition frequencies (label-harmonized compartments 기준)
- **주요 수치**:
  - Cell type concordance (SCimilarity vs. original): Pearson r ≈ 0.99
  - Major immune lineage frequency agreement: 98%
  - T CELL: original 79.1% vs. SCimilarity 72.9% vs. CellTypist 72.6%
  - B CELL: 9.8% vs. 11.1% vs. 11.2%
  - MYELOIDS: 5.5% vs. 6.8% vs. 6.7%
  - NK CELL: 5.1% vs. 5.9% vs. 8.4%
  - Full pipeline runtime: ~30분
- **통계적 유의성**: p-value 미제공 (Pearson r 수치만 제시)
- 해석: Pearson r ≈ 0.99는 major compartment 비율 비교 기반. subtype 수준 concordance는 미제공.

##### Dataset 5 — 25개 암 연구 다중 dataset 벤치마크

- **Dataset**: 25개 공개 human scRNA-seq (6개 암종 — breast n=5, lung n=3, prostate n=3, colorectal n=5, ovary n=5, pancreas n=4), 290 samples (Figure S33 전체 결과표)
- **목적**: CellAtria agentic automation 확장성·일관성 정량 평가
- **gpt-4o agentic controller 결과**:
  - 평균 agentic task 시간: 1.45 ± 1.25분/dataset
  - 평균 token count: 6,589 ± 1,317 tokens/run
  - 평균 output size: 20.5 ± 4.0 KB
  - Gini coefficient: ≈ 0.10 (low dispersion — 일관된 verbosity)
  - 완료율: 25/25 = 100%, 수동 개입 없음
- **gpt-4o-mini agentic controller 결과**:
  - 평균 agentic task 시간: 1.70 ± 1.70분/dataset
  - 평균 token count: 5,439 ± 1,369 tokens/run
  - 평균 output size: 16.9 ± 4.1 KB
  - Gini coefficient: 0.14
  - 완료율: 25/25 = 100%
- **CellExpress pipeline 결과 (25 datasets)**:
  - 총 처리 cells: ~1,000,000 post-QC cells
  - 평균 CellExpress runtime: 3.16분/dataset
  - 평균 post-QC cells: ~39,000 ± 32,000
  - 평균 memory usage: 10.1 ± 9.8 GB/run
  - Post-QC cell count vs. memory: Pearson r = 0.45, p < 0.05 (moderately positive, non-strictly linear)
- **관찰된 lexical variation**: PBMC를 "peripheral blood mononuclear cells"로 expanded form으로 렌더링하는 등 surface-level 용어 차이 발생. 그러나 CellExpress는 schema-validated arguments를 소비하므로 분석에 영향 없음.

##### Dataset 6 — One-shot 자율 실행 시나리오

- **Dataset**: 유아 PBMC 연구 (Use case 1과 동일 URL; GEO: GSE213996)
- **목적**: 단일 고수준 명령으로 document-to-analysis 전 과정 자율 실행 평가
- **주요 수치**:
  - 전체 실행 (CellExpress runtime 포함): 10분 미만
  - 동등 수동 작업 (저자 내부 기준): ~15 cumulative hours
  - One-shot processed cells × genes: 86,784 × 20,630 (Figure S31)
- **수행된 agentic 단계** (수동 개입 없음): article parsing → structured metadata extraction → dataset retrieval → CellExpress pipeline configuration (context-aware parameters) → execution dispatch (Figure S32 backend trace)

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 모든 use case(URL/PDF/H5AD)와 두 LLM backend(gpt-4o/gpt-4o-mini)에서 수동 개입 없이 완료.
- **가장 중요한 수치**: Pearson r ≈ 0.99 (annotation concordance), 25/25 datasets 100% 성공, one-shot 10분 vs. 수동 ~15시간.
- **baseline 대비 차이**: ad-hoc code generation baseline에 대한 정량적 비교는 미제공. 주요 baseline은 "수동 분석가 작업시간"(~15시간)이며, 이는 저자 내부 추정치다.
- **결과 해석 시 주의점**: annotation concordance(Pearson r ≈ 0.99)는 GSE213996 한 dataset에서만 보고됨. 25개 cancer dataset에서의 생물학적 정확성은 별도 정량화되지 않았다. "성공"의 정의가 pipeline completion 여부로 제한됨.

---

## Figures

#### Figure 1

- **이 Figure가 필요한 이유**: 기존 수동 workflow의 다단계 병목과 CellAtria 자동화 접근의 차이를 대비 시각화. 시스템이 왜 필요한지 직관적으로 설득.
- **이 Figure가 뒷받침하는 주장**: 수동 data onboarding의 8단계 순환이 CellAtria의 LLM-mediated toolchain orchestration으로 단순화된다.

##### 패널별 설명
- **a**: 기존 수동 data onboarding cycle — Announcement → Assignment → Identification → Review → Metadata → Data → Analysis → Results. 각 단계에 인력 의존 표시.
- **b**: CellAtria agentic triage 및 실행 아키텍처 — Narrative-formatted scientific documents → Parse → LLM → Retrieve → (trigger) → Graph-based multi-actor execution framework + CellExpress pipeline → Processed data. Toolchain dispatch 단계: Document Parsing, Accession Resolution, Dataset Retrieval, File & Data Organization, Pipeline Configuration, CellExpress Execution, Standardized dataset.

##### 본문에서 강조한 비교
- 수동 workflow(panel a)는 domain knowledge + computational proficiency를 가진 전문가가 각 단계에 필요. CellAtria(panel b)는 LLM semantic layer가 이를 대체해 비전문가도 chatbot으로 접근 가능.

##### 해석 시 주의점
- Panel b는 "optimized execution path(canonical workflow)"를 표현. 저자 명시: 각 module은 독립 호출 가능, non-linear entry point 지원.

---

#### Figure 2

- **이 Figure가 필요한 이유**: CellAtria의 LLM-tool interaction 사이클과 CellExpress의 단계별 구조를 구체화. 시스템 내부 작동 방식의 투명성 확보.
- **이 Figure가 뒷받침하는 주장**: LLM이 tool을 orchestrate하는 방식의 투명성, CellExpress가 raw counts → interpretable output으로 가는 완결된 파이프라인임을 시각화.

##### 패널별 설명
- **a**: LLM-mediated orchestration — Human → Interface → LLM → Toolset → CellExpress 5개 layer. 사용자 prompt 제출 → Interface가 LLM에 전달 → LLM이 intent 해석 후 tool 자율 호출 → 실행 결과 반환. "context-aware execution" cycle.
- **b**: CellExpress pipeline 구조 — Project Setup & Settings → Quality Control & Filtering → Normalization & Transformation → Reduction & Batch Correction → Clustering & Embeddings → Cell Type Annotation. 우측에 4개 출력: HTML Report, Processed Data, Configs, Post-QC Counts.

##### 본문에서 강조한 비교
- CellExpress 출력이 4종으로 구조화됨 — annotated AnnData(downstream 분석용), HTML report, configuration JSON(reproducibility), QC-filtered AnnData(alternative workflow용).

##### 해석 시 주의점
- Panel b의 "Hardware/Computing Infrastructure Environment" 하위 레이어는 Docker containerization을 나타내는 것으로 해석됨. 추론: Methods에서 Docker-based 실행 환경 명시.

---

#### Supplementary Figures S1–S35 (주요 내용 요약)

- **S1**: CellAtria UI 7개 구성요소 (a: chatbot, b: prompt input, c: PDF upload, d: live log viewer, e: agent backend, f: terminal, g: file browser, h: export utility).
- **S2**: CellAtria toolchain 32개 도구 전체 목록 (4개 domain).
- **S3–S11**: Use case 1 전체 interaction trace — working directory 설정 → URL metadata 추출 → JSON 저장 → GEO metadata 추출 → CSV 저장 → dataset 다운로드 → 10X file naming 표준화. 실제 추출된 metadata 필드(tissue, species, disease, data availability, publication date, publisher, conflicts of interest) 확인 가능.
- **S12–S15**: Use case 2 — PDF upload → NSCLC metadata 추출 → GSE185206 연동 → GSM-level 다운로드.
- **S16–S18**: Use case 3 — H5AD dataset direct URL 다운로드 + 파일 통합 + metadata.csv 생성.
- **S19**: System-level panels — a: agent backend 내부 reasoning trace(gpt-4o-2024-11-20, token usage 표시), b: terminal panel(tree 명령 결과), c: file browser, d: export utility(chat_json 1.3 KB, llm_json 206.0 B).
- **S20**: machine-readable JSON transcript 예시 (agent-user 대화 구조).
- **S21**: LLM metadata export JSON (provider: azure-openai, model: gpt-4o, version: 2024-11-20, temperature: 1.0, top_p: 1.0).
- **S22–S28**: CellExpress orchestration — pipeline 초기화(required parameters: --input, --project, --species, --tissue, --disease) → parameter 구성 → YAML-format validation preview → launch(PID 제공) → real-time monitoring → log summary → completion(outputs: HTML report, QC-controlled H5AD, annotated H5AD, config JSON, AnnData 71,101 × 20,630).
- **S29**: Cell type composition comparison table (7개 cell type, original vs. SCimilarity vs. CellTypist count + frequency).
- **S30**: CellExpress full execution record JSON (18 samples, GSM6189249–GSM6189266, runtime 31.55분, post-QC 71,101 cells, n_vars 20,630, QC settings 상세 포함).
- **S31**: One-shot autonomous execution — 단일 prompt로 complete pipeline 완료 (86,784 × 20,630).
- **S32**: One-shot agentic backend reasoning trace — chatbot과 tools 단계가 교번하며 tool invocation(set_working_directory, fetch_article_metadata_url, refine_article_metadata, make_directory, fetch_geo_metadata, download_geo, store_geo_metadata_file 등) 순서 확인 가능.
- **S33**: 25개 dataset benchmark 상세 table (각 GSE별 gpt-4o/gpt-4o-mini agentic performance + CellExpress performance).
- **S34**: Out-of-scope tool request("magicharm") → CellAtria 거절 + Harmony/scVI redirect.
- **S35**: CellExpress 전체 CLI argument 목록 (35개 인수, default 포함).

---

## Tables

#### Supplementary Figure S29 (Cell type composition comparison table)

- **이 Table이 필요한 이유**: CellExpress annotation과 원저자 annotation의 일치도를 세포 유형별로 정량화하여 Pearson r ≈ 0.99 주장을 지지.
- **이 Table이 뒷받침하는 주장**: CellExpress의 automated cell type annotation이 expert annotation과 높은 compartment-level 일치도를 달성.

##### 표 구조
- Row: 7개 canonical cell type (T CELL, B CELL, MYELOIDS, NK CELL, DENDRITIC CELL, ERYTHROID, PLATELET)
- Column: Count + Frequency (original_paper, cellexpress_scimilarity, cellexpress_celltypist) × 2 = 6개 값 열

##### 핵심 수치

| Cell Type | Original (n, %) | SCimilarity (n, %) | CellTypist (n, %) |
|---|---|---|---|
| T CELL | 55,210 (79.1%) | 51,835 (72.9%) | 51,601 (72.6%) |
| B CELL | 6,835 (9.8%) | 7,916 (11.1%) | 7,984 (11.2%) |
| MYELOIDS | 3,811 (5.5%) | 4,804 (6.8%) | 4,775 (6.7%) |
| NK CELL | 3,526 (5.1%) | 4,192 (5.9%) | 5,952 (8.4%) |
| DENDRITIC CELL | 209 (0.3%) | 237 (0.3%) | 344 (0.5%) |
| ERYTHROID | 157 (0.2%) | 200 (0.3%) | 169 (0.2%) |
| PLATELET | 54 (0.1%) | 188 (0.3%) | 175 (0.2%) |

- 통계적 유의성: p-value 미제공 (이 표에 대한 별도 검정 없음, Pearson r ≈ 0.99는 본문에만 기술)

##### 본문에서 강조한 비교
- T CELL: original 79.1% vs. CellExpress ~72.9% — 6.2%p 차이가 가장 크다.
- NK CELL: SCimilarity 5.9% vs. CellTypist 8.4% — 두 automated method 간 2.5%p 불일치.
- PLATELET: original 54 (0.1%) vs. SCimilarity 188 (0.3%) — proportional 3배 차이.

##### 해석 시 주의점
- 이 concordance는 major lineage "compartment" 수준 비교다. CD4/CD8 T cell, Treg, cytotoxic subtypes 등 세부 subtype 수준 일치도는 미제공.
- NK CELL의 SCimilarity/CellTypist 간 2.5%p 차이는 tissue-agnostic vs. tissue-specific model 간 annotation 불일치를 반영한다.
- 해석: 이 표의 수치는 major compartment에서 세 annotation이 대체로 일치하나, T CELL 과소추정 패턴이 두 automated model에서 공통으로 나타난다. 원인(예: subtype 분류 경계 차이)은 미설명.

---

#### Supplementary Figure S33 (25 dataset benchmark 상세 table)

- **이 Table이 필요한 이유**: 대규모 벤치마크에서 CellAtria의 일관성·확장성을 GSE 단위로 정량화.
- **표 구조**: Row = 25개 GSE dataset, Column = samples / gpt-4o 성능(output_size_bytes, output_token_count, runtime_sec, status) / gpt-4o-mini 성능(동일) / CellExpress 성능(runtime_min, post_qc_cells, memory_GB)
- **핵심 수치 선별 (Figure S33 기준)**:
  - GSE188711 (39 samples): gpt-4o runtime 286.26초 (최장); CellExpress 11.01분, 162,520 post-QC cells, 27.56 GB — 대용량 dataset에서의 scaling 확인 케이스.
  - GSE228499 (9 samples): CellExpress 1.41분, 23,980 cells, 5.13 GB — 소규모 최솟값.
  - 모든 25개 row의 status: "success" — 100% 완료율.
- 해석: Runtime과 memory는 dataset 크기에 비례하지만 strictly linear하지 않음 (Pearson r = 0.45). 일부 dataset은 sample 수 대비 cell 수가 적거나 많아 분산이 크다.

---

## Supplementary Information

- **Supplementary Figures S1–S35**: 모든 use case의 실제 chatbot interaction 스크린샷, system-level panels, LLM configuration export, CellExpress pipeline 모니터링 trace, benchmark 전체 결과표, out-of-scope 처리 예시, CellExpress argument 전체 목록.
- **HTML summary report**: CellExpress 결과 예시 HTML이 CellAtria GitHub repository에 공개 (https://github.com/AstraZeneca/cellatria/tree/main/docs).
- **Processed objects (Use case 3)**: CZ CELLxGENE Discover platform 직접 접근 가능 (myeloid states: collections/3f7c572c-cd73-4b51-a313-207c7f20f188; ICB response: collections/61e422dd-c9cd-460e-9b91-72d9517348ef).

---

## 분석 자체에 대한 메모

- **저자 이해상충**: 저자 3인 모두 AstraZeneca 직원. 자체 개발 시스템에 대한 benchmark가 내부 기준으로 설계됨. Competing interests 명시: "The authors are employees of AstraZeneca US."
- **"수동 ~15시간" 기준 검토 필요**: "as per our internal benchmarks"로만 명시. 외부 검증 없는 내부 추정치. 인용 시 한계 표시 권장.
- **생물학적 정확성 검증 범위**: Pearson r ≈ 0.99는 GSE213996(PBMC) 한 dataset에서만 보고됨. 25개 cancer dataset에서는 annotation 정확도 별도 정량화 없음.
- **One-shot 시나리오 cell count 불일치**: Fig. S28/S30의 71,101 cells(multi-turn, GSE213996)과 Fig. S31의 86,784 cells(one-shot, 동일 URL?) 사이에 차이가 있다. 실행 조건 또는 QC parameter 차이 가능성 — 검토필요.
- **Scanpy 버전 명시 없음**: CellExpress의 핵심 dependency인 Scanpy의 정확한 버전이 Methods에 명시되지 않았다. 재현 시 버전 고정이 필요할 수 있다 — 검토필요.
