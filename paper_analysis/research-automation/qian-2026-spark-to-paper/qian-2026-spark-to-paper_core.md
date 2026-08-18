# Qian et al., 2026 — Spark-to-Paper — core 분석

> 근거 자료: `sources/fulltext_extract.md`(arXiv:2608.11924 HTML fulltext, WebFetch 자동추출 2026-08-18). 저자 자체 추출본이 아니라 fulltext HTML 자동추출이므로, 본문에 텍스트로 명시된 구조·수치만 단정하고 §번호가 걸리는 인용은 `검토필요:`로 둔다.
>
> 표기: `해석:`(분석자 재구성) / `외부 맥락:` / `추정:` / `미제공:`(본문에 없음) / `검토필요:`(§·정확 위치 불확실).

---

### Background

#### 배경 스토리

- **문제의 출발점**: end-to-end 논문 생성(연구 질문 설정부터 인용, 집필, 그림, 조립까지)을 자동화하려는 흐름이 있다. 본문의 문제 정의는 짧다. 기존 자율 연구 에이전트는 "standalone applications with their own orchestration layers"(자체 오케스트레이션 계층을 갖춘 독립 애플리케이션)를 요구하는 반면, 현대적 coding assistant(코딩 보조 도구)는 이미 연구 자동화에 필요한 기본 능력을 제공한다는 것이 저자의 대비다.

- **선행 접근 A (자율 연구 에이전트 계열)**: 논문 생성을 위해 별도 플랫폼을 세우는 방식. 본문에 이름이 나오는 인스턴스는 AI Scientist(Lu 2024), AI Scientist-v2(Yamada 2025), Agent Laboratory(Schmidgall 2025)다. 이들은 논문을 end-to-end로 뽑는 것을 이미 보였다.
  - `해석:` 저자가 A를 "동기가 된 선행 한계"로 명시적으로 비판했다고 본문이 말하지는 않는다. A는 본문에서 baseline audit 대상으로 등장한다. 따라서 아래 A의 한계는 저자의 motivating critique가 아니라 이 논문의 audit에서 관측된 값으로 읽어야 한다.

- **A의 한계 (이 논문의 audit에서 관측됨)**: 이전 자율 시스템의 그림은 raster(래스터 이미지)로 임베드되어 편집 가능한 요소가 0–3%에 그쳤다. citation validity는 AI Scientist 93%, AI Scientist-v2 91%, Agent Laboratory 96%로 측정됐다. 별도 플랫폼(자체 orchestration)을 세워야 한다는 인프라 부담이 있다.

- **선행 접근 B (single-pass LLM 생성)**: gate(관문 검사)나 review(검토) 없이 LLM이 원고를 한 번에 직접 생성하는 방식. 별도 인프라가 필요 없고 저렴하다(11 만 token, $0.66, 16분).

- **B의 한계 (이 논문의 audit에서 관측됨)**: 검증 장치가 없어 citation validity가 81%로 떨어지고, 심어 둔 fabrication(날조) probe 36개 중 5개(14%)만 탐지된다. 근거 없는 정량 주장을 걸러 내지 못한다.

- **이 논문으로 이어지는 gap**: `해석:` 별도 자율 플랫폼(A)은 무겁고, 단순 single-pass 생성(B)은 검증이 없다. 저자가 던진 핵심 질문은 "end-to-end 논문 생성을 별도 자율 플랫폼이 아니라 기존 coding assistant 안의 재사용 가능한 skill 묶음으로, 그리고 결정론적 gate와 model-based review를 얹은 검증 스택 위에서 돌릴 수 있는가"이다.

#### 기본 개념

- **coding assistant 내장 skill**: 이 논문의 시스템은 독립 플랫폼이 아니라 Claude Code라는 coding assistant 위에서 도는 13개의 composable skill(조합 가능한 skill) 묶음이다. skill은 stage(단계)별로 호출되며, 별도 orchestration 계층을 새로 만들지 않는다.

