# Abstract Analysis — Spark-to-Paper

> 대상: Qian et al., "Spark-to-Paper: End-to-End Research Paper Generation as a Composable Skill", arXiv:2608.11924 (2026).
> 근거: `sources/fulltext_extract.md`(HTML fulltext 추출). Abstract 원문 대신 fulltext 요약 기반이라, 초록 고유 문구는 `검토필요:`.

## Abstract Summary
- **한 문장 요약:** end-to-end 논문 생성(문헌검색·실험·증거기반 claim 수정·그림·문서정합)을 별도 자율 에이전트 플랫폼이 아니라 기존 coding assistant 안의 **13개 재사용 skill**(8 stage + 각 stage 결정론적 gate)로 구현하고, 검증 스택으로 fabrication 탐지·인용 정합을 정량화한 시스템.
- **연구 목적:** "논문 생성을 standing orchestration 인프라 없이, coding assistant 내장 skill 묶음으로 돌릴 수 있는가"를 실증.
- **문제 또는 gap:** 기존 자율 연구 에이전트(AI Scientist 등)는 자체 orchestration layer를 가진 standalone 플랫폼을 요구한다. 반대로 인프라 없는 접근은 자동화 범위가 좁다. Spark-to-Paper는 그 사이(인프라 없이 넓은 범위)를 노린다.
- **핵심 방법:** (1) 8 stage 파이프라인(Input Routing→Plan→Cite→Write→Refine→Review→Figure→Assemble, 조건부 Experiment)에 stage별 **결정론적 gate**. (2) 검증 3층: 결정론 gate + self-review + adversarial review(3분류 검증). (3) 실험 **preregistration**(표 구조 먼저, 셀은 결과 전까지 공백). (4) **Claim Admission 5라벨**(supported/partially/unsupported/contradicted/needs-confirmation). (5) **Self-Refutation loop 7-cap → 실패 리포트**.
- **주요 결과:** citation validity **99.5%** [98.4–100%] (384 refs; human 97.8%, single-pass 81%). figure editability **96.4%** (human 58%, 이전 자율시스템 0–3%). fabrication 탐지 ablation **14%→69%(+gate)→81%(+self-review)→92%(+adversarial)** (36 probe). adversarial review precision **74%** (57 issue). 비용 **$8.1**·**11.9M token**·**3.2h**/편 (8 topic).
- **저자가 주장하는 기여:** 자율 플랫폼 없이 coding assistant 내장 skill만으로 "증거에 묶인(evidence-grounded)" 논문 생성이 가능함을 보이고, 결정론적 검증가능 속성(인용·그림·fabrication)을 정량화. `해석: 저자 스스로 "출력의 검증가능 속성을 잰 것이지 연구 가치를 잰 것이 아니다"라고 범위를 좁힌다.`

## 모호한 주장 / caveat (저자 자체 표기)
- claim-level 증거 판정이 현재 **model-based**(의미적 지지 여부를 모델이 판단) → auditing 필요 약점으로 인정.
- preregistration은 **lightweight·non-binding**, 모델이 여전히 사후 claim 판정.
- 이전 시스템 비교는 **재실행 없이** 공개 논문 값만 사용(model backbone·pricing 비정규화).
- fabrication ablation은 **36 probe/10 failure family**만 → coverage 제한.
- Claude Code backend 종속(타 구현 없음).

## Abstract 외부 맥락 (우리 관점)
`외부 맥락: 이 논문은 우리 팀이 만드는 논문 생산·검증 하네스(kakyungkim/paper-production-harness + verify-harness 3층)와 독립적으로 같은 문제를 푼 선례다. 우리 BIOP01 §6.1 AI Scientist 검증게이트(BIOP01-81)·검증하네스 운영화(BIOP01-84)의 직접 근거·비교 대상이 된다. 상세 비교는 이 폴더의 comparison 문서 및 JIRA 티켓 참조.`
