# scBench — core

## Executive Summary

- **무엇**: scRNA-seq 분석을 수행하는 LLM agent(코드를 쓰고 도구를 호출하며 목표를 향해 반복하는 frontier model)를 평가하는 benchmark. 실제 워크플로우에서 추출한 394개의 *검증 가능한(verifiable)* 문제 + deterministic grader로 구성되며, agent가 messy한 real-world 데이터에서 생물학적 결과를 재현할 수 있는지를 pass/fail로 채점한다.
- **모델 / 방법**: 각 문제는 (1) 분석 단계 직전의 데이터 snapshot(주로 AnnData `.h5ad`), (2) 자연어 task prompt(정확한 JSON 출력 schema 포함), (3) agent의 구조화된 JSON 출력을 채점하는 deterministic grader 3요소로 이루어진다. grader는 5개 family로 분기하고($\mathrm{NumericTolerance}$, $\mathrm{DistributionComparison}$ 등), 각 평가는 scientific / procedural / observational 3개 유형 중 하나로 분류되어 tolerance 폭을 결정한다. 통합 점수는 8개 frontier model을 mini-SWE-agent harness 아래에서 3 replicate로 돌려 산출한다.
- **핵심 결과**:
  - ① 8개 frontier model 전체 정확도 29–53% 범위. 최고 Claude Opus 4.6 = 52.8% (95% CI 48.3–57.2), 최저 Gemini 2.5 Pro = 29.2%. best–worst spread 23.6 pp.
  - ② Task 난이도 gradient 일관: Normalization이 가장 쉬움(cross-model mean 70.4%), Differential Expression이 가장 어려움(mean 27.0%). 8개 중 7개 model이 동일 난이도 순서.
  - ③ Platform 효과가 model 선택만큼 큼: cross-model mean이 CSGenetics 59.1% → MissionBio 26.4%로 32.7 pp 차이(23.6 pp의 model spread를 초과). Gemini는 platform 간 42 pp swing.
  - ④ SpatialBench(공간 transcriptomics) 대비: 같은 harness에서 top model이 scBench 52.8% vs SpatialBench 38.4%로 scRNA-seq가 더 tractable. model ranking은 양 극단에서 보존(Opus 1위, Gemini 꼴찌).
- **우리 적용**: chromatin-lag biology와 직접 관련은 낮다(이 paper는 agent 평가 benchmark이지 velocity/multiome method가 아님). 다만 (a) scRNA-seq 분석을 LLM agent에 위임할 때 어느 model·task·platform이 실패하는지의 정량 근거 → 내부 파이프라인의 agent 선정/검증 기준으로 `internal-tool-evaluation`, (b) deterministic grader + evaluation-type tiering 설계는 우리 자체 분석 자동화의 평가 프레임 reference로 `methodology-reference`.
- **심층**: 한계·재현 ROI는 `workman-2026-scbench_lens-academic.md` / `workman-2026-scbench_lens-industry.md` / `workman-2026-scbench_methodology-brief.md` 참고.

## Identity

- **Title**: scBench: Evaluating AI Agents on Single-Cell RNA-seq Analysis
- **Authors**: Kenny Workman, Zhen Yang, Harihara Muralidharan, Aidan Abdulali, Hannah Le (LatchBio, San Francisco, CA)
- **Year**: 2026
- **Venue**: arXiv preprint (q-bio.GN), "Preprint. Under review."
- **arXiv ID**: 2602.09063v1 (2026-02-09)
- **DOI**: 없음 (preprint)
- **Correspondence**: kenny@latch.bio
- **Citation key**: `workman2026scbench`

## Background

### 배경 스토리

