# scBench: Evaluating AI Agents on Single-Cell RNA-seq Analysis

**paper-id**: workman-2026-scbench  
**arXiv**: 2602.09063v1 (2026-02-09, preprint under review)  
**저자**: Kenny Workman, Zhen Yang, Harihara Muralidharan, Aidan Abdulali, Hannah Le (LatchBio)  
**소스**: `sources/workman-2026-scbench.pdf`

---

## 문제 정의 및 연구 목적

### Background

#### 배경 스토리

- **문제의 출발점**: scRNA-seq 분석은 통계, 고차원 데이터, 프로그래밍을 잇는 다단계 계산 파이프라인에 의존한다. 대부분의 연구 그룹에서 시퀀싱 자체보다 *분석*이 병목(rate-limiting step)이 됐다 (Introduction — Lähnemann et al., 2020 인용).

- **선행 접근 A — 기존 biology benchmark**: PubMedQA (Jin et al., 2019), BioLLM (Tinn et al., 2023) 등은 recall·interpretation·literature-style reasoning을 평가한다. 이들은 문헌 이해력을 측정하는 데 유효했다.

- **A의 한계**: 실제 데이터와의 경험적 상호작용(empirical interaction)이 없다. 실제 scRNA-seq 워크플로우에서 발생하는 데이터 기반 판단(QC threshold 선택, marker gene 발굴, cluster annotation 등)을 테스트하지 못한다 (Introduction §1).

- **선행 접근 B — LLM coding agents (mini-SWE-agent 계열)**: Yang et al., 2024의 SWE-agent처럼 코드를 쓰고, 도구를 호출하고, 반복적으로 목표를 향해 나아가는 agent가 등장했다.

- **B의 한계**: scRNA-seq에 적용할 경우 과학적 부정확성·hallucination 빈발, domain-specific 분석 단계에서 잦은 실패. 기존 benchmark로는 이 능력을 정량적으로 측정할 방법이 없었다 (Introduction §1).

- **이 논문으로 이어지는 gap**: 실제 scRNA-seq 데이터와 상호작용해야 답할 수 있는, deterministic하게 채점 가능한 표준 yardstick이 없었다. scBench는 이 gap을 채우기 위해 도입됐다.

#### 기본 개념

- **scRNA-seq 분석 파이프라인**: 원시 count matrix → QC (저품질 세포 제거) → Normalization → Dimensionality Reduction (PCA, UMAP) → Clustering → Cell Typing → Differential Expression → (선택적) Trajectory Analysis. 각 단계가 순차 의존하므로 초기 오류가 하류 분석 전체에 전파된다.

- **Deterministic grader**: agent의 JSON 출력을 ground truth와 자동 비교해 pass/fail을 산출하는 채점기. 주관적 언어("흥미롭다", "유의미하다") 없이 수치 허용 범위(tolerance) 또는 집합 유사도(Jaccard) 기준으로 판정한다.

- **mini-SWE-agent harness**: LLM이 free-form 응답을 생성하면 harness가 첫 번째 fenced code block을 추출해 bash shell에서 실행하고, stdout/stderr를 다음 관찰(observation)로 모델에 돌려준다. 1 evaluation 당 최대 100 action step, 300초 timeout (명령당), 600초 총 timeout.

- **AnnData (.h5ad)**: scRNA-seq 데이터의 표준 컨테이너. 발현 행렬 `.X`, 세포 메타데이터 `.obs`, 유전자 주석 `.var`, 전처리 결과 `.obsm` 등을 담는다. 이 논문은 data snapshot을 .h5ad로 제공한다 (Methods §4.2).

- **SpatialBench**: 같은 그룹이 만든 spatial transcriptomics용 benchmark (Workman et al., 2025). scBench는 scRNA-seq용으로, 두 benchmark를 합치면 두 가지 주요 전사체 분석 modality가 커버된다 (Results §2.5).

#### 이 논문의 필요성