- **8-stage pipeline과 결정론적 gate**: 입력 분류(Stage 0)부터 조립(Stage 7), 조건부 실험(Stage 8)까지 8단계로 나뉘고, 각 stage는 다음으로 넘어가기 전에 결정론적 gate(정해진 규칙으로 통과 여부를 판정하는 검사)를 통과해야 한다.

- **검증 스택의 두 층위**: 결정론적 gate는 "규칙으로 판정 가능한 것"(placeholder 미해결, 인용 key 오류, 컴파일 실패 등)만 막을 수 있다. "논증이 충분히 뒷받침되는가, 섹션 간 개념 정합이 맞는가"는 결정론적으로 판정할 수 없어 model-based review(self-review와 adversarial review)를 얹는다.

- **preregistration(사전등록)과 evidence grounding**: 실험 실행 전에 planning stage가 dataset, baseline, metric, ablation, result table 구조를 미리 고정하고 수치 칸만 비워 둔다. planning(계획)과 reporting(보고)을 분리해 사후에 프로토콜을 결과에 맞춰 바꾸는 위험을 줄이려는 lightweight preregistration이다.

#### 이 논문이 필요한 이유

- **핵심 이유**: 자율 논문 생성을 별도 인프라 없이 기존 coding assistant의 skill 조합으로 구현할 수 있는지, 그리고 그 위에 검증 스택을 얹어 fabrication과 인용 오류를 줄일 수 있는지를 확인한다.
- **기존 방법으로 부족했던 지점**: 자율 에이전트 계열은 독립 플랫폼을 요구하고 그림이 편집 불가능한 raster였으며, 검증 없는 single-pass 생성은 날조를 거의 걸러 내지 못했다.
- **이 논문이 해결하려는 방향**: 13 skill을 8-stage pipeline으로 엮고, 결정론적 gate와 model-based review, preregistration, claim admission을 검증 스택으로 결합한다.

---

### Results

> 전제(본문 명시): 여기의 CI(신뢰구간)는 개별 run 단위가 아니라 **paper 단위(n > 3)**로 계산됐다. 비용·token의 불확실성 범위도 공개돼 있다. 이전 시스템 값은 재실행이 아니라 공개 artifact에서 읽은 것이며 model backbone·pricing을 정규화하지 않았다(저자: "mark unavailable measurements as not reported rather than estimating them").

#### 평가 축별 결과

##### 평가 범위(sample)

- 주 평가: 외부에서 선정한 8개 research topic(사전등록). single-pass와의 paired 비교는 **3 topic**뿐이다. human preprint audit는 8편, 이전 시스템 audit는 공개 artifact 사용(재실행 없음).
- `미제공:` cross-template robustness(다른 venue 템플릿에서의 견고성)는 본문에 언급되나 main table에 수치가 없다.
- `논문 주장과의 연결`: 평가가 8개 통제된 topic과 human preprint 8편에 한정되므로, 저자도 이를 체계적 audit이 아닌 controlled 범위로 인정한다.

##### 1. Citation validity (인용 유효성)

- **목적**: 생성된 인용의 서지 metadata가 외부에서 검증되는가. in-pipeline gate와 독립적으로 감사.
- **Metric / 평가 기준**: DOI/arXiv/metadata 대조로 유효 인용 비율.
- **Baseline / 비교 대상**: human preprint, AI Scientist, AI Scientist-v2, Agent Laboratory, single-pass LLM.
- **주요 수치**(각 값에 denominator 명기):
  - Spark-to-Paper(full): **99.5% [98.4–100%]**, 384 refs / 8 papers.
  - Human preprint: 97.8% [94.6–99.4%], 320 refs.
  - AI Scientist: 93% (42/45). AI Scientist-v2: 91% (58/64). Agent Laboratory: 96% (27/28).
  - single-pass LLM: 81% [76–86%].
  - `해석:` 인용 형식·해소(resolution) 수준에서는 human preprint(97.8%)와 겹치는 구간이 있고 single-pass(81%)와는 뚜렷이 갈린다. denominator가 384 대 45/64/28로 크게 달라 이전 시스템 값은 소표본이다.
