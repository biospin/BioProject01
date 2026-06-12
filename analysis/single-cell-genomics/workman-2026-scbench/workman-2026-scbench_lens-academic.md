# Lens — Academic: workman-2026-scbench

**소스**: `workman-2026-scbench_core.md` + `sources/workman-2026-scbench.pdf`

---

## Limitations

### 저자가 명시한 한계

- **Single-step snapshot**: 각 evaluation은 단일 workflow step을 스냅샷한다. 오류가 누적되고 threshold를 재검토하는 long-horizon iteration을 캡처하지 못한다 (Discussion §3).
- **Deterministic grader의 과학적 판단 이산화**: 연속적인 과학적 판단을 자동 채점 가능한 덩어리로 쪼개면 분야 전문가가 수용할 range를 놓칠 수 있다 (Discussion §3).
- **Full 394-eval suite 비공개**: training contamination 방지를 위해 30개 canonical evaluation만 공개. 외부 연구자가 동일 benchmark로 자신의 모델을 평가하려면 공개 subset만 가능 (Data Availability §5).
- **SpatialBench와 공유하는 한계**: 두 benchmark 모두 spatial 또는 scRNA-seq 전용. 멀티모달(multi-omic joint analysis) 평가는 미존재 (Discussion §3).

### 분석자가 발견한 추가 한계

**방법론적**

- **Trajectory analysis underrepresentation**: 7개 evaluation만 있어 95% CI가 극도로 넓다. Illumina 단일 platform 의존. RNA velocity, pseudotime 등 trajectory 분석의 핵심 단계를 대표하지 못한다.
  - 질문: Trajectory evaluation에서 7개 중 몇 개나 pass@K ≥ 1인가? 모델이 모두 0%에 가깝다면 benchmark 신호 자체가 약함.

- **ParseBio QC 공백**: QC evaluation이 없어 cross-platform 공정 비교에 구조적 불균형 존재. ParseBio 성능이 다른 플랫폼과 다른 이유가 QC 구성 부재 때문인지 모델 실패 때문인지 분리 불가.

- **Evaluation type 분포 미공개**: Scientific / Procedural / Observational 비율이 Table에 없다. 이 분포가 다르면 aggregate accuracy 해석이 달라진다. Procedural이 많으면 더 높은 평균이 나오는 구조적 편향이 발생 (§4.3).
  - 미제공: Evaluation type별 breakdown이 paper·appendix에 없음.

- **3 replicates의 통계 충분성**: K=3은 high-variance task(Scientific evaluations)에서 추정 정밀도가 낮다. per-evaluation mean이 {0, 1/3, 2/3, 1}의 4개 값만 취하므로 micro-level 추정은 거칠다.

**생물학적 타당성**

- **Tissue-platform confounding**: MissionBio는 hematopoietic tissue(CCUS), Illumina는 DRG 등 tissue와 platform이 완전히 confounded. Platform 어려움이 실제로 platform 고유한가, tissue 특수성 때문인가를 분리할 수 없다.
  - 해석: MissionBio의 낮은 성능은 비표준 데이터 구조 + DNA/protein multiome + 희귀 임상 샘플(CCUS) 세 가지가 동시에 기여할 수 있다.

- **Adversarial evaluation의 소수성**: Illumina adversarial brain-signature MCQ처럼 biological implausibility를 테스트하는 evaluation이 몇 개인지 명시되지 않음. 이런 유형이 많으면 모델이 memorization으로 통과하지 못하는 실제 생물학 추론 능력을 더 정밀하게 측정할 수 있다.

**범용성**

- **Harness 의존성**: mini-SWE-agent harness에서 잘 동작하는 모델이 다른 harness(Jupyter notebook, tool-calling API 등)에서도 동일 성능을 보일지 미검증. 해석: LLM 능력 benchmark인지 harness-LLM 조합 benchmark인지 구분이 어렵다.

- **Multi-omic 미지원**: MissionBio Tapestri (DNA+protein+RNA 통합)처럼 진정한 multi-omic 분석은 현재 framework에서 부분만 커버된다.

---

## 후속 연구 아이디어

1. **Long-horizon evaluation 도입**: 여러 단계 연속 실행 — QC threshold 결정 → normalization → clustering → annotation — 에서 초기 오류가 하류에 미치는 누적 영향을 측정하는 multi-step evaluation 설계.

2. **Platform-tissue deconfounding**: 동일 tissue를 여러 platform으로 프로파일링한 paired 데이터로 platform effect를 tissue effect와 분리. 기존 공개 cross-platform benchmark dataset 활용 가능.

3. **Trajectory evaluation 확장**: scVelo, Monocle, Palantir 등 다양한 trajectory 방법을 포함한 evaluation을 현재 7개에서 최소 50+개로 확대. RNA velocity prediction의 biological coherence를 grader로 측정하는 방법 개발 필요.