- **문제의 출발점**: scRNA-seq는 분자 상태를 single-cell 해상도로 측정하는 핵심 assay다. 데이터셋이 커지고 사용 범위가 넓어지면서, 과학적 결론은 통계·고차원 데이터 분석·프로그래밍을 잇는 다단계·자원 집약적 계산 방법에 점점 더 의존하게 됐다. 많은 연구 그룹에서 시퀀싱이 아니라 *분석*이 rate-limiting step이 됐다 (Introduction, Lähnemann et al. 2020 인용).
- **선행 접근 A — LLM coding agent의 부상**: 코드를 작성하고 도구를 호출하며 목표를 향해 반복하는 agent(LLM)가 software engineering과 일반 data analysis에서 빠르게 능력을 키웠다 (Yang et al. 2024 인용). 그러나 scRNA-seq에 적용하면 여전히 신뢰성이 낮고 underpowered하며, 과학적 부정확성·hallucination이 잦고, messy한 real-world dataset에 의존하는 domain-specific 분석 단계를 자주 완수하지 못한다 (Introduction §1).
- **선행 접근 B — 기존 biology benchmark**: 기존 benchmark는 recall, interpretation, literature-style reasoning을 강조한다 (Jin et al. 2019, Tinn et al. 2023 인용). 이들은 데이터와의 *경험적 상호작용*을 요구하지 않으며 real-world 분석 작업을 충실히 대표하지도 않는다.
- **이 논문으로 이어지는 gap**: 그 결과로 데이터에 근거한(data-grounded) scRNA-seq 분석을 측정할 *표준적·deterministic한 잣대*가 부재하다. scBench는 이 gap을 메우기 위해 도입됐다.
- **자매 benchmark와의 관계**: 저자들의 SpatialBench(Workman et al. 2025, 공간 transcriptomics)와 짝을 이뤄, single-cell의 두 주요 전사체 assay(scRNA-seq와 spatial)를 함께 커버한다. scBench는 측정 도구이자 agent 개발을 위한 진단 lens 역할을 의도한다.

### 기본 개념

- **scRNA-seq 분석 파이프라인 (task category의 근거)**: raw count matrix → QC(저품질 세포 제거) → Normalization → Dimensionality Reduction(PCA 등) → Clustering → Cell Typing → Differential Expression → (선택) Trajectory Analysis. scBench의 7개 task category가 이 단계들에 대응한다.
- **Agent**: 코드를 작성하고, 도구를 호출하고, 결과를 보고 반복하며 목표를 향해 움직이는 LLM 기반 시스템. 본 paper에서는 mini-SWE-agent harness 아래에서 실행되는 8개 frontier model을 가리킨다.
- **Verifiable problem**: 정답이 deterministic하게 채점 가능한 구조화된 정량 artifact(named field + value type을 갖는 JSON)로 환원되는 문제. 주관적 해석("interesting", "meaningful") 없이 pass/fail로 판정된다.
- **Deterministic grader**: agent의 JSON 출력을 ground truth와 비교해 자동·재현적으로 pass/fail을 내는 채점기. tolerance와 threshold로 방법론적 변동을 흡수한다.
- **외부 맥락**: mini-SWE-agent / SWE-agent는 software-engineering agent harness 계열이다 (본문은 Yang et al. 2024를 인용하나 harness 내부 구현 세부는 PDF에 미제공).

## Methods

> 자료 유형: AI-agent benchmark preprint. method 중심이되 확률 모델이 아니라 *benchmark 구성·채점 설계*가 핵심이므로, core-methods의 adaptive depth에 따라 "benchmark 설계 + grading 구조" 중심으로 정리한다.

### 이 method가 푸는 문제

- **Formal task**: scRNA-seq 분석 능력을 가진 agent를, *데이터와의 경험적 상호작용*을 요구하고 *deterministic하게 채점 가능한* 단위 문제들의 집합으로 측정한다.
- **입력 (agent가 보는 것)**: 한 개 이상의 AnnData `.h5ad` 파일을 가리키는 *data node*(expression matrix + cell metadata `.obs` + gene annotation `.var`; runtime에 isolated workspace로 다운로드), 정확한 JSON 출력 format을 명시한 자연어 *task prompt*, 그리고 *metadata* tag(task category, evaluation type, platform, computational complexity).
- **출력 (agent가 내는 것)**: prompt가 지정한 schema를 따르는 structured JSON. grader가 이를 ground truth와 대조한다.
- **추정 대상 (benchmark가 측정하는 것)**: 문제별 pass/fail, 그리고 이를 model × task × platform으로 집계한 정확도.
- **중요한 hidden assumption**: 과학적 판단을 *automatically checkable한 조각*으로 이산화(discretize)할 수 있다는 가정. 각 문제는 long-horizon iteration이 아니라 *단일 워크플로우 단계*의 snapshot을 본다(저자도 한계로 명시 — Discussion §3).

