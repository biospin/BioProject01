# 논문 생산 하네스 — 구조 ↔ 현재 상태 불일치 보고 (BIOP01)

- **작성**: 이건규 (Geon-Gyu LEE) · 2026-07-26
- **관련 티켓**: BIOP02-100 (논문 생산 하네스 검토 — 원본·BIOP01·BIOP02)
- **검토 대상**: BIOP01의 논문 생산 하네스 문서·에이전트 (`docs/HARNESS.md`, `CLAUDE.md` *Agent routing & artifact contract*, `.claude/agents/*`, `.claude/skills/paper-production-orchestrator/SKILL.md`)
- **검증 기준**: `gglee` 브랜치 (kkkim-pipeline 기준, tip `ee9d836`) 실제 파일. 아래 모든 항목은 리포 파일을 직접 확인한 결과이며 `/workspace` 사본이 아님.
- **7/21 회의 합의 반영**: 하네스 *구조*는 수정하지 않고 현황만 정리. 구조 변경이 필요한 항목은 후속 티켓으로 분리했다.

---

## 요약 (TL;DR)

- **확정 불일치 2건**: (M1) `reviewer` 팬텀 에이전트 — 문서 6곳에서 라우팅/멤버로 참조되나 실체(`.claude/agents/reviewer.md`) 없음. (M3) 프로젝트 스코프 에이전트가 **cwd 의존**으로 로드 실패(`agent type not found`) — 실행 전제(repo 루트)가 어디에도 문서화되지 않음.
- **설계 관찰 1건**: (M2) orchestrator 실행흐름에서 **외부 리뷰(step 7)가 결정론적 검증 게이트(step 8)보다 먼저** 배치됨. 게이트를 리뷰 앞에 두는 게 통상 순서.
- **이미 해소됨 1건**: (M4) 산출물 계약의 원고 경로가 구 `draft.md` → 정본 `draft_v2.md`/`draft_v2_ko.md`로 정리됨(kkkim, commit `ff0ec25` 계열, 본 브랜치 기준에도 반영 확인).
- **정상 확인**: 실재 에이전트 9개, orchestrator는 에이전트가 아닌 Skill로 실재, 검증 게이트 스크립트 3종(`p3_concordance.py`·`p3_crossdataset_concordance.py`·`p3_scrambled_null.py`) 모두 SKILL.md 명령 경로와 일치.

---

## 1. 확정 불일치

### M1 — `reviewer` 팬텀 에이전트 (구조 판단 필요)

`.claude/agents/`에 실재하는 에이전트는 **9개**: `design`, `hspc-velocity-analyst`, `literature-scout`, `manuscript-writer`, `novelty-strategist`, `paper-critic`, `paper-orchestrator`, `presenter`, `research-methodologist`. **`reviewer.md`는 없다.**

그런데 `reviewer`는 다음 6곳에서 실재 멤버/라우팅 대상으로 등장한다:

| 위치 | 내용 |
| --- | --- |
| `docs/HARNESS.md:28` | 멤버 명부 #9 `reviewer` (전역, 선택) |
| `docs/HARNESS.md:49` | 관계도(org chart)에 `reviewer(선택)` |
| `docs/HARNESS.md:62` | 표준 경로 `paper-critic ──▶ reviewer ──▶ manuscript/REVIEW-*.md` |
| `CLAUDE.md:63` | "모든 논문 멤버(novelty·literature·methodologist·writer·critic·**reviewer**)는 …" |
| `CLAUDE.md:76` | 라우팅표: "정식 venue 리뷰 시뮬레이션" → `reviewer` (전역, 선택) |
| `CLAUDE.md:89` | 산출물 계약: 리뷰 단계 Writer = `paper-critic / reviewer` |
| `SKILL.md:3,28,51,73` | description·멤버 구성·실행흐름 step7·산출물 계약 모두 `reviewer` 호출 |

**영향**: 자연어 "정식 venue 리뷰 시뮬레이션" 요청 → 존재하지 않는 에이전트로 라우팅 → (M3와 겹치면) `agent type not found`. 문서는 `reviewer`를 **"전역(global), 선택"** 으로 표기하는데, 이는 프로젝트 스코프(`.claude/agents/`)가 아니라 **유저 전역(`~/.claude/agents/`)에 두겠다는 의도**로 읽힌다. 그러나 이 환경엔 전역 위치에도 없다.

**판단 포인트(후속 티켓)**: (a) `reviewer`를 전역 에이전트로 **실체화**, (b) 문서에서 제거하고 `paper-critic`으로 **통합**, (c) 계속 "선택 전역"으로 두되 설치 안내를 문서화 — 중 택1. → **FT1**.

### M3 — 프로젝트 스코프 에이전트의 cwd 의존 로딩 (구조 판단 필요)

`.claude/agents/`의 프로젝트 에이전트는 Claude Code가 **cwd = repo 루트(또는 프로젝트 내부)** 일 때만 발견된다. cwd가 상위 디렉터리(예: `/home/kkkim/project`)면 `paper-critic`/`hspc-velocity-analyst` 호출 시 `agent type not found` → `general-purpose`로 폴백(7/21 kkkim 재현 기록).

