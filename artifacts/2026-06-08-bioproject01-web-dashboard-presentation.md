---
marp: true
title: BioProject01 Paper Dashboard Harness
date: 2026-06-08
audience: BioProject01 teammates
format: markdown-slide-deck
paginate: true
---

# BioProject01 Paper Dashboard Harness

CLI 중심 논문 분석 하네스를 클릭 기반 웹 흐름으로 확장

2026-06-08

---

## 문제

기존 BioProject01 논문 분석은 강력했지만 진입점이 CLI와 prompt였다.

- DOI, topic, mode, lens를 매번 prompt로 작성
- Codex가 실제 실행 중인지 화면에서 확인하기 어려움
- 결과 파일은 `analysis/...`에 생기지만 팀원이 바로 열어보기 어려움
- 팀 공유 시 실행 방법과 상태 확인 절차가 구두 설명에 의존

---

## 목표

팀원이 브라우저에서 논문 분석 하네스를 실행하고 확인하게 만든다.

- 클릭으로 분석 요청 생성
- `Run in Codex`로 저장된 prompt 실행
- 같은 화면에서 실행 상태와 산출물 확인
- HTML report와 Core 분석을 새 탭에서 바로 열람
- LAN 공유와 token 기반 접근 지원

---

## 하네스 원칙

웹 대시보드는 기존 분석 규칙을 대체하지 않는다.

- 분석 계약은 그대로 `AGENTS.md`와 `skills/`가 담당
- 웹은 control surface 역할
- 모든 요청과 실행 로그는 `artifacts/`에 저장
- 최종 분석 결과는 계속 `analysis/<topic>/<paper-id>/`에 저장

---

## 구조

```text
web/
  app.py
  index.html
  static/app.js
  static/app.css
  README.md
  DEPLOY.md
  scripts/share_dashboard.sh

artifacts/
  web-runs/<run-id>/
    request.json
    prompt.md
    codex-job.json
    codex.log
```

---

## 사용자 흐름

1. DOI / URL / PDF path 입력
2. Topic, mode, lens 선택
3. `Create Run Prompt`
4. `Run in Codex`
5. 상태 카드, 파일 배지, Codex log 확인
6. `Build Index`
7. `Render HTML`
8. `View Core`

---

## Run In Codex

대시보드는 저장된 `prompt.md`를 그대로 Codex에 넘긴다.

```bash
codex exec --cd /Users/kkkim/projects/autobiox/BioProject01 -
```

기록 위치:

```text
artifacts/web-runs/<run-id>/codex-job.json
artifacts/web-runs/<run-id>/codex.log
```

---

## 상태 확인 개선

초기 버전은 실행 여부가 직관적이지 않았다.

수정 후:

- status card: `running`, `succeeded`, `failed`, `finished-unknown`
- generated-file badges: `paper-info.yaml`, `core.md`, lens, brief, HTML
- Codex log tail: 실행 버튼 바로 아래 표시
- 시스템 로그는 보조 로그로 분리

---

## 결과 보기

`Render HTML`

- `skills/core-to-html/scripts/build_html.py <paper-dir>` 실행
- 완료 후 HTML report를 새 탭에서 열기

`View Core`

- `*_core.md`를 raw Markdown으로 보여주지 않음
- 제목, 목록, 강조, 코드, 표를 HTML로 렌더링
- 새 탭에서 읽기용 문서로 표시

---

## 테스트 케이스

입력:

```text
Source: 10.1016/j.cell.2021.07.039
Topic: single-cell-genomics
Mode: full
Lens: both
```

출력:

```text
analysis/single-cell-genomics/trevino-2021-cortex
```

---

## 생성된 산출물

- `paper-info.yaml`
- `trevino-2021-cortex_core.md`
- `trevino-2021-cortex_lens-academic.md`
- `trevino-2021-cortex_lens-industry.md`
- `trevino-2021-cortex_methodology-brief.md`
- `trevino-2021-cortex_core.html`
- `analysis/_index/single-cell-genomics.md`