### 확률 / 통계학적 구조

- **Grading model**: 확률 generative model이 아니라 deterministic rule 기반 채점. 출력 모양에 맞는 5개 grader family가 있다. 본문에 명시된 예: cell count류에는 $\mathrm{NumericTolerance}$, cell type proportion류에는 $\mathrm{DistributionComparison}$ (Methods §4.1, §4.4).
- **Tolerance 결정**: 각 문제는 scientific / procedural / observational 3개 *evaluation type* 중 하나로 분류되고, 이 유형이 tolerance를 얼마나 공격적으로 풀어줄지를 지배한다 (Methods §4.3). scientific은 가장 넓은 tolerance(method·parameter 모두 agent 재량), procedural은 method가 고정되어 더 tight, observational은 verifiability/anti-shortcut 요건을 완화.
- **Tolerance calibration**: 같은 데이터에 대해 *여러 valid method·parameter*로 분석을 돌려 acceptable answer의 범위를 잡고, 그 범위를 tolerance로 설정한다 (Methods §4.1). 저자가 parameter를 유일하게 명시하지 않은 경우(예: QC threshold 미보고)는 standard default를 쓰고 tolerance를 넓힌다.
- **집계 통계**: 통합 정확도는 8 model × 394 eval × 3 replicate를 *two-stage aggregation*으로 묶고, 95% CI를 $t$-분포로 계산한다 (Figure 2 caption).
- **Uncertainty / shortcut 처리**: precomputed embedding·cached label·정답을 그냥 읽을 수 있게 하는 field를 제거해 anti-shortcut 구조를 만든다. 추가 QC로 각 문제를 (a) `.obs`/`.uns` 직접 읽기, (b) 사전 생물학 지식으로 답하기, (c) 다른 valid method로 풀기로 시도해 tolerance coverage를 점검하고, 실패하는 문제는 수정·제거한다 (Methods §4.1).

### 핵심 method insight

- **기존 방법의 한계**: 기존 biology benchmark는 literature recall·interpretation을 측정할 뿐 데이터와의 경험적 상호작용을 요구하지 않는다. 따라서 "이 agent가 실제 데이터를 분석해 옳은 생물학적 결과를 내는가"를 가릴 수 없다.
- **이 논문이 바꾼 가정**: "answer를 검증 가능한 정량 artifact로 환원하고, 방법론적 자유는 tolerance로 흡수한다"는 설계. 즉 *specify what, not how* — task는 과학적 목표와 정확한 출력 format만 정의하고 step-by-step 방법은 강제하지 않는다(procedural 평가만 method를 명시)(Methods §4.4).
- **새로 추가한 구조**: (1) evaluation type 3분류로 tolerance를 차등화, (2) 5개 grader family로 출력 모양별 채점, (3) deterministic *linter*가 schema 정합성(required field, grader config, tolerance type, answer field와 prompt 일치)을 사전 검증해 ambiguous/shortcut-prone eval을 block (Methods §4.2).
- **이 변화가 중요한 이유**: 채점이 주관적 해석 없이 자동·재현적으로 이뤄지므로, agent 개발에서 test-driven development가 가능한 *evolving specification*이 된다.

### 이전 방법과의 차이

- **Baseline benchmark**: literature-style biology benchmark(PubMedQA류, Jin et al. 2019 / Tinn et al. 2023). 그리고 동일 저자의 SpatialBench(공간 transcriptomics).
- **공통점**: SpatialBench와 동일한 mini-SWE-agent harness, 동일한 3가지 design 원칙(specify what not how / verifiability / scientific durability), 동일한 5-stage 문제 구성 파이프라인.
- **차이점**: 대상 assay가 scRNA-seq(6 platform)로 바뀌고, eval 수가 394개(SpatialBench 146개)로 더 크며, task category 7개는 공유하되 분포가 다르다.
- **차이가 크게 나타나는 조건**: 같은 harness에서 scRNA-seq가 spatial보다 전반적으로 풀기 쉽다(top 52.8% vs 38.4%). 저자 해석: scRNA-seq의 public dataset과 tooling(예: Scanpy) 문서가 훨씬 풍부하기 때문(Results §2.5).

