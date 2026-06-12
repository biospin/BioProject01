# Codex 논문 분석 하네스를 Claude Code로 옮기고, 웹으로 굴리기까지

> 한 줄 요약: Codex CLI 전용으로 만들었던 "논문 분석 하네스"를 Claude Code에서도 그대로 돌아가게 옮기고, 브라우저에서 클릭으로 실행하는 대시보드와 튜토리얼을 붙인 기록. 같은 하네스를 두 엔진(Codex·Claude)으로 굴린다.
>
> 형식 메모: 이 파일은 **읽는 블로그(산문)** 다. 발표용 슬라이드는 `2026-06-08-bioproject01-web-dashboard-presentation.md`(Marp)로 따로 둔다. 내용은 공유하되 형식만 분리.

---

## 0. 하네스가 뭔가 (직관적으로)

"하네스(harness)"는 거창한 게 아니다. **AI가 같은 일을 매번 같은 품질로 반복하도록 짜둔 작업 틀**이다. 사람이 매번 "이 논문 이렇게 분석해줘"를 길게 설명하는 대신, 규칙을 파일로 박아두고 한 줄만 던진다.

이 프로젝트(BioProject01)의 하네스는 **논문 한 편을 받아 구조화된 분석 노트로 바꾸는 일**을 자동화한다. 핵심 부품은 셋이다.

```
라우터        무엇을 언제 할지 정하는 안내판
  AGENTS.md   (Codex용)   ─┐  둘은 같은 규칙을 가리킴
  CLAUDE.md   (Claude용)  ─┘  (CLAUDE.md는 AGENTS.md에 위임)

스킬          실제 작업 단위 (각 SKILL.md가 규칙 1개)
  source-grounding   원문만 근거로 쓰게 막는 규칙 (환각 방지)
  core-problem / core-methods / core-results / core-figure / core-table
  lens-academic      학계 시선 해석
  lens-industry      산업 시선 해석
  methodology-brief  재현용 압축 요약
  ... (총 16개)

산출물 계약    결과가 항상 같은 자리·같은 형식으로 떨어짐
  analysis/<topic>/<paper-id>/
    paper-info.yaml          (single source of truth)
    <paper-id>_core.md        (객관적 분석)
    <paper-id>_lens-academic.md / _lens-industry.md
    <paper-id>_methodology-brief.md
    sources/                  (원문 PDF·supplementary)
```

한 줄 입력(`DOI: 10.xxxx 분석해줘`)이면 폴더 생성 → 원문 수집 → core/lens/brief 작성 → 인덱스 갱신 → HTML 리포트까지 흐른다.

**가장 중요한 규칙 하나**: `sources/`에 있는 원문만 근거로 쓴다. 본문에 없는 수치·추측은 `해석:` / `추정:` / `검토필요:`로 분리 표기한다. 이게 "AI가 그럴듯하게 지어내는" 걸 막는 장치다.

---

## 왜 옮겼나

원래 이 하네스는 **Codex CLI 전용**이었다. 라우터(`AGENTS.md`), 스킬(`skills/*/SKILL.md`), 그리고 Codex가 인식하는 에이전트 정의(`skills/*/agents/openai.yaml`)로 짜여 있었다. 같은 작업을 **Claude Code에서도** 하고 싶어졌다. 분석 규칙을 다시 짜는 게 아니라, **같은 규칙을 Claude가 알아보게 등록**만 하면 되는 일이었다.

아래는 실제로 진행한 스텝이다.

---

## Step 1 — Codex 하네스를 Claude로 포팅

Codex와 Claude는 "스킬·에이전트를 어디서 읽는지"가 다르다.

| | Codex | Claude Code |
|---|---|---|
| 스킬 위치 | `skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` |
| 에이전트 | `skills/*/agents/openai.yaml` | `.claude/agents/*.md` |
| 라우터 | `AGENTS.md` | `CLAUDE.md` |

그래서 한 일:

- **스킬 16개**를 Claude가 자동 인식하는 `.claude/skills/`에 등록. 실행 스크립트(`build_index.py` 등)는 원본 `skills/`를 그대로 참조해서 **중복 없이** 정의(SKILL.md)만 둔다.
- **에이전트 7개**: Codex의 `openai.yaml`(Abstract Analysis, Full Background, Full Results, Full Figure, Full Discussion, Full Slides, Question)을 Claude subagent(`.claude/agents/*.md`)로 변환. 각 에이전트는 자기 SKILL.md + 라우터 + source-grounding 규칙을 읽고 작업한다.
- **`CLAUDE.md`**: 규칙을 복사하지 않고 `AGENTS.md`에 위임. "단일 진실 원천(single source of truth)"을 하나로 유지하기 위함.

> 핵심 원칙: 규칙은 한 곳(`AGENTS.md` + `skills/`)에만 둔다. Claude용 레이어는 "얇은 등록"일 뿐. 한쪽만 고치면 두 환경이 어긋나기 때문.

---

## Step 2 — 같은 논문으로 재현 검증

포팅이 "진짜 되는지"는 같은 입력으로 같은 결과가 나오는지로 확인한다. Codex로 분석했던 Cell 2021 논문(Trevino et al., human cortex)을 Claude에서 다시 돌려, 원본을 덮어쓰지 않고 `claude-rerun/` 폴더에 따로 저장해 비교했다.

