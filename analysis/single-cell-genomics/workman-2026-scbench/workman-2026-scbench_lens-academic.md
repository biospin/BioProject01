# Lens — Academic — scBench

## Limitations

### 저자가 명시한 한계
- **판단의 이산화(discretization)**: deterministic grader는 검증 가능한 평가를 가능케 하지만, 과학적 판단을 *자동 채점 가능한 조각*으로 강제 이산화한다. 미묘한 판단이 단일 pass/fail로 환원되며 그 과정의 정보 손실은 측정되지 않는다 (Discussion §3, 마지막 문단).
- **단일 워크플로우 단계 snapshot**: 각 eval은 한 분석 단계의 snapshot만 본다. 오류가 누적되고 결과를 재검토하는 *long-horizon iteration*은 포착하지 못한다 (Discussion §3). 실제 분석에서 errors compound하는 부분이 평가 밖에 있다.
- **개선 여지**: 최고 model도 52.8%로 substantial room for progress가 남았다고 명시 (Discussion §3).
- **platform swing의 원인 추정**: MissionBio collapse·Illumina 강세를 unbalanced training data와 memorized technique의 fragility로 해석하나, 이는 저자도 "likely reflect"로 표현한 *추정*이다 (§2.4, §3).

### 분석자가 판단한 한계
- **부족한 점 — Trajectory/observational의 분해 부재**: Trajectory는 7 eval(전체의 ~1.8%)뿐이고 Table 3·Figure 4의 task별 분해에 포함되지 않는다. observational evaluation type의 model별 성능도 별도로 보고되지 않는다.
  - 왜 중요한가: 우리 팀 주제(chromatin-RNA lag, velocity)에 가장 가까운 task가 trajectory다. 그런데 정확히 그 부분의 표본이 가장 얇고 분해가 없어, "agent가 trajectory/velocity 분석을 신뢰성 있게 하는가"를 이 benchmark로 답할 수 없다.
  - 어떤 증거가 부족한가: trajectory eval 수 확대 + model별 정확도 분해.
- **부족한 점 — grading 설계의 외적 타당성**: tolerance를 "여러 valid method를 돌려 acceptable range를 잡는" 방식으로 calibrate하는데, 그 method pool과 default parameter 선택 자체가 정답 분포를 정의한다. pool이 좁으면 정답이 인위적으로 좁아진다.
  - 왜 중요한가: pass/fail이 grader 설계에 민감하면 model ranking도 그에 의존할 수 있다.
  - 어떤 증거가 부족한가: tolerance 폭에 대한 sensitivity analysis(tolerance를 흔들었을 때 ranking이 보존되는가).
- **부족한 점 — single replicate count·single harness**: 3 replicate, mini-SWE-agent harness 하나로만 측정. harness(prompting, tool 구성, retry 정책)가 model별로 다른 영향을 줄 수 있는데 harness ablation이 없다.
  - 왜 중요한가: "model 능력"과 "harness×model 상호작용"이 분리되지 않는다. Opus의 상위권이 model 자체인지 Anthropic 친화적 harness인지 구분 불가.

### 설명이 매끄럽지 않은 지점
- **연결이 약한 주장**: "scRNA-seq가 spatial보다 tractable한 이유 = public dataset·Scanpy 문서가 더 많기 때문"이라는 인과 해석.
  - 현재 논문이 제시한 근거: 정확도 격차(52.8 vs 38.4)와 정성적 설명(QC task에서 차이가 가장 큼).
  - 더 필요해 보이는 근거: training corpus 내 platform/assay 언급 빈도의 정량 proxy(예: 공개 문서 hit count)와 정확도의 상관. 현재는 association을 인과처럼 서술.
- **연결이 약한 주장**: "model 차이가 judgment-heavy 단계에 집중된다"는 결론.
  - 현재 근거: DE·cell typing에서 spread가 큼.
  - 더 필요해 보이는 근거: 어떤 종류의 오류(잘못된 test 선택 vs marker gene 누락 vs 통계 해석 오류)가 차이를 만드는지의 error taxonomy. 현재는 단계 라벨까지만.
- **grading 로직 가시성 (해소됨)**: 5개 grader family가 §4.5에 모두 명시됨 — $\mathrm{NumericTolerance}$ / $\mathrm{MultipleChoice}$ / $\mathrm{MarkerGenePrecisionRecall}$ / $\mathrm{LabelSetJaccard}$ / $\mathrm{DistributionComparison}$ (정식 spec Appendix C). 채점 로직은 auditable하다. 남는 academic 한계는 *tolerance/threshold 민감도 분석 부재*(위 grading robustness 항목)이지 grader 가시성이 아니다. (초기 분석의 "PDF가 §4.4에서 절단" 서술은 page count 오판에 따른 오류 — 실제 PDF는 17쪽 완전본.)