### 효과가 Results에서 나타난 방식

- **Benchmark / dataset**: 394 eval, 6 platform, 7 task category (Table 1, Figure 1).
- **Metric**: pass/fail 기반 accuracy(%), 95% CI.
- **드러난 결과**: model 간 23.6 pp spread → benchmark가 model 능력을 *discriminate*함. task·platform 양축의 stratified gradient가 일관 → 측정이 안정적.
- **정성적 효과**: 판단이 많이 필요한 단계(DE, cell typing)에서 model 차이가 집중되고, 절차적 단계(normalization)에서는 수렴한다. 즉 scBench는 "general coding 능력"이 아니라 "domain 판단"을 가른다.

### Method 관점의 한계

- **약한 assumption**: 과학적 판단의 이산화. 각 eval이 *단일 워크플로우 단계*만 보므로, 오류가 누적되는 long-horizon iteration은 측정하지 못한다 (Discussion §3, 저자 명시).
- **구현/운영 부담**: ground truth를 author-specified parameter로 published pipeline을 재실행해 산출하고 도메인 기대값과 대조하는 수작업 검증이 필요. parameter 미보고 시 default + 넓은 tolerance로 처리.
- **일반화가 불확실한 조건**: deterministic grader가 가능한 문제만 포함되므로, operational definition이 없는 주관적 task("interesting cluster" 등)는 구조적으로 배제된다.

## Results

### Dataset 구성 (Table 1, Figure 1)

- scBench = 394 eval, 6 sequencing platform × 7 task category. 각 eval은 data snapshot(주로 AnnData `.h5ad`) + 자연어 task + deterministic grader.
- **Task 분포**: Cell Typing 118 (30%)와 Differential Expression 71 (18%)이 거의 절반. Dim. Reduction 69, Clustering 49, Normalization 44, QC 36, Trajectory 7. Normalization·QC가 작은 이유는 절차적 단계라 dataset당 distinct 문제 형식이 적기 때문 (Results §2.1).
- **Platform 분포**: Illumina 85 → MissionBio 81 → ParseBio 65 → BD Rhapsody 61 → Chromium 60 → CSGenetics 42. ParseBio는 vendor workflow가 명시적 quality filtering을 생략해 QC eval이 없음(5개 platform만 QC 비교 가능). MissionBio Tapestri는 RNA-seq가 아니라 targeted DNA+protein platform인데, agent가 transcriptomic을 넘어 관련 single-cell 분석 패턴(clustering, protein marker 기반 cell typing, variant interpretation)에 일반화하는지를 stress-test하려 포함했다 (Results §2.1).

### 전체 model 성능 (Table 2, Figure 2)

- 4개 provider의 8개 frontier model, 3 replicate, mini-SWE-agent harness.

| Model | Provider | Accuracy (%) | 95% CI | Latency (s) |
|---|---|---|---|---|
| Claude Opus 4.6 | Anthropic | 52.8 | (48.3, 57.2) | 303 |
| Claude Opus 4.5 | Anthropic | 49.9 | (45.3, 54.4) | 154 |
| GPT-5.2 | OpenAI | 45.2 | (40.9, 49.5) | 133 |
| Claude Sonnet 4.5 | Anthropic | 44.2 | (39.9, 48.6) | 193 |
| GPT-5.1 | OpenAI | 37.9 | (33.7, 42.0) | 94 |
| Grok-4.1 | xAI | 35.6 | (31.6, 39.7) | 180 |
| Grok-4 | xAI | 33.9 | (30.1, 37.8) | 203 |
| Gemini 2.5 Pro | Google | 29.2 | (25.6, 32.9) | 300 |

- best–worst spread 23.6 pp가 SpatialBench의 18.3 pp를 초과 → 더 높은 전체 정확도에도 model을 잘 변별 (Results §2.2).
- Anthropic이 상위 4위 독점(Opus 2종 + Sonnet). Pareto 관점(Figure 3): GPT-5.2가 낮은 cost/latency로 near-top accuracy, Opus 4.6은 최고 정확도지만 cost·latency가 높음.