결과: 섹션 구조 동일, `해석:`/`외부 맥락:`/`검토필요:` 같은 source-grounding 표기 동일, 핵심 사실(GEO 번호, 코드 저장소) 일치. 포팅이 형식만이 아니라 **동작까지** 같음을 확인.

---

## Step 3 — 웹 대시보드 + 인터랙티브 튜토리얼

CLI는 강력하지만 팀원이 쓰기엔 진입장벽이 있다. 그래서 브라우저에서 클릭으로 굴리는 대시보드(`web/`, 파이썬 표준 라이브러리만 사용)를 붙였다.

- 자료 입력(DOI·URL·PDF 업로드) → 요청 만들기 → 실행 → 상태·생성 파일 배지·로그 확인 → HTML 리포트 열기.
- 화면을 "기능 목록"이 아니라 **작업 순서**(1. 자료 입력 → 2. 실행 → 3. 결과 확인)로 재배치.
- **인터랙티브 튜토리얼**: 첫 방문 시 우측 하단에 6단계 가이드가 자동으로 뜨고, 각 단계가 해당 화면 영역을 강조한다. `❓ 튜토리얼` 버튼으로 언제든 다시 본다. (브라우저 `localStorage`에 본 기록을 남겨 다음부터는 자동으로 안 뜬다.)

> 원칙: 대시보드는 분석 규칙을 **대체하지 않는다**. 입력을 모으고 실행을 켜는 "조작판"일 뿐, 실제 분석은 그대로 `skills/` 규칙과 `analysis/` 산출물 계약을 따른다.

---

## Step 4 — 대시보드에서 Claude로도 실행

대시보드는 처음엔 Codex만 호출했다(`codex exec`). 이제 **Claude로도** 실행한다.

- 백엔드를 "엔진 무관(engine-aware)"으로 일반화: `ENGINES` 설정 하나로 Codex/Claude의 명령·로그·작업 파일을 분기. 한 요청에 두 엔진을 **독립적으로** 돌릴 수 있다(`<run_id>:<engine>` 키로 분리).
- Claude 실행: `claude -p --dangerously-skip-permissions` (프롬프트를 stdin으로, 저장소를 작업 폴더로). 무인 실행이라 Codex의 자율 실행과 동일하게 승인 게이트 없이 돈다.
- 화면엔 `Claude로 분석`(기본)·`Codex로 분석` 두 버튼. 상태 카드·로그는 누른 엔진에 맞춰 표시.

> 실전 교훈: Codex(ChatGPT 플랜)는 사용량 한도가 있어 분석 도중 `usage limit`으로 죽을 수 있다. Claude 엔진을 붙여 두면 한도와 무관하게 계속 굴릴 수 있다.

---

## Step 5 — 디테일 두 가지 보정

써보니 걸리는 지점 둘을 고쳤다.

1. **paper 행의 "분석" 버튼이 조용히 Codex를 썼다** → Codex 한도가 차면 그 버튼만 계속 실패. 이제 `Claude로 분석`으로 동작하고 라벨도 그렇게 바꿈.
2. **업로드한 PDF가 분석 폴더에 안 남았다** → 업로드본은 `artifacts/uploads/`에만 저장돼서, 하네스가 PDF 없이 분석하고 figure/supplementary를 `검토필요:`로 남겼다. 이제 Source가 로컬 PDF면 프롬프트가 "분석 폴더를 만든 뒤 그 PDF를 `sources/`로 복사해 1차 근거로 쓰라"고 명시한다.

---

## 옮기면서 새로 배운 점 (요점)

- **단일 진실 원천**: 규칙은 한 곳에. Claude 레이어는 얇은 등록만. 안 그러면 두 환경이 갈라진다.
- **세션 로드 타이밍**: `.claude/skills`·`.claude/agents`는 **세션 시작 때 한 번** 읽힌다. 새로 추가하면 **새 세션**을 열어야 인식된다.
- **웹은 곧 GitHub**: claude.ai/code(웹)는 로컬 디스크가 아니라 저장소를 읽는다. 커밋·푸시하지 않으면 웹 세션엔 안 보인다. (그래서 `.claude/`는 per-machine로 무시하되 `skills`·`agents`만 공유 예외로 열었다.)
- **자율 실행 플래그는 신중히**: `--dangerously-skip-permissions`는 승인 게이트를 모두 끈다. 무인 대시보드엔 필요하지만, 무엇이 켜지는지 알고 쓴다.
- **원문에 충실(source-grounding)**: PDF가 폴더에 실제로 있어야 그림·표·supplementary까지 검증된다. 없으면 정직하게 `검토필요:`로 남긴다 — 지어내지 않는다.

---

## 지금 상태 / 다음

- 하네스 Claude 포팅, 웹 대시보드, 튜토리얼: 완료·반영.
- 대시보드 Claude 실행 엔진, 위 두 보정: 추가 완료.
- 한 줄로 다시 정리하면 — **"같은 논문 분석 하네스를, CLI에서도 웹에서도, Codex로도 Claude로도 굴릴 수 있게 되었다."**

<!-- 업데이트 로그: 새 작업이 생기면 위 Step에 이어서 항목을 추가하고 이 줄 위에 날짜를 남긴다. -->
<!-- 2026-06-09: Step 1~5 작성 (포팅·재현·대시보드·튜토리얼·Claude 엔진·두 보정). -->