- **caveat(저자)**: 이 metric은 외부 metadata 검증이라 인용의 의미적 정확성이나 맥락 적절성은 보증하지 않는다.
- **논문 주장과의 연결**: 검증 스택이 malformed·미해결 인용 key를 걸러 낸다는 Citation Gate의 효과를 뒷받침.

##### 2. Figure editability (그림 편집 가능성)

- **목적**: 생성된 그림이 raster 임베드가 아니라 편집 가능한 vector 요소로 이뤄졌는가.
- **Metric / 평가 기준**: ground-truth figure 요소 중 편집 가능한 비율(약 1,900개 요소 기준).
- **Baseline / 비교 대상**: human preprint, 이전 자율 시스템.
- **주요 수치**:
  - Spark-to-Paper: **96.4% [92.7–98.6%]** of ~1,900 ground-truth figure elements editable.
  - Human preprint: 58% [44–71%].
  - 이전 자율 시스템: 0–3%(raster 임베드).
- **caveat(저자)**: 의도적으로 raster를 제외했다. 저자 스스로, 생성된 explanatory figure가 human의 것보다 오히려 editable 하기 쉬운 셈이라고 적는다(이 프레이밍은 저자의 것).
- **논문 주장과의 연결**: method figure를 raster→HTML 재구성→vector PDF로 만드는 Figure 단계의 산물이 편집 가능함을 보임.

##### 3. Fabrication detection — ablation (날조 탐지, 구성 요소 제거 실험)

- **목적**: 검증 스택 각 층을 더할 때 seeded fabrication probe 탐지율이 어떻게 변하는가.
- **데이터 규모 / denominator**: seeded probe **36개**(10 failure family, 3 source). ablation 4행 모두 같은 36 probe 분모를 공유.
- **주요 수치**:

  | 구성 | detection (탐지) | precision (정밀도) |
  |---|---|---|
  | single-pass draft (gate 없음) | 14% (5/36) [6–29%] | N/A |
  | +gate | 69% (25/36) [53–82%] | N/A |
  | +gate +self-review | 81% (29/36) [65–90%] | N/A |
  | +gate +self-review +adversarial | 92% (33/36) [78–97%] | 74% (42/57 issue) [61–83%] |

  - precision denominator 주의: blinded 60 sampled issue에서 "cannot tell" 3개를 제외해 **57**이 분모다. 74% = **42/57**(60이 아님).
  - `해석:` gate가 가장 큰 단일 상승(14→69%)을 만들고, self-review(+12%p)와 adversarial(+11%p)이 추가 상승을 준다. 마지막 층까지 쌓아도 8%(3/36)는 미탐지로 남는다.
- **caveat(저자)**: probe가 36개, 10 family, 3 source에 한정돼 failure coverage가 제한적이다.
- **논문 주장과의 연결**: fabrication detection이 14%에서 92%로 오른다는 것이 검증 스택 4층의 핵심 정량 근거다.

##### 4. 생성 효율 (비용·token·시간)

- **목적**: full pipeline 한 편 생성에 드는 비용·token·시간과, 검증 층이 얹는 증분 비용.
- **데이터 규모**: 8 topic 기준(증분 측정은 3-topic subset).
- **주요 수치**:
  - full pipeline: 비용 **$8.1 [6.9–9.6]**, token **11.9M [10.2–13.7M]**, wall-clock **3.2h [2.6–3.9h]**, 8 topic.
  - 증분(3-topic subset): gate +8.1M±0.9M tok / +$5.3±0.5; self-review +1.1M±0.2M tok / +$0.6±0.1; adversarial +2.6M±0.4M tok / +$1.6±0.2.
  - single-pass baseline: 0.11M tok, $0.66, 16 min.
  - 이전 시스템: $10–25/run 또는 $2.33–$20–25/attempt(재실행 아님, 공개 값).
  - `해석:` full pipeline은 single-pass보다 약 100배 token·비용이 크고, 증분 비용의 대부분은 gate 층(+8.1M tok)에서 온다. 이전 시스템과의 비교는 pricing·model 가정이 달라 직접 비교로 못 쓴다.
