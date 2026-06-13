# Methodology Brief — workman-2026-scbench

## 한 줄 결론 (모든 독자)
- Citation: `@workman2026scbench`  |  Importance: 상 (LLM agent의 scRNA-seq 분석 능력을 task·platform 두 축으로 처음 정량화 — 분석 자동화 도입 의사결정의 1차 근거)
- 한 문장 결론: scRNA-seq 분석을 *검증 가능한 단위 문제 + deterministic grader*로 환원한 agent benchmark(394 eval, 6 platform, 7 task). 최고 model 52.8%로 아직 자율 신뢰 불가 — 우리는 결과보다 *평가 설계*를 차용하고, 분석 자동화 SOP에 human-in-the-loop 근거로 인용한다.

## 재현 가능성 체크 (재현 담당자)
- 데이터 접근: AnnData `.h5ad` snapshot, runtime에 isolated workspace로 다운로드. 개별 dataset accession은 본문 미명시 (`미제공:`).
- 코드 공개: GitHub `latchbio/scbench` (paper-info.yaml `url-only`; framework/graders/linter/harness, "30 canonical evals public"). `검토필요:` PDF 본문에서 직접 확인 안 됨 — repo 접근·license 별도 확인 필요.
- 자원 요구: frontier model API + agent harness(mini-SWE-agent). per-eval latency ~94–303s (Table 2). GPU 불요, API 비용 의존.
- 핵심 의존성: AnnData/`.h5ad`(Wolf et al. 2018, Scanpy 생태계), mini-SWE-agent harness, deterministic grader 5종(본문 확인 2종: $\mathrm{NumericTolerance}$, $\mathrm{DistributionComparison}$).
- 자세히 → [workman-2026-scbench_core.md](workman-2026-scbench_core.md) §Methods, [sources/workman-2026-scbench.pdf](sources/workman-2026-scbench.pdf) §4

## 우리 적용 가능성 (의사결정자)
- Dataset 호환: 부분. scBench는 scRNA-seq 단독, 우리는 HSPC 10x Multiome(Chromium, ATAC+RNA). Chromium eval 60개로 간접 참조 가능하나 multiome task는 그대로 매핑 안 됨.
- 자원 가능성: 평가 *설계*(grader/linter/tolerance) 자체 구현은 우리 팀 역량으로 가능. benchmark 재실행은 API 비용·harness 구성 필요.
- 비용·시간 추정: grader 컨셉 PoC(우리 데이터 QC/normalization 단계) ~다음 분기, 수 주 규모.
- ROI 한 줄: 결과 수치보다 *deterministic grading + evaluation-type tiering* 설계가 우리 분석 자동화의 audit-ready 평가 layer로 재사용 가치 높음.
- 자세히 → [workman-2026-scbench_lens-industry.md](workman-2026-scbench_lens-industry.md) §3

## 본인 재회고 (본인)
- 질문: latchbio/scbench repo 실제 public·license? grader 컨셉 차용 가능 여부 좌우.
- 질문: trajectory/velocity task가 7개뿐이라 우리 chromatin-lag 주제에 직접 쓸 신호가 없음 — multiome agent benchmark가 따로 있는지 확인.
- 다음 액션: GitHub 공개/license 확인(지금) → 내부 agent 평가 mini-harness PoC를 우리 Chromium 데이터로(다음 분기, 하네스 담당과).
- 자세히 → [workman-2026-scbench_lens-academic.md](workman-2026-scbench_lens-academic.md), [workman-2026-scbench_lens-industry.md](workman-2026-scbench_lens-industry.md) §4

---
마지막 갱신: 2026-06-13