4. **Evaluation type-stratified leaderboard**: Scientific / Procedural / Observational별 분리 성능 공개. 이를 통해 모델이 "코드만 잘 쓰는지" vs. "과학적 판단을 잘 내리는지" 분리 측정 가능.

5. **Harness ablation**: 동일 모델을 mini-SWE-agent, Jupyter agent, tool-calling API, plain code interpreter 등 여러 harness에서 실행해 harness 선택의 성능 기여 정량화.

6. **Multi-omic benchmark 확장**: scBench + SpatialBench에 이어 CITE-seq(protein+RNA), multiome(ATAC+RNA), Tapestri(DNA+protein) 전용 evaluation 추가. 세 modality를 통합하는 joint benchmark로 발전 가능.

7. **Agent self-calibration 연구**: 모델이 자신이 풀 수 없는 evaluation을 인식하고 "모르겠다"고 답하는 능력 측정. 현재는 wrong answer와 "모름 → 0점"이 구분되지 않음.

---

## Citation 후보 (본인 논문·제안서·학회 발표용)

### 인용 가능 문장

- §Introduction: "agents for scRNA-seq remain both unreliable and underpowered, prone to scientific inaccuracies and hallucinations, and frequently fail to complete domain-specific analysis steps that depend on messy, real-world datasets."
  - 사용 시나리오: 본인의 scRNA-seq agent 논문 intro에서 *현재 LLM agent의 한계*를 짚을 때
  - BibTeX key: `@workman2026scbench`

- §Discussion: "today's agents can accelerate routine analysis but cannot yet be trusted to autonomously answer scientific questions without stringent verification of intermediate results and human oversight."
  - 사용 시나리오: human-in-the-loop scRNA-seq 파이프라인 제안서에서 *automated vs. semi-automated* 프레임을 논거할 때
  - BibTeX key: `@workman2026scbench`

- §2.4: "Platform choice affects accuracy as much as model choice… a 32.7 pp gap that exceeds the 23.6 pp spread between best and worst models."
  - 사용 시나리오: platform-aware agent 설계 논문에서 *platform effect의 severity*를 수치로 인용
  - BibTeX key: `@workman2026scbench`

- §Discussion: "reliable agents will require platform-aware context, assay-specific tooling, and self-calibration heuristics rather than one-size-fits-all reasoning."
  - 사용 시나리오: RAG 기반 scRNA-seq agent 제안서에서 *platform-aware context 필요성* 논거
  - BibTeX key: `@workman2026scbench`

### 인용 가능 수치

- **52.8%** — Claude Opus 4.6, scBench 394 evaluations, 95% CI (48.3, 57.2) (Table 2)
  - 사용 시나리오: "현재 SOTA agent의 scRNA-seq 정확도"를 baseline으로 제시할 때
  - BibTeX key: `@workman2026scbench`

- **70.4%** (normalization) vs **27.0%** (differential expression) — task category cross-model mean (§2.3)
  - 사용 시나리오: task 난이도 계층 구조를 설명하고 DE·cell typing에 집중해야 하는 이유 논거
  - BibTeX key: `@workman2026scbench`

- **32.7 pp** platform gap (CSGenetics 59.1% vs MissionBio 26.4%) > 23.6 pp model gap (§2.4)
  - 사용 시나리오: platform-aware benchmarking 필요성, platform diversity의 중요성 논거
  - BibTeX key: `@workman2026scbench`

- **scBench 52.8% vs SpatialBench 38.4%** (top model) — scRNA-seq이 spatial보다 tractable (§2.5, Table 5)
  - 사용 시나리오: spatial transcriptomics agent 논문에서 *modality별 LLM difficulty* 비교 인용
  - BibTeX key: `@workman2026scbench`

### 인용 가능 Figure/Table

- **Figure 2** (p.3) — 8개 모델 aggregate accuracy 바 차트 + 95% CI
  - 무엇을 보여주는지: 현재 frontier LLM의 scRNA-seq 분석 능력 스냅샷
  - 사용 시나리오: 본인 review/survey에서 LLM-scRNA-seq 성능 현황 도식으로 재현
  - BibTeX key: `@workman2026scbench`

- **Table 3** (p.4) — task category별 모델 성능 matrix
  - 무엇을 보여주는지: task별 난이도와 모델 간 discriminability 동시 조망
  - 사용 시나리오: 특정 task(DE, cell typing)에 집중하는 agent 연구 동기 부분에서 인용
  - BibTeX key: `@workman2026scbench`

- **Table 4** (p.5) — platform별 모델 성능 matrix (ranking inversion 포함)
  - 무엇을 보여주는지: platform이 모델 선택보다 더 큰 성능 변동을 유발함
  - 사용 시나리오: platform-specific fine-tuning 또는 RAG 제안서의 motivation 그림으로 사용
  - BibTeX key: `@workman2026scbench`
