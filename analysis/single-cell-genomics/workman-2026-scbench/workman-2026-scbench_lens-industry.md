# Lens — Industry — scBench

## 1. Categorization
> paper-info.yaml의 categorization 블록과 동기화.

### Domain (자동 추출, 검토 표시)
- single-cell genomics (scRNA-seq)
- AI/LLM agents
- bioinformatics benchmarking

### Use case (vocabulary 6개 중)
- `internal-tool-evaluation` (vocabulary 확장 항목) — scRNA-seq 분석을 LLM agent에 위임할 때 어느 model·task·platform이 실패하는지의 정량 근거. 내부 파이프라인의 agent 선정·검증 기준으로 활용.
- `methodology-reference` — deterministic grader + evaluation-type tiering + linter + tolerance calibration 설계를, 우리 자체 분석 자동화의 *평가 layer* reference로 차용 가능.
- `academic-citation` — scRNA-seq agent의 현재 성능 상한·platform 의존성 수치를 본인 논문·제안서에 인용.

### Importance (1개 종합 등급)
- Level: 상
- Perspective (1문장): LLM agent를 scRNA-seq 분석에 실제 적용할 때 어느 task·platform에서 실패하는지 처음으로 정량화한 benchmark이며, 우리가 분석 자동화를 도입할 때의 model 선정·검증·human-in-the-loop 설계에 직접 참조 가능.

## 2. 산업·규제·임상 리스크 (QA / RA)

### 2.1 데이터·통계적 리스크
- **표본 불균형**: task category가 매우 불균형(Cell Typing 118 vs Trajectory 7). 우리가 trajectory/velocity 분석을 agent에 맡길 때의 신뢰도는 이 benchmark로 거의 알 수 없음(`미제공:` trajectory model별 분해 없음).
- **단일 harness·3 replicate**: harness ablation 없음 → model 정확도가 model 능력인지 harness×model 상호작용인지 분리되지 않음. 운영 model 선정 시 *우리 harness에서 재측정* 필요.
- **grading 민감도**: tolerance sensitivity analysis 부재. ranking이 grader 설계에 얼마나 robust한지 검증 안 됨.
- **수치의 시점성**: model lineup(Opus 4.6/4.5, GPT-5.2/5.1, Grok-4.1/4, Gemini 2.5 Pro)과 cost·latency 수치는 빠르게 노후화. 절대 정확도보다 *상대 패턴*(task 난이도 순서, platform swing)이 더 오래 유효.

### 2.2 임상·기술적 제약
- **임상 직접 적용성 낮음**: 이 자료는 임상 진단 도구가 아니라 연구용 분석 agent의 평가 benchmark. IVD/LDT/SaMD 같은 임상 pathway와 직접 연결 안 됨.
- **계산 자원**: agent 실행은 frontier model API + isolated workspace 의존. cost/latency는 Figure 3에 정량화(예: Opus 4.6 latency 303s/eval). 대량 평가 시 API 비용 누적.
- **데이터 의존성**: eval은 AnnData `.h5ad` 기반. 우리 HSPC multiome 데이터에 그대로 쓰려면 별도 변환·task 정의 필요.

### 2.3 규제·QA·RA 관점
- **regulatory pathway**: `미제공:` 본 자료는 analytical/clinical validation(정밀도, sensitivity/specificity 등) 데이터를 제시하지 않는다 — 임상 검증 자료가 아니라 연구 능력 측정 benchmark.
- **audit 관점 시사**: 오히려 *deterministic grading + linter + tolerance calibration* 구조는, 우리가 분석 자동화에 audit-ready 검증 layer를 붙일 때의 설계 참고가 된다. agent 출력의 pass/fail을 재현적으로 기록하는 틀.
- **human oversight 권고**: 저자 결론(§3)이 "중간 결과의 엄격한 검증과 사람 감독 없이는 자율 신뢰 불가"라고 명시 → 우리가 agent를 도입할 때 SOP에 human-in-the-loop를 명문화할 근거.

### 2.4 권위·신뢰 가중치
- `1차 출처:` 원저자(LatchBio)의 1차 benchmark 결과.
- **Peer review 여부**: preprint, "Under review" — peer-reviewed 아님. 가중치 하향.
- **저자 이해상충(COI)**: 저자 전원 LatchBio 소속. LatchBio는 bioinformatics 분석 플랫폼 사업체로 추정되며, 자사 agent/플랫폼 포지셔닝과 이해관계가 있을 수 있음(`해석:`). benchmark 자체는 공개 model을 평가하므로 직접적 자사 우대는 본문에서 드러나지 않으나, framing(agent로 분석 자동화의 필요성)은 사업 방향과 align.
- **Funding source**: `미제공:` 본문에 funding statement 없음.

## 3. BD value & 상용화 가능성

