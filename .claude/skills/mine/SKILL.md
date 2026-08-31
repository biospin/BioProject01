---
name: mine
description: 내 할 일 브리핑. git 원격 동기화 상태, JIRA(나에게 할당된 이슈 + 내가 멘션된 댓글), HANDOFF/TODO/SESSION-LOG 를 한 번에 훑어 "지금 내가 할 일"을 우선순위로 정리한다. "/mine", "내 할일", "오늘 뭐 해야 하지", "상태 브리핑", "밀린 것 정리해줘" 에서 사용한다. 읽기 전용이며 커밋·수정·댓글 작성은 하지 않는다.
---

# /mine — 내 할 일 브리핑

세션을 열자마자 흩어진 상태(git, JIRA, 로컬 원장)를 한 번에 모아 **오늘 내가 손댈 것**을 추려 내는 스킬이다.

## 대원칙

- **읽기 전용.** fetch 는 하되 pull·merge·commit·push 는 하지 않는다. JIRA 댓글도 쓰지 않는다.
  상태를 바꿔야 할 일이 보이면 목록에만 올리고 사용자 지시를 기다린다.
- **추측 금지.** 조회가 실패했거나 파일이 없으면 "확인 못 함"으로 적는다. 비어 있는 것과
  못 본 것을 구분한다.
- **덤프 금지.** 원시 JSON·전체 로그를 늘어놓지 말고, 사람이 바로 행동할 수 있는 형태로 줄인다.

## 고정값 (검증됨, 2026-08-31)

- JIRA cloudId: `612634c4-1477-4aed-a493-c0b6d1fd27ec` (biospin-ai)
- 본인 accountId: `5be381ccf6f9e64e2f12a012` (김가경)
- 프로젝트 키: `BIOP01`(BioProject01), `BIOP02`(BioProject02), `SCRUM`(VibeCoding)
- 리포: `~/projects/autobiox/BioProject01`, `~/projects/autobiox/BioProject02` (각각 별도 git)

## 1단계 — git 원격 동기화 상태

두 리포 각각에 대해 실행한다. 현재 작업 중인 리포를 먼저 본다.

```bash
git fetch --all --prune
git status -sb | head -2          # ahead/behind 확인
git log --oneline HEAD..@{u}      # 원격에만 있는 새 커밋
git log --oneline @{u}..HEAD      # 아직 push 안 한 로컬 커밋
git status --porcelain | head     # 커밋 안 된 변경
```

보고할 것은 넷이다. 현재 브랜치와 HEAD, 뒤처진/앞선 커밋 수와 그 제목, 커밋 안 된 변경,
그리고 남이 올린 커밋 중 내 작업과 겹치는 것.

`behind` 이면 "pull 필요"라고만 적고 **직접 pull 하지 않는다** (로컬 변경과 충돌할 수 있다).

## 2단계 — JIRA

두 쿼리를 던진다. `mcp__atlassian__searchJiraIssuesUsingJql` 을 쓰고, 응답이 길어지지 않도록
`fields` 를 반드시 좁힌다.

**(a) 나에게 할당된 미완료 이슈**

```
jql: assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC
fields: ["summary","status","updated","duedate"]
```

**(b) 내가 멘션된 이슈 (최근 14일)**

```
jql: comment ~ "5be381ccf6f9e64e2f12a012" AND updated >= -14d ORDER BY updated DESC
fields: ["summary","updated"]
```

(b) 는 후보만 준다. 여기서 멈추지 말고 **상위 8건 정도만** `mcp__atlassian__getJiraIssue`
(`fields: ["comment"]`, `responseContentFormat: "markdown"`)로 댓글을 읽어 다음을 가린다.

- 내 accountId 가 멘션된 댓글만 남긴다.
- **작성자가 나인 댓글은 뺀다.** 내가 남을 부른 것이지 나를 부른 것이 아니다.
- 남은 것 중 **질문·결정요청·회신 요구**인지, 단순 공유인지 구분한다. 회신이 필요한데
  그 뒤로 내 댓글이 없으면 "미회신"으로 표시한다.

기간은 기본 14일이되, 사용자가 "밀린 것 전부"라고 하면 `-30d` 로 넓힌다.

제목에 `[결정요청]`, `[리뷰요청]`, `긴급`, `마감` 이 있거나 요약에 날짜가 박힌 것은
따로 뽑아 맨 위에 둔다.

## 3단계 — 로컬 원장

`HANDOFF.md`, `TODO.md`, `SESSION-LOG.md` 를 읽는다. 셋 다 `.gitignore` 대상이라
**clone 에 따라 없을 수 있고, 없는 것이 정상이다** — 없으면 "이 clone 에는 없음"이라 적는다.

- `TODO.md`: 미완료(`- [ ]`) 항목만 추린다.
- `HANDOFF.md`: "현재 상태"와 "주의" 절. 다음 세션이 밟을 함정이 여기 적혀 있다.
- `SESSION-LOG.md`: 마지막 항목 하나. 직전에 무엇을 하다 멈췄는지 확인용.

## 4단계 — 종합해서 내놓기

아래 순서로 짧게 정리한다. 각 항목은 한 줄이고, 근거(이슈 키·커밋 해시·파일명)를 붙인다.

1. **먼저 볼 것** — 마감이 임박했거나 남이 내 회신을 기다리는 것. 없으면 "없음"이라 적는다.
2. **JIRA 할당 미완료** — 상태별로 묶는다(진행 중 / 해야 할 일).
3. **미회신 멘션** — 누가, 어느 이슈에서, 무엇을 물었는지.
4. **git** — 동기화 상태와 커밋 안 된 변경.
5. **로컬 원장 미완료** — TODO 체크박스와 HANDOFF 주의 항목.
6. **막힌 것** — 남의 답을 기다리는 중이라 내가 못 움직이는 것. 내 할 일과 섞지 않는다.

마지막에 "지금 시작한다면 이것부터"로 한 가지만 추천한다. 근거를 한 줄 덧붙인다.

## 자주 틀리는 지점

- `comment ~ "<accountId>"` 는 **내가 쓴 댓글도 함께** 잡는다. 작성자 필터를 빼먹지 말 것.
- JQL `assignee = currentUser()` 는 세 프로젝트를 모두 훑는다. BIOP01 만 볼 이유가 없으면
  좁히지 않는다. 사용자가 프로젝트를 지정하면 `AND project = BIOP01` 을 붙인다.
- `fields` 를 지정해도 응답에 project·avatar 블록이 딸려 온다. 그대로 옮기지 말고
  키·요약·상태·갱신일만 뽑아 쓴다.
- 원장 3종이 없다고 해서 "할 일이 없다"로 결론 내지 말 것. 서버 clone 에만 있을 수 있다.