- **핵심 이유**: frontier LLM agent가 scRNA-seq 분석에 실제로 얼마나 유능한지 측정하는 표준 benchmark가 없었다.
- **기존 방법으로 부족했던 지점**: 데이터 상호작용이 없는 문헌 기반 benchmark는 "텍스트를 이해하는 능력"만 평가하며, 분석 오류나 platform-specific 실패를 감지하지 못한다.
- **이 논문이 해결하려는 방향**: 실제 워크플로우에서 추출한 394개의 검증 가능 문제(verifiable problem)를 deterministic grader로 채점해 모델·task·platform별 능력을 정량화한다.

---

## 방법론

### 4.1 문제 구성 (Problem Construction)

5단계 파이프라인으로 각 evaluation을 만든다 (Methods §4.1):

1. **타겟 분석 단계 재현**: 발표된 workflow로 제공된 데이터에서 분석 결과를 재현.
2. **출력 artifact 정의**: JSON schema 형태로 답변 형식(field 이름·값 유형)을 명세.
3. **Grader family 선택**: 출력 형태에 맞는 채점기 지정 (§4.5 참조).
4. **허용 범위 캘리브레이션**: 여러 유효한 방법·파라미터로 분석을 반복해 tolerance 범위 결정.
5. **Anti-shortcut hardening**: 사전 계산된 embedding·캐시 label 제거, 답변을 직접 읽을 수 있는 field 삭제.

**Ground truth 검증**: 가능하면 published pipeline을 raw count에서 재실행. 파라미터가 명시되지 않은 경우(QC threshold 등) 표준 default 사용 + tolerance 확대. 각 문제를 (a) `.obs`·`.uns` 직접 읽기, (b) 사전 biological 지식, (c) 대안 유효 방법으로 풀어 anti-shortcut 검증 (§4.1).

### 4.2 Evaluation 해부 (Anatomy of a Problem)

각 evaluation은 JSON specification으로 4개의 agent-visible 구성요소 + 1개 internal 구성요소:

| 구성요소 | 내용 |
|---|---|
| **data node** | AnnData `.h5ad` 파일 (1개 이상) — 발현 행렬, 세포 메타데이터, 유전자 주석 포함 |
| **task prompt** | 자연어 분석 목표 + 정확한 JSON 출력 형식 명세 |
| **deterministic grader** | grader family, ground truth, tolerance, pass threshold |
| **metadata** | task category, evaluation type, sequencing platform, computational complexity |
| **notes** (internal) | 해법 접근법, tolerance 근거, known edge case — agent context에서 숨김 |

Linter가 정적 schema 검증 → manual review가 각 기준 확인 (§4.2).

### 4.3 Evaluation 유형과 내구성

**Scientific**: 생물학적 목표만 명세, 방법·파라미터는 agent 선택. 다양한 합리적 선택을 모두 수용하도록 tolerance 넓음.  
**Procedural**: 특정 방법 지정, 파라미터만 agent가 선택. tolerance를 더 좁게 설정 가능.  
**Observational**: 데이터 속성 보고·해석. 검증 가능성·anti-shortcut 구조에 초점 (§4.3).

### 4.4 설계 원칙

- **Specify what, not how**: task는 목표와 출력 형식만 지정 (procedural 제외).
- **Verifiability**: 주관적 언어 없이 deterministic 채점 가능한 JSON 출력 요구.
- **Scientific durability**: 합리적 방법론 변동에도 안정적인 답변이어야 함. random seed 민감성(Leiden clustering), library version artifact(UMAP 좌표) 회피.
- **Anti-shortcut**: precomputed embedding 제거, cached label 제거, multiple-choice 함정(biologically plausible distractors) 포함 (§4.4).

### 4.5 채점기 (Graders)

5개 grader family (§4.5, Appendix C):

| Grader | 용도 | Pass 기준 |
|---|---|---|
| **NumericTolerance** | cell count, QC metric, fold change 등 수치 | absolute / relative / min / max / asymmetric tolerance 모드 |
| **MultipleChoice** | 생물학적 해석, 패턴 식별 | `correct_answers` 목록 멤버십 (대소문자 무관) |
| **MarkerGenePrecisionRecall** | marker gene list, DE gene list | recall@K ≥ τ_r (default 0.50) **and** precision@K ≥ τ_p (default 0.60) |
| **LabelSetJaccard** | cell type label 집합 예측 | Jaccard J(A,B) = \|A∩B\|/\|A∪B\| ≥ 0.90 (default) |
| **DistributionComparison** | cell type 비율 등 다범주 분포 | 각 카테고리 독립적으로 ±ε pp 이내 (default ε=3), 전체 통과 필요 |

