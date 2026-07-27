# HARNESS.md — 랩 구조 (Agent 하네스 지도) — HSPC velocity-lag benchmark  【after / 검토용】

*Designed by Ka-Kyung Kim, 2026 — reusable paper-production harness (CC BY 4.0). after-revision by 이건규, 2026-07-26 (BIOP02-100).*

> **교체 후보본.** 라이브 `docs/HARNESS.md`를 아직 대체하지 않았다. 승인 시 스왑.
> 이 하네스를 **하나의 연구 랩**으로 본 지도다. 각 agent는 멤버, 사람(+메인 루프)이 PI.
> 정본 명세는 리포 루트 **`harness.yaml`**(SSOT). 이 문서·CLAUDE.md·SKILL은 그 manifest를 따르며 `scripts/harness_doctor.py`가 대조한다.

## 0. 실행 전제 (필수)
- **반드시 repo 루트를 cwd로 실행한다.** 상위 디렉터리에서 시작하면 `.claude/agents/`가 로드되지 않아 `agent type not found` → `general-purpose`로 **조용히 폴백**한다(산출물은 나오므로 놓치기 쉬움).
- **전문 agent 호출 실패를 범용 agent 실행으로 대체하지 않는다.** 필수 agent·Skill 누락 시 production run을 **중단**한다.
- 진입은 `scripts/start-paper-harness`(존재 검사) → orchestrator self-check(첫 단계 필수 구성요소 검사) 경유. (BIOP01-65)

## 1. 구성요소 인벤토리 (숫자 요약 대신 명세표)
| 논리 역할 | 구현 형태 | 경로 | 상태 |
| --- | --- | --- | --- |
| domain analyst (`hspc-velocity-analyst`) | project agent | `.claude/agents/` | 구현 (project profile 슬롯) |
| literature scout | project agent | `.claude/agents/` | 구현 |
| novelty strategist | project agent | `.claude/agents/` | 구현 |
| research methodologist | project agent | `.claude/agents/` | 구현 |
| manuscript writer | project agent | `.claude/agents/` | 구현 |
| presenter | project agent | `.claude/agents/` | 구현 |
| paper critic | project agent | `.claude/agents/` | 구현 |
| design | project agent | `.claude/agents/` | 구현 |
| paper planner (`paper-orchestrator`→`paper-planner`) | agent | `.claude/agents/` | 구현 (개명 예정 BIOP01-70) |
| **venue reviewer** | agent | `.claude/agents/venue-reviewer.md` | **미구현** — 참조만 존재 (BIOP01-64) |
| production runner (`paper-production-orchestrator`→`paper-runner`) | **Skill** | `.claude/skills/.../SKILL.md` | 구현 (개명 예정) |
| figure generation | script | `figures/figNN_*.py` | 구현 |
| result / package validation | script | `scripts/p3_*.py` | 구현 |
| release approval | human | — | 운영 규칙 |

> `venue reviewer`는 프로젝트 로컬로 구현하거나(전역 실체화 금지) 참조를 제거한다. 같은 모델 계열이 역할만 바꾸면 외부 referee가 아니라 venue-style *simulated* review이므로, 구현 시 격리(다른 모델 계열 / 원고 패키지만 전달 / 내부 논의 차단 / 사용 모델·입력 기록).

## 2. 게이트 (3분류)
| 게이트 유형 | 예시 | 실패 시 |
| --- | --- | --- |
| 자동 무결성 | 숫자 재계산·파일 대조·스키마 검사 (`p3_*`), 하네스 정합성(`harness_doctor.py`) | 즉시 중단 |
| 과학적 판단 | claim-defensibility(반증기준+make-or-break+advisor), 방법론 승인 | 사람 승인 |
| 공개·거버넌스 | 저자·소속·IP·corresponding email·데이터 공개 | 책임자 승인 |

- **검증은 두 번**: ① 분석 직후(결과 검증) ② 공개 직전(패키지 검증). claim lock에는 사람(advisor)의 과학적 판단이 들어간다 — "사람 게이트=공개뿐"이 아니다.

## 3. 표준 경로 (검증 게이트를 외부 리뷰 앞에)
```
기획(methodologist/scout/novelty) → claim·검정 계획 확정
  → hspc-velocity-analyst → results/FINDINGS.md
  → [결과 검증 게이트: p3_concordance + p3_crossdataset_concordance + p3_scrambled_null]
  → manuscript-writer → manuscript/draft_v2.md + draft_v2_ko.md  (그림: figures/figNN_*.py)
  → paper-critic (적대 검수 + 그림 QA)
  → (선택) venue-reviewer → manuscript/REVIEW-<venue>-<date>.md
  → [패키지 검증 게이트: 원고 숫자=결과 파일, 그림 재생성, commit/데이터 고정]
  → presenter (최종 발표자료)
  → [공개 게이트: 사람 — 저자·소속·IP]
```

## 4. 계층 분리 (재사용 관점 — BIOP01-67)
- **Core harness**(도메인 무관): 호출 규약·artifact contract·stage transition·실패 정책·run state·reviewer 격리·release gate·self-check.
- **Project profile**(프로젝트별): domain analyst·검증 명령·데이터/결과 경로·claim 금지 규칙·`PAPER_DIRECTION.md`·필수 그림/표·지표. → "슬롯 하나만 교체"가 아니라 **profile 제공**.
- **Run instance**: `RUN_STATE.yaml`(BIOP01-68) — 현재 단계·commit·완료 게이트·승인자·산출물 sha256.

## 5. 정합성 (SSOT + doctor)
`harness.yaml`이 명세, 문서·코드가 이를 따른다. `python scripts/harness_doctor.py --repo . --manifest harness.yaml`을 PR CI에서 실행 → 팬텀 역할·경로 drift가 사람 검토 전에 실패한다. (BIOP01-66)
