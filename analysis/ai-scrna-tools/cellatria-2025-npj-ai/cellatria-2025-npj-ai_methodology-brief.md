# CellAtria — Methodology Brief

Citation: `@nouri2026cellatria` — Nouri N, Artzi R, Savova V. *npj Artificial Intelligence* (2026) 2:8. DOI: 10.1038/s44387-025-00064-0.

> 본 분석은 원문 PDF (`sources/cellatria-2025-npj-ai.pdf`) 및 supplementary (`44387_2025_64_MOESM1_ESM.pdf`)를 근거로 한다.

---

## 한 줄 요약

**CellAtria**: LangGraph 기반 agentic AI 프레임워크로, 논문 PDF 한 장으로부터 scRNA-seq 데이터 취득·전처리·annotation까지 single prompt로 완전 자동화 (<10분). LLM은 코드를 생성하지 않고 pre-vetted 32개 도구를 orchestrate한다.

---

## 재현에 필요한 최소 구성 요소

| 구성 요소 | 버전/상세 | 출처 |
|----------|----------|------|
| CellAtria (agentic layer) | LangGraph v0.5.4 기반 | https://github.com/AstraZeneca/cellatria |
| CellExpress (processing pipeline) | Scanpy 기반, Docker image | 위 GitHub |
| LLM backend | gpt-4o (primary), gpt-4o-mini (경제형) | Azure OpenAI |
| SCimilarity | v1.1 (cell type annotation) | 별도 GitHub |
| CellTypist | v2.6.0 | pip 설치 |
| Python | ≥3.10 추정 | — |
| 최소 RAM | ~10 GB/dataset (평균); 최대 27.56 GB (GSE188711) | Supplementary Fig. S33 |
| 권장 환경 | Docker, AWS EC2 r6i.32xlarge 또는 동급 서버 | Methods §실행환경 |

---

## 핵심 방법 (재현 가능 수준으로 압축)

### 1. 전체 실행 흐름

```
[입력] 논문 PDF 또는 자연어 prompt
      ↓
[단계 1] Metadata extraction agent
  - PDF에서 tissue, species, disease context, GEO accession ID 추출
  - LLM이 논문 서술 parsing → structured JSON 출력
  - 추출 실패 시 "unavailable" 표시 (hallucination 방지)
      ↓
[단계 2] Dataset acquisition agent
  - GEO API (NCBI) 또는 CZ CELLxGENE에서 raw count matrix 자동 다운로드
  - GSE / GSM 레코드 처리; 다중 sample 자동 분기
  - Supported input: 10X matrix trio (barcodes/features/matrix), HDF5 (.h5)
      ↓
[단계 3] File organization agent
  - 다운로드 파일을 CellExpress가 기대하는 표준 디렉토리 구조로 정리
  - Configuration JSON 자동 생성 (dataset metadata, CellExpress parameter)
      ↓
[단계 4] CellExpress execution via Docker
  - QC → Normalization → Dimensionality reduction (PCA/UMAP/t-SNE)
  → Clustering (Leiden) → Cell type annotation (SCimilarity + CellTypist)
  - HTML report + AnnData (.h5ad) + 실행 log 생성
```

### 2. CellExpress pipeline 상세 (Supplementary Fig. S22–S28)

**QC 단계:**
- Gene 필터: 최소 3 cell에서 발현
- Cell 필터: nGenes > 500 (또는 dataset별 자동 조정), percent.mito < 20%
- Doublet detection: scrublet

**Normalization:**
- Library size normalization (10,000 counts/cell → log1p)
- Highly variable gene (HVG) selection: top 3,000 genes

**Dimensionality reduction:**
- PCA (50 components)
- UMAP + t-SNE (2D visualization)
- Leiden clustering (resolution 자동 또는 기본값)

**Cell type annotation:**
- SCimilarity v1.1: gene expression similarity 기반 (k-nearest neighbor, pan-tissue atlas)
- CellTypist v2.6.0: logistic regression 기반 (tissue-specific model 선택)
- 두 방법을 병렬 적용 → 각 cluster에 대해 두 label을 모두 출력, consensus 표시

**Output files:**
1. `output.h5ad` — 전처리 완료 AnnData (cell × gene matrix + metadata)
2. `summary.html` — QC metrics, UMAP, cell type composition, provenance
3. `cellexpress_config.json` — 모든 parameter 기록
4. execution log — package version, timestamp, resource usage

### 3. LangGraph agentic 실행 구조

- **Graph topology**: Directed acyclic graph (DAG) — 4개 stage node + conditional edge
- **State management**: 각 node가 shared state를 읽고 업데이트 → 다음 node로 전달
- **Tool invocation**: 각 agent node가 pre-vetted tool 중 해당 작업에 적합한 것을 선택
- **32개 tool 분류**:
  - Document analysis tools (5): PDF parser, DOI resolver, metadata extractor 등
  - Data retrieval tools (8): GEO downloader, SRA toolkit wrapper, CZ CELLxGENE client 등
  - File system tools (6): directory creator, file mover, format converter 등
  - CellExpress interface tools (7): config generator, Docker runner, log parser 등
  - Utility tools (6): format checker, error handler, report formatter 등