### Task category 분석 (Table 3, Figure 4)

- 일관된 난이도 gradient: **Normalization 가장 쉬움(cross-model mean 70.4%)** → QC 55.3% → Clustering 38.3% → Cell Typing 34.9% → **Differential Expression 가장 어려움(27.0%)** (Results §2.3).
- 8개 중 7개 model이 동일 난이도 순서를 따른다.
- DE가 가장 *discriminative*: best–worst 27.7 pp spread. model 차이는 judgment-heavy 단계(DE, cell typing)에 집중되고 절차적 단계에는 거의 없다.
- Table 3 best-per-task(95% CI): QC Opus 4.5 = 63.9, Norm. Opus 4.5 = 83.8, Dim. Red. Opus 4.6 = 55.4, Clust. Opus 4.6 = 52.7, Cell Typ. Opus 4.6 = 48.2, Diff. Expr. Opus 4.6 = 41.4.

### Platform 의존 성능 (Table 4, Figure 5)

- Platform 선택이 model 선택만큼 정확도를 좌우. cross-model mean accuracy가 **CSGenetics 59.1% → MissionBio 26.4%**로 32.7 pp 차이(23.6 pp의 model spread 초과)(Results §2.4).
- CSGenetics가 8개 중 6개 model에서 가장 쉬움; MissionBio가 8개 모두에서 가장 어려움.
- **Ranking 역전**: MissionBio에서는 Grok-4(전체 6위)가 GPT-5.2(전체 3위)를 이김(24.7% vs 23.0%), Sonnet 4.5가 GPT-5.2를 11 pp 앞섬. Anthropic model은 MissionBio에서 버티고 대부분 경쟁자는 붕괴.
- 모든 model이 큰 platform swing: Gemini는 CSGenetics 52.4% ↔ MissionBio 10.3%로 42 pp 하락. 가장 일관적인 Opus 4.5도 best–worst 39 pp 손실. 저자 해석: 불균등한 training data(MissionBio가 public 문서에 덜 등장)(Results §2.4).
- Table 4 best-per-platform: CSGenetics Opus 4.5 = 77.0, BD Rhapsody Opus 4.5 = 55.7, Illumina GPT-5.2 = 54.5, Chromium Opus 4.6 = 51.7, ParseBio Opus 4.6 = 53.2, MissionBio Opus 4.6 = 42.0.

### scBench vs SpatialBench 비교 (Table 5, Figure 6)

| 지표 | scBench | SpatialBench |
|---|---|---|
| Number of evaluations | 394 | 146 |
| Number of platforms | 6 | 5 |
| Number of task categories | 7 | 7 |
| Top model accuracy | 52.8% | 38.4% |
| Bottom model accuracy | 29.2% | 20.1% |
| Top–bottom spread | 23.6 pp | 18.3 pp |
| Easiest task (best model) | Norm. 84% | Norm. 76% |
| Hardest task (best model) | DE 41% | QC 22% |

- scRNA-seq가 더 tractable하지만 *ranking은 양 극단에서 보존*(Claude Opus 1위, Gemini 꼴찌, 양 benchmark 공통). 둘 다 Normalization이 가장 쉽고 platform별 30–40 pp swing을 보인다. 정확도 격차는 training data 차이(scRNA-seq의 public dataset·Scanpy 문서가 훨씬 풍부)에서 비롯한다는 해석 (Results §2.5).

### 전체 결과 요약

- frontier agent는 scRNA-seq에서 *어느 정도* 능력을 보이지만, messy real-world dataset에서 생물학적 통찰을 충실히 추출하지는 못한다. 최고가 52.8%로 개선 여지가 크다.
- 23.6 pp의 model spread와 task·platform별 행동 변화 → scBench가 능력을 변별함을 보인다.
- 실무적 함의: 오늘날 agent는 routine 분석을 가속할 수 있으나, 중간 결과의 엄격한 검증과 사람 감독 없이 과학적 질문에 자율적으로 답하도록 신뢰할 수는 없다 (Discussion §3).