이는 Claude Code의 동작 특성이지만, **하네스 문서 어디에도 "repo 루트에서 실행" 전제가 없다.** 하네스 사용성에 직접 영향.

**판단 포인트(후속 티켓)**: (a) `CLAUDE.md`/`docs/HARNESS.md`에 "실행 cwd = repo 루트" 전제 명시, (b) cwd 무관 로드가 필요한 멤버(특히 M1의 `reviewer`)는 전역(`~/.claude/agents/`) 배치로 분리. → **FT2**. (M1과 연동.)

---

## 2. 설계 관찰 (검토 질문 답변에 포함)

### M2 — 검증 게이트 ↔ 외부 리뷰 순서

`SKILL.md` 실행흐름: **step 7 `(선택) 정식 리뷰 reviewer` → step 8 `검증 게이트`**. `docs/HARNESS.md:62–64` 표준경로도 `paper-critic ▶ reviewer ▶ REVIEW` 다음에 `verify-gate ▶ presenter`. 즉 **외부 referee가 결정론적 숫자 재계산 게이트보다 먼저** 돈다.

헤드라인 숫자가 검증되기 전에 외부 리뷰를 소모하는 순서라, "내부 검수+검증 게이트를 먼저, 그다음 외부 referee"가 더 안전하다. (현재는 `reviewer`가 선택+팬텀이라 실무상 거의 안 돌지만, 구조 기술로는 어긋남.) → 권고: 게이트를 리뷰 앞으로. (경미 — FT에 선택 포함.)

---

## 3. 이미 해소된 항목 (확인만)

### M4 — 원고 경로(구 `draft.md`) → 정본 `draft_v2`

7/21 kkkim이 처리(commit `ff0ec25` 계열). 본 `gglee` 브랜치 기준에서도 살아있는 참조가 전부 정본을 가리킴을 확인: `CLAUDE.md:87`, `docs/HARNESS.md:60`, `SKILL.md:20/48/70`, `manuscript-writer.md:43`, `presenter.md:10` → 모두 `draft_v2.md` + `draft_v2_ko.md`. 구 `draft.md`/`draft_ko.md`는 삭제(git 이력 보존). **추가 조치 불필요.**

---

## 4. 검토 질문 5개에 대한 답 (AI로 논문 써본 관점)

1. **역할 분해가 실전과 맞는가**: 대체로 적절. 도메인 슬롯 1개(`hspc-velocity-analyst`) + 재사용 8개 구성은 깔끔하다. 단 `reviewer`(외부 referee)와 `paper-critic`(내부 적대검수)의 경계가 문서상 겹치고, `reviewer`가 팬텀이라 실전에선 `paper-critic` 하나가 두 역할을 겸한다 → 역할이 문서보다 하나 적게 돈다.
2. **게이트가 환각·과대주장을 실제로 막는 위치인가**: `claim-defensibility 게이트`(SKILL §2.5 — 반증기준+가장 싼 make-or-break 검정+advisor, 2층 융합 금지, 사전등록 봉인)는 **위치·설계 모두 좋다**(headline이 본문 들어가기 전). 결정론적 **검증 게이트**(숫자 재계산)도 유효. 다만 문서는 검증 게이트를 "PI(사람)가 통과"라 하지만 실제는 스크립트 자동 재계산이라 *사람 게이트가 아니다* — 표현 정정 필요. 그리고 M2(리뷰 뒤 배치).
3. **자연어 → 라우팅이 직관적인가**: 라우팅표(CLAUDE.md:67–79)는 직관적. 유일한 죽은 링크가 `reviewer` 행(M1).
4. **도메인 슬롯 1개 교체 = 타 분야 이식 가능한가**: 구조적으로 가능하고 **BIOP02(병리)가 실제 이식 사례**. 주의점: 검증 게이트 스크립트(`p3_*`)가 도메인 특화라 **슬롯과 함께 교체**돼야 하는데 문서엔 "슬롯만 갈아끼우면 됨"으로만 적혀 게이트 교체가 누락돼 있다.
5. **있었으면 했던 것**: (a) `reviewer` 전역 에이전트 실체 또는 명확한 제거, (b) 실행 cwd 전제 명시, (c) 도메인 이식 체크리스트(슬롯 + 검증게이트 스크립트 + PAPER_DIRECTION 동시 교체).

---

## 5. 후속 조치

- **FT1** (구조 판단): `reviewer` 팬텀 해소 — 전역 실체화 vs 제거/통합 결정 후 문서 6곳 반영.
- **FT2** (구조 판단): 프로젝트 에이전트 cwd 로딩 전제 문서화 + 전역 에이전트 배치 정리 (M1과 연동).
- 문서 최신화(비구조): 검증 게이트 "사람 통과" 표현 정정, 도메인 이식 시 게이트 교체 명시 — `gglee` 브랜치 문서 정리에서 처리.
- 공용 하네스 자산이므로 위 결정은 **BIOP02에도 동일 반영** 필요.
