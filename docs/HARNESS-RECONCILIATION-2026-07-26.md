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

---

## 6. 2차 조사 — 원본·BIOP02까지 확대 (2026-07-26 추가)

**배경.** §1–§5(1차)는 BIOP01만 봤다. 그런데 BIOP02-100의 원래 검토 대상은 **원본·BIOP01·BIOP02 3자**다. 이날 저녁 원본(`kakyungkim/paper-production-harness`)과 BIOP02(`docs/BIOP02-53-kkkim-critic-review`)를 추가로 클론해 대조했고, BIOP01 문서는 백틱 인용 경로까지 전수 재스캔했다. 아래는 전부 파일 직접 확인 결과이며, 1차 결론 중 **두 건(M1 범위·M2 등급)을 정정**한다.

### M5 — `reviewer` 팬텀의 출처는 원본이다 (M1 범위 정정)

- **사실**: 원본 `agents/`에 파일 8개(design · literature-scout · manuscript-writer.template · novelty-strategist · paper-critic · paper-orchestrator · presenter · research-methodologist) — **`reviewer.md` 없음**. 그런데 원본 `agents/paper-orchestrator.md:13`이 `**reviewer** (external referee, substance-only)`를 정식 멤버로 명시한다.
- **영향**: BIOP01·BIOP02가 각각 실수한 게 아니라 **원본이 유령을 배포했고 두 인스턴스가 상속**했다. BIOP01만 고치면 원본에서 새로 인스턴스화하는 다음 프로젝트가 같은 팬텀을 다시 상속한다.
- **재현**: `git clone --depth 1 https://github.com/kakyungkim/paper-production-harness` → `ls agents/` → `grep -n "reviewer" agents/paper-orchestrator.md`
- **권고**: BIOP01-64의 반영 대상을 **2곳(BIOP01·BIOP02) → 3곳(+원본)** 으로 확대. 원본은 소유자(kkkim) 협의 필요.
- **완료조건**: 세 리포 모두에서 `reviewer` 참조가 실체와 일치(구현 또는 제거)하고, 원본 README에 이 스캐폴드가 `reviewer`를 포함하는지 여부가 1줄로 명시된다.

### M6 — 게이트 순서(M2)는 설계 관찰이 아니라 원본 규칙 위반이다 (등급 승격)

- **사실**: 원본 `agents/paper-orchestrator.md:23`이 순서를 명문화한다 — *"the internal→external review order (**paper-critic + gate FIRST, then reviewer** — reviewer assumes pre-submission QA is done)"*. 그런데 **BIOP01 SKILL.md와 BIOP02 SKILL.md 둘 다** step 7(정식 리뷰) → step 8(검증 게이트) 순서다.
- **영향**: 1차 보고는 이를 "설계 관찰(권고)"로 적었다. 실제로는 **원본이 스스로 정한 규칙을 두 인스턴스가 동일하게 뒤집은 인스턴스화 회귀**다. 취향 논쟁이 아니라 확정 불일치이므로 합의 없이 정정 가능한 항목으로 등급을 올린다.
- **재현**: 원본 `agents/paper-orchestrator.md:23` vs `BioProject01/.claude/skills/.../SKILL.md:51-52`, `BioProject02/.claude/skills/.../SKILL.md:39-40`.
- **권고**: 두 인스턴스의 step 7↔8 순서 교환. 검증 게이트는 §4 권고대로 **분석 직후 + 공개 직전 이중화**(kkkim 공동리뷰에서 동의됨 — `harness.yaml`의 result_validation/package_validation 분리로 해소).
- **완료조건**: 양 SKILL.md에서 결정론 게이트가 외부 리뷰보다 앞에 오고, 원본 규칙 인용이 주석으로 남는다.

### M7 — BIOP02에서는 팬텀이 문서가 아니라 **실행 설정에 배선**돼 있다 (신규·최고 위험)

