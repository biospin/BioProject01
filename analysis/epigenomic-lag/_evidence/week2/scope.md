# Scope

## Topic

- primary topic: `epigenomic-lag`
- research question: gene별 chromatin-transcription lag structure를 정량화하고, epigenetic drug response timing 예측에 연결할 수 있는 방법론과 evidence를 비교한다.

## Seed papers

- `li-2023-multivelo` — MultiVelo, chromatin accessibility와 RNA velocity를 결합한 baseline method.
- `li-2025-multivelovae` — MultiVeloVAE, continuous decoupling factor와 VAE 기반 확장.
- `hong-2026-moflow` — MoFlow 후보. full analysis 필요.

## Keywords

- chromatin RNA coupling
- epigenomic lag
- RNA velocity
- ATAC RNA velocity
- multiome velocity
- chromatin accessibility transcription lag
- gene regulatory dynamics

## Inclusion criteria

- paired chromatin accessibility + RNA 또는 multiome data를 활용한다.
- chromatin state와 transcription / RNA dynamics의 시간적 관계를 다룬다.
- method, benchmark, biological validation, 또는 downstream drug response timing과 연결 가능성이 있다.
- 우리 프로젝트의 Human HSPC 10x Multiome 또는 유사 multiome dataset에 적용 가능성이 있다.

## Exclusion criteria

- scRNA-only velocity method로 chromatin / epigenomic feature를 다루지 않는다.
- 순수 epigenomic atlas paper로 temporal coupling 또는 response timing과 연결이 약하다.
- review / news / blog만 있고 primary evidence가 부족하다. 단, field map 보조 자료로는 별도 표시 가능.

## Priority

- must-have:
  - MultiVelo 계열 method 비교.
  - MultiVeloVAE의 개선점과 남은 한계.
  - MoFlow의 위치와 기존 method 대비 차별점.
  - HSPC multiome 적용 가능성.
- nice-to-have:
  - perturbation 또는 metabolic labeling 기반 external validation paper.
  - drug response timing과 epigenomic baseline feature를 연결한 paper.
  - regulatory / BD 관점에서 상용화 가능성이 있는 software 또는 assay paper.

## Week2 target outputs

- `papers.jsonl`: 비교 가능한 paper records.
- `comparison_table.md`: method / assay / result / limitation 빠른 비교표.
- `evidence_bundle.md`: Insight Agent 입력용 evidence bundle.
- `insight.md`: 연구 흐름, 차이, 반복 한계, unresolved gap.
- `validation_report.md`: insight claim별 근거 검증.
- `handoff.md`: Jira / Confluence ready action items.