## Figures

> 본문 Figure 6개. 모두 PDF 본문에 정식 게재. 패널은 대부분 막대그래프/산점도이며 별도 sub-panel label(a,b,…)은 표기되지 않음.

#### Figure 1 — 394 eval의 platform × task 분포
- **패널별 설명**: 좌측 "By Platform" 가로 막대(Illumina 85, MissionBio 81, ParseBio 65, BD Rhapsody 61, Chromium 60, CSGenetics 42), 우측 "By Task Category" 가로 막대(Cell Typing 118, Diff. Expr. 71, Dim. Reduction 69, Clustering 49, Normalization 44, QC 36, Trajectory 7).
- **본문에서 강조한 비교**: cell typing과 differential expression이 지배적; ParseBio는 QC eval 없음 (caption).
- **해석 시 주의점**: 막대 수치는 Table 1의 marginal total과 일치. eval 분포가 task별로 매우 불균형(Trajectory 7개)이므로 Trajectory 결과는 소표본임을 유념.

#### Figure 2 — 8개 model 통합 정확도
- **패널별 설명**: model별 정확도 막대 + 95% CI error bar. Opus 4.6 = 52.8 부터 Gemini 2.5 Pro = 29.2 까지 단조 감소.
- **본문에서 강조한 비교**: best–worst 23.6 pp; Anthropic 상위 4위 (§2.2).
- **해석 시 주의점**: CI는 two-stage aggregation + $t$-분포(caption). CI가 서로 겹치는 인접 model(예: GPT-5.2 vs Sonnet 4.5)은 통계적으로 동급일 수 있음.

#### Figure 3 — 정확도 vs cost / latency (Pareto)
- **패널별 설명**: 좌 "Accuracy vs Cost"(x축 Cost per Eval USD), 우 "Accuracy vs Latency"(x축 Latency per Eval s). 점선이 Pareto-optimal model 연결.
- **본문에서 강조한 비교**: GPT-5.2가 낮은 cost로 near-top accuracy; Opus 4.6은 최고 accuracy지만 cost·latency 큼 (caption).
- **해석 시 주의점**: x축 cost 절대값은 시점·API 가격에 의존. 운영 의사결정에 그대로 옮길 때 가격 변동 주의.

#### Figure 4 — model × task category 정확도
- **패널별 설명**: 7개 task(난이도 순, normalization 쉬움 → DE 어려움)에 대한 8 model grouped bar + 95% CI.
- **본문에서 강조한 비교**: 난이도 gradient가 model 전반에 일관 (caption, §2.3).
- **해석 시 주의점**: 수치는 Table 3와 대응. Trajectory는 Figure 4 막대에 포함되지 않은 듯(Table 3에 Traj. 열 없음) — Trajectory 7개 eval은 소표본이라 별도 stratified 분석에서 제외된 것으로 보임. `검토필요:` Trajectory의 model별 정확도는 본문·표에 명시 없음.

#### Figure 5 — model × platform 정확도
- **패널별 설명**: 6개 platform(cross-model mean 내림차순: CSGenetics → BD Rhapsody → Illumina → Chromium → ParseBio → MissionBio)에 대한 8 model grouped bar + 95% CI.
- **본문에서 강조한 비교**: 큰 platform swing, MissionBio collapse, ranking 역전 (§2.4).
- **해석 시 주의점**: 수치는 Table 4와 대응.

#### Figure 6 — scBench vs SpatialBench (model별)
- **패널별 설명**: 8 model에 대해 scBench(solid bar) vs SpatialBench(hatched bar) 정확도, 50% 기준선 표시, 95% CI.
- **본문에서 강조한 비교**: scRNA-seq가 일관되게 높지만 ranking 보존(Opus 최상, Gemini 최하)(caption).
- **해석 시 주의점**: 두 benchmark는 eval 수·platform이 달라 절대 비교보다 *ranking 보존*에 의미를 둔다.

## Tables

#### Table 1 — platform × task별 eval 수
- **무엇을 비교**: 6 platform × 7 task의 eval 개수와 marginal total(총 394).
- **본문에서 강조한 비교**: cell typing(118)·DE(71) 지배, ParseBio QC 결측(§2.1).
- **해석 시 주의점**: Trajectory 총 7개(Illumina 7, 나머지 0). 소표본.