- **사실**: `BioProject02/agents/critic/auto_review_config.json:58` → `"agents": ["paper-critic", "reviewer"]`, `"independent_passes": 2`. 이 값은 `auto_review_orchestrator.py`의 `drain_queue()`가 `review_requests/*.req.json`으로 발행하고 세션/OpenClaw가 그대로 실행한다. 현재 `"enabled": false`(dry-run)라 아직 터지지 않았을 뿐이다.
- **영향**: 활성화하는 순간 **적대적 리뷰 2패스 중 한 축이 존재하지 않는 에이전트를 호출**한다. 호출 실패가 예외로 뜨지 않고 범용 에이전트로 조용히 대체되면, 자동 리뷰는 "2패스 통과"로 기록되지만 실제로는 1패스만 돈 것이 된다. **P2(침묵 폴백)를 P0로 올린 판단이 코드로 확증됐다.**
- **재현**: `grep -n '"agents"' BioProject02/agents/critic/auto_review_config.json`, `sed -n 95,120p BioProject02/agents/critic/auto_review_orchestrator.py`
- **권고**: BIOP01-64 결정(구현 or 제거) 전까지 `enabled=true` 금지. 결정 후 config를 실체와 일치시키고, `forbid_generic_fallback`을 실행 래퍼가 강제한다(BIOP01-65).
- **완료조건**: config의 `agents` 목록 전원이 `.claude/agents/`에 실재하고, harness_doctor의 스캔 대상에 이 config가 포함된다.

### M8 — BIOP01 라우터·핸드오프 계약이 통째로 팬텀 (신규, `reviewer`보다 넓음)

- **사실 (a) 라우터**: `skills/` 디렉터리는 `bc7f824`(2026-06-14, *"pipeline: restructure kkkim-pipeline as pipeline-only branch"*)에서 삭제됐다. 그런데 `AGENTS.md:52-56`은 여전히 *"Dataset 작업 요청이면 먼저 `skills/ROUTES.md`를 읽습니다 → `skills/<dataset>/<task>/SKILL.md`를 사용합니다"* 로 라우팅을 위임한다. `README.md:12,27` · `CLAUDE.md:17,18,19`도 같은 경로(`skills/ROUTES.md`, `agents/openai.yaml`)를 가리킨다. **OpenClaw/Codex 쪽 라우터 전체가 죽은 링크다.**
- **사실 (b) 핸드오프 계약**: `CLAUDE.md:91` 산출물 계약의 마지막 행이 `| 상태 핸드오프 | (전원) | HANDOFF.md, TODO.md, SESSION-LOG.md | 다음 세션 |` 이고 `SKILL.md:75`도 동일하다. 이 브랜치에 **세 파일 모두 없다**(같은 재구조화 때 정리됨, 이력상 다른 브랜치에 존재). BIOP02도 동일 증상(`SESSION_LOG.md`/`TODO.md`/`HANDOFF.md`).
- **사실 (c) 규약**: `AGENTS.md:61-67`의 `data/` · `metadata/` · `work/` · `outputs/` 규약 디렉터리도 이 브랜치에 없다.
- **영향**: ① **BIOP01-45(OpenClaw로 P2–P5 runner 자동 실행)가 존재하지 않는 라우터 위에 설계되고 있다.** ② 모든 에이전트가 "필수 산출물"로 지시받는 핸드오프 파일이 없어, 매 실행이 새로 만들거나 조용히 건너뛴다 — 세션 간 상태 인계가 계약상으로만 존재한다. ③ **근본 원인이 `reviewer` 팬텀과 같다**: 파일을 지운 커밋이 문서를 안 고쳤고, 이를 잡을 게이트가 없었다. 즉 BIOP01-66(정합성 게이트)의 실증 사례가 1건에서 **3건**으로 늘었다.
- **재현**: `git log --diff-filter=D --oneline -- skills` → `bc7f824`. 그리고 아래 M9의 doctor 실행.
- **권고**: (1) `AGENTS.md` 라우팅 절을 실체에 맞게 정정하거나 `skills/`를 복원 — **BIOP01-45 착수 전 선결**. (2) 핸드오프 3파일을 만들거나 계약에서 제거(둘 중 하나, 방치 금지). 어느 쪽이든 `harness.yaml`에 등재.
- **완료조건**: harness_doctor `phantom-path` 0건.

### M9 — 1차 `harness_doctor.py`는 M8을 잡지 못했다 (자기 점검 + 이번 커밋의 보완)

