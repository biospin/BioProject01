# 하네스 3계층 — core / project profile / run instance (BIOP01-67)

> 이 문서는 "재사용 하네스"라는 주장을 실제 구조와 일치시킨다. 결론부터:
> **"도메인 슬롯 하나만 바꾸면 된다"는 과소진술이다.** core harness 는 재사용
> 가능하되, 각 프로젝트는 domain agent·검증 명령·paper direction·산출물 경로·
> claim별 과학 정책을 담은 **project profile** 을 제공해야 한다.

관련: `harness.yaml`(SSST manifest) · [HARNESS.md](HARNESS.md) · BIOP01-68(RUN_STATE.yaml) · BIOP01-69(CLAIMS.yaml).

---

## 왜 이 문서가 필요한가

`harness.yaml` 의 `roles` 는 재사용 코어 멤버와 도메인 슬롯을 한 파일에 섞어
둔다. 게이트도 마찬가지로 도메인 무관한 것(무결성 재계산)과 도메인 특화한 것
(`p3_concordance.py` 같은 HSPC velocity 전용 재계산)이 섞여 있다. 이 때문에
"도메인 슬롯 하나만 교체"라는 문장이 실제보다 이식을 쉬워 보이게 만든다.
새 분야로 옮기려면 아래 **project profile** 전체를 새로 써야 한다.

---

## 세 계층

### 1. Core harness — 도메인 무관 (리포·문서로 고정, 프로젝트 간 재사용)

바꾸지 않고 그대로 가져가는 부분:

- **agent 호출 규약** — 자연어 요청 → 역할 라우팅, 전문 agent 실패를 general
  로 대체 금지(`execution.forbid_generic_fallback`).
- **artifact contract** — 각 단계 산출물을 파일로 남긴다는 계약.
- **stage transition** — analysis → result_validation → writing → figures →
  review → package_validation → claim_defensibility → release 순서.
- **실패 정책** — 자동 게이트 실패 시 `stop_and_report`, 커밋·발행 금지.
- **run state** — RUN_STATE.yaml 스키마(BIOP01-68). 값은 run instance.
- **reviewer 격리 규칙** — venue-reviewer 는 검증 통과 원고만 입력받는다.
- **release gate** — 저자·소속·IP·corresponding·data_release 사람 승인.
- **self-check** — harness_doctor 정합성 게이트(BIOP01-66).

코어 멤버(재사용 agent): literature_scout · novelty_strategist ·
research_methodologist · manuscript_writer · presenter · paper_critic ·
design · manuscript_condenser · paper_planner · venue_reviewer ·
production_runner.

### 2. Project profile — 프로젝트별 (프로젝트마다 새로 제공)

`harness.yaml` 의 `project_profile:` 가 가리키는 도메인 특화 묶음. **여기가
이식 비용의 대부분이다.**

| 구성요소 | BIOP01(현재) 실체 | 새 프로젝트가 제공해야 하는 것 |
|---|---|---|
| domain analyst | `hspc-velocity-analyst` | 그 분야 분석 실행 agent |
| 검증 명령(result_validation) | `p3_concordance.py` · `p3_crossdataset_concordance.py` · `p3_scrambled_null.py` | headline 숫자를 결정론적으로 재계산하는 스크립트 |
| 데이터셋/결과 경로 | `pipeline/hspc-velocity-benchmark/{results,manuscript,figures}` | 그 프로젝트의 artifact 경로 |
| paper direction | `manuscript/PAPER_DIRECTION.md` | 연구 질문·서사·차별화 |
| claim별 과학 정책 | CLAIMS.yaml 의 limitations(예: "실질 비식별성을 완전 비식별성으로 과장 금지") | claim별 금지·한정 규칙 |
| 필수 그림/표 | figures 스크립트 | 그 논문의 필수 도표 |
| 평가 지표 | concordance ρ · sign-agreement · profile-likelihood 민감도 | 그 분야 지표 |

### 3. Run instance — 실행마다 (RUN_STATE.yaml 한 파일)

한 번의 생산 실행 상태. run_id · source_commit · stage · 게이트별 통과 기록 ·
산출물 sha256 · 실패·재시작 이력. 코드가 아니라 상태다. → `RUN_STATE.yaml`
(BIOP01-68). runner 만 갱신, planner 는 읽기만(BIOP01-70).

---

## 경계 판정 규칙 (어디에 넣을지)

새 구성요소를 추가할 때:

1. **분야가 바뀌어도 그대로 쓰는가?** → core harness.
2. **분야가 바뀌면 새로 써야 하는가?** → project profile.
3. **실행마다 값이 바뀌는가?** → run instance(RUN_STATE.yaml).

`p3_*` 스크립트가 core 처럼 보이지만 HSPC velocity 지표를 재계산하므로
project profile 이다. 반대로 "숫자는 결과 파일에서만"이라는 규칙은 분야와
무관하므로 core 다.

---

## project profile 스펙 (새 프로젝트 체크리스트)

새 분야로 하네스를 이식할 때 아래를 모두 채워야 "이식 완료"다. 하나라도
비면 harness_doctor 가 팬텀으로 잡거나(경로/역할) 게이트가 도메인 숫자를
재계산하지 못한다.

- [ ] `harness.yaml` 의 `project_profile:` 값을 새 프로젝트 키로 교체
- [ ] domain analyst agent 1개(`roles.domain_analyst.path`)
- [ ] `gates.result_validation.commands` — headline 숫자 재계산 스크립트
- [ ] `artifacts.*` — findings·manuscript·figures_dir·paper_direction 경로
- [ ] `PAPER_DIRECTION.md` — 연구 질문·차별화
- [ ] `CLAIMS.yaml` — headline claim + claim별 limitations(BIOP01-69)
- [ ] 필수 그림/표 생성 스크립트
- [ ] harness_doctor PASS(팬텀 0)로 정합 확인