### 4.6 Agent Harness

**mini-SWE-agent** (Yang et al., 2024): LLM → fenced code block 추출 → bash 실행 → stdout/stderr를 다음 observation으로 반환. 반복 (§4.6).

- 실행 환경: scanpy, anndata, numpy, pandas, scipy, matplotlib (모든 모델 동일 버전). 네트워크 접근 허용 (추가 패키지 설치 가능). GUI 불가 (Jupyter, plot display 없음).
- 격리 workspace: 데이터 파일은 local cache에서 symlink. read/write access는 workspace 내부만.
- Step 제한: 100 action steps / evaluation; 300초 timeout/bash command; 600초 총 wall-clock.
- Timeout·crash 시: 그 시점의 `eval_answer.json`으로 채점. 파일 없으면 0점.
- Retry 없음: 각 replicate는 single attempt.

### 4.7 통계 설계

K=3 replicates, two-stage aggregation (SpatialBench 동일 방식):

- Stage 1: per-evaluation mean $\bar{s}_i = \frac{1}{K}\sum_r s_{i,r} \in \{0, \frac{1}{3}, \frac{2}{3}, 1\}$
- Stage 2: aggregate accuracy $\hat{\mu} = \frac{1}{n}\sum_i \bar{s}_i$, 95% CI via t-distribution (n-1 df)
- 모든 394 evaluation 등가중치. 평가 분기(task/platform별)도 동일 절차 재적용 (§4.7).

---

## 결과

### 2.1 Benchmark 구성

394 evaluations, 6 sequencing platforms, 7 task categories (Table 1):

**플랫폼별 분포**:

| Platform | QC | Norm. | Dim.Red. | Clust. | Cell Typ. | Diff.Exp. | Traj. | Total |
|---|---|---|---|---|---|---|---|---|
| BD Rhapsody | 6 | 11 | 14 | 7 | 13 | 10 | — | 61 |
| Chromium | 10 | 11 | 15 | 8 | 5 | 11 | — | 60 |
| CSGenetics | 4 | 5 | 7 | 5 | 20 | 1 | — | 42 |
| Illumina | 8 | 7 | 10 | 12 | 33 | 8 | 7 | 85 |
| MissionBio | 8 | 3 | 5 | 12 | 34 | 19 | — | 81 |
| ParseBio | — | 7 | 18 | 5 | 13 | 22 | — | 65 |
| **Total** | **36** | **44** | **69** | **49** | **118** | **71** | **7** | **394** |

Cell typing (118, 30%)과 Differential Expression (71, 18%)이 전체의 약 절반. Normalization (44)과 QC (36)은 단계당 distinct 문제 수가 적음. ParseBio는 vendor workflow가 cross-platform QC를 제공하지 않아 QC evaluation 없음 (§2.1).

**Tissue 커버리지** (Appendix A):
- PBMC: BD Rhapsody, CSGenetics, ParseBio — 168 evaluations
- Tumor microenvironment: Chromium — 60 evaluations (4T1 mammary carcinoma, CDX)
- Dorsal root ganglia (DRG): Illumina — 85 evaluations
- Hematopoietic: MissionBio — 81 evaluations (CCUS, clonal hierarchy)

### 2.2 모델 전체 성능

8개 frontier model, 4개 provider (Table 2, Figure 2):