#### Table 2 — 통합 model 성능
- **무엇을 비교**: 8 model의 accuracy / 95% CI / latency(s). (본문 위 Results §전체 model 성능에 전재.)
- **해석 시 주의점**: latency는 per-eval 초. accuracy와 독립적으로 봐야(예: GPT-5.1이 최저 latency 94s지만 정확도 37.9%).

#### Table 3 — task category별 정확도 (95% CI, best per task bold)
- **무엇을 비교**: 8 model × 6 task(QC, Norm., Dim. Red., Clust., Cell Typ., Diff. Expr.)의 정확도.
- **해석 시 주의점**: Trajectory 열이 없다 — 소표본이라 stratified 표에서 제외된 것으로 보임. 난이도 gradient(§2.3)의 근거 표.

#### Table 4 — sequencing platform별 정확도 (95% CI, best per platform bold)
- **무엇을 비교**: 8 model × 6 platform 정확도.
- **해석 시 주의점**: platform swing·ranking 역전(§2.4)의 근거 표. CSGenetics가 6개 model에서 best, MissionBio가 8개 모두에서 worst.

#### Table 5 — scBench vs SpatialBench 요약
- **무엇을 비교**: eval/platform/task 수, top·bottom model 정확도, spread, easiest/hardest task. (본문 위 Results §비교에 전재.)
- **해석 시 주의점**: cross-benchmark 비교는 ranking 보존 중심으로 해석.

## Supplementary Information

- **미제공**: 본 PDF(8 page)에는 formal Supplementary Note·Supplementary Figure·Supplementary Table 섹션이 포함되어 있지 않다. paper-info.yaml의 `sources.supplementary`도 빈 배열.
- **코드/벤치마크 공개**: paper-info.yaml의 `sources.data`에 GitHub(latchbio/scbench)가 `url-only`로 기록되어 있고 "benchmark framework, graders, linter, agent harness; 30 canonical evals public"이라는 note가 있다. `검토필요:` 단, 이 GitHub URL과 "30 canonical evals public" 문구는 본 PDF 본문(p.1–8)에서 직접 확인되지 않았다. 본문에서 확인된 것은 isolated workspace로 `.h5ad`를 다운로드하는 harness 운용과 mini-SWE-agent harness 사용까지다. URL/공개 범위는 별도 검증 필요.
- **Methods 절단**: PDF p.8(Methods §4.4 "Scientific durability")이 문장 중간에서 끝난다 — 이 arXiv v1의 본문 텍스트가 8 page에서 절단된 것으로 보인다. §4.4 이후(추가 design 원칙, §4.5 grader family 상세 등)는 `미제공:` 상태. grader family 5종 중 본문에서 이름이 확인된 것은 $\mathrm{NumericTolerance}$, $\mathrm{DistributionComparison}$ 2종뿐.

## 분석 자체에 대한 메모

- `검토필요:` PDF가 §4.4 중간에서 절단되어 §4.5(grader family 전체 정의)와 이후 내용이 누락. arXiv abstract 페이지 또는 최신 버전(v2 이상)에서 full Methods를 받아 grader family 5종과 §4.5를 보완하면 좋다.
- `질문:` GitHub repo(latchbio/scbench)가 실제 public인지, "30 canonical evals"가 무엇인지 확인 필요 — 우리가 자체 grader 프레임을 만든다면 직접 참조할 1차 자산.
- `질문:` Trajectory(7 eval)·observational evaluation type의 model별 성능은 본문에 분해 없음. agent를 trajectory/velocity 분석에 위임할 경우의 신뢰도는 이 benchmark로 알 수 없다 — 우리 chromatin-lag 주제와 가장 가까운 task인데 데이터가 가장 얇다.
- `해석:` 우리 팀 관점에서 가장 재사용 가치 높은 부분은 결과 수치가 아니라 *evaluation-type tiering + deterministic linter + tolerance calibration* 설계다. 자체 분석 자동화의 평가 layer에 그대로 차용 가능.