- **사실**: 1차 doctor의 `doc_reference_scan.files`가 3개(`CLAUDE.md` · `docs/HARNESS.md` · `SKILL.md`)뿐이라 **`README.md` · `AGENTS.md`가 스캔 밖**이었고, 검사 대상도 *역할 이름 토큰*뿐이라 **경로 실재는 보지 않았다**. M8은 doctor가 아니라 별도 임시 스캔으로 찾았다.
- **조치 (이번 커밋)**:
  1. `harness.yaml`에 `path_reference_scan` 추가 — 백틱 인용 경로의 실재 검사. `resolve_by_basename`으로 상대 인용(`p3_concordance.py`)을 허용하고, 외부 repo·IP·모델 ID는 `ignore` 정규식으로 제외.
  2. 스캔 대상을 5개 문서로 확대(`README.md` · `AGENTS.md` 추가).
  3. **팬텀 에이전트 검출에 맥락 필터** — 백틱 인용 또는 표 행만 `FAIL`, 산문 언급은 `WARN`. (kkkim 공동리뷰 지적 반영: 산문에 'reviewer'가 우연히 들어간 경우의 오검 방지.)
- **실측 결과** (BIOP01 현재 상태, 보완 후):

  ```
  harness_doctor: repo=/home/gglee/project/BioProject01
    roles=12  artifacts=5  scan_files=5  phantom_paths=11
    WARN [phantom-agent?] 'reviewer' … CLAUDE.md:63 / HARNESS.md:49,62 / SKILL.md:3,28   (산문 — 사람 확인)
    FAIL [phantom-agent]  'reviewer' … CLAUDE.md:76,89 / HARNESS.md:28 / SKILL.md:51,73  (라우팅·계약 = 강한 참조)
    FAIL [phantom-path]   'skills/ROUTES.md'  ← README.md:27, AGENTS.md:52,54, CLAUDE.md:18
    FAIL [phantom-path]   'HANDOFF.md' · 'TODO.md' · 'SESSION-LOG.md'                     (핸드오프 계약)
    FAIL [phantom-path]   'agents/openai.yaml' · 'openai.yaml' · 'data/' · 'metadata/' · 'work/' · 'outputs/'
                          · 'download/preprocessing/model/visualization'
  RESULT: FAIL (14 문제, 3 경고)   exit 1
  ```

- **교훈**: 정합성 게이트도 **스코프가 곧 성능**이다. 게이트를 넣는 것으로 끝나지 않고, "무엇을 스캔 대상에 넣을지"가 manifest에 명시되고 리뷰돼야 한다.

### 공동 리뷰 반영 (kkkim, 2026-07-26 18:53)

self-review 방지를 위해 kkkim 님께 공동 리뷰를 요청했고 **3관점(① venue-reviewer 프로젝트 로컬 ② 정합성 게이트 최우선 ③ 검증 게이트 이중화) 모두 승인**을 받았다. kkkim 님은 gglee 브랜치를 worktree로 띄워 doctor를 직접 실행해 FAIL(exit 1) 재현까지 확인했다. 반영 요청 2건은 다음과 같이 처리한다.

| 요청 | 처리 |
| --- | --- |
| 팬텀 토큰 스캔에 맥락 필터 한 겹 (오검 방지) | **이번 커밋 반영** — 강한 참조(백틱/표)만 FAIL, 산문은 WARN (M9-3) |
| 스왑 시 `ci/harness-doctor.yml` → `.github/workflows/` 로 PR CI 활성화 | **스왑 승인 시 수행** (BIOP01-66). 활성화 전까지 doctor는 수동 실행이라 drift가 사람 손에 의존한다 |

kkkim 님이 예고한 BIOP02용 `harness.yaml`(project_profile: biop02, 슬롯=`spatialpatho-analyst`, 게이트=BIOP02판)에는 위 M7(config의 `agents` 목록)도 스캔 대상으로 포함할 것을 권한다.

### 2차 조사 후 우선순위 갱신

| 순위 | 항목 | 티켓 | 변화 |
| --- | --- | --- | --- |
| P0 | 정합성 게이트(manifest + doctor + CI) — 스캔 범위 확대 포함 | BIOP01-66 | 실증 사례 1건 → **3건** |
| P0 | 침묵 폴백 차단(실행 전제 · 래퍼 · self-check) | BIOP01-65 | BIOP02 config 배선(M7)으로 **근거 강화** |
| P0 | 라우터 팬텀 해소 — `skills/ROUTES.md` | (신규) | **BIOP01-45 선결 조건** |
| P1 | `reviewer` → `venue-reviewer` 실체화/제거 | BIOP01-64 | 대상 2곳 → **3곳(+원본)** |
| P1 | 게이트 순서 정정(step 7↔8) | (신규) | 관찰 → **원본 규칙 위반** |
| P1~P3 | 3계층 분리 / RUN_STATE / CLAIMS / 개명 | BIOP01-67 · 68 · 69 · 70 | 변화 없음 |

