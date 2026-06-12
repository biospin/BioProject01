# Methodology Brief — workman-2026-scbench

## 한 줄 결론 (모든 독자)

- Citation: `@workman2026scbench` | Importance: `상` — AI agent가 scRNA-seq에서 어떤 task·platform에서 실패하는지 처음으로 정량화한 유일한 benchmark.
- 한 문장 결론: 394개 검증 가능 문제로 구성된 scRNA-seq AI agent benchmark; 현재 SOTA(Claude Opus 4.6) 52.8%, cell typing·DE가 가장 어렵고 platform 선택이 모델 선택보다 성능 변동에 더 크게 기여.

## 재현 가능성 체크 (재현 담당자)

- 데이터 접근: 공개 30개 canonical evaluation — `open` (GitHub latchbio/scbench); 나머지 364개 — `proprietary` (training contamination 방지, 저자 보유)
- 코드 공개: https://github.com/latchbio/scbench — CC BY 4.0; benchmark framework + graders + linter + agent harness 포함; maintenance 상태 active (2026-02)
- 자원 요구: LLM API 비용(frontier model 필수); 로컬 실행 환경(Python + scanpy/anndata/numpy/pandas/scipy); GPU 불필요 (통계 분석 위주)
- 핵심 의존성: `scanpy`, `anndata`, `numpy`, `pandas`, `scipy`, `matplotlib`; mini-SWE-agent harness (Yang et al., 2024)
- 자세히 → [workman-2026-scbench_core.md](workman-2026-scbench_core.md) §방법론, [sources/workman-2026-scbench.pdf](sources/workman-2026-scbench.pdf) §Methods 4

## 우리 적용 가능성 (의사결정자)

- Dataset 호환: 부분 일치 — Chromium platform이 10x 기반으로 가장 근접; HSPC multiome은 scBench에 직접 포함 안 됨
- 자원 가능성: 가능 — 공개 30개 eval은 현재 팀 환경에서 실행 가능; Claude API 비용만 발생
- 비용·시간 추정: 30개 canonical eval 자체 실행 → 1~2일; 결과 해석 + 내부 보고서 → 1주
- ROI 한 줄: cell typing·DE 자동화 한계(~30%)를 확인 → 인간 전문가 유지 비용 정당화, normalization 자동화(~70%) 우선 도입 근거
- 자세히 → [workman-2026-scbench_lens-industry.md](workman-2026-scbench_lens-industry.md) §3 (BD value & 상용화)

## 본인 재회고 (본인)

- 질문: 우리 Claude API 기반 파이프라인으로 30개 canonical eval 실행 시 논문 결과(Claude Sonnet 4.5 = 44.2%)와 얼마나 일치하는지 자체 검증 필요
- 질문: scBench peer review 결과 추적 — Nature Methods / Bioinformatics 제출 여부 확인
- 다음 액션: latchbio/scbench GitHub clone → 30개 canonical eval 환경 셋업 → 내부 eval 실행 (다음 스프린트 내)
- 자세히 → [workman-2026-scbench_lens-academic.md](workman-2026-scbench_lens-academic.md), [workman-2026-scbench_lens-industry.md](workman-2026-scbench_lens-industry.md) §4

---
마지막 갱신: 2026-06-09