### 정리되지 않은 질문
- 질문: tolerance를 흔들면 model ranking이 보존되는가? (grading robustness)
- 질문: 같은 model을 다른 harness(예: 다른 prompting/tool set)로 돌리면 platform swing이 줄어드는가? — swing이 model 한계인지 harness 한계인지 가른다.
- 질문: error mode 분포는? hallucination인가, wrong-method-selection인가, format 위반인가? 우리 파이프라인에 agent를 넣을 때 어디에 guardrail을 둘지 결정한다.

## Citation 후보 (본인 논문·제안서·학회 발표용)

> `paper-info.yaml`에 `academic-citation` use_case 있음 → 인용 후보 정리.

### 인용 가능 문장
- §Abstract: "accuracy ranges from 29–53%, with strong model-task and model-platform interactions"
  - 사용 시나리오: 본인 introduction/discussion에서 *LLM agent가 scRNA-seq 분석에 아직 신뢰성이 부족하다*는 근거로.
  - BibTeX key: `@workman2026scbench`
- §3 (Discussion): "today's agents can accelerate routine analysis but cannot yet be trusted to autonomously answer scientific questions without stringent verification of intermediate results and human oversight"
  - 사용 시나리오: 자동화 파이프라인 제안서에서 *human-in-the-loop가 필요한 이유*를 정당화할 때.
  - BibTeX key: `@workman2026scbench`
- §2.4: "Platform choice affects accuracy as much as model choice" (32.7 pp gap > 23.6 pp model spread)
  - 사용 시나리오: agent 평가는 model뿐 아니라 *데이터 출처(platform)*를 stratify해야 한다는 방법론적 주장의 근거.
  - BibTeX key: `@workman2026scbench`

### 인용 가능 수치
- best model accuracy 52.8% (95% CI 48.3–57.2), worst 29.2% (§2.2, Table 2)
  - 사용 시나리오: scRNA-seq agent 성능의 현재 상한선 baseline 인용.
  - BibTeX key: `@workman2026scbench`
- task 난이도: Normalization 70.4% (easiest) vs Differential Expression 27.0% (hardest), cross-model mean (§2.3)
  - 사용 시나리오: "어느 분석 단계가 agent에게 어려운가"를 단계별로 언급할 때.
  - BibTeX key: `@workman2026scbench`
- platform 격차: CSGenetics 59.1% vs MissionBio 26.4% cross-model mean, 32.7 pp (§2.4)
  - 사용 시나리오: 데이터 출처 의존성의 정량 근거.
  - BibTeX key: `@workman2026scbench`

### 인용 가능 Figure/Table
- Table 5 (§2.5) — scBench vs SpatialBench 요약 비교
  - single-cell의 두 주요 assay에서 agent 성능을 한 표로 대조.
  - 사용 시나리오: 본인 review/제안서에서 "agent benchmark 현황"을 한 표로 인용.
  - BibTeX key: `@workman2026scbench`
- Figure 3 (§Results) — accuracy vs cost/latency Pareto
  - 정확도-비용 trade-off 도식.
  - 사용 시나리오: 운영 model 선정 논의에서 Pareto 개념 재현.
  - BibTeX key: `@workman2026scbench`

## Final Takeaways
- **이 논문의 가장 큰 의미**: scRNA-seq 분석을 *데이터와 상호작용해야 답할 수 있고 deterministic하게 채점 가능한* 단위로 환원해, LLM agent의 domain 능력을 처음으로 platform·task 두 축으로 stratify해 정량화했다. "general coding 능력 ≠ domain 분석 능력"을 데이터로 보였다.
- **다음 논문으로 이어질 아이디어**:
  - (1) error taxonomy 추가 — pass/fail을 넘어 *실패 유형*을 라벨링해 agent guardrail 설계 근거를 만든다.
  - (2) harness ablation — 같은 model을 여러 harness로 돌려 model 능력과 harness 효과를 분리.
  - (3) long-horizon eval — 단일 step이 아니라 QC→…→DE 전 파이프라인을 이어 달리게 해 error compounding을 측정.
  - (4) trajectory/velocity task 확장 — 우리 주제(chromatin-lag)와 직결되는 task를 7개에서 의미 있는 규모로 늘려 분해 분석.
- **설명을 더 매끄럽게 만들 방법**: training-corpus 언급 빈도 proxy를 측정해 "tractability ∝ 문서량" 주장을 association→정량 상관으로 격상.
- **우선순위가 높은 후속 실험 / 분석**: tolerance sensitivity analysis(grading robustness)와 error taxonomy. 둘 다 benchmark 결론의 신뢰도를 직접 강화하고, 우리가 agent를 도입할 때 가장 알고 싶은 것이다.