---

## Source Boundary

Trevino 테스트는 source-limited run이었다.

- local DNS 제한으로 Cell PDF 다운로드 실패
- abstract, publisher metadata, URL stub 기반 분석
- PDF panel, STAR Methods, supplementary 수치는 `검토필요` 또는 `미제공`

이 원칙은 하네스의 hallucination 방지 규칙과 일치한다.

---

## 팀 배포

로컬:

```bash
python3 web/app.py --port 8765
```

LAN 공유:

```bash
BIOP01_DASHBOARD_TOKEN='change-this-token' python3 web/app.py --host 0.0.0.0 --port 8765
```

간편 실행:

```bash
./web/scripts/share_dashboard.sh
```

---

## 하네스 등록

등록 위치:

- `AGENTS.md` `Web Dashboard Workflow`
- `artifacts/README.md`
- `web/README.md`
- `web/DEPLOY.md`

핵심:

- 자연어로 "웹으로 논문 분석", "클릭으로 논문 해석", "팀원에게 배포" 요청 시 `web/` 대시보드로 라우팅
- 실행 로그와 재현 문서는 `artifacts/`에 저장

---

## 남은 개선 후보

- HTML report에서 lens와 methodology brief까지 함께 여는 탭 추가
- 최근 실행 목록에서 job status badge 표시
- PDF를 브라우저에서 upload/drop하는 기능
- 팀 서버 배포 방식 고도화: reverse proxy, HTTPS, persistent process
- source-limited run과 PDF-grounded run을 UI에서 더 명확히 구분

---

## 결론

오늘 작업으로 BioProject01 논문 분석 하네스는 CLI-only에서 browser-assisted workflow로 확장됐다.

분석의 기준은 유지했다.

- source grounding 유지
- `analysis/` 산출물 계약 유지
- `skills/` workflow 유지

사용 경험만 바뀌었다.

- 입력은 클릭으로
- 실행 상태는 같은 화면에서
- 결과는 새 탭에서 바로 확인

---

## 부록 (2026-06-09): Claude Code 포팅

같은 하네스를 Codex 전용에서 Claude Code에서도 네이티브로 실행하도록 확장했다.

- 분석 규칙의 single source of truth는 그대로 `AGENTS.md` + `skills/*/SKILL.md`
- 추가한 것은 Claude가 자동 인식하는 얇은 등록 레이어뿐

---

## 포팅 매핑

| 레이어 | Codex | Claude |
| --- | --- | --- |
| 스킬 | `skills/*/SKILL.md` 16 | `.claude/skills/*` (committed 복사본) |
| 에이전트 | `skills/*/agents/openai.yaml` 7 | `.claude/agents/*.md` 7 |
| 라우터 | `AGENTS.md` | `CLAUDE.md` → AGENTS.md 위임 |

포팅한 에이전트 7개: Abstract Analysis, Full Background, Full Results, Full Figure, Full Discussion, Full Slides, Question.

---

## 웹/팀 적용 조건

- `.claude/`는 원래 per-machine으로 git ignore → `.claude/skills`·`.claude/agents`만 예외로 공유
- skills/agents는 **세션 시작 시 로드** → commit + push 후 **새 Claude 세션**에서 적용
- 웹(claude.ai/code)은 GitHub 체크아웃이라 심볼릭 링크 대신 실제 복사본 사용

---

## 재현 검증 (Trevino 2021)

Codex 6/8 run과 같은 paper를 Claude에서 재실행해 대조.

- 출력: `analysis/single-cell-genomics/trevino-2021-cortex/claude-rerun/` (원본 보존, 비교용 별도 폴더)
- 섹션 구조 동일, source-grounding 표기 동일, 핵심 사실(GSE162170, code repo) 일치
- full PDF 미확보 경계도 `검토필요:`로 동일 처리 → hallucination 방지 규칙 유지