- **논문 주장과의 연결**: 검증 스택의 detection 상승이 상당한 token·비용 증분을 대가로 온다는 trade-off를 정량화.

#### 전체 결과 요약

- **반복적으로 관찰된 패턴**: 검증 층(gate → self-review → adversarial)을 더할수록 fabrication detection이 오르되, 대부분의 token·비용 증분은 gate 층에서 발생한다.
- **가장 중요한 수치**: fabrication detection 14→69→81→92%(36 probe 공통 분모), citation validity 99.5% [98.4–100%](384 refs), figure editability 96.4%(~1,900 요소).
- **baseline 대비 차이**: citation·figure·fabrication 모두에서 single-pass와 이전 자율 시스템보다 높은 값. 단 이전 시스템은 재실행이 아닌 공개 artifact 값이고 소표본(45/64/28 refs)이다.
- **결과 해석 시 주의점**: (1) CI는 paper 단위(n>3)이지 run 단위가 아니다. (2) single-pass paired 비교는 8이 아니라 3 topic이다. (3) precision 분모는 60이 아니라 57이다. (4) 이전 시스템 값은 pricing·model 정규화가 없다. (5) cross-template robustness는 수치 미제공.

---

### Methods

> `검토필요:` core-methods의 표준 template은 확률/통계 구조(model family, likelihood, prior, latent variable, inference)를 요구하나, 이 시스템은 확률 모델이 아니라 결정론적 pipeline과 gate 계약, 그리고 model-based review 스택으로 구성된 systems 논문이다. 따라서 core-methods §147의 규정(확률 방법이 없으면 objective·architecture·model assumption·benchmark design 중심으로 대체)에 따라 "확률/통계학적 구조" 소절을 "아키텍처와 gate 계약" 소절로 대체한다.

#### 이 method가 푸는 문제