- **Hallucination safeguard 3층**:
  1. Tool-schema validation: LLM이 tool 호출 전 input schema 자동 검증
  2. Restricted invocation patterns: 특정 도구 조합만 허용
  3. Boundary-aware system prompts: scope 밖 요청 거부 (Supplementary Fig. S34)

### 4. LLM 설정

| 항목 | 값 |
|------|---|
| Primary model | gpt-4o (Azure OpenAI) |
| Economy model | gpt-4o-mini (Azure OpenAI) |
| Temperature | 0 (deterministic) — Methods 명시 |
| Context window | 128k tokens (gpt-4o 기준) |
| Tool use mode | function calling (parallel tool call 허용) |
| Output format | structured JSON (schema-validated) |

---

## 재현성 체크리스트

재현 시도 전 확인 사항:

- [ ] Azure OpenAI API key 또는 OpenAI API key 설정
- [ ] Docker 설치 및 CellExpress image pull (`docker pull ghcr.io/astrazeneca/cellexpress:latest`)
- [ ] CellAtria GitHub 설치 (`pip install cellatria` 또는 소스 설치)
- [ ] SCimilarity v1.1 모델 파일 다운로드 (GitHub에서 별도 제공 여부 확인)
- [ ] CellTypist v2.6.0 설치 및 tissue model 다운로드
- [ ] GEO 인터넷 접근 확인 (NCBI GEO API, FTP)
- [ ] RAM ≥ 32 GB 권장 (dataset 크기에 따라 최대 28 GB+ 소요)

**재현 가능성 평가**: 중-상. GitHub 공개 코드 + Docker image + AnnData 출력 → technical reproducibility 높음. 단, LLM API 버전 고정, SCimilarity 모델 파일 가용성, GEO dataset 안정성이 장기 재현성의 변수.

---

## 우리 파이프라인에서 쓸 수 있는 것

### 즉시 활용 가능 (High priority)

**CellExpress standalone 적용**:
- 우리 HSPC 10x Multiome RNA (GSE209878) 전처리에 CellExpress를 직접 적용
- Input: 10X matrix trio (우리가 이미 갖고 있음)
- Output: quality-controlled, normalized AnnData → MultiVelo/MoFlow 입력으로 연결
- 절차: CellExpress Docker image pull → config JSON 작성 (tissue: bone_marrow, species: human) → 실행 → output.h5ad 확인
- 예상 소요 시간: dataset 크기에 따라 3–11분 (Supplementary Fig. S33 기준)

**Configuration JSON 패턴 참조**:
- CellAtria가 자동 생성하는 config JSON 구조를 참조해 우리 pipeline parameter를 표준화
- 특히 QC thresholds (nGenes, mito%) 를 dataset별로 자동 선택하는 로직이 참고 가치 있음

### 중기 활용 (Medium priority)

**SCimilarity + CellTypist 병렬 annotation**:
- CellExpress가 쓰는 two-model annotation 전략(SCimilarity + CellTypist)을 우리 annotation 파이프라인에 도입
- 현재 우리가 annotation model을 하나만 쓴다면 두 model의 consensus를 cross-validation으로 사용 가능

**LangGraph agentic 패턴 참조**:
- 우리 자체 scRNA-seq 분석 자동화 도구를 개발할 때 LangGraph 기반 directed graph + shared state + schema-validated tool 호출 패턴을 architectural template으로 참조

### 현재 사용 불가 (Low priority / 외부 의존)

- CellAtria의 full agentic interface: Azure OpenAI API 필수, 비용 발생
- GEO automatic download: 우리가 이미 data를 갖고 있어 불필요
- SCimilarity pan-tissue atlas: pan-tissue 모델이 HSPC-specific annotation에 optimal인지 확인 필요

---

## 비교 참고 (field context)

| 도구 | 접근 방식 | LLM 역할 | 재현성 | 도메인 범위 |
|------|----------|---------|------|-----------|
| **CellAtria** | Tool orchestration (pre-vetted) | Orchestrator (no code gen) | 높음 | scRNA-seq ingestion |
| CellAgent | Code generation | Code writer | 낮음 (stochastic code) | 광범위 |
| BiomNI | NLP → bioinformatics query | Query translator | 중간 | DB query |
| scGPT | Foundation model | Feature encoder | 높음 | scRNA-seq representation |

---

## 인용 핵심 수치 요약

| 수치 | 출처 | 사용 시나리오 |
|------|------|------------|
| Pearson r ≈ 0.99 (cell type concordance, PBMC) | Supplementary Fig. S29 | annotation 정확도 citation |
| 25/25 datasets 100% completion | Fig. S33 | pipeline 안정성 citation |
| <10분 one-shot vs. ~15시간 수동 | Results §One-shot | efficiency 비교 (internal benchmark 한계 명시 권장) |
| 평균 1.45 ± 1.25분/task | Supplementary Fig. S33 | 실행 속도 citation |
| 평균 10.1 ± 9.8 GB RAM/dataset | Supplementary Fig. S33 | 자원 요구사항 citation |
| 32개 pre-vetted atomic tools | Methods, Supplementary Fig. S2 | 아키텍처 설명 citation |