---

## 7. 산출물 인덱스 (branch `gglee`)

| 산출물 | 내용 |
| --- | --- |
| `docs/HARNESS-RECONCILIATION-2026-07-26.md` | 이 문서 — 불일치 보고 (1차 §1–§5, 2차 §6) |
| `harness_after/` | 교체용 after 버전 (manifest · doctor · 문서 · 래퍼 · 템플릿 · CI). **라이브 미적용** |
| `harness_after/README.md` | 스왑 방법 (`cp` 목록 + `git revert` 되돌리기) |
| `onboarding_gglee/` | 온보딩 1~3주차 회고 산출물 (BIOP01-1 · 15 · 8) |

> 라이브 `README.md` · `CLAUDE.md` · `docs/HARNESS.md`에서 위 산출물로 가는 링크는 **아직 넣지 않았다** — 7/21 합의(구조 미수정)에 따라 스왑 승인 시 함께 반영한다.

---

## 8. 정정 — M8(b) 핸드오프 파일은 팬텀이 아니다 (2026-07-26 밤, 스왑 중 발견)

§6 M8(b)에서 나는 `HANDOFF.md`·`TODO.md`·`SESSION-LOG.md`가 *"같은 재구조화 커밋으로 사라졌는데 계약은 여전히 필수로 지시한다"* 고 적었다. **이 진단은 틀렸다.**

- 실제: `.gitignore:115-117`이 세 파일을 명시적으로 제외한다. 도입 커밋은 `78a5a92`(2026-07-01) — *"chore: 개인 작업기록(HANDOFF/TODO/SESSION-LOG) untrack"*, 주석은 *"개인 작업기록(연구 산출물 아님, 편의상 로컬 유지)"*.
- BIOP02도 동일하다(`.gitignore:246-248`).
- 즉 **삭제된 게 아니라 의도적으로 리포에서 뺀 로컬 전용 파일**이다. 새 clone에 없는 것이 정상 동작이다.

발견 경위: BIOP01-71로 세 파일을 만들어 커밋하려 하자 `git add`가 스테이징하지 않았다. `git check-ignore -v`로 확인.

### 그래서 진짜 결함은 무엇인가 (범위 축소·성격 변경)

1. **계약에 "로컬 전용"이 안 적혀 있다.** `CLAUDE.md:91`·`SKILL.md:75`가 이들을 "(전원) 필수 산출물"로만 지시해서, 리포를 처음 보는 세션은 존재해야 할 파일이 없다고 읽는다 — 내가 정확히 그렇게 읽었다. → 두 계약 행에 **로컬 전용(.gitignore) 표기 추가**로 해소.
2. **doctor가 오검을 냈다.** 팬텀 경로 검사가 이 셋을 FAIL로 올렸다. kkkim 님이 공동리뷰에서 경고한 오검 유형(맥락 없는 스캔)이 다른 형태로 재현된 것이다. → manifest에 `path_reference_scan.local_only` 선언을 두고, doctor는 **부재해도 FAIL하지 않되 `.gitignore` 등재 여부를 확인**한다(계약상 필수인데 ignore에서 빠지면 실수로 커밋되므로 그때는 FAIL). 테스트 2종 추가(#13·#14).

### 교훈 (게이트 설계)

"문서가 가리키는데 파일이 없다"는 **두 가지 다른 상태**를 가린다 — ① 진짜 drift(고쳐야 함) ② 의도적 로컬 전용(정상). 게이트가 이 둘을 구분하지 못하면, 팀은 게이트의 빨간불을 무시하는 법을 배운다. **의도는 manifest에 선언돼야 하고, 게이트는 선언되지 않은 것만 문제 삼아야 한다.**

이 정정으로 팬텀 경로는 11건 → **8건**으로 줄었고, 남은 8건은 전부 `skills/` 라우터 결정(BIOP01-71)에 걸려 있다: `skills/ROUTES.md`, `openai.yaml`, `agents/openai.yaml`, `download/preprocessing/model/visualization`(README:12), 그리고 `AGENTS.md`의 규약 디렉터리 `data/`·`metadata/`·`work/`·`outputs/`.

> §6 M8(b)와 그에 근거한 BIOP01-71 설명·Jira 코멘트는 이 절로 정정한다. 원문은 기록으로 남긴다.