- **Formal task**: 입력(연구 topic 또는 측정 데이터)으로부터 검증 가능한 end-to-end 학술 논문(LaTeX 원고, 인용, 그림, 컴파일 산출물)을 생성하되, 결정론적 gate와 model-based review로 fabrication·인용 오류·placeholder 미해결을 걸러 낸다.
- **입력**: research topic(데이터 없음) 또는 측정 데이터(있음). Stage 0에서 둘을 분류한다.
- **출력**: main.tex/pdf, sections/*.tex, refs.bib, figures/, blueprint.json, template.json, claims_map.json, results.facts.json, logs/*.io.md (Table 6, Appendix D).
- **중요한 hidden assumption**: 검증 가능성이 두 층으로 나뉜다는 가정. 규칙으로 판정 가능한 결함(placeholder, 인용 key, 컴파일)은 결정론적 gate가 막고, 판정 불가능한 결함(논증 충분성, 섹션 정합)은 model-based review에 맡긴다. 후자는 model이 판정하므로 audit이 필요하다.

#### 아키텍처와 gate 계약 (확률/통계 구조 대체)

- **13 composable skill을 8 stage로 조립.** 각 stage는 다음으로 넘어가기 전에 자기 gate를 통과해야 한다.

  | Stage | 작업 | 결정론적 Gate |
  |---|---|---|
  | 0 Input Routing | 입력 분류. Proposal Mode(데이터 없음) vs Data-Aware Mode(데이터 있음) 선택 | Template Gate: venue spec 검증 |
  | 1 Planning | research question, contribution, section 구조, notation, 실험설계 추출 | Blueprint Gate: venue 구조 정합 |
  | 2 Citation | 문헌 검색, DOI/arXiv/metadata 검증, BibTeX 구축 | Citation Gate: malformed·미해결 key·일관성 |
  | 3 Writing | blueprint+bib에 맞춰 LaTeX section 생성 | Manuscript Gate: 미해결 placeholder, mode별 result-integrity |
  | 4 Refinement | 반복 제거, 용어 정합, 논증 개선, 길이 조정 | 이전 gate 전부 재실행 |
  | 5 Review | 다중 isolated review pass, issue 검증 | issue는 특정 구절에 묶이고 3분류 검증 |
  | 6 Figure | method figure(raster→HTML→vector PDF), result figure(데이터에서 plot) | Figure Gate: artifact 존재, 정량 figure는 측정결과 grounding |
  | 7 Assembly | section·bib·figure·template 결합→LaTeX 컴파일 | Compilation Gate: 인용·교차참조 해소된 컴파일 |
  | 8 Experiment(조건부) | 증거 gap 식별·실행·provenance 검증·claim 수정 | evidence integrity. 실행불가는 결과 미기재 |

- **Gate 실행 semantics(핵심)**: 각 gate는 결정론적 검사다. **fatal violation은 실행을 중단시키고, warning은 기록하되 진행을 허용한다.** 이 비대칭이 gate 층의 enforcement 계약이다.
- **Manuscript Gate는 mode-의존**: Proposal Mode는 미관측 실증 결과를 거부하고, Data-Aware Mode는 공급 데이터가 뒷받침하지 않는 정량 진술을 플래그한다. 두 모드를 하나로 뭉뚱그리지 않는다.
- **저자 명시 한계(gate 자체)**: "Deterministic checks cannot determine whether an argument is sufficiently supported, whether different sections remain conceptually consistent." 결정론적 gate가 판정할 수 없는 영역이 있어 아래 model-based review가 필요하다.

#### 핵심 method insight

- **기존 방법의 한계**: 자율 에이전트 계열은 별도 orchestration 계층(독립 플랫폼)을 세워야 하고, single-pass 생성은 검증이 전혀 없다.
- **이 논문이 바꾼 가정**: 논문 생성을 독립 플랫폼이 아니라 기존 coding assistant의 재사용 skill 조합으로 구현할 수 있고, 검증을 "결정론적으로 판정 가능한 것"과 "model이 판정해야 하는 것"으로 분리해 각각 gate와 review로 처리한다.
- **새로 추가한 구조**: 4층 검증 스택(결정론적 gate, self-review, adversarial review, preregistration), Claim Admission Protocol, Self-Refutation loop bounding.
- **이 변화가 중요한 이유**: fabrication detection이 gate 없는 14%에서 4층까지 쌓아 92%로 오른 것이 이 분리 설계의 정량 근거다.

#### 검증 스택 (4층)

1. **결정론적 integrity gate** (앞의 Stage 표): Template/Blueprint/Citation/Manuscript/Figure/Compilation gate. 규칙으로 판정 가능한 결함만 막는다.

2. **Self-Review** (model-based, local): 편집 직후 실행. 수정 내용을 주변 원고와 대조해 terminology drift, redundancy, local inconsistency를 수리한다.

3. **Adversarial Review** (model-based, manuscript-level): 다중 isolated pass가 상보적 측면(theoretical soundness, experimental design, systems validity)을 검토한다. **3-Way Validation Protocol**(§5.2 `검토필요:`)로 각 issue를 세 관문에 건다. (1) 문제가 원고에 실제 존재하는가, (2) 다른 곳에서 이미 다뤄졌는가, (3) 명시 scope 안인가. 하나라도 실패하면 폐기하고, 생존 issue만 수정에 회부한다.

4. **Preregistration** (experiment planning): 실행 전 planning stage가 dataset, baseline, metric, ablation, result table 구조를 명시한다. "The table structure is fixed in advance, while numerical cells remain empty until the corresponding experiments are completed." planning과 reporting을 분리하는 lightweight preregistration이다.

##### Claim Admission Protocol (Appendix C, 5라벨)

실험 후 각 claim에 5개 라벨 중 하나를 붙이고 그에 맞춰 조치한다.

| 라벨 | 조치 |
|---|---|
| supported | 근거에 맞춰 유지 |
| partially-supported | 근거에 맞춰 좁힘 |
| unsupported | 추가 실험, 약화, 또는 삭제 |
| contradicted | 삭제하거나 한계로 강등 |
| needs-confirmation | 저자 확인. 미해결로 남길 수 없음 |

- 수정은 abstract, intro, results, conclusion의 모든 occurrence로 전파한다.

##### Self-Refutation Loop bounding (7-cap → failure report)

- **실패모드**: 시스템이 자기 결과가 원 가설을 지지하지 않는다고 반복 결론내면서 같은 방향으로 계속 수정하는 무한 loop.
- **처방**: experiment–critique–revision cycle을 **7회로 bound**한다. 한계 후에도 미지지면 trajectory를 종료하고 **failure report**(원 아이디어, 시도한 방법, 관측 결과, 불충분한 사유)를 기록한다. 억지 성공을 만들지 않고, 이후 새 아이디어로 전체 pipeline을 재실행한다.

#### 이전 방법과의 차이

- **Baseline**: AI Scientist(Lu 2024), AI Scientist-v2(Yamada 2025), Agent Laboratory(Schmidgall 2025)는 공개 논문 audit. single-pass LLM은 같은 Claude backbone에 gate/review를 뺀 in-house 구현. human preprint.
- **공통점**: end-to-end 논문 생성을 목표로 한다는 점.
- **차이점**: 이 논문은 별도 orchestration 계층 없이 coding assistant의 skill 조합으로 구현하고, 결정론적 gate와 model-based review를 명시적 검증 스택으로 얹는다.
- **비교의 한계(저자)**: 이전 시스템은 재실행 없이 공개 artifact 값만 썼고 model backbone·pricing을 정규화하지 않았다. 측정 못 한 값은 추정하지 않고 not reported로 표기했다.

#### 효과가 Results에서 나타난 방식

- **Benchmark**: 외부 선정 8 topic(사전등록), single-pass paired 3 topic, human preprint 8편.
- **핵심 ablation 근거**: fabrication detection이 single-pass 14%(5/36) → +gate 69%(25/36) → +self-review 81%(29/36) → +adversarial 92%(33/36)로 오른다. 각 검증 층이 detection에 기여함을 보인다.
- **정성적 효과**: citation validity 99.5%, figure editability 96.4%가 gate·Figure 단계 산물의 효과로 제시된다.

#### Method 관점의 한계 (저자 caveat)

- **claim-level 판정이 model-based**: "determining whether a particular piece of evidence semantically supports a claim is currently performed by the model." 저자가 auditing이 필요한 약점으로 인정한다.
- **preregistration이 non-binding**: lightweight이고 강제력이 없으며, model이 여전히 사후 claim을 판정한다.
- **7-iteration bound의 근거 부재**: 명시적 정당화 없이 선택됐고 도메인별로 다를 수 있다.
- **Self-Refutation의 잔여 위험**: "some trajectories may fail in the same way." coherent claim을 낸 trajectory만 최종 원고가 되므로, 거부된 trajectory가 전부 진짜 불가능이었다는 보증은 없다.
- **실험 feasibility**: 자원이 없으면 missing dependency를 기록하고 결과를 미기재한다. 자원 gap을 자동 해결하지 않는다.
- **model/tool 분리 불완전**: adversarial review는 여전히 3분류 수동 검증이 필요하다.
- **figure 재구성 신뢰성**: 소수 correction round로 대개 복원하되, 불가하면 raster fallback으로 떨어진다.
- **구현 의존성**: 시스템이 Claude Code backend와 Claude model family를 요구하며, 타 구현은 없다.

#### 재현성 메모

- GitHub(예고): https://github.com/Spark-To-Paper-Skills/spark-to-paper-skills. corresponding: wangwenhao@vastilab.com.
- venue별 동작을 hard-code가 아니라 JSON spec으로 둔다(Appendix D). case study 도메인: clinical risk screening, PM2.5 forecasting. figure count는 self-reported(존재 증거이지 benchmark가 아님).
- 감사 corpus: fabrication probe 36개, review precision 60 issue(57 usable), citation audit 384 ref(human 320).