| Model | Provider | Accuracy (%) | 95% CI | Latency (s) |
|---|---|---|---|---|
| **Claude Opus 4.6** | Anthropic | **52.8** | (48.3, 57.2) | 303 |
| Claude Opus 4.5 | Anthropic | 49.9 | (45.3, 54.4) | 154 |
| GPT-5.2 | OpenAI | 45.2 | (40.9, 49.5) | 133 |
| Claude Sonnet 4.5 | Anthropic | 44.2 | (39.9, 48.6) | 193 |
| GPT-5.1 | OpenAI | 37.9 | (33.7, 42.0) | 94 |
| Grok-4.1 | xAI | 35.6 | (31.6, 39.7) | 180 |
| Grok-4 | xAI | 33.9 | (30.1, 37.8) | 203 |
| Gemini 2.5 Pro | Google | 29.2 | (25.6, 32.9) | 300 |

- Best-to-worst spread: 23.6 pp (SpatialBench: 18.3 pp). scBench가 모델 능력을 더 잘 변별.
- Anthropic 모델이 top 4 독점. GPT-5.2는 3위로 Opus 4.5에 근접.
- Pareto-optimal (accuracy vs. cost): GPT-5.2가 낮은 비용으로 top-tier 근사 (Figure 3).
- Gemini 2.5 Pro: 최저 accuracy 29.2%, latency 300s로 cost-latency도 불리.

### 2.3 Task Category 분석

난이도 일관 gradient (Table 3, Figure 4):

| Task | Cross-model mean | 비고 |
|---|---|---|
| Normalization | 70.4% | 가장 쉬움 — 표준 변환, 함수 호출만 식별 |
| QC | 55.3% | |
| Dim. Reduction | ~ | |
| Clustering | 38.3% | |
| Cell Typing | 34.9% | |
| Differential Expression | 27.0% | 가장 어려움 — 다단계 과학적 판단 필요 |

- 8개 모델 중 7개가 동일한 난이도 순서를 따름.
- DE가 가장 discriminative (best-worst spread 27.7 pp). 모델 차이는 판단 집약적 task에서 집중됨.
- Normalization·QC: procedural 특성 강해 표준 구현 식별로 해결 가능.
- Cell typing·DE: marker gene 선택, cluster identity 해석, 통계 검정 선택, tissue-specific 특성 등 contextual 과학적 판단 필요 (§2.3).

### 2.4 Platform-Dependent Performance

플랫폼 선택이 모델 선택만큼 accuracy에 영향 (Table 4, Figure 5):

| Platform | Cross-model mean | 특이사항 |
|---|---|---|
| CSGenetics | 59.1% | 가장 쉬움. 8개 모델 중 6개에서 최고 |
| BD Rhapsody | ~ | |
| Illumina | ~ | |
| Chromium | ~ | |
| ParseBio | ~ | |
| MissionBio | 26.4% | 가장 어려움. 8개 모델 모두에서 최저 |

- CSGenetics vs. MissionBio: 32.7 pp 차이 → 모델 간 23.6 pp spread 초과.
- **MissionBio가 ranking을 역전시킴**: Grok-4 (6위 overall)가 MissionBio에서 GPT-5.2 (3위 overall)를 이김 (24.7% vs. 23.0%). Sonnet 4.5가 GPT-5.2를 11 pp 상회.
- **Gemini의 극단적 platform swing**: CSGenetics 52.4% → MissionBio 10.3%, 42 pp 하락.
- **Opus 4.5가 가장 일관**: best-worst platform 차이 39 pp로 상대적으로 작음.
- 원인: MissionBio (Tapestri)는 DNA+protein targeted platform, 비표준 데이터 구조, 공개 문서가 적음 → training data 편향 반영 (§2.4).

### 2.5 SpatialBench 비교

| | scBench | SpatialBench |
|---|---|---|
| Evaluations | 394 | 146 |
| Platforms | 6 | 5 |
| Task categories | 7 | 7 |
| Top model accuracy | 52.8% | 38.4% |
| Bottom model accuracy | 29.2% | 20.1% |
| Top-bottom spread | 23.6 pp | 18.3 pp |
| Easiest task (best model) | Norm. 84% | Norm. 76% |
| Hardest task (best model) | DE 41% | QC 22% |

- scRNA-seq가 spatial transcriptomics보다 tractable (더 많은 공개 데이터·툴 문서).
- Model ranking 극단부 보존: Opus가 양쪽 1위, Gemini가 양쪽 꼴찌.
- QC가 SpatialBench에서 hardest인 이유: 기술 특이적 threshold 지식이 결정적 (§2.5).