### 3.1 BD-opportunity (외부 자산 정찰)
- **LatchBio 관찰 가치**: scRNA-seq + spatial 두 benchmark(scBench, SpatialBench)를 보유 → 분석 agent 평가 영역에서 선점 포지션. 우리가 분석 자동화 제품/내부 도구를 고려한다면 경쟁사/협력 후보로 모니터링 가치.
- **공개 자산 (확인 완료, 2026-06-13 web)**: GitHub `latchbio/scbench` **public, license Apache-2.0**(상용·차용 친화). framework/graders/linter/agent harness 공개, `agent_function` pluggable interface 제공. → deterministic grader 프레임 차용은 license상 자유.
  - `검토필요:` **수치 불일치** — 논문 §5는 "394 evals, 30 canonical public"인데 *현재 repo README는 "195 problems, 6 canonical public"*. preprint(arXiv 2602.09063 v1) 이후 repo가 갱신된 것으로 보임(`해석:`). BD/차용 판단 시 *repo 현재 상태*(195/6, Apache-2.0)를 기준으로.

### 3.2 Commercialization-candidate (자체 제품화)
- 직접 제품화 후보로는 낮음. 이 자료 자체는 평가 도구이지 우리가 팔 Dx/assay/therapeutic이 아님.
- 단 **SW 관점 간접 가치**: deterministic grader 프레임을 우리 분석 SW의 *내부 회귀 테스트/QA harness*로 자체 구현하는 것은 가능(IP 자유도 높음 — 개념은 공개).

### 3.3 우리 파이프라인과의 fit
- **Dataset 호환**: 부분. 우리 HSPC 10x Multiome(GSE209878)은 Chromium platform → scBench에 Chromium eval 60개 포함되어 *간접 참조* 가능. 단 scBench는 scRNA-seq 단독이고 우리는 multiome(ATAC+RNA)이라 task 정의가 그대로 맞지는 않음.
- **팀 역량**: 우리 팀이 grader/linter 컨셉을 자체 구현할 역량은 충분(코드 중심 workstream).
- **전략 align**: 우리 핵심 주제(chromatin-RNA lag)와 *직접* align은 약함. agent 분석 자동화를 도입할 경우의 *운영 의사결정*에 align.

### 3.4 후속 BD·제품 액션 후보
- ~~GitHub repo 공개 여부·license 확인~~ **(완료 2026-06-13)**: public, Apache-2.0 → grader 프레임 차용 가능. (repo 현재 195 problems / 6 canonical, 논문은 394/30 — 갱신됨.)
- 내부 agent 평가 mini-harness PoC
  - 누가: 본인 + 하네스 담당(지용기)
  - 언제: 다음 분기
  - 자원: 우리 Chromium/multiome 데이터 1~2개로 deterministic grader 컨셉 적용
  - 성공 기준: 우리 데이터 단계(QC/normalization)에서 agent pass/fail을 재현적으로 채점하는 PoC 동작.

## 4. 전문가 코멘트

### 4.1 종합 등급
- Level: 상
- Perspective: LLM agent의 scRNA-seq 분석 능력을 task·platform 두 축으로 처음 정량화 — 분석 자동화 도입 의사결정의 1차 근거.
- 등급 근거:
  - frontier agent의 현재 상한이 52.8%로 *자율 신뢰 불가* 영역임을 정량 확인(§2.2) → 우리 SOP에 human-in-the-loop를 넣을 직접 근거.
  - platform 효과(32.7 pp)가 model 효과(23.6 pp)를 초과(§2.4) → 우리 데이터 platform(Chromium)에서 별도 재측정 필요성의 근거.
  - deterministic grader + evaluation-type tiering + linter + tolerance calibration이라는 *재사용 가능한 평가 설계*(§4.1–4.4)를 제공.
  - 단 우리 핵심 주제(chromatin-lag/velocity)와 직접 관련은 낮고, trajectory task는 7개로 빈약.

### 4.2 활용 우선순위
- 지금: (GitHub 확인 완료 — public/Apache-2.0) 평가 설계(grader/linter/tolerance) 메모 + 차용 PoC 범위 스코핑.
- 다음 분기: 내부 agent 평가 mini-harness PoC(우리 데이터).
- 장기: 분석 자동화 제품/내부 도구 도입 시 model 선정·검증 기준 문서의 reference.

### 4.3 발표·미팅에서 들이밀 시점
- 사내 R&D 리뷰: "분석을 LLM agent에 위임할 때 어디까지 믿을 수 있는가"를 논의할 때 1차 근거 자료.
- 본인 논문/제안서 introduction: scRNA-seq agent의 한계 정량화 인용.

### 4.4 추가 탐색 필요 영역
- ~~질문: latchbio/scbench repo가 실제 public이고 license가 무엇인지?~~ **답: public, Apache-2.0 → grader 컨셉 차용 가능.**
- 질문: LatchBio의 사업 모델(분석 플랫폼/agent 제품)은? COI 가중치와 BD 관찰 우선순위에 반영.
- 질문: multiome(ATAC+RNA) 대상 agent benchmark가 있는가? 없으면 우리 데이터가 차별적 자산이 될 수 있음.