---

## Figure 분석

### Figure 1 — 플랫폼·Task 분포 바 차트 (p.2)
394 evaluation의 platform별(좌), task category별(우) 분포.  
**핵심**: Cell typing (118)이 단일 최대 category. ParseBio에 QC 없음. MissionBio와 Illumina가 platform 중 가장 많은 evaluation.

### Figure 2 — 모델 aggregate accuracy 바 차트 (p.3)
8개 모델의 전체 accuracy + 95% CI 에러바.  
**핵심**: Opus 4.6 (52.8%)과 Gemini (29.2%) 사이 23.6 pp. CI가 겹치지 않아 최상위·최하위 구분은 통계적으로 유의.

### Figure 3 — Accuracy vs. Cost / Accuracy vs. Latency scatter (p.4)
Pareto-optimal 모델을 점선으로 연결.  
**핵심**: GPT-5.2가 cost Pareto-frontier — 낮은 비용으로 3위 성능. Opus 4.6은 accuracy는 1위지만 비용·latency 모두 높음.

### Figure 4 — Task category별 accuracy 바 차트 (p.5)
8개 모델, 7개 task category. 난이도 순서(Norm. 가장 쉬움 → DE 가장 어려움)로 정렬.  
**핵심**: 난이도 gradient가 모델과 무관하게 일관. Trajectory analysis는 7개 evaluations로 CI가 매우 넓음.

### Figure 5 — Platform별 accuracy 바 차트 (p.6)
8개 모델, 6개 platform. cross-model mean 감소 순으로 정렬.  
**핵심**: MissionBio에서 전 모델 급락. Gemini의 CSGenetics→MissionBio 42 pp 하락이 시각적으로 두드러짐.

### Figure 6 — scBench vs. SpatialBench 비교 바 차트 (p.7)
scBench(solid) vs. SpatialBench(hatched), 모델별 나란히.  
**핵심**: scRNA-seq가 전 모델에서 일관되게 높음. Ranking 상·하위 보존.

---

## Table 분석

### Table 1 — Platform × Task category 평가 수 (p.2)
→ Figure 분석 참조. ParseBio QC=0, Illumina only가 Trajectory 보유.

### Table 2 — Overall model performance (p.3)
→ Results §2.2 참조.

### Table 3 — Task category별 accuracy, 95% CI (p.4)
각 task에서 best model 굵게 표시. Norm.에서 Opus 4.5가 83.8%로 최고.  
QC에서 Opus 4.5가 63.9%로 최고.

### Table 4 — Platform별 accuracy, 95% CI (p.5)
Chromium에서 Opus 4.6이 53.2%로 최고 (ParseBio는 Opus 4.6이 51.7%로 최고).  
MissionBio 최고: Opus 4.6 42.0%. Gemini MissionBio: 10.3%.

### Table 5 — scBench vs. SpatialBench 비교 요약 (p.6)
→ Results §2.5 참조.

### Table 6 — scBench evaluation 요약 (Appendix A, p.11)
Platform별 / Task category별 eval 수 재요약.

### Table 7 — Complete evaluation inventory (p.12-14)
394개 evaluation 목록: description, platform, task category, grader type.  
**중요 예시**:
- BD Rhapsody Treg marker (Cell Typ., P@K): canonical markers FOXP3, IL2RA, CTLA4, DUSP4, RGS1 (5종), recall@10 ≥ 0.60
- Chromium CAF subcluster (Cell Typ., Jaccard): Acta2, Col1a1, Mki67, Ly6c1 등 12 markers, Jaccard ≥ 0.60
- CSGenetics PBMC cell type proportions (DistributionComparison): 59.0%/20.3%/5.0%/14.8%/0.7%, ±5 pp/카테고리
- Illumina brain region adversarial (MCQ): DRG에서 brain-specific microglia signature가 가장 높게 보이는지 여부로 tissue context 이해 테스트
- MissionBio CCUS clonal hierarchy (MCQ): DNA variant call + cell label 통합 필요
